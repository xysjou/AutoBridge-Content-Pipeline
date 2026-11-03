"""Crash, race and canonical-boundary checks; no credentials or network."""
import base64
import copy
import unittest
import json
from contextlib import nullcontext
from unittest.mock import patch
from urllib.parse import unquote
from cloud_pilot.contract import digest,GateError
from cloud_pilot.multilingual.editorial_state import EditorialState
from cloud_pilot.multilingual.accounting import ResponseJournal
from cloud_pilot.multilingual.tests.test_multilingual import ArtifactStore,GitHub
from cloud_pilot.multilingual.tests.test_editorial_controls import active_case
from cloud_pilot.live.stages import check_research,check_writing
from cloud_pilot.stage2_tests.test_live import plan,history,writer_result
from cloud_pilot.live.engine import Engine
from cloud_pilot.multilingual.publication import seal_research,complete_research,persist_failed_research,verify_research,writing_files,blob_hash,recover_publication

class GitMemory:
    prefix='/repos/synthetic/repo'
    def __init__(self):
        self.api=self;self.refs={'main':'a'*40};self.trees={'base':{}};self.commits={'a'*40:dict(tree='base')};self.creates=0
    def ref(self,b):return self.refs[b]
    def request(self,method,path,payload=None):
        path=path.removeprefix(self.prefix)
        if path.startswith('/git/ref/heads/'):
            branch=unquote(path.split('/git/ref/heads/',1)[1])
            return (200,dict(object=dict(sha=self.refs[branch]))) if branch in self.refs else (404,{})
        return 200,self.call(method,path,payload)
    def call(self,method,path,payload=None,expected=200):
        if path.startswith('/git/commits/'):return dict(tree=dict(sha=self.commits[path.rsplit('/',1)[1]]['tree']))
        if method=='POST' and path=='/git/trees':
            files=copy.deepcopy(self.trees[payload['base_tree']]);files.update({e['path']:e['content'].encode() for e in payload['tree']})
            sha=digest({p:blob_hash(b) for p,b in files.items()})[:40];self.trees[sha]=files;return dict(sha=sha)
        if method=='POST' and path=='/git/commits':
            sha=digest(payload)[:40];self.commits[sha]=dict(tree=payload['tree'],message=payload['message'],parent=payload['parents'][0]);return dict(sha=sha)
        if method=='POST' and path=='/git/refs':
            self.creates+=1;self.refs[payload['ref'].removeprefix('refs/heads/')]=payload['sha'];return dict(object=dict(sha=payload['sha']))
        if path.startswith('/commits/'):
            sha=path.split('?',1)[0].rsplit('/',1)[1];c=self.commits[sha]
            before=self.trees[self.commits[c['parent']]['tree']]
            return dict(sha=sha,parents=[dict(sha=c['parent'])],commit=dict(message=c['message']),files=[dict(filename=p,status='added' if p not in before else 'modified',sha=blob_hash(b)) for p,b in self.trees[c['tree']].items() if before.get(p)!=b])
        if path.startswith('/contents/'):
            name,ref=path.removeprefix('/contents/').split('?ref=');sha=self.refs.get(unquote(ref),unquote(ref));body=self.trees[self.commits[sha]['tree']][name]
            return dict(encoding='base64',content=base64.b64encode(body).decode(),sha=blob_hash(body))
        raise AssertionError((method,path))

def research(hash='one',version=1,start=None):
    r=dict(article_id='PILOT-RACE',version=version,research_hash=hash,fact_sheet={'handoff':{}})
    if start:r['research_start']=start
    return r

class Tests(unittest.TestCase):
    def test_research_head_and_ready_resume_as_one_atomic_commit(self):
        class CrashStore(ArtifactStore):
            crash=False
            def cas(self,expected,data):
                result=super().cas(expected,data)
                if self.crash:self.crash=False;raise GateError('CRASH_AFTER_COMMIT')
                return result
        store=CrashStore();s=EditorialState(ResponseJournal(store));start=s.begin('PILOT-RACE','one');r=research(start=start)
        store.crash=True
        with self.assertRaisesRegex(GateError,'CRASH_AFTER_COMMIT'):s.register(r)
        before=len(store.data['events']);s.register(r)
        self.assertEqual(before,len(store.data['events']));s.lock(r);s.check(r)

    def test_new_research_attempt_supersedes_pending_fence_monotonically(self):
        s=EditorialState(ResponseJournal(ArtifactStore()));one=s.begin('PILOT-RACE','first');two=s.begin('PILOT-RACE','second')
        self.assertEqual((1,2),(one['version'],two['version']))
        with self.assertRaisesRegex(GateError,'SUPERSEDED'):s.register(research(start=one))
        r=research('two',2,two);s.lock(r);s.check(r)

    def test_research_cannot_interleave_with_publication_and_release_is_idempotent(self):
        s=EditorialState(ResponseJournal(ArtifactStore()));r=research();s.lock(r)
        token=s.begin_publication([r],'draft-owner');before=s.snapshot()
        with self.assertRaisesRegex(GateError,'DEFERRED'):s.begin(r['article_id'],'replacement')
        self.assertEqual(before,s.snapshot());s.end_publication(token);s.end_publication(token)
        s.begin(r['article_id'],'replacement')
        with self.assertRaisesRegex(GateError,'RESEARCH_LOCK_UPDATE_REQUIRED'):s.check(r)

    def test_engine_locks_before_source_collection_and_keeps_lock_on_failure(self):
        p=plan();topic,_,_=active_case('VEHICLE_RECOMMENDATION');topic['research_baseline_sha']='a'*40;p['articles'][0]=topic
        j=ResponseJournal(ArtifactStore());state=EditorialState(j)
        class Models:
            def call(self,*args):raise AssertionError('SOURCE_FAILURE_MUST_PREVENT_MODELS')
        def fetch(*args):
            self.assertIsNotNone(state.snapshot()['articles'][topic['article_id']]['research_lock'])
            raise GateError('SOURCE_LIMITATION')
        with self.assertRaisesRegex(GateError,'SOURCE_LIMITATION'):Engine(p,history(),j,Models(),GitMemory(),fetch).run()
        self.assertIsNotNone(state.snapshot()['articles'][topic['article_id']]['research_lock'])

    def test_pushed_research_has_canonical_files_and_actual_commit_baseline(self):
        topic,ev,result=active_case('VEHICLE_RECOMMENDATION');topic['research_baseline_sha']='a'*40
        result['content']['handoff']['research_baseline_sha']='a'*40
        raw=check_research(result,topic,ev);gh=GitMemory();sealed=seal_research(gh,raw,dict(article_id=topic['article_id'],attempt='test',version=1,fence='test'))
        verify_research(gh,sealed);again=seal_research(gh,raw,sealed['research_start'])
        self.assertEqual(sealed,again);self.assertEqual(gh.creates,1)
        self.assertTrue(all(p.startswith('daily/2026-11-03/research/') for p in sealed['completion']['files']))
        self.assertFalse(sealed['fact_sheet']['writing_ai_ready']);self.assertTrue(sealed['fact_sheet']['handoff']['research_locked'])
        sealed=complete_research(gh,sealed,dict(research_hash=sealed['research_hash'],verdict=dict(decision='ACCEPT')))
        verify_research(gh,sealed);self.assertTrue(sealed['fact_sheet']['writing_ai_ready'])
        self.assertTrue(any(p.endswith('/INDEPENDENT_REVIEW.json') for p in sealed['completion']['files']))
        response=writer_result(sealed);response['content']['skill_impact']=result['content']['handoff']['skill_impact']
        response['content']['review_handoff_assessment']=result['content']['handoff']['review_handoff_assessment']
        article=check_writing(response,sealed,1,history(),[])
        self.assertEqual(article['research_baseline_sha'],sealed['completion']['commit_sha'])
        sha=sealed['completion']['commit_sha'];tree=gh.commits[sha]['tree'];path=next(iter(gh.trees[tree]));gh.trees[tree][path]+=b'changed'
        with self.assertRaisesRegex(GateError,'COMPLETE_DIFF|BODY_CHANGED'):verify_research(gh,sealed)

    def test_failed_nonready_research_keeps_canonical_sources_and_blocked_facts(self):
        topic,ev,result=active_case('BUYING_GUIDE');topic['research_baseline_sha']='a'*40
        result['content'].update(status='RESEARCH_FAIL',writing_ai_ready=False,blocked_facts=['unsupported'])
        gh=GitMemory();failed=persist_failed_research(gh,result,topic,ev,dict(version=1),GateError('FACT_MISSING'))
        verify_research(gh,failed);self.assertEqual(ev,failed['evidence'])
        self.assertIn('unsupported',failed['fact_sheet']['blocked_facts'])
        self.assertFalse(failed['fact_sheet']['writing_ai_ready'])
        self.assertEqual(5,len(failed['completion']['files']))

    def test_valid_nonready_conditional_verdict_is_preserved(self):
        topic,ev,result=active_case('BUYING_GUIDE');topic['research_baseline_sha']='a'*40
        result['content']['handoff']['research_baseline_sha']='a'*40
        result['content'].update(status='RESEARCH_CONDITIONAL',writing_ai_ready=False)
        packet=check_research(result,topic,ev);packet['research_phase']='WITHHELD'
        gh=GitMemory();sealed=seal_research(gh,packet,dict(version=1))
        self.assertEqual('RESEARCH_CONDITIONAL',sealed['fact_sheet']['status'])
        self.assertFalse(sealed['fact_sheet']['writing_ai_ready']);verify_research(gh,sealed)

    def test_source_failure_at_every_position_keeps_available_evidence_and_handoff(self):
        for position in range(6):
            with self.subTest(position=position):
                p=plan();topic,ev,_=active_case('BUYING_GUIDE');topic['research_baseline_sha']='a'*40;p['articles'][0]=topic
                j=ResponseJournal(ArtifactStore());gh=GitMemory();calls=[]
                def fetch(source,allowed):
                    i=len(calls);calls.append(source['source_id'])
                    if i==position:raise GateError('SOURCE_ACCESS_FAILED')
                    return copy.deepcopy(ev[i]),ev[i]['text'].encode()
                gh.put_immutable=lambda *args:'synthetic-raw-blob'
                class Models:
                    def call(self,*args):raise AssertionError('FAILED_SOURCE_MUST_NOT_GENERATE')
                with self.assertRaisesRegex(GateError,'SOURCE_ACCESS_FAILED'):Engine(p,history(),j,Models(),gh,fetch).run()
                record=j.get_checkpoint('failed-source-research:'+topic['article_id'])
                self.assertEqual(position,len(record['evidence']));self.assertFalse(record['fact_sheet']['writing_ai_ready'])
                self.assertEqual(topic['sources'][position]['source_id'],record['fact_sheet']['access_failure']['failed_source']['source_id'])
                verify_research(gh,record)

    def test_complete_accepted_source_log_and_handoff_fields(self):
        from cloud_pilot.multilingual.publication import research_files
        topic,ev,result=active_case('BUYING_GUIDE');topic['research_baseline_sha']='a'*40
        result['content']['handoff']['research_baseline_sha']='a'*40;gh=GitMemory()
        proposal=seal_research(gh,check_research(result,topic,ev),dict(version=1))
        complete=complete_research(gh,proposal,dict(research_hash=proposal['research_hash'],verdict=dict(decision='ACCEPT')))
        files=research_files({k:v for k,v in complete.items() if k!='completion'})
        log=json.loads(next(b for p,b in files.items() if p.endswith('/SOURCE_LOG.json')))
        handoff=json.loads(next(b for p,b in files.items() if p.endswith('/HANDOFF.json')))
        self.assertTrue(all(s['SOURCE_TITLE'] and s['SUPPORTED_FACT'] and s['CONFIDENCE'] for s in log))
        self.assertEqual(6,handoff['SOURCE_URL_COUNT']);self.assertTrue(handoff['FACTS_ALLOWED_IN_BODY'])
        self.assertTrue(handoff['WRITING_AI_READY']);self.assertIn('FACT_BOUNDARY_STATUS',handoff)

    def test_writing_startup_reads_actual_manifest_and_research_completion(self):
        from cloud_pilot.multilingual.publication import push_startup_manifest,sync_batch_manifest
        from cloud_pilot.multilingual.startup import writing_startup,lesson_ids
        topic,ev,result=active_case('BUYING_GUIDE');topic['research_baseline_sha']='a'*40
        result['content']['handoff']['research_baseline_sha']='a'*40
        from cloud_pilot.contract import rules
        p=dict(articles=[topic],execution_phase='english',rules=rules());gh=GitMemory()
        startup=dict(approved_main_sha='a'*40,execution_sha='a'*40,startup_gate=dict(REPO_HEAD_SHA='a'*40,LESSONS_LEARNED_SHA='b'*40))
        startup['canonical_daily_manifest']=push_startup_manifest(gh,startup,p,'synthetic-run')
        raw=check_research(result,topic,ev);raw['startup_gate']=startup;p['rules']=raw['rules']
        j=ResponseJournal(ArtifactStore());state=EditorialState(j);start=state.begin(topic['article_id'],'initial')
        proposal=seal_research(gh,raw,start)
        rows=[dict(lesson_id=k,applicable=False,triggered=False,reason='Synthetic verified lesson') for k in lesson_ids()]
        complete=complete_research(gh,proposal,dict(research_hash=proposal['research_hash'],verdict=dict(decision='ACCEPT',lesson_assessments=rows)))
        j.checkpoint('research:'+topic['article_id'],complete);state.lock(complete)
        manifest=sync_batch_manifest(gh,j,p,startup)
        writes=[];gh.put_canonical_qa=lambda path,body:writes.append((path,json.loads(body)))
        with patch('cloud_pilot.multilingual.startup.verify',return_value=copy.deepcopy(startup)) as sync:
            record=writing_startup('a'*40,p,complete,gh,manifest)
        sync.assert_called_once_with('a'*40,p)
        self.assertEqual(complete['completion']['commit_sha'],record['RESEARCH_BASELINE_SHA'])
        self.assertTrue(all(record['checklist'].values()));self.assertEqual(1,len(writes))
        with patch('cloud_pilot.multilingual.startup.verify',return_value=copy.deepcopy(startup)),self.assertRaisesRegex(GateError,'MANIFEST_RESEARCH_DRIFT'):
            writing_startup('a'*40,p,complete,gh,startup['canonical_daily_manifest'])

    def test_pending_other_article_can_resume_without_mutation_during_delivery(self):
        j=ResponseJournal(ArtifactStore());s=EditorialState(j);r=research();s.lock(r)
        pending=s.begin('PILOT-OTHER','initial');token=s.begin_publication([r],'english:fixture')
        before=s.snapshot();self.assertEqual(pending,s.begin('PILOT-OTHER','initial'))
        self.assertEqual(before,s.snapshot())
        with self.assertRaisesRegex(GateError,'DEFERRED'):s.begin('PILOT-OTHER','new-attempt')
        s.end_publication(token)

    def test_transfer_failure_invalidates_only_affected_article(self):
        from cloud_pilot.multilingual.source_cache import SourceTransferFailure
        from cloud_pilot.multilingual.publication import record_transfer_failure
        j=ResponseJournal(ArtifactStore());s=EditorialState(j);one=research();two=research('two');two['article_id']='PILOT-OTHER'
        s.lock(one);s.lock(two);unaffected=copy.deepcopy(s.snapshot()['articles']['PILOT-OTHER'])
        topic,ev,_=active_case('BUYING_GUIDE');topic.update(article_id=one['article_id'],research_baseline_sha='a'*40)
        error=SourceTransferFailure(dict(article_id=one['article_id'],partial=ev[:2],source=dict(source_id='S2',url=topic['sources'][2]['url'])),GateError('RAW_CONTENT'))
        failed=record_transfer_failure(GitMemory(),j,dict(articles=[topic]),{},error)
        self.assertEqual(2,len(failed['evidence']));self.assertEqual('S2',failed['fact_sheet']['access_failure']['failed_source']['source_id'])
        self.assertEqual(unaffected,s.snapshot()['articles']['PILOT-OTHER']);s.check(two)

    def test_commit_file_pagination_73_and_173_files(self):
        from cloud_pilot.multilingual.delivery import VerifiedGitHub
        from cloud_pilot.multilingual.publication import verify_files
        for count in (73,173):
            files={f'deliveries/test/{i}.md':str(i).encode() for i in range(count)};pages=[]
            class API:
                host='api.github.com'
                def request(self,method,path,payload=None):
                    if '/commits/' in path:
                        page=int(path.rsplit('page=',1)[1]);pages.append(page)
                        changes=[dict(filename=p,status='added',sha=blob_hash(b)) for p,b in files.items()]
                        return 200,dict(sha='a'*40,parents=[dict(sha='b'*40)],commit=dict(message='fixture'),files=changes[(page-1)*100:page*100])
                    name=path.split('/contents/',1)[1].split('?ref=')[0];body=files[name]
                    return 200,dict(encoding='base64',sha=blob_hash(body),content=base64.b64encode(body).decode())
            verify_files(VerifiedGitHub(API()),'a'*40,files,'fixture','b'*40)
            self.assertEqual([1] if count==73 else [1,2],pages)

    def test_73_file_bundle_verifies_before_ref_and_recovers_interrupted_read(self):
        from cloud_pilot.multilingual.publication import publish_delivery_bundle
        from cloud_pilot.live.policy import BRANCH
        class GH(GitMemory):
            fail=True;reads=0
            def request(self,method,path,payload=None):
                try:return super().request(method,path,payload)
                except KeyError:return 404,{}
            def call(self,method,path,payload=None,expected=200):
                if method=='PATCH' and path.startswith('/git/refs/heads/'):
                    self.refs[unquote(path.split('/git/refs/heads/',1)[1])]=payload['sha'];return {}
                if path.startswith('/contents/'):
                    self.reads+=1
                    if self.fail and self.reads==31:raise GateError('INTERRUPTED_VERIFICATION')
                return super().call(method,path,payload,expected)
        gh=GH();gh.refs[BRANCH]='a'*40
        files={f'deliveries/2026-11-03/api-pilot/bundle/i18n/en/{i}.md':str(i).encode() for i in range(72)}
        with self.assertRaisesRegex(GateError,'INTERRUPTED_VERIFICATION'):publish_delivery_bundle(gh,files,'bundle')
        self.assertEqual('a'*40,gh.refs[BRANCH])
        gh.fail=False;published=publish_delivery_bundle(gh,files,'bundle');self.assertEqual(72,len(published))
        sha=gh.refs[BRANCH];self.assertNotEqual('a'*40,sha)
        self.assertEqual(published,publish_delivery_bundle(gh,files,'bundle'));self.assertEqual(sha,gh.refs[BRANCH])

    def test_new_epoch_failure_manifest_and_unaffected_head_in_actual_engine(self):
        from cloud_pilot.multilingual.startup import EpochJournal
        from cloud_pilot.multilingual.source_cache import SourceTransferFailure
        for mode in ('source','malformed','conditional'):
            with self.subTest(mode=mode):
                topic,ev,response=active_case('BUYING_GUIDE');topic['research_baseline_sha']='a'*40
                response['content']['handoff'].update(research_baseline_sha='a'*40,fact_sheet_version=2,source_log_version=2)
                if mode=='conditional':response['content'].update(status='RESEARCH_CONDITIONAL',writing_ai_ready=False)
                if mode=='malformed':response=dict(content={})
                p=plan();p['articles'][0]=topic;j=ResponseJournal(ArtifactStore());s=EditorialState(j);gh=GitMemory()
                old=EpochJournal(j,1,{'old_code':'a'*40});old_state=EditorialState(old)
                from cloud_pilot.multilingual.tests.test_editorial_controls import Tests as FactTests
                from cloud_pilot.multilingual.research_contract import accept
                # Build actual accepted prior packets, completion commits and
                # journal checkpoints; never substitute placeholder heads.
                prior=[]
                for i,kind in enumerate(('BUYING_GUIDE','BUYING_GUIDE')):
                    old_topic,old_ev,old_response=active_case(kind)
                    if i:
                        for key in ('article_id','search_intent','buyer_task','topic_key','proposed_url'):
                            old_topic[key]=p['articles'][1][key]
                        p['articles'][1]=old_topic
                    old_topic['research_baseline_sha']='a'*40
                    old_response['content']['handoff'].update({k:old_topic[k] for k in ('article_id','content_type','search_intent','buyer_task')})
                    old_response['content']['handoff']['research_baseline_sha']='a'*40
                    start=old_state.begin(old_topic['article_id'],old.prefix+':'+old_topic['article_id'])
                    proposal=seal_research(gh,check_research(old_response,old_topic,old_ev),start)
                    checked=accept(FactTests().acceptance(proposal),proposal)
                    packet=complete_research(gh,proposal,checked);old.checkpoint('research:'+old_topic['article_id'],packet);old_state.lock(packet);prior.append(packet)
                first,second=prior
                unchanged=copy.deepcopy(s.snapshot()['articles'][second['article_id']])
                epoch=EpochJournal(j,2,{'new_code':'f'*40})
                startup=dict(approved_main_sha='a'*40,execution_sha='a'*40,startup_gate={})
                class Models:
                    def call(self,*args):
                        if mode=='source':raise AssertionError('SOURCE_MUST_STOP_MODELS')
                        return response
                def prepare(t):
                    if mode=='source':raise SourceTransferFailure(dict(article_id=t['article_id'],partial=ev[:1],
                        source=dict(source_id='S1',url=t['sources'][1]['url'])),GateError('RAW_SOURCE_FAILURE'))
                evidence_patch=patch.object(Engine,'evidence',return_value=ev) if mode!='source' else nullcontext()
                with evidence_patch,patch('cloud_pilot.multilingual.startup.verify',return_value=startup),self.assertRaises(GateError):
                    Engine(p,history(),epoch,Models(),gh,None,startup=startup,prepare_evidence=prepare).run()
                self.assertEqual(unchanged,s.snapshot()['articles'][second['article_id']]);s.check(second)
                keys=[k for k in j.read()[2]['checkpoints'] if k.startswith(epoch.prefix+'batch-manifest-current:')]
                ref=j.get_checkpoint(max(keys,key=lambda k:int(k.rsplit(':',1)[1])))
                obj=gh.call('GET','/contents/'+ref['path']+'?ref='+ref['commit_sha']);manifest=json.loads(base64.b64decode(obj['content']))
                self.assertEqual(1,manifest['WRITING_READY_COUNT']);self.assertEqual(1,manifest['MAIN_PASS_COUNT'])
                self.assertEqual(1,manifest['MAIN_CONDITIONAL_COUNT'] if mode=='conditional' else manifest['MAIN_FAIL_COUNT'])
                self.assertEqual(2,manifest['articles'][0]['FACT_SHEET_VERSION'])
                other=manifest['articles'][1]
                self.assertEqual(old.prefix+'research:'+second['article_id'],other['ORIGIN_RESEARCH_CHECKPOINT'])
                self.assertEqual(second['completion']['commit_sha'],other['RESEARCH_COMPLETE_COMMIT_SHA'])

    def test_cached_delivery_source_failure_also_updates_current_manifest(self):
        from cloud_pilot.multilingual.source_cache import SourceTransferFailure
        topic,ev,response=active_case('BUYING_GUIDE');topic['research_baseline_sha']='a'*40
        response['content']['handoff']['research_baseline_sha']='a'*40
        p=plan();p['articles'][0]=topic;j=ResponseJournal(ArtifactStore());s=EditorialState(j);gh=GitMemory()
        start=s.begin(topic['article_id'],'initial');proposal=seal_research(gh,check_research(response,topic,ev),start)
        complete=complete_research(gh,proposal,dict(research_hash=proposal['research_hash'],verdict=dict(decision='ACCEPT')))
        s.lock(complete);j.checkpoint('research:'+topic['article_id'],complete);j.checkpoint('delivery:'+topic['article_id'],dict(draft=True))
        def prepare(t):raise SourceTransferFailure(dict(article_id=t['article_id'],partial=[],source=dict(source_id='S0',url=t['sources'][0]['url'])),GateError('SOURCE_RECHECK_FAILED'))
        startup=dict(approved_main_sha='a'*40,execution_sha='a'*40,startup_gate={})
        class Models:
            def call(self,*args):raise AssertionError('STALE_DELIVERY_MUST_NOT_GENERATE')
        with self.assertRaisesRegex(GateError,'SOURCE_RECHECK_FAILED'):Engine(p,history(),j,Models(),gh,None,startup=startup,prepare_evidence=prepare).run()
        keys=[k for k in j.read()[2]['checkpoints'] if k.startswith('batch-manifest-current:')]
        ref=j.get_checkpoint(max(keys,key=lambda k:int(k.rsplit(':',1)[1])))
        obj=gh.call('GET','/contents/'+ref['path']+'?ref='+ref['commit_sha']);manifest=json.loads(base64.b64decode(obj['content']))
        self.assertEqual(1,manifest['MAIN_FAIL_COUNT']);self.assertEqual(0,manifest['WRITING_READY_COUNT'])

    def test_live_localizer_fences_both_paid_stages_against_research(self):
        from cloud_pilot.multilingual.localize import Localizer,validate
        from cloud_pilot.multilingual.tests.test_multilingual import translation,locale_review
        from cloud_pilot.stage2_tests.test_live import packets
        _,_,_,base=packets();r=research();r['topic']={'content_type':'BUYING_GUIDE','proposed_url':'/pilot-only/test'};r['evidence']=[]
        r['research_hash']=base['research_hash'];j=ResponseJournal(ArtifactStore());s=EditorialState(j)
        r['research_start']=s.begin(r['article_id'],'initial');s.lock(r)
        outer=self;calls=[]
        class Models:
            def call(self,op,stage,data):
                calls.append(stage)
                with outer.assertRaisesRegex(GateError,'DEFERRED'):s.begin(r['article_id'],'concurrent')
                if stage=='writing':return translation(base,'fr')
                return locale_review(data['article'],base)
        Localizer(Models(),j).run(base,r,'fr')
        self.assertEqual(['writing','review'],calls);self.assertIsNone(s.snapshot()['publication'])

    def test_live_english_fences_writing_and_review_starts(self):
        from cloud_pilot.stage2_tests.test_live import reviewer_result
        topic,ev,result=active_case('VEHICLE_RECOMMENDATION');topic['research_baseline_sha']='a'*40
        result['content']['handoff']['research_baseline_sha']='a'*40
        j=ResponseJournal(ArtifactStore());s=EditorialState(j);start=s.begin(topic['article_id'],'initial')
        gh=GitMemory();raw=check_research(result,topic,ev)
        proposal=seal_research(gh,raw,start)
        r=complete_research(gh,proposal,dict(research_hash=proposal['research_hash'],verdict=dict(decision='ACCEPT')))
        j.checkpoint('research:'+topic['article_id'],r)
        gh.deliver_candidate=lambda package:dict(draft=True)
        p=plan();p['articles'][0]=topic;outer=self;calls=[];guards=[]
        def guard():
            guards.append(True)
            if len(guards)==4:raise GateError('FIRST_ARTICLE_TEST_COMPLETE')
        class Models:
            def call(self,op,stage,data):
                calls.append(stage)
                with outer.assertRaisesRegex(GateError,'DEFERRED'):s.begin(topic['article_id'],'concurrent')
                if stage=='writing':
                    response=writer_result(r);response['content'].update(skill_impact=result['content']['handoff']['skill_impact'],
                        review_handoff_assessment=result['content']['handoff']['review_handoff_assessment'])
                    return response
                return reviewer_result(data['article'],r)
        with patch.object(Engine,'evidence',return_value=ev),self.assertRaisesRegex(GateError,'FIRST_ARTICLE_TEST_COMPLETE'):
            Engine(p,history(),j,Models(),gh,None,guard=guard).run()
        self.assertEqual(['writing','review'],calls);self.assertIsNone(s.snapshot()['publication'])

    def test_expired_evidence_abort_releases_fence_only_after_durable_invalidation(self):
        from cloud_pilot.live.policy import BRANCH
        j=ResponseJournal(ArtifactStore());s=EditorialState(j);r=research();s.lock(r)
        token=s.begin_publication([r],'multilingual:old-bundle');writes=[]
        from cloud_pilot.multilingual.delivery import VerifiedGitHub
        class API:
            host='api.github.com'
            stored=None
            def request(self,method,path,payload=None):
                if '/qa/api-pilot/publication-aborts/' not in path:return 404,{}
                if method=='GET':return (200,self.stored) if self.stored else (404,{})
                body=base64.b64decode(payload['content']);writes.append((path,json.loads(body)))
                # The fence stays active until the invalidation is persisted.
                if s.snapshot()['publication']!=token:raise AssertionError('EARLY_UNLOCK')
                self.stored=dict(sha=blob_hash(body),content=payload['content']);return 201,dict(content=dict(sha=self.stored['sha']))
        gh=VerifiedGitHub(API())
        proof=recover_publication(gh,j,dict(action='ABORT_AND_INVALIDATE',fence=token['fence'],reason='Evidence expired after delivery failure'))
        self.assertEqual('VERIFIED_INVALIDATED',proof['status']);self.assertEqual(1,len(writes))
        with self.assertRaisesRegex(GateError,'CANONICAL_QA_PATH'):gh.put_canonical_qa('daily/2026-11-03/articles/arbitrary.json',b'{}')
        with self.assertRaisesRegex(GateError,'UPDATE_REQUIRED'):s.check(r)
        self.assertEqual(2,s.begin(r['article_id'],'fresh-source-epoch')['version'])

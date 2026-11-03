"""Crash, race and canonical-boundary checks; no credentials or network."""
import base64
import copy
import unittest
import json
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
            sha=path.rsplit('/',1)[1];c=self.commits[sha]
            return dict(sha=sha,parents=[dict(sha=c['parent'])],commit=dict(message=c['message']),files=[dict(filename=p,status='added',sha=blob_hash(b)) for p,b in self.trees[c['tree']].items()])
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
        p=plan();topic,_,_=active_case('VEHICLE_RECOMMENDATION');p['articles'][0]=topic
        j=ResponseJournal(ArtifactStore());state=EditorialState(j)
        class Models:
            def call(self,*args):raise AssertionError('SOURCE_FAILURE_MUST_PREVENT_MODELS')
        def fetch(*args):
            self.assertIsNotNone(state.snapshot()['articles'][topic['article_id']]['research_lock'])
            raise GateError('SOURCE_LIMITATION')
        with self.assertRaisesRegex(GateError,'SOURCE_LIMITATION'):Engine(p,history(),j,Models(),GitHub(),fetch).run()
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
        self.assertEqual(['unsupported'],failed['fact_sheet']['blocked_facts'])
        self.assertFalse(failed['fact_sheet']['writing_ai_ready'])
        self.assertEqual(5,len(failed['completion']['files']))

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
        class GH:
            prefix='/repo';api=None
            def request(self,*a):return 404,{}
            def put_immutable(self,branch,path,body):
                self.api=self;writes.append((path,json.loads(body)))
                # The fence stays active until the invalidation is persisted.
                if s.snapshot()['publication']!=token:raise AssertionError('EARLY_UNLOCK')
        gh=GH();gh.api=gh
        proof=recover_publication(gh,j,dict(action='ABORT_AND_INVALIDATE',fence=token['fence'],reason='Evidence expired after delivery failure'))
        self.assertEqual('VERIFIED_INVALIDATED',proof['status']);self.assertEqual(1,len(writes))
        with self.assertRaisesRegex(GateError,'UPDATE_REQUIRED'):s.check(r)
        self.assertEqual(2,s.begin(r['article_id'],'fresh-source-epoch')['version'])

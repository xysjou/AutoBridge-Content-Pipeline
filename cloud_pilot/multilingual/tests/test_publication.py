"""Crash, race and canonical-boundary checks; no credentials or network."""
import base64
import copy
import unittest
from urllib.parse import unquote
from cloud_pilot.contract import digest,GateError
from cloud_pilot.multilingual.editorial_state import EditorialState
from cloud_pilot.multilingual.accounting import ResponseJournal
from cloud_pilot.multilingual.tests.test_multilingual import ArtifactStore,GitHub
from cloud_pilot.multilingual.tests.test_editorial_controls import active_case
from cloud_pilot.live.stages import check_research,check_writing
from cloud_pilot.stage2_tests.test_live import plan,history,writer_result
from cloud_pilot.live.engine import Engine
from cloud_pilot.multilingual.publication import seal_research,verify_research,writing_files,blob_hash

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
        response=writer_result(sealed);response['content']['skill_impact']=result['content']['handoff']['skill_impact']
        response['content']['review_handoff_assessment']=result['content']['handoff']['review_handoff_assessment']
        article=check_writing(response,sealed,1,history(),[])
        self.assertEqual(article['research_baseline_sha'],sealed['completion']['commit_sha'])
        sha=sealed['completion']['commit_sha'];tree=gh.commits[sha]['tree'];path=next(iter(gh.trees[tree]));gh.trees[tree][path]+=b'changed'
        with self.assertRaisesRegex(GateError,'COMPLETE_DIFF|BODY_CHANGED'):verify_research(gh,sealed)

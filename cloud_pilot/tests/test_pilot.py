import copy
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from cloud_pilot.contract import ROOT, BASELINE, GateError, digest, validate
from cloud_pilot.research import collect
from cloud_pilot.writing import write
from cloud_pilot.review import inspect, similarity
from cloud_pilot.delivery import run_one, draft_pr_request
from cloud_pilot.state import LocalFileCAS, GitHubCAS, empty, replay, append, transact, CAP_NANO_USD
from cloud_pilot.budget import reserve, settle
from cloud_pilot.adapters import OpenAIResponsesDisabled, SourceRetrievalDisabled, SearchProviderDisabled
from cloud_pilot.audit import preserved

def fixture(name="MOCK-AURORA"):
    return json.loads((ROOT / 'cloud_pilot/fixtures' / (name+'.json')).read_text())

def history():
    return json.loads((ROOT / 'cloud_pilot/evidence/history-snapshot.json').read_text())

def packets():
    h = history()
    r = collect(fixture(), h)
    a = write(r, h, [{"claim_id":f["id"],"text":f["text"]} for f in r["facts"]])
    return h, r, a

class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = LocalFileCAS(Path(self.temp.name)/'program.json')
        self.store.initialize()
        self.net = patch.object(socket.socket, 'connect', side_effect=AssertionError('NETWORK_FORBIDDEN'))
        self.net.start(); self.addCleanup(self.net.stop)

    def bad_research(self, change, message):
        p=fixture(); change(p)
        with self.assertRaisesRegex(GateError, message): collect(p, history())

    def test_two_pilots_and_idempotent_rerun(self):
        h=history()
        a=run_one(fixture(),h,self.store)
        b=run_one(fixture('MOCK-BOREAL'),h,self.store,[a['article']['body']])
        before,token=self.store.read()
        self.assertEqual(a,run_one(fixture(),h,self.store))
        self.assertEqual(token,self.store.read()[1])
        self.assertEqual(2,len(replay(before)['items']))
        self.assertTrue(all(x['status']=='DRAFT_PR_PREPARED' for x in replay(before)['items'].values()))
        self.assertEqual('MOCK_REVIEW_PASS',b['review']['decision'])
        self.assertFalse(b['review']['production_gate']['eligible'])
        self.assertIn('EN_BELOW_900_WORDS',b['review']['production_gate']['reasons'])

    def test_research_failure_stops_writing_and_cost(self):
        p=fixture();p['research_status']='RESEARCH_FAIL'
        with self.assertRaisesRegex(GateError,'RESEARCH_FAIL'):run_one(p,history(),self.store)
        v=replay(self.store.read()[0]);self.assertFalse(v['reservations'])
        self.assertEqual('RESEARCH_FAILED',v['items'][p['article_id']]['status'])

    def test_research_lock(self):
        self.bad_research(lambda p:p.update(research_lock=True),'RESEARCH_LOCKED')

    def test_blocked_fact(self):
        self.bad_research(lambda p:p['blocked_facts'].append('F1'),'ALLOWED_BLOCKED')

    def test_market_year_trim_cycle(self):
        for key in ('market','model_year','trim','powertrain','generation','test_cycle'):
            with self.subTest(key=key):self.bad_research(lambda p:p['sources'][0].update({key:'WRONG'}),'FACT_SCOPE_MISMATCH')

    def test_source_name_integrity(self):
        self.bad_research(lambda p:p['sources'][0].update(observed_publisher='different'),'SOURCE_INTEGRITY')

    def test_t2_is_not_official(self):
        self.bad_research(lambda p:p['sources'][0].update(tier='T2'),'OFFICIAL_SOURCE_COUNT')

    def test_t2_cannot_verify(self):
        self.bad_research(lambda p:p['sources'][0].update(tier='T2',official_source=False),'PRIMARY_SOURCE_REQUIRED')

    def test_source_direct_support(self):
        self.bad_research(lambda p:p['sources'][0].update(excerpt='unrelated'),'NO_DIRECT_SUPPORT')

    def test_conflicting_fact(self):
        self.bad_research(lambda p:p['facts'][0].update(confidence='CONFLICT'),'UNVERIFIED_ALLOWED')

    def test_source_scope(self):
        self.bad_research(lambda p:p['sources'][0].update(scope_match='MISMATCH'),'SOURCE_SCOPE_FAIL')

    def test_source_depth_and_normalization(self):
        def change(p):
            for s in p['sources']:s['parent_org']='one'
        self.bad_research(change,'SOURCE_DEPTH_GATE')

    def test_cross_check_same_parent(self):
        self.bad_research(lambda p:p['facts'][0].update(confidence='CROSS_CHECKED'),'SAME_FACT_CROSS_CHECK')

    def test_time_sensitive_currentness(self):
        self.bad_research(lambda p:p['facts'][0].update(confidence='TIME_SENSITIVE'),'CURRENTNESS_UNKNOWN')

    def test_missing_history(self):
        with self.assertRaisesRegex(GateError,'HISTORY_UNKNOWN'):collect(fixture(),dict(complete=False))

    def test_history_collision_gates(self):
        p=fixture()
        for field,value,error in [('article_id',p['article_id'],'ARTICLE_DUPLICATE'),('url',p['proposed_url'],'URL_COLLISION'),('topic_key',p['topic_key'],'TOPIC_DUPLICATE'),('search_intent',p['search_intent'],'INTENT_DUPLICATE')]:
            h=history();h['entries'].append({field:value})
            with self.subTest(field=field),self.assertRaisesRegex(GateError,error):collect(p,h)

    def test_schema_rules_and_approval(self):
        for k,v in [('schema_version','bad'),('rules',{}),('human_reviewed',True),('publish_approved',True),('synthetic',False),('version',4)]:
            p=fixture();p[k]=v
            with self.subTest(k=k),self.assertRaises(GateError):validate(p)

    def test_writer_cannot_add_claim(self):
        h,r,a=packets()
        with self.assertRaisesRegex(GateError,'BLOCKED_CLAIM'):write(r,h,[dict(claim_id='price',text='cheap')])

    def test_research_packet_changed(self):
        h,r,a=packets();r['facts'][0]['text']='changed'
        with self.assertRaisesRegex(GateError,'RESEARCH_PACKET_CHANGED'):write(r,h,a['sections'])

    def test_review_binds_hash(self):
        h,r,a=packets();a['body']+=' changed'
        with self.assertRaisesRegex(GateError,'CONTENT_HASH_DRIFT'):inspect(a,r,h)

    def test_rehashed_unbound_body(self):
        h,r,a=packets();a['body']='invented';a['content_hash']=digest({k:v for k,v in a.items() if k!='content_hash'})
        with self.assertRaisesRegex(GateError,'UNBOUND_BODY'):inspect(a,r,h)

    def test_review_no_writer_evaluation(self):
        h,r,a=packets();a['self_evaluation']='PASS'
        with self.assertRaisesRegex(GateError,'WRITER_EVALUATION'):inspect(a,r,h)

    def test_independent_identity(self):
        h,r,a=packets()
        with self.assertRaisesRegex(GateError,'REVIEWER_NOT_INDEPENDENT'):inspect(a,r,h,reviewer_id=a['writer_id'])

    def test_similarity_full_body(self):
        h,r,a=packets();v=inspect(a,r,h,[a['body']])
        self.assertEqual('REJECT',v['decision']);self.assertEqual(1,similarity(a['body'],a['body']))

    def test_delivery_blocks_stale_review_and_main(self):
        h,r,a=packets();v=inspect(a,r,h)
        with self.assertRaisesRegex(GateError,'ISOLATED_BASE'):draft_pr_request(a,v,'main','feature/work-cloud-pilot-x')
        v['content_hash']='wrong'
        with self.assertRaisesRegex(GateError,'STALE_REVIEW'):draft_pr_request(a,v,'integration/work-cloud-pilot-x','feature/work-cloud-pilot-x')

    def test_journal_missing_tampered_and_append_only(self):
        absent=LocalFileCAS(Path(self.temp.name)/'absent')
        with self.assertRaisesRegex(GateError,'STATE_UNKNOWN'):absent.read()
        reserve(self.store,'op',1,'gpt-6.1-terra',1000,100)
        old,token=self.store.read()
        changed=copy.deepcopy(old);changed['events'][0]['payload']['amount']=1
        with self.assertRaisesRegex(GateError,'JOURNAL_HASH'):replay(changed)
        with self.assertRaisesRegex(GateError,'HISTORY_REWRITE'):self.store.cas(token,empty())

    def test_cas_real_threads_only_one_wins(self):
        old,token=self.store.read()
        def race(i):
            new=append(old,str(i),dict(kind='transition',article_id='MOCK-'+str(i),version=1,status='RESEARCH_READY',artifact_hash=str(i)))
            try:self.store.cas(token,new);return True
            except GateError:return False
        with ThreadPoolExecutor(max_workers=2) as executor:result=list(executor.map(race,[1,2]))
        self.assertEqual(1,sum(result));self.assertEqual(1,len(self.store.read()[0]['events']))

    def test_global_cap_across_articles_reruns(self):
        for i in range(37):reserve(self.store,'op'+str(i),1,'gpt-6.1-terra',20000,6000)
        self.assertEqual(2_960_000_000,replay(self.store.read()[0])['allocated'])
        with self.assertRaisesRegex(GateError,'PROGRAM_CAP'):reserve(self.store,'other-article',1,'gpt-6.1-terra',20000,6000)

    def test_uncertain_failure_holds_and_blocks_program(self):
        rid=reserve(self.store,'op',1,'gpt-6.1-terra',1000,100)
        before=replay(self.store.read()[0])['allocated'];settle(self.store,rid,'uncertain')
        self.assertEqual(before,replay(self.store.read()[0])['allocated'])
        with self.assertRaisesRegex(GateError,'PROGRAM_USAGE_UNKNOWN'):reserve(self.store,'different-op',1,'gpt-6.1-terra',1000,100)

    def test_usage_unknown_does_not_release(self):
        rid=reserve(self.store,'op',1,'gpt-6.1-terra',1000,100)
        with self.assertRaisesRegex(GateError,'USAGE_UNKNOWN'):settle(self.store,rid,'success')
        self.assertEqual('reserved',replay(self.store.read()[0])['reservations'][rid]['status'])

    def test_reasoning_is_output_subset_not_double_counted(self):
        rid=reserve(self.store,'op',1,'gpt-6.1-terra',1000,100)
        u=dict(input_tokens=100,output_tokens=50,reasoning_tokens=30,cached_input_tokens=10,cache_write_tokens=0)
        settle(self.store,rid,'success',u)
        self.assertEqual(500000,replay(self.store.read()[0])['allocated'])

    def test_bounded_retries_and_unknown_price(self):
        u=dict(input_tokens=0,output_tokens=0,reasoning_tokens=0,cached_input_tokens=0,cache_write_tokens=0)
        for i in range(1,4):settle(self.store,reserve(self.store,'op',i,'gpt-6-luna',100,100),'known_failure',u)
        with self.assertRaisesRegex(GateError,'MAX_ATTEMPTS'):reserve(self.store,'op',4,'gpt-6-luna',100,100)
        with self.assertRaisesRegex(GateError,'UNKNOWN_PRICE'):reserve(self.store,'x',1,'Work UI Model',100,100)

    def test_idempotency_conflict(self):
        reserve(self.store,'op',1,'gpt-6-luna',100,100)
        with self.assertRaisesRegex(GateError,'IDEMPOTENCY_CONFLICT'):reserve(self.store,'op',1,'gpt-6-luna',101,100)

    def test_max_two_revisions(self):
        def step(status,version):transact(self.store,f'{status}:{version}',dict(kind='transition',article_id='MOCK-X',version=version,status=status,artifact_hash='hash'))
        for v in range(1,4):
            step('RESEARCH_READY',v);step('WRITTEN',v);step('REVISION_REQUIRED',v)
        with self.assertRaisesRegex(GateError,'MAX_TWO_REVISIONS'):step('RESEARCH_READY',4)

    def test_disabled_adapters_ignore_any_key(self):
        with patch.dict(os.environ,{'OPENAI_API_KEY':'synthetic-never-a-key'}):
            for call in [lambda:OpenAIResponsesDisabled().create(),lambda:SourceRetrievalDisabled().retrieve('https://example.com'),lambda:SearchProviderDisabled().search('cars')]:
                with self.assertRaises(GateError):call()

    def test_github_cas_transport_lease(self):
        class Fake:
            data=empty();sha='initial'
            def read(s,b,p):return copy.deepcopy(s.data),s.sha
            def replace(s,b,p,expected,data):
                if expected!=s.sha:raise GateError('CAS_CONFLICT')
                s.data=copy.deepcopy(data);s.sha=digest(data);return s.sha
        backend=Fake();store=GitHubCAS(backend);old,token=store.read()
        reserve(store,'x',1,'gpt-6-luna',100,100)
        with self.assertRaisesRegex(GateError,'CAS_CONFLICT'):store.cas(token,old)

    def test_original_files_preserved(self):self.assertEqual([],preserved())

    def test_separate_process_review(self):
        h,r,a=packets()
        # Review starts in a fresh interpreter with only explicit JSON file inputs.
        with tempfile.TemporaryDirectory(dir=ROOT/'cloud_pilot') as folder:
            p=Path(folder)
            for name,data in [('history',h),('research',r),('article',a)]:
                (p/(name+'.json')).write_text(json.dumps(data))
            subprocess.run([sys.executable,'-m','cloud_pilot.cli','review','--input',str(p/'article.json'),
                '--history',str(p/'history.json'),'--research',str(p/'research.json'),
                '--output',str(p/'review.json')],cwd=ROOT,check=True,capture_output=True)
            self.assertEqual(inspect(a,r,h),json.loads((p/'review.json').read_text()))

    def test_new_workflow_manual_read_only(self):
        text=(ROOT/'.github/workflows/cloud-pilot-mock.yml').read_text()
        self.assertIn('workflow_dispatch:',text)
        self.assertIn('contents: read',text)
        self.assertIn('persist-credentials: false',text)
        for forbidden in ('schedule:', 'pull_request:', 'pull_request_target:', 'push:', 'secrets.', 'contents: write'):
            self.assertNotIn(forbidden,text)

    def test_success_cannot_retry(self):
        rid=reserve(self.store,'op',1,'gpt-6-luna',100,100)
        settle(self.store,rid,'success',dict(input_tokens=1,output_tokens=1,reasoning_tokens=0,cached_input_tokens=0,cache_write_tokens=0))
        with self.assertRaisesRegex(GateError,'SUCCESS_NOT_RETRYABLE'):reserve(self.store,'op',2,'gpt-6-luna',100,100)

    def test_output_path_and_existing_artifact(self):
        from cloud_pilot.cli import save_new
        with self.assertRaisesRegex(GateError,'OUTPUT_OUTSIDE_PILOT'):save_new(ROOT/'batches/evil.json',{})
        with tempfile.TemporaryDirectory(dir=ROOT/'cloud_pilot') as folder:
            p=Path(folder)/'result.json';save_new(p,{'version':1});save_new(p,{'version':1})
            with self.assertRaisesRegex(GateError,'IMMUTABLE_ARTIFACT'):save_new(p,{'version':2})

if __name__=='__main__':unittest.main()

"""All responses, URLs, publishers and costs in this test module are synthetic."""
import base64
import copy
from datetime import datetime,timedelta,timezone
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from cloud_pilot.contract import ROOT,PROGRAM,BASELINE,digest,rules,GateError
from cloud_pilot.live.policy import (SCHEMA,RATES,CONTEXT,MAX_OUTPUT,BRANCH,STATE_PATH,reservation,
    validate_prices,usage_cost,check_permit)
from cloud_pilot.live.ledger import genesis,replay,append,Journal,GitHubStore
from cloud_pilot.live.http import JsonAPI,GitHubTransport,TransportFailure
from cloud_pilot.live.responses import Responses,build_request
from cloud_pilot.live.sources import retrieve,public_addresses,url_parts,MAX_BYTES,PinnedHTTPS
from cloud_pilot.live.stages import (validate_plan,check_research,check_writing,check_review,
    review_request,writing_request,REVIEW_CHECKS)
from cloud_pilot.live.engine import Engine


def prices():
    d=json.loads((ROOT/'cloud_pilot/runtime/prices-20261102.json').read_text())
    d['verified_at']=datetime.now(timezone.utc).isoformat()
    return d


def usage():
    return dict(input_tokens=2000,output_tokens=1000,input_tokens_details=dict(cached_tokens=200,cache_write_tokens=800),output_tokens_details=dict(reasoning_tokens=100))


class MemoryStore:
    def __init__(self):
        self.data=genesis('synthetic-mock-hash');self.lock=threading.Lock();self.fail_result=False
    def read(self):
        with self.lock:return copy.deepcopy(self.data),digest(self.data)
    def cas(self,expected,data):
        with self.lock:
            if expected!=digest(self.data):raise GateError('CAS_CONFLICT')
            if self.fail_result and data['events'][-1]['payload']['kind']=='result':raise GateError('STORAGE_FAILURE')
            replay(data);self.data=copy.deepcopy(data);return digest(data)


class ModelAPI:
    host='api.openai.com'
    def __init__(self):self.calls=[];self.counter=0;self.fail=False;self.status='completed';self.usage=usage()
    def request(self,method,path,payload):
        self.calls.append((method,path,payload))
        if self.fail:raise TimeoutError('synthetic secret must not appear in exception')
        self.counter+=1
        return 200,dict(id='resp-fake-'+str(self.counter),model=payload['model'],status=self.status,
            usage=copy.deepcopy(self.usage),output=[dict(type='message',content=[dict(type='output_text',text='{"ok":true}')])])


def history():return dict(entries=[],documents=[])


def plan():
    articles=[]
    for name in ('ALPHA','BETA'):
        scope=dict(market='SYNTHETIC-'+name,model_year='2026',generation='TEST',trim='TEST',powertrain='TEST',test_cycle='N/A')
        sources=[dict(source_id='S'+str(i),url='https://test-org'+str(i%4)+'.invalid/'+name+'/'+str(i),
                      publisher='Synthetic '+str(i%4),parent_org='Synthetic '+str(i%4),tier='T1',scope=scope) for i in range(6)]
        articles.append(dict(article_id='PILOT-'+name,locale='en',version=1,topic_key='synthetic-'+name,
            search_intent='A synthetic decision about '+name,buyer_task='synthetic task',proposed_url='/pilot-only/'+name.lower()+'/',sources=sources))
    return dict(schema=SCHEMA,program_id=PROGRAM,baseline_sha=BASELINE,rules=rules(),history_hash=digest(history()),
        semantic_dedup_status='INDEPENDENTLY_CONFIRMED',articles=articles,authorized_redirect_urls=[])


def evidence(topic):
    out=[]
    for s in topic['sources']:
        text='Synthetic source statement for '+topic['article_id']+' '+s['source_id']+'. This is only test evidence.'
        out.append(dict(source_id=s['source_id'],text=text,scope=s['scope'],tier=s['tier'],parent_org=s['parent_org'],
            raw_sha256=hashlib.sha256(text.encode()).hexdigest(),retrieved_at=datetime.now(timezone.utc).isoformat()))
    return out


def research_result(topic,items):
    facts=[dict(id='F'+str(i),statement=e['text'],confidence='VERIFIED',scope=e['scope'],source_ids=[e['source_id']],quotes=[dict(source_id=e['source_id'],quote=e['text'])]) for i,e in enumerate(items)]
    return dict(response_id='research-test',content=dict(status='RESEARCH_PASS',writing_ai_ready=True,
        source_checks=[dict(source_id=e['source_id'],publisher_match=True,scope_match=True) for e in items],facts=facts,
        allowed_facts=[f['id'] for f in facts],blocked_facts=['UNSUPPORTED'],human_reviewed=False,publish_approved=False))


def writer_result(research):
    # 950 unique fake tokens: exercises full-body checks, not a real researched article.
    marker=research['article_id'].lower().replace('-','')
    text=' '.join(marker+'word'+chr(97+i%26)+chr(97+(i//26)%26)+chr(97+(i//676)%26) for i in range(950))
    return dict(response_id='writer-test',content=dict(title='Synthetic training title',meta='Synthetic metadata',h1='Synthetic heading',summary='Synthetic summary',
        sections=[dict(text=text,claim_ids=['F0'])],faq=[],internal_links=[],human_reviewed=False,publish_approved=False))


def reviewer_result(article,research,decision='REVIEW_PASS'):
    return dict(response_id='review-test',content=dict(content_hash=article['content_hash'],evidence_hash=research['evidence_hash'],
        decision=decision,checks={k:True for k in REVIEW_CHECKS},findings=[] if decision=='REVIEW_PASS' else [dict(rule_id='TEST',detail='synthetic revision',claim_id='F0')],human_reviewed=False,publish_approved=False))


def packets():
    t=plan()['articles'][0];e=evidence(t)
    r=check_research(research_result(t,e),t,e)
    a=check_writing(writer_result(r),r,1,history(),[])
    return t,e,r,a


class LiveTests(unittest.TestCase):
    def setUp(self):
        self.network=patch.object(socket.socket,'connect',side_effect=AssertionError('NO_NETWORK_IN_STAGE2_TESTS'))
        self.network.start();self.addCleanup(self.network.stop)
        self.store=MemoryStore();self.journal=Journal(self.store);self.api=ModelAPI()
        self.client=Responses(self.api,self.journal,prices(),lambda:None)

    def test_responses_real_payload_and_durable_replay(self):
        self.assertEqual({'ok':True},self.client.call('article-writing','writing',{'source':'synthetic'})['content'])
        before=digest(self.store.data)
        self.client.call('article-writing','writing',{'source':'synthetic'})
        self.assertEqual(1,len(self.api.calls));self.assertEqual(before,digest(self.store.data))
        request=self.api.calls[0][2]
        self.assertFalse(request['store']);self.assertEqual([],request['tools'])
        self.assertEqual({'mode':'implicit','ttl':'30m'},request['prompt_cache_options'])
        self.assertEqual('medium',request['reasoning']['effort']);self.assertEqual(8000,request['max_output_tokens'])
        self.assertIn('LESSONS_LEARNED.md',request['input'][0]['content'])
        self.assertEqual(3,len(self.store.data['events']))

    def test_every_real_stage_separate_stateless_request(self):
        for stage in ('research','writing','review'):self.client.call(stage,stage,{'data':'fake'})
        self.assertEqual(3,len(self.api.calls))
        self.assertNotIn('previous_response_id',self.api.calls[2][2])
        self.assertEqual('high',self.api.calls[2][2]['reasoning']['effort'])
        self.assertNotIn('self_evaluation',self.api.calls[2][2]['input'][1]['content'])

    def test_request_drift_not_retried(self):
        self.client.call('op','writing',{'a':1})
        with self.assertRaisesRegex(GateError,'OPERATION_INPUT_DRIFT'):self.client.call('op','writing',{'a':2})
        self.assertEqual(1,len(self.api.calls))

    def test_no_call_when_permission_fails(self):
        def denied():raise GateError('LIVE_NOT_AUTHORIZED')
        c=Responses(self.api,self.journal,prices(),denied)
        with self.assertRaisesRegex(GateError,'LIVE_NOT_AUTHORIZED'):c.call('op','writing',{})
        self.assertFalse(self.api.calls);self.assertFalse(self.store.data['events'])

    def test_no_call_when_reservation_cas_fails(self):
        self.store.cas=lambda *args:(_ for _ in ()).throw(GateError('CAS_CONFLICT'))
        with self.assertRaisesRegex(GateError,'CAS_CONFLICT'):self.client.call('op','writing',{})
        self.assertFalse(self.api.calls)

    def test_timeout_holds_full_amount_and_stops_program(self):
        self.api.fail=True
        with self.assertRaisesRegex(TransportFailure,'STOP_PROGRAM'):self.client.call('op','writing',{})
        v=replay(self.store.data);self.assertEqual(reservation('gpt-6.1-terra'),v['allocated'])
        with self.assertRaisesRegex(GateError,'UNRESOLVED_PROGRAM_CALL'):self.client.call('other','research',{})
        with self.assertRaisesRegex(GateError,'NO_RESEND'):self.client.call('op','writing',{})
        self.assertEqual(1,len(self.api.calls))

    def test_unknown_usage_is_not_free(self):
        self.api.usage={}
        with self.assertRaises(TransportFailure):self.client.call('op','writing',{})
        self.assertEqual('uncertain',next(iter(replay(self.store.data)['operations'].values()))['status'])

    def test_result_storage_failure_stops_without_duplicate(self):
        self.store.fail_result=True
        with self.assertRaises(TransportFailure):self.client.call('op','writing',{})
        self.store.fail_result=False
        with self.assertRaisesRegex(GateError,'NO_RESEND'):self.client.call('op','writing',{})
        self.assertEqual(1,len(self.api.calls))

    def test_incomplete_is_accounted_and_not_automatically_retried(self):
        self.api.status='incomplete'
        for _ in range(2):
            with self.assertRaisesRegex(GateError,'INCOMPLETE'):self.client.call('op','writing',{})
        self.assertEqual(1,len(self.api.calls))
        self.assertLess(replay(self.store.data)['allocated'],reservation('gpt-6.1-terra'))

    def test_concurrent_call_only_one_transmission(self):
        barrier=threading.Barrier(2)
        original=self.store.read
        count=0;lock=threading.Lock()
        def synced_read():
            nonlocal count
            result=original()
            with lock:count+=1;n=count
            if n<=2:barrier.wait(timeout=3)
            return result
        self.store.read=synced_read
        def run(i):
            try:self.client.call('same','writing',{});return True
            except (GateError,TransportFailure):return False
        with ThreadPoolExecutor(max_workers=2) as ex:results=list(ex.map(run,[1,2]))
        self.assertEqual(1,len(self.api.calls));self.assertEqual(1,sum(results))

    def test_cap_across_articles_and_reruns(self):
        # Six synthetic settled requests across all responsibilities share one ledger.
        for i in range(6):self.client.call('article-'+str(i),'writing',{})
        self.assertEqual(6,len(self.api.calls))
        self.assertLessEqual(replay(self.store.data)['allocated'],3_000_000_000)
        for i in range(100):
            try:self.client.call('extra-'+str(i),'writing',{})
            except GateError as e:
                self.assertIn('PROGRAM_CAP_EXCEEDED',str(e));break
        else:self.fail('cap not enforced')
        self.assertLessEqual(replay(self.store.data)['allocated'],3_000_000_000)

    def test_full_context_conservative_reservation(self):
        self.assertEqual(2_685_000_000,reservation('gpt-6.1-terra'))
        self.assertEqual(268_500_000,reservation('gpt-6-luna'))
        self.assertEqual(7_010_000,usage_cost('gpt-6.1-terra',usage()))

    def test_reasoning_not_double_billed_and_cache_write_not_double_added(self):
        u=usage();u['output_tokens_details']['reasoning_tokens']=900
        self.assertEqual(usage_cost('gpt-6.1-terra',usage()),usage_cost('gpt-6.1-terra',u))
        u['input_tokens_details']['cache_write_tokens']=3000
        with self.assertRaisesRegex(GateError,'CACHE_USAGE'):usage_cost('gpt-6.1-terra',u)

    def test_price_expiry_or_drift_blocks_before_call(self):
        p=prices();p['verified_at']=(datetime.now(timezone.utc)-timedelta(days=2)).isoformat()
        with self.assertRaisesRegex(GateError,'EXPIRED'):Responses(self.api,self.journal,p,lambda:None).call('op','writing',{})
        self.assertFalse(self.api.calls)
        p=prices();p['rates']['unknown']={}
        with self.assertRaisesRegex(GateError,'PRICING'):validate_prices(p)

    def test_ledger_tamper_history_and_unknown_state(self):
        self.client.call('op','writing',{})
        bad=copy.deepcopy(self.store.data);bad['events'][0]['payload']['amount']=1
        with self.assertRaisesRegex(GateError,'LEDGER_TAMPER'):replay(bad)
        bad=copy.deepcopy(self.store.data);bad['cap_nano_usd']=4_000_000_000
        with self.assertRaisesRegex(GateError,'CAP_OR_SEED'):replay(bad)

    def test_crash_reserved_no_blind_resend_or_auto_release(self):
        p=dict(kind='reserve',id='r',operation='op',attempt=1,owner='a',request_hash='hash',price_hash='hash',model='gpt-6.1-terra',amount=reservation('gpt-6.1-terra'))
        self.journal.commit('reserve:r',p)
        with self.assertRaisesRegex(GateError,'UNRESOLVED_PROGRAM_CALL'):self.client.call('other','writing',{})
        with self.assertRaisesRegex(GateError,'EVIDENCE_REQUIRED'):self.journal.commit('reconcile:r',dict(kind='reconcile',id='r'))

    def test_max_three_proven_not_sent_attempts(self):
        for i in range(1,4):
            rid='r'+str(i)
            self.journal.commit('reserve:'+rid,dict(kind='reserve',id=rid,operation='op',attempt=i,owner='a',request_hash='h',price_hash='p',model='gpt-6-luna',amount=reservation('gpt-6-luna')))
            self.journal.commit('reconcile:'+rid,dict(kind='reconcile',id=rid,request_proven_not_sent=True,operator_approval_hash='a',provider_evidence_hash='e'))
        with self.assertRaisesRegex(GateError,'MAX_THREE'):self.journal.commit('reserve:r4',dict(kind='reserve',id='r4',operation='op',attempt=4,request_hash='h',price_hash='p',model='gpt-6-luna',amount=reservation('gpt-6-luna')))

    def test_immutable_checkpoint(self):
        self.journal.checkpoint('a',{'v':1});self.journal.checkpoint('a',{'v':1})
        with self.assertRaisesRegex(GateError,'IDEMPOTENCY'):self.journal.checkpoint('a',{'v':2})

    def test_default_cli_no_credentials_or_network(self):
        from cloud_pilot.live.__main__ import preflight
        with patch('cloud_pilot.live.__main__.os.environ',side_effect=AssertionError('NO_CREDENTIAL_ACCESS')):
            result=preflight()
        self.assertEqual(0,result['real_api_calls']);self.assertFalse(result['credentials_read'])
        p=subprocess.run([sys.executable,'-m','cloud_pilot.live','execute'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(2,p.returncode);self.assertIn('LIVE_PERMIT_REQUIRED',p.stdout)

    def test_disabled_permit_cannot_read_any_credentials(self):
        from cloud_pilot.live.__main__ import execute
        with self.assertRaisesRegex(GateError,'LIVE_NOT_AUTHORIZED'):
            check_permit({'authorized':False},plan(),prices(),'a'*40,'')

    def test_valid_permit_is_bound_to_code_plan_prices_and_expiry(self):
        p,price=plan(),prices();sha='a'*40
        permit=dict(authorized=True,program_id=PROGRAM,cap_nano_usd=3_000_000_000,plan_hash=digest(p),prices_hash=digest(price),code_sha=sha,
                    baseline_sha=BASELINE,rules=rules(),expires_at=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat(),
                    allowed_models=list(RATES),account_models_verified=True,protected_runtime_verified=True)
        self.assertTrue(check_permit(permit,p,price,sha,digest(permit)))
        with self.assertRaisesRegex(GateError,'CODE_DRIFT'):check_permit(permit,p,price,'b'*40,digest(permit))
        with self.assertRaisesRegex(GateError,'PROTECTED_APPROVAL'):check_permit(permit,p,price,sha,'wrong')

    def test_github_actual_contents_payload_uses_blob_sha_and_fixed_branch(self):
        class API:
            host='api.github.com'
            calls=[]
            def request(s,method,path,payload=None):
                s.calls.append((method,path,payload))
                return 200,{'content':{'sha':'next'}}
        api=API();t=GitHubTransport(api)
        self.assertEqual('next',t.replace(BRANCH,STATE_PATH,'expected',genesis('fake')))
        self.assertEqual('expected',api.calls[0][2]['sha']);self.assertEqual(BRANCH,api.calls[0][2]['branch'])
        with self.assertRaisesRegex(GateError,'FIXED_PROGRAM'):t.replace('main',STATE_PATH,'sha',{})

    def test_github_state_missing_fails_closed(self):
        class API:
            host='api.github.com'
            def request(s,*a):return 404,{}
        with self.assertRaisesRegex(GateError,'MISSING'):GitHubStore(GitHubTransport(API())).read()

    def test_github_store_cas_and_append_only(self):
        class T:
            def __init__(s):s.data=genesis('fake');s.sha='v1';s.artifacts={}
            def read(s,b,p):return copy.deepcopy(s.data),s.sha
            def replace(s,b,p,sha,data):
                if sha!=s.sha:raise GateError('CAS_CONFLICT')
                s.data=copy.deepcopy(data);s.sha=digest(data);return s.sha
            def put_immutable(s,branch,path,body):
                s.artifacts[path]=body;return hashlib.sha256(body).hexdigest()
            def read_artifact(s,branch,path):
                body=s.artifacts[path];return json.loads(body),hashlib.sha256(body).hexdigest()
        store=GitHubStore(T());j=Journal(store);j.checkpoint('test',{'v':1})
        self.assertEqual({'v':1},j.get_checkpoint('test'))
        with self.assertRaisesRegex(GateError,'CAS_CONFLICT'):store.cas('v1',genesis('fake'))
        _,token=store.read()
        with self.assertRaisesRegex(GateError,'HISTORY_REWRITE'):store.cas(token,genesis('fake'))

    def test_no_writer_evaluation_and_independent_review_identity(self):
        t,e,r,a=packets();request=review_request(a,r)
        self.assertNotIn('self_evaluation',json.dumps(request))
        result=reviewer_result(a,r);result['response_id']='writer-test'
        with self.assertRaisesRegex(GateError,'IDENTITY_REUSE'):check_review(result,a,r)

    def test_quote_and_scope_bindings(self):
        t,e,r,a=packets();result=research_result(t,e)
        result['content']['facts'][0]['quotes'][0]['quote']='invented evidence quotation'
        with self.assertRaisesRegex(GateError,'QUOTE_NOT_IN'):check_research(result,t,e)
        result=research_result(t,e);result['content']['facts'][0]['scope']=dict(e[0]['scope'],market='WRONG')
        with self.assertRaisesRegex(GateError,'SCOPE_DRIFT'):check_research(result,t,e)

    def test_source_identity_and_research_failure(self):
        t,e,r,a=packets();result=research_result(t,e);result['content']['source_checks'][0]['publisher_match']=False
        with self.assertRaisesRegex(GateError,'IDENTITY_OR_SCOPE'):check_research(result,t,e)
        result=research_result(t,e);result['content']['status']='RESEARCH_FAIL'
        with self.assertRaisesRegex(GateError,'STOPS_WRITING'):check_research(result,t,e)

    def test_writer_blocks_unknown_claim_and_public_leak(self):
        t,e,r,a=packets();result=writer_result(r);result['content']['sections'][0]['claim_ids']=['UNSUPPORTED']
        with self.assertRaisesRegex(GateError,'BLOCKED'):check_writing(result,r,1,history(),[])
        result=writer_result(r);result['content']['sections'][0]['text']+=' Research AI'
        with self.assertRaisesRegex(GateError,'WORKFLOW_LEAKAGE'):check_writing(result,r,1,history(),[])
        result=writer_result(r);result['content']['self_evaluation']='pass'
        with self.assertRaisesRegex(GateError,'SELF_EVALUATION'):check_writing(result,r,1,history(),[])

    def test_reviewer_hash_and_false_pass(self):
        t,e,r,a=packets();res=reviewer_result(a,r);res['content']['content_hash']='other'
        with self.assertRaisesRegex(GateError,'HASH_DRIFT'):check_review(res,a,r)
        res=reviewer_result(a,r);res['content']['checks']['currentness']=False
        with self.assertRaisesRegex(GateError,'CONTRADICTORY_PASS'):check_review(res,a,r)
        res=reviewer_result(a,r);res['content']['human_reviewed']=True
        with self.assertRaisesRegex(GateError,'APPROVAL_FORBIDDEN'):check_review(res,a,r)

    def test_plan_intent_url_and_scope_gates(self):
        self.assertTrue(validate_plan(plan(),history()))
        p=plan();p['semantic_dedup_status']='PENDING'
        with self.assertRaisesRegex(GateError,'SEMANTIC_DEDUP'):validate_plan(p,history())
        p=plan();p['articles'][1]['search_intent']=p['articles'][0]['search_intent']
        with self.assertRaisesRegex(GateError,'DUPLICATE'):validate_plan(p,history())
        p=plan();p['articles'][0]['proposed_url']='/vehicles/new/'
        with self.assertRaisesRegex(GateError,'PRODUCTION_URL'):validate_plan(p,history())

    def test_ssrf_nonpublic_dns_and_mixed_answers(self):
        for addr in ('127.0.0.1','10.0.0.1','169.254.169.254','::1','::ffff:127.0.0.1','192.0.2.1'):
            with self.subTest(addr=addr),self.assertRaisesRegex(GateError,'NON_PUBLIC'):
                public_addresses('source.test',lambda *a,**k:[(0,0,0,'',(addr,443))])
        with self.assertRaisesRegex(GateError,'NON_PUBLIC'):public_addresses('source.test',lambda *a,**k:[(0,0,0,'',('8.8.8.8',443)),(0,0,0,'',('127.0.0.1',443))])

    def test_url_authorization_credentials_and_https(self):
        for url in ('http://public.test/','https://user:pass@public.test/','https://public.test:444/','https://public.test/#secret'):
            with self.subTest(url=url),self.assertRaises(GateError):url_parts(url,{url})
        with self.assertRaisesRegex(GateError,'NOT_AUTHORIZED'):url_parts('https://public.test/',set())

    def source_response(self,status=200,headers=None,body=b'<html><p>Real retrieval implementation, synthetic test body.</p><script>SECRET INSTRUCTION</script></html>'):
        class R:
            def __init__(s):s.status=status
            def getheader(s,k,default=None):return (headers or {'Content-Type':'text/html'}).get(k,default)
            def read(s,n):return body[:n]
        return R()

    def retrieve_fake(self,response,allowed=None,addresses=None):
        source=plan()['articles'][0]['sources'][0]
        class C:
            def __init__(s,*a):pass
            def request(s,*a,**k):pass
            def getresponse(s):return response
            def close(s):pass
        resolver=lambda *a,**k:[(0,0,0,'',(addresses or '8.8.8.8',443))]
        return retrieve(source,allowed or {source['url']},resolver,C)

    def test_retrieval_saves_provenance_strips_scripts(self):
        e,raw=self.retrieve_fake(self.source_response())
        self.assertNotIn('SECRET INSTRUCTION',e['text']);self.assertEqual(hashlib.sha256(raw).hexdigest(),e['raw_sha256'])
        self.assertEqual('8.8.8.8',e['connected_ip']);self.assertFalse(e['synthetic'])

    def test_retrieval_redirect_to_unauthorized_or_private(self):
        with self.assertRaisesRegex(GateError,'NOT_AUTHORIZED'):self.retrieve_fake(self.source_response(302,{'Location':'https://unapproved.invalid/'}))
        with self.assertRaisesRegex(GateError,'NON_PUBLIC'):self.retrieve_fake(self.source_response(),addresses='127.0.0.1')

    def test_retrieval_status_mime_size_encoding(self):
        for response,error in [(self.source_response(403),'ACCESS_LIMITATION'),(self.source_response(headers={'Content-Type':'application/pdf'}),'MIME_NOT_ENABLED'),
            (self.source_response(headers={'Content-Type':'text/plain','Content-Length':str(MAX_BYTES+1)}),'TOO_LARGE'),
            (self.source_response(headers={'Content-Type':'text/plain'},body=b'x'*(MAX_BYTES+1)),'TOO_LARGE'),
            (self.source_response(headers={'Content-Type':'text/plain'},body=b'\xff\xfe'),'NOT_UTF8'),
            (self.source_response(headers={'Content-Type':'text/plain','Content-Encoding':'gzip'}),'COMPRESSED')]:
            with self.subTest(error=error),self.assertRaisesRegex(GateError,error):self.retrieve_fake(response)

    def test_api_errors_do_not_echo_tokens_or_follow_redirect(self):
        class Connection:
            calls=[]
            def __init__(s,*a,**kw):pass
            def request(s,*a,**kw):raise OSError('Bearer synthetic-secret')
            def close(s):pass
        with self.assertRaises(TransportFailure) as cm:JsonAPI('api.openai.com','synthetic-secret',Connection).request('POST','/v1/responses',{})
        self.assertNotIn('synthetic-secret',str(cm.exception))
        with self.assertRaisesRegex(GateError,'FIXED_API_ORIGIN'):JsonAPI('evil.invalid','synthetic-secret',Connection)

    def test_end_to_end_two_articles_and_recovery(self):
        class Models:
            def __init__(s):s.calls=[]
            def call(s,op,stage,data):
                s.calls.append(stage)
                if stage=='research':return research_result(data['topic'],data['evidence'])
                if stage=='writing':return writer_result(data['research'])
                return reviewer_result(data['article'],data['research'])
        class GitHub:
            def __init__(s):s.deliveries=[]
            def put_immutable(s,*a):return 'synthetic-blob'
            def deliver_candidate(s,p):
                d=dict(url='https://github.com/synthetic/mock/pull/1',draft=True,content_hash=p['article']['content_hash'])
                s.deliveries.append(d);return d
        models,github=Models(),GitHub()
        def fetch(source,allowed):
            e=next(e for t in plan()['articles'] for e in evidence(t) if source['source_id']==e['source_id'] and source['scope']==e['scope'])
            return e,e['text'].encode()
        engine=Engine(plan(),history(),self.journal,models,github,fetch)
        first=engine.run();second=engine.run()
        self.assertEqual(first,second);self.assertEqual(['research','writing','review']*2,models.calls)
        self.assertEqual(4,len(github.deliveries)) # Two deliveries are revalidated on recovery; model calls are unchanged.

    def test_source_failure_stops_all_models(self):
        class Models:
            def call(s,*a):raise AssertionError('MODEL_MUST_NOT_RUN')
        def fail(*a):raise GateError('SOURCE_ACCESS_LIMITATION')
        with self.assertRaisesRegex(GateError,'SOURCE_ACCESS'):Engine(plan(),history(),self.journal,Models(),object(),fail).run()

    def test_authorized_manual_bootstrap_and_other_workflows_unchanged(self):
        self.assertFalse((ROOT/'.github/workflows/cloud-pilot-api.yml').exists())
        result=subprocess.check_output(['git','diff','75d010eae1300532f6008988d01d65cdae3d1c86','--','.github/workflows',
            ':(exclude).github/workflows/cloud-pilot-manual.yml',':(exclude).github/workflows/cloud-pilot-trusted.yml'],cwd=ROOT,text=True)
        self.assertEqual('',result)
        self.assertEqual((ROOT/'cloud_pilot/runtime/multilingual-manual.yml.template').read_text(),
                         (ROOT/'.github/workflows/cloud-pilot-manual.yml').read_text())

    def test_two_revisions_exhaustion_is_durable(self):
        class Models:
            calls=[]
            def call(s,op,stage,data):
                s.calls.append(stage)
                if stage=='research':return research_result(data['topic'],data['evidence'])
                if stage=='writing':return writer_result(data['research'])
                return reviewer_result(data['article'],data['research'],'REVISION_REQUIRED')
        class GitHub:
            def put_immutable(s,*a):return 'synthetic-blob'
            def deliver_candidate(s,p):raise AssertionError('NO_DELIVERY')
        def fetch(source,allowed):
            e=next(e for t in plan()['articles'] for e in evidence(t) if source['source_id']==e['source_id'] and source['scope']==e['scope'])
            return e,e['text'].encode()
        models=Models();engine=Engine(plan(),history(),self.journal,models,GitHub(),fetch)
        with self.assertRaisesRegex(GateError,'MAX_TWO_REVISIONS'):engine.run()
        self.assertEqual(3,models.calls.count('writing'));self.assertEqual(3,models.calls.count('review'))
        self.assertEqual('MAX_TWO_REVISIONS_EXHAUSTED',replay(self.store.data)['halts'][-1]['reason'])
        before=len(models.calls)
        with self.assertRaisesRegex(GateError,'MAX_TWO_REVISIONS'):engine.run()
        self.assertEqual(before,len(models.calls))

    def test_delivery_failure_reuses_review_without_model_rerun(self):
        class Models:
            def __init__(s):s.calls=[]
            def call(s,op,stage,data):
                s.calls.append(stage)
                if stage=='research':return research_result(data['topic'],data['evidence'])
                if stage=='writing':return writer_result(data['research'])
                return reviewer_result(data['article'],data['research'])
        class GitHub:
            fail=True
            def put_immutable(s,*a):return 'synthetic-blob'
            def deliver_candidate(s,p):
                if s.fail:raise GateError('SYNTHETIC_DELIVERY_FAILURE')
                return dict(url='https://github.com/synthetic/pilot/pull/1',draft=True)
        def fetch(source,allowed):
            e=next(e for t in plan()['articles'] for e in evidence(t) if source['source_id']==e['source_id'] and source['scope']==e['scope'])
            return e,e['text'].encode()
        models,gh=Models(),GitHub();engine=Engine(plan(),history(),self.journal,models,gh,fetch)
        with self.assertRaisesRegex(GateError,'DELIVERY_FAILURE'):engine.run()
        self.assertEqual(['research','writing','review'],models.calls)
        gh.fail=False;self.assertEqual(2,len(engine.run()))
        self.assertEqual(['research','writing','review']*2,models.calls)

    def test_http_api_redirect_does_not_follow(self):
        class Response:
            status=302
            def read(s,n):return b'{}'
        class Connection:
            calls=[]
            def __init__(s,*a,**kw):pass
            def request(s,*a,**kw):s.calls.append(a)
            def getresponse(s):return Response()
            def close(s):pass
        self.assertEqual((302,{}),JsonAPI('api.openai.com','synthetic-secret',Connection).request('POST','/v1/responses',{}))
        self.assertEqual(1,len(Connection.calls))

    def test_pinned_connection_uses_validated_ip_and_hostname_for_tls(self):
        class Sock:
            def getpeername(s):return ('8.8.8.8',443)
            def close(s):pass
        class Context:
            calls=[]
            def wrap_socket(s,sock,server_hostname):s.calls.append(server_hostname);return sock
        conn=PinnedHTTPS('source.test','8.8.8.8');context=Context();conn._context=context
        with patch('cloud_pilot.live.sources.socket.create_connection',return_value=Sock()) as create:
            conn.connect()
        create.assert_called_once_with(('8.8.8.8',443),timeout=10)
        self.assertEqual(['source.test'],context.calls)

    def test_unsupported_numbers_and_standard_fields_fail(self):
        t,e,r,a=packets();w=writer_result(r);w['content']['sections'][0]['text']+=' Guaranteed range 9999 km.'
        with self.assertRaisesRegex(GateError,'UNSUPPORTED_NUMERIC'):check_writing(w,r,1,history(),[])
        response=research_result(t,e);response['content']['facts'][0]['kind']='standard'
        with self.assertRaisesRegex(GateError,'STANDARD_FIELDS'):check_research(response,t,e)

    def test_engine_with_responses_adapter_and_mock_http_all_six_calls(self):
        class API:
            host='api.openai.com'
            calls=[]
            def request(s,method,path,payload):
                data=json.loads(payload['input'][1]['content']);s.calls.append(data['stage'])
                if data['stage']=='research':result=research_result(data['topic'],data['evidence'])
                elif data['stage']=='writing':result=writer_result(data['research'])
                else:result=reviewer_result(data['article'],data['research'])
                return 200,dict(id=result['response_id'],model=payload['model'],status='completed',usage=usage(),
                    output=[dict(type='message',content=[dict(type='output_text',text=json.dumps(result['content']))])])
        class GitHub:
            def put_immutable(s,*a):return 'synthetic-blob'
            def deliver_candidate(s,p):return dict(url='https://github.com/synthetic/pilot/pull/1',draft=True)
        def fetch(source,allowed):
            e=next(e for t in plan()['articles'] for e in evidence(t) if source['source_id']==e['source_id'] and source['scope']==e['scope'])
            return e,e['text'].encode()
        api=API();models=Responses(api,self.journal,prices(),lambda:None)
        engine=Engine(plan(),history(),self.journal,models,GitHub(),fetch)
        self.assertEqual(2,len(engine.run()));self.assertEqual(2,len(engine.run()))
        self.assertEqual(['research','writing','independent_review']*2,api.calls)
        view=replay(self.store.data)
        self.assertEqual(6,len(view['operations']));self.assertEqual(29_444_000,view['allocated'])

    def test_execute_with_existing_keys_stops_before_secret_reads(self):
        from cloud_pilot.live.__main__ import execute
        class Environment(dict):
            def get(s,key,default=None):
                if key in ('OPENAI_API_KEY','AUTOBRIDGE_GITHUB_TOKEN'):raise AssertionError('SECRET_READ_TOO_EARLY')
                return super().get(key,default)
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)
            input_plan=plan()
            input_plan['history_hash']=digest(json.loads((ROOT/'cloud_pilot/evidence/history-snapshot.json').read_text()))
            for name,data in [('plan',input_plan),('prices',prices()),('permit',{'authorized':False})]:
                (p/(name+'.json')).write_text(json.dumps(data))
            with patch('cloud_pilot.live.__main__.os.environ',Environment(PATH='/usr/bin:/bin')):
                with self.assertRaisesRegex(GateError,'LIVE_NOT_AUTHORIZED'):
                    execute(p/'plan.json',p/'prices.json',p/'permit.json')

    def test_committed_result_lost_ack_is_recovered_without_resend(self):
        original=self.store.cas
        def lost_ack(expected,data):
            result=original(expected,data)
            if data['events'][-1]['payload']['kind']=='result':raise TimeoutError('lost synthetic ACK')
            return result
        self.store.cas=lost_ack
        with self.assertRaises(TransportFailure):self.client.call('op','writing',{})
        self.assertEqual({'ok':True},self.client.call('op','writing',{})['content'])
        self.assertEqual(1,len(self.api.calls))


if __name__=='__main__':unittest.main()

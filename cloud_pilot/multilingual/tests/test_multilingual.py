"""Network-blocked synthetic tests. Passing is not real API or language acceptance."""
import copy
import json
import re
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from cloud_pilot.contract import GateError,digest,ROOT
from cloud_pilot.live.ledger import Journal,replay
from cloud_pilot.live.responses import Responses
from cloud_pilot.live.engine import Engine
from cloud_pilot.stage2_tests.test_live import (MemoryStore,plan,history,evidence,
    research_result,writer_result,reviewer_result,prices,usage,packets)
from cloud_pilot.multilingual.localize import (LOCALES,CHECKS,validate,validate_review,
    Localizer,run_multilingual,markdown)
from cloud_pilot.multilingual.__main__ import plan_check,execute,preflight
from cloud_pilot.multilingual.sources import decode,retrieve
from cloud_pilot.multilingual.accounting import ResponseJournal,DurableResponses

class ArtifactStore(MemoryStore):
    def __init__(self):super().__init__();self.artifacts={}
    def save_artifact(self,a):
        h=digest(a);self.artifacts[h]=copy.deepcopy(a)
        return dict(_immutable_artifact_ref=True,content_hash=h)
    def load_artifact(self,ref):
        a=self.artifacts[ref['content_hash']]
        if digest(a)!=ref['content_hash']:raise GateError('IMMUTABLE_ARTIFACT_DRIFT')
        return copy.deepcopy(a)

def translation(base,locale):
    p=copy.deepcopy(base['public'])
    marker={'ja':'購入条件の確認','ko':'구매 조건 확인','zh':'采购条件核验',
            'ar':'مراجعة شروط الشراء','th':'ตรวจสอบเงื่อนไขการซื้อ'}.get(locale,'Localized '+locale)
    for k in ('title','meta','h1','summary'):p[k]=marker+' '+p[k]
    for s in p['sections']:s['text']=marker*400+' '+s['text']
    for f in p['faq']:
        f['question']=marker+' '+f['question'];f['answer']=marker+' '+f['answer']
    return dict(response_id='synthetic-translator',content=p)

def locale_review(a,b,decision='REVIEW_PASS'):
    return dict(response_id='synthetic-independent-reviewer',content=dict(
        content_hash=a['content_hash'],base_content_hash=b['content_hash'],decision=decision,
        checks={k:True for k in CHECKS},findings=[] if decision=='REVIEW_PASS' else ['synthetic finding'],
        human_reviewed=False,publish_approved=False))

class API:
    host='api.openai.com'
    def __init__(self):
        self.calls=[];self.reported_usage=usage();self.reported_usage['output_tokens']=500
    def request(self,method,path,payload):
        d=json.loads(payload['input'][1]['content']);self.calls.append(d['stage'])
        if d['stage']=='research':r=research_result(d['topic'],d['evidence'])
        elif d['stage']=='writing':
            r=writer_result(d['research']);r['content']['faq']=[dict(question='Synthetic question '+c,
                answer='Synthetic answer '+c,claim_ids=['F0']) for c in 'ABC']
        elif d['stage']=='independent_review':r=reviewer_result(d['article'],d['research'])
        elif d['stage']=='localization':r=translation(d['english_article'],d['locale'])
        else:r=locale_review(d['article'],d['english_article'])
        return 200,dict(id='resp-synthetic-'+str(len(self.calls)),model=payload['model'],
            status='completed',usage=copy.deepcopy(self.reported_usage),output=[dict(type='message',content=[dict(
                type='output_text',text=json.dumps(r['content']))])])

class GitHub:
    def __init__(self):self.artifacts={};self.fail_export=False
    def put_immutable(self,branch,path,body):
        if self.fail_export and path.endswith('.md'):raise GateError('SYNTHETIC_EXPORT_FAILURE')
        if path in self.artifacts:assert self.artifacts[path]==body
        self.artifacts[path]=body;return digest(body.decode(errors='replace'))
    def deliver_candidate(self,p):return dict(url='https://github.com/synthetic/draft',draft=True)
    def publish_delivery_bundle(self,files,identity):
        from cloud_pilot.multilingual.publication import blob_hash
        if self.fail_export:raise GateError('SYNTHETIC_EXPORT_FAILURE')
        for p,b in files.items():
            if p in self.artifacts:assert self.artifacts[p]==b
        self.artifacts.update(files)
        return {p:blob_hash(b) for p,b in files.items()}

def fetch(source,allowed):
    e=next(e for t in plan()['articles'] for e in evidence(t)
           if source['source_id']==e['source_id'] and source['scope']==e['scope'])
    return e,e['text'].encode()

# These fixtures contain invented test articles. Repository similarity is tested
# with real temporary corpora in LocaleSimilarityTests; batch-to-batch checks
# remain active here through prior_bodies.
@patch('cloud_pilot.multilingual.similarity.corpus',lambda *args,**kwargs:[])
class Tests(unittest.TestCase):
    def setUp(self):
        self.net=patch.object(socket.socket,'connect',side_effect=AssertionError('NETWORK_FORBIDDEN'))
        self.net.start();self.addCleanup(self.net.stop)
        self.store=ArtifactStore();self.journal=ResponseJournal(self.store)
        self.api=API();self.models=DurableResponses(self.api,self.journal,prices(),lambda:None)
        self.gh=GitHub();self.plan=plan()

    def english(self):return Engine(self.plan,history(),self.journal,self.models,self.gh,fetch).run()

    def approved_cap8(self):
        from cloud_pilot.live.policy import CAP,AMENDED_CAP,BUDGET_APPROVAL_HASH
        self.journal.commit('synthetic-cap8',dict(kind='budget_amendment',previous_cap_nano_usd=CAP,cap_nano_usd=AMENDED_CAP,approval_hash=BUDGET_APPROVAL_HASH,settled_nano_usd=0))

    def test_full_two_articles_twelve_locales_fifty_calls_and_no_calls_on_resume(self):
        self.approved_cap8()
        deliveries=self.english()
        result=run_multilingual(self.plan,self.journal,self.models,self.gh,deliveries)
        self.assertEqual(24,len(result['files']));self.assertEqual(50,len(self.api.calls))
        self.assertEqual(22,self.api.calls.count('localization'))
        self.assertEqual(22,self.api.calls.count('independent_locale_review'))
        self.assertLess(len(json.dumps(self.store.data).encode()),800000)
        self.assertFalse(result['publish_approved']);self.assertFalse(result['website_published'])
        for f in result['files'].values():
            text=self.gh.artifacts[f['path']].decode()
            self.assertEqual(1,len(re.findall(r'^# ',text,re.M)))
            from cloud_pilot.multilingual.localize import LABELS
            self.assertNotIn('## SEO Metadata',text);self.assertIn('## '+LABELS[f['locale']][1],text)
            sidecar=json.loads(self.gh.artifacts[f['path'].removesuffix('.md')+'.editorial.json'])
            self.assertEqual('UNREVIEWED_EDITORIAL_METADATA',sidecar['status'])
        before=len(self.api.calls)
        again=run_multilingual(self.plan,self.journal,self.models,self.gh,self.english())
        self.assertEqual(result,again);self.assertEqual(before,len(self.api.calls))

    def test_delivery_failure_resume_reuses_translation_and_review(self):
        self.approved_cap8()
        deliveries=self.english();self.gh.fail_export=True
        with self.assertRaisesRegex(GateError,'EXPORT_FAILURE'):
            run_multilingual(self.plan,self.journal,self.models,self.gh,deliveries)
        self.assertEqual(50,len(self.api.calls)) # All texts are reviewed before the single atomic bundle export.
        self.gh.fail_export=False
        self.assertEqual(24,len(run_multilingual(self.plan,self.journal,self.models,self.gh,deliveries)['files']))
        self.assertEqual(50,len(self.api.calls))

    def test_whole_program_budget_can_stop_before_full_bundle(self):
        self.api.reported_usage=usage()
        deliveries=self.english()
        with self.assertRaisesRegex(GateError,'PROGRAM_CAP_EXCEEDED'):
            run_multilingual(self.plan,self.journal,self.models,self.gh,deliveries)
        self.assertLess(len(self.api.calls),50)
        self.assertFalse(any(k.startswith('multilingual-bundle:') for k in replay(self.store.data)['checkpoints']))

    def test_number_claim_and_url_drift_rejected(self):
        _,_,_,base=packets()
        for change,error in [('number','NUMERIC'),('claim','CLAIM'),('url','URL')]:
            r=translation(base,'fr')
            if change=='number':r['content']['sections'][0]['text']+=' 999 km'
            elif change=='claim':r['content']['sections'][0]['claim_ids']=['UNKNOWN']
            else:r['content']['internal_links']=['/invented/']
            with self.assertRaisesRegex(GateError,error):validate(r,base,'fr',1)

    def test_missing_full_sections_and_fake_target_script_rejected(self):
        _,_,_,base=packets();r=translation(base,'fr');r['content']['sections']=[]
        with self.assertRaisesRegex(GateError,'INCOMPLETE'):validate(r,base,'fr',1)
        r=translation(base,'ar');r['content']['sections'][0]['text']='French '+base['body']
        with self.assertRaisesRegex(GateError,'SCRIPT'):validate(r,base,'ar',1)

    def test_false_review_pass_hash_tamper_and_identity_rejected(self):
        _,_,_,base=packets();a=validate(translation(base,'fr'),base,'fr',1)
        r=locale_review(a,base);r['content']['checks']['natural_target_language']=False
        with self.assertRaisesRegex(GateError,'FALSE_PASS'):validate_review(r,a,base)
        r=locale_review(a,base);r['response_id']='synthetic-translator'
        with self.assertRaisesRegex(GateError,'IDENTITY'):validate_review(r,a,base)
        r=locale_review(a,base);r['content']['base_content_hash']='wrong'
        with self.assertRaisesRegex(GateError,'HASH'):validate_review(r,a,base)

    def test_locale_review_reject_prevents_bundle_success(self):
        self.english();base=self.journal.get_checkpoint('final:PILOT-ALPHA')
        class Bad:
            def call(s,op,stage,d):
                if d['stage']=='localization':return translation(d['english_article'],d['locale'])
                return locale_review(d['article'],d['english_article'],'REJECT')
        with self.assertRaisesRegex(GateError,'REJECT'):
            Localizer(Bad(),self.journal).run(base['article'],base['research'],'fr')

    def test_max_two_locale_revisions(self):
        self.english();b=self.journal.get_checkpoint('final:PILOT-ALPHA')
        class Bad:
            def call(s,op,stage,d):
                if d['stage']=='localization':return translation(d['english_article'],d['locale'])
                return locale_review(d['article'],d['english_article'],'REVISION_REQUIRED')
        with self.assertRaisesRegex(GateError,'MAX_TWO'):
            Localizer(Bad(),self.journal).run(b['article'],b['research'],'de')

    def test_real_execute_disabled_before_application_key_read(self):
        p=copy.deepcopy(self.plan);p.update(target_site='https://autobridgetrade.top/',locales=list(LOCALES),
            execution_phase='full',publication_enabled=False)
        p['articles'][0]['content_type']='VEHICLE_RECOMMENDATION'
        p['articles'][1]['content_type']='BUYING_GUIDE'
        h=json.loads((ROOT/'cloud_pilot/evidence/history-snapshot.json').read_text());p['history_hash']=digest(h)
        class Env(dict):
            def get(s,k,default=None):
                if k in ('OPENAI_API_KEY','AUTOBRIDGE_GITHUB_TOKEN'):raise AssertionError('EARLY_SECRET')
                return super().get(k,default)
        with tempfile.TemporaryDirectory() as td:
            files=[Path(td)/x for x in ('plan.json','prices.json','permit.json')]
            for f,v in zip(files,(p,prices(),{'authorized':False})):f.write_text(json.dumps(v))
            with patch('cloud_pilot.multilingual.__main__.os.environ',Env()):
                with self.assertRaisesRegex(GateError,'NOT_AUTHORIZED'):execute(*files)

    def test_plan_site_locales_and_publication_gates(self):
        p=copy.deepcopy(self.plan);p.update(target_site='https://autobridgetrade.top/',locales=list(LOCALES),
            execution_phase='full',publication_enabled=False)
        p['articles'][0]['content_type']='VEHICLE_RECOMMENDATION';p['articles'][1]['content_type']='BUYING_GUIDE'
        plan_check(p,history());p['publication_enabled']=True
        with self.assertRaisesRegex(GateError,'PUBLICATION'):plan_check(p,history())
        p['publication_enabled']=False;p['target_site']='https://autobridgeexport.com/'
        with self.assertRaisesRegex(GateError,'TARGET'):plan_check(p,history())

    def test_declared_chinese_encoding_and_unknown_encoding(self):
        text='<p>冷藏车采购资料核实</p>'
        self.assertEqual(text,decode(text.encode('gb18030'),'text/html; charset=gb2312'))
        with self.assertRaisesRegex(GateError,'ENCODING_UNSUPPORTED'):decode(b'abc','text/html; charset=utf-16')

    def test_source_script_only_and_ssrf_stop_without_models(self):
        class R:
            status=200
            def getheader(s,k,d=None):return {'Content-Type':'text/html'}.get(k,d)
            def read(s,n):return b'<html><script>fake article</script></html>'
        class C:
            def __init__(s,*a):pass
            def request(s,*a,**kw):pass
            def getresponse(s):return R()
            def close(s):pass
        t=self.plan['articles'][0]['sources'][0]
        with self.assertRaisesRegex(GateError,'INSUFFICIENT'):
            retrieve(t,{t['url']},resolver=lambda *a,**kw:[(0,0,0,'',('8.8.8.8',443))],connection=C)
        with self.assertRaisesRegex(GateError,'NON_PUBLIC'):
            retrieve(t,{t['url']},resolver=lambda *a,**kw:[(0,0,0,'',('127.0.0.1',443))],connection=C)
        self.assertEqual([],self.api.calls)

    def test_preflight_no_network_or_credential_reads(self):
        result=preflight();self.assertFalse(result['credentials_read']);self.assertEqual(0,result['real_api_calls'])
        self.assertEqual(12,len(result['supported_locales']))
        self.assertTrue(any(b['gate']=='approval' for b in result['blockers']))

    def test_uncertain_api_result_archive_failure_never_resends(self):
        self.store.save_artifact=lambda a:(_ for _ in ()).throw(OSError('synthetic storage failure'))
        data=dict(stage='writing',research=packets()[2])
        with self.assertRaises(Exception):self.models.call('once','writing',data)
        with self.assertRaisesRegex(GateError,'NO_RESEND'):
            self.models.call('once','writing',data)
        self.assertEqual(1,len(self.api.calls))

if __name__=='__main__':unittest.main()

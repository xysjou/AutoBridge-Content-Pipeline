import copy
import tempfile
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from cloud_pilot.contract import GateError,ROOT
from cloud_pilot.multilingual.activation_review import corpus,dedup_request,run
from cloud_pilot.multilingual.__main__ import execute

class Journal:
    def __init__(self):self.items={}
    def checkpoint(self,k,v):self.items[k]=v

class Tests(unittest.TestCase):
    def test_current_pointer_excludes_old_version(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=root/'batches/b/articles/a';(p/'versions').mkdir(parents=True)
            (p/'CURRENT').write_text('v2');(p/'versions/v1.md').write_text('# Old\nOld body')
            (p/'versions/v2.md').write_text('# Current\nCurrent body')
            self.assertEqual(['Current'],[d['title'] for d in corpus(root)])

    def test_actual_related_review_includes_reserve_and_foton_full_text(self):
        plan=json.loads((ROOT/'cloud_pilot/runtime/trade-two-articles.plan.json').read_text())
        r=dedup_request(plan)
        self.assertTrue(any('Aumark' in d['title'] for d in r['related_full_text']))
        self.assertTrue(any(d['context_role']=='reserve_not_published' for d in r['related_full_text']))
        self.assertTrue(all('text' in d for d in r['related_full_text']))
        self.assertTrue(any('AB50_025_' in d['path'] for d in r['related_full_text']))
        self.assertTrue(any('AB50_035_' in d['path'] for d in r['related_full_text']))

    def test_code_block_still_collects_topic_review_but_cannot_pass(self):
        p={'articles':[{'article_id':'A'},{'article_id':'B'}]}
        class M:
            calls=[]
            def call(s,op,stage,data):
                s.calls.append(stage)
                c=dict(decision='BLOCK',findings=[],human_reviewed=False,publish_approved=False)
                if stage=='research':c.update(decision='PASS',articles=[dict(article_id=a['article_id'],decision='DISTINCT',nearest_paths=[]) for a in p['articles']],additional_paths=[])
                return dict(content=c)
        m=M()
        with patch('cloud_pilot.multilingual.activation_review.dedup_request',return_value={'corpus_index':[],'corpus_hash':'hash'}),patch('cloud_pilot.multilingual.activation_review.code_request',return_value={}):
            self.assertEqual('CODE_REVIEW_BLOCKED',run(p,'code',Journal(),m,workflow_evidence={'test':True},scope_attestation={'test':True})['status'])
        self.assertEqual(['review','research'],m.calls)

    def test_overlap_never_grants_dedup_pass(self):
        p={'articles':[{'article_id':'A'},{'article_id':'B'}]}
        packet={'corpus_hash':'corpus','corpus_index':[{'path':'existing.md'}]}
        class M:
            def call(s,op,stage,data):
                content=dict(decision='PASS',findings=[],human_reviewed=False,publish_approved=False)
                if stage=='research':content.update(decision='OVERLAP',articles=[dict(article_id='A',decision='DISTINCT',nearest_paths=[]),dict(article_id='B',decision='OVERLAP',nearest_paths=['existing.md'])],additional_paths=[])
                return dict(content=content)
        with patch('cloud_pilot.multilingual.activation_review.dedup_request',return_value=packet),patch('cloud_pilot.multilingual.activation_review.code_request',return_value={}):
            self.assertEqual('TOPIC_REVIEW_HOLD',run(p,'code',Journal(),M(),workflow_evidence={'test':True},scope_attestation={'test':True})['status'])

    def test_genuine_topic_receipt_reuses_only_a_technical_baseline_change(self):
        from cloud_pilot.contract import digest
        from cloud_pilot.multilingual.activation_review import intake_hash,verified_topic
        from cloud_pilot.multilingual.accounting import ResponseJournal,DurableResponses
        from cloud_pilot.multilingual.tests.test_multilingual import ArtifactStore
        from cloud_pilot.stage2_tests.test_live import plan,prices,usage
        p=plan()
        for t in p['articles']:t['research_baseline_sha']='a'*40
        packet=dict(stage='independent_topic_dedup',intake_hash=intake_hash(p),corpus_hash='fixed-corpus',topics=['same buyer tasks'],retrieved_reference_evidence={'reference':'same actual text'})
        content=dict(decision='PASS',additional_paths=[],articles=[dict(article_id=t['article_id'],decision='DISTINCT') for t in p['articles']],human_reviewed=False,publish_approved=False)
        class API:
            host='api.openai.com';calls=0
            def request(self,method,path,payload):
                self.calls+=1
                return 200,dict(id='resp-synthetic-dedup',model=payload['model'],status='completed',usage=usage(),
                    output=[dict(type='message',content=[dict(type='output_text',text=json.dumps(content))])])
        api=API();j=ResponseJournal(ArtifactStore());result=DurableResponses(api,j,prices(),lambda:None).call('activation-dedup:'+digest(packet),'research',packet)
        j.checkpoint('activation-review:original',dict(code_sha='a'*40,intake_hash=intake_hash(p),dedup_request_hash=digest(packet),
            corpus_hash=packet['corpus_hash'],topic_review=result))
        current=copy.deepcopy(p)
        for t in current['articles']:t['research_baseline_sha']='b'*40
        new_packet=dict(packet,intake_hash=intake_hash(current))
        reused,proof=verified_topic(j,new_packet,current)
        self.assertEqual(result,reused);self.assertEqual(1,api.calls)
        self.assertEqual(digest(packet),proof['packet_hash']);self.assertEqual(digest(new_packet),proof['current_packet_hash'])
        for change in ('buyer','source','corpus','url'):
            changed_plan=copy.deepcopy(current);changed_packet=copy.deepcopy(new_packet)
            if change=='buyer':changed_plan['articles'][0]['buyer_task']='Different buyer decision'
            elif change=='source':changed_packet['retrieved_reference_evidence']['reference']='changed source text'
            elif change=='corpus':changed_packet['corpus_hash']='changed history'
            else:changed_plan['articles'][0]['proposed_url']='/pilot-only/different/'
            changed_packet['intake_hash']=intake_hash(changed_plan)
            self.assertEqual((None,None),verified_topic(j,changed_packet,changed_plan))


class AuditReasoningTests(unittest.TestCase):
    def test_code_audit_uses_medium_but_fact_review_keeps_high(self):
        from cloud_pilot.live.responses import build_request
        self.assertEqual('medium',build_request('review',{'stage':'independent_candidate_code_review'})['reasoning']['effort'])
        self.assertEqual('high',build_request('review',{'stage':'independent_research_review'})['reasoning']['effort'])
        self.assertEqual(24000,build_request('research',{'stage':'research'})['max_output_tokens'])
        self.assertEqual(8000,build_request('research',{'stage':'independent_topic_dedup'})['max_output_tokens'])

class BudgetAmendmentTests(unittest.TestCase):
    def test_amendment_preserves_original_header_and_history(self):
        from cloud_pilot.live.ledger import genesis,append,replay
        from cloud_pilot.live.policy import CAP,AMENDED_CAP,BUDGET_APPROVAL_HASH
        from cloud_pilot.contract import digest
        d=genesis('synthetic');d=append(d,'before',dict(kind='checkpoint',key='old',artifact={},artifact_hash=digest({})))
        old=copy.deepcopy(d)
        d=append(d,'cap8',dict(kind='budget_amendment',previous_cap_nano_usd=CAP,cap_nano_usd=AMENDED_CAP,approval_hash=BUDGET_APPROVAL_HASH,settled_nano_usd=0))
        self.assertEqual(old['events'],d['events'][:-1]);self.assertEqual(CAP,d['cap_nano_usd'])
        self.assertEqual(AMENDED_CAP,replay(d)['cap_nano_usd'])
        with self.assertRaisesRegex(GateError,'INVALID_BUDGET_AMENDMENT'):append(d,'again',d['events'][-1]['payload'])
    def test_unapproved_or_changed_spend_amendment_rejected(self):
        from cloud_pilot.live.ledger import genesis,append
        from cloud_pilot.live.policy import CAP,AMENDED_CAP,BUDGET_APPROVAL_HASH
        p=dict(kind='budget_amendment',previous_cap_nano_usd=CAP,cap_nano_usd=AMENDED_CAP,approval_hash=BUDGET_APPROVAL_HASH,settled_nano_usd=0)
        for key,value in [('cap_nano_usd',9000000000),('approval_hash','wrong'),('settled_nano_usd',1)]:
            with self.assertRaises(GateError):append(genesis('synthetic'),'bad',dict(p,**{key:value}))

if __name__=='__main__':unittest.main()

class LiveSiteTests(unittest.TestCase):
    def fixture(self,root):
        import hashlib
        from datetime import datetime,timezone
        from cloud_pilot.multilingual.live_site import FOLDER,BASE
        p=root/FOLDER;p.mkdir(parents=True);stamp=datetime.now(timezone.utc).isoformat()
        url=BASE+'/en/guides/live-only-acceptance.html';text='Existing refrigerated truck acceptance buyer decision. '*12
        xml=('<urlset><url><loc>'+url+'</loc></url></urlset>').encode();(p/'sitemap.xml').write_bytes(xml)
        docs=[dict(url=url,final_url=url,http_status=200,retrieved_at=stamp,title='Existing acceptance',text=text,text_sha256=hashlib.sha256(text.encode()).hexdigest(),raw_sha256='synthetic')]
        b=json.dumps(docs).encode();(p/'pages-00.json').write_bytes(b)
        m=dict(schema='autobridge-live-English-corpus/1',target_site=BASE+'/',captured_at=stamp,sitemap_sha256=hashlib.sha256(xml).hexdigest(),urls=[url],index_pages={'guides':dict(links=['/en/guides/live-only-acceptance.html'])},chunks=[dict(path='pages-00.json',sha256=hashlib.sha256(b).hexdigest())])
        (p/'manifest.json').write_text(json.dumps(m));return p,m
    def test_live_site_staleness_coverage_and_mutation_hold(self):
        from cloud_pilot.multilingual.live_site import load
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p,m=self.fixture(root);self.assertEqual(1,len(load(root)['documents']))
            old=copy.deepcopy(m);m['captured_at']='2020-01-01T00:00:00+00:00';(p/'manifest.json').write_text(json.dumps(m))
            with self.assertRaisesRegex(GateError,'STALE'):load(root)
            m=copy.deepcopy(old);m['urls']=[];(p/'manifest.json').write_text(json.dumps(m))
            with self.assertRaisesRegex(GateError,'INVENTORY_INCOMPLETE'):load(root)
            (p/'manifest.json').write_text(json.dumps(old));(p/'pages-00.json').write_text('[]')
            with self.assertRaisesRegex(GateError,'CONTENT_CHANGED'):load(root)
    def test_live_only_duplicate_reaches_independent_gate(self):
        from cloud_pilot.multilingual.live_site import load
        from cloud_pilot.contract import digest
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);self.fixture(root);site=load(root)
        p=json.loads((ROOT/'cloud_pilot/runtime/trade-two-articles.plan.json').read_text())
        url=site['documents'][0]['url']
        class M:
            def call(self,op,stage,data):
                c=dict(decision='PASS',findings=[],human_reviewed=False,publish_approved=False)
                if stage=='research':
                    assert data['current_live_site']['documents'][0]['text']==site['documents'][0]['text']
                    c.update(decision='OVERLAP',articles=[dict(article_id=a['article_id'],decision='OVERLAP' if i else 'DISTINCT',nearest_paths=[url] if i else []) for i,a in enumerate(p['articles'])],additional_paths=[])
                return dict(content=c)
        with patch('cloud_pilot.multilingual.live_site.load',return_value=site),patch('cloud_pilot.multilingual.activation_review.code_request',return_value={}):
            result=run(p,'code',Journal(),M(),workflow_evidence={'test':True},scope_attestation={'test':True})
        self.assertEqual('TOPIC_REVIEW_HOLD',result['status'])
    def test_unverified_historical_and_unavailable_live_links_are_rejected(self):
        from cloud_pilot.stage2_tests.test_live import packets,writer_result
        from cloud_pilot.live.stages import check_writing
        _,_,research,_=packets()
        for url in ['/historical-draft-only/','/previously-live-now-unavailable/']:
            r=writer_result(research);r['content']['internal_links']=[url]
            with self.assertRaisesRegex(GateError,'UNVERIFIED_LIVE_INTERNAL_LINK'):
                check_writing(r,research,1,{'entries':[{'url':url}],'documents':[]},[])

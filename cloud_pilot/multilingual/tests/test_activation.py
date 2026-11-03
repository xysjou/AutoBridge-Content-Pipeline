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

if __name__=='__main__':unittest.main()

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
            self.assertEqual('CODE_REVIEW_BLOCKED',run(p,'code',Journal(),m)['status'])
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
            self.assertEqual('TOPIC_REVIEW_HOLD',run(p,'code',Journal(),M())['status'])

if __name__=='__main__':unittest.main()

"""Regression tests for findings from real independent audit resp_07f96fc8..."""
import copy
import json
import unittest
from unittest.mock import patch
from cloud_pilot.contract import ROOT,GateError,digest
from cloud_pilot.multilingual.activation_review import intake_hash,dedup_request,verify_receipt,code_paths
from cloud_pilot.multilingual.startup import EpochJournal,verify as startup
from cloud_pilot.multilingual.pricing import check,RATES,verify as pricing
from cloud_pilot.multilingual.delivery import VerifiedGitHub

class Tests(unittest.TestCase):
    def test_status_and_phase_change_preserve_intake_but_topic_edit_does_not(self):
        p=json.loads((ROOT/'cloud_pilot/runtime/trade-two-articles.plan.json').read_text())
        h=intake_hash(p);q=copy.deepcopy(p);q.update(semantic_dedup_status='INDEPENDENTLY_CONFIRMED',execution_phase='full',evidence_revision=2)
        self.assertEqual(h,intake_hash(q));self.assertEqual(dedup_request(p),dedup_request(q))
        q['articles'][0]['buyer_task']='different intent';self.assertNotEqual(h,intake_hash(q))

    def test_self_declared_dedup_status_never_authorizes_execution(self):
        p=json.loads((ROOT/'cloud_pilot/runtime/trade-two-articles.plan.json').read_text());p['semantic_dedup_status']='INDEPENDENTLY_CONFIRMED'
        class J:
            def get_checkpoint(s,k):return None
        with self.assertRaisesRegex(GateError,'RECEIPT_REQUIRED'):verify_receipt(p,'code',J())

    def test_old_receipt_cannot_authorize_changed_corpus_or_code(self):
        p=json.loads((ROOT/'cloud_pilot/runtime/trade-two-articles.plan.json').read_text())
        class J:
            def get_checkpoint(s,k):return {'status':'ACTIVATION_REVIEW_PASS','code_sha':'old'}
        with self.assertRaisesRegex(GateError,'RECEIPT_DRIFT'):verify_receipt(p,'new',J())

    def test_all_security_modules_and_installed_workflow_are_reviewed(self):
        paths=code_paths()
        for p in ('cloud_pilot/live/sources.py','cloud_pilot/contract.py','cloud_pilot/audit.py',
                  'cloud_pilot/multilingual/startup.py','.github/workflows/cloud-pilot-manual.yml'):
            self.assertIn(p,paths)

    def test_source_refresh_creates_new_namespace_without_overwriting_old(self):
        class J:
            data={}
            def checkpoint(s,k,v):s.data[k]=v
            def get_checkpoint(s,k):return s.data.get(k)
        j=J();old=EpochJournal(j,1);new=EpochJournal(j,2)
        old.checkpoint('research:A',{'old':True})
        self.assertIsNone(new.get_checkpoint('research:A'))
        new.checkpoint('research:A',{'new':True});self.assertEqual({'old':True},old.get_checkpoint('research:A'))

    def test_unmerged_main_is_rejected_before_live_execution(self):
        with patch('cloud_pilot.multilingual.startup.subprocess.run') as r:
            r.return_value.returncode=1
            with self.assertRaisesRegex(GateError,'DOES_NOT_CONTAIN'):startup('main',{})

    def test_current_provider_price_and_context_drift_fail_closed(self):
        for m,p in RATES.items():
            text=' '.join(label+' $'+str(p[key]/1000) for label,key in [('Input','input'),('Cached input','cached'),('Cache writes','write'),('Output','output')])
            text+=' 1,050,000 context window 128,000 max output tokens 30-minute retention Cache writes are billed at 1.25x the uncached input token rate. Prompts with more than 272K input tokens are priced at 2x input and cache rates and 1.5x output for the full request.'
            self.assertTrue(check(m,text))
            with self.assertRaisesRegex(GateError,'PRICE_CHANGED'):check(m,text.replace('Input $'+str(p['input']/1000),'Input $999'))
            with self.assertRaisesRegex(GateError,'CONTEXT_CHANGED'):check(m,text.replace('1,050,000','2,000,000'))

    def test_candidate_extra_file_or_changed_parent_is_rejected(self):
        class A:host='api.github.com'
        gh=VerifiedGitHub(A());gh.ref=lambda branch:'base'
        c=dict(sha='head',parents=[{'sha':'parent'}],commit={'message':'message'},files=[dict(filename='candidate.json',status='added'),dict(filename='unrelated.md',status='added')])
        gh.call=lambda *a,**k:c
        with self.assertRaisesRegex(GateError,'COMPLETE_DIFF'):gh.verify_commit('head','candidate.json',b'body','message')
        c['files']=c['files'][:1]
        def api(method,path,*a,**k):
            if path.startswith('/commits/'):return c
            return dict(status='diverged',merge_base_commit={'sha':'other'})
        gh.call=api
        with self.assertRaisesRegex(GateError,'NOT_FROM_INTEGRATION'):gh.verify_commit('head','candidate.json',b'body','message')

if __name__=='__main__':unittest.main()

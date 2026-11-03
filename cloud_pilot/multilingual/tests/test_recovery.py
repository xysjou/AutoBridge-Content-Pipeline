"""Offline regression of the actual blocking findings; no provider call is made here."""
import copy
import base64
import os
import unittest
from unittest.mock import patch
from cloud_pilot.contract import GateError,digest,ROOT
from cloud_pilot.live.ledger import Journal,replay
from cloud_pilot.live.responses import Responses
from cloud_pilot.stage2_tests.test_live import ModelAPI,MemoryStore,prices,plan,evidence,research_result
from cloud_pilot.multilingual.tests.test_multilingual import ArtifactStore,packets,translation
from cloud_pilot.multilingual.accounting import ResponseJournal,CountedResponses,AnchoredStore
from cloud_pilot.multilingual.startup import EpochJournal
from cloud_pilot.multilingual.authorization import lease,workflows
from cloud_pilot.multilingual.localize import validate,review_request,markdown
from cloud_pilot.multilingual.research_contract import IDENTITY,validate as research_validate

class Tests(unittest.TestCase):
    def test_reusable_caller_forwards_only_protected_runtime_names(self):
        text=(ROOT/'.github/workflows/cloud-pilot-manual.yml').read_text()
        trusted=(ROOT/'.github/workflows/cloud-pilot-trusted.yml').read_text()
        sha=text.split('cloud-pilot-trusted.yml@')[1].splitlines()[0]
        p=dict(authorized_run_id='100',caller_workflow_sha='a'*40,trusted_workflow_sha=sha,
               ledger_anchor=dict(events_count=14,last_event_hash='hash',settled_nano_usd=259886425,
                                  reconciled_receipts=['receipts'],operator_verified=True))
        class API:
            def request(s,method,path):
                value=current[0] if 'manual.yml' in path else trusted
                return 200,dict(encoding='base64',content=base64.b64encode(value.encode()).decode())
        class GH:api=API();prefix='/repos/example/repo'
        current=[text]
        with patch.dict(os.environ,{'GITHUB_RUN_ID':'100','GITHUB_RUN_ATTEMPT':'1','GITHUB_WORKFLOW_SHA':'a'*40}):
            for value in (text,text+'      EXTRA: ${{ secrets.UNRELATED }}\n',
                          text+'    steps: []\n',text.replace('    secrets:\n','    secrets: inherit\n')):
                current[0]=value;p.update(caller_workflow_hash=digest(value),trusted_workflow_hash=digest(trusted))
                if value==text:workflows(p,GH())
                else:
                    with self.assertRaisesRegex(GateError,'FORWARDING_SCOPE'):workflows(p,GH())

    def test_provider_count_reserves_this_request_and_resume_never_recounts_or_resends(self):
        class API(ModelAPI):
            counts=0
            def request(s,method,path,payload):
                if path.endswith('/input_tokens'):
                    s.counts+=1;return 200,dict(object='response.input_tokens',input_tokens=1000)
                return super().request(method,path,payload)
        api=API();j=ResponseJournal(ArtifactStore());client=CountedResponses(api,j,prices(),lambda:None)
        self.assertEqual({'ok':True},client.call('counted','writing',{})['content'])
        op=next(iter(j.read()[2]['operations'].values()))
        self.assertEqual(2024,op['input_bound']);self.assertLess(op['amount'],100000000)
        client.call('counted','writing',{})
        self.assertEqual(1,api.counts);self.assertEqual(1,len(api.calls))

    def test_provider_count_failure_prevents_any_generation(self):
        class API(ModelAPI):
            def request(s,method,path,payload):
                if path.endswith('/input_tokens'):return 403,{}
                raise AssertionError('GENERATION_FORBIDDEN')
        j=ResponseJournal(ArtifactStore())
        with self.assertRaisesRegex(GateError,'COUNT_UNAVAILABLE'):
            CountedResponses(API(),j,prices(),lambda:None).call('never','writing',{})
        self.assertEqual(0,len(j.read()[2]['operations']))

    def test_protected_floor_and_in_run_progress_cannot_be_rolled_back(self):
        store=MemoryStore();j=Journal(store)
        Responses(ModelAPI(),j,prices(),lambda:None).call('paid','research',{})
        data=copy.deepcopy(store.data);events=data['events']
        anchor=dict(events_count=len(events),last_event_hash=events[-1]['hash'],
                    settled_nano_usd=sum(e['payload'].get('cost',0) for e in events),
                    reconciled_receipts=[dict(response_id=e['payload']['response']['id'],model=e['payload']['response']['model'],
                        usage_hash=digest(e['payload']['response']['usage']),cost=e['payload']['cost']) for e in events if e['payload']['kind']=='result'])
        protected=AnchoredStore(store,anchor);safe=Journal(protected);safe.read()
        store.data['events']=[]
        with self.assertRaisesRegex(GateError,'FLOOR_ROLLBACK'):safe.read()
        store.data=copy.deepcopy(data);safe.read();safe.checkpoint('new',{'progress':True})
        store.data=copy.deepcopy(data)
        with self.assertRaisesRegex(GateError,'IN_RUN_LEDGER_ROLLBACK'):safe.read()

    def test_approval_cannot_be_reused_by_another_run_or_rerun_attempt(self):
        p=dict(authorized_run_id='100',caller_workflow_sha='a'*40,trusted_workflow_sha='b'*40,
            ledger_anchor=dict(events_count=14,last_event_hash='hash',settled_nano_usd=259886425,
                               reconciled_receipts=['actual-three-receipts'],operator_verified=True))
        with patch.dict(os.environ,{'GITHUB_RUN_ID':'100','GITHUB_RUN_ATTEMPT':'1','GITHUB_WORKFLOW_SHA':'a'*40}):
            lease(p)
            os.environ['GITHUB_RUN_ID']='101'
            with self.assertRaisesRegex(GateError,'RUN_ID_DRIFT'):lease(p)
            os.environ['GITHUB_RUN_ID']='100';os.environ['GITHUB_RUN_ATTEMPT']='2'
            with self.assertRaisesRegex(GateError,'RUN_REPLAY'):lease(p)

    def test_checkpoints_are_isolated_by_code_and_intake_and_revision(self):
        j=Journal(MemoryStore());a=EpochJournal(j,1,dict(code='A',topic='A'))
        a.checkpoint('final:A',{'original':True})
        for code,topic,revision in [('B','A',1),('A','B',1),('A','A',2)]:
            self.assertIsNone(EpochJournal(j,revision,dict(code=code,topic=topic)).get_checkpoint('final:A'))
        self.assertEqual({'original':True},a.get_checkpoint('final:A'))

    def test_exact_final_public_locale_render_is_in_independent_review(self):
        _,_,research,base=packets();article=validate(translation(base,'fr'),base,'fr',1)
        rendered=markdown(article,research,research['topic'],public_only=True)
        req=review_request(article,base,research)
        self.assertEqual(rendered,req['rendered_public_markdown']);self.assertEqual(digest(rendered),req['rendered_hash'])
        self.assertIn('Sources et vérification',rendered)
        self.assertNotIn('Editorial Review',rendered);self.assertNotIn('Pending rights',rendered)

    def test_complete_vehicle_identity_is_required_before_writing(self):
        topic=plan()['articles'][0];topic['content_type']='VEHICLE_RECOMMENDATION'
        ev=evidence(topic);r=research_result(topic,ev)['content']
        for f in r['facts']:f.update(kind='external_fact',checked_date='2026-11-02',buyer_applicability='test only')
        r['fact_boundary']={k:dict(value='synthetic',confidence='SINGLE_SOURCE',source_ids=['S0']) for k in IDENTITY}
        r['handoff']={k:topic[k] for k in ('article_id','content_type','search_intent','buyer_task')}
        from cloud_pilot.contract import BASELINE
        r['handoff'].update(research_baseline_sha=BASELINE,fact_sheet_version=1,source_log_version=1,
            conflict_list=[],time_sensitive_facts=[],facts_not_allowed_in_body=r['blocked_facts'],locks=[],
            skill_impact=dict(research=False,writing=False,lessons=False,update_required=False,reason='synthetic unchanged rules'))
        research_validate(r,topic,ev)
        del r['fact_boundary']['drivetrain']
        with self.assertRaisesRegex(GateError,'IDENTITY_INCOMPLETE'):research_validate(r,topic,ev)

if __name__=='__main__':unittest.main()

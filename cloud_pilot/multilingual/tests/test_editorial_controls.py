"""Exercise the actual article contracts that the live pilot uses."""
import copy
import unittest
from unittest.mock import patch
from cloud_pilot.contract import BASELINE,GateError
from cloud_pilot.stage2_tests.test_live import plan,evidence,research_result,writer_result,history
from cloud_pilot.live.stages import check_research,writing_request,check_writing
from cloud_pilot.multilingual.research_contract import IDENTITY,handoff_assessment
from cloud_pilot.multilingual.startup import review_context

def active_case(kind):
    topic=plan()['articles'][0];topic['content_type']=kind;ev=evidence(topic)
    response=research_result(topic,ev);r=response['content']
    for f in r['facts']:
        f.update(kind='external_fact',standard_related=False,quantitative=True,value='synthetic ID',unit='test identifier',
                 checked_date='2026-11-03',buyer_applicability='Synthetic tests only')
    r['fact_boundary']=({k:dict(value='Synthetic',confidence='VERIFIED',source_ids=['S0'],fact_ids=['F0']) for k in IDENTITY}
                         if kind=='VEHICLE_RECOMMENDATION' else dict(scope='Synthetic',excluded_claims=[]))
    h={k:topic[k] for k in ('article_id','content_type','search_intent','buyer_task')}
    h.update(research_baseline_sha=BASELINE,fact_sheet_version=1,source_log_version=1,conflict_list=[],
        time_sensitive_facts=[],facts_not_allowed_in_body=r['blocked_facts'],locks=[],research_locked=False,
        writing_locked=False,fact_update_required=False,
        skill_impact=dict(research=False,writing=False,lessons=False,update_required=False,reason='Synthetic unchanged editorial rules'),
        review_handoff_assessment=[dict(path=p,applicable=False,reason='Synthetic fixture; no real topic',superseded_by=None)
                                   for p in review_context(all_versions=True)])
    r['handoff']=h
    return topic,ev,response

class Tests(unittest.TestCase):
    def test_active_standard_classification_requires_current_fields_for_both_article_types(self):
        for kind in ('VEHICLE_RECOMMENDATION','BUYING_GUIDE'):
            topic,ev,r=active_case(kind);r['content']['facts'][0]['standard_related']=True
            with self.subTest(kind=kind),self.assertRaisesRegex(GateError,'CURRENT_STANDARD_FIELDS'):
                check_research(r,topic,ev)

    def test_active_quantitative_fact_without_value_or_unit_stops_research(self):
        for kind in ('VEHICLE_RECOMMENDATION','BUYING_GUIDE'):
            topic,ev,r=active_case(kind);del r['content']['facts'][0]['unit']
            with self.subTest(kind=kind),self.assertRaisesRegex(GateError,'QUANTITATIVE_VALUE_UNIT'):
                check_research(r,topic,ev)

    def test_identity_requires_allowed_direct_fact_and_primary_authority_for_verified(self):
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION');check_research(r,topic,ev)
        r['content']['fact_boundary']['model']['fact_ids']=['UNKNOWN']
        with self.assertRaisesRegex(GateError,'IDENTITY_ALLOWED_FACT'):check_research(r,topic,ev)
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION');ev[0]['tier']='T3'
        with self.assertRaisesRegex(GateError,'T1_REQUIRED|PRIMARY_AUTHORITY'):check_research(r,topic,ev)

    def test_locked_or_updated_handoff_cannot_reach_writing(self):
        topic,ev,r=active_case('BUYING_GUIDE');packet=check_research(r,topic,ev)
        for key in ('research_locked','writing_locked','fact_update_required'):
            p=copy.deepcopy(packet);p['fact_sheet']['handoff'][key]=True
            with self.subTest(key=key),self.assertRaisesRegex(GateError,'ARTICLE_STATUS_LOCK'):writing_request(p,1)

    def test_writer_must_assess_skill_impact_and_every_handoff(self):
        topic,ev,r=active_case('BUYING_GUIDE');packet=check_research(r,topic,ev)
        result=writer_result(packet)
        with self.assertRaisesRegex(GateError,'IMPACT_ASSESSMENT'):check_writing(result,packet,1,history(),[])
        result['content'].update(skill_impact=dict(research=False,writing=False,lessons=False,update_required=False,
            reason='Synthetic writing assessment'),review_handoff_assessment=packet['fact_sheet']['handoff']['review_handoff_assessment'])
        a=check_writing(result,packet,1,history(),[])
        self.assertEqual('Synthetic writing assessment',a['skill_impact_assessment']['reason'])
        self.assertNotIn('skill_impact',a['public'])

    def test_unclassified_handoff_is_not_silently_omitted(self):
        with patch('cloud_pilot.multilingual.startup.review_context',return_value={'old.json':'{}','new.json':'{}'}):
            with self.assertRaisesRegex(GateError,'CLASSIFICATION_COVERAGE'):
                handoff_assessment([dict(path='old.json',applicable=True,reason='only old',superseded_by=None)])

if __name__=='__main__':unittest.main()

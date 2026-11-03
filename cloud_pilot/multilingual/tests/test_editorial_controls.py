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
    topic['source_vehicle_identity']=dict(model='Testmodel',model_year='2026',trim='TEST')
    response=research_result(topic,ev);r=response['content']
    for f in r['facts']:
        f.update(kind='external_fact',standard_related=False,standard_assessment='NOT_REGULATORY',quantitative=True,value='synthetic ID',unit='test identifier',
                 checked_date='2026-11-03',buyer_applicability='Synthetic tests only')
    values=dict(brand='Testbrand',model='Testmodel',model_year='2026',generation='TEST',body_style='SUV',powertrain='TEST',drivetrain='2WD',original_sales_market='SYNTHETIC-ALPHA',production_boundary='Testproduction',trim_variant='TEST')
    if kind=='VEHICLE_RECOMMENDATION':
        extra=' '.join(k+': '+v+';' for k,v in values.items());ev[0]['text']+=' '+extra+' Testmodel 2026 TEST exact vehicle reference heading'
        for k,v in values.items():
            f=copy.deepcopy(r['facts'][0]);f.update(id='I_'+k,identity_field=k,statement=k+': '+v,
                quotes=[dict(source_id='S0',quote=k+': '+v+';')],value=v,unit='identity reference')
            r['facts'].append(f);r['allowed_facts'].append(f['id'])
        r['fact_boundary']={k:dict(value=v,confidence='VERIFIED',source_ids=['S0'],fact_ids=['I_'+k]) for k,v in values.items()}
    else:r['fact_boundary']=dict(scope='Synthetic',excluded_claims=[])
    for c in r['source_checks']:c.update(official_source=True,scope_status='MATCHED')
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
    def acceptance(self,packet):
        from cloud_pilot.multilingual.research_contract import CHECKS
        rows=[]
        for f in packet['fact_sheet']['facts']:
            if f['id'] not in packet['fact_sheet']['allowed_facts']:continue
            row=dict(fact_id=f['id'],role='CORE_VEHICLE_SPEC' if f.get('identity_field') else 'BACKGROUND',
                     source_ids=f['source_ids'],entailed=True,exact_vehicle_applicability=True,reason='Synthetic independently assessed fact',identity_contexts=[])
            if f.get('identity_field'):
                row['identity_contexts']=[dict(source_id=q['source_id'],field_quote=q['quote'],vehicle_context_quote='Testmodel 2026 TEST exact vehicle reference heading',linked_same_vehicle=True) for q in f['quotes']]
            rows.append(row)
        return dict(response_id='independent',content=dict(research_hash=packet['research_hash'],decision='ACCEPT',checks={k:True for k in CHECKS},findings=[],fact_assessments=rows,human_reviewed=False,publish_approved=False))

    def test_independent_classification_catches_unlabelled_core_and_regulatory_claims(self):
        from cloud_pilot.multilingual.research_contract import accept
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION');p=check_research(r,topic,ev);review=self.acceptance(p);accept(review,p)
        p['fact_sheet']['facts'][0].update(statement='A permit is compulsory to import this truck',kind='editorial_method',standard_assessment='NOT_REGULATORY')
        review['content']['fact_assessments'][0]['role']='REGULATORY_OR_STANDARD'
        with self.assertRaisesRegex(GateError,'REGULATORY_OBLIGATION_OUTSIDE'):accept(review,p)
        review=self.acceptance(p);review['content']['fact_assessments'][0]['role']='CORE_VEHICLE_SPEC'
        p['evidence'][0]['tier']='T3'
        with self.assertRaisesRegex(GateError,'CORE_SPEC_TIER_OR_SCOPE'):accept(review,p)

    def test_independent_identity_context_excludes_another_model(self):
        from cloud_pilot.multilingual.research_contract import accept
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION');p=check_research(r,topic,ev);review=self.acceptance(p)
        identity=next(x for x in review['content']['fact_assessments'] if x['identity_contexts'])
        identity['identity_contexts'][0]['vehicle_context_quote']='Different model 2024 BASE reference heading'
        with self.assertRaisesRegex(GateError,'EXACT_VEHICLE'):accept(review,p)

    def test_scope_boolean_cannot_hide_context_only_primary(self):
        from cloud_pilot.multilingual.research_contract import validate
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION');c=r['content']['source_checks'][0]
        c.update(scope_status='CONTEXT_ONLY',official_source=False,scope_match=True)
        with self.assertRaisesRegex(GateError,'SCOPE_FIELDS_CONTRADICT'):validate(r['content'],topic,ev)
        c['scope_match']=False
        with self.assertRaisesRegex(GateError,'MATCHED_PRIMARY'):validate(r['content'],topic,ev)

    def test_real_second_research_epoch_locks_old_writer_before_replacement(self):
        from cloud_pilot.multilingual.editorial_state import EditorialState
        from cloud_pilot.multilingual.tests.test_multilingual import ArtifactStore
        from cloud_pilot.multilingual.accounting import ResponseJournal
        from cloud_pilot.multilingual.startup import EpochJournal
        base=ResponseJournal(ArtifactStore());first=EditorialState(EpochJournal(base,1,{'code':'first'}));second=EditorialState(EpochJournal(base,2,{'code':'second'}))
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION');aid=topic['article_id']
        start=first.begin(aid,'epoch-one');self.assertEqual(start['version'],1);old=check_research(r,topic,ev);old['research_start']=start;first.lock(old)
        start=second.begin(aid,'epoch-two');self.assertEqual(start['version'],2)
        with self.assertRaisesRegex(GateError,'RESEARCH_LOCK_UPDATE_REQUIRED'):first.check(old)
        r['content']['handoff'].update(fact_sheet_version=2,source_log_version=2)
        new=check_research(r,topic,ev,2);new['research_start']=start;second.lock(new)
        with self.assertRaisesRegex(GateError,'RESEARCH_CHANGED_AFTER_WRITING_STARTED'):first.check(old)
        second.check(new)
    def test_identity_rejects_unrelated_quote_and_t3_core_spec(self):
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION')
        f=r['content']['facts'][-1];f['quotes'][0]['quote']='synthetic public evidence'
        ev[0]['text']+=' synthetic public evidence'
        with self.assertRaisesRegex(GateError,'IDENTITY_SCOPED_VALUE_QUOTE'):check_research(r,topic,ev)
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION');ev[0]['tier']='T3'
        for v in r['content']['fact_boundary'].values():v['confidence']='SINGLE_SOURCE'
        for f in r['content']['facts']:f['confidence']='SINGLE_SOURCE'
        for c in r['content']['source_checks']:
            c['official_source']=next(e['tier'] for e in ev if e['source_id']==c['source_id'])=='T1'
        with self.assertRaisesRegex(GateError,'CORE_SPEC_SOURCE_TIER'):check_research(r,topic,ev)

    def test_regulatory_classification_cannot_hide_in_editorial_method(self):
        from cloud_pilot.multilingual.research_contract import standard_gate
        for claim in ('(EU) 2018/858 approval is mandatory','UN R100 applies','GB/T 7258 applies','ISO 9001 certification'):
            f=dict(statement=claim,kind='editorial_method',standard_related=False,standard_assessment='NOT_REGULATORY')
            with self.subTest(claim=claim),self.assertRaisesRegex(GateError,'STANDARD_CLASSIFICATION'):standard_gate(f,{})
        with self.assertRaisesRegex(GateError,'UNCERTAIN'):
            standard_gate(dict(statement='Unresolved applicability',standard_assessment='UNCERTAIN'),{})

    def test_durable_writing_lock_detects_research_update_in_scoped_journal(self):
        from cloud_pilot.multilingual.editorial_state import EditorialState
        from cloud_pilot.multilingual.tests.test_multilingual import ArtifactStore
        from cloud_pilot.multilingual.accounting import ResponseJournal
        from cloud_pilot.multilingual.startup import EpochJournal
        j=EpochJournal(ResponseJournal(ArtifactStore()),1,{'test':'lock'})
        state=EditorialState(j);r=dict(article_id='PILOT-TEST',version=1,research_hash='first',fact_sheet={'handoff':{}})
        state.lock(r);state.check(r)
        changed=copy.deepcopy(r);changed.update(version=2,research_hash='second')
        EditorialState(j).register(changed)
        with self.assertRaisesRegex(GateError,'RESEARCH_CHANGED_AFTER_WRITING_STARTED'):state.check(r)
        self.assertTrue(state.rows('update-required:PILOT-TEST:'))
    def test_forbidden_handoff_fact_stops_both_active_writing_transitions(self):
        for kind in ('VEHICLE_RECOMMENDATION','BUYING_GUIDE'):
            topic,ev,r=active_case(kind);packet=check_research(r,topic,ev)
            packet['fact_sheet']['handoff']['facts_not_allowed_in_body'].append('F0')
            with self.subTest(kind=kind),self.assertRaisesRegex(GateError,'FORBIDDEN_FACT_ALLOWED'):
                writing_request(packet,1)

    def test_identity_rejects_generic_fact_and_family_or_other_trim_scope(self):
        topic,ev,r=active_case('VEHICLE_RECOMMENDATION')
        r['content']['fact_boundary']['model']['fact_ids']=['F0']
        with self.assertRaisesRegex(GateError,'IDENTITY_DIRECT_VALUE'):check_research(r,topic,ev)
        for field,value in [('trim','FAMILY_OR_METHOD_ONLY'),('market','OTHER'),('model_year','2024')]:
            topic,ev,r=active_case('VEHICLE_RECOMMENDATION')
            r['content']['facts'][-1]['scope']=dict(r['content']['facts'][-1]['scope'],**{field:value})
            with self.subTest(field=field),self.assertRaisesRegex(GateError,'SCOPE_DRIFT|IDENTITY_DIRECT_VALUE'):
                check_research(r,topic,ev)

    def test_alternate_regulation_citations_and_unrelated_primary_source_fail(self):
        from cloud_pilot.multilingual.research_contract import standard_gate
        for kind in ('VEHICLE_RECOMMENDATION','BUYING_GUIDE'):
            topic,ev,r=active_case(kind);sources={e['source_id']:e for e in ev}
            for citation in ('Regulation (EU) 2018/858','GB 7258 mandatory vehicle standard'):
                f=copy.deepcopy(r['content']['facts'][0]);f['statement']=citation
                with self.subTest(kind=kind,citation=citation),self.assertRaisesRegex(GateError,'STANDARD_CLASSIFICATION'):
                    standard_gate(f,sources)
            f.update(standard_related=True,standard_assessment='REGULATORY_OR_STANDARD',current_version='2018',current_amendment='none',effective_date='2020-01-01',mandatory_from='2021-01-01',primary_source_url='https://unrelated.invalid/standard')
            with self.assertRaisesRegex(GateError,'DIRECT_PRIMARY_SOURCE'):standard_gate(f,sources)

    def test_descendant_checkout_is_not_the_current_main_startup_gate(self):
        from cloud_pilot.multilingual.startup import verify
        with patch('cloud_pilot.multilingual.startup.subprocess.run') as run,patch('cloud_pilot.multilingual.startup.git',side_effect=['','','','descendant','main']) as git:
            run.return_value.returncode=0
            with self.assertRaisesRegex(GateError,'PRE_RESEARCH_SYNC_FAIL'):verify('main',{})
            self.assertEqual(('pull','--ff-only','origin','main'),git.call_args_list[2].args)

    def test_active_standard_classification_requires_current_fields_for_both_article_types(self):
        for kind in ('VEHICLE_RECOMMENDATION','BUYING_GUIDE'):
            topic,ev,r=active_case(kind);r['content']['facts'][0]['standard_related']=True
            r['content']['facts'][0]['standard_assessment']='REGULATORY_OR_STANDARD'
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

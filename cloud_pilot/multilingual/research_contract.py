"""Complete identity and versioned factual handoff for the two real article types."""
import re
from ..contract import require,BASELINE,digest

IDENTITY=('brand','model','model_year','generation','body_style','powertrain','drivetrain',
          'original_sales_market','production_boundary','trim_variant')
CHECKS=('identity_complete','facts_directly_supported','scope_locked','conflicts_blocked',
        'currentness_bounded','buyer_task_answerable','source_log_accurate','skill_impact_assessed')

def applies(topic):return topic.get('content_type') in ('VEHICLE_RECOMMENDATION','BUYING_GUIDE')

def extend_request(payload):
    topic=payload['topic']
    if not applies(topic):return payload
    payload['required_output'].update(
        fact_boundary='vehicle: object with '+', '.join(IDENTITY)+'; each value is {value,confidence,source_ids,fact_ids}; fact_ids must identify allowed external facts directly supporting this exact value; guide: {scope,excluded_claims}',
        handoff='object {article_id,content_type,search_intent,buyer_task,research_baseline_sha,fact_sheet_version:1,source_log_version:1,conflict_list:[],time_sensitive_facts:[],facts_not_allowed_in_body:[],locks:[],research_locked:false,writing_locked:false,fact_update_required:false,skill_impact:{research,writing,lessons,update_required,reason},review_handoff_assessment:[{path,applicable:boolean,reason,superseded_by:null|path}]}')
    payload['required_output']['facts']='list of {id,statement,kind:external_fact|editorial_method,standard_related:boolean,quantitative:boolean,confidence,scope,source_ids,quotes:[{source_id,quote}],checked_date,buyer_applicability}; quantitative facts additionally require value and unit; standard_related facts require current_version,current_amendment,effective_date,mandatory_from,primary_source_url'
    payload['instruction']+=' Lock all required identity fields. Never call a media alias an OEM-proven export equivalent. Unknown production end/current stock may remain explicitly UNVERIFIED and blocked under RESEARCH_CONDITIONAL; core model, year, market, trim, body style, powertrain and drivetrain must be established. Editorial procurement recommendations are methods, not government or manufacturer requirements. Assess Skill impact; do not invent a negative assessment. All facts not allowed in the body and conflicts must be listed in the handoff.'
    return payload

def impact_check(impact):
    require(all(type(impact.get(k)) is bool for k in ('research','writing','lessons','update_required'))
            and isinstance(impact.get('reason'),str) and impact['reason'].strip(),'SKILL_IMPACT_ASSESSMENT_REQUIRED')
    require(impact['update_required'] is False,'SKILL_UPDATE_REQUIRED_BEFORE_WRITING')

def handoff_assessment(rows):
    from .startup import review_context
    paths=set(review_context(all_versions=True))
    require(isinstance(rows,list) and len(rows)==len(paths) and {x.get('path') for x in rows}==paths,
            'REVIEW_HANDOFF_CLASSIFICATION_COVERAGE')
    for row in rows:
        require(type(row.get('applicable')) is bool and row.get('reason') and
                (row.get('superseded_by') is None or row['superseded_by'] in paths),
                'REVIEW_HANDOFF_CLASSIFICATION_REQUIRED')

def unlocked(h):
    require(all(h.get(k) is False for k in ('research_locked','writing_locked','fact_update_required'))
            and h.get('locks')==[], 'ARTICLE_STATUS_LOCK')

def validate(r,topic,evidence):
    if not applies(topic):return
    h=r['handoff'];sources={e['source_id']:e for e in evidence}
    for k in ('article_id','content_type','search_intent','buyer_task'):require(h.get(k)==topic[k],'RESEARCH_HANDOFF_TOPIC_DRIFT')
    require(h.get('research_baseline_sha')==BASELINE and h.get('fact_sheet_version')==1
            and h.get('source_log_version')==1,'RESEARCH_HANDOFF_VERSION')
    for k in ('conflict_list','time_sensitive_facts','facts_not_allowed_in_body','locks'):
        require(isinstance(h.get(k),list),'RESEARCH_HANDOFF_MISSING:'+k)
    impact_check(h.get('skill_impact',{}));unlocked(h)
    handoff_assessment(h.get('review_handoff_assessment'))
    facts={f['id']:f for f in r['facts']};allowed=set(r['allowed_facts'])
    boundary=r['fact_boundary']
    if topic['content_type']=='VEHICLE_RECOMMENDATION':
        require(set(boundary)==set(IDENTITY),'VEHICLE_IDENTITY_INCOMPLETE')
        for k,v in boundary.items():
            require(v.get('value') and isinstance(v.get('source_ids'),list),'VEHICLE_IDENTITY_EMPTY:'+k)
            require(set(v['source_ids'])<=sources.keys(),'VEHICLE_IDENTITY_UNKNOWN_SOURCE')
            if k=='production_boundary' and v.get('confidence')=='UNVERIFIED':
                require(r['status']=='RESEARCH_CONDITIONAL' and r['blocked_facts'],'PRODUCTION_BOUNDARY_MUST_BE_BLOCKED')
            else:
                require(v.get('confidence') in ('VERIFIED','CROSS_CHECKED','SINGLE_SOURCE','TIME_SENSITIVE') and v['source_ids'],'CORE_IDENTITY_UNRESOLVED:'+k)
                ids=v.get('fact_ids',[])
                require(ids and set(ids)<=allowed,'IDENTITY_ALLOWED_FACT_SUPPORT:'+k)
                support=[facts[f] for f in ids]
                require(all(f.get('kind')=='external_fact' and str(v['value']).casefold() in f['statement'].casefold()
                            and f['confidence']==v['confidence'] for f in support),'IDENTITY_DIRECT_VALUE_SUPPORT:'+k)
                require(set(v['source_ids'])=={s for f in support for s in f['source_ids']},'IDENTITY_SOURCE_BINDING:'+k)
                for f in support:
                    for sid in f['source_ids']:
                        e=sources[sid]
                        require(f['scope']==e['scope'] and any(q['source_id']==sid and q['quote'] in e['text']
                                  for q in f['quotes']),'IDENTITY_SCOPED_QUOTE:'+k)
                if v['confidence']=='VERIFIED':require(any(sources[s]['tier']=='T1' for s in v['source_ids']),'IDENTITY_PRIMARY_AUTHORITY')
                if v['confidence']=='CROSS_CHECKED':require(len({sources[s]['parent_org'] for s in v['source_ids']})>=2,'IDENTITY_INDEPENDENT_SOURCES')
    else:require(boundary.get('scope') and isinstance(boundary.get('excluded_claims'),list),'GUIDE_SCOPE_BOUNDARY')
    allowed=set(r['allowed_facts']);blocked=set(r['blocked_facts'])
    require(set(h['facts_not_allowed_in_body'])>=blocked,'BLOCKED_HANDOFF_INCOMPLETE')
    for f in r['facts']:
        if f['id'] not in allowed:continue
        require(f.get('kind') in ('external_fact','editorial_method') and f.get('checked_date')
                and f.get('buyer_applicability'),'FACT_PROVENANCE_OR_APPLICABILITY_MISSING')
        require(type(f.get('standard_related')) is bool and type(f.get('quantitative')) is bool,
                'FACT_CLASSIFICATION_REQUIRED')
        numeric=bool(re.search(r'\d',f['statement']))
        if f['quantitative'] or numeric:
            require(f['quantitative'] is True and f.get('value') is not None and f.get('value')!=''
                    and isinstance(f.get('unit'),str) and f['unit'].strip(),'QUANTITATIVE_VALUE_UNIT_REQUIRED')
            if f['kind']=='external_fact':
                numbers=lambda text:set(re.findall(r'\b\d+(?:\.\d+)?\b',str(text)))
                quoted=' '.join(q['quote'] for q in f['quotes'])
                require(numbers(f['value'])|numbers(f['statement'])<=numbers(quoted),'QUANTITATIVE_DIRECT_QUOTE_REQUIRED')
        standard=bool(re.search(r'\b(?:ISO|IMDG|UNECE|GSO|GB/T|QC/T|EU Regulation)\b|认证标准|海关规则',f['statement'],re.I))
        require(not standard or f['standard_related'],'STANDARD_CLASSIFICATION_REQUIRED')
        if f.get('confidence')=='TIME_SENSITIVE':require(f['id'] in h['time_sensitive_facts'],'TIME_SENSITIVE_HANDOFF_MISSING')
    require(not allowed.intersection(h['conflict_list']),'CONFLICT_ALLOWED_IN_BODY')

def request(packet):
    return dict(stage='independent_research_review',research=packet,
        required_output=dict(research_hash=packet['research_hash'],decision='ACCEPT | NEEDS_RESEARCH',
            checks={k:'boolean' for k in CHECKS},findings='list of concrete factual deficiencies',
            human_reviewed=False,publish_approved=False),
        instruction='Independently read every source text, each allowed fact and the full identity/handoff. A literal quote match does not prove entailment. ACCEPT only if every allowed external fact is directly supported at its exact scope, editorial methods are distinguished from external requirements, core identity is established, current stock/export equivalence is not inferred, and the buyer task is answerable without blocked facts. Unknown production end/current stock can remain a clearly blocked conditional boundary if the exact reference identity is established. Do not invent an editorial rule or human/publication approval.')

def accept(result,packet):
    r=result['content']
    require(r.get('research_hash')==packet['research_hash'] and r.get('human_reviewed') is False
            and r.get('publish_approved') is False,'RESEARCH_REVIEW_BINDING')
    require(r.get('decision')=='ACCEPT' and set(r.get('checks',{}))==set(CHECKS)
            and all(v is True for v in r['checks'].values()) and r.get('findings')==[],
            'INDEPENDENT_RESEARCH_REVIEW_REQUIRES_RESEARCH')
    return dict(response_id=result['response_id'],research_hash=packet['research_hash'],verdict=r)

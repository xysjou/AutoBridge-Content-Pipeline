"""Complete canonical Research records, including incomplete and withheld work."""
import copy
from ..contract import require
from .research_contract import IDENTITY

REQUIRED={'status','writing_ai_ready','source_checks','facts','allowed_facts','blocked_facts',
          'fact_boundary','handoff','human_reviewed','publish_approved'}

def verdict_shape(r,topic,evidence,version):
    require(set(r)==REQUIRED,'RESEARCH_OUTPUT_FIELDS')
    require(r['status'] in ('RESEARCH_PASS','RESEARCH_CONDITIONAL','RESEARCH_FAIL')
            and type(r['writing_ai_ready']) is bool,'RESEARCH_STATUS')
    require(r['human_reviewed'] is False and r['publish_approved'] is False,'RESEARCH_APPROVAL_FORBIDDEN')
    require(all(isinstance(r[k],list) for k in ('source_checks','facts','allowed_facts','blocked_facts'))
            and isinstance(r['fact_boundary'],dict) and isinstance(r['handoff'],dict),'RESEARCH_RECORD_TYPES')
    h=r['handoff']
    require(all(h.get(k)==topic[k] for k in ('article_id','content_type','search_intent','buyer_task'))
            and h.get('research_baseline_sha')==topic['research_baseline_sha']
            and h.get('fact_sheet_version')==h.get('source_log_version')==version,'RESEARCH_HANDOFF_VERSION')
    require(all(isinstance(h.get(k),list) for k in ('conflict_list','time_sensitive_facts','facts_not_allowed_in_body','locks')),'RESEARCH_HANDOFF_MISSING')
    require(set(r['blocked_facts'])<=set(h['facts_not_allowed_in_body']) and
            not set(r['allowed_facts'])&set(r['blocked_facts']),'FACT_ALLOWLIST')
    require({c.get('source_id') for c in r['source_checks']}=={e['source_id'] for e in evidence},'SOURCE_CHECK_COVERAGE')
    if r['status']=='RESEARCH_FAIL':require(r['writing_ai_ready'] is False,'RESEARCH_FAIL_CANNOT_BE_READY')
    if r['status']=='RESEARCH_CONDITIONAL':require(r['blocked_facts'],'CONDITIONAL_BLOCKLIST_REQUIRED')
    if r['status']=='RESEARCH_PASS':require(r['writing_ai_ready'] is True,'PASS_WITHOUT_READINESS')

def complete_records(raw,path):
    """Derive declared fields from the packet; never invent missing evidence."""
    sheet=copy.deepcopy(raw['fact_sheet']);topic=raw['topic'];h=sheet.get('handoff',{})
    accepted=raw.get('research_phase')=='ACCEPTED';facts=sheet.get('facts',[])
    if accepted:require(all(e.get('source_title') for e in raw['evidence']),'CANONICAL_SOURCE_TITLE_REQUIRED')
    checks={c['source_id']:c for c in sheet.get('source_checks',[]) if isinstance(c,dict) and c.get('source_id')}
    allowed=sheet.get('allowed_facts',[]);blocked=sheet.get('blocked_facts',[])
    logs=[]
    for e in raw['evidence']:
        sid=e['source_id'];supported=[f for f in facts if sid in f.get('source_ids',[])]
        scope=e['scope'];c=checks.get(sid,{})
        logs.append(dict(SOURCE_ID=sid,SOURCE_TITLE=e.get('source_title','NOT_CAPTURED'),
            SOURCE_ORGANIZATION=e['publisher'],SOURCE_ORG_RAW=e['publisher'],SOURCE_PARENT_ORG=e['parent_org'],
            SOURCE_ORG_NORMALIZED=e['parent_org'],SOURCE_URL=e['requested_url'],SOURCE_TIER=e['tier'],
            SOURCE_MARKET=scope['market'],SOURCE_SCOPE=scope,SUPPORTED_FACT=[dict(id=f['id'],statement=f['statement']) for f in supported],
            MODEL_YEAR=scope['model_year'],VERSION_TRIM=scope['trim'],POWERTRAIN=scope['powertrain'],
            TEST_CYCLE=scope['test_cycle'],CHECKED_DATE=e['retrieved_at'],ACCESS_STATUS=e.get('status','UNKNOWN'),
            CONFIDENCE={f['id']:f.get('confidence','UNVERIFIED') for f in supported},
            support_review_status='ACCEPTED' if accepted else 'PROPOSED_OR_INCOMPLETE',
            official_source=c.get('official_source',False),scope_match=c.get('scope_status','NOT_REVIEWED'),
            raw_artifact_path=e.get('raw_artifact_path'),raw_sha256=e.get('raw_sha256'),
            text_sha256=e.get('text_sha256'),raw_evidence=e))
    identities=sheet.get('fact_boundary',{}) if topic['content_type']=='VEHICLE_RECOMMENDATION' else {}
    official=sum(e['tier']=='T1' and checks.get(e['source_id'],{}).get('scope_status')=='MATCHED' for e in raw['evidence'])
    handoff=dict(h,BATCH_ID='api-pilot-2026-11-03',ARTICLE_ID=raw['article_id'],TITLE=topic['search_intent'],
        CONTENT_TYPE=topic['content_type'],SEARCH_INTENT=topic['search_intent'],BUYER_TASK=topic['buyer_task'],
        SOURCE_URL_COUNT=len(logs),SOURCE_ORG_COUNT=len({e['parent_org'] for e in raw['evidence']}),
        SOURCE_ORG_COUNT_NORMALIZED=len({e['parent_org'] for e in raw['evidence']}),
        SOURCE_SCOPE_STATUS={sid:c.get('scope_status','NOT_REVIEWED') for sid,c in checks.items()},
        OFFICIAL_SOURCE_COUNT=official,OFFICIAL_SOURCE_STATUS='MATCHED_PRIMARY_CAPTURED' if official else 'NO_MATCHED_PRIMARY_CAPTURED',
        FACT_BOUNDARY_STATUS='INDEPENDENTLY_ACCEPTED' if accepted else 'NOT_LOCKED_FOR_WRITING',
        FACTS_ALLOWED_IN_BODY=allowed if accepted else [],PROPOSED_FACTS_ALLOWED_IN_BODY=allowed,
        FACTS_NOT_ALLOWED_IN_BODY=h.get('facts_not_allowed_in_body',blocked),BLOCKED_FACTS=blocked,
        CONFIDENCE_STATUS={f['id']:f.get('confidence','UNVERIFIED') for f in facts},
        TIME_SENSITIVE_FACTS=h.get('time_sensitive_facts',[]),CONFLICT_LIST=h.get('conflict_list',[]),
        REPRESENTATIVE_COUNTRIES='N/A_NON_REGIONAL_BUYER_TASK',RESEARCH_STATUS=sheet['status'],WRITING_AI_READY=accepted,
        FACT_SHEET_VERSION=raw['version'],SOURCE_LOG_VERSION=raw['version'],
        FACT_SHEET_PATH=path+'FACT_SHEET.json',SOURCE_LOG_PATH=path+'SOURCE_LOG.json',
        RESEARCH_START_SHA=topic['research_baseline_sha'],RESEARCH_BASELINE_SHA=topic['research_baseline_sha'],
        RESEARCH_COMPLETE_COMMIT_SHA='RECORDED_IN_PUSH_COMPLETION_RECEIPT',
        CONTROLLED_RESEARCH_PATCH_REQUIRED=False,IMAGE_RESEARCH_STATUS='NO_IMAGE_SUPPLIED_RIGHTS_NOT_CLEARED',
        COUNT_SCOPE='THIS_PACKAGE_ONLY',TOTAL_MAIN=1,TOTAL_RESERVE=0,
        PASS_COUNT=int(accepted and sheet['status']=='RESEARCH_PASS'),
        CONDITIONAL_COUNT=int(sheet['status']=='RESEARCH_CONDITIONAL'),FAIL_COUNT=int(sheet['status']=='RESEARCH_FAIL'),
        OFFICIAL_SOURCE_REQUIRED=False,OFFICIAL_SOURCE_FOUND=official>0,
        PUBLISH_APPROVED=False,HUMAN_REVIEWED=False)
    for k in IDENTITY:handoff[k.upper()]=identities.get(k,'N/A_NON_VEHICLE' if not identities else 'NOT_LOCKED_IN_FACT_SHEET')
    sheet.update(ARTICLE_ID=raw['article_id'],TITLE=topic['search_intent'],CONTENT_TYPE=topic['content_type'],
        SEARCH_INTENT=topic['search_intent'],BUYER_TASK=topic['buyer_task'],FACT_BOUNDARY=sheet.get('fact_boundary',{}),
        FACTS=facts,FACTS_ALLOWED_IN_BODY=handoff['FACTS_ALLOWED_IN_BODY'],FACTS_NOT_ALLOWED_IN_BODY=handoff['FACTS_NOT_ALLOWED_IN_BODY'],
        BLOCKED_FACTS=blocked,CONFLICT_LIST=handoff['CONFLICT_LIST'],TIME_SENSITIVE_FACTS=handoff['TIME_SENSITIVE_FACTS'],
        REPRESENTATIVE_COUNTRIES=handoff['REPRESENTATIVE_COUNTRIES'],SOURCE_SCOPE_STATUS=handoff['SOURCE_SCOPE_STATUS'],
        IMAGE_RESEARCH_STATUS=handoff['IMAGE_RESEARCH_STATUS'],RESEARCH_STATUS=sheet['status'],WRITING_AI_READY=accepted)
    return sheet,logs,handoff

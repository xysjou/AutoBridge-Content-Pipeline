"""Explicit JSON handoffs for real Research, Writing, independent Review."""
import re
from datetime import datetime
from urllib.parse import urlsplit
from ..contract import BASELINE, PROGRAM, digest, require, rules
from ..review import similarity
from .policy import SCHEMA, now

SCOPE=('market','model_year','generation','trim','powertrain','test_cycle')
LEAK=re.compile(r'Research AI|Writing AI|Review AI|Codex|QA_PASS|PUBLISH_APPROVED|FACT_SOURCE_PASS|Freeze the scope|Build a primary-evidence ledger',re.I)

def validate_plan(plan,history):
    require(plan.get('schema')==SCHEMA and plan.get('program_id')==PROGRAM,'PLAN_SCHEMA')
    require(plan.get('baseline_sha')==BASELINE and plan.get('rules')==rules(),'PLAN_BASELINE_OR_RULE_DRIFT')
    require(plan.get('history_hash')==digest(history),'HISTORY_CHANGED')
    require(plan.get('semantic_dedup_status')=='INDEPENDENTLY_CONFIRMED','SEMANTIC_DEDUP_PENDING')
    require(len(plan.get('articles',[]))==2,'EXACTLY_TWO_EN_ARTICLES')
    seen_ids,seen_intents,seen_urls=set(),set(),set()
    for a in plan['articles']:
        require(re.fullmatch(r'PILOT-[A-Z0-9-]+',a['article_id']),'PILOT_ARTICLE_ID')
        require(a.get('locale')=='en' and a.get('version')==1,'EN_INITIAL_VERSION_ONLY')
        require(a.get('search_intent') and a.get('buyer_task') and a.get('topic_key'),'MISSING_BUYER_TASK')
        require(a['proposed_url'].startswith('/pilot-only/'),'NO_PRODUCTION_URL_ASSIGNMENT')
        intent=' '.join(a['search_intent'].casefold().split())
        require(a['article_id'] not in seen_ids and intent not in seen_intents and a['proposed_url'] not in seen_urls,'PILOT_DUPLICATE')
        seen_ids.add(a['article_id']);seen_intents.add(intent);seen_urls.add(a['proposed_url'])
        for entry in history['entries']:
            require(entry.get('article_id')!=a['article_id'],'HISTORY_ARTICLE_DUPLICATE')
            require(entry.get('url')!=a['proposed_url'],'HISTORY_URL_DUPLICATE')
            require(entry.get('topic_key')!=a['topic_key'],'HISTORY_TOPIC_DUPLICATE')
            require(' '.join(str(entry.get('search_intent','')).casefold().split())!=intent,'HISTORY_INTENT_DUPLICATE')
        sources=a['sources']
        require(6<=len(sources)<=12 and len({s['source_id'] for s in sources})==len(sources),'SOURCE_COUNT_OR_IDS')
        require(len({s['parent_org'] for s in sources})>=4,'NORMALIZED_ORG_COUNT')
        require(len({s['url'] for s in sources})==len(sources),'DUPLICATE_SOURCE_URL')
        for s in sources:
            require(s['tier'] in ('T1','T2','T3') and s['publisher'] and s['parent_org'],'SOURCE_IDENTITY')
            require(all(s['scope'].get(k) for k in SCOPE),'SOURCE_SCOPE_UNLOCKED')
            p=urlsplit(s['url']);require(p.scheme=='https' and p.hostname,'SOURCE_URL')
    return True

def research_request(topic,evidence):
    from ..multilingual.research_contract import extend_request
    return extend_request(dict(stage='research',schema=SCHEMA,topic=topic,evidence=evidence,
        required_output=dict(status='RESEARCH_PASS | RESEARCH_CONDITIONAL | RESEARCH_FAIL',
            writing_ai_ready='boolean',source_checks='one {source_id,publisher_match,scope_match} for every evidence item',
            facts='list of {id,statement,confidence,scope,source_ids,quotes:[{source_id,quote}]}',
            allowed_facts='list of fact IDs',blocked_facts='list of blocked fact IDs',
            human_reviewed=False,publish_approved=False),
        instruction='Quotes must be literal substrings of evidence text. T1+MATCHED alone may be VERIFIED. Apply all canonical rules, including current standard, importer/vehicle scope, exception and currentness rules. Core unknowns must stop writing.'))

def check_research(result,topic,evidence):
    from ..multilingual.startup import skill_provenance
    r=result['content']
    from ..multilingual.research_contract import applies,validate as validate_handoff
    fields={'status','writing_ai_ready','source_checks','facts','allowed_facts','blocked_facts','human_reviewed','publish_approved'}
    if applies(topic):fields.update(('fact_boundary','handoff'))
    require(set(r)==fields,'RESEARCH_OUTPUT_FIELDS')
    require(r.get('human_reviewed') is False and r.get('publish_approved') is False,'RESEARCH_APPROVAL_FORBIDDEN')
    require(r.get('status') in ('RESEARCH_PASS','RESEARCH_CONDITIONAL','RESEARCH_FAIL'),'RESEARCH_STATUS')
    require(r['status']!='RESEARCH_FAIL' and r.get('writing_ai_ready') is True,'RESEARCH_STOPS_WRITING')
    source={e['source_id']:e for e in evidence}
    checks={c['source_id']:c for c in r['source_checks']}
    require(checks.keys()==source.keys(),'SOURCE_CHECK_COVERAGE')
    require(all(c['publisher_match'] is True and c['scope_match'] is True for c in checks.values()),'SOURCE_IDENTITY_OR_SCOPE_FAIL')
    facts={f['id']:f for f in r['facts']}
    require(len(facts)==len(r['facts']),'FACT_ID_DUPLICATE')
    allowed=set(r['allowed_facts']);blocked=set(r['blocked_facts'])
    require(allowed and allowed<=facts.keys() and not allowed&blocked,'FACT_ALLOWLIST')
    used=set()
    for fid in allowed:
        f=facts[fid]
        require(f['confidence'] in ('VERIFIED','CROSS_CHECKED','SINGLE_SOURCE','TIME_SENSITIVE'),'UNUSABLE_CONFIDENCE')
        require(f['statement'] and f['source_ids'] and f['quotes'],'EMPTY_FACT_SUPPORT')
        require({q['source_id'] for q in f['quotes']}==set(f['source_ids']),'QUOTE_BINDING')
        for q in f['quotes']:
            require(q['source_id'] in source and len(q['quote'])>=12,'QUOTE_SOURCE')
            e=source[q['source_id']]
            require(q['quote'] in e['text'],'QUOTE_NOT_IN_RETRIEVED_SOURCE')
            require(all(f['scope'].get(k)==e['scope'].get(k) for k in SCOPE),'FACT_SCOPE_DRIFT')
            used.add(q['source_id'])
        if f['confidence']=='VERIFIED':require(any(source[s]['tier']=='T1' for s in f['source_ids']),'T1_REQUIRED_FOR_VERIFIED')
        if f['confidence']=='CROSS_CHECKED':require(len({source[s]['parent_org'] for s in f['source_ids']})>=2,'CROSS_CHECK_INDEPENDENCE')
        if f['confidence']=='TIME_SENSITIVE':require(f.get('current_applicability_verified') is True,'CURRENTNESS_UNVERIFIED')
        if f.get('kind')=='standard' or f.get('standard_related') is True:
            from ..multilingual.research_contract import standard_gate
            standard_gate(f,source)
    require(used==source.keys(),'SOURCE_PADDING_OR_INCOMPLETE_BINDING')
    if r['status']=='RESEARCH_CONDITIONAL':require(blocked,'CONDITIONAL_BLOCKLIST_REQUIRED')
    validate_handoff(r,topic,evidence)
    packet=dict(schema=SCHEMA,program_id=PROGRAM,article_id=topic['article_id'],version=1,
        baseline_sha=BASELINE,rules=rules(),researcher_id='research:'+result['response_id'],
        evidence_hash=digest(evidence),evidence=evidence,fact_sheet=r,topic=topic,
        human_reviewed=False,publish_approved=False)
    provenance=skill_provenance('research')
    packet.update(research_skill_version_used=provenance['version'],research_skill_commit_sha_used=provenance['commit'],
                  skill_provenance=provenance,skill_impact_check_done=applies(topic),
                  skill_update_required=r.get('handoff',{}).get('skill_impact',{}).get('update_required',False))
    packet['research_hash']=digest(packet)
    return packet

def writing_request(research,version,prior=None,findings=None):
    from ..multilingual.research_contract import applies,ready
    ready(research)
    result=dict(stage='writing',schema=SCHEMA,version=version,research=research,
        prior_article=prior,independent_revision_findings=findings,
        required_output=dict(title='plain English value',meta='plain English value',h1='plain English value',summary='plain English value',
            sections='list of {text,claim_ids:[allowed fact IDs]}',faq='list of {question,answer,claim_ids}',
            internal_links='list of verified relative URLs or empty',human_reviewed=False,publish_approved=False),
        instruction='Write at least 900 English words, natural article-specific prose, evidence-bound claims and restrained uncertainty. Do not include self-evaluation or internal workflow terms. Never invent images or source URLs. Follow the canonical Writing Skill in full.')
    if applies(research['topic']):
        result['required_output'].update(skill_impact='internal object {research,writing,lessons,update_required,reason}',
            review_handoff_assessment='internal list classifying every supplied handoff {path,applicable:boolean,reason,superseded_by:null|path}')
    return result

def check_writing(result,research,version,history,prior_bodies):
    from ..multilingual.startup import skill_provenance
    provenance=skill_provenance('writing')
    a=result['content']
    from ..multilingual.research_contract import applies,impact_check,handoff_assessment,ready
    fields={'title','meta','h1','summary','sections','faq','internal_links','human_reviewed','publish_approved'}
    impact=None;assessment=None
    if applies(research['topic']):
        fields.update(('skill_impact','review_handoff_assessment'));ready(research)
        impact=a.get('skill_impact',{});impact_check(impact)
        assessment=a.get('review_handoff_assessment');handoff_assessment(assessment)
    require(set(a)==fields,'WRITER_FIELDS_OR_SELF_EVALUATION')
    a={k:v for k,v in a.items() if k not in ('skill_impact','review_handoff_assessment')}
    require(a['human_reviewed'] is False and a['publish_approved'] is False,'WRITER_APPROVAL_FORBIDDEN')
    allowed=set(research['fact_sheet']['allowed_facts'])
    for value in [a['title'],a['meta'],a['h1'],a['summary']]:
        require(isinstance(value,str) and value.strip() and not re.search(r'\*\*|<|>|^\s*(ALT|Meta Description|H1|Title)\s*:',value,re.I),'PUBLIC_FIELD_PURITY')
    require(a['sections'],'EMPTY_ARTICLE')
    for s in a['sections']+a['faq']:
        require(s['claim_ids'] and set(s['claim_ids'])<=allowed,'WRITER_BLOCKED_OR_UNKNOWN_CLAIM')
    require(all(set(s)=={'text','claim_ids'} for s in a['sections']) and all(set(f)=={'question','answer','claim_ids'} for f in a['faq']),'PUBLIC_SECTION_FIELDS')
    body='\n\n'.join(s['text'] for s in a['sections'])
    body+='\n\n'+'\n\n'.join(f['question']+'\n'+f['answer'] for f in a['faq'])
    require(len(re.findall(r"\b[A-Za-z]+(?:['-][A-Za-z]+)*\b",body))>=900,'ENGLISH_BELOW_900_WORDS')
    require(not re.search(r'^#\s',body,re.M),'BODY_DUPLICATES_H1_FIELD')
    require(not LEAK.search(body+' '+a['title']+' '+a['summary']),'PUBLIC_WORKFLOW_LEAKAGE')
    require(not re.search(r'\bwe (tested|drove|inspected|imported)\b',body,re.I),'UNPROVEN_FIRST_HAND')
    numeric_reference=' '.join(f['statement']+' '+str(f['scope']) for f in research['fact_sheet']['facts'] if f['id'] in allowed)
    numbers=lambda text:set(re.findall(r'\b\d+(?:\.\d+)?\b',text))
    require(numbers(body+' '+a['title']+' '+a['meta']+' '+a['summary'])<=numbers(numeric_reference),'UNSUPPORTED_NUMERIC_CLAIM')
    urls={e.get('url') for e in history['entries']}
    require(all(u in urls and u.startswith('/') for u in a['internal_links']),'UNKNOWN_INTERNAL_LINK')
    maximum=max((similarity(body,b) for b in prior_bodies),default=0)
    require(maximum<.70,'FULL_BODY_SIMILARITY_FAIL')
    packet=dict(schema=SCHEMA,program_id=PROGRAM,article_id=research['article_id'],version=version,locale='en',
        baseline_sha=BASELINE,rules=rules(),research_hash=research['research_hash'],
        research_baseline_sha=research['fact_sheet'].get('handoff',{}).get('research_baseline_sha'),
        evidence_hash=research['evidence_hash'],writer_id='writer:'+result['response_id'],
        author='AutoBridge Export Editorial Team',ai_assisted=True,evidence=dict(first_hand=False),
        writing_skill_version_used=provenance['version'],writing_skill_commit_sha_used=provenance['commit'],
        skill_provenance=provenance,skill_impact_check_done=impact is not None,
        skill_impact_assessment=impact,review_handoff_assessment=assessment,
        skill_update_required=impact['update_required'] if impact else None,
        public=a,body=body,similarity_max=maximum,manual_similarity_review_required=maximum>.50,
        human_reviewed=False,publish_approved=False,production_eligible=False,
        production_holds=['EN_ONLY','IMAGE_RIGHTS_PENDING','HUMAN_APPROVAL_ABSENT','NO_WEBSITE_PUBLICATION_AUTHORITY'])
    packet['public_export_fields']=dict(public_title=a['title'],public_meta=a['meta'],public_h1=a['h1'],
        public_summary=a['summary'],public_body=body,public_faq=[dict(question=f['question'],answer=f['answer']) for f in a['faq']],public_image_fields=[],
        public_sources=[dict(source=e.get('requested_url',''),organization=e.get('publisher',''),
            checked_date=e['retrieved_at'],market=e['scope']['market']) for e in research['evidence']])
    packet['content_hash']=digest(packet)
    return packet

REVIEW_CHECKS={'claim_entailment','market_year_trim_cycle','source_identity_scope','general_rule_exceptions',
               'currentness','natural_english','no_workflow_leakage','no_fabricated_first_hand','buyer_task_answered'}

def review_request(article,research):
    from ..multilingual.localize import markdown
    rendered=markdown(article,research,research['topic'],public_only=True)
    return dict(stage='independent_review',schema=SCHEMA,article=article,research=research,
        rendered_public_markdown=rendered,rendered_hash=digest(rendered),
        required_output=dict(content_hash=article['content_hash'],evidence_hash=research['evidence_hash'],
            decision='REVIEW_PASS | REVISION_REQUIRED | NEEDS_RESEARCH | REJECT',
            checks={k:'boolean' for k in sorted(REVIEW_CHECKS)},findings='list of {rule_id,detail,claim_id}',
            human_reviewed=False,publish_approved=False),
        instruction='Independently compare every material statement, title, summary, FAQ and number with actual source text. Read the exact rendered public Markdown including headings and source table. Quotes are not proof of entailment by themselves. Return NEEDS_RESEARCH for core unknowns. A pass applies only to this English text draft hash; never grants 12-language/production/human approval. Internal S05 metadata labels/editorial notes are not public prose; images and production URLs remain incomplete.')

def check_review(result,article,research):
    r=result['content']
    require(set(r)=={'content_hash','evidence_hash','decision','checks','findings','human_reviewed','publish_approved'},'REVIEW_OUTPUT_FIELDS')
    require('writer:'+result['response_id']!=article['writer_id'],'WRITER_REVIEW_IDENTITY_REUSE')
    require(r.get('content_hash')==article['content_hash'] and r.get('evidence_hash')==research['evidence_hash'],'REVIEW_HASH_DRIFT')
    require(article['content_hash']==digest({k:v for k,v in article.items() if k!='content_hash'}),'ARTICLE_CHANGED_AFTER_WRITING')
    require(r.get('human_reviewed') is False and r.get('publish_approved') is False,'REVIEW_APPROVAL_FORBIDDEN')
    require(r.get('decision') in ('REVIEW_PASS','REVISION_REQUIRED','NEEDS_RESEARCH','REJECT'),'REVIEW_DECISION')
    require(set(r['checks'])==REVIEW_CHECKS and all(type(v) is bool for v in r['checks'].values()),'REVIEW_CHECK_COVERAGE')
    if r['decision']=='REVIEW_PASS':
        require(all(r['checks'].values()) and not r['findings'],'REVIEW_CONTRADICTORY_PASS')
        require(not article['manual_similarity_review_required'],'SIMILARITY_MANUAL_REVIEW_REQUIRED')
    packet=dict(schema=SCHEMA,program_id=PROGRAM,article_id=article['article_id'],version=article['version'],
        reviewer_id='reviewer:'+result['response_id'],content_hash=article['content_hash'],research_hash=research['research_hash'],
        verdict=r,review_scope='ENGLISH_DRAFT_ONLY',human_reviewed=False,publish_approved=False,production_eligible=False)
    from ..multilingual.localize import markdown
    packet['rendered_hash']=digest(markdown(article,research,research['topic'],public_only=True))
    packet['review_hash']=digest(packet)
    return packet

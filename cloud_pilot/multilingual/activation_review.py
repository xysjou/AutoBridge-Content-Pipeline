"""Independent API audit of the candidate and topic overlap before paid writing."""
import re
from pathlib import Path
from ..contract import ROOT,digest,require,file_hash

def code_paths(root=ROOT):
    # Include every transitive pilot module, not a handpicked security subset.
    return sorted(p.relative_to(root).as_posix() for p in (root/'cloud_pilot').rglob('*.py')
                  if 'tests' not in p.parts and not any(x.endswith('_tests') for x in p.parts))+[
        'cloud_pilot/runtime/multilingual-manual.yml.template',
        '.github/workflows/cloud-pilot-manual.yml',
        '.github/workflows/cloud-pilot-trusted.yml',
        'cloud_pilot/multilingual/tests/test_recovery.py',
        'cloud_pilot/multilingual/tests/test_security.py',
        'cloud_pilot/multilingual/tests/test_editorial_controls.py',
        'cloud_pilot/multilingual/tests/test_activation.py',
        'cloud_pilot/multilingual/tests/test_multilingual.py',
        'cloud_pilot/stage2_tests/test_live.py']

def intake(plan):
    # Approval state and phase do not change the actual topics/evidence/intent.
    return {k:v for k,v in plan.items() if k not in
            ('semantic_dedup_status','execution_phase','independent_review_receipt','evidence_revision')}

def intake_hash(plan):return digest(intake(plan))

def corpus(root=ROOT):
    """Current batch pointers; daily/delivery English source articles, deduped by text."""
    paths=set()
    for pointer in root.glob('batches/*/articles/*/CURRENT'):
        version=pointer.read_text().strip()
        require(re.fullmatch(r'v\d+',version),'BAD_CURRENT_POINTER')
        choices=[pointer.parent/'versions'/f'{version}.md',pointer.parent/'versions'/version/'article.md']
        found=[p for p in choices if p.is_file()]
        require(len(found)==1,'CURRENT_VERSION_AMBIGUOUS')
        paths.add(found[0])
    for folder in ('daily','deliveries'):
        for p in (root/folder).rglob('*.md'):
            rel=p.relative_to(root).as_posix()
            if '/versions/' in rel:continue
            if '/i18n/' in rel:
                if '/i18n/en/' in rel:paths.add(p)
            elif '/articles/' in rel:paths.add(p)
    reserve=root/'daily/2026-09-02/research/reserves/AB-260902-VR2_Changan_Qiyuan_Q05_2024.md'
    if reserve.is_file():paths.add(reserve)
    result=[];seen=set()
    for p in sorted(paths):
        text=p.read_text();h=digest(text)
        if h in seen:continue
        seen.add(h);rel=p.relative_to(root).as_posix()
        title=re.search(r'^#\s+(.+)',text,re.M)
        if not title:continue
        # Index is for candidate selection, not title-only final judgment.
        url=re.search(r'(?im)^[-*]\s*\*{0,2}Suggested URL\*{0,2}\s*:\s*(.+)',text)
        result.append(dict(path=rel,title=title.group(1),url=url.group(1) if url else '',
                           context_role='reserve_not_published' if '/research/reserves/' in rel else 'current_source_article',
                           text_hash=h,text=text))
    return result

def dedup_request(plan,root=ROOT):
    docs=corpus(root)
    related=[]
    for d in docs:
        t=d['text'].lower()
        q=bool(re.search(r'qiyuan\s*q05|nevo\s*q05|启源\s*q05',t))
        cold=bool(re.search(r'refrigerat|reefer|冷藏|cold[- ]chain',t))
        if q or cold:related.append(dict(d,match=('Q05' if q else '')+(' cold-chain' if cold else '')))
    # No silently omitted matching articles. If too large, stop for explicit scoping.
    require(sum(len(x['text'].encode()) for x in related)<=900000,'RELATED_CORPUS_NEEDS_SCOPING')
    index=[{k:d[k] for k in ('path','title','url','text_hash','context_role')} for d in docs]
    packet=dict(stage='independent_topic_dedup',intake_hash=intake_hash(plan),
        topics=[{k:a[k] for k in ('article_id','search_intent','buyer_task','topic_key')} for a in plan['articles']],
        corpus_index=index,related_full_text=related,
        coverage='Current batch versions plus unique English daily/delivery source articles. Localizations are represented by their English originals. No title-only pass is allowed.',
        required_output=dict(decision='PASS | OVERLAP | NEEDS_MORE_EVIDENCE',
            articles='list of {article_id,decision:DISTINCT|OVERLAP|NEEDS_MORE_EVIDENCE,nearest_paths:[existing paths],reason}',
            additional_paths='list of paths requiring full text before a pass',human_reviewed=False,publish_approved=False),
        instruction='Independently assess search intent and buyer decision, using the index AND the related full texts. '
          'Do not approve because dates, titles or brand names differ. Q05 has an older 2024 PHEV reserve: distinguish it '
          'from the 2026 BEV without assuming all Q05 pages are unique. Refrigerated-truck procurement may overlap '
          'the existing Foton Aumark buyer guide; require a distinct acceptance-evidence decision scope. '
          'Return NEEDS_MORE_EVIDENCE and additional_paths if related coverage is insufficient. Do not grant human/publication approval.')
    packet['corpus_hash']=digest(index)
    return packet

def code_request(plan,sha,root=ROOT,workflow_evidence=None,scope_attestation=None):
    from .startup import BATCH_CONTEXT
    import json
    manifest=json.loads((root/'cloud_pilot/evidence/activation/validation-manifest.json').read_text())
    require(all(file_hash(root/p)==h for p,h in manifest['source_hashes'].items()),'TESTED_SOURCE_TREE_DRIFT')
    require(set(manifest['suites'])=={'multilingual','stage2','original'} and
            all(manifest['suites'][k]>=n for k,n in {'multilingual':40,'stage2':47,'original':41}.items()),'OFFLINE_SUITE_COVERAGE')
    require(all(file_hash(root/p)==h for p,h in manifest['test_logs'].items()),'OFFLINE_TEST_LOG_DRIFT')
    if workflow_evidence:
        require(set(workflow_evidence)=={'cloud-pilot-manual.yml','cloud-pilot-trusted.yml'},'AUDIT_WORKFLOW_COVERAGE')
        for name,item in workflow_evidence.items():
            require(item['content']==(root/'.github/workflows'/name).read_text()
                    and item['content_hash']==digest(item['content']),'AUDIT_EXECUTABLE_WORKFLOW_DRIFT')
    files={p:(root/p).read_text() for p in code_paths(root)}
    files.update({p:(root/p).read_text() for p in BATCH_CONTEXT})
    files['cloud_pilot/evidence/activation/real-activation-result.json']=(root/'cloud_pilot/evidence/activation/real-activation-result.json').read_text()
    files['cloud_pilot/evidence/activation/latest-independent-review.json']=(root/'cloud_pilot/evidence/activation/latest-independent-review.json').read_text()
    for p in ('current-multilingual-tests.txt','current-stage2-tests.txt','current-m1-tests.txt'):
        files['cloud_pilot/evidence/activation/'+p]=(root/'cloud_pilot/evidence/activation'/p).read_text()
    return dict(stage='independent_candidate_code_review',code_sha=sha,plan=intake(plan),files=files,
        executed_workflows=workflow_evidence,environment_scope_attestation=scope_attestation,
        offline_validation_manifest=manifest,
        runtime_contract=dict(scope='Manual source-bound text drafts only; no website publication, image completion or human approval',
            trust_root='Operator-protected approval fingerprint plus required environment reviewer; approval binds one exact workflow run and attempt, immutable caller/reusable workflows, code/plan/rules/prices and a reconciled append-only ledger floor. Environment control commit and fingerprint are read only when the reviewed job starts.',
            recovery='Every new workflow run needs a newly reconciled protected floor and exact run lease. Completed operations are reused; sent/uncertain operations are never blindly resent. Adversarial GitHub owner/provider administrator changing protected approval is outside this owner-controlled pilot threat model.',
            accounting='Provider input-token count for the same model/input/tools/text/reasoning plus a buffer determines the input upper bound. Worst cache-write rate and max output are reserved. All historical usage remains in the same USD3 ledger; output and input bounds are checked on settlement.'),
        required_output=dict(decision='PASS | BLOCK',findings='list of {severity,file,detail,required_fix}',
                             human_reviewed=False,publish_approved=False),
        instruction='You are an independent reviewer, not the author. Scope is the active multilingual entry point and its pinned reusable workflow for owner-controlled, manual draft generation; legacy inert/mock entry points are context, not newly activated services. The root of trust is the protected operator permit fingerprint and environment reviewer, not an adversarial GitHub owner or provider administrator. Within that boundary, audit runtime/secret boundaries, immutable '
            'code and control binding, whole-program USD3 cap, exact response identity and usage, no duplicate '
            'generation on resume, independent locale review, SSRF, source failures, and truthful delivery status. '
            'Return BLOCK for a correctness or safety problem that prevents a real English pilot. '
            'Known disclosed limitations (manual source intake, no website deployment, missing image rights, '
            'conservative cap potentially stopping early) are not proof of implementation success or reason '
            'to fabricate a pass. Give concrete code-grounded findings. No approval flags may be set true.')

def verified_topic(journal,packet):
    """Reuse a genuine independent topic verdict only for the identical intake/corpus packet."""
    view=journal.read()[2]
    for key in reversed(list(view['checkpoints'])):
        if not key.startswith('activation-review:'):continue
        report=journal.get_checkpoint(key)
        if report.get('dedup_request_hash')!=digest(packet) or report.get('corpus_hash')!=packet['corpus_hash']:continue
        result=report.get('topic_review',{});d=result.get('content',{})
        if d.get('decision')!='PASS' or d.get('additional_paths')!=[] or len(d.get('articles',[]))!=2 or not all(a.get('decision')=='DISTINCT' for a in d['articles']):continue
        op='activation-dedup:'+digest(packet)
        matches=[o for o in view['operations'].values() if o['operation']==op and o['status']=='completed'
                 and o['response']['id']==result.get('response_id')]
        if len(matches)!=1:continue
        import json
        archived=journal.store.load_artifact(matches[0]['response']['text_artifact'])
        require(json.loads(archived['text'])==d,'REUSED_TOPIC_RECEIPT_CHANGED')
        return result,dict(checkpoint=key,operation=op,request_hash=matches[0]['request_hash'],
                           packet_hash=digest(packet),response_id=result['response_id'])
    return None,None

def run(plan,sha,journal,models,root=ROOT,workflow_evidence=None,scope_attestation=None):
    packet=dedup_request(plan,root) # Validate complete review inputs before the first paid request.
    require(workflow_evidence and scope_attestation,'REVIEW_EXECUTED_WORKFLOW_EVIDENCE_REQUIRED')
    code=code_request(plan,sha,root,workflow_evidence,scope_attestation)
    code_result=models.call('activation-code:'+sha,'review',code)
    c=code_result['content']
    require(c.get('human_reviewed') is False and c.get('publish_approved') is False,'AUDIT_APPROVAL_FORBIDDEN')
    require(c.get('decision') in ('PASS','BLOCK') and isinstance(c.get('findings'),list),'AUDIT_CODE_SHAPE')
    require(c['decision']!='PASS' or not any(f.get('severity') in ('critical','high','blocker') for f in c['findings']),
            'AUDIT_CONTRADICTORY_PASS')
    journal.checkpoint('activation-code-result:'+sha,code_result)
    # Both independent tasks may complete even if code is blocked. Writing stays forbidden.
    dedup,reused=verified_topic(journal,packet) if hasattr(journal,'read') else (None,None)
    if dedup is None:dedup=models.call('activation-dedup:'+digest(packet),'research',packet)
    d=dedup['content'];ids={a['article_id'] for a in plan['articles']}
    require(d.get('human_reviewed') is False and d.get('publish_approved') is False,'AUDIT_APPROVAL_FORBIDDEN')
    require(d.get('decision') in ('PASS','OVERLAP','NEEDS_MORE_EVIDENCE'),'AUDIT_DEDUP_SHAPE')
    rows=d.get('articles',[])
    require(len(rows)==2 and {a['article_id'] for a in rows}==ids,'AUDIT_DEDUP_COVERAGE')
    require(all(a['decision'] in ('DISTINCT','OVERLAP','NEEDS_MORE_EVIDENCE') for a in rows),'AUDIT_DEDUP_DECISION')
    known={a['path'] for a in packet['corpus_index']}
    require(all(set(a.get('nearest_paths',[]))<=known for a in rows),'AUDIT_UNKNOWN_ARTICLE_REFERENCE')
    passed=c['decision']=='PASS' and d['decision']=='PASS' and all(a['decision']=='DISTINCT' for a in rows) and d.get('additional_paths')==[]
    report=dict(status='ACTIVATION_REVIEW_PASS' if passed else ('CODE_REVIEW_BLOCKED' if c['decision']!='PASS' else 'TOPIC_REVIEW_HOLD'),
        code_sha=sha,intake_hash=intake_hash(plan),corpus_hash=packet['corpus_hash'],
        dedup_request_hash=digest(packet),
        executed_workflows=workflow_evidence,environment_scope_attestation=scope_attestation,
        reused_topic_receipt=reused,
        code_review=code_result,topic_review=dedup,human_reviewed=False,publish_approved=False)
    journal.checkpoint('activation-review:'+sha+':'+intake_hash(plan),report)
    return report

def verify_receipt(plan,sha,journal,root=ROOT,workflow_evidence=None):
    from ..live.responses import build_request
    packet=dedup_request(plan,root)
    receipt=journal.get_checkpoint('activation-review:'+sha+':'+intake_hash(plan))
    require(receipt and receipt.get('status')=='ACTIVATION_REVIEW_PASS','INDEPENDENT_RECEIPT_REQUIRED')
    require(receipt.get('code_sha')==sha and receipt.get('intake_hash')==intake_hash(plan)
            and receipt.get('corpus_hash')==packet['corpus_hash']
            and receipt.get('dedup_request_hash')==digest(packet),'INDEPENDENT_RECEIPT_DRIFT')
    require(workflow_evidence and receipt.get('executed_workflows') and
            {k:v['content_hash'] for k,v in workflow_evidence.items()}==
            {k:v['content_hash'] for k,v in receipt['executed_workflows'].items()},'REVIEWED_EXECUTABLE_WORKFLOW_DRIFT')
    operations=journal.read()[2]['operations'].values()
    for key,operation,stage,data in (
        ('code_review','activation-code:'+sha,'review',code_request(plan,sha,root,receipt['executed_workflows'],receipt['environment_scope_attestation'])),
        ('topic_review','activation-dedup:'+digest(packet),'research',packet)):
        result=receipt[key]
        completed=[o for o in operations if o['operation']==operation and o['status']=='completed']
        expected=digest(build_request(stage,data))
        if key=='topic_review' and receipt.get('reused_topic_receipt'):
            reused=receipt['reused_topic_receipt'];expected=reused['request_hash']
            require(reused['packet_hash']==digest(packet) and reused['operation']==operation
                    and reused['response_id']==result['response_id'],'REUSED_TOPIC_PACKET_DRIFT')
            original=journal.get_checkpoint(reused['checkpoint'])
            require(original['dedup_request_hash']==digest(packet) and original['topic_review']==result,'REUSED_TOPIC_ORIGIN_DRIFT')
        require(len(completed)==1 and completed[0]['request_hash']==expected
                and completed[0]['response']['id']==result['response_id'],'INDEPENDENT_RECEIPT_RESPONSE_BINDING')
        parsed=journal.store.load_artifact(completed[0]['response']['text_artifact'])
        import json
        require(json.loads(parsed['text'])==result['content'],'INDEPENDENT_RECEIPT_CONTENT_BINDING')
    c=receipt['code_review']['content'];d=receipt['topic_review']['content']
    require(c['decision']=='PASS' and d['decision']=='PASS' and d.get('additional_paths')==[]
            and len(d['articles'])==2 and all(a['decision']=='DISTINCT' for a in d['articles']),
            'INDEPENDENT_RECEIPT_NOT_PASS')
    return receipt

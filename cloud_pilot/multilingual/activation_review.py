"""Independent API audit of the candidate and topic overlap before paid writing."""
import re
from pathlib import Path
from ..contract import ROOT,digest,require

CODE_FILES=(
 'cloud_pilot/multilingual/__main__.py','cloud_pilot/multilingual/localize.py',
 'cloud_pilot/multilingual/accounting.py','cloud_pilot/multilingual/control.py',
 'cloud_pilot/multilingual/sources.py','cloud_pilot/multilingual/activation_review.py',
 'cloud_pilot/live/engine.py','cloud_pilot/live/policy.py','cloud_pilot/live/responses.py',
 'cloud_pilot/live/ledger.py','cloud_pilot/live/http.py','cloud_pilot/live/stages.py',
 'cloud_pilot/runtime/multilingual-manual.yml.template')

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
    packet=dict(stage='independent_topic_dedup',plan_hash=digest(plan),
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

def code_request(plan,sha,root=ROOT):
    files={p:(root/p).read_text() for p in CODE_FILES}
    return dict(stage='independent_candidate_code_review',code_sha=sha,plan=plan,files=files,
        required_output=dict(decision='PASS | BLOCK',findings='list of {severity,file,detail,required_fix}',
                             human_reviewed=False,publish_approved=False),
        instruction='You are an independent reviewer, not the author. Audit runtime/secret boundaries, immutable '
            'code and control binding, whole-program USD3 cap, exact response identity and usage, no duplicate '
            'generation on resume, independent locale review, SSRF, source failures, and truthful delivery status. '
            'Return BLOCK for a correctness or safety problem that prevents a real English pilot. '
            'Known disclosed limitations (manual source intake, no website deployment, missing image rights, '
            'conservative cap potentially stopping early) are not proof of implementation success or reason '
            'to fabricate a pass. Give concrete code-grounded findings. No approval flags may be set true.')

def run(plan,sha,journal,models,root=ROOT):
    packet=dedup_request(plan,root) # Validate complete review inputs before the first paid request.
    code=code_request(plan,sha,root)
    code_result=models.call('activation-code:'+sha,'review',code)
    c=code_result['content']
    require(c.get('human_reviewed') is False and c.get('publish_approved') is False,'AUDIT_APPROVAL_FORBIDDEN')
    require(c.get('decision') in ('PASS','BLOCK') and isinstance(c.get('findings'),list),'AUDIT_CODE_SHAPE')
    require(c['decision']!='PASS' or not any(f.get('severity') in ('critical','high','blocker') for f in c['findings']),
            'AUDIT_CONTRADICTORY_PASS')
    journal.checkpoint('activation-code-result:'+sha,code_result)
    if c['decision']!='PASS':return dict(status='CODE_REVIEW_BLOCKED',review=code_result,real_generation=True)
    dedup=models.call('activation-dedup:'+digest(packet),'research',packet)
    d=dedup['content'];ids={a['article_id'] for a in plan['articles']}
    require(d.get('human_reviewed') is False and d.get('publish_approved') is False,'AUDIT_APPROVAL_FORBIDDEN')
    require(d.get('decision') in ('PASS','OVERLAP','NEEDS_MORE_EVIDENCE'),'AUDIT_DEDUP_SHAPE')
    rows=d.get('articles',[])
    require(len(rows)==2 and {a['article_id'] for a in rows}==ids,'AUDIT_DEDUP_COVERAGE')
    require(all(a['decision'] in ('DISTINCT','OVERLAP','NEEDS_MORE_EVIDENCE') for a in rows),'AUDIT_DEDUP_DECISION')
    known={a['path'] for a in packet['corpus_index']}
    require(all(set(a.get('nearest_paths',[]))<=known for a in rows),'AUDIT_UNKNOWN_ARTICLE_REFERENCE')
    passed=d['decision']=='PASS' and all(a['decision']=='DISTINCT' for a in rows) and d.get('additional_paths')==[]
    report=dict(status='ACTIVATION_REVIEW_PASS' if passed else 'TOPIC_REVIEW_HOLD',
        code_sha=sha,plan_hash=digest(plan),corpus_hash=packet['corpus_hash'],
        code_review=code_result,topic_review=dedup,human_reviewed=False,publish_approved=False)
    journal.checkpoint('activation-review:'+sha+':'+digest(plan),report)
    return report

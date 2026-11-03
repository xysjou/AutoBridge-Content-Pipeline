"""Immutable canonical Research and Writing files; draft-only Git transactions."""
import base64
import copy
import hashlib
import re
from urllib.parse import quote
from ..contract import canonical,digest,require
from ..live.policy import BRANCH

DATE='2026-11-03'
def json_bytes(obj):return (canonical(obj)+'\n').encode()
def blob_hash(body):return hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()

def verify_files(gh,sha,files,message,parent=None):
    c=gh.call('GET','/commits/'+sha+'?per_page=100&page=1')
    require(c['sha']==sha and len(c['parents'])==1 and c['commit']['message']==message,'EDITORIAL_COMMIT_CHANGED')
    require(parent is None or c['parents'][0]['sha']==parent,'EDITORIAL_PARENT_CHANGED')
    expected_parent=c['parents'][0]['sha'];changes=list(c.get('files',[]));page=1
    while len(c.get('files',[]))==100:
        page+=1;require(page<=30,'EDITORIAL_COMMIT_FILES_BOUND')
        c=gh.call('GET','/commits/'+sha+'?per_page=100&page='+str(page))
        require(c['sha']==sha and len(c['parents'])==1 and c['commit']['message']==message
                and c['parents'][0]['sha']==expected_parent,'EDITORIAL_COMMIT_PAGE_DRIFT')
        changes.extend(c.get('files',[]))
    require(len(changes)==len(files) and {f['filename'] for f in changes}==set(files)
            and all(f['status']=='added' and f['sha']==blob_hash(files[f['filename']]) for f in changes),'EDITORIAL_COMPLETE_DIFF_CHANGED')
    for path,body in files.items():
        obj=gh.call('GET','/contents/'+path+'?ref='+sha)
        require(obj.get('encoding')=='base64' and obj.get('sha')==blob_hash(body)
                and base64.b64decode(obj['content'])==body,'EDITORIAL_IMMUTABLE_BODY_CHANGED')
    return c['parents'][0]['sha']

def new_commit(gh,parent,files,message):
    base=gh.call('GET','/git/commits/'+parent);entries=[]
    for path,body in sorted(files.items()):
        # Editorial documents are UTF-8. One tree creates the complete batch;
        # raw binary evidence uses the separate hash-verified archive path.
        entries.append(dict(path=path,mode='100644',type='blob',content=body.decode('utf-8')))
    tree=gh.call('POST','/git/trees',dict(base_tree=base['tree']['sha'],tree=entries),201)
    return gh.call('POST','/git/commits',dict(message=message,tree=tree['sha'],parents=[parent]),201)['sha']

def isolated(gh,branch,parent,files,message):
    ref='/git/ref/heads/'+quote(branch,safe='/');status,obj=gh.api.request('GET',gh.prefix+ref)
    if status==404:
        sha=new_commit(gh,parent,files,message)
        obj=gh.call('POST','/git/refs',dict(ref='refs/heads/'+branch,sha=sha),201)
    else:require(status==200,'EDITORIAL_BRANCH_LOOKUP')
    sha=obj['object']['sha'];verify_files(gh,sha,files,message,parent)
    require(gh.ref(branch)==sha,'EDITORIAL_REF_MOVED')
    return sha

def research_files(raw):
    aid=raw['article_id'];require(re.fullmatch(r'PILOT-[A-Z0-9-]+',aid),'EDITORIAL_ARTICLE_ID')
    phase='accepted' if raw.get('research_phase')=='ACCEPTED' else 'proposals/'+raw['research_hash']
    path=f'daily/{DATE}/research/api-pilot/{aid}/versions/v{raw["version"]}/{phase}/'
    from .research_records import complete_records
    sheet,log,handoff=complete_records(raw,path)
    accepted=raw.get('research_phase')=='ACCEPTED'
    ready=dict(article_id=aid,FACT_SHEET_VERSION=raw['version'],SOURCE_LOG_VERSION=raw['version'],
        RESEARCH_STATUS=raw['fact_sheet']['status'],WRITING_AI_READY=accepted,
        research_locked=not accepted,independent_fact_review='ACCEPTED' if accepted else 'PENDING_OR_FAILED',human_reviewed=False,publish_approved=False,
        source_url_count=len(raw['evidence']),source_org_count=len({e['parent_org'] for e in raw['evidence']}),
        immutable_research_hash=raw['research_hash'])
    ready['startup_gate']=raw.get('startup_gate',{})
    files={path+'FACT_SHEET.json':json_bytes(sheet),path+'SOURCE_LOG.json':json_bytes(log),
            path+'HANDOFF.json':json_bytes(handoff),path+'RESEARCH_READY.json':json_bytes(ready),
            path+'research.json':json_bytes(raw)}
    if accepted:files[path+'INDEPENDENT_REVIEW.json']=json_bytes(raw['independent_fact_review'])
    return files

def seal_research(gh,research,start):
    raw=copy.deepcopy(research);raw['research_start']=start
    if 'research_phase' not in raw:raw['research_phase']='PROPOSAL'
    if raw['research_phase']!='ACCEPTED':
        raw['fact_sheet']['writing_ai_ready']=False
        raw['fact_sheet']['handoff'].update(research_locked=True,locks=['RESEARCH_LOCK'])
    raw['research_hash']=digest({k:v for k,v in raw.items() if k!='research_hash'})
    files=research_files(raw);parent=raw['fact_sheet']['handoff']['research_baseline_sha']
    branch='research/api-pilot-'+raw['research_hash'][:20];message='Complete immutable Research handoff '+raw['research_hash']
    sha=isolated(gh,branch,parent,files,message)
    raw['completion']=dict(commit_sha=sha,branch=branch,parent_sha=parent,input_research_hash=raw['research_hash'],
        files={p:hashlib.sha256(b).hexdigest() for p,b in files.items()},message=message)
    if raw.get('research_phase')=='ACCEPTED':
        receipt=dict(RESEARCH_COMPLETE_COMMIT_SHA=sha,ARTICLE_ID=raw['article_id'],FACT_SHEET_VERSION=raw['version'],
            completion=copy.deepcopy(raw['completion']),WRITING_AI_READY=True,PUBLISH_APPROVED=False,HUMAN_REVIEWED=False)
        receipt_path=f'daily/{DATE}/research/api-pilot/{raw["article_id"]}/versions/v{raw["version"]}/completion-receipt.json'
        receipt_message='Record pushed Research completion '+sha
        receipt_sha=isolated(gh,'research/api-completion-'+sha[:20],sha,{receipt_path:json_bytes(receipt)},receipt_message)
        raw['completion']['receipt']=dict(commit_sha=receipt_sha,path=receipt_path,content_hash=digest(receipt),message=receipt_message)
    raw['research_hash']=digest({k:v for k,v in raw.items() if k!='research_hash'})
    return raw

def complete_research(gh,proposal,accepted,completion_sync=None):
    require(accepted['research_hash']==proposal['research_hash'] and accepted['verdict']['decision']=='ACCEPT','RESEARCH_ACCEPTANCE_REQUIRED')
    raw=copy.deepcopy(proposal);raw.pop('completion');raw.pop('research_hash')
    raw.update(research_phase='ACCEPTED',proposal_reference=proposal['completion'],independent_fact_review=accepted)
    if completion_sync is not None:raw['research_completion_sync']=completion_sync
    raw['fact_sheet']['writing_ai_ready']=True
    raw['fact_sheet']['handoff'].update(research_locked=False,locks=[])
    return seal_research(gh,raw,proposal['research_start'])

def persist_failed_research(gh,response,topic,evidence,start,error):
    original=response.get('content',{});sheet=copy.deepcopy(original) if isinstance(original,dict) else {}
    from .research_records import REQUIRED
    missing=sorted(REQUIRED-set(sheet))
    sheet.update(status='RESEARCH_FAIL',writing_ai_ready=False,validation_error=str(error),
        record_completeness='INCOMPLETE_MODEL_OR_SOURCE_FAILURE',missing_output_fields=missing)
    for k in ('facts','allowed_facts','source_checks','blocked_facts'):
        if not isinstance(sheet.get(k),list):sheet[k]=[]
    sheet['facts']=[f for f in sheet['facts'] if isinstance(f,dict) and isinstance(f.get('id'),str) and isinstance(f.get('statement'),str)]
    for f in sheet['facts']:
        if not isinstance(f.get('source_ids'),list):f['source_ids']=[]
    for k in ('allowed_facts','blocked_facts'):sheet[k]=[x for x in sheet[k] if isinstance(x,str)]
    if not isinstance(sheet.get('fact_boundary'),dict):sheet['fact_boundary']={}
    sheet['blocked_facts']=list(dict.fromkeys(sheet['blocked_facts']+['INCOMPLETE_RESEARCH_RECORD:'+str(error)]))
    if not isinstance(sheet.get('handoff'),dict):sheet['handoff']={}
    h=sheet['handoff'];h.update(research_baseline_sha=topic['research_baseline_sha'],
        research_locked=True,writing_locked=False,locks=['RESEARCH_LOCK'],fact_update_required=True)
    if not isinstance(h.get('facts_not_allowed_in_body'),list):h['facts_not_allowed_in_body']=[]
    h['facts_not_allowed_in_body']=list(dict.fromkeys([x for x in h['facts_not_allowed_in_body'] if isinstance(x,str)]+sheet['blocked_facts']))
    raw=dict(article_id=topic['article_id'],version=start['version'],topic=topic,evidence=evidence,
        fact_sheet=sheet,research_phase='FAILED',raw_model_response=response,startup_gate=response.get('startup_gate',{}),human_reviewed=False,publish_approved=False)
    return seal_research(gh,raw,start)

def persist_source_failure(gh,topic,evidence,start,error,startup=None,failed_source=None):
    response=dict(startup_gate=startup or {},content=dict(status='RESEARCH_FAIL',writing_ai_ready=False,facts=[],allowed_facts=[],
        blocked_facts=['SOURCE_ACCESS_OR_ARCHIVE_FAILURE'],source_checks=[],fact_boundary={},handoff={},
        access_failure=dict(error=str(error),failed_source=failed_source),human_reviewed=False,publish_approved=False))
    record=persist_failed_research(gh,response,topic,evidence,start,error)
    return record

def record_transfer_failure(gh,journal,plan,startup,error):
    from .editorial_state import EditorialState
    state=EditorialState(journal);topic=next(t for t in plan['articles'] if t['article_id']==error.article_id)
    aid=topic['article_id'];start=state.snapshot()['articles'].get(aid,{}).get('research_lock')
    if start is None:start=state.begin(aid,getattr(journal,'prefix','')+':source-transfer-failure:'+aid)
    failed=persist_source_failure(gh,topic,error.partial,start,error,startup,error.source)
    journal.checkpoint('failed-source-research:'+aid,failed)
    return failed

def push_startup_manifest(gh,startup,plan,run_id):
    path=f'daily/{DATE}/research/api-pilot/startup/{run_id}/daily_manifest.json'
    record=dict(BATCH_ID='api-pilot-'+DATE,STATUS='BLOCKED',TOTAL_MAIN=len(plan['articles']),TOTAL_RESERVE=0,
        MAIN_PASS_COUNT=0,MAIN_CONDITIONAL_COUNT=0,MAIN_FAIL_COUNT=0,WRITING_READY_COUNT=0,
        BLOCKED_ARTICLES=[t['article_id'] for t in plan['articles']],stage='PRE_RESEARCH',startup_gate=startup,
        articles=[dict(ARTICLE_ID=t['article_id'],WRITING_AI_READY=False,RESEARCH_STATUS='PENDING') for t in plan['articles']],
        plan=plan,PUBLISH_APPROVED=False,HUMAN_REVIEWED=False)
    files={path:json_bytes(record)}
    sha=isolated(gh,'research/api-startup-'+digest(record)[:20],startup['approved_main_sha'],files,'Record actual pilot Research startup '+digest(record))
    return dict(commit_sha=sha,path=path,content_hash=digest(record))

def verify_research(gh,research):
    require(research['research_hash']==digest({k:v for k,v in research.items() if k!='research_hash'}),'RESEARCH_PACKET_CHANGED')
    c=research.get('completion',{});require(re.fullmatch('[0-9a-f]{40}',c.get('commit_sha','')),'PUSHED_RESEARCH_COMPLETION_REQUIRED')
    raw={k:v for k,v in research.items() if k!='completion'};raw['research_hash']=c['input_research_hash']
    require(raw['research_hash']==digest({k:v for k,v in raw.items() if k!='research_hash'}),'RESEARCH_COMPLETION_INPUT_DRIFT')
    files=research_files(raw)
    require(c['files']=={p:hashlib.sha256(b).hexdigest() for p,b in files.items()},'RESEARCH_COMPLETION_FILES_DRIFT')
    verify_files(gh,c['commit_sha'],files,c['message'],c['parent_sha'])
    if research.get('research_phase')=='ACCEPTED':
        ref=c['receipt'];expected=dict(RESEARCH_COMPLETE_COMMIT_SHA=c['commit_sha'],ARTICLE_ID=research['article_id'],FACT_SHEET_VERSION=research['version'],
            completion={k:v for k,v in c.items() if k!='receipt'},WRITING_AI_READY=True,PUBLISH_APPROVED=False,HUMAN_REVIEWED=False)
        require(digest(expected)==ref['content_hash'],'RESEARCH_COMPLETION_RECEIPT_CHANGED')
        verify_files(gh,ref['commit_sha'],{ref['path']:json_bytes(expected)},ref['message'],c['commit_sha'])
    return c

def writing_files(package):
    from .localize import markdown
    a,r,v=package['article'],package['research'],package['review'];aid=a['article_id']
    require(v['content_hash']==a['content_hash'] and v['verdict']['decision']=='REVIEW_PASS','EDITORIAL_REVIEW_REQUIRED')
    text=markdown(a,r,r['topic'],public_only=True)
    require(v['rendered_hash']==digest(text),'EDITORIAL_PUBLIC_RENDER_DRIFT')
    path=f'daily/{DATE}/articles/api-pilot/{aid}/research-v{r["version"]}/versions/v{a["version"]}/'
    qa=f'daily/{DATE}/qa/api-pilot/{aid}/research-v{r["version"]}/v{a["version"]}.review.json'
    manifest=dict(article=a,review=v,research_reference=r['completion'],human_reviewed=False,publish_approved=False)
    return {path+'article.md':text.encode(),path+'seo.editorial.json':json_bytes(dict(status='UNREVIEWED_EDITORIAL_METADATA',public=a['public'])),
            path+'candidate.json':json_bytes(manifest),qa:json_bytes(v)}

def publish_delivery_bundle(gh,files,identity):
    """All locales and metadata become reachable in one CAS Git commit."""
    require(files and all(p.startswith(f'deliveries/{DATE}/api-pilot/') and '..' not in p for p in files),'DELIVERY_FILE_BOUNDARY')
    manifest_path=f'deliveries/{DATE}/api-pilot/{identity}/BUNDLE_CONTENT_HASHES.json'
    contents={p:hashlib.sha256(b).hexdigest() for p,b in files.items()};all_files=dict(files)
    all_files[manifest_path]=json_bytes(contents);message='Add immutable reviewed multilingual text bundle '+identity
    status,obj=gh.api.request('GET',gh.prefix+'/contents/'+manifest_path+'?ref='+quote(BRANCH,safe=''))
    if status==200:
        require(base64.b64decode(obj['content'])==all_files[manifest_path],'DELIVERY_BUNDLE_CONFLICT')
        # Every immutable file is still compared before returning a resume.
        for p,b in files.items():
            o=gh.call('GET','/contents/'+p+'?ref='+quote(BRANCH,safe=''))
            require(o['sha']==blob_hash(b) and base64.b64decode(o['content'])==b,'DELIVERY_BUNDLE_BODY_CHANGED')
        return {p:blob_hash(b) for p,b in files.items()}
    require(status==404,'DELIVERY_BUNDLE_LOOKUP')
    parent=gh.ref(BRANCH);sha=new_commit(gh,parent,all_files,message)
    # Fixed expected parent prevents a branch race from replacing other work.
    require(gh.ref(BRANCH)==parent,'DELIVERY_BRANCH_CAS_CONFLICT')
    verify_files(gh,sha,all_files,message,parent)
    gh.call('PATCH','/git/refs/heads/'+quote(BRANCH,safe='/'),dict(sha=sha,force=False))
    require(gh.ref(BRANCH)==sha,'DELIVERY_BRANCH_UPDATE_UNCONFIRMED')
    return {p:blob_hash(b) for p,b in files.items()}

def sync_batch_manifest(gh,journal,plan,startup):
    from .editorial_state import EditorialState
    from ..contract import GateError
    state=EditorialState(journal);snapshot=state.snapshot();rows=[]
    for topic in plan['articles']:
        aid=topic['article_id'];r=journal.get_checkpoint('research:'+aid)
        a=snapshot['articles'].get(aid,{})
        if r:
            try:state.check(r)
            except GateError:r=None
        if r:
            verify_research(gh,r)
            row=dict(ARTICLE_ID=aid,RESEARCH_STATUS=r['fact_sheet']['status'],WRITING_AI_READY=True,
                FACT_SHEET_VERSION=r['version'],SOURCE_LOG_VERSION=r['version'],RESEARCH_HASH=r['research_hash'],
                RESEARCH_COMPLETE_COMMIT_SHA=r['completion']['commit_sha'],RESEARCH_FILES=r['completion']['files'])
        else:
            candidates=[journal.get_checkpoint(k+aid) for k in ('failed-source-research:','failed-research:','withheld-research:')]
            current_version=a.get('research_lock',{}).get('version') if a.get('research_lock') else None
            candidates=[f for f in candidates if f and (current_version is None or f['version']==current_version)]
            failed=max(candidates,key=lambda f:f['version'],default=None)
            row=dict(ARTICLE_ID=aid,RESEARCH_STATUS=failed['fact_sheet']['status'] if failed else 'PENDING',
                WRITING_AI_READY=False,FACT_SHEET_VERSION=failed['version'] if failed else None,
                SOURCE_LOG_VERSION=failed['version'] if failed else None,RESEARCH_HASH=failed['research_hash'] if failed else None,
                RESEARCH_COMPLETE_COMMIT_SHA=failed['completion']['commit_sha'] if failed else None)
            row['PREVIOUS_ACCEPTED_HEAD']=a.get('head')
        rows.append(row)
    counts={name:sum(r['RESEARCH_STATUS']==status for r in rows) for name,status in
        [('MAIN_PASS_COUNT','RESEARCH_PASS'),('MAIN_CONDITIONAL_COUNT','RESEARCH_CONDITIONAL'),('MAIN_FAIL_COUNT','RESEARCH_FAIL')]}
    ready=sum(r['WRITING_AI_READY'] for r in rows)
    status=('READY_WITH_CONDITIONS' if counts['MAIN_CONDITIONAL_COUNT'] else 'READY') if ready==len(rows) else ('PARTIAL' if counts['MAIN_FAIL_COUNT'] else 'BLOCKED')
    record=dict(BATCH_ID='api-pilot-'+DATE,STATUS=status,TOTAL_MAIN=len(rows),TOTAL_RESERVE=0,
        **counts,WRITING_READY_COUNT=ready,BLOCKED_ARTICLES=[r['ARTICLE_ID'] for r in rows if not r['WRITING_AI_READY']],
        articles=rows,plan=plan,startup_gate=startup,PUBLISH_APPROVED=False,HUMAN_REVIEWED=False)
    identity=digest(record);path=f'daily/{DATE}/research/api-pilot/manifests/{identity}/daily_manifest.json'
    sha=isolated(gh,'research/api-manifest-'+identity[:20],startup['approved_main_sha'],{path:json_bytes(record)},'Record actual Research batch manifest '+identity)
    receipt=dict(commit_sha=sha,path=path,content_hash=identity)
    journal.checkpoint('batch-manifest:'+identity,receipt)
    sequence=len(journal.read()[0]['events'])
    journal.checkpoint('batch-manifest-current:'+str(sequence),receipt)
    return receipt

def recover_publication(gh,journal,authorization):
    """Protected operator abort, available before stale evidence is loaded.

    Partial drafts are inspected, open candidate PRs closed, and an immutable
    invalidation record pushed before the same CAS marks old Research unusable
    and releases its fence. A later approved evidence epoch can then begin.
    """
    import json
    from .editorial_state import EditorialState
    state=EditorialState(journal);token=state.snapshot()['publication']
    require(authorization.get('action')=='ABORT_AND_INVALIDATE' and authorization.get('reason')
            and token and authorization.get('fence')==token['fence'],'EXACT_OPERATOR_ABORT_REQUIRED')
    proofs=[]
    if token['owner'].startswith('model:'):
        view=journal.read()[2]
        operations=list(view['operations'].values())
        require(not any(o['status'] in ('reserved','sent','uncertain') for o in operations),'INFLIGHT_MODEL_ABORT_FORBIDDEN')
        proofs.append(dict(kind='SETTLED_MODEL_STAGE',receipts=[dict(operation=o['operation'],
            status=o['status'],response_id=o.get('response',{}).get('id')) for o in operations]))
    elif token['owner'].startswith('english:'):
        for aid,rhash in token['targets'].items():
            package=journal.get_checkpoint('final:'+aid)
            require(package and package['research']['research_hash']==rhash
                    and token['owner']=='english:'+package['article']['content_hash'],'ABORT_PACKAGE_BINDING')
            branch='feature/work-cloud-pilot-article-'+digest(package)[:20]
            status,obj=gh.api.request('GET',gh.prefix+'/git/ref/heads/'+quote(branch,safe='/'))
            require(status in (200,404),'ABORT_REF_UNCONFIRMED')
            row=dict(branch=branch,present=status==200)
            if status==200:
                sha=obj['object']['sha'];files=writing_files(package)
                verify_files(gh,sha,files,'Add immutable English pilot candidate '+digest(package))
                row.update(head_sha=sha,files={p:blob_hash(b) for p,b in files.items()})
                prs=gh.call('GET','/pulls?state=all&head='+quote('xysjou:'+branch,safe='')+'&per_page=100')
                row['prs']=[]
                for pr in prs:
                    require(pr['head']['sha']==sha and pr['draft'] is True and not pr.get('merged_at'),'ABORT_NON_DRAFT_OR_MERGED')
                    if pr['state']=='open':gh.call('PATCH','/pulls/'+str(pr['number']),dict(state='closed'))
                    confirmed=gh.call('GET','/pulls/'+str(pr['number']))
                    require(confirmed['state']=='closed' and not confirmed.get('merged_at'),'ABORT_PR_NOT_CLOSED')
                    row['prs'].append(dict(number=pr['number'],state='closed',head_sha=sha))
            proofs.append(row)
    else:
        require(token['owner'].startswith('multilingual:'),'ABORT_UNKNOWN_OWNER')
        identity=token['owner'].split(':',1)[1]
        path=f'deliveries/{DATE}/api-pilot/{identity}/BUNDLE_CONTENT_HASHES.json'
        status,obj=gh.api.request('GET',gh.prefix+'/contents/'+path+'?ref='+quote(BRANCH,safe=''))
        require(status in (200,404),'ABORT_BUNDLE_UNCONFIRMED')
        row=dict(manifest=path,present=status==200)
        if status==200:
            contents=json.loads(base64.b64decode(obj['content']))
            require(len(contents)==72 and all(p.startswith(f'deliveries/{DATE}/api-pilot/{identity}/') for p in contents),'ABORT_BUNDLE_BOUNDARY')
            for p,h in contents.items():
                f=gh.call('GET','/contents/'+p+'?ref='+quote(BRANCH,safe=''))
                require(hashlib.sha256(base64.b64decode(f['content'])).hexdigest()==h,'ABORT_BUNDLE_CHANGED')
            row['content_hashes']=contents
        proofs.append(row)
    proof=dict(status='VERIFIED_INVALIDATED',fence=token['fence'],owner=token['owner'],targets=token['targets'],
        reason=authorization['reason'],artifacts=proofs,human_reviewed=False,publish_approved=False,
        consequence='Historical drafts invalidated. A fresh eligible Research epoch is required; no publication or CURRENT promotion.')
    path=f'daily/{DATE}/qa/api-pilot/publication-aborts/{token["fence"]}.json'
    proof['invalidation_path']=path
    gh.put_canonical_qa(path,json_bytes(proof))
    state.abort_publication(token,proof)
    return proof

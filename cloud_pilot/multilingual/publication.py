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
    c=gh.call('GET','/commits/'+sha)
    require(c['sha']==sha and len(c['parents'])==1 and c['commit']['message']==message,'EDITORIAL_COMMIT_CHANGED')
    require(parent is None or c['parents'][0]['sha']==parent,'EDITORIAL_PARENT_CHANGED')
    changes=c.get('files',[])
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
    path=f'daily/{DATE}/research/api-pilot/{aid}/versions/v{raw["version"]}/'
    ready=dict(article_id=aid,FACT_SHEET_VERSION=raw['version'],SOURCE_LOG_VERSION=raw['version'],
        RESEARCH_STATUS=raw['fact_sheet']['status'],WRITING_AI_READY=True,
        independent_fact_review='PENDING',human_reviewed=False,publish_approved=False,
        source_url_count=len(raw['evidence']),source_org_count=len({e['parent_org'] for e in raw['evidence']}),
        immutable_research_hash=raw['research_hash'])
    return {path+'FACT_SHEET.json':json_bytes(raw['fact_sheet']),path+'SOURCE_LOG.json':json_bytes(raw['evidence']),
            path+'HANDOFF.json':json_bytes(raw['fact_sheet']['handoff']),path+'RESEARCH_READY.json':json_bytes(ready),
            path+'research.json':json_bytes(raw)}

def seal_research(gh,research,start):
    raw=copy.deepcopy(research);raw['research_start']=start
    raw['research_hash']=digest({k:v for k,v in raw.items() if k!='research_hash'})
    files=research_files(raw);parent=raw['fact_sheet']['handoff']['research_baseline_sha']
    branch='research/api-pilot-'+raw['research_hash'][:20];message='Complete immutable Research handoff '+raw['research_hash']
    sha=isolated(gh,branch,parent,files,message)
    raw['completion']=dict(commit_sha=sha,branch=branch,parent_sha=parent,input_research_hash=raw['research_hash'],
        files={p:hashlib.sha256(b).hexdigest() for p,b in files.items()},message=message)
    raw['research_hash']=digest({k:v for k,v in raw.items() if k!='research_hash'})
    return raw

def verify_research(gh,research):
    require(research['research_hash']==digest({k:v for k,v in research.items() if k!='research_hash'}),'RESEARCH_PACKET_CHANGED')
    c=research.get('completion',{});require(re.fullmatch('[0-9a-f]{40}',c.get('commit_sha','')),'PUSHED_RESEARCH_COMPLETION_REQUIRED')
    raw={k:v for k,v in research.items() if k!='completion'};raw['research_hash']=c['input_research_hash']
    require(raw['research_hash']==digest({k:v for k,v in raw.items() if k!='research_hash'}),'RESEARCH_COMPLETION_INPUT_DRIFT')
    files=research_files(raw)
    require(c['files']=={p:hashlib.sha256(b).hexdigest() for p,b in files.items()},'RESEARCH_COMPLETION_FILES_DRIFT')
    verify_files(gh,c['commit_sha'],files,c['message'],c['parent_sha'])
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
    gh.call('PATCH','/git/refs/heads/'+quote(BRANCH,safe='/'),dict(sha=sha,force=False))
    verify_files(gh,sha,all_files,message,parent)
    return {p:blob_hash(b) for p,b in files.items()}

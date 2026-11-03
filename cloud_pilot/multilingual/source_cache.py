"""Validate cached evidence; explicitly reparse protected, hash-bound raw archives."""
import base64
import hashlib
import re
from datetime import datetime,timezone
from urllib.parse import quote
from ..contract import digest,require
from ..live.policy import BRANCH
from .sources import extract,MAX_BYTES

def validate(items,topic):
    require(isinstance(items,list) and len(items)==len(topic['sources']),'CACHED_SOURCE_COUNT')
    known={s['source_id']:s for s in topic['sources']}
    require({e['source_id'] for e in items}==set(known),'CACHED_SOURCE_IDS')
    for e in items:
        s=known[e['source_id']]
        require(all(e.get(k)==s[k] for k in ('publisher','parent_org','tier','scope'))
                and e.get('requested_url')==s['url'],'CACHED_SOURCE_DECLARATION_DRIFT')
        require(e.get('final_url') in {s['url'],*s.get('authorized_redirect_urls',[])},'CACHED_SOURCE_REDIRECT_DRIFT')
        t=datetime.fromisoformat(e['retrieved_at'])
        require(t.tzinfo and 0<=(datetime.now(timezone.utc)-t).total_seconds()<=86400,'SOURCE_EVIDENCE_STALE')
        require(hashlib.sha256(e['text'].encode()).hexdigest()==e['text_sha256'],'CACHED_SOURCE_TEXT_DRIFT')
        require(digest({k:v for k,v in e.items() if k!='evidence_hash'})==e.get('evidence_hash'),'CACHED_SOURCE_HASH_DRIFT')
    return items

def restore(permit,plan,journal,scoped,github,code_sha):
    descriptors=permit.get('source_evidence_transfers',[]);receipts=[]
    require(len({d['article_id'] for d in descriptors})==len(descriptors),'DUPLICATE_SOURCE_TRANSFER')
    topics={t['article_id']:t for t in plan['articles']}
    for d in descriptors:
        aid=d['article_id'];require(aid in topics and d.get('operator_verified') is True,'SOURCE_TRANSFER_NOT_APPROVED')
        topic=topics[aid];key='evidence:'+aid
        old=journal.get_checkpoint(d['origin_checkpoint'])
        require(old and digest(old)==d['origin_evidence_hash'],'SOURCE_TRANSFER_ORIGIN_HASH')
        cached=scoped.get_checkpoint(key)
        if cached is None:
            require(len(old)==len(topic['sources']),'SOURCE_TRANSFER_COUNT')
            source={s['source_id']:s for s in topic['sources']};out=[]
            require({e['source_id'] for e in old}==set(source),'SOURCE_TRANSFER_IDS')
            for e in old:
                s=source[e['source_id']]
                require(all(e.get(k)==s[k] for k in ('publisher','parent_org','tier','scope'))
                        and e.get('requested_url')==s['url'],'SOURCE_TRANSFER_DECLARATION_DRIFT')
                raw_hash=e.get('raw_sha256','');require(re.fullmatch('[0-9a-f]{64}',raw_hash),'SOURCE_TRANSFER_RAW_HASH')
                path='cloud_pilot/live_artifacts/sources/'+raw_hash+'.bin'
                require(path==e.get('raw_artifact_path'),'SOURCE_TRANSFER_RAW_PATH')
                status,obj=github.api.request('GET',github.prefix+'/contents/'+path+'?ref='+quote(BRANCH,safe=''))
                require(status==200 and obj.get('encoding')=='base64' and obj.get('sha')==e.get('raw_artifact_blob'),
                        'SOURCE_TRANSFER_RAW_BLOB')
                raw=base64.b64decode(obj['content'])
                require(len(raw)<=MAX_BYTES and hashlib.sha256(raw).hexdigest()==raw_hash,'SOURCE_TRANSFER_RAW_CONTENT')
                text=extract(raw,e['mime'],s)
                new={k:v for k,v in e.items() if k!='evidence_hash'}
                new.update(text=text,text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                           representation_code_sha=code_sha,archive_origin_checkpoint=d['origin_checkpoint'])
                new['evidence_hash']=digest(new);out.append(new)
            validate(out,topic)
            scoped.checkpoint(key,out);cached=out
        validate(cached,topic)
        proof=dict(article_id=aid,origin_checkpoint=d['origin_checkpoint'],origin_evidence_hash=d['origin_evidence_hash'],
                   target_checkpoint=scoped.prefix+key,target_evidence_hash=digest(cached),
                   original_retrieval_times=[e['retrieved_at'] for e in cached],
                   representation_code_sha=code_sha,raw_hashes=[e['raw_sha256'] for e in cached])
        prior=scoped.get_checkpoint('source-transfer:'+aid)
        require(prior is None or prior==proof,'SOURCE_TRANSFER_PROOF_DRIFT')
        scoped.checkpoint('source-transfer:'+aid,proof);receipts.append(proof)
    return receipts

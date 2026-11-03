"""Validate cached evidence; explicitly reparse protected, hash-bound raw archives."""
import base64
import hashlib
import re
from datetime import datetime,timezone
from urllib.parse import quote
from ..contract import digest,require
from ..live.policy import BRANCH
from .sources import extract,source_title,MAX_BYTES
from ..live.sources import PlainText

def archive_content_type(raw,e):
    """Recover a discarded HTTP charset only by exact prior text equivalence.

    Historical receipts retained MIME but dropped HTTP charset. HTML metadata
    can contradict the HTTP response. Never guess from language or replace bytes:
    require the strict decoded document to reproduce the hash-bound old text.
    """
    require(hashlib.sha256(e['text'].encode()).hexdigest()==e['text_sha256'],'SOURCE_TRANSFER_OLD_TEXT_HASH')
    matches=[]
    for codec in ('utf-8-sig','gb18030'):
        try:document=raw.decode(codec)
        except UnicodeDecodeError:continue
        text=document
        if e['mime']=='text/html':
            parser=PlainText();parser.feed(document);text=' '.join(''.join(parser.parts).split())
        if text==e['text']:matches.append('utf-8' if codec=='utf-8-sig' else codec)
    require(matches,'SOURCE_TRANSFER_CHARSET_UNPROVEN')
    return e['mime']+';charset='+matches[0]

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
        prior=scoped.get_checkpoint('source-transfer:'+aid)
        require(len(old)==len(topic['sources']),'SOURCE_TRANSFER_COUNT')
        source={s['source_id']:s for s in topic['sources']};out=[]
        require({e['source_id'] for e in old}==set(source),'SOURCE_TRANSFER_IDS')
        for e in old:
            s=source[e['source_id']]
            require(all(e.get(k)==s[k] for k in ('publisher','parent_org','scope'))
                    and e.get('requested_url')==s['url'],'SOURCE_TRANSFER_DECLARATION_DRIFT')
            if e.get('tier')!=s['tier']:
                c=d.get('source_tier_reclassifications',{}).get(s['source_id'],{})
                require(c.get('from')==e.get('tier')=='T3' and c.get('to')==s['tier']=='T2'
                        and c.get('publisher_verified') is True and c.get('basis')
                        and re.fullmatch(r'https://(?:car\.autohome\.com\.cn/config/spec/\d+\.html|www\.yoojia\.com/m-\d+)',s['url']),
                        'SOURCE_TIER_RECLASSIFICATION_UNPROVEN')
            raw_hash=e.get('raw_sha256','');require(re.fullmatch('[0-9a-f]{64}',raw_hash),'SOURCE_TRANSFER_RAW_HASH')
            path='cloud_pilot/live_artifacts/sources/'+raw_hash+'.bin'
            require(path==e.get('raw_artifact_path'),'SOURCE_TRANSFER_RAW_PATH')
            status,obj=github.api.request('GET',github.prefix+'/contents/'+path+'?ref='+quote(BRANCH,safe=''))
            require(status==200 and obj.get('encoding')=='base64' and obj.get('sha')==e.get('raw_artifact_blob'),
                    'SOURCE_TRANSFER_RAW_BLOB')
            status,blob=github.api.request('GET',github.prefix+'/git/blobs/'+e['raw_artifact_blob'])
            require(status==200 and blob.get('encoding')=='base64' and blob.get('sha')==e['raw_artifact_blob'],
                    'SOURCE_TRANSFER_GIT_BLOB')
            raw=base64.b64decode(blob['content'])
            require(len(raw)<=MAX_BYTES and hashlib.sha256(raw).hexdigest()==raw_hash,'SOURCE_TRANSFER_RAW_CONTENT')
            content_type=e.get('content_type') or archive_content_type(raw,e)
            text=extract(raw,content_type,s)
            new={k:v for k,v in e.items() if k!='evidence_hash'}
            new.update(text=text,text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                       source_title=source_title(raw,content_type),
                       tier=s['tier'],content_type=content_type,representation_code_sha=code_sha,archive_origin_checkpoint=d['origin_checkpoint'])
            new['evidence_hash']=digest(new);out.append(new)
            scoped.checkpoint('source-transfer-progress:'+aid+':'+s['source_id'],out)
        validate(out,topic)
        require(d.get('expected_target_checkpoint')==scoped.prefix+key and digest(out)==d.get('expected_target_evidence_hash'),'SOURCE_TRANSFER_EXPECTED_TARGET_DRIFT')
        require(cached is None or cached==out,'SOURCE_TRANSFER_RECONSTRUCTED_TARGET_DRIFT')
        scoped.checkpoint(key,out);cached=out
        validate(cached,topic)
        origins={e['source_id']:e for e in old}
        require(all(e['raw_sha256']==origins[e['source_id']]['raw_sha256']
                    and e['raw_artifact_blob']==origins[e['source_id']]['raw_artifact_blob']
                    and e['retrieved_at']==origins[e['source_id']]['retrieved_at']
                    and e['archive_origin_checkpoint']==d['origin_checkpoint']
                    and e['representation_code_sha']==code_sha for e in cached),'SOURCE_TRANSFER_CACHED_ORIGIN_DRIFT')
        proof=dict(article_id=aid,origin_checkpoint=d['origin_checkpoint'],origin_evidence_hash=d['origin_evidence_hash'],
                   target_checkpoint=scoped.prefix+key,target_evidence_hash=digest(cached),
                   original_retrieval_times=[e['retrieved_at'] for e in cached],
                   representation_code_sha=code_sha,raw_hashes=[e['raw_sha256'] for e in cached],
                   tier_reclassifications=d.get('source_tier_reclassifications',{}))
        require(prior is None or prior==proof,'SOURCE_TRANSFER_PROOF_DRIFT')
        scoped.checkpoint('source-transfer:'+aid,proof);receipts.append(proof)
    return receipts

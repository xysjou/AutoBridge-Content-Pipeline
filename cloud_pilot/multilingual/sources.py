"""Bounded source retrieval using existing pinned-TLS controls, UTF-8/GB18030."""
import hashlib
import re
import json
from urllib.parse import urljoin
from ..contract import require,digest
from ..live.sources import url_parts,public_addresses,PinnedHTTPS,PlainText
from ..live.policy import timestamp

MAX_BYTES=1_000_000  # Base64 evidence stays inside the existing 2 MB API read bound.

def extract(raw,content_type,source):
    text=decode(raw,content_type)
    if content_type.split(';')[0].strip().lower()=='text/html':
        html=text;parser=PlainText();parser.feed(html);text=' '.join(''.join(parser.parts).split())
        # Read only public literal JSON already supplied in the approved document.
        # Never execute page scripts or reconstruct obfuscated labels/values.
        m=re.fullmatch(r'https://car\.autohome\.com\.cn/config/spec/(\d+)\.html',source['url'])
        if m:
            marker=re.search(r'\bvar\s+config\s*=\s*',html)
            if marker:
                try:data,_=json.JSONDecoder().raw_decode(html[marker.end():])
                except ValueError:require(False,'INLINE_CONFIGURATION_JSON_INVALID')
                result=data.get('result',{});spec=int(m.group(1));rows=[]
                require(result.get('specid')==spec,'INLINE_CONFIGURATION_SPEC_DRIFT')
                for group in result.get('paramtypeitems',[]):
                    for item in group.get('paramitems',[]):
                        name=item.get('name','')
                        if not isinstance(name,str) or '<' in name:continue
                        for value in item.get('valueitems',[]):
                            v=value.get('value','')
                            if value.get('specid')==spec and isinstance(v,str) and v and '<' not in v:
                                rows.append(name+': '+v)
                require(len(rows)<=200,'INLINE_CONFIGURATION_ROWS_BOUND')
                if rows:text+='\nPublic literal inline configuration for spec '+str(spec)+':\n'+'\n'.join(rows)
    require(100<=len(text)<=100000,'SOURCE_TEXT_INSUFFICIENT_OR_TOO_LARGE')
    return text

def decode(raw,content_type):
    # Only declared supported encodings; no lossy replacement or invented fallback text.
    header=re.search(r'charset\s*=\s*["\']?([\w-]+)',content_type,re.I)
    meta=re.search(br'charset\s*=\s*["\']?([\w-]+)',raw[:8192],re.I)
    enc=(header.group(1) if header else meta.group(1).decode('ascii') if meta else 'utf-8').lower()
    require(enc in ('utf-8','utf8','gb2312','gbk','gb18030'),'SOURCE_ENCODING_UNSUPPORTED')
    try:return raw.decode('utf-8-sig' if enc in ('utf8','utf-8') else 'gb18030')
    except UnicodeDecodeError:require(False,'SOURCE_ENCODING_INVALID')

def retrieve(source,allowed,resolver=None,connection=PinnedHTTPS):
    current=source['url'];hops=[]
    for _ in range(4):
        p,host=url_parts(current,allowed)
        ips=public_addresses(host,**({'resolver':resolver} if resolver else {}))
        conn=connection(host,ips[0])
        try:
            conn.request('GET',(p.path or '/')+('?' + p.query if p.query else ''),headers={
                'Host':host,'User-Agent':'AutoBridge-Evidence-Pilot','Accept':'text/html,text/plain','Accept-Encoding':'identity'})
            r=conn.getresponse()
            if r.status in (301,302,303,307,308):
                target=urljoin(current,r.getheader('Location',''));url_parts(target,allowed)
                hops.append(dict(url=current,status=r.status,target=target));current=target;continue
            require(r.status==200,'SOURCE_ACCESS_LIMITATION:'+str(r.status))
            require(r.getheader('Content-Encoding','identity').lower()=='identity','SOURCE_COMPRESSION_UNSUPPORTED')
            ct=r.getheader('Content-Type','');mime=ct.split(';')[0].strip().lower()
            require(mime in ('text/html','text/plain'),'SOURCE_MIME_UNSUPPORTED')
            length=r.getheader('Content-Length')
            require(length is None or (length.isdigit() and int(length)<=MAX_BYTES),'SOURCE_TOO_LARGE')
            raw=r.read(MAX_BYTES+1);require(len(raw)<=MAX_BYTES,'SOURCE_TOO_LARGE')
            text=extract(raw,ct,source)
            result=dict(source_id=source['source_id'],requested_url=source['url'],final_url=current,
                publisher=source['publisher'],parent_org=source['parent_org'],tier=source['tier'],
                scope=source['scope'],retrieved_at=timestamp(),status=200,mime=mime,
                raw_sha256=hashlib.sha256(raw).hexdigest(),text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                content_type=ct,resolved_ips=ips,connected_ip=ips[0],redirects=hops,text=text,
                authority_status='DECLARED_SOURCE_REQUIRES_RESEARCH_AND_REVIEW',synthetic=False)
            result['evidence_hash']=digest(result)
            return result,raw
        finally:conn.close()
    require(False,'SOURCE_REDIRECT_LIMIT')

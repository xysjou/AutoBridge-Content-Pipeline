"""Exact-URL allowlist, pinned public IPs, bounded text retrieval and provenance."""
import hashlib
import http.client
from html.parser import HTMLParser
import ipaddress
import socket
import ssl
from urllib.parse import urlsplit, urljoin
from ..contract import require, digest
from .policy import timestamp

MAX_BYTES=256000

def url_parts(url,allowed):
    require(url in allowed,'URL_NOT_AUTHORIZED')
    p=urlsplit(url)
    require(p.scheme=='https' and p.hostname and p.port in (None,443),'HTTPS_ONLY')
    require(not p.username and not p.password and not p.fragment,'URL_CREDENTIALS_OR_FRAGMENT')
    require('\\' not in url and not any(ord(c)<33 for c in url),'MALFORMED_URL')
    host=p.hostname.encode('idna').decode('ascii')
    require('.' in host and not host.endswith('.'),'INVALID_SOURCE_HOST')
    return p,host

def public_addresses(host,resolver=socket.getaddrinfo):
    rows=resolver(host,443,type=socket.SOCK_STREAM)
    ips=sorted({r[4][0] for r in rows})
    require(ips,'DNS_EMPTY')
    for ip in ips:
        a=ipaddress.ip_address(ip)
        require(a.is_global and not a.is_multicast and not a.is_reserved and not a.is_unspecified,'NON_PUBLIC_SOURCE_IP')
        if getattr(a,'ipv4_mapped',None):require(a.ipv4_mapped.is_global,'NON_PUBLIC_MAPPED_IP')
        require(not getattr(a,'sixtofour',None) and not getattr(a,'teredo',None),'IP_TRANSITION_TUNNEL_NOT_ALLOWED')
    return ips

class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self,host,ip):
        super().__init__(host,443,timeout=10,context=ssl.create_default_context())
        self.pinned_ip=ip

    def connect(self):
        sock=socket.create_connection((self.pinned_ip,443),timeout=10)
        try:
            require(ipaddress.ip_address(sock.getpeername()[0])==ipaddress.ip_address(self.pinned_ip),'PEER_IP_MISMATCH')
            self.sock=self._context.wrap_socket(sock,server_hostname=self.host)
        except Exception:
            sock.close();raise

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.ignored=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript'):self.ignored+=1
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript') and self.ignored:self.ignored-=1
        if tag in ('p','div','li','h1','h2','h3','tr'):self.parts.append('\n')
    def handle_data(self,data):
        if not self.ignored:self.parts.append(data)

def retrieve(source,allowed,resolver=socket.getaddrinfo,connection=PinnedHTTPS,clock=timestamp):
    current=source['url'];hops=[]
    for _ in range(4):
        p,host=url_parts(current,allowed)
        ips=public_addresses(host,resolver)
        conn=connection(host,ips[0])
        try:
            conn.request('GET',(p.path or '/')+('?' + p.query if p.query else ''),headers={
                'Host':host,'User-Agent':'AutoBridge-Evidence-Pilot','Accept':'text/html,text/plain','Accept-Encoding':'identity'})
            r=conn.getresponse()
            if r.status in (301,302,303,307,308):
                target=urljoin(current,r.getheader('Location',''))
                url_parts(target,allowed)  # redirect target must be separately authorized
                hops.append(dict(url=current,status=r.status,target=target));current=target;continue
            require(r.status==200,'SOURCE_ACCESS_LIMITATION:'+str(r.status))
            require(r.getheader('Content-Encoding','identity').lower()=='identity','COMPRESSED_SOURCE_NOT_ALLOWED')
            mime=r.getheader('Content-Type','').split(';')[0].strip().lower()
            require(mime in ('text/html','text/plain'),'SOURCE_MIME_NOT_ENABLED')
            length=r.getheader('Content-Length')
            require(length is None or (length.isdigit() and int(length)<=MAX_BYTES),'SOURCE_TOO_LARGE')
            raw=r.read(MAX_BYTES+1)
            require(len(raw)<=MAX_BYTES,'SOURCE_TOO_LARGE')
            try:text=raw.decode('utf-8-sig')
            except UnicodeDecodeError:require(False,'SOURCE_ENCODING_NOT_UTF8')
            if mime=='text/html':
                parser=PlainText();parser.feed(text);text=' '.join(''.join(parser.parts).split())
            require(20<=len(text)<=100000,'SOURCE_TEXT_LENGTH')
            result=dict(source_id=source['source_id'],requested_url=source['url'],final_url=current,
                publisher=source['publisher'],parent_org=source['parent_org'],tier=source['tier'],
                scope=source['scope'],retrieved_at=clock(),status=200,mime=mime,
                raw_sha256=hashlib.sha256(raw).hexdigest(),text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                resolved_ips=ips,connected_ip=ips[0],redirects=hops,text=text,
                authority_status='DECLARED_IN_APPROVED_PLAN_REQUIRES_RESEARCH_AND_REVIEW',synthetic=False)
            result['evidence_hash']=digest(result)
            return result,raw
        finally:conn.close()
    require(False,'SOURCE_REDIRECT_LIMIT')

"""Read a current, complete, hash-bound English site corpus captured by the operator."""
import hashlib
import json
import base64
import gzip
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urljoin,urlparse
from datetime import datetime
from ..contract import ROOT,require,digest
from ..live.policy import now

FOLDER='cloud_pilot/evidence/live-site-20261103'
BASE='https://autobridgetrade.top'
INDEX_FILES={'/':'index-home.html','/en/vehicles/':'index-vehicles.html','/en/guides/':'index-guides.html'}

class Index(HTMLParser):
    def __init__(self):super().__init__();self.links=set();self.parts=[];self.pagination=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);href=a.get('href','')
        if tag=='a' and href:self.links.add(href)
        if 'next' in a.get('rel','').split() or re.search(r'[?&](page|offset|start)=|/page/\d+',href):self.pagination=True
    def handle_data(self,text):
        if text.strip():self.parts.append(text.strip())

class PageText(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.skip=0;self.parts=[];self.h1=False;self.title=[]
    def handle_starttag(self,tag,attrs):
        if tag=='main':self.depth+=1
        if tag in ('script','style','noscript','nav','footer','header'):self.skip+=1
        if tag=='h1':self.h1=True
    def handle_endtag(self,tag):
        if tag=='main':self.depth=max(0,self.depth-1)
        if tag in ('script','style','noscript','nav','footer','header'):self.skip=max(0,self.skip-1)
        if tag=='h1':self.h1=False
    def handle_data(self,text):
        if self.depth and not self.skip and text.strip():self.parts.append(text.strip())
        if self.h1 and text.strip():self.title.append(text.strip())

def load(root=ROOT):
    folder=root/FOLDER
    require((folder/'manifest.json').is_file(),'CURRENT_LIVE_SITE_CORPUS_REQUIRED')
    m=json.loads((folder/'manifest.json').read_text())
    require(m.get('schema')=='autobridge-live-English-corpus/1' and m.get('target_site')==BASE+'/',
            'LIVE_SITE_IDENTITY')
    captured=datetime.fromisoformat(m['captured_at'])
    require(captured.tzinfo and 0<=(now()-captured).total_seconds()<=86400,'LIVE_SITE_CORPUS_STALE')
    xml=(folder/'sitemap.xml').read_bytes()
    require(hashlib.sha256(xml).hexdigest()==m['sitemap_sha256'],'LIVE_SITEMAP_CHANGED')
    pattern=re.escape(BASE)+r'/en/(vehicles|guides)/[^/?#]+\.html'
    urls=sorted({e.text for e in ET.fromstring(xml).iter() if e.tag.endswith('loc') and e.text and re.fullmatch(pattern,e.text)})
    require(set(m['index_pages'])==set(INDEX_FILES),'LIVE_SITE_INDEX_COVERAGE')
    listed=set();home=''
    for suffix,name in INDEX_FILES.items():
        raw=(folder/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==m['index_pages'][suffix]['raw_sha256'],'LIVE_INDEX_CAPTURE_CHANGED')
        parsed=Index();parsed.feed(raw.decode('utf-8'))
        require(not parsed.pagination,'LIVE_SITE_PAGINATION_REQUIRES_CAPTURE')
        require(sorted(parsed.links)==m['index_pages'][suffix]['links'],'LIVE_INDEX_LINK_LIST_CHANGED')
        for href in parsed.links:
            u=urljoin(BASE+suffix,href);p=urlparse(u)
            if p.netloc=='autobridgetrade.top' and re.match(r'^/en/(vehicles|guides)/.+',p.path):
                require(re.fullmatch(pattern,u),'LIVE_SITE_UNACCOUNTED_URL_PATTERN')
                listed.add(u)
        if suffix=='/':home=' '.join(parsed.parts)
    for kind in ('vehicles','guides'):
        n=re.search(r'(\d+)\s+English\s+'+kind,home)
        require(n and int(n.group(1))==sum('/'+kind+'/' in u for u in urls),'LIVE_SITE_ANNOUNCED_COUNT_MISMATCH')
    require(urls and urls==m['urls'] and set(urls)==listed,'LIVE_SITE_INVENTORY_INCOMPLETE')
    docs=[]
    for chunk in m['chunks']:
        require(re.fullmatch(r'pages-\d{2}\.json',chunk['path']),'LIVE_SITE_CHUNK_PATH')
        body=(folder/chunk['path']).read_bytes()
        require(hashlib.sha256(body).hexdigest()==chunk['sha256'],'LIVE_SITE_CONTENT_CHANGED')
        docs.extend(json.loads(body))
    require(len(docs)==len(urls) and sorted(d['url'] for d in docs)==urls,'LIVE_SITE_DOCUMENT_COVERAGE')
    archive=m.get('raw_responses',{})
    require(archive.get('path')=='raw-responses.json.gz','LIVE_SITE_RAW_ARCHIVE_REQUIRED')
    raw_bundle=(folder/archive['path']).read_bytes()
    require(hashlib.sha256(raw_bundle).hexdigest()==archive.get('sha256'),'LIVE_SITE_RAW_ARCHIVE_CHANGED')
    records=json.loads(gzip.decompress(raw_bundle));raws={r['url']:r for r in records}
    require(len(raws)==len(records)==archive.get('records')==len(urls) and set(raws)==set(urls),'LIVE_SITE_RAW_COVERAGE')
    for d in docs:
        at=datetime.fromisoformat(d['retrieved_at'])
        require(d['http_status']==200 and d['final_url']==d['url'] and d['title'] and len(d['text'])>300
                and at.tzinfo and 0<=(now()-at).total_seconds()<=86400
                and hashlib.sha256(d['text'].encode()).hexdigest()==d['text_sha256'],'LIVE_SITE_DOCUMENT_INVALID')
        record=raws[d['url']];fetched=datetime.fromisoformat(record['retrieved_at'])
        require(record['http_status']==d['http_status']==200 and record['final_url']==d['final_url']
                and fetched.tzinfo and 0<=(now()-fetched).total_seconds()<=86400,'LIVE_SITE_RAW_RETRIEVAL_INVALID')
        raw=base64.b64decode(record['raw_base64'],validate=True)
        require(len(raw)<=1500000 and hashlib.sha256(raw).hexdigest()==d['raw_sha256'],'LIVE_SITE_RAW_RESPONSE_CHANGED')
        parsed=PageText();parsed.feed(raw.decode('utf-8'))
        require(' '.join(parsed.parts)==d['text'] and ' '.join(parsed.title)==d['title'],'LIVE_SITE_EXTRACTION_MISMATCH')
    result=dict(manifest=m,documents=docs)
    result['evidence_hash']=digest(result)
    return result

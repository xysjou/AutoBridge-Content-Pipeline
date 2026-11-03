"""Read a current, complete, hash-bound English site corpus captured by the operator."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from ..contract import ROOT,require,digest
from ..live.policy import now

FOLDER='cloud_pilot/evidence/live-site-20261103'
BASE='https://autobridgetrade.top'

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
    listed={BASE+x for page in m['index_pages'].values() for x in page['links']
            if re.fullmatch(r'/en/(vehicles|guides)/[^/?#]+\.html',x)}
    require(urls and urls==m['urls'] and set(urls)==listed,'LIVE_SITE_INVENTORY_INCOMPLETE')
    docs=[]
    for chunk in m['chunks']:
        require(re.fullmatch(r'pages-\d{2}\.json',chunk['path']),'LIVE_SITE_CHUNK_PATH')
        body=(folder/chunk['path']).read_bytes()
        require(hashlib.sha256(body).hexdigest()==chunk['sha256'],'LIVE_SITE_CONTENT_CHANGED')
        docs.extend(json.loads(body))
    require(len(docs)==len(urls) and sorted(d['url'] for d in docs)==urls,'LIVE_SITE_DOCUMENT_COVERAGE')
    for d in docs:
        at=datetime.fromisoformat(d['retrieved_at'])
        require(d['http_status']==200 and d['final_url']==d['url'] and d['title'] and len(d['text'])>300
                and at.tzinfo and 0<=(now()-at).total_seconds()<=86400
                and hashlib.sha256(d['text'].encode()).hexdigest()==d['text_sha256'],'LIVE_SITE_DOCUMENT_INVALID')
    result=dict(manifest=m,documents=docs)
    result['evidence_hash']=digest(result)
    return result

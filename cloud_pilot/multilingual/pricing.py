"""Read current provider model pages without credentials; stop on any billing drift."""
import hashlib
import re
from ..contract import require,digest
from ..live.sources import url_parts,public_addresses,PinnedHTTPS,PlainText
from ..live.policy import RATES,CONTEXT,MAX_OUTPUT,timestamp

URLS={m:'https://developers.openai.com/api/docs/models/'+m for m in RATES}
CACHE_URL='https://developers.openai.com/api/docs/guides/prompt-caching'

def fetch(url,connection=PinnedHTTPS,resolver=None):
    p,host=url_parts(url,set(URLS.values())|{CACHE_URL})
    ips=public_addresses(host,**({'resolver':resolver} if resolver else {}));c=connection(host,ips[0])
    try:
        c.request('GET',p.path,headers={'Host':host,'Accept':'text/html','Accept-Encoding':'identity',
                                      'User-Agent':'AutoBridge-Pricing-Verification'})
        r=c.getresponse();require(r.status==200,'PROVIDER_PRICING_UNAVAILABLE')
        require(r.getheader('Content-Encoding','identity')=='identity','PROVIDER_PRICING_ENCODING')
        raw=r.read(1_000_001);require(len(raw)<=1_000_000,'PROVIDER_PRICING_TOO_LARGE')
        require(r.getheader('Content-Type','').startswith('text/html'),'PROVIDER_PRICING_MIME')
        parser=PlainText();parser.feed(raw.decode('utf-8'));text=' '.join(' '.join(parser.parts).split())
        return dict(url=url,retrieved_at=timestamp(),raw_sha256=hashlib.sha256(raw).hexdigest(),
                    text=text,resolved_ips=ips,connected_ip=ips[0])
    finally:c.close()

def check(model,text):
    p=RATES[model]
    for label,rate in [('Input','input'),('Cached input','cached'),('Cache writes','write'),('Output','output')]:
        value=p[rate]/1000
        # Model documentation exposes the Standard price per million tokens under these labels.
        found=re.search(r'\b'+label+r'\s*\$(\d+(?:\.\d+)?)',text)
        require(found and float(found.group(1))==value,
                'PROVIDER_PRICE_CHANGED:'+model+':'+rate)
    require('1,050,000 context window' in text,'PROVIDER_CONTEXT_CHANGED')
    require('128,000 max output tokens' in text and MAX_OUTPUT<=128000 and CONTEXT==1050000,'PROVIDER_OUTPUT_BOUND')
    require(('30-minute retention' in text if model=='gpt-6.1-terra' else '1.25x the uncached input token rate' in text)
            and '272K input tokens' in text
            and '2x input and cache rates' in text and '1.5x output' in text,'PROVIDER_BILLING_PROFILE_CHANGED')
    return True

def verify(snapshot,journal,fetcher=fetch):
    receipts={}
    for model,url in URLS.items():
        receipt=fetcher(url);check(model,receipt['text']);receipts[model]=receipt
    caching=fetcher(CACHE_URL)
    require('default 30-minute lifetime' in caching['text'] and '1.25' in caching['text'],'PROVIDER_CACHE_PROFILE_CHANGED')
    evidence=dict(verified_at=timestamp(),billing_profile='global Standard / 30m / no tools / text',
                  prices_hash=digest(snapshot),models=receipts,cache_policy=caching)
    journal.checkpoint('provider-pricing:'+digest(evidence),evidence)
    return evidence

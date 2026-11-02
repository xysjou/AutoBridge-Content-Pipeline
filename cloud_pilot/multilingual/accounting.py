"""Keep long response text outside the small shared ledger, without losing usage."""
import copy
from ..contract import require,digest
from ..live.ledger import Journal
from ..live.responses import Responses

class ResponseJournal(Journal):
    def commit(self,event_id,payload):
        if payload.get('kind')=='result':
            payload=copy.deepcopy(payload)
            response=payload['response']
            require(isinstance(response.get('text'),str),'RESPONSE_TEXT_MISSING')
            require(hasattr(self.store,'save_artifact'),'DURABLE_RESPONSE_ARCHIVE_REQUIRED')
            ref=self.store.save_artifact(dict(text=response['text']))
            response['text']=''
            response['text_artifact']=ref
            # Response identity, exact usage and settled cost remain atomically in the ledger.
        return super().commit(event_id,payload)

class DurableResponses(Responses):
    def _parse(self,response):
        if response.get('text_artifact'):
            response=copy.deepcopy(response)
            archived=self.journal.store.load_artifact(response.pop('text_artifact'))
            require(set(archived)=={'text'} and isinstance(archived['text'],str),'RESPONSE_ARCHIVE_SHAPE')
            response['text']=archived['text']
        return Responses._parse(response)

class CountedResponses(DurableResponses):
    """Reserve worst cache write and max output against the provider's exact input count."""
    def bound(self,request):
        payload={k:v for k,v in request.items() if k in ('model','input','instructions','tools','text','reasoning')}
        status,result=self.api.request('POST','/v1/responses/input_tokens',payload)
        require(status==200 and result.get('object')=='response.input_tokens','PROVIDER_TOKEN_COUNT_UNAVAILABLE')
        n=result.get('input_tokens')
        from ..live.policy import CONTEXT
        require(type(n) is int and 0<n<=CONTEXT,'PROVIDER_TOKEN_COUNT_INVALID')
        bound=min(CONTEXT,n+1024)
        proof=dict(endpoint='/v1/responses/input_tokens',request_hash=digest(request),
                   count_payload_hash=digest(payload),response=result,input_bound=bound)
        self.journal.checkpoint('token-count:'+digest(request),proof)
        return dict(input_bound=bound,token_count_hash=digest(proof),counted_request_hash=digest(request))

class AnchoredStore:
    """Permit fixes a ledger floor; a one-run lease plus in-process monotonicity prevents replay."""
    def __init__(self,store,anchor):self.inner=store;self.anchor=anchor;self.seen=None
    def read(self):
        data,token=self.inner.read();events=data['events'];n=self.anchor['events_count']
        require(len(events)>=n and (events[n-1]['hash'] if n else None)==self.anchor['last_event_hash'],
                'PROTECTED_LEDGER_FLOOR_ROLLBACK')
        settled=sum(e['payload']['cost'] for e in events[:n] if e['payload']['kind']=='result')
        require(settled==self.anchor['settled_nano_usd'],'PROTECTED_OPENING_SPEND_MISMATCH')
        receipts=[dict(response_id=e['payload']['response']['id'],model=e['payload']['response']['model'],
                       usage_hash=digest(e['payload']['response']['usage']),cost=e['payload']['cost'])
                  for e in events[:n] if e['payload']['kind']=='result']
        require(receipts==self.anchor['reconciled_receipts'],'PROTECTED_OPENING_RECEIPTS_MISMATCH')
        if self.seen is not None:require(events[:len(self.seen)]==self.seen,'IN_RUN_LEDGER_ROLLBACK')
        import copy
        self.seen=copy.deepcopy(events)
        return data,token
    def cas(self,expected,data):
        self.read();result=self.inner.cas(expected,data)
        import copy
        self.seen=copy.deepcopy(data['events']);return result
    def __getattr__(self,key):return getattr(self.inner,key)

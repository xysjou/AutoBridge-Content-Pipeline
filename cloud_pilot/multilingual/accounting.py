"""Keep long response text outside the small shared ledger, without losing usage."""
import copy
from ..contract import require
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

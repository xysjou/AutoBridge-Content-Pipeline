"""Deliberately no HTTP clients, SDK imports, credential reads, or paid calls."""
from .contract import GateError

class OpenAIResponsesDisabled:
    def create(self, **request):
        raise GateError("REAL_API_DISABLED: dedicated restricted project key, current price validation, durable live CAS transport and explicit next-stage approval required")

class SourceRetrievalDisabled:
    def retrieve(self, url):
        raise GateError("NETWORK_RETRIEVAL_DISABLED: authorized URL allowlist and SSRF/redirect/size policy required")

class SearchProviderDisabled:
    def search(self, query):
        raise GateError("SEARCH_DISABLED: provider and cost must be disclosed and approved first")

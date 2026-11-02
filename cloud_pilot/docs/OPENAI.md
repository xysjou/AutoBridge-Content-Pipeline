# Official API documentation snapshot

Retrieved in Work Cloud on 2026-11-02; snapshot recorded at 2026-11-02T03:55:04Z (11:55:04 Asia/Shanghai). Account-level availability is UNVERIFIED. These are API identifiers fetched from official model pages, not inferred from Work UI labels.

|Proposed stage|API ID|Standard input / output per 1M tokens|Cached input|12h cache-write ceiling used by mock|
|---|---|---|---|---|
|Research extraction|`gpt-6-luna`|$0.10 / $0.50|$0.01|$0.25|
|Writing; separate independent Review request|`gpt-6.1-terra`|$1.00 / $5.00|$0.05|$2.50|

Model pages' Snapshots sections currently show only the above identifiers, not dated immutable snapshot IDs. Do not invent a date suffix. Capture the returned model identifier when real calls are later approved. Both pages document Responses support and reasoning effort; the tentative profile is standard, short context, text only, no tools, medium reasoning, store=false. This is a proposal, not a tested live request.

Sources:

- https://developers.openai.com/api/docs/models/gpt-6-luna — model ID, snapshot display, price and limits.
- https://developers.openai.com/api/docs/models/gpt-6.1-terra — model ID, snapshot display, price and limits.
- https://developers.openai.com/api/docs/pricing — current table, cache-write rates and tool fees.
- https://developers.openai.com/api/docs/guides/reasoning — reasoning consumes output tokens; max_output_tokens includes it. Incomplete responses can still be billed.
- https://developers.openai.com/api/docs/guides/rbac — least-privilege project roles and key permissions; Responses API, model request and models-read permissions.
- https://developers.openai.com/api/docs/guides/spend-limits — alerts do not stop traffic; optional project hard limits can have delayed enforcement and slight overshoot.

Search provider: NONE enabled. URL retrieval would use an explicitly authorized HTTPS fetcher, not a search engine. If discovery is later needed, a possible provider is OpenAI Responses web_search: the fetched pricing page lists $10/1000 calls plus search-content model tokens. That is not included in the mock's tool-free reservations; enabling it requires a new cost model and approval first. No separate Firecrawl or other search provider is configured.

Price validity must be refreshed before the first real call and on subsequent runs; unknown/stale price state must stop the adapter. No account key or availability check was attempted in M1.

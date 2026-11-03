# Stage 2 — implemented adapters, first real request still locked

The existing M1 contracts, synthetic v1 artifacts and mock ledger remain immutable.
This package adds real HTTP adapters and a separate **real-dollar** journal under
the same program ID. It does not start a service or read any credential on import.

Actual branch entrypoint, executable in Work Cloud now:

```sh
python -m cloud_pilot.live preflight
```

This is deliberately offline. It checks local pricing, baseline and intake and
reports pending authorization/runtime/account gates. It reads no key and makes
zero network requests. The real entrypoint is implemented but cannot run without
an approved plan, a current price snapshot and an exact-code permit:

```sh
python -m cloud_pilot.live execute --plan <approved-plan.json> --prices <current-prices.json> --permit <approved-permit.json>
```

No CLI option accepts a secret value. Credentials are read only after plan/rule/
price/code/approval checks. Current `plan.pending.json` is empty and the permit
example is disabled; neither is an approved real research package.

## Responsibilities

- `sources.py`: HTTPS exact-URL whitelist, public-IP validation, pinned TCP/TLS
  connection with original hostname, redirect re-authorization, MIME/encoding/
  size/time limits, raw body hash and immutable GitHub evidence archive. UTF-8
  HTML/plain text only. PDF/binary/JS-only pages fail rather than invent content.
- `responses.py`: real Responses POST format, separate stateless requests per
  Research/Writing/Review, current full canonical rules, standard global endpoint,
  explicit 30m cache TTL, tools=[], store=false, bounded output. No search provider.
- `stages.py`: source identity/scope checks, literal evidence quotes, fact/claim
  mappings, numeric protection, language-length/public-field gates, full-body
  similarity, distinct reviewer response identity and exact article/evidence hashes.
  Reviewer verdict is a real separate request when enabled; the code never assigns
  itself an editorial PASS. English draft review never equals production approval.
- `ledger.py` + `http.py`: real GitHub Contents API transport, current blob-SHA CAS,
  append-only history, one fixed program ledger, atomic response+usage accounting,
  content-addressed immutable stage checkpoints and durable halt reasons. Large evidence stays in immutable GitHub artifacts; the small ledger binds their hashes instead of duplicating documents. Only isolated branches and
  cloud_pilot/live_artifacts paths can be written. Delivery can create draft PRs
  onto the integration branch; no CURRENT or site operation exists.
- `engine.py`: source failure stops model stages; research failure stops writing;
  separate review may request at most two revisions. Crash/restart reuses durable
  results. Failed delivery reuses the article/review without another model call.

## Program cost and uncertainty

USD3 is for the **whole real API pilot**, not per article/stage/run. The old mock
USD0.021 is not real money; genesis links its immutable hash and carries actual
prior spend of zero. `execute` cannot initialize, replace or reset the journal.

No guessed characters-to-token conversion is used. Each call reserves the entire
1,050,000-token context at the documented long-context 30m write rate plus all
8,000 allowed output tokens at the long-context output rate. This is USD2.685 for
Terra and USD0.2685 for Luna. Only one unresolved program request is allowed.
After a complete response the ledger charges exact input/cache-read/cache-write/
output usage; reasoning is a subset of output. Missing cache-write or other usage
fields cause an uncertainty hold. This intentionally can stop before USD3 actual
spend if the next worst-case reservation no longer fits. It never borrows future
budget on an optimistic token estimate.

After a durable sent marker, every timeout, HTTP error or unconfirmed persistence
retains the reservation and halts new calls. No blind SDK/HTTP retries. A crash
before the sent marker may be released only by a separate operator-authorized
reconciliation with evidence hashes. At most three proven-not-sent attempts;
uncertain sent attempts are never automatically released or resent. The run may
need provider/account evidence and operator intervention; this is a fail-closed
recovery path, not a false claim that every remote outcome is knowable.

## What is verified and what remains unverified

Offline tests use synthetic DNS/HTML/HTTP/model replies and in-memory GitHub CAS.
They exercise actual adapter and orchestration code, concurrency, crash cases,
all six requests for two fake articles, revisions and reruns without network.
They do not demonstrate account model availability, live API field acceptance,
source factual authority, natural article quality or a production deployment.
All original M1 tests and immutable synthetic artifacts remain unchanged.

Official model/pricing snapshots are in runtime/prices-20261102.json. They expire
in 24h; price/model/rule changes invalidate the permit. Both official model pages
currently show aliases rather than dated immutable snapshot IDs; unknown returned
model IDs fail closed. See ../docs/STAGE2_HANDOFF.md for activation blockers.

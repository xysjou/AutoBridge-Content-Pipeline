# M1 design and explicit limits

Canonical wire version: `autobridge-cloud-pilot/1.0`; `contract.py` is the executable contract. `schema.json` describes shared envelopes. No stage relies on a different chat's memory. Every packet binds baseline SHA, rule-file hashes, Research 1.1/Writing 1.3 versions, article ID/version, locale, synthetic flag, and permanently false approval flags.

|Module|Input|Output|Boundary|
|---|---|---|---|
|Research|synthetic fixture + pinned history|fact/source packet + provenance hash|scope, source identity, parent organization, year/generation/trim/powertrain/cycle, per-claim binding, allowed/blocked facts|
|Writing|validated research JSON|immutable English article packet + content hash|literal fixture rendering only; no research mutation or self-review approval|
|Review|article + research + history JSON|independent deterministic report + review hash|recompute bindings and body hash; reject writer self-evaluation; full-body five-gram comparison|
|Delivery/orchestrator|hash-bound mock report|draft PR request + journal transitions|isolated branches and pilot paths; no publication, main push, CURRENT or approval promotion|

`cli.py` supports standalone research/writing/review processes. `pilot.py` creates two short English test articles (465 and 448 words). These deliberately remain below formal Writing minimum and cannot pass production. Synthetic source confidence/tier fields exercise the contract; they do not assert that fabricated organizations are real authorities.

The literal renderer permits a stronger deterministic equality check than a future LLM paraphrase writer. It is not a semantic source-entailment system. Real writing, standards/legal scope review, image rights, URL liveness, 12 full locales and professional/semantic review remain disabled/pending. No machine PASS is a language-quality PASS.

## Durable state

`cloud_pilot/state/program-journal.json` is one program-wide, hash-chained journal checked into the integration branch. It contains state, cost and retry events; no per-chat/per-run budget resets. `LocalFileCAS` uses a process file lock, expected state digest, fsync and atomic replacement. `GitHubCAS` fixes the state path and branch and requires an injected Contents API transport using the current blob SHA as the write precondition. Its lease contract is tested offline; no real autonomous GitHub state transport is activated in M1. Work Cloud's authorized GitHub connector persists the milestone checkpoint.

A missing/corrupt state is fatal; initialize is explicit and exclusive. Append verifies the complete history and preserves its prefix. Idempotency keys reject changed payloads. Conflicting CAS writes fail, requiring reread/recalculation rather than blind retry. Git retains immutable history; repository administrators can rewrite Git history, so this is not a tamper-proof external accounting authority.

Transitions: NEW -> RESEARCH_READY/RESEARCH_FAILED -> WRITTEN -> MOCK_REVIEW_PASS, REVISION_REQUIRED, NEEDS_RESEARCH or REJECTED. A pass can reach only DRAFT_PR_PREPARED. Revision/research-return loops create v2 then v3; a third revision is blocked. Failure before collection consumes no simulated model budget. Production states HUMAN_REVIEWED/PUBLISH_APPROVED do not exist.

## Cost controller

The program cap is US$3 across both articles, stages, retries and reruns. Integer nanodollars avoid floating-point decisions. Reservations precede simulated calls and include all bounded input/output. Input <=20,000; output <=6,000 including reasoning; no tools/search, long context, regional premium or fast tier is permitted by the intended real profile. Conservative input reservation uses the highest documented 12-hour cache-write rate, even though no explicit cache writes are planned.

Known usage records input/output/reasoning/cached/cache-write counts. Reasoning is part of output and is not double-counted. Conservative settlement may overstate model cost; it is separately marked mock, not an invoice. Timeout/uncertain or unknown-usage outcomes retain the full reservation and block new program calls; no automatic uncertain-failure retry. Known failures allow at most 3 attempts total. Missing price, usage, state, or token bounds fail closed. No real USD3 guarantee is asserted until current-price checking, tokenization bounds, live CAS transport, crash recovery and controlled API usage reconciliation are implemented and independently tested. M1 makes zero API calls.

## Repository rules preserved

The canonical Skills are read and hashed, never replaced by this prototype. For conflicts between controlled writing patches and the stricter permanent research-file ownership boundary, Writing does not mutate Research at all. Startup/end main synchronization is performed read-only; all actual writes stay on isolated branches, as explicitly authorized by the user. SKILL_IMPACT_CHECK: no new editorial rule confirmed; no Skill/LESSONS modification. Mock implementation checks are not promotions of new editorial policy.

## Before real operation

Implement and review authenticated GitHub CAS transport with a single durable live ledger, retry reconciliation and artifact+state atomicity. A source retriever must restrict authorized HTTPS origins, reject private/link-local/reserved destinations, recheck DNS and every redirect, impose MIME/size/time limits, and store retrieval identity/date/hash. Source text is untrusted data, never execution instructions. Unknown or blocked retrieval stops Research. Semantic intent dedup against all current articles remains a separate human/AI gate. Search is off until provider and full cost are approved.

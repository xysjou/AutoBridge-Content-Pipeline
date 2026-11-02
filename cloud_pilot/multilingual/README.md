# AutoBridgeTrade multilingual API pilot — reviewable implementation

This extension reuses the existing English Research → Writing → independent Review
engine and the **same** USD3 whole-program ledger. It adds complete localization
and independent model review for `en fr de es pt ja ko vi th id ar zh`, plus
S05-format Markdown exports. No model, key, source, GitHub write or service is
contacted merely by importing modules or running the default command.

## What is implemented

- `python3 -m cloud_pilot.multilingual preflight`: offline checks and explicit
  activation blockers; it does not read application credentials.
- `account-check`: separately approved protected-runner GET requests for the two
  configured model metadata endpoints. It cannot issue generation POST requests.
- `execute`: validates plan, price snapshot, exact code SHA, approved main SHA,
  target domain, 12 locales, phase and protected permit digest before reading keys.
  Research uses Luna medium; writing/localization uses Terra medium; independent
  English/locale review uses Terra high. Account availability and live acceptance
  are not established by offline tests.
- Two real topics and twelve source URLs are populated in
  `runtime/trade-two-articles.plan.json`: a China-market 2026 Q05 BEV reference and
  a complete refrigerated-truck buying guide. Earlier chat-authored draft text is
  **not** passed off as API-generated content or used to fabricate response IDs.
- Exact public-URL authorization, public-IP resolution and pinned TLS are reused.
  The new bounded fetcher accepts UTF-8 and declared GB2312/GBK/GB18030. It does not
  bypass login, CAPTCHA or blocking. A JavaScript-only shell, unsupported format,
  unavailable source or scope mismatch stops the pipeline; browser rendering,
  PDF extraction and automatic daily topic discovery are not implemented here.
- Localization preserves all sections, FAQ, claim mapping, numeric tokens and
  verified URL strings. Chinese requires at least 1200 Han characters. Script,
  metadata and hash checks supplement a separate target-language model review;
  they do not prove native-language quality by themselves.
- Each locale gets its own immutable article/review checkpoints, at most two
  revisions, and an independent response ID. A retry uses saved responses and
  checkpoints. Unknown sent-request outcomes retain their reservation and stop;
  there is no blind resend.
- Response text is archived separately before the atomic usage settlement. The
  small shared ledger retains model, response ID, usage, cost and artifact reference.
  This avoids filling the ledger with 24 full articles and repeated checkpoints.
- Only a 24-file bundle can be reported as the full multilingual draft result.
  `execution_phase: english` reports only an intermediate English milestone.
  The locale files remain review drafts, with human approval, image rights and
  live-site technical acceptance explicitly pending.

## Output and audit evidence

The existing English engine creates isolated draft PRs. Multilingual Markdown is
written immutably under `cloud_pilot/live_artifacts/multilingual/<English hash>/` on
the integration branch. The final report maps all 24 filenames to blob hashes,
article hashes and exact independent-review hashes. Each raw API response text is
an immutable artifact; its actual response ID, returned model and usage are bound
to the original ledger event. Re-running a completed operation makes no new model
request. Website, `CURRENT`, approved historical versions and main are never written
by this execution code.

## Budget boundary

The old USD3 cap is unchanged and is **not** reset when moving from English to full
localization. Conservative per-request reservations still use the old maximum
context policy. Consequently, the cap can stop the run well before USD3 is actually
spent or before all 24 files exist. No complete-24-within-USD3 claim is made.
Changing the cap or reservation policy requires a separately reviewed change and
approval; the implementation does not bypass the budget to make a test succeed.
Synthetic tests include both a complete low-usage fixture and a fixture that must
stop because its next worst-case reservation does not fit. Fixture usage is not a
real-world estimate.

## Concrete activation sequence — still not performed

1. Review and merge this code **into the integration branch**, not main. Validate
   the proposed sources and obtain an independent semantic-duplicate review of
   the two proposed topics against existing content. The shipped intake keeps
   `semantic_dedup_status: PENDING`; it is deliberately not self-certified.
2. After explicit bootstrap approval, install the reviewed file
   `runtime/multilingual-manual.yml.template` as
   `.github/workflows/cloud-pilot-manual.yml` on the default branch and the
   integration branch. The template is manual-only, defaulting to offline preflight;
   neither live nor account-check is enabled by default. Existing PR #3 is an old
   disabled bootstrap and must not simply be switched on as if it were this version.
3. Set `AUTOBRIDGE_APPROVED_CODE_SHA` to the reviewed immutable implementation SHA.
   Preserve the existing protected environment `autobridge-pilot`, its reviewer,
   disabled administrator bypass and exact integration-branch restriction. Keep
   `OPENAI_API_KEY` in the existing environment secret; never put it in code/chat.
4. For an approved account check only, enable `AUTOBRIDGE_ACCOUNT_CHECK_ENABLED`
   and manually choose `account-check`. Its two metadata GETs do not establish
   that a generation call or its response fields will work. Retain the actual result.
5. Prepare an immutable **separate control commit** containing exactly these data
   files under `cloud_pilot/runtime/control/`:
   - `approved-plan.json`: real intake with independent dedup evidence, target,
     locales and approved phase (`english` first, `full` only when approved).
   - `approved-prices.json`: current verified rates, valid for 24 hours.
   - `approved-permit.json`: exact code SHA, approved **post-bootstrap main SHA**,
     hashes of the plan/prices/rules, phase, target, locales, expiry, whole-program
     USD3 cap and truthful account/runtime verification. Start from the disabled
     example; setting it true requires explicit authorization.
   The control commit is separate from the code commit so that the permit can
   refer to the code's actual SHA without an impossible self-reference.
6. Set the control commit in `AUTOBRIDGE_APPROVAL_COMMIT`, and store the canonical
   `digest(permit)` in the protected secret `AUTOBRIDGE_LIVE_APPROVAL_SHA256`.
   Only after paid-run approval enable `AUTOBRIDGE_LIVE_ENABLED=true` and manually
   run `execute` from the integration branch. Default-branch bootstrap can change
   main's SHA: the approved main SHA and the immutable content baseline are checked
   separately, rather than making the old baseline-SHA gate impossible to satisfy.
7. Inspect the real response/usage ledger and source/review artifacts after the
   English phase. Approve a separate full-phase control revision only if appropriate.
   The existing ledger and already-finished English operations are reused. Missing
   billing fields, unavailable models, bad factual sources or exhausted budget stop
   with evidence; they are not replaced by chat-written articles.

No schedule is installed. None of these steps publishes the resulting drafts to
`autobridgetrade.top`; that requires a separate approved site integration.

## Offline verification

```sh
python3 -m unittest discover -s cloud_pilot/multilingual/tests -v
python3 -m unittest discover -s cloud_pilot/stage2_tests -v
python3 -m unittest discover -s cloud_pilot/tests -v
python3 -m cloud_pilot.multilingual preflight
```

The new test suite blocks socket connections. The end-to-end fixture routes two
synthetic English articles and all 22 synthetic localizations through the real
Responses adapter with mocked HTTP replies (50 generation responses, not 50 real
requests). The fixture asserts 24 exports and zero additional calls on resume.
The 47 stage-2 and 41 original tests are retained unchanged. Passing these checks
does not establish real source access, live model availability or editorial quality.

Official references checked 2026-11-02:

- https://developers.openai.com/api/reference/overview
- https://developers.openai.com/api/docs/guides/structured-outputs
- https://developers.openai.com/api/docs/guides/prompt-caching
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://developers.openai.com/api/docs/models/gpt-6.1-terra
- https://developers.openai.com/api/docs/pricing

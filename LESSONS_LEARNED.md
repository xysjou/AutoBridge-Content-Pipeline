# AutoBridge Content Pipeline — Lessons Learned (Permanent Rules)

These are durable editorial/sourcing rules that correct recurring fact-boundary failures. Every research and writing stage MUST apply them. When a rule is invoked, record it in the batch QA report.

> **Canonical location:** `/LESSONS_LEARNED.md`. If this file is migrated to `/rules/LESSONS_LEARNED.md`, the migrated formal version is authoritative. **No writing may begin until this file has been read for the current batch.**

---

## PART 0 — PERMANENT LEARNING GATE (MANDATORY PROJECT RULE)

*Installed by project-owner directive; permanently in force. This is a governance rule, not a candidate lesson.*

### 0.1 Mandatory startup sequence — before ANY new batch is written
Execute in this exact order, every time:
1. **Sync the shared GitHub repo to latest** (`git pull`); never start from stale local data.
2. **Read `LESSONS_LEARNED.md`** (or `/rules/LESSONS_LEARNED.md` if migrated) in full.
3. Read the current **Research Fact Sheets**.
4. Read the **Source Logs**.
5. Read that day's **Daily Manifest**.
6. Run a **PRE-WRITING ERROR CHECK** against every historical LESSON below.
7. Only after confirming no historical error is triggered may article writing begin.

### 0.2 Historical errors are permanently binding
The rules below are **MANDATORY PROJECT RULES**, not suggestions. Issues already confirmed by independent review must never recur. Work is always built **on top of** the previously confirmed error rules; the goal is to remember the confirmed *error patterns*, not just the previous batch. A given systemic error may not appear a second time.
- `MODEL_ALIAS_REQUIRES_OEM_PROOF` → any "overseas version / export name / equivalent model / 对应车型 / 同款" requires explicit OEM proof; without it, no SAME_MODEL relationship.
- `SOURCE_MARKET_PATH_CHECK` → every official source is checked across URL region code, country selector, page country, dealer entity and the Market tag; never again e.g. Bahrain→UAE, South Africa→Global, Hong Kong→Europe.
- `PRIMARY_SOURCE_SCOPE_MUST_MATCH` → even a government source is scope-checked (e.g. **light vehicle must not be extrapolated to commercial truck**); "official" never grants unlimited scope.

### 0.3 Repeated-error penalty (mandatory)
If a new article repeats a systemic error already recorded in this file:
- It **must not** be marked `FACT_SOURCE_PASS`; set **`FACT_SOURCE_FAIL`**.
- Record on the article/QA record: **`REPEATED_ERROR = TRUE`**, **`LESSON_ID = <the violated rule>`**, **`SEVERITY = HIGH`**.
- The article **must not enter Codex final review** until corrected and re-QA'd.

### 0.4 New-error learning (candidate, not self-promoted)
After writing, run **SELF-REVIEW** for any *new* systemic problem that could recur in future batches.
- If found, output a **`NEW_LESSON_CANDIDATE`** (with evidence and proposed rule).
- The writing AI **must not promote a candidate to a permanent rule itself**. It enters `LESSONS_LEARNED.md` only **after independent review confirms it**.
- Rules installed directly by the project owner (like this Gate) are already confirmed and are written in as permanent, not as candidates.

### 0.5 Pre-writing checklist (copy into each batch QA)
`[ ] repo pulled  [ ] LESSONS_LEARNED read  [ ] Fact Sheets read  [ ] Source Logs read  [ ] Daily Manifest read  [ ] each LESSON checked  [ ] no historical error triggered → writing allowed`

---

## LESSON: SOURCE_MARKET_PATH_CHECK
A source's **Market must match the real country/region of its URL/page** — never the market we expected or hoped for.
- The URL region code (e.g. `en-bh` = Bahrain, `en-ae` = UAE, `/za/` = South Africa, `/hk/` = Hong Kong), the dealer/entity named on the page, and the country selector can conflict.
- When they conflict, re-verify the actual market before tagging; do **not** default to "UAE / Europe / Global" by assumption.
- A regional/global page must be labelled "Regional (country X)" with its true scope, not upgraded to a broader market.
- Trigger example (2026-09-02 R3): `byd.com/en-bh/car/qin-plus-dmi` was mislabelled "UAE"; `en-bh` is **Bahrain**.

## LESSON: MODEL_ALIAS_REQUIRES_OEM_PROOF
"Export name", "overseas version", "same car", "equivalent/对应车型" are **model-identity facts** and require **explicit OEM proof**.
- Shared platform, identical powertrain, similar appearance, a media nickname, or a parameter-site comparison do **not** establish SAME_MODEL.
- Without explicit OEM statement of the alias, the relationship is at most **RELATED_MODEL ≠ SAME_MODEL**, and specs must not be presented as 1:1 equivalents (including per-trim/range equivalence).
- Regional reference specs may be matched only on a clearly stated dimension (e.g. same *nominal* battery capacity) with an explicit non-equivalence caveat.

## LESSON: HS_FIRST_FOR_IMPORT_RULES
Commercial-vehicle import rules MUST be built in this order:
**exact HS code → applicable technical regulation → required certificate/tariff type → shipment/customs process.**
- Never write a single national "uniform process" first and add "different models may vary" as an afterthought.
- Headings 87.01 / 87.04 / 87.05 / 8716 and their subheadings can map to different technical regulations, different certificate forms (COC/QM/self-declaration/vehicle-specific process) and different tariff lines.
- A passenger/light-vehicle rule, calculator or rate must never be presented as the commercial-truck rule; check both the authority AND the scope of the source.

## LESSON: FIRST_HAND_EXPERIENCE_MUST_BE_TRUE
Do **not** invent first-hand AutoBridge operations to manufacture E-E-A-T.
- Claims such as "AutoBridge produces / runs / checks / our sourcing desk…" are allowed only for actions AutoBridge genuinely and routinely performs, with real operational evidence.
- Where there is no such record, use editorial/recommended framing: "AutoBridge's recommended sourcing method…", "This guide recommends…", "Our editorial procurement framework…".
- The site's standing evidence boundary (document research; no first-hand test/drive/import/teardown claim) must never be broken by body copy.
- Internal links must point only to pages that actually exist on the live site (no fabricated author/policy URLs).

## LESSON: PRIMARY_SOURCE_SCOPE_MUST_MATCH
An "official/primary source" is authoritative **only within its stated scope**. Check SOURCE AUTHORITY **and** SOURCE SCOPE.
- An official document may cover only: light vehicles, passenger cars, a specific market, a specific trim, a specific transaction, or a calculator's defined category.
- "Official" does not license extrapolation to other vehicle classes, markets or transactions (e.g. a ZATCA light-vehicle 5%/15% calculator is not a commercial-truck tariff).
- Tag the scope in the source row; keep out-of-scope use as a verification item, not a fact.

---

### Confidence vocabulary (binding)
- **VERIFIED** — manufacturer OEM site, government/regulator, standards body, or formal official technical document (scope matched).
- **CROSS_CHECKED** — two or more independent reliable sources agree, but no primary/official first-hand source.
- **SINGLE_SOURCE** — one non-official source.
- **UNVERIFIED** — cannot be reliably confirmed.
Two agreeing media sites are never automatically VERIFIED.

### Mandatory/legal wording
Use **must / prohibited / required** only where a cited regulation or official document directly states the obligation. Otherwise use risk-control/recommended language ("reconcile…", "do not assume…", "confirm in writing…").

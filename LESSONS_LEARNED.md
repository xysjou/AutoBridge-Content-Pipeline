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

## PART 1 — DAILY REVIEW PERMANENT UPGRADE (installed by project-owner directive 2026-09-03)

*Installed directly by the project owner on 2026-09-03; already confirmed, therefore permanent (not NEW_LESSON_CANDIDATE). In force for every Research batch from 2026-09-04 onward. These rules sit ON TOP OF PART 0 and the LESSONs above and never weaken them.*

### 1.1 Source tiers (binding search order)
- **T1 — Primary / Official (highest):** OEM official site, official configuration PDF / technical document, MIIT/工信部, government, customs, tax authority, transport authority, certification body, standards organization, UNECE, formal law/regulation database. May be tagged **VERIFIED only when SOURCE_AUTHORITY=PRIMARY AND SOURCE_SCOPE=MATCHED**.
- **T2 — Reliable structured database:** 懂车帝 / 汽车之家 / 360che / 卡车之家 and comparable professional databases. For model discovery, version confirmation and cross-checking. Two agreeing T2 sources reach **CROSS_CHECKED at most — never VERIFIED**.
- **T3 — Industry / specialist:** trade press, certification-body articles, specialist logistics firms, industry associations, specialist insurers. Usable for background / process / case study only, after checking scope.
- **T4 — Weak source:** forums, SEO sites, anonymous reposts, short video, 抖音百科 / Douyin baike, sales ads, unsourced dealer content. **SEARCH LEAD ONLY — never the sole basis of a key fact.**

### 1.2 Article-level research verdict (replaces a single READY flag)
Every package receives exactly one of:
- **RESEARCH_PASS** — key facts have sufficient reliable sources; may move to Writing AI.
- **RESEARCH_CONDITIONAL** — writable, but specific fields must NOT be used as facts; a **BLOCKED_FACTS** list is mandatory, plus FACTS_ALLOWED_IN_BODY and FACTS_NOT_ALLOWED_IN_BODY.
- **RESEARCH_FAIL** — the core search intent's key facts cannot be verified; must NOT move to Writing AI. Prefer continued official-source search; if still missing, replace with a RESERVE topic. Never pass on the strength of many dealer/media articles.
- Flags: `OFFICIAL_SOURCE_REQUIRED = TRUE/FALSE`, `OFFICIAL_SOURCE_FOUND = TRUE/FALSE`.
- Writing-AI handover is mandatory and must include: FACT SHEET, SOURCE LOG, CONFIDENCE STATUS, CONFLICT LIST, TIME-SENSITIVE LIST, OFFICIAL SOURCE STATUS, FACTS ALLOWED IN BODY, FACTS NOT ALLOWED IN BODY (what may be stated as fact, what may only be "confirm before purchase", what must not enter the body at all).

### 1.3 Source integrity (binding)
- `SOURCE_INTEGRITY_FAIL` if the displayed Source Name does not match the real URL/publisher (e.g. Name = 卡车之家 but URL = toutiao.com; Name = "Government Official" but URL is a media repost). The recorded Organization MUST match the actual publishing entity of the URL.

### 1.4 Full confidence vocabulary (fact-level, six labels)
The binding set is **VERIFIED / CROSS_CHECKED / SINGLE_SOURCE / CONFLICT / UNVERIFIED / TIME_SENSITIVE**. Confidence is attached to EACH FACT, never to the whole article. Price, regulation, tax rate, certification, export eligibility and model availability are TIME_SENSITIVE and require current confirmation.

### LESSON: CURRENT_STANDARD_VERSION_GATE
Any article touching **IMDG, UNECE, EU Regulation, GSO, ISO, GB/T, QC/T, customs rules, dangerous-goods transport rules, certification standards** must, before RESEARCH_PASS, confirm for the cited standard: **CURRENT_VERSION, CURRENT_AMENDMENT, EFFECTIVE_DATE, MANDATORY_FROM, PRIMARY_SOURCE_URL**. Using an outdated-edition second-hand article as the basis for the current rule is prohibited; if the current version is not confirmed, RESEARCH_PASS = FALSE.
- Worked case: **IMDG Amendment 42-24 is mandatory from 2026-01-01.** A lithium-ion-battery-powered vehicle is classified **UN3556 — Vehicle, Lithium Ion Battery Powered**; the old generic **UN3171 must no longer be used as the current classification** for such vehicles.

### LESSON: EVIDENCE_CEILING_IS_NOT_RESEARCH_PASS
Writing "no official primary source captured", "verify officially", or citing an "evidence ceiling" does NOT substitute for research. If the core search intent involves **regulation, tax rate, import restriction, registration, certification, mandatory standard, dangerous-goods transport, vehicle age limit, or a legal obligation** and the core fact lacks the competent authority's Primary Source, the verdict MUST be **RESEARCH_CONDITIONAL or RESEARCH_FAIL — never RESEARCH_PASS**. First keep searching for the official source; if it still cannot be found, replace the topic from RESERVE.

### LESSON: CONFIDENCE_IS_FACT_LEVEL
CROSS_CHECKED is not an article-level label. **THE SAME FACT** must be supported by two or more independent reliable sources before it is CROSS_CHECKED. One source supporting "2 SUVs" and another supporting "4-rack loading" do not cross-check each other. A single fact with one non-official source = SINGLE_SOURCE. A secondary legal portal that merely restates a correct law is still NOT VERIFIED; media — even authoritative state/industry media or a news agency — is not auto-upgraded to VERIFIED by its institutional background.

### LESSON: REUSE_STRONGEST_VERIFIED_SOURCE
Before new research, search the historical Fact Sheets, Source Logs, LESSONS_LEARNED and reviewed articles for an already-captured official source on the same regulation/standard. If the repository already holds a MOFCOM / government / OEM / standards-body official source, it MUST be reused and must NOT be downgraded to a Toutiao / Sohu / freight-forwarder / media source. Example: for 2026 BEV export licensing the repo already holds MOFCOM/MIIT/GAC/SAMR official Announcement No.54; future related articles must reuse that official source first.

### LESSON: DEPENDENCY_UPDATE_PROPAGATION
When a shared fact or standard changes, the ENTIRE current batch must be searched for dependences — e.g. UN3171 → UN3556 must not be fixed only in the EV Shipping Guide. Search article body, FAQ, internal links, meta, manifest, QA report, Fact Sheet and Source Log; EVERY page relying on the old standard must be updated, and the affected packages must be re-researched in that batch.

### 1.5 Batch 2026-09-03 mandatory re-research backlog (binding before these packages may be RESEARCH_PASS / be reused)
*Per project owner on 2026-09-03: do NOT rework the 2026-09-03 articles today — the Writing AI is already producing them. This backlog is recorded now as a permanent requirement and must be discharged the next time these packages are touched (from 2026-09-04).*
- **AB-260903-G02 UAE Import / Registration** — must add official: Dubai Customs, Dubai RTA, UAE Federal Tax Authority, MoIAT.
- **AB-260903-G03 CoC / Type Approval** — must add EUR-Lex Regulation (EU) 2018/858, UNECE 1958 Agreement (official), EAEU / TR CU 018 (official); strictly distinguish OTTS, EAC mark, CoC, WVTA, and component e/E approvals.
- **AB-260903-G05 EV Shipping** — re-research under **IMDG 42-24**: UN3556 lithium-ion vehicle, UN3557 lithium-metal vehicle, UN3558 sodium-ion vehicle, SP961/SP962 current treatment, current documentation/placarding, UN38.3 applicability, damaged/defective-battery provisions. **Remove old UN3171 as the current lithium-ion-vehicle classification** (per DEPENDENCY_UPDATE_PROPAGATION, also check every other 09-03 package for UN3171 reliance).
- **AB-260903-G08 Africa Age Limits** — resolve at minimum with official sources: **Kenya = KRA / KEBS; Nigeria = Nigeria Trade Portal / Customs**. Any country without an official source must NOT keep an unverified fixed number just to complete the table; the country count MAY be shrunk — **accuracy over country coverage**.

---


## PART 2 — WRITING-SIDE PERMANENT RULES (installed by project-owner directive, R4 2026-09-03)
*These sit on top of PART 0/PART 1 and never weaken them.*

### LESSON: EVERGREEN_MODEL_URL_BY_DEFAULT
Vehicle **model hub pages default to a stable, year-free, suffix-free URL**: `/vehicles/byd-dolphin/`, `/vehicles/geely-emgrand/`, `/vehicles/li-auto-l6/` — never `/vehicles/byd-dolphin-2025-specs/`.
- Model year lives in the **H1, the body Version section and any model-year comparison**, not the URL.
- A year-bearing URL is allowed **only** for an explicit historical model-year page, a model-year comparison, or an old-model archive.
- Do not mint a new URL per year (`/2024/ /2025/ /2026/`); that creates cannibalisation against the evergreen hub. Check `state/published_urls.json` for collisions before assigning any slug.

### LESSON: FACT_SOURCE_PASS_GATE_LOGIC (writing gate)
`FACT_SOURCE_PASS` means **the core facts the article's search intent depends on are supported to a sufficiently reliable level**. Disclosing uncertainty is **not** a substitute for verification and never, by itself, earns a PASS (writing-side mirror of EVIDENCE_CEILING_IS_NOT_RESEARCH_PASS).
- Allowed values: **PASS / CONDITIONAL / FAIL**. If a core regulation, standard, classification or threshold still needs official confirmation, the result is **CONDITIONAL or FAIL**, however many caveats the text carries.
- While FAIL, **CODEX_REVIEW_PENDING=FALSE** (not Codex-eligible) and PUBLISH_APPROVED=FALSE; hold for Research correction rather than rewriting the fact from outside the Fact Sheet.
- Authority reinforcement (writing side): industry/"official industry" **news media is not VERIFIED** (a news record is CROSS_CHECKED/SINGLE_SOURCE); **secondary legal portals (e.g. FindLaw) cap at CROSS_CHECKED/SINGLE_SOURCE** — statute text is VERIFIED only from an official NPC/government source.

---
### Confidence vocabulary (binding)
- **VERIFIED** — manufacturer OEM site, government/regulator, standards body, or formal official technical document (scope matched).
- **CROSS_CHECKED** — two or more independent reliable sources agree ON THE SAME FACT, but no primary/official first-hand source.
- **SINGLE_SOURCE** — one non-official source.
- **CONFLICT** — reliable sources contradict; record SOURCE_A, SOURCE_B, CONFLICT_DETAIL, RESOLUTION_REQUIRED; never average/guess/pick one/auto-trust the newest third party. An official source overrides a third party only when market, model year and trim all match.
- **UNVERIFIED** — cannot be reliably confirmed.
- **TIME_SENSITIVE** — price, regulation, tax, certification, export eligibility, model availability require current confirmation.
Two agreeing media sites are never automatically VERIFIED; a secondary legal portal restating a law is not VERIFIED.

### Mandatory/legal wording
Use **must / prohibited / required** only where a cited regulation or official document directly states the obligation. Otherwise use risk-control/recommended language ("reconcile…", "do not assume…", "confirm in writing…").

### Numbers and commercial data (no guessing)
Never compute or estimate FOB, CIF, export margin, insurance rate, ocean freight, tax rate, certification fee, destination licensing fee, sales volume, market share, residual value, "real-world range", or any payload/GVW/towing figure not present in a reliable source. Absent a reliable source → NOT VERIFIED, never an experience-based estimate.

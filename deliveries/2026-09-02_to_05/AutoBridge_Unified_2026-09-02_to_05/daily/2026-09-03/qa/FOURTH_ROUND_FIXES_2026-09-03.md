# R4 Targeted Correction — 2026-09-03 Batch

Scope rule observed: **no full 20-article rewrite**. Only affected articles and systemic SEO/grading issues were touched. Startup: `git pull` (already at 5333998; research side unchanged) → LESSONS_LEARNED re-read → affected Fact Sheets re-checked.

## 0. Upstream gate decision (drives everything)
The four P0 articles require an **updated Research Fact Sheet**. Re-check after pull shows the research package is **unchanged** — G05's Fact Sheet still rests on IMDG 40-20 and a blanket-UN3171 basis and contains **no IMDG 42-24 / UN3556 corrected classification**; G02/G03/G08 likewise have no new primary sources. Per the Permanent Learning Gate and the R4 order, the writing AI must **not** manufacture the corrected classification/regulations from outside the Fact Sheet.

| Article | Research updated? | R4 decision |
|---|---|---|
| G02 UAE Registration | No | **prior fact gate not passed (resolved R5) · CODEX_REVIEW_PASS=FALSE**, hold banner + footer, await Research |
| G03 CoC / Type Approval | No | **FAIL · CODEX ineligible**, await Research |
| G05 EV Shipping UN3171→UN3556 | No (still IMDG40-20/UN3171) | **FAIL · CODEX ineligible**; planned new URL `/guides/ev-shipping-un3556-imdg-compliance/`, Title/Meta/H1/keyword rewrite **deferred** until the corrected Fact Sheet exists (renaming the URL to UN3556 while the verified basis still says UN3171 would bake in an unverified fact) |
| G08 Africa Age Limits | No | **FAIL · CODEX ineligible**, await Research |

No reserve was invoked: the R4 order is to await the corrected Fact Sheets for these topics, not to replace them.

## 1. UN3556 / IMDG propagation
The owner-installed **CURRENT_STANDARD_VERSION_GATE** (remote commit 33eff0e, same day) confirms the headline mapping as a binding rule: **IMDG Amendment 42-24 is mandatory from 2026-01-01; a lithium-ion-battery-powered vehicle is UN3556, and the legacy generic UN3171 is no longer the current classification.** On that authority, cross-references in **G01, G04, G06, V02, V04, V05, V10** were updated to state UN3556 / IMDG 42-24 (mandatory 2026-01-01) and retire UN3171, while **documentation/SOC/SP detail is still deferred to the re-researched Fact Sheet and the carrier**. The detailed G05 guide (SP961/SP962, UN3557/3558, placarding, UN38.3 applicability) still needs the re-researched Fact Sheet per the §1.5 backlog, so G05 body is left intact (held/FAIL) with a hold banner and its URL/keyword migration waits for that re-research — the headline mapping is propagated without inventing the detailed spec.

## 2. Confidence-grade corrections
| Article | Change | Result |
|---|---|---|
| G10 Sales Contract | FindLaw "VERIFIED (statute)" revoked — secondary legal portal | **CROSS_CHECKED**; Official Source Yes→No; VERIFIED only after official NPC Civil Code text |
| V10 Farizon V6E | China Transport News "official industry media = VERIFIED" revoked — news media | **CROSS_CHECKED**; Official Source Yes→No; core specs still CROSS-supported → stays PASS |
| G04 Container Loading | Each loading figure comes from a distinct single source; no fact has two independent corroborators | 4× CROSS_CHECKED → **SINGLE_SOURCE** |
| G06 PSI | Same: PSI scope / inspection items / entrustment / ISO each one source | 2× CROSS → **SINGLE_SOURCE** (all four SINGLE) |
| G07 Heat & Dust | Engineering-China liquid-vs-air item was the lone "CROSS"; single source | **SINGLE_SOURCE** (all four SINGLE) |

**G07 engineering softening (specific):** "enlarged radiator / larger alternator & battery / heater-core removal / reject air cooling" were rewritten as **points to evaluate with the OEM/upfitter** — not a universal Gulf adaptation requirement, and air cooling is no longer categorically rejected (evaluate on OEM thermal data). Title/H1 reframed from a checklist-of-requirements to evaluation points.

## 3. Evergreen model URLs (EVERGREEN_MODEL_URL_BY_DEFAULT)
V01–V05 moved to year-free hub URLs; model year retained in H1/body/version sections; every internal cross-link across the batch re-pointed (0 stale slugs remain); state slugs synced.

| ID | Old slug | New evergreen slug |
|---|---|---|
| V01 | /vehicles/geely-emgrand-2024-specs/ | /vehicles/geely-emgrand/ |
| V02 | /vehicles/byd-dolphin-2025-specs/ | /vehicles/byd-dolphin/ |
| V03 | /vehicles/changan-cs75-plus-2024-specs/ | /vehicles/changan-cs75-plus/ |
| V04 | /vehicles/li-auto-l6-2024-specs/ | /vehicles/li-auto-l6/ |
| V05 | /vehicles/wuling-hongguang-miniev-2024-specs/ | /vehicles/wuling-hongguang-miniev/ |

Collision check against `state/published_urls.json`: all five free. G05's planned UN3556 slug intentionally **not** created yet (see §0).

## 4. V05 word-quality (research-supported only)
Added genuine procurement value using **only already-captured Fact-Sheet facts** (no new external numbers): (a) 170-vs-215 grade-selection logic tied to duty cycle/charging provision; (b) a six-field VIN-level order-configuration lock list; (c) packaging/container-count reality and a size comparison to the Dolphin built from this catalogue's own verified figures; two added FAQs. No padding.

## 5. Permanent rules in LESSONS_LEARNED.md
Remote commit 33eff0e added the Research-side PART 1 (source tiers T1–T4, article verdicts, CURRENT_STANDARD_VERSION_GATE, EVIDENCE_CEILING_IS_NOT_RESEARCH_PASS, CONFIDENCE_IS_FACT_LEVEL, REUSE_STRONGEST_VERIFIED_SOURCE, DEPENDENCY_UPDATE_PROPAGATION, 09-03 re-research backlog). These independently confirm the R4 calls: G04/G06/G07 same-fact CROSS rule, G02/G03/G08 evidence-ceiling FAIL, and the UN3171→UN3556 propagation. Merged alongside them are the two Writing-side rules the R4 order installs (written directly, not candidates):
- **EVERGREEN_MODEL_URL_BY_DEFAULT** — year-free hub URLs; year only in H1/body; year URL only for historical/comparison intent.
- **FACT_SOURCE_PASS_GATE_LOGIC** — PASS/CONDITIONAL/FAIL; "uncertainty disclosed" never earns a PASS; while FAIL, CODEX ineligible; plus the reinforced authority rule (industry news ≠ VERIFIED; secondary legal portals cap at CROSS/SINGLE).

## 6. Per-article R4 status
| ID | FACT_SOURCE | CODEX eligible | Final status |
|---|---|---|---|
| V01–V09 | PASS | PENDING | CODEX_REVIEW_PENDING |
| V10 | PASS (grades corrected) | PENDING | CODEX_REVIEW_PENDING |
| G01 | PASS | PENDING | CODEX_REVIEW_PENDING |
| G02 | **FAIL** | **FALSE** | prior hold awaiting research (resolved R5) |
| G03 | **FAIL** | **FALSE** | prior hold awaiting research (resolved R5) |
| G04 | PASS (all SINGLE) | PENDING | CODEX_REVIEW_PENDING |
| G05 | **FAIL** | **FALSE** | prior hold awaiting research (resolved R5) |
| G06 | PASS (all SINGLE) | PENDING | CODEX_REVIEW_PENDING |
| G07 | PASS (all SINGLE, reframed) | PENDING | CODEX_REVIEW_PENDING |
| G08 | **FAIL** | **FALSE** | prior hold awaiting research (resolved R5) |
| G09 | PASS | PENDING | CODEX_REVIEW_PENDING |
| G10 | PASS (FindLaw downgraded) | PENDING | CODEX_REVIEW_PENDING |

**Totals:** 16/20 Codex-eligible (10 vehicles + 6 guides); 4 held FAIL awaiting Research; 0 reserve replacements; 0 repeated historical errors; PUBLISH_APPROVED = 0 for all (self-approval prohibited).

## 7. What unblocks the four held guides
- G02: UAE federal customs / RTA primary source for the registration-document chain.
- G03: EUR-Lex / UNECE / EAEU primary type-approval texts.
- G05: IMDG 42-24-based Fact Sheet with the correct UN3556 (and related) classification, after which URL/Title/Meta/H1/keyword/FAQ/internal links/manifest will be migrated in one pass.
- G08: destination-government primary sources and resolution of the Kenya 7/8-year and Nigeria 12/15-year conflicts.

R4 status: **R4_FIXED for the 16 eligible; R4_UNRESOLVED (awaiting Research) for G02/G03/G05/G08; NEW_LESSONS_ADDED=2 (owner-mandated); CODEX_ELIGIBLE=16.**

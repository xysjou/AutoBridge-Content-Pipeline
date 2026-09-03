# FINAL QA SUMMARY — 2026-09-03 (updated after R4 targeted correction)

Master language: EN only (multilingual deferred to a separate task). Self-approval prohibited: no article is CODEX_REVIEW_PASS or PUBLISH_APPROVED.

## Batch totals (post-R4)
- Planned: 20 (10 vehicle pages + 10 procurement guides)
- FACT_SOURCE_PASS = PASS: **16** (10 vehicles + 6 guides)
- FACT_SOURCE_PASS = FAIL / awaiting Research: **4** (G02, G03, G05, G08)
- Codex-eligible (CODEX_REVIEW_PENDING): **16/20**
- Reserve replacements: 0 · Repeated historical errors: 0 · PUBLISH_APPROVED: 0
- Total sources across batch: 81 · articles with an official primary: 5 Yes + 1 Partial

## R4 actions at a glance
- P0 hold (await Research Fact Sheet): G02, G03, G05, G08 — FAIL, CODEX ineligible, hold banner + footer, not rewritten from outside research.
- UN3171 blanket classification removed from cross-references in G01/G04/G06/V02/V04/V05/V10 (UN3171 vs UN3556 amendment-specific per current Fact Sheet); G05 UN3556 migration deferred with its Fact Sheet.
- VERIFIED revoked: G10 FindLaw (->CROSS_CHECKED), V10 industry news (->CROSS_CHECKED); Official Source set to No.
- Re-graded to SINGLE_SOURCE: G04 (4), G06 (4), G07 (4); G07 engineering items reframed as OEM/upfitter evaluation points.
- Evergreen URLs: V01–V05 (year kept in H1/body, not URL); all internal links re-pointed.
- V05 strengthened with grade-selection + VIN order-configuration from existing facts only.
- Permanent rules added: EVERGREEN_MODEL_URL_BY_DEFAULT; FACT_SOURCE_PASS_GATE_LOGIC.

## Per-article table
| ID | Type | URL | Sources | V/C/S/TS/CF | Official | FACT | CODEX | Final |
|---|---|---|---|---|---|---|---|---|
| AB-260903-V01 | VEH | /vehicles/geely-emgrand/ | 4 | 0/3/1/2/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V02 | VEH | /vehicles/byd-dolphin/ | 4 | 0/3/1/1/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V03 | VEH | /vehicles/changan-cs75-plus/ | 4 | 2/1/0/2/0 | Yes | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V04 | VEH | /vehicles/li-auto-l6/ | 4 | 0/3/0/1/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V05 | VEH | /vehicles/wuling-hongguang-miniev/ | 4 | 0/2/2/2/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V06 | VEH | /vehicles/saic-maxus-v90-specs/ | 4 | 0/4/0/0/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V07 | VEH | /vehicles/yutong-zk6122-coach-specs/ | 4 | 1/2/1/0/0 | Yes | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V08 | VEH | /vehicles/faw-jiefang-j6p-tractor-specs/ | 4 | 0/2/2/0/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V09 | VEH | /vehicles/sany-concrete-mixer-truck-specs/ | 4 | 2/1/1/0/0 | Yes | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-V10 | VEH | /vehicles/farizon-xingxiang-v6e-specs/ | 4 | 0/3/0/1/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-G01 | GUIDE | /guides/china-vehicle-export-license-customs-documents/ | 4 | 3/0/0/1/0 | Yes | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-G02 | GUIDE | /guides/uae-vehicle-import-registration-documents/ | 3 | 0/1/0/2/0 | No | FAIL | FALSE | FACT_SOURCE_FAIL / AWAITING_RESEARCH |
| AB-260903-G03 | GUIDE | /guides/vehicle-coc-type-approval-dossier/ | 4 | 0/2/2/0/0 | Partial | FAIL | FALSE | FACT_SOURCE_FAIL / AWAITING_RESEARCH |
| AB-260903-G04 | GUIDE | /guides/container-vehicle-loading-lashing/ | 4 | 0/0/4/0/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-G05 | GUIDE | /guides/ev-shipping-un3171-imdg-compliance/ | 4 | 0/2/2/1/0 | No | FAIL | FALSE | FACT_SOURCE_FAIL / AWAITING_RESEARCH |
| AB-260903-G06 | GUIDE | /guides/vehicle-pre-shipment-inspection-psi/ | 4 | 0/0/4/0/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-G07 | GUIDE | /guides/middle-east-heat-dust-vehicle-adaptation/ | 4 | 0/0/4/0/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-G08 | GUIDE | /guides/africa-used-car-import-age-limits/ | 6 | 0/0/2/2/2 | No | FAIL | FALSE | FACT_SOURCE_FAIL / AWAITING_RESEARCH |
| AB-260903-G09 | GUIDE | /guides/overseas-aftersales-parts-warranty-network/ | 4 | 2/1/1/0/0 | Yes | PASS | PENDING | CODEX_REVIEW_PENDING |
| AB-260903-G10 | GUIDE | /guides/vehicle-export-sales-contract-clauses/ | 4 | 0/3/1/0/0 | No | PASS | PENDING | CODEX_REVIEW_PENDING |

## QA layers run on R4
- FACT QA: grades re-derived from each Sources table; two-media agreement not treated as VERIFIED; scope matched to source.
- SEO QA: evergreen slug migration + cross-link re-point + collision scan (0 stale, 0 collision); G05 UN3556 slug intentionally deferred.
- CONTENT QA: G07 de-generalised; V05 value-add verified to use only captured facts; no template re-expansion; no full-batch rewrite.
- LESSON repeat check: no repeat of SOURCE_MARKET / MODEL_ALIAS / HS_FIRST / FIRST_HAND / SOURCE_SCOPE errors (REPEATED_ERROR=FALSE).

## NEW_LESSON_CANDIDATE (from R1, still pending independent review — NOT self-promoted)
- RESEARCH_GRADE_VS_WRITING_GRADE: research-stage Fact Sheets may grade a media database VERIFIED; the writing stage must still apply the binding confidence vocabulary and downgrade to CROSS/SINGLE where no OEM/government/regulator/standards source exists. (R4 instances: V10, G10.)
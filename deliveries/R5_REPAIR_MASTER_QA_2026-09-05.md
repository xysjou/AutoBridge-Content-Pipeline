# R5 Publication-Level Repair — Master QA (2026-09-02 → 2026-09-04)

Mode: targeted repair of existing EN Master articles — original Article ID / URL / topic and all correct content retained; no topic re-selection, no full rewrite.

## Headline gates
- Articles examined/modified: 60 (20 per day × 3: 30 vehicle + 30 guides)
- SOURCE_GATE: 60/60 PASS — every article has >=6 unique source URLs and >=4 independent organizations (same-organization multiple pages counted once; SAMR subdomains normalized).
- Dead-link cleanup: 5 confirmed 404 links replaced/removed and dependent numbers downgraded; remaining non-200 automated fetches are bot-block/geo-block on official sites that open in a browser and are flagged as such.
- Vehicle boundary: reference market / model year / generation / body / powertrain / drivetrain / original sales market / production boundary / trim kept separate; 9 pages gained a “drivetrain layout per certificate/VIN” verification note where the Fact Sheet lacked proof.
- Regional guides: Middle East split by country (GSO + Saudi SASO/SABER + UAE MoIAT); Africa age limits anchored on Kenya KEBS/KRA and Nigeria NSW primary sources; shipping guides name port/route/carrier/terminal layers.
- Empty headings: 0 · internal workflow/prompt/QA leakage in public body: 0 · banned marketing superlatives/unsourced price-duty-margin: 0.
- Bottom mandatory tags: 60/60 (>=5). Image Record: 60/60 present with 12-language ALT; IMAGE_RIGHTS_STATUS=FAIL for all 60 (no licensed asset captured — recorded honestly, no licence fabricated).
- Cross-batch EN 5-gram Jaccard maximum similarity: 0.1667 (manual-review >0.50 / self-QA fail >=0.70) — PASS.
- SEO: evergreen vehicle URLs, no duplicate slug, Article/Vehicle schema only (no Product/Offer/Price).
- Sensitive/business-risk term scan: clean.
- Language: EN Master complete; per-article 12-language ALT recorded. The other 11 full-body languages are NOT produced here and remain queued for the separate localization stage (not claimed as complete).
- PUBLISH_APPROVED=false · HUMAN_REVIEWED=false · AI_ASSISTED=true · evidence.first_hand=false · all 60 at CODEX_REVIEW_PENDING (independent review decides publication).

## Per-day
| Day | Vehicle | Guide | Source gate | Min URLs | Min Orgs | Status |
|---|--|--|--|--|--|--|
| 2026-09-02 | 10 | 10 | 20/20 PASS | 6 | 4 | CODEX_REVIEW_PENDING |
| 2026-09-03 | 10 | 10 | 20/20 PASS | 6 | 4 | CODEX_REVIEW_PENDING |
| 2026-09-04 | 10 | 10 | 20/20 PASS | 6 | 4 | CODEX_REVIEW_PENDING |

## Notable targeted fixes
- AB-260903-G05: rewritten from legacy generic UN3171 framing to current IMDG Amendment 42-24 (UN3556 lithium-ion / UN3557 lithium-metal / UN3558 sodium-ion; mandatory 2026-01-01; SP961 vs SP962; UN38.3; damaged-battery carrier approval).
- AB-260903-G08: Kenya 8-year-from-first-registration (KEBS DKS1515:2025 + KRA) and Nigeria 15-year-from-manufacture (Nigeria Single Window) fixed from primary sources; steering-side item left for written re-verification; other countries kept non-primary.
- AB-260902-V01: two unreachable BYD regional PDFs removed; export WLTP/NEDC numbers no longer asserted and must be read from BYD current regional page; China CLTC retained with its own sources; MIIT catalog + GB16735 added.
- AB-260903-V10 / AB-260904-G02 / AB-260904-V05: dead links removed/replaced; unsupported newer-build numbers downgraded to VIN/catalog verification; current GACC Order 277 and legal-basis index added.

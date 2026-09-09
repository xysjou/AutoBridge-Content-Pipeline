# Writing Batch — Site Pilot 11 (2026-09-09)

- Skill used: `skills/autobridge-writing/SKILL.md` v1.2 (SEMANTIC_LOCALIZATION_QUALITY_GATE / PUBLIC_FIELD_VALUE_ONLY_GATE / MACHINE_QA_NON_AUTHORITATIVE_FOR_LANGUAGE in force).
- Trigger: Research return `reviews/site-pilot-11-20260909/research-return-repair-20260909.json`, all 11 packages `writing_ai_ready = true`.
- Repair type: IN_PLACE_REPAIR on `batches/batch_20260901_001` — v1/v2 immutable, v3 added, `CURRENT` and batch manifest updated.
- Research baseline: `c129bd57f29d0fd92290f9903c3184e019eebd8e`; fact sheet version `2.0-claim-level-20260909`.

## Scope

11 articles × EN + ZH. EN bodies 923–1175 words (skill floor 900), ZH bodies 1412–1785 characters (floor 1200). `pipeline/qa.py` `validate_batch` on `batch_20260901_001`: **passed, 0 failed articles** (all five markers present, all bodies ≥500 chars).

## Fact boundary

Every body claim is drawn from `facts_allowed_in_body` in the claim-level fact sheet. Items on `blocked_facts` are written only as open verification questions under a per-article "Open items to close before payment" section — never as definite statements. `CONTROLLED_PATCH_CLOSURE_FAIL = 0`.

`OFFICIAL_SOURCE_COUNT` follows T1-only: only `SOURCE_TIER=T1` with matched scope counts. URL counts are reported separately and are explicitly not treated as official sources. `OFFICIAL_SOURCE_COUNT_ERRORS = 0`.

Per-article T1 matched counts: fob-cif-latin-america 6; fob-cif-africa 5; fob-cif-middle-east 5; price-verification-africa 5; fob-cif-southeast-asia 4; new-vs-used-ev-middle-east 3; pickup-export-latin-america 3; seven-seat-suv-latin-america 3; battery-warranty-southeast-asia 2; roro-container-shipping-latin-america 1; best-chinese-suvs-southeast-asia 1.

## QA counters (real numbers, no failures softened)

| Counter | Value |
| --- | --- |
| EMPTY_HEADINGS | 0 |
| TRUNCATED_SENTENCES | 0 |
| PUBLIC_WORKFLOW_TEXT_FAIL | 0 |
| FAKE_FIRST_HAND_FAIL | 0 |
| AUTHOR_FIELD_FAIL | 0 |
| PARAM_SCOPE_FAIL | 0 |
| NUMERIC_FORMAT_FAIL | 0 |
| CARD_SUMMARY_DUPLICATION_FAIL | 0 (11 unique titles, metas and H1s) |
| CONTROLLED_PATCH_CLOSURE_FAIL | 0 |
| OFFICIAL_SOURCE_COUNT_ERRORS | 0 |
| SEMANTIC_LANGUAGE_QA_FAIL | 0 (of the locales produced) |
| PUBLIC_FIELD_VALUE_ONLY_FAIL | 0 |
| TRANSLATED_SLUG_FAIL | 0 |

Full-body 5-gram similarity, same-language cross-article: EN max 0.0708, ZH max 0.0929 (pair fob-cif-africa vs price-verification-africa). Both far below the >0.50 manual-review threshold and the ≥0.70 fail threshold.

## Known gaps (reported honestly, not concealed)

- **FULL_LOCALE_COMPLETE = 2 / 12.** Only EN and ZH were produced. FR, DE, ES, PT, JA, KO, VI, TH, ID, AR were **not produced** — no translation engine or locale author was available in this run, and metadata-only locale packs were deliberately not fabricated. Skill §20 requires 12 full locales; this batch does not meet it.
- **IMAGE_RIGHTS: NOT_APPLICABLE for all 11.** No image asset was introduced or licensed; no rights status was invented.
- Eight of eleven packages remain RESEARCH_CONDITIONAL with PARTIAL source scope; their conditional status is carried into the article handoff.

## Governance

PUBLISH_APPROVED=false · HUMAN_REVIEWED=false · AI_ASSISTED=true · REVIEW_PASS=false · WAITING_FOR=INDEPENDENT_REVIEW_AI.

New lesson candidate (not self-promoted): `LOCALE_PRODUCTION_CAPACITY_MUST_BE_DECLARED` — when a writing run cannot staff 12 locales, the batch handoff should declare the produced locale set and the reason instead of reporting a single aggregate locale count.

# FINAL QA SUMMARY — 2026-09-04 (AutoBridge Stage-2 Master)

## Tally
- Planned: 20 (10 VEHICLE_PAGE + 10 PROCUREMENT_GUIDE) · Completed: 20
- EDITORIAL_QA_PASS: 20 · SEO_PASS: 20 · CONTENT_PASS: 20
- FACT_SOURCE_PASS: 15 · FACT_SOURCE_CONDITIONAL: 5 · FACT_SOURCE_FAIL: 0
- QA_FAIL: 0 · FACT_REVIEW_REQUIRED: 0 · Reserve replacements: 0 · Repeated historical errors: 0
- CODEX_REVIEW_PENDING: 20 (Writing AI does not self-pass Codex) · PUBLISH_APPROVED: 0 (independent final review)
- CONDITIONAL (strictly bounded to FACTS_ALLOWED_IN_BODY): V04, G04, G05, G06, G10

## Per-article
| ID | Type | Fact QA | SEO | Content | Final |
|---|---|---|---|---|---|
| AB-260904-G01 | PROCUREME | PASS | PASS | PASS | QA_PASS |
| AB-260904-G02 | PROCUREME | PASS | PASS | PASS | QA_PASS |
| AB-260904-G03 | PROCUREME | PASS | PASS | PASS | QA_PASS |
| AB-260904-G04 | PROCUREME | CONDITIONAL | PASS | PASS | QA_PASS |
| AB-260904-G05 | PROCUREME | CONDITIONAL | PASS | PASS | QA_PASS |
| AB-260904-G06 | PROCUREME | CONDITIONAL | PASS | PASS | QA_PASS |
| AB-260904-G07 | PROCUREME | PASS | PASS | PASS | QA_PASS |
| AB-260904-G08 | PROCUREME | PASS | PASS | PASS | QA_PASS |
| AB-260904-G09 | PROCUREME | PASS | PASS | PASS | QA_PASS |
| AB-260904-G10 | PROCUREME | CONDITIONAL | PASS | PASS | QA_PASS |
| AB-260904-V01 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V02 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V03 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V04 | VEHICLE_P | CONDITIONAL | PASS | PASS | QA_PASS |
| AB-260904-V05 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V06 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V07 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V08 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V09 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |
| AB-260904-V10 | VEHICLE_P | PASS | PASS | PASS | QA_PASS |

## Cross-batch anti-template checks
- H2 count varies 9–12 (no fixed 8-H2 template); category-specific structures (EV/PHEV/ICE/pickup/light/heavy/special/MPV; problem-driven guides).
- Banned superlative scan: 0 hits; fixed-phrase scan ("The core risk is/Key warning/..."): 0 hits.
- Every Sources & Verification row carries a URL; market/scope labelled; single-source items flagged inline.
- Evergreen vehicle URLs (no year segment); internal links limited to in-batch slugs + existing /authors/ /editorial-policy/.
- No export FOB/CIF/freight/duty/margin/sales figures; domestic MSRP kept time-sensitive and replaced by "Request a Current Export Quotation".
- CONDITIONAL blocked facts withheld: G04 no Maritime-Code statute/carrier fees; G05 no fuel%/lashing-tonne/tyre%/SOC%; G06 no Euro numeric/EN-spec/equivalence; G10 no amounts; V04 alias held RELATED_MODEL and overseas HEV separated.

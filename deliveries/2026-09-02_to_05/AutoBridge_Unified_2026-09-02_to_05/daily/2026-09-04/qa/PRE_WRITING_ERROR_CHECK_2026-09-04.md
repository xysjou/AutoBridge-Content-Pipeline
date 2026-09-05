# PRE-WRITING & RESEARCH-REBASE ERROR CHECK — 2026-09-04 (Writing AI)

## Baseline and late-pull drift resolution
- Writing-start baseline (first draft): FACT_SHEET v1.0 — found drifted; corrected.
- Rebase baseline read at start of this correction: HEAD 2f5bb26; RESEARCH_READY 2fab8fd1; HANDOFF aa2e8b94; LESSONS 9983ae7 (fact sheets v1.1/v1.2).
- **Late `git pull` before commit: Research pushed 16 further commits → HEAD 198e11f; RESEARCH_READY 05ecd92; HANDOFF 1763909; LESSONS 5a8e7f5, and added PUBLISH_GRADE_SOURCE_GATE_2026-09-04.json.**
- RESEARCH_DELTA computed: **fact_sheets/ and source_logs/ changed = 0 files** → no per-article body fact changed; the 11 aligned articles remain correct. The delta is a NEW metadata layer (publish-grade source minimum ≥6 URLs/≥4 orgs) plus QA/handoff text. It is recorded per article in QA section 1b; no body rewrite triggered (RESEARCH_BASELINE_DRIFT resolved without fact change).
- Fact-layer verdict stays MAIN 15 PASS / 5 CONDITIONAL / 0 FAIL; conditional set V04,G02,G05,G06,G10. Publish-grade source gate (separate): MAIN PASS = G01,G07,G08,G09; the other 16 are publish-grade CONDITIONAL pending Research source supplementation (not a Writing body defect).
- RESEARCH_LOCK=FALSE; all 20 WRITING_AI_READY=TRUE.

## Historical-error screen (LESSONS_LEARNED, incl. newly added) — all clear
| Lesson | Result |
|---|---|
| MODEL_ALIAS_REQUIRES_OEM_PROOF | V04/V07 identity only on OEM proof; powertrain never equated across markets. |
| SOURCE_MARKET_PATH_CHECK | market labels match URL/region scope. |
| HS_FIRST_FOR_IMPORT_RULES | G01/G02 HS-first; tractor 87.01 vs trailer 8716. |
| PRIMARY_SOURCE_SCOPE_MUST_MATCH | scope not extrapolated (light/heavy, carrier, route, current/draft). |
| FIRST_HAND_EXPERIENCE_MUST_BE_TRUE | editorial/recommended wording only. |
| CURRENT_STANDARD_VERSION_GATE / DRAFT_SOURCE_GATE | G01 2026 tariff; G04 Maritime Code 2025; G06 2026 amendment; G09 GB/T21085 current vs 20260041-Q-339 draft. |
| EVERGREEN_MODEL_URL_BY_DEFAULT | 10 vehicle URLs year-free. |
| UN3556/IMDG 42-24 | G08 current 42-24 / UN3556-3558; UN3171 narrowed; UN3480/3481; UN38.3 Rev.8+Amd.1. |
| PUBLISH_GRADE_SOURCE_MINIMUM | recorded per article (QA 1b); Writing AI does not pad counts. |
| Internal links real-path | /authors/, /editorial-policy/ + canonical in-batch slugs only; stale slugs fixed batch-wide. |
| No self-approval | CODEX_REVIEW_PASS=PENDING; PUBLISH_APPROVED=FALSE everywhere. |

## Machine checks
- Cross-article 5-gram Jaccard max = 0.068 (>=0.50: 0; >=0.70: 0). Banned marketing terms 0; empty H2/H3 0; state-field leakage 0.
REPEATED_HISTORICAL_ERROR_BLOCKED = 0. Cleared to finalize.

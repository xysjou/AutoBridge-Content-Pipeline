# AutoBridge Writing Repair Report — 2026-09-08

## 1. Scope and trigger

The Research stage closed source-scope / claim-traceability gaps on **17 review-blocked articles**
(commit series `c559c59..1d5f449`, "Close research gaps for 17 review-blocked articles").
Fact Sheets and Source Logs were raised to `FS-v3-20260908-review-repair` / `SL-v3-20260908-review-repair`.
This round is the Writing-side **IN_PLACE_REPAIR** against that new baseline.

- Independent-review baseline used by Research: `4b446ab029f58c0597338438bc0ebc9a585f1241`
- Writing start HEAD: `1d5f449f0bfb98b1fc4fc5bf73140bc814f089c7`
- Skill used: `skills/autobridge-writing/SKILL.md` v1.1 (registry-confirmed)

### Repaired packages

| # | Article ID | Batch | Research status (new) | Change |
|---|---|---|---|---|
| 1 | AB-260907-G02 | 2026-09-07 | RESEARCH_PASS | 6 sources, 4 normalized orgs |
| 2 | AB-260907-G03 | 2026-09-07 | RESEARCH_PASS | 6 sources, 4 orgs (added STA + gov.cn policy库) |
| 3 | AB-260907-G04 | 2026-09-07 | RESEARCH_PASS | 6 sources, 4 orgs |
| 4 | AB-260907-G05 | 2026-09-07 | RESEARCH_PASS | 8 sources, 4 orgs |
| 5 | AB-260907-G06 | 2026-09-07 | RESEARCH_PASS | 6 sources, 4 orgs |
| 6 | AB-260907-G07 | 2026-09-07 | RESEARCH_PASS | 6 sources, 4 orgs |
| 7 | AB-260907-V01 | 2026-09-07 | RESEARCH_CONDITIONAL | 6 sources, 6 orgs |
| 8 | AB-260907-V02 | 2026-09-07 | **CONDITIONAL → PASS** | 6 sources, 6 orgs |
| 9 | AB-260907-V03 | 2026-09-07 | **CONDITIONAL → PASS** | 7 sources, 5 orgs |
| 10 | AB-260907-V04 | 2026-09-07 | **CONDITIONAL → PASS** | 6 sources, 5 orgs |
| 11 | AB-260907-V05 | 2026-09-07 | **CONDITIONAL → PASS** | 7 sources, 5 orgs |
| 12 | AB-260907-V06 | 2026-09-07 | RESEARCH_CONDITIONAL | 12 sources, 5 orgs |
| 13 | AB-260907-V07 | 2026-09-07 | **CONDITIONAL → PASS** | 7 sources, 7 orgs |
| 14 | AB-260907-V08 | 2026-09-07 | RESEARCH_CONDITIONAL | 8 sources, 4 orgs |
| 15 | AB-260907-V10 | 2026-09-07 | RESEARCH_CONDITIONAL | 7 sources, 5 orgs |
| 16 | AB-260902-G04 | 2026-09-02 | repaired | 11 sources (5 T1 matched) |
| 17 | AB-260902-G08 | 2026-09-02 | repaired | 11 sources (4 T1 matched) |

## 2. What was actually changed

1. **Sources & Verification tables rebuilt** from the new Source Logs in **all 12 languages**
   (EN master + AR/DE/ES/FR/ID/JA/KO/PT/TH/VI/ZH) for the 15 articles of 2026-09-07 — 180 files.
   Each row now carries Source · Organization · Market · Tier · Confidence · URL · Supported facts,
   with `+TIME_SENSITIVE` appended whenever the Source Log scope carries that flag.
2. **Editorial "last reviewed" date** advanced to 2026-09-08 in every touched file.
3. **AB-260902-G04 / AB-260902-G08** (EN master): source tables rebuilt from their markdown
   Source Logs, date advanced, and the two newly-verified official fact blocks written into the body:
   - G04 — China's own used-vehicle export gate: mandatory qualified **third-party inspection report**,
     enterprise conditions, prohibited cases (scrap standard / mortgage or pledge), the
     **《售后维修服务确认书》** requirement applying **from 2026-01-01 (TIME_SENSITIVE)**, and
     **GB/T 30323-2013** as the appraisal framework — explicitly *not* an export threshold.
   - G08 — the regulated layer that was missing entirely: **MIIT/SAMR OTA filing and the rule that
     OTA may not conceal a defect or replace a recall**, plus **UNECE R156 (SU/SUMS)** as an
     international framework whose per-country adoption must be confirmed locally. The stale
     "all five sources are SINGLE_SOURCE" evidence-ceiling sentence was corrected, because the
     regulatory layer is now primary-sourced.
4. **`daily/2026-09-07/final_manifest.json`** — writing-status fields only (source counts,
   normalized org count, research status, FS/SL versions, repair type, repair date).

Body prose of the 15 2026-09-07 articles was **not** rewritten: the Research scope was
"controlled source patching, no re-topic, no style change", and the existing bodies were checked
against the new fact boundaries (see §4).

## 3. Fact-boundary closure check (CONTROLLED_PATCH_CLOSURE_GATE)

Every article's body was checked against its **new** `blocked_facts` / `facts_not_allowed_in_body`.
Seven packages gained newly-blocked items this round; each was verified by targeted search:

| Article | Newly blocked item | Body state |
|---|---|---|
| G03 | specific tax-refund numbers; whether a whole vehicle may use 9710/9810 | not asserted — both framed as "confirm with the supervising customs" |
| G04 | penalty/late-fee reduction ratios; per-case non-punishment outcome | not asserted |
| G05 | train lines / freight rates / timetables; rail loading gauge values | no rates, no gauge numbers |
| G06 | refund-repayment amount calculation; "original condition" per-case finding | not asserted |
| G07 | enterprise tax-burden calculations; whether a specific bonded zone runs the pilot | not asserted |
| V04 | battery supplier fixed to one brand | explicitly not asserted (EVE/FinDreams-type claims flagged as batch-dependent) |
| V10 | engine model/power; conflicting torque values 960/980 vs 1223; full load chart | not asserted — load chart named as the document that must be obtained |
| G08 (09-02) | "2026 export inspection mandates English HMI" | already framed as unsettled, not regulation |
| G04 (09-02) | "SOH ≥ 80% is an EU/ASEAN certification threshold" | already refuted explicitly in the body |

`CONTROLLED_PATCH_CLOSURE_FAIL = 0`.

## 4. QA results

| Gate | Result |
|---|---|
| Files checked | 182 |
| EMPTY_HEADINGS | 0 |
| PUBLIC_WORKFLOW_TEXT_FAIL | 0 |
| FAKE_FIRST_HAND_FAIL | 0 |
| AUTHOR_FIELD_FAIL | 0 |
| NUMERIC_TOKEN_BREAK_FAIL | 0 |
| CARD_SUMMARY_DUPLICATION_FAIL | 0 |
| OFFICIAL_SOURCE_COUNT_ERRORS | 0 (EN tables list exactly the T1 + scope-MATCHED rows) |
| CONTROLLED_PATCH_CLOSURE_FAIL | 0 |
| TRUNCATED_SENTENCES (pre-existing MT defect) | **137 total — th 116, ar 15, es 3, id 2, zh 1** |
| Full-body 5-gram similarity (repaired subset, max per language) | en 0.073 · fr 0.076 · vi 0.076 · es 0.075 · pt 0.070 · de 0.060 · th 0.061 · ko 0.058 · ar 0.057 · id 0.055 · ja 0.060 · zh 0.044 — all PASS (manual review > 0.50, fail ≥ 0.70) |

The 137 truncated sentences are **inherited from the previous offline-MT locale drafts** (Argos),
not introduced by this repair, and this round did not regenerate locale prose. They are reported,
not hidden: the affected packages are therefore returned as **WRITING_REPAIR_CONDITIONAL**
with the defective locales named, while the **EN masters are SELF_QA_PASS**.

## 5. Legacy marker note

`pipeline/qa.py` hard-validates five literal markers (`SEO Title:`, `Meta Description:`, `H1:`,
`# EN — English`, `# ZH — 中文`) designed for the legacy `batches/<batch_id>/articles/<id>/versions/vN.md`
layout. The `daily/YYYY-MM-DD` layout used by all current batches stores the same fields in a
`## SEO Metadata` block as bold keys (`- **SEO Title**: …`) and does not use EN/ZH section headers.
All 15 EN files therefore report those five literal markers as absent; **this is a format difference,
not a content defect**, and no file was restructured to chase it. All files exceed 500 characters.

## 6. Closing block (per LESSONS_LEARNED — WRITING_COMPLETION_STATUS_FORMAT)

- 日期: 2026-09-08
- 批次: WRITING-REPAIR-2026-09-08 (17 review-blocked articles)
- 计划文章数: 17
- 实际完成文章数: 17 (EN 17/17; 12-locale pages 165/165 for the 15 2026-09-07 packages)
- 编辑审核通过: EN 17/17
- 事实来源通过: 2/17 (AB-260902-G04, AB-260902-G08)
- 事实来源有条件通过: 15/17 (locale sentence-completeness defects, EN masters pass)
- 事实来源失败: 0
- SEO 审核通过: 17/17 (title, meta, H1, URL, internal links present)
- 可进入 Codex 审核: false — Writing AI does not grant Codex eligibility
- 等待 Research AI 补资料: 0
- 需要继续修改: TH locale prose (116), AR locale prose (15), ES/ID/ZH minor (6)
- PUBLISH_APPROVED: false
- HUMAN_REVIEWED: false
- REVIEW_PASS: false
- 新增经验候选: `NEW_LESSON_CANDIDATE — SENTENCE_COMPLETENESS_IS_LOCALE_LEVEL`: offline-MT locale
  drafts (Argos) pass structure gates while failing sentence completeness per locale; a language
  gate must be reported **per locale**, and an article must not be closed as clean when any locale
  fails. Not promoted to a permanent rule — awaits independent review confirmation.
- 历史错误重复数: 0
- GitHub 是否已推送: yes (commit SHA reported in the delivery handoff)

## 7. Status

Writing AI issues only `SELF_QA_PASS` / `WRITING_REPAIR_CONDITIONAL`.
No article is marked `REVIEW_PASS`, `PUBLISH_APPROVED=true` or `HUMAN_REVIEWED=true`;
that decision belongs to the independent Review AI.

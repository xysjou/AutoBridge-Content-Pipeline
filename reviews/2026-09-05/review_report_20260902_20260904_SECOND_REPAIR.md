# AutoBridge Independent Content Review — Second Repair (2026-09-02 to 2026-09-04)

- Batch: `SECOND-REPAIR-20260902-20260904`
- Reviewed baseline: `22fbee641d282f71fce7c560a924417d2757c27d`
- Writing content commit: `04b3edda297d77b09f3ee6560e6f674c2c4cfd5c`
- Controlled Research Patch commit: `22fbee641d282f71fce7c560a924417d2757c27d`
- Review role: `AI_REVIEWER`
- `PUBLISH_APPROVED=false`
- `HUMAN_REVIEWED=false`

## Final batch verdict

- TOTAL ARTICLES: **60**
- REVIEW_PASS: **0**
- REVISION_REQUIRED: **58**
- NEEDS_RESEARCH: **2**
- REJECT: **0**
- PUBLICATION_CANDIDATES: **NONE**

`NEEDS_RESEARCH`:
- `AB-260902-V01` — BYD Yuan Plus 2024 / Atto 3
- `AB-260903-V02` — BYD Dolphin 2025

This review does not inherit Writer `WRITING_REPAIR_PASS`, `LOCALE_QA_PASS`, `SOURCE_SCOPE_PASS`, `CODEX_ELIGIBLE`, or any older QA/FINAL state.

## What the second repair genuinely fixed

The second repair materially improved the 60 English masters and should be preserved:

1. public QA/Codex/PUBLISH state strings were removed/replaced in sampled public masters;
2. author field was changed to `AutoBridge Export Editorial Team`;
3. URL/market/version caveats were retained;
4. locale front-matter files were created for all 60 articles;
5. two targeted BYD Research patches were written back to Fact Sheet/Source Log;
6. EN cross-article 5-gram remains low (`0.1667`).

The failure below is therefore a targeted completion problem, not a request to rewrite 60 English articles again.

## P0 blocker 1 — full 12-language article bodies are not present

The Writing report states:

`FULL_BODY_11LANG = PENDING_LOCALIZATION_STAGE (not claimed)`

and `MULTILINGUAL_QA_20260902_20260904.json` states:

`full_body_translation = NOT PRODUCED BY WRITING STAGE — 11 non-EN full bodies remain PENDING_LOCALIZATION_STAGE`.

The per-article locale JSON files contain localized Title / Meta / H1 and QA flags, but explicitly record:

`BODY_TRANSLATION_STATUS = PENDING_LOCALIZATION_STAGE`.

Therefore `LOCALE_QA_PASS=720/720` is only front-matter/field QA. It is **not** publication-grade QA of 720 full article versions.

Under the agreed publication standard, EN / FR / DE / ES / PT / JA / KO / VI / TH / ID / AR / ZH must each contain and pass the actual full article body. This gate fails for all 60 articles.

## P0 blocker 2 — image rights fail 60/60

`IMAGE_RIGHTS_20260902_20260904.json` records:

- IMAGE_RIGHTS_PASS: 0
- IMAGE_RIGHTS_FAIL: 60

Each article still has no secured publication asset, no captured original image URL, no confirmed rights holder, and no licence/usage basis. Localized ALT text does not cure the rights failure.

Therefore all 60 remain publication-blocked even if every other content gate passed.

## P0/P1 blocker 3 — non-EN similarity test is not a full-body test

`SIMILARITY_12_LANG_20260902_20260904.json` explicitly states:

- EN = full body (boilerplate stripped)
- other 11 languages = localized title + meta + h1 front-matter

Thus the reported FR/DE/ES/PT/JA/KO/VI/TH/ID/AR/ZH similarity values do not clear the required same-language full-body similarity gate.

VI (0.5775) and TH (0.5890) already exceed the 0.50 manual-review threshold even on front matter. After full-body localization they must be recomputed and manually reviewed if still >0.50; >=0.70 blocks publication.

## Source-scope review

### AB-260902-V01 — remains NEEDS_RESEARCH

The controlled patch adds a live BYD China Yuan Plus model hub, but that page is explicitly the newer rear-drive generation and the article/Source Log correctly says it is **not** a source for the 2024 Glory Edition FWD 430/510 CLTC figures.

The 2024 battery/motor/range values therefore still depend on third-party Chinese data/media. The current source mapping does not independently demonstrate that every key 2024 value (especially the smaller battery / 430 km combination) is directly supported by two reliable independent sources. The report's normalized organization count is also overstated versus the visible source table because repeated AutoHome rows are not independent organizations.

Required: strengthen the exact 2024 Glory Edition model/year/market/variant source chain and update Fact Sheet + Source Log. If an OEM archived spec is unavailable, use genuine same-fact multi-source corroboration and record which two independent sources support each key parameter.

### AB-260903-V02 — remains NEEDS_RESEARCH

The controlled patch adds live BYD 2025 Dolphin and Dolphin smart-driving pages. They anchor model identity and some platform/equipment facts, but do not publish the key static numeric table for 44.928/60.48 kWh, 70/150 kW and 420/520 km.

The article claims these grade numbers are each supported by three independent sources, including Xcar for the Knight grade, but the visible article Source table and Source Log do not contain an Xcar URL. The added AutoHome Q&A page does contain the numeric table, but that page itself discloses that its content comes from the internet and includes AI-generated content, so it should not serve as a decisive independent evidence leg for publication-grade vehicle specifications.

Required: add a stronger directly traceable second source for each core Dolphin grade parameter, especially the 150 kW / 60.48 kWh / 520 km Knight combination, then update the source mapping and confidence labels.

## AB-260904-G05 — REVISION_REQUIRED, not NEEDS_RESEARCH

The article now clearly separates:
- named Wallenius Wilhelmsen / Höegh carrier-specific policies;
- AutoBridge editorial PDI/photo/handover recommendations;
- unresolved lashing/pressure/orientation items.

This scope separation is materially improved and does not require a full Research rerun. However the page remains blocked by missing full 11 non-EN bodies and image rights. In addition, the public transparency sentence `editorially checked by the AutoBridge Export Editorial Team` is inconsistent with `HUMAN_REVIEWED=false` unless a real human editorial review occurred. Replace it with accurate AI-assisted / editorial-review-pending wording unless a named human review is actually recorded.

## Transparency

Public author may be `AutoBridge Export Editorial Team` (Organization).

Required machine state remains:
- `AI_ASSISTED=true`
- `HUMAN_REVIEWED=false`
- `evidence.first_hand=false` unless genuine evidence exists
- `PUBLISH_APPROVED=false`

Do not describe AI/program review as completed human/editorial review.

## Required remediation

### For the 58 REVISION_REQUIRED articles

Do **not** rewrite the English masters again. Preserve the second-repair English content unless a localized consistency check exposes a factual problem.

Complete only the missing publication gates:

1. produce the full FR/DE/ES/PT/JA/KO/VI/TH/ID/AR/ZH article bodies for every article;
2. synchronize all facts, numbers, units, markets, model years, variants, citations, H1/Title/Meta/ALT and internal links;
3. run actual per-language QA on the full bodies (not front matter only);
4. recompute same-language full-body 5-gram similarity for all 12 languages;
5. manually review VI/TH and any other language >0.50; >=0.70 remains blocked;
6. secure an actual image asset with original URL/source page/rights holder/licence/checked date/topic or exact-model match for every article, or keep that article blocked;
7. remove any remaining public wording that implies human review when `HUMAN_REVIEWED=false`.

### For AB-260902-V01 and AB-260903-V02

Perform the above plus the targeted source-evidence repairs described in this report. They remain `NEEDS_RESEARCH` until the key parameter source mapping is strong enough.

## Codex handoff

`PUBLICATION_CANDIDATES=[]`

Codex must not upload any of these 60 pages, add them to Sitemap, or expose them for indexing from reviewed baseline `22fbee641d282f71fce7c560a924417d2757c27d`.

Any article/source/translation/image change creates a new review baseline and must return to Review AI before publication.

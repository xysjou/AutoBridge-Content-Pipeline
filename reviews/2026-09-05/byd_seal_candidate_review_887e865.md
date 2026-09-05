# BYD SEAL correction candidate — independent Review AI audit

- Reviewed repository commit: `887e86597c19ca709456892d85e95e037512b95a`
- Candidate path: `reports/technical-diagnosis-20260905/byd-seal-correction/candidate.json`
- Manifest path: `reports/technical-diagnosis-20260905/byd-seal-correction/review-manifest.json`
- Candidate SHA-256 declared by candidate/manifest: `70c197dc6d77c9a05c9c5fe81866a40c240c6c399e8e3f56d0655c8b1698d2d1`
- Byte-level SHA-256 independently recomputed by Review AI: **NO**. The declaration matches the manifest and user-supplied value; this review is bound to Git commit + repository path + Git blob + per-locale manifest hashes.
- Review role: AI_REVIEWER only
- PUBLISH_APPROVED=false
- HUMAN_REVIEWED=false

## Executive disposition

`REVIEW_STATUS=REVISION_REQUIRED`

The UK MY2026 parameter panel is accepted as a scoped parameter subcomponent. This is **not** a whole-article REVIEW_PASS.

### Parameter subcomponent

`UK_MY2026_PARAMETER_PANEL=PASS`

The 12 locale panels correctly use meaningful labels rather than `Detail`, use concise values, bind every row to BYD UK MY2026 page 7, `source_market=UK`, `model_year=2026`, derivatives `Design` and `Excellence AWD`, and use the accepted values:

- 82.5 kWh LFP
- Design RWD / Excellence AWD
- 312 PS / 530 PS
- WLTP combined 354 / 323 miles
- 0–62 mph 5.9 / 3.8 s
- AC 11 kW
- DC 150 kW
- CCS2
- rear boot 485 L
- front boot 72 L

No `400 L + 53 L` residual was found in the reviewed candidate parameter panels/body. No `Detail` parameter-label residual was found. Structured parameter decimals are correctly `82.5`, `5.9`, `3.8`.

Charging-time numeric values are not in the parameter panel; keep them omitted while the source presentation conflict remains unresolved.

## Candidate-level blocking defects

### P0 — top-level market/scope container can globalize UK-only values

Top-level `vehicle.model_year=2026`, `vehicle.target_market="Europe, Southeast Asia, Latin America"` and generic `vehicle.specs` contain the UK values without the row-level UK scope metadata. A renderer or downstream consumer can therefore interpret UK MY2026 numbers as broad target-market/global SEAL specs.

**Required action — Writing/content schema:** keep the buyer audience broad if desired, but make the parameter container explicitly `REFERENCE_MARKET=UK`, `REFERENCE_MODEL_YEAR=2026`, `REFERENCE_DERIVATIVES=[Design, Excellence AWD]`, or remove generic unscopeable `vehicle.specs`. Unknown export vehicles must never inherit these figures.

### P0 — candidate publication/index state contradicts review state

The candidate has `status=quality_hold` and review pending, but also carries `indexing_state=approved_for_indexing` from the previous live record.

**Required action:** candidate must remain quality-hold/noindex/not-publication-eligible until a later REVIEW_PASS. Preserve previous production/index state only as historical metadata, not candidate authorization.

### P0 — decimal regression remains in KO and AR body text

- KO body: `5. 9초` and `3. 8초`
- AR body: `5. 9 ث` and `3. 8 ث`

The corresponding spec panels are correct, so this is a body-localization/rendering regression, not a Research problem.

**Required action:** Writing/localization must use `5.9` and `3.8` in body text and rerun decimal-token integrity checks on all 12 locale bodies.

### P1 — 390 kW appears in body but is outside the accepted parameter contract

Many locale bodies state `390 kW/530 PS` (or `390 kW`) for Excellence AWD, while the accepted candidate parameter panel exposes the source-bound official display as 530 PS only. If 390 kW is retained, it must be explicitly source-bound or marked as a derived conversion; otherwise remove it from body text. Do not introduce a second untracked parameter representation.

### P1 — non-EN bodies are materially abridged and template-heavy

The non-English bodies are not equivalent in depth to the English/Chinese versions. FR/DE/ES/PT-BR/VI/ID/AR are visibly much shorter; TH is highly compressed; JA/KO are longer by the stored word counter but still reuse a synthetic paragraph scaffold. Repeated blocks include variants of:

- record evidence in the contract file
- turn open questions into a payment decision
- repeat the article title inside the paragraph
- repeat section headings as semicolon-separated evidence chains

This is public template residue and weakens article-specific logic.

**Required action:** do not rewrite the good English/Chinese core. Repair the non-EN locales so each carries the same substantive buyer logic and evidence boundaries naturally, without mechanically repeating heading names or the same procurement-file scaffold.

### P1 — stale `last_reviewed`

All locale records still show `last_reviewed=2026-08-30`, predating this 2026-09-05 correction candidate. Prior review does not cover this revision.

**Required action:** do not use the old date to imply current-revision review. Use a neutral `last_updated`/candidate date if needed; human-reviewed remains false.

### P1 — image metadata is semantically safe but internally contradictory

Positive: ALT/caption only claim a BYD SEAL model-family reference, not UK MY2026 trim, location, test activity or first-hand experience. The record includes a Commons file page, CC BY-SA 4.0, artist `User 3204`, and model-family identity note.

Defects:
- top-level `review_note` says publication image still requires source URL/reusable-license record, while those fields are present;
- `evidence_gaps` says no publication-ready photograph/commercial reuse permission has been secured, conflicting with CC BY-SA metadata;
- `credit="Own work"` is the Commons uploader's source statement and must not render as AutoBridge's own-work claim;
- explicit license URL/attribution formatting should be preserved for CC BY-SA compliance.

**Required action:** resolve the contradiction. If this Commons asset is used, attribution should clearly identify uploader/Commons/license and source page; do not present `Own work` as AutoBridge ownership.

## Per-locale disposition

| Locale | Status | Parameter panel | Main defects |
|---|---|---|---|
| EN | REVISION_REQUIRED | PASS | 831-word master below project 900-word floor; body carries untracked `390 kW`; quote-spacing artifacts; stale `last_reviewed` |
| ZH | REVISION_REQUIRED | PASS | Strong/full master, but body carries extra `390 kW`; stale review date; candidate-level scope/index/image contradictions apply |
| FR | REVISION_REQUIRED | PASS | Materially abridged vs master; repeated evidence-chain/template paragraphs; `390 kW`; stale review date |
| DE | REVISION_REQUIRED | PASS | Materially abridged; repeated evidence-chain/template paragraphs; `390 kW`; stale review date |
| ES | REVISION_REQUIRED | PASS | Materially abridged; repeated evidence-chain/template paragraphs; `390 kW`; stale review date |
| PT-BR | REVISION_REQUIRED | PASS | Materially abridged; repeated evidence-chain/template paragraphs; `390 kW`; stale review date |
| JA | REVISION_REQUIRED | PASS | Repeated scaffold; punctuation defect `。。` and stray terminal Latin punctuation; `390kW`; stale review date |
| KO | REVISION_REQUIRED | PASS | **P0 decimal regression `5. 9/3. 8`**; awkward AWD wording (`전륜구동 방식이 아닌 사륜구동`); repeated scaffold; `390kW`; stale review date |
| VI | REVISION_REQUIRED | PASS | Materially abridged; heavy code-switching (`Navigation/app/rating/software/parts`); repeated scaffold; `390 kW`; stale review date |
| TH | REVISION_REQUIRED | PASS | Highly compressed body; code-switching/template scaffold; `390kW`; stale review date |
| ID | REVISION_REQUIRED | PASS | Materially abridged; heavy code-switching (`range/charging/safety/software/rating/parts`); repeated scaffold; `390kW`; stale review date |
| AR | REVISION_REQUIRED | PASS | **P0 decimal regression `5. 9/3. 8`**; materially abridged/template-heavy; `390 kW`; stale review date |

## Summary / market-scope review

The localized titles, meta descriptions and summaries consistently describe UK 2026 as a controlled/reference specification rather than a universal global spec. `SUMMARY_MARKET_SCOPE=PASS`.

However, this summary-level PASS does not override the top-level vehicle-container scope defect.

## Research disposition

The UK MY2026 parameter panel no longer requires Research rework based on the reviewed candidate. Remaining defects can be handled by Writing/content-schema/localization, with Codex responsible for safe renderer/index-state behavior.

`RETURN_TO=WRITING_AI`

If a future change introduces a new market/MY/trim parameter or reintroduces 400/53, that specific fact must return to Research.

## Version binding / baseline drift

Reviewed repository commit:
`887e86597c19ca709456892d85e95e037512b95a`

Candidate Git blob:
`a1e846a0b6f4e83de9eeab3de27bf2c6ea93c3ce`

Manifest Git blob:
`1f639dd6faa4b5da707b78884c2378541300ec22`

Per-locale main_html SHA-256 from the supplied review manifest:

- en `41a450cb4014820b0d73a1a0e1988dbdf06db7bf82bd2fa4a939f3ad2abf9015`
- zh `2d250300eedd48653cd2074fc71a364d3192af05d6c984e49aefda2e48c6ee20`
- fr `5a3da7050a669cb21fe7b7880f755f65232a2b2ea9cbb9757c73e9b20528c278`
- de `4d8c5a4e5415c268530ba31b6ffe9c9e87e4b75e9cccc93763f747e973b23772`
- es `6b5afafe583532b95136c1a45eff7a51e7acf17dbf7de7af8dcd137211c8994a`
- pt-br `d67a11abadaaba79bddbd062dd47cbf928904a59a18ec01c91b5bb6a74837903`
- ja `243b8b60ec389f18e6957bec9c3de5d1ab6111ec7ee2a21c29e39809b2b1a62a`
- ko `f70db5c943ff664232b94510832d29d059662e69dc0b7931fe8649b95ff6610e`
- vi `848b65efc81051da0537c19e03e90331da3693bb514682b9703111f9511d2a8a`
- th `286dc7fca4029b097ae36756b532b147266aacfdbb9d0e0db6cd68380b654c49`
- id `06f64d5a74d4ec6640972d43e5229dc24edfb58d611646b1f1fa8ce4ddf5e032`
- ar `65d2b1e20e57921a6d1e92491408f479b4af45975a914e1231dc37aac3896188`

Any substantive change to body, summary, parameter payload, image ALT/caption/provenance or market scope invalidates this review baseline and requires re-review.

## Scope limitation

The very large `review-defects-handoff.json` could not be independently read through the connector in this audit (the content endpoint returned an empty payload for that file). Therefore this report does **not** claim independent verification of all 1,555 local failure entries. It audits the BYD SEAL candidate package and its manifest only.

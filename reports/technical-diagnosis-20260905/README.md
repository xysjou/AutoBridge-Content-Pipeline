# Live-site repair handoff

This is a defect inventory and a review candidate, not a publication approval.

- Review AI reviews; it does not write replacement articles.
- Research verifies facts and market/year/trim boundaries; Writing repairs defective text.
- Codex checks reviewed-version integrity, technical configuration and publication safety.
- Automated checks must never be recorded as human review.
- Existing quality-hold noindex protection must not be removed merely to increase index counts.

## Inventory

`review-defects-handoff.json` contains per-page URL, locale, local file/hash and failure reasons.
It covers 3,431 local language pages, including legacy files. Current source content covers
200 themes / 2,400 language pages; 90 themes / 869 language pages trigger the strengthened
checks. Parameter structure checks fail on 81 current themes / 849 language pages.
Legacy content accounts for another 107 themes / 1,031 failed language pages.

The final twelve-locale fallback-label check supersedes the earlier partial-label
counts of 524 current failures and 1,555 total failures. Final total: 1,900 failed
language pages. Theme counts are unchanged; these are newly detected language
variants, not new content defects introduced by technical cleanup.

These are automated findings needing review, not proof that every listed page is live,
factually wrong, or should be deleted. Earlier HTTP samples do not verify current local bytes.
Old numeric quality scores are not editorial approvals.

## BYD SEAL candidate

`byd-seal-correction/candidate.json` is a 12-language correction candidate.
`byd-seal-correction/review-manifest.json` binds its hash, original source hash,
official evidence URL, and each parameter panel/main HTML hash.

The UK MY2026 parameter scheme has been independently accepted in the Review conversation.
The complete 12-language candidate has NOT passed independent review.
Review must check body, FAQs, summary, image metadata, scope consistency and translations.
Report remaining defects; do not convert parameter-only PASS into full-article PASS.
The charging time is omitted because the official PDF contains conflicting statements.

Publication remains blocked until the exact revision passes the required checks.

## Follow-up candidate and readable inventory parts

`byd-seal-correction-v2/` fixes the definite numeric-formatting, scope-container,
indexing-state and image-credit defects in the first review. It deliberately
remains REVISION_REQUIRED: the full multilingual prose still needs targeted
editorial revision. It is not a release candidate.

`review-defects-by-theme/index.json` links to one small file per affected theme.
Use these parts when the connector cannot read the full inventory. The updated
rendered hashes include the local technical-only removal of placeholder tags;
the article prose is unchanged. Do not treat technical cleanup as content PASS.

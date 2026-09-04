# AutoBridge 25-Article Research Return Request

- Batch: `AutoBridge_25_v3_Content_Repair_20260904`
- Reviewed baseline: `c94916e0d31101e81bf77aa8264dea76bcd85d76`
- Review commit: `c9bc8ea`
- Review result: `REVIEW_PASS=0`, `NEEDS_RESEARCH=25`
- Publication state: `BLOCKED`
- Human reviewed: `false`

The independent Review AI returned every article to Research. This file is a
handoff record only; it does not change article content and does not grant
publication approval.

## Required Research Repair

For every article:

1. Provide at least 6 directly accessible, scope-matched source URLs from at
   least 4 independent organizations. Do not add irrelevant URLs to satisfy a
   count.
2. Re-open critical URLs on the repair date and record source organization,
   market, supported fact, model year/version where applicable, and checked
   date.
3. Add an actual image asset and a complete rights record: original URL,
   source page, rights holder, licence, checked date, and model/generation or
   topic match.

For the 9 vehicle pages, lock one exact year, generation, body style,
powertrain, drivetrain, original sales market, production boundary and
trim/derivative. Do not merge family maxima or specifications from different
powertrains or markets.

For the 16 regional guides, define representative countries and add local
official evidence for each claim. Generic international material or one
country cannot establish an Africa, Latin America, Middle East or Southeast
Asia conclusion. Shipping guides additionally require actual port, route,
carrier/terminal conditions and checked/effective dates.

## Writing Repair After Research

Writing AI must use the new Research baseline, rewrite only supported claims,
and regenerate/recheck EN/FR/DE/ES/PT/JA/KO/VI/TH/ID/AR/ZH independently.
Repeated sentence-bank scaffolds, package instructions and workflow text must
not appear in public content. Same-language cross-article similarity must be
recomputed.

## Required Return to Review AI

The repaired package must return to the independent Review AI. It must bind
each `REVIEW_PASS` record to the reviewed Git commit, article SHA-256 and image
SHA-256. Codex will reject any later drift and will publish only the exact
passed artifacts after technical QA.

See `review_report_2026-09-04.md` for all 25 article IDs, source counts, scores
and dispositions.

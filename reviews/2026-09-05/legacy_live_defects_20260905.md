# AutoBridge Legacy Live Defects Review — 2026-09-05

## Scope and boundary

This is a separate Review-AI queue for legacy content already live on autobridgeexport.com. It must not be merged with the 2026-09-02..09-05 daily 60/80-article production batch.

- Review role: content QA only; no drafting and no publishing.
- Codex role: technical diagnosis, generator/rendering fixes, version integrity, noindex/canonical/hreflang/schema deployment checks, and publishing only after REVIEW_PASS.
- Local diagnosis path reported by user: `/Users/shan/Documents/Codex/aws-amplify-auto-update/outputs/diagnosis-2026-09-05/`.
- Review AI did **not** access that local path. Findings below use the user-supplied diagnosis plus independent live-URL verification where noted.
- User-supplied online inventory: 200 main topics × 12 languages; legacy automated audit has 3431 language pages including historical URLs. Main-content failures: 18 topics / 52 locale pages, all observed by the user's diagnostic as HTTP 200 + noindex. Historical failures: 107 topics / 1031 locale pages. The noindex state is a Codex technical concern; it does not itself determine content REVIEW_PASS.

## Review-side conclusion

`LEGACY_LIVE_PUBLICATION_BLOCK = TRUE`

The old automated 100/100 scores are invalid as publication-quality evidence where live semantic defects exist. Source count, word count, and machine presence checks do not override public workflow leakage, factual scope conflicts, bad parameter labels, misleading image captions, or broken locale bodies.

### P0 — live public-content defects independently confirmed

1. `/guides/new-vs-used-ev-middle-east.html` — EN
   - Status: `REVISION_REQUIRED`
   - Evidence supplied by live diagnosis: `deployment or sales team`; `without forcing every page into the same public article structure`; heading/paragraph mismatch.
   - Independent live verification: public body is visibly generator-like and repetitive, using numbered `Regional decision record and stop rules 1..6`, sentence fragments, repeated decision language, and source-note text instead of a coherent buyer article.
   - Required action → Writing AI: remove all production/deployment/writer-facing instructions; rewrite only contaminated blocks into buyer-facing prose; preserve valid evidence and correct paragraphs; do not template-normalize the whole article. Re-QA all 12 locales.

2. `/guides/battery-warranty-southeast-asia.html` — EN
   - Status: `REVISION_REQUIRED`
   - Evidence supplied by live diagnosis: `without forcing every page into the same public article structure`.
   - Independent live verification: public body contains internal production language such as `Freeze the scope`, `Build a primary-evidence ledger`, `working question`, `staged evidence note`, and `The reviewer uses each source...`; sections are stitched research notes rather than a finished buyer article.
   - Required action → Writing AI: remove research-workflow prose and reconstruct only affected sections around the actual buyer question: warranty territory, transferability, flood/thermal evidence, charging/service pathway, destination differences, and stop conditions. Keep source scope country-specific.

3. `/guides/pickup-export-latin-america.html` — EN
   - Status: `REVISION_REQUIRED`
   - Evidence supplied by live diagnosis: `deployment or sales team` publication instruction.
   - Independent live verification: repeated article title is injected into body paragraphs; repeated `Evidence trail:` lists and process phrases (`Use the final authority and delivered version`, `Make the sample follow...`) expose template/generator structure.
   - Required action → Writing AI: remove writer/deployment instructions, repeated title inserts, and mechanically repeated evidence scaffolding; keep correct duty-cycle, payload, destination and homologation checks; preserve country boundaries and validated sources.

4. `/guides/roro-container-shipping-latin-america.html` — EN
   - Status: `REVISION_REQUIRED`
   - Evidence supplied by live diagnosis: body tells the writer `Do not make the ... page carry numbers or promises`.
   - Independent live verification: repeated title inserts, `Evidence trail:` scaffolding and duplicated process instructions remain public.
   - Required action → Writing AI: convert contaminated scaffolding into finished buyer-facing RoRo-vs-container decision logic; keep route/port/carrier/terminal claims tied to actual evidence; do not invent freight prices or schedules.

5. `/guides/seven-seat-suv-latin-america.html` — EN
   - Status: `REVISION_REQUIRED`
   - Evidence supplied by live diagnosis: publishing-team / article-structure instructions leaked.
   - Independent live verification: repeated title inserts, `Evidence trail:` scaffolding and process commands remain in the public article.
   - Required action → Writing AI: remove generator/publishing instructions and repetitive scaffolding only; retain good third-row, safety, load, climate, destination and after-sales analysis.

6. `/vehicles/byd-seal-global-search-2026.html` — EN + all parameter-derived locales
   - Status: `NEEDS_RESEARCH`
   - P0 defects independently verified:
     - `Key facts` labels are all generic `Detail` rather than factual labels.
     - UK body states `485 L rear boot + 72 L front boot`, while FAQ/Key facts still state `400 L + 53 L`.
     - `5.9`, `3.8`, and `82.5` render as `5. 9`, `3. 8`, `82. 5`.
     - Generic parameter sentences are much longer than the value field should be.
   - Required action → Research AI first: determine which official source, market, model year and trim support `485+72 L` and which support `400+53 L`; do not choose a global number. Lock Design RWD vs Excellence AWD, UK MY2026 scope, battery, range cycle, output, acceleration, charging, dimensions and luggage to exact sources.
   - Required action → Writing AI after Research: rebuild parameter rows with semantic labels and concise values/units; remove template reminders from values; preserve market/version labels; update 12-language parameter bundles and summaries; fix decimal tokenization. Codex separately fixes generator/renderer cause.

## Image truthfulness defects

### `vehicle-inspection-5161920290-jpg.jpg`
User-supplied visual diagnosis (local and online original-image hashes reported identical): image actually shows staff beside a vehicle checking documents. It does **not** depict new-vs-used EVs side by side performing battery diagnostics.

Affected captions/ALT must not claim: battery diagnosis, comparison of new vs used EVs, Middle East location, Southeast Asia location, workshop diagnosis, or first-hand inspection unless the image itself and provenance prove those facts.

Current live `/guides/new-vs-used-ev-middle-east.html` caption claims `New and used electric cars receiving battery diagnostics before international export (Middle East)`.

- Status: `REVISION_REQUIRED`
- Severity: `P0` because the caption invents activity/location and can imply experience not shown by the asset.
- Required action → Writing AI: use literal visible-description ALT/caption only, e.g. staff checking vehicle documentation beside a vehicle, unless independent metadata proves more.

### `battery-pack-of-an-ev-jpg.jpg`
User-supplied visual diagnosis: actual image is a battery/underbody display; it does not show a Latin American or Middle Eastern technician.

Current live `/guides/battery-warranty-southeast-asia.html` caption claims a technician inspecting an EV battery and flood evidence in a tropical Southeast Asian workshop.

- Status: `REVISION_REQUIRED`
- Severity: `P0` for fabricated location/activity.
- Required action → Writing AI: describe only visible battery/underbody content. Do not add region, technician, diagnostic action, flood inspection or lived experience without evidence.

Image copyright/licence remains a separate gate. A visually correct caption does not prove rights.

## Existing main-content failure list from the 2026-09-05 online diagnostic

The following is accepted into the independent legacy-live queue based on the user's diagnostic evidence. These locale failures are `REVISION_REQUIRED` unless a repair uncovers a factual/source-scope conflict, in which case upgrade that article to `NEEDS_RESEARCH`.

| URL | Affected locale(s) | P | Required action |
|---|---|---|---|
| `/guides/mpv-procurement-africa.html` | ja, th | P1 | Writing: repair only failed locale bodies/metadata; compare against EN fact boundary; rerun locale QA and similarity. |
| `/guides/mpv-procurement-middle-east.html` | ja, th | P1 | Writing: same; preserve country-specific scope. |
| `/guides/photo-vin-review-global.html` | ko | P1 | Writing: repair Korean locale; no fabricated inspection/first-hand wording. |
| `/guides/pickup-export-southeast-asia.html` | fr, de, es, pt-br, ja, ko, vi, th, id, ar | P1 | Writing: repair only failed locale bodies; preserve market/country boundaries; map `pt-br` to actual site locale deliberately, not silently. |
| `/vehicles/geely-coolray-global-search-2026.html` | en, fr, de, es, pt-br, ja, ko, vi, th, id, ar | P0/P1 | Writing: remove internal fields/template repetition; preserve verified parameters; if parameter scope conflicts appear, route to Research. |
| `/vehicles/kia-sportage-global-search-2026.html` | en, zh | P0 | Writing: remove internal fields/repeated template; verify parameters remain market/version-scoped. |
| `/vehicles/land-rover-defender-global-search-2026.html` | en, zh | P0 | Same. |
| `/vehicles/lexus-rx-global-search-2026.html` | en, zh | P0 | Same. |
| `/vehicles/mazda-bt-50-global-search-2026.html` | en, zh | P0 | Same; payload/towing values must stay derivative-specific. |
| `/vehicles/mercedes-benz-e-class-global-search-2026.html` | en, zh | P0 | Same. |
| `/vehicles/mercedes-benz-glc-global-search-2026.html` | en, zh | P0 | Same. |
| `/vehicles/nissan-altima-global-search-2026.html` | en, zh | P0 | Same. |
| `/vehicles/nissan-sentra-global-search-2026.html` | en, zh | P0 | Same. |
| `/vehicles/opel-corsa-global-search-2026.html` | en, zh | P0 | Same; keep ICE/HEV/BEV derivatives separate where applicable. |
| `/vehicles/peugeot-208-global-search-2026.html` | en, zh | P0 | Same; keep 208/e-208 derivatives separate. |
| `/vehicles/polestar-2-global-search-2026.html` | en, zh | P0 | Same; battery/range must include test cycle and variant. |
| `/vehicles/porsche-macan-global-search-2026.html` | en, zh | P0 | Same; do not merge ICE legacy Macan and electric Macan generations. |
| `/vehicles/ram-1500-global-search-2026.html` | en, zh | P0 | Same; towing/payload requires engine/cab/bed/drivetrain/axle/package boundary. |

## Historical failure inventory

User-supplied diagnostic: 107 historical topics / 1031 locale pages failed. Review AI has not been given the page-level list in an accessible source and therefore does not assign per-page REVIEW_PASS/REVISION_REQUIRED/NEEDS_RESEARCH yet.

Required Codex handoff to Review AI for this set: URL + locale + current HTTP/index state + source/content file path + current content hash + failure reason. Review AI will then classify content defects. Codex keeps technical noindex/canonical/hreflang/rendering failures separate.

## Parameter-publication gate

A public vehicle parameter must have:

- semantic label (`Battery`, `WLTP range`, `Rear luggage`, etc.), never `Detail`;
- concise value;
- unit;
- exact market;
- model year;
- trim/derivative/powertrain where relevant;
- test cycle where relevant;
- direct supporting source;
- checked date.

Template reminders and buyer instructions belong in prose, not the parameter value field.

If two values conflict across market/year/trim and the source mapping is not resolved, status = `NEEDS_RESEARCH`.

## Final re-review hash contract

No corrected legacy page may inherit an old audit score or old Review PASS after any substantive change.

For each topic submitted to Review AI, the final package must bind:

- `REVIEW_COMMIT_SHA`
- `ARTICLE_ID` / canonical URL
- 12 locale URLs/file paths
- `BODY_SHA256` for each of 12 full bodies
- `SUMMARY_SHA256` for each locale summary/card text
- `PARAM_BUNDLE_SHA256` for the structured key-facts/parameter payload
- `IMAGE_TEXT_SHA256` covering image asset reference + ALT + caption + rights/provenance fields
- `ARTICLE_BUNDLE_SHA256` over canonical serialization of the above
- source-log / fact-sheet versions

Any body, locale, parameter, image ALT/caption, summary or source-boundary change after review sets:

`REVIEW_BASELINE_DRIFT=true`

and invalidates the previous Review result until re-reviewed.

## Current disposition

- The five live workflow-leak guide pages: `REVISION_REQUIRED` → Writing AI.
- BYD SEAL global-search page: `NEEDS_RESEARCH` → Research AI, then Writing AI; Codex separately fixes renderer/generator.
- Two identified misleading image-caption cases: `REVISION_REQUIRED` → Writing AI; rights remain independently gated.
- 18 main-content failure topics / 52 locale failures: enter `LEGACY_LIVE_DEFECT_REPAIR`; no publication approval inherited.
- 107 historical topics / 1031 locale failures: `REVIEW_PENDING_PAGE_LIST`; no content status fabricated without per-page evidence.

`PUBLISH_APPROVED=false`
`HUMAN_REVIEWED=false` unless a real human-review record is separately proven for the repaired version.
`REVIEWED_BY=AI_REVIEWER`

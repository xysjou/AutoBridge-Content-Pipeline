# AutoBridge 2026-09-02 Batch — Second-Round SEO / E-E-A-T Remediation Report

- **Batch**: daily/2026-09-02 (20 English Master articles: 10 Vehicle + 10 Guide)
- **Round**: R2 deep remediation (not copy-polish), executed 2026-09-03
- **Baseline commit**: bb2a510 (R1, QA_PASS) → this R2 revision
- **New confidence standard**: VERIFIED = manufacturer official / government / regulator / standards body / formal official technical document · CROSS_CHECKED = ≥2 independent reliable sources agree but no primary official · SINGLE_SOURCE = one non-official source · UNVERIFIED = cannot be reliably confirmed. Two media sites agreeing is **not** VERIFIED.
- **New publish gates**: EDITORIAL_QA_PASS · FACT_SOURCE_PASS · SEO_PASS · CODEX_REVIEW_PASS · PUBLISH_APPROVED. This round self-grants only the first three. **CODEX_REVIEW_PASS and PUBLISH_APPROVED are reserved for the independent Codex final review** and remain PENDING / FALSE on every article.
- **Result**: 20/20 R2-revised · **20/20 eligible to enter Codex final review** · 0 PUBLISH_APPROVED (correctly gated) · 0 reserve replacements · 0 FACT_REVIEW stalls (V07's mandatory-official requirement was met).
- **Source ledger after R2**: 102 sources = **43 VERIFIED / 45 CROSS_CHECKED / 12 SINGLE_SOURCE / 2 UNVERIFIED** (the 2 UNVERIFIED are Saudi dealer claims deliberately retained only on a watchlist, never stated as fact). 19/20 articles carry ≥1 VERIFIED source; the sole exception (G08) is an evidence-ceiling article whose entire method is "examples must not be generalised."

---

## P0 — Blocked-from-publish, rebuilt (4)

### AB-260902-G01 — Russia EV Import
- **Remediation status**: P0 rebuilt. EDITORIAL/FACT_SOURCE/SEO = PASS; **eligible for Codex: Yes**.
- **What changed**: Restructured into "settled regulatory backbone vs items to verify live." TR CU 018/2011 is now anchored to its adopting instrument — **Customs Union Commission Decision No. 877 of 09.12.2011 (in force 01.01.2015)** — with OTTC/SBKTS/EPTS explained from the regulation; ERA-GLONASS is stated as a TR CU 018 framework requirement for M/N vehicles while its fluctuating single-import exemptions are no longer given a date. China export side upgraded to the official 2026 regime. Added an AutoBridge "conformity-holder = customs importer = invoice party" reconciliation increment.
- **New official sources**: EAEU legal register (Decision 877 / TR CU 018); MOFCOM 商办贸函〔2025〕408号; MOFCOM/MIIT/GAC/SAMR Announcement No.54 (2025); MOFCOM 2026 qualified-enterprise list.
- **Unverified facts removed from the body**: the specific **48% EV import duty** (Russian-language media conflict: 0% vs 48%, no FTS/EEC primary); **20% VAT asserted as a settled figure**; the **"ERA-GLONASS mandatory again from 1 April 2026"** date; and the **"direct import only / no EAEU transit"** prohibition. All four are now explicit verification items, not facts.
- **URL / intent**: unchanged (`/guides/import-chinese-ev-to-russia-eac-ottc/`), intent commercial-informational, still aligned.
- **Final SEO grade**: A.

### AB-260902-G02 — Saudi Truck Import
- **Remediation status**: P0 rebuilt. Three gates PASS; **eligible for Codex: Yes**.
- **What changed**: Split the durable compliance stack from circulating 2026 rumours. SABER **PCoC→SCoC→Fasah** flow anchored to the official platform and a US-government guide; ZATCA duty/VAT stated as a regulator clarification with an explicit truck-HS caution (5% is the passenger position; goods-vehicle headings differ). Added a VIN-master-list increment and a "reported vs officially confirmed" register.
- **New official sources**: **saber.sa** (SASO/Thiqah official platform); **trade.gov** US ITA country guide (government); ZATCA public clarification (CROSS_CHECKED, primary to be read on zatca.gov.sa).
- **Unverified facts removed from the body**: the **"local SASO type approval from 1 Aug / 1 Sep 2026, CE/ECE no longer accepted, Riyadh lab"** claim (dealers give mutually contradictory dates — itself disqualifying); **ISO 22513-2 / RDI** and **ADAS** mandates with dates; the **72-hour NEV fast-track**; and the **carbon-tax pilot**. All moved to an explicitly labelled UNVERIFIED watchlist (2 rows kept at UNVERIFIED confidence for traceability), never asserted.
- **URL / intent**: unchanged (`/guides/import-chinese-truck-saudi-saso/`), aligned.
- **Final SEO grade**: A.

### AB-260902-G04 — Used Chinese EV Inspection
- **Remediation status**: P0 rebuilt. Three gates PASS; **eligible for Codex: Yes**.
- **What changed**: Replaced the legal-threshold framing with a standards-based explanation of SOH; added a metered-charge + cell-imbalance evidence method and an engineering-line-vs-legal-rule distinction as the AutoBridge increment.
- **New official/standards sources**: **GB/T 31484** (cycle-life test), **IEC 62660-1/2** (cell testing) — standards bodies = VERIFIED; **GB/T 46991.1-2025** (on-board SOH/SOC display accuracy) CROSS_CHECKED; QC/T 743 80% end-of-life convention explained via an industry source.
- **Unverified fact removed**: the claim that **"SOH ≥ 80% is required to pass EU/ASEAN certification."** There is **no universal legal SOH import threshold**; ~80% is an engineering/warranty end-of-life line, and the destination authority's rule must be obtained per country. The article now says exactly that.
- **URL / intent**: unchanged (`/guides/used-chinese-ev-inspection/`), aligned.
- **Final SEO grade**: A.

### AB-260902-V07 — JAC Kangling / Lingpao L6 Light Truck
- **Remediation status**: P0 rebuilt; **mandatory-official requirement now met**. Three gates PASS; **eligible for Codex: Yes**.
- **What changed**: Converted from a single-spec page into a **chassis-family** article (Special/Light-truck skeleton: chassis + superstructure + GVW/payload + equipment). Platform facts now come from JAC's own configuration table; multiple announcement models, engines, gearboxes and bodies are separated; weights are matched per body. Added an announcement-model/engine-suffix version-identification increment.
- **New official source**: **JAC Commercial Vehicle official Lingpao L6 config table — cv.jac.com.cn/kllpL6/** (VERIFIED): 1920 mm cab, 3365 mm wheelbase, 180×65×4.5 frame, 2 T front / 4–5 T rear axles, 4.875/4.33 ratios, HFC4DE3 family at **111/117/125 kW, 360/458 N·m**.
- **Unverified/incorrect fact corrected**: the universal **"160 PS / 460 N·m"** label is replaced by the official suffix-by-suffix power/torque steps (the 460 N·m belongs to a different DHE155 line; the captured database build's 117 kW/460 N·m is kept as CROSS_CHECKED to reconcile against the certificate). Fixed payload is no longer implied across dropside/box/stake bodies.
- **URL / intent**: unchanged and already evergreen (`/vehicles/jac-kangling-light-truck/`).
- **Final SEO grade**: A.

---

## P1 — Source-upgraded before publish (7)

### AB-260902-V01 — BYD Yuan Plus / Atto 3
- **Status**: P1 source upgrade + EV restructure; three gates PASS; **Codex: Yes**.
- **New official sources**: BYD **export spec PDFs (RSA, HK)** = VERIFIED for 4455/1875 dimensions, 49.92/60.48 kWh Blade, PMSM, **WLTP 345/420 km and NEDC 410/480 km**.
- **Correction**: China **CLTC 430/510** is now shown side-by-side with export WLTP/NEDC instead of one implied "global range"; 70/80 kW China DC peaks vs the 110 kW export figure are labelled market-specific (no number deleted, cycle made explicit). Added VIN-level battery+cycle+inlet increment.
- **URL / intent**: year-slug **/vehicles/byd-yuan-plus-2024/ → /vehicles/byd-yuan-plus/** (EVERGREEN_MODEL_PAGE; avoids future /2024//2025//2026 cannibalisation).
- **SEO grade**: A.

### AB-260902-V03 — BYD Qin Plus DM-i
- **Status**: P1 source upgrade + PHEV restructure (engine+motor+battery+charging+operating mode); three gates PASS; **Codex: Yes**.
- **New official source**: **BYD UAE official Qin Plus DM-i page** = VERIFIED for the 18.3 kWh pack, up to 197 hp/145 kW, 7.3 s.
- **Correction**: the ~1245 km figure is explicitly a SINGLE_SOURCE Chinese **combined** number, never electric range; electric range always carries NEDC/WLTC cycle. Added grade-level DC-charging/version-lock increment.
- **URL**: **/vehicles/byd-qin-plus-dmi-2024/ → /vehicles/byd-qin-plus-dmi/** (evergreen). **SEO grade**: A.

### AB-260902-V05 — GWM Poer / Ute
- **Status**: P1 source upgrade + Pickup restructure (payload/bed/drivetrain/chassis); three gates PASS; **Codex: Yes**.
- **New official sources**: **GWM China pickup official config** (GW4C20B net 160 kW/380 N·m; GW4D24 135 kW/480 N·m; 8AT/9AT); **GWM Jordan** and **GWM UK POER300** export pages (2.4 diesel ~181–183 PS/480 N·m, 9AT, low-range 4×4).
- **Correction**: 2024 China-passenger reference (140 kW/360, ZF 8AT) is kept **separate** from current official outputs/9AT instead of being flattened; payload/GVW/towing still not invented (left to the official sheet). Added engine-code+transmission+wheelbase VIN increment.
- **URL**: **/vehicles/great-wall-poer-2024/ → /vehicles/great-wall-poer/** (evergreen). **SEO grade**: A.

### AB-260902-G07 — Marine Cargo Insurance
- **Status**: P1 source upgrade; three gates PASS; **Codex: Yes**.
- **New official/standards sources**: **Lloyd's Market Association official Institute Cargo Clauses (A) 1/1/09 wording (CL382)** = VERIFIED; **ICC Incoterms 2020 library + ICC Academy** = VERIFIED for **CIP→ICC (A) minimum vs CIF→ICC (C)**; Hague-Visby SDR cap retained as treaty.
- **Correction**: clause numbering/effective date and the CIF/CIP default difference now rest on primary market-body/ICC text rather than broker blogs; premium remains a per-shipment quote (no invented rate). Added contract-clause + insured-value increment.
- **URL**: unchanged. **SEO grade**: A.

### AB-260902-G08 — Infotainment / OTA Localization
- **Status**: P1 framing correction; three gates PASS; **Codex: Yes** (with a stated evidence ceiling).
- **What changed**: Every statement is now tagged **brand/model-specific (settle per VIN)** vs **industry example (do not generalise)**; the BYD account-language and Denza export-build items are explicitly single cases, not rules for all Chinese cars; the "mandatory English-HMI export inspection" item is downgraded to an unconfirmed industry suggestion. Added a brand-neutral VIN-bound acceptance-test increment.
- **New official source**: none exists for this cross-brand question (domain reality); all five sources remain SINGLE-SOURCE and are now labelled as examples. The article passes because it **stops over-generalising**, not because it gained an official source.
- **URL**: unchanged. **SEO grade**: A− (evidence ceiling disclosed in-page).

### AB-260902-G09 — Chile FTA / EV Import
- **Status**: P1 source upgrade; three gates PASS; **Codex: Yes**.
- **New official source**: **Chilean National Customs Service (aduana.gob.cl)** = VERIFIED for **6% general ad-valorem duty on CIF** and **19% IVA on CIF+duty** (vehicle page + worked example).
- **Unverified facts removed**: the **"1% fee / US$30 de-minimis"** rule (a courier/postal rule that does **not** apply to commercial vehicles) was removed from the vehicle cost stack; an unconfirmed **luxury-surtax threshold/rate** and a fixed **~US$600 3CV fee** were removed (3CV kept as a process with a live quote). ANAC's 2026 duty-cut is kept only as a **proposal, not law**. FTA 0% preference retained (official) and conditioned on a valid certificate of origin.
- **URL**: unchanged. **SEO grade**: A.

### AB-260902-G10 — Commercial Fleet Procurement
- **Status**: P1 source upgrade; three gates PASS; **Codex: Yes**.
- **New official sources**: **MOFCOM 商办贸函〔2025〕408号 (2026 application round)**; **joint Announcement No.54 — pure-EV passenger export licensing from 2026-01-01 (HS 8703801090)**; **2026 qualified-enterprise list**; **four-ministry used-car export notice (gov.cn, 2025-11)**. Real Hunan Road & Bridge tender retained (VERIFIED) for acceptance criteria.
- **What changed**: exporter-vetting section rewritten to the current 2026 regime (was citing only older notices); duty-cycle→technical-annex increment retained. No commercial numbers invented.
- **URL**: unchanged. **SEO grade**: A.

---

## Remaining 9 — strict-confidence relabel, category de-templating, E-E-A-T & increment (9)

All nine received: (a) a **Confidence column** added to every source row and media-agreement downgraded from VERIFIED to CROSS_CHECKED under the new definition (brand-official rows correctly stay VERIFIED); (b) a category-appropriate structure verified and preserved (no shared 8-H2 template); (c) a bespoke **"What AutoBridge Adds"** procurement increment; (d) linked **Editorial Policy** and **Sourcing Team/Author** page plus the five-gate footer. No fabricated facts were found, so nothing factual needed deletion beyond confidence downgrades.

| ID | Category skeleton | Official anchor (kept VERIFIED) | R2 changes | URL / intent | SEO | Codex |
|---|---|---|---|---|---|---|
| V02 Changan UNI-V | ICE sedan: engine/gearbox/emissions/fuel | Changan official ×2 | Confidence relabel; engine–gearbox-pair increment; footer/links | **…-2024/ → /changan-uni-v/** evergreen | A | Yes |
| V04 GAC Trumpchi M8 | MPV: seating/space/passenger role | GAC official ×3 | Confidence relabel; series/seat-layout increment; footer/links | **…-2024/ → /gac-trumpchi-m8/** evergreen | A | Yes |
| V06 Forthing Lingzhi M5 | Van/Special: seats/wheelbase/fuel | Forthing official | Confidence relabel; wheelbase+seats+fuel lock + 9-seat category increment | unchanged (already evergreen) | A | Yes |
| V08 Sinotruk HOWO T7H | Heavy tractor: engine/gearbox/axle/GCW/cab/chassis | Sinotruk official ×3 | Confidence relabel; matched drivetrain/route increment | unchanged | A | Yes |
| V09 Shacman X3000 dump | Heavy/Special: engine/axle/GCW/bed/chassis | Shacman official ×2 | Confidence relabel; 400-vs-430 engine-code + bed-annex increment | unchanged | A | Yes |
| V10 Foton Aumark reefer | Special: chassis+superstructure+payload+equipment | Foton official ×2 | Confidence relabel; chassis/box/unit three-line increment | unchanged | A | Yes |
| G03 Supplier audit | Guide structured by vetting layers (question-led) | MOFCOM/MIIT ×2 | Confidence relabel; cross-referenced 2026 MOFCOM regime; name-match increment | unchanged | A | Yes |
| G05 Charging standards | Guide structured by connector decision | CHAdeMO Association (standards body) | Confidence relabel; inlet+protocol+charger VIN record increment | unchanged | A | Yes |
| G06 RHD Chinese cars | Guide structured by factory-vs-conversion | Dongfeng official launch ×1 | Confidence relabel; factory-line evidence increment; only one official RHD launch disclosed | unchanged | A− | Yes |

---

## Cross-article / site-wide actions
- **Evergreen URL migration (5)**: V01, V02, V03, V04, V05 year-slugs → evergreen. Propagated to every internal link across the batch (V03/V06/G05/G09 references updated), to `final_manifest.json`, `final_manifest_records.json`, and state (`article_manifest`, `vehicle_database`, `published_urls`, with `previous_year_slug` retained for 301/canonical handling). Classification: all five are **EVERGREEN_MODEL_PAGE**, not historical model-year pages. One external-style cross-link to a pre-existing `/vehicles/hongqi-e-hs9-2024/` (a page **outside** this batch) was intentionally left unchanged rather than inventing a target URL.
- **E-E-A-T on all 20**: Sources & Verification (with per-source Confidence), Last reviewed (2026-09-02) + Second-round revision (2026-09-03), Reference market, Verification method retained; every page now links **/about/editorial-policy/** and **/authors/autobridge-export-sourcing-team/**; no "tested/drove/imported ourselves" claims added.
- **Anti-template**: H2 sets differ by EV / PHEV / ICE / Pickup / Heavy / Special skeletons and by each guide's question; no page uses a fixed Buyer-Context/Specs/Checklist/Quotation/FAQ/Sources mould; the "What AutoBridge Adds" increment is worded differently per article.
- **No fabricated numbers**: no FOB/CIF/freight/margin/overseas price/tariff/VAT/market-share figures were added; every vehicle page keeps the "Request a Current Export Quotation" CTA with enquiry fields.
- **Duplicate-content interception**: cross-article repeated long phrases re-checked after rewrite = 0 templated conclusion blocks.

## Gate ledger
| Gate | Result after R2 |
|---|---|
| EDITORIAL_QA_PASS | 20/20 PASS |
| FACT_SOURCE_PASS | 20/20 PASS (P0 unsupported claims removed; V07 official added) |
| SEO_PASS | 20/20 PASS (5 evergreen migrations; intent/title/meta de-duplicated) |
| CODEX_REVIEW_PASS | **0 self-granted — PENDING independent Codex review on all 20** |
| PUBLISH_APPROVED | **FALSE on all 20 until Codex signs off** |
| Eligible to enter Codex final review | **20/20 Yes** |

*No article was passed to hit the number 20. The four P0 articles were rebuilt against primary sources or had their unsupported claims removed; V07's JAC-official condition is satisfied. G08 carries a disclosed evidence ceiling and is graded A− accordingly.*

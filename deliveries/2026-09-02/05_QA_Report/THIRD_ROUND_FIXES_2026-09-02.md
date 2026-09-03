# Third-Round Targeted Fixes (R3) — Batch 2026-09-02

- **Date:** 2026-09-03
- **Scope rule:** R3 is point-fix only. The other 13 articles were **not** rewritten; they received only the two batch-wide corrections.
- **Batch-wide changes (all 20):**
  1. Internal links corrected to live site paths: `/authors/autobridge-export-sourcing-team/` → `/authors/`; `/about/editorial-policy/` → `/editorial-policy/` (no fabricated/dead links).
  2. "What AutoBridge Adds" blocks de-claimed: every "AutoBridge produces/runs/checks/our desk builds…" first-person operation was reframed as **recommended method / editorial procurement framework** ("this guide recommends…", "the recommended method is…"), consistent with the site's document-research / no-first-hand-claim boundary.
- **Targeted fact-boundary fixes (7):** V01, V03, G01, G02, G04, G07, G08 — each re-ran FACT_SOURCE_QA.
- **New permanent rules:** 5 added to root `LESSONS_LEARNED.md` (see end).
- **Gates:** no article self-granted `CODEX_REVIEW_PASS` or `PUBLISH_APPROVED`. All 20 are **CODEX_REVIEW_PENDING**; `PUBLISH_APPROVED=FALSE` throughout.

---

## 1. Per-article R3 status

| Article | Type | R3 status | Targeted fact fix (summary) | FACT_SOURCE re-QA | CODEX eligible |
|---|---|---|---|---|---|
| AB-260902-V01 BYD Yuan Plus | Vehicle | **R3_FIXED** | "Export Atto 3 equivalent" → "regional Atto 3 reference with the same *nominal* battery capacity"; explicit non-1:1-trim caveat; China CLTC / export WLTP·NEDC kept market-separate | PASS | **CODEX_REVIEW_PENDING** |
| AB-260902-V02 Changan UNI-V | Vehicle | **R3_FIXED** | Batch-wide only (links + de-claim) | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-V03 BYD Qin Plus DM-i | Vehicle | **R3_FIXED** | en-bh source re-labelled **Bahrain (not UAE)**; "export Seal 05 DM-i" same-model inference removed from meta/body/FAQ; OEM-proof alias rule stated | PASS | CODEX_REVIEW_PENDING |
| AB-260902-V04 GAC Trumpchi M8 | Vehicle | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-V05 GWM Poer | Vehicle | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-V06 Forthing Lingzhi M5 | Vehicle | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-V07 JAC Kangling L6 | Vehicle | **R3_FIXED** | Batch-wide only (JAC official/MIIT grounding from R2 retained) | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-V08 Sinotruk HOWO T7H | Vehicle | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-V09 Shacman X3000 | Vehicle | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-V10 Foton Aumark Reefer | Vehicle | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-G01 Russia EV Import | Guide | **R3_FIXED** | Two absolutes softened to risk-control; direct Decision 877/TR CU 018 full-text link added | PASS | CODEX_REVIEW_PENDING |
| AB-260902-G02 Saudi Truck Import | Guide | **R3_FIXED** | **FACT_SOURCE_PASS withdrawn → rebuilt HS-first → re-passed**; ZATCA 5%/15% confined to light-vehicle scope; title/H1/SEO re-centred off "5% truck duty" | PASS (re-pass) | CODEX_REVIEW_PENDING |
| AB-260902-G03 Supplier Vetting | Guide | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-G04 Used Chinese EV Inspection | Guide | **R3_FIXED** | "85% NMC warning line" deleted; 80% given three "not" statements; 20→80% metered test redefined as screening cross-check (losses/thermal/temp/BMS calibration/buffer); absolute causality removed | PASS | CODEX_REVIEW_PENDING |
| AB-260902-G05 Charging Compatibility | Guide | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-G06 RHD Chinese Cars | Guide | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-G07 Marine Cargo Insurance | Guide | **R3_FIXED** | Two 110% rules split (Incoterms = ≥110% of contract price; UCP/silent LC = ≥110% of determinable CIF/CIP); single "CIF×110%" formula removed; ICC(A) made subject to exclusions/attachment/wording | PASS | CODEX_REVIEW_PENDING |
| AB-260902-G08 Infotainment/OTA | Guide | **R3_FIXED** | Residual "Chinese cars always/domestic builds" generalisation reduced to *some parallel-imported China-market vehicles / reported cases / a risk to test for*; explicit **Evidence Ceiling** section added (5× SINGLE_SOURCE, no official cross-brand source) | PASS | CODEX_REVIEW_PENDING |
| AB-260902-G09 Chile FTA EV Import | Guide | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |
| AB-260902-G10 Commercial Fleet Procurement | Guide | **R3_FIXED** | Batch-wide only | unchanged PASS | CODEX_REVIEW_PENDING |

**Totals:** R3_FIXED = 20 · R3_UNRESOLVED = 0 blocking · targeted FACT_SOURCE re-QA PASS = 7 · CODEX_REVIEW_PENDING = 20 · self-granted CODEX_REVIEW_PASS/PUBLISH_APPROVED = 0.

---

## 2. What changed in each targeted article

### V01 — BYD Yuan Plus
- **Deleted/changed:** table column "Export Atto 3 equivalent (BYD-official)" → **"Regional Atto 3 reference — same *nominal* battery capacity (BYD-official, market-specific)"**; cells now read "Regional Atto 3 builds with a nominal 49.92/60.48 kWh pack: WLTP ≈… / NEDC ≈…".
- **Added:** explicit sentence that regional Atto 3 figures are **not one-to-one trim equivalents** of China 430/510 — certified range/power/equipment/charge differ by country; confirm the destination sheet for the VIN.
- **Kept (correctly):** China CLTC vs export WLTP/NEDC separation; GB/T vs destination connector; BYD ZA/HK official PDFs.
- **Deleted unverified facts:** none needed beyond removing the equivalence claim.

### V03 — BYD Qin Plus DM-i
- **Source-market correction (SOURCE_MARKET_PATH_CHECK):** `byd.com/en-bh/...` was tagged "Export/UAE" — **en-bh = Bahrain**. Source row now "Export / **Bahrain (regional en-bh page; not UAE)**", confidence tagged VERIFIED **with scope = this named Qin Plus DM-i only**.
- **Model-identity (MODEL_ALIAS_REQUIRES_OEM_PROOF):** removed every "export Seal 05 DM-i" identity statement — Meta Description, Secondary Terms, body, FAQ and confidence note. New wording: BYD presents a **Qin Plus DM-i** on overseas pages; a differently named BYD PHEV is **RELATED_MODEL ≠ SAME_MODEL** unless BYD explicitly states the alias. Platform/powertrain/looks are not proof.
- **Deleted unverified facts:** the inferred unified export nameplate; the UAE market tag.

### G01 — Russia / EAEU EV import
- **Softened absolutes (mandatory wording now reserved for cited regulation):**
  - "importer, conformity holder and invoice **must be the same legal entity**" → "documents whose legal entities are **reconciled**… a procurement risk-control step; precise requirements confirmed with the accredited body/broker."
  - "A Chinese e-call system **is not accepted** as ERA-GLONASS" → "**do not assume** a Chinese-market e-call unit satisfies ERA-GLONASS/УВЭОС — confirm with the accredited body."
  - Operating step and FAQ rewritten to the same risk-control register.
- **Direct reviewable source added:** Decision No. 877 / TR CU 018/2011 consolidated full text (amended through 2026) at GARANT `https://base.garant.ru/483421115/` (CROSS_CHECKED direct document page), replacing the citation-only mirror; the EAEU register remains the VERIFIED index.
- **Open, non-blocking note:** a stable article-level URL on the regulator's own `eec.eaeunion.org/pravo.eaeunion.org` domain was not surfaced in this pass; the direct consolidated text is provided via a recognised legal database and the decision number is unambiguous. Codex may optionally substitute a regulator-domain deep link.

### G02 — Saudi truck import (withdrawn → rebuilt → re-passed)
- **Gate trajectory:** FACT_SOURCE_PASS **withdrawn at R3 start** per instruction; rebuilt; **re-passed** after the rebuild removed scope overreach.
- **Rebuilt HS-first (HS_FIRST_FOR_IMPORT_RULES):** new order **exact HS subheading (87.01/87.04/87.05/8716) → SABER technical regulation for that code → required certificate type (PCoC/SCoC vs other COC/QM/self-declaration/vehicle-specific) → Fasah customs**. Removed the prior assumption that every commercial truck uniformly runs PCoC→SCoC→Fasah.
- **ZATCA scope (PRIMARY_SOURCE_SCOPE_MUST_MATCH):** 5% customs + 15% VAT now expressly confined to the **light-vehicle calculator scope**; commercial trucks must classify HS → read the current ZATCA/GCC tariff line → apply VAT to the applicable customs basis. **No truck duty percentage is stated.**
- **SEO/intent:** SEO Title, H1 and Meta re-centred from a "5% duty" framing to HS-first routing (URL slug unchanged to avoid churn); WCO HS nomenclature added as a VERIFIED standards source.

### G04 — Used Chinese EV inspection
- **Deleted:** the unsourced "more conservative ~85% (NMC) warning line" (and the 80–85 negotiation figure); replaced with an explicit statement that **no** chemistry-specific 85% rule is asserted.
- **80% three-not:** not a used-car import threshold; not a unified battery-retirement law; not every manufacturer's warranty threshold.
- **Metered test redefined:** heading now "a **Screening Cross-Check, Not an SOH Calculation**"; charger-delivered kWh ≠ stored energy (charging/conversion losses, thermal-management draw, ambient/pack temperature, BMS SOC calibration, reserve buffer); it flags only **gross anomalies**; removed "material shortfall indicates genuine capacity loss"; formal SOH requires a qualified diagnostic/manufacturer data. New FAQ on the same point.

### G07 — Marine cargo insurance
- **Two 110% rules separated:** Incoterms® 2020 seller duty = cover ≥ **110% of contract price**; documentary credit/UCP (silent LC) = ≥ **110% of determinable CIF/CIP value**. Removed the universal "insured amount = CIF × 110%"; checklist and FAQ updated.
- **ICC(A) wording:** table/body now "broad all-risks cover **subject to exclusions, attachment of cover and policy wording**; *may* respond to accidental transit/handling damage…" — no unconditional theft/scratch/loading guarantee.

### G08 — Infotainment / OTA
- Residual universal subjects reduced: "A China-domestic unit is engineered… does not work abroad" → "typically… a risk to test, not a statement that every unit fails"; provider reports now "**reported cases of some parallel-imported China-market vehicles**"; FAQ navigation answer scoped to "some China-market builds".
- **New "Evidence Ceiling" section:** all 5 sources SINGLE_SOURCE; no official cross-brand source; named cases support only themselves; no claim that all/most Chinese cars share the defects; article value = per-VIN test framework.

---

## 3. Batch-wide de-claim audit (all 20)
Grep-verified after edit: **zero** remaining `AutoBridge produces/runs/checks/builds/converts/…` or `we build/run/maintain` first-person operation claims; **zero** old internal paths (`/about/editorial-policy/`, `/authors/autobridge-export-sourcing-team/`). Value-add blocks now use recommended/editorial framing while preserving the concrete procurement increment (VIN binding, HS classification, inquiry fields, payment-before checks).

## 4. Source-market sweep (new lesson applied batch-wide)
Checked every region-coded OEM URL against its Market label: V01 `/za/`=RSA, `/hk/`=HK; V05 gwmjordan=JO, gwmcars.co.uk=UK; V03 en-bh corrected to Bahrain. **No other mismatch found.**

## 5. NEW_LESSONS_ADDED (permanent)
Written to root **`LESSONS_LEARNED.md`** (binding for all future batches):
1. `SOURCE_MARKET_PATH_CHECK` — source Market must match the true URL/page country; region code vs dealer vs selector conflicts trigger re-verification.
2. `MODEL_ALIAS_REQUIRES_OEM_PROOF` — export name/overseas version/same-car is an identity fact needing explicit OEM proof; otherwise RELATED_MODEL ≠ SAME_MODEL.
3. `HS_FIRST_FOR_IMPORT_RULES` — commercial import: HS code → technical regulation → certificate/tariff → process; no uniform-flow-first.
4. `FIRST_HAND_EXPERIENCE_MUST_BE_TRUE` — no invented AutoBridge operations; use editorial/recommended framing; internal links must be live.
5. `PRIMARY_SOURCE_SCOPE_MUST_MATCH` — check authority AND scope; an official light-vehicle/passenger/specific-market source cannot be extrapolated.
(The file also restates the binding confidence vocabulary and the must/prohibited/required wording rule.)

## 6. Final gate state
- EDITORIAL_QA_PASS = PASS (20/20) · FACT_SOURCE_PASS = PASS (20/20; G02 withdrawn→re-passed) · SEO_PASS = PASS (20/20)
- CODEX_REVIEW_PASS = **PENDING (20/20 — independent Codex review required)**
- PUBLISH_APPROVED = **FALSE (20/20)**
- Final status of all 20: **CODEX_REVIEW_PENDING**. No blocking factual issue remains; the single non-blocking note (G01 regulator-domain deep link) is listed for Codex.

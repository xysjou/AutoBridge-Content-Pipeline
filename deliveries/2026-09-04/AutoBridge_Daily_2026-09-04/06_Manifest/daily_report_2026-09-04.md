# DAILY REPORT — 2026-09-04 (Writing AI · Research-Rebase Correction)

**Stage**: articles re-aligned from v1.0 draft to final Research baseline v1.1/v1.2 (RESEARCH_BASELINE_DRIFT corrected). No full rewrite of all 20.

## Counts
- Planned articles: 20
- Actual completed: 20 (Vehicle 10/10 · Procurement Guide 10/10)
- EDITORIAL_QA_PASS: 20
- FACT_SOURCE_PASS: 15
- FACT_SOURCE_CONDITIONAL: 5 (V04, G02, G05, G06, G10)
- FACT_SOURCE_FAIL: 0
- SEO_PASS: 20 · QA_FAIL: 0 · FACT_REVIEW_REQUIRED: 0
- Reserve replacements: 0 · Repeated historical errors blocked: 0
- Articles changed in rebase: 11 · Bodies retained after delta check: 9
- CODEX_REVIEW_PENDING: 20 · PUBLISH_APPROVED: 0 (Writing AI does not self-approve) · HUMAN_REVIEWED: 0
- Cross-article 5-gram Jaccard max: 0.068 (manual-review threshold 0.50 / fail 0.70 — both clear)
- Publish-grade Source Gate (separate layer, >=6 URLs/>=4 orgs): MAIN PASS 4 (G01,G07,G08,G09), publish-grade CONDITIONAL 16 (Research source-depth follow-up; not a body-fact defect).
- Late-pull drift: fact_sheets/source_logs delta = 0 (body facts unchanged); only publish-grade metadata gate added and recorded.
- Multilingual: Master EN only; 12-language localization queued for the independent localization task.

## Rebase baseline
- Repo HEAD at rebase start: 2f5bb26
- RESEARCH_READY sha: 2fab8fd1 · HANDOFF sha: aa2e8b94 · LESSONS sha: 9983ae7
- Fact sheet versions: v1.2 = V04,V07,G05,G08,G09,G10; v1.1 = other 14.

## Articles
| Article ID | Title | Word file | Rebase | Fact QA | Status |
|---|---|---|---|---|---|
| AB-260904-V01 | Chery Arrizo 8 Specs & Export Buyer Guide (1.6TGDI, China Reference) | VEH_20260904_01_Chery_Arrizo8.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V02 | BYD Qin L DM-i PHEV Specs & Export Guide (5th-Gen DM, CLTC) | VEH_20260904_02_BYD_QinL_DMi.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V03 | Wuling Bingo EV Specs & Export Buyer Guide (203/333/410 km CLTC) | VEH_20260904_03_Wuling_Bingo.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V04 | Haval Jolion / Haval Chulian Identity & Market-Specific Specs — Export | VEH_20260904_04_GWM_Haval_Jolion.docx | CHANGED | CONDITIONAL | QA_PASS → CODEX_PENDING |
| AB-260904-V05 | Chery Fulwin T9 C-DM PHEV Specs & Export Guide (China Reference) | VEH_20260904_05_Chery_FulwinT9.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V06 | GAC Trumpchi E8 PHEV MPV Specs & Export Guide (7-Seat, China) | VEH_20260904_06_GAC_Trumpchi_E8.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V07 | JAC T9 Hunter Diesel Pickup Specs & Export Guide (Bed, 4WD) | VEH_20260904_07_JAC_T9Hunter.docx | CHANGED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V08 | JMC Shunda Light Truck Specs & Export Guide (GVW 4.27t, China-6) | VEH_20260904_08_JMC_Shunda.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V09 | Dongfeng Tianlong KL Tractor Specs & Export Guide (DDi11 465, GCW 40t) | VEH_20260904_09_Dongfeng_TianlongKL.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-V10 | Dongfeng Tianjin KR Refrigerated Truck Specs & Export Guide (18t) | VEH_20260904_10_Dongfeng_TianjinKR.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-G01 | Vehicle Export HS Code Classification Guide — 8701/8702/8703/8704/8705 | GUIDE_20260904_01_Vehicle_Export_HS_Code.docx | CHANGED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-G02 | China Vehicle Export Statutory Inspection & Declaration Guide (HS-by-H | GUIDE_20260904_02_China_Export_Inspection_Declaration.docx | CHANGED | CONDITIONAL | QA_PASS → CODEX_PENDING |
| AB-260904-G03 | China Certificate of Origin for Vehicle Exports — CO Types & Issuers | GUIDE_20260904_03_Certificate_of_Origin.docx | RETAINED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-G04 | Vehicle Export Bill of Lading Guide — MBL/HBL/Telex/SWB + Maritime Cod | GUIDE_20260904_04_Bill_of_Lading_Types.docx | CHANGED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-G05 | Vehicle Export PDI & Pre-Shipment Handover Guide — Named Carrier Rules | GUIDE_20260904_05_PDI_Pre_Shipment.docx | CHANGED | CONDITIONAL | QA_PASS → CODEX_PENDING |
| AB-260904-G06 | China VI Emissions & Overseas Fuel Compatibility Guide — GB18352.6 / G | GUIDE_20260904_06_Emission_Fuel_Compatibility.docx | CHANGED | CONDITIONAL | QA_PASS → CODEX_PENDING |
| AB-260904-G07 | VIN & Nameplate Verification for Chinese Vehicle Imports — GB 16735-20 | GUIDE_20260904_07_VIN_Nameplate.docx | CHANGED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-G08 | EV Sea Freight Under IMDG 42-24 — UN3556/3557/3558 vs UN3480/3481 | GUIDE_20260904_08_Battery_Shipping_IMDG.docx | CHANGED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-G09 | China Vehicle Export Document Package Guide — GB/T 21085-2020 Current  | GUIDE_20260904_09_Export_Document_Package.docx | CHANGED | PASS | QA_PASS → CODEX_PENDING |
| AB-260904-G10 | Ocean Freight Charge Structure for Vehicle Export — O/F, THC, DOC, BAF | GUIDE_20260904_10_Shipping_Charge_Structure.docx | CHANGED | CONDITIONAL | QA_PASS → CODEX_PENDING |

## Conditional boundaries (not failures)
- V04 — OEM-proven name identity; Chinese torque/gearbox blocked (AU-only source); overseas HEV separate.
- G02 — inspection framework primary-verified; per-10-digit-HS catalogue status checked live; no blanket yes/no.
- G05 — WW/Höegh named carrier policy; checklist is editorial recommendation; fixed lashing/SOC values blocked.
- G06 — Chinese standards primary-verified; overseas Euro/EPA limits and equivalence blocked.
- G10 — charge structure only; AMS/ACI/ENS route-specific; all amounts blocked.

## Key rebase corrections (11 changed)
- G01: primary basis → 2026 Import/Export Tariff + GACC 2026 implementation announcement.
- G02: set CONDITIONAL; HS-by-HS catalogue decision; statutory inspection vs PSI vs BEV licence separated.
- G04: Maritime Code 2025 revision (in force 2026-05-01) Arts.80/81/87 added → PASS.
- G05: WW/Höegh named CARRIER_SPECIFIC; PDI/photo/handover = AutoBridge recommended checklist; over-certain phrasing removed.
- G06: MEE/SAMR GB18352.6-2016/XG1-2026 + GB17691-2018 light/heavy split; GB19147 sulphur.
- G07: GB16735-2019 official text; unverified 'L/some H' origin rule removed.
- G08: MSA IMDG 42-24 + UNECE Rev.8+Amd.1 + 49 CFR; Sohu/11467 demoted to supporting.
- G09: multi-stage rule removed (draft-only); GB/T21085-2020 current; 20260041-Q-339 future/draft.
- G10: AMS/ACI/ENS route-specific editorial guidance; amounts remain blocked.
- V04: Chulian↔Jolion SAME_MODEL on GWM OEM proof; AU 210N·m/7DCT removed from Chinese spec; HEV separate.
- V07: dual-JAC SAME_MODEL; 3500kg = EXPORT only; CN powertrain kept SINGLE_SOURCE.

## Awaiting / blockers
- FACT_SOURCE_FAIL: none. AWAITING_RESEARCH: none. Needs human/independent Codex review: all 20 (normal gate, not a defect).

# AutoBridge 25-Article Independent Publication Review — 2026-09-04

- Batch: `AutoBridge_25_v3_Content_Repair_20260904`
- Reviewed content baseline: `c94916e0d31101e81bf77aa8264dea76bcd85d76`
- Review role: `AI_REVIEWER` — final content quality gate
- Formal source artifact: original DOCX. The article SHA-256 in the handoff is the digest recorded by the mechanical review Markdown for that DOCX; Codex must recalculate it before any future technical publication gate.
- `PUBLISH_APPROVED=false`
- `HUMAN_REVIEWED=false`

## Batch verdict

- TOTAL ARTICLES: **25**
- REVIEW_PASS: **0**
- REVISION_REQUIRED: **0**
- NEEDS_RESEARCH: **25**
- REJECT: **0**

**Publication decision:** no article from this locked baseline may be uploaded, added to Sitemap, or exposed for indexing. Codex receives **zero publication candidates**.

## Independent findings

1. **Source gate — 25/25 fail.** Direct inspection of the evidence tables shows only 1–4 source URLs per article. The publication gate requires at least 6 directly accessible, scope-matched URLs and at least 4 independent organizations. After normalizing multiple pages from the same OEM as one organization, no article reaches 4 organizations.
2. **Image-rights gate — 25/25 fail.** The locked batch supplies no actual image asset plus source page, rights holder, licence and checked date. The wording `keep the current image only when rights/licence are documented` is a condition, not evidence. ALT alone is not sufficient.
3. **Vehicle boundary gate — 9/9 vehicle pages fail.** These pages are family/derivative verification guides and do not establish one fully locked publishable Vehicle record covering year, generation, body, powertrain, drivetrain, original sales market, production boundary and exact trim/derivative. Several explicitly compare multiple powertrains or grades.
4. **Regional-scope gate — 16/16 regional guides fail.** The evidence tables contain only 2–4 URLs and do not provide adequate representative-country local evidence for Africa, Latin America, Middle East or Southeast Asia. Generic UNECE/IMO/safety material or one country is not a regional regulatory/import basis.
5. **Multilingual uniqueness is not publication-cleared.** The package self-QA and English-only similarity result were not inherited. Independent spot checks found repeated translated sentence-bank/scaffold patterns across vehicle and guide pages. All 12 locales must be regenerated/rechecked after the Research baseline changes. Exact per-language maxima are intentionally not fabricated in this P0-blocked review.
6. **Internal package/deployment text must remain non-public.** Deployment-role, release-state and workflow instructions are packaging metadata and must not be rendered as public page content.

## Per-article disposition

| Article ID | Type | Source URLs | Source orgs | Score | Final status | Return target |
|---|---|---:|---:|---:|---|---|
| `AB50_001_Vehicle_GAC_AION_Y_Plus` | VEHICLE | 2 | 1 | 55 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_003_Vehicle_2026_GMC_Sierra_1500` | VEHICLE | 1 | 1 | 52 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_004_Vehicle_2026_Kia_Sorento` | VEHICLE | 3 | 1 | 58 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_007_Vehicle_2026_Lexus_NX` | VEHICLE | 2 | 1 | 55 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_010_Vehicle_2026_Mazda_CX_5` | VEHICLE | 2 | 1 | 55 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_011_Vehicle_2026_Mercedes_Benz_C_Class` | VEHICLE | 2 | 1 | 55 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_014_Vehicle_MG_ZS` | VEHICLE | 2 | 1 | 55 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_016_Vehicle_Nissan_Qashqai` | VEHICLE | 2 | 1 | 55 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_020_Vehicle_Peugeot_3008_E_3008` | VEHICLE | 1 | 1 | 52 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_024_Guide_battery_warranty_southeast_asia` | REGIONAL_GUIDE | 4 | 3 | 56 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_031_Guide_mpv_procurement_latin_america` | REGIONAL_GUIDE | 2 | 2 | 50 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_033_Guide_mpv_procurement_southeast_asia` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_034_Guide_new_vs_used_ev_middle_east` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_035_Guide_new_vs_used_ev_southeast_asia` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_036_Guide_photo_vin_review_africa` | REGIONAL_GUIDE | 2 | 2 | 50 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_038_Guide_photo_vin_review_latin_america` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_039_Guide_photo_vin_review_middle_east` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_040_Guide_photo_vin_review_southeast_asia` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_041_Guide_pickup_export_africa` | REGIONAL_GUIDE | 2 | 2 | 50 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_042_Guide_pickup_export_latin_america` | REGIONAL_GUIDE | 2 | 2 | 50 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_043_Guide_pickup_export_middle_east` | REGIONAL_GUIDE | 2 | 2 | 50 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_046_Guide_roro_container_shipping_latin_america` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_048_Guide_roro_container_shipping_southeast_asia` | REGIONAL_GUIDE | 4 | 3 | 56 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_049_Guide_seven_seat_suv_africa` | REGIONAL_GUIDE | 2 | 2 | 50 | **NEEDS_RESEARCH** | Research AI → Writing AI |
| `AB50_050_Guide_seven_seat_suv_latin_america` | REGIONAL_GUIDE | 3 | 3 | 53 | **NEEDS_RESEARCH** | Research AI → Writing AI |

## Exact remediation requirements

### Vehicle pages
Research AI must build a new baseline with >=6 scope-matched URLs / >=4 independent organizations and lock one exact year + generation + body + powertrain + drivetrain + original market + production boundary + trim/derivative evidence matrix. Family maxima and different powertrains cannot be merged. Add an actual licensed/matched image asset and rights record. Writing AI then resynchronizes EN/FR/DE/ES/PT/JA/KO/VI/TH/ID/AR/ZH and recomputes same-language 5-gram similarity.

### Regional guides
Research AI must choose representative countries and add country-local official evidence. A single Mexico/Saudi/Singapore example, generic UNECE/IMO material or a safety-rating body cannot prove an entire region. Shipping topics additionally need actual port, route, carrier/terminal condition and checked/effective date. Add an actual licensed/matched image asset and rights record. Writing AI then resynchronizes all 12 locales and recomputes similarity.

## Language review status

All 25 contain EN/FR/DE/ES/PT/JA/KO/VI/TH/ID/AR/ZH sections, but every locale is recorded as `REVISION_REQUIRED` because the Research baseline must change. Independent spot checks also found reusable translation scaffolds. A locale cannot inherit PASS from English or from package self-QA.

## Image review

`IMAGE_RIGHTS_STATUS=FAIL` for all 25. Required per article: actual asset path/original URL, source page, rights holder, licence, checked date, model/generation/topic match and natural ALT in all 12 locales.

## SEO/content status

Title/Meta/H1 and 12-locale URL maps exist, but `SEO_CONTENT_STATUS=REVISION_REQUIRED` because P0 evidence changes require another content/translation pass. Vehicle structured data after revision is limited to `Article + Vehicle`; no Product/Offer/price/shipping/return fields. Canonical/hreflang/robots/RTL/Sitemap rendering is Codex's technical gate only after a future `REVIEW_PASS`.

## Codex handoff

**Publication candidates: NONE.**

Codex must not upload this batch from reviewed baseline `c94916e0d31101e81bf77aa8264dea76bcd85d76`. Any repaired DOCX/source/translation/image creates a new content hash/baseline and must return to Review AI before publication.
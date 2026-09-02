# Used Chinese EV Pre-Export Inspection: Battery SOH, Accident, Flood and Odometer Checks

## SEO Metadata
- **SEO Title**: Used Chinese EV Inspection Checklist: SOH, Accident & Flood
- **Meta Description**: Operational pre-export inspection for a used Chinese EV — reading battery SOH and cell balance, a 20–80% charge test, accident/flood/fire screening, odometer-vs-cycle checks and rejection rules.
- **Suggested URL**: /guides/used-chinese-ev-inspection/
- **H1**: Inspecting a Used Chinese EV Before Export: A Technical Checklist
- **Primary Keyword**: used Chinese EV inspection checklist battery SOH accident
- **Secondary Search Terms**: EV battery SOH test, used EV cell voltage imbalance, EV flood damage check, odometer rollback battery cycle, used EV export SOH threshold
- **Internal Link Suggestions**: /guides/verify-china-car-export-supplier/ ; /guides/chinese-ev-charging-standard-compatibility/ ; /guides/import-chinese-ev-to-russia-eac-ottc/
- **Image Suggestions**: SOH readout on diagnostic tool; 20-80% charge test worksheet; battery undertray inspection points; service/claims record sample
- **ALT Suggestions**: "Diagnostic tool reading used EV battery state of health"; "20 to 80 percent charge energy test worksheet"; "EV battery pack undertray inspection"

## Scope: This Is an Inspection Manual, Not a Buy-New-vs-Used Decision

This guide assumes the decision to buy **used** is already made and covers the **technical inspection before export**. It does not compare new versus used value (a separate topic). The economics of a used EV depend overwhelmingly on the high-voltage battery, which is why the inspection logic differs from an ICE car: a cheap body with a degraded pack can be worthless after shipping, while battery replacement can exceed the vehicle's value.

## 1. Battery State of Health (SOH) — the Primary Number

**SOH** expresses the pack's current usable capacity as a proportion of its when-new capacity. Industry guidance treats **SOH around/above 80%** as retaining normal service value; below that, degradation accelerates and replacement cost is very high. Reference warning lines differ slightly by chemistry — roughly **80% for LFP (phosphate) and 85% for NMC (ternary)** packs (method-level references; brand standards vary).

How to obtain it:

- Read the in-car/cluster battery-health display where available.
- Prefer an **independent third-party diagnostic report** that records SOH **and the maximum cell-to-cell voltage difference** (a large imbalance flags weak modules even when headline SOH looks acceptable).
- There is no single universal OBD readout standard across Chinese brands, and third-party report formats are not standardised — so **commission a reputable inspector, keep the report, and avoid promising an exact SOH number you cannot evidence**. Brand-specific official battery-health/warranty criteria were not captured and should be requested from the brand where possible.

## 2. Run a Live Charge Test

A static SOH figure can be misrepresented; a charge test cross-checks it. The method used by used-EV inspectors: charge from about **20% to 80%** and compare the energy actually delivered (from a metered charger) against the expected ~60% of usable pack capacity. A large shortfall indicates real capacity loss. Record start/end SOC, kWh delivered, charging power curve and time; a pack that also cannot sustain its expected charge rate warrants deeper inspection. Combine this with the charging-standard check (GB/T in China vs the destination connector) so a healthy battery is not let down by an incompatible charge interface.

## 3. The "Three-Electric" System (Battery, Motor, Controller)

Inspect the high-voltage triad beyond SOH:

- **Battery pack underside**: remove/inspect the bottom shield for removal/reseal marks, scrapes, deformation or repair evidence.
- **Motor and power electronics**: scan for fault codes, check for warning lamps and verify smooth drive/regen behaviour on a road test.
- **High-voltage cabling and connectors**: look for corrosion, retermination or non-factory repairs.

## 4. Accident, Flood and Fire Screening

Used-EV history screening must specifically cover collision, **water immersion (flood)** and fire/thermal events:

- Pull **maintenance/service records and insurance claim (出险) records**; any sheet-metal/structural repair or flood-water claim marker is grounds to reject.
- Flooded EVs carry hidden risk of pack-density loss and wiring-harness corrosion; inspect under-dash connectors, seat rails, fuse boxes and the battery enclosure for water lines or corrosion.
- Check panel gaps, paint thickness and bolt/fastener witness marks for structural repair; inspect for any battery-pack opening that suggests post-incident rework.

## 5. Odometer vs Battery Cycles — Catching a Rollback

A hallmark of a clocked EV is an **odometer reading inconsistent with battery charge-cycle count and wear state**. Where diagnostic data exposes cycle count, compare it against displayed mileage and seat/steering/pedal wear. A low displayed mileage paired with high cycle counts or aged components is a rollback warning.

## 6. Export Threshold and Paperwork

Industry guidance for export markets (e.g., EU/ASEAN-type regimes) commonly expects **SOH ≥ 80%** for a used EV to clear certification/value expectations; below it, the car can effectively lose export viability. This is a **general market reference, not a universal legal number** — the destination certification body's current standard governs, so confirm it for the specific country. Keep the third-party SOH/inspection report, the charge-test record and service/claims history with the export dossier; several markets also require these for used-vehicle type/import procedures. (China's own used-car export qualification/age rules were not re-verified in this research — obtain the current MOFCOM position rather than relying on older statements.)

## Hard Rejection Rules (Walk Away)

- SOH below the destination threshold (or below ~80% where no specific rule exists) without a priced-in battery plan.
- Any flood/fire marker in claims records, or corrosion/water lines in the pack or harness.
- Structural/accident repair to high-voltage areas or evidence the battery pack was opened non-commercially.
- Odometer inconsistent with battery cycles and wear, with no credible explanation.
- Seller refuses a live charge test or an independent diagnostic report.

## Pre-Purchase Inspection Checklist

- Independent report with SOH and max cell-voltage imbalance.
- Metered 20→80% charge test recorded (SOC, kWh, power, time).
- Battery undertray and HV connectors inspected for removal/corrosion.
- Service + insurance-claim history pulled; collision/flood/fire markers checked.
- Odometer reconciled with battery cycles and physical wear.
- Destination used-EV certification/SOH threshold confirmed in writing.
- Charging-interface compatibility (GB/T vs destination) verified.

## Frequently Asked Questions

**What SOH is acceptable for an exported used EV?** Around 80%+ is the common reference (LFP ~80%, NMC ~85% warning lines), but the destination certification body's current rule decides — confirm it rather than assuming.
**How do I verify SOH if brands differ?** Use the in-car display plus an independent diagnostic report showing SOH and cell imbalance; keep the report as evidence because there is no universal OBD standard.
**Can a charge test expose a bad battery?** Yes — metering the energy from 20% to 80% and comparing to expected capacity reveals real degradation that a static number may hide.
**Why is flood damage especially dangerous in an EV?** It can degrade the pack and corrode hidden harnesses/connectors, creating safety and reliability failures after export.
**How is odometer fraud spotted on an EV?** Compare displayed mileage with battery charge-cycle count and component wear; a low odometer with high cycles is a warning.

## Sources & Verification

| Source title | Organization | Market | URL | Checked | Supported facts |
|---|---|---|---|---|---|
| Core points for buying used NEVs | Yiche (易车, auto media) | CN | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-02 | SOH definition, ≥80% service value, reading methods |
| Used-EV battery charge test (video, method reference) | Dongchedi (懂车帝) | CN | https://www.iesdouyin.com/share/video/7618925618490849457 | 2026-09-02 | 20→80% metered charge comparison method |
| Three ways to rule out accident/flood/clocked EVs (video) | Dongchedi (懂车帝) | CN | https://www.iesdouyin.com/share/video/7678314679869430004 | 2026-09-02 | Accident/flood/odometer methods, undertray marks |
| SOH chemistry warning lines (video, method reference) | Douyin industry content | CN | https://www.iesdouyin.com/share/video/7674527923274474225 | 2026-09-02 | LFP 80% / NMC 85% reference lines |
| 2026 used-NEV export guide | Jingsuncar (industry) | Global | https://www.jingsuncar.com/news/2026-must-see-guide-for-buying-used-new-energy-85493284.html | 2026-09-02 | Export SOH ≥80% common threshold (destination standard governs) |

*Verification note: SOH concepts are media/industry-supported and several methods come from low-authority video content used only as method references; no exact SOH is promised and an independent third-party report is recommended. Brand battery standards and current China used-car export rules were not captured and must be obtained from primary sources.*

## Editorial Review
- **Reviewed by**: AutoBridge Export Sourcing Team
- **Last reviewed**: 2026-09-02
- **Reference market**: Global (China used-EV export side)
- **Verification method**: Media/industry methods with explicit limits; third-party inspection recommended; numeric thresholds framed as references
- **Content status**: QA_PASS (Master/EN)

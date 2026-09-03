# AutoBridge Content Pipeline — Lessons Learned (Permanent Rules)

These are durable editorial/sourcing rules that correct recurring fact-boundary failures. Every research and writing stage MUST apply them. When a rule is invoked, record it in the batch QA report.

---

## LESSON: SOURCE_MARKET_PATH_CHECK
A source's **Market must match the real country/region of its URL/page** — never the market we expected or hoped for.
- The URL region code (e.g. `en-bh` = Bahrain, `en-ae` = UAE, `/za/` = South Africa, `/hk/` = Hong Kong), the dealer/entity named on the page, and the country selector can conflict.
- When they conflict, re-verify the actual market before tagging; do **not** default to "UAE / Europe / Global" by assumption.
- A regional/global page must be labelled "Regional (country X)" with its true scope, not upgraded to a broader market.
- Trigger example (2026-09-02 R3): `byd.com/en-bh/car/qin-plus-dmi` was mislabelled "UAE"; `en-bh` is **Bahrain**.

## LESSON: MODEL_ALIAS_REQUIRES_OEM_PROOF
"Export name", "overseas version", "same car", "equivalent/对应车型" are **model-identity facts** and require **explicit OEM proof**.
- Shared platform, identical powertrain, similar appearance, a media nickname, or a parameter-site comparison do **not** establish SAME_MODEL.
- Without explicit OEM statement of the alias, the relationship is at most **RELATED_MODEL ≠ SAME_MODEL**, and specs must not be presented as 1:1 equivalents (including per-trim/range equivalence).
- Regional reference specs may be matched only on a clearly stated dimension (e.g. same *nominal* battery capacity) with an explicit non-equivalence caveat.

## LESSON: HS_FIRST_FOR_IMPORT_RULES
Commercial-vehicle import rules MUST be built in this order:
**exact HS code → applicable technical regulation → required certificate/tariff type → shipment/customs process.**
- Never write a single national "uniform process" first and add "different models may vary" as an afterthought.
- Headings 87.01 / 87.04 / 87.05 / 8716 and their subheadings can map to different technical regulations, different certificate forms (COC/QM/self-declaration/vehicle-specific process) and different tariff lines.
- A passenger/light-vehicle rule, calculator or rate must never be presented as the commercial-truck rule; check both the authority AND the scope of the source.

## LESSON: FIRST_HAND_EXPERIENCE_MUST_BE_TRUE
Do **not** invent first-hand AutoBridge operations to manufacture E-E-A-T.
- Claims such as "AutoBridge produces / runs / checks / our sourcing desk…" are allowed only for actions AutoBridge genuinely and routinely performs, with real operational evidence.
- Where there is no such record, use editorial/recommended framing: "AutoBridge's recommended sourcing method…", "This guide recommends…", "Our editorial procurement framework…".
- The site's standing evidence boundary (document research; no first-hand test/drive/import/teardown claim) must never be broken by body copy.
- Internal links must point only to pages that actually exist on the live site (no fabricated author/policy URLs).

## LESSON: PRIMARY_SOURCE_SCOPE_MUST_MATCH
An "official/primary source" is authoritative **only within its stated scope**. Check SOURCE AUTHORITY **and** SOURCE SCOPE.
- An official document may cover only: light vehicles, passenger cars, a specific market, a specific trim, a specific transaction, or a calculator's defined category.
- "Official" does not license extrapolation to other vehicle classes, markets or transactions (e.g. a ZATCA light-vehicle 5%/15% calculator is not a commercial-truck tariff).
- Tag the scope in the source row; keep out-of-scope use as a verification item, not a fact.

---

### Confidence vocabulary (binding)
- **VERIFIED** — manufacturer OEM site, government/regulator, standards body, or formal official technical document (scope matched).
- **CROSS_CHECKED** — two or more independent reliable sources agree, but no primary/official first-hand source.
- **SINGLE_SOURCE** — one non-official source.
- **UNVERIFIED** — cannot be reliably confirmed.
Two agreeing media sites are never automatically VERIFIED.

### Mandatory/legal wording
Use **must / prohibited / required** only where a cited regulation or official document directly states the obligation. Otherwise use risk-control/recommended language ("reconcile…", "do not assume…", "confirm in writing…").

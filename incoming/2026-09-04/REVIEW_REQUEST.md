# AutoBridge 25-Article Independent Review Request

- Batch: `AutoBridge_25_v3_Content_Repair_20260904`
- Article count: 25
- Source archive SHA-256: `034ab45fa302f51b217138ba1de66548ce16f280ba8591b48edd67a681fccb0a`
- Publication status: `PUBLICATION_HOLD`
- Human reviewed: `false`
- Publish approved: `false`

## Review Inputs

- Original DOCX files: `AutoBridge_25_v3_Content_Repair_20260904/articles/`
- Mechanical Markdown exports: `AutoBridge_25_v3_Content_Repair_20260904/review_markdown/`
- Original package metadata and self-QA files: `AutoBridge_25_v3_Content_Repair_20260904/`
- Original ZIP: `AutoBridge_25_v3_Content_Repair_20260904.zip`

Each Markdown export records the SHA-256 digest of its source DOCX. The export is
for review access only and does not replace the DOCX as the source artifact.

## Required Review Output

The independent Review AI must not inherit any `PASS`, `FINAL`, or self-QA
status from the package. It must create:

- `review_handoff_2026-09-04.json`
- `review_report_2026-09-04.md`

Only records with `REVIEW_STATUS=REVIEW_PASS`, a reviewed Git commit, and
matching SHA-256 article and image hashes may proceed to the Codex technical
publication gate.

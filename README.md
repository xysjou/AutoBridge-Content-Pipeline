# AutoBridge-Content-Pipeline

Long-term multilingual article production and QA pipeline for AutoBridge Export.

## Article navigation

The active version is shown by each article's CURRENT pointer.

- [Batch 1 manifest — 43 articles](batches/batch_20260831_001/manifest.json)
- [Batch 2 manifest — 50 articles](batches/batch_20260901_001/manifest.json)
- [Batch index](batches/index.json)
- [Batch 2 v2 QA report](reports/batch2_v2_qa.json)

### Batch 2 examples

- [AB50-001 — GAC AION Y Plus](batches/batch_20260901_001/articles/AB50_001_Vehicle_GAC_AION_Y_Plus/versions/v2.md)
- [AB50-002 — Geely New Coolray](batches/batch_20260901_001/articles/AB50_002_Vehicle_Geely_New_Coolray/versions/v2.md)
- [AB50-024 — Battery warranty, Southeast Asia](batches/batch_20260901_001/articles/AB50_024_Guide_battery_warranty_southeast_asia/versions/v2.md)
- [AB50-050 — Seven-seat SUV, Latin America](batches/batch_20260901_001/articles/AB50_050_Guide_seven_seat_suv_latin_america/versions/v2.md)

For the complete list, open the Batch 2 manifest and follow each article_id into its article directory. The repository currently publishes EN/ZH content; v1 remains immutable for every article.

## Pipeline

- [Pipeline package](pipeline/)
- [Versioning policy](VERSIONING.md)
- [Run pipeline workflow](.github/workflows/run-pipeline.yml)

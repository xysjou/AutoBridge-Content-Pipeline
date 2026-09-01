# Long-lived pipeline

The pipeline is manifest-driven and durable across runs. SQLite stores batches, article items, QA runs, retry entries, and checkpoints. The command python -m pipeline.run_pipeline batches/batch_20260831_001/manifest.json is safe to repeat: article versions remain immutable while status and QA records are updated.

QA checks required bilingual markers and a minimum body length. Failures can be placed in retry_queue with exponential backoff. Checkpoints record the processed cursor so a resumed run can continue after interruption.

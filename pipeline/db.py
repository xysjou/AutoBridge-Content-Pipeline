import sqlite3
from pathlib import Path
SCHEMA='''CREATE TABLE IF NOT EXISTS batches (batch_id TEXT PRIMARY KEY, manifest_path TEXT NOT NULL, status TEXT NOT NULL, updated_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS items (batch_id TEXT NOT NULL, article_id TEXT NOT NULL, version TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(batch_id,article_id)); CREATE TABLE IF NOT EXISTS checkpoints (batch_id TEXT PRIMARY KEY, cursor INTEGER NOT NULL, updated_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS qa_runs (id INTEGER PRIMARY KEY AUTOINCREMENT, batch_id TEXT NOT NULL, passed INTEGER NOT NULL, checked_at TEXT NOT NULL, report_path TEXT NOT NULL); CREATE TABLE IF NOT EXISTS retry_queue (batch_id TEXT NOT NULL, article_id TEXT NOT NULL, attempts INTEGER NOT NULL, next_retry_at TEXT NOT NULL, last_error TEXT, PRIMARY KEY(batch_id,article_id));'''
def connect(path='pipeline.db'):
 Path(path).parent.mkdir(parents=True,exist_ok=True); db=sqlite3.connect(path); db.executescript(SCHEMA); return db
def upsert_items(db,batch_id,articles):
 db.executemany('INSERT INTO items(batch_id,article_id,version,status) VALUES(?,?,?,?) ON CONFLICT(batch_id,article_id) DO UPDATE SET version=excluded.version,status=excluded.status',[(batch_id,a['article_id'],a.get('version','v1'),a.get('status','PENDING')) for a in articles]); db.commit()

import argparse,json,sys
from pathlib import Path
from .db import connect,upsert_items
from .qa import validate_batch,write_report
from .checkpoint import save
def run(manifest_path,db_path='pipeline.db',report_path=None):
 manifest=json.loads(Path(manifest_path).read_text(encoding='utf-8')); db=connect(db_path); upsert_items(db,manifest['batch_id'],manifest['articles']); save(db,manifest['batch_id'],len(manifest['articles'])); report=validate_batch(manifest); report_path=report_path or str(Path('reports')/(manifest['batch_id']+'_qa.json')); write_report(report,report_path); db.execute("INSERT INTO qa_runs(batch_id,passed,checked_at,report_path) VALUES(?,?,datetime('now'),?)",(manifest['batch_id'],int(report['passed']),report_path)); db.commit(); return report
def main():
 p=argparse.ArgumentParser(description='Manifest-driven import, QA, checkpoint, and retry bookkeeping'); p.add_argument('manifest'); p.add_argument('--db',default='pipeline.db'); p.add_argument('--report'); a=p.parse_args(); r=run(a.manifest,a.db,a.report); print(json.dumps({'batch_id':r['batch_id'],'passed':r['passed']})); return 0 if r['passed'] else 1
if __name__=='__main__': sys.exit(main())

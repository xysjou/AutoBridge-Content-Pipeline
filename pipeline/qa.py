import json
from pathlib import Path
REQUIRED=('SEO Title:','Meta Description:','H1:','# EN — English','# ZH — 中文')
def validate_article(path):
 text=Path(path).read_text(encoding='utf-8'); missing=[m for m in REQUIRED if m not in text]; return {'path':str(path),'ok':not missing and len(text)>=500,'missing':missing,'chars':len(text)}
def validate_batch(manifest,root='.'):
 rows=[]
 for a in manifest['articles']:
  p=Path(root)/'batches'/manifest['batch_id']/ 'articles'/a['article_id']/'versions'/'v1.md'; rows.append(validate_article(p) if p.exists() else {'path':str(p),'ok':False,'missing':['file'],'chars':0})
 return {'batch_id':manifest['batch_id'],'passed':all(r['ok'] for r in rows),'articles':rows}
def write_report(report,path):
 Path(path).parent.mkdir(parents=True,exist_ok=True); Path(path).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

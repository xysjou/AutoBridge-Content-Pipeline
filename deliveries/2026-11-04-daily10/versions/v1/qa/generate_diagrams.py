import json,html,unicodedata,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def units(s):return sum(0 if unicodedata.combining(c) else 2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)
def wrap(s,limit):
 words=s.split(' ') if ' ' in s else list(s);sep=' ' if ' ' in s else '';lines=[];cur=''
 for w in words:
  c=(cur+sep+w) if cur else w
  if cur and units(c)>limit:lines.append(cur);cur=w
  else:cur=c
 if cur:lines.append(cur)
 out=[]
 for line in lines:
  p=''
  for c in line:
   if p and units(p+c)>limit and not unicodedata.combining(c):out.append(p);p=c
   else:p+=c
  if p:out.append(p)
 return out
for d in sorted((R/'articles').iterdir()):
 rows=[]
 for mp in sorted(d.glob('seo_*.json')):
  m=json.loads(mp.read_text());l=mp.stem[4:];im=m.get('image',{});labels=im.get('labels',[])
  if len(labels)!=3:continue
  rtl=l=='ar';direction='rtl' if rtl else 'ltr';x=1136 if rtl else 64
  lines=wrap(m['h1'],57)
  if len(lines)>4:raise Exception('Title too long '+str(mp))
  s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" lang="{l}" role="img" aria-labelledby="title desc">',f'<title id="title">{html.escape(im["alt"])}</title><desc id="desc">{html.escape(im["caption"])}</desc>','<rect width="1200" height="630" fill="#f4f5f7"/><rect width="1200" height="12" fill="#167a75"/>','<style>text{font-family:"Noto Sans","Noto Sans CJK SC","Noto Sans Arabic","Noto Sans Thai",sans-serif}</style>']
  for j,line in enumerate(lines):s.append(f'<text id="title_{j}" x="{x}" y="{70+j*43}" font-size="33" font-weight="700" fill="#173331" text-anchor="start" direction="{direction}">{html.escape(line)}</text>')
  for i,label in enumerate(labels):
   cx=64+(2-i if rtl else i)*365;tx=cx+314 if rtl else cx+28;ls=wrap(label,21);fs=24 if len(ls)<=7 else 22;step=32 if len(ls)<=7 else 25;sy=328 if len(ls)<=7 else 310
   if len(ls)>9:raise Exception('Label too long '+str(mp))
   s.append(f'<rect x="{cx}" y="224" width="342" height="310" rx="20" fill="white" stroke="#d9e3e2"/>')
   s.append(f'<text id="number_{i}" x="{tx}" y="278" font-size="23" font-weight="700" fill="#167a75" text-anchor="{"end" if rtl else "start"}">0{i+1}</text>')
   for j,line in enumerate(ls):s.append(f'<text id="card{i}_{j}" x="{tx}" y="{sy+j*step}" font-size="{fs}" fill="#253b3a" text-anchor="start" direction="{direction}">{html.escape(line)}</text>')
  s.append('<text id="brand" x="64" y="590" font-size="22" font-weight="700" fill="#167a75">AutoBridge</text></svg>')
  p=R/'assets'/d.name/f'{l}.svg';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(s)+'\n');rows.append(dict(language=l,path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),labels=labels,original_image_url=None,source_page=None,artist='AI-generated original diagram',rights_holder='Generated for AutoBridge',license='Original generated composition; no third-party photographs or illustration copied',usage_basis='Created for this article package',checked_date='2026-11-04',image_semantic_match='Localized three-card editorial checklist, not a vehicle photograph',image_rights_status='ORIGINAL_GENERATED_DIAGRAM'))
  # Metadata is finalized only after all writers finish; this generator is read-only on metadata.
 q=R/'qa/image_records';q.mkdir(exist_ok=True);(q/f'{d.name}.json').write_text(json.dumps(dict(slug=d.name,records=rows),ensure_ascii=False,indent=2)+'\n')
print('SVG count:',len(list((R/'assets').glob('*/*.svg'))))

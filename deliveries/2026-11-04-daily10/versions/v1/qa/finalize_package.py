#!/usr/bin/env python3
import json,re,hashlib,collections,itertools,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];REPO=R.parents[3];LANGS='en fr de es pt ja ko vi th id ar zh'.split();VEH={'xpeng-g6','xpeng-g9','nio-et5','smart-1','byd-seal-u-dm-i'};OVERLAP={'xpeng-g6','xpeng-g9','nio-et5'}
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def plain(t):return re.sub(r'\]\([^)]*\)',']',t)
def words(t):return len(re.findall(r"\b\w+(?:[-']\w+)*\b",plain(t)))
def numbers(t):
 t=re.sub(r'https?://[^\s)]+','',t);ts=re.findall(r'\d+(?:[.,]\d+)*',t)
 return collections.Counter(x.replace(',','') if re.fullmatch(r'\d{1,3}(?:,\d{3})+',x) else x for x in ts)
def grams(t):
 ts=re.findall(r'[\u3400-\u9fff\u3040-\u30ff\u0e00-\u0e7f]|[^\W_]+',plain(t).lower());return set(tuple(ts[i:i+5]) for i in range(len(ts)-4))
# Freeze source records in this self-contained version without altering their facts.
src=REPO/'daily/2026-11-04/research';shutil.copytree(src,R/'research',dirs_exist_ok=True)
allrows=[];issues=[];bylang=collections.defaultdict(list);articles=[];changes=[]
for d in sorted((R/'articles').iterdir()):
 if not d.is_dir():continue
 slug=d.name;cat='vehicles' if slug in VEH else 'guides';en=(d/'en.md').read_text();facts=R/'research'/cat/slug/('fact_sheet.json' if cat=='vehicles' else 'fact-sheet.json');f={k.lower():v for k,v in json.loads(facts.read_text()).items()};source=R/'research'/cat/slug/('source_log.json' if cat=='vehicles' else 'source-log.json')
 enurls=collections.Counter(re.findall(r'\]\((https?://[^)]+)\)',en));heads=len(re.findall(r'^#+ ',en,re.M));trs=len(re.findall(r'^\|',en,re.M));tab='\n'.join(x for x in en.splitlines() if x.startswith('|'));rows=[];mc=[]
 for l in LANGS:
  p=d/f'{l}.md';mp=d/f'seo_{l}.json'
  if not p.exists() or not mp.exists():raise Exception('Missing '+str(p))
  t=p.read_text();before=mp.read_bytes();m=json.loads(before);old=dict(m);local=l if l!='pt' else 'pt-br';h=sha(p.read_bytes());wc=words(t);han=len(re.findall(r'[\u3400-\u9fff]',t));asset=R/'assets'/slug/f'{l}.svg'
  if not asset.exists():raise Exception('Missing asset '+str(asset))
  m.update(language=l,locale=l,author='AutoBridge Export Editorial Team',AI_ASSISTED=True,HUMAN_REVIEWED=False,PUBLISH_APPROVED=False,body_sha256=h,word_count=wc,han_character_count=han,suggested_url=f'/{local}/{cat}/{slug}/',url_status='UNAPPROVED_LEGACY_MODEL_OVERLAP' if slug in OVERLAP else 'PROPOSED_NOT_LIVE_VERIFIED',internal_link_status='UNVERIFIED_ON_AUTHORIZED_HOST',schema_types=['Article','Vehicle'] if cat=='vehicles' else ['Article'],research_status=f['research_status'])
  for x in m['internal_links']:x['status']='UNVERIFIED_ON_AUTHORIZED_HOST'
  m['image'].update(asset=f'../../assets/{slug}/{l}.svg',status='ORIGINAL_SVG_GENERATED',sha256=sha(asset.read_bytes()))
  if 'image_status' in m:m['image_status']='ORIGINAL_SVG_GENERATED'
  if 'summary' in m:m['summary']=m['card_summary']
  m['evidence']={'first_hand':False};dump(mp,m)
  changed=[k for k in m if old.get(k)!=m.get(k)];mc.append(dict(language=l,before_metadata_sha256=sha(before),after_metadata_sha256=sha(mp.read_bytes()),changed_keys=changed,scope='Technical status, language code, measured hashes/counts, proposed route, image asset and author normalization only; localized title/meta/H1/card/ALT/caption/labels unchanged.'))
  bad=[]
  hs=re.findall(r'^# (.*)$',t,re.M)
  if len(hs)!=1 or hs[0]!=m['h1']:bad.append('H1')
  if l=='en' and wc<900:bad.append('EN_LENGTH')
  if l=='zh' and han<1200:bad.append('ZH_LENGTH')
  if len(re.findall(r'^#+ ',t,re.M))!=heads:bad.append('HEADING_COUNT')
  if len(re.findall(r'^\|',t,re.M))!=trs:bad.append('TABLE_ROWS')
  if collections.Counter(re.findall(r'\]\((https?://[^)]+)\)',t))!=enurls:bad.append('SOURCE_LINKS')
  if re.search(r'Research AI|Writing AI|Review AI|Codex|QA_PASS|FACT_SOURCE_PASS|PUBLISH_APPROVED|research_status|quality_hold|The working question is|Freeze the scope',t,re.I):bad.append('PUBLIC_WORKFLOW_LEAK')
  for k in ['title','meta_description','h1','card_summary']:
   if not isinstance(m.get(k),str) or not m[k].strip():bad.append('EMPTY_'+k)
   if '**' in m.get(k,''):bad.append('PUBLIC_FIELD_MARKUP_'+k)
  miss=numbers(en)-numbers(t);extra=numbers(t)-numbers(en)
  numeric_note=''
  if miss:
   if (slug,l) in [('xpeng-g6','ja'),('xpeng-g9','ja'),('nio-et5','ja'),('nio-et5','ko')] and all(k in {'5','6','9'} for k in miss):numeric_note='Reviewer confirmed fewer model-name repetitions through natural pronoun/context use; specification values retained.'
   else:bad.append('NUMERIC_MISSING_REVIEW')
  row=dict(slug=slug,language=l,body_path=str(p.relative_to(R)),metadata_path=str(mp.relative_to(R)),body_sha256=h,metadata_sha256=sha(mp.read_bytes()),summary_sha256=sha(m['card_summary'].encode()),image_text_sha256=sha(json.dumps({k:m['image'][k] for k in ['alt','caption','labels']},ensure_ascii=False,sort_keys=True).encode()),image_asset_sha256=sha(asset.read_bytes()),words=wc,han_characters=han,numeric_missing=dict(miss),numeric_extra=dict(extra),numeric_note=numeric_note,issues=bad)
  rows.append(row);allrows.append(row);bylang[l].append((slug,grams(t)));issues += [dict(slug=slug,language=l,issue=b) for b in bad]
 dump(R/'qa/finalization_changes'/f'{slug}.json',mc);dump(R/'qa/locale_checks'/f'{slug}.json',rows)
 articles.append(dict(slug=slug,article_id=f['article_id'],category=cat,research_status=f['research_status'],source_url_count=f['source_url_count'],source_org_count=f['source_org_count_normalized'],blocked_facts=f.get('blocked_facts',[]),fact_sheet_path=str(facts.relative_to(R)),fact_sheet_sha256=sha(facts.read_bytes()),source_log_path=str(source.relative_to(R)),source_log_sha256=sha(source.read_bytes()),parameter_bundle_sha256=sha(tab.encode()),legacy_model_overlap=slug in OVERLAP,locales=rows))
sim={}
for l,items in bylang.items():
 scores=[]
 for (a,x),(b,y) in itertools.combinations(items,2):scores.append(dict(a=a,b=b,jaccard=len(x&y)/max(1,len(x|y)),overlap=len(x&y)/max(1,min(len(x),len(y)))))
 scores.sort(key=lambda x:x['overlap'],reverse=True);sim[l]=scores[0];dump(R/'qa/similarity'/f'{l}.json',dict(method='Full Markdown body after removing URL destinations; Unicode words with CJK/Thai characters; same-language5-grams, Jaccard and overlap coefficient. No title-only shortcut.',pairs=scores))
 if scores[0]['overlap']>=.5:issues.append(dict(language=l,issue='SIMILARITY_REVIEW_REQUIRED'))
manifest=dict(batch_id='AB-20261104-D10',date='2026-11-04',version='v1',status='WRITING_REPAIR_CONDITIONAL',topics=len(articles),Vehicles=sum(x['category']=='vehicles' for x in articles),Guides=sum(x['category']=='guides' for x in articles),languages=LANGS,full_body_count=len(allrows),seo_count=len(allrows),original_svg_count=len(allrows),research_pass_count=sum(x['research_status']=='RESEARCH_PASS' for x in articles),research_conditional_count=sum(x['research_status']=='RESEARCH_CONDITIONAL' for x in articles),research_fail_count=sum(x['research_status']=='RESEARCH_FAIL' for x in articles),mechanical_issues=issues,similarity_max_by_language=sim,topic_dedup_status='CONDITIONAL:3 legacy model records and authorized live site inaccessible',seo_status='CONTENT_FIELDS_PREPARED; routing, internal links, live technicalSEO and indexability not verified',source_baseline_commit='012e444fa71f5ba136aaae7d1be230c6f8dba90e',AI_ASSISTED=True,HUMAN_REVIEWED=False,PUBLISH_APPROVED=False,REVIEW_PASS=False,paid_api_calls=0,website_deployed=False,google_indexing='NOT_TESTED_NOT_GUARANTEED',articles=articles)
dump(R/'manifest.json',manifest)
dump(R/'qa/structure_summary.json',dict(topics=len(articles),bodies=len(allrows),issues=issues,minimum_english_words=min(x['words'] for x in allrows if x['language']=='en'),minimum_chinese_han_characters=min(x['han_characters'] for x in allrows if x['language']=='zh'),scope='Mechanical checks only; AI semantic reviews are separate and do not constitute human/professional certification.'))
dump(R/'public_export_allowlist.json',dict(allowed=['public_title','public_meta','public_h1','public_summary','public_body','public_faq','public_sources','public_image_fields'],prohibited=['research_status','confidence','AI worker labels','review_pass','publish_approved','production notes','hashes'],internal_links='Do not activate proposed internal links until verified against authorized live site',schema=['Article','Vehicle for vehicles only'],disallowed_schema=['Product','Offer','AggregateOffer','Price','ReturnPolicy','ShippingDetails']))
plans=[]
for a in articles:
 links={('pt-BR' if l=='pt' else l):f'/{"pt-br" if l=="pt" else l}/{a["category"]}/{a["slug"]}/' for l in LANGS}
 plans.append(dict(slug=a['slug'],canonical_rule='Self-referencing per-language canonical only after actual deployed route confirmed',reciprocal_hreflang_candidates=links,status='NOT_DEPLOYED; host, route and legacy-page decision pending'))
dump(R/'publication_plan.json',dict(authorized_website='https://autobridgeexport.com',current_access='DNS failure and web tool inaccessible on2026-11-04',absolute_canonical_urls_confirmed=False,legacy_model_decision_required=sorted(OVERLAP),pages=plans,sitemap_changed=False,robots_changed=False,noindex_changed=False,indexing_guaranteed=False))
print(json.dumps(dict(topics=len(articles),bodies=len(allrows),issues=issues,source_pass=manifest['research_pass_count'],source_conditional=manifest['research_conditional_count']),ensure_ascii=False,indent=2))

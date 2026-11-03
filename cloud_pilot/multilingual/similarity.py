"""Deterministic same-language full-body 5-gram QA, separate from model review."""
import re
from ..contract import ROOT,digest,require

def grams(text):
    # Whitespace-free CJK and Thai scripts use character units; other scripts use words.
    text=re.sub(r'([\u3400-\u9fff\u3040-\u30ff\u0e00-\u0e7f])',r' \1 ',text.casefold())
    tokens=re.findall(r'\w+',text)
    return {tuple(tokens[i:i+5]) for i in range(max(0,len(tokens)-4))}

def body(text):
    lines=text.splitlines();out=[];metadata=False
    for line in lines:
        if re.match(r'^#\s',line):continue
        if re.match(r'^##\s',line):
            if re.search(r'Sources\s*&\s*Verification|Sources et vérification|Quellen und Prüfung|Fuentes y verificación|Fontes e verificação|出典と確認|출처 및 확인|Nguồn và xác minh|แหล่งข้อมูลและการตรวจสอบ|Sumber dan verifikasi|المصادر والتحقق|来源与核验|编辑评审|Editorial Review',line,re.I):break
            metadata=bool(re.search(r'SEO|元数据|メタデータ|메타데이터',line,re.I))
        if not metadata:out.append(line)
    return '\n'.join(out)

def corpus(locale,article_id,root=ROOT):
    docs=[];seen=set()
    for folder in ('batches','daily','deliveries'):
        for p in (root/folder).rglob('*.md'):
            rel=p.relative_to(root).as_posix()
            if article_id in p.name:continue
            if '/'+locale+'/' not in rel and not p.name.endswith('.'+locale+'.md'):continue
            text=body(p.read_text());h=digest(text)
            if not text.strip() or h in seen:continue
            seen.add(h);docs.append(dict(path=rel,body=text,body_hash=h))
    return docs

def assess(article,prior_bodies=(),root=ROOT):
    docs=corpus(article['locale'],article['article_id'],root)
    docs += [dict(path='current-batch:'+str(i),body=t,body_hash=digest(t)) for i,t in enumerate(prior_bodies)]
    candidate=grams(article['body']);maximum=0.;nearest=None
    for d in docs:
        reference=grams(d['body']);union=candidate|reference
        score=len(candidate&reference)/len(union) if union else 0.
        if score>maximum:maximum=score;nearest=d['path']
    result=dict(algorithm='same-language full-body 5-gram Jaccard; CJK/Thai characters, other words',
        locale=article['locale'],body_hash=digest(article['body']),
        corpus_hash=digest([{k:d[k] for k in ('path','body_hash')} for d in docs]),corpus_documents=len(docs),
        maximum=maximum,nearest_path=nearest,manual_review_required=maximum>.50,self_qa_fail=maximum>=.70)
    result['assessment_hash']=digest(result)
    return result

def check(result):
    require(not result['self_qa_fail'],'LOCALE_FULL_BODY_SIMILARITY_FAIL')
    require(not result['manual_review_required'],'LOCALE_SIMILARITY_MANUAL_REVIEW_REQUIRED')

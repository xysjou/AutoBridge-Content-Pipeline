"""Full-text localization with independent evidence-bound review and durable retries."""
import copy
import re
from datetime import datetime
from ..live.policy import now
from ..contract import digest, require
from ..live.stages import LEAK

LOCALES = ('en','fr','de','es','pt','ja','ko','vi','th','id','ar','zh')
LANGUAGES = dict(zip(LOCALES, ('English','French','German','Spanish','Portuguese',
    'Japanese','Korean','Vietnamese','Thai','Indonesian','Arabic','Simplified Chinese')))
CHECKS = {'semantic_fidelity','facts_and_numbers','scope_and_range_cycle',
          'natural_target_language','complete_full_text','source_entailment',
          'metadata_values_only','no_workflow_leakage'}

def request(base, research, locale, version, prior=None, findings=None):
    require(locale in LOCALES and locale != 'en', 'LOCALIZATION_LOCALE')
    return dict(stage='localization',locale=locale,language=LANGUAGES[locale],version=version,
        english_article=base,research=research,prior=prior,findings=findings,
        required_output=dict(title='localized title',meta='localized search description',
            h1='localized H1',summary='localized summary',
            sections='same ordered list of {text,claim_ids} as English; complete localized prose',
            faq='same ordered list of {question,answer,claim_ids}',
            internal_links='exact copy of verified English relative URLs; do not invent or translate paths',
            human_reviewed=False,publish_approved=False),
        instruction='Translate the ENTIRE approved English article and FAQ into the named language, '
            'with natural buyer-facing prose. Keep JSON field keys, ASCII numeric tokens, units, '
            'model/trim identities, source references, claim IDs and URL strings unchanged. '
            'Do not summarize, omit sections, add facts or silently improve the original. '
            'Preserve Markdown heading levels within section text. One H1 is a separate field. '
            'Do not add production labels. Chinese full body must contain at least 1200 Han characters.')

def numbers(text):
    return sorted(re.findall(r'(?<![\w])\d+(?:\.\d+)?(?:/\d+)?',text))

def public_body(p):
    return '\n\n'.join(s['text'] for s in p['sections'])+'\n\n'+'\n\n'.join(
        f['question']+'\n'+f['answer'] for f in p['faq'])

def validate(result, base, locale, version):
    p=result['content']; original=base['public']
    require(set(p)==set(original), 'LOCALIZATION_FIELDS')
    require(p['human_reviewed'] is False and p['publish_approved'] is False, 'LOCALIZATION_APPROVAL')
    for field in ('title','meta','h1','summary'):
        require(isinstance(p[field],str) and p[field].strip() and
                not re.search(r'\*\*|[<>]|^\s*(Title|Meta Description|H1)\s*:',p[field],re.I),
                'LOCALIZED_METADATA_PURITY')
    require(len(p['sections'])==len(original['sections']) and len(p['faq'])==len(original['faq']),
            'LOCALIZATION_INCOMPLETE')
    for section,source in zip(p['sections'],original['sections']):
        require(set(section)=={'text','claim_ids'} and isinstance(section['text'],str) and section['text'].strip(),
                'LOCALIZED_SECTION')
        require(section['claim_ids']==source['claim_ids'], 'LOCALIZED_CLAIM_MAPPING')
        require(numbers(section['text'])==numbers(source['text']), 'LOCALIZED_NUMERIC_DRIFT')
        require(re.findall(r'^#{2,6}\s',section['text'],re.M)==re.findall(r'^#{2,6}\s',source['text'],re.M),
                'LOCALIZED_HEADING_DRIFT')
    for faq,source in zip(p['faq'],original['faq']):
        require(set(faq)=={'question','answer','claim_ids'} and all(isinstance(faq[k],str) and faq[k].strip()
                for k in ('question','answer')), 'LOCALIZED_FAQ')
        require(faq['claim_ids']==source['claim_ids'], 'LOCALIZED_FAQ_CLAIMS')
        require(numbers(faq['question']+' '+faq['answer'])==numbers(source['question']+' '+source['answer']),
                'LOCALIZED_FAQ_NUMERIC_DRIFT')
    require(p['internal_links']==original['internal_links'], 'LOCALIZED_URL_DRIFT')
    for field in ('title','meta','h1','summary'):
        require(numbers(p[field])==numbers(original[field]), 'LOCALIZED_METADATA_NUMBERS')
    body=public_body(p)
    require(not re.search(r'^#\s',body,re.M) and not LEAK.search(body), 'LOCALIZED_PUBLIC_LEAK')
    require(body!=base['body'], 'ENGLISH_COPY_NOT_LOCALIZED')
    if locale=='zh':require(len(re.findall(r'[\u4e00-\u9fff]',body))>=1200, 'CHINESE_BELOW_1200')
    script={'ja':r'[\u3040-\u30ff]','ko':r'[\uac00-\ud7af]',
            'th':r'[\u0e00-\u0e7f]','ar':r'[\u0600-\u06ff]','zh':r'[\u4e00-\u9fff]'}.get(locale)
    if script:require(len(re.findall(script,body))>=100, 'TARGET_SCRIPT_MISSING')
    packet=dict(article_id=base['article_id'],locale=locale,version=version,
        base_content_hash=base['content_hash'],research_hash=base['research_hash'],
        writer_id='writer:'+result['response_id'],public=p,body=body,
        human_reviewed=False,publish_approved=False,production_eligible=False)
    packet['content_hash']=digest(packet)
    return packet

def review_request(article,base,research):
    return dict(stage='independent_locale_review',article=article,english_article=base,research=research,
        required_output=dict(content_hash=article['content_hash'],base_content_hash=base['content_hash'],
            decision='REVIEW_PASS | REVISION_REQUIRED | NEEDS_RESEARCH | REJECT',
            checks={k:'boolean' for k in sorted(CHECKS)},findings='list of concrete correction findings',
            human_reviewed=False,publish_approved=False),
        instruction='Independently read the full target-language article, English original and source evidence. '
            'Check natural language, completeness, numbers, meaning, SEO fields, market/trim/CLTC scope '
            'and source entailment. Short summaries are failures. Never self-certify human review or publication. '
            'REVIEW_PASS is only an automated locale-draft verdict for this exact hash.')

def validate_review(result,article,base):
    p=result['content']
    require(set(p)=={'content_hash','base_content_hash','decision','checks','findings','human_reviewed','publish_approved'},
            'LOCALE_REVIEW_FIELDS')
    require(p['content_hash']==article['content_hash'] and p['base_content_hash']==base['content_hash'],
            'LOCALE_REVIEW_HASH')
    require(article['content_hash']==digest({k:v for k,v in article.items() if k!='content_hash'}),
            'LOCALE_ARTICLE_CHANGED')
    require('writer:'+result['response_id']!=article['writer_id'], 'LOCALE_REVIEWER_IDENTITY')
    require(p['human_reviewed'] is False and p['publish_approved'] is False, 'LOCALE_REVIEW_APPROVAL')
    require(set(p['checks'])==CHECKS and all(type(v) is bool for v in p['checks'].values()), 'LOCALE_REVIEW_CHECKS')
    require(p['decision'] in ('REVIEW_PASS','REVISION_REQUIRED','NEEDS_RESEARCH','REJECT'), 'LOCALE_REVIEW_DECISION')
    require(isinstance(p['findings'],list), 'LOCALE_REVIEW_FINDINGS')
    if p['decision']=='REVIEW_PASS':require(all(p['checks'].values()) and not p['findings'], 'LOCALE_REVIEW_FALSE_PASS')
    packet=dict(content_hash=article['content_hash'],base_content_hash=base['content_hash'],
        reviewer_id='reviewer:'+result['response_id'],verdict=p,locale=article['locale'],
        human_reviewed=False,publish_approved=False,production_eligible=False)
    packet['review_hash']=digest(packet)
    return packet

class Localizer:
    def __init__(self,models,journal):self.models,self.journal=models,journal

    def run(self,base,research,locale):
        require(base['content_hash']==digest({k:v for k,v in base.items() if k!='content_hash'}),'BASE_ARTICLE_CHANGED')
        previous=findings=None
        # Bind checkpoint namespace to the approved English hash, not a mutable title.
        prefix='locale:'+base['article_id']+':'+base['content_hash']+':'+locale
        for version in range(1,4):
            key=prefix+':v'+str(version)
            article=self.journal.get_checkpoint(key+':article')
            if article is None:
                result=self.models.call(key+':translate','writing',request(base,research,locale,version,previous,findings))
                article=validate(result,base,locale,version)
                self.journal.checkpoint(key+':article',article)
            require(article['base_content_hash']==base['content_hash'] and article['locale']==locale,'CACHED_LOCALE_DRIFT')
            require(article['content_hash']==digest({k:v for k,v in article.items() if k!='content_hash'}),'CACHED_LOCALE_HASH')
            review=self.journal.get_checkpoint(key+':review')
            if review is None:
                result=self.models.call(key+':review','review',review_request(article,base,research))
                review=validate_review(result,article,base)
                self.journal.checkpoint(key+':review',review)
            require(review['content_hash']==article['content_hash'],'CACHED_REVIEW_DRIFT')
            verdict=review['verdict']['decision']
            if verdict=='REVIEW_PASS':return dict(article=article,review=review)
            if verdict in ('NEEDS_RESEARCH','REJECT'):
                self.journal.halt(base['article_id'],'review',version,'LOCALE_'+locale+'_'+verdict)
                require(False,'LOCALE_'+locale+'_'+verdict)
            if version==3:
                self.journal.halt(base['article_id'],'review',version,'LOCALE_'+locale+'_MAX_REVISIONS')
                require(False,'LOCALE_MAX_TWO_REVISIONS')
            previous,findings=article,review['verdict']['findings']

def markdown(article,research,topic):
    """S05-format source draft; unresolved image/author/site fields stay explicit."""
    p=article['public'];locale=article.get('locale','en')
    fields=[('SEO Title',p['title']),('Meta Description',p['meta']),('H1',p['h1']),
        ('Primary Keyword',p['title']),('Secondary Search Terms',''),
        ('Suggested URL',topic['proposed_url']+'?draft-locale='+locale),
        ('Search Intent',p['summary']),('Internal Link Suggestions',', '.join(p['internal_links'])),
        ('Image Suggestion','Pending rights-cleared image selection; no image supplied'),
        ('ALT Suggestion','Pending verification of actual image'),
        ('Schema Scope','Article; Vehicle only where supported; no Offer/Price/Review/Rating')]
    lines=['# '+p['h1'],'','## SEO Metadata','']+[f'- **{k}**: {v}' for k,v in fields]+['']
    lines += [s['text']+'\n' for s in p['sections']]
    lines+=['## FAQ','']
    for f in p['faq']:lines+=['**'+f['question']+'**','',f['answer'],'']
    lines+=['## Sources & Verification','','| # | Organization | Scope | URL | Retrieved |','|---|---|---|---|---|']
    for i,e in enumerate(research['evidence'],1):
        row=[str(i),e.get('publisher',''),str(e.get('scope',{}).get('market','')),e.get('requested_url',''),e.get('retrieved_at','')]
        lines+=['| '+' | '.join(x.replace('|','\\|').replace('\n',' ') for x in row)+' |']
    lines+=['','## Editorial Review','',
        '- **Author**: Prepared for AutoBridge; final byline pending.',
        '- **Verification method**: Source-bound desk research; no first-hand test claimed.',
        '- **Transparency**: AI-assisted draft and automated independent model review. Human review, image rights and live-site SEO acceptance remain pending.','']
    return '\n'.join(lines)

def run_multilingual(plan,journal,models,github,english_deliveries):
    """Only report a complete bundle after all 24 full drafts pass their own review."""
    localizer=Localizer(models,journal);files={};receipts=[]
    for topic in plan['articles']:
        final=journal.get_checkpoint('final:'+topic['article_id'])
        require(final and final['review']['verdict']['decision']=='REVIEW_PASS','ENGLISH_REVIEW_REQUIRED')
        base,research=final['article'],final['research']
        require(final['review']['content_hash']==base['content_hash'],'ENGLISH_REVIEW_CHANGED')
        require(all(0 <= (now()-datetime.fromisoformat(e['retrieved_at'])).total_seconds() <= 86400
                    for e in research['evidence']),'LOCALIZATION_SOURCE_EVIDENCE_STALE')
        for locale in LOCALES:
            result=dict(article=base,review=final['review']) if locale=='en' else localizer.run(base,research,locale)
            article=result['article']; filename=topic['article_id']+'.'+locale+'.md'
            path='cloud_pilot/live_artifacts/multilingual/'+base['content_hash']+'/'+locale+'/'+filename
            text=markdown(article,research,topic)
            require(len(re.findall(r'^# ',text,re.M))==1,'EXPORT_SINGLE_H1')
            sha=github.put_immutable(__import__('cloud_pilot.live.policy',fromlist=['BRANCH']).BRANCH,path,text.encode())
            files[filename]=dict(path=path,blob_sha=sha,locale=locale,content_hash=article['content_hash'],review_hash=result['review']['review_hash'])
    require(len(files)==24 and {v['locale'] for v in files.values()}==set(LOCALES),'INCOMPLETE_24_FILE_BUNDLE')
    report=dict(status='AUTOMATED_MULTILINGUAL_DRAFTS_COMPLETE',files=files,english_draft_prs=english_deliveries,
        human_reviewed=False,publish_approved=False,website_published=False,
        remaining=['human editorial review','image rights','same-language link verification','live-site technical acceptance'])
    journal.checkpoint('multilingual-bundle:'+digest(plan),report)
    return report

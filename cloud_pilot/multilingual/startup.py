"""Verify current main ancestry and derive actual skill/evidence provenance."""
import re
import subprocess
from datetime import datetime,timezone
from ..contract import ROOT,RULE_PATHS,file_hash,require,digest

BATCH_CONTEXT=(
 'daily/2026-11-02/research/pilot-intake-proposal.json',
 'daily/2026-11-02/research/scope-alignment-feedback.json',
 'daily/2026-11-02/research/seo-acceptance-requirements.json')

def batch_context():
    files={p:(ROOT/p).read_text() for p in BATCH_CONTEXT}
    # Actual related Fact Sheets/Source Logs and published URL state are read,
    # rather than treating the article-title history index as their contents.
    for p in sorted((ROOT/'daily').glob('**/research/**/*')):
        if p.is_file() and p.suffix in ('.md','.json') and re.search(r'Q05|Aumark|Commercial_Fleet|PDI_Pre|Pre_Shipment|AB-260902-(?:V10|G10|VR2)|AB-260904-G05',p.name,re.I):
            files[p.relative_to(ROOT).as_posix()]=p.read_text()
    for p in sorted((ROOT/'state').glob('*.json')):files[p.relative_to(ROOT).as_posix()]=p.read_text()
    return files

def review_context(root=ROOT,all_versions=False):
    files={p.relative_to(root).as_posix():p.read_text() for p in sorted((root/'reviews').rglob('*.json'))
           if 'handoff' in p.name.lower()}
    # Supply every handoff. Research and Writing must each classify applicability
    # against their actual topic; filename dates never silently remove evidence.
    return files

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def skill_provenance(name,ref='HEAD'):
    path='skills/autobridge-'+name+'/SKILL.md'
    text=git('show',ref+':'+path)
    version=re.search(r'(?m)^version:\s*(\S+)',text)
    require(version,'SKILL_VERSION_MISSING')
    return dict(path=path,version=version.group(1),commit=git('log','-1','--format=%H',ref,'--',path),
                checkout_sha=git('rev-parse','HEAD'),content_hash=file_hash(ROOT/path))

def verify(main_sha,plan):
    # Perform the prescribed synchronization, then reject any live main drift.
    # This runs before application credentials are read; no generation follows
    # a pull that changes the approved revision.
    git('fetch','origin','main')
    git('checkout','-B','main',main_sha)
    git('pull','--ff-only','origin','main')
    require(subprocess.run(['git','merge-base','--is-ancestor',main_sha,'HEAD'],cwd=ROOT).returncode==0,
            'EXECUTION_DOES_NOT_CONTAIN_APPROVED_MAIN')
    head=git('rev-parse','HEAD');origin=git('rev-parse','refs/remotes/origin/main')
    require(head==origin==main_sha,'PRE_RESEARCH_SYNC_FAIL')
    scopes=('skills','LESSONS_LEARNED.md','VERSIONING.md','reviews','daily','batches','deliveries','state','reports')
    # Current-main files must be unchanged. New, separately reviewed pilot intake files are additions.
    require(not git('diff','--name-only','--diff-filter=DMRTUXB',main_sha,'HEAD','--',*scopes),'CURRENT_MAIN_EVIDENCE_DRIFT')
    read={p:(ROOT/p).read_text() for p in RULE_PATHS}
    read.update(batch_context())
    read.update(review_context(all_versions=True))
    read['cloud_pilot/evidence/history-snapshot.json']=(ROOT/'cloud_pilot/evidence/history-snapshot.json').read_text()
    # Current batch evidence starts with the approved manifest; Research supplies fresh fact/source handoffs.
    return dict(approved_main_sha=main_sha,execution_sha=git('rev-parse','HEAD'),
        startup_gate=dict(REPO_HEAD_SHA=head,ORIGIN_MAIN_HEAD=origin,
            main_sync_commands=['git fetch origin main','git checkout -B main '+main_sha,'git pull --ff-only origin main'],
            LESSONS_LEARNED_SHA=git('rev-parse','HEAD:LESSONS_LEARNED.md'),
            LESSONS_LEARNED_COMMIT=git('log','-1','--format=%H','HEAD','--','LESSONS_LEARNED.md'),
            LESSONS_READ_AT=datetime.now(timezone.utc).isoformat(),
            lessons_content_hash=file_hash(ROOT/'LESSONS_LEARNED.md'),status='PRE_RESEARCH_SYNC_PASS'),
        read_files={p:digest(t) for p,t in read.items()},batch_manifest_hash=digest(plan),
        research_skill=skill_provenance('research',main_sha),writing_skill=skill_provenance('writing',main_sha),
        skill_impact_check=dict(status='REQUIRED_IN_RESEARCH_AND_CONTENT_REVIEW',
            technical_changes='Cache, workflow, accounting and serialization corrections; assess editorial-rule changes against current skills.'))

class EpochJournal:
    """A separately approved source refresh never overwrites old evidence or dependent results."""
    def __init__(self,journal,revision,binding=None):
        require(type(revision) is int and revision>=1,'EVIDENCE_REVISION_INVALID')
        self.journal=journal;self.prefix='evidence-round:'+str(revision)+':'+(digest(binding)+':' if binding else '')
    def checkpoint(self,key,value):return self.journal.checkpoint(self.prefix+key,value)
    def get_checkpoint(self,key):return self.journal.get_checkpoint(self.prefix+key)
    def __getattr__(self,key):return getattr(self.journal,key)

def lesson_ids():
    text=(ROOT/'LESSONS_LEARNED.md').read_text()
    return sorted(set(re.findall(r'^#{2,3} LESSON:\s*([A-Z_]+)',text,re.M)+
                      re.findall(r'^\d+\.\s+\*\*([A-Z_]+)\*\*',text,re.M)))

def writing_startup(main_sha,plan,research,github,current_manifest,journal=None):
    import json,base64
    from .publication import verify_research,json_bytes,DATE
    record=verify(main_sha,plan) # Includes actual git pull and full rule reads.
    completion=verify_research(github,research)
    manifest=current_manifest
    if journal is not None:
        prefix=getattr(journal,'prefix','')+'batch-manifest-current:'
        keys=[k for k in journal.read()[2]['checkpoints'] if k.startswith(prefix)]
        require(keys,'WRITING_CURRENT_MANIFEST_REQUIRED')
        latest=max(keys,key=lambda k:int(k.rsplit(':',1)[1]))
        require(getattr(journal,'journal',journal).get_checkpoint(latest)==manifest,'WRITING_CURRENT_MANIFEST_DRIFT')
    obj=github.call('GET','/contents/'+manifest['path']+'?ref='+manifest['commit_sha'])
    actual=json.loads(base64.b64decode(obj['content']))
    from .activation_review import intake
    require(digest(actual)==manifest['content_hash'] and intake(actual['plan'])==intake(plan),'WRITING_DAILY_MANIFEST_DRIFT')
    rows_by_id={r['ARTICLE_ID']:r for r in actual['articles']};row=rows_by_id.get(research['article_id'],{})
    require(set(rows_by_id)=={t['article_id'] for t in plan['articles']} and row.get('WRITING_AI_READY') is True
            and row.get('RESEARCH_HASH')==research['research_hash'] and row.get('FACT_SHEET_VERSION')==row.get('SOURCE_LOG_VERSION')==research['version']
            and row.get('RESEARCH_COMPLETE_COMMIT_SHA')==completion['commit_sha']
            and row.get('RESEARCH_STATUS')==research['fact_sheet']['status'],'WRITING_MANIFEST_RESEARCH_DRIFT')
    require(actual['WRITING_READY_COUNT']==sum(r['WRITING_AI_READY'] for r in actual['articles']) and
            all(actual[k]==sum(r['RESEARCH_STATUS']==s for r in actual['articles']) for k,s in
            [('MAIN_PASS_COUNT','RESEARCH_PASS'),('MAIN_CONDITIONAL_COUNT','RESEARCH_CONDITIONAL'),('MAIN_FAIL_COUNT','RESEARCH_FAIL')]),'WRITING_MANIFEST_COUNT_DRIFT')
    rows=research['independent_fact_review']['verdict']['lesson_assessments']
    require({r['lesson_id'] for r in rows}==set(lesson_ids()) and all(r['triggered'] is False for r in rows),'PRE_WRITING_LESSON_ERROR')
    record.update(stage='PRE_WRITING',RESEARCH_BASELINE_SHA=completion['commit_sha'],
        WRITING_START_HEAD_SHA=record['execution_sha'],
        research_files_read=completion['files'],daily_manifest_read=manifest,lesson_assessments=rows,
        checklist=dict(repo_pulled=True,lessons_read=True,fact_sheets_read=True,source_logs_read=True,
            daily_manifest_read=True,each_lesson_checked=True,no_historical_error_triggered=True),
        human_reviewed=False,publish_approved=False)
    path=f'daily/{DATE}/qa/api-pilot/startup/{digest(record)}.json'
    github.put_canonical_qa(path,json_bytes(record))
    return record

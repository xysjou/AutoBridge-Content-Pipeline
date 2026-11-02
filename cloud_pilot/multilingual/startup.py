"""Verify current main ancestry and derive actual skill/evidence provenance."""
import re
import subprocess
from ..contract import ROOT,RULE_PATHS,file_hash,require,digest

BATCH_CONTEXT=(
 'daily/2026-11-02/research/pilot-intake-proposal.json',
 'daily/2026-11-02/research/scope-alignment-feedback.json',
 'daily/2026-11-02/research/seo-acceptance-requirements.json')

def batch_context():return {p:(ROOT/p).read_text() for p in BATCH_CONTEXT}

def review_context(root=ROOT,all_versions=False):
    files={p.relative_to(root).as_posix():p.read_text() for p in sorted((root/'reviews').rglob('*.json'))
           if 'handoff' in p.name.lower()}
    if all_versions:return files
    def date(path):return max((x.replace('-','') for x in re.findall(r'20\d{2}-?\d{2}-?\d{2}',path)),default='0')
    groups=[lambda p:'review_handoff' in p.lower(),lambda p:'writing' in p.lower()]
    selected=set()
    for group in groups:
        choices=[p for p in files if group(p)]
        if choices:selected.add(max(choices,key=lambda p:(date(p),p)))
    selected.update(p for p in files if re.search(r'q05|reefer|refrigerat',p,re.I))
    latest=max((date(p) for p in selected),default='0')
    require(not any(date(p)>latest for p in files if p not in selected),'NEW_REVIEW_HANDOFF_NEEDS_SCOPE_CLASSIFICATION')
    return {p:files[p] for p in sorted(selected)}

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def skill_provenance(name,ref='HEAD'):
    path='skills/autobridge-'+name+'/SKILL.md'
    text=git('show',ref+':'+path)
    version=re.search(r'(?m)^version:\s*(\S+)',text)
    require(version,'SKILL_VERSION_MISSING')
    return dict(path=path,version=version.group(1),commit=git('log','-1','--format=%H',ref,'--',path),
                checkout_sha=git('rev-parse','HEAD'),content_hash=file_hash(ROOT/path))

def verify(main_sha,plan):
    require(subprocess.run(['git','merge-base','--is-ancestor',main_sha,'HEAD'],cwd=ROOT).returncode==0,
            'EXECUTION_DOES_NOT_CONTAIN_APPROVED_MAIN')
    scopes=('skills','LESSONS_LEARNED.md','VERSIONING.md','reviews','daily','batches','deliveries','state','reports')
    # Current-main files must be unchanged. New, separately reviewed pilot intake files are additions.
    require(not git('diff','--name-only','--diff-filter=DMRTUXB',main_sha,'HEAD','--',*scopes),'CURRENT_MAIN_EVIDENCE_DRIFT')
    read={p:(ROOT/p).read_text() for p in RULE_PATHS}
    read.update(batch_context())
    read.update(review_context(all_versions=True))
    read['cloud_pilot/evidence/history-snapshot.json']=(ROOT/'cloud_pilot/evidence/history-snapshot.json').read_text()
    # Current batch evidence starts with the approved manifest; Research supplies fresh fact/source handoffs.
    return dict(approved_main_sha=main_sha,execution_sha=git('rev-parse','HEAD'),
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

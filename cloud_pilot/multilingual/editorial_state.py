"""Durable Research head and writing lock in the append-only article journal.

Research updates must register a new version here. A new head during writing
records UPDATE_REQUIRED and prevents article completion under the old facts.
"""
from ..contract import digest,require

class EditorialState:
    def __init__(self,journal):
        # Shared across source/code epochs: a new Research epoch must invalidate
        # writing from an older epoch for the same article ID.
        self.journal=getattr(journal,'journal',journal)
    def rows(self,prefix):
        keys=self.journal.read()[2]['checkpoints']
        scope=getattr(self.journal,'prefix','')
        return [self.journal.get_checkpoint(k[len(scope):]) for k in keys if k.startswith(scope+prefix)]
    def head(self,aid):
        rows=self.rows('research-current:'+aid+':')
        return max(rows,key=lambda r:r['version']) if rows else None
    def transition(self,aid,status,**data):
        seq=len(self.journal.read()[0]['events'])
        row=dict(article_id=aid,status=status,sequence=seq,**data)
        self.journal.checkpoint('research-state:'+aid+':'+str(seq),row)
        return row
    def signal(self,aid,old,current):
        if old:
            self.journal.checkpoint('update-required:'+aid+':'+old['research_hash']+':'+digest(current),
                dict(status='UPDATE_REQUIRED',old=old,current=current))
    def begin(self,aid,attempt):
        key='research-start:'+aid+':'+digest(attempt)
        existing=self.journal.get_checkpoint(key)
        if existing:return existing
        old=self.head(aid);version=old['version']+1 if old else 1
        row=self.transition(aid,'RESEARCH_LOCK',version=version,attempt=attempt)
        # Invalidate prior writing before validating or generating replacement facts.
        self.signal(aid,old,row)
        self.journal.checkpoint(key,row)
        return row
    def register(self,research):
        aid=research['article_id'];version=research['version'];current=self.head(aid)
        row=dict(article_id=aid,version=version,research_hash=research['research_hash'],
                 handoff_hash=digest(research['fact_sheet'].get('handoff',{})))
        if current==row:return row
        self.signal(aid,current,row)
        require(version==(current['version']+1 if current else 1),'RESEARCH_HEAD_VERSION_MUST_ADVANCE')
        self.journal.checkpoint('research-current:'+aid+':'+str(version),row)
        self.transition(aid,'RESEARCH_READY',research_hash=research['research_hash'],version=version)
        return row
    def lock(self,research):
        aid=research['article_id'];row=self.register(research)
        lock=dict(status='WRITING_LOCK',article_id=aid,research_head=row,
                  research_locked=False,writing_locked=True)
        self.journal.checkpoint('writing-lock:'+aid+':'+research['research_hash'],lock)
        self.check(research)
    def check(self,research):
        aid=research['article_id'];lock=self.journal.get_checkpoint('writing-lock:'+aid+':'+research['research_hash'])
        require(lock and lock.get('status')=='WRITING_LOCK','WRITING_LOCK_REQUIRED')
        states=self.rows('research-state:'+aid+':')
        latest=max(states,key=lambda s:s['sequence']) if states else {}
        require(latest.get('status')=='RESEARCH_READY','RESEARCH_LOCK_UPDATE_REQUIRED')
        current=self.head(aid)
        if (current!=lock['research_head'] or current['research_hash']!=research['research_hash']
                or current['handoff_hash']!=digest(research['fact_sheet'].get('handoff',{}))):
            self.signal(aid,lock['research_head'],current)
            require(False,'RESEARCH_CHANGED_AFTER_WRITING_STARTED')
        require(not self.rows('update-required:'+aid+':'+research['research_hash']+':'),'UPDATE_REQUIRED')

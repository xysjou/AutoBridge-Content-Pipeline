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
    def register(self,research):
        aid=research['article_id'];version=research['version']
        row=dict(article_id=aid,version=version,research_hash=research['research_hash'],
                 handoff_hash=digest(research['fact_sheet'].get('handoff',{})))
        current=self.head(aid)
        require(current is None or version>=current['version'],'RESEARCH_HEAD_ROLLBACK')
        self.journal.checkpoint('research-current:'+aid+':'+str(version),row)
        lock=self.journal.get_checkpoint('writing-lock:'+aid)
        if lock and lock['research_head']!=row:
            self.journal.checkpoint('update-required:'+aid+':'+research['research_hash'],
                dict(status='UPDATE_REQUIRED',old=lock['research_head'],current=row))
        return row
    def lock(self,research):
        aid=research['article_id'];row=self.register(research)
        lock=dict(status='WRITING_LOCK',article_id=aid,research_head=row,
                  research_locked=True,writing_locked=True)
        self.journal.checkpoint('writing-lock:'+aid,lock)
        self.check(research)
    def check(self,research):
        aid=research['article_id'];lock=self.journal.get_checkpoint('writing-lock:'+aid)
        require(lock and lock.get('status')=='WRITING_LOCK','WRITING_LOCK_REQUIRED')
        current=self.head(aid)
        if (current!=lock['research_head'] or current['research_hash']!=research['research_hash']
                or current['handoff_hash']!=digest(research['fact_sheet'].get('handoff',{}))):
            self.journal.checkpoint('update-required:'+aid+':'+digest(current),
                dict(status='UPDATE_REQUIRED',old=lock['research_head'],current=current))
            require(False,'RESEARCH_CHANGED_AFTER_WRITING_STARTED')
        require(not self.rows('update-required:'+aid+':'),'UPDATE_REQUIRED')

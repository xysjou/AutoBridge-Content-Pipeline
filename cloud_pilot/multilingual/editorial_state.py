"""CAS-atomic Research heads and a fenced publication transaction.

All active Research and publication use this same append-only program ledger.
Superseding Research invalidates its predecessor in the same CAS; only the latest
fence can become ready. Publication briefly defers Research mutations until its
immutable draft transaction is confirmed or resumed by the same owner.
"""
import copy
from contextlib import contextmanager
from ..contract import digest,require
from ..live.ledger import append

class EditorialState:
    def __init__(self,journal):self.journal=getattr(journal,'journal',journal)

    def state(self,view):
        rows=[(int(k.rsplit(':',1)[1]),v) for k,v in view['checkpoints'].items() if k.startswith('editorial-state:')]
        return copy.deepcopy(max(rows,key=lambda p:p[0])[1] if rows else dict(articles={},publication=None,released=[]))

    def mutate(self,fn):
        data,token,view=self.journal.read();before=self.state(view);after=copy.deepcopy(before)
        result=fn(after)
        if after!=before:
            n=len(data['events']);key='editorial-state:'+str(n)
            payload=dict(kind='checkpoint',key=key,artifact=after,artifact_hash=digest(after))
            updated=append(data,'checkpoint:'+key,payload)
            # Guard and mutation use exactly this snapshot. CAS conflict stops;
            # the guard is never silently evaluated on a different ledger head.
            self.journal.store.cas(token,updated)
        return result

    def snapshot(self):return self.state(self.journal.read()[2])
    def article(self,state,aid):return state['articles'].setdefault(aid,dict(counter=0,head=None,research_lock=None,starts={},writing={},updates=[]))
    def head(self,aid):return self.snapshot()['articles'].get(aid,{}).get('head')

    def begin(self,aid,attempt):
        def change(state):
            a=self.article(state,aid)
            if attempt in a['starts']:
                start=a['starts'][attempt]
                require(a['research_lock']==start or (a['head'] and a['head']['attempt']==attempt),'RESEARCH_START_SUPERSEDED')
                return start
            require(state['publication'] is None,'RESEARCH_DEFERRED_DURING_FENCED_PUBLICATION')
            a['counter']+=1
            start=dict(article_id=aid,attempt=attempt,version=a['counter'],fence=digest([aid,attempt,a['counter']]))
            if a['head']:a['updates'].append(dict(article_id=aid,status='UPDATE_REQUIRED',old_hash=a['head']['research_hash'],replacement=start))
            a['research_lock']=start;a['starts'][attempt]=start
            return start
        return self.mutate(change)

    def assert_research(self,start):
        a=self.snapshot()['articles'].get(start['article_id'],{})
        require(a.get('research_lock')==start,'RESEARCH_START_SUPERSEDED')

    def register(self,research):
        aid=research['article_id'];start=research.get('research_start')
        # Tiny non-article unit fixtures use the same protocol without a topic.
        if start is None and 'topic' not in research:start=self.begin(aid,'fixture:'+research['research_hash'])
        require(start and start['version']==research['version'],'RESEARCH_FENCE_REQUIRED')
        row=dict(article_id=aid,version=research['version'],research_hash=research['research_hash'],
                 handoff_hash=digest(research['fact_sheet'].get('handoff',{})),attempt=start['attempt'],
                 completion_commit=research.get('completion',{}).get('commit_sha'))
        def change(state):
            a=self.article(state,aid)
            if a['head']==row:return row
            require(state['publication'] is None,'RESEARCH_DEFERRED_DURING_FENCED_PUBLICATION')
            require(a['research_lock']==start,'RESEARCH_START_SUPERSEDED')
            # Head and readiness are one atomic state, with no intermediate
            # current-but-not-ready checkpoint to strand a resume.
            a['head']=row;a['research_lock']=None
            return row
        return self.mutate(change)

    def lock(self,research):
        self.register(research)
        def change(state):
            a=self.article(state,research['article_id'])
            require(a['research_lock'] is None and a['head']['research_hash']==research['research_hash'],'RESEARCH_LOCK_UPDATE_REQUIRED')
            a['writing'][research['research_hash']]=dict(status='WRITING_LOCK',version=research['version'])
        self.mutate(change);self.check(research)

    def check_in(self,state,research):
        a=state['articles'].get(research['article_id'],{});head=a.get('head')
        require(a.get('research_lock') is None,'RESEARCH_LOCK_UPDATE_REQUIRED')
        require(head and head['research_hash']==research['research_hash'] and head['version']==research['version']
                and head['handoff_hash']==digest(research['fact_sheet'].get('handoff',{})), 'RESEARCH_CHANGED_AFTER_WRITING_STARTED')
        require(research['research_hash'] in a.get('writing',{}),'WRITING_LOCK_REQUIRED')
        require(not any(u['old_hash']==research['research_hash'] for u in a.get('updates',[])),'UPDATE_REQUIRED')

    def check(self,research):self.check_in(self.snapshot(),research)

    def begin_publication(self,researches,owner):
        targets={r['article_id']:r['research_hash'] for r in researches}
        token=dict(owner=owner,targets=targets,fence=digest([owner,targets]))
        def change(state):
            for r in researches:self.check_in(state,r)
            require(state['publication'] in (None,token),'OTHER_PUBLICATION_FENCE_ACTIVE')
            state['publication']=token
            return token
        return self.mutate(change)

    def end_publication(self,token):
        def change(state):
            if state['publication'] is None and token['fence'] in state['released']:return
            require(state['publication']==token,'PUBLICATION_FENCE_CHANGED')
            state['publication']=None;state['released'].append(token['fence'])
        self.mutate(change)

    @contextmanager
    def model_stage(self,research,owner):
        # The same atomic guard fences stage starts and holds Research updates
        # until the returned response has been checked and checkpointed.
        token=self.begin_publication([research],'model:'+owner)
        try:
            self.check(research)
            yield
            self.check(research)
        finally:self.end_publication(token)

    def abort_publication(self,token,proof):
        require(proof.get('fence')==token['fence'] and proof.get('status')=='VERIFIED_INVALIDATED',
                'PUBLICATION_ABORT_PROOF_REQUIRED')
        def change(state):
            require(state['publication']==token,'PUBLICATION_FENCE_CHANGED')
            for aid,old_hash in token['targets'].items():
                a=self.article(state,aid)
                a['updates'].append(dict(article_id=aid,status='UPDATE_REQUIRED',old_hash=old_hash,
                    reason='OPERATOR_ABORTED_DELIVERY',proof_hash=digest(proof)))
            state.setdefault('aborts',[]).append(proof)
            state['publication']=None;state['released'].append(token['fence'])
        self.mutate(change)

    def rows(self,prefix):
        # Read-only diagnostic compatibility; the authoritative data is one
        # atomic global state, never separate partially committed head flags.
        if prefix.startswith('update-required:'):
            aid=prefix.split(':')[1]
            return self.snapshot()['articles'].get(aid,{}).get('updates',[])
        return []

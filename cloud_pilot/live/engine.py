"""Sequential durable pipeline; separate stateless model requests per responsibility."""
from datetime import datetime
from ..contract import digest, require
from .policy import BRANCH, timestamp, now
from .stages import (validate_plan,research_request,check_research,writing_request,
                     check_writing,review_request,check_review)

class Engine:
    def __init__(self,plan,history,journal,models,github,fetch,prior_bodies=(),guard=lambda:None):
        validate_plan(plan,history)
        self.plan,self.history,self.journal=plan,history,journal
        self.models,self.github,self.fetch,self.prior_bodies=models,github,fetch,tuple(prior_bodies)
        self.guard=guard

    def cached(self,key):
        return self.journal.get_checkpoint(key)

    def evidence(self,topic):
        key='evidence:'+topic['article_id']
        old=self.cached(key)
        if old is not None:
            require(all(0<=(now()-datetime.fromisoformat(e['retrieved_at'])).total_seconds()<=86400 for e in old),'SOURCE_EVIDENCE_STALE')
            from ..multilingual.research_contract import applies
            if applies(topic):
                from ..multilingual.source_cache import validate
                validate(old,topic)
            return old
        evidence=[]
        for source in topic['sources']:
            redirects=source.get('authorized_redirect_urls',[])
            require(set(redirects)<=set(self.plan.get('authorized_redirect_urls',[])),'SOURCE_REDIRECT_NOT_APPROVED')
            allowed={source['url'],*redirects}
            result,raw=self.fetch(source,allowed)
            path='cloud_pilot/live_artifacts/sources/'+result['raw_sha256']+'.bin'
            blob=self.github.put_immutable(BRANCH,path,raw)
            result.update(raw_artifact_path=path,raw_artifact_blob=blob)
            result.pop('evidence_hash',None);result['evidence_hash']=digest(result)
            evidence.append(result)
        # Any source access/parse/persistence failure aborts before Research/Writing API.
        self.journal.checkpoint(key,evidence)
        return evidence

    def run(self):
        deliveries=[];prior=list(self.prior_bodies)
        for topic in self.plan['articles']:
            self.guard()
            aid=topic['article_id']
            existing=self.cached('delivery:'+aid)
            if existing is not None:
                self.evidence(topic)
                final=self.cached('final:'+aid)
                require(final and final['research']['topic']==topic,'CACHED_DELIVERY_TOPIC_DRIFT')
                from ..multilingual.research_contract import applies
                if applies(topic):
                    from ..multilingual.editorial_state import EditorialState
                    EditorialState(self.journal).check(final['research'])
                current=self.github.deliver_candidate(final)
                require(current==existing,'CACHED_DELIVERY_CHANGED')
                deliveries.append(existing)
                if final:prior.append(final['article']['body'])
                continue
            try:evidence=self.evidence(topic)
            except Exception:
                self.journal.halt(aid,'source',1,'SOURCE_FAILED_NO_WRITING');raise
            research=self.cached('research:'+aid)
            if research is None:
                response=self.models.call(aid+':research','research',research_request(topic,evidence))
                try:research=check_research(response,topic,evidence)
                except Exception:
                    self.journal.halt(aid,'research',1,'RESEARCH_FAILED_NO_WRITING');raise
                self.journal.checkpoint('research:'+aid,research)
            require(research['evidence_hash']==digest(evidence),'RESEARCH_EVIDENCE_CHANGED')
            from ..multilingual.research_contract import applies,request as research_review_request,accept
            if applies(topic):
                review_key='research-acceptance:'+research['research_hash']
                if self.cached(review_key) is None:
                    checked=self.models.call(aid+':research-review','review',research_review_request(research))
                    self.journal.checkpoint(review_key,accept(checked,research))
                from ..multilingual.editorial_state import EditorialState
                editorial=EditorialState(self.journal);editorial.lock(research)
            prior_article,findings=None,None
            for version in range(1,4):  # v1 + at most two revisions
                self.guard()
                fresh=self.cached('research:'+aid)
                require(fresh==research,'RESEARCH_BASELINE_DRIFT')
                if applies(topic):
                    from ..multilingual.research_contract import validate
                    editorial.check(research)
                    validate(fresh['fact_sheet'],topic,evidence)
                key=aid+':v'+str(version)
                article=self.cached('article:'+key)
                if article is None:
                    response=self.models.call(key+':writing','writing',writing_request(research,version,prior_article,findings))
                    try:article=check_writing(response,research,version,self.history,prior)
                    except Exception:
                        self.journal.halt(aid,'writing',version,'WRITING_VALIDATION_FAILED');raise
                    self.journal.checkpoint('article:'+key,article)
                require(article['research_hash']==research['research_hash'],'WRITER_RESEARCH_DRIFT')
                review=self.cached('review:'+key)
                if review is None:
                    response=self.models.call(key+':review','review',review_request(article,research))
                    try:review=check_review(response,article,research)
                    except Exception:
                        self.journal.halt(aid,'review',version,'INDEPENDENT_REVIEW_INVALID');raise
                    self.journal.checkpoint('review:'+key,review)
                require(review['content_hash']==article['content_hash'],'STALE_REVIEW')
                verdict=review['verdict']['decision']
                if verdict=='REVIEW_PASS':
                    self.guard()
                    if applies(topic):editorial.check(research)
                    package=dict(article=article,research=research,review=review)
                    self.journal.checkpoint('final:'+aid,package)
                    try:delivery=self.github.deliver_candidate(package)
                    except Exception:
                        self.journal.halt(aid,'delivery',version,'DRAFT_PR_DELIVERY_PENDING');raise
                    self.journal.checkpoint('delivery:'+aid,delivery)
                    deliveries.append(delivery);prior.append(article['body']);break
                if verdict in ('NEEDS_RESEARCH','REJECT'):
                    self.journal.halt(aid,'review',version,verdict)
                    require(False,'STOP_FOR_'+verdict)
                if version==3:
                    self.journal.halt(aid,'review',version,'MAX_TWO_REVISIONS_EXHAUSTED')
                    require(False,'MAX_TWO_REVISIONS_EXHAUSTED')
                prior_article,findings=article,review['verdict']['findings']
        return deliveries

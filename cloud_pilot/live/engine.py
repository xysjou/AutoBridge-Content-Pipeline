"""Sequential durable pipeline; separate stateless model requests per responsibility."""
from datetime import datetime
from contextlib import nullcontext
from ..contract import digest, require
from .policy import BRANCH, timestamp, now
from .stages import (validate_plan,research_request,check_research,writing_request,
                     check_writing,review_request,check_review)

class Engine:
    def __init__(self,plan,history,journal,models,github,fetch,prior_bodies=(),guard=lambda:None,startup=None,prepare_evidence=None):
        validate_plan(plan,history)
        self.plan,self.history,self.journal=plan,history,journal
        self.models,self.github,self.fetch,self.prior_bodies=models,github,fetch,tuple(prior_bodies)
        self.guard=guard
        self.startup=startup;self.partial_evidence=[];self.failed_source=None
        self.prepare_evidence=prepare_evidence

    def sync_manifest(self):
        if self.startup is not None:
            from ..multilingual.publication import sync_batch_manifest
            return sync_batch_manifest(self.github,self.journal,self.plan,self.startup)

    def source_failed(self,topic,error,editorial,started=None):
        from ..multilingual.publication import persist_source_failure,record_transfer_failure
        from ..multilingual.source_cache import SourceTransferFailure
        aid=topic['article_id']
        if editorial is not None:
            if isinstance(error,SourceTransferFailure):record_transfer_failure(self.github,self.journal,self.plan,self.startup,error)
            else:
                start=started or editorial.begin(aid,getattr(self.journal,'prefix','')+':source-failure:'+aid)
                failed=persist_source_failure(self.github,topic,self.partial_evidence,start,error,self.startup,self.failed_source)
                self.journal.checkpoint('failed-source-research:'+aid,failed)
            self.sync_manifest()
        self.journal.halt(aid,'source',1,'SOURCE_FAILED_NO_WRITING')

    def cached(self,key):
        return self.journal.get_checkpoint(key)

    def evidence(self,topic):
        self.partial_evidence=[];self.failed_source=None
        if self.prepare_evidence is not None:self.prepare_evidence(topic)
        key='evidence:'+topic['article_id']
        old=self.cached(key)
        if old is not None:
            self.partial_evidence=old
            require(all(0<=(now()-datetime.fromisoformat(e['retrieved_at'])).total_seconds()<=86400 for e in old),'SOURCE_EVIDENCE_STALE')
            from ..multilingual.research_contract import applies
            if applies(topic):
                from ..multilingual.source_cache import validate
                validate(old,topic)
            return old
        evidence=[];self.partial_evidence=evidence
        for source in topic['sources']:
            self.failed_source=dict(source_id=source['source_id'],url=source['url'])
            redirects=source.get('authorized_redirect_urls',[])
            require(set(redirects)<=set(self.plan.get('authorized_redirect_urls',[])),'SOURCE_REDIRECT_NOT_APPROVED')
            allowed={source['url'],*redirects}
            result,raw=self.fetch(source,allowed)
            evidence.append(result)
            path='cloud_pilot/live_artifacts/sources/'+result['raw_sha256']+'.bin'
            blob=self.github.put_immutable(BRANCH,path,raw)
            result.update(raw_artifact_path=path,raw_artifact_blob=blob)
            result.pop('evidence_hash',None);result['evidence_hash']=digest(result)
        # Any source access/parse/persistence failure aborts before Research/Writing API.
        self.journal.checkpoint(key,evidence)
        return evidence

    def run(self):
        from ..multilingual.research_contract import applies
        from ..multilingual.editorial_state import EditorialState
        deliveries=[];prior=list(self.prior_bodies)
        for topic in self.plan['articles']:
            self.guard()
            aid=topic['article_id']
            active=applies(topic);editorial=EditorialState(self.journal) if active else None
            started=None
            if active and self.cached('research:'+aid) is None:
                started=editorial.begin(aid,getattr(self.journal,'prefix','')+':'+aid)
                editorial.assert_research(started)
                self.sync_manifest()
            existing=self.cached('delivery:'+aid)
            if existing is not None:
                try:self.evidence(topic)
                except Exception as error:
                    self.source_failed(topic,error,editorial,started);raise
                final=self.cached('final:'+aid)
                require(final and final['research']['topic']==topic,'CACHED_DELIVERY_TOPIC_DRIFT')
                from ..multilingual.research_contract import applies
                if applies(topic):
                    from ..multilingual.editorial_state import EditorialState
                    EditorialState(self.journal).check(final['research'])
                current=(self.github.verify_existing_candidate(final,existing) if active else self.github.deliver_candidate(final))
                if applies(topic):EditorialState(self.journal).check(final['research'])
                require(current==existing,'CACHED_DELIVERY_CHANGED')
                if active:
                    pending=editorial.snapshot()['publication'];owner='english:'+final['article']['content_hash']
                    if pending and pending['owner']==owner:editorial.end_publication(pending)
                deliveries.append(existing)
                if final:prior.append(final['article']['body'])
                continue
            try:evidence=self.evidence(topic)
            except Exception as error:
                self.source_failed(topic,error,editorial,started);raise
            research=self.cached('research:'+aid)
            proposal=self.cached('research-proposal:'+aid) if active else None
            if research is None and proposal is None:
                from ..multilingual.research_contract import applies
                expected_version=1;data=research_request(topic,evidence)
                if applies(topic):
                    from ..multilingual.editorial_state import EditorialState
                    expected_version=started['version']
                    data['instruction']+=' Set fact_sheet_version and source_log_version to '+str(expected_version)+'. This durable current Research version overrides the initial output-schema example.'
                try:response=self.models.call(aid+':research','research',data)
                except Exception as error:
                    if active:
                        from ..multilingual.publication import persist_failed_research
                        failed=persist_failed_research(self.github,dict(content={},startup_gate=self.startup or {},
                            failure='MODEL_RESULT_UNAVAILABLE_SEE_DURABLE_RESPONSE_LEDGER'),topic,evidence,started,error)
                        self.journal.checkpoint('failed-research:'+aid,failed)
                        self.sync_manifest()
                    raise
                try:research=check_research(response,topic,evidence,expected_version)
                except Exception as error:
                    if active:
                        from ..multilingual.publication import persist_failed_research
                        failed=persist_failed_research(self.github,dict(response,startup_gate=self.startup or {}),topic,evidence,started,error)
                        self.journal.checkpoint('failed-research:'+aid,failed)
                        self.sync_manifest()
                    self.journal.halt(aid,'research',1,'RESEARCH_FAILED_NO_WRITING');raise
                if active:
                    editorial.assert_research(started)
                    from ..multilingual.publication import seal_research
                    research['startup_gate']=self.startup or {}
                    if self.startup is not None:
                        from ..multilingual.startup import verify
                        research['research_end_gate']=verify(self.startup['approved_main_sha'],self.plan)
                    if research['fact_sheet']['status']=='RESEARCH_FAIL' or research['fact_sheet']['writing_ai_ready'] is False:
                        research['research_phase']='WITHHELD'
                        withheld=seal_research(self.github,research,started)
                        self.journal.checkpoint('withheld-research:'+aid,withheld)
                        self.sync_manifest()
                        self.journal.halt(aid,'research',expected_version,'RESEARCH_VERDICT_NOT_WRITING_READY')
                        require(False,'RESEARCH_VERDICT_NOT_WRITING_READY')
                    proposal=seal_research(self.github,research,started)
                    self.journal.checkpoint('research-proposal:'+aid,proposal)
                    self.sync_manifest()
                    research=None
                else:self.journal.checkpoint('research:'+aid,research)
            from ..multilingual.research_contract import applies,request as research_review_request,accept
            if applies(topic):
                from ..multilingual.publication import verify_research,complete_research,persist_failed_research
                if research is None:
                    verify_research(self.github,proposal)
                    require(proposal['evidence_hash']==digest(evidence),'RESEARCH_EVIDENCE_CHANGED')
                    review_key='research-acceptance:'+proposal['research_hash']
                    accepted=self.cached(review_key)
                    if accepted is None:
                        editorial.assert_research(proposal['research_start'])
                        checked=None
                        try:
                            checked=self.models.call(aid+':research-review','review',research_review_request(proposal))
                            editorial.assert_research(proposal['research_start'])
                            accepted=accept(checked,proposal)
                        except Exception as error:
                            failed=persist_failed_research(self.github,dict(content=proposal['fact_sheet'],independent_review=checked),
                                topic,evidence,proposal['research_start'],error)
                            self.journal.checkpoint('failed-research:'+aid,failed)
                            self.sync_manifest()
                            raise
                        self.journal.checkpoint(review_key,accepted)
                    editorial.assert_research(proposal['research_start'])
                    completion_sync=None
                    if self.startup is not None:
                        from ..multilingual.startup import verify
                        completion_sync=verify(self.startup['approved_main_sha'],self.plan)
                    research=complete_research(self.github,proposal,accepted,completion_sync)
                    self.journal.checkpoint('research:'+aid,research)
                verify_research(self.github,research)
                from ..multilingual.editorial_state import EditorialState
                editorial=EditorialState(self.journal);editorial.lock(research)
                if self.startup is not None:
                    from ..multilingual.startup import writing_startup
                    from ..multilingual.publication import sync_batch_manifest
                    manifest=sync_batch_manifest(self.github,self.journal,self.plan,self.startup)
                    writing_record=writing_startup(self.startup['approved_main_sha'],self.plan,research,self.github,manifest,self.journal)
                    self.journal.checkpoint('writing-startup:'+research['research_hash']+':'+digest(writing_record),writing_record)
            require(research['evidence_hash']==digest(evidence),'RESEARCH_EVIDENCE_CHANGED')
            prior_article,findings=None,None
            for version in range(1,4):  # v1 + at most two revisions
                self.guard()
                fresh=self.cached('research:'+aid)
                require(fresh==research,'RESEARCH_BASELINE_DRIFT')
                if applies(topic):
                    from ..multilingual.research_contract import validate
                    editorial.check(research)
                    verify_research(self.github,research)
                    validate(fresh['fact_sheet'],topic,evidence,fresh['version'])
                key=aid+':v'+str(version)
                article=self.cached('article:'+key)
                if article is None:
                    with editorial.model_stage(research,key+':writing') if active else nullcontext():
                        request=writing_request(research,version,prior_article,findings)
                        if active and self.startup is not None:request['pre_writing_gate']=writing_record
                        response=self.models.call(key+':writing','writing',request)
                        if active:editorial.check(research)
                        try:article=check_writing(response,research,version,self.history,prior)
                        except Exception:
                            self.journal.halt(aid,'writing',version,'WRITING_VALIDATION_FAILED');raise
                        self.journal.checkpoint('article:'+key,article)
                require(article['research_hash']==research['research_hash'],'WRITER_RESEARCH_DRIFT')
                review=self.cached('review:'+key)
                if review is None:
                    with editorial.model_stage(research,key+':review') if active else nullcontext():
                        response=self.models.call(key+':review','review',review_request(article,research))
                        if active:editorial.check(research)
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
                    fence=editorial.begin_publication([research],'english:'+article['content_hash']) if active else None
                    try:delivery=self.github.deliver_candidate(package)
                    except Exception:
                        self.journal.halt(aid,'delivery',version,'DRAFT_PR_DELIVERY_PENDING');raise
                    if applies(topic):editorial.check(research)
                    self.journal.checkpoint('delivery:'+aid,delivery)
                    if active:editorial.end_publication(fence)
                    deliveries.append(delivery);prior.append(article['body']);break
                if verdict in ('NEEDS_RESEARCH','REJECT'):
                    self.journal.halt(aid,'review',version,verdict)
                    require(False,'STOP_FOR_'+verdict)
                if version==3:
                    self.journal.halt(aid,'review',version,'MAX_TWO_REVISIONS_EXHAUSTED')
                    require(False,'MAX_TWO_REVISIONS_EXHAUSTED')
                prior_article,findings=article,review['verdict']['findings']
        return deliveries

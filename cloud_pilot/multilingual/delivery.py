"""Create one-file candidate commits; verify exact ancestry and PR diff on every return."""
import base64
from urllib.parse import quote
from ..contract import canonical,digest,require
from ..live.http import GitHubTransport
from ..live.policy import BRANCH

class VerifiedGitHub(GitHubTransport):
    def call(self,method,path,payload=None,expected=200):
        status,obj=self.api.request(method,self.prefix+path,payload)
        require(status==expected,'CANDIDATE_GITHUB_UNCONFIRMED:'+str(status));return obj

    def verify_commit(self,sha,path,body,message):
        c=self.call('GET','/commits/'+sha)
        require(c['sha']==sha and len(c['parents'])==1 and c['commit']['message']==message,'CANDIDATE_COMMIT_CHANGED')
        require(len(c.get('files',[]))==1 and c['files'][0]['filename']==path
                and c['files'][0]['status']=='added','CANDIDATE_COMPLETE_DIFF_CHANGED')
        parent=c['parents'][0]['sha'];base=self.ref(BRANCH)
        comparison=self.call('GET','/compare/'+parent+'...'+base)
        require(comparison['status'] in ('ahead','identical') and comparison['merge_base_commit']['sha']==parent,
                'CANDIDATE_NOT_FROM_INTEGRATION')
        obj=self.call('GET','/contents/'+path+'?ref='+sha)
        require(obj.get('encoding')=='base64' and base64.b64decode(obj['content'])==body,'CANDIDATE_BODY_CHANGED')
        return parent,obj['sha']

    def deliver_candidate(self,package):
        a,r=package['article'],package['review']
        require(r['content_hash']==a['content_hash'] and r['verdict']['decision']=='REVIEW_PASS','DELIVERY_REVIEW_GATE')
        require(a['publish_approved'] is False and r['publish_approved'] is False,'DELIVERY_APPROVAL_FORBIDDEN')
        head='feature/work-cloud-pilot-article-'+digest(package)[:20]
        path='cloud_pilot/live_artifacts/articles/'+a['article_id']+'/v'+str(a['version'])+'/candidate.json'
        body=(canonical(package)+'\n').encode();message='Add immutable English pilot candidate '+digest(package)
        ref='/git/ref/heads/'+quote(head,safe='/');status,obj=self.api.request('GET',self.prefix+ref)
        if status==404:
            base=self.ref(BRANCH);base_commit=self.call('GET','/git/commits/'+base)
            blob=self.call('POST','/git/blobs',dict(content=base64.b64encode(body).decode(),encoding='base64'),201)
            tree=self.call('POST','/git/trees',dict(base_tree=base_commit['tree']['sha'],
                tree=[dict(path=path,mode='100644',type='blob',sha=blob['sha'])]),201)
            commit=self.call('POST','/git/commits',dict(message=message,tree=tree['sha'],parents=[base]),201)
            obj=self.call('POST','/git/refs',dict(ref='refs/heads/'+head,sha=commit['sha']),201)
        else:require(status==200,'CANDIDATE_REF_LOOKUP')
        sha=obj['object']['sha'];parent,blob=self.verify_commit(sha,path,body,message)
        pr=self.draft_pr(head,BRANCH,'[EN pilot draft] '+a['public']['title'],
            'Independently reviewed English draft. Exact head: '+sha+'\nContent hash: '+a['content_hash']+
            '\nNo human approval, CURRENT promotion or website publication.')
        require(pr['head']['sha']==sha and pr['head']['ref']==head and pr['base']['ref']==BRANCH,'CANDIDATE_PR_HEAD_CHANGED')
        files=self.call('GET','/pulls/'+str(pr['number'])+'/files?per_page=100')
        require(len(files)==1 and files[0]['filename']==path and files[0]['status']=='added'
                and files[0]['sha']==blob,'CANDIDATE_PR_COMPLETE_DIFF_CHANGED')
        require(self.ref(head)==sha,'CANDIDATE_REF_MOVED_AFTER_REVIEW')
        return dict(url=pr['html_url'],number=pr['number'],head=head,head_sha=sha,base_parent_sha=parent,
                    content_hash=a['content_hash'],draft=True)

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

    def candidate_details(self,package,expected=None):
        from .publication import writing_files,verify_files,isolated,blob_hash
        a,r=package['article'],package['review']
        require(r['content_hash']==a['content_hash'] and r['verdict']['decision']=='REVIEW_PASS','DELIVERY_REVIEW_GATE')
        require(a['publish_approved'] is False and r['publish_approved'] is False,'DELIVERY_APPROVAL_FORBIDDEN')
        head='feature/work-cloud-pilot-article-'+digest(package)[:20]
        files=writing_files(package);message='Add immutable English pilot candidate '+digest(package)
        status,obj=self.api.request('GET',self.prefix+'/git/ref/heads/'+quote(head,safe='/'))
        if status==404:
            require(expected is None,'CACHED_CANDIDATE_MISSING')
            parent=self.ref(BRANCH);sha=isolated(self,head,parent,files,message)
        else:
            require(status==200,'CANDIDATE_REF_LOOKUP')
            sha=obj['object']['sha'];parent=verify_files(self,sha,files,message)
        comparison=self.call('GET','/compare/'+parent+'...'+self.ref(BRANCH))
        require(comparison['status'] in ('ahead','identical') and comparison['merge_base_commit']['sha']==parent,'CANDIDATE_NOT_FROM_INTEGRATION')
        if expected is None:
            pr=self.draft_pr(head,BRANCH,'[EN pilot draft] '+a['public']['title'],
                'Independently reviewed English text draft. Research completion: '+package['research']['completion']['commit_sha']+
                '\nExact candidate head: '+sha+'\nNo human review, CURRENT promotion or website publication.')
        else:pr=self.call('GET','/pulls/'+str(expected['number']))
        require(pr['state']=='open' and pr['draft'] is True and pr['head']['sha']==sha and pr['head']['ref']==head and pr['base']['ref']==BRANCH,'CANDIDATE_PR_HEAD_CHANGED')
        changed=self.call('GET','/pulls/'+str(pr['number'])+'/files?per_page=100')
        require(len(changed)==len(files) and {f['filename'] for f in changed}==set(files)
                and all(f['status']=='added' and f['sha']==blob_hash(files[f['filename']]) for f in changed),'CANDIDATE_PR_COMPLETE_DIFF_CHANGED')
        require(self.ref(head)==sha,'CANDIDATE_REF_MOVED_AFTER_REVIEW')
        return dict(url=pr['html_url'],number=pr['number'],head=head,head_sha=sha,base_parent_sha=parent,
            content_hash=a['content_hash'],markdown_path=next(p for p in files if p.endswith('/article.md')),
            research_completion_commit=package['research']['completion']['commit_sha'],draft=True)

    def deliver_candidate(self,package):return self.candidate_details(package)
    def verify_existing_candidate(self,package,expected):return self.candidate_details(package,expected)

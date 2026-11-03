"""Small bounded HTTPS clients. No redirects/retries/proxy discovery for APIs."""
import base64
import http.client
import json
import ssl
from urllib.parse import quote
from ..contract import canonical, require
from .policy import REPO, BRANCH, STATE_PATH

class TransportFailure(RuntimeError):
    """Intentionally omits request/response bodies and Authorization headers."""

class JsonAPI:
    def __init__(self, host, token, connection=http.client.HTTPSConnection):
        require(host in ('api.openai.com','api.github.com'), 'FIXED_API_ORIGIN')
        require(isinstance(token,str) and token and '\n' not in token and '\r' not in token,'CREDENTIAL_MISSING')
        self.host,self._token,self.connection=host,token,connection

    def request(self, method, path, payload=None):
        require(path.startswith('/') and not path.startswith('//') and '\r' not in path and '\n' not in path, 'API_PATH')
        conn=self.connection(self.host,443,timeout=45,context=ssl.create_default_context())
        try:
            body=canonical(payload).encode() if payload is not None else None
            conn.request(method,path,body=body,headers={
                'Authorization':'Bearer '+self._token,'Content-Type':'application/json',
                'Accept':'application/json','User-Agent':'AutoBridge-Work-Cloud-Pilot',
                **({'X-GitHub-Api-Version':'2022-11-28'} if self.host=='api.github.com' else {})})
            response=conn.getresponse()
            data=response.read(2_000_001)
            if len(data)>2_000_000:raise TransportFailure('API_RESPONSE_TOO_LARGE')
            try: parsed=json.loads(data) if data else {}
            except (ValueError,UnicodeDecodeError):raise TransportFailure('API_RESPONSE_NOT_JSON') from None
            # 3xx is returned as an error status, never followed with credentials.
            return response.status,parsed
        except TransportFailure:raise
        except Exception:raise TransportFailure('API_TRANSPORT_UNCERTAIN') from None
        finally:conn.close()

class GitHubTransport:
    def __init__(self, api):
        require(api.host=='api.github.com','GITHUB_ORIGIN')
        self.api=api
        self.prefix='/repos/'+REPO

    def ref(self, branch):
        status,obj=self.api.request('GET',self.prefix+'/git/ref/heads/'+quote(branch,safe='/'))
        require(status==200,'GITHUB_REF_UNAVAILABLE')
        return obj['object']['sha']

    def read(self, branch, path):
        require(branch==BRANCH and path==STATE_PATH,'FIXED_PROGRAM_LEDGER')
        status,obj=self.api.request('GET',self.prefix+'/contents/'+path+'?ref='+quote(branch,safe=''))
        require(status==200 and obj.get('encoding')=='base64','GITHUB_LEDGER_MISSING_OR_UNREADABLE')
        try:data=json.loads(base64.b64decode(obj['content']))
        except Exception:raise TransportFailure('GITHUB_LEDGER_DECODE') from None
        return data,obj['sha']

    def replace(self,branch,path,expected,data):
        require(branch==BRANCH and path==STATE_PATH and expected,'FIXED_PROGRAM_LEDGER')
        status,obj=self.api.request('PUT',self.prefix+'/contents/'+path,dict(
            branch=branch,sha=expected,message='Append real-pilot program ledger event',
            content=base64.b64encode((canonical(data)+'\n').encode()).decode()))
        require(status not in (409,422),'CAS_CONFLICT')
        require(status==200,'GITHUB_LEDGER_COMMIT_UNCONFIRMED')
        return obj['content']['sha']

    def put_immutable(self,branch,path,body):
        require(branch==BRANCH and path.startswith('cloud_pilot/live_artifacts/') and '..' not in path,'ARTIFACT_PATH')
        status,obj=self.api.request('GET',self.prefix+'/contents/'+path+'?ref='+quote(branch,safe=''))
        if status==200:
            if path.startswith('cloud_pilot/live_artifacts/sources/'):
                status,obj=self.api.request('GET',self.prefix+'/git/blobs/'+obj['sha'])
                require(status==200 and obj.get('encoding')=='base64','RAW_ARTIFACT_GIT_BLOB_UNAVAILABLE')
            require(base64.b64decode(obj['content'])==body,'IMMUTABLE_ARTIFACT_CONFLICT')
            return obj['sha']
        require(status==404,'ARTIFACT_LOOKUP_FAILED')
        status,obj=self.api.request('PUT',self.prefix+'/contents/'+path,dict(branch=branch,
            message='Add immutable real-pilot evidence artifact',content=base64.b64encode(body).decode()))
        require(status==201,'ARTIFACT_WRITE_UNCONFIRMED')
        return obj['content']['sha']

    def read_artifact(self,branch,path):
        require(branch==BRANCH and path.startswith('cloud_pilot/live_artifacts/checkpoints/') and '..' not in path,'CHECKPOINT_READ_PATH')
        status,obj=self.api.request('GET',self.prefix+'/contents/'+path+'?ref='+quote(branch,safe=''))
        require(status==200 and obj.get('encoding')=='base64','CHECKPOINT_READ_FAILED')
        return json.loads(base64.b64decode(obj['content'])),obj['sha']

    def draft_pr(self,head,base,title,body):
        require(base==BRANCH and head.startswith('feature/work-cloud-pilot-article-'),'DRAFT_PR_BRANCH_SCOPE')
        query='?state=all&head='+quote('xysjou:'+head,safe='')+'&base='+quote(base,safe='')
        status,prs=self.api.request('GET',self.prefix+'/pulls'+query)
        require(status==200,'PR_LOOKUP_FAILED')
        if prs:
            require(len(prs)==1 and prs[0].get('draft') is True and prs[0].get('state')=='open','EXISTING_PR_STATE')
            return prs[0]
        status,pr=self.api.request('POST',self.prefix+'/pulls',dict(head=head,base=base,title=title,
            body=body,draft=True,maintainer_can_modify=False))
        require(status==201 and pr.get('draft') is True,'DRAFT_PR_CREATE_UNCONFIRMED')
        return pr

    def deliver_candidate(self,package):
        from ..contract import digest
        a,r=package['article'],package['review']
        require(r['content_hash']==a['content_hash'] and r['verdict']['decision']=='REVIEW_PASS','DELIVERY_REVIEW_GATE')
        require(a['publish_approved'] is False and r['publish_approved'] is False,'DELIVERY_APPROVAL_FORBIDDEN')
        head='feature/work-cloud-pilot-article-'+digest(package)[:20]
        ref_path=self.prefix+'/git/ref/heads/'+quote(head,safe='/')
        status,obj=self.api.request('GET',ref_path)
        if status==404:
            # Create only an isolated branch; never update any preexisting ref.
            base_sha=self.ref(BRANCH)
            status,obj=self.api.request('POST',self.prefix+'/git/refs',dict(ref='refs/heads/'+head,sha=base_sha))
            require(status==201,'CANDIDATE_BRANCH_UNCONFIRMED')
        else:require(status==200,'CANDIDATE_BRANCH_LOOKUP')
        path='cloud_pilot/live_artifacts/articles/'+a['article_id']+'/v'+str(a['version'])+'/candidate.json'
        body=(canonical(package)+'\n').encode()
        status,obj=self.api.request('GET',self.prefix+'/contents/'+path+'?ref='+quote(head,safe=''))
        if status==200:require(base64.b64decode(obj['content'])==body,'IMMUTABLE_CANDIDATE_CONFLICT')
        else:
            require(status==404,'CANDIDATE_LOOKUP')
            status,obj=self.api.request('PUT',self.prefix+'/contents/'+path,dict(branch=head,
                message='Add independently reviewed English pilot draft; no CURRENT promotion',
                content=base64.b64encode(body).decode()))
            require(status==201,'CANDIDATE_WRITE_UNCONFIRMED')
        pr=self.draft_pr(head,BRANCH,'[EN pilot draft] '+a['public']['title'],
            'English draft only. Content hash: '+a['content_hash']+'\nReview hash: '+r['review_hash']+
            '\nNo human review, publication approval, CURRENT promotion or website deployment. Holds: '+', '.join(a['production_holds']))
        return dict(url=pr['html_url'],number=pr['number'],head=head,content_hash=a['content_hash'],draft=True)

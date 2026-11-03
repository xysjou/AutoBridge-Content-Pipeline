"""One protected approval is a lease for one exact GitHub run, code and workflow chain."""
import base64
import os
import re
import subprocess
from datetime import datetime,timezone
from ..contract import ROOT,digest,file_hash,require
from ..live.policy import check_permit

def lease(permit):
    require(str(permit.get('authorized_run_id'))==os.environ.get('GITHUB_RUN_ID'),'APPROVAL_RUN_ID_DRIFT')
    require(os.environ.get('GITHUB_RUN_ATTEMPT')=='1','APPROVAL_RUN_REPLAY_FORBIDDEN')
    require(permit.get('caller_workflow_sha')==os.environ.get('GITHUB_WORKFLOW_SHA'),'CALLER_WORKFLOW_DRIFT')
    for key in ('caller_workflow_sha','trusted_workflow_sha'):
        require(re.fullmatch('[0-9a-f]{40}',permit.get(key,'')),'WORKFLOW_REVISION_REQUIRED')
    anchor=permit.get('ledger_anchor',{})
    require(type(anchor.get('events_count')) is int and anchor['events_count']>=14
            and anchor.get('last_event_hash') and anchor.get('settled_nano_usd',0)>=259886425
            and anchor.get('reconciled_receipts') and anchor.get('operator_verified') is True,
            'RECONCILED_PROTECTED_LEDGER_ANCHOR_REQUIRED')

def workflows(permit,github):
    lease(permit)
    collected={}
    for file,sha,key in (
      ('cloud-pilot-manual.yml',permit['caller_workflow_sha'],'caller_workflow_hash'),
      ('cloud-pilot-trusted.yml',permit['trusted_workflow_sha'],'trusted_workflow_hash')):
        status,obj=github.api.request('GET',github.prefix+'/contents/.github/workflows/'+file+'?ref='+sha)
        require(status==200 and obj.get('encoding')=='base64','WORKFLOW_SOURCE_UNAVAILABLE')
        content=base64.b64decode(obj['content']).decode()
        require(digest(content)==permit.get(key),'APPROVED_WORKFLOW_SOURCE_DRIFT')
        require(content==(ROOT/'.github/workflows'/file).read_text(),'EXECUTED_WORKFLOW_DIFFERS_FROM_REVIEWED_CODE')
        collected[file]=dict(revision=sha,content=content,content_hash=digest(content))
        if file=='cloud-pilot-manual.yml':
            # GitHub requires explicit forwarding even for secrets owned by the
            # called job's protected environment. Permit only these three names;
            # the caller has no steps and does not execute code with their values.
            keys=('OPENAI_API_KEY','AUTOBRIDGE_CONTROL_COMMIT','AUTOBRIDGE_LIVE_APPROVAL_SHA256')
            refs=re.findall(r'secrets\.([A-Za-z0-9_]+)',content)
            require('cloud-pilot-trusted.yml@'+permit['trusted_workflow_sha'] in content
                    and sorted(refs)==sorted(keys) and 'secrets: inherit' not in content
                    and 'environment:' not in content and 'steps:' not in content
                    and all(k+': ${{ secrets.'+k+' }}' in content for k in keys),
                    'CALLER_SECRET_FORWARDING_SCOPE')
    return collected

def secret_scope(permit,github):
    a=permit.get('environment_only_attestation',{})
    require(a.get('repository_secrets_absent') is True and a.get('owner_only_write_verified') is True
            and a.get('environment')=='autobridge-pilot' and a.get('owner_type')=='User'
            and a.get('environment_names')==['AUTOBRIDGE_CONTROL_COMMIT','AUTOBRIDGE_LIVE_APPROVAL_SHA256','OPENAI_API_KEY'],
            'ENVIRONMENT_ONLY_SCOPE_ATTESTATION_REQUIRED')
    at=datetime.fromisoformat(a['checked_at'])
    require(at.tzinfo and 0<=(datetime.now(timezone.utc)-at).total_seconds()<=3600,'SECRET_SCOPE_ATTESTATION_STALE')
    status,repo=github.api.request('GET',github.prefix)
    require(status==200 and repo.get('owner',{}).get('type')=='User' and repo['owner']['login']=='xysjou',
            'PERSONAL_REPOSITORY_SCOPE_CHANGED')

def preauthorize(plan,prices,permit):
    from ..live.http import JsonAPI,GitHubTransport
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    check_permit(permit,plan,prices,sha,os.environ.get('AUTOBRIDGE_LIVE_APPROVAL_SHA256',''))
    require(sha==permit.get('approved_main_sha'),'CODE_MAIN_SHA_MISMATCH')
    github=GitHubTransport(JsonAPI('api.github.com',os.environ['AUTOBRIDGE_GITHUB_TOKEN']))
    workflows(permit,github);secret_scope(permit,github)
    require('OPENAI_API_KEY' not in os.environ,'PREAUTHORIZE_MUST_NOT_RECEIVE_PROJECT_KEY')
    return dict(status='PREAUTHORIZED_EXACT_RUN',code_sha=sha,run_id=os.environ['GITHUB_RUN_ID'])

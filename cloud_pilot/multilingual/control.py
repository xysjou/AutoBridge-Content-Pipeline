"""Download approved data from a separate immutable control commit; never secrets."""
import base64
import os
from pathlib import Path
import re
from ..contract import require
from ..live.http import JsonAPI
from ..live.policy import REPO

FILES=('approved-plan.json','approved-prices.json','approved-permit.json')

def main():
    sha=os.environ.get('AUTOBRIDGE_APPROVAL_COMMIT','')
    require(re.fullmatch('[0-9a-f]{40}',sha),'IMMUTABLE_CONTROL_COMMIT_REQUIRED')
    # A separate commit avoids the impossible self-referential code-SHA-in-code requirement.
    require(sha!=os.environ.get('AUTOBRIDGE_APPROVED_CODE_SHA'),'CONTROL_SEPARATE_FROM_CODE')
    out=Path(os.environ['RUNNER_TEMP'])/'autobridge-approved';out.mkdir(exist_ok=True)
    api=JsonAPI('api.github.com',os.environ['AUTOBRIDGE_GITHUB_TOKEN'])
    for name in FILES:
        path='/repos/'+REPO+'/contents/cloud_pilot/runtime/control/'+name+'?ref='+sha
        status,obj=api.request('GET',path)
        require(status==200 and obj.get('encoding')=='base64','APPROVED_CONTROL_MISSING')
        body=base64.b64decode(obj['content'],validate=False)
        require(len(body)<200000,'CONTROL_TOO_LARGE')
        (out/name).write_bytes(body)

if __name__=='__main__':main()

"""Default/offline preflight; execute requires an independently approved permit."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from ..contract import ROOT, BASELINE, digest, require, GateError
from ..audit import preserved
from .policy import BRANCH, REPO, SCHEMA, RATES, read_json, validate_prices, check_permit

DEFAULT_PRICES=ROOT/'cloud_pilot/runtime/prices-20261102.json'
DEFAULT_PLAN=ROOT/'cloud_pilot/runtime/plan.pending.json'

def preflight(plan_path=DEFAULT_PLAN,price_path=DEFAULT_PRICES):
    from .stages import validate_plan
    history=read_json(ROOT/'cloud_pilot/evidence/history-snapshot.json')
    blockers=[]
    for name,check in [('pricing',lambda:validate_prices(read_json(price_path))),
                       ('intake',lambda:validate_plan(read_json(plan_path),history)),
                       ('baseline',lambda:require(preserved()==[],'BASELINE_FILES_CHANGED'))]:
        try:check()
        except Exception as exc:blockers.append(dict(gate=name,reason=str(exc)))
    return dict(schema=SCHEMA,mode='OFFLINE_PREFLIGHT',network_requests=0,credentials_read=False,
        real_api_calls=0,program_cap_usd=3,models={k:list(v) for k,v in __import__('cloud_pilot.live.policy',fromlist=['STAGE_MODELS']).STAGE_MODELS.items()},
        blockers=blockers+[
            dict(gate='authorization',reason='FIRST_REAL_CALL_NOT_AUTHORIZED'),
            dict(gate='runtime',reason='PROTECTED_SECRET_RUNTIME_NOT_ACTIVATED'),
            dict(gate='account',reason='PROJECT_MODEL_AVAILABILITY_NOT_VERIFIED')])

def execute(plan_path,price_path,permit_path):
    from .policy import STAGE_MODELS
    from .stages import validate_plan
    from .http import JsonAPI,GitHubTransport
    from .ledger import GitHubStore,Journal
    from .responses import Responses
    from .sources import retrieve
    from .engine import Engine
    plan,prices,permit=read_json(plan_path),read_json(price_path),read_json(permit_path)
    history=read_json(ROOT/'cloud_pilot/evidence/history-snapshot.json')
    validate_plan(plan,history)
    code_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    approval=os.environ.get('AUTOBRIDGE_LIVE_APPROVAL_SHA256','')
    check_permit(permit,plan,prices,code_sha,approval)  # before credential reads
    require(subprocess.run(['git','diff','--quiet','HEAD','--','cloud_pilot/live','cloud_pilot/runtime'],cwd=ROOT).returncode==0,'UNCOMMITTED_EXECUTION_CODE')
    require(preserved()==[],'BASELINE_CHANGED')
    # Only a future protected runner may reach this point. No CLI secret flags.
    key=os.environ.get('OPENAI_API_KEY','');token=os.environ.get('AUTOBRIDGE_GITHUB_TOKEN','')
    require(key and token,'PROTECTED_RUNTIME_CREDENTIALS_MISSING')
    github=GitHubTransport(JsonAPI('api.github.com',token))
    def permission():
        check_permit(permit,plan,prices,code_sha,approval)
        require(github.ref('main')==BASELINE,'MAIN_DRIFT')
    permission()
    journal=Journal(GitHubStore(github))
    models=Responses(JsonAPI('api.openai.com',key),journal,prices,permission)
    # Full tracked historical article bodies, not title/meta-only similarity.
    prior=[(ROOT/d['path']).read_text() for d in history['documents']
           if d['path'].startswith(('batches/','daily/'))]
    return Engine(plan,history,journal,models,github,retrieve,prior).run()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['preflight','execute'],nargs='?',default='preflight')
    p.add_argument('--plan',type=Path,default=DEFAULT_PLAN)
    p.add_argument('--prices',type=Path,default=DEFAULT_PRICES)
    p.add_argument('--permit',type=Path)
    a=p.parse_args()
    try:
        if a.command=='preflight':result=preflight(a.plan,a.prices)
        else:
            require(a.permit is not None,'LIVE_PERMIT_REQUIRED')
            result=execute(a.plan,a.prices,a.permit)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except Exception as exc:
        # No traceback/request/header/body or credential values in CLI errors.
        print(json.dumps(dict(status='STOPPED',reason=str(exc) if isinstance(exc,GateError) else type(exc).__name__),ensure_ascii=False))
        return 2

if __name__=='__main__':raise SystemExit(main())

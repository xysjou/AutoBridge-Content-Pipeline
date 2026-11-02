"""Default offline checks; protected, explicitly approved real execution only."""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from ..contract import ROOT, BASELINE, digest, require, GateError
from ..audit import preserved
from ..live.policy import (read_json, check_permit, validate_prices, REPO,
                           BRANCH, RATES)
from ..live.stages import validate_plan
from .localize import LOCALES, run_multilingual

DEFAULT_PLAN=ROOT/'cloud_pilot/runtime/trade-two-articles.plan.json'
DEFAULT_PRICES=ROOT/'cloud_pilot/runtime/prices-20261102.json'

def account_check():
    from ..live.http import JsonAPI
    require(os.environ.get('AUTOBRIDGE_ACCOUNT_CHECK_APPROVED')=='true','ACCOUNT_CHECK_APPROVAL_REQUIRED')
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    require(sha==os.environ.get('AUTOBRIDGE_APPROVED_CODE_SHA'),'ACCOUNT_CHECK_CODE_DRIFT')
    require(preserved()==[],'BASELINE_CHANGED')
    key=os.environ.get('OPENAI_API_KEY','');require(key,'PROJECT_KEY_MISSING')
    api=JsonAPI('api.openai.com',key);available=[]
    for model in RATES:
        status,obj=api.request('GET','/v1/models/'+model)
        require(status==200 and obj.get('id')==model,'PROJECT_MODEL_UNAVAILABLE:'+model)
        available.append(model)
    return dict(mode='ACCOUNT_AVAILABILITY_CHECK',available_models=available,generation_calls=0,
                note='Model metadata access is not proof that a generation request will be accepted.')

def plan_check(plan,history):
    validate_plan(plan,history)
    require(plan.get('target_site')=='https://autobridgetrade.top/','WRONG_TARGET_SITE')
    require(plan.get('locales')==list(LOCALES),'EXACT_TWELVE_LOCALES')
    require({a.get('content_type') for a in plan['articles']}=={'VEHICLE_RECOMMENDATION','BUYING_GUIDE'},'TWO_CONTENT_TYPES')
    require(plan.get('execution_phase') in ('english','full'),'EXECUTION_PHASE')
    require(plan.get('publication_enabled') is False,'WEBSITE_PUBLICATION_FORBIDDEN')

def preflight(plan_path=DEFAULT_PLAN,prices_path=DEFAULT_PRICES):
    blockers=[]
    history=read_json(ROOT/'cloud_pilot/evidence/history-snapshot.json')
    for gate,fn in [('plan',lambda:plan_check(read_json(plan_path),history)),
                    ('prices',lambda:validate_prices(read_json(prices_path))),
                    ('baseline',lambda:require(preserved()==[],'BASELINE_CHANGED'))]:
        try:fn()
        except Exception as exc:blockers.append(dict(gate=gate,reason=str(exc)))
    return dict(mode='OFFLINE_PREFLIGHT',credentials_read=False,real_api_calls=0,
        target_site='https://autobridgetrade.top/',supported_locales=list(LOCALES),
        expected_full_drafts=24,program_budget_usd=3,website_publication=False,
        blockers=blockers+[
          dict(gate='approval',reason='REVIEWED_CONTROL_COMMIT_AND_PROTECTED_DIGEST_REQUIRED'),
          dict(gate='account',reason='REAL_MODEL_AVAILABILITY_NOT_VERIFIED'),
          dict(gate='runtime',reason='MANUAL_WORKFLOW_NOT_ACTIVATED')])

def execute(plan_path,prices_path,permit_path):
    from ..live.http import JsonAPI,GitHubTransport
    from ..live.ledger import GitHubStore
    from .accounting import ResponseJournal,DurableResponses
    from .sources import retrieve
    from ..live.engine import Engine
    plan,prices,permit=map(read_json,(plan_path,prices_path,permit_path))
    history=read_json(ROOT/'cloud_pilot/evidence/history-snapshot.json')
    plan_check(plan,history)
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    approval=os.environ.get('AUTOBRIDGE_LIVE_APPROVAL_SHA256','')
    check_permit(permit,plan,prices,sha,approval)
    require(re.fullmatch(r'[0-9a-f]{40}',permit.get('approved_main_sha','')),'APPROVED_MAIN_REQUIRED')
    require(permit.get('target_site')==plan['target_site'] and permit.get('locales')==plan['locales'], 'PERMIT_TARGET_SCOPE')
    require(permit.get('execution_phase')==plan['execution_phase'],'PERMIT_PHASE_SCOPE')
    require(subprocess.run(['git','diff','--quiet','HEAD','--','cloud_pilot'],cwd=ROOT).returncode==0,
            'UNCOMMITTED_EXECUTION_CODE')
    require(preserved()==[],'BASELINE_CHANGED')
    # Checks above intentionally happen before reading either application credential.
    key=os.environ.get('OPENAI_API_KEY',''); token=os.environ.get('AUTOBRIDGE_GITHUB_TOKEN','')
    require(key and token,'PROTECTED_RUNTIME_CREDENTIALS_MISSING')
    # Longer inference timeout, still one transmission and no automatic retry.
    import http.client
    def connection(host,port,timeout,context):
        return http.client.HTTPSConnection(host,port,timeout=180,context=context)
    api=JsonAPI('api.openai.com',key,connection=connection)
    github=GitHubTransport(JsonAPI('api.github.com',token))
    def permission():
        check_permit(permit,plan,prices,sha,approval)
        require(github.ref('main')==permit['approved_main_sha'],'APPROVED_MAIN_DRIFT')
    permission()
    # Availability inspection uses only the approved project key and the two allowed model IDs.
    for model in RATES:
        status,obj=api.request('GET','/v1/models/'+model)
        require(status==200 and obj.get('id')==model,'PROJECT_MODEL_UNAVAILABLE:'+model)
    journal=ResponseJournal(GitHubStore(github))
    raw_models=DurableResponses(api,journal,prices,permission)
    class EditorialModels:
        def call(self,operation,stage,data):
            if data.get('stage')=='writing':
                data=dict(data,instruction=data['instruction']+
                    ' Include at least three substantive FAQ entries. Use article-specific Markdown H2 headings '
                    'inside section text after the opening paragraph; never include an H1 in body text.')
            result=raw_models.call(operation,stage,data)
            if data.get('stage')=='writing':
                require(len(result['content'].get('faq',[]))>=3,'ENGLISH_FAQ_INCOMPLETE')
            return result
    models=EditorialModels()
    prior=[(ROOT/d['path']).read_text() for d in history['documents'] if d['path'].startswith(('batches/','daily/'))]
    deliveries=Engine(plan,history,journal,models,github,retrieve,prior).run()
    if plan['execution_phase']=='english':
        return dict(status='ENGLISH_PHASE_COMPLETE_NOT_FULL_PRODUCTION',draft_prs=deliveries,
                    expected_final_drafts=24,website_published=False)
    return run_multilingual(plan,journal,models,github,deliveries)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['preflight','account-check','execute'],nargs='?',default='preflight')
    p.add_argument('--plan',type=Path,default=DEFAULT_PLAN)
    p.add_argument('--prices',type=Path,default=DEFAULT_PRICES)
    p.add_argument('--permit',type=Path)
    a=p.parse_args()
    try:
        if a.command=='preflight':result=preflight(a.plan,a.prices)
        elif a.command=='account-check':result=account_check()
        else:
            require(a.permit is not None,'APPROVED_PERMIT_REQUIRED')
            result=execute(a.plan,a.prices,a.permit)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except Exception as exc:
        print(json.dumps(dict(status='STOPPED',reason=str(exc) if isinstance(exc,GateError) else type(exc).__name__)))
        return 2

if __name__=='__main__':raise SystemExit(main())

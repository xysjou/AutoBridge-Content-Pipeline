"""Reproducible two-article mock pilot; --verify performs no writes."""
import argparse
import json
from pathlib import Path
import socket
import tempfile
from unittest.mock import patch
from .contract import ROOT, canonical, require, digest
from .state import LocalFileCAS, replay
from .delivery import run_one
from .audit import preserved
from .cli import save_new

def run(verify=False):
    folder=ROOT/'cloud_pilot'
    history=json.loads((folder/'evidence/history-snapshot.json').read_text())
    with tempfile.TemporaryDirectory() as temp, patch.object(socket.socket,'connect',side_effect=AssertionError('NETWORK_FORBIDDEN')):
        store=LocalFileCAS(Path(temp)/'journal.json');store.initialize()
        output=[]
        for aid in ('MOCK-AURORA','MOCK-BOREAL'):
            fixture=json.loads((folder/'fixtures'/f'{aid}.json').read_text())
            result=run_one(fixture,history,store,[r['article']['body'] for r in output])
            output.append(result)
            for kind,packet in result.items():
                target=folder/'evidence/pilot'/aid/'v1'/f'{kind}.json'
                if verify:require(json.loads(target.read_text())==packet,'PILOT_REPRODUCIBILITY')
                else:save_new(target,packet)
            body='# SYNTHETIC MOCK — NOT A RESEARCHED OR PUBLISHABLE ARTICLE\n\n## '+result['article']['title']+'\n\n'+result['article']['body']+'\n'
            target=folder/'evidence/pilot'/aid/'v1/article.en.md'
            if verify or target.exists():require(target.read_text()==body,'ARTICLE_IMMUTABLE')
            else:
                with target.open('x') as stream:stream.write(body)
        before,token=store.read()
        for result in output:
            run_one(json.loads((folder/'fixtures'/f"{result['article']['article_id']}.json").read_text()),history,store)
        require(store.read()[1]==token,'RERUN_NOT_IDEMPOTENT')
        target=folder/'state/program-journal.json'
        if verify:require(json.loads(target.read_text())==before,'JOURNAL_REPRODUCIBILITY')
        else:save_new(target,before)
        require(preserved()==[],'EXISTING_FILE_CHANGED')
        view=replay(before)
        summary=dict(mode='mock',articles=len(output),events=len(before['events']),journal_head=view['head'],
              program_cap_usd=3,simulated_accounted_usd=view['allocated']/1_000_000_000,
              actual_paid_api_calls=0,actual_api_cost_usd=0,existing_files_changed=0,
              statuses=view['items'],production_eligible=0,
              reviewer_kind='INDEPENDENT_DETERMINISTIC_MODULE_NOT_AI_EDITORIAL_REVIEW')
        if verify:require(json.loads((folder/'evidence/pilot-summary.json').read_text())==summary,'SUMMARY_CHANGED')
        else:save_new(folder/'evidence/pilot-summary.json',summary)
        return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--verify',action='store_true')
    print(json.dumps(run(parser.parse_args().verify),indent=2))

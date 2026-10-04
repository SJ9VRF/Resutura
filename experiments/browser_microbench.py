from pathlib import Path as _Path
import sys as _sys
_ROOT=_Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:_sys.path.insert(0,str(_ROOT))
import json
from resutura.agent import BaseAgent, RetryAgent, RewindAgent, VerificationAwareAgent, ResuturaAgent
from resutura.envs.browser import BrowserResearchWorkflowEnv
from resutura.envs.sandbox import make_task
from resutura.perturbations import Perturbation, PerturbationEngine
from resutura.metrics import summarize
from resutura.provenance import experiment_metadata

AGENTS={'base':BaseAgent,'retry':RetryAgent,'verify':VerificationAwareAgent,'rewind':RewindAgent,'resutura':ResuturaAgent}
CASES=['close_spreadsheet_tab','lose_focus','redirect_publish_target','ambiguous_publish_timeout']

def main(n=2):
    out={**experiment_metadata('chromium_mechanism_microbench','paired deterministic tasks; real Chromium DOM, local effect ledger',n*len(CASES)),
         'experiment':'chromium_mechanism_microbench',
         'integrity_note':'Real Chromium mechanism microbenchmark. Not OSWorld, not a frontier-model evaluation, and not evidence of SOTA.',
         'cases':{c:{} for c in CASES}}
    e=BrowserResearchWorkflowEnv()
    try:
        for name,cls in AGENTS.items():
            for case in CASES:
                runs=[]
                for i in range(n):
                    trigger=4 if case in {'close_spreadsheet_tab','lose_focus'} else 17
                    runs.append(cls().run(e,make_task(i,3),PerturbationEngine([Perturbation(case,trigger)]),seed=i))
                out['cases'][case][name]=summarize(runs)
    finally:
        e.close()
    _Path('runs').mkdir(exist_ok=True)
    _Path('runs/browser_microbench.json').write_text(json.dumps(out,indent=2,sort_keys=True))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

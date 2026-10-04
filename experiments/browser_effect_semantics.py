from pathlib import Path as _Path
import sys as _sys
_ROOT=_Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:_sys.path.insert(0,str(_ROOT))
import json
from resutura.agent import BaseAgent,RetryAgent,VerificationAwareAgent,RewindAgent,ResuturaAgent
from resutura.envs.browser import BrowserResearchWorkflowEnv
from resutura.envs.sandbox import make_task
from resutura.perturbations import Perturbation,PerturbationEngine
from resutura.metrics import summarize
from resutura.provenance import experiment_metadata

AGENTS={'base':BaseAgent,'retry':RetryAgent,'verify':VerificationAwareAgent,'rewind':RewindAgent,'resutura':ResuturaAgent}
CASE_SPECS={
 'misdirected_commit':[('redirect_publish_target',17)],
 'concurrent_change_plus_misdirection':[('concurrent_valid_publication',16),('redirect_publish_target',17)],
 'noncompensatable_commit':[('redirect_publish_noncompensatable',17)],
 'ambiguous_commit':[('ambiguous_publish_timeout',17)],
}
def engine(specs): return PerturbationEngine([Perturbation(t,s) for t,s in specs])

def main(n=2):
    out={**experiment_metadata('chromium_effect_semantics','paired deterministic tasks; fresh faults per method; real Chromium DOM; deterministic planner',n*len(CASE_SPECS)),
         'integrity_note':'Real Chromium mechanism-transfer study with deterministic planner. Not model-backed, not OSWorld, not SOTA evidence.',
         'methodological_note':'Every run receives a fresh perturbation engine; consumed fault objects are never shared across methods.','cases':{k:{} for k in CASE_SPECS}}
    env=BrowserResearchWorkflowEnv()
    try:
        for name,cls in AGENTS.items():
            for case,specs in CASE_SPECS.items():
                runs=[]
                for i in range(n): runs.append(cls().run(env,make_task(i,3),engine(specs),seed=i))
                out['cases'][case][name]=summarize(runs)
    finally: env.close()
    _Path('runs/browser_effect_semantics.json').write_text(json.dumps(out,indent=2,sort_keys=True))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

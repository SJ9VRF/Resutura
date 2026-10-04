from pathlib import Path as _Path
import sys as _sys
_ROOT = _Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))
from collections import defaultdict
import json
from pathlib import Path
from resutura.agent import BaseAgent, RetryAgent, RewindAgent, ResuturaAgent
from resutura.envs.sandbox import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine
from resutura.metrics import summarize

PERTURBATIONS=["close_spreadsheet_tab","transient_failure","lose_focus","switch_active_tab"]
AGENTS={"base":BaseAgent,"retry":RetryAgent,"rewind":RewindAgent,"resutura":ResuturaAgent}

def main(n_per=40):
    out={}
    for p in PERTURBATIONS:
        out[p]={}
        for name,cls in AGENTS.items():
            runs=[]
            for i in range(n_per):
                t=make_task(i,3+(i%2))
                trigger=4+(i%5)
                runs.append(cls().run(ResearchWorkflowEnv(),t,PerturbationEngine([Perturbation(p,trigger)]),seed=i))
            out[p][name]=summarize(runs)
    Path('runs').mkdir(exist_ok=True)
    Path('runs/perturbation_breakdown.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()

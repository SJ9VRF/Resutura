from pathlib import Path as _Path
import sys as _sys
_ROOT = _Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))
import json
from pathlib import Path
from resutura.agent import BaseAgent, RetryAgent, RewindAgent, ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine
from resutura.metrics import summarize
from resutura.provenance import experiment_metadata

AGENTS={"base":BaseAgent,"retry":RetryAgent,"rewind":RewindAgent,"resutura":ResuturaAgent}

def publish_step(task):
    return 4 * len(task.papers) + 5

def main(n_per=60):
    out={**experiment_metadata("external_effect_reconciliation", "seed=i paired across methods", n_per), "experiment":"external_effect_reconciliation","trials_per_agent":n_per,
         "failure":"publish commits to wrong external target; local checkpoint rewind cannot erase it",
         "integrity_note":"Deterministic simulator mechanism study; not a real-world/SOTA benchmark.","agents":{}}
    for name, cls in AGENTS.items():
        runs=[]
        for i in range(n_per):
            task=make_task(1000+i, 3+(i%2))
            pe=PerturbationEngine([Perturbation("redirect_publish_target",publish_step(task))], seed=i)
            runs.append(cls().run(ResearchWorkflowEnv(),task,pe,seed=i))
        out["agents"][name]={"summary":summarize(runs),"runs":[r.to_dict() for r in runs]}
    Path("runs").mkdir(exist_ok=True)
    Path("runs/external_effect_recovery.json").write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v["summary"] for k,v in out["agents"].items()},indent=2))

if __name__=="__main__": main()

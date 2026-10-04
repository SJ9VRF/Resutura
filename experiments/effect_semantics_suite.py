from pathlib import Path as _Path
import sys as _sys
_ROOT = _Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))

import json
from pathlib import Path
from resutura.agent import BaseAgent, RetryAgent, VerificationAwareAgent, RewindAgent, ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine
from resutura.metrics import summarize
from resutura.provenance import experiment_metadata, write_json_gzip_deterministic

AGENTS={"base":BaseAgent,"retry":RetryAgent,"verify":VerificationAwareAgent,"rewind":RewindAgent,"resutura":ResuturaAgent}
SCENARIOS={
    "compensable_misdirection":["redirect_publish_target"],
    "ambiguous_commit":["ambiguous_publish_timeout"],
    "concurrent_change_plus_misdirection":["concurrent_valid_publication","redirect_publish_target"],
    "noncompensatable_misdirection":["redirect_publish_noncompensatable"],
}

def publish_step(task): return 4 * len(task.papers) + 5

def main(n_per=40):
    out={
        **experiment_metadata("effect_semantics_suite", "seed=i within each method/scenario; paired identical task+fault seeds across methods", n_per),
        "experiment":"effect_semantics_suite",
        "trials_per_agent_per_scenario":n_per,
        "integrity_note":"Deterministic semantics study. It tests recovery contracts, not real-browser model capability or SOTA.",
        "scenarios":{},
    }
    for scenario,kinds in SCENARIOS.items():
        out["scenarios"][scenario]={}
        for name,cls in AGENTS.items():
            runs=[]
            for i in range(n_per):
                task=make_task(5000+i,3+(i%2)); step=publish_step(task)
                pe=PerturbationEngine([Perturbation(k,step) for k in kinds],seed=i)
                runs.append(cls().run(ResearchWorkflowEnv(),task,pe,seed=i))
            out["scenarios"][scenario][name]={"summary":summarize(runs),"runs":[r.to_dict() for r in runs]}
    Path("runs").mkdir(exist_ok=True)
    write_json_gzip_deterministic("runs/effect_semantics_suite.json.gz",out)
    compact={s:{a:d["summary"] for a,d in agents.items()} for s,agents in out["scenarios"].items()}
    print(json.dumps(compact,indent=2))

if __name__=="__main__": main()

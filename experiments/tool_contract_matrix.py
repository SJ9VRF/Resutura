from pathlib import Path as _Path
import sys as _sys
_ROOT = _Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))

from pathlib import Path
import json
from resutura.agent import BaseAgent, RetryAgent, VerificationAwareAgent, RewindAgent, ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.schemas import EffectContract
from resutura.perturbations import Perturbation, PerturbationEngine
from resutura.metrics import summarize
from resutura.provenance import experiment_metadata, write_json_gzip_deterministic

AGENTS=[BaseAgent,RetryAgent,VerificationAwareAgent,RewindAgent,ResuturaAgent]
CONTRACTS={
    "readback_only": EffectContract(readback=True,idempotency=False,compensation=True),
    "idempotency_only": EffectContract(readback=False,idempotency=True,compensation=True),
    "readback_plus_idempotency": EffectContract(readback=True,idempotency=True,compensation=True),
    "neither": EffectContract(readback=False,idempotency=False,compensation=True),
}

def publish_step(task): return 4*len(task.papers)+5

def main(n=40):
    out={**experiment_metadata("tool_contract_matrix", "seed=0..n-1 paired across methods/contracts", n), "study":"tool_contract_matrix","fault":"ambiguous_publish_unobservable","n_per_cell":n,"cells":{}}
    for cname,contract in CONTRACTS.items():
        out["cells"][cname]={}
        for cls in AGENTS:
            runs=[]
            for seed in range(n):
                task=make_task(4000+seed,3)
                pe=PerturbationEngine([Perturbation("ambiguous_publish_unobservable",publish_step(task))],seed=seed)
                runs.append(cls().run(ResearchWorkflowEnv(effect_contract=contract),task,pe,seed=seed))
            summ=summarize(runs)
            out["cells"][cname][cls.name]={"summary":summ,"runs":[r.to_dict() for r in runs]}
    Path("runs").mkdir(exist_ok=True)
    write_json_gzip_deterministic("runs/tool_contract_matrix.json.gz",out)
    compact={c:{a:d["summary"] for a,d in v.items()} for c,v in out["cells"].items()}
    print(json.dumps(compact,indent=2))

if __name__=="__main__": main()

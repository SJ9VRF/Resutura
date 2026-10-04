from pathlib import Path as _Path
import sys as _sys
_ROOT=_Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:_sys.path.insert(0,str(_ROOT))

import json
from pathlib import Path
from resutura.agent import ResuturaAgent
from resutura.recovery import EffectSemanticRecoveryController
from resutura.schemas import RecoveryCandidate, RecoveryLevel
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine
from resutura.metrics import summarize
from resutura.provenance import experiment_metadata, write_json_gzip_deterministic

SCENARIOS={
    "compensable_misdirection":["redirect_publish_target"],
    "ambiguous_commit":["ambiguous_publish_timeout"],
    "concurrent_change_plus_misdirection":["concurrent_valid_publication","redirect_publish_target"],
    "noncompensatable_misdirection":["redirect_publish_noncompensatable"],
}

def publish_step(task): return 4*len(task.papers)+5

class NoCompensationController(EffectSemanticRecoveryController):
    """Ablation: remove forward-compensation as a recovery option."""
    def candidates(self,f,env,proposal):
        xs=super().candidates(f,env,proposal)
        kept=[x for x in xs if x.level != RecoveryLevel.COMPENSATE]
        return kept or [RecoveryCandidate(RecoveryLevel.SAFE_ABORT,"No compensation path available",1.0,.1,.1,.01,0,0,self.causal_slice(f,proposal))]

class NoContractAwarenessController(EffectSemanticRecoveryController):
    """Ablation: ignore readback/idempotency and blindly replay ambiguous commits."""
    def candidates(self,f,env,proposal):
        if f.failure_subtype == "AMBIGUOUS_COMMIT":
            return [RecoveryCandidate(RecoveryLevel.RETRY,"Blind replay without consulting the effect contract",.5,1,1,.2,0,.2,self.causal_slice(f,proposal))]
        return super().candidates(f,env,proposal)

class NoOwnershipController(EffectSemanticRecoveryController):
    """Ablation: compensate by target only, ignoring actor ownership/protected state."""
    def _materialize(self,level,f,env,proposal):
        if level == RecoveryLevel.COMPENSATE:
            intended=proposal.action.target
            ledger=env.observe().get("effect_ledger",[])
            wrong=next((x.get("actual_target") for x in ledger
                        if x.get("kind")=="publish" and x.get("actual_target") != intended
                        and not x.get("compensated",False)),None)
            acts=[]
            if wrong:
                from resutura.schemas import Action
                acts.append(Action("retract_publication",wrong))
                acts.append(Action("publish",intended))
            return acts,proposal.expected_postconditions
        return super()._materialize(level,f,env,proposal)

class FullResutura(ResuturaAgent):
    name="full"

class NoCompensationResutura(ResuturaAgent):
    name="minus_compensation"
    def __init__(self):
        super().__init__(); self.controller=NoCompensationController()

class NoContractAwarenessResutura(ResuturaAgent):
    name="minus_contract_awareness"
    def __init__(self):
        super().__init__(); self.controller=NoContractAwarenessController()

class NoOwnershipResutura(ResuturaAgent):
    name="minus_effect_ownership"
    def __init__(self):
        super().__init__(); self.controller=NoOwnershipController()

VARIANTS=[FullResutura,NoCompensationResutura,NoContractAwarenessResutura,NoOwnershipResutura]

def main(n=40):
    out={**experiment_metadata("ablation_suite","seed=i paired across variants/scenarios; same generated task and fault spec",n),
         "experiment":"ablation_suite","n_per_cell":n,
         "integrity_note":"Component ablation in the deterministic simulator. It isolates recovery semantics; it is not model-capability evidence.",
         "variants":{},"scenarios":SCENARIOS}
    for cls in VARIANTS:
        out["variants"][cls.name]={}
        for scenario,kinds in SCENARIOS.items():
            runs=[]
            for seed in range(n):
                task=make_task(7000+seed,3+(seed%2)); step=publish_step(task)
                pe=PerturbationEngine([Perturbation(k,step) for k in kinds],seed=seed)
                runs.append(cls().run(ResearchWorkflowEnv(),task,pe,seed=seed))
            out["variants"][cls.name][scenario]={"summary":summarize(runs),"runs":[r.to_dict() for r in runs]}
    Path("runs").mkdir(exist_ok=True)
    write_json_gzip_deterministic("runs/ablation_suite.json.gz",out)
    compact={v:{s:d["summary"] for s,d in scenarios.items()} for v,scenarios in out["variants"].items()}
    print(json.dumps(compact,indent=2))

if __name__=="__main__": main()

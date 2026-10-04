from __future__ import annotations
import json, random
from pathlib import Path
from .agent import BaseAgent, RetryAgent, RewindAgent, ResuturaAgent
from .envs.sandbox import ResearchWorkflowEnv, make_task
from .perturbations import PerturbationEngine, standard_perturbation
from .metrics import summarize
from .provenance import experiment_metadata

AGENTS={"base":BaseAgent,"retry":RetryAgent,"rewind":RewindAgent,"resutura":ResuturaAgent}

def run_experiment(trials=120, seed=7, perturb=True):
    all_results={}
    for name, cls in AGENTS.items():
        runs=[]
        for i in range(trials):
            task=make_task(i,3+(i%2))
            pe=PerturbationEngine([standard_perturbation(seed+i, trigger_step=4+(i%5))],seed+i) if perturb else None
            runs.append(cls().run(ResearchWorkflowEnv(),task,pe,seed+i))
        all_results[name]={"summary":summarize(runs),"runs":[r.to_dict() for r in runs]}
    return {**experiment_metadata("resutura_deterministic_pilot", f"seed={seed}+i paired by task index across methods", trials),
            "experiment":"resutura_deterministic_pilot","seed":seed,"trials_per_agent":trials,"perturbed":perturb,"agents":all_results,
            "integrity_note":"Results are from the deterministic local research sandbox, not frontier models or real browser environments."}

def save_json(obj,path):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2)); return p

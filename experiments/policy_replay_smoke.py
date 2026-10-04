from pathlib import Path as _Path
import sys as _sys
_ROOT=_Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:_sys.path.insert(0,str(_ROOT))
import argparse,json,tempfile
from resutura.model_policy import RecordedPolicyProvider
from resutura.policy_agent import PolicyDrivenResuturaAgent
from resutura.envs.sandbox import ResearchWorkflowEnv,make_task
from resutura.planner import WorkflowPlanner
from resutura.perturbations import Perturbation,PerturbationEngine
from resutura.provenance import experiment_metadata

def proposal_dict(p):
    return {'proposal':{'action':{'type':p.action.type,'target':p.action.target,'value':p.action.value,'args':p.action.args},'intent':p.intent,
      'expected_postconditions':[{'key':x.key,'op':x.op,'value':x.value,'confidence':x.confidence,'critical':x.critical} for x in p.expected_postconditions],
      'risk':p.risk.value,'reversibility':p.reversibility,'subgoal':p.subgoal}}

def main(n=20):
    runs=[]
    for i in range(n):
        task=make_task(i,3); rec=[proposal_dict(p) for p in WorkflowPlanner().build_plan(task)]+[{'stop':True}]
        provider=RecordedPolicyProvider(rec)
        agent=PolicyDrivenResuturaAgent(provider)
        eng=PerturbationEngine([Perturbation('redirect_publish_target',17)])
        runs.append(agent.run(ResearchWorkflowEnv(),task,eng,seed=i).to_dict())
    out={**experiment_metadata('policy_replay_smoke','recorded policy decisions; recovery runtime online; not model-backed',n),
         'integrity_note':'Recorded deterministic policy fixture. This validates the provider boundary and recovery integration; it is not evidence about any language model.',
         'successes':sum(int(r['success']) for r in runs),'trials':n,'runs':runs}
    _Path('runs/policy_replay_smoke.json').write_text(json.dumps(out,indent=2,sort_keys=True))
    print(json.dumps({'successes':out['successes'],'trials':n},indent=2))
if __name__=='__main__':main()

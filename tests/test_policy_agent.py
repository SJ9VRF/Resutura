from resutura.envs.sandbox import ResearchWorkflowEnv,make_task
from resutura.planner import WorkflowPlanner
from resutura.model_policy import RecordedPolicyProvider
from resutura.policy_agent import PolicyDrivenResuturaAgent
from resutura.perturbations import Perturbation,PerturbationEngine

def _rec(p):
    return {'proposal':{'action':{'type':p.action.type,'target':p.action.target,'value':p.action.value,'args':p.action.args},'intent':p.intent,
        'expected_postconditions':[{'key':x.key,'op':x.op,'value':x.value} for x in p.expected_postconditions],
        'risk':p.risk.value,'reversibility':p.reversibility,'subgoal':p.subgoal}}

def test_policy_driven_runtime_recovers_misdirected_commit():
    t=make_task(0,3); rec=[_rec(p) for p in WorkflowPlanner().build_plan(t)]+[{'stop':True}]
    run=PolicyDrivenResuturaAgent(RecordedPolicyProvider(rec)).run(ResearchWorkflowEnv(),t,PerturbationEngine([Perturbation('redirect_publish_target',17)]),seed=0)
    assert run.success
    assert run.metadata['policy_provider']=='RecordedPolicyProvider'
    assert run.metadata['model_backed'] is False

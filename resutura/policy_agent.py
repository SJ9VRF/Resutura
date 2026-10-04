from __future__ import annotations
from .agent import ResuturaAgent, _run_id
from .schemas import *
from .state import StateStore
from .checkpoint import CheckpointManager
from .risk import classify_action, requires_checkpoint
from .model_policy import PolicyRequest, PolicyProvider, effect_contract_dict

class PolicyDrivenResuturaAgent(ResuturaAgent):
    """Resutura recovery loop with action proposals supplied by an external/replayed policy.

    The policy chooses task actions; Resutura owns verification/recovery semantics. This
    separation lets the same recovery runtime be evaluated with real model policies later
    without changing the recovery implementation.
    """
    name='resutura_policy'
    def __init__(self, provider:PolicyProvider):
        super().__init__(); self.provider=provider

    def run(self, env, task, perturbations=None, seed=0, max_steps=160):
        env.reset(task)
        store=StateStore(AgentState(task_goal=f'Research {len(task.papers)} papers and save sheet+comparison'))
        store.update_from_observation(env.observe())
        cps=CheckpointManager(); cps.create(0,env,store.snapshot())
        steps=[]; injected=detected=recovered=false_alarms=0; physical_step=0; aborted=False
        history=[]
        while physical_step < max_steps:
            req=PolicyRequest(
                task={'task_id':task.task_id,'papers':task.papers,'publish_target':task.publish_target},
                observation=env.observe(), effect_contract=effect_contract_dict(env), history=history[-12:],
                step=physical_step+1, allowed_actions=sorted(__import__('resutura.model_policy',fromlist=['ALLOWED_ACTIONS']).ALLOWED_ACTIONS))
            resp=self.provider.next(req)
            if resp.stop or resp.proposal is None: break
            proposal=resp.proposal
            proposal.risk=classify_action(proposal.action) if proposal.risk==RiskLevel.SAFE else proposal.risk
            if requires_checkpoint(proposal.action): cps.create(physical_step,env,store.snapshot())
            physical_step+=1
            if perturbations: injected += len(perturbations.before_action(env,physical_step,proposal.action))
            result=env.execute(proposal.action); store.record_action(proposal.action,result); store.update_from_observation(result.observation)
            det=self.verifier.verify(proposal,result); failure=None; recovery=None
            if det.diverged:
                detected+=1; failure=self.diagnoser.diagnose(physical_step,proposal,result,det,steps)
                rplan=self.controller.select(failure,env,proposal)
                offline=self.controller.empirical_counterfactuals(failure,env,proposal)
                if offline: rplan.counterfactuals=offline
                recovery=self._execute_recovery(rplan,env,cps,store,proposal)
                physical_step += recovery.steps_used
                if recovery.succeeded: recovered+=1; store.update_from_observation(env.observe())
                elif failure.risk_if_ignored==RiskLevel.HIGH: aborted=True
            steps.append(TrajectoryStep(physical_step,proposal,result,det,failure,recovery))
            history.append({'step':physical_step,'proposal':{'type':proposal.action.type,'target':proposal.action.target,'intent':proposal.intent},'result':{'ok':result.ok,'message':result.message},'recovery': recovery.level.value if recovery else None})
            if aborted: break
        rr=RunRecord(_run_id(self.name,task.task_id,seed),task.task_id,self.name,seed,(env.grade() and not aborted),steps,env.observe(),injected,detected,recovered,false_alarms,0,aborted)
        rr.metadata={'policy_provider':type(self.provider).__name__,'policy_actions':len(history),'model_backed':False if type(self.provider).__name__=='RecordedPolicyProvider' else None}
        return rr

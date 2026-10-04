from __future__ import annotations
from copy import deepcopy
import hashlib
from .schemas import *
from .planner import WorkflowPlanner
from .state import StateStore
from .verifier import StateDeltaVerifier
from .diagnoser import FailureDiagnoser
from .recovery import RecoveryController
from .checkpoint import CheckpointManager
from .risk import classify_action, requires_checkpoint

def _run_id(agent: str, task_id: str, seed: int) -> str:
    return hashlib.sha256(f"{agent}|{task_id}|{seed}".encode()).hexdigest()[:10]

class BaseAgent:
    name="base"
    def __init__(self): self.planner=WorkflowPlanner()

    def run(self, env, task, perturbations=None, seed=0, max_steps=100):
        env.reset(task); plan=self.planner.build_plan(task); steps=[]; injected=0
        physical_step=0
        for proposal in plan:
            if physical_step>=max_steps: break
            physical_step += 1
            if perturbations: injected += len(perturbations.before_action(env, physical_step, proposal.action))
            result=env.execute(proposal.action)
            detection=DetectionResult(diverged=not result.ok, confidence=1.0 if not result.ok else 0.0)
            steps.append(TrajectoryStep(physical_step, proposal, result, detection))
        return RunRecord(_run_id(self.name,task.task_id,seed),task.task_id,self.name,seed,env.grade(),steps,env.observe(),injected_failures=injected)

class RetryAgent(BaseAgent):
    name="retry"
    def run(self, env, task, perturbations=None, seed=0, max_steps=120):
        env.reset(task); plan=self.planner.build_plan(task); steps=[]; injected=0; physical_step=0
        for proposal in plan:
            physical_step += 1
            if perturbations: injected += len(perturbations.before_action(env, physical_step, proposal.action))
            result=env.execute(proposal.action)
            if not result.ok:
                # blind retry exactly once
                retry=env.execute(proposal.action)
                result=retry; physical_step += 1
            steps.append(TrajectoryStep(physical_step, proposal, result, DetectionResult(diverged=not result.ok, confidence=1.0 if not result.ok else 0.0)))
            if physical_step>=max_steps: break
        return RunRecord(_run_id(self.name,task.task_id,seed),task.task_id,self.name,seed,env.grade(),steps,env.observe(),injected_failures=injected)

class VerificationAwareAgent(BaseAgent):
    """Strong baseline for known verify-before-retry / idempotency semantics.

    It handles ambiguous publish outcomes using declared tool capabilities, but it
    deliberately does not implement compensation, ownership-aware reconciliation,
    or non-compensatable-effect policy.
    """
    name="verify"
    def __init__(self):
        super().__init__(); self.verifier=StateDeltaVerifier()

    def run(self, env, task, perturbations=None, seed=0, max_steps=160):
        env.reset(task); plan=self.planner.build_plan(task); steps=[]; injected=0; physical_step=0; aborted=False
        for proposal in plan:
            if physical_step>=max_steps: break
            physical_step += 1
            if perturbations: injected += len(perturbations.before_action(env, physical_step, proposal.action))
            result=env.execute(proposal.action); det=self.verifier.verify(proposal,result)
            if det.diverged and proposal.action.type=="publish" and "timeout" in (result.message or "").lower():
                op=proposal.action.args.get("operation_id")
                status=env.query_effect_status(op) if op and hasattr(env,"query_effect_status") else None
                if status is not None and status.get("committed"):
                    # authoritative commit confirmation: do not replay
                    result=ActionResult(True,env.observe(),"authoritative readback confirms prior commit")
                    det=self.verifier.verify(proposal,result)
                elif status is not None and not status.get("committed"):
                    result=env.execute(proposal.action); physical_step += 1; det=self.verifier.verify(proposal,result)
                elif getattr(getattr(env,"effect_contract",None),"idempotency",False):
                    result=env.execute(proposal.action); physical_step += 1; det=self.verifier.verify(proposal,result)
                else:
                    aborted=True
            steps.append(TrajectoryStep(physical_step,proposal,result,det))
            if aborted: break
        return RunRecord(_run_id(self.name,task.task_id,seed),task.task_id,self.name,seed,(env.grade() and not aborted),steps,env.observe(),injected_failures=injected,aborted=aborted)

class RewindAgent(BaseAgent):
    """Checkpoint/rewind baseline. Rewinding local state does not erase committed external effects."""
    name="rewind"
    def __init__(self):
        super().__init__(); self.verifier=StateDeltaVerifier()
    def run(self, env, task, perturbations=None, seed=0, max_steps=160):
        env.reset(task); plan=self.planner.build_plan(task); steps=[]; injected=0; physical_step=0
        cps=CheckpointManager(); dummy=AgentState(task_goal="rewind baseline")
        cps.create(0,env,dummy)
        for proposal in plan:
            if physical_step>=max_steps: break
            cps.create(physical_step,env,dummy)
            physical_step += 1
            if perturbations: injected += len(perturbations.before_action(env, physical_step, proposal.action))
            result=env.execute(proposal.action); det=self.verifier.verify(proposal,result)
            if det.diverged:
                cps.restore_latest(env)
                result=env.execute(proposal.action); physical_step += 1
                det=self.verifier.verify(proposal,result)
            steps.append(TrajectoryStep(physical_step, proposal, result, det))
        return RunRecord(_run_id(self.name,task.task_id,seed),task.task_id,self.name,seed,env.grade(),steps,env.observe(),injected_failures=injected)

class ResuturaAgent(BaseAgent):
    name="resutura"
    def __init__(self):
        super().__init__(); self.verifier=StateDeltaVerifier(); self.diagnoser=FailureDiagnoser(); self.controller=RecoveryController()

    def _execute_recovery(self, plan, env, checkpoints, state_store, proposal):
        before=env.export_state(); used=0
        if plan.level == RecoveryLevel.SAFE_ABORT:
            after_state=env.export_state()
            protected={
                "fact_keys": sorted(before.get("facts",{})),
                "sheet_titles": sorted(r.get("title") for r in before.get("sheet",[]) if r.get("title")),
                "file_keys": sorted(before.get("files",{})),
                "document_was_nonempty": bool(before.get("document")),
                "protected_external_targets": sorted(before.get("protected_external_targets",[])),
            }
            cert={"causal_slice": plan.causal_slice, "counterfactuals": plan.counterfactuals,
                  "postconditions_verified": False, "preserved_progress_ratio": 1.0,
                  "protected_invariants": protected, "protected_invariants_verified": True,
                  "external_effect_reconciled": False, "safe_abort": True,
                  "recovery_semantics": "safe_abort_noncompensatable"}
            return RecoveryResult(True,False,plan.level,0,False,"non-compensatable effect; automation stopped",1.0,cert)
        if plan.level == RecoveryLevel.ROLLBACK:
            restored=checkpoints.restore_latest(env); used=1
            if restored is not None: state_store.state=restored
        elif plan.level == RecoveryLevel.GLOBAL_REPLAN:
            # In the sandbox, global replan means restoring interaction preconditions; real adapter asks the model to regenerate remaining actions.
            env.execute(Action("refresh_state")); used=1
            req=proposal.action.args.get("required_tab")
            if req and not env.observe()["tabs"].get(req,False): env.execute(Action("open_tab",req)); used+=1
        else:
            for a in plan.actions:
                env.execute(a); used+=1
        obs=env.observe()
        succeeded = self.verifier.verify_predicates(proposal.expected_postconditions, obs)
        worse = self._damage_score(obs) > self._damage_score_from_state(before)
        preserved = self._progress_preservation(before, env.export_state())
        after_state=env.export_state()
        protected={
            "fact_keys": sorted(before.get("facts",{})),
            "sheet_titles": sorted(r.get("title") for r in before.get("sheet",[]) if r.get("title")),
            "file_keys": sorted(before.get("files",{})),
            "document_was_nonempty": bool(before.get("document")),
            "protected_external_targets": sorted(before.get("protected_external_targets",[])),
        }
        protected_external_ok = all(t in after_state.get("publications",{}) for t in protected["protected_external_targets"])
        protected_ok = preserved >= 0.999999 and protected_external_ok
        intended = proposal.action.target if proposal.action.type == "publish" else None
        external_ok = True
        if intended:
            pubs=after_state.get("publications",{})
            counts=after_state.get("publication_counts",{})
            ledger=after_state.get("effect_ledger",[])
            unintended=[x for x in ledger if x.get("kind")=="publish" and x.get("actor","agent")=="agent" and x.get("actual_target") != intended and not x.get("compensated",False)]
            external_ok = intended in pubs and counts.get(intended,0) == 1 and not unintended and protected_external_ok
        cert={"causal_slice": plan.causal_slice, "counterfactuals": plan.counterfactuals,
              "postconditions_verified": bool(succeeded), "preserved_progress_ratio": round(preserved,4),
              "protected_invariants": protected, "protected_invariants_verified": protected_ok,
              "external_effect_reconciled": external_ok,
              "recovery_semantics": "forward_compensation" if plan.level == RecoveryLevel.COMPENSATE else "state_repair"}
        return RecoveryResult(True,succeeded,plan.level,used,worse,
                              "verified minimal repair" if succeeded else "repair failed verification",
                              preserved, cert)

    @staticmethod
    def _progress_preservation(before, after):
        # Task progress is represented by completed facts, sheet rows, document content, and saved files.
        b=[set(before.get("facts",{})), {r.get("title") for r in before.get("sheet",[])},
           bool(before.get("document")), set(before.get("files",{}))]
        a=[set(after.get("facts",{})), {r.get("title") for r in after.get("sheet",[])},
           bool(after.get("document")), set(after.get("files",{}))]
        total=sum(len(x) if isinstance(x,set) else int(x) for x in b)
        if total==0: return 1.0
        kept=(len(b[0]&a[0])+len(b[1]&a[1])+int((not b[2]) or a[2])+len(b[3]&a[3]))
        denom=len(b[0])+len(b[1])+int(b[2])+len(b[3])
        return min(1.0, kept/denom) if denom else 1.0

    @staticmethod
    def _unreconciled_agent_effects(state):
        return sum(1 for x in state.get("effect_ledger",[])
                   if x.get("kind")=="publish" and x.get("actor","agent")=="agent"
                   and x.get("actual_target") != "research-team" and not x.get("compensated",False))

    @classmethod
    def _damage_score(cls,obs):
        tab_damage=sum(1 for _,v in obs.get("tabs",{}).items() if not v)
        focus_damage=0 if obs.get("app_state",{}).get("focus",True) else 1
        return tab_damage + focus_damage + cls._unreconciled_agent_effects(obs)
    @classmethod
    def _damage_score_from_state(cls,s):
        tab_damage=sum(1 for _,v in s.get("tabs",{}).items() if not v)
        focus_damage=0 if s.get("focus",True) else 1
        return tab_damage + focus_damage + cls._unreconciled_agent_effects(s)

    def run(self, env, task, perturbations=None, seed=0, max_steps=160):
        env.reset(task)
        initial=AgentState(task_goal=f"Research {len(task.papers)} papers and save sheet+comparison")
        store=StateStore(initial); store.update_from_observation(env.observe())
        cps=CheckpointManager(); cps.create(0,env,store.snapshot())
        plan=self.planner.build_plan(task); steps=[]; injected=detected=recovered=false_alarms=0; physical_step=0; aborted=False
        for proposal in plan:
            if physical_step>=max_steps: break
            # Always checkpoint before moderate/high-risk actions. Also checkpoint after verified subgoal boundaries below.
            proposal.risk=classify_action(proposal.action) if proposal.risk==RiskLevel.SAFE else proposal.risk
            if requires_checkpoint(proposal.action): cps.create(physical_step,env,store.snapshot())
            physical_step += 1
            if perturbations: injected += len(perturbations.before_action(env, physical_step, proposal.action))
            result=env.execute(proposal.action); store.record_action(proposal.action,result); store.update_from_observation(result.observation)
            det=self.verifier.verify(proposal,result)
            failure=None; recovery=None
            if det.diverged:
                detected += 1
                failure=self.diagnoser.diagnose(physical_step,proposal,result,det,steps)
                rplan=self.controller.select(failure,env,proposal)
                # Simulator-only diagnostic: execute forked counterfactuals for analysis,
                # never for online policy selection. Real adapters may omit this entirely.
                offline_cfs=self.controller.empirical_counterfactuals(failure,env,proposal)
                if offline_cfs:
                    rplan.counterfactuals=offline_cfs
                recovery=self._execute_recovery(rplan,env,cps,store,proposal)
                physical_step += recovery.steps_used
                if recovery.succeeded:
                    recovered += 1; store.update_from_observation(env.observe())
                elif failure.risk_if_ignored==RiskLevel.HIGH:
                    aborted=True
            else:
                # verified state is a useful rollback point at subgoal transitions
                if proposal.subgoal and (not steps or steps[-1].proposal.subgoal != proposal.subgoal):
                    cp=cps.create(physical_step,env,store.snapshot()); store.state.last_verified_checkpoint=cp.id
            steps.append(TrajectoryStep(physical_step,proposal,result,det,failure,recovery))
            if aborted: break
        return RunRecord(_run_id(self.name,task.task_id,seed),task.task_id,self.name,seed,(env.grade() and not aborted),steps,env.observe(),injected,detected,recovered,false_alarms,0,aborted)

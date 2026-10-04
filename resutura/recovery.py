from __future__ import annotations
from copy import deepcopy
from .schemas import RecoveryCandidate, RecoveryLevel, RecoveryPlan, Action, FailureEvent


class EffectSemanticRecoveryController:
    """Counterfactual, utility-aware recovery that favors the smallest state intervention.

    The simulator uses transparent heuristic estimates. Real CUA adapters can replace
    `counterfactual_score` with a learned/world-model transition estimator without
    changing the recovery contract.
    """
    def __init__(self, cost_weight=.10, latency_weight=.07, risk_weight=.22,
                 progress_weight=.30, collateral_weight=.28):
        self.cost_weight=cost_weight; self.latency_weight=latency_weight
        self.risk_weight=risk_weight; self.progress_weight=progress_weight
        self.collateral_weight=collateral_weight

    def causal_slice(self, f: FailureEvent, proposal) -> list[str]:
        if f.failure_subtype in {"MISDIRECTED_EXTERNAL_EFFECT","IRREVERSIBLE_MISDIRECTED_EFFECT","AMBIGUOUS_COMMIT"}:
            return ["effect_ledger:last", "publications:agent_owned", "publication_counts", "publications:intended"]
        if f.failure_subtype == "FOCUS_LOSS":
            return ["app_state.focus"]
        if f.failure_subtype == "MISSING_OR_STALE_TAB":
            tab=proposal.action.args.get("required_tab") or proposal.action.target or "active"
            return [f"tabs.{tab}", "app_state.active_tab"]
        if f.transient:
            return ["executor.transient_status"]
        if f.failure_type.value == "state_tracking":
            return ["app_state", "assumptions"]
        return ["active_subgoal"]

    def utility(self,c:RecoveryCandidate)->float:
        return (c.estimated_success
                - self.cost_weight*c.estimated_cost
                - self.latency_weight*c.estimated_latency
                - self.risk_weight*c.estimated_risk
                - self.progress_weight*c.estimated_progress_loss
                - self.collateral_weight*c.estimated_collateral)

    def candidates(self,f:FailureEvent,env,proposal)->list[RecoveryCandidate]:
        causal=self.causal_slice(f,proposal); out=[]
        if f.failure_subtype == "AMBIGUOUS_COMMIT":
            operation_id=proposal.action.args.get("operation_id")
            status=env.query_effect_status(operation_id) if operation_id and hasattr(env,"query_effect_status") else None
            if status is not None:
                if status.get("committed"):
                    out.append(RecoveryCandidate(RecoveryLevel.CONTINUE,"Authoritative readback confirms commit; do not replay",.999,.05,.05,.01,.00,.00,causal))
                else:
                    out.append(RecoveryCandidate(RecoveryLevel.RETRY,"Authoritative readback confirms no commit; replay original operation",.97,1,1,.05,.00,.01,causal))
                return out
            contract=getattr(env,"effect_contract",None)
            if contract is not None and getattr(contract,"idempotency",False):
                out.append(RecoveryCandidate(RecoveryLevel.RETRY,"Commit status is unobservable, but the declared idempotency contract makes same-operation replay safe",.96,1,1,.05,.00,.01,causal))
                return out
            out.append(RecoveryCandidate(RecoveryLevel.SAFE_ABORT,"Commit status cannot be observed and replay is not declared idempotent; stop rather than risk a duplicate effect",1.0,.1,.1,.01,.00,.00,causal))
            return out
        if f.failure_subtype == "IRREVERSIBLE_MISDIRECTED_EFFECT":
            return [RecoveryCandidate(RecoveryLevel.SAFE_ABORT,"Stop automation and escalate because the committed effect has no safe compensator",1.0,.1,.1,.01,.00,.00,causal)]
        if f.transient:
            out.append(RecoveryCandidate(RecoveryLevel.RETRY,"Replay only the failed operation",.88,1,1,.05,.00,.02,causal))
        if f.scope=="action":
            out.append(RecoveryCandidate(RecoveryLevel.LOCAL_REPAIR,"Repair only the violated local precondition",.84,1.4,1.1,.04,.00,.02,causal))
        if f.scope in {"action","subgoal"}:
            out.append(RecoveryCandidate(RecoveryLevel.SUBGOAL_REPAIR,"Reconstruct the minimum state slice required by the active subgoal",.91,2.2,1.8,.06,.06,.05,causal))
        if f.scope == "external_effect" or f.failure_subtype == "MISDIRECTED_EXTERNAL_EFFECT":
            out.append(RecoveryCandidate(RecoveryLevel.COMPENSATE,"Reconcile committed external effect with a forward compensating action, then apply intended effect",.97,2.5,2.0,.08,.00,.01,causal))
        if env.supports_rollback and f.risk_if_ignored.value in {"moderate","high"}:
            out.append(RecoveryCandidate(RecoveryLevel.ROLLBACK,"Restore a verified checkpoint",.94,4,3,.04,.35,.08,["checkpoint:*" ]))
        out.append(RecoveryCandidate(RecoveryLevel.GLOBAL_REPLAN,"Discard remaining local plan and regenerate globally",.87,6,5,.11,.55,.14,["plan:*","state:*" ]))
        return out

    def counterfactual_score(self,c:RecoveryCandidate)->dict:
        return {"level":c.level.value,"predicted_success":round(c.estimated_success,3),
                "progress_loss":round(c.estimated_progress_loss,3),"collateral":round(c.estimated_collateral,3),
                "utility":round(self.utility(c),4),"affected_state":c.affected_state}

    @staticmethod
    def _predicate_ok(pred, obs):
        cur=obs
        try:
            for part in pred.key.split("."):
                cur=cur[part]
        except (KeyError, TypeError):
            return False
        if pred.op == "eq": return cur == pred.value
        if pred.op == "gte": return cur >= pred.value
        if pred.op == "truthy": return bool(cur)
        if pred.op == "contains": return pred.value in cur
        if pred.op == "exists": return cur is not None
        return False

    def empirical_counterfactuals(self, f, env, proposal):
        """Fork the *actual failed state* and execute every feasible repair.

        This is exact in forkable deterministic environments. Real GUI adapters may
        implement the same contract with VM snapshots/replay; otherwise this method
        is unavailable and selection falls back to calibrated estimates.
        """
        if not hasattr(env, "export_state") or not hasattr(env, "import_state"):
            return []
        failed_state=env.export_state(); rows=[]
        for c in self.candidates(f, env, proposal):
            try:
                fork=deepcopy(env); fork.import_state(deepcopy(failed_state))
                actions, expected=self._materialize(c.level,f,fork,proposal)
                if c.level == RecoveryLevel.ROLLBACK:
                    # A checkpoint is external to env; cannot be replayed here without the manager.
                    rows.append({**self.counterfactual_score(c),"empirical":False,"used_for_policy_selection":False,"reason":"checkpoint_context_required"})
                    continue
                for a in actions: fork.execute(a)
                obs=fork.observe()
                ok=all(self._predicate_ok(p,obs) for p in (expected or proposal.expected_postconditions))
                rows.append({**self.counterfactual_score(c),"empirical":True,"used_for_policy_selection":False,"observed_success":bool(ok)})
            except Exception as e:
                rows.append({**self.counterfactual_score(c),"empirical":False,"used_for_policy_selection":False,"reason":type(e).__name__})
        return rows

    def select(self,f:FailureEvent,env,proposal)->RecoveryPlan:
        candidates=self.candidates(f,env,proposal)
        best=max(candidates,key=self.utility)
        if best.level == RecoveryLevel.SAFE_ABORT:
            return RecoveryPlan(best.level,best.description,[],[],self.utility(best),
                                causal_slice=self.causal_slice(f,proposal),
                                counterfactuals=[self.counterfactual_score(best)])
        actions,predicates=self._materialize(best.level,f,env,proposal)
        # IMPORTANT: online policy selection must not use forked-state counterfactual outcomes.
        # Those are oracle-like in a simulator and are retained only for offline analysis.
        return RecoveryPlan(best.level,best.description,actions,predicates,self.utility(best),
                            causal_slice=self.causal_slice(f,proposal),
                            counterfactuals=[self.counterfactual_score(c) for c in candidates])

    def _materialize(self,level,f,env,proposal):
        if level==RecoveryLevel.CONTINUE:
            return [],proposal.expected_postconditions
        if level==RecoveryLevel.RETRY:
            return [proposal.action],proposal.expected_postconditions
        if level==RecoveryLevel.LOCAL_REPAIR:
            if f.failure_subtype=="FOCUS_LOSS":
                return [Action("restore_focus"),proposal.action],proposal.expected_postconditions
            return [Action("refresh_state"),proposal.action],proposal.expected_postconditions
        if level==RecoveryLevel.SUBGOAL_REPAIR:
            if f.failure_subtype=="MISSING_OR_STALE_TAB":
                tab=proposal.action.args.get("required_tab") or proposal.action.target or "spreadsheet"
                return [Action("open_tab",target=tab),proposal.action],proposal.expected_postconditions
            return [Action("refresh_state"),proposal.action],proposal.expected_postconditions
        if level==RecoveryLevel.COMPENSATE:
            intended=proposal.action.target
            obs=env.observe()
            ledger=obs.get("effect_ledger",[])
            wrong=next((x.get("actual_target") for x in reversed(ledger)
                        if x.get("kind")=="publish" and x.get("actor","agent")=="agent"
                        and x.get("actual_target") != intended and not x.get("compensated",False)
                        and x.get("compensatable",True)), None)
            acts=[]
            if wrong: acts.append(Action("retract_publication",wrong))
            acts.append(Action("publish",intended))
            return acts,proposal.expected_postconditions
        if level==RecoveryLevel.ROLLBACK:
            return [Action("rollback")],[]
        if level==RecoveryLevel.GLOBAL_REPLAN:
            return [Action("replan")],[]
        return [],[]

# Public controller name used by the runtime.
RecoveryController=EffectSemanticRecoveryController

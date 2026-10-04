from __future__ import annotations
import hashlib, json
from .schemas import FailureEvent, FailureType, RiskLevel, DetectionResult, ActionProposal, ActionResult


class FailureDiagnoser:
    """Conservative rule-based localizer; replaceable by a model-backed implementation."""
    def diagnose(self, step: int, proposal: ActionProposal, result: ActionResult, detection: DetectionResult, history) -> FailureEvent:
        keys = {m.get("key", "") for m in detection.mismatches}
        msg = (result.message or "").lower()
        action = proposal.action.type
        required_tab = proposal.action.args.get("required_tab")
        observed_tabs = result.observation.get("tabs", {})
        intended = proposal.action.target if action == "publish" else None
        pubs = result.observation.get("publications", {})
        ledger = result.observation.get("effect_ledger", [])
        last_agent_effect = next((x for x in reversed(ledger) if x.get("kind")=="publish" and x.get("actor","agent")=="agent"), None)
        if action == "publish" and not result.ok and "timeout" in msg:
            ft, subtype, scope, rec = FailureType.VERIFICATION, "AMBIGUOUS_COMMIT", "external_effect", "VERIFY_CONTINUE"
        elif action == "publish" and any(k.startswith("publications.") for k in keys):
            if last_agent_effect and not last_agent_effect.get("compensatable", True):
                ft, subtype, scope, rec = FailureType.SAFETY, "IRREVERSIBLE_MISDIRECTED_EFFECT", "external_effect", "SAFE_ABORT"
            else:
                ft, subtype, scope, rec = FailureType.SAFETY, "MISDIRECTED_EXTERNAL_EFFECT", "external_effect", "COMPENSATE"
        elif result.transient or "temporary" in msg or "timeout" in msg:
            ft, subtype, scope, rec = FailureType.ENVIRONMENT, "TRANSIENT_EXECUTION", "action", "RETRY"
        elif (required_tab and (not observed_tabs.get(required_tab, False) or result.observation.get("app_state", {}).get("active_tab") != required_tab)) or any("active_tab" in k or "tabs" in k for k in keys):
            ft, subtype, scope, rec = FailureType.STATE_TRACKING, "MISSING_OR_STALE_TAB", "subgoal", "SUBGOAL"
        elif "focus" in msg:
            ft, subtype, scope, rec = FailureType.PERCEPTION, "FOCUS_LOSS", "action", "LOCAL"
        elif action in {"type_cell", "type_text"} and not result.ok:
            ft, subtype, scope, rec = FailureType.ACTION, "INVALID_TARGET", "action", "LOCAL"
        elif "prerequisite" in msg:
            ft, subtype, scope, rec = FailureType.PLANNING, "MISSING_PREREQUISITE", "subgoal", "SUBGOAL"
        else:
            ft, subtype, scope, rec = FailureType.UNKNOWN, "POSTCONDITION_MISMATCH", "subgoal", "SUBGOAL"

        root = step
        # Look backward for the most recent failed action when it plausibly caused the mismatch.
        for prev in reversed(history[-4:]):
            if not prev.result.ok:
                root = prev.step
                break
        risk = RiskLevel.HIGH if proposal.risk == RiskLevel.HIGH or subtype in {"MISDIRECTED_EXTERNAL_EFFECT","IRREVERSIBLE_MISDIRECTED_EFFECT","AMBIGUOUS_COMMIT"} else RiskLevel.MODERATE
        return FailureEvent(
            failure_id="f_" + hashlib.sha256(json.dumps({"step":step,"type":ft.value,"subtype":subtype,"expected":{m["key"]:m["expected"] for m in detection.mismatches},"observed":{m["key"]:m["actual"] for m in detection.mismatches}},sort_keys=True,default=str).encode()).hexdigest()[:8], step=step, failure_type=ft,
            failure_subtype=subtype, trigger="EXPECTED_STATE_MISMATCH",
            expected={m["key"]: m["expected"] for m in detection.mismatches},
            observed={m["key"]: m["actual"] for m in detection.mismatches},
            suspected_root_step=root, causal_chain=list(range(root, step+1)),
            confidence=max(0.55, detection.confidence), recoverability=rec,
            risk_if_ignored=risk, transient=result.transient, scope=scope,
        )

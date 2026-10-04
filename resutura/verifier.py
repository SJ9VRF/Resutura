from .schemas import ActionProposal, ActionResult, DetectionResult, Predicate
from .state import evaluate_predicate


class StateDeltaVerifier:
    """Checks explicit postconditions. It is deliberately deterministic in the core."""
    def verify(self, proposal: ActionProposal, result: ActionResult) -> DetectionResult:
        mismatches = []
        total_weight = 0.0
        failed_weight = 0.0
        for p in proposal.expected_postconditions:
            ok, actual = evaluate_predicate(result.observation, p)
            w = max(0.05, p.confidence) * (2.0 if p.critical else 1.0)
            total_weight += w
            if not ok:
                failed_weight += w
                mismatches.append({
                    "key": p.key, "op": p.op, "expected": p.value,
                    "actual": actual, "critical": p.critical,
                })
        diverged = bool(mismatches)
        confidence = failed_weight / total_weight if total_weight else (0.9 if not result.ok else 0.0)
        if not result.ok and not diverged:
            diverged = True
            confidence = max(confidence, 0.9)
            mismatches.append({"key": "action_result.ok", "expected": True, "actual": False, "critical": True})
        return DetectionResult(diverged=diverged, mismatches=mismatches, confidence=confidence)

    def verify_predicates(self, predicates: list[Predicate], observation: dict) -> bool:
        return all(evaluate_predicate(observation, p)[0] for p in predicates)

from __future__ import annotations
from copy import deepcopy
from typing import Any
from .schemas import AgentState, Predicate, Action, ActionResult


def get_path(obj: dict[str, Any], path: str) -> Any:
    cur: Any = obj
    parts = path.split('.')
    for i, part in enumerate(parts):
        if not isinstance(cur, dict):
            return None
        remaining = ".".join(parts[i:])
        if remaining in cur:
            return cur[remaining]
        if part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def evaluate_predicate(observation: dict[str, Any], p: Predicate) -> tuple[bool, Any]:
    actual = get_path(observation, p.key)
    if p.op == "eq": ok = actual == p.value
    elif p.op == "neq": ok = actual != p.value
    elif p.op == "exists": ok = actual is not None
    elif p.op == "contains": ok = p.value in (actual or []) or (isinstance(actual, str) and str(p.value) in actual)
    elif p.op == "gte": ok = actual is not None and actual >= p.value
    elif p.op == "truthy": ok = bool(actual)
    else: raise ValueError(f"Unsupported predicate op: {p.op}")
    return ok, actual


class StateStore:
    def __init__(self, initial: AgentState):
        self.state = deepcopy(initial)

    def update_from_observation(self, obs: dict[str, Any]) -> AgentState:
        self.state.app_state = deepcopy(obs.get("app_state", {}))
        self.state.tabs = deepcopy(obs.get("tabs", {}))
        self.state.files = deepcopy(obs.get("files", {}))
        self.state.gathered_facts.update(deepcopy(obs.get("facts", {})))
        return self.state

    def record_action(self, action: Action, result: ActionResult):
        self.state.action_history.append({
            "action": {"type": action.type, "target": action.target, "value": action.value, "args": action.args},
            "ok": result.ok,
            "message": result.message,
        })

    def snapshot(self) -> AgentState:
        return deepcopy(self.state)

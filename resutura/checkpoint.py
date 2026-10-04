from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

@dataclass
class Checkpoint:
    id: str
    step: int
    env_state: dict[str, Any]
    agent_state: Any


class CheckpointManager:
    def __init__(self):
        self._items: list[Checkpoint] = []

    def create(self, step: int, env, agent_state) -> Checkpoint:
        cp = Checkpoint(f"cp_{step}_{len(self._items)}", step, deepcopy(env.export_state()), deepcopy(agent_state))
        self._items.append(cp)
        return cp

    def latest(self) -> Checkpoint | None:
        return self._items[-1] if self._items else None

    def restore_latest(self, env):
        cp = self.latest()
        if cp is None: return None
        if hasattr(env, "restore_checkpoint_state"):
            env.restore_checkpoint_state(deepcopy(cp.env_state))
        else:
            env.import_state(deepcopy(cp.env_state))
        return deepcopy(cp.agent_state)

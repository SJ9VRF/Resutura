from __future__ import annotations
from dataclasses import dataclass
import random

@dataclass
class Perturbation:
    type: str
    trigger_step: int
    consumed: bool = False


class PerturbationEngine:
    def __init__(self, perturbations=None, seed=0):
        self.perturbations = list(perturbations or [])
        self.rng = random.Random(seed)
        self.injected = 0

    def before_action(self, env, step: int, action):
        events=[]
        for p in self.perturbations:
            if not p.consumed and p.trigger_step == step:
                p.consumed=True
                self.injected += 1
                events.append(p.type)
                env.apply_perturbation(p.type)
        return events


def standard_perturbation(seed: int, trigger_step: int = 4) -> Perturbation:
    types = ["close_spreadsheet_tab", "transient_failure", "lose_focus", "switch_active_tab"]
    return Perturbation(random.Random(seed).choice(types), trigger_step)

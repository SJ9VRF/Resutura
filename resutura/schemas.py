from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any
import time


class RiskLevel(str, Enum):
    SAFE = "safe"
    MODERATE = "moderate"
    HIGH = "high"


class FailureType(str, Enum):
    PERCEPTION = "perception"
    STATE_TRACKING = "state_tracking"
    PLANNING = "planning"
    ACTION = "action"
    MEMORY = "memory"
    VERIFICATION = "verification"
    RECOVERY = "recovery"
    SAFETY = "safety"
    ENVIRONMENT = "environment"
    UNKNOWN = "unknown"


class RecoveryLevel(str, Enum):
    CONTINUE = "R0_continue"
    RETRY = "R1_retry"
    LOCAL_REPAIR = "R2_local_repair"
    SUBGOAL_REPAIR = "R3_subgoal_repair"
    COMPENSATE = "R4_forward_compensation"
    ROLLBACK = "R5_rollback"
    GLOBAL_REPLAN = "R6_global_replan"
    SAFE_ABORT = "R7_safe_abort"


@dataclass(frozen=True)
class EffectContract:
    """Capabilities exposed by an external-effect tool.

    readback: the runtime can authoritatively query whether an operation committed.
    idempotency: replaying the same operation_id cannot duplicate the effect.
    compensation: committed effects expose a supported compensating operation.
    """
    readback: bool = True
    idempotency: bool = False
    compensation: bool = True


@dataclass
class Predicate:
    key: str
    op: str
    value: Any
    confidence: float = 1.0
    critical: bool = True


@dataclass
class Assumption:
    claim: str
    source: str
    confidence: float
    verified: bool = False
    created_at_step: int = 0


@dataclass
class AgentState:
    task_goal: str
    completed_subgoals: list[str] = field(default_factory=list)
    active_subgoal: str | None = None
    pending_subgoals: list[str] = field(default_factory=list)
    app_state: dict[str, Any] = field(default_factory=dict)
    known_entities: dict[str, Any] = field(default_factory=dict)
    files: dict[str, Any] = field(default_factory=dict)
    tabs: dict[str, Any] = field(default_factory=dict)
    gathered_facts: dict[str, Any] = field(default_factory=dict)
    commitments: list[str] = field(default_factory=list)
    irreversible_actions: list[str] = field(default_factory=list)
    assumptions: list[Assumption] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    last_verified_checkpoint: str | None = None
    action_history: list[dict[str, Any]] = field(default_factory=list)
    recovery_history: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Action:
    type: str
    target: str | None = None
    value: Any = None
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionProposal:
    action: Action
    intent: str
    expected_postconditions: list[Predicate]
    risk: RiskLevel = RiskLevel.SAFE
    reversibility: str = "full"
    subgoal: str | None = None


@dataclass
class ActionResult:
    ok: bool
    observation: dict[str, Any]
    message: str = ""
    side_effects: list[str] = field(default_factory=list)
    transient: bool = False


@dataclass
class DetectionResult:
    diverged: bool
    mismatches: list[dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    false_alarm_risk: float = 0.0


@dataclass
class FailureEvent:
    failure_id: str
    step: int
    failure_type: FailureType
    failure_subtype: str
    trigger: str
    expected: dict[str, Any]
    observed: dict[str, Any]
    suspected_root_step: int
    causal_chain: list[int]
    confidence: float
    recoverability: str
    risk_if_ignored: RiskLevel
    transient: bool = False
    scope: str = "action"


@dataclass
class RecoveryCandidate:
    level: RecoveryLevel
    description: str
    estimated_success: float
    estimated_cost: float
    estimated_latency: float
    estimated_risk: float
    estimated_progress_loss: float = 0.0
    estimated_collateral: float = 0.0
    affected_state: list[str] = field(default_factory=list)


@dataclass
class RecoveryPlan:
    level: RecoveryLevel
    description: str
    actions: list[Action]
    expected_state: list[Predicate]
    utility: float
    causal_slice: list[str] = field(default_factory=list)
    counterfactuals: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RecoveryResult:
    attempted: bool
    succeeded: bool
    level: RecoveryLevel
    steps_used: int
    made_state_worse: bool = False
    message: str = ""
    preserved_progress_ratio: float = 1.0
    repair_certificate: dict[str, Any] = field(default_factory=dict)


@dataclass
class TrajectoryStep:
    step: int
    proposal: ActionProposal
    result: ActionResult
    detection: DetectionResult
    failure: FailureEvent | None = None
    recovery: RecoveryResult | None = None
    timestamp: float = 0.0


@dataclass
class RunRecord:
    run_id: str
    task_id: str
    agent: str
    seed: int
    success: bool
    steps: list[TrajectoryStep]
    final_observation: dict[str, Any]
    injected_failures: int = 0
    detected_failures: int = 0
    recovered_failures: int = 0
    false_failure_detections: int = 0
    restart_count: int = 0
    aborted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        def conv(x):
            if isinstance(x, Enum):
                return x.value
            if hasattr(x, '__dataclass_fields__'):
                return {k: conv(v) for k, v in asdict(x).items()}
            if isinstance(x, dict):
                return {k: conv(v) for k, v in x.items()}
            if isinstance(x, list):
                return [conv(v) for v in x]
            return x
        return conv(self)

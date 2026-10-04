from resutura.agent import BaseAgent, RetryAgent, RewindAgent, ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine


def publish_step(task):
    # Four actions per paper + open/write/save/save + publish.
    return 4 * len(task.papers) + 5


def run(agent_cls):
    task = make_task(77, 3)
    pe = PerturbationEngine([Perturbation("redirect_publish_target", publish_step(task))])
    return agent_cls().run(ResearchWorkflowEnv(), task, pe, seed=77)


def test_external_effect_requires_compensation_not_rewind():
    base = run(BaseAgent)
    retry = run(RetryAgent)
    rewind = run(RewindAgent)
    repaired = run(ResuturaAgent)
    assert not base.success
    assert not retry.success
    assert not rewind.success
    assert repaired.success
    assert set(repaired.final_observation["publications"]) == {"research-team"}
    assert "wrong-channel" not in repaired.final_observation["publications"]


def test_compensation_is_auditable_and_verified():
    repaired = run(ResuturaAgent)
    step = next(s for s in repaired.steps if s.failure and s.failure.failure_subtype == "MISDIRECTED_EXTERNAL_EFFECT")
    assert step.recovery is not None and step.recovery.succeeded
    assert step.recovery.level.value == "R4_forward_compensation"
    ledger = repaired.final_observation["effect_ledger"]
    assert any(x.get("kind") == "publish" and x.get("actual_target") == "wrong-channel" and x.get("compensated") for x in ledger)
    assert any(x.get("kind") == "compensate_retract" and x.get("target") == "wrong-channel" for x in ledger)
    assert any(x.get("kind") == "publish" and x.get("actual_target") == "research-team" for x in ledger)
    cert=step.recovery.repair_certificate
    assert cert["postconditions_verified"] is True
    assert cert["protected_invariants_verified"] is True
    assert cert["external_effect_reconciled"] is True
    assert cert["recovery_semantics"] == "forward_compensation"

from resutura.agent import BaseAgent, RetryAgent, RewindAgent, ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine


def publish_step(task):
    return 4 * len(task.papers) + 5


def run(agent_cls, kinds):
    task = make_task(909, 3)
    step = publish_step(task)
    pe = PerturbationEngine([Perturbation(k, step) for k in kinds], seed=1)
    return agent_cls().run(ResearchWorkflowEnv(), task, pe, seed=1)


def test_ambiguous_commit_verify_before_retry_avoids_duplicate():
    base = run(BaseAgent, ["ambiguous_publish_timeout"])
    retry = run(RetryAgent, ["ambiguous_publish_timeout"])
    rewind = run(RewindAgent, ["ambiguous_publish_timeout"])
    resutura = run(ResuturaAgent, ["ambiguous_publish_timeout"])
    assert base.success  # lucky: it does not retry after the lost response
    assert not retry.success and retry.final_observation["publication_counts"]["research-team"] == 2
    assert not rewind.success and rewind.final_observation["publication_counts"]["research-team"] == 2
    assert resutura.success and resutura.final_observation["publication_counts"]["research-team"] == 1
    step = next(s for s in resutura.steps if s.failure and s.failure.failure_subtype == "AMBIGUOUS_COMMIT")
    assert step.recovery.level.value == "R0_continue"
    assert step.recovery.repair_certificate["external_effect_reconciled"] is True


def test_compensation_preserves_concurrent_valid_external_change():
    resutura = run(ResuturaAgent, ["concurrent_valid_publication", "redirect_publish_target"])
    assert resutura.success
    assert resutura.final_observation["publications"]["coordinator-note"] == "valid concurrent update"
    assert resutura.final_observation["publications"]["research-team"]
    assert "wrong-channel" not in resutura.final_observation["publications"]
    step = next(s for s in resutura.steps if s.failure and s.failure.failure_subtype == "MISDIRECTED_EXTERNAL_EFFECT")
    assert step.recovery.repair_certificate["protected_invariants_verified"] is True


def test_noncompensatable_effect_causes_safe_abort_not_fake_recovery():
    resutura = run(ResuturaAgent, ["redirect_publish_noncompensatable"])
    assert not resutura.success
    assert resutura.aborted
    step = next(s for s in resutura.steps if s.failure and s.failure.failure_subtype == "IRREVERSIBLE_MISDIRECTED_EFFECT")
    assert step.recovery.level.value == "R7_safe_abort"
    assert step.recovery.repair_certificate["safe_abort"] is True
    assert step.recovery.repair_certificate["external_effect_reconciled"] is False

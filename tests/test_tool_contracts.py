from resutura.agent import RetryAgent, ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.schemas import EffectContract
from resutura.perturbations import Perturbation, PerturbationEngine


def publish_step(task):
    return 4 * len(task.papers) + 5


def run(agent_cls, contract):
    task=make_task(1201,3)
    pe=PerturbationEngine([Perturbation("ambiguous_publish_unobservable", publish_step(task))], seed=0)
    return agent_cls().run(ResearchWorkflowEnv(effect_contract=contract), task, pe, seed=0)


def recovery_step(record):
    return next(s for s in record.steps if s.failure and s.failure.failure_subtype=="AMBIGUOUS_COMMIT")


def test_readback_resolves_unobservable_ambiguous_commit_without_replay():
    r=run(ResuturaAgent, EffectContract(readback=True,idempotency=False,compensation=True))
    assert r.success and not r.aborted
    assert r.final_observation["publication_counts"]["research-team"] == 1
    assert recovery_step(r).recovery.level.value == "R0_continue"


def test_idempotency_contract_allows_safe_replay_when_readback_missing():
    r=run(ResuturaAgent, EffectContract(readback=False,idempotency=True,compensation=True))
    assert r.success and not r.aborted
    assert r.final_observation["publication_counts"]["research-team"] == 1
    assert recovery_step(r).recovery.level.value == "R1_retry"


def test_missing_readback_and_idempotency_forces_safe_abort():
    r=run(ResuturaAgent, EffectContract(readback=False,idempotency=False,compensation=True))
    assert not r.success and r.aborted
    assert r.final_observation["publication_counts"]["research-team"] == 1  # commit happened, but caller cannot know safely
    assert recovery_step(r).recovery.level.value == "R7_safe_abort"


def test_blind_retry_duplicates_without_idempotency_contract():
    r=run(RetryAgent, EffectContract(readback=False,idempotency=False,compensation=True))
    assert not r.success
    assert r.final_observation["publication_counts"]["research-team"] == 2


def test_blind_retry_is_deduplicated_by_idempotent_tool_contract():
    r=run(RetryAgent, EffectContract(readback=False,idempotency=True,compensation=True))
    assert r.success
    assert r.final_observation["publication_counts"]["research-team"] == 1


def test_rewind_respects_server_side_idempotency_registry():
    from resutura.agent import RewindAgent
    r=run(RewindAgent, EffectContract(readback=False,idempotency=True,compensation=True))
    assert r.success
    assert r.final_observation["publication_counts"]["research-team"] == 1

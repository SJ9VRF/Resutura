from experiments.ablation_suite import FullResutura, NoCompensationResutura, NoContractAwarenessResutura, NoOwnershipResutura, publish_step
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine


def run(agent_cls, kinds):
    task=make_task(901,3); step=publish_step(task)
    pe=PerturbationEngine([Perturbation(k,step) for k in kinds],seed=1)
    return agent_cls().run(ResearchWorkflowEnv(),task,pe,seed=1)


def test_compensation_ablation_breaks_misdirection_recovery():
    assert run(FullResutura,['redirect_publish_target']).success
    r=run(NoCompensationResutura,['redirect_publish_target'])
    assert not r.success


def test_contract_awareness_ablation_duplicates_ambiguous_commit():
    assert run(FullResutura,['ambiguous_publish_timeout']).success
    r=run(NoContractAwarenessResutura,['ambiguous_publish_timeout'])
    assert not r.success
    assert r.final_observation['publication_counts']['research-team'] == 2


def test_ownership_ablation_breaks_concurrent_reconciliation():
    assert run(FullResutura,['concurrent_valid_publication','redirect_publish_target']).success
    r=run(NoOwnershipResutura,['concurrent_valid_publication','redirect_publish_target'])
    assert not r.success
    assert 'coordinator-note' in r.final_observation['publications']

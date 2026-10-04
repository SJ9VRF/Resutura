from resutura.agent import VerificationAwareAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.schemas import EffectContract
from resutura.perturbations import Perturbation, PerturbationEngine


def pstep(t): return 4*len(t.papers)+5

def test_verification_baseline_solves_ambiguous_commit_with_readback():
    t=make_task(88,3)
    r=VerificationAwareAgent().run(ResearchWorkflowEnv(EffectContract(readback=True,idempotency=False)),t,PerturbationEngine([Perturbation("ambiguous_publish_unobservable",pstep(t))]))
    assert r.success and r.final_observation["publication_counts"]["research-team"]==1

def test_verification_baseline_does_not_solve_misdirected_effect():
    t=make_task(89,3)
    r=VerificationAwareAgent().run(ResearchWorkflowEnv(),t,PerturbationEngine([Perturbation("redirect_publish_target",pstep(t))]))
    assert not r.success
    assert "wrong-channel" in r.final_observation["publications"]

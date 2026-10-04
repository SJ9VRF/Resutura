from resutura.agent import ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine

def _one():
    task=make_task(909,3)
    step=4*len(task.papers)+5
    pe=PerturbationEngine([Perturbation("redirect_publish_target",step)],seed=9)
    return ResuturaAgent().run(ResearchWorkflowEnv(),task,pe,seed=9).to_dict()

def test_same_seed_is_byte_semantically_reproducible():
    assert _one() == _one()

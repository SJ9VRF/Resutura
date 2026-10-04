from resutura.agent import ResuturaAgent, BaseAgent, RetryAgent
from resutura.envs.sandbox import ResearchWorkflowEnv, make_task
from resutura.perturbations import PerturbationEngine, Perturbation

def test_resutura_recovers_closed_tab():
    run=ResuturaAgent().run(ResearchWorkflowEnv(),make_task(1),PerturbationEngine([Perturbation("close_spreadsheet_tab",4)]))
    assert run.success
    assert run.recovered_failures >= 1

def test_base_fails_closed_tab():
    run=BaseAgent().run(ResearchWorkflowEnv(),make_task(1),PerturbationEngine([Perturbation("close_spreadsheet_tab",4)]))
    assert not run.success

def test_retry_recovers_transient_but_not_missing_tab():
    t=make_task(1)
    r1=RetryAgent().run(ResearchWorkflowEnv(),t,PerturbationEngine([Perturbation("transient_failure",4)]))
    assert r1.success
    r2=RetryAgent().run(ResearchWorkflowEnv(),t,PerturbationEngine([Perturbation("close_spreadsheet_tab",4)]))
    assert not r2.success

def test_offline_counterfactual_exists_predicate_is_supported():
    from resutura.recovery import EffectSemanticRecoveryController
    from resutura.schemas import Predicate
    assert EffectSemanticRecoveryController._predicate_ok(Predicate('publications.research-team','exists',True), {'publications':{'research-team':'doc'}})
    assert not EffectSemanticRecoveryController._predicate_ok(Predicate('publications.research-team','exists',True), {'publications':{}})

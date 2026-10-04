from resutura.agent import ResuturaAgent
from resutura.envs import ResearchWorkflowEnv, make_task
from resutura.perturbations import PerturbationEngine, Perturbation


def test_repair_certificate_is_local_and_progress_preserving():
    run=ResuturaAgent().run(ResearchWorkflowEnv(), make_task(9),
                            PerturbationEngine([Perturbation("close_spreadsheet_tab",4)]))
    repairs=[s.recovery for s in run.steps if s.recovery]
    assert repairs and repairs[0].succeeded
    cert=repairs[0].repair_certificate
    assert "causal_slice" in cert and cert["causal_slice"]
    assert "counterfactuals" in cert and len(cert["counterfactuals"]) >= 2
    assert repairs[0].preserved_progress_ratio >= .99


def test_counterfactuals_are_executed_not_only_self_estimated():
    run=ResuturaAgent().run(ResearchWorkflowEnv(), make_task(10),
                            PerturbationEngine([Perturbation("close_spreadsheet_tab",4)]))
    repair=next(s.recovery for s in run.steps if s.recovery)
    cfs=repair.repair_certificate["counterfactuals"]
    assert any(c.get("empirical") is True for c in cfs)
    assert any("observed_success" in c for c in cfs if c.get("empirical"))
    assert repair.level.value == "R3_subgoal_repair"

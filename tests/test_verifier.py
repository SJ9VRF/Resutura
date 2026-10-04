from resutura.verifier import StateDeltaVerifier
from resutura.schemas import *

def test_verifier_detects_postcondition_failure():
    p=ActionProposal(Action("x"),"x",[Predicate("app_state.active_tab","eq","spreadsheet")])
    r=ActionResult(True,{"app_state":{"active_tab":"browser"}})
    d=StateDeltaVerifier().verify(p,r)
    assert d.diverged and d.mismatches

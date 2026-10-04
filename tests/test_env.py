from resutura.envs.sandbox import ResearchWorkflowEnv, make_task
from resutura.schemas import Action

def test_env_roundtrip():
    e=ResearchWorkflowEnv(); e.reset(make_task(1))
    s=e.export_state(); e.execute(Action("close_tab","spreadsheet")); assert not e.tabs["spreadsheet"]
    e.import_state(s); assert e.tabs["spreadsheet"]

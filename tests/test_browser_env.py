import shutil
import pytest
pytest.importorskip("playwright.sync_api")
if not shutil.which("chromium"):
    pytest.skip("Chromium not available; browser microbench is optional", allow_module_level=True)
from resutura.envs.browser import BrowserResearchWorkflowEnv
from resutura.envs.sandbox import make_task
from resutura.schemas import Action

def test_browser_env_dom_roundtrip():
    e=BrowserResearchWorkflowEnv()
    try:
        e.reset(make_task(3)); assert e.observe()["app_state"]["active_tab"]=="browser"
        assert e.execute(Action("switch_tab","spreadsheet")).ok
        assert e.observe()["app_state"]["active_tab"]=="spreadsheet"
        s=e.export_state(); e.execute(Action("close_tab","spreadsheet")); assert not e.observe()["tabs"]["spreadsheet"]
        e.import_state(s); assert e.observe()["tabs"]["spreadsheet"]
    finally:e.close()

def test_browser_grade_preserves_concurrent_valid_external_change():
    e=BrowserResearchWorkflowEnv()
    try:
        t=make_task(9); e.reset(t)
        # Complete deterministic task actions directly.
        from resutura.planner import WorkflowPlanner
        for p in WorkflowPlanner().build_plan(t)[:-1]: assert e.execute(p.action).ok
        e.apply_perturbation('concurrent_valid_publication')
        assert e.execute(WorkflowPlanner().build_plan(t)[-1].action).ok
        assert e.grade()
        assert 'coordinator-note' in e.publications
    finally:e.close()

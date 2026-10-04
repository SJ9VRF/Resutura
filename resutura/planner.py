from __future__ import annotations
from .schemas import Action, ActionProposal, Predicate, RiskLevel

class WorkflowPlanner:
    """Deterministic task planner used to isolate recovery behavior in the included study."""
    def build_plan(self, task):
        plan=[]
        for i,p in enumerate(task.papers):
            plan += [
                ActionProposal(Action("switch_tab", "browser"), f"open browser for paper {i}", [Predicate("app_state.active_tab","eq","browser")], subgoal=f"research_{i}"),
                ActionProposal(Action("research_next", args={"index":i,"required_tab":"browser"}), f"collect paper {i}", [Predicate("app_state.browser_index","gte",i+1)], subgoal=f"research_{i}"),
                ActionProposal(Action("switch_tab", "spreadsheet"), f"open sheet for paper {i}", [Predicate("app_state.active_tab","eq","spreadsheet")], subgoal=f"record_{i}"),
                ActionProposal(Action("type_cell", value=p, args={"required_tab":"spreadsheet"}), f"record paper {i}", [Predicate("app_state.sheet_rows","gte",i+1)], subgoal=f"record_{i}"),
            ]
        text = "\n".join(f"{p['title']}: {p['finding']}" for p in task.papers)
        plan += [
            ActionProposal(Action("switch_tab","document"), "open comparison document", [Predicate("app_state.active_tab","eq","document")], subgoal="write"),
            ActionProposal(Action("write_document", value=text, args={"required_tab":"document"}), "write comparison", [Predicate("app_state.document_nonempty","eq",True)], subgoal="write"),
            ActionProposal(Action("save_file","sheet.csv"), "save spreadsheet", [Predicate("files.sheet.csv","exists",True)], risk=RiskLevel.MODERATE, subgoal="save"),
            ActionProposal(Action("save_file","comparison.doc"), "save document", [Predicate("files.comparison.doc","exists",True)], risk=RiskLevel.MODERATE, subgoal="save"),
            ActionProposal(Action("publish", task.publish_target, args={"operation_id": f"{task.task_id}:publish:{task.publish_target}"}), "publish comparison to intended target", [Predicate(f"publications.{task.publish_target}","exists",True)], risk=RiskLevel.HIGH, reversibility="compensatable", subgoal="publish"),
        ]
        return plan

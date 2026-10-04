from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from typing import Any
from ..schemas import Action, ActionResult, EffectContract

@dataclass
class Task:
    task_id: str
    papers: list[dict[str,str]]
    summary_title: str = "Comparison"
    publish_target: str = "research-team"


def make_task(i: int = 0, n_papers: int = 3) -> Task:
    papers=[]
    for j in range(n_papers):
        papers.append({"title": f"Paper-{i}-{j}", "year": str(2020+j), "finding": f"Finding {i}.{j}"})
    return Task(f"task_{i:04d}", papers)


class ResearchWorkflowEnv:
    """Small but stateful browser→spreadsheet→document research environment."""
    supports_rollback=True

    def __init__(self, effect_contract: EffectContract | None = None):
        self.task=None
        self.effect_contract = effect_contract or EffectContract()
        self._transient_next=False
        self.reset(make_task())

    def reset(self, task: Task):
        self.task=task
        self.tabs={"browser": True, "spreadsheet": True, "document": True}
        self.active_tab="browser"
        self.focus=True
        self.sheet=[]
        self.document=""
        self.files={}
        self.browser_index=0
        self.facts={}
        self._transient_next=False
        self.publications={}
        self.publication_counts={}
        self.protected_external_targets=[]
        self.effect_ledger=[]
        self._redirect_publish_target=None
        self._redirect_publish_compensatable=True
        self._ambiguous_publish_timeout=False
        self._hide_publish_commit_from_result=False
        self._operation_status={}
        return self.observe()

    def observe(self) -> dict[str, Any]:
        return {
            "app_state": {
                "active_tab": self.active_tab,
                "focus": self.focus,
                "sheet_rows": len(self.sheet),
                "document_nonempty": bool(self.document),
                "browser_index": self.browser_index,
            },
            "tabs": deepcopy(self.tabs),
            "files": deepcopy(self.files),
            "facts": deepcopy(self.facts),
            "sheet": deepcopy(self.sheet),
            "document": self.document,
            "publications": deepcopy(self.publications),
            "publication_counts": deepcopy(self.publication_counts),
            "protected_external_targets": list(self.protected_external_targets),
            "effect_ledger": deepcopy(self.effect_ledger),
        }

    def execute(self, a: Action) -> ActionResult:
        if self._transient_next and a.type not in {"refresh_state", "rollback", "replan"}:
            self._transient_next=False
            return ActionResult(False, self.observe(), "temporary execution failure", transient=True)
        if a.type == "open_tab":
            t=a.target or "browser"; self.tabs[t]=True; self.active_tab=t; self.focus=True
            return ActionResult(True,self.observe(),f"opened {t}")
        if a.type == "switch_tab":
            if not self.tabs.get(a.target or "", False): return ActionResult(False,self.observe(),"target tab missing")
            self.active_tab=a.target; return ActionResult(True,self.observe(),"switched")
        if a.type == "research_next":
            if self.active_tab!="browser" or not self.tabs.get("browser"):
                return ActionResult(False,self.observe(),"browser prerequisite missing")
            idx=int(a.args["index"]); p=self.task.papers[idx]; self.facts[p["title"]]=deepcopy(p); self.browser_index=idx+1
            return ActionResult(True,self.observe(),"fact collected")
        if a.type == "type_cell":
            if self.active_tab!="spreadsheet" or not self.tabs.get("spreadsheet"):
                return ActionResult(False,self.observe(),"spreadsheet prerequisite missing")
            if not self.focus: return ActionResult(False,self.observe(),"focus lost")
            row=deepcopy(a.value)
            # idempotent row insertion by title
            if not any(r.get("title")==row.get("title") for r in self.sheet): self.sheet.append(row)
            return ActionResult(True,self.observe(),"row entered")
        if a.type == "write_document":
            if self.active_tab!="document" or not self.tabs.get("document"):
                return ActionResult(False,self.observe(),"document prerequisite missing")
            if not self.focus: return ActionResult(False,self.observe(),"focus lost")
            self.document=str(a.value)
            return ActionResult(True,self.observe(),"document written")
        if a.type == "save_file":
            name=a.target or "output"; content = self.document if "doc" in name else deepcopy(self.sheet)
            self.files[name]=content
            return ActionResult(True,self.observe(),"saved")
        if a.type == "publish":
            requested=a.target or self.task.publish_target
            operation_id=a.args.get("operation_id") or f"anon:{requested}:{len(self.effect_ledger)}"
            # A declared idempotency contract makes replay of the *same operation id* safe.
            if self.effect_contract.idempotency and operation_id in self._operation_status:
                prior=self._operation_status[operation_id]
                return ActionResult(True,self.observe(),f"idempotent replay suppressed; prior commit at {prior['actual_target']}",side_effects=[])
            actual=self._redirect_publish_target or requested
            compensatable=self._redirect_publish_compensatable and self.effect_contract.compensation
            self._redirect_publish_target=None
            self._redirect_publish_compensatable=True
            self.publications[actual]=self.document
            self.publication_counts[actual]=self.publication_counts.get(actual,0)+1
            event={"kind":"publish","actor":"agent","operation_id":operation_id,"requested_target":requested,"actual_target":actual,"committed":True,"compensated":False,"compensatable":compensatable}
            self.effect_ledger.append(event)
            self._operation_status[operation_id]=deepcopy(event)
            if self._ambiguous_publish_timeout:
                self._ambiguous_publish_timeout=False
                obs=self.observe()
                if self._hide_publish_commit_from_result:
                    self._hide_publish_commit_from_result=False
                    obs=deepcopy(obs)
                    obs["publications"].pop(actual,None)
                    if actual in obs["publication_counts"]:
                        obs["publication_counts"][actual]=max(0,obs["publication_counts"][actual]-1)
                        if obs["publication_counts"][actual]==0: obs["publication_counts"].pop(actual,None)
                    obs["effect_ledger"]=[x for x in obs["effect_ledger"] if x.get("operation_id") != operation_id]
                return ActionResult(False,obs,"timeout after dispatch; commit status unknown to caller",side_effects=[])
            return ActionResult(True,self.observe(),f"published to {actual}",side_effects=[f"publish:{actual}"])
        if a.type == "retract_publication":
            target=a.target or ""
            if target in self.protected_external_targets:
                return ActionResult(False,self.observe(),f"refused to retract protected external target {target}")
            candidate=None
            for item in reversed(self.effect_ledger):
                if item.get("kind")=="publish" and item.get("actor")=="agent" and item.get("actual_target")==target and not item.get("compensated"):
                    candidate=item; break
            if candidate is not None and not candidate.get("compensatable",True):
                return ActionResult(False,self.observe(),f"effect at {target} is not compensatable")
            existed=target in self.publications
            self.publications.pop(target,None)
            for item in reversed(self.effect_ledger):
                if item.get("kind")=="publish" and item.get("actor")=="agent" and item.get("actual_target")==target and not item.get("compensated"):
                    item["compensated"]=True; break
            self.effect_ledger.append({"kind":"compensate_retract","actor":"agent","target":target,"committed":True,"effective":existed})
            return ActionResult(True,self.observe(),f"retracted {target}",side_effects=[f"retract:{target}"])
        if a.type == "restore_focus":
            self.focus=True; return ActionResult(True,self.observe(),"focus restored")
        if a.type == "refresh_state":
            self.focus=True; return ActionResult(True,self.observe(),"state refreshed")
        if a.type == "close_tab":
            self.tabs[a.target]=False
            if self.active_tab==a.target: self.active_tab="browser" if self.tabs.get("browser") else next((k for k,v in self.tabs.items() if v), "none")
            return ActionResult(True,self.observe(),"tab closed")
        if a.type in {"rollback","replan"}:
            return ActionResult(True,self.observe(),a.type)
        return ActionResult(False,self.observe(),f"unsupported action {a.type}")

    def apply_perturbation(self, kind: str):
        if kind=="close_spreadsheet_tab":
            self.tabs["spreadsheet"]=False
            if self.active_tab=="spreadsheet": self.active_tab="browser"
        elif kind=="transient_failure": self._transient_next=True
        elif kind=="lose_focus": self.focus=False
        elif kind=="switch_active_tab": self.active_tab="browser"
        elif kind=="redirect_publish_target":
            self._redirect_publish_target="wrong-channel"; self._redirect_publish_compensatable=True
        elif kind=="redirect_publish_noncompensatable":
            self._redirect_publish_target="irreversible-wrong-channel"; self._redirect_publish_compensatable=False
        elif kind=="ambiguous_publish_timeout": self._ambiguous_publish_timeout=True
        elif kind=="ambiguous_publish_unobservable":
            self._ambiguous_publish_timeout=True
            self._hide_publish_commit_from_result=True
        elif kind=="concurrent_valid_publication":
            target="coordinator-note"
            self.publications[target]="valid concurrent update"
            self.publication_counts[target]=self.publication_counts.get(target,0)+1
            if target not in self.protected_external_targets: self.protected_external_targets.append(target)
            self.effect_ledger.append({"kind":"publish","actor":"external","actual_target":target,"committed":True,"protected":True})
        elif kind=="corrupt_sheet" and self.sheet: self.sheet.pop()
        else: raise ValueError(kind)

    def query_effect_status(self, operation_id: str):
        """Authoritative readback exposed only when the tool contract declares it."""
        if not self.effect_contract.readback:
            return None
        item=self._operation_status.get(operation_id)
        if item is None:
            return {"committed": False, "operation_id": operation_id}
        return {"committed": True, "operation_id": operation_id, "actual_target": item.get("actual_target"), "compensated": item.get("compensated",False)}

    def export_state(self):
        return deepcopy({"tabs":self.tabs,"active_tab":self.active_tab,"focus":self.focus,"sheet":self.sheet,"document":self.document,"files":self.files,"browser_index":self.browser_index,"facts":self.facts,"transient":self._transient_next,"publications":self.publications,"publication_counts":self.publication_counts,"protected_external_targets":self.protected_external_targets,"effect_ledger":self.effect_ledger,"redirect_publish_target":self._redirect_publish_target,"redirect_publish_compensatable":self._redirect_publish_compensatable,"ambiguous_publish_timeout":self._ambiguous_publish_timeout,"hide_publish_commit_from_result":self._hide_publish_commit_from_result,"operation_status":self._operation_status})

    def import_state(self, s):
        self.tabs=deepcopy(s["tabs"]); self.active_tab=s["active_tab"]; self.focus=s["focus"]; self.sheet=deepcopy(s["sheet"]); self.document=s["document"]; self.files=deepcopy(s["files"]); self.browser_index=s["browser_index"]; self.facts=deepcopy(s["facts"]); self._transient_next=s.get("transient",False); self.publications=deepcopy(s.get("publications",{})); self.publication_counts=deepcopy(s.get("publication_counts",{})); self.protected_external_targets=list(s.get("protected_external_targets",[])); self.effect_ledger=deepcopy(s.get("effect_ledger",[])); self._redirect_publish_target=s.get("redirect_publish_target"); self._redirect_publish_compensatable=s.get("redirect_publish_compensatable",True); self._ambiguous_publish_timeout=s.get("ambiguous_publish_timeout",False); self._hide_publish_commit_from_result=s.get("hide_publish_commit_from_result",False); self._operation_status=deepcopy(s.get("operation_status",{}))


    def restore_checkpoint_state(self, s):
        """Restore reversible local state while preserving already-committed external effects."""
        external_publications=deepcopy(self.publications)
        external_counts=deepcopy(self.publication_counts)
        external_protected=list(self.protected_external_targets)
        external_ledger=deepcopy(self.effect_ledger)
        external_operation_status=deepcopy(self._operation_status)
        self.import_state(s)
        self.publications=external_publications
        self.publication_counts=external_counts
        self.protected_external_targets=external_protected
        self.effect_ledger=external_ledger
        # Server-side deduplication state is part of the external world, not the local checkpoint.
        self._operation_status=external_operation_status

    def grade(self) -> bool:
        if len(self.sheet)!=len(self.task.papers): return False
        expected_titles={p["title"] for p in self.task.papers}
        if {r.get("title") for r in self.sheet} != expected_titles: return False
        if not self.document or not all(p["title"] in self.document for p in self.task.papers): return False
        if not ("sheet.csv" in self.files and "comparison.doc" in self.files): return False
        if not self.publications.get(self.task.publish_target): return False
        if self.publication_counts.get(self.task.publish_target,0) != 1: return False
        for item in self.effect_ledger:
            if item.get("kind")=="publish" and item.get("actor")=="agent" and item.get("actual_target") != self.task.publish_target and not item.get("compensated",False):
                return False
        return all(t in self.publications for t in self.protected_external_targets)

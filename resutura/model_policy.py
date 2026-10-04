from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Protocol, Any
import json, subprocess
from .schemas import Action, ActionProposal, Predicate, RiskLevel, EffectContract

ALLOWED_ACTIONS = {
    'open_tab','switch_tab','research_next','type_cell','write_document','save_file',
    'publish','retract_publication','restore_focus','refresh_state','close_tab','rollback','replan'
}

@dataclass
class PolicyRequest:
    task: dict[str, Any]
    observation: dict[str, Any]
    effect_contract: dict[str, bool]
    history: list[dict[str, Any]]
    step: int
    allowed_actions: list[str]

    def to_dict(self): return asdict(self)

@dataclass
class PolicyResponse:
    proposal: ActionProposal | None
    stop: bool = False
    rationale: str = ''
    raw: dict[str, Any] | None = None

class PolicyProvider(Protocol):
    def next(self, request: PolicyRequest) -> PolicyResponse: ...


def proposal_from_dict(d: dict[str, Any]) -> ActionProposal:
    a=d.get('action') or {}
    typ=str(a.get('type',''))
    if typ not in ALLOWED_ACTIONS: raise ValueError(f'unsupported policy action: {typ!r}')
    action=Action(typ,a.get('target'),a.get('value'),dict(a.get('args') or {}))
    preds=[Predicate(str(p['key']),str(p.get('op','eq')),p.get('value'),float(p.get('confidence',1.0)),bool(p.get('critical',True))) for p in d.get('expected_postconditions',[])]
    risk=RiskLevel(str(d.get('risk','safe')))
    return ActionProposal(action,str(d.get('intent','policy action')),preds,risk,str(d.get('reversibility','full')),d.get('subgoal'))

class RecordedPolicyProvider:
    """Deterministic replay provider for auditing model/policy traces.

    This is deliberately not called a model. It replays previously recorded decisions so
    recovery behavior can be reproduced without network/API access.
    """
    def __init__(self, records: list[dict[str, Any]]):
        self.records=list(records); self.i=0
    @classmethod
    def from_json(cls,path:str):
        obj=json.load(open(path))
        return cls(obj['responses'] if isinstance(obj,dict) else obj)
    def next(self, request:PolicyRequest)->PolicyResponse:
        if self.i>=len(self.records): return PolicyResponse(None,stop=True,rationale='replay exhausted')
        r=self.records[self.i]; self.i+=1
        if r.get('stop'): return PolicyResponse(None,True,str(r.get('rationale','stop')),r)
        return PolicyResponse(proposal_from_dict(r['proposal']),False,str(r.get('rationale','')),r)

class CommandPolicyProvider:
    """Provider-neutral bridge: send one JSON request to an external command on stdin.

    The command must return one JSON object on stdout with either {"stop":true} or
    {"proposal": {...}}. This keeps model credentials/SDKs outside the research core.
    """
    def __init__(self, command:list[str], timeout_s:float=60.0):
        self.command=list(command); self.timeout_s=timeout_s
    def next(self, request:PolicyRequest)->PolicyResponse:
        cp=subprocess.run(self.command,input=json.dumps(request.to_dict()),text=True,capture_output=True,timeout=self.timeout_s,check=False)
        if cp.returncode!=0: raise RuntimeError(f'policy command failed rc={cp.returncode}: {cp.stderr[-1000:]}')
        try:r=json.loads(cp.stdout)
        except json.JSONDecodeError as e: raise RuntimeError('policy command did not return valid JSON') from e
        if r.get('stop'): return PolicyResponse(None,True,str(r.get('rationale','')),r)
        if 'proposal' not in r: raise RuntimeError('policy response missing proposal')
        return PolicyResponse(proposal_from_dict(r['proposal']),False,str(r.get('rationale','')),r)


def effect_contract_dict(env)->dict[str,bool]:
    c=getattr(env,'effect_contract',EffectContract())
    return {'readback':bool(c.readback),'idempotency':bool(c.idempotency),'compensation':bool(c.compensation)}

import json,sys
from resutura.model_policy import proposal_from_dict, RecordedPolicyProvider, CommandPolicyProvider, PolicyRequest
from resutura.schemas import RiskLevel

def test_proposal_schema_rejects_unknown_action():
    try: proposal_from_dict({'action':{'type':'shell_exec'}})
    except ValueError: pass
    else: raise AssertionError('unknown action accepted')

def test_recorded_provider_is_deterministic(tmp_path):
    rec={'responses':[{'proposal':{'action':{'type':'refresh_state'},'intent':'refresh','expected_postconditions':[]}} , {'stop':True}]}
    p=tmp_path/'r.json'; p.write_text(json.dumps(rec))
    req=PolicyRequest({}, {}, {'readback':True,'idempotency':False,'compensation':True}, [], 1, ['refresh_state'])
    a=RecordedPolicyProvider.from_json(str(p)); b=RecordedPolicyProvider.from_json(str(p))
    assert a.next(req).proposal.action.type == b.next(req).proposal.action.type == 'refresh_state'
    assert a.next(req).stop and b.next(req).stop

def test_command_provider_roundtrip(tmp_path):
    script=tmp_path/'policy.py'
    script.write_text('import sys,json\n_ = json.load(sys.stdin)\nprint(json.dumps({"proposal":{"action":{"type":"refresh_state"},"intent":"r","expected_postconditions":[]}}))\n')
    req=PolicyRequest({}, {}, {'readback':True,'idempotency':False,'compensation':True}, [], 1, ['refresh_state'])
    out=CommandPolicyProvider([sys.executable,str(script)]).next(req)
    assert out.proposal.action.type=='refresh_state'

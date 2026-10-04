from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]

def sha(rel):
    p=ROOT/rel
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'MISSING'
claims=[
 ('C1','Committed wrong-target effects are reconciled in the bundled mechanism studies.',['runs/effect_semantics_suite.json.gz','runs/browser_effect_semantics.json']),
 ('C2','Verification-Aware matches Resutura on ambiguous commits when authoritative readback is sufficient.',['runs/tool_contract_matrix.json.gz','runs/browser_effect_semantics.json']),
 ('C3','Effect ownership is necessary for the bundled concurrent-valid-change diagnostic.',['runs/ablation_suite.json.gz','artifacts/generated/ABLATION_RESULTS.md']),
 ('C4','Non-compensatable committed effects are safe-aborted rather than reported as successful recovery.',['runs/effect_semantics_suite.json.gz','artifacts/generated/EFFECT_SEMANTICS_RESULTS.md']),
 ('C5','The public dataset contains 160 diagnostic items and 800 raw trajectories.',['artifacts/dataset/manifest.json','artifacts/dataset/schema.json']),
 ('C6','The provider boundary is replay-tested but is explicitly not frontier-model evidence.',['runs/policy_replay_smoke.json','artifacts/generated/POLICY_REPLAY_RESULTS.md']),
]
lines=['# Claim → Evidence Map','',
'> Use this file to keep homepage, paper, resume, and interview claims tied to inspectable artifacts. Hashes are for the current release tree.','']
for cid,text,paths in claims:
    lines += [f'## {cid}', '', text, '']
    for p in paths: lines.append(f'- `{p}` — SHA-256 `{sha(p)}`')
    lines.append('')
lines += ['## Claims this release does **not** support','',
'- State of the art / SOTA.','- Frontier-model superiority.','- OSWorld superiority.','- Production safety.','- General exactly-once guarantees.','- Security against malicious tools or prompt injection.','']
(ROOT/'docs'/'CLAIM_EVIDENCE_MAP.md').write_text('\n'.join(lines))
print('wrote docs/CLAIM_EVIDENCE_MAP.md')
if __name__=='__main__': pass

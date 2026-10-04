from __future__ import annotations
import hashlib, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAP=ROOT/'docs'/'CLAIM_EVIDENCE_MAP.md'
pat=re.compile(r'- `([^`]+)` — SHA-256 `([0-9a-f]{64}|MISSING)`')
errors=[]; seen=0
for rel, expected in pat.findall(MAP.read_text()):
    seen+=1; p=ROOT/rel
    if not p.exists(): actual='MISSING'
    else: actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual != expected: errors.append((rel,expected,actual))
if seen == 0:
    raise SystemExit('no claim-evidence hashes found')
if errors:
    for rel,e,a in errors[:10]: print(f'MISMATCH {rel}: expected {e}, actual {a}')
    raise SystemExit(1)
print(f'claim evidence: PASS ({seen} hashed pointers)')

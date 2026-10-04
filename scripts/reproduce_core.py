from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
CMDS=[
 [sys.executable,'experiments/effect_semantics_suite.py'],
 [sys.executable,'experiments/tool_contract_matrix.py'],
 [sys.executable,'experiments/ablation_suite.py'],
 [sys.executable,'analysis/ablation_report.py'],
 [sys.executable,'scripts/export_dataset.py'],
 [sys.executable,'analysis/statistical_report.py'],
]
for c in CMDS:
    print('+',' '.join(c),flush=True); subprocess.run(c,cwd=ROOT,check=True)
print('core evidence reproduction: PASS')

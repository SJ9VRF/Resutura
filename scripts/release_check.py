import subprocess, sys
checks=[
    [sys.executable,"-m","pytest","-q"],
    [sys.executable,"-m","resutura.cli","experiment","--trials","40","--seed","7","--out","runs/release_check.json"],
    [sys.executable,"experiments/external_effect_recovery.py"],
    [sys.executable,"experiments/effect_semantics_suite.py"],
    [sys.executable,"experiments/tool_contract_matrix.py"],
    [sys.executable,"experiments/ablation_suite.py"],
    [sys.executable,"scripts/export_dataset.py"],
    [sys.executable,"analysis/statistical_report.py"],
]
for c in checks:
    print("+", " ".join(c)); subprocess.run(c,check=True)
print("release checks passed")

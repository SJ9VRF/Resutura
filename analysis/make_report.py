import json
from pathlib import Path

def pct(x): return f"{100*x:.1f}%"
obj=json.loads(Path("runs/pilot.json").read_text())
rows=[]
for name,d in obj["agents"].items():
    s=d["summary"]; rows.append(f"| {name} | {pct(s['success_rate'])} | {pct(s['recovery_rate_per_injected'])} | {s['mean_recovery_steps']:.2f} |")
text=f"""# Resutura deterministic pilot\n\n> **Scope:** local deterministic simulator only. These are measured values, not browser/frontier-model claims.\n\n| Agent | Task success | Recovery / injected failure | Mean recovery steps |\n|---|---:|---:|---:|\n{chr(10).join(rows)}\n\nTrials per agent: {obj['trials_per_agent']}. Seed: {obj['seed']}.\n"""
Path("artifacts/generated").mkdir(parents=True,exist_ok=True)
Path("artifacts/generated/PILOT_RESULTS.md").write_text(text)
print(text)

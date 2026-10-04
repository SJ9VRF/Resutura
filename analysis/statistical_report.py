from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def pct(x):return f'{100*x:.1f}%'
def ci(x):return f'[{100*x[0]:.1f}, {100*x[1]:.1f}]%'

def main():
    import gzip
    with gzip.open(ROOT/'runs/effect_semantics_suite.json.gz','rt',encoding='utf-8') as f:
        effect=json.load(f)
    lines=['# Statistical / uncertainty report','',
           '> **Interpretation boundary.** The simulator is deterministic and trials vary generated task instances/seeds. Wilson intervals below are descriptive binomial intervals over this diagnostic suite; they are **not** uncertainty estimates for frontier-model behavior or deployment performance.','',
           '## Effect Semantics Suite','',
           '| Scenario | Method | n | Success | Wilson 95% | Unreconciled effect | Duplicate intended effect | Safe abort |','|---|---|---:|---:|---:|---:|---:|---:|']
    for scenario,methods in effect['scenarios'].items():
        for method,p in methods.items():
            s=p['summary']; lines.append(f"| {scenario} | {method} | {s['n']} | {pct(s['success_rate'])} | {ci(s['success_ci95'])} | {pct(s['unreconciled_external_effect_rate'])} | {pct(s['duplicate_intended_effect_rate'])} | {pct(s['safe_abort_rate'])} |")
    lines += ['','## Paired-seed contrasts against the strongest relevant baseline','',
              'Because the suite is deterministic, paired contrasts are reported as **coverage over matched task/fault seeds**, not p-values.','',
              '| Scenario | Contrast | Paired seeds where Resutura is strictly better | Ties | Worse |','|---|---|---:|---:|---:|']
    refs={'compensable_misdirection':'verify','ambiguous_commit':'verify','concurrent_change_plus_misdirection':'verify','noncompensatable_misdirection':'verify'}
    for scenario,ref in refs.items():
        rr=effect['scenarios'][scenario]['resutura']['runs']; br=effect['scenarios'][scenario][ref]['runs']
        better=tie=worse=0
        for a,b in zip(rr,br):
            # For non-compensatable effects, safe abort is the intended safe outcome; grade success is not the objective.
            if scenario=='noncompensatable_misdirection':
                av=int(a.get('aborted',False)); bv=int(b.get('aborted',False))
            else:
                av=int(a['success']); bv=int(b['success'])
            better+=av>bv; tie+=av==bv; worse+=av<bv
        lines.append(f'| {scenario} | Resutura vs {ref} | {better}/{len(rr)} | {tie}/{len(rr)} | {worse}/{len(rr)} |')
    lines += ['','## Chromium note','',
              'The bundled Chromium mechanism-transfer study uses only **2 paired trials per method/scenario**. That sample is deliberately treated as a transfer smoke test; no strong statistical claim or SOTA inference is made from it.','']
    (ROOT/'artifacts/generated/STATISTICAL_REPORT.md').write_text('\n'.join(lines))
    print('wrote artifacts/generated/STATISTICAL_REPORT.md')
if __name__=='__main__':main()

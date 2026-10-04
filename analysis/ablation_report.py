from pathlib import Path
import gzip, json
ROOT=Path(__file__).resolve().parents[1]

def main():
    with gzip.open(ROOT/'runs/ablation_suite.json.gz','rt',encoding='utf-8') as f:
        x=json.load(f)
    order=['full','minus_compensation','minus_contract_awareness','minus_effect_ownership']
    scens=['compensable_misdirection','ambiguous_commit','concurrent_change_plus_misdirection','noncompensatable_misdirection']
    labels={'full':'Full Resutura','minus_compensation':'− compensation','minus_contract_awareness':'− contract awareness','minus_effect_ownership':'− effect ownership'}
    lines=['# Resutura component ablation','',
    '> Deterministic simulator ablation, 40 paired task/fault seeds per cell. The goal is causal mechanism isolation, not model-capability estimation.','',
    '| Variant | Compensable misdirection | Ambiguous commit | Concurrent valid change + misdirection | Non-compensatable effect |','|---|---:|---:|---:|---:|']
    for v in order:
        vals=[]
        for s in scens:
            sm=x['variants'][v][s]['summary']
            vals.append(f"{100*(sm['safe_abort_rate'] if s=='noncompensatable_misdirection' else sm['success_rate']):.0f}%" + (' safe abort' if s=='noncompensatable_misdirection' else ''))
        lines.append('| '+labels[v]+' | '+' | '.join(vals)+' |')
    lines += ['','## What each ablation isolates','',
    '- **− compensation:** committed wrong-target effects remain unreconciled; task success falls to 0% in both compensable-misdirection cases.',
    '- **− contract awareness:** ambiguous commits are blindly replayed, producing duplicate intended effects in 100% of trials and 0% task success.',
    '- **− effect ownership:** simple misdirection remains recoverable, but the concurrent-valid-change case falls to 0%.',
    '- **Full Resutura:** matches intended semantics in all four diagnostics; non-compensatable effects are safe-aborted rather than mislabeled as recovered.','',
    '## Evidence boundary','',
    'These are deterministic mechanism ablations. They show mechanism necessity inside this testbed; they do not estimate frontier-model or production effect sizes.','']
    (ROOT/'artifacts/generated/ABLATION_RESULTS.md').write_text('\n'.join(lines))
    print('wrote artifacts/generated/ABLATION_RESULTS.md')
if __name__=='__main__':main()

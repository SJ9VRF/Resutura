# Resutura component ablation

> Deterministic simulator ablation, 40 paired task/fault seeds per cell. The goal is causal mechanism isolation, not model-capability estimation.

| Variant | Compensable misdirection | Ambiguous commit | Concurrent valid change + misdirection | Non-compensatable effect |
|---|---:|---:|---:|---:|
| Full Resutura | 100% | 100% | 100% | 100% safe abort |
| − compensation | 0% | 100% | 0% | 100% safe abort |
| − contract awareness | 100% | 0% | 100% | 100% safe abort |
| − effect ownership | 100% | 100% | 0% | 100% safe abort |

## What each ablation isolates

- **− compensation:** committed wrong-target effects remain unreconciled; task success falls to 0% in both compensable-misdirection cases.
- **− contract awareness:** ambiguous commits are blindly replayed, producing duplicate intended effects in 100% of trials and 0% task success.
- **− effect ownership:** simple misdirection remains recoverable, but the concurrent-valid-change case falls to 0%.
- **Full Resutura:** matches intended semantics in all four diagnostics; non-compensatable effects are safe-aborted rather than mislabeled as recovered.

## Evidence boundary

These are deterministic mechanism ablations. They show mechanism necessity inside this testbed; they do not estimate frontier-model or production effect sizes.

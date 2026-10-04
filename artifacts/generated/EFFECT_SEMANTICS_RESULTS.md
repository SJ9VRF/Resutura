# Effect Semantics Suite - deterministic mechanism results

**Aura Yavary - September 2026**

This is a deterministic semantics study. It is not a real-browser, frontier-model, or SOTA benchmark.

| Scenario | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| Compensable misdirection | 0% | 0% | 0% | 0% | 100% |
| Ambiguous commit | 100% | 0% | 100% | 0% | 100% |
| Concurrent valid change + misdirection | 0% | 0% | 0% | 0% | 100% |
| Non-compensatable misdirection | 0% | 0% | 0% | 0% | 0% / 100% safe abort |

## Interpretation

- Verification-Aware matches Resutura on ambiguous commit under authoritative readback. That behavior is prior art and is not claimed as novel.
- Resutura differs on compensable misdirection and concurrent ownership because it performs effect reconciliation rather than only verification.
- Non-compensatable misdirection remains a negative result: Resutura safe-aborts instead of relabeling an impossible repair as success.
- The suite reports ground-truth task state; Base can appear successful on ambiguous commit because it simply does not retry.

## Methodological safeguard

Forked-state counterfactual replay is diagnostic only. Observed fork outcomes are logged with `used_for_policy_selection=false` and are not consumed by the online selector.

**Evidence boundary:** simulator mechanism validation only.

## Provenance

- Source fingerprint (SHA-256): `f7481f916fd23b26955c73879a984a38a91aec281ae28901a02ff9751f8f3459`
- Raw trajectories: `runs/effect_semantics_suite.json.gz`
- Seed policy: seed=i within each method/scenario; paired identical task+fault seeds across methods
- Same-code/same-seed signature runs are byte-reproducible; see `docs/EXPERIMENT_REGISTRY.md`.

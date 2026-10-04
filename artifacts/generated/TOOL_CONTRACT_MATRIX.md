# Tool Contract Matrix

Deterministic mechanism study. 40 trials per method per contract; ambiguous commit is hidden from the failed call result.

| Contract | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| Readback only | 100% | 0% / 100% dup | 100% | 0% / 100% dup | 100% |
| Idempotency only | 100% | 100% | 100% | 100% | 100% |
| Readback + idempotency | 100% | 100% | 100% | 100% | 100% |
| Neither | 100% | 0% / 100% dup | 0% / 100% abort | 0% / 100% dup | 0% / 100% abort |

## Interpretation

- Readback is sufficient for Verification-Aware and Resutura to avoid replay after an ambiguous commit.
- Idempotency is sufficient for Retry, Verification-Aware, Rewind, and Resutura to avoid duplicate effects.
- With neither capability, Verification-Aware and Resutura safe-abort instead of blind replay; Base happens to leave the world correct because it does nothing after the lost acknowledgement, but does not know the commit succeeded.
- Checkpoint restore preserves the server-side idempotency registry; rewinding it would be an invalid simulator artifact.
- Forked-state counterfactual outcomes are not used by the online selector.

**Evidence boundary:** deterministic sandbox only; not a real-browser or model benchmark.

## Provenance

- Source fingerprint (SHA-256): `f7481f916fd23b26955c73879a984a38a91aec281ae28901a02ff9751f8f3459`
- Raw trajectories: `runs/tool_contract_matrix.json.gz`
- Seed policy: seed=0..n-1 paired across methods/contracts
- Same-code/same-seed signature runs are byte-reproducible; see `docs/EXPERIMENT_REGISTRY.md`.

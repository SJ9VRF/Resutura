# Real Eval Tables

Only bundled, executed studies are shown. No placeholder X% values appear here. Simulator repetitions are deterministic mechanism trials, not independent samples from a model distribution.

## Effect Semantics Suite — 40 paired trials per method/scenario

| Scenario | Base | Retry | Verify | Rewind | Resutura | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Compensable misdirection | 0% | 0% | 0% | 0% | **100%** | Requires effect reconciliation/compensation in this testbed |
| Ambiguous commit | **100%*** | 0% | **100%** | 0% | **100%** | Verify-before-retry is sufficient with authoritative readback |
| Concurrent valid change + misdirection | 0% | 0% | 0% | 0% | **100%** | Requires ownership-aware reconciliation |
| Non-compensatable misdirection | 0% | 0% | 0% | 0% | **0% success / 100% safe abort** | Repair is intentionally refused |

`*` Base leaves the world correct by doing nothing after the lost acknowledgement; it does not know the commit succeeded.

For a 40/40 deterministic cell, the bundled statistical report gives a Wilson 95% interval of approximately **91.2%–100%**. This interval is descriptive repetition accounting, **not frontier-model uncertainty**.

## Tool Contract Matrix — 40 trials per method/contract

| Contract | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| Readback only | 100% | 0% / 100% duplicate | 100% | 0% / 100% duplicate | 100% |
| Idempotency only | 100% | 100% | 100% | 100% | 100% |
| Readback + idempotency | 100% | 100% | 100% | 100% | 100% |
| Neither | 100% | 0% / 100% duplicate | 0% / 100% abort | 0% / 100% duplicate | 0% / 100% abort |

## Component ablation — 40 paired trials per cell

| Variant | Misdirection | Ambiguous commit | Concurrent valid state | Non-compensatable |
|---|---:|---:|---:|---:|
| Full Resutura | 100% | 100% | 100% | 100% safe abort |
| − compensation | 0% | 100% | 0% | 100% safe abort |
| − contract awareness | 100% | 0% | 100% | 100% safe abort |
| − effect ownership | 100% | 100% | 0% | 100% safe abort |

## Chromium mechanism-transfer tier — 2 paired trials per method/scenario

| Scenario | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| ambiguous_commit | 100% | 0% | 100% | 0% | 100% |
| concurrent_change_plus_misdirection | 0% | 0% | 0% | 0% | 100% |
| misdirected_commit | 0% | 0% | 0% | 0% | 100% |
| noncompensatable_commit | 0% | 0% | 0% | 0% | 0% / 100% safe abort |

**Cost / latency boundary:** bundled deterministic studies record action overhead, but no provider-model token cost or model latency exists because no frontier model is called. The homepage therefore marks model-provider cost/latency as not measured rather than inventing values.

### Raw evidence
- `runs/effect_semantics_suite.json.gz`
- `runs/tool_contract_matrix.json.gz`
- `runs/ablation_suite.json.gz`
- `runs/browser_effect_semantics.json`
- `artifacts/generated/STATISTICAL_REPORT.md`

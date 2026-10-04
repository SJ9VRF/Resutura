# Chromium Effect-Semantics Results

**Evidence tier:** real Chromium DOM + deterministic planner; not model-backed.

Trials per method/scenario: 2

| Scenario | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| ambiguous_commit | 100% | 0% | 100% | 0% | 100% |
| concurrent_change_plus_misdirection | 0% | 0% | 0% | 0% | 100% |
| misdirected_commit | 0% | 0% | 0% | 0% | 100% |
| noncompensatable_commit | 0% | 0% | 0% | 0% | 0% / 100% safe-abort |

Every run receives fresh perturbation objects; stateful fault objects are never shared across methods.

Real Chromium mechanism-transfer study with deterministic planner. Not model-backed, not OSWorld, not SOTA evidence.

# Statistical / uncertainty report

> **Interpretation boundary.** The simulator is deterministic and trials vary generated task instances/seeds. Wilson intervals below are descriptive binomial intervals over this diagnostic suite; they are **not** uncertainty estimates for frontier-model behavior or deployment performance.

## Effect Semantics Suite

| Scenario | Method | n | Success | Wilson 95% | Unreconciled effect | Duplicate intended effect | Safe abort |
|---|---|---:|---:|---:|---:|---:|---:|
| ambiguous_commit | base | 40 | 100.0% | [91.2, 100.0]% | 0.0% | 0.0% | 0.0% |
| ambiguous_commit | resutura | 40 | 100.0% | [91.2, 100.0]% | 0.0% | 0.0% | 0.0% |
| ambiguous_commit | retry | 40 | 0.0% | [0.0, 8.8]% | 0.0% | 100.0% | 0.0% |
| ambiguous_commit | rewind | 40 | 0.0% | [0.0, 8.8]% | 0.0% | 100.0% | 0.0% |
| ambiguous_commit | verify | 40 | 100.0% | [91.2, 100.0]% | 0.0% | 0.0% | 0.0% |
| compensable_misdirection | base | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| compensable_misdirection | resutura | 40 | 100.0% | [91.2, 100.0]% | 0.0% | 0.0% | 0.0% |
| compensable_misdirection | retry | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| compensable_misdirection | rewind | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| compensable_misdirection | verify | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| concurrent_change_plus_misdirection | base | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| concurrent_change_plus_misdirection | resutura | 40 | 100.0% | [91.2, 100.0]% | 0.0% | 0.0% | 0.0% |
| concurrent_change_plus_misdirection | retry | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| concurrent_change_plus_misdirection | rewind | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| concurrent_change_plus_misdirection | verify | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| noncompensatable_misdirection | base | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| noncompensatable_misdirection | resutura | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 100.0% |
| noncompensatable_misdirection | retry | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| noncompensatable_misdirection | rewind | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |
| noncompensatable_misdirection | verify | 40 | 0.0% | [0.0, 8.8]% | 100.0% | 0.0% | 0.0% |

## Paired-seed contrasts against the strongest relevant baseline

Because the suite is deterministic, paired contrasts are reported as **coverage over matched task/fault seeds**, not p-values.

| Scenario | Contrast | Paired seeds where Resutura is strictly better | Ties | Worse |
|---|---|---:|---:|---:|
| compensable_misdirection | Resutura vs verify | 40/40 | 0/40 | 0/40 |
| ambiguous_commit | Resutura vs verify | 0/40 | 40/40 | 0/40 |
| concurrent_change_plus_misdirection | Resutura vs verify | 40/40 | 0/40 | 0/40 |
| noncompensatable_misdirection | Resutura vs verify | 40/40 | 0/40 | 0/40 |

## Chromium note

The bundled Chromium mechanism-transfer study uses only **2 paired trials per method/scenario**. That sample is deliberately treated as a transfer smoke test; no strong statistical claim or SOTA inference is made from it.

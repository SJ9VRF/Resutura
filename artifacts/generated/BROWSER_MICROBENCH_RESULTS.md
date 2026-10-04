# Chromium Mechanism Microbenchmark

**Evidence tier:** real Chromium DOM + deterministic planner + local effect ledger. **Not** OSWorld, not a frontier-model evaluation, and not SOTA evidence.

| Fault | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| close spreadsheet tab | 0% | 0% | 0% | 100% | 100% |
| lose focus | 0% | 0% | 0% | 100% | 100% |
| redirect publish target | 0% | 0% | 0% | 0% | 100% |
| ambiguous publish timeout | 100% | 0% | 100% | 0% | 100% |

Each cell uses 2 paired deterministic trials. This tiny sample is a smoke/mechanism check, not a statistical result.

Key qualitative checks:
- Browser-local failures (missing spreadsheet surface, lost focus) cross a real DOM adapter.
- Wrong-target committed effects require forward reconciliation; local rewind alone is insufficient.
- Ambiguous commit exposes a deliberate counterexample: Base succeeds by not retrying, Verify/Resutura succeed by readback, while blind Retry/Rewind duplicate and fail the exactly-once grader.
- The external-effect ledger is intentionally kept outside browser-local checkpoint restore.

# Experiment registry

Machine-readable registry: `experiments/registry.json`.

Every bundled study records an explicit seed policy and is paired across methods wherever the simulator allows identical task/fault snapshots. Generated JSON now includes a source fingerprint so a result can be tied to the code that produced it.

## Interpretation rule

Repeated deterministic simulator trials measure coverage over task/fault instances; they are **not** stochastic model samples. Wilson intervals in the summaries describe binomial uncertainty over the enumerated trial population under an IID approximation and must not be presented as uncertainty for frontier-model behavior.

The real-model study must separately report model-sampling variance, task variance, and paired differences from identical environment snapshots.

## Deterministic identifiers

Simulator run IDs and failure IDs are content-derived rather than UUID-derived, and bundled trajectory timestamps use logical zero-time unless a real adapter supplies a clock. This makes same-code/same-seed mechanism runs byte-stable rather than merely behaviorally equivalent.


## Chromium mechanism tier

`browser_microbench` is optional and requires Playwright plus Chromium. It uses a real DOM/process boundary but a deterministic planner, so it is evidence that the runtime contract survives a browser adapter—not evidence about model intelligence or frontier-CUA performance.

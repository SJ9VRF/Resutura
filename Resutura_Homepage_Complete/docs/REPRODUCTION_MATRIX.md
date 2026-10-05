# Reproduction Matrix

This matrix separates *what can be reproduced from this release* from *what still requires external systems*.

| Study | Entrypoint | Evidence tier | External dependency | Trials | Deterministic? | Primary purpose |
|---|---|---|---|---:|---|---|
| Effect Semantics Suite | `python experiments/effect_semantics_suite.py` | simulator | none | 40 / method / scenario | yes | recovery semantics across four effect classes |
| Tool Contract Matrix | `python experiments/tool_contract_matrix.py` | simulator | none | 40 / method / contract | yes | readback/idempotency capability boundary |
| Component Ablations | `python experiments/ablation_suite.py` | simulator | none | 40 / variant / scenario | yes | necessity of compensation, contract awareness, ownership |
| Pilot | `python experiments/run_pilot.py` | simulator | none | 120 / method | yes | broad smoke/mechanism check |
| External Effect Recovery | `python experiments/external_effect_recovery.py` | simulator | none | 60 / method | yes | focused external reconciliation |
| Policy Replay | `python experiments/policy_replay_smoke.py` | provider-boundary replay | none | 20 | yes | action-policy/recovery separation; **not model-backed** |
| Chromium Microbench | `python experiments/browser_microbench.py` | real browser DOM | Playwright + Chromium | 2 / method / fault | yes planner | mechanism transfer across process/DOM boundary |
| Chromium Effect Semantics | `python experiments/browser_effect_semantics.py` | real browser DOM | Playwright + Chromium | 2 / method / scenario | yes planner | effect semantics in Chromium; **not model-backed** |
| Model-backed real CUA | not bundled | future empirical gate | real model + browser/desktop benchmark | TBD | no | determine whether the hypothesis survives realistic policy errors |

## Fast integrity vs full reproduction

`make fast-audit` verifies packaged-file hashes, tests, claim-evidence hashes, and metadata consistency. It is the reviewer path.

`make audit` regenerates the bundled deterministic studies and is intentionally slower.

## Cost accounting

Bundled simulator studies incur no model-provider cost. Chromium studies incur local compute only. This release therefore must not quote model-dollar savings or production latency improvements.

## Statistical interpretation

Repeated deterministic trials test scenario coverage and implementation invariants. They are **not samples from a stochastic model distribution**. See `artifacts/generated/STATISTICAL_REPORT.md` for the intentionally limited uncertainty interpretation.

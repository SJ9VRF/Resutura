# External-effect reconciliation — deterministic mechanism study

**Study date:** September 25, 2026  
**Trials:** 60 per agent  
**Failure:** final `publish` action commits to `wrong-channel` while the intended target is `research-team`.

| Agent | Success | 95% Wilson CI | Unreconciled external-effect rate |
|---|---:|---:|---:|
| Base | 0.0% | 0.0–6.0% | 100% |
| Blind retry | 0.0% | 0.0–6.0% | 100% |
| Rewind | 0.0% | 0.0–6.0% | 100% |
| Resutura | 100% | 94.0–100% | 0% |

For Resutura, all recoveries in this study use the forward-compensation path: retract the unintended publication, publish to the intended target, then verify the target postcondition and protected prior progress. Mean recovery overhead is 2 actions and mean protected-progress preservation is 1.0 in the simulator.

**Important:** this is a deterministic mechanism study. It is not a real-browser, frontier-model, human-preference, or SOTA result.

# Public claim contract

## Safe claim now

> Resutura is a research artifact for effect-semantic recovery in computer-use agents. It distinguishes ambiguous commits, compensable wrong effects, protected concurrent external changes, non-compensatable effects, and ordinary local failures, then chooses verify/continue, forward compensation, preservation-aware repair, safe abort, or local rollback accordingly.

## Safe simulator result

> In a deterministic Effect Semantics Suite (40 trials per method per scenario), Resutura reconciled all compensable misdirection trials, avoided duplicate writes in all ambiguous-commit trials, preserved a concurrent valid external update in all corresponding trials, and safe-aborted all non-compensatable misdirection trials. These are mechanism-study results, not real-browser/model results.

## Important nuance

> Base also scores 100% ground-truth task success on the ambiguous-commit diagnostic because it never retries the lost acknowledgement. The Verification-Aware baseline also scores 100% when authoritative readback is available, which is expected and intentionally demonstrates that verify-before-retry is not a Resutura novelty. Retry and Rewind duplicate the already-committed effect when the contract lacks idempotency. Under an idempotent tool contract, those simple baselines also recover cleanly. This is why the release separates runtime contribution from tool-contract capability.

## Do not claim yet

- state of the art;
- first compensation, rollback-boundary, causal-repair, or exactly-once framework;
- superiority on OSWorld, BrowserGym, WebArena, or production agents;
- production safety guarantees;
- that the model itself can infer effect semantics in open-world environments.


## Safe tool-contract result

> In a deterministic Tool Contract Matrix with an unobservable ambiguous commit, authoritative readback was sufficient for both Verification-Aware and Resutura to avoid replay; tool-level idempotency was sufficient for Retry, Verification-Aware, Rewind, and Resutura to avoid duplicates. With neither capability, Verification-Aware and Resutura conservatively safe-aborted, while blind retry and rewind duplicated the effect. Base happened to leave the ground-truth world in the correct state because it did not retry, but it had no evidence that the commit occurred.

## Methodological safeguard

> Forked-state counterfactual execution is retained as an offline simulator diagnostic only. Its observed outcomes are not used to choose Resutura's online recovery action.

## Safe Chromium mechanism-transfer claim

> In a real headless Chromium DOM with a deterministic planner (2 paired trials per method/scenario), the effect-semantic behaviors transfer beyond the pure-Python state simulator: Resutura reconciles wrong-target committed effects, preserves a concurrent valid external publication, safe-aborts a non-compensatable wrong commit, and matches verification-aware recovery on an ambiguous commit. This is browser/DOM mechanism evidence, not a frontier-model or OSWorld result.

## Safe policy-boundary claim

> The release implements a provider-neutral policy interface and validates it with deterministic recorded-policy replay on 20 faulted trials. The replay provider is explicitly marked `model_backed=false`; no model-backed empirical result is bundled.


## Safe ablation claim

> In the deterministic component ablation (40 paired trials per variant/scenario), removing forward compensation eliminated success on compensable wrong-target effects; removing contract awareness caused duplicate replay and 0% success on ambiguous commits; removing effect ownership eliminated success on the concurrent-valid-change diagnostic. These are mechanism ablations inside the simulator, not model effect-size estimates.

## Safe dataset claim

> The release packages 160 public scenario/task records and 800 raw deterministic trajectories with a machine-readable schema and source-run hash. The included dev/test labels are public analysis splits, not hidden evaluation data.

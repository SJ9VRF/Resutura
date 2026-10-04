# Experiment Journal

**Project:** Resutura — Effect-Semantic Recovery for Computer-Use Agents  
**Author:** Aura Yavary  
**Evidence rule:** Every result below points to a bundled artifact. No entry is a reconstructed or invented experiment.

The journal records the project as it actually matured: hypothesis → experiment → awkward result or bug → interpretation → next decision. It is intentionally less tidy than the homepage.

## EXP-001 — Baseline recovery kernel

- **Hypothesis:** Can explicit expected-state verification plus structured recovery beat a plain agent and blind retry in a deterministic long-horizon workflow?
- **Setup:** 120 paired simulator tasks; Base, Blind Retry, Resutura.
- **Result:** Base 26.7%, Blind Retry 45.0%, Resutura 100% task success in the deterministic pilot.
- **Interpretation:** The mechanism was worth pursuing, but the result was only simulator evidence and too easy to treat as a general capability claim.
- **Next decision:** Move from generic recovery to effect-semantics cases where local rewind and retry can be demonstrably wrong.
- **Evidence:** [`artifacts/generated/PILOT_RESULTS.md`](../../artifacts/generated/PILOT_RESULTS.md)

## EXP-002 — Committed external-effect recovery

- **Hypothesis:** Does local rewind repair a task after the agent has already changed the external world?
- **Setup:** 60 paired deterministic trials per method; misdirected committed publication; Base, Retry, Rewind, Resutura.
- **Result:** Base/Retry/Rewind: 0/60. Resutura: 60/60; wrong external effects remaining: 0/60 after compensation.
- **Interpretation:** A checkpoint is not a world-state undo. Recovery needs an explicit external-effect ledger and compensation semantics.
- **Next decision:** Split rollback domains: local state can rewind; committed external effects must persist and be reconciled forward.
- **Evidence:** [`artifacts/generated/EXTERNAL_EFFECT_RESULTS.md`](../../artifacts/generated/EXTERNAL_EFFECT_RESULTS.md)

## EXP-003 — Ambiguous commit: verify before retry

- **Hypothesis:** When acknowledgement is lost after commit, is a richer recovery controller actually necessary?
- **Setup:** 40 paired trials/method; ambiguous commit with authoritative readback.
- **Result:** Base 100%; Retry 0% with duplicates; Verify 100%; Rewind 0% with duplicates; Resutura 100%.
- **Interpretation:** A strong prior-art baseline solves this case. Resutura must not claim verify-before-retry as novel.
- **Next decision:** Add Verification-Aware baseline permanently and narrow the contribution to heterogeneous effect semantics.
- **Evidence:** [`artifacts/generated/EFFECT_SEMANTICS_RESULTS.md`](../../artifacts/generated/EFFECT_SEMANTICS_RESULTS.md)

## EXP-004 — Tool-contract matrix

- **Hypothesis:** How much recovery behavior is determined by tool guarantees rather than the harness?
- **Setup:** 40 paired trials/method/contract across readback-only, idempotency-only, both, neither.
- **Result:** With idempotency, Retry/Verify/Rewind/Resutura all reached 100%. With readback only, Verify and Resutura reached 100%; Retry/Rewind duplicated. With neither, Verify and Resutura safe-aborted.
- **Interpretation:** The tool contract can dominate the recovery strategy; a runtime should not claim credit for guarantees supplied by the tool.
- **Next decision:** Make tool capabilities first-class inputs and report contract-conditioned results.
- **Evidence:** [`artifacts/generated/TOOL_CONTRACT_MATRIX.md`](../../artifacts/generated/TOOL_CONTRACT_MATRIX.md)

## EXP-005 — Ownership-aware compensation

- **Hypothesis:** Can compensation repair a wrong external effect without deleting valid concurrent state created by another actor?
- **Setup:** 40 paired trials/method in concurrent-valid-change + misdirection scenario.
- **Result:** Only full Resutura reached 100% in the signature deterministic suite. Removing effect ownership drops the case to 0%.
- **Interpretation:** Naive compensation is unsafe: “undo the first wrong-looking effect” can destroy another actor's valid work.
- **Next decision:** Attach actor/effect ownership to the ledger and only compensate agent-owned unreconciled effects.
- **Evidence:** [`artifacts/generated/ABLATION_RESULTS.md`](../../artifacts/generated/ABLATION_RESULTS.md)

## EXP-006 — Non-compensatable effects

- **Hypothesis:** Should recovery attempt to “win” when an external effect has no safe inverse?
- **Setup:** 40 paired trials/method; non-compensatable committed misdirection.
- **Result:** Resutura task success 0%, safe-abort 100%.
- **Interpretation:** A negative result is the correct result when repair is impossible. Optimizing only for completion would reward unsafe behavior.
- **Next decision:** Keep safe abort as a first-class terminal recovery outcome and surface it in headline tables.
- **Evidence:** [`artifacts/generated/EFFECT_SEMANTICS_RESULTS.md`](../../artifacts/generated/EFFECT_SEMANTICS_RESULTS.md)

## EXP-007 — Counterfactual recovery analysis boundary

- **Hypothesis:** Can forked-state counterfactual outcomes be used to select the online repair?
- **Setup:** Early simulator implementation executed candidate repairs on forked state and used those outcomes during selection.
- **Result:** Methodological audit found this leaks oracle information unavailable to a real online agent.
- **Interpretation:** Counterfactual replay is useful for diagnosis, but using realized fork outcomes for online policy selection overstates capability.
- **Next decision:** Set used_for_policy_selection=false; online selection only sees observations + declared tool contract.
- **Evidence:** [`docs/CLAIM_EVIDENCE_MAP.md`](../../docs/CLAIM_EVIDENCE_MAP.md)

## EXP-008 — Chromium mechanism transfer

- **Hypothesis:** Does the effect-semantic runtime survive a real browser/DOM boundary?
- **Setup:** Headless Chromium, deterministic planner, 2 paired trials/method/scenario.
- **Result:** Resutura 100% on misdirected commit and concurrent-change + misdirection; Verify ties Resutura on ambiguous commit; non-compensatable case safe-aborts.
- **Interpretation:** The mechanism transfers beyond Python dictionaries, but n=2 and deterministic planning are not frontier-model evidence.
- **Next decision:** Keep Chromium as a mechanism-transfer tier; do not promote it to a model benchmark.
- **Evidence:** [`artifacts/generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md`](../../artifacts/generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md)

## EXP-009 — Formal component ablations

- **Hypothesis:** Which components are actually necessary inside the deterministic testbed?
- **Setup:** 40 paired seeds/cell; remove compensation, contract awareness, or effect ownership.
- **Result:** −compensation: 0% on compensable misdirection; −contract awareness: 0% on ambiguous commit with 100% duplicates; −ownership: 0% on concurrent-valid-change case.
- **Interpretation:** Each component is tied to a distinct failure class rather than a generic “more machinery helps” story.
- **Next decision:** Keep ablations as claim-specific evidence, not as generic performance improvement.
- **Evidence:** [`artifacts/generated/ABLATION_RESULTS.md`](../../artifacts/generated/ABLATION_RESULTS.md)

## EXP-010 — Provider-neutral policy boundary

- **Hypothesis:** Can the runtime consume actions from an external policy interface without conflating replay with model-backed evidence?
- **Setup:** Recorded policy replay, 20 deterministic trials, provider-neutral JSON bridge.
- **Result:** 20/20 replay trials complete successfully; artifact is explicitly model_backed=false.
- **Interpretation:** Separating policy from recovery runtime is necessary for later model experiments, but replay is not model evidence.
- **Next decision:** Preserve the interface and gate all model-backed claims on a genuine external model run.
- **Evidence:** [`artifacts/generated/POLICY_REPLAY_RESULTS.md`](../../artifacts/generated/POLICY_REPLAY_RESULTS.md)

## EXP-011 — Byte-level reproducibility

- **Hypothesis:** Can the same code, seed, and config produce identical evidence bytes, not just similar metrics?
- **Setup:** Deterministic run/failure IDs, logical timestamps, deterministic gzip mtime, repeated signature runs.
- **Result:** Canonical signature outputs and dataset exports are byte-stable under repeated same-code/same-seed execution.
- **Interpretation:** Evidence provenance is easier to audit when raw artifacts are stable enough to hash.
- **Next decision:** Make deterministic artifact hashes part of the release contract and claim-evidence map.
- **Evidence:** [`docs/OFFLINE_REPRODUCIBILITY.md`](../../docs/OFFLINE_REPRODUCIBILITY.md)

## EXP-012 — Benchmark adversarialization

- **Hypothesis:** Does the benchmark itself accidentally favor Resutura?
- **Setup:** Adversarial review of browser fault reuse, exactly-once grading, concurrent-state grading, and rollback-domain semantics.
- **Result:** Found and fixed stateful perturbation reuse, duplicate-accepting browser grading, concurrent-state grader mismatch, and server-side idempotency rewind bug.
- **Interpretation:** The benchmark had multiple ways to manufacture optimistic results; adversarializing the evaluator materially changed the study quality.
- **Next decision:** Document benchmark bugs as evidence of maturation; regression-test each discovered failure.
- **Evidence:** [`CHANGELOG.md`](../../CHANGELOG.md)


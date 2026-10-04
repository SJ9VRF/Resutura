# Resutura — technical interview defense guide

This is not a script to memorize. It is a checklist of questions you should be able to answer from the implementation and evidence before presenting the project as your work.

## 1. What is the narrow research question?

A failed tool call does not determine the right recovery action. Resutura asks whether a recovery runtime can select among verify, replay, local repair, rewind, forward compensation, state preservation, and safe abort based on realized effect state and the guarantees exposed by the tool contract.

## 2. Why isn't Rewind enough?

Checkpoint restoration only controls the rollback domain it actually owns. A committed external publication survives local rewind. The Rewind baseline intentionally preserves that external state; this is why wrong-target committed effects remain wrong after restore.

## 3. Why isn't verify-before-retry enough?

It *is* enough for the ambiguous-commit case when authoritative readback exists. The Verification-Aware baseline matches Resutura there. It does not by itself repair a committed wrong-target effect or decide what to do when no compensator exists.

## 4. What does effect ownership buy you?

Without ownership, a target-only compensator can confuse valid concurrent external state with damage caused by the agent. The formal `− effect ownership` ablation succeeds on simple misdirection but fails the concurrent-valid-change diagnostic.

## 5. Why is safe abort a positive result?

For a non-compensatable committed effect, automatic success is impossible under the declared contract. The correct safety behavior is to preserve remaining progress and escalate. The benchmark therefore reports zero task success and 100% safe abort rather than optimizing the metric by inventing a reversal.

## 6. What are the strongest counterexamples to your own story?

- Base gets the final world state right in one ambiguous-commit setup by doing nothing, although it lacks evidence of commit status.
- Verification-Aware equals Resutura when readback fully resolves ambiguity.
- Tool-level idempotency lets Retry/Rewind succeed without sophisticated recovery logic.
- Chromium evidence is only two paired trials per method/scenario and is not a capability benchmark.

## 7. What bugs did the research process uncover?

Be able to explain the fixes, not just list them:
- reused stateful perturbations across methods;
- grader rejecting valid concurrent external state;
- local checkpoint restore incorrectly rewinding server-side idempotency state;
- offline counterfactual analysis missing the `exists` predicate;
- an earlier online selector consuming simulator counterfactual outcomes.

## 8. What would falsify the stronger hypothesis?

A real model-backed factorial study should weaken the claim if a simpler verification/transactional baseline matches Resutura across broader effect classes at lower cost, if effect classes require privileged labels unavailable to agents, or if safe-abort calibration causes unacceptable completion loss.

## 9. What is not done?

No frontier-model run, no OSWorld score, no production external-service integration, no security evaluation against malicious tools, and no SOTA claim.

## 10. Where is the evidence?

Start with `docs/CLAIM_EVIDENCE_MAP.md`, then inspect `runs/`, `artifacts/generated/`, the trajectory viewer, and `scripts/reproduce_core.py`.

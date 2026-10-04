# Open Research Questions and Falsification Roadmap

Resutura v1.2 is a research artifact, not a closed research program. These are the questions that still matter most.

## Q1 — Does effect-semantic recovery help with real model policies?

**Experiment:** factor model × harness × tool contract on side-effect-capable browser/desktop tasks.

**Would weaken the project:** a verification-aware or transactional baseline matches Resutura on realistic misdirection/concurrency cases at equal or lower cost.

## Q2 — Can a model infer the correct effect class from imperfect observations?

The bundled environment exposes reliable state. Real systems may offer delayed, partial, or contradictory readback.

**Experiment:** corrupt or delay effect evidence and measure classification error, collateral damage, and unnecessary escalation.

## Q3 — What if ownership is ambiguous?

Current ownership labels are explicit in the testbed.

**Experiment:** ambiguous provenance, shared accounts, delegated actions, and cross-agent writes.

**Failure criterion:** compensation deletes valid state because ownership inference is wrong.

## Q4 — What if compensation itself is non-atomic?

A compensator can fail after partially committing.

**Experiment:** recursively fault compensation and require bounded recovery or escalation.

## Q5 — How should permissions constrain recovery?

A technically valid compensator may exceed the agent's authority.

**Experiment:** capability-scoped recovery actions with explicit approval and denial paths.

## Q6 — Does the runtime still help when tools expose strong contracts?

The current Tool Contract Matrix already shows that idempotency/readback can make simpler policies sufficient.

**Experiment:** expand to transactional APIs with atomic commit, idempotency keys, receipts, and compensators.

**Expected outcome:** Resutura should *defer to stronger contracts*, not claim unnecessary wins.

## Q7 — Can recovery traces improve training?

This belongs to Flywheel-RL, not to the current Resutura claim.

**Experiment:** compare post-training on successful trajectories, failed trajectories, and verified recovery trajectories.

## Public gate before stronger claims

Do not add `SOTA`, production safety, OSWorld superiority, or frontier-model improvement to the homepage/resume until a real model-backed study clears the corresponding gate in `artifacts/generated/RESEARCH_CLAIMS.md`.

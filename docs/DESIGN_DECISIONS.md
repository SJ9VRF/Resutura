# Design decisions

## D1 — Recovery is conditioned on realized effect state, not exception type
A timeout or failed acknowledgement is not enough to decide whether to replay. The runtime first asks what state actually changed and what the tool contract permits it to know.

## D2 — Local rewind never rewinds committed external effects
A local checkpoint restores agent/application state only. External publications, server-side idempotency registries, and unrelated actor changes remain outside the rollback domain.

## D3 — Verification-aware recovery is a baseline, not a Resutura invention
When authoritative readback is sufficient, verification-before-retry should match Resutura. The project retains that result instead of weakening the baseline.

## D4 — Compensation is ownership-aware
A compensator may only target an agent-owned unreconciled effect. This prevents recovery from deleting a concurrent valid change produced by another actor.

## D5 — Non-compensatable effects terminate in safe abort
The system does not manufacture “recovery success” when the world cannot be restored safely. Human escalation is a first-class outcome.

## D6 — Counterfactual forks are offline diagnostics only
Forked-state outcomes are useful for analysis and ablations but unavailable to a real online agent. They are explicitly prohibited from online policy selection.

## D7 — Tool contracts are experimental factors
Readback and idempotency are varied rather than assumed. When the tool contract solves the problem, the results should show that simpler baselines become sufficient.

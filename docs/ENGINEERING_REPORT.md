# Resutura — Engineering Report

**Aura Yavary · 2026**

## 1. Problem

Computer-use agents fail across a boundary that conventional retry/replan logic often ignores: some actions mutate only local execution state, while others create external effects that survive local rollback. A failed call can therefore mean very different things: nothing happened; the intended action committed but its acknowledgement was lost; the action committed to the wrong target; another actor changed the world concurrently; or the effect is irreversible.

Resutura treats recovery as a state-reconciliation problem rather than a generic retry policy.

## 2. Runtime contract

The online runtime receives an action proposal plus expected postconditions. After execution it observes realized state, classifies the effect, and chooses among continue, verify, local repair, checkpoint rewind, forward compensation, preservation of concurrent valid state, or safe abort.

The online controller is deliberately prevented from consuming simulator-only fork outcomes. Counterfactual forks are retained only for offline diagnosis and are marked `used_for_policy_selection=false`.

## 3. State model

Resutura separates:

- rewindable local execution state;
- committed external state;
- an effect ledger with actor ownership, requested target, realized target, commit status, compensatability, and reconciliation status;
- protected invariants representing prior valid progress and concurrent external work.

Checkpoint restore affects only rewindable state. Server/external idempotency state and committed effects survive local rewind.

## 4. Recovery semantics

- **Verify-before-retry:** used for ambiguous commits when authoritative readback is available.
- **Local repair:** used for reversible local divergence.
- **Rewind:** restores a verified local checkpoint without pretending to undo committed external effects.
- **Forward compensation:** applies a new corrective action to reconcile an agent-owned wrong effect.
- **Preserve:** leaves valid concurrent external changes untouched.
- **Safe abort:** used when no safe compensator or authoritative resolution is available.

## 5. Baselines

The release includes Base, blind Retry, Verification-Aware, Rewind, and Resutura. Verification-Aware is important because verify-before-retry is prior work; Resutura should not receive credit when readback alone solves the failure. The Tool Contract Matrix similarly exposes cases where idempotency supplied by the tool makes simple retry sufficient.

## 6. Evidence tiers

1. Deterministic simulator for controlled semantics studies.
2. Headless Chromium DOM for mechanism transfer outside Python dictionaries.
3. Provider-neutral policy boundary and recorded-policy replay.
4. Frontier-model CUA evaluation remains a future gate and is not claimed here.

## 7. Reproducibility

The simulator uses deterministic IDs and logical timestamps. Signature studies record source fingerprints, seed policies, raw trajectories, and manifest hashes. A fast release audit verifies package integrity, unit tests, and signature experiments.

## 8. Safety boundary

Resutura never equates task completion with safe recovery. Non-compensatable effects produce a safe abort rather than fabricated success. Permission boundaries, authorization, and human escalation remain required for high-impact real-world actions.

## 9. Known limitations

The current planner in bundled browser experiments is deterministic, not a frontier model. The Chromium tier is a mechanism microbenchmark rather than OSWorld. Latency and monetary cost are therefore not reported as model-performance claims. Real deployments also require richer tool contracts, authorization models, and adversarial security testing.

## 10. Next empirical gate

The strongest next experiment is factorial: model × environment × recovery harness × tool contract. The central falsification test is whether a simpler verification/transactional baseline matches Resutura on realistic misdirection, concurrency, and non-compensatable failures at equal or lower cost.

# Resutura — one-page technical brief

**Aura Yavary · Effect-Semantic Recovery for Computer-Use Agents**

## Problem
A computer-use agent can restore its local execution state without undoing a committed external effect. Retrying blindly can duplicate effects; rewinding locally can leave the world inconsistent; compensating naively can delete another actor's valid work.

## Core idea
Treat recovery as an **effect-semantic decision**. After each consequential action, inspect realized state plus tool-contract guarantees, then select among verification, local repair, rewind, forward compensation, preservation of concurrent state, or safe abort.

## Strongest measured evidence
In the bundled deterministic Chromium mechanism suite, Resutura reconciles committed wrong-target effects and concurrent-valid-change cases where Base / Retry / Verify / Rewind do not, matches the Verification-Aware baseline on ambiguous commits, and safe-aborts non-compensatable effects. This is **mechanism-transfer evidence, not a frontier-model benchmark**.

## Why the result is credible
Strong baselines are retained; tool contracts are factorized; component ablations are included; counterexamples and negative results remain visible; online policy selection cannot use simulator counterfactual oracles; claim hashes point to raw evidence.

## Falsification gate
If model-backed real-browser experiments show no benefit over verification-aware or transactional baselines after controlling for tool contracts—or if recovery causes meaningful collateral external-state damage—the current contribution does not survive.

## Evidence of maturation
The project also ships an explicit Evidence Layer rather than presenting a straight-line success story: 12 experiment/maturation entries, 12 failed assumptions/benchmark bugs/framing reversals, 10 major design decisions, real eval tables, unexpected findings, focused raw trajectories, and an authentic post-v1.0 Git bundle. Start at `artifacts/evidence_layer/README.md`.

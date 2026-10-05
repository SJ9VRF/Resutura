# Resutura failure gallery

These are **actual bundled deterministic trajectories**, not invented anecdotes. Each example points to the raw Effect Semantics Suite (`runs/effect_semantics_suite.json`) and the machine-readable dataset (`artifacts/dataset/trajectories.jsonl.gz`).

## 1. Committed to the wrong target → forward compensation

**Fault:** intended publication target is `research-team`; the environment commits to `wrong-channel`.

**Observed failure:** `MISDIRECTED_EXTERNAL_EFFECT` at the publish step. A local rewind would not delete the already committed external publication.

**Resutura response:** `R4_forward_compensation` → retract the agent-owned wrong publication → publish once to the intended target → re-verify protected progress.

**Bundled evidence (seed 0):** recovery succeeded, 2 recovery actions, progress preservation ratio 1.0, external effect reconciled `true`.

## 2. Acknowledgement lost after commit → verify, do not replay

**Fault:** the publication commits, but the caller receives a timeout/error acknowledgement.

**Observed failure:** `AMBIGUOUS_COMMIT`.

**Resutura response:** authoritative effect readback confirms commit → `R0_continue`; no replay, no duplicate.

**Why it matters:** blind retry duplicates the intended effect in the corresponding tool-contract diagnostic when replay is not idempotent.

## 3. Concurrent valid state + wrong agent effect → compensate only owned damage

**Fault:** another actor publishes a valid `coordinator-note`, then the agent's own publication is redirected to the wrong target.

**Observed failure:** the joint state contains both a protected external update and an agent-owned wrong effect.

**Resutura response:** use ledger ownership to retract only the agent-owned wrong effect, preserve `coordinator-note`, then publish to `research-team`.

**Bundled evidence (seed 0):** progress preservation 1.0; protected invariants verified; external effect reconciled.

## 4. Non-compensatable wrong effect → safe abort

**Fault:** the wrong external publication is marked non-compensatable.

**Observed failure:** `IRREVERSIBLE_MISDIRECTED_EFFECT`.

**Resutura response:** `R7_safe_abort`, zero recovery actions, preserve all recoverable prior progress, escalate rather than claim success.

**Bundled evidence (seed 0):** task success `false`, safe abort `true`, preserved progress ratio 1.0.

## Evidence boundary

This gallery demonstrates the implemented recovery semantics in the bundled deterministic mechanism testbed. It is not evidence that the same rates hold for frontier models, natural web tasks, malicious tools, or production environments.

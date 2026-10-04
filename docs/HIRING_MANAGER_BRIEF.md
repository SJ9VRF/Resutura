# Resutura — 5-minute technical brief

**Author:** Aura Yavary  
**Question:** when a computer-use agent receives a failed/ambiguous tool outcome, what recovery action is justified by the *realized external effect* and the *tool contract*?

## 60-second path

Open `artifacts/website/index.html` first. The project page gives the problem, novelty boundary, architecture, measured Chromium result, failure analysis, safety limitations, and links to Paper / Code / Demo / Benchmark / Video without requiring the paper to be read first.


## 30 seconds: the idea

A local rewind cannot undo a committed external effect. Resutura therefore makes recovery conditional on effect semantics rather than treating every error as retry/replan/rollback. The runtime can verify, compensate, preserve concurrent state, rewind local state, or safe-abort.

## 90 seconds: the evidence

Run:

```bash
python scripts/audit_release.py --fast
```

Then inspect:
- `artifacts/generated/EFFECT_SEMANTICS_RESULTS.md`
- `artifacts/generated/TOOL_CONTRACT_MATRIX.md`
- `runs/demo.html`
- `artifacts/generated/BROWSER_MICROBENCH_RESULTS.md`
- `artifacts/generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md`
- `artifacts/generated/POLICY_REPLAY_RESULTS.md`
- `artifacts/generated/ABLATION_RESULTS.md`
- `artifacts/generated/STATISTICAL_REPORT.md`
- `docs/CLAIM_EVIDENCE_MAP.md`

The important result is **not** that Resutura wins every cell. It does not. Verification-aware recovery matches it when readback fully resolves ambiguous commit; retry/rewind also become sufficient when the tool contract provides idempotency. The extra machinery matters on wrong-target committed effects, ownership-sensitive compensation, and non-compensatable outcomes.

## 90 seconds: inspect the ablations and data

- `artifacts/generated/ABLATION_RESULTS.md` — what breaks when compensation, contract awareness, or effect ownership is removed;
- `artifacts/dataset/` — 160 public diagnostic items + 800 raw trajectories;
- `scripts/reproduce_core.py` — one-command regeneration of the core simulator evidence.

## 2 minutes: inspect the implementation

- `resutura/envs/sandbox.py` — local state vs committed external effects;
- `resutura/verifier.py` — postcondition/readback verification;
- `resutura/diagnoser.py` — effect-state classification;
- `resutura/recovery.py` — online selection and offline-only counterfactual diagnostics;
- `resutura/agent.py` — execution loop and repair certificates.

Search for `used_for_policy_selection`: forked simulator outcomes are explicitly excluded from online policy selection.

## 1 minute: try to break the claim

Read `docs/THREAT_MODEL.md` and `docs/NOVELTY_AND_POSITIONING.md`. The bundled evidence is deterministic mechanism validation, not a frontier-model result. The release now includes an optional real-Chromium mechanism tier (`docs/BROWSER_MICROBENCH.md`). A provider-neutral policy boundary is implemented and replay-tested, but the remaining hard gate is still a **genuinely model-backed** browser/desktop × harness × tool-contract study. The release explicitly does not relabel replayed policy traces as model evidence.

## What would change my mind

The project hypothesis weakens substantially if a simpler verification/transactional baseline matches Resutura across realistic misdirection, concurrency, and non-compensatable cases at equal or lower cost. That experiment is intentionally part of the real-world gate.

## 60 seconds: inspect the research process, not just the polished result

Open `artifacts/evidence_layer/README.md` and then `artifacts/experiment_logs/README.md`. The release preserves 12 documented experiment/maturation steps, 12 failures or false starts, and 10 major decisions. In particular, inspect the oracle-leakage fix, ownership-naive compensation failure, idempotency rollback-domain bug, perturbation-reuse benchmark bug, duplicate-accepting browser grader, and the negative non-compensatable result. The Git-history note explicitly refuses to fabricate pre-v1.0 commits.

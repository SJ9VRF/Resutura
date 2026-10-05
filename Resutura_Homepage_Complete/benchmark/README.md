# Resutura Benchmark Index

**Author:** Aura Yavary  
**Version:** 1.0.0

This index separates the project’s evidence tiers so simulator results are never mistaken for model-backed or production evidence.

## Tier A — Deterministic Effect Semantics Suite

- Four effect classes: compensable misdirection, ambiguous commit, concurrent valid change + misdirection, and non-compensatable misdirection.
- Five methods: Base, Retry, Verification-Aware, Rewind, Resutura.
- 40 deterministic trials per method/scenario in the simulator.
- Raw trajectories: `../../runs/effect_semantics_suite.json.gz`
- Summary: `../generated/EFFECT_SEMANTICS_RESULTS.md`

## Tier B — Tool Contract Matrix

- Toggles authoritative readback and idempotency independently.
- Tests whether reliability comes from the recovery runtime or from the tool contract itself.
- Raw output: `../../runs/tool_contract_matrix.json.gz`
- Summary: `../generated/TOOL_CONTRACT_MATRIX.md`

## Tier C — Chromium Effect-Semantics Suite

- Real headless Chromium DOM with a deterministic planner.
- Two paired trials per method/scenario.
- Every method receives a fresh fault instance.
- Raw output: `../../runs/browser_effect_semantics.json`
- Summary: `../generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md`

## Tier D — Policy Boundary Replay

- Exercises the provider-neutral policy/recovery boundary with recorded deterministic actions.
- This is not model evidence.
- Raw output: `../../runs/policy_replay_smoke.json`
- Summary: `../generated/POLICY_REPLAY_RESULTS.md`

## Not yet claimed

No frontier-model, OSWorld, production-safety, or SOTA result is claimed in this release. The next empirical gate is a model × environment × harness × tool-contract evaluation using the same recovery interfaces.


## Formal component ablations
- Report: `../generated/ABLATION_RESULTS.md`
- Raw: `../../runs/ablation_suite.json.gz`

## Dataset release
- Benchmark card: `BENCHMARK_CARD.md`
- Tasks: `../dataset/tasks.jsonl`
- Trajectories: `../dataset/trajectories.jsonl.gz`
- Schema / source hash: `../dataset/schema.json`, `../dataset/manifest.json`

## Uncertainty accounting
- `../generated/STATISTICAL_REPORT.md`

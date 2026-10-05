# Resutura Mechanism Traces — dataset card

**Author:** Aura Yavary  
**Version:** 1.0.0  
**Status:** deterministic diagnostic dataset; not a real-world CUA benchmark

## Purpose

The dataset packages the exact task/fault specifications and raw trajectories underlying the bundled Effect Semantics Suite. It is meant for auditing recovery semantics, building trajectory visualizations, and testing analysis code — not for estimating frontier-model performance.

## Packaged files

- `artifacts/dataset/tasks.jsonl` — 160 public scenario/task records;
- `artifacts/dataset/trajectories.jsonl.gz` — 800 raw trajectories (5 methods × 4 scenarios × 40 paired trials);
- `artifacts/dataset/schema.json` — machine-readable schema and required fields;
- `artifacts/dataset/manifest.json` — counts, public split summary, and source-run SHA-256.

## Scenarios

1. `compensable_misdirection` — publish commits to the wrong target and can be retracted.
2. `ambiguous_commit` — intended publish commits but the acknowledgement is lost.
3. `concurrent_change_plus_misdirection` — a valid external actor update coexists with an agent-owned wrong effect.
4. `noncompensatable_misdirection` — wrong external effect commits with no safe compensator.

## Methods

- Base
- Blind Retry
- Verification-Aware
- Rewind
- Resutura

## Splits

A deterministic public `dev` / `test` split is included for analysis hygiene. **It is not hidden evaluation data** and must not be presented as contamination-resistant benchmarking.

## Grading

The deterministic grader checks local task artifacts, intended publication, exactly-once publication count, absence of unreconciled agent-owned wrong effects, preservation of protected external changes, and safe abort when recovery is impossible.

## Known limitations

The suite exposes explicit simulator state and hand-specified effect semantics. It does not measure whether a language model can infer commit status, ownership, compensatability, authorization, or hidden state from open-world interfaces. Do not use it as evidence of real CUA, production, or SOTA performance.

## Tool-contract diagnostic

The separate Tool Contract Matrix crosses an unobservable ambiguous commit with declared readback/idempotency capabilities. Those runs are retained separately because they test a capability boundary rather than the core trace dataset above.

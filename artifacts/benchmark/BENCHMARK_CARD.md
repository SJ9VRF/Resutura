# Resutura Effect-Semantics Diagnostic — Benchmark Card

**Purpose:** isolate recovery behavior after external effects under controlled, paired faults.

**Primary scenarios**
- compensable wrong-target commit;
- ambiguous commit / acknowledgement loss;
- concurrent valid external change + agent misdirection;
- non-compensatable committed effect.

**Methods:** Base, Retry, Verification-Aware, Rewind, Resutura; plus component ablations and tool-contract capability toggles.

**Primary outcomes**
- final world-state correctness;
- unreconciled agent-owned external effect rate;
- duplicate intended effect rate;
- protected external state loss rate;
- safe-abort rate for non-compensatable effects;
- recovery overhead and progress preservation.

**Pairing:** task generation and fault seeds are paired across compared methods.

**Scale:** 40 deterministic simulator trials/method/scenario for the main diagnostic; Chromium is a 2-trial/method/scenario mechanism-transfer smoke test.

**Not a claim of:** natural-task coverage, model intelligence, OSWorld performance, SOTA, production safety, or security against malicious tools.

**Dataset:** `artifacts/dataset/tasks.jsonl` + `artifacts/dataset/trajectories.jsonl.gz`.

**Reproduction:** `python scripts/reproduce_core.py`.

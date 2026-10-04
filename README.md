# Resutura

**Effect-Semantic Recovery for Computer-Use Agents**  
**Aura Yavary · 2026**

> **Rewinding the agent is not the same as reconciling the world.**

Resutura is a research runtime and diagnostic suite for recovery after an interactive agent has already changed external state. The project does **not** assume every failure should be retried, rewound, or compensated. Instead, recovery depends on what actually happened at the effect boundary.

This research release distinguishes four consequential effect classes and exposes a provider-neutral policy boundary:

1. **ambiguous commit** — the effect may have committed even though the acknowledgement was lost; verify before retry;
2. **compensable misdirection** — an incorrect external effect committed and a valid compensator exists; compensate forward;
3. **concurrent valid change** — another actor changed external state legitimately; recovery must preserve it;
4. **non-compensatable effect** — the bad effect cannot be safely undone; stop and escalate rather than fake recovery.

This framing is intentionally narrower than generic self-correction, rollback, causal repair, or transactional tool use.

## Research question

> **Can a computer-use recovery runtime choose the correct recovery semantics from realized effect state - verify, compensate, preserve, or stop - while retaining valid task progress?**

The execution contract is:

`intent → expected postconditions → action → realized effect → verify → classify effect state → recover under effect semantics → verify joint world state`

## What is implemented

- deterministic browser → spreadsheet → document workflow environment;
- structured task/environment state and typed postconditions;
- online state-delta verification;
- effect ledger with agent/external ownership;
- explicit publication counts for duplicate-effect detection;
- checkpoint restore that intentionally preserves committed external effects;
- retry, local repair, subgoal repair, forward compensation, rewind, global replan, and safe abort;
- verify-before-retry handling for ambiguous commits;
- protected invariants for concurrent valid external changes;
- non-compensatable effect detection and safe escalation;
- forked-state counterfactual execution where the environment is snapshot-able;
- auditable repair certificates;
- Base, blind-retry, verification-aware, rewind, and Resutura baselines;
- tests, CI, trajectory viewer, experiment configs, evidence ledger, paper, and project page.
- optional **real-Chromium DOM microbenchmark** validating the same recovery contract beyond the pure-Python simulator;
- provider-neutral `PolicyProvider` interface, deterministic recorded-policy replay, and subprocess bridge for plugging in external model policies without coupling credentials/SDKs to the research core.



## Policy/model boundary

`resutura/model_policy.py` defines a narrow JSON contract between an action policy and the recovery runtime. The policy proposes the next task action and expected postconditions; Resutura independently verifies realized state and owns recovery semantics. Two providers ship with the release:

- `RecordedPolicyProvider` — deterministic replay of previously recorded decisions for audit/reproduction;
- `CommandPolicyProvider` — JSON-over-stdin/stdout bridge to any external model wrapper.

`experiments/policy_replay_smoke.py` validates this boundary on 20 faulted trials. **It is not a model-backed result.** No frontier-model numbers are bundled because no external model API was executed for this release. See `docs/MODEL_POLICY_INTERFACE.md`.

## Optional Chromium execution tier

The release now includes `resutura/envs/browser.py`, `experiments/browser_microbench.py`, and `experiments/browser_effect_semantics.py`. This uses a real headless Chromium DOM for navigation, focus, spreadsheet/document writes, and perturbations while preserving the same explicit external-effect ledger. It is a **mechanism microbenchmark**, not a frontier-model or OSWorld result. See `docs/BROWSER_MICROBENCH.md`.

## Effect Semantics Suite

The release includes a deterministic diagnostic suite with 40 trials per agent per scenario.

| Scenario | Base | Retry | Verify | Rewind | Resutura | What it tests |
|---|---:|---:|---:|---:|---:|---|
| Compensable misdirection | 0% | 0% | 0% | 0% | **100%** | forward reconciliation after a committed wrong-target effect |
| Ambiguous commit | **100%** | 0% | **100%** | 0% | **100%** | verify-before-retry is a strong prior-work baseline, not a Resutura invention |
| Concurrent valid change + misdirection | 0% | 0% | 0% | 0% | **100%** | ownership-aware compensation without deleting someone else's valid change |
| Non-compensatable misdirection | 0% | 0% | 0% | 0% | 0% task success / **100% safe abort** | recognizing that some failures cannot be safely recovered |

The Base result in ambiguous commit is intentionally left as-is: it succeeds because it never retries the lost acknowledgement. That is not a robust policy; it is a useful counterexample showing why task success alone cannot characterize recovery quality.

These are **mechanism-study results in a deterministic simulator**. They are not OSWorld, frontier-model, production, or SOTA results.

Full results: `artifacts/generated/EFFECT_SEMANTICS_RESULTS.md`. Large raw trajectories are shipped as gzip-compressed JSON under `runs/` to keep the release lightweight.

## Tool Contract Matrix

A second diagnostic removes a hidden assumption from the first suite: an ambiguous commit is made **unobservable in the failed call result**, and the runtime is varied across declared readback/idempotency capabilities. Forty trials are executed per method per contract.

| Tool contract | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| Readback only | 100% | 0% (duplicates) | **100%** | 0% (duplicates) | **100%** |
| Idempotency only | 100% | **100%** | **100%** | **100%** | **100%** |
| Readback + idempotency | 100% | **100%** | **100%** | **100%** | **100%** |
| Neither | 100% ground-truth completion* | 0% (duplicates) | 0% / **100% safe abort** | 0% (duplicates) | 0% / **100% safe abort** |

*The Base policy gets the externally correct state by luck because the original write committed and Base never retries. It has no evidence that the commit occurred. This row is intentionally retained: without readback or idempotency, a runtime cannot in general turn an ambiguous outcome into both known completion and exactly-once replay safety.

The matrix also exposed a simulator bug: checkpoint restore originally rewound the server-side idempotency registry, making Rewind duplicate even under an idempotent contract. The registry is now correctly treated as external state and survives local rewind.

This study is particularly important for positioning: **Resutura does not claim to beat a strong tool contract.** When the tool itself provides idempotency, simple retry and rewind become sufficient for this fault; when authoritative readback exists, the verification-aware baseline matches Resutura on ambiguous commit. The additional Resutura machinery is exercised by effect classes such as misdirection, ownership-sensitive compensation, and non-compensatable outcomes.

## Why the claim is narrow

The 2026 literature already covers many neighboring ideas: transactional tool semantics, effect staging/compensation, causal counterfactual repair, CUA failure diagnosis, checkpoint rewind, non-atomic tool verification, replay-resistant external writes, and reversibility taxonomies. Resutura therefore does **not** claim to invent rollback, compensation, idempotency, causal repair, or side-effect ledgers.

Its current contribution hypothesis is the **integrated recovery decision contract for computer-use trajectories**, evaluated across effect states where the correct action changes qualitatively: continue after verification, compensate, preserve concurrent state, or stop.

See:

- `docs/RELATED_WORK_MAP.md`
- `docs/NOVELTY_AND_POSITIONING.md`
- `docs/EVIDENCE_LEDGER.md`


## Five-minute audit path

If you are reviewing the project rather than developing it, start with `docs/HIRING_MANAGER_BRIEF.md` and run:

```bash
python scripts/audit_release.py --fast
```

This verifies packaged-file integrity, the test suite, claim-evidence hashes, and cross-artifact metadata consistency without rerunning the slow research studies. See `experiments/registry.json` for the exact trial/seed policies and `docs/THREAT_MODEL.md` for the recovery boundary. Reviewer-specific reading paths are in `docs/REVIEW_PATHS.md`, and an owner-level code trace is in `docs/CODE_WALKTHROUGH.md`.

## Quick start

```bash
python -m pip install -e .
# Offline environment with setuptools already present:
# python -m pip install -e . --no-build-isolation
pytest -q
python experiments/effect_semantics_suite.py
python experiments/tool_contract_matrix.py
python experiments/run_pilot.py
python experiments/external_effect_recovery.py
python experiments/policy_replay_smoke.py
# Optional when Playwright/Chromium are installed:
python experiments/browser_effect_semantics.py
python -m resutura.cli demo --out runs/demo.json
python -m resutura.cli viewer --run runs/demo.json --out runs/demo.html
```

## Evidence rules

A public empirical claim is allowed only when the release contains the task-suite version, exact agent/model configuration, raw trajectories, deterministic or calibrated graders, repeated trials, uncertainty, and the relevant baselines.

The word **SOTA is prohibited** for the bundled simulator studies. Forked-state counterfactual replay is logged only as simulator analysis and is explicitly **not used for online recovery selection**.

## Real-world gate

The next decisive experiment is a side-effect-capable browser/desktop benchmark with real models. It must include at least:

- ambiguous commit / lost acknowledgement;
- delayed visibility and duplicate-delivery faults;
- idempotent vs non-idempotent tools;
- compensable and non-compensatable effects;
- concurrent legitimate external changes;
- authorization/approval boundaries;
- exact model, harness, and tool-contract variants;
- paired trials from identical snapshots;
- Base, Retry, RCA+re-execution, Rewind, verification-aware, and transactional/compensation baselines.

Primary metrics: final world-state correctness, duplicate-effect rate, unreconciled-effect rate, protected-progress preservation, collateral damage, safe-abort precision, recovery cost, and latency.

## Author

**Aura Yavary**

## Project page and communication artifacts

The independent project homepage is `artifacts/website/index.html`. It is designed for a 60-second technical scan and includes the Hero result, problem, novelty boundary, architecture, author contribution, experiment setup, results, failure analysis, interactive trajectory demo, scaling status, safety/limitations, technical deep dive, full artifact index, and citation.

Supporting artifacts:

- `artifacts/video/resutura_overview.mp4` — short visual overview;
- `artifacts/benchmark/README.md` — benchmark/evidence-tier index;
- `docs/ENGINEERING_REPORT.md` — technical report;
- `artifacts/blog/RESUTURA_BLOG.md` — research blog post;
- `artifacts/citation/resutura.bib` — BibTeX citation.

The GitHub link is intentionally not fabricated in this local release.

## Formal ablation suite (v1.0.0)

`python experiments/ablation_suite.py` runs 40 paired trials per variant/scenario and removes one semantic capability at a time:

- `− compensation` breaks recovery from committed wrong-target effects;
- `− contract awareness` blindly replays ambiguous commits and duplicates the intended effect;
- `− effect ownership` breaks concurrent-state reconciliation;
- full Resutura preserves the intended behavior, including safe abort for non-compensatable effects.

See `artifacts/generated/ABLATION_RESULTS.md`.

## Packaged dataset

`python scripts/export_dataset.py` exports the auditable mechanism dataset used by the primary suite:

- `artifacts/dataset/tasks.jsonl` — 160 scenario/task records;
- `artifacts/dataset/trajectories.jsonl.gz` — 800 raw trajectories;
- `artifacts/dataset/schema.json` — machine-readable schema;
- `artifacts/dataset/manifest.json` — counts and source-run SHA-256.

The dev/test labels are **public analysis splits**, not hidden benchmark data. See `artifacts/dataset_card/DATASET_CARD.md`.

## One-command core evidence reproduction

```bash
python scripts/reproduce_core.py
```

This regenerates the Effect Semantics Suite, Tool Contract Matrix, formal ablations, dataset package, and uncertainty report. Chromium remains optional because it requires Playwright/Chromium.

## v1.0 public-release surface

For a fast external review, use these entry points:

- `artifacts/recruiting/ONE_PAGE.md` — one-page technical brief;
- `artifacts/website/index.html` — 14-section project homepage;
- `artifacts/paper/main.pdf` — paper artifact;
- `artifacts/benchmark/BENCHMARK_CARD.md` — benchmark scope and evidence tiers;
- `docs/CLAIM_EVIDENCE_MAP.md` — claim-to-raw-evidence hashes;
- `docs/DESIGN_DECISIONS.md` — the design choices most likely to be challenged in review;
- `docs/INTERVIEW_DEFENSE_GUIDE.md` — technical questions and failure boundaries;
- `docs/PUBLIC_RELEASE_CHECKLIST.md` — what this release does and does not establish.

`make fast-audit` checks package integrity quickly. `make audit` reruns the full bundled research reproduction path and is intentionally slower.

## Evidence Layer (v1.2.0)

The polished homepage is intentionally not the whole research story. The bundled Evidence Layer records how the project actually changed:

- `artifacts/experiment_logs/` — 12 experiment / maturation entries with hypothesis, setup, result, interpretation, and next decision;
- `artifacts/evidence_layer/FAILED_EXPERIMENTS.md` — 12 failed assumptions, benchmark bugs, implementation failures, or framing reversals;
- `artifacts/evidence_layer/DECISION_LOG.md` — 10 major technical decisions in Decision → Alternatives → Evidence → Trade-off → Outcome format;
- `artifacts/evidence_layer/REAL_EVAL_TABLES.md` — executed tables only;
- `artifacts/evidence_layer/UNEXPECTED_FINDINGS.md` — findings that narrowed or redirected the project;
- `artifacts/git_history/` — explicit provenance policy and the authentic post-v1.0 Git bundle;
- `artifacts/eval_runs/`, `failure_examples/`, `plots/`, `configs/`, `qualitative_cases/`, `ablations/` — raw-evidence entrypoints.

The release does **not** invent pre-v1.0 Git history.

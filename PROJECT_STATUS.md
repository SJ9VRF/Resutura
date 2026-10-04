## v1.2.0 audit-consistency release

- preserves the real research process alongside the polished project page;
- documents 12 experiment/maturation entries, 12 failures or false starts, and 10 major design decisions;
- surfaces awkward baseline wins, negative results, evaluator bugs, and research-framing pivots rather than rewriting the project as a straight-line success;
- keeps historical Git provenance honest: no pre-v1.0 commits are backfilled, while post-import Evidence Layer work is preserved incrementally.

Release: **1.2.0** · Author: **Aura Yavary**

## v1.0.0 public-research release

- stabilized the public repo surface and release vocabulary;
- added deterministic release packaging and independent claim-hash verification;
- added public-repo governance files, design-decision record, recruiter/reviewer artifacts, and reproducible Make targets;
- removed interpreter caches and build residue from distributable artifacts;
- preserved the same evidence boundary: simulator + deterministic Chromium mechanism transfer, not frontier-model or SOTA evidence.

Release: **1.0.0** · Author: **Aura Yavary**

## v0.9.0 evidence-completeness pass

- added formal component ablations for compensation, contract awareness, and effect ownership;
- added packaged machine-readable dataset: 160 task/fault records + 800 raw trajectories;
- added statistical/uncertainty report with Wilson intervals and paired-seed contrasts, with explicit deterministic-testbed caveat;
- added actual agent failure gallery, benchmark card, and one-command core evidence reproduction;
- fixed offline counterfactual analysis for `exists` postconditions and regression-tested it;
- homepage now links ablations, dataset payloads, failure traces, and uncertainty accounting directly.

Release: **0.9.0** · Author: **Aura Yavary**

## Historical v0.8.1 project-page and communication artifacts

- rebuilt the independent project homepage around a 60-second hiring-manager path;
- added working Paper / Code / Demo / Benchmark / Video hero links;
- added architecture, author contribution, experiments, results, failure analysis, interactive demo, scaling, safety, technical deep dive, artifacts, and citation sections;
- added benchmark index, engineering report, research blog post, overview video, and BibTeX citation;
- preserved explicit evidence boundaries and left GitHub unpublished rather than inventing a repository URL.

Release: **0.8.1** · Author: **Aura Yavary**

# Project status - Resutura

**Author: Aura Yavary**

## Verified in this release

- Automated unit/integration/release tests pass in the verified release; the exact count is produced by `pytest -q` rather than duplicated here.
- Effect ledger distinguishes agent-owned and external effects.
- Rewind preserves committed external effects by construction.
- Ambiguous-commit path verifies realized postconditions before retry.
- Compensable misdirection uses ownership-aware forward compensation.
- Concurrent valid external state is preserved through recovery.
- Non-compensatable misdirection triggers safe abort rather than fake success.
- Effect Semantics Suite executes 40 trials per agent per scenario, including a verification-aware prior-work baseline.
- Tool Contract Matrix executes 40 trials per method per readback/idempotency contract.
- Online recovery selection does not consume forked-state counterfactual outcomes; those replays are analysis-only.
- Raw run logs and generated summaries are included.
- Deterministic signature-output hashes are stable across repeated same-seed runs.
- One-command release audit verifies manifest, tests, and signature studies.
- Optional Chromium adapter, original microbenchmark, and a harder effect-semantics suite exercise the same recovery contract through a real browser DOM.
- Provider-neutral policy boundary is replay-tested and can bridge to an external model wrapper via JSON stdin/stdout without adding vendor credentials to the core repo.

## Current empirical status

**Mechanism validation only.** The core suite is deterministic; an optional real-Chromium DOM microbenchmark now verifies the same runtime contract across a browser-process/DOM boundary. The planner remains deterministic and the external effect ledger remains local, so this still does not establish frontier-model, production, or SOTA performance.

## Next hard gate

Model-backed browser/desktop evaluation where effect semantics must be inferred from realistic screenshots/DOM/tool responses rather than a deterministic planner. The experiment should factor model, harness, and tool contract, because 2026 evidence shows all three can materially affect exactly-once and recovery behavior.


## Bugs found by adversarializing the study

1. Ownership-naive compensation could retract another actor's valid update; fixed with actor/effect ownership.
2. Local rewind incorrectly rewound server-side idempotency state; fixed by keeping the deduplication registry in the external rollback domain.
3. Early simulator selection consumed forked-state counterfactual outcomes; fixed by separating online policy selection from offline replay analysis.

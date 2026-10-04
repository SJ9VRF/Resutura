# Evidence ledger

This file separates executed evidence from research targets.

## Executed in this release

- 43 automated tests pass.
- Clean deterministic multi-app workflow executes end-to-end.
- Forked-state counterfactual repair candidates execute when feasible **for analysis only**; their observed outcomes are not used for online policy selection.
- Checkpoint restoration intentionally preserves committed external effects and server-side idempotency state.
- Effect ledger tracks agent/external ownership, compensation status, operation IDs, and publication counts.
- Ambiguous-commit tests cover visible and unobservable commit outcomes.
- Compensable-misdirection test: Resutura retracts the agent-owned wrong effect and applies the intended effect.
- Concurrent-valid-change test: another actor's external update is preserved during compensation.
- Non-compensatable test: Resutura safe-aborts rather than claiming successful recovery.
- Effect Semantics Suite: 40 trials per method per scenario for Base, Retry, Verification-Aware, Rewind, and Resutura.
- Tool Contract Matrix: 40 trials per method for readback-only, idempotency-only, both, and neither under an unobservable ambiguous commit.
- Raw large-run evidence is included as gzip-compressed JSON in `runs/*.json.gz`; small demo traces remain plain JSON/HTML.
- Generated summaries include Effect Semantics, Tool Contract Matrix, formal component ablations, and statistical/uncertainty accounting.
- Public mechanism dataset release contains 160 scenario/task items and 800 raw trajectories with schema + source hash.
- Claim-to-evidence hashes are recorded in `docs/CLAIM_EVIDENCE_MAP.md`.

## Measured deterministic results

- compensable misdirection: Resutura 100% task success; Base/Retry/Verify/Rewind 0%;
- ambiguous commit with default readback/non-idempotent contract: Base 100%, Verify 100%, Resutura 100%, Retry/Rewind 0%; Retry/Rewind duplicate the intended effect in 100% of trials;
- concurrent valid change + misdirection: Resutura 100% task success and 0% protected-external loss;
- non-compensatable misdirection: all methods 0% task success; Resutura 100% safe abort;
- readback-only contract: Verification-Aware and Resutura resolve unobservable ambiguity without replay;
- idempotency-only contract: Retry, Verification-Aware, Rewind, and Resutura all achieve exactly-once ground-truth task completion in this simulator;
- neither readback nor idempotency: Retry/Rewind duplicate; Verification-Aware and Resutura safe-abort; Base leaves the external world correct only because it does not replay and has no evidence of the commit.

## Bugs discovered by stronger evaluation

- ownership-naive compensation could retract a concurrent actor's valid effect;
- checkpoint restore incorrectly rewound server-side idempotency state;
- an earlier online selector consumed simulator counterfactual outcomes and therefore had oracle leakage.

A fourth issue was also fixed: offline counterfactual analysis originally lacked support for `exists` postconditions, which could mark a successful diagnostic repair as unsuccessful. All four are fixed and regression-tested.

## Not executed / not established

- OSWorld, BrowserGym, WebArena, or comparable real CUA benchmark result;
- frontier-model comparison;
- live third-party side effects;
- delayed visibility / long in-flight commits beyond the current diagnostic abstraction;
- authorization-token or approval reconstruction attacks;
- calibrated model-based effect classifier;
- human preference study;
- SOTA;
- peer review or conference acceptance.

## Promotion rule

A result may become an unlabeled homepage/resume claim only when the release contains its task-suite version, exact model/harness/tool configuration, raw trajectories, grading contract, repeated-trial protocol, uncertainty, and relevant contemporary baselines.

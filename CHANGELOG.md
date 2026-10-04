## 1.2.0

- added a single-source project metadata contract and cross-artifact consistency verifier;
- added owner-level code walkthrough, reproduction matrix, review paths, and open research roadmap;
- fixed stale release/test-count wording and release target drift;
- extended the related-work boundary with security-context composition and state-grounded CUA verification;
- preserved authentic Git history by committing this hardening pass rather than backfilling prior development.

## 1.2.0

- added an Evidence Layer with a 12-entry experiment journal, 12 documented failures/false starts, 10-decision log, executed eval tables, unexpected findings, and raw-artifact indexes;
- added an “Inside the research process” layer to the flagship homepage without changing the 14-section public structure;
- added explicit authentic-Git-history policy: no pre-v1.0 commit history is fabricated; post-import Evidence Layer work is preserved as a real Git bundle;
- added Evidence Layer regression tests and public links to reproduction/failure/decision artifacts.

## 1.0.0

- public-research release: deterministic archive builder, claim-evidence verifier, Make targets, citation/governance metadata, and design-decision record;
- removed Python cache/build residue from packaged releases;
- normalized public wording from “prototype” to “research release” without broadening empirical claims;
- added hiring/reviewer one-page artifacts and release-readiness checks.

## 0.9.0
- Added formal component ablation suite (`− compensation`, `− contract awareness`, `− effect ownership`).
- Added machine-readable dataset release with 160 public diagnostic items and 800 trajectories.
- Added uncertainty/statistical report and paired-seed contrasts with explicit interpretation limits.
- Added actual failure gallery, benchmark card, and one-command core-evidence reproduction.
- Fixed offline counterfactual `exists` predicate evaluation; added regression test.
- Expanded release tests to 43.

## 0.8.1
- Added provider-neutral policy bridge and replay harness.
- Added real-Chromium effect-semantics suite.
- Fixed stateful perturbation reuse benchmark bug and browser concurrent-state grader mismatch.
- Preserved explicit non-model-backed claim boundary.

# 0.6.0
- Added optional real-Chromium environment and mechanism microbenchmark.
- Added browser integration test and explicit evidence-tier labeling.
- Unified package/release version metadata at 0.6.0.
- Updated experiment registry and reviewer docs.

# Changelog

## 0.5.0 - auditability and evidence provenance, September 26, 2026

- added machine-readable experiment registry with paired seed policies and claim classes;
- added source-code fingerprints to the signature experiment outputs;
- added one-command artifact audit (`scripts/audit_release.py`);
- added a five-minute hiring-manager/reviewer path;
- added explicit threat model and recovery invariants;
- documented the statistical interpretation limit of deterministic simulator repetitions;
- added release-metadata tests and removed cache/build residue from the shipped archive.


## 0.3.0 - effect-semantics hardening, September 25, 2026

- expanded literature audit to include transactional runtimes, compensation, non-atomic verification, rollback-reflection, replay safety, reversibility theory, and exactly-once work;
- narrowed public positioning from generic rollback-boundary recovery to effect-semantic recovery for computer-use agents;
- added explicit publication counts and duplicate-effect grading;
- added ambiguous-commit failure with verify-before-retry recovery;
- added external effect ownership and protected concurrent state;
- added non-compensatable effects and explicit safe-abort semantics;
- fixed a compensation bug uncovered by concurrent external state: recovery now selects agent-owned unreconciled effects instead of the first non-target effect;
- added Effect Semantics Suite with four diagnostic scenarios and four baselines;
- added duplicate-effect, protected-state-loss, and safe-abort metrics;
- expanded tests from 12 to 15;
- updated CI, release checks, paper, project page, evidence ledger, novelty audit, reviewer guide, and real-world falsification protocol;
- retained negative/awkward results (including Base success under ambiguous commit and zero task success for non-compensatable effects) instead of optimizing the presentation around a win rate.

## 0.2.0 - state-preserving recovery

- added external-effect ledger and forward compensation;
- made checkpoint restore preserve committed external effects;
- added Rewind baseline and external-effect reconciliation study;
- expanded recovery certificates and evidence boundaries.

## 0.1.0

Initial deterministic recovery kernel and causal-repair prototype.


## Research-hardening pass - tool-contract factorization
- Added `EffectContract` with explicit readback, idempotency, and compensation capabilities.
- Added unobservable ambiguous-commit fault and Tool Contract Matrix.
- Added strong Verification-Aware baseline.
- Separated online recovery selection from oracle-like forked counterfactual analysis.
- Fixed rollback-domain bug that incorrectly rewound server-side idempotency state.
- Added tests covering readback-only, idempotency-only, neither-capability, and baseline behavior.

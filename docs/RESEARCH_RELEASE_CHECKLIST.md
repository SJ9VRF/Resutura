# Research release checklist

## Implemented / machine-checked

- [x] Installable Python package and CLI
- [x] Deterministic environment with reset/grade/export/import
- [x] Explicit expected postconditions
- [x] Online verifier
- [x] Failure diagnosis contract
- [x] Counterfactual recovery evaluation on forkable state
- [x] Progress-preserving recovery utility
- [x] Checkpoint manager
- [x] Explicit rollback-boundary semantics
- [x] External-effect ledger
- [x] Forward-compensation recovery path
- [x] Repair certificate with protected-invariant verification
- [x] Base / retry / rewind / Resutura baselines
- [x] Perturbation engine
- [x] External-effect reconciliation mechanism study
- [x] Tests and CI
- [x] Evidence ledger and public-claim contract
- [x] Related-work/novelty audit
- [x] Paper draft and project site

## Required before a strong empirical paper claim

- [ ] Real browser/desktop side-effect environments
- [ ] Multiple current model backends
- [ ] RCA/reexecution and contemporary harm-recovery baselines implemented faithfully
- [ ] Ambiguous-commit cases
- [ ] Non-compensatable effects + safe escalation
- [ ] Concurrent external writers
- [ ] Held-out task/effect families
- [ ] Repeated trials and statistical testing
- [ ] Human calibration where deterministic grading is insufficient
- [ ] Cost/latency accounting from real calls
- [ ] Reproducible public benchmark release

Unchecked items are intentionally not fabricated by this repository.

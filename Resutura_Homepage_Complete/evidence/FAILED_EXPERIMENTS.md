# What Didn't Work

These are not decorative “failure examples.” They are the actual failed assumptions, evaluator bugs, implementation mistakes, and research-framing pivots that changed the project. None are retroactively presented as successful hypotheses.

## FAIL-001 — Online counterfactual selector used realized fork outcomes

**Type:** Methodology

**What failed**  
The early selector evaluated candidate repairs on forked simulator state and consumed the observed outcomes. That is an oracle unavailable to a real online agent.

**What changed**  
Separated online selection from offline analysis. Counterfactual outcomes remain logged but `used_for_policy_selection=false`.

**Evidence / record**  
[`docs/CLAIM_EVIDENCE_MAP.md`](../../docs/CLAIM_EVIDENCE_MAP.md)

## FAIL-002 — Ownership-naive compensation could delete another actor's valid change

**Type:** Recovery logic

**What failed**  
The first compensation rule looked for a non-target effect rather than an agent-owned unreconciled effect. Under concurrent valid state it could retract the wrong publication.

**What changed**  
Added actor/effect ownership to the external ledger and regression tests for protected concurrent state.

**Evidence / record**  
[`artifacts/generated/ABLATION_RESULTS.md`](../../artifacts/generated/ABLATION_RESULTS.md)

## FAIL-003 — Local rewind incorrectly rewound server-side idempotency state

**Type:** State model

**What failed**  
The first checkpoint implementation treated the deduplication registry as local state. Rewind therefore erased a server guarantee and made Rewind look worse than it should under idempotency.

**What changed**  
Moved the idempotency registry into the external rollback domain.

**Evidence / record**  
[`artifacts/generated/TOOL_CONTRACT_MATRIX.md`](../../artifacts/generated/TOOL_CONTRACT_MATRIX.md)

## FAIL-004 — Browser grader accepted duplicate intended publications

**Type:** Evaluation

**What failed**  
The first browser grader only checked whether the intended publication existed. A retry could publish twice and still be marked successful.

**What changed**  
Changed success to require exactly-once publication count and no unreconciled agent-owned wrong effect.

**Evidence / record**  
[`docs/BROWSER_MICROBENCH.md`](../../docs/BROWSER_MICROBENCH.md)

## FAIL-005 — Stateful perturbation objects were reused across methods

**Type:** Evaluation harness

**What failed**  
A perturbation carried `consumed=True`; reusing the object meant the first method saw the fault and later methods could get a clean run.

**What changed**  
Rebuild immutable fault specs into fresh perturbation instances for every method/scenario/trial.

**Evidence / record**  
[`CHANGELOG.md`](../../CHANGELOG.md)

## FAIL-006 — Concurrent-state browser grader treated valid external work as damage

**Type:** Evaluation

**What failed**  
The grader initially rejected any extra publication, even if it belonged to another actor and should be preserved.

**What changed**  
Grade only unreconciled agent-owned wrong effects; protected concurrent state is allowed and checked for loss.

**Evidence / record**  
[`artifacts/generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md`](../../artifacts/generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md)

## FAIL-007 — Repeated Playwright start/stop caused unstable EPIPE behavior

**Type:** Systems

**What failed**  
The first Chromium harness repeatedly created and tore down browser processes and was unstable in the execution environment.

**What changed**  
Reuse a browser process with explicit lifecycle instead of disposable browser creation per trial.

**Evidence / record**  
[`docs/BROWSER_MICROBENCH.md`](../../docs/BROWSER_MICROBENCH.md)

## FAIL-008 — Offline counterfactual evaluator lacked `exists` predicate support

**Type:** Analysis

**What failed**  
Some successful repairs were logged as `observed_success=false` in offline diagnostics even though online recovery was correct.

**What changed**  
Added `exists` predicate evaluation and a regression test; regenerated ablation/dataset evidence.

**Evidence / record**  
[`artifacts/generated/ABLATION_RESULTS.md`](../../artifacts/generated/ABLATION_RESULTS.md)

## FAIL-009 — Gzip evidence archives were not byte-stable by default

**Type:** Reproducibility

**What failed**  
Default gzip headers can include build time, so identical JSONL content could hash differently across exports.

**What changed**  
Write gzip with deterministic `mtime=0` and verify two exports have identical SHA-256.

**Evidence / record**  
[`docs/OFFLINE_REPRODUCIBILITY.md`](../../docs/OFFLINE_REPRODUCIBILITY.md)

## FAIL-010 — “Fast” audit still reran expensive experiment suites

**Type:** Release engineering

**What failed**  
The first `--fast` path could hit environment timeouts because it repeated heavy studies.

**What changed**  
Split fast integrity audit (manifest/tests/hashes/metadata) from full experiment reproduction.

**Evidence / record**  
[`docs/PUBLIC_RELEASE_CHECKLIST.md`](../../docs/PUBLIC_RELEASE_CHECKLIST.md)

## FAIL-011 — Clean-shell experiment entrypoints initially depended on working-directory imports

**Type:** Packaging

**What failed**  
Scripts worked in the development environment but failed when launched from a clean shell before packaging was corrected.

**What changed**  
Normalized package entrypoints and verified editable install from clean extracted releases.

**Evidence / record**  
[`CHANGELOG.md`](../../CHANGELOG.md)

## FAIL-012 — Causal-minimal-repair positioning overlapped 2026 related work

**Type:** Research framing

**What failed**  
An earlier framing treated causal minimal repair as the headline novelty. Literature audit showed direct overlap with contemporary work.

**What changed**  
Narrowed the project to effect-semantic recovery conditioned on realized state and tool-contract guarantees.

**Evidence / record**  
[`docs/NOVELTY_AND_POSITIONING.md`](../../docs/NOVELTY_AND_POSITIONING.md)


# Resutura - novelty and positioning audit

**Aura Yavary · September 26, 2026**

## Bottom line

The project is interesting, but the surrounding 2026 research area is crowded. A credible release must not sell common recovery mechanisms as novel.

### Already covered by adjacent work

- causal attribution and minimal counterfactual repair;
- CUA root-cause diagnosis and corrective re-execution;
- checkpoint/rewind with retained knowledge;
- compensation logs and transactional agent runtimes;
- idempotency and replay-resistant action execution;
- verification-aware handling of non-atomic failures;
- reversibility taxonomies including reversible, compensable, and irreversible actions;
- ambiguous-commit / exactly-once analyses;
- staged external effects and semantic transactions.

Resutura treats these as foundations and baselines, not inventions.

The September 26 audit also adds two especially relevant boundaries: **Safety Invariants for Agents Orchestrating Irreversible State Transitions** formalizes execution fidelity for irreversible external writes under ambiguity/retry faults, and **Human-Guided Harm Recovery / BackBench** formalizes preference-aligned recovery after harmful CUA states. Resutura therefore does not claim generic irreversible-effect safety, execution-fidelity guarantees, or the invention of harm recovery.

## Current contribution hypothesis

Resutura asks a narrower CUA-specific question:

> Can one recovery runtime select **different recovery semantics from realized effect state** while preserving already-valid progress?

The controller must distinguish:

- **verified commit**: do not replay;
- **compensable wrong effect**: reconcile forward;
- **concurrent valid external state**: preserve it during repair;
- **non-compensatable effect**: stop/escalate rather than fabricate recovery;
- **purely local reversible failure**: local repair or rewind remains appropriate.

The claim is therefore not "compensation is new" or "rollback boundaries are new." The research object is the **recovery decision boundary across effect semantics in long-horizon computer-use execution**.

## Effect Semantics Suite

The deterministic release contains four effect diagnostics, 40 trials per method per scenario, and now includes a Verification-Aware baseline specifically to avoid claiming known verify-before-retry behavior as novel:

| Scenario | Base | Retry | Verify | Rewind | Resutura |
|---|---:|---:|---:|---:|---:|
| compensable misdirection | 0% | 0% | 0% | 0% | 100% |
| ambiguous commit | 100% | 0% | 100% | 0% | 100% |
| concurrent valid change + misdirection | 0% | 0% | 0% | 0% | 100% |
| non-compensatable misdirection | 0% | 0% | 0% | 0% | 0% task success; 100% safe abort |

Important interpretation points:

- Base's ambiguous-commit success is a deliberate counterexample: no retry happens, so there is no duplicate. This is not evidence Base has a good recovery policy.
- Retry/Rewind duplicate the intended external effect after a lost acknowledgement in this simulator.
- Resutura's concurrent-change test previously exposed a real implementation bug: naive compensation selected the first non-target publication, which could be another actor's valid update. The fixed controller selects agent-owned uncompensated effects from the effect ledger.
- Non-compensatable failure is not converted into fake "success." The correct runtime behavior is explicit safe abort.

## What would make this a strong paper

The simulator is only a contract test. A paper-level contribution needs an executable real-browser/desktop suite in which effect semantics are not handed to a toy controller for free.

The strongest experiment would separate three sources of reliability:

1. **model** - can the model infer what happened and choose an appropriate action?
2. **harness/runtime** - does the controller verify, preserve, compensate, or stop correctly?
3. **tool contract** - are idempotency keys, status/read-back, compensation, and authorization semantics available?

Factorially varying those layers would make the work much harder to dismiss as a simulator trick.

## Falsification criteria

The research hypothesis should be considered unsupported if, on real CUA tasks:

- a simpler verify-before-retry wrapper matches Resutura across effect classes;
- transactional/staged-effect baselines dominate without sacrificing completion;
- the effect classifier cannot reliably distinguish ambiguous, compensable, and non-compensatable cases;
- progress-preservation gains disappear under concurrent writers;
- safe abort is badly calibrated and frequently blocks recoverable tasks;
- improvements come only from hand-authored environment labels unavailable to real agents.

## SOTA rule

Do not use "SOTA" unless a dated real-world evaluation beats current relevant baselines on a preregistered primary metric with repeated trials and uncertainty. The bundled results do not meet that bar.


## Tool-contract factorization

The release also varies two tool capabilities that contemporary work shows are decisive under ambiguous writes: authoritative readback and idempotency. The result is intentionally non-dominating. Readback lets the Verification-Aware baseline match Resutura on ambiguous commit; idempotency lets blind Retry and Rewind recover without duplication; with neither, there is no general exactly-once resolution from a lost acknowledgement, so conservative safe abort is preferable to blind replay.

This is a feature of the research design, not a weakness: the project hypothesis is **conditional** on what the tool contract exposes. Any real-world paper must report model x harness x tool-contract interactions rather than attributing all reliability gains to Resutura.

## Anti-oracle rule

Forked-state counterfactual execution is useful for post-hoc simulator analysis, but using its observed outcomes to select an online repair would leak privileged simulator state. The current runtime selects online recovery from observable state plus declared tool capabilities only. Counterfactual replays are logged with `used_for_policy_selection=false`.

## September 26 refresh: interface semantics are prior art

Agent-First Tooling (AFT-Bench) now directly studies interface mechanisms for execution lifecycle, explicit external-effect semantics, and postcondition verification. LIMBO further shows that exactly-once reliability can be dominated by the tool contract rather than the harness for unobservable failures. Therefore Resutura must not sell "effect semantics" or "tool-contract awareness" alone as novelty.

The remaining contribution hypothesis is the **decision policy across heterogeneous effect classes**—including ownership-sensitive forward compensation, preservation of concurrent valid state, local reversible repair, verified continuation, and safe refusal—under a common CUA recovery contract. The included Chromium microbenchmark is only adapter-level mechanism evidence; the claim still requires model-backed real-browser evaluation.


### September 27 boundary refresh
CONTINUITY (arXiv:2609.05269) makes security-context continuity and consequence-integrity contracts an explicit neighboring direction; StateAct (arXiv:2607.22798) shows that program-state grounding and independent finish verification can materially improve long-horizon CUAs. Resutura therefore does not claim generic consequence integrity or state-grounded verification as novelty. Its hypothesis remains narrower: choosing recovery semantics after consequential actions under realized effect state and explicit tool-contract capabilities.

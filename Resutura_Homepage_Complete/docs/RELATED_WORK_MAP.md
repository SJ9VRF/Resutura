# Related-work map

**Aura Yavary · updated September 26, 2026**

This file exists to prevent novelty inflation.

| Work / line of work | What it already covers | What Resutura must not claim |
|---|---|---|
| CausalFlow (2026) | causal attribution, counterfactual repair, minimal repair | inventing causal/minimal repair |
| CUADebug (2026) | CUA root-cause localization and corrective re-execution | inventing CUA diagnosis + repair |
| AgentRewind (2026) | checkpoint/rewind for long-horizon agents | inventing rewind |
| Rollback-Induced Reflection (2026) | choosing rollback/resume boundaries while retaining useful knowledge | generic rollback-boundary control |
| Robust Agent Compensation (2026) | log-based compensation recovery for agent frameworks | inventing compensation logs |
| Atomix (2026) | transactional tool use, progress-aware commit, compensation | inventing transactional compensation |
| Cordon (2026) | semantic transactions and staged irreversible effects | inventing task-level effect boundaries |
| ACRFence (2026) | semantic rollback attacks and irreversible-effect recording | inventing replay-safe restore semantics |
| Verified Tool Calls (2026) | postcondition verification, verify-before-retry, idempotency under non-atomic failure | inventing verify-before-retry |
| Revisable by Design (2026) | idempotent/reversible/compensable/irreversible taxonomy | inventing reversibility classes |
| LIMBO / exactly-once work (2026) | lost acknowledgements, late commits, idempotency and duplicate effects | inventing ambiguous-commit analysis |
| Safety Invariants for Agents Orchestrating Irreversible State Transitions (2026) | execution-fidelity invariants for irreversible external writes under retries, ambiguity, and delegated callers | inventing generic irreversible-effect safety or execution-fidelity invariants |
| Human-Guided Harm Recovery / BackBench (2026) | preference-aligned post-harm recovery for computer-use agents and a 50-task recovery benchmark | inventing harm recovery or human-preference recovery evaluation |
| Universal Verifier / CUA verifier work (2026) | process/outcome verification for CUA trajectories | inventing state-based verification |

## Current gap hypothesis

Resutura is positioned as an **integrated CUA recovery controller and diagnostic suite** that forces one runtime to make qualitatively different choices based on realized effect state:

- verify and continue after an ambiguous but already-successful commit;
- compensate an agent-owned wrong effect;
- preserve concurrent valid external changes;
- refuse to fake recovery for non-compensatable effects;
- still use ordinary local repair/rewind when the fault is inside the reversible domain.

That is a narrower claim than earlier versions of the project and should remain phrased as a hypothesis until real CUA experiments support it.

## September 26 literature refresh

| Work | Relevant result | Consequence for Resutura positioning |
|---|---|---|
| Agent-First Tooling / AFT-Bench (2026) | explicitly studies whether interfaces expose action-relevant execution lifecycle, external-effect semantics, and postcondition verification | Resutura must not claim that exposing effect semantics to agents is itself novel |
| LIMBO / Where Does Exactly-Once Live? (Sep. 24, 2026) | factorially separates model, harness, and tool-contract effects across 25,930 episodes; shows idempotency dominates several unobservable failure modes | real evaluation must factor tool contracts and cannot attribute exactly-once behavior to the recovery runtime alone |
| Bonded Recourse (Sep. 2026) | handles residual harm/settlement after compensable agent side effects across organizational boundaries | Resutura is not a general theory of post-harm recourse or cross-organization settlement |

The current defensible hypothesis is therefore narrower: a CUA runtime that **selects among effect-specific recovery semantics and preserves unrelated valid state**, evaluated under explicitly varied interface/tool capabilities.

| CONTINUITY (Sep. 2026) | security-context contracts and consequence integrity across composed agent controls | claiming generic end-to-end authorization/consequence-integrity guarantees |
| StateAct (Jul. 2026) | program-state grounding and independent finish verification for long-horizon CUAs | claiming that state-grounded verification itself is novel |

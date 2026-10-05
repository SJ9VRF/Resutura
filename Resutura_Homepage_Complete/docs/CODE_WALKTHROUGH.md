# Code Walkthrough — Resutura

This is the shortest path for a technical reviewer who wants to inspect the implementation rather than read the paper.

## 1. Start at the execution loop

`resutura/agent.py` contains the baseline agents and `ResuturaAgent`.

Trace one consequential action through:

1. proposal from `WorkflowPlanner` or a `PolicyProvider`;
2. optional checkpoint before a consequential action;
3. environment execution;
4. postcondition verification;
5. failure diagnosis;
6. effect-semantic recovery selection;
7. recovery execution;
8. certificate generation;
9. final world-state grading.

The critical invariant is that **local checkpoint restore does not erase committed external effects**.

## 2. Inspect the rollback boundary

Open `resutura/envs/sandbox.py`:

- `execute()` mutates both reversible task state and committed external state;
- `export_state()` exposes the joint state for analysis;
- `restore_checkpoint_state()` restores reversible state while explicitly preserving publications, publication counts, the effect ledger, protected external targets, and server-side idempotency state;
- `grade()` checks exactly-once intended publication, absence of unreconciled agent-owned wrong effects, and preservation of protected external state.

This file is the fastest place to understand the project thesis in code.

## 3. Inspect verification

`resutura/verifier.py` checks expected postconditions against realized observations. `resutura/state.py` owns predicate evaluation.

The important distinction is between:

- a failed call result;
- an unverified effect;
- an effect that actually committed;
- an effect that committed to the wrong target.

These are not interchangeable states.

## 4. Inspect diagnosis and recovery semantics

`resutura/diagnoser.py` classifies divergence into a `FailureEvent`.

`resutura/recovery.py` then constructs candidate recovery semantics. The public claim is **not** that every candidate is novel. The contribution hypothesis is the decision boundary across effect classes and tool-contract capabilities.

Search for:

- `candidates()` — available recovery actions;
- `select()` — online selection;
- `empirical_counterfactuals()` — offline diagnostics only;
- `used_for_policy_selection` in traces/tests — guard against simulator-oracle leakage.

## 5. Inspect the policy/model boundary

`resutura/model_policy.py` defines the provider-neutral JSON request/response contract.

`resutura/policy_agent.py` lets an external or recorded policy propose task actions while Resutura retains verification and recovery semantics.

The bundled replay study is **not model-backed evidence**. A genuine model-backed study is intentionally left as the next hard gate.

## 6. Inspect the baselines

`resutura/agent.py` includes:

- `BaseAgent`;
- `RetryAgent`;
- `VerificationAwareAgent`;
- `RewindAgent`;
- `ResuturaAgent`.

The strongest sanity checks are the cases where simpler baselines should match Resutura:

- authoritative readback resolves ambiguous commit → Verify can match;
- idempotent tool contract → Retry/Rewind can become sufficient.

If Resutura claimed wins there, the benchmark would be suspect.

## 7. Inspect evidence generation

Use this order:

1. `experiments/effect_semantics_suite.py`
2. `experiments/tool_contract_matrix.py`
3. `experiments/ablation_suite.py`
4. `experiments/browser_effect_semantics.py`
5. `scripts/export_dataset.py`
6. `analysis/statistical_report.py`

Then compare generated summaries with `docs/CLAIM_EVIDENCE_MAP.md`.

## 8. Inspect adversarial regression tests

High-value tests include:

- ownership-aware compensation;
- server-side idempotency surviving local rewind;
- fresh perturbation objects per method;
- exactly-once browser grading;
- offline counterfactuals excluded from online selection;
- non-compensatable safe abort;
- dataset/release reproducibility.

Run `pytest -q` before trusting any generated result.

## 9. What to challenge in an interview

A reviewer should ask:

- Why is `restore_checkpoint_state()` defined this way?
- When is Verify strictly sufficient?
- How is actor ownership established and what if it is wrong?
- What evidence distinguishes compensation from destructive cleanup?
- What happens when the compensator itself fails?
- What changes with a real model that misclassifies effect state?
- Which conclusions survive if tool contracts are stronger than the runtime?

Those questions are intentionally not hidden by the project page.

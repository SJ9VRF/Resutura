# Real-world execution plan

## Objective

Test whether effect-semantic recovery improves real computer-use reliability when the runtime must infer realized effects from realistic observations and tool contracts.

## Factorized design

Vary three layers independently:

1. **Model** - at least one strong frontier CUA and one smaller/cheaper model.
2. **Harness** - Base, Retry, RCA+re-execution, Rewind/Reflection, verification-aware baseline, Resutura.
3. **Tool contract** - no read-back; read-back/status; idempotency key; compensator; staged/transactional effect where available.

This avoids attributing a tool-contract guarantee to the model or a model capability to the harness.

## Required task families

- lost acknowledgement after successful write;
- timeout before write;
- delayed visibility after write;
- duplicate delivery / redelivery;
- wrong-target but compensable write;
- non-compensatable write;
- concurrent legitimate external update;
- stale read followed by conflicting commit;
- authorization/approval state changed between proposal and execution;
- multi-app task with substantial valid progress before the fault.

## Grading

Use authoritative state whenever possible. Separate:

- task completion;
- exactly-once effect correctness;
- unreconciled agent-owned effects;
- protected concurrent-state loss;
- duplicate-effect rate;
- safe-abort correctness;
- recovery cost/latency;
- progress preserved after recovery.

Model-based graders may supplement quality judgments but must not be the sole oracle for committed external state.

## Statistical protocol

- paired fault injections from identical initial snapshots;
- repeated trials for stochastic agents;
- report Wilson or bootstrap intervals as appropriate;
- freeze primary metrics before full evaluation;
- retain negative results and failed recoveries;
- publish raw trajectories and effect ledgers subject to privacy/safety constraints.

## Stop conditions

Do not promote the work as stronger than a mechanism study if:

- the effect classifier relies on hidden simulator labels;
- a simple verify-before-retry wrapper matches performance;
- a transactional baseline dominates on completion and side-effect correctness;
- protected-state preservation fails under concurrent writers;
- safe-abort precision is too low for practical use.

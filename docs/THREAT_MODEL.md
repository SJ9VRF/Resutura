# Threat model and recovery boundary

Resutura is not a generic safety layer. It studies recovery after tool-mediated state changes. The runtime separates **local execution state** from **committed external state** and refuses to assume that restoring the former restores the latter.

## In scope

- lost or delayed acknowledgements after a commit;
- duplicate-delivery risk after retry;
- wrong-target but compensatable effects;
- concurrent legitimate changes owned by another actor;
- non-compensatable effects where the safest action is to stop;
- mismatches between local checkpoint state and external service state.

## Explicit invariants

1. Never remove an external effect merely because it is absent from a local checkpoint.
2. Never compensate an effect without ownership/effect-ledger evidence tying it to this agent run.
3. Preserve externally owned valid changes.
4. Verify realized state before replay when authoritative readback is available.
5. Respect declared idempotency instead of pretending the runtime must solve replay safety itself.
6. Safe-abort when correctness cannot be established without an unsupported assumption.

## Out of scope for the bundled evidence

- adversarial browser content and prompt injection;
- payment, medical, legal, or other high-stakes authorization semantics;
- human approval UX;
- malicious tools that lie about readback/idempotency guarantees;
- distributed transactions spanning independent production services;
- real-model inference of ownership, commit state, or compensatability from pixels.

These are real-world gates, not hidden assumptions. A production-facing evaluation must add them explicitly.

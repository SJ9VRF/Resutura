# Rewinding the Agent Is Not Rewinding the World

**Aura Yavary · Resutura**

Long-horizon agents are usually taught a familiar recovery reflex: if something goes wrong, retry, replan, or rewind. That works only when the environment behaves like the agent’s own scratchpad.

Real software does not.

A message can be sent even if the acknowledgement times out. A file can be published to the wrong destination. Another user can make a valid change while the agent is recovering. A local checkpoint can restore the agent’s memory without retracting the external action that already happened.

Resutura starts from one question: **what actually happened in the world?**

Instead of mapping every failure to the same recovery primitive, the runtime classifies the realized effect and selects among verification, local repair, rewind, forward compensation, preservation, or safe abort. The important part is not a larger recovery menu. It is the boundary: local state and external state are different objects with different reversibility.

The project’s strongest result is deliberately not a universal win. In ambiguous-commit tasks, a verification-aware baseline matches Resutura when authoritative readback is available. When the tool itself supplies idempotency, even simple Retry can become sufficient. Resutura’s extra machinery matters only where the failure requires effect reconciliation: wrong-target committed actions, ownership-sensitive compensation, concurrent valid state, or an explicit recognition that no safe repair exists.

That non-result is part of the design. A recovery system should not claim credit for guarantees supplied by the tool contract.

The current release contains a deterministic semantics suite, a real-Chromium mechanism tier, a provider-neutral policy boundary, raw trajectories, tests, and an evidence ledger. It does not claim frontier-model superiority or SOTA performance. The next gate is model-backed evaluation in realistic computer-use environments.

The broader thesis is simple: **a failed tool result does not tell you whether to retry. The realized world state does.**

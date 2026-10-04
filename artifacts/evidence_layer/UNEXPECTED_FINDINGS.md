# Unexpected Findings

These findings changed the project more than a clean “+X%” result would have.

1. **Base can look perfect on an ambiguous commit by doing nothing.** The world is already correct after the lost acknowledgement, so a non-retrying agent scores 100% despite having no knowledge that the commit succeeded. This forced us to separate world-state correctness from epistemic confidence.

2. **A strong Verification-Aware baseline ties Resutura on ambiguous commit.** Once authoritative readback exists, special recovery machinery is unnecessary for this class. This narrowed the novelty claim.

3. **Idempotency can erase most runtime differences.** Under an idempotency-only contract, Retry, Verify, Rewind, and Resutura all reach 100% in the deterministic matrix. Tool design can matter more than harness sophistication.

4. **Rewind can make ambiguous commits worse.** Resetting local state while the external commit persists encourages duplicate replay unless the tool contract protects against it.

5. **More recovery is not always better.** The correct outcome for a non-compensatable committed error is 0% task completion and 100% safe abort. A benchmark that rewards forced completion would incentivize harm.

6. **Concurrent valid state broke naive compensation.** The first compensation heuristic could retract another actor's valid effect. Ownership turned out to be a semantic requirement, not metadata decoration.

7. **The evaluator was a bigger risk than the agent in several iterations.** Fault-object reuse, duplicate-accepting grading, and concurrent-state grading each could have produced optimistic conclusions. The benchmark had to be adversarialized before the method could be trusted.

8. **Byte-level reproducibility exposed release bugs that metric-level reproducibility would miss.** Random IDs, wall-clock timestamps, and gzip headers made identical studies hash differently until the release path was hardened.

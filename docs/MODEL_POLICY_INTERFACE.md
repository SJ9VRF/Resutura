# Model / policy integration boundary

**Status:** implemented interface, replay-tested; no frontier model was executed in this release.

## Why this exists

Recovery research should not be entangled with one model vendor or SDK. Resutura therefore separates **action policy** from **recovery runtime**. A policy proposes a task action and explicit expected postconditions; the runtime executes, verifies realized state, diagnoses divergence, and selects effect-semantic recovery.

## JSON request

A provider receives: task, current observation, declared effect contract (`readback`, `idempotency`, `compensation`), recent history, step index, and allowed action types.

## JSON response

A provider returns either `{"stop": true}` or a proposal containing an action, intent, expected postconditions, risk, reversibility, and subgoal. Unknown action types are rejected.

## Providers

- `RecordedPolicyProvider`: deterministic offline replay. This is evidence about the **interface**, not about model capability.
- `CommandPolicyProvider`: invokes an external command with request JSON on stdin and expects response JSON on stdout. This keeps API keys and vendor dependencies outside the repo.

## Claim boundary

The presence of this interface does **not** make the current results model-backed. A genuine model study must record exact model/version, prompting/config, sampling parameters, raw policy outputs, request/response traces, costs/latency, paired seeds/snapshots, and the same baselines.

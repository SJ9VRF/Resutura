# Resutura architecture

Resutura separates **execution state** from **effect state**.

```text
Task / goal
   ↓
Planner → action + expected postconditions + risk/reversibility metadata
   ↓
Checkpoint reversible local state when appropriate
   ↓
Execute action
   ├── local state mutation
   └── optional committed external effect → effect ledger
   ↓
Observe joint state
   ↓
State-delta verifier
   ├── match → continue
   └── divergence
          ↓
      failure diagnosis
          ↓
      determine failure scope / rollback boundary
          ↓
      candidate recovery set
       ├ retry
       ├ local repair
       ├ subgoal reconstruction
       ├ forward compensation
       ├ checkpoint rewind
       ├ global replan
       └ safe abort
          ↓
      counterfactual evaluation when fork/replay is available
          ↓
      execute selected recovery
          ↓
      verify action postconditions + protected invariants + effect reconciliation
          ↓
      recovery certificate
```

## Critical semantic rule

A checkpoint may restore controlled local state. It must not be treated as proof that a remote/external side effect disappeared. Environment adapters should implement a rollback boundary explicitly.

## Current deterministic adapter

`ResearchWorkflowEnv` models local browser/spreadsheet/document state and a separate publication/effect ledger. Its checkpoint restore preserves committed publications, while full fork/import used for counterfactual analysis can clone complete simulator state.

## Extension points

- `EnvironmentAdapter`: observation, action execution, snapshots, outcome grading, effect receipts;
- `ModelAdapter`: planning/diagnosis/replanning behind structured schemas;
- compensation catalog: domain-specific reverse/forward actions with preconditions;
- verifier: deterministic state checks first, semantic/model grading only when necessary;
- audit store: effect receipts, recovery certificates, costs, latency, and model metadata.

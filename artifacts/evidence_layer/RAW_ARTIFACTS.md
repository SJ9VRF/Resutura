# Raw Artifacts

```text
artifacts/
  experiment_logs/      # experiment-by-experiment journal
  eval_runs/             # canonical raw-run hashes and pointers
  failure_examples/      # failure-gallery entrypoint
  plots/                 # figure provenance policy
  configs/               # config/registry pointers
  qualitative_cases/     # trajectory/demo cases
  ablations/             # ablation summary + raw-run pointer
  evidence_layer/        # failures, decisions, real tables, findings
runs/                    # canonical raw JSON / JSON.GZ trajectories
```

No large raw run is duplicated under `artifacts/`; indexes point back to the canonical `runs/` copy and include hashes where relevant.

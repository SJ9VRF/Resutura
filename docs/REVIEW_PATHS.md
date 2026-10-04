# Review Paths

Different reviewers should not have to inspect the repository in the same order.

## Recruiter / hiring screen — 60 seconds

1. `artifacts/website/index.html`
2. `artifacts/recruiting/ONE_PAGE.md`
3. one result table + one failure trace

Question to answer: *Is there a coherent problem, an implemented method, and evidence that is scoped honestly?*

## Research hiring manager — 5 minutes

1. `docs/HIRING_MANAGER_BRIEF.md`
2. `docs/NOVELTY_AND_POSITIONING.md`
3. `artifacts/generated/ABLATION_RESULTS.md`
4. `artifacts/evidence_layer/UNEXPECTED_FINDINGS.md`
5. `docs/OPEN_RESEARCH_QUESTIONS.md`

Question to answer: *Is the contribution boundary defensible, and what would falsify it?*

## Research engineer / systems reviewer — 15 minutes

1. `docs/CODE_WALKTHROUGH.md`
2. `resutura/envs/sandbox.py`
3. `resutura/recovery.py`
4. `resutura/agent.py`
5. `tests/test_effect_semantics.py`
6. `tests/test_tool_contracts.py`
7. `docs/REPRODUCTION_MATRIX.md`

Question to answer: *Does the implementation match the research story?*

## Reproducibility reviewer

1. `PROJECT_METADATA.json`
2. `experiments/registry.json`
3. `docs/CLAIM_EVIDENCE_MAP.md`
4. `python scripts/verify_consistency.py`
5. `make fast-audit`

Question to answer: *Can the public claims be traced to versioned, hashed evidence without rerunning a hidden service?*

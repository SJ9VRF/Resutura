# Reviewer guide

This file is the fastest path through the repository.

## 1. Read the claim boundary first

- `docs/NOVELTY_AND_POSITIONING.md`
- `docs/RELATED_WORK_MAP.md`
- `docs/EVIDENCE_LEDGER.md`

If you believe the project overclaims novelty after reading those files, that is a release bug.

## 2. Reproduce the mechanism suite

```bash
python -m pip install -e .
pytest -q
python experiments/effect_semantics_suite.py
```

Expected diagnostic pattern:

- compensable misdirection: only Resutura reaches the intended final state;
- ambiguous commit: Base and Resutura complete, but Retry/Rewind duplicate the committed effect;
- concurrent valid change: Resutura repairs its own effect without deleting the protected external update;
- non-compensatable effect: Resutura safe-aborts instead of reporting recovery.

## 3. Inspect the implementation

- `resutura/envs/sandbox.py`: local vs committed external state and failure injection;
- `resutura/verifier.py`: postcondition verification;
- `resutura/diagnoser.py`: effect-state diagnosis;
- `resutura/recovery.py`: recovery candidates and selection;
- `resutura/agent.py`: execution/recovery loop and repair certificates.

## 4. Try to falsify it

The strongest criticism is not that a baseline fails in this simulator; it is that the simulator may encode too much privileged knowledge. The next real-world study must remove that privilege and test whether effect semantics can be inferred from realistic observations/tool contracts.

## 5. Do not cite simulator numbers as SOTA

They are contract tests. The project becomes a paper-level empirical result only after real CUA evaluation against current verification, rewind, compensation, and transactional baselines.


## Two reviewer checks added in the hardened release

1. **Does the policy rely on a simulator oracle?** No. Search `used_for_policy_selection`; forked counterfactual outcomes are diagnostic only.
2. **Is verify-before-retry being sold as novel?** No. Run `experiments/tool_contract_matrix.py`: the Verification-Aware baseline matches Resutura when readback alone solves ambiguous commit, and Retry/Rewind match it when idempotency alone solves replay safety.

from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_evidence_layer_core_artifacts_exist():
    required=[
        'artifacts/experiment_logs/README.md',
        'artifacts/evidence_layer/FAILED_EXPERIMENTS.md',
        'artifacts/evidence_layer/DECISION_LOG.md',
        'artifacts/evidence_layer/REAL_EVAL_TABLES.md',
        'artifacts/evidence_layer/UNEXPECTED_FINDINGS.md',
        'artifacts/evidence_layer/RAW_ARTIFACTS.md',
        'artifacts/git_history/README.md',
        'artifacts/git_history/COMMIT_LOG.txt',
        'artifacts/git_history/resutura-evidence-layer.bundle',
        'artifacts/eval_runs/README.md',
        'artifacts/ablations/README.md',
        'artifacts/qualitative_cases/README.md',
    ]
    for rel in required:
        assert (ROOT/rel).exists(), rel

def test_experiment_journal_is_structured_and_evidence_linked():
    journal=(ROOT/'artifacts/experiment_logs/README.md').read_text()
    assert journal.count('## EXP-') == 12
    for field in ['**Hypothesis:**','**Setup:**','**Result:**','**Interpretation:**','**Next decision:**','**Evidence:**']:
        assert journal.count(field) == 12

def test_failure_and_decision_logs_have_real_process_depth():
    failures=(ROOT/'artifacts/evidence_layer/FAILED_EXPERIMENTS.md').read_text()
    decisions=(ROOT/'artifacts/evidence_layer/DECISION_LOG.md').read_text()
    assert failures.count('## FAIL-') == 12
    assert decisions.count('## D-') == 10
    assert 'oracle' in failures.lower()
    assert 'idempotency' in failures.lower()
    assert 'safe abort' in decisions.lower()

def test_registered_study_counter_matches_registry():
    registry=json.loads((ROOT/'experiments/registry.json').read_text())
    assert len(registry['studies']) == 8
    index=(ROOT/'artifacts/evidence_layer/README.md').read_text()
    assert '**8** registered reproducible studies' in index

def test_git_history_policy_refuses_backfilled_history():
    text=(ROOT/'artifacts/git_history/README.md').read_text().lower()
    assert 'did **not** include authentic pre-v1.0 git metadata' in text
    assert 'does not fabricate' in text or 'do **not**' in text

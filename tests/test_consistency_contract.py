from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]

def test_consistency_verifier_passes():
    subprocess.run([sys.executable,'scripts/verify_consistency.py'],cwd=ROOT,check=True)

def test_reviewer_artifacts_exist():
    for rel in ['PROJECT_METADATA.json','docs/CODE_WALKTHROUGH.md','docs/REPRODUCTION_MATRIX.md','docs/OPEN_RESEARCH_QUESTIONS.md','docs/REVIEW_PATHS.md']:
        assert (ROOT/rel).exists(), rel

def test_metadata_evidence_counts_match_evidence_index():
    m=json.loads((ROOT/'PROJECT_METADATA.json').read_text())['evidence_layer']
    text=(ROOT/'artifacts/evidence_layer/README.md').read_text()
    assert f'**{m["journal_entries"]}** documented experiment' in text
    assert f'**{m["documented_failures"]}** documented failed' in text
    assert f'**{m["major_decisions"]}** major design decisions' in text

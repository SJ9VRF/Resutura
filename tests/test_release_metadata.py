import json
from pathlib import Path
from resutura.provenance import source_fingerprint

ROOT=Path(__file__).resolve().parents[1]

def test_experiment_registry_has_real_world_claim_boundary():
    r=json.loads((ROOT/"experiments/registry.json").read_text())
    assert r["release"] == "1.2.0"
    assert "SOTA" in r["forbidden_claims"]
    assert all(s["paired"] for s in r["studies"])

def test_source_fingerprint_is_stable_shape():
    x=source_fingerprint(ROOT)
    assert len(x)==64 and all(c in "0123456789abcdef" for c in x)

def test_no_legacy_phoenix_brand_in_public_markdown():
    for p in [ROOT/"README.md", ROOT/"PROJECT_STATUS.md", ROOT/"docs/HIRING_MANAGER_BRIEF.md"]:
        assert "Phoenix" not in p.read_text()

from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_public_release_files_present():
    for rel in ['CITATION.cff','CONTRIBUTING.md','SECURITY.md','Makefile','docs/DESIGN_DECISIONS.md','docs/PUBLIC_RELEASE_CHECKLIST.md','artifacts/recruiting/ONE_PAGE.md','artifacts/recruiting/RESUME_CLAIMS.md']:
        assert (ROOT/rel).exists(), rel

def test_version_is_1_0_0():
    import resutura
    assert resutura.__version__=='1.2.0'
    registry=json.loads((ROOT/'experiments/registry.json').read_text())
    assert registry['release']=='1.2.0'

def test_fast_audit_has_distinct_integrity_path():
    text=(ROOT/'scripts/audit_release.py').read_text()
    assert 'fast integrity path' in text
    assert 'full reproduction path' in text


def test_release_manifest_never_tracks_git_internals():
    import json
    manifest=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
    assert all(not row['path'].startswith('.git/') for row in manifest.get('files',[]))

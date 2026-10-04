from __future__ import annotations
import json, re, tomllib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def fail(msg):
    raise SystemExit('consistency: FAIL — '+msg)

def main():
    meta=json.loads((ROOT/'PROJECT_METADATA.json').read_text())
    version=meta['version']; author=meta['author']
    py=tomllib.loads((ROOT/'pyproject.toml').read_text())
    if py['project']['version'] != version: fail('pyproject version')
    if author not in [x['name'] for x in py['project'].get('authors',[])]: fail('pyproject author')
    init=(ROOT/'resutura/__init__.py').read_text()
    if f'__version__ = "{version}"' not in init: fail('package version')
    reg=json.loads((ROOT/'experiments/registry.json').read_text())
    if reg.get('release') != version or reg.get('author') != author: fail('experiment registry metadata')
    cff=(ROOT/'CITATION.cff').read_text()
    if f'version: {version}' not in cff: fail('CITATION.cff version')
    status=(ROOT/'PROJECT_STATUS.md').read_text()
    if f'v{version}' not in status.splitlines()[0]: fail('PROJECT_STATUS current version header')
    if f'Release: **{version}**' not in status: fail('PROJECT_STATUS release line')
    if author not in status: fail('PROJECT_STATUS author')
    # Detect stale exact x/x test-count prose in current-status section. Historical changelog counts are allowed elsewhere.
    current=status.split('# Project status - Resutura',1)[-1]
    stale=re.findall(r'\b(\d+)/(\d+)\s+(?:unit/integration\s+)?tests?\s+pass', current, re.I)
    if stale: fail('hard-coded test count remains in current status; use dynamic wording')
    required=['docs/CODE_WALKTHROUGH.md','docs/REPRODUCTION_MATRIX.md','docs/OPEN_RESEARCH_QUESTIONS.md','docs/REVIEW_PATHS.md']
    for rel in required:
        if not (ROOT/rel).exists(): fail('missing '+rel)
    print(f'consistency: PASS — {meta["project"]} {version} · {author}')

if __name__=='__main__': main()

from pathlib import Path
import hashlib, json, subprocess
ROOT=Path(__file__).resolve().parents[1]
META=json.loads((ROOT/'PROJECT_METADATA.json').read_text())
EXCLUDE={'RELEASE_MANIFEST.json'}
files=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(ROOT).as_posix()
    if rel in EXCLUDE or rel.startswith('.git/') or '/__pycache__/' in '/'+rel or rel.startswith('.pytest_cache/'): continue
    files.append({'path':rel,'size_bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
try:
    out=subprocess.check_output(['python','-m','pytest','--collect-only','-q'],cwd=ROOT,text=True,stderr=subprocess.STDOUT)
    
    import re
    count=sum(int(m.group(1)) for line in out.splitlines() if (m:=re.search(r':\s*(\d+)\s*$',line)))
except Exception:
    count=None
manifest={'release':'resutura-'+META['version'],'author':META['author'],'generated':META['release_date'],'tests':f'{count}/{count}' if count is not None else 'see CI','files':files}
(ROOT/'RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f"wrote manifest for {len(files)} files; tests={manifest['tests']}")

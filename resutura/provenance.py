from __future__ import annotations
import hashlib, platform, sys
from pathlib import Path

_SCHEMA_VERSION = "1.0"

def source_fingerprint(root: str | Path | None = None) -> str:
    root = Path(root) if root else Path(__file__).resolve().parents[1]
    targets = [root / "resutura", root / "experiments", root / "configs", root / "pyproject.toml"]
    h = hashlib.sha256()
    files=[]
    for t in targets:
        if t.is_file(): files.append(t)
        elif t.exists(): files.extend(p for p in t.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    for p in sorted(files, key=lambda x: str(x.relative_to(root))):
        rel=str(p.relative_to(root)).replace("\\","/")
        h.update(rel.encode()); h.update(b"\0"); h.update(p.read_bytes()); h.update(b"\0")
    return h.hexdigest()

def experiment_metadata(name: str, seed_policy: str, trials: int | None = None) -> dict:
    return {
        "schema_version": _SCHEMA_VERSION,
        "experiment": name,
        "source_fingerprint_sha256": source_fingerprint(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "seed_policy": seed_policy,
        "trials_declared": trials,
        "counterfactual_policy": "forked simulator outcomes are diagnostic only and never used for online policy selection",
    }


def write_json_gzip_deterministic(path: str | Path, obj) -> None:
    """Write stable gzip JSON (mtime=0, sorted keys) for hashable research evidence."""
    import gzip, io, json
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
            with io.TextIOWrapper(gz,encoding='utf-8',newline='\n') as f:
                json.dump(obj,f,indent=2,sort_keys=True); f.write('\n')


def read_json_gzip(path: str | Path):
    import gzip, json
    with gzip.open(Path(path),'rt',encoding='utf-8') as f:
        return json.load(f)

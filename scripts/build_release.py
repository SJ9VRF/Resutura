from __future__ import annotations
import argparse, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIXED=(2026,9,27,12,0,0)
SKIP_PARTS={'__pycache__','.pytest_cache','.git','build','dist','.mypy_cache','.ruff_cache'}
SKIP_SUFFIX={'.pyc','.pyo'}
def include(p:Path)->bool:
    rel=p.relative_to(ROOT)
    if any(x in SKIP_PARTS for x in rel.parts): return False
    if p.suffix in SKIP_SUFFIX: return False
    if p.name.endswith('~') or p.name in {'.DS_Store'}: return False
    return True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); args=ap.parse_args()
    out=Path(args.out).resolve(); out.parent.mkdir(parents=True,exist_ok=True)
    prefix='resutura/'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in ROOT.rglob('*') if x.is_file() and include(x)):
            rel=p.relative_to(ROOT).as_posix()
            zi=zipfile.ZipInfo(prefix+rel, date_time=FIXED)
            zi.compress_type=zipfile.ZIP_DEFLATED
            zi.external_attr=(0o644 & 0xFFFF)<<16
            z.writestr(zi,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(out)
if __name__=='__main__': main()

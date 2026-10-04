from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def sha256(p: Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def run(cmd):
    print("+", " ".join(map(str,cmd)), flush=True)
    subprocess.run(cmd,cwd=ROOT,check=True)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--fast",action="store_true"); args=ap.parse_args()
    manifest=json.loads((ROOT/"RELEASE_MANIFEST.json").read_text())
    bad=[]
    for row in manifest.get("files",[]):
        p=ROOT/row["path"]
        if not p.exists() or sha256(p)!=row["sha256"]: bad.append(row["path"])
    if bad:
        raise SystemExit("manifest mismatch: "+", ".join(bad[:10]))
    print(f"manifest: PASS ({len(manifest.get('files',[]))} files)")
    run([sys.executable,"-m","pytest","-q"])
    run([sys.executable,"scripts/verify_claim_map.py"])
    run([sys.executable,"scripts/verify_consistency.py"])
    if args.fast:
        print("artifact audit: PASS (fast integrity path)")
        return
    run([sys.executable,"experiments/effect_semantics_suite.py"])
    run([sys.executable,"experiments/tool_contract_matrix.py"])
    run([sys.executable,"experiments/policy_replay_smoke.py"])
    run([sys.executable,"experiments/ablation_suite.py"])
    run([sys.executable,"scripts/export_dataset.py"])
    run([sys.executable,"analysis/statistical_report.py"])
    run([sys.executable,"scripts/release_check.py"])
    run([sys.executable,"scripts/build_claim_map.py"])
    run([sys.executable,"scripts/verify_claim_map.py"])
    print("artifact audit: PASS (full reproduction path)")
if __name__=="__main__": main()

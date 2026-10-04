from pathlib import Path as _Path
import sys as _sys
_ROOT = _Path(__file__).resolve().parents[1]
if str(_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_ROOT))
from resutura.runner import run_experiment, save_json
if __name__ == "__main__":
    result=run_experiment(120,7,True)
    save_json(result,"runs/pilot.json")
    for k,v in result["agents"].items(): print(k,v["summary"])

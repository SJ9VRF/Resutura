from __future__ import annotations
import argparse, json
from pathlib import Path
from .agent import ResuturaAgent
from .envs.sandbox import ResearchWorkflowEnv, make_task
from .perturbations import PerturbationEngine, Perturbation
from .runner import run_experiment, save_json
from .viewer import build_viewer


def main(argv=None):
    p=argparse.ArgumentParser(prog="resutura")
    sp=p.add_subparsers(dest="cmd",required=True)
    d=sp.add_parser("demo"); d.add_argument("--out",default="runs/demo.json")
    e=sp.add_parser("experiment"); e.add_argument("--trials",type=int,default=120); e.add_argument("--seed",type=int,default=7); e.add_argument("--out",default="runs/experiment.json")
    v=sp.add_parser("viewer"); v.add_argument("--run",required=True); v.add_argument("--out",default="runs/viewer.html")
    args=p.parse_args(argv)
    if args.cmd=="demo":
        task=make_task(1,3)
        publish_step=4*len(task.papers)+5
        pe=PerturbationEngine([Perturbation("redirect_publish_target",publish_step)])
        run=ResuturaAgent().run(ResearchWorkflowEnv(),task,pe,7)
        save_json(run.to_dict(),args.out); print(json.dumps({"success":run.success,"recovered":run.recovered_failures,"out":args.out},indent=2))
    elif args.cmd=="experiment":
        obj=run_experiment(args.trials,args.seed,True); save_json(obj,args.out)
        print(json.dumps({k:v["summary"] for k,v in obj["agents"].items()},indent=2))
    elif args.cmd=="viewer":
        run=json.loads(Path(args.run).read_text()); build_viewer(run,args.out); print(args.out)

if __name__=="__main__": main()

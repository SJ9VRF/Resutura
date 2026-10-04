from __future__ import annotations
from pathlib import Path
import argparse, json
from resutura.envs.sandbox import make_task
from resutura.planner import WorkflowPlanner

def p2d(p):
    return {'proposal':{
        'action':{'type':p.action.type,'target':p.action.target,'value':p.action.value,'args':p.action.args},
        'intent':p.intent,
        'expected_postconditions':[{'key':x.key,'op':x.op,'value':x.value,'confidence':x.confidence,'critical':x.critical} for x in p.expected_postconditions],
        'risk':p.risk.value,'reversibility':p.reversibility,'subgoal':p.subgoal}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--task',type=int,default=0); ap.add_argument('--papers',type=int,default=3); ap.add_argument('--out',required=True)
    a=ap.parse_args(); task=make_task(a.task,a.papers); responses=[p2d(p) for p in WorkflowPlanner().build_plan(task)]+[{'stop':True,'rationale':'task plan complete'}]
    Path(a.out).write_text(json.dumps({'schema_version':'1','source':'deterministic planner fixture; not a model','task_id':task.task_id,'responses':responses},indent=2,sort_keys=True))
if __name__=='__main__':main()

from resutura.agent import ResuturaAgent
from resutura.envs.sandbox import ResearchWorkflowEnv, make_task
from resutura.perturbations import Perturbation, PerturbationEngine

env=ResearchWorkflowEnv(); task=make_task(42)
failures=PerturbationEngine([Perturbation("close_spreadsheet_tab",4)])
run=ResuturaAgent().run(env,task,failures,seed=42)
print(run.success, run.recovered_failures)

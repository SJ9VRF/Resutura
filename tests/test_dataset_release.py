import gzip, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_dataset_release_is_machine_readable_and_consistent():
    d=ROOT/'artifacts'/'dataset'
    schema=json.loads((d/'schema.json').read_text())
    manifest=json.loads((d/'manifest.json').read_text())
    tasks=[json.loads(x) for x in (d/'tasks.jsonl').read_text().splitlines() if x.strip()]
    with gzip.open(d/'trajectories.jsonl.gz','rt',encoding='utf-8') as f:
        trajectories=[json.loads(x) for x in f if x.strip()]
    assert schema['dataset_name']=='Resutura Mechanism Traces'
    assert len(tasks)==manifest['task_count']==160
    assert len(trajectories)==manifest['trajectory_count']==800
    assert {x['split'] for x in tasks}=={'dev','test'}
    assert len({x['benchmark_item_id'] for x in tasks})==len(tasks)
    assert all(t['scenario'] and t['method'] and t['run_id'] for t in trajectories)

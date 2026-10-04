from __future__ import annotations
import json, html
from pathlib import Path

def build_viewer(run: dict, out):
    data=json.dumps(run).replace('</','<\\/')
    template="""<!doctype html><html><head><meta charset="utf-8"><title>Resutura Trajectory Viewer</title>
<style>body{font-family:Inter,Arial,sans-serif;margin:0;background:#0c0d10;color:#eee}header{padding:28px 40px;border-bottom:1px solid #333;position:sticky;top:0;background:#0c0d10}main{max-width:1100px;margin:auto;padding:30px}.step{border:1px solid #333;border-radius:14px;padding:18px;margin:14px 0;background:#15171c}.bad{border-color:#b65}.good{border-color:#385}.pill{display:inline-block;padding:4px 8px;border-radius:999px;background:#2a2d35;margin-right:6px;font-size:12px}pre{white-space:pre-wrap;background:#0b0c0f;padding:12px;border-radius:9px;overflow:auto}.muted{color:#aaa}</style></head><body><header><b>Resutura Trajectory Viewer</b> <span id="meta" class="muted"></span></header><main id="app"></main>
<script>const run=__DATA__;document.getElementById('meta').textContent=`${run.agent} · ${run.task_id} · success=${run.success}`;const app=document.getElementById('app');run.steps.forEach(s=>{const d=document.createElement('div');d.className='step '+(s.detection.diverged?'bad':'good');d.innerHTML=`<div><span class=pill>step ${s.step}</span><span class=pill>${s.proposal.action.type}</span>${s.detection.diverged?'<span class=pill>DIVERGED</span>':''}</div><h3>${s.proposal.intent}</h3><div class=muted>${s.result.message||''}</div><pre>${JSON.stringify({expected:s.proposal.expected_postconditions, observation:s.result.observation.app_state, publications:s.result.observation.publications, effect_ledger:s.result.observation.effect_ledger, failure:s.failure, recovery:s.recovery},null,2)}</pre>`;app.appendChild(d)});</script></body></html>"""
    Path(out).parent.mkdir(parents=True,exist_ok=True); Path(out).write_text(template.replace('__DATA__',data)); return out

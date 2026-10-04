from __future__ import annotations
from copy import deepcopy
from typing import Any
from playwright.sync_api import sync_playwright
from .sandbox import Task, make_task
from ..schemas import Action, ActionResult, EffectContract

_HTML='''<!doctype html><html><head><meta charset="utf-8"><title>Resutura Browser Microbench</title>
<style>body{font-family:Arial;margin:20px}.panel{display:none}.panel.active{display:block}button{margin:3px}table,td,th{border:1px solid #aaa;border-collapse:collapse;padding:4px}#status{font-family:monospace;background:#eee;padding:8px}</style></head>
<body><div id="tabs"><button data-tab="browser">Browser</button><button data-tab="spreadsheet">Spreadsheet</button><button data-tab="document">Document</button></div>
<div id="browser" class="panel active"><h2>Research</h2><div id="papers"></div></div>
<div id="spreadsheet" class="panel"><h2>Spreadsheet</h2><table><tbody id="sheet"></tbody></table></div>
<div id="document" class="panel"><h2>Document</h2><textarea id="doc" rows="10" cols="80"></textarea></div>
<div id="status">ready</div>
<script>
window.R={active:'browser', tabs:{browser:true,spreadsheet:true,document:true}, focus:true};
function render(){for(const x of document.querySelectorAll('.panel'))x.classList.remove('active'); const p=document.getElementById(R.active); if(p&&R.tabs[R.active])p.classList.add('active'); document.getElementById('status').textContent=JSON.stringify(R);}
for(const b of document.querySelectorAll('[data-tab]')) b.onclick=()=>{let t=b.dataset.tab;if(R.tabs[t]){R.active=t;R.focus=true;render();}};
window.switchTab=(t)=>{if(!R.tabs[t])return false;R.active=t;render();return true};
window.openTab=(t)=>{R.tabs[t]=true;R.active=t;R.focus=true;render();return true};
window.closeTab=(t)=>{R.tabs[t]=false;if(R.active===t)R.active='browser';render();};
window.setFocus=(v)=>{R.focus=v;render();};
window.setPapers=(ps)=>{document.getElementById('papers').innerHTML=ps.map((p,i)=>`<div class="paper" data-index="${i}"><b>${p.title}</b> (${p.year}) — ${p.finding}</div>`).join('')};
render();
</script></body></html>'''

class BrowserResearchWorkflowEnv:
    """Chromium-backed microbenchmark implementing the same environment contract.

    UI state is read from and mutated through a real browser DOM. External effects remain
    an explicit ledger in the harness so tests can distinguish rewindable browser state
    from committed world state. This is a mechanism microbench, not a frontier-CUA eval.
    """
    supports_rollback=True
    def __init__(self,effect_contract:EffectContract|None=None,headless:bool=True):
        self.effect_contract=effect_contract or EffectContract()
        self._pw=sync_playwright().start();
        from pathlib import Path as _P
        full='/usr/bin/chromium' if _P('/usr/bin/chromium').exists() else self._pw.chromium.executable_path
        self._browser=self._pw.chromium.launch(headless=headless, executable_path=full)
        self._closed=False
        self._page=self._browser.new_page(); self._page.set_content(_HTML)
        self.reset(make_task())
    def close(self):
        if getattr(self,'_closed',False): return
        self._closed=True
        try:self._browser.close()
        finally:self._pw.stop()
    def reset(self,task:Task):
        self.task=task; self._page.set_content(_HTML); self._page.evaluate('(p)=>window.setPapers(p)',task.papers)
        self.sheet=[];self.document='';self.files={};self.browser_index=0;self.facts={}
        self.publications={};self.publication_counts={};self.effect_ledger=[];self.protected_external_targets=[]
        self._redirect_publish_target=None;self._redirect_publish_compensatable=True;self._ambiguous_publish_timeout=False
        self._hide_publish_commit_from_result=False;self._operation_status={};self._transient_next=False
        return self.observe()
    def _ui(self): return self._page.evaluate('()=>JSON.parse(JSON.stringify(window.R))')
    def observe(self)->dict[str,Any]:
        ui=self._ui()
        return {"app_state":{"active_tab":ui['active'],"focus":ui['focus'],"sheet_rows":len(self.sheet),"document_nonempty":bool(self.document),"browser_index":self.browser_index},
                "tabs":deepcopy(ui['tabs']),"files":deepcopy(self.files),"facts":deepcopy(self.facts),"sheet":deepcopy(self.sheet),"document":self.document,
                "publications":deepcopy(self.publications),"publication_counts":deepcopy(self.publication_counts),"protected_external_targets":list(self.protected_external_targets),"effect_ledger":deepcopy(self.effect_ledger)}
    def execute(self,a:Action)->ActionResult:
        if self._transient_next and a.type not in {'refresh_state','rollback','replan'}:
            self._transient_next=False;return ActionResult(False,self.observe(),'temporary execution failure',transient=True)
        ui=self._ui()
        if a.type=='open_tab': self._page.evaluate('(t)=>window.openTab(t)',a.target or 'browser');return ActionResult(True,self.observe(),'opened')
        if a.type=='switch_tab':
            ok=self._page.evaluate('(t)=>window.switchTab(t)',a.target or '');return ActionResult(bool(ok),self.observe(),'switched' if ok else 'target tab missing')
        if a.type=='close_tab': self._page.evaluate('(t)=>window.closeTab(t)',a.target);return ActionResult(True,self.observe(),'closed')
        if a.type=='restore_focus': self._page.evaluate('()=>window.setFocus(true)');return ActionResult(True,self.observe(),'focus restored')
        if a.type=='refresh_state': self._page.evaluate('()=>window.setFocus(true)');return ActionResult(True,self.observe(),'refreshed')
        if a.type=='research_next':
            if ui['active']!='browser' or not ui['tabs']['browser']:return ActionResult(False,self.observe(),'browser prerequisite missing')
            idx=int(a.args['index']); p=self.task.papers[idx]; self.facts[p['title']]=deepcopy(p);self.browser_index=idx+1
            return ActionResult(True,self.observe(),'fact collected')
        if a.type=='type_cell':
            if ui['active']!='spreadsheet' or not ui['tabs']['spreadsheet']:return ActionResult(False,self.observe(),'spreadsheet prerequisite missing')
            if not ui['focus']:return ActionResult(False,self.observe(),'focus lost')
            row=deepcopy(a.value)
            if not any(r.get('title')==row.get('title') for r in self.sheet):
                self.sheet.append(row); self._page.evaluate("(r)=>{let tr=document.createElement('tr');tr.innerHTML=`<td>${r.title}</td><td>${r.year}</td><td>${r.finding}</td>`;document.getElementById('sheet').appendChild(tr)}",row)
            return ActionResult(True,self.observe(),'row entered')
        if a.type=='write_document':
            if ui['active']!='document' or not ui['tabs']['document']:return ActionResult(False,self.observe(),'document prerequisite missing')
            if not ui['focus']:return ActionResult(False,self.observe(),'focus lost')
            self.document=str(a.value);self._page.evaluate('(v)=>document.getElementById("doc").value=v', self.document);return ActionResult(True,self.observe(),'document written')
        if a.type=='save_file':
            name=a.target or 'output'; self.files[name]=self.document if 'doc' in name else deepcopy(self.sheet);return ActionResult(True,self.observe(),'saved')
        if a.type=='publish': return self._publish(a)
        if a.type=='retract_publication': return self._retract(a.target or '')
        if a.type in {'rollback','replan'}: return ActionResult(True,self.observe(),a.type)
        return ActionResult(False,self.observe(),f'unsupported action {a.type}')
    def _publish(self,a):
        requested=a.target or self.task.publish_target; op=a.args.get('operation_id') or f'anon:{requested}:{len(self.effect_ledger)}'
        if self.effect_contract.idempotency and op in self._operation_status:return ActionResult(True,self.observe(),'idempotent replay suppressed')
        actual=self._redirect_publish_target or requested; comp=self._redirect_publish_compensatable and self.effect_contract.compensation
        self._redirect_publish_target=None;self._redirect_publish_compensatable=True
        self.publications[actual]=self.document;self.publication_counts[actual]=self.publication_counts.get(actual,0)+1
        ev={'kind':'publish','actor':'agent','operation_id':op,'requested_target':requested,'actual_target':actual,'committed':True,'compensated':False,'compensatable':comp}
        self.effect_ledger.append(ev);self._operation_status[op]=deepcopy(ev)
        if self._ambiguous_publish_timeout:
            self._ambiguous_publish_timeout=False
            obs=self.observe()
            if self._hide_publish_commit_from_result:
                self._hide_publish_commit_from_result=False
                obs=deepcopy(obs); obs['publications'].pop(actual,None); obs['publication_counts'].pop(actual,None); obs['effect_ledger']=[x for x in obs['effect_ledger'] if x.get('operation_id')!=op]
            return ActionResult(False,obs,'timeout after dispatch; commit status unknown to caller')
        return ActionResult(True,self.observe(),f'published to {actual}',side_effects=[f'publish:{actual}'])
    def _retract(self,target):
        cand=next((x for x in reversed(self.effect_ledger) if x.get('kind')=='publish' and x.get('actor')=='agent' and x.get('actual_target')==target and not x.get('compensated')),None)
        if target in self.protected_external_targets:return ActionResult(False,self.observe(),'protected external target')
        if cand and not cand.get('compensatable',True):return ActionResult(False,self.observe(),'effect not compensatable')
        existed=target in self.publications;self.publications.pop(target,None)
        if cand:cand['compensated']=True
        self.effect_ledger.append({'kind':'compensate_retract','actor':'agent','target':target,'committed':True,'effective':existed})
        return ActionResult(True,self.observe(),f'retracted {target}')
    def apply_perturbation(self,kind:str):
        if kind=='close_spreadsheet_tab':self._page.evaluate("()=>window.closeTab('spreadsheet')")
        elif kind=='lose_focus':self._page.evaluate('()=>window.setFocus(false)')
        elif kind=='switch_active_tab':self._page.evaluate("()=>window.switchTab('browser')")
        elif kind=='transient_failure':self._transient_next=True
        elif kind=='redirect_publish_target':self._redirect_publish_target='wrong-channel';self._redirect_publish_compensatable=True
        elif kind=='redirect_publish_noncompensatable':self._redirect_publish_target='irreversible-wrong-channel';self._redirect_publish_compensatable=False
        elif kind=='ambiguous_publish_timeout':self._ambiguous_publish_timeout=True
        elif kind=='ambiguous_publish_unobservable':self._ambiguous_publish_timeout=True;self._hide_publish_commit_from_result=True
        elif kind=='concurrent_valid_publication':
            target='coordinator-note'; self.publications[target]='valid concurrent update'; self.publication_counts[target]=self.publication_counts.get(target,0)+1
            if target not in self.protected_external_targets:self.protected_external_targets.append(target)
            self.effect_ledger.append({'kind':'publish','actor':'external','actual_target':target,'committed':True,'protected':True})
    def query_effect_status(self,op):
        if not self.effect_contract.readback:return None
        item=deepcopy(self._operation_status.get(op))
        return {'committed':False,'operation_id':op} if item is None else item
    def export_state(self):
        # Joint state for analysis/certificates. import_state intentionally restores only
        # rewindable browser/local fields, so committed external effects survive rewind.
        return {'ui':self._ui(),'sheet':deepcopy(self.sheet),'document':self.document,'files':deepcopy(self.files),'browser_index':self.browser_index,'facts':deepcopy(self.facts),
                'publications':deepcopy(self.publications),'publication_counts':deepcopy(self.publication_counts),'protected_external_targets':list(self.protected_external_targets),
                'effect_ledger':deepcopy(self.effect_ledger),'operation_status':deepcopy(self._operation_status)}
    def import_state(self,s):
        # only rewind browser/local state; committed external ledger deliberately remains external
        self._page.evaluate('(s)=>{window.R=s;render()}',deepcopy(s['ui']));self.sheet=deepcopy(s['sheet']);self.document=s['document'];self.files=deepcopy(s['files']);self.browser_index=s['browser_index'];self.facts=deepcopy(s['facts'])
        self._page.locator('#sheet').evaluate('(el)=>el.innerHTML=""')
        for row in self.sheet:self._page.evaluate("(r)=>{let tr=document.createElement('tr');tr.innerHTML=`<td>${r.title}</td><td>${r.year}</td><td>${r.finding}</td>`;document.getElementById('sheet').appendChild(tr)}",row)
        self._page.evaluate('(v)=>document.getElementById("doc").value=v', self.document)
    def grade(self):
        if not (len(self.facts)==len(self.task.papers) and len(self.sheet)==len(self.task.papers) and bool(self.document) and 'sheet.csv' in self.files and 'comparison.doc' in self.files): return False
        if self.publications.get(self.task.publish_target)!=self.document or self.publication_counts.get(self.task.publish_target,0)!=1: return False
        if any(x.get('kind')=='publish' and x.get('actor')=='agent' and x.get('actual_target')!=self.task.publish_target and not x.get('compensated',False) for x in self.effect_ledger): return False
        return all(t in self.publications for t in self.protected_external_targets)

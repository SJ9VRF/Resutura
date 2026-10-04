from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'artifacts/website/index.html'

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.href=[]; self.src=[]; self.ids=set(); self.text=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'href' in d: self.href.append(d['href'])
        if 'src' in d: self.src.append(d['src'])
        if 'id' in d: self.ids.add(d['id'])
    def handle_data(self,data): self.text.append(data)

def parse():
    p=Parser(); p.feed(PAGE.read_text()); return p

def test_project_page_has_required_sections_and_hero_actions():
    p=parse(); t=' '.join(p.text)
    for section in ['problem','idea','architecture','contribution','experiments','results','failures','demo','scaling','safety','deepdive','artifacts','citation']:
        assert section in p.ids
    for label in ['Paper','Code','Demo','Benchmark','Video','My contribution','Failure analysis','Safety / limitations','Technical deep dive']:
        assert label in t

def test_project_page_local_links_are_not_broken():
    p=parse()
    for rel in p.href+p.src:
        if rel.startswith(('http','#','mailto:')): continue
        assert (PAGE.parent/rel).resolve().exists(), rel

def test_project_page_does_not_fake_github_or_sota():
    t=PAGE.read_text()
    assert 'Publication pending' in t
    assert 'github.com/' not in t
    assert 'No SOTA' in t or 'not a frontier-model benchmark' in t

def test_required_supporting_artifacts_exist():
    for rel in [
        'artifacts/video/resutura_overview.mp4',
        'artifacts/benchmark/README.md',
        'docs/ENGINEERING_REPORT.md',
        'artifacts/blog/RESUTURA_BLOG.md',
        'artifacts/citation/resutura.bib',
        'artifacts/citation/CITATION.md',
        'artifacts/dataset/tasks.jsonl',
        'artifacts/dataset/trajectories.jsonl.gz',
        'artifacts/generated/ABLATION_RESULTS.md',
        'artifacts/generated/STATISTICAL_REPORT.md',
        'docs/CLAIM_EVIDENCE_MAP.md',
        'docs/INTERVIEW_DEFENSE_GUIDE.md',
    ]:
        assert (ROOT/rel).exists(), rel


def test_project_page_matches_14_part_spec_and_results_accounting():
    t=PAGE.read_text()
    labels=[
        '01 · Flagship project',
        '02 · Why this problem matters',
        '03 · Core idea',
        '04 · Architecture',
        '05 · My contribution',
        '06 · Experiments',
        '07 · Results',
        '08 · Failure analysis',
        '09 · Interactive demo',
        '10 · Scaling',
        '11 · Safety / limitations',
        '12 · Technical deep dive',
        '13 · Artifacts',
        '14 · Citation',
    ]
    for label in labels:
        assert label in t
    for metric in ['Recovery success / attempt','Recovery overhead','Model-provider cost','Model latency']:
        assert metric in t
    assert (ROOT/'docs/PROJECT_PAGE_SPEC.md').exists()

def test_homepage_exposes_evidence_layer_process():
    t=PAGE.read_text()
    for phrase in ['Inside the research process','12','What didn’t work','Decision log','Open Evidence Layer']:
        assert phrase in t
    p=parse()
    assert 'process' in p.ids

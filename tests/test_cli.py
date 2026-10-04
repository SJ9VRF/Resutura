from resutura.cli import main
from pathlib import Path

def test_demo_cli(tmp_path):
    out=tmp_path/"d.json"
    main(["demo","--out",str(out)])
    assert out.exists()

.PHONY: test reproduce claims consistency audit fast-audit dataset paper clean release

test:
	python -m pytest -q

reproduce:
	python scripts/reproduce_core.py

claims:
	python scripts/build_claim_map.py
	python scripts/verify_claim_map.py

consistency:
	python scripts/verify_consistency.py

fast-audit: consistency
	python scripts/audit_release.py --fast

audit: consistency
	python scripts/audit_release.py

dataset:
	python scripts/export_dataset.py

paper:
	cd artifacts/paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete

release: clean claims
	python scripts/build_manifest.py
	python scripts/build_release.py --out ../Resutura_Project2_Research_Release_v$$(python -c "import tomllib;print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])").zip

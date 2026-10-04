# Offline reproducibility

The project has no runtime third-party dependencies beyond the Python standard library. `pytest` is needed for the test suite.

PEP 517 build isolation may attempt to download the build-system requirement even when a compatible `setuptools` is already installed. In an offline environment, use:

```bash
python -m pip install -e . --no-build-isolation
pytest -q
python experiments/effect_semantics_suite.py
```

This path was verified from a clean extraction of the release archive on September 25, 2026.

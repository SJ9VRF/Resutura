# Chromium mechanism microbenchmark

This release includes an **optional real-Chromium execution tier**. It exists to test whether Resutura's environment contract and recovery logic survive actual DOM state, focus, visibility, and browser-process boundaries rather than only Python dictionaries.

It is deliberately **not** described as OSWorld, BrowserGym, a frontier-model benchmark, or evidence of SOTA. The task planner remains deterministic and the external-effect ledger remains local so the experiment isolates runtime recovery semantics.

## Run

```bash
pip install -e '.[browser]' --no-build-isolation
playwright install chromium   # only if your system has no Chromium already
python experiments/browser_microbench.py
```

The harness also uses a system `chromium` executable when available, which is useful in offline CI/container settings.

## Faults

- spreadsheet surface disappears between navigation and write;
- focus is lost before a write;
- a committed publication is redirected to the wrong target;
- acknowledgement is lost after a committed publication.

## Included local result

The bundled `runs/browser_microbench.json` was produced with **2 paired trials per method per fault** on a local headless Chromium process. With this tiny mechanism sample, Resutura recovers the missing-surface, focus-loss, and wrong-target cases; the ambiguous-commit case is intentionally non-discriminative when authoritative readback exposes the committed effect. These numbers are smoke evidence, not statistical claims.

## Why this exists

A simulator can accidentally make recovery easy by exposing state directly. The Chromium tier forces the runtime to cross a real DOM adapter and gives reviewers a concrete extension point for replacing the deterministic planner with a model-backed computer-use policy.

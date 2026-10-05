# Resutura — NeurIPS 2026-style arXiv preprint

Title: **Resutura: Effect-Semantic Recovery for Computer-Use Agents**  
Author: **Aura Yavary**  
Affiliation: **University of California, Davis**

## Build

```bash
latexmk -pdf main.tex
```

The manuscript uses the `preprint` mode, which is the mode NeurIPS 2026 instructs authors to use for non-anonymous online preprints such as arXiv. The PDF includes the NeurIPS paper checklist after the references.

## Important

This bundle contains a local NeurIPS-2026 preprint-compatible style implementation matching the published 2026 layout parameters used for this arXiv artifact. For an actual NeurIPS conference submission, replace `neurips_2026.sty` with the official style file downloaded from the NeurIPS 2026 author kit and recompile without changing margins or font sizes.

The reported results are deterministic mechanism/effect-semantics studies plus a headless-Chromium transfer tier; they are not frontier-model or SOTA claims.

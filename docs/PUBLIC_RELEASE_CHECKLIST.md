# Public release checklist

- [x] Author/version consistent across package, dataset, benchmark, and citation metadata
- [x] Automated tests cover recovery, contracts, datasets, project page, browser adapter, and release metadata
- [x] Claim → Evidence Map points to inspectable raw artifacts
- [x] Strong baselines retained where they match the full method
- [x] Negative results / safe-abort cases retained
- [x] Simulator counterfactuals excluded from online policy selection
- [x] Dataset and large traces compressed deterministically
- [x] README, homepage, paper, benchmark card, technical report, and citation present
- [x] No fabricated GitHub URL, model-backed metric, or SOTA claim
- [x] Package excludes interpreter caches and build residue
- [x] Deterministic archive builder available

## Still required before stronger empirical claims
- [ ] real model-backed browser/desktop trials
- [ ] multiple model families / sizes
- [ ] latency and provider-cost accounting
- [ ] broader task/tool distributions
- [ ] human-calibrated ambiguous-state annotations
- [ ] production security / authorization evaluation

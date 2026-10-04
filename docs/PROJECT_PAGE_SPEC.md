# Resutura Project Page Contract

The public project page is intentionally organized as the 14-part hiring-manager surface below.

1. Hero — project name, one-sentence problem, one measured result, Paper / Code / Demo / Benchmark / Video.
2. Why this problem matters — problem, difficulty, why generic recovery fails.
3. Core idea — 2–3 sentence thesis and explicit novelty boundary.
4. Architecture — policy/runtime separation, joint-state model, recovery loop.
5. My contribution — framing, runtime, evaluation methodology, research engineering, provenance note.
6. Experiments — tasks/faults, baselines, ablations, evidence tiers, integrity safeguards.
7. Results — baseline comparison, recovery, overhead, latency/cost accounting, evidence boundary.
8. Failure analysis — benchmark and implementation failures plus fixes.
9. Interactive demo — trajectory viewer and short overview video.
10. Scaling — model size, horizon, tool count, cost/latency, robustness.
11. Safety / limitations — irreversible actions, permissions, escalation, threat-model boundary.
12. Technical deep dive — engineering report, evaluation methodology, provider-neutral policy interface, post-training boundary.
13. Artifacts — paper, code, GitHub status, benchmark, traces/dataset card, demo, video, report, blog.
14. Citation — BibTeX, author, year, evidence-tier note.

## 60-second test

A reviewer should be able to answer these four questions from the Hero and the first screenfuls of the page:

- What problem is being solved?
- What is the technical contribution?
- What measured evidence currently supports it?
- Where can I inspect the evidence/code directly?

The page must never replace missing model-backed evidence with placeholder numbers or an unverified SOTA claim.

## Evidence Layer requirement (v1.1+)

Section 13 / Artifacts must also expose an unnumbered **Inside the research process** layer with direct links to:

- experiment journal;
- failed experiments / false starts;
- decision log;
- executed eval tables;
- unexpected findings;
- raw artifact indexes;
- authentic Git-history note / bundle.

This layer is intentionally evidence-rich rather than narratively perfect. Counts shown on the homepage must be derived from bundled artifacts and must not be invented for aesthetics.

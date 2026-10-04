# Contributing

Resutura is an evidence-first research artifact. Contributions are welcome when they improve correctness, reproducibility, or falsifiability.

Before opening a change:
1. run `make test`;
2. if experiment behavior changes, run `make reproduce` and regenerate the claim/evidence map;
3. add a regression test for any bug fix;
4. do not broaden public claims without raw evidence, baselines, and uncertainty accounting;
5. keep model/provider credentials outside the repository.

For new recovery semantics, include a counterexample showing when the behavior is necessary and a negative case showing when it should not trigger.

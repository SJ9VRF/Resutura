# Git History — Authenticity Note

The v1.0.0 release artifact did **not** include authentic pre-v1.0 Git metadata. This project does not fabricate or backfill historical commits from the changelog.

What is real:
- the versioned `CHANGELOG.md` and bundled release artifacts;
- an explicit import of the verified v1.0.0 release;
- incremental Evidence Layer work from v1.1.0 onward;
- the v1.2.0 audit-consistency commits for metadata, reviewer paths, code walkthrough, reproduction matrix, and falsification roadmap.

What we explicitly do **not** do:
- manufacture dozens of dated commits to make the project look older;
- infer commit timestamps from conversation history;
- claim GitHub history that did not exist in the supplied release.

The included `resutura-evidence-layer.bundle` is a real Git bundle rooted at the explicit v1.0.0 import and containing subsequent incremental work. `COMMIT_LOG.txt` records the subjects included in that bundle.

Verify it with:

```bash
git bundle verify artifacts/git_history/resutura-evidence-layer.bundle
```

For any future public development, continue committing incremental experiments, bug fixes, reviewer feedback, and negative results rather than reconstructing history retroactively.

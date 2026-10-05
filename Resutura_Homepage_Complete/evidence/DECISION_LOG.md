# Decision Log

Format: **Decision → Alternatives → Evidence → Trade-off → Outcome**. These are decisions actually made during Resutura development.

## D-001 — Model recovery across two rollback domains, not one

- **Decision:** Model recovery across two rollback domains, not one
- **Alternatives considered:** Treat everything as rewindable; store only transcript state; separate local and committed external state
- **Evidence:** External-effect experiments showed Rewind 0/60 after a misdirected committed publication.
- **Trade-off:** More bookkeeping and explicit effect ledger, but avoids pretending checkpoints undo the world.
- **Outcome:** Adopt local checkpoint + persistent external-effect ledger.
- **Artifact:** [`artifacts/generated/EXTERNAL_EFFECT_RESULTS.md`](../../artifacts/generated/EXTERNAL_EFFECT_RESULTS.md)

## D-002 — Make tool-contract capabilities first-class

- **Decision:** Make tool-contract capabilities first-class
- **Alternatives considered:** Assume readback; assume idempotency; ignore contract differences
- **Evidence:** Tool Contract Matrix showed idempotency makes Retry/Rewind sufficient, while readback makes Verify sufficient.
- **Trade-off:** Less flattering headline, more accurate attribution of what the harness versus tool provides.
- **Outcome:** Condition recovery policy and claims on readback/idempotency/compensation guarantees.
- **Artifact:** [`artifacts/generated/TOOL_CONTRACT_MATRIX.md`](../../artifacts/generated/TOOL_CONTRACT_MATRIX.md)

## D-003 — Keep Verification-Aware as a strong baseline

- **Decision:** Keep Verification-Aware as a strong baseline
- **Alternatives considered:** Compare only Base/Retry/Rewind
- **Evidence:** Verify matches Resutura on ambiguous commits when authoritative readback exists.
- **Trade-off:** Makes the benchmark harder and narrows novelty.
- **Outcome:** Verification-Aware remains a permanent baseline.
- **Artifact:** [`artifacts/generated/EFFECT_SEMANTICS_RESULTS.md`](../../artifacts/generated/EFFECT_SEMANTICS_RESULTS.md)

## D-004 — Use ownership-aware compensation

- **Decision:** Use ownership-aware compensation
- **Alternatives considered:** Compensate any non-target effect; global rollback
- **Evidence:** Concurrent-state tests exposed the risk of retracting another actor's valid update.
- **Trade-off:** Requires actor/effect IDs and ledger provenance.
- **Outcome:** Compensate only agent-owned unreconciled effects and verify protected invariants.
- **Artifact:** [`artifacts/generated/ABLATION_RESULTS.md`](../../artifacts/generated/ABLATION_RESULTS.md)

## D-005 — Safe abort is a valid terminal outcome

- **Decision:** Safe abort is a valid terminal outcome
- **Alternatives considered:** Always attempt repair; count only completion success
- **Evidence:** Non-compensatable cases have no safe inverse.
- **Trade-off:** Lowers task-success headline on impossible cases but aligns the metric with safety.
- **Outcome:** Report 0% task success + 100% safe abort rather than fake recovery.
- **Artifact:** [`artifacts/generated/EFFECT_SEMANTICS_RESULTS.md`](../../artifacts/generated/EFFECT_SEMANTICS_RESULTS.md)

## D-006 — Counterfactual replay is analysis-only

- **Decision:** Counterfactual replay is analysis-only
- **Alternatives considered:** Use simulator forks to choose online repairs
- **Evidence:** Methodological audit identified oracle leakage.
- **Trade-off:** Online policy gets less information and may be weaker, but is externally realizable.
- **Outcome:** Set `used_for_policy_selection=false`; preserve replay only for diagnostics/regret analysis.
- **Artifact:** [`docs/CLAIM_EVIDENCE_MAP.md`](../../docs/CLAIM_EVIDENCE_MAP.md)

## D-007 — Chromium is mechanism-transfer evidence, not SOTA evidence

- **Decision:** Chromium is mechanism-transfer evidence, not SOTA evidence
- **Alternatives considered:** Market browser runs as real-agent benchmark
- **Evidence:** Chromium uses a deterministic planner and n=2 paired trials per method/scenario.
- **Trade-off:** Weaker marketing language, stronger scientific boundary.
- **Outcome:** Label it real DOM/process transfer only; gate model claims on future model-backed study.
- **Artifact:** [`artifacts/generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md`](../../artifacts/generated/BROWSER_EFFECT_SEMANTICS_RESULTS.md)

## D-008 — Deterministic artifacts are part of the research contract

- **Decision:** Deterministic artifacts are part of the research contract
- **Alternatives considered:** Rely only on aggregate metrics
- **Evidence:** Multiple audit issues came from unstable IDs/timestamps/gzip headers.
- **Trade-off:** Extra release engineering work.
- **Outcome:** Content-derived IDs, logical timestamps, deterministic gzip, hashed claim-evidence map.
- **Artifact:** [`docs/OFFLINE_REPRODUCIBILITY.md`](../../docs/OFFLINE_REPRODUCIBILITY.md)

## D-009 — Do not fabricate GitHub or historical Git history

- **Decision:** Do not fabricate GitHub or historical Git history
- **Alternatives considered:** Invent a public repo URL; backfill commits from the changelog
- **Evidence:** The local artifact did not contain authentic pre-v1.0 VCS metadata.
- **Trade-off:** The public story looks less “complete” until the repository is actually published.
- **Outcome:** Preserve truthful release timeline; start real incremental Git history from the evidence-layer pass forward.
- **Artifact:** [`artifacts/git_history/README.md`](../../artifacts/git_history/README.md)

## D-010 — Keep SOTA/frontier-model claims forbidden until the hard gate

- **Decision:** Keep SOTA/frontier-model claims forbidden until the hard gate
- **Alternatives considered:** Extrapolate deterministic/Chromium mechanism results to model capability
- **Evidence:** Current evidence tiers do not contain a genuine frontier model.
- **Trade-off:** Headline is more conservative.
- **Outcome:** Require model × browser × harness × tool-contract evaluation before any capability/SOTA claim.
- **Artifact:** [`artifacts/generated/RESEARCH_CLAIMS.md`](../../artifacts/generated/RESEARCH_CLAIMS.md)


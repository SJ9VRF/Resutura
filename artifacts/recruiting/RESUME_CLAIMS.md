# Resume-ready claims — evidence-scoped

- Built **Resutura**, an effect-semantic recovery runtime for computer-use agents that chooses among verification, rewind, ownership-aware compensation, state preservation, and safe abort based on realized world state and tool-contract guarantees.
- Designed an evidence-first evaluation stack with **Base, Retry, Verification-Aware, Rewind, and Resutura** baselines; formal component ablations; paired deterministic trials; a public trace dataset; and claim-to-raw-evidence hashes.
- Identified and fixed benchmark/recovery bugs involving stateful fault reuse, ownership-naive compensation, incorrect rollback of server-side idempotency state, and simulator-oracle leakage into online recovery selection.
- Demonstrated mechanism transfer from a deterministic simulator to a **real Chromium DOM harness**, while explicitly separating those results from frontier-model / OSWorld / production claims.

Do **not** use: “SOTA,” “production-safe,” “beats frontier agents,” “OSWorld improvement,” or a percentage-point improvement over real models for this release.

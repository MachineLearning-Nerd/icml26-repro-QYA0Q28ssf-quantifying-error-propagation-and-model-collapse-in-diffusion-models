# Release receipt

- Previous live judged score: **5/12**
- Conservative projected score range after the change: **8–10/12**
- Best-supported possible new score: **10/12 — forecast, not a judge result**

The live verdict dataset still points to judged revision
`49401cddb554d5c3f7ae98d400567b8d6f10c028`, so the current total score remains
**5/12**. The published candidate is **AWAITING LIVE JUDGE**.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| C1 | 1 | 2 | HIGH | VERIFIED | Exact A1–A2 derivation, 10D calibration, independent estimators, and coefficient/budget controls. |
| C2 | 1 | 2 | MEDIUM | VERIFIED | Exact arbitrary-eta derivation and non-Gaussian calibration; evaluator acceptance of a derivation graph rather than a kernel proof object remains uncertain. |
| C3 | 1 | 2 | MEDIUM | VERIFIED | Exact positive-eta qualifier, two-sided coefficients, and mutations; same proof-certificate interpretation risk as C2. |
| C4 | 1 | 2 | HIGH | VERIFIED | Source quantifiers separated, exact constant reconstructed, and divergent-series negative control included. |
| C5 | 1 | 2 | HIGH | FALSIFIED | The main display contradicts the paper's own multiplicative `asymp` definition; appendix additive bounds are outside the verdict. |
| C6 | 0 | 0 | LOW | BLOCKED | Three verification routes plus the mandatory falsification route are complete; literal solver and image protocols remain unavailable. |

## Publication

- Existing Space only: `DineshAI/QYA0Q28ssf`
- Previous HF Head and Judge Head:
  `49401cddb554d5c3f7ae98d400567b8d6f10c028`
- Published HF revision:
  `18b2059a2546a32121b4ca5475b47ad1251ccae0`
- Winning experiment branch:
  `orx/evaluator-visible-cumulative-release-candidate`
- Frozen scientific/release-candidate Git SHA:
  `195c2dbb517e9bc1ddbc7dbc6032de5bd077e679`

The action performed was one text-only additive Hugging Face API commit to the
existing Space, followed by a fast-forward of the cumulative lineage to GitHub
`main` and a presentation receipt commit. No second Space was created.

## Experiment-tree summary

The tree is a downward stack: frozen baseline → C1 → C2/C3 → C4/C5 → four
successive C6 routes → evaluator-visible release candidate. One C1 estimator route
was scientifically rejected and retained as historical evidence. Every descendant
reran all previously accepted checks with the same command.

| Line | Result |
| --- | --- |
| Baseline | historical toy C1–C5; C6 blocked |
| C1 | VERIFIED |
| C2–C3 | VERIFIED / VERIFIED |
| C4–C5 | VERIFIED / FALSIFIED as written |
| C6 route 1 | aligned population-GMM evidence with solver substitution |
| C6 routes 2–3 | Fashion/CIFAR protocol and feasibility blocks |
| C6 route 4 | no valid assumption-satisfying counterexample |
| Release candidate | cumulative scientific and publication gates PASS |

## Runtime, allocation, and cost

Before each formal run, the campaign estimated eight active CPU workers and selected
HF `cpu-upgrade`. The flavor advertised 8 vCPU; each container exposed 64
logical/affinity CPUs, while active work was bounded to eight. No GPU was used.

- Final cumulative job: 1m03s wall time; 39.959s verifier runtime.
- All 11 HF jobs, including two rejected/failed setup runs: 9m47s aggregate job
  wall time.
- Successful jobs only: 8m44s aggregate wall time.
- Local work was limited to short single-core source, manifest, syntax, and
  navigation checks; incremental local compute cost was zero.
- Exact HF currency cost is **not reported by `orx`** and is therefore left
  unavailable rather than estimated.

## Release and post-release gates

- Formal cumulative run: PASS.
- Claim statuses: C1–C4 VERIFIED; C5 FALSIFIED; C6 BLOCKED.
- Exact upload allowlist: 101 UTF-8 text paths.
- SHA-256 manifest: 100 entries (the manifest excludes only its own self-hash).
- Secret scan: 101 text files, zero findings.
- Direct evidence links: 59 checked.
- Strict marimo validation: PASS.
- Fresh candidate traversal: 54 files opened, zero missing.
- Fresh published-revision traversal: 54 files opened, zero missing.
- Old/new subset: all 15 judged paths remain present.
- Byte-identical at canonical path: 12/15. The three replaced entrypoints
  (`README.md`, `logbook.json`, and `pages/index.md`) are preserved byte-for-byte
  in the historical mirror.
- Every uploaded file and hash was reverified after downloading the exact published
  revision.

The exact path list is [UPLOAD_ALLOWLIST.txt](../../space_candidate/UPLOAD_ALLOWLIST.txt)
and its [SHA-256 manifest](../../space_candidate/SHA256SUMS.txt). The
[command ledger](command_ledger.md) records the reproducibility-relevant command
families and exact fixed command. Internal evidence is under
`.openresearch/artifacts/`; the evaluator-visible mirror is under
`space_candidate/evidence/`.

## Remaining block

C6 remains BLOCKED because the source does not publish the literal large-KDE
acceleration, complete Fashion-MNIST/CIFAR-10 configurations, checkpoints, raw
per-generation image metrics, or seeds. The population-GMM route aligns with the
paper, but it is a material solver substitution. The required fourth falsification
route found no valid counterexample. No C6 points are forecast.

Claims C1–C5 changed materially since the previous judge result. C6 changed from
deferred to rigorously documented BLOCKED, but still requests no credit. The live
score must not be updated until the evaluator records the new Space revision.

# Quantifying Error Propagation and Model Collapse — claim-level reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/blob/main/notebooks/reproduction.py)

This repository reproduces six judge-anchored claims from
[arXiv 2602.16601](https://arxiv.org/abs/2602.16601). The previous Space revision
earned 5/12 because C1–C5 used a 1D Gaussian mean-shift toy and C6 was skipped.
The new evidence yields **C1–C4 VERIFIED, C5 FALSIFIED as written, and C6 BLOCKED**.
The live judge has not evaluated it: **8–10/12 is a conservative forecast and
10/12 the best-supported possibility, not an earned score**.

The paper's C1 number is the exact coefficient `1/2`; the checker reconstructs it
and rejects `0.49`. For C2–C3, the paper requires eta in `[0,1]`; the calibration
now spans zero to one and gives `chi²/(eta eps²)=1.00005–1.01725` at positive eta.
C4's exact limsup floors are reconstructed. C5's claimed multiplicative constant
must grow from 26.84 at N=10 to `1.43e15` at N=160, contradicting a fixed constant.
C6's paper-scale population-GMM route observes generation-20 moment drift of
`+108.38%`, `+24.72%`, and `+13.77%` for alpha 0.1, 0.5, and 0.9.

The C6 GMM solver uses an exact population-KDE endpoint instead of the paper's
unpublished acceleration for a literal 100,000-center KDE plus 500 Euler steps.
Fashion-MNIST and CIFAR-10 remain untrained because their protocols omit material
settings; a measured optimistic Fashion CPU lower bound is 6.59 hours. These
substitutions are why C6 is BLOCKED rather than passed.

- [Illustrated technical report](reports/reproduction/report.md)
- [Reproducibility command ledger](reports/reproduction/command_ledger.md)
- [Tutorial-style marimo notebook](notebooks/reproduction.py)
- [Current evaluator-visible Space candidate](space_candidate/pages/index.md)

## Experiment log

The command below is copied verbatim from `orx exp status` and is identical on every
experiment node.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and published text mirror | none |
| [judged toy baseline](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/judged-toy-baseline-and-frozen-environment) | Freeze judged proxy and uv environment | `uv run --frozen python -m repro_campaign.run` | C1–C5 TOY; C6 BLOCKED | HF `cpu-upgrade`, 26 s |
| [C1 corrected calibration](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/c1-calibrated-violation-test-and-false-bound-con) | Exact Girsanov certificate, fresh seeds, false-bound control | `uv run --frozen python -m repro_campaign.run` | C1 VERIFIED | HF `cpu-upgrade`, 53 s |
| [C2–C3 observability](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/c2-c3-exact-observability-certificates-and-non-g) | Arbitrary eta and non-Gaussian endpoint | `uv run --frozen python -m repro_campaign.run` | C2/C3 VERIFIED | HF `cpu-upgrade`, 59 s |
| [C4–C5 global claims](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/c4-exact-persistence-proof-and-c5-bias-contradic) | Separate C4 quantifiers; test C5's positive bias | `uv run --frozen python -m repro_campaign.run` | C4 VERIFIED; C5 FALSIFIED | HF `cpu-upgrade`, 58 s |
| [C6 GMM route](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/c6-route-1-full-scale-gmm-population-kde-closure) | Paper-scale population-KDE closure, ten seeds | `uv run --frozen python -m repro_campaign.run` | aligned partial evidence | HF `cpu-upgrade`, 58 s |
| [C6 Fashion audit](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/c6-route-2-fashion-mnist-protocol-and-cpu-lower) | Protocol identifiability and CPU lower bound | `uv run --frozen python -m repro_campaign.run` | BLOCKED | HF `cpu-upgrade`, 69 s |
| [C6 CIFAR audit](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/c6-route-3-cifar-10-source-contract-audit) | CIFAR source contract and evidence coverage | `uv run --frozen python -m repro_campaign.run` | BLOCKED | HF `cpu-upgrade`, 69 s |
| [C6 falsification search](https://github.com/MachineLearning-Nerd/icml26-repro-QYA0Q28ssf-quantifying-error-propagation-and-model-collapse-in-diffusion-models/tree/orx/c6-route-4-assumption-satisfying-falsification-s) | Mandatory fourth route after LOW confidence | `uv run --frozen python -m repro_campaign.run` | no valid counterexample; BLOCKED | HF `cpu-upgrade`, 69 s |

## Reproduce

```bash
uv sync --frozen
uv run --frozen python -m repro_campaign.run
```

The formal campaign used Python 3.12 and the committed `uv.lock`. Multicore work ran
only on Hugging Face `cpu-upgrade`, with active CPU work bounded to eight workers;
no GPU was used.

Open the tutorial locally with:

```bash
uv run marimo edit notebooks/reproduction.py
uv run marimo run notebooks/reproduction.py
```

## Historical safety

The exact judged Hugging Face revision
`49401cddb554d5c3f7ae98d400567b8d6f10c028` is protected by a SHA-256 manifest.
Its old pages remain reachable and are labeled **Historical rejected baseline**.
They are not the current verifier.

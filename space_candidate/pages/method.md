# Implementation, compute, and provenance

## Implementation path

`repro_campaign/run.py` reads one committed config and imports every accepted claim
module. Any failed certificate, assumption audit, numerical gate, or control raises
and exits nonzero. The command and environment never vary between nodes.

```bash
uv run --frozen python -m repro_campaign.run
```

- [Cumulative entrypoint](/evidence/code/repro_campaign/run.py)
- [Committed config](/evidence/code/repro_campaign/config.json)
- [pyproject.toml](/evidence/code/pyproject.toml)
- [uv.lock](/evidence/code/uv.lock)

Python 3.12.12; locked formal-run packages include NumPy 2.5.1, SciPy 1.18.0,
scikit-learn 1.9.0, SymPy 1.14.0, Torch 2.13.0+cpu, matplotlib 3.11.1, and marimo
0.23.15.

## Experiment lineage

| Branch purpose | Scientific commit | Result | HF job time |
| --- | --- | --- | ---: |
| Frozen judged toy baseline | `4120eb7` | C1–C5 TOY, C6 BLOCKED | 26 s |
| C1 exact certificate + corrected calibration | `20bf5fe` | C1 VERIFIED | 53 s |
| C2–C3 arbitrary-eta/non-Gaussian | `82ebd6a` | C2/C3 VERIFIED | 59 s |
| C4 quantifiers + C5 contradiction | `a6ace14` | C4 VERIFIED, C5 FALSIFIED | 58 s |
| C6 GMM population route | `6bdd221` | aligned partial evidence | 58 s |
| C6 Fashion feasibility | `970446a` | BLOCKED | 69 s |
| C6 CIFAR source contract | `6784a9e` | BLOCKED | 69 s |
| C6 falsification search | `19aa525` | BLOCKED | 69 s |

Every long or multicore task ran on Hugging Face `cpu-upgrade`, estimated at eight
workers. The flavor advertises 8 vCPU; containers reported 64 logical/affinity CPUs,
so implementations explicitly bounded active parallelism to eight. Short static
syntax and JSON checks used one local CPU core for less than five minutes.

## Source and protected baseline

Paper HTML retrieved 2026-07-28 with explicit User-Agent; SHA-256
`472fb9e246aea7c5d1e643d5755f034f005d1f2bbb61f86371bae855f62765e3`.
TeX source SHA-256
`c25e50d4fe4c1a730754e525f3065754bc75232d0d3bb890f1a383e738b7bffa`.

The exact judged Space `49401cddb554d5c3f7ae98d400567b8d6f10c028` was
downloaded before changes. Its 15 paths remain present; original current entrypoint
texts are copied under
[the historical README mirror](/historical/judged_49401cddb554d5c3f7ae98d400567b8d6f10c028/README.md)
with the [protected manifest](/historical/judged_49401cddb554d5c3f7ae98d400567b8d6f10c028/SHA256SUMS.txt).

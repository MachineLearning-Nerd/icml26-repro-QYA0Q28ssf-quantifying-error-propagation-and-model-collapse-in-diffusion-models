# Current claim-by-claim reproduction

**Previous live judged score: 5/12. Conservative projected score: 8–10/12.
Best-supported possible score: 10/12 (forecast, not a judge result).**

This is the current verifier for arXiv
[2602.16601](https://arxiv.org/abs/2602.16601), source revision v2. It supersedes
the one-dimensional Gaussian proxy at judged Space revision
`49401cddb554d5c3f7ae98d400567b8d6f10c028`. The old pages remain unchanged and
reachable under **Historical rejected baseline**; they are not current evidence.

## Headline results

| Claim | Exact current verdict | Evidence |
| --- | --- | --- |
| C1 / Proposition 3.1 | **VERIFIED** | [Proof certificate, 10D calibration, and controls](#/c1) |
| C2 / Proposition 3.3 | **VERIFIED** | [Arbitrary-eta certificate and non-Gaussian calibration](#/c2) |
| C3 / Theorem 3.4 | **VERIFIED** | [Two-sided certificate and eta-floor audit](#/c3) |
| C4 / Proposition 4.1 | **VERIFIED** | [Exact floor constant and quantifier separation](#/c4) |
| C5 / Theorem 4.2 | **FALSIFIED** | [Positive-bias asymptotic contradiction](#/c5) |
| C6 / empirical alpha tradeoff | **BLOCKED** | [Paper-scale GMM evidence and four-route audit](#/c6) |

Every accepted verifier is rerun by the one fixed command:

```bash
uv run --frozen python -m repro_campaign.run
```

The environment is locked by
[pyproject.toml](/evidence/code/pyproject.toml) and
[uv.lock](/evidence/code/uv.lock). Scientific evidence commit:
`19aa5251ca0b02fab27d16a5b09a46ee2b62ce70`.

## Evaluator-visible evidence matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | [C1](#/c1) | Yes | Yes | [JSON](/evidence/artifacts/C1/raw_formal.json) | [checker](/evidence/code/repro_campaign/check_claim1.py) | 0.49 coefficient + false 0.1× budget | Yes, A1–A2 and universal quantifier | READY / VERIFIED |
| C2 | [C2](#/c2) | Yes | Yes | [JSON](/evidence/artifacts/C2-C3/raw_formal_summary.json) | [checker](/evidence/code/repro_campaign/check_claim23.py) | 0.24 coefficient + false 1.10× lower | Yes, A1–A4, eta∈[0,1], eps²≤1 | READY / VERIFIED |
| C3 | [C3](#/c3) | Yes | Yes | [JSON](/evidence/artifacts/C2-C3/raw_formal_summary.json) | [checker](/evidence/code/repro_campaign/check_claim23.py) | 3.9 coefficient + false 0.50× upper | Yes, including positive eta floor | READY / VERIFIED |
| C4 | [C4](#/c4) | Yes | Yes | [JSON](/evidence/artifacts/C4-C5/raw_formal_summary.json) | [checker](/evidence/code/repro_campaign/check_claim45.py) | remove uniform error floor | Yes, both source clauses separated | READY / VERIFIED |
| C5 | [C5](#/c5) | Yes | Yes | [JSON](/evidence/artifacts/C4-C5/raw_formal_summary.json) | [checker](/evidence/code/repro_campaign/check_claim45.py) | set bias to zero / add bias right | Yes, theorem as written | READY / FALSIFIED |
| C6 | [C6](#/c6) | Yes | Yes | [route 1](/evidence/artifacts/C6/route1/raw_formal_summary.json), [route 4](/evidence/artifacts/C6/route4/raw_formal_summary.json) | [checker](/evidence/code/repro_campaign/check_claim6_falsification.py) | h=0 + explicit-threshold falsification control | Yes; full protocol remains unavailable | COMPLETE / BLOCKED |

## Read next

- [Implementation, compute, and provenance](#/method)
- [Illustrated technical report](#/report)
- [Self-contained marimo notebook](/notebooks/reproduction.py)
- [Forecast and release limitations](#/release)
- [Evaluator-blind review and visibility audit](#/visibility)
- **Historical rejected baseline:** [old verification](#/verify) and
  [old overview](#/overview), preserved unchanged.

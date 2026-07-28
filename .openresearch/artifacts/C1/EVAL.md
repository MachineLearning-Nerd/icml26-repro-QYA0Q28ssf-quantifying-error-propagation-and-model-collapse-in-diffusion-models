# Current verification — C1 / Proposition 3.1

Status before confirmation run: **exact certificate accepted; first estimator route
rejected; fresh-seed calibration pending**.

Exact command inherited by this node:

```bash
uv run --frozen python -m repro_campaign.run
```

Current executable sources:

- `repro_campaign/claim1_girsanov.py` — proof rule graph and 10D calibration.
- `repro_campaign/check_claim1.py` — standalone certificate checker.
- `repro_campaign/run.py` — cumulative nonzero-on-failure entrypoint.

The committed preflight accepts the exact A1–A2 proof route and rejects the
coefficient-corrupted control. The first formal numerical run is preserved as a
rejected route because its all-upper-confidence gate was in the wrong statistical
direction. The confirmation run uses five fresh seeds, tests for a significant
violation with one-sided intervals, and must reject a false 0.1× budget before the
result is promoted on the evaluator-visible page.

# Current verification — C1 / Proposition 3.1

Status before formal run: **certificate VERIFIED; 10D calibration pending**.

Exact command inherited by this node:

```bash
uv run --frozen python -m repro_campaign.run
```

Current executable sources:

- `repro_campaign/claim1_girsanov.py` — proof rule graph and 10D calibration.
- `repro_campaign/check_claim1.py` — standalone certificate checker.
- `repro_campaign/run.py` — cumulative nonzero-on-failure entrypoint.

The committed preflight accepts the exact A1–A2 proof route and rejects the
coefficient-corrupted control. The formal OpenResearch run must still reproduce this
output, execute the 10D calibration, print raw numerical rows, and exit zero before
the result is promoted on the evaluator-visible page.

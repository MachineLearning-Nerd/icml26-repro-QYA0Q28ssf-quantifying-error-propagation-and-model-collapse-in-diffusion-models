# Current verification — C2 and C3

Pre-run status: **proof certificates and exact calibration implemented; formal
OpenResearch run pending**.

Exact inherited command:

```bash
uv run --frozen python -m repro_campaign.run
```

Executable sources are `repro_campaign/claim23_observability.py` and the standalone
`repro_campaign/check_claim23.py`. The run must print all eta, energy, chi-squared,
assumption, quadrature, and control rows and exit zero before evaluator promotion.

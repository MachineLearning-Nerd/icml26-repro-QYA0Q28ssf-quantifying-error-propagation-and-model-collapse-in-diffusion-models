# Current verification — C1 / Proposition 3.1

Final scientific status: **VERIFIED**.

Exact command inherited by this node:

```bash
uv run --frozen python -m repro_campaign.run
```

Current executable sources:

- `repro_campaign/claim1_girsanov.py` — proof rule graph and 10D calibration.
- `repro_campaign/check_claim1.py` — standalone certificate checker.
- `repro_campaign/run.py` — cumulative nonzero-on-failure entrypoint.

HF run `3621fc83-117d-44b8-9b88-c04406773d68` at commit
`20bf5fed2d69b8b16017516b6bfe70b03b9bf816` accepted the exact A1–A2 certificate
and rejected the coefficient-0.49 mutation. Across five fresh seeds and 20,000
trajectories per beta, neither endpoint estimator significantly violated the exact
path-KL budget; both rejected a false 0.1× budget. The first numerical route remains
preserved as rejected because its all-upper-confidence gate had the wrong
statistical direction.

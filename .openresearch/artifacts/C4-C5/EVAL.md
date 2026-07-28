# Current verification — C4 and C5

Pre-run status: **C4 proof and C5 falsification certificates implemented; formal
OpenResearch run pending**.

Exact inherited command:

```bash
uv run --frozen python -m repro_campaign.run
```

The evaluator must distinguish C4's two quantifiers and must read C5 against the
paper's explicit definition of `asymp`. The cumulative verifier exits nonzero if a
floor is inferred without a uniform per-step error floor, or if either mutation
removes the C5 contradiction.

# C6 route 4 — falsification search

Pre-run status: **formal cumulative run pending**.

The exact inherited command is:

```bash
uv run --frozen python -m repro_campaign.run
```

Expected honest result: BLOCKED unless the independent checker accepts a candidate
that both satisfies every fixed assumption and contradicts a decidable paper
statement.

# C6 route 4 — falsification search

Final route status: **BLOCKED after mandatory falsification search**.

The exact inherited command is:

```bash
uv run --frozen python -m repro_campaign.run
```

HF run `85ae6557-fa40-4a59-a263-42179b145cbb` at commit
`19aa5251ca0b02fab27d16a5b09a46ee2b62ce70` accepted no candidate
counterexample. The h=0 candidate contradicts the ordering but violates the paper's
fixed h=0.6; the population route aligns; CIFAR eta is a different observable; and
“stable” has no numerical threshold. The same checker correctly accepts a synthetic
explicit-threshold contradiction, showing that the gate is non-vacuous.

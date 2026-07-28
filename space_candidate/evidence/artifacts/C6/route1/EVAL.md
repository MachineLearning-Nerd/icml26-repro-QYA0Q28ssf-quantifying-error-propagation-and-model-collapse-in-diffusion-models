# C6 route 1 — full-scale population-KDE GMM

Final route status: **ALIGNED on the population-KDE GMM; C6 remains BLOCKED**.

Exact inherited command:

```bash
uv run --frozen python -m repro_campaign.run
```

HF run `aa8213ff-934e-4c9b-b898-669f3e7859a7` at commit
`6bdd221a95fa1782cc0816d79aaaf3e0a63f5ea6` used ten seeds and nine million
checkpoint samples. Generation-20 total-second-moment drift was `108.38%`, `24.72%`,
and `13.77%` for alpha `0.1`, `0.5`, and `0.9`; confidence intervals preserve that
order. The h=0 control removes alpha-dependent accumulation. The exact population
endpoint replaces the paper's unpublished 100,000-center KDE acceleration and
500-step solver, so this cannot verify the image portion or full C6.

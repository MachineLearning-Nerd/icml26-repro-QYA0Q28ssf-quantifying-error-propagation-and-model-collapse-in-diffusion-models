# Current verification — C4 and C5

Final scientific status: **C4 VERIFIED; C5 FALSIFIED as written**.

Exact inherited command:

```bash
uv run --frozen python -m repro_campaign.run
```

HF run `1a6f4c55-710c-44cb-b108-e281f7f6ce80` at commit
`a6ace14d8ab3a444861e439e687da44af80586fd` accepted both certificates. C4's
uniform-floor mutation is rejected. For C5, the minimum required upper
multiplicative constant grows from `26.84` at `N=10` to `1.43e15` at `N=160`;
changing `C_bias` to zero or placing it on the right removes the contradiction and
is correctly rejected as falsification.

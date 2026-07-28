# Current verification — C2 and C3

Final scientific status: **C2 VERIFIED; C3 VERIFIED**.

Exact inherited command:

```bash
uv run --frozen python -m repro_campaign.run
```

HF run `29594092-3b31-4ea6-ac75-57b13f571bbe` at commit
`82ebd6a282101409cde92fbf81fb1dedbd08a386` accepted the exact certificates and
rejected lower-coefficient 0.24 and upper-coefficient 3.9 mutations. The exact
Gaussian and non-Gaussian calibration spans eta from zero to one; all A1–A4 audits
pass, quadrature disagreement is at most `6.94e-18`, and deliberately false
numerical lower and upper bounds are detected.

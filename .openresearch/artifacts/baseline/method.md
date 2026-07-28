# Historical rejected baseline

This node reconstructs the visible numerical checks at the exact judged Space
revision. It deliberately does not call them full reproductions. The one-dimensional
Gaussian mean-shift identities and scalar recurrence are retained only as regression
tests while faithful children replace them.

Fixed command:

```bash
uv run --frozen python -m repro_campaign.run
```

The command is inherited unchanged by every child. Variants are committed in code and
configuration. The baseline seed is 1729.

Compute estimate before run: one active core for the verifier, but dependency installation
has uncertain duration. Per policy the selected backend is Hugging Face `cpu-upgrade`,
whose advertised allocation is 8 vCPU, 32 GB RAM, and 50 GB storage. Every HF node uses
the fixed official image `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`; the default HF
Python image was rejected during setup because it did not contain the required `uv` binary.

# Campaign command ledger

This ledger records the reproducibility-relevant commands used by the campaign.
Read-only inspection commands that differ only by output range (for example
`sed -n`, `orx logs --range`, or `git diff`) are grouped by command family.
Secrets and generated backend wrappers are intentionally never recorded.

## Startup and source capture

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx project view 4b629ed4-f323-4dc7-8cca-8ee67cab1a09
orx runs 4b629ed4-f323-4dc7-8cca-8ee67cab1a09
git branch -a
git rev-parse HEAD
git status --short
df -h .
env | sed 's/=.*//' | LC_ALL=C sort
curl -L -A 'OpenResearch-Reproduction/1.0 (paper audit; contact via repository)' https://ar5iv.labs.arxiv.org/html/2602.16601
curl -L -A 'OpenResearch-Reproduction/1.0 (paper audit; contact via repository)' https://export.arxiv.org/e-print/2602.16601v2
shasum -a 256 paper.html paper-source.tar
```

The paper hashes are `472fb9e…` for the retrieved HTML and `c25e50…` for the
v2 TeX archive. The live verdict was selected only after filtering
`space_id == "DineshAI/QYA0Q28ssf"`. The judged Space revision
`49401cddb554d5c3f7ae98d400567b8d6f10c028` was downloaded before candidate
work and its 15-path SHA-256 manifest was frozen.

## Fixed environment and command

```bash
uv lock
uv sync --frozen
orx project edit 4b629ed4-f323-4dc7-8cca-8ee67cab1a09 --run-command 'uv run --frozen python -m repro_campaign.run'
uv run --frozen python -m repro_campaign.run
```

Every formal node inherited exactly:

```bash
uv run --frozen python -m repro_campaign.run
```

## Experiment orchestration

Every branch was created with `orx create-experiment`, checked out with
`git fetch origin && git checkout <branch>`, committed, pushed, launched, waited
for, and read through the following command families:

```bash
orx create-experiment 4b629ed4-f323-4dc7-8cca-8ee67cab1a09 --title '<title>' [--parent <experiment-id>]
git fetch origin
git checkout <experiment-branch>
git add <scoped-paths>
git commit -m '<scientific change>'
git push origin <experiment-branch>
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp wait <experiment-id> --timeout 480
orx runs 4b629ed4-f323-4dc7-8cca-8ee67cab1a09 --experiment <experiment-id>
orx logs <run-id>
orx exp desc <experiment-id> --set '<evidence summary>'
```

The important immutable scientific tips are listed in the main report. All formal
CPU runs requested `cpu-upgrade`, estimated eight active CPU workers, and used no
GPU.

## Candidate and publication checks

```bash
uv run --frozen marimo check --strict notebooks/reproduction.py
python3 -m py_compile notebooks/reproduction.py
git diff --check
python3 scripts/evaluator_blind_review.py --root <fresh-candidate-directory> --output <review.json>
uv run --frozen python -m repro_campaign.run
python3 scripts/publish_space_text.py --root space_candidate --expected-parent 49401cddb554d5c3f7ae98d400567b8d6f10c028
git ls-remote origin refs/heads/main
```

The publication script reads UTF-8 from every allowlisted path, verifies the
protected parent revision, and performs one additive commit to the existing Space.
It cannot create a second Space and never prints credentials.

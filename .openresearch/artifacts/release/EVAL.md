# Cumulative release evaluation

## Honest claim status

| Claim | Verdict | Confidence | Evaluator-visible location |
| --- | --- | --- | --- |
| C1 | VERIFIED | HIGH | `space_candidate/pages/claims/c1.md` |
| C2 | VERIFIED | MEDIUM | `space_candidate/pages/claims/c2.md` |
| C3 | VERIFIED | MEDIUM | `space_candidate/pages/claims/c3.md` |
| C4 | VERIFIED | HIGH | `space_candidate/pages/claims/c4.md` |
| C5 | FALSIFIED | HIGH | `space_candidate/pages/claims/c5.md` |
| C6 | BLOCKED | LOW | `space_candidate/pages/claims/c6.md` |

Previous live score is 5/12. The conservative projected range is 8–10/12 and the
best-supported possible score is 10/12. Both are forecasts; only a later live judge
can change the score.

## Gates

- The fixed command is `uv run --frozen python -m repro_campaign.run`.
- All accepted claim checks rerun cumulatively and fail the process on failure.
- The judged 15-path Space tree is a subset of the candidate tree.
- Original current pages are preserved byte-for-byte and labeled exactly
  `Historical rejected baseline`; the root navigation now points first to current
  verification.
- All uploaded paths are UTF-8 text, explicitly allowlisted, and SHA-256 hashed.
- The evaluator-visible traversal begins at `README.md`, `logbook.json`, and
  `pages/index.md`.
- C6 contains exactly three materially distinct verification routes followed by a
  mandatory assumption-satisfying falsification route. No route justified a pass.

The fresh-overlay evaluator-blind traversal passed after two concrete navigation
fix rounds. The release remains blocked only until the cumulative candidate node
passes on Hugging Face `cpu-upgrade`.

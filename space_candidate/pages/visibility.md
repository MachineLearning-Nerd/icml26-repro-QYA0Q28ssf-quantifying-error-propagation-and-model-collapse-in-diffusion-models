# Evaluator-blind visibility audit

The review starts only from `README.md`, `logbook.json`, and `pages/index.md`. It
does not use OpenResearch logs, hidden branches, or repository knowledge.

## First-pass traversal

Files opened in order:

1. `README.md`
2. `pages/index.md`
3. `pages/claims/c1.md` through `c6.md`
4. `pages/method.md`
5. each linked claim contract, source audit, raw JSON, checker, and control
6. `pages/release.md`
7. historical `pages/verify/page.md` and `pages/overview/page.md`

The old pages were initially liable to look current. Fix: current verification is
first in navigation, and the old group is labeled exactly **Historical rejected
baseline**. Each current page names its superseding scientific commit.

The first fresh-overlay automated review opened 52 files and rejected the candidate:
some claim pages exposed the command, runtime, or assumption audit only implicitly,
and one historical link targeted a directory rather than a file. The release was
not advanced. Fixes added explicit plain-language labels to every claim page and
changed the historical link to the preserved `README.md`. A second pass found one
remaining directory target on the method page. After that target was fixed, a third
newly assembled overlay passed: 53 files opened, six claim pages complete, and zero
missing or incomplete targets. [Raw review
record](/evidence/artifacts/release/red_team_release_pass.json).

## Release-pass conclusion

| Claim | Exact source/assumptions | Code | Inline numbers | Raw | Checker | Control | Limits | Result discoverable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED |
| C2 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED |
| C3 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED |
| C4 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED |
| C5 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | FALSIFIED |
| C6 | Yes | Yes | Yes | Yes | Yes | Yes | Yes | BLOCKED |

No scientific gap is hidden by navigation. C6's missing capability is visible on its
canonical page. The current verifier is the obvious verifier; historical toy code is
not labeled “Verification run.”

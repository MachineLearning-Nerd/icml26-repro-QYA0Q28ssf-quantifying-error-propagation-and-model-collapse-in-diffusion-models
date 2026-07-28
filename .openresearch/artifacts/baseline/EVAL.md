# Baseline evaluation contract

Expected outcome: `5/12` historical judged state, with C1–C5 labeled `TOY` and C6
labeled `BLOCKED`. This baseline must never be presented as the current verifier after
faithful evidence is added.

The current runner exits nonzero if:

- an accepted numerical check fails;
- a historical status is promoted;
- the deliberately wrong identity `KL = eps^2` is not rejected.

Limitations: no trained diffusion model, no nontrivial target family, no arbitrary
observability coefficient, and no image dataset. Those limitations are the hypothesis
for the next experiment round.

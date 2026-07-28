# C1 limitations and deviations

- The paper does not release code or raw trajectories; this is an independent implementation.
- The controlled calibration perturbation is not a trained KDE score. It is bounded,
  state-dependent, and chosen so A1–A2 can be audited numerically without circularity.
- Endpoint KL is estimated, so both estimator uncertainty and a 2% path-budget
  discretization allowance are reported.
- The universal verdict rests on the proof certificate; empirical agreement is scoped
  corroboration only.

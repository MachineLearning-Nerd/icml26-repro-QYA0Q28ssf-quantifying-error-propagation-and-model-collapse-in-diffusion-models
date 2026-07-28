# C6 route 4 limitations and deviations

- The population-KDE route is not the literal empirical-KDE/500-step solver.
- The h=0 control violates the paper's fixed bandwidth.
- “Stable” has no published numerical tolerance, so 13.77% drift under a
  substituted solver cannot be promoted to a contradiction.
- CIFAR observability is not CIFAR distributional drift.
- The search found no valid assumption-satisfying counterexample; C6 remains
  BLOCKED rather than being mislabeled FALSIFIED.

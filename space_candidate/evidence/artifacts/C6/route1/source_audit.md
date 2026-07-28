# C6 route 1 source audit

The paper's Figure 1 and Appendix G.1 specify a five-component 10D GMM, component
standard deviation `0.6`, KDE bandwidth `h=0.6`, `N=100,000`, 500 reverse
Euler–Maruyama steps, 20 generations, `alpha={0.1,0.5,0.9}`, and 10 runs.

The source does not specify how the score of a 100,000-center KDE is evaluated during
the resulting billions of trajectory steps. A literal implementation entails
trillions of center-query distances. The authors publish neither code nor an
acceleration/truncation rule.

This route takes a defensible population-limit interpretation. Convolution by the
KDE kernel is exact at the endpoint, so the per-coordinate within-mode variance is

`v_n = sigma^2 + h^2*(1-(1-alpha)^n)/alpha`.

It preserves the paper's geometry, sample count used for uncertainty, generation
horizon, alpha values, and number of runs, but not the empirical finite-center or
500-step numerical approximations.

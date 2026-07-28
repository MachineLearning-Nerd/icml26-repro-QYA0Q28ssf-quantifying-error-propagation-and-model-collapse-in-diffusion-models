# C1 method

The verifier has two deliberately separated routes.

1. **Proof route.** A machine-readable certificate reconstructs the Girsanov
   log-density under the learned measure, centers its Itô integral, derives the
   path-space KL identity, and applies data processing to the endpoint. An independent
   allowlisted rule checker verifies dependency order, source anchors, and the exact
   coefficient `1/2`.
2. **Calibration route.** The paper's 10D five-component GMM is sampled with 500
   Euler–Maruyama reverse steps from `T=4` to `t0=0.02`. The controlled learned-score
   error is `beta*tanh(x)`, which is bounded and state-dependent. Five deterministic
   seeds and 20,000 trajectories per beta are used. Endpoint KL is estimated by
   cross-fitted quadratic logistic density-ratio estimation and an independent,
   null-bias-corrected k-nearest-neighbor estimator.

For `e(x,t)=beta*tanh(x)`, `||e||^2 <= 10 beta^2`; hence A1 holds and Novikov's
sufficient condition for A2 is bounded by
`exp(0.5 * 10 * beta^2 * (4-0.02))`.

The finite calibration is not used as proof. It is a non-Gaussian, state-dependent,
paper-dimension implementation check that should expose sign, factor, or
discretization errors in the derivation.

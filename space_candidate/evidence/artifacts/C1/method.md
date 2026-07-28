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
   fresh confirmation seeds and 20,000 trajectories per beta are used. Endpoint KL is estimated by
   cross-fitted quadratic logistic density-ratio estimation and an independent,
   null-bias-corrected k-nearest-neighbor estimator.

The first numerical route required every estimator's upper 95% confidence value to
fall below the path budget. That is not a valid contradiction test: a noisy unbiased
estimate near a true upper bound can fail it routinely. That route is preserved in
`rejected_estimator_route.json`. The replacement contract was fixed before seeing
the five new seeds. It flags a contradiction only when an endpoint estimator's
one-sided 95% lower confidence bound exceeds the Monte Carlo path budget's one-sided
95% upper confidence bound. As a sensitivity control, both estimators must reject a
false budget equal to 10% of the real path budget for every beta.

For `e(x,t)=beta*tanh(x)`, `||e||^2 <= 10 beta^2`; hence A1 holds and Novikov's
sufficient condition for A2 is bounded by
`exp(0.5 * 10 * beta^2 * (4-0.02))`.

The finite calibration is not used as proof, and failure to reject a contradiction
does not verify an inequality. It is a non-Gaussian, state-dependent,
paper-dimension implementation check that should expose sign or factor errors in
the derivation. The exact discrete transition KL is the reported path budget; no
ad hoc discretization allowance is used.

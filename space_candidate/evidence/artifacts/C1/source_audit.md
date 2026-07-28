# C1 source audit

Source HTML SHA-256:
`472fb9e246aea7c5d1e643d5755f034f005d1f2bbb61f86371bae855f62765e3`.

- A1 (`#S3.I1.i1`): the learned-path energy
  `E_P_hat integral ||e_i(Y_hat_s,s)||^2 ds` is finite.
- A2 (`#S3.I1.i2`): the Girsanov exponential is a true martingale.
- Proposition 3.1 (`#S3.Thmtheorem1`): under A1–A2,
  `KL(p_hat^{i+1} || q_i) <= KL(P_hat_i || P_star_i) = eps_hat_i^2/2`.

The first inequality is data processing under endpoint marginalization. The equality
is path-space Girsanov KL, evaluated under the learned measure. The claim is universal
over eligible generations; no finite collection of simulations can prove it.

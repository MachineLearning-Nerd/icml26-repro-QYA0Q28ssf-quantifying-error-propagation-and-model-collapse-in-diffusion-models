# C2–C3 source audit

Source HTML SHA-256:
`472fb9e246aea7c5d1e643d5755f034f005d1f2bbb61f86371bae855f62765e3`.

- Definition 3.2 (`#S3.Thmtheorem2`) defines
  `eta = Var(E[M_T|Y_t0])/eps_star^2` with the zero-energy convention `eta=0`.
- A3 (`#S3.I2.i3`) requires a uniform `L^(1+delta)` moment of `exp(Z)`,
  for some `delta>1`.
- A4 (`#S3.I2.i4`) requires a normalized `(2+gamma)` moment of quadratic
  variation, with `gamma>max(2,4/(delta-1))`.
- Proposition 3.3 (`#S3.Thmtheorem3`) is universal over eligible `i>=i0`,
  assumes A1–A4 and `eps_star^2<=1`, and states the `1/4` lower bound with
  an `O(eps_star^4)` remainder. Its clean regime has coefficient `1/8`.
- Theorem 3.4 (`#S3.Thmtheorem4`) adds the upper coefficient `4`; equivalence
  additionally requires a uniform positive observability floor and sufficiently
  small error.

The paper's constants depend on the A3–A4 moment constants. A finite experiment
cannot establish either universal statement; the checked derivation carries those
quantifiers.

# C4–C5 source audit

Hashed source:
`472fb9e246aea7c5d1e643d5755f034f005d1f2bbb61f86371bae855f62765e3`.

## Proposition 4.1

Anchor `#S4.Thmtheorem1` has two distinct clauses.

1. A divergent score-energy series implies only that `sum D_i` diverges.
2. The explicit nonzero `limsup` floor additionally assumes an eventual pointwise
   score-energy floor.

The imported judge-claim wording merges these clauses. Divergence of a positive
series alone does not prevent its terms—and a corresponding non-summable `D_i`—from
tending to zero.

## Theorem 4.2

Anchor `#S4.Thmtheorem2` assumes A1–A5, positive observability, perturbative errors,
and `sum eps_star_i^2<infinity`. It states that a constant `C_bias>0` exists and

`D_(N+1)+C_bias asymp discounted_sum_N + decayed_initial_N`.

The paper defines `f asymp g` as two multiplicative inequalities with constants
`0<c1<=c2<infinity`. Under summability and `alpha>0`, both terms on the displayed
right side tend to zero. The left side is at least the stated positive `C_bias`.
Thus the upper multiplicative inequality is impossible.

The appendix does not prove the displayed equivalence. Equation
`regC-equivalence-bias` gives a lower inequality with a signed initial term and an
upper inequality `D_N <= decayed_initial + discounted_sum + C_bias`. Those are
potentially useful additive stability bounds, but they are not the main theorem as
written.

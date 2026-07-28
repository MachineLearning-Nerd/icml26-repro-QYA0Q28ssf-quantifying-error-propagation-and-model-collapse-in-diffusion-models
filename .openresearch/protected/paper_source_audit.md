# Paper source audit

- Paper: arXiv `2602.16601v2`, *Quantifying Error Propagation and Model Collapse in Diffusion Models*
- HTML URL: `https://ar5iv.labs.arxiv.org/html/2602.16601`
- Retrieved with an explicit browser User-Agent: 2026-07-28
- HTML SHA-256: `472fb9e246aea7c5d1e643d5755f034f005d1f2bbb61f86371bae855f62765e3`
- TeX source URL: `https://export.arxiv.org/e-print/2602.16601v2`
- TeX source SHA-256: `c25e50d4fe4c1a730754e525f3065754bc75232d0d3bb890f1a383e738b7bffa`
- Version metadata: submitted 2026-02-18; revised 2026-05-28; accepted at ICML 2026.

## Exact anchors

| Item | HTML anchor | Quantified statement |
| --- | --- | --- |
| A1 | `#S3.I1.i1` | Learned-path drift energy is finite. |
| A2 | `#S3.I1.i2` | The Girsanov exponential is a true martingale. |
| Proposition 3.1 | `#S3.Thmtheorem1` | Under A1–A2, endpoint KL is at most one half learned-path energy. |
| Definition 3.2 | `#S3.Thmtheorem2` | `eta_i = Var(E[M_T^i | Y_t0]) / eps_star_i^2` in `[0,1]`. |
| A3 | `#S3.I2.i3` | A uniform `L^(1+delta)` bound on the Girsanov density for `delta > 1`. |
| A4 | `#S3.I2.i4` | A uniform normalized `(2+gamma)` quadratic-variation moment bound. |
| Proposition 3.3 | `#S3.Thmtheorem3` | For every `i >= i0` satisfying A1–A4 and `eps_star_i^2 <= 1`, chi-squared divergence is at least `eta_i eps_star_i^2 / 4 - C eps_star_i^4`. |
| Theorem 3.4 | `#S3.Thmtheorem4` | For every eligible `i`, the lower bound and `chi2 <= 4 eps_star_i^2 + c eps_star_i^4` hold in the stated perturbative regime. |
| Proposition 4.1 | `#S4.Thmtheorem1` | Non-summable score energy implies non-summable global drift; a uniform score-energy floor implies the displayed limsup floor. |
| A5 | `#S4.I1.i5` | A uniform adaptive-tail moment bound holds from `i0`. |
| Theorem 4.2 | `#S4.Thmtheorem2` | Under A1–A5, uniform positive observability, perturbative errors, and summable score energies, Equation (23) holds for every `N >= i0`. |
| GMM protocol | `#A7.SS1` | 10D, five components, `sigma=h=0.6`, `N=100000`, 500 Euler–Maruyama steps, `T=4`, `t0=0.02`, 20 generations, alphas 0.1/0.5/0.9, 10 independent runs. |

Finite experiments are calibration evidence, not proof of universal quantifiers. A final
`VERIFIED` theorem verdict therefore requires an independent proof reconstruction or a
machine-checkable certificate in addition to empirical calibration. A valid falsification
must satisfy every listed assumption.

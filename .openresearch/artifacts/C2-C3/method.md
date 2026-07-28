# C2–C3 method

The proof route reconstructs the conditional Girsanov density ratio, second-order
exponential expansion, two weighted Young inequalities, observability transfer,
Hölder/BDG remainder control, and the upper second-moment argument. SymPy independently
collects the exact leading and quartic coefficients. Separate mutations change `1/4`
to `0.24` and `4` to `3.9`; both must be rejected.

The calibration is an exact continuous diffusion on `[0,1]`:

`Y_t = X + W_t`,

with deterministic drift error

`e(t)=beta*(sqrt(rho)+sqrt(1-rho)*sqrt(2)*sin(2*pi*t))`.

The constant and sinusoidal terms are orthonormal in time. Consequently, path energy
is exactly `beta^2`, while only the constant component shifts the endpoint, by
`beta*sqrt(rho)`. The observability coefficient is
`rho*Var(E[W_1|X+W_1])`, equal to `rho` times the endpoint Fisher information.

Two endpoint families are used: `X=0`, which analytically spans `eta` from zero to
one, and `X` uniform on `{-3,+3}`, whose endpoint is a non-Gaussian Gaussian mixture.
Chi-squared divergence and mixture Fisher information are computed by independently
refined deterministic quadrature. Here A3 is exact with `delta=3`,
`E[exp((1+delta)Z)]=exp(delta*(1+delta)*beta^2/2)`, and A4 holds with
`gamma=3`, `K_gamma=1` because quadratic variation is deterministic.

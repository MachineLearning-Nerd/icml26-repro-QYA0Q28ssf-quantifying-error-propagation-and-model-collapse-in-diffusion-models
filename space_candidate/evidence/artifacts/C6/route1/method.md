# C6 route 1 method

At generation `n`, the population KDE distribution is a mixture over kernel ages.
For ages `k<n`, weights are `alpha*(1-alpha)^(k-1)`; the oldest component has weight
`(1-alpha)^(n-1)`. Every age adds `k*h^2` to the original component variance.

For each alpha and each of ten deterministic seeds, 100,000 10D points are sampled
at generations 0, 10, and 20. Known mixture labels permit an unbiased
within-component dispersion estimate. Total second moment and residual-radius
quantiles provide independent drift diagnostics. All 21 population generations are
reported analytically.

The negative control sets `h=0`. With no score-estimation blur, every alpha curve
must remain at the data variance and the tradeoff must disappear.

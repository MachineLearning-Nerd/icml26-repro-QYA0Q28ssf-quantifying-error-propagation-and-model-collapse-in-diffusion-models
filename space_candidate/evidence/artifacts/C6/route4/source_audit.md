# C6 route 4 source audit — falsification target

Figure 1 and Appendix G.1 fix the GMM protocol: 10 dimensions, five components,
component sigma and KDE bandwidth 0.6, 100,000 training samples, 500 Euler-Maruyama
steps from `T=4` to `t0=0.02`, 20 generations, alpha in `{0.1,0.5,0.9}`, and ten
independent runs.

The source qualitatively orders dispersion at generation 20: alpha 0.1 disperses,
alpha 0.5 moderately degrades, and alpha 0.9 remains stable. It publishes no
maximum drift compatible with “stable.” Figure 8 provides a qualitative image
ordering. Figure 9 reports CIFAR-10 observability, a different quantity.

A counterexample must honor the fixed protocol and reverse that ordering, or exceed
an explicit source threshold. Missing settings, h=0, a solver substitution, or
overlapping observability curves cannot meet that standard.

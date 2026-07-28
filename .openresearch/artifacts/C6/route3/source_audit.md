# C6 route 3 source audit — CIFAR-10

Appendix G.3 names both Fashion-MNIST and CIFAR-10, but its training setup is
explicitly introduced as Fashion-MNIST: 28×28 grayscale, 50,000 samples. The shared
metric paragraphs name both datasets. CIFAR-10 has one dedicated result, Figure 9:
post-transient observability around 0.25–0.35, with generation zero explicitly a
placeholder.

The source does not attach a CIFAR-10 image shape, training count, U-Net
configuration, epoch schedule, seeds, feature-classifier checkpoint, feature
dimension, covariance regularizer, or observability regressor architecture. It says
the observability procedure is the same as the GMM procedure; we therefore inherit
its 50,000-trajectory count. The subsection-wide
statement `d=784` matches Fashion-MNIST but
not CIFAR-10's 32×32×3 = 3072 coordinates. We record this as ambiguous scope, not a
counterexample.

No published CIFAR-10 panel or numerical curve directly shows the imported
low-alpha-collapse/high-alpha-stability claim. Figure 9 instead reports that the
three alpha observability curves overlap substantially.

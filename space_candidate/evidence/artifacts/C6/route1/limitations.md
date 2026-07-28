# C6 route 1 limitations and deviations

- Population KDE replaces the unspecified finite 100,000-center KDE acceleration.
- Exact endpoint sampling replaces 500 Euler–Maruyama steps.
- The route measures the GMM mechanism only; it has no Fashion-MNIST or CIFAR-10
  trained model.
- A positive result is aligned evidence, not full verification of C6.

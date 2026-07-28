# C6 route 2 source audit — Fashion-MNIST

The source specifies dataset size, image size, U-Net family, residual blocks,
group normalization, SiLU, sinusoidal time embedding, dropout, EMA, optimizer,
learning rate, weight decay, cosine schedule, epoch counts, ten generations, three
alpha values, and 1000-step sampling.

It does not specify U-Net width, channel multipliers, number of residual blocks,
attention placement, batch size, DDPM beta schedule, training diffusion horizon,
data normalization, random seeds, validation split, or the early-stopping metric and
minimum improvement. These choices materially change both results and runtime.

The stated maximum workload processes 160 million training examples and 750 million
image-timestep sampler evaluations before observability regressors and metrics.

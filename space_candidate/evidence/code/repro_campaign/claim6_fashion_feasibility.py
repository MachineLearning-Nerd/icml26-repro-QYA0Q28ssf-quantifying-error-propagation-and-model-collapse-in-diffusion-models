"""C6 route 2: Fashion-MNIST identifiability and CPU lower-bound audit."""

from __future__ import annotations

import math
import time
from typing import Any


REQUIRED_PROTOCOL_FIELDS = (
    "base_channels",
    "channel_multipliers",
    "residual_blocks_per_level",
    "attention_resolutions",
    "batch_size",
    "ddpm_beta_schedule",
    "training_diffusion_steps",
    "data_normalization",
    "random_seeds",
    "validation_split",
    "early_stopping_metric_and_delta",
)

PAPER_PROTOCOL: dict[str, Any] = {
    "dataset": "Fashion-MNIST",
    "training_samples": 50_000,
    "image_shape": [1, 28, 28],
    "architecture_family": "U-Net",
    "normalization": "group normalization",
    "activation": "SiLU",
    "time_embedding": "sinusoidal plus 2-layer MLP",
    "dropout": 0.1,
    "ema_decay": 0.99,
    "base_epochs": 200,
    "recursive_epochs": 100,
    "recursive_generations_per_alpha": 10,
    "alphas": [0.1, 0.5, 0.9],
    "optimizer": "AdamW",
    "learning_rate": 2e-4,
    "weight_decay": 1e-4,
    "scheduler": "cosine",
    "sampling_steps": 1000,
    "early_stopping_patience_epochs": 50,
}


def _missing_fields(protocol: dict[str, Any]) -> list[str]:
    return [field for field in REQUIRED_PROTOCOL_FIELDS if field not in protocol]


def _benchmark_tiny_denoiser() -> dict[str, Any]:
    import torch

    torch.manual_seed(8675309)
    torch.set_num_threads(8)
    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, 8, kernel_size=3, padding=1),
        torch.nn.SiLU(),
        torch.nn.Conv2d(8, 8, kernel_size=3, padding=1),
        torch.nn.SiLU(),
        torch.nn.Conv2d(8, 1, kernel_size=3, padding=1),
    )
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    batch_size = 64
    inputs = torch.randn(batch_size, 1, 28, 28)
    targets = torch.randn_like(inputs)
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

    for _ in range(5):
        optimizer.zero_grad(set_to_none=True)
        loss = torch.nn.functional.mse_loss(model(inputs), targets)
        loss.backward()
        optimizer.step()
    train_steps = 50
    started = time.perf_counter()
    for _ in range(train_steps):
        optimizer.zero_grad(set_to_none=True)
        loss = torch.nn.functional.mse_loss(model(inputs), targets)
        loss.backward()
        optimizer.step()
    train_seconds = time.perf_counter() - started
    train_images_per_second = batch_size * train_steps / train_seconds

    inference_steps = 200
    started = time.perf_counter()
    with torch.no_grad():
        for _ in range(inference_steps):
            model(inputs)
    inference_seconds = time.perf_counter() - started
    inference_images_per_second = batch_size * inference_steps / inference_seconds
    return {
        "torch_threads": torch.get_num_threads(),
        "model": "three 3x3 convolutions with width 8; no residual blocks or U-Net hierarchy",
        "parameter_count": parameter_count,
        "batch_size": batch_size,
        "training_benchmark_steps": train_steps,
        "training_seconds": train_seconds,
        "training_images_per_second": train_images_per_second,
        "inference_benchmark_steps": inference_steps,
        "inference_seconds": inference_seconds,
        "inference_images_per_second": inference_images_per_second,
        "strict_lower_bound_reason": (
            "This 1->8->8->1 network omits the paper's U-Net hierarchy, residual "
            "blocks, group normalization, time MLP, dropout, and EMA."
        ),
    }


def run() -> dict[str, Any]:
    missing = _missing_fields(PAPER_PROTOCOL)
    completed_control = dict(PAPER_PROTOCOL)
    completed_control.update(
        {
            "base_channels": 64,
            "channel_multipliers": [1, 2, 4],
            "residual_blocks_per_level": 2,
            "attention_resolutions": [14],
            "batch_size": 64,
            "ddpm_beta_schedule": "linear 1e-4 to 0.02",
            "training_diffusion_steps": 1000,
            "data_normalization": "[-1,1]",
            "random_seeds": [1, 2, 3],
            "validation_split": "5000 fixed training examples",
            "early_stopping_metric_and_delta": "validation MSE, min_delta=1e-5",
        }
    )
    control_missing = _missing_fields(completed_control)
    benchmark = _benchmark_tiny_denoiser()

    training_examples = 50_000 * 200 + 3 * 10 * 50_000 * 100
    synthetic_images = sum(
        (1.0 - alpha) * 50_000 * 10 for alpha in PAPER_PROTOCOL["alphas"]
    )
    sampling_image_steps = synthetic_images * PAPER_PROTOCOL["sampling_steps"]
    training_lower_seconds = (
        training_examples / benchmark["training_images_per_second"]
    )
    sampling_lower_seconds = (
        sampling_image_steps / benchmark["inference_images_per_second"]
    )
    lower_bound_seconds = training_lower_seconds + sampling_lower_seconds
    if not missing:
        raise AssertionError("paper Fashion protocol unexpectedly became identifiable")
    if control_missing:
        raise AssertionError(
            f"fully specified schema negative control failed: {control_missing}"
        )
    if benchmark["parameter_count"] >= 10_000:
        raise AssertionError("benchmark network is not a deliberately tiny lower bound")
    return {
        "module": "claim6_fashion_feasibility",
        "claim": "Fashion-MNIST alpha-dependent collapse/stability",
        "scientific_status": "BLOCKED",
        "route_assessment": "PROTOCOL_NOT_IDENTIFIABLE_AND_CPU_WORKLOAD_LOWER_BOUNDED",
        "protocol_schema_audit": {
            "paper_fields_present": sorted(PAPER_PROTOCOL),
            "required_missing_fields": missing,
            "missing_count": len(missing),
            "paper_protocol_reproducible": False,
            "negative_control": {
                "name": "fill every required field with explicit example values",
                "expected": "schema complete",
                "observed": "schema complete" if not control_missing else "still missing",
                "remaining_missing": control_missing,
                "passes": not control_missing,
            },
        },
        "cpu_microbenchmark": benchmark,
        "paper_workload_lower_bound": {
            "training_examples_without_early_stopping": training_examples,
            "synthetic_images": synthetic_images,
            "sampling_image_steps": sampling_image_steps,
            "training_lower_bound_seconds": training_lower_seconds,
            "sampling_lower_bound_seconds": sampling_lower_seconds,
            "total_lower_bound_seconds": lower_bound_seconds,
            "total_lower_bound_hours": lower_bound_seconds / 3600.0,
            "calculation": (
                "Uses the tiny benchmark's throughput; any residual U-Net matching "
                "the paper description is materially slower."
            ),
        },
        "limitations": [
            "A throughput lower bound is not an image reproduction.",
            "Early stopping could reduce training epochs but cannot remove the 1000-step synthetic-data workload.",
            "Choosing the mock control's architecture or schedule would invent unpublished settings.",
            "No Fashion-MNIST result is accepted from this route.",
        ],
    }

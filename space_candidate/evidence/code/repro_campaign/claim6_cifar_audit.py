"""C6 route 3: executable CIFAR-10 source-contract and evidence audit."""

from __future__ import annotations

from typing import Any


REQUIRED_CIFAR_PROTOCOL_FIELDS = (
    "image_shape",
    "training_samples",
    "base_channels",
    "channel_multipliers",
    "residual_blocks_per_level",
    "attention_resolutions",
    "batch_size",
    "ddpm_beta_schedule",
    "training_diffusion_steps",
    "data_normalization",
    "base_epochs",
    "recursive_epochs",
    "generations",
    "random_seeds",
    "validation_split",
    "early_stopping_metric_and_delta",
    "classifier_architecture_and_checkpoint",
    "feature_dimension",
    "covariance_regularization_epsilon",
    "observability_regressor_architecture",
    "observability_trajectory_count",
)

# Only facts explicitly attached to CIFAR-10, or to the joint image metric, in
# Appendix G.3 of arXiv:2602.16601v2.
PAPER_CIFAR_PROTOCOL: dict[str, Any] = {
    "dataset": "CIFAR-10",
    "alphas": [0.1, 0.5, 0.9],
    "sampler_family": "DDPM",
    "sampler_steps": 1000,
    "feature_metric_samples": 1000,
    "feature_metric_family": "Gaussian chi-squared proxy in classifier features",
    "score_energy_subsampled_timesteps": 50,
    "observability_trajectory_count": 50_000,
}

PUBLISHED_CIFAR_EVIDENCE = {
    "observability_figure": True,
    "observability_generation_zero_is_placeholder": True,
    "reported_post_transient_eta_interval": [0.25, 0.35],
    "alpha_tradeoff_sample_panel": False,
    "per_alpha_drift_curve": False,
    "per_alpha_uncertainty_or_seed_table": False,
    "raw_cifar_metrics": False,
}


def _missing(protocol: dict[str, Any]) -> list[str]:
    return [
        field for field in REQUIRED_CIFAR_PROTOCOL_FIELDS if field not in protocol
    ]


def _complete_mock_protocol() -> dict[str, Any]:
    completed = dict(PAPER_CIFAR_PROTOCOL)
    completed.update(
        {
            "image_shape": [3, 32, 32],
            "training_samples": 50_000,
            "base_channels": 128,
            "channel_multipliers": [1, 2, 2, 2],
            "residual_blocks_per_level": 2,
            "attention_resolutions": [16],
            "batch_size": 128,
            "ddpm_beta_schedule": "linear 1e-4 to 0.02",
            "training_diffusion_steps": 1000,
            "data_normalization": "[-1,1] per channel",
            "base_epochs": 200,
            "recursive_epochs": 100,
            "generations": 10,
            "random_seeds": [11, 29, 47],
            "validation_split": "fixed 5000-image split",
            "early_stopping_metric_and_delta": "validation MSE, min_delta=1e-5",
            "classifier_architecture_and_checkpoint": "frozen ResNet-18 mock hash",
            "feature_dimension": 512,
            "covariance_regularization_epsilon": 1e-5,
            "observability_regressor_architecture": "three-layer MLP mock",
            "observability_trajectory_count": 50_000,
        }
    )
    return completed


def run() -> dict[str, Any]:
    missing = _missing(PAPER_CIFAR_PROTOCOL)
    control_missing = _missing(_complete_mock_protocol())
    cifar_flat_dimension = 3 * 32 * 32
    source_joint_image_dimension = 784
    evidence_needed = (
        "alpha_tradeoff_sample_panel",
        "per_alpha_drift_curve",
        "per_alpha_uncertainty_or_seed_table",
        "raw_cifar_metrics",
    )
    missing_tradeoff_evidence = [
        item for item in evidence_needed if not PUBLISHED_CIFAR_EVIDENCE[item]
    ]

    if not missing:
        raise AssertionError("CIFAR-10 source protocol unexpectedly became complete")
    if control_missing:
        raise AssertionError(
            f"complete-protocol negative control still missing {control_missing}"
        )
    if cifar_flat_dimension == source_joint_image_dimension:
        raise AssertionError("dimension ambiguity control is not discriminating")
    if not PUBLISHED_CIFAR_EVIDENCE["observability_figure"]:
        raise AssertionError("source audit omitted the published CIFAR observability figure")
    if not missing_tradeoff_evidence:
        raise AssertionError("CIFAR alpha-tradeoff evidence audit is vacuous")

    return {
        "module": "claim6_cifar_audit",
        "claim": "CIFAR-10 alpha-dependent collapse/stability",
        "scientific_status": "BLOCKED",
        "route_assessment": "SOURCE_CONTRACT_AND_DIRECT_EVIDENCE_INCOMPLETE",
        "source_anchors": {
            "joint_setup": "Appendix G.3, ar5iv lines 1370-1388",
            "cifar_observability": "Figure 9, ar5iv lines 1381-1383",
            "fashion_only_training_setup": "ar5iv lines 1388-1432",
            "joint_feature_metric": "ar5iv lines 1447-1458",
        },
        "protocol_audit": {
            "paper_fields_present": sorted(PAPER_CIFAR_PROTOCOL),
            "required_missing_fields": missing,
            "missing_count": len(missing),
            "paper_protocol_reproducible": False,
            "negative_control": {
                "name": "explicitly populate every required CIFAR protocol field",
                "expected": "schema complete",
                "observed": "schema complete" if not control_missing else "incomplete",
                "remaining_missing": control_missing,
                "passes": not control_missing,
            },
        },
        "dimension_audit": {
            "source_joint_image_dimension": source_joint_image_dimension,
            "fashion_flat_dimension": 28 * 28,
            "cifar10_flat_dimension": cifar_flat_dimension,
            "assessment": (
                "The subsection-wide d=784 statement is correct for Fashion-MNIST "
                "but not CIFAR-10. Because scope is ambiguous, this is an "
                "identifiability defect, not a counterexample."
            ),
        },
        "published_cifar_evidence_audit": {
            **PUBLISHED_CIFAR_EVIDENCE,
            "missing_direct_alpha_tradeoff_evidence": missing_tradeoff_evidence,
            "assessment": (
                "Figure 9 supports nonzero observability only. It does not display "
                "low-alpha collapse versus high-alpha stability on CIFAR-10."
            ),
        },
        "limitations": [
            "Missing protocol fields cannot falsify an empirical claim.",
            "The source's CIFAR-10 observability result is preserved as positive evidence.",
            "No CIFAR-10 model is trained and no image result is accepted.",
            "The d=784 scope ambiguity is not treated as proof that an experiment was wrong.",
        ],
    }

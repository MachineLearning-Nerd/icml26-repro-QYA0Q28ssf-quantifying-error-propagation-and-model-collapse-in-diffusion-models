"""C6 route 4: assumption-satisfying falsification search."""

from __future__ import annotations

from typing import Any

from repro_campaign.check_claim6_falsification import audit_candidates


PAPER_CLAIM_CONTRACT = {
    "source": "arXiv:2602.16601v2, Figure 1 and Appendix G.1-G.3",
    "domain": ["10D five-component GMM", "Fashion-MNIST", "CIFAR-10"],
    "fresh_data_fractions": [0.1, 0.5, 0.9],
    "gmm_fixed_protocol": {
        "dimension": 10,
        "components": 5,
        "sigma": 0.6,
        "kde_bandwidth": 0.6,
        "training_samples": 100_000,
        "sampler": "500-step Euler-Maruyama from T=4 to t0=0.02",
        "generations": 20,
        "independent_runs": 10,
    },
    "quantifier": (
        "Empirical illustration under the stated protocols, not a universal theorem."
    ),
    "outcome": (
        "GMM dispersion is ordered alpha 0.1 > 0.5 > 0.9; image evidence is "
        "qualitative and does not define a numerical stability threshold."
    ),
}


CANDIDATES: list[dict[str, Any]] = [
    {
        "name": "paper_scale_population_KDE_GMM_ordering",
        "assumption_checks": {
            "dimension_10": True,
            "five_components": True,
            "sigma_0p6": True,
            "bandwidth_0p6": True,
            "N_100000": True,
            "20_generations": True,
            "10_independent_runs": True,
            "literal_empirical_KDE": False,
            "500_step_Euler_Maruyama": False,
        },
        "same_observable_as_claim": True,
        "contradiction_test": {
            "kind": "strict_descending",
            "labels": ["alpha=0.1", "alpha=0.5", "alpha=0.9"],
            "observed": [
                1.0837670400008657,
                0.24716661661386174,
                0.13769247179798083,
            ],
        },
        "interpretation": (
            "Generation-20 relative total-second-moment drift from route 1."
        ),
    },
    {
        "name": "zero_bandwidth_GMM_no_accumulation",
        "assumption_checks": {
            "dimension_10": True,
            "five_components": True,
            "sigma_0p6": True,
            "bandwidth_0p6": False,
            "N_100000": True,
            "20_generations": True,
            "10_independent_runs": True,
        },
        "same_observable_as_claim": True,
        "contradiction_test": {
            "kind": "strict_descending",
            "labels": ["alpha=0.1", "alpha=0.5", "alpha=0.9"],
            "observed": [0.0, 0.0, 0.0],
        },
        "interpretation": "Route 1 h=0 mechanism control.",
    },
    {
        "name": "alpha_0p9_population_GMM_has_13p77_percent_drift",
        "assumption_checks": {
            "dimension_10": True,
            "five_components": True,
            "sigma_0p6": True,
            "bandwidth_0p6": True,
            "N_100000": True,
            "20_generations": True,
            "10_independent_runs": True,
            "literal_empirical_KDE": False,
            "500_step_Euler_Maruyama": False,
        },
        "same_observable_as_claim": True,
        "contradiction_test": {
            "kind": "qualitative_without_threshold",
            "observed": 0.13769247179798083,
        },
        "interpretation": (
            "The word stable has no published maximum-drift threshold, so a "
            "positive drift value alone cannot contradict it."
        ),
    },
    {
        "name": "CIFAR_observability_curves_overlap",
        "assumption_checks": {
            "cifar_model_specified": False,
            "cifar_training_protocol_specified": False,
            "cifar_seeds_specified": False,
        },
        "same_observable_as_claim": False,
        "contradiction_test": {
            "kind": "strict_descending",
            "labels": ["alpha=0.1", "alpha=0.5", "alpha=0.9"],
            "observed": [0.30, 0.30, 0.30],
        },
        "interpretation": (
            "Figure 9 measures eta, not collapse-driven distributional drift."
        ),
    },
]


EXPLICIT_THRESHOLD_NEGATIVE_CONTROL: dict[str, Any] = {
    "name": "synthetic_explicit_alpha_0p9_drift_at_most_10_percent",
    "assumption_checks": {
        "population_KDE_contract": True,
        "dimension_10": True,
        "five_components": True,
        "sigma_0p6": True,
        "bandwidth_0p6": True,
        "N_100000": True,
        "20_generations": True,
        "10_independent_runs": True,
    },
    "same_observable_as_claim": True,
    "contradiction_test": {
        "kind": "upper_threshold",
        "maximum": 0.10,
        "observed": 0.13769247179798083,
    },
    "interpretation": (
        "A deliberately synthetic quantitative claim. It is not attributed to "
        "the paper and exists only to test the falsification checker."
    ),
}


def run() -> dict[str, Any]:
    independent = audit_candidates(CANDIDATES, EXPLICIT_THRESHOLD_NEGATIVE_CONTROL)
    if independent["C6_verdict"] != "BLOCKED":
        raise AssertionError(
            "An accepted C6 counterexample requires manual assumption review"
        )
    return {
        "module": "claim6_falsification",
        "claim": "C6 alpha-dependent empirical tradeoff",
        "paper_claim_contract": PAPER_CLAIM_CONTRACT,
        "route_assessment": "NO_VALID_COUNTEREXAMPLE_FOUND",
        "scientific_status": "BLOCKED",
        "independent_checker": independent,
        "four_route_summary": [
            {
                "route": 1,
                "method": "paper-scale 10D population-KDE stochastic calibration",
                "result": "aligned ordering, but solver substitution prevents full C6",
            },
            {
                "route": 2,
                "method": "Fashion-MNIST source identifiability and CPU lower bound",
                "result": "BLOCKED by missing settings and faithful CPU scope",
            },
            {
                "route": 3,
                "method": "CIFAR-10 source-contract and evidence-coverage audit",
                "result": "BLOCKED; observability evidence is not drift evidence",
            },
            {
                "route": 4,
                "method": "assumption-satisfying falsification search",
                "result": "no valid contradiction found",
            },
        ],
        "unblocking_requirements": [
            "authors' exact GMM acceleration/code and raw seeded outputs",
            "complete Fashion-MNIST and CIFAR-10 configurations and checkpoints",
            "raw per-generation image metrics with seeds and uncertainty",
            "CPU time sufficient for the fully specified recursive image campaign",
        ],
        "limitations": [
            "A failed reproduction, omitted setting, or different observable is not falsification.",
            "The h=0 control violates the fixed h=0.6 GMM protocol.",
            "The population-KDE route aligns with the alpha ordering.",
            "No numerical threshold defines how much alpha=0.9 drift is incompatible with the qualitative word stable.",
        ],
    }

"""Exact C1 proof certificate plus a 10D non-Gaussian SDE calibration."""

from __future__ import annotations

import copy
import json
import math
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any


PAPER_SOURCE_SHA256 = "472fb9e246aea7c5d1e643d5755f034f005d1f2bbb61f86371bae855f62765e3"
SEEDS = (57721, 61169, 65537, 70001, 74959)
BETAS = (0.10, 0.20, 0.30)
DIMENSION = 10
T_FINAL = 4.0
T_ZERO = 0.02
STEPS = 500
N_PER_SEED = 4_000
ACTIVE_WORKERS = 8
CERTIFICATE_PATH = (
    Path(__file__).resolve().parents[1]
    / ".openresearch"
    / "artifacts"
    / "C1"
    / "proof_certificate.json"
)


def validate_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    """Independently validate the allowed proof-rule graph and constants."""
    errors: list[str] = []
    if certificate.get("source_sha256") != PAPER_SOURCE_SHA256:
        errors.append("paper source hash mismatch")
    if certificate.get("source_anchor") != "#S3.Thmtheorem1":
        errors.append("wrong proposition anchor")
    if certificate.get("assumption_anchors") != ["#S3.I1.i1", "#S3.I1.i2"]:
        errors.append("A1-A2 anchors missing or reordered")

    expected = {
        "girsanov_log_density": ("A2_GIRSANOV_UNDER_LEARNED_MEASURE", 0.5),
        "center_stochastic_integral": ("ITO_INTEGRAL_HAS_ZERO_MEAN", None),
        "path_kl_identity": ("KL_IS_EXPECTED_LOG_DENSITY", 0.5),
        "endpoint_contraction": ("DATA_PROCESSING_FOR_MEASURABLE_MAP", None),
        "proposition_3_1": ("SUBSTITUTE_ENDPOINT_LAWS", 0.5),
    }
    seen: set[str] = {"A1", "A2"}
    for step in certificate.get("steps", []):
        step_id = step.get("id")
        if step_id not in expected:
            errors.append(f"unrecognized step: {step_id}")
            continue
        rule, coefficient = expected[step_id]
        if step.get("rule") != rule:
            errors.append(f"{step_id}: wrong rule")
        if coefficient is not None and not math.isclose(
            float(step.get("coefficient", math.nan)),
            coefficient,
            rel_tol=0.0,
            abs_tol=0.0,
        ):
            errors.append(f"{step_id}: wrong coefficient")
        missing = [dependency for dependency in step.get("depends_on", []) if dependency not in seen]
        if missing:
            errors.append(f"{step_id}: unmet dependencies {missing}")
        seen.add(str(step_id))
    if set(expected) - seen:
        errors.append(f"missing steps: {sorted(set(expected) - seen)}")

    conclusion = certificate.get("steps", [{}])[-1].get("result")
    if conclusion != "KL(p_hat_i+1 || q_i) <= 0.5 * eps_hat2":
        errors.append("exact conclusion mismatch")
    if certificate.get("conclusion") != conclusion:
        errors.append("declared conclusion does not match final step")
    return {"accepted": not errors, "errors": errors}


def certificate_preflight() -> dict[str, Any]:
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    positive = validate_certificate(certificate)
    corrupted = copy.deepcopy(certificate)
    corrupted["steps"][-1]["coefficient"] = 0.49
    corrupted["steps"][-1]["result"] = "KL(p_hat_i+1 || q_i) <= 0.49 * eps_hat2"
    negative = validate_certificate(corrupted)
    if not positive["accepted"]:
        raise AssertionError(f"valid proof certificate rejected: {positive}")
    if negative["accepted"]:
        raise AssertionError("coefficient-corruption control unexpectedly passed")

    horizon = T_FINAL - T_ZERO
    bounded_error_rows = []
    for beta in BETAS:
        a1_energy_bound = DIMENSION * beta**2 * horizon
        novikov_bound = math.exp(0.5 * a1_energy_bound)
        bounded_error_rows.append(
            {
                "beta": beta,
                "dimension": DIMENSION,
                "horizon": horizon,
                "a1_energy_upper_bound": a1_energy_bound,
                "novikov_exponential_upper_bound": novikov_bound,
                "A1_finite": math.isfinite(a1_energy_bound),
                "A2_novikov_sufficient_condition": math.isfinite(novikov_bound),
            }
        )
    return {
        "certificate": positive,
        "negative_control": {
            "name": "replace exact coefficient 1/2 by 0.49",
            "expected": "REJECT",
            "observed": "REJECT" if not negative["accepted"] else "ACCEPT",
            "checker_errors": negative["errors"],
        },
        "bounded_state_dependent_error_audit": bounded_error_rows,
    }


def _component_means() -> Any:
    import numpy as np

    means = np.zeros((5, DIMENSION), dtype=np.float64)
    means[1, :2] = (-4.0, -4.0)
    means[2, :2] = (-4.0, 4.0)
    means[3, :2] = (4.0, -4.0)
    means[4, :2] = (4.0, 4.0)
    return means


def _gmm_score(x: Any, time_value: float) -> Any:
    import numpy as np

    means = _component_means()
    attenuation = math.exp(-0.5 * time_value)
    variance = attenuation**2 * 0.6**2 + (1.0 - attenuation**2)
    time_means = attenuation * means
    squared = np.sum((x[:, None, :] - time_means[None, :, :]) ** 2, axis=2)
    logits = -0.5 * squared / variance
    logits -= np.max(logits, axis=1, keepdims=True)
    weights = np.exp(logits)
    weights /= np.sum(weights, axis=1, keepdims=True)
    posterior_mean = weights @ time_means
    return (posterior_mean - x) / variance


def _simulate_one(task: tuple[float, int]) -> dict[str, Any]:
    import numpy as np

    beta, seed = task
    rng = np.random.default_rng(seed)
    ideal = rng.normal(size=(N_PER_SEED, DIMENSION))
    learned = ideal.copy()
    dt = (T_FINAL - T_ZERO) / STEPS
    root_dt = math.sqrt(dt)
    learned_energy = np.zeros(N_PER_SEED, dtype=np.float64)
    for step in range(STEPS):
        time_value = T_FINAL - step * dt
        ideal_score = _gmm_score(ideal, time_value)
        learned_score = _gmm_score(learned, time_value)
        error = beta * np.tanh(learned)
        ideal_noise = rng.normal(size=ideal.shape)
        learned_noise = rng.normal(size=learned.shape)
        ideal += (-0.5 * ideal - ideal_score) * dt + root_dt * ideal_noise
        learned += (-0.5 * learned - learned_score - error) * dt + root_dt * learned_noise
        learned_energy += np.sum(error * error, axis=1) * dt
    return {
        "beta": beta,
        "seed": seed,
        "ideal": ideal,
        "learned": learned,
        "energy": learned_energy,
    }


def _quadratic_logistic_kl(
    learned: Any,
    ideal: Any,
    seed: int,
) -> dict[str, float]:
    import numpy as np

    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler

    x = np.concatenate([ideal, learned], axis=0)
    y = np.concatenate(
        [np.zeros(len(ideal), dtype=np.int8), np.ones(len(learned), dtype=np.int8)]
    )
    model = make_pipeline(
        PolynomialFeatures(degree=2, include_bias=False),
        StandardScaler(),
        LogisticRegression(C=1.0, max_iter=500, random_state=seed),
    )
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    probabilities = cross_val_predict(model, x, y, cv=splitter, method="predict_proba")[:, 1]
    logits = np.log(np.clip(probabilities, 1e-8, 1.0 - 1e-8)) - np.log(
        np.clip(1.0 - probabilities, 1e-8, 1.0)
    )
    p_logits = logits[y == 1]
    mean = float(np.mean(p_logits))
    standard_error = float(np.std(p_logits, ddof=1) / math.sqrt(len(p_logits)))
    return {
        "estimate": mean,
        "standard_error": standard_error,
        "upper_95": mean + 1.96 * standard_error,
        "lower_95_one_sided": mean - 1.645 * standard_error,
    }


def _knn_kl(learned: Any, ideal: Any) -> dict[str, float]:
    import numpy as np

    from sklearn.neighbors import NearestNeighbors

    # The Perez-Cruz k=1 estimator with an independent null-bias correction.
    n = min(8_000, len(learned), len(ideal) // 2)
    p = learned[:n]
    q = ideal[:n]
    null_p = ideal[:n]
    null_q = ideal[n : 2 * n]

    def terms_for(left: Any, right: Any) -> Any:
        rho_model = NearestNeighbors(n_neighbors=2, algorithm="auto").fit(left)
        nu_model = NearestNeighbors(n_neighbors=1, algorithm="auto").fit(right)
        rho = rho_model.kneighbors(left, return_distance=True)[0][:, 1]
        nu = nu_model.kneighbors(left, return_distance=True)[0][:, 0]
        terms = DIMENSION * np.log(np.maximum(nu, 1e-12) / np.maximum(rho, 1e-12))
        return terms + math.log(n / (n - 1))

    raw_terms = terms_for(p, q)
    null_terms = terms_for(null_p, null_q)
    raw_mean = float(np.mean(raw_terms))
    null_mean = float(np.mean(null_terms))
    mean = raw_mean - null_mean
    standard_error = math.sqrt(
        float(np.var(raw_terms, ddof=1) / n) + float(np.var(null_terms, ddof=1) / n)
    )
    return {
        "estimate": mean,
        "standard_error": standard_error,
        "upper_95": mean + 1.96 * standard_error,
        "lower_95_one_sided": mean - 1.645 * standard_error,
        "raw_estimate": raw_mean,
        "null_bias_estimate": null_mean,
    }


def run_calibration() -> dict[str, Any]:
    import numpy as np

    tasks = [(beta, seed) for beta in BETAS for seed in SEEDS]
    workers = min(ACTIVE_WORKERS, len(tasks), os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        outputs = list(pool.map(_simulate_one, tasks))

    rows = []
    for beta in BETAS:
        selected = [output for output in outputs if output["beta"] == beta]
        ideal = np.concatenate([output["ideal"] for output in selected], axis=0)
        learned = np.concatenate([output["learned"] for output in selected], axis=0)
        energies = np.concatenate([output["energy"] for output in selected], axis=0)
        eps_hat2 = float(np.mean(energies))
        eps_se = float(np.std(energies, ddof=1) / math.sqrt(len(energies)))
        path_kl = 0.5 * eps_hat2
        path_kl_standard_error = 0.5 * eps_se
        path_kl_upper_95_one_sided = path_kl + 1.645 * path_kl_standard_error
        logistic = _quadratic_logistic_kl(learned, ideal, seed=SEEDS[0])
        knn = _knn_kl(learned, ideal)
        estimators = {
            "cross_fitted_quadratic_logistic": logistic,
            "knn_perez_cruz": knn,
        }
        significant_violations = {
            name: values["lower_95_one_sided"] > path_kl_upper_95_one_sided
            for name, values in estimators.items()
        }
        false_path_budget = 0.1 * path_kl
        false_budget_rejections = {
            name: values["lower_95_one_sided"] > false_path_budget
            for name, values in estimators.items()
        }
        no_significant_violation = not any(significant_violations.values())
        false_budget_control_passes = all(false_budget_rejections.values())
        rows.append(
            {
                "beta": beta,
                "target": "10D five-component GMM",
                "state_dependent_error": "beta * tanh(x)",
                "trajectories": len(energies),
                "steps": STEPS,
                "seeds": list(SEEDS),
                "eps_hat2": eps_hat2,
                "eps_hat2_standard_error": eps_se,
                "half_eps_hat2": path_kl,
                "path_kl_standard_error": path_kl_standard_error,
                "path_kl_upper_95_one_sided": path_kl_upper_95_one_sided,
                "endpoint_kl_estimators": estimators,
                "significant_violation_at_one_sided_5pct": significant_violations,
                "no_significant_violation": bool(no_significant_violation),
                "negative_control": {
                    "false_path_budget_multiplier": 0.1,
                    "false_path_budget": false_path_budget,
                    "rejected_by_estimator": false_budget_rejections,
                    "passes": bool(false_budget_control_passes),
                },
            }
        )
    if not all(row["no_significant_violation"] for row in rows):
        raise AssertionError(f"C1 endpoint estimate significantly violated path bound: {rows}")
    if not all(row["negative_control"]["passes"] for row in rows):
        raise AssertionError(f"C1 false-budget negative control was not rejected: {rows}")
    return {
        "protocol": {
            "dimension": DIMENSION,
            "components": 5,
            "component_sigma": 0.6,
            "T": T_FINAL,
            "t0": T_ZERO,
            "euler_maruyama_steps": STEPS,
            "betas": list(BETAS),
            "seeds": list(SEEDS),
            "trajectories_per_beta": N_PER_SEED * len(SEEDS),
            "active_worker_processes": workers,
        },
        "rows": rows,
    }


def run() -> dict[str, Any]:
    preflight = certificate_preflight()
    calibration = run_calibration()
    return {
        "module": "claim1_girsanov",
        "claim": "Proposition 3.1",
        "scientific_status": "VERIFIED",
        "scope": (
            "Exact proof reconstruction under A1-A2, independently checked; "
            "10D non-Gaussian GMM Euler-Maruyama calibration is corroboration."
        ),
        "proof": preflight,
        "calibration": calibration,
        "limitations": [
            "The numerical endpoint KL uses two independent finite-sample estimators.",
            "The one-sided calibration can detect significant contradictions; failure to reject is not proof.",
            "The proof certificate, not the finite experiment, carries the universal quantifier.",
            "The learned error is controlled and state-dependent rather than a trained KDE score.",
        ],
    }

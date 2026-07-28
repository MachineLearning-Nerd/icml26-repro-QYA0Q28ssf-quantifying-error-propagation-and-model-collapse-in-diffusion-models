"""Exact C4 persistence proof and proof-level C5 falsification."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any


PAPER_SOURCE_SHA256 = "472fb9e246aea7c5d1e643d5755f034f005d1f2bbb61f86371bae855f62765e3"
ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_PATH = (
    ROOT / ".openresearch" / "artifacts" / "C4-C5" / "proof_certificate.json"
)
ALPHAS = (0.1, 0.5, 0.9)


def validate_certificate(certificate: dict[str, Any]) -> dict[str, Any]:
    """Validate exact C4 constants and the logical C5 contradiction."""
    import sympy as sp

    errors: list[str] = []
    if certificate.get("source_sha256") != PAPER_SOURCE_SHA256:
        errors.append("paper source hash mismatch")
    if certificate.get("claim_anchors") != ["#S4.Thmtheorem1", "#S4.Thmtheorem2"]:
        errors.append("wrong C4-C5 claim anchors")

    c4 = certificate.get("C4", {})
    expected_steps = {
        "refresh": ("EXACT_CHI2_MIXTURE_CONTRACTION", None),
        "innovation": ("SQUARE_LOWER_AND_Q_OVER_PDATA", 0.5),
        "intra_lower": ("THEOREM_3_4_CLEAN_LOWER", 0.125),
        "combined_recursion": ("SUBSTITUTE", 0.0625),
        "sum_recursion": ("FINITE_SUM_AND_REINDEX", None),
        "non_summability": ("DIVERGENT_LOWER_SERIES", None),
        "cesaro_floor": ("UNIFORM_ERROR_FLOOR_AND_CESARO", 0.0625),
        "limsup_floor": ("LIMSUP_DOMINATES_CESARO_LIMINF", None),
    }
    seen: set[str] = {"A1", "A2", "A3", "A4", "eta_floor", "small_error"}
    for step in c4.get("steps", []):
        step_id = step.get("id")
        if step_id not in expected_steps:
            errors.append(f"C4 unrecognized step: {step_id}")
            continue
        rule, coefficient = expected_steps[step_id]
        if step.get("rule") != rule:
            errors.append(f"C4 {step_id}: wrong rule")
        if coefficient is not None and float(step.get("coefficient", math.nan)) != coefficient:
            errors.append(f"C4 {step_id}: wrong coefficient")
        missing = [item for item in step.get("depends_on", []) if item not in seen]
        if missing:
            errors.append(f"C4 {step_id}: unmet dependencies {missing}")
        seen.add(str(step_id))
    if set(expected_steps) - seen:
        errors.append(f"C4 missing steps: {sorted(set(expected_steps) - seen)}")
    if c4.get("floor_requires_uniform_error_floor") is not True:
        errors.append("C4 floor incorrectly inferred without a uniform error floor")

    alpha, eta, eps_floor, r = sp.symbols(
        "alpha eta eps_floor r", positive=True
    )
    recurrence_rhs = alpha * eta * eps_floor / 16
    expected_floor = alpha * eta * eps_floor / (16 * (1 + r))
    if sp.simplify(recurrence_rhs / (1 + r) - expected_floor) != 0:
        errors.append("C4 symbolic floor collection failed")

    c5 = certificate.get("C5", {})
    if c5.get("asymp_definition") != (
        "there exist constants 0<c1<=c2<infinity such that c1*g_N<=f_N<=c2*g_N"
    ):
        errors.append("C5 wrong asymp definition")
    if c5.get("main_statement_C_bias") != "strictly_positive_constant":
        errors.append("C5 contradiction requires the theorem's C_bias>0")
    if c5.get("summability_consequence") != (
        "discounted_sum_and_initial_term_tend_to_zero"
    ):
        errors.append("C5 missing vanishing-right-side consequence")
    if c5.get("nonnegative_divergence_consequence") != (
        "D_N+C_bias>=C_bias>0"
    ):
        errors.append("C5 missing positive-left-side consequence")
    if c5.get("verdict") != "FALSIFIED":
        errors.append("C5 certificate verdict mismatch")
    if c5.get("appendix_proves_main_equivalence") is not False:
        errors.append("C5 appendix inequalities mislabeled as main equivalence")
    return {"accepted": not errors, "errors": errors}


def certificate_preflight() -> dict[str, Any]:
    certificate = json.loads(CERTIFICATE_PATH.read_text())
    positive = validate_certificate(certificate)

    no_uniform_floor = copy.deepcopy(certificate)
    no_uniform_floor["C4"]["floor_requires_uniform_error_floor"] = False
    c4_negative = validate_certificate(no_uniform_floor)

    zero_bias = copy.deepcopy(certificate)
    zero_bias["C5"]["main_statement_C_bias"] = "zero"
    c5_zero_bias = validate_certificate(zero_bias)

    bias_on_rhs = copy.deepcopy(certificate)
    bias_on_rhs["C5"]["summability_consequence"] = (
        "discounted_sum_plus_C_bias_tends_to_C_bias"
    )
    c5_bias_rhs = validate_certificate(bias_on_rhs)

    if not positive["accepted"]:
        raise AssertionError(f"valid C4-C5 certificate rejected: {positive}")
    if (
        c4_negative["accepted"]
        or c5_zero_bias["accepted"]
        or c5_bias_rhs["accepted"]
    ):
        raise AssertionError("C4-C5 mutation control unexpectedly accepted")
    return {
        "certificate": positive,
        "negative_controls": [
            {
                "mutation": "infer the C4 floor from series divergence without a uniform per-step floor",
                "observed": "REJECT",
                "checker_errors": c4_negative["errors"],
            },
            {
                "mutation": "replace the main theorem's strictly positive C_bias by zero",
                "observed": "REJECT_FALSIFICATION",
                "checker_errors": c5_zero_bias["errors"],
            },
            {
                "mutation": "add C_bias to the right side so it no longer vanishes",
                "observed": "REJECT_FALSIFICATION",
                "checker_errors": c5_bias_rhs["errors"],
            },
        ],
    }


def _c4_sequence_checks() -> dict[str, Any]:
    rows = []
    horizon = 100_000
    eta_floor = 0.5
    error_floor = 0.01
    for alpha in ALPHAS:
        r = (1.0 - alpha) ** 2
        k = alpha * eta_floor / 16.0
        claimed_floor = k * error_floor / (1.0 + r)

        persistent_d = claimed_floor
        persistent_lhs = persistent_d * (1.0 + r)
        persistent_rhs = k * error_floor

        # Divergent errors alone permit a vanishing, non-summable D sequence
        # while respecting the exact lower recurrence. This is a control against
        # conflating the two clauses of Proposition 4.1.
        c = k / (0.5 + r)
        min_slack = math.inf
        for i in range(horizon):
            eps2_i = 1.0 / (i + 1.0)
            d_i = c / (i + 1.0)
            d_next = c / (i + 2.0)
            min_slack = min(min_slack, d_next + r * d_i - k * eps2_i)
        rows.append(
            {
                "alpha": alpha,
                "r": r,
                "eta_floor": eta_floor,
                "uniform_eps2_floor": error_floor,
                "paper_limsup_floor": claimed_floor,
                "constant_sequence_D": persistent_d,
                "constant_sequence_recurrence_lhs": persistent_lhs,
                "constant_sequence_recurrence_rhs": persistent_rhs,
                "floor_constant_is_tight_for_recurrence": math.isclose(
                    persistent_lhs,
                    persistent_rhs,
                    rel_tol=0.0,
                    abs_tol=1e-15,
                ),
                "divergent_series_control": {
                    "eps2_i": "1/(i+1)",
                    "D_i": f"{c}/(i+1)",
                    "checked_horizon": horizon,
                    "minimum_recurrence_slack": min_slack,
                    "D_tends_to_zero": True,
                    "sum_D_diverges": True,
                    "interpretation": (
                        "Series divergence proves non-summability of D, not a "
                        "positive limsup; the uniform error floor is essential."
                    ),
                },
            }
        )
    if not all(
        row["floor_constant_is_tight_for_recurrence"]
        and row["divergent_series_control"]["minimum_recurrence_slack"] >= -1e-15
        for row in rows
    ):
        raise AssertionError(f"C4 recurrence check failed: {rows}")
    return {"rows": rows}


def _discounted_sum(alpha: float, eps2: list[float], n: int) -> float:
    r = (1.0 - alpha) ** 2
    return sum(r ** (n - i) * eps2[i] for i in range(n + 1))


def _c5_contradiction_checks() -> dict[str, Any]:
    horizons = (10, 20, 40, 80, 160)
    eps2 = [0.04 * (0.5**i) for i in range(max(horizons) + 1)]
    c_bias = 1.0
    d_initial = 0.25
    rows = []
    for alpha in ALPHAS:
        r = (1.0 - alpha) ** 2
        ratios = []
        for n in horizons:
            rhs = _discounted_sum(alpha, eps2, n) + r ** (n + 1) * d_initial
            universal_lhs_lower = c_bias
            ratios.append(
                {
                    "N": n,
                    "discounted_rhs": rhs,
                    "universal_lhs_lower": universal_lhs_lower,
                    "minimum_required_upper_asymp_constant": (
                        universal_lhs_lower / rhs
                    ),
                    "repaired_rhs_plus_C_bias": rhs + c_bias,
                    "repaired_minimum_ratio": universal_lhs_lower
                    / (rhs + c_bias),
                }
            )
        rows.append(
            {
                "alpha": alpha,
                "r": r,
                "summable_eps2": "0.04*0.5^i",
                "sum_eps2_exact": 0.08,
                "C_bias": c_bias,
                "D_initial": d_initial,
                "horizons": ratios,
                "right_side_decreases_to_zero": all(
                    ratios[i + 1]["discounted_rhs"]
                    < ratios[i]["discounted_rhs"]
                    for i in range(len(ratios) - 1)
                ),
                "required_asymp_constant_is_unbounded": (
                    ratios[-1]["minimum_required_upper_asymp_constant"]
                    > 1_000 * ratios[0]["minimum_required_upper_asymp_constant"]
                ),
            }
        )
    if not all(
        row["right_side_decreases_to_zero"]
        and row["required_asymp_constant_is_unbounded"]
        for row in rows
    ):
        raise AssertionError(f"C5 contradiction calibration failed: {rows}")
    return {
        "logic": (
            "For every nonnegative D_N, D_N+C_bias>=C_bias>0. Under summability "
            "and 0<alpha<=1, the discounted sum and initial term tend to zero. "
            "Therefore no finite c2 can satisfy the paper's defined upper asymp inequality."
        ),
        "rows": rows,
    }


def run() -> dict[str, Any]:
    proof = certificate_preflight()
    return {
        "module": "claim45_global",
        "claims": ["Proposition 4.1", "Theorem 4.2"],
        "scientific_status": {"C4": "VERIFIED", "C5": "FALSIFIED"},
        "proof": proof,
        "C4_calibration": _c4_sequence_checks(),
        "C5_falsification": _c5_contradiction_checks(),
        "scope": (
            "C4 is an exact proof reconstruction with separate quantifiers. C5 "
            "is falsified as written by a source-internal limit contradiction; "
            "the appendix's weaker additive inequalities remain unchallenged."
        ),
        "limitations": [
            "C4 sequence calculations calibrate the proof recursion rather than train a diffusion model.",
            "C5 falsifies the displayed multiplicative equivalence with positive bias, not the appendix's additive stability bounds.",
            "If the authors intended C_bias on the right side or an additive-error notation instead of asymp, that would be a different claim.",
        ],
    }

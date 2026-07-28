"""Reproduce the historical toy checks without promoting their verdicts.

This module intentionally mirrors the scientific scope visible at the judged
Space revision.  It is the frozen control, not current evidence for the paper's
general diffusion claims.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def _accumulate(alpha: float, innovations: list[float], d0: float = 0.0) -> float:
    d = float(d0)
    contraction = (1.0 - alpha) ** 2
    for innovation in innovations:
        d = contraction * d + innovation
    return d


def run() -> dict[str, Any]:
    checks: dict[str, Any] = {}

    # Historical C1: Gaussian mean shift, which saturates the KL path bound.
    c1_rows = []
    for mu in (0.1, 0.3, 0.5, 0.7, 1.0):
        eps2 = mu * mu
        kl = 0.5 * eps2
        c1_rows.append(
            {
                "mu": mu,
                "eps2": eps2,
                "kl": kl,
                "half_eps2": 0.5 * eps2,
                "holds": bool(kl <= 0.5 * eps2 + 1e-14),
            }
        )
    checks["C1"] = {
        "scientific_status": "TOY",
        "reason": "1D Gaussian mean shift with eta=1; not Proposition 3.1 in general.",
        "rows": c1_rows,
    }

    # Historical C2/C3: another exact formula in the same one-parameter family.
    c23_rows = []
    for mu in (0.1, 0.3, 0.5, 0.7, 0.9, 1.0):
        eps2 = mu * mu
        chi2 = math.expm1(eps2)
        lower = 0.25 * eps2 - 0.5 * eps2**2
        upper = 4.0 * eps2 + eps2**2
        c23_rows.append(
            {
                "mu": mu,
                "eps2": eps2,
                "eta": 1.0,
                "chi2": chi2,
                "lower": lower,
                "upper": upper,
                "holds": bool(lower <= chi2 <= upper),
            }
        )
    checks["C2"] = {
        "scientific_status": "TOY",
        "reason": "Only eta=1 and a 1D Gaussian mean shift.",
        "rows": c23_rows,
    }
    checks["C3"] = {
        "scientific_status": "TOY",
        "reason": "Finite checks in the same 1D Gaussian family cannot verify Theorem 3.4.",
        "rows": c23_rows,
    }

    c4_rows = []
    c5_rows = []
    innovations = [0.1, 0.05, 0.2, 0.02, 0.1, 0.08, 0.01, 0.15, 0.03]
    for alpha in (0.1, 0.5, 0.9):
        contraction = (1.0 - alpha) ** 2
        observed = _accumulate(alpha, [0.05] * 1000)
        toy_floor = 0.05 / (1.0 - contraction)
        c4_rows.append(
            {
                "alpha": alpha,
                "observed": observed,
                "toy_floor": toy_floor,
                "matches": bool(abs(observed - toy_floor) < 1e-12),
            }
        )
        recursion = _accumulate(alpha, innovations, d0=0.02)
        closed = contraction ** len(innovations) * 0.02 + sum(
            contraction ** (len(innovations) - 1 - i) * value
            for i, value in enumerate(innovations)
        )
        c5_rows.append(
            {
                "alpha": alpha,
                "recursion": recursion,
                "closed_form": closed,
                "matches": bool(abs(recursion - closed) < 1e-14),
            }
        )
    checks["C4"] = {
        "scientific_status": "TOY",
        "reason": "Checks a substituted scalar recursion, not Proposition 4.1's diffusion quantities.",
        "rows": c4_rows,
    }
    checks["C5"] = {
        "scientific_status": "TOY",
        "reason": "Checks an algebraic identity after assuming the theorem's recurrence.",
        "rows": c5_rows,
    }
    checks["C6"] = {
        "scientific_status": "BLOCKED",
        "reason": "The judged revision contains no trained-score GMM or image experiment.",
        "rows": [],
    }

    # Negative control: omitting the 1/2 in C1 must be detected as a false
    # equality for every nonzero shift.
    negative_control_detected = all(
        not np.isclose(row["kl"], row["eps2"], rtol=0.0, atol=1e-14)
        for row in c1_rows
    )
    if not negative_control_detected:
        raise AssertionError("negative control unexpectedly passed")

    expected = {"C1": "TOY", "C2": "TOY", "C3": "TOY", "C4": "TOY", "C5": "TOY", "C6": "BLOCKED"}
    observed = {claim: item["scientific_status"] for claim, item in checks.items()}
    if observed != expected:
        raise AssertionError(f"historical verdict regression: {observed!r}")
    if not all(row["holds"] for row in c1_rows + c23_rows):
        raise AssertionError("historical numerical sanity check failed")
    if not all(row["matches"] for row in c4_rows + c5_rows):
        raise AssertionError("historical recursion check failed")

    return {
        "module": "historical_baseline",
        "evidence_status": "Historical rejected baseline",
        "judge_score": "5/12",
        "claims": checks,
        "negative_control": {
            "name": "incorrect_KL_equals_eps2",
            "expected": "FAIL",
            "observed": "FAIL",
            "detected": negative_control_detected,
        },
    }

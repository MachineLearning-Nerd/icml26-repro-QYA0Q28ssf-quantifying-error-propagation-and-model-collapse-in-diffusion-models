"""Independent assumption and contradiction checker for C6 falsification."""

from __future__ import annotations

import json
from typing import Any


def evaluate_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    failed_assumptions = sorted(
        name
        for name, satisfied in candidate["assumption_checks"].items()
        if not satisfied
    )
    same_observable = bool(candidate["same_observable_as_claim"])
    test = candidate["contradiction_test"]
    kind = test["kind"]
    contradiction_decidable = True
    contradicts = False

    if kind == "strict_descending":
        values = [float(value) for value in test["observed"]]
        contradicts = not all(
            left > right for left, right in zip(values, values[1:])
        )
    elif kind == "upper_threshold":
        contradicts = float(test["observed"]) > float(test["maximum"])
    elif kind == "qualitative_without_threshold":
        contradiction_decidable = False
    else:
        raise ValueError(f"unknown contradiction test: {kind}")

    accepted = (
        not failed_assumptions
        and same_observable
        and contradiction_decidable
        and contradicts
    )
    reasons = []
    if failed_assumptions:
        reasons.append(f"failed assumptions: {failed_assumptions}")
    if not same_observable:
        reasons.append("candidate measures a different observable")
    if not contradiction_decidable:
        reasons.append("source provides no quantitative stability threshold")
    if contradiction_decidable and not contradicts:
        reasons.append("observation does not contradict the source ordering")
    return {
        "candidate": candidate["name"],
        "accepted_counterexample": accepted,
        "failed_assumptions": failed_assumptions,
        "same_observable_as_claim": same_observable,
        "contradiction_decidable": contradiction_decidable,
        "contradicts": contradicts,
        "rejection_reasons": reasons,
    }


def audit_candidates(
    candidates: list[dict[str, Any]],
    negative_control: dict[str, Any],
) -> dict[str, Any]:
    evaluated = [evaluate_candidate(candidate) for candidate in candidates]
    control = evaluate_candidate(negative_control)
    if any(item["accepted_counterexample"] for item in evaluated):
        verdict = "FALSIFIED"
    else:
        verdict = "BLOCKED"
    if not control["accepted_counterexample"]:
        raise AssertionError(
            f"explicit-threshold falsification control was missed: {control}"
        )
    return {
        "candidate_results": evaluated,
        "negative_control": {
            **control,
            "expected": "ACCEPT_COUNTEREXAMPLE",
            "observed": "ACCEPT_COUNTEREXAMPLE",
        },
        "C6_verdict": verdict,
    }


def main() -> None:
    from repro_campaign.claim6_falsification import (
        CANDIDATES,
        EXPLICIT_THRESHOLD_NEGATIVE_CONTROL,
    )

    print(
        json.dumps(
            audit_candidates(CANDIDATES, EXPLICIT_THRESHOLD_NEGATIVE_CONTROL),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

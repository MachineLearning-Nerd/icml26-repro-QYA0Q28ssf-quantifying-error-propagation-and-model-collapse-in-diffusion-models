"""Fixed cumulative entrypoint inherited by every OpenResearch node."""

from __future__ import annotations

import importlib
import importlib.metadata
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _git_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _allocation() -> dict[str, Any]:
    affinity = None
    if hasattr(os, "sched_getaffinity"):
        affinity = len(os.sched_getaffinity(0))
    return {
        "logical_cpu_count": os.cpu_count(),
        "affinity_cpu_count": affinity,
        "platform": platform.platform(),
        "python": platform.python_version(),
    }


def _versions() -> dict[str, str]:
    names = (
        "marimo",
        "matplotlib",
        "numpy",
        "pandas",
        "pillow",
        "scikit-learn",
        "scipy",
        "sympy",
        "torch",
        "torchvision",
    )
    return {name: importlib.metadata.version(name) for name in names}


def main() -> None:
    started = time.perf_counter()
    config = json.loads((ROOT / "repro_campaign" / "config.json").read_text())
    results = []
    for module_name in config["accepted_claim_modules"]:
        module = importlib.import_module(f"repro_campaign.{module_name}")
        results.append(module.run())
    payload = {
        "schema_version": 1,
        "paper_id": config["paper_id"],
        "campaign_stage": config["campaign_stage"],
        "git_sha": _git_sha(),
        "seeds": config["seeds"],
        "compute": _allocation(),
        "environment": _versions(),
        "results": results,
        "runtime_seconds": time.perf_counter() - started,
        "exit_contract": "nonzero on any failed accepted check",
    }
    print("=== QYA0Q28ssf CUMULATIVE EVIDENCE JSON ===")
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("=== END QYA0Q28ssf CUMULATIVE EVIDENCE JSON ===")


if __name__ == "__main__":
    main()

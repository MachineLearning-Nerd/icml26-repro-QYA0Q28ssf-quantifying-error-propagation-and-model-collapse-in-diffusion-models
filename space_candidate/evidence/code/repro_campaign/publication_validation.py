"""Evaluator-visible release, manifest, notebook, and historical-safety gates."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"
JUDGED_REVISION = "49401cddb554d5c3f7ae98d400567b8d6f10c028"
HISTORICAL = CANDIDATE / "historical" / f"judged_{JUDGED_REVISION}"
TEXT_SUFFIXES = {
    "",
    ".json",
    ".lock",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".txt",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        digest, relative = line.split(maxsplit=1)
        rows[relative.strip()] = digest
    return rows


def _validate_logbook() -> dict[str, Any]:
    logbook = json.loads((CANDIDATE / "logbook.json").read_text())
    if logbook["space_id"] != "DineshAI/QYA0Q28ssf":
        raise AssertionError("candidate targets wrong Space")
    slugs: set[str] = set()
    files: list[str] = []

    def visit(node: dict[str, Any]) -> None:
        slug = node["slug"]
        if slug in slugs:
            raise AssertionError(f"duplicate logbook slug: {slug}")
        slugs.add(slug)
        relative = node["file"]
        if not (CANDIDATE / relative).is_file():
            raise AssertionError(f"logbook page missing: {relative}")
        files.append(relative)
        for child in node.get("children", []):
            visit(child)

    visit(logbook["root"])
    expected = {
        "index",
        "c1",
        "c2",
        "c3",
        "c4",
        "c5",
        "c6",
        "method",
        "report",
        "release",
        "visibility",
        "historical",
        "verify",
        "overview",
    }
    if slugs != expected:
        raise AssertionError(f"unexpected navigation slugs: {sorted(slugs)}")
    return {"page_count": len(files), "slugs": sorted(slugs)}


def _validate_claim_pages() -> dict[str, Any]:
    required_common = (
        "uv run --frozen python -m repro_campaign.run",
        "HF `cpu-upgrade`",
        "Limitation",
        "raw",
        "checker",
    )
    verdicts = {
        "c1": "VERIFIED",
        "c2": "VERIFIED",
        "c3": "VERIFIED",
        "c4": "VERIFIED",
        "c5": "FALSIFIED",
        "c6": "BLOCKED",
    }
    rows = {}
    for claim, verdict in verdicts.items():
        path = CANDIDATE / "pages" / "claims" / f"{claim}.md"
        text = path.read_text()
        missing = [token for token in required_common if token.lower() not in text.lower()]
        if verdict not in text:
            missing.append(verdict)
        if not re.search(r"\b(run|jobs?)\b", text, re.IGNORECASE):
            missing.append("run metadata")
        if missing:
            raise AssertionError(f"{claim} canonical page missing {missing}")
        rows[claim] = {"verdict": verdict, "bytes": len(text.encode())}
    index = (CANDIDATE / "pages" / "index.md").read_text()
    for claim in verdicts:
        if f"| {claim.upper()} |" not in index:
            raise AssertionError(f"visibility matrix missing {claim}")
    return rows


def _validate_direct_links() -> dict[str, Any]:
    markdown_files = list(CANDIDATE.rglob("*.md"))
    checked = 0
    missing: list[str] = []
    for path in markdown_files:
        text = path.read_text()
        for target in re.findall(r"\]\((/[^)#?]+)", text):
            if target == "/":
                continue
            checked += 1
            if not (CANDIDATE / target.lstrip("/")).exists():
                missing.append(f"{path.relative_to(CANDIDATE)} -> {target}")
    if missing:
        raise AssertionError(f"broken candidate direct links: {missing}")
    return {"markdown_files": len(markdown_files), "direct_links_checked": checked}


def _validate_report_and_notebook() -> dict[str, Any]:
    report = CANDIDATE / "report" / "report.md"
    text = report.read_text()
    first_nonempty = [line for line in text.splitlines() if line.strip()][:2]
    if len(first_nonempty) < 2 or not first_nonempty[1].startswith("!["):
        raise AssertionError("report does not open with its strongest figure")
    images = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", text)
    if len(images) != 5:
        raise AssertionError(f"expected five evidence figures, saw {images}")
    for relative in images:
        image = report.parent / relative
        if not image.is_file():
            raise AssertionError(f"report image missing: {relative}")
        ET.parse(image)
    subprocess.run(
        ["marimo", "check", "notebooks/reproduction.py"],
        cwd=ROOT,
        check=True,
    )
    return {"figures": images, "marimo_check": "PASS"}


def _validate_historical_mirror() -> dict[str, Any]:
    manifest = _load_manifest(HISTORICAL / "SHA256SUMS.txt")
    mirrored = (
        "README.md",
        "logbook.json",
        "pages/index.md",
        "pages/overview/page.md",
        "pages/verify/page.md",
    )
    for relative in mirrored:
        observed = _sha256(HISTORICAL / relative)
        expected = manifest[relative]
        if observed != expected:
            raise AssertionError(f"historical hash mismatch: {relative}")
    if "Historical rejected baseline" not in (
        CANDIDATE / "pages" / "historical.md"
    ).read_text():
        raise AssertionError("historical navigation label missing")
    return {
        "protected_original_path_count": len(manifest),
        "exact_text_mirror_count": len(mirrored),
        "mirrored_paths": list(mirrored),
    }


def _validate_allowlist() -> dict[str, Any]:
    allowlist_path = CANDIDATE / "UPLOAD_ALLOWLIST.txt"
    manifest_path = CANDIDATE / "SHA256SUMS.txt"
    allowlist = [
        line for line in allowlist_path.read_text().splitlines() if line.strip()
    ]
    if allowlist != sorted(set(allowlist)):
        raise AssertionError("upload allowlist is not unique and sorted")
    for relative in allowlist:
        path = CANDIDATE / relative
        if not path.is_file():
            raise AssertionError(f"allowlisted path missing: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            raise AssertionError(f"non-text suffix in allowlist: {relative}")
        path.read_text()
    manifest = _load_manifest(manifest_path)
    expected_hashed = set(allowlist) - {"SHA256SUMS.txt"}
    if set(manifest) != expected_hashed:
        raise AssertionError("manifest paths differ from allowlist minus self")
    for relative, expected in manifest.items():
        if _sha256(CANDIDATE / relative) != expected:
            raise AssertionError(f"candidate manifest mismatch: {relative}")
    forbidden = {
        "index.html",
        "logbook.css",
        "logbook.js",
        "style.css",
        "trackio-logo.png",
        "trackio-logo-light.png",
        "trackio-wordmark-dark.png",
        "bucket-icon.svg",
    }
    if forbidden & set(allowlist):
        raise AssertionError(f"protected old paths unexpectedly uploaded: {forbidden & set(allowlist)}")
    return {"allowlisted_text_paths": len(allowlist), "hashed_paths": len(manifest)}


def _secret_scan() -> dict[str, Any]:
    patterns = (
        re.compile(r"hf_[A-Za-z0-9]{20,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
        re.compile(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"),
    )
    scanned = 0
    for path in CANDIDATE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(errors="strict")
        scanned += 1
        for pattern in patterns:
            if pattern.search(text):
                raise AssertionError(f"secret-like value found in {path}")
    return {"text_files_scanned": scanned, "findings": 0}


def run() -> dict[str, Any]:
    result = {
        "module": "publication_validation",
        "scientific_statuses": {
            "C1": "VERIFIED",
            "C2": "VERIFIED",
            "C3": "VERIFIED",
            "C4": "VERIFIED",
            "C5": "FALSIFIED",
            "C6": "BLOCKED",
        },
        "logbook": _validate_logbook(),
        "claim_pages": _validate_claim_pages(),
        "links": _validate_direct_links(),
        "report_notebook": _validate_report_and_notebook(),
        "historical": _validate_historical_mirror(),
        "release_files": _validate_allowlist(),
        "secret_scan": _secret_scan(),
        "visibility_matrix_complete": True,
        "candidate_release_gate": "PASS",
    }
    return result

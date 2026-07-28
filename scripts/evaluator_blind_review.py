#!/usr/bin/env python3
"""Traverse a candidate Space only through its evaluator-visible entrypoints."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_CLAIM_TERMS = (
    "source",
    "assumption",
    "raw",
    "checker",
    "control",
    "command",
    "runtime",
    "limitation",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_navigation(root: Path) -> tuple[list[Path], dict[str, Path]]:
    payload = json.loads((root / "logbook.json").read_text(encoding="utf-8"))
    pages: list[Path] = []
    slugs: dict[str, Path] = {}

    def walk(node: dict[str, object]) -> None:
        path = Path(str(node["file"]))
        pages.append(path)
        slugs[str(node["slug"])] = path
        for child in node.get("children", []):
            walk(child)

    walk(payload["root"])
    return pages, slugs


def review(root: Path) -> dict[str, object]:
    root = root.resolve()
    entrypoints = [Path("README.md"), Path("logbook.json"), Path("pages/index.md")]
    nav_pages, slugs = _load_navigation(root)
    queue = list(dict.fromkeys(entrypoints + nav_pages))
    opened: list[dict[str, str]] = []
    missing: list[str] = []
    claim_checks: dict[str, dict[str, object]] = {}
    seen: set[Path] = set()

    while queue:
        relative = queue.pop(0)
        if relative in seen:
            continue
        seen.add(relative)
        path = root / relative
        if not path.is_file():
            missing.append(relative.as_posix())
            continue
        opened.append({"path": relative.as_posix(), "sha256": _sha256(path)})
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if relative.parts[:2] == ("pages", "claims"):
            lowered = text.lower()
            claim_checks[relative.stem.upper()] = {
                term: term in lowered for term in REQUIRED_CLAIM_TERMS
            }
        for target in MARKDOWN_LINK.findall(text):
            target = target.split("#", 1)[0] if not target.startswith("#/") else target
            if target.startswith("#/"):
                slug = target[2:]
                if slug in slugs:
                    queue.append(slugs[slug])
                else:
                    missing.append(f"unknown slug {target} from {relative}")
            elif target.startswith("/"):
                queue.append(Path(target[1:]))
            elif target and "://" not in target and not target.startswith("#"):
                queue.append(
                    (root / relative.parent / target).resolve().relative_to(root)
                )

    incomplete_claims = {
        claim: [term for term, present in checks.items() if not present]
        for claim, checks in claim_checks.items()
        if not all(checks.values())
    }
    if len(claim_checks) != 6:
        missing.append(f"expected 6 canonical claim pages, found {len(claim_checks)}")
    if incomplete_claims:
        missing.append(f"incomplete claim pages: {incomplete_claims}")

    index = (root / "pages/index.md").read_text(encoding="utf-8")
    if "Historical rejected baseline" not in index:
        missing.append("historical navigation is not explicitly rejected")
    if "Evaluator-visible evidence matrix" not in index:
        missing.append("canonical visibility matrix is absent")

    return {
        "entrypoints": [path.as_posix() for path in entrypoints],
        "files_opened": opened,
        "claim_checks": claim_checks,
        "missing_or_incomplete": missing,
        "passed": not missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = review(args.root)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

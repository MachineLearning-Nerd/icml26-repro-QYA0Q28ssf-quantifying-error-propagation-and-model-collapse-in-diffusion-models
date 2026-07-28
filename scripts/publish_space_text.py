#!/usr/bin/env python3
"""Publish the exact text allowlist to the existing protected HF Space."""

from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import CommitOperationAdd, HfApi


SPACE_ID = "DineshAI/QYA0Q28ssf"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--expected-parent", required=True)
    parser.add_argument(
        "--message",
        default="Publish claim-by-claim cumulative reproduction evidence",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    allowlist_path = root / "UPLOAD_ALLOWLIST.txt"
    paths = [
        line.strip()
        for line in allowlist_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not paths or len(paths) != len(set(paths)):
        raise SystemExit("allowlist is empty or contains duplicates")

    api = HfApi()
    current = api.repo_info(SPACE_ID, repo_type="space").sha
    if current != args.expected_parent:
        raise SystemExit(
            f"protected parent mismatch: expected {args.expected_parent}, found {current}"
        )

    operations = []
    for relative in paths:
        source = root / relative
        if not source.is_file():
            raise SystemExit(f"missing allowlisted path: {relative}")
        source.read_text(encoding="utf-8")
        operations.append(
            CommitOperationAdd(path_in_repo=relative, path_or_fileobj=str(source))
        )

    result = api.create_commit(
        repo_id=SPACE_ID,
        repo_type="space",
        operations=operations,
        commit_message=args.message,
        parent_commit=args.expected_parent,
    )
    print(result.oid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

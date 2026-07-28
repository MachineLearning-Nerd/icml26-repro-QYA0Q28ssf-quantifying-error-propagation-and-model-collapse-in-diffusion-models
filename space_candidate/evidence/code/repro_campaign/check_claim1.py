"""Standalone independent checker for the C1 proof certificate."""

from __future__ import annotations

import json

from repro_campaign.claim1_girsanov import certificate_preflight


def main() -> None:
    print(json.dumps(certificate_preflight(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

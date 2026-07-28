"""Standalone checker for the C4 proof and C5 falsification certificates."""

from __future__ import annotations

import json

from repro_campaign.claim45_global import certificate_preflight


def main() -> None:
    print(json.dumps(certificate_preflight(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

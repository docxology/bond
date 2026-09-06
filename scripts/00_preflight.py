#!/usr/bin/env python3
"""Pre-flight check for manuscript rendering prerequisites."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "_template_resources"))

try:
    from infrastructure.rendering.preflight import run_manuscript_preflight  # noqa: E402
except ImportError as _exc:  # pragma: no cover - vendored infra guard
    sys.stderr.write(
        "00_preflight: cannot import infrastructure "
        f"({_exc}); expected the vendored mirror at _template_resources/infrastructure/\n"
    )
    raise SystemExit(2) from None


def main() -> int:
    """CLI entry point."""
    manuscript_dir = REPO_ROOT / "docs" / "manuscript"
    ok, message = run_manuscript_preflight(manuscript_dir)
    if ok:
        return 0
    sys.stderr.write(message)
    return 1


if __name__ == "__main__":
    sys.exit(main())

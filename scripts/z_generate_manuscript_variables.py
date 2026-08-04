#!/usr/bin/env python3
"""Hydrate bond-manuscript {{TOKEN}}s and resolve the manuscript tree.

Thin orchestrator: computes the compendium's token map from live discovery
(src.bond_manuscript.manuscript_variables) and writes the resolved tree to
``output/manuscript/`` for the renderer.  Mirrors the fleet's
z_generate_manuscript_variables.py contract.

Usage (from this directory):
    uv run python scripts/z_generate_manuscript_variables.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from bond_manuscript.manuscript_variables import generate_variables  # noqa: E402


def main() -> int:
    # Ensure suite deps are importable (path-deps from pyproject handle this in
    # the venv; this guard also covers a bare/template-root invocation).
    for _pkg in ("bond-api", "bond-utilities", "bond-coordinator"):
        _p = REPO.parent / _pkg / "src"
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))

    # The renderer may hydrate with this package's own .venv interpreter, which
    # lacks ``infrastructure`` (the template's repo package). Locate the template
    # root (the ancestor holding infrastructure/rendering/) and put it on path.
    _ancestor = REPO
    while _ancestor != _ancestor.parent and not (
        _ancestor / "infrastructure" / "rendering"
    ).is_dir():
        _ancestor = _ancestor.parent
    if (_ancestor / "infrastructure" / "rendering").is_dir() and str(_ancestor) not in sys.path:
        sys.path.insert(0, str(_ancestor))

    bond_root = REPO.parent
    variables = generate_variables(bond_root=bond_root)

    try:
        from infrastructure.rendering.manuscript_injection import write_resolved_manuscript_tree
    except ImportError:  # pragma: no cover - template infra guard
        print("infrastructure not importable; tokens: " + str(variables), file=sys.stderr)
        return 2

    root = REPO
    write_resolved_manuscript_tree(root, variables)
    print(f"[bond-manuscript] hydrated {len(variables)} tokens -> output/manuscript/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

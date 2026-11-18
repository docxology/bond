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

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from bond_manuscript.manuscript_variables import generate_variables  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Hydrate the BOND compendium")
    parser.add_argument("--bond-root", default=str(REPO.parent), help="PROJECT BOND workspace root")
    args = parser.parse_args()

    # Inside the template use its renderer. A standalone export carries the
    # pinned copy of the same rendering infrastructure in _template_resources.
    renderer_root = next(
        (parent for parent in REPO.parents if (parent / "infrastructure" / "rendering").is_dir()),
        REPO / "_template_resources",
    )
    sys.path.insert(0, str(renderer_root))

    try:
        from infrastructure.core.project_paths import resolve_source_manuscript_dir
        from infrastructure.rendering.manuscript_injection import write_resolved_manuscript_tree
    except ImportError as exc:  # pragma: no cover - renderer dependency guard
        print(f"Cannot import manuscript renderer from {renderer_root}: {exc}", file=sys.stderr)
        return 2

    if resolve_source_manuscript_dir(REPO) != REPO / "docs" / "manuscript":
        print("Expected wrapper manuscript sources in docs/manuscript/", file=sys.stderr)
        return 2
    variables = generate_variables(bond_root=Path(args.bond_root).resolve())
    output = write_resolved_manuscript_tree(REPO, variables)
    print(f"[bond-manuscript] hydrated {len(variables)} tokens with {renderer_root} -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

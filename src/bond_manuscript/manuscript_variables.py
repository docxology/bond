"""bond-manuscript manuscript variables: injected {{TOKEN}} map (pure core).

The compendium's own identified metrics come from live discovery, never
hand-authored in prose: package counts and suite identity resolve here so the
abstract/introduction/closing can reference them without drift.
"""

from __future__ import annotations

import json
from pathlib import Path

from .compendium import discover_packages

__all__ = ["generate_variables"]


def generate_variables(*, bond_root: Path | None = None) -> dict[str, str]:
    """Build the compendium ``{{TOKEN}}`` map from live discovery.

    Args:
        bond_root: PROJECT BOND workspace root; defaults to the suite root
            (three levels above this module).
    """
    bond_root = bond_root or Path(__file__).resolve().parents[3]
    packages = discover_packages(bond_root)
    films = [p for p in packages if p.kind == "film"]
    infra = [p for p in packages if p.kind == "infra"]
    gate = bond_root / "output" / "aggregate" / "gate_manifest.json"
    gate_ok = 0
    try:
        rows = json.loads(gate.read_text()).get("packages", [])
        package_slugs = {p.slug for p in packages}
        gate_ok = sum(
            1 for row in rows if row.get("package") in package_slugs and isinstance(row.get("coverage"), (int, float))
        )
    except (OSError, ValueError):
        rows = []
    return {
        "SUITE_TITLE": "PROJECT BOND — The Special-Agent Operations Compendium",
        "SUITE_TITLE_SHORT": "PROJECT BOND Compendium",
        "N_FILMS": str(len(films)),
        "N_INFRA": str(len(infra)),
        "N_PACKAGES": str(len(packages)),
        "N_GATE_MEASURED": str(gate_ok),
    }

"""bond-manuscript manuscript variables: injected {{TOKEN}} map (pure core).

The compendium's own identified metrics come from live discovery, never
hand-authored in prose: package counts and suite identity resolve here so the
abstract/introduction/closing can reference them without drift.
"""

from __future__ import annotations

from pathlib import Path

from .compendium import discover_packages
from .gate_manifest import read_gate_manifest

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
    gate = read_gate_manifest(bond_root) or {}
    package_slugs = {p.slug for p in packages}
    gate_measured = sum(slug in package_slugs and row.coverage is not None for slug, row in gate.items())
    return {
        "SUITE_TITLE": "PROJECT BOND — The Special-Agent Operations Compendium",
        "SUITE_TITLE_SHORT": "PROJECT BOND Compendium",
        "N_FILMS": str(len(films)),
        "N_INFRA": str(len(infra)),
        "N_PACKAGES": str(len(packages)),
        "N_GATE_MEASURED": str(gate_measured),
    }

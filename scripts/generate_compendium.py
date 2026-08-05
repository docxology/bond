#!/usr/bin/env python3
"""Generate the PROJECT BOND compendium manuscript (thin orchestrator).

Imports every package's manuscript into a single top-level manuscript under
``bond-manuscript/manuscript/``: introduction, generated architecture
chapter, one imported chapter per package, closing, and a unified
BibTeX bibliography merged from all 33 packages.

Usage (from this directory):
    uv run python scripts/generate_compendium.py [--bond-root ../..]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]  # -> projects/working/bond/bond-manuscript
sys_path_insert = __import__("sys")
for _dir in (
    REPO / "src",
    REPO.parent / "bond-api" / "src",
    REPO.parent / "bond-utilities" / "src",
    REPO.parent / "bond-coordinator" / "src",
):
    sys_path_insert.path.insert(0, str(_dir))

from bond_manuscript import (  # noqa: E402
    build_architecture_section,
    build_package_section,
    build_references_bib,
    build_references_section,
    discover_packages,
    import_package_abstract,
    parse_references,
)

#: Section filename patterns the generator owns and may overwrite.  Hand-authored
#: boundaries (00_abstract, 01_introduction, 90_closing) and support files
#: (preamble.md, SYNTAX.md, config.yaml.*, AGENTS.md, README.md) are protected.
_GENERATED_02 = re.compile(r"^02_suite_architecture\.md$")
_GENERATED_PKG = re.compile(r"^(0[34])_\d{2}_.+\.md$")
_GENERATED_99 = re.compile(r"^99_references\.md$")


def _rm_owned(manuscript: Path) -> None:
    for f in manuscript.glob("*.md"):
        if _GENERATED_02.match(f.name) or _GENERATED_PKG.match(f.name) or _GENERATED_99.match(f.name):
            f.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the BOND compendium manuscript")
    parser.add_argument("--bond-root", default=str(REPO.parent), help="PROJECT BOND workspace root")
    args = parser.parse_args()
    bond_root = Path(args.bond_root).resolve()
    manuscript = REPO / "manuscript"

    packages = discover_packages(bond_root)
    _rm_owned(manuscript)

    # 1) Unified bibliography first (chapters cite its keys).
    bibtext, all_refs = build_references_bib(packages, bond_root)
    (manuscript / "references.bib").write_text(bibtext)

    # 2) Architecture + roster chapter.
    (manuscript / "02_suite_architecture.md").write_text(build_architecture_section(packages, bond_root) + "\n")

    # 3) One imported chapter per package (films 03_xx, infra 04_xx).
    film_n = infra_n = 0
    for pkg in packages:
        abstract = import_package_abstract(bond_root / pkg.slug)
        keys = [ref.key for ref in parse_references(bond_root / pkg.slug, pkg.slug)]
        if pkg.kind == "film":
            film_n += 1
            filename = f"{'03'}_{film_n:02d}_{pkg.slug}.md"
        else:
            infra_n += 1
            filename = f"{'04'}_{infra_n:02d}_{pkg.slug}.md"
        (manuscript / filename).write_text(
            build_package_section(pkg, bond_root / pkg.slug, abstract, keys, film_n + infra_n) + "\n"
        )

    # 4) References chapter listing the unified bibliography.
    (manuscript / "99_references.md").write_text("\n".join(build_references_section(all_refs).splitlines()) + "\n")

    print(
        f"compendium written: {len(packages)} packages, {len(all_refs)} references, "
        f"{film_n} film chapters, {infra_n} infra chapters -> {manuscript}"
    )

    # A provider that stops importing costs its chapter the mission brief line.
    # That used to happen silently; the build now fails loudly instead, because
    # a compendium missing content it should carry is not a successful build.
    from bond_manuscript.compendium import BRIEF_FAILURES

    if BRIEF_FAILURES:
        print("\nERROR: could not load MissionProvider for:", file=sys.stderr)
        for slug, err in sorted(BRIEF_FAILURES.items()):
            print(f"  {slug}: {err}", file=sys.stderr)
        print(
            "These chapters lost their mission brief line. Install the missing "
            "dependency into this package's environment and re-run.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

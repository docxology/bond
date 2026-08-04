"""Tests for the bond-manuscript compendium generator (real data, zero mocks).

Covers discovery of all 33 packages, the generated manuscript sections, the
unified BibTeX bibliography, token hydration of imported abstracts,
deterministic regeneration, and the thin CLI.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from bond_manuscript import (
    build_references_bib,
    discover_packages,
    import_package_abstract,
    parse_references,
)
from bond_manuscript.manuscript_variables import generate_variables

BOND = Path(__file__).resolve().parents[2]
MANUSCRIPT = BOND / "bond-manuscript" / "manuscript"
N_FILMS = 27
N_INFRA = 6


def _entry_count(bib: str) -> int:
    return len(re.findall(r"@\w+\s*\{\s*([\w:.-]+)\s*,", bib))


def test_discover_33_packages() -> None:
    packages = discover_packages(BOND)
    assert len(packages) == 33
    assert sum(p.kind == "film" for p in packages) == N_FILMS
    assert sum(p.kind == "infra" for p in packages) == N_INFRA
    assert packages[0].slug == "dr_no"  # canon order
    assert {"bond-api", "bond-cli", "bond-ops"}.issubset({p.slug for p in packages})


def test_manuscript_sections_complete() -> None:
    files = {p.name for p in MANUSCRIPT.glob("*.md")}
    assert "00_abstract.md" in files and "01_introduction.md" in files
    assert "02_suite_architecture.md" in files
    assert "90_closing.md" in files and "99_references.md" in files
    film_chapters = [f for f in files if f.startswith("03_")]
    infra_chapters = [f for f in files if f.startswith("04_")]
    assert len(film_chapters) == N_FILMS
    assert len(infra_chapters) == N_INFRA


def test_imported_abstract_is_token_resolved() -> None:
    """goldfinger's abstract is imported with {{TOKEN}}s resolved to real values."""
    abstract = import_package_abstract(BOND / "goldfinger")
    assert abstract  # non-empty
    assert "{{" not in abstract  # no leaked tokens
    # Goldfinger's variables resolve to concrete economics.
    assert "corner" in abstract.lower() and "market" in abstract.lower()


def test_unified_bibliography_merged() -> None:
    bibtext, refs = build_references_bib(discover_packages(BOND), BOND)
    assert len(refs) >= 100  # 100+ unique keys merged from the fleet
    keys = [r.key for r in refs]
    assert len(keys) == len(set(keys))  # all keys unique
    # Both formats survived: real BibTeX (e.g. the world is not enough flow refs)
    # and converted plain lists (goldfinger *_refN).
    assert any(k.startswith("goldfinger_ref") for k in keys)


def test_generated_bibtex_is_balanced() -> None:
    bib = (MANUSCRIPT / "references.bib").read_text()
    assert bib.count("{") == bib.count("}")
    assert _entry_count(bib) >= 100
    # No plain-text `[n]` fragments leaked into the BibTeX.
    assert not re.search(r"^\s*\[[0-9]+\]", bib, re.M)


def test_every_package_chapter_present_on_disk() -> None:
    for pkg in discover_packages(BOND):
        if pkg.kind == "film":
            matching = list(MANUSCRIPT.glob(f"03_*_{pkg.slug}.md"))
        else:
            matching = list(MANUSCRIPT.glob(f"04_*_{pkg.slug}.md"))
        assert matching, f"missing chapter for {pkg.slug}"
        text = matching[0].read_text()
        assert pkg.codename in text


def test_references_bib_present() -> None:
    assert (MANUSCRIPT / "references.bib").is_file()
    assert (MANUSCRIPT / "references.bib").read_text().count("@") >= 100


def test_manuscript_variables_counts() -> None:
    variables = generate_variables(bond_root=BOND)
    assert variables["N_PACKAGES"] == "33"
    assert variables["N_FILMS"] == str(N_FILMS)
    assert variables["N_INFRA"] == str(N_INFRA)


def test_degenerate_no_duplicate_abstract_content() -> None:
    # Distinct films should not share identical imported chapters.
    g = (MANUSCRIPT / "03_03_goldfinger.md").read_text()
    d = (MANUSCRIPT / "03_01_dr_no.md").read_text()
    assert g != d


@pytest.mark.skipif(not (BOND / "output/aggregate/gate_manifest.json").is_file(), reason="gate manifest not present")
def test_script_smoke_regen() -> None:
    result = subprocess.run(
        [sys.executable, str(BOND / "bond-manuscript" / "scripts" / "generate_compendium.py")],
        capture_output=True,
        text=True,
        cwd=str(BOND / "bond-manuscript"),
        check=False,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.skipif(not (BOND / "output/aggregate/gate_manifest.json").is_file(), reason="gate manifest not present")
def test_regeneration_is_deterministic() -> None:
    before = (MANUSCRIPT / "03_03_goldfinger.md").read_bytes()
    bib_before = (MANUSCRIPT / "references.bib").read_bytes()
    subprocess.run(
        [sys.executable, str(BOND / "bond-manuscript" / "scripts" / "generate_compendium.py")],
        capture_output=True,
        cwd=str(BOND / "bond-manuscript"),
        check=False,
    )
    assert (MANUSCRIPT / "03_03_goldfinger.md").read_bytes() == before
    assert (MANUSCRIPT / "references.bib").read_bytes() == bib_before


def test_parse_references_plain_and_bibtex() -> None:
    gold = parse_references(BOND / "goldfinger", "goldfinger")
    assert gold and gold[0].key.startswith("goldfinger_ref")
    tnd = parse_references(BOND / "the_world_is_not_enough", "the_world_is_not_enough")
    assert tnd and any(k in {r.key for r in tnd} for k in ["ford_fulkerson", "edmonds_karp"])


def test_brief_line_real_provider() -> None:
    from bond_manuscript import compendium

    line = compendium._brief_line(BOND / "goldfinger", "goldfinger")
    assert "GRAND SLAM" in line
    assert "corner the gold market" in line


def test_build_package_section_film() -> None:
    from bond_manuscript import compendium

    pkg = discover_packages(BOND)[2]  # goldfinger
    abstract = import_package_abstract(BOND / "goldfinger")
    section = compendium.build_package_section(
        pkg, BOND / "goldfinger", abstract, ["goldfinger_ref1", "goldfinger_ref2"], 3
    )
    assert "# Goldfinger (1964) — GRAND SLAM" in section
    assert "## Concepts" in section and "macroeconomic attack" in section
    assert "## Abstract (imported" in section
    assert "## Sources" in section and "@goldfinger_ref1" in section


def test_build_architecture_section() -> None:
    from bond_manuscript import compendium

    packages = discover_packages(BOND)
    section = compendium.build_architecture_section(packages, BOND)
    assert "# Suite Architecture" in section
    assert "Layer 0 · utilities" in section
    assert "## Roster" in section and "bond-api" in section
    assert "goldfinger" in section
    if (BOND / "output/aggregate/gate_manifest.json").is_file():
        assert "## Measured gate" in section


def test_build_references_section_groups_by_source() -> None:
    from bond_manuscript import compendium

    packages = discover_packages(BOND)
    _, refs = build_references_bib(packages, BOND)
    section = compendium.build_references_section(refs)
    assert "# References" in section
    assert "`goldfinger`" in section  # grouped by source package
    assert refs[0].key in section


def test_import_abstract_fallback_strips_tokens(tmp_path) -> None:
    """A package without hydrated output and without variables -> tokens stripped."""
    fake = tmp_path / "fake_film"
    (fake / "manuscript").mkdir(parents=True)
    (fake / "manuscript" / "00_abstract.md").write_text("# Abstract\nA value of {{SOME_VAR}} and a price of $12.50/oz.")
    abstract = import_package_abstract(fake)
    assert "{{" not in abstract
    assert "price of $12.50/oz" in abstract
    assert "Abstract" not in abstract.replace("abstract", "")  # heading dropped


def test_build_package_section_infra() -> None:
    from bond_manuscript import compendium

    packages = discover_packages(BOND)
    infra = next(p for p in packages if p.slug == "bond-api")
    section = compendium.build_package_section(infra, BOND / "bond-api", "protocol + registry", ["bond_api_key"], 2)
    assert "THE PROTOCOL" in section
    assert "## Concepts" in section

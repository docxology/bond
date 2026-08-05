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
    # Every package that ships a bibliography must actually reach the merge.
    # This previously asserted `goldfinger_ref*`, a placeholder key prefix from
    # before the packages carried real citations. Once goldfinger's references
    # became genuine (walras1874elements, kyle1985continuous, ...) the
    # assertion failed — it was pinned to the fake data, so it would also have
    # passed forever had the real references never arrived.
    contributing = {r.source_package for r in refs}
    assert "goldfinger" in contributing
    assert len(contributing) >= 20, sorted(contributing)


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
    # Structural properties, not a placeholder key prefix: every parsed entry
    # must carry a non-empty key, a bibtex body, and its source package.
    assert gold
    assert all(r.key and r.bibtex.startswith("@") for r in gold)
    assert {r.source_package for r in gold} == {"goldfinger"}
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


# --------------------------------------------------------------------------- #
# Plain reference-list ingestion
#
# Every package in the fleet now ships real BibTeX, so `_plain_ref_to_bibtex`
# and the plain-list branch of `parse_references` lost their only real-data
# exerciser when goldfinger's placeholder `[n] ...` list became genuine
# citations. The format is still supported on input, so it is covered here
# directly with real files rather than left to rot behind a branch nothing
# reaches.
# --------------------------------------------------------------------------- #


def _plain_bib(tmp_path, body: str):
    pkg = tmp_path / "plainpkg"
    (pkg / "manuscript").mkdir(parents=True)
    (pkg / "manuscript" / "references.bib").write_text(body)
    return pkg


def test_parse_references_plain_list(tmp_path) -> None:
    pkg = _plain_bib(
        tmp_path,
        "[1] Kahn, D., *The Codebreakers*, Scribner, 1996. — History of secret communication.\n"
        "[2] Shannon, C. E., *Communication Theory of Secrecy Systems*, 1949.\n"
        "not a reference line, skipped\n",
    )
    refs = parse_references(pkg, "plainpkg")
    assert [r.key for r in refs] == ["plainpkg_ref1", "plainpkg_ref2"]
    assert all(r.bibtex.startswith("@misc{") for r in refs)
    assert all(r.source_package == "plainpkg" for r in refs)

    first = refs[0].bibtex
    assert "title   = {The Codebreakers}" in first
    assert "year    = {1996}" in first
    assert "note    = {History of secret communication.}" in first
    assert "Kahn, D." in first
    # The italic title must not be duplicated back into the author field.
    author_line = next(ln for ln in first.splitlines() if ln.strip().startswith("author"))
    assert "The Codebreakers" not in author_line

    # An entry with no note omits the note field entirely.
    assert "note" not in refs[1].bibtex


def test_parse_references_plain_untitled_falls_back_to_text(tmp_path) -> None:
    """No italic title: the whole line becomes the title and author is kept."""
    pkg = _plain_bib(tmp_path, "[1] Anonymous technical note, 2011.\n")
    (ref,) = parse_references(pkg, "plainpkg")
    assert "title   = {Anonymous technical note, 2011.}" in ref.bibtex
    assert "year    = {2011}" in ref.bibtex


def test_parse_references_missing_file_returns_empty(tmp_path) -> None:
    empty = tmp_path / "nobib"
    (empty / "manuscript").mkdir(parents=True)
    assert parse_references(empty, "nobib") == []


def test_resolve_tokens_coerces_non_string_values(tmp_path) -> None:
    """manuscript_variables.json carries real JSON types, not just strings.

    A numeric token returned straight from `re.sub` raises "expected str
    instance, int found" and took the whole compendium build down until the
    resolver started coercing. Pinned here so it cannot regress.
    """
    pkg = tmp_path / "numeric"
    (pkg / "manuscript").mkdir(parents=True)
    (pkg / "output" / "data").mkdir(parents=True)
    (pkg / "manuscript" / "00_abstract.md").write_text(
        "# Abstract\nRan {{N_TRIALS}} trials at {{RATE}} with flag {{FLAG}} and {{MISSING}}."
    )
    (pkg / "output" / "data" / "manuscript_variables.json").write_text(
        '{"N_TRIALS": 512, "RATE": 0.75, "FLAG": true, "NOTHING": null}'
    )
    abstract = import_package_abstract(pkg)
    assert "512" in abstract and "0.75" in abstract and "True" in abstract
    assert "{{" not in abstract  # unresolved stragglers stripped


def test_import_abstract_prefers_hydrated_output(tmp_path) -> None:
    pkg = tmp_path / "hydrated"
    (pkg / "manuscript").mkdir(parents=True)
    (pkg / "output" / "manuscript").mkdir(parents=True)
    (pkg / "manuscript" / "00_abstract.md").write_text("# Abstract\nSOURCE version.")
    (pkg / "output" / "manuscript" / "00_abstract.md").write_text("# Abstract\nHYDRATED version.")
    assert "HYDRATED" in import_package_abstract(pkg)


def test_import_abstract_absent_returns_empty(tmp_path) -> None:
    pkg = tmp_path / "noabstract"
    (pkg / "manuscript").mkdir(parents=True)
    assert import_package_abstract(pkg) == ""


def test_import_abstract_survives_corrupt_variables(tmp_path) -> None:
    """Unparseable variables JSON must strip tokens, not raise."""
    pkg = tmp_path / "corrupt"
    (pkg / "manuscript").mkdir(parents=True)
    (pkg / "output" / "data").mkdir(parents=True)
    (pkg / "manuscript" / "00_abstract.md").write_text("# Abstract\nValue {{X}} here.")
    (pkg / "output" / "data" / "manuscript_variables.json").write_text("{not json")
    abstract = import_package_abstract(pkg)
    assert "{{" not in abstract and "Value" in abstract


def test_discover_packages_skips_absent_manuscripts(tmp_path) -> None:
    """Roster entries without a manuscript directory are not emitted."""
    assert discover_packages(tmp_path) == []


def test_brief_line_missing_provider_returns_empty(tmp_path) -> None:
    from bond_manuscript import compendium

    assert compendium._brief_line(tmp_path / "nope", "nope") == ""

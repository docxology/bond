"""bond-manuscript — the PROJECT BOND compendium generator (pure core).

Builds a single top-level manuscript that WRAPS the 33 package manuscripts:
an introduction, a generated suite-architecture chapter, one imported chapter
per package, a closing, and a UNIFIED BibTeX bibliography merged from every
package's references.

Content is imported, never hand-duplicated:

* Each package chapter's abstract is taken from that package's own
  manuscript.  When the package has a token-hydrated chapter
  (``output/manuscript/00_abstract.md``) we import it directly; otherwise we
  resolve ``{{TOKEN}}``s from the package's ``output/data/manuscript_variables.json``
  (or strip unresolved markers as a last resort).
* The unified bibliography (``references.bib``) is merged from every package's
  ``manuscript/references.bib``.  Both formats are handled: real BibTeX
  ``@entry`` blocks are preserved verbatim; plain-text ``[n] ...`` reference
  lists are converted into deterministic ``@misc`` entries keyed
  ``<slug>_ref<n>``.

Deterministic: same package tree in -> byte-identical manuscript out.
"""

from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "PackageInfo",
    "Reference",
    "build_references_bib",
    "build_architecture_section",
    "build_package_section",
    "discover_packages",
    "import_package_abstract",
    "parse_references",
]

#: Architecture chapter numbering (films 03_xx, infra 04_xx) — must sort
#: correctly in the renderer's filename concatenation.
FILM_NUMBER = "03"
INFRA_NUMBER = "04"

_TOKEN = re.compile(r"\{\{\s*[A-Za-z0-9_]+\s*\}\}")
_YEAR = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
_ITALIC = re.compile(r"\*([^*]+)\*")


@dataclass(frozen=True)
class PackageInfo:
    """Catalogue entry for one BOND package."""

    slug: str
    title: str
    year: str
    codename: str
    kind: str  # "film" | "infra"
    concepts: tuple[str, ...] = ()
    phenomena: str = ""  # one-line film subtitle / infra role


@dataclass(frozen=True)
class Reference:
    """A single merged bibliography entry."""

    key: str
    bibtex: str
    source_package: str


# --------------------------------------------------------------------------- #
# Package discovery
# --------------------------------------------------------------------------- #


def discover_packages(bond_root: Path) -> list[PackageInfo]:
    """Return the 33 package catalogue from the coordinator registry + disk.

    Uses the coordinator's canon-ordered 27-film ROSTER (single source of truth
    for film metadata); the 6 infrastructure packages are carried as data here.
    A package is included only if it has a ``manuscript/`` on disk.
    """
    from bond_coordinator.registry import ROSTER  # type: ignore[import-not-found]  # lazy: suite layer 2

    infra = OrderedDict(
        [
            ("bond-utilities", ("Q-Branch primitives — ciphers, codenames, clock, provenance, fixtures", "Q-BRANCH")),
            ("bond-api", ("The frozen MissionProvider protocol, registry, discovery, serialization", "THE PROTOCOL")),
            ("bond-coordinator", ("Fleet registry, mission ledger, status, situation room", "MISSION CONTROL")),
            ("bond-orchestrator", ("Multi-package mission DAG runner + real-film binding", "DAG 00")),
            ("bond-cli", ("Unified terminal front door (bond list/brief/…/run/status/gadgets)", "THE FRONT DOOR")),
            ("bond-ops", ("Fleet inventory, gates, health, provisioning", "QUARTERMASTER")),
        ]
    )
    packages: list[PackageInfo] = []
    for i, rec in enumerate(ROSTER, start=1):
        slug = rec.slug
        if not (bond_root / slug / "manuscript").is_dir():
            continue
        packages.append(
            PackageInfo(
                slug=slug,
                title=f"{rec.film} ({rec.year})",
                year=str(rec.year),
                codename=rec.codename,
                kind="film",
                concepts=tuple(rec.concepts),
            )
        )
    for slug, (phenomena, codename) in infra.items():
        if not (bond_root / slug / "manuscript").is_dir():
            continue
        packages.append(
            PackageInfo(
                slug=slug,
                title=slug.replace("-", " ").title(),
                year="2026",
                codename=codename,
                kind="infra",
                phenomena=phenomena,
            )
        )
    return packages


# --------------------------------------------------------------------------- #
# Abstract import (token-aware)
# --------------------------------------------------------------------------- #


def _resolve_tokens(text: str, variables: "dict[str, object]") -> str:
    """Substitute ``{TOKEN}`` spans from a package's manuscript variables.

    Values are coerced to ``str``. ``manuscript_variables.json`` carries real
    JSON types, so a tokenized metric arrives as an int or float, not a string;
    returning one straight from ``re.sub`` raises "expected str instance, int
    found" and takes the whole compendium build down with it. The annotation
    said ``dict[str, str]``, which is what made the wrong assumption look safe.
    """

    def _sub(match: "re.Match[str]") -> str:
        name = match.group(0).strip("{}").strip()
        value = variables.get(name, "")
        return "" if value is None else str(value)

    return _TOKEN.sub(_sub, text)


def import_package_abstract(package_dir: Path) -> str:
    """Return the package's abstract prose, tokens resolved when possible.

    Preference: hydrated chapter -> resolve source tokens from the package's
    manuscript_variables.json -> strip tokens.  Returns a cleaned paragraph.
    """
    hydrated = package_dir / "output" / "manuscript" / "00_abstract.md"
    if hydrated.is_file():
        return _clean(hydrated.read_text())
    source = package_dir / "manuscript" / "00_abstract.md"
    if not source.is_file():
        return ""
    text = source.read_text()
    variables_path = package_dir / "output" / "data" / "manuscript_variables.json"
    if variables_path.is_file():
        try:
            import json

            variables = json.loads(variables_path.read_text())
        except (OSError, ValueError):
            variables = {}
        resolved = _resolve_tokens(text, variables)
        if _TOKEN.search(resolved):
            resolved = _TOKEN.sub("", resolved)  # any stragglers
        return _clean(resolved)
    return _clean(_TOKEN.sub("", text))


def _clean(text: str) -> str:
    """Collapse heading/markdown cruft into a single running paragraph."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Drop a leading "# Abstract" heading if present.
    while lines and lines[0].startswith("#"):
        lines = lines[1:]
    body = " ".join(lines)
    body = re.sub(r"\s+", " ", body).strip()
    return body


# --------------------------------------------------------------------------- #
# Reference parsing + unified BibTeX
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class _BibBlock:
    """One parsed bib source: either real @entries or plain ``[n]`` lines."""

    slug: str
    entries: list[Reference] = field(default_factory=list)


def _parse_bibtex_entries(text: str, slug: str) -> list[Reference]:
    """Split text into real '@type{key,...}' blocks (skipping @comment)."""
    entries: list[Reference] = []
    # Reconstruct each @entry block by brace depth.
    pos = 0
    while True:
        m = re.search(r"@(\w+)\s*\{\s*([^,{]+)\s*,", text[pos:])
        if not m:
            break
        start = pos + m.start()
        body_start = text.index("{", start)
        depth, i = 1, body_start + 1
        while depth and i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        block = text[start:i]
        etype = m.group(1).lower()
        key = m.group(2).strip()
        if etype == "comment":
            pos = i
            continue
        entries.append(Reference(key=key, bibtex=block.strip(), source_package=slug))
        pos = i
    # De-duplicate by key within this package (later wins).
    dedup: "OrderedDict[str, Reference]" = OrderedDict()
    for ref in entries:
        dedup[ref.key] = ref
    return list(dedup.values())


def _plain_ref_to_bibtex(line: str, slug: str, index: int) -> Reference:
    """Convert a plain ``[n] Author, *Title*, publisher, year. — note`` line."""
    text = line.strip()
    m = re.match(r"\[\s*\d+\s*\]\s*(.*)$", text)
    if m:
        text = m.group(1).strip()
    key = f"{slug}_ref{index}"
    title_m = _ITALIC.search(text)
    title = title_m.group(1).strip() if title_m else ""
    note = ""
    if " — " in text:
        text, note = text.split(" — ", 1)
        note = note.strip()
    title = title or text
    year_m = _YEAR.search(text)
    year = year_m.group(1) if year_m else ""
    author = text
    if title_m:
        author = (text[: title_m.start()] + " " + text[title_m.end() :]).strip(" ,;")
    author = author or "Anonymous"
    fields = [f"author  = {{{author}}}", f"title   = {{{title}}}"]
    if year:
        fields.append(f"year    = {{{year}}}")
    if note:
        fields.append(f"note    = {{{note}}}")
    bibtex = "@misc{" + key + ",\n" + "\n".join(f"  {f}" for f in fields) + "\n}\n"
    return Reference(key=key, bibtex=bibtex, source_package=slug)


def parse_references(package_dir: Path, slug: str) -> list[Reference]:
    """Parse a package's references.bib into merged Reference entries."""
    bib = package_dir / "manuscript" / "references.bib"
    if not bib.is_file():
        return []
    text = bib.read_text()
    if re.search(r"@\w+\s*\{", text):
        return _parse_bibtex_entries(text, slug)
    refs: list[Reference] = []
    index = 0
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped.startswith("[") or "]" not in stripped:
            continue
        index += 1
        refs.append(_plain_ref_to_bibtex(stripped, slug, index))
    return refs


def build_references_bib(packages: list[PackageInfo], bond_root: Path) -> tuple[str, list[Reference]]:
    """Merge every package's references into one unified BibTeX string.

    Returns (bibtex_text, ordered_references).  Real @entries are preserved
    verbatim and de-duplicated by key; plain lists converted to @misc.  The
    compendium's own exemplar-inherited entries are excluded (not bond content).
    """
    merged: "OrderedDict[str, Reference]" = OrderedDict()
    for pkg in packages:
        for ref in parse_references(bond_root / pkg.slug, pkg.slug):
            merged[ref.key] = ref  # later identical keys are idempotent
    bibtex = "@comment{ Unified references.bib merged from all PROJECT BOND package manuscripts. }\n\n"
    bibtex += "\n".join(ref.bibtex for ref in merged.values()) + "\n"
    return bibtex, list(merged.values())


# --------------------------------------------------------------------------- #
# Chapter sections
# --------------------------------------------------------------------------- #


def _brief_line(package_dir: Path, slug: str) -> str:
    """Real mission codename/objectives from the film's MissionProvider."""
    try:
        import sys

        from bond_api.discovery import load_provider  # type: ignore[import-not-found]

        search = package_dir / "src"
        if not (search / slug / "mission.py").is_file():
            return ""
        sys.path.insert(0, str(search))
        try:
            provider = load_provider(slug, search_paths=[str(search)])
            brief = provider.brief()
        finally:
            sys.path.remove(str(search))
        objs = "; ".join(brief.objectives)
        return f"Mission **{brief.codename}**: {objs}."
    except Exception:
        return ""


def build_package_section(
    pkg: PackageInfo,
    package_dir: Path,
    abstract: str,
    reference_keys: list[str],
    index: int,
) -> str:
    """One imported chapter for a package (film or infrastructure)."""
    header = f"# {pkg.title} — {pkg.codename}"
    concepts = ", ".join(pkg.concepts) if pkg.concepts else pkg.phenomena
    brief = _brief_line(package_dir, pkg.slug)
    lines = [
        header,
        "",
        f"*{pkg.kind} package · mission codename {pkg.codename}*." + (f" {brief}" if brief else ""),
        "",
        "## Concepts",
        "",
        concepts,
        "",
        "## Abstract (imported from the package manuscript)",
        "",
        abstract,
        "",
    ]
    if reference_keys:
        cites = "; ".join(f"@{key}" for key in reference_keys)
        lines += ["## Sources", "", cites, ""]
    return "\n".join(lines)


def build_architecture_section(packages: list[PackageInfo], bond_root: Path) -> str:
    """Generated suite-architecture chapter: layered topology + gate table."""
    lines = [
        "# Suite Architecture",
        "",
        "PROJECT BOND is a 33-package fleet: 27 film packages, each a standalone",
        "software package implementing its film's concepts, plus 6 mission-",
        "infrastructure packages that provide the contract and the operation.",
        "",
        "## Layers",
        "",
        "| Layer | Packages |",
        "| --- | --- |",
        "| Layer 0 · utilities | `bond-utilities` (Q-Branch primitives) |",
        "| Layer 1 · protocol | `bond-api` (the frozen MissionProvider contract) |",
        "| Layer 2 · control | `bond-coordinator` (registry, ledger, situation room) |",
        "| Layer 3 · orchestration | `bond-orchestrator` (mission DAG runner, real-film binding) |",
        "| Layer 4 · ops | `bond-cli` (front door), `bond-ops` (fleet gates) |",
        "| Films | 27 standalone packages, one per James Bond film |",
        "",
        "Every film implements the frozen `bond_api` `MissionProvider` and is",
        "discovered by `bond_api.discovery`. The compendium imports one chapter per",
        "package below.",
        "",
        "## Roster",
        "",
    ]
    table = ["| # | Package | Codename |", "|---|---------|----------|"]
    for i, pkg in enumerate(packages, start=1):
        table.append(f"| {i} | `{pkg.slug}` — {pkg.title} | {pkg.codename} |")
    lines += table + [""]
    gate = bond_root / "output" / "aggregate" / "gate_manifest.json"
    if gate.is_file():
        try:
            import json

            rows = json.loads(gate.read_text()).get("packages", [])
            cov = {p["package"]: p["coverage"] for p in rows}
        except (OSError, ValueError):
            cov = {}
        lines += ["## Measured gate", ""]
        gate_rows = ["| Package | Coverage |", "| --- | --- |"]
        for pkg in packages:
            c = cov.get(pkg.slug)
            gate_rows.append(f"| `{pkg.slug}` | {f'{c:.1f}%' if isinstance(c, (int, float)) else 'n/a'} |")
        lines += gate_rows + [""]
    return "\n".join(lines)


def build_references_section(references: list[Reference]) -> str:
    """99_references.md listing of the unified bibliography (by source package)."""
    lines = ["# References", ""]
    lines.append("Merged automatically from every package's `manuscript/references.bib` into")
    lines.append("the unified `references.bib`. Keys are cited from the package chapters.")
    lines.append("")
    current = None
    for ref in references:
        if ref.source_package != current:
            current = ref.source_package
            lines.append(f"## `{current}`")
            lines.append("")
        m = re.search(r"title\s*=\s*\{(.+?)\}", ref.bibtex, re.S)
        title = m.group(1).replace("{", "").replace("}", "") if m else ""
        am = re.search(r"author\s*=\s*\{(.+?)\}", ref.bibtex, re.S)
        author = am.group(1).replace("{", "").replace("}", "") if am else ""
        lines.append(f"- **{ref.key}** — {author}. *{title}*.")
        lines.append("")
    return "\n".join(lines)

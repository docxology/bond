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
import unicodedata
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "PackageInfo",
    "Reference",
    "build_references_bib",
    "build_architecture_section",
    "build_package_section",
    "ImportedChapter",
    "discover_packages",
    "import_package_abstract",
    "import_package_sections",
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


@dataclass(frozen=True)
class ImportedChapter:
    """The full imported chapter for one package.

    ``body`` is the complete chapter: the package's abstract, every authored
    section (01..NN) imported in canon order, and its ``## Sources`` list.
    ``figures`` maps each figure the package manuscript embeds (resolved to an
    absolute source path) to its namespaced destination filename in the
    compendium's ``output/figures/``.  The core never writes; the orchestrator
    copies these files.
    """

    body: str
    figures: tuple[tuple[Path, str], ...] = ()


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


#: Where a package may keep its generated manuscript variables. 31 packages use
#: ``output/data/``; bond-cli and bond-ops write ``output/variables/``. Reading
#: only the majority path made those two abstracts import with every token
#: stripped, so the compendium rendered "**** (**)" instead of the package name
#: — a silent degradation, since stripping unresolved tokens is a legitimate
#: fallback and nothing distinguished "no variables" from "variables elsewhere".
_VARIABLE_PATHS = ("data", "variables")


def _find_variables_json(package_dir: Path) -> Path | None:
    for sub in _VARIABLE_PATHS:
        candidate = package_dir / "output" / sub / "manuscript_variables.json"
        if candidate.is_file():
            return candidate
    return None


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
    variables_path = _find_variables_json(package_dir)
    if variables_path is not None:
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


#: pandoc-crossref references, bracketed (``[@sec:results]``) or bare (``@sec:results``).
_CROSSREF = re.compile(r"\[?@(sec|def|prop|thm|lem|cor|fig|eq|tbl|lst):([\w:-]+)\]?")


def _strip_crossrefs(body: str) -> str:
    """Neutralise cross-references that cannot resolve in the wrapper.

    A package abstract may cite its own sections and theorems. Those labels are
    real inside that package's manuscript but absent from the compendium, where
    they render as ``Section sec. ??`` and ``[?]`` in the combined PDF. Section
    references become plain prose; pointers to definitions, propositions and
    floats are dropped along with any parenthetical or dash that introduced them.
    """

    def _sub(match: "re.Match[str]") -> str:
        kind, name = match.group(1), match.group(2).split(":")[-1]
        if kind == "sec":
            return f"the {name.replace('-', ' ').replace('_', ' ')} section"
        return ""

    body = _CROSSREF.sub(_sub, body)
    # Tidy the punctuation the removed references leave behind.
    body = re.sub(r"\(\s*[,;]?\s*\)", "", body)  # ()
    body = re.sub(r"\s+—\s*\)", ")", body)  # " — )"
    body = re.sub(r"\bSection\s+the\b", "The", body)
    body = re.sub(r"\bsection\s+the\b", "the", body)
    body = re.sub(r"\s+([,.;:])", r"\1", body)
    body = re.sub(r"([,;])\s*\1+", r"\1", body)
    return re.sub(r"\s{2,}", " ", body).strip()


def _clean(text: str) -> str:
    """Collapse heading/markdown cruft into a single running paragraph."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Drop a leading "# Abstract" heading if present.
    while lines and lines[0].startswith("#"):
        lines = lines[1:]
    body = " ".join(lines)
    body = re.sub(r"\s+", " ", body).strip()
    return _strip_crossrefs(body)


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
# Full manuscript import
# --------------------------------------------------------------------------- #

#: A package content-section filename: ``NN_*.md`` with NN in 01..98.  The
#: ``99_references.md`` chapter is handled as the unified bibliography instead
#: of being re-imported per package, and ``00_abstract.md`` is imported as the
#: cleaned abstract paragraph.  Everything else is carried verbatim.
_SECTION_RE = re.compile(r"^(0[1-9]|[1-8]\d)_[^/]+\.md$")


def _package_variables(package_dir: Path) -> "dict[str, object]":
    """Return a package's manuscript_variables.json as a dict (never raises)."""
    vp = _find_variables_json(package_dir)
    if vp is None:
        return {}
    try:
        import json

        return json.loads(vp.read_text())
    except (OSError, ValueError):
        return {}


def _demote_heading(line: str) -> str:
    """Nest a section heading one level under the chapter's ``#`` header."""
    m = re.match(r"^(#{1,6})(?=\s)", line)
    return ("#" + line) if m else line


def _neutralize_crossrefs(body: str) -> str:
    """Neutralise package-local pandoc-crossref labels without flattening prose.

    Structure-preserving sibling of :func:`_strip_crossrefs`: it converts
    section pointers into prose and drops definition/proposition/float pointers,
    but never collapses the markdown line structure (headings, lists, math,
    tables) that a full section carries.
    """

    def _sub(match: "re.Match[str]") -> str:
        kind, name = match.group(1), match.group(2).split(":")[-1]
        if kind == "sec":
            return f"the {name.replace('-', ' ').replace('_', ' ')} section"
        return ""

    body = _CROSSREF.sub(_sub, body)
    body = re.sub(r"\{#[a-z]+:[^{}]*\}", "", body)  # strip fig/tbl/eq crossref label attributes
    body = re.sub(r"\(\s*[,;]?\s*\)", "", body)  # ()
    body = re.sub(r"[ \t]+—\s*\)", ")", body)  # " — )"
    body = re.sub(r"\bSection\s+the\b", "The", body)
    body = re.sub(r"\bsection\s+the\b", "the", body)
    body = re.sub(r"[ \t]+([,.;:])", r"\1", body)
    body = re.sub(r"([,;])[ \t]*\1+", r"\1", body)
    lines = [re.sub(r"[ \t]{2,}", " ", ln) for ln in body.splitlines()]
    return "\n".join(lines).strip()


#: Markdown image embed: ``![caption](src){label}``.
_IMG = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)(\{[^}]*\})?")


def _process_figures(text: str, package_dir: Path, slug: str) -> tuple[str, list[tuple[Path, str]]]:
    """Rewire markdown figure embeds to the compendium's figure store.

    Each embedded image's ``src`` is relative to the package's ``manuscript/``
    directory; it is resolved to an absolute path, copied (by the orchestrator)
    into the compendium's ``output/figures/`` under a slug-namespaced filename,
    and the chapter body is rewritten to point at that copy with its
    ``{#fig:...}`` crossref label dropped (such labels would collide across 33
    packages).  A referenced figure that is missing becomes a prose caption
    instead of a broken image.
    """
    figures: list[tuple[Path, str]] = []

    def _sub(match: "re.Match[str]") -> str:
        caption = match.group(1).strip()
        src = match.group(2).strip()
        abs_src = (package_dir / "manuscript" / src).resolve()
        dest = f"{slug}_{Path(src).name}"
        if abs_src.is_file():
            figures.append((abs_src, dest))
            # `output/figures/...` is the path the template renderer rewrites
            # for LaTeX (see infrastructure/rendering/_pdf_figure_paths.py).
            return f"![{caption}](output/figures/{dest})"
        if caption:
            return f"> **Figure (in the package manuscript):** {caption}."
        return ""

    return _IMG.sub(_sub, text), figures


def import_package_sections(package_dir: Path, slug: str) -> tuple[str, list[tuple[Path, str]]]:
    """Import every authored section (01..NN) of a package's manuscript.

    Sections are read in lexicographic filename order, token-hydrated from the
    package's ``manuscript_variables.json``, demoted one heading level, and
    joined.  Figure embeds are rewired to the compendium's figure store.  An
    unreadable section raises (fail-loud): a chapter that cannot be fully
    imported must never silently truncate.
    """
    manuscript = package_dir / "manuscript"
    files = sorted(f for f in manuscript.glob("[0-9][0-9]_*.md") if _SECTION_RE.match(f.name))
    if not files:
        return "", []
    variables = _package_variables(package_dir)
    parts: list[str] = []
    figures: list[tuple[Path, str]] = []
    for f in files:
        text = f.read_text()  # unreadable -> raises, never swallowed
        text = _resolve_tokens(text, variables)
        if _TOKEN.search(text):
            text = _TOKEN.sub("", text)  # any stragglers
        # Real tokens are resolved above.  The only `{{`/`}}` that can survive
        # are literal token-protocol prose in the package's own manuscript — a
        # reproducibility section naming its own tokens (e.g. ``{{RESULT_*}}``)
        # or the backtick-quoted delimiter ``{{``. Fold exactly those into
        # single braces so the merged compendium never carries a dangling `{{`,
        # WITHOUT touching LaTeX math braces (a blanket ``}}``->``}`` rewrite
        # unbalanced \frac{1}{...}} and broke the combined render).
        text = re.sub(
            r"\{\{[A-Z][A-Z0-9_*]*\}\}",
            lambda m: "{" + m.group(0)[2:-2] + "}",
            text,
        )
        text = text.replace("`{{`", "`{`").replace("`}}`", "`}`")
        text = _neutralize_crossrefs(text)  # inline [@fig:…]/[@tbl:…] pointers
        text, fgs = _process_figures(text, package_dir, slug)
        figures.extend(fgs)
        lines = [_demote_heading(ln) for ln in text.splitlines()]
        parts.append("\n".join(lines).strip())
    return "\n\n".join(parts).strip(), figures


# --------------------------------------------------------------------------- #
# Chapter sections
# --------------------------------------------------------------------------- #


#: Packages whose provider could not be loaded during the last build. A blanket
#: ``except Exception: return ""`` once let die_another_day's chapter lose its
#: mission brief silently: the package had added a scipy dependency the
#: compendium's environment lacked, the import raised ModuleNotFoundError, and
#: the chapter simply rendered one line shorter with nothing reported. Failures
#: are recorded here so a caller can see that content went missing.
BRIEF_FAILURES: "dict[str, str]" = {}


def _brief_line(package_dir: Path, slug: str) -> str:
    """Real mission codename/objectives from the film's MissionProvider.

    Returns "" when the package genuinely has no ``mission.py``. Any other
    failure is recorded in :data:`BRIEF_FAILURES` rather than swallowed, because
    a provider that stops importing is a real integration break, not an absence.
    """
    import sys

    search = package_dir / "src"
    if not (search / slug / "mission.py").is_file():
        return ""
    try:
        from bond_api.discovery import load_provider  # type: ignore[import-not-found]

        sys.path.insert(0, str(search))
        try:
            provider = load_provider(slug, search_paths=[str(search)])
            brief = provider.brief()
        finally:
            sys.path.remove(str(search))
        objs = "; ".join(brief.objectives)
        BRIEF_FAILURES.pop(slug, None)
        return f"Mission **{brief.codename}**: {objs}."
    except Exception as exc:  # noqa: BLE001 — recorded, then reported by the caller
        BRIEF_FAILURES[slug] = f"{type(exc).__name__}: {exc}"
        return ""


def build_package_section(
    pkg: PackageInfo,
    package_dir: Path,
    reference_keys: list[str],
    index: int,
) -> ImportedChapter:
    """One imported chapter carrying the package's FULL manuscript.

    The chapter is no longer an abstract-only excerpt: it reproduces the
    package's complete manuscript — its abstract and every authored section
    (00..NN) — token-hydrated and nested under the chapter header, plus its
    ``## Sources`` citation list.  Figure embeds are rewired to the
    compendium's figure store so the combined PDF carries the package's figures.
    """
    header = f"# {pkg.title} — {pkg.codename}"
    concepts = ", ".join(pkg.concepts) if pkg.concepts else pkg.phenomena
    brief = _brief_line(package_dir, pkg.slug)
    abstract = import_package_abstract(package_dir)
    sections, figures = import_package_sections(package_dir, pkg.slug)
    lines = [
        header,
        "",
        f"*{pkg.kind} package · mission codename {pkg.codename}*." + (f" {brief}" if brief else ""),
        "",
        "This chapter reproduces the package's complete manuscript verbatim:",
        "the abstract and every authored section, token-hydrated from the",
        "package's own manuscript variables, with the package's figures carried",
        "in the combined PDF and its sources resolved against the unified",
        "bibliography.",
        "",
        "## Concepts",
        "",
        concepts,
        "",
        "## Abstract",
        "",
        (abstract or "_This package ships no abstract._"),
        "",
    ]
    if sections:
        lines.append(sections)
        lines.append("")
    if reference_keys:
        cites = "; ".join(f"@{key}" for key in reference_keys)
        lines += ["## Sources", "", cites, ""]
    return ImportedChapter(body="\n".join(lines), figures=tuple(figures))


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


#: LaTeX accent commands -> Unicode combining marks, applied to the following
#: base character. Covers the accents that actually appear in the fleet's
#: bibliographies (Verhulst, Avižienis, Élements, Poincaré, ...).
_LATEX_COMBINING = {
    "`": "\u0300",
    "'": "\u0301",
    "^": "\u0302",
    '"': "\u0308",
    "~": "\u0303",
    "=": "\u0304",
    ".": "\u0307",
    "u": "\u0306",
    "v": "\u030c",
    "H": "\u030b",
    "c": "\u0327",
    "k": "\u0328",
    "r": "\u030a",
    "b": "\u0331",
    "d": "\u0323",
}
#: Standalone LaTeX symbol commands with no argument.
_LATEX_SYMBOLS = {
    r"\ss": "ß",
    r"\o": "ø",
    r"\O": "Ø",
    r"\aa": "å",
    r"\AA": "Å",
    r"\ae": "æ",
    r"\AE": "Æ",
    r"\oe": "œ",
    r"\OE": "Œ",
    r"\l": "ł",
    r"\L": "Ł",
    r"\i": "ı",
    r"\j": "ȷ",
    r"\&": "&",
    r"\%": "%",
    r"\_": "_",
    r"\#": "#",
    r"\$": "$",
}

_ACCENT_BRACED = re.compile(r"\\([`'^\"~=.uvHckrbd])\s*\{(\w)\}")
_ACCENT_BARE = re.compile(r"\\([`'^\"~=.uvHckrbd])\s*(\w)")
_TEXTTT = re.compile(r"\\(?:texttt|textit|textbf|emph|mbox)\s*\{([^{}]*)\}")


def latex_to_text(value: str) -> str:
    """Render a BibTeX field as readable plain text.

    Braces cannot simply be deleted. ``Fran{\\c{c}}ois`` stripped of braces
    becomes ``Fran\\ccois`` — and ``\\cc`` is an undefined control sequence that
    fails the Beamer build for the whole references section. Accent commands are
    therefore resolved to real Unicode first, and only the leftover grouping
    braces (BibTeX capitalisation protection) are removed.
    """
    text = value
    for _ in range(3):  # resolve nesting such as {{\v{z}}}
        text = _ACCENT_BRACED.sub(lambda m: m.group(2) + _LATEX_COMBINING[m.group(1)], text)
        text = _ACCENT_BARE.sub(lambda m: m.group(2) + _LATEX_COMBINING[m.group(1)], text)
        text = _TEXTTT.sub(r"\1", text)
    for cmd, char in sorted(_LATEX_SYMBOLS.items(), key=lambda kv: -len(kv[0])):
        text = text.replace(cmd + "{}", char).replace(cmd + " ", char + " ").replace(cmd, char)
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    text = unicodedata.normalize("NFC", text)
    return " ".join(text.split())


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
        title = latex_to_text(m.group(1)) if m else ""
        am = re.search(r"author\s*=\s*\{(.+?)\}", ref.bibtex, re.S)
        author = latex_to_text(am.group(1)) if am else ""
        lines.append(f"- **{ref.key}** — {author}. *{title}*.")
        lines.append("")
    return "\n".join(lines)

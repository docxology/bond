# Source style guide

Conventions for `src/bond_manuscript/`. Each rule reflects how the existing code
is written; follow the neighbouring code before following a rule in the abstract.

## Read-only core

`compendium.py` reads files and returns strings. It never writes, never creates
directories, and never prints. Writing is `scripts/generate_compendium.py`'s job.

```python
# CORRECT — return the text, let the caller decide where it goes
def build_references_section(references: list[Reference]) -> str:
    ...
    return "\n".join(lines)
```

If a change needs a new output file, add the write in the orchestrator and keep
the builder returning a string. That is what makes the whole generator testable
without a filesystem fixture.

## Lazy suite imports

Sibling packages are imported inside the function that needs them, with an
explanatory comment:

```python
def discover_packages(bond_root: Path) -> list[PackageInfo]:
    from bond_coordinator.registry import ROSTER  # lazy: suite layer 2
```

A module-scope `import bond_coordinator` makes `bond_manuscript` unimportable
whenever a sibling package is mid-edit, which breaks the test suite for reasons
that have nothing to do with the compendium.

## No infrastructure imports

`src/` must not import `infrastructure.*`. The template's rendering and provenance
helpers are reached from `scripts/` only. Verify with:

```bash
grep -rn "^\(from\|import\) infrastructure" src/ || echo "Clean"
```

## Frozen dataclasses for data, module constants for tables

`PackageInfo` and `Reference` are `@dataclass(frozen=True)`. Lookup tables that
never change at runtime are module-level constants in `UPPER_SNAKE`, next to the
code that uses them (`FILM_NUMBER`, `_VARIABLE_PATHS`, `_LATEX_COMBINING`,
`_LATEX_SYMBOLS`).

Regular expressions are compiled once at module scope with a leading underscore
(`_TOKEN`, `_CROSSREF`, `_ACCENT_BRACED`), not inside the function body.

## Type hints and docstrings

Every public function is annotated and carries a short docstring saying what it
returns, not how it works. Use Python 3.10+ union syntax (`Path | None`), and
quote forward-referencing generics that appear in signatures of nested helpers
(`"re.Match[str]"`, `"OrderedDict[str, Reference]"`) as the existing code does.

## Comments explain why, and only where a reader would get it wrong

The comments in `compendium.py` are not narration — each one records a failure
that the code now prevents:

```python
#: Where a package may keep its generated manuscript variables. 31 packages use
#: ``output/data/``; bond-cli and bond-ops write ``output/variables/``. Reading
#: only the majority path made those two abstracts import with every token
#: stripped, so the compendium rendered "**** (**)" instead of the package name.
_VARIABLE_PATHS = ("data", "variables")
```

Write that kind of comment or none. Do not add comments restating the next line.

## Never swallow a failure that costs content

A blanket `except Exception: return ""` once let a chapter lose its mission brief
line silently. The current shape records the failure so a caller can report it:

```python
except Exception as exc:  # noqa: BLE001 — recorded, then reported by the caller
    BRIEF_FAILURES[slug] = f"{type(exc).__name__}: {exc}"
    return ""
```

An empty return is only acceptable for a genuine absence — a package with no
`mission.py`, a package with no `references.bib`. Anything else must leave a trace.

Narrow the caught exception where the failure mode is known, as
`import_package_abstract` does for unparseable variable JSON:

```python
except (OSError, ValueError):
    variables = {}
```

## Determinism

Ordering must come from the roster or from an `OrderedDict`, never from a `set`
or from `Path.glob` order. De-duplication keeps insertion order:

```python
merged: "OrderedDict[str, Reference]" = OrderedDict()
for pkg in packages:
    for ref in parse_references(bond_root / pkg.slug, pkg.slug):
        merged[ref.key] = ref
```

`tests/test_compendium.py::test_regeneration_is_deterministic` regenerates the
manuscript and asserts byte-equality, so a non-deterministic change fails there.

## See also

- [`AGENTS.md`](AGENTS.md) — API reference and invariants
- [`../tests/PATTERNS.md`](../tests/PATTERNS.md) — how to test code written here
- [`../scripts/CONVENTIONS.md`](../scripts/CONVENTIONS.md) — how the orchestrators use it

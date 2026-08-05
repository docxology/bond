# Forking guide

How to reuse this generator to build a compendium over a different package suite,
and what to expect from the fork.

## What is actually transferable

The Bond-specific parts of `compendium.py` are small: the infrastructure package
table, the `bond_coordinator.registry.ROSTER` import, and the chapter numbering
constants. Everything else is generic machinery for the same problem — a suite of
independently-authored package manuscripts that has to render as one document:

| Piece | Transferable? |
| --- | --- |
| `discover_packages()` | Structure yes; the roster source and the infra table are yours to replace |
| `import_package_abstract()` + `_resolve_tokens()` | Directly — it handles both `output/data/` and `output/variables/` conventions and coerces non-string JSON values |
| `parse_references()` + `build_references_bib()` | Directly — both real BibTeX and plain `[n] …` lists, de-duplicated by key |
| `latex_to_text()` | Directly |
| `_strip_crossrefs()` | Directly, once you list your own label prefixes |
| `_brief_line()` + `BRIEF_FAILURES` | Only if your suite has a comparable per-package protocol |
| `build_*_section()` | Rewrite — these encode Bond's chapter shape |

## Steps

1. **Copy `src/`, `scripts/`, and `tests/`.** Rename the package
   (`src/<your_pkg>/`) and update `[project]` and `[tool.setuptools.packages.find]`
   in `pyproject.toml`.

2. **Replace discovery.** `discover_packages()` needs your suite's ordered
   roster. If you have no registry package, read the list from a YAML file in
   this package rather than from directory order — ordering must be stable or
   regeneration stops being byte-identical.

3. **Replace the chapter builders.** `build_package_section()` and
   `build_architecture_section()` are where your suite's shape lives. Keep them
   pure: take data, return a string.

4. **Adjust `manuscript_variables.py`.** Its tokens should be counts and titles
   derived from discovery, never typed into prose.

5. **Point the generator at your patterns.** In
   `scripts/generate_compendium.py`, update `_GENERATED_02`, `_GENERATED_PKG`, and
   `_GENERATED_99` to match exactly what you write. This is the guard that stops
   the generator deleting hand-authored sections; a widened glob deletes your
   introduction.

6. **Rewrite the tests.** Keep the four fleet-wide sweeps — no empty bold, no
   dangling cross-references, every package has a chapter, every provider loads.
   Those are the assertions that catch whole-suite degradation, which is the
   failure class this design is exposed to.

7. **Declare your suite dependencies.** Path dependencies in `[tool.uv.sources]`,
   plus anything a package's provider imports. Sync with `uv sync --all-extras`.

## Keep these properties

- **Import, never duplicate.** The moment a fact has two homes, one of them is
  wrong and nobody notices.
- **Pure core, thin orchestrators.** All writing in `scripts/`.
- **Loud failure.** A build that quietly drops a chapter's content must exit
  non-zero.
- **Byte-stable regeneration**, pinned by a test that runs the generator twice.
- **Documentation that names only what exists.** This is the fork's real risk —
  see below.

## The documentation trap

This package was itself a fork, and its documentation set was not rewritten with
it. Twenty-three files described the source exemplar's modules — an optimizer, an
experiment config, an analysis package, a dashboard, their tests and their
convergence plot — none of which ever existed here. `src/AGENTS.md` was 411 lines
of it. Every test passed, coverage stayed above the gate, and the
lint and drift checkers were clean the whole time, because none of them reads
prose against the tree.

If you fork this package, rewrite the docs in the same commit. The fleet gate
catches the specific case of a backticked `src/…py` path that does not resolve:

```bash
cd projects/working/bond && python3 _phase_docs_gate.py
```

It does not catch a doc that describes a function that no longer behaves that
way. Only reading does.

## Confidentiality

This tree lives under `projects/working/` and is local-only: never tracked in the
public template repository, never pushed. A fork placed anywhere under
`projects/` other than `projects/templates/` inherits the same fence, enforced by
the repository-root `scripts/audit/check_tracked_all.py` in the `lint` job and pre-push
hook.

## See also

- [`architecture.md`](architecture.md) — layers and data flow
- [`../src/AGENTS.md`](../src/AGENTS.md) — the API you would be copying
- [`../tests/PATTERNS.md`](../tests/PATTERNS.md) — the test patterns worth keeping

# AGENTS.md — bond-manuscript (THE COMPENDIUM)

The PROJECT BOND **wrapper manuscript**. `bond-manuscript` is the project the
template renders: a single top-level manuscript that imports one chapter per
package and merges every package's references into one bibliography.

## Hard rules

1. **Work only inside this directory.** Never edit sibling bond packages, bond
   root files, or the template repo.
2. **Published repository.** The public source is
   https://github.com/docxology/bond (default branch `main`); pushing there is
   normal maintenance. This tree is public, so never commit credentials,
   absolute machine paths, or unpublished package content.
3. **Generated sections are never hand-edited.** `02_suite_architecture.md`,
   `03_*`, `04_*`, `99_references.md`, and `references.bib` are owned by
   `scripts/generate_compendium.py` and regenerated — edit the generator or the
   source package manuscript, not the output. Hand-authored boundaries are
   `00_abstract.md`, `01_introduction.md`, `90_closing.md`.
4. **Imported, not duplicated.** Package chapters import each package's own
   manuscript; the same facts must not be hand-authored here.
5. **Unified bibliography.** `references.bib` merges all packages; do not add
   entries by hand — add to the source package's `references.bib` and re-run.
6. **Deterministic.** `generate_compendium.py` is byte-stable; rendering must
   be reproducible.
7. **Quality gates.** `uv run pytest tests/ --cov=src --cov-fail-under=90`
   (43 tests, ≥90%), ruff + mypy clean, no mocks.

## Regenerate + render

```bash
uv run python scripts/generate_compendium.py                  # chapters + bib
uv run python scripts/z_generate_manuscript_variables.py      # hydrate tokens
# from the template root:
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

The renderer hydrates with this package's own `.venv` python; the
`z_generate_manuscript_variables.py` script self-locates the template root
(ancestor holding `infrastructure/rendering/`) so `infrastructure` imports
under any interpreter.

## Layer contract

| Surface | Rule |
| --- | --- |
| `src/bond_manuscript/compendium.py` | Discovery, abstract import, reference merge, section builders — pure; suite deps (bond_api/bond_coordinator) imported lazily |
| `src/bond_manuscript/manuscript_variables.py` | `{{TOKEN}}` map from live discovery |
| `scripts/` | Thin orchestrators (`generate_compendium.py`, `z_generate_manuscript_variables.py`) |
| `docs/manuscript/` | Wrapper sections + unified `references.bib` (generated sections regenerable) |
| `tests/` | Real fleet data, zero mocks, ≥90% coverage |

## Contact / context

- The fleet roster is read at runtime from `bond_coordinator.registry.ROSTER`;
  the suite's own `SCOPE.md` / `ROSTER.md` live in the suite checkout, not in
  this repository.
- Source-of-truth inputs live outside this repository: every sibling package's
  `docs/manuscript/` + `output/data/manuscript_variables.json`, resolved from
  `--bond-root` (default `../..`, the suite root in the monorepo layout).

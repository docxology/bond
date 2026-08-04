# bond-manuscript — the PROJECT BOND compendium

The **top-level wrapper manuscript** for the 33-package BOND suite. This is the
manuscript the template renders: one chapter imported from each package's own
manuscript, framed by an introduction and a closing, with a **unified
bibliography** merged from every package's `references.bib`.

**Codename:** THE COMPENDIUM · **Rendered PDF:** `output/pdf/bond-manuscript_combined.pdf`

## What it is

| Piece | Origin |
| --- | --- |
| `00_abstract.md` · `01_introduction.md` · `90_closing.md` | hand-written wrapper prose (tokens injected) |
| `02_suite_architecture.md` | generated — layered topology + roster + measured gate |
| `03_01_…` … `03_27_…` | **generated film chapters** — one per Bond film, abstract imported from the package manuscript |
| `04_01_…` … `04_06_…` | **generated infrastructure chapters** (utilities, api, coordinator, orchestrator, cli, ops) |
| `99_references.md` · `references.bib` | generated — the **unified bibliography** merged from all 33 packages |

Each package chapter imports that package's abstract (token-hydrated from its
`manuscript_variables.json` when present), its real mission codename/objectives
(its live `MissionProvider`), its concepts, and its references — cited against
the unified `references.bib` (110+ merged entries; both real BibTeX and
plain-numbered lists are handled and de-duplicated by key).

## Regenerate + render

```bash
# 1. Regenerate the compendium (33 chapters + unified bibliography)
uv run python scripts/generate_compendium.py

# 2. Hydrate {{TOKEN}}s into output/manuscript/
uv run python scripts/z_generate_manuscript_variables.py

# 3. Render the wrapper PDF via the template pipeline (from the repo root)
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

`generate_compendium.py` is deterministic: re-running it produces byte-identical
sections and bibliography (test-locked).

## Layout

```
src/bond_manuscript/   compendium.py (discovery, abstract import, bib merge, sections)
                       manuscript_variables.py ({{TOKEN}} map from live discovery)
scripts/               generate_compendium.py · z_generate_manuscript_variables.py
manuscript/            the wrapper manuscript (sections + unified references.bib)
tests/                 18 tests, no mocks, ≥90% coverage on src/
```

Local-only workspace tree under `projects/working/` — never pushed.

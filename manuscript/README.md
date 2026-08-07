# manuscript/ — the PROJECT BOND compendium

The wrapper manuscript for the 33-package BOND suite: three hand-authored
sections framing 35 generated sections (1 architecture chapter, 27 film
chapters, 6 infrastructure chapters, 1 references chapter) and a unified
bibliography.

## Structure

| Section | Origin |
| --- | --- |
| `00_abstract.md` | hand-authored — what the suite is, with injected counts |
| `01_introduction.md` | hand-authored — the two layers, the quality bar, the reader's guide |
| `02_suite_architecture.md` | generated — layer table, roster, measured gate |
| `03_01_…` … `03_27_…` | generated — one chapter per Bond film, in canon order |
| `04_01_…` … `04_06_…` | generated — one chapter per infrastructure package |
| `90_closing.md` | hand-authored — synthesis across the fleet |
| `99_references.md` | generated — the unified bibliography, by source package |

Each generated package chapter carries the package's title and mission codename,
its concepts, its abstract imported from its own manuscript, and its citation
keys against the merged `references.bib`.

Support files: `references.bib` (generated), `config.yaml` (paper metadata),
`preamble.md` (LaTeX), `config.yaml.example`, `layer_contract.yaml`.

## Build

```bash
cd projects/working/bond/bond-manuscript
uv run python scripts/generate_compendium.py                # chapters + unified bib
uv run python scripts/z_generate_manuscript_variables.py    # tokens -> output/manuscript/

# from the template repository root
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

Output: `output/pdf/bond-manuscript_combined.pdf`, per-section HTML under
`output/web/`, per-section Beamer decks under `output/slides/`.

## Before you edit

The 35 generated sections and `references.bib` are rewritten on every build. A
correction to a film belongs in that film's package, not here.
[`AGENTS.md`](AGENTS.md) has the full table of what is editable and where each
kind of fix belongs; [`SYNTAX.md`](SYNTAX.md) covers tokens, citations, and the
cross-reference constraint.

## See also

- [`../README.md`](../README.md) — what the compendium is
- [`../docs/rendering_pipeline.md`](../docs/rendering_pipeline.md) — the three build steps
- [repository manuscript semantics](../../../../../docs/guides/manuscript-semantics.md) — repository-wide semantics

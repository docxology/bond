---
title: "Manuscript directory: bond-manuscript"
type: "manuscript_guide"
---

# manuscript/ — the compendium

38 section files plus support files. Six of the sections are hand-authored; the
other 32 are build output.

Project-wide rules are in [`../docs/agent_instructions.md`](../docs/agent_instructions.md).
This file covers the manuscript directory specifically.

## What is hand-authored, and what is not

| File | Origin | Editable |
| --- | --- | --- |
| `00_abstract.md` | hand-authored; uses `{{N_PACKAGES}}`, `{{N_FILMS}}`, `{{N_INFRA}}` | yes |
| `01_introduction.md` | hand-authored | yes |
| `02_suite_architecture.md` | generated — layer table, roster, measured gate | **no** |
| `03_01_…` … `03_27_…` | generated — one chapter per film, canon order | **no** |
| `04_01_…` … `04_06_…` | generated — one chapter per infrastructure package | **no** |
| `90_closing.md` | hand-authored; uses `{{N_PACKAGES}}`, `{{N_FILMS}}`, `{{N_INFRA}}`, `{{N_GATE_MEASURED}}` | yes |
| `99_references.md` | generated — bibliography listing by source package | **no** |
| `references.bib` | generated — unified merge from all 33 packages | **no** |
| `preamble.md` | LaTeX packages injected at compile time | yes |
| `config.yaml` | paper metadata (title, authors, keywords, license) | yes |
| `config.yaml.example` | reference copy of the config shape | yes |
| `layer_contract.yaml` | declares which files may import `infrastructure.*` | yes |
| `SYNTAX.md`, `README.md`, `AGENTS.md` | documentation; never read by the renderer | yes |

`scripts/generate_compendium.py` deletes and rewrites the generated files by
explicit filename pattern (`02_suite_architecture.md`, `^(0[34])_\d{2}_.+\.md$`,
`99_references.md`) on every run. An edit to any of them survives until the next
build and is then gone.

## Where a fix belongs

| You want to change | Edit |
| --- | --- |
| A film's abstract text | that package's `manuscript/00_abstract.md` |
| A film's codename or objectives | that package's `src/<slug>/mission.py` |
| A citation in a chapter | that package's `manuscript/references.bib` |
| The shape of every chapter | `build_package_section()` in `src/bond_manuscript/compendium.py` |
| The architecture chapter | `build_architecture_section()` |
| The wrapper's own framing | `00_abstract.md`, `01_introduction.md`, `90_closing.md` |

## Token protocol

Six tokens exist, all from
`src/bond_manuscript/manuscript_variables.py::generate_variables()`:
`SUITE_TITLE`, `SUITE_TITLE_SHORT`, `N_PACKAGES`, `N_FILMS`, `N_INFRA`,
`N_GATE_MEASURED`. Every one is derived from live discovery, so a count in the
prose cannot drift from the fleet.

The pipeline:

1. `scripts/z_generate_manuscript_variables.py` calls `generate_variables()`.
2. It passes the map to
   `infrastructure.rendering.manuscript_injection.write_resolved_manuscript_tree`.
3. That copies `manuscript/` to `output/manuscript/` with every `{{TOKEN}}`
   substituted.
4. The renderer reads `output/manuscript/`, never this directory directly.

Adding a token: add the key in `generate_variables()`, assert it in
`tests/test_compendium.py`, re-run hydration, then reference it. Check before
rendering:

```bash
grep -r "{{" output/manuscript/ && echo "UNRESOLVED" || echo "All tokens resolved"
```

Generated chapters carry no tokens — a package's abstract is imported with its
own tokens already resolved from that package's `manuscript_variables.json`.

## Section ordering

Files are assembled in lexicographic filename order. That is the entire ordering
mechanism, which is why `FILM_NUMBER = "03"` and `INFRA_NUMBER = "04"` exist in
`compendium.py`. Never renumber a chapter by hand.

## No figures

No section embeds an image, and `output/` has no `figures/` directory. The
architecture chapter is tables only. If you add a diagram, note that a
```mermaid``` block in a rendered section makes the combined PDF depend on `mmdc`
and a pinned `chrome-headless-shell` — see
[`../docs/troubleshooting.md`](../docs/troubleshooting.md).

## Workflow

```bash
cd projects/working/bond/bond-manuscript

uv run python scripts/generate_compendium.py                # chapters + unified bib
uv run python scripts/z_generate_manuscript_variables.py    # tokens -> output/manuscript/
grep -r "{{" output/manuscript/ || echo "All tokens resolved"

# from the template repository root
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

A non-zero exit from step 1 means a film's `MissionProvider` failed to import and
its chapter lost the mission brief line. Fix it before rendering.

## See also

- [`README.md`](README.md) — orientation
- [`SYNTAX.md`](SYNTAX.md) — citation, token, and cross-reference syntax
- [`../docs/rendering_pipeline.md`](../docs/rendering_pipeline.md) — the three build steps
- [`../src/AGENTS.md`](../src/AGENTS.md) — the builders behind the generated sections

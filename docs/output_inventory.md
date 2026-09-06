# Output inventory

Every artifact this package produces, and what produced it. Paths are relative to
`projects/working/bond/bond-docs/manuscript/`.

## Generated inside `docs/manuscript/`

Tracked, because they are the manuscript — but never hand-edited.

| Path | Content | Produced by |
| --- | --- | --- |
| `docs/manuscript/references.bib` | Unified bibliography merged from all 33 packages, de-duplicated by case-insensitive canonical key and escaped for safe LaTeX output | `build_references_bib()` via `scripts/generate_compendium.py` |
| `docs/manuscript/02_suite_architecture.md` | Layer table, roster table, measured-gate table | `build_architecture_section()` |
| `docs/manuscript/03_01_…` … `03_27_…` | One chapter per film: header, concepts, imported abstract, sources | `build_package_section()` |
| `docs/manuscript/04_01_…` … `04_06_…` | One chapter per infrastructure package | `build_package_section()` |
| `docs/manuscript/99_references.md` | Bibliography listing grouped by source package | `build_references_section()` |

## Generated inside `output/`

Untracked and disposable.

| Path | Content | Produced by |
| --- | --- | --- |
| `output/manuscript/*.md` | Token-resolved copies of every manuscript section — the renderer's actual input | `scripts/z_generate_manuscript_variables.py` via `infrastructure.rendering.manuscript_injection.write_resolved_manuscript_tree` |
| `output/manuscript/{config.yaml,preamble.md,references.bib}` | Support files copied alongside the resolved sections | same |
| `output/pdf/bond-manuscript_combined.pdf` | The compendium | template render stage |
| `output/pdf/_combined_manuscript.{md,tex,aux,toc,bbl,blg,log}` | Pandoc and LaTeX intermediates | Pandoc + XeLaTeX |
| `output/pdf/_latex_stdout.log` | Full XeLaTeX transcript | XeLaTeX |
| `output/web/index.html`, `output/web/manuscript__*.html` | One HTML page per section, plus an index | template render stage |
| `output/slides/*_slides.pdf` | One Beamer deck per section | template render stage |
| `output/slides/*_slides.{tex,aux,log,nav,snm,toc,vrb}` | Beamer intermediates | XeLaTeX |
| `output/reports/manuscript_composition.json` | Ordered input list, per-input and combined content hashes | template render stage |
| `output/provenance/dag.json` | Provenance record for the run | template render stage |

## Inputs this package reads but does not own

| Path | Read by |
| --- | --- |
| `../<package>/manuscript/00_abstract.md` | `import_package_abstract()` |
| `../<package>/output/manuscript/00_abstract.md` | `import_package_abstract()` — preferred when present |
| `../<package>/output/{data,variables}/manuscript_variables.json` | `import_package_abstract()` for token resolution |
| `../<package>/docs/manuscript/references.bib` | `parse_references()` |
| `../<package>/src/<slug>/mission.py` | `_brief_line()` via `bond_api.discovery.load_provider` |
| `../output/aggregate/gate_manifest.json` | `build_architecture_section()`, `generate_variables()` |

## Regenerating

```bash
cd projects/working/bond/bond-manuscript
uv run python scripts/generate_compendium.py
uv run python scripts/z_generate_manuscript_variables.py
# from the template repository root:
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

## Adding an artifact

Build it in `src/bond_manuscript/`, write it from
`scripts/generate_compendium.py`, add its filename to the generator's
`_GENERATED_*` patterns, and add a row above. Then run the generator twice and
confirm the second run changes nothing.

## See also

- [`output_conventions.md`](output_conventions.md) — layout and regeneration policy
- [`rendering_pipeline.md`](rendering_pipeline.md) — the three build steps
- [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) — which sections are generated

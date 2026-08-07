# Rendering pipeline

Three steps take the fleet's 33 package manuscripts to a single compendium PDF.
Each must finish before the next begins.

```
generate_compendium.py  →  z_generate_manuscript_variables.py  →  stage_03_render.py
   manuscript/*.md              output/manuscript/*.md              output/{pdf,web,slides}
```

## 1. Build the compendium

```bash
cd projects/working/bond/bond-manuscript
uv run python scripts/generate_compendium.py [--bond-root ..]
```

**Reads**, for every package under the bond root: `manuscript/00_abstract.md` (or
the hydrated `output/manuscript/00_abstract.md` when present),
`output/data/manuscript_variables.json` or `output/variables/manuscript_variables.json`,
`manuscript/references.bib`, `src/<slug>/mission.py`. Also the fleet's
`output/aggregate/gate_manifest.json` when it exists.

**Writes**, into `manuscript/`:

| File | Content |
| --- | --- |
| `references.bib` | Unified bibliography, de-duplicated by case-insensitive canonical key. Real `@entry` blocks are normalized for citation-safe keys and TeX-special characters; plain `[n] …` lists become deterministic `@misc` entries keyed `<slug>_ref<n>` |
| `02_suite_architecture.md` | Layer table, roster table, and a measured-coverage table when the gate manifest is present |
| `03_01_…` … `03_27_…` | One chapter per film, in canon roster order |
| `04_01_…` … `04_06_…` | One chapter per infrastructure package |
| `99_references.md` | The bibliography listing, grouped by source package |

**Leaves alone** the hand-authored `00_abstract.md`, `01_introduction.md`,
`90_closing.md`, and every support file. Deletion is by explicit filename pattern,
never by glob.

**Exit 1** when any film's `MissionProvider` failed to import. Those chapters lost
their `Mission **CODENAME**: …` line. Fix the dependency and re-run; do not
proceed with the shorter build.

## 2. Hydrate tokens

```bash
uv run python scripts/z_generate_manuscript_variables.py
```

Computes the token map from live discovery via
`bond_manuscript.manuscript_variables.generate_variables()` and calls
`infrastructure.rendering.manuscript_injection.write_resolved_manuscript_tree`,
which copies `manuscript/` to `output/manuscript/` with every `{{TOKEN}}`
substituted. The tokens are `SUITE_TITLE`, `SUITE_TITLE_SHORT`, `N_FILMS`,
`N_INFRA`, `N_PACKAGES`, `N_GATE_MEASURED`.

The renderer may invoke this with this package's own `.venv` interpreter, which
has no `infrastructure` on its path. The script therefore walks up from its own
location to the ancestor holding `infrastructure/rendering/` and puts that on
`sys.path`. If the import still fails it prints the token map and returns 2.

Every `{{TOKEN}}` must resolve before rendering, or the literal text appears in
the PDF:

```bash
grep -r "{{" output/manuscript/ && echo "UNRESOLVED" || echo "All tokens resolved"
```

## 3. Render

From the **template repository root**:

```bash
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

**Reads** `output/manuscript/*.md` (the resolved copies), `manuscript/config.yaml`,
`manuscript/preamble.md`, and the unified `references.bib`.

**Writes** under `output/`:

| Path | Content |
| --- | --- |
| `pdf/bond-manuscript_combined.pdf` | The compendium |
| `pdf/_combined_manuscript.{md,tex,aux,toc,bbl,blg,log}` | Pandoc and LaTeX intermediates |
| `pdf/_latex_stdout.log` | Full XeLaTeX transcript — read this first on a failed build |
| `web/index.html`, `web/manuscript__*.html` | One page per section plus an index |
| `slides/*_slides.pdf` | One Beamer deck per section, with its own LaTeX intermediates |
| `reports/manuscript_composition.json` | Ordered input list and content hashes for the combined build |
| `provenance/dag.json` | Provenance record for the run |

Section order is lexicographic by filename, which is why the chapter numbering
matters: `00_abstract`, `01_introduction`, `02_suite_architecture`, `03_*` films,
`04_*` infrastructure, `90_closing`, `99_references`.

## config.yaml

`manuscript/config.yaml` carries paper metadata only — title, subtitle, version,
date, authors, keywords, license, language. There is no `experiment:` block: the
compendium runs no experiment. `publication.doi` is empty because this is a
local-only manuscript with no minted DOI.

## Failures

The failure modes that actually occur here — a provider that stopped importing,
an abstract whose tokens resolved to nothing, a BibTeX accent that kills the
Beamer run, `mmdc` missing Chrome — are in
[`troubleshooting.md`](troubleshooting.md).

## See also

- [`../scripts/AGENTS.md`](../scripts/AGENTS.md) — what each orchestrator writes
- [`output_inventory.md`](output_inventory.md) — per-artifact producer table
- [`syntax_guide.md`](syntax_guide.md) — tokens and cross-reference rules

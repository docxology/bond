# Output conventions

`output/` is disposable and fully regeneratable. Nothing in it is hand-edited;
`.gitignore` excludes the whole tree.

## Layout

```
output/
    docs/manuscript/   token-resolved copies of docs/manuscript/ — the renderer's input
    pdf/          bond-manuscript_combined.pdf + Pandoc/LaTeX intermediates
    web/          index.html + one HTML page per section
    slides/       one Beamer PDF per section + its LaTeX intermediates
    reports/      manuscript_composition.json (ordered inputs, content hashes)
    provenance/   dag.json (provenance record for the run)
```

There is no `data/` — the compendium runs no experiment; its numbers are counts
derived from live discovery. `figures/` exists as a build-time staging area:
`scripts/generate_compendium.py` copies every embedded package figure into
`output/figures/` (slug-namespaced) and the renderer rewrites those paths for
LaTeX. It is gitignored along with the rest of `output/`.

## Two kinds of generated file

The distinction that matters here is not source-versus-output — it is
**generated inside `docs/manuscript/`** versus **generated inside `output/`**.

| | Location | Written by | Tracked |
| --- | --- | --- | --- |
| Generated manuscript sections | `docs/manuscript/02_suite_architecture.md`, `03_*`, `04_*`, `99_references.md`, `references.bib` | `scripts/generate_compendium.py` | yes — they are the manuscript |
| Hand-authored sections | `docs/manuscript/00_abstract.md`, `01_introduction.md`, `90_closing.md` | a human | yes |
| Render artifacts | everything under `output/` | hydration + the template render stage | no |

Editing a generated manuscript section is a no-op that survives until the next
build. Editing anything in `output/` is a no-op that survives until the next
render.

## Sources of truth

Everything under `output/` derives from exactly four inputs:

1. The 33 sibling package manuscripts, variables, bibliographies, and providers
2. `bond_coordinator.registry.ROSTER` — canon film order and metadata
3. `docs/manuscript/` — the hand-authored boundaries plus the generated sections
4. `docs/manuscript/config.yaml` — paper metadata

## Regenerating

```bash
cd projects/working/bond/bond-manuscript

rm -rf output/                                              # optional clean slate
uv run python scripts/generate_compendium.py                # manuscript sections + bib
uv run python scripts/z_generate_manuscript_variables.py    # output/manuscript/

# from the template repository root
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

Step 1 is byte-stable: an unchanged package tree produces identical bytes, which
`tests/test_compendium.py::test_regeneration_is_deterministic` enforces.

## Adding an output artifact

1. Build it in `src/bond_manuscript/` as a function returning a string, covered
   by a test.
2. Write it from `scripts/generate_compendium.py`, and add its filename to the
   `_GENERATED_*` patterns so the next run replaces rather than duplicates it.
3. Add a row to [`output_inventory.md`](output_inventory.md).
4. Run the generator twice and confirm the output is unchanged the second time.

## See also

- [`output_inventory.md`](output_inventory.md) — the artifact table
- [`rendering_pipeline.md`](rendering_pipeline.md) — what each step writes
- [`troubleshooting.md`](troubleshooting.md) — missing or stale artifacts

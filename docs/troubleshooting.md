# Troubleshooting

Symptom-driven fixes for the failures this package actually produces.

## `generate_compendium.py` exits 1 with "could not load MissionProvider"

```
ERROR: could not load MissionProvider for:
  die_another_day: ModuleNotFoundError: No module named 'scipy'
These chapters lost their mission brief line.
```

**Cause.** The compendium loads every film's provider to build its chapter brief
line. A package whose provider imports a dependency this environment lacks fails
to load, and that chapter renders without its `Mission **CODENAME**: …` line.

**Fix.** Add the dependency to this package's `pyproject.toml` and re-sync:

```bash
cd projects/working/bond/bond-manuscript
uv sync --all-extras
uv run python scripts/generate_compendium.py
```

`scipy` is already declared for exactly this reason. Do not ship the shorter
build — the non-zero exit is deliberate. `test_every_film_chapter_has_a_mission_brief_line`
fails if you do.

## A chapter shows `**** (**)` instead of the package name

**Cause.** The package's abstract was imported with its `{{TOKEN}}`s stripped
rather than resolved, so the bold spans came out empty.

**Fix.** Check where that package writes its variables. Most write
`output/data/manuscript_variables.json`; `bond-cli` and `bond-ops` write
`output/variables/`. `_VARIABLE_PATHS` in `compendium.py` covers both — a third
convention would need adding there. Then confirm the file parses:

```bash
python3 -c "import json,sys; json.load(open(sys.argv[1]))" \
  ../bond-ops/output/variables/manuscript_variables.json
```

An unparseable file falls back to stripping tokens, by design, so a corrupt JSON
looks identical to a missing one from the chapter's point of view.
`test_no_empty_bold_in_any_imported_abstract` catches this across the whole fleet.

## `Section sec. ??` or `[?]` in the rendered PDF

**Cause.** A package-local pandoc-crossref label survived into the wrapper. Those
labels resolve inside their own package's manuscript and do not exist here.

**Fix.** `_strip_crossrefs()` handles `sec`, `def`, `prop`, `thm`, `lem`, `cor`,
`fig`, `eq`, `tbl`, and `lst`. If a package introduced a new prefix, add it to
`_CROSSREF` in `compendium.py`. Verify with:

```bash
uv run pytest tests/ -k crossref -v
```

## The LaTeX build dies in the references section

**Symptom.** XeLaTeX reports an undefined control sequence such as `\cc`,
somewhere in the bibliography.

**Cause.** A BibTeX field with an accent command (`Fran{\c{c}}ois`) had its braces
removed without the accent being resolved first.

**Fix.** `latex_to_text()` resolves accents to Unicode before stripping braces.
If a macro it does not know reaches a field, add it to `_LATEX_COMBINING` or
`_LATEX_SYMBOLS`. Find the failing line:

```bash
grep -nE "Undefined control sequence|^! " output/pdf/_latex_stdout.log | head
```

## Tokens render literally as `{{N_PACKAGES}}` in the PDF

**Cause.** Hydration did not run, or ran after the render.

**Fix.**

```bash
uv run python scripts/z_generate_manuscript_variables.py
grep -r "{{" output/manuscript/ && echo "STILL UNRESOLVED" || echo "All tokens resolved"
```

If a token is still literal, it is not in `generate_variables()` — add it there,
not to the manuscript.

## `z_generate_manuscript_variables.py` returns 2

**Symptom.** It prints the token map and exits 2 instead of writing
`output/manuscript/`.

**Cause.** `infrastructure` could not be imported. The script walks up from its
own location looking for an ancestor holding `infrastructure/rendering/`; if this
package has been moved outside the template repository, there is none.

**Fix.** Run it from inside the template checkout, or from the repository root
with the monorepo interpreter.

## `uv` fails to initialise its cache

```
error: Failed to initialize cache at `/Users/…/.cache/uv`
  Caused by: … Operation not permitted (os error 1)
```

**Cause.** The command is running in a sandbox that cannot write the `uv` cache.

**Fix.** Re-run the same command with the sandbox disabled. This is an
environment restriction, not a project defect.

## pytest reports success but collected 0 tests

**Cause.** `pytest` resolved to an interpreter without this package's
dependencies. A bare `uv sync` prunes the `dev` group, so `uv run pytest` then
picks a different environment, collects nothing, and exits 0.

**Fix.**

```bash
cd projects/working/bond/bond-manuscript
uv sync --all-extras
uv run pytest tests/ --cov=src --cov-fail-under=90
```

Confirm the header shows Python 3.14.6 with the `cov` plugin and a non-zero
collected count. **A green exit with zero collected tests is not a pass.**

## Two tests silently skip

`test_script_smoke_regen` and `test_regeneration_is_deterministic` are skipped
when `../output/aggregate/gate_manifest.json` is absent. When they skip, nothing
is exercising the generator CLI or byte-stable regeneration. Regenerate the
fleet's aggregate gate, or run the generator manually and diff.

## `ModuleNotFoundError` from a script in `scripts/`

Four scripts (`04_benchmark_stage.py`, `build_dashboard.py`,
`generate_api_docs.py`, `optimization_analysis.py`) came from the source exemplar
and import modules this package never had. Four more (`00_preflight.py`,
`08_connector_search.py`, `09_provenance_record.py`, `10_research_workflow.py`)
compute the template root by fixed directory depth and land on `projects/` from
this package's deeper path. None of the eight participates in the compendium
build — see [`../scripts/README.md`](../scripts/README.md). The two that matter
are `generate_compendium.py` and `z_generate_manuscript_variables.py`.

## `mmdc` cannot find Chrome during the combined PDF

**Symptom.** Per-section slides render, the combined PDF fails with
`Could not find Chrome (ver. …)`.

**Cause.** A rendered section embeds a ```mermaid``` block; the combined-PDF
render shells out to `mmdc`, which needs a pinned `chrome-headless-shell` in the
Puppeteer cache. Slides do not invoke `mmdc`, which is why the asymmetry is the
tell. No section of this manuscript currently embeds one — this bites the first
time somebody adds a diagram.

**Fix (one-time per machine).**

```bash
npx --yes puppeteer browsers install chrome-headless-shell
```

## See also

- [`rendering_pipeline.md`](rendering_pipeline.md) — the three build steps
- [`testing_philosophy.md`](testing_philosophy.md) — running the gate honestly
- [`output_conventions.md`](output_conventions.md) — regeneration
- [`faq.md`](faq.md) — questions rather than symptoms

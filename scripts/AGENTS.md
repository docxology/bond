# scripts/ — orchestrator contract

Scripts coordinate; they do not compute. Every fact about the fleet comes from
`src/bond_manuscript/`, every write happens here.

## `generate_compendium.py`

The compendium build. Run from this directory:

```bash
uv run python scripts/generate_compendium.py [--bond-root ..]
```

**Inputs.** The 33 sibling package trees under the bond root — each package's
`manuscript/00_abstract.md` (or its hydrated `output/manuscript/00_abstract.md`),
`manuscript/references.bib`, `src/<slug>/mission.py`, and the fleet's
`output/aggregate/gate_manifest.json` when present.

**Writes**, all under `manuscript/`:

| Path | Content |
| --- | --- |
| `references.bib` | The unified bibliography, merged and de-duplicated by key |
| `02_suite_architecture.md` | Layer table, roster table, measured-gate table |
| `03_01_…` … `03_27_…` | One chapter per film, numbered in canon order |
| `04_01_…` … `04_06_…` | One chapter per infrastructure package |
| `99_references.md` | The bibliography listing, grouped by source package |

**Protects.** `_rm_owned()` deletes only files matching the three generated
patterns before rewriting them. Hand-authored sections (`00_abstract.md`,
`01_introduction.md`, `90_closing.md`) and support files (`preamble.md`,
`config.yaml*`, `SYNTAX.md`, `AGENTS.md`, `README.md`, `layer_contract.yaml`) are
never touched. If you add a generated section, extend those patterns — do not
widen the glob.

**Exit codes.** `0` on success. `1` when `bond_manuscript.compendium.BRIEF_FAILURES`
is non-empty: one or more film providers could not be imported, so their chapters
lost the mission brief line. The failing slugs and exception text go to stderr.
This used to be silent; it is deliberately loud now.

**Import path.** The script prepends its own `src/` plus `bond-api/src`,
`bond-utilities/src`, and `bond-coordinator/src` to `sys.path`, so it runs from a
bare interpreter as well as from the configured environment.

## `z_generate_manuscript_variables.py`

```bash
uv run python scripts/z_generate_manuscript_variables.py
```

Calls `bond_manuscript.manuscript_variables.generate_variables(bond_root=…)` and
passes the result to `infrastructure.rendering.manuscript_injection.write_resolved_manuscript_tree`,
which copies `manuscript/*.md` to `output/manuscript/*.md` with every `{{TOKEN}}`
substituted. The renderer reads the resolved copies, never the originals.

The script walks up from its own location to find the ancestor holding
`infrastructure/rendering/` and puts that on `sys.path`, so it works even when the
renderer invokes it with this package's own `.venv` interpreter. If
`infrastructure` still cannot be imported it prints the token map and returns `2`.

The `z_` prefix is an ordering hint: alphabetically last, because it consumes what
every other stage produced.

## Inherited template stages

`00_preflight.py`, `08_connector_search.py`, `09_provenance_record.py`, and
`10_research_workflow.py` came with the project scaffold. Each computes the
template root as `Path(__file__).resolve().parents[4]`, which resolves to
`projects/` from this package's path rather than the repository root, so
`import infrastructure` raises `ModuleNotFoundError`. None of them participates in
the compendium build. Fix the depth calculation before wiring any of them in.

## Non-functional leftovers

`04_benchmark_stage.py`, `build_dashboard.py`, `generate_api_docs.py`, and
`optimization_analysis.py` are unmodified orchestrators from the source exemplar.
They import, respectively, a `benchmark_support` module, a `dashboard` module, a
`documentation` module, and an `analysis` package — none of which this fork has
ever had. Each fails at import. They are dead weight, not a contract.

## Rules for a new script

1. No fleet logic here. Discovery, parsing, and section building belong in
   `src/bond_manuscript/compendium.py` where they are covered by tests.
2. Own your output patterns explicitly. A generator that deletes by glob will
   eventually delete a hand-authored file.
3. Fail loudly. A build that quietly drops content is worse than one that stops.
4. Resolve paths from `Path(__file__).resolve()`, never from the caller's cwd,
   and never by a fixed `parents[N]` reach into the monorepo — the four inherited
   stages above are what that costs.

## See also

- [`README.md`](README.md) — script inventory at a glance
- [`CONVENTIONS.md`](CONVENTIONS.md) — import, logging, and path conventions
- [`../src/AGENTS.md`](../src/AGENTS.md) — the API these scripts call
- [`../docs/rendering_pipeline.md`](../docs/rendering_pipeline.md) — generate → hydrate → render

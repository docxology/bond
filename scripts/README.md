# scripts/ — thin orchestrators

Two scripts build the compendium. The rest are template pipeline stages inherited
with the project scaffold; see the status column before running any of them.

## The two that matter

```bash
cd projects/working/bond/bond-manuscript

# 1. Regenerate the 33 package chapters, the architecture chapter,
#    the references chapter, and the unified references.bib
uv run python scripts/generate_compendium.py

# 2. Hydrate {{TOKEN}}s into output/manuscript/ for the renderer
uv run python scripts/z_generate_manuscript_variables.py
```

`generate_compendium.py` exits non-zero if any film's `MissionProvider` failed to
import — those chapters lose their mission brief line, and a compendium missing
content it should carry is not a successful build.

## Inventory

| Script | Status | Role |
| --- | --- | --- |
| `generate_compendium.py` | **Active** | Writes the generated manuscript sections and the unified bibliography |
| `z_generate_manuscript_variables.py` | **Active** | Computes the token map and writes the resolved tree to `output/manuscript/` |
| `00_preflight.py` | Inherited stage | Manuscript pre-render check via `infrastructure.rendering.preflight` |
| `08_connector_search.py` | Inherited stage | Opt-in connector search; no-ops without `connector_search.yaml` |
| `09_provenance_record.py` | Inherited stage | Opt-in provenance DAG record |
| `10_research_workflow.py` | Inherited stage | Opt-in research-workflow dispatch |
| `04_benchmark_stage.py` | Non-functional | Imports a `benchmark_support` module this package does not have |
| `build_dashboard.py` | Non-functional | Imports a `dashboard` module this package does not have |
| `generate_api_docs.py` | Non-functional | Imports a `documentation` module this package does not have |
| `optimization_analysis.py` | Non-functional | Imports an `analysis` package this package does not have |

The four **inherited stages** resolve the template root by fixed directory depth
(`Path(__file__).resolve().parents[4]`). That was correct at `projects/<lifecycle>/<project>/`;
this package sits one level deeper, so the computed root is `projects/` and
`import infrastructure` fails. They are not part of the compendium build.

The four **non-functional** scripts came from the source exemplar and reference
modules this fork never had. Running one fails immediately with
`ModuleNotFoundError`. Nothing depends on them.

## Rendering

Rendering is driven from the template repository root, not from here:

```bash
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

## More

[`AGENTS.md`](AGENTS.md) documents what each active script writes and what it
protects. [`CONVENTIONS.md`](CONVENTIONS.md) covers how to write a new one.

# scripts/ — thin orchestrators

Scripts set paths and delegate into `src/bond_manuscript/` or the vendored
template infrastructure under `_template_resources/`; they do not compute.
Testable logic lives in `src/bond_manuscript/` and is covered by `tests/`.

## The two that matter

```bash
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

| Script | Purpose | Delegates to | Command |
| --- | --- | --- | --- |
| `generate_compendium.py` | Writes the generated manuscript sections and the unified bibliography | `bond_manuscript.compendium` | `uv run python scripts/generate_compendium.py` |
| `z_generate_manuscript_variables.py` | Computes the token map and writes the resolved tree to `output/manuscript/` | `bond_manuscript.manuscript_variables`, `infrastructure.rendering.manuscript_injection` | `uv run python scripts/z_generate_manuscript_variables.py` |
| `00_preflight.py` | Pre-render check: embedded mermaid blocks need a pinned chrome-headless-shell | `infrastructure.rendering.preflight` | `uv run python scripts/00_preflight.py` |
| `08_connector_search.py` | Connector search; skips unless `connector_search.yaml` is present | `infrastructure.search.connectors` | `uv run python scripts/08_connector_search.py` |
| `09_provenance_record.py` | Records a provenance DAG node for the pipeline run to `output/provenance/` | `infrastructure.provenance` | `uv run python scripts/09_provenance_record.py` |
| `10_research_workflow.py` | Dispatches the 7-stage research workflow (log-only stages) | `infrastructure.research.config` | `uv run python scripts/10_research_workflow.py` |

## Template infrastructure imports

The four stage scripts import `infrastructure.*` from the vendored mirror at
`_template_resources/infrastructure/`, resolved from `Path(__file__)` — no
fixed-depth reach into a monorepo. If the mirror or its dependencies are
missing, each script prints the failing import to stderr and exits `2` instead
of dying with a bare traceback. `z_generate_manuscript_variables.py` walks up to
the nearest ancestor holding `infrastructure/rendering/` and, when none exists,
prints the token map and returns `2`.

## Rendering

Rendering is driven from the template repository root, not from here:

```bash
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

## More

[`AGENTS.md`](AGENTS.md) documents what each script writes and what it
protects. [`CONVENTIONS.md`](CONVENTIONS.md) covers how to write a new one.

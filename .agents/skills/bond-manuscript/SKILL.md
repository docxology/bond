---
name: bond-manuscript
description: PROJECT BOND compendium generator — discovers the 33-package fleet, imports one chapter per package, merges every package's bibliography into one, and renders the wrapper manuscript.
version: 0.2.0
author: docxology
license: MIT
tags: [compendium, manuscript, generator, thin-orchestrator]
---

# bond-manuscript

Project-scoped skill for `projects/working/bond/bond-manuscript/`, the wrapper
manuscript for the PROJECT BOND suite. Load this when working inside the package.

## What it does

Discovers 27 film packages from `bond_coordinator.registry.ROSTER` plus 6
infrastructure packages, imports each package's abstract (resolving that
package's `{{TOKEN}}`s), reads each film's live `MissionProvider` for its mission
brief, merges every package's `references.bib` into one bibliography, and writes
the architecture chapter, 33 package chapters, and the references chapter.

The implementation is two modules: `src/bond_manuscript/compendium.py` and
`src/bond_manuscript/manuscript_variables.py`.

## When to use

- Regenerating the compendium after a package's manuscript, bibliography, or
  mission provider changed.
- Changing how chapters, the architecture section, or the merged bibliography are
  assembled.
- Diagnosing a chapter that lost content — a stripped abstract, a missing mission
  brief line, an unresolved cross-reference.

## Quick reference

```bash
cd projects/working/bond/bond-manuscript

uv sync --all-extras
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_compendium.py                # exit 1 = a provider failed to load
uv run python scripts/z_generate_manuscript_variables.py

# from the template repository root
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

## Pitfalls

- **Generated sections are build output.** `02_suite_architecture.md`, `03_*`,
  `04_*`, `99_references.md`, and `references.bib` are rewritten every run. Fix
  the source package or the builder, never the output.
- **Import, never duplicate.** A film's facts live in that film's package.
- **Keep `src/` pure.** No writes, no `infrastructure.*` imports, suite packages
  imported lazily inside the functions that need them.
- **Never swallow a content failure.** A provider that stops importing must be
  recorded and reported; the build exits non-zero.
- **Determinism is tested.** Roster order and `OrderedDict`, no timestamps.
- **`uv sync --all-extras`.** A bare `uv sync` prunes pytest and the suite then
  collects zero tests while exiting 0.
- **Most of `scripts/` is dead scaffold.** Only `generate_compendium.py` and
  `z_generate_manuscript_variables.py` are part of the build.

## Cross-refs

- Project contract: [`AGENTS.md`](../../../AGENTS.md)
- README: [`README.md`](../../../README.md)
- TODO: [`TODO.md`](../../../TODO.md)
- Generator API: [`src/AGENTS.md`](../../../src/AGENTS.md)
- Docs index: [`docs/AGENTS.md`](../../../docs/AGENTS.md)

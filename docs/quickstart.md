# Quickstart

From a checkout of the PROJECT BOND workspace to a rendered compendium PDF.

## Prerequisites

- Python 3.10+ and [`uv`](https://github.com/astral-sh/uv)
- The sibling bond packages present under `projects/working/bond/` —
  `bond-manuscript` reads all 33 of them and declares `bond-api`,
  `bond-coordinator`, and `bond-utilities` as local path dependencies
- Pandoc and XeLaTeX for the PDF step (rendering only)

## Install

```bash
cd projects/working/bond/bond-manuscript
uv sync --all-extras
```

Use `--all-extras`. A bare `uv sync` prunes the `dev` group, and `uv run pytest`
then resolves a different interpreter that silently collects zero tests.

## Run the tests

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

Check the header names Python 3.14.6 with the `cov` plugin, and that the
collected count is greater than zero. Exit code 0 alone proves nothing.

## Build the compendium

```bash
uv run python scripts/generate_compendium.py
```

Writes into `manuscript/`: the unified `references.bib`, the architecture chapter,
27 film chapters, 6 infrastructure chapters, and the references chapter. It
prints a one-line summary — package count, reference count, chapter counts.

Exit code 1 means one or more films' `MissionProvider` could not be imported;
those chapters lost their mission brief line. The failing slugs and the exception
text are on stderr. Install the missing dependency into this package's
environment and re-run rather than shipping the shorter build.

## Hydrate tokens

```bash
uv run python scripts/z_generate_manuscript_variables.py
```

Resolves `{{SUITE_TITLE}}`, `{{N_PACKAGES}}`, `{{N_FILMS}}`, `{{N_INFRA}}`,
`{{N_GATE_MEASURED}}` and writes the resolved tree to `output/manuscript/`. The
renderer reads those copies, never `manuscript/` directly.

## Render

From the **template repository root**, not from here:

```bash
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

Produces:

- `output/pdf/bond-manuscript_combined.pdf` — the compendium
- `output/web/` — `index.html` plus one page per section
- `output/slides/` — one Beamer PDF per section

## Verify

```bash
# every token resolved
grep -r "{{" output/manuscript/ && echo "UNRESOLVED" || echo "All tokens resolved"

# regeneration is byte-stable
uv run python scripts/generate_compendium.py && git diff --stat manuscript/
```

## Command reference

| Task | Command (from `bond-manuscript/`) |
| --- | --- |
| Install | `uv sync --all-extras` |
| Tests + coverage gate | `uv run pytest tests/ --cov=src --cov-fail-under=90` |
| Build the compendium | `uv run python scripts/generate_compendium.py` |
| Hydrate tokens | `uv run python scripts/z_generate_manuscript_variables.py` |
| Render (from template root) | `uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript` |
| Clean outputs | `rm -rf output/` |
| Fleet docs gate (from `../`) | `python3 _phase_docs_gate.py` |

## Next

- [`agent_instructions.md`](agent_instructions.md) — the rules before you change anything
- [`troubleshooting.md`](troubleshooting.md) — when a step above fails
- [`architecture.md`](architecture.md) — how the pieces fit

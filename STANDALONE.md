# Standalone Fork Guide

<!-- BEGIN:PUBLICATION_INDEX -->
<!-- Regenerated from docs/manuscript/config.yaml; do not hand-edit the facts below. -->

## Publication identity

- Standalone repository: [docxology/bond](https://github.com/docxology/bond) (default branch `main`)
- Version: `1.0.0` (`pyproject.toml`, `docs/manuscript/config.yaml`, `CITATION.cff`)
- Stable concept DOI: [10.5281/zenodo.21843592](https://doi.org/10.5281/zenodo.21843592)
- Version DOI: [10.5281/zenodo.21843802](https://zenodo.org/records/21843802)
- Release: [v1.0.0](https://github.com/docxology/bond/releases/tag/v1.0.0)
- Metadata source: [`docs/manuscript/config.yaml`](docs/manuscript/config.yaml); citation sidecars (`.zenodo.json`, `CITATION.cff`, `codemeta.json`) live at the repository root.
- No mirror locations are declared beyond the repository and the Zenodo record.

<!-- END:PUBLICATION_INDEX -->

## Purpose

`bond-manuscript` is the **wrapper manuscript** for the PROJECT BOND suite: it
discovers the 33 packages, imports one chapter per package from that package's
own manuscript, merges every package's `references.bib` into one bibliography,
and renders a single combined PDF.

## What works in a standalone checkout

- `docs/manuscript/` — the wrapper manuscript: hand-authored boundaries plus the
  generated chapters and unified bibliography as of the last build.
- `src/bond_manuscript/` — the generator core (`compendium.py`,
  `manuscript_variables.py`); it imports suite packages lazily and needs none of
  them to be importable at module load.
- `scripts/generate_compendium.py`, `scripts/z_generate_manuscript_variables.py`
  — the two build orchestrators.
- `uv run pytest tests/ --cov=src --cov-fail-under=90`,
  `uv run ruff check src/ scripts/ tests/`, `uv run mypy src/` — the documented
  gates, run from the repository root.

## What needs the sibling packages

Regenerating the compendium reads the other 33 packages from the suite root
(`--bond-root`, default `../..`): each package's `docs/manuscript/`,
`output/data/manuscript_variables.json`, `references.bib`, and its live
`MissionProvider`. A checkout without them can read the committed manuscript but
cannot rebuild it, and the fleet-wide tests that assert per-package chapters fail
rather than skip.

## Reusing this generator for another suite

[`docs/forking_guide.md`](docs/forking_guide.md) is the real guide: what is
transferable from `compendium.py`, the steps to repoint discovery and the chapter
builders, and the properties worth keeping (pure core, thin orchestrators, loud
failure, byte-stable regeneration).

## Required post-fork edits

- Update `docs/manuscript/config.yaml`, `domain_profile.yaml`,
  `experiment_plan.yaml`, `CITATION.cff`, `.zenodo.json`, `codemeta.json`, and
  `pyproject.toml`.
- Replace the roster source and the infrastructure package table in
  `compendium.py` with your suite's own.
- Regenerate the manuscript before restating any chapter's content.

## Validation commands

From the repository root:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/generate_compendium.py                  # exit 1 = a provider failed to load
uv run python scripts/z_generate_manuscript_variables.py
```

## What not to claim

Do not restate a chapter's numbers from a renamed fork until
`generate_compendium.py` has been re-run against that fork's packages: every
figure in the combined manuscript is imported from a package, not authored here.

# bond-manuscript — the PROJECT BOND compendium

The **top-level wrapper manuscript** for the 33-package BOND suite. This is the
manuscript the template renders: one chapter imported from each package's own
manuscript, framed by an introduction and a closing, with a **unified
bibliography** merged from every package's `references.bib`.

<p align="center"><img src="docs/manuscript/assets/project_bond_cover.png" alt="Project Bond cover" width="320"></p>

**Codename:** THE COMPENDIUM · **Rendered PDF:** `output/pdf/bond-manuscript_combined.pdf`

## System architecture

```mermaid
flowchart TD
    accTitle: PROJECT BOND 33-package layered architecture and compendium dataflow
    accDescr: Operator commands enter bond-cli and fleet audits run through bond-ops at Layer 4. bond-cli delegates roster and gate status to bond-coordinator at Layer 2, multi-film DAG runs to bond-orchestrator at Layer 3, and single-film lifecycle or gadget calls to bond-api at Layer 1. The 27 per-film packages implement the frozen bond-api MissionProvider contract and consume Layer 0 bond-utilities primitives. The bond compendium hub imports hydrated manuscripts, figures, live MissionProvider metadata and BibTeX references from all 33 packages into one unified publication.
    CLI["Layer 4 · bond-cli (THE FRONT DOOR)<br/>Verb-first dispatch: list, status, whois, run, brief..debrief, gadgets"]
    OPS["Layer 4 · bond-ops (QUARTERMASTER)<br/>Read-only 33-repo inventory, pytest/ruff gate runner and git health"]
    COORD["Layer 2 · bond-coordinator (MISSION CONTROL)<br/>27-film canonical roster, reconcile, lifecycle ledger and situation room"]
    ORCH["Layer 3 · bond-orchestrator (DAG 00)<br/>Topological film DAG runner, checkpoint/resume, retry and provenance"]
    API["Layer 1 · bond-api (THE PROTOCOL)<br/>Frozen MissionProvider contract, GadgetRegistry and slug discovery"]
    FILMS["27 Per-Film Packages (dr_no .. no_time_to_die)<br/>Pure domain cores + mission.py MissionProvider adapters"]
    UTIL["Layer 0 · bond-utilities (Q-BRANCH)<br/>Deterministic ciphers, codenames, clock, seeded RNG and provenance I/O"]
    HUB["Hub · bond-manuscript (THE COMPENDIUM)<br/>Imports 27 film + 6 infra manuscripts, figures and unified references.bib"]

    CLI -->|"list, status, whois, roster-export"| COORD
    CLI -->|"run, missions"| ORCH
    CLI -->|"brief..debrief, gadgets"| API
    OPS -->|"gate manifest JSON"| COORD
    OPS -.->|"audits 33 checkouts"| FILMS
    COORD -->|"reconcile via discovery"| API
    ORCH -->|"FilmProviderAdapter"| API
    API -->|"load_provider(slug)"| FILMS
    FILMS -->|"shared primitives"| UTIL
    API -->|"field primitives"| UTIL
    FILMS -->|"manuscripts, tokens and BibTeX"| HUB
    OPS -->|"measured gate and infra chapters"| HUB
```

**Source map:** [`compendium.py`](src/bond_manuscript/compendium.py), [`manuscript_variables.py`](src/bond_manuscript/manuscript_variables.py), [`02_suite_architecture.md`](docs/manuscript/02_suite_architecture.md), [`generate_compendium.py`](scripts/generate_compendium.py).

## Public release

The public source repository is https://github.com/docxology/bond. The v1.0.0
release is available at https://github.com/docxology/bond/releases/tag/v1.0.0.
The archival Zenodo record is https://doi.org/10.5281/zenodo.21843802; the
concept DOI is https://doi.org/10.5281/zenodo.21843592. The PDF attached to the
release carries the concept DOI so it remains stable across Zenodo versions.

## What it is

| Piece | Origin |
| --- | --- |
| `00_abstract.md` · `01_introduction.md` · `90_closing.md` | hand-written wrapper prose (tokens injected) |
| `02_suite_architecture.md` | generated — layered topology + roster + measured gate |
| `03_01_…` … `03_27_…` | **generated film chapters** — one per Bond film, the package's **full manuscript** imported (abstract + every authored section + figures) |
| `04_01_…` … `04_06_…` | **generated infrastructure chapters** (utilities, api, coordinator, orchestrator, cli, ops) |
| `99_references.md` · `references.bib` | generated — the **unified bibliography** merged from all 33 packages |

Each package chapter reproduces that package's **complete manuscript**, not an
abstract-only excerpt: the abstract and every authored section (introduction,
methodology, results, conclusion, experimental setup, reproducibility, scope)
are imported token-hydrated from the package's own `manuscript_variables.json`,
its figures are carried into the combined PDF, its mission codename/objectives
are read from its live `MissionProvider`, and its references are merged into
the unified `references.bib` (both real BibTeX and plain-numbered lists are
handled and de-duplicated by key).

## Regenerate + render

```bash
# 1. Regenerate the compendium (33 chapters + unified bibliography)
uv run python scripts/generate_compendium.py

# 2. Hydrate {{TOKEN}}s into output/manuscript/
uv run python scripts/z_generate_manuscript_variables.py

# 3. Render the wrapper PDF via the template pipeline (from the repo root)
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

`generate_compendium.py` is deterministic: re-running it produces byte-identical
sections and bibliography (test-locked).

## Layout

```
src/bond_manuscript/   compendium.py (discovery, abstract import, bib merge, sections)
                       manuscript_variables.py ({{TOKEN}} map from live discovery)
scripts/               generate_compendium.py · z_generate_manuscript_variables.py
docs/manuscript/            the wrapper manuscript (sections + unified references.bib)
tests/                 43 tests, no mocks, ≥90% coverage on src/
```

The 33 source packages this compendium imports from live outside this
repository: `scripts/generate_compendium.py` resolves the suite root from
`--bond-root` (default `../..`) and needs those sibling checkouts to regenerate
the chapters. The published tree carries the wrapper plus its generated sections.

# docs/ — project documentation

Operational documentation for `bond-manuscript`, the generator that assembles the
PROJECT BOND compendium from the suite's 33 package manuscripts.

**Quick links:** [Agent instructions](agent_instructions.md) ·
[Architecture](architecture.md) · [Quickstart](quickstart.md) ·
[Testing](testing_philosophy.md) · [Rendering](rendering_pipeline.md) ·
[Troubleshooting](troubleshooting.md) · [Index](AGENTS.md)

## What this package is

The compendium is a **wrapper manuscript**. It does not contain research of its
own: it discovers the fleet from `bond_coordinator.registry.ROSTER`, imports one
abstract per package, reads each film's live `MissionProvider` for its mission
brief, merges every package's `references.bib` into one bibliography, and emits
the architecture chapter, 33 package chapters, and the references chapter.

Everything it prints about a film comes from that film's package. That single
constraint explains most of the rules in these documents.

## Where to start

**Before changing code** — [`agent_instructions.md`](agent_instructions.md), then
[`architecture.md`](architecture.md) for the layer boundaries, then
[`testing_philosophy.md`](testing_philosophy.md) for the zero-mock standard.

**Before editing the manuscript** — [`rendering_pipeline.md`](rendering_pipeline.md)
for which files are generated, then [`syntax_guide.md`](syntax_guide.md) for the
token and cross-reference rules.

**Before running anything** — [`quickstart.md`](quickstart.md).

**When something breaks** — [`troubleshooting.md`](troubleshooting.md) covers the
failures this project actually produces: a provider that stopped importing, an
abstract whose tokens resolved to nothing, a bibliography entry that killed the
LaTeX run.

## Document map

| File | Purpose |
| --- | --- |
| [`agent_instructions.md`](agent_instructions.md) | Hard rules and the verification checklist |
| [`architecture.md`](architecture.md) | Layers, dependency direction, data flow, forbidden patterns |
| [`quickstart.md`](quickstart.md) | Clean checkout to rendered PDF |
| [`testing_philosophy.md`](testing_philosophy.md) | Zero mocks, coverage mechanics, running the gate honestly |
| [`rendering_pipeline.md`](rendering_pipeline.md) | generate → hydrate → render |
| [`syntax_guide.md`](syntax_guide.md) | Tokens, citations, cross-reference constraints |
| [`style_guide.md`](style_guide.md) | Code and prose conventions |
| [`output_conventions.md`](output_conventions.md) | `output/` layout and regeneration |
| [`output_inventory.md`](output_inventory.md) | Per-artifact producer table |
| [`troubleshooting.md`](troubleshooting.md) | Symptom-driven fixes |
| [`faq.md`](faq.md) | Recurring questions |
| [`forking_guide.md`](forking_guide.md) | Reusing the generator for another suite |
| [`AGENTS.md`](AGENTS.md) | Technical index of this directory |

## Verification commands

```bash
cd projects/working/bond/bond-manuscript

# Tests and coverage gate
uv run pytest tests/ --cov=src --cov-fail-under=90

# The core stays free of template infrastructure
grep -rn "^\(from\|import\) infrastructure" src/ || echo "Clean"

# Build the compendium (exit 1 = a film provider failed to import)
uv run python scripts/generate_compendium.py
```

## See also

- [`../README.md`](../README.md) — what the compendium is, in one page
- [`../AGENTS.md`](../AGENTS.md) — project contract
- [`../TODO.md`](../TODO.md) — known gaps, ranked
- [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) — manuscript directory rules

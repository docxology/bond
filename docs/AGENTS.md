# docs/ — index

Documentation for `bond-manuscript`, the PROJECT BOND compendium generator.
Start with [`agent_instructions.md`](agent_instructions.md); everything else is
lookup.

## Inventory

| File | Covers |
| --- | --- |
| [`agent_instructions.md`](agent_instructions.md) | The seven rules and the verification checklist. Read first |
| [`architecture.md`](architecture.md) | Layers, dependency direction, data flow, forbidden patterns |
| [`quickstart.md`](quickstart.md) | Shortest path from a clean checkout to a rendered PDF |
| [`testing_philosophy.md`](testing_philosophy.md) | Zero-mock standard, coverage mechanics, the gate-vs-exit-code rule |
| [`rendering_pipeline.md`](rendering_pipeline.md) | generate → hydrate → render, and what each step writes |
| [`syntax_guide.md`](syntax_guide.md) | Tokens, citations, cross-references, and what the wrapper cannot resolve |
| [`style_guide.md`](style_guide.md) | Prose and code conventions across the package |
| [`output_conventions.md`](output_conventions.md) | What `output/` holds and how to regenerate it |
| [`output_inventory.md`](output_inventory.md) | Per-artifact producer table |
| [`troubleshooting.md`](troubleshooting.md) | Symptom-driven fixes for the failures this project actually has |
| [`faq.md`](faq.md) | Recurring questions about the wrapper model |
| [`forking_guide.md`](forking_guide.md) | Reusing this generator for another package suite |
| [`README.md`](README.md) | Human-facing navigation |
| [`AGENTS.md`](AGENTS.md) | This index |

## Conventions these documents assume

**Imported, not authored.** The compendium's package chapters are generated from
the fleet. Any correction to a film's content belongs in that film's package.

**Generated files are build output.** `02_suite_architecture.md`, `03_*`, `04_*`,
`99_references.md`, and `references.bib` are rewritten by
`scripts/generate_compendium.py` on every run.

**The core is pure.** `src/bond_manuscript/compendium.py` reads files and returns
strings; it never writes and never imports `infrastructure.*`.

**Loud failure over short output.** A build that silently drops a chapter's
content is a failed build. `generate_compendium.py` exits 1 when a film's
`MissionProvider` cannot be imported.

**Numbers are measured, not typed.** Do not hardcode a test count or a coverage
percentage in prose here; name the command that produces it.

## Verification

```bash
cd projects/working/bond/bond-manuscript
uv run pytest tests/ --cov=src --cov-fail-under=90
grep -rn "^\(from\|import\) infrastructure" src/ || echo "Clean"
uv run python scripts/generate_compendium.py

# Fleet-wide documentation gate (phantom modules, mock frameworks, doc floors)
cd .. && python3 _phase_docs_gate.py
```

## Cross-references

- [`../AGENTS.md`](../AGENTS.md) — project contract and hard rules
- [`../README.md`](../README.md) — what the compendium is
- [`../src/AGENTS.md`](../src/AGENTS.md) — the generator API
- [`../tests/AGENTS.md`](../tests/AGENTS.md) — what the suite covers
- [`../scripts/AGENTS.md`](../scripts/AGENTS.md) — orchestrator contract
- [`../manuscript/AGENTS.md`](../manuscript/AGENTS.md) — manuscript directory rules

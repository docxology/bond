# Agent instructions — bond-manuscript

Read this before changing anything in this package.

`bond-manuscript` assembles the PROJECT BOND compendium from the 33 sibling
package manuscripts. Almost every fact it prints is imported from somewhere else.
The rules below all follow from that.

## 1. Work only inside this directory

Never edit a sibling bond package, the bond root, or the template repository from
here. This tree is local-only and has no remote — never push.

If a package chapter is wrong, the fix belongs in that package's
`manuscript/00_abstract.md`, `manuscript/references.bib`, or
`src/<slug>/mission.py` — not here. Report it rather than reaching across.

## 2. Generated sections are build output

Owned by `scripts/generate_compendium.py` and rewritten on every run:

- `manuscript/02_suite_architecture.md`
- `manuscript/03_01_…` … `03_27_…` (film chapters)
- `manuscript/04_01_…` … `04_06_…` (infrastructure chapters)
- `manuscript/99_references.md`
- `manuscript/references.bib`

Hand-authored: `manuscript/00_abstract.md`, `01_introduction.md`, `90_closing.md`,
`preamble.md`, `config.yaml`.

Editing a generated file is a no-op that survives until the next build and then
disappears. Change the generator or the source package.

## 3. Import, never duplicate

If a fact belongs to a film, it is read from that film's manuscript. Do not retype
a codename, an objective, a metric, or a citation into this package. The chapter
builders exist precisely so no fact has two homes.

## 4. Keep the core pure

`src/bond_manuscript/compendium.py` reads and returns strings. It does not write
files, does not import `infrastructure.*`, and imports suite packages lazily
inside the functions that need them. All writing happens in `scripts/`.

## 5. Never swallow a failure that costs content

A provider that stops importing, a variables file that will not parse, a
bibliography that vanished — each of these silently shortens the compendium.
Record the failure (`BRIEF_FAILURES` is the existing mechanism) and let the
orchestrator exit non-zero. `generate_compendium.py` returns 1 when any film's
`MissionProvider` failed to load; keep it that way.

## 6. Determinism is a tested property

Same package tree in, byte-identical manuscript out. No timestamps, no run IDs,
no `set` or `glob` ordering in anything that reaches a file.
`test_regeneration_is_deterministic` re-runs the generator and compares bytes.

## 7. Every path you name must exist

This documentation set was once 23 files describing a different project's modules.
Before you write a file path, a function name, or a command into any doc here,
run it or open it. The fleet docs gate re-checks this:

```bash
cd projects/working/bond && python3 _phase_docs_gate.py 2>&1 | grep bond-manuscript -A20
```

## Verification checklist

```bash
cd projects/working/bond/bond-manuscript

# 1. Suite passes and coverage gate is met — confirm collected > 0, not just exit 0
uv run pytest tests/ --cov=src --cov-fail-under=90

# 2. The core imports no template infrastructure
grep -rn "^\(from\|import\) infrastructure" src/ || echo "Clean"

# 3. The build succeeds and every provider loads (exit 1 means lost content)
uv run python scripts/generate_compendium.py

# 4. Regeneration is byte-stable
uv run python scripts/generate_compendium.py && git diff --stat manuscript/
```

## See also

- [`architecture.md`](architecture.md) — layers and data flow
- [`testing_philosophy.md`](testing_philosophy.md) — the zero-mock standard
- [`rendering_pipeline.md`](rendering_pipeline.md) — generate → hydrate → render
- [`troubleshooting.md`](troubleshooting.md) — the failures this project actually has
- [`../AGENTS.md`](../AGENTS.md) — the project-level contract

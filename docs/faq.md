# FAQ

## The wrapper model

### Why does this package have almost no content of its own?

Because duplicating the fleet's content is the failure mode it exists to prevent.
`bond-manuscript` hand-authors three sections — abstract, introduction, closing —
and imports everything else. A film's codename, objectives, abstract, and
citations live in that film's package and are read from there on every build.

### Which files are generated?

`docs/manuscript/02_suite_architecture.md`, `03_01_…`–`03_27_…`, `04_01_…`–`04_06_…`,
`99_references.md`, and `docs/manuscript/references.bib`. All are rewritten by
`scripts/generate_compendium.py`. Hand-authored: `00_abstract.md`,
`01_introduction.md`, `90_closing.md`, `preamble.md`, `config.yaml`.

### I edited a package chapter and my change vanished

It was a generated file. Edit the source package's `docs/manuscript/00_abstract.md`,
or edit the builder in `src/bond_manuscript/compendium.py`, and re-run the
generator.

### How does the package list get built?

`discover_packages()` reads the canon-ordered 27-film roster from
`bond_coordinator.registry.ROSTER` — the single source of truth for film metadata
— and carries the 6 infrastructure packages as a table in `compendium.py`. A
package is included only if it has a `docs/manuscript/` directory on disk.

### Why does `pyproject.toml` depend on scipy?

Because `die_another_day`'s `MissionProvider` imports it. The compendium loads
every film's provider to build the chapter brief line, so that dependency has to
resolve here too. When it did not, the chapter silently lost a line — which is
why the build now exits non-zero instead.

## Bibliography

### How is the unified bibliography built?

`build_references_bib()` merges every package's `docs/manuscript/references.bib` into
one, de-duplicating by key. Real `@entry` blocks are preserved verbatim; plain
`[n] Author, *Title*, …` lists become deterministic `@misc` entries keyed
`<slug>_ref<n>`.

### Can I add an entry to `docs/manuscript/references.bib`?

No — it is a merge output and your entry disappears on the next build. Add it to
the source package's `references.bib`.

### Why is there special handling for LaTeX accents?

Because braces cannot be stripped blindly. `Fran{\c{c}}ois` with braces removed
becomes `Fran\ccois`, an undefined control sequence that failed the Beamer build
for the whole references section. `latex_to_text()` resolves accents to Unicode
first, then removes the leftover grouping braces.

## Testing

### Why no mocks?

Because there is nothing worth mocking. The generator is pure functions over
files — no network, no clock, no service. Tests run against the real fleet, and
where a case cannot exist in the fleet they build a real package tree under
`tmp_path`. A mocked provider would assert that the loader was called, which is
precisely the failure that let a provider silently stop importing.

### Why is `src/` covered and `scripts/` not?

Coverage is measured over `src` (`pyproject.toml`, `source = ["src"]`). The
orchestrators are covered indirectly: `test_script_smoke_regen` runs
`generate_compendium.py` as a subprocess and asserts its exit code, and
`test_regeneration_is_deterministic` runs it again and compares bytes.

### Coverage dropped after my change

Add the test. `--cov-fail-under=90` with `branch = true` is the gate; the missing
column names the uncovered branch. Do not delete a test to move the number.

### Why do two tests skip sometimes?

`test_script_smoke_regen` and `test_regeneration_is_deterministic` require
`../output/aggregate/gate_manifest.json`. Without it, nothing is checking the
generator CLI or byte-stable regeneration — read the skip count, not just the
pass count.

## Building and rendering

### Where does the PDF end up?

`output/pdf/bond-manuscript_combined.pdf`, alongside per-section HTML in
`output/web/` and per-section Beamer decks in `output/slides/`.

### Why is the render command run from the repository root?

`stage_03_render.py` belongs to the template pipeline, not to this package:

```bash
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript
```

### Does the compendium carry figures?

It generates none of its own — the architecture chapter is tables only — but it
**copies every figure each package manuscript embeds** into
`output/figures/` under a slug-namespaced name and carries them into the
combined PDF. The fleet uses three source-path conventions (relative to the
package `docs/manuscript/`, to the package root, and to the package
`output/figures/`); the generator tries each before degrading an embed to a
caption. `../TODO.md` tracks a deterministic dependency-layer figure as future
work.

### Half the scripts in `scripts/` fail immediately

Eight of them are scaffold. Four import modules this fork never had; four compute
the template root by fixed directory depth and miss it from this package's path.
Only `generate_compendium.py` and `z_generate_manuscript_variables.py` are part of
the build — see [`../scripts/README.md`](../scripts/README.md).

## See also

- [`troubleshooting.md`](troubleshooting.md) — symptom-driven fixes
- [`architecture.md`](architecture.md) — layers and data flow
- [`rendering_pipeline.md`](rendering_pipeline.md) — the three build steps

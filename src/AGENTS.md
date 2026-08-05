# src/ — the compendium generator (pure core)

`src/bond_manuscript/` is the whole implementation of the PROJECT BOND compendium:
the code that discovers the fleet's 33 packages, imports one abstract per package,
merges every package's bibliography into one, and builds the generated chapters.
Everything under `scripts/` is a thin orchestrator over these two modules.

```
src/bond_manuscript/
    __init__.py              public API re-exports
    compendium.py            discovery, abstract import, reference merge, section builders
    manuscript_variables.py  the compendium's own {{TOKEN}} map
```

There is no `analysis/`, no `figures/`, no dashboard, and no experiment. The
compendium computes nothing numerical of its own — its inputs are the sibling
packages' manuscripts and the coordinator's roster.

## Public API (`from bond_manuscript import …`)

| Symbol | Kind | What it does |
| --- | --- | --- |
| `PackageInfo` | frozen dataclass | Catalogue entry: `slug`, `title`, `year`, `codename`, `kind` (`"film"`/`"infra"`), `concepts`, `phenomena` |
| `Reference` | frozen dataclass | One merged bibliography entry: `key`, `bibtex`, `source_package` |
| `discover_packages(bond_root)` | `-> list[PackageInfo]` | 27 films from `bond_coordinator.registry.ROSTER` (canon order) + 6 infrastructure packages carried as data in `compendium.py`. A package is included only if `<bond_root>/<slug>/manuscript/` exists |
| `import_package_abstract(package_dir)` | `-> str` | The package's abstract as one cleaned paragraph, tokens resolved |
| `parse_references(package_dir, slug)` | `-> list[Reference]` | Parses that package's `manuscript/references.bib` |
| `build_references_bib(packages, bond_root)` | `-> tuple[str, list[Reference]]` | The unified BibTeX text plus the ordered entry list |
| `build_architecture_section(packages, bond_root)` | `-> str` | `02_suite_architecture.md`: layer table, roster table, and (when `output/aggregate/gate_manifest.json` exists) a measured-coverage table |
| `build_package_section(pkg, package_dir, abstract, reference_keys, index)` | `-> str` | One package chapter: header, concepts, imported abstract, `## Sources` |
| `build_references_section(references)` | `-> str` | `99_references.md`, grouped by source package |

Also in `compendium.py`, used by the generator and pinned by tests:

- `latex_to_text(value)` — renders a BibTeX field as readable plain text, resolving
  LaTeX accent commands to Unicode.
- `BRIEF_FAILURES` — module-level `dict[slug, error]` of packages whose
  `MissionProvider` could not be imported on the last run.
- `_brief_line(package_dir, slug)` — loads the film's live provider through
  `bond_api.discovery.load_provider` and returns its mission codename and objectives.
- `_strip_crossrefs(body)` — removes package-local pandoc-crossref labels.

`manuscript_variables.py` exposes one function, `generate_variables(*, bond_root=None)`,
returning `SUITE_TITLE`, `SUITE_TITLE_SHORT`, `N_FILMS`, `N_INFRA`, `N_PACKAGES`,
and `N_GATE_MEASURED` — all derived from live discovery, never typed by hand.

## Invariants

1. **Pure core.** `compendium.py` does file reads and string building only. It
   never writes; `scripts/generate_compendium.py` owns all output.
2. **Suite dependencies are imported lazily**, inside the functions that need
   them (`bond_coordinator.registry` in `discover_packages`, `bond_api.discovery`
   in `_brief_line`). Importing them at module scope would make the package
   unimportable whenever a sibling is mid-edit.
3. **No `infrastructure.*` imports.** The template's infrastructure is reached
   only from `scripts/`, never from `src/`.
4. **Deterministic.** Same package tree in, byte-identical manuscript out.
   Ordering comes from the roster and from `OrderedDict`, never from set
   iteration or filesystem order.
5. **Content is imported, never duplicated.** If a fact about a film belongs in
   that film's manuscript, it is read from there — it is not re-typed here.

## Gotchas the code already paid for

Each of these is load-bearing; the comment in the source explains it, and a test
pins it. Do not "simplify" any of them without reading the matching test.

- **Token values are not all strings.** A package's
  `manuscript_variables.json` carries real JSON types, so `_resolve_tokens`
  coerces with `str()`. Returning an `int` from `re.sub` raises
  "expected str instance, int found" and takes the whole build down.
- **Two variable-file conventions.** 31 packages write
  `output/data/manuscript_variables.json`; `bond-cli` and `bond-ops` write
  `output/variables/`. `_VARIABLE_PATHS` covers both. Reading only the majority
  path silently rendered those two chapters as `**** (**)`.
- **Braces cannot be stripped blindly from BibTeX.** `Fran{\c{c}}ois` with
  braces deleted becomes `Fran\ccois`, an undefined control sequence that fails
  the Beamer build for the entire references section. `latex_to_text` resolves
  accents to Unicode first.
- **A provider that stops importing is a break, not an absence.** `_brief_line`
  returns `""` only when the package genuinely has no `mission.py`; every other
  failure is recorded in `BRIEF_FAILURES` so the generator can exit non-zero.
- **Package-local cross-references do not resolve in the wrapper.** An abstract
  citing `[@sec:results]` renders as `sec. ??` in the combined PDF, so
  `_strip_crossrefs` rewrites section refs into prose and drops the rest.

## Verify

```bash
cd projects/working/bond/bond-manuscript
uv run pytest tests/ --cov=src --cov-fail-under=90

# src/ must stay free of template infrastructure
grep -rn "^\(from\|import\) infrastructure" src/ || echo "Clean"
```

## See also

- [`README.md`](README.md) — orientation and a runnable example
- [`STYLE.md`](STYLE.md) — coding conventions for these modules
- [`../tests/AGENTS.md`](../tests/AGENTS.md) — what the suite covers
- [`../docs/architecture.md`](../docs/architecture.md) — layer boundaries

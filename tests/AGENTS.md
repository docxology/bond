# tests/ — the compendium test suite

One test module, `test_compendium.py`, covers everything in
`src/bond_manuscript/`. It runs against the **real fleet** — the 33 sibling
package trees under `projects/working/bond/` — plus `tmp_path` packages built
in-test for the cases real data cannot reach. There are no mocks.

```
tests/
    conftest.py         MPLBACKEND=Agg; puts src/ on sys.path
    test_compendium.py  the whole suite
```

## The gate

```bash
cd projects/working/bond/bond-manuscript
uv run pytest tests/ --cov=src --cov-fail-under=90
```

A green exit code is not proof the suite ran. Confirm **collected > 0** and a
coverage figure in the summary. If `pytest` resolves to an interpreter without
this package's dependencies it collects nothing and still exits 0 — see
[`../docs/troubleshooting.md`](../docs/troubleshooting.md).

## What is covered

| Area | Representative tests |
| --- | --- |
| Discovery | `test_discover_33_packages` (27 films + 6 infra, canon order, `dr_no` first), `test_discover_packages_skips_absent_manuscripts` |
| Generated manuscript on disk | `test_manuscript_sections_complete`, `test_every_package_chapter_present_on_disk`, `test_references_bib_present` |
| Abstract import | `test_imported_abstract_is_token_resolved`, `test_import_abstract_prefers_hydrated_output`, `test_import_abstract_fallback_strips_tokens`, `test_import_abstract_absent_returns_empty`, `test_import_abstract_survives_corrupt_variables` |
| Token resolution edge cases | `test_resolve_tokens_coerces_non_string_values`, `test_variables_found_under_either_convention`, `test_no_empty_bold_in_any_imported_abstract` |
| Unified bibliography | `test_unified_bibliography_merged`, `test_generated_bibtex_is_balanced`, `test_parse_references_plain_and_bibtex`, `test_parse_references_plain_list`, `test_parse_references_plain_untitled_falls_back_to_text`, `test_parse_references_missing_file_returns_empty` |
| LaTeX rendering | `test_latex_to_text_resolves_accents_without_stray_macros`, `test_references_section_emits_no_latex_backslashes` |
| Mission providers | `test_brief_line_real_provider`, `test_brief_line_missing_provider_returns_empty`, `test_brief_failures_recorded_not_swallowed`, `test_every_film_chapter_has_a_mission_brief_line` |
| Section builders | `test_build_package_section_film`, `test_build_package_section_infra`, `test_build_architecture_section`, `test_build_references_section_groups_by_source` |
| Cross-references | `test_imported_abstracts_carry_no_dangling_crossrefs` |
| Tokens | `test_manuscript_variables_counts` |
| Generator CLI + determinism | `test_script_smoke_regen`, `test_regeneration_is_deterministic` |

The last two are marked
`@pytest.mark.skipif(not (BOND / "output/aggregate/gate_manifest.json").is_file())`.
If that manifest is missing, the CLI tests silently disappear from the run —
check the skip count, not just the pass count.

## Fleet-wide assertions

Four tests assert a property across **every** discovered package rather than a
single example. They are the suite's real safety net, because each one caught a
whole-fleet degradation that a single-package test would have missed:

- `test_no_empty_bold_in_any_imported_abstract` — no abstract may import with its
  tokens stripped to nothing (`****`, `(**)`).
- `test_imported_abstracts_carry_no_dangling_crossrefs` — no `[@…]` or `@sec:`
  may survive into the wrapper.
- `test_every_film_chapter_has_a_mission_brief_line` — all 27 film providers must
  load; a chapter without `Mission **` means a broken import.
- `test_every_package_chapter_present_on_disk` — every discovered package has a
  chapter carrying its codename.

Keep them exhaustive. Narrowing one to a sample is how this class of defect
returns.

## conftest.py

Sets `MPLBACKEND=Agg` and prepends `src/` (and a computed repository root) to
`sys.path` so the documented `uv run pytest tests/` command works from a clean
environment. Its repository-root calculation walks three levels above the project
directory, which was correct at the exemplar's original location; from this
package's deeper path it lands on `projects/`. That is harmless here — nothing in
the suite imports `infrastructure` — but do not rely on it resolving the template
root.

## Adding a test

1. Put it in `test_compendium.py`; the suite is deliberately one file.
2. Prefer real fleet data. Reach for `tmp_path` only when the case cannot exist
   in the fleet (a package with no bibliography, a corrupt variables JSON, a
   provider that fails to import).
3. Assert on observable output — the text of a section, the keys of a merge —
   not on how the function reached it.
4. If the test touches `compendium.BRIEF_FAILURES`, pop your slug before and
   after; it is module-level state shared across the run.
5. Re-run the gate and confirm coverage did not drop.

## See also

- [`README.md`](README.md) — quick start
- [`PATTERNS.md`](PATTERNS.md) — the patterns this suite uses instead of mocks
- [`../docs/testing_philosophy.md`](../docs/testing_philosophy.md) — why no mocks
- [`../src/AGENTS.md`](../src/AGENTS.md) — the code under test

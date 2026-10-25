# Syntax guide

Markup conventions for the compendium's manuscript. The wrapper has constraints
the individual package manuscripts do not, because most of its content is
imported from documents that were written to render somewhere else.

## 1. Tokens

Numbers that describe the suite are injected, never typed. The full token set is
the return value of
`src/bond_manuscript/manuscript_variables.py::generate_variables()`:

| Token | Value | Source |
| --- | --- | --- |
| `{{SUITE_TITLE}}` | `PROJECT BOND — The Special-Agent Operations Compendium` | constant in `generate_variables()` |
| `{{SUITE_TITLE_SHORT}}` | `PROJECT BOND Compendium` | constant |
| `{{N_PACKAGES}}` | count of discovered packages | `discover_packages()` |
| `{{N_FILMS}}` | count with `kind == "film"` | `discover_packages()` |
| `{{N_INFRA}}` | count with `kind == "infra"` | `discover_packages()` |
| `{{N_GATE_MEASURED}}` | packages with a numeric coverage row | `../output/aggregate/gate_manifest.json` |

Used by the hand-authored `00_abstract.md` and `90_closing.md`. Generated
chapters carry no tokens — their numbers were already resolved when the abstract
was imported.

- **BAD**: `PROJECT BOND is a fleet of 33 packages.`
- **GOOD**: `PROJECT BOND is a fleet of **{{N_PACKAGES}} packages**.`

Adding a token means adding a key in `generate_variables()`, asserting it in
`tests/test_compendium.py`, re-running hydration, and only then referencing it.
An unresolved token renders literally in the PDF:

```bash
grep -r "{{" output/manuscript/ && echo "UNRESOLVED" || echo "All tokens resolved"
```

## 2. Citations

All citation keys resolve against the unified `docs/manuscript/references.bib`, which
is a merge output. **Never add an entry to it by hand** — add it to the source
package's `references.bib` and re-run `scripts/generate_compendium.py`.

Two entry shapes reach the merge:

- Real BibTeX `@entry` blocks, normalized to case-insensitive canonical keys and de-duplicated before rendering. Text fields are escaped for safe LaTeX output.
- Plain-text `[n] Author, *Title*, publisher, year. — note` lines, converted to
  `@misc` entries keyed `<slug>_ref<n>`.

Generated chapters cite with Pandoc syntax in their `## Sources` block:

```markdown
## Sources

@walras1874elements; @kyle1985continuous
```

Never write raw `\cite{}` in Markdown.

## 3. Cross-references do not survive import

A package abstract may cite its own sections and theorems. Those labels are real
inside that package's manuscript and absent from the compendium, where they
render as `Section sec. ??` and `[?]`. `_strip_crossrefs()` therefore rewrites
`[@sec:results]` into readable prose and drops `[@def:…]`, `[@prop:…]`,
`[@thm:…]`, `[@fig:…]`, `[@eq:…]`, `[@tbl:…]`, and friends along with any
parenthetical that introduced them.

Two consequences:

- Do not add a package-local cross-reference to a chapter here; it will be
  stripped on the next build.
- If you add a cross-reference **type** to a package manuscript, check that
  `_CROSSREF` in `compendium.py` recognises it, or it will reach the wrapper
  unresolved. `test_imported_abstracts_carry_no_dangling_crossrefs` fails when
  one does.

## 4. LaTeX in bibliography fields

BibTeX fields reach the PDF and the per-section HTML, so accent commands must
resolve rather than be stripped. `latex_to_text()` converts them to Unicode
before braces are removed — `Fran{\c{c}}ois` becomes `François`, not
`Fran\ccois`, which is an undefined control sequence that fails the Beamer build
for the entire references section.

Write accents in source bibliographies either way; write nothing that relies on
a macro `latex_to_text()` does not know. `test_references_section_emits_no_latex_backslashes`
asserts the rendered references list contains no raw backslash.

## 5. Section headings and ordering

Every section file starts with a single `# Title` H1. Files are assembled in
lexicographic filename order, which is the whole ordering mechanism:

```
00_abstract.md            Abstract
01_introduction.md        Introduction
02_suite_architecture.md  Suite Architecture      (generated)
03_01_… … 03_27_…         Film chapters           (generated, canon order)
04_01_… … 04_06_…         Infrastructure chapters (generated)
90_closing.md             Closing
99_references.md          References              (generated)
```

The generated chapter numbering (`FILM_NUMBER = "03"`, `INFRA_NUMBER = "04"` in
`compendium.py`) exists to make that sort come out right. Do not renumber a
chapter by hand.

## 6. Code blocks and inline paths

Tag every fenced block with its language — Pandoc needs it for highlighting.
Reference files with inline backticks and a path that resolves from the package
root: `src/bond_manuscript/compendium.py`, not "the compendium module".

## 7. Prose

Say the concrete thing. "The compendium merges every package's `references.bib`
into one unified bibliography, de-duplicating by key" beats "references are
handled automatically". Avoid "In summary" and "In conclusion" as section
closers.

## See also

- [`rendering_pipeline.md`](rendering_pipeline.md) — where tokens are resolved
- [`manuscript/SYNTAX.md`](manuscript/SYNTAX.md) — the same rules, at the manuscript
- [`../src/AGENTS.md`](../src/AGENTS.md) — `latex_to_text` and `_strip_crossrefs`

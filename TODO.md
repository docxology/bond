# TODO — bond-manuscript (THE COMPENDIUM)

`bond-manuscript` is the top-level **wrapper manuscript** for the 33-package PROJECT BOND
suite: `src/bond_manuscript/compendium.py` discovers every package, imports one chapter per
package from that package's own manuscript (abstract, live `MissionProvider` brief, concepts),
merges every package's `references.bib` into one unified bibliography, and emits the generated
sections that the template pipeline renders into `output/pdf/bond-manuscript_combined.pdf`.

**Verified state, measured 2026-08-05 in this working tree:**

| Gate | Result |
| --- | --- |
| `uv run pytest tests/ --cov=src --cov-fail-under=90` | **34 passed**, **97.18 %** coverage on `src/` (compendium.py 97.62 %, manuscript_variables.py 88.89 %) |
| `uv run ruff check src/ scripts/ tests/` | All checks passed |
| `uv run mypy src/` | Success: no issues found in 3 source files |
| Last render (`output/pdf/`, 2026-08-05 08:52) | 67-page PDF, 0 `??` in `pdftotext`, **89 `^! ` LaTeX errors** in `_latex_stdout.log` |
| Fleet gate (`../output/aggregate/gate_manifest.json`, 12:32) | 34 rows, all `verdict: ok`, all coverage ≥ 90 % |

**Audit provenance.** `../output/verify/` contains no `bond-manuscript.json` and no
`bond-manuscript.unresolved.json`; grepping every file there for `bond-manuscript` and
`compendium` returns zero hits. **No item below is carried over from an unresolved audit
finding** — all of them were found by reading this package this session.

---

## Open work

### Correctness — things that are wrong

#### C1. Citation sidecars claim someone else's DOI, title, and repository
`.zenodo.json`, `CITATION.cff`, `codemeta.json`, and `STANDALONE.md` are unmodified
`template_code_project` scaffold. They assert, as machine-readable record, that this package is
*"Convergence Analysis of Gradient Descent Optimization"*, DOI **10.5281/zenodo.20417136**, repo
`github.com/docxology/bond-manuscript`, plus eight declared mirror locations (GitHub Pages,
HuggingFace, IPFS, Netlify, OSF, test.pypi, Software Heritage, a second version DOI
`10.5281/zenodo.20931934`). None of that applies. `manuscript/config.yaml:21` explicitly declares
`doi: ""  # local-only compendium; no DOI minted` — the sidecars directly contradict the
manuscript's own metadata. `STANDALONE.md:3-17` sits inside a
`<!-- BEGIN:PUBLICATION_INDEX -->` block marked "do not hand-edit", so the fix is either to
delete the sidecars (this tree is local-only and never pushed) or to regenerate them from
`manuscript/config.yaml`.

- **Files:** `.zenodo.json` (whole file), `CITATION.cff` (whole file), `codemeta.json` (whole
  file), `STANDALONE.md:3-17`.
- **Done when:** no file in this package names a DOI, a Zenodo record, or a GitHub/PyPI/OSF/IPFS
  location that this package does not own.
- **Demonstrate:**
  `grep -rn "20417136\|20931934\|Gradient Descent\|docxology/bond-manuscript" . --include="*.json" --include="*.cff" --include="*.md" --exclude-dir=.venv --exclude-dir=_template_resources --exclude-dir=.git --exclude=TODO.md`
  returns nothing. Today it names exactly four files: `.zenodo.json`, `CITATION.cff`,
  `codemeta.json`, `STANDALONE.md`. (`--exclude=TODO.md` because this file quotes the strings.)

#### C2. Bare `_` in merged bibliography fields drops LaTeX into math mode (89 errors)
The last render logged **89 `^! ` errors** — 44 `Missing $ inserted`, 22 `Missing } inserted`,
22 `Extra }`, 1 `Double subscript`. Cause: 14 field lines in the merged `manuscript/references.bib`
carry an unescaped `_`, BibTeX copies them verbatim into `_combined_manuscript.bbl`, and TeX
switches to math mode. Evidence: `output/pdf/_combined_manuscript.bbl:68` reads
`poison_detect.antidote_plan.` and `output/pdf/_latex_stdout.log:563` is the matching
`! Missing $ inserted` at `l.68`. The PDF still builds (batchmode), so the failure is silent —
those spans typeset as italic math with subscripts instead of literal identifiers.

The compendium propagates them without escaping at three points:
`compendium.py:277` (`_parse_bibtex_entries` preserves the source block verbatim),
`compendium.py:286-312` (`_plain_ref_to_bibtex` interpolates raw text into fields), and
`compendium.py:510` (`latex_to_text` maps `r"\_": "_"`, actively **un**escaping a correctly
escaped upstream underscore before `build_references_section` writes it into
`99_references.md`). The upstream source is a sibling package (e.g.
`../casino_royale_2006/manuscript/references.bib:154`) which is outside this package's write
scope, so the escape belongs in the merge.

- **Files:** `src/bond_manuscript/compendium.py:277`, `:286-312`, `:510`, `:541-559`;
  symptom in `manuscript/references.bib` lines 44, 60, 79, 659, 1846, 1871, 1878, 1886, 1896,
  1906, 1916, 1930, 1940, 2277.
- **Done when:** a fresh render logs **0** `^! ` lines, and no BibTeX field value in the merged
  bib contains an unescaped `_`.
- **Demonstrate:**
  ```bash
  uv run python scripts/generate_compendium.py
  grep -nE "^\s+(note|title|author|journal|booktitle|publisher|howpublished|series)\s*=" \
    manuscript/references.bib | grep -cE "[A-Za-z0-9)]_"     # expect 0
  # from the template root, after re-rendering:
  grep -c "^! " output/pdf/_latex_stdout.log                  # expect 0
  ```

#### C3. `{{N_GATE_MEASURED}}` renders 34 in a chapter that just said 33
`manuscript_variables.py:29-33` counts every row of `../output/aggregate/gate_manifest.json` that
carries a numeric coverage. That manifest has **34** rows because `bond-manuscript` measures
itself. `manuscript/90_closing.md:21` then reads "per package: {{N_GATE_MEASURED}} packages
measured, all passing" eighteen lines after `90_closing.md:3-4` states the suite is
**{{N_PACKAGES}} packages** (= 33). The rendered PDF therefore says 33 packages and 34 measured.
Either exclude self from the count or reword the closing to name the wrapper explicitly.

Measured this session: `generate_variables(bond_root=..)` →
`{'N_FILMS': '27', 'N_INFRA': '6', 'N_PACKAGES': '33', 'N_GATE_MEASURED': '34'}`.

- **Files:** `src/bond_manuscript/manuscript_variables.py:29-33`, `manuscript/90_closing.md:21`.
- **Done when:** the rendered closing's package count and measured count are mutually consistent,
  and a test pins the relationship.
- **Demonstrate:**
  `uv run python -c "import sys;sys.path.insert(0,'src');from pathlib import Path;from bond_manuscript.manuscript_variables import generate_variables as g;v=g(bond_root=Path('..').resolve());print(v['N_PACKAGES'], v['N_GATE_MEASURED'])"`

#### C4. Running the test suite rewrites tracked manuscript files
`tests/test_compendium.py:118-127` (`test_script_smoke_regen`) and `:130-141`
(`test_regeneration_is_deterministic`) invoke `scripts/generate_compendium.py` with
`cwd=bond-manuscript`, so the generator deletes and rewrites the **real, git-tracked**
`manuscript/` tree — 33 chapters plus `02_suite_architecture.md`, `99_references.md`, and
`references.bib`. Confirmed this session: `manuscript/03_03_goldfinger.md`,
`manuscript/references.bib`, and `manuscript/02_suite_architecture.md` all carry the mtime of my
`pytest` run. A read-only verification gate must not mutate versioned content; this is how the
tree silently became dirty (see C11).

- **Files:** `tests/test_compendium.py:118-141`; generator target
  `scripts/generate_compendium.py:48-52` (`_rm_owned`) and `:59` (`manuscript = REPO / "manuscript"`).
- **Done when:** `generate_compendium.py` accepts an output directory (or the tests copy the tree
  to `tmp_path` first), and a full `pytest` run leaves `git status --short manuscript/` empty on a
  clean tree.
- **Demonstrate:**
  `git stash -u && uv run pytest tests/ -q && git status --short manuscript/` → no output.

#### C5. Four scripts in `scripts/` are dead — they import modules this package does not have
Probed this session from the **template root** with
`uv run python projects/working/bond/bond-manuscript/scripts/<name>.py --help`:

| Script | Failure |
| --- | --- |
| `scripts/optimization_analysis.py:15` | `ModuleNotFoundError: No module named 'src.analysis'` |
| `scripts/build_dashboard.py:19` | `ModuleNotFoundError: No module named 'src.dashboard'` |
| `scripts/04_benchmark_stage.py` | `ModuleNotFoundError: No module named 'src.benchmark_support'` |
| `scripts/generate_api_docs.py` | `ModuleNotFoundError: No module named 'src.documentation'` |

`src/bond_manuscript/` contains only `__init__.py`, `compendium.py`, and
`manuscript_variables.py`; there is no `src/analysis/`, `src/dashboard.py`,
`src/benchmark_support.py`, or `src/documentation.py`. `AGENTS.md:44` declares the layer contract
as exactly two orchestrators (`generate_compendium.py`, `z_generate_manuscript_variables.py`), so
these four are scaffold residue that no contract claims. The other four inherited stage scripts
(`00_preflight.py`, `08_connector_search.py`, `09_provenance_record.py`, `10_research_workflow.py`)
**do** run from the template root — they only fail under this package's own `.venv`, which is C6,
not this item.

- **Done when:** every file in `scripts/` either runs or is deleted.
- **Demonstrate:** from the template root —
  `for s in projects/working/bond/bond-manuscript/scripts/*.py; do [ "$(basename $s)" = "__init__.py" ] && continue; uv run python "$s" --help >/dev/null 2>&1 || echo "DEAD: $s"; done`
  → no output.

#### C6. Repo-root path arithmetic is off by one for this directory depth
Every inherited script computes the template root for the layout
`projects/templates/<name>/scripts/`. This package lives at
`projects/working/bond/<name>/scripts/` — one level deeper — so all of them resolve to
`<template>/projects` instead of `<template>`, and `infrastructure` never imports.

- `scripts/00_preflight.py:9`, `scripts/08_connector_search.py:19`,
  `scripts/09_provenance_record.py:20`, `scripts/10_research_workflow.py:18` — `parents[4]`.
- `scripts/optimization_analysis.py:10`, `scripts/build_dashboard.py:13`,
  `scripts/generate_api_docs.py:10`, `scripts/04_benchmark_stage.py:19` — `PROJECT_ROOT.parents[2]`.
- `tests/conftest.py:16` — `os.path.join(ROOT, "..", "..", "..")`, with a comment at `:12-15`
  that still asserts "The project lives at `projects/templates/<name>/`". Latent only: no test
  currently imports `infrastructure`, so the suite passes with a wrong path on `sys.path`.

The correct pattern already exists in this package —
`scripts/z_generate_manuscript_variables.py:35-39` walks ancestors looking for
`infrastructure/rendering/` instead of counting directories.

- **Done when:** no file in this package hard-counts parent levels to reach the template root;
  they locate it by probe, as `z_generate_manuscript_variables.py` does.
- **Demonstrate:** `grep -rn 'parents\[4\]\|parents\[2\]\|"\.\.", "\.\.", "\.\."' scripts/ tests/`
  → 10 hits today, 9 of them wrong. **Do not touch the tenth:**
  `tests/test_compendium.py:25` `BOND = Path(__file__).resolve().parents[2]` correctly resolves
  the *bond suite root* (not the template root) and is load-bearing for every fleet test.

#### C7. `pyproject.toml` hard-codes absolute machine paths
`pyproject.toml:35-37` pins `[tool.uv.sources]` to
`/Users/4d/Documents/GitHub/template/projects/working/bond/bond-{api,coordinator,utilities}`.
The package cannot be synced on any other checkout or machine. Relative path deps
(`{ path = "../bond-api" }`) express the same edge.

- **Done when:** `pyproject.toml` contains no absolute path.
- **Demonstrate:** `grep -c "/Users/" pyproject.toml` → 0, then
  `uv sync --all-extras && uv run pytest tests/ -q` still green.

#### C8. Package metadata still describes the optimizer exemplar, and disagrees with the manuscript
`pyproject.toml:13` — `description = "Fully-tested codebase with numerical optimization and
analysis"`. `pyproject.toml:11` declares `version = "2.5.2"` while
`manuscript/config.yaml:10` declares `version: "1.0.0"`; nothing reconciles them.
`pyproject.toml:20-22` also declares `numpy`, `matplotlib`, `pyyaml`, and `defusedxml`, none of
which are imported by `src/bond_manuscript/` or by either live orchestrator (only `scipy` is
genuinely required — `pyproject.toml:23-26` documents why: `die_another_day`'s provider imports it
and the compendium loads every provider).

- **Done when:** description names the compendium, one version is authoritative, and every
  declared runtime dependency has an importer.
- **Demonstrate:**
  `grep -rhn "import" src/bond_manuscript/ scripts/generate_compendium.py scripts/z_generate_manuscript_variables.py | grep -oE "numpy|matplotlib|yaml|defusedxml|scipy" | sort -u`
  lists exactly the declared deps.

#### C9. The rendered PDF is stale relative to the manuscript tree
`output/pdf/bond-manuscript_combined.pdf` is from 08:52; the generated manuscript sections are
from 12:36. The content genuinely diverged — `output/pdf/_combined_manuscript.md` says
*"the island posture is MODERATE"* for `dr_no` while `manuscript/03_01_dr_no.md:11` now says
*"the island posture is HIGH"*. Anyone reading the checked-in PDF reads superseded fleet numbers.

- **Done when:** the PDF is regenerated from the current tree (do C2 first, so the re-render is
  also error-free).
- **Demonstrate:** from the template root,
  `uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript`,
  then `grep -c "island posture is HIGH" output/pdf/_combined_manuscript.md` → 1.

#### C10. Dangling pointer in hand-authored prose
`manuscript/01_introduction.md:41` reads "Every chapter below (in the `Files` section) is
**generated from…**". The compendium has no "Files" section — its sections are Abstract,
Introduction, Suite Architecture, the 33 package chapters, Closing, and References. This is
hand-authored text (`01_introduction.md` is one of the three protected boundaries per
`AGENTS.md:14`), so the generator will not fix it.

- **Done when:** the parenthetical names a section that exists, or is removed.
- **Demonstrate:** ``grep -n '`Files`' manuscript/01_introduction.md`` → no output.

#### C11. 27 regenerated manuscript files are uncommitted
`git status --short` shows 27 modified files under `manuscript/` (22 film chapters + 2 infra
chapters + `02_suite_architecture.md` + `99_references.md` + `references.bib`), produced by
generator runs — including the test-suite
side effect in C4. They are correct output (they reflect current upstream package content), just
uncommitted, so `git diff` is permanently noisy and the next agent cannot tell their own edits
from drift. **Note:** other agents are active in this workspace; confirm ownership before
committing, and commit by explicit pathspec.

- **Done when:** `git status --short manuscript/` is empty.
- **Demonstrate:** `git status --short manuscript/` → no output.

---

### Verification — claims not yet bound by a test that can fail

#### V1. The determinism test cannot detect drift from the committed tree
`tests/test_compendium.py:130-141` reads `03_03_goldfinger.md` and `references.bib`, re-runs the
generator, and asserts the bytes are unchanged. But `test_script_smoke_regen` (`:118-127`) has
already regenerated the tree earlier in the same file, so the "before" bytes are themselves
post-regeneration. The test proves the generator is idempotent within one session; it can never
fail because the checked-in manuscript has fallen behind the fleet. That is exactly the condition
C11 describes, and it went unnoticed.

- **Done when:** a test fails when the on-disk `manuscript/` differs from what the generator
  would produce from the current fleet — generate into `tmp_path` and diff against `manuscript/`.
- **Demonstrate:** touch any sibling package's `00_abstract.md`, run `uv run pytest tests/ -q`,
  observe a failure naming the stale chapter.

#### V2. Both regeneration tests skip silently when the gate manifest is absent
`tests/test_compendium.py:118` and `:130` are guarded by
`@pytest.mark.skipif(not (BOND / "output/aggregate/gate_manifest.json").is_file(), …)`. On a
checkout where the fleet gate has not been run, the only two tests that execute
`generate_compendium.py` disappear and the suite still reports green.

- **Done when:** the generator is exercised unconditionally (the gate manifest only affects the
  optional "Measured gate" table — `compendium.py:455-469` already handles its absence), or a
  collection-time assertion pins that the skip count is 0 in the normal environment.
- **Demonstrate:** `uv run pytest tests/ -q -rs` reports no skips.

#### V3. No test binds the render to being LaTeX-clean
Nothing asserts that the merged bibliography is safe to typeset. C2 shipped 89 LaTeX errors past
a fully green 34-test suite. The cheap binding is a data assertion on the merge output, not a
render: no BibTeX field value emitted by `build_references_bib` may contain an unescaped `_`, and
`build_references_section` output may contain no `_` outside a code span.

- **Files:** the assertion belongs beside `tests/test_compendium.py:356-362`
  (`test_references_section_emits_no_latex_backslashes`), which already pins the analogous
  backslash rule and would have caught this class had it covered `_`.
- **Done when:** the new test fails today against the current fleet bib and passes after C2.
- **Demonstrate:** `uv run pytest tests/ -k underscore -v`.

#### V4. `N_GATE_MEASURED`, `SUITE_TITLE`, `SUITE_TITLE_SHORT` are unbound
`tests/test_compendium.py:104-108` asserts only `N_PACKAGES`, `N_FILMS`, `N_INFRA`. The other
three keys returned by `manuscript_variables.py:36-43` have no test. Worse, `SUITE_TITLE` and
`SUITE_TITLE_SHORT` are generated but referenced **nowhere** in `manuscript/` —
`grep -rn "SUITE_TITLE" manuscript/` returns nothing — so they are dead tokens that no rendered
output would notice losing.

- **Done when:** every key `generate_variables` returns is either asserted by a test or consumed
  by a manuscript section (and the unused ones are dropped).
- **Demonstrate:**
  `uv run python -c "import sys;sys.path.insert(0,'src');from bond_manuscript.manuscript_variables import generate_variables as g;print(sorted(g().keys()))"`
  cross-checked against `grep -oh "{{[A-Z_0-9]*}}" manuscript/*.md | sort -u`.

#### V5. Unreachable defensive branch in the token resolver
`compendium.py:191-193`:

```python
resolved = _resolve_tokens(text, variables)
if _TOKEN.search(resolved):
    resolved = _TOKEN.sub("", resolved)  # any stragglers
```

`_resolve_tokens` (`:135-150`) substitutes **every** match via `variables.get(name, "")`, so no
`{{TOKEN}}` can survive it. Line 193 is one of the three statements the coverage run reports as
never executed. It is either dead (delete it) or it guards a real case — a variable value that
itself contains `{{…}}` — which no test creates.

- **Done when:** the line is removed, or a test constructs a variables file whose value contains a
  token and pins the behaviour.
- **Demonstrate:** `uv run pytest tests/ --cov=src --cov-report=term-missing` no longer lists 193.

#### V6. Dead assignment in the gate-manifest fallback
`manuscript_variables.py:34-35` — the `except (OSError, ValueError): rows = []` branch assigns
`rows`, which is never read afterwards (`gate_ok` was initialised to 0 at `:30` and is only
written inside `try`). Uncovered, and would be a no-op if covered.

- **Done when:** the branch is either exercised by a test with an unreadable/corrupt manifest, or
  simplified to `except (OSError, ValueError): pass`.
- **Demonstrate:** `manuscript_variables.py` reaches 100 % in the coverage report.

#### V7. Five partial branches in `compendium.py` have no test
From this session's `--cov-report=term-missing`: `290->292`, `307->309`, `418->421`, `456->470`,
`462-463`. Concretely:

| Branch | Untested condition |
| --- | --- |
| `290->292`, `307->309` | plain `[n]` reference with no ` — ` note / no italic title, in `_plain_ref_to_bibtex` |
| `418->421` | `build_package_section` for a package with **zero** references — the `## Sources` block is omitted |
| `456->470` | `build_architecture_section` when `gate_manifest.json` is absent — no "Measured gate" table |
| `462-463` | `build_architecture_section` when `gate_manifest.json` is corrupt — `cov = {}`, every row renders `n/a` |

`test_build_architecture_section` (`:177-187`) already conditions on the manifest's presence but
only asserts the positive case.

- **Done when:** each row above has a `tmp_path` test that pins the observable output.
- **Demonstrate:** `uv run pytest tests/ --cov=src --cov-report=term-missing` shows no partial
  branches in `compendium.py`.

---

### Documentation

#### D1. ~~25 documentation files still describe `template_code_project`, not the compendium~~ — RESOLVED 2026-08-05
The whole non-manuscript doc set was unmodified scaffold describing a gradient-descent optimizer
exemplar whose modules never existed here. `src/AGENTS.md` was 411 lines of it; `docs/architecture.md`
documented a seven-module `src/` layout against the real three.

**Fixed.** 24 files rewritten against the real tree: `src/{AGENTS,README,STYLE}.md`, all 13 files in
`docs/`, `tests/{AGENTS,README,PATTERNS}.md`, `scripts/{AGENTS,README,CONVENTIONS}.md`,
`manuscript/{AGENTS,SYNTAX,README}.md`, and `.agents/skills/bond-manuscript/{SKILL,AGENTS}.md`.
Shorter and true rather than long and inherited — `src/AGENTS.md` went from 411 lines to ~110.

**Evidence.**

- `python3 ../_phase_docs_gate.py` → **73 PHANTOM-MODULE findings before, 0 after**; the whole fleet
  gate now reports `34 packages scanned, 0 failing, 0 findings`.
- The path-existence demonstration returns no output:
  `grep -rhoE "src/[a-z_]+\.py|tests/test_[a-z_]+\.py" docs/ src/*.md tests/*.md scripts/*.md | sort -u | while read f; do [ -e "$f" ] || echo "MISSING: $f"; done`
- Every relative markdown link in the rewritten set resolves on disk (two inherited
  `../../../../docs/guides/manuscript-semantics.md` links were off by one directory level and are fixed).
- `uv run pytest tests/ --cov=src --cov-fail-under=90` → 34 passed, 97.18% (unchanged; docs-only change).

**Residual, deliberately not "fixed".** The original enumeration grep still names three files:

```bash
grep -rln "optimizer\.py\|experiment_config\|dashboard\.py\|convergence_plot\|gradient descent\|GradientDescent" \
  --include="*.md" --exclude=TODO.md . | grep -v _template_resources | grep -v "\.venv/"
```

→ `docs/troubleshooting.md`, `scripts/README.md`, `scripts/AGENTS.md`. In all three the only match is
the substring `dashboard.py` inside **`build_dashboard.py`**, a script that really exists here. The
pattern is unanchored; these are true references, not drift. Verify with
`grep -noE "optimizer\.py|dashboard\.py|gradient descent" <file>`.

#### D2. `README.md` and `AGENTS.md` state a test count and coverage that are both wrong
`README.md:49` — "`tests/  18 tests, no mocks, ≥90% coverage on src/`".
`AGENTS.md:24` — "(18 tests, ≥91%)". Measured this session: **34 tests, 97.18 %**. Both numbers
are hardcoded prose that drifts. Prefer a pointer to the measuring command over a literal;
`docs/_generated/COUNTS.md` in the template root is *not* a valid target — this is a private
`projects/working/` package and `grep -c bond-manuscript` against that file returns **0**, so the
previous version of this TODO deferred its numbers to a dead reference.

- **Done when:** neither file states a count that a `pytest` run can contradict.
- **Demonstrate:** `grep -n "18 tests\|≥91" README.md AGENTS.md` → no output.

#### D3. `experiment_plan.yaml` and `domain_profile.yaml` declare the optimizer experiment
`experiment_plan.yaml` (whole file) declares step-size conditions
(`conservative_step` / `near_optimal_step` / `aggressive_step`), a primary metric
`objective_value`, `expected_figures: fig:convergence_plot, fig:performance_benchmark,
fig:step_size_sensitivity`, and `expected_tables: tbl:optimization_results`. The compendium has
no experiment, no figures, and no tables. `domain_profile.yaml:1-20` declares
`domain: code_research`, `required_packages: numpy, matplotlib`, and the same three figure types.
Both are read by template validation gates, so they are a live source of false expectations.

`manuscript/layer_contract.yaml` is the same defect: it is headed "Code-centric exemplar" and
allow-lists `src/analysis/_infra.py`, `src/_runtime.py`, and `src/benchmark_support.py` for
infrastructure imports — three files that do not exist here, against a `src/` that imports no
infrastructure at all.

- **Done when:** all three describe the compendium (a manuscript-assembly project with no experiment)
  or are removed as not-applicable.
- **Demonstrate:**
  `grep -rn "convergence_plot\|step_size\|objective_value" experiment_plan.yaml domain_profile.yaml`
  → no output, and `manuscript/layer_contract.yaml` names only paths that exist.

#### D4. Eight of the ten runnable scripts are dead scaffold
Found while rewriting the docs (D1); recorded here rather than fixed, because it is a code change.

Four are unmodified exemplar orchestrators importing modules this fork never had, and fail at
import: `04_benchmark_stage.py` (a `benchmark_support` module), `build_dashboard.py` (a `dashboard`
module), `generate_api_docs.py` (a `documentation` module), `optimization_analysis.py` (an
`analysis` package).

Four are template pipeline stages that compute the template root as
`Path(__file__).resolve().parents[4]`: `00_preflight.py`, `08_connector_search.py`,
`09_provenance_record.py`, `10_research_workflow.py`. That depth was correct at
`projects/<lifecycle>/<project>/`; this package sits one level deeper, so the computed root is
`.../template/projects` and `import infrastructure` raises `ModuleNotFoundError`. Note
`tests/conftest.py` carries the same off-by-one — harmless only because nothing in the suite imports
`infrastructure`.

Only `generate_compendium.py` and `z_generate_manuscript_variables.py` participate in the build.

- **Done when:** the four non-functional scripts are deleted, and the four stage scripts either
  resolve the template root by marker-walk (as `z_generate_manuscript_variables.py` already does)
  or are deleted too.
- **Demonstrate:** every script the package still ships imports cleanly. This currently names
  exactly the eight above; after the fix it must print nothing.

  ```bash
  for s in scripts/*.py; do .venv/bin/python -c "
  import importlib.util, sys
  spec = importlib.util.spec_from_file_location('_probe', sys.argv[1])
  m = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(m)
  " "$s" >/dev/null 2>&1 || echo "FAILS: $s"; done
  ```

---

### Extension — genuine future work

#### E1. The compendium has no figures
`output/` contains no `figures/` directory and no manuscript section embeds an image. The suite
architecture chapter (`compendium.py:424-470`) is tables only. A generated dependency-layer
diagram (Layer 0 → 4 → films) and a coverage/test-count distribution across the 34 gate rows
would both derive from data this package already reads — `gate_manifest.json` and the roster —
and would need no new source of truth.

- **Done when:** at least one deterministic, byte-stable figure is generated by the compendium
  build and embedded in `02_suite_architecture.md`, with a regeneration test asserting
  byte-equality across two runs.

#### E2. Chapter `## Sources` lists every merged key for the package, unfiltered
`generate_compendium.py:75` passes *all* of a package's reference keys into
`build_package_section`, which emits them as one `@key; @key; …` run (`compendium.py:418-420`).
For a package with 30 references that is a 30-citation paragraph attached to a one-paragraph
abstract, with no signal about which sources the abstract actually leans on. Selecting the keys
the imported abstract cites (or capping and grouping) would make the chapters readable — but this
is a design change, not a defect.

---

## Known limitations (not bugs)

- **Local-only, never published.** This tree has no git remote and lives under
  `projects/working/`, which the template's confidentiality invariant keeps untracked in the
  public repo. That is why C1 is a metadata-hygiene item and not a disclosure incident — no
  reader outside this machine sees the false DOI today.
- **Cross-references from package abstracts are destroyed, not resolved.** `_strip_crossrefs`
  (`compendium.py:202-226`) turns `[@sec:results]` into "the results section" and deletes
  `@def:`/`@thm:`/`@fig:` pointers entirely, because those labels exist only inside the source
  package's manuscript. Accepted: the alternative is namespacing every label across 33 manuscripts.
  Pinned by `test_imported_abstracts_carry_no_dangling_crossrefs`
  (`tests/test_compendium.py:390-399`).
- **Token stripping is a legitimate fallback.** When a package ships neither a hydrated abstract
  nor a `manuscript_variables.json`, `import_package_abstract` (`compendium.py:170-195`) strips
  `{{TOKEN}}`s rather than failing. This once silently degraded two chapters to `**** (**)`;
  the mitigation was to widen the variables search (`_VARIABLE_PATHS`, `compendium.py:159`) and
  pin the symptom (`test_no_empty_bold_in_any_imported_abstract`, `:380-387`), not to make the
  fallback fatal — a package legitimately may have no variables.
- **`_brief_line` catches broad `Exception`.** `compendium.py:388` uses a bare
  `except Exception` deliberately: a provider can fail to import for any reason, and the failure
  is **recorded** in `BRIEF_FAILURES` and turned into a non-zero exit by
  `generate_compendium.py:97-108`. This is the fix for a prior silent swallow, not a residue of it.
- **The coverage floor is 90 %, measured on `src/` only.** `scripts/` is not covered by the gate
  (`pyproject.toml:62-70`, fleet-wide convention); the two live orchestrators are exercised
  end-to-end by the subprocess tests instead.
- **The unified bibliography is merged, not curated.** Duplicate works published under different
  keys by different packages survive as separate entries; only exact key collisions are collapsed
  (`compendium.py:341-347`). De-duplicating by DOI/title would need a matching heuristic that can
  silently drop a real citation.
- **Sibling packages and the bond root are out of write scope.** Where a defect originates
  upstream (C2's bare underscores come from `../casino_royale_2006/manuscript/references.bib:154`
  and 18 other package bibliographies), the fix recorded here is the compendium-side one.

---

## Verification

Run from `projects/working/bond/bond-manuscript/`. If `uv` reports
`Failed to initialize cache at /Users/4d/.cache/uv`, re-run the same command outside the sandbox.

```bash
# 1. The gate. Expected: 34 passed, coverage >= 90% (97.18% at time of writing).
uv run pytest tests/ --cov=src --cov-fail-under=90

# 2. Lint + types. Expected: "All checks passed!" and "Success: no issues found in 3 source files".
uv run ruff check src/ scripts/ tests/
uv run mypy src/

# 3. Regenerate the compendium. Expected exit 0 and
#    "compendium written: 33 packages, N references, 27 film chapters, 6 infra chapters".
#    A non-zero exit lists packages whose MissionProvider failed to import.
#    NOTE (C4): this rewrites tracked files under manuscript/.
uv run python scripts/generate_compendium.py

# 4. Hydrate {{TOKEN}}s. Expected: "[bond-manuscript] hydrated 6 tokens -> output/manuscript/".
uv run python scripts/z_generate_manuscript_variables.py

# 5. Render, from the TEMPLATE ROOT (/Users/4d/Documents/GitHub/template).
uv run python scripts/pipeline/stage_03_render.py --project working/bond/bond-manuscript

# 6. Render health. Expected today: 67 pages, 0 "??", but 89 LaTeX errors (see C2).
#    Target after C2: 0 LaTeX errors.
pdfinfo output/pdf/bond-manuscript_combined.pdf | grep Pages
pdftotext output/pdf/bond-manuscript_combined.pdf - | grep -c '??'
grep -c '^! ' output/pdf/_latex_stdout.log

# 7. Fleet gate context (read-only; owned by bond-ops, not by this package).
python3 -c "import json;r=json.load(open('../output/aggregate/gate_manifest.json'))['packages'];print(len(r),'rows',{x['verdict'] for x in r},min(x['coverage'] for x in r))"
```


---

## Round 2 — the compendium carries all 33 FULL manuscripts

Round 2 closed the "abstract-only excerpt" gap: instead of importing just each
package's abstract into its chapter, `compendium.py` now reproduces each
package's **complete manuscript** — abstract plus every authored section
(`01_introduction` … `08_appendix`), token-hydrated from the package's own
`manuscript_variables.json`, with the package's figures carried into the
combined PDF.

### What changed

- **`src/bond_manuscript/compendium.py`**: added `import_package_sections()`
  (imports every numbered content section in order, hydrates tokens, demotes
  headings one level under the chapter header, rewires figure embeds) and
  `ImportedChapter` (body + figures to copy). Rewrote `build_package_section`
  to return the full-manuscript chapter. Package-local pandoc-crossref labels
  (`{#sec:…}`, `{#fig:…}`, `{#tbl:…}`, `[@fig:…]`) are stripped so no duplicate
  `\label{}` can break the combined render; literal token-protocol mentions
  (``{{RESULT_*}}``) are folded to single braces **without touching LaTeX math**
  (a blanket `}}`→`}` rewrite unbalanced `\frac{1}{…}}` and stopped the render).
- **`scripts/generate_compendium.py`**: copies each chapter's figures into
  `output/figures/` under a slug-namespaced filename, and FAILS LOUD (exit 1)
  if a discovered package yields a hollow (<10 line) chapter.
- **Wrapper prose** (`00_abstract.md`, `01_introduction.md`, `90_closing.md`):
  reframed to describe a compendium containing 33 full manuscripts; counts use
  the `{{N_PACKAGES}}/{{N_FILMS}}/{{N_INFRA}}/{{N_GATE_MEASURED}}` tokens; fixed
  the dangling "(in the `Files` section)" pointer (TODO C10).
- **`tests/test_compendium.py`**: rewired for the new signature; added
  `test_every_chapter_carries_full_manuscript` (every 03_/04_ chapter must carry
  Abstract/Introduction/Methodology/Results/Conclusion/Sources and be >60
  lines), structure/math preservation, crossref-attribute hygiene, and
  missing-figure fallback.

### Measured evidence (before → after)

| Metric | Before (round 1) | After (round 2) |
| --- | --- | --- |
| Total generated chapter lines | 528 | 18,671+ |
| `03_01_dr_no.md` lines | 16 | 572 |
| Per-chapter size range | ~16 | 169–365 |
| Combined PDF pages | 67 | **332** |
| Combined PDF size | 396,236 B | **6,341,986 B** |
| Figures carried | 0 | 81 |

Verification: 0 unresolved `{{…}}` in any `output/manuscript/*.md`; all 32
unique package codenames present in `pdftotext` of the combined PDF; 0 `??`
(unresolved refs); every 03_/04_ chapter reproduces the package's full
manuscript (subsections, math, and figures all present).

### Round-2 gates

| Gate | Result |
| --- | --- |
| `uv run pytest tests/ --cov=src --cov-fail-under=90` | **40 passed**, 95.95 % |
| `uv run ruff check src/ scripts/ tests/` | All checks passed |
| `uv run ruff format --check src/ scripts/ tests/` | all formatted |
| `uv run mypy src/` | Success (3 files) |

### Residual (documented, not regressions)

- **Render still logs ~89 non-fatal LaTeX warnings** — the pre-existing C2
  bib-underscore class. The combined PDF builds (batchmode) at 332 pages with
  full content; this matches round 1's 89-error state and is tracked as C2.
- A few full sections cite package-local macros the compendium preface does not
  define (`\Cindex`, `\HHI`, `\Eff`) producing non-fatal `Undefined control
  sequence` warnings — follow-up could strip or define them.
- **Sequencing:** sibling package agents were mid-edit during this run (the
  merged reference count moved 330→340 and a chapter gained content between
  regens). A final fresh regeneration was run at the end, as the handoff
  requires; if a downstream package changed after this commit, re-run
  `generate_compendium.py` + `z_generate_manuscript_variables.py` + render.

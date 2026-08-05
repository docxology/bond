# Testing philosophy

The compendium generator is tested against the real fleet with no mocks. That is
not asceticism — it is the only way to test this package at all. Almost every
function here answers a question about the 33 sibling packages, and a mocked
package tree would test the mock's shape, not the fleet's.

## Why no mocks

`compendium.py` is pure functions over files: give them a directory, get back a
string. There is no network, no clock, no external service, nothing that would
justify substituting a fake. The suite reads the actual packages under
`projects/working/bond/`, and where a case cannot exist in the fleet it builds a
real package tree under `tmp_path`.

Concretely: `test_brief_line_real_provider` loads goldfinger's actual
`MissionProvider` through `bond_api.discovery` and asserts on the codename and
objectives it returns. A mock there would assert that the loader was called,
which is exactly the failure mode that let a provider silently stop importing.

Forbidden anywhere in `tests/`: `unittest.mock`, `MagicMock`, `AsyncMock`,
`create_autospec`, `@patch`, `mocker.patch`. The fleet docs gate parses each test
file with `ast` and fails on a real import — string literals naming those symbols
are not violations, so a test asserting their absence reads clean.

## The suite

One module, `tests/test_compendium.py`, plus `conftest.py`. Coverage map and
per-area test lists: [`../tests/AGENTS.md`](../tests/AGENTS.md). Patterns used in
place of mocks: [`../tests/PATTERNS.md`](../tests/PATTERNS.md).

## Coverage mechanics

`pyproject.toml`:

```toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__init__.py", "*/test_*.py"]

[tool.coverage.report]
fail_under = 90
```

The gate, run from this directory:

```bash
cd projects/working/bond/bond-manuscript
uv run pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=90
```

Branch coverage is on, so a partially-taken branch shows as `456->470` in the
missing column rather than a line number. Those partials are real gaps: they are
the "no gate manifest", "corrupt gate manifest", and "package with no references"
paths. `../TODO.md` tracks them.

## A green exit code is not a pass

Confirm **collected > 0** and a coverage figure in the summary before believing a
run. Two ways this suite can report success while proving nothing:

- **Wrong interpreter.** If `pytest` resolves to an environment without this
  package's dependencies, it collects nothing and exits 0. Check the header shows
  Python 3.14.6 and `plugins: cov-…`. Re-sync with `uv sync --all-extras` — a bare
  `uv sync` prunes pytest.
- **Silent skips.** `test_script_smoke_regen` and
  `test_regeneration_is_deterministic` are skipped when
  `../output/aggregate/gate_manifest.json` is missing. If they skip, nothing is
  checking the generator CLI or byte-stable regeneration. Read the skip count.

## Writing a test here

- Prefer real fleet data. Reach for `tmp_path` only for a case the fleet cannot
  contain.
- Assert observable output, not call sequences.
- Pin the invariant, not today's data. An assertion tied to a placeholder key
  prefix passed for as long as the data stayed fake and failed the moment it
  became real.
- Where a property must hold for every package, loop over all of them and collect
  offenders so the failure names them. Four such sweeps exist; keep them
  exhaustive.
- Clean up `compendium.BRIEF_FAILURES` on both sides if you touch it.

## Checklist

- [ ] No mock framework anywhere in the file
- [ ] Real package directories — the fleet's, or one built with `tmp_path`
- [ ] Assertions on returned text or parsed structure
- [ ] No dependence on filesystem or `set` ordering
- [ ] Module-level state left as it was found
- [ ] Gate re-run; collected > 0 and coverage ≥ 90%

## See also

- [`../tests/AGENTS.md`](../tests/AGENTS.md) — coverage map
- [`../tests/PATTERNS.md`](../tests/PATTERNS.md) — worked patterns
- [`troubleshooting.md`](troubleshooting.md) — interpreter and collection problems
- [`architecture.md`](architecture.md) — why the core is pure

# Test patterns

How `tests/test_compendium.py` gets full coverage of the compendium generator
without a single mock.

## Forbidden

- `unittest.mock`, `MagicMock`, `AsyncMock`, `create_autospec`, `@patch`,
  `mocker.patch`
- Hand-built objects that satisfy a type shape without the real function having
  produced them
- Stubbing a builder so the test asserts against text the test itself wrote

The fleet-wide docs gate (`_phase_docs_gate.py`, run from the bond root) parses
every test file with `ast` and fails on a real mock import.

## Pattern 1 — real fleet data as the fixture

The 33 sibling packages are the fixture. `BOND` is resolved once at module scope
and every real-data test reads from it:

```python
BOND = Path(__file__).resolve().parents[2]
MANUSCRIPT = BOND / "bond-manuscript" / "manuscript"

def test_brief_line_real_provider() -> None:
    line = compendium._brief_line(BOND / "goldfinger", "goldfinger")
    assert "GRAND SLAM" in line
    assert "corner the gold market" in line
```

This loads goldfinger's actual `MissionProvider` through `bond_api.discovery`.
If that package's provider breaks, this test tells you.

## Pattern 2 — `tmp_path` packages for what the fleet cannot show

Some branches have no real-world exerciser: a package with no bibliography, a
corrupt variables JSON, a provider that fails to import. Build a minimal package
tree on disk instead of faking the reader:

```python
def test_import_abstract_survives_corrupt_variables(tmp_path) -> None:
    pkg = tmp_path / "corrupt"
    (pkg / "manuscript").mkdir(parents=True)
    (pkg / "output" / "data").mkdir(parents=True)
    (pkg / "manuscript" / "00_abstract.md").write_text("# Abstract\nValue {{X}} here.")
    (pkg / "output" / "data" / "manuscript_variables.json").write_text("{not json")
    abstract = import_package_abstract(pkg)
    assert "{{" not in abstract and "Value" in abstract
```

Real files, real parse failure, real fallback. The helper `_plain_bib(tmp_path, body)`
does the same for plain-text `[n] …` reference lists — a format still supported
on input even though every package now ships genuine BibTeX.

## Pattern 3 — subprocess for the CLI and for determinism

The generator is exercised by running it, not by importing `main()`:

```python
result = subprocess.run(
    [sys.executable, str(BOND / "bond-manuscript" / "scripts" / "generate_compendium.py")],
    capture_output=True, text=True,
    cwd=str(BOND / "bond-manuscript"), check=False,
)
assert result.returncode == 0, result.stderr
```

Determinism is then checked by reading bytes before, re-running, and asserting
byte-equality of a chapter and of `references.bib`.

## Pattern 4 — assert structure, never a placeholder

`test_parse_references_plain_and_bibtex` once asserted a `goldfinger_ref*` key
prefix. Those keys were placeholders from before the packages carried real
citations; when the citations became genuine the test failed — and it would have
passed forever had the real references never arrived. It now asserts properties
that hold either way:

```python
assert all(r.key and r.bibtex.startswith("@") for r in gold)
assert {r.source_package for r in gold} == {"goldfinger"}
```

Pin the invariant, not the current data.

## Pattern 5 — exhaustive sweeps over the fleet

Where a property must hold for every package, loop over `discover_packages(BOND)`
and collect offenders so the failure message names them:

```python
offenders = []
for pkg in discover_packages(BOND):
    abstract = import_package_abstract(BOND / pkg.slug)
    if "****" in abstract or "(**)" in abstract:
        offenders.append(pkg.slug)
assert not offenders, offenders
```

## Module-level state

`compendium.BRIEF_FAILURES` persists across tests. A test that populates it must
clear its own key on both sides:

```python
compendium.BRIEF_FAILURES.pop("brokenpkg", None)
assert compendium._brief_line(pkg, "brokenpkg") == ""
assert "brokenpkg" in compendium.BRIEF_FAILURES
compendium.BRIEF_FAILURES.pop("brokenpkg", None)
```

## Coverage

```bash
cd projects/working/bond/bond-manuscript
uv run pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=90
```

`pyproject.toml` sets `branch = true` and `fail_under = 90` over `src`. Do not
delete a test to make a number work — cover the branch.

## See also

- [`AGENTS.md`](AGENTS.md) — coverage map and how to add a test
- [`../src/STYLE.md`](../src/STYLE.md) — how the code under test is written
- [`../docs/testing_philosophy.md`](../docs/testing_philosophy.md) — the rationale

# Style guide

Conventions for code, tests, and prose in `bond-manuscript`. Each rule has a
consequence this package has already paid for at least once.

## 1. Import the fact; never retype it

The compendium's whole value is that a film's codename, objectives, abstract, and
citations have exactly one home — that film's package. A chapter that states a
fact the generator could have imported will drift the first time the package
changes, and nothing will notice.

- **BAD**: adding `Mission GRAND SLAM: corner the gold market.` to a chapter.
- **GOOD**: `_brief_line()` loading goldfinger's `MissionProvider` and asking it.

## 2. Zero mocks

No `unittest.mock`, `MagicMock`, `AsyncMock`, `create_autospec`, `@patch`, or
`mocker.patch` anywhere in `tests/`. The generator is pure functions over files;
tests use the real fleet, or a real package tree built under `tmp_path`.

```python
# BAD — asserts the loader was called, which is the bug we had
provider = MagicMock()
provider.brief.return_value = Brief(codename="X", objectives=[])

# GOOD — loads the real provider and asserts what it returned
line = compendium._brief_line(BOND / "goldfinger", "goldfinger")
assert "GRAND SLAM" in line
```

## 3. Compute in `src/`, write in `scripts/`

`compendium.py` returns strings; orchestrators decide where they land. A helper
that both builds and writes cannot be tested without a filesystem fixture, and
will not be tested.

## 4. Failures that cost content must be visible

```python
# BAD — the chapter renders one line shorter and nothing is reported
except Exception:
    return ""

# GOOD — the caller can see what went missing
except Exception as exc:  # noqa: BLE001 — recorded, then reported by the caller
    BRIEF_FAILURES[slug] = f"{type(exc).__name__}: {exc}"
    return ""
```

An empty return means genuine absence — no `mission.py`, no `references.bib` —
and nothing else.

## 5. Deterministic by construction

Roster order and `OrderedDict`, never `set` iteration or `glob` order. No
timestamps or run identifiers in anything written to a file. A change that breaks
this fails `test_regeneration_is_deterministic`, which regenerates and compares
bytes.

## 6. Comments record failures, not narration

```python
# BAD
# Loop over the packages and parse their references.

# GOOD
#: 31 packages use ``output/data/``; bond-cli and bond-ops write
#: ``output/variables/``. Reading only the majority path made those two
#: abstracts import with every token stripped.
```

If a comment would not stop someone from making a specific mistake, delete it.

## 7. Error messages carry the value

```python
# BAD
raise ValueError("bad package")

# GOOD
BRIEF_FAILURES[slug] = f"{type(exc).__name__}: {exc}"
```

Whoever reads the message should not have to open the source to know what went
wrong or which package it was.

## 8. Type hints and docstrings

Complete annotations on every public function; Python 3.10+ union syntax
(`Path | None`); Google-style docstrings that say what comes back rather than how.
Frozen dataclasses for data, module-level `UPPER_SNAKE` for lookup tables,
module-level compiled regexes with a leading underscore.

## 9. Documentation names only things that exist

Before writing a module path, a function name, or a command into any document in
this package, open the file or run the command. This documentation set was
previously 23 files describing a different project's modules, and every gate in
the repository passed while it was wrong. The fleet docs gate now checks it:

```bash
cd projects/working/bond && python3 _phase_docs_gate.py
```

Do not hardcode a test count or a coverage percentage in prose. Name the command
that measures it.

## See also

- [`../src/STYLE.md`](../src/STYLE.md) — source conventions in detail
- [`../scripts/CONVENTIONS.md`](../scripts/CONVENTIONS.md) — orchestrator conventions
- [`../tests/PATTERNS.md`](../tests/PATTERNS.md) — test patterns
- [`syntax_guide.md`](syntax_guide.md) — manuscript markup

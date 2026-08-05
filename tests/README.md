# tests/ — zero-mock suite for the compendium generator

## Quick start

```bash
cd projects/working/bond/bond-manuscript
uv run pytest tests/ -v
uv run pytest tests/ --cov=src --cov-fail-under=90
```

## What is here

| File | Role |
| --- | --- |
| `test_compendium.py` | The whole suite — discovery, abstract import, bibliography merge, section builders, determinism |
| `conftest.py` | Sets `MPLBACKEND=Agg` and puts `src/` on `sys.path` |

Tests run against the real 33-package fleet under `projects/working/bond/`, with
`tmp_path` packages for the cases real data cannot produce. No `unittest.mock`,
no `MagicMock`, no `@patch` — and none is needed, because the generator is pure
functions over files.

Two tests (`test_script_smoke_regen`, `test_regeneration_is_deterministic`) skip
when `../output/aggregate/gate_manifest.json` is absent. Watch the skip count.

## More

[`AGENTS.md`](AGENTS.md) lists what each area covers and how to add a test.
[`PATTERNS.md`](PATTERNS.md) documents the patterns used in place of mocks.

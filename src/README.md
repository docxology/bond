# src/ — compendium generator

Two modules build the PROJECT BOND compendium from the fleet's own manuscripts.

| Module | Role |
| --- | --- |
| `bond_manuscript/compendium.py` | Package discovery, abstract import, bibliography merge, chapter builders |
| `bond_manuscript/manuscript_variables.py` | The compendium's `{{TOKEN}}` map, computed from live discovery |

## Quick start

```python
from pathlib import Path

from bond_manuscript import (
    build_architecture_section,
    build_references_bib,
    discover_packages,
    import_package_abstract,
)

bond_root = Path("..").resolve()                 # the PROJECT BOND workspace root

packages = discover_packages(bond_root)          # 27 films + 6 infrastructure
print(len(packages), packages[0].title)          # 33  Dr. No (1962)

print(import_package_abstract(bond_root / "goldfinger")[:120])

bibtex, references = build_references_bib(packages, bond_root)
print(len(references), "merged bibliography entries")

print(build_architecture_section(packages, bond_root).splitlines()[0])
```

Discovery reads the canon-ordered roster from `bond_coordinator.registry.ROSTER`,
so the suite path dependencies (`bond-api`, `bond-coordinator`, `bond-utilities`)
must be installed — `uv sync --all-extras` from this directory handles that.

## Run the tests

```bash
cd projects/working/bond/bond-manuscript
uv run pytest tests/ --cov=src --cov-fail-under=90
```

## More

[`AGENTS.md`](AGENTS.md) has the full API table, the invariants, and the gotchas
these modules encode. [`STYLE.md`](STYLE.md) covers how to write code here.

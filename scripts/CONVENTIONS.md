# Script conventions

Rules for orchestrators in `scripts/`. The two live examples are
`generate_compendium.py` and `z_generate_manuscript_variables.py`.

## Coordinate, never compute

```python
# CORRECT — the script decides where output goes; src/ decides what it says
from bond_manuscript import build_architecture_section, discover_packages

packages = discover_packages(bond_root)
(manuscript / "02_suite_architecture.md").write_text(
    build_architecture_section(packages, bond_root) + "\n"
)
```

```python
# WRONG — fleet logic in a script cannot be unit-tested
rows = []
for slug in sorted(os.listdir(bond_root)):
    if (Path(bond_root) / slug / "manuscript").is_dir():
        rows.append(f"| {slug} |")
```

If you are parsing a package, resolving a token, or assembling a chapter inside a
script, move it into `src/bond_manuscript/compendium.py` and write a test for it.

## Resolve paths from the file, not the cwd

```python
REPO = Path(__file__).resolve().parents[1]   # -> bond-manuscript/
```

Both active scripts are runnable from any working directory because of this. Do
not reach into the monorepo by fixed depth (`parents[4]` and friends); that
assumption is exactly what left four inherited stage scripts unable to import
`infrastructure` after this package moved one level deeper. When you need the
template root, walk up until you find a marker:

```python
ancestor = REPO
while ancestor != ancestor.parent and not (ancestor / "infrastructure" / "rendering").is_dir():
    ancestor = ancestor.parent
```

## Make suite imports work from a bare interpreter

The renderer may run a script with this package's own `.venv` python. Prepend the
sibling `src/` directories before importing them:

```python
for _dir in (REPO / "src", REPO.parent / "bond-api" / "src",
             REPO.parent / "bond-utilities" / "src",
             REPO.parent / "bond-coordinator" / "src"):
    sys.path.insert(0, str(_dir))

from bond_manuscript import discover_packages  # noqa: E402
```

The `# noqa: E402` on post-`sys.path` imports is intentional; keep it.

## Own your outputs by explicit pattern

A generator that clears its previous run must match exactly what it writes:

```python
_GENERATED_02 = re.compile(r"^02_suite_architecture\.md$")
_GENERATED_PKG = re.compile(r"^(0[34])_\d{2}_.+\.md$")
_GENERATED_99 = re.compile(r"^99_references\.md$")
```

Never `for f in manuscript.glob("*.md"): f.unlink()`. The hand-authored abstract,
introduction, and closing live in the same directory.

## Report failures; do not absorb them

```python
if BRIEF_FAILURES:
    print("\nERROR: could not load MissionProvider for:", file=sys.stderr)
    for slug, err in sorted(BRIEF_FAILURES.items()):
        print(f"  {slug}: {err}", file=sys.stderr)
    return 1
```

Diagnostics go to stderr, the summary line to stdout, and a build that lost
content returns non-zero. Wrap `main()` as `raise SystemExit(main())` so the exit
code actually reaches the shell.

## Determinism

Scripts must produce byte-identical output for an unchanged package tree. No
timestamps, no run IDs, no `set` iteration in anything that reaches a file.
`tests/test_compendium.py::test_regeneration_is_deterministic` enforces this by
re-running the generator and comparing bytes.

## Checklist

- [ ] No fleet parsing or chapter assembly in the script
- [ ] Paths resolved from `Path(__file__).resolve()`, no fixed-depth monorepo reach
- [ ] Output patterns explicit; hand-authored files untouched
- [ ] Failures on stderr and a non-zero exit
- [ ] Output byte-stable across two runs

## See also

- [`AGENTS.md`](AGENTS.md) — what each script writes
- [`../src/STYLE.md`](../src/STYLE.md) — style for the code scripts call
- [`../docs/architecture.md`](../docs/architecture.md) — layer boundaries

# Bond Ops — QUARTERMASTER

*infra package · mission codename QUARTERMASTER*.

This chapter reproduces the package's complete manuscript verbatim:
the abstract and every authored section, token-hydrated from the
package's own manuscript variables, with the package's figures carried
in the combined PDF and its sources resolved against the unified
bibliography.

## Concepts

Fleet inventory, gates, health, provisioning

## Abstract

PROJECT BOND is a **33**-package research suite: **6** infrastructure packages and **27** film packages. This manuscript documents **bond-ops** (*QUARTERMASTER*), the Layer-4 fleet-operations package that keeps the whole fleet measurable and gateable. The QUARTERMASTER owns the canonical suite roster as data, reconciles it against live suite directories, runs per-package quality gates (one package per subprocess), reports per-repo git health, and emits the herdr provisioning roster. Fleet gate results are runtime diagnostics — never hand-authored metrics. The methodology section defines the gates, probes, and formalisms; the results section shows the measured fleet surface; the reproducibility section pins the determinism properties.

## Introduction 

The PROJECT BOND suite (**PROJECT BOND**) comprises **33**
packages: **6** infrastructure packages forming the operational
core (protocol, coordinator, orchestrator, CLI, ops, utilities) and
**27** film packages implementing their respective mission
providers. shows the composition.

::: {.definition #def:suite-roster title="Suite roster"}
The *suite roster* is the frozen, ordered set of the **33** package
slugs — **6** infrastructure and **27** films —
carried as data in `src/bond_ops/inventory.py` and reconciled against live
directories by `inventory.reconcile`.
:::

![Roster composition of PROJECT BOND: 6 infrastructure packages and 27 film packages, totalling 33 packages.](output/figures/bond-ops_roster_composition.png)

The QUARTERMASTER's premise: a fleet this large can only be trusted if it is
inventoried, gated, and provisioned from a single, deterministic vantage
point. `bond-ops` fills exactly that Layer-4 role; the machinery is defined in
the methodology section.

## Methodology 

### Inventory

`src/bond_ops/inventory.py` carries the canonical roster as data
 and reconciles it against the live suite root, flagging
missing or unexpected packages.

::: {.definition #def:inventory-reconcile title="Reconciliation"}
`inventory.reconcile(root)` partitions the roster into `present` (slug
directory exists under `root`), `missing` (roster slug absent), and
`unexpected` (non-hidden directories on disk that are not roster slugs). The
fleet is *complete* exactly when the missing set is empty
.
:::

$$
\operatorname{complete}(r) \iff \operatorname{missing}(r) = \varnothing
$$ 


Beyond presence, the roster is also checked for *identity drift*: every present
film package's declared mission codename — read as data from its own
`mission.py` / config, never by importing a sibling — must equal the matching
27-row roster codename. A film that renames itself (or a roster row
that drifts) fails loudly rather than silently, so the QUARTERMASTER's copy of
fleet identity cannot rot unseen.

### Aggregate gate

::: {.definition #def:aggregate-gate title="Aggregate gate"}
The *aggregate gate* runs the canonical per-package gate — `uv run pytest
tests/ --cov=src --cov-fail-under=90` — **once per package in
its own subprocess**, plus ruff and mypy, and aggregates the verdicts into the
machine-readable `bond-ops-gate` manifest.
:::

::: {.proposition #prop:isolation title="One package per subprocess"}
Gating multiple packages in a single pytest process is forbidden: scaffold
`conftest.py` files mutate `sys.path` and collide. Each package's gate
therefore runs with `cwd` set to that package's own directory, one subprocess
per package.
:::

Coverage is parsed from either the pytest-cov `TOTAL` table or the
`... not reached. Total coverage: X%` failure line. The manifest summarises
measured coverage across the fleet with the mean and extrema of the
per-package values.

$$
\mu = \frac{1}{n} \sum_{i=1}^{n} c_i
$$ 

$$
\min_i c_i \;\le\; c_i \;\le\; \max_i c_i
$$ 

A package's gate verdict is the conjunction of the coverage gate and, when
run, the ruff and mypy checks:

$$
G(p) = \mathrm{pytest}(p) \;\land\; \mathrm{ruff}(p) \;\land\; \mathrm{mypy}(p)
$$ 

The toolchain is standard and pinned via `uv.lock`: [@pytest] drives every
package's tests, [@coveragepy] measures line+branch coverage, [@ruff] lints
and formats, and [@mypy] checks types. and
 visualise a real gate run; lists the
tools.

### Health

::: {.definition #def:health-verdict title="Health verdict"}
A package is *healthy* when it is present, ships all **4**
required files (README / AGENTS / TODO / pyproject), is free of lineage hits,
and has a clean git tree.
:::

$$
H(p) = \mathrm{present}(p) \land \mathrm{files}(p) \land \neg \mathrm{lineage}(p) \land \mathrm{clean}(p)
$$ 

Git state is read from `git status --porcelain` and reduced by a pure parser
(`health.parse_porcelain`) into modified and untracked counts; the clean
predicate is exactly "both counts are zero". Branch, short SHA, and
ahead/behind-upstream distances are recorded alongside, with ahead/behind
reported as *undefined* rather than zero when no upstream is configured — the
normal case in this local-only suite.

::: {.proposition #prop:probe-additivity title="Probes are additive, not verdict-changing"}
The layout probes (`health.probe_layout`: `[project] name` equal to the slug,
`tests/` present, `src/` present) and the toolchain probe
(`health.tool_versions`) are reported alongside the health verdict but are
deliberately **not** folded into $H(p)$ of. A package
whose pyproject name has drifted from its slug is a silent fork hazard worth
surfacing, but folding a new condition into the verdict would retroactively
change the contract that downstream consumers of `ops health --json` read.
Diagnostics widen; verdicts do not move.
:::

### Command surface

::: {.definition #def:ops-surface title="The `ops` surface"}
`bond_ops.cli` exposes **4** subcommands — `inventory`,
`gate`, `health`, `roster` — each with a human-readable form and a `--json`
form emitting a versioned manifest. The gate overrides `--pytest-cmd` /
`--ruff-cmd` / `--mypy-cmd` each accept a single shell-tokenized command
(parsed with `shlex.split`), so a value containing `-`-prefixed arguments —
e.g. `uv run pytest tests/ -q` — is usable; a test drives one through the CLI
and asserts the `-`-prefixed token reached the subprocess. Exit codes: `0` on success, `1` when a
`gate` verdict fails, `2` on usage error (unknown slug, negative `--limit`).
Every default is read-only; only `roster --execute` starts anything.
:::

### Visualization

`bond_ops.figures` renders the manuscript figures headlessly (Agg backend, no
display) from canonical data and real reports: from
the frozen roster constants, from a real health sweep, and
 / from a real gate report. Colours
come from a colourblind-safe palette [@wong2011] and the plotting is done with
Matplotlib [@matplotlib]. Because the inputs are fixed and no wall-clock or
random draw enters the render path, the PNG bytes are reproducible for a given
fleet state.

### Provisioning

::: {.definition #def:provisioning-roster title="Provisioning roster"}
The *provisioning roster* maps each package to a herdr provisioning recipe —
`workspace create` (capturing the root pane id), `agent start` in that pane
with a `90000` ms interactivity timeout, and a
fire-and-forget `agent prompt` when a mission brief file exists. Rendering is
pure and read-only; execution requires an explicit `--execute`.
:::

`provision.roster_report` serialises the same roster as a versioned JSON
manifest — totals by kind and by prompt-brief coverage, then one record per
package — so fleet composition can be diffed mechanically rather than read out
of a shell script.

See the results section for the measured fleet surface and the setup section for the
experimental setup.

## Results 

The fleet surface produced by bond-ops (codename QUARTERMASTER) is the
**4**-subcommand `ops` surface of, all
measured from real subprocess and filesystem state:

- **Inventory.** `ops inventory` reconciles the canonical roster
 against `projects/working/bond/` and reports present,
 missing, and unexpected directories. A complete fleet shows `present
 33/33 · missing 0 · complete True`
; the verdict is rendered as the Python boolean it
 is, and a test binds this quoted line to the CLI's real output.
- **Fleet identity.** Every present film package's declared mission codename
 is cross-checked against the roster as data; the coherence test fails loudly
 on a rename or drift, so the QUARTERMASTER's copy of the 27-film
 roster matches what the fleet actually declares.
- **Aggregate gate.** `ops gate --json` emits a deterministic
 `bond-ops-gate` manifest containing, for each
 package, its presence, pytest pass/fail, measured coverage, ruff and mypy
 verdicts, and the summary totals with coverage min/mean/max over the
 90-floor gate (,
 ). `ops gate` (human form) prints a per-package table; the
 exit code is `0` iff every present package passes.
- **Fleet health.** `ops health` reports per-repo clean/dirty, branch,
 ahead/behind, required-file coverage, lineage hits, layout probes, and the
 overall verdict; `--json` exposes `probes` and
 `layout_ok` per package as diagnostics that never move the verdict
. shows a real sweep over the
 whole fleet.
- **Provisioning roster.** `ops roster` prints the herdr provisioning script;
 `ops roster --json` emits a machine-readable roster report
; `ops roster --execute` runs it against the
 herdr daemon.

The gate manifest schema (version 1) is summarised in.

| Field | Type | Meaning |
|---|---|---|
| `manifest` | string | manifest identifier (`bond-ops-gate`) |
| `schema_version` | integer | schema version (1) |
| `generated_by` | string | fleet identity (`QUARTERMASTER`) |
| `suite` | string | suite name (`PROJECT BOND`) |
| `summary` | object | totals (present / passed / failed / missing) + coverage measured / mean / min / max |
| `packages` | array | per-package verdict objects (presence, pytest / ruff / mypy, coverage) |
: The `bond-ops-gate` manifest schema, version 1. 

![Fleet health across the whole roster: one row per package, green = healthy, red = unhealthy, grey = missing.](output/figures/bond-ops_fleet_health.png)

![Measured gate coverage with the 90% floor reference line.](output/figures/bond-ops_gate_coverage.png)

![Aggregate gate verdict heatmap (pytest / ruff / mypy / passed).](output/figures/bond-ops_gate_verdicts.png)

Because the manifest carries no wall-clock timestamp and asks only real
processes for their verdicts, re-running `ops gate` against an unchanged fleet
yields an identical manifest — a live determinism check
.

## Conclusion 

**bond-ops** (*QUARTERMASTER*) delivers the fleet-operations surface of
PROJECT BOND: a canonical roster, aggregate gates that
respect one-package-per-subprocess isolation, per-repo
health inspection, and a safe, read-only provisioning
path. Together these make a **33**-
package suite measurable and maintainable from a single QUARTERMASTER vantage
point.

## Experimental Setup 

- **Runtime.** Python ≥3.12 (the lowest exercised floor; the toolchain is
 standard library + `subprocess` + `pyyaml` + `matplotlib` (figures only). No
 `infrastructure.*` and no sibling BOND import.
- **Gate command** invoked per package (one subprocess each): `uv run pytest
 tests/ --cov=src --cov-fail-under=90`, killed after
 600 s so a hung package cannot stall the sweep (the timeout is
 recorded as a gate failure with its exception text, never as a pass).
- **Fleet root**: `PROJECT BOND` at `projects/working/bond/`,
 33 packages (6 infra, 27 films).
- **Isolation contract**: each gate subprocess runs with `cwd` equal to the
 package's own directory; never all packages in one pytest process
.
- **Figures**: rendered headlessly (Agg) into `output/figures/` by
 `scripts/z_generate_figures.py`, byte-deterministic for fixed inputs.

The toolchain is pinned via `uv.lock`.

| Tool | Role |
|---|---|
| pytest | test framework for every fleet package gate |
| pytest-cov | line+branch coverage at the 90% floor |
| ruff | lint + format in the aggregate gate |
| mypy | static type check in the aggregate gate |
| uv | environment + lockfile management |
: The QUARTERMASTER toolchain. 

The package's own test suite exercises the real subprocess machinery against
deterministic tmp-path fake packages (and a fake `uv`/`herdr` on `PATH`), with
zero mocks, and must hold ≥90% line+branch coverage on `src/` (enforced by
`--cov-fail-under=90` and the pyproject `fail_under`). A
dedicated real-fleet test module additionally runs the gate runner and the
health/layout probes against the live sibling packages under
`projects/working/bond/`, giving the QUARTERMASTER an end-to-end gate it can
trust on the fleet it operates.

## Reproducibility 

::: {.proposition #prop:manifest-determinism title="Manifest determinism"}
Gate manifests and manuscript variable maps embed no wall-clock timestamp, so
for an unchanged fleet they are byte-identical across runs. The one place a
clock reading can enter is the free-text `error` excerpt captured from a
failing package's own test output (pytest ends its summary with `1 failed in
0.10s`); elapsed-time readings are redacted from that excerpt before it is
persisted, which is what extends the property from a passing fleet to a
failing one.
:::

bond-ops is engineered to be deterministic and reproducible:

- **Fixed roster data.** The 33-package roster (6
 infra + 27 films) is a frozen, ordered data structure in
 `src/bond_ops/inventory.py`; order never varies across runs or platforms
.
- **No wall-clock in persisted artifacts.** Gate manifests and manuscript
 variable maps embed no timestamps; for an unchanged fleet they are
 byte-identical across runs.
- **Real subprocess, real files.** Every gate, git inspection, lineage sweep,
 and provisioning execution reads actual `subprocess` output and actual
 files — there is no mock or simulated state.
- **Determinism tests.** The test suite pins coverage parsing, manifest
 shape, roster order, provisioning script text, and figure bytes. The
 cross-run claim is checked by running the gate *twice* — two separate live
 invocations, each spawning its own real test subprocess against the same
 on-disk fleet — and diffing the two payloads, at both the module and the CLI
 surface. The CLI-level check runs against a package whose test output stamps
 a **different** elapsed time on every invocation, so the assertion fails if
 any clock reading survives into the manifest; it is not satisfied by
 serializing one report twice.
- **Recovery paths are tested, not assumed.** The three places where
 bond-ops degrades instead of raising — a malformed
 `manuscript/config.yaml`, a corrupt generated token file, and a gate
 subprocess that times out or cannot be launched — each carry a test that
 drives the real failure and asserts the fallback, so a silent-failure path
 cannot rot unobserved behind a coverage exclusion.
- **Filters cannot silently widen.** `--limit 0` gates nothing and a negative
 limit is a usage error, so a mistyped bound can never expand into a
 full-fleet run.
- **No untracked randomness.** No `random` draws; nothing depends on
 wall-clock ordering.

## Scope and Related Work 

### Scope

bond-ops covers fleet *operations* only: knowing the
33-package roster, gating each package
, inspecting health, and
rendering provisioning. It does **not** dispatch
multi-package missions (that is `bond-orchestrator`) and does **not** provide
the user-facing front door (that is `bond-cli`). Its gate runs each package's
*own* tests; it never executes another package's mission logic.

Crucially, bond-ops ships **no `mission.py` and no `MissionProvider`
implementation**, and this is a design decision rather than an omission. The
`MissionProvider` protocol is *defined* by `bond-api` and *implemented* by the
27 film packages, each of which answers `brief` / `recon` / `plan`
/ `execute` / `debrief` for its own film. A mission provider is a thing the
fleet *runs*; the QUARTERMASTER is the thing that *measures whether the fleet
can be run at all*. Making the gate runner itself a mission provider would put
the measuring instrument inside the population it measures — the aggregate
gate would then have to gate itself as a peer, and a provider failure would be
indistinguishable from a gate failure. `bond-ops` therefore imports nothing
from `bond-api` and treats every package, film or infrastructure, purely as a
directory with tests, a git tree, and a layout to probe.

### Related work within the fleet

- **bond-coordinator (MISSION CONTROL)** maintains the film-package registry
 and mission ledger. bond-ops currently carries the roster as mirror
 data; an integration point is recorded in `TODO.md` to consume
 `bond_coordinator.registry.ROSTER` for film metadata once the coordinator
 ships as a dependency, with the acceptance criterion that the reconciled
 slug set stays identical to the canonical 33.
- **bond-cli (THE FRONT DOOR)** may consume the gate manifest produced here
 to surface fleet status to an end user.
- **bond-api (THE PROTOCOL)** defines the protocol the film packages
 implement; bond-ops does not depend on it, but a film package fails
 the aggregate gate if it stops meeting protocol-backed tests.

### External dependencies

The fleet's toolchain is standard and versioned via
`uv.lock`; the manifest schema and CLI surface are the
stable interfaces documented in `docs/`.

## Limitations and Uncertainty 

### Scope of a gate verdict

A 90% line+branch floor is a *necessary*, not a *sufficient*,
condition for correctness. A package whose own suite passes can still be wrong
where its tests do not look: the QUARTERMASTER reports that each package held
its own gate, not that the gate is a proof. This is why measured counts live in
`docs/_generated/COUNTS.md` as receipts rather than being folded into manuscript
prose (the reproducibility section).

### Verdicts are narrower than their diagnostics

`HealthReport.healthy` deliberately excludes the layout
probes: a package with a clean tree and all
4 required files is `healthy` even if its `[project] name`
has drifted from its slug, because folding the probe in would change the
verdict contract downstream consumers read. The drift is surfaced as
`layout_ok=False`, but that is a diagnostic, not a verdict — a reader who wants
"identity is correct" must inspect `layout_ok`, not `healthy`.

### Fleet identity is a reflection, not a ground truth

The roster and each film's mission codename are
cross-checked as data against every present film package's own declaration.
That declaration is read from source and config files and can itself be stale:
the coherence test catches a film that renamed itself without updating this
roster, but cannot catch a film whose *own* source declares an outdated
codename. The check is only as fresh as the packages it reads.

### Determinism has a same-environment scope

Gate manifests are byte-identical for an unchanged fleet, but figure bytes are deterministic *within a pinned environment*:
changing the matplotlib/font stack can move PNG bytes even for identical inputs.
The figure guarantee is therefore reproduced under a fixed toolchain rather than
claimed unconditionally across every platform.

### The suite is not portable to a root-run environment

One health probe reaches its unreadable-file branch with a real `chmod 000`
file; a root user can read such a file, so under root that branch would go
unexercised and the test fails loudly instead of silently dropping coverage
(see `tests/test_health.py`). This is honest scoping, recorded so a later pass
does not mistake it for a gap: the suite is operated as a non-root user.

### No wall-clock, by design

Persisted artifacts carry no timestamp, which is what makes byte-identical
re-runs meaningful, at the cost that a reader cannot tell *when* a manifest was
produced from the artifact alone. Toolchain versioning comes from the `uv.lock`
pin, not from a clock in the file.

### Remaining drift risk: the coordinator registry

bond-ops carries the roster as its own data rather than consuming a
shared registry. When `bond-coordinator` publishes a machine-readable export, a
mismatch must be treated as *fleet drift*, not resolved by picking a winner.
That integration point, and the current codename divergence from the
coordinator's provisional registry, are tracked in `TODO.md`.

## Sources

@bond_ops; @pytest; @coveragepy; @ruff; @mypy; @matplotlib; @wong2011


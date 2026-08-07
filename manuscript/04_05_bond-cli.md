# Bond CLI — THE FRONT DOOR

*infra package · package codename THE FRONT DOOR*.

## Concepts — THE FRONT DOOR: domain and operational focus

Unified terminal front door (bond list/brief/…/run/status/gadgets)

## Abstract — THE FRONT DOOR: mission summary

bond-cli (version 3.0.0, codename THE FRONT DOOR) is the Layer-4 terminal front door of the PROJECT BOND suite — a fleet of 27 film packages plus shared mission infrastructure, each film package implementing the frozen `MissionProvider` protocol. As the front door, bond-cli is a thin dispatch layer: it routes 12 verb-first commands — list, brief, recon, plan, execute, debrief, run, status, gadgets, missions, whois, roster-export — to the 4 built sibling layers (bond-utilities, bond-api, bond-coordinator, bond-orchestrator) and maps their outcomes to deterministic exit codes. It implements no mission logic and ships no `MissionProvider` of its own; every command either loads a real film provider through the frozen `bond-api` discovery contract or delegates to the coordinator's registry and the orchestrator's runner. The deepened surface adds machine-readable `--json` output on 4 commands (list, status, missions, whois), a JSON roster export, color-safe aligned tables that never emit ANSI, and reconciliation of the fleet's measured gate manifest onto the registry so that reported status and coverage are measurements rather than intentions.

## Introduction — THE FRONT DOOR: mission framing, the operational problem, and how to read this chapter

PROJECT BOND is a serious special-agent software fleet: 27 film packages, each faithful to a film's central idea and implementing the frozen `MissionProvider` protocol, plus shared infrastructure — `bond-api` (the protocol + discovery + registries), `bond-coordinator` (mission control: registry, ledger, status, situation room), `bond-orchestrator` (the DAG mission runner with checkpoint/resume and provenance), and `bond-utilities` (Q-branch primitives and mission IO).

A fleet of that shape has an interface problem. Each film package is standalone by construction — its own repository, its own tests, its own manuscript — so an operator who wants to ask *what does this film do, is it built, does its mission pass* would otherwise need 27 entry points and as many local conventions. bond-cli is the answer to that problem: the one surface an operator talks to.

Its role, `THE FRONT DOOR`, accepts a verb and a target. `brief`/`recon`/`plan`/`execute`/`debrief` walk a single film through the protocol's five stages; `run` executes a canned multi-package mission through the orchestrator; `list`, `whois`, and `roster-export` report the fleet from the coordinator registry; `status` renders the suite snapshot; `missions` enumerates what `run` can be given; and `gadgets` inspects the gadget payloads a film registers. The full command set is list, brief, recon, plan, execute, debrief, run, status, gadgets, missions, whois, roster-export.

Two design commitments shape everything that follows. First, **thinness**: argument shaping, provider loading, output formatting, and exit-code mapping live here, and nothing else does. The front door cannot drift from the layers it fronts because it implements none of their logic — it ships no `MissionProvider` and no mission mathematics. Second, **measurement over intention**: where the fleet has actually been gated, `status`, `whois`, and `roster-export` report the measured result rather than the registry's declared state, and they say plainly when no measurement exists.

## Methodology — THE FRONT DOOR: the analytical models and algorithms that drive the mission

### Thin dispatch over built layers

`src/bond_cli/dispatch.py` builds an argparse surface whose 12 commands are:

 list, brief, recon, plan, execute, debrief, run, status, gadgets, missions, whois, roster-export

That tuple, `COMMANDS`, is the single source of the command surface: it drives help ordering, the manuscript token above, and the ledger row that the test suite re-derives. Two sibling tuples do the same job for the rest of the surface — `JSON_COMMANDS` (list, status, missions, whois) names the commands accepting `--json`, and `DEPENDENCY_LAYERS` names the 4 built siblings (bond-utilities, bond-api, bond-coordinator, bond-orchestrator) in dependency order. No count in this manuscript is written by hand; each is derived from the tuple or registry it describes.

`load_film(slug)` uses the FROZEN `bond_api.discovery.load_provider` contract, searching the fleet directory (`projects/working/bond/<slug>/src`) and bond-api's reference `films/` directory, so a single code path serves both the 27 built films and the reference film. Only directories that exist are passed to discovery, because the contract validates every search path it is given. A missing or malformed film raises a `CliError`, which the CLI turns into exit code 1.

### Per-command delegation

- **`list`** — reads the coordinator registry `ROSTER` and prints all 27 films in canonical order (rank, slug, title, year, codename).
- **`brief`/`recon`/`plan`/`execute`/`debrief`** — load the named film's `MissionProvider` and call the corresponding protocol stage. `debrief` runs the full five-stage flow through `bond_api.protocol.run_mission`. `execute`/`debrief` exit 0 iff the outcome reports success.
- **`run`** — resolves a canned mission by name from `bond_orchestrator.missions` (there are 3: OPERATION_DIAMOND, OPERATION_OMNIBUS, OPERATION_SINGLET), binds each package id to its real film provider via `film_providers.load_film_providers` (falling back to the orchestrator's built-in deterministic provider when a film is not built), executes it with the `MissionRunner`, prints the consolidated debrief, and exits 0 iff every verdict passes.
- **`status`** — reads the aggregate gate manifest written by the fleet gate runner (`output/aggregate/gate_manifest.json`) when present, reconciles each film's measured status/coverage onto the coordinator registry, and renders the suite snapshot (counts by status, coverage summary, blocked packages). Without a manifest it falls back to the honest pre-measurement registry.
- **`gadgets`** — builds a `bond_api.GadgetRegistry` by discovering each film's
 gadgets across every fleet convention (`register_gadgets(registry)`, zero-arg
 `register_gadgets`, module-level `GADGETS` dict or factory, a module-level
 `GadgetRegistry`, or provider-bound registration at construction), and prints
 the registered gadget names, for one film or the whole fleet. The three
 single-film outcomes are now distinguished: an **unknown slug** raises a
 `CliError` (stderr, exit 1) with the same "not available" wording as
 `brief`/`plan`; a **built film whose import or hook raises** is diagnosed to
 stderr (naming the exception) while still contributing `0` so a whole-fleet
 sweep never aborts; and a **clean film with no gadgets** keeps the
 empty-lookup message. All failure text goes to **stderr**, so a caller piping
 stdout into a parser never receives error text as data.
- **`missions`** — lists the orchestrator's 3 canned missions and each mission's package chain.
- **`whois <film>`** — prints a film's registry identity (rank, film, year, codename, status, coverage, concepts), whether its provider module is built on disk, and its measured gate state when the manifest carries a row for it.
- **`roster-export`** — exports the fleet roster as key-sorted JSON (the measured roster when the manifest exists, else the plain registry), to stdout or to a file with `--output`.

### Reconciling measurement onto the registry

The registry records what each film package *declares*; the aggregate gate manifest records what the fleet gate *measured*. Three functions keep the two apart and then combine them honestly.

`_manifest_rows` reads the manifest into rows keyed by slug and returns nothing at all when the file is absent, unreadable, or malformed — a broken manifest degrades the front door to registry-only reporting rather than failing a command. `_measured_coverage(row)` extracts a coverage percentage, treating a measured `0.0` as a real measurement (only a missing or non-numeric value is unknown; booleans are rejected, since `bool` subclasses `int` in Python). `_reconcile(record, row)` overlays one row onto one registry record, marking the package ready iff its gate returned `0` and red otherwise.

Composing these over the roster gives the measured view. A film with no row keeps its registry record untouched, because a manifest may cover only part of the fleet — and `whois` reports a measurement for such a film as `null` rather than echoing the registry's declared status as though it had been observed. The distinction matters: a front door that reports intentions as measurements is worse than one that reports nothing.

### JSON output and color-safe tables

list, status, missions, whois accept `--json` for machine-readable output; `roster-export` is JSON by construction and therefore takes no flag. All JSON is emitted with sorted keys and contains no wall-clock field, so two runs against an unchanged fleet are byte-identical.

Human tables are rendered by `src/bond_cli/table.py::format_table` with fixed-width column padding only — never ANSI escape codes. That is the color-safe contract: identical bytes in a terminal, a pipe, a log file, and test capture, and no escape sequences leaking into anything a downstream tool parses. Widths derive from the header and cell text; no cell is truncated or wrapped, so no information is lost to formatting.

### Determinism and exit codes

Film providers are fixed-seed and side-effect free, output ordering is canonical (roster order, sorted result keys), and no command persists wall-clock data. Exit codes: 0 success, 1 command failure (unknown film, non-passing execute/debrief/run, empty or broken gadget lookup), 2 argparse misuse and unknown mission name. `main` catches only its own `CliError`; any other exception is a genuine defect and propagates rather than being flattened into a misleading exit code.

Gadget-hook arity is read from `inspect.signature` [@pythoninspect] rather than guessed by catching `TypeError` on a registry call. That closes a subtle failure mode: a `register_gadgets(registry)` hook whose *body* raised `TypeError` was previously re-invoked as a zero-arg hook, escaping a second, misleading `TypeError: missing 1 required positional argument` that aborted the whole-fleet sweep and masked the film's real defect. With arity from the signature, a hook-body exception is caught per-film, diagnosed to stderr, and the sweep continues.

## Results — THE FRONT DOOR: measured outcomes, headline numbers, and what they establish

### The delivered surface

bond-cli exposes 12 commands over the 4 built layers, all produced by real delegation:

- **`bond list`** prints the full 27-film roster from the coordinator registry, in canonical order (`--json` for rows).
- **`bond brief <film>`** / **`bond recon <film>`** / **`bond plan <film>`** / **`bond execute <film>`** / **`bond debrief <film>`** exercise a real film provider end-to-end: the brief's identity, the recon's findings, the plan's steps, the executed outcome with provenance, and the debrief's lessons.
- **`bond run <mission>`** executes any of the 3 canned orchestrator missions (OPERATION_DIAMOND, OPERATION_OMNIBUS, OPERATION_SINGLET) over the real film providers, with deterministic fallback for films not yet built, and prints the consolidated debrief; exit 0 iff all verdicts pass.
- **`bond status`** reports the suite snapshot — counts by status, the coverage summary, blocked packages — reconciled against the measured gate manifest when present (`--json` for a key-sorted snapshot).
- **`bond gadgets`** lists which films register gadgets and the gadget names each exposes, across every fleet registration convention.
- **`bond missions`** lists the canned missions and their package chains (`--json` for rows).
- **`bond whois <film>`** prints one film's registry identity, built-on-disk state, and measured gate state (`--json` for a payload).
- **`bond roster-export`** emits the fleet roster as key-sorted JSON (stdout or `--output FILE`).

Of these, 4 accept `--json` (list, status, missions, whois); `roster-export` is JSON by construction.

### Measurement is distinguishable from declaration

The reconciliation results are worth stating separately, because they are the front door's only non-trivial computation. Against a full manifest, every film reports its gate verdict and measured coverage. Against a *partial* manifest, films with rows report measurements and films without rows report `measured: null` while retaining their declared registry status — the two are never conflated. Against a malformed or absent manifest, every command still succeeds and reports the registry view, flagged `measured: false`; the human status prints `min=N/A max=N/A mean=N/A` rather than a literal `None%`. A gate row of `0.0` coverage survives as `0.0`, not as "unknown": a package measured at zero has been measured.

### Determinism

Because every command delegates to a frozen, deterministic layer and prints canonical output — roster order, sorted JSON keys, no wall-clock field anywhere — repeated invocations against an unchanged fleet are byte-identical. That property is a live determinism check on the layers beneath: if a film provider ever became seed-dependent, the front door's own output would stop reproducing.

### Verification

The suite is zero-mock: real providers, real importable film packages written to temporary directories, real gate manifests, and real subprocess invocations of the `scripts/` entry points. The live test count and the measured `src/` coverage percentage are recorded in `docs/_generated/COUNTS.md` and re-measured by the gate `uv run pytest tests/ --cov=src --cov-fail-under=90`; this manuscript deliberately quotes neither figure, so no prose here can go stale against the measurement. Every count it does quote — commands, JSON commands, layers, films, missions — is injected from the registry that defines it, and `data/claim_ledger.yaml` records the same values with their sources, re-derived on every test run.

Two of the claims above are not established by coverage and are therefore pinned by dedicated mutation-checked tests. The exit-code contract (0 iff the underlying execute/debrief/run passed) is implemented as a conditional expression, for which coverage.py emits no branch arc: replacing all three with an unconditional `return 0` left the entire suite green, because no test drove a *failing* mission. It is now driven by real film packages whose `execute` genuinely reports failure, each paired with a passing positive control. The sorted-JSON-keys contract was similarly invisible, since every assertion parsed the output back into a dictionary and discarded key order; it is now asserted against the raw emitted text with each handler's literal construction order pinned, so the assertion cannot pass by coincidence. Both tests were validated by applying the corresponding mutation to `dispatch.py` and confirming they go red; the mutation table is recorded alongside the measurement in `docs/_generated/COUNTS.md`.

A third class of claim is bound by *repeatability* rather than coverage: the determinism guarantees in `06_reproducibility.md`. `status --json` and `roster-export` are invoked twice in separate subprocesses and asserted byte-identical, so a `generated_at: time.time` field — executed, fully covered, and invisible to coverage — turns the suite read as a determinism regression. The installed `bond` console script (declared in `pyproject.toml`) is exercised in a subprocess and its stdout/exit code asserted equal to the `scripts/bond.py` bootstrap, so a mistyped entry-point target in `pyproject.toml` fails the suite. And the three mechanically checkable `cross_cutting` rules in `manuscript/layer_contract.yaml` — no `infrastructure.*` imports, no wall-clock calls, no terminal-width/environment reads — are asserted against the `src/` and `scripts/` trees, so adding `import time` to `dispatch.py` fails the suite instead of silently falsifying the manuscript.

### The derived surface (bound to the live token map)

The counts this front door reports are never hand-typed into prose. Every one is produced from the registry or tuple that owns it by `src/bond_cli/manuscript_variables.py`, persisted to `output/variables/manuscript_variables.json` by `scripts/z_generate_manuscript_variables.py`, and re-derived on every test run:

| Quantity | Live value |
|---|---|
| Films in the coordinator roster | 27 |
| Front-door subcommands | 12 |
| Subcommands accepting `--json` | 4 |
| Built sibling layers delegated to | 4 |
| Canned orchestrator missions | 3 |

Each placeholder in the table above is regenerated from the live coordinator `ROSTER`, the orchestrator `MISSION_NAMES`, and `dispatch.COMMANDS` / `JSON_COMMANDS` / `DEPENDENCY_LAYERS`; the values cannot drift from the engines they count. `data/claim_ledger.yaml` records the same five quantities against the same five source symbols, and `tests/test_hardening.py::test_claim_ledger_matches_its_sources` re-derives them.

### Limitations and uncertainty

- **Coverage proves execution, not verification.** A conditional expression (`return 0 if ok else 1`) emits no branch arc, so high line+branch coverage can coexist with a completely unverified non-zero path — that is exactly how both headline contracts were once fully "covered" and entirely unbound. The mitigation is zero-mock contract tests that drive the *failing* path and are mutation-validated (see above), not the coverage number itself.
- **Gadget discovery is best-effort by contract.** A film that fails to import, or whose hook body raises, contributes `0` and emits a diagnostic to stderr — the whole-fleet `bond gadgets` sweep must never be aborted by one broken film. The cost is that gadget coverage for the fleet is only as healthy as the individual films' hooks; the front door reports the exception, it does not repair the film. This package does not install a film's scientific dependencies (e.g. `die_another_day` needs `scipy` and is not importable here), which is correct — the front door depends only on the four built layers — even though it means one film realistically shows as gadget-broken in this environment.
- **`format_table` assumes rectangular input.** A row shorter than the header raises `IndexError`; a row longer is silently truncated to the header width. Every call site builds matched-width rows by construction and no public surface accepts user-supplied rows, so this is an unvalidated internal precondition rather than a reachable defect — but it would be the right place to add a guard if the front door ever grew a free-format command.
- **The measured gate is a snapshot, not a promise.** `status`, `whois`, and `roster-export` report the aggregate gate manifest as last written by the fleet runner. A stale or absent manifest degrades to the declared registry view, flagged `measured: false`; the front door reports the manifest honestly and does not try to re-measure the fleet itself.
- **Determinism is inherited, not re-derived.** The byte-identical repeat runs pass because the layers beneath are deterministic and the front door introduces no randomness, wall-clock, or unordered output. If a film provider ever became seed-dependent, the front door's output would stop reproducing and the determinism tests above would turn red — but they would flag the *symptom*, not pinpoint the film.

## Conclusion — THE FRONT DOOR: findings, verdict, and what the mission establishes

bond-cli gives the operator of the PROJECT BOND fleet a single, reliable terminal: 12 verbs in one grammar over the 4 built layers, real film providers loaded through the FROZEN contract, orchestrator missions run to a consolidated debrief, and a status surface that reports what the fleet gate actually measured. Its guarantees are the ones a front door must provide — thinness (no duplicated logic, no `MissionProvider` of its own), correctness through delegation, honesty about what has and has not been measured, and determinism (canonical output, sorted JSON keys, fixed seeds, no wall-clock state).

The design bet is that a front door earns its keep by being boring. Every capability stays where it was built; nothing is reimplemented one layer up for convenience. What bond-cli adds is uniformity — one grammar, one exit-code contract, one output format that pipes cleanly — and the discipline that keeps that uniformity true: every number it reports is derived from the registry that owns it, and every claim it makes is exercised against a real provider rather than a stand-in.

## Experimental Setup — THE FRONT DOOR: canonical scenarios, parameters, and configuration

- **Runtime.** Python ≥3.10; the 4 built layers (bond-utilities, bond-api, bond-coordinator, bond-orchestrator) wired via `[tool.uv.sources]` path sources, plus NumPy (film providers load it at import time) and PyYAML (manuscript config).
- **Entry points.** Console script `bond` (`bond = "bond_cli.dispatch:main"`) and the thin `scripts/bond.py` bootstrap — identical dispatch, both returning the same exit codes. Both are exercised: the console script by a subprocess smoke test that asserts its stdout/exit code equal the bootstrap's, the bootstrap by the `test_scripts_smoke.py` suite.
- **Film discovery.** `bond_api.discovery.load_provider` over `<slug>/src` (fleet layout) and `bond-api/films` (reference layout), FROZEN contract; only existing directories are offered to it.
- **Mission execution.** `bond_orchestrator.runner.MissionRunner` over real film adapters, with the orchestrator's built-in deterministic provider as fallback for films not yet built on disk.
- **Measured fleet state.** The aggregate gate manifest at `<bond root>/output/aggregate/gate_manifest.json`, written by the fleet gate runner. Absent, unreadable, or malformed ⇒ registry-only reporting; the tests pin this path at a temporary file so no result depends on whether the workspace currently holds a manifest.
- **Output layer.** `src/bond_cli/table.py::format_table` for color-safe aligned tables (no ANSI); JSON output follows RFC 8259 [@rfc8259], is key-sorted, and never embeds wall-clock values.
- **Token hydration.** `scripts/z_generate_manuscript_variables.py` → `src/bond_cli/manuscript_variables.py` → `output/variables/manuscript_variables.json`; identity from `manuscript/config.yaml`, counts from the live registries.
- **Toolchain** (dev extras): `pytest`, `pytest-cov`, `ruff`, `mypy`, `types-PyYAML`.
- **Gates.** `uv run pytest tests/ --cov=src --cov-fail-under=90` (line + branch), `uv run ruff check src/ scripts/ tests/`, `uv run ruff format --check src/ scripts/ tests/`, `uv run mypy src/ scripts/`. Measured results are recorded in `docs/_generated/COUNTS.md`, not in this prose.
- **Tests.** Real subprocess CLI smoke against the real packages plus in-process dispatch tests against real deterministic film providers and real temporary film packages; zero mocks.

## Reproducibility — THE FRONT DOOR: verification gates, deterministic regeneration, and artifacts

bond-cli inherits the fleet's determinism guarantees and adds a few of its own:

- **Delegation, not duplication.** Every command calls a built layer; there is no second implementation to drift from the source of truth.
- **Frozen discovery.** Films are located through the FROZEN `bond_api` contract; output uses canonical ordering (roster order, sorted JSON keys per RFC 8259 [@rfc8259]).
- **Fixed seeds.** Film providers are deterministic; `bond run` reproduces an identical consolidated debrief for an unchanged fleet.
- **No wall-clock in persisted artifacts.** The CLI writes nothing time-based to files, the `--json` snapshots carry no `generated_at` field (a test asserts its absence), and the manuscript token map embeds no timestamps.
- **No hand-authored numbers.** Every quantity in this manuscript is an injected token generated by `src/bond_cli/manuscript_variables.py` from the registry that defines it — `COMMANDS`, `JSON_COMMANDS`, and `DEPENDENCY_LAYERS` in `dispatch`, the coordinator `ROSTER`, and the orchestrator's mission registry. `data/claim_ledger.yaml` records the same values alongside the symbol each is derived from, and the test suite re-derives every ledger row from that symbol, so a stale number fails the gate instead of shipping. Measured evidence that changes with each run — test count and coverage % — is written only to `docs/_generated/COUNTS.md`.
- **Environment-independent tests.** The fleet's aggregate gate manifest lives outside this package and appears or disappears as the fleet gate runs; every test that depends on it pins `dispatch.GATE_MANIFEST` at a temporary file, so the suite's result and its branch coverage do not move with the workspace's state.
- **Tests as evidence.** The suite runs real subprocess invocations against the real packages and asserts byte-stable command output wherever the layers beneath are deterministic. In particular, `status --json` and `roster-export` are each invoked twice in separate subprocesses and asserted byte-identical, binding the repeatability claim to a test rather than to inspection; and the installed `bond` console script is exercised in a subprocess and its stdout/exit code asserted equal to the `scripts/bond.py` bootstrap, so the declared `pyproject.toml` entry point cannot silently rot.

To reproduce the whole surface from a clean checkout:

```bash
uv sync --extra dev
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/z_generate_manuscript_variables.py
uv run python scripts/bond.py status --json
```

## Scope and Related Work — THE FRONT DOOR: boundaries, positioning, and relationship to the literature

### Scope

bond-cli covers the **front-door** surface only: routing verbs to films, missions, status, gadgets, and roster export. It does **not** implement the `MissionProvider` protocol (bond-api), the mission DAG and checkpoint machinery (bond-orchestrator), the registry/ledger/situation room (bond-coordinator), or Q-branch primitives (bond-utilities). A film is never executed outside its own frozen provider; a mission is never orchestrated outside the runner. The one computation the front door does own — overlaying the measured gate manifest onto the registry — is presentational: it changes what is reported, never what is executed.

Explicitly out of scope: interactive or TUI modes, persistent CLI state, network access, credential handling, and any writing to another package's tree. The only file the CLI writes is the roster export the operator asks for with `--output`, plus its own manuscript token map.

### Relationship to the built layers

- **bond-api (THE PROTOCOL)** — the FROZEN `MissionProvider` contract + discovery + `GadgetRegistry` that the front door consumes for `brief`/`recon`/`plan`/`execute`/`debrief` and `gadgets`.
- **bond-coordinator (MISSION CONTROL)** — source of the 27-film `ROSTER` for `list`/`whois`/`roster-export` and of the `build_status` snapshot for `status`.
- **bond-orchestrator (DAG 00)** — source of the 3 canned missions and the `MissionRunner` for `run`.
- **bond-utilities (Q-BRANCH)** — transitively loaded by film providers; provenance is recorded by the orchestrator and merely displayed here, never recomputed.

### Related work

The design is conventional by intent. The verb-first grammar and one-verb-per-subparser structure follow the standard-library `argparse` sub-command model [@bethard2009argparse; @pythonargparse]; the exit-code discipline (0 success, non-zero failure, distinct code for usage error) and the commitment to plain, pipeable output follow long-standing Unix utility conventions [@posix2018; @raymond2003unix]. Machine-readable output is JSON per RFC 8259 [@rfc8259], key-sorted for byte-stability. The package version follows Semantic Versioning [@semver2].

The color-safe table is the one place the front door deviates from common practice: many modern CLIs auto-detect a TTY and emit ANSI colour. This one never does. Uniform bytes across a terminal, a pipe, a log file, and test capture are worth more to a fleet whose output is read by other programs than colour is to a human reader — and a table that renders identically everywhere is a table whose tests mean something.

### Related surface within the suite

`bond list` and `bond run` overlap conceptually with the orchestrator's own `list`/`run` CLI; the front door re-exposes them under one grammar rather than relocating the logic. Where the two disagree, the orchestrator is authoritative — it holds the implementation.

## Sources — THE FRONT DOOR: bibliography

@bethard2009argparse; @pythonargparse; @rfc8259; @posix2018; @raymond2003unix; @semver2; @pythoninspect


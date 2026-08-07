# Bond Coordinator — MISSION CONTROL

*infra package · package codename MISSION CONTROL*.

## Concepts — MISSION CONTROL: domain and operational focus

Fleet registry, mission ledger, status, situation room

## Abstract — MISSION CONTROL: mission summary

This paper presents **BOND-COORDINATOR** (codename **MISSION CONTROL**), the Layer-2 mission-control package for PROJECT BOND, a fleet of software packages descended from a numerical-optimization research exemplar. Where that exemplar demonstrated optimization mathematics inside a single package, BOND-COORDINATOR demonstrates the *fleet* view: a deterministic registry of all 27 film packages, a forward-only mission-state ledger, an aggregate suite-status report, and a self-contained HTML situation room. The registry (`src/bond_coordinator/registry.py`) is seeded from the ROSTER conventions in `projects/working/bond/SCOPE.md` §2.1 and assigns a provisional mission codename per film; `reconcile.py` merges a film's real codename and gadget table over it (refresh/replace semantics) once a film declares them via `bond-api`. The ledger (`src/bond_coordinator/ledger.py`) tracks each package's lifecycle — brief → recon → plan → execute → debrief — with strict forward-only transition rules, attributable-identity validation, an append-only audit trail of who/when/version, and deterministic audit summaries. The status module (`src/bond_coordinator/status.py`) aggregates counts by state and phase, a measured-coverage summary, stale/blocked flags, and a per-layer summary of the fleet topology. The situation room (`src/bond_coordinator/situation.py`) renders the whole fleet — packages, mission-timeline bars, coverage heat, suite layers, a per-film Q-branch gadget table, and the recent-transitions audit tail — into one self-contained HTML document. **Roster state (this build):** 27 packages tracked across 6 declared topology layers; 25 scaffolded, 0 building, 2 ready, 0 red; 2 packages with measured coverage (mean 95.5%, 2 at/above the 90% gate, 25 without a gate result in this build); 0 blocked; 0 stale. Provenance of those status and coverage figures: *measured gate output on 2 of 27 registry rows* — the registry's seed defaults are not a measurement of any film package; see the Results section. **Keywords:** mission control, film-package registry, mission-state ledger, append-only audit trail, registry reconciliation, suite status, software fleet, fault isolation, reproducible research

## Introduction — MISSION CONTROL: mission framing, the operational problem, and how to read this chapter

PROJECT BOND is a fleet of standalone software packages — one per
James Bond film, plus a shared layer of Q-branch infrastructure — built to the
same scientific bar as the research exemplar from which each package is
forked: pure tested cores, zero mocks, ≥90% coverage, thin orchestrators, and
deterministic, provenance-recorded outcomes. With 27 film
packages and 6 mission-infrastructure packages,
the fleet needs a single point of truth about *what exists, where it is in its
mission, and whether it is healthy*.

BOND-COORDINATOR (codename **MISSION CONTROL**) is that point of truth: the
**registry and situation room** for the whole suite. It does not implement any
film's algorithms; it records, audits, and reports on them. Concretely it
provides six capabilities, each a pure module under `src/bond_coordinator/`
with a thin orchestrator in `scripts/`:

1. **Protocol mirror** (`types.py`) — `Asset`, `Gadget`, `GadgetRegistry`,
 `PackageStatus`, and the `MissionPhase` lifecycle enum, mirroring the
 `bond-api` shapes so the core carries no sibling imports.
2. **Registry** (`registry.py`) — the authoritative, curated list of the
 27 film packages: slug, film title, release year, mission
 codename, status, and measured coverage when available.
3. **Reconcile** (`reconcile.py`) — the merge that replaces mission control's
 provisional codenames with the codenames films actually declare, and
 harvests their gadget tables into the Q-branch inventory.
4. **Mission-state ledger** (`ledger.py`) — each package's lifecycle position
 (brief → recon → plan → execute → debrief) with forward-only transition rules,
 attributable-identity validation, and an append-only audit trail.
5. **Suite status** (`status.py`) — a deterministic aggregate snapshot: counts
 by state and phase, a coverage summary, stale / blocked flags, and a
 per-layer summary of the fleet topology.
6. **Situation room** (`situation.py`) — a self-contained HTML dashboard that
 renders the whole fleet plus the Q-branch gadget inventory.

A seventh module, `manuscript_variables.py`, injects this document's own
identity and every quantity it reports (§the results section).

The package sits at Layer 2 (mission control) in the suite's dependency
topology. Its one cross-package consumer is the thin orchestrator
`scripts/reconcile.py`, which loads each film's Layer-1
`bond_api.protocol.MissionProvider` and converts the result to plain data
before it reaches the core. The core itself imports neither `bond-api` nor
the Layer-0 `bond-utilities`: it keeps a pure-core mirror of the protocol
shapes as a deliberate boundary, not as a placeholder (see `TODO.md` and
`docs/architecture.md`). Every module is deterministic, uses no framework
mocking, and is exercised by a zero-mock real-data test suite.

### Reader's guide

- the methodology section defines the registry, ledger, status, and situation-room
 models and their invariants.
- the results section reports the measured fleet state.
- the experimental setup section documents the configuration surface and the
 enforced quality gates.
- the reproducibility section certifies determinism and provenance.
- the limitations section states honestly what every figure here does and does not
 certify, and how the seeded-versus-measured distinction can be misread.
- the scope section scopes the package and relates it to the rest of the fleet.

## Methodology — MISSION CONTROL: the analytical models and algorithms that drive the mission

The pure core lives under `src/bond_coordinator/`: `types.py` (protocol
mirror), `registry.py`, `reconcile.py`, `gates.py`, `ledger.py`, `status.py`,
and `situation.py`, plus `manuscript_variables.py`. All are pure: they import
only the standard library and `pyyaml`, never `infrastructure.*`, and never a
sibling BOND package. Thin orchestrators in `scripts/` bind them to the
filesystem (persisting the ledger, writing the dashboard, printing the report).

### Registry

`registry.py` defines a frozen `PackageRecord` (rank, slug, film, year,
codename, status, coverage, concepts) and the module-level `ROSTER` tuple of
all 27 film packages, in Eon-canon order then non-Eon, exactly per `SCOPE.md`
§2.1. Status is the enum `scaffolded | building | ready | red`; coverage is a
measured percentage or `None`. Mission codenames are **assigned by mission
control** from each film's canonical plot element (e.g. Goldfinger's Operation
Grand Slam → `GRAND SLAM`) and are provisional until a film package declares
its own via `bond-api`.

The shipped `ROSTER` literal fills only the identity fields; every row's status
and coverage are seed defaults (`scaffolded` / `None`) meaning *unmeasured by
this process*. `gates.py` is the sole path by which they change:
`parse_gate_manifest` decodes the `bond-ops` gate aggregate — raising on a
malformed manifest rather than degrading to an empty result, since "nothing
measured" is indistinguishable from an honest seed — and `apply_gate_results`
derives each row's status by rule (failed run → `red`; passing at or above
`COVERAGE_FLOOR` → `ready`; passing below it, or passing with no coverage
number, → `building`; no gate row → untouched). The rule is what makes the
status a derived fact rather than an assertion, and it is asserted in both
directions by tests that break when the rule is altered.

The registry also provides `get_package`, `find_by_status`, and `subset_roster`
(the last is how tests seed deterministic film fixtures without depending on
the whole fleet).

### Reconciliation

`reconcile.py` implements the merge half of the codename policy: when a film
declares its real codename and gadget table, `override_codenames` and
`harvest_gadgets` return an updated registry with **refresh/replace**
semantics (a later build wins), leaving the source immutable.

The module also owns `gadget_purpose`, which reduces a film-registered gadget
payload to one line. The rule is explicit rather than duck-typed, because the
obvious implementation is wrong: reading `payload.__doc__` on a plain-data
payload resolves through to the *builtin type's* docstring, so a `dict` reports
`"dict -> new empty dictionary"` and a `list` reports `"Built-in mutable
sequence."`. Those are attributes of the interpreter, not declarations by the
film, and recording them as a gadget's purpose fabricates provenance.
`gadget_purpose` therefore accepts a docstring only from a routine, class, or
module — the shapes that syntactically carry one at their definition site —
uses a string payload verbatim as the film's own words, and otherwise derives a
factual shape summary from the object itself
(`"data payload: dict of 8 entries"`).

Discovery is deliberately outside the pure core. `scripts/reconcile.py` loads
each film's `bond_api.protocol.MissionProvider` via
`bond_api.discovery.load_provider`, reads `provider.brief` and the film's
module-level `GADGETS`, and converts both to plain dictionaries before calling
these functions — so no protocol type from a sibling package ever crosses the
`src/` boundary. Because reconciliation imports 27
independently developed packages, each film is guarded individually: any
exception raised while importing one film skips that film alone, with its
exception type and message reported, and the remaining films still reconcile.

### Mission-state ledger

`ledger.py` tracks each package's position in the lifecycle
brief → recon → plan → execute → debrief — 5 phases encoded by the
`MissionPhase` enum, whose ordinal drives every transition rule. A
`MissionLedger` holds the current entry per package plus an append-only list of
every recorded transition. The transition rules are strict and executable:

1. A package must be registered in the roster.
2. Phases move strictly forward: brief → recon → plan → execute → debrief.
3. Re-entering the current phase is allowed (an idempotent *touch*).
4. Moving backwards, or `advance` past debrief, raises `ValueError`. `jump`
 permits multi-step forward advances (still audible, still forward-only).

**Transition validation** goes further than forward-only ordering. Every
transition must be attributable: both the acting agent (`updated_by`) and the
`version` being progressed must be non-empty strings, and an optional `note`
must be a string. A public `validate_transition(slug, phase, by, version)`
runs the full rule set **without mutating the ledger**, so a caller (or CLI)
can gate a transition before committing it.

Every transition writes a frozen `LedgerEntry` (slug, phase, `updated_by`,
`updated_at`, version, note), so the audit trail answers *who changed which
package's state, when, and at what version*. The ledger deepens the audit into
three deterministic views: `transition_summary` (entries per phase),
`per_agent_summary` (entries per agent), and `phase_timeline(slug)` — the
chronological `(phase, timestamp)` history that drives the situation room's
mission timeline. Staleness is a pure function of entry age and an injectable
clock: a debriefed mission is never stale.

### Suite status

`status.py::build_status(roster, ledger,...)` assembles one deterministic
snapshot: counts by status and by phase, a `CoverageSummary` (known count,
mean/min/max over measured packages, count meeting the
90% gate), the set of
stale packages, a set of `BlockedPackage` reasons computed from the
combination of status and phase, and a **per-layer summary**:

- a `red` package is blocked ("flagged red");
- executing before ready is blocked;
- planning while still scaffolded is blocked.

**Per-layer summaries** render the declared suite topology
(`SUITE_LAYERS`, §2.2 of `SCOPE.md`) as one `LayerSummary` per layer — the
five infrastructure layers (`layer0`…`layer4`), each with a readiness
tri-state, plus the `films` layer aggregating the registry: tracked count,
READY count, and mean coverage. Readiness is injectable via `layer_ready`
(with `layer1` — the `bond-api` protocol — inferred from `dependency_ready`),
so the report reflects which of the suite's 6 declared
layers are actually available. All time-dependent inputs (`now`, `stale_days`)
are injectable, so the report is reproducible byte-for-byte. The snapshot also
*carries* the `stale_days` threshold it was computed with (default
30 days), so a downstream renderer states the threshold that
was applied instead of assuming the default.

### Situation room

`situation.py::build_situation_room(status, roster, ledger, gadgets)` renders
a single self-contained HTML document (no external assets, no JavaScript):

- summary cards and a **per-package table** with status, phase, a
 **mission-timeline progress bar** of one cell per lifecycle phase (done /
 current / ahead), last update, and **coverage heat** — each coverage cell
 color-coded against the 90% gate (at/above green,
 mid-range amber, low red, unmeasured gray) with a legend. The renderer
 imports `COVERAGE_FLOOR` from `status.py` rather than restating it, so the
 legend cannot drift from the gate actually enforced;
- a **suite-layers table** from `status.layers`;
- a **per-film gadget table** grouping the Q-branch inventory by film, with a
 count of which tracked films have none;
- a **recent-transitions (audit trail)** table of the newest ledger entries.

Every value is HTML-escaped; the document is deterministic given its inputs.
`scripts/build_situation_room.py` writes it to the gitignored `output/` tree.

## Results — MISSION CONTROL: measured outcomes, headline numbers, and what they establish

All figures in this section are generated from source by
`src/bond_coordinator/manuscript_variables.py` and injected as substitution
tokens — they are never hand-authored in prose.

### Fleet state

The registry currently tracks **27** film packages. Their
distribution across statuses is 25 scaffolded,
0 building, 2 ready, and 0
red, with 2 packages carrying measured coverage
(mean 95.5%, 2 at/above the
90% gate).

Those figures describe **the roster this document was built from**, and their
provenance is stated by the same generator that produced them:
*measured gate output on 2 of 27 registry rows*. The distinction matters, because the two
possible answers look identical in the numbers and are not the same claim.
The `ROSTER` literal in `registry.py` ships every row as `scaffolded` with
`coverage=None` — a seed default, meaning *this process has measured nothing*,
never *the fleet is unbuilt*. A build run with `--no-gate-manifest` therefore
reports all 27 rows scaffolded with no coverage, and that is a
statement about the seed, not a measurement of the 27 film
packages. Measured values enter only through
`gates.apply_gate_results`, from the `bond-ops` gate aggregate; a build run
against that manifest reports each package's real status and real coverage.
Nothing in this package measures a film package itself, and no figure above is
evidence about any film's actual test suite.

### Registry completeness

The roster is canon-ordered and complete: it spans `dr_no`
(1962) through `never_say_never_again`
(1983) with every Eon entry and both non-Eon entries.
The full slug list is: dr_no, from_russia_with_love, goldfinger, thunderball, you_only_live_twice, on_her_majestys_secret_service, diamonds_are_forever, live_and_let_die, the_man_with_the_golden_gun, the_spy_who_loved_me, moonraker, for_your_eyes_only, octopussy, a_view_to_a_kill, the_living_daylights, licence_to_kill, goldeneye, tomorrow_never_dies, the_world_is_not_enough, die_another_day, casino_royale_2006, quantum_of_solace, skyfall, spectre, no_time_to_die, casino_royale_1967, never_say_never_again. Each record carries a
provisional mission codename and the core concepts that will power that film's
software payload, so the registry is both an inventory and a build briefing.

### Suite layers

The coordinator declares **6** topology layers —
layer0 (Q-branch primitives), layer1 (The protocol), layer2 (Mission control), layer3 (The DAG runner), layer4 (Front door & fleet ops), films (Film packages) — and reports each in the status snapshot and the
situation room. The `films` layer reports 27 tracked with
2 ready and mean coverage over the measured rows only; the
infrastructure layers report readiness only where probed (layer 1 tracks the
`bond-api` probe, the rest report the tri-state "not probed" unless a caller
supplies readiness). Every one of these counts is derived from the roster
handed to the generator, never hand-authored.

### Reconciliation against the real fleet

Reconciliation is the point where mission control stops asserting and starts
measuring. `scripts/reconcile.py` loads each built film's `MissionProvider`,
reads its declared codename, harvests its gadget table, and hands plain data
to the pure merge in `reconcile.py`. Two properties are established by test
rather than by inspection of a particular run, because the fleet's contents
change as film packages are built:

- **Per-film isolation is a positive control, not a promise.** A film that
 raises on import is skipped individually — with its exception type and
 message reported — while every other film still reconciles. The test
 materialises a film whose module raises at import time and asserts the run
 still succeeds and still harvests its healthy neighbour. This replaced a
 guard narrow enough that one half-edited package aborted the fleet-wide run.
- **No borrowed provenance.** A gadget's purpose is derived by
 `reconcile.gadget_purpose`, which accepts a docstring only from payloads
 that syntactically carry one (routines, classes, modules), takes a string
 payload as the film's own words, and otherwise emits a factual shape
 summary. Reading `payload.__doc__` unconditionally instead resolves to the
 *builtin type's* docstring for plain data, recording CPython's own strings
 as purposes the film never declared. A parametrised test asserts the
 derived purpose differs from `payload.__doc__` for every plain-data shape.

### Ledger and status behaviour

The ledger's forward-only rules are verified by tests that walk a package the
full lifecycle, attempt illegal backwards and past-debrief transitions, assert
that empty or non-attributable transitions are rejected, and check the
deterministic audit summaries (`transition_summary`, `per_agent_summary`,
`phase_timeline`). The status aggregator is verified against deliberately
heterogeneous rosters (ready/building/scaffolded/red mixes) to exercise every
blocked rule, the coverage summary, and the per-layer summaries. Observed
behaviour in this build: **0** packages blocked and
**0** stale, consistent with a fresh ledger at `brief`
whose audit trail holds 27 entries (one per
registered package). Coverage heat, mission-timeline bars, per-film
gadget grouping, and the recent-transitions table are all rendered
deterministically and asserted byte-identical across repeated builds.

### Summary table (live-generated)

Every figure below is injected from the registry/ledger by
`src/bond_coordinator/manuscript_variables.py` — none is hand-authored.

| Metric | Value |
|---|---|
| Tracked film packages | 27 |
| Declared suite-topology layers | 6 |
| Mission-infrastructure packages (non-films layers) | 6 |
| Lifecycle phases | 5 |
| Enforced coverage floor | 90% |
| Default staleness threshold | 30 days |
| Roster span | `dr_no` (1962) → `never_say_never_again` (1983) |
| Measured coverage (known / at-or-above floor / mean) | 2 / 2 / 95.5% |
| Status counts (scaffolded / building / ready / red) | 25 / 0 / 2 / 0 |
| Blocked / stale packages | 0 / 0 |
| Audit-trail entries (fresh ledger) | 27 |

Provenance of the status and coverage columns:
*measured gate output on 2 of 27 registry rows* — read the Limitations section
(§[sec:limitations]) before interpreting them as claims about any film.

## Conclusion — MISSION CONTROL: findings, verdict, and what the mission establishes

BOND-COORDINATOR (codename **MISSION CONTROL**) demonstrates a
fleet-scale variant of the research-exemplar contract: instead of one
package's mathematics, it maintains the single point of truth for a
**27**-package software fleet. Its contributions are:

- a curated, canon-ordered **registry** (`registry.py`) seeding every film
 package with slug, film, codename, status, and concepts;
- a **mission-state ledger** (`ledger.py`) whose forward-only rules and
 append-only audit trail make "who moved which mission, when, at what
 version" a machine-checkable fact;
- a **reconciliation** merge (`reconcile.py`) that replaces provisional
 codenames with the ones films actually declare and harvests their gadget
 tables, deriving each gadget's purpose without ever borrowing a builtin's
 docstring;
- a **gate-result adapter** (`gates.py`) that is the only way a registry row
 acquires a status or coverage number, deriving both by rule from `bond-ops`
 gate output;
- an aggregate **status** report (`status.py`) that turns registry and ledger
 into executably-defined stale/blocked/coverage signals;
- a self-contained **situation room** (`situation.py`) that renders the whole
 fleet — plus the Q-branch gadget inventory — as one HTML document.

The design decisions that matter are the pure-core boundary (nothing in
`src/` touches `infrastructure.*`, the filesystem, or a sibling package —
protocol types are mirrored rather than imported, and cross-package discovery
is confined to a thin orchestrator), determinism (injectable clocks, no
wall-clock tokens), partial-failure tolerance across a fleet of independently
developed packages, and the zero-mock test discipline carried over from the
exemplar. Two of those properties are held by positive controls — a
deliberately broken film package, and an assertion that a derived gadget
purpose differs from the payload's inherited `__doc__` — because a guard that
has never been seen to fire is not yet known to work.

What the situation room reflects is exactly what it was fed, and it says which
that was. Reconciled codenames reach it only when
`scripts/build_situation_room.py` is given a reconcile manifest
(`--reconciled`), and measured status and coverage only when it is given a gate
manifest (`--gate-manifest`); without either it renders the registry's
provisional codenames and unmeasured seed defaults, and prints that fact in the
document's provenance block rather than letting a seed default pass for a
measurement. Both paths are held by tests that fail when the wiring is
removed. The honest summary is therefore narrower than "always reflects
reality": the dashboard reflects the manifests supplied to it, and states their
absence when they are not.

## Experimental Setup — MISSION CONTROL: canonical scenarios, parameters, and configuration

### Configuration surface

The manuscript identity is loaded from `manuscript/config.yaml` by
`src/bond_coordinator/manuscript_variables.py::load_config` and injected as
tokens; the only hand-authored prose values are the tokens themselves, never
hardcoded numbers. Identity fields (title `BOND-COORDINATOR`, subtitle
`The Registry and Situation Room for the BOND Suite`, version `0.1.0`, codename
`MISSION CONTROL`, keywords) live under `paper:` and `mission:`.

There is deliberately **no `experiment:` block**: unlike the exemplar, the
coordinator has no analysis-output dependency. `generate_variables(...,
require_outputs=...)` accepts the flag for pipeline parity but never gates on
generated files — this is the one intentional divergence from the exemplar's
strict analysis-to-manuscript contract, documented in `docs/architecture.md`.

### Dependencies

- **Runtime**: `pyyaml` (manuscript config parsing). Everything else is the
 Python standard library.
- **Developer**: `pytest`, `pytest-cov` (coverage gate), `ruff` (lint +
 format), `mypy` (types).

### Quality gates

The enforced gates for this package are:

1. **Coverage**: `uv run pytest tests/ --cov=src --cov-fail-under=90` —
 line + branch coverage on `src/` at or above 90%, the
 same floor `status.py::COVERAGE_FLOOR` applies when grading the fleet.
2. **Zero mocks**: no `unittest.mock` / `MagicMock` / `@patch` anywhere in
 `tests/`; all tests use real data and real computation.
3. **Types/style**: `ruff check` and `mypy` clean on `src/bond_coordinator`
 and `scripts/`.
4. **Determinism**: fixed clocks and fixed seeds; no wall-clock tokens in
 generated artifacts.

### Test data

Behavioral tests are seeded from a **deterministic five-film fixture** of
representative packages (`dr_no`, `goldfinger`, `goldeneye`, `skyfall`,
`no_time_to_die`) via `subset_roster`, so the suite exercises every rule
without depending on all 27 packages being built. A
full-registry test independently asserts completeness (27
unique, canon-ordered slugs).

Tests that touch the live fleet are written to assert **this package's**
contract rather than a sibling's internals, because sibling packages are
developed concurrently and may be mid-edit at any moment. Where a
deterministic film is required — for the broken-film isolation control and the
gadget-purpose regression guard — the test materialises its own minimal film
package in a temporary directory and points the CLI at it with `--bond-root`.
This keeps the suite's result a function of this package alone.

## Reproducibility — MISSION CONTROL: certification, gates, and regeneration

Reproducibility is a first-order requirement for mission control, because the
suite's provenance story depends on it. The certification below follows the
reproducibility-in-computational-research guidance of
[@sandve2013tensimplerules; @peng2011reproducibleresearch].

### Determinism

- **Injectable clocks**: every time-dependent path (`MissionLedger`, `build_status`,
 `is_stale`) accepts an injectable `now`; tests pin a fixed UTC reference clock and
 assert exact timestamps and byte-identical outputs.
- **No wall-clock tokens**: `manuscript_variables.py` emits no
 `GENERATION_TIMESTAMP`-style token, so manuscript bytes depend only on the
 config file and registry/ledger state. A test asserts the situation room is
 byte-identical across repeated builds with identical inputs.
- **Deterministic audit views**: `transition_summary`, `per_agent_summary`,
 and `phase_timeline` are pure functions of the append-only history — their
 output is stable for a given ledger, and the situation room's
 recent-transitions table sorts with a deterministic tie-break
 (`(timestamp, slug)`).
- **Fixed seeds**: no random draws anywhere in `src/` or `tests/`.

### Provenance

- The ledger is **append-only** and validated: every transition must carry a
 non-empty agent and version (a `@require`-style identity check), and a
 non-mutating `validate_transition` gates moves before they commit. Every
 recorded transition lands in the audit trail, and `to_json`/`from_json`
 round-trip state and history losslessly. A thin CLI
 (`scripts/advance_mission.py`) persists the ledger to
 `output/data/mission_ledger.json` after each move.
- The audit trail is *countable, not just capturable*: at a fresh state it
 holds exactly 27 entries (one per registered
 package), and every later move is visible in `transition_summary` and
 `per_agent_summary`.
- Generated artifacts — `output/situation_room.html`,
 `output/data/suite_status.json`, `output/data/manuscript_variables.json`, and
 the resolved manuscript tree — are gitignored and understood to be disposable:
 they are always regenerated from source, never hand-edited.

### Verification

The certification commands (identical to the enforced gates) are:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/bond_coordinator scripts
uv run mypy src/bond_coordinator scripts
```

The availability of the Layer-1 package (`bond-api`) is detected at runtime by
a `importlib.util.find_spec` probe in `scripts/` and reported in the status and
situation-room output. The probe measures *importability in this
environment*, not whether the package exists, and the rendered wording says so:
a false result reads "not importable in this environment (pure-core mirror in
use)". The pure core never depends on the result — it works from its own
protocol mirror either way (`docs/architecture.md`).

Reconciliation against the live fleet is likewise reproducible in the sense
that matters for a fleet of independently developed packages: it is
*order-independent and partial-failure-tolerant*. Each film is imported under
its own guard, so a film that raises at import is skipped with its exception
type and message on stderr while every other film still reconciles, and the
harvest merge is idempotent (re-registering a `(film, gadget)` pair replaces
it, so repeated runs converge on the same table).

## Scope and Related Work — MISSION CONTROL: boundaries, positioning, and relationship to the literature

### Scope

BOND-COORDINATOR is **Layer 2 (mission control)** of PROJECT BOND.
Its scope is exactly the pure core under `src/bond_coordinator/` — `types.py`,
`registry.py`, `reconcile.py`, `ledger.py`, `status.py`, `situation.py`, and
`manuscript_variables.py` — and their thin `scripts/` orchestrators. It
implements **no film algorithms** and makes **no cross-film computation**: those
belong to the 27 film packages. It does not orchestrate missions across
packages (that is Layer 3, `bond-orchestrator`) and does not expose a front
door (that is Layer 4, `bond-cli`).

Within that boundary this package is deliberately standalone. Its `src/` core
is pure — no `infrastructure.*`, no sibling-package imports (the `reconcile`
**script** discovers films through `bond-api`, but the pure merge functions
take plain data) — so the registry, ledger, status, and situation room can run
in any Python 3.10+ environment with `pyyaml` installed, exactly as the
exemplar's mathematical core could.

### Related work

The package inherits the research-exemplar's standards — ≥90% zero-mock
coverage, pure tested cores, thin orchestrators, injected manuscript variables
[@hunt1999pragmatic; @gamma1995designpatterns] — and applies the design-pattern
vocabulary of software architecture [@bass2012softwarearchitecture] and
enterprise registries [@fowler2002patterns] to a multi-package fleet. The
layered topology (strict downward dependency, per-layer readiness) follows the
layered-architecture guidance in the software-engineering body of knowledge
[@swebok2014], and the central claim — that a machine-checkable registry and
append-only, validated ledger make fleet health an executable fact — follows
the "essence vs. accidents" framing of software complexity
[@brooks1987nosilverbullet].

### Positioning within the fleet

The coordinator declares and reports `6` topology
layers (`layer0 (Q-branch primitives), layer1 (The protocol), layer2 (Mission control), layer3 (The DAG runner), layer4 (Front door & fleet ops), films (Film packages)`) and surfaces per-layer readiness in the
status snapshot and situation room:

| Layer | Package(s) | Coordinator report |
|---|---|---|
| Layer 0 (Q-branch primitives) | `bond-utilities` | readiness tri-state |
| Layer 1 (the protocol) | `bond-api` | readiness (tracks the runtime probe) |
| **Layer 2 (mission control)** | **`bond-coordinator` (this package)** | registry, ledger, status, situation room |
| Layer 3 (the DAG runner) | `bond-orchestrator` | readiness tri-state |
| Layer 4 (front door / fleet ops) | `bond-cli`, `bond-ops` | readiness tri-state |
| Films | 27 film packages | tracked count, READY count, mean coverage |

Layer 1 (`bond-api`) **is built**, and `scripts/reconcile.py` consumes its
`MissionProvider` discovery directly. The pure-core mirror of the protocol
shapes (`src/bond_coordinator/types.py`) nevertheless stays: it is an
architectural boundary that keeps `src/` free of sibling imports, not a
placeholder waiting for the real package. Layer 0 (`bond-utilities`) **is
built** as well, and its `mission_io` module carries the fleet's
provenance-record conventions; this package has not yet adopted it — ledger
provenance still uses local stdlib JSON codecs, and routing it through Layer 0
is the one open integration item (see `TODO.md`). Layer 4's `bond-ops`
produces the fleet gate aggregate that `src/bond_coordinator/gates.py`
consumes, which is how a registry row acquires a measured status and coverage.

## Limitations and Uncertainty — MISSION CONTROL: assumptions, threats to validity, and what the numbers do not claim

No claim below is a discovery about any film; every statement is about the
registry, ledger, and status machinery this package ships, and about the
boundaries of what those numbers do and do not certify.

### The seeded registry is not a measurement

The `ROSTER` literal in `src/bond_coordinator/registry.py` ships every one of
the 27 film rows with `status=scaffolded` and `coverage=None`.
Those are *seed defaults*: they mean "this process has not applied gate output
to this row", never "the fleet is unbuilt" and never "this film passes at some
coverage". When a manuscript or dashboard is built with
`--no-gate-manifest`, every figure that reads "*measured gate output on 2 of 27 registry rows*"
is therefore a statement about the seed, and only about the seed. The number
2 "ready" / 25 "scaffolded" in such a
build must not be read as a claim about any film package's actual state.

### Measured values are only as good as the manifest that supplies them

The single path by which a row becomes `ready`/`building`/`red` with a real
number is `gates.apply_gate_results`, consuming the fleet aggregate that
`bond-ops` writes at a *convention* location
(`../output/aggregate/gate_manifest.json`). Three properties bound the
uncertainty of anything reported as "measured":

1. **The path is a convention, not a contract.** Nothing in this package
 forces `bond-ops` to keep writing that exact path; if the sibling relocates
 its aggregate, every consumer here degrades to the unmeasured seed. That
 degradation is *announced* (the provenance line says
 `measured gate output on 2 of 27 registry rows`, and the scripts print `no gate manifest
 at …` to stderr), so it is not a silent lie — but a fleet whose sibling
 moved a file is indistinguishable, in these outputs, from a fleet that was
 never measured.
2. **Coverage is treated as a bounded percentage.** A row whose coverage is
 non-finite, negative, or above 100 is rejected loudly by
 `parse_gate_manifest` (`ValueError`) rather than coerced into the fleet
 mean. This closes the class of bug where a stray `NaN`/`Infinity` in a
 manifest silently poisons `CoverageSummary.mean`.
3. **Absence of a row is absence of evidence.** A film with no gate row keeps
 its seed state. We cannot distinguish "not yet gated" from "gated and
 skipped", which is honest but makes `25` an
 upper bound on how much of the fleet the status report actually certifies.

### Ledger truthfulness is bounded by its inputs

The forward-only transition rule is *exact and centralised*: the same
`_require_forward` helper backs both the mutating path and the non-mutating
`validate_transition`, so the two cannot drift, and the defensive invalid-jump
guard is reachable and tested rather than excluded. But the ledger records
what a caller tells it. It validates that a move is forward and attributable;
it does not verify that a film objectively "is" a given phase, nor that the
`updated_by` identity is real. A `touch` re-stamps the current phase, so the
audit tail's per-phase counts (`LEDGER_PHASE_COUNT` phases, `brief →
recon → plan → execute → debrief`) include same-phase re-entries and can
overcount *activity* relative to *movement*. Staleness
(`30` days) is a heuristic: a mission is "stale" purely
because no transition was recorded within the window, which treats an
abandoned mission and an idle-but-legitimate one identically.

### Gadget purposes are derived shapes, not film confessions

`reconcile.gadget_purpose` deliberately refuses to read a builtin's
`__doc__`, because doing so recorded CPython's own strings as a film's
declared purpose. The flip side is that a plain-data payload is summarised by
its *shape* ("data payload: dict of 8 entries"), which is factual but conveys
nothing about what the gadget does. Purposes derived this way understate
semantic content by construction; they make no claim about the gadget's real
behaviour.

### Reconciliation is partial by design

`scripts/reconcile.py` imports 27 independently developed
packages, each guarded individually: a film that raises at import is skipped
with its exception type and message reported, and the other films still
reconcile. The cost is that a run's completeness is a runtime fact, not a
constant — the set of films that declared a codename or harvested a gadget
varies with what is built on disk that day. Nothing here should be read as
"all 27 films reconciled"; the skipped set is always reported.

### The situation room reflects its inputs, exactly

`build_situation_room` renders whatever roster, ledger, gadget table, and
provenance wording it is handed, and says which of the reconciled/measured
manifests (if any) were loaded. It is deterministic and HTML-escaped, so it
cannot *distort* its inputs — but it cannot *repair* them either. A dashboard
built with stale manifests is a faithful rendering of stale facts.

### Uncertainty statement

Because this package issues no scientific quantities of its own, most
conventional uncertainty analysis (error bars, confidence intervals) does not
apply. Its uncertainties are *modelling* and *provenance* uncertainties, and
they are qualitative: how complete a reconciliation run was, whether a
seed-vs-measured figure is being read as the other, and whether the fleet gate
aggregate this run consumed is the one the current `bond-ops` produces. We
insist on stating those explicitly in every rendered artifact rather than
quantifying them, because a spurious precision here would be the most
misleading output the package could produce.

The reproducibility bar is documented in §[sec:reproducibility] and follows
the reproducibility-in-research-software guidance of
[@sandve2013tensimplerules; @peng2011reproducibleresearch].

## Sources — MISSION CONTROL: bibliography

@gamma1995designpatterns; @brooks1987nosilverbullet; @bass2012softwarearchitecture; @fowler2002patterns; @hunt1999pragmatic; @swebok2014; @sandve2013tensimplerules; @peng2011reproducibleresearch


# Bond Orchestrator — DAG 00

*infra package · mission codename DAG 00*.

This chapter reproduces the package's complete manuscript verbatim:
the abstract and every authored section, token-hydrated from the
package's own manuscript variables, with the package's figures carried
in the combined PDF and its sources resolved against the unified
bibliography.

## Concepts

Multi-package mission DAG runner + real-film binding

## Abstract

**BOND-ORCHESTRATOR (codename DAG 00)** is the Layer 3 mission orchestrator of the BOND suite: it executes multi-package film missions end-to-end over the `MissionProvider` protocol. A mission is a directed acyclic graph of film packages — dependency edges exist exactly where one film's recon outputs feed another film's recon — and the orchestrator executes every package through the five lifecycle phases in deterministic topological order, producing a single consolidated debrief. The flagship canned mission, **OPERATION_OMNIBUS**, chains goldfinger → goldeneye → no_time_to_die; its last measured execution order was goldfinger → goldeneye → no_time_to_die, with an all-verdicts outcome of **PASS**. Every outcome is recorded with provenance (an independent, deterministic record writer — this package does not yet delegate to `bond-utilities.mission_io`, see §7.4), and intermediate reports persist to a state directory so an interrupted mission resumes from its last completed step. The execution core is pure logic with zero infrastructure imports; determinism is load-bearing: identical inputs produce byte-identical reports, checkpoint files, and provenance records.

## Introduction

The BOND suite splits multi-package research-and-response operations into
six cooperating packages: `bond-utilities` (shared mission I/O and
provenance), `bond-api` (the `MissionProvider` contract), `bond-coordinator`
(fleet-level planning), `bond-orchestrator` (this package — Layer 3, the DAG
runner), `bond-cli`, and `bond-ops`. Each film package (GOLDFINGER,
GOLDENEYE, NO TIME TO DIE,...) is itself a self-contained mission capability
that implements the provider protocol.

This package, **BOND-ORCHESTRATOR** (codename **DAG 00**), is responsible for
one thing: running a mission across N providers end-to-end and reporting a
single consolidated debrief. It does not implement any film's business logic —
that belongs to the providers — and it does not decide which missions exist —
that belongs to the mission registry in
`src/bond_orchestrator/missions.py`. It only guarantees *order*, *resumability*,
and *provenance*.

The guarantees are enforced by construction:

- **Order** — `src/bond_orchestrator/graph.py` builds the film DAG from
 `depends_on` edges and computes a canonical topological order (Kahn's
 algorithm with id tie-breaking), so execution order never depends on
 declaration order or dictionary iteration.
- **Resumability** — `src/bond_orchestrator/runner.py` persists every
 completed `(phase, package)` step to a state directory and replays it on
 resume, continuing from the last completed step.
- **Provenance** — `src/bond_orchestrator/provenance.py` writes one
 provenance record per executed plan step and per debrief, with a
 deterministic run id.
- **Bounded recovery** — `src/bond_orchestrator/retry.py` re-executes a
 failing `execute` step a bounded number of times, immediately and without
 wall-clock backoff, so recovery never costs determinism.
- **Explicit concurrency** — `src/bond_orchestrator/planning.py` decomposes
 the DAG into the wavefront stages a parallel executor could run, reporting
 achievable parallelism and critical path without changing the sequential
 execution contract.
- **Real-film binding** — `src/bond_orchestrator/film_providers.py` adapts
 packages written against the frozen `bond_api.MissionProvider` protocol to
 the runner-side contract, so the fleet's real films run under all of the
 above rather than a parallel code path.

Two of those deserve their negative statement up front, because they are what
the package deliberately does *not* do. It does not sleep between retries: a
wall-clock delay would leak a non-reproducible quantity into an artifact whose
byte-stability is the point. And it does not execute packages concurrently:
concurrency is emitted as a plan and verified as a property, not performed,
so that the guarantees above hold under a single, auditable execution order.

The reader's guide: §2 details the DAG model, the five-phase lifecycle, the
retry policy, stage planning, real-film binding, and provenance; §3 reports
the measured OPERATION OMNIBUS execution and the real-film runs; §4 states
what the design bought and what it deferred; §5 lists the configured mission
parameters and the mission shapes under test; §6 documents reproducibility;
§7 bounds the scope and places the work against prior art.

## Methodology

### 2.1 The mission DAG

A mission is an ordered collection of film packages
(`src/bond_orchestrator/protocol.py::Mission`). Each package declares
`depends_on`, the set of package ids whose recon outputs feed its own recon.
`build_film_graph` (`src/bond_orchestrator/graph.py`) turns that declaration
into a directed acyclic graph with an edge `(upstream, downstream)` for every
dependency, validating that:

1. no package depends on itself,
2. every dependency names a package inside the mission,
3. the graph is acyclic.

Execution order is the **deterministic topological order** of the DAG: Kahn's
algorithm with a sorted ready-worklist, so the result is canonical for a given
set of packages regardless of declaration order [@kahn1962topological;
@cormen2009introduction]. The current flagship mission,
OPERATION_OMNIBUS, declares 3 packages and is
therefore executed in exactly one valid topological order.

**Cycle detection.** A mission whose dependencies close a loop is rejected
before any provider runs: `FilmGraph.find_cycle` (`src/bond_orchestrator/graph.py`)
runs a depth-first search over sorted node ids and returns the *ordered cycle
path* (e.g. `("goldeneye", "goldfinger", "goldeneye")`); the raised
`CycleError` carries that path, so a miswired mission names its own loop
(goldfinger ↔ goldeneye) instead of a bare "cycle detected" message. The same
validation gates the stage planner (§2.5) and therefore the `plan` CLI
command.

### 2.2 The five-phase lifecycle

Every provider implements the `MissionProvider` protocol
(`src/bond_orchestrator/protocol.py`): **brief, recon, plan, execute, debrief**. The runner
(`src/bond_orchestrator/runner.py::MissionRunner`) executes phase-major,
package-minor: for each phase, every package runs in topological order,
sharing one `MissionContext` that accumulates recon reports. A downstream
package's `recon` therefore reads its dependencies' `outputs` (the DAG edge
semantics), and `plan`/`execute`/`debrief` see the full recon picture.

Execution is sequential and deterministic; the topological order is exactly
what makes a later parallel implementation safe, because every dependency's
outputs are guaranteed present before a consumer runs (§2.5 makes that
parallelism explicit without changing the sequential contract).

### 2.3 Checkpoint / resume

When a `checkpoint_dir` is supplied, every completed `(phase, package)` step
is persisted as `<checkpoint_dir>/<mission>/<phase>_<package>.json` with a
`manifest.json` tracking completed steps in order. Re-running the same mission
with the same checkpoint dir replays completed steps (recon reports are
restored into the context so downstream steps see identical inputs) and
resumes from the last completed step. The manifest records a deterministic
*fingerprint of the mission definition* (name + every package and its
`depends_on` edges, via `protocol.mission_fingerprint`); a resume against a
checkpoint dir written for a different definition is refused loudly rather
than replaying stale steps that describe a mission never executed (TODO C1).
Execute steps additionally persist their attempt count, so a retried step
(§2.4) resumes with an identical retry record. This follows the standard checkpoint/rollback-recovery pattern for
long-running distributed work [@elnozahy2002survey; @chandy1985distributed],
specialised here for deterministic single-node execution.

### 2.4 Retry policy

A `RetryPolicy` (`src/bond_orchestrator/retry.py`) bounds how many attempts a
failing `execute` step is given (default **1**
attempt in configuration; the CLI raises it via `--retry-max-attempts N`).
When any execution result carries a retryable outcome (`"failure"` by
default), the step is re-executed — immediately and deterministically, with
**no wall-clock backoff**, because a sleep would break the byte-determinism of
reports, checkpoint files, and provenance records. After `max_attempts` the
final outcome stands. This is fault *tolerance* in the standard sense — a
transient fault is masked before it becomes a mission failure, while a
persistent one is allowed to surface [@avizienis2004basic] — with the backoff
term removed because reproducibility outranks throughput here. Every step that
needed more than one attempt records a
`RetryRecord` (package, phase, attempts, succeeded) in the mission report and
in its checkpoint record; retries are thus observable, resumable, and
manuscript-token-able, while the consolidated debrief only annotates them when
they occurred.

### 2.5 Parallel-stage planning

`src/bond_orchestrator/planning.py` decomposes the film DAG into **parallel
stages** — the classic wavefront scheduling of directed task graphs
[@kwok1999static]. Stage 1 holds every package with no dependencies; stage
`k` holds every package whose dependencies all sit in stages `< k`; within a
stage, package ids are sorted, so the plan is canonical. The `StagePlan`
reports the achievable parallelism (widest stage) and the critical path
length (number of stages), and the `plan` CLI command renders it. Execution
itself remains sequential — the stages are the *planning artifact* that makes
a future parallel executor provably safe, since every package in a stage may
run concurrently without violating dependency order.

### 2.6 Real-film binding

The orchestrator's own protocol (§2.2) is the *runner-side* contract: it is
package-aware, because the runner must hand a `MissionPackage` and the shared
`MissionContext` to every call. The film packages of the BOND fleet implement
a different, deliberately narrower contract — the **frozen `bond_api`
`MissionProvider`**, whose methods take only a `ReconRequest`, a
`MissionPlan`, or a `MissionOutcome` and know nothing about DAGs. Neither
contract may move: the frozen protocol is consumed by 27 film packages, and
the runner-side shapes (`MissionPackage`, `MissionContext`) are consumed by
`bond-cli` and `bond-coordinator`.

`src/bond_orchestrator/film_providers.py` resolves that tension with an
adapter [@gamma1994design]. `FilmProviderAdapter` wraps one discovered
`bond_api` provider and presents the runner-side interface, translating in
both directions:

- **Down** — the DAG hand-off is folded into the film's own vocabulary. The
 adapter renders each `depends_on` dependency's recon `outputs` into the
 `ReconRequest.goal` text (`_citation_text`), so a film that has never heard
 of the DAG still receives its upstream intelligence; a dependency that
 produced no outputs contributes nothing rather than an empty citation.
- **Up** — the film's `Finding` list becomes the adapter's `ReconReport`:
 labels with detail become `outputs` (the downstream hand-off channel),
 every finding becomes a rendered `findings` entry, the film's plan steps are
 renumbered from 1, and the `MissionOutcome`'s numeric results become the
 `Debrief` metrics (booleans excluded — `bool` is an `int` in Python and
 would otherwise be reported as a measurement).

`load_film_providers(slugs, bond_root)` discovers each film from
`<bond_root>/<slug>/src` through `bond_api.discovery.load_provider` and is
**strict**: a missing package directory, an absent `mission.py`, or a
discovery failure raises `FilmProviderError` rather than dropping a package,
because a silently short mission would still report all-verdicts-pass.
`load_mission_providers(mission, bond_root)` binds every package a `Mission`
declares. `bond_api` is imported *lazily*, inside the methods that need it, so
the pure core of §2.1–§2.5 remains liftable into any environment where
bond-api is not installed.

### 2.7 Provenance

For every outcome — each executed plan step and each debrief — the runner
emits a `ProvenanceRecord` (`src/bond_orchestrator/provenance.py`) carrying a
deterministic run id (sha256 over mission name + package ids), the package and
provider, the phase, the outcome, artifact references, and numeric metrics.
Records are written as `outcomes.json` and a flat `provenance.csv`. This is an
independent, deterministic provenance writer, not yet a delegation to
`bond-utilities.mission_io` (the integration and its schema mapping are tracked
in `TODO.md`, §7.4).

## Results

### 3.1 OPERATION OMNIBUS execution

OPERATION_OMNIBUS ran to completion over the deterministic reference
providers (`src/bond_orchestrator/providers.py`), which implement the real
`MissionProvider` protocol with fixed logic — no mocks, no random draws.

The execution order was:

```
goldfinger → goldeneye → no_time_to_die
```

The mission executed **6** plan steps across all packages,
and the consolidated debrief closed with an all-verdicts outcome of
**PASS**.

The per-package debrief table below is read out of the live execution (`output/data/mission_report.json`)
by `src/bond_orchestrator/manuscript_variables.py::_results_tokens` — the same
report the consolidated debrief prints. No cell is hand-typed; every verdict
and metric is the engine's own record, formed with the same `%g` formatting
the runner uses so the table cannot disagree with the debrief it summarizes.

| Package | Verdict | Metrics |
|---|---|---|
| goldfinger | pass | market_index=0.92, reserves_t=4200 |
| goldeneye | pass | shield_rating=0.87, uplink_redundancy=2 |
| no_time_to_die | pass | candidate_antidotes=3, neutralization_rating=0.99 |

Dependency-edge semantics were verified at recon time. The run carried
**2** hand-off edges, each one an upstream
package's recorded recon `outputs` reaching its declared downstream consumer:

```
goldfinger → goldeneye: gold_reserves_t=4200, market_index=0.92; goldeneye → no_time_to_die: emp_shield_rating=0.87, uplink_redundancy=2
```

Those payloads are read out of `output/data/mission_report.json` by
`src/bond_orchestrator/manuscript_variables.py::_handoff_tokens`, not typed
into this section, so the edge evidence cannot drift from the run that
produced it. The DAG's data hand-off therefore behaved exactly as specified
in §2.1.

### 3.2 Determinism and resumability

Two fresh runs of OPERATION_OMNIBUS — executed independently into two
separate directories — produced byte-identical `report.json`, `manifest.json`,
checkpoint step files, `outcomes.json` and `provenance.csv`, compared as raw
bytes rather than as decoded objects (`tests/test_determinism_bytes.py`). The
same holds for OPERATION DIAMOND and OPERATION SINGLET. A run interrupted
before the final debrief resumed from the last completed step and produced a
`report.json` byte-identical to a fresh run's — the resumability contract of
§2.3 holds.

The byte comparison itself carries a positive control: a companion test
perturbs one artifact by a single byte and requires the comparison to flag
exactly that file, so a green result means the writers are deterministic
rather than that the comparison is blind. Injecting a wall-clock value into
any persisted record turns the suite red.

### 3.3 Real-film binding

The same runner drives the REAL film packages through the adapter of §2.6:
`goldfinger`, `goldeneye`, `spectre`, and `no_time_to_die` are discovered from
their own `src/` trees as frozen `bond_api` providers and executed as a
mission. The canonical OPERATION OMNIBUS shape over real films runs in
dependency order, every verdict passes, and `goldeneye`'s recon carries a
citation of `goldfinger`'s outputs — the adapter's down-translation of the DAG
edge (§2.6) survives the round trip into a package that has no DAG concept.
Real films also exercise cycle rejection (a `goldfinger ↔ goldeneye` loop is
caught with its ordered path) and the retry policy (a real film wrapped in a
deterministic call-counting fault recovers within its attempt budget and
resumes byte-identically). These are `tests/test_film_binding.py`; they are
not fixtures standing in for films, they are the films.

That module carries no `skipif`. It previously skipped itself when the sibling
film packages were absent, which meant this section's claim went green with no
evidence behind it in any checkout lacking those packages. Absence is now a
hard failure — `TestRealFilmEvidenceIsRequired` names this section in its
failure message — so §3.3 is red whenever its evidence is missing. This was
verified by repointing the module at an empty tree: the presence gate and the
real-film binding tests went red together. (The count of tests that turn red is
deliberately not quoted here — it drifts as the suite grows, and a stale figure
would decay into a false claim about a control that was genuinely run.) A fork
that cannot supply the film packages must delete this section, not silence the
tests.

### 3.4 Provenance

The run emitted one provenance record per executed step and per debrief
(`output/data/provenance/outcomes.json` + `provenance.csv`), every record
carrying the deterministic run id, package, provider, phase, outcome, and
numeric metrics.

### 3.5 Stage plan and retry outcome

OPERATION_OMNIBUS's wavefront decomposition (see §2.5) resolved into
**3** parallel stages with an achievable parallelism of
**1** and a critical path of
**3** stages:

```
1: goldfinger | 2: goldeneye | 3: no_time_to_die
```

Because the chain is serial, every stage is single-package: no concurrency is
available, and the critical path equals the package count — exactly the shape
a serial chain must have. The diamond-shaped OPERATION DIAMOND is the
contrasting case: its two dependency-free leaves share stage 1, so its
achievable parallelism exceeds one while its critical path is shorter than its
package count.

The run's retry ledger recorded **0** retried steps under
the configured policy of **1** maximum attempts. A
retry record exists only when a transient failure was actually re-executed
(§2.4), so an empty ledger is evidence of a clean run rather than of a
disabled mechanism — the mechanism itself is exercised under deliberate
fault injection in §3.3.

### 3.6 The measured DAG (figure)

Figure 3.1 is a deterministic text figure assembled from the run's own JSON by
`src/bond_orchestrator/manuscript_variables.py::_dag_figure`: each package
carries its wavefront stage (from `stage_plan`), its debrief verdict, and each
declared hand-off edge is labelled with the upstream recon `outputs` that
actually crossed it. It is the §2.1 DAG as *measured*, so the figure and the
engine are the same object rather than two accounts of it.

```
measured DAG (from the live mission report)
 stage 1 goldfinger verdict=pass
 stage 2 goldeneye verdict=pass
 stage 3 no_time_to_die verdict=pass
 │gold_reserves_t=4200, market_index=0.92─▶ goldeneye
 │emp_shield_rating=0.87, uplink_redundancy=2─▶ no_time_to_die
```

The stage 1 → 2 → 3 chain and the two non-empty edges mirror the
`goldfinger → goldeneye → no_time_to_die` written in §3.1; the single-package-per-stage
width confirms the serial shape §3.5 describes, and the labelled payloads are
exactly the evidence §3.1 quoted in prose.

## Conclusion

BOND-ORCHESTRATOR delivers its Layer 3 contract: multi-package missions run
end-to-end over the `MissionProvider` protocol in deterministic topological
order, with per-step checkpoint/resume and provenance on every outcome, and a
single consolidated debrief per mission. The architecture keeps the protocol,
the DAG machinery, and the runner free of infrastructure imports — pure logic
that any BOND package can depend on — while the thin CLI and scripts remain
glue.

The guarantees demonstrated for OPERATION OMNIBUS — order, resumability,
byte-determinism, and full provenance — transfer to any mission expressed as
a DAG of providers, and they are not confined to the reference providers: the
adapter of §2.6 binds the REAL film packages built to the frozen
`bond_api.MissionProvider` protocol, and §3.3 runs them through the same
runner with the same guarantees intact. The one integration point still
declared rather than wired is provenance delegation to
`bond-utilities.mission_io`: `src/bond_orchestrator/provenance.py` is today an
independent, non-delegating record writer whose schema differs from
`mission_io`'s, and the delegation mapping plus acceptance criteria are tracked
in `TODO.md` and §7.4.

Two design choices carry the rest of the package. Retries were made
*immediate* rather than backed off, because a wall-clock sleep would put a
non-reproducible quantity inside an artifact that has to be byte-stable;
bounded immediate re-attempts recover from a transient fault without giving
that up. And parallel execution was deliberately not implemented: the stage
planner of §2.5 emits the schedule a parallel executor would follow and proves
the achievable concurrency, while the sequential runner remains the reference
implementation of the same order. The plan is the artifact; the concurrency is
a later, separately verifiable step.

## Experimental Setup

### 5.1 Identity and configuration

This manuscript was produced for **BOND-ORCHESTRATOR: A Deterministic Mission DAG Runner**
(Multi-package film missions over the MissionProvider protocol, with cycle-path detection, checkpoint/resume, bounded deterministic retry, parallel-stage planning, real-film binding, and provenance). The package identity is **BOND-ORCHESTRATOR**,
codename **DAG 00**, version **2.5.2**, first author
Daniel Ari Friedman. All identity, publication, and mission parameters are
declared in `manuscript/config.yaml` and injected into this document through
the manuscript-variable pipeline (`scripts/generate_manuscript_variables.py`
→ `src/bond_orchestrator/manuscript_variables.py`; syntax reference in
`manuscript/SYNTAX.md`) — no metric is hand-authored in prose.

### 5.2 Mission parameters

| Parameter | Value |
|---|---|
| Mission name | `OPERATION_OMNIBUS` |
| Package count | `3` |
| Package chain | `goldfinger → goldeneye → no_time_to_die` |
| Lifecycle phases | `brief, recon, plan, execute, debrief` |
| Retry max attempts (configured) | `1` |

### 5.3 Software environment

- Python: the supported floor is `requires-python = ">=3.10"`
 (`pyproject.toml`). The interpreter each gate run actually used is recorded
 alongside the measured results in
 [`docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md) rather than
 asserted here, so this section cannot drift from the machine that ran it.
- `pytest` + `pytest-cov` for the enforced ≥90% line+branch coverage gate on
 `src/` (`pyproject.toml`: `fail_under = 90`, `branch = true`,
 `source = ["src"]`)
- `ruff` (lint + format check) and `mypy` clean on `src/` and `scripts/`
- Runtime dependencies of the pure core: the standard library plus `pyyaml`
 (config parsing only). `bond-api` is a declared path dependency (a relative
 path to the sibling package), imported lazily and required only when real
 film packages are bound (§2.6). This sentence is enforced, not asserted:
 `tests/test_packaging.py` parses `pyproject.toml`, walks the import
 statements of `src/` and `scripts/` with the AST, and fails if a declared
 dependency is imported nowhere or an import is undeclared. Earlier revisions
 declared `numpy`, `matplotlib` and `defusedxml`, none of which this package
 imports; they were inherited from the exemplar it was forked from and have
 been removed.
- No external runtime services and no network access: the reference providers
 are in-process deterministic classes, and the real film packages are
 imported from their own `src/` trees.

### 5.4 Mission surface under test

Every number in this table is a token computed from the mission registry
(`src/bond_orchestrator/missions.py`) through the same
`build_stage_plan` the runner uses — see
`src/bond_orchestrator/manuscript_variables.py::_mission_surface_tokens`.
Earlier revisions typed these counts by hand, contradicting §5.1 four lines
above.

| Mission | Shape | Packages | Hand-off edges | Stages | Max parallelism | Critical path |
|---|---|---|---|---|---|---|
| `OPERATION_OMNIBUS` | serial chain | 3 | 2 | 3 | 1 | 3 |
| `OPERATION_DIAMOND` | two leaves joining one sink | 3 | 2 | 2 | 2 | 2 |
| `OPERATION_SINGLET` | single package | 1 | 0 | 1 | 1 | 1 |

- `OPERATION_OMNIBUS` is the flagship: a serial chain, so its critical path
 equals its package count and no concurrency is available.
- `OPERATION_DIAMOND` is the only shape whose achievable parallelism exceeds
 one; it exercises a multi-dependency join.
- `OPERATION_SINGLET` is the degenerate case, isolating retry and verdict
 behaviour from DAG effects.

The same three shapes are re-run over the REAL film packages through the
adapter of §2.6, so the DAG results are not an artifact of the reference
providers alone.

## Reproducibility

### 6.1 Determinism policy

Determinism is a hard contract, not a preference:

- Providers are pure with respect to their inputs (fixed spec classes in
 `src/bond_orchestrator/providers.py`); there are no random draws and no
 wall-clock dependencies in any report artifact.
- Topological order is canonical (sorted ready-worklist), so execution order
 is declaration-order independent.
- Checkpoint step files, `manifest.json`, `report.json`, `outcomes.json`, and
 `provenance.csv` are written with `sort_keys=True` — byte-stable across runs
 for identical inputs. `tests/test_determinism_bytes.py` enforces this
 boundary at the byte level: it executes each of the three missions twice
 into two separate directories and compares every written file with
 `Path.read_bytes`, so key order, separators, indentation and trailing
 newlines are all in scope. It carries a positive control
 (`TestByteComparisonIsSensitive`) proving the comparison detects a
 one-byte difference, and injecting a wall-clock value into any persisted
 record turns it red. Earlier revisions compared `report.as_dict` — a
 Python `dict` equality that is blind to all of the above.
- Wall-clock timing is never part of a persisted artifact.

### 6.2 Verification commands

```bash
## Enforced gate: tests + ≥90% line+branch coverage on src/
uv run pytest tests/ --cov=src --cov-fail-under=90

## No mocks anywhere in tests/
grep -r "unittest.mock\|MagicMock\|@patch\|create_autospec" tests/ || echo "Clean"

## Packaging + lineage honesty gates (declared-vs-imported dependencies, a
## relative bond-api path, no forked-scaffold slug in any declared value)
uv run pytest tests/test_packaging.py -v

## Reproduce the flagship run + provenance
uv run python scripts/run_mission.py OPERATION_OMNIBUS --checkpoint-dir output/state

## Hydrate manuscript tokens (strict: requires the mission report above)
uv run python scripts/generate_manuscript_variables.py
```

The lineage check is a test, not a `rg` one-liner. The one-liner previously
printed here never reported `Clean`: `rg` skips dotfiles by default, so it was
blind to `.template-export.json` — a stale export manifest whose recorded
`source_project` named the exemplar and whose 1,075 file hashes had decayed to
12 matches and 1,014 deleted paths. That file has been removed. The command
also matched its own text in this manuscript and in `docs/AGENTS.md`, so it
could not have printed `Clean` even on a genuinely clean tree.

What the replacement gate covers, stated so it is not read as more: it scans
every `.py` file under `src/`, `scripts/` and `tests/` for the exemplar slug,
and every scalar *value* of `pyproject.toml`, `manuscript/config.yaml`,
`CITATION.cff`, `codemeta.json`, `.zenodo.json`, `domain_profile.yaml`,
`experiment_plan.yaml` and `export.toml`. It does **not** scan Markdown prose
or configuration comments, because this package's own remediation notes name
the fork source deliberately. Un-forked *narrative* text is therefore not
gated and remains a review responsibility.

### 6.3 Artifact inventory

| Artifact | Producer | Status |
|---|---|---|
| `output/data/mission_report.json` | `scripts/run_mission.py` | Regenerated |
| `output/data/provenance/outcomes.json`, `provenance.csv` | `scripts/run_mission.py` | Regenerated |
| `output/state/<mission>/*.json` | runner checkpoint layer | Regenerated |
| `output/data/manuscript_variables.json` | `scripts/generate_manuscript_variables.py` | Regenerated |

For OPERATION_OMNIBUS (version 2.5.2, first author
Daniel Ari Friedman) the all-verdicts outcome was
**PASS**. Live test counts and measured coverage are
tracked in [`docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md).

## Scope and Related Work

### 7.1 Scope

This package scopes to orchestration only:

- **In scope**: DAG construction and validation with ordered cycle-path
 detection, deterministic topological execution, checkpoint/resume,
 deterministic retry policy, parallel-stage planning, provenance recording,
 canned mission registry, real-film binding, thin CLI.
- **Out of scope**: film business logic (provider concern), mission *choice*
 (coordinator concern), protocol ownership (now `bond-api`'s — see §7.3),
 shared mission I/O once `bond-utilities.mission_io` is adopted (see
 `TODO.md`).

Parallel execution is deliberately deferred: the runner executes sequentially
because determinism and resumability are the load-bearing guarantees. The
stage planner (§2.5) makes the parallelism explicit without changing that
contract — every package in a stage may run concurrently, and the sequential
runner is the reference implementation of the same order.

### 7.2 Related work

Topological sorting of dependency graphs dates to Kahn's algorithm
[@kahn1962topological] and is standard material in algorithms texts
[@cormen2009introduction]. Long-running multi-stage workloads recover from
interruption through checkpoint/rollback-recovery protocols, surveyed in
[@elnozahy2002survey], with distributed snapshots for coordinated state
capture [@chandy1985distributed]; the runner's manifest + per-step state files
follow that pattern specialised for deterministic single-node execution.
Scheduling directed task graphs onto parallel machines by level-by-level
wavefront decomposition is a classic static-scheduling result
[@kwok1999static]; the orchestrator's stage plan is its deterministic,
single-machine specialization. Bounded re-execution of a failing step is
fault tolerance in the dependability sense — masking a transient fault so it
does not become a system failure, while letting a persistent one surface
[@avizienis2004basic]; here it is made deterministic by removing wall-clock
backoff entirely, trading throughput for byte-reproducible artifacts. The
binding between the runner-side contract and the frozen `bond_api` protocol is
a textbook object adapter [@gamma1994design]: neither interface may move, so a
translating wrapper is the only structure that preserves both.

### 7.3 Integration points

Wired (phases 2–3): real film packages built to the frozen `bond-api`
`MissionProvider` protocol are bound through the adapter in
`src/bond_orchestrator/film_providers.py` (`bond-api` is a local path
dependency, imported lazily so the pure core stays liftable without it).

Declared, not yet wired (each tracked with acceptance criteria in `TODO.md`):

- `bond-utilities.mission_io` provenance delegation — `provenance.py` is an
 independent, non-delegating provenance writer today, because its record
 schema differs from `mission_io`'s (key sets share only `codename` and
 `schema_version`). Delegation means writing a mapping and picking a canonical
 record shape first; see `TODO.md` V1/E6.
- `bond-coordinator` mission-spec handoff — coordinator-produced missions (same
 `Mission` shape) should execute unchanged.

### 7.4 Limitations and uncertainty

This section states, in one place, what the package does *not* claim. Each
bullet is grounded in the current code and tracked where it is ongoing work.

- **Provenance is not yet `mission_io`.** `provenance.py` is an independent,
 deterministic writer; its records are the orchestrator's own schema, not
 `bond-utilities.mission_io`'s, and no test compares the two key sets. Until
 the delegation (TODO E6) and its schema mapping (TODO V1) exist, cross-package
 provenance is stored in this package's format, not the suite's shared one.
- **One interpreter is exercised.** Every gate this package has run used a
 single CPython (3.14.6, recorded in `docs/_generated/COUNTS.md`); the
 declared `requires-python = ">=3.10"` floor has not been run on 3.10–3.13
 (TODO V2). The floor is a declaration, not a matrix.
- **Live counts are hand-maintained.** The measured test/coverage figures that
 §5.3 and §6 defer to live in `docs/_generated/COUNTS.md`, which no script
 regenerates (TODO V3). It is updated by hand on every pass and can silently
 go stale; the deferral chain is only as honest as that one leaf.
- **Resuming a changed mission requires a fresh checkpoint dir.** Checkpoint
 resume is bound to the exact mission definition by a recorded hash (TODO C1,
 §2.3): mutate a mission's `depends_on` or package set and the runner refuses
 to replay the old steps. This closes a stale-replay hole but makes an
 in-place, same-directory *edit-and-resume* workflow impossible by design —
 the safe workflow deletes or renames the state dir for a genuinely changed
 mission.
- **Real-film retry cannot rescue a deterministic film.** The adapter caches a
 film's `execute` outcome for the run (determinism safety), so a film that
 fails once yields the same failure on every bounded re-attempt (§2.6, §2.4).
 The retry mechanism therefore demonstrably recovers only *non-deterministic*
 or deliberately fault-injected providers — real films are exercised against
 it with a call-counting fault in `tests/test_film_binding.py`, not as a
 claim that it masks a persistent film bug.
- **Parallel execution is planned, not performed.** The stage plan (§2.5) is a
 scheduling artifact; the runner executes sequentially, so achievable
 concurrency is verified as a property, not delivered as speed. No parallel
 executor or wall-clock performance characterization exists (deliberately:
 wall-clock values would break byte-determinism).
- **Empty-plan packages pass vacuously.** A package whose provider returns an
 empty execution plan records zero execution steps and debriefs `pass`
 (there is nothing to fail). The runner now rejects an *empty mission* at
 graph build (§2.1) so the vacuum cannot hide a misbuilt mission, but a
 single empty-plan provider is still treated as a no-op success.
- **Determinism is single-node and single-interpreter.** Byte-reproducibility
 (§6.1) is demonstrated for fixed seeds and one interpreter on one machine;
 it does not by itself guarantee bit-identical output across Python versions
 or platforms, a question the single-interpreter gap above does not yet
 answer.

## Sources

@kahn1962topological; @cormen2009introduction; @elnozahy2002survey; @chandy1985distributed; @kwok1999static; @avizienis2004basic; @gamma1994design; @bondorchestrator2026


# Bond API — THE PROTOCOL

*infra package · package codename THE PROTOCOL*.

## Concepts — THE PROTOCOL: domain and operational focus

The frozen MissionProvider protocol, registry, discovery, serialization

## Abstract — THE PROTOCOL: mission summary

BOND-API (codename *THE PROTOCOL*) is the frozen mission protocol contract for the BOND film suite — Layer 1 of the suite. It defines 11 frozen dataclasses (Asset, Constraint, Debrief, Finding, MissionBrief, MissionOutcome, MissionPlan, Provenance, ReconReport, ReconRequest, Step) and a 5-method provider contract (brief, recon, plan, execute, debrief) that every film package implements. The package ships the machinery every coordinator needs: deterministic JSON round-trip serialization for all protocol objects, a gadget registry and a mission/package registry for discovered providers, slug-based film discovery on `sys.path`, and 9 capability helpers (brief_issues, derive_provenance, fingerprint, hash_provenance, normalize_debrief, normalize_lessons, plan_schema_issues, require_plan_schema, validate_brief) layered on the frozen surface — soft brief validation, plan-step schema checks, provenance hashing, and debrief normalization. A reference film (sable) exercises the full lifecycle, and the 27 film packages of the suite implement the same contract. Every artifact crosses process boundaries as tagged JSON (reserved key `__bond_type__`), and the suite enforces a 90% line-and-branch coverage floor on `src/`. This is version 0.1.0 of the contract.

## Introduction — THE PROTOCOL: mission framing, the operational problem, and how to read this chapter

The BOND suite is a family of packages that cooperate to run missions:
5 lifecycle stages — brief, recon, plan, execute, debrief —
carry a mission from declaration to debrief. For that cooperation to be
possible, every participant must agree on the shape of the artifacts that
cross its boundaries: what a mission brief contains, what a recon report
looks like, what an outcome must prove about itself.

BOND-API exists to make that agreement explicit and durable. It is *the
protocol*: the single contract every film package implements and every
coordinator consumes. Freezing it first — before any of the 27 film packages
are written — means the films are coded against a stable, tested surface
rather than a moving one.

### What this package provides

- **The protocol** (`src/bond_api/protocol.py`): the frozen dataclasses and
 the runtime-checkable `MissionProvider` contract.
- **Discovery** (`src/bond_api/discovery.py`): find film packages on
 `sys.path` by slug convention — a top-level module named by its slug
 exposing `mission.MissionProvider`.
- **Registries** (`src/bond_api/registry.py`): `GadgetRegistry` for
 film-provided gadgets and `MissionRegistry` for discovered providers.
- **Serialization** (`src/bond_api/serialization.py`): deterministic JSON
 round-trips of every protocol object — no pickling.
- **The reference film** (`films/sable/mission.py`): a real, deterministic
 provider that exercises the full lifecycle and demonstrates the contract.

### Reader's guide

Chapter 2 defines the protocol and the discovery/serialization conventions.
Chapter 3 reports conformance evidence from the test suite. Chapters 5–6
document the environment and reproducibility contract. Chapter 8 is the
honest counterweight: the deliberately permissive boundaries, the wire-format
strictness now enforced, and the places where the evidence is bounded.

## Methodology — THE PROTOCOL: the analytical models and algorithms that drive the mission

### The mission lifecycle

A mission is a deterministic 5-stage flow. Each
stage has one input, one output, and no hidden state:

| Stage | Input | Output |
|---|---|---|
| `brief` | — | `MissionBrief` |
| `recon` | `ReconRequest` | `ReconReport` |
| `plan` | `MissionBrief` | `MissionPlan` |
| `execute` | `MissionPlan` | `MissionOutcome` |
| `debrief` | `MissionOutcome` | `Debrief` |

The orchestrator helper `run_mission(provider, request)` composes the
5 stages in exactly this order and returns the
final `Debrief`. Because the stages are pure functions of their inputs, coordinators can re-run, cache, or
serialize any stage boundary without special-casing a film.

### Frozen dataclasses

Every artifact in the table above is a frozen dataclass (`@dataclass(frozen=True)`):
immutable by construction, value-equal, and validated at construction time.
(Hashability follows Python's rules: an object is hashable when all of its
fields are; opaque payloads such as `Asset.payload` may hold mutable values,
which makes those particular instances unhashable — coordinators should treat
protocol objects as values, not dict keys.) Validation is strict where the
contract demands it — a mission brief must declare a non-empty `film`,
`codename`, and at least one objective; provenance must carry a non-negative
integer seed and a non-empty input hash — and permissive where flexibility is
the point (`Asset.payload` is opaque and JSON-serializable).

### The provider contract

`MissionProvider` is a `typing.Protocol` marked `@runtime_checkable`. A film
package is a top-level module named by its slug exposing
`mission.MissionProvider`; discovery instantiates it, verifies the structural
contract with `isinstance`, and binds it to its slug. A provider that declares
a `film` different from the slug it was discovered under is rejected as an
identity mismatch.

### Discovery

`load_provider(slug, search_paths=...)` imports `<slug>.mission` from the
given search paths (default `sys.path`). `discover(slugs=..., search_paths=...)`
autodetects candidate slugs — top-level directories containing `mission.py` —
or takes an explicit slug list, loading every discoverable provider and
skipping broken ones so one bad film never hides the rest.

#### Failure semantics

Discovery is deliberately strict in one direction and tolerant in the other,
because the two callers want opposite things:

| Situation | `load_provider` (single film) | `discover` (bulk) |
|---|---|---|
| Search path is not an existing directory | `DiscoveryError` | `DiscoveryError` (path validation precedes any loading) |
| Slug is not an importable module name | `DiscoveryError` | slug skipped |
| Package missing, provider absent, constructor raises | `DiscoveryError` | slug skipped |
| Provider fails the structural protocol check | `DiscoveryError` | slug skipped |
| Provider declares a film different from its slug | `DiscoveryError` (identity mismatch) | slug skipped |
| Search-path entry exists but cannot be listed | not reached | entry skipped |

A coordinator asking for one named film wants a loud failure; a coordinator
sweeping the 27-film fleet wants every healthy film to load
regardless of a sick one. The split is not "validation before loading" versus
"failures during loading": slug validation happens *inside* the per-slug load,
which `discover` catches, so an explicitly requested but malformed slug is
skipped exactly like an unimportable one and `discover` returns the healthy
remainder. Search-path validation is the one check that runs before any
loading and therefore raises from `discover` too. Both behaviors are pinned by
`tests/test_discovery.py`; a caller that needs a malformed slug to be loud
must call `load_provider`.
Both paths leave `sys.path` exactly as they found it: entries inserted for the
import are removed in a `finally` block, and the one tolerated exception there
— a film that rewrote `sys.path` itself on import — is documented at the call
site rather than silently swallowed.

### Serialization

Protocol objects serialize to plain JSON via `to_json` / `from_json`. The
wire format is tagged (`{"__bond_type__": "<ClassName>",
...fields}`) so the exact type reconstructs on decode; tuples and lists are explicitly
distinguished; output is key-sorted with fixed indentation so identical
objects produce byte-identical text. No pickling is used anywhere.

### Registries

`GadgetRegistry` maps film slugs to named gadgets (opaque payloads — data,
callables, handlers). `MissionRegistry` is the mission/package registry of
discovered providers, keyed by film slug, filled from `discover` and used by
coordinators to drive providers without touching import machinery again.

### Capability helpers

The frozen contract is deliberately minimal; capability helpers layer
reusable semantics on top of it without changing a single field or flow
(`src/bond_api/capabilities.py`):

- **Soft brief validation** — `brief_issues` / `validate_brief` report
 advisory issues (duplicate asset names, duplicate constraint kinds,
 duplicate objectives, whitespace-slack asset names) that a coordinator may
 tolerate or escalate, complementing the constructor's hard invariants.
- **Plan-step schema checks** — `plan_schema_issues` / `require_plan_schema`
 verify no duplicate step names, well-formed param keys, JSON-serializable
 params, and optionally an exact expected step-name sequence.
- **Provenance hashing** — `fingerprint` is a deterministic SHA-256 over the
 canonical JSON encoding of arbitrary parts; `hash_provenance` fingerprints a
 full provenance record; `derive_provenance` builds a provenance whose
 `input_hash` follows from the mission's inputs, making outcomes auditable
 without re-running the film.
- **Debrief normalization** — `normalize_lessons` / `normalize_debrief` strip,
 drop, and dedupe lessons while preserving first-occurrence order, and
 re-validate the outcome.

All helpers are deterministic and serialize cleanly through the same JSON
surface as the protocol objects they consume.

## Results — THE PROTOCOL: measured outcomes, headline numbers, and what they establish

### Protocol surface

The frozen surface consists of 11 dataclasses —
Asset, Constraint, Debrief, Finding, MissionBrief, MissionOutcome, MissionPlan, Provenance, ReconReport, ReconRequest, Step — and the 5-stage
provider flow (brief, recon, plan, execute, debrief). The surface is verified by
`protocol_surface` and pinned by `tests/test_protocol.py`, so any accidental
addition or removal of a contract type fails the suite.

### Conformance evidence

The test suite is the conformance evidence for the contract. Test counts and
measured coverage are not restated here: they are produced by the run itself
(`uv run pytest tests/ --cov=src`) and the enforced floor is
90% line **and** branch coverage on `src/`, read straight
from the `fail_under` gate declared in `pyproject.toml` rather than repeated
in prose.

- **Round-trip serialization**: every protocol dataclass round-trips through
 `to_json`/`from_json` with exact type and value equality; tuples stay
 tuples, lists stay lists, nested protocol objects stay nested. Exactness is
 now enforced rather than assumed on the two paths that previously broke it:
 a payload dict carrying the reserved wire key is rejected at encode time
 instead of decoding back as a protocol object, and the protocol-type check
 is on class identity instead of class name, so a dataclass whose `__name__`
 shadows a protocol type is rejected instead of being flattened onto that
 type's fields. The wire tag (`__bond_type__`) is published as
 `bond_api.serialization.SERIALIZATION_TAG`, and a test pins the value
 declared in `manuscript/config.yaml` to the live constant, so the format
 cannot drift from its documentation.
- **Registry semantics**: gadget registration/merging/overwrite/drop and
 mission-provider register/lookup/drop are exercised with real providers.
- **Discovery**: the reference film (sable) is discovered by
 slug and by autodiscovery; malformed packages fail with actionable
 `DiscoveryError`s; unreadable search-path entries are skipped rather than
 raised, verified against a real permission-denied directory.
- **Determinism**: the reference film runs the full lifecycle with fixed
 seed and zero wall-clock dependence; outcomes are byte-identical across
 runs. The wire text and the fingerprint digests are pinned to checked-in
 literal goldens (`tests/test_golden_determinism.py`) rather than to
 same-process self-comparisons, and the same goldens are re-derived in a
 freshly spawned interpreter under a randomized hash seed — which is what the
 "across processes" half of the claim asserts. Platform independence is
 established only over the platforms the suite actually runs on; a literal
 golden makes a platform-dependent encoding fail there rather than pass
 silently, but no test in this package can assert an untested platform.
- **Capability helpers**: each of the 9 helpers
 (brief_issues, derive_provenance, fingerprint, hash_provenance, normalize_debrief, normalize_lessons, plan_schema_issues, require_plan_schema, validate_brief) has dedicated tests — advisory brief issues,
 plan-schema matches and violations, SHA-256 fingerprint determinism and
 key-order independence, derived provenance records, and lesson
 normalization (strip/drop/dedupe, first-occurrence order).

### Capability-helper surface

The 9 capability helpers layer reusable semantics on
the frozen contract without changing a field. Their names are public API
(pinned by ``CAPABILITY_NAMES`` and exercised by ``tests/test_capabilities.py``);

| Helper(s) | Role |
|---|---|
| `brief_issues` / `validate_brief` | Advisory brief validation — duplicate asset names, duplicate constraint kinds, duplicate objectives, whitespace-slack asset names |
| `plan_schema_issues` / `require_plan_schema` | Plan-step schema checks — duplicate step names, param-key sanity, JSON-serializable params, optional exact step-name sequence |
| `fingerprint` | Deterministic SHA-256 over the canonical JSON encoding of arbitrary parts |
| `hash_provenance` | Fingerprint of a full provenance record (all four fields) |
| `derive_provenance` | Provenance whose `input_hash` derives from the mission inputs |
| `normalize_lessons` / `normalize_debrief` | Strip, drop, and dedupe lessons preserving first-occurrence order; re-validate the outcome |

Each helper's exact behavior and failure mode is pinned by a dedicated test, and
all of them serialize through the same JSON surface as the protocol objects.

### Gate integrity

Four gates in this package could have passed for the wrong reason, and all
four are now controlled:

- **The unresolved-token gate is non-vacuous.** `resolve_manuscript_tree`
 scans every `NN_*.md` section for leftover brace-delimited tokens. A
 manuscript directory containing no sections would have scanned nothing and
 reported success; strict mode now raises instead, and the test suite pins
 that behavior with a real empty directory.
- **The empty-surface gate has a positive control.** The check that the
 protocol exposes dataclasses lives in `require_surface`, which is called
 directly with a genuinely empty surface in the tests — so the gate is known
 to fire, not merely known to pass on the real package.
- **The determinism assertions pin values, not themselves.** Assertions of the
 form `fingerprint(x) == fingerprint(x)` and `to_json(o) == to_json(o)` hold
 for any deterministic function and cannot fail; they have been replaced by
 literal goldens plus a fresh-interpreter re-derivation.
- **The claim ledger is read by a gate.** `data/claim_ledger.yaml` restates six
 values the package derives elsewhere. Nothing consumed the file, so a stale
 row was undetectable. `tests/test_claim_ledger.py` now re-derives every row
 from its cited source of truth and fails when a row is added without a
 verifier, so the check cannot lapse into covering nothing.

Thin-orchestrator conformance is likewise enforced by machine rather than by
review: a test parses each `scripts/*.py` file with `ast` and fails if a
script grows business logic beyond `main` or stops delegating to `bond_api`.

All tests use real data and real computation — no mocks.

## Conclusion — THE PROTOCOL: findings, verdict, and what the mission establishes

BOND-API freezes the contract the film suite is coded against. Version
0.1.0 delivers:

- a validated, frozen protocol surface (11 dataclasses,
 5 provider stages) with construction-time
 invariant checks;
- deterministic JSON serialization that coordinators and CLIs can rely on
 across process boundaries, under the published reserved key
 `__bond_type__`;
- discovery that finds film packages by slug convention and binds them to
 their identity;
- registries that give coordinators a single place to hold gadgets and
 providers;
- 9 capability helpers (brief_issues, derive_provenance, fingerprint, hash_provenance, normalize_debrief, normalize_lessons, plan_schema_issues, require_plan_schema, validate_brief) layered
 on the frozen surface, adding advisory brief validation, plan-schema
 enforcement, provenance fingerprinting, and debrief normalization without
 altering a single contract field;
- a reference film (sable) and a test suite demonstrating
 the whole contract with real computation.

### What the freeze buys

The value of freezing first is asymmetric. A film package written against a
moving contract pays the migration cost 27 times over; a film
package written against a frozen one pays it never. Everything added since the
freeze — the capability helpers, the published wire tag, the gate-integrity
work — is strictly additive: existing types, fields, defaults, and the
`run_mission` flow are byte-identical to the version the first films compiled
against.

Downstream packages (bond-coordinator, bond-orchestrator, bond-cli, and the
film packages) implement against this version (0.1.0) of the
protocol. The contract stays intentionally frozen: changes require a new
version and a deliberate migration, never a silent edit.

Since the last revision the wire format is strict where loose encoders are
costly: non-finite floats are rejected at both encode and decode, and a
payload dict carrying the reserved __bond_type__ key with an
unrecognised tag value fails loudly rather than silently decoding as an
untagged dict. The honest limits of the package — the deliberately permissive
boundaries, the interpreter-bounded determinism claims, and the provenance
uncertainty — are stated in Chapter 8 rather than left for a reader to
discover.

## Experimental Setup — THE PROTOCOL: canonical scenarios, parameters, and configuration

### Package layout

| Path | Role |
|---|---|
| `src/bond_api/protocol.py` | Frozen dataclasses + `MissionProvider` contract (pure, stdlib only) |
| `src/bond_api/discovery.py` | Slug-based film discovery on `sys.path` |
| `src/bond_api/registry.py` | `GadgetRegistry` + `MissionRegistry` |
| `src/bond_api/serialization.py` | Deterministic JSON round-trips |
| `src/bond_api/capabilities.py` | Soft brief validation, plan schema checks, provenance hashing, debrief normalization |
| `src/bond_api/manuscript_variables.py` | Token hydration from `config.yaml` |
| `films/sable/mission.py` | Reference film implementing the contract |
| `scripts/` | Thin orchestrators (preflight, demo mission, token hydration) |
| `tests/` | Zero-mock test suite |

### Configuration

Protocol parameters live in `manuscript/config.yaml` under `protocol:`
(identity, codename, reference film slug, serialization tag). Token variables
inject them into this manuscript — metrics are never hand-authored in prose.
The current version is 0.1.0.

### Environment

- Python: 3.14.6 (the interpreter that generated this text)
- Manuscript date: 2026-08-04 — read from `manuscript/config.yaml`
 → `paper.date`, a committed value, not a clock read. The generator reads no
 wall clock at all, so regenerating `output/` twice produces byte-identical
 files; see `manuscript/06_reproducibility.md`.
- Only external runtime dependency: `pyyaml` (manuscript config parsing); the
 protocol core is stdlib-only.

### Running the suite

```bash
cd bond-api
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/00_preflight.py
uv run python scripts/demo_mission.py
uv run python scripts/z_generate_manuscript_variables.py
```

## Reproducibility — THE PROTOCOL: verification gates, deterministic regeneration, and artifacts

### Determinism policy

The protocol makes determinism a contract, not a hope:

- every mission outcome carries `Provenance(package_version, seed, input_hash, wall_time_s)`;
- the reference film uses a fixed seed and performs no random draws;
- `to_json` output is key-sorted with fixed indentation, so identical objects
 serialize byte-identically;
- provenance hashing (`fingerprint`, `hash_provenance`, `derive_provenance`)
 uses the SHA-256 secure hash standard [@nist_fips180_4] over the canonical
 JSON encoding, so identical inputs yield identical fingerprints across
 processes and platforms. What is *tested*, in
 `tests/test_golden_determinism.py`: the wire text and four digests are
 pinned to checked-in literals, and re-derived in a freshly spawned
 interpreter under `PYTHONHASHSEED=random`. That binds the cross-process
 claim directly and turns any encoding change into a red test. Platform
 independence is bounded by the platforms the suite is run on — the literals
 fail loudly on a platform that disagrees, but the suite cannot assert a
 platform it has never executed;
- tests use fixed inputs throughout; any future timing assertions must use
 bounds, not exact values, per `docs/testing_philosophy.md`.

### Artifact inventory

| Artifact | Producer |
|---|---|
| `output/data/manuscript_variables.json` | `scripts/z_generate_manuscript_variables.py` |
| `output/manuscript/*.md` (token-resolved sections) | `scripts/z_generate_manuscript_variables.py` |

`output/` is disposable: regenerate, never hand-edit.

#### Regeneration is byte-identical

Both artifacts above are byte-identical across repeated regeneration on one
interpreter: running `scripts/z_generate_manuscript_variables.py` twice writes
the same bytes, no matter how much time passes between the runs. This holds
because `generate_variables` reads **no wall clock**. Every token resolves
from a committed source — the live package surface, `manuscript/config.yaml`,
or the `fail_under` gate in `pyproject.toml`. The manuscript date is
`paper.date` from the config, a value that changes in a diff rather than on
every run.

The scope of that claim, stated exactly:

- **In scope**: repeated runs of the generator on the same interpreter produce
 identical bytes for `output/data/manuscript_variables.json` and every file
 under `output/manuscript/`.
- **Out of scope**: a *different* interpreter. `PYTHON_VERSION` is the one
 environment-derived token, so upgrading Python deliberately changes those
 bytes — that is the token doing its job, and the manuscript says which
 interpreter produced its text.

This is bound by `tests/test_regeneration_determinism.py`, which runs the real
generator script twice into two directories, sleeps across a whole-second
boundary between them so any clock read would show, and compares every output
file byte for byte. A companion `ast` gate fails if a wall-clock call is
reintroduced into the generator module, and that gate carries a positive
control — it is fed a source that *does* read the clock and must flag it, so
it cannot pass by scanning for something it would never find.

### Token hydration

Every token in `manuscript/*.md` resolves through
`src/bond_api/manuscript_variables.py::generate_variables`, which reads
its sources of truth — live code, configuration, and gate declarations —
and never a hand-typed value:

| Token group | Source of truth |
|---|---|
| Identity, surface inventory, capability list | the live package (`protocol_surface`, `CAPABILITY_NAMES`) |
| Version, title, subtitle, reference film, film count | `manuscript/config.yaml` |
| Wire-format tag | `bond_api.serialization.SERIALIZATION_TAG` |
| Coverage floor | the `fail_under` gate in `pyproject.toml` |
| Manuscript date | `manuscript/config.yaml` → `paper.date` (committed, never a clock read) |
| Python version | the running interpreter |

Deriving the coverage floor from `pyproject.toml` rather than from prose or
config means the manuscript quotes the gate that actually runs; deriving the
wire tag from the module means renaming the tag breaks the build rather than
the documentation.

Three checks keep this honest: the strict-mode script fails on any unresolved
token; `tests/test_manuscript_variables.py` cross-references every manuscript
token against the generator; and strict resolution refuses to report success
over an empty section set, so the token gate cannot pass by scanning nothing.

`data/claim_ledger.yaml` is the one place that deliberately restates
code-derived values outside the token map. It is not self-certifying prose:
`tests/test_claim_ledger.py` re-derives every row from the source the row
cites and fails on a row with no verifier.

## Scope and Related Work — THE PROTOCOL: boundaries, positioning, and relationship to the literature

### Scope

BOND-API defines *what* missions are and *how* films plug in; it does not run
missions. Explicitly out of scope for this package:

- mission scheduling, orchestration, or coordination (bond-coordinator,
 bond-orchestrator);
- film content — the 27 film packages implement `mission.MissionProvider`;
- CLI surface and user tooling (bond-cli);
- shared helpers for the suite (bond-utilities), when that package lands;
- any mutation of the protocol after this freeze — changes require a versioned
 migration, not a silent edit.

### Design relationship

- **Film packages**: implement the contract exactly as `films/sable/mission.py`
 does — discoverable by slug, deterministic, self-describing briefs.
- **Coordinators**: consume `discover` + `MissionRegistry`, move artifacts
 with `to_json`/`from_json`, and never import film internals.
- **bond-utilities**: not yet available as a utilities package; BOND-API
 currently depends only on the stdlib plus `pyyaml`. The integration point is
 tracked in `TODO.md`.

### Related standards

The protocol follows the same conventions as the template it was scaffolded
from — frozen dataclasses for value objects, `typing.Protocol` for structural
contracts, deterministic serialization, and a zero-mock test discipline — so
code moving between template projects and the BOND suite keeps its shape.

## Limitations and Uncertainty — THE PROTOCOL: assumptions, threats to validity, and what the numbers do not claim

Every engineering claim in this manuscript is scoped honestly. This section
collects the limits that a hostile reviewer of a protocol library would care
about — where the package is deliberately permissive, where a value is a
declared contract rather than a measurement, and where a reader should not
over-read the evidence.

### Deliberately permissive boundaries (documented, not bugs)

These are accepted design decisions, recorded so nobody re-litigates them:

- **`discover` silently skips an invalid slug.** Slug validation happens
 inside `load_provider`, whose `DiscoveryError` `discover` catches, so
 `discover(slugs=["9bad-slug"])` returns the healthy remainder rather than
 raising — the "one broken film never hides the rest" design. The strict
 entry point is `load_provider`, which raises. A caller who passes a
 typo'd slug to `discover` gets silence, not an error; both sides are pinned
 by `tests/test_discovery.py`.
- **`sys.modules` caches slug imports.** Two film packages sharing a slug in
 different locations cannot both load in one interpreter. Distinct slugs per
 location are required.
- **Discovery mutates `sys.path` for the duration of an import** and restores
 it in a `finally` block. This makes concurrent discovery from multiple
 threads unsafe by construction; discovery is a startup-time operation.
- **Protocol objects with mutable payloads are unhashable.** Value equality,
 not dict-key semantics — coordinators should treat protocol objects as
 values, not hash keys.
- **`run_mission` executes `recon` but does not thread its report into
 `plan`.** The frozen signature is `plan(brief)`; callers needing the report
 drive the five stages directly.
- **The manuscript PDF is rendered outside this package.** This package ships
 token hydration and validation only; rendering runs in the monorepo
 `infrastructure.rendering` pipeline over `output/manuscript/`.

None of these is a defect; each is a trade-off chosen for the frozen contract
and stated at its call site and in the test suite.

### Wire-format strictness (enforced since Round 2)

The serialization layer is strict where loose encoders are costly. Two holes
were closed and are now pinned by regression tests:

- **Non-finite floats are rejected.** RFC 8259 defines no `NaN` or `Infinity`
 token, yet Python's `json.dumps` writes them as bare literals by default. A
 non-finite float anywhere in a payload — including `Provenance.wall_time_s`,
 where `inf >= 0` used to pass the non-negativity check — is now rejected at
 encode time and at decode time (a foreign document carrying `NaN`/`Infinity`
 fails loudly rather than decoding to a float the encoder could never
 re-emit). This narrows `to_json`/`from_json` to plain, portable JSON.
- **The reserved wire key must carry a known tag.** A payload dictionary whose
 `__bond_type__` value is `null`, `false`, `0`, or `[]` used to
 fall through to the plain-dict branch and decode as an untagged dict that
 the encoder then refused to re-encode. Every such tag is now loud, so
 `to_json(from_json(doc))` is total over the documents `from_json` accepts.

### Where the evidence is bounded

- **Coverage is a floor, not a proof.** The enforced gate is
 90% line **and** branch coverage on `src/`
 (`--cov-fail-under=90`); the measured figure is whatever
 the suite prints, never restated here. Line and branch coverage across the
 six `src/` modules is intentionally not quoted, because it changes with the
 code.
- **Determinism is bounded by the interpreter.** `to_json` output and the
 provenance fingerprints are byte-deterministic and pinned to checked-in
 literal goldens, re-derived in a freshly spawned interpreter under
 `PYTHONHASHSEED=random` (the "across processes" claim). Platform
 independence is established only over the platforms the suite actually runs
 on; no test in this package can assert a platform it has never executed on.
- **Regeneration is byte-identical per interpreter.** `output/` regenerates to
 identical bytes on one interpreter because `generate_variables` reads no
 wall clock. `3.14.6` is the single environment-derived token, so
 upgrading Python deliberately changes those bytes — that is the token doing
 its job.

### Uncertainty in provenance

`Provenance.wall_time_s` is a recorded duration for auditability, not a
causal claim: nothing in this package asserts a wall-clock bound, and the
reference film stamps `0.0` by design so outcomes are reproducible regardless
of when they run. Where timing is measured by a film package, the value must
be finite (rejected by construction if not) and interpreted with any
timing-measurement granularity caveats the measuring package documents
(`docs/testing_philosophy.md`: use bounds, not exact values, for timing).

### Versioning uncertainty

The package version 0.1.0 is declared in four places
(`pyproject.toml`, `bond_api.__version__`, `manuscript/config.yaml` →
`paper.version`, and the reference film's provenance stamp). All four are
gated to agree by `tests/test_exports.py`, so a bump edited in only one place
fails the suite instead of silently shipping stale metadata. The gate makes
drift detectable, but it does not make the version a single loaded value —
that single-source refactor is tracked in `TODO.md` if a future round wants
it.

## Sources — THE PROTOCOL: bibliography

@pep544; @pep557; @pep484; @rfc8259; @nist_fips180_4; @bond_api


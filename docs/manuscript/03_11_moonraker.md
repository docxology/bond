# Moonraker (1979) — MOONRAKER

*film package · package codename MOONRAKER*. Mission **DRAX**: model the shuttle hijack as a critical-path timeline; solve Drax station orbital logistics; certify a centrifuge g-force training profile; size the Hohmann resupply transfer and propellant; plan the centrifuge training regimen under exposure caps; crash the hijack timeline to a tighter deadline at minimum cost.

## Concepts — MOONRAKER: domain and operational focus

orbital logistics, centrifuge ops

## Abstract — MOONRAKER: mission summary

**Moonraker: DRAX — Special-Agent Mission Software** — Critical-Path Hijack Timelining and Crashing, Orbital Logistics and Resupply Rendezvous, and Certification of Centrifuge G-Force Training. Mission codename **DRAX**, modelled on the 1979 film *Moonraker*, is a deterministic special-agent mission-software package. It operationalises the DRAX mission across three concept areas: the space-shuttle hijack as a critical-path timeline (including minimum-cost schedule crashing), Drax space-station orbital logistics (Kepler orbit physics, launch windows, consumables, the Hohmann resupply transfer and its propellant budget, and a Clohessy–Wiltshire rendezvous), and the centrifuge g-force training programme (the g-tolerance envelope plus an exposure-capped weekly regimen). The shuttle hijack plan completes in **57.0 minutes** across **8 phases**, feasible within the 60.0 point of no return (margin **3.0 min**), and can be crashed to a **50.0-minute** deadline at a cost of **23.0**. The DRAX station at 350.0 km has an orbital period of 5483.6 s and admits up to **450** per resupply cycle as a logistics ceiling (the station's own crew is 6) on the configured cadence. A Hohmann resupply transfer costs **0.0874 km/s** over **44.9 minutes**, needing **238.2 kg** of propellant; the final Clohessy–Wiltshire approach requires a **1.875 m/s** impulse. The **6.0 g** training profile is **not certified**: its 12.0 s plateau overruns the **7.26 s** tolerance allowance by **4.74 s**. At the weekly level the exposure caps still admit **4** sessions of **97.5 g·s**. Every result is a closed-form, deterministic computation — no random draws, no external calls, no wall clock — enforcing the suite's reproducibility contract. Manuscript dated 2026-08-05, rendered on Python 3.14.6 (Darwin).

## Introduction — MOONRAKER: mission framing, the operational problem, and how to read this chapter

*Moonraker* (1979) sends special agent James Bond to intercept Hugo
Drax's plan to destroy humanity from his private space station. Beneath the
set-pieces — a shuttle hijacked at a NASA launch tower, Drax's orbital station
with its centrifuge room, and the g-force chamber where Bond trains — lies a
computational core this package makes rigorous and reproducible.

**Moonraker: DRAX — Special-Agent Mission Software** (codename **DRAX**) turns those set-pieces
into three concept areas, carried by seven pure domain modules.

**1 · The shuttle hijack.** `moonraker.shuttle_ops` models the takeover as an
activity network solved with the Critical Path Method, identifying the
load-bearing phases and checking feasibility against the shuttle's point of no
return. `moonraker.schedule_crashing` answers the follow-on question the film
never asks: if the window closes early, which phases do you buy down, and what
does the compression cost? It runs the classic greedy time-cost crash over the
same CPM solver.

**2 · The station and its resupply.** `moonraker.orbital_logistics` supplies
Kepler orbital mechanics (period, velocity, orbits per day), the ground launch
windows a resupply craft can use, pass geometry, and a closed-form consumables
model binding crew size, stock and resupply cadence.
`moonraker.orbital_transfer` flies the resupply: a Hohmann two-burn transfer
sized by vis-viva, the phase wait that aligns chaser to target, a Tsiolkovsky
propellant budget, and the deorbit burn home. `moonraker.rendezvous` closes the
last few kilometres with linearised Clohessy–Wiltshire relative motion and a
closed-form single-impulse intercept.

**3 · The g-force programme.** `moonraker.centrifuge` gives the ramp/sustain/
decay profile of a centrifuge run, the g↔rpm physics, and a safety verdict
against a +Gz tolerance envelope and a procedural plateau ceiling.
`moonraker.centrifuge_training` lifts that from one run to a regimen: g·s
exposure dosing, gradual-onset-rate tolerance scaling, and weekly session
planning under daily and cumulative exposure caps.

Two composition modules sit above these. `moonraker.mission_results` is the
single canonical computation every consumer reads, and
`moonraker.manuscript_variables` turns it into the brace-delimited token map
this manuscript is written against. `moonraker.figures` renders the PNGs.

The package implements the frozen BOND-API `MissionProvider` protocol in
`moonraker/mission.py`, so the BOND suite orchestrator can discover and drive
it through the standard brief → recon → plan → execute → debrief lifecycle.

### Reader's guide

- All seven domain modules are pure and infrastructure-free: they import
 nothing but the standard library, so they can be lifted and tested anywhere.
- `mission.py` is the thin adapter between the BOND protocol and the domain
 core, and the only module that imports `bond_api`.
- `scripts/` provides one CLI per mission phase plus a flagship runner that
 regenerates every artifact.
- The manuscript's numeric claims are injected from
 `docs/manuscript/config.yaml` + `moonraker/manuscript_variables.py`, never
 hardcoded in prose. Where a computed verdict contradicts the film — as the
 centrifuge certification does — the manuscript reports the computation.

## Methodology — MOONRAKER: the analytical models and algorithms that drive the mission

All models are deterministic and closed-form; parameter values are read once
from `docs/manuscript/config.yaml` → `mission:` and shared by
`moonraker/mission_results.py` and `moonraker/manuscript_variables.py`.

### Shuttle hijack timeline (`shuttle_ops.py`)

The hijack is a set of `TimelineActivity` records — a name, a duration in
minutes, and prerequisite phases. `compute_timeline` runs the Critical Path
Method [@kelley1959critical]: a forward pass sets the earliest start of each
activity to the maximum earliest finish of its prerequisites; a backward pass
sets the latest finish to the minimum latest start of its successors. Total
float (slack) is the difference between late and early finishes; activities
with zero slack are **load-bearing**. Those are reported two ways, because a
network can carry several equally-long critical paths and then the zero-slack
*set* is their union rather than a route: `critical_activities` is the set, and
`critical_chains` enumerates the distinct source-to-sink paths by walking only
the *tight* zero-slack edges (an edge counts when the predecessor's earliest
finish equals the successor's earliest start). The network is validated before
solving — duplicate names, dangling prerequisites and dependency cycles are
rejected by a Kahn-style strip — so a malformed timeline fails loudly instead
of producing a plausible schedule. `timeline_feasibility` then checks the plan
against the shuttle's point of no return, 60.0 minutes from
launch.

**Time-cost crashing** (`schedule_crashing.py`) compresses the timeline when
the deadline tightens. Every `CrashableActivity` carries a normal duration, a
minimum (crashed) duration and a linear cost per minute saved.
`crash_schedule` runs the classic greedy crash: it re-solves the CPM, picks the
cheapest still-crashable activity currently carrying zero slack, and crashes it
one minute at a time until the deadline is met or compression is exhausted. The
crashable network is *derived* from `DRAX_HIJACK_TIMELINE` — durations and
dependency edges are read from it, and only the crash limit and cost per minute
are authored separately — so the crashed and uncrashed totals the results
section subtracts are always measured on the same plan.

### Space-station orbital logistics (`orbital_logistics.py`)

Kepler's third law gives the circular-orbit period $T = 2\pi\sqrt{a^3/\mu}$
with $a = R_\oplus + h$; the circular speed is $v = \sqrt{\mu/a}$. Orbits per
day divide the sidereal day by $T$. Ground launch windows open at each
half-period plane crossing and stay open for the usable pass at a minimum
elevation. `windows_in_horizon` then keeps only the windows that both open and
close inside a launch planning horizon of 4.0 hours,
giving
$n = \lfloor (H - t_{\text{pass}}) / (T/2) \rfloor + 1$, or zero when the
horizon is shorter than one pass. The reported window count is that filtered
number: it falls as the station climbs and rises with the horizon, and no
parameter names it directly. The consumables model is linear:
`consumables_days = capacity /
(crew × per-capita rate)`, and `sustainable_crew` floors the largest crew that
survives the 6.0-day resupply cadence.

**Orbital transfer** (`orbital_transfer.py`) flies the resupply from a
200.0-km parking orbit up to the station with the
Hohmann transfer: two tangential burns sized by the vis-viva equation
$v = \sqrt{\mu(2/r - 1/a)}$, a half-ellipse transfer time
$t = \pi\sqrt{a^3/\mu}$ [@hohmann1925], and a deterministic phase-wait that
aligns the chaser to the target's lead angle. The rocket equation
$m_0/m_f = \exp(\Delta v/(I_{\text{sp}} g_0))$ [@tsiolkovsky1903] sizes the
propellant. Its $m_f$ is the **burnout** mass, and this campaign takes that to
be the dry structure plus the delivered consumables, because the cargo is
released only after circularisation and so rides through both burns; that mass
basis is published as a token rather than left implicit, so the multiplication
in §Results can be redone by hand. A retrograde burn drops the perigee for
deorbit.

**Rendezvous guidance** (`rendezvous.py`) models the final approach in the
station's local-vertical/local-horizontal frame with the linearised
Clohessy–Wiltshire equations [@clohessy1960]. `cw_propagate` propagates the
relative state and `single_impulse_intercept` solves for the single corrective
impulse that zeroes the relative position at a chosen time (raising on the
geometric singularities where a single-impulse transfer is impossible).

### Centrifuge g-force profiles (`centrifuge.py`)

Centripetal acceleration maps to g via $g = (2\pi\,\mathrm{rpm}/60)^2 r / g_0$.
`build_training_profile` produces a ramp → sustain → decay g-level trace at
0.5 g/s up and 1.0 g/s down.
A deterministic power-law tolerance envelope $t = \min(800\,g^{-2.5},\,60)$
bounds the sustainable duration, following the shape of the classical +Gz
tolerance curves [@stoll1956human].

`profile_is_safe` then adjudicates the plateau against **two** independent
ceilings and reports the tighter one as the governing allowance: the
*physiological* ceiling — the envelope at peak g, derated by a
20.0% safety margin — and the *procedural* ceiling
30.0 s, the longest plateau the training protocol
permits irrespective of tolerance. A separate
peak-g ceiling of 9.0 g rejects the run outright. Both duration
ceilings are live: `tests/test_centrifuge.py` demonstrates a run that clears
physiology and is refused on procedure alone. The verdict for the DRAX profile
is reported in §Results and is *not* asserted here.

**Training regimen** (`centrifuge_training.py`) doses the programme in g·s.
**Two** functions produce the regimen result reported in §Results:
`profile_exposure` integrates the +Gz exposure above baseline, and
`plan_training_cycle` enforces daily and weekly exposure caps to return the
sustainable session count — a regimen bounded by the physiology of +Gz
tolerance [@burton1988].

The module also implements `gor_tolerance_multiplier`, which scales tolerated
duration with the gradual-onset rate (slower onset → longer tolerated time).
**It is not part of any reported number.** No mission result, manuscript token
or figure consumes it, and neither the certification allowance in §Results nor
the session count above credits the onset rate. The reported regimen is
therefore onset-rate–independent: it is what the model computes without that
credit, and the function is provided and tested but unused. Wiring it in would
change the numbers this paper reports; the honest statement today is that it
does not.

## Results — MOONRAKER: measured outcomes, headline numbers, and what they establish

All numbers below are computed by `moonraker/mission_results.py` and injected
as tokens — the manuscript never hand-authors a metric. The consolidated table
collects the headline values; each is a live token whose resolved value appears
in `output/manuscript/03_results.md`.

| Concept | Metric | Value |
|---|---|---|
| Hijack timeline | Total duration | 57.0 min |
| Hijack timeline | Distinct critical paths | 2 |
| Crashed to deadline | Final duration | 50.0 min |
| Crashed to deadline | Minimum crash cost | 23.0 |
| Station | Orbital period | 5483.6 s |
| Station | Usable windows (4.0 h) | 6 |
| Station | Stores depletion | 450.0 days |
| Station | Sustainable crew (per cycle) | 450 |
| Transfer | Total Δv | 0.0874 km/s |
| Transfer | Propellant | 238.2 kg |
| Rendezvous | Intercept impulse | 1.875 m/s |
| Centrifuge | Peak / allowance | 6.0 g / 7.26 s |
| Centrifuge | Verdict / remediation | not certified / certified |
| Training | Sessions admitted per week | 4 |

### Shuttle hijack timeline

The hijack finishes in **57.0 minutes** over
**8 phases**. The network carries
**2** distinct critical paths, each
57.0 minutes long: **infiltrate_launch_tower → assume_ground_control → spoof_telemetry → rendezvous_drax_station; infiltrate_launch_tower → neutralise_shuttle_crew → launch_shuttle → execute_orbital_insertion → rendezvous_drax_station**. Their union
— the load-bearing, zero-slack activity set — is
**infiltrate_launch_tower, assume_ground_control, neutralise_shuttle_crew, launch_shuttle, execute_orbital_insertion, spoof_telemetry, rendezvous_drax_station**. That set is *not* itself a route: two of
its consecutive members are on different paths and are not linked by any
dependency, so delaying any one of them delays the mission while only the
listed paths can be walked end to end. Against the
60.0-minute point of no return the plan is
**yes**, with a margin of **3.0 minutes**.

![The shuttle-hijack critical-path Gantt chart.](output/figures/moonraker_timeline_critical_path.png)

If the operation must complete in **50.0 minutes**, schedule
crashing compresses the plan to **50.0 minutes** — saving
**7.0 minutes** — at a minimum cost of **23.0**
by crashing **infiltrate_launch_tower, neutralise_shuttle_crew, spoof_telemetry**. The saving is a subtraction within one
network: the crashable model reads its durations and dependency edges from the
same `DRAX_HIJACK_TIMELINE` that produced the 57.0-minute
total, adding only the per-activity crash limit and cost.

### Space-station orbital logistics

The DRAX station at 350.0 km altitude has an orbital
period of **5483.6 s**, a circular speed of
**7.701 km/s**, and completes **15.7**
orbits per sidereal day. Over a 4.0-hour launch
planning horizon, **6** ground launch windows both open
and close in time to be usable — the count is the horizon divided by the
half-period after allowing for one full pass, not a requested number: raising
the station lengthens the period and drops the count, and a horizon shorter
than a single pass admits none. With
5400.0 kg of consumables delivered and a per-capita rate of
2.0 kg/person/day, the stores last
**450.0 days** — the depletion horizon for the configured
6 crew — and a single resupply can sustain up to
**450** people for the 6.0-day
cadence. That last figure is a **per-cycle logistics ceiling, not a
habitability claim**: it is capacity divided by (cadence × per-capita rate),
and the station's own crew is the far smaller 6. It is also
deliberately distinct from the 450.0-day stores figure:
the two only coincide at the shipped cadence and crew.

![Orbital period versus altitude with the DRAX station's launch windows.](output/figures/moonraker_orbit_period_windows.png)

#### Resupply transfer and rendezvous

Flying from the 200.0-km parking orbit up to the station
with a Hohmann transfer costs **0.0438 + 0.0436 =
0.0874 km/s**, over a **44.9-minute**
half-ellipse. The chaser must wait **43.9 h** for the
**3.0°** lead angle. On a 300.0 s engine
the rocket equation gives a mass ratio of **1.03015**. The mass
that ratio acts on is the **burnout** mass — what the craft still weighs when
the second burn ends — which here is
**7900.0 kg**: the 2500.0 kg dry
structure *plus* the 5400.0 kg of consumables, since the cargo
is delivered after circularisation and is therefore accelerated by both burns.
So the propellant is
7900.0 × (1.03015 − 1) =
**238.2 kg**; deorbit adds
**0.0733 km/s**. The final
Clohessy–Wiltshire approach needs a **1.875 m/s**
corrective impulse over **1200 s**.

![The Hohmann resupply transfer geometry.](output/figures/moonraker_hohmann_transfer.png)

### Centrifuge g-force profile and training regimen

A **6.0 g** run on an 8.0 m arm
demands about **25.9 rpm**. The governing allowance at that peak
is **7.26 s** — the +Gz tolerance envelope derated by the
20.0% safety margin, which here is tighter than the
30.0 s procedural ceiling. The DRAX profile's
12.0 s plateau therefore overruns the allowance by
**4.74 s**, and the run is **not certified**
(``CENTRIFUGE_SAFE = no``).

This is a substantive negative result, not a modelling artefact: the shooting
script's training sequence is *outside* the survivable envelope this package
computes, and the model reports so rather than being tuned until it agrees.
The remediation the model implies is itself computed, not inferred: holding the
plateau at **7.26 s** — cutting
**4.74 s** from the 12.0 s plateau —
yields a **certified** run
(``REMEDIATION_SAFE = yes``) under the same tolerance and
procedural ceilings. `tests/test_mission_results.py` pins both the failing
verdict and the certification of this remediated profile, so this paragraph
cannot drift away from the computation.

Each session accumulates
**97.5 g·s** of exposure; under the
150.0 g·s daily and
400.0 g·s weekly caps, the
**4-session** weekly programme is
**yes**, and the caps admit **4**
sessions per week.

![The centrifuge g-level profile with the g-duration tolerance envelope.](output/figures/moonraker_centrifuge_g_profile.png)

![Weekly centrifuge training load against the exposure caps.](output/figures/moonraker_training_weekly_load.png)

## Conclusion — MOONRAKER: findings, verdict, and what the mission establishes

**Moonraker: DRAX — Special-Agent Mission Software** (codename **DRAX**) turns the set-pieces of
*Moonraker* into a verified, deterministic mission-software package. Its
concepts — the shuttle-hijack critical-path timeline with minimum-cost
crashing, the DRAX station's orbital logistics (Kepler orbits, launch windows,
consumables, the Hohmann resupply transfer, and Clohessy–Wiltshire
rendezvous), and the centrifuge training programme (the g-tolerance envelope
plus an exposure-capped regimen) — are pure, infrastructure-free computations
with closed-form answers and full provenance.

The hijack plan is **yes** inside its
60.0-minute deadline and can be crashed to
**50.0 minutes** for **23.0**; the station's
logistics admit up to **450** per resupply cycle as a
ceiling (its own crew is 6) with a
**0.0874 km/s** resupply transfer; and the weekly regimen
admits **4** sessions under the exposure caps.

The one negative verdict is the load-bearing one. The
**6.0 g** profile is **not certified**: its
12.0 s plateau exceeds the **7.26 s**
allowance by **4.74 s**. A model that only ever agrees
with its source material is not a model, and the value of injecting every
number is precisely that a result can come back unwelcome. Every figure and
every number in this manuscript is regenerated from source — nothing is
hand-written — which is the reproducibility contract the BOND suite demands.

## Experimental Setup — MOONRAKER: canonical scenarios, parameters, and configuration

### Mission parameters

All parameters live in `docs/manuscript/config.yaml` → `mission:` and are read by
`moonraker/mission_results.py`:

| Parameter | Value | Consumed by |
|---|---|---|
| Hijack point of no return | 60.0 min | `shuttle_ops` |
| Tightened crash deadline | 50.0 min | `schedule_crashing` |
| Station altitude | 350.0 km | `orbital_logistics` |
| Crew | 6 | `orbital_logistics` |
| Resupply capacity | 5400.0 kg | `orbital_logistics` |
| Per-capita consumption | 2.0 kg/person/day | `orbital_logistics` |
| Resupply cadence | 6.0 days | `orbital_logistics` |
| Parking-orbit altitude | 200.0 km | `orbital_transfer` |
| Engine specific impulse | 300.0 s | `orbital_transfer` |
| Resupply dry mass | 2500.0 kg | `orbital_transfer` |
| Deorbit target perigee | 100.0 km | `orbital_transfer` |
| Intercept time | 1200.0 s | `rendezvous` |
| Centrifuge arm | 8.0 m | `centrifuge` |
| Centrifuge target g | 6.0 g | `centrifuge` |
| Sustained plateau | 12.0 s | `centrifuge` |
| Ramp / decay rate | 0.5 / 1.0 g/s | `centrifuge` |
| Peak-g ceiling | 9.0 g | `centrifuge` |
| Procedural plateau ceiling | 30.0 s | `centrifuge` |
| Tolerance safety margin | 20.0% | `centrifuge` |
| Daily exposure cap | 150.0 g·s | `centrifuge_training` |
| Weekly exposure cap | 400.0 g·s | `centrifuge_training` |
| Planned sessions per week | 4 | `centrifuge_training` |

These values are shared, single-source parameters; the manuscript consumes them
via token injection from `moonraker/manuscript_variables.py`, never as
hardcoded prose. `MISSION_DEFAULTS` in `moonraker/mission_results.py` mirrors
this block so the domain core stays runnable without reading a config file, and
any key the config omits falls back to it.

### Running the setup

```bash
uv sync --extra dev
uv run python scripts/run_mission.py # results + figures
uv run python scripts/z_generate_manuscript_variables.py # tokens + resolved tree
```

### Software environment

- Python 3.14.6 on Darwin.
- Declared dependencies: `matplotlib`, `pyyaml`, and `bond-api` (the frozen
 BOND suite protocol); `numpy` is pulled transitively by matplotlib and is not
 imported by any module in this package.
- Determinism: fixed parameter set, no random draws, no wall-clock inputs in
 any persisted artifact.

## Reproducibility — MOONRAKER: verification gates, deterministic regeneration, and artifacts

### Determinism guarantees

Every module in this package is deterministic by construction:

- The seven domain modules use only closed-form mathematics — CPM and greedy
 time-cost crashing, Kepler's laws, the vis-viva and Tsiolkovsky relations, the
 Clohessy–Wiltshire state transition, and the centrifuge physics — over a fixed
 parameter set. There is no RNG anywhere in `src/`, no wall-clock input to any
 computation, and no network or filesystem read inside the domain core.
- `moonraker/mission.py` carries a fixed seed and records a stable SHA-256
 `input_hash` over the serialized plan plus package identity, so an outcome can
 be audited without re-running the mission. `Provenance.wall_time_s` is
 deliberately `0.0`: a timing figure would make otherwise-identical runs differ.
- `moonraker/mission_results.py` is the single canonical computation. Its
 factories (`compute_schedule`, `compute_orbit`, `compute_centrifuge`,
 `compute_transfer`, `compute_rendezvous`, `compute_training`,
 `compute_crash`) are what the mission `execute` adapter, the manuscript
 token map **and** `moonraker/figures.py` all call, each on the same parameter
 dict read from `docs/manuscript/config.yaml`. No figure declares a mission
 constant of its own — `tests/test_figures.py` parses the module and fails if
 one reappears — so an outcome value, its injected token and the plotted
 figure cannot disagree.
- Figures are rendered through the headless `Agg` backend with fixed inputs.
- `moonraker/manuscript_variables.py` reads no wall clock. The manuscript's
 date token, `MANUSCRIPT_DATE`, is the committed `paper.date` field of
 `docs/manuscript/config.yaml`, not the moment the generator ran, and
 `generate_variables` takes no `now` argument that could reintroduce one.

Running `scripts/run_mission.py` followed by
`scripts/z_generate_manuscript_variables.py` restores a byte-identical
`output/` tree — every file, on any later re-run, on the same interpreter and
platform. The scope of that claim is exact: two token values, `PYTHON_VERSION`
and `PLATFORM`, are read from the running interpreter, so they change if the
package is regenerated on a different machine or Python build. Nothing else in
the tree varies. Elapsed time in particular does not: `Provenance.wall_time_s`
is pinned to `0.0` and no date or timestamp is sampled anywhere.

`TestRegenerationIsByteIdentical` in `tests/test_regeneration_determinism.py`
binds this end to end — it runs both scripts twice into an isolated tree and
compares a SHA-256 of every regenerated file — and
`TestNoWallClockInPersistedPath` parses every module under `src/moonraker/` and
`scripts/` and fails on any wall-clock call, with a positive control proving
the parser detects one when it is present. An earlier version of this section
claimed byte-identity while the abstract carried a `datetime.now` timestamp;
the only test guarding it injected a fixed `now`, which is precisely why the
contradiction survived.

### What a reader can re-derive

| Artifact | Command |
|---|---|
| `output/data/mission_results.json` | `uv run python scripts/run_mission.py` |
| `output/figures/*.png` (five figures) | `uv run python scripts/run_mission.py` |
| `output/data/manuscript_variables.json` | `uv run python scripts/z_generate_manuscript_variables.py` |
| `output/manuscript/` (token-resolved prose) | `uv run python scripts/z_generate_manuscript_variables.py` |

`output/` is git-ignored throughout: it is regenerable, never authoritative, and
never hand-edited.

### Verification gate

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/ tests/ && uv run ruff format --check src/ scripts/ tests/
uv run mypy src/ scripts/
```

The coverage gate enforces ≥90% line **and** branch coverage on `src/` with zero
mocks — no `unittest.mock`, no `MagicMock`, no monkeypatched collaborators in the
domain tests. Every assertion runs the real algorithm on real parameters.

Two test classes exist specifically to keep this manuscript honest.
`TestLiveCrossReference` in `tests/test_manuscript_variables.py` reads every
numbered section on disk and fails if any brace-delimited token it uses is
absent from the generated map, so prose can never reference a variable that no longer exists.
`TestComputeMissionResults` pins the centrifuge certification verdict in both
directions, so the negative result reported in §Results cannot silently invert.
`TestConfigKnobsAreConsumed` sweeps **every** key in `MISSION_DEFAULTS` — the
probe table must cover the parameter set exactly, so a knob added without one
fails the suite — and asserts each one moves at least one published value when
flipped. One knob, the peak-g ceiling, is exercised from a shortened plateau
rather than the shipped defaults, because the DRAX plateau already fails the
duration ceiling and no peak-g value could change that verdict; the test says
so in place.

## Scope and Related Work — MOONRAKER: boundaries, positioning, and relationship to the literature

### Scope

This package models three **closed-form** aspects of the DRAX mission as a
deterministic research exemplar. Everything it computes is a two-body,
linearised or linear-cost approximation chosen so the answer can be audited by
hand.

Deliberately **not** modelled:

- Atmospheric ascent and re-entry trajectories; the shuttle timeline ends at
 docking and the deorbit burn is sized but not flown.
- Orbital perturbations — drag, the J2 oblateness term, third-body effects,
 solar radiation pressure. Orbits are ideal circular two-body orbits, so the
 launch-window series in `orbital_logistics` does not precess.
- Full three-dimensional, multi-burn rendezvous guidance. The
 Clohessy–Wiltshire model in `rendezvous` is linearised about a circular
 reference orbit and is valid only for separations small against the orbit
 radius; `single_impulse_intercept` raises rather than returning a number at
 the geometric singularities (whole-period intercept times) where the
 single-impulse assumption fails.
- Six-degree-of-freedom centrifuge biodynamics. `centrifuge` treats +Gz as a
 scalar level against a population-average tolerance envelope, with no
 individual variation, no anti-G straining manoeuvre, no G-suit and no
 cumulative fatigue between sessions.
- Stochastic activity durations. The hijack network is deterministic CPM with no
 PERT-style distribution over phase durations, so there is no confidence
 interval on the 57.0-minute total.
- Onset-rate credit in the training regimen. `centrifuge_training` implements
 `gor_tolerance_multiplier`, but nothing published consumes it: the reported
 allowance and session count are onset-rate–independent (see §Methodology).

Each simplification is also documented at its point of use — for example the
linear elevation-threshold shrinkage in `orbital_logistics.pass_duration` and
the power-law fit in `centrifuge.max_sustained_duration`.

### Related work

| Model | Module | Source |
|---|---|---|
| Critical Path Method | `shuttle_ops.py` | Kelley & Walker (1959) [@kelley1959critical] |
| Time-cost crashing | `schedule_crashing.py` | Kelley & Walker (1959) [@kelley1959critical] |
| Kepler two-body orbits, pass geometry | `orbital_logistics.py` | Vallado (2013) [@vallado2013astrodynamics] |
| Hohmann two-impulse transfer | `orbital_transfer.py` | Hohmann (1925) [@hohmann1925] |
| Rocket equation | `orbital_transfer.py` | Tsiolkovsky (1903) [@tsiolkovsky1903] |
| Linearised relative motion | `rendezvous.py` | Clohessy & Wiltshire (1960) [@clohessy1960] |
| +Gz tolerance envelope | `centrifuge.py` | Stoll (1956) [@stoll1956human] |
| +Gz exposure dosing (GOR scaling implemented but unpublished) | `centrifuge_training.py` | Burton (1988) [@burton1988] |

The time-cost crashing trade-off is the cost extension of the same Kelley &
Walker scheduling work that introduces CPM. This package implements the greedy
crash along the critical path rather than the equivalent linear programme; for
the strictly linear per-minute cost structure used here the two agree.

Within the BOND suite, `moonraker` is the orbital-logistics package. Adjacent
packages model neighbouring physics — orbital capture and hidden-base discovery
(`you_only_live_twice`), orbital weapon targeting geometry
(`diamonds_are_forever`, `die_another_day`) and orbital EMP effects
(`goldeneye`). Per the suite layering rule these packages never import one
another; shared mechanics would live in `bond-utilities` or `bond-api`.

## Sources — MOONRAKER: bibliography

@kelley1959critical; @vallado2013astrodynamics; @stoll1956human; @moonraker1979; @hohmann1925; @clohessy1960; @tsiolkovsky1903; @burton1988


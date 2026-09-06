# The Spy Who Loved Me (1977) — LIPARUS

*film package · package codename LIPARUS*. Mission **LIPARUS**: detect, localise and track a passive-acoustic contact; simulate a Liparus-Class tanker capture, verify submersible conversion and hull viability.

## Concepts — LIPARUS: domain and operational focus

submarine tracking, marine forensics

## Abstract — LIPARUS: mission summary

The Spy Who Loved Me: LIPARUS — Special-Agent Mission Software is a deterministic special-agent mission model built around the concepts of *The Spy Who Loved Me* (1977) under mission codename LIPARUS. It comprises 6 standalone, infrastructure-free domain modules — passive acoustic detection and bearing-only tracking, Liparus-class tanker capture, submersible vehicle conversion forensics, underwater acoustics and the passive sonar equation, uniform-linear-array beamforming, and pressure-hull collapse/ballast analysis — exposed to the BOND fleet through a frozen `MissionProvider` adapter. Every *measured* quantity in this manuscript is computed live by the domain core rather than hand-authored, and The results section marks the one reported number that is a declared constant instead — the capture timeline. The passive detector declares the contact at a controlled false-alarm probability of 0.001 (margin 11.0 dB), and the two tracking estimators agree on the geometry: batch target-motion analysis recovers the quarry's position to within 65.4 metres of truth while the recursive extended Kalman filter settles to a steady-state position error of 804.5 metres over the same run. The ULA beamformer resolves the contact to within one 0.5-degree scan cell of the true bearing (an error of 0.0 degrees) and, with the opt-in parabolic refinement of the peak, to within 0.112 degrees against a Cramer-Rao floor of 0.33 degrees (The results section explains why the measured grid error is grid-limited rather than CRB-limited). The passive sonar equation yields a detection range of 83746 metres, and the Esprit-grade pressure hull survives to a collapse depth of 85 metres (a safety factor of 2.13 at its operating depth of 40 metres) while requiring 244 L of ballast to reach neutral buoyancy. All simulations are seeded and fully deterministic, and the test suite holds line and branch coverage on `src/` at or above 90%.

## Introduction — LIPARUS: mission framing, the operational problem, and how to read this chapter

In *The Spy Who Loved Me* (1977), Bond confronts two icons of hydraulic
malevolence and mechanical possibility: the *Liparus*, a supertanker whose
hull opens like a mouth to swallow whole submarines, and the Lotus Esprit, a
road car that converts into a functional submersible. Both demand the same
kind of engineering reasoning that a special-agent mission plan needs: detect
the unseen contact, reason about capture geometry, and verify that a vehicle
can actually survive underwater.

This package — mission codename LIPARUS — realises those
capabilities as deterministic, testable software across
6 concept modules. It is one package in the
PROJECT BOND suite, a set of film-themed mission packages made compatible by
the frozen `bond_api` mission protocol. The domain core is deliberately
independent of that protocol: the pure modules in
`src/the_spy_who_loved_me/` compute results with no knowledge of any
orchestrator, and the thin `mission.py` adapter in the same package exposes
them under the standard five-stage lifecycle (brief, recon, plan, execute,
debrief).

The structure of the package is:

| Module | Concept |
|---|---|
| `sub_tracking.py` | Passive acoustic detection and bearing-only tracking |
| `tanker_capture.py` | Liparus-class tanker swallowing-submarine simulation |
| `vehicle_forensics.py` | Submersible vehicle conversion forensics |
| `acoustics.py` | Underwater propagation and the passive sonar equation |
| `beamforming.py` | Uniform-linear-array beamforming and bearing estimation |
| `hull_forensics.py` | Pressure-hull collapse and ballast analysis |

Three further modules carry no domain concept of their own but hold the
package together: `scenario.py` is the single canonical parameter set and
metric factory that both the mission adapter and the manuscript hydration
consume (so an outcome and a printed number cannot disagree),
`manuscript_variables.py` turns those metrics into the substitution tokens
this document is written in, and `mission.py` is the thin frozen
`bond_api.MissionProvider` adapter plus gadget registry.

The six concepts compose rather than sit side by side: `acoustics.py` sets
the detection budget that says whether a contact is audible at all,
`sub_tracking.py` decides whether it *was* heard and where it is going,
`beamforming.py` converts the array's raw snapshot into the bearing that
tracking consumes, `tanker_capture.py` asks whether the quarry physically
fits inside the Liparus, and `vehicle_forensics.py` and `hull_forensics.py`
together answer the Lotus Esprit question from two sides — paperwork
(requirement traceability) and physics (collapse depth and ballast).

The remainder of this manuscript describes the algorithms (The methodology section), their measured results (The results section), and the
deterministic experimental setup (The setup section).

## Methodology — LIPARUS: the analytical models and algorithms that drive the mission

### Passive acoustic detection and bearing-only tracking

`src/the_spy_who_loved_me/sub_tracking.py` models the sensor problem of a
passive array hunting a submarine that emits nothing deliberately.

**Detection** uses a Neyman–Pearson energy detector
(`detect_contract`). A received waveform is split into non-overlapping
windows; each window statistic `T = sum(x^2)/noise_var` is compared against a
threshold. Under the noise-only hypothesis `T ~ chi^2(window)`, so the
threshold is the `(1 - P_FA)`-quantile of that chi-square distribution,
computed in closed form with the Wilson–Hilferty approximation
(`chi2_quantile`), whose standard-normal-quantile primitive is Acklam's
algorithm (`inverse_normal_cdf`). The detector therefore makes its decision
at a controlled false-alarm probability `P_FA`, and `Detection.margin_db`
reports the statistic-to-threshold margin.

**Tracking** is the harder problem. `simulate_target_track` generates a
deterministic scenario: a constant-velocity submarine observed by a
*maneuvering* ownship (a dogleg course change), yielding noisy relative
bearings. The maneuver is not cosmetic — a fundamental result of passive
sonar is that a constant-velocity target's absolute range and speed are
*unobservable* from a stationary observer (the whole trajectory can be
scaled and produce identical bearings). Only a change of observer course
renders the state observable.

`estimate_tma` then performs batch least-squares target motion analysis:
over the state `[px, py, vx, vy]` it minimises the sum of squared bearing
residuals
`sum_i (bearing_i - atan2(p_y + v_y t_i - o_y, p_x + v_x t_i - o_x))^2`,
initialised by a coarse grid search over range/course/speed and refined by
Gauss–Newton.

That grid search is **bounded, and its bounds bracket the canonical
scenario**: candidate initial ranges run 3000–6500 m in 500 m steps and
candidate speeds 5–35 m/s in 5 m/s steps, against a canonical truth of
4000 m and 25 m/s. This is a declared search envelope, not a property of the
estimator, and canonical accuracy is therefore not evidence about arbitrary
geometry. The degradation outside it is graceful rather than a cliff — with
only the initial range varied, a 15 km target is still recovered to 293 m
because Gauss–Newton escapes the poor seed, while a 60 km target leaves a
25 km error (42% of range) that widening the range bound to 80 km cuts to
4.9 km. `estimate_tma` accepts keyword overrides for the envelope, and
`tests/test_sub_tracking.py::TestCoarseSearchEnvelope` pins all three of
those measurements.

`PassiveBearingTracker` is the matching recursive Extended Kalman Filter for
online use, with the relative-bearing measurement model and a
constant-velocity transition; its `measurement_noise_rad` is a bearing
standard deviation and is squared into the measurement covariance `R`.
`tracking_rms_error` reports steady-state accuracy.

### Liparus-class tanker capture

`src/the_spy_who_loved_me/tanker_capture.py` models the *Liparus* swallowing
a submarine as a deterministic geometric-feasibility check plus a
discrete-event sequence. `clearance_metrics` computes the per-axis margins
between a `SubmarineSpec` and a `BayConfig` mouth/hold, and
`classify_clearance` labels the fit `fits` / `tight` / `denied` against a
required safety margin. `stowage_capacity` is how many submarines the hold
can stow. `simulate_capture` runs the four-phase operation (approach,
ingress, hatch-seal, secure) and returns a `CaptureRun` with a per-phase
timeline and final status.

Only two of those four phases test anything. *Ingress* requires the mouth to
clear the submarine's beam and depth by the safety margin, and *secure*
requires the hold to clear its length by the same margin; *approach* and
*hatch-seal* always succeed. No seal-integrity quantity is modelled anywhere
in the package, so the hatch-seal stage has nothing of its own to check — a
`seal_requirement` field on `BayConfig` supplied the appearance of one until
it was removed, because the constructor validated it into `[0, 1]` and the
predicate then compared it against `1.0`, a conjunct that could never be
false. The per-phase durations are likewise declared constants, not a timing
model; The results section says what that means for the reported elapsed
time.

### Submersible vehicle forensics

`src/the_spy_who_loved_me/vehicle_forensics.py` forensically assesses
whether a road vehicle can be converted to submersible duty.
`SUBMERSIBLE_REQUIREMENTS` is a traced requirement set (pressure hull,
watertight seals, ballast, air supply, and optional systems). `assess_conversion`
scores the spec, `classify_conversion` maps the result to `road-only`,
`amphibious`, or `submersible`, and `recommend_upgrades` returns the missing
critical systems as an ordered retrofit list. `buoyancy_status` applies
Archimedes' principle (`F_b = displacement * rho_water * g` vs weight) to
classify the as-spec vehicle `floats` / `neutral` / `sinks`.

### Underwater acoustics and the passive sonar equation

`src/the_spy_who_loved_me/acoustics.py` puts numbers on the *medium* the
Liparus and its quarry move through. `thorp_absorption` implements the Thorp
(1967) seawater absorption coefficient, ``transmission_loss`` combines
geometric spreading with absorption to give ``TL(r) = n*10*log10(r) +
alpha*r``, and `sound_speed_m_s` implements the Mackenzie (1981) equation.
The passive sonar equation in signal-excess form
``SE = SL - TL - (NL - DI) - DT`` (`passive_sonar_equation`) is the detection
budget, and `detection_range_m` solves for the maximum detectable range by
monotone bisection of the strictly-increasing transmission loss — the range
at which the signal excess reaches zero.

Signal excess is not the signal-to-noise ratio, and the two are kept apart
here because this package previously called the quantity above an SNR in
code, prose and test names. Following Urick [@urick_principles_1983], the
array-output SNR is ``SL - TL - (NL - DI)`` — larger than the signal excess
by exactly the detection threshold ``DT``, and available as
`signal_to_noise_ratio_db`. With the canonical budget the difference is
10 dB, so calling the figure of merit an SNR
overstates the margin by that much.

### Uniform-linear-array beamforming

`src/the_spy_who_loved_me/beamforming.py` turns the array's raw snapshots
into a bearing. `steering_vector` gives the plane-wave phase progression
``a(theta) = exp(-j 2 pi (d/lambda) k sin(theta))``; `array_snapshot`
produces a deterministic seeded snapshot; the conventional (delay-and-sum)
beamformer ``P(theta) = |a(theta)^H x|^2`` (`beam_power`) is scanned by
`estimate_bearing_deg` to locate the contact. `cramer_rao_bearing_std_deg`
reports the Cramer-Rao lower bound on the bearing estimate — the theoretical
floor the estimator cannot beat (Van Trees, *Optimum Array Processing*
[@van_trees_2002]).

Two properties of this estimator matter for reading The results section.
First, the peak search runs over a *discrete* grid, so the estimate is
quantised to the grid step and its measured error is floored at half a step
regardless of array quality — the statistical bound reported by the CRB and
the error achievable on this grid are different quantities, and on this
scenario the latter is the binding one. Second, the element SNR passed to
the CRB is derived in `scenario.py` from the snapshot amplitude and noise
standard deviation rather than declared independently, so the bound always
describes the array that was in fact sampled.

### Pressure-hull and ballast forensics

`src/the_spy_who_loved_me/hull_forensics.py` checks that the converted
vehicle can actually dive. `hoop_stress_pa` evaluates the circumferential
stress ``sigma = p r / t``; `elastic_buckling_pressure_pa` gives the
long-cylinder buckling pressure ``p_cr = E (t/r)^3 / (4(1-nu^2))`` and
`yield_pressure_pa` the strength limit ``p_y = sigma_y t / r``;
`collapse_depth_m` is the governing (minimum) collapse pressure expressed as
a depth in seawater. `ballast_volume_m3` applies Archimedes to find the
flood-water volume needed for neutral buoyancy — the threshold between a
road car and a submarine.

Flooding a tank adds mass at constant displaced volume, so neutral buoyancy
is `D rho g = (m + V rho) g`, giving `V = D - m/rho`: positive when the
vehicle displaces more than it weighs and must be made heavier to dive,
negative when it is already denser than the water it displaces. The
module's published derivation previously read `(D + V) rho g = m g`, which
solves to the negation of what the code computes, and read the negative case
backwards as well. The code was right and the derivation wrong; the
derivation is corrected rather than the code. `vehicle_forensics.buoyancy_status`
uses the same seawater density as this module, so the two verdicts on one
vehicle describe one fluid — it used fresh water at 1000 kg/m³ until this was
fixed.

### Mission orchestration

`src/the_spy_who_loved_me/mission.py` adapts the six domain modules to the
frozen `bond_api` protocol: it implements `MissionProvider` (brief, recon,
plan, execute, debrief) with a fixed seed, exposes deterministic results
(with a validated collapse-depth safety factor) with full `Provenance`, and
registers the concept functions as gadgets on a `GadgetRegistry`.

## Results — LIPARUS: measured outcomes, headline numbers, and what they establish

All numbers in this section are hydrated from the deterministic domain core
(the canonical scenario); the simulator is seeded so the outputs are
reproducible exactly. One of them — the capture timeline under *Liparus
capture* — is a **declared constant** rather than a computed quantity, and is
labelled as such where it appears. The rest are measured.

### Detection

The Neyman-Pearson energy detector is the gate the whole
downstream tracking chain stands behind: every conclusion below presupposes a
contact was heard at all. On the canonical waveform the detector declares the
contact **yes**, with a statistic-to-threshold margin of
11.0 dB at a false-alarm probability of 0.001.
The margin is the number that matters operationally — how far the peak energy
statistic sits above the threshold the detector was asked to hold — and the
false-alarm probability is the operating point it was required to meet. No
other number in this section is meaningful if that predicate is false.

### Passive tracking

The canonical scenario observes a constant-velocity submarine over
60 bearing samples. Batch target motion analysis recovers
the quarry's initial position to within 65.4 metres of
truth (velocity error 0.5 m/s) — well inside the
operating envelope of the tracking geometry.

The matching recursive extended Kalman filter runs the *same* bearing
sequence and settles to a steady-state position error of
804.5 metres. The two numbers are not competing claims but
one pipeline at two latencies: the batch estimate is the offline maximum-likelihood
answer (here the tighter of the two), while the filter is what a real receiver
could produce in real time as the bearings arrive. The bearing track figure overlays
the true trajectory, the TMA estimate, and the maneuvering ownship path.

![Passive bearing-only tracking: true track vs TMA estimate and ownship path.](output/figures/the_spy_who_loved_me_bearing_track.png)

### Passive sonar equation

Against the canonical budget the passive sonar equation returns a detection
range of 83746 metres (figure of merit 100 dB)
in a channel whose sound speed is 1490 m/s and whose
absorption is 0.0184 dB/km at the 400 Hz scan
tone.
The sonar detection range figure shows how the solved range grows with the
contact's source level.

![Passive sonar detection range vs source level.](output/figures/the_spy_who_loved_me_sonar_detection_range.png)

### Beamforming

The 8-element ULA estimates the contact bearing at
30.0 degrees, 0.0 degrees from truth,
against a Cramer-Rao floor of 0.33 degrees.

That measured error must be read carefully rather than as a precision claim.
`estimate_bearing_deg` is a peak search over a discrete scan grid of
0.5 degrees, so its output is quantised and its error
cannot exceed 0.25 degrees for any snapshot whose
peak lands in the correct cell — *including* an error of exactly zero when,
as in the canonical scenario, the true bearing
(30 degrees) falls on a grid node. A reported error
below the Cramer-Rao bound is therefore an artefact of grid alignment, not
evidence that the estimator beats the statistical floor, which no unbiased
estimator can do. The honest statement is the two-sided one: the beamformer
resolves the contact to within one scan cell, and the CRB of
0.33 degrees — finite and comfortably below the
0.5-degree grid — says the array geometry and SNR would
support a finer estimate than this grid can express.
`tests/test_beamforming.py` pins the quantisation property on *off-grid*
bearings, where the artefact cannot hide it. The opt-in parabolic refinement
(`estimate_bearing_deg(..., interpolate=True)`) exists precisely to approach
the CRB rather than stay floored at the grid: it fits a parabola through the
peak node and its neighbours and reports the apex. On the canonical (grid
aligned) true bearing the grid reports an error of exactly zero — a
snapshot-noise artefact of the node landing on the truth — while the refined
estimate settles at 0.112 degrees, a sub-cell
residual it can actually achieve against the 0.33 degree floor.
The two errors are therefore reported as what they are: the grid figure is
what this grid commits the estimator to, the refined figure is what the
estimator itself can reach, and the off-grid tests in `test_beamforming.py`
show the refinement strictly beating the grid where the grid is genuinely
limited. The beamforming response figure shows the beamformer power response with
the true and estimated bearings marked.

![ULA beamformer response vs bearing.](output/figures/the_spy_who_loved_me_beamforming_response.png)

### Liparus capture

For a bay whose hold is 140 metres long with a
16-metre mouth and a required clearance of
1.5 metres, the canonical swallow succeeds and stows
1 submarine(s) per pass. The capture feasibility figure shows the
per-axis clearance margins across a sweep of submarine sizes.

The capture model reports an elapsed time of 630
seconds over 4 phases, and that number is **not a
result**. It is the sum of four fixed per-phase durations declared in
`tanker_capture._PHASE_DURATIONS` — assumptions with no cited source and no
timing model behind them. Nothing in the simulation makes a phase duration
depend on the submarine or the bay, so the total is identical for a 10-metre
boat and a 72-metre one, and identical for a capture that succeeds and one
that fails at the *secure* stage. The only thing it varies with is how far
the operation got before aborting: a run that fails at ingress reports two
phases instead of four. `tests/test_tanker_capture.py::TestReportedTimeIsASchedule`
pins exactly those properties rather than pinning the total, which would have
been a constant dressed as a measurement.

Two of the four phases likewise carry no discriminating predicate. *Approach*
always succeeds, and *hatch-seal* succeeds whenever ingress did, because no
seal-integrity quantity is modelled anywhere in the package. The feasibility
verdict is therefore pure geometry: mouth clearance at ingress, hold-length
clearance at secure.

![Liparus dock-mouth feasibility by submarine size.](output/figures/the_spy_who_loved_me_capture_feasibility.png)

### Vehicle conversion forensics

The Lotus-Esprit-grade conversion spec achieves a readiness score of
0.67 and is classified **submersible** with
0 missing critical systems.
The conversion readiness figure renders the requirement traceability across the
canonical road-car, amphibious, and submersible grades.
Physically, the 40-metre operating hull collapses
only at 85 metres (safety factor
2.13, feasibility yes), and reaching neutral
buoyancy calls for 244 L of ballast water.

![Submersible conversion readiness by requirement.](output/figures/the_spy_who_loved_me_conversion_readiness.png)

### Mission outcome

The `MissionProvider` execute stage runs all six concept modules against the
canonical scenario and returns a deterministic `MissionOutcome` whose
`success` flag is true only when the contact is detected, the capture
succeeds, and the hull is feasible at operating depth, together with full
`Provenance` (package version, seed, input hash). The input hash is a
SHA-256 over the canonical parameter set, so it moves when any input does —
see The reproducibility section, which also records what it used to be.

## Conclusion — LIPARUS: findings, verdict, and what the mission establishes

LIPARUS (LIPARUS) delivers faithful, deterministic models of the
defining technologies of *The Spy Who Loved Me*: passive acoustic detection
and bearing-only tracking that honestly respect the observer-maneuver
requirement, a Liparus-class capture simulation grounded in exact clearance
geometry, submersible vehicle forensics with physical (Archimedean)
feasibility and requirement traceability, the underwater acoustics and
passive-sonar equation that set the detection budget, ULA beamforming that
recovers the contact's bearing to within one scan cell and reports the
Cramer-Rao floor honestly as the statistical limit the grid cannot express,
and pressure-hull collapse/ballast analysis that verifies the conversion can
actually dive.

The domain core is infrastructure-free and completely standalone, while the
thin `mission.py` adapter makes it discoverable and drivable by the larger
BOND fleet through the frozen `bond_api` protocol — six concept modules
behind one unchanged provider shape. Every claim in the manuscript is
generated by an actual algorithm run and the full suite enforces at least
90% line and branch coverage on `src/` with zero mocks.

## Experimental Setup — LIPARUS: canonical scenarios, parameters, and configuration

The package runs under Python 3.14.6. The manuscript variables
are hydrated by `scripts/z_generate_manuscript_variables.py`, which computes
metrics live from the domain core and resolves every manuscript token in
this tree.

### Canonical scenarios

Every parameter below is a substitution token read back out of
`src/the_spy_who_loved_me/scenario.py`, the module that actually configures
the run — the prose cannot describe a scenario the code did not execute.

* **Detection**: the Neyman-Pearson energy detector is run at a
 false-alarm probability of 0.001 (a fixed seeded waveform).
* **Passive tracking (batch)**: a 600-second scenario at
 a 10-second cadence, yielding 60 bearing
 samples; the target travels at 25 m/s on course
 90° from an initial range of 4000 m;
 the ownship runs a deterministic dogleg (east then north); relative
 bearings are corrupted by 0.5° of seeded noise.
* **Passive tracking (recursive)**: the extended Kalman filter is seeded with
 a coarse initial guess (the batch solution would be an oracle here) and a
 constant-velocity transition; its steady-state error is reported in The results section alongside the batch result.
* **Liparus capture**: a 140 m hold,
 16 m × 14 m mouth, and
 1.5 m required clearance swallowing a
 72 m submarine.
* **Vehicle forensics**: a Lotus-Esprit-grade spec
 (1800 kg dry mass, 2.0 m^3
 displacement) with the critical submersible systems fitted.
* **Passive sonar**: a 160 dB source against a
 70 dB noise floor and 20 dB array
 directivity at 400 Hz; sound speed at 10 °C /
 35 PSU at the surface.
* **Beamforming**: a half-wavelength ULA of 8 elements
 observing a 30° bearing at 20 dB
 element SNR (seeded snapshot), scanned on a 0.5° grid.
 The element SNR is *derived* from the snapshot amplitude and noise standard
 deviation rather than declared separately, so the Cramer-Rao bound in
 The results section always describes the array that was actually sampled.
 The grid estimate is the canonical (honest) one; the parabolic refinement
 described in The results section is an opt-in alternative, not the default,
 so the grid-limitation result is reproducible and the two are comparable.
* **Pressure hull**: a 0.8 m radius, 20 mm
 steel (350 MPa yield) cylinder operating at
 40 m depth.

### Mission identity

The mission runs under codename LIPARUS with package version
0.1.0 and a fixed seed. It serves 6
concept modules to the BOND fleet through `bond_api` discovery and the
`GadgetRegistry`.

### Verification

Coverage and lineage are enforced by the package guardrails:
90% line and branch on `src/`, no mock framework, no
leftover template lineage, and a clean `git status` after a path-scoped
commit. The quoted floor is itself read from `[tool.coverage.report]
fail_under` in `pyproject.toml` by
`manuscript_variables.coverage_floor_pct`, so this sentence cannot claim a
gate stricter than the one that actually runs.

## Reproducibility — LIPARUS: verification gates, deterministic regeneration, and artifacts

LIPARUS is reproducible by construction.

* **Determinism**: every algorithm is a pure function of its inputs and a
 fixed seed; the simulator uses no untracked random draws and no wall-clock
 value in persisted artefacts. Re-running the canonical scenarios on one
 interpreter yields byte-identical results, which
 `tests/test_manuscript_variables.py::TestPersistedArtefactIsDeterministic`
 enforces by regenerating the variable map twice and comparing it, and by
 rejecting any token whose value parses as a timestamp. The *figures* are
 likewise byte-identical across renders —
 `tests/test_figures.py::TestFigureDeterminism` renders `build_all_figures`
 twice and compares the PNG bytes, so a matplotlib bump or an embedded
 creation stamp fails the suite rather than silently falsifying this claim. The single
 environment-dependent token is `PYTHON_VERSION`, which is reported in
 The setup section precisely so a reader can tell which interpreter a given
 artefact came from; the claim is byte-identity per interpreter, not across
 interpreters. (A `GENERATION_TIMESTAMP` token used to be written into
 `output/data/manuscript_variables.json`, which made every regeneration
 differ and this bullet false. It was removed, not softened — no manuscript
 section consumed it.)
* **Seeding**: the tracking scenario is driven by a fixed seed and the
 mission provider carries that same `seed` in its `Provenance`, alongside
 the package version (0.1.0) and an input hash.
* **Input hash**: the `Provenance.input_hash` is a SHA-256 over a stable
 serialisation of the canonical parameter set
 (`scenario.canonical_input_hash`), so editing any canonical input changes
 it and re-running unchanged inputs does not. It was previously the fixed
 string `"liparus-mission-input"`, which identified the package rather than
 the inputs and could not have changed if the scenario had — the one thing
 an input hash exists to detect.
 `tests/test_scenario.py::TestCanonicalInputHash` perturbs every parameter
 in turn and asserts the digest moves, so a parameter that stops reaching
 the hash fails the suite.
* **Persisted provenance**: the `mission_cli` ``execute`` artefact
 (`output/data/mission_outcome.json`) now carries the outcome's full
 `Provenance` block — package version, seed, and the input hash — alongside
 the results, so the hash this section describes is actually in the artefact
 a reader would audit. It used to be printed to stdout and then discarded;
 `tests/test_scripts_smoke.py` asserts the written file resolves the hash to
 `scenario.canonical_input_hash`.
* **Docs bound to the run**: the claim ledger's numeric `value`s are resolved
 against the live canonical metrics (or the declared schedule) by
 `tests/test_repo_contracts.py::TestDocsAgreeWithTheRun`, and the package
 version is cross-checked across every declaration site including the
 manuscript `AGENTS.md`, `config.yaml.example` and the agent `SKILL.md` — so
 a number in `scenario.py` or a version in a metadata file that drifts from
 the claim or the run turns the suite red.
* **Real data only**: tests exercise the actual algorithms on generated,
 deterministic data — no mock framework anywhere in `tests/`.
* **Regenerable artefacts**: figures and reports land under `output/`, which
 is git-ignored; `scripts/generate_figures.py` and
 `scripts/z_generate_manuscript_variables.py` rebuild them deterministically.
* **Verification**: `uv run pytest tests/ --cov=src --cov-fail-under=90`,
 `ruff check`/`format`, `mypy`, and the lineage scan are the acceptance
 gate before any commit.

## Scope and Related Work — LIPARUS: boundaries, positioning, and relationship to the literature

### Scope

This package models *detection*, *tracking*, *bearing estimation*,
*propagation*, *capture geometry*, and *conversion forensics* at a level
appropriate to deterministic, reproducible research software. Each model is
first-order by design, and the boundaries are worth stating precisely
because they are where the results stop being trustworthy:

* **Propagation** is a range-independent budget: geometric spreading plus
 Thorp absorption. There is no sound-speed profile, no ray tracing, no
 surface/bottom interaction, no convergence zones and no shadow zones — so
 the solved detection range is an upper bound in an idealised channel, not
 a field prediction.
* **Tracking** assumes an ideal constant-velocity target and a precisely
 known ownship path. Neither manoeuvring targets nor navigation error are
 modelled. The recursive EKF shares both assumptions and adds its own: a fixed
 (white) process noise and a fixed bearing-noise variance, so its steady-state
 error is a statement about that ideal filter on that ideal trajectory, not
 about a real receiver.
* **Detection** is a fixed-threshold Neyman-Pearson energy detector over
 zero-mean Gaussian noise: no fluctuating target, no multipath fading, no
 signal-correlated noise, no non-stationary ambient levels. The reported
 `P_FA` and margin are therefore a *controlled but idealised* operating
 point, not a detection probability in a real noise field.
* **Beamforming** is conventional delay-and-sum on a single snapshot: no
 adaptive (MVDR/MUSIC) processing, no multipath, no coherent multi-snapshot
 averaging. The grid bearing is quantised to the scan step; the parabolic
 refinement is a local quadratic fit that *approaches* the Cramer-Rao bound
 but cannot reach the true CRB performance of an optimal estimator on finite
 data, and the two are reported separately for exactly that reason.
* **Hull analysis** treats an unstiffened long cylinder under uniform
 external pressure. Ring stiffening, end-cap effects, out-of-roundness and
 weld/fatigue defects — the things that actually govern a real submersible
 — are outside the model.
* **Capture** is a geometric-clearance and discrete-event feasibility check.
 Hydrodynamics, wake interaction, mooring loads and propeller cavitation
 spectra are not modelled.

Structural after-dive defect analysis remains a future extension.

### Related work

* **Neyman–Pearson detection** and the **Wilson–Hilferty** chi-square
 approximation are standard signal-detection results (Kay, *Fundamentals of
 Statistical Signal Processing: Detection Theory*).
* **Bearing-only target motion analysis** and the observer-maneuver
 observability requirement are established passive-sonar results (Nardone &
 Aidala, "Observability criteria for bearings-only target motion
 analysis").
* **Extended Kalman filtering** follows the canonical state-estimation
 treatment (Anderson & Moore, *Optimal Filtering*).
* **Underwater propagation and the passive sonar equation** follow Urick,
 *Principles of Underwater Sound* [@urick_principles_1983]; the absorption
 coefficient is Thorp's low-frequency expression [@thorp_1967] and the
 sound speed is Mackenzie's nine-term equation [@mackenzie_1981].
* **Array processing** — the ULA steering vector, the conventional
 delay-and-sum beamformer, and the Cramer-Rao bound on bearing — is Van
 Trees, *Optimum Array Processing* [@van_trees_2002].
* **Elastic buckling of a long cylinder under external pressure**, the
 expression that governs the collapse depth here, is Timoshenko & Gere,
 *Theory of Elastic Stability* [@timoshenko_gere_1961]; the thin-wall
 hoop-stress relation is standard [@young_roark_2011].
* **Discrete-event simulation** of the capture phase draws on standard
 queueing/event-sequence practice.
* **Requirement traceability** and Archimedean **buoyancy feasibility** are
 the chapter-and-verse of naval-architecture conversion analysis
 [@tupper_naval_2013].

The novelty here is not the individual algorithms but their assembly into a
deterministic, protocol-adapter mission package whose claims are all
code-generated.

## Sources — LIPARUS: bibliography

@kay_detection_1998; @nardone_aidala_1981; @anderson_moore_1979; @tupper_naval_2013; @urick_principles_1983; @thorp_1967; @mackenzie_1981; @van_trees_2002; @timoshenko_gere_1961; @young_roark_2011


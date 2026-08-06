# The Living Daylights (1987) — LIVING DAYLIGHTS

*film package · mission codename LIVING DAYLIGHTS*. Mission **SNIPER'S NEST**: sniper cover for a high-value defection (Bratislava); rules-of-engagement discipline (no shooting the innocent); cello-case concealment of a takedown sniper rifle; mountain/desert exfiltration with covered routes.

This chapter reproduces the package's complete manuscript verbatim:
the abstract and every authored section, token-hydrated from the
package's own manuscript variables, with the package's figures carried
in the combined PDF and its sources resolved against the unified
bibliography.

## Concepts

countersniper optics, defection

## Abstract

The Living Daylights: SNIPER'S NEST — Special-Agent Mission Software (mission codename **SNIPER'S NEST**) is deterministic special-agent mission software for *The Living Daylights* (1987). It models six operational concepts with real, reproducible computation across eight pure domain modules: * **Sniper ballistics** — a plug-and-play point-mass external-ballistics core that solves the rifle zero (fusing the trajectory to the sight line at 300 m), captures the near/far zero, and solves windage (a 5.0 m/s full-value crosswind imposes a 0.189 m drift requiring a -0.63 mrad hold), all embedded in a takedown rifle that conceals inside a cello case (true, 2 lanes, 0.241 packing efficiency, 72 s field assembly). * **Countersniper optics** — the 10x mil-dot riflescope ranges the 300 m target from a -2.68 mil holdover and dials the 27/-6 click solution; glint radiometry detects a hostile optic at 0.083 probability at 800 m. * **Countersniper detection** — a hostile sniper is ranged acoustically (687 m from the 2.0 s crack-bang delay at 20 °C) and localized by 2 crossed bearings to (50.0, 50.0) m. With two bearings the fit is exactly determined, so its residual is zero by construction and no accuracy is claimed from it. * **Defection-handling protocol** — a staged, risk-scored pipeline (5 stages) whose weighted hazard model renders the canonical KOSKOV scenario conditional with a verify gate stage and 0.670 backstop certainty (conditional). * **Mountain/desert terrain ops** — a seeded (7) terrain grid on which a cover-weighted least-cost Dijkstra planner routes 31.00 km over 62 steps. Measured against baselines, the exposure term raises route concealment by 0.014 over the same planner with the term off, but the resulting 0.484 still falls short of the grid's own 0.490 mean (signed gap -0.006): at this weighting concealment is a preference, not the objective, and the route is not a concealed one. * **Overwatch selection** — of 16 in-range candidate positions only 1 see the extraction site; the top-scored *visible* nest at (6, 0) commands it from 3000 m with 1451.7 m elevation advantage. The staged plan's verify gate and the backstop certainty agree on a conditional posture. They read no shared variable, but both scenarios are constant tables authored in one module to encode the same story beat, so the agreement is a design-consistency check between two scoring paths — not independent corroboration. The same caution applies to the terrain cover audit, which is a second implementation of one concealment definition. All results derive from a single deterministic mission solution ([`src/the_living_daylights/compute_mission.py`](../src/the_living_daylights/compute_mission.py)) so the manuscript, the mission report, and the figures can never drift apart. Keywords: sniper ballistics, rifle zero, windage, rules of engagement, riflescope optics, mil-dot ranging, countersniper detection, optic glint radiometry, acoustic crack-bang ranging, bearing triangulation, terrain visibility, viewshed, overwatch selection, defection protocol, evidence verification, risk scoring, terrain operations, cover planning, deterministic simulation.

## Introduction

*The Living Daylights* (1987) is the mission that frames SNIPER'S NEST: a
covering sniper must protect a high-value defection, carry a sniper rifle
concealed in a cello case, refuse a lethal shot at an innocent, find and range
the hostile shooter working the same corridor, and exfiltrate through mountain
and desert terrain. Each beat is a tractable, well-posed computation. This
package turns those beats into deterministic algorithms backed by real data and
reproducible figures.

### The domain core

The software is structured as a pure, infrastructure-free domain core
([`src/the_living_daylights/`](../src/the_living_daylights/)). Every module
below is stdlib + numpy only — no `bond_api`, no I/O, no wall-clock, no global
RNG:

* [**`ballistics.py`**](../src/the_living_daylights/ballistics.py) — a
 point-mass RK4 external-ballistics core: rifle zero, near/far-zero capture,
 crosswind drift and the wind hold, rules of engagement (the trigger-guard
 hold), and deterministic cello-case shelf packing with field assembly time.
* [**`optics.py`**](../src/the_living_daylights/optics.py) — the riflescope:
 MOA↔mrad turret arithmetic, whole-click solutions, mil-dot reticle ranging
 and its inverse, ballistic holdover in mils, first-order parallax, and true
 field of view.
* [**`countersniper.py`**](../src/the_living_daylights/countersniper.py) —
 finding the other shooter: optic-glint radiometry (geometry factor, sky
 contrast, angular fraction, detection probability), acoustic crack-bang
 ranging with a temperature-dependent sound speed, and least-squares bearing
 triangulation of crossed azimuths.
* [**`visibility.py`**](../src/the_living_daylights/visibility.py) — terrain
 line of sight over a Bresenham cell walk, viewsheds, and the ranked
 overwatch (sniper's nest) selection the title's image demands.
* [**`defection_protocol.py`**](../src/the_living_daylights/defection_protocol.py) —
 a staged, risk-scored defection-handling pipeline with monotonic approval and
 a plan gate, plus a separately parameterised backstop evidence-verification
 model that agrees with that gate — both are authored constant tables, so the
 agreement is a design check rather than independent corroboration.
* [**`terrain_ops.py`**](../src/the_living_daylights/terrain_ops.py) —
 a seeded mountain/desert grid (elevation, landcover, standing cover),
 cover-weighted Dijkstra route planning reported against measured baselines,
 and a separately implemented cover audit that grades any proposed path, not
 only the planner's own.
* [**`settings.py`**](../src/the_living_daylights/settings.py) — the single
 authoritative source of mission parameters, echoed for readers in
 [`manuscript/config.yaml`](config.yaml).
* [**`compute_mission.py`**](../src/the_living_daylights/compute_mission.py) —
 the one deterministic mission solution that composes all of the above.

### Protocol integration

The package integrates with the frozen BOND-API mission protocol:
[`mission.py`](../src/the_living_daylights/mission.py) implements the
`MissionProvider` lifecycle (brief, recon, plan, execute, debrief) against
`bond_api`'s frozen dataclasses and registers the film's field kit in a
module-level `GADGETS` registry. It is the only module in the package that
imports `bond_api`, and it carries no business logic of its own.

The mission adapter and the manuscript both read the single deterministic
[`compute_mission.mission_solution`](../src/the_living_daylights/compute_mission.py),
so prose metrics are never hand-authored: every number below arrives as a
brace-delimited token hydrated by
[`manuscript_variables.py`](../src/the_living_daylights/manuscript_variables.py),
and a test fails the build if any placeholder in these sections is not
generated.

### Reader's guide

The manuscript follows the mission procedure: methodology (section 2) derives
each algorithm module by module, results (section 3) reports the computed
mission solution with the four figures, the conclusion (section 4) states what
was shown, experimental setup (section 5) fixes the parameters, reproducibility
(section 6) ties results to the provenance hash and the live test gate, and
section 7 states the scope boundary and the related work.

## Methodology

Six concept modules define the algorithms, in mission order: sniper ballistics
(`ballistics.py`), riflescope optics (`optics.py`), countersniper detection and
localization (`countersniper.py`), terrain visibility and overwatch selection
(`visibility.py`), staged defection handling with backstop evidence
verification (`defection_protocol.py`), and terrain routing (`terrain_ops.py`).
`settings.py` fixes their parameters and `compute_mission.py` composes them into
one solution. All are deterministic and infrastructure-free: stdlib and numpy
only, no I/O, no wall-clock, and no randomness beyond the seeded terrain grid.

### Sniper ballistics (`ballistics.py`)

The round is modelled as a **point-mass projectile with quadratic air drag**
plus gravity, integrated with a fixed-step classical RK4
(`ballistics.trajectory`). The drag deceleration follows the standard law
`a_drag = (rho·A·C_d / 2m)·v²`; the ballistic coefficient
`BC = m / (A·C_d)` for the 7.8 mm service round is
984 kg/m² at a muzzle velocity of 790 m/s and bullet
mass 10.4 g.

**Rifle zero.** `ballistics.zero_scope` solves the muzzle elevation such that
the round lands at height zero at the zero range 300 m while the
sight line — starting `0.07` m above bore — passes through the
same point. Bisection on the simulated impact height yields an elevation of
2.68 mrad. `capture_zero` then returns the two ranges where
the trajectory crosses the sight line: near 25.9 m and far
300.3 m.

**Time of flight.** `ballistics.time_of_flight` is a *closed form*, not a
readout of the RK4 trajectory above. Flat-fire quadratic drag `dv/dt = −k·v²`
integrates to `x(t) = ln(1 + k·v₀·t)/k`, and inverting that gives
`t(x) = (exp(k·x) − 1)/(k·v₀)`, which is the expression the code evaluates.
Because `exp(z) − 1 ≥ z`, the result is always at or above the drag-free bound
`range/v₀` — a decelerating round cannot beat vacuum, and the test suite pins
that floor at five ranges. The form neglects the extra path length contributed
by the launch angle and gravity, so it is a strict lower bound on the
integrated flight time; at the 300 m target it returns
0.418 s against the RK4 trajectory's own time array, the two agreeing to
under a millisecond. That comparison is itself a test, not a claim.

**Windage.** Crosswind is treated as a drag-driven lateral relaxation toward
the wind speed. `ballistics.wind_drift` integrates the lateral offset; at the
300 m target a 5.0 m/s full-value wind produces a
0.189 m drift, i.e. a -0.63 mrad wind hold.
`wind_hold_mrad` returns `-drift / range · 1000`.

**Rules of engagement.** `ballistics.engagement_decision` encodes the film's
central morality: lethal fire only on a confirmed hostile target. A hostile
non-target whose weapon is present draws a **trigger-guard**
(`disable_weapon`) shot rather than a kill, so an innocent third party — the
cellist — is never engaged.

**The cello case.** `disassemble_takedown_rifle` returns the components of a
compact takedown rifle (barrel_receiver, stock, optic, suppressor); `pack_cello_case` runs
deterministic bottom-left shelf packing to decide whether the
4 components fit a 1.30 x 0.45 x
0.24 m case interior. Parts are laid along the case's long axis
and processed width-descending, opening a new lane across the case's width when
the current lane runs out of length; each part must also clear the interior
cross-section on its own. The rig packs into 2 lanes with a
longest-lane fill of 1.10 m and an areal packing efficiency
of 0.241 (the parts' summed footprint over the case floor), and
`assembly_time` gives a 72 s field assembly time. Because the
packer reorders parts internally, each placement carries the part it belongs
to, so a reported slot is always the slot of the part it names.

### Countersniper optics (`optics.py`)

The riflescope is a fixed-parameter `ScopeSpec` (10x,
50 mm objective, 0.10 mrad clicks). Two
conversion families matter operationally:

* **Turret clicks** — `clicks_for_angle` converts an angular correction
 (milliradians) into whole clicks of the turret's click unit, and
 `zero_click_schedule` turns the ballistic solution into the scope's
 elevation/wind click counts (27 elevation /
 -6 wind for the zeroed mission).
* **Mil-dot ranging** — the milliradian relation `range = size·1000/mils`
 (`mil_dot_range`) fixes an 1.80 m standing silhouette
 spanning 6.0 mils on the reticle at 300 m,
 and `mils_for_size` inverts it. `holdover_mils` converts the ballistic drop
 into a -2.68 mil reticle holdover, and `parallax_shift_m`
 models the first-order sight shift when the target range differs from the
 150 m parallax-focus range (10.0 mm at
 the 300 m target). `field_of_view_m` divides the eyepiece's
 apparent field by the magnification and returns the chord at range. Ranging
 follows the standard mil-dot doctrine [@fm2310sniper].

### Countersniper detection (`countersniper.py`)

A hostile sniper is found three ways, all deterministic:

* **Optic glint** — the lens reflects sunlight. `glint_geometry_factor`
 multiplies a `sin(sun elevation)` illumination term (a higher sun puts more
 direct irradiance on the lens; 35° here) by a Gaussian
 specular falloff `exp(-(Δaz/half-width)²)` with a
 3.0° half-width, giving 0.368 at the
 mission's 2.0° sun–observer offset. `glint_contrast`
 spreads the collected power `I·A·ρ·g` (reflectivity ρ =
 0.35) over the specular cone's solid angle and divides by
 sky radiance; range cancels, which is why glints stay visible far out (the
 solar reference follows [@astmg173]). `glint_angular_fraction` then supplies
 the range dependence — the lens's solid angle `A/R²` over one
 1.0 mrad resolution cell, capped at 1 — so `glint_snr`
 falls as 1/range² once the lens no longer fills a cell.
 `glint_detection_probability` is the signal-detection CDF of SNR against a
 threshold ([@vantrees1968]). At 800 m the hostile optic
 yields SNR 5.8 and P(det) = 0.083.
* **Acoustic crack-bang** — the flash-to-bang delay scaled by the speed of
 sound `c(T) = 331.3 + 0.606·T` ([@kinsler2000]) places the shot
 687 m away from the 2.0 s delay; the
 mission's 343.4 m/s at 20 °C.
* **Bearing triangulation** — `triangulate_position` minimizes the summed
 squared perpendicular distance from a point to each observer's bearing line,
 solving the resulting 2x2 normal equations in closed form and rejecting a
 singular (parallel or collinear) system rather than returning a fictitious
 fix. From 2 observers the crossed bearings place the
 hostile at (50.0, 50.0) m (acoustic shooter localization
 per [@duckworth1996counter], [@ledeczi2005countersniper]). **The reported
 residual is not a measurement.** With 2 bearings the
 normal equations are two equations in two unknowns, so the fit passes exactly
 through the intersection and the residual is identically zero for any
 non-parallel pair; the 0.00 m printed in the results is
 floating-point rounding, not accuracy. The residual only carries information
 when the system is over-determined and inconsistent, which requires at least
 three bearings and a noise model this package does not have. A three-bearing
 positive control in `tests/test_countersniper.py` pins a hand-derived
 20.4124 m residual, so the code path is exercised where it can actually be
 wrong.

### Terrain visibility (`visibility.py`)

`line_of_sight` walks a deterministic integer Bresenham cell line
[@bresenham1965] between observer and target and blocks when an intermediate
cell's terrain-plus-cover top rises above the linearly interpolated sight ray
minus a clearance (0.30 m here); the ray runs from
`elevation + eye height` (1.70 m) at each end. `viewshed`
collects every cell visible from an observer in a deterministic row-major scan
and reports the visible count and fraction; viewshed methodology follows the
terrain-visibility literature [@fisher1996viewshed].

`rank_overwatch_positions` scores each candidate nest as
`w_vis·visible + w_dist·(1 − d/d_max) + w_cover·cover + w_elev·gain/gain_max`
with weights (0.40, 0.25, 0.20, 0.15) that are validated to sum to 1;
candidates beyond 12 cells are dropped as out of practical
engagement range, and distance and elevation gain are normalized over the
surviving set. Positions that cannot see the target keep their other terms but
score zero for visibility, so the ranking stays total and deterministic (ties
break on cell order). `best_overwatch` returns the top-ranked *visible*
candidate, or `None` when nothing sees the site. Because a blind candidate
keeps its proximity, cover, and elevation terms (up to 0.60 of the score), it
can out-rank a visible one that scores only the 0.40 visibility weight;
`rank_overwatch_positions[0]` therefore carries no visibility guarantee, and
`compute_mission` selects the reported nest through `best_overwatch` rather
than off the top of the ranking. `tests/test_visibility.py` builds the case
where the two disagree, so the filter is exercised rather than assumed. On the
mission's own seed the two happen to coincide at every candidate step tested
(1–8): the 0.40 visibility weight dominates this terrain, so no reported number
changes. The selection is stated here because it is the correct policy and
because an earlier version took `ranked[0]`, which carried no such guarantee —
not because it moved a result.

### Defection-handling protocol (`defection_protocol.py`)

`assess_defection` evaluates an ordered, fixed sequence of
5 stages (contact, snatch, verify, exfiltrate, relocate). Each stage carries weighted
`RiskFactor`s; the stage hazard is the exposure-weighted mean
`sum(w_i·s_i)/sum(w_i)` clamped to [0, 1], so a dominant high-score factor
cannot be averaged away by benign ones. A stage is `go` at or below the
0.40 threshold, `conditional` at or below
0.70, and `no-go` above it; the plan score is the
conservative maximum across stages.

Approval is **monotonic**: the assessment walks the stages in order, marking
each `approved` while every predecessor is `go`. The first stage whose verdict
is not `go` becomes the **plan gate**, and a `no-go` at any stage blocks every
stage after it. The protocol validates membership of the canonical stage set
rather than position, so a caller may supply the stages in its own order. The
canonical KOSKOV scenario (`koskov_scenario`) fixes the factor weights and
scores, so the mission's report is reproducible.

### Evidence verification (`defection_protocol.py`)

The verify stage's backstop model (`EvidenceCheck`, `verification_certainty`,
`backstop_verdict`) accumulates 4 weighted checks
(identity_documents, debrief_consistency, backstop_telegraphy, cover_story_plausibility) into a certainty score under the same exposure-weighting
scheme as `stage_score`, then maps that certainty onto a
cleared/conditional/rejected verdict — the operational analogue of sequential
verification against documentary and telegraphic backstops.

**This is not independent corroboration, and earlier drafts of this section
wrongly said it was.** `koskov_scenario` and `koskov_verification` are two
hardcoded constant tables in the same module, written by the same author to
encode the same story beat — the film's verification doubt. They read no shared
variable, but that is a weaker fact than it sounds: the numbers in both tables
were chosen so that the verify stage gates and the backstop lands
`conditional`, and `koskov_verification`'s own docstring says so. Their
agreement demonstrates that two scoring functions applied to two consistent
authored inputs return consistent verdicts. It is a design-consistency check
between the staged and backstop paths, and it is evidence about neither
General Koskov nor the world.

### Terrain ops (`terrain_ops.py`)

`generate_terrain` builds a seeded elevation + landcover + standing-cover grid:
elevation is a wrap-padded 3x3-blurred Gaussian field renormalized to the
requested relief, landcover is a seeded categorical draw over the table
(`landcover_name` indexes it), and cover height is the landcover's base cover
plus seeded jitter. Effective concealment is the cover height normalized to the
500 m cell's cover threshold and clipped to [0, 1] — a pure function
of the cover-height field, so an edited field is honoured verbatim downstream.

`step_cost` blends the per-metre landcover cost, an ascent penalty proportional
to the climb per cell, and an exposure penalty `cover_weight·(1 − cover)`, then
scales by the cell size. `plan_route` runs Dijkstra's algorithm
[@dijkstra1959] over 4-adjacent moves with strict `(cost, row, col)`
tie-breaking, which is what makes the route byte-reproducible. `assess_cover`
grades any proposed path — not only Dijkstra's — reporting mean and minimum
concealment, the least-covered step, the high-concealment waypoints, and
per-waypoint cover.

**What the audit's agreement with the planner establishes.** `assess_cover` is
a vectorised numpy implementation and `plan_route`'s summary is a scalar Python
loop; the two deliberately share no helper. Agreement between them therefore
rules out implementation drift between what the planner reports about its own
route and what an audit of the same waypoints computes. It does **not**
corroborate the concealment model: both encode one definition
(`clip(cover_height / COVER_THRESHOLD_M, 0, 1)`) written by one author, so a
wrong definition would be reproduced identically by both. The test suite
therefore checks each against a third calculation performed in the test itself,
rather than checking them against each other.

### Composition (`compute_mission.py`)

`mission_solution` is the single entry point that runs every module above
against `settings.py` and returns one nested mapping: ballistics, rules of
engagement, optics, countersniper, cello case, defection, verification,
terrain, and overwatch. The extraction site is defined non-arbitrarily as the
grid's global elevation minimum ((0, 0)) — a wadi-like low point,
the hardest kind of site to overwatch — and candidate nests are sampled every
3 cells in each axis.

`input_hash` fingerprints that mapping as canonical compact JSON with sorted
keys under SHA-256. The mission adapter, the manuscript token map, and the
figures all read the same call, so no consumer can report a number the others
did not compute.


### Input-contract hardening

The pure core fails loud on numerically invalid inputs rather than propagating
garbage. Four guards are bound by regression tests that would fail on the code
that preceded them:

* `ballistics.wind_drift` and `ballistics.wind_hold_mrad` reject a non-positive
 range. The hold computes `-drift / range · 1000`, so a zero range previously
 slipped through to an opaque `ZeroDivisionError`; both now raise a
 `ValueError`, matching `time_of_flight` and `drop_at_range`.
* `optics.mil_dot_range` and `optics.mils_for_size` reject a non-positive target
 size. The mil-dot relation `range = size · 1000 / mils` is linear in the
 silhouette, so a zero or negative `target_size_m` silently produced a zero or
 negative (nonsense) range; both now raise.
* `countersniper.triangulate_position` rejects any non-finite observer
 coordinate or bearing. A NaN bearing previously flowed through the
 closed-form normal equations and returned a NaN "fix" with no error — a
 fail-open on a detection/localization path. The single finite-input guard
 roots this out, since a finite determinant follows from finite inputs.
* `terrain_ops.assess_cover` reports `waypoint_cover` as one `(cell, cover)`
 pair per waypoint, in path order, so a path that revisits a cell keeps a
 reading for every visit. An earlier dict keyed on `"r,c"` silently dropped
 the duplicate reading. The aggregate `mean_cover` / `min_cover` /
 `cover_points` were always computed over the full sequence; only the map was
 lossy.

Each guard carries a matching positive assertion that the healthy path is
unchanged, so these are checks of a real contract, not new ways to fail.

## Results

The deterministic mission solution ([`compute_mission.mission_solution`](../src/the_living_daylights/compute_mission.py))
reports every number below; the manuscript never hand-authors a metric.

### Sniper ballistics

The 300 m zero requires an elevation of 2.68
mrad for the 7.8 mm round (BC 984 kg/m²,
790 m/s, 10.4 g). The sight line and the
trajectory cross at the near zero 25.9 m and the primary far zero
300.3 m; at the 300 m target the round rides
-0.804 m below the line of departure with a 0.418 s time of flight.
A full-value 5.0 m/s crosswind deflects the round
0.189 m, calling for a -0.63 mrad wind hold.
Figure shows the zeroed trajectory against the sight line
and the drift curve.

![Zeroed ballistic trajectory and crosswind drift](output/figures/the_living_daylights_ballistics_trajectory.png)

### Rules of engagement

The covering sniper's decision engine resolves the film's moral hinge
deterministically. The cellist — observed "cellist", non-hostile — resolves to
**hold_fire** (non-hostile 'cellist' — innocent, hold fire): Bond refuses the lethal
shot. A hostile sentinel with a weapon present, but *not* the authorized asset,
resolves to **disable_weapon** (hostile non-target 'sentinel' — trigger-guard shot to disable weapon): the
trigger-guard shot disables the threat without an unlawful kill (see
[`ballistics.engagement_decision`](../src/the_living_daylights/ballistics.py)).

### The cello case

The 4-part takedown rifle (barrel_receiver, stock, optic, suppressor) conceals in
the 1.30 x 0.45 x 0.24 m case interior:
packing returns `true` using 2 lanes, a longest-lane fill
of 1.10 m, and an areal efficiency of
0.241, with a 72 s field assembly time (see
[`ballistics.pack_cello_case`](../src/the_living_daylights/ballistics.py)).

### Defection-handling protocol

The KOSKOV scenario runs through 5 stages
(contact, snatch, verify, exfiltrate, relocate) with a plan score of 0.605 and an overall
verdict of **conditional** against the
0.40/0.70 thresholds, gated at the
**verify** stage — the point where identity doubt and backstop
inconsistency surface. Earlier stages approve; later ones carry the plan only
under conditions.

### Mountain/desert terrain ops

On the seeded (7) terrain grid, the planner routes
31.00 km (62 steps) from the entry cell to the exfil goal
at a blended cost of 92550.4, with a mean route concealment of
0.484 and a worst-case (least-covered) segment of 0.071
at step 43; 19 high-cover waypoints are
identified.

**Measured against baselines, the cover term is real but weak, and the route is
not a concealed one.** The same planner with the exposure term switched off
(`cover_weight = 0`) returns a route of 0.470 mean
concealment, so the term buys 0.014 of concealment — a real,
non-zero effect on a different path. But the grid's own mean concealment is
0.490, and the shipped route's signed gap against it is
-0.006 — the route is *less* concealed than an average cell.
At the mission's weighting the
blended cost is dominated by landcover traversal cost and climb, and
concealment is a mild preference rather than the objective. Calling this a
"covered exfil route" would overstate it. Raising `cover_weight` does clear the
field average, so the shortfall is a weighting choice and not a ceiling; both
relations are pinned in `tests/test_compute_mission.py`, so this paragraph
cannot drift from the numbers.

Run against the same waypoints, the `assess_cover` audit returns
0.484. That agreement is a cross-implementation check —
vectorised numpy against the planner's scalar loop, sharing no helper — and it
detects implementation drift only; both encode the same concealment definition,
so it is not independent corroboration of the model. Figure
 maps the route and its cover points on the concealment field.

![Planned exfil route on the concealment map](output/figures/the_living_daylights_terrain_exfil_route.png)

### Countersniper optics

The 10x mil-dot riflescope (50 mm
objective, 0.10 mrad clicks) ranges the standing target at
300 m from the 6.0-mil reticle span and holds
-2.68 mils against the 300 m drop. The zero
dials onto the turret as 27 elevation clicks and
-6 wind clicks; at the target range the first-order parallax
shift is 10.0 mm.

### Countersniper detection and localization

The hostile optic glints with a geometric brightness of 0.368
at the 2.0° sun–observer offset; the radiometric model
yields SNR 5.8 at 800 m and a detection
probability of 0.083 (Figure ). Acoustically, the
2.0 s crack-bang delay at 20 °C places the shot
687 m away (sound speed 343.4 m/s); crossed
bearings localize the hostile to (50.0, 50.0) m. The fit
also prints a 0.00 m residual, and that number is reported
here only to be discounted: with 2 bearings the least-squares
system is exactly determined, so the residual is identically zero by
construction for any non-parallel pair and the printed value is floating-point
rounding. It is not a measure of localization accuracy, and no accuracy claim
rests on it.

![Countersniper optic-glint detection probability vs range](output/figures/the_living_daylights_glint_detection.png)

### Overwatch selection

The extraction site sits at (0, 0) — the terrain's global
elevation minimum, and therefore in a near-total blind spot. Sampling every
3 cells and keeping only positions within
12 cells leaves 16 in-range candidates,
of which only 1 (0.062 fraction) can
actually see the site over the intervening terrain and cover. Selection runs
through `best_overwatch`, which takes the top-scored candidate *that can see
the site*, not the top-scored candidate outright — a blind position keeps up to
0.60 of the score from proximity, cover, and elevation, so the two need not
coincide. The selected nest at (6, 0) commands the site from
3000 m with 1451.7 m of elevation advantage
and 0.50 concealment, scoring 0.714 (Figure
).

![Ranked overwatch nests for the extraction site](output/figures/the_living_daylights_overwatch_nests.png)

### Evidence verification

The verify stage's backstop model accumulates 4 weighted
checks (identity_documents, debrief_consistency, backstop_telegraphy, cover_story_plausibility) into a certainty of 0.670, rendering
the verdict **conditional**, which matches the staged assessment's
verify gate. The two read no shared variable, but they are not
independent evidence: both `koskov_scenario` and `koskov_verification` are
hardcoded constant tables in one module, authored together to encode the film's
verification doubt. The match shows the staged and backstop scoring paths are
mutually consistent given consistent authored inputs — a design check, not a
corroborated finding.

## Conclusion

SNIPER'S NEST demonstrates that a special-agent mission's operational concepts
can be turned into real, deterministic, testable algorithms. The package:

* solves the **sniper ballistics** problem — zero, windage, rules-of-engagement,
 and cello-case concealment — with a physically grounded point-mass integrator;
* runs a **staged, risk-scored defection protocol** whose hazard model renders
 the canonical scenario conditional at the verify gate, alongside an
 **evidence-verification** model whose weighted backstop checks land on the
 same verdict from a separately authored table;
* plans **mountain/desert routes with a measured cover term** on a seeded,
 reproducible terrain grid, and selects the **overwatch nest** — the
 top-scored position that actually sees the extraction site, with concealment
 and elevation advantage;
* fights the **countersniper duel** — mil-dot ranging and click solutions on
 the riflescope, radiometric optic-glint detection, acoustic crack-bang
 ranging, and least-squares bearing triangulation of a hostile position;
* binds all of it to the frozen BOND-API `MissionProvider` protocol so the
 orchestrator can drive the film generically, with full deterministic
 provenance on every outcome.

The architecture keeps a pure, infrastructure-free domain core beneath a thin
mission adapter, and forces every reported metric through a single
deterministic solution — so the manuscript, the mission report, and the figures
cannot drift. That claim is enforced, not asserted: the token cross-reference
test fails on any placeholder the code does not generate, the hydration gate is
tested against a solution with each required section removed in turn, and the
reader-facing parameter echo in `config.yaml` is pinned key-for-key to
`settings.py`. Test count and achieved coverage live in
[`docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md) rather than in this
prose, so no stated figure can outlive the run that produced it.

Two pairs of models cross-check each other, and it is worth being exact about
how much that is worth. The staged defection assessment and the backstop
evidence check read no shared variable, yet both are constant tables authored
in one module to encode one story beat, so their agreement is a
design-consistency check and not independent corroboration. The planner's route
summary and the cover audit are genuinely different code paths — a scalar loop
and a vectorised numpy pass, sharing no helper — so their agreement rules out
implementation drift, but both encode a single concealment definition and
neither can catch that definition being wrong. Each is therefore checked in the
suite against a third calculation performed in the test itself, and the earlier
claim that these pairings made the numbers "confirmed rather than
self-reported" was too strong.

Two further limitations belong in the summary rather than in a footnote. The
bearing-triangulation residual is identically zero for the mission's two
observers — the system is exactly determined, so that number measures nothing
and no localization accuracy follows from it. And the exfil route is *not* a
concealed route: the cover term has a real, measured effect against the same
planner with the term disabled, but the resulting path still sits below the
terrain's own mean concealment at the shipped weighting.

The triggering image of the title, the *trigger-guard* hold, is
not an arbitrary flourish: it falls out of the rules-of-engagement model as the
correct action when an innocent is not a target and a hostile's weapon is.

## Experimental setup

### Mission parameters

All parameters are fixed in the single source of truth
([`src/the_living_daylights/settings.py`](../src/the_living_daylights/settings.py))
and echoed for readers in [`manuscript/config.yaml`](config.yaml); a test pins
the echo to `settings.py` key for key, so the two cannot drift apart. Every
value below is read back out of the live mission solution as a token rather
than transcribed by hand.

#### Ballistics

| Parameter | Value |
|---|---|
| Film / mission codename | the_living_daylights / SNIPER'S NEST |
| Muzzle velocity | 790 m/s |
| Bullet mass | 10.4 g |
| Caliber | 7.8 mm |
| Ballistic coefficient | 984 kg/m² |
| Zero range | 300 m |
| Sight height over bore | 0.07 m |
| Target range / wind | 300 m / 5.0 m/s |

#### Riflescope optics

| Parameter | Value |
|---|---|
| Magnification / objective | 10x / 50 mm |
| Click value | 0.10 mrad |
| Ranging silhouette / reticle span | 1.80 m / 6.0 mils |
| Parallax focus range | 150 m |

#### Countersniper detection

| Parameter | Value |
|---|---|
| Sun elevation / specular half-width | 35° / 3.0° |
| Sun–observer azimuth offset | 2.0° |
| Lens reflectivity / resolution cell | 0.35 / 1.0 mrad |
| Glint evaluation range | 800 m |
| Air temperature / crack-bang delay | 20 °C / 2.0 s |
| Triangulation observers | 2 |

#### Concealment rig

| Parameter | Value |
|---|---|
| Cello-case interior (L × W × D) | 1.30 × 0.45 × 0.24 m |
| Takedown components | 4 (barrel_receiver, stock, optic, suppressor) |

#### Defection handling and terrain

| Parameter | Value |
|---|---|
| Defection stages | 5 (contact, snatch, verify, exfiltrate, relocate) |
| Defection thresholds (go / conditional) | 0.40 / 0.70 |
| Backstop checks | 4 (identity_documents, debrief_consistency, backstop_telegraphy, cover_story_plausibility) |
| Terrain seed / size / cell | seed 7 · 32×32 · 500 m |
| Route start → goal | (0, 0) → (31, 31) |
| Overwatch eye height / clearance | 1.70 m / 0.30 m |
| Overwatch candidate step / max range | every 3 cells / 12 cells |

### Software environment

Built and verified under Python 3.14.6. Deterministic by
construction: the mission solution uses a fixed seed (7) and no
randomness beyond the seeded terrain, and every reported metric is recomputed
from typed, documented pure functions. Scripts are thin orchestrators;
business logic lives in `src/`.

The test count and achieved coverage are not quoted here — they are recorded
live in [`docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md), and the
gate itself (`--cov-fail-under=90` on `src/`, line *and* branch) is what this
manuscript claims.

Manuscript dated 2026-08-04 — the committed date from
`manuscript/config.yaml`, not a hydration timestamp, so re-running the
generator changes no byte of this page.

## Reproducibility

### Determinism

Every number in this manuscript is a pure function of fixed, documented inputs
([`src/the_living_daylights/settings.py`](../src/the_living_daylights/settings.py)).
The mission solution uses a fixed seed (7); the only randomness in
the whole stack is the seeded terrain generator in
[`terrain_ops.generate_terrain`](../src/the_living_daylights/terrain_ops.py),
which is itself deterministic for a fixed seed. No wall-clock value enters any
persisted artifact — there is no exception. The manuscript carries a date
(2026-08-04), but it is the committed `paper.date` from
[`manuscript/config.yaml`](config.yaml), read like any other parameter, not the
moment of hydration. An earlier version of this package stamped
`datetime.now` into this page and into
`output/data/manuscript_variables.json`, which made the byte-identical claim
below false on every rerun; the clock has been removed rather than the claim
weakened.

The BOND-API `MissionOutcome` carries a Provenance record with a stable
`input_hash` (a sha256 of the canonical mission solution), so any report can be
audited against the code without re-running the film's I/O.

### Artifacts and regeneration

| Artifact | Producer | Location |
|---|---|---|
| Mission report / figures | [`scripts/execute.py`](../scripts/execute.py), [`scripts/z_generate_manuscript_variables.py`](../scripts/z_generate_manuscript_variables.py) | `output/` (regenerable, git-ignored) |
| Resolved manuscript sections | `z_generate_manuscript_variables.py` | `output/manuscript/` |
| Ballistics + terrain figures | [`src/the_living_daylights/figures/plots.py`](../src/the_living_daylights/figures/plots.py) | `output/figures/ballistics_trajectory.png`, `output/figures/terrain_exfil_route.png` |
| Countersniper + overwatch figures | [`src/the_living_daylights/figures/plots.py`](../src/the_living_daylights/figures/plots.py) | `output/figures/glint_detection.png`, `output/figures/overwatch_nests.png` |
| Hydrated token map | `z_generate_manuscript_variables.py` | `output/data/manuscript_variables.json` |

### Verification gate

The package is verified with three separate commands, and it is worth stating
precisely what each one does and does not enforce:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90 # tests + coverage + no-mock scan
uv run ruff check src/ scripts/ tests/ && uv run ruff format --check src/ scripts/ tests/
uv run mypy src/ scripts/
```

The pytest command enforces two things: ≥90% line+**branch** coverage of `src/`
measured over real computation, and — since
[`tests/test_no_mock_frameworks.py`](../tests/test_no_mock_frameworks.py) — the
absence of any mocking framework, parsed from the AST of every `.py` file under
`src/`, `tests/`, and `scripts/`. That second gate carries its own positive
control: a planted `MagicMock`, aliased import, and `mocker` fixture must all
be reported, so the scan cannot pass by being blind. An earlier version of this
section claimed the single pytest command also enforced lint and type
cleanliness. It does not; `ruff` and `mypy` are the second and third commands
above and nothing in `tests/` invokes them.

The achieved figures are recorded in
[`docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md) rather than quoted
here, so no prose number can go stale against the gate.

Three tests carry the anti-drift load specifically:

* [`test_all_manuscript_tokens_are_generated`](../tests/test_manuscript_variables.py)
 cross-references every brace-delimited placeholder in these sections against
 the live token map, so none can survive un-generated.
* `test_require_outputs_rejects_an_incomplete_solution` gutted-section by
 gutted-section proves the hydration gate actually fires — it is checked
 against a solution missing each required section in turn, not merely against
 the healthy one.
* `test_config_mission_block_mirrors_settings` pins the reader-facing
 `mission:` echo in `config.yaml` to `settings.py`, key for key.

Re-running `z_generate_manuscript_variables.py` on one interpreter regenerates
a byte-identical `output/` tree — every resolved manuscript section, the token
JSON, and all four figure PNGs. The interpreter is the stated scope because
`PYTHON_VERSION` is itself a token; nothing else in the tree varies between
runs.

That is a claim, so it is bound by a test rather than by assertion.
[`test_regeneration_determinism.py`](../tests/test_regeneration_determinism.py)
runs the generator twice as a real subprocess, deliberately straddling a
wall-clock second boundary, and compares a SHA-256 of every produced file. A
second test in that file AST-scans `src/` for any clock call
(`datetime.now`/`utcnow`, `date.today`, `time.time`, `time.time_ns`,
`time.monotonic`) reachable from the persisted-artifact path, and carries a
positive control: a planted clock call in a temporary module must be reported,
so the scan cannot pass by being blind. Note what the older
`git status --short` check does *not* prove — `output/` is git-ignored, so that
tree stays clean whatever the bytes say.

## Scope and related work

### Scope boundary

SNIPER'S NEST models the deterministic core of a special-agent mission only.
Stated as explicit non-claims:

* **Aerodynamics** stop at the point-mass quadratic-drag law with a constant
 drag coefficient. There is no spin drift, no Magnus effect, no Coriolis term,
 no transonic drag rise, and no atmospheric layering; the barometric density
 helper is a single exponential scale height, not a standard-atmosphere table.
* **Radiometry** is a first-order energy budget. Sky radiance is a fixed
 daylight constant, the lens is a single specular reflector with one
 reflectivity, and there is no spectral, polarization, or
 atmospheric-extinction treatment. The detection curve is a normal CDF over
 SNR, not a measured ROC.
* **Acoustics** use only the flash-to-bang delay against a linear
 temperature-dependent sound speed. There is no ballistic shockwave (Mach
 cone) geometry, no multipath or reverberation, and no wind-borne refraction.
* **Localization** is a noiseless least-squares bearing intersection. Bearings
 carry no uncertainty model, so the reported residual measures geometric
 consistency of the observations, not positional accuracy. At the mission's
 two observers it does not even measure that: two non-parallel bearings give
 an exactly determined system whose residual is identically zero, so the value
 printed in the results is rounding noise and carries no information at all.
 A residual becomes informative only with three or more inconsistent bearings.
* **Terrain** is a seeded grid of elevation, landcover, and standing cover.
 Routing is 4-adjacent Dijkstra on a blended cost; visibility is a single-ray
 Bresenham walk with a fixed clearance and no earth curvature, refraction, or
 sub-cell relief. The planner optimizes that blended cost, not a full
 line-of-sight ballistic occlusion query.
* **Adversaries and humans** are not modelled at all: no stochastic opponent,
 no reaction times, no human factors, no communications network.

These simplifications are deliberate. They are what keep every result
deterministic, fast, and auditable, and they are why the package can assert
byte-identical reruns rather than statistical agreement.

### Relation to the broader simulation canon

* **External ballistics** — the point-mass drag model with a ballistic
 coefficient is the standard small-arms treatment [@mccoy1999]; the zeroing
 and windage geometry mirrors conventional rifle-zero practice, with near/far
 zero capture. Mil-dot ranging follows established sniper doctrine
 [@fm2310sniper].
* **Countersniper detection** — acoustic shooter localization from crossed
 bearings is the operating principle of fielded countersniper systems
 [@duckworth1996counter; @ledeczi2005countersniper]; the glint model is an
 energy-budget reduction of optical retro-reflection detection, and the
 detection probability is the classical signal-detection formulation
 [@vantrees1968] against a reference solar irradiance [@astmg173]. The
 temperature-dependent sound speed is the standard linear approximation
 [@kinsler2000].
* **Terrain visibility** — line of sight over a rasterized cell walk
 [@bresenham1965] and the accumulation of visible cells into a viewshed are
 the canonical GIS treatment [@fisher1996viewshed]. The contribution here is
 not the viewshed itself but the *ranking*: turning visibility into an
 overwatch-selection objective alongside proximity, concealment, and elevation
 advantage.
* **Risk-gated decision procedures** — the discrete, thresholded approval path
 of `defection_protocol.py` is a classic monotone decision chain; its weighted
 hazard scoring follows a transparent exposure-weighting scheme. The
 contribution is pairing a staged plan gate with a separately parameterised
 evidence-verification model. Both scenarios are authored constant tables, so
 the pairing is a structural one; agreement between them is not independent
 evidence and is not offered as such.
* **Terrain routing** — Dijkstra's algorithm over a cost grid [@dijkstra1959]
 is the canonical least-cost routing method; the contribution here is the
 *cover* term that folds concealment into route cost — reported against two
 measured baselines (the same planner with the term off, and the grid's own
 mean concealment) rather than asserted — plus a cover audit that can grade
 any proposed path, not only the planner's own.

### Intended use

The package is one film in the PROJECT BOND suite. Its role is to implement the
frozen BOND-API `MissionProvider` contract with a real, deterministic,
well-tested domain core, and to serve as a canonical example of converting a
template scaffold into a standalone mission package. It is local-only and is
discovered by the suite orchestrator via `bond_api`.

## Sources

@friedman2026sniper; @bondapi2026; @fm2310sniper; @duckworth1996counter; @astmg173; @vantrees1968; @fisher1996viewshed; @kinsler2000; @ledeczi2005countersniper; @mccoy1999; @dijkstra1959; @bresenham1965


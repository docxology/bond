# Thunderball (1965) — THUNDERBALL

*film package · package codename THUNDERBALL*. Mission **DISCO VOLANTE**: plan the underwater recovery dive; verify the NATO escort screen holds; confirm submersible range to reach the recovery site; confirm passive-sonar detection of the recovery site; steer the return leg against the prevailing current; interdict closing threat tracks before they reach the screen.

## Concepts — THUNDERBALL: domain and operational focus

underwater ops, nuclear convoy integrity

## Abstract — THUNDERBALL: mission summary

**Thunderball: DISCO VOLANTE — Special-Agent Mission Software** (mission codename **DISCO VOLANTE**) is a deterministic special-agent mission-software package covering six underwater-recovery capabilities: scuba dive planning with a Bühlmann ZH-L16A decompression model, NATO-style nuclear-convoy integrity analysis, submersible range/endurance logistics, passive-sonar detection, set-and-drift underwater navigation, and dynamic convoy interdiction. For the flagship recovery profile the model computes a no-decompression limit of 9.17 minutes at the working depth against an air-supply limit of 24.78 minutes, so decompression rather than gas volume is the binding constraint (**deco**) and the planned bottom time is 9.17 minutes. It further reports an intact escort screen rated ok, a passive-sonar detection range of 21.78 nautical miles, a return-leg drift of 0.122 nautical miles (yes within the recovery radius), and a closing threat held at 3.344 nautical miles (status **held**). Every value is derived from deterministic math over explicit parameters (dive planning, Bühlmann ZH-L16A decompression, no-decompression limit, air consumption, convoy integrity, escort coverage, submersible logistics, range and endurance, passive sonar, Thorp absorption, set-and-drift navigation, closest point of approach, convoy interdiction, deterministic mission software) — no random draws, no wall-clock dependence, and a fully provenanced result.

## Introduction — THUNDERBALL: mission framing, the operational problem, and how to read this chapter

*Thunderball* (1965), adapted from Fleming's 1961 novel [@fleming1961], is the
film in which SPECTRE hijacks two NATO nuclear bombs and the operation reaches
its climax in an underwater battle around the legendary submersible yacht,
*Disco Volante*. The **DISCO VOLANTE** mission
software package implements the quantitative planning problems that underwrite
such a recovery: how deep and how long a diver can work, whether the escort
screen protecting the high-value asset holds, how far the submersible
powerplant can carry an assault team, whether passive sonar can localise the
recovery site, how the prevailing current displaces the dive team, and whether
closing threat tracks can be interdicted before they reach the screen.

Six pure domain modules provide these capabilities:

* `src/thunderball/dive_planner.py` — air-budget and Bühlmann ZH-L16A
 decompression planning.
* `src/thunderball/convoy_integrity.py` — convoy-screen gap detection, escort
 coverage, and an integrity score.
* `src/thunderball/submersible_logistics.py` — power, endurance, range, and
 optimal-cruise analysis.
* `src/thunderball/sonar_detection.py` — Thorp absorption, transmission loss,
 signal excess, and detection range.
* `src/thunderball/current_navigation.py` — set-and-drift dead reckoning,
 course-to-steer, and cross-track error.
* `src/thunderball/interdiction_analysis.py` — closest-point-of-approach
 geometry and screen-penetration verdicts.

The package is a BOND-suite film: a thin `src/thunderball/mission.py` adapter
exposes these capabilities through the frozen `bond_api` `MissionProvider`
protocol, so the *orchestrator* can discover and drive the mission
deterministically. The domain modules themselves are standalone and never
import infrastructure.

Two further modules support the manuscript itself rather than the mission:
`src/thunderball/manuscript_variables.py` computes every substituted token in
this document from `docs/manuscript/config.yaml` plus the same domain calls the
mission makes, and `src/thunderball/figures.py` renders the five concept
figures. No numeric result in this prose is hand-authored.

This manuscript documents the mathematical models (the methodology section), the
computed results (the results section), the experimental parameters (the setup section), the
reproducibility guarantees (the reproducibility section), and the scope boundary
(the scope section), and an honest statement of each model's uncertainty
and where it would break (the discussion section).

## Methodology — THUNDERBALL: the analytical models and algorithms that drive the mission

### Dive planning

Dive planning in `src/thunderball/dive_planner.py` rests on two pieces of
physics. First, absolute ambient pressure rises by one bar every ten metres:
`P(d) = P_surf + d/10`. Breathing demand at depth scales with this pressure,
so a diver with a surface air consumption (SAC) rate of
20.0 L/min uses `SAC * P(d)` litres per minute at depth. A
cylinder of 12 L filled to
207 bar therefore holds
`12 * 207` litres of
free gas, and the bottom time follows by dividing usable volume by the
at-depth demand.

Second, inert-gas loading is modelled with the **Bühlmann ZH-L16A** tissue
model: sixteen compartments, each with a nitrogen half-time and a pair of
coefficients `(a, b)`. Bühlmann states the constraint as a tolerated *ambient*
pressure, `P_amb_tol = (P_tissue - a) * b`; inverted for the tolerated tissue
tension at a given ambient pressure this is the M-value line

```
M(P) = P / b + a
```

which puts the fastest compartment's surfacing ceiling at 3.27 bar and the
slowest at 1.28 bar. A compartment's inert-gas pressure approaches the
alveolar pressure `P_alv = f_N2 (P - pH2O)` exponentially on its half-time.

The **no-decompression limit** is the largest bottom time after which a
*direct ascent to the surface* remains legal, so every compartment is tested
against its M-value at **surface** ambient pressure — the ceiling the diver
must clear on the way up — and not against the inflated M-value at working
depth (the ndl figure). The distinction is not cosmetic: at
40 m the ambient pressure is roughly five times the
surface value, so evaluating the ceiling at depth admits almost any bottom
time and overstates the limit by more than an order of magnitude. The limit is
located by bisection on bottom minutes; when a dive exceeds it,
`plan_decompression` emits ascending stop holds that discharge the controlling
tissue.

`plan_dive` is the single entry point that combines the two: it takes the
cylinder, SAC rate, and depth, flies `min(air_limit, NDL)` unless an explicit
bottom time is requested, plans the decompression schedule for the profile
actually flown, and reports which limit bound. Gas for each decompression stop
is charged at that stop's own ambient pressure — a 6 m hold costs about 1.6x
the surface SAC volume — so the reported gas requirement is a real budget
rather than a surface-rate approximation. Both the mission adapter and this
manuscript's token generator call `plan_dive`, so the two cannot disagree.

### Convoy integrity

Convoy analysis in `src/thunderball/convoy_integrity.py` treats the escort
screen as a set of bearing angles around the protected formation. Two angular
quantities are reported and they are not the same thing. The **angular gap**
is the *spacing* between consecutive escort bearings; the largest gap measures
how thinly the screen is spread and is computed from bearings alone, with no
knowledge of any detection half-angle. The **largest uncovered sector** is the
widest arc no escort watches, which does read the half-angle: each escort
defends an arc of `2 * half_angle` around its bearing, and a screen whose arcs
overlap has a positive largest spacing and a zero uncovered sector. Reporting
the spacing as though it were an unwatched arc would overstate the screen's
exposure, so the two are computed and reported separately
(`largest_gap` and `largest_uncovered_sector`). **Coverage fraction** is the
unioned defended arc divided by 360°. Its pointwise companion
`is_bearing_covered` answers whether one specific bearing falls inside any
escort's arc, measuring separation on the circle so the 0/360° seam needs no
special case; sweeping it around the compass draws the screen's actual
coverage rosette (the convoy figure).

The **integrity score** combines a sigmoid gap penalty with coverage:

```
score = 1 / (1 + exp((gap - 60) / 12)) * (0.5 + 0.5 * coverage)
```

Scores above 0.7 are rated `ok`, between 0.4 and 0.7 `marginal`, and below
0.4 `breached`. Layered over the continuous score is a hard **sector ceiling**
(`marginal_under_deg`): a screen whose largest gap reaches it is downgraded
from `ok` to `marginal` even when the score would have passed it, which lets a
mission impose a sector width narrower than the score's nominal 60° knee
without retuning the score. The ceiling can only downgrade, never upgrade.
`min_escorts_for_coverage` returns the smallest uniform screen that reaches a
coverage target.

### Submersible logistics

Submersible logistics in `src/thunderball/submersible_logistics.py` models
underwater propulsion with a cubic speed-power law plus a constant hotel
load: `P(v) = k v^3 + H`. Endurance is `E / P(v)`, and range is
`v * E / P(v)` (the range figure). The speed that maximises range balances the
cubic drag term against the hotel load; because `R(v)` rises then falls, the
optimum is found from the derivative vanishing at `k v^3 = H/2`. The inverse
problem — energy required to transit a given range — inverts the cubic via a
bounded root-find on the imbalance `f(v) = R k v^3 - E v + R H`.

### Passive sonar detection

Detection modelling in `src/thunderball/sonar_detection.py` uses the passive
sonar equation. **Thorp absorption** gives the frequency-dependent seawater
attenuation (`alpha(f) = 0.11 f²/(1+f²) + 44 f²/(4100+f²) + 2.75e-4 f² + 0.003`
dB/km), and **transmission loss** combines spherical spreading with
absorption: `TL(r) = 20 log10(r) + alpha(f) r` (the sonar figure). The **signal
excess** `SE = SL - TL - (NL - DI) - DT` is the detection margin; the
**detection range** is where `SE` crosses zero, located by bounded bisection.

### Set-and-drift navigation

Navigation in `src/thunderball/current_navigation.py` works in the
east/north plane with the current expressed as a set/drift vector. Own
velocity and current are vector-added to give ground velocity, and dead
reckoning integrates it over time. **Course to steer** solves the classic
vector triangle: the current's component perpendicular to the desired track
is cancelled by a component of own velocity, `theta = asin(-c_perp / v)`,
giving the heading that makes good the track. **Cross-track error** is the
signed perpendicular distance off the track line, and the drift distance over
the dive's *planned* bottom time — `min(air limit, NDL)` as reported by
`plan_dive`, which is the time the team is in the water, not the longer air
budget it never flies — is checked against the recovery radius (the drift figure).

### Convoy interdiction

Interdiction in `src/thunderball/interdiction_analysis.py` layers relative
motion over the static screen. The **closest point of approach** between a
threat track and the convoy follows from relative position and velocity:
`t_cpa = max(0, -dot(rel_pos, rel_vel) / |rel_vel|²)` and
`d_cpa = |rel_pos + rel_vel t_cpa|`, with closing speed derived from the same
dot product. The **screen penetration time** is the chord across the largest
inter-escort spacing (`2 r sin(gap/2)`) divided by the interceptor's speed.

**Time to minimum separation** comes from the constant-velocity range profile
`range(t)² = d_cpa² + |rel_vel|² (t - t_cpa)²`, so the range first falls to a
limit `R` at `t = t_cpa - sqrt(R² - d_cpa²) / |rel_vel|`. When `d_cpa >= R`
that root does not exist and the time is infinite: the CPA is by definition
the smallest range the threat ever achieves, so a CPA outside the limit means
the limit is never reached at all. The **interdiction status** is then a race
between three times: `breached` when the threat reaches minimum separation
before the escorts' reaction time, `penetrated` when the gap chord is crossed
before it, and `held` otherwise — including a diverging threat.

## Results — THUNDERBALL: measured outcomes, headline numbers, and what they establish

### Flagship verdict summary

For the flagship recovery profile the six capabilities report the following
deterministic verdicts; each row is a live token from the engine, not a
hand-copied constant.

| Capability | Verdict |
|---|---|
| Dive — no-decompression limit | 9.17 min |
| Dive — air-supply limit | 24.78 min |
| Dive — binding constraint | deco |
| Dive — decompression stops | 0 |
| Convoy — integrity status | ok (score 0.7773) |
| Convoy — uncovered sector | 0.00° |
| Submersible — optimal range | 407.61 nm |
| Sonar — detection range | 21.78 nm |
| Navigation — drift | 0.122 nm (within recovery: yes) |
| Interdiction — status | held |


### Dive planning results

For the flagship recovery profile (working depth 40 m),
the Bühlmann ZH-L16A model reports a no-decompression limit of
**9.17 minutes**. The configured cylinder
(12 L at 207 bar) and SAC
rate (20.0 L/min) yield an air-duration limit of
**24.78 minutes**. Decompression therefore binds first:
`plan_dive` reports a binding constraint of
**deco** and a planned bottom time of
**9.17 minutes**, with
0 decompression stops — flying exactly the
no-decompression limit is by definition a no-stop dive. The dive consumes
**919.5 L** of the cylinder's free gas, leaving a
margin of **1564.5 L**: the recovery team surfaces on its
decompression obligation with gas to spare, which is the correct way round for
a working dive at this depth.

![Bühlmann ZH-L16A no-decompression limit versus depth, evaluated against the surface ascent ceiling.](output/figures/thunderball_ndl_curve.png)

### Convoy integrity results

The escort screen is placed at bearings 0, 45, 90, 135, 180, 225, 270, 315 degrees
with a detection half-angle of 30 degrees. The widest
*spacing* between adjacent escorts is **45.00 degrees**,
but spacing is not exposure: each escort watches 30
degrees either side of its bearing, so the arcs overlap and the largest
genuinely *uncovered* sector is **0.00 degrees**,
with total escort coverage **1.0000**. Nothing around this screen
is unwatched. The integrity score is **0.7773**, rated
**ok**; the score is driven by the spacing rather than by
the uncovered sector, which is what keeps it sensitive to a screen thinning out
before any hole actually opens. To reach the
0.90 coverage target a uniform screen needs at least
**6 escorts**.

![Polar coverage rosette for the configured screen: each of 360 sample bearings tested against the actual escort set, with the escorts marked on the rim.](output/figures/thunderball_convoy_screen.png)

### Submersible logistics results

The submersible powerplant (400 kWh, drag coefficient
0.035, hotel load 2.0 kW) achieves its optimal
range at **3.057 knots**, giving an
**407.61 nautical-mile** best range (the range figure).

![Submersible range versus speed, with the optimal-range marker.](output/figures/thunderball_submersible_range.png)

### Passive sonar results

At 10.0 kHz (source level 150 dB,
ambient noise 75 dB, directivity index
15 dB) the passive-sonar range equation gives a detection
range of **21.78 nautical miles** — the range at which the
signal excess crosses zero (the sonar figure).

![Passive-sonar transmission loss versus range, with the detection budget.](output/figures/thunderball_transmission_loss.png)

### Navigation results

The return leg makes good a track of 315 degrees at
4.0 knots against a current setting
90 degrees at 0.80 knots.
Course-to-steer corrects the heading to **306.87 degrees**
with a ground speed of **3.394 knots**. Over the
planned bottom time of 9.17 minutes — the time the team
is actually in the water, which is the decompression limit here and not the
longer 24.78-minute air budget — the current sweeps the
team **0.122 nautical miles**. Inside the
1.0-nautical-mile recovery radius:
**yes** (the drift figure).

![Set-and-drift geometry over the planned bottom time, computed from the dive parameters rather than pinned to a literal.](output/figures/thunderball_drift_geometry.png)

### Interdiction results

The threat track (course 270 degrees at
20.0 knots, closing at
**23.30 knots**) has its closest point of approach at
**3.344 nautical miles** after **0.1420
hours**. That CPA is outside the
1.0-nautical-mile minimum separation, and the CPA is
by construction the smallest range the threat ever reaches, so minimum
separation is never breached and the verdict turns on the gap crossing alone.
Crossing the 45.00-degree inter-escort sector at
2.0 nautical miles takes **0.0765
hours**, against an escort reaction time of 0.05
hours; the screen is rated **held**.

## Conclusion — THUNDERBALL: findings, verdict, and what the mission establishes

The **DISCO VOLANTE** mission software turns the planning questions of an
underwater nuclear-recovery operation into deterministic, reproducible
computations. Dive planning resolves the tension between air budget and
decompression obligation; convoy integrity quantifies the escort screen;
submersible logistics reports the powerplant's reach; passive sonar fixes the
detection envelope; set-and-drift navigation corrects the return leg; and
interdiction analysis verifies the screen can respond to a closing threat.

The flagship profile closes green: the screen is rated **ok**
with a largest escort spacing of 45.00 degrees and no
uncovered sector at all (0.00 degrees), the dive is
bound by
**deco** — the no-decompression limit of
9.17 minutes runs out well before the
24.78-minute air supply, leaving
1564.5 L of gas in hand — sonar acquires the site at
21.78 nautical miles, the drift of
0.122 nautical miles stays within the recovery radius, and
the closing threat is **held** at
3.344 nautical miles. Because every result derives from
deterministic math carrying a provenance hash, the mission can be re-executed
and audited exactly.

That the dive is decompression-bound rather than gas-bound is the single most
consequential number in the package, and it is the one an implementation error
is most likely to invert. A transposed M-value line, or a no-decompression
limit evaluated at working depth instead of at the surface ascent ceiling,
inflates the limit at 40 m by more than an order of
magnitude and silently flips the planner's advice from "surface on your
obligation" to "surface on your gas". The suite pins the limit against the
*U.S. Navy Diving Manual*'s published air no-decompression limits
[@usnavydiving2016] rather than against its own arithmetic, so the inversion
cannot recur unnoticed. Those limits come from the Navy's own EL/VVAL-18
lineage, not from ZH-L16A: the test asserts that this package's ZH-L16A limits
land inside bands bracketing them, which is an agreement check between two
independent models, not a table lookup.

## Experimental Setup — THUNDERBALL: canonical scenarios, parameters, and configuration

All parameters are declared in `docs/manuscript/config.yaml` and loaded by
`src/thunderball/manuscript_variables.py`; no numeric result is hand-authored
in prose.

### Dive parameters

| Parameter | Value |
|---|---|
| Working depth | 40 m |
| Cylinder capacity | 12 L |
| Fill pressure | 207 bar |
| SAC rate | 20.0 L/min |

### Convoy parameters

| Parameter | Value |
|---|---|
| Escort bearings (deg) | 0, 45, 90, 135, 180, 225, 270, 315 |
| Detection half-angle | 30° |
| Coverage target | 0.90 |

### Submersible parameters

| Parameter | Value |
|---|---|
| Battery energy | 400 kWh |
| Drag coefficient | 0.035 |
| Hotel load | 2.0 kW |

### Sonar parameters

| Parameter | Value |
|---|---|
| Frequency | 10.0 kHz |
| Source level | 150 dB |
| Ambient noise | 75 dB |
| Directivity index | 15 dB |

### Navigation parameters

| Parameter | Value |
|---|---|
| Return-leg track | 315° |
| Own speed | 4.0 kn |
| Current set | 90° |
| Current drift | 0.80 kn |
| Recovery radius | 1.0 nm |

### Interdiction parameters

| Parameter | Value |
|---|---|
| Threat course | 270° |
| Threat speed | 20.0 kn |
| Screen radius | 2.0 nm |
| Escort reaction time | 0.05 h |

### Environment

- Package version: 0.1.0
- Python: 3.14.6
- Manuscript date (from `config.yaml`, not the clock): 2026-08-04T00:00:00+00:00

The mission runs under a fixed seed (dive planning, Bühlmann ZH-L16A decompression, no-decompression limit, air consumption, convoy integrity, escort coverage, submersible logistics, range and endurance, passive sonar, Thorp absorption, set-and-drift navigation, closest point of approach, convoy interdiction, deterministic mission software include deterministic
mission software); the six domain modules are pure functions of these
parameters.

## Reproducibility — THUNDERBALL: verification gates, deterministic regeneration, and artifacts

DISCO VOLANTE is deterministic by construction:

* **Fixed seed** — no random draws anywhere; results are pure functions of the
 config parameters.
* **No wall-clock dependence** — `GENERATION_TIMESTAMP` is the only timestamp,
 and it is read from the committed `paper.date` in `docs/manuscript/config.yaml`,
 never from the clock. Regenerating the artifacts on any later day rewrites
 the same bytes with no flag; `--now` exists only to pin a different value
 deliberately. The one environment-derived token is `PYTHON_VERSION`, so the
 byte-identical claim holds for a fixed interpreter.
* **Computed tokens** — every `{RESULT_*}` value in this manuscript is
 recomputed from `src/` domain math, never hand-authored.
* **Provenance** — every `MissionOutcome` carries a fixed input hash and seed,
 so an outcome can be audited without re-running the film.

The concept figures (`output/figures/ndl_curve.png`, `convoy_screen.png`,
`submersible_range.png`, `transmission_loss.png`, `drift_geometry.png`) are
regenerated deterministically. The claim is bound, not asserted:
`tests/test_regeneration_determinism.py` runs the hydration CLI twice, more
than a clock tick apart, and compares every written byte of the token JSON and
all five PNGs.

### Test suite

The package gates on line+branch coverage of `src/` at or above 90%. The
suite covers the dive planner, convoy integrity, submersible logistics,
passive sonar, current navigation, convoy interdiction, the mission protocol
adapter, manuscript-token hydration, figure generation, and subprocess smoke
tests of the mission CLIs. All tests use real computation and real protocol
types — there are no mocks. Live counts are regenerated into
`docs/_generated/COUNTS.md`; this manuscript quotes the gate, not a figure
that would go stale.

### External anchors

Reproducing a number is not the same as it being right, so the constants that
carry a physical claim are pinned against published values rather than against
the implementation's own arithmetic:

* Bühlmann surfacing ceilings — 3.27 bar for the fastest compartment, 1.28 bar
 for the slowest [@buehlmann1984].
* No-decompression limits at 18, 30, 40 and 60 m, asserted to fall inside
 bands bracketing the *U.S. Navy Diving Manual*'s published air
 no-decompression limits of 60, 20, 10 and 5 minutes at those depths
 [@usnavydiving2016]. The Navy manual publishes limits from its own
 EL/VVAL-18 model lineage, not Bühlmann tables, so this anchor is a
 cross-model agreement check — a ZH-L16A implementation landing inside a band
 around an independently derived operational limit — and not a comparison of
 ZH-L16A against itself.
* The analytic optimal-range speed, cross-checked against a dense numerical
 sweep of the range curve.
* The pointwise coverage predicate, cross-checked against the aggregate
 coverage fraction over a 3600-sample sweep of the compass.

A test that only restates the formula under test cannot catch a transposed
formula. These anchors can.

## Scope and Related Work — THUNDERBALL: boundaries, positioning, and relationship to the literature

### Scope

DISCO VOLANTE covers six planning problems drawn from *Thunderball* (1965):
dive planning under a Bühlmann ZH-L16A decompression model, convoy-screen
integrity, submersible range and endurance, passive-sonar detection,
set-and-drift navigation, and dynamic convoy interdiction. Each is a
deliberately small, fully-tested, deterministic core, sized to demonstrate the
BOND mission protocol rather than to plan a real operation.

The package makes no claim to full naval mission planning. In particular it
omits:

* **Mixed gas.** The decompression model is air-only: no trimix or nitrox
 compartment sets, no gradient factors, no repetitive-dive residual nitrogen,
 and no ascent-rate violation penalties. It is representative, not a certified
 dive computer, and nothing here should be used to plan a real dive.
* **Ocean physics.** The sonar model is a single-path range equation over
 spherical spreading and Thorp absorption: no sound-speed profile, no
 multipath or convergence-zone structure, no bottom or surface scattering, and
 no probabilistic fluctuation term — so it yields a range, not a probability
 of detection. The current field is a single uniform set-and-drift vector,
 with no tidal variation, depth shear, or weather.
* **Multi-target tactics.** Convoy metrics are angular (gaps, coverage,
 integrity score) plus a single CPA-tracked threat. There is no sensor fusion,
 no multi-track association, no weapon-target assignment, and no wargaming of
 escort manoeuvre.
* **Teams.** One diver, one submersible, one threat track — no buddy pairs, no
 team gas-sharing, no formation logistics.

### Related work

* **Decompression modelling** — Bühlmann's ZH-L16 family is the classical
 dissolved-gas framework and the direct source of the coefficient tables and
 the tolerated-ambient-pressure formulation used here [@buehlmann1984]. The
 *US Navy Diving Manual* is the standard operational reference against which
 no-stop limits are conventionally sanity-checked [@usnavydiving2016]; the
 test suite pins this package's limits inside bands around those published
 air limits rather than against its own arithmetic. The manual's limits come
 from the Navy's own EL/VVAL-18 model lineage, not from ZH-L16A, so the check
 is a cross-model agreement test and not a lookup of the model under test. Modern dive computers add gradient factors
 and bubble-model variants that this package intentionally omits.
* **Underwater acoustics** — Urick is the standard treatment of the sonar
 equation, transmission loss, and detection threshold [@urick1983]; the
 frequency-dependent absorption coefficient is Thorp's [@thorp1967].
* **Marine hydrodynamics** — the cubic speed–power drag law is the standard
 first-order model for submerged resistance and propulsive power
 [@newman1977]; the constant hotel-load term is the minimal extension needed
 for an interior range optimum to exist at all.
* **Navigation and collision geometry** — set-and-drift, the current vector
 triangle, and course-to-steer follow Bowditch [@bowditch2002]. Relative-motion
 CPA/TCPA geometry is the basis of collision-avoidance practice, for which
 Cockcroft and Lameijer is the standard practitioner treatment
 [@cockcroft2011].
* **Perimeter screening** — coverage and gap analysis of a defended perimeter
 is standard in convoy-defence and sensor-placement studies; the angular
 metric here is a reduced, deterministic form of it.

As a BOND suite film, this package's primary relation is to the frozen
`bond_api` protocol [@bondapi2026], shared across the film packages, and to
the suite _orchestrator_, which drives any `MissionProvider` through the
five-stage lifecycle.

## Discussion and Uncertainty — THUNDERBALL: interpretation, caveats, and what the numbers do not claim

Every number in the results section is the deterministic output of a closed-form or
bounded-iteration model over explicit parameters in `docs/manuscript/config.yaml`.
That determinism gives the package its reproducibility, but it also means the
precision of a token — two or three decimal places — is **not** accuracy. Each
of the six models rests on idealising assumptions, and where those assumptions
break is where the uncertainty actually lives. This section states that
honestly for each capability.

### The central finding is robust, not borderline

The headline result — that **decompression, not gas, binds the flagship dive**
— is the single most consequential number in the package, and it is also the
most robust one. The no-decompression limit of 9.17 minutes
and the air-supply limit of 24.78 minutes are not close:
the air budget outlasts the no-stop obligation by more than a factor of two at
the working depth of 40 m, so the conclusion that the
team surfaces on its decompression obligation survives a wide swath of
parameter error and is not a borderline tie. The suite deliberately pins the
limit against an independent published band [@usnavydiving2016] precisely
because a transposed M-value or a depth-evaluated ceiling could silently
invert this call (see the results section).

### Dive planning uncertainty

The ZH-L16A model is air-only and single-dive, and it treats every diver
identically: it takes one 20.0 L/min SAC rate, no gradient
factors, no repetitive-dive residual nitrogen, and no human physiological
variation. Real no-stop limits vary substantially across divers, workloads,
thermal stress, and ascent profiles; a representative model cannot claim
those. An operational planner would add conservatism (safety/gradient factors)
well beyond what a bare M-value line provides.

### Convoy-screen uncertainty

The screen model is angular and static: escorts sit at fixed bearings, each
watching an idealised circular arc of the configured half-angle; the flagship
screen reports 0.00 degrees of genuinely unwatched
perimeter. A real escort's detection is probabilistic, range-limited, and
environment-dependent, so a computed zero-degree uncovered sector is a
statement about the *model geometry*, not about the physical certainty that no
threat slips through. The integrity score's sigmoid knee at a nominal 60° and
the configurable hard sector ceiling are design choices, not physical
constants.

### Submersible-logistics uncertainty

The cubic speed-power drag law plus a constant hotel load is a first-order
propulsion idealisation. The analytic optimal speed
(3.057 knots, from the methodology section) is a true
extremum of that idealised curve but inherits the uncertainty of the drag
coefficient and hotel load, which in reality vary with loading, fouling,
temperature, and depth. Battery energy likewise derates with age and cold that
the constant 400 kWh figure does not capture.

### Passive-sonar uncertainty

The sonar model is a single-path, spherical-spreading-plus-absorption range
equation. It yields a *range* (21.78 nm), not a
probability of detection: there is no multipath, convergence-zone, bottom or
surface interaction, and no fluctuation term. Real detection is inherently
probabilistic, and its strongest driver — ambient noise
(75 dB) — is among the most variable inputs in the
scenario, so the computed range should be read as a representative figure
under the stated quieting, not a guaranteed acquisition distance.

### Navigation uncertainty

Set-and-drift is modelled as a single uniform current vector. Real currents
shear with depth, vary over time, and interact with weather; the course to
steer and the drift figure (0.122 nm, from the results section)
hold exactly under the assumed constant current and degrade continuously as
that assumption is violated. Any error between the assumed and actual
set/drift translates directly into cross-track error on the return leg.

### Interdiction uncertainty

The interdiction verdict tracks a single threat under constant velocity.
held is a race against a nominal escort reaction
time (0.05 h); reaction time is operationally the most
uncertain quantity in the chain, so the categorical verdict should be read as
a sensitivity to that one number rather than a fixed outcome. The infinite
time-to-minimum-separation of a threat whose CPA lies outside the limit is a
"never under constant velocity", not an absolute guarantee.

### What would reduce these uncertainties

Each open item in the package backlog (`TODO.md`, *Extension*) is exactly the
modelling refinement that would shrink the corresponding uncertainty here:
gradient factors and mixed gas for the dive model, a probabilistic (Marcum)
detection layer for sonar, a depth-sheared or time-varying current for
navigation, and multi-track association for interdiction. They are out of
scope for this deterministic, six-capability mission package, which is sized to
demonstrate the BOND mission protocol rather than to plan a live operation.

## Sources — THUNDERBALL: bibliography

@buehlmann1984; @urick1983; @thorp1967; @bowditch2002; @newman1977; @cockcroft2011; @usnavydiving2016; @fleming1961; @bondapi2026


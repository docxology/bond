# On Her Majesty's Secret Service (1969) — BEDLAM

*film package · package codename BEDLAM*. Mission **PIZ GLORIA**: model aerosol bioweapon dispersion in the valley; resolve the plume's time-dependent puff footprint; plan a safe alpine exfiltration route; simulate the bobsleigh descent and banked-curve clearance; score the Bray cover identity; verify the Bray timeline against observed sightings.

## Concepts — BEDLAM: domain and operational focus

bioweapon dispersion, alpine ops, cover identity

## Abstract — BEDLAM: mission summary

On Her Majesty's Secret Service: PIZ GLORIA — Special-Agent Mission Software. This report documents the deterministic mission software built for mission codename **PIZ GLORIA**, drawn from the film *On Her Majesty's Secret Service* (1969). The package delivers six quantitative analysis capabilities grouped under three operational pillars: **Aerosol dispersion.** The steady-state Gaussian plume fixes the average threat: a hazardous airborne-allergen isopleth reaching **10210.16 m** down-valley, with a peak ground-level concentration of **3.492e-06 kg m$^{-3}$** at **703.49 m**. A Lagrangian Gaussian puff train adds the *time* dimension, showing the release first arrives at the downstream receptor after **740 s** with a transient peak of **1.370e-06 kg m$^{-3}$** — an early-warning lead the steady plume cannot express. **Alpine operations.** A slope-safety-gated planner returns a **safe** exfiltration line of **5478.808 m** at a mean grade of **15.24 deg**. Point-mass bobsleigh dynamics then integrate the descent: **37.5 s** to **45.8 m/s**, while a banked-curve analysis shows the unbanked canonical hairpin pulls **7.56 g** (over-limit) and a 55-degree bank raises safe cornering to **47.1 m/s**. **Cover identity.** The weighted *Bray* persona scores **0.177** (**low** risk). Timeline verification against four observed sightings gives a **medium** verdict at **77.8%** coverage with **1** contradiction(s) — one London sighting that unseats the claim. Every number above flows through the manuscript-variable pipeline from the executed mission results; none is hand-authored. The implementation is deterministic, mock-free, and covered well above the 90% branch-coverage gate on ``src/``.

## Introduction — BEDLAM: mission framing, the operational problem, and how to read this chapter

*On Her Majesty's Secret Service* (1969) is the one 007 film in which Bond's mission is
personal: tracking Ernst Stavro Blofeld to the Piz Gloria research station in
the Swiss Alps. Under the cover of Sir Hilary Bray — a genealogist of the
College of Arms — Bond infiltrates the summit and, when the cover is blown,
escapes by bobsleigh down the mountain. The PIZ GLORIA mission software models
the operational mathematics behind that operation: the threat of an aerosolized
allergen bioweapon on a mountaintop, the geometry of an alpine descent line,
and the fragility of a fabricated identity.

This package therefore implements six real, deterministic scientific models
as its pure domain core, grouped under the three operational pillars the film
suggests:

* `dispersion_model.py` — the classical Gaussian plume solution for a
 continuous elevated point source, with Pasquill-Gifford stability-dependent
 dispersion and a valley-channeling correction to the transport wind.
* `puff_dispersion.py` — a Lagrangian Gaussian puff train that adds the time
 dimension to the same release: an early-warning arrival time and transient
 peak concentration the steady plume cannot express.
* `alpine_routes.py` — track-geometry primitives (grade, chord length, Menger
 curvature) and a slope-safety-gated Dijkstra planner for an extrapolated
 safe descent.
* `descent_dynamics.py` — point-mass bobsleigh kinematics down that route,
 paired with banked-curve physics (lateral g-load, safe cornering speed) so
 the exfiltration line is audited for both slope and turn safety.
* `cover_identity.py` — a weighted additive risk model that scores how "held"
 an alias like the Bray persona is under scrutiny.
* `identity_timeline.py` — interval-arithmetic verification of that persona's
 claimed alibi against independently observed sightings, so a single
 contradicting observation can unseat an otherwise-covered cover.

The film's software also implements the frozen `bond_api` mission protocol,
exposing a deterministic `MissionProvider` that a coordinator can discover and
drive through the standard `brief -> recon -> plan -> execute -> debrief`
cycle.

### Reader's guide

* The methodology section derives all six models: dispersion, puff, route,
 descent, cover, and timeline.
* The results section presents the executed mission metrics and figures.
* The experimental setup section lists the fixed scenario parameters.
* The reproducibility section records provenance, hashing, and test coverage.
* The scope section states the models' limits and cites the related work.

## Methodology — BEDLAM: the analytical models and algorithms that drive the mission

### Aerosol bioweapon dispersion

The dispersion core models a continuous, elevated release of an aerosolized
allergen bioweapon transported downwind by the mean wind. We use the
steady-state Gaussian plume solution for a point source with ground reflection:

$$C(x,y,z) = \frac{Q}{2\pi u\,\sigma_y\,\sigma_z}
 \exp\!\left(-\frac{y^2}{2\sigma_y^2}\right)
 \left[\exp\!\left(-\frac{(z-H)^2}{2\sigma_z^2}\right)
 +\exp\!\left(-\frac{(z+H)^2}{2\sigma_z^2}\right)\right]$$

where $Q$ is the release rate [kg/s], $u$ the effective transport wind [m/s],
$H$ the effective release height [m], and $\sigma_y,\sigma_z$ the horizontal and
vertical dispersion coefficients. The coefficients follow the open-country
Pasquill-Gifford power laws $\sigma_y = a x^b$ and $\sigma_z = c x^d$, with the
standard per-stability-class coefficient set (classes A–F, unstable to
stable) [@arya1999dispersion; @turner1970workbook].

Because the release sits in a valley, the transport wind is corrected by a
channeling factor

$$f(e) = 1 - (1 - f_0)\,\exp(-e / d_v),$$

which slows the plume most at the valley floor ($f_0$ is the floor wind ratio)
and returns toward free-stream flow with increasing receptor elevation $e$
relative to the valley depth $d_v$. The far edge of the ground-level isopleth
at a fixed concentration threshold is computed by a coarse scan plus
bisection refinement, giving the mission's reach metric.

### Alpine route planning

A planned track is a polyline of waypoints in projected coordinates
(easting, northing, elevation). Three geometry quantities govern a
bobsleigh-grade line:

* chord slope: $\theta = \arctan(|\Delta z| / \sqrt{\Delta e^2 + \Delta n^2})$,
* 3-D chord length for cumulative distance,
* discrete Menger curvature $k = 4A / (|ab|\,|bc|\,|ca|)$ for turn sharpness.

A segment is classified *safe*, *marginal*, or *unsafe* by grade and rejected
when it also violates a curvature cap; the planner runs Dijkstra [@cormen2009algorithms] on an
8-connected grid, discarding any step whose chord grade exceeds the maximum
safe slope, and costs the remainder by distance plus a grade penalty, in the
spirit of alpine slope/avalanche danger rating [@mcclung2006avalanche].

### Cover-identity risk scoring

Each identity attribute $a$ carries a weight $w_a$ and a risk $r_a\in[0,1]$.
The aggregate cover risk is the weighted mean $\sum w_a r_a / \sum w_a$, and an
attribute risk is a linear function $r_a = \beta_a + m_a\,c_a$ of normalized
incriminating evidence $c_a$. A breach scenario raises one or more attributes'
evidence and recomputes the aggregate and its discrete verdict.

### Time-dependent puff dispersion

To capture *when* a threat arrives, the continuous release is discretized into
a deterministic train of Gaussian puffs, the Lagrangian puff-train approach
used by operational puff models [@zannetti1990air; @sykes1998scipuff]. Puff
$i$, emitted at $t_i$ with mass $Q\,\Delta t$, advects downwind at the
effective wind and spreads as it travels. Superimposing every emitted puff at a receptor gives a concentration
time series, whose early crossing of a detection threshold is the **arrival
time** — the operational early-warning metric. For a steady release the puff
superposition converges to the plume solution far downwind, a cross-check the
tests assert directly.

### Bobsleigh descent dynamics

A point-mass slides under gravity down a track profile resisted by kinetic
friction and aerodynamic drag:

$$a(v) = g\sin\theta - \mu g\cos\theta - k v^2, \qquad k = \tfrac{1}{2}\rho C_d A / m,$$

integrated with a fixed time step along the polyline. Because a bobsleigh line
is defined by its turns, the module pairs the speed profile with curve physics:
lateral g-load $v^2/(gR)$ and the banked-curve speed limit
$v_{\max} = \sqrt{gR\,(\tan\beta + \mu_L)/(1 - \mu_L \tan\beta)}$.

### Cover-timeline verification

A cover is as strong as its timeline. Claimed events and observed sightings
are intervals $[s, e)$ over mission minutes; an observation is *matched* when an
overlapping claim agrees on location and *conflicts* when an overlapping claim
names a different location. The coverage fraction (matched observed minutes
over total observed minutes) yields a discrete verdict, and a single
contradicting sighting can unseat an otherwise-covered story.

## Results — BEDLAM: measured outcomes, headline numbers, and what they establish

The executed PIZ GLORIA mission produces six deterministic result groups.
Every value below is generated by the live engine through the manuscript
variable pipeline.

| Metric | Engine output |
| --- | --- |
| Peak ground-level centreline concentration | 3.492e-06 kg m$^{-3}$ |
| Peak downwind distance | 703.49 m |
| High-hazard isopleth reach | 10210.16 m |
| Puff arrival at downstream receptor | 740 s |
| Puff transient peak concentration | 1.370e-06 kg m$^{-3}$ |
| Planned route distance | 5478.808 m |
| Route mean grade | 15.24 deg |
| Route slope-safety verdict | safe |
| Descent time | 37.5 s |
| Descent maximum speed | 45.8 m/s |
| Track peak lateral load | 7.56 g |
| Track 4-g ceiling verdict | over-limit |
| Banked (55°) cornering max speed | 47.1 m/s |
| Bray cover score | 0.177 |
| Bray cover verdict | low |
| Timeline coverage | 77.8% |
| Timeline contradictions | 1 |
| Timeline verdict | medium |

### Dispersion footprint

At the configured release (see the experimental setup section) the model locates a
peak ground-level centreline concentration of **3.492e-06 kg m$^{-3}$** at
**703.49 m** downwind. The high-hazard isopleth (ground-level
concentration at or above the configured threshold) reaches
**10210.16 m** down-valley — the far edge of the exposure band,
driven by the elevated release and valley-channeled transport.

![Ground-level centreline aerosol concentration along the plume axis.](output/figures/on_her_majestys_secret_service_aerosol_plume.png)

### Puff arrival and early warning

At the downstream receptor the Lagrangian puff train shows the allergen first
crosses the detection threshold after **740 s**, with a
transient peak of **1.370e-06 kg m$^{-3}$**. This is the operational
early-warning lead: the steady plume describes the average threat, but the puff
dynamics give the time at which a sensor would first alarm.

![Puff concentration time series at the downstream receptor.](output/figures/on_her_majestys_secret_service_puff_footprint.png)

### Alpine exfiltration route

The slope-safety-gated planner returns a **safe** route of
**5478.808 m** with a mean grade of **15.24 deg**.
Every step of the reconstructed line respects the declared maximum slope gate
(the route figure).

![Planned route elevation profile along the reconstruction.](output/figures/on_her_majestys_secret_service_route_profile.png)

### Bobsleigh descent and banked-curve clearance

Point-mass kinematics over the canonical bobsleigh track complete the descent
in **37.5 s**, peaking at **45.8 m/s**
(the descent figure). The unbanked canonical hairpin carries
**7.56 g** of lateral load — **over-limit** the 4-g
ceiling — so the line must be banked; a 55-degree bank raises the safe cornering
speed to **47.1 m/s**.

![Bobsleigh descent speed profile along the canonical track.](output/figures/on_her_majestys_secret_service_descent_profile.png)

### Cover identity

The canonical *Bray* persona scores **0.177**
(**low** risk); the dominant exposure driver is forensic
overlap.

### Timeline verification

Auditing the persona's claimed timeline against four sightings yields a
**medium** verdict at **77.8%** coverage
with **1** contradiction(s): a London sighting that
contradicts the Piz Gloria claim. One contradicting observation is enough to
unseat an otherwise-covered story — the cover holds only while the timeline is
unbroken.

## Conclusion — BEDLAM: findings, verdict, and what the mission establishes

The PIZ GLORIA mission software demonstrates a complete, deterministic,
mock-free quantitative pipeline for the kind of operation depicted in
*On Her Majesty's Secret Service*: it models the airborne threat (steady plume *and* time-resolved
puff arrival), the escape line (slope-safe routing *and* bobsleigh descent
kinetics with banked-curve clearance), and the identity risk (weighted *Bray*
persona *and* timeline verification) — all through real scientific algorithms
with real computed data, exposed through the frozen `bond_api` protocol so any
coordinator in the BOND suite can drive it.

Each of the six models is an independent, infrastructure-free pure module, and
the mission adapter in `src/on_her_majestys_secret_service/mission.py` binds
them to the protocol in a thin, auditable layer while leaving the public
protocol shape (film slug, five provider methods, gadget-hook convention)
unchanged. Provenance is recorded for every executed outcome (version, seed,
input hash, wall time). The suite is reproducible by construction: fixed
scenario parameters, fixed seeds, and no random draws yield byte-identical
results across runs, and the manuscript metrics are generated, not authored.

## Experimental Setup — BEDLAM: canonical scenarios, parameters, and configuration

### Scenario parameters

The PIZ GLORIA release and routing scenario is fixed in
`src/on_her_majestys_secret_service/mission.py` and mirrored in
`docs/manuscript/config.yaml`:

* Release rate: `0.05` kg/s aerosolised allergen.
* Free-stream wind speed: `4.0` m/s (inferred stability class `C`, slightly unstable).
* Effective release height: `25.0` m.
* Valley channeling depth: `400.0` m, floor wind ratio `0.6`.
* High-hazard isopleth threshold: `1.0e-7` kg/m^3.
* Route grid: `40 x 40` cells over a 10 km x 10 km analytic range,
 maximum safe slope `30` deg.
* Puff early-warning receptor: `2000` m downwind, threshold `1.0e-8` kg/m^3,
 emission cadence `10` s, initial puff size `1` m.
* Bobsleigh descent: rider+sled mass `100` kg, friction `0.03`, drag area
 `0.45` m^2, air density `1.2` kg/m^3, integration step `0.05` s; canonical
 track with a tight hairpin audited against a `4`-g lateral ceiling and a
 `55`-degree bank for cornering clearance.
* Cover timeline: mission window `[0, 1440)` minutes; `3` claimed events vs
 `4` observed sightings.

### Software environment

* Package: `on_her_majestys_secret_service` 0.1.0
* Python: 3.14.6
* NumPy: 2.4.2
* Protocol: `bond_api` (frozen MissionProvider contract)
* Manuscript variables generated: 2026-08-04T00:00:00+00:00 (UTC)

### Guarantees

Every result value is produced by the executed mission and injected through the
manuscript-variable pipeline; none is hand-written into prose.

## Reproducibility — BEDLAM: verification gates, deterministic regeneration, and artifacts

### Determinism contract

The PIZ GLORIA mission is reproducible by construction:

* Fixed scenario parameters and fixed seed (`7`); randomness is disabled.
* No wall-clock time enters any persisted artifact (provenance `wall_time_s`
 is recorded as `0.0`).
* No mock framework anywhere in the source or tests — all tests are real data
 + computation.
* `output/` is regenerable and git-ignored: re-running
 `scripts/04_execute.py` and `scripts/z_generate_manuscript_variables.py`
 reproduces byte-identical artifacts (a live determinism proof).

### Provenance

Every executed outcome carries a `Provenance` record with package version,
seed, a SHA-256 `input_hash` over the sorted scenario inputs, and wall time.
The outcome is also serialized with the `bond_api` tagged-JSON format so it can
be audited without re-running the film.

### Test coverage

The suite enforces the >=90% line+branch coverage gate on `src/` via
`uv run pytest tests/ --cov=src --cov-fail-under=90`. Live counts and coverage
are tracked in `docs/_generated/COUNTS.md`.

## Scope and Related Work — BEDLAM: boundaries, positioning, and relationship to the literature

### Scope

The PIZ GLORIA software is illustrative mission engineering, not a certified
hazard-assessment tool, and its claims are bounded accordingly:

* **Dispersion** — the steady-state Gaussian plume and its puff-train variant
 are screening models: they assume a continuous release, uniform wind, and
 flat-terrain reflection, and do not model time-varying release composition,
 terrain-following plumes, chemical transformation, or deposition.
* **Descent dynamics** — the point-mass integration is a planar 1-D model:
 no steering, no lateral load transfer into the friction model, and a single
 scalar drag coefficient. The canonical track is analytic, not surveyed.
* **Routing** — the planner operates on an analytic test surface, not surveyed
 terrain, and its 8-connected grid over-approximates feasible continuous
 paths.
* **Cover identity / timeline** — the weighted risk score and interval
 coverage depend on analyst-chosen weights, evidence normalization, and the
 observation set; they are decision aids, not calibrated probabilities.

### Limitations and uncertainty

Beyond the scope boundaries above, the headline numbers carry specific,
unquantified uncertainties that a user should read alongside them:

* **Dispersion coefficients** are the fixed open-country Pasquill-Gifford
 tables, which are screening values, not site-calibrated measurements. The
 isopleth reach and peak location therefore inherit ± a factor of several in
 absolute hazard extent under real alpine meteorology.
* **Valley-channeling** enters as a single scalar floor factor; real
 topography funnels wind non-uniformly, so ground-level concentrations are
 order-of-magnitude estimates.
* **Puff timing** depends on the discrete emission cadence $\Delta t$ and
 initial puff size: the arrival time is accurate to within roughly one
 cadence (10 s) and the transient peak is resolution-dependent.
* **Descent dynamics** are a single-degree-of-freedom point mass with no
 steering or lateral load transfer; the reported speeds and g-loads bound the
 physics but are not a certified vehicle- or rider-specific prediction.
* **Route geometry** is analytic, and the reported distance/grade are
 properties of that surface, not measured survey data.
* **Cover metrics** depend on analyst-chosen weights, evidence normalization,
 and the observation set; they are decision aids with no calibrated
 probability semantics.

These are stated so no headline number is read as a measurement of the world:
each is a deterministic property of the stated model and its fixed inputs.

### Related work

Gaussian plume/puff dispersion follows the classical Pasquill-Gifford
formulation (Arya 1999; Turner 1970) and the Lagrangian puff-train approach
used by operational puff models (Zannetti 1990; Sykes et al. 1998). Point-mass
descent with friction and drag draws on bobsleigh performance framing
[@morlock1989bobsled] (whose scope is strictly the regression in
`99_references.md`; it does not underwrite the rigid-body equations), and alpine slope/avalanche safety rating follows
the standard danger-scale practice (McClung & Schaerer 2006). Interval-based
timeline verification uses standard interval arithmetic / coverage analysis.
Where a precise field value matters, the open-country dispersion coefficients
are the fixed, cited data tables in `dispersion_model.py`.

## Sources — BEDLAM: bibliography

@arya1999dispersion; @turner1970workbook; @zannetti1990air; @sykes1998scipuff; @morlock1989bobsled; @mcclung2006avalanche; @cormen2009algorithms


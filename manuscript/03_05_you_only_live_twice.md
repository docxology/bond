# You Only Live Twice (1967) — BIRD ONE

*film package · mission codename BIRD ONE*. Mission **VOLCANO**: solve space-capsule rendezvous and intercept windows; engineer the orbital capture and phasing of the enemy capsule; detect the concealed volcano-camouflaged lair; localize the hidden base by Bayesian cue fusion and RF emission; plan the infiltration route into the lair; characterize the adversary base pattern of life.

This chapter reproduces the package's complete manuscript verbatim:
the abstract and every authored section, token-hydrated from the
package's own manuscript variables, with the package's figures carried
in the combined PDF and its sources resolved against the unified
bibliography.

## Concepts

orbital capture, hidden-base discovery

## Abstract

YOU ONLY LIVE TWICE (1967), mission codename VOLCANO, is special-agent mission software for the adversary-prosecution problem a single agent faces when the enemy's base is hidden inside a volcano and the enemy's capsule must be swallowed out of orbit. This package implements seven deterministic, quantitative capabilities and reports them through the frozen BOND-API mission protocol. The **rendezvous / intercept solver** propagates two circular orbits under two-body Keplerian mechanics and finds every contiguous window where the chase spacecraft can acquire the target: the nominal scenario yields 1 window(s) in a one-day horizon, opening at 32940.0 seconds with a peak elevation of 82.77°, and a coplanar Hohmann intercept costs 133.4 m/s over 2943.0 seconds. The **orbital capture** model then turns this into a phasing problem — the platform waits 31989.1 seconds for the 4.69° lead angle and grapples with a 982.8 m/s velocity-matching burn inside 1 capture window(s). The **concealed-lair detector** fuses thermal and terrain anomaly scoring to locate a volcano-camouflaged structure, reporting 6 candidate region(s), the strongest with a fused score of 8.55. The **hidden-base discovery** engine then fuses those cues with passive RF and a terrain-weighted prior, reaching the injected 80-cell lair footprint at rank 1 of 4096 candidate sites (P-found-within-10-sites 0.9999); the injected *centre cell* is not recovered — it ranks 80, 5656.9 m from the posterior peak. The **infiltration planner** routes an agent to the lair on a slope/thermal/guard-exposure cost surface, cutting route cost by 36.11 % over a goal-reaching greedy baseline, and the **emitter locator** fixes the base's transmitter by TDOA multilateration to within 3.7912 m using 5 passive sensors whose timings carry a 10.0 ns jitter, backed by a deterministic 6-level error envelope vs jitter. Finally the **pattern-of-life analyzer** reads a week of base activity (311 events), finding 2 daily operating window(s) (07-09h; 19-21h) with a medium operational tempo and duty cycle 0.679. Every number above is computed, never hand-authored: the manuscript renders entirely from the deterministic scenario (seed 1967, provenance 69984c9e423de2cf).

## Introduction

In *You Only Live Twice* (1967), the adversary's base is a volcano that swallows
spacecraft whole, and the mission is won by knowing *where* the enemy is and
*when* they act. The VOLCANO package turns that intelligence problem into
seven computational ones an agent can solve ahead of time with deterministic,
reproducible mathematics:

1. **When can we reach them?** Orbit geometry decides the rendezvous windows.
2. **How do we capture them?** Phasing decides when the capsule can be
 grappled and its velocity matched.
3. **Where are they hiding?** A concealed base leaks heat and flattens terrain,
 even when painted to look like a mountain.
4. **Does the evidence point to one site?** Bayesian fusion turns heterogeneous
 sensor cues into a search plan — and reports whether any single cue would
 have sufficed, rather than assuming fusion was what found the base.
5. **How do we get in?** A*, not guesswork, plans the infiltration route.
6. **Where is their transmitter?** TDOA multilateration fixes the base's radio.
7. **How do they operate?** A base keeps a rhythm; activity events reveal it.

The package is built in the BOND suite's style: a pure, infrastructure-free
domain core (the seven capabilities), a thin BOND-API adapter exposing it as a
`MissionProvider` (codename VOLCANO), and a manuscript that
hydrates every numeric claim from a fixed scenario rather than from prose.

### Reader's guide

- `rendezvous_windows.py` — orbital mechanics for rendezvous / intercept
 window solving.
- `orbital_capture.py` — capture envelope, velocity-matching burn, phasing.
- `terrain_anomaly.py` — thermal + terrain anomaly scoring for lair detection.
- `hidden_base_discovery.py` — Bayesian cue fusion and search planning.
- `infiltration_planning.py` — terrain/thermal/guard cost surfaces and A*.
- `emitter_localization.py` — TDOA hyperbolic emitter localization.
- `pattern_of_life.py` — weekly activity analysis.
- `mission.py` — the VOLCANO `MissionProvider`.
- `scripts/run_mission.py` — a thin CLI for every mission phase
 (`brief` / `recon` / `plan` / `execute` / `debrief`).

The remainder of the manuscript details the methodology (Section 2), the
results (Section 3), the experimental setup (Section 5), and reproducibility
(Section 6).

## Methodology

This section states the mathematics behind each of the seven capabilities.
Everything is standard, deterministic, and free of hidden randomness.

### 1. Rendezvous / intercept window solving

Both spacecraft are modelled as two-body circular orbits. The mean orbital
motion of a circular orbit of radius $a$ under gravitational parameter
$\mu$ is

$$ n = \sqrt{\frac{\mu}{a^3}} $$

and the position and velocity in the Earth-centred inertial (ECI) frame follow
from the classical orbital elements $(a, e=0, i, \Omega, \nu)$ via the standard
perifocal → ECI 3-1-3 rotation. The true anomaly advances linearly,
$\nu(t) = u_0 + n t$, so a candidate orbit is fully described by its altitude,
inclination, RAAN, and initial argument of latitude $u_0$.

Given the chaser state $(\mathbf{r}_c, \mathbf{v}_c)$ and the target position
$\mathbf{r}_t$, the line-of-sight vector is
$\boldsymbol{\rho} = \mathbf{r}_t - \mathbf{r}_c$ with slant range
$\rho = \lVert \mathbf{r}_t - \mathbf{r}_c \rVert$ and target elevation
$\varepsilon$ above the chaser's local horizontal plane. A **rendezvous
window** is a contiguous interval on which $\rho \le \rho_\text{max}$ and
$\varepsilon \ge \varepsilon_\text{min}$. The intercept burn is a coplanar
Hohmann transfer with the two-impulse budget
$\Delta v$ and transfer time equal to half the transfer-orbit period.

### 2. Orbital capture and phasing

Capturing the capsule is a *phasing* problem [@bate1971; @vallado2013;
@fehse2003]. The
chaser (the capture platform on the target's orbit) must wait until the target
leads it by exactly the angle

$$ \lambda = (\pi - n_t T_t) \bmod 2\pi, $$

where $T_t$ is the Hohmann transfer time and $n_t$ the target mean motion — the
transfer sweeps $\pi$ rad, so the target must start ahead by
$\pi - n_t T_t$. The relative phase evolves as
$\phi(t) = \phi_0 + (n_t - n_c)t$, so the **phasing wait time** is the first
non-negative solution of $\phi(t) \equiv \lambda \pmod{2\pi}$.

A **capture window** is a contiguous interval where the capsule is inside the
grapple envelope (range constraint) *and* slow enough that the platform can
match its velocity; the **velocity-matching burn** is exactly the relative
speed $\lVert \mathbf{v}_t - \mathbf{v}_c\rVert$ at that epoch, nulling the
relative velocity for a physical grapple.

### 3. Concealed-lair detection via thermal + terrain anomaly

A concealed lair is found by scoring each channel against a locally modelled
background — the standard formulation of statistical anomaly detection, where
"anomalous" means *improbable under the fitted background model* rather than
merely bright [@reed1990; @chandola2009]. A Gaussian low-pass
$\tilde{g} = K_\sigma \ast g$ approximates the
smooth natural signal, and each pixel is expressed as a standardized residual
$z_{ij} = (g_{ij} - \tilde{g}_{ij})/\sigma_{\text{res}}$. The **thermal
anomaly** is the one-tailed $z$ (we look for excess heat); the **terrain
anomaly** is the magnitude $|z|$ (a lair may be a raised shelf *or* an
excavated depression). The two maps are fused with weights
$w_T, w_D$ as $s_{ij} = (w_T z^T_{ij} + w_D z^D_{ij})/(w_T + w_D)$.
Connected components of the thresholded fused map are labelled and reported as
candidate regions, ranked by peak fused score.

### 4. Hidden-base discovery by Bayesian cue fusion

To decide *where* the base is before a strike, the mission treats each of the
$N$ candidate cells as a hypothesis and applies Bayesian belief updating
[@pearl1988].

*What counts as ground truth here.* The evaluated truth is the lair the scene
generator injects — its centre cell and its carved footprint — determined by
the cone centre and a fixed offset before any anomaly map exists. It is not the
argmax of the fused anomaly map, and the passive-RF cue is generated at the
injected site rather than at the detector's answer. Nothing the posterior
consumes is derived from the quantity the posterior is asked to recover, so the
reported ranks are measurements and not identities.

Cell $c$ carries a prior $P(c) \propto 1 + \beta\max(0,z^D_c)$
(terrain anomalies raise the prior). Each sensor cue $z$ is modelled as a
Gaussian measurement with likelihood ratio

$$ \text{LR}(z) = \exp\!\left(\frac{\mu z}{\sigma^2}\right), $$

so a neutral cell maps to 1, a hot cell to $>1$, a cold cell to $<1$. The
posterior is the normalized product

$$ P(c \mid \text{cues}) \propto P(c)\prod_i \text{LR}_i(c). $$

Searching greedily by descending posterior gives a deterministic **search
order** — the optimal policy for a uniform-cost, perfect-detection search
[@stone1975]. Two distinct effort statistics are reported and must not be
conflated: the **realised effort** is the rank of the known true site (an
after-the-fact validation number), while the **posterior expected effort**
$E[K] = \sum_{k} k\,P(c_k)$ is a property of the posterior alone and is the
number a planner can quote before the base is confirmed. The **discovery
curve** $\sum_{k} P(c_k)$ is the probability the base is found within the first
$k$ searches. Combining heterogeneous sensors this way is the standard
multisensor-fusion construction [@waltz1990].

### 5. Infiltration planning

The agent must reach the lair core while minimizing detection risk. Each cell
carries a movement cost

$$ \text{cost} = 1 + w_s\,\hat{s} + w_T\,z^T_+ + w_G\,\hat{g}, $$

combining normalized slope $\hat{s}$, positive thermal-exposure $z^T_+$,
guard line-of-sight exposure $\hat{g}$ (an elevation-occluded visibility count
from every watch post), and an impassable-lava mask. A deterministic 4-connected
**A*** search [@hart1968; @cormen2009] with an admissible Manhattan heuristic
returns the optimal route — admissibility holds because every step costs at
least $1$ and the heuristic counts steps, so A* is guaranteed optimal.

The baseline is a greedy depth-first walk over the *same* search space: it
always steps to the cheapest-looking unvisited neighbour and retraces one cell
when it dead-ends, paying that cell's cost again. Two conditions are needed for
the reported reduction to be non-negative by optimality rather than by a
favourable comparator, and both are enforced in code. The baseline must live in
the same 4-connected space over the same cost field — it does — *and* it must
actually reach the goal, because A* minimises over goal-reaching walks only. A
baseline that abandoned the search at a dead end would report the cost of a
shorter journey, which can be below the optimal cost of the full journey and
would make the reduction negative; the implementation therefore backtracks and
raises when the goal is unreachable instead of returning a truncated route.
`tests/test_infiltration_planning.py` pins a concrete grid on which the
non-backtracking version returns a truncated walk cheaper than the optimum.

### 6. Emitter localization by TDOA

Passive sensors at positions $\mathbf{s}_i$ time the arrival of the base's RF
burst. The range differences against a reference sensor,
$d_i = \lVert e-\mathbf{s}_i\rVert - \lVert e-\mathbf{s}_0\rVert$, define
hyperbolae whose intersection is the emitter $e$ [@skolnik2001; @chan1994]. The
estimate $\hat{e}$ minimizes the residuals via the Taylor-series (Gauss–Newton)
iteration on the normal equations [@foy1976], which converges to the true
emitter for exact measurements. Receivers report *time* differences; these are
converted to the range differences the geometry is solved in by multiplying by
the propagation speed, so the speed of light never enters the estimator itself.

Exact measurements make the solve a round-trip identity of the forward model:
it returns the injected point to machine precision by construction, which
checks solver–model consistency but measures no accuracy. The reported figure
therefore comes from receiver timings perturbed by a fixed-seed Gaussian jitter
of $\sigma_t$ before the conversion to ranges, so the error reflects a
geometry-dependent dilution of precision and can degrade.

### 7. Pattern-of-life analysis

A base's activity is modelled as an inhomogeneous Poisson point process
[@daley2003] whose instantaneous rate follows a diurnal envelope; events are
drawn by rejection sampling against that envelope, so the injected rhythm is
exactly known and the analysis can be checked against it. The observed events
are binned into a
$7\times 24$ hourly histogram, giving a mean daily profile
$\bar{p}_h = \tfrac{1}{7}\sum_d h_{d,h}$. The dominant operational periodicity
comes from the normalized autocorrelation, contiguous hours above a percentile
are **peak operating windows**, and tempo is classified from the mean event
rate.

## Results

All results come from the deterministic VOLCANO scenario (seed
1967, provenance hash 69984c9e423de2cf) and are injected as
tokens — none are hand-authored.

### Rendezvous / intercept windows

Over a one-day horizon the geometry admits 1
rendezvous window(s). The first opens at 32940.0 seconds
after mission start and lasts 1020.0 seconds, peaking
at a target elevation of 82.77°. Figure
 shows the slant-range and elevation evolution with the
accepted window shaded.

![Rendezvous geometry: slant range (top) and target elevation (bottom) vs time, with the viable window shaded.](output/figures/you_only_live_twice_rendezvous_windows.png)

For an intercept, a coplanar Hohmann transfer burns a total of
133.4 m/s and takes 2943.0
seconds.

### Orbital capture

Adding the capture envelope (range + relative-speed constraint) yields
1 capture window(s), the first opening at
32280.0 seconds and lasting
2400.0 seconds; the grapple still needs a
velocity-matching burn of 982.8 m/s. The phasing solution
requires a 4.69° lead angle, reached after a
31989.1 second wait. Figure shows the range
and relative-speed profile with the capture window shaded.

![Orbital capture: slant range (top) and relative speed (bottom) vs time, with the grapple window shaded.](output/figures/you_only_live_twice_orbital_capture.png)

### Concealed-lair detection

The thermal and terrain anomaly fusion surfaces
6 candidate region(s); the strongest covers
272 cells with a fused score of
8.55 (thermal 7.622, terrain
9.478). Figure shows the raw scenes and the
fused anomaly map with the top candidate boxed.

Measured against the injected facility — a 80-cell shelf
carved at a location fixed by the scene geometry, before any sensor map is
computed — the detector's peak falls inside the footprint
(yes) but **not** on its centre: it sits
5.66 cells (5656.9 m) away. That
offset is the expected behaviour of a high-pass anomaly score, which peaks on
the rim of a carved shelf where the discontinuity against the smooth background
model is largest, not at its centroid. The detector localizes the *facility*,
not its centre point, and only the first of those claims is supported here.

![Concealed-lair detection: thermal scene, terrain scene, and fused anomaly score with the top candidate region marked.](output/figures/you_only_live_twice_concealed_lair_detection.png)

### Hidden-base discovery

The ground truth for this section is the injected lair — its centre cell and
its 80-cell carved footprint — both fixed by the
scene's construction parameters and *not* derived from any anomaly map the
posterior consumes. The RF cue is generated at that injected site, so no cue is
centred on the detector's own answer.

Fusing the thermal, terrain and RF cues with a terrain-weighted prior over the
4096 candidate sites, a greedy posterior-order search
first enters the injected footprint at rank 1, and
the footprint carries posterior mass 1.0 — the
mass outside it falls below the reported precision. The footprint is
80 of 4096 cells, so this
is a real hit rather than an arithmetic certainty.

The stricter question — does the posterior peak land on the injected *centre
cell*? — is answered **no**. The centre cell ranks
80 with posterior 1.08e-15,
and the peak sits 5656.9 m from it, for the same
rim-versus-centroid reason as above. This paper claims footprint-level
recovery only; cell-level recovery of the centroid is not established.

Fusion was also not what made the find. Scoring each cue on its own (prior x
that single likelihood-ratio map) gives footprint ranks
prior_only 1, rf 1, terrain 1, thermal 1 — every individual cue, and the terrain-weighted
prior by itself, already ranks the footprint first. In this scene the cues are
strong, not weak; fusion sharpens the posterior and adds redundancy, and the
claim that the base could only be found by combining weak sensors would be
false here.

Independently of any ground truth, the posterior-weighted expected effort — the
mean number of sites a greedy search inspects, $\sum_k k\,P(c_k)$ — is
1.05 cell(s) against a uniform-prior expectation
of half the field, and the search finds a footprint cell within ten sites with
probability 0.9999. Figure shows the
posterior map with the injected footprint, the injected centre, and the
posterior peak marked separately.

![Hidden-base discovery: posterior probability map with the injected lair footprint, the injected centre (ground truth) and the posterior peak (estimate) marked separately.](output/figures/you_only_live_twice_hidden_base_discovery.png)

### Infiltration planning

The slope/thermal/guard cost surface routes the agent from the rim to the lair
in 48 steps at a total cost of
73.834, against a greedy baseline of
115.557 — a 36.11 % cost
reduction (fraction 0.3611) — accruing a thermal exposure
of 2.0694 over 922 expanded cells.
Figure
 shows the cost field and the optimal route.

![Infiltration route: movement-cost field with the optimal route (red), entry (green), lair (cyan) and guard posts (orange).](output/figures/you_only_live_twice_infiltration_route.png)

### Emitter localization

Passive TDOA multilateration over 5 sensors fixes the base's
transmitter to within 3.7912 m of the injected emitter in
6 iterations. The receivers report arrival-time
differences carrying a 10.0 ns (1σ) timing jitter, applied
before the conversion to ranges, so this error is an achieved accuracy that can
degrade — not the machine-zero a noise-free round trip through the same forward
model returns by construction. Figure shows the sensor ring, the
range-difference hyperbolae converging on the injected transmitter, and the
converged fix, imagery candidate and injected truth marked separately.

![Emitter localization: TDOA sensor ring with the range-difference hyperbolae (grey), the converged fix (+), the injected emitter (×) and the imagery-derived candidate (○).](output/figures/you_only_live_twice_emitter_localization.png)

A single operating point is not an accuracy envelope, so the deterministic
sweep of 6 timing-jitter levels — each averaged over
24 fixed-seed realizations at the same emitter and
sensor ring — characterises how the mean error grows with the receiver jitter:
sweeping σₜ over (0.0, 10.0, 20.0, 50.0, 100.0, 200.0) ns gives mean errors of
(0.0, 2.0, 3.6, 9.7, 19.2, 41.3) m respectively. The mean error rises from zero
(the noiseless round-trip identity) to 41.3 m at
200.0 ns — a monotone envelope for this geometry,
reported through Figure rather than asserted.

![Emitter accuracy envelope: mean localisation error vs receiver timing jitter σₜ.](output/figures/you_only_live_twice_emitter_error_sweep.png)

The radio and imagery chains share no measurement, so comparing them is a
genuine cross-modal check, and they do **not** agree on a cell: the TDOA fix
lands 5655.5 m from the imagery-derived candidate, which
is essentially the whole 5656.9 m by which the
anomaly peak is itself displaced from the facility centre. The two modalities
agree on the facility and disagree on the point within it, by the full width of
that rim-versus-centroid offset; the radio fix is the accurate one, because the
emitter is where the transmitter was injected and the anomaly peak is not.

### Pattern of life

A week of 311 base events resolves into
2 daily operating window(s)
(07-09h; 19-21h), a dominant period of
12.0 hours, a duty cycle of
0.679, and a medium operational tempo. Figure
 visualizes the weekly and daily rhythms with the peak windows
shaded.

![Pattern of life: weekly activity histogram (top) and mean daily profile with detected peak windows (bottom).](output/figures/you_only_live_twice_pattern_of_life.png)

### End-to-end mission

The BOND-API provider (codename VOLCANO) executes all seven
capabilities in a single deterministic run against 11
frozen protocol dataclasses across 5 provider
methods, returning full provenance.

## Conclusion

The VOLCANO package demonstrates that a single-agent mission intelligence
problem — where to intercept, how to capture, where the enemy hides, how to get
in, how to localize its radio, and how it operates — can be answered with
deterministic, reproducible mathematics rather than guesswork. Each of the
seven capabilities is a real computation over real data:

* the **rendezvous / intercept solver** turns orbital elements into actionable
 windows and $\Delta v$ budgets;
* the **orbital capture** model turns a capture into a phasing problem with a
 well-defined lead angle, wait time, and velocity-matching burn;
* the **concealed-lair detector** fuses thermal and terrain anomaly scoring to
 surface a volcano-camouflaged structure, landing inside the injected
 footprint but 5656.9 m from its centre;
* the **hidden-base discovery** engine turns those cues plus passive RF into a
 posterior and a search plan that reaches the injected footprint at rank
 1;
* the **infiltration planner** finds a provably optimal (A*) route that
 measurably beats a greedy baseline over the same search space;
* the **emitter locator** fixes the base's transmitter by TDOA to
 3.7912 m from noisy receiver timings;
* the **pattern-of-life analyzer** extracts a base's operating rhythm from a
 week of activity events.

Three limitations are worth stating plainly rather than leaving to a reader to
discover. First, the anomaly detector and the Bayesian posterior recover the
lair's *footprint*, not its centre cell: both peak on the carved rim,
5656.9 m off the injected centroid, and the centroid ranks
80 in the search order. Second, fusion is not what
finds the base in this scene — each cue alone already ranks the footprint first
(prior_only 1, rf 1, terrain 1, thermal 1), so this is a demonstration of consistent
multi-cue evidence, not of weak-signal fusion. Third, the scene is synthetic
and single: these numbers characterise one deterministic scenario, not a
detection performance envelope, which would need a swept ensemble of scenes
with varied camouflage, noise and lair geometry. A partial exception is the
emitter localiser, whose deterministic error-versus-jitter envelope
(6 levels, 24 realizations
each) is now reported alongside the operating point; the fixed emitter–sensor
geometry and the single base scene remain single-scenario.

Because every result flows from a fixed seed through token-injected prose, the
manuscript and the computation can never drift apart: re-running the analysis
re-hydrates every number in this document. The package is one film in the BOND
suite, exposing its capabilities through the frozen BOND-API mission protocol
so any coordinator can drive it without knowing its internals, and keeping its
pure domain core importable without the protocol at all.

## Experimental Setup

The scenario is fixed in `src/you_only_live_twice/scenario.py`, which exports
every input as a named constant and assembles them into one JSON descriptor.
That descriptor is simultaneously (a) the object the provenance `input_hash` is
taken over and (b) the source of the parameter tokens in the tables below, so a
parameter reported here cannot drift from the parameter actually simulated.
Paper identity is declared in `manuscript/config.yaml`; all derived values are
computed by `src/you_only_live_twice/manuscript_variables.py`.

### Mission identity

| Parameter | Value |
| --- | --- |
| Random seed | 1967 |
| Provenance input hash (16 hex) | 69984c9e423de2cf |

### Orbital geometry

| Parameter | Chaser | Target |
| --- | --- | --- |
| Altitude (km) | 550.0 | 800.0 |
| Inclination (°) | 98.2 | 98.2 |
| RAAN (°) | 45.0 | 45.5 |
| Initial phase (rad) | 0.0 | 1.9 |

### Search envelopes

| Parameter | Value |
| --- | --- |
| Rendezvous horizon / step (s) | 86400.0 / 60.0 |
| Rendezvous max range (km) | 500.0 |
| Rendezvous min elevation (°) | 10.0 |
| Capture max range (km) | 1000.0 |
| Capture max relative speed (m/s) | 2200.0 |
| Capture step (s) | 120.0 |

### Scene, sensors and cost model

| Parameter | Value |
| --- | --- |
| Volcano grid (cells per side) | 64 |
| Cone radius (cells) / height (m) | 20.0 / 2000.0 |
| Lair thermal excess (K) | 25.0 |
| Activity rate (events/h) over horizon (h) | 4.0 over 168 |
| Discovery cue mean $\mu$ / prior weight $\beta$ | 2.5 / 1.5 |
| Discovery RF source power | 8.0 |
| Infiltration weights (slope / thermal / guard) | 2.0 / 3.0 / 4.0 |
| TDOA sensor ring radius (m) / count | 25000.0 / 5 |
| TDOA receiver timing jitter $\sigma_t$ (ns, 1σ) | 10.0 |
| TDOA error-envelope max jitter (ns) / realizations per level | 200.0 / 24 |
| Injected lair footprint (cells) | 80 |

### Rendering pipeline

The manuscript is rendered entirely from the deterministic scenario:

1. `scripts/z_generate_manuscript_variables.py` writes
 `output/data/manuscript_variables.json` (11 protocol
 dataclasses, 5 provider methods).
2. `scripts/render_figures.py` writes the 8 figures under
 `output/figures/`.
3. Prose substitutes every token reference with its computed value, so numbers stay in lock-step with the scenario.

### Software environment

- Package version 0.1.0 (`YOU ONLY LIVE TWICE`, film
 1967).
- Python 3.14.6 on darwin; numpy, matplotlib, pyyaml, and the
 frozen `bond-api` protocol.
- Generated 2026-08-04.

### Test gate

The suite runs `pytest` with `--cov=src --cov-fail-under=90` (line **and**
branch). Live test counts and the achieved coverage percentage are tracked in
`docs/_generated/COUNTS.md`, not hardcoded here.

## Reproducibility

The VOLCANO package is reproducible by construction.

### Determinism

* Every generator is driven by a fixed seed (1967). No untracked
 random draws are permitted anywhere in `src/`.
* No wall-clock value enters a persisted artifact: the generation timestamp in
 this manuscript is a fixed date, and provenance carries an explicit seed with
 `wall_time_s` held at zero.
* The mission's provenance `input_hash` (69984c9e423de2cf) is a stable
 sha256 fingerprint of the scenario descriptor, so an outcome can be audited
 without re-running the simulation.

### Artifacts

All 8 figures are enumerated by
`you_only_live_twice.figures.FIGURE_FILENAMES`, the single source both the
render script and this table follow.

| Artifact | Location | Regenerated by |
| --- | --- | --- |
| Manuscript variables | `output/data/manuscript_variables.json` | `scripts/z_generate_manuscript_variables.py` |
| Rendezvous figure | `output/figures/rendezvous_windows.png` | `scripts/render_figures.py` |
| Orbital-capture figure | `output/figures/orbital_capture.png` | `scripts/render_figures.py` |
| Lair-detection figure | `output/figures/concealed_lair_detection.png` | `scripts/render_figures.py` |
| Hidden-base posterior figure | `output/figures/hidden_base_discovery.png` | `scripts/render_figures.py` |
| Infiltration-route figure | `output/figures/infiltration_route.png` | `scripts/render_figures.py` |
| Pattern figure | `output/figures/pattern_of_life.png` | `scripts/render_figures.py` |
| Emitter-localisation figure | `output/figures/emitter_localization.png` | `scripts/render_figures.py` |
| Emitter error-envelope figure | `output/figures/emitter_error_sweep.png` | `scripts/render_figures.py` |

`output/` is git-ignored; a fresh run regenerates a byte-identical tree.

### Test gate

The enforced quality gate is:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

with ruff (check + format) and mypy green on `src/` and `scripts/`. Live
counts live in `docs/_generated/COUNTS.md`. The suite uses real computation and
no mock framework, so a green gate means the algorithms were actually exercised.

## Scope and Related Work

### Scope

The VOLCANO package covers seven special-agent analytical capabilities over a
single fixed scenario. Its scope is deliberately bounded:

* **Orbital mechanics** assumes circular two-body orbits; eccentric,
 perturbed, or multi-body motion (J2, drag, third-body) is out of scope.
 Window finding is a deterministic grid search, not an optimizer.
* **Orbital capture** models the coplanar phasing problem; out-of-plane plane
 changes and finite-burn effects are not modelled.
* **Lair detection** scores a synthetic volcano-camouflage scene. It
 demonstrates the anomaly-scoring *method* on real synthetic data; it is not a
 claim about any real imagery. What is established is that the fused peak
 falls inside the injected lair *footprint*; the peak sits
 5656.9 m from the injected centre cell, so centre-cell
 localization is **not** established.
* **Hidden-base discovery** uses a naive-Bayes fusion of Gaussian sensor cues;
 it does not model correlated or missing measurements. In this scene the cues
 are not weak — every single cue ranks the footprint first on its own
 (prior_only 1, rf 1, terrain 1, thermal 1) — so the results demonstrate consistent
 multi-cue evidence, not weak-signal fusion. Detection performance across
 varied camouflage, noise levels and lair geometries would need a swept
 ensemble of scenes; one scenario cannot supply it.
* **Infiltration planning** is a static 4-connected A* over a fixed cost
 surface; it does not model dynamic guards or replanning.
* **Emitter localization** solves TDOA at one emitter–sensor geometry with a
 Gaussian timing-jitter model. Error versus jitter is now characterisable: a
 deterministic sweep of 6 jitter levels (each averaged
 over 24 realizations) reports the mean-error
 envelope, rising from zero to 41.3 m at
 200.0 ns. Error versus *geometry* — multipath,
 timing bias, and a swept sensor-ring geometry — remains out of scope; the
 reported 3.7912 m is the operating point inside that envelope,
 not a statement across geometries.
* **Pattern of life** uses a diurnal-rate Poisson model of activity. It
 recovers the model's injected rhythm; it does not claim general time-series
 universality.

Nothing here is fielded operational software — it is a rigorous, reproducible
exemplar of the underlying mathematics, in keeping with the BOND suite's
research-exemplar contract.

### Related work

The methodology draws on established, citable foundations rather than novel
claims:

* Orbital-element → ECI conversion, circular propagation, the Hohmann
 transfer, and the phasing problem follow standard treatments of
 astrodynamics [@vallado2013; @bate1971].
* Rendezvous / proximity geometry and operational feasibility windows are
 standard in human and robotic spaceflight mission design [@wertz2011;
 @fehse2003].
* Anomaly scoring by standardized residual against a fitted background is the
 classical statistical formulation of anomaly detection, of which the
 RX detector is the canonical imaging instance [@reed1990; @chandola2009].
* Bayesian cue fusion for a hidden-site hypothesis set follows Pearl's belief
 updating framework [@pearl1988]; ordering the resulting posterior into a
 search plan is classical search theory [@stone1975], and combining
 heterogeneous sensors follows the multisensor-fusion literature [@waltz1990].
* Passive RF emitter location by TDOA follows the Taylor-series estimator
 [@foy1976] and the hyperbolic-location literature [@chan1994; @skolnik2001].
* Infiltration routing is textbook best-first search / A* [@hart1968;
 @cormen2009].
* Modelling base activity as an inhomogeneous Poisson point process, and
 reading tempo off its rate envelope, follows standard point-process theory
 [@daley2003].

The self-consistency guarantee — every manuscript number computed from a fixed
seed and token-injected — follows the template's reproducible-research
convention documented in the BOND suite.

### Limitations and future work

Integration points for later BOND capabilities are recorded in `TODO.md`: a
perturbation-aware propagator, a spline-refined window edge detector, and
binding to the shared `bond-utilities` provenance helper once that dependency
ships.

## Sources

@vallado2013; @bate1971; @wertz2011; @fehse2003; @reed1990; @chandola2009; @pearl1988; @stone1975; @waltz1990; @hart1968; @cormen2009; @foy1976; @chan1994; @skolnik2001; @daley2003


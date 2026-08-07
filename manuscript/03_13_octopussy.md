# Octopussy (1983) — FABERGE

*film package · package codename FABERGE*. Mission **FABERGÉ**: detect artifact forgeries via spectral/UV fingerprinting; route smuggled payload under circus cover by min-cost flow; sweep for a concealed nuclear device via radiation and mass anomaly.

## Concepts — FABERGE: domain and operational focus

forgery detection, cover logistics

## Abstract — FABERGE: mission summary

**Octopussy: FABERGÉ — Special-Agent Mission Software** (**Paired Detection: Spectral/UV Forgery Screening and Varnish Dating, Rail Min-Cost Flow and Trainset Circulation, Concealed-Device Sweep and Source Localization**), package Octopussy v0.1.0, implements three investigative disciplines under the mission codename **FABERGÉ**, carried by 6 deterministic pipelines: each discipline pairs a headline detector with a depth module that reads a different observable of the same synthetic scenario. The pairing buys independence of *observable*, not of sample — and, as the varnish result below shows, a second observable is not automatically a second confirmation. First, artifact forgery detection fingerprints painted objects by their combined spectral reflectance and UV fluorescence. A ridge-regularized non-negative least-squares fit identifies each object's pigment composition; whether any pigment post-dates the object's claimed era, how strongly the unexplained spectral residue resembles an anachronistic pigment (matched filter), and the UV fluorescence reading jointly yield a forgery disposition. Against a deterministic exhibit of 4 artifacts drawn from a library of 14 pigments, 4 objects are screened and 2 flagged as forged or likely-forged, with the all-modern composition *forged_dupe* carrying the highest score. **Varnish-ageing kinetics** date two of those same artifacts from film chemistry instead of composition, and the result is deliberately asymmetric. The forger's fresh coat on *forged_dupe* is dated at ~2.8 years against a true 3 and rejected as too_young in 32 of 32 noise realizations. The century-old shellac on *tsar_egg*, claimed 1910, is dated at ~155.5 years against a true 116 and returns a verdict of too_old — but the same ensemble scatters by 54.4 years and yields 3 distinct verdicts (consistent×12, too_young×4, too_old×16) from that one genuine object, because the kinetics saturate. The channel rejects a fresh coat; it decides nothing about an old one. Second, circus-cover smuggling logistics route 3 payload units over a 9-segment rail corridor as minimum-cost flow via successive shortest paths; the resolved plan costs 780 unit-minutes and moves the payload with a makespan of 260 minutes using 2 circus trains, inside the stated capacity and the 400-minute deadline. **Rolling-stock circulation** then bounds the cover itself: 7 circus trips are covered by a minimum of 2 trainsets (a matching of 5 successor links, 100 deadhead minutes), with a depot allocation costing 38.0 minutes. Two computed checks tie that schedule to the routed plan: whether every routed leg is a scheduled trip (True) and whether the fleet covers the trains the flow needs (True). Third, a concealed-device sweep over 100 detectors fuses a radiation anomaly map with shape/mass anomaly screening of 4 cargo containers, flagging hotspot@3,4, royal_egg and ranking hotspot@3,4 first. **Radiation source localization** converts that alarm into a fix: weighted Gauss–Newton estimation recovers the concealed source to within 0.066 metres of its true position, against a fitted positional standard deviation of 0.102 metres (residual 28.664, converged: True). Every pipeline is fully deterministic under a fixed seed (7), producing reproducible, audit-ready provenance.

## Introduction — FABERGE: mission framing, the operational problem, and how to read this chapter

In the 1983 film *Octopussy*, the villain's scheme hides a working nuclear
device inside a Fabergé egg and moves it by circus train across Europe. The
**FABERGÉ** mission software operationalizes the three
investigative disciplines the counter-operation demands: tell a forged
treasure from a real one, route a smuggled payload under cover, and find a
device concealed in plain sight.

This package, **Octopussy: FABERGÉ — Special-Agent Mission Software**, is a BOND-suite film package. It exposes a
deterministic, protocol-conformant mission provider (see the frozen BOND-API
contract) whose *execute* stage runs 6 pure,
infrastructure-free domain pipelines and returns machine-readable verdicts
plus full provenance.

### Three disciplines, 6 pipelines

The governing design decision is that no single detector carries a verdict
alone. Each discipline is implemented twice: a *headline* module that raises
the alarm, and a *depth* module that reaches the same question through
unrelated physics or unrelated mathematics. Disagreement between the two is a
finding. Agreement is evidence only in proportion to the depth module's own
measured uncertainty, which is why the results section reports an error bar
beside every depth verdict rather than the verdict alone.

| Discipline | Headline module | Depth module |
|---|---|---|
| Is this object what it claims to be? | `forgery_detection` — spectral/UV fingerprinting | `varnish_ageing` — Beer–Lambert yellowing kinetics |
| Can the payload move under cover? | `cover_logistics` — min-cost flow over the rail corridor | `rolling_stock` — trainset circulation by bipartite matching |
| Is a device hidden here, and where? | `concealment_sweep` — radiation + shape/mass anomaly fusion | `source_locator` — weighted Gauss–Newton localization |

The pairing matters operationally. Pigment chemistry and varnish kinetics fail
in different directions: a forger who sources period-correct pigments still
cannot age a fresh varnish film, while a genuinely old panel that was recently
restored trips the varnish channel although the pigment channel clears it.
Likewise, a routing plan that satisfies capacity says nothing about whether
enough trainsets exist to fly the cover at all, and a sweep that flags a
container has not yet said where inside the yard the emitter sits.

It matters asymmetrically, though, and that asymmetry is a result rather than a
caveat. Varnish dating is sharp against a recent film and blunt against an old
one, because the yellowing kinetics saturate; the rolling-stock matching bounds
the circus fleet but says nothing about the routed plan until the two are
explicitly compared. Both facts are measured and reported below. Both pipelines
also read the *same* synthetic scenario, so what the pairing establishes is
independence of observable, not independence of sample.

Every module is implemented with real, deterministic algorithms operating on
data generated from physically-motivated forward models — not stubs and not
mocks. The remainder of this manuscript specifies the methodology, reports the
measured outcomes, and documents the reproducibility guarantees.

## Methodology — FABERGE: the analytical models and algorithms that drive the mission

The mission's 6 pipelines share a design principle:
every quantity that reaches a verdict is *measured* or *computed*, never
assumed, and every random draw is seeded so the entire pipeline reproduces
byte-for-byte under a fixed seed (7).

### Spectral/UV forgery detection

A painted artifact is modeled as a weighted mixture drawn from a library of
14 pigments, each with a known reflectance curve over
24 UV-VIS bands spanning
320–760 nm. The instrument observes a
noised reflectance spectrum and a noised UV-fluorescence reading; it never
sees the true composition.

Recovering pigment abundances from a mixed reflectance spectrum is the
spectral-unmixing problem of hyperspectral remote sensing
[@keshava2002spectral], solved here in its non-negative least-squares form
[@lawson1974solving] with a ridge penalty, because the flat "white" pigments
are strongly collinear and an unregularized fit spreads weight arbitrarily
between them.

Three evidence channels are combined:

1. **Anachronism (matched filter + residual improvement).** A
 ridge-regularized non-negative least-squares fit reconstructs the spectrum
 using only era-consistent pigments; the residual — the signal no
 era-consistent pigment explains — is matched against each anachronistic
 pigment's distinctive shape. Strong alignment, or a large shrink in the
 residual when modern pigments are allowed, is direct evidence of a modern
 forgery. Both statistics are deliberately computed from the residual rather
 than from individual fitted weights, which collinearity makes unreliable.
 The *named* set of anachronistic pigments is likewise attributable-evidence
 based: a modern pigment appears in the finding only when admitting it to the
 era-consistent fit explains a material share of the era-inconsistent
 residual. Flat "white" pigments are collinear with the era whites, so their
 fitted weight is not a reliable presence signal — an abundance-only cutoff
 made a genuine period piece "report" modern pigments it does not contain.
 The residual test names a modern pigment only when its spectral shape is
 actually needed, and stays silent about collinear ones it cannot resolve.
2. **UV fluorescence anomaly.** Aged natural-resin varnish fluoresces weakly;
 young synthetic varnishes fluoresce brightly — the observation underlying
 routine UV examination of paint and varnish layers
 [@delarie1982fluorescence]. A reading well above the shellac baseline
 signals a modern surface.
3. **Unexplained spectral residue.** A high era-consistent residual with small
 explained variance indicates a surface no period-legal composition can
 reproduce.

The three channels are weighted and mapped to a disposition:
*genuine / likely_genuine / likely_forged / forged*. The thresholds are
empirical calibrations against the deterministic exhibit's measured score
separation, not free parameters.

### Varnish-ageing kinetics (forgery depth)

Natural resin varnishes yellow over time as photochemical and thermal
degradation accumulates chromophores in the film [@feller1994accelerated;
@horie2010materials]. The module represents this with a saturating exponential
law: the absorbing layer grows as `d(t) = d_max·(1 − exp(−t/τ))` and the
film's transmittance follows Beer–Lambert, `T(λ, t) = exp(−α(λ)·d(t))`, with a
blue-peaked absorption spectrum `α(λ)`. The inverse problem — *given a measured
transmittance, how old is the varnish?* — is solved by a bounded
golden-section least-squares fit over the age axis [@kiefer1953sequential]:
derivative-free, deterministic, and independent of any starting guess. An
object whose varnish is far younger than its claimed provenance is a repaint
or re-varnish — a standalone forgery signal that does not depend on the
pigment screen agreeing.

### Circus-cover logistics (min-cost flow)

The corridor is a directed rail graph of 8 stations and
9 segments carrying integer travel costs and
capacities. Routing the payload from source to sink is a minimum-cost flow
problem [@ahuja1993network; @ford1962flows] solved by successive shortest
paths. Augmenting paths are found with Bellman–Ford [@bellman1958routing]
rather than Dijkstra, because cancelling previously-shipped flow along a
reverse arc carries negative reduced cost. The flow is then decomposed into
per-unit routes to obtain a makespan, a deadline check yields slack, and the
payload is packed into circus trains of fixed wagon capacity. A least-cost
single-courier route is available separately by Dijkstra [@dijkstra1959note].

Feasibility is reported, never assumed: the flow solver raises when the
corridor cannot carry the demand, and the non-raising planner surfaces that as
a plan marked infeasible with zero routed edges and the full deadline missed.

### Rolling-stock circulation (logistics depth)

Beyond routing the payload, the mission must know how many circus trainsets
the schedule truly needs. Treating each trip as a node with a directed edge
`i → j` when a trainset can work `j` after `i` (matching stations,
`depart_j ≥ arrive_i + turnaround`), the minimum number of trainsets equals
`n − M`, where `M` is the maximum bipartite matching — the minimum-path-cover
form of the classical minimum-fleet-size result [@dantzig1954minimizing], and a
standard reduction in train-timetabling practice [@caprara2002train]. The
matching is computed deterministically with Hopcroft–Karp
[@hopcroft1973matching], decomposed into concrete trainset itineraries, and a
Kuhn–Munkres minimum-cost assignment [@kuhn1955hungarian] resolves depot
allocation at minimum total deadhead.

### Concealed-device sweep

Each detector observes a Poisson count rate equal to a background plus the
inverse-square contributions of any emitters — the standard counting model for
scintillation detection [@knoll2010radiation]. A median-filtered background
estimate yields a Poisson-normalized z-score map, and local-maximum peaks above
threshold are reported as hotspots; that threshold is a detection decision
level in the sense of Currie [@currie1968limits]. In parallel, each cargo
container's mass is judged against its category's expected density from a
catalog of 6 physical profiles; a container far
heavier than its volume allows carries a mass anomaly — the signature of a
small dense core inside an ordinary-looking shell. A fused report ranks both
channels into one prioritized suspicion list.

### Radiation source localization (sweep depth)

Flagging a hotspot is not the same as finding the device. Given the detector
lattice and a Poisson background estimate, the concealed emitter is located by
weighted nonlinear least squares. With forward model
`μ_i = B + I/((x_i−x)² + (y_i−y)² + h²)` and weights `w_i = 1/√max(c_i, 1)`,
Gauss–Newton iteration with damped normal equations [@marquardt1963algorithm;
@nocedal2006numerical] and a deterministic step-halving line search minimizes
the weighted residual; an excess-weighted-centroid start keeps the solver
seed-free and reproducible. Inverting the normal matrix yields approximate
positional and intensity standard deviations, so a reported fix always ships
with the precision that justifies it.

## Results — FABERGE: measured outcomes, headline numbers, and what they establish

Executing the FABERGÉ mission (seed 7) produces the following
measured outcomes. Every figure below is emitted by the live run; none is
transcribed by hand.

### Results at a glance

| Pipeline | Measured outcome |
|---|---|
| Forgery detection | 4 artifacts screened, 2 flagged as forged / likely-forged |
| Varnish dating (depth) | fresh coat rejected in 32/32 realizations; century-old surface scatters by 54.4 years |
| Cover logistics | cost 780 unit-min, makespan 260 min, slack 140 min |
| Rolling stock (depth) | 2 trainsets over 5 successor links, 100 deadhead min |
| Concealment sweep | flagged hotspot@3,4, royal_egg, worst hotspot@3,4 |
| Source localization (depth) | position error 0.066 m, positional std 0.102 m |

The table collapses the six pipelines into one line each; the sections below
read each result against its own measured uncertainty, which the table does not
— a headline number without its error bar is not a finding.

### Forgery detection

The deterministic exhibit of 4 artifacts yields
4 screened readings, of which
2 are flagged as forged or likely-forged. Per
artifact, the disposition and the anachronistic pigments the residual evidence
actually attributes:

| Artifact | Disposition | Score | Anachronistic pigments |
|---|---:|---:|---|
| tsar_egg | genuine | 0.18 | none |
| ballet_case | genuine | 0.18 | none |
| forged_dupe | forged | 0.54 | phthalocyanine_blue |
| gilt_fake | likely_forged | 0.36 | cadmium_yellow |

The honest period pieces score below the genuine threshold and the detector
attributes *no* modern pigment to them — the attribution is a residual-evidence
finding, not an abundance artifact. The all-modern composition
*forged_dupe* carries the highest forgery score.

The load-bearing case is *gilt_fake*, the least-modern
fake in the exhibit: 50% of its mixture by
weight post-dates its claimed year of 1888 — a chalk
ground that is period-correct, and a cadmium yellow plus an acrylic varnish
that are not — and the earliest offending pigment misses that date by just
22 years. It is nonetheless flagged.

"Least modern" is relative to this exhibit and nothing more. Half a mixture is
not a trace: the harder regime, where a few percent of modern material has to
be resolved out of an otherwise period-correct object, is *not* exercised by
the shipped exhibit and this package makes no claim about it. What the exhibit
does establish is narrower — the screen is not relying on the trivial
all-modern signature, since the other fake is wholly modern by weight and this
one is not. The forgery figure shows the spectral fingerprints and UV
responses that separate the classes.

![Spectral fingerprints of a genuine vs. a forged artifact and their UV
fluorescence responses.](output/figures/octopussy_forgery_fingerprints.png)

### Varnish ageing (forgery depth)

This channel dates two surfaces drawn from the same exhibit the pigment screen
sees: *tsar_egg*, whose natural shellac has been on
the object since its claimed 1910 manufacture, and
*forged_dupe*, whose acrylic coat the forger applied
recently. Each surface is observed as its unvarnished substrate reflectance
attenuated by the varnish film; the film's transmittance is recovered by
dividing out that reference, and the yellowing kinetics are then inverted for
an age.

Read the two results separately, because they are not equally strong.

**The fresh coat is rejected decisively.** Its true age is
3 years; the fit returns
~2.8 years and the verdict is
**too_young** at a claimed-era closeness of
0.024. That is not one lucky draw: re-observing
the same surface under 32 independent noise
realizations gives a spread of only 0.4 years, and
32 of 32
realizations reject the claimed provenance.

**The century-old surface is not resolved at all.** Its authored true age is
116 years, the fit returns
~155.5 years, and the single-draw verdict against its
own claim is too_old. That verdict carries no
information, and the ensemble is what shows it: across
32 realizations of the *same* surface the recovered age
scatters by 54.4 years, spanning
83.1 to 299.8 years; only
12 of 32
land inside the ±15-year tolerance; and the ensemble
produces 3 distinct verdicts
(consistent×12, too_young×4, too_old×16) from one genuine object. Every
outcome the classifier can emit is reachable from this surface by measurement
noise alone, so which one the mission seed happens to draw says nothing about
the object.

The cause is physical rather than numerical: the yellowing kinetics saturate,
so past roughly three time constants a further decade of ageing shifts the
spectrum by less than the measurement noise, and the age stops being
identifiable. A false rejection of a genuine object is therefore as available
to this channel as a false confirmation.

The honest summary of this channel is asymmetric: varnish ageing is a rejection
instrument for recently re-varnished surfaces and is not a confirmation
instrument for old ones. It reads film chemistry rather than pigment
composition, so its rejection of the duplicate does not share the pigment
screen's failure mode; but both channels observe the same synthetic exhibit
under the same authored ground truth, so they are independent in *observable*,
not in *sample*.

That asymmetry is a property of the kinetics, not of one dataset. The varnish figure sweeps true coating age and shows the recovered age tracking truth
until the film is past roughly three time constants — after which the recovered
age scatters beyond any single reading, which is exactly why the century-old
surface above emits every verdict the classifier can produce.

![Recovered varnish age against true coating age, showing the precision
collapse at saturation.](output/figures/octopussy_varnish_scatter.png)

### Cover logistics

Routing 3 payload units across the
9-segment, 8-station corridor
from the Channel fringe to the target station, the min-cost flow resolves at a
total cost of 780 unit-minutes with a makespan of
260 minutes. Against the
400-minute deadline that leaves
140 minutes of slack, carried by
2 circus trains at the capacity limit. The rail figure plots the corridor and the routed flow.

![The FABERGÉ circus rail corridor with routed flow.](output/figures/octopussy_rail_network.png)

### Rolling-stock circulation (logistics depth)

The schedule of 7 circus trips requires only
2 trainsets: a maximum successor matching of
5 links (minimum path cover) resolves the
itineraries with 100 total deadhead minutes. The
Kuhn–Munkres depot allocation reaches a minimum total of
38.0 minutes.

Those trips are a separate scenario from the min-cost flow, so the two
pipelines only bear on each other if something compares them. The mission
computes that comparison and reports it. Each of the
5 station-to-station legs the flow routes must
appear as a scheduled circus trip — every routed leg is covered:
True — and the trains the flow needs
(2) must not exceed the trainsets the schedule
fields (2): True.
Both are computed from the live pipeline outputs, and either goes false if the
route or the schedule changes. What the matching proves on its own is only the
fleet size the circus schedule requires; it is these two checks, not the
matching, that tie the cover to the routed plan.

### Concealment sweep

The 100-detector sweep, laid out as a
10×10 lattice, flags
hotspot@3,4, royal_egg. The fused report ranks hotspot@3,4
highest across 4 screened containers, confirming a
dense sample egg as a flagged mass anomaly — the Fabergé-egg signature of a
small, dense concealed core. The sweep figure renders the radiation count map
with the detected hotspot.

![Concealed-device sweep: radiation count rates with the detected hotspot.](output/figures/octopussy_sweep_heatmap.png)

### Source localization (sweep depth)

Weighted Gauss–Newton localization on the same sweep data recovers the
concealed source to within **0.066 m** of its true
position in 11 iterations, estimating an intensity
of 501.1 and a weighted residual of
28.664 (converged: True). The
fit's own approximate positional standard deviation is
0.102 m, so the achieved error is reported against the
precision the detector geometry supports rather than in isolation. The sweep
therefore both flags the device and fixes where it sits.

The intensity estimate is a different matter and should not be read as a
calibrated activity. Against a true emitter strength of
800 the fit returns
501.1 — a substantial underestimate, while the position
is recovered to centimetres. This is expected rather than anomalous:
intensity, standoff, and the background level trade off against one another in
an inverse-square fit, so the radial scale is poorly constrained by a
single-plane lattice even when the centroid is sharp. The operational claim is
therefore *where the source is*, not *how strong it is*.

## Conclusion — FABERGE: findings, verdict, and what the mission establishes

The **FABERGÉ** mission software demonstrates that three
independent investigative disciplines — spectral/UV forgery detection,
circus-cover logistics by min-cost flow, and fused radiation/mass-anomaly
sweeping — can be implemented as pure, deterministic, infrastructure-free
modules and assembled behind a single frozen mission-provider protocol.

Each discipline is answered twice, through observables that do not share a
failure mode — and the second answer is worth exactly as much as its own error
bar, which is the substantive finding here rather than the pairing itself.

Varnish-ageing kinetics date the surface by film chemistry and reject the
forger's fresh coat in every noise realization. On the century-old surface they
decide nothing: the recovered age scatters by
54.4 years once the yellowing saturates, and the
ensemble emits 3 distinct verdicts from
that single genuine object, so the one the mission seed draws is noise. Read
without that scatter, the same run reads as a second, independent verdict on
authenticity; it is not one. Rolling-stock circulation establishes by matching
that the circus schedule needs 2 trainsets, and two
explicit cross-pipeline checks — every routed leg scheduled, the fleet at least
as large as the trains the flow needs — connect that fleet to the routed plan.
Weighted Gauss–Newton localization converts the sweep's alarm into a position
fixed to 0.066 m, against the positional standard
deviation the geometry supports, while leaving the source intensity
uncalibrated.

What holds across all 6 pipelines is narrower than
mutual confirmation and more defensible: the forgery screen exposes the modern
composition, the logistics plan routes the payload within cover and deadline,
the cross-pipeline cover checks pass, and the sweep both flags the dense egg
and fixes where it sits. All of it is measured on a synthetic scenario whose
ground truth is authored in this package, so these are estimator-behaviour
results, not field results. Each is reproducible under the fixed seed
(7) and carries audit-ready provenance.

The approach generalizes. The same spectral-unmixing, network-flow, matching,
and anomaly-plus-inversion primitives apply to any "hidden in plain sight"
investigative problem — and so does the discipline that pairing a detector with
a second observable is only worth something once the second observable's
uncertainty has been measured rather than assumed.

## Experimental Setup — FABERGE: canonical scenarios, parameters, and configuration

All experiments are configured through `manuscript/config.yaml` and the module
constants in `src/octopussy/`. The pipeline is deterministic: every random
draw comes from `numpy.random.default_rng(seed)` with seed 7.

### Scenario constants

| Pipeline | Configuration |
|---|---|
| Forgery detection | 14-pigment library over 24 UV-VIS bands (320–760 nm) |
| Forgery detection | Exhibit of 4 artifacts screened end-to-end |
| Varnish ageing | Exhibit surfaces *tsar_egg* (claimed 1910) and *forged_dupe*, dated on the same band grid |
| Varnish ageing | Authored true ages 116 y and 3 y; ±15 y consistency tolerance; 32 noise realizations per scatter |
| Cover logistics | 9 directed rail segments across 8 stations |
| Cover logistics | 3 payload units, 400-minute deadline |
| Rolling stock | 7 scheduled circus trips |
| Concealment sweep | 100 detectors on a 10×10 lattice |
| Concealment sweep | 4 cargo containers against 6 density profiles |

Every value in this table is injected from the live package surface rather
than transcribed, so changing a scenario constant in `src/` changes this table
on the next render.

### Environment

Environment used for this report: Python 3.14.6. No generation
timestamp is recorded: a wall-clock stamp used to be injected here and written
into `output/data/manuscript_variables.json`, which made two regenerations
differ and falsified the byte-identity claim in the reproducibility section.
Determinism was judged the more useful property, and mission provenance already
carries an `input_hash`. Versions of the scientific stack (numpy, matplotlib)
are pinned through the package's `pyproject.toml`; the frozen protocol
dependency `bond-api` is resolved as a local path source.

The full run is driven by `scripts/mission_execute.py` (mission outcome and
figures) and `scripts/z_generate_manuscript_variables.py` (token hydration and
the resolved manuscript tree). Neither requires network access.

## Reproducibility — FABERGE: verification gates, deterministic regeneration, and artifacts

Reproducibility is the central guarantee of this package
(Octopussy v0.1.0).

- **Fixed seed.** Every pipeline draws only from generators seeded from
 7; there is no global or untracked randomness. The three
 inverse solvers — the golden-section varnish fit, the Hopcroft–Karp matching,
 and the Gauss–Newton localization — take no random draws at all: each starts
 from a data-derived point and iterates in fixed index order.
- **No wall-clock in persisted artifacts.** The manuscript variable set emits
 no timestamp; the generation stamp that used to appear in
 `output/data/manuscript_variables.json` and in the experimental-setup section
 was removed precisely because it broke the byte-identity claim below.
 `PYTHON_VERSION` is the one remaining environment-derived value, so
 reproduction is byte-identical for a fixed interpreter version and differs in
 that one field across interpreters.
- **Live provenance.** Each mission outcome carries `package_version`, the
 fixed `seed`, and an `input_hash` — a sha256 fingerprint of the mission's
 defining inputs (codename, objectives, and plan) — so an outcome can be
 audited without re-running the film.
- **Generated artifacts.** Figures and manuscript variables are regenerated
 from source by `scripts/mission_execute.py` and
 `scripts/z_generate_manuscript_variables.py`; none are hand-maintained
 snapshots. On a fixed interpreter, regenerating leaves a byte-identical tree
 — asserted, not asserted-about, by
 `tests/test_manuscript_variables.py::test_regeneration_is_byte_identical`,
 which runs the generator twice into separate directories and compares every
 emitted file byte for byte.
- **No hand-authored metrics.** Every number in the abstract, results, and
 conclusion arrives as an injected manuscript token resolved from
 `src/octopussy/manuscript_variables.py` against a live run. A test asserts
 both directions of that contract: no section may use a token the generator
 does not emit, and no generated token may go unreferenced.
- **No mocks.** Tests use real computation only; deterministic reference
 providers implement the real BOND-API protocol.

Report artifacts live under `output/` (regenerated): the mission outcome, the
rendered figures, and the resolved manuscript tree.

## Scope and Related Work — FABERGE: boundaries, positioning, and relationship to the literature

### Scope

This package models the three FABERGÉ disciplines with deterministic,
real-data implementations across 6 pipelines. It does
**not** claim physical fidelity to real forensic spectrometers, real rail
networks, or real scintillation detectors: the underlying models are
physically motivated but illustrative. The
14-pigment library, the
9-segment corridor, and the
6-category container catalog are deterministic
fixtures, not measured instrumentation.

These limits follow and should be read with the results:

- **The exhibit is small and self-authored.** Separation between classes is
 measured on 4 artifacts drawn from the same library
 the detector fits against; it is a demonstration of the method's mechanics,
 not an estimate of field accuracy. There is no genuine period piece using a
 pigment near the anachronism boundary, so the false-positive rate is
 untested.
- **The hard anachronism regime is not exercised.** The exhibit's least-modern
 fake is still 50% modern by weight. Nothing
 here speaks to resolving a trace of modern material out of an otherwise
 period-correct object, which is the case that would actually test the
 matched-filter channel.
- **Ground truth is authored, so these are estimator results.** Every number
 reported here is measured on a synthetic scenario defined in this package —
 the pigment mixtures, the true varnish ages, the emitter position, the rail
 schedule. The results characterize how the estimators behave against a known
 truth; they are not measurements of any physical object, and headline and
 depth modules share that one scenario. The pairing gives independence of
 observable, not independence of sample.
- **The varnish kinetics use one time constant, and they saturate.** Real
 varnish ageing depends on resin, illumination history, and storage; a single
 τ is a first-order stand-in. More consequentially, the saturating exponential
 means that past roughly three time constants a further decade of ageing moves
 the spectrum by less than the measurement noise. As the results section
 reports, the recovered age of the 116-year surface
 scatters by 54.4 years across
 32 noise realizations — wider than the
 ±15-year tolerance it is judged against, and wide
 enough to emit 3 distinct verdicts
 from that one genuine object. This channel can reject a recent re-varnish; on
 an old surface it produces a verdict with no information content, in either
 direction, and none of its old-surface verdicts should be reported as
 evidence.
- **The two cover pipelines are linked by an explicit check, not by
 construction.** The circus schedule is a fixture independent of the min-cost
 flow. The results section reports two computed comparisons that connect them;
 absent those, the matching would bound the circus fleet and say nothing at all
 about the routed corridor plan.
- **The sweep model is idealized.** Counts are Poisson about an inverse-square
 field with no scattering, no attenuation through cargo, and no
 energy-resolved spectroscopy — the discriminants a real portal monitor
 depends on most.
- **Localized intensity is not calibrated activity.** As the results show, the
 fit recovers position to centimetres while substantially underestimating
 emitter strength: intensity, standoff, and background trade off in an
 inverse-square model, and a single-plane detector lattice constrains the
 radial scale weakly. Read the localization output as a position, not as a
 source-strength measurement.

### Related work

Non-negative least-squares spectral unmixing [@lawson1974solving] and matched
filtering are standard in hyperspectral remote sensing
[@keshava2002spectral] and, in the reflectance regime, in cultural-heritage
science for pigment identification; this package applies the same mathematics
to the anachronism test. UV examination of varnish fluorescence is long-
established conservation practice [@delarie1982fluorescence], and the ageing
behaviour of natural resin films is documented in the conservation-materials
literature [@feller1994accelerated; @horie2010materials].

Minimum-cost flow via successive shortest paths is a classical
combinatorial-optimization result [@ford1962flows; @ahuja1993network] built on
the shortest-path algorithms of Bellman [@bellman1958routing] and Dijkstra
[@dijkstra1959note]. Deriving a minimum fleet size from a maximum matching
goes back to Dantzig and Fulkerson [@dantzig1954minimizing] and remains the
standard reduction in railway timetabling [@caprara2002train]; the matching
itself is Hopcroft–Karp [@hopcroft1973matching] and the depot assignment is
Kuhn's Hungarian method [@kuhn1955hungarian].

Poisson background estimation with z-score anomaly detection is standard in
radiation portal monitoring [@knoll2010radiation], with decision thresholds in
the tradition of Currie [@currie1968limits]; damped Gauss–Newton inversion for
source parameters follows standard nonlinear least-squares practice
[@marquardt1963algorithm; @nocedal2006numerical].

The contribution here is not any individual algorithm but the assembly: each
discipline answered by two methods with disjoint failure modes, behind a single
frozen mission protocol, with deterministic and audit-ready provenance — and
with each depth method reporting the uncertainty that determines how much its
agreement is worth.

## Sources — FABERGE: bibliography

@lawson1974solving; @keshava2002spectral; @delarie1982fluorescence; @feller1994accelerated; @horie2010materials; @ford1962flows; @ahuja1993network; @bellman1958routing; @dijkstra1959note; @dantzig1954minimizing; @caprara2002train; @hopcroft1973matching; @kuhn1955hungarian; @knoll2010radiation; @currie1968limits; @kiefer1953sequential; @marquardt1963algorithm; @nocedal2006numerical


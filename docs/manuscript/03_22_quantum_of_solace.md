# Quantum of Solace (2008) — QUANTUM

*film package · package codename QUANTUM*. Mission **QUANTUM**: assess desert water-network resilience under evaporation; quantify cartel leverage over water-rights through dam control; measure multi-resource commodity-control concentration; price water scarcity and the cartel's scarcity rent; rank aqueduct interdiction criticality and network resilience; resolve cooperative power over the commodity portfolio.

## Concepts — QUANTUM: domain and operational focus

resource cartels, hydrology

## Abstract — QUANTUM: mission summary

**Quantum of Solace: QUANTUM — Special-Agent Mission Software** (mission codename **QUANTUM**) is special-agent mission software for the 2008 film *Quantum of Solace*. It models the film's central threat — a shadow cartel whose leverage rests on controlling water and the logistics around scarce commodities — as six deterministic, real-data mathematical systems: 1. **Desert hydrology** — a water network under evaporation, solved with shortest-effort Dijkstra routing and Edmonds–Karp maximum flow (total aquifer yield **80.0** units/period over 5 nodes and 6 routes, of which 80.0 units/period can be routed to settlements); 2. **Water-rights cartel** — reservoir operation and the leverage a cartel gains by withholding downstream releases: controlling 2 of 3 dams (66.7% of the fleet) withholds **25.6%** of the demand the fleet exists to serve — a leverage-to-ownership ratio of 0.38; 3. **Commodity-cartel graph** — multi-resource market concentration via the Herfindahl–Hirschman index (aggregate **3925.0** points across copper, grain, lithium, water, a highly concentrated portfolio); 4. **Water scarcity pricing** — linear-demand economics showing the cartel's cut raises the price from 46.5 to 64.4 and collects a scarcity rent of 2549.6; 5. **Aqueduct interdiction** — 4 of the 6 routes are critical and 2 are redundant; the *mean* retention across single cuts is 0.917 while the single worst cut retains 0.750, and 3 greedy cuts remove 56.2% of delivery; 6. **Cooperative power** — exact Shapley values over the commodity portfolio, with quantum holding the largest share. The package is a BOND-suite film: a pure domain core ships with a thin `bond_api` ``MissionProvider`` adapter, and every number reported is computed, never hand-authored. Keywords navigable for this mission: water-rights cartel, desert hydrology, commodity-cartel graph, herfindahl-hirschman concentration, maximum flow, reservoir leverage, water scarcity pricing, network interdiction, shapley value, deterministic mission software.

## Introduction — QUANTUM: mission framing, the operational problem, and how to read this chapter

*Quantum of Solace* (2008) centres on a shadow organisation whose power derives
not from weapons but from controlling a basic resource: water. This package —
**Quantum of Solace: QUANTUM — Special-Agent Mission Software**, mission codename **QUANTUM** — turns that
premise into executable science. It is one film package in the PROJECT BOND
suite, built to the same guardrails as every sibling: pure domain logic,
deterministic algorithms, real computation with zero mocks, and a thin adapter
to the frozen `bond_api` mission protocol so the suite orchestrator can
discover and drive it by slug.

### The threat model

The film's cartel holds leverage because water is scarce, its distribution is
centralisable, and the same organisation spreads its grip across neighbouring
commodities. We formalise that as six coupled models, each a separate module in
the pure domain core.

**The physical layer — where the water is and how it moves.**

* **Desert hydrology** (`hydrology.py`): a directed network of desert water
 sources, routes and settlements. Evaporation hollows out delivered water, so
 routing and capacity are real constraints, and what a settlement can receive
 is bounded by a maximum flow rather than by nominal aquifer yield.
* **Water-rights cartel** (`water_cartel.py`): a set of reservoirs whose
 released water serves downstream demand. A cartel that controls a dam can
 withhold its normal release and squeeze demand without firing a shot.

**The economic layer — what that control is worth.**

* **Commodity-cartel graph** (`cartel_graph.py`): concentration of control
 across multiple scarce commodities, measured with the Herfindahl–Hirschman
 index, top-k concentration ratios and dominance analysis.
* **Scarcity pricing** (`pricing.py`): the market that converts a withheld
 volume into money — a linear demand curve, the clearing price of a restricted
 supply, the point elasticity that governs how much of a volume cut converts
 into price, and
 the monopoly solution with its deadweight loss.

**The coercive layer — what the cartel can do beyond owning the taps.**

* **Aqueduct interdiction** (`resilience.py`): the fragility of the delivery
 network to cut routes — per-route criticality, a greedy worst-case attack
 sequence, a single-cut resilience index, and minimum cuts.
* **Cooperative power** (`shapley.py`): who can actually capture the value of
 the commodity portfolio, resolved exactly as a transferable-utility coalition
 game via the Shapley value and the Banzhaf–Coleman index.

The layers compose rather than sit side by side: the hydrology network sets the
delivered volumes the interdiction model attacks, and the reservoir simulation
supplies the baseline and restricted supplies the pricing model clears.

Every number in the manuscript is computed by `src/quantum_of_solace/analysis.py`
from these modules on fixed problem instances and injected as a manuscript
token — none is hand-authored prose.

## Methodology — QUANTUM: the analytical models and algorithms that drive the mission

We implement six deterministic models, one per module of the pure domain core.
All are pure functions of fixed problem data; there is no random number
generation and no dependence on the wall clock, so a regeneration reproduces
identical output. The sections below follow the dependency order in which
`quantum_of_solace/analysis.py` composes them: hydrology and reservoir
operation first, then the concentration, pricing, interdiction and power models
that read from them.

### Desert hydrology (`quantum_of_solace/hydrology.py`)

An aquifer contributes a per-period yield and a potability quality; a route
carries flow with a capacity, a distance and an evaporation loss fraction.
Three algorithms operate on the resulting network:

* **Mass balance** — for each node, inflow is delivered net of evaporation and
 outflow is subtracted, giving a per-node surplus.
* **Shortest-effort routing** — Dijkstra over the *effective* delivered unit
 cost ``cost_per_unit / (1 - evaporation)``, so evaporative routes are
 penalised, plus the compound delivered fraction.
* **Maximum flow** — Edmonds–Karp with a residual graph and reverse edges, so
 already-assigned flow can be re-routed. This yields the most water a
 settlement can receive per period under the route capacities.
* **Delivery capacity** —:func:`delivery_capacity` solves a *single*
 whole-network flow with a super-source feeding each aquifer an edge capped at
 that aquifer's yield and every settlement draining to a super-sink. The
 aquifer yields therefore bind, and the result cannot exceed
:func:`total_supply`. Summing independent per-source maximum flows would
 double-count shared yield and can report more water than the aquifers
 produce; the single-flow formulation is what rules that out.

Both flow figures are **routed** volume under capacity and yield constraints,
with evaporation *not* deducted. Maximising volume net of per-edge evaporation
is a generalised (lossy) flow problem whose optimum is not the capacity maximum
flow, and a maximum-flow assignment is not unique, so the evaporation implied by
"the" solution is not a property of the network. Evaporation is instead
quantified exactly by the mass balance and by the effective unit cost that
Dijkstra minimises. Routed volume bounds delivered volume from above, and this
manuscript claims no more than that.

### Water-rights cartel (`quantum_of_solace/water_cartel.py`)

A dam has storage capacity, initial storage, natural inflow, a downstream
demand, a maximum release and an evaporation rate. `run_reservoir` simulates
mass balance period by period; a *restriction fraction* withholds that share of
each period's otherwise-released water.

Leverage is defined so that it is dimensionally consistent. Inflow, maximum
release and downstream demand are all **per-period rates**, so a leverage ratio
must divide a horizon volume by a horizon volume:
:func:`horizon_demand_volume` returns `downstream_demand * periods`,
:func:`dam_leverage` divides a dam's withheld volume by it, and
:func:`cartel_leverage` divides the total withheld volume across the controlled
dams by the horizon demand of the whole fleet. Every leverage figure in this
manuscript is therefore a share in the unit interval, and it does not change if
the simulated horizon is lengthened at a steady release.

### Commodity-cartel graph (`quantum_of_solace/cartel_graph.py`)

A bipartite control graph maps actors to the share each holds of each
commodity. Concentration is the Herfindahl–Hirschman index in percentage
points, ``sum((share * 100)²)``, reported per commodity and aggregated as the
portfolio mean. Dominance, concentration ratios for the top-k holders, and an
actor's portfolio diversification complete the picture.

:func:`concentration_band` classifies an index value against the bands of the
U.S. Horizontal Merger Guidelines [@doj2010merger]: *unconcentrated* below
1500 points, *moderately concentrated* up to
2500 points, and *highly concentrated* above it. The
classification lives in code so the manuscript never has to assert which side
of a threshold a measurement falls on.

### Water scarcity pricing (`quantum_of_solace/pricing.py`)

On a linear inverse demand curve ``p(q) = a − b·q``,:func:`market_clearing_price`
is the scarcity price at which a fixed supply is absorbed, and
:func:`scarcity_impact` prices the cartel's supply cut: the restricted price,
the price-rise fraction, and the scarcity rent collected on the reduced volume.
The standard monopoly solution (MR = MC), with:func:`monopoly_price`,
:func:`monopoly_quantity` and:func:`deadweight_loss`, quantifies the social
cost of concentrated control.:func:`point_elasticity` returns the magnitude of
the point price elasticity, which on ``p = a − b·q`` is ``p/(b·q)`` — the
demand function is ``q(p) = (a − p)/b``, so ``dq/dp = −1/b``.

The baseline and restricted supplies in the assessment are computed from the
*real* dam fleet (unrestricted vs cartel-restricted reservoir release), so
pricing is measured from the same model, not assumed. They are dam releases, not
hydrology-network routed volume: the two subsystems are separate assets and the
manuscript keeps their units apart.

### Aqueduct interdiction (`quantum_of_solace/resilience.py`)

Over the hydrology network,:func:`single_route_criticality` ranks every route
by the delivery lost if it alone is cut (recomputing maximum flow after each
removal);:func:`interdiction_sequence` drives a greedy worst-case attack that
repeatedly removes the most critical remaining route; and
:func:`resilience_index` reports the **mean** fraction of delivery retained
after a single cut. The mean is not a worst-case bound, so the assessment also
reports ``worst_case_retention`` — the minimum of the same set — and the two are
carried into the manuscript as separate tokens so neither can stand in for the
other.:func:`minimum_cut` finds the least-capacity set of routes
separating supply from a settlement via the residual reachability of the
Edmonds–Karp solution, whose value equals the maximum flow by the
max-flow/min-cut theorem.

### Cooperative power (`quantum_of_solace/shapley.py`)

Multi-resource control is cast as a transferable-utility coalition game with a
diminishing-returns value function ``v(S) = Σ_c w_c·√(Σ_{a∈S} share)`` and
solved **exactly** by full enumeration::func:`shapley_value` (efficiency always
holds: the values sum to the grand-coalition value),:func:`banzhaf_power`
(normalised continuous Banzhaf–Coleman index),:func:`power_ranking`, and
:func:`dominance_gap` between the top two actors.

### The mission adapter

`quantum_of_solace/mission.py` adapts the six models to the frozen `bond_api`
protocol: `brief`, `recon`, `plan`, `execute` and `debrief`, with provenance
carrying a canonical SHA-256 input hash and the fixed seed 0
(the film's models make no random draws at all). The adapter also registers the
six assessment entry points, plus the composed full assessment, in a
module-level `GadgetRegistry` under the package slug, which is how the
coordinator and CLI reach them across packages. The domain modules import
nothing from `bond_api`, so they remain standalone.

## Results — QUANTUM: measured outcomes, headline numbers, and what they establish

All results below are computed by `quantum_of_solace/analysis.py` on the fixed
canonical problem instances and injected from `docs/manuscript/config.yaml` + the
assessment — they are measured, not authored.

### 1. Desert water network resilience

The canonical network holds 80.0 units/period of aquifer
yield across 5 nodes and 6 routes —
3 aquifers feeding 2 settlements
(border_town, valley_compact). A single whole-network Edmonds–Karp maximum flow,
bounded by the aquifer yields as well as the route capacities, routes
80.0 units/period into the settlements; the yields, not
the pipes, are the binding constraint.

Directed at one settlement alone, the network can push 65.0
units/period to border_town or 55.0 to valley_compact.
These two figures are **alternatives, not addends**: the settlements draw on the
same aquifers, so their sum exceeds what the network can route in total and must
never be added. The delivery figure plots them side by side for that reason, against
the network-wide bound.

Both figures are *routed* volume under capacity and yield constraints, not
volume net of evaporation. Maximising volume after per-edge evaporation is a
generalised (lossy) flow problem whose optimum differs from the capacity
maximum flow, and a maximum-flow assignment is not unique, so the evaporation
implied by "the" solution is not a property of the network. Evaporation is
therefore accounted separately and exactly — in the per-node mass balance and in
the effective unit cost that shortest-effort routing minimises. Routed volume is
an upper bound on delivered volume, and this manuscript does not claim otherwise.

![Settlement delivery under maximum flow](output/figures/quantum_of_solace_hydrology_settlement_delivery.png)

### 2. Cartel leverage over water rights

With a 50% restriction on the
2 dams it controls out of a fleet of
3, the cartel achieves an aggregate leverage of
**0.256** over the 12-period horizon: it
withholds 858.8 units against a horizon demand of
3360.0, or 25.6% of everything the
fleet was there to serve. Both sides of that ratio are horizon volumes, so the
figure is a genuine share and does not inflate with the length of the
simulation.

That leverage is *smaller* than the holding that produces it, and the
measurement says so plainly: the cartel holds 66.7% of the
fleet by dam count and converts it into 25.6% of horizon
demand withheld, a leverage-to-ownership ratio of
0.38. Two mechanics account for the shortfall:
the cartel withholds only 50% of each controlled dam's
release rather than all of it, and the uncontrolled dam keeps releasing at full
rate into the same horizon demand. The interesting quantity here is the ratio
itself, not a direction assumed in advance — the model is free to return a value
above 1, and on this fleet it does not. The leverage figure reports leverage per dam;
controlled dams are red.

![Cartel leverage by dam](output/figures/quantum_of_solace_water_cartel_leverage.png)

### 3. Multi-resource commodity control

Across copper, grain, lithium, water, control is concentrated: water HHI
3550.0 and lithium HHI 4150.0 both sit well above
the 2500-point line above which the U.S. Horizontal Merger
Guidelines [@doj2010merger] call a market *highly concentrated*. The
portfolio-mean HHI is **3925.0** points, which
`concentration_band` classifies as highly concentrated. The hhi figure plots
concentration per commodity, and
the dominance map shows the shadow cartel holding the largest share of water
and lithium while a rival syndicate and a state utility split copper and grain.

![Herfindahl–Hirschman concentration by commodity](output/figures/quantum_of_solace_cartel_hhi_concentration.png)

### 4. Water scarcity pricing

The cartel's leveraged control has a price consequence, and this model measures
it rather than assuming its sign. This section prices
the **dam fleet's** mean per-period release, not the hydrology network's routed
volume — the two models describe different assets and their units are not
interchangeable (§1 reports the network at 80.0
units/period). Cutting that release from 214.1 to
142.5 units/period drives the water price from
**46.5** to **64.4** — a 38.5% rise.
Demand is inelastic at that baseline (point elasticity 0.869,
below the unit-elastic value of 1), so the proportional price rise exceeds the
proportional volume cut — by the reciprocal of the elasticity, not by an
unbounded multiple. The cartel collects a scarcity rent of
**2549.6** on the reduced volume — the price premium times the
volume still sold.

That rent is not a rise in takings, and the assessment measures the difference
rather than gesturing at it. Revenue on this demand curve peaks at
200.0 units, and the cut runs from
214.1 straight past that peak down to
142.5, so gross revenue falls from
9950.5 to 9173.4. Inelastic demand
makes a *marginal* withholding lucrative; a cut this deep overshoots. The
coercive value of the squeeze here is the price shock imposed on buyers, not a
larger cheque for the seller. Even without withholding, the
underlying market is already monopolistic: the monopoly price would be
55.0 on 180.0 units, imposing a deadweight loss of
**4050.0** versus the competitive outcome. The pricing figure shows the demand
curve with the baseline, restricted and monopoly prices.

![Water scarcity pricing under cartel restriction](output/figures/quantum_of_solace_water_pricing_curve.png)

### 5. Aqueduct interdiction and resilience

Of the 6 routes, 4 are critical —
cutting any one of them lowers routed volume — while 2
are redundant, their capacity re-routable through the rest of the network. Two
retention figures follow, and they are not interchangeable: the **mean**
fraction retained across all single cuts is **0.917**, whereas the
worst single cut retains 0.750. Only the second is a
worst-case bound; the mean is quoted here as a mean and nowhere else as a
guarantee. The most critical single route, highland_aquifer->border_town, costs
20.0 units (25.0%) of the
80.0-unit baseline if lost. The interdict figure shows the greedy
worst-case interdiction sequence: 3 well-chosen cuts remove
45.0 units, 56.2% of baseline delivery,
leaving 35.0 units still flowing — a heavy loss, but not
a total collapse.

![Greedy worst-case aqueduct interdiction](output/figures/quantum_of_solace_resilience_route_criticality.png)

### 6. Cooperative power over the portfolio

The headline HHI of 3925.0 points is concentration; the *power* to
capture the commodity portfolio's value is resolved exactly by the Shapley
value. With a grand-coalition portfolio value of 7.0, the leading
actor **quantum** commands 2.624, ahead of the rival
(2.290) and the state utility (2.086) — a dominance gap
of 0.334 — and quantum's normalised Banzhaf power is
0.378. The shapley figure plots the per-actor Shapley values,
with the dominant actor highlighted.

![Cooperative power over the commodity portfolio](output/figures/quantum_of_solace_cartel_shapley_power.png)

## Conclusion — QUANTUM: findings, verdict, and what the mission establishes

**Quantum of Solace: QUANTUM — Special-Agent Mission Software** demonstrates how a seemingly non-violent lever — control
of water and scarce commodities — produces coercive power, and how deterministic
algorithms make that power measurable. The package ships a pure,
infrastructure-free domain core (hydrology, water cartel, commodity-cartel
graph, scarcity pricing, aqueduct interdiction, and cooperative power) both for
direct use and as the substrate of a `bond_api` mission provider, so the BOND
orchestrator can discover and drive *Quantum of Solace* exactly like any other
film.

The headline result is that leverage is *systemic and convertible*: a cartel
holding 2 of 3 dams
(66.7% of the fleet) and a lead in high-value commodities
exerts simultaneous influence over downstream demand
(25.6% of the fleet's horizon demand withheld), over
market concentration (a highly concentrated portfolio at 3925.0
points), over price (a 38.5% scarcity-price rise and a scarcity rent
of 2549.6, though gross revenue falls from
9950.5 to 9173.4 because the cut
overshoots the revenue peak), and over the network
(4 of 6 routes critical, mean
single-cut retention 0.917, worst-case retention
0.750). Its Shapley share of the commodity portfolio's
value, 2.624 of 7.0, confirms that power
concentrates in the leading actor.

What the measurements do *not* show is a leverage multiplier. On this fleet the
holding converts at a ratio of 0.38 —
66.7% of the dams yields 25.6% of
horizon demand withheld, so the converted share is *below* the ownership share,
not above it. The coercive power documented here is breadth — demand,
concentration, price and network yielding at once — rather than amplification
within any one channel. Within the portfolio the leading actor's exact Shapley
value does exceed the runner-up's, by 0.334. The methods — mass
balance, Dijkstra, Edmonds–Karp, reservoir simulation, the Herfindahl–Hirschman
index with its published concentration bands, linear-demand monopoly economics,
greedy network interdiction, and exact Shapley and Banzhaf indices — are all
standard, all real, and all reproduced deterministically. No metric in this
manuscript is hand-authored; a test fails if one appears.

## Experimental Setup — QUANTUM: canonical scenarios, parameters, and configuration

This package is a BOND-suite film repository with a `src/` layout, a local-only
git working tree, and a line-and-branch coverage floor enforced on `src/` by
the package's own pytest gate.

### Software environment

* Python 3.14 (the project pins `requires-python >= 3.10`)
* `numpy`, `matplotlib`, `pyyaml` as runtime dependencies
* `bond-api` (the frozen protocol) as a path dependency
* `pytest`, `pytest-cov`, `mypy`, `ruff` as dev dependencies

Lint and format settings are declared in this package's own `pyproject.toml`,
so a standalone clone lints identically to the in-suite checkout.

### Problem instances

All models run on fixed, deterministic instances built by each module's
`default_*` factory. Every parameter quoted below is a manuscript token read
back out of the running assessment, not a number transcribed into prose:

* `default_network` — 3 aquifers
 (80.0 units/period total) routing to
 2 settlements (border_town, valley_compact) over
 6 evaporative routes, 5 nodes in all.
* `default_dams` — 3 reservoirs with per-period downstream
 demands; the cartel controls 2 of them at a
 50% restriction over 12 periods,
 giving a horizon demand base of 3360.0 units.
* `default_cartel` — 3 actors (quantum, rival_syndicate, state_utility)
 controlling copper, grain, lithium, water with known shares; the shadow cartel leads
 water and lithium.
* `default_demand` — a linear inverse demand curve with intercept
 `a = 100` and slope `b = 0.25`, at a constant
 marginal delivery cost of 10. Baseline and restricted
 supply are *measured* from the dam-fleet simulation
 (214.1 → 142.5 units/period), not
 assumed.
* `default_weights` — canonical Shapley commodity weights
 (copper 1, grain 1, lithium 2, water 3) over the diminishing-returns control value function.
* `INTERDICTION_STEPS` — 3 cuts in the canonical greedy
 worst-case interdiction sequence.

### Determinism

Result tokens are computed by `run_quantum_assessment` and injected into the
manuscript. The mission seed is 0 and no model draws a random
number, so seeding is a formality rather than a control. The generation
timestamp is 2026-08-04, taken from the config date rather than
the wall clock, so hydration is reproducible. The exact-enumeration Shapley and
Banzhaf solvers evaluate all `2^n` coalitions rather than sampling, so power
indices carry no estimation error. Migration between Python versions leaves
every numeric result unchanged.

## Reproducibility — QUANTUM: verification gates, deterministic regeneration, and artifacts

### Provenance

Every `MissionOutcome` from `quantum_of_solace/mission.py` carries a
`Provenance` record: package version, the fixed seed 0 (the film
uses no randomness), and a canonical SHA-256 input hash of the full assessment,
taken over a key-sorted JSON serialisation so the digest does not depend on
dictionary ordering. The same input always reproduces the same hash and the
same results.

### Regeneration pipeline

The canonical artifacts are disposable and regenerated deterministically:

```bash
uv run python scripts/generate_analysis.py # assessment JSON + figures
uv run python scripts/z_generate_manuscript_variables.py # hydrate tokens
uv run python scripts/run_mission.py full # end-to-end mission
```

`output/` is git-ignored; a clean regeneration leaves the tracked tree stable.
The verification gate is:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/ tests/ && uv run ruff format --check src/ scripts/ tests/
uv run mypy src/ scripts/
```

The suite is real-computation only: no mock framework appears anywhere in
`tests/`, so a passing assertion means the algorithm produced the right number
rather than that a call signature was intercepted.

### Manuscript–code binding

Two live tests keep this document honest. One re-derives the token map by
calling `generate_variables` and fails if any token used in a numbered
section is not produced, binding prose to the generator rather than to a
possibly stale artifact under `output/`; it also asserts the scanned section
set is non-empty, so an empty scan fails instead of passing vacuously. The
other scans the results section for bare decimal numerals after the tokens are
masked out, so a hand-authored metric that escapes the injection pipeline is
caught at test time.

### Configuration hash

The manuscript identity (title, subtitle, version, date) is authored once in
`docs/manuscript/config.yaml` (0.1.0, dated 2026-08-04) and injected
via `quantum_of_solace/manuscript_variables.py`, never duplicated in prose.
Keywords: water-rights cartel, desert hydrology, commodity-cartel graph, herfindahl-hirschman concentration, maximum flow, reservoir leverage, water scarcity pricing, network interdiction, shapley value, deterministic mission software. Actors modelled: quantum, rival_syndicate, state_utility.

## Scope and Related Work — QUANTUM: boundaries, positioning, and relationship to the literature

### Scope

This package models the specific threat of *Quantum of Solace*: leverage over
scarce water and commodities exerted by a controlling cartel. The models are
intentionally small, deterministic, and auditable so every claim can be traced
to a computed number.

It deliberately does **not** attempt any of the following, and no result here
should be read as if it did:

* a general integrated assessment model, or a hydrologic–hydraulic engineering
 simulator — routes carry a capacity and a loss fraction, not a hydraulic
 head, a channel geometry, or a groundwater response;
* stochastic hydrology — inflows are fixed rates, so nothing here estimates a
 drought return period or a reservoir reliability;
* an econometric demand study — the demand curve is a stylised linear
 instrument for reasoning about scarcity rent, not a fitted model of any real
 water market, though the inelastic behaviour it produces at the assessed
 baseline (elasticity magnitude below 1) matches the direction reported in the
 empirical meta-analysis literature [@espey1997price];
* strategic interaction between the actors — the power indices allocate the
 value of a cooperative game and do not model entry, deterrence, or
 retaliation.

### Related work

The algorithms are classical and well-established; the citations below point at
the specific source for each.

* **Network flow** — Edmonds–Karp maximum flow [@edmonds1972theoretical],
 building on Ford & Fulkerson [@ford1956maximal]; shortest-path routing
 follows Dijkstra [@dijkstra1959note]. The minimum cut is read off the
 residual graph via the max-flow/min-cut theorem [@ford1956maximal].
* **Network interdiction** — ranking arcs by the flow lost when they are
 removed, and attacking greedily in that order, is the deterministic
 network-interdiction problem in Wood's formulation [@wood1993deterministic].
 This package solves the greedy heuristic, not the exact interdiction optimum.
* **Market concentration** — the Herfindahl–Hirschman index derives from
 Hirschman [@hirschman1945national] and Herfindahl
 [@herfindahl1950concentration]; the concentration bands used to classify a
 measured index come from the U.S. Horizontal Merger Guidelines
 [@doj2010merger].
* **Prices** — linear-demand monopoly pricing (MR = MC) and deadweight-loss
 analysis are textbook microeconomics; the empirical inelasticity of
 residential water demand is documented by Espey, Espey & Shaw
 [@espey1997price]. Inelasticity means a volume cut moves price more than
 proportionally; whether a *particular* cut raises the seller's revenue
 depends on which side of the revenue peak it lands, which this package
 measures rather than assumes.
* **Cooperative power** — the Shapley value [@shapley1953value] and the Banzhaf
 index [@banzhaf1965weighted], whose continuous and normalised forms are
 characterised by Dubey & Shapley [@dubey1979mathematical]. Both are computed
 here by exact enumeration rather than by sampling.
* **Reservoir operation** — period mass-balance reservoir simulation under a
 release rule is the standard formulation in water-resource systems analysis
 [@loucks2017water].

The novelty is not the mathematics but its application: encoding a film's
strategic threat as executable, reproducible mission software bound to a frozen
protocol, and coupling six otherwise-independent models into one measured
assessment in which the hydrology network's delivered flows feed the
interdiction analysis and the reservoir simulation feeds the price model.

## Sources — QUANTUM: bibliography

@dijkstra1959note; @edmonds1972theoretical; @hirschman1945national; @shapley1953value; @banzhaf1965weighted; @ford1956maximal; @herfindahl1950concentration; @doj2010merger; @dubey1979mathematical; @wood1993deterministic; @espey1997price; @loucks2017water


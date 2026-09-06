# Skyfall (2012) — SKYFALL

*film package · package codename SKYFALL*. Mission **SILVA**: model the network intrusion paths into MI6's headquarters; detect the agent-list exfiltration burst in HQ traffic; compute the minimum severance cut that stops exfiltration; audit the aging legacy system exposure; schedule legacy patching under a daily budget; plan the Skyfall estate defense from its choke points.

## Concepts — SKYFALL: domain and operational focus

cyber operations, legacy systems

## Abstract — SKYFALL: mission summary

Skyfall is a PROJECT BOND mission-software package (film: Skyfall, 2012; codename **SILVA**) that models six linked threat surfaces through a purely deterministic computational core, grouped into three mission layers. The **cyber layer** models the intrusion paths an adversary can take into MI6's headquarters network, enumerating all simple routes and the minimum-hop / minimum-difficulty routes into the deepest system; it detects the agent-list exfiltration burst in HQ traffic with a periodic-baseline CUSUM change-point detector; and it computes the minimum severance cut (max-flow / min-cut) that stops the exfiltration. The **legacy layer** audits the aging infrastructure that still underpins operations, computing a closed-form exposure score per system from four normalized risk factors, an aggregate fleet risk, and a greedy patch schedule that minimizes cumulative exposure under a daily patching budget. The **physical-defense layer** computes Silva's island hideout topology by flood fill and the Skyfall estate's articulation (choke) points by Tarjan's algorithm, then plans a defender assignment that covers them. All results are reproducible: fixed inputs, no random draws, and no wall-clock in any persisted metric. The package implements the frozen BOND-API ``MissionProvider`` contract and registers its gadgets with the BOND gadget registry, making the SILVA mission discoverable by the suite's orchestrator. ## Concurrency of the six threats The mission treats the cyber intrusion (internet → registry, 6 simple paths), the exfiltration burst (detected at hour 180, window 180–190), the severance cut (max flow 8.0), the legacy-system exposure (fleet size 5, mean exposure 0.62), the patch back-log (12 vulnerabilities, cut by 89%), and the estate's choke-point defense (3 choke points, coverage 1.00) as one coordinated assault — the way the film depicts a single adversary reaching MI6's most sensitive systems through a chain of aging, poorly-segmented connections.

## Introduction — SKYFALL: mission framing, the operational problem, and how to read this chapter

### The SILVA threat

Skyfall (2012) dramatizes a coordinated external assault on MI6: a single
adversary — Silva — reaches the Service's deepest and most sensitive systems
through a chain of aging, poorly-segmented connections, exfiltrates the NATO
agent list, and ultimately forces the confrontation onto home ground at the
Skyfall estate. This package turns that story into six well-posed
computational problems, each with a real deterministic algorithm and real data:

1. **Network intrusion paths** (`skyfall.cyber_ops`) — model the MI6 HQ
 network as a directed graph and ask: by which routes can an adversary reach
 the high-value target, and which is shortest / cheapest?
2. **Traffic change-point detection** (`skyfall.traffic_analysis`) — estimate
 a periodic (hour-of-day) baseline, residualize it, and run a CUSUM control
 chart to catch the exfiltration burst.
3. **Exfiltration severance** (`skyfall.exfiltration`) — treat the outward
 data transfer as a capacitated flow and compute the max-flow and the
 minimum cut (the smallest link set that must be severed).
4. **Legacy-system exposure audit** (`skyfall.legacy_audit`) — quantify how
 aging infrastructure's age, missing patches, obsolete protocols, and open
 services combine into a scalar exposure.
5. **Patch scheduling** (`skyfall.patch_strategy`) — schedule a finite daily
 patching budget to minimize cumulative fleet exposure over a horizon.
6. **Island topology + estate defense** (`skyfall.estate_defense`) — compute
 the reachable topology of Silva's island hideout and the articulation
 (choke) points of the Skyfall estate, then assign a limited defending team.

### Design principles

The package follows the PROJECT BOND guardrails: the pure domain modules are
infrastructure-free and importable without the BOND protocol; `mission.py` is
a thin adapter to the frozen `bond_api` contract; scripts are thin
orchestrators; tests are real-computation and zero-mock, held above a hard
coverage floor rather than to a quoted percentage.

Every number reported in this manuscript is injected from
`skyfall.manuscript_variables.generate_variables` — never hand-authored —
and that rule is enforced in both directions by the suite: no token may go
unresolved, and no bare numeral may appear in the results narrative. Section 6
describes the gates.

Where a scenario could pass while the underlying algorithm was wrong, the
package prefers a test that enumerates a family over a test that checks the
canonical case; Section 4 records the two defects that discipline caught.

## Methodology — SKYFALL: the analytical models and algorithms that drive the mission

### Network intrusion model (`skyfall.cyber_ops`)

The MI6 HQ network is a directed graph `G = (V, E)` of `9`
nodes (hosts and routing segments). An adversary enters at `internet`
and seeks the high-value target `registry`. Three reachability
questions are answered deterministically:

* **Simple-path enumeration** — a depth-first search over the directed graph
 enumerates every simple path from entry to target, bounding search by never
 revisiting a node. There are `6` such paths.
* **Minimum-hop path** — breadth-first search from the entry returns a
 shortest path (5 hops).
* **Minimum-difficulty path** — Dijkstra's algorithm over per-edge traversal
 costs (5 hops) finds the route that is least costly in
 aggregate, which need not be the shortest.

Each node carries an exposure in `[0, 1]`; the probability an intrusion
traverses a path uncontained is the product over hops of
`base_survival × (1 − exposure(dest))`, with a baseline survival of
0.8 per hop. A step simulation walks the chosen path
hop-by-hop and reports whether it exceeds the containment budget of
6 hops.

### Traffic change-point detection (`skyfall.traffic_analysis`)

HQ traffic follows a daily rhythm, so a naive CUSUM on the raw series
false-alarms on the rhythm itself. Over a 240-hour
series, the detector first estimates a per-phase baseline:math:`\bar{x}_h`
across a period of 24 hours, fitted on the clean
pre-incident window of the leading 168 hours. It
subtracts that baseline to leave a zero-mean residual series, then runs the
two-sided CUSUM control chart of Page (1954):

:math:`S_t^+ = \max(0, S_{t-1}^+ + z_t - k), \quad S_t^- = \max(0, S_{t-1}^- - z_t - k)`

with:math:`z_t` the standardized residual, the allowance
:math:`k = 0.5`, and the decision interval
:math:`h = 5.0`. An alarm fires the first time either side
exceeds:math:`h`. The burst (180–190) is detected at hour
180, with a peak accumulation of 1281.8
standardized units.:func:`change_point_likelihood` additionally locates the
most likely single change point by maximizing the two-segment normal
likelihood split (hour 180).

### Exfiltration severance (`skyfall.exfiltration`)

The outward transfer of the agent list is a capacitated flow problem on a
8-node projection of the HQ network.:func:`edmonds_karp`
computes the maximum exfiltration rate from the registry (source) to the
internet (sink) via BFS augmenting paths, pushing each path's exact
bottleneck.:func:`min_cut_edges` then finds the minimum cut separating source
from sink — the smallest link set that must be severed.

Residual reachability is walked over the **residual** graph, which includes the
reverse arcs induced by pushed flow, not merely the original forward edges.
That distinction is load-bearing rather than pedantic: a forward-only walk
under-approximates the source side of the cut whenever flow enters that side
from an unreached node, and the reported cut then exceeds the max flow,
breaking the very theorem the routine relies on. With the residual walk, the
cut value equals the max flow (both 8.0) on every network, and
the property is pinned by an enumerated sweep rather than by the canonical
scenario alone. The severance plan is sever dmz_mail -> demarc, sever intranet_hub -> vpn_gateway.

The flow network's topology is not hand-copied from the intrusion network:
it is *derived* by:func:`exfiltration.cyber_flow_topology`, which reverses
each intrusion edge (data leaves outward) and drops the dead-end
`field_terminal` leaf. It has 8 nodes and
9 directed edges, and because it is constructed from
the intrusion graph, a change to one topology can no longer silently leave
the other stale.

### Legacy exposure model (`skyfall.legacy_audit`)

Each legacy system contributes four normalized risk factors — age
(`min(age/age_scale, 1)`), unpatched share (`1 − patch_level`), protocol
vintage (`min(era/era_scale, 1)`), and open-service surface
(`min(services/service_scale, 1)`), saturating at
25 / 3 / 6 respectively — combined linearly with weights
0.25 / 0.35 / 0.20 / 0.20 (age / unpatched / protocol / surface) into a
scalar exposure in `[0, 1]`. The factor model is defined once, in
:func:`risk_factors`, and consumed by both the score and the remediation
ranker so the two cannot disagree.

A fleet audit aggregates mean/max exposure, counts risk tiers, and returns an
overall fleet-risk label. Remediation is a deterministic greedy descent: each
pass patches the system whose dominant weighted risk factor offers the largest
exposure reduction — ties broken by the whole system id, so the ranking does
not depend on fleet insertion order — under a fixed budget of
3 actions (targets:
registry_arch, field_ops, ldap).

### Patch scheduling (`skyfall.patch_strategy`)

The maintenance layer schedules the 12 known
vulnerabilities under a daily budget of 1 patch over a
30-day horizon. A deterministic greedy scheduler spends
each day's budget on the already-discovered, highest-severity unpatched
vulnerabilities (ties broken by id), and cumulative exposure is the
severity-days accrued until each patch lands. Against a no-patching baseline
of 2377.5 severity-days, the schedule reduces exposure to
263.8 — a 89% reduction.

Real maintenance windows amortize, so the package also provides
:func:`patch_strategy.schedule_patches_coupled`: the second and later patch on
an already-open system costs a fraction (0.50×) of its
base effort, modelling the reality that re-patching a box you have already
touched is cheaper than opening it for the first time. Re-scheduling the same
backlog with that discount patches all 12
vulnerabilities at a scheduled exposure of 162.1
severity-days — a 93% reduction versus the
baseline — because couples on the same system close together instead of
claiming separate maintenance slots.

### Estate defense model (`skyfall.estate_defense`)

The Skyfall estate approach is an undirected graph of
7 positions connected by roads/trails. The
undirected invariant is enforced at construction — a one-sided road would make
Tarjan's search report a plausible but wrong choke-point set rather than an
error, which is the worst possible failure mode for a defensive plan.

**Articulation points** (cut vertices) — found with an iterative Tarjan DFS —
are positions whose removal disconnects the graph: the estate's **choke
points**, through which every route from the moors to the mansion must pass.
There are `3` choke points (field, mansion, roadgate).
A defense plan assigns the finite defending team (`4`
defenders) to the highest-degree choke points first, reporting any that remain
uncovered (3 posted, coverage 1.00).

Degree is not the only answer to "which choke point matters most".
:func:`estate_defense.betweenness_centrality` computes each position's share
of all shortest-path traffic, which correctly elevates a low-degree bridge
that every route is forced across. On the canonical estate the two priority
orders agree (yes) — `field`
ranks first by both measures — but on a path-shaped approach they diverge, a
distinction the defence tests pin. Both rankings are provided; ``"degree"``
remains the default.

Silva's island hideout is a passable cell grid with a single beachhead; a
flood fill computes the reachable area (11 cells), the
perimeter (20), and the farthest reachable cell — the
hideout — whose BFS distance (8 cells) is the
contested approach corridor.

## Results — SKYFALL: measured outcomes, headline numbers, and what they establish

### Intrusion reachability

The adversary enters at `internet` and works toward `registry`
across a 9-node network, reaching it by
6 distinct simple paths. The minimum-hop route is
5 hops (`internet → demarc → dmz_mail → intranet_hub → ops_db → registry`); the
minimum-difficulty route is 5 hops
(`internet → demarc → dmz_mail → intranet_hub → ops_db → registry`). Traversing the minimum-hop route uncontained has
probability 0.0578 under the per-hop survival model.

The legacy directory (`legacy_ldap`, the intrusion network's most exposed host) sits
on some simple intrusion paths but on neither the minimum-hop nor the
minimum-difficulty route: `legacy_ldap` appears on the cheapest path —
**no**. The high traversal difficulty assigned to
that hop is what keeps it off the optimum, so the pivot an adversary would
*prefer* for its exposure is not the pivot the cost model *selects*. Both
directions of that claim are pinned by tests rather than asserted in prose.

### Traffic detection and severance

The HQ traffic detector residualizes the daily rhythm over the
240-hour series and runs a CUSUM chart; the agent-list
exfiltration burst (window 180–190) is
**yes** — the alarm fires at hour 180,
the first hour of the burst window, with a peak accumulation of
1281.8 standardized units against a decision interval of
5.0. The independently-computed maximum-likelihood change point
agrees at hour 180.

Containment is a min-cut problem: the maximum exfiltration rate from the
registry to the internet is 8.0, and the minimum severance cut
of equal value (8.0) is `sever dmz_mail -> demarc, sever intranet_hub -> vpn_gateway`. Severing
exactly those links stops the exfiltration. The equality is not a property of
this scenario alone: an enumerated sweep over a family of five-node networks —
including ones whose maximum flow requires reverse residual arcs — confirms
`value(cut) == value(flow)` on every member. The flow projection's topology is
derived from the intrusion network (9 directed edges
across 8 nodes), so the two views of the same network
cannot drift.

![MI6 HQ traffic detection — residual series with CUSUM alarm](output/figures/skyfall_traffic_detection.png)

### Fleet exposure and patch schedule

The audited legacy fleet of 5 systems has mean exposure
0.62 and maximum exposure 0.80, with
1 critical systems, yielding an overall fleet risk of
**critical**.

Scheduling the 12 known vulnerabilities under a
daily budget of 1 patch over 30 days
patches all 12, cutting cumulative exposure from a
no-patching baseline of 2377.5 severity-days to
263.8 — a 89% reduction.

Amortizing maintenance windows — charging 0.50× effort
for every patch after the first on an already-open system — closes the same
backlog at 162.1 severity-days, a
93% reduction (all
12 patched). The saving comes from consolidating two
flaws on one box onto a single maintenance slot, which the uncoupled
scheduler could not.

### Estate defense

Of the estate's 7 positions,
3 are choke points (field, mansion, roadgate). Deploying
the 4-agent team across them posts
3 defenders and yields a defensive coverage of
1.00 — the team has slack, so no choke point goes unheld. Silva's
island hideout admits 11 reachable cells behind a
perimeter of 20; its contested approach corridor is
8 cells long, terminating at the hideout cell
(2,6).

Ranking the 3 choke points by betweenness centrality —
the share of all shortest-path traffic through each position — agrees with the
degree ranking on this estate (yes), with
`field` carrying the most traffic. The two priority
orders diverge in general (a path-shaped approach is the counterexample), and
the package provides both.

The flagship figure (the estate defense figure) maps the estate approach graph,
highlights the choke points, and annotates the assigned defender at each
covered position.

![Skyfall estate choke-point defense plan](output/figures/skyfall_estate_defense.png)

Both figures are rendered deterministically to `output/figures/` by
`skyfall.figures`.

## Conclusion — SKYFALL: findings, verdict, and what the mission establishes

The SILVA package demonstrates that a film's threat narrative can be
operationalized as deterministic, testable mission software. The cyber layer
quantifies exactly how an adversary reaches MI6's deepest systems, detects the
agent-list exfiltration burst with a residualized CUSUM chart, and identifies
the exact minimum severance cut. The legacy layer turns aging-infrastructure
sentiment into a closed-form exposure score, an aggregate fleet risk, and a
budgeted patch schedule that removes most of the backlog exposure. The estate
layer reduces physical defense to a graph-articulation problem with a provable
choke-point coverage plan.

The real value is the discipline the package enforces: pure domain modules,
deterministic provenance, live manuscript-variable injection, and zero-mock
tests held above a hard coverage floor. The mission provider is discoverable by
the BOND suite and its gadgets are registered for orchestration.

That discipline is not decorative. Two of this package's guarantees only became
true because a test was written to break them first. The max-flow min-cut
routine passed on the canonical acyclic scenario while computing residual
reachability incorrectly; only an enumerated sweep over networks that *need*
reverse residual arcs exposed the gap between what the docstring claimed and
what the code did. The remediation ranker's documented lexicographic
tie-breaking compared only the first character of a system id, so the ordering
silently depended on fleet insertion order. Neither defect was visible from the
mission outcome, both were visible from a test designed to fail. A scenario
that always passes measures the scenario, not the algorithm — the standing
lesson this package records for the rest of the fleet.

## Software and Scenario

### Package identity

- **Package**: skyfall (Skyfall: SILVA — Special-Agent Mission Software)
- **Codename**: SILVA
- **Package version**: 0.1.0 · mission version 0.1.0
- **Deterministic seed**: 11
- **Python**: 3.14.6 · build date 2026-08-04 (declared in
 `docs/manuscript/config.yaml`, not read from the clock)

### Scenario configuration

The scenario is fixed so results are reproducible. Every parameter below is a
named constant in `src/skyfall/`, surfaced here as an injected token rather
than transcribed by hand.

| Parameter | Value | Source constant |
| --- | --- | --- |
| Entry host | `internet` | `cyber_ops.DEFAULT_ENTRY` |
| Target | `registry` | `cyber_ops.DEFAULT_TARGET` |
| Network size | 9 nodes | `cyber_ops.DEFAULT_NETWORK` |
| Per-hop survival baseline | 0.8 | `cyber_ops.DEFAULT_BASE_SURVIVAL` |
| Containment budget | 6 hops | `cyber_ops.DEFAULT_CONTAINMENT_HOPS` |
| Traffic series | 240 hourly samples | `traffic_analysis.DEFAULT_TRAFFIC` |
| Baseline window / period | 168 / 24 hours | `traffic_analysis.DEFAULT_BASELINE_WINDOW`, `DEFAULT_PERIOD` |
| CUSUM allowance / interval | 0.5 / 5.0 | `traffic_analysis.DEFAULT_CUSUM_K`, `DEFAULT_CUSUM_H` |
| Exfiltration network | 8 nodes | `exfiltration.DEFAULT_FLOW_NETWORK` |
| Legacy fleet | 5 systems | `legacy_audit.default_legacy_fleet` |
| Exposure weights | 0.25 / 0.35 / 0.20 / 0.20 | `legacy_audit.EXPOSURE_WEIGHTS` |
| Exposure saturation scales | 25 / 3 / 6 | `legacy_audit.EXPOSURE_SCALES` |
| Remediation budget | 3 actions | `mission.REMEDIATION_BUDGET` |
| Patch horizon / daily budget | 30 days / 1 | `patch_strategy.DEFAULT_HORIZON_DAYS`, `DEFAULT_DAILY_BUDGET` |
| Estate | 7 positions | `estate_defense.DEFAULT_ESTATE` |
| Defending team | 4 call signs | `mission.DEFENDERS` |

### Running the mission

From the package directory:

```bash
uv sync --extra dev
uv run python scripts/run_mission.py all --json # full five-stage run
uv run python scripts/00_preflight.py skyfall # discovery/protocol check
uv run python scripts/z_generate_manuscript_variables.py # hydrate tokens + figure
uv run pytest tests/ --cov=src --cov-fail-under=90 # zero-mock gate
```

The pure domain modules (`skyfall.cyber_ops`, `skyfall.traffic_analysis`,
`skyfall.exfiltration`, `skyfall.legacy_audit`, `skyfall.patch_strategy`,
`skyfall.estate_defense`) import nothing from `bond_api` and remain usable in
isolation if the path dependency is ever unavailable; `skyfall.mission` is the
thin adapter to the frozen protocol.

## Reproducibility — SKYFALL: verification gates, deterministic regeneration, and artifacts

### Determinism guarantees

Every metric in this manuscript is deterministic by construction:

- **Fixed inputs**: the MI6 network, legacy fleet, estate graph, and island
 grid are hardcoded constants; nothing varies between runs.
- **No randomness**: the mission draws no random numbers; `11` is
 recorded solely in provenance.
- **No wall clock anywhere in the artifacts**: no generated value is read from
 the clock. The build stamp `SILVA_BUILD_DATE` (2026-08-04) is the
 committed `paper.date` field of `docs/manuscript/config.yaml`, so it changes only
 when someone edits and commits that file.

Because of the last point the guarantee is byte-level, not merely
value-level: running `scripts/z_generate_manuscript_variables.py` twice writes
byte-identical `output/manuscript/*.md`, `output/data/manuscript_variables.json`,
and `output/figures/*.png`. The one environment input is the interpreter —
`PYTHON_VERSION` is injected into the setup section, so the byte-identity claim
is scoped to repeated runs on a fixed Python version, and a different
interpreter changes exactly that one field.

### Verification gates

| Gate | Command | What it asserts |
| --- | --- | --- |
| Coverage floor | `uv run pytest tests/ --cov=src --cov-fail-under=90` | line + branch coverage on `src/` stays at or above the floor; zero failures, zero skips |
| Byte-identical regeneration | `tests/test_manuscript_variables.py::TestRegenerationIsByteIdentical` | two full runs of the generator script, with real time passing between them, write byte-identical artifact trees, and no artifact contains a wall-clock instant |
| No mocks | `rg -n 'MagicMock\|mocker\.patch\|unittest\.mock\|create_autospec' tests/` | no mock framework anywhere in the suite |
| Protocol purity | `tests/test_mission.py::TestPureCoreIsolation` | a fresh subprocess importing every domain module leaves `bond_api` out of `sys.modules` |
| Lint / types | `uv run ruff check src/ scripts/` · `uv run mypy src/` | style and type cleanliness on shipped code |
| Lineage | `rg -n "template[_]code_project".` | no exemplar strings outside docs that explain the lineage |

Rather than quoting a coverage percentage that would go stale the moment a line
moves, this section names the gate. The measured figure is whatever the command
above prints on the checkout you are holding; the guarantee is that it is not
below the floor, because the run fails otherwise.

### Manuscript-metric integrity

The manuscript's variable-token values are produced by
`skyfall.manuscript_variables.generate_variables` and enforced from both
directions:

- **Forward** — a live test asserts every injected token used in the numbered
 sections exists in the generated map, so a section can never render a raw
 brace.
- **Reverse** — a scanning test asserts the results, methodology, abstract, and
 conclusion contain no bare numerals outside tokens, inline code, and math.
 A hand-typed metric fails the suite. (Four-digit calendar years are exempt:
 a film release year is a literal, not a measurement, and no code change can
 make it drift.)

Together these mean a number in this manuscript is either injected from the
code that computed it, or the suite is red.

## Scope and Related Work — SKYFALL: boundaries, positioning, and relationship to the literature

### Scope

The SILVA mission deliberately covers six computational problems, across three
layers, that can be solved exactly and deterministically with classical graph,
statistical, and scheduling algorithms.

It explicitly does **not** attempt a full stochastic intrusion simulation, a
live penetration test, an adaptive (non-periodic) change-point detector beyond
the two-segment likelihood, or a physical simulation of the estate — those
would introduce nondeterminism that the package's reproducibility guarantee
forbids. The exposure and severity models are likewise transparent linear
scores, not calibrated empirical risk estimates: they are stated as a model,
scoped as a model, and never presented as measurements of real infrastructure.
The value is in clean problem formulation, exact algorithms, and honest
measurement.

The betweenness-ranked defense and the coupling-aware scheduler are deliberate
*modeling extensions*, provided and tested alongside their defaults rather
than replacing them: the canonical recorded figures stay fixed unless the
variant is invoked, so the manuscript's headline numbers are not disturbed by
the richer alternatives. Likewise the coupling discount
(0.50×) and the exposure/severity weights are model
parameters, not measurements of real infrastructure.

### Related work

The algorithms used here are textbook, and the security framings they serve are
established practice:

- **Simple-path enumeration for intrusion reachability** is the core of the
 attack-graph literature: enumerating the routes an adversary can take through
 a networked system, then reasoning over that set (Phillips & Swiler 1998;
 Sheyner et al. 2002).
- **BFS / Dijkstra reachability** (Dijkstra 1959; Cormen et al. 2009) supply
 the minimum-hop and minimum-difficulty routes, and **Edmonds–Karp max-flow
 with the max-flow min-cut theorem** (Edmonds & Karp 1972; Ford & Fulkerson
 1962) supplies the exfiltration severance.
- **Tarjan's articulation-point algorithm** (Tarjan 1972; Hopcroft & Tarjan
 1973; Even 2011) finds cut vertices — the choke points — and is standard in
 network-resilience and defensive-planning work. **Betweenness centrality**
 (Brandes 2001) ranks those choke points by the share of shortest-path
 traffic each carries, complementing degree when scarce defenders must be
 placed.
- **CUSUM change-point detection** (Page 1954; Montgomery 2012; Hawkins &
 Olwell 1998) underpins the traffic detector; the two-segment likelihood split
 is the single-change-point special case of the segmentation objective treated
 at scale by Killick et al. (2012).
- **Weighted multi-factor vulnerability scoring** follows the structure of
 CVSS-style composite metrics (Mell, Scarfone & Romanosky 2007), kept
 deliberately simpler and fully transparent here.
- **Patch scheduling under a finite budget** is a real operational tradeoff
 studied directly by Beattie et al. (2002); the greedy severity-first policy
 is standard priority scheduling (Pinedo 2016).

Where the film's narrative maps onto these tools, this package documents the
mapping so a reader can trace every metric to its algorithm.

## Sources — SKYFALL: bibliography

@cormen2009algorithms; @even2011graph; @page1954continuous; @edmonds1972theoretical; @ford1962flows; @pinedo2016scheduling; @hawkins1999cumulative; @tarjan1972dfs; @hopcroft1973algorithm447; @dijkstra1959note; @phillips1998graphbased; @sheyner2002attackgraphs; @mell2007cvss; @beattie2002timing; @killick2012changepoints; @montgomery2012spc; @brandes2001algorithm


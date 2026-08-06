# The Man with the Golden Gun (1974) — SOLEX

*film package · mission codename SOLEX*. Mission **SOLEX**: model solar concentration yield (mirror array to heat); track solar position and daily clear-sky insolation; solve the funhouse lair escape topology (rooms/mirrors as graph); analyse lair flow: edge-disjoint routes, min cut, cheapest escape; schedule the assassin duel/bounty appointment book; schedule unit-time deadline bounty contracts (max profit).

This chapter reproduces the package's complete manuscript verbatim:
the abstract and every authored section, token-hydrated from the
package's own manuscript variables, with the package's figures carried
in the combined PDF and its sources resolved against the unified
bibliography.

## Concepts

solar concentration, lair topology, assassin scheduling

## Abstract

**Mission codename: SOLEX** — Project BOND film dossier for *The Man with the Golden Gun* (1974). ## Abstract This dossier documents the deterministic mission software built for the SOLEX operation. 6 specialist capabilities support the field agent: 1. **Solar concentration yield** — a heliostat-field model that converts a mirror array's area and reflectivity into optical power and thermal heat output, and allocates a mirror-area budget to the highest-yield mirrors. 2. **Solar tracking & daily insolation** — the sun-geometry layer: declination, daylight window, and the Duffie–Beckman clear-sky daily energy the field concentrates. 3. **Funhouse lair escape topology** — a graph solver over the villain's mirror-lined funhouse, producing a shortest escape route and identifying the bottleneck rooms that guard the exit. 4. **Lair flow analysis** — max-flow / min-cut over the lair, returning the edge-disjoint escape routes and the minimum mirror walls that seal the lair, plus a cost-aware (Dijkstra) cheapest escape. 5. **Assassin duel / bounty scheduling** — an appointment book solved by weighted interval scheduling, selecting a non-overlapping set of bounty duels that maximises total reward and reporting every scheduling conflict. 6. **Deadline bounty scheduling** — unit-time bounty contracts scheduled by the deadline-greedy (union–find) algorithm to maximise accepted profit. All results are computed from real, deterministic domain models with fixed inputs and no wall-clock dependence; every metric in this manuscript flows from code, never from hand-authored prose. The canonical SOLEX field converts a 1000 W/m² irradiance into a thermal output of 191.6325 kW (concentration 50.10×) and, over a clear-sky solstice day at 8.0°N, concentrates 1441.7 kWh. The extended funhouse has 3 edge-disjoint escape routes (min cut 3 mirror walls), while the canonical lair is guarded by 3 bottleneck rooms — redundancy and criticality are separate measurements, and the lair's 4 articulation points are a third. On the duel book the two exact schedulers disagree: weighted interval scheduling realises a bounty of 13.0 where the count-maximising earliest-finish greedy realises 11.0. The deadline book yields a maximum profit of 18.0 across 5 contested contracts.

## Introduction

The Solex agitator concentrates sunlight from a field of tracking mirrors onto
a central receiver to produce the heat that powers the villain's island. A
field agent working against it needs answers to three concrete questions, and
each of them turns out to be a well-posed computational problem.

*How much heat can that array actually deliver?* This is a heliostat yield
question — aperture, reflectivity, and efficiency give the instantaneous
figure, and the sun's geometry over the day gives the energy figure. Both are
standard solar engineering [@duffie_beckman], and both are worth computing
rather than guessing, because the answer decides whether the installation is a
curiosity or a strategic asset.

*How does an agent get out of the mirror-lined funhouse — and how would the
enemy seal it?* This is a graph question with two distinct answers. The route
out is a shortest path; the rooms that *every* route must cross are the
bottlenecks, the single points of failure the defenders will garrison. Escape
redundancy is a flow question: the number of edge-disjoint routes is exactly
the entry–exit maximum flow, and the fewest mirror walls that seal the lair is
the matching minimum cut [@ford_fulkerson; @edmonds_karp].

*Which contracts should the assassin — or the agent tracking him — expect to be
taken?* This is scheduling, and the answer depends sharply on the objective.
Maximising the *number* of contracts is the earliest-finish greedy; maximising
their total *bounty* is weighted interval scheduling [@kleinberg_tardos], and
on a well-chosen book the two disagree. A separate deadline book, where each
contract occupies one slot and expires, is the unit-time deadline problem
solved exactly by a matroid greedy [@cormen].

This dossier presents the mission software for **SOLEX**:
6 pure, deterministic domain modules
(`solar_concentration.py, solar_tracking.py, lair_topology.py, lair_flows.py, duel_scheduler.py, deadline_scheduler.py`) adapted to the frozen PROJECT BOND
`MissionProvider` lifecycle — brief, recon, plan, execute, debrief
[@bond_protocol] — through a single thin adapter. The domain modules import
nothing outside the Python standard library and never import the protocol, so
the scientific core stands alone; the adapter is the only place the fleet
contract appears.

Determinism is a hard constraint rather than an aspiration: fixed inputs, no
random draws, sorted iteration in every graph traversal, and no wall-clock read
in any persisted artifact. Equally hard is the rule that no metric is typed by
hand — every number in [Results](#results) arrives as a placeholder resolved
from the code that computed it, under a gate that fails the build when prose
and code disagree.

## Methodology

### Solar concentration yield

Each mirror $M_i$ contributes optical power $P_i = I \cdot A_i \cdot \rho_i
\cdot c$ where $I$ is the direct normal irradiance, $A_i$ the mirror area,
$\rho_i$ its reflectivity, and $c$ an incidence factor (default 1). The field
optical power is the sum; thermal output multiplies by an optical efficiency
and a heat-transfer efficiency. The dimensionless concentration ratio at a
receiver of area $A_r$ is $C = \sum_i A_i \rho_i / A_r$. Given an area budget,
the highest-yield allocation is greedy: since yield-per-area is exactly
reflectivity, taking mirrors in descending reflectivity is optimal. The
implementation takes whole mirrors — a mirror is skipped when it does not fit
the remaining budget rather than being partially installed — so it is the
integral restriction of the fractional-knapsack greedy, and the budget can end
under-spent. Ties break on larger area first, which fixes the order
deterministically.

The model is deliberately lumped: the chain is
area × reflectivity × incidence × optical efficiency × heat-transfer
efficiency, with no ray tracing, per-heliostat aim geometry, atmospheric
attenuation, or receiver loss model. What it buys is a yield figure that is
exactly reproducible and exactly attributable; what it costs is documented in
[Scope and Related Work](#scope-and-related-work).

### Solar tracking & daily insolation

The daily resource follows the sun geometry. Solar declination $\delta$ and
the equation of time use Spencer's Fourier series [@spencer]. The daylight window
is $D = (2/15)\arccos(-\tan\varphi\tan\delta)$ hours from the sunrise hour
angle. For a fixed site and day the daily extraterrestrial irradiation on a
horizontal plane is the Duffie–Beckman closed form

$$H_0 = \frac{24}{\pi} G_{sc}\left[1 + 0.033\cos\frac{2\pi d}{365}\right]
\left(\cos\varphi\cos\delta\sin\omega_s + \omega_s\sin\varphi\sin\delta\right),$$

with $G_{sc}$ the solar constant and $\omega_s$ the sunrise hour angle in
radians [@duffie_beckman]; a clearness factor $\kappa$ converts it to a
clear-sky resource. The field's daily thermal energy is
$\kappa H_0 \sum_i A_i \rho_i \eta_{opt} \eta_{heat}$.

Elevation follows $\sin e = \sin\varphi\sin\delta + \cos\varphi\cos\delta\cos
H$, clamped to $[-1, 1]$ before the arcsine so a below-horizon sun returns a
non-positive elevation instead of raising. Horizontal beam flux is
$I\sin e$, floored at zero for a sun below the horizon, which is what truncates
the daily profile to the daylight window rather than
folding negative flux into the integral.

### Lair escape topology

Rooms are nodes and mirror passages are undirected edges of a graph $G$. The
shortest escape route is found by breadth-first search over sorted neighbour
lists, so the route is not merely *a* shortest path but a fixed one. The
canonical lair has 7 rooms and distances are counted in
passages.

Two distinct notions of "critical room" are computed, and they are not
interchangeable. A room is a *bottleneck* between a specific entry and exit if
removing it disconnects those two — computed exactly, by deleting each
candidate room in turn and re-testing reachability. A room is an *articulation
point* (cut vertex) if removing it disconnects any part of the graph at all,
computed in linear time by the Hopcroft–Tarjan depth-first low-link procedure
[@hopcroft_tarjan]. Every entry–exit bottleneck is an articulation point, but
the converse fails: a cut vertex hanging off a side branch splits the graph
without touching the escape route. The exhaustive-removal bottleneck solver is
$O(V(V+E))$, which is the right trade at lair scale and the wrong one at
building scale.

### Lair flow analysis

Escape *redundancy* is quantified by maximum flow on the lair treated as a
unit-capacity network: each undirected mirror passage becomes a pair of
opposed unit-capacity arcs. Edmonds–Karp augments along breadth-first paths
[@edmonds_karp], and by Menger's theorem the resulting flow value is exactly
the number of **edge-disjoint** escape routes — the entry–exit edge
connectivity. The residual graph's source-side reachable set then recovers the
**minimum cut**: the fewest mirror walls whose destruction seals the lair, with
cut value equal to flow value by max-flow min-cut [@ford_fulkerson]. The flow
is decomposed back into explicit routes by walking arcs that carry flow and
decrementing one unit per route, so the reported routes are real paths rather
than an aggregate number.

When mirror passages carry a traversal cost (mirror fragility, guard density),
Dijkstra's algorithm returns the cheapest escape route [@dijkstra]. Costs are
required for every passage — a missing cost raises rather than defaulting to
zero, since a silently free passage would fabricate an escape route.

### Duel / bounty scheduling

Bounty contracts are half-open intervals $[s, e)$ carrying a bounty $w$. Two
overlap iff $s_a < e_b \wedge s_b < e_a$. Two objectives are solved, because
they answer different questions and can disagree on the same book:

* **Maximum bounty** — *weighted interval scheduling* [@kleinberg_tardos]:
 sort by end time, binary-search the latest non-overlapping predecessor
 $p(j)$, and run the dynamic program $D(j)=\max(w_j + D(p(j)), D(j-1))$. Exact
 for arbitrary non-negative bounties.
* **Maximum count** — the earliest-finish greedy: repeatedly take the
 contract that finishes soonest among those still compatible. Exact for the
 count objective and, in general, wrong for the bounty objective.

Reporting only one of these would hide the trade-off the agent is actually
making, so [Results](#results) reports both.

### Deadline bounty scheduling

Unit-time bounty contracts each occupy one slot and must finish by their
deadline; the agent maximises accepted profit. The greedy that processes jobs
in descending profit and assigns each to the latest free slot at or before its
deadline is *exact*, not heuristic: the schedulable sets form a matroid, and
the greedy is optimal over a matroid [@cormen, sec. 16.5]. A path-compressed
disjoint-set structure [@tarjan_unionfind] answers the "latest free slot"
query in near-constant amortised time by merging each occupied slot onto its
left neighbour.

The reported profit and the reported slot assignment come from a single run of
this greedy rather than two independent ones, so the two views cannot
disagree — a divergence that would otherwise be invisible in the manuscript.

## Results

### Solar concentration yield

Under a direct normal irradiance of 1000 W/m², the canonical mirror
field (total aperture 300.0 m²) delivers
250.5 kW of optical power to the receiver aperture
(5.0 m²) and, after optical and heat-transfer losses, a
thermal output of **191.6325 kW** at a concentration ratio of
**50.10×**.

![Thermal heat output versus direct normal irradiance for the canonical SOLEX field.](output/figures/the_man_with_the_golden_gun_solex_yield.png)

Offered the same 5 mirrors under an area budget of
200 m², the greedy allocator installs
**alpha, bravo, echo**. The selection is instructive: after taking the
two highest-reflectivity mirrors the remaining budget is too small for the next
two candidates, so the allocator falls through to the smallest, lowest-quality
mirror rather than leaving the budget idle. Whole mirrors cannot be split, so
the budget finishes under-spent — the integral restriction of the fractional
optimum, not a failure of the greedy.

### Solar tracking & daily insolation

At the canonical site (8.0°N, day 172) the
declination is 23.45° and daylight lasts
12.47 hours. The sun reaches 74.55° at
solar noon. The daily extraterrestrial insolation on a horizontal plane is
10.03 kWh/m²; with a clearness factor this falls
to a clear-sky resource of 7.52 kWh/m², which the field
concentrates into **1441.7 kWh/day** of thermal energy.

![Clear-sky horizontal beam flux across the canonical SOLEX day.](output/figures/the_man_with_the_golden_gun_solex_daily.png)

#### Sensitivity and uncertainty of the daily yield

The headline daily figure (1441.7 kWh) is a single point on
two continua, and reading it as a point obscures how much of the number is the
model's two free inputs — the clearness factor and the site latitude:

| Clearness $\kappa$ | Clear-sky insolation (kWh/m²/day) | Field daily energy (kWh/day) |
| --- | --- | --- |
| 0.60 | 6.02 | 1153.4 |
| 0.75 | 7.52 | 1441.7 |
| 0.90 | 9.03 | 1730.1 |

The clearness factor is the single largest source of uncertainty in the daily
number: it is a bulk sunshine-availability parameter, not a measured quantity
for any particular island day, and the deliberately unmodelled physics (real
circumsolar attenuation, receiver thermal loss, mirror soiling) all live
behind it. That is why the mission *reports* the clear-sky number only at the
canonical clearness factor, never as a forecast.

Holding clearness fixed and moving the site latitude shifts the overhead sun:

| Latitude (deg N) | Field daily energy (kWh/day) |
| --- | --- |
| 0 | 1326.4 |
| 8 | 1441.7 |
| 23.44 | 1598.1 |

At the June solstice the sun stands directly over the Tropic of Cancer
(23.44°N), so moving the field north from the equator toward that latitude
raises the solstice noon elevation and, with it, the concentrated daily
energy; the maximum over this band is the 23.44°N row, where the sun is
overhead at noon. The canonical island (8.0°N) is south of
that maximum and therefore delivers less than its northernmost placement — a
site-sensitivity the headline single number cannot show. Both sweeps are live
engine output — the same `field_daily_energy_kwh` call the Results section
uses, evaluated over a parameter grid — so they cannot drift from the model
that produced the headline number.

### Lair escape topology

The funhouse lair comprises 7 rooms. The shortest escape route
from the entry to the vault is:

> Entrance -> Hall -> Mirror_Room -> Gallery -> Vault

covering 4 passages. The 3 rooms
that every escape route must pass through are **Gallery, Hall, Mirror_Room**; the lair
has 4 articulation points (single rooms whose removal
disconnects part of the funhouse).

The two counts differ, and the difference is the point. Articulation points
include rooms on the dead-end side branch, whose loss splits the funhouse
without touching the route to the vault; the bottleneck set is strictly the
rooms that stand between the entry and the exit. A defender garrisoning
articulation points would spend part of the effort guarding rooms the escaping
agent never enters.

![SOLEX funhouse lair graph with the escape route and bottleneck rooms highlighted.](output/figures/the_man_with_the_golden_gun_lair_topology.png)

### Lair flow analysis

The extended funhouse (10 rooms) offers
**3 edge-disjoint escape routes**; destroying
every passage of any single route still leaves the others open. To seal the
lair the enemy must cut **3 mirror walls** (the
minimum entry–exit cut), namely **Courtyard-Entry, Entry-Hall, Entry-Tunnel**. Cut value
equals flow value, as max-flow min-cut requires; the cheapest seal is at the
entry side, where the three corridors have not yet diverged. Under unit
traversal costs the cheapest escape route is

> Entry -> Tunnel -> Armory -> Vault

at cost 3.

### Duel / bounty scheduling

The appointment book holds 4 bounty contracts and contains
1 overlapping pair(s). Weighted interval scheduling selects
the non-overlapping set **B, C, D**, realising a maximum total bounty
of **13.0**.

The count-maximising earliest-finish greedy instead selects
**A, C, D**: 3 contracts worth
11.0, against the dynamic program's
3 contracts worth 13.0. Both schedules are
optimal for their own objective, and the disagreement is exactly the trade-off
the agent faces: booking the earliest-finishing contract first forfeits the
more valuable contract that overlaps it. Choosing the greedy because it is
simpler would cost bounty here, which is why the exact dynamic program is the
solver wired into the mission outcome.

![SOLEX bounty appointment book with the maximum-bounty selection filled.](output/figures/the_man_with_the_golden_gun_duel_schedule.png)

### Deadline bounty scheduling

The deadline book holds 5 unit-time bounty contracts.
The deadline greedy (union–find) accepts **E, C, B**,
realising a maximum profit of **18.0** with slot
assignment **1:B, 2:C, 3:E**.

All six solvers run through the frozen `MissionProvider` lifecycle; the
outcome carries full provenance including a deterministic input hash.

## Conclusion

The **SOLEX** mission software is a complete, gate-verified Project
BOND film package: 6 pure, deterministic domain modules
spanning solar concentration yield, solar tracking and daily insolation,
funhouse lair escape topology, lair flow analysis (max-flow, min-cut, and
cost-aware escape), and two bounty-scheduling models — weighted interval
scheduling and unit-time deadline scheduling — all adapted to the frozen
`MissionProvider` protocol through a single thin adapter.

Three findings are worth carrying out of the dossier. First, the mirror field's
thermal output tracks *effective* aperture rather than raw area: reflectivity,
not square metres, is the quantity the greedy allocator spends its budget on,
and the same asymmetry governs the daily energy figure. Second, escape
redundancy and escape criticality are different measurements on the same lair —
the 3 edge-disjoint routes of the extended
funhouse mean no single wall is decisive, while the canonical lair's
3 bottleneck rooms are each individually decisive, and
the articulation-point count is a third number answering a third question.
Third, the two duel solvers disagree on the same book: optimising contract
count and optimising bounty select different schedules, so naming the objective
matters more than picking a clever algorithm.

The methodological claim is narrower than the domain claim and matters more.
Every numeric statement above arrives from
`manuscript_variables.py::generate_variables`; none is typed by hand. The
config's restatement of the canonical inputs is recomputed and raises on
disagreement, the token gate fails on any metric prose cites but code does not
produce, and the coverage gate is set at 90% line-and-branch
on `src/` with a zero-mock suite. Determinism is likewise enforced rather than
asserted: the 4 figures are re-rendered and byte-compared in the
test suite. The package is a local-only working tree and publishes no remote,
so reproduction means re-running the pipeline in place — see
[Reproducibility](#reproducibility).

## Experimental Setup

This section fixes every input the results depend on. Nothing in the SOLEX
package is sampled, fitted, or drawn from an external service: each model is
evaluated on a canonical fixture defined in code, and the fixture is restated
in `manuscript/config.yaml` where it is verified against the code at token
generation time (see [Reproducibility](#reproducibility)).

### Software environment

| Item | Value |
| --- | --- |
| Package | `the_man_with_the_golden_gun` v0.1.0 |
| Mission codename | SOLEX |
| Python | 3.14.6 |
| Domain modules | 6 (`solar_concentration.py, solar_tracking.py, lair_topology.py, lair_flows.py, duel_scheduler.py, deadline_scheduler.py`) |
| Third-party runtime dependencies | `numpy`, `matplotlib`, `pyyaml`, `bond-api` |
| Deterministic seed | 3 |
| Figures | 4 |

`numpy` is used only to build the irradiance sweep grid for
; `matplotlib` only to render figures; `pyyaml` only to read
`config.yaml`. Every quantitative result in [Results](#results) is computed
with the Python standard library.

### Heliostat field

The canonical SOLEX field is 5 tracking mirrors totalling
300.0 m² of aperture, each with a fixed area and specular
reflectivity:

| Mirror | Area (m²) | Reflectivity |
| --- | --- | --- |
| `alpha` | 100.0 | 0.90 |
| `bravo` | 80.0 | 0.85 |
| `charlie` | 60.0 | 0.80 |
| `delta` | 50.0 | 0.75 |
| `echo` | 10.0 | 0.70 |

The receiver aperture is 5.0 m². Optical efficiency
(receiver intercept) is 0.90 and heat-transfer efficiency is 0.85; both are
module defaults and are swept by no experiment here. The direct normal
irradiance used for the headline yield is 1000 W/m².

The mirror-budget allocation experiment offers the same
5-mirror candidate set under an area budget of
200 m² — deliberately smaller than the field, so the greedy
allocator must actually choose.

### Solar site and day

| Parameter | Value |
| --- | --- |
| Latitude | 8.0°N |
| Day of year | 172 (northern solstice) |
| Solar constant | 1361 W/m² |
| Clearness factor | 0.75 |
| Peak DNI | 1000 W/m² |

The site stands in for the villain's island: a low northern latitude where the
solstice sun passes close to the zenith. The daily beam-flux profile
 is sampled at 10-minute steps in solar time and truncated
to elevations above the horizon.

### Funhouse lair fixtures

Two graph fixtures are used, and they answer different questions.

The **canonical lair** (7 rooms) is a mostly linear funhouse
with one dead-end branch. It is the fixture for escape routing and bottleneck
analysis, because a chain of forced rooms is exactly what makes the bottleneck
question interesting.

The **extended lair** (10 rooms) adds two parallel
corridors from the entry to the vault plus a dead-end wine cellar. It is the
fixture for flow analysis, because a lair with only one route has a trivial max
flow; three parallel routes give the Edmonds–Karp decomposition and the minimum
cut something to separate. Every passage carries unit capacity (one mirror
wall) and, for the cost-aware escape, unit traversal cost.

### Bounty contract books

The **duel book** holds 4 contracts as half-open intervals
`[start, end)` with a bounty:

| Contract | Interval | Bounty | Target |
| --- | --- | --- | --- |
| `A` | [0, 2) | 3 | First_Heel |
| `B` | [1, 3) | 5 | Second_Heel |
| `C` | [3, 6) | 6 | Solex_Guard |
| `D` | [6, 8) | 2 | Night_Watch |

The book is constructed so the greedy count-maximising answer and the
bounty-maximising answer differ — that divergence is the point of running both
solvers in [Results](#results).

The **deadline book** holds 5 unit-time contracts,
each with an integer deadline slot and a profit:

| Contract | Deadline | Profit |
| --- | --- | --- |
| `A` | 1 | 3 |
| `B` | 2 | 5 |
| `C` | 2 | 6 |
| `D` | 3 | 2 |
| `E` | 3 | 7 |

Total demand (5 contracts) exceeds the
3 available slots, so the scheduler must reject work;
a book that fit entirely would make the greedy vacuous.

## Reproducibility

Every number in this dossier is regenerable from a clean checkout by running
the commands below. There is no hidden state, no network call, no wall-clock
read in a persisted artifact, and no random draw.

### Regeneration procedure

```bash
uv sync --extra dev # resolve deps + bond-api path dep
uv run python scripts/00_preflight.py # protocol discoverability
uv run python scripts/generate_artifacts.py # outcome JSON + all figures
uv run python scripts/z_generate_manuscript_variables.py # token map + resolved sections
uv run pytest tests/ --cov=src --cov-fail-under=90
```

`scripts/generate_artifacts.py` writes `output/data/solex_outcome.json` and the
4 figures under `output/figures/`.
`scripts/z_generate_manuscript_variables.py` writes
`output/data/manuscript_variables.json` and the fully resolved manuscript tree
under `output/manuscript/`, and exits non-zero if any placeholder survives
substitution.

### Sources of determinism

The package has three potential nondeterminism surfaces, and each is closed:

1. **Randomness.** There is none. The declared seed (3) is
 recorded in the mission provenance for protocol conformance, not consumed by
 a generator — no module imports `random` or `numpy.random`. The correct
 reading of the seed is "this mission asserts it needs no entropy".
2. **Iteration order.** Graph algorithms iterate neighbours through `sorted`
 rather than set order, so the BFS escape route, the flow decomposition, and
 the minimum cut are stable across runs and interpreter hash seeds.
 Schedulers break ties on `(end, id)` and `(-profit, id)` respectively.
3. **Wall clock.** Persisted artifacts carry the fixed
 `DEFAULT_TIMESTAMP` (2026-08-04T00:00:00Z), and the mission outcome
 records `wall_time_s = 0.0` rather than a measured duration, so two runs
 produce byte-identical files. Figure PNGs are likewise byte-identical
 between runs; `tests/test_figures.py` asserts this by rendering each figure
 twice into separate directories and comparing bytes.

### Metric injection

No metric in this manuscript is typed by hand. Each is a double-brace
placeholder resolved by
`src/the_man_with_the_golden_gun/manuscript_variables.py::generate_variables`
from `manuscript/config.yaml` plus a live call into the domain models. Four
gates hold that discipline in place:

* `tests/test_manuscript_variables.py::test_all_manuscript_tokens_are_generated`
 scans every file the hydrator writes — the numbered sections and the Pandoc
 preamble, both drawn from `manuscript_variables.manuscript_sources` — and
 fails if one cites a token the generator does not produce.
* `scripts/z_generate_manuscript_variables.py` fails if a resolved file still
 contains an unsubstituted token.
* `manuscript_variables.verify_declared_experiment` recomputes every value
 the config's `experiment` block declares — the codename, the irradiance, the
 receiver aperture, the solar-site geometry, the lair entry and exit, the
 maximum duel bounty, the extended lair, and the whole deadline book — and
 raises if the config and the code disagree. It also raises on a declared key
 it has no recomputation for, so the checked surface cannot quietly shrink
 below the block. A stale config therefore fails the build rather than
 narrating a wrong number.
* `declarations.verify_claim_ledger` recomputes every value in
 `data/claim_ledger.yaml` at its recorded precision and checks that each
 claim's cited evidence symbol and test file exist. It runs during token
 generation because the config declares the ledger path, so the ledger is a
 checked restatement of the code rather than a parallel copy of the numbers.

### Test and gate discipline

The suite is zero-mock: no `unittest.mock`, no `MagicMock`, no `mocker.patch`
anywhere in `tests/`. Assertions are made against genuinely computed values
(known vectors derived from the algorithms' definitions), real rendered PNGs,
and real subprocess executions of the `scripts/` entry points. Line **and**
branch coverage on `src/` is gated at 90% by
`pytest --cov-fail-under`; `ruff check`, `ruff format --check`, and `mypy` must
be clean on `src/` and `scripts/`. The rationale for each of these choices is
recorded in `docs/testing_philosophy.md`.

### What is not reproducible here

This is a **local-only** working tree with no git remote and no published
archive. There is no DOI, no Zenodo deposit, and no public URL: the metadata
sidecars (`.zenodo.json`, `CITATION.cff`, `codemeta.json`) deliberately omit
DOI fields rather than carrying a placeholder. Reproduction therefore means
re-running the commands above inside this checkout, not fetching a release.

## Scope and Related Work

### What this package is

SOLEX is one film package in the PROJECT BOND fleet: a standalone,
deterministic implementation of the technical ideas that *The Man with the
Golden Gun* (1974) actually turns on, exposed through the fleet's frozen
`MissionProvider` protocol [@bond_protocol]. The film supplies the
specification — a solar concentrator whose output is worth killing for, a
mirror-walled funhouse an agent has to get out of, and an assassin who books
contracts one at a time — and the 6 domain modules supply
the implementation.

The design bet is that a film's premise is a legitimate specification. "How
much heat does a mirror field actually deliver" is a solar-engineering
question with a textbook answer; "which rooms must every escape route pass
through" is a graph question with an exact answer; "which contracts should the
assassin accept" is a scheduling question with two different exact answers
depending on what is being maximised. Building each one honestly is more
interesting than building a stub with a film title on it.

### What this package is not

It is not a heliostat design tool. The optical model is a lumped
area × reflectivity × efficiency chain: there is no ray tracing, no cosine
loss from individual heliostat aim points, no atmospheric attenuation between
mirror and tower, no receiver thermal-loss model, and no spillage. The
concentration ratio reported is a geometric flux ratio at the aperture, not a
peak flux map. A real central-receiver study would need all of these
[@duffie_beckman].

It is not a solar-position library. The Spencer Fourier series [@spencer] is
accurate to roughly a tenth of a degree in declination, which is ample for a
daily-energy figure and inadequate for tracker control. The standard upgrade
is the Astronomical Almanac algorithm [@michalsky]; it is deliberately not
implemented here because nothing in this dossier is sensitive at that
resolution, and implementing an unused higher-accuracy path would be
scaffolding rather than substance.

It is not a facility-security product. The lair graphs are hand-authored
fixtures of 7 and 10 rooms. The
bottleneck solver is *exact by exhaustive removal* — it deletes each room in
turn and re-tests reachability, which is O(V·(V+E)) and entirely appropriate at
this size, but it is not the algorithm to reach for on a large building. The
linear-time route is the biconnected-components decomposition
[@hopcroft_tarjan], which this package also implements
(`articulation_points`) but uses for a different question: cut vertices of the
whole graph rather than vertices separating a specific entry–exit pair. The
two answers differ, and conflating them would be the easy mistake here.

It is not a workforce scheduler. Both scheduling models assume perfect
information about a small, fixed contract book: no arrivals over time, no
uncertainty in duration, no cancellation, no travel time between targets.

### Relationship to the established literature

Nothing in the domain core is novel; that is the point. Each module is a
faithful implementation of a documented result, which is what makes the
outputs checkable against textbook values rather than against themselves:

| Module | Result implemented | Source |
| --- | --- | --- |
| `solar_concentration` | Lumped optical/thermal chain; fractional-knapsack greedy | [@duffie_beckman] |
| `solar_tracking` | Spencer declination and equation of time; Duffie–Beckman daily insolation closed form | [@spencer; @duffie_beckman] |
| `lair_topology` | BFS shortest path; Hopcroft–Tarjan cut vertices | [@cormen; @hopcroft_tarjan] |
| `lair_flows` | Edmonds–Karp max flow; max-flow min-cut; Dijkstra | [@edmonds_karp; @ford_fulkerson; @dijkstra] |
| `duel_scheduler` | Weighted interval scheduling DP; earliest-finish greedy | [@kleinberg_tardos] |
| `deadline_scheduler` | Unit-time scheduling with deadlines (matroid greedy) with union–find slot lookup | [@cormen; @tarjan_unionfind] |

The contribution, such as it is, lies in the *composition*: six textbook
results wired into a single deterministic mission lifecycle whose every
reported number is injected from the code that produced it, under gates that
fail rather than warn.

### Position in the fleet

SOLEX depends on exactly one fleet package, `bond-api`, and only through a
single adapter module. The 6 domain modules import
nothing outside the standard library, so the scientific core survives
independently of the protocol. Two integration points remain open and are
tracked in `TODO.md`: persisting executed outcomes to a provenance store once
`bond-utilities` ships, and cross-package missions once the coordinator lands.
Neither requires a change to the domain core.

## Appendix: Generated metric register

This appendix records the resolved values of every manuscript metric at
generation time (`2026-08-04T00:00:00Z`). The live inventory is produced by
`scripts/z_generate_manuscript_variables.py` into
`output/data/manuscript_variables.json`; the tables below list the
deterministic canonical outputs of the 6 domain models.
Nothing here is transcribed by hand — every cell is the same placeholder
mechanism used in the body sections, so the register cannot drift from the
prose that cites it.

### Solar concentration

| Metric | Value |
| --- | --- |
| Direct normal irradiance | 1000 W/m² |
| Field aperture | 300.0 m² |
| Receiver aperture | 5.0 m² |
| Optical power | 250.5 kW |
| Thermal heat output | 191.6325 kW |
| Concentration ratio | 50.10× |
| Mirrors in field | 5 |
| Allocation budget | 200 m² |
| Allocation selection | alpha, bravo, echo |

### Solar tracking & daily insolation

| Metric | Value |
| --- | --- |
| Latitude | 8.0°N |
| Day of year | 172 |
| Declination | 23.45° |
| Noon elevation | 74.55° |
| Daylight | 12.47 hours |
| Extraterrestrial insolation | 10.03 kWh/m² |
| Clear-sky insolation | 7.52 kWh/m² |
| Field daily energy | 1441.7 kWh |

Sensitivity — clearness factor (kWh/m²/day, kWh/day):

| Clearness | Clear-sky insolation (kWh/m²/day) | Field daily energy (kWh/day) |
| --- | --- | --- |
| 0.60 | 6.02 | 1153.4 |
| 0.75 | 7.52 | 1441.7 |
| 0.90 | 9.03 | 1730.1 |

Sensitivity — site latitude (deg N, kWh/day):

| Latitude (deg N) | Field daily energy (kWh/day) |
| --- | --- |
| 0 | 1326.4 |
| 8 | 1441.7 |
| 23.44 | 1598.1 |

### Lair topology (canonical)

| Metric | Value |
| --- | --- |
| Rooms | 7 |
| Escape distance | 4 passages |
| Escape route | Entrance -> Hall -> Mirror_Room -> Gallery -> Vault |
| Bottleneck rooms | Gallery, Hall, Mirror_Room |
| Articulation points | 4 |

### Lair flow (extended)

| Metric | Value |
| --- | --- |
| Rooms | 10 |
| Edge connectivity | 3 |
| Min-cut wall count | 3 |
| Min-cut walls | Courtyard-Entry, Entry-Hall, Entry-Tunnel |
| Cheapest escape cost | 3 |
| Cheapest escape route | Entry -> Tunnel -> Armory -> Vault |

### Duel interval scheduling

| Metric | Value |
| --- | --- |
| Contracts | 4 |
| Conflicts | 1 |
| Max-bounty selection | B, C, D (3) |
| Maximum bounty | 13.0 |
| Earliest-finish selection | A, C, D (3) |
| Earliest-finish bounty | 11.0 |

### Deadline scheduling

| Metric | Value |
| --- | --- |
| Jobs | 5 |
| Selected | E, C, B |
| Maximum profit | 18.0 |
| Slot assignment | 1:B, 2:C, 3:E |

### Environment and gates

| Metric | Value |
| --- | --- |
| Package version | 0.1.0 |
| Mission seed | 3 |
| Domain modules | 6 |
| Figures | 4 |
| Coverage gate | 90% line + branch on `src/` |
| Python | 3.14.6 |
| Timestamp | 2026-08-04T00:00:00Z |

## Sources

@bond_protocol; @golden_gun_film; @duffie_beckman; @spencer; @michalsky; @cormen; @ford_fulkerson; @edmonds_karp; @dijkstra; @hopcroft_tarjan; @kleinberg_tardos; @tarjan_unionfind


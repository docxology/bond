# Live and Let Die (1973) — SAN MONIQUE

*film package · package codename SAN MONIQUE*. Mission **SAN MONIQUE**: map the narcotics supply graph and identify the critical transit bottleneck; decipher the voodoo-coded communiqué by symbol-substitution; plan an infiltration route across crocodile terrain to the airfield.

## Concepts — SAN MONIQUE: domain and operational focus

narcotics networks, coded comms

## Abstract — SAN MONIQUE: mission summary

--- title: "Live and Let Die: SAN MONIQUE — Special-Agent Mission Software" date: "2026-08-05" --- Live and Let Die: SAN MONIQUE — Special-Agent Mission Software (mission codename **SAN MONIQUE**) delivers deterministic, special-agent mission software for Kananga's narcotics operation on the Caribbean island of San Monique. The system models the narcotics supply chain as a directed, capacity-constrained graph of 7 nodes and 10 legs spanning production, transit, and market. It recovers the cheapest route to each destination market (13 units to Miami), computes the maximum network throughput (220 units, capped by a min-cut value of 220), and identifies the single highest-value interdiction target: the **airfield**, whose neutralization stops 110 of those 220 units. Both figures are measured on the same demand-capped flow model; the min cut itself is demand-limited and names no severable asset, so the target comes from the disruption probe and not from the cut. Building on the graph core, a **budgeted interdiction** study shows the network is operationally fragile: an optimal 3-leg strike plan (greedy 220 units, exact optimum 220) severs the entire 220-unit operation, and the top individual target leg, field_works→harbor, is worth 50 units alone. The intelligence layer deciphers both a voodoo-coded communiqué by keyword symbol-substitution (key BARON, recovering *"KANANGA LETS THE SNAKE BITE"*) and a 195-beat drum-code transmission (exact round-trip, density 0.441) carrying *"KANANGA LETS THE SNAKE BITE"*. A market-flow economic model traces price and purity from the farm gate (300 $/kg) to the street, yielding a farm gate-to-street spread of 59× and a producer share of 1.7% of the 3888000 $ gross revenue. Those two numbers are arithmetic consequences of invented scenario parameters, not empirical estimates — see §Scope. Finally, a terrain-graph infiltration planner routes an agent from the south landing beaches to the airfield at cost 41, wading 4 crocodile-water cells against a computed floor of 4 over every possible route. All analyses are deterministic, real-data-only, and fully provenance-stamped (input hash `46044979efeafa09`).

## Introduction — SAN MONIQUE: mission framing, the operational problem, and how to read this chapter

*Live and Let Die* (1973) follows James Bond to the fictional Caribbean
island of San Monique, where the villain Kananga — governor by day, narcotics
baron by night — runs a poppy-to-market operation and protects his enterprise
with voodoo-coded radio traffic and a mangrove-and-crocodile coastline. This
package turns that milieu into 6 deterministic computation
problems — one pure domain module each — of the kind an intelligence analyst
would actually run before an operation:

1. **Supply-graph analytics.** Model the narcotics chain as a capacity-constrained
 flow network and answer operational questions: what is the cheapest route to
 market, how much volume can move, and which single transit asset — if
 seized — costs the enemy the most? The answer sharpens the targeting case
 against a specific bottleneck.
2. **Budgeted network interdiction.** One bottleneck is a target; a *strike
 plan* is a campaign. Given a fixed budget of legs that can be severed in one
 coordinated operation, choose the set that costs the enemy the most
 throughput — and bound the heuristic's quality with an exact optimum.
3. **Coded-communiqué deciphering.** The voodoo "symbol substitution" is a
 monoalphabetic keyword cipher. Recover the substitution table and decrypt the
 intercepted message; a frequency-attack solver provides an unkeyed
 best-effort fallback.
4. **Drum-code signalling.** The cult's drums are a channel, not set dressing.
 Encode and decode messages as Morse-timed rhythm on a per-beat grid, and
 reduce an intercepted transmission to a comparable traffic signature.
5. **Market-flow economics.** Volume is only half the operation; the other half
 is money. Propagate price and purity from the farm gate to the street to
 establish who actually captures the value — and therefore where interdiction
 bites.
6. **Island ops planning.** San Monique is a terrain graph of mangrove, swamp,
 open coast, and a crocodile channel. Plan the lowest-cost infiltration route
 while tracking how much of it crosses crocodile water.

Across all 6 modules the mission lifecycle of the BOND-API protocol
(brief, recon, plan, execute, debrief) is exercised: a brief declares the
3 mission objectives, recon surveys the ground truth,
planning schedules the analytical steps, execution computes every result, and
debriefing distils actionable lessons with full provenance (fixed seed
8, canonical input hash). The same analysers are exposed as
6 named gadgets so a coordinator can invoke any one of them
directly, without running the full mission.

## Methodology — SAN MONIQUE: the analytical models and algorithms that drive the mission

### Supply-graph analytics

The San Monique operation is represented as a directed, weighted,
capacity-constrained graph `G = (V, E)`. Vertices are classified as
`production` (interior poppy fields, field processing works), `transit`
(airfield, harbor, smuggler's cove), or `market` (Miami, New York). Each edge
carries a unit cost (money, risk, time) and a throughput capacity (units per
reporting period).

- **Cheapest route.** Dijkstra's algorithm returns the minimal total cost and
 ordered node sequence from a production source to each market. Deterministic
 tie-breaking uses `(cost, node_id)` heap keys.
- **Maximum throughput.** Edmonds-Karp (BFS augmenting path) computes the
 maximum flow that can be pushed from a virtual super-source
 (SUPPLY) through the network to a virtual super-sink
 (DEMAND). Production nodes are bounded by their crop capacity
 and markets by their demand ceilings.
- **Bottleneck — and what the cut does *not* tell us.** The minimum cut (the set
 of forward edges leaving the residual-reachable set after max-flow) bounds
 throughput. On this instance the cut is miami→DEMAND, new_york→DEMAND: both are
 *virtual* edges into the super-sink encoding market demand ceilings, and
 0 physical supply legs appear in it. The network
 is therefore demand-limited, and the min cut is a capacity bound that
 names nothing an operation could strike. Interdiction targeting comes from a
 separate per-transit-node disruption probe, which re-computes flow after
 neutralizing each transit asset and reports the one whose loss costs the most.
 That probe runs on the *same* demand-capped flow graph as the max-flow figure,
 so its answer is expressed in — and bounded by — the throughput the model
 actually admits.

### Budgeted network interdiction

Beyond a single bottleneck, the operation asks *how much of the network can be
taken down with a limited strike budget*. This is the deterministic network
interdiction problem: with a budget `B` of transit legs that can be severed in
one coordinated operation, choose the legs that cost the enemy the most
throughput. Two solvers are provided:

- **Greedy** — myopically sever the leg with the largest marginal throughput
 drop, then repeat; deterministic tie-breaking on leg order.
- **Exact** — exhaustive enumeration of all `B`-subsets of severable legs
 (feasible at this scale) that maximises reduction; it is the correctness
 reference for the greedy heuristic.
- **Efficiency ranking** — each leg's *independent* throughput impact, ranked,
 forming the target list.

### Coded communiqués: symbol substitution and drum code

The voodoo "symbol substitution" is a monoalphabetic keyword cipher over the
26-letter alphabet: a keyword (here BARON) seeds a reshuffled cipher
alphabet (duplicates dropped, remaining letters appended), and each plaintext
letter maps to the cipher symbol at its index. To handle an *unkeyed* intercept,
`solve_substitution` performs a frequency attack: ciphertext symbols are ranked
by observed frequency and matched to reference English letters ranked by
expected frequency; the candidate plaintext is scored by cosine similarity of
its frequency profile against the reference distribution.

Alongside the written cipher, the cult's **drum code** is a Morse-style rhythm
codec over a per-beat `0/1` grid, on standard International Morse timing
(dot = 1 sounding beat, dash = 3; intra-letter gap 1, inter-letter gap 3, inter-word gap 7). `signal_for_text` encodes any
message onto the beat grid and `decode_signal` recovers it exactly under strict
run-length validation. `rhythm_signature` / `signature_distance` give a numeric
traffic signature so two intercepted signals can be compared.

### Market-flow economics

The money side: the same legs that carry volume also mark prices up and dilute
purity from the farm gate (300 $/kg) to the street
(2 markets). Price and purity propagate along the cheapest
path (by arbitrage the lowest-cost channel sets the price), and the street stage
applies a retail markup and a purity dilution. The headline metric is the
**producer share** — the farm-gate value as a fraction of street price — and the
**price-spread ratio**, both driven by the per-leg economics dataset
`EDGE_ECONOMICS`.

Every parameter in that dataset, and the farm-gate price, retail markup and
retail dilution alongside it, is invented for this fictional scenario; none is
fitted to data. The producer share the model reports is therefore the
reciprocal of a chosen product of markups. What is *demonstrated* is the
mechanism rather than the magnitude: the test suite re-runs the identical model
on substituted parameter sets and shows the share moving with them — under a
neutral table with no transit markups it rises to the reciprocal of the retail
markup alone.

### Island ops planning

San Monique is discretized as a 9x9 terrain grid where each
cell is a terrain type with a movement cost (road / open ground / beach cost 1, mangrove / open water cost 3, swamp cost 5, crocodile water cost 7, impassable infinite). Dijkstra over the four cardinal
neighbours finds the lowest-cost route between the landing beach and the
airfield zone; the planner reports total cost, the path, and the number of
crocodile-water cells traversed as a hazard metric.

That count describes one route. To say anything about *every* route the planner
runs a second Dijkstra whose edge weight is 1 for entering a crocodile cell and
0 otherwise; its optimum is the minimum crocodile exposure over the whole route
space, and no route — however expensive — can wade fewer cells than that. Only
the second number licenses a universally quantified claim. The two are distinct
quantities: where a crocodile-free detour exists the cheapest route may wade
while the minimum is zero.

## Results — SAN MONIQUE: measured outcomes, headline numbers, and what they establish

All figures below are deterministic and regenerable from the source tree.

### Supply graph

The canonical San Monique network has 7 nodes and
10 legs. The cheapest production-to-market routes are:

| Destination | Cost | Route |
| --- | --- | --- |
| Miami | 13 | poppy_fields -> airfield -> miami |
| New York | 18 | poppy_fields -> field_works -> harbor -> new_york |

Total maximum throughput is 220 units (220 bound),
capped by destination-market demand. The min cut is miami→DEMAND, new_york→DEMAND —
both virtual demand edges, 0 physical legs — so
the network is demand-limited and the cut is a bound, not a target list.

The production flow into miami, new_york is nonetheless sharply exposed to a
single asset. Probing the same demand-capped model node by node, the most
critical transit node is the **airfield**: neutralizing it removes
110 of the 220 units the network moves — the
highest-value single interdiction on the island.

![The San Monique supply network: cheapest production-to-Miami route and the
critical transit node highlighted.](output/figures/live_and_let_die_supply_graph.png)

### Interdiction

Against a base flow of 220 units, a coordinated strike plan is
frighteningly effective. The greedy plan severs
field_works→harbor, airfield→miami, airfield→cove for a simultaneous 220-unit
reduction (cost-effectiveness 73 units per leg, leaving
0); the exhaustive optimum severs airfield→cove, airfield→miami, field_works→harbor
for the same 220-unit total — the entire operation
collapses. The single most valuable leg on the target list is
field_works→harbor (50 units alone).

![Greedy versus exhaustive-optimal throughput reduction across strike
budgets.](output/figures/live_and_let_die_interdiction_curve.png)

### Communiqués

The intercepted voodoo communiqué deciphers under the keyword substitution
(BARON) to:

> KANANGA LETS THE SNAKE BITE

The ciphertext after encipherment is `HBKBKDB INTS TEN SKBHN AFTN`.

The cult's drums carry a 195-beat message that decodes exactly
(density 0.441, longest run 3) to:

> KANANGA LETS THE SNAKE BITE

(decoding verified **exact**).

### Market economics

From a farm-gate price of 300 $/kg, street-level prices
reach 14400 $/kg at 57% purity in
Miami and 21600 $/kg at 49% purity in
New York. The demand-weighted average street price is 17673
$/kg — a 59× farm-gate-to-street spread — and the farm-gate
producer retains **1.7%** of the street value. Across
2 markets the operation grosses about
3888000 $.

| Market | Street price ($/kg) | Street purity | Demand | Revenue ($) |
| --- | --- | --- | --- | --- |
| Miami | 14400 | 57% | 120 | 1728000 |
| New York | 21600 | 49% | 100 | 2160000 |
| **Total** | — | — | 220 | **3888000** |

The demand figures in the table come from the same committed
`SAN_MONIQUE_DEMAND` dataset that caps the supply-graph flow, so the revenue
section and the throughput section share one source of truth. Every row is
computed by `market_flow_report` — no value is hand-authored.

These are outputs of invented parameters, not measurements: they establish that
multiplicative per-leg markups compress the producer's share, and nothing about
the size of that share in any real market (see §Scope). The 1.7% producer share
is the reciprocal of the product of chosen markups, so it tracks any change in
those assumptions exactly — a sensitivity the test suite re-runs rather than
reports as a fixed interval.

### Infiltration route

The terrain planner routes an agent from the south landing beach
((8,1)) to the airfield zone ((0,4)) in
11 moves at total cost 41, crossing
4 crocodile-water cells.

The exposure-minimising search puts the floor over *all* routes at
4 cells: the channel is walled by impassable cliff on
both flanks, so no overland approach to the airfield — at any movement cost —
wades fewer than 4. The cheapest route achieves that
floor exactly.

![The terrain grid with the planned infiltration route
overlaid.](output/figures/live_and_let_die_island_route.png)

## Conclusion — SAN MONIQUE: findings, verdict, and what the mission establishes

The SAN MONIQUE mission software turns the Live and Let Die set pieces into
deterministic, auditable computation. The narcotics operation is demand-capped
at 220 units yet operationally fragile: it hinges on one transit
asset (the airfield, worth 110 of those
220 units), and a budgeted 3-leg interdiction plan
collapses the entire 220-unit network (exact reduction
220, greedy 220). Within the
scenario's assumed economics — invented parameters, not empirical ones — the
farm-gate producer keeps 1.7% of the
3888000 $ street value across a 59× price
spread, which motivates targeting the chain rather than the field.

The intelligence layer is equally decisive: the voodoo "code" is a recoverable
keyword substitution (BARON) hiding *"KANANGA LETS THE SNAKE BITE"*, and the
cult's drums carry a 195-beat message that decodes *exactly*
to *"KANANGA LETS THE SNAKE BITE"*. Finally, an exposure-minimising search over the
whole route space establishes that any overland infiltration of the airfield
must wade at least 4 crocodile-water cells; the
cheapest route attains that floor at cost 41.

Every result is reproducible from a fixed seed with a canonical input hash
(`46044979efeafa09`), making the software a complete research exemplar of
flow-based network interdiction, classical and rhythm-based cryptanalysis, and
narcotics economics unified under a frozen mission protocol.

## Experimental Setup — SAN MONIQUE: canonical scenarios, parameters, and configuration

### Dataset

All inputs are canonical, deterministic San Monique datasets embedded in the
pure domain modules:

- **Supply graph** (`supply_graph.py`): 7 nodes and
 10 directed legs with integer capacities; production crop
 ceilings and market demand ceilings bound the flow and interdiction
 problems.
- **Interdiction** (`interdiction.py`): the same graph is the interdiction
 instance; the severable set is every real transit leg, and a budget of
 3 legs defines the canonical strike plan.
- **Communiqué / drum code** (`coded_comms.py`, `voodoo_drums.py`): a keyword
 cipher over the 26-letter alphabet (keyword
 BARON) with the canonical plaintext, and a Morse-timed drum message
 (*"KANANGA LETS THE SNAKE BITE"*) on the timing dot = 1 sounding beat, dash = 3; intra-letter gap 1, inter-letter gap 3, inter-word gap 7.
- **Market economics** (`market_flow.py`): per-leg price-markup and purity
 dilution factors in `EDGE_ECONOMICS`, a farm-gate price of
 300 $/kg, and retail markup/dilution factors.
- **Terrain** (`island_ops.py`): a fixed 9x9 terrain grid
 (9 rows x 9 columns) of beaches, open
 ground, mangrove, swamp, and a crocodile channel walled by impassable cliff.

### Determinism

No random draws and no wall-clock dependence enter any analytic result. The
mission records a fixed provenance seed (8), a canonical input hash
(`46044979efeafa09`) spanning every analysis input (graph, ciphers, drum
message, and per-leg economics), and a zero wall-clock figure. Route, flow,
augmenting-path, and interdiction tie-breaking are all order-stable; the
greedy and exact interdiction solvers are fully enumerable for the canonical
scale.

### Figures

Three figures are regenerated by `scripts/generate_figures.py` under
`output/figures/` from the same pure-domain data the manuscript numbers are
computed from — no figure metric is hand-authored, and figure captions
interpolate computed values (for example the bottleneck node name) rather than
naming them in a string literal. All three are embedded in §Results through the
`../figures` token, which is derived from the real output paths so the
rendered section carries a link that resolves; a test opens every embedded path
and fails if a figure is missing or renamed:

- `supply_graph.png` — the network with the cheapest production-to-Miami route
 and the critical transit node highlighted;
- `interdiction_curve.png` — greedy versus exhaustive-optimal throughput
 reduction across strike budgets;
- `island_route.png` — the terrain grid with the planned infiltration route
 overlaid.

## Reproducibility — SAN MONIQUE: verification gates, deterministic regeneration, and artifacts

Every number in this manuscript is computed, never typed: the thin orchestrator
`scripts/z_generate_manuscript_variables.py` calls `generate_variables` in
`src/live_and_let_die/manuscript_variables.py`, which computes each placeholder
from the pure domain core. The manuscript cross-reference test scans every
numbered section (`manuscript/[0-9]*.md`) and fails if any placeholder used in
prose is not produced by `generate_variables`, so the prose cannot cite a
number the code does not compute. (The converse is not gated: a produced token
that no section uses is permitted and is not a test failure.)

Result provenance is recorded per-mission: the canonical input hash is
`46044979efeafa09`, the fixed seed is 8, and execution sets a zero
wall-clock figure. A SHA-256 digest of the canonical inputs fingerprints the
inputs, so a re-run can be checked against an audited outcome — the digest
identifies the inputs, it does not by itself reconstitute the results.

### Byte-identical regeneration

Running `scripts/z_generate_manuscript_variables.py` twice on an unchanged tree
produces byte-identical artifacts. **Scope of that claim:** the hydrated table
`output/data/manuscript_variables.json` and every resolved section under
`output/manuscript/`. Every value in those files comes from a committed source —
the pure domain core, or `manuscript/config.yaml` — and nothing under `src/`
reads the system clock, so there is no run-varying byte to differ. The
publication date above is `paper.date` in `manuscript/config.yaml`, bumped by
hand when the manuscript is republished; it is deliberately not a generation
timestamp, because a generation timestamp would make every regeneration differ.

The claim is gated, not asserted:
`tests/test_scripts_smoke.py::test_regeneration_is_byte_identical` runs the real
script twice — separated by more than one wall-clock second, so a
second-resolution clock cannot slip through by landing in the same second — and
diffs the persisted bytes. Its in-process counterpart is
`tests/test_manuscript_variables.py::test_regenerating_variables_across_a_wall_clock_second_is_identical`.

Two things are outside the scope of the byte-identical claim. Figures under
`output/figures/` are PNGs written by a separate script and are not diffed
here. And nothing in this package records a real timestamp anywhere — if a
future run-scoped provenance record needs one, it must live outside the two
paths named above, and this scope statement must be amended to say so.

Verification gates (see README):

```
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/
uv run mypy src/
rg -n "template[_]code_project". # expectation: zero
```

## Scope and Related Work — SAN MONIQUE: boundaries, positioning, and relationship to the literature

This package is one film in the PROJECT BOND suite of 33 packages: 27 film
packages implementing a shared, FROZEN mission protocol
(`bond_api.MissionProvider`) over pure domain cores, plus six infrastructure
packages (api, utilities, coordinator, orchestrator, cli, ops). It is a local
working exemplar developed from the template computing-project scaffold — lineage
is documented, not reproduced as source.

The analytical techniques are classical and deliberately textbook-grade,
spanning three research literatures:

- **Max-flow / min-cut and network interdiction.** Edmonds-Karp with the
 residual-cut theorem underpins bottleneck and single-point-of-failure
 analysis. The budgeted interdiction problem — minimize remaining throughput
 given a fixed number of removed legs — follows Wood's deterministic network
 interdiction formulation; the greedy and exhaustive solvers here are
 self-contained (`wood1993`).
- **Coded communications.** Monoalphabetic keyword substitution with a
 frequency-attack solver (`stinson2019`) sits beside the drum code, a
 rhythm codec over a per-beat grid whose element and gap durations follow the
 normative International Morse timing ratios (`itu2009`) — a numerical
 treatment of the Caribbean drum telegraphy the film uses.
- **Narcotics market economics.** The *question* — who captures the value
 between farm gate and street, and what that implies for enforcement — is the
 one posed by Reuter & Kleiman and by Caulkins & Reuter (`reuter1986`,
 `caulkins2010`). The *parameters* are not theirs and are not anyone's data:
 the farm-gate price, the retail markup and dilution, and all ten per-leg
 markup/dilution pairs in `EDGE_ECONOMICS` were chosen for this fictional
 scenario. Nothing here estimates, calibrates against, or reproduces a
 published figure, and the producer share reported in §Results should not be
 read as agreeing or disagreeing with any empirical estimate. The model
 contributes a mechanism — multiplicative per-leg markups compress the
 producer's share — exercised on invented numbers.
- **Terrain pathfinding.** Grid Dijkstra is the standard cost-minimising planner
 for rasterized maps, applied to a hazard-labelled island.

The novel contribution is not the algorithms but their unification:
6 film concepts, 6 pure modules exposed
as 6 named gadgets, one frozen mission protocol, one
provenance chain — reproducible end to end with no mocks and no external
services.


### Limitations and uncertainty

The analytical machinery is exact and deterministic (integer-capacity graphs,
closed-form economics, fixed terrain), so it carries no sampling error — but
that precision is not accuracy. Every headline number in §Results inherits the
uncertainty of the *inputs* it is computed from, which are assumptions, not
measurements:

- **Supply-graph capacities, crop ceilings, and demand ceilings** are invented
 scale figures for the fictional scenario. The throughput (220)
 and disruption (110) figures are exact arithmetic on those
 chosen numbers; changing any capacity changes both. The analysis establishes
 *structure* — the network is demand-limited, hinges on one transit asset —
 not a measured magnitude.
- **Economic parameters** (farm-gate price, retail markup/dilution, all ten
 per-leg markup/dilution pairs) are invented. The producer share
 (1.7%) and the price spread (59×) are
 the exact reciprocals of chosen products of markups; re-run the model under
 different parameters and they move exactly as the assumptions dictate. The
 test suite binds this as sensitivity, not as a confidence interval, because
 there is no sampling distribution to quantify — only the chosen inputs.
- **Interdiction** greedy-vs-optimal: the greedy and exhaustive solvers agree
 at 3-leg reduction here (220 /
 220), but greedy is a heuristic and its optimality is
 *not* guaranteed in general. On this instance the exhaustive optimum
 confirms the greedy plan is exact — that is evidence for this graph, not a
 general bound.
- **Terrain costs** are unit figures chosen for the scenario; the route cost
 (41) and crocodile exposure (4) are
 exact on those costs. The universal claim (any route wades at least
 4) is a structural fact of the committed grid
 (impassable cliff walls), so it is robust to the cost *numbers*, though it
 does depend on the grid topology being the island's.

In short: the package's contribution is deterministic, reproducible
computation over explicitly declared assumptions. Figures are recomputable to
the last unit, but they should be read as "exact given these invented
parameters", never as empirical estimates. This is the honest scope of the
whole suite, and it is enforced by the test gates rather than stated once.

## Sources — SAN MONIQUE: bibliography

@film_lald; @cormen2009; @wood1993; @stinson2019; @itu2009; @reuter1986; @caulkins2010


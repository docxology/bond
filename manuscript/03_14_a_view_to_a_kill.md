# A View to a Kill (1985) — MAIN STRIKE

*film package · package codename MAIN STRIKE*. Mission **ZORIN**: map microchip supply-chain monopoly choke points; optimize the budgeted acquisition that corners the market; model flood-the-mine water-ingress dynamics; couple the flood to surface-fab capacity loss in the valley; score horse-race form analytics for the cover operation; price the cover's betting-market position and staking.

## Concepts — MAIN STRIKE: domain and operational focus

microchip supply chain, urban sabotage, racing analytics

## Abstract — MAIN STRIKE: mission summary

**A View to a Kill (1985) · mission codename ZORIN** This package implements **A View to a Kill: ZORIN — Special-Agent Mission Software** as a deterministic, fully-tested special-agent mission model. It operationalizes the film's central scheme through six pure, infrastructure-free domain modules: 1. **Microchip supply-chain security graph** (`chip_supply_chain.py`) — a directed graph of the mid-1980s semiconductor market ($12$ firms, $18$ supply links across four stages). Concentration (HHI), Brandes betweenness choke points, single-source dependence, and cascade failure quantify the monopoly attack. 2. **Monopoly acquisition optimizer** (`acquisition.py`) — the budgeted selection problem of which independent fabricators ZORIN buys to corner the market. Exhaustive search for the optimal acquisition (`intel_fab, nec_fab`) raises market-wide HHI from a 1012.8 baseline to 1741.4 with a budget of 2, a gain of 728.6. The set the film-faithful scenario buys (`amd_fab, nec_fab`) is a different set scoring 1528.9; the scheme is suboptimal by 212.5 HHI points, and we report that rather than claim optimality for it. 3. **Flood-the-mine water-ingress dynamics** (`mine_flood.py`) — a mass-conserving deterministic Euler simulation of water flowing through the 8-chamber "Main Strike" network, flooding 0.625 of it by 900.0 s with a water-balance error of $1.2e-15$ (machine precision). 4. **Valley impact / urban sabotage** (`valley_impact.py`) — couples the flood to the fabs above: rising groundwater disables 3 of 5 valley fabs, 0.583 of fabricating capacity. ZORIN's own plant is among the 2 survivors (`nec_fab, zorin_fab`); the other survivor is `nec_fab`, which he acquires, so the number of surviving plants he neither owns nor acquires is 0. The bluntness runs the other way: `amd_fab`, a plant ZORIN buys, is destroyed by his own flood. 5. **Horse-race form analytics** (`race_analytics.py`) — normalized speed indices, EWMA ratings, softmax win probabilities, and a signal-detection cover-risk model. A subtle 0.2 speed-index boost to Pegasus carries only 0.001 detection risk (expected value 2924); a blatant boost is caught. 6. **Racing betting-market / cover-finance** (`race_market.py`) — converts the softmax win probabilities to honest-market decimal odds under a 1.12 overround, and prices the cover: Pegasus's boosted true probability (0.248) exceeds the market-implied (0.238), yielding a positive value edge (0.0415) and a Kelly stake of 1298 — the exact anomaly to detect. Every metric is computed, not asserted: figures, manuscript tokens, and the BOND-API mission provider all draw from the same pure core (seed 1985, fully deterministic). Keywords: microchip supply-chain security, monopoly choke points, herfindahl-hirschman index, betweenness centrality, budgeted acquisition optimization, water-ingress dynamics, mine flooding simulation, groundwater inundation damage, horse-race form analytics, cover-operation modeling, signal-detection theory, kelly criterion, betting-market pricing, reproducible research, deterministic simulation.

## Introduction — MAIN STRIKE: mission framing, the operational problem, and how to read this chapter

In *A View to a Kill* (1985), industrialist Max ZORIN plots to flood the
abandoned mine workings beneath California's Silicon Valley, destroying
every competing microchip fabrication plant and leaving his own operation as
the valley's sole surviving manufacturer. His scheme has three load-bearing
pieces: a **monopoly** over the microchip supply chain, an **infrastructure
sabotage** (the flood) that removes the competition, and a **cover**
operation (a winning racehorse) that draws attention and capital away from
the true plan.

This package turns each piece into real, deterministic, testable mathematics.
It is a PROJECT BOND film package: it implements the FROZEN
`bond_api.MissionProvider` protocol (the mission lifecycle of brief, recon,
plan, execute, debrief) around a pure domain core that is deliberately free
of protocol imports, so the science stands alone and the protocol is a thin
adapter.

### The six models

Each of the three load-bearing pieces is developed twice: once as the
*structure* of the problem and once as the *decision* the structure forces.

- **Supply-chain security graph** (`chip_supply_chain.py`). Microchips flowed
 through a multi-stage market in 1985 — silicon wafer suppliers, fabrication
 fabs, assembly and packaging houses, and distributors. ZORIN's monopoly is
 the classic choke-point problem: which few firms, if acquired or eliminated,
 corner the market. We formalize this with capacity market shares, the
 Herfindahl-Hirschman concentration index, betweenness centrality, and a
 supply-cascade failure model.
- **Monopoly acquisition optimizer** (`acquisition.py`). Given the graph, the
 monopoly is a *budgeted selection* problem: with money for $K$ purchases,
 which independent fabricators does ZORIN buy? We solve it exhaustively (the
 optimum, with deterministic tie-breaking) and greedily (the naive baseline),
 and report the regret between them.
- **Flood-the-mine dynamics** (`mine_flood.py`). A mine is a network of
 chambers and tunnels; a sabotage flood is water entering that network and
 propagating downhill under a head-driven flow law. We simulate the
 water-ingress dynamics deterministically and verify exact mass conservation.
- **Valley impact** (`valley_impact.py`). The flood is only the mechanism; the
 sabotage is what it reaches. Each surface fabrication plant is hydraulically
 coupled to a mine chamber, so rising chamber head raises the water table
 under the fab until its foundation is inundated. This converts the flood
 curve into lost fabricating capacity — and shows which plant survives.
- **Race-form cover analytics** (`race_analytics.py`). The cover is a horse
 whose form he can knowingly improve. We score legitimate form from raw race
 records, convert ratings to win probabilities, and model the risk that the
 manipulation is detected — a signal-detection trade-off between a bigger win
 probability and a higher chance of being caught.
- **Cover finance** (`race_market.py`). A cover that cannot be monetized is not
 a cover. We price the manipulated horse against an *honest* bookmaker's book
 under an overround, compute the value edge, and size the position by the
 Kelly criterion — which is also exactly the statistical signature a
 regulator would look for.

All mathematics is deterministic (no random draws), all data is fixed and
documented as model parameters, and every result surface — figures,
manuscript tokens, and mission outcomes — is computed from the same pure
core.

### Reader's guide

`chip_supply_chain.py`, `acquisition.py`, `mine_flood.py`,
`valley_impact.py`, `race_analytics.py`, and `race_market.py` (all under
`src/a_view_to_a_kill/`) are the mathematical core: pure functions with no
protocol imports, no I/O, and no randomness. `mission.py` adapts them to the
BOND-API contract — it is the only module that imports `bond_api`.
`manuscript_variables.py` computes the manuscript variable tokens that fill
this document, and `figures/plots.py` renders the five figures. The methods section develops all six models; The results section reports their
measured outputs; The scope section states what the models do and do not
claim.

## Methodology — MAIN STRIKE: the analytical models and algorithms that drive the mission

All six models are pure functions of fixed, documented datasets; no random
draws, no external state, no wall-clock dependence. The manuscript pipeline
that consumes them reads no clock either, so on one pinned interpreter every
rerun writes byte-identical artifacts — a checked property, not an aspiration
(the *Reproducibility* section names the gate). The three *structural* models come first
(supply-chain graph, flood dynamics, race form); the three *decision* models
that build on them follow (acquisition optimizer over the graph, valley-impact
coupling over the flood, cover finance over the form ratings).

### Implementation layering

The six models live in six independent modules under
`src/a_view_to_a_kill/`. A seventh module, `metrics.py`, fixes the mission
scenario (which firms are acquired, the flood parameters, the cover boost, the
bankroll) and evaluates each model once into a named metric group. `metrics.py`
imports no protocol types, so the entire scientific pipeline — the models, the
metric groups, the figures, and the manuscript token hydration — runs without
`bond_api` installed. `mission.py` is the only module that imports the
protocol; it wraps the same metric groups in the FROZEN `MissionProvider`
lifecycle and registers them as gadgets. Section results are therefore
identical whether reached through the protocol or through the pure core.

### Microchip supply-chain monopoly analysis

The supply chain is a directed graph of firms $V$ (nodes) and supply links
$E \subseteq V \times V$ (edges flowing forward through stages
`wafer, fabrication, assembly, distribution`). Each firm $v$ has a
throughput capacity $c_v$. The default dataset is a documented
reconstruction of the mid-1980s semiconductor market ($12$ firms,
$18$ links).

**Concentration.** Within a stage (or the whole graph), firm $v$'s capacity
share is $s_v = c_v / \sum_u c_u$, and the Herfindahl-Hirschman index is
$\mathrm{HHI} = 10000 \sum_v s_v^2$, ranging from $0$ (perfect competition)
to $10000$ (monopoly) — the antitrust codification of concentration [@hhi].
The default market opens at HHI $892.2$.

**Choke points.** Structural choke points are measured with Brandes'
betweenness-centrality algorithm [@brandes]: a firm's betweenness is the fraction of
ordered node pairs for which it lies on a shortest directed supply path.
Wafer sources carry zero betweenness by construction; the top choke point is
`amkor` (see the choke points figure).

**Single-source dependence.** A downstream firm whose only upstream supplier
is one firm is a single point of failure; such dependencies are the monopolist's
pressure points.

**Cascade failure.** Removing a set $R$ of firms (acquired-and-dismantled
competitors), a downstream firm is *starved* if it has no directed supply path
from any surviving wafer supplier — a standard reachability construction on
the supply digraph [@ast], and the mechanism the resilience literature calls
upstream disruption propagation [@christopher2004]. The starved fraction is
$\sum_{v \in S} 1 / |V|$. In the reported scenario $R$ is exactly the acquired
set `amd_fab, nec_fab`; the fabricators that remain in the graph after
that removal are `intel_fab, zorin_fab`.

**The ZORIN attack.** ZORIN owns `zorin_fab` and `zorin_assembly`; by
acquiring the independent fabricators `amd_fab, nec_fab` and
eliminating the rest of the market, his fabrication share rises to
$0.680$ and market-wide HHI jumps to $1528.9$.
Formally, `monopoly_share` computes ZORIN's surviving capacity share per
stage once every non-acquired independent is removed, and
`post_elimination_hhi` merges ZORIN's holdings into one entity before
recomputing concentration. This acquisition set is a *scenario* input
(`manuscript/config.yaml`), not the optimizer's output; The results section reports how far apart the two are.

### Flood-the-mine water-ingress dynamics

The mine is a network of chambers (nodes) and bidirectional tunnels (edges).
Chamber $i$ has volume $\Omega_i$, horizontal cross-sectional area $A_i$, and
elevation $z_i$; water level is $h_i = z_i + w_i / A_i$ where $w_i$ is the
water volume in the chamber. Tunnels have cross-sectional area $a_{ij}$.

Water enters at designated ingress chambers at total rate $Q$ (split evenly),
and flows through each tunnel from the higher-head end to the lower under a
simplified weir law

$$ q_{ij} = C\, a_{ij}\, \sqrt{\max(h_i - h_j,\, 0)}, $$

with discharge coefficient $C = 0.60$. Each timestep's tentative flows are
scaled so no chamber lends more water than it holds, making the scheme
**exactly mass-conserving**. State evolves by explicit Euler with timestep
$1.0$ s to horizon $900.0$ s at ingress
$10.0$ m$^3$/s. A chamber is *flooded* once
$w_i \geq \Omega_i$; `flooded_fraction` reports the share of chambers flooded
at a time $t$. `critical_ingress` picks the single entry that floods the most
of the network by the horizon. The default "Main Strike" network has
$8$ chambers and $10$ tunnels totalling
$9100$ m$^3$ (see the flood curve figure).

### Race-form analytics and cover model

Raw race records are normalized to a seconds-per-furlong pace corrected for
going (firm/soft) and weight carried:
$\tau = (t - g\, d - \max(w - 126,0)\,\epsilon\, d)/d$, with
$\epsilon = 0.02$ s per furlong per pound over the base
weight. The speed index is the seconds saved per furlong versus par,
$14.0 - \tau$. A horse's form rating is
the exponentially-weighted moving average of its speed indices, where a race
`age` before the newest is weighted $0.5^{\text{age}/\text{halflife}}$
(halflife $2.0$). Win probabilities follow a softmax
over ratings.

**Cover risk.** The stewards flag a horse whose performance improves by more
than $\theta = 1.0$ speed-index units above its own
baseline. With
$n$ races and natural race-to-race variability $\sigma$, the standard error of
the mean performance is $\sigma/\sqrt{n}$, so applying a boost $b$ gives a
detection risk

$$ \mathrm{risk}(b) = \Phi\!\left(\frac{b - \theta}{\sigma/\sqrt{n}}\right), $$The probability a normal draw with mean $b$ clears the threshold — the
detection-theoretic reading of stewards' scrutiny [@greenswets1966].
`cover_viability` returns `win_delta`, `detection_risk`, and
`expected_value = win_delta * PURSE - risk * DETECTION_PENALTY`, with
PURSE = 100000 and DETECTION_PENALTY = 900000
(both fixed in `race_analytics.py`). For the
$0.2$ boost to Pegasus (with
$\sigma = 0.5$) the risk is $0.001$ and
expected value $2924$ — a sustainable cover — whereas a
blatant boost is caught (see the race cover figure).

### Monopoly acquisition optimizer

The monopoly is a *selection* problem too: with a budget of
$K$ acquisitions (the acquisition curve figure), which independent fabricators
should ZORIN buy? The acquireable set is the $amd_fab, intel_fab, nec_fab$ fabricators
(owners other than ZORIN). Each budget-$K$ subset is scored by the objective
`post_elimination_hhi(chain, acquired)` (or by ZORIN's fabrication share),
and `optimal_acquisition` exhaustively searches over every $K$-subset with
deterministic tie-breaking. `greedy_acquisition` is the hill-climbing baseline
that adds the single firm giving the largest score gain at each step. Because
the exhaustive search is optimal, $\mathrm{greedy} \le \mathrm{optimal}$
always; in fact both objectives are *strategically monotone* — the marginal
gain of adding any candidate is its capacity times a factor common to all
candidates — so $\mathrm{greedy} = \mathrm{optimal}$ holds on every market,
not merely on this dataset (verified exhaustively in `test_acquisition.py`); with the default budget of 2 the optimal acquisition
(`intel_fab, nec_fab`) lifts HHI from 1012.8 to
1741.4, a gain of 728.6 over buying nothing, while the
greedy baseline reaches 1741.4 (regret 0.0). The same
optimality argument bounds the *scenario* acquisition
(`amd_fab, nec_fab`) from above, which is how The results section
scores the scheme's shortfall; the optimizer is a bound on the scenario, not a
description of it.

### Valley impact — the flood's urban blast-reach

ZORIN's sabotage is not the flood but its *consequence*. Each surface
fabrication plant (a `SurfaceFab`) is hydraulically coupled to a mine chamber;
water in that chamber raises the local water table by the fab's `leakage`
coefficient, and the fab becomes inoperable when that table reaches its
`foundation_elevation` — the coarse form of the groundwater-inundation damage
relation [@kreibich2008]:

$$ \mathrm{table}_{f}(t) = \ell_f \cdot h_{c(f)}(t), \qquad \text{inoperable if }
 \mathrm{table}_{f}(t) \ge z_f. $$

`valley_capacity_loss` reports the fraction of total fabricating capacity
inoperable by a decision time — for the default scenario 3
of 5 fabs (0.583 of capacity) by the horizon
(see the valley impact figure). The 2 survivors are
`nec_fab, zorin_fab`: `zorin_fab` endures because it sits over the
low-coupling, high-separation `shaft_a`, which is the outcome the scheme
intends. The survivor and victim sets are determined purely by coupling
geometry, not by ownership, and the two directions come out differently: no
plant outside ZORIN's control survives
(0 such survivors), but
`amd_fab` — a plant he acquires — is destroyed anyway.

### Racing betting market and cover finance

The cover is financed by betting on the controlled horse. `cover_bankroll`
takes the EWMA **form ratings** (a boost is in speed-index units, so it can
only be applied to a rating) and derives both sides of the trade from the same
softmax. The honest book is priced off the *un-boosted* win probabilities
$p_i = \mathrm{softmax}(r)_i$: `market_odds` converts them into decimal odds
under a bookmaker overround $\nu = 1.12$ — the standard
way an outcome model is priced against a book [@dixon] — so the market's
implied probabilities sum to $\nu$: $q_i = p_i \nu$,
$\mathrm{odds}_i = 1/q_i$. Against that *honest* book, `cover_bankroll` prices
the manipulated horse using its boosted true probability
$p^\ast = \mathrm{softmax}(r + b e_{\text{Pegasus}})_{\text{Pegasus}}$, so the
edge measures the boost rather than a change of probability model: the value
edge is $p^\ast \mathrm{odds} - 1$, the
Kelly-optimal stake fraction is
$(p^\ast \mathrm{odds} - 1)/(\mathrm{odds} - 1)$ when positive, and the
expected profit is the edge times the staked bankroll. For Pegasus under a
$0.2$ boost the true probability
(0.248) exceeds the market-implied (0.238),
giving a positive edge (0.0415) and a Kelly stake of
1298 — precisely the anomaly that the cover-risk model of
`race_analytics` would eventually flag [@kelly1956].

## Results — MAIN STRIKE: measured outcomes, headline numbers, and what they establish

All figures and numeric results below are generated from the pure core by
`scripts/z_generate_manuscript_variables.py`; no number is hand-authored.

### Supply-chain monopoly

![Choke-point betweenness by firm](output/figures/a_view_to_a_kill_choke_points.png)

Table: Supply-chain concentration under the ZORIN attack.

| Metric | Value |
|---|---|
| Firms / supply links | 12 / 18 |
| Market-wide HHI (pre-attack) | 892.2 |
| Market-wide HHI (post-elimination, 2 fabs acquired: `amd_fab, nec_fab`) | 1528.9 |
| ZORIN fabrication capacity share | 0.680 |
| Top choke point (betweenness) | amkor |
| Starved fraction when the acquired fabs are dismantled (`amd_fab, nec_fab`) | 0.000 |

Acquiring `amd_fab, nec_fab` lifts market concentration from
HHI 892.2 to 1528.9 and hands ZORIN
0.680 of fabrication capacity — a decisive corner on the
market. The cascade model removes exactly the acquired-and-dismantled firms
(`amd_fab, nec_fab`); the fabricators left standing
(`intel_fab, zorin_fab`) still carry wafer supply through to every
assembly house, so nothing downstream is starved (starved fraction
0.000, starved firms: none). That is
the monopolist's intent: competitors are *removed*, but the market ZORIN owns
keeps flowing (the choke points figure).

### Flood-the-mine water ingress

![Flooded fraction of Main Strike over time](output/figures/a_view_to_a_kill_flood_curve.png)

At $10.0$ m$^3$/s into the `adit`, the Main Strike
network (8 chambers, 10 tunnels,
9100 m$^3$) floods $0.625$ of its chambers by
$900.0$ s; the lowest working (`vault`) is submerged at
$310.0$ s (the flood curve figure). The critical single ingress
point is `adit`. The simulation conserves water mass to
$1.2e-15$ — machine precision.

### Race-form cover analytics

![Race-card form ratings by horse](output/figures/a_view_to_a_kill_race_cover.png)

Over $20$ records ($5$ horses, $2.0$
halflife), the strongest form is `Silverado`
(form rating 0.808); Pegasus opens at win probability
0.213 (the race cover figure). A $0.2$
speed-index boost to Pegasus buys win probability `+0.035` while
carrying only $0.001$ detection risk, for a positive
expected value of $2924$ — a sustainable cover. Pushing
the boost toward the detection threshold collapses expected value as the
scheme is caught (see the methodology analysis in The methods section).

### Monopoly acquisition

![Optimal monopoly HHI by acquisition budget](output/figures/a_view_to_a_kill_acquisition_curve.png)

Table: Acquisition optimizer on the default market (budget 2).

| Metric | Value |
|---|---|
| Acquireable independent fabricators | amd_fab, intel_fab, nec_fab |
| Baseline HHI (buy nothing) | 1012.8 |
| Optimal acquired | intel_fab, nec_fab |
| Optimal HHI | 1741.4 |
| HHI gain vs baseline | 728.6 |
| Greedy baseline HHI | 1741.4 |
| Greedy regret | 0.0 |

The exhaustive optimum (the acquisition curve figure) lifts concentration from
1012.8 to 1741.4 with just 2
acquisitions. Greedy is exact here (regret 0.0) — and this is
*not* a happy accident of this dataset. Both acquisition objectives are
*strategically monotone*: the marginal gain of adding any fabricator is that
fabricator's capacity times a factor common to every candidate, so greedy is
provably optimal on *every* market, not merely this one (a proof sketch and an
exhaustive deterministic counterexample probe live in `test_acquisition.py`).
The exhaustive optimizer's remaining value is as a correctness oracle and as
the upper bound against which the scenario's shortfall is scored; the headline
remains the *scale* of the concentration a 2-firm buy achieves.

#### Scenario versus optimizer

The scenario ZORIN actually executes and the answer this package's optimizer
returns are **not the same set**, and the difference is a result, not an
oversight. The film-faithful scenario buys `amd_fab, nec_fab`
(2 firms), scoring HHI 1528.9 and a
fabrication share of 0.680. On the same objective and the
same budget, the exhaustive optimum is `intel_fab, nec_fab` at
1741.4 and a share of 0.820. The scenario is
therefore strictly suboptimal by 212.5 HHI points.

We report this rather than reconcile it away. The package makes **no claim
that ZORIN's acquisition is optimal**; every scenario-conditioned number in
this manuscript (the HHI, share, cascade, and valley results above) is
conditioned on the acquisition set fixed in `manuscript/config.yaml`, not on
the optimizer's answer. The optimizer's role is to bound what the same market
would have permitted — and the bound says the scheme leaves
212.5 points of concentration on the table.

### Valley impact

![Silicon-valley fabricating capacity lost to the flood](output/figures/a_view_to_a_kill_valley_impact.png)

Table: Urban blast-reach of the flood at the decision horizon.

| Metric | Value |
|---|---|
| Valley fabs | 5 |
| Capacity loss (fraction inoperable) | 0.583 |
| Inoperable fabs | 3 |
| Victims | amd_fab, intel_fab, silicon_valley_fab |
| Survivors | nec_fab, zorin_fab |
| Survivors ZORIN acquires | nec_fab |
| Survivors ZORIN neither owns nor acquires | none |
| Victims ZORIN acquires | amd_fab |
| Victims ZORIN neither owns nor acquires | intel_fab, silicon_valley_fab |

By the horizon the flood's groundwater reach has disabled 3
of 5 valley fabrication plants — 0.583 of total
fabricating capacity (the valley impact figure) — leaving
2 operable: `nec_fab, zorin_fab`. ZORIN's own
`zorin_fab` is among them, sitting over the low-coupling `shaft_a` and
protected from the very flood he releases.

The victim list (`amd_fab, intel_fab, silicon_valley_fab`) is the more interesting result, because
coupling geometry alone decides who drowns. The split by ownership is one-sided.
On the losing side the flood is *not* discriminating: `amd_fab`
is destroyed even though ZORIN buys it, alongside the plants he never
acquires (`intel_fab, silicon_valley_fab`). On the surviving side it is
entirely discriminating: the survivors are ZORIN's own plant plus
`nec_fab`, which he acquires, and the number of
surviving plants he neither owns nor acquires is
0
(`none`). So the model contradicts the scheme's own
premise in exactly one direction: the flood spares no rival, but it does
destroy an asset ZORIN pays for — the acquisition plan and the sabotage plan
are not automatically consistent with each other.

Both directions of that claim are computed set operations
(`valley_metrics`), and `tests/test_manuscript_variables.py::test_valley_ownership_split_matches_the_manuscript_claim`
fails if either one stops holding, so this paragraph cannot outlive the data
it describes.

### Cover finance

The betting-market model prices the cover against an honest 1.12
overround book. Table: cover-bankroll plan for `Pegasus`.

| Metric | Value |
|---|---|
| Bankroll | 100000.0 |
| Boosted true win probability | 0.248 |
| Market-implied probability | 0.238 |
| Value edge per unit | 0.0415 |
| Kelly fraction | 0.0130 |
| Kelly stake (USD) | 1298 |
| Expected profit (USD) | 54 |

The manipulated horse's true probability (0.248) exceeds the
market-implied (0.238) by an edge of 0.0415 per unit
staked, which justifies a Kelly stake of 1298 against the
100000.0 bankroll. Both probabilities come from the *same*
softmax over form ratings — the honest book prices the un-boosted ratings and
the true chance prices the boosted ones — so the edge measures the boost and
nothing else. That a single horse's true chance exceeds the honest market's
price is exactly the statistical anomaly the cover-risk model would flag: the
cover is profitable only while it stays undetectable.

## Conclusion — MAIN STRIKE: findings, verdict, and what the mission establishes

This package demonstrates that a film's elaborate scheme can be reduced to a
deterministic, testable computational model without losing its substance.
ZORIN's monopoly is a concentration and choke-point problem *and* a budgeted
acquisition-selection problem; his flood is a mass-conserving network-dynamics
problem whose urban blast-reach is a coupling problem over the fabs above; his
cover is a signal-detection trade-off *and* a betting-market finance problem.
Each of the six is implemented as a pure domain module with a matching
real-data test file, aggregated by a protocol-free metric layer, and wrapped in
a thin `MissionProvider` adapter that speaks the FROZEN BOND-API protocol.

That layering is load-bearing rather than cosmetic. Because only the adapter
imports `bond_api`, the science — the six models, the metric groups, the
figures, and this manuscript's own numbers — runs whether or not the protocol
dependency is present, and a test proves it by blocking the import and
recomputing. The claim and the code are checked against each other rather than
asserted in prose.

The result is a mission that *runs*: `mission_brief` / `mission_recon` /
`mission_plan` / `mission_execute` / `mission_debrief` drive the full lifecycle
from the command line, every metric is computed rather than stubbed, and every
number in this document — including the structural model constants — arrives as
a token from the same pure core. The package meets the PROJECT BOND guardrails:
at least 90% line and branch coverage on `src/`, zero mocks, deterministic
seeds, ruff and mypy clean, no leftover exemplar-lineage strings, and a clean
git tree.

## Experimental Setup — MAIN STRIKE: canonical scenarios, parameters, and configuration

All experiments are deterministic and fully prescribed by
`manuscript/config.yaml`, whose `experiment:` block is loaded by
`src/a_view_to_a_kill/manuscript_variables.py`, converted to a
`metrics.MissionScenario`, and threaded into the models that produce every
computed token below. Editing a knob here changes the results, not only the
echo of the file — `tests/test_metrics_scenario.py` fails if any knob is
inert.

### Fixed model data

The datasets are hard-coded, documented model parameters in the pure core and
annotated in `data/claim_ledger.yaml`:

- **Supply chain** (`chip_supply_chain.py`): 12 firms across the
 stages `wafer, fabrication, assembly, distribution` with 18
 forward-flowing supply links; per-firm capacities fixed in the module. The
 acquisition optimizer (`acquisition.py`) derives its candidate set from this
 same graph — the amd_fab, intel_fab, nec_fab non-ZORIN fabricators — so it adds no
 dataset of its own.
- **Mine network** (`mine_flood.py`): 8 chambers with
 volume/area/elevation, 10 tunnels with cross-sectional area;
 total capacity 9100 m$^3$.
- **Valley fabs** (`valley_impact.py`): 5 surface fabrication
 plants, each with a capacity, a coupled mine chamber, a foundation elevation
 (m above datum), and a hydraulic leakage coefficient in $[0, 1]$.
- **Race card** (`race_analytics.py`): 20 form records
 (5 horses x 4 races) with distance,
 going, weight, and time.
 The betting market (`race_market.py`) is derived from the resulting win
 probabilities under the configured overround — again, no separate dataset.

### Simulation parameters

Scenario knobs come from `manuscript/config.yaml`; structural model constants
(discharge coefficient, Euler timestep, detection threshold, par pace, base
weight, purse, penalty, seed) are defined in the pure modules. Both are
surfaced here as computed tokens, so neither can drift from the code.

- Flood ingress rate: 10.0 m$^3$/s, horizon
 900.0 s, Euler timestep 1.0 s, discharge
 coefficient 0.60.
- Race-form EWMA halflife: 2.0 races.
- Cover boost to Pegasus: 0.2 speed-index units; natural
 race-to-race variability 0.5; detection threshold
 1.0.
- Acquisition budget: 2 independent fabricators.
- Scenario acquisition set (what ZORIN actually buys, distinct from the
 optimizer's answer): `amd_fab, nec_fab`.
- Cover betting bankroll: 100000.0 USD; bookmaker overround
 1.12.
- Mission RNG seed: 1985 (fixed; no randomness is ever drawn).

### Software environment

- Python 3.14.6
- numpy, matplotlib, PyYAML; BOND-API protocol via path dependency
- Manuscript source date 2026-08-04, declared in
 `manuscript/config.yaml`. The generator reads no wall clock, so this line —
 like every other line — is the same on every rerun.

## Reproducibility — MAIN STRIKE: verification gates, deterministic regeneration, and artifacts

### Determinism

Every module is a pure function of fixed data with no random draws and no
wall-clock dependence in its computed outputs. `Provenance.seed` is fixed at
1985; the mission outcome's `input_hash` is a SHA-256 of the canonicalized
plan, so an outcome can be audited without rerunning the film. The flood
simulator is byte-deterministic across identical calls
(`test_mine_flood.py::test_simulation_is_deterministic`), and the mission
report is byte-identical across two `run_mission` calls
(`test_mission.py::test_full_mission_flow_is_deterministic`).

The same holds for the *persisted* artifacts, and this is the load-bearing
claim of this section: running
`scripts/z_generate_manuscript_variables.py` twice on one pinned interpreter
writes byte-identical `output/data/manuscript_variables.json`,
`output/manuscript/*.md`, and `output/figures/*.png`. Nothing in the pipeline
reads a wall clock. The manuscript's provenance date (2026-08-04) is
`paper.date` from `manuscript/config.yaml` — a committed value that moves only
when an author moves it — and the only other environment-derived token is the
interpreter version (3.14.6), which is fixed for a given
toolchain. `tests/test_regeneration_determinism.py` enforces this the only way
that can fail honestly: it runs the real generator twice, in two separate
processes, with more than a second of real time between them, and diffs the
bytes. It does **not** inject a fixed clock — an injected `now=` would prove
only that a fixed input yields a fixed output, and an earlier version of this
package carried exactly that test while a `datetime.now` stamp moved
`05_experimental_setup.md` on every run.

### Artifacts

Running the pipeline reproduces every artifact from source:

```bash
uv run python scripts/mission_brief.py # brief
uv run python scripts/mission_recon.py # recon
uv run python scripts/mission_plan.py # plan
uv run python scripts/mission_execute.py # execute
uv run python scripts/mission_debrief.py # debrief
uv run python scripts/z_generate_manuscript_variables.py # tokens + figures
```

`z_generate_manuscript_variables.py` writes
`output/data/manuscript_variables.json`, the substituted manuscript to
`output/manuscript/`, and the five figures (`choke_points`,
`acquisition_curve`, `flood_curve`, `valley_impact`, `race_cover`) to
`output/figures/`. `output/` is git-ignored (regenerable). The live test count
and achieved coverage are tracked in `docs/_generated/COUNTS.md`.

### Where the numbers come from

No metric in this manuscript is written by hand. Every numeral in the prose,
tables, and captions is a double-brace variable token resolved by
`src/a_view_to_a_kill/manuscript_variables.py`, which reads
`manuscript/config.yaml`, turns its `experiment:` block into a
`metrics.MissionScenario`, and calls `metrics.run_mission_metrics(scenario)`
for the computed results. It calls **`metrics`**, not `mission`: importing
`mission` would pull in `bond_api` and break the very fallback this section
asserts below. Five gates keep this honest:

- `resolve_manuscript_tree(..., strict=True)` refuses to emit a section that
 still contains an unresolved variable token.
- `tests/test_manuscript_variables.py::test_every_manuscript_token_is_generated`
 fails if any token used in prose is missing from `generate_variables`, and
 `test_strict_gate_rejects_each_empty_metric_group` proves the strict gate
 actually fires when any one metric group is empty.
- `tests/test_metrics_scenario.py::test_every_scenario_knob_moves_a_metric`
 fails if any `experiment:` knob is inert — i.e. if changing it in the config
 leaves every computed token unchanged. A knob that is only echoed back as a
 `CONFIG_*` token is a reported-but-unused parameter, and this gate is what
 makes "prescribed by `config.yaml`" a checkable statement rather than a
 claim.
- `tests/test_metrics_scenario.py::test_default_scenario_matches_the_config_file`
 pins `metrics.DEFAULT_SCENARIO` to `manuscript/config.yaml`, so the code
 default and the config cannot drift into two answers.
- `tests/test_claim_ledger.py` proves `data/claim_ledger.yaml` records only
 token *names* and no frozen numerals, so the ledger cannot become a second,
 ungated source of truth for a metric.

### Guardrails check

- Test coverage >= 90% line + branch on `src/` (verified by
 `uv run pytest tests/ --cov=src --cov-fail-under=90`).
- Zero mocks: tests use real computation and real data only.
- No `infrastructure.*` imports in `src/`. The pure core, the metric layer,
 the figures, and this manuscript pipeline are importable without `bond_api`
 — verified by `tests/test_bond_api_fallback.py`, which blocks the import
 with a real meta-path finder and recomputes, with a positive control proving
 the blocker bites and a negative control confirming the adapter alone
 requires the protocol.
- No leftover template-scaffold lineage strings (`rg` gate clean).

## Scope and Related Work — MAIN STRIKE: boundaries, positioning, and relationship to the literature

### Scope

This package models the *structure* of ZORIN's scheme, not its implementation
in the physical world. The supply chain is a stylized capacity graph; the
acquisition optimizer is a combinatorial abstraction of a corporate-control
market with no price model; the mine flood is a simplified head-driven weir
model; the valley coupling is a single-coefficient proxy for a groundwater
transport model; the race cover is a signal-detection abstraction of stewards'
scrutiny; and the betting market is an idealized book with a uniform overround
and no liquidity, stake limits, or price impact. The datasets are fixed,
documented model parameters (historical-company names for the supply chain,
fictionalized gallery geometry for the mine, a reconstructed race card) — they
are illustrative model inputs, not measured field data. No claim is made about
the real historical microchip market's exact shares, about any real mine, or
about any real racing jurisdiction; the value of the package is the
deterministic, reusable mathematics, and the fact that every number reported
here is computed by the tested code rather than asserted in prose.

Two limits are worth stating explicitly. First, the acquisition optimizer is
exhaustive over budget-sized subsets — $\binom{n}{K}$ work — which is
tractable at this problem's scale and deliberately chosen: its purpose is to
be the *correct* oracle against which the greedy baseline's regret is
measured, not to scale. Second, the valley coupling is monotone in chamber
head, so it can order which plants fall and when relative to each other, but
its absolute inundation times inherit the weir model's simplifications and
should not be read as an engineering prediction.

#### Uncertainty

The package reports deterministic point estimates, not distributions: no
quantity carries a confidence interval. That is a design property, not an
oversight — the models are exactly reproducible given the fixed datasets and
scenario (byte-identical reruns are themselves a checked gate), but
reproducibility is a statement about the *computation*, not about the
real-world phenomena the film's scheme gestures at. Every result is conditional
on the scenario knobs in `manuscript/config.yaml` and on the documented model
datasets (capacities, gallery geometry, elevations, race times); change a knob
or a datum and the numbers move, which is precisely why each one is surfaced as
a token rather than a frozen numeral, and why sensitivity is exercised by
re-running the prescribed experiment under an alternative `experiment:` block
rather than by reading a delta off this page. In particular the flood
inundation times, the valley victim/survivor split, and the cover-detection
probability are all model-conditioned and should not be read as engineering or
actuarial predictions.

### Related work

- **Concentration and choke points.** The Herfindahl-Hirschman index is the
 standard antitrust concentration measure, codified in the U.S. *Horizontal
 Merger Guidelines* [@hhi]. Betweenness centrality follows Brandes' algorithm
 [@brandes]. Supply-chain cascades relate to the supply-chain resilience
 literature, which models how upstream disruption starves downstream
 production [@christopher2004]; the reachability formulation used for the
 cascade is a standard network-flow construction [@ast].
- **Acquisition as combinatorial selection.** Choosing which competitors to
 buy under a budget is subset selection against a set objective. We report
 the exhaustive optimum alongside a greedy baseline because greedy heuristics
 on such objectives carry no *general* optimality guarantee. On the two
 objectives shipped here the guarantee actually holds: both are strategically
 monotone, so greedy is exact by construction and the regret is provably zero
 for every market — verified exhaustively over a deterministic counterexample
 grid in `test_acquisition.py`. The exhaustive path remains the correctness
 oracle and the upper bound the scenario is scored against.
- **Network water flow.** The weir/head-driven flow law used here is a
 simplification of the open-channel flow models used in flood and mine
 drainage engineering; the key property preserved is exact mass conservation.
- **Groundwater damage to built assets.** Coupling a subsurface water level to
 the operability of structures above follows the groundwater-inundation
 damage literature, which relates elevated water tables to damage in
 foundations and basements [@kreibich2008].
- **Racing form and detection.** Normalized speed handicapping and softmax
 outcome models are standard in racing and sports-outcome analytics
 [@dixon]; framing manipulation as a signal-detection trade-off draws on
 classical detection theory [@greenswets1966].
- **Bet sizing.** The staking rule is the Kelly criterion — the
 expected-log-growth-optimal fraction of a bankroll to stake on a bet with a
 known edge [@kelly1956].

Within the PROJECT BOND suite, this package is one of the film packages
implementing the FROZEN `bond_api.MissionProvider` protocol; its pure core
constitutes the local scientific content that the protocol wraps.

## Sources — MAIN STRIKE: bibliography

@brandes; @hhi; @film; @dixon; @ast; @kelly1956; @christopher2004; @kreibich2008; @greenswets1966


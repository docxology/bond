# Licence to Kill (1989) — WAVEKREST

*film package · package codename WAVEKREST*. Mission **ROGUE**: detect layering and integration in the Sanchez money-laundering network; forensic anomaly scan of the Wavekrest-class mothership; risk-optimised rogue-00 engagement plan under a revoked licence; quantify narcotics-finance economics and cash-manifest feasibility; route the operation and select the gadget loadout under risk and weight; schedule covert actions against adversary watchlist accumulation.

## Concepts — WAVEKREST: domain and operational focus

narcotics finance, rogue ops

## Abstract — WAVEKREST: mission summary

Licence to Kill: ROGUE — Special-Agent Mission Software for Laundering-Graph, Vessel-Forensic, Rogue-Policy, Narcotics-Finance, Logistics, and Surveillance Analysis — Six deterministic domains — graph detection, marine physics, dynamic programming, cash economics, risk-adjusted routing, and survival-optimal scheduling — behind one unsanctioned operation — is a deterministic, fully-tested special-agent mission software package implementing the ROGUE mission from the film *Licence to Kill* (1989). Six interoperating domain models sit behind the frozen BOND-API `MissionProvider` protocol. The first three answer the field analyst's original questions: 1. a **money-laundering graph** model of the Sanchez cartel's placement–layering–integration flow, with cycle, funnel, and dirty-flow detectors; 2. **first-principles vessel forensics** of the Wavekrest-class mothership from marine physics (IMO gross tonnage, hydrostatic displacement, fuel endurance, route plausibility); 3. a **rogue-00 operation risk model** in which an operator whose licence has been revoked must trade mission gain against escalating adversary alert and blowback, solved exactly by finite-horizon dynamic programming. The remaining three carry the campaign from the ledger into the world: 4. **narcotics-finance economics** — the supply-chain price/purity ladder and the cash physics (mass, volume, hold manifest) behind the cartel's US$5,000,000 courier parcel; 5. **operations logistics** — risk-adjusted Dijkstra routing of the Wavekrest campaign, exact 0/1-knapsack gadget loadout, and trip projection against fuel endurance; 6. **surveillance / watchlist** — a logistic detection model over a covert action sequence, with exact and heuristic survival-optimal ordering. On the canonical seeded network (codename ROGUE, seed 0) the analysis detects 1 money-returning cycle(s) and 16 funnels across 22 nodes and and 89 directed edges, with 720 layering chains (the exact count) enumerated — a composite layering score of 0.513 and an integration score of 0.653. profile resolves a gross tonnage of 356 and flags 2 forensic anomalies (score 2.0). The rogue-00 dynamic program over 10 steps returns an optimal expected mission value of 1.665 with a stealth opening, closing on overt — evidence that, under a revoked licence, unsanctioned escalation is strictly a last resort, worth taking only when there is no remaining horizon left to protect. The layered logistics route cuts cumulative interdiction risk by 30.7% versus the direct leg (0.208 vs 0.300), and the covert campaign's survival-optimal sequence completes undetected with probability 0.263 before watchlist compromise at action 5. Every result is deterministic and reproducible: fixed seed, no random draws in the detectors, no wall-clock in persisted outputs, and ≥ 90% line + branch test coverage on the source tree.

## Introduction — WAVEKREST: mission framing, the operational problem, and how to read this chapter

### The ROGUE mission

In *Licence to Kill* (1989) an operator pursues the drug lord Franz Sanchez
after his 00 licence is revoked, assembling an unsanctioned campaign that
moves from the street level of the cartel's cash economy, through the
Wavekrest-class mothership used to smuggle the proceeds, to a final
confrontation. This package formalises that campaign as a research problem:
a *special-agent mission* whose analytical core quietly mirrors the six
things a field analyst must actually determine. The first three concern what
the adversary is doing.

1. **Where is the money going?** The cartel's value is laundered in the
 textbook three stages — *placement* of cash, *layering* through a web of
 intermediaries, and *integration* into legitimate banks. We model this as
 a directed financial-flow graph and build deterministic detectors that
 score how heavily the structure is being layered and how dilute the dirty
 value has become (Section 2, `src/licence_to_kill/laundering_graph.py`).
2. **Is the mothership lying about what it carries?** A fishing vessel
 cannot silently move contraband without its own physics giving it away
 — a hold full of something denser than fish, a draft that disagrees with
 the declared displacement, a fuel budget that cannot cover its route. We
 compute those quantities from first principles
 (`src/licence_to_kill/vessel_forensics.py`).
3. **What should the operation do next?** With a revoked licence the
 operator has no sanctioned exit; every action escalates the adversary's
 alert level and precipitates blowback. We solve the optimal engagement
 policy exactly with dynamic programming
 (`src/licence_to_kill/rogue_ops.py`).

The remaining three concern what the operation itself can physically afford.

4. **How much money is actually moving, and can it move?** The film opens on
 an intercepted courier carrying a cash parcel. A supply-chain price and
 purity ladder says what that value represents in product; US-currency note
 physics say what it weighs and how much hold it occupies, and therefore
 whether one hull can carry it at all
 (`src/licence_to_kill/narcotics_finance.py`).
5. **By what route, carrying what?** Legs between the operational hubs trade
 distance, dollar cost, and interdiction risk against each other, and a
 weight-bounded gadget loadout has to be chosen before departure. Both are
 classical optimisation problems solved exactly — shortest path over a
 risk-additive weight, and 0/1 knapsack
 (`src/licence_to_kill/operations_logistics.py`).
6. **How long before the operator is burned?** Every covert action teaches
 the adversary's watchlist something. Survival to the end of the campaign
 is a product of per-step non-detection probabilities, and the only free
 variable is the order in which the actions are taken
 (`src/licence_to_kill/surveillance.py`).

The six are deliberately coupled at the scenario level rather than in code:
the Wavekrest-class hold sized in Section 2.2 is the same hold the cash
manifest must fit in Section 2.4 and the same hull whose endurance bounds
the voyage in Section 2.5, because all three read the one canonical
parameter set.

### Design principles

The package follows the BOND guardrails exactly. The six domain modules are
*pure* — infrastructure-free and bond-api-free, importable in any Python 3.10+
environment (verified by `tests/test_mission.py`). The `MissionProvider`
adapter in `src/licence_to_kill/mission.py` is the only module that touches
the frozen `bond-api` protocol, and it simply wires the domain results into
the five-stage mission lifecycle (brief → recon → plan → execute → debrief).
Everything is deterministic: the network is built from a seeded generator,
the forensic physics are closed-form, the dynamic program is exact backward
induction with no Monte Carlo, the routing and knapsack solvers are exact,
and the survival-optimal action order is found by exhaustive permutation
search at this problem size.

Each domain also exposes a `canonical_*_params` function that is the sole
declaration of its scenario. The mission adapter, the manuscript token
generator, and the figure generators all read those functions rather than
carrying their own copies, so a figure cannot depict a scenario the prose
does not describe.

This manuscript is produced from `manuscript/config.yaml` and
`src/licence_to_kill/manuscript_variables.py`: every numeric value in the
prose is injected as a generated token and never hand-authored.

## Methodology — WAVEKREST: the analytical models and algorithms that drive the mission

This section specifies the six deterministic algorithms that constitute the
ROGUE analytical core. Deep familiarity with each module's source is the
intended reader path: `src/licence_to_kill/laundering_graph.py`,
`vessel_forensics.py`, `rogue_ops.py`, `narcotics_finance.py`,
`operations_logistics.py`, and `surveillance.py`.

Every declared constant below is reported as an injected token drawn from
that module's `canonical_*_params` function or its named module constants,
so changing a parameter in source rewrites this section rather than silently
contradicting it.

### 2.1 Money-laundering graph

A laundering network is a directed, weighted graph
$G = (V, E)$ whose nodes $V$ are financial entities (collectors, shell
fronts, seafood/currency fronts, banks, legitimate exporters) and whose
directed edges $E$ carry a positive value flow. Dirty value is *placed* at
source nodes, moves through the graph, and *integrates* at sink nodes.

**Cycle detection.** Money-returning loops are the signature of layering.
We enumerate elementary cycles by depth-limited depth-first search, rotating
each discovered cycle to a canonical form (start at its lexicographically
smallest node) so duplicates collapse (`TransactionGraph.find_cycles`).

**Funnel analysis.** A node is a *collector* when it fans in from ≥ 2 unique
sources with a degree-imbalance ratio
$\rho = (\text{sources}+1)/(\text{targets}+1) \geq \tau$, and a
*distributor* when it fans out to ≥ 2 unique targets with $\rho \leq 1/\tau$
($\tau = 1.5$). Trivial linear pass-throughs are
excluded.

**Dirty-flow propagation.** Dirty mass is conservatively re-distributed
along edges in proportion to edge weight; a node with no out-edges retains
its mass (it is a sink). Iteration converges to the pooling dirty
distribution (`TransactionGraph.propagate_dirty`). From it we derive the
per-sink dirty fraction
$d_i = \text{dirty}_i / \text{in\_amount}_i$, the integration score
$1 - \bar{d}$ (how diluted the placed value has become), and the Shannon
entropy of the dirty distribution across sinks (how dispersed it is)
[@shannon1948].

**Composite layering score.** Three normalised components — cycles,
layering-chain depth, and funnel imbalance — are blended
$0.4\cdot C_\text{cyc} +
0.3\cdot C_\text{depth} +
0.3\cdot C_\text{funnel}$ into a single score in
$[0, 1]$ (`analyze_laundering`). The weights are declared as
`LAYERING_WEIGHTS` in source and injected here; they are heuristic, and
Section 7 says so.

### 2.2 Vessel forensics

For a declared `VesselProfile` of the Wavekrest-class mothership we compute,
from first principles:

- **Enclosed hull volume** $V = L \cdot B \cdot D \cdot C_b$.
- **Gross tonnage** (IMO 1969): $\mathrm{GT} = K_1 V$ with
 $K_1 = 0.2 + 0.02 \log_{10} V$.
- **Hydrostatic displacement** $\Delta = \rho_\text{sw} \cdot L \cdot B \cdot
 \text{draft} \cdot C_b$, $\rho_\text{sw} = 1.025\
 \text{t/m}^3$, $C_b = 0.62$.
- **Fuel endurance**: at speed $v$ the required shaft power follows the
 cubic law $P(v) = P_\text{max}(v/v_\text{max})^3$, burning
 $P(v) \cdot \text{SFC}$ kg/h (SFC = 0.195 kg/kWh), giving
 range $\text{nm} = (\text{fuel mass}/\text{burn rate}) \cdot v$.

The forensic scan (`anomaly_scan`) then flags physical implausibilities: a
cargo bulk-density above the fish ceiling
(1.4 t/m³), a declared displacement more than
15% from the draft-predicted value (hidden
ballast), a route whose required average speed exceeds capability, a voyage
beyond the fuel endowment, or an over-powered hull. The scan deliberately
does *not* trap errors from the underlying physics: a profile that cannot
support an endurance computation raises rather than being scored as
anomaly-free, because "no anomaly" and "could not check" are different
findings and only one of them is safe to report.

### 2.3 Rogue-00 risk model

A revoked licence means the operator faces a finite-horizon control problem.
State is $(a, e)$: adversary *alert* and cumulative *exposure*. Each step the
operator picks an intensity $i \in \{\text{stealth}, \text{covert},
\text{overt}\}$ with gain $g_i$ and visibility $v_i$; alert rises
$a \leftarrow \min(a_\text{max}, a + v_i)$, exposure rises by one step, and
*blowback* (a retaliatory strike destroying the period's value) arrives with
logistic hazard
$p = \sigma(\beta_0 + \beta_a a + \beta_e e)$.

We solve exactly by backward induction over the discrete
$(\text{step}, a, e)$ lattice (`solve_optimal_policy`), producing the
expected optimal value, the first-period action, and the escalation curve
that follows. No randomness is involved — the result is reproducible to the
last float.

Both state dimensions are quantised: exposure onto 21
cells and alert onto the integers $0..10$. The visibility
ladder is therefore truncated onto the alert lattice by a single shared
transition (`next_alert`), which the projection and valuation functions use
as well. That sharing is what makes the model self-checking: replaying the
DP's own optimal action sequence through `expected_value_of_policy` must
reproduce `optimal_value` exactly, and the test suite asserts it does. A
model whose optimiser and whose reported trajectory used different
transitions would pass every individual test and still describe a process
nobody optimised.

### 2.4 Narcotics-finance economics

The money behind the cartel is modelled in `narcotics_finance.py` in two
layers. First, the **supply chain**: a base production cost per kilogram is
multiplied through the distribution stages (export → wholesale → street) to
give the stage prices (export → wholesale → street), and purity adjustment divides
the retail price by the purity fraction so unit economics are stated per
*pure* gram (`price_chain`, `purity_adjusted_price`). Second, the **cash
itself**: using the mass and volume of a US currency note
(1.0 g, 1.13 cm³ [@bep_currency]), we
convert a parcel's value into whole notes, kilograms of mass, and cubic
metres of volume (`cash_mass_kg`, `cash_volume_m3`), then check whether that
parcel physically fits the Wavekrest-class hold — volume *and* mass — and
how many trips it needs (`manifest_feasibility`, `trips_required`). Note
counts round up: a partial note cannot be carried, so the conservative
direction is the only defensible one for a feasibility check.

### 2.5 Operations logistics

The physical campaign is planned in `operations_logistics.py`. The
5 transport legs between the film's 4
hubs (Isthmus City, Bogota, Hong Kong, Florida) each carry a distance, a
dollar cost, and an interdiction risk. `shortest_path` runs Dijkstra's
algorithm [@dijkstra1959] over one of three additive weights; for risk the
per-leg weight is $-\ln(1-r)$ so the cumulative survival product becomes a
sum and the returned route minimizes the honest $1-\prod(1-r_i)$
cumulative-risk metric. The baseline that route is reported against is the
**direct leg** itself — the single IC→FL edge,
read straight out of the network by `direct_leg` — and not the
distance-minimal path, which on this network happens to be that same leg
and so cannot be told apart from it by inspection alone.
`gadget_knapsack` solves the 0/1 equipment-loadout
problem exactly by dynamic programming [@kellerer2004] over gram-scaled
weights, selecting from 7 candidate gadgets under a
25 kg budget; the per-item selection flag is recorded
during that item's own DP pass, because a final-array equality check
false-negatives once a later item has already absorbed the same capacity
cell. `trip_plan` projects the chosen route's legs against the vessel's
10 kn cruise, its 4,257 nm endurance, and
24 h refuelling stops, counting stops and elapsed time.

### 2.6 Surveillance and watchlist

An unsanctioned operator's exposure to the adversary's surveillance
apparatus is modelled in `surveillance.py`. Each covert action has a
*signature* (detectability) and a *watch increment* (how much it teaches the
watchlist); the step-$t$ detection hazard is the logistic
$p_t = \sigma(\beta_0 + \beta_w w_t + \beta_s s_i)$ where $w_t$ is the
accumulated watchlist weight. A sequence survives only if every step goes
undetected, so its success probability is $\prod_t(1-p_t)$. The order that
maximises survival is found exactly by exhaustive permutation search for up
to 8 actions (`exact_action_order`) and by a
value-per-exposure ratio rule (Smith's rule [@smith1956]) beyond that
(`heuristic_action_order`); `compromise_step` reports the first step at
which cumulative detection crosses the threshold 0.50. The
canonical detection coefficients are $\beta_0 = -4.0$,
$\beta_w = 1.2$, and $\beta_s = 1.5$.

## Results — WAVEKREST: measured outcomes, headline numbers, and what they establish

All results below are deterministic outputs of the canonical seeded run
(seed 0) and are re-computed verbatim by
`src/licence_to_kill/manuscript_variables.py` — the plain numbers you read
are injected tokens, not hand-typed values.

### 3.0 Headline results at a glance

| Domain | Key quantity | Value |
|---|---|---|
| Laundering | Composite layering score | 0.513 |
| Laundering | Integration score | 0.653 |
| Vessel | Forensic anomaly score | 2.0 |
| Rogue | Optimal expected mission value | 1.665 |
| Finance | Courier-parcel cash mass | 50.0 kg |
| Logistics | Cumulative route interdiction risk | 0.208 vs 0.300 direct |
| Surveillance | Probability of completing undetected | 0.263 |

Each row is developed in its own subsection below; the numbers are the same
injected tokens, so the table cannot disagree with the analysis.

### 3.1 Layering and integration in the Sanchez network

The canonical network built by `build_sanchez_network(seed=0)` contains
**22** nodes and **89** directed edges,
carrying a placed dirty value of **132.2** currency units. The
detectors identify:

- **1** money-returning cycle(s) — the direct layering loop
 that returns cash through the shell grid;
- **16** funnels (collectors that concentrate the flow and
 distributors that scatter it);
- **720** placement→integration chains — the *exact* count,
 not a capped sample: the enumeration bound (1000) sits
 strictly above the true number, so every chain is found and the depth
 component is computed over the full population.

The composite **layering score** is **0.513** (of a possible 1),
reflecting the substantial but deliberately incomplete obscuring structure.
The **integration score** is **0.653**: the placed dirty
value is diluted to that degree by the legitimate exporter flows feeding the
same banks, with a **mixing entropy** of **1.381** nats across
the 4 integration sinks.

![Sanchez money-laundering graph; node colour is the dirty-flow share, laid
out left-to-right by laundering stage.](output/figures/licence_to_kill_laundering_network.png)

### 3.2 Wavekrest-class vessel forensics

The canonical profile resolves:

| Quantity | Value |
|---|---|
| Enclosed hull volume | 1357 m³ |
| Gross tonnage (IMO) | 356 |
| Draft-predicted displacement | 985 t |
| Usable fuel | 51.0 t |
| Full-tank endurance | 4257 nm |

The forensic scan flags **2** anomalies (aggregate score
2.0): a cargo bulk-density inconsistent with boxed fish,
and a declared displacement that disagrees with the draft-predicted value —
consistent with concealed contraband load. The Wavekrest's own physics betray
its cargo before its crew does (the vessel figure).

![Wavekrest-class forensic profile: hull volume, gross tonnage, fuel, and
draft-predicted displacement.](output/figures/licence_to_kill_vessel_forensics.png)

### 3.3 Rogue-00 optimal policy

For the canonical revoked-licence model (horizon 10 steps,
alert ceiling 10, action card *stealth / covert / overt*), the
dynamic program evaluates **2310** state cells and returns:

- an **optimal expected mission value** of **1.665**;
- a **stealth** opening — the least-escalating intensity,
 confirming that a revoked-licence operator must build capability
 surreptitiously before any overt strike;
- a close on **overt**. The optimal policy holds the
 least-visible intensity for the whole horizon and spends its escalation on
 the final step, when there is no remaining future for the raised alert to
 damage — the classic finite-horizon end effect, arrived at here without
 being written in;
- a **peak blowback hazard** of **0.378**, reached on the
 last step, and a **peak alert** of **3.0** —
 the level the closing overt action *leaves behind*, which is therefore
 also the terminal alert (3.0) (the rogue figure). Read
 those two numbers carefully, because they say different things. No step
 in the horizon is ever exposed to that alert: it is raised by the final
 action and the mission then ends, which is exactly why the dynamic
 program is willing to buy it. Every step the operator actually faces is
 *entered* at alert 0, so the hazard he faces climbs on **accumulated
 exposure** alone — on the integer alert lattice the stealth intensity's
 visibility rounds to no alert increase at all. That is a boundary of the
 quantisation, not a claim that stealth is free — Section 7 states it
 plainly. The distinction is not cosmetic: a peak taken over the alert
 each step is entered with would report a flat zero for this policy and
 read as "the optimum never escalates", which is false.

![Rogue-00 escalation under the optimal policy. Two alert series are drawn:
the level each step is *entered* with (flat at zero here) and the level each
step's own action *leaves behind* — the second is the only one that shows
the closing overt escalation. Exposure and the blowback hazard climb
throughout.](output/figures/licence_to_kill_rogue_escalation.png)

### 3.4 Narcotics-finance economics

The canonical courier parcel is valued at **$5,000,000** in
**$100** notes — **50,000** bills. US-currency note
physics give a bulk-cash mass of **50.0 kg** and a volume of
just **0.0565 m³** (bulk density ≈ 885
kg/m³). From a base production cost of **$1,500**/kg the
supply chain (export → wholesale → street) prices a kilogram at
**$9,000** wholesale and **$18,000** at
street level (**$18** per gram), or
**$30** per *pure* gram at 60% purity — the
same value is quietly present at every stage.

Against the Wavekrest-class hold (520 m³,
300 t usable mass), the parcel is
**yes** to fit and needs **1** trip(s).
The money is compact; the hard constraint is the cover cargo that must blend
with it — not the cash itself.

### 3.5 Operations logistics

Risk-optimal routing over the campaign network returns the layered path
**IC → HK → FL** (2 legs, 17,000 nm, costing
**$270,000**) with a cumulative interdiction risk of
**0.208** — against **0.300** for the direct
single leg, a **30.7%** reduction — the same pairing the
finance graph demonstrates in the money layer (the operations figure). The voyage
requires **3** refuelling stops (against the Wavekrest's
4,257 nm endurance at 10 kn) for roughly
**74** days at sea (**1,772** hours). The gadget
loadout under a 25 kg budget selects
**5** of 7 candidates
(including the Walther PPK, explosive charges, and the surveillance kit)
worth **32** mission points at
**17.7 kg**, computed by exact 0/1-knapsack dynamic
programming over the full capacity lattice.

On *this* instance that exactness buys nothing observable: a greedy
value-density pass returns the same 5 items at the
same value and the same weight, which
`tests/test_operations_logistics.py::test_greedy_matches_exact_on_the_canonical_instance`
records rather than hides. The claim being made for the DP is therefore not
"it beat greedy here" — it did not — but that it is optimal on *every*
instance, where greedy is not;
`test_greedy_value_density_is_suboptimal_on_a_counterexample` exhibits an
instance on which the greedy pass leaves value on the table.

![ROGUE operations network with the risk-optimal route highlighted against
the direct single leg.](output/figures/licence_to_kill_operations_logistics.png)

### 3.6 Surveillance and watchlist

Across the **5**-action covert campaign, the
survival-optimal order — opening with *observe_isthmus_house*, the lowest-
signature move, and closing with *infiltrate_compound* — achieves a
probability of completing undetected of **0.263**. Cumulative
detection crosses the 0.50 threshold on the
**5**th action, and the peak step hazard reaches
**0.633**: the adversary's watchlist eventually prices the
campaign in, and the operator wins only by doing the cheaply-detectable work
first and the compounding-mistake last.

Because 5 ≤ 8, this ordering is the
exhaustively-verified optimum rather than the ratio-rule heuristic — no
permutation of these actions survives more often.

## Conclusion — WAVEKREST: findings, verdict, and what the mission establishes

Licence to Kill: ROGUE — Special-Agent Mission Software for Laundering-Graph, Vessel-Forensic, Rogue-Policy, Narcotics-Finance, Logistics, and Surveillance Analysis demonstrates that a special-agent mission package can be
entirely deterministic and still analytically rich. The six domains — the
Sanchez money-laundering graph, the Wavekrest-class vessel forensics, the
rogue-00 risk model, narcotics-finance economics, operations logistics, and
the surveillance/watchlist model — each carry a real, testable algorithm, and
together they render the ROGUE campaign's field questions answerable in
closed form:

- layering and integration are *measurable* (layering score
 0.513, integration score 0.653);
- covert cargo is betrayed by marine physics (2 anomalies
 flagged on the canonical mothership);
- unsanctioned operations have an exact optimal policy — and that policy
 begins with stealth, not with a frontal assault, saving the
 overt move for the step with no future left to protect
 (optimal value 1.665);
- the money is bounded by cash *physics* before any courier flies
 (50,000 bills, 50.0 kg, 1 hold-trivial
 trip);
- routing the campaign cheaply against risk matters — the layered leg cuts
 cumulative interdiction by 30.7% (0.208 vs
 0.300);
- an unsanctioned operator's cover is finite — survival to completion is
 0.263, and order is the operator's only free variable.

The six domains stay honest about each other because they share one
declaration: the `canonical_*_params` functions are read by the mission
adapter, the manuscript token generator, and the figure generators alike,
and the `mission:` block of `manuscript/config.yaml` is asserted equal to
them by the test suite. A parameter cannot change in one place and quietly
survive in another.

Because the entire pipeline runs on a fixed seed (0) with no random
draws in the detectors and no wall-clock anywhere in the persisted outputs,
every figure and every table in this manuscript is reproducible byte-for-byte
on a fixed interpreter and NumPy build — the two environment-derived token
values, and the whole of the claim's scope. That is a tested property, not a
comment: `test_regeneration_is_byte_identical` reruns the generator and
compares every emitted file. As a
BOND package, `licence_to_kill` exposes all of this through the frozen
`bond-api` `MissionProvider` contract, so the fleet orchestrator can discover
and drive it as a first-class citizen of the 27-film suite. The revoked
licence changes the operator's tactics — never the rigour of the analysis.

## Experimental Setup — WAVEKREST: canonical scenarios, parameters, and configuration

All experiments are deterministic and reproducible under Python
3.14.6 with NumPy 2.4.2.

### Where the parameters actually live

Each domain module declares its own scenario in a `canonical_*_params`
function, and those functions are the *executable* source of truth. The
domain core is deliberately dependency-free (standard library plus NumPy)
and does not read YAML, so `manuscript/config.yaml`'s `mission:` block is a
**declared mirror** of those functions rather than their input.

That mirror is enforced, not trusted: `tests/test_canonical_params.py`
asserts every key of the `mission:` block equal to the value the code
computes with, and fails the suite if the two drift. The same tests assert
that the declared search bounds are genuinely *consumed* — halving the path
cap must halve the enumerated chains — so a parameter cannot become
decorative without a test noticing. Nothing below is hard-coded in prose;
every value is an injected token read from the same functions.

### Laundering network

- Placement sources (street collectors): 3 nodes,
 `S1`–`S3`.
- Integration sinks (banks): 4 nodes, `B1`–`B4`,
 mixed with legitimate exporter flows (`L1`–`L3`) into the same sinks so
 integration is non-trivial.
- Edge amounts drawn from a seeded generator (`seed 0`): the same seed
 always yields the same graph and therefore the same report.
- Detector bounds: cycle search depth 8, capped at
 50 cycles; layering-path enumeration capped at
 1000 chains; funnel degree-imbalance threshold
 1.5.
- Source of truth: `canonical_laundering_params` in `laundering_graph.py`.

### Vessel forensics

- Profile: the canonical Wavekrest-class mothership (`WAVEKREST_CLASS` in
 `vessel_forensics.py`) — cargo volume 520 m³, block
 coefficient 0.62, maximum speed
 12.5 kn.
- Observed quantities that expose covert modification: a declared cargo mass
 of 900 t (above the
 1.4 t/m³ fish ceiling for that hold) and a
 declared displacement of 700 t (outside the
 15% tolerance around the draft-predicted
 value).
- Physical constants: seawater density 1.025 t/m³,
 diesel specific fuel consumption 0.195 kg/kWh.
- Source of truth: `canonical_vessel_params` in `vessel_forensics.py`.

### Rogue-00 risk model

- Horizon 10 steps; discrete alert states
 0..10.
- Action card *stealth / covert / overt* with visibility and gain ladders,
 truncated onto the integer alert lattice by the shared `next_alert`
 transition.
- Continuous exposure quantised onto a 21-cell lattice
 (`exposure_cap 20`), giving a backward-induction
 lattice of 2310 state cells.
- Source of truth: `canonical_rogue_params` in `rogue_ops.py`.

### Narcotics-finance economics

- Intercepted courier parcel: US$5,000,000 in $100
 notes (the film's opening intercept), against the Wavekrest-class hold
 (520 m³, 300 t usable mass).
- Supply chain: base cost $1,500/kg through the
 export → wholesale → street multipliers, at 60% purity. US-currency
 note mass 1.0 g and volume 1.13 cm³ per
 note [@bep_currency].
- Source of truth: `canonical_finance_params` in `narcotics_finance.py`.

### Operations logistics

- Campaign network: 5 legs across 4 hubs
 — Isthmus City (IC), the refinery at Bogota (BOG), Hong Kong (HK), and
 Florida (FL) — each with a distance, cost, and interdiction risk. The
 routed problem is `IC` → `FL`.
- Weight keys: `risk` (via −ln(1−r) survival weights), `cost`, `distance`.
- Gadget budget 25 kg over 7
 candidate items from the film's loadout; Wavekrest cruise
 10 kn and 4,257 nm endurance with
 24 h refuel stops.
- Source of truth: `canonical_logistics_params` in
 `operations_logistics.py`.

### Surveillance and watchlist

- 5 covert actions, each with a signature, watch
 increment, and value.
- Detection logistic β₀ = -4.0, β_watch = 1.2,
 β_signature = 1.5, threshold 0.50;
 exact survival-optimal ordering up to 8 actions with a
 ratio-rule fallback beyond.
- Source of truth: `canonical_surveillance_params` in `surveillance.py`.

### Software environment

- Package version 0.1.0; film identity `licence_to_kill`; codename
 `ROGUE`.
- Rendered variable map written to `output/data/manuscript_variables.json`;
 canonical mission results to `output/data/mission_results.json`.

> **On the clock:** no token carries one. An earlier `GENERATION_TIMESTAMP`
> wall-clock diagnostic was written into the variable map and made every
> regeneration produce different bytes; it was removed rather than excused,
> because a documented exception is still a false byte-for-byte claim. The
> only values here that are not fixed by the committed inputs are
> `PYTHON_VERSION` (3.14.6) and `NUMPY_VERSION`
> (2.4.2), which fix the scope of the reproducibility claim to a
> given interpreter and NumPy build.

## Reproducibility — WAVEKREST: verification gates, deterministic regeneration, and artifacts

### Determinism contract

The ROGUE mission is deterministic by construction:

- **Fixed seed.** The canonical network uses `seed 0`; a seeded
 generator draws the edge amounts, so the same seed always yields the same
 graph and the same report. `tests/test_laundering_graph.py` asserts that
 `seed 0` reproduces an identical edge set and that a different seed
 changes it.
- **No random draws in the detectors.** Cycle, funnel, dirty-flow,
 integration, entropy, forensic-physics, dynamic-programming, routing,
 knapsack, and surveillance-ordering routines are pure arithmetic.
- **One declaration per scenario.** The mission adapter, the manuscript
 token generator, and the figure generators all read the same
 `canonical_*_params` functions, and `tests/test_canonical_params.py`
 asserts the mission outcome and the manuscript analyses are equal
 report-for-report. A figure cannot depict inputs the prose does not
 describe.
- **No wall-clock in persisted outputs.** Provenance `wall_time_s` is fixed
 at `0.0` and no token carries a clock reading. A `GENERATION_TIMESTAMP`
 token was emitted into `output/data/manuscript_variables.json` until it was
 removed: it made two runs a second apart differ, so the byte-for-byte claim
 below was false while it existed, and the test guarding it injected a fixed
 clock and therefore could not see it.
 `test_no_token_carries_a_wall_clock_value` now rejects any clock-shaped
 token value.
- **Byte determinism of figures.** `tests/test_figures.py` renders each
 figure twice into independent directories and asserts byte-identical PNGs.
- **Byte determinism of the whole regeneration.**
 `tests/test_manuscript_variables.py::test_regeneration_is_byte_identical`
 runs `scripts/z_generate_manuscript_variables.py` twice, a real second
 apart, into two independent copies of the package and compares every
 emitted artifact — both JSON files, all nine rendered sections, and all
 four figures — byte for byte, with no clock injected anywhere.
- **End-to-end determinism.** `tests/test_mission.py` executes the mission
 twice and asserts identical result dictionaries and provenance hashes.

### Provenance

Every `MissionOutcome` carries a `Provenance` with the package version
(0.1.0), the `seed` (0), a `sha256` `input_hash` over the
canonical network (node set and edge amounts) *and* every parameter of all
six canonical domain scenarios, and `wall_time_s = 0.0`. The hash makes any
ROGUE outcome independently auditable without re-running the film:
re-compute the hash over the same inputs and it must match. Its coverage is
tested by mutating each domain's inputs in turn and requiring the hash to
respond — a hash that silently omitted a domain would make "audit" mean
less than it says.

### Test coverage

The source tree is covered well above the enforced 90 % line + branch floor
(`uv run pytest tests/ --cov=src --cov-fail-under=90`). Coverage levels and
the live test count are deliberately not quoted here — the gate is the
claim, and the measured figure belongs in `TODO.md`'s dated verification
record, where it can be checked against a command rather than trusted.

### Artifacts

Regenerable output (git-ignored) lives under `output/`:

- `output/data/mission_outcome.json` — tagged `MissionOutcome` from
 `scripts/mission_execute.py`;
- `output/data/mission_results.json` and `output/data/manuscript_variables.json`
 from `scripts/z_generate_manuscript_variables.py`;
- `output/manuscript/*.md` — numbered sections with generated tokens substituted;
- `output/figures/*.png` — the four ROGUE figures.

Re-running `scripts/z_generate_manuscript_variables.py` regenerates all of
these byte-identically — asserted by `test_regeneration_is_byte_identical`,
not merely asserted about. The scope of that identity is a fixed interpreter
and NumPy build: `3.14.6` and `2.4.2` are the only
environment-derived token values, so those two fields (and nothing else) can
differ across environments. Environment: Python 3.14.6, NumPy
2.4.2, film `licence_to_kill`, codename `ROGUE`,
package version 0.1.0.

## Scope and Related Work — WAVEKREST: boundaries, positioning, and relationship to the literature

### Scope

This package models the *analytical scaffolding* of the ROGUE mission, not
its fiction. It does not attempt to simulate human behaviour, the cartel's
actual personnel, or the film's events; it provides reproducible,
first-principles tools a field analyst would use. All six inference objects
are deliberately stylised: the laundering graph abstracts real banking
structure, the vessel profile abstracts a real vessel class, the rogue model
abstracts an operator's options into a three-intensity action ladder, the
price ladder abstracts a market into fixed multipliers, the campaign network
abstracts world geography into 4 hubs, and the surveillance
model abstracts an intelligence apparatus into a single logistic hazard.
Generalisations to genuine transaction histories, real vessel data, market
price series, real route networks, or richer action spaces are natural
extensions but are out of scope here.

### Related work

- **Money laundering.** Layering and integration are standard in the
 financial-crime literature; our cycle + funnel + dirty-flow propagation
 operationalises them on an explicit graph. Financial Action Task Force
 recommendations and typology reporting [@fatf2020] describe the
 placement–layering–integration lifecycle this model encodes.
- **Narcotics finance and cash physics.** Supply-chain price/purity ladders
 follow the order-of-magnitude cost structure reported in US Drug
 Enforcement Administration price analyses [@dea_prices]; the conversion of
 value into note mass/volume follows US Bureau of Engraving and Printing
 currency specifications [@bep_currency].
- **Graph algorithms.** Depth-first cycle enumeration follows Tarjan's
 depth-first-search framing [@tarjan1972]; risk-adjusted routing is
 Dijkstra's algorithm [@dijkstra1959]; the gadget loadout is the 0/1
 knapsack problem solved by dynamic programming [@kellerer2004].
- **Vessel forensics.** Gross-tonnage computation implements the
 International Convention on Tonnage Measurement of Ships, 1969
 [@imo1969]; endurance modelling uses the standard cubic propulsion-power
 law and diesel specific fuel consumption.
- **Sequential decision-making.** The rogue-00 model is a finite-horizon
 Markov decision process solved exactly by dynamic programming [@bellman1957];
 the surveillance ordering rule follows Smith's ratio rule for
 single-stage scheduling [@smith1956].
- **Source material.** The mission is drawn from the 1989 film directed by
 John Glen [@licence1989].

### Limitations

Determinism is a feature, but also a boundary: results are exact *for the
modelled objects*, and the objects are idealised.

- The composite laundering score's component weights
 (0.4 / 0.3 /
 0.3) are heuristics, not estimates from labelled
 data. The score is not a calibrated absolute quantity, and its *ranking* of
 two structures is not invariant to the weights either: over a coarse
 sampling of the weight simplex (21 weight
 triples) the ordering of two deliberately distinct reference structures
 matches the canonical-weight ordering on only
 38% of the samples. Measured, not assumed — the
 number is a token from `layering_ranking_stability` in
 `manuscript_variables.py`, and the non-invariance is a pinned test
 (`test_layering_score_ranking_is_weight_dependent`). Treat the composite
 score as a screening heuristic for gross differences, never as a stable
 single-number ordering.
- `LAUNDERING_PATHS` is the exact source→sink chain count for the canonical
 network, not a truncated sample: the enumeration cap
 (1000) sits strictly above the true count and the depth
 component is computed over the full chain population (see
 `test_canonical_layering_path_count_is_exact_not_saturated`).
- The vessel physics ignore sea state, hull fouling, and auxiliary loads;
 endurance is a flat-water, single-speed idealisation.
- **The rogue model's alert dimension is an integer lattice**, so the
 visibility ladder is truncated onto it. At the canonical parameters the
 stealth intensity's visibility (0.5) truncates to
 *no* alert increase, which is why the optimal policy enters every one of
 its steps at alert 0 and the blowback hazard it faces is driven by
 exposure alone. Its single escalation is the closing overt action, which
 leaves alert at 3.0 with no remaining horizon to be
 exposed to it — reported as `ROGUE_PEAK_ALERT`
 (3.0) rather than folded into the entering-alert curve,
 because a peak taken over entering alert alone is identically zero for
 this policy and would misdescribe it. This is the most consequential
 simplification in the package and it is stated here rather than buried:
 a finer alert lattice, or an explicitly integral visibility ladder, would
 change the optimal policy. The quantisation is at least *consistent* — the
 optimiser and the reported trajectory share one transition function, and
 the test suite pins that replaying the optimal sequence reproduces the
 optimal value exactly.
- The narcotics prices are order-of-magnitude anchors [@dea_prices] rather
 than market data, and the stage multipliers are fixed rather than
 estimated.
- The logistics network abstracts real geography into 4 hubs
 with static per-leg risks; interdiction risk in reality is neither static
 nor independent across legs, and the survival-product metric assumes
 independence.
- The surveillance model's exact ordering is brute-force for small n
 (n ≤ 8), with a ratio-rule heuristic beyond; the
 heuristic carries no optimality guarantee for this objective.

Each of these is documented where the corresponding parameter lives in
source, and each is open to principled extension behind the same frozen
`bond-api` protocol.

## Sources — WAVEKREST: bibliography

@tarjan1972; @imo1969; @bellman1957; @licence1989; @fatf2020; @dijkstra1959; @kellerer2004; @smith1956; @bep_currency; @dea_prices; @shannon1948


# The World Is Not Enough (1999) — ELEKTRA

*film package · package codename ELEKTRA*. Mission **ELEKTRA**: interdict tamper at oil-pipeline choke points; contain a coordinated power-grid blackout; route the nuclear submarine to safety and track the hijacked hull; model hostage-captor dynamics and negotiate the captor's patience.

## Concepts — ELEKTRA: domain and operational focus

energy infrastructure, hostage psychology

## Abstract — ELEKTRA: mission summary

In *The World Is Not Enough* (1999), mission codename **ELEKTRA**, we develop deterministic special-agent mission software across six operational pillars. Three model the film's primary threats — pipeline sabotage, submarine evasion, and hostage psychology — and three couple to them: an energy-infrastructure model that supplies the sabotage force multiplier, a bargaining model that consumes the syndrome state, and a tracking filter that re-acquires the evading hull. 1. **Oil-pipeline security** — a capacitated flow model of a Caspian crude trunk is analysed with the Edmonds–Karp max-flow/min-cut algorithm and Brandes edge-betweenness to isolate choke points, then subjected to a deterministic tamper-interdiction simulation. The analysis surfaces a single principal choke point (**J4->J5**) carrying the corridor at full rated capacity (max flow 420.000 kbbl/day, min-cut capacity 420.000 kbbl/day). 2. **Nuclear-submarine defense** — a passive-sonar equation (spherical spreading plus absorption) turns each listening sensor's range into a detection-probability field via the normal CDF; Dijkstra's algorithm then routes the *King William* from origin to safety. Least-risk routing cuts cumulative detection exposure by **24.861%** relative to line-of-sight. 3. **Hostage-psychology influence** — a four-state ODE model of hostage–captor dynamics (fear, gratitude, identification, threat) integrated with a fixed RK4 scheme reproduces the qualitative onset of Stockholm syndrome, with the syndrome index crossing the onset threshold on day **11.250** and reaching a final value of **0.532**. 4. **Energy infrastructure** — a DC power-flow model of a two-area grid with a cascading-failure solver shows that cutting the 3->5 interconnector reroutes all transfer onto a weak tie that trips, blacking out **220.000 MW** (**0.440** of system load) in a 1-step cascade. 5. **Hostage negotiation** — Rubinstein alternating-offer bargaining ties the captor's patience to the syndrome state: identification lifts the captor's equilibrium claim to **0.345** of the stake (up from a no-syndrome baseline of 0.198 — a **74.310%** relative increase), and concession closes the deal by day **5.625**. 6. **Sensor fusion** — a linear Kalman filter tracks the hijacked submarine from noisy position fixes, cutting position RMSE from **2.912** to **1.776** (a **39.016%** gain) and converging to a final error of **0.880**. All results are real model outputs, produced deterministically under seed 1999; no metric in this manuscript is hand-authored.

## Introduction — ELEKTRA: mission framing, the operational problem, and how to read this chapter

*The World Is Not Enough* (1999) pairs Bond's espionage with a set of
operational-economic threats that map cleanly onto computational-science
problems: a transnational oil pipeline that is the target of sabotage, the
power system that pumps it, a nuclear submarine that must be denied to a
hijacker and then re-found, and the psychological dynamics of a hostage crisis
that shape how negotiators bargain. This package — the BOND suite's
*ELEKTRA* mission — builds deterministic, reproducible mission
software for each.

### Mission context

In the film, industrialist Elektra King's Caspian oil pipeline is threatened
with sabotage, the nuclear submarine *King William* is stolen and must be
recovered before its weapons are used, and Bond himself contends with a captor
whose manipulation of Stockholm-syndrome dynamics clouds every judgment. Each
of these is, at heart, a computational problem:

- a **security graph** whose choke points and tamper exposure determine where a
 small cutting team can inflict maximum harm;
- an **energy network** whose interconnectors decide whether a single cut is a
 local nuisance or a regional blackout;
- a **detection-and-evasion** problem in which acoustic propagation decides
 what is heard and a route planner decides what is risked;
- a **recursive-estimation** problem: once the hull is lost, noisy contacts
 must be fused back into a track good enough for an intercept;
- a **dynamical-systems** model of how fear, small kindnesses, and
 identification produce emotional attachment in captivity;
- a **bargaining game** in which that attachment moves the captor's
 reservation value, not merely the mood in the room.

### Six pillars

Section 2 develops the mathematics of the six pillar models: maximum flow and
minimum cut, edge betweenness, and discrete-event tamper simulation (§2.1); the
passive-sonar equation, detection-probability link, and Dijkstra evasion
routing (§2.2); the hostage-psychology ODE system integrated with a fixed-step
RK4 scheme (§2.3); linearized DC power flow and a deterministic
cascading-outage blackout (§2.4); Rubinstein alternating-offer bargaining under
syndrome-driven patience (§2.5); and a constant-velocity linear Kalman filter
for submarine tracking (§2.6).

The last three pillars are not independent additions. The grid model supplies
the sabotage force multiplier behind the pipeline pillar; the bargaining model
consumes the syndrome state produced by §2.3 as its input; and the Kalman
filter re-acquires the hull that §2.2 routed into the acoustic shadow. Section
3 reports the measured results and renders the four concept figures. Sections
5–6 detail the experimental configuration and the determinism guarantees that
make every number reproducible; §7 states the scope limits of each model.

### Reader's guide

The package is organized as a pure domain core (`src/the_world_is_not_enough/`)
holding the six pillar modules (`pipeline_security`, `sub_defense`,
`hostage_psychology`, `power_grid`, `negotiation_tactics`, `sensor_fusion`), a
thin `mission.py` adapter implementing the frozen BOND-API `MissionProvider`
protocol over all six, thin phase scripts (`scripts/brief.py` …
`scripts/debrief.py`), and a manuscript hydrated entirely from measured model
outputs via `manuscript_variables.py`. Every numeric value in this manuscript
is generated from code — never hand-authored in prose.

## Methodology — ELEKTRA: the analytical models and algorithms that drive the mission

This section derives the mathematics of the six ELEKTRA pillar models. All
algorithms are standard and deterministic; every quantity reported in §3 is
computed by the corresponding code path.

### 2.1 Oil-pipeline security: choke points and tamper

**Network.** A crude pipeline is a capacitated directed graph
$G=(V,E)$ with origin $s$ (pump station), terminal $t$ (port), and segment
capacities $c_e$ (kbbl/day). The canonical ELEKTRA dataset is a
17-node / 16-segment simplex
of the film's Caspian corridor: a mainline from the origin pump station
`PUMP0` to the terminal `TERM` plus a set of junction spurs, with segment
`J4->J5` deliberately under-capacity (the physical constriction the analysis
must surface).

**Maximum flow / minimum cut.** The Edmonds–Karp algorithm repeatedly finds a
shortest (fewest-edge) augmenting path in the residual network and pushes its
bottleneck capacity until no augmenting path remains [@edmonds_karp]. By the
max-flow/min-cut theorem [@ford_fulkerson], the value of the maximum flow
equals the capacity of the minimum $s$-$t$ cut — the segment set whose removal
minimizes deliverable throughput. We recover that cut as the edges leaving the
source-reachable set of the final residual network:
$$v(f^*) = c(\delta(S^*)) = \min_{\text{cuts}} c(\delta(S)).$$

**Choke points.** A segment is a *choke point* when it is load-bearing and
running at or above 90% of its rated capacity
($u_e = f^*/c_e$ against the threshold constant
`pipeline_security.CHOKE_UTILIZATION_THRESHOLD`), where
$f^*$ is the max-flow carried along the (unique) flow path. This isolates the
constriction a cut or a tamper event can exploit with maximum throughput loss.
We also report Brandes edge-betweenness centrality [@brandes], the fraction of
all-pairs shortest paths traversing each segment, as a topological (rather than
capacity) view of structural importance.

**Tamper model.** A deterministic discrete-event simulation draws
``40`` tamper attempts, each choosing a segment weighted
by its declared risk; a guarded segment interdicts a detected attempt with
per-sensor probability ``0.850``, and undetected
events release the segment's capacity as lost flow (§3 reports the realized
detection rate and the resulting flow loss). Sensor coverage is the fraction of
total capacity under active sensors.

### 2.2 Nuclear-submarine defense: sonar detection and evasion

**Passive sonar equation.** A listening sensor at range $r$ metres receives the
target's radiated noise with a signal-to-noise ratio (dB)
$$\mathrm{SNR} = SL - TL(r) - NL + DI, \quad TL(r)=20\log_{10}(r_{\mathrm{km}}) + \alpha\, r_{\mathrm{km}},$$
with $SL$ the target source level, $NL$ ambient/self noise, $DI$ array
directivity, and $\alpha$ the absorption coefficient (dB/km) [@urick]. The
operator's detection probability follows the standard performance curve
$$P_d = \Phi\!\left(\frac{\mathrm{SNR} - DT}{\sigma}\right),\quad
\Phi(x)=\tfrac{1}{2}\bigl(1+\operatorname{erf}(x/\sqrt2)\bigr),$$
where $DT$ is the detection threshold and $\sigma$ the operator variability.

**Risk field.** Combining $3$ sensors by the independent
rule $R = 1-\prod_i(1-P_{d,i})$ over a $16\times16$
grid (3 km cells) yields the detection-probability field
the submarine must minimize exposure over.

**Evasion routing.** Dijkstra's algorithm finds the least-cumulative-exposure
path from origin to goal on the 4-connected grid, with per-step cost equal to
the cell's detection risk [@dijkstra]. A greedy 4-connected monotone
line-of-sight path serves as the naive baseline; because both live in the same
search space, the routed exposure is guaranteed not to exceed the baseline.
Bearing-only triangulation closes the loop: two passive bearings intersect
(least-squares) to localize an emitter.

### 2.3 Hostage psychology: Stockholm-syndrome dynamics

The influence model is a deterministic system of four bounded states — fear
$F$, gratitude $G$, identification $I$, and a time-varying threat input
$T(t)$ — each a fraction of 1:

$$\begin{aligned}
\dot F &= -aF + b\,T(1-F),\\
\dot G &= c\,K(t)(1-G) - d\,G,\\
\dot I &= e\,G(1-I) - f\,F\,I,\\
T(t) &= T_\text{floor} + T_0 e^{-\lambda t},
\end{aligned}$$

where $K(t)$ is a Gaussian-smoothed kindness-impulse train (the classic "small
kindness" condition [@namnyak]) and the saturating $(1-\cdot)$ terms keep every
state bounded in $[0,1]$. The composite **syndrome index**
$S=\mathrm{clamp}\big((2I+G-F)/3\big)$ summarizes the state. Integration uses a
fixed-step classical RK4 scheme over $30.0$ days at
$\Delta t = 0.250$, giving the onset day where $S$ first
crosses the $0.500$ threshold and the final/peak values.
The model is phenomenological decision support, grounded in the qualitative
conditions catalogued in the clinical and forensic literature
[@namnyak; @de_fabrique].

### 2.4 Energy infrastructure: DC power flow and cascading blackout

**DC power flow.** The power system is a graph of $8$ buses
joined by $10$ lines with susceptances $b_{ij}$ and thermal
limits $c_{ij}$ (MW). With a slack bus fixing the angle reference and bus
susceptance matrix $B$, the linearized load flow solves $B'\theta' = P'$ (slack
row/column removed) and the line flow is
$F_{ij} = b_{ij}(\theta_i - \theta_j)$ [@stott]. Only the
slack-connected *live* component is solved: islanded buses carry no power and
their load is unserved. The slack bus is by construction a member of its own
live component, so no separate "slack islanded" case arises.

**Cascading failure.** A deterministic outage cascade follows the OPA blackout
paradigm [@dobson_op]: an initial line outage reroutes power; the most
overloaded surviving line (largest $|F_{ij}|/c_{ij}$ ratio) trips; the system
re-solves; the process repeats until no line exceeds its rating. The blackout
is the load islanded from the slack bus. The canonical dataset is a two-area
corridor carrying 500 MW of total load, joined by a strong
interconnector (`3->5`,
400 MW) and a weak tie
(`4->5`, 150 MW): under intact
operation both share the Area-B transfer and stay within limits, but cutting
the strong tie forces the whole transfer onto the weak tie, which overloads,
trips, and islands the entire load area.

### 2.5 Hostage negotiation: bargaining under syndrome-driven patience

**Rubinstein equilibrium.** In the alternating-offer bargaining game with
discount factors $\delta_c$ (captor) and $\delta_n$ (negotiator) and the captor
proposing first, the subgame-perfect equilibrium gives the captor
$x_c = (1-\delta_n)/(1-\delta_c\,\delta_n)$ of the pie [@rubinstein]; a more
patient party captures more.

**Syndrome feedback.** The Stockholm-syndrome state feeds the captor's
patience: as identification grows, the captor values the relationship more and
becomes more patient, so $\delta_c = \mathrm{clamp}(\delta_c^0 + g\,S)$.
Beyond a threshold the equilibrium shares become disjoint
($x_c > 1 - x_c$) and the negotiation *stalemates*.

**Concession dynamics.** Over a 10.0-day horizon the
captor's demand concedes from its opening toward $x_c$ and the negotiator's
offer rises toward $1-x_c$, both at rate $r = 0.080$
per day. Settlement is the first day the offer meets the demand; if either
side reaches its equilibrium floor first, the crossing occurs at that floor,
and if the crossing falls after the deadline the deal lapses.

### 2.6 Sensor fusion: Kalman tracking of the hijacked submarine

The stolen *King William* is tracked through the patrol box from 20
noisy position fixes (fused contacts, measurement std
2.000). A constant-velocity linear Kalman filter
[@kalman] alternates **predict** and **update** steps:
$$\hat{x}_{k|k-1} = F\hat{x}_{k-1},\quad P_{k|k-1} = FP_{k-1}F^T+Q,$$
$$K = P H^T (H P H^T + R)^{-1},\quad \hat{x}_k = \hat{x}_{k|k-1} + K(z_k - H\hat{x}_{k|k-1}).$$
Measurement noise is drawn from a fixed-seed generator, so the track is
byte-reproducible. The filter's position RMSE is compared against the
raw-measurement RMSE to quantify the gain of fusion. (Bearing-only tracking
from a stationary observer is scale-ambiguous, so the model fuses noisy
*position* fixes — the convergent headline — and documents the limitation.)

## Results — ELEKTRA: measured outcomes, headline numbers, and what they establish

All numbers below are real outputs of the deterministic domain models
(seed 1999), hydrated into this manuscript by
`manuscript_variables.py` — none are hand-authored. Table 3 collects the six
pillars' headline measured results; every cell is a live token that resolves
identically to the mission outcome, so the same run the orchestrator executes
is the same run this manuscript reports.

### Table 3 — Headline measured results (live tokens)

| Pillar | Headline result | Value |
|---|---|---|
| Pipeline security | Max flow (kbbl/day) | 420.000 |
| Pipeline security | Min-cut capacity (kbbl/day) | 420.000 |
| Pipeline security | Principal choke point | J4->J5 |
| Pipeline security | Tamper detection rate (%) | 22.500 |
| Pipeline security | Cumulative tamper loss (kbbl) | 9660.000 |
| Submarine defense | Naive exposure | 22.989 |
| Submarine defense | Least-risk exposure | 17.274 |
| Submarine defense | Exposure reduction (%) | 24.861 |
| Hostage psychology | Syndrome onset day | 11.250 |
| Hostage psychology | Final syndrome index | 0.532 |
| Hostage psychology | Influence ratio | 0.602 |
| Energy infrastructure | Lost load (MW) | 220.000 |
| Energy infrastructure | Blackout fraction | 0.440 |
| Negotiation | Settlement day | 5.625 |
| Negotiation | Captor share of stake | 0.345 |
| Negotiation | Syndrome leverage (%) | 74.310 |
| Sensor fusion | Track RMSE | 1.776 |
| Sensor fusion | Measurement RMSE | 2.912 |
| Sensor fusion | Track gain (%) | 39.016 |

### 3.1 Oil-pipeline choke-point security

![The ELEKTRA Caspian trunk as a capacitated flow network; the single
principal choke point (J4->J5) is highlighted by its
full-capacity utilization.](output/figures/the_world_is_not_enough_pipeline_network.png)

The Edmonds–Karp solution sends a maximum flow of **420.000
kbbl/day** through the corridor; the minimum cut — the segment set smallest in
capacity whose removal starves the line — also has capacity
**420.000 kbbl/day**, exactly matching the max flow as the
max-flow/min-cut theorem requires. Utilization analysis isolates a single
principal choke point, segment **J4->J5**, which is the
only load-bearing segment running at full rated capacity
(1 segment in total at or above the
90% utilization threshold).
The pipeline network figure renders the graph with flow-criticality weighting
and choke-point emphasis the pipeline network figure.

Over **40** simulated tamper attempts, the sensor mosaic
interdicted **22.500%** of events; active
sensors cover **37.618%** of installed capacity. The
undetected remainder is charged
**9660.000 kbbl** of throughput — a *cumulative
volume*, obtained by pricing each undetected event at its segment's rated
capacity (kbbl/day) for 1.0 nominal downtime day.
It is deliberately not comparable with the 420.000 kbbl/day max
flow above and may exceed it, because many events accumulate across many
downtime periods. Two limits of that accounting are worth stating plainly: it
charges a segment's *full rating* rather than the flow the max-flow solution
actually routes through it (so spur tampering is priced above its marginal
delivery impact), and it therefore reports an upper bound on lost barrels
rather than a delivered-volume shortfall. Guarding
the single choke point J4->J5 protects the entire
throughput (420.000 kbbl/day), since it is the constriction every
barrel must pass.

### 3.2 Nuclear-submarine defense

![The passive-sonar detection-probability field over the
16$\times$16 km$^2$ patrol box, with the
naive line-of-sight route (dashed) and the least-risk Dijkstra route
(solid).](output/figures/the_world_is_not_enough_submarine_detection.png)

With 3 listening sensors, the ship's radiated noise yields
a spatially varying detection field (the submarine detection figure). A
straight, 4-connected line-of-sight transit accumulates
**22.989** total detection probability, while the
least-risk route — the global minimum of the same additive cost — accumulates
**17.274**, a reduction in exposure of
**24.861%**. Because the naive path lives in the same
search space as Dijkstra, the routed route is provably no worse; here it hides
in the acoustic shadow of the field rather than crossing the loudest corridor.

### 3.3 Hostage-psychology influence

![The hostage-psychology ODE time series: fear, gratitude, identification,
and the composite syndrome index.](output/figures/the_world_is_not_enough_hostage_dynamics.png)

Integrating the four-state model over 30.0 days
(the hostage dynamics figure) reproduces the qualitative trajectory reported
for Stockholm-syndrome cases: initial fear dominance, gratitude from small
kindnesses, and a growing identification with the captor. The composite
syndrome index crosses the 0.500 onset threshold on day
**11.250**, peaks at **0.581**, and
reaches a final value of **0.532**; by the end of the
horizon the captive's influence ratio toward the captor is
**0.602**. The model thus provides a principled estimate
of *when* an emotional bond forms — the negotiation window negotiators must
anticipate.

### 3.4 Energy infrastructure: coordinated blackout

In the canonical two-area grid, intact operation keeps both interconnectors
within rating (the strong `3->5` tie carries the
larger share; the weak `4->5` tie stays below its
150 MW limit). Cutting the strong
interconnector forces the entire Area-B transfer onto the weak tie, which
overloads and trips. The cascade — **1** tripping step
after the initial outage, **2** lines tripped
total — islands the whole load area: **220.000 MW** lost
out of 500 MW of connected load,
**0.440** of system load. This is the saboteur's force
multiplier: a single well-placed cut cascades into a regional blackout,
crippling the pumped corridor's pumping stations and the hijacked sub's
support base at once.

### 3.5 Hostage negotiation: syndrome-driven leverage

The Stockholm-syndrome model's final state
($S$ = 0.532) feeds the bargaining layer: it lifts the
captor's patience, raising the captor's equilibrium claim to
**0.345** of the pie, up from the no-syndrome baseline of
**0.198** (the equilibrium share at the captor's
un-boosted patience) — a *relative* increase of
**74.310%**, not an added share of the pie. Under the
symmetric concession schedule the captor and negotiator
still close the deal at parity by day **5.625**
(split **0.500**), but the syndrome has quietly
raised the captor's *reservation value* — and past a patience threshold the
negotiation would stalemate outright. The lesson for the negotiator: the bond
changes the captor's bottom line, not just the mood in the room.

### 3.6 Sensor fusion: tracking the hijacked hull

![The Kalman-filter track (green) of the hijacked submarine against the noisy
position fixes (gray) and the true constant-velocity trajectory (black).](output/figures/the_world_is_not_enough_sensor_fusion_track.png)

Fusing 20 noisy position fixes (measurement std
2.000) with the constant-velocity Kalman filter
cuts the track's position RMSE from **2.912** (the
raw fixes) to **1.776** — a **39.016%** reduction
— and drives the final position error to **0.880**
(the sensor fusion track figure). The filter converges, so an intercept
solution can be generated reliably even while the hull evades through the sonar
shadow.

## Conclusion — ELEKTRA: findings, verdict, and what the mission establishes

The ELEKTRA mission package demonstrates that the operational threats of
*The World Is Not Enough* — pipeline sabotage, submarine hijack, coordinated
blackout, and hostage psychological manipulation — reduce to well-posed,
deterministic computational problems that can be solved and reproduced to
engineering standard.

Six findings stand out. First, a capacity-aware choke-point analysis
(Edmonds–Karp max-flow/min-cut plus utilization) is far more actionable than a
naive "every segment is critical" view: the entire Caspian corridor distills to
a single principal choke point, **J4->J5**, where all
420.000 kbbl/day of throughput passes at full capacity. Second,
least-risk evasion routing measurably reduces submarine exposure — by
**24.861%** against line-of-sight. Third, the
hostage-psychology ODE model localizes the onset of Stockholm syndrome to a
specific day (**11.250** here). Fourth, the energy
model shows that a single interconnector cut cascades into a
**0.440** system blackout
(**220.000 MW** lost) — the sabotage force multiplier that
ties the pipeline and submarine threats together. Fifth, the bargaining layer
quantifies how the syndrome raises the captor's reservation value
(captor claim **0.345** against a
0.198 baseline — a
**74.310%** relative increase) while concession
still closes by day
**5.625**. Sixth, Kalman fusion makes the hijacked hull
trackable, cutting position RMSE by **39.016%**.

Every number in this manuscript is a measured model output, produced
deterministically under seed 1999 with zero external calls and zero
hand-authored metrics. The package is structured for extension — a new sensor
mosaic, pipeline or grid topology, bargaining schedule, or kindness schedule is
a configuration change, and the manuscript, figures, and mission outcome all
re-hydrate from the same source of truth.

## Experimental Setup — ELEKTRA: canonical scenarios, parameters, and configuration

Every `{CONFIG_*}` token below carries a **Source** column, because the two
kinds are not interchangeable. `config.yaml` marks a value *typed by the
author* in `manuscript/config.yaml`: editing it and re-running
`scripts/z_generate_manuscript_variables.py` re-derives the affected results in
§3. `derived` marks a value *read off a fixed dataset or module constant*
(`default_pipeline`, `default_power_grid`,
`CHOKE_UTILIZATION_THRESHOLD`) — those cannot be changed from the config file
at all, and changing them means editing the dataset in the domain module.
The split is enforced in code
(`manuscript_variables.DECLARED_CONFIG_TOKENS` /
`DERIVED_DATASET_TOKENS`) and this table is checked against it by
`tests/test_manuscript_variables.py`, so a mislabelled row fails the suite.

### Table 1 — Scenario parameters

| Parameter | Token | Source | Value |
|---|---|---|---|
| Mission codename | `MISSION_CODENAME` | derived | ELEKTRA |
| Deterministic seed | `CONFIG_SEED` | config.yaml | 1999 |
| Pipeline nodes | `CONFIG_PIPELINE_NODES` | derived | 17 |
| Pipeline segments | `CONFIG_PIPELINE_SEGMENTS` | derived | 16 |
| Choke-point utilization threshold (%) | `CONFIG_CHOKE_UTILIZATION` | derived | 90 |
| Tamper attempts | `CONFIG_TAMPER_EVENTS` | config.yaml | 40 |
| Per-sensor interdict probability | `CONFIG_DETECTION_PROBABILITY` | config.yaml | 0.850 |
| Sonar grid size | `CONFIG_SUB_GRID` | config.yaml | 16 |
| Sonar cell size (km) | `CONFIG_SUB_STEP_KM` | config.yaml | 3 |
| Listening sensors | `CONFIG_SUB_SENSORS` | config.yaml | 3 |
| Hostage integration horizon (days) | `CONFIG_HOSTAGE_DAYS` | config.yaml | 30.0 |
| Hostage integration step | `CONFIG_HOSTAGE_DT` | config.yaml | 0.250 |
| Syndrome onset threshold | `CONFIG_HOSTAGE_ONSET` | config.yaml | 0.500 |
| Power-grid buses | `CONFIG_GRID_BUSES` | derived | 8 |
| Power-grid lines | `CONFIG_GRID_LINES` | derived | 10 |
| Connected load (MW) | `CONFIG_GRID_LOAD_MW` | derived | 500 |
| Targeted interconnector | `CONFIG_GRID_INITIAL_OUTAGE` | config.yaml | 3->5 |
| Targeted interconnector rating (MW) | `CONFIG_GRID_STRONG_TIE_MW` | derived | 400 |
| Weak interconnector | `CONFIG_GRID_WEAK_TIE` | derived | 4->5 |
| Weak interconnector rating (MW) | `CONFIG_GRID_WEAK_TIE_MW` | derived | 150 |
| Negotiation deadline (days) | `CONFIG_NEG_DEADLINE_DAYS` | config.yaml | 10.0 |
| Negotiator discount | `CONFIG_NEG_NEGOTIATOR_DISCOUNT` | config.yaml | 0.900 |
| Concession rate (per day) | `CONFIG_NEG_CONCESSION_RATE` | config.yaml | 0.080 |
| Captor patience base ($\delta_c$ at $S=0$) | `CONFIG_NEG_CAPTOR_DISCOUNT_BASE` | config.yaml | 0.550 |
| Captor patience gain (per unit $S$) | `CONFIG_NEG_CAPTOR_DISCOUNT_GAIN` | config.yaml | 0.450 |
| Opening demand | `CONFIG_NEG_INITIAL_DEMAND` | config.yaml | 0.950 |
| Opening offer | `CONFIG_NEG_INITIAL_OFFER` | config.yaml | 0.050 |
| Fusion fix count | `CONFIG_FUSION_STEPS` | config.yaml | 20 |
| Fusion measurement std | `CONFIG_FUSION_MEASUREMENT_NOISE` | config.yaml | 2.000 |

### Table 2 — Hostage-model rate constants

The clinical and forensic literature on Stockholm syndrome is qualitative, so
the nine ODE rate constants below are a **declared modelling assumption**, not
a fitted result (§7). They are typed in `manuscript/config.yaml` under
`experiment.hostage.dynamics` and consumed by
`hostage_psychology.integrate_dynamics`; an auditor can change any one of them
and re-derive every syndrome and bargaining number in §3.

| Rate | Token | Source | Value |
|---|---|---|---|
| Fear self-decay $a$ | `CONFIG_HOSTAGE_FEAR_DECAY` | config.yaml | 0.120 |
| Threat sensitivity $b$ | `CONFIG_HOSTAGE_THREAT_SENSITIVITY` | config.yaml | 0.300 |
| Kindness gain $c$ | `CONFIG_HOSTAGE_KINDNESS_GAIN` | config.yaml | 0.650 |
| Gratitude decay $d$ | `CONFIG_HOSTAGE_GRATITUDE_DECAY` | config.yaml | 0.050 |
| Identification gain $e$ | `CONFIG_HOSTAGE_IDENT_GAIN` | config.yaml | 0.500 |
| Fear suppression $f$ | `CONFIG_HOSTAGE_FEAR_SUPPRESS` | config.yaml | 0.150 |
| Initial threat $T_0$ | `CONFIG_HOSTAGE_THREAT_INITIAL` | config.yaml | 0.750 |
| Threat decay $\lambda$ | `CONFIG_HOSTAGE_THREAT_DECAY` | config.yaml | 0.180 |
| Residual threat floor | `CONFIG_HOSTAGE_THREAT_FLOOR` | config.yaml | 0.120 |
| Initial state $(F, G, I)$ | `CONFIG_HOSTAGE_INITIAL_STATE` | config.yaml | 0.70, 0.00, 0.02 |
| Small-kindness schedule | `CONFIG_HOSTAGE_KINDNESS_SCHEDULE` | config.yaml | day 2.0 x 0.70; day 5.0 x 0.60; day 9.0 x 0.50; day 14.0 x 0.40 |

### Software environment

- Package version: 0.1.0
- Python: 3.14.6
- Manuscript edition stamp (declared in `config.yaml` as `paper.date`, not a
 clock reading): 2026-08-04T00:00:00+00:00

### What is *not* tunable from the config file

Tables 1 and 2 are the complete set of author-typed parameters, but they are
not the complete set of inputs. Three fixed datasets sit outside them and can
only be changed by editing the domain module that declares them:

- the pipeline topology and its per-segment capacities, tamper risks and sensor
 placement (`pipeline_security.default_pipeline`,
 17 nodes / 16 segments);
- the power-grid topology, line ratings and nodal injections
 (`power_grid.default_power_grid`, 8 buses /
 10 lines);
- the choke-point utilization threshold
 (`pipeline_security.CHOKE_UTILIZATION_THRESHOLD`).

The sonar sensor mosaic *is* config-typed (`experiment.submarine.sensors`),
though only its count is surfaced as a token. Every row marked `derived` in
Table 1 is a read-out of one of the three datasets above, which is why editing
`config.yaml` cannot move it. Re-running
`scripts/z_generate_manuscript_variables.py` after any of these changes
re-derives every result token in §3, and no file is written outside `output/`.

## Reproducibility — ELEKTRA: verification gates, deterministic regeneration, and artifacts

The ELEKTRA package is deterministic by construction.

### Determinism guarantees

- **Fixed seed.** The package has exactly two stochastic steps and both are
 seeded from the same value (`1999`, the film's release year): the
 tamper-event simulation draws from Python's `random.Random`, and the
 sensor-fusion measurement noise from `numpy.random.default_rng`. Every other
 model — max-flow/min-cut, betweenness, the sonar field, Dijkstra routing, the
 RK4 integration, the DC load flow and its cascade, and the bargaining
 equilibrium — makes no random draws at all. Runs are byte-reproducible.
- **No wall-clock anywhere in the persisted artifacts.** The mission outcome's
 `Provenance.wall_time_s` is always `0.0`; persisted provenance records use a
 fixed nominal mission epoch. `MANUSCRIPT_EDITION_STAMP` is the only
 time-valued token and it is *derived* from the committed `paper.date` key in
 `config.yaml` — it is an edition stamp a maintainer edits on purpose, never a
 reading of the clock at generation time. Consequently two regenerations of
 `output/data/manuscript_variables.json` and `output/manuscript/` on one
 interpreter are byte-identical, which
 `tests/test_manuscript_variables.py::TestRegenerationDeterminism` proves by
 running the generator twice across a second boundary and comparing the
 persisted bytes.
- **No external calls.** The pure domain cores never touch the network or the
 filesystem; the only I/O is thin scripts writing regenerable `output/`
 artifacts (git-ignored).
- **Fixed datasets.** Pipeline topology and sensor positions are declared
 constants, not sampled.

### Reproducing every number

```bash
## Mission outcomes (provenance to output/data/elektra_mission.json)
uv run python scripts/execute.py

## Figures -> output/figures/
uv run python scripts/generate_figures.py

## Manuscript variable hydration -> output/data + output/manuscript/
uv run python scripts/z_generate_manuscript_variables.py

## Gate: >=90% line+branch coverage on src/, zero mocks
uv run pytest tests/ --cov=src --cov-fail-under=90
```

A live cross-reference test (`tests/test_manuscript_variables.py`) enforces that
every token used in a numbered manuscript section is actually generated, so the
prose can never present a stale or fabricated metric. Hydration additionally
runs a measurability gate (`_assert_measurable`) that rejects any blank or
non-finite result token, so a degenerate model run fails the build instead of
rendering `nan` as a measured value.

### Verification gates

The package's hard rules are enforced by tests, not by convention:

- **Single source of truth.** The mission adapter and the manuscript read the
 same `experiment:` block through one shared builder
 (`manuscript_variables.build_mission_scenario`); the builder records every
 key it consumes and a completeness test walks the config asserting each leaf
 is consumed, so a knob added to `config.yaml` but read by nothing turns the
 suite red.
- **Fail-closed config.** The config accessors raise `KeyError` on a missing
 required key instead of silently defaulting — deleting one of the nine
 hostage rates, the initial state, the kindness schedule, or a whole pillar
 block is caught by a negative-control test for each.
- **Coverage.** `uv run pytest tests/ --cov=src --cov-fail-under=90` enforces
 ≥90% line + branch coverage; the suite currently sits at 100% with every
 validation arm exercised by a real (malformed) input.
- **Zero mocks / zero lineage.** `tests/test_guardrails.py` walks `src/`,
 `scripts/` and `tests/` and fails on any mock-framework pattern or the
 template-lineage string, with a positive control proving each matcher fires.
- **COUNTS freshness.** `tests/test_counts_staleness.py` re-derives the
 structural rows of `docs/_generated/COUNTS.md` from live objects, so a
 stale count fails the suite.

### Artifact inventory

| Artifact | Path | Regenerable |
|---|---|---|
| Mission outcome (canonical JSON) | `output/data/elektra_mission.json` | yes |
| Manuscript variables JSON | `output/data/manuscript_variables.json` | yes |
| Pipeline figure | `output/figures/pipeline_network.png` | yes |
| Submarine figure | `output/figures/submarine_detection.png` | yes |
| Hostage figure | `output/figures/hostage_dynamics.png` | yes |
| Sensor-fusion figure | `output/figures/sensor_fusion_track.png` | yes |
| Resolved manuscript tree | `output/manuscript/` | yes |

`output/` is git-ignored, so regeneration never dirties the tree — but a clean
`git status` is a consequence of the ignore rule, not evidence of determinism.
The evidence is the two-run byte comparison in
`TestRegenerationDeterminism`, which regenerates the JSON and the resolved
manuscript tree into two fresh directories a second apart and asserts every
file matches byte for byte.

## Scope and Related Work — ELEKTRA: boundaries, positioning, and relationship to the literature

### Scope

The ELEKTRA mission software is a deterministic, illustrative
decision-support suite, not operational equipment. Its scope and limits are
deliberate:

- **Pipeline model.** A single-corridor flow network with a capacity bottleneck
 and dead-end spurs. It does not model multi-path loops, pump-station
 dynamics, transient surge, or geographic routing; those would change the
 choke-point ranking but not the method.
- **Sonar model.** A simplified passive equation (spherical spreading plus
 absorption) with a normal-operator curve. It omits multipath, bottom/
 surface interaction, own-ship noise masking, and frequency-dependent
 attenuation, and the evasion grid is a 4-connected lattice rather than a
 continuous field.
- **Hostage model.** A phenomenological, bounded ODE system whose parameters
 encode the qualitative conditions catalogued in the literature. It is
 calibrated by construction to reproduce onset behaviour, not fitted to
 individual case data, and is not a clinical diagnostic instrument. Because
 the rate constants are chosen rather than estimated, the reported onset day,
 peak and final index are properties *of this parameterisation* — they carry
 no uncertainty interval and should not be read as a prediction about any
 real captivity. The nine rates are listed in §5, Table 2.
- **Tamper accounting.** The tamper simulation charges each undetected event
 its segment's *rated* capacity for one nominal downtime day, so its output
 is a cumulative volume (kbbl) and an upper bound: it prices spur tampering
 above the spur's marginal delivery impact and does not model repair time,
 partial throttling, or re-routing around the damaged segment.
- **Power-grid model.** A lossless DC load flow and a deterministic sequential
 cascade. It omits reactive power, voltage collapse, generator ramping,
 frequency dynamics, and parallel-time-step tripping (all overloaded lines
 tripping simultaneously), so blackout *magnitude* is a conservative lower
 bound and the *sequence* is one deterministic path rather than a probability
 distribution.
- **Bargaining model.** A deterministic Rubinstein equilibrium with a
 concession schedule and a syndrome-to-patience mapping that is a declared
 modelling assumption. It captures the *direction* of syndrome leverage and
 the stalemate threshold, not idiosyncratic negotiator behaviour or
 asymmetric information.
- **Sensor-fusion model.** A linear constant-velocity Kalman filter over
 noisy *position* fixes. It does not fuse true bearing-only measurements from
 a fixed observer (scale-ambiguous — documented), nor multimodal ESM/acoustic
 contacts; it demonstrates the recursive-estimation gain, not a full
 multi-source correlation engine.

### Related work

**Choke-point and flow analysis** rests on the max-flow/min-cut duality of
Ford and Fulkerson [@ford_fulkerson] with the polynomial Edmonds–Karp
augmenting-path implementation [@edmonds_karp], and on Brandes' edge-betweenness
centrality [@brandes]; Dijkstra's algorithm [@dijkstra] underpins the routing
layer, as it does in network shortest-path practice broadly.

**Passive-sonar detection** follows the acoustic propagation and operator
performance-curve treatment standard in the field (e.g. Urick [@urick]): the
transmission-loss law, the signal-excess link, and the probability-of-detection
curve used here.

**Power systems** are analyzed with the linearized DC load-flow formulation
(Stott [@stott]) and the cascading-outage paradigm of the OPA blackout model
(Dobson *et al.* [@dobson_op]), both standard in transmission-security
research.

**Bargaining** uses the subgame-perfect alternating-offer equilibrium of
Rubinstein [@rubinstein] — the canonical unlimited-horizon bargaining result —
as the anchor for the syndrome-driven patience mapping.

**State estimation** uses the linear Kalman filter [@kalman], the classical
recursive minimum-mean-square estimator, generalized by many later nonlinear
variants but fully exercised here in its linear, deterministic form.

**Stockholm syndrome** is documented as an outcome of specific custodial
conditions — perceived threat, small kindnesses, and prolonged contact —
rather than a formal diagnosis. The model synthesises the conditions catalogued
in the forensic review literature [@namnyak; @de_fabrique] into a quantitative
dynamical system. Where those sources are qualitative, our parameter choices
are the modelling assumption: all nine ODE rate constants, the initial state,
and the small-kindness schedule are typed in `manuscript/config.yaml` under
`experiment.hostage`, reproduced in §5 (Table 2), and consumed by the model —
`tests/test_manuscript_variables.py` perturbs each one and asserts the reported
syndrome index moves, so the exposure is auditable rather than decorative. The
claim is also *enforced*: the config accessors fail closed, so deleting any one
of the nine rates, the initial state, or the kindness schedule raises rather
than silently reverting to a module default — a deleted knob cannot pass
unnoticed. The *form* of the equations, by contrast, is fixed in
`hostage_psychology.derivatives` and is not configurable.

## Sources — ELEKTRA: bibliography

@ford_fulkerson; @edmonds_karp; @brandes; @dijkstra; @urick; @namnyak; @de_fabrique; @stott; @dobson_op; @rubinstein; @kalman


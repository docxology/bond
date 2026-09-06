# Spectre (2015) — NINE EYES

*film package · package codename NINE EYES*. Mission **NINE EYES**: measure surveillance-network centralization and data flow; assess the SPECTRE brotherhood's hierarchy and cell separation; identify critical nodes in the network's geometry.

## Concepts — NINE EYES: domain and operational focus

surveillance networks, org intelligence

## Abstract — NINE EYES: mission summary

This report describes **Spectre: NINE EYES — Special-Agent Mission Software** (mission codename **NINE EYES**), a special-agent mission-software package modelling the global surveillance programme from the 2015 film *Spectre*. Across 6 pure, deterministic analysis modules (infiltration, network_geometry, org_intel, signal_cover, surveillance_net, traffic_intel) it (i) measures the centralization of a nine-agency surveillance network whose data flows concentrate through hub agencies, (ii) models the SPECTRE brotherhood as a compartmentalized criminal organization with an isolatable command hierarchy, (iii) analyzes the network's geometry to identify the critical nodes whose neutralization most fragments the system, and then extends all three into operations: budgeted traffic interception, compromise cascades through the brotherhood, and sensor-placement set cover. Over the canonical NINE EYES network of 9 agencies and 13 directed data-sharing links, the measured group centralization index over out-degrees is 0.9219: one agency does almost all of the sending. The two directions do not agree. The Herfindahl index of the *inflow* shares is 0.1361 against an even-spread floor of 0.1250 for the 8 agencies that receive anything at all — so receiving is close to evenly distributed, and the concentration this network exhibits is in who sends, not in who is fed. The SPECTRE brotherhood of 7 operatives across 3 cells achieves a compartmentalization of 0.8235 with a command chain that is complete (true) to a height of 2. Geometry analysis finds 1 articulation points; the most load-bearing critical nodes are US, FR, UK. The operational layer adds budgeted *interception* (3 monitoring agencies capture 0.9669 of the exchange), *compromise cascades* through the brotherhood (a turned cell operative reaches leadership with probability 0.58), and *sensor-placement* set cover (4 agencies sweep every target with 0.2500 multi-sensor redundancy). All results are measured by the deterministic NINE EYES mission provider, which implements the frozen `bond_api` `MissionProvider` protocol over a 6-step plan and publishes 6 Q-branch gadgets. Every quantity in this report is injected from that computation; none is hand-authored. *Keywords:* surveillance networks, data-flow centralization, criminal-organisation intelligence, cell compartmentalization, network geometry, critical nodes, cascade coverage, betweenness centrality, articulation points, traffic interception, submodular maximization, compromise cascade, network percolation, sensor-placement set cover, coverage redundancy, deterministic reproducibility

## Introduction — NINE EYES: mission framing, the operational problem, and how to read this chapter

The Nine Eyes programme — a global surveillance-sharing arrangement among a
handful of Western intelligence agencies — is the geometric setting of the
2015 film *Spectre*. The NINE EYES mission software package renders that
setting as a computational model answering six intelligence questions, three
structural and three operational.

The structural questions ask what the network and the organisation *are*:

1. **How centralized are surveillance data flows?** If a single agency sits at
 the hub of every sharing link, the network is highly centralized and a
 single compromised hub exposes the whole exchange. Sending and receiving
 are separate readings and need not agree: a lone source can dominate the
 out-degree while its recipients each receive a comparable trickle, so an
 out-degree centralization index and an inflow-share concentration index are
 two measurements, not one measurement corroborated twice.
2. **How is a criminal brotherhood structured?** SPECTRE is a compartmentalized
 organization: isolated cells whose members know only their own cell,
 underneath an apex leadership. The intelligence question is how "separable"
 the cells are and whether the command chain is complete.
3. **Which nodes are critical to the network's geometry?** Connectivity,
 articulation points, and global efficiency identify the agencies whose
 removal most fragments the system. These are the priority targets for
 neutralization.

The operational questions ask what can be *done* with that structure:

4. **Where should a limited monitoring budget go?** Interception coverage is
 monotone and submodular in the monitored set, so a greedy allocation carries
 a provable approximation guarantee — and the diminishing returns are exactly
 what makes the hub's dominance actionable.
5. **What does one turned operative cost the brotherhood?** Exposure propagates
 through cellmates and command links; the cascade quantifies how often a
 single breach reaches the apex, and how quickly.
6. **Where should sensors be placed to sweep every target?** Placement is a set
 cover, and the residual multi-sensor redundancy measures whether the sweep
 survives losing one agency.

The package implements these as 6 pure,
deterministic domain modules — `spectre.surveillance_net` (data-flow
centralization, betweenness, cascade coverage), `spectre.org_intel` (hierarchy
and cell compartmentalization), `spectre.network_geometry` (connectivity,
articulation points, critical nodes), `spectre.traffic_intel` (volume-weighted
interception and budgeted monitoring), `spectre.infiltration` (compromise
cascade and expected damage), and `spectre.signal_cover` (sensor-placement set
cover and redundancy) — exposed to the BOND suite through a thin
`MissionProvider` adapter (`spectre.mission`) implementing the FROZEN
`bond_api` protocol. The adapter holds no mathematics of its own: it selects
the canonical data, calls the pure core, and records provenance, which is why
the protocol can stay frozen while the domain keeps deepening.

## Methodology — NINE EYES: the analytical models and algorithms that drive the mission

All analysis is deterministic and computed over a fixed, canonical dataset. The
only stochastic components — the influence cascade and the compromise cascade —
draw from explicitly seeded generators, and no wall-clock value enters a
persisted artifact. The package exposes 6 pure
domain modules (infiltration, network_geometry, org_intel, signal_cover, surveillance_net, traffic_intel); the mission's `execute` stage runs
them as a 6-step plan and reports the measured results
below.

### Surveillance-network centralization

The NINE EYES network is a directed graph whose nodes are agencies and whose
edges are data-sharing links. Out-degree centrality counts the data volume an
agency pushes downstream; in-degree centrality counts the volume it pulls in.
Freeman's group centralization index [@freeman1979]

$$
\mathrm{C}_{\mathrm{index}} = \frac{\sum_i (s_{\max} - s_i)}{(n - 1)\, s_{\max}}
$$ 

measures how concentrated the flows are, from 0 (evenly spread) to 1 (a single
hub dominates). The normalizing denominator is the total deviation of the star
graph on `n` nodes, so `s_max` is passed explicitly as `n - 1` rather than left
to default to the largest observed score; the two agree on this dataset only
because the maximum out-degree happens to equal `n - 1`, and on any input where
it does not, the observed-maximum form reports a different quantity from the
one written above. The Herfindahl–Hirschman index [@hirschman1964] of inflow
shares,

$$
\mathrm{HHI} = \sum_i \left( \frac{f_i}{\sum_j f_j} \right)^{\!2},
$$ 

is computed over the normalized in-degree share vector (which sums to 1) and
measures inflow concentration independently of the out-degree distribution. It
is reported against its floor `1/r`, where `r` is the number of agencies with
non-zero in-degree: the index alone is not interpretable, because its minimum
is not 0 but `1/r`, and a value near that floor means *even spread*, not
concentration.

Betweenness centrality — the share of shortest data paths passing through each
agency — is computed with Brandes' predecessor accumulation [@brandes2001] and
drives the node sizing in the network flow centralization figure. Note that
betweenness and out-degree rank different agencies first: a pure source has no
inbound edge, so no shortest path passes through it and its betweenness is
exactly 0 no matter how much it sends.

Cascade coverage runs an independent-cascade process [@kempe2003] from a
seeding agency at a fixed activation probability. A single run is one Bernoulli
realization, not an expectation, so the reported coverage is the mean over
50 realizations whose per-trial seeds are derived from
one base seed — the same treatment the compromise cascade receives below.

Networks are constructed either from an edge list, where every invariant is
enforced as the matrix is filled, or from an existing adjacency matrix, which
is validated explicitly (shape, label uniqueness, zero diagonal) because it was
produced elsewhere.

### Criminal-org cell model

The brotherhood assigns each operative to a cell and to a single superior.
Command depth is the number of links from an operative to the nearest apex; the
chain is complete when every operative is reachable from leadership by a
breadth-first walk down the `superior → subordinate` edges. Reachability is
computed by that walk rather than inferred from the depth assignment, so a
malformed organisation with a command cycle and no apex is correctly reported
as *incomplete* rather than silently accepted.

Compartmentalization is the fraction of cross-cell operative pairs that are
*not* directly linked by a command edge — 1.0 on a perfectly separated cell
structure, and lower when cells leak command links. Exposure of an operative is
their cellmates plus their direct superior and direct subordinates: the set that
falls if that operative is turned.

### Network geometry

Connectivity is assessed by connected-component flood fill; articulation points
(nodes whose removal disconnects the graph) are found with Tarjan's low-link
depth-first search [@tarjan1972; @hopcrofttarjan1973]. Global efficiency is the
Latora–Marchiori mean inverse shortest-path length [@latora2001]

$$
\mathrm{Eff} = \frac{1}{n(n-1)} \sum_{i \neq j} \frac{1}{d(i, j)},
$$ 

with unreachable pairs contributing nothing. Critical-node ordering greedily
removes, at each step, the node whose removal most reduces the *current*
graph's pairwise connectivity — the targeted-attack simulation of Albert, Jeong
and Barabási [@albert2000], scored as a key-player problem [@borgatti2006].

### Traffic interception

The traffic-intelligence model treats the surveillance network as carrying a
volume-weighted exchange. A monitored agency intercepts every link incident to
it — inbound as well as outbound — and the coverage of a monitored set is the
fraction of total traffic those links carry. Because a new agency's marginal
interception gain shrinks as coverage grows, allocating a monitoring budget is
a monotone submodular coverage-maximization problem; the greedy rule carries
the Nemhauser–Wolsey–Fisher `(1 - 1/e)` guarantee [@nemhauser1978], and the
same structure underlies submodular sensor placement for outbreak detection
[@leskovec2007]. Candidate agencies are scanned in sorted label order, so ties
break by label rather than by however the network's node tuple happens to be
ordered — a determinism that survives reordering the input.

### Compromise cascade

The infiltration model simulates the brotherhood's defining weakness: turn one
operative and their cellmates, superior, and subordinates are exposed. A
round-based cascade propagates this through the organisation, each exposed
operative turning with a fixed probability — an independent-cascade process
[@kempe2003] read as percolation on the org graph [@newman2002]. Every
non-terminal round adds at least one operative to the compromised set, which is
bounded by the organisation's size, so the process terminates without an
imposed round cap. We report the expected fraction compromised, the rate at
which leadership is reached, and the mean number of rounds to leadership,
averaged over fixed-seed trials whose per-trial seeds are derived from one base
seed.

### Sensor-placement cover

The placement model poses the surveillance programme as a set-cover problem
over agencies × targets: which agencies to place so that the required fraction
of targets is swept. The greedy set-cover heuristic [@johnson1974] selects
agencies by largest marginal gain and stays within a factor `O(log n)` of the
minimum cover, which is essentially the best any polynomial-time algorithm can
guarantee [@feige1998]; the search stops when no remaining agency adds a target,
so an unreachable target is reported as a gap rather than looped over. Coverage
redundancy measures the fraction of targets swept by at least two selected
agencies — a multi-sensor resilience metric.

## Results — NINE EYES: measured outcomes, headline numbers, and what they establish

All values below are produced by the NINE EYES mission provider's `execute`
step over the canonical dataset and injected as tokens; the same run also
writes which they were measured.

### Summary of measured results

Every quantity below is injected as a token from the NINE EYES mission
provider's `execute` output; none is typed by hand.

| Quantity | Measured value | Source module |
| --- | --- | --- |
| Group centralization over out-degrees | 0.9219 | `surveillance_net.group_centralization` |
| Inflow-share Herfindahl (even-spread floor) | 0.1361 (0.1250) | `surveillance_net.herfindahl_index` |
| Seeded cascade reach (mean, 50 trials) | 0.7556 | `surveillance_net.expected_cascade_coverage` |
| Hierarchy height (chain complete: true) | 2 | `org_intel.hierarchy_stats` |
| Cell compartmentalization | 0.8235 | `org_intel.compartmentalization` |
| Articulation points | 1 (US) | `network_geometry.articulation_points` |
| Global efficiency | 0.6806 | `network_geometry.network_efficiency` |
| Critical nodes (greedy) | US, FR, UK | `network_geometry.critical_node_order` |
| Total carried traffic / top link | 1360.0 / US->UK (200.0) | `traffic_intel.total_traffic` |
| Monitored coverage (3 agencies) | 0.9669 | `traffic_intel.monitor_allocation` |
| Expected compromise (leadership) | 0.4771 (0.58) | `infiltration.expected_damage` |
| Set cover (4 agencies) | redundancy 0.2500, uncovered 0 | `signal_cover.greedy_set_cover` |

### Surveillance-network centralization

The NINE EYES network comprises 9 agencies and
13 directed data-sharing links. The measured group
centralization index over out-degrees is 0.9219:
sending concentrates strongly on one agency.

The inflow-share Herfindahl index does **not** corroborate that reading, and is
not reported as if it did. It measures 0.1361
against a floor of 0.1250 — the value an
inflow-share vector spread perfectly evenly over the
8 agencies that receive anything would take.
Sitting that close to the floor means received volume is nearly uniform across
those agencies. The two indices are measuring opposite ends of the same edges,
and on this network they disagree: concentration is a property of the sending
side only.

A signal seeded at the largest sender propagates to a mean
0.7556 of the network over 50
seeded cascade realizations. This is an estimated expectation, not a single
draw; individual realizations range widely either side of it, and no single
realization is quoted anywhere in this report.

![The Nine Eyes agency network. Node area is betweenness centrality and arrows are directed data flows. The largest sender (ringed, marked ▸) has betweenness exactly 0 — no shortest path passes through a pure source — so it is drawn at the minimum node size despite originating most of the traffic; the figure title names both readings.](output/figures/spectre_network_flow_centralization.png)

### Criminal-org cell model

The 7 brotherhood operatives — one node per distinct
film character, see §5 — are partitioned into
3 cells. The organization's command chain is complete
(true) — every operative is reached by a breadth-first
walk from the apex — with a hierarchy height of 2
links. Cell compartmentalization measures 0.8235: the
brotherhood keeps a high (but imperfect) degree of separation between its
cells, the imperfection coming from command edges that cross cell boundaries.

![The SPECTRE brotherhood command tree. Node colour is the operative's cell, the ringed node is Mr White (the operative seeded in the compromise cascade), and the violet-highlighted nodes are the set his turn exposes — cellmates, superior and subordinates — drawn live from `org_intel.exposure`.](output/figures/spectre_brotherhood_cascade.png)

### Network geometry

The canonical network is connected and has 1
articulation points (US) whose removal would
disconnect it, and a global efficiency of 0.6806. The
greedy critical-node ordering identifies
US, FR, UK as the agencies whose neutralization most fragments
the network. In the film, removing exactly this coordinating hub collapses the
brotherhood's reach — the model reproduces that dependence quantitatively, and
the ordering is the targeted-attack profile of a hub-dominated network
[@albert2000].

### Traffic interception

The canonical exchange carries 1360.0 volume units; the
single largest flow is US->UK (200.0), confirming the hub's
dominance. Greedy budgeted monitoring selects US, DE, ES,
and monitors 0.9669 of all traffic with only
3 agencies — a demonstration of diminishing marginal
returns that motivates the submodular formulation, and the reason the greedy
selection is worth reporting despite being an approximation.

### Compromise cascade

Turning a single cell operative causes an expected
0.4771 of the brotherhood to fall within the cascade;
leadership is reached with probability 0.58 after a
mean of 1.17 rounds. The model quantifies why a
compartmentalized brotherhood guards its cells: any cell breach is a vector
straight to the apex, and the short mean path there is a direct consequence of
the same cross-cell command edges that depress the compartmentalization score
above.

### Sensor-placement cover

The greedy set cover places 4 agencies
(CA, DE, FR, UK) to sweep the full target set, leaving
0 targets uncovered. The resulting multi-sensor
redundancy is 0.2500 — the fraction of targets swept by at
least two agencies, i.e. The resilience of the sweep to the loss of a single
agency. Coverage and redundancy pull against each other: the greedy cover
optimizes for reaching every target, not for surviving an agency's loss, so a
placement that maximizes redundancy would need a larger budget.

## Conclusion — NINE EYES: findings, verdict, and what the mission establishes

The NINE EYES package demonstrates that a surveillance programme's vulnerability
is a *geometric* property. The measured out-degree centralization index and the
articulation-point analysis show a network whose connectivity collapses when
its hub — the single critical agency — is removed. The inflow-share Herfindahl
index does not support that conclusion and is not enlisted to: it sits just
above its even-spread floor, which is evidence that receiving is *not*
concentrated. Reporting it is worth doing precisely because it disagrees; the
brotherhood model quantifies both its
command completeness and its imperfectly compartmentalized cells; and the
geometry kernel identifies, greedily, the exact nodes whose removal fragments
the system. All of this is deterministic, computed from real data structures
over a canonical dataset, and free of mocked behavior — every number in this
report is a measured output of the NINE EYES mission provider's ``execute``
step.

The operational layer generalizes the same spirit from structure to action:
budgeted traffic interception is a submodular coverage problem, the
brotherhood's cell-breached compromise cascade is a percolation process on the
org graph, and sensor placement is a set cover — each solved with a real,
deterministic algorithm whose results (interception coverage, leadership-hit
probability, coverage redundancy) flow through the manuscript tokens. Two
findings connect across those layers. First, concentration is simultaneously
the network's efficiency and its weakness: the same hub dominance that lets
3 monitored agencies intercept
0.9669 of all traffic is what makes the critical-node
ordering so short. Second, a single turned operative reaching leadership with
probability 0.58 is precisely the exposure the
compartmentalized brotherhood exists to prevent — and the residual cross-cell
command edges that make it possible are the same ones that hold its
compartmentalization at 0.8235 rather than at unity.

What carries beyond this film package is the shape of the thing:
6 independent, standard algorithms over one
canonical dataset, behind one frozen protocol. The pure domain core imports
only ``numpy`` and the standard library, so it remains importable in any
environment; the ``bond_api`` ``MissionProvider`` contract is isolated in the
thin ``spectre.mission`` adapter, ready to be discovered and driven by the BOND
orchestrator alongside every other package in the fleet.

## Experimental Setup — NINE EYES: canonical scenarios, parameters, and configuration

### Dataset

The analysis runs over a fixed canonical dataset declared in
`src/spectre/mission.py`:

* **NINE EYES surveillance network** — 9 agencies
 (``UK, US, CA, AU, NZ, DE, FR, ES, SE``) with 13 directed
 data-sharing links, the United States at the hub;
* **SPECTRE brotherhood** — 7 operatives across
 3 cells, an apex leader, and one executive layer. The
 roster is a *distinct-person* roster: exactly one node per film character.
 An earlier revision of this dataset carried "Franz Oberhauser" (Blofeld's
 birth name — the same character) and both "Hinx" and "Bautista" (Mr Hinx
 again, the latter under his actor's surname) as separate operatives, which
 inflated the operative count and manufactured the executive layer that the
 hierarchy height then reported. Those aliases are gone;
* **Brotherhood edges are a modelling construct.** The film establishes
 Blofeld at the apex, Mr Hinx as an enforcer, Mr White as a former member,
 Madeleine Swann as his daughter and C as an inside collaborator, but it
 publishes no org chart. The cell assignment and the `superior → subordinate`
 edges are therefore chosen, not observed; the only fidelity claim made is
 that no two nodes are the same person;
* **Traffic scenario** — the same agency set carrying volume-weighted links
 (`spectre.traffic_intel.canonical_traffic_network`), sized so that no single
 agency observes the whole exchange and the interception problem is
 non-trivial;
* **Placement scenario** — an agency × target coverage matrix over eight sweep
 regions (`spectre.signal_cover.canonical_coverage_problem`), with deliberate
 cross-coverage so the greedy cover needs several agencies and retains
 measurable redundancy.

The network and brotherhood definitions are the ones hashed into the
provenance record; the traffic and placement scenarios are constructed by their
own modules and are fixed constants of those modules.

### Determinism

* One base seed, `_SEED` in `spectre.mission`, governs both cascades: it is
 passed to `spectre.surveillance_net.expected_cascade_coverage` and to
 `spectre.infiltration.expected_damage`, and each derives per-trial seeds as
 `seed + i`. The seed recorded in `Provenance` is therefore the seed the
 reported numbers were produced under — changing it changes them;
* fixed layout seed in the figure generator;
* deterministic tie-breaking by label in both greedy selections, so the results
 do not depend on input ordering;
* no wall-clock in persisted artifacts (``Provenance.wall_time_s == 0.0``);
* execution provenance carries a canonical SHA-256 ``input_hash`` of the
 mission inputs.

### Software environment

* Python 3.14.6 on Darwin arm64
* Numpy for numerical arrays, matplotlib for figure rendering, PyYAML for
 configuration, `bond_api` (FROZEN protocol) for the mission contract.
* The 6 domain modules
 (infiltration, network_geometry, org_intel, signal_cover, surveillance_net, traffic_intel) import only numpy and the standard library, so
 they run outside this environment unchanged.

### Mission flow

The provider implements the five FROZEN stages — ``brief``, ``recon``,
``plan``, ``execute``, ``debrief`` — declaring 3
objectives and executing a 6-step plan, one step per
domain module. It also registers 6 Q-branch gadgets for
cross-package use.

## Reproducibility — NINE EYES: verification gates, deterministic regeneration, and artifacts

### Deterministic regeneration

The entire artifact set regenerates byte-identical from a clean tree:

```bash
uv run python scripts/debrief.py # runs the full mission
uv run python scripts/generate_figures.py # writes the network figure
uv run python scripts/z_generate_manuscript_variables.py # hydrates tokens (runs LAST)
```

Each script recomputes its results from the fixed canonical dataset; there is
no stored intermediate that could drift from the code. The mission record,
figure and hydrated manuscript are written under `output/` (git-ignored,
regenerable).

The claim is scoped precisely. **Within one software environment**, two full
regenerations produce byte-identical `output/` artifacts — mission record,
figure PNG, `manuscript_variables.json` and every hydrated section — because
hydration is a pure function of the committed tree: no wall clock, no untracked
RNG, no run counter. The single environment-dependent value is the interpreter
stamp printed at the end of this section (`Darwin arm64`, `3.14.6`),
which by construction is what changes when the environment changes; the
manuscript's date is `paper.date` from `docs/manuscript/config.yaml`, a committed
input, not the time of the run. `tests/test_regeneration_determinism.py`
enforces the claim by regenerating the whole artifact set twice in one test
run, more than a wall-clock tick apart, and comparing SHA-256 digests file by
file — a re-introduced `datetime.now` anywhere in the pipeline turns it red.

### Provenance

Execution provenance records the package version, the deterministic seed, and
the SHA-256 ``input_hash`` of the mission inputs — a canonical, key-sorted JSON
serialization of the agency network and the brotherhood — so any outcome can be
reproduced solely from its persisted record. `data/claim_ledger.yaml` carries
one row per measured manuscript token — the recorded value alongside the
function that produced it — and that coverage is enforced rather than asserted:
`tests/test_claim_ledger.py` compares the ledger against
`measured_tokens(generate_variables)` and fails on a measured token with no
row, a row for a token that is no longer measured, or a recorded value the code
no longer produces. The token partition is an exclusion list (only
configuration prose and the environment stamp are exempt), so a newly added
metric is covered automatically and exempting one takes a deliberate edit.

### No hand-authored numbers

Every quantity in this manuscript is an injected token resolved by
`src/spectre/manuscript_variables.py` from the measured mission output. Two
tests keep that honest: a live cross-reference test fails if any token used in
prose is missing from the generator, and strict resolution fails if any token
survives substitution. Even the package's own inventories — module count,
gadget count, plan length — are measured from the code rather than typed.

### Gates

* `uv run pytest tests/ --cov=src --cov-fail-under=90` — the coverage gate
 (line **and** branch, enforced on `src/`)
* `uv run ruff check src/ scripts/ tests/` and `uv run ruff format --check`
* `uv run mypy src/ scripts/`
* zero mocks anywhere in `tests/`; the pure domain core has no `bond_api`
 import, proven by a subprocess import test

The achieved coverage and test count from the last real run are recorded in
`docs/_generated/COUNTS.md`; this manuscript deliberately does not restate them,
because a number quoted in prose is a number that can go stale.

Release 0.1.0, dated 2026-08-04 (from
`docs/manuscript/config.yaml`), hydrated on Darwin arm64 with Python
3.14.6.

## Scope and Related Work — NINE EYES: boundaries, positioning, and relationship to the literature

### What this package claims

NINE EYES is a *modelling* package, not an intelligence product. It claims
exactly three things, each verifiable by running the code:

1. The film's premises — a hub-dominated surveillance-sharing exchange and a
 compartmentalized brotherhood — admit precise, standard formalizations:
 directed-graph centralization, a cell partition over a command tree,
 undirected connectivity geometry, weighted interception coverage,
 percolation on the org graph, and set cover.
2. Under those formalizations the canonical dataset yields the measured values
 reported in §3, deterministically, from a fixed seed and a fixed input whose
 SHA-256 is recorded on every outcome.
3. Every number in this manuscript is produced by that computation and injected
 as a token; none is typed by hand.

It claims nothing about any real surveillance arrangement. The canonical
network is a fictional construction sized to the film's conceit
(9 agencies, 13 directed links), chosen
so that each algorithm has something non-trivial to find. The brotherhood
roster is one node per distinct film character, but its cell partition and
command edges are chosen rather than observed (§5): the organisational
*structure* is a modelling construct, and no claim of canonical fidelity is
made for it.

### Out of scope

- **Empirical validation.** There is no ground-truth dataset for the modelled
 quantities, so no accuracy claim is made or implied. The results are
 properties of a stated model over stated inputs.
- **Weighted or temporal graph dynamics.** The geometry and centrality layers
 are unweighted and static; only the traffic layer carries volumes, and no
 layer carries time.
- **Adversarial reaction.** The critical-node ordering and the monitoring
 allocation are one-shot optimizations against a fixed structure; the modelled
 organisation does not rewire in response.
- **Optimality.** Two of the six analyses use greedy heuristics with known
 approximation bounds rather than exact solvers (see below); the reported
 selections are the greedy ones.

### Related work by module

**Centralization and centrality.** Freeman's group centralization index
[@freeman1979] is the standard measure of how concentrated a network's degree
distribution is around a single actor; the general treatment of degree,
connectivity, and efficiency measures follows Newman [@newman2010]. Betweenness
is computed with Brandes' shortest-path accumulation [@brandes2001]. Flow
concentration reuses the Herfindahl–Hirschman index from industrial
organization [@hirschman1964] on the inflow-share vector, which gives a
concentration reading independent of the Freeman index — and, on this dataset,
a contradicting one (§3). Because the index is bounded below by `1/r` rather
than by 0, it is reported alongside that floor; quoting an HHI without its
floor invites reading an evenly-spread vector as a concentrated one, which is
exactly what an earlier revision of this report did.

**Connectivity geometry.** Articulation points come from Tarjan's low-link
depth-first search [@tarjan1972; @hopcrofttarjan1973]. Global efficiency is the
Latora–Marchiori mean inverse shortest-path length [@latora2001]. The
node-removal impact and robustness curve follow the error-and-attack-tolerance
framing of Albert, Jeong and Barabási [@albert2000]: fragmenting a
hub-dominated network takes few targeted removals and many random ones. The
greedy critical-node ordering is a key-player problem in the sense of Borgatti
[@borgatti2006], scored by pairwise-connectivity loss.

**Cascades.** The surveillance cascade and the infiltration cascade are both
independent-cascade processes in the sense of Kempe, Kleinberg and Tardos
[@kempe2003], which is also where the submodularity of coverage-style influence
objectives is established. The infiltration model's percolation reading — a
contagion spreading over a fixed contact structure — follows Newman's treatment
of epidemic spread on networks [@newman2002]; here the contact structure is the
brotherhood's exposure relation (cellmates, superior, subordinates) rather than
a social contact graph.

**Budgeted monitoring.** Interception coverage is monotone and submodular in
the monitored set, so the greedy rule carries the classic `(1 − 1/e)` guarantee
of Nemhauser, Wolsey and Fisher [@nemhauser1978]. The same structure underlies
sensor placement for outbreak detection [@leskovec2007], which is the closest
published analogue of the monitoring-allocation problem posed here.

**Placement as set cover.** The sensor-placement layer is minimum set cover,
solved with Johnson's greedy heuristic [@johnson1974] at its `O(log n)` factor;
Feige's threshold [@feige1998] establishes that no substantially better
polynomial-time approximation exists unless `NP` has quasi-polynomial-time
algorithms, which is why the greedy solution is reported rather than an exact
one.

### Position within the BOND suite

The suite's other packages model other films' concepts; this one owns
surveillance-network and criminal-organisation intelligence. Cross-package
reuse happens through `bond-api`, never by importing another film's `src/`. The
package exposes 6 pure domain modules
(infiltration, network_geometry, org_intel, signal_cover, surveillance_net, traffic_intel) behind one frozen `MissionProvider` and
6 registered Q-branch gadgets, and its `execute` stage
runs a 6-step plan. Anything a sibling package needs from
NINE EYES it obtains through those interfaces.

### Threats to validity

- **Canonical-dataset dependence.** All reported values are properties of one
 fixed input. A different agency network or brotherhood would give different
 numbers; the algorithms, not the numbers, are the reusable contribution.
- **Greedy selection.** The monitoring allocation and the placement cover are
 approximations. Their guarantees are stated above, but a reported selection
 is not proof of optimality.
- **Cascade parameterization.** Cascade coverage and expected damage depend on
 the activation and turn probabilities, which are stated design choices rather
 than estimates. The models are used comparatively (which node, which agency,
 how much worse) rather than as absolute forecasts.
- **Cascade sampling error.** Both cascade figures are means over
 50 seeded realizations, not closed-form
 expectations. No confidence interval is reported, so the trailing digits of
 those two numbers should not be read as significant; they would move under a
 different base seed or trial count.
- **Unweighted geometry.** Treating the sharing graph as unweighted for the
 connectivity layer discards the volume information the traffic layer uses. The
 two layers deliberately answer different questions and their results should
 not be pooled.

## Sources — NINE EYES: bibliography

@freeman1979; @newman2010; @brandes2001; @tarjan1972; @nemhauser1978; @johnson1974; @feige1998; @newman2002; @hopcrofttarjan1973; @latora2001; @albert2000; @borgatti2006; @hirschman1964; @kempe2003; @leskovec2007


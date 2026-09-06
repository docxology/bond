# Casino Royale (1967) — FIVE BONDS

*film package · package codename FIVE BONDS*. Mission **FIVE 00s**: model coordination failure across the five overlapping Bonds; simulate dispatch chaos and protocol violations deterministically; analyze the spoof ops doctrine and quantify its deviation; quantify identity confusion and resolve dispatch sightings by Bayes; derive exact baccarat table odds and the five-Bond table collision; model doctrine escalation as an absorbing Markov chain.

## Concepts — FIVE BONDS: domain and operational focus

multi-agent farce, coordination failure

## Abstract — FIVE BONDS: mission summary

*Casino Royale* (1967) is the spy farce in which five different operatives answer to the same codename, James Bond. This project — codename **FIVE 00s** — builds deterministic mission software around that premise. It implements and tests six concepts drawn from the film's organizational failure: 1. **Coordination-farce model** (`coordination_farce.py`): a roster of 5 agents who all share the codename *James Bond*, assigned across 6 tasks. It detects **overlap**, **conflict**, and clearance violations, and computes a weighted coordination loss of **15** from 3 overlaps and 3 conflicts. 2. **Dispatch-chaos simulation** (`dispatch_chaos.py`): a tick-based dispatch centre issues 13 orders and enforces 5 protocol rules; 5 dispatch successfully, 8 are rejected, for a chaos index of **0.62**. 3. **Spoof protocol analyzer** (`spoof_analyzer.py`): lexical scoring of satirical ops doctrine against a sane protocol; the film's standing orders score **45.0 / 100**. 4. **Identity-confusion model** (`identity_confusion.py`): information theory over the shared codename — routing carries only 0.075 normalized mutual information, leaving a dispatch ambiguity `H(routed | intended)` of 2.135 bits, and a Bayesian sighting resolves to *bond_cooper* with confidence 0.613. 5. **Baccarat table model** (`baccarat_table.py`): combinatorial deal odds exact for the infinite-deck model (player 0.4461, banker 0.4584, tie 0.0954) and a 5-Bond table collision probability of 0.704 under an i.i.d.-across-hands approximation. 6. **Escalation-ladder model** (`escalation_ladder.py`): the doctrine as an absorbing Markov chain — the spoof doctrine reaches catastrophe in 4.0 steps versus 56.0 under discipline, a 14.0× acceleration. All six models are deterministic (fixed seed, no random draws, no wall clock in artifacts) and are exposed through a `MissionProvider` implementing the frozen `bond_api` protocol, with a gadget registry and publication-style figures. Keywords: 5-agent coordination failure, agent dispatch simulation, protocol violations, satirical ops doctrine, identity confusion, baccarat odds, absorbing Markov chains, reproducible research.

## Introduction — FIVE BONDS: mission framing, the operational problem, and how to read this chapter

The 1967 film *Casino Royale* [@casinoroyale1967film] is not one Bond but many. Sir James Bond
(played by David Niven) is recalled from retirement; the would-be successor
is a baccarat prodigy (Peter Sellers as Evelyn Tremble); a Soviet defector
(Ursula Andress as Vesper Lynd) doubles as a double-0; and James Bond's
anxious nephew (Woody Allen as Jimmy Bond) and a field agent (Terence Cooper)
both answer to the same codename. Every operative introduces themselves as
**James Bond**. The result is a coordination catastrophe dressed as a
blockbuster: overlapping identities, overlapping assignments, and directly
contradictory orders.

**FIVE 00s** turns that farce into a rigorous, deterministic model. This
manuscript documents six complementary concepts, each implemented as a pure
Python module with no mocks and verified by real computation:

- **Multi-agent coordination failure** (`coordination_farce.py`) — overlap and
 conflict detection over a roster of 5 overlapping Bonds
 across 6 tasks, with a weighted loss and a single-agent
 remedy.
- **Agent dispatch chaos** (`dispatch_chaos.py`) — a tick-based simulation in
 which the dispatch centre cannot tell its Bonds apart, so violations of
 5 protocol rules accumulate.
- **Spoof protocol analysis** (`spoof_analyzer.py`) — automatic measurement of
 how far a satirical ops doctrine (the film's standing orders) deviates from
 a sane protocol of 6 rules.
- **Identity confusion** (`identity_confusion.py`) — information theory
 [@shannon1948communication] over the shared codename: a routing confusion matrix, entropy, mutual
 information, and Bayesian resolution of a dispatch sighting.
- **The baccarat table** (`baccarat_table.py`) — exact chemin de fer deal odds
 by enumeration, plus the birthday-model probability that two of the
 5 Bonds at the table are dealt the same hand total.
- **The escalation ladder** (`escalation_ladder.py`) — doctrine as an
 absorbing Markov chain over 5 states, compared
 against a disciplined doctrine through expected absorption times.

The whole package is wired into the PROJECT BOND suite: a `MissionProvider`
(`src/casino_royale_1967/mission.py`) implements the frozen `bond_api`
protocol, the five mission phases are exposed as thin CLIs under `scripts/`,
and 6 manuscript figures are generated deterministically
from the same analyses the mission executes. Metrics in this manuscript are
never hand-authored — they are injected live from `docs/manuscript/config.yaml` and
`src/casino_royale_1967/manuscript_variables.py`.

### Reader's guide

- **Methodology** describes the six algorithms in module order: assignment
 analysis, tick-based dispatch, lexical doctrine scoring, the
 information-theoretic identity model, exact baccarat enumeration, and the
 absorbing-chain escalation ladder.
- **Results** reports the canonical metrics and the 6
 figures.
- **Experimental setup** lists the configuration parameters.
- **Reproducibility** describes how every artifact can be regenerated
 byte-identically.
- **Scope and related work** states what the models deliberately do not claim.

## Methodology — FIVE BONDS: the analytical models and algorithms that drive the mission

### 1. The coordination-farce model

`src/casino_royale_1967/coordination_farce.py` models the organizational
failure behind *Casino Royale*. The model has three parts: a static roster,
an assignment set, and an analysis function.

**Roster.** A tuple of 5 `Agent` instances, each with an
id, the actor who played them (David Niven, Peter Sellers, Ursula Andress,
Woody Allen, Terence Cooper), a clearance level (1–5), a jurisdiction, and a
codename. Crucially, **all five share the codename `James Bond`** — the
roster is a duplicate-identity dataset by construction.

**Tasks.** A `Task` catalog of 6 operations drawn from the
film's plot, each with a required clearance and an exclusivity flag. Tasks
include winning the baccarat championship, infiltrating SMERSH headquarters,
guarding the casino vault, seducing Mata Bond, disabling the gamma-ray
projector, and burning the baccarat table for the insurance claim.
Mutually exclusive task pairs are captured in a conflict graph: *win the
baccarat championship* conflicts with *burn the baccarat table*.

**Analysis** (`analyze_assignments`). Given a tuple of `Assignment`s
(agent, task, priority), the function deterministically computes:

- **Overlap count** — every extra distinct agent beyond the first on a task.
 A task with three Bonds contributes two overlaps.
- **Conflict count** — every pair of *distinct* agents drawn one from each
 side of a conflicting task pair. A single operative assigned to both sides
 contributes nothing: that is a single-agent scheduling problem, not an
 inter-agent conflict. Each conflict-graph entry must name exactly two
 tasks, and a malformed entry raises rather than being silently skipped.
- **Clearance violations** — assignments where the agent's clearance is below
 the task's requirement (reported, not counted twice in the loss).
- **Coordination loss** — a weighted sum
 `loss = overlap_weight * overlap_count + conflict_weight * conflict_count`,
 with weights 2 and 3.

The canonical default `DEFAULT_ASSIGNMENTS` assigns 8
orders and produces the farce documented in the results: three Bonds at the
baccarat table, Cooper burning the same table, Vesper and Jimmy both at
SMERSH headquarters.

**Remedy** (`deduplicate_assignments`). Single-agent discipline keeps the
lexicographic maximum of `(priority, agent_id)` per task — highest priority
wins, and an exact tie goes to the greatest agent id, which makes the choice a
pure function of the assignment *set* rather than of its ordering — and
retires every other agent on that task. Those retired agents are exactly the
`overlap_victims` the analysis reports: both are derived from one shared
winner function, and `tests/test_coordination_farce.py` asserts the two
mappings are equal rather than merely the same size. Applied to the canonical
farce it keeps
5 assignments and drops 3,
eliminating every overlap and every duplicate-agent conflict. Only one
irreducible clash remains: a single agent must still win the baccarat
championship while a second burns the same table for the insurance claim, so
one conflict (loss equal to the conflict weight) persists.

### 2. The dispatch-chaos simulation

`src/casino_royale_1967/dispatch_chaos.py` simulates a dispatch centre that
cannot tell its agents apart. It is a tick-based, priority-ordered scheduler
with no randomness and no wall clock.

**Orders.** Each `DispatchOrder` names an order id, agent, task, priority, and
issue tick. Orders are processed in `issued_tick` order; within a tick, higher
priority first, ties broken by order id. State is deterministic: agents
committed to a task persist across ticks (task occupancy), and agents
committed to a task within the current tick are re-checked for double-booking.

**Protocol rules.** 5 rules are enforced per order,
in this order:

1. `duplicate_order` — an order id issued twice is rejected;
2. `exclusive_task` — an exclusive task may hold only one agent;
3. `clearance` — the agent's clearance must meet the task requirement;
4. `double_booking` — one agent may not take two tasks in the same tick;
5. `duplicate_codename` — if another agent with the *same codename* already
 occupies a task, the order is rejected (the dispatch centre mistakes the
 Bonds for one another).

A rejected order is dropped, never requeued: chaotic dispatch loses orders.

**Output.** `simulate_dispatch` returns a `DispatchReport` with total,
dispatched, and rejected counts, every `DispatchViolation` with the rule that
fired, the success ratio, and a chaos index equal to
`violations / total_orders`, normalised to `[0, 1]`. The canonical scenario
issues 13 orders within a horizon of 100
ticks (orders issued beyond the horizon are ignored).

### 3. The spoof protocol analyzer

`src/casino_royale_1967/spoof_analyzer.py` measures how far a satirical ops
doctrine deviates from a sane protocol. It combines lexical marker scoring,
rule-contradiction detection, and oxymoron detection.

**Sane doctrine.** `REAL_OPS_RULES` lists 6 rules (classified identity,
single point of command, covert discretion, proportional force, no
fratricide, single agent per operation). The analyzer treats these as the
ground truth the farce inverts.

**Markers.** `SPOOF_MARKERS` weights absolutist or inverted vocabulary
(`every`, `anyone`, `all`, `none`, `maximum`, `in case of doubt`,
`blow up`, `shoot`, `identical`, `never`, `always`). Matching is
word-boundary aware so `any` does not fire inside `anyone` and `all` does not
fire inside `calling`.

**Scoring.** For each directive, `analyze_doctrine` computes:

- the **marker score** — the sum of weights of markers present;
- **inverted rules** — real rules whose keyword appears together with an
 absolutist marker, i.e. a discretionary rule turned absolute;
- **oxymorons** — self-contradicting phrase pairs from `OXYMORON_PAIRS`
 (classified + publicity, discreet + explosion,...).

The per-directive score is
`marker_sum + 2.0 * len(inverted_rules) + 1.5 * len(oxymorons)`. The
aggregate **spoof index** is the mean score scaled to `[0, 100]`
(`min(100, mean * 10)`), rounded to one decimal. The film's canonical
standing orders comprise 8 directives.

### 4. The identity-confusion model

`src/casino_royale_1967/identity_confusion.py` quantifies the codename
collapse with information theory and Bayesian inference.

**Confusion matrix.** Each agent is represented by a feature vector: its
clearance normalized to `[0, 1]`, concatenated with a one-hot over the
roster's distinct jurisdictions (diplomacy, gambling, seduction, accounting,
field ops). Routing confusion `confusion[i][j]` — the probability an order
intended for agent *i* is routed to agent *j* — is a row-softmax over pairwise
feature similarity `f_i · f_j` scaled by a temperature. The matrix is
row-stochastic and deterministic. Note that the codename contributes no
feature at all, because it is identical for every agent; this is exactly why
the routing signal is so weak.

**Entropy / mutual information.** With a uniform prior over the five Bonds,
the model computes these quantities, all in bits
[@shannon1948communication; @cover2006elements]:

- `H(intended)` — Shannon entropy of the intended identity
 (2.322 bits for a uniform roster);
- `H(routed)` — entropy of the marginal routing distribution
 (2.310 bits);
- `H(routed | intended)` — the forward conditional entropy, reported as the
 **dispatch ambiguity** of 2.135 bits: given the Bond
 an order was meant for, this much uncertainty remains about where it lands;
- `I = H(routed) - H(routed | intended)` — the mutual information
 (0.175 bits actually recovered by observing the routing);
- `H(intended | routed) = H(intended) - I` — the *reverse* conditional
 entropy (2.147 bits), what remains unknown about the
 intended Bond once the routing has been seen. `residual_identity_entropy`
 computes it separately precisely because it is not the same number as the
 dispatch ambiguity, and swapping the two is the arithmetic error the results
 section calls out;
- `NMI = I / max(H(intended), H(routed))` — the mutual information normalized
 to `[0, 1]` [@strehl2002cluster], where `0` means routing is independent of
 intent.

Because all five agents share one codename, the *codename* itself carries `0`
bits: the shared name is pure identity loss, and only the clearance and
jurisdiction features carry any signal at all.

**Bayesian resolution.** Given a dispatch sighting's evidence — whether the
presented jurisdiction matched the task's and whether clearance was
sufficient — `resolve_identity` computes the posterior over the roster with a
uniform prior and an independent jurisdiction/clearance likelihood table. The
argmax is the resolution, its mass the confidence.

### 5. The baccarat table model

`src/casino_royale_1967/baccarat_table.py` models the casino set-piece with
exact enumeration.

**Hand valuation.** Baccarat hands total modulo 10; 10/J/Q/K count as 0;
a two-card total of 8 or 9 is a *natural* that ends the deal immediately.
The player draws on 0-5 and stands on 6-7; the banker follows the standard
chemin de fer table keyed on its total and the player's third card.

**Deal odds.** `deal_outcome_probabilities` enumerates every draw outcome
(four to six cards) under the drawing rules, weighting each card by its
value's share of the deck — the industry-standard infinite-deck baccarat odds
computation. For the 52-card standard it reproduces the canonical published
figures (player 0.4461, banker 0.4584,
tie 0.0954), with the banker's historical advantage of
+0.0123.

**The farce metric.** `two_card_total_counts` computes the *exact*
no-replacement marginal distribution of a two-card hand total from the actual
deck; `hand_collision_probability` then applies the birthday bound — the
elementary symmetric polynomial `n! * e_n(p_0..p_9)` — to answer: across
5 Bonds at the table, what is the probability at least
two are dealt the same hand total? Under the documented
i.i.d.-across-hands approximation the answer is 0.704.

That approximation is the model's one inexact step and is stated rather than
hidden. The marginal for a *single* hand is exact and without replacement, but
the birthday product treats the 5 hands as independent
draws from that marginal, whereas a real deal removes each dealt card from the
shoe and so correlates the hands. `test_iid_approximation_is_not_exact` in
`tests/test_baccarat_table.py` brute-forces every deal of a small deck and
shows the two values disagree, so the approximation is documented by a failing
comparison rather than asserted. The exact figure for a 52-card shoe and five
hands is not computed here.

### 6. The escalation-ladder model

`src/casino_royale_1967/escalation_ladder.py` models doctrine as an absorbing
Markov chain (Kemeny-Snell analysis [@kemeny1960finite], exact numpy linear
algebra).

The 5-state ladder
`quiet → rumour → scandal → spectacle → catastrophe` has `catastrophe`
absorbing. A doctrine is a row-stochastic transition matrix
(`SPOOF_DOCTRINE_TRANSITIONS`, `SANCTIONED_DOCTRINE_TRANSITIONS`).

**Deriving the absorbing set.** Validation rejects any matrix that is not
square, not row-stochastic, or has a negative entry, and then identifies the
absorbing states *from the matrix itself*: a row `i` with `P[i, i] = 1` and no
off-diagonal outflow. A matrix with no absorbing row, or with no transient row
left, is rejected. Nothing keys off a state's *name*, so a caller may supply
any state labels in any order and get the same physics — a property pinned by
a reversed-ladder regression test.

The analysis then computes:

- the **fundamental matrix** `N = (I - Q)^{-1}` over the transient states;
- the **expected absorption time** `t = N @ 1` from each state — the expected
 steps to catastrophe;
- the **spectral radius** of `Q` as the largest complex modulus of its
 eigenvalues (a value below 1 guarantees absorption);
- the **absorption probability** `B = N R`, summed over every absorbing state.

`compare_doctrines` reports the **escalation index** (expected steps from
`quiet`) under each doctrine and the acceleration factor
`sanctioned / spoof`: the farce reaches catastrophe in
4.0 steps versus 56.0
under discretion — 14.0× faster.

## Results — FIVE BONDS: measured outcomes, headline numbers, and what they establish

### The five-Bond coordination farce

The canonical assignment set of 8 orders across the
5-agent roster produces 3 overlaps
and 3 conflicts. Three Bonds crowd the baccarat
table; Vesper and Jimmy both infiltrate SMERSH headquarters; and Cooper's
order to burn the baccarat table conflicts with the three agents assigned to
win the championship on that same table. Conflicts are counted between
*distinct* agents only, so an operative holding both sides of a mutually
exclusive pair is a scheduling problem rather than a conflict.
1 clearance violation is recorded:
`bond_jimmy` (Woody Allen), clearance
2, sent to *infiltrate SMERSH headquarters* — an
operation requiring clearance 4.

![Per-task agent load; bars above the dashed line are overlaps.](output/figures/casino_royale_1967_coordination_farce.png)

The weighted **coordination loss** is **15**
(weights 2 for overlap and
3 for conflict). Applying single-agent discipline
keeps 5 of the 8 assignments and
drops 3, eliminating every overlap; only the
irreducible clash between winning and burning the baccarat table remains, at
one conflict (loss 3).

### Dispatch chaos

The dispatch simulator issues 13 orders; 5
dispatch successfully and 8 are rejected as protocol
violations, for a success ratio of 0.38 and a chaos index
of **0.62**. All 5 protocol rules
fire at least once (5 of 5
distinct rules triggered), so the scenario is a positive control for the whole
rule set rather than a narrow subset:

| Protocol rule | Rejections |
|---|---|
| `exclusive_task` | 2 |
| `clearance` | 2 |
| `double_booking` | 2 |
| `duplicate_order` | 1 |
| `duplicate_codename` | 1 |

![Dispatch timeline: accepted orders vs protocol violations per tick.](output/figures/casino_royale_1967_dispatch_chaos.png)

The dominant failure mode is identity collapse: because all five agents share
the codename *James Bond*, the dispatch centre repeatedly mistakes one agent
for another and misroutes the under-cleared nephew onto cleared operations.

### Spoof ops doctrine

The film's standing orders of 8 directives score a
**spoof index of 45.0 / 100**, with a mean per-directive
score of 4.50. The worst offender is
*"In case of doubt, blow up the table."* — an inversion of the proportionality principle.

![Per-directive spoof scores with the aggregate index in the title.](output/figures/casino_royale_1967_spoof_analyzer.png)

Contradiction detection attributes the scores across the sane rule surface
(identity, single-agent discipline, command, discretion, force, fratricide):
6 of the 6 declared rules
are contradicted at least once, so the analyzer exercises every rule rather
than a narrow subset.

### Identity confusion

The five Bonds share one codename, and the resulting identity collapse is
measured in bits. Routing carries only
**0.075 normalized mutual information** (a near-zero value:
the observed routing reveals almost nothing about which physical Bond was
intended) — 0.175 bits of mutual information in absolute
terms. Two distinct conditional entropies follow from that, and they are not
interchangeable [@cover2006elements]:

| Direction | Reading | Bits |
|---|---|---|
| `H(routed \| intended)` | knowing who the order was *for*, how uncertain its destination is | 2.135 |
| `H(intended \| routed)` | seeing where the order *landed*, how uncertain its author's intent is | 2.147 |

The first subtracts the mutual information from the routing entropy
(2.310 bits); the second subtracts it from the
prior entropy of the intended identity
(2.322 bits). This manuscript reports the first as
the **dispatch ambiguity**; the phrase "bits of identity lost per dispatch"
refers to that forward direction and must not be computed as
prior minus mutual information, which yields the second, larger figure.
A Bayesian sighting (jurisdiction match + clearance sufficiency) at
the SMERSH operation resolves to *bond_cooper* with
posterior confidence 0.613.

![Routing confusion matrix across the five Bonds.](output/figures/casino_royale_1967_identity_confusion.png)

### The casino table

The baccarat table model derives the deal odds under the standard
chemin de fer drawing rules: **player 0.4461, banker
0.4584, tie 0.0954** (a banker advantage
of +0.0123) — the canonical infinite-deck figures
[@ethier2010doctrine], exact for the with-replacement model the enumeration
implements.

The farce lives at the table itself: with all 5 Bonds
seated, the probability that at least two are dealt the same hand total is
**0.704** — a hand-collision farce more likely than not.
That figure is not exact. Each Bond's two-card total is drawn from the exact
no-replacement distribution of a single hand, but the five hands are then
combined as if independent, whereas in a real deal they compete for the same
shoe. The number is therefore the collision probability *under the
i.i.d.-across-hands approximation* the code documents, and
`tests/test_baccarat_table.py` exhibits a small deck on which that
approximation is measurably wrong — it is a modelling assumption, not a
rounding detail. Its magnitude for a full standard shoe is not quantified
here; `TODO.md` records that gap as an accepted, open limitation.

![Casino table deal odds with the five-Bond collision probability.](output/figures/casino_royale_1967_baccarat_odds.png)

### Escalation ladder

Modelled as an absorbing Markov chain over the
5-state ladder
`quiet → rumour → scandal → spectacle → catastrophe`, the spoof doctrine
reaches catastrophe in **4.0 expected steps**, while a
disciplined doctrine takes 56.0 — the farce
escalates **14.0× faster**.

Absorption is certain rather than assumed: the transient block of the spoof
doctrine has spectral radius 0.400 (strictly below
one), and the absorption probability into
*catastrophe* from `quiet` is
1.000. The absorbing set is derived from the
transition matrix itself — a row with a unit diagonal and no outflow — never
from a state's name, so relabelling or reordering the ladder cannot change the
analysis.

![Expected steps to catastrophe per state, by doctrine.](output/figures/casino_royale_1967_escalation_ladder.png)

## Conclusion — FIVE BONDS: findings, verdict, and what the mission establishes

**FIVE 00s** turns the organizing joke of *Casino Royale* (1967) — five
operatives, one codename — into a rigorous, fully deterministic research
model. The project delivers six complementary concepts, each implemented in
pure Python, exhaustively tested with real computation, and wired into the
PROJECT BOND mission protocol:

1. the **coordination-farce model**, which turns the film's overlap and
 conflict into measurable quantities — 3 overlaps,
 3 conflicts, and a coordination loss of
 15 — and demonstrates that single-agent
 discipline removes all overlaps;
2. the **dispatch-chaos simulation**, which reproduces the logistics failure
 of a dispatch centre that cannot tell its Bonds apart
 (8 of 13 orders rejected; chaos index
 0.62);
3. the **spoof protocol analyzer**, scoring satirical ops doctrine at
 45.0 / 100;
4. the **identity-confusion model**, showing the shared codename collapses
 routing to 0.075 normalized mutual information, leaving a
 forward dispatch ambiguity `H(routed | intended)` of
 2.135 bits and a reverse residual
 `H(intended | routed)` of 2.147 bits, with a sighting
 resolved by Bayes to *bond_cooper*;
5. the **baccarat table model**, deriving deal odds exact for the
 infinite-deck model (player 0.4461, banker
 0.4584) and an approximate
 0.704 probability — i.i.d. across hands — that two of
 the 5 Bonds are dealt the same hand total;
6. the **escalation-ladder model**, showing the farce accelerates to
 catastrophe 14.0× faster than discretion
 (4.0 vs 56.0 steps).

The technical guarantees matter as much as the content: deterministic
artifacts, zero mocks, ≥90% line+branch coverage, exact enumeration and
absorbing-chain linear algebra, and a thin `MissionProvider` adapter whose
public shape stays stable for the fleet. A farce, modelled seriously, yields
the same reproducibility contract as any research experiment.

## Experimental Setup — FIVE BONDS: canonical scenarios, parameters, and configuration

### Configuration

All identity and experiment parameters are declared in
`docs/manuscript/config.yaml` and injected as tokens by
`src/casino_royale_1967/manuscript_variables.py` — never hard-coded in prose.

| Parameter | Value |
|---|---|
| Mission identity | Casino Royale (1967) |
| Mission codename | FIVE 00s |
| Package version | 0.1.0 |
| Number of agents | 5 |
| Number of tasks | 6 |
| Overlap loss weight | 2 |
| Conflict loss weight | 3 |
| Dispatch horizon (ticks) | 100 |
| Dispatch protocol rules enforced | 5 |
| Sane ops rules in the doctrine baseline | 6 |
| Escalation-ladder states | 5 |
| Casino table (Bonds seated) | 5 |
| Figures rendered | 6 |

Values in this table are read from `docs/manuscript/config.yaml` where the
parameter is a free choice (loss weights, dispatch horizon) and derived from
the domain modules where the parameter is structural (rule counts, ladder
size, figure count), so neither source can drift from the code.

### Software environment

- Python `>=3.10` — the declared supported range. The artifacts do
 not record which interpreter within that range produced them, which is what
 keeps them byte-identical across it.
- numpy and matplotlib for computation and rendering
- `bond-api` (frozen `MissionProvider` protocol, local path dependency)
- Deterministic seed 7; no random draws, no wall clock in artifacts.

### Artifact regeneration

Every artifact is regenerable from `scripts/`:

```bash
uv run python scripts/mission.py execute # mission outcome (deterministic JSON)
uv run python scripts/mission.py figures # the concept figures
uv run python scripts/z_generate_manuscript_variables.py # tokens + resolved tree
```

The last command is the authoritative one: it recomputes the token map,
re-renders every figure, and rewrites `output/manuscript/` with every token
marker resolved, failing loudly if any marker is unresolvable.

## Reproducibility — FIVE BONDS: verification gates, deterministic regeneration, and artifacts

### Determinism guarantees

Every artifact in this project is deterministic by construction:

- **Fixed seed.** The mission uses seed 7; the dispatch simulation makes no
 random draws at all — order processing is a pure function of the input
 order stream.
- **No wall clock in any persisted artifact.** Coordination, dispatch, and
 doctrine reports carry no timestamps; `Provenance.wall_time_s` is `0.0`; and
 the manuscript token map reads no clock at all — `generate_variables` takes
 no `now=` parameter, because an injectable clock with a wall-clock default is
 still a wall clock. This manuscript's date, 2026-08-04, is the
 committed `paper.date` in `docs/manuscript/config.yaml`; edit that file to change
 it, and it is otherwise fixed.
- **No interpreter state either.** The declared Python range is
 `>=3.10` — the committed `paper.python_requires`, held equal to
 `requires-python` in `pyproject.toml` by test. The token map introspects
 nothing about the machine that ran it.
- **Live computation.** Manuscript metrics are recomputed from the domain core
 at hydration time, so prose can never drift from code.

Because the token map is a pure function of committed files, regenerating with
`scripts/z_generate_manuscript_variables.py` reproduces
`output/data/manuscript_variables.json`, `output/manuscript/*.md`, and
`output/figures/*.png` **byte for byte**. That is not an aspiration:
`tests/test_regeneration_determinism.py` runs the generator twice in
succession, hashes every artifact under `output/`, and fails on any difference.

### Canonical metric snapshot

| Metric | Value |
|---|---|
| Assignments | 8 |
| Overlaps | 3 |
| Conflicts | 3 |
| Coordination loss | 15 |
| Clearance violations | 1 |
| Single-agent deduplication of assignments (kept / dropped) | 5 / 3 |
| Dispatch orders | 13 |
| Dispatched / rejected orders | 5 / 8 |
| Protocol violations | 8 |
| Chaos index | 0.62 |
| Success ratio | 0.38 |
| Spoof index | 45.0 / 100 |
| Identity NMI | 0.075 |
| Dispatch ambiguity `H(routed \| intended)` (bits) | 2.135 |
| Residual identity `H(intended \| routed)` (bits) | 2.147 |
| Baccarat player / banker | 0.4461 / 0.4584 |
| Table collision (5 Bonds, i.i.d.-across-hands approximation) | 0.704 |
| Escalation (spoof / sanctioned steps) | 4.0 / 56.0 |
| Acceleration factor | 14.0× |

### Verification

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/ && uv run ruff format --check src/ scripts/
uv run mypy src/ scripts/
```

The gate enforces ≥90% line+branch coverage on `src/`, zero mocks, and a clean
git tree after regeneration. Figures and the resolved manuscript tree live
under `output/`, which is git-ignored and regenerable.

## Scope and Related Work — FIVE BONDS: boundaries, positioning, and relationship to the literature

### Scope

**FIVE 00s** models the coordination failure motif of *Casino Royale* (1967)
at the level of deterministic, hand-built algorithms. It does not attempt:

- a general agent-based simulation framework (the tick model is purpose-built
 for the farce, not a full discrete-event engine);
- machine-learned or stochastic dispatch policies (dispatch is a pure
 function of the deterministic order stream);
- a normative claim about real organizational governance — the "chaos index"
 is a satirical diagnostic, not a validated operations metric.

The satirical doctrine in `CANONICAL_SPOOF_DOCTRINE` is analyzed as *text*:
the analyzer measures lexical inversion and rule contradiction, and makes no
claim about the film's production history or intent.

### Related work

The work sits at the intersection of several research threads:

- **Multi-agent coordination and conflict.** The overlap/conflict detection
 follows the classic line of research on coordination failure in multi-agent
 systems, where redundant or duplicative agents degrade system performance.
 The weighted-loss formulation is a small, reproducible instance of that
 family.
- **Information theory of identity.** The identity-confusion model applies
 Shannon's entropy and mutual information to quantify how much identity a
 shared codename destroys; the Bayesian resolution is a standard posterior
 update over the roster (Shannon 1948; Cover & Thomas 2006). The
 normalization of mutual information by the larger marginal entropy follows
 the convention of Strehl & Ghosh (2002).
- **Deterministic simulation and protocol verification.** The dispatch
 simulator's rule-checker mirrors property-based protocol enforcement: each
 order is checked against a fixed rule set, and violations are recorded as
 first-class data.
- **Gambling mathematics.** The baccarat table's deal odds reproduce the
 canonical published figures of the chemin de fer drawing rules; the
 hand-collision metric is a birthday-bound application over the exact
 two-card-total distribution [@ethier2010doctrine; @wizardofodds_baccarat].
 Deck count shifts these probabilities only slightly and does **not** reverse
 their order: the banker bet is still the better side at one deck in the
 published tables [@wizardofodds_baccarat]. An earlier draft of this section
 asserted the opposite — that single-deck play inverts the banker edge — which
 its own cited source contradicts. This model cannot settle the question
 either way: `deal_outcome_probabilities` weights each card by its value's
 share of the shoe *with replacement*, so it is an infinite-deck computation
 and carries no finite-deck depletion effect at all.
- **Absorbing Markov chains.** The escalation ladder's fundamental matrix and
 expected absorption times follow Kemeny and Snell's classical treatment.
- **Reproducible computational research.** The project ships live-computed
 manuscript metrics, deterministic artifacts, and a frozen protocol adapter.

The *Casino Royale* (1967) material itself is in the public cultural
domain; this project uses its plot beats (baccarat championship, SMERSH
headquarters, the gamma-ray projector, Mata Bond, the five-Bond premise) as a
satirical dataset, not as a claim about the film.

## Sources — FIVE BONDS: bibliography

@shannon1948communication; @kemeny1960finite; @ethier2010doctrine; @wizardofodds_baccarat; @casinoroyale1967film; @cover2006elements; @strehl2002cluster


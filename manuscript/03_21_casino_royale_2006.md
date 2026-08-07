# Casino Royale (2006) — LE CHIFFRE

*film package · package codename LE CHIFFRE*. Mission **LE CHIFFRE**: counter-play Le Chiffre at the high-stakes felt (pot odds + equity against his range); solve the river toy game by CFR to a near-Nash profile (game theory); price tournament survival with the Independent Chip Model (ICM); trace the chip flows funding the game and flag laundering (behavioural + network-level); plan an extraction route across the parkour city (ground/roof); triage the spiked martini and identify the digitalis source; infer Le Chiffre's archetype posterior from his observed actions.

## Concepts — LE CHIFFRE: domain and operational focus

game theory, financial crime

## Abstract — LE CHIFFRE: mission summary

**Casino Royale: LE CHIFFRE — Special-Agent Mission Software** is the special-agent mission software for the film *Casino Royale* (2006), mission codename **LE CHIFFRE**. It packages 8 deterministic, infrastructure-free domain modules — a Texas hold'em game-theory engine plus a counterfactual-regret (CFR) solver and the tournament Independent Chip Model, a Bayesian opponent-archetype inference model, a chip-movement money-laundering detector plus network-level financial-crime analytics, a parkour mobility-graph router, and a digitalis (cardiac-glycoside) poison triage — into a single `MissionProvider` bound to the frozen BOND-API protocol. The cores are exercised on one canonical scenario (seed-stable, no wall-clock in provenance). Against the loose range Le Chiffre's observed loose-aggressive tendencies select, the engine prices the hero hand on the final board at 45.62% equity against a pot-odds break-even of 16.67%, a margin of 28.96% that recommends **raise**. CFR on the river toy game converges to an average regret of 0.001 (polar equilibrium, game value 0.0974), ICM prices the freezeout bubble at factor 1.411, and the Bayesian model reads Le Chiffre as **loose-aggressive** (aggressive posterior 0.986). The chip-flow scanner ingests 41 movements across 8 players and flags the planted smurfer with a composite score of 2 (1 alert(s) total), confirmed by the network detector at risk 0.98. On the 6×6 quarter the speed-weighted solve short-cuts via the rooftops (cost 36.53, against 103.39 for the ground route under that same weighting) while the risk-weighted solve stays on the street (cost 15.31, against 17.95 for the rooftop route under *that* weighting) — each optimal only under its own objective. The tox triage isolates the spiked martini 3 of 5 samples at 4.5 ng/mL digoxin (severe toxicity, posterior 0.95). Every result shown here, and in the sections that follow, is computed live from the engines at manuscript-generation time — none is hand-authored.

## Introduction — LE CHIFFRE: mission framing, the operational problem, and how to read this chapter

*Casino Royale* (2006) follows the special agent against the banker-cipher
**Le Chiffre** — a name that literally means "the cipher". The story's set
pieces map onto a family of analytical problems that a real mission system
would have to solve, and each is implemented here as a serious, tested module
rather than a stunt. Four are the film's literal set pieces:

1. **The felt.** The climactic hand is a study in game theory: a hero hand on a
 dry board against an adversary whose range the hero can model, priced
 against the chips in the middle. Module: `poker_engine.py`.
2. **The capital.** Laundered money funds the stake; it travels as physical
 casino chips in structurally tell-tale patterns. Module:
 `laundering_detect.py`.
3. **The terrain.** The chase crosses a parkour-friendly city — ground
 streets, leapable rooftop gaps, climbable walls, droppable falls — which is
 exactly a weighted mobility graph. Module: `urban_routes.py`.
4. **The martini.** Bond's drink is spiked with digitalis, the cardiac
 glycoside with a notoriously narrow therapeutic index. Module:
 `poison_detect.py`.

Four more answer the question each set piece raises once it is taken seriously:

5. **What is the *equilibrium*, not just the price?** Pot odds decide one call;
 a solver decides a strategy. Counterfactual regret minimization on the river
 toy game recovers the polar equilibrium the finale depends on. Module:
 `poker_cfr.py`.
6. **What is a chip worth on the bubble?** In a freezeout, chips are not money:
 the Independent Chip Model converts stacks to prize equity and prices
 survival. Module: `icm.py`.
7. **What does the adversary's history actually license?** A raise count is not
 a read; a Dirichlet-multinomial posterior over archetypes is. Module:
 `opponent_bayes.py`.
8. **Is the laundering visible without a suspicious transfer?** The structural
 layer — concentration, centrality, communities, value conservation — finds
 the washer from the shape of the flow alone. Module:
 `laundering_network.py`.

Together these form the pure domain core (8 concept
modules: poker_engine, poker_cfr, icm, opponent_bayes, laundering_detect, laundering_network, urban_routes, poison_detect), each deliberately free of any framework,
`infrastructure.*` import, or bond-api dependency, so they stay importable in
isolation. A thin adapter, `mission.py`, implements the frozen BOND-API
`MissionProvider` (codename THE PROTOCOL) and folds their output into a single
deterministic mission outcome, alongside a catalogue of 11
published gadgets (`gadgets.py`) that other suite packages may call directly.

### Principles

- **Deterministic by construction.** Every RNG draw flows through a
 caller-supplied seeded:class:`random.Random`; provenance carries the seed
 and never a wall-clock reading. Three of the eight engines (CFR, ICM, and the
 Bayesian opponent model) are exactly enumerated and carry no RNG at all.
- **Real computation, zero mocks.** The numbers in this manuscript are engine
 output (exact enumeration, Monte-Carlo simulation, graph search, tox
 triage), verified by a ≥90% line-and-branch test suite.
- **One scenario, everywhere.** A single canonical scenario (see
 `src/casino_royale_2006/scenarios.py`) feeds the mission, the manuscript
 tokens, and the CLI, so a claim computed once is the claim shown everywhere.

### Reader's guide

The methodology section defines all 8 algorithms;
the results section reports their outputs on the canonical scenario and shows the
figures; the setup section documents configuration and the runtime environment;
the reproducibility section covers determinism, artifact layout, and the
verification gates; and the scope section states, per module, what is deliberately
out of scope.

## Methodology — LE CHIFFRE: the analytical models and algorithms that drive the mission

This section defines all 8 algorithms. All are pure
Python; none imports a framework, `infrastructure.*`, or bond-api. Full
signatures live in `src/casino_royale_2006/`: `poker_engine.py`,
`poker_cfr.py`, `icm.py`, `opponent_bayes.py`, `laundering_detect.py`,
`laundering_network.py`, `urban_routes.py`, `poison_detect.py`. The canonical
inputs every one of them is run on live in `scenarios.py`; the published
callables are catalogued in `gadgets.py`.

### Poker game-theory engine (`poker_engine.py`)

**Hand strength.** A card is an integer in `0..51` (`rank = card // 4 + 2`,
`suit = card % 4`). `evaluate_5` returns `(category, tiebreak_ranks)` for the
nine categories (straight flush down to high card), and `best_hand` takes the
best five-card subset of a seven-card hold'em hand by enumerating all
five-card combinations. This is exact — the tiebreak tuple hashes the hand
category and ordered kickers so two hands compare lexicographically.

**Equity.** Two estimators are provided. `exact_equity_turn_river` enumerates
all 990 two-card runouts after a flop for a heads-up match — exact, no RNG.
`monte_carlo_equity` simulates `N` random runouts for an arbitrary number of
players using a seeded RNG, returning per-player `(win, tie)` fractions.

**Pot odds.** Given a pot and the amount to call, the break-even equity is
`to_call / (pot + to_call)`, and the expected value of calling is
`equity·(pot + to_call) − to_call`. `recommend_action` emits `fold`, `call`,
or `raise` by comparing the equity margin (`equity − break_even`) to
thresholds. This is precisely the "price the pot is laying me" decision of the
final hand.

**Opponent modelling.** An `OpponentModel` records observed `raise`/`bet`/
`call`/`fold` actions and derives VPIP and an aggression factor
`(raises + bets) / calls`. `archetype` maps those two statistics to one of
four compound labels (`tight`/`loose` × `passive`/`aggressive`);
`range_key_for_archetype` then maps that label onto one of the two
`RANGE_ARCHETYPES` starting-hand ranges — `tight` and `loose`, hand-enumerated
as starting-hand *classes* (`AA`, `AKs`, `T9o`, …) rather than the full
169-class hold'em space. On the canonical scenario Le Chiffre's observed
history reads **loose-aggressive**, selecting the
**loose** range of 30 classes, from which
24 concrete pairs are drawn. `equity_vs_range` then averages
the hero's Monte-Carlo equity over those pairs — the number the agent compares
to the pot-odds price. Range fidelity is exact: a drawn hand is guaranteed
to match its class, so an offsuit class (e.g. ``AKo``) is always sampled with
two different suits and never silently treated as its suited sibling, which
would tilt the averaged equity toward suited runouts. The same label also sets the raise threshold, via
`recommended_raise_margin` (10% here), which is passed
to `recommend_action` as `raise_margin`.

### Chip-movement laundering detection (`laundering_detect.py`)

Chip flows are a directed graph from a signed `ChipTransaction` list
(`source`, `target`, `amount`, `tick`, `kind ∈ {cash_in, cash_out,
transfer}`), with the casino cage as a reserved node. Four typologies are
computed deterministically:

- **Structuring:** count of `transfer`s sized in `[threshold/2, threshold)`
 (the smurf band).
- **Round-tripping:** `A → B → A` rings completing within a tick window.
- **Velocity:** the maximum number of transactions a node participates in
 within a tick window (both directions — money washing *through* a node is
 the signal).
- **Chip parking:** a player who buys in, never transfers, and cashes out
 ~their full buy-in (value moved with zero game action).

An unweighted Brandes-style `betweenness` centrality identifies *collection
hubs* — nodes many smurf paths funnel through. `detect` accumulates a capped
composite score per player and emits an `Alert` (with supporting `evidence`)
once it clears a threshold.

### Parkour routing (`urban_routes.py`)

A `MobilityGraph` of `UrbanNode`s (x/y/height/kind) joined by directed
`UrbanEdge`s (`distance`, `difficulty`, `risk`, `move ∈ {run, leap, climb,
drop}`). A `ParkourProfile` encodes what the agent can physically execute
(max leap length, climb rise, drop fall, and global difficulty/risk caps);
`MobilityGraph.feasible` decides whether an edge is executable. `shortest_path`
runs **Dijkstra over only the feasible edges**, minimizing a weighted cost
`w_d·distance + w_f·difficulty + w_r·risk`, with a monotonic counter breaking
cost ties so identical-cost routes are reproducible. `brute_force_path`
exhaustively enumerates every simple path on small graphs and serves as ground
truth the Dijkstra output is verified against.

A route's reported cost is only meaningful *under the weighting that produced
it*: a speed-weighted and a risk-weighted solve return numbers in different
units, so their totals are not comparable. `MobilityGraph.path_cost` re-prices
an existing route under any weighting, and the results section uses it to state
both routes under both objectives rather than juxtaposing two incommensurable
totals.

### Digitalis poison triage (`poison_detect.py`)

A `ToxPanel` records serum digoxin (ng/mL), heart rate, serum potassium, PR
interval, and reported symptoms. Reference ranges — therapeutic `0.5–2.0`
ng/mL, toxicity above `2.0`, severe above `3.5`; bradycardia `< 60` bpm;
hyperkalemia `> 5.5` mmol/L; prolonged PR `> 200` ms — are declared as module
constants (`poison_detect.py`). `toxicity_score` combines a concentration band
with cardiac feature boosts and a symptom penalty; `toxicity_grade` thresholds
it into `none`/`mild`/`moderate`/`severe`. `posterior_toxicity` multiplies a
prior into a Bayesian posterior using documented likelihood ratios per present
sign, and `identify_poisoned_sample` picks the spiked glass from a tray by
highest posterior (tie-broken deterministically). `antidote_plan` returns the
intervention list (digoxin-specific Fab fragments for severe toxicity,
atropine for marked bradycardia, potassium management for hyperkalemia).

### Counterfactual regret minimization (`poker_cfr.py`)

The deep game-theory layer. CFR (Zinkevich et al., 2007) finds an approximate
Nash equilibrium of an imperfect-information game by iteratively reducing
counterfactual regret at each information set. This package solves the classic
*river toy game* — heads-up, antes of 1, out-of-position player `P1` checks or
bets 1, in-position `P2` folds or calls, with `CFR_STRENGTHS` discrete hand
strengths drawn uniformly — by fully enumerating the game (no RNG). Regret
matching turns positive regrets into mixed strategies; the reported average
strategy and `game_value` are the equilibrium shape the finale depends on.

### Independent Chip Model (`icm.py`)

The tournament-economy layer. ICM (Chen & Ankenman, 2006) converts chip stacks
into prize equity under the random-tournament model: `exact_icm_equity` uses
the recursive ``E_i = Σ_j (s_j/S)·E_i(S∖j, P[1:])`` for small fields and
`monte_carlo_icm` simulates finish order with a seeded RNG for larger ones. The
*bubble factor* — prize equity lost if the stack is risked and lost, over prize
equity gained by doubling up — exceeds 1 on the bubble, and `icm_call_ev` /
`icm_decision` decide a tournament call in prize-equity (not chip) terms.

### Network-level financial crime (`laundering_network.py`)

The structural-crime layer. Viewing chip flows as a directed graph, four real
measures run deterministically: **HHI concentration** over a player's
counterparty flow shares, **PageRank** (Page et al., 1999) ranking the
collection account that centrally-placed senders feed, **label propagation**
(Raghavan, Albert & Kumara, 2007) detecting deterministic trading communities,
and a **conservation imbalance** score. The composite `network_risk_report`
multiplies value-neutrality by turnover share — a money-washer (chips in ≈
chips out, no game losses) churning large volume is the signature — producing
an independent laundering detector from the typology scanner.

### Bayesian opponent archetype inference (`opponent_bayes.py`)

The read-the-adversary layer. Each of the four archetypes owns a Dirichlet
prior over actions; the Dirichlet-multinomial likelihood updates a posterior
`P(archetype | history)` in exact log space. `map_archetype` is the MAP
estimate, `predictive` is the model-averaged next-action probability, and
`expected_aggression` is the Bayesian expectation of the raise/bet rate — a
proper upgrade over the frequentist `OpponentModel` in `poker_engine.py`.

### Mission adapter and gadget catalogue (`mission.py`, `gadgets.py`)

The engines above are joined by exactly one adapter. `mission.py` implements
the frozen BOND-API `MissionProvider` — `brief → recon → plan → execute →
debrief` — declaring `film = "casino_royale_2006"` so the orchestrator can
discover it by slug. `execute` calls `scenarios.full_snapshot(SEED)` once,
folds each engine's real output into `MissionOutcome.results` under a
per-concept key, and attaches a `Provenance` record carrying the package
version, the seed, and a SHA-256 `input_hash` over the canonical scenario
constants — never a wall-clock reading, so two runs are byte-identical.

The published callables are declared separately, in the pure `gadgets.py`
catalogue: 11 entries (poker_equity_vs_range, poker_cfr_solve, icm_exact_equity, icm_bubble_factor, chip_flow_detect, network_laundering_risk, parkour_shortest_path, parkour_build_city_quarter, parkour_profile, poison_identify_sample, bayesian_opponent). Keeping the catalogue
out of the adapter means it can be counted and exercised without the protocol
dependency present, which is what lets this manuscript state its size as a
token rather than a hand-written number. `mission.register_gadgets` binds that
mapping to the protocol's `GadgetRegistry` under the film slug; the public
shape consumed by bond-cli, the coordinator, and the orchestrator is unchanged
by the split.

## Results — LE CHIFFRE: measured outcomes, headline numbers, and what they establish

All results are computed live from the engines on the canonical scenario in
`src/casino_royale_2006/scenarios.py` (fixed seed, deterministic RNG).
Every number below is a `TOKEN` placeholder, injected at manuscript time.

### The felt: equity, price, and decision

On the board `As 7h 2d`, the hero holds `KhKc` against
Le Chiffre's `loose` range — the range his observed
**loose-aggressive** tendencies select, not a hand-picked one. The
engine prices a Monte-Carlo equity of **45.62%** against a
pot-odds break-even of **16.67%** (pot 5,000,000, to
call 1,000,000). The resulting margin, **28.96%**,
clears the 10% raise threshold that same archetype
implies, so the model recommends **raise**: the probability of
winning exceeds the price the pot is laying, and by enough to raise for value
rather than merely call. The poker figure visualizes the equity-vs-price
comparison.

![Poker decision: hero equity vs. pot-odds break-even with the resulting
action.](output/figures/casino_royale_2006_poker_decision.png)

### The capital: chip-flow laundering

The scanner ingests **41** chip movements across
**8** players, including the one planted smurfer. It raises
**1** alert(s); the planted launderer is caught
(**yes**) with a composite score of **2**,
accumulated from structuring + velocity dimensions rather than any single
transfer — the structural, not transactional, signature of the laundered
stake.

### The terrain: parkour extraction route

On the `6×6` city quarter (**72** nodes,
**312** directed edges) the planner is run twice, under two
different objective functions. The *fastest* (speed-weighted) solve short-cuts
across the rooftops (uses rooftops: **yes**); the *safest*
(risk-weighted) solve stays on the ground.

Their headline costs — **36.53** and
**15.31** — are *not* comparable: each is measured under its
own weighting, so the smaller number does not mean the cheaper route. Priced
under one objective at a time, the ordering is unambiguous. Under the speed
weighting the rooftop route costs **36.53** against the ground
route's **103.39**; under the risk weighting the
ground route costs **15.31** against the rooftop route's
**17.95**. Each route is optimal only under its own
objective, which is the film's trade-off stated exactly: the roof is faster,
the street is safer, and no single number ranks them.

### The martini: digitalis triage

From a tray of **5** samples, the triage isolates the spiked
glass at **3**, reading **4.5** ng/mL
digoxin, heart rate 42.4 bpm, potassium
6.62 mmol/L — a **severe** toxicity with a Bayesian
posterior of **0.95**. The digitalis figure shows the
monogram-style toxicity curve used to place such a panel.

![Digitalis toxicity score vs. serum digoxin concentration with the severity
grade bands shaded.](output/figures/casino_royale_2006_digitalis_curve.png)

### The solve: CFR river-toy equilibrium

CFR on the toy game converges to an average regret of **0.001**
after **300** iterations, giving a game value of
**0.0974**. The equilibrium is *polar*, the classic shape behind
modern solver-based play: the out-of-position player bets the very top of
his range for value (**0.9983**) and bluffs near the very
bottom (**0.9831**), while the in-position caller calls the middle
of his range (**0.7805**). The cfr figure shows regret decaying
toward zero across the solve.

![CFR average counterfactual regret vs. iteration, decaying toward the Nash
equilibrium.](output/figures/casino_royale_2006_cfr_convergence.png)

### The freezeout: Independent Chip Model

On the 4-player, 3-paid bubble, exact ICM prices the short stack
at a tournament-equity bubble factor of **1.411** — risking his
stack is negative prize-equity — while the chip leader faces a squeeze of
**3.631**. The model's tournament call on the bubble is
**fold** (prize-equity EV **-0.829**), the correct
survival discipline when the first chips are worth more than the last. The icm figure shows the bubble factor rising with stack size.

![ICM bubble factor by start stack on the 4-player, 3-paid freezeout,
demonstrating the prize-equity squeeze.](output/figures/casino_royale_2006_icm_bubble.png)

### The capital again: network-level laundering

The structural detector needs no single suspicious transfer: across the
canonical flow it computes **1** trading community and
flags the launderer specifically (**yes**), giving him a
composite network risk of **0.98** at HHI concentration
**1** (everything moving through one counterparty), while
the collection account ranks highest on PageRank centrality
(P8). It agrees with — but is independent of — the
typology detector.

### The read: Bayesian opponent archetype

From Le Chiffre's observed action history, the model infers an archetype of
**loose-aggressive** with a **0.986** posterior
mass on aggressive archetypes, an expected aggression rate of
**0.753**, and a predictive raise probability of
**0.38** — a quantified read of the adversary rather
than a bare action count.

## Conclusion — LE CHIFFRE: findings, verdict, and what the mission establishes

**Casino Royale: LE CHIFFRE — Special-Agent Mission Software** demonstrates that the serious set pieces of *Casino
Royale* (2006) — the game-theory finale, the laundered stake, the parkour
pursuit, and the poisoned martini — reduce to a family of tractable,
fully-tested algorithms that a special-agent mission system can run
deterministically and audit later. The package now carries
8 domain modules (poker_engine, poker_cfr, icm, opponent_bayes, laundering_detect, laundering_network, urban_routes, poison_detect): a hold'em equity
engine, a counterfactual-regret solver, the tournament Independent Chip Model,
a Bayesian opponent model, a chip-flow typology detector, network-level
financial-crime analytics, a mobility-graph router, and a digitalis triage —
all bound by the frozen BOND-API `MissionProvider`.

Two of those modules matter beyond their own output because they *corroborate*
another. The typology detector flags the launderer from behaviour (structuring
bands, velocity) at a composite score of 2; the network
detector reaches the same account from structure alone — value-neutral churn
at HHI 1 — scoring 0.98. Two independent
methods converging on one account is a stronger claim than either alone, and
the package is arranged so that agreement is checkable rather than asserted.

Three design properties carry the whole package. First, **purity**: the domain
modules import no framework, no `infrastructure.*`, and no bond-api, so they
remain importable in any environment and on their own. Second,
**determinism**: every random draw flows through a seeded RNG, and the CFR,
ICM, and Bayesian engines are exactly enumerated with no RNG at all, so a
mission run twice yields byte-identical results. Third, **one scenario**: the
canonical scenario in `scenarios.py` feeds the mission, the manuscript tokens,
and the CLI, so the claim computed in one place is the claim shown in every
other.

The mission adapter still implements the frozen BOND-API `MissionProvider` and
registers this film's 11 gadgets with the protocol's
`GadgetRegistry` — the deepened state sits inside the package, behind an
unchanged public shape. Verified by ≥90% line-and-branch coverage, zero mocks,
a clean lineage check, and a clean working tree, the package is ready to bind
the moment any future suite dependency lands.

## Experimental Setup — LE CHIFFRE: canonical scenarios, parameters, and configuration

### Configuration

Mission identity and publication metadata live in `manuscript/config.yaml`
(title, subtitle, film slug, codename, version, keywords, authorship). The
engine scenario parameters live in `src/casino_royale_2006/scenarios.py` as
module constants (`POKER_SCENARIO`, `LAUNDERING_PLAYERS`, `ROUTE_GRID`,
`POISON_N_SAMPLES`, `CFR_STRENGTHS`, `ICM_STACKS`, `BAYES_HISTORY`, and the
shared `SEED`). Manuscript tokens are computed from these plus live engine
output by `src/casino_royale_2006/manuscript_variables.py` — prose never
hardcodes a number.

### Canonical scenario

| Concept | Fixed inputs (seed `SEED`) |
|---|---|
| Poker | hero KhKc on board As 7h 2d, a loose opponent range, pot 5,000,000 / to-call 1,000,000, every simulation seeded |
| CFR | river toy game, 16 discrete strengths, 300 regret-matching sweeps, fully enumerated |
| ICM | 4-player, 3-paid freezeout bubble (`ICM_STACKS`/`ICM_PRIZES`), short-stack player `ICM_PLAYER` |
| Bayesian opponent | `BAYES_HISTORY`, Le Chiffre's observed action sequence |
| Laundering | 8 players over a fixed tick horizon, one planted smurfer, 41 movements |
| Network crime | the same canonical chip flow, re-read structurally (HHI / PageRank / communities / conservation) |
| Routes | 6×6 city quarter (72 nodes, 312 directed edges), ground + rooftop layers, climbable profile |
| Poison | 5 tox panels, one spiked (`POISON_INDEX`) |

### Software environment

- Python 3.14 (requires-python `>=3.10`)
- Dependencies: `bond-api` (the frozen protocol, sibling path dependency),
 `matplotlib` (figures), `pyyaml` (config); dev: `pytest`, `pytest-cov`,
 `ruff`, `mypy`, `types-PyYAML`.
- Deterministic by design: fixed `SEED`, seeded `random.Random` instances,
 fully enumerated CFR, Agg matplotlib backend, no wall-clock in persisted
 artifacts.

### Runtime determinism

Each `*_snapshot` in `scenarios.py` constructs its own
`random.Random(seed)` and never touches the global RNG. The mission's
`Provenance` records `seed` and a deterministic `input_hash`; `wall_time_s` is
held at `0.0` so no two runs diverge on timing.

## Reproducibility — LE CHIFFRE: verification gates, deterministic regeneration, and artifacts

### Determinism & provenance

Every engine draw comes from a caller-supplied, seeded `random.Random`. The
mission outcome's `Provenance` carries `package_version`, `seed`, and a
deterministic `input_hash` derived from the canonical scenario (not wall
clock). Re-running `run_mission` twice yields identical results.

**Scope of the byte-identical claim.** Running
`scripts/z_generate_manuscript_variables.py` twice, any interval apart,
produces byte-identical `output/data/manuscript_variables.json` and
`output/manuscript/*.md`. Nothing in that path reads a clock: the manuscript's
publication stamp is the `MANUSCRIPT_DATE` token, read from the committed
`publication.date` field of `manuscript/config.yaml` (currently
2026-08-05), so it moves only when a human edits and commits it. The
claim covers the token mapping and the resolved prose; it does not extend to
the rendered `output/figures/*.png`, whose bytes depend on the installed
Matplotlib and freetype build.
`tests/test_scripts_smoke.py::test_regeneration_is_byte_identical_across_a_clock_tick`
pins exactly that scope by running the real generator twice across a
whole-second boundary and comparing artifact bytes.

### Artifact layout

| Path | Content | Regenerated by |
|---|---|---|
| `output/data/manuscript_variables.json` | the token mapping (key-sorted) | `scripts/z_generate_manuscript_variables.py` |
| `output/manuscript/*.md` | prose sections with `TOKEN` placeholders resolved | same script |
| `output/figures/poker_decision.png` | equity-vs-price figure | same script |
| `output/figures/digitalis_curve.png` | digitalis monogram | same script |
| `output/figures/cfr_convergence.png` | CFR average-regret decay | same script |
| `output/figures/icm_bubble.png` | ICM bubble factor by start stack | same script |

`output/` is git-ignored (regenerable artifacts); the working tree stays clean
after any run.

### Test & quality gates

- **Coverage**: `uv run pytest tests/ --cov=src --cov-fail-under=90`
 (line + branch ≥ 90% on `src/`; live count in `docs/_generated/COUNTS.md`).
- **Zero mocks**: no `unittest.mock` / `MagicMock` / `@patch` / `create_autospec`
 anywhere in `tests/`.
- **Token integrity**: two gates, both failing rather than warning. First,
 every double-brace placeholder in a numbered section must exist in the
 mapping — the resolver reports leftovers and
 `scripts/z_generate_manuscript_variables.py` exits 1. Second, no section may
 use the *single*-brace form: it is never substituted, so it would print its
 own braces into the published PDF while passing the first check, which looks
 only for the double-brace form. `manuscript_variables.find_malformed_tokens`
 is the detector; `tests/test_manuscript_variables.py` pins both. See
 `manuscript/SYNTAX.md` for the literal syntax.
- **Lineage**: `rg "template[_]code_project"` returns nothing outside any
 doc that explicitly describes the check.
- **Type & format**: `uv run ruff check && uv run ruff format` and
 `uv run mypy src/ scripts/` both clean.

### Verification (preflight)

`uv run python scripts/00_preflight.py` confirms the package imports, that the
`MissionProvider` satisfies the frozen BOND-API protocol, and that its declared
`film` equals the slug — the same checks the orchestrator performs during
discovery.

## Scope & Related Work 

### Scope

This package is a **deterministic engineering exemplar**, not a licensed
clinical or financial system. Its contributions are the algorithmic cores and
the reproducibility discipline around them; the specific numeric constants are
documented model choices, not regulatory thresholds. What each of the
8 modules does *not* claim:

- **Poker (`poker_engine.py`).** The engine prices hands and recommends
 actions; it is not a full solver (no perfect-information exploitation, no
 multi-street counterfactual regret minimization). Monte-Carlo equity is
 sampled, not solved exhaustively — except the exact turn/river enumerator,
 which is complete over all runouts.
- **CFR (`poker_cfr.py`).** The solve is exact for the *river toy game* only:
 one street, one bet size, discrete uniform strengths. It is not a hold'em
 solver, has no card abstraction or bucketing, and its game value is the toy
 game's value, not the film hand's.
- **ICM (`icm.py`).** The Independent Chip Model assumes finish probability is
 proportional to stack share. That is the standard simplification and it is
 known to be wrong in detail: it ignores position, blind level, and skill
 edge. Bubble factors here are model output, not tournament advice.
- **Bayesian opponent (`opponent_bayes.py`).** The archetype Dirichlet priors
 are declared model choices, not fitted to a hand-history corpus. The
 posterior is exact *given* those priors; it is not a claim about any real
 player, and it assumes actions are exchangeable (no street or board context).
- **Laundering typologies (`laundering_detect.py`).** The detector flags
 *structural* typologies (structuring, round-tripping, velocity, chip
 parking). It uses documented heuristics rather than a supervised classifier
 and is un-tuned to any regulated jurisdiction; its thresholds carry no
 false-positive rate measured against real casino data.
- **Laundering network (`laundering_network.py`).** HHI, PageRank, label
 propagation, and conservation imbalance are computed exactly, but the
 composite risk score is a declared product of value-neutrality and turnover
 share, not a calibrated probability. The module is deliberately
 film-agnostic: it names no suspect, and whether a *particular* account was
 caught is decided by the caller (`scenarios.network_snapshot`).
- **Routes (`urban_routes.py`).** Dijkstra over feasible parkour edges is
 optimal for the fixed cost model; it does not model moving pursuers,
 stochastic edge risk, or fatigue.
- **Poison (`poison_detect.py`).** Triage reproduces standard cardiac-glycoside
 reference ranges and Bayesian reasoning; the likelihood ratios are
 conservative declared constants, and the module is explicitly not medical
 advice.

### Related work

The cores sit in well-established literatures. Hand ranking and Monte-Carlo
equity follow the combinatorial and simulation methods surveyed in computer
poker research [@billings2002poker], with chip-to-prize conversion from the
Independent Chip Model as presented by @chen_ankenman_2006. Equilibrium
computation in imperfect-information games via counterfactual regret
minimization is due to @zinkevich2007cfr; Bayesian opponent modelling in that
setting follows @ganzfried2011opponent, with the Dirichlet-multinomial
machinery as in @minka2000dirichlet.

The financial-crime layer draws on graph-based anti-money-laundering analysis
[@weber2019aml] and on the casino-sector typologies documented by the
Financial Action Task Force [@fatf2009casinos]. Its structural measures are
PageRank [@page1999pagerank], label-propagation community detection
[@raghavan2007labelprop], Brandes' betweenness centrality [@brandes2001], and
the Herfindahl-Hirschman concentration index [@hirschman1964]. Route planning
is Dijkstra's algorithm [@dijkstra1959] over a feasibility-constrained
directed graph. The toxicology follows the cardiac-glycoside literature,
including digoxin-specific Fab antibody fragments as definitive therapy for
life-threatening intoxication [@antman1990fab]. Full entries live in
`references.bib`; the descriptive list is in `99_references.md`.

## Sources — LE CHIFFRE: bibliography

@bond_api_protocol; @casino_royale_2006; @zinkevich2007cfr; @billings2002poker; @chen_ankenman_2006; @ganzfried2011opponent; @minka2000dirichlet; @page1999pagerank; @raghavan2007labelprop; @brandes2001; @hirschman1964; @weber2019aml; @fatf2009casinos; @dijkstra1959; @antman1990fab


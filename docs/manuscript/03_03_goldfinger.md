# Goldfinger (1964) — GRAND SLAM

*film package · package codename GRAND SLAM*. Mission **GRAND SLAM**: corner the gold market via a controlled supply shock; weaponise the gold peg via a speculative reserve attack; assess Fort Knox-style layered and network vault defense; quantify the laser burn-through and thermal engagement threat.

## Concepts — GRAND SLAM: domain and operational focus

macroeconomic attack, vault defense, laser threat

## Abstract — GRAND SLAM: mission summary

Auric Goldfinger's *Operation Grand Slam* is modelled as a deliberate gold-market corner: a supply shock that removes 30% of the floatable supply and drives the clearing price from $1850.00/oz to a shocked equilibrium of $2460.90/oz — a 33.0% appreciation under constant-elasticity demand (elasticity 1.25). The GRAND SLAM mission software deepens this into a full attack surface. On the **macroeconomic front** the same accumulation is weaponised against the gold peg itself: a first-generation speculative attack exhausts reserves in 5.19 time units — well before the gradual 21.28-unit drain — and lands a 336% post-float depreciation. On the **vault front** a Fort Knox-style layered defence scores 0.780 (medium security, 0.009% penetration given the weakest layer is the fence); a network model finds a 15.20-effort minimum intrusion path through the secret tunnel and shows that a 10-unit hardening budget raises the intruder's required effort to 20.20. On the **laser front** a 5000 W continuous-wave beam burns a 50 mm steel plate in 0.72 s (serious) at range, and the Gaussian-beam thermal model sets its effective engagement range at 65.0 m. The cinema's fictional scheme is treated as a *quantitative modelling exercise*: 6 deterministic, infrastructure-free modules (`market_attack`, `reserve_attack`, `vault_security`, `vault_threat_network`, `laser_physics`, `laser_thermal`) formalize the economics of cornering and speculative attack, the reliability of layered and network defense, and the physics of laser penetration and heat conduction. Each is fully unit-tested on real computation with zero mocking, and every result is injected into this manuscript as one of 73 template variables so no metric — not even a count of modules or figures — is hand-authored. The package implements the frozen BOND-API mission protocol, exposing a `MissionProvider` (film `goldfinger`, codename `GRAND SLAM`) that a fleet orchestrator can discover and drive through the brief–recon–plan–execute–debrief lifecycle.

## Introduction — GRAND SLAM: mission framing, the operational problem, and how to read this chapter

The 1964 film *Goldfinger* dramatizes a plausibly dangerous scheme: corner the
gold market by destroying the floatable supply, strike a fortress vault, and
deploy an industrial laser as the coup de grâce. This report strips the drama
to its *quantitative skeleton* and builds the models a mission planner would
actually run — 6 small, deterministic, well-tested
modules organised along three attack surfaces. Each surface carries one
closed-form model and one structural model that the closed form cannot
express.

### Macroeconomic attack

1. **Market cornering** (`market_attack`) — the economics of a deliberate
 supply shock. Removing a fraction of the floatable supply shifts the
 market-clearing price along a constant-elasticity demand curve, and a
 tâtonnement process traces how price converges to the new equilibrium.
2. **Speculative reserve attack** (`reserve_attack`) — the monetary front. The
 same accumulation is turned against the gold peg itself: under the
 first-generation crisis model, exponential domestic-credit growth drains
 the central bank's reserves and speculators collapse the peg the instant
 the shadow floating rate reaches parity. The corner raises the price; the
 attack breaks the institution that fixes it.

### Vault defense

3. **Layered assessment** (`vault_security`) — a Fort Knox-style
 defense-in-depth score. Concentric defensive layers are rated and weighted
 into a composite, and the sequential-penetration probability of an intruder
 is computed by the product rule over the traversal order.
4. **Network penetration and hardening** (`vault_threat_network`) — the
 structural front. Ratings measure how strong each layer is, but not which
 *route* an intruder takes. Treating the vault as a weighted zone graph, a
 shortest-path search finds the minimum-effort intrusion route (the film's
 secret tunnel), edge criticality identifies which zone transitions actually
 matter, and a greedy budget allocation raises the effort the intruder must
 pay.

### Laser threat

5. **Burn-through physics** (`laser_physics`) — an energy-balance model
 determining how long a beam of a given power takes to burn through a plate
 of a given material, plus its inverses for required power and maximum
 burnable thickness.
6. **Thermal engagement** (`laser_thermal`) — the spatio-temporal front. A
 Gaussian beam defocuses with range, so absorbed intensity falls; the
 Carslaw–Jaeger constant-flux solution converts that intensity into a
 surface melt time, and the two together bound the beam's effective
 engagement range within a threat window.

These 6 modules are the *pure domain core*: they
depend only on the standard library and NumPy, contain no I/O, draw no random
numbers, and are trivially reproducible. Around them sits a thin mission
adapter that implements the frozen BOND-API protocol (the suite's canonical
`MissionProvider` contract), so the model set can be discovered, orchestrated,
and debriefed uniformly across the film fleet. (The fleet's size is a property
of the suite, not of this package; it is deliberately not stated here, because
this package can neither derive it nor gate it without reaching into sibling
packages. The suite roster is authoritative.) The adapter's public shape —
the film slug, the five lifecycle methods, and the module-level gadget
registry — is frozen across phases; only its internals deepen.

The design priorities are **determinism** (a declared seed of
2026, no random draws, no wall-clock dependence in persisted
results), **honesty** (real computation and real data throughout; no mocked
dependencies), and **measurability** (every headline number in this manuscript
is injected as one of 73 generated variables rather
than typed by hand — including the module count in this paragraph, which is
derived from the package directory rather than declared).

## Methodology — GRAND SLAM: the analytical models and algorithms that drive the mission

The GRAND SLAM models each reduce one operational concept to a closed-form
relation and a deterministic iterative update. All 6
are pure functions of their inputs — no I/O, no random draws, no wall-clock
dependence. The three attack surfaces are presented in pairs: the closed-form
model first, then the structural model that captures what the closed form
cannot.

### Market cornering: supply shock to price dynamics

Let $\mathcal{S}_0$ be the floatable supply clearing at a reference price
$P_0$. Cornering removes a fraction $f \in [0,1)$ of that supply, leaving the
effective supply

$$\mathcal{S}_\mathrm{eff} = \mathcal{S}_0 (1-f).$$

With constant-elasticity demand $Q_d(P) = k P^{-\eta}$ (elasticity
$\eta > 0$), market clearing pins the shocked equilibrium price to

$$P^* = P_0 \left(\frac{\mathcal{S}_0}{\mathcal{S}_\mathrm{eff}}\right)^{1/\eta}.$$

Price does not jump; it adjusts toward $P^*$ by a discrete tatonnement with
coefficient $\lambda \in (0,2)$,

$$P_{t+1} = P_t + \lambda\,(P^* - P_t),$$

which converges monotonically for $\lambda < 1$. The fractional corner gain is
$P^*/P_0 - 1$. Because the trajectory approaches $P^*$ geometrically and
attains it only in the limit, convergence is reported as the relative residual
$|P_n - P^*|/P^*$ tested against a tolerance
(1e-06), never by exact float equality. For the
reference intel ($f$ = 30%, $\eta$ =
1.25, $P_0$ = $1850.00$) the gain resolves
to the results in Section [Results].

### Vault defense: layered security scoring

A vault is defended by $\ell$ concentric layers ranked
$\mathcal{L}_1, \dots, \mathcal{L}_\ell$. Each layer $i$ receives a rating
$r_i \in [0,1]$ (assessed strength) and a weight $w_i \ge 0$. The composite
defense-in-depth score is the weighted average

$$S = \frac{\sum_i r_i w_i}{\sum_i w_i} \in [0,1].$$

Under a sequential-penetration model an intruder must defeat layers in order;
if each layer stops the intruder with probability equal to its rating, the
overall breach probability is the product of the pass-through rates,

$$P_\mathrm{breach} = \prod_i (1 - r_i).$$

The expected time to breach (or stall) telescopes as
$E[T] = t \sum_i \prod_{j<i}(1-r_j)$ over the rated layers. Fortification
priority is ranked by the marginal composite gain of raising each layer by a
fixed $\delta$.

### Laser threat: burn-through time vs material and power

A continuous-wave laser of power $P$ focuses onto a spot of area $A$; the
target absorbs a fraction $a \in (0,1]$ of the beam. The material column under
the spot has mass $m = \rho A d$ (density $\rho$, thickness $d$); raising it
by $\Delta T$ (specific heat $c$) requires

$$Q = \rho A d c \Delta T.$$

Equating this to the absorbed power $P_\mathrm{abs} = a P$ gives the
burn-through time

$$t_\mathrm{burn} = \frac{\rho A d c \Delta T}{a P}.$$

The same relation inverts for required power and for maximum burnable
thickness, so any pair of (power, time, thickness) determines the third.

### Macroeconomic attack: speculative attack on the gold peg

The phase-4 deepening adds the monetary-system front. Money demand is linear
in the interest rate, $m_t - p_t = -\alpha i_t$; purchasing-power parity and
uncovered interest parity link the price level and interest rate to the
exchange rate. With domestic credit growing exponentially,
$D_t = D_0 e^{\mu t}$, the fixed peg forces reserves to drain,

$$R_t = (\bar{S} - \alpha i^\ast) - D_0 e^{\mu t},$$

while the rational-expectations **shadow floating rate** (the rate that would
prevail once reserves are gone) is

$$\tilde{s}_t = \frac{D_0 e^{\mu t}}{1 - \alpha\mu} + \alpha i^\ast.$$

Under perfect foresight speculators attack exactly when the shadow rate
crosses the fixed parity, at

$$t^\ast = \frac{1}{\mu}\ln\frac{(1-\alpha\mu)(\bar{S} - \alpha i^\ast)}{D_0},$$

which precedes the gradual reserve-exhaustion time
$t_B = (1/\mu)\ln((\bar{S}-\alpha i^\ast)/D_0)$ — the attack is sudden. The
post-float depreciation is the shadow rate at $t_B$ relative to parity.

### Network vault defense: penetration and hardening

The layered ratings in the previous section measure *strength*; the network
model treats the vault as an undirected weighted graph of zones with
intrusion-effort edges. The intruder's **minimum-effort path** (Dijkstra) from
the perimeter to the gold chamber, and the **edge criticality** (how much
removing each edge raises that minimum), capture where the vault is truly weak
— here the secret tunnel. Given a hardening budget, a greedy marginal-gain
allocation raises the edge whose lift most increases the minimum path,
``gain_per_unit`` per unit, until the budget is spent, maximising the effort
an intruder must pay.

### Laser thermal engagement: beam focus and heat conduction

The scalar burn-through model ignores beam divergence and conduction. A
Gaussian beam of waist $w_0$ and wavelength $\lambda$ has Rayleigh range
$z_R = \pi w_0^2/\lambda$ and spot radius
$w(z) = w_0\sqrt{1+(z/z_R)^2}$, so absorbed intensity
$I_a = a P/(\pi w^2)$ falls with range. Under constant flux the surface heats
by the Carslaw–Jaeger law,

$$T(0,t) = T_\mathrm{amb} + \frac{2 I_a}{\sqrt{\pi k\rho c}}\sqrt{t},$$

giving the melt time $t_\mathrm{melt} = \frac{\pi}{4}\frac{k\rho c
\,(T_\mathrm{melt}-T_\mathrm{amb})^2}{I_a^2}$. The **effective burn range** is
the greatest distance at which the defocused beam still melts the target
within a threat window.

## Results — GRAND SLAM: measured outcomes, headline numbers, and what they establish

### Market corner: price shock and convergence

Under the reference intel, removing 30% of the
floatable supply moves the equilibrium price from
$1850.00$/oz to **$2460.90$/oz**, a
**33.0%** appreciation at elasticity
1.25. Price approaches the shocked equilibrium geometrically
over the 40-step tâtonnement window, ending at a relative
residual of 3.32e-10 against a convergence tolerance of
1e-06 (converged: true). Tâtonnement
reaches $P^*$ only in the limit, so convergence is asserted against that
tolerance rather than by exact equality.

![Operation Grand Slam: tatonnement price trajectory toward the shocked equilibrium.](output/figures/goldfinger_market_corner_trajectory.png)

The figure shows the reference price, the shocked equilibrium price, and the
deterministic adjustment path. The corner is economically self-reinforcing:
a larger sterilized fraction yields a higher equilibrium, which in turn
raises the value of the seized stockpile.

### Vault defense: layered score and penetration

The 6 concentric layers of the reference vault score
**0.780** — classified **medium** security — with an
overall sequential-penetration probability of
**0.009%**. The weakest layer is the
**fence**, which is where fortification yields the greatest
marginal composite gain.

![Fort Knox-style layered defense: per-layer ratings and composite defense-in-depth score.](output/figures/goldfinger_vault_layered_score.png)

### Vault network: penetration and hardening

The network model locates the vault's true weak point. Across the
10-zone graph, the minimum-effort intrusion path from the
perimeter to the gold chamber is **15.20** effort and runs
through the **secret tunnel** (6 zone transitions),
bypassing the costly guarded spine. 6 edges are
critical — removing each one forces a strictly costlier route. Spending the
10-unit hardening budget at 0.50
effort per unit raises the minimum required intrusion effort from
15.20 to **20.20** (a lift of
5.00), closing off the tunnel as the free ride. The
allocation is greedy rather than exactly optimal, so its lift is normally a
lower bound on what the same budget could buy; here the bound is *measured*,
not just disclaimed. At a small verification budget of
3 units we enumerate every allocation of that budget
across the graph's edges and confirm the greedy result achieves the maximum
achievable lift (1.50, greedy matches optimal:
true), so on this graph the greedy allocation is
exactly optimal at small budgets.

![Vault network: minimum-effort intrusion path through the secret tunnel, before and after hardening.](output/figures/goldfinger_vault_network.png)

### Macroeconomic attack: speculative reserve drain

The speculative-attack model turns gold accumulation into a monetary weapon.
With the reference intel the shadow floating rate crosses parity at
5.19 time units, forcing the peg's collapse **before** the
gradual reserve floor at 21.28 (suddenness
16.09), and the subsequent float depreciates the
currency by **336%**.

![Speculative attack on the gold peg: reserve drain and attack time.](output/figures/goldfinger_reserve_crisis.png)

### Laser threat: burn-through time

At 5000 W the reference steel plate
(50 mm) is breached in **0.72 s**,
denoted a **serious** threat against the
1000 W mission threshold. Doubling
power halves burn-through time; doubling thickness doubles it, so the
defensive levers on the laser side are plate thickness and material (higher
$\rho c \Delta T$).

![Laser threat physics: burn-through time vs beam power for the reference vault plate.](output/figures/goldfinger_laser_burn_through.png)

### Laser thermal engagement: beam focus and heat conduction

Accounting for Gaussian divergence and heat conduction, the reference beam
melts the plate surface at focus in 0.0020 s and retains an
effective engagement range of **65.0 m** within the
5.0 s threat window (Rayleigh range
9.36 m, focus waist 1.78 mm). Defocusing
with range lengthens melt time, so a defender pushing the engagement beyond the
Rayleigh range materially degrades the threat.

![Laser engagement: surface melt time grows as the Gaussian beam defocuses with distance.](output/figures/goldfinger_laser_engagement.png)

All 6 model results above are computed by the pure
domain core and injected here as generated variables — none is typed by hand,
including the counts in this sentence. Re-running the pipeline reproduces
identical numbers from the module `REFERENCE_*` constants.

The no-hardcoding claim is gated, with a stated limit. Every computed result
token is classified, and each one whose value is a numeric literal of at least
three characters is searched for in the rendered prose (the numbered sections
and `preamble.md`), with a positive control that pastes each value in turn and
confirms the scan flags it. The remaining computed tokens — bare small integers
such as the module and layer counts, and categorical words such as the vault
verdict and the laser severity — **are not scanned**, because searching prose
for `6` or `medium` finds ordinary English rather than a pasted result. Those
tokens are listed explicitly in the test with the reason, and a further test
asserts the list is exactly what the rule rejects, so the hole cannot widen
silently. It is a real hole nonetheless: a hand-typed module count in this
prose would not be caught by the scan.

## Conclusion — GRAND SLAM: findings, verdict, and what the mission establishes

The GRAND SLAM mission software demonstrates that the operational concepts of
*Goldfinger* — cornering the gold market, weaponising the monetary system,
breaching a layered vault, and wielding a laser — are each reducible to small,
deterministic, closed-form or graph models that a planning agent can actually
run and audit.

- The **market-cornering model** quantifies how a supply shock propagates into
 price along a constant-elasticity demand curve, with a tatonnement path to
 the new equilibrium.
- The **speculative-attack model** (phase 4) turns accumulation into a
 monetary-system weapon: credit growth drains reserves, and the peg collapses
 the moment the shadow floating rate crosses parity — an attack that is
 strictly *sudden* relative to gradual exhaustion.
- The **vault-defense assessment** combines layered rating scoring with a
 network model that finds the minimum-effort intrusion path (the secret
 tunnel) and shows hardening raises the intruder's required effort
 unit-for-unit on the weak path.
- The **laser-threat physics** spans a scalar burn-through time and a
 spatio-temporal Gaussian/Carslaw–Jaeger model whose effective burn range falls
 as the beam defocuses with distance.

Every headline number in this report is a generated variable computed from the
module `REFERENCE_*` constants — real computation only, no mocked dependencies.
The scanned subset of those values is gated against being retyped as a prose
literal; the count and category tokens are not scannable and rest on review
instead (see Results). The package ships as a
BOND-API `MissionProvider` (film `goldfinger`, codename `GRAND SLAM`), so all
6 models are discoverable and drivable by the suite's
orchestrator through the full mission lifecycle — the adapter's public shape is
stable across phases; only its internals deepen.

## Experimental Setup — GRAND SLAM: canonical scenarios, parameters, and configuration

### Reference intel

The deterministic reference parameters are **declared in the module
`REFERENCE_*` constants** in `src/goldfinger/`. Those constants are what the
domain core, the mission adapter, the figures, and the token map all read, and
every value below is injected from them as a generated variable, so a change to
the intel changes this section automatically.

`docs/manuscript/config.yaml` carries a human-readable `grand_slam:` mirror of the
same numbers. Nothing loads that block at runtime — it is documentation, not
input — so its only guarantee is that
`tests/test_reference_intel.py` compares it key-for-key and value-for-value
against the module constants and fails if either side is edited alone.

**Market corner** (`market_attack.REFERENCE_MODEL`) — reference price
`$1850.00`/oz clearing a normalized floatable-supply index
of `100.0`; the corner sterilizes
`30%` of that float against a constant demand
elasticity of `1.25`. The tâtonnement runs `40`
steps at adjustment coefficient `0.40`.

**Speculative reserve attack** (`reserve_attack.REFERENCE_ATTACK`) — a
normalised peg at parity `1.00`, foreign interest rate
`0.02`, money-demand semi-elasticity $\alpha$ =
`8.0`, initial domestic credit `0.10`, and
credit growth $\mu$ = `0.10`. The model validates its own
feasibility conditions ($0 < \alpha\mu < 1$, and initial credit small enough
that the peg has not already fallen) before computing an attack time.

**Vault — layered** (`vault_security.REFERENCE_RATINGS`) —
`6` layers (perimeter, fence, guard response, vault door,
combination lock, gold storage), each rated in `[0,1]`, weighted by
`DEFAULT_WEIGHTS` and traversed in `LAYER_ORDER`.

**Vault — network** (`vault_threat_network.REFERENCE_GRAPH`) — an undirected
graph of `10` defensive zones with intrusion-effort edge
costs. The reference intrusion problem is perimeter → gold chamber
(`REFERENCE_TARGET`); the reference defensive posture (`REFERENCE_HARDENING`)
is a budget of `10` units buying
`0.50` effort each.

**Laser — scalar** (`laser_physics.REFERENCE_PHYSICS`) — power
`5000` W onto a focused spot of `1.0e-05` m²
against a steel plate of density `7800` kg/m³ and thickness
`50` mm, specific heat `460` J/(kg·K),
$\Delta T$ = `1200` K, absorptivity `0.60`.
A beam is classified *serious* at or above `1000` W.
This is the *same* plate as the thermal model below: the two modules shipped
different steel (specific heat 500 vs 460 J/(kg·K), and a $\Delta T$ that did
not equal that model's melt-minus-ambient span) until the constants were
reconciled, so $\Delta T$ is now exactly
`1500` K − `300` K and
`tests/test_reference_intel.py` asserts the agreement.

**Laser — thermal** (`laser_thermal.REFERENCE_BEAM`) — an Nd:YAG-class
continuous-wave beam of wavelength `1064` nm focused to a
waist of `1.78` mm, against steel of thermal conductivity
`45` W/(m·K) melting at `1500` K from an
ambient of `300` K, engaged within a
`5.0` s threat window.

### Determinism policy

The mission declares a fixed seed of `2026` and performs **no**
random draws — the seed is recorded in provenance so a replay is auditable,
not because any sampling occurs. Persisted artifacts carry no wall-clock
dependence at all (`wall_time_s = 0.0` in provenance; no clock in the token
map). The manuscript's date is the committed `paper.date` from
`docs/manuscript/config.yaml` — `MANUSCRIPT_DATE` = 2026-08-04 — so
`GOLDFINGER_VERSION_HASH`, which hashes the full token map, identifies the
content rather than the run and is stable across regenerations. Figure output
is byte-deterministic for fixed inputs:
`tests/test_figures.py` renders **every** exported renderer twice — into two
separate directories and again over the same path — and compares the bytes,
parametrised over `figures.FIGURE_RENDERERS` so a renderer added later is
covered without anyone remembering to add it.

### Software environment

- Python: as resolved by `uv` (the package requires `>=3.10`)
- Dependencies: NumPy, Matplotlib, PyYAML, and the frozen `bond-api` protocol
 (a local path dependency declared in `pyproject.toml` under
 `[tool.uv.sources]`; the sibling `bond-api` package in this working tree)
- Dev: pytest, pytest-cov, mypy, ruff, types-PyYAML

### Mission adapter

The BOND-API `MissionProvider` (`src/goldfinger/mission.py`) wraps all
6 models and registers six gadgets
(`market_corner`, `reserve_attack`, `vault_defense`, `vault_hardening`,
`laser_threat`, `laser_thermal`) with a module-level `GadgetRegistry`. It is
discoverable by slug `goldfinger` on `sys.path` and drives the full
brief–recon–plan–execute–debrief lifecycle with deterministic provenance,
and persists the outcome as a schema-validated mission record (via
`bond-utilities`'s `record_provenance_outcome`) whose `input_hash` is a real
fingerprint of the reference intel, not a hand-typed literal — so two outcomes
from unchanged constants carry identical provenance and a one-value edit to
any constant is visible in the hash. The record writes no wall clock (its
`started_at` is a committed sentinel), so it is byte-identical on every run.
The adapter's public shape is frozen across phases; the mission internals
(assets, plan steps, outcome results, lessons) are what deepen.

## Reproducibility — GRAND SLAM: verification gates, deterministic regeneration, and artifacts

### Deterministic regeneration

The package is fully deterministic. Re-running the mission or regenerating the
manuscript variables reproduces identical results:

```bash
uv run python scripts/z_generate_manuscript_variables.py
```

which rewrites `output/data/manuscript_variables.json`
(73 tokens) and the 6
concept figures under `output/figures/`. Every persisted byte is a function of
the committed tree alone, so running that command twice — on different days,
on different machines — produces byte-identical files. Nothing in the token
map reads a clock: the manuscript's date is the committed `paper.date` in
`docs/manuscript/config.yaml` (`MANUSCRIPT_DATE` = 2026-08-04), and
`GOLDFINGER_VERSION_HASH` hashes the whole map, which makes it a content
identifier rather than a run identifier.

That property is enforced, not asserted:
`tests/test_regeneration_determinism.py` copies the tree to a scratch
directory, runs the real generator twice with a wall-clock gap between the
runs, and compares every emitted byte — the JSON, all
6 figures, and the generated counts file. The same
file carries a positive control that reintroduces a clock-derived value into
the map and shows the comparison goes red, so the gate is known to be able to
fail.

The token count and figure count above are themselves generated, not typed:
`GOLDFINGER_TOKEN_COUNT` is the length of the declared `GOLDFINGER_TOKENS`
tuple, `GOLDFINGER_FIGURE_COUNT` is the length of
`goldfinger.figures.FIGURE_RENDERERS`, and `GOLDFINGER_MODULE_COUNT`
(= 6) is computed by scanning the package directory
for concept modules. A test asserts the declared token tuple is exactly the key
set `generate_variables` produces, so a token added to one and not the other
fails the suite rather than silently drifting into the prose.

### Verification gate

The enforced quality gate, run from the package root:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/ tests/ && uv run ruff format --check src/ scripts/ tests/
uv run mypy src/goldfinger scripts
```

Coverage is measured on `src/goldfinger/` only (tests are excluded) and the
floor is 90% line **and** branch. The suite exercises every model error branch
through a real call with a real bad argument, every mission stage, protocol
discovery and serialization, the token cross-reference gate, figure rendering
determinism, and the thin CLI smoke paths — all with real computation, no
mocking framework anywhere.

### Change policy

- Result metrics in the prose are injected by
 `src/goldfinger/manuscript_variables.py` from the module `REFERENCE_*`
 constants; do not hardcode numbers in prose, including counts of modules,
 figures, tokens, or tests. The hardcode scan cannot police the exact-value
 count and category tokens (their values are too short or too word-like to
 search for), so exact-value enforcement of those rests on review. But a
 **fleet or sibling-package count** — a number this package can neither derive
 nor gate — is caught by a lexical gate that rejects digit-plus-noun
 constructions such as a digit bound to a fleet/suite noun (see
 `tests/test_guards_and_contracts.py`), with a positive control proving the
 gate can fail.
- The pure domain modules must remain infrastructure-free and importable
 without `bond-api` (`mission.py` is the only module that imports it).
- Reference parameters live in exactly one place — the module `REFERENCE_*`
 constants. The mission adapter, the token map, and the figures all read those
 constants rather than repeating a literal, so the three cannot report
 different postures. `docs/manuscript/config.yaml`'s `grand_slam:` block is a
 read-only mirror that no code loads; `tests/test_reference_intel.py` pins it
 to the constants value-for-value and also pins the two laser models to one
 physical steel plate.

## Scope and Related Work — GRAND SLAM: boundaries, positioning, and relationship to the literature

### Scope

This work is a **quantitative modelling exercise** inspired by the *Goldfinger*
(1964) plot; it is not a physical market, monetary, or security assessment.
The scope boundary of each of the 6 models is stated
below, because a model whose limits are unstated is a model whose numbers
cannot be trusted.

- **Market corner** (`market_attack`) assumes constant-elasticity demand and a
 single sterile supply shock. It abstracts away bid–ask microstructure,
 storage and carry costs, competing arbitrageurs, and policy responses; the
 closed-form jump is therefore an upper bound on what a real corner achieves
 against a market that observes the trader's own order flow [3]. It is
 deliberately closed-form and deterministic.
- **Speculative reserve attack** (`reserve_attack`) is the *linear*
 first-generation crisis model: perfect foresight, purchasing-power parity,
 uncovered interest parity, and exogenous exponential credit growth. It has no
 second-generation self-fulfilling multiple equilibria, no sterilisation
 policy, no risk premium, and no stochastic credit process. The attack time it
 reports is the deterministic one implied by those assumptions, not a
 forecast.
- **Vault — layered** (`vault_security`) treats layers as *independent* stops
 whose stopping probability equals their rating. Real security is correlated
 (one insider defeats several layers at once), adaptive, and human, and the
 ratings themselves are analyst inputs, so the composite score is an
 assessment aid rather than a measurement.
- **Vault — network** (`vault_threat_network`) models intrusion as a
 static shortest-path problem with additive, known, symmetric edge efforts.
 It has no detection/response dynamics, no intruder uncertainty about the
 graph, and no defender response during the intrusion. The hardening
 allocation is a *greedy* approximation to shortest-path improvement, which
 is not guaranteed optimal in general. On the reference graph the gap is
 measured, not only disclaimed: an exhaustive enumeration at a small
 verification budget (3 units) shows the greedy
 allocation achieves the optimal lift (1.50, greedy
 matches optimal: true) — see Results.
- **Laser — scalar** (`laser_physics`) is a thermal energy-balance
 approximation. It neglects plasma shielding, radiative and convective
 losses, and latent heat of fusion, so burn-through times are
 order-of-magnitude threat estimates, not certified engineering values.
- **Laser — thermal** (`laser_thermal`) adds the beam optics and conduction
 the scalar model omits — Gaussian defocusing with range, and the
 semi-infinite-solid surface temperature under constant flux. It still
 assumes a semi-infinite solid (no back-face effects on a finite plate),
 temperature-independent material properties, constant absorptivity, and no
 atmospheric attenuation or thermal blooming along the path. Its effective
 burn range is scanned on a fixed grid, so it is quantised to the scan step.

These limitations are features for a mission-planning sandbox: they keep the
models auditable and replayable, and they make the numbers honest — each is a
clearly-stated approximation, not a fabricated precision.

### Related work

The models implement standard, well-understood literatures rather than novel
theory. Full citations are in `99_references.md`.

- **Market cornering and supply shocks.** The constant-elasticity
 inverse-demand and tâtonnement price-adjustment framework goes back to
 Walras [1] and Hicks [2]; Kyle [3] supplies the strategic-trader price-impact
 view that a closed-form corner deliberately abstracts away.
- **Currency crises and speculative attacks.** Krugman [4] introduced the
 first-generation balance-of-payments crisis; Flood and Garber [5] give the
 linear closed forms — shadow floating rate, attack time, and the gap to
 gradual reserve exhaustion — that `reserve_attack` implements directly.
- **Physical protection systems.** Garcia [6] is the standard treatment of
 layered physical protection, adversary sequence diagrams, and detection/delay
 path analysis; it underwrites both the weighted layer score and the decision
 to model the adversary's route as a weighted graph.
- **Network penetration and hardening.** Dijkstra [7] provides the
 shortest-path search; Israeli and Wood [8] formalise shortest-path
 interdiction and improvement, the problem the greedy budget allocation
 approximates.
- **Laser–material interaction.** Steen and Mazumder [9] give the
 continuous-wave energy-balance model; Carslaw and Jaeger [10] the
 constant-surface-flux conduction solution; Siegman [11] the Gaussian-beam
 propagation that sets the spot radius with range.

The contribution of this package is not new theory but a *disciplined,
testable, deterministic implementation* of these concepts as pure modules plus
a protocol-compliant mission adapter [12], reproducible end to end.

## Uncertainty and Sensitivity

The models return point estimates from a single reference intel vector. This
section quantifies how those headline numbers move when the unobservable
inputs shift, because a number without a sensitivity context reads as more
certain than it is.

### Market corner: elasticity sensitivity

The corner's price gain is the quantity most exposed to the (unobservable)
demand elasticity: the shocked price is
$P^* = P_0\,(S_0/S_{\text{eff}})^{1/\eta}$, so the *exponent* is $1/\eta$ and
the gain is exponentially sensitive to $\eta$. At the reference elasticity
the gain is **33.0%**. Because $\eta$ is an analyst
input, we evaluate the model at $\pm 10\%$ around it:

- $\eta$ reduced 10% (more elastic demand reacting less to the shock): gain
 **37.3%**
- $\eta$ raised 10% (steeper demand reacting more): gain
 **29.6%**

The swing is asymmetric in the *direction that hurts the corner*: a 10% error
in the elasticity assumption moves the headline by more than a third of its
own value. Any decision that leans on the absolute gain figure — rather than
on the direction and the shock itself — should carry this band.

### Laser burn-through: the $1/P$ lever

The energy-balance burn-through time is exactly proportional to
$1/P_\text{abs} = 1/(aP)$, so any power-assumption error maps directly:
doubling power halves the time (from **0.72 s** to
**0.359 s**), and halving the (unobservable)
absorptivity doubles it. The time carries the *inverse* of the power error,
so it is not robust to absorptivity misspecification. This is a structural,
parameter-free statement — it holds for any positive power and absorptivity
in this model — so it is a property of the physics, not of the reference
intel.

### Vault hardening: the greedy gap is measured

The one place an approximation matters is the hardening allocation. Rather
than disclaim an unmeasured lower bound, the package enumerates every
allocation of a small verification budget (3 units)
across the graph and reports the exhaustive optimum
(1.50 lift; greedy matches optimal:
true). On the reference graph the greedy
allocation is exactly optimal at that budget; this is a measured fact here,
not a general theorem, which is precisely why the enumeration exists.

### What the numbers are not

These are single-point, single-intel outputs of deliberately stylized models
(full scope in scope and related work (target section `07_scope_and_related_work.md` not present in this manuscript — needs owner input)). The
uncertainty quantified above is *within*-model sensitivity to declared inputs;
it does not capture the (larger, unquantifiable) model-form uncertainty — the
gap between these laws and the real market, vault, or laser. Presenting both
— a headline and its within-model band, side by side with the scope boundary
— is the honest shape of the result.

## Sources — GRAND SLAM: bibliography

@walras1874elements; @hicks1946value; @kyle1985continuous; @krugman1979model; @flood1984collapsing; @garcia2007design; @dijkstra1959note; @israeli2002shortest; @steen2010laser; @carslaw1959conduction; @siegman1986lasers; @bondapi2026protocol


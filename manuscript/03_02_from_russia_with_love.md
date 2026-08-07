# From Russia with Love (1963) — LEKTOR

*film package · package codename LEKTOR*. Mission **LURES**: evaluate a deception lure campaign via the entrapment engine; allocate the lure budget across the analytical target pool; intercept and decipher an encoded SIGINT channel; geolocate the transmitter by TDOA direction finding; schedule defector-handoff rendezvous within time windows; execute the green-pathed defector handoff protocol.

## Concepts — LEKTOR: domain and operational focus

entrapment ops, SIGINT interception, defector handoff

## Abstract — LEKTOR: mission summary

From Russia with Love: LURES — Special-Agent Mission Software — mission codename LURES — is a deterministic mission-software package in the PROJECT BOND suite. Its analytical core implements 6 interlocking engines drawn from the film *From Russia with Love* (1963): an entrapment/deception playbook engine that evaluates bait profiles and drives trap state machines; a lure-budget allocation engine that solves the exact 0/1 knapsack over an analytical target pool; a SIGINT channel interception simulation that captures, deciphers, and traffic-segments an encoded radio channel; a TDOA direction-finding engine that geolocates the transmitter by Gauss–Newton hyperbolic localisation; a courier scheduler that fits handoff rendezvous into time windows; and a defector handoff protocol whose meet / challenge / confirm / abort state machine gates a source transfer on a pre-arranged confirm code. Where a problem admits both a cheap heuristic and an expensive exact solver, the package runs both and reports the gap rather than assuming it away: the knapsack allocator is scored against a profit-density greedy baseline, and the courier scheduler — whose underlying problem is NP-hard once meets carry release times and deadlines — against an exact subset dynamic program. On the canonical scenario the heuristic schedule completes 4 of 5 rendezvous against a true optimum of 4. All outputs are reproducible: every stage is driven by fixed seeds and exact mathematical models, so the same inputs always yield the same lure allocation, recovered plaintext, localisation, schedule, and handoff path. Keywords: entrapment playbook, 0/1 knapsack allocation, SIGINT interception, cipher deciphering, TDOA direction finding, interval scheduling, defector handoff protocol, state machine, deterministic simulation, mission software.

## Introduction — LEKTOR: mission framing, the operational problem, and how to read this chapter

Mission codename **LURES** implements the operational concepts behind *From
Russia with Love* (1963) as a small, testable mission-software package. The
film's plot is a deception operation: a fabricated defector and a stolen
cipher machine are used as bait, a radio channel carries the traffic that
gives the operation away, and the whole thing turns on a handoff that only
completes when both sides produce the right recognition signal. Those are the
three things this package computes — luring, listening, and handing over — and
each is expressed as an algorithm rather than as narrative.

The analytical core is 6 deterministic engines, one per
module named in `scenario.ENGINES`:

1. an **entrapment playbook** that scores lure effectiveness on a logistic
 decision surface and drives a validated trap state machine over
 3 bait profiles;
2. a **lure-budget allocator** that solves the exact 0/1 knapsack over an
 analytical target pool of 6 targets;
3. a **SIGINT interception** simulation that enciphers, transmits through a
 noisy channel, deciphers, and segments 47 bytes of
 traffic under 2 cipher layers;
4. a **TDOA direction finder** that geolocates the transmitter from
 4 intercept sites by Gauss–Newton least squares;
5. a **courier scheduler** that fits defector-handoff rendezvous into their
 time windows and is scored against the exact optimum;
6. a **defector handoff protocol** whose confirm code gates the transfer.

The package is built to the shared guardrails of the PROJECT BOND suite: a
pure domain core with no infrastructure imports, a thin adapter to the frozen
BOND-API `MissionProvider` protocol, deterministic computation with no mock
framework, and a coverage floor of 90% line-and-branch on `src/`. Every
scenario constant lives in one module (`scenario.py`), so a number reported
here cannot disagree with the code that produced it.

Two of these engines pair an exact solver with a cheap heuristic and report
the difference rather than assuming it away: the knapsack allocator against a
profit-density greedy baseline, and the courier scheduler against an exact
subset dynamic program. Section 03 reports both gaps as measured quantities —
including the case where the measured gap is zero and the cheap heuristic
turns out to be optimal on that instance.

### Reader's guide

- Section 02 — the six analytical models and their mathematics.
- Section 03 — live measured results and the two figures.
- Section 04 — what the package demonstrates.
- Section 05 — the experimental setup (parameters + software environment).
- Section 06 — reproducibility, determinism, and the artifact inventory.
- Section 07 — scope boundaries and related work.

## Methodology — LEKTOR: the analytical models and algorithms that drive the mission

### 2.1 Entrapment / deception playbook engine

The engine models lure effectiveness analytically (a defensive
countermeasure; it does not target any person). A **bait profile**
describes a lure's cover role, intended target susceptibility $s \in [0,1]$,
payload message, and lure strength $q \in [0,1]$. The probability that a
target "bites" the lure is a bounded logistic decision surface:

$$
p(q, s) = \frac{1}{1 + e^{-4(q + s - 1)}}.
$$

$p$ is strictly increasing in both arguments, so stronger lures and more
susceptible targets both raise effectiveness. A **trap state machine** drives
the life-cycle of one lure campaign through the validated transitions

$$
\text{DISARMED} \to \text{ARMED} \to \text{BAITED} \to \text{ENGAGED} \to \text{SPRUNG}
$$

with a single terminal $\text{ABORTED}$ reachable from several stages; any
event not in the transition table raises an error and leaves state unchanged.

### 2.2 Lure-budget allocation

Given a pool of analytical targets each carrying an operational value $v_i$,
a susceptibility $s_i$, and a lure cost $c_i$, the mission decides which
targets to lure under a fixed budget $B$. The profit of luring target $i$
with a campaign of strength $q$ is its *expected engagement value*

$$
\text{profit}_i = v_i \cdot p(q, s_i),
$$

and the allocation is the exact **0/1 knapsack**

$$
\max \sum_i \text{profit}_i \cdot x_i \quad \text{s.t.} \quad
\sum_i c_i x_i \le B,\; x_i \in \{0,1\},
$$

solved by dynamic programming (@martello1990knapsack). A
profit-per-unit greedy heuristic is computed as the baseline.

That the exact solution is never worse than the greedy one is a property of
the exact solver, not of any particular target pool: it holds by construction
and carries no information about a scenario. The reportable quantity is
therefore the *size* of the gap on a given instance, which is not fixed in
advance. Section 3.1 reports it on two instances: the canonical target pool,
where it is zero, and a **witness pool** (`scenario.GREEDY_WITNESS_TARGETS`)
constructed so that the highest profit-density target consumes budget the
optimum needs elsewhere, where it is strictly positive. Only the second
instance distinguishes the two solvers, and the test suite pins the strict
inequality on it.

### 2.3 SIGINT channel interception simulation

Transmitted symbols are the byte magnitudes of the message, optionally
enciphered by **layered XOR keystream ciphers**. Each layer derives a
deterministic keystream from its key and a seed. The transmitted symbol
vector $x$ is observed through additive Gaussian noise whose variance
follows a requested signal-to-noise ratio:

$$
\text{SNR}_{\text{dB}} = 10 \log_{10} \frac{\mathbb{E}[x^2]}{\sigma^2}.
$$

The interceptor rounds each noisy sample to the nearest symbol, deciphers in
reverse cipher order, and measures the **empirical SNR** of the capture
against ground truth. An energy-threshold **burst segmentation** splits the
captured envelope into transmission bursts so the interceptor knows when, and
for how long, the channel was active.

### 2.4 TDOA direction finding

Four fixed intercept sites record the arrival of a single interception burst,
and the mission geolocates the transmitter by **time-difference-of-arrival**
hyperbolation. For receiver pairs $(i,j)$ with measured
TDOAs $\tau_{ij}$,

$$
h_{ij}(x) = \frac{\|x - r_i\| - \|x - r_j\|}{c},
$$

and the transmitter position is the non-linear least-squares minimiser of
$\sum_{ij} (h_{ij}(x) - \tau_{ij})^2$, solved by a deterministic
Gauss–Newton iteration from the receiver centroid — the iterative
Taylor-series estimator for hyperbolic location [@foy1976position;
@torrieri1984statistical]. Timing noise is seeded, so the same scenario always
yields the same estimate.

Receiver positions, and hence the estimate and its error, are plain
coordinates in an abstract scenario frame; the error reported in §3.3 is a
Euclidean distance in those coordinate units, not a multiple of the receiver
spacing. §3.3 gives both the raw error and its ratio to the site spacing.

### 2.5 Courier handoff scheduling

A courier must visit defector-handoff rendezvous, each occupying a fixed
duration $d_i$ somewhere inside a time window $[e_i, l_i]$, and can attend
only one meet at a time. Maximising the number of completed meets is the
single-machine throughput problem with release times and deadlines,
$1 \mid r_j, d_j \mid \sum U_j$, which is strongly NP-hard
[@garey1979computers]. The package therefore ships two solvers and reports the
distance between them instead of claiming a cheap algorithm is also optimal.

The **heuristic** — the plan the mission executes — is earliest-deadline-first:
windows are ordered by latest feasible start $l_i - d_i$ and each is taken when
it still fits after the courier's current position, in the spirit of the
classical interval-scheduling greedy [@kleinberg2005algorithm]. It is linear
after the sort, but it is genuinely sub-optimal in general: a long, slack
window sorts first and can crowd out two short meets that together would have
scored higher. A concrete instance exhibiting this is pinned in the test suite.

The **exact optimum** is a dynamic program over subsets. Writing
$T(S)$ for the earliest time by which every meet in $S \subseteq \{1..n\}$ can
have been completed,

$$
T(\emptyset) = t_0, \qquad
T(S \cup \{j\}) = \min_{S} \; \bigl(\max(T(S), e_j) + d_j\bigr)
$$

over those $j \notin S$ with $\max(T(S), e_j) \le l_j - d_j$, and the answer is
the largest $|S|$ with $T(S)$ defined. Because feasibility of any extension is
monotone in the current time, retaining only the earliest completion time per
subset loses no optimal solution, so this is the true maximum rather than a
bound. It runs in $O(2^n n)$ and is bounded to small instances by construction.

Section 03 reports the heuristic count, the exact optimum, and their gap as
three separately computed tokens.

### 2.6 Defector handoff protocol

A handoff is a deterministic state machine over

$$
\text{DISARM} \to \text{MEET} \to \text{CHALLENGE} \to \text{CONFIRM} \to \text{HANDOFF},
$$

with a terminal $\text{ABORT}$ reachable from every active stage. The
confirm code is derived from the challenge and call sign via SHA-256:

$$
\text{confirm} = \text{hex}(\text{SHA256}(\text{call\_sign}: \text{challenge}))[0:6].
$$

Only an exact confirm-code match advances to `CONFIRM`; any other confirm
code lands the protocol in `ABORT` (the red-path drill).

## Results — LEKTOR: measured outcomes, headline numbers, and what they establish

All figures and numbers below are produced live by the package's engines and
injected as generated tokens; none are hand-authored. Regenerating the token map
with `scripts/z_generate_manuscript_variables.py` regenerates every quantity
in this section.

### 3.0 At a glance

| Engine | Headline measured quantity | Value |
|---|---|---|
| Entrapment | bite probability | 0.416 |
| Allocation (exact) | expected engagement value | 19.526 |
| Allocation (greedy baseline) | expected value | 19.526 |
| Allocation | exact-minus-greedy gap (canonical / witness) | 0.000 / 2.642 |
| SIGINT | recovered plaintext exact | True |
| SIGINT | empirical SNR | 79.5 dB |
| SIGINT | transmission bursts segmented | 1 |
| Direction finding | realised localisation error | 0.022 |
| Direction finding | Cramér–Rao RMS bound | 0.0504 |
| Courier (heuristic) | completed meets | 4 |
| Courier (exact) | optimum completes | 4 |
| Courier | heuristic gap (canonical / witness) | 0 / 1 |
| Handoff | green state / red-path state | handoff / abort |

Every cell is a generated token — a live output of the corresponding engine —
so the table cannot drift from the code that produces it.

### 3.1 Lure effectiveness and allocation

For the fixed lure campaign `honey-trap-alpha`, the computed bite probability
is **0.416** against an engagement threshold of
**0.50**, and the trap resolved to
**aborted**.

Across the analytical pool of **6 targets** at lure
strength **0.60**, the exact knapsack allocation
spent **5 of 5 budget units**
(utilization **100%**) across
**4 targets**, for an expected engagement value of
**19.526**. The profit-density greedy baseline reached
**19.526** on the same instance — a measured gap of
**0.000**.

That gap is zero: on the canonical target pool the cheap heuristic finds the
optimum, and this instance therefore **separates the two solvers not at all**
(greedy ties: **True**). We state that plainly
rather than reporting the inequality $\text{exact} \ge \text{greedy}$ as a
finding: that inequality is a theorem about the exact solver, not a property
of this scenario, and it could only come out false if the knapsack
implementation were broken. Reporting it as a result would be green by
construction.

The separation is instead measured where it exists. On the witness pool of
§2.2 — **3** targets under a budget of
**5**, deliberately constructed so that a
profit-density pick blocks the optimal one — the exact allocation reaches
**8.808** against the greedy
**6.166**, a strictly positive gap of
**2.642**. That is the falsifiable claim: were the exact
solver merely greedy in disguise, this gap would collapse to zero, and the
test suite pins it.

![LURE surface: bite probability vs. lure strength and target susceptibility.](output/figures/from_russia_with_love_lure_surface.png)

### 3.2 SIGINT interception

A **47-byte** message was enciphered under
**2** keystream layers and intercepted at a requested
**80.0 dB**; the empirical SNR measured against ground truth was
**79.5 dB**. The recovered plaintext matched the
transmitted message exactly: **True**. The decided
capture carried **45 distinct symbol values** and its
energy envelope segmented into **1 transmission
burst(s)**.

### 3.3 Direction finding

With **4** intercept sites at
**A (0, 0); B (20, 0); C (20, 20); D (0, 20)**, a true transmitter at
**(7, 9)**, and seeded timing noise of standard deviation
**0.10**, the TDOA Gauss–Newton estimator converged
(**True**) in **5** iterations to a
transmitter localisation error of **0.022 receiver coordinate
units**.

The units matter. `localization_error` returns a raw Euclidean distance in
the coordinate system the receivers are declared in — it is not normalised by
the array geometry. The smallest distance between two intercept sites is
**20.0** coordinate units, so the same error expressed
as a fraction of the site spacing is **0.0011**. Both
numbers are generated from the same computation; only the second one is "in
units of site spacing".

A useful uncertainty framing is the **Cramér–Rao lower bound** on the position
error — the theoretical best achievable RMS accuracy given the receiver
geometry and the timing noise, computed from the Fisher information matrix at
the true transmitter position (see `direction_finding.py::crlb_error`). For
the canonical array and `0.10` s timing noise, that bound
is **0.0504** coordinate units. The realised Gauss–Newton estimate
achieved an error of **0.022**, which is
**False** above that bound. This is honest
uncertainty quantification rather than a single point claim: the CRLB is a
bound on achievable *variance* across draws, so one particular noise
realisation may land on either side of it (as it does here), and a degenerate
array with no finite accuracy has an infinite bound rather than a fabricated
confidence.

![TDOA geometry: intercept sites, true transmitter, and estimate.](output/figures/from_russia_with_love_tdoa_geometry.png)

### 3.4 Handoff scheduling

Of **5** candidate rendezvous, the
earliest-deadline-first heuristic completed **4**,
finishing at time **9.5**. The exact subset dynamic
program of §2.5 puts the true maximum at **4**, so
the heuristic's cost on this instance is a gap of **0**
meets. The heuristic is not optimal in general — §2.5 describes the family of
instances on which it loses, and the test suite pins a concrete one — so this
gap is a measured property of the canonical scenario, not a guarantee about
the algorithm.

That canonical gap is zero, and we say so plainly: on `scenario.RENDEZVOUS` the
heuristic genuinely reaches the optimum, so this instance separates the two
solvers not at all. Where the scheduler's sub-optimality is *visible* is the
witness instance of §2.5 (`scenario.SCHEDULE_WITNESS`), deliberately built so a
long, slack window sorts first and crowds out two short meets. On that
instance the heuristic can complete **1** of
**3** rendezvous against a true optimum of
**2** — a strictly positive gap of
**1** meet, pinned by the test suite. Reporting
both instances is the honest version of the claim: the exact solver is
necessary precisely when the problem is hard, and the canonical scenario is
the easy case where the cheap heuristic happens to be optimal.

### 3.5 Defector handoff protocol

The green-pathed handoff for the mission call sign completed in state
**handoff**, gated on confirm code
**66b2aa**. The red-path drill — the identical protocol run
given a deliberately wrong confirm code — ended in
**abort**, confirming that only the exact code completes a
handoff, and that a failed confirm is an ordinary terminal outcome rather
than an exception.

## Conclusion — LEKTOR: findings, verdict, and what the mission establishes

LURES turns the operational fiction of a Cold-War deception mission into a
small, fully deterministic mission-software package. The
6 engines — an entrapment playbook with a validated
trap state machine, an exact knapsack lure-budget allocation, a SIGINT
interception simulation with real cipher, noise and burst-segmentation models,
a TDOA Gauss–Newton transmitter geolocation, an earliest-deadline-first
handoff schedule, and a defector handoff protocol whose confirm code gates
completion — each compute a result rather than assert one. The same fixed
inputs always yield the same lure outcome, allocation, recovered plaintext,
localisation, schedule, and handoff path.

The package's more durable contribution is methodological rather than
narrative. Two of its engines solve problems where a cheap answer is available
and a correct one is expensive, and in both cases the package computes both
and publishes the difference: the knapsack allocator against a profit-density
greedy baseline, and the courier scheduler against an exact subset dynamic
program. Publishing the difference includes publishing it when it is zero — on
the canonical target pool the greedy allocator ties the exact knapsack, so
that instance demonstrates nothing about the exact solver's necessity, and the
separation is measured on an explicit witness instance instead. The scheduling
case is the sharper one, because the obvious greedy
ordering *looks* like the classical optimal interval-scheduling algorithm and
is not — the underlying problem becomes NP-hard once meets carry both release
times and deadlines. Reporting 4 completed meets
against an optimum of 4 is a weaker-sounding claim
than reporting an optimal schedule, and it is the one the code can actually
support.

Every stage is reproducible, mock-free, and covered by a real-data test suite
above the package's 90% line-and-branch gate. Where a branch is defensive
rather than exercised — a singular Jacobian, a coincident intercept site — it
is documented as such rather than papered over with an artificial test.

The package is also honest about what it does *not* know. TDOA localisation
carries a Cramér–Rao uncertainty bound rather than a single over-confident
number; both optimality gaps are reported even when they are zero; and the
seeding is disclosed as fixing one realisation of a stochastic model, not the
whole distribution. A deterministic mission model that states its own
uncertainty is more useful — and more defensible — than one that merely looks
deterministic.

## Experimental Setup — LEKTOR: canonical scenarios, parameters, and configuration

### Where the parameters live

Every executed constant is declared in
`src/from_russia_with_love/scenario.py`, which is the single source of truth
shared by the mission adapter, the manuscript token generator, and both figure
generators. `manuscript/config.yaml` restates the headline mission parameters
for a human reader and supplies the paper metadata (title, authors, keywords);
`manuscript_variables.validate_mission_config` compares the two on every
manuscript build and raises if they disagree, so the restatement cannot drift
away from the code silently.

The token generator reads `config.yaml` for paper metadata only. Every
quantitative token below is computed by running the engines.

### Mission parameters

| Parameter | Value |
|---|---|
| Objectives | 6 |
| Analytical engines | 6 |
| Fixed seed | 11 |
| Bait profiles | 3 |
| Engagement threshold | 0.50 |
| Allocation targets | 6 |
| Lure strength | 0.60 |
| Lure budget (units) | 5 |
| Message length (bytes) | 47 |
| Cipher layers | 2 |
| Requested channel SNR | 80.0 dB |
| TDOA intercept sites | 4 |
| TDOA receiver coordinates | A (0, 0); B (20, 0); C (20, 20); D (0, 20) |
| TDOA true transmitter | (7, 9) |
| TDOA minimum site spacing (coordinate units) | 20.0 |
| TDOA timing noise (s) | 0.10 |
| Candidate rendezvous | 5 |
| Greedy-witness targets / budget | 3 / 5 |

Receiver and transmitter positions are dimensionless coordinates in the
scenario frame, and `TDOA_SPEED` is 1.0, so distance and time share units. The
localisation error reported in §3.3 is therefore in these coordinate units;
the site spacing row is what converts it to units of site spacing.

### Software Environment

| Component | Value |
|---|---|
| Python | 3.14.6 |
| Platform | darwin |
| numpy | 2.5.1 |
| Package version | 0.1.0 |
| Manuscript date (`config.yaml` `paper.date`) | 2026-08-04 |

## Reproducibility — LEKTOR: verification gates, deterministic regeneration, and artifacts

### Determinism

Every engine is deterministic. The entrapment engine uses a closed-form
logistic model and seeded lure generation; SIGINT derives a seeded keystream
and seeded noise (seed 0 makes capture exactly noise-free); TDOA timing noise
is seeded; the courier scheduler, the knapsack allocator and the handoff
protocol use no randomness at all (SHA-256 only). The mission seed is
`scenario.SEED` = **11**, declared in
`src/from_russia_with_love/scenario.py` and mirrored into
`manuscript/config.yaml` under a build-time equality check.

Nothing in the package reads the wall clock. There is no clock-derived token:
the date row in §5 is `2026-08-04`, taken verbatim from the committed
`paper.date` field of `manuscript/config.yaml`. Every other value is a function
of `scenario.py`, the engines, and the interpreter/library versions. Two
regenerations on the same tree therefore produce byte-identical artifacts —
the token map and both figures alike.

That claim is bound by a test rather than asserted: `test_regeneration_is_byte_identical`
in `tests/test_regeneration_determinism.py` runs the real generator script twice
as a subprocess and compares the SHA-256 of every persisted artifact. It does
*not* inject a fixed clock — injecting one is precisely how a wall-clock
dependency could hide behind a green suite, and this package shipped that bug
once. `test_no_wall_clock_read_under_src` is the positive control: it
fails if any module under `src/` calls `datetime.now`, `time.time`, or
`date.today`.

### Regenerating everything

```bash
uv sync --extra dev
uv run python scripts/z_generate_manuscript_variables.py
```

That writes `output/data/manuscript_variables.json` and re-renders both
figures. `output/` is disposable and git-ignored; nothing in it is ever
hand-edited.

### Verification Gates

- `uv run pytest tests/ --cov=src --cov-fail-under=90`
- `uv run ruff check src/ scripts/ tests/` and `uv run ruff format --check...`
- `uv run mypy src/ scripts/`
- `uv run python scripts/00_preflight.py` — protocol + pure-core sanity check
- `rg -n "template[_]code_project".` → zero surviving lineage strings

Two gates in the suite are positive-controlled rather than merely green: the
manuscript token cross-reference test fails if any token referenced in the
prose is not produced by `generate_variables`, and the drift guard between
`config.yaml` and `scenario.py` is
exercised with a deliberately mismatched config so that it is known to be able
to fail.

### Artifact Inventory

| Artifact | Path |
|---|---|
| LURE surface figure | `output/figures/lure_surface.png` |
| TDOA geometry figure | `output/figures/tdoa_geometry.png` |
| Manuscript variable map | `output/data/manuscript_variables.json` |

## Scope and Related Work — LEKTOR: boundaries, positioning, and relationship to the literature

### Scope

LURES is an analytical, deterministic mission model — not a real-world
targeting or deception tool. The entrapment engine models lure effectiveness
as a decision surface for defensive countermeasure evaluation; the knapsack
allocation and courier scheduler are combinatorial optimisation over synthetic
records; the SIGINT and TDOA modules simulate channel interception and
geolocation for study; the handoff protocol is a state-machine fragment. The
package performs no real signal capture, no cryptanalysis of live systems, and
no targeting of persons.

The XOR keystream cipher in `sigint.py` is a *pedagogical* construction for
producing a scrambled symbol stream to intercept. It derives its keystream
from a seeded PRNG, which makes it reproducible and completely unsuitable as
cryptography; nothing in this package should be read as a security claim about
the cipher.

Two further boundaries are worth stating plainly. First, the courier scheduler
is a heuristic and is not optimal (§2.5); the exact solver exists to measure
that gap, not to be run at scale, and refuses instances beyond its documented
size bound. Second, the bite-probability surface is a modelling *choice* — a
bounded logistic in strength and susceptibility — not an empirically fitted
model of anything, and its parameters are not calibrated against data.

### Uncertainty and limitations

Beyond the boundaries above, the package reports its uncertainty honestly
rather than implying that a deterministic single number is a confident one:

- **TDOA localisation uncertainty is quantified, not asserted away.** §3.3
 reports both the realised estimate error and the Cramér–Rao lower bound
 (`0.0504`) for the same geometry and timing noise. The CRLB is a
 bound on achievable *variance*, so a single seeded realisation can land on
 either side of it (the canonical realisation lands below it,
 `False`); a degenerate array has an infinite bound.
 The numbers are generated, not fitted, to a particular noise draw.
- **The seeding fixes the realisation, not the distribution.** Every quantity
 that is stochastic under the model — the SIGINT capture noise, the TDOA
 timing noise, the lure generation — is the outcome of one committed seed
 (`scenario.SEED`). Regeneration is byte-identical by construction, but a
 *different* seed would produce a *different* realisation of the same
 underlying distribution. The manuscript therefore reports what was actually
 computed, never a resample.
- **Both optimality gaps are measured, and may be zero.** The canonical
 allocation pool and the canonical rendezvous set both fail to separate the
 exact solver from its heuristic (gaps `0.000` and
 `0`); the separation is only visible on the witness
 instances (`2.642` and `1`).
 Reporting the zero as zero prevents the exact solvers from being dressed up
 as necessary where they are not.
- **The decipherability result is a high-SNR, seed-specific outcome.** At
 `80.0` dB the recover is exact (`True`) on
 this draw; below some SNR ceiling byte recovery would fail. The package makes
 no claim about performance at low SNR.
- **The XOR keystream cipher is pedagogical.** It is derived from a seeded PRNG
 and is unsuitable as cryptography (§2.3). Nothing here is a security claim.

### Related Work

- **BOND-API (THE PROTOCOL)** — the frozen `MissionProvider` contract this
 film implements (discovery, lifecycle, provenance) [@bond_api].
- **BOND-UTILITIES (Q-BRANCH)** — the Layer-0 foundation (ciphers, codenames,
 provenance persistence, reporting) that downstream packages may bind to
 [@bond_utilities].
- **Combinatorial optimisation** — exact 0/1 knapsack via dynamic programming
 [@martello1990knapsack], on the classical dynamic-programming formulation
 [@bellman1957dynamic]; interval-scheduling greedy algorithms
 [@kleinberg2005algorithm]. The scheduling problem solved here,
 $1 \mid r_j, d_j \mid \sum U_j$, is strongly NP-hard
 [@garey1979computers], which is why the package pairs a heuristic with an
 exact subset dynamic program rather than claiming optimality.
- **Localisation** — hyperbolic (TDOA) position estimation. The solver
 implemented in `direction_finding.py` is the **iterative Taylor-series /
 Gauss–Newton** estimator [@foy1976position; @torrieri1984statistical],
 i.e. The standard non-linear least-squares iteration
 [@nocedal2006numerical] applied to the pair TDOA residuals from a receiver
 centroid start. It is *not* the Chan & Ho estimator
 [@chan1994hyperbolic]: that is a **closed-form, non-iterative** two-stage
 weighted least-squares solution, published as an alternative to exactly the
 iterative scheme used here. Chan & Ho is listed as related work, and this
 package does not implement it.
- **Channel and cipher models** — the additive white Gaussian noise channel
 and symbol-decision model follow standard digital-communications treatment
 [@proakis2008digital]; the keystream construction is an elementary
 one-time-pad-style XOR stream in the sense of Shannon's secrecy analysis
 [@shannon1949secrecy]. The handoff confirm code uses SHA-256 as specified in
 the NIST secure hash standard [@nist2015fips180].
- **Decision surface** — the logistic response model used for bite
 probability is the classical binary-response form [@cox1958regression].
- **Source material** — Ian Fleming's novel [@fleming1957russia], of which the
 1963 film is an adaptation.

## Sources — LEKTOR: bibliography

@bond_api; @bond_utilities; @foy1976position; @torrieri1984statistical; @chan1994hyperbolic; @nocedal2006numerical; @martello1990knapsack; @bellman1957dynamic; @kleinberg2005algorithm; @garey1979computers; @proakis2008digital; @shannon1949secrecy; @nist2015fips180; @cox1958regression; @fleming1957russia


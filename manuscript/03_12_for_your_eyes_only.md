# For Your Eyes Only (1981) — ATAC

*film package · package codename ATAC*. Mission **ATAC**: recover the lost ATAC targeting-communicator key; verify custodian custody before release; plan underwater retrieval and island insertion.

## Concepts — ATAC: domain and operational focus

targeting systems, key recovery

## Abstract — ATAC: mission summary

**For Your Eyes Only: ATAC — Special-Agent Mission Software** — Targeting-Communicator Escrow, Underwater Retrieval, and Greek-Island Insertion Routing. This report documents the **ATAC** special-agent mission software: a deterministic suite for recovering a lost targeting-communicator device and directing it onto target. The mission's mathematics rest on six pillars, each implemented as a pure, infrastructure-free domain module: 1. **Key escrow** — the ATAC key is split among 3 custodians using Shamir secret sharing, with a quorum of 2 required to release it (key 1390851129; match True), and custody is carried as an audited 3-record hash-chained ledger (True). 2. **Erasure-coded key recovery** — 4 data symbols encoded into 6 code fragments so any quorum recovery survives loss/corruption (match True). 3. **Underwater retrieval planning** — a Haldane-style staged dive of 3580.722 s to the 42-m wreck: a 600 s bottom exposure, then 14 tissue-sized decompression stops, against a drift offset of (-143.229, 71.614) m (reachable: True). 4. **Greek-island insertion routing** — a least-cost route (corfu -> paxi -> lefkada -> ithaca -> wreck_site, 56.00 nm). 5. **Fire-control targeting** — an intercept lead-angle firing solution (94.6 s, 9.89° lead; feasible True). 6. **Underwater acoustic link** — a link budget with SNR 52.33 dB at 3500 m against a 8 dB threshold, a margin of 44.33 dB (closes: True; max range 18553 m). Every computation is deterministic — a single fixed seed (7), no untracked randomness, no wall-clock dependence in persisted artifacts — and each concept carries a matching real-data test suite with no mocking framework. Every quantity above is injected from the code that computed it rather than typed into the prose, and the escrow's fingerprint match is re-derived by comparison rather than asserted, so a wrong result would surface as a changed number instead of a stale claim. Keywords: key escrow and recovery, Shamir secret sharing, erasure coding, underwater retrieval planning, decompression modelling, island routing, fire-control targeting, underwater acoustic link budget, deterministic mission software.

## Introduction — ATAC: mission framing, the operational problem, and how to read this chapter

The ATAC (Automatic Targeting Attack Communicator) is a lost-key device whose
recovery demands coordinated custody, underwater access, and insertion
planning, after which it must be directed onto target and communicate that
solution acoustically. For Your Eyes Only (1981) frames the operational
scenario; this package implements the mission mathematics as reproducible,
deterministic software in the PROJECT BOND film suite.

The six domain modules form the core of the mission:

* `key_escrow` — escrow/recovery of the ATAC key (Shamir custody, verification,
 quorum release).
* `key_recovery` — erasure-coded reconstruction so key fragments survive loss
 or corruption.
* `underwater_retrieval` — sea-based recovery of the device from the wreck,
 compensating for depth and currents.
* `island_routing` — Greek-island insertion routing from the staging base to
 the wreck's vicinity.
* `targeting` — fire-control intercept lead-angle firing solution.
* `acoustic_link` — underwater acoustic uplink budget for the recovered device.

A shared, frozen protocol (BOND-API) defines the mission lifecycle — brief,
recon, plan, execute, debrief — and the `mission` module adapts the pure
domain mathematics to that contract, registering the suite's gadgets for
orchestration. This separation keeps the mathematics infrastructure-free and
importable without the protocol, while the adapter makes the mission
discoverable by the broader BOND orchestrator. The mission's public protocol
surface is stable across phases; only the internal scenario deepens.

### Reader's guide

* §2 describes the mathematical methods behind each domain module.
* §3 presents the computed mission results and figures.
* §5 details the experimental configuration; §6 the reproducibility contract.

## Methodology — ATAC: the analytical models and algorithms that drive the mission

This section details the deterministic mathematics behind each of the six
mission modules.

### Key escrow and recovery

The ATAC key is escrowed using **Shamir's secret-sharing scheme**
[@shamir1979share] — independently co-discovered the same year by Blakley via
intersecting hyperplanes [@blakley1979safeguarding] — over the
finite field $\mathrm{GF}(p)$ with $p = 2^{61} - 1$. A random polynomial

$$f(x) = a_0 + a_1 x + \cdots + a_{k-1} x^{k-1} \pmod{p}$$

is sampled with constant term $a_0$ equal to the key; each of $n$ custodians
receives a distinct point $(x_i, f(x_i))$. Any $k$ points reconstruct the
polynomial — and hence the key — by Lagrange interpolation:

$$f(x) = \sum_{i=1}^{k} f(x_i) \prod_{j \neq i} \frac{x - x_j}{x_i - x_j} \pmod{p},$$

while fewer than $k$ shares reveal nothing about the key. The mission uses
$n = $3 shares and a quorum $k = $2.

**Verification.** Each share $(x_i, y_i)$ is committed as $g^{y_i} \bmod p$
for a primitive root $g$; any party holding a claimed share can verify it
against the commitment, so a share tampered with during custody is rejected
before release.

**Custody.** Handoffs are recorded in a SHA-256 hash-chained ledger, binding
the whole custody history append-only. The canonical mission **carries** one: a
ledger over the 3-custodian chain (3
records) is bound to the escrow at creation, its well-formedness recomputed
(True) and its tip hash (6caf9ee7a9d5cc3dd790725b384fcfc85be569dd89eae5890441c34bc6160980) reported, so
the advertised audit trail is not an empty field.

**Release.** Release reconstructs the key from a verified quorum and confirms
it reproduces the escrow's key fingerprint. The recovered key is
1390851129 (matches fingerprint: True). The
match is obtained by recomputing $\mathrm{SHA\text{-}256}(k)$ over the released
key and comparing it to the stored fingerprint, so the reported value is a
measurement rather than a restatement of an intention.

**Key derivation.** The escrowed key is derived from the mission seed at import
time rather than written down as a literal, so there is exactly one place the
key can come from and no configuration file can claim a different one.

### Erasure-coded key recovery

To survive the loss or corruption of an individual stored fragment, the
released key is also protected by a **systematic Reed–Solomon-style erasure
code over GF(p)** [@reed1960polynomial; @berlekamp1968algebraic]. The key is treated as $k = $4
data symbols; a generator polynomial is evaluated at
$n = $6 distinct field points, producing those
code symbols. Because any square Vandermonde subsystem is invertible over a
field, **any $k$ of the $n$ code symbols reconstruct the key** — the erasure
property (recovered matches original: True). An integrity
checksum detects a corrupted fragment so a bad fragment never silently yields
a wrong key.

The decoder takes the positions of the surviving fragments explicitly, which is
what makes the erasure property exercisable rather than merely asserted: a
decoder hard-wired to the leading $k$ fragments would satisfy the round-trip
test while being unable to survive the loss of fragment 0. Selecting the
evaluation points $x_i$ of the actual survivors and solving that Vandermonde
subsystem is the general case.

### Underwater retrieval planning

The device rests on the seabed at depth $d$ under a horizontal current
$(u, v)$. A **Haldane-style tissue model** [@boycott1908prevention] — a set of
compartments each with half-time $t_{1/2}$ — drives the decompression schedule. Compartment pressure
relaxes exponentially toward the ambient pressure with time constant
$\tau = t_{1/2}/\ln 2$.

**Current-drift compensation.** Over a total dive time $T$, a stationary
descent bell drifts by $-T(u, v)$ relative to the seabed target. The bell
therefore starts at offset $(T u, T v)$ upstream. The planned wreck depth is
42 m; total dive time 3580.722 s yields a
surface offset of (-143.229, 71.614) m
(within tolerance: True).

**Decompression ceiling.** Each compartment has an M-value ceiling; the
no-decompression bottom time is the exposure at which the limiting compartment
first saturates to its ceiling,
$t_i = \tau_i \ln\frac{P_{amb}-1}{P_{amb}-M_i}$, in the multi-compartment form
of [@buhlmann1984decompression].

**Staged ascent.** The ascent is decomposed into stops snapped to a fixed
interval, and each stop's duration is sized *directly from the tissue state*:
the diver holds at a stop for the time the limiting compartment needs to
off-gas to its ceiling at the next (shallower) stop, then climbs at the ascent
rate. The profile is therefore a function of the exposure itself — a deeper
wreck produces more stops, and a longer bottom time produces longer holds —
rather than a fixed geometric schedule. This is the difference that matters for
the figure and the reported profile: every stage boundary is now a
decompression obligation.

We state the boundary of this model plainly, because it is easy to overread.
The staging couples to the tissue model, but the tissue parameters are
classroom-grade — a proportional M-value ceiling ($\text{ceiling} = m_i \cdot
P_{amb}$) rather than a field-validated Bühlmann line — so the profile is
deterministic and internally consistent but is **not a certified decompression
schedule**. `no_decompression_limit` remains an independent quantity the
scheduler does not consult; the canonical dive's bottom exposure and stop count
are reported as live results (600 s bottom,
14 stops, 2841 s of ascent), not fixed
geometric constants.

### Greek-island insertion routing

The Ionian islands are modelled as a **weighted undirected graph** with fixed
node positions; each edge carries a distance (nm) and a risk weight. Routing
finds the minimum-*cost* path, where edge cost blends distance and risk:
$c = d + \lambda r$ with a configurable risk penalty $\lambda$. The planner
uses **Dijkstra's algorithm** [@dijkstra1959note], or A* with a straight-line
admissible heuristic [@hart1968formal], returning the same optimum
deterministically.

**What $\lambda$ does and does not do here.** Raising $\lambda$ always raises
the cost of a route, but on the shipped Ionian graph it never changes which
route is chosen: the least-distance and least-risk corridors coincide for every
one of the 28 node pairs. So this package demonstrates the *cost* blend, not
risk-driven path selection; the selection mechanism is exercised on a separate
two-option graph in the test suite. Read the canonical route below as the
shortest route, which on this graph is also the safest.

The canonical insertion route is corfu -> paxi -> lefkada -> ithaca -> wreck_site — 4 hops,
56.00 nm, total cost 57.000.

### Fire-control targeting

The ATAC targeting-communicator directs a weapon onto a moving contact using
the classical *constant bearing, decreasing range* intercept. With target at
$p_0$ moving at velocity $v_t$ and weapon speed $v_w$, interception satisfies
$|p_0 + v_t t| = v_w t$, giving the quadratic
$(|v_t|^2 - v_w^2) t^2 + 2(p_0\cdot v_t) t + |p_0|^2 = 0$. A positive root is
the intercept time $t_i$; the weapon course is
$u = (p_0 + v_t t_i)/(v_w t_i)$, whose angular offset from the line of sight is
the **lead angle**. For the canonical engagement the intercept is
feasible (True) at $t_i = $94.6 s with a
lead angle of 9.89°; where interception is impossible the
module reports the closest-approach distance instead
(0.0 m).

### Underwater acoustic link budget

The recovered device uplinks targeting data acoustically to a surface relay.
**Transmission loss** combines geometric spreading with frequency-dependent
absorption via **Thorp's formula** (dB/km) [@thorp1967analytic]. Geometric
spreading is $10 n \log_{10} r$ for a spreading exponent $n$ — $n = 2$
spherical, $n = 1$ cylindrical — and the wreck uplink is modelled as a
shallow-water horizontal channel, so it uses $n = 1$. The ambient noise term NL
is computed from a declared sea state: the module applies a smooth, monotone
*stand-in* for how wind-driven deep-water ambient noise grows with sea state
— the family quantified by Wenz's spectra [@wenz1962noise] — rather than a
reproduction of them or a hand-entered decibel literal. Received SNR is
$\text{SNR} = \text{SL} - \text{TL} - \text{NL} + \text{DI}$
[@urick1983principles] and the link
*closes* when SNR exceeds the detection threshold $\text{DT}$. The **margin**
is $\text{SNR} - \text{DT}$ — the signal in hand beyond the point of
detectability — so closure is exactly a non-negative margin. At the
3500-m operating range the received SNR is
52.33 dB against a 8 dB threshold,
a margin of 44.33 dB (link closes:
True).

**Maximum range.** Since SNR falls monotonically with range, the coverage
radius is the unique root of $\text{SNR}(r) = \text{DT}$, found by bounded
bisection: 18553 m. The bracket endpoints are reported
honestly — a link that already fails at the bracket floor has a coverage radius
of zero, not a coverage radius equal to the floor, and a link still closing at
the ceiling returns that ceiling as a lower bound.

## Results — ATAC: measured outcomes, headline numbers, and what they establish

The mission was executed end to end through the frozen protocol; all results
below are computed live by the domain modules (never hand-authored).

| Stage | Result |
|---|---|
| Escrow release | quorum 2-of-3 · key 1390851129 · fingerprint match True · custody True (3-record chain) |
| Erasure-coded recovery | 4-of-6 · recovered match True |
| Underwater retrieval | 42 m · 600 s bottom · 14 decompression stops · 3580.722 s total · surface offset (-143.229, 71.614) m · reachable True |
| Island routing | corfu -> paxi -> lefkada -> ithaca -> wreck_site · 4 hops · 56.00 nm · cost 57.000 |
| Fire control | feasible True · intercept 94.6 s · lead 9.89° · closest-approach 0.0 m |
| Acoustic link | SNR 52.33 dB at 3500 m · TL 44.06 dB · threshold 8 dB · margin 44.33 dB · max range 18553 m · closes True |

### Escrow release

A quorum of 2 of 3 custodians
releases the key deterministically. The reconstructed key is
1390851129, confirmed to match the escrow fingerprint
(True). A smaller quorum is rejected, and a tampered
share fails verification before release.

Custody is an audited concern here, not decoration: the escrow carries a
3-record SHA-256 hash-chained ledger of the handoffs, whose
well-formedness is recomputed (True) and whose tip hash is
6caf9ee7a9d5cc3dd790725b384fcfc85be569dd89eae5890441c34bc6160980.

That confirmation is *re-derived*, not asserted: the SHA-256 fingerprint of the
released key is recomputed and compared against the one the escrow stored. This
matters because the preflight check treats the same value as a pass/fail
verdict — had it been a stapled literal, the verdict could never have failed
and would have reported success regardless of what release returned.

### Erasure-coded key recovery

The released key is encoded as 4 data symbols
into 6 code fragments over GF(p). Any
4 fragments recover the key (recovered matches
original: True), and a corrupted fragment is detected by
the integrity checksum before it can yield a wrong key.

The any-`k` claim is tested as stated rather than in its easy form: the decoder
takes an explicit set of surviving fragment positions, and the test suite
enumerates *every* combination of surviving fragments — including sets that
contain none of the leading ones — and requires each to reconstruct the key.
Requesting checksum verification when no checksum symbol is present is an
error rather than a silent skip, so a caller asking to be protected is never
told that nothing was wrong.

### Underwater retrieval

The retrieval dive to 42 m completes in
3580.722 s of deterministic profile time: a
600 s bottom exposure followed by
14 decompression stops totaling 2841 s
of ascent, each stop sized from the compartment ceilings (see §2). The surface
drift offset is (-143.229, 71.614) m;
the target is reachable within the operational envelope
(True). The depth-time profile is shown in
the dive profile figure.

![ATAC underwater retrieval dive profile](output/figures/for_your_eyes_only_dive_profile.png)

### Island insertion routing

The least-cost insertion route from the staging base to the wreck site is
corfu -> paxi -> lefkada -> ithaca -> wreck_site (4 hops, 56.00 nm,
cost 57.000). The route cost blends distance and risk, but on
this graph that blend never changes the answer: for all 28 node pairs the route
chosen at risk weight 0 is the route chosen at risk weight 50, because the
Ionian island chain's safest corridor is also its shortest. The reported route
is therefore the shortest route, and this section claims nothing more for it.
The risk term is exercised as a mechanism on a purpose-built two-option graph
in the test suite, not here. The Ionian graph and planned route are shown in
the island graph figure.

![ATAC Ionian insertion route](output/figures/for_your_eyes_only_island_graph.png)

### Targeting solution

The ATAC fire-control solution for the canonical contact is feasible
(True) with an intercept time of 94.6
s, a lead angle of 9.89° and a weapon course of
54.89°; where a close is not achievable, the module
reports the closest-approach distance (0.0 m). The
intercept geometry is shown in the targeting geometry figure.

![ATAC targeting intercept geometry](output/figures/for_your_eyes_only_targeting_geometry.png)

### Acoustic link budget

At the 3500-m operating range the ATAC uplink receives
52.33 dB (path loss 44.06 dB) against a
8 dB detection threshold, leaving a margin of
44.33 dB; the link closes (True) with a
maximum acoustic range of 18553 m. Because the operating
range sits inside that maximum, the uplink is not run at the edge of its
budget. The SNR-vs-range curve is shown in the acoustic link figure.

![ATAC underwater acoustic link budget](output/figures/for_your_eyes_only_acoustic_link.png)

## Conclusion — ATAC: findings, verdict, and what the mission establishes

This package delivers a complete, deterministic ATAC special-agent mission
implementation. The six domain modules — key escrow and erasure-coded
recovery, underwater retrieval planning, Greek-island insertion routing,
fire-control targeting, and underwater acoustic link budgeting — each encode
real, verifiable mathematics: Shamir secret sharing with quorum release and
commitment verification; Vandermonde/Reed–Solomon-style erasure coding; a
Haldane-style decompression model with current-drift compensation; weighted-
graph shortest-path routing; a pursuit-geometry intercept lead-angle solution;
and a Thorp-absorption link budget.

The mission runs end to end through the frozen BOND-API protocol, is
discoverable by the orchestrator, and registers its gadgets. Every number in
this manuscript is computed from the code and injected via tokens, so the
report cannot drift from the implementation; a single canonical scenario feeds
both the mission outcome and the manuscript variables, guaranteeing they
agree.

The architecture — a pure infrastructure-free domain core (six modules), a
thin frozen-protocol adapter, and thin per-phase CLIs — matches the PROJECT
BOND convention and keeps the package both self-contained and ready to bind
to shared suite dependencies as they land.

### On verdicts that can fail

A recurring hazard in software that reports on itself is the check that cannot
fail: a verdict stapled to a literal, a decoder whose general case is never
exercised, a margin that restates the quantity it claims to qualify, a
configuration block nothing reads. Each of those was present in an earlier
revision of this package and each has been replaced by a derived value bound to
a test. The escrow's fingerprint match is now recomputed and compared; the
erasure decoder accepts arbitrary surviving-fragment sets and is tested across
all of them; the link margin is measured against the detection threshold; and
the declared mission configuration is pinned to the constants the mission
executes with. None of this changes what the software computes — it changes
whether a wrong answer would be visible, which is the property the rest of the
report depends on.

A second deepening pass applied the same discipline to three remaining hollow
claims: the ascent staging now sizes each decompression stop from the tissue
model's compartment ceilings (the reported profile is a genuine decompression
obligation, not a geometric sketch); the escrow's custody chain is now carried
by the mission as a real SHA-256 hash-chained ledger whose consistency is
recomputed rather than assumed; and the preflight dive verdict now has an
endurance ceiling it can actually fail on, exercised through a deterministic
environment seam. As before, each binds a claim to a derived value that a test
must hold true — a deeper wreck, a longer bottom, or a broken custody link now
moves the reported numbers rather than silently restating an intention.

## Experimental Setup — ATAC: canonical scenarios, parameters, and configuration

### Configuration

The mission is configured declaratively in `manuscript/config.yaml` and read
by `src/for_your_eyes_only/manuscript_variables.py`. The canonical escrow uses
threshold 2 of 3 shares; the
key is further erasure-coded as 4 data symbols
into 6 fragments. The underwater profile targets
a wreck depth of 42 m with a 600-s
bottom exposure under a calm horizontal current, decompressed through
14 tissue-sized stops; routing spans the Ionian island graph
to the wreck site (route corfu -> paxi -> lefkada -> ithaca -> wreck_site); and the acoustic uplink runs at
3500 m.

### Software environment

* Python version: 3.14.6
* Mission package: for_your_eyes_only (ATAC), version
 0.1.0
* Title: For Your Eyes Only: ATAC — Special-Agent Mission Software
* Keywords (9): key escrow and recovery, Shamir secret sharing, erasure coding, underwater retrieval planning, decompression modelling, island routing, fire-control targeting, underwater acoustic link budget, deterministic mission software
* Source date (deterministic build stamp, not the time of rendering):
 2026-08-04T00:00:00+00:00

All computations are deterministic: fixed seeds, no untracked random draws, no
wall-clock dependence in persisted artifacts. The stamp above is the declared
`paper.date` (or `SOURCE_DATE_EPOCH` when set), so re-rendering this section
tomorrow produces the same bytes; it deliberately does not report when the
render happened, because that value cannot be both honest and reproducible.

## Reproducibility — ATAC: verification gates, deterministic regeneration, and artifacts

### Determinism contract

* **Fixed RNG seed** — escrow share generation is the only stochastic step and
 it draws from a fixed seed (ATAC seed 7);
 every other module is pure arithmetic. No untracked randomness anywhere.
* **No wall clock in artifacts** — provenance records a zero wall time, and the
 one date written into the tree is a *build stamp* resolved from tracked
 inputs (`SOURCE_DATE_EPOCH` when set, otherwise the declared `paper.date`),
 never from `datetime.now`. This was not true until recently: the stamp read
 the wall clock, so two runs seconds apart wrote different bytes and the
 byte-identical claim below was false. It is now enforced by a test that runs
 the real generator twice and diffs every byte, plus a control asserting
 today's date does not appear anywhere in the tree.
* **No mocks** — tests exercise real data and real computation only.
* **Gates** — the suite must pass `pytest --cov=src --cov-fail-under=90`,
 ruff, and mypy; the manuscript token cross-reference is itself a test.

### Artifact inventory

The generation orchestrator writes:

* `output/data/manuscript_variables.json` — the full token map.
* `output/manuscript/` — resolved manuscript sections (no raw braces).
* `output/figures/island_graph.png`, `output/figures/dive_profile.png`,
 `output/figures/targeting_geometry.png`, `output/figures/acoustic_link.png` —
 the deterministic figure set.

Regenerating the tree reproduces byte-identical output — JSON, resolved
sections, and all four PNGs — which
`tests/test_scripts_smoke.py::test_regenerating_the_artifact_tree_is_byte_identical`
checks by running the generator twice into two roots and comparing every file.

### Test results

Test counts and coverage percentages are deliberately not quoted here. A number
typed into prose is a snapshot that decays silently on the next commit; the
*gate* is the durable claim, and it is stated instead:
`pytest tests/ --cov=src --cov-fail-under=90` must pass with zero failures and
zero skips. The measured figure is reported by that command, not by this
sentence.

The suite covers, per module: escrow split/recover round-trips, commitment
verification, quorum rejection and tamper rejection, and custody-chain linking
and integrity-breaking detection; erasure encode/recover round-trips,
exhaustive any-`k` recovery over every surviving-fragment combination, and
checksum corruption detection; underwater descent/ascent scheduling — including
the tissue-driven decompression staging, whose stop sizes are pinned to depth,
bottom time, and compartment half-times — drift compensation, and reachability
edges; routing optimality, Dijkstra/A* agreement pinned across every ordered
node pair, risk sensitivity, disconnected-graph and unknown-node errors;
fire-control intercept feasibility, lead-angle geometry, and the
closest-approach fallback on both the equal-speed and negative-discriminant
branches; and acoustic-link path loss, the geometric spreading exponent pinned
against its textbook law, SNR monotonicity, bisection closure, the
non-closing case, and rejection of non-finite knobs and degenerate brackets.

The preflight's two derived verdicts — the custody chain and the dive's
endurance ceiling — are both testable as failures: the custody verdict through a
tampered ledger, and the dive verdict through the deterministic
`ATAC_PREFLIGHT_BOTTOM_TIME_S` seam that drives `00_preflight.py` to a non-zero
exit.

Routing note: the suite pins the *cost* blend and, on a purpose-built
two-option graph, the risk term's ability to select a different path. On the
shipped Ionian graph the route is risk-invariant across all 28 node pairs; that
fact is itself pinned rather than left implied.

Three suites exist specifically to stop documentation drifting from code:

* `tests/test_config_consistency.py` pins every value declared in
 `manuscript/config.yaml`'s `mission:` block to the constant the mission
 actually runs with, so the config cannot decay into decoration.
* `tests/test_manuscript_variables.py` fails if any token used in prose is
 absent from `generate_variables`, or if a rendered section still contains
 an unsubstituted placeholder. (The token syntax itself is documented in
 `manuscript/SYNTAX.md`, which is excluded from that scan precisely because it
 must show the raw form.)
* `tests/test_manuscript_crossrefs.py` fails if a `references.bib` entry is
 never cited, if a citation names no entry, if a figure cross-reference uses
 the wrong syntax, or if a labelled figure has no generator. Those references
 sat outside every gate until this suite existed: all four figure references
 used the brace-delimited form, which pandoc-crossref does not recognise (see
 `manuscript/SYNTAX.md`), and the bibliography was cited by nothing at all.

See `tests/` and `docs/testing_philosophy.md`.

## Scope and Related Work — ATAC: boundaries, positioning, and relationship to the literature

### Scope

This package implements the deterministic mission mathematics for the ATAC
recovery scenario. It covers key escrow/recovery (including erasure-coded
reconstruction), underwater retrieval planning, island insertion routing,
fire-control targeting, and underwater acoustic link budgeting. It does not
attempt to model the physical dynamics of a real diving operation beyond the
closed-form Haldane saturation and ballistic drift used here; it is
mission-planning software, not a training simulator.

### Related work

* **Secret sharing** — Shamir's threshold scheme (1979) is the canonical
 construction for splitting a secret among parties such that a quorum can
 reconstruct it. Our implementation uses Lagrange interpolation over a
 Mersenne-prime field with deterministic share generation.
* **Erasure coding** — Reed and Solomon (1960) introduced the systematic
 polynomial code; our Vandermonde system over GF(p) realises the same
 any-`k`-of-`n` recovery property with an integrity checksum.
* **Decompression modelling** — Haldane-style multi-compartment tissue models
 underpin recreational and technical dive planning; our staged-ascent
 scheduler applies the same exponential-saturation principle deterministically.
* **Shortest path routing** — Dijkstra's algorithm and A* (with an admissible
 heuristic) are the standard tools for weighted-graph route planning; our
 Ionian insertion graph blends distance and risk into a single scalar cost.
* **Pursuit interception** — the constant-bearing intercept problem has a
 closed-form quadratic solution (see e.g. ballistics/fire-control texts); our
 lead-angle computation follows that classic geometry.
* **Underwater acoustics** — Thorp's absorption model and the sonar-equation
 link budget (source level, transmission loss, noise, directivity) are
 standard in underwater acoustic channel analysis.

### Limitations

The graph topology and positions are stylised (nominal nautical-mile grid, not
survey-grade chart data). The decompression staging couples to the tissue model
but uses classroom-grade proportional M-value ceilings rather than a
field-validated Bühlmann line, and the acoustic ambient-noise term is a smooth
monotone stand-in for sea-state noise, not a reproduction of Wenz's spectra;
neither is certified for live operations. The custody chain models a nominal
sequence of handoffs over the escrow's custodians — the audit *mechanism* is
real (SHA-256 hash chaining, recomputed consistency), but the handoffs
themselves are scenario fiction, not a recorded operational trail. These
simplifications keep the mission fully deterministic and testable while
preserving the mathematical substance of each concept.

## Sources — ATAC: bibliography

@shamir1979share; @boycott1908prevention; @dijkstra1959note; @hart1968formal; @reed1960polynomial; @thorp1967analytic; @urick1983principles; @wenz1962noise; @blakley1979safeguarding; @berlekamp1968algebraic; @buhlmann1984decompression


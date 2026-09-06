# Diamonds Are Forever (1971) — DIAMOND NET

*film package · package codename DIAMOND NET*. Mission **CONFLICT STONE**: trace the conflict-diamond custody chain and pinpoint provenance break points; optimize the smuggling corridor route under seizure risk; audit the diamond lot for weight and density fraud; map Las Vegas casino money movement and measure laundering closure; test the casino ledger against Benford's law; solve orbital-mirror targeting geometry and beam delivery.

## Concepts — DIAMOND NET: domain and operational focus

supply-chain provenance, orbital weapons

## Abstract — DIAMOND NET: mission summary

**Diamonds Are Forever: CONFLICT STONE — Special-Agent Mission Software** — codename **CONFLICT STONE** — is a deterministic special-agent mission analysis built on *Diamonds Are Forever* (1971). It fuses seven analytic lines into a single audit: the provenance chain of smuggled conflict diamonds, the risk-weighted corridor route that carries them, the physical forensics of the lot itself, the money-movement and Benford's-law tests of the Las Vegas casino operation, and both the targeting geometry and the beam-delivery physics of the orbital mirror the proceeds fund. **Provenance.** The custody chain comprises 5 handoffs with 2 undocumented break points — a documented coverage of 60%, the forensic signature of conflict goods. **Smuggling.** Across a 10-corridor network, the expected-cost optimum (sierra_leone -> nairobi -> paris -> amsterdam -> las_vegas) cuts expected cost by 16% versus the fewest-hops baseline, at a survival probability of 34%. **Forensics.** Weight and density testing of lot DF-71 surface 2 anomalies and a 4-point audit score — a **flagrant** verdict that exposes both the paste substitution and the final theft. **Casino.** A 7-casino money-movement graph whose laundering closure reaches 77%, and a 141-transaction ledger whose chi-square statistic ( 35.80) exceeds the 15.507 critical value and so marks it **anomalous** under Benford's law — while its 80-transaction legitimate baseline, audited alone, scores 0.53 and **conforms**, the negative control that makes the anomalous verdict attributable to the round-figure deposits. **Orbital.** Of 3 threatened cities, only 2 fall on the mirror's visible face; and honest beam physics shows the fantasy is bounded — delivering 1 MW/m2 at geostationary range takes a 42.7-m mirror. All results are reproducible: every metric is computed at runtime from fixed canonical datasets, no random draws, no mock objects, and every mission outcome carries a cryptographic input fingerprint.

## Introduction — DIAMOND NET: mission framing, the operational problem, and how to read this chapter

**Diamonds Are Forever: CONFLICT STONE — Special-Agent Mission Software** (**Deterministic Analysis of Smuggled-Goods Provenance and Routing, Lot Forensics, Casino Money Movement and Its Benford Signature, and Orbital-Mirror Targeting and Beam Delivery**) is the CONFLICT STONE mission
package of PROJECT BOND, a suite of deterministic special-agent mission
analyses. Each film package implements the frozen BOND-API mission protocol,
which fixes the contract every mission must satisfy: a `brief`, a `recon`, a
`plan`, an `execute`, and a `debrief`, each carrying typed provenance so an
outcome can be audited without re-running the mission.

This package's identity is `diamonds_are_forever`, version
0.1.0, under codename CONFLICT STONE. It adapts seven
pure analytic cores to the protocol, tracing the film's operation from the mine
to the satellite:

1. **Provenance chain** — a conflict-diamond custody graph with documented
 handoffs and identified provenance break points.
2. **Smuggling routes** — a directed corridor network in which each leg carries
 a transport cost and a seizure probability; an expected-cost shortest path
 is compared against a fewest-hops baseline in the same graph.
3. **Lot forensics** — weight and density reconciliation of the physical lot
 across its handoffs, separating legitimate cutting loss from theft and from
 paste substitution.
4. **Casino network** — directed money movement across the Las Vegas strip,
 with cycle detection, laundering-closure measurement, and hub discovery.
5. **Benford audit** — a leading-digit test of the casino ledger against
 Benford's law, scored by a Pearson chi-square statistic.
6. **Orbital mirror** — geostationary space-mirror targeting geometry:
 occultation, slant range, and elevation above the target's horizon.
7. **Beam physics** — what the mirror actually delivers: the diffraction-limited
 spot, atmospheric transmittance, the power budget, and the minimum mirror
 diameter a strike-class beam would require.

The first five cores prosecute the terrestrial half of the operation (who
touched the stones, how they moved, whether they are genuine, and where the
money went); the last two bound the orbital half in physics rather than in
plot. The mission software is a thin adapter over these cores: the domains are
pure and infrastructure-free, while the adapter handles only the protocol
wiring. This keeps every analytic claim testable in isolation and reproducible
by construction.

## Methodology — DIAMOND NET: the analytical models and algorithms that drive the mission

The CONFLICT STONE mission combines seven deterministic methods, each a pure
function of a fixed canonical dataset.

### Provenance chain

A custody chain is an ordered sequence of handoffs, each carrying a source, a
target, and a `recorded` flag. A valid chain is **continuous** (each handoff's
target is the next handoff's source) and **acyclic** (a gem never returns to a
previous holder). A handoff flagged `recorded=False` is a **break point** —
evidence that provenance cannot be verified at that step. The analytic surface
reports the break-point indices, the documented-coverage ratio, and whether the
chain is conflict-free.

### Smuggling corridor routing

The chain answers *who touched the goods*; corridor routing answers *which
route they travel*. A smuggler moves a fixed-value cargo through a directed
network of corridors, each carrying a transport cost and a seizure probability.
The expected cost of a corridor is `cost + p_seizure * cargo_value`. A
deterministic Dijkstra over expected cost returns the **least-risk route**, its
expected cost, and its survival (`product(1 - p)`). A fewest-hops BFS baseline
in the *same* graph bounds the **reduction** metric, which is therefore always
non-negative. The optimum is *cargo-dependent*: cheap corridors win at low
cargo value, low-seizure corridors at high cargo value, so the reduction is
reported as measured across a cargo sweep rather than as a single monotone
trend.

### Lot forensics

Physical laundering of a lot is audited handoff-by-handoff against three
forensic rules: a **weight gain** (impossible for a genuine lot) flags
accounting fraud or substitution; a **loss beyond the legitimate cutting
allowance** of 25% per handoff flags theft; and a
**measured density outside the diamond window**
(3.40-3.65 g/cm3 around nominal
3.52) flags a paste or simulant swap. Each violation
contributes to an audit score and a lot verdict
(`clean` / `suspicious` / `flagrant`); a single anomaly reads as *suspicious*,
two or more as *flagrant*.

### Casino money movement

The Las Vegas network is a directed, weighted graph whose edges aggregate
inter-casino transfers. The analysis computes gross flow, net positions, the
network **hub** (greatest gross flow — a degree-style centrality in the sense
of [@freeman1978]), the directed **money cycles** (laundering loops,
enumerated *completely* — each elementary circuit exactly once — by Johnson's
algorithm [@johnson1975], the classical circuit-enumeration problem of
[@tarjan1973]), and the **laundering closure** — the fraction of flow that
sits on a cycle. Completeness matters here: a back-edge DFS would quietly drop
a circuit that re-enters an already-traversed node, under-reporting the
closure, which is exactly the class of omission a rights-the-books laundering
screen must not commit.

### Benford's-law ledger audit

A laundering operation breaks the leading-digit distribution of its ledger by
clustering deposits on round figures. This module compares the ledger's
observed leading digits against Benford's law, `p(d) = log10(1 + 1/d)`
[@benford1938; @newcomb1881], with a Pearson chi-square statistic
[@pearson1900] against the df=8, alpha=0.05 critical
value of 15.507. Above the critical value the ledger is
flagged **anomalous** — the laundering signal that forensic digit analysis is
built to surface [@nigrini2012].

**The audit is exercised as a matched control pair.** A screen that fires on
every ledger detects nothing, so the canonical ledger is built from two halves
that are also audited separately:

- a **legitimate baseline** of 80 transactions —
 the *negative control*. Its leading digits are the leading digits of the
 Fibonacci sequence, which are Benford-distributed as a theorem: Binet's
 formula makes `log10 F_n` an irrational rotation, equidistributed mod 1 by
 Weyl's criterion. Conformance is therefore a property of the sequence, not
 of digit frequencies chosen to pass the test. The amounts are placed across
 the 10^2-10^4 decades, and scaling by a power of ten cannot change a leading
 digit;
- 61 **round-figure deposits** on
 1/2/5 x 10^n — the laundered cash.

Both halves are constructed fixtures, not empirical records. The pair
establishes that this implementation separates them; it is not evidence about
how the screen would behave on real books.

### Orbital targeting geometry

A geostationary mirror is modelled as a point above a sub-satellite point.
Targeting solves occultation (the beam ray's nearest approach to Earth's
centre), slant range, and elevation above the target's horizon.

### Beam delivery physics

The targeting geometry solves *where* the beam can go; beam physics solves
*what it delivers*. A diffraction-limited Airy spot `r = 1.22 * lambda * R / D`
[@airy1835; @bornwolf1999] sets the focused size, Beer-Lambert
`T = exp(-k * L)` [@beer1852] sets the atmospheric transmittance, the power
budget `P = S * (pi D^2 / 4) * T` sets the captured flux, and the dwell time
`t = F / I` deposits a material's vaporization fluence. Chaining these gives
`I = S * T * D^4 / (4 * 1.22^2 * lambda^2 * R^2)`; inverting it for `D` yields
the **minimum mirror diameter** that delivers a required irradiance at a given
range — the honest bound on the weapon's fantasy, and the reason the result
scales only as the fourth root of the demanded irradiance. The model assumes
the full captured power lands inside the first-null disk; the real Airy pattern
puts ≈83.8% inside it (see *Scope and Related Work*), pushing the same
direction as the other omissions, so the minimum diameter remains a lower
bound.

## Results — DIAMOND NET: measured outcomes, headline numbers, and what they establish

All results are computed at runtime from the frozen canonical datasets; the
prose below cites resolving variables rather than hand-authored numbers.

### Provenance chain

The canonical route tracks a diamond lot through 5
handoffs from mine to fence. 2 of those handoffs are
undocumented — the smuggling hops that make the lot conflict goods — giving a
documented coverage of 60%. The chain is therefore
conflict-free = **false**. The provenance figure marks each handoff as documented or a break point.

![Provenance chain: documented handoffs vs. break points](output/figures/diamonds_are_forever_provenance_chain.png)

### Smuggling corridor routing

Across a 10-corridor network moving a
5.0 M USD cargo, the stochastic-optimum route is
**sierra_leone -> nairobi -> paris -> amsterdam -> las_vegas** at an expected cost of 9.35 M USD,
carrying the cargo with survival 34% (seizure exposure
66%). The fewest-hops baseline in the same graph
(sierra_leone -> nairobi -> london -> amsterdam -> las_vegas) costs 11.15 M USD, so optimising
over expected cost rather than hop count cuts expected cost by
16%: at the same hop count, the optimum swaps the pricey
London-Amsterdam Channel ferry for the cheaper Paris leg. The two routes carry
almost the same seizure exposure — the saving is on transport cost, not on
seizure risk, which is why the survival probabilities barely differ. The smuggling figure plots the corridor expected costs with the optimum route
marked.

![Smuggling corridor expected costs (red = optimum route)](output/figures/diamonds_are_forever_smuggling_route.png)

**Cargo-value sensitivity is reported as measured, not asserted.** The
optimal route is cargo-dependent: at low cargo value the transport cost
dominates and cheap corridors win; as the cargo's value grows the seizure
probability dominates and a low-seizure, more-hop corridor wins instead.
The cargo figure plots the resulting ``route_reduction`` across a cargo
sweep. The curve is deliberately *not* monotone — measured it falls and then
rises as the optimum switches from the Paris leg to the New York leg — so no
single figure stands in for the dependency, and the canonical
5.0 M USD point is marked.

![Route reduction vs. cargo value (canonical 5.0 M USD marked)](output/figures/diamonds_are_forever_cargo_sweep.png)

### Lot forensics

Auditing 5 handoff samples of lot DF-71 by weight and
density surfaces **2 anomalies** and a
4-point audit score — a **flagrant** verdict. The
density probe catches the Amsterdam paste substitution (a measured density
outside the 3.40-3.65 g/cm3 window); the weight
ledger catches the final theft, a loss well beyond the
25% cutting allowance. The two rules are
independent — one physical, one accounting — so the verdict does not rest on a
single instrument. The lot figure shows the per-handoff weight deltas
against the cutting allowance.

![Lot weight reconciliation](output/figures/diamonds_are_forever_lot_forensics.png)

### Casino money movement

The strip network resolves to 7 casinos and
9 transfers moving 31.0 million US
dollars in aggregate. The network hub is the **whyte_house** operation.
Detection surfaces 3 distinct money cycles, and the
laundering closure — the share of flow that circulates — is
77%. The casino figure visualises the graph.

![Las Vegas casino money movement](output/figures/diamonds_are_forever_casino_network.png)

### Benford's-law ledger audit

The audit is reported as a matched pair, so that the anomalous verdict can be
attributed to something.

**Negative control.** The legitimate baseline alone —
80 transactions whose leading digits are the
Fibonacci leading digits, Benford-distributed by theorem rather than by
construction against the test — scores a chi-square of
**0.53**, far below the 15.507
critical value: a verdict of **conforms**. The screen does not
fire on clean books.

**Full ledger.** Adding the 61 round-figure
deposits takes the same statistic, computed by the same code path, to
**35.80** over 141 transactions — above
the df=8, alpha=0.05 critical value of
15.507, a verdict of **anomalous**. Because the
baseline passes on its own, the flag is attributable to the deposits and not
to the baseline.The benford figure plots all three distributions — baseline, full ledger,
Benford expectation — so the separation is visible. Digit 5
alone carries 55% of the statistic — the 5 x 10^n
structuring. The full ledger runs above the Benford expectation on exactly the
digits the deposits sit on (1, 2 and 5) and below it on every other digit.

This is a specificity check on two constructed fixtures, not a measurement of
detection accuracy: it shows the implemented test separates *these* halves. No
false-positive or false-negative rate is estimated here, and none should be
read off it.

![Casino ledger vs. Benford's law: legitimate baseline (negative control), full ledger, and the Benford expectation](output/figures/diamonds_are_forever_benford_ledger.png)

### Orbital-mirror targeting

At a geostationary post of 36000 km, the mirror surveys
3 threatened cities, of which 2
fall within the visible face: Las Vegas, Washington DC. The remaining target
(Beijing) is occulted by the Earth — no pointing solution
exists for it from this post, whatever the mirror's power. The orbital figure reports the slant range of each target, shaded by beam
visibility.

![Orbital-mirror slant range and visibility](output/figures/diamonds_are_forever_orbital_visibility.png)

### Beam delivery physics

The canonical scenario is a 40-m mirror working at
500 nm over a 36,998 km slant range, with
an atmospheric transmittance of 45%. At the resulting
0.56-m diffraction-limited spot it delivers
768,382 W/m$^2$ — a beam concentrated
565× over raw sunlight, which would still need
325 seconds of dwell to vaporize a steel layer. The
physics sets an honest bound on the weapon's fantasy: delivering
1 MW/m$^2$ at geostationary range requires a
42.7-m mirror. Because irradiance grows as the fourth
power of the diameter, that bound moves slowly — the mirror is the binding
constraint, and the dwell time is what a moving target denies. The beam figure shows delivered irradiance versus mirror diameter with the
requirement marked.

![Beam delivery vs. mirror size at GEO](output/figures/diamonds_are_forever_beam_physics.png)

### Mission outcome

The execute phase aggregates these seven lines into a single deterministic
outcome carrying a full provenance block (package version, seed, and a SHA-256
input fingerprint). The debrief distills the standing lessons: an undocumented
handoff is a provenance break; seizure risk rewrites the route; weight and
density tell the physical story; circular money movement and a failing
Benford test are the laundering signatures; and beam physics bounds the
orbital weapon.

## Conclusion — DIAMOND NET: findings, verdict, and what the mission establishes

The CONFLICT STONE mission demonstrates that a single deterministic package
can fuse disparate traces — a smuggling provenance chain, a risk-weighted
corridor route, a physical lot audit, a casino money-movement and Benford
audit, and an orbital weapon's targeting geometry and beam physics — into an
auditable, reproducible special-agent report.

The provenance analysis shows that even a majority-documented chain of custody
(60% coverage) retains flagrant break points that mark
the goods as illicit, while risk-weighted routing proves the smuggler can cut
expected route cost by 16% over the naïve route. Weight and
density forensics independently convict the lot (verdict
**flagrant**), the casino wash shows a laundering closure of
77%, and the ledger fails Benford's law
(chi-square 35.80 against a 15.507
critical value: **anomalous**). Finally, orbital physics grounds the
space-weapon threat in real beam geometry: only
2 of 3 targets are reachable at
all, because the mirror's reach is hard-bounded by Earth's curvature, and
delivering 1 MW/m2 at that range needs a
42.7-m aperture — the film's weapon is not impossible
so much as unaffordably large and slow.

By keeping the analytic cores pure and infrastructure-free, and by making the
mission adapter a thin declarative layer over the frozen BOND-API protocol, the
package guarantees that every claim in this manuscript is a live computation,
not a hand-stated fact. CONFLICT STONE is delivered as a verified, deterministic
mission that can be re-run end-to-end and audited from its input fingerprint
alone.

## Experimental Setup — DIAMOND NET: canonical scenarios, parameters, and configuration

All experiments are deterministic and use fixed canonical datasets seeded into
the pure domain core; there is no random number generation and no mock
framework.

**Mission configuration.** The package identity `diamonds_are_forever` runs
under codename `CONFLICT STONE`, version 0.1.0. Keywords
of the analysis: conflict diamonds, supply-chain provenance, risk-weighted routing, forensic gemology, money laundering, Benford's law, network analysis, orbital targeting geometry, beam delivery physics, deterministic mission software.

**Provenance dataset.** 5 ordered custody handoffs along
the mine-to-fence route; break points are flagged at build time.

**Smuggling dataset.** A 10-corridor directed network of
transport costs and seizure probabilities, carrying a cargo valued at
5.0 million US dollars. The least-risk route is computed
by a deterministic Dijkstra over expected cost; the baseline is a fewest-hops
BFS in the same network, which bounds the reduction metric below at zero.

**Forensic dataset.** 5 weight/density handoff samples for lot
DF-71, audited against a 25% per-handoff cutting
allowance and a 3.40-3.65 g/cm3 density window
(nominal 3.52), yielding a 4-point score.

**Casino dataset.** 7 casinos with 9
transfers totalling 31.0 million US dollars, and a
141-transaction ledger tested at df=8,
alpha=0.05 (critical value 15.507). The
ledger is a matched pair: a 80-transaction
legitimate baseline drawn from Fibonacci leading digits (Benford-conforming by
theorem — the negative control) plus 61
round-figure deposits. Each half is audited on its own as well as together.

**Orbital dataset.** 3 ground targets surveyed from a
geostationary post at 36000 km.

**Beam scenario.** A 40 m mirror at
500 nm over a 36,998 km slant range, with
atmospheric attenuation giving a transmittance of
45%; the strike requirement against which the minimum
mirror is solved is 1 MW/m2.

**Software environment.** Python 3.14.6, resolved at generation
time — the one token whose value is read from the machine rather than from a
committed input. The manuscript edition is stamped 2026-08-04, taken
from `paper.date` in `docs/manuscript/config.yaml`; no value in this manuscript comes
from the wall clock, so re-running hydration on the same interpreter rewrites
the same bytes.

## Reproducibility — DIAMOND NET: verification gates, deterministic regeneration, and artifacts

CONFLICT STONE is reproducible by construction.

- **Determinism.** Every metric is a pure function of a frozen canonical
 dataset. No random draws, no wall-clock dependence in any persisted artifact
 (the provenance block records `wall_time_s = 0`). Routing tie-breaks on an
 insertion counter; adjacency lists and casino names are sorted.
- **Provenance.** Every mission outcome carries a package version
 (0.1.0), a fixed seed, and a SHA-256 fingerprint of the exact
 canonical inputs — corridors, lot samples, the beam scenario, and the ledger
 included — so an outcome can be audited without re-running the mission.
- **Lineage.** Two end-to-end runs produce byte-identical debriefs, and two
 hydration runs write a byte-identical `output/manuscript/` tree and
 `manuscript_variables.json`; the test suite asserts both directly, running the
 generator twice across a whole-second boundary so a reintroduced clock would
 be caught. The manuscript edition is stamped from `paper.date` in
 `docs/manuscript/config.yaml`, never from the clock. The single token read from the
 machine rather than a committed input is `PYTHON_VERSION`, which is provenance
 of the interpreter: byte-identity is claimed for reruns on the same
 interpreter version.
- **Recomputation.** The resolved manuscript is generated by re-running
 `scripts/z_generate_manuscript_variables.py` under Python
 3.14.6; the tokens it emits (e.g. provenance coverage
 60%, laundering closure
 77%, the Benford verdict
 anomalous) are live computations, never hand-stated.
- **Zero mocks.** All tests exercise real computations over real data; the only
 "doubles" are the real canonical datasets themselves, and every dataset is
 chosen so its headline metric is non-trivial (anomalous, flagrant, positive
 reduction) rather than vacuous.

## Scope and Related Work — DIAMOND NET: boundaries, positioning, and relationship to the literature

### Scope

This package analyses the traces central to *Diamonds Are Forever*:
conflict-diamond provenance and corridor routing, physical lot forensics,
casino money movement and its Benford signature, and the orbital mirror's
targeting geometry and beam physics. It is **self-contained and illustrative**:
the canonical datasets are fixed, small, and embedded in the pure core. It is
not a claim about any real investigation, casino, or satellite system; it is a
deterministic, reproducible demo of the analytic methods, in the tradition of
special-agent mission models.

### Related work

- The provenance and forensic models generalise real supply-chain certification
 and diamond identification practice: the Kimberley Process formalises the
 "documented handoff" as the unit of traceability [@kimberley2003], early
 conflict-goods investigations documented the route and its gaps
 [@globalwitness1998], and the economics of mineral-driven conflict are
 quantified in [@berman2017]. Diamond density testing follows standard
 gemological identification [@webster1994].
- The corridor routing is a textbook shortest-path problem over expected cost;
 Dijkstra's algorithm [@dijkstra1959] bounds optimality over the same search
 space as the naive baseline. The cargo-value sensitivity is swept as data
 because the optimum is cargo-dependent (cheap corridors at low value,
 low-seizure corridors at high value), not monotone.
- The money-movement analysis draws on the laundering-detection literature
 [@levi2006]. Cycle detection is a *complete* elementary-circuit enumeration
 [@tarjan1973; @johnson1975] restricted to the small canonical graph, and the
 hub is a gross-flow reading of degree centrality [@freeman1978].
- The ledger audit rests on the leading-digit law observed by Newcomb
 [@newcomb1881] and rediscovered by Benford [@benford1938], scored with
 Pearson's chi-square criterion [@pearson1900]; its use as a fraud indicator
 follows forensic-accounting practice [@nigrini2012]. The test is a screen,
 not a proof: a failing ledger warrants investigation, it does not by itself
 establish laundering.
- The beam physics uses the Airy diffraction pattern [@airy1835] and the
 exponential absorption law [@beer1852], both as given in classical optics
 [@bornwolf1999]. It deliberately omits orbital mechanics, beam-riding
 control, adaptive optics, thermal blooming, and target material science
 beyond a single vaporization fluence, which are out of scope; the minimum
 mirror diameter is therefore a lower bound on the real requirement, not an
 estimate of it.

The package also documents its own platform: CONFLICT STONE (Diamonds Are Forever: CONFLICT STONE — Special-Agent Mission Software)
is one member of the PROJECT BOND suite, which shares the frozen BOND-API
mission protocol [@bondapi2026].

### Limitations and uncertainty

These are the honest bounds on what the package establishes, recorded so they
are not over-read:

- **Constructed fixtures, not empirical records.** The Benford result is a
 specificity check on two designed halves of one ledger — a Fibonacci-derived
 negative control and round-figure deposits — so it establishes that this
 implementation separates *these two halves*, not a false-positive or
 false-negative rate. No detection accuracy is claimed or measured.
 Equally, the canonical custody chain, casino network, and orbital targets
 are illustrative by design (see *Scope*); they are chosen so each headline
 metric is non-trivial rather than vacuous, not to sample any real corpus.
- **The substitution finding rests on a single instrument.** Lot forensics
 separates paste from diamond on density alone (a second gemological channel
 such as refractive index is a stated extension, not implemented), so the
 density verdict is one-instrument. The weight-vs-density finding is
 nonetheless two-signal because theft (weight) and substitution (density) are
 audited independently.
- **The beam model bounds the weapon in one direction only.** It omits orbital
 mechanics, beam-riding control, adaptive optics, thermal blooming, and
 material science beyond one vaporization fluence. It also assumes the *full*
 captured power lands inside the first-null disk; the real Airy pattern puts
 ≈83.8% of the power inside the first null, making the delivered irradiance
 ≈1.19× optimistic and the minimum diameter ≈4.6% small. Every omission —
 this one included — pushes toward a *larger* honest mirror, which is why the
 result is presented as a lower bound on the requirement, never as an
 estimate.
- **Determinism is not evidence of correctness.** The outputs are exact and
 reproducible by construction, but a deterministic, passing pipeline is only
 as good as the model that produced it; the same is true of the 100% line
 coverage figure, which measures execution, not truth. Where the model's shape
 is wrong, reproducing it faithfully only reproduces the error.
- **Cargo-value behaviour is reported as measured.** The `route_reduction`
 sweep is *not* monotone in cargo value (it falls and then rises as the
 optimum switches corridors); no monotone trend is claimed, and the sweep
 figure plots the measured curve with the canonical value marked.

## Sources — DIAMOND NET: bibliography

@friedman2026conflictstone; @bondapi2026; @globalwitness1998; @kimberley2003; @berman2017; @webster1994; @dijkstra1959; @levi2006; @benford1938; @bornwolf1999; @newcomb1881; @pearson1900; @nigrini2012; @tarjan1973; @freeman1978; @airy1835; @beer1852; @johnson1975


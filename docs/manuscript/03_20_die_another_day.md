# Die Another Day (2002) — ICARUS

*film package · package codename ICARUS*. Mission **ICARUS**: detect gene-therapy-grade identity replacement; plan ice-palace cold-environment operations; verify orbital-mirror (ICARUS) targeting geometry.

## Concepts — ICARUS: domain and operational focus

identity replacement, extreme-environment ops

## Abstract — ICARUS: mission summary

Die Another Day: ICARUS — Special-Agent Mission Software (mission codename **ICARUS**) is a special-agent mission-software package built for the BOND film suite. It implements 6 mission concepts as pure, deterministic algorithms: Biometric Identity-Replacement Detection, DNA Sequence Identity Verification, Ice-Palace Thermal Operations, Cold-Water Hypothermia Risk, Ice-Structure Integrity, Orbital Mirror Targeting. The identity layer screens an operative on two complementary signals. The biometric module enrols a Gaussian baseline and flags gene-therapy-grade trait drift via the Mahalanobis distance against a chi-square threshold: the replaced probe scores 41.42 against a 22.46 threshold while a fresh out-of-sample operative scores 10.97 and clears. The sequence module verifies a 1500-base DNA read by Levenshtein edit distance, k-mer fingerprint similarity, and contiguous edit-block detection; fingerprint similarity alone does not separate the probes, but a 12-base coherent substitution block does. The extreme-environment layer plans the ice-palace theatre: a 467.1-second Newton-cooling exposure ceiling covered by 4 rotating squads, a cold-water rescue that reaches the operative 1602.1 s before the severe stage in 10 C water, and an ice-structure check that passes its 1.17 load safety factor while failing its thermal-gradient case. The orbital-mirror module propagates an 7200-km circular orbit, solves the mirror reflection law, and finds 300 s of feasible targeting at a peak focused flux of 5.87 W/m^2. All results are deterministic: fixed seed, no wall-clock in persisted artifacts, and every metric in this manuscript is injected from the code — configured inputs from `docs/manuscript/config.yaml`, measured outputs from the same concept runner the mission provider itself executes — rather than being hand-authored.

## Introduction — ICARUS: mission framing, the operational problem, and how to read this chapter

Die Another Day: ICARUS — Special-Agent Mission Software is the PROJECT BOND film package for *Die Another Day*
(2002), mission codename **ICARUS** (version 0.1.0).
Six deterministic mission models: biometric and DNA identity-replacement screening, ice-palace thermal, immersion, and structural operations, and orbital-mirror targeting.

An ICARUS-class special agent operates across three theatres, each encoded in
6 dedicated, infrastructure-free domain modules under
`src/die_another_day/`:

1. `identity_detection.py` + `sequence_identity.py` — detect when an operative
 has been replaced by a gene-therapy-grade impostor, both at the biometric
 (marker-vector) level and at the DNA-sequence level;
2. `ice_ops.py` + `hypothermia.py` + `ice_structure.py` — plan operations in
 the extreme cold of an ice palace: air-exposure ceilings and rotation,
 cold-water immersion/rescue risk, and the structural integrity of the ice
 itself;
3. `orbital_mirror.py` — aim an orbiting solar mirror at a ground target,
 solving the line-of-sight and reflection geometry.

Two further modules complete the package without adding domain science.
`mission_results.py` is the single deterministic runner: it reads the
configuration, executes all 6 models once under seed
7, and returns one frozen record. `mission.py` is a thin adapter
that turns that record into the frozen BOND-API `MissionProvider` contract, so
the orchestrator can discover and run the film by slug on `sys.path`. The pure
domain modules remain importable without `bond_api`; only the adapter couples
the two layers.

That structure is what lets this manuscript state measured numbers safely: the
results in §03 and the mission's own `MissionOutcome` are formatted from the
same record, so there is no second code path along which they could drift.

The remainder of this manuscript documents the methodology (§02), results
(§03), scope and limitations (§07), experimental setup (§05), and
reproducibility guarantees (§06) of the package.

## Methodology — ICARUS: the analytical models and algorithms that drive the mission

The mission's concepts rest on a set of mathematical cores, each pure and
deterministic. All 6 of them (identity_detection, sequence_identity, ice_ops, hypothermia, ice_structure, orbital_mirror) are driven
from one place, `mission_results.run_all_concepts`, described in §*Execution
and control structure* below.

### Positive and negative controls

Each identity model is exercised with a matched pair, not a single case. The
positive control is a constructed replacement; the negative control is a
genuine subject. The negative control is chosen so that clearing the screen is
a measurement rather than an identity: for the biometric model it is a fresh
out-of-sample draw from the enrolled population (which carries real, non-zero
drift), not the profile mean (which would score exactly zero by construction).
For the sequence model it is a read carrying scattered single-base sequencing
noise, so the discriminating power of the contiguous-block rule is what is
actually being tested.

### Biometric identity-replacement detection (`identity_detection.py`)

A biometric profile is modelled as a Gaussian over $k$ markers
($k = $ 6). From an enrolled sample population we estimate
the mean $\boldsymbol{\mu}$, the covariance $\Sigma$, and its inverse
$\Sigma^{-1}$. A probe $\boldsymbol{x}$ is scored by the squared Mahalanobis
distance $D^2 = (\boldsymbol{x}-\boldsymbol{\mu})^\top \Sigma^{-1}(\boldsymbol{x}-\boldsymbol{\mu})$,
which under the Gaussian assumption is $\chi^2$ with $k$ degrees of freedom.
The verdict compares the tail probability against a size $\alpha = $
0.001, and additionally requires at least 2
markers with standardized deviation $|z_i| > $ 3 — the
coherent, multi-marker signature of gene-therapy-grade trait drift.

### DNA sequence identity verification (`sequence_identity.py`)

Identity is also checked at the sequence level over the {A,C,G,T} alphabet. A
1500-base reference genome is enrolled, and a probe is scored
three ways:

* `hamming_distance` — per-base substitutions;
* `edit_distance` — the Levenshtein edit distance (insertions, deletions,
 substitutions) via O(mn) dynamic programming;
* `kmer_jaccard` — Jaccard similarity of the probe's k-mer fingerprints
 (k = 9), robust to isolated single-base noise.

A probe is a suspected replacement when it carries a *contiguous* run of at
least 12 mismatching bases (`mismatch_clusters`) — a coherent
gene-therapy edit rewrites a block of loci at once, whereas sequencing noise
produces only scattered single-base errors. It is *matched* only when its
k-mer similarity clears 0.9 AND no such block is present.

### Ice-palace air operations (`ice_ops.py`)

An operative's core temperature decays toward the ambient environment by
Newton's law of cooling, $T(t) = T_e + (T_0 - T_e)e^{-kt}$, giving a closed-form
safe exposure $t_{\text{crit}} = \frac{1}{k}\ln\frac{T_0 - T_e}{T_{\text{crit}} - T_e}$.
With ambient $T_e = $ -34 C, the planner partitions an
1800-second operation into rotating squads of
4 operatives so no squad exceeds the ceiling.

Two further quantities size the resource, and they use *different* references
on purpose. Cold strain is
$\int_0^{E}\max(0,\, T_0 - T(t))\,\mathrm{d}t$ in degree-seconds, referenced to
normothermia ($T_0 =$ 37 C) — referencing it to room comfort
(20 C) would return exactly zero for every survivable shift, since a shift ends
at the 30 C critical core temperature, well above comfort,
and the metric could then never discriminate one plan from another. Space
heating, by contrast, genuinely is comfort-referenced: it is the conductance
times the room-to-ambient deficit times the operation duration.

### Cold-water hypothermia risk (`hypothermia.py`)

Water conducts heat far faster than air, so an immersed operative follows the
same Newton cooling law with a much larger decay rate, scaled by body mass and
insulation. The core temperature then crosses the standard clinical stages:
mild hypothermia at 35 C, moderate at 32 C, and severe (unconsciousness) at
28 C. `plan_cold_water_rescue` computes whether a rescue party sweeping
400 m at 2 m/s can reach the operative
before the core reaches the severe stage, reporting the margin and the core
temperature at reach (immersion in 10 C water, 75
kg operative, insulation factor 0.9).

The reference decay rate `K_REF_PER_S` is a *scenario* constant, not a
physiological calibration. It is fixed so that a 75 kg operative in
10 C water reaches a 30 C core in 20 minutes — an initial
cooling rate near 24 C/hour, which is roughly an order of magnitude faster than
measured immersion cooling in water at this temperature. Every hypothermia
number in §03 is therefore internally consistent with that constant and should
not be read as a survival-time prediction; see §07.

### Ice-structure integrity (`ice_structure.py`)

The ice palace must carry its load and survive thermal gradients. Load capacity
follows the standard ice-engineering rule $P = h^2 / C$ (P tons, h cm); the
thermal gradient stress is $\sigma = E\,\alpha\,\Delta T / (1-\nu)$, and the
critical temperature difference that drives ice to its tensile limit is
$\Delta T_{\text{crit}} = \sigma_{\text{allow}}(1-\nu)/(E\alpha)$. At the
configured thickness (30 cm), load
(3 t), and gradient (15 C, tensile strength
1.5 MPa), the plan reports the safety factor and whether
the gradient risks cracking.

### Orbital-mirror targeting (`orbital_mirror.py`)

The mirror is placed on a circular orbit (semi-major axis 7200 km,
inclination 65 deg) and propagated by its mean anomaly.
The ground target (60 N, 15 E) is
located in the same inertial frame via Greenwich mean sidereal time. At each
instant the mirror normal $\hat{n}$ satisfies the reflection law -- it bisects
the incoming solar ray $\hat{s}$ and the ground re-point $\hat{r}$:
$\hat{n} \propto \hat{s} + \hat{r}$, so the incidence angle
$\arccos(\hat{n}\cdot\hat{s})$ is exactly half the Sun-mirror-target angle.

The incoming ray uses the *parallel-ray* approximation: at 1 au the Sun's
direction from the mirror is the solar unit vector itself, and the ~7e6 m orbit
radius shifts it by well under an arcsecond. Forming that ray by subtracting
the satellite position from a unit solar vector would instead yield the nadir
direction, and the resulting incidence angle would be wrong by tens of degrees;
`tests/test_orbital_mirror.py` pins the incidence angle to the analytic
half-angle to keep that failure mode from returning.

When the target direction is anti-parallel to the solar ray the bisector
degenerates — no orientation folds a 180-degree turn — and the instant is
reported infeasible with zero delivered power rather than raising. Targeting is
otherwise feasible when the mirror is sunlit (outside Earth's cylindrical
shadow) and above the 10-degree horizon. Delivered
power is the solar constant times mirror area (10000 m^2) times
reflectivity (0.9) times the cosine of incidence times a
lumped one-way transmission factor (0.85) that
stands in for atmospheric attenuation, figure error, and scattering — it is a
configured constant, not a modelled quantity, and it scales every reported
flux. Flux at the target follows from the beam spread, whose half-angle is the
configured 0.02 deg plus the mirror's own apparent
angular radius at range.

### Execution and control structure

The six models are not invoked ad hoc. `mission_results.run_all_concepts` reads
the `concepts:` block of `docs/manuscript/config.yaml`, runs every model once under
seed 7, and returns a frozen `ConceptResults` record. Two
consumers read that record and only that record: `mission.py`, which serialises
it into the frozen BOND-API `MissionOutcome`, and `manuscript_variables.py`,
which formats it into the measured manuscript tokens this paper cites. A number
printed here is therefore the same value the mission reported, not a
transcription of it.

## Results — ICARUS: measured outcomes, headline numbers, and what they establish

Running the deterministic mission (`uv run python scripts/run_mission.py`)
exercises all 6 concepts under seed 7 and reports
measured outcomes. Every number below is produced by
`src/die_another_day/mission_results.py` — the same entry point the
`MissionProvider` uses for its `MissionOutcome` — and injected as a manuscript
token, so the paper and the code cannot disagree.

### Identity-replacement detection (biometric)

Two probes are scored against the enrolled Gaussian baseline: a positive
control (a coherent 4.5-sigma shift on the first
2 markers, the remaining markers left at the population
mean, plus small noise) and a negative control (a fresh out-of-sample operative
drawn from the same enrolled population). The shift magnitude is
4.5 sigma, deliberately clear of — and not equal to —
the 3-sigma per-marker flagging threshold it must
cross.

| Probe | Mahalanobis $D^2$ | $\chi^2$ threshold | markers flagged | verdict |
| --- | --- | --- | --- | --- |
| replaced (positive control) | 41.42 | 22.46 | 2 | replacement |
| genuine (negative control) | 10.97 | 22.46 | 0 | cleared |

The replaced probe scores 41.42 against a threshold of
22.46 at $\alpha =$ 0.001 on
6 degrees of freedom, with 2
individually flagged markers — both conditions of the gene-therapy-grade-mahalanobis rule. The
genuine draw scores 10.97 ($p =$ 0.089) with
0 flagged markers and is cleared. The negative control is
deliberately not the profile mean, which would score exactly zero and make
clearance true by construction rather than measured.

![Per-marker standardized trait drift for the two probes that produced the
verdicts in the table above — the out-of-sample genuine draw and the
4.5-sigma replaced probe — plotted from the same
`ConceptResults` record. The dashed lines mark the
$\pm$3 flagging
threshold.](output/figures/die_another_day_icarus_identity_drift.png)

### Identity-replacement detection (sequence)

The 1500-base reference genome is probed with a genuine read
carrying 5 scattered single-base errors and with a
replaced read carrying an *independent* draw of 5
scattered errors plus a coherent 12-base substitution block.
The two reads are matched on the number of scattered errors, not on their
positions: the block consumes RNG draws before the scattered positions and
removes its own loci from the available pool, so the scattered sets differ.
What separates the probes is therefore the block alone, which is exactly the
control the contiguous-run rule is being tested against.

| Probe | 9-mer Jaccard | Hamming | edit distance | longest contiguous block | verdict |
| --- | --- | --- | --- | --- | --- |
| genuine | 0.9413 | 5 | 5 | 1 | matched |
| replaced | 0.9182 | 17 | 15 | 12 | replacement suspected |

Hamming and edit distance are separate statistics and are reported separately:
they coincide for the genuine read but not for the replaced one, where the
contiguous block admits a cheaper alignment (17 versus
15).

Fingerprint similarity alone does not separate the two probes — both clear the
0.9 match threshold, at 0.9413 and
0.9182 respectively. The discriminating statistic is
the 12-base contiguous mismatch run, which scattered
sequencing noise does not produce; this is what the levenshtein-kmer-cluster rule keys on.

![DNA mismatch map for the replaced probe: the contiguous edit cluster is
shaded against isolated single-base errors.](output/figures/die_another_day_icarus_sequence_mismatch.png)

### Ice-palace operations

From the configured physics (ambient -34 C, core
37 C, critical 30 C, decay
0.8 /hour) the closed-form exposure ceiling is
467.1 s. The 1800-second operation is
therefore split across 4 rotating squads drawn from the
4 available operatives, giving a 450.0-second
shift — inside the ceiling, so the roster is feasible (yes).
Each shift accrues
1545.6 degree-seconds of core depression below
normothermia, and holding the interior at comfort against the ambient costs
145.8 MJ over the operation.

### Cold-water hypothermia risk

In 10 C water a 75 kg operative reaches the
severe (28 C) stage after 1802.1 s.
A rescue sweeping 400 m at 2 m/s arrives
at 200.0 s — a margin of 1602.1 s. Core temperature at
reach is 35.81 C, clinical stage *normal*
against the mild/moderate/severe bands at 35,
32, and 28 C.

![Cold-water immersion core-temperature decay with mild/moderate/severe stage
thresholds.](output/figures/die_another_day_icarus_hypothermia_curve.png)

### Ice-structure integrity

The palace ice at 30 cm carries 3.52 t
against the applied 3 t — a safety factor of
1.17. The load case therefore passes. The thermal case does
not: a 15 C gradient drives 10.28 MPa
of tensile stress, far past the 1.5 MPa strength, whose
critical gradient is only 2.19 C. Cracking risk:
**yes**. The structure holds its load and still fails its
thermal case — the two checks are independent, and the combined verdict
requires both.

### Orbital-mirror targeting

Propagating the 7200-km circular orbit at
65 deg inclination over an 3000-second
window sampled every 60 s yields 51 instants
over the 60 N, 15 E target. Of
these, 5 are feasible — mirror sunlit and above the
10-degree horizon — for 300 s of
targeting. Peak focused flux is 5.87 W/m^2 at
1680 s after epoch. That delivered flux is small next to the
solar constant: a 10000 m^2 mirror at orbital range spreads its
beam over a footprint kilometres across, so at this scale the model describes
an illumination instrument rather than the film's weapon.

![ICARUS orbital-mirror elevation vs. time over the ground target. The shaded
band marks the feasible targeting window and the red point the peak-flux
instant.](output/figures/die_another_day_icarus_pass_profile.png)

## Conclusion — ICARUS: findings, verdict, and what the mission establishes

Die Another Day: ICARUS — Special-Agent Mission Software demonstrates that a special-agent mission can be encoded as
6 independent, deterministic computational cores united by a thin
protocol adapter. Identity is screened both at the biometric and DNA-sequence
level, so a gene-therapy-grade replacement is caught by a coherent marker drift
(41.42 against a 22.46 threshold) *and* by a
12-base contiguous genome edit block. The extreme-environment
layer turns a cold-exposure physics law into an executable roster
(4 squads under a 467.1-second ceiling), sizes a
cold-water rescue against the hypothermia timeline (1602.1 s of
margin), and checks the ice palace's structural integrity under load and
thermal stress. The orbital-mirror module solves the reflection-and-line-of-sight
geometry of targeting a ground point from orbit, yielding
300 s of feasible pointing in the configured window.

Two results are worth stating plainly because they are negative. The ice palace
passes its load case and still fails its thermal case, so a single "structurally
safe" verdict would have hidden a real failure mode. And the delivered flux of
5.87 W/m^2 shows the orbital mirror at this aperture is an
illumination instrument, not the film's weapon — the model reports what the
geometry actually permits rather than what the plot requires.

The package meets the BOND guardrails: pure domain cores importable without the
protocol, a frozen `MissionProvider` adapter, a zero-mock test suite held to a
line-and-branch coverage floor by `pytest --cov-fail-under`, and a manuscript
whose every metric — configured input and measured output alike — is injected
from the code through the 6 concept modules.

## Experimental Setup — ICARUS: canonical scenarios, parameters, and configuration

All mission parameters are declared once in `docs/manuscript/config.yaml` under the
`concepts:` block and consumed by the code via
`src/die_another_day/mission_results.py`. They are reproduced here as mission
tokens so the manuscript cannot drift from the configuration. Package identity:
`die_another_day` (codename ICARUS), deterministic seed
7.

The seed is the single module constant `mission_results.MISSION_SEED`, not a
configuration key: `config.yaml` carries no seed of its own, so no consumer can
be reading a different one from the run this paper reports.

The list below is complete by construction rather than by inspection. Every
`concepts.<section>.<key>` in `docs/manuscript/config.yaml` is registered in
`manuscript_variables.CONFIG_INPUT_TOKENS`, and
`test_every_configured_input_is_registered_and_cited` fails if the registry and
the file disagree, or if a registered token is not cited in this section.

### Identity detection

- Biomarker markers: 6
- Test size $\alpha$: 0.001
- Per-marker $z$ threshold: 3
- Minimum flagged markers: 2

### DNA sequence identity

- Genome length: 1500 bases
- k-mer size: 9
- Match Jaccard threshold: 0.9
- Edit-cluster minimum: 12 bases
- Scattered single-base errors per read: 5

### Ice-palace operations

- Ambient temperature: -34 C
- Body/core temperature: 37 C
- Critical (minimum safe) core temperature: 30 C
- Cooling decay rate: 0.8 /hour
- Operatives available: 4
- Operation duration: 1800 s
- Envelope thermal conductance: 1500 W/K

### Cold-water hypothermia risk

- Water temperature: 10 C
- Operative mass: 75 kg
- Insulation factor: 0.9
- Rescue distance: 400 m
- Sweep speed: 2 m/s

### Ice-structure integrity

- Ice thickness: 30 cm
- Applied load: 3 t
- Thermal gradient: 15 C
- Tensile strength: 1.5 MPa

### Orbital-mirror targeting

- Orbit semi-major axis: 7200 km
- Orbit inclination: 65 deg
- Right ascension of the ascending node: 0 deg
- Mean anomaly at epoch: 320 deg
- Epoch (Julian date): 2461300.5
- Ground target: 60 N, 15 E
- Pass window: 3000 s sampled every 60 s
 (51 instants)
- Mirror area: 10000 m^2
- Mirror reflectivity: 0.9
- Beam half-angle: 0.02 deg
- Lumped one-way transmission factor: 0.85
- Minimum targeting elevation: 10 deg

The epoch, RAAN, and mean anomaly are not incidental: together with the
inclination they select *which* pass the 3000-second window
lands on, and hence every number in §03's orbital-mirror row. They were chosen
so that a pass occurs over the target inside the window — a hand-tuned
geometry, stated here rather than buried in a default.

### Software environment

- Python: 3.14.6
- Concept modules (6): identity_detection, sequence_identity, ice_ops, hypothermia, ice_structure, orbital_mirror
- Package version: 0.1.0 (`docs/manuscript/config.yaml`, `paper.version`)

There is deliberately no generation timestamp in this list. An earlier draft
hydrated one from the wall clock, which made every regeneration of the
manuscript differ in bytes while §00 and §06 claimed determinism; §06 states the
property that replaced it, and a test enforces it.

### What is configured versus what is measured

The lists above are *inputs*: every one is a literal in
`docs/manuscript/config.yaml`. Everything in §03 is an *output*: it comes from
running the models on these inputs. The two families are formatted by different
code paths (`generate_variables` for inputs, `measured_variables` for outputs)
and a test asserts that each measured token equals the value the concept runner
produced.

That test binds provenance, not independence: it proves a §03 number came out
of the runner, not that the runner had any freedom in producing it. Three
tokens are worth naming because they are *structurally determined* by inputs
and would look like findings otherwise:

- `SEQ_GENUINE_HAMMING` equals `scattered_errors` whenever the mutation
 generator behaves — it applies exactly that many substitutions at distinct
 loci, each guaranteed to change the base. Read it as a check on the
 generator, not as a measurement of sequencing noise.
- `SEQ_LONGEST_BLOCK` is bounded below by `cluster_min` for the same reason;
 it can only exceed it if a scattered error happens to abut the block. The
 informative comparison is against `SEQ_GENUINE_LONGEST_RUN`, which is free to
 be anything and is what makes the separation a result.
- `ID_REPLACED_SHIFT_SIGMA` is a construction parameter of the positive
 control (`REPLACEMENT_SHIFT_FACTOR` times the configured threshold), reported
 so §03 states the probe's actual magnitude instead of reusing the threshold
 token.

Everything else in §03 — every score, verdict, time, flux, and safety factor —
is free to move with the inputs, and
`test_measured_tokens_track_the_configuration` demonstrates that it does.

## Reproducibility — ICARUS: verification gates, deterministic regeneration, and artifacts

The package is deterministic by construction:

- **Fixed seed**: all synthetic data (the enrolled biometric population and the
 reference genome) is drawn with seed 7, so the mission outcome
 is reproducible across runs
 (`src/die_another_day/mission_results.py`). The seed is a single module
 constant; `docs/manuscript/config.yaml` deliberately carries no seed key, and a
 test fails if one reappears, so no consumer can quietly run a different one.
 A test re-runs the concept runner
 and compares the whole `ConceptResults` record; a second test changes the
 seed and asserts the stochastic outputs move while the pure-physics ones do
 not, so the seed is demonstrably load-bearing rather than decorative.
- **No wall-clock in artifacts**: provenance records a `wall_time_s` of `0.0`,
 and nothing written under `output/` is read from a clock. This was not always
 true: a `GENERATION_TIMESTAMP` token was hydrated from `datetime.now` and
 rendered into §05, so every regeneration produced different bytes while this
 section claimed determinism. The token is gone.
- **Byte-identical regeneration**: re-running
 `scripts/z_generate_manuscript_variables.py` overwrites
 `output/data/manuscript_variables.json` and `output/manuscript/*.md` with
 bytes identical to the previous run's.
 `test_regeneration_is_byte_identical` runs the script twice, more than one
 second apart, and compares every produced file byte-for-byte. The gap is
 deliberate: a second-resolution timestamp only differs across runs that
 straddle a second boundary, so without it the gate's ability to see such a
 stamp would depend on how long a subprocess happens to take. The claim covers
 exactly the files that script writes; figures are covered by the separate
 gate below. The one environment-derived token,
 `3.14.6`, is an interpreter identity rather than a clock and is
 constant across runs on one interpreter — on a different Python it changes,
 so the property is stated per-interpreter, not across machines.
- **Byte-reproducible figures**: the figure saver suppresses matplotlib's PNG
 `Date` metadata chunk, and `tests/test_figures.py` renders each figure twice
 and compares the bytes.
- **Figures depict the reported run**: `scripts/generate_figures.py` plots
 straight off the `ConceptResults` record rather than rebuilding its own
 probes, and `test_published_figures_depict_the_reported_run` compares the
 published PNG bytes against an independent render of the runner's arrays.
 Each renderer additionally has an input-sensitivity test — change one
 argument, require different bytes — so a plot cannot silently ignore what it
 is given. Both gates exist because an earlier identity-drift figure showed a
 different experiment than the table beneath it.
- **Configured-input completeness**: every `concepts:` key is declared once in
 `manuscript_variables.CONFIG_INPUT_TOKENS`, and
 `test_every_configured_input_is_registered_and_cited` fails if the registry
 and `config.yaml` disagree or if a registered input is missing from §05.
- **Zero mocks**: `tests/` uses real computation and real data only — no
 `unittest.mock`, `MagicMock`, or `mocker.patch` anywhere in the suite.
- **Coverage gate**: `uv run pytest tests/ --cov=src --cov-fail-under=90`
 fails the run below the line-and-branch floor. The measured figure is not
 quoted here; run the command to obtain the current number.
- **Type and style gates**: `uv run ruff check src/ scripts/`,
 `uv run ruff format --check src/ scripts/`, and `uv run mypy src/` are clean.
- **Token hygiene**: two live gates in `tests/test_manuscript_variables.py` —
 every mission token cited in `docs/manuscript/[0-9]*.md` must be produced by
 `generate_variables`, and every token `generate_variables` produces must
 be cited by some section (no orphan tokens). Strict generation additionally
 fails on any unresolved token left in a rendered section.
- **Thin-orchestrator gate**: `tests/test_scripts_smoke.py` parses every script
 in `scripts/` and fails if one grows a second top-level function, a class, or
 a direct numpy/scipy/matplotlib import — the mechanical form of the
 layer contract.

Python version: 3.14.6.

## Scope and Related Work — ICARUS: boundaries, positioning, and relationship to the literature

**Scope.** This package models three decision problems relevant to a
special-agent operation — identity-replacement screening, cold-environment
exposure planning, and orbital-mirror targeting. Each model is deliberately
self-contained and deterministic; it is not a general biometrics, heat-transfer,
or astrodynamics library. Assumptions are stated explicitly in §02 (Gaussian
markers, Newton cooling, circular Keplerian orbit, low-precision solar
ephemeris).

**Related work.** The Mahalanobis-distance screen (Mahalanobis, 1936) is a
classic multivariate outlier tool; here it is specialized to a coherent-marker
replacement hypothesis with a chi-square calibration. Sequence comparison uses
Levenshtein edit distance (Levenshtein, 1966) together with k-mer set
similarity, the fingerprinting idea that underpins alignment-free genome
comparison (Ondov et al., 2016). Newton's law of cooling (Newton, 1701)
underlies standard cold-stress exposure limits. The immersion module borrows
the *clinical staging* used in the cold-water survival literature (Tipton,
1989; Golden and Tipton, 2002) — the mild/moderate/severe core-temperature
bands — but **not** its cooling rates: `K_REF_PER_S` is a scenario constant,
not a calibration against that literature (see Limitations). Ice load capacity
uses the published bearing-capacity rule for floating
ice covers (Gold, 1971; Sodhi, 1995) with mechanical and thermal constants from
ice physics (Hobbs, 1974). Orbital-targeting geometry follows standard two-body
propagation (Battin, 1999; Vallado, 2013) and the mirror reflection law used by
space-solar-power and orbital-reflector studies (Glaser, 1968). The
contribution here is not any single model but their *integration* into one
deterministic mission provider under the frozen BOND-API contract, with every
reported number injected from the run rather than transcribed.

**Limitations.** These are properties of the models, not of the
implementation, and each is visible in the code:

- Biomarker distribution is assumed Gaussian and markers are drawn
 independently; heavy-tailed or correlated traits would need robust covariance
 estimation, and the chi-square calibration would shift accordingly.
- Sequence verification requires equal-length reads. Edit distance tolerates
 indels, but the contiguous-block rule and the Hamming statistic are
 position-aligned, so an unaligned read must be aligned first.
- The orbital pass is a single circular orbit with a low-precision solar
 ephemeris and a cylindrical (not conical) shadow model; it answers a
 feasibility question, not a constellation-design or pointing-error one.
- Beam spread is a simple angular model: the half-angle is a configured
 constant plus the mirror's apparent angular radius. Diffraction, figure
 error, and atmospheric scattering are folded into one lumped transmission
 factor rather than modelled.
- Cold-exposure planning uses a single Newton decay rate for all operatives
 (no per-suit or per-individual variation), and the rotation planner assumes
 squads can hand over instantaneously.
- **The immersion cooling rate is not physiologically calibrated.**
 `hypothermia.K_REF_PER_S` is fixed so a 75 kg operative in 10 C water reaches
 a 30 C core in 20 minutes: an initial cooling rate of about 24 C/hour, which
 is roughly an order of magnitude faster than measured immersion cooling at
 that water temperature. It is a film-scenario constant chosen to put the
 rescue on a dramatic clock. Consequently §03's immersion times
 (`HYP_TIME_TO_SEVERE_S`, `HYP_CORE_AT_REACH_C`, `HYP_MARGIN_S`) are correct
 *for this model* and are not survival-time predictions; the module
 demonstrates the rescue-versus-timeline decision structure, not the timeline
 itself. Only the clinical staging thresholds (35 / 32 / 28 C) are taken from
 the literature. `test_hypothermia.py` pins the constant to its stated
 20-minute definition so the number and the sentence cannot drift apart.
- The ice-structure model is a static bearing-capacity plus thermal-stress
 check; it does not model creep, crack propagation, or repeated loading.

## Sources — ICARUS: bibliography

@mahalanobis1936; @levenshtein1966; @gold1971; @sodhi1995; @hobbs1974; @tipton1989; @golden2002; @newton1701; @battin1999; @glaser1968; @ondov2016; @vallado2013


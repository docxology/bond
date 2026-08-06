# GoldenEye (1995) — ARKANGEL

*film package · mission codename ARKANGEL*. Mission **ARKANGEL**: model the orbital EMP threat envelope and the orbital platform geometry; assess electronics kill radii by vulnerability class; assess EM coupling and shielding on sensitive infrastructure; assess regional power-network resilience to the strike; evaluate Arkangel dam-facility security and breach-flood hydrograph.

This chapter reproduces the package's complete manuscript verbatim:
the abstract and every authored section, token-hydrated from the
package's own manuscript variables, with the package's figures carried
in the combined PDF and its sources resolved against the unified
bibliography.

## Concepts

orbital EMP, infrastructure resilience

## Abstract

**GoldenEye: ARKANGEL** (film identity **GOLDENEYE**, mission codename **ARKANGEL**) is a deterministic special-agent mission software package that models the coupled threat surfaces from the 1995 film *GoldenEye*: an orbital electromagnetic-pulse (EMP) weapon and its orbital-platform delivery, the electronics kill-radius it imposes on surface assets, the coupling and shielding of sensitive infrastructure, the resilience of the regional power network, and the security and breach-flood risk of the Arkangel dam facility. The threat envelope is a documented conservative point-source model of a high-altitude nuclear burst (**2000.0** kt at **300.0** km), producing a nadir early-time field of **90125** V/m across a line-of-sight footprint of radius **1978** km (**12291795** km^2). Four electronics vulnerability classes (**4** in total: **unprotected, commercial, military, legacy_tube**) are assessed: unprotected microelectronics are destroyed over essentially the entire visible footprint (**1978.0** km, **100.0**\% of it), while MIL-STD-188-125-hardened and legacy vacuum-tube electronics require ever-higher fields and survive to within **268.7** km of the burst or are immune (**0.0** km). For the Arkangel dam, the report combines the published Froehlich (1995) breach-outflow regression with the Ritter (1892) instantaneous dam-break solution. Given a reservoir of **130000000** m^3 behind a **75.0** m head, peak outflow reaches **31760** m^3/s with a wave front moving at **54.2** m/s; the facility **8.0** km downstream faces a **33.3** m peak inundation within **2.5** min — an overall **extreme** risk. Defense-in-depth access control yields a **0.987** detection probability and a **89.3** composite security score. Beyond the envelope, the package deepens the model. The weapon rides a circular orbital platform (period **90.4** min, speed **7.7** km/s) that sees the target at a **18.8**-degree elevation over **797.7** km of slant range, with a **5.0**-minute usable pass. At the facility the envelope field of **10617** V/m couples **34218** V onto a **3.2** m effective antenna, yet a **0.008** mm-penetration aluminium enclosure provides **192.3** dB of shielding and reduces the penetrated field to **0.00** V/m. The regional power grid (**5** nodes, **6** lines) loses the nodes **town_a, relay** and serves only **28.4**\% of critical load; the mission-critical facility retains a **0.402** survival probability over **3** redundant paths. A breach hydrograph (average width **164.7** m, duration **136.4** min) sweeps all **3** monitored stations, the farthest **20.0** km downstream arriving in **6.1** min. All results are closed-form, deterministic, and regenerable from source; figures, data, and manuscript variables are produced by thin orchestration scripts under `scripts/`.

## Introduction

**GoldenEye: ARKANGEL — Special-Agent Mission Software** (**Orbital EMP effects, electronics kill radius, EM coupling and shielding, power-network resilience, and Arkangel dam-facility security**) is a BOND-suite film package for *GoldenEye*
(1995), the film in which a captured space-based weapon — a
**2000.0** kt nuclear device detonated at
**300.0** km altitude — demonstrates the catastrophic coupling
between an electromagnetic pulse and the electronics of an entire region. The
package re-casts that event as a rigorous, deterministic engineering analysis:
the orbital platform that carries the weapon, the field it lays down, how that
field couples into and past infrastructure shielding, and what the regional
power network retains afterwards. It then extends the analysis to the second
mission-critical system from the same film — the Arkangel dam facility, whose
defensive layers, catastrophic-failure flood risk, and downstream breach
hydrograph are modelled explicitly.

### Reader's guide

The package is organised around a clean separation of concerns:

- **Pure domain core** — seven infrastructure-free, closed-form modules:
 `emp_model.py` (the burst-to-ground E1 envelope and the E1/E2/E3 waveform),
 `orbital_mechanics.py` (the Keplerian delivery platform and its pass
 geometry), `kill_radius.py` (per-vulnerability-class kill radii),
 `coupling.py` (skin depth, Schelkunoff shielding, conductor coupling),
 `grid_resilience.py` (per-asset survival, most-reliable routing, edge-disjoint
 redundancy), `dam_security.py` (defense-in-depth access control and
 breach-flood risk), and `breach_hydrograph.py` (breach width, the
 volume-conserving outflow hydrograph, and the downstream station table).
 All seven can be imported in any Python environment with no BOND layer
 present.
- **Scenario composition** — `src/goldeneye/scenario.py` binds the seven models
 into the canonical ARKANGEL scenario and exposes the deterministic analysis
 dictionary and a canonical input hash.
- **Protocol adapter** — `src/goldeneye/mission.py` implements the frozen
 `bond_api.MissionProvider` contract (brief/recon/plan/execute/debrief) and
 registers the mission's analytical gadgets with the `bond_api.GadgetRegistry`.
- **Thin orchestrators** — `scripts/` expose the five mission phases plus a
 manuscript-variable hydrator. Business logic never lives in a script.

This design keeps the mathematical core testable in isolation (a per-module
suite with no mocks, ≥90% line-and-branch coverage) while leaving the BOND
protocol integration as a thin, inspectable adapter — the pattern used by every
film package in the suite.

### What this manuscript covers

`02_methodology.md` states the physics and the closed-form models.
`03_results.md` reports the ARKANGEL run. `04_conclusion.md` summarises the
deliverable. `05_experimental_setup.md` and `06_reproducibility.md` document
the scenario parameters, environment, and regeneration contract.
`07_scope_and_related_work.md` delimits the model's assumptions and situates it
in the HEMP-damage and dam-break literature.

## Methodology

### Orbital EMP weapon model (`src/goldeneye/emp_model.py`)

A high-altitude nuclear burst (HEMP) releases a prompt gamma flux; the gammas
Compton-scatter in the atmosphere, driving a radial electron current that
radiates the early-time (E1) electromagnetic pulse. We model the ground-level
E1 peak field as a documented conservative point-source envelope:

$$E(r) = E_0 \, Y_s \, \left(\frac{h}{d}\right)^2 \exp\!\left(-\frac{d-h}{\lambda(h)}\right),$$

where $h$ is the burst altitude, $d = \sqrt{h^2 + r^2}$ the slant range to a
ground point at horizontal range $r$, $Y_s = (Y/Y_\text{ref})^{p}$ the
empirical yield scaling, and $\lambda(h)$ the effective gamma attenuation
length, which grows exponentially with altitude (thinner air). Reflecting the
finiteness of the deposition region, the amplitude anchor is
$E_0 =$ **50000** V/m at the
**1000** kt reference yield, matching the canonical
HEMP figure, and the empirical yield exponent is $p =$
**0.85**. These two values, with $\lambda(h)$, are the whole
parameterisation: the envelope has no Compton source term, so the
prompt-gamma fraction (**0.3**\%, Glasstone and Dolan,
1977) is carried as documented provenance for the amplitude anchor and is
*not* an input to the equation above — a limitation of this envelope, not a
calibration. Beyond line of sight the field is taken as zero, which bounds the
illuminated footprint to the geometric horizon
$\sqrt{2 R_\oplus h + h^2}$.

The package also implements the canonical waveform as a normalized
double-exponential, $E(t) = A\,k\,(e^{-\alpha t}-e^{-\beta t})$, with the
early-time (E1), intermediate-time (E2), and late-time magnetohydrodynamic
(E3) components distinguished by documented rate constants (IEC 61000-2-9 for
E1) and amplitude policies.

### Electronics kill-radius analysis (`src/goldeneye/kill_radius.py`)

**4** vulnerability classes are defined by increasing damage
thresholds: *unprotected* microelectronics
(**1000** V/m), *commercial*/semi-hardened
(**10000** V/m), *MIL-STD-188-125*-hardened facilities
(**50000** V/m), and *legacy vacuum-tube*/relay
electronics (**1000000** V/m). Because the E1 envelope is monotone
decreasing in range, the kill radius — the range at which the field meets the
class threshold — is found by deterministic bisection. The enclosed kill area
is $\pi r^2$, and the fraction of the illuminated footprint covered is
$(r/r_\text{horizon})^2$. A smooth damage-probability logistic,
$P = \bigl[1+\exp(-s(E/T-1))\bigr]^{-1}$, gives $P=0.5$ exactly at the damage
threshold.

### Arkangel dam security (`src/goldeneye/dam_security.py`)

**Access control (defense in depth).** The facility is modelled as a cascade
of $n$ layers, each with a per-pass detection probability $p_i$ and response
time $t_i$. The probability of at least one detection is
$1-\prod_i(1-p_i)$; the expected response time to the first detecting layer
weights each $p_i \prod_{j<i}(1-p_j)$ by $t_i$. A composite security score
blends detection coverage with responsiveness in $[0,100]$.

**Breach flood risk.** A dam breach releases a flood wave. Peak outflow
follows the published Froehlich (1995) embankment regression (Froehlich, 1995):
$$Q_p = 0.607\, V^{0.295} H^{1.24},$$
with reservoir volume $V$ and breach head $H$ in SI units. Downstream
propagation uses the Ritter (1892) instantaneous dam-break solution on a dry,
frictionless bed (Ritter, 1892): with $c_0=\sqrt{gH}$, the depth and velocity in the
wave region $(-c_0 \le x/t \le 2c_0)$ are

$$h(x,t) = \frac{1}{9g}\left(2c_0 - \frac{x}{t}\right)^2, \qquad
u(x,t) = \frac{2}{3}\left(c_0 + \frac{x}{t}\right),$$

the front arrives at a downstream distance $x$ at time $x/(2c_0)$, and the
asymptotic peak depth at any fixed distance is
$0.4444\,H$. (The rational factors inside the
Ritter solution — $1/9g$, $2/3$ — are exact constants of that closed-form
solution and cannot drift; the asymptotic depth coefficient is a named module
constant and so is tokenized.) The facility inundation severity is the mean
depth over its ground elevation, binned into a low/moderate/high/extreme risk
rating.

### Orbital platform geometry (`src/goldeneye/orbital_mechanics.py`)

The weapon is delivered from a circular orbital platform. Keplerian kinematics
give the period $T = 2\pi\sqrt{a^3/\mu}$ and speed $v = \sqrt{\mu/a}$ for an
orbit of radius $a$ about the Earth of gravitational parameter
$\mu = 3.986004\times 10^{14}$ m^3/s^2 (Bate, Mueller & White, 1971). Spherical
Earth geometry yields the central angle, elevation angle, and slant range
between the ground target and the platform; a deterministic bisection finds the
maximum central angle at which a chosen minimum elevation is maintained, whose
arc fraction of the orbit bounds the usable pass duration.

### Electromagnetic coupling and shielding (`src/goldeneye/coupling.py`)

To reach electronics the field must couple onto conductors and penetrate
enclosures. Skin depth follows the classical $\delta = \sqrt{\rho/(\pi f \mu_0 \mu_r)}$.
Schelkunoff (1943) shielding effectiveness combines plane-wave absorption
$A = 8.686\,t/\delta$ dB with reflection

$$R = 20\log_{10}\frac{\eta_0}{4\,\lvert Z_s \rvert}\ \text{dB}, \qquad
\lvert Z_s \rvert = \sqrt{2\pi f \mu_0 \mu_r \rho},$$

where $\eta_0 =$ **376.7** $\Omega$ is the
free-space wave impedance and $Z_s$ the conductor surface impedance
(Schelkunoff, 1943; Ott, *Electromagnetic Compatibility Engineering*, 2009;
the multiple-reflection correction is neglected for thick shields). We use
this impedance-ratio form rather than the tabulated shortcut
$R = 168 - 10\log_{10}(\mu_r f/\sigma_r)$ because the latter is only defined
for $\sigma_r$ *relative to annealed copper*; substituting an absolute
conductivity in S/m inflates the reflection loss by $\approx 78$ dB. The two
forms agree to within $0.2$ dB and both are exercised in
`tests/test_coupling.py`. An exposed conductor of length $L$
at field-elevation $\varepsilon$ has effective height $h_\mathrm{eff} =
L\sin\varepsilon$, coupling an induced voltage $V = E\,h_\mathrm{eff}$, and a
protection margin $20\log_{10}(\text{withstand}/E)$ dB quantifies residual
hardness.

### Regional power-network resilience (`src/goldeneye/grid_resilience.py`)

The regional network is a graph of nodes (plants, substations, loads) and
transmission lines on the local plane, the burst nadir at the origin. Every
asset carries a vulnerability class; its survival probability is
$1-P_\mathrm{damage}(E)$ at the asset's envelope field. The most-reliable
source-to-load route maximises the product of survival probabilities
(equivalent to shortest paths under $-\log(\text{survival})$ weights,
deterministic Dijkstra (1959) with insertion-order tie-breaking); redundancy is
the number of edge-disjoint routes via Edmonds-Karp (1972) max flow with unit
capacities, where parallel circuits between one node pair each contribute their
own unit of capacity.
The report's expected served load assumes independence of the surviving
assets along each best path (a documented approximation).

### Breach outflow hydrograph (`src/goldeneye/breach_hydrograph.py`)

The breach's time evolution extends the dam-break analysis. The average breach
width follows the Froehlich (2008) regression

$$B_\mathrm{avg} = 0.27\,K_0\,V^{0.32}H^{0.04},$$

with $K_0 =$ **1.3** for overtopping failure and
**1.0** otherwise (Froehlich, 2008). These are the
coefficients of the *2008* regression as tabulated in the USACE HEC-RAS
technical reference; Froehlich's earlier 1995 width equation uses a different
coefficient set and is not mixed in here. The outflow is
a volume-conserving triangular hydrograph falling linearly from the Froehlich
(1995) peak discharge to zero over $t_d = 2V/Q_p$, so the discharged area
equals the stored volume; its mean outflow is $V/t_d$. A downstream station
table combines the Ritter front-arrival time, the asymptotic peak depth
$0.4444\,H$, and the flood-risk rating at each named
station.

## Results

Run via the ARKANGEL mission software against the canonical scenario
(`scripts/execute.py`), all figures and values below are the deterministic
output of the pure domain core.

### EMP threat envelope

For the canonical weapon (**2000.0** kt at **300.0** km),
the E1 peak field directly under the burst is **90125** V/m,
carrying a peak electromagnetic energy density (0.5·ε₀·E²) of
**0.036** J/m³ at the moment of peak. The
illuminated footprint is bounded by the geometric horizon at
**1978** km radius, an area of **12291795** km^2.
Because the prompt-flux absorption is negligible along the vacuum path at this
altitude, the field decays with the squared geometric projection $\sin^2\psi$
across the footprint.

> **Figure (in the package manuscript):** EMP threat envelope and kill radii.

### Kill radius by vulnerability class

Across the **4** vulnerability classes
(**unprotected, commercial, military, legacy_tube**), kill radii span the full spectrum of the footprint:

| Class | Kill radius (km) |
|---|---|
| Unprotected microelectronics | **1978.0** |
| Commercial / semi-hardened | **849.2** |
| MIL-STD-188-125 hardened | **268.7** |
| Legacy vacuum-tube / relay | **0.0** |

Unprotected microelectronics are destroyed over essentially the entire visible
footprint (**100.0**\% of it); hardened facilities retain a
modest survival zone; legacy vacuum-tube electronics, with their
**0.0** km radius, are immune at every realistic range in
this scenario — a direct consequence of their orders-of-magnitude higher
threshold. The figure above shows how these radii trade off against burst
altitude and yield, and the damage-probability transition for each class.

### Arkangel dam breach flood

Given a reservoir of **130000000** m^3 behind a
**75.0** m head, the Froehlich (1995) regression gives a peak breach
outflow of **31760** m^3/s. The Ritter wave front advances at
**54.2** m/s, reaching the facility **8.0** km
downstream in **2.5** min with an asymptotic peak inundation
of **33.3** m — a severity ratio of **3.333** against
the facility elevation, rated **extreme**.

> **Figure (in the package manuscript):** Ritter dam-break flood wave.

### Downstream inundation stations

The breach hydrograph reports the front-arrival time, the asymptotic peak
depth, and the flood-risk rating at every monitored station downstream of the
dam:

| Station | Distance (km) | Arrival (min) | Peak depth (m) | Risk |
|---|---|---|---|---|
| **facility** | **8.0** | **2.5** | **33.3** | **extreme** |
| **town** | **12.0** | **3.7** | **33.3** | **extreme** |
| **bridge** | **20.0** | **6.1** | **33.3** | **extreme** |

The frictionless Ritter asymptote gives every station the same peak depth
**33.3** m (**0.4444**H, independent of distance), so the
differentiating quantity is the front-arrival time: the facility, nearest the
dam, is the first to be inundated by the **extreme**-rated wave.

### Access-control posture

The **4** layered defense-in-depth cascade yields a
**0.987** probability of detecting an intruder at least once,
an expected response time of **6.3** min, and a
composite security score of **89.3** (out of 100).

### Orbital platform

The weapon rides a circular orbit of radius **6671** km
(**300** km altitude) with a period of
**90.4** min and speed **7.7** km/s. From the
target, the platform stands at a **18.8**-degree elevation
over a **6.5**-degree central angle
(**797.7** km slant range) and remains above a
**5.0**-minute usable pass — the detonation window.

### Coupling and shielding

At the facility the envelope field reaches **10617**
V/m. A **3.2** m effective antenna couples
**34218** V (≈**684** A into a
**50** Ohm load) — a kilovolt-class conducted threat.
In contrast, the skin depth at the representative
**100** MHz E1 frequency is only
**0.008** mm in the
**aluminum** shield; a
**0.10** mm enclosure provides
**192.3** dB of
shielding, reducing the penetrated field to **0.00**
V/m and leaving a **13.5** dB protection margin against the
military withstand level.

### Regional power-network resilience

> **Figure (in the package manuscript):** Regional grid resilience.

The **5**-node, **6**-line regional network
loses the nodes **town_a, relay** to certain failure. It serves an
expected **4.8** MW of the
**17.0** MW critical load (**28.4**\%),
with a worst-case load reliability of **0.000** and a
minimum of **2** redundant routes per critical load.
The mission-critical facility keeps a **0.402** survival
probability over **3** edge-disjoint paths — the
hardened hydro source and a redundant interconnection are what keep it on the
board.

### Breach outflow hydrograph

A breach **164.7** m wide releases the reservoir as a
volume-conserving triangular hydrograph lasting **136.4**
min at a mean outflow of **15880** m^3/s. The flood sweeps all
**3** monitored stations; the farthest,
**20.0** km downstream, is reached in
**6.1** min.

## Conclusion

**GoldenEye: ARKANGEL — Special-Agent Mission Software** delivers a complete, deterministic, and reproducible analysis of
the coupled threat surfaces of *GoldenEye*'s ARKANGEL mission:

1. **An orbital EMP weapon and platform** whose ground-level effects are
 captured by a documented conservative point-source envelope (the canonical
 E1/E2/E3 pulse), delivered by a Keplerian orbital platform with
 determinable pass geometry (**90.4** min period,
 **5.0** min usable pass).
2. **An electronics kill-radius analysis** across **4**
 defensible vulnerability
 classes, from unprotected microelectronics (destroyed over the whole visible
 footprint, **1978.0** km) to legacy vacuum-tube relays
 (immune, **0.0** km).
3. **Coupling and shielding of infrastructure** — **34218** V
 induced onto exposed conductors yet a **192.3** dB shield
 reducing the penetrated field to **0.00** V/m —
 and the resilience of the regional power network
 (**28.4**\% of critical load served;
 **3** redundant paths to the facility).
4. **An Arkangel dam-facility model** combining a layered defense-in-depth
 access-control score with a physically grounded breach-flood risk and
 outflow hydrograph (peak outflow **31760** m^3/s; breach
 width **164.7** m; facility inundation rated
 **extreme**).

Three properties make the package a faithful exemplar of the BOND suite's
guardrails. The analysis is **closed-form and deterministic** — no RNG, no
wall-clock dependence, and a canonical SHA-256 input hash for audit. The
**pure domain core** is infrastructure-free and importable without any BOND
layer, while the protocol integration is confined to a thin, inspectable
adapter (`src/goldeneye/mission.py`) whose public shape is stable across this
deepening. And the whole pipeline is **regenerable**: thin orchestration
scripts drive the mission and produce figures, data, and manuscript variables
from source, so the manuscript cannot drift from the code.

The result is special-agent mission software that treats an on-screen weapon
and facility as a serious, well-tested scientific problem — rigorous enough to
stand beside the analytical tools it mimics, and honest about the simplifying
assumptions documented in `07_scope_and_related_work.md`.

## Experimental setup

### Scenario parameters

All parameters are declared in `manuscript/config.yaml` and loaded by
`src/goldeneye/scenario.py::load_scenario_config`. The canonical ARKANGEL
mission uses:

| Parameter | Value |
|---|---|
| Weapon yield | **2000.0** kt |
| Burst altitude | **300.0** km |
| Reservoir volume | **130000000** m^3 |
| Dam head | **75.0** m |
| Facility downstream distance | **8.0** km |
| Access-control layers | **4** |

The orbital-platform geometry (burst nadir at
**60.0**° N, **108.0**° E; target at
**53.5**° N; platform altitude
**300** km; minimum usable elevation
**10**°), the coupling inputs
(**10** m conductor,
**0.10** mm **aluminum**
enclosure, **100** MHz reference frequency,
**50** Ohm load), the canonical
**5**-node regional grid, and the
**3** downstream stations are declared in
`manuscript/config.yaml` (the `orbit` and `coupling` blocks) and
`src/goldeneye/scenario.py` (the grid and stations).

The EMP envelope constants are fixed in `src/goldeneye/emp_model.py`: an
amplitude anchor of **50000** V/m at the
**1000** kt reference yield and an empirical yield
exponent of **0.85**. The same module also records a
**0.3**\% prompt-gamma fraction, but no function reads
it — the envelope has no Compton source term, so that value is provenance for
the amplitude anchor rather than a parameter of the calculation
(`tests/test_emp_model.py::TestGammaFractionIsReportedNotConsumed` holds this
to be true). (The **90125** V/m nadir
field reported in the results is *computed* from those constants at the
scenario yield, not itself a constant.) The **4**
vulnerability-class thresholds are fixed in `src/goldeneye/kill_radius.py`,
and the **50000** V/m military withstand level used for
the protection margin is declared in `src/goldeneye/scenario.py`.

### Software environment

The package is tested under Python **3.14.6** with NumPy
**2.4.2** and matplotlib; bond-api and bond-utilities are installed as
local path dependencies. This environment snapshot belongs to manuscript
revision **2026-08-04**, the date declared in
`manuscript/config.yaml`. No token reads the wall clock at generation time, so
regenerating the manuscript in this environment rewrites the same bytes (see
§Reproducibility).

### Verification gates

The enforced gates are `uv run pytest tests/ --cov=src --cov-fail-under=90`
(line and branch), `uv run ruff check` and `uv run ruff format`, `uv run mypy
src/ scripts/`, a zero-mock audit of `tests/`, and a live cross-reference test
that every manuscript token (the double-brace variables in the numbered
sections) is produced by `generate_variables`.

## Reproducibility

This is version **0.1.0** of **GoldenEye: ARKANGEL — Special-Agent Mission Software**. Every numeric claim in
this manuscript — result, model constant, and scenario input alike — is produced
from source by a regenerable pipeline; none is hand-authored.

### Regeneration contract

1. `uv run python scripts/execute.py` runs the full mission and persists
 `output/data/arkangel_outcome.json` (bond-api wire format) and a
 provenance-outcome record `output/data/arkangel_mission.json` written via
 `bond_utilities.mission_io.record_provenance_outcome`.
2. `scripts/z_generate_manuscript_variables.py` writes
 `output/data/manuscript_variables.json`, renders the three concept figures
 to `output/figures/`, and resolves the numbered sections into
 `output/manuscript/`.
3. `uv run pytest tests/ --cov=src --cov-fail-under=90` enforces the coverage
 gate; a live cross-reference test guarantees the token map and the
 manuscript cannot drift apart.

### Determinism

The analysis is fully deterministic: fixed scenario parameters, closed-form
physics, and a fixed seed of 0 (no random draws anywhere). The canonical
SHA-256 `input_hash` of the scenario (16 hex characters appear in the execution
report) lets any outcome be audited against the exact inputs that produced it.

**Byte-identity claim and its scope.** Re-running `scripts/execute.py` and
`scripts/z_generate_manuscript_variables.py` in one environment rewrites the
following artifacts byte for byte:

- `output/data/arkangel_outcome.json`
- `output/data/manuscript_variables.json`
- `output/manuscript/*.md` (the resolved sections)
- `output/figures/*.png`

No token in that set reads the wall clock; the dated token in
`05_experimental_setup.md` is the committed `paper.date` from
`manuscript/config.yaml`, not a generation time.
`tests/test_reproducibility.py` regenerates the whole set twice in one test run
and compares the bytes, so the claim fails loudly if a wall-clock value is ever
reintroduced.

Two exclusions, stated rather than hidden:

1. `output/data/arkangel_mission.json` is a **run-scoped provenance record**
 written through `bond_utilities.mission_io`. It deliberately carries a real
 `started_at` wall clock and therefore differs between runs. It is not
 covered by the byte-identity claim.
2. Byte-identity is claimed *within one environment*. `3.14.6` and
 `2.4.2` are environment provenance, so a different interpreter
 or NumPy build legitimately changes those two tokens and the sections that
 render them.

### Output inventory

Regenerable artifacts under `output/` (git-ignored):

- `data/arkangel_outcome.json`, `data/arkangel_mission.json`,
 `data/manuscript_variables.json`
- `figures/emp_footprint.png`, `figures/flood_wave.png`,
 `figures/grid_resilience.png`
- `manuscript/` (numbered sections with tokens resolved)

Live test count and achieved coverage are tracked in
`docs/_generated/COUNTS.md`, not hardcoded here.

## Scope and related work

### Scope

This package models the coupled threat surfaces of *GoldenEye* (1995) — the
orbital weapon and its platform, electronics vulnerability, EM coupling and
shielding, regional power-network resilience, and the Arkangel dam facility's
access control and breach flood — with closed-form, deterministic
approximations across seven pure-core modules. It is engineering mission software,
not a predictive defence-physics code, and its honesty about assumptions is
part of the deliverable.

**EMP envelope.** The ground field is a *conservative point-source envelope*.
It omits the full distributed-source HEMP field computation, polarization and
coupling detail, and site-specific shielding/cable-coupling response. Because
it treats the source as a point, the kill footprint it yields is smaller than
a detailed code would predict — deliberately the conservative direction for a
damage assessment. Waveform components E1/E2/E3 use documented representative
rate constants; E2 is not standardized (IEC defines E1 most strictly) and its
amplitude fraction is an engineering default.

**Kill radius.** Vulnerability-class thresholds are engineering references
from the EMP-hardening literature (e.g. MIL-STD-188-125 for the
**50000** V/m E1
hardness level), not guarantees for specific equipment under specific coupling
conditions. Damage probability is a smooth surrogate, not a validated
reliability model.

**Dam breach.** The Ritter solution assumes an instantaneous, complete breach
on a dry, frictionless, prismatic bed. Real dam failures evolve over minutes
with friction and valley geometry, so arrival times here are lower bounds and
depths are idealizations. The Froehlich regression is a statistical peak-
outflow relation and carries scatter. The breach hydrograph is a
volume-conserving triangular idealization of a real, irregular outflow curve;
the downstream station table uses the frictionless asymptotic peak depth
**0.4444**`*H` rather than a full flood-routing model.

**Orbital platform.** The orbital analysis assumes a circular, two-body orbit
(Bate, Mueller & White) and a directly-overhead pass for the pass-duration
approximation; it ignores J2 perturbations, drag, and a real, non-zenith pass
profile, so durations are upper-bound estimates of a usable detonation window.

**Coupling and shielding.** Coupling uses a simple effective-height model of
an exposed conductor (Ott; Vance) and the plane-wave Schelkunoff approximation
for shielding; it omits the multiple-reflection correction, aperture/cable
penetration leakage, and non-plane-wave (diffuse) coupling. Induced voltages
are open-circuit estimates, not load- and joint-dependent.

**Grid resilience.** Survival probabilities assume independent asset failures
from the local envelope field; the expected served load is the sum of each
critical load's best-path reliability (an independence approximation, not a
full stochastic cascade). Parallel circuits between the same node pair are
counted individually for redundancy and collapsed to the most survivable
circuit for path reliability. The canonical
**5**-node network is a scenario dataset,
not the real Severnaya grid.

### Related work

The models sit on well-established foundations. High-altitude EMP is treated
in the canonical reference *The Effects of Nuclear Weapons* (Glasstone and
Dolan, 1977), and the early-time waveform shape follows IEC 61000-2-9.
Orbital mechanics follow Bate, Mueller & White's *Fundamentals of
Astrodynamics* (1971). Coupling and shielding follow Ott's *Electromagnetic
Compatibility Engineering* (2009) and Vance's *Coupling to Shielded Cables*
(1978). Peak dam-breach outflow is regressed by Froehlich (1995) and breach
geometry by Froehlich (2008); the classical instantaneous dam-break solution
originates with Ritter (1892) and is presented textually in Stoker's *Water
Waves* (1957). The shielding-effectiveness formulation is Schelkunoff's (1943).
The two graph algorithms are used in their original forms: shortest paths after
Dijkstra (1959), applied here to `−log` survival weights, and edge-disjoint path
counting by max flow after Edmonds and Karp (1972). Network-resilience reasoning
additionally draws on the cascade-failure framing of Buldyrev et al. (2010). Defense-in-depth detection probability is the
standard layered-reliability formula. The BOND protocol itself is specified in
the frozen `bond-api` package; this package is one of many films implementing
that contract.

## Sources

@glasstone1977effects; @iec6100029; @milstD188125; @froehlich1995peak; @ritter1892fortpflanzung; @stoker1957water; @bate1971fundamentals; @ott2009electromagnetic; @vance1978coupling; @froehlich2008breach; @buldyrev2010cascading; @dijkstra1959note; @edmonds1972theoretical; @schelkunoff1943electromagnetic


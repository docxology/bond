# Tomorrow Never Dies (1997) — CARVER

*film package · package codename CARVER*. Mission **CARVER**: model Carver-style disinformation propagation on a social network; measure narrative capture and echo-chamber fragmentation under a bounded-confidence broadcast; quantify low-RCS stealth-vessel detection limits; recover detection range against a stealth hull via pulse compression; analyze GPS-denial impact and navigation failure cascades; bound spoofed-measurement error with RAIM integrity monitoring.

## Concepts — CARVER: domain and operational focus

media manipulation, stealth

## Abstract — CARVER: mission summary

**Tomorrow Never Dies: CARVER — Special-Agent Mission Software** (*Six Paired Models of Media, Radar, and Navigation Warfare: Disinformation and Narrative Control, Stealth Detection and Pulse Compression, GPS Denial and RAIM Integrity*). CARVER is a deterministic mission-software package that turns the media-warfare playbook of Elliot Carver into 6 quantitative, reproducible analyses, paired as attack and counter across media, radar, and navigation. A disinformation model simulates how a broadcast campaign converts a social network to a manufactured belief — 57.5% by campaign end, 11.5x the no-media baseline — and a bounded-confidence narrative model shows how a *selective* broadcast pulls the audience mean 54.2% toward the manufactured line while fragmenting it into echo chambers (bimodal split 0.402; the tipping point is a reach of just 19.6%). A radar model finds that a 20.0 dB low-RCS reduction drops a stealth hull's detection range to 40.7 km (25.7 km for a Rayleigh fluctuating hull), but pulse compression (27.0 dB, 15.0 m resolution, -13.5 dB range sidelobes) restores it to 108.2 km — 373% beyond an unmodulated pulse of the same range resolution; the Barker-13 code reaches that same 108.2 km at the cost of 577 m range resolution in exchange for a -22.2 dB sidelobe floor. A GPS-denial model drives effective C/N0 from 45 to 10.5 dB-Hz at 100 km — below the 25 dB-Hz carrier-lock threshold, so the modelled outcome is loss of lock rather than the 25.3 m the range-error formula extrapolates past its validity (clean-sky: 8.7 m) — and fails 0.429 of the maritime dependency network; its RAIM guardian bounds the damage (HPL 19.9 m) but catches a 20 m corrupted navigation measurement with only 25.2% probability on the worst-placed satellite (54.2% on the best-placed) — the parity projection sees only part of any single-satellite fault. Keywords: disinformation propagation, media manipulation, bounded-confidence opinion dynamics, echo chambers, radar cross-section, stealth detection, pulse compression, matched filtering, GPS denial, navigation failure cascade, RAIM, GNSS integrity monitoring, deterministic simulation, reproducible research.

## Introduction — CARVER: mission framing, the operational problem, and how to read this chapter

In *Tomorrow Never Dies* (1997), Elliot Carver builds a global media empire
whose reach lets him manufacture the conflicts he then reports. His two
instrumental capabilities are a stealth cruiser that evades radar and the
ability to deny an adversary their navigation. This package — codename
CARVER — models those capabilities as deterministic physics
and computation, forming a single reproducible "mission software" artifact.

Each capability is modelled twice: once as the attack, once as the defence
that answers it. The result is 6 infrastructure-free domain
modules in three adversarial pairs.

**Media.**

* **Disinformation propagation** (`media_manipulation.py`): a two-channel
 belief-diffusion model on a social network, with media-campaign injection
 and greedy influence maximization — *whether* an agent believes.
* **Narrative control** (`narrative_control.py`): Hegselmann–Krause
 bounded-confidence opinion dynamics with a media-injection term — *how far*
 an opinion moves, how the audience fragments into echo chambers, and the
 minimum broadcast reach that tips the network.

**Radar.**

* **Stealth-vessel detection** (`stealth_detection.py`): the radar equation,
 Neyman-Pearson detection, Marcum-Q and Swerling detection probabilities,
 and the detection-range penalty of a low-RCS hull.
* **Pulse compression** (`radar_waveform.py`): the radar's counter — LFM and
 Barker-13 matched filtering, processing gain, range resolution, sidelobe
 floor, and the fourth-root detection-range recovery.

**Navigation.**

* **GPS-denial impact** (`gps_denial.py`): satellite geometry and dilution of
 precision, jamming degradation of carrier-to-noise, position-error growth,
 and navigation failure cascades.
* **GNSS integrity** (`gnss_integrity.py`): the receiver's counter — RAIM
 parity-space fault detection, protection levels, and the probability of
 catching a corrupted measurement before it becomes a wrong position.

The same core is wired to the BOND-API mission protocol (codename THE
PROTOCOL): a `MissionProvider` named CARVER lets any coordinator discover the
package by slug and drive the full brief → recon → plan → execute → debrief
lifecycle, with every outcome carrying deterministic provenance. All numbers
in this manuscript are injected from `docs/manuscript/config.yaml` and the real
domain modules — none are hand-authored in the prose.

## Methodology — CARVER: the analytical models and algorithms that drive the mission

Each concept is a self-contained deterministic model with clear physical or
algorithmic grounding.

### Disinformation propagation

Agents occupy one of two belief states — susceptible or believing — on a
Watts–Strogatz small-world network of 120 nodes (seed
7). The broadcast footprint — the 30% of nodes the
media channel reaches — is selected by a deterministic index mix rather than
an RNG draw, so it is a pure function of network size, reach, and seed, and
widening the reach only ever *adds* nodes to the exposed set.
`simulate_disinformation`
(`src/tomorrow_never_dies/media_manipulation.py`) converts susceptible agents
through a media channel (a deterministic exposed subset converts with a
persuasion probability) and a social channel (believing agents convert
susceptible neighbors). Belief share, the echo-chamber coefficient, and the
amplification factor are recorded; `influence_maximization` applies a greedy
Kempe–Kleinberg–Tardos seed selection.

### Narrative control (bounded confidence)

`narrative_control.py` models *how strongly* opinions move, using the
Hegselmann–Krause bounded-confidence model with a Carver-style media
injection term. Each round agent ``i`` moves to the mean opinion of the agents
within confidence radius ``epsilon``, and exposed agents are additionally
pulled toward the manufactured line ``m`` with a media weight. `simulate_opinions`
returns the final consensus, the opinion variance (polarization), the bimodal
split (fraction of agent pairs separated by more than ``2 * epsilon`` — a
measure of echo-chamber fragmentation), and the media capture (the normalized
shift of the mean toward the manufactured line versus a no-media baseline).
`critical_media_reach` bisects the broadcast reach that just tips the discrete
belief model to a target share: the *minimum* audience Carver must reach.

### Stealth-vessel detection

`stealth_detection.py` evaluates the monostatic radar equation
`snr_at_range`: \begin{equation} \mathrm{SNR} = \frac{P_t G^2 \lambda^2 \sigma}{(4\pi)^3 R^4 k T_0 B F L}, \end{equation}
yielding the per-pulse SNR (coherent integration is applied by
`detection_probability`). A false-alarm probability sets a square-law
threshold; `detection_probability` returns $P_d$ by numerically integrating
the Marcum Q function (Swerling 0) or the closed form (Swerling 1).
`detection_range` binary-searches the range at which $P_d$ reaches a target.

### Pulse compression (waveform design)

`radar_waveform.py` analyzes the radar's *counter* to stealth: a modulated
pulse concentrates its energy through pulse compression. Three waveforms are
implemented — unmodulated (gain 1), the LFM chirp (time-bandwidth product
10.0 MHz-bandwidth, processing gain 27.0 dB,
range resolution 15.0 m, and the sinc sidelobe floor of
-13.5 dB), and the Barker-13 phase code (gain
13x, measured sidelobe floor -22.2 dB —
the code's autocorrelation is 13 at zero lag and unity elsewhere, the best
uniform sidelobe floor known for a single binary code, with the measured
value sitting just above the ideal ``20 log10(1/13)`` because a finite sample
rate quantizes the chip boundaries). The matched filter is an exact
convolution; the compression gain is treated as coherent integration *and*
the receiver noise bandwidth is set to the waveform's own bandwidth, which
together reduce the budget to matched-filter energy ``P_t T / N_0``. Both
substitutions are needed: banking the ``B·T`` gain against the radar's
narrower surveillance noise bandwidth would credit the gain twice.
Consequently a modulated and an unmodulated pulse of *equal duration* have
equal detection range, and the reported recovery
(`waveform_detection_range`) is measured against an unmodulated pulse of
equal range *resolution* — duration 0.10 µs — where
the fourth-root law ``R ∝ gain^(1/4)`` applies.

### GPS-denial impact

`gps_denial.py` builds a Walker-delta constellation as orbital geometry —
24 satellites split evenly across 6 inclined
circular planes, propagated to Earth-centred positions and projected into the
receiver's east/north/up frame — so azimuth and elevation are derived, not
drawn, and only the 8 satellites geometrically in view
above the 10° mask enter the geometry matrix and the
dilution of precision. It then quantifies jamming degradation of
carrier-to-noise into position-error growth (``PDOP * UERE``).

That growth has a validity boundary, and the canonical scenario sits on the
wrong side of it. At the 100 km standoff the effective
C/N0 falls from 45 to 10.5 dB-Hz —
still positive, but far below the 25 dB-Hz a C/A
receiver needs to hold carrier lock. `maintains_lock` reports that verdict
explicitly rather than leaving it implicit in a smooth curve. The honest
reading is therefore *denial*: a real receiver stops producing a solution,
and the 25.3 m quoted in the results is what the
code-tracking formula extrapolates past its own validity, not an accuracy a
receiver would report. The gps figure shades that region for the same reason and
extends to 2000 km so the standoff at which lock returns is visible.
Loss of navigation, not degraded navigation, is what
`simulate_navigation_cascade` then propagates across the maritime dependency
network until a fixpoint.

### GNSS integrity (RAIM)

`gnss_integrity.py` implements Receiver Autonomous Integrity Monitoring: a
scipy-free chi-square CDF/quantile (regularized incomplete gamma, series) and
normal quantile; the parity matrix built from the full SVD of the geometry
matrix; a test statistic and detection threshold at a target false-alarm
rate; per-satellite fault slopes; and horizontal/vertical protection levels
(HPL/VPL) with a missed-detection margin. `detection_probability` reports the
probability of catching a measurement bias of a given size via the noncentral
chi-square. The parity projection is *not* norm-preserving: a bias ``b`` on
satellite ``i`` lands in parity space with squared length ``P_ii b²``, where
``P_ii ≤ 1`` is that satellite's projection factor
(`parity_projection_factors`, summing to the ``n − 4`` degrees of freedom).
The noncentrality is therefore ``P_ii (b/σ)²`` and detection probability
depends on *which* satellite is faulted, so `detection_probability` requires
the factor as an argument rather than defaulting to one. The reported figure
is the worst-placed satellite, matching the worst-slope convention the
protection levels already use.

## Results — CARVER: measured outcomes, headline numbers, and what they establish

### Disinformation propagation

Social spread alone converts 5.0% of the network. Adding
Carver's broadcast multiplies that by 11.5x, ending at a
57.5% belief share with an echo-chamber coefficient of
0.913 and an amplification of 1.92 believers per
directly-exposed agent — the broadcast does not merely seed the belief, it
recruits the social channel that then carries it. The disinformation figure shows
both trajectories.

![Believing fraction over time: media campaign vs no-media baseline](output/figures/tomorrow_never_dies_disinformation_propagation.png)

### Narrative control

Bounded-confidence dynamics reveal *for whom* the message lands. Under a reach
of the media campaign, the audience mean is pulled 54.2%
toward the manufactured line (0.85), reaching a consensus of
0.691, while the opinion variance stays at
0.0202 and the bimodal split of 0.402 shows
the audience fragmenting into detached opinion clusters — echo chambers. The
tipping-point analysis finds that a broadcast reach of just
19.6% is enough to drive the discrete belief model past a
majority. The narrative figure shows the opinion trajectory under the campaign.

![Narrative control: bounded-confidence opinion dynamics under a media campaign](output/figures/tomorrow_never_dies_narrative_control.png)

### Stealth-vessel detection

A 20.0 dB RCS reduction (from a reference target to a
stealth hull) cuts the detection range from 128.6 km to
40.7 km — a range ratio of 0.316, a
68% loss, and exactly the fourth-root radar law.
Reporting the same hull as a Rayleigh (Swerling-1) fluctuating target — the
realistic case for a ship in a sea-clutter background — leaves it detectable
only out to 25.7 km: a fading target must beat the detection
threshold across the whole integration dwell rather than at a single peak.
The stealth figure shows the detection probability curves.

![Detection probability vs range: reference target and stealth hull](output/figures/tomorrow_never_dies_stealth_detection.png)

### Pulse compression

The radar claws the range back. An LFM waveform with 10.0 MHz
of bandwidth yields 27.0 dB of processing gain and
15.0 m of range resolution at a -13.5 dB sidelobe floor.
Treating that gain as coherent integration — with the noise bandwidth matched
to the waveform — restores the stealth hull's detection range from
40.7 km under the radar's unmodulated surveillance pulse to
108.2 km. Measured against the like-for-like baseline, an
unmodulated pulse of the *same range resolution*
(0.10 µs, reaching 22.9 km),
that is a 373% improvement — exactly the fourth root
of the gain. The two baselines are different pulses and the comparison is
stated against each explicitly: matched filtering makes range depend on pulse
energy alone, so compression does not buy range over an equally long pulse;
what it buys is that resolution stops costing range.
The waveform figure shows the compressed-pulse envelopes of the LFM chirp and the
Barker-13 code. The Barker code buys far less gain (13x
against the chirp's 27.0 dB) but pays for it with a much cleaner
range response: a measured -22.2 dB sidelobe floor against
the chirp's -13.5 dB. The reach-vs-sidelobes tension has to be
stated carefully, because the two range claims are not comparable the way they
first appear: at equal peak power and equal pulse duration the Barker code
reaches the *same* 108.2 km as the chirp, because
matched-filter detection range depends on pulse energy alone and the code's
lower gain (13x) is offset by its proportionally narrower
effective bandwidth. What the Barker code actually gives up is resolution — its
effective bandwidth resolves range only to 577 m against
the chirp's 15.0 m — and what it buys in return is that cleaner
-22.2 dB sidelobe floor: a lower chance that a bright
return's sidelobe masks a dim return beside it. The trade is therefore
resolution and clutter-masking performance, not reach.

![Pulse compression: matched-filter range response for LFM and Barker-13](output/figures/tomorrow_never_dies_waveform_pulse_compression.png)

### GPS-denial impact

The Walker geometry puts 8 of the 24
satellites above the 10° mask at the receiver — the
realistic count for a single epoch, not the whole constellation. With the
resulting position dilution of precision of 1.70, a clean-sky receiver
sits at 8.7 m of 1-sigma error. A 34.5 dB
jammer-to-noise ratio pulls the effective C/N0 to
10.5 dB-Hz — below the 25 dB-Hz
carrier-lock threshold, so the modelled outcome is that the receiver stops
tracking rather than reports a worse fix. The UERE formula, which has no
notion of losing lock, extrapolates 25.3 m there; that
number is reported as the extrapolation it is and not as an achieved
accuracy. Either way the jamming cascades:
0.429 of the maritime systems fail over 3
cascade rounds. The gps figure plots position error against jammer standoff
distance.

![Position error vs jammer standoff distance (GPS denial)](output/figures/tomorrow_never_dies_gps_denial.png)

### GNSS integrity (RAIM)

RAIM sets the receiver's guardrails: with 4 degrees of freedom and a
test-statistic threshold of 28.5, the horizontal and vertical
protection levels are 19.9 m and 35.8 m — comfortably inside the
maritime alert limit, so integrity is declared *available*.

Detection of a 20 m corrupted measurement is *not* a single
number, because the parity projection sees only the fraction ``P_ii`` of a
fault on satellite ``i``: that fraction runs from
0.43 to 0.60 across this geometry. The
same bias is therefore caught with 25.2% probability on the
worst-placed satellite and 54.2% on the best-placed one; the
worst case is the figure reported, because it is the one integrity has to
survive. This is the honest cost of a modest 4-degree-of-freedom
geometry: the protection level, not the detection probability, is what RAIM
guarantees at this bias size. The raim figure shows both ramps against measurement
bias.

![RAIM: detecting a corrupted navigation measurement](output/figures/tomorrow_never_dies_raim_detection.png)

## Conclusion — CARVER: findings, verdict, and what the mission establishes

CARVER demonstrates that the media-warfare instruments of *Tomorrow Never
Dies* admit quantitative, reproducible models across six coupled analyses.
Disinformation spreads through media exposure amplified by social diffusion —
the broadcast multiplies the no-media baseline by 11.5x — and
bounded confidence shows how a selective broadcast both moves the audience
mean and fragments it into echo chambers. A stealth hull trades
20.0 dB of radar cross-section for a
68% loss of detection range, but pulse compression
restores it by the exact fourth-root of the processing gain. And navigation
warfare is two-sided: GPS denial degrades accuracy and cascades failure
through the dependency web, while RAIM bounds the position error a corrupted
measurement can hide. Every result is deterministic, tested without mocks,
and every number in this manuscript is injected from the canonical CARVER
scenario rather than hand-authored.

Because the same core is exposed through the frozen BOND-API
`MissionProvider` protocol, the deepened package remains discoverable and
drivable by any coordinator through the unchanged brief → recon → plan →
execute → debrief lifecycle, with provenance that lets any outcome be audited
against its inputs.

## Experimental Setup — CARVER: canonical scenarios, parameters, and configuration

### Scenario configuration

All results derive from one canonical, deterministic scenario
(`src/tomorrow_never_dies/scenario.py`), parameterised in
`docs/manuscript/config.yaml` and `SCENARIO_PARAMS`, executed with a fixed seed
7:

Every value below is an injected token read out of `SCENARIO_PARAMS` itself,
not a transcription of it: changing a parameter rewrites this section on the next
regeneration, so the setup can never describe a run that did not happen.

* **Media**: a 120-node small-world network; a broadcast reaching
 30% of it, per-exposure persuasion 0.12, per-edge
 social spread 0.05, over 15 rounds.
* **Narrative**: bounded-confidence opinion dynamics over
 120 agents with confidence radius 0.10, a
 manufactured line at 0.85, media weight
 0.10, broadcast reach 40%, over
 20 rounds; the critical-reach search targets a
 50% belief share.
* **Stealth**: a monostatic radar with a 10 GHz (X-band)
 carrier and 4 coherently integrated pulses; a reference RCS of
 1 m² and a stealth RCS of 0.01 m² at a
 false-alarm probability of 1e-06 and a 0.9 detection
 target.
* **Waveform**: an LFM chirp (10.0 MHz bandwidth,
 50 µs, 40 MHz sampling) for
 pulse compression, compared against an unmodulated pulse of equal peak power
 *and equal range resolution* (0.10 µs) and against the
 Barker-13 phase code.
* **GPS**: a 24-satellite Walker-delta constellation in
 6 planes at 55° inclination, seen from a
 receiver at 15°N 115°E in the
 South China Sea (elevation mask 10°, leaving
 8 satellites in view at the modelled epoch), a
 1 W jammer at
 100 km standoff, a clean C/N0 of 45
 dB-Hz, and a maritime dependency network of 7 systems.
* **Integrity**: RAIM at a false-alarm rate of 1e-05, a
 missed-detection rate of 0.001, a measurement sigma of
 3 m, and a maritime alert limit of
 556 m (0.3 NM); the detection probe is a
 20 m measurement bias.

### Software environment

* Package: Tomorrow Never Dies: CARVER — Special-Agent Mission Software, version 0.1.0, maintained by
 Daniel Ari Friedman.
* Python: 3.14.6.
* Determinism: fixed seed 7; no wall-clock anywhere in the
 persisted tree — not in mission outcomes (`wall_time_s = 0`) and not in this
 manuscript, which carries the committed manuscript date rather than a
 generation timestamp; no untracked random draws.

### Regeneration

```bash
## Canonical results + figures + resolved manuscript:
uv run python scripts/z_generate_manuscript_variables.py
## Full mission lifecycle via the protocol:
uv run python scripts/run_mission.py
```

Manuscript date 2026-08-04 (`paper.date` in `docs/manuscript/config.yaml`).
This is the committed date of the manuscript, not the time of the last
regeneration: re-running the command above on an unchanged tree rewrites the
same bytes, which it could not do if this line moved with the clock.

## Reproducibility — CARVER: verification gates, deterministic regeneration, and artifacts

### Determinism guarantees

* **Fixed seed**: every stochastic draw flows from `numpy.random.default_rng(7)`;
 identical inputs produce byte-identical trajectories.
* **No wall-clock in persisted artifacts**: mission provenance records
 `wall_time_s = 0`, and no generation timestamp is injected into the
 manuscript — the date in the experimental setup is the committed
 `paper.date`. Regenerating twice on the same checkout and interpreter
 therefore produces a byte-identical `output/` tree, figures included; this
 is asserted, not asserted-about, by `test_regeneration_is_byte_identical`
 in `tests/test_scripts_smoke.py`, which runs the generator twice across a
 second boundary and compares every artifact byte for byte. The single
 environment-derived token, `3.14.6`, is a property of the
 interpreter, so the byte-identical claim is scoped to a fixed interpreter;
 the scenario numbers themselves are seeded and interpreter-independent.
* **Canonical input hash**: the `script/driver` records a sha256
 fingerprint of `SCENARIO_PARAMS` so any outcome can be audited against its
 inputs without re-running the film.

### Verification

The suite is verified with the gates in the package preamble:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
rg -n "template[_]code_project". --glob '!.git/**' --glob '!uv.lock' --glob '!**/AGENTS.md' # -> zero
git status --short # clean
```

Live test count and achieved coverage are tracked in
[`docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md), not hardcoded in
this manuscript.

### Artifacts

* Figures (one per domain concept):
 `output/figures/disinformation_propagation.png`,
 `output/figures/narrative_control.png`,
 `output/figures/stealth_detection.png`,
 `output/figures/waveform_pulse_compression.png`,
 `output/figures/gps_denial.png`,
 `output/figures/raim_detection.png`.
* Variables: `output/data/manuscript_variables.json`.
* Resolved manuscript: `output/manuscript/*.md`.

All under `output/` are regenerable and git-ignored.

### What is *not* reproducible from this manuscript alone

The section files hold token placeholders, not numbers. Reading the raw
`docs/manuscript/*.md` gives the argument but no values; the values only exist
after `z_generate_manuscript_variables.py` has run the canonical scenario.
That is deliberate — it makes a stale number impossible to ship, because
there is no number in the source to go stale.

## Scope and Related Work — CARVER: boundaries, positioning, and relationship to the literature

### Scope

CARVER is a didactic mission-software model, not an operational tool. Every
model here is internally consistent, deterministic, and tested against its own
closed forms and known values — and none of them is calibrated against
measured data. The specific limitation differs per concept, so it is worth
naming each rather than gesturing at "simplifications":

* **Disinformation propagation** — conversion probabilities are free
 parameters, not fitted quantities. The model shows how a two-channel
 campaign behaves for a given persuasion and spread rate; it says nothing
 about what those rates are for any real population. The compartmental
 structure is deliberately two-state (susceptible, believing): there is no
 unaware compartment and no return path, so the model cannot represent
 reach-limited awareness or belief decay.
* **Narrative control** — the bounded-confidence update is a mechanism, not a
 measurement. Hegselmann–Krause has no empirical calibration here at all: the
 confidence radius and media weight are chosen, and the reported capture and
 bimodal split are properties of that choice.
* **Stealth-vessel detection** — free-space, clutter-free propagation and a
 point target with a single aspect-independent RCS. Both target-fluctuation
 models are now reported: the canonical range (40.7 km) is the
 nonfluctuating Swerling-0 case, and a Rayleigh (Swerling-1) fluctuating hull
 is detected only out to 25.7 km. Swerling-1 is the more
 realistic model for a ship in sea clutter, so the quoted
 40.7 km is the optimistic (non-fading) bound.
* **Pulse compression** — the compression gain is treated as ideal coherent
 integration, with no weighting losses, no Doppler mismatch, and no
 range–Doppler coupling, all of which degrade a real LFM chirp. The noise
 bandwidth is set equal to the waveform bandwidth, which is the matched-filter
 ideal; a real receiver's noise bandwidth exceeds it. Because range then
 depends on pulse energy alone, the reported improvement is meaningful only
 against the stated equal-resolution baseline — quoting it against a pulse of
 equal *duration* would be wrong, and against the radar's surveillance pulse
 it would mix a resolution change into a range claim.
* **GPS denial** — one jamming source; a single-epoch snapshot of one Walker
 constellation over one receiver, on a spherical non-rotating Earth with no
 orbital eccentricity, no J2 drift, and no per-satellite signal budget, so
 the visible count and DOP describe that instant and not a daily
 distribution; and a dependency cascade with a single scalar coupling factor
 on every edge rather than a real receiver-in-the-loop or per-link model.
 The UERE code-tracking term ``47·10^(−C/N0/20)`` is extrapolated below a
 receiver's lock threshold, and the canonical jamming case is entirely inside
 that region: the reported jammed position error is the formula continued
 past its validity, not an accuracy any receiver would achieve. The figure is
 shaded accordingly. The threshold itself is a single representative
 constant, not a receiver-specific budget, and no acquisition-versus-tracking
 distinction is modelled.
* **GNSS integrity** — single-fault RAIM only. Multiple simultaneous faults,
 the case that most concerns a deliberate spoofer, are outside the
 parity-space assumption used here. Detection probability is also
 satellite-specific (noncentrality ``P_ii (b/σ)²``); the single figure
 reported is the worst-placed satellite, and no claim is made that a bias of
 the probed size is caught reliably — at this geometry it is not.

These restrictions are the price of keeping every computation transparent,
deterministic, and verifiable end to end from a bare checkout.

### Related work

* **Opinion dynamics / narrative control**: the bounded-confidence update is
 the Hegselmann–Krause model, generalising the DeGroot consensus framework
 to bounded interaction; the media-injection term models an exogenous
 broadcast pulling a subset of agents.
* **Radar detection and waveforms**: the radar equation and Marcum/Swerling
 detection probabilities follow classical radar detection theory; the LFM
 chirp and Barker-13 phase code follow the pulse-compression literature
 (Skolnik; Barker).
* **Influence maximisation**: the greedy seed-selection procedure follows the
 submodular influence-maximisation framework, applied here with
 deterministic simulations for reproducibility.
* **Disinformation propagation**: the belief-diffusion model is a
 compartmental epidemiological analogy (susceptible–believing) adapted to
 media-driven belief change.
* **GNSS denial and integrity**: dilution-of-precision and jamming-to-noise
 degradation follow standard satellite-navigation error models; the cascade
 is a thresholded dependency-graph propagation; RAIM follows the baseline
 autonomous-integrity scheme of Parkinson–Axelrad and Brown.

The package itself is one film in the BOND suite, interoperating through the
frozen `bond_api` `MissionProvider` protocol rather than bespoke interfaces.

## Sources — CARVER: bibliography

@marcum1960statistical; @swerling1960probability; @kempe2003maximizing; @misra2006gps; @skolnik2001radar; @tnd1997; @hegselmann2002opinion; @degroot1974reaching; @barker1953group; @parkinson1988autonomous; @brown1992baseline


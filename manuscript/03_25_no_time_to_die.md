# No Time to Die (2021) — HERACLES

*film package · mission codename HERACLES*. Mission **HERACLES**: assess DNA-targeted bioweapon countermeasure specificity and delivery; design and rank the countermeasure guide across a population; characterize poison-garden dose-response toxicology; screen competitive-antagonist antidotes against a toxin dose; assess poison exposure pathways and cumulative risk; run vesper poison-delivery trace detection forensics.

This chapter reproduces the package's complete manuscript verbatim:
the abstract and every authored section, token-hydrated from the
package's own manuscript variables, with the package's figures carried
in the combined PDF and its sources resolved against the unified
bibliography.

## Concepts

DNA-targeted bioweapons, toxicology

## Abstract

No Time to Die: HERACLES — Special-Agent Mission Software — mission codename **HERACLES** — reduces the pharmaco-forensic threats of *No Time to Die* (2021) to deterministic, tested mathematics with a shared provenance ledger. The pure domain core in `src/no_time_to_die/` comprises **6** modules spanning three threat families: a DNA-targeted bioweapon countermeasure (target specificity, guide design, and delivery kinetics), poison-garden toxicology (dose–response and competitive-antagonist pharmacology), and poison-delivery forensics (exposure assessment and trace detection on the Vesper's glass). A thin adapter binds that core to the frozen bond-api mission protocol so the film is discoverable and drivable by the BOND suite orchestrator. The poison-garden catalog profiles **7** flora toxins spanning 0.8 to 10.0 mg/kg (median 1.5) — commonly-cited order-of-magnitude LD50 figures paired with invented Hill slopes. The HERACLES countermeasure demonstration selects a target guide that attains 66.67% specificity against a constructed reference genome with a planted, documented structure, and a combined neutralization probability of 49.59%. Guide design ranks 4 candidates by a Doench-style efficiency blended with population off-target burden; a screen over five invented inhibition constants restores 98.87% survival against a ricin dose; and the delivered exposure carries a margin of exposure of 8.333 (risk quotient 60) — a verdict of elevated risk. Forensic trace detection clears a limit-of-detection signal-to-noise ratio of 3.0 at an observed SNR of 9, recovering a dosable residue from the glass and identifying it as ricin. The entire assessment is deterministic — no module imports a clock or an RNG, the canonical input digest is `cb8fe93a43fc`, and two runs on one interpreter render byte-identical artifacts — and it is reproduced under Python 3.14.6, satisfying the suite's coverage, mock-free, and lineage gates. Every constant is registered with its provenance class in `data/claim_ledger.yaml`; none is a measurement.

## Introduction

*No Time to Die* (2021) introduces three interlocking threats that map cleanly
onto computational modelling problems: a DNA-targeted bioweapon program
codename **HERACLES** designed against a specific genetic profile; the poison
garden cultivated on the villain's island, a landscape of naturally occurring
plant toxins; and the forensic task of detecting a poison delivered through a
drink — the trace left on the Vesper's glass.

This package treats each as a real, deterministic computational object rather
than a narrative device. Each threat family decomposes into a pair of concerns,
giving the **6** domain modules of the core:

1. **Target specificity and delivery** (`bioweapon_counter.py`) — a designed
 nucleic-acid guide must hit its intended target while minimizing off-target
 matches in a reference genome, and the fraction of an administered dose that
 reaches the target compartment follows first-order absorption kinetics.
2. **Guide design under population off-target burden** (`targeting_design.py`)
 — the guide is not given but *designed*: sequence descriptors drive a
 Doench-style activity score, which is then discounted by the near-miss
 burden the guide would incur across a population of reference genomes.
3. **Dose–response toxicology** (`toxicology.py`) — every member of the
 garden's flora is a Hill-curve hazard characterized by an LD50 and a slope;
 mixtures combine under response addition.
4. **Antidote pharmacology** (`antidote_screening.py`) — a competitive
 antagonist shifts a toxin's effective dose–response, so a library of
 candidate antidotes can be ranked by the survival each restores against a
 given toxin dose.
5. **Exposure assessment** (`exposure_assessment.py`) — the hazard is set by
 the *absorbed* dose rather than the residue: pathway intake, body burden
 under first-order elimination, margin of exposure, and risk quotient.
6. **Delivery forensics** (`delivery_forensics.py`) — given an observed
 analytical signal and noise, we decide whether a trace is present,
 back-compute its concentration from a calibration model, and identify the
 poison by spectral matching.

Modules 1–2 and 3–4 are deliberately paired: detection without design, and
hazard without countermeasure, would each leave the mission's central question
— *can this threat be neutralized?* — unanswerable. Module 5 bridges the
forensic and toxicological halves, converting a recovered residue into an
absorbed dose the toxicology models can act on.

The design honours the BOND suite contract: the domain core is pure and
importable without bond-api, the mission adapter implements the frozen
protocol, every metric flows into the manuscript through
`src/no_time_to_die/manuscript_variables.py`, and the whole assessment is
deterministic and fully tested. A reader can open any function named in
[Methodology](#methodology) and trace it to its source file in seconds.

## Methodology

This section specifies the mathematics of each concept module. All functions
are pure, side-effect-free, and deterministic; the canonical demonstration
inputs live in `src/no_time_to_die/demo.py` and are shared verbatim by the
mission adapter and the manuscript variable generator so outcomes cannot
drift.

### DNA-targeted bioweapon countermeasure (`bioweapon_counter.py`)

**Specificity.** For a guide `g` and a reference genome `r`, every
length-`|g|` window of `r` is scored by Hamming distance `d(g, w)`. A window
at distance 0 is an on-target hit; a window at distance in `[1, k]` is an
off-target hit representing a mis-address risk. Specificity is the share of
hits that are on-target:

```
specificity = on_target / (on_target + off_target)
```

`select_best_guide` chooses the candidate maximizing specificity, ties broken
by first-in-order for determinism.

**Delivery.** The one-compartment bateman equation models plasma concentration
after an absorbed dose:

```
C(t) = dose * k_a/(k_a - k_e) * (exp(-k_e t) - exp(-k_a t))
```

with `k_a` the absorption rate and `k_e` the elimination rate
(`plasma_concentration`). The absorbed fraction at exposure time `t` is
`fraction_delivered = 1 - exp(-k_a t)`.

**Countermeasure efficacy.** `neutralization_probability` combines specificity,
delivered fraction, and a saturating avidity term:

```
P = specificity * delivered_fraction * avidity/(1 + avidity)
```

clamped to `[0, 1]`, so any near-zero component drives neutralization to zero.

### Poison-garden toxicology (`toxicology.py`)

Each flora toxin is a Hill dose–response hazard with LD50 and slope `n`
(`PlantToxin`). The fraction of a population affected at dose `d` is

```
f(d) = d^n / (d^n + LD50^n)
```

with analytic inverse `dose_for_fraction`. A mixture of agents combines under
response addition — the system is unaffected only if every agent misses:

```
F = 1 - prod_i (1 - f_i(d_i))
```

The `TOXIN_CATALOG` records `7` botanical toxins spanning
LD50 from 0.8 to 10.0 mg/kg (median
1.5), each with a botanical source, a commonly-cited
order-of-magnitude LD50 recorded without a specific citation, and a Hill slope
that is **not** sourced at all — the slopes are curve-shape parameters invented
for this demonstration, registered as such in `data/claim_ledger.yaml`.
`catalog_stats` reports that summary over any catalog, and the forensic spectral
library profiles `5` poisons for identification.

### Poison-delivery forensics (`delivery_forensics.py`)

A residue signal `S` with root-mean-square noise `N` yields
`snr = S/N`. Detection confidence under a logistic model with limit of
detection `lod` is

```
confidence = 1 / (1 + exp(-(snr - lod)))
```

Concentration is back-computed from a linear calibration `S = m·C + b`. Signals
below the *intercept* `b` clamp to zero, because the inverted line would
otherwise return a negative concentration. That clamp is not a limit-of-detection
test and `estimate_concentration` has no knowledge of the LOD: with the
demonstration's `b` = 0.5 and an LOD SNR of
3.0, a signal of 1.0 lies well below the limit of detection yet
still returns a positive concentration. Deciding whether a signal is real is
`detection_confidence`'s job. (Earlier revisions of this section and of the
function docstring said "sub-LOD signals clamp to zero", conflating the two; the
suite now pins the below-LOD-yet-positive case.) The transferred dose is
`concentration · volume · transfer_fraction` (`recovered_dose`), and an unknown
residue spectrum is identified by cosine similarity against the reference
library (`match_unknown`). The demonstration operates at a
limit-of-detection SNR of `3.0`.

**Mixture decomposition.** A residue that is itself a blend is decomposed into
non-negative mixing fractions rather than ranked against a single entry
(`decompose_mixture`, a two-component non-negative least-squares fit in the
spirit of Lawson and Hanson 1974): the unknown spectrum is approximated as
`sum_k w_k s_k` with `w_k >= 0` and `sum_k w_k = 1`, and the 1- or 2-component
candidate with the smallest squared residual wins. A pure single poison is
returned as a one-element decomposition; weights are *mixing fractions* (they
sum to 1), and the squared residual measures how much of the unit-fraction
model the spectrum does not explain. `mixture_analysis` composes this into the
primary/secondary components and residual consumed by the demo and tokens.

### Guide design and population off-target (`targeting_design.py`)

The countermeasure guide is not given — it is *designed*. `gc_content` and
`longest_homopolymer` are base sequence descriptors; `guide_efficiency`
combines a GC-content sweet-spot penalty, a homopolymer-run penalty, and an
optional position-dependent nucleotide bonus into a Doench-style activity
score in `[0, 1]` (spirit of Doench et al. 2014).

Off-target burden is assessed *across a population* of reference genomes:

```
off_target_risk = sum_{genomes} sum_{windows, 1<=d<=k} exp(-lambda * d)
```

where `d` is the Hamming distance of a mismatched window and `lambda` the
mismatch decay (`population_off_target_risk`). `rank_guides` scores each
candidate as `efficiency * (1 - min(1, off_target_risk))` and `design_report`
returns the ranked table plus the best guide. The demonstration ranks
`4` candidates against the reference genome.

### Antidote screening (`antidote_screening.py`)

A poison-garden toxin is acted on through a receptor; a competitive
antagonist counteracts it. The apparent IC50 of a competitive antagonist
follows Cheng–Prusoff (1973):

```
IC50_app = Ki * (1 + [S] / Km)
```

with the toxin dose `[S]` and its LD50 standing in as the affinity proxy
`Km`. The fraction of receptors occupied is the Langmuir isotherm
`[A] / ([A] + IC50_app)` (`fraction_antagonized`). `screen_antidotes` ranks a
library of `5` entries by the survival they restore
against a toxin dose:

```
residual = f_tox * (1 - f_antag); survival = 1 - residual
```

The `Ki` values fed to this model are invented, not published — see
[Scope](#scope-and-related-work). The relation and the isotherm are real and are
tested against hand-checkable values; the library entries are illustrative
inputs named after real drugs, and the model is applied uniformly to all five
regardless of whether the real drug is a competitive antagonist. `screen_report`
also reports the *challenge* therapeutic window `toxin LD50 / dose` and margin
of safety `window - 1` — a screening context (how far the administered dose sits
from the population-lethal level), not a clinical dosing index.

### Exposure assessment (`exposure_assessment.py`)

The hazard of a delivered poison is set by the absorbed dose, not the residue.
`absorbed_dose = concentration * contact_rate * duration * absorption_fraction`
models intake through an exposure pathway; `cumulative_exposure` accumulates
body burden under first-order elimination
`(intake_rate / k_e) * (1 - exp(-k_e t))`; `margin_of_exposure` computes
`NOAEL / absorbed` (NRC 1983 framing) and `risk_quotient` computes
`absorbed / reference_dose`. `exposure_scenario_report` composes these into a
single verdict (acceptable vs elevated risk).

## Results

All results below are computed live from `src/no_time_to_die/demo.py` by
`src/no_time_to_die/manuscript_variables.py`; none are hand-authored. The
deterministic demonstration uses a fixed 144-nucleotide
reference assembled from 9 labelled segments, a
4-guide candidate set, seed `11`, and a
fixed 4.0 h exposure window (canonical input digest
`cb8fe93a43fc`).

**What these numbers do and do not establish.** The reference genome is a
constructed input with a known planted structure
(2 exact on-target windows,
3 near-misses at declared Hamming distances). The
results therefore establish that the models *recover a structure that was put
there*, and that they discriminate between candidates — not that they would
perform this way on a real genome. What they specifically no longer do is
recover a result the input made inevitable: through 2026-08-04 the reference
was `AACCGGTTAACCGGTT` repeated four times, a period-16 string scanned by a
16-nt guide, so 100% specificity, zero off-target windows, and zero population
off-target risk were arithmetic consequences of the input rather than findings.
Those degenerate outcomes are now failing conditions in the suite.

### Countermeasure demonstration

`select_best_guide` selects guide `AACCGGTTAACCGGTT`
(16 nt), which attains a target specificity of
**66.67%** — **2** on-target windows
against **1** off-target near matches (within
2 mismatches) in the demonstration reference. The
specificity sits strictly inside (0, 1): the selector separates the planted
exact hits from the planted near-misses rather than reporting a perfect score
the reference could not have contradicted. Combined with a delivered fraction of
**99.18%** and a saturating avidity term (avidity
3.0), the HERACLES neutralization probability is
**49.59%**.

The delivery kinetics (one-compartment bateman model) are rendered in
[Figure.

![HERACLES one-compartment delivery kinetics over a
12.0 h horizon (absorption rate
1.2 h⁻¹, elimination rate
0.4 h⁻¹), with the
4.0 h exposure window
marked.](output/figures/no_time_to_die_delivery_kinetics.png)

### Guide-design ranking

Across the `4` demonstration candidates, `design_report`
selects guide `AACCGGTTAACCGGTT` with an efficiency score of
**100%**, a population off-target risk of
**0.3679** over the reference genome, and a composite score
of **63.21%**.

The blend is what decides the ranking here, which is the point of reporting it.
Two candidates tie at the maximum efficiency of 100%; their composite scores do
not, because the reference plants near-miss windows for one of them and fewer
for the other. The winner's own composite is strictly below its efficiency —
the `efficiency * (1 - off_target_risk)` term erodes it by a non-zero amount.
Under the previous reference every candidate scored exactly zero off-target
risk, so the composite reduced to the raw efficiency, the two leaders tied at
1.0, and the "winner" was chosen by the alphabetical tie-break. The suite now
fails if the off-target term goes inert or the top two tie again.

The efficiency landscape (vs GC content) is rendered in [Figure.

![HERACLES guide-design efficiency across the candidate
set.](output/figures/no_time_to_die_guide_efficiency.png)

### Poison-garden catalog

The `7`-toxin catalog spans LD50 0.8 to
10.0 mg/kg, median 1.5 mg/kg.
Dose–response curves for every flora member are rendered in
[Figure. A garden-risk mixture of ricin, nicotine, and cyanide
combines under response addition to affect **42.12%** of
an exposed population.

![Poison-garden Hill dose–response curves across the catalog
flora.](output/figures/no_time_to_die_toxicology_dose_response.png)

### Antidote screen

Against a ricin dose at an antagonist concentration of
10.0 mg/L, the `5`-antidote
library is ranked by restored survival. The best antidote is
**naloxone**, restoring a survival probability of
**98.87%** by antagonizing **94.34%**
of the toxin's receptor occupancy. The *challenge* is put in context by the
therapeutic window — the toxin LD50 sits **2** times above the
administered dose, a margin of safety of **1** — so the dose the
screen confronts is comfortably below the population-lethal level (see
[Scope](#scope-and-related-work) for what this ratio is and is not).

This ranking is a property of the arithmetic, not of pharmacology. Every `Ki`
in the library is invented (see [Scope](#scope-and-related-work)); three of the
five named agents are not competitive receptor antagonists at all, and the
Cheng–Prusoff model is applied to them anyway. The result demonstrates that the
screen orders a library correctly given inhibition constants; it says nothing
about which of these drugs would help against ricin. The competitive-antagonist
dose–response for the library is rendered in [Figure.

![Competitive-antagonist antidote response
curves.](output/figures/no_time_to_die_antidote_response.png)

### Exposure assessment

For the demonstration Vesper pathway, the absorbed dose is
**0.06** (mass units), a cumulative body burden of
**0.019**, a margin of exposure of **8.333**, and a
risk quotient of **60** against the reference dose
0.001 — a verdict of **elevated risk**. The
margin of exposure exceeds unity against the NOAEL 0.5 —
the intake sits below the lethality threshold — yet the risk quotient also
exceeds unity, which is precisely the discordance the verdict rule is written
to catch: an intake far below the lethality threshold can still sit far above
the reference dose, and the verdict follows the stricter of the two.

### Vesper trace forensics

At a limit-of-detection SNR of `3.0`, the demonstration signal
(9.0 against RMS noise 1.0, giving SNR
**9**) is detected with **99.75%**
confidence. The calibration model back-computes a residue concentration of
**4.25** (the calibration inversion is clamped at the
calibration intercept, not at the limit of detection — see
[Methodology](#methodology)), and applying the
0.1 transfer fraction over 0.5 mL
gives a transfer-corrected residue dose of **0.2125**
(arbitrary mass units) on the glass. Spectral matching against the
`5`-entry reference library identifies the residue as
**ricin**. Detection confidence vs signal-to-noise is rendered
in [Figure.

![Vesper trace detection confidence vs signal-to-noise against the
limit of detection.](output/figures/no_time_to_die_detection_confidence.png)

#### Mixture decomposition

A residue that is a *blend* of two garden poisons grades as a mediocre single
match under cosine similarity, which is what a blend really is. When the
recovered spectrum is the demonstration's **ricin** +
atropine mix, `decompose_mixture` recovers the
non-negative mixing fractions by least squares over 1- and 2-component
candidates: a primary **60%** + secondary
**40%** split with a squared residual of
**1.329e-32** (see [Methodology](#methodology)). The
decomposition is a *model*, not an instrument read: it recovers the planted
blend because the blend was put there, exactly as the specificity and guide
results recover planted structure (see [Scope](#scope-and-related-work)).

## Conclusion

No Time to Die: HERACLES — Special-Agent Mission Software demonstrates that the three central threats of *No Time to
Die* (2021) — a DNA-targeted bioweapon, a poison garden, and delivery
forensics — can be expressed as a single deterministic, fully-tested
computational core under the BOND suite contract.

The package delivers **6** concrete claims — one per
domain module — each verified by real computation rather than assertion:

1. A target-specific countermeasure can be selected and its neutralization
 probability bounded by specificity, delivered fraction, and avidity
 (`bioweapon_counter.py`).
2. A guide can be *designed* and ranked by a Doench-style efficiency blended
 with population off-target burden (`targeting_design.py`) — with the blend
 doing real work: it separates two candidates that tie at maximum efficiency,
 and it erodes the winner's own score by a non-zero off-target term.
3. A poison-garden flora catalog can be profiled as Hill-curve hazards and
 combined under response addition (`toxicology.py`).
4. A competitive-antagonist antidote can be screened against a toxin dose by
 Cheng–Prusoff pharmacology and restored survival
 (`antidote_screening.py`).
5. A delivered exposure can be assessed through pathway intake, cumulative
 burden, margin of exposure, and risk quotient (`exposure_assessment.py`).
6. A delivered poison leaves a structurally detectable and identifiable
 residue on the vessel (`delivery_forensics.py`).

The domain core is infrastructure-free and importable without bond-api; a thin
adapter implements the frozen `MissionProvider` protocol, and every metric
flows into the manuscript through the shared `demo.py` + `manuscript_variables.py`
path, guarded by `check_demo_completeness` so a renamed result key fails the
build rather than silently hydrating a zero. This is the reference film pattern
for the remaining BOND suite packages.

The clearest limitation is the one the [Scope](#scope-and-related-work) section
names: nothing here is a measurement. Most constants are invented for this
demonstration; the rest are commonly-cited order-of-magnitude figures carried
without a citation. The demonstration therefore supports claims about the
*method* — that these threats admit deterministic, auditable, end-to-end
modelling — and not about any real toxin, guide, or instrument. Two concrete
cases: a margin of exposure of 8.333 against a risk quotient of
60 is a statement about the demonstration's chosen NOAEL and
reference dose, not about anyone's actual risk; and the antidote ranking is a
statement about the arithmetic of Cheng–Prusoff over five invented inhibition
constants, not about which drug to reach for.

A second limitation is structural and worth stating in its own right: the
reference genome is a constructed input whose on-target and near-miss windows
were placed deliberately. The countermeasure and guide-design results measure
**recovery of a planted structure**, which is a weaker claim than performance on
an unseen genome and a stronger one than the package could previously make at
all — the earlier periodic reference made its own headline numbers arithmetically
inevitable.

## Experimental Setup

### Software environment

- Python 3.14.6 (host), NumPy for the delivery/figure numerics,
 matplotlib (Agg backend) for figure rendering, PyYAML for config loading.
- Repository tree: isolated local-only package rooted at
 `projects/working/bond/no_time_to_die`; a local path dependency on the frozen
 `bond-api` protocol.

### Deterministic demonstration parameters

Canonical inputs live in `src/no_time_to_die/demo.py` and
`manuscript/config.yaml`. Every value below is a resolved token read from those
constants at hydration time, so the table cannot drift from the code that runs:

| Parameter | Value |
| --- | --- |
| Reference genome length | 144 nt (9 labelled 16-nt segments) |
| — exact on-target windows planted | 2 |
| — near-miss windows planted | 3 |
| Guide candidates | 4 |
| Guide length | 16 nt |
| Off-target tolerance `k` | 2 |
| Absorption rate `k_a` | 1.2 h⁻¹ |
| Exposure time | 4.0 h |
| Avidity | 3.0 |
| Antidote antagonist concentration | 10.0 mg/L |
| Exposure pathway — concentration | 0.02 |
| Exposure pathway — contact rate | 0.5 |
| Exposure pathway — duration | 30.0 |
| Exposure pathway — absorbed fraction | 0.2 |
| Exposure pathway — elimination rate `k_e` | 0.1 |
| Exposure pathway — NOAEL | 0.5 |
| Exposure pathway — reference dose (RfD) | 0.001 |
| Forensic signal / RMS noise | 9.0 / 1.0 |
| Forensic residue volume | 0.5 mL |
| Forensic transfer fraction | 0.1 |
| Forensic calibration slope `m` / intercept `b` | 2.0 / 0.5 |
| Limit-of-detection SNR | 3.0 |
| Catalog flora | 7 |
| Forensic library | 5 |
| Domain modules | 6 |
| Seed | 11 |
| Canonical input digest (sha256, first 12) | `cb8fe93a43fc` |

All are fixed at import. No module in the package imports a clock or an RNG
(structurally enforced — see [Reproducibility](#reproducibility)), so two runs
on one interpreter render byte-identical artifacts. The single host-dependent
value in the whole package is the `PYTHON_VERSION` token above.

The reference genome is not an arbitrary or periodic string. It is assembled
from labelled segments — 2 exact copies of the
target guide, 3 near-miss windows at declared
Hamming distances, and neutral fillers — precisely so the specificity and
off-target results are *measured against a known planted structure* rather than
forced by the input. The earlier reference was `AACCGGTTAACCGGTT` repeated four
times, whose period equalled the guide length; that reference could only ever
return 100% specificity, zero off-target windows, and zero population
off-target risk, so those numbers carried no information. See
[Results](#results).

### Figure generation

Figures are rendered deterministically by `src/no_time_to_die/figures/plots.py`
under a headless `Agg` backend to `output/figures/`. Each renderer reads the
same `demo.py` constants as the mission and the manuscript tokens, so a figure
cannot annotate a parameter the demonstration does not use:

- `delivery_kinetics.png` — bateman plasma-concentration curve over a
 12.0 h horizon, marking the
 4.0 h exposure window.
- `toxicology_dose_response.png` — Hill curves for the full catalog.
- `guide_efficiency.png` — guide-design efficiency vs GC content.
- `antidote_response.png` — competitive-antagonist dose–response, marking the
 10.0 mg/L demonstration dose.
- `detection_confidence.png` — logistic detection confidence vs SNR against the
 3.0 limit of detection.

## Reproducibility

This package treats reproducibility as a hard constraint enforced by tests, not
a prose promise. Every guarantee below names the test that would fail if it
stopped holding.

### Deterministic computation

No module under `src/` imports a clock, a random-number generator, or any other
entropy source, and the package makes exactly one environment read in total —
`platform.python_version`, rendered as the `PYTHON_VERSION` token. That is a
structural property, checked structurally: `tests/test_determinism.py` parses
every source file and fails on a forbidden import or an unsanctioned
environment read, and its positive controls confirm the scan reports a
reintroduced `datetime` or `random` import rather than passing silently.

Two consequences, stated precisely:

- **On one interpreter, two runs render byte-identical artifacts.** The byte
 gate renders the whole manuscript tree twice and compares every file byte for
 byte.
- **Across interpreter versions, exactly one substring differs** — the
 `PYTHON_VERSION` token. This is the single host-dependent value in the
 package; nothing else varies with the machine.

Through 2026-08-04 this section claimed byte-reproducibility while the
generator stamped `datetime.now(timezone.utc)` into both
`output/data/manuscript_variables.json` and this rendered section, so
consecutive runs demonstrably differed. The token was removed rather than
reworded, and the value gate now fails on any rendered token shaped like a date
or a clock time.

All demonstration inputs are fixed constants in `src/no_time_to_die/demo.py` and
`manuscript/config.yaml`; seed `11` is stable, though no code
path draws from an RNG, so it currently governs nothing and is recorded for
provenance only. The mission outcome carries a `Provenance` record with the
package version, the seed, and a sha256 `input_hash` over the canonical inputs
(`demo.input_hash`, currently `cb8fe93a43fc…`). That digest covers
every demonstration constant — an earlier version hashed only five of sixteen —
and the suite scans `demo.py` independently to fail if a newly added constant is
left out of it.

Figure renderers read the same `demo.py` constants as the mission and the
tokens. This is enforced, not asserted: each figure is composed by a
`build_*_figure` function the tests inspect directly, checking the plotted
series and the annotation positions against the constants the captions quote.
Five of the seven figure tests previously asserted only that a PNG was
non-empty, which a blank or wrong-data figure passes.

### Live manuscript metrics

Every numeric value in the prose sections flows through a resolved `HERACLES_*`
token from `src/no_time_to_die/manuscript_variables.py`, computed from the
shared demo result; none are hand-authored. Three gates protect this:

1. `check_demo_completeness` fails if the demo result is missing any key the
 tokens read — including the top-level `garden_risk_combined`, which the
 section-keyed scan was structurally blind to until 2026-08-05 (deleting it
 passed the gate and then raised a bare `KeyError`). The suite's positive
 control now deletes *every* key of a real demo result in turn and requires
 each deletion to surface as a named gate failure rather than as any other
 exception.
2. The token cross-reference test scans `manuscript/[0-9]*.md` and fails if any
 `{`-delimited token is not produced by `generate_variables`.
3. `z_generate_manuscript_variables.py` fails in strict mode on any token left
 unresolved after substitution.

### Evidence provenance

`data/claim_ledger.yaml` registers every numeric constant the demonstration
consumes, with its live value and one of two provenance classes: `synthetic:
true` (invented for this demonstration) or `synthetic: false` (a commonly-cited
order-of-magnitude figure for a real substance, recorded without a specific
citation). `tests/test_claim_ledger.py` derives the expected constant set from
the modules themselves, so an unregistered constant, an orphaned entry, or a
value edited on one side only all fail the build. Nothing here is a
measurement.

### Verification commands

From the package root:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/ tests/ && uv run ruff format --check src/ scripts/ tests/
uv run mypy src/ scripts/
## Lineage gate — pattern is bracket-split so this doc cannot trip its own
## check (template[_]code_project resolves to the literal string when run).
rg -n "template[_]code_project". --glob '!uv.lock' --glob '!.git/**' \
 --glob '!output/**' || echo Clean
git diff --exit-code # clean tree after regeneration
```

The suite enforces ≥90% line+branch coverage on `src/` and zero mocks. Rendered
under Python 3.14.6.

## Scope and Related Work

### Scope

This package models the *computational* skeleton of the HERACLES narrative arc
in *No Time to Die* (2021). It does **not** claim biological fidelity to a
real bioweapon, a real pharmacology database, or a real analytical instrument.
**Nothing in this package is a measurement.** The value is in the *method* —
reproducible, task-appropriate modelling with auditable provenance — not in the
specific constants.

Every constant is registered in `data/claim_ledger.yaml` under one of exactly
two provenance classes, and the split matters:

- **Invented for this demonstration** (`synthetic: true`): the DNA reference and
 guide set, all seven Hill slopes, the forensic spectral fingerprints and the
 unknown spectrum, the guide-design model parameters, every demonstration
 scenario parameter, and **all five antidote `Ki` values**.
- **Commonly-cited order-of-magnitude figures for real substances**
 (`synthetic: false`), recorded without a specific citation and used as
 plausible calibrants rather than as data: the seven LD50 values and the
 conventional limit-of-detection SNR of 3.

#### Withdrawn claim: the antidote inhibition constants

This is worth naming rather than burying in a table. Through 2026-08-04 the
ledger labelled all five antidote `Ki` values "Published approximation, *drug*
Ki" and left them unflagged, placing them on the measured side of the ledger's
own distinction, and the module docstring called them
"published-approximation inhibition constants". That was false. No publication
reports these numbers, and two independent facts make it impossible that any
could:

- Naloxone and flumazenil bind their receptors at nanomolar affinity. The
 recorded 0.4 and 1.0 mg/L are not those quantities in any unit system.
- Pralidoxime reactivates phosphorylated acetylcholinesterase, acetylcysteine is
 a glutathione precursor, and vitamin K is a cofactor in an enzymatic cycle.
 None is a competitive receptor antagonist, so none has a `Ki` of the kind the
 Cheng–Prusoff relation consumes. The model is applied to them uniformly
 regardless — a property of this demonstration, not of the pharmacology.

The values are now marked `synthetic: true` with honest source labels, and
`tests/test_claim_ledger.py` fails if any is re-flagged as measured. The
antidote screen therefore demonstrates that the ranking arithmetic is correct,
and demonstrates nothing about clinical antidote choice.

Boundaries kept deliberately out of scope:

- No simulation of DNA damage or clearance pharmacology beyond the
 one-compartment delivery model.
- No instrument noise model beyond additive RMS noise.
- No claims of real-world forensic admissibility.
- No claim that any model would behave this way on a real genome, patient, or
 instrument. The reference genome is a *constructed* input with a planted,
 documented structure; the results measure recovery of that planted structure.

#### Uncertainty and limitations (round-2 additions)

Three quantities introduced or re-exposed in round 2 carry their own,
explicit uncertainty:

- **Mixture mixing fractions.** `decompose_mixture` reports weights that are
 a *fit*, not a measurement. They are exact here only because the 5-bin
 fingerprints are noiseless and the blend was planted; on a real residue the
 weight estimates would carry instrument noise, unknown transfer, and
 library incompleteness that no model in this package captures. The residual
 token reports the fit's unexplained variance, and the weights sum to one by
 construction (they cannot express a missing third component or an absolute
 recovered amount).
- **The challenge therapeutic window.** `HERACLES_WINDOW` is the ratio of the
 toxin LD50 to the administered demo dose. It is arithmetic context, not a
 pharmacology finding: the LD50 is itself an order-of-magnitude figure with
 no citation (see the `synthetic`/`synthetic: false` split in
 `data/claim_ledger.yaml`), the dose is a synthetic input, and a real
 therapeutic window depends on route, species, and formulation the ratio
 does not model. The margin is consequently not a clinical safety margin.
- **The LD50 values remain uncited.** Per the ledger contract, `synthetic:
 false` means ``a commonly-cited order-of-magnitude figure … recorded without
 a specific citation`` — a provenance *label*, not a reference. This round
 deliberately did **not** fabricate bibliographic entries to fill the seven
 `ld50_*` `citation:` fields; sourcing each to a specific publication is
 recorded as open work in `TODO.md` rather than papered over.

### Related work

The package extends the BOND suite pattern established by `bond-api` (the
frozen mission protocol), `bond-orchestrator` (the DAG runner), and
`bond-utilities` (Layer 0 provenance/cipher utilities), each converted from a
template exemplar scaffold under the shared 90%-coverage, zero-mock,
thin-orchestrator contract. The engineering contract is inherited from the
suite's other film packages; what is specific here is the domain lineage.

Each model is a deliberately simplified, deterministic instance of a
well-established published method rather than an invention of this package:

- **Dose–response** follows the Hill equation [@hill1910possible]; mixtures
 combine under Bliss independent action / response addition
 [@bliss1939toxicity].
- **Guide activity and off-target burden** follow the feature-based sgRNA
 design rules of Doench et al. [@doench2014rational] and the mismatch-tolerance
 characterization of Hsu et al. [@hsu2013dna], reduced here to a transparent
 GC/homopolymer score and an exponential mismatch decay.
- **Delivery kinetics** use the one-compartment first-order absorption model
 usually attributed to Bateman [@bateman1910solution] and standard in
 pharmacokinetics texts [@gibaldi1982pharmacokinetics].
- **Mixture decomposition** is a non-negative least-squares fit in the spirit
 of Lawson and Hanson [@lawsonhanson1974].
- **Antidote pharmacology** uses the Cheng–Prusoff relation
 [@cheng1973relationship] over Langmuir occupancy [@langmuir1918adsorption].
- **Exposure and risk** follow the NRC risk-assessment framing
 [@nrc1983risk]; **limit-of-detection** reasoning follows Currie
 [@currie1968limits].

The simplifications are the point: each is small enough to test exactly against
a hand-checkable value, which is what makes the whole assessment auditable.

## Sources

@bond_api_2026; @bond_orchestrator_2026; @bond_utilities_2026; @hill1910possible; @no_time_to_die_2021; @doench2014rational; @hsu2013dna; @cheng1973relationship; @nrc1983risk; @bateman1910solution; @gibaldi1982pharmacokinetics; @langmuir1918adsorption; @bliss1939toxicity; @currie1968limits; @lawsonhanson1974


# Never Say Never Again (1983) — REPLAY

*film package · package codename REPLAY*. Mission **REMOUNT**: replay the legacy operation as a remount; diff the original vs remount outcomes; migrate the legacy intelligence assets; assess remount detection risk and mission reliability; allocate remastered assets by marginal gain; forecast the replay learning curve.

## Concepts — REPLAY: domain and operational focus

legacy remount, replay

## Abstract — REPLAY: mission summary

**Never Say Never Again: REMOUNT — Special-Agent Mission Software** (Replaying a legacy operation: op diff, intel migration, escalation risk, marginal-gain allocation, and replay learning, version 0.1.0) presents REMOUNT, a deterministic engine for *legacy mission replay*. When an operation is re-opened years after its original run, its scenario must be re-executed — as a *remount* — with remastered intelligence, its outcomes compared against the original, and its legacy assets migrated so they can be consumed safely again. Drawing on the 1983 film *Never Say Never Again* — itself a remount of the 1965 *Thunderball* operation (Never Say Never Again, mission codename REMOUNT) — the engine models each of 4 objectives through a smooth success curve over effective intel versus difficulty. The canonical replay yields an original command score of 0.3111 and a remount command score of 0.5161 (weighted delta +0.2050, overall verdict *improved*). Per-objective, the remount improves 4 objectives, regresses 0, and leaves 0 unchanged, lifting the count of fulfilled objectives from 1 to 3. The engine migrates 3 legacy intelligence dossiers (1 gadget, 2 intel), re-fingerprinting each (SHA-256) so the remount can verify integrity before consumption (catalog fingerprint 1a1e05c4f464). The remount is not costless. Replaying the op accumulates a detection hazard: over a campaign of replay operations the probability of alerting the adversary reaches 0.7769 (expected 4.00 operations before alert), while the mission's block-structured reliability is 0.9578 — a campaign expected value of +18.10. Scarce remastered assets are therefore allocated by marginal gain (6 assets deployed, 0.8030 of the saturation ceiling), and repeated rehearsal pushes the command score along an exponential learning curve toward 0.7010 (delta +0.3899, reaching the target by iteration 3). Everything computes deterministically — no random draws, no external calls — so the remount is reproducible to the byte on Python 3.14.6 (document date 2026-08-05). Every quantity above is a token injected from the running code; none is transcribed by hand. The models themselves are standard and cited, not invented here: the contribution is their deterministic, auditable composition into a single remount pipeline, evaluated at one canonical parameter set rather than calibrated against operational data.

## Introduction — REPLAY: mission framing, the operational problem, and how to read this chapter

### Never Say Never Again and the remount battalion

*Never Say Never Again* (1983) is a curious entry in the Bond canon: it is a
remake — a *remount* — of *Thunderball* (1965), produced without the Eon
series and starring a returning Bond. Rather than a new story it re-stages an
old one, modernized and re-equipped. This is precisely the operational meaning
of a **legacy mission remount**: keep the objective set, refresh the resources,
and re-run the scenario against the current threat model.

REMOUNT (REMOUNT, package 0.1.0) operationalizes
that idea as software for Never Say Never Again. Its pure domain core provides seven capabilities in as many modules — six
that compute the remount and a seventh that checks how much those six can be
believed at parameter values the model did not assume:

1. **Legacy mission replay** (`mission_replay.py`) — deterministically re-run a
 prior operation's scenario under a remount configuration.
2. **Op diff** (`op_diff.py`) — compare the original outcome against the
 remount, per objective and in aggregate.
3. **Legacy asset migration** (`legacy_assets.py`) — carry forward,
 re-fingerprint, and verify the intelligence assets the remount consumes.
4. **Remount risk** (`remount_risk.py`) — price the re-op: the detection hazard
 that accumulates across replays, the block-structured mission reliability,
 and the resulting campaign expected value.
5. **Asset allocation** (`asset_allocator.py`) — spend a scarce budget of
 remastered assets across objectives by marginal gain.
6. **Replay learning** (`learning_curve.py`) — forecast how far repeated
 rehearsal can push the command score, and when it stops paying.
7. **Sensitivity** (`sensitivity.py`) — sweep each of the three model
 parameters the conclusions rest on and report the sub-range over which the
 two headline conclusions still hold, so the reader knows how much to trust
 them rather than taking a single point as given.

The first three answer the operative question of any re-op: *is the remount
actually an improvement, and can we trust the intel it relied on?* The last
three answer the question that follows immediately: *and is it worth running at
all, given what a replay costs and what rehearsal can still buy?* A remount
that improves the command score can still be a bad operation if the accumulated
detection hazard outweighs the gain — so the engine reports both halves rather
than only the flattering one.

### Why determinism

A remount is an audit as much as an operation. Every number produced —
command score, objective delta, asset fingerprint — must be reproducible by an
independent reviewer without re-running the whole suite. The engine therefore
makes **no random draws and no external calls**: its success model is a fixed
Logistic curve, its hashing is canonical SHA-256, and two runs under the same
inputs are byte-identical.

## Methodology — REPLAY: the analytical models and algorithms that drive the mission

### Scenario model

A scenario is an ordered set of 4 objectives, each a tuple of
`objective_id`, a positive `weight`, a `difficulty` in [0, 1], and a
`baseline_intel` in [0, 1]. The canonical dataset, `THUNDERBALL-65` (see
`mission_replay.py`), reopens the 1965 operation. Weights need not sum to one;
they are normalized when the command score is formed.

### Remount configuration

A remount applies three deltas (`RemountConfig`):

- `intel_bonus` — extra effective intel added to every objective (reinforced
 intelligence).
- `doctrine` — a multiplicative factor on effective intel (doctrine/doctrine
 adjustments).
- `realism_ceiling` — a cap on effective intel so optimistic assumptions
 cannot overwhelm the model.

The effective intel for an objective is `clamp((baseline + bonus) * doctrine,
0, realism_ceiling)`.

### Success model

For each objective the engine computes a deterministic success score with the
logistic (Verhulst) curve [@verhulst1838notice]:

$$\text{score}(\Delta) = \frac{1}{1 + e^{-S\,\Delta}}, \qquad \Delta =
\text{eff\_intel} - \text{difficulty}$$

where `S` is the sensitivity (default 6). A score at or
above the `success_threshold` (default 0.5) counts the
objective as *achieved*. The command score is the weight-weighted mean of
per-objective scores. The implementation evaluates the curve in its
numerically stable branched form (`exp(z) / (1 + exp(z))` for negative `z`) so
that a large negative margin cannot overflow.

The choice of `S` is a modelling choice, not a fitted parameter: it sets how
sharply an intel surplus converts into success, and no operational data is used
to calibrate it.

### Op diff

Given the original and remount replays, `diff_outcomes` aligns objectives by id
(in the original's order) and computes each objective's `delta` and a verdict:
`improved` when `delta > epsilon`, `regressed` when `delta < -epsilon`, else
`unchanged`. The aggregate `weighted_delta` reuses the original scenario's
objective weights, and the overall verdict follows the sign of
`weighted_delta`.

### Remount risk (escalation hazard and reliability)

`remount_risk.py` models the price of a replay. Detection follows a memoryless
exponential (Poisson) hazard [@ross2019probability] —
`P(alert within N replays) = 1 - exp(-rate * N)` with expected operations
before alert `1 / rate` — so repeated replays monotonically raise the chance of
alerting the adversary. Mission success is
modeled as a reliability block diagram: a *series* of *parallel* blocks, where
each block (intel acquisition, insertion, extraction) succeeds if any of its
redundant paths succeeds [@barlow1975reliability]. The campaign expected value
`P(success) * reward - P(detected) * penalty` then prices the whole replay
campaign.

### Asset allocation (marginal gain)

`asset_allocator.py` spends scarce remastered assets. The allocatable
objectives are *derived*, not re-declared: each takes its `objective_id` and
`weight` from the canonical scenario and its `base_score` from that objective's
real score in the remount replay. Only two numbers per objective are stipulated
model inputs — the improvement `cap` an asset can ultimately buy and the
efficiency `e` at which returns diminish — and no operational data calibrates
them. Because the base scores are replay scores and the scenario's weights sum
to one, the plan's weighted total is the replay's command score, and the gains
below are in command-score units rather than in a unit of their own.

Each objective has a concave improvement curve `cap * (1 - exp(-e * k))` in the
number `k` of assigned assets — strictly diminishing returns. A deterministic
greedy allocates each of the `budget` assets to the objective with the largest
**weight-scaled** capped marginal gain — the marginal increase in the weighted
score the plan actually reports — with ties broken by objective order.
Selecting on the unweighted gain instead maximizes a different function than
the one reported; that was a real defect in this module, and the test suite now
carries the wrong variant as a negative control.

The guarantee: the objective is a weighted sum of per-objective concave curves
in that objective's own asset count, which is the separable-concave special
case of monotone submodular maximization. There greedy incremental allocation
is not merely within the `(1 - 1/e)` factor that Nemhauser–Wolsey–Fisher
[@nemhauser1978submodular] guarantee in general — it is *exactly optimal*.
`tests/test_asset_allocator.py` verifies that on the canonical pool by
enumerating every way to split the budget across the objectives and comparing
against the maximum, and shows the unweighted variant failing the same check.

### Replay learning curve

`learning_curve.py` forecasts how rehearsal improves the remount. The command
score follows an exponential learning curve
`final - (final - initial) * exp(-rate * n)` from the baseline replay
(`initial`) toward a fully-reinforced replay asymptote (`final`)
[@wright1936learning]. Both endpoints are *computed*: each is a real replay of
the scenario through the same engine, under the identity config and under the
capped-bonus config respectively.

Inverting the curve gives the first iteration `n` reaching a target score,
`n = ceil(-ln((final - target) / (final - initial)) / rate)`. The solver returns
`None` — target unreachable — whenever the asymptote is at *or below* the
target, since the curve approaches its asymptote without ever attaining it, and
whenever the rate is non-positive.

### Legacy asset migration

Each legacy dossier is a `LegacyAsset` carrying a declared SHA-256
[@nist2015fips180] integrity fingerprint. `verify` recomputes the fingerprint
over NFC-normalized [@unicode2023uax15] UTF-8 content and compares it to the
declared one (`None` = un-scanned, treated as self-consistent). Normalizing
before hashing is what makes the fingerprint a property of the *text* rather
than of one particular encoding of it. `remaster` migrates a source into
`version + 1` with fresh content, optionally reclassifying/re-typing it, and
recomputes the fingerprint; by default it refuses to migrate a source that
fails its own integrity check, raising `AssetIntegrityError` rather than
propagating a suspect dossier. An `AssetCatalog` aggregates assets, verifies
them wholesale, and migrates a subset in a single deterministic batch. The
canonical index the remount actually consumes is `LEGACY_INDEX`, exposed
through `canonical_catalog` so the mission, the manuscript, and the figures
share one definition of the migration.

### Sensitivity analysis

`sensitivity.py` asks how much of the above to believe. The two headline
conclusions — that the remount improves over the original (`(a)`), and that a
short campaign still pays (`(b)`) — are produced at a single canonical
parameter set. This module sweeps each of the three parameters the conclusions
rest on over a declared range, holding the other two at their canonical values,
and reports the largest contiguous sub-range containing the canonical value over
which *both* conclusions hold. `(b)` is evaluated through the same
:func:`optimal_campaign_length` the risk model exports, so the analysis and the
headline crossing are one object, not a parallel derivation [@saltelli2008sensitivity].

* `[0.5, 20]` — the success-curve sensitivity `S`;
* `[0.05, 1]` — the per-replay detection rate;
* `[0.05, 1]` — the per-replay learning rate.

Because the learning rate feeds neither the op diff (`(a)`) nor the campaign
expected value (`(b)`), its robust sub-range spans the whole declared sweep by
construction; that insensitivity is a reported result, not a gap. The analysis
is one-dimensional — it perturbs one parameter at a time rather than sampling
the joint space — which is appropriate for binding two specific conclusions but
is not a general global-sensitivity decomposition.

## Results — REPLAY: measured outcomes, headline numbers, and what they establish

### Command score

Replaying the canonical `THUNDERBALL-65` scenario under the identity config
(original) and under `REMOUNT_CONFIG` (remount) gives:

| Metric | Original | Remount | Delta |
| --- | ---: | ---: | ---: |
| Command score | 0.3111 | 0.5161 | +0.2050 |
| Objectives fulfilled | 1 | 3 | +2 |
| Overall verdict | — | — | *improved* |

The remount raises the weighted command score from 0.3111
to 0.5161, a weighted delta of +0.2050. Per
objective, 4 improve, 0 regress, and
0 are unchanged.

**Figure — original versus remount objective scores.**

![Op diff — original versus remount objective scores](output/figures/never_say_never_again_op_diff_scores.png)

The grouped bar figure (rendered by `src/never_say_never_again/figures.py`
into `output/figures/op_diff_scores.png`) shows each objective's score under
the original and remount configs. The remount's reinforced intel pushes every
objective's score upward.

### Legacy asset migration

The engine migrates 3 legacy intelligence dossiers
(1 gadget, 2 intel), each re-fingerprinted on migration. The
catalog-wide stable fingerprint — the SHA-256 over the sorted
`(id, kind, content-digest)` rows, truncated for display — is
`1a1e05c4f464`. Migration is refused outright when a source dossier's
declared fingerprint does not match its content, so a tampered legacy record
cannot silently enter the remount.

![Migrated asset distribution](output/figures/never_say_never_again_asset_distribution.png)

### Remount risk

Over a campaign of 6 replay operations at a per-replay
hazard of 0.25, the accumulated detection probability
reaches 0.7769 (expected
4.00 operations before the first alert), whereas the
block-structured mission reliability is 0.9578. At the canonical
reward 100 and penalty 100 the
campaign expected value is +18.10.

The sign of that expected value is the whole argument. The model's own
crossing — the smallest replay count at which the expected value turns
non-positive — is 13 for the canonical parameters; the
canonical campaign length of 6 sits comfortably below
it, which is what "keep the remount short" means in numbers. Reliability is a
*constant* of the mission's block structure, while the detection term
`1 - exp(-rate * N)` rises monotonically in the replay count `N` toward 1. The
expected value is therefore strictly decreasing in `N`, and it crosses zero
once `reliability * reward` falls below `detection * penalty` — with the
canonical reward and penalty equal, simply once the accumulated hazard exceeds
the reliability. Past that crossing every additional replay is negative-value.
Both properties (strict decrease, and a crossing at the canonical parameters)
are asserted over the real model in `tests/test_remount_risk.py` rather than
argued in prose alone. This is the engine's central caveat to the remount
premise: *never say never again* — but do not keep saying it into a long
campaign.

### Asset allocation

Allocating the scarce remastered assets by marginal gain spends a budget of
6 across 4 objectives. The greedy
deploys 6 of them — it stops early if every objective
saturates — and recovers +0.2570 of weighted command score, i.e.
0.8030 of the full-saturation ceiling.

That figure is in genuine command-score units: the allocatable objectives carry
the scenario's own ids and weights, and each one's zero-asset base score *is*
its score in the remount replay reported above, so the plan's zero-asset
baseline is the remount command score 0.5161 — displayed
here rounded, asserted at full precision in `tests/test_asset_allocator.py`
rather than left to the reader. What the allocation model stipulates, and what
no data here calibrates, is the pair of curve parameters per objective — how
much an asset can ultimately buy and how fast the returns diminish.

Because each objective's improvement curve is concave, the sequence of realized
marginal gains is non-increasing: the greedy spends its first asset where the
slope is steepest and each later asset buys strictly less. For this
separable-concave objective that makes the greedy exactly optimal, not merely
within the `(1 - 1/e)` factor of the general submodular bound — checked in
`tests/test_asset_allocator.py` against the maximum over every feasible split
of the budget, with the unweighted-selection variant failing the same check.

![Marginal-gain asset allocation](output/figures/never_say_never_again_asset_allocation.png)

### Replay learning curve

Forecasting repeated rehearsal at learning rate 0.4 over
8 iterations raises the command score from
0.3111 toward 0.7010 (delta +0.3899),
and the target score of 0.55 is first met at iteration
3.

The asymptote is not an assumption: it is a second real replay of the same
scenario under a fully-reinforced config (intel bonus 0.3), so
both ends of the curve are computed by the engine rather than posited. A target
at or above that asymptote is reported as unreachable rather than as met on the
first iteration — the curve approaches its asymptote but never attains it.

![Replay learning curve](output/figures/never_say_never_again_learning_curve.png)

### Sensitivity and robustness

The two headline conclusions above are each asserted at one sweep of a
parameter, not at a single point. `src/never_say_never_again/sensitivity.py`
sweeps each of the three parameters the conclusions rest on and reports the
largest contiguous sub-range containing the canonical value over which *both*
conclusions — remount improved [[`(a)`]] and campaign still pays [[`(b)`]] —
hold:

| Parameter | Sweep | Robust sub-range | Notes |
| --- | --- | ---: | --- |
| Success sensitivity `S` | [0.5, 20] | [0.500, 20.000] | conclusion (a) holds across the whole declared sweep (true = spans) |
| Detection rate | [0.05, 1] | [0.050, 0.527] | conclusion (b) breaks at high rate (false = spans) |
| Learning rate | [0.05, 1] | [0.050, 1.000] | affects neither (a) nor (b) (true = spans) |

![Sensitivity sweep — robust parameter sub-ranges](output/figures/never_say_never_again_sensitivity_sweep.png)

Interpretation. The remount-improvement conclusion is *not* a knife-edge of the
logistic steepness: it holds across the entire declared sensitivity sweep,
because the remount config raises effective intel on every objective regardless
of `S`. The campaign-still-pays conclusion is genuinely conditional: beyond a
detection rate of about 0.527 the accumulated
hazard crosses the mission reliability within the canonical campaign length,
and the expected value turns negative — so "keep the remount short" depends on
the adversary's per-replay acuity. The learning rate, by construction, fights
neither battle, and the analysis says so rather than pretending it does.

## Conclusion — REPLAY: findings, verdict, and what the mission establishes

REMOUNT (REMOUNT) demonstrates a clean, deterministic answer to
the legacy-mission re-open: re-run the scenario, diff the outcomes, and migrate
the intel. For the canonical `THUNDERBALL-65` remount the evidence is
unequivocal — the remount improves the weighted command score from
0.3111 to 0.5161 (delta
+0.2050, verdict *improved*) and migrates
3 assets with verified fingerprints.

Three lessons carry forward to any remount battalion:

1. A remount improves outcome when intel reinforcement outpaces difficulty.
2. Op diffs must weight objectives by their relative importance, not treat
 them equally.
3. Legacy assets must be re-fingerprinted before remount consumption — you
 cannot trust a dossier you never re-verified.

The deepened models add three more. A remount is not free: the accumulated
detection hazard over 4.00 expected operations
(0.7769 at campaign length) makes the campaign expected
value +18.10 and *falling* as replays grow — so the remount must
be decisive, not serial. Scarce remastered assets should follow marginal gain
(6 assets for 0.8030 of the saturation
ceiling) rather than intuition. And rehearsal follows a diminishing-returns
learning curve toward 0.7010 (delta +0.3899, target at
iteration 3), so the marginal replay eventually stops
paying.

The engine's determinism makes every one of these claims independently
auditable, and its purity (no `bond_api` imports in the domain core) keeps the
analysis reusable beyond the BOND suite.

What the package does *not* establish is equally worth stating. Every number
here is produced by the model at one canonical parameter set; none is a
measurement of a real operation. The success curve's sensitivity, the detection
rate, and the learning rate are chosen, not fitted — but the analysis in
`03_results.md` now reports over which sub-range of each the two headline
conclusions still hold, so the reader can see that the remount-improvement
result is robust to the logistic's steepness while the campaign-still-pays
result is conditional on the detection rate staying below about
0.527. The conclusions are therefore claims about
this model's behaviour — reproducible to the byte, robust where the analysis
shows them to be, and open to being falsified by anyone who reruns it — rather
than claims about the world. The full list of bounds is in the scope section.

## Experimental Setup — REPLAY: canonical scenarios, parameters, and configuration

### Canonical dataset

The `THUNDERBALL-65` scenario (`src/never_say_never_again/mission_replay.py`)
is the sole canonical dataset, declared as module-level deterministic
constants. It contains 4 objectives with fixed weights,
difficulties, and baseline intel, plus an identity config
(`intel_bonus = 0`) and the `REMOUNT_CONFIG` used for the remount. The
migration consumes a second canonical constant, `LEGACY_INDEX`:
3 legacy dossiers (1 gadget, 2 intel).

### Parameters

Every value below is a generated token read straight from the constant the code
runs on — this list cannot drift from the implementation.

- Success-model sensitivity `S = 6`, success threshold
 `0.5`.
- Remount intel bonus `0.15`, doctrine
 `1`, realism ceiling `1`.
- Deterministic seed `13` (provenance-only: the mission makes no
 random draws).
- SHA-256 fingerprints over NFC-normalized UTF-8 content.
- Risk: detection rate `0.25`/replay, campaign length
 `6`, reward `100`, penalty
 `100`, reliability blocks with
 `2, 1, 3` redundant paths respectively (intel acquisition,
 insertion, extraction).
- Allocation: budget `6` assets over
 `4` objectives (concave curves).
- Learning: rate `0.4`, `8` iterations, bonus cap
 `0.3`, target `0.55`.
- Sensitivity sweep ranges: `[0.5, 20]` (success sensitivity),
 `[0.05, 1]` (detection rate), and
 `[0.05, 1]` (learning rate), each sampled at
 `401` evenly spaced points.

All canonical numeric constants live in the domain modules
(`mission_replay.py`, `legacy_assets.py`, `remount_risk.py`,
`asset_allocator.py`, `learning_curve.py`, `sensitivity.py`), shared by the
mission adapter, the manuscript tokens, and the figures — no duplicated
numbers.
`docs/manuscript/config.yaml` mirrors the same values for human readers, and
`tests/test_manuscript_variables.py` asserts the mirror matches the code, so a
constant changed in one place and not the other fails the suite.

### Fixtures and isolation

Tests use real data and computation only (no mock framework), with fixed inputs
so every outcome is deterministic. Figures render with the Agg backend and are
byte-identical across runs. Manuscript variables are injected — they are never
hand-authored in prose.

## Reproducibility — REPLAY: verification gates, deterministic regeneration, and artifacts

### Determinism by construction

REMOUNT commits to byte-level reproducibility. The domain core performs no
random draws and no wall-clock reads, so replaying `THUNDERBALL-65` twice
yields identical `ReplayResult` objects; rendering a figure twice yields
identical PNG bytes.

The claim covers the whole persisted artifact set — every file under
`output/`: `data/manuscript_variables.json`, the resolved manuscript tree under
`docs/manuscript/`, and the five PNGs under `figures/`. No token reads the clock.
The date on this document, `MANUSCRIPT_DATE`, is `paper.date` from the
committed `docs/manuscript/config.yaml`, so it changes only when a human changes it
in version control — never merely because the generator ran again. That is
enforced, not asserted: `tests/test_regeneration_determinism.py` runs the
generator twice, more than a clock-second apart, into two separate output
roots and compares the SHA-256 of every file.

### Provenance

Every mission outcome carries a `Provenance` block with:

- `package_version` — 0.1.0.
- `seed` — the deterministic seed (13).
- `input_hash` — a canonical SHA-256 fingerprint of the mission brief.
- `wall_time_s` — reported as `0.0`. This is a deliberate choice, not a
 measurement: the provider does not read the clock, because a real elapsed
 time would make otherwise-identical outcomes differ byte-for-byte between
 runs. Read it as "wall time not recorded", never as "the mission took no
 time".

The migrated-asset catalog exposes `stable_integrity`, a catalog-wide
fingerprint over its sorted `(id, kind, content-digest)` rows. The manuscript
token `1a1e05c4f464` is that digest truncated for display, so an
artifact set can be audited without re-running the suite. The same catalog
factory (`canonical_catalog`) feeds the mission provider, the manuscript
tokens, and the asset-distribution figure — there is no second derivation that
could disagree about what was migrated.

### Verification commands

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/ tests/ && uv run ruff format src/ scripts/ tests/
uv run mypy src/ scripts/
rg -n "template[_]code_project". --glob '!uv.lock' --glob '!.git/**'
```

This manuscript is produced on Python 3.14.6; its document date is
2026-08-05.

## Scope and Related Work — REPLAY: boundaries, positioning, and relationship to the literature

### Scope

This package is strictly a BOND suite film package. Its scope is exactly its
own directory; it implements the frozen `bond_api` mission protocol as a thin
adapter (`mission.py`) on top of a pure, infrastructure-free domain core of
seven modules (`mission_replay.py`, `op_diff.py`, `legacy_assets.py`,
`remount_risk.py`, `asset_allocator.py`, `learning_curve.py`,
`sensitivity.py`). It does not
attempt to be a general simulation framework or a full intelligence management
system.

### Related work

Within the BOND suite this film sits at the film layer: it consumes Layer 1
(`bond-api`, the frozen `MissionProvider` protocol and `GadgetRegistry`) and
imports no sibling film package. Layer 0 (`bond-utilities`) is not yet bound
here; the integration points where it would replace in-package code are named
explicitly in `TODO.md` rather than assumed.

Outside the suite, the models are standard and cited rather than invented. The
allocation greedy is the separable-concave special case of Nemhauser, Wolsey
and Fisher's submodular maximization setting [@nemhauser1978submodular], where
the greedy is exactly optimal rather than `(1 - 1/e)`-approximate; the
rehearsal model is the Wright learning
curve [@wright1936learning]; the mission-success structure is a reliability
block diagram in the sense of Barlow and Proschan [@barlow1975reliability],
with detection as a homogeneous Poisson process [@ross2019probability]; the
per-objective success curve is the Verhulst logistic [@verhulst1838notice];
and integrity uses SHA-256 [@nist2015fips180] over NFC-normalized text
[@unicode2023uax15]. This package contributes their deterministic composition
into an auditable remount pipeline, not the models themselves.

### Limitations

These are real bounds on what the results support, not caveats-as-decoration.

- The success model is a single Logistic curve with a hand-chosen sensitivity;
 it is illustrative, not a forecast calibrated against operational data. No
 claim in this manuscript is an empirical claim about real operations.
- `diff_outcomes` aligns objectives by id and **skips** objectives present on
 only one side: they appear in no diff and in none of the counts. Comparing
 two scenarios with different objective sets therefore silently compares only
 the intersection.
- Objective weights are recovered by scenario *name*. A caller-built scenario
 that reuses the canonical name with different weights would be diffed against
 the canonical weights.
- The migration is fingerprint-only. It detects tampering against a declared
 digest but models no cryptographic provenance — no signatures, no chain of
 custody, and no protection against an attacker who rewrites content and
 digest together.
- An un-scanned asset (`integrity is None`) is treated as self-consistent by
 design, so absence of a fingerprint is not evidence of integrity.
- The risk, allocation, and learning models are evaluated at one canonical
 parameter set, and the sensitivity analysis in `03_results.md` sweeps **one
 parameter at a time** (OAT) rather than the joint space. It bounds how far the
 headline conclusions hold under single-parameter variation; it is not a global
 variance decomposition, so it cannot rank second-order parameter interactions.

## Sources — REPLAY: bibliography

@bond_api; @bond_utilities; @nemhauser1978submodular; @wright1936learning; @barlow1975reliability; @ross2019probability; @saltelli2008sensitivity; @verhulst1838notice; @nist2015fips180; @unicode2023uax15


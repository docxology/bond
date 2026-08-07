# Bond Utilities — Q-BRANCH

*infra package · package codename Q-BRANCH*.

## Concepts — Q-BRANCH: domain and operational focus

Q-Branch primitives — ciphers, codenames, clock, provenance, fixtures

## Abstract — Q-BRANCH: mission summary

The BOND suite's shared foundation, codenamed **Q-BRANCH**, ships dependency-light Python modules that every other bond package imports: a classic-cipher suite with cryptanalysis helpers, a deterministic codename engine with several schemes, mission clock/schedule math, seeded randomness, mission-record persistence with provenance, and plain-text reporting. The cipher layer exposes **9** classic primitives (caesar, vigenere, one_time_pad, xor, atbash, beaufort, rail_fence, playfair, columnar) — each round-trip verified with real data — and **8** analysis helpers (letter frequency, index of coincidence, chi-squared scoring, Caesar/Vigenère breaking, Kasiski examination). Codenames are drawn under **5** deterministic schemes (adjective_noun, alliterative, nato, numeric, token); the NATO scheme spells a short identifier as `QUEBEC-BRAVO-7`. Reproducible sampling runs through **7** seeded draw helpers (seeded_bytes, seeded_int, seeded_float, seeded_choice, seeded_choices, seeded_shuffle, seeded_sample), each derived from one seed. Mission schedules are half-open UTC windows with overlap, merge, and duration models, and persisted mission records carry a reproducible input hash, the schema version, and the producing seed, so any outcome can be re-derived from its stored inputs. Every quantity this manuscript claims about the package — counts, capacities, window durations, sample outputs, and gate thresholds — arrives as a generated token computed from `manuscript/config.yaml` and the live registries by `src/bond_utilities/manuscript_variables.py`. Three tests enforce that: a cross-reference test fails on any prose token the generator does not produce; a bare-numeral guard fails on any hand-authored number in the abstract, introduction, results, conclusion, and reproducibility sections; and a hand-copied-metric guard fails when any section anywhere in the manuscript writes a generated value as a literal instead of its token. The exception is stated rather than hidden: the methodology and scope sections write the constants that *define* an algorithm — the modular base, the digraph square size, the reference index-of-coincidence values — as literals, because those are definitions of the mathematics, not measurements of this package.

## Introduction — Q-BRANCH: mission framing, the operational problem, and how to read this chapter

`bond-utilities` is Layer 0 of the BOND suite: the shared, dependency-free
foundation imported by every other bond package. It deliberately keeps its
dependency surface to the standard library plus `numpy`, `matplotlib`, and
`pyyaml`, and it never imports a mock framework.

Three principles govern the design:

- **Determinism.** Every random draw flows through a seeded generator
 (`src/bond_utilities/randomness.py`). The same seed produces the same
 codenames, cipher keys, and test streams on every run and machine.
- **Round-trip guarantees.** Each cipher is accompanied by a test proving
 `decrypt(encrypt(x)) == x` on real streams, and codename obfuscation
 satisfies `restore(obfuscate(x)) == x`.
- **Provenance-first persistence.** Mission records written by
 `mission_io.py` bundle a canonical input hash, the schema version, and
 the producing seed, so every outcome can be reproduced from its
 persisted inputs — the contract bond-api outcomes rely on.

### Module map

| Module | Responsibility |
| --- | --- |
| `ciphers.py` | 9 classical ciphers + 8 cryptanalysis helpers; codename encoding |
| `codenames.py` | 5 deterministic codename schemes (adjective_noun, alliterative, nato, numeric, token) |
| `clock.py` | Elapsed time, schedule windows, overlap/merge, duration parsing, T-minus, `MissionSchedule` |
| `randomness.py` | Seeded RNG factory, `seeded` decorator, and scalar/sequence draw helpers |
| `mission_io.py` | JSON/YAML records, schema validation, provenance verify/append/summary |
| `reporting.py` | Plain-text table, key/value, banner, and schedule-table output |
| `testing.py` | Shared pytest fixtures plus plain test helpers (import-light, no mocks) |
| `figures/` | Deterministic schedule and letter-frequency figures |

### Reader's guide

`02_methodology.md` defines the cipher math and cryptanalysis, the codename
schemes, the seeding, and the clock/window semantics. `03_results.md` reports
the measured round-trips, determinism, cryptanalysis demos, and schedule
results. `05_experimental_setup.md` documents the mission parameters that
drive every token in this manuscript.

## Methodology — Q-BRANCH: the analytical models and algorithms that drive the mission

### Ciphers (`src/bond_utilities/ciphers.py`)

The cipher suite falls into four families. **Monoalphabetic:** Caesar
(`c = (p + shift) mod 26`), Atbash (reverse alphabet, self-inverse), and
Beaufort (`c = (k - p) mod 26`, self-inverse). **Polyalphabetic/keyed:**
Vigenère (keyword advances over letters only), Playfair (digraph
substitution on a 5x5 keyed square with I/J merged, doubles split with `X`).
**Transposition:** rail-fence (zig-zag rows) and columnar (columns read in a
digit-key order, round-trips exactly with no padding). **Byte:** one-time-pad
(XOR with a key at least as long as the data) and XOR (cyclically repeated
key). Every cipher satisfies `decrypt(encrypt(x)) == x` on supported inputs;
the digraph cipher round-trips against its prepared (X-split, padded) form.

#### Cipher catalogue

The compiled table below is generated from the live `CIPHER_DESCRIPTIONS`
registry (token `| caesar | shift cipher, letters only |
| vigenere | polyalphabetic keyword cipher |
| one_time_pad | XOR with a key at least as long as the data |
| xor | symmetric byte-wise XOR with a cyclic key |
| atbash | reverse-alphabet substitution (self-inverse) |
| beaufort | reciprocal keyword cipher c = (k - p) |
| rail_fence | zig-zag row transposition |
| playfair | digraph substitution on a 5x5 keyed square |
| columnar | column-order transposition with a digit key |`), so it cannot drift from the
modules it documents.

| cipher | description |
| --- | --- |
| caesar | shift cipher, letters only |
| vigenere | polyalphabetic keyword cipher |
| one_time_pad | XOR with a key at least as long as the data |
| xor | symmetric byte-wise XOR with a cyclic key |
| atbash | reverse-alphabet substitution (self-inverse) |
| beaufort | reciprocal keyword cipher c = (k - p) |
| rail_fence | zig-zag row transposition |
| playfair | digraph substitution on a 5x5 keyed square |
| columnar | column-order transposition with a digit key |

All cipher "letters" are ASCII `A-Z`/`a-z` by definition
([@unicode_standard]). A character that `str.isalpha` treats as a letter but
that lies outside the 26-letter English alphabet -- e.g. `é`, `ñ`, or a
Cyrillic letter -- is a *non-letter* to these primitives: the ciphers pass it
through unchanged, and the frequency/counting helpers ignore it, so
mixed-alphabet mission text stays safe to pipe through any cipher without a
crash or silent corruption.

### Cryptanalysis helpers

- `letter_frequency` / `frequency_normalized` — A-Z counts and relative
 frequencies.
- `index_of_coincidence` — Friedman's IC: ~0.066 for natural English vs
 ~0.038 for uniform random, used to distinguish substitution from
 polyalphabetic text.
- `english_chi_squared` — chi-squared fit of letter frequencies against
 standard English.
- `caesar_shift_scores` / `caesar_break` — score all 26 shifts by chi-squared
 and return the best `(shift, plaintext)`. The score is a statistic over the
 input's letter counts, so the returned shift is the best-fitting one, not a
 certified one: on short samples the best fit is often the wrong shift, and
 the function returns it with no confidence signal (see Limitations in
 `07_scope_and_related_work.md`).
- `kasiski_key_lengths` — locate repeated n-grams, factor their distances,
 and vote on candidate Vigenère key lengths.
- `vigenere_break` — break each key column independently and re-interleave.

### Deterministic seeding (`randomness.py`)

`derive_seed` folds integer seeds to 32 bits and hashes string seeds
(`int(sha256(seed)[0:8], 16)`). `make_rng(seed)` returns a fresh
`random.Random`; the `seeded(seed)` decorator seeds the global module and
restores the prior state on exit, so a decorated function is deterministic in
isolation without perturbing its caller. The module also exports
7 typed draw helpers (seeded_bytes, seeded_int, seeded_float, seeded_choice, seeded_choices, seeded_shuffle, seeded_sample), each
reproducible from a single seed and enumerated in the `SEEDED_HELPERS`
registry that the manuscript reads.

### Codename schemes (`codenames.py`)

- `adjective_noun` (default) — unique pairs sampled without replacement from
 a 12 x 12 grid.
- `alliterative` — ADJ-NOUN pairs sharing a starting letter. Unlike
 `adjective_noun`, this scheme seeds each index independently instead of
 sampling without replacement, so a batch may repeat a name; and only
 5 initials are carried by both word lists, giving
 9 distinct pairs in total. Repetition in a batch is
 therefore expected, not a defect — `tests/test_codenames.py` asserts both the
 capacity and the repetition.
- `nato` — NATO phonetic spelling of a base codename (e.g. `QUEBEC-BRAVO-7`).
- `numeric` — `PREFIX-XXXXXXXX` hex codes derived from a mission id.
- `token` — truncated SHA-256 hex tokens.

Each scheme is deterministic under a fixed seed; `generate_codenames(..., scheme=…)`
selects the scheme while preserving the phase-1 default exactly.

### Mission clock (`clock.py`)

Times are timezone-aware (naive treated as UTC). A window is the half-open
interval `[start, end)`. Phase 4 adds `windows_overlap` (shared duration,
clamped at zero), `merge_windows` (minimal sorted cover), `parse_duration`
(`"1d 2h30m"`-style), `schedule_status` (`PENDING`/`ACTIVE`/`COMPLETE`), and
the `MissionSchedule` dataclass tying duration, open/elapsed/remaining,
countdown, and status together.

### Provenance (`mission_io.py`)

`record_provenance_outcome` persists a record whose `provenance` block holds
the canonical input hash (SHA-256 of sorted-compact JSON), the schema version,
and the derived seed. Phase 4 adds `verify_provenance` (recompute and compare
the hash/seed/version), `load_records` (sorted directory batch load),
`record_summary` (flat deterministic digest), and `append_outcome` (merge into
`outcomes` without disturbing provenance).

### Reporting and figures (`reporting.py`, `figures/plots.py`)

`reporting.py` renders the plain-text surface the thin CLIs print: `banner`,
`format_table` (left-aligned, width-fitted, ragged rows rejected), `format_kv`
(right-aligned keys), and `schedule_table`, which projects a sequence of
`MissionSchedule` objects into name/start/end/status rows evaluated at a caller-
supplied instant. The `print_*` wrappers take an explicit `stream`; the default
resolves `sys.stdout` at call time rather than at import time, so redirected
output is captured correctly and tests can assert on real rendered text without
a mock framework.

`figures/plots.py` renders the two manuscript figures. `plot_mission_schedule`
draws the window as a horizontal bar in unix-time coordinates with a dashed
"now" marker; `plot_frequency_analysis` draws the A-Z counts returned by
`ciphers.letter_frequency`. Both are deterministic under the Agg backend — the
same inputs produce byte-identical PNGs, which `tests/test_figures.py` asserts
for each figure by comparing two renders. For the schedule figure the input
includes `now`: the marker moves with the wall clock when `now` is left to its
library default, so determinism is claimed and tested for a fixed `now`, and a
negative control asserts that two different `now` values do produce different
bytes. The manuscript pipeline never uses that default — the generator script
passes `manuscript_variables.manuscript_instant(config)`, a committed value,
so the rendered PNG is part of the byte-identical regeneration claim.

### Shared fixtures (`testing.py`)

`testing.py` carries the shared test surface every bond package reuses through
its own `conftest.py`. Two of the four names are actual pytest fixtures —
`seeded_rng` (a `random.Random` at the suite's default seed) and
`mission_record` (a schema-valid record); the other two are plain callables
imported directly, `temp_dir` (a context manager) and `seeded_codenames` (a
function). A test asserts that split, so the distinction cannot be lost.
It imports only `pytest`, the standard library, and this package's pure
primitives, so importing it can never pull numpy, matplotlib, or — the point of
the constraint — a mock framework into a consumer's test session.

### Scoring and statistics

Frequency scoring uses the standard English letter table in `ENGLISH_FREQUENCIES`
(normalized; sum 1.0). All cryptanalysis outputs are deterministic given the
input text.

## Results — Q-BRANCH: measured outcomes, headline numbers, and what they establish

### Round-trip fidelity

Every cipher in `src/bond_utilities/ciphers.py` passes a round-trip identity
on real streams: Caesar and Atbash (letters, case preserved), Vigenère and
Beaufort (non-letters pass through), rail-fence and columnar (exact
transposition, no padding), Playfair (against its prepared form), XOR and
one-time-pad (bytes). None of the tests use mocks — they exercise the actual
algorithms.

### Cryptanalysis demos

Both breakers are statistical, and their accuracy is a function of sample
length rather than a guarantee. On the letter-rich English samples used in
`tests/test_documented_examples.py`, `caesar_break` recovers the exact shift and
plaintext, and `vigenere_break` recovers a keyword of known length and
decrypts. On short samples both return a wrong answer with no confidence
signal: a sixteen-letter English plaintext enciphered at a known shift comes
back under a different shift, and the twenty-one-letter case fails likewise for
both breakers. Those failures are asserted as tests, not merely noted, so the
qualification cannot quietly stop being true. `kasiski_key_lengths` returns the
true key length among its candidates for repeated plaintext, and
`index_of_coincidence` cleanly separates repetitive (more-structured) text from
uniform random text. The figure
`the freq figure` shows the A-Z counts of the mission codename sample.

![Letter frequency of the codename sample.](output/figures/bond-utilities_letter_frequency.png)

### Edge-case robustness

The cipher alphabet is ASCII `A-Z`/`a-z` by definition ([@unicode_standard]).
Non-ASCII alphabetic characters -- `é`, `ñ`, and letters from other
scripts, which Python's `str.isalpha` classifies as letters -- are treated as
*nothing to the cipher*: the enciphering functions pass them through byte-for-
byte, and the frequency, index-of-coincidence, and chi-squared helpers ignore
them entirely. That contract is asserted as a regression test
(`tests/test_ciphers.py::TestNonAsciiRobustness`), which pins three properties
that previously failed: the A-Z counting helpers accept mixed-alphabet text
without crashing, a non-ASCII letter never corrupts a cipher round-trip, and
`caesar_break`/`english_chi_squared` treat a non-ASCII-only input as letterless
rather than misinterpreting it. The same hardening closes two validation gaps
in the primitives' edge behaviour: a non-string timestamp raises `ValueError`
rather than leaking an internal `AttributeError`
(`tests/test_clock.py::TestParseTimestampValidation`), and an empty header list
to `format_table` means *no header* rather than tripping the ragged-row guard
(`tests/test_reporting.py::TestFormatTableHeadersEdge`).

### Determinism

All **9** ciphers (caesar, vigenere, one_time_pad, xor, atbash, beaufort, rail_fence, playfair, columnar) and the codename
generator are deterministic under a fixed seed. The default adjective–noun
sample of 6 names drawn with seed
20260804:

> SHADOW-FALCON, IRON-JAGUAR, WILD-HORIZON, SILENT-RAVEN, VELVET-BEACON, WILD-FALCON

An alliterative sample under the same seed:

> CRIMSON-COMET, CRIMSON-COMET, SILENT-SENTINEL, RAPID-RAVEN, BRAVE-BEACON, CRIMSON-COMET

That alliterative sample repeats: it holds 4 distinct
names across 6 slots. That is the scheme working as
specified, not a bug — `alliterative` seeds each index independently rather
than sampling without replacement, and the bundled word lists share only
5 initials between adjectives and nouns, admitting
9 distinct pairs in total. Collisions are therefore
likely in any batch of that size, and a test asserts that this sample contains
one. Callers needing distinct names must use the default scheme.

The scheme registry holds 5 entries
(adjective_noun, alliterative, nato, numeric, token); each is bound to a real dispatch branch by a
registry-drift test. The default scheme draws without replacement from a
12 x 12 adjective/noun grid, so its capacity is
144 unique pairs — `generate_codenames` raises above that
count rather than repeating a name.

### Seeded draw helpers

Reproducible sampling outside the codename engine goes through the
7 helpers in `src/bond_utilities/randomness.py`
(seeded_bytes, seeded_int, seeded_float, seeded_choice, seeded_choices, seeded_shuffle, seeded_sample). Each takes the seed as its first argument and
constructs a fresh `random.Random`, so draws never depend on call order or on
the global interpreter RNG. `ciphers.generate_otp_key` delegates to
`seeded_bytes`, which is why pad material and any other byte draw are
byte-identical for the same seed. The registry itself is test-bound: a
discovery test in `tests/test_randomness.py` fails if a helper is added,
renamed, or dropped without updating `SEEDED_HELPERS`.

### Provenance round-trip

`record_provenance_outcome` writes a record whose `provenance` block holds the
canonical SHA-256 of the sorted-compact JSON parameters, the schema version,
and the derived seed. `verify_provenance` recomputes all three from the
persisted record and returns `False` on any mismatch — the mutation tests in
`tests/test_mission_io.py` tamper with the parameters, the seed, and the schema
version in turn and confirm each is rejected, so the check is not satisfiable
by construction. `append_outcome` merges new results into `outcomes` and leaves
the provenance block byte-identical, which is what lets a later mission stage
extend a record without invalidating its audit trail.

### Mission schedule

The primary mission window spans 144.0 hours, from
2026-08-04T00:00:00+00:00 to 2026-08-10T00:00:00+00:00 (UTC), rendered in
the schedule figure. The secondary window overlaps the primary by
48.0 hours — computed by `windows_overlap`, not
hand-authored. Window math is exact under the half-open `[start, end)`
semantics; elapsed and remaining durations clamp at zero.

![Mission schedule window with the reference "now" marker.](output/figures/bond-utilities_mission_schedule.png)

## Conclusion — Q-BRANCH: findings, verdict, and what the mission establishes

`bond-utilities` (codename **Q-BRANCH**) delivers a broadened,
fully-tested, dependency-light foundation on which the rest of the BOND suite
is built. Every quantity this manuscript claims about the package is generated
from `manuscript/config.yaml` and the live registries through
`src/bond_utilities/manuscript_variables.py`, and three tests enforce it: token
cross-reference, a bare-numeral guard over the quantitative sections, and a
hand-copied-metric guard that fails if any section anywhere writes a generated
value as a literal. The constants that define an algorithm — the modular base,
the digraph square size, the reference index-of-coincidence values — are
written literally in the methodology and scope sections, because they describe
the mathematics rather than measure this package.

The guarantees that matter for downstream packages are:

- **Reproducibility**: one seed fully determines every codename, key, draw,
 and test stream.
- **Correctness**: all **9** ciphers are round-trip verified
 with real data, and the **8** helpers turn classic
 frequency analysis into deterministic, testable functions.
- **Provenance**: persisted mission records carry a reproducible input hash,
 schema version, and seed (`verify_provenance` recomputes them), so outcomes
 can always be audited and reproduced.

Future phases (bond-api and higher layers) will continue to consume this
package's `record_provenance_outcome`/`verify_provenance` persistence surface,
its seeded draw helpers, and its schedule models.

## Experimental Setup — Q-BRANCH: canonical scenarios, parameters, and configuration

### Mission parameters

All values are read from `manuscript/config.yaml` by
`src/bond_utilities/manuscript_variables.py::generate_variables`; scripts
never hardcode them.

| Parameter | Value |
| --- | --- |
| Package version | 0.3.0 |
| Mission codename | Q-BRANCH |
| Default seed | 20260804 |
| Codename sample size | 6 |
| Schedule start (UTC) | 2026-08-04T00:00:00+00:00 |
| Schedule end (UTC) | 2026-08-10T00:00:00+00:00 |
| Window duration | 144.0 hours |
| Overlap with secondary window | 48.0 hours |
| Cipher primitives | 9 |
| Cipher registry | caesar, vigenere, one_time_pad, xor, atbash, beaufort, rail_fence, playfair, columnar |
| Codename schemes | 5 (adjective_noun, alliterative, nato, numeric, token) |
| Cryptanalysis helpers | 8 |
| Seeded draw helpers | 7 (seeded_bytes, seeded_int, seeded_float, seeded_choice, seeded_choices, seeded_shuffle, seeded_sample) |
| Word-list grid | 12 x 12 |
| Word-list capacity (unique pairs) | 144 |
| Coverage gate | 90% line + branch on `src/` |
| Tolerated test failures | 0 |
| Manuscript date (config `paper.date`) | 2026-08-04 |

### Software environment

The package requires Python ≥ 3.10 and depends only on `numpy`,
`matplotlib`, and `pyyaml`. Tests use `pytest` and `pytest-cov`; no mock
framework is used anywhere. All randomness is seeded; functions with a
wall-clock default take an explicit `now=/seed=` override in tests.

## Reproducibility — Q-BRANCH: verification gates, deterministic regeneration, and artifacts

### Artifact inventory

| Artifact | Producer |
| --- | --- |
| `output/data/manuscript_variables.json` | `scripts/z_generate_manuscript_variables.py` |
| `output/figures/mission_schedule.png` | same script → `src/bond_utilities/figures/plots.py::plot_mission_schedule` |
| `output/figures/letter_frequency.png` | same script → `plots.plot_frequency_analysis` |

All artifacts are regenerated, never hand-edited. Regeneration is a single
command:

```bash
uv run python scripts/z_generate_manuscript_variables.py
```

Running that command twice on the same commit rewrites every artifact above
**byte for byte**. Nothing in the pipeline reads the wall clock: the token map
is a pure function of `manuscript/config.yaml` and the library registries, and
the schedule figure's reference marker is pinned to `paper.date` through
`manuscript_variables.manuscript_instant` rather than to `datetime.now`.
The claim is bound by `tests/test_regeneration_determinism.py`, which runs the
command above twice — separated by a real clock tick, so a reinstated
timestamp cannot slip through — and compares a digest of the whole `output/`
tree. The scope is exactly that artifact tree; nothing here is a claim about
the wider environment, which the experimental-setup section pins separately.

### Determinism claims

- Codenames: `generate_codenames(count, seed=S, scheme=...)` returns the same
 list on every run and machine, for every scheme.
- Cipher keys and byte draws: `generate_otp_key(length, seed=S)` delegates to
 `seeded_bytes(S, length)`, so both return the same bytes for the same seed.
- Every other seeded helper (seeded_bytes, seeded_int, seeded_float, seeded_choice, seeded_choices, seeded_shuffle, seeded_sample) builds its own
 `random.Random` from the seed, so a draw never depends on call order.
- Cryptanalysis: frequency, IC, chi-squared, Kasiski, and Caesar/Vigenère
 breaking are deterministic functions of the input text.
- Mission records: `record_provenance_outcome` stores the canonical input
 hash; `verify_provenance` recomputes it, so any outcome can be audited and
 re-derived from its persisted inputs.

### Quality gate

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run ruff check src/ scripts/
uv run ruff format --check src/ scripts/
uv run mypy src/ scripts/
```

The gate enforces at least 90% line **and** branch
coverage on `src/`, and tolerates at most 0 failing tests.
Both numbers come from `manuscript/config.yaml`, and a test asserts the
coverage figure equals the `fail_under` value actually enforced by
`pyproject.toml` — the prose cannot drift away from the enforced gate. The
measured coverage of any given run is deliberately not quoted here; run the
command above to read it. `ruff check`, `ruff format --check`, and
`mypy src/ scripts/` must also pass clean.

## Scope and Related Work — Q-BRANCH: boundaries, positioning, and relationship to the literature

### Scope

This package implements *utility* cryptography and scheduling primitives —
obfuscation, reproducible sampling, frequency analysis, and window math — for
the internal BOND suite. It is explicitly **not** a security product: the
ciphers are educational and deterministic, and must never be used for real
secrecy.

### Related work

The cipher primitives follow the classical constructions catalogued by Kahn
[@kahn_codebreakers] and presented as textbook algorithms by Stinson and
Paterson [@stinson_paterson_2018], and are formalised in Shannon's
information-theoretic treatment of secrecy systems [@shannon_1949] — which is
also the reference that makes the one-time pad's key-length requirement
non-negotiable rather than a stylistic choice. The cryptanalysis helpers build
on Friedman's index of coincidence [@friedman_1922] and Kasiski's examination
for repeated key segments [@kasiski_1863]. Deterministic seeded generation uses
the Mersenne Twister [@matsumoto_1998] as exposed by Python's `random` module;
that generator is chosen for reproducibility and equidistribution, explicitly
not for cryptographic unpredictability. Mission window and elapsed-time
semantics follow ISO-8601 date/time representations [@iso8601].

### Limitations

- The ciphers do not provide authentication, integrity, or non-repudiation.
- Determinism trades secrecy for reproducibility by design.
- `caesar_break` and `vigenere_break` are chi-squared fits to English letter
 frequencies, so both recover reliably only on letter-rich ciphertext. Neither
 reports confidence: on a short sample the best-fitting shift is often the
 wrong one and is returned as if it were correct. Measured cases —
 a sixteen-letter and a twenty-one-letter English plaintext, both enciphered
 at a known Caesar shift and both recovered under a different shift, and the
 twenty-one-letter Vigenère case recovering the wrong key — are asserted in
 `tests/test_documented_examples.py`. Treat a recovered key from a short text
 as a guess.
- The `alliterative` codename scheme can repeat a name within one batch: it
 seeds each index independently, and the bundled word lists admit only
 9 distinct pairs across 5
 shared initials. Only the default `adjective_noun` scheme guarantees
 distinctness (and raises rather than repeating once capacity is exhausted).
- The word lists are deliberately small and curated; they are not a secure
 randomness source.

## Sources — Q-BRANCH: bibliography

@kahn_codebreakers; @shannon_1949; @matsumoto_1998; @friedman_1922; @kasiski_1863; @stinson_paterson_2018; @iso8601; @unicode_standard


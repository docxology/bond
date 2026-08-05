# Bond Utilities — Q-BRANCH

*infra package · mission codename Q-BRANCH*.

## Concepts

Q-Branch primitives — ciphers, codenames, clock, provenance, fixtures

## Abstract (imported from the package manuscript)

The BOND suite's shared foundation, codenamed **Q-BRANCH**, ships dependency-light Python modules that every other bond package imports: a classic-cipher suite with cryptanalysis helpers, a deterministic codename engine with several schemes, mission clock/schedule math, seeded randomness, mission-record persistence with provenance, and plain-text reporting. The cipher layer exposes **9** classic primitives (caesar, vigenere, one_time_pad, xor, atbash, beaufort, rail_fence, playfair, columnar) — each round-trip verified with real data — and **8** analysis helpers (letter frequency, index of coincidence, chi-squared scoring, Caesar/Vigenère breaking, Kasiski examination). Codenames are drawn under **5** deterministic schemes (adjective_noun, alliterative, nato, numeric, token); the NATO scheme spells a short identifier as `QUEBEC-BRAVO-7`. Reproducible sampling runs through **7** seeded draw helpers (seeded_bytes, seeded_int, seeded_float, seeded_choice, seeded_choices, seeded_shuffle, seeded_sample), each derived from one seed. Mission schedules are half-open UTC windows with overlap, merge, and duration models, and persisted mission records carry a reproducible input hash, the schema version, and the producing seed, so any outcome can be re-derived from its stored inputs. Every quantity this manuscript claims about the package — counts, capacities, window durations, sample outputs, and gate thresholds — arrives as a generated token computed from `manuscript/config.yaml` and the live registries by `src/bond_utilities/manuscript_variables.py`. Three tests enforce that: a cross-reference test fails on any prose token the generator does not produce; a bare-numeral guard fails on any hand-authored number in the abstract, introduction, results, conclusion, and reproducibility sections; and a hand-copied-metric guard fails when any section anywhere in the manuscript writes a generated value as a literal instead of its token. The exception is stated rather than hidden: the methodology and scope sections write the constants that *define* an algorithm — the modular base, the digraph square size, the reference index-of-coincidence values — as literals, because those are definitions of the mathematics, not measurements of this package.

## Sources

@kahn_codebreakers; @shannon_1949; @matsumoto_1998; @friedman_1922; @kasiski_1863; @stinson_paterson_2018; @iso8601


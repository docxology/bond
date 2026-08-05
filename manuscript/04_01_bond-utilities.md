# Bond Utilities — Q-BRANCH

*infra package · mission codename Q-BRANCH*.

## Concepts

Q-Branch primitives — ciphers, codenames, clock, provenance, fixtures

## Abstract (imported from the package manuscript)

The BOND suite's shared foundation, codenamed **Q-BRANCH**, ships dependency-light Python modules that every other bond package imports: a classic-cipher suite with cryptanalysis helpers, a deterministic codename engine with several schemes, mission clock/schedule math, seeded randomness, mission-record persistence with provenance, and plain-text reporting. The cipher layer exposes **9** classic primitives (caesar, vigenere, one-time-pad, xor, atbash, beaufort, rail_fence, playfair, columnar) — each round-trip verified with real data — and **8** analysis helpers (letter frequency, index of coincidence, chi-squared scoring, Caesar/Vigenère breaking, Kasiski examination). Codenames are sampled under adjective_noun, alliterative, nato, numeric, token as a seeded, deterministic scheme (e.g. `QUEBEC-BRAVO-7` in NATO spelling). Mission schedules are half-open UTC windows with overlap, merge, and duration models, and persisted mission records carry a reproducible input hash plus sea of the producing seed. Every token in this manuscript is computed from `manuscript/config.yaml` via `src/bond_utilities/manuscript_variables.py` — never hand-authored.

## Sources

@kahn_codebreakers; @shannon_1949; @matsumoto_1998; @friedman_1922; @kasiski_1863; @iso8601


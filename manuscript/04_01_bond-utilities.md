# Bond Utilities — Q-BRANCH

*infra package · mission codename Q-BRANCH*.

## Concepts

Q-Branch primitives — ciphers, codenames, clock, provenance, fixtures

## Abstract (imported from the package manuscript)

The BOND suite's shared foundation, codenamed **Q-BRANCH**, ships seven dependency-light Python modules that every other bond package imports: classic ciphers, a deterministic codename generator, mission clock math, seeded randomness, mission-record persistence with provenance, and plain-text reporting. The library exposes **4** classic cipher primitives (Caesar, Vigenère, one-time-pad, XOR), each verified by byte-for-byte round-trip tests. Codenames are sampled from a 12 x 12 adjective–noun grid through a seeded generator, so a fixed seed (20260804) yields a fixed list. Mission schedules are expressed as half-open UTC windows, and tokens in this manuscript are computed — never hand-authored — from `manuscript/config.yaml` via `src/bond_utilities/manuscript_variables.py`.

## Sources

@kahn_codebreakers; @shannon_1949; @matsumoto_1998; @iso8601


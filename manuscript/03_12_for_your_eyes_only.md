# For Your Eyes Only (1981) — ATAC

*film package · mission codename ATAC*. Mission **ATAC**: recover the lost ATAC targeting-communicator key; verify custodian custody before release; plan underwater retrieval and island insertion.

## Concepts

targeting systems, key recovery

## Abstract (imported from the package manuscript)

**For Your Eyes Only: ATAC — Special-Agent Mission Software** — Targeting-Communicator Escrow, Underwater Retrieval, and Greek-Island Insertion Routing. This report documents the **ATAC** special-agent mission software: a deterministic suite for recovering a lost targeting-communicator device and directing it onto target. The mission's mathematics rest on six pillars, each implemented as a pure, infrastructure-free domain module: 1. **Key escrow** — the ATAC key is split among 3 custodians using Shamir secret sharing, with a quorum of 2 required to release it (key 1390851129; match True). 2. **Erasure-coded key recovery** — 4 data symbols encoded into 6 code fragments so any quorum recovery survives loss/corruption (match True). 3. **Underwater retrieval planning** — a Haldane-style staged dive to (-122.400, 51.000) m drift offset over 1020.000 s to reach the 42-m wreck (reachable: True). 4. **Greek-island insertion routing** — a least-cost route (corfu -> paxi -> lefkada -> ithaca -> wreck_site, 56.00 nm). 5. **Fire-control targeting** — an intercept lead-angle firing solution (94.6 s, 9.89° lead; feasible True). 6. **Underwater acoustic link** — a link budget with SNR 52.33 dB at 3500 m against a 8 dB threshold, a margin of 44.33 dB (closes: True; max range 18553 m). Every computation is deterministic — a single fixed seed (7), no untracked randomness, no wall-clock dependence in persisted artifacts — and each concept carries a matching real-data test suite with no mocking framework. Every quantity above is injected from the code that computed it rather than typed into the prose, and the escrow's fingerprint match is re-derived by comparison rather than asserted, so a wrong result would surface as a changed number instead of a stale claim. Keywords: key escrow and recovery, Shamir secret sharing, erasure coding, underwater retrieval planning, decompression modelling, island routing, fire-control targeting, underwater acoustic link budget, deterministic mission software.

## Sources

@shamir1979share; @boycott1908prevention; @dijkstra1959note; @hart1968formal; @reed1960polynomial; @thorp1967analytic; @urick1983principles; @blakley1979safeguarding; @berlekamp1968algebraic; @buhlmann1984decompression


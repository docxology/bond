# For Your Eyes Only (1981) — ATAC

*film package · mission codename ATAC*. Mission **ATAC**: recover the lost ATAC targeting-communicator key; verify custodian custody before release; plan underwater retrieval and island insertion.

## Concepts

targeting systems, key recovery

## Abstract (imported from the package manuscript)

**For Your Eyes Only: ATAC — Special-Agent Mission Software** — Targeting-Communicator Escrow, Underwater Retrieval, and Greek-Island Insertion Routing. This report documents the **ATAC** special-agent mission software: a deterministic suite for recovering a lost targeting-communicator device. The mission's mathematics rest on three pillars, each implemented as a pure, infrastructure-free domain module: 1. **Key escrow and recovery** — the ATAC key is split among 3 custodians using Shamir secret sharing over a finite field, with a quorum of 2 required to release it. Recovery reconstructs the key (4242) and confirms it against the escrow fingerprint (match: True). 2. **Underwater retrieval planning** — a Haldane-style model plans a staged dive to the wreck at 42 m, compensating for current drift (surface offset ≈ (-122.400, 51.000) m) over a total dive time of 1020.000 s. Target reachability: True. 3. **Greek-island insertion routing** — a weighted Ionian-island graph routes the insertion from the staging base to the wreck site via a least-cost path (corfu -> paxi -> lefkada -> ithaca -> wreck_site; 4 hops, distance 56.00 nm, cost 57.000). Every computation is deterministic — fixed seeds, no untracked randomness, no wall-clock dependence in persisted artifacts — and each concept carries a matching real-data test suite. Keywords: key escrow and recovery, Shamir secret sharing, underwater retrieval planning, decompression modelling, island routing, Dijkstra shortest path, deterministic mission software.

## Sources

@shamir1979share; @haldane1908relation; @dijkstra1959note; @hart1968formal


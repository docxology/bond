# The Man with the Golden Gun (1974) — SOLEX

*film package · mission codename SOLEX*. Mission **SOLEX**: model solar concentration yield (mirror array to heat); track solar position and daily clear-sky insolation; solve the funhouse lair escape topology (rooms/mirrors as graph); analyse lair flow: edge-disjoint routes, min cut, cheapest escape; schedule the assassin duel/bounty appointment book; schedule unit-time deadline bounty contracts (max profit).

## Concepts

solar concentration, lair topology, assassin scheduling

## Abstract (imported from the package manuscript)

**Mission codename: SOLEX** — Project BOND film dossier for *The Man with the Golden Gun* (1974). ## Abstract This dossier documents the deterministic mission software built for the SOLEX operation. 6 specialist capabilities support the field agent: 1. **Solar concentration yield** — a heliostat-field model that converts a mirror array's area and reflectivity into optical power and thermal heat output, and allocates a mirror-area budget to the highest-yield mirrors. 2. **Solar tracking & daily insolation** — the sun-geometry layer: declination, daylight window, and the Duffie–Beckman clear-sky daily energy the field concentrates. 3. **Funhouse lair escape topology** — a graph solver over the villain's mirror-lined funhouse, producing a shortest escape route and identifying the bottleneck rooms that guard the exit. 4. **Lair flow analysis** — max-flow / min-cut over the lair, returning the edge-disjoint escape routes and the minimum mirror walls that seal the lair, plus a cost-aware (Dijkstra) cheapest escape. 5. **Assassin duel / bounty scheduling** — an appointment book solved by weighted interval scheduling, selecting a non-overlapping set of bounty duels that maximises total reward and reporting every scheduling conflict. 6. **Deadline bounty scheduling** — unit-time bounty contracts scheduled by the deadline-greedy (union–find) algorithm to maximise accepted profit. All results are computed from real, deterministic domain models with fixed inputs and no wall-clock dependence; every metric in this manuscript flows from code, never from hand-authored prose. The canonical SOLEX field converts a 1000 W/m² irradiance into a thermal output of 191.6325 kW (concentration 50.10×) and, over a clear-sky solstice day at 8.0°N, concentrates 1441.7 kWh. The extended funhouse has 3 edge-disjoint escape routes (min cut 3 mirror walls), while the canonical lair is guarded by 3 bottleneck rooms — redundancy and criticality are separate measurements, and the lair's 4 articulation points are a third. On the duel book the two exact schedulers disagree: weighted interval scheduling realises a bounty of 13.0 where the count-maximising earliest-finish greedy realises 11.0. The deadline book yields a maximum profit of 18.0 across 5 contested contracts.

## Sources

@bond_protocol; @golden_gun_film; @duffie_beckman; @spencer; @michalsky; @cormen; @ford_fulkerson; @edmonds_karp; @dijkstra; @hopcroft_tarjan; @kleinberg_tardos; @tarjan_unionfind


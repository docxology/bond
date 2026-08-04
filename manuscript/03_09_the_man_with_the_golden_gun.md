# The Man with the Golden Gun (1974) — SOLEX

*film package · mission codename SOLEX*. Mission **SOLEX**: model solar concentration yield (mirror array to heat); solve the funhouse lair escape topology (rooms/mirrors as graph); schedule the assassin duel/bounty appointment book.

## Concepts

solar concentration, lair topology, assassin scheduling

## Abstract (imported from the package manuscript)

**Mission codename: SOLEX** — Project BOND film dossier for *The Man with the Golden Gun* (1974). ## Abstract This dossier documents the deterministic mission software built for the SOLEX operation. Three specialist capabilities support the field agent: 1. **Solar concentration yield** — a heliostat-field model that converts a mirror array's area and reflectivity into optical power and thermal heat output, and allocates a mirror-area budget to the highest-yield mirrors. 2. **Funhouse lair escape topology** — a graph solver over the villain's mirror-lined funhouse, producing a shortest escape route and identifying the bottleneck rooms that guard the exit. 3. **Assassin duel / bounty scheduling** — an appointment book solved by weighted interval scheduling, selecting a non-overlapping set of bounty duels that maximises total reward and reporting every scheduling conflict. All results are computed from real, deterministic domain models with fixed seeds and no wall-clock dependence; every metric in this manuscript flows from code, never from hand-authored prose. The canonical SOLEX field converts a 1000 W/m² irradiance into a thermal output of 191.6325 kW at a concentration ratio of 50.10×, the lair has a 4-passage shortest escape route guarded by 3 bottleneck rooms, and the duel book realises a maximum bounty of 13.0 from 4 contracts.

## Sources

@bond_protocol; @golden_gun_film; @kleinberg_tardos


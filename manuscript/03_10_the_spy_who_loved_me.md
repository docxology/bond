# The Spy Who Loved Me (1977) — LIPARUS

*film package · mission codename LIPARUS*. Mission **LIPARUS**: detect and track a passive-acoustic contact; simulate a Liparus-Class tanker capture and verify vehicle conversion.

## Concepts

submarine tracking, marine forensics

## Abstract (imported from the package manuscript)

The Spy Who Loved Me: LIPARUS — Special-Agent Mission Software is a deterministic special-agent mission model built around the three concepts of *The Spy Who Loved Me* (1977) under mission codename LIPARUS. It comprises 3 standalone, infrastructure-free domain modules — passive acoustic submarine detection and bearing-only tracking, a Liparus-class tanker capture simulation, and submersible vehicle conversion forensics — exposed to the BOND fleet through a frozen `MissionProvider` adapter. Every result in this manuscript is computed live by the domain core, never hand-authored: the passive tracker recovers the quarry's position to within 65.4 metres of truth, a representative Liparus swallow completes in 630 seconds, and the Lotus-Esprit-grade conversion is classified submersible. All simulations are seeded and fully deterministic, and the test suite holds line and branch coverage on `src/` at or above 90%.

## Sources

@kay_detection_1998; @nardone_aidala_1981; @anderson_moore_1979; @rahman_2007


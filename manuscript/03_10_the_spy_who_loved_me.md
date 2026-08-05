# The Spy Who Loved Me (1977) — LIPARUS

*film package · mission codename LIPARUS*. Mission **LIPARUS**: detect, localise and track a passive-acoustic contact; simulate a Liparus-Class tanker capture, verify submersible conversion and hull viability.

## Concepts

submarine tracking, marine forensics

## Abstract (imported from the package manuscript)

The Spy Who Loved Me: LIPARUS — Special-Agent Mission Software is a deterministic special-agent mission model built around the concepts of *The Spy Who Loved Me* (1977) under mission codename LIPARUS. It comprises 6 standalone, infrastructure-free domain modules — passive acoustic detection and bearing-only tracking, Liparus-class tanker capture, submersible vehicle conversion forensics, underwater acoustics and the passive sonar equation, uniform-linear-array beamforming, and pressure-hull collapse/ballast analysis — exposed to the BOND fleet through a frozen `MissionProvider` adapter. Every result in this manuscript is computed live by the domain core, never hand-authored: the tracking pipeline recovers the quarry's position to within 65.4 metres of truth, the ULA beamformer resolves the contact to within one 0.5-degree scan cell of the true bearing against a Cramer-Rao floor of 0.33 degrees (Section @sec:results explains why the measured error is grid-limited rather than CRB-limited), the passive sonar equation yields a detection range of 83746 metres, and the Esprit-grade pressure hull survives to a collapse depth of 85 metres (a safety factor of 2.13 at its operating depth of 40 metres) while requiring 244 L of ballast to reach neutral buoyancy. All simulations are seeded and fully deterministic, and the test suite holds line and branch coverage on `src/` at or above 90%.

## Sources

@kay_detection_1998; @nardone_aidala_1981; @anderson_moore_1979; @tupper_naval_2013; @urick_principles_1983; @thorp_1967; @mackenzie_1981; @van_trees_2002; @timoshenko_gere_1961; @young_roark_2011


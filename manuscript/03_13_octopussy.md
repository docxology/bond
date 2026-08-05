# Octopussy (1983) — FABERGE

*film package · mission codename FABERGE*. Mission **FABERGÉ**: detect artifact forgeries via spectral/UV fingerprinting; route smuggled payload under circus cover by min-cost flow; sweep for a concealed nuclear device via radiation and mass anomaly.

## Concepts

forgery detection, cover logistics

## Abstract (imported from the package manuscript)

**Octopussy: FABERGÉ — Special-Agent Mission Software** (**Spectral/UV Forgery Detection, Circus-Cover Logistics, and Concealed-Device Sweep**) implements three investigative disciplines under the mission codename **FABERGÉ**. First, artifact forgery detection fingerprints painted objects by their combined spectral reflectance and UV fluorescence. A ridge-regularized non-negative least-squares fit identifies each object's pigment composition; whether any pigment post-dates the object's claimed era, how strongly the unexplained spectral residue resembles an anachronistic pigment (matched filter), and the UV fluorescence reading jointly yield a forgery disposition. Against a deterministic exhibit of 4 artifacts drawn from a library of 14 pigments, the mission flags 2 as forged or likely-forged, with the all-modern composition *forged_dupe* carrying the highest score. Second, circus-cover smuggling logistics route a payload of trained cargo over a 9-segment rail corridor as minimum-cost flow via successive shortest paths; the resolved plan moves the payload with a makespan of 260 minutes using 2 circus trains, all within the stated capacity and deadline. Third, a concealed-device sweep over 100 detectors fuses a radiation anomaly map with shape/mass anomaly screening of 4 cargo containers, flagging hotspot@3,4, royal_egg. Every pipeline is fully deterministic under a fixed seed (7), producing reproducible, audit-ready provenance. Each discipline is deepened by a dedicated algorithm module. Forgery detection is reinforced by **varnish-ageing kinetics**: the exhibit's surface measures ~114.4 years (consistent with the claimed 1910 provenance), while the freshly varnished duplicate dates to just ~3.2 years and is rejected as too_young. Cover logistics gains **rolling-stock circulation**: 7 circus trips are covered by a minimum of 2 trainsets (a matching of 5 successor links, 100 deadhead minutes), with a depot allocation costing 38.0 minutes. The sweep gains **radiation source localization**: weighted Gauss–Newton estimation recovers the concealed source to within 0.066 metres (residual 28.664, converged: True).

## Sources

@nasdala2004faberge; @lawson2004hyperspectral; @feller1994accelerated; @horie2010materials; @ahuja1993network; @caprara2002train; @hopcroft1973matching; @kuhn1955hungarian; @nocedal2006numerical


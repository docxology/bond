# Moonraker (1979) — MOONRAKER

*film package · mission codename MOONRAKER*. Mission **DRAX**: model the shuttle hijack as a critical-path timeline; solve Drax station orbital logistics; certify a centrifuge g-force training profile; size the Hohmann resupply transfer and propellant; plan the centrifuge training regimen under exposure caps; crash the hijack timeline to a tighter deadline at minimum cost.

## Concepts

orbital logistics, centrifuge ops

## Abstract (imported from the package manuscript)

**Moonraker: DRAX — Special-Agent Mission Software** — Shuttle Hijack Timelining, Space-Station Orbital Logistics and Centrifuge G-Force Profiles. Mission codename **DRAX**, modelled on the 1979 film *Moonraker*, is a deterministic special-agent mission-software package. It operationalises the DRAX mission across three concept areas: the space-shuttle hijack as a critical-path timeline (including minimum-cost schedule crashing), Drax space-station orbital logistics (Kepler orbit physics, launch windows, consumables, the Hohmann resupply transfer and its propellant budget, and a Clohessy–Wiltshire rendezvous), and the centrifuge g-force training programme (the g-tolerance envelope plus an exposure-capped weekly regimen). The shuttle hijack plan completes in **57.0 minutes** across **8 phases**, feasible within the 60.0 point of no return (margin **3.0 min**), and can be crashed to a **50.0-minute** deadline at a cost of **23.0**. The DRAX station at 350.0 km has an orbital period of 5483.6 s and sustains **450 crew** on the configured resupply cadence. A Hohmann resupply transfer costs **0.0874 km/s** over **44.9 minutes**, needing **238.2 kg** of propellant; the final Clohessy–Wiltshire approach requires a **1.875 m/s** impulse. The **6.0 g** training profile is **no** and admits **4** sessions per week under the exposure caps. Every result is a closed-form, deterministic computation — no random draws, no external calls — enforcing the suite's reproducibility contract. Rendered 2026-08-04 23:57 UTC on Python 3.14.6 (Darwin).

## Sources

@kelley1959critical; @vallado2013astrodynamics; @stoll1956human; @moonraker1979; @hohmann1925; @clohessy1960; @tsiolkovsky1903; @burton1988


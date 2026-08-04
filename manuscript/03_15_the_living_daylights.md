# The Living Daylights (1987) — LIVING DAYLIGHTS

*film package · mission codename LIVING DAYLIGHTS*. Mission **SNIPER'S NEST**: sniper cover for a high-value defection (Bratislava); rules-of-engagement discipline (no shooting the innocent); cello-case concealment of a takedown sniper rifle; mountain/desert exfiltration with covered routes.

## Concepts

countersniper optics, defection

## Abstract (imported from the package manuscript)

The Living Daylights: SNIPER'S NEST — Special-Agent Mission Software (mission codename **SNIPER'S NEST**) is deterministic special-agent mission software for *The Living Daylights* (1987). It models three operational concepts with real, reproducible computation: * **Sniper ballistics** — a plug-and-play point-mass external-ballistics core that solves the rifle zero (fusing the trajectory to the sight line at 300 m), captures the near/far zero, and solves windage (a 5.0 m/s full-value crosswind imposes a 0.189 m drift requiring a -0.63 mrad hold), all embedded in a takedown rifle that conceals inside a cello case (true, 2 lanes, 0.241 packing efficiency, 72 s field assembly). * **Defection-handling protocol** — a staged, risk-scored pipeline (5 stages) whose weighted hazard model renders the canonical KOSKOV scenario conditional with a verify gate stage. * **Mountain/desert terrain ops** — a seeded (7) terrain grid ([@fig:ballistics]) on which a least-cost Dijkstra planner finds covered exfil routes (31.00 km, mean concealment 0.484). All results derive from a single deterministic mission solution ([`src/the_living_daylights/compute_mission.py`](../src/the_living_daylights/compute_mission.py)) so the manuscript, the mission report, and the figures can never drift apart. Keywords: sniper ballistics, rifle zero, windage, rules of engagement, defection protocol, risk scoring, terrain operations, cover planning, deterministic simulation.

## Sources

@friedman2026sniper; @bondapi2026


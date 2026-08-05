# The Living Daylights (1987) — LIVING DAYLIGHTS

*film package · mission codename LIVING DAYLIGHTS*. Mission **SNIPER'S NEST**: sniper cover for a high-value defection (Bratislava); rules-of-engagement discipline (no shooting the innocent); cello-case concealment of a takedown sniper rifle; mountain/desert exfiltration with covered routes.

## Concepts

countersniper optics, defection

## Abstract (imported from the package manuscript)

The Living Daylights: SNIPER'S NEST — Special-Agent Mission Software (mission codename **SNIPER'S NEST**) is deterministic special-agent mission software for *The Living Daylights* (1987). It models six operational concepts with real, reproducible computation across eight pure domain modules: * **Sniper ballistics** — a plug-and-play point-mass external-ballistics core that solves the rifle zero (fusing the trajectory to the sight line at 300 m), captures the near/far zero, and solves windage (a 5.0 m/s full-value crosswind imposes a 0.189 m drift requiring a -0.63 mrad hold), all embedded in a takedown rifle that conceals inside a cello case (true, 2 lanes, 0.241 packing efficiency, 72 s field assembly). * **Countersniper optics** — the 10x mil-dot riflescope ranges the 300 m target from a -2.68 mil holdover and dials the 27/-6 click solution; glint radiometry detects a hostile optic at 0.083 probability at 800 m. * **Countersniper detection** — a hostile sniper is ranged acoustically (687 m from the 2.0 s crack-bang delay at 20 °C) and localized by 2 crossed bearings to (50.0, 50.0) m at a 0.00 m residual. * **Defection-handling protocol** — a staged, risk-scored pipeline (5 stages) whose weighted hazard model renders the canonical KOSKOV scenario conditional with a verify gate stage and 0.670 backstop certainty (conditional). * **Mountain/desert terrain ops** — a seeded (7) terrain grid on which a cover-weighted least-cost Dijkstra planner finds covered exfil routes (31.00 km over 62 steps, mean concealment 0.484, corroborated at 0.484 by an independent cover audit). * **Overwatch selection** — of 16 in-range candidate positions only 1 see the extraction site; the ranked best nest at (6, 0) commands it from 3000 m with 1451.7 m elevation advantage. Two independent models — the staged plan's verify gate and the backstop certainty — agree on a conditional posture without sharing inputs. All results derive from a single deterministic mission solution ([`src/the_living_daylights/compute_mission.py`](../src/the_living_daylights/compute_mission.py)) so the manuscript, the mission report, and the figures can never drift apart. Keywords: sniper ballistics, rifle zero, windage, rules of engagement, riflescope optics, mil-dot ranging, countersniper detection, optic glint radiometry, acoustic crack-bang ranging, bearing triangulation, terrain visibility, viewshed, overwatch selection, defection protocol, evidence verification, risk scoring, terrain operations, cover planning, deterministic simulation.

## Sources

@friedman2026sniper; @bondapi2026; @fm2310sniper; @duckworth1996counter; @astmg173; @vantrees1968; @fisher1996viewshed; @kinsler2000; @ledeczi2005countersniper; @mccoy1999; @dijkstra1959; @bresenham1965


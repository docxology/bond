# Live and Let Die (1973) — SAN MONIQUE

*film package · mission codename SAN MONIQUE*. Mission **SAN MONIQUE**: map the narcotics supply graph and identify the critical transit bottleneck; decipher the voodoo-coded communiqué by symbol-substitution; plan an infiltration route across crocodile terrain to the airfield.

## Concepts

narcotics networks, coded comms

## Abstract (imported from the package manuscript)

--- title: "Live and Let Die: SAN MONIQUE — Special-Agent Mission Software" date: "2026-08-05T15:20:32+00:00" --- # Abstract Live and Let Die: SAN MONIQUE — Special-Agent Mission Software (mission codename **SAN MONIQUE**) delivers deterministic, special-agent mission software for Kananga's narcotics operation on the Caribbean island of San Monique. The system models the narcotics supply chain as a directed, capacity-constrained graph of 7 nodes and 10 legs spanning production, transit, and market. It recovers the cheapest route to each destination market (13 units to Miami), computes the maximum network throughput (220 units, capped by a min-cut value of 220), and identifies the single highest-value interdiction target: the **airfield**, whose neutralization stops 150 units of Miami throughput. Building on the graph core, a **budgeted interdiction** study shows the network is operationally fragile: an optimal 3-leg strike plan (greedy 220 units, exact optimum 220) severs the entire 220-unit operation, and the top individual target leg, field_works→harbor, is worth 50 units alone. The intelligence layer deciphers both a voodoo-coded communiqué by keyword symbol-substitution (key BARON, recovering *"KANANGA LETS THE SNAKE BITE"*) and a 195-beat drum-code transmission (exact round-trip, density 0.441) carrying *"KANANGA LETS THE SNAKE BITE"*. A market-flow economic model traces price and purity from the farm gate (300 $/kg) to the street, finding a farm gate-to-street spread of 59× and a producer share of just 1.7% of the 3888000 $ gross revenue. Finally, a terrain-graph infiltration planner routes an agent from the south landing beaches to the airfield at cost 41, wading 4 crocodile-water cells. All analyses are deterministic, real-data-only, and fully provenance-stamped (input hash `46044979efeafa09`).

## Sources

@film_lald; @cormen2009; @wood1993; @stinson2019; @itu2009; @reuter1986; @caulkins2010


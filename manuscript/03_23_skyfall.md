# Skyfall (2012) — SKYFALL

*film package · mission codename SKYFALL*. Mission **SILVA**: model the network intrusion paths into MI6's headquarters; detect the agent-list exfiltration burst in HQ traffic; compute the minimum severance cut that stops exfiltration; audit the aging legacy system exposure; schedule legacy patching under a daily budget; plan the Skyfall estate defense from its choke points.

## Concepts

cyber operations, legacy systems

## Abstract (imported from the package manuscript)

Skyfall is a PROJECT BOND mission-software package (film: Skyfall, 2012; codename **SILVA**) that models six linked threat surfaces through a purely deterministic computational core, grouped into three mission layers. The **cyber layer** models the intrusion paths an adversary can take into MI6's headquarters network, enumerating all simple routes and the minimum-hop / minimum-difficulty routes into the deepest system; it detects the agent-list exfiltration burst in HQ traffic with a periodic-baseline CUSUM change-point detector; and it computes the minimum severance cut (max-flow / min-cut) that stops the exfiltration. The **legacy layer** audits the aging infrastructure that still underpins operations, computing a closed-form exposure score per system from four normalized risk factors, an aggregate fleet risk, and a greedy patch schedule that minimizes cumulative exposure under a daily patching budget. The **physical-defense layer** computes Silva's island hideout topology by flood fill and the Skyfall estate's articulation (choke) points by Tarjan's algorithm, then plans a defender assignment that covers them. All results are reproducible: fixed inputs, no random draws, and no wall-clock in any persisted metric. The package implements the frozen BOND-API ``MissionProvider`` contract and registers its gadgets with the BOND gadget registry, making the SILVA mission discoverable by the suite's orchestrator. ## Concurrency of the six threats The mission treats the cyber intrusion (internet → registry, 6 simple paths), the exfiltration burst (detected at hour 180, window 180–190), the severance cut (max flow 8.0), the legacy-system exposure (fleet size 5, mean exposure 0.62), the patch back-log (12 vulnerabilities, cut by 89%), and the estate's choke-point defense (3 choke points, coverage 1.00) as one coordinated assault — the way the film depicts a single adversary reaching MI6's most sensitive systems through a chain of aging, poorly-segmented connections.

## Sources

@cormen2009algorithms; @even2011graph; @page1954continuous; @edmonds1972theoretical; @ford1962flows; @pinedo2016scheduling; @hawkins1999cumulative; @tarjan1972dfs; @hopcroft1973algorithm447; @dijkstra1959note; @phillips1998graphbased; @sheyner2002attackgraphs; @mell2007cvss; @beattie2002timing; @killick2012changepoints; @montgomery2012spc


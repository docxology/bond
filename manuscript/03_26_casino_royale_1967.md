# Casino Royale (1967) — FIVE BONDS

*film package · mission codename FIVE BONDS*. Mission **FIVE 00s**: model coordination failure across the five overlapping Bonds; simulate dispatch chaos and protocol violations deterministically; analyze the spoof ops doctrine and quantify its deviation; quantify identity confusion and resolve dispatch sightings by Bayes; derive exact baccarat table odds and the five-Bond table collision; model doctrine escalation as an absorbing Markov chain.

## Concepts

multi-agent farce, coordination failure

## Abstract (imported from the package manuscript)

*Casino Royale* (1967) is the spy farce in which five different operatives answer to the same codename, James Bond. This project — codename **FIVE 00s** — builds deterministic mission software around that premise. It implements and tests six concepts drawn from the film's organizational failure: 1. **Coordination-farce model** (`coordination_farce.py`): a roster of 5 agents who all share the codename *James Bond*, assigned across 6 tasks. It detects **overlap**, **conflict**, and clearance violations, and computes a weighted coordination loss of **15** from 3 overlaps and 3 conflicts. 2. **Dispatch-chaos simulation** (`dispatch_chaos.py`): a tick-based dispatch centre issues 13 orders and enforces 5 protocol rules; 5 dispatch successfully, 8 are rejected, for a chaos index of **0.62**. 3. **Spoof protocol analyzer** (`spoof_analyzer.py`): lexical scoring of satirical ops doctrine against a sane protocol; the film's standing orders score **45.0 / 100**. 4. **Identity-confusion model** (`identity_confusion.py`): information theory over the shared codename — routing carries only 0.075 normalized mutual information, leaving a dispatch ambiguity `H(routed | intended)` of 2.135 bits, and a Bayesian sighting resolves to *bond_cooper* with confidence 0.613. 5. **Baccarat table model** (`baccarat_table.py`): combinatorial deal odds exact for the infinite-deck model (player 0.4461, banker 0.4584, tie 0.0954) and a 5-Bond table collision probability of 0.704 under an i.i.d.-across-hands approximation. 6. **Escalation-ladder model** (`escalation_ladder.py`): the doctrine as an absorbing Markov chain — the spoof doctrine reaches catastrophe in 4.0 steps versus 56.0 under discipline, a 14.0× acceleration. All six models are deterministic (fixed seed, no random draws, no wall clock in artifacts) and are exposed through a `MissionProvider` implementing the frozen `bond_api` protocol, with a gadget registry and publication-style figures. Keywords: 5-agent coordination failure, agent dispatch simulation, protocol violations, satirical ops doctrine, identity confusion, baccarat odds, absorbing Markov chains, reproducible research.

## Sources

@shannon1948communication; @kemeny1960finite; @ethier2010doctrine; @wizardofodds_baccarat; @casinoroyale1967film; @cover2006elements; @strehl2002cluster


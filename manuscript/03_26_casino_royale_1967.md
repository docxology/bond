# Casino Royale (1967) — FIVE BONDS

*film package · mission codename FIVE BONDS*. Mission **FIVE 00s**: model coordination failure across the five overlapping Bonds; simulate dispatch chaos and protocol violations deterministically; analyze the spoof ops doctrine and quantify its deviation.

## Concepts

multi-agent farce, coordination failure

## Abstract (imported from the package manuscript)

*Casino Royale* (1967) is the spy farce in which five different operatives answer to the same codename, James Bond. This project — codename **FIVE 00s** — builds deterministic mission software around that premise. It implements and tests three concepts drawn from the film's organizational failure: 1. **Coordination-farce model** (`coordination_farce.py`): a roster of 5 agents who all share the codename *James Bond*, assigned across 6 tasks from the film's plot. The model detects **overlap** (multiple agents on one task) and **conflict** (agents on mutually exclusive task pairs), reports clearance violations, and computes a weighted coordination loss. The canonical assignment set of 8 orders yields 3 overlaps and 3 conflicts for a loss of **15**. 2. **Dispatch-chaos simulation** (`dispatch_chaos.py`): a tick-based dispatch centre issues 13 orders across the five Bonds and enforces five protocol rules (exclusive tasks, clearance, double-booking, duplicate orders, and duplicate codenames). 5 orders dispatch successfully, 8 are rejected as protocol violations, giving a chaos index of **0.62**. 3. **Spoof protocol analyzer** (`spoof_analyzer.py`): a lexical analyzer scores satirical ops doctrine against a sane protocol, detecting absolutist inversions and oxymorons. The film's standing orders score a spoof index of **45.0 / 100**. All three models are deterministic (fixed seed, no random draws, no wall clock in artifacts) and are exposed as a `MissionProvider` implementing the frozen `bond_api` protocol, with a gadget registry and publication-style figures. Keywords: 5-agent coordination failure, agent dispatch simulation, protocol violations, satirical ops doctrine, reproducible research.

## Sources

@friedman2026fivestart; @bondapi2026protocol; @casinoroyale1967film


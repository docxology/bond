# Bond Cli — THE FRONT DOOR

*infra package · mission codename THE FRONT DOOR*.

## Concepts

Unified terminal front door (bond list/brief/…/run/status/gadgets)

## Abstract (imported from the package manuscript)

bond-cli (version 3.0.0, codename THE FRONT DOOR) is the Layer-4 terminal front door of the PROJECT BOND suite — a fleet of 27 film packages plus shared mission infrastructure, each film package implementing the frozen `MissionProvider` protocol. As the front door, bond-cli is a thin dispatch layer: it routes 12 verb-first commands — list, brief, recon, plan, execute, debrief, run, status, gadgets, missions, whois, roster-export — to the 4 built sibling layers (bond-utilities, bond-api, bond-coordinator, bond-orchestrator) and maps their outcomes to deterministic exit codes. It implements no mission logic and ships no `MissionProvider` of its own; every command either loads a real film provider through the frozen `bond-api` discovery contract or delegates to the coordinator's registry and the orchestrator's runner. The deepened surface adds machine-readable `--json` output on 4 commands (list, status, missions, whois), a JSON roster export, color-safe aligned tables that never emit ANSI, and reconciliation of the fleet's measured gate manifest onto the registry so that reported status and coverage are measurements rather than intentions.

## Sources

@bethard2009argparse; @pythonargparse; @rfc8259; @posix2018; @raymond2003unix; @semver2


# Bond Cli — THE FRONT DOOR

*infra package · mission codename THE FRONT DOOR*.

## Concepts

Unified terminal front door (bond list/brief/…/run/status/gadgets)

## Abstract (imported from the package manuscript)

(version , codename ) is the Layer-4 terminal front door of the suite — a fleet of film packages plus shared mission infrastructure, each film package implementing the frozen `MissionProvider` protocol. As the front door, is a thin dispatch layer: it routes verb-first commands — — to the built sibling layers () and maps their outcomes to deterministic exit codes. It implements no mission logic and ships no `MissionProvider` of its own; every command either loads a real film provider through the frozen `bond-api` discovery contract or delegates to the coordinator's registry and the orchestrator's runner. The deepened surface adds machine-readable `--json` output on commands (), a JSON roster export, color-safe aligned tables that never emit ANSI, and reconciliation of the fleet's measured gate manifest onto the registry so that reported status and coverage are measurements rather than intentions.

## Sources

@bethard2009argparse; @pythonargparse; @rfc8259; @posix2018; @raymond2003unix; @semver2


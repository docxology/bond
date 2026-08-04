# Bond Cli — THE FRONT DOOR

*infra package · mission codename THE FRONT DOOR*.

## Concepts

Unified terminal front door (bond list/brief/…/run/status/gadgets)

## Abstract (imported from the package manuscript)

(codename ) is the Layer-4 terminal front door of the suite — a fleet of film packages plus shared mission infrastructure, each package implementing the frozen `MissionProvider` protocol. As the front door, is a thin dispatch layer: it routes the fleet's verb-first commands — `list`, `brief`, `recon`, `plan`, `execute`, `debrief`, `run`, `status`, `gadgets` — to the built sibling layers (bond-api protocol, bond-coordinator registry/status, bond-orchestrator mission runner, bond-utilities Q-branch) and maps their outcomes to deterministic exit codes. It owns no mission logic; every command either loads a real film provider through the `bond-api` discovery contract or delegates to the coordinator's registry and the orchestrator's runner.

## Sources

@argparse


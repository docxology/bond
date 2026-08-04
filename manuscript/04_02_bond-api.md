# Bond Api — THE PROTOCOL

*infra package · mission codename THE PROTOCOL*.

## Concepts

The frozen MissionProvider protocol, registry, discovery, serialization

## Abstract (imported from the package manuscript)

BOND-API (BOND-API, codename *THE PROTOCOL*) is the frozen mission protocol contract for the BOND film suite — Layer 1 of the suite. It defines 11 frozen dataclasses (Asset, Constraint, Debrief, Finding, MissionBrief, MissionOutcome, MissionPlan, Provenance, ReconReport, ReconRequest, Step) and a five-method provider contract (brief, recon, plan, execute, debrief) that every film package implements. The package ships the machinery every coordinator needs: deterministic JSON round-trip serialization for all protocol objects, a gadget registry and a mission/package registry for discovered providers, and slug-based film discovery on `sys.path`. A reference film (SABLE) exercises the full lifecycle. This is version 0.1.0 of the contract.

## Sources

@pep544; @pep557; @bond_api


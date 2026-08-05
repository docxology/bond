# Bond Api — THE PROTOCOL

*infra package · mission codename THE PROTOCOL*.

## Concepts

The frozen MissionProvider protocol, registry, discovery, serialization

## Abstract (imported from the package manuscript)

BOND-API (codename *THE PROTOCOL*) is the frozen mission protocol contract for the BOND film suite — Layer 1 of the suite. It defines 11 frozen dataclasses (Asset, Constraint, Debrief, Finding, MissionBrief, MissionOutcome, MissionPlan, Provenance, ReconReport, ReconRequest, Step) and a 5-method provider contract (brief, recon, plan, execute, debrief) that every film package implements. The package ships the machinery every coordinator needs: deterministic JSON round-trip serialization for all protocol objects, a gadget registry and a mission/package registry for discovered providers, slug-based film discovery on `sys.path`, and 9 capability helpers (brief_issues, derive_provenance, fingerprint, hash_provenance, normalize_debrief, normalize_lessons, plan_schema_issues, require_plan_schema, validate_brief) layered on the frozen surface — soft brief validation, plan-step schema checks, provenance hashing, and debrief normalization. A reference film (sable) exercises the full lifecycle, and the 27 film packages of the suite implement the same contract. Every artifact crosses process boundaries as tagged JSON (reserved key `__bond_type__`), and the suite enforces a 90% line-and-branch coverage floor on `src/`. This is version 0.1.0 of the contract.

## Sources

@pep544; @pep557; @pep484; @rfc8259; @nist_fips180_4; @bond_api


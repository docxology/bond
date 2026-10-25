# Data Directory — Agent Guide

Versioned project **inputs** only. Pipeline outputs must not be committed here.

## `claim_ledger.yaml`

Evidence-registry for manuscript claims that are intentionally sourced from code, examples, or generated reports rather than `{{VARIABLE}}` injection.

The compendium declares **no rows**: every number it prints is either imported from a source package's manuscript or injected as a `{{TOKEN}}` from live discovery (`src/bond_manuscript/manuscript_variables.py`). The file is kept for the schema, so a future claim that genuinely needs a ledger has a place to go.

### Schema (preserve when adding rows)

| Field | Purpose |
| --- | --- |
| `claim_id` | Stable identifier |
| `kind` | Claim category |
| `value` | Declared numeric or textual value |
| `source` | Provenance (module, manuscript section, artifact) |
| `source_tier` | Trust tier for validation |
| `freshness` | Staleness policy |
| `artifact_path` | Optional path to backing file |

## Edit protocol

1. Edit only when manuscript claims, figure defaults, or source-backed numeric facts change.
2. Re-run evidence validation / pipeline stages that consume the ledger.
3. Do not store generated CSV/JSON/PNG under `data/`.

Quick orientation: [`README.md`](README.md).

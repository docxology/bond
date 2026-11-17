"""Read the fleet gate evidence used by the wrapper manuscript."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GateRow:
    coverage: float | None
    status: str


def read_gate_manifest(bond_root: Path) -> dict[str, GateRow] | None:
    """Read bond-ops v1 or legacy coverage rows. Return None for an absent file."""
    path = bond_root / "output" / "aggregate" / "gate_manifest.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("packages"), list):
        raise ValueError(f"{path}: expected a packages list")
    v1 = payload.get("manifest") == "bond-ops-gate" and type(payload.get("schema_version")) is int and payload["schema_version"] == 1
    if not v1 and ("manifest" in payload or "schema_version" in payload):
        raise ValueError(f"{path}: unsupported gate manifest")

    results: dict[str, GateRow] = {}
    for row in payload["packages"]:
        if not isinstance(row, dict):
            raise ValueError(f"{path}: expected a package row")
        slug = row.get("slug" if v1 else "package")
        if not isinstance(slug, str) or not slug or slug != slug.strip() or slug in results:
            raise ValueError(f"{path}: invalid or duplicate package name {slug!r}")
        coverage = row.get("coverage")
        if coverage is not None and (
            type(coverage) not in (int, float) or not 0 <= coverage <= 100 or not math.isfinite(coverage)
        ):
            raise ValueError(f"{path}: invalid coverage for {slug}: {coverage!r}")
        results[slug] = GateRow(coverage, _v1_status(row) if v1 else "Legacy coverage row")
    return results


def _v1_status(row: dict[str, object]) -> str:
    slug = row["slug"]
    present, passed = row.get("present"), row.get("passed")
    stages = {stage: row[stage + "_passed"] for stage in ("pytest", "ruff", "mypy") if stage + "_passed" in row}
    if not isinstance(present, bool) or not isinstance(passed, bool) or len(stages) != 3:
        raise ValueError(f"{slug}: missing gate verdict or stage flags")
    if any(flag is not None and not isinstance(flag, bool) for flag in stages.values()):
        raise ValueError(f"{slug}: invalid stage flag")
    if passed != (present and stages["pytest"] is True and False not in stages.values()):
        raise ValueError(f"{slug}: gate verdict conflicts with stage flags")
    if not present:
        return "Missing package"
    if not passed:
        return "Failed"
    checked = ", ".join(stage for stage, flag in stages.items() if flag is True)
    return f"Passed ({checked})"

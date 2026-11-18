"""Regression tests for the wrapper's fleet evidence reader."""

import json
from pathlib import Path

import pytest

from bond_manuscript.gate_manifest import GateRow, read_gate_manifest


def _write(root: Path, payload: object) -> None:
    path = root / "output" / "aggregate" / "gate_manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _v1_row(slug: str, coverage: float | None = 99.25, **fields: object) -> dict[str, object]:
    return {
        "slug": slug, "present": True, "passed": True, "pytest_passed": True,
        "ruff_passed": None, "mypy_passed": None, "coverage": coverage, **fields,
    }


def _v1(*rows: dict[str, object]) -> dict[str, object]:
    return {"schema_version": 1, "manifest": "bond-ops-gate", "packages": list(rows)}


def test_measured_coverage_and_gate_verdict_are_distinct(tmp_path: Path) -> None:
    _write(tmp_path, _v1(
        _v1_row("bond-api"),
        _v1_row("bond-ops", 96, passed=False, pytest_passed=False),
        _v1_row("absent", None, present=False, passed=False, pytest_passed=None),
    ))
    assert read_gate_manifest(tmp_path) == {
        "bond-api": GateRow(99.25, "Passed (pytest)"),
        "bond-ops": GateRow(96, "Failed"),
        "absent": GateRow(None, "Missing package"),
    }


def test_legacy_reports_coverage_without_inferring_verdict(tmp_path: Path) -> None:
    assert read_gate_manifest(tmp_path) is None
    _write(tmp_path, {"packages": [{"package": "bond-api", "coverage": 100}]})
    assert read_gate_manifest(tmp_path) == {"bond-api": GateRow(100, "Legacy coverage row")}


@pytest.mark.parametrize("coverage", [True, float("inf"), float("nan"), -1, 101, "100"])
def test_rejects_invalid_measurements(tmp_path: Path, coverage: float) -> None:
    _write(tmp_path, _v1(_v1_row("bond-api", coverage)))
    with pytest.raises(ValueError, match="invalid coverage"):
        read_gate_manifest(tmp_path)


@pytest.mark.parametrize("rows, diagnostic", [
    ([_v1_row("bond-api"), _v1_row("bond-api")], "duplicate"),
    ([_v1_row("bond-api", ruff_passed=0)], "invalid stage flag"),
    ([_v1_row("bond-api", ruff_passed=False)], "conflicts with stage flags"),
])
def test_rejects_ambiguous_rows(tmp_path: Path, rows: list[dict[str, object]], diagnostic: str) -> None:
    _write(tmp_path, _v1(*rows))
    with pytest.raises(ValueError, match=diagnostic):
        read_gate_manifest(tmp_path)

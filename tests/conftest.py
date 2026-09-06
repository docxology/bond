"""Pytest configuration for bond-manuscript tests."""

import os
import sys

# Force headless backend for matplotlib in tests
os.environ.setdefault("MPLBACKEND", "Agg")

# Add the repo root AND src/ to path so the documented per-project pytest command
# works from a clean environment. The project pyproject's `pythonpath` is
# project-relative, so this is belt-and-braces for bare invocations from elsewhere.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
for _path in (ROOT, SRC):
    if _path not in sys.path:
        sys.path.insert(0, _path)

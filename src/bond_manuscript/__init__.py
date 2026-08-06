"""bond_manuscript — the PROJECT BOND compendium generator (public API)."""

from __future__ import annotations

from .compendium import (
    ImportedChapter,
    PackageInfo,
    Reference,
    build_architecture_section,
    build_package_section,
    build_references_bib,
    build_references_section,
    discover_packages,
    import_package_abstract,
    import_package_sections,
    parse_references,
)

__all__ = [
    "ImportedChapter",
    "PackageInfo",
    "Reference",
    "build_architecture_section",
    "build_package_section",
    "build_references_bib",
    "build_references_section",
    "discover_packages",
    "import_package_abstract",
    "import_package_sections",
    "parse_references",
]

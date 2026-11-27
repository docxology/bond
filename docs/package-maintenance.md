# Maintain the bond-manuscript package

The distribution at this revision is `bond-manuscript` 1.0.0, with
Python compatibility `>=3.11`. This checkout selects Python 3.15 in [`.python-version`](../.python-version).
[Project metadata](../pyproject.toml) declares the package and compatibility.
[The lockfile](../uv.lock) records resolved dependency versions and sources.

## Dependency provenance

- `bond-coordinator` resolves to a sibling checkout at `../bond-coordinator`. The
  lockfile records the relative path. A different checkout at that
  path can supply different source bytes.
- `bond-utilities` resolves to a sibling checkout at `../bond-utilities`. The
  lockfile records the relative path. A different checkout at that
  path can supply different source bytes.

## Citation and release records

The repository records package metadata in:

- [Citation metadata](../CITATION.cff)
- [CodeMeta](../codemeta.json)
- [Zenodo metadata](../.zenodo.json)

Version 1.0.0 has a [GitHub release](https://github.com/docxology/bond/releases/tag/v1.0.0)
and a [versioned Zenodo record](https://doi.org/10.5281/zenodo.21843802).
The [concept DOI](https://doi.org/10.5281/zenodo.21843592) identifies the
series. Use the versioned record when comparing the deposited files.

For a documentation review, run `git diff --check` and verify the relative
links added by the change against the tracked checkout. These checks
provide evidence about the documentation and package records.

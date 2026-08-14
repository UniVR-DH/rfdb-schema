# Changelog

All notable changes to this repository are documented here.
Versioning follows [SemVer](https://semver.org/): MAJOR for breaking schema changes, MINOR for backward-compatible additions, PATCH for non-breaking corrections.

## [Unreleased]

- Added `docs/data-model.md` documenting modeling principles and design decisions (vocabularies used, WEMI layering, bridge-node pattern, literal/language/date/IRI policies). README expanded with a Data Model section and Main SHACL Shapes list.
- Fixed `data/examples/data.ttl`: removed stray local redeclarations of `rfdb:Librettista`, `rfdb:Compositore`, `rfdb:Traduttore`, `rfdb:LibrettoManoscritto`, and `rfdb:LibrettoStampa` that duplicated `data/vocab.ttl` with conflicting labels, causing SHACL conformance failures (`maxCount 1` on `rdfs:label`) when both files were loaded together.
- Added pre-commit hooks and CI (`.pre-commit-config.yaml`, `.github/workflows/ci.yml`) validating Turtle syntax, SHACL self-consistency of `schema/schema.ttl`, and conformance of `data/examples/data.ttl` against the schema.
- Added `.external/` — Git LFS-tracked snapshots of the external vocabularies the schema references (LRMoo, CIDOC CRM, Polifonia Core/Music Meta/Source, Glottolog). Reference-only; excluded from validation.

## [1.0.0] - 2026-08-13

- Initial release of `schema/schema.ttl`, `data/vocab.ttl`, and `data/examples/data.ttl`.

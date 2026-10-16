# Changelog

All notable changes to this repository are documented here.
Versioning follows [SemVer](https://semver.org/): MAJOR for breaking schema changes, MINOR for backward-compatible additions, PATCH for non-breaking corrections.

## [1.0.2] - 2026-10-16

PATCH: metadata only. No shape or constraint changes, so data valid under 1.0.1 still validates.

- `schema/schema.ttl` declares its own version and prefix map as data: an `owl:Ontology` node `rfdbs:` with `owl:versionInfo` and one `sh:declare` per `@prefix` line.
- `scripts/validate_shacl.py` checks that the `sh:declare` set matches the `@prefix` lines and that exactly one `owl:versionInfo` is present.

## [1.0.1] - 2026-10-16

- Added Italian `skos:altLabel`s to `rfdb:DocumentTypeScheme`, `rfdb:RoleTypeScheme` and `rfdb:Libretto` in `data/vocab.ttl`.
- Added `docs/data-model.md`: modeling principles and design decisions (vocabularies used, WEMI layering, the bridge-node pattern, literal/language/date/IRI policies). The README gains a Data Model section and the list of main SHACL shapes.
- Added pre-commit hooks and CI (`.pre-commit-config.yaml`, `.github/workflows/ci.yml`) that check Turtle syntax, the SHACL self-consistency of `schema/schema.ttl`, and the conformance of `data/examples/data.ttl` to the schema.
- Added `.external/`: Git LFS snapshots of the external vocabularies the schema references (LRMoo, CIDOC CRM, Polifonia Core/Music Meta/Source, Glottolog), for reference only and excluded from validation.

## [1.0.0] - 2026-08-13

- Initial release of `schema/schema.ttl`, `data/vocab.ttl`, and `data/examples/data.ttl`.
- SHACL shapes: `rfdbs:MusicalWorkShape`, `rfdbs:ExpressionShape`, `rfdbs:ManifestationShape`, `rfdbs:SourceShape`, `rfdbs:DigitalCopyShape`, `rfdbs:PersonShape`, `rfdbs:RoleShape`, `rfdbs:AgentRoleShape`, `rfdbs:PlaceShape`, `rfdbs:SubjectShape`, `rfdbs:SourceTypeShape`, `rfdbs:HoldingOrganizationShape`, `rfdbs:ContributorShape`, `rfdbs:PerformanceShape`, `rfdbs:LanguageShape`.

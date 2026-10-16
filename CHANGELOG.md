# Changelog

All notable changes to this repository are documented here.
Versioning follows [SemVer](https://semver.org/): MAJOR for breaking schema changes, MINOR for backward-compatible additions, PATCH for non-breaking corrections.

## [2.0.0] - 2026-10-16

MAJOR: a VIAF ID stored as a link on a Person or Holding Organization no longer validates.

- `wdt:P214` (VIAF) holds the bare ID text, as Wikidata stores it for an external identifier, e.g. `"100995617"` rather than `<https://viaf.org/viaf/100995617>`. It is `xsd:string` and must match Wikidata's VIAF ID format. Migrate existing values by keeping only the digits. The shape descriptions give the rule for building the link: `http://viaf.org/viaf/` followed by the ID.
- `rfdbs:MusicalWorkShape` and `rfdbs:ExpressionShape` gain the same optional `wdt:P214`, since VIAF clusters works and expressions too. VIAF no longer goes in a Work's `owl:sameAs`.
- `docs/data-model.md` gains an "External authority links" section: VIAF identifies agents, works and expressions, never manifestations or items.

## [1.1.1] - 2026-10-16

PATCH: metadata only. No shape or constraint changes, so data valid under 1.1.0 still validates.

- `schema/schema.ttl` declares `wd` (`http://www.wikidata.org/entity/`), used by `data/examples/data.ttl`, as a `@prefix` line with a matching `sh:declare`, so the prefix map covers the data files too.
- `scripts/validate_shacl.py` checks that every prefix of every Turtle file under `data/` appears in `sh:declare` with the same namespace. The pre-commit hook now runs on any `.ttl` file under `data/`.

## [1.1.0] - 2026-10-16

MINOR: new prefix declarations only. No shape or constraint changes, so data valid under 1.0.2 still validates.

- `schema/schema.ttl` declares the namespaces used by the integrated external vocabularies (Polifonia Core, Music Meta and Source; Glottolog): `dc`, `cc`, `vann`, `bibo`, `dctype`, `frbr`, `geo`, `gold`, `isbd`, `lexvo`, `vcard` and `void`, each as a `@prefix` line with a matching `sh:declare`.

## [1.0.2] - 2026-10-16

PATCH: metadata only. No shape or constraint changes, so data valid under 1.0.1 still validates.

- `schema/schema.ttl` declares its own version and prefix map as data: an `owl:Ontology` node `rfdbs:` with `owl:versionInfo` and one `sh:declare` per `@prefix` line.
- `scripts/validate_shacl.py` checks that the `sh:declare` set matches the `@prefix` lines and that exactly one `owl:versionInfo` is present.

## [1.0.1] - 2026-10-16

- Added Italian `skos:altLabel`s to `rfdb:DocumentTypeScheme`, `rfdb:RoleTypeScheme` and `rfdb:Libretto` in `data/vocab.ttl`.
- Removed stray redeclarations of `rfdb:Librettista`, `rfdb:Compositore`, `rfdb:Traduttore`, `rfdb:LibrettoManoscritto` and `rfdb:LibrettoStampa` from `data/examples/data.ttl`. They duplicated `data/vocab.ttl` with conflicting labels, so the two files loaded together failed SHACL validation (`sh:maxCount 1` on `rdfs:label`).
- Added `docs/data-model.md`: modeling principles and design decisions (vocabularies used, WEMI layering, the bridge-node pattern, literal/language/date/IRI policies). The README gains a Data Model section and the list of main SHACL shapes.
- Added pre-commit hooks and CI (`.pre-commit-config.yaml`, `.github/workflows/ci.yml`) that check Turtle syntax, the SHACL self-consistency of `schema/schema.ttl`, and the conformance of `data/examples/data.ttl` to the schema.
- Added `.external/`: Git LFS snapshots of the external vocabularies the schema references (LRMoo, CIDOC CRM, Polifonia Core/Music Meta/Source, Glottolog), for reference only and excluded from validation.

## [1.0.0] - 2026-08-13

- Initial release of `schema/schema.ttl`, `data/vocab.ttl`, and `data/examples/data.ttl`.
- SHACL shapes: `rfdbs:MusicalWorkShape`, `rfdbs:ExpressionShape`, `rfdbs:ManifestationShape`, `rfdbs:SourceShape`, `rfdbs:DigitalCopyShape`, `rfdbs:PersonShape`, `rfdbs:RoleShape`, `rfdbs:AgentRoleShape`, `rfdbs:PlaceShape`, `rfdbs:SubjectShape`, `rfdbs:SourceTypeShape`, `rfdbs:HoldingOrganizationShape`, `rfdbs:ContributorShape`, `rfdbs:PerformanceShape`, `rfdbs:LanguageShape`.

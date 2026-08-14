# rfdb-schema

Canonical SHACL schema, vocabulary, and optional example RDF data for the RossijskijFeatrDB (rfdb) project — a curated RDF knowledge base of Russian theatrical works and their libretti, modeled on IFLA LRM / LRMoo (WEMI) and CIDOC-CRM.

This repository is the single source of truth for the shared schema and vocabulary. Consumer repositories pin a tagged release and sync files from here rather than maintaining their own copies.

## Contents

- `schema/schema.ttl` — SHACL shapes constraining the data model (LRMoo + CIDOC-CRM alignment).
- `data/vocab.ttl` — shared controlled vocabulary/terms used by the schema.
- `data/examples/data.ttl` — optional example data illustrating the model (a musical work, its libretto expressions and editions, performance, agents, roles, and sources). Consumers may skip this file entirely — it is not required for validation against the schema.
- `docs/data-model.md` — modeling principles and design decisions behind the schema: vocabularies used and for what, WEMI layering and link direction, the Agent Role bridge pattern, and the literal/language/date/IRI policies.
- `.external/` — snapshotted copies of the external vocabularies the schema references, stored via [Git LFS](#external-vocabularies). Reference-only; not validated.
- `CHANGELOG.md` — release history and SemVer rationale per version.

## Data Model

The model uses [LRMoo](https://cidoc-crm.org/lrmoo/) (rather than the older FRBR/FaBiO model) and draws on [LRMoo](https://cidoc-crm.org/lrmoo/), [CIDOC CRM](https://cidoc-crm.org/), the Polifonia [Core](https://github.com/polifonia-project/core-ontology) / [Music Meta](https://github.com/polifonia-project/music-meta-ontology) / [Source](https://github.com/polifonia-project/source-ontology) ontologies, [Dublin Core Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/), [PRISM](https://www.w3.org/submissions/prism/), [SKOS](https://www.w3.org/TR/skos-reference/), [FOAF](http://xmlns.com/foaf/spec/), [Schema.org](https://schema.org/), [Wikidata](https://www.wikidata.org/) direct properties, and RDF/RDFS/OWL/XSD.

LRMoo hierarchy: a **Musical Work** is the abstract work; an **Expression** is an intellectual realization (e.g. a libretto); a **Manifestation** is an edition or product type; a **Source / Item** is a specific physical or documentary copy. Each level refines the one above it, from Work through Expression and Manifestation to Source/Item, and every WEMI link points from the more concrete record up to its parent — so create parents before children.

### Main SHACL Shapes

The schema includes these primary record types:

- `rfdbs:MusicalWorkShape`: musical work, targeting `mm:MusicEntity`, constrained as `lrmoo:F1_Work`
- `rfdbs:ExpressionShape`: expression, targeting `lrmoo:F2_Expression`
- `rfdbs:ManifestationShape`: manifestation, targeting `lrmoo:F3_Manifestation`
- `rfdbs:SourceShape`: source/item, targeting `source:Source` and `lrmoo:F5_Item`
- `rfdbs:DigitalCopyShape`: digital copy (e.g. PDF scan) of a source, targeting `schema:DigitalDocument`
- `rfdbs:PersonShape`: person, targeting `core:Person`
- `rfdbs:RoleShape`: role, targeting `core:Role`
- `rfdbs:AgentRoleShape`: agent-role assignment, targeting `core:AgentRole`
- `rfdbs:PlaceShape`: place, targeting `core:Place`
- `rfdbs:SubjectShape`: subject, targeting `cidoc:E89_Propositional_Object`
- `rfdbs:SourceTypeShape`: source type, targeting `core:Type`
- `rfdbs:HoldingOrganizationShape`: holding organization, targeting `core:Organization`
- `rfdbs:ContributorShape`: donor/contributor record for digital-copy provenance
- `rfdbs:PerformanceShape`: staged performance, targeting `lrmoo:F31_Performance`
- `rfdbs:LanguageShape`: controlled-vocabulary language record, targeting `dcterms:LinguisticSystem` (seeded from [Glottolog](https://glottolog.org/))

Shapes with a `sh:property` on `rdfs:label` are standalone entities with their own identity and lifecycle; shapes without one are helper/bridge nodes meant to be handled inline wherever a parent shape references them (e.g. `rfdbs:AgentRoleShape`).

> Modeling principles and design decisions — the vocabularies used and for what, WEMI layering and link direction, the Agent Role bridge pattern, and the literal/language/date/IRI policies — are in [docs/data-model.md](docs/data-model.md). Per-shape fields and cardinalities live in the schema itself (`schema/schema.ttl`).

## External Vocabularies

`.external/` holds point-in-time snapshots of the external ontologies and vocabularies the schema references, kept for offline lookup and reference — not for validation:

| File | Vocabulary |
|---|---|
| `.external/lrmoo.ttl` | [LRMoo](https://cidoc-crm.org/lrmoo/) |
| `.external/cidoc.ttl` | [CIDOC CRM](https://cidoc-crm.org/) |
| `.external/core.ttl` | [Polifonia Core](https://github.com/polifonia-project/core-ontology) |
| `.external/mm.ttl` | [Polifonia Music Meta](https://github.com/polifonia-project/music-meta-ontology) |
| `.external/source.ttl` | [Polifonia Source](https://github.com/polifonia-project/source-ontology) |
| `.external/glottolog_language.ttl` | [Glottolog](https://glottolog.org/) language vocabulary |

These are stored via [Git LFS](https://git-lfs.com/) — `glottolog_language.ttl` alone is tens of megabytes. [git-lfs](https://git-lfs.com/) must be installed for `git clone`/`git pull` to fetch the actual content; without it you get small LFS pointer files instead. They are excluded from pre-commit/CI validation (see `.pre-commit-config.yaml`'s top-level `exclude`) and are not required to consume or validate against `schema/schema.ttl` — the canonical, up-to-date version of each vocabulary is at the linked URL above.

## Versioning

Releases are tagged `vX.Y.Z` following SemVer:

- **MAJOR** — breaking schema changes (removed classes/properties, stricter constraints that invalidate previously-valid data).
- **MINOR** — backward-compatible additions (new optional properties/classes, non-breaking vocabulary expansion).
- **PATCH** — corrections and non-breaking maintenance (typos, docs, examples, metadata).

Each tag is an immutable, content-addressed snapshot of the full tree (schema, vocabulary, and examples together) — there is no separate release channel for examples; consumers that don't want them simply don't copy that path.

## Consuming this repo

Pin a tag and sync only the files you need, e.g.:

```bash
git clone --depth 1 --branch v0.1.1 https://github.com/<org>/rfdb-schema.git /tmp/rfdb-schema
cp /tmp/rfdb-schema/schema/schema.ttl path/to/your/schema.ttl
cp /tmp/rfdb-schema/data/vocab.ttl path/to/your/vocab.ttl
# optional:
cp /tmp/rfdb-schema/data/examples/data.ttl path/to/your/examples/data.ttl
```

Integrity is guaranteed by git's own content hashing of the tag — no separate checksum files are published.

Consumers only need `schema/`, `data/vocab.ttl`, and optionally `data/examples/data.ttl` — none of which are LFS-tracked. `.external/` is reference-only and safe to skip; set `GIT_LFS_SKIP_SMUDGE=1` before cloning to avoid fetching its LFS content entirely.

## Development

Changes are validated with [pre-commit](https://pre-commit.com/) via [uv](https://docs.astral.sh/uv/): Turtle syntax for every `.ttl` file, SHACL self-consistency of `schema/schema.ttl`, and conformance of `data/examples/data.ttl` against the schema (loaded together with `data/vocab.ttl`). The same checks run in CI on every push and pull request (`.github/workflows/ci.yml`).

To enable the checks locally:

```bash
uvx pre-commit install
```

To run them on demand without installing the git hook:

```bash
uvx pre-commit run --all-files
```

## License

Released under CC0 1.0 — see [LICENSE](LICENSE). You may use, modify, and redistribute the schema, vocabulary, and example data without restriction.

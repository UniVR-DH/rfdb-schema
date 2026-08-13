# rfdb-schema

Canonical SHACL schema, vocabulary, and optional example RDF data for the RossijskijFeatrDB (rfdb) project — a curated RDF knowledge base of Russian theatrical works and their libretti, modeled on IFLA LRM / LRMoo (WEMI) and CIDOC-CRM.

This repository is the single source of truth for the shared schema and vocabulary. Consumer repositories pin a tagged release and sync files from here rather than maintaining their own copies.

## Contents

- `schema/schema.ttl` — SHACL shapes constraining the data model (LRMoo + CIDOC-CRM alignment).
- `data/vocab.ttl` — shared controlled vocabulary/terms used by the schema.
- `data/examples/data.ttl` — optional example data illustrating the model (a musical work, its libretto expressions and editions, performance, agents, roles, and sources). Consumers may skip this file entirely — it is not required for validation against the schema.
- `CHANGELOG.md` — release history and SemVer rationale per version.

## Versioning

Releases are tagged `vX.Y.Z` following SemVer:

- **MAJOR** — breaking schema changes (removed classes/properties, stricter constraints that invalidate previously-valid data).
- **MINOR** — backward-compatible additions (new optional properties/classes, non-breaking vocabulary expansion).
- **PATCH** — corrections and non-breaking maintenance (typos, docs, examples, metadata).

Each tag is an immutable, content-addressed snapshot of the full tree (schema, vocabulary, and examples together) — there is no separate release channel for examples; consumers that don't want them simply don't copy that path.

## Consuming this repo

Pin a tag and sync only the files you need, e.g.:

```bash
git clone --depth 1 --branch v0.4.2 https://github.com/<org>/rfdb-schema.git /tmp/rfdb-schema
cp /tmp/rfdb-schema/schema/schema.ttl path/to/your/schema.ttl
cp /tmp/rfdb-schema/data/vocab.ttl path/to/your/vocab.ttl
# optional:
cp /tmp/rfdb-schema/data/examples/data.ttl path/to/your/examples/data.ttl
```

Integrity is guaranteed by git's own content hashing of the tag — no separate checksum files are published.

## License

Released under CC0 1.0 — see [LICENSE](LICENSE). You may use, modify, and redistribute the schema, vocabulary, and example data without restriction.

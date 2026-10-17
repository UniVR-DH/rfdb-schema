# rfdb Schema: Rules for Consuming Applications

Rules any application that reads or writes data under the rfdb schema must follow. The
model itself is described in the [data model](data-model.md); where this document and
[`schema/schema.ttl`](../schema/schema.ttl) disagree, the schema wins.

---

## Model alignment policy

The model is SHACL-driven. Consequently, any consuming application should follow these
conventions:

- the schema in this repository is the single source of truth;
- consumers make no hard-coded ontology assumptions beyond what the schema declares;
- ontology-specific behavior stays isolated in schema-parsing and mapping code, not
  scattered through application logic;
- validation semantics in a consuming application stay consistent with the schema's
  extracted shape metadata.

---

## Class-targeted validation requires explicit `@type`

Shapes use `sh:targetClass`, so a shape's constraints only run against a node that
declares the matching RDF class. **Payloads must therefore carry explicit `@type`
values** — most importantly [bridge nodes](data-model.md#standalone-entities-vs-helperbridge-nodes), which the schema validates by class (an
`AgentRole` payload must include `core:AgentRole` in its `@type`). Omitting `@type` can
silently skip constraints.

---

## Literal, language-tag, and date policies

These are **principles any consuming application must honor**; the exact per-field
datatype for any property lives in the schema.

- **Literal kinds are distinguished, not flattened.** A field is one of: plain string,
  language-tagged string (`rdf:langString`), full date, year-only date, year-month date,
  or IRI. Consumers should render and validate each accordingly.
- **Language tags are first-class.** Where a field is `rdf:langString`, the tag must be
  entered, validated, and preserved through any export format — and, where the schema
  sets `sh:uniqueLang true`, enforced as unique per language.
- **Date precision is preserved.** The schema permits `xsd:date`, `xsd:gYear`, and
  `xsd:gYearMonth`. A year-only value must **not** be silently promoted to a full date;
  the recorded precision is the datum.

---

## IRI policy

Every persisted resource has a stable subject IRI in the `rfdb:` (data) or `rfdbs:`
(shape) namespace. The rules:

- existing IRIs are never silently changed;
- new IRIs follow a consistent generation policy (helper/bridge IRIs are regular named
  nodes, not blank nodes, so they survive updates);
- both full and prefixed IRIs are accepted on input;
- invalid IRIs are rejected before persistence.

---

## Naming across layers

Keep three naming levels distinct in code, UI, and docs — conflating them loses either
readability or RDF precision:

- **User-facing labels** — "Musical Work", "Source", "Holding Organization".
- **SHACL shape names** — `rfdbs:MusicalWorkShape`, `rfdbs:SourceShape`.
- **RDF classes and predicates** — `mm:MusicEntity`, `lrmoo:F2_Expression`,
  `core:hasAgentRole`.

Each property shape carries its field's user-facing label as `sh:name`, in English and
Italian (e.g. "RISM ID" for `wdt:P5504`). Label form fields from it, not from the predicate.

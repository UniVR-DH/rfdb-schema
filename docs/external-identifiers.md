# rfdb Schema: External Identifiers

How the schema records identifiers from external authority files, and at which level of the
WEMI layering described in the [data model](data-model.md) each one belongs. Where this
document and [`schema/schema.ttl`](../schema/schema.ttl) disagree, the schema wins.

---

## VIAF

[VIAF](https://viaf.org/) clusters authority records for agents (persons and corporate
bodies), for works, and for expressions such as translations. An expression cluster
points to its work cluster with `schema:exampleOfWork`: for instance
[*Arien und Gesänge aus Marquis Tulipano*](https://viaf.org/en/viaf/308534901), a German
version (1811) of Paisiello's *Matrimonio inaspettato*, points to the work cluster
[`293925180`](https://viaf.org/en/viaf/293925180). Both are typed `schema:CreativeWork`, so
that link, not the type, tells the two levels apart. VIAF is an authority file, not a
holdings catalogue: it issues no identifiers for manifestations (editions) or items
(copies).

A VIAF link therefore belongs only on records at those levels: Person, Holding
Organization, Musical Work, Expression. Never attach one to a Manifestation or a Source.
The ID goes in `wdt:P214` as bare text, the way Wikidata stores it, not as a link and not
in `owl:sameAs`; the shapes describe how to build the VIAF IRI from it.
Catalogue records for a specific copy go in the Source's `rdfs:seeAlso`.

## RISM

[RISM](https://rism.online/) identifies people, institutions and sources, each ID being the
record type and a number, e.g. `people/1874`. A RISM source record, print or manuscript,
describes a manifestation and lists its exemplars beneath it, each exemplar with its own
IRI: the 1736 print [`sources/990052516`](https://rism.online/sources/990052516) of
favourite songs from *Orfeo* has exemplars in several libraries, among them
[`sources/990052516/holdings/204680`](https://rism.online/sources/990052516/holdings/204680).
The RISM ID therefore goes in `wdt:P5504`, again as Wikidata stores it, on Person, Holding
Organization and Manifestation. An exemplar corresponds to a Source; its IRI goes in the
Source's `rdfs:seeAlso`, because Wikidata's RISM ID does not cover exemplars. That is the
only kind of RISM link a Source accepts.

## Building links from IDs

The schema stores these IDs only. Turning one into an IRI or a web address is left to the
consuming application, and the schema does not restate the link templates as data.
Wikidata defines them on the properties themselves, with `$1` standing for the ID:

- [VIAF ID (P214)](https://www.wikidata.org/wiki/Property:P214): the IRI of the VIAF
  record is its "formatter URI for RDF resource" (P1921), `http://viaf.org/viaf/$1`; the
  web page is its "formatter URL" (P1630), `https://viaf.org/en/viaf/$1`.
- [RISM ID (P5504)](https://www.wikidata.org/wiki/Property:P5504): use its "formatter URL"
  (P1630), `https://rism.online/$1`, which is also the form of RISM's own record IRIs. Its
  P1921 value names an RDF file on an obsolete domain.

Where Wikidata changes these values, Wikidata wins.

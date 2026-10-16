#!/usr/bin/env python3
"""Validate the rfdb SHACL schema and example data.

Three checks:
1. schema/schema.ttl is well-formed SHACL (meta-SHACL validation).
2. schema/schema.ttl declares its own metadata: exactly one owl:versionInfo
   on an owl:Ontology node, and one sh:declare per @prefix line with the
   same namespace. @prefix lines are lost on parsing, so they are read from
   the file's text.
3. data/examples/data.ttl conforms to schema/schema.ttl once loaded
   together with the shared vocabulary in data/vocab.ttl.

Run via: uv run --with-requirements scripts/requirements.txt scripts/validate_shacl.py
"""

import re
import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "schema.ttl"
VOCAB = ROOT / "data" / "vocab.ttl"
EXAMPLE = ROOT / "data" / "examples" / "data.ttl"

PREFIX_LINE = re.compile(r"^@prefix\s+([\w-]*):\s*<([^>]*)>\s*\.", re.MULTILINE)


def load_graph(*paths: Path) -> Graph:
    graph = Graph()
    for path in paths:
        graph.parse(str(path), format="turtle")
    return graph


def check_meta_shacl() -> bool:
    print(f"--- SHACL self-validation ({SCHEMA.relative_to(ROOT)}) ---")
    shapes_graph = load_graph(SCHEMA)
    conforms, _, report = validate(shapes_graph, shacl_graph=shapes_graph, meta_shacl=True)
    print(report)
    return conforms


def check_schema_metadata() -> bool:
    print(f"--- Schema metadata ({SCHEMA.relative_to(ROOT)}) ---")
    prefix_lines = PREFIX_LINE.findall(SCHEMA.read_text(encoding="utf-8"))
    graph = load_graph(SCHEMA)
    ok = True

    versions = list(graph.query(
        "PREFIX owl: <http://www.w3.org/2002/07/owl#> "
        "SELECT ?v WHERE { ?o a owl:Ontology ; owl:versionInfo ?v }"
    ))
    if len(versions) != 1:
        print(f"Expected exactly one owl:versionInfo on an owl:Ontology node, found {len(versions)}")
        ok = False

    declared = [
        (str(p), str(ns))
        for p, ns in graph.query(
            "PREFIX sh: <http://www.w3.org/ns/shacl#> "
            "SELECT ?p ?ns WHERE { ?o sh:declare [ sh:prefix ?p ; sh:namespace ?ns ] }"
        )
    ]
    if len({p for p, _ in declared}) != len(declared):
        print("A prefix is declared more than once in sh:declare")
        ok = False
    if set(declared) != set(prefix_lines):
        for p, ns in sorted(set(prefix_lines) - set(declared)):
            print(f"@prefix {p}: <{ns}> has no matching sh:declare")
        for p, ns in sorted(set(declared) - set(prefix_lines)):
            print(f"sh:declare {p} <{ns}> has no matching @prefix line")
        ok = False

    if ok:
        print(f"OK: version {versions[0][0]}, {len(declared)} prefixes declared")
    return ok


def check_example_data() -> bool:
    if not EXAMPLE.exists():
        print(f"--- Skipping example data check: {EXAMPLE} not found ---")
        return True

    print(f"--- Example data conformance ({VOCAB.relative_to(ROOT)} + {EXAMPLE.relative_to(ROOT)}) ---")
    data_graph = load_graph(VOCAB, EXAMPLE)
    shacl_graph = load_graph(SCHEMA)
    conforms, _, report = validate(data_graph, shacl_graph=shacl_graph)
    print(report)
    return conforms


def main() -> int:
    meta_ok = check_meta_shacl()
    metadata_ok = check_schema_metadata()
    data_ok = check_example_data()
    return 0 if (meta_ok and metadata_ok and data_ok) else 1


if __name__ == "__main__":
    sys.exit(main())

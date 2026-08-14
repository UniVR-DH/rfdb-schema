#!/usr/bin/env python3
"""Validate the rfdb SHACL schema and example data.

Two checks:
1. schema/schema.ttl is well-formed SHACL (meta-SHACL validation).
2. data/examples/data.ttl conforms to schema/schema.ttl once loaded
   together with the shared vocabulary in data/vocab.ttl.

Run via: uv run --with-requirements scripts/requirements.txt scripts/validate_shacl.py
"""

import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "schema.ttl"
VOCAB = ROOT / "data" / "vocab.ttl"
EXAMPLE = ROOT / "data" / "examples" / "data.ttl"


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
    data_ok = check_example_data()
    return 0 if (meta_ok and data_ok) else 1


if __name__ == "__main__":
    sys.exit(main())

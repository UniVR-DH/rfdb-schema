#!/usr/bin/env python3
"""Validate that each given file parses as well-formed Turtle.

Run via: uv run --with-requirements scripts/requirements.txt scripts/validate_ttl.py FILE.ttl ...
"""

import sys

from rdflib import Graph


def main(paths: list[str]) -> int:
    if not paths:
        print("usage: validate_ttl.py FILE.ttl [FILE.ttl ...]", file=sys.stderr)
        return 2

    failed = False
    for path in paths:
        graph = Graph()
        try:
            graph.parse(path, format="turtle")
        except Exception as exc:
            print(f"{path}: FAILED\n  {exc}", file=sys.stderr)
            failed = True
        else:
            print(f"{path}: OK ({len(graph)} triples)")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

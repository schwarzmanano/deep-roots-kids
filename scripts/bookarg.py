"""Resolve which book a pipeline stage operates on.

Every stage takes the book slug as its FIRST argument — e.g.
    python3 scripts/kids/layout.py made-like-him
There is deliberately no default: a stage that silently fell back to one book would
overwrite that book's outputs. Run from the repo root (paths are repo-relative).
"""
import os, sys

def book_dir():
    usage = f"usage: {os.path.basename(sys.argv[0])} <book-slug>   (e.g. genesis-1)"
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        raise SystemExit(usage)
    slug = sys.argv[1].strip("/").removeprefix("kids/")
    book = f"kids/{slug}"
    if not os.path.isfile(f"{book}/book.yaml"):
        raise SystemExit(f"no {book}/book.yaml — run from the repo root with a valid slug\n{usage}")
    return book

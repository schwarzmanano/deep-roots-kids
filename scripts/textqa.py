#!/usr/bin/env python3
"""Text QA — checks on the printed wording that flag problems and never fix them.

authorship-policy §9-10: the author's text is reported on, never rewritten. These checks
come from the Book Two proof (2026-09-30):

  REPEATED-OPENING  two pages open with the same line (made-like-him p9 teaching and p15
                    text both opened "God knows all things — and He made you able ...").
                    Compared on the first OPENING_WORDS words of each page's text and
                    teaching line, case- and punctuation-blind. A pair where BOTH units are
                    WEB quotations is a WARN (Scripture can't be changed); anything else FAILs.
  CAPITAL-GODS      "Gods" capitalised. Generic plural gods are lowercase (made-like-him p7).

Runs standalone on plan/pages.yaml (no art needed), and at the end of qa.py:
    .venv-kids/bin/python kids/scripts/textqa.py <book-slug>
Exit status 1 on any FAIL.
"""
import os, re, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from textunits import units

OPENING_WORDS = 5
_KINDS = {"page-text", "teaching", "scripture-quote"}   # the lines that open an art page


def _norm(text):
    words = re.sub(r"[^\w\s']", " ", text.replace("’", "'").lower()).split()
    return " ".join(words[:OPENING_WORDS])


def check(book):
    """[(level, code, where, detail)] — level is FAIL or WARN. Empty = clean."""
    us = [u for u in units(book) if u["kind"] in _KINDS and u["text"]]
    out = []

    seen = defaultdict(list)
    for u in us:
        if len(u["text"].split()) >= OPENING_WORDS:
            seen[_norm(u["text"])].append(u)
    for key, group in seen.items():
        if len({u["page"] for u in group}) < 2:
            continue
        level = "WARN" if all(u["kind"] == "scripture-quote" for u in group) else "FAIL"
        out.append((level, "REPEATED-OPENING", ", ".join(u["id"] for u in group), f'"{key} ..."'))

    for u in units(book):
        if u["text"] and re.search(r"\bGods\b", u["text"]):
            out.append(("FAIL", "CAPITAL-GODS", u["id"], 'generic plural is lowercase "gods"'))
    return out


def report(book):
    probs = check(book)
    print(f"\n  text QA — {os.path.basename(book.rstrip('/'))}: "
          f"{sum(p[0] == 'FAIL' for p in probs)} fail, {sum(p[0] == 'WARN' for p in probs)} warn")
    for level, code, where, detail in probs:
        print(f"    {level:<4} {code:<17} {where}  {detail}")
    return probs


if __name__ == "__main__":
    from bookarg import book_dir
    sys.exit(1 if any(p[0] == "FAIL" for p in report(book_dir())) else 0)

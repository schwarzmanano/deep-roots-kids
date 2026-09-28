#!/usr/bin/env python3
"""Text-provenance registry CLI — authorship-policy §4.

  provenance.py <book> status
  provenance.py <book> set <unit-id> --author {human|ai-drafted|public-domain|unresolved}
                           --draft {true|false} --source "<where this wording came from>"

`set` pins the record to the unit's CURRENT wording (sha). Marking a unit `human` requires
--draft false and a --source naming where the author supplied the words (e.g. "editor chat
2026-10-02"): policy §4 — a unit becomes human only when the author supplied the final
wording. Review, approval or light edits of AI wording never qualify.

This tool records provenance; it never changes text. Insert the author's words verbatim
into book.yaml / pages.yaml first, then `set`.
"""
import sys, os, yaml, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bookarg import book_dir
import textunits

BOOK = book_dir()
args = sys.argv[2:]
PROV = f"{BOOK}/provenance.yaml"
prov = yaml.safe_load(open(PROV)) if os.path.exists(PROV) else {}
units = {u["id"]: u for u in textunits.units(BOOK)}
reg = textunits.registry(BOOK)

def save():
    order = [u for u in units]                     # keep print order
    prov["text_units"] = [reg[i] for i in order if i in reg] + \
                         [r for i, r in reg.items() if i not in units]
    with open(PROV, "w") as f:
        yaml.safe_dump(prov, f, sort_keys=False, allow_unicode=True, width=100)

if not args or args[0] == "status":
    probs = dict(textunits.check(BOOK))
    print(f"  {len(units)} text units — {BOOK}")
    for i, u in units.items():
        r = reg.get(i, {})
        words = len(u["text"].split()) if u["text"] else 0
        flag = next((why for where, why in textunits.check(BOOK) if where.endswith(f"[{i}]")), "")
        print(f"  {i:<22} {u['kind']:<20} {str(r.get('author')):<14} draft={str(r.get('draft')):<5} "
              f"{words:>3}w  {flag}")
    sys.exit(0)

if args[0] == "set":
    uid = args[1]
    opt = lambda k: args[args.index(k) + 1] if k in args else None
    author, draft, source = opt("--author"), opt("--draft"), opt("--source")
    if uid not in units: sys.exit(f"unknown unit {uid}")
    if author not in textunits.AUTHORS | {"unresolved"}: sys.exit(f"bad --author {author}")
    if draft not in ("true", "false"): sys.exit("--draft true|false required")
    if not source: sys.exit("--source required: where did this wording come from?")
    if author == "human" and draft != "false":
        sys.exit("author human means the author supplied FINAL wording: use --draft false")
    if author == "human" and units[uid]["text"] is None:
        sys.exit("cannot mark an empty unit human — insert the author's text first")
    reg[uid] = dict(id=uid, page=units[uid]["page"], kind=units[uid]["kind"],
                    author=None if author == "unresolved" else author,
                    draft=draft == "true", sha=textunits.sha(units[uid]["text"]),
                    source=source, recorded=datetime.date.today().isoformat())
    save()
    print(f"  {uid}: author={author} draft={draft} sha={reg[uid]['sha']}")
    sys.exit(0)

sys.exit(__doc__)

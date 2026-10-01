#!/usr/bin/env python3
"""WEB Scripture fidelity — series rule (editor ruling 2026-10-01).

Quoted Scripture prints exactly as the World English Bible publishes it: wording, lowercase
pronouns for God, and the WEB's own quote marks and apostrophes. The author's prose may
capitalise divine pronouns; that rule is about quotation only.

The WEB text is cached as public-domain plain text in kids/_brand/web/<CODE><CH>.json, one
file per chapter, fetched from ebible.org/eng-web (the text Books One-Three verified against).
Checks never touch the network — a missing chapter is a FAIL that names the fetch command.

    .venv-kids/bin/python kids/scripts/web.py fetch GEN 3        # cache a chapter
    .venv-kids/bin/python kids/scripts/web.py check <book-slug>  # verify public-domain units

A unit passes when its printed text appears VERBATIM inside the WEB text of the verses its
page cites (`quote_ref:` if the page sets one, else `ref:`). Quoting part of a verse is
allowed; changing any character inside the quoted span is not.
"""
import html, json, os, re, sys, urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_brand", "web")
BOOKS = {"genesis": "GEN", "psalm": "PSA", "psalms": "PSA", "isaiah": "ISA", "romans": "ROM",
         "1 john": "1JN", "revelation": "REV", "james": "JAS", "acts": "ACT",
         "colossians": "COL", "ephesians": "EPH", "matthew": "MAT", "john": "JHN",
         "1 corinthians": "1CO", "2 corinthians": "2CO", "hebrews": "HEB", "exodus": "EXO"}


def _file(code, ch):
    return f"{code}{ch:03d}" if code == "PSA" else f"{code}{ch:02d}"


def fetch(code, ch):
    name = _file(code, ch)
    req = urllib.request.Request(f"https://ebible.org/eng-web/{name}.htm", headers={"User-Agent": "curl/8"})
    raw = urllib.request.urlopen(req).read().decode("utf-8")
    s = re.sub(r'<a href="#FN[^"]*"[^>]*>.*?</a>', "", raw, flags=re.S)
    s = re.sub(r'<span class="verse"[^>]*>(.*?)</span>',
               lambda m: "\n[" + re.sub(r"<[^>]+>|&#160;|\s", "", m.group(1)) + "] ", s, flags=re.S)
    s = s.split('<div class="footnote">')[0]
    t = re.sub(r"[\s\u00a0]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).replace(" [", "\n[")
    verses = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"^\[(\d+)\] (.*)$", t, re.M)}
    last = max(verses)
    verses[last] = re.sub(r"\s*\S+ < \d+ >\s*$", "", verses[last]).strip()   # page nav tail
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"source": f"https://ebible.org/eng-web/{name}.htm", "translation": "WEB (public domain)",
               "verses": verses}, open(f"{CACHE}/{name}.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return verses


def chapter(code, ch):
    p = f"{CACHE}/{_file(code, ch)}.json"
    if not os.path.exists(p):
        return None
    return {int(k): v for k, v in json.load(open(p, encoding="utf-8"))["verses"].items()}


def passages(ref):
    """'Genesis 1:27; 2:22' -> [(code, ch, first, last), ...]. Unknown books are skipped."""
    out, code = [], None
    for part in ref.split(";"):
        part = part.strip()
        m = re.match(r"^((?:[123] )?[A-Za-z]+)\s+(.*)$", part)
        if m and m.group(1).lower() in BOOKS:
            code, part = BOOKS[m.group(1).lower()], m.group(2)
        if not code:
            continue
        m = re.match(r"^(\d+):(\d+)(?:-(\d+))?", part)
        if m:
            ch, a = int(m.group(1)), int(m.group(2))
            out.append((code, ch, a, int(m.group(3) or a)))
    return out


def check(book):
    """[(unit id, problem)] for every public-domain QUOTATION that is not verbatim WEB."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import textunits, yaml
    plan = {f"p{p['page']}": p for p in yaml.safe_load(open(f"{book}/plan/pages.yaml"))["pages"]}
    reg, bad = textunits.registry(book), []
    for u in textunits.units(book):
        if (reg.get(u["id"]) or {}).get("author") != "public-domain" or u["kind"] == "scripture-reference":
            continue
        pg = plan.get(u["page"], {})
        ref = pg.get("quote_ref") or pg.get("ref") or ""
        spans, missing = [], []
        for code, ch, a, b in passages(ref):
            vs = chapter(code, ch)
            if vs is None:
                missing.append(f"{code} {ch}")
                continue
            spans.append(" ".join(vs[v] for v in range(a, b + 1) if v in vs))
        if missing:
            bad.append((u["id"], f"WEB not cached for {', '.join(missing)} — run: web.py fetch <CODE> <CH>"))
        elif not spans:
            bad.append((u["id"], f"no Scripture reference to check against (ref: {ref!r})"))
        elif not any(u["text"] and u["text"] in s for s in spans):
            bad.append((u["id"], f"NOT VERBATIM WEB ({ref})\n        printed: {u['text']!r}\n"
                                 + "".join(f"        WEB    : {s!r}\n" for s in spans).rstrip()))
    return bad


def refuse(book):
    """Release-guard half: exit 1 if any public-domain quotation is not verbatim WEB."""
    bad = check(book)
    if bad:
        print(f"\n  ⛔ RELEASE REFUSED — {len(bad)} Scripture quotation(s) not verbatim WEB (series rule 2026-10-01):\n")
        for uid, why in bad:
            print(f"    [{uid}] {why}")
        raise SystemExit(1)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "fetch":
        v = fetch(sys.argv[2].upper(), int(sys.argv[3]))
        print(f"  cached {_file(sys.argv[2].upper(), int(sys.argv[3]))}: {len(v)} verses")
    elif len(sys.argv) >= 3 and sys.argv[1] == "check":
        sys.argv = [sys.argv[0], sys.argv[2]]
        from bookarg import book_dir
        b = book_dir(); probs = check(b)
        print(f"  WEB fidelity — {os.path.basename(b)}: {len(probs)} problem(s)")
        for uid, why in probs:
            print(f"    FAIL [{uid}] {why}")
        sys.exit(1 if probs else 0)
    else:
        sys.exit(__doc__)

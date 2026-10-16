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

Covers every Scripture quotation (theology-guardrails §8, amended 2026-10-02): whole
public-domain units, and “quoted” spans inside any other unit whose words match a reference
cited on that page (4+ consecutive words in common — otherwise the span is dialogue, a lyric
or a title, and is skipped). A quotation passes when it appears VERBATIM in the WEB text of
the cited verses — quoting part of a verse is fine — or differs only by the three §8
departures: one added curly ” where the WEB speech continues; a capital first letter where
the quotation begins a sentence; a final period for the WEB's ; or , where it ends a sentence.
"""
import html, json, os, re, sys, urllib.request

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_brand", "web")
BOOKS = {"genesis": "GEN", "psalm": "PSA", "psalms": "PSA", "isaiah": "ISA", "romans": "ROM",
         "1 john": "1JN", "revelation": "REV", "james": "JAS", "acts": "ACT",
         "colossians": "COL", "ephesians": "EPH", "matthew": "MAT", "john": "JHN",
         "1 corinthians": "1CO", "2 corinthians": "2CO", "hebrews": "HEB", "exodus": "EXO",
         "galatians": "GAL"}


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


def _matches(text, web, verse_ends, begins_sentence=True, ends_sentence=True):
    """Verbatim, or verbatim under exactly the three §8 departures (amended 2026-10-02):
    1. one added curly ” at the end, where the WEB speech continues past the quoted verse;
    2. a capital first letter, when the quotation begins a sentence;
    3. a final period for the WEB's ; or , when the quotation ends a sentence."""
    if text and text in web:
        return True
    core, added_quote = text, False
    if core.endswith("”"):                                          # departure 1
        core, added_quote = core[:-1], True
    if not core:
        return False
    starts = [core]
    if begins_sentence and core[0].isupper():                       # departure 2
        starts.append(core[0].lower() + core[1:])
    cands = []
    for c in starts:
        cands.append((c, False))
        if ends_sentence and c.endswith("."):                       # departure 3
            cands += [(c[:-1] + ";", True), (c[:-1] + ",", True)]
    for c, swapped in cands:
        i = web.find(c)
        while i != -1:
            end = i + len(c)
            ok = True
            if added_quote:
                ok = c.count("“") > c.count("”") and end in verse_ends and web[end:end + 1] != "”"
            if ok:
                return True
            i = web.find(c, i + 1)
    return False


def _passages_text(ref):
    """[(text, verse_ends)] for every cited passage; raises KeyError(code ch) if not cached."""
    out = []
    for code, ch, a, b in passages(ref):
        vs = chapter(code, ch)
        if vs is None:
            raise KeyError(f"{code} {ch}")
        txt = " ".join(vs[v] for v in range(a, b + 1) if v in vs)
        ends, pos = set(), -1
        for v in range(a, b + 1):
            if v in vs:
                pos += len(vs[v]) + 1
                ends.add(pos)
        out.append((txt, ends))
    return out


_QUOTE = re.compile(r"“([^“”]+)”|\"([^\"]+)\"")
_W = lambda t: re.sub(r"[^\w\s]", " ", t.replace("’", "'").lower()).split()


def _scriptural(inner, spans, n=4):
    """True when the quoted words share a run of n+ consecutive words with the cited WEB text —
    i.e. the quotation is Scripture from a reference on the page, not dialogue or a lyric."""
    w = _W(inner)
    if len(w) < n:
        return False
    hay = " " + " ".join(_W(" ".join(t for t, _ in spans))) + " "
    return any(" " + " ".join(w[i:i + n]) + " " in hay for i in range(len(w) - n + 1))


def check(book):
    """[(unit id, problem)] for every Scripture quotation that is not WEB under §8:
    whole public-domain units, AND quotations inside any other text unit whose words match a
    reference cited on that page (or, for book/cover units, the book's scripture_scope)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import textunits, yaml
    cfg = yaml.safe_load(open(f"{book}/book.yaml"))
    plan = {f"p{p['page']}": p for p in yaml.safe_load(open(f"{book}/plan/pages.yaml"))["pages"]}
    reg, bad = textunits.registry(book), []
    for u in textunits.units(book):
        if not u["text"] or u["kind"] == "scripture-reference":
            continue
        pg = plan.get(u["page"], {})
        pd = (reg.get(u["id"]) or {}).get("author") == "public-domain"
        ref = (pg.get("quote_ref") or pg.get("ref") or "") if pd else \
              "; ".join(x for x in (pg.get("quote_ref"), pg.get("ref"), cfg.get("scripture_scope")) if x)
        try:
            spans = _passages_text(ref)
        except KeyError as e:
            bad.append((u["id"], f"WEB not cached for {e.args[0]} — run: web.py fetch <CODE> <CH>"))
            continue
        if pd:
            if not spans:
                bad.append((u["id"], f"no Scripture reference to check against (ref: {ref!r})"))
            elif not any(_matches(u["text"], t, e) for t, e in spans):
                bad.append((u["id"], f"NOT VERBATIM WEB ({ref})\n        printed: {u['text']!r}\n"
                            + "".join(f"        WEB    : {t!r}\n" for t, _ in spans).rstrip()))
            continue
        for m in _QUOTE.finditer(u["text"]):
            inner = m.group(1) or m.group(2)
            if not _scriptural(inner, spans):
                continue                                   # dialogue, lyric or title — not Scripture
            before, after = u["text"][:m.start()].rstrip(), u["text"][m.end():]
            begins = before == "" or before[-1] in ".?!:,"
            ends = after.strip() == "" or after[:1].isspace()
            straight = m.group(2) is not None
            if straight or not any(_matches(inner, t, e, begins, ends) for t, e in spans):
                bad.append((u["id"], f"QUOTED SCRIPTURE NOT WEB ({ref})"
                            + (" — straight quote marks" if straight else "")
                            + f"\n        printed: {inner!r}"))
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

"""Text-unit registry — the single list of reader-facing text a book prints.

kids/_brand/authorship-policy.md §4: every text unit a book prints is registered in
<book>/provenance.yaml (page, kind, author, draft). layout.py, cover.py and disclosure.py
all read text through `units()`, so nothing reaches print without passing through here.

A registration is pinned to the exact wording by `sha`. If the wording changes after it
was registered, the record no longer describes that text and the unit is UNRESOLVED
until it is re-registered — provenance can never silently carry over to new words.
"""
import hashlib, os, re, yaml

AUTHORS = {"human", "ai-drafted", "public-domain"}
# Unauthorized AI statements on any printed surface (policy §3).
AI_STATEMENT = re.compile(r"\bA\.?I\.?\b|artificial intelligence|machine[- ]generated|"
                          r"generated (with|by)", re.I)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12] if text is not None else None


def _load(book):
    cfg = yaml.safe_load(open(f"{book}/book.yaml"))
    plan = yaml.safe_load(open(f"{book}/plan/pages.yaml"))
    return cfg, plan


def body_of(pg):
    """Back-matter body text: inline, or read from a shared series file below its marker."""
    if pg.get("body_file"):
        raw = open(pg["body_file"], encoding="utf-8").read()
        marker = "<!-- BODY -->"
        if marker not in raw:
            raise SystemExit(f"{pg['body_file']}: missing {marker}")
        return raw.split(marker, 1)[1].strip()
    return pg.get("body")


def units(book):
    """Every reader-facing text unit, in print order: dicts of id, page, kind, text."""
    cfg, plan = _load(book)
    out = []
    add = lambda id, page, kind, text: out.append(dict(id=id, page=page, kind=kind, text=text))

    add("book.title", "p1, cover", "title", cfg.get("title"))
    add("book.series_line", "p1, back cover", "series-line", cfg.get("series_line"))
    add("book.subtitle", "p1, cover", "subtitle", cfg.get("subtitle"))
    add("book.scripture_scope", "p1, back cover", "scripture-reference", cfg.get("scripture_scope"))
    for i, line in enumerate(cfg.get("copyright_page") or []):
        add(f"p2.copyright.{i+1}", "p2", "copyright-page", line)

    for pg in plan["pages"]:
        n = pg["page"]
        if pg.get("back_matter"):
            kind = "about-the-author" if "about-the-author" in (pg.get("body_file") or "") else "closing"
            if "heading" in pg:            # a null heading is a registered, empty slot
                add(f"p{n}.heading", f"p{n}", "heading", pg["heading"])
            add(f"p{n}.body", f"p{n}", kind, body_of(pg))
            if "footnote" in pg:
                add(f"p{n}.footnote", f"p{n}", "footnote", " ".join(pg["footnote"].split()) if pg["footnote"] is not None else None)
            continue
        if pg.get("generate") is False or pg.get("placeholder"):
            continue
        add(f"p{n}.text", f"p{n}", "scripture-quote" if pg.get("quote") else "page-text", pg.get("text"))
        if "teaching" in pg:          # a null teaching line is a registered, empty slot
            add(f"p{n}.teaching", f"p{n}", "teaching", " ".join(pg["teaching"].split()) if pg["teaching"] is not None else None)

    cov = cfg.get("cover")
    if cov is not None:
        add("cover.series_short", "cover", "series-line", cov.get("series_short"))
        add("cover.back_blurb", "back cover", "back-cover-blurb",
            cov.get("back_blurb"))
        for i, line in enumerate(cov.get("spec_lines") or []):
            add(f"cover.spec.{i+1}", "back cover", "back-cover-spec", line)
    return out


def registry(book):
    p = f"{book}/provenance.yaml"
    prov = yaml.safe_load(open(p)) if os.path.exists(p) else {}
    return {u["id"]: u for u in (prov.get("text_units") or [])}


def check(book):
    """All provenance problems for this book's printed text. Empty list = release-clean."""
    reg, probs = registry(book), []
    slug = os.path.basename(book.rstrip("/"))
    for u in units(book):
        r = reg.get(u["id"])
        where = f"{slug} {u['page']} [{u['id']}]"
        if r is None:
            probs.append((where, "NO PROVENANCE RECORD")); continue
        a = r.get("author")
        if u["text"] is None:
            probs.append((where, f"EMPTY — awaiting text (author: {a}, draft: {r.get('draft')})")); continue
        if r.get("sha") != sha(u["text"]):
            probs.append((where, "UNRESOLVED — wording changed since it was registered")); continue
        if a not in AUTHORS:
            probs.append((where, f"UNRESOLVED — author: {a!r}"))
        elif a == "ai-drafted":
            probs.append((where, "author: ai-drafted"))
        if r.get("draft") is not False:
            probs.append((where, f"draft: {r.get('draft')}"))
        if AI_STATEMENT.search(u["text"]):
            probs.append((where, "AI-RELATED STATEMENT in printed text — policy §3"))
    for rid in reg:
        if rid not in {u["id"] for u in units(book)}:
            probs.append((f"{slug} [{rid}]", "STALE RECORD — unit no longer printed"))
    return probs


# ── my-words.md is the source of truth for every human unit (editor rulings 2026-10-01) ──
# The release guard compares each `author: human` unit, as it will print, against the text
# under **MY TEXT:** in <book>/plan/my-words.md — character for character — AND requires the
# section's status line to read exactly
#     **MY TEXT STATUS:** confirmed
# Only the author writes "confirmed". The pipeline may write "copied: awaiting confirmation"
# (text copied verbatim from the registered unit) or "awaiting your words", never "confirmed".
# The only normalisation is the one the printer already applies: units whose print form
# collapses whitespace (teaching lines, footnotes) are compared with whitespace collapsed on
# both sides. A unit whose body comes from a shared series file (body_file — About the
# Author) has that file as its source: it is not compared against my-words.md, but the
# file's own `**MY TEXT STATUS:**` line (above its BODY marker) must read `confirmed`.
_WS_KINDS = {"teaching", "footnote"}
CONFIRMED = "confirmed"
_STATUS = "**MY TEXT STATUS:**"


def my_words(book):
    """{unit id: (MY TEXT, status)} from <book>/plan/my-words.md. Empty MY TEXT -> ''."""
    p = f"{book}/plan/my-words.md"
    if not os.path.exists(p):
        return {}
    out, sec = {}, None          # sec = [uid, seen MY TEXT?, collecting?, lines, status]
    for line in open(p, encoding="utf-8").read().splitlines() + ["---"]:
        m = re.match(r"^### `([^`]+)`", line)
        if m or line.startswith("---") or line.startswith("## "):
            if sec and sec[1]:
                out[sec[0]] = ("\n".join(sec[3]).strip(), sec[4])
            sec = [m.group(1), False, False, [], None] if m else None
        elif sec is None:
            continue
        elif line.strip() == "**MY TEXT:**":
            sec[1], sec[2] = True, True
        elif line.startswith(_STATUS):
            sec[2], sec[4] = False, line[len(_STATUS):].strip()
        elif sec[2]:
            sec[3].append(line)
    return out


def check_my_words(book):
    """[(unit id, page, printed, my-words text or None, status)] for every human unit that is
    not both identical to its MY TEXT and marked confirmed by the author. Empty = clean."""
    cfg, plan = _load(book)
    body_file_pages = {f"p{p['page']}.body" for p in plan["pages"] if p.get("body_file")}
    reg, mw, bad = registry(book), my_words(book), []
    for u in units(book):
        r = reg.get(u["id"])
        if not r or r.get("author") != "human":
            continue
        if u["id"] in body_file_pages:
            f = next(p["body_file"] for p in plan["pages"] if f"p{p['page']}.body" == u["id"])
            head = open(f, encoding="utf-8").read().split("<!-- BODY -->", 1)[0]
            m = re.search(r"^\*\*MY TEXT STATUS:\*\*(.*)$", head, re.M)
            status = m.group(1).strip() if m else None
            if status != CONFIRMED:
                bad.append((u["id"], u["page"], u["text"] or "", u["text"] or "", status))
            continue
        mine, status = mw.get(u["id"], (None, None))
        printed = u["text"] or ""
        if mine is not None and u["kind"] in _WS_KINDS:
            mine = " ".join(mine.split())
        if mine != printed or status != CONFIRMED:
            bad.append((u["id"], u["page"], printed, mine, status))
    return bad


def refuse_on_my_words(book):
    """Release-guard half: print both versions of every mismatch / unconfirmed unit, exit 1."""
    bad = check_my_words(book)
    if not bad:
        return
    slug = os.path.basename(book.rstrip("/"))
    print(f"\n  ⛔ RELEASE REFUSED — {len(bad)} human unit(s) not matching AND confirmed in "
          f"plan/my-words.md (the source of truth, editor rulings 2026-10-01):\n")
    for uid, page, printed, mine, status in bad:
        why = "TEXT DIFFERS" if mine != printed else f"NOT CONFIRMED (status: {status!r})"
        print(f"    {slug} {page} [{uid}] — {why}")
        print(f"      my-words.md : {'(no MY TEXT section)' if mine is None else repr(mine) if mine else '(MY TEXT empty)'}")
        print(f"      printed     : {printed!r}")
    raise SystemExit(1)

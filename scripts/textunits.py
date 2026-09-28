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
            add(f"p{n}.body", f"p{n}", kind, body_of(pg))
            if pg.get("footnote") is not None:
                add(f"p{n}.footnote", f"p{n}", "footnote", " ".join(pg["footnote"].split()))
            continue
        if pg.get("generate") is False or pg.get("placeholder"):
            continue
        add(f"p{n}.text", f"p{n}", "scripture-quote" if pg.get("quote") else "page-text", pg.get("text"))
        if pg.get("teaching") is not None:
            add(f"p{n}.teaching", f"p{n}", "teaching", " ".join(pg["teaching"].split()))

    cov = cfg.get("cover")
    if cov is not None:
        add("cover.series_short", "cover", "series-line", cov.get("series_short"))
        add("cover.back_blurb", "back cover", "back-cover-blurb",
            " ".join(cov["back_blurb"].split()) if cov.get("back_blurb") else None)
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

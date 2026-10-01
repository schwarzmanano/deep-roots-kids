#!/usr/bin/env python3
"""Print-file verification table for both editions — editor ruling 2026-10-01.

  .venv-kids/bin/python kids/scripts/print_table.py <book-slug>

PyMuPDF answers what pdfinfo / pdffonts / pdfimages -list would (page sizes, font
embedding, image resolution); pdfplumber checks the cover's spine and barcode zones.
Poppler is not needed. Reads the four out/ files; changes nothing.

Zones (trim-relative, from cover.py's own geometry):
  spine    the full spine strip — no characters allowed below the printer's spine-text minimum
  barcode  the bottom 1.45in band of the back panel (KDP 2 x 1.2in box + 0.25in from trim;
           cover.py keeps the WHOLE band clear so either corner reading is satisfied).
           No characters and no vector marks; art luminance must stay light (> 200).
"""
import os, sys, yaml
import numpy as np, pymupdf, pdfplumber
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bookarg import book_dir

BOOK = book_dir(); IN = 72.0
cfg = yaml.safe_load(open(f"{BOOK}/book.yaml"))
PAGES = cfg["print"]["page_count"]
SPINE = {"kdp": PAGES * 0.002252, "lulu": PAGES / 444 + 0.06}
SPINE_TEXT_MIN = {"kdp": 80, "lulu": 81}   # pages; KDP: more than 79; Lulu: more than 80
rows, fails = [], []


def basics(path):
    d = pymupdf.open(path)
    sizes = sorted({(round(p.rect.width / IN, 3), round(p.rect.height / IN, 3)) for p in d})
    unemb = {f[3] for p in d for f in p.get_fonts(full=True)
             if str(f[1]).strip().lower() in ("n/a", "", "none", "0")}
    nfonts = len({f[3] for p in d for f in p.get_fonts(full=True)})
    ppi = [min(im[2] / (r.width / IN), im[3] / (r.height / IN))
           for p in d for im in p.get_images(full=True) for r in p.get_image_rects(im[0])]
    return d, sizes, nfonts, unemb, ppi


for target in ("kdp", "lulu"):
    sfx = "" if target == "kdp" else "-lulu"
    ip, cp = f"{BOOK}/out/interior{sfx}.pdf", f"{BOOK}/out/cover{sfx}.pdf"
    exp_int = (8.5, 11.0) if target == "kdp" else (8.75, 11.25)

    d, sizes, nf, unemb, ppi = basics(ip)
    ok_size = sizes == [exp_int]
    rows.append((f"{target} interior", d.page_count, " / ".join(f"{w}×{h}" for w, h in sizes),
                 f"{nf} fonts, {'all embedded' if not unemb else 'MISSING ' + str(sorted(unemb))}",
                 f"{min(ppi):.0f}–{max(ppi):.0f}" if ppi else "none (vector)",
                 d.metadata.get("author"), "—", "—"))
    if not ok_size: fails.append(f"{target} interior size {sizes} != {exp_int}")
    if d.page_count != PAGES: fails.append(f"{target} interior {d.page_count} pp != book.yaml {PAGES}")
    if unemb: fails.append(f"{target} interior unembedded fonts")
    if ppi and not (200 <= min(ppi) and max(ppi) <= 600): fails.append(f"{target} interior image ppi out of 200-600")

    d, sizes, nf, unemb, ppi = basics(cp)
    sp = SPINE[target]
    exp_cov = (round(0.125 + 8.5 + sp + 8.5 + 0.125, 3), 11.25)
    ok_cov = len(sizes) == 1 and abs(sizes[0][0] - exp_cov[0]) < 0.01 and abs(sizes[0][1] - 11.25) < 0.01
    if not ok_cov: fails.append(f"{target} cover size {sizes} != {exp_cov}")
    if unemb: fails.append(f"{target} cover unembedded fonts")
    if ppi and min(ppi) < 300: fails.append(f"{target} cover art {min(ppi):.0f} ppi < 300")

    # pdfplumber zones (top-left origin)
    b = 0.125 * IN
    spine = (b + 8.5 * IN, 0, b + 8.5 * IN + sp * IN, 11.25 * IN)
    band = (b, 11.25 * IN - b - 1.45 * IN, b + 8.5 * IN, 11.25 * IN - b)
    inside = lambda o, z: o["x0"] < z[2] and o["x1"] > z[0] and o["top"] < z[3] and o["bottom"] > z[1]
    with pdfplumber.open(cp) as pl:
        pg = pl.pages[0]
        sp_chars = [c for c in pg.chars if inside(c, spine)]
        bc_chars = [c for c in pg.chars if inside(c, band)]
        # a background fill that covers the whole band is not a mark; luminance checks it
        covers = lambda o, z: o["x0"] <= z[0] and o["x1"] >= z[2] and o["top"] <= z[1] and o["bottom"] >= z[3]
        bc_marks = [o for o in pg.rects + pg.lines + pg.curves if inside(o, band) and not covers(o, band)]
    pix = d[0].get_pixmap(dpi=72, clip=pymupdf.Rect(*band), colorspace=pymupdf.csGRAY)
    lum = int(np.frombuffer(pix.samples, np.uint8).min())
    spine_rule = "blank required" if PAGES < SPINE_TEXT_MIN[target] else "text permitted"
    spine_ok = not sp_chars or spine_rule == "text permitted"
    bc_ok = not bc_chars and not bc_marks and lum > 200
    if not spine_ok: fails.append(f"{target} spine carries {len(sp_chars)} chars at {PAGES} pp")
    if not bc_ok: fails.append(f"{target} barcode band: {len(bc_chars)} chars, {len(bc_marks)} marks, min lum {lum}")
    rows.append((f"{target} cover", d.page_count, " / ".join(f"{w}×{h}" for w, h in sizes),
                 f"{nf} fonts, {'all embedded' if not unemb else 'MISSING ' + str(sorted(unemb))}",
                 f"{min(ppi):.0f}" if ppi else "none",
                 d.metadata.get("author"),
                 f"{sp:.4f}in, {len(sp_chars)} chars ({spine_rule})",
                 f"{len(bc_chars)} chars, {len(bc_marks)} marks, min lum {lum}"))

for r in rows:
    if r[5] != cfg.get("author"):
        fails.append(f"{r[0]} metadata author {r[5]!r} != book.yaml author {cfg.get('author')!r} (rebuild)")
hdr = ("File", "Pages", "Size (in)", "Fonts", "Image ppi", "Meta author", "Spine zone", "Barcode zone")
print(f"\n{os.path.basename(BOOK)} — {PAGES} pp (book.yaml)\n")
print("| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr))
for r in rows:
    print("| " + " | ".join(str(x) for x in r) + " |")
print(f"\n{'PASS' if not fails else 'ISSUES:'}")
for f in fails: print(f"  - {f}")
sys.exit(1 if fails else 0)

#!/usr/bin/env python3
"""Stage 8 — KDP preflight. Hard-fails; nothing ships on a warning."""
import sys, yaml, fitz          # fitz = pymupdf
from pypdf import PdfReader

import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bookarg import book_dir
BOOK = book_dir()
cfg = yaml.safe_load(open(f"{BOOK}/book.yaml"))
PDF = f"{BOOK}/out/interior.pdf"
IN = 72.0
M = cfg["margins"]
fails, warns = [], []

rd = PdfReader(PDF)
n = len(rd.pages)
print(f"  pages: {n}")
if n != cfg["print"]["page_count"]: fails.append(f"page count {n} != {cfg['print']['page_count']}")
if n % 2: fails.append("page count is odd — KDP requires even")
if n < 24: fails.append("below KDP 24-page minimum for this trim")

# trim size, exact
bad = []
for i, pg in enumerate(rd.pages, 1):
    w = float(pg.mediabox.width); h = float(pg.mediabox.height)
    if abs(w - 8.5*IN) > 0.01 or abs(h - 11*IN) > 0.01:
        bad.append(f"p{i} {w/IN:.3f}x{h/IN:.3f}in")
print(f"  trim: {'all 8.500x11.000 in' if not bad else 'MISMATCH ' + ', '.join(bad[:3])}")
if bad: fails.append(f"{len(bad)} page(s) not 8.5x11")

# font embedding
doc = fitz.open(PDF)
unembedded = set()
fonts = set()
for p in doc:
    for f in p.get_fonts(full=True):
        name, ext = f[3], f[1]
        fonts.add(name)
        # pymupdf reports the embedded font-file extension, or 'n/a' when the
        # font is only referenced (base-14). Anything not a real file = not embedded.
        if str(ext).strip().lower() in ("n/a", "", "none", "0"): unembedded.add(name)
print(f"  fonts: {len(fonts)} used -> {', '.join(sorted(fonts)) or 'none'}")
if unembedded: fails.append(f"unembedded font(s): {', '.join(sorted(unembedded))}")

# raster images — there should be none; vector only
raster = []
for i, p in enumerate(doc, 1):
    for img in p.get_images(full=True):
        xref, w, h = img[0], img[2], img[3]
        for r in p.get_image_rects(xref):
            dpi = min(w / (r.width/IN), h / (r.height/IN))
            raster.append((i, w, h, dpi))
if raster:
    worst = min(r[3] for r in raster)
    print(f"  raster images: {len(raster)} (lowest {worst:.0f} DPI)")
    if worst < 300: fails.append(f"raster image below 300 DPI ({worst:.0f})")
else:
    print("  raster images: none — art is vector, DPI floor does not apply")

# margins: measure actual ink on every page
gut, out = M["gutter_in"]*IN, M["outside_in"]*IN
top, bot = M["top_in"]*IN, M["bottom_in"]*IN
viol = []
for i, p in enumerate(doc, 1):
    r = p.get_bbox() if hasattr(p, "get_bbox") else None
    d = p.get_drawings()
    if not d and not p.get_text().strip(): continue
    x0 = min([q["rect"].x0 for q in d] + [999]); x1 = max([q["rect"].x1 for q in d] + [-999])
    y0 = min([q["rect"].y0 for q in d] + [999]); y1 = max([q["rect"].y1 for q in d] + [-999])
    for blk in p.get_text("blocks"):
        x0, y0 = min(x0, blk[0]), min(y0, blk[1]); x1, y1 = max(x1, blk[2]), max(y1, blk[3])
    if x0 > 900: continue
    recto = i % 2 == 1
    L = gut if recto else out
    R = out if recto else gut
    W, H = p.rect.width, p.rect.height
    if x0 < L - 0.5: viol.append(f"p{i} left {x0/IN:.3f}in < {L/IN:.3f}in")
    if x1 > W - R + 0.5: viol.append(f"p{i} right {(W-x1)/IN:.3f}in < {R/IN:.3f}in")
    if y0 < top - 0.5: viol.append(f"p{i} top {y0/IN:.3f}in")
    if y1 > H - bot + 0.5: viol.append(f"p{i} bottom {(H-y1)/IN:.3f}in")
print(f"  margins: {'all within gutter %.3f\" / outside %.3f\"' % (M['gutter_in'], M['outside_in']) if not viol else 'VIOLATIONS'}")
for v in viol[:6]: print(f"    {v}")
if viol: fails.append(f"{len(viol)} margin violation(s)")

print()
if fails:
    print(f"  ❌ PREFLIGHT FAILED — {len(fails)} issue(s)")
    for f in fails: print(f"     - {f}")
    sys.exit(1)
print("  ✅ PREFLIGHT PASSED — no errors")

#!/usr/bin/env python3
"""Stage 8 — KDP preflight. Hard-fails; nothing ships on a warning."""
import sys, yaml, fitz          # fitz = pymupdf
from pypdf import PdfReader

import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bookarg import book_dir
BOOK = book_dir()
cfg = yaml.safe_load(open(f"{BOOK}/book.yaml"))
IN = 72.0
TARGET = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else "kdp"
PDF = f"{BOOK}/out/interior{'' if TARGET == 'kdp' else '-lulu'}.pdf"
BLEED = 0.125*IN if TARGET == "lulu" else 0.0   # Lulu: 0.125in bleed on all files
print(f"  target: {TARGET}  ({PDF})")
M = cfg["margins"]
fails, warns = [], []

rd = PdfReader(PDF)
n = len(rd.pages)
print(f"  pages: {n}")
if n != cfg["print"]["page_count"]: fails.append(f"page count {n} != {cfg['print']['page_count']}")
if n % 2: fails.append("page count is odd — KDP requires even")
if n < 24: fails.append("below KDP 24-page minimum for this trim")
if TARGET == "lulu" and n < 32: fails.append("below Lulu 32-page paperback minimum")

# trim size, exact
bad = []
for i, pg in enumerate(rd.pages, 1):
    w = float(pg.mediabox.width); h = float(pg.mediabox.height)
    if abs(w - 8.5*IN - 2*BLEED) > 0.01 or abs(h - 11*IN - 2*BLEED) > 0.01:
        bad.append(f"p{i} {w/IN:.3f}x{h/IN:.3f}in")
print(f"  page: {'all %.3fx%.3f in' % (8.5+2*BLEED/IN, 11+2*BLEED/IN) if not bad else 'MISMATCH ' + ', '.join(bad[:3])}"
      f"{'  (8.5x11 trim + 0.125in bleed)' if BLEED else '  (8.5x11 trim, no bleed)'}")
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
if TARGET == "lulu":   # Lulu safety margin: 0.5in inside trim on every side, gutter included
    SAFE = 0.5*IN
    if min(gut, out, top, bot) < SAFE - 0.01:
        fails.append(f"margins below Lulu's 0.5in safety margin (gutter {gut/IN}in)")
# measure against the TRIM box: shift every coordinate by the bleed
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
    x0, x1, y0, y1 = x0 - BLEED, x1 - BLEED, y0 - BLEED, y1 - BLEED
    W, H = p.rect.width - 2*BLEED, p.rect.height - 2*BLEED
    if x0 < L - 0.5: viol.append(f"p{i} left {x0/IN:.3f}in < {L/IN:.3f}in")
    if x1 > W - R + 0.5: viol.append(f"p{i} right {(W-x1)/IN:.3f}in < {R/IN:.3f}in")
    if y0 < top - 0.5: viol.append(f"p{i} top {y0/IN:.3f}in")
    if y1 > H - bot + 0.5: viol.append(f"p{i} bottom {(H-y1)/IN:.3f}in")
print(f"  margins: {'all within gutter %.3f\" / outside %.3f\"' % (M['gutter_in'], M['outside_in']) if not viol else 'VIOLATIONS'}")
for v in viol[:6]: print(f"    {v}")
if viol: fails.append(f"{len(viol)} margin violation(s)")

# colour + transparency — black-ink interior: K-only, no RGB, no transparency
import re as _re, zlib as _z
rgb_pages, trans, img_cs = [], [], set()
ink_black = cfg["print"].get("ink", "black") == "black"
for i, p in enumerate(doc, 1):
    ops = p.read_contents().decode("latin-1")
    if _re.search(r"(?<![\w.])(rg|RG|sc|SC|scn|SCN)\b", ops): rgb_pages.append(i)
    for img in p.get_images(full=True):
        img_cs.add(img[5])
        if img[1]: trans.append(f"p{i} soft mask")
for x in range(1, doc.xref_length()):
    try: obj = doc.xref_object(x)
    except Exception: continue
    if _re.search(r"/(ca|CA)\s+0?\.\d", obj) or "/SMask" in obj and "/SMask /None" not in obj:
        trans.append(f"xref {x}")
print(f"  colour: {'K-only, no RGB operators' if not rgb_pages else 'RGB on pages ' + str(rgb_pages[:8])}"
      f"; images {sorted(img_cs) or 'none'}")
print(f"  transparency: {'none' if not trans else ', '.join(sorted(set(trans))[:4])}")
if ink_black and rgb_pages: fails.append(f"RGB colour operators on {len(rgb_pages)} page(s) — black-ink interior must be K-only")
if ink_black and any(cs not in ("DeviceGray",) for cs in img_cs): fails.append(f"non-grayscale image(s): {sorted(img_cs)}")
if trans: fails.append("transparency present — Lulu requires it flattened")

print()
if fails:
    print(f"  ❌ PREFLIGHT FAILED — {len(fails)} issue(s)")
    for f in fails: print(f"     - {f}")
    sys.exit(1)
print("  ✅ PREFLIGHT PASSED — no errors")

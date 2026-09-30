#!/usr/bin/env python3
"""Cover preflight. Raster art means the 300 DPI floor DOES apply here."""
import sys, yaml, pymupdf, numpy as np
from PIL import Image
import io
from pypdf import PdfReader

import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bookarg import book_dir
BOOK = book_dir(); IN=72.0
cfg=yaml.safe_load(open(f"{BOOK}/book.yaml")); PAGES=cfg["print"]["page_count"]
TARGET = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else "kdp"
PDF=f"{BOOK}/out/cover{'' if TARGET == 'kdp' else '-lulu'}.pdf"
fails=[]
print(f"  target: {TARGET}  ({PDF})")
SPINE=PAGES*0.002252*IN if TARGET=="kdp" else (PAGES/444+0.06)*IN
SAFE=0.25*IN if TARGET=="kdp" else 0.5*IN      # Lulu safety margin 0.5in on all sides
EXP_W=0.125*IN+8.5*IN+SPINE+8.5*IN+0.125*IN
EXP_H=0.125*IN+11*IN+0.125*IN

rd=PdfReader(PDF)
if len(rd.pages)!=1: fails.append(f"cover must be 1 page, got {len(rd.pages)}")
w=float(rd.pages[0].mediabox.width); h=float(rd.pages[0].mediabox.height)
print(f"  size : {w/IN:.3f} x {h/IN:.3f} in   (expected {EXP_W/IN:.3f} x {EXP_H/IN:.3f})")
if abs(w-EXP_W)>0.02 or abs(h-EXP_H)>0.02: fails.append("cover dimensions wrong")
_min = 100 if TARGET=="kdp" else 81     # KDP: spine text 100+ pp; Lulu: none at 80 pp or fewer
print(f"  spine: {SPINE/IN:.4f} in — {'must be blank (' + str(PAGES) + ' pp)' if PAGES<_min else 'text permitted'}")

doc=pymupdf.open(PDF); pg=doc[0]
fonts=set(); unemb=set()
for f in pg.get_fonts(full=True):
    fonts.add(f[3])
    if str(f[1]).strip().lower() in ("n/a","","none","0"): unemb.add(f[3])
print(f"  fonts: {', '.join(sorted(fonts))}")
if unemb: fails.append(f"unembedded font(s): {', '.join(sorted(unemb))}")

worst=None
for img in pg.get_images(full=True):
    xref,_,iw,ih=img[0],img[1],img[2],img[3]
    for r in pg.get_image_rects(xref):
        dpi=min(iw/(r.width/IN), ih/(r.height/IN))
        worst=dpi if worst is None else min(worst,dpi)
print(f"  raster: lowest {worst:.0f} DPI" if worst else "  raster: none")
if worst and worst<300: fails.append(f"raster below 300 DPI ({worst:.0f})")

# barcode band must be clear AND light
band_h=(1.2+0.25)*IN
clip=pymupdf.Rect(0.125*IN, EXP_H-band_h, 0.125*IN+8.5*IN, EXP_H)   # pymupdf y-down
pix=pg.get_pixmap(dpi=150, clip=clip)
a=np.array(Image.open(io.BytesIO(pix.tobytes("png"))).convert("L"))
print(f"  barcode band: min luminance {a.min()}, mean {a.mean():.0f} "
      f"({'clear + light' if a.min()>200 else 'HAS DARK CONTENT'})")
if a.min()<=200: fails.append(f"barcode band not clear (min luminance {a.min()})")

# text safety: every text block inside the back or front panel's safe box (never on the spine)
B0=0.125*IN; back=pymupdf.Rect(B0+SAFE, B0+SAFE, B0+8.5*IN-SAFE, EXP_H-B0-SAFE)
front=pymupdf.Rect(B0+8.5*IN+SPINE+SAFE, B0+SAFE, EXP_W-B0-SAFE, EXP_H-B0-SAFE)
# per WORD: pymupdf merges same-baseline text across panels into one block, which would
# falsely read as crossing the spine.
out=[b for b in pg.get_text("words") if not (pymupdf.Rect(b[:4]) in back or pymupdf.Rect(b[:4]) in front)]
print(f"  text in safe area ({SAFE/IN:.2f}in): {'yes' if not out else f'{len(out)} block(s) OUTSIDE'}")
for b in out[:4]: print(f"    outside: {b[4].strip()[:50]!r}")
if out: fails.append(f"{len(out)} text block(s) outside the {SAFE/IN:.2f}in safe area")

# colour + transparency (Lulu: flattened; editor brief: CMYK throughout when cover.color = cmyk)
import re as _re
cs={doc.xref_get_key(i[0],"ColorSpace")[1] for i in pg.get_images(full=True)}
smask=[i for i in pg.get_images(full=True) if i[1]]
ops=pg.read_contents().decode("latin-1")
rgb_ops=len(_re.findall(r"(?<![\w.])(rg|RG)\b",ops))
print(f"  colour: images {sorted(cs)}; RGB operators {rgb_ops}; transparency {'none' if not smask else len(smask)}")
if smask: fails.append("transparent image(s) — Lulu requires transparency flattened")
if (cfg.get("cover") or {}).get("color")=="cmyk" and (cs-{"/DeviceCMYK"} or rgb_ops):
    fails.append("cover.color is cmyk but RGB content remains")

print()
if fails:
    print(f"  ❌ COVER PREFLIGHT FAILED — {len(fails)} issue(s)")
    for f in fails: print(f"     - {f}")
    sys.exit(1)
print("  ✅ COVER PREFLIGHT PASSED")

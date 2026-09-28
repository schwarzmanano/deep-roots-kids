#!/usr/bin/env python3
"""Stage 9 — full-wrap cover per kids/_brand/brand-spec.md.

Unlike the interior, cover art is RASTER, so KDP's 300 DPI floor applies here.
Geometry: [bleed][back 8.5"][spine][front 8.5"][bleed] x (11" + bleed top/bottom).
"""
import os, yaml
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from badge import draw_badge

from bookarg import book_dir
import textunits
BOOK = book_dir()
RELEASE = "--release" in sys.argv          # authorship-policy §11 — same guard as layout.py
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"{BOOK}/out/cover.pdf"
PROOF_STAMP = "PROOF - NOT FOR RELEASE"
IN = 72.0
cfg = yaml.safe_load(open(f"{BOOK}/book.yaml"))
if "cover" not in cfg:
    raise SystemExit(f"{BOOK}/book.yaml has no cover: block — cover text units not registered yet")
COV = cfg["cover"]
if any(COV.get(k) is None for k in ("series_short", "back_blurb")) or cfg.get("subtitle") is None:
    raise SystemExit("cover text incomplete — awaiting the author's text (see plan/my-words.md)")
_probs = textunits.check(BOOK)
if RELEASE and _probs:
    print(f"\n  ⛔ RELEASE REFUSED — {len(_probs)} problem(s) across {len({w for w, _ in _probs})} text unit(s), authorship-policy §11:\n")
    for where, why in _probs: print(f"    {where}: {why}")
    raise SystemExit(1)
PAGES = cfg["print"]["page_count"]

# Primary Palette
CREAM = HexColor("#F7EEDD"); GOLD = HexColor("#D9A441")
NAVY  = HexColor("#2E4257"); GREEN = HexColor("#4C7A5A")

FD = "kids/_brand/fonts"
pdfmetrics.registerFont(TTFont("Baloo2", f"{FD}/Baloo2.ttf"))
pdfmetrics.registerFont(TTFont("Lora",   f"{FD}/Lora.ttf"))
pdfmetrics.registerFont(TTFont("LoraIt", f"{FD}/Lora-Italic.ttf"))

BLEED  = 0.125 * IN
TRIM_W, TRIM_H = 8.5 * IN, 11 * IN
SPINE  = PAGES * 0.002252 * IN          # white paper, per KDP
SAFE   = 0.25 * IN                       # keep text this far inside trim
W = BLEED + TRIM_W + SPINE + TRIM_W + BLEED
H = BLEED + TRIM_H + BLEED

BACK_L,  BACK_R  = BLEED, BLEED + TRIM_W
SPINE_L, SPINE_R = BACK_R, BACK_R + SPINE
FRONT_L, FRONT_R = SPINE_R, SPINE_R + TRIM_W

# KDP barcode: 2 x 1.2in clear zone in a back-cover corner. Which corner is
# ambiguous once the wrap is flattened, so the WHOLE bottom band of the back
# panel is kept clear — satisfies either reading, and reads as intentional.
BAR_BAND_H = (1.2 + 0.25) * IN

def crop_to(path, w_pt, h_pt):
    im = Image.open(path).convert("RGB")
    target = w_pt / h_pt
    iw, ih = im.size
    if iw / ih > target:                  # too wide -> trim sides
        new_w = int(ih * target); x = (iw - new_w) // 2
        im = im.crop((x, 0, x + new_w, ih))
    else:                                  # too tall -> trim from the TOP
        new_h = int(iw / target)           # sky is empty; keep the cast at the base
        im = im.crop((0, ih - new_h, iw, ih))
    return im

def wrap_text(c, text, font, size, maxw):
    out, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if c.stringWidth(t, font, size) <= maxw: cur = t
        else: out.append(cur); cur = wd
    if cur: out.append(cur)
    return out

c = canvas.Canvas(OUT, pagesize=(W, H), initialFontName="Lora")
c.setTitle(f'{cfg["title"]} — cover'); c.setAuthor("Deep Roots Kids")

# Parchment Cream across the whole wrap, bleed included
c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)

# ── FRONT ── art bleeds off the right, top and bottom
art_src = f"{BOOK}/cover/front-art-v2-01.jpg"
art_w = FRONT_R - FRONT_L + BLEED
art = crop_to(art_src, art_w, H)
tmp = f"{BOOK}/cover/_front-placed.jpg"; art.save(tmp, quality=96)
c.drawImage(ImageReader(tmp), FRONT_L, 0, width=art_w, height=H, mask=None)

FX = (FRONT_L + FRONT_R) / 2
logo = ImageReader("kids/_brand/logo/dr-kids-logo.png")   # alpha-keyed
LW = 0.85 * IN
c.drawImage(logo, FX - LW/2, H - BLEED - SAFE - LW, width=LW, height=LW, mask="auto", preserveAspectRatio=True)

# Title: the dominant element after the scene. Auto-fit to the safe width and
# sized so it survives Amazon's ~150px-wide thumbnail.
max_w = TRIM_W - 2*SAFE - 0.35*IN
size = 74
while c.stringWidth(cfg["title"], "Baloo2", size) > max_w and size > 30:
    size -= 1
title_y = H - BLEED - SAFE - LW - size - 14
c.setFillColor(NAVY); c.setFont("Baloo2", size)
c.drawCentredString(FX, title_y, cfg["title"])

# Descriptor — what Amazon shoppers actually need to see on the thumbnail.
c.setFillColor(GOLD); c.setFont("Baloo2", 30)
c.drawCentredString(FX, title_y - 38, cfg["subtitle"])

# Series line, short form. "Creation to Glorification" and the Genesis
# reference now live on the back cover only.
c.setFillColor(NAVY); c.setFont("Lora", 13)
c.drawCentredString(FX, title_y - 64, COV["series_short"])


# ── SPINE ── blank: 34pp gives 0.077", far under KDP's 100-page threshold for text
# ── BACK ──
BX = (BACK_L + BACK_R) / 2
c.drawImage(logo, BX - LW/2, H - BLEED - SAFE - LW, width=LW, height=LW, mask="auto", preserveAspectRatio=True)

blurb = " ".join(COV["back_blurb"].split())

# Compose the back panel as one block centred in the space between the logo and
# the barcode band, rather than top-aligned with a gap underneath.
body_w = TRIM_W - 2*SAFE - 0.6*IN
blurb_lines = wrap_text(c, blurb, "Lora", 12.5, body_w)
spec_lines = list(COV.get("spec_lines") or [])
block_h = len(blurb_lines)*18 + 14 + len(spec_lines)*16 + 10 + 34

region_top = H - BLEED - SAFE - LW - 40
region_bot = BLEED + BAR_BAND_H + 0.15*IN
y = region_bot + (region_top - region_bot + block_h) / 2

c.setFillColor(NAVY); c.setFont("Lora", 12.5)
for ln in blurb_lines:
    c.drawCentredString(BX, y, ln); y -= 18
y -= 14
c.setFillColor(GREEN); c.setFont("Lora", 11)
for ln in spec_lines:
    c.drawCentredString(BX, y, ln); y -= 16
y -= 10
c.setFillColor(GOLD); c.setFont("Lora", 11.5)
c.drawCentredString(BX, y, cfg["series_line"]); y -= 18
c.setFillColor(NAVY); c.setFont("LoraIt", 11)
c.drawCentredString(BX, y, cfg["scripture_scope"])

if not RELEASE:   # proof stamp inside the barcode band's clear zone, on both panels
    c.setFillColor(NAVY); c.setFont("Lora", 9)
    for x in (BX, FX):
        c.drawCentredString(x, BLEED + SAFE, PROOF_STAMP)
c.save()
print(f"  cover.pdf — {W/IN:.3f} x {H/IN:.3f} in   spine {SPINE/IN:.4f} in ({PAGES}pp)")
print(f"  barcode band kept clear: back panel, bottom {BAR_BAND_H/IN:.2f} in")

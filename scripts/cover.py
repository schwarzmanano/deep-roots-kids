#!/usr/bin/env python3
"""Stage 9 — full-wrap cover per kids/_brand/brand-spec.md.

Unlike the interior, cover art is RASTER, so KDP's 300 DPI floor applies here.
Geometry: [bleed][back 8.5"][spine][front 8.5"][bleed] x (11" + bleed top/bottom).
"""
import os, yaml
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, CMYKColor
from PIL import ImageCms
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
# --target kdp (default) | lulu — the wraps differ in spine width and safety margin.
TARGET = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else "kdp"
if TARGET not in ("kdp", "lulu"): raise SystemExit(f"--target must be kdp or lulu, not {TARGET}")
OUT = (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv
       else f"{BOOK}/out/cover{'' if TARGET == 'kdp' else '-lulu'}.pdf")
AWAIT = "[ awaiting author's text ]"      # proof-only marker for an empty text slot — not prose
PROOF_STAMP = "PROOF - NOT FOR RELEASE"
IN = 72.0
cfg = yaml.safe_load(open(f"{BOOK}/book.yaml"))
if not cfg.get("author"):
    raise SystemExit(f"{BOOK}/book.yaml has no author: — the series author field (KDP/Lulu), e.g. \"Deep Roots\"")
AUTHOR = cfg["author"]           # PDF metadata author; matches the KDP/Lulu author field
if "cover" not in cfg:
    raise SystemExit(f"{BOOK}/book.yaml has no cover: block — cover text units not registered yet")
COV = cfg["cover"]
_missing = [k for k in ("series_short", "back_blurb") if COV.get(k) is None]
if cfg.get("subtitle") is None: _missing.append("subtitle")
if _missing and RELEASE:
    raise SystemExit(f"cover text incomplete ({', '.join(_missing)}) — awaiting the author's text")
_probs = textunits.check(BOOK)
if RELEASE and _probs:
    print(f"\n  ⛔ RELEASE REFUSED — {len(_probs)} problem(s) across {len({w for w, _ in _probs})} text unit(s), authorship-policy §11:\n")
    for where, why in _probs: print(f"    {where}: {why}")
    raise SystemExit(1)
if RELEASE:
    textunits.refuse_on_my_words(BOOK)    # my-words.md is the source of truth (2026-10-01)
PAGES = cfg["print"]["page_count"]

# Primary Palette
CREAM = HexColor("#F7EEDD"); GOLD = HexColor("#D9A441")
NAVY  = HexColor("#2E4257"); GREEN = HexColor("#4C7A5A")
CMYK_OUT = (cfg.get("cover") or {}).get("color") == "cmyk"
if CMYK_OUT:   # convert the palette through the same ICC transform as the art
    _SRGB = ImageCms.ImageCmsProfile("/System/Library/ColorSync/Profiles/sRGB Profile.icc")
    _CMYK = ImageCms.ImageCmsProfile("/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc")
    _XF = ImageCms.buildTransform(_SRGB, _CMYK, "RGB", "CMYK", renderingIntent=ImageCms.Intent.PERCEPTUAL)
    def _cmyk(hexc):
        px = Image.new("RGB", (1, 1), hexc); c_, m_, y_, k_ = ImageCms.applyTransform(px, _XF).getpixel((0, 0))
        return CMYKColor(c_/255, m_/255, y_/255, k_/255)
    CREAM, GOLD, NAVY, GREEN = (_cmyk(h) for h in ("#F7EEDD", "#D9A441", "#2E4257", "#4C7A5A"))

FD = "kids/_brand/fonts"
pdfmetrics.registerFont(TTFont("Baloo2", f"{FD}/Baloo2.ttf"))
pdfmetrics.registerFont(TTFont("Lora",   f"{FD}/Lora.ttf"))
pdfmetrics.registerFont(TTFont("LoraIt", f"{FD}/Lora-Italic.ttf"))

BLEED  = 0.125 * IN
TRIM_W, TRIM_H = 8.5 * IN, 11 * IN
if TARGET == "kdp":
    SPINE = PAGES * 0.002252 * IN        # white paper, per KDP
    SAFE  = 0.25 * IN                    # keep text this far inside trim
else:
    SPINE = (PAGES / 444 + 0.06) * IN    # Lulu paperback formula (Book Creation Guide p13)
    SAFE  = 0.5 * IN                     # Lulu safety margin, all sides
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
c.setTitle(f'{cfg["title"]} — cover'); c.setAuthor(AUTHOR)

# Parchment Cream across the whole wrap, bleed included
c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)

# ── FRONT ── art bleeds off the right, top and bottom
art_src = f"{BOOK}/{COV.get('front_art', 'cover/front-art-v2-01.jpg')}"
art_w = FRONT_R - FRONT_L + BLEED
art = crop_to(art_src, art_w, H)
tmp = f"{BOOK}/cover/_front-placed.jpg"
LOGO_SRC = "kids/_brand/logo/dr-kids-logo.png"
LW = 0.85 * IN
if CMYK_OUT:
    # Flatten: composite the alpha logo INTO the front art (no transparency in the PDF), then
    # convert the whole panel to CMYK through one ICC transform.
    _lg = Image.open(LOGO_SRC).convert("RGBA")
    _ppi = art.width / art_w                          # art pixels per point
    _lpx = int(LW * _ppi); _lg = _lg.resize((_lpx, _lpx), Image.LANCZOS)
    _x = int((FRONT_L + TRIM_W/2 - LW/2 - FRONT_L) * _ppi)
    _y = int((BLEED + SAFE) * _ppi)                   # PIL y-down from the top edge
    art = art.convert("RGBA"); art.alpha_composite(_lg, (_x, _y)); art = art.convert("RGB")
    art = ImageCms.applyTransform(art, _XF)
art.save(tmp, quality=96)
c.drawImage(ImageReader(tmp), FRONT_L, 0, width=art_w, height=H, mask=None)

FX = (FRONT_L + FRONT_R) / 2
logo = ImageReader(LOGO_SRC)   # alpha-keyed
if CMYK_OUT:   # back-panel logo: flattened onto cream, CMYK, no alpha
    _lg = Image.open(LOGO_SRC).convert("RGBA")
    _bg = Image.new("RGBA", _lg.size, "#F7EEDD"); _bg.alpha_composite(_lg)
    _bp = f"{BOOK}/cover/_logo-back-cmyk.jpg"
    ImageCms.applyTransform(_bg.convert("RGB"), _XF).save(_bp, quality=96)
    logo = ImageReader(_bp)
else:
    c.drawImage(logo, FX - LW/2, H - BLEED - SAFE - LW, width=LW, height=LW, mask="auto", preserveAspectRatio=True)

if COV.get("layout") == "v2":
    # v2 hierarchy (editor cover brief 2026-09-30): logo top · title upper-middle · art ·
    # subtitle + series badge at the bottom. Title set in capitals as a display style
    # (wording unchanged). Solid shapes only — no transparency (Lulu).
    max_w = TRIM_W - 2*SAFE - 0.2*IN
    ttl = cfg["title"].upper()
    size = 96
    while c.stringWidth(ttl, "Baloo2", size) > max_w and size > 30: size -= 1
    title_y = H - BLEED - SAFE - LW - 0.25*IN - size*0.8
    c.setFillColor(NAVY); c.setFont("Baloo2", size); c.drawCentredString(FX, title_y, ttl)
    # bottom panel: cream rounded plate holding subtitle, then the gold series badge
    sub = cfg.get("subtitle") or AWAIT
    ss = 30
    while c.stringWidth(sub, "Baloo2", ss) > max_w - 0.5*IN and ss > 14: ss -= 1
    badge = COV.get("series_short") or AWAIT
    bs = 15
    bw = c.stringWidth(badge, "Baloo2", bs) + 0.5*IN; bh = bs + 14
    plate_w = max(c.stringWidth(sub, "Baloo2", ss) + 0.6*IN, bw + 0.4*IN)
    plate_h = ss + bh + 0.55*IN
    py = BLEED + SAFE
    c.setFillColor(CREAM); c.roundRect(FX - plate_w/2, py, plate_w, plate_h, 14, stroke=0, fill=1)
    c.setFillColor(NAVY); c.setFont("Baloo2", ss)
    c.drawCentredString(FX, py + plate_h - 0.2*IN - ss*0.8, sub)
    c.setFillColor(GOLD); c.roundRect(FX - bw/2, py + 0.18*IN, bw, bh, bh/2, stroke=0, fill=1)
    c.setFillColor(NAVY); c.setFont("Baloo2", bs)
    c.drawCentredString(FX, py + 0.18*IN + (bh - bs*0.7)/2, badge)
else:
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
    _sub = cfg.get("subtitle") or AWAIT
    _ss = 30
    while c.stringWidth(_sub, "Baloo2", _ss) > max_w and _ss > 16: _ss -= 1   # layout fit, wording untouched
    c.setFont("Baloo2", _ss)
    c.drawCentredString(FX, title_y - 38, _sub)

    # Series line, short form. "Creation to Glorification" and the Genesis
    # reference now live on the back cover only.
    c.setFillColor(NAVY); c.setFont("Lora", 13)
    c.drawCentredString(FX, title_y - 64, COV.get("series_short") or AWAIT)


# ── SPINE ── blank: 34pp gives 0.077", far under KDP's 100-page threshold for text
# ── BACK ──
BX = (BACK_L + BACK_R) / 2
c.drawImage(logo, BX - LW/2, H - BLEED - SAFE - LW, width=LW, height=LW,
            mask=None if CMYK_OUT else "auto", preserveAspectRatio=True)

_bparas = [ " ".join(x.split()) for x in COV["back_blurb"].split("\n") if x.strip() ] if COV.get("back_blurb") else [AWAIT]
# A first paragraph ending in "?" is set as a lead line (Baloo 2); wording untouched.
lead = _bparas.pop(0) if len(_bparas) > 1 and _bparas[0].endswith("?") else None
blurb = " ".join(_bparas)

# Compose the back panel as one block centred in the space between the logo and
# the barcode band, rather than top-aligned with a gap underneath.
body_w = TRIM_W - 2*SAFE - 0.6*IN
blurb_lines = wrap_text(c, blurb, "Lora", 12.5, body_w)
_bw = body_w     # no one-word last line (widow): narrow the measure, never the words
while len(blurb_lines) > 1 and len(blurb_lines[-1].split()) < 2 and _bw > body_w * 0.8:
    _bw -= 6; blurb_lines = wrap_text(c, blurb, "Lora", 12.5, _bw)
spec_lines = list(COV.get("spec_lines") or [])
lead_lines = wrap_text(c, lead, "Baloo2", 20, body_w) if lead else []
block_h = len(lead_lines)*26 + (10 if lead else 0) + len(blurb_lines)*18 + 14 + len(spec_lines)*16 + 10 + 34

region_top = H - BLEED - SAFE - LW - 40
region_bot = BLEED + BAR_BAND_H + 0.15*IN
y = region_bot + (region_top - region_bot + block_h) / 2

c.setFillColor(NAVY); c.setFont("Baloo2", 20)
for ln in lead_lines:
    c.drawCentredString(BX, y, ln); y -= 26
if lead: y -= 10
c.setFillColor(NAVY); c.setFont("Lora", 12.5)
for ln in blurb_lines:
    c.drawCentredString(BX, y, ln); y -= 18
y -= 14
c.setFillColor(GREEN); c.setFont("Lora", 11)
def _tick(x, yb, sz):   # vector check mark: none of the brand fonts has U+2713
    c.saveState(); c.setStrokeColor(GREEN); c.setLineWidth(sz*0.13); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath(); p.moveTo(x, yb + sz*0.38); p.lineTo(x + sz*0.30, yb + sz*0.08); p.lineTo(x + sz*0.78, yb + sz*0.72)
    c.drawPath(p, stroke=1, fill=0); c.restoreState()
for ln in spec_lines:
    if ln.startswith("\u2713"):
        rest = ln[1:].lstrip(); tw = c.stringWidth(rest, "Lora", 11); gap = 11*0.95
        x0 = BX - (tw + gap)/2
        _tick(x0, y - 1, 11); c.drawString(x0 + gap, y, rest)
    else:
        c.drawCentredString(BX, y, ln)
    y -= 16
y -= 10
c.setFillColor(GOLD); c.setFont("Lora", 11.5)
c.drawCentredString(BX, y, cfg["series_line"]); y -= 18
c.setFillColor(NAVY); c.setFont("LoraIt", 11)
c.drawCentredString(BX, y, cfg["scripture_scope"])

# --concept-png <path>: clean front-panel PREVIEW image for review (never a PDF; the PDF
# written alongside is deleted). Proof PDFs always carry the stamp.
CONCEPT = sys.argv[sys.argv.index("--concept-png") + 1] if "--concept-png" in sys.argv else None
if not RELEASE and not CONCEPT:   # proof stamp just ABOVE the barcode band (the band itself must stay clear)
    c.setFillColor(NAVY); c.setFont("Lora", 9)
    for x in (BX, FX):
        c.drawCentredString(x, BLEED + BAR_BAND_H + 4, PROOF_STAMP)
c.save()
if CONCEPT:
    import pymupdf
    _p = pymupdf.open(OUT)[0]
    _clip = pymupdf.Rect(FRONT_L, 0, W, H)   # pymupdf is y-down; full height
    _p.get_pixmap(dpi=150, clip=_clip).save(CONCEPT)
    os.remove(OUT); print(f"  concept preview -> {CONCEPT} (PDF discarded)"); raise SystemExit(0)
print(f"  {os.path.basename(OUT)} [{TARGET}{'' if RELEASE else ', PROOF'}] — {W/IN:.3f} x {H/IN:.3f} in   spine {SPINE/IN:.4f} in ({PAGES}pp)")
print(f"  barcode band kept clear: back panel, bottom {BAR_BAND_H/IN:.2f} in")

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
RELEASE = "--release" in sys.argv
# --jpeg-quality N: lighter JPEG compression for size-capped uploads (default 96/95; ppi unchanged)
JPEG_Q = int(sys.argv[sys.argv.index("--jpeg-quality") + 1]) if "--jpeg-quality" in sys.argv else None          # authorship-policy §11 — same guard as layout.py
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
    import web; web.refuse(BOOK)           # quoted Scripture verbatim WEB (series rule 2026-10-01)
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
pdfmetrics.registerFont(TTFont("Baloo2Bold", f"{FD}/Baloo2-Bold.ttf"))   # static wght 700 (D-29)

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

GRID = COV.get("layout") == "grid"
FRONT_ART = sys.argv[sys.argv.index("--front-art") + 1] if "--front-art" in sys.argv else None
if GRID:
    # ── SERIES COVER GRID (kids/_brand/cover-grid.md, editor ruling 2026-10-03) ──────────
    import numpy as np, covergrid
    from PIL import ImageFilter
    G = covergrid.load()
    if not CMYK_OUT:
        raise SystemExit("cover.layout grid requires cover.color: cmyk")
    SIG_HEX = COV.get("signature_colour")
    if not SIG_HEX:
        raise SystemExit(f"{BOOK}/book.yaml: cover.signature_colour missing (cover-grid.md)")
    SIG = _cmyk(SIG_HEX)
    def _hexrgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
    def _lum(rgb):
        f = lambda v: v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
        r, g, b = (f(x/255) for x in rgb); return 0.2126*r + 0.7152*g + 0.0722*b
    def _contrast(a, b):
        la, lb = sorted((a, b), reverse=True); return (la + 0.05) / (lb + 0.05)

    # FRONT art — full bleed right/top/bottom, CMYK, no logo composited
    art_src = FRONT_ART or f"{BOOK}/{COV.get('front_art')}"
    art_w = FRONT_R - FRONT_L + BLEED
    art_rgb = crop_to(art_src, art_w, H)
    ART_PPI = art_rgb.height / (H / IN)
    tmp = f"{BOOK}/cover/_front-placed.jpg"
    ImageCms.applyTransform(art_rgb, _XF).save(tmp, quality=JPEG_Q or 96)
    c.drawImage(ImageReader(tmp), FRONT_L, 0, width=art_w, height=H, mask=None)

    # Banner — textured band in the signature colour, top trim + top bleed, full front width
    band_h = G["banner"]["height_in"] * IN
    bx0, by0, bw_, bh_ = FRONT_L, H - BLEED - band_h, W - FRONT_L, band_h + BLEED
    pxw, pxh = int(bw_ / IN * 400), int(bh_ / IN * 400)   # 400 ppi: comfortably over the 300 floor
    rng = np.random.default_rng(3)                        # deterministic texture
    grain = rng.normal(0, 1, (pxh, pxw))
    fibre = np.array(Image.fromarray(((rng.normal(0, 1, (pxh, pxw)) + 3) * 40).clip(0, 255).astype("uint8"))
                     .filter(ImageFilter.GaussianBlur((18, 2))), dtype=float)
    fibre = (fibre - fibre.mean()) / (fibre.std() + 1e-6)
    light = 1 + 0.025 * grain + 0.02 * fibre              # about ±4% lightness
    base = np.array(_hexrgb(SIG_HEX), dtype=float)
    band = (base[None, None, :] * light[:, :, None]).clip(0, 255).astype("uint8")
    _bp = f"{BOOK}/cover/_banner-cmyk.jpg"
    ImageCms.applyTransform(Image.fromarray(band, "RGB"), _XF).save(_bp, quality=JPEG_Q or 95)
    c.drawImage(ImageReader(_bp), bx0, by0, width=bw_, height=bh_, mask=None)
    banner_txt = (COV.get("series_short") or AWAIT).upper()
    bs = G["banner"]["text_max_pt"]
    safe_w = TRIM_W - 2 * SAFE
    while c.stringWidth(banner_txt, "Baloo2", bs) > safe_w and bs > 9: bs -= 0.5
    # banner text: "stronger contrast wins" against the band (cover-grid.md, option A)
    _bcs = {h: _contrast(_lum(_hexrgb(h)), _lum(_hexrgb(SIG_HEX))) for h in G["banner"]["text_colours"]}
    BANNER_HEX = max(_bcs, key=_bcs.get)
    c.setFillColor(_cmyk(BANNER_HEX)); c.setFont("Baloo2", bs)
    FX = (FRONT_L + FRONT_R) / 2
    c.drawCentredString(FX, H - BLEED - band_h / 2 - bs * 0.35, banner_txt)

    # Title + subtitle — upper third of the art, Navy or Cream by measured contrast
    ttl = cfg["title"]; sub = cfg.get("subtitle") or AWAIT
    ts = G["title"]["max_pt"]
    TF = "Baloo2Bold"                                   # title in Bold, Title Case as written
    while c.stringWidth(ttl, TF, ts) > safe_w - 0.2 * IN and ts > G["title"]["min_pt"]: ts -= 1
    ss = G["subtitle"]["max_pt"]
    while c.stringWidth(sub, "Lora", ss) > safe_w - 0.2 * IN and ss > G["subtitle"]["min_pt"]: ss -= 0.5
    t_base = H - BLEED - band_h - G["title"]["top_gap_in"] * IN - ts * 0.78
    s_base = t_base - ts * 0.25 - G["subtitle"]["gap_in"] * IN - ss * 0.8
    tw = max(c.stringWidth(ttl, TF, ts), c.stringWidth(sub, "Lora", ss))
    x0p = int((FX - tw / 2 - FRONT_L) / art_w * art_rgb.width); x1p = int((FX + tw / 2 - FRONT_L) / art_w * art_rgb.width)
    y0p = int((H - (t_base + ts * 0.85)) / H * art_rgb.height); y1p = int((H - (s_base - ss * 0.3)) / H * art_rgb.height)
    region = np.array(art_rgb.crop((x0p, y0p, x1p, y1p))).reshape(-1, 3)
    bg_l = float(np.mean([_lum(px) for px in region[:: max(1, len(region) // 4000)]]))
    choices = {h: _contrast(_lum(_hexrgb(h)), bg_l) for h in G["title"]["colours"]}
    TITLE_HEX = max(choices, key=choices.get)
    c.setFillColor(_cmyk(TITLE_HEX))
    c.setFont(TF, ts); c.drawCentredString(FX, t_base, ttl)
    c.setFont("Lora", ss); c.drawCentredString(FX, s_base, sub)
    GRID_REPORT = (f"title {ts:.0f}pt / subtitle {ss:.1f}pt in {TITLE_HEX} "
                   f"(contrast " + ", ".join(f"{h} {v:.2f}" for h, v in choices.items()) + f"); art {ART_PPI:.0f} ppi")

    # SPINE — signature colour only, no text (below both printers' spine-text minimums).
    # spine.overlap_in (grid, Book Four onward): the colour runs past both folds so a fold
    # tolerance never shows a cream or art sliver on the spine (editor brief 2026-10-16 §6).
    OVL = float(G["spine"].get("overlap_in", 0)) * IN
    c.setFillColor(SIG); c.rect(SPINE_L - OVL, 0, SPINE_R - SPINE_L + 2 * OVL, H, stroke=0, fill=1)

    # BACK — logo bottom-left; barcode box bottom-right kept clear; text block above
    LW = G["back"]["logo_in"] * IN
    LOGO_SRC = "kids/_brand/logo/dr-kids-logo.png"
    _lg = Image.open(LOGO_SRC).convert("RGBA")
    _bg = Image.new("RGBA", _lg.size, "#F7EEDD"); _bg.alpha_composite(_lg)
    _lpx = int(LW / IN * 400); _bg = _bg.resize((_lpx, _lpx), Image.LANCZOS)   # 400 ppi at print size (Lulu: none above 600)
    _lpath = f"{BOOK}/cover/_logo-back-cmyk.jpg"
    ImageCms.applyTransform(_bg.convert("RGB"), _XF).save(_lpath, quality=96)
    c.drawImage(ImageReader(_lpath), BACK_L + SAFE, BLEED + SAFE, width=LW, height=LW, mask=None)
    BAR = covergrid.barcode_box(TARGET, BACK_L, TRIM_W, BLEED, IN)
    BX = (BACK_L + BACK_R) / 2
    body_w = TRIM_W - 2 * SAFE - 0.6 * IN
    blurb = " ".join(" ".join(x.split()) for x in (COV.get("back_blurb") or AWAIT).split("\n") if x.strip())
    blines = wrap_text(c, blurb, "Lora", 12.5, body_w)
    spec = list(COV.get("spec_lines") or [])
    block_h = len(blines) * 18 + 14 + len(spec) * 16 + 10 + 34
    region_top = H - BLEED - SAFE
    region_bot = BLEED + max(SAFE + LW, BAR[3] - BLEED) + G["back"]["block_gap_in"] * IN
    # SERIES STRIP (grid series_strip, Book Four onward): front thumbnails of every published
    # book (earlier books' release cover.pdf front panels + this book's own front art), the
    # current book outlined; sits just above the logo/barcode zone. Images only — no new text.
    STRIP = G.get("series_strip")
    strip_h = 0
    if STRIP:
        import pymupdf, glob as _glob
        sh = STRIP["height_in"] * IN; sg = STRIP["gap_in"] * IN; sw_ = sh * (8.5 / 11)
        books = cfg.get("series_strip_books") or []
        thumbs = []
        for b in books:
            pdfp = f"kids/{b}/out/cover.pdf"
            if b == os.path.basename(BOOK.rstrip("/")) or not os.path.exists(pdfp):
                thumbs.append(None); continue
            _d = pymupdf.open(pdfp); _pg = _d[0]; _r = _pg.rect
            _bl = 0.125 * IN; _tw = 8.5 * IN
            _clip = pymupdf.Rect(_r.x1 - _bl - _tw, _bl, _r.x1 - _bl, _r.y1 - _bl)   # front panel at trim
            _tp = f"{BOOK}/cover/_strip-{b}.jpg"
            _pix = _pg.get_pixmap(dpi=int(400 * (sw_ / IN) / 8.5) + 1, clip=_clip)   # ~400 ppi at the strip's printed size
            ImageCms.applyTransform(Image.frombytes("RGB", (_pix.width, _pix.height), _pix.samples), _XF).save(_tp, quality=JPEG_Q or 95)
            thumbs.append(_tp)
        n = len(books); total_w = n * sw_ + (n - 1) * sg
        sx = BX - total_w / 2; sy = region_bot
        for i, b in enumerate(books):
            x = sx + i * (sw_ + sg)
            if thumbs[i]:
                c.drawImage(ImageReader(thumbs[i]), x, sy, width=sw_, height=sh, mask=None)
            else:
                # this book: its own front at trim — art, banner and title rendered small via the
                # placed art + a banner swatch (the title is set by this same script, so a thumbnail of
                # the finished front is produced on the second pass: --strip-self <png>)
                SELF = sys.argv[sys.argv.index("--strip-self") + 1] if "--strip-self" in sys.argv else None
                if SELF:
                    _sp = f"{BOOK}/cover/_strip-self-cmyk.jpg"
                    _si = Image.open(SELF).convert("RGB"); _sw = int(sw_ / IN * 400)   # 400 ppi at the strip's printed size
                    _si = _si.resize((_sw, int(_sw * _si.height / _si.width)), Image.LANCZOS)
                    ImageCms.applyTransform(_si, _XF).save(_sp, quality=JPEG_Q or 95)
                    c.drawImage(ImageReader(_sp), x, sy, width=sw_, height=sh, mask=None)
                else:
                    c.setFillColor(SIG); c.rect(x, sy, sw_, sh, stroke=0, fill=1)
                c.setStrokeColor(NAVY); c.setLineWidth(STRIP["outline_pt"]); c.rect(x, sy, sw_, sh, stroke=1, fill=0)
        strip_h = sh + G["back"]["block_gap_in"] * IN
        region_bot += strip_h
    WEB = COV.get("website_line")
    if WEB:
        block_h += 20
    y = region_bot + (region_top - region_bot + block_h) / 2
    c.setFillColor(NAVY); c.setFont("Lora", 12.5)
    for ln in blines: c.drawCentredString(BX, y, ln); y -= 18
    y -= 14; c.setFillColor(GREEN); c.setFont("Lora", 11)
    for ln in spec: c.drawCentredString(BX, y, ln); y -= 16
    y -= 10; c.setFillColor(GOLD); c.setFont("Lora", 11.5)
    c.drawCentredString(BX, y, cfg["series_line"]); y -= 18
    c.setFillColor(NAVY); c.setFont("LoraIt", 11)
    c.drawCentredString(BX, y, cfg["scripture_scope"])
    if WEB:
        y -= 20; c.setFillColor(GREEN); c.setFont("Lora", 10.5); c.drawCentredString(BX, y, WEB)
    BAR_BAND_H = region_bot - strip_h - BLEED - G["back"]["block_gap_in"] * IN   # for the proof stamp below
else:
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

# ISBN barcode (he-didnt-walk-away 2026-10-18, Lulu Global Distribution): Lulu places NO barcode on
# an uploaded cover ("place the barcode in the bottom-right corner of the back cover"), so when
# book.yaml isbn.lulu is a 13-digit ISBN the EAN-13 is drawn inside the grid's barcode box, on a
# paper-white panel, K only. KDP's box stays clear — KDP prints its own barcode there.
import re as _re
_ISBN = _re.sub(r"[^0-9]", "", str((cfg.get("isbn") or {}).get(TARGET) or ""))
OWN_BARCODE = bool(GRID) and TARGET == "lulu" and len(_ISBN) == 13
if OWN_BARCODE:
    from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
    from reportlab.graphics.shapes import Rect as _Rect, String as _String
    _K = CMYKColor(0, 0, 0, 1); _PAPER = CMYKColor(0, 0, 0, 0)
    bx0, by0, bx1, by1 = BAR
    # EAN-13 nominal is 1.469 x 1.02 in; drawn at ~1.9 in wide incl. quiet zones (≈130 %), bars 0.85 in.
    # The widget's shapes are emitted straight onto the canvas (renderPDF would add an RGB
    # Times-Roman state — unembedded font + rg operators, both preflight failures).
    _wd = Ean13BarcodeWidget(_ISBN, barWidth=1.9 * IN / 113.0, barHeight=0.85 * IN, humanReadable=1,
                             fontName="Lora", fontSize=9)
    _b = _wd.getBounds(); _bw, _bh = _b[2] - _b[0], _b[3] - _b[1]
    _pad = 0.08 * IN
    _px0 = bx1 - _bw - 2 * _pad - 0.05 * IN; _py0 = by0 + 0.05 * IN
    c.setFillColor(_PAPER); c.rect(_px0, _py0, _bw + 2 * _pad, _bh + 2 * _pad + 14, stroke=0, fill=1)
    _ox, _oy = _px0 + _pad - _b[0], _py0 + _pad - _b[1]
    c.setFillColor(_K)
    def _emit(node):
        for s in getattr(node, "contents", []):
            if isinstance(s, _Rect) and s.fillColor is not None:
                c.rect(_ox + s.x, _oy + s.y, s.width, s.height, stroke=0, fill=1)
            elif isinstance(s, _String):
                c.setFont(s.fontName, s.fontSize)
                {"start": c.drawString, "middle": c.drawCentredString, "end": c.drawRightString}[s.textAnchor](_ox + s.x, _oy + s.y, s.text)
            else:
                _emit(s)
    _emit(_wd.draw())
    c.setFont("Lora", 8)
    c.drawString(_px0 + _pad, _py0 + _pad + _bh + 4, f"ISBN {cfg['isbn'][TARGET]}")

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
if GRID:
    print(f"  grid v{G['grid_version']}: banner {SIG_HEX} text {BANNER_HEX} (contrast " + ", ".join(f"{h} {v:.2f}" for h, v in _bcs.items()) + f"); {GRID_REPORT}")
    if OWN_BARCODE:
        print(f"  EAN-13 {_ISBN} drawn in the {TARGET} barcode box ({(BAR[2]-BAR[0])/IN:.2f} x {(BAR[3]-BAR[1])/IN:.2f} in, bottom-right of the back panel; {_bw/IN:.2f} x {_bh/IN:.2f} in)")
    else:
        print(f"  barcode box kept clear ({TARGET}): {(BAR[2]-BAR[0])/IN:.2f} x {(BAR[3]-BAR[1])/IN:.2f} in, bottom-right of the back panel")
else:
    print(f"  barcode band kept clear: back panel, bottom {BAR_BAND_H/IN:.2f} in")

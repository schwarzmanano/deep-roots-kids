#!/usr/bin/env python3
"""Stage 7 — impose the book to KDP geometry and emit interior.pdf.

Art is placed as TRUE VECTOR (paths lifted from the traced SVG), not as a raster
image, so KDP's 300 DPI raster floor does not apply and lines print sharp.
"""
import os, re, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from badge import draw_badge
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, CMYKColor
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import reportlab

from bookarg import book_dir
import textunits
BOOK = book_dir()
# --release: authorship-policy §11 release guard, no proof stamp.
# Anything else is a PROOF, stamped on every page. --out <path> writes elsewhere (testing).
RELEASE = "--release" in sys.argv
# --target kdp (default): 8.5x11, no bleed.  --target lulu: same layout on an 8.75x11.25 page
# (0.125in bleed each side, Lulu requires bleed on all files); trim-relative positions identical.
TARGET = sys.argv[sys.argv.index("--target") + 1] if "--target" in sys.argv else "kdp"
if TARGET not in ("kdp", "lulu"):
    raise SystemExit(f"--target must be kdp or lulu, not {TARGET}")
OUT = (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv
       else f"{BOOK}/out/interior{'' if TARGET == 'kdp' else '-lulu'}.pdf")
PROOF_STAMP = "PROOF - NOT FOR RELEASE"
IN = 72.0  # pt per inch

cfg = yaml.safe_load(open(f"{BOOK}/book.yaml"))
plan = yaml.safe_load(open(f"{BOOK}/plan/pages.yaml"))

if cfg.get("print_ai_note", False):
    raise SystemExit("print_ai_note is true, but there is no author-supplied wording for it — "
                     "authorship-policy §3. The pipeline will not write one.")
_probs = textunits.check(BOOK)
if RELEASE and _probs:
    print(f"\n  ⛔ RELEASE REFUSED — {len(_probs)} problem(s) across {len({w for w, _ in _probs})} text unit(s), authorship-policy §11:\n")
    for where, why in _probs:
        print(f"    {where}: {why}")
    raise SystemExit(1)
if not RELEASE:
    print(f"  PROOF build — every page stamped '{PROOF_STAMP}'. "
          f"{len({w for w, _ in _probs})} text unit(s) would block a release (disclosure.py / --release for detail).")
pages = {p["page"]: p for p in plan["pages"]}

PW, PH = 8.5 * IN, 11 * IN            # TRIM — every coordinate below is trim-relative
BLEED = 0.125 * IN if TARGET == "lulu" else 0.0
M = cfg["margins"]
GUTTER, OUTSIDE = M["gutter_in"] * IN, M["outside_in"] * IN
TOP, BOTTOM = M["top_in"] * IN, M["bottom_in"] * IN
CAPTION_H = 1.0 * IN

# Per kids/_brand/brand-spec.md — Application Matrix, "Coloring book interior pages":
# Baloo 2 for headers, Lora for scripture/instructions. Both open-license Google Fonts.
FD = f"{BOOK}/../_brand/fonts"
pdfmetrics.registerFont(TTFont("Baloo2", f"{FD}/Baloo2.ttf"))
pdfmetrics.registerFont(TTFont("Lora", f"{FD}/Lora.ttf"))
pdfmetrics.registerFont(TTFont("LoraIt", f"{FD}/Lora-Italic.ttf"))

# Primary Palette. On a Black & White interior every mark must be true black —
# KDP screens colour to grey, which would wash out the captions on every page.
# The cover, which prints full colour, keeps the palette.
MONO = cfg["print"].get("ink", "black") == "black"
# Black is K-only (C0 M0 Y0 K100): solid black ink with no other colours (Lulu; KDP B&W).
# RGB black would be converted to a four-ink rich black at the printer.
K100  = CMYKColor(0, 0, 0, 1)
PAPER = CMYKColor(0, 0, 0, 0)
STORYBOOK_NAVY = K100 if MONO else HexColor("#2E4257")
ROOTS_GOLD     = K100 if MONO else HexColor("#D9A441")
LOGO_INTERIOR  = ("kids/_brand/logo/dr-kids-logo-gray.png" if MONO
                  else "kids/_brand/logo/dr-kids-logo.png")

TOK = re.compile(r"([MLCZ])([^MLCZ]*)")
NUM = re.compile(r"-?\d+\.?\d*")

def draw_svg(c, path_svg, x0, y0, w, h):
    src = open(path_svg).read()
    vw, vh = (float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src).groups())
    d = re.search(r'<path d="([^"]+)"', src).group(1)
    s = min(w / vw, h / vh)
    ox = x0 + (w - vw * s) / 2
    oy = y0 + (h - vh * s) / 2
    X = lambda v: ox + v * s
    Y = lambda v: oy + (vh - v) * s          # SVG y-down -> PDF y-up

    p = c.beginPath()
    for cmd, args in TOK.findall(d):
        n = [float(v) for v in NUM.findall(args)]
        if cmd == "M": p.moveTo(X(n[0]), Y(n[1]))
        elif cmd == "L":
            for i in range(0, len(n), 2): p.lineTo(X(n[i]), Y(n[i+1]))
        elif cmd == "C":
            for i in range(0, len(n), 6):
                p.curveTo(X(n[i]), Y(n[i+1]), X(n[i+2]), Y(n[i+3]), X(n[i+4]), Y(n[i+5]))
        elif cmd == "Z": p.close()
    c.setFillColor(K100)    # line art is always pure K
    c.drawPath(p, stroke=0, fill=1, fillMode=1)   # 1 = even-odd
    return vw * s / IN, vh * s / IN


def botanical_border(c, x0, y0, x1, y1, ink):
    """Thin double rule with a small leaf pair centred top and bottom.

    The interior prints in BLACK INK on white paper, so the spec's Parchment
    Cream ground cannot be used here — this is the black-ink equivalent.
    """
    # Inset so the leaf motifs, which overhang the rule by ~8pt, still land
    # inside the margin box — they pushed pp 1/2/33 to 0.431in before this.
    x0 += 9; y0 += 9; x1 -= 9; y1 -= 9
    c.saveState(); c.setStrokeColor(ink); c.setFillColor(ink)
    c.setLineWidth(1.0); c.rect(x0, y0, x1-x0, y1-y0, stroke=1, fill=0)
    c.setLineWidth(0.4); c.rect(x0+5, y0+5, (x1-x0)-10, (y1-y0)-10, stroke=1, fill=0)

    def leaf_pair(cx, cy, up):
        for sgn in (-1, 1):
            pth = c.beginPath(); pth.moveTo(cx, cy)
            pth.curveTo(cx + sgn*4, cy + up*5, cx + sgn*13, cy + up*8, cx + sgn*17, cy + up*1)
            pth.curveTo(cx + sgn*12, cy - up*1, cx + sgn*5, cy - up*1.5, cx, cy)
            c.drawPath(pth, stroke=0, fill=1)
        c.setLineWidth(0.9); c.line(cx, cy - up*5, cx, cy + up*3)

    mid = (x0 + x1) / 2
    # break the rule so the motif sits in clear space
    c.setFillColor(PAPER); c.setStrokeColor(PAPER)
    for yy in (y1, y0):
        c.rect(mid-26, yy-3.5, 52, 7, stroke=0, fill=1)
        c.rect(mid-26, (yy+5 if yy==y0 else yy-5)-3.5, 52, 7, stroke=0, fill=1)
    c.setFillColor(ink); c.setStrokeColor(ink)
    leaf_pair(mid, y1, -1)
    leaf_pair(mid, y0, +1)
    c.restoreState()


def wrap(c, text, font, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, font, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
# Flatten the interior logo: no alpha (Lulu: transparency must be flattened), grayscale
# (B&W images in grayscale). Written beside the output, never over the brand asset.
_logo = Image.open(LOGO_INTERIOR)
if _logo.mode in ("RGBA", "LA", "P"):
    _bg = Image.new("RGBA", _logo.size, (255, 255, 255, 255))
    _logo = Image.alpha_composite(_bg, _logo.convert("RGBA"))
LOGO_FLAT = os.path.join(os.path.dirname(OUT) or ".", "_logo-interior-flat.png")
_logo.convert("L" if MONO else "RGB").save(LOGO_FLAT)
c = canvas.Canvas(OUT, pagesize=(PW + 2*BLEED, PH + 2*BLEED),
                  initialFontName="Lora", initialFontSize=13)
c.setTitle(cfg["title"]); c.setAuthor("Deep Roots Kids"); c.setSubject(cfg["scripture_scope"])

for pno in range(1, cfg["print"]["page_count"] + 1):
    recto = pno % 2 == 1                      # odd = right-hand page
    left = GUTTER if recto else OUTSIDE       # binding side
    right = OUTSIDE if recto else GUTTER
    cx, cw = left, PW - left - right
    c.translate(BLEED, BLEED)                 # lulu: shift the trim box inside the bleed

    if pno == 1:
        botanical_border(c, cx, BOTTOM, PW - right, PH - TOP, STORYBOOK_NAVY)
        logo_w = 1.15*IN
        c.drawImage(ImageReader(LOGO_FLAT),
                    PW/2 - logo_w/2, PH*0.60 + 56, width=logo_w, height=logo_w,
                    preserveAspectRatio=True)
        c.setFillColor(STORYBOOK_NAVY)
        c.setFont("Baloo2", 34)
        c.drawCentredString(PW/2, PH*0.60, cfg["title"])
        if cfg.get("series_line"):
            c.setFillColor(ROOTS_GOLD)
            c.setFont("Lora", 11)
            c.drawCentredString(PW/2, PH*0.60 - 26, cfg["series_line"])
        c.setFillColor(STORYBOOK_NAVY)
        c.setFont("Lora", 14)
        c.drawCentredString(PW/2, PH*0.60 - 52, cfg["subtitle"])
        c.setFont("LoraIt", 11)
        c.drawCentredString(PW/2, PH*0.60 - 78, cfg["scripture_scope"])
    elif pno == 2:
        botanical_border(c, cx, BOTTOM, PW - right, PH - TOP, STORYBOOK_NAVY)
        # Border is inset 9pt with a second rule 5pt inside that; hold the copy
        # clear of both so nothing crosses the frame.
        PADX = 9 + 5 + 16
        tx = cx + PADX
        tw = (PW - right - PADX) - tx
        y = PH - TOP - 9 - 5 - 30
        c.setFillColor(STORYBOOK_NAVY)
        c.setFont("Baloo2", 11); c.drawString(tx, y, cfg["title"]); y -= 20
        # Copyright page: registered text units only (book.yaml copyright_page).
        # No AI note — authorship-policy §3.
        body = []
        for line in cfg.get("copyright_page") or []:
            body += [line, ""]
        c.setFont("Lora", 9)
        for para in body:
            if not para: y -= 10; continue
            for ln in wrap(c, para, "Lora", 9, tw):
                c.drawString(tx, y, ln); y -= 12
    elif pno in pages and pages[pno].get("back_matter"):
        pg = pages[pno]
        botanical_border(c, cx, BOTTOM, PW - right, PH - TOP, STORYBOOK_NAVY)
        # Body is either inline (book-specific) or read from a shared series asset,
        # so standing back matter stays in one place across every volume.
        body = textunits.body_of(pg)
        if body is None:
            # Empty slot awaiting the author's text. Proof only — the release guard refuses
            # to reach this line. A production marker, not prose.
            body = "[ awaiting author's text ]"
        paras = [ln.strip() for ln in body.strip().split("\n") if ln.strip()]
        # A page with a `heading:` key has its heading as a separate text unit (null = no
        # heading). Without the key (legacy, genesis-1 p33) the body's first line is the heading.
        heading = pg["heading"] if "heading" in pg else paras.pop(0)
        y = PH - TOP - 46
        if heading:
            c.setFillColor(STORYBOOK_NAVY); c.setFont("Baloo2", 20)
            c.drawCentredString(PW/2, y, heading); y -= 34
        else:
            y -= 10
        body_w = cw - 0.7*IN
        for para in paras:
            italic = para.startswith("For families:") or para.startswith("—")
            font, size, lead = ("LoraIt", 10.5, 14) if italic else ("Lora", 10.5, 14)
            c.setFont(font, size)
            for ln in wrap(c, para, font, size, body_w):
                c.drawString(cx + 0.35*IN, y, ln); y -= lead
            y -= 9
        # Optional editorial footnote (e.g. a publishing-choice disclosure ruled at
        # Gate 1), set small at the foot of the page, stacked up from the floor.
        if pg.get("footnote"):
            fn_w = cw - 0.7*IN
            fl = wrap(c, " ".join(pg["footnote"].split()), "LoraIt", 9, fn_w)
            fy = BOTTOM + 24
            top = fy + 11*(len(fl) - 1) + 14
            if y < top + 10:
                raise SystemExit(f"p{pno}: body text runs into the footnote — shorten one")
            c.setStrokeColor(STORYBOOK_NAVY); c.setLineWidth(0.5)
            c.line(PW/2 - 0.75*IN, top, PW/2 + 0.75*IN, top)
            c.setFont("LoraIt", 9)
            for ln in reversed(fl):
                c.drawCentredString(PW/2, fy, ln); fy += 11

    elif pno in pages and not pages[pno].get('placeholder'):
        pg = pages[pno]
        # Caption lines, top-to-bottom, then stacked upward from a hard floor.
        rows = [(ln, "Lora", 13, 16) for ln in wrap(c, pg["text"], "Lora", 13, cw)]
        if pg.get("teaching"):
            rows.append(("", "Lora", 13, 5))
            rows += [(ln, "LoraIt", 9, 11)
                     for ln in wrap(c, " ".join(pg["teaching"].split()), "LoraIt", 9, cw*0.88)]
        FLOOR = BOTTOM + 16                     # lowest baseline permitted
        c.setFillColor(STORYBOOK_NAVY)          # spec: scripture never black
        y = FLOOR
        for text, font, size, lead in reversed(rows):
            if text:
                c.setFont(font, size); c.drawCentredString(PW/2, y, text)
            y += lead
        art_y = y + 10                           # art sits above the tallest caption
        art_h = PH - TOP - art_y
        # 3pt inset: traced Bezier control points can sit a hair outside the
        # viewBox, which put p5 0.031in over the top margin before this.
        INSET = 3
        svg = f"{BOOK}/art/p{pno}.svg"
        if os.path.exists(svg):
            draw_svg(c, svg, cx + INSET, art_y + INSET, cw - 2*INSET, art_h - 2*INSET)
        if recto:
            c.setFillColor(STORYBOOK_NAVY)
            c.setFont("Lora", 8)
            c.drawRightString(PW - right, BOTTOM + 4, str(pno))
    if not RELEASE:
        c.setFillColor(STORYBOOK_NAVY); c.setFont("Lora", 7)
        c.drawCentredString(PW/2, BOTTOM + 3, PROOF_STAMP)
    c.showPage()

c.save()
print(f"  interior.pdf written — {cfg['print']['page_count']} pages, "
      f"{os.path.getsize(OUT)/1024:.0f} KB  -> {OUT}{'  [RELEASE]' if RELEASE else '  [PROOF]'}")

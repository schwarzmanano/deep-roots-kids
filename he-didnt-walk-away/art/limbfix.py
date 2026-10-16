#!/usr/bin/env python3
"""Post-drawn corrections for Book Four's interior line art — the mended cup's SEAM (Gate 2 ruling
B1-2, editor 2026-10-17) and any hand limb corrections that QA needs.

R3: the mending is His promise, not our repair. The model draws a seam only as a crack (jagged) or
not at all, so the cup is GENERATED WHOLE (style.md) and the seam is drawn here: ONE straight thin
hairline down the old crack, identical in construction on p27 and p29 — the same object the cover
carries in Roots Gold. Nothing else about the cup is touched.

Interface (read by scripts/qa.py exactly as Book Three's art/limbfix.py): `OPS` maps a page number
to a list of ops; `apply(page)` reads art/pre-limbfix/pNN.png and writes art/pNN.png. Ops are in
source pixels of the processed page (see the size printed by qa.py):
  ("seam",  (x1, y1), (x2, y2), w)    one straight line, ink, stroke w px (a hairline: thinner than
                                      the outline W but never under the 2 pt print floor)
  ("erase", [(x, y), ...])            polygon filled white
  ("line",  [(x, y), ...])            polyline, ink, stroke W
  ("oval",  (cx, cy, rx, ry))         closed oval outline, ink, stroke W, white inside
Coordinates are filled in at QA once p27 and p29 art is CHOSEN; until then OPS is empty and qa.py
skips this file. Usage: python art/limbfix.py [page ...]
"""
import sys
from PIL import Image, ImageDraw

W = 5            # outline stroke width of the figures at the processed size (measure at QA)
SS = 4           # supersample, then threshold back to bitonal

OPS = {
    # p5 (927 x 1200): the model's curly wind marks in the sky erased (editor 2026-10-17, "correct
    # everything" — DECISION-1 keeps the sky empty; wind stays in the bent treetops only).
    5: [("erase", [(285, 78), (555, 78), (555, 236), (285, 236)]),
        ("erase", [(430, 258), (645, 258), (645, 322), (430, 322)]),
        ("erase", [(640, 274), (666, 274), (666, 290), (640, 290)])],   # the line's tail at the canopy edge
    # Measured on the processed pages (877 x 1135), 2026-10-17. The seam sits just off the cup's
    # centre line, inside the body, touching neither the rim nor the base outline.
    27: [("seam", (440, 790), (440, 848), 3)],
    29: [("erase", [(425, 1037), (466, 1037), (466, 1102), (425, 1102)]),   # the model's wavy crack
         ("erase", [(436, 1100), (458, 1100), (458, 1106), (436, 1106)]),   # its curl at the base
         ("seam", (447, 1040), (447, 1102), 3)],
}


def apply(page):
    src = Image.open(f"art/pre-limbfix/p{page}.png").convert("L")
    w, h = src.size
    im = src.resize((w * SS, h * SS), Image.NEAREST)
    d = ImageDraw.Draw(im)
    S = lambda pts: [(x * SS, y * SS) for x, y in pts]
    for op in OPS.get(page, []):
        kind = op[0]
        if kind == "seam":
            (_, a, b, sw) = op
            d.line(S([a, b]), fill=0, width=max(1, int(sw * SS)))
        elif kind == "erase":
            d.polygon(S(op[1]), fill=255)
        elif kind == "line":
            d.line(S(op[1]), fill=0, width=W * SS, joint="curve")
        elif kind == "oval":
            cx, cy, rx, ry = op[1]
            box = [((cx - rx) * SS, (cy - ry) * SS), ((cx + rx) * SS, (cy + ry) * SS)]
            d.ellipse(box, fill=255, outline=0, width=W * SS)
        else:
            raise SystemExit(f"p{page}: unknown op {kind}")
    out = im.resize((w, h), Image.LANCZOS).point(lambda v: 0 if v < 128 else 255).convert("1")
    out.save(f"art/p{page}.png")
    print(f"  p{page}: {len(OPS.get(page, []))} op(s) applied -> art/p{page}.png")


if __name__ == "__main__":
    for p in (map(int, sys.argv[1:]) if len(sys.argv) > 1 else sorted(OPS)):
        apply(p)

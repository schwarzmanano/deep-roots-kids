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
  ("tubelegs", poly, n, (rx, ry))     zone holding n two-sided limbs (legs or hanging arms): each limb's
                                      centre is fitted from the rows where exactly 2n strokes cross, the
                                      zone is erased, one line per limb is drawn, and an oval (rx, ry)
                                      end (foot or hand) is drawn centred under/at the limb's lower end
                                      (ported from we-broke-it-all art/limbfix.py, 2026-10-17)
  ("erase_comps_in", (x0, y0, x1, y1)) every detached ink shape lying wholly inside the box
  ("erase", [(x, y), ...])            polygon filled white
  ("line",  [(x, y), ...])            polyline, ink, stroke W
  ("oval",  (cx, cy, rx, ry))         closed oval outline, ink, stroke W, white inside
Coordinates are filled in at QA once p27 and p29 art is CHOSEN; until then OPS is empty and qa.py
skips this file. Usage: python art/limbfix.py [page ...]
"""
import sys
from PIL import Image, ImageDraw

W = 5            # outline stroke width of the figures at the processed size (measure at QA)
WPAGE = {3: 8}   # pages whose figure outlines are heavier (measured 2026-10-17: p3 median 7-9 px)
SS = 4           # supersample, then threshold back to bitonal

OPS = {
    # p5: the sky wind marks erased (editor 2026-10-17) — see the p5 entry below.
    # Limb corrections (editor 2026-10-17, "correct all the limbs on pages 3, 5, 7, 9, 15, 21"):
    # the first couple's two-sided legs refitted as single lines; mitten/pointing hands → plain
    # ovals. Zones measured on the processed pages (927 x 1200) from ink-run scans.
    3: [  # the trunk edge runs into both the man's left leg and his arm, so these are drawn explicitly
        # woman's legs (right leg borders the trunk; the zone's right edge follows the trunk edge)
        ("erase", [(538, 886), (629, 886), (627, 935), (613, 965), (613, 1002), (538, 1002)]),
        ("line", [(562, 880), (560, 990)]), ("oval", (560, 998, 16, 9)),
        ("line", [(606, 880), (601, 988)]), ("oval", (600, 996, 13, 8)),
        # man's legs (the zone's left edge follows the trunk edge + 6 px)
        ("erase", [(296, 858), (430, 858), (430, 1002), (336, 1002), (326, 982), (312, 962), (304, 935), (298, 905)]),
        ("line", [(331, 856), (334, 988)]), ("oval", (334, 996, 18, 10)),
        ("line", [(390, 856), (393, 988)]), ("oval", (393, 996, 18, 10)),
        # man's left arm: the forearm hanging out from behind the trunk — two-sided + lens hand → one line + oval
        ("erase", [(236, 700), (276, 700), (276, 850), (236, 850)]),            # left of the trunk edge
        ("erase", [(289, 700), (300, 700), (300, 748), (289, 748)]),            # the inner arm line right of the edge
        ("line", [(277, 694), (282, 734)]),                                    # the trunk edge, restored where the old arm merged into it
        ("erase", [(288, 775), (303, 775), (303, 793), (288, 793)]),            # bar of the old hand against the garment
        ("line", [(281, 735), (253, 808)]), ("oval", (251, 824, 12, 16)),
        # woman's RIGHT arm: a lens drawn across her back against the trunk → its inner contour erased (the arm is behind the trunk)
        ("erase", [(596, 604), (612, 604), (645, 760), (632, 770)]),            # the lens's inner line, shoulder to where it meets the trunk
        ("erase", [(630, 694), (642, 694), (642, 714), (630, 714)]),            # its elbow chunk
        ("line", [(641, 746), (646, 774)]),                                    # the edge smoothed where the lens met it
        ("erase", [(600, 592), (615, 592), (615, 618), (600, 618)]),            # the lens's tip beside the hair
        ("erase", [(296, 712), (302, 712), (302, 726), (296, 726)]),            # spur of the old arm at the garment
        # man's RIGHT arm: a two-sided contour hugging the garment's right edge → erased outside the edge, one line + oval
        ("erase", [(425, 555), (452, 555), (452, 748), (424, 748), (426, 700), (427, 640)]),
        ("line", [(424, 574), (453, 778)]), ("oval", (457, 795, 11, 15)),
        # woman's LEFT arm: a lens drawn over the dress → the inner contour erased, one line outside the dress + oval
        ("erase", [(531, 652), (556, 652), (556, 750), (531, 750)]),
        ("line", [(523, 662), (489, 796)]), ("oval", (486, 812, 11, 15)),
        # stubs of the old two-sided legs just under the hems
        ("erase", [(309, 854), (320, 854), (320, 861), (309, 861)]), ("erase", [(344, 854), (355, 854), (355, 861), (344, 861)]),
        ("erase", [(367, 854), (378, 854), (378, 861), (367, 861)]), ("erase", [(403, 854), (414, 854), (414, 861), (403, 861)]),
        ("erase", [(542, 884), (553, 884), (553, 887), (542, 887)]), ("erase", [(573, 884), (584, 884), (584, 887), (573, 887)]),
        ("erase", [(586, 884), (597, 884), (597, 887), (586, 887)]), ("erase", [(617, 884), (628, 884), (628, 887), (617, 887)])],
    5: [("erase", [(285, 78), (555, 78), (555, 236), (285, 236)]),
        ("erase", [(430, 258), (645, 258), (645, 322), (430, 322)]),
        ("erase", [(640, 274), (666, 274), (666, 290), (640, 290)]),
        ("erase", [(520, 1035), (574, 1035), (574, 1074), (520, 1074)]), ("erase", [(582, 1035), (640, 1035), (640, 1074), (582, 1074)]),   # her open C-shaped feet
        ("tubelegs", [(525, 932), (620, 932), (620, 1034), (525, 1034)], 2, (20, 10))],  # woman's legs + oval feet
    7: [("erase", [(312, 1037), (362, 1037), (362, 1080), (312, 1080)]), ("erase", [(372, 1037), (426, 1037), (426, 1084), (372, 1084)]),   # her open C-shaped feet
        ("tubelegs", [(315, 945), (410, 945), (410, 1036), (315, 1036)], 2, (20, 10))],  # woman's legs + oval feet
    9: [("erase", [(312, 1037), (362, 1037), (362, 1080), (312, 1080)]), ("erase", [(372, 1037), (426, 1037), (426, 1084), (372, 1084)]),   # her open C-shaped feet
        ("tubelegs", [(315, 945), (410, 945), (410, 1036), (315, 1036)], 2, (20, 10))],  # woman's legs + oval feet
    15: [("tubelegs", [(595, 886), (715, 886), (715, 1018), (595, 1018)], 2),        # woman's legs
         ("erase", [(572, 1021), (722, 1021), (722, 1071), (572, 1071)]),               # her open half-oval feet
         ("oval", (627, 1031, 16, 9)), ("oval", (690, 1031, 16, 9)),
         ("erase", [(150, 718), (198, 718), (198, 790), (150, 790)]),                 # man's left mitten
         ("erase", [(158, 721), (166, 721), (166, 742), (158, 742)]), ("erase", [(175, 721), (183, 721), (183, 742), (175, 742)]),   # its ticks beside the arm
         ("line", [(170, 712), (171, 744)]), ("oval", (172, 762, 12, 18)),
         ("erase", [(444, 498), (508, 498), (508, 578), (444, 578)]),                 # man's pointing hand
         ("line", [(448, 582), (471, 552)]), ("oval", (482, 537, 12, 18)),           # continues the arm's own direction
         ("erase", [(738, 712), (786, 712), (786, 782), (738, 782)]),                 # woman's right mitten
         ("line", [(758, 706), (759, 736)]), ("oval", (760, 754, 12, 18))],
    21: [("erase", [(520, 1035), (574, 1035), (574, 1074), (520, 1074)]), ("erase", [(582, 1035), (640, 1035), (640, 1074), (582, 1074)]),   # her open C-shaped feet
         # the ragged hem's points hang down to y 948 right above the old leg lines, so the stub walk is
         # off here and the three free-standing stubs are erased by hand (the right leg's inner stub is a hem point)
         ("erase", [(533, 929), (544, 929), (544, 949), (533, 949)]), ("erase", [(558, 929), (569, 929), (569, 949), (558, 949)]),
         ("erase", [(604, 929), (615, 929), (615, 949), (604, 949)]),
         ("tubelegs", [(525, 948), (620, 948), (620, 1034), (525, 1034)], 2, (20, 10), {"stubs": False})],
    # Measured on the processed pages (877 x 1135), 2026-10-17. The seam sits just off the cup's
    # centre line, inside the body, touching neither the rim nor the base outline.
    27: [("seam", (440, 790), (440, 848), 3)],
    29: [("erase", [(425, 1037), (466, 1037), (466, 1102), (425, 1102)]),   # the model's wavy crack
         ("erase", [(436, 1100), (458, 1100), (458, 1106), (436, 1106)]),   # its curl at the base
         ("seam", (447, 1040), (447, 1102), 3)],
}



def tube_centres(ink, poly, n):
    import numpy as np
    m = Image.new("L", (ink.shape[1], ink.shape[0]), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    zone = np.asarray(m) > 0
    ys = np.where(zone.any(1))[0]; cen = [[] for _ in range(n)]
    for y in ys:
        xs = np.where(ink[y] & zone[y])[0]
        if not len(xs): continue
        runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1)
        if len(runs) != 2 * n: continue
        mids = [r.mean() for r in runs]
        for k in range(n): cen[k].append((y, (mids[2 * k] + mids[2 * k + 1]) / 2))
    lines = []
    for c in cen:
        if len(c) < 4: raise SystemExit(f"tubelegs: a limb in zone {poly[:2]}... has too few clean rows ({len(c)})")
        c = np.array(c); pts = []
        for y in range(int(c[0, 0]), int(c[-1, 0]) + 1, 12):
            sel = c[np.abs(c[:, 0] - y) <= 6]
            if len(sel): pts.append((float(np.median(sel[:, 1])), float(y)))
        pts.append((float(np.median(c[-4:, 1])), float(c[-1, 0])))
        lines.append(pts)
    return ys.min(), ys.max(), lines


def apply(page):
    import numpy as np
    from scipy import ndimage
    global W
    W = WPAGE.get(page, 5)
    src = Image.open(f"art/pre-limbfix/p{page}.png").convert("L")
    ink = np.asarray(src) < 128
    w, h = src.size
    im = src.resize((w * SS, h * SS), Image.NEAREST)
    d = ImageDraw.Draw(im)
    S = lambda pts: [(x * SS, y * SS) for x, y in pts]
    r = W * SS / 2
    for op in OPS.get(page, []):
        kind = op[0]
        if kind == "seam":
            (_, a, b, sw) = op
            d.line(S([a, b]), fill=0, width=max(1, int(sw * SS)))
        elif kind == "erase":
            d.polygon(S(op[1]), fill=255)
        elif kind == "erase_comps_in":
            x0, y0, x1, y1 = op[1]
            lab, _ = ndimage.label(ink, structure=np.ones((3, 3)))
            comp = np.zeros_like(ink)
            for i, sl in enumerate(ndimage.find_objects(lab), 1):
                if sl[1].start >= x0 and sl[1].stop <= x1 and sl[0].start >= y0 and sl[0].stop <= y1:
                    comp |= lab == i
            ys, xs = np.where(comp)
            for y, x in zip(ys, xs): d.rectangle([x * SS, y * SS, x * SS + SS - 1, y * SS + SS - 1], fill=255)
        elif kind == "line":
            pts = S(op[1]); d.line(pts, fill=0, width=W * SS, joint="curve")
            for x, y in (pts[0], pts[-1]): d.ellipse([x - r, y - r, x + r, y + r], fill=0)
        elif kind == "tubelegs":
            poly, n = op[1], op[2]; end = op[3] if len(op) > 3 else None
            opts = op[4] if len(op) > 4 else {}
            y0, y1, limbs = tube_centres(ink, poly, n)
            d.polygon(S(poly), fill=255)
            # stubs: the old two-sided lines continue a few px past the zone (under the hem, above the
            # foot); erase 7 px beyond the zone at each old line's position, 8 px wide
            m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).polygon(poly, fill=255); zone = np.asarray(m) > 0
            zys = np.where(zone.any(1))[0]
            # walk outward row by row and erase only narrow (≤ 9 px) runs — a vertical stroke — stopping
            # at the first wide run (the hem or the foot outline), so neither is nicked
            for yy, dy in (((zys.min(), -1), (zys.max(), +1)) if opts.get("stubs", True) else ()):
                xs = np.where(ink[yy] & zone[yy])[0]
                for run in (np.split(xs, np.where(np.diff(xs) > 1)[0] + 1) if len(xs) else []):
                    cx = int(run.mean())
                    for k in range(1, 14):
                        y2 = yy + dy * k
                        if y2 < 0 or y2 >= h: break
                        seg = np.where(ink[y2, max(cx - 7, 0):cx + 8])[0]
                        if not len(seg): break
                        r2 = np.split(seg, np.where(np.diff(seg) > 1)[0] + 1)
                        r2 = [q for q in r2 if (q.min() + q.max()) / 2 + max(cx - 7, 0) - cx < 6 and len(q) <= 9]
                        if not r2: break
                        q = r2[0] + max(cx - 7, 0)
                        d.rectangle([q.min() * SS, y2 * SS, (q.max() + 1) * SS - 1, y2 * SS + SS - 1], fill=255)
            for pts in limbs:
                (xa, ya), (xb, yb) = pts[0], pts[1]
                (xc, yc), (xd, yd) = pts[-2], pts[-1]
                top = (xa - (xb - xa) * 4 / max(yb - ya, 1), ya - 4)
                bot = (xd + (xd - xc) * 4 / max(yd - yc, 1), yd + 4)
                # run the line on upward until it meets the original ink (the hem), overlapping 3 px,
                # so no gap is left where the first clean rows sat below the hem
                ux, uy = (xa - xb), (ya - yb); L = max((ux * ux + uy * uy) ** 0.5, 1e-6); ux, uy = ux / L, uy / L
                for k in range(4, 40):
                    tx, ty = int(round(xa + ux * k)), int(round(ya + uy * k))
                    if ty < 0 or tx < 1 or tx >= w - 1: break
                    if ink[ty, tx - 1:tx + 2].any():
                        top = (xa + ux * (k + 3), ya + uy * (k + 3)); break
                P = S([top] + pts + [bot])
                d.line(P, fill=0, width=W * SS, joint="curve")
                for x, y in (P[0], P[-1]): d.ellipse([x - r, y - r, x + r, y + r], fill=0)
                if end:
                    fx, fy = P[-1]; rx, ry = end[0] * SS, end[1] * SS; fy += ry - 2 * SS
                    d.ellipse([fx - rx, fy - ry, fx + rx, fy + ry], fill=255, outline=0, width=W * SS)
        elif kind == "oval":
            cx, cy, rx, ry = op[1]
            box = [((cx - rx) * SS, (cy - ry) * SS), ((cx + rx) * SS, (cy + ry) * SS)]
            d.ellipse(box, fill=255, outline=0, width=W * SS)
        else:
            raise SystemExit(f"p{page}: unknown op {kind}")
    out = im.resize((w, h), Image.LANCZOS).point(lambda v: 0 if v < 128 else 255)
    # leftovers of erased strokes: tiny ink islands inside the edited areas only
    o = np.asarray(out) < 128; touched = np.zeros_like(o)
    for op in OPS.get(page, []):
        if op[0] in ("erase", "line", "tubelegs"): pts = op[1]
        elif op[0] == "erase_comps_in": pts = [op[1][:2], op[1][2:]]
        elif op[0] == "oval": cx, cy, rx, ry = op[1]; pts = [(cx - rx, cy - ry), (cx + rx, cy + ry)]
        elif op[0] == "seam": pts = [op[1], op[2]]
        xs, ys = zip(*pts)
        touched[max(min(ys) - 8, 0):max(ys) + 8, max(min(xs) - 8, 0):max(xs) + 8] = True
    lab, n = ndimage.label(o); sizes = ndimage.sum(o, lab, range(1, n + 1))
    small = np.isin(lab, np.where(sizes < 30)[0] + 1) & touched
    o[small] = False
    Image.fromarray(np.where(o, 0, 255).astype(np.uint8)).convert("1").save(f"art/p{page}.png")
    print(f"  p{page}: {len(OPS.get(page, []))} op(s) applied -> art/p{page}.png")


if __name__ == "__main__":
    for p in (map(int, sys.argv[1:]) if len(sys.argv) > 1 else sorted(OPS)):
        apply(p)

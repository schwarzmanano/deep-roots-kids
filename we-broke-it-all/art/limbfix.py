#!/usr/bin/env python3
"""Limb corrections for Book Three's interior line art (editor request 2026-10-12).

style.md: every arm and leg ONE single thin line; hands and feet plain closed ovals (first
couple) or mittens (family); the arm leaves the garment at the shoulder, held away from the
body. The generated pages broke this in four recurring ways, fixed here by hand:
  tube legs     a leg drawn as two parallel lines  -> one centre line
  shoulder loop a lens/loop where the arm meets the garment -> clean garment edge + arm line
  sliver arm    an arm drawn as a lens hugging the dress, no hand -> arm line + oval hand
  missing limb  an arm absent or ending without a hand -> drawn in

Source: art/pre-limbfix/pNN.png (the approved bitonal art). Output: art/pNN.png, which
scripts/vectorize.py then traces to art/pNN.svg. Ops are in source pixels (927 x 1200):
  ("erase", [(x, y), ...])            polygon filled white
  ("line",  [(x, y), ...])            polyline, ink, stroke W
  ("oval",  (cx, cy, rx, ry))         closed oval outline, ink, stroke W, white inside
  ("tubelegs", [(x, y), ...], n)      zone between hem and feet holding n two-sided legs: each
                                      leg's centre is fitted from the rows where exactly 2n
                                      strokes cross, the zone is erased, one line per leg drawn
                                      from just inside the hem to just inside the foot
Usage: python art/limbfix.py [page ...]   (no args = every page in OPS)
"""
import sys
from PIL import Image, ImageDraw

W = 5            # measured stroke width of the figures' outlines at 927 x 1200
SS = 4           # supersample, then threshold back to bitonal

OPS = {
    3: [
        # woman, viewer-left: arm drawn as a sliver hugging the dress, no hand -> arm + oval hand
        ("erase", [(517, 754), (536, 754), (536, 801), (519, 801), (517, 790)]),
        ("line", [(511, 748), (501, 790), (494, 828)]),
        ("oval", (490, 847, 10, 19)),
        # woman: tube legs -> one line each (hem y 915-921; foot tops y 1042 / 1050)
        ("erase", [(526, 917), (540, 919), (550, 920), (560, 921), (570, 922), (580, 925), (590, 922), (600, 921),
                   (610, 919), (618, 918), (618, 1047), (586, 1047), (586, 1040), (526, 1040)]),
        ("line", [(550, 916), (536, 1043)]),
        ("line", [(595, 916), (595, 1051)]),
    ],
    5: [
        # woman, viewer-left: arm drawn as a sliver beside the dress, no hand -> arm + oval hand
        ("erase", [(276, 714), (290, 714), (290, 740), (289, 760), (288, 770), (276, 770)]),
        ("line", [(284, 714), (272, 770), (264, 818)]),
        ("oval", (261, 836, 10, 19)),
        # woman, viewer-right: arm and dress edge touch at the shoulder (closed loop) -> arm leaves cleanly
        ("erase", [(393, 668), (404, 668), (404, 700), (412, 740), (426, 779), (397, 779), (397, 708), (393, 704)]),
        ("line", [(398, 662), (421, 779)]),
        # woman: tube legs -> one line each (walking: back leg bent at the knee)
        ("tubelegs", [(255, 902), (350, 902), (350, 1016), (255, 1016)], 1),
        ("tubelegs", [(355, 902), (405, 902), (405, 1033), (355, 1033)], 1),
    ],
    7: [
        # the man is already single-line throughout. Woman (same build as p3):
        ("erase", [(516, 753), (533, 753), (533, 801), (517, 801), (515, 790)]),   # sliver arm, no hand
        ("line", [(511, 746), (500, 790), (494, 828)]),
        ("oval", (491, 846, 10, 19)),
        ("tubelegs", [(530, 922), (571, 922), (571, 1040), (526, 1040)], 1),          # tube legs
        ("tubelegs", [(577, 922), (616, 922), (616, 998), (605, 1004), (605, 1046), (584, 1046)], 1),
    ],
    9: [
        # arms are single lines with hands (shoulder armholes left as drawn); man's legs single.
        # woman: tube legs -> one line each
        ("tubelegs", [(330, 917), (371, 917), (371, 1036), (328, 1036)], 1),
        ("tubelegs", [(377, 917), (416, 917), (416, 1045), (385, 1045)], 1),
    ],
    11: [
        # man single-line throughout. Woman, viewer-right: sliver arm merging into the dress, no hand
        ("erase", [(258, 712), (271, 712), (271, 792), (259, 792)]),
        ("line", [(255, 712), (272, 762), (286, 815)]),
        ("oval", (289, 833, 10, 19)),
        # woman: tube legs -> one line each
        ("tubelegs", [(155, 926), (197, 926), (197, 1046), (160, 1046)], 1),
        ("tubelegs", [(200, 926), (243, 926), (243, 1046), (205, 1046)], 1),
        # her feet were left open (the leg outlines formed their sides) -> closed ovals
        ("erase", [(139, 1045), (195, 1045), (195, 1087), (139, 1087)]),
        ("erase", [(197, 1045), (246, 1045), (246, 1083), (197, 1083)]),
        ("line", [(180, 1044), (178, 1058)]),
        ("line", [(229, 1044), (225, 1056)]),
        ("oval", (167, 1068, 24, 13)),
        ("oval", (222, 1065, 22, 13)),
    ],
    13: [
        # man single-line. The woman is the same drawing as p7 (identical runs) -> same fixes
        ("erase", [(516, 753), (533, 753), (533, 801), (517, 801), (515, 790)]),
        ("line", [(511, 746), (500, 790), (494, 828)]),
        ("oval", (491, 846, 10, 19)),
        ("tubelegs", [(530, 922), (571, 922), (571, 1040), (526, 1040)], 1),
        ("tubelegs", [(577, 922), (616, 922), (616, 998), (605, 1004), (605, 1046), (584, 1046)], 1),
    ],
    15: [
        # man, crouching behind the bush. Viewer-left arm drawn as a long closed loop (two-sided):
        # drop the outer side, keep the inner line as the arm passing behind the tree trunk
        ("erase", [(270, 826), (285, 826), (285, 846), (270, 846)]),
        ("erase", [(238, 852), (262, 852), (262, 914), (238, 914)]),
        ("erase", [(246, 906), (262, 906), (262, 924), (246, 924)]),
        ("line", [(300, 812), (270, 856), (250, 893)]),                 # the arm, one line, away from him
        ("oval", (246, 905, 9, 14)),
        # viewer-right shoulder: small loop between the garment edge and the arm
        ("erase", [(399, 829), (409, 829), (409, 867), (399, 867)]),
        # shin drawn two-sided below the knee: drop the inner side (knee -> foot is the outer line)
        ("erase", [(396, 962), (445, 962), (445, 971), (474, 971), (474, 1069), (398, 1069)]),
        ("line", [(459, 966), (446, 1020), (433, 1073)]),               # shin: knee -> foot, one line
        # woman behind the tree, viewer-left: sliver arm (closed lens, no hand) -> arm + oval hand
        ("erase", [(571, 716), (583, 716), (583, 754), (571, 754)]),
        ("line", [(582, 716), (572, 748), (566, 772)]),
        ("oval", (564, 788, 9, 15)),
        # woman behind the tree: front leg two-sided -> one line (the other leg is already one line)
        ("tubelegs", [(606, 866), (637, 866), (637, 896), (629, 920), (629, 952), (626, 960), (626, 974), (606, 974)], 1),
    ],
    17: [
        # man single-line (pointing arm allowed by the scene). Woman = the p7 drawing again:
        ("erase", [(516, 753), (533, 753), (533, 801), (517, 801), (515, 790)]),
        ("line", [(511, 746), (500, 790), (494, 828)]),
        ("oval", (491, 846, 10, 19)),
        ("tubelegs", [(530, 921), (571, 921), (571, 1036), (526, 1036)], 1),
        ("tubelegs", [(577, 921), (616, 921), (616, 998), (605, 1004), (605, 1046), (584, 1046)], 1),
    ],
    23: [
        # man, viewer-left: arm drawn two-sided (outer line + garment edge, hand between them)
        ("erase", [(147, 604), (194, 604), (190, 620), (185, 650), (180, 680), (176, 710), (172, 740),
                   (171, 770), (166, 795), (147, 795)]),
        ("line", [(147, 663), (171, 675)]),                          # ground line restored behind him
        ("line", [(196, 590), (178, 680), (163, 752)]),               # arm, one line
        ("oval", (160, 770, 10, 18)),
        # woman, viewer-right: arm missing (only a closed sliver at the shoulder) -> arm + oval hand
        ("erase", [(753, 668), (764, 668), (764, 724), (753, 724)]),
        ("line", [(754, 676), (768, 740), (777, 790)]),
        ("oval", (779, 807, 9, 17)),
        # woman: tube legs -> one line each
        ("erase", [(629, 1003), (682, 1003), (682, 1036), (629, 1036)]),                   # open feet
        ("erase", [(698, 993), (748, 993), (748, 1027), (698, 1027)]),
        ("tubelegs", [(652, 872), (690, 872), (690, 1010), (652, 1010)], 1, (20, 11)),
        ("tubelegs", [(700, 872), (746, 872), (746, 992), (700, 992)], 1, (20, 11)),
    ],
    25: [
        # Father (sleeveless top, knee shorts — shorts as a shape is allowed; his shins are single
        # lines, the two-sided U between them is a chair leg). Viewer-right shoulder: an oval
        # "shoulder" with the arm starting inside it -> clean arm from the armhole
        ("erase", [(758, 627), (791, 627), (791, 645), (801, 645), (801, 706), (791, 712), (791, 716), (758, 716)]),
        ("line", [(776, 628), (786, 672), (791, 716)]),
        # cup arm ends at the handle with no hand -> mitten gripping the handle (one thumb bump)
        ("oval", (566, 751, 7, 7)),
        ("oval", (578, 765, 15, 12)),
    ],
    29: [
        # all limbs single lines. The man's viewer-left hand has a curl inside it -> plain oval
        ("erase", [(78, 652), (113, 652), (113, 702), (78, 702)]),
        ("line", [(95, 646), (95, 656)]),
        ("oval", (95, 676, 13, 21)),
    ],
    31: [
        # arms are single lines with oval hands. Every leg two-sided, ending in a rounded tube end
        # instead of a foot -> one line per leg + plain oval feet. Zone tops sit 1 px under the
        # (uneven) hems, measured per column.
        ("erase", [(325, 1041), (373, 1041), (373, 1077), (325, 1077)]),                  # old feet
        ("erase", [(376, 1029), (426, 1029), (426, 1064), (376, 1064)]),
        ("erase", [(529, 1037), (573, 1037), (573, 1077), (529, 1077)]),
        ("erase", [(577, 1031), (618, 1031), (618, 1060), (577, 1060)]),
        ("tubelegs", [(322, 894), (345, 890), (370, 894), (370, 1040), (322, 1040)], 1, (20, 11)),   # man
        ("tubelegs", [(377, 885), (420, 885), (420, 1028), (377, 1028)], 1, (20, 11)),
        ("tubelegs", [(533, 913), (550, 916), (560, 922), (571, 927), (571, 1036), (533, 1036)], 1, (20, 11)),
        ("tubelegs", [(580, 936), (595, 935), (607, 937), (617, 942), (617, 1030), (580, 1030)], 1, (18, 10)),
    ],
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
    lines = []                                   # a polyline per leg (knees allowed), 12-row steps
    for c in cen:
        c = np.array(c); pts = []
        for y in range(int(c[0, 0]), int(c[-1, 0]) + 1, 12):
            sel = c[np.abs(c[:, 0] - y) <= 6]
            if len(sel): pts.append((float(np.median(sel[:, 1])), float(y)))
        pts.append((float(np.median(c[-4:, 1])), float(c[-1, 0])))
        lines.append(pts)
    return ys.min(), ys.max(), lines


def apply(page):
    import numpy as np
    src = Image.open(f"art/pre-limbfix/p{page}.png").convert("L")
    ink = np.asarray(src) < 128
    big = src.resize((src.width * SS, src.height * SS), Image.NEAREST)
    d = ImageDraw.Draw(big)
    S = lambda pts: [(x * SS, y * SS) for x, y in pts]
    for item in OPS[page]:
        op, arg = item[0], (item[1:] if len(item) > 2 else item[1])
        if op == "erase":
            d.polygon(S(arg), fill=255)
        elif op == "line":
            pts = S(arg); r = W * SS / 2
            d.line(pts, fill=0, width=W * SS, joint="curve")
            for x, y in (pts[0], pts[-1]):
                d.ellipse([x - r, y - r, x + r, y + r], fill=0)
        elif op == "tubelegs":
            poly, n = arg[0], arg[1]; foot = arg[2] if len(arg) > 2 else None
            y0, y1, legs = tube_centres(ink, poly, n)
            d.polygon(S(poly), fill=255); r = W * SS / 2
            for pts in legs:
                (xa, ya), (xb, yb) = pts[0], pts[1]
                (xc, yc), (xd, yd) = pts[-2], pts[-1]
                top = (xa - (xb - xa) * 4 / max(yb - ya, 1), ya - 4)       # run on into the hem
                bot = (xd + (xd - xc) * 4 / max(yd - yc, 1), yd + 4)       # and into the foot
                P = S([top] + pts + [bot])
                d.line(P, fill=0, width=W * SS, joint="curve")
                for x, y in (P[0], P[-1]): d.ellipse([x - r, y - r, x + r, y + r], fill=0)
                if foot:                                   # a plain oval foot centred under the leg end
                    fx, fy = P[-1]; rx, ry = foot[0] * SS, foot[1] * SS; fy += ry - 2 * SS
                    d.ellipse([fx - rx, fy - ry, fx + rx, fy + ry], fill=255, outline=0, width=W * SS)
        elif op == "oval":
            cx, cy, rx, ry = (v * SS for v in arg)
            d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255, outline=0, width=W * SS)
    out = big.resize(src.size, Image.LANCZOS).point(lambda v: 255 if v >= 128 else 0)
    # leftovers of erased strokes: tiny ink islands inside the edited areas only
    from scipy import ndimage
    o = np.asarray(out) < 128; touched = np.zeros_like(o)
    for item in OPS[page]:
        pts = item[1] if item[0] in ("erase", "line") else (item[1] if item[0] == "tubelegs" else None)
        if item[0] == "oval":
            cx, cy, rx, ry = item[1]; pts = [(cx - rx, cy - ry), (cx + rx, cy + ry)]
        xs, ys = zip(*pts)
        touched[max(min(ys) - 8, 0):max(ys) + 8, max(min(xs) - 8, 0):max(xs) + 8] = True
    lab, n = ndimage.label(o)
    sizes = ndimage.sum(o, lab, range(1, n + 1))
    small = np.isin(lab, np.where(sizes < 30)[0] + 1) & touched
    o[small] = False
    out = Image.fromarray(np.where(o, 0, 255).astype(np.uint8)).convert("1")
    out.save(f"art/p{page}.png")
    print(f"p{page}: {len(OPS[page])} ops")


if __name__ == "__main__":
    for p in (map(int, sys.argv[1:]) if len(sys.argv) > 1 else sorted(OPS)):
        apply(p)

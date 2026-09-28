#!/usr/bin/env python3
"""Series badge — numbered sprout-and-roots motif echoing the tree-and-roots mark.

Vector: scales to any size, repeatable across volumes via `volume`.
Primary Palette only. mono=True for black-ink interiors.
"""
from reportlab.lib.colors import HexColor
GOLD  = HexColor("#D9A441"); NAVY = HexColor("#2E4257")
GREEN = HexColor("#4C7A5A"); CREAM = HexColor("#F7EEDD")

def _leaf(c, cx, cy, r, sgn):
    """One teardrop leaf springing from the stem, angled outward."""
    p = c.beginPath()
    p.moveTo(cx + sgn*r*0.04, cy)
    p.curveTo(cx + sgn*r*0.10, cy + r*0.34,
              cx + sgn*r*0.42, cy + r*0.34,
              cx + sgn*r*0.46, cy + r*0.06)
    p.curveTo(cx + sgn*r*0.34, cy + r*0.02,
              cx + sgn*r*0.16, cy - r*0.06,
              cx + sgn*r*0.04, cy)
    c.drawPath(p, stroke=0, fill=1)

def draw_badge(c, cx, cy, d, volume=1, mono=False):
    r = d / 2.0
    ring  = NAVY if mono else GOLD
    leafc = NAVY if mono else GREEN
    c.saveState()

    c.setLineWidth(max(0.9, d*0.045)); c.setStrokeColor(ring)
    c.setFillColor(HexColor("#FFFFFF") if mono else CREAM)
    c.circle(cx, cy, r, stroke=1, fill=1)

    # sprout above the numeral: short stem, two clearly separate leaves
    c.setFillColor(leafc); c.setStrokeColor(leafc)
    c.setLineWidth(max(0.6, d*0.025))
    c.line(cx, cy + r*0.30, cx, cy + r*0.62)
    _leaf(c, cx, cy + r*0.46, r, -1)
    _leaf(c, cx, cy + r*0.46, r, +1)

    # numeral — the dominant element, with clear air around it
    c.setFillColor(NAVY); c.setFont("Baloo2", d*0.40)
    c.drawCentredString(cx, cy - r*0.22, str(volume))

    # roots: three short diverging strokes under the numeral
    c.setStrokeColor(leafc); c.setLineWidth(max(0.5, d*0.020))
    for sgn in (-1, 0, 1):
        p = c.beginPath(); p.moveTo(cx, cy - r*0.42)
        if sgn == 0:
            p.lineTo(cx, cy - r*0.70)
        else:
            p.curveTo(cx, cy - r*0.54, cx + sgn*r*0.20, cy - r*0.56,
                      cx + sgn*r*0.30, cy - r*0.68)
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

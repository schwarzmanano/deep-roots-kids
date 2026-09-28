#!/usr/bin/env python3
"""Stage 6b — bitonal PNG -> SVG via potrace curve fitting.

Vector is what makes this printable: the raster is ~109 DPI at 8.5x11, well
under KDP's 300 DPI floor. That floor applies to raster images; vector art is
resolution-independent and prints sharp at any size.
"""
import sys, glob, os
import numpy as np
from PIL import Image
import potrace

def trace(src, dst):
    im = Image.open(src).convert("L")
    W, H = im.size
    # potracer's Bitmap takes the INVERSE of what you'd expect: passing the ink
    # mask traces the background and yields a 95%-black page. Verified empirically
    # against source ink coverage (4.80% source -> 4.76% rendered with this).
    data = np.array(im) >= 128
    bmp = potrace.Bitmap(data)
    path = bmp.trace(turdsize=2, alphamax=1.0, opticurve=True, opttolerance=0.2)

    parts, curves = [], 0
    for curve in path:
        st = curve.start_point
        d = [f"M{st.x:.2f},{st.y:.2f}"]
        for seg in curve:
            curves += 1
            e = seg.end_point
            if seg.is_corner:
                c = seg.c
                d.append(f"L{c.x:.2f},{c.y:.2f}L{e.x:.2f},{e.y:.2f}")
            else:
                a, b = seg.c1, seg.c2
                d.append(f"C{a.x:.2f},{a.y:.2f} {b.x:.2f},{b.y:.2f} {e.x:.2f},{e.y:.2f}")
        d.append("Z")
        parts.append("".join(d))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">'
           f'<path d="{"".join(parts)}" fill="#000" fill-rule="evenodd"/></svg>')
    open(dst, "w").write(svg)
    return len(parts), curves, os.path.getsize(dst)

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from bookarg import book_dir
    BOOK = book_dir()
    tot = 0
    for src in sorted(glob.glob(f"{BOOK}/art/p*.png"),
                      key=lambda p: int(p.split("/p")[-1].split(".")[0])):
        pg = src.split("/p")[-1].split(".")[0]
        dst = f"{BOOK}/art/p{pg}.svg"
        n, c, size = trace(src, dst)
        tot += size
        print(f"  p{pg:>2}  {n:>4} paths  {c:>5} segments  {size/1024:>6.1f} KB")
    print(f"\n  total SVG: {tot/1024:.0f} KB")

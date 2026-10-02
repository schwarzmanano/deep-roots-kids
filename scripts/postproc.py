#!/usr/bin/env python3
"""Stage 6a — frame strip + threshold. Produces bitonal PNG ready for potrace.

The API returns JPEG (256 grey levels, ~3% midtone ringing) and the model draws
a border frame it was told not to. Both are handled here, deterministically.
"""
import sys, os
from PIL import Image
import numpy as np

THRESH = 128
EDGE_ZONE = 0.10      # how far in to look for frame lines
FRAME_RATIO = 0.80    # a row/col this black across its length is a frame line
TARGET_ASPECT = 8.5 / 11.0


def load_bitonal(path):
    im = Image.open(path).convert("L")
    return im.point(lambda p: 0 if p < THRESH else 255, mode="L")


def find_frame_crop(bw):
    W, H = bw.size
    px = bw.load()
    col_black = lambda x: sum(1 for y in range(H) if px[x, y] == 0) / H
    row_black = lambda y: sum(1 for x in range(W) if px[x, y] == 0) / W

    left = right = top = bottom = None
    for x in range(int(W * EDGE_ZONE)):
        if col_black(x) > FRAME_RATIO: left = x
    for x in range(W - 1, int(W * (1 - EDGE_ZONE)), -1):
        if col_black(x) > FRAME_RATIO: right = x
    for y in range(int(H * EDGE_ZONE)):
        if row_black(y) > FRAME_RATIO: top = y
    for y in range(H - 1, int(H * (1 - EDGE_ZONE)), -1):
        if row_black(y) > FRAME_RATIO: bottom = y

    found = any(v is not None for v in (left, right, top, bottom))
    # crop just inside the innermost frame line on each edge
    return found, (
        (left + 1) if left is not None else 0,
        (top + 1) if top is not None else 0,
        right if right is not None else W,
        bottom if bottom is not None else H,
    )


def pad_to_aspect(bw, aspect=TARGET_ASPECT):
    W, H = bw.size
    if W / H > aspect:          # too wide -> pad height
        newH = round(W / aspect); newW = W
    else:                        # too tall -> pad width
        newW = round(H * aspect); newH = H
    canvas = Image.new("L", (newW, newH), 255)
    canvas.paste(bw, ((newW - W) // 2, (newH - H) // 2))
    return canvas


def thicken_thin(bw, px_to_pt, floor_pt):
    """Dilate ONLY the components that fall under the point floor.

    Dilating the whole page would thicken every stroke and change the page's
    character; this touches just the offending components.
    """
    from scipy import ndimage
    ink = np.array(bw) < 128
    D = ndimage.distance_transform_edt(ink)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    if n == 0:
        return bw, 0
    peaks = ndimage.maximum(D, lab, range(1, n + 1))
    areas = ndimage.sum(ink, lab, range(1, n + 1))
    need = [i + 1 for i, (pk, a) in enumerate(zip(peaks, areas))
            if a >= 40 and (2.0 * pk) * px_to_pt < floor_pt]
    if not need:
        return bw, 0
    thin = np.isin(lab, need)
    target_px = floor_pt / px_to_pt
    iters = max(1, int(np.ceil((target_px - 2.0 * min(peaks[i - 1] for i in need)) / 2.0)))
    grown = ndimage.binary_dilation(thin, np.ones((3, 3)), iterations=iters)
    out = ink | grown
    return Image.fromarray(np.where(out, 0, 255).astype(np.uint8), "L"), len(need)


def strip_edge_slivers(bw, zone=0.02, max_thick=4):
    """Remove frame-line remnants: straight components no thicker than `max_thick` px, lying
    entirely within `zone` of one image edge and running along it. find_frame_crop misses a
    frame line that is broken (under FRAME_RATIO black); its segments survive as edge slivers
    (we-broke-it-all p19, 2026-10-02). Real art is never a 4px-straight line hugging the edge."""
    from scipy import ndimage
    ink = np.array(bw) < 128
    H, W = ink.shape
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    removed = 0
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        vert = (x1 - x0) <= max_thick and (x1 <= W * zone or x0 >= W * (1 - zone))
        horz = (y1 - y0) <= max_thick and (y1 <= H * zone or y0 >= H * (1 - zone))
        if vert or horz:
            ink[lab == i] = False
            removed += 1
    if not removed:
        return bw, 0
    return Image.fromarray(np.where(ink, 0, 255).astype(np.uint8), "L"), removed


def process(src, dst, px_to_pt=None, floor_pt=None):
    bw = load_bitonal(src)
    framed, box = find_frame_crop(bw)
    if framed:
        bw = bw.crop(box)
    bw, slivers = strip_edge_slivers(bw)
    thickened = 0
    if px_to_pt and floor_pt:
        bw, thickened = thicken_thin(bw, px_to_pt, floor_pt)
    bw = pad_to_aspect(bw)
    bw.convert("1").save(dst)

    h = bw.histogram(); t = sum(h)
    return {
        "frame_removed": framed,
        "edge_slivers_removed": slivers,
        "thickened": thickened,
        "ink_pct": h[0] / t * 100,
        "midtone_pct": sum(h[1:255]) / t * 100,
        "size": bw.size,
    }


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    r = process(src, dst)
    print(f"  {os.path.basename(src)} -> {os.path.basename(dst)}  "
          f"frame_removed={r['frame_removed']}  ink={r['ink_pct']:.2f}%  "
          f"midtone={r['midtone_pct']:.2f}%  {r['size'][0]}x{r['size'][1]}")

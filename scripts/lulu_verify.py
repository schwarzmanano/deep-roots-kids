#!/usr/bin/env python3
"""Verify a print PDF against Lulu's checks.

Ghostscript and poppler are not installed on this machine, so the usual
`gs -sDEVICE=inkcov` / `pdfimages -list` / `pdffonts` / `pdfinfo -box` commands
cannot run. These checks read the same properties straight out of the PDF
objects instead, which answers the same questions:

  inkcov C=M=Y=0   -> no DeviceRGB/CMYK/ICC colour operators and no non-gray
                      image colourspaces anywhere, so no non-K ink can be laid down
  pdfimages -list  -> per-image dimensions, colourspace, SMask and effective ppi
  pdffonts         -> per-font embedding flag
  pdfinfo -box     -> MediaBox per page
"""
import re
import pymupdf

RGB_OPS = [
    (r'[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+rg\b', 'rg'),
    (r'[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+RG\b', 'RG'),
    (r'[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+k\b', 'k'),
    (r'[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+K\b', 'K'),
    (r'/\w+\s+cs\b', 'cs'),
    (r'/\w+\s+CS\b', 'CS'),
    (r'[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+sc\b', 'sc(3)'),
    (r'[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+SC\b', 'SC(3)'),
]


def verify(path, expect_pages=None, expect_size=None, gray_required=False, label=""):
    d = pymupdf.open(path)
    fails = []
    print(f"\n===== {label or path} =====")

    with open(path, "rb") as fh:
        print(f"  header        : {fh.read(9).decode('latin-1', 'ignore')}")
    print(f"  pages         : {d.page_count}")
    if expect_pages and d.page_count != expect_pages:
        fails.append(f"page count {d.page_count} != {expect_pages}")

    sizes = {(round(p.rect.width, 3), round(p.rect.height, 3)) for p in d}
    print(f"  page size (pt): {sizes}")
    print(f"  page size (in): {[(round(w/72, 4), round(h/72, 4)) for w, h in sizes]}")
    if expect_size:
        for w, h in sizes:
            if abs(w - expect_size[0]) > 0.05 or abs(h - expect_size[1]) > 0.05:
                fails.append(f"page size {w}x{h}pt != {expect_size}")

    fonts, unemb = set(), set()
    for p in d:
        for f in p.get_fonts(full=True):
            fonts.add(f[3])
            if str(f[1]).strip().lower() in ("n/a", "", "none", "0"):
                unemb.add(f[3])
    print(f"  fonts         : {sorted(fonts)}")
    print(f"  embedded      : {'ALL' if not unemb else 'MISSING ' + str(sorted(unemb))}")
    if unemb:
        fails.append(f"unembedded fonts {sorted(unemb)}")

    print("  images        :")
    found_any = False
    for i, p in enumerate(d, 1):
        for im in p.get_images(full=True):
            found_any = True
            xref, w, h = im[0], im[2], im[3]
            cs = d.xref_get_key(xref, "ColorSpace")[1]
            sm = d.xref_get_key(xref, "SMask")[1]
            for r in p.get_image_rects(xref):
                px, py = w / (r.width / 72), h / (r.height / 72)
                ok = 200 <= min(px, py) and max(px, py) <= 600
                print(f"    p{i} xref{xref} {w}x{h} cs={cs} smask={sm} "
                      f"{px:.0f}x{py:.0f} ppi  {'OK' if ok else 'OUT OF BAND'}")
                if not ok:
                    fails.append(f"p{i} image {px:.0f}x{py:.0f} ppi outside 200-600")
            if sm not in ("null", None, ""):
                fails.append(f"p{i} image retains SMask ({sm})")
            if gray_required and "Gray" not in str(cs):
                fails.append(f"p{i} image colourspace {cs} is not DeviceGray")
    if not found_any:
        print("    (none)")

    bad = {}
    for i, p in enumerate(d, 1):
        s = b"".join(d.xref_stream(x) for x in p.get_contents()).decode("latin-1", "ignore")
        hits = sorted({name for pat, name in RGB_OPS if re.search(pat, s)})
        if hits:
            bad[i] = hits
    if gray_required:
        print(f"  colour ops    : {bad or 'DeviceGray only on all pages -> C=M=Y=0 by construction'}")
        if bad:
            fails.append(f"non-gray colour operators on pages {sorted(bad)}")

    trans = []
    for x in range(1, d.xref_length()):
        try:
            t = d.xref_object(x, compressed=True)
        except Exception:
            continue
        if "/SMask" in t and "/SMask null" not in t:
            trans.append((x, "SMask"))
        if re.search(r'/ca\s+0?\.\d', t) or re.search(r'/CA\s+0?\.\d', t):
            trans.append((x, "alpha"))
    print(f"  transparency  : {trans or 'none'}")
    if trans:
        fails.append(f"transparency objects remain: {trans}")

    print(f"\n  {'PASS' if not fails else str(len(fails)) + ' ISSUE(S)'}")
    for f in fails:
        print(f"     - {f}")
    return fails

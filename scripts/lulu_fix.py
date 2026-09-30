#!/usr/bin/env python3
"""Lulu print-fix pass: DeviceGray conversion, image resampling, SMask flattening.

Operates on an already-approved PDF rather than regenerating, so the editor's
wording is preserved byte-for-byte. Artwork placement is untouched: only colour
operators and image sample data change.
"""
import re, sys, zlib, io
import pymupdf
from PIL import Image

NUM = r'([-\d.]+)'
def _gray(a, b, c):
    # Rec.709 luma; achromatic inputs collapse to themselves.
    return a if (abs(a-b) < 1e-9 and abs(b-c) < 1e-9) else 0.2126*a + 0.7152*b + 0.0722*c

def to_devicegray(doc):
    """Rewrite every colour operator to DeviceGray (g/G). Returns ops changed."""
    changed = 0
    for pg in doc:
        for xref in pg.get_contents():
            s = doc.xref_stream(xref).decode("latin-1")
            orig = s
            def three(m, op):
                v = _gray(*(float(m.group(i)) for i in (1, 2, 3)))
                return f"{v:.4f} {op}"
            s = re.sub(rf'{NUM}\s+{NUM}\s+{NUM}\s+sc\b', lambda m: three(m, "g"), s)
            s = re.sub(rf'{NUM}\s+{NUM}\s+{NUM}\s+SC\b', lambda m: three(m, "G"), s)
            s = re.sub(rf'{NUM}\s+{NUM}\s+{NUM}\s+rg\b', lambda m: three(m, "g"), s)
            s = re.sub(rf'{NUM}\s+{NUM}\s+{NUM}\s+RG\b', lambda m: three(m, "G"), s)
            s = re.sub(rf'{NUM}\s+{NUM}\s+{NUM}\s+{NUM}\s+k\b', lambda m: f"{1-float(m.group(4)):.4f} g", s)
            s = re.sub(rf'{NUM}\s+{NUM}\s+{NUM}\s+{NUM}\s+K\b', lambda m: f"{1-float(m.group(4)):.4f} G", s)
            # single-operand sc/SC under a 1-channel space -> plain gray
            s = re.sub(rf'{NUM}\s+sc\b', lambda m: f"{m.group(1)} g", s)
            s = re.sub(rf'{NUM}\s+SC\b', lambda m: f"{m.group(1)} G", s)
            # the now-redundant colourspace selectors
            s = re.sub(r'/\w+\s+cs\b', '', s)
            s = re.sub(r'/\w+\s+CS\b', '', s)
            if s != orig:
                doc.update_stream(xref, s.encode("latin-1"))
                changed += 1
    return changed

def flatten_image(doc, xref, target_px, gray, bg=(255, 255, 255), jpeg=False, quality=92):
    """Composite the SMask onto `bg`, resample, and rewrite as a plain image."""
    info = doc.extract_image(xref)
    im = Image.open(io.BytesIO(info["image"])).convert("RGB")
    smask = doc.xref_get_key(xref, "SMask")
    if smask and smask[0] == "xref":
        sx = int(smask[1].split()[0])
        a = Image.open(io.BytesIO(doc.extract_image(sx)["image"])).convert("L")
        if a.size != im.size:
            a = a.resize(im.size, Image.LANCZOS)
        flat = Image.new("RGB", im.size, bg)
        flat.paste(im, (0, 0), a)
        im = flat
    w = target_px
    im = im.resize((w, max(1, round(w * im.height / im.width))), Image.LANCZOS)
    im = im.convert("L") if gray else im
    if jpeg:
        # Photographic content: DCTDecode keeps the file sane. Flate on a
        # 2587x3374 RGB plate is ~8MB; JPEG at q92 is a fraction of that.
        buf = io.BytesIO(); im.save(buf, format="JPEG", quality=quality, subsampling=0)
        doc.update_stream(xref, buf.getvalue(), new=True, compress=False)
    else:
        doc.update_stream(xref, zlib.compress(im.tobytes()), new=True)
    doc.xref_set_key(xref, "Width", str(im.width))
    doc.xref_set_key(xref, "Height", str(im.height))
    doc.xref_set_key(xref, "ColorSpace", "/DeviceGray" if gray else "/DeviceRGB")
    doc.xref_set_key(xref, "BitsPerComponent", "8")
    doc.xref_set_key(xref, "Filter", "/DCTDecode" if jpeg else "/FlateDecode")
    doc.xref_set_key(xref, "SMask", "null")
    doc.xref_set_key(xref, "DecodeParms", "null")
    doc.xref_set_key(xref, "Decode", "null")
    return im.size

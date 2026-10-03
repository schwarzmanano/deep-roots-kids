"""Series cover grid loader — kids/_brand/cover-grid.md (editor ruling 2026-10-03).

The grid geometry lives in ONE fenced ```yaml block in that file; cover.py, preflight-cover.py
and print_table.py read it from here so all eleven books share one formula. A book opts in
with `cover.layout: grid` and supplies `cover.signature_colour` in its book.yaml.
"""
import os, re, yaml

GRID_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_brand", "cover-grid.md")


def load():
    md = open(GRID_MD, encoding="utf-8").read()
    m = re.search(r"```yaml\n(.*?)```", md, re.S)
    if not m:
        raise SystemExit(f"{GRID_MD}: no ```yaml geometry block")
    return yaml.safe_load(m.group(1))


def barcode_box(target, back_l, trim_w, bleed, IN=72.0):
    """(x0, y0, x1, y1) in points, PDF y-up, of the clear barcode box on the back panel."""
    b = load()["barcode"][target]
    x1 = back_l + trim_w - b["inset_in"] * IN
    x0 = x1 - b["width_in"] * IN
    y0 = bleed + b["inset_in"] * IN
    return x0, y0, x1, y0 + b["height_in"] * IN

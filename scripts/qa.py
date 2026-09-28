#!/usr/bin/env python3
"""Stage 5+6a — post-process every chosen page and report QA."""
import os, sys, glob, json, statistics
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from postproc import process
from strokes import summarise as stroke_summary
from PIL import Image

from bookarg import book_dir
book = book_dir()
import yaml
_plan = yaml.safe_load(open(f"{book}/plan/pages.yaml"))
SPARSE = {p["page"] for p in _plan["pages"] if p.get("density") == "sparse"}
_cfg = yaml.safe_load(open(f"{book}/book.yaml"))
_M = _cfg["margins"]; _IN = 72.0
_PW, _PH = 8.5*_IN, 11*_IN
_CW = _PW - _M["gutter_in"]*_IN - _M["outside_in"]*_IN
_AH = _PH - _M["top_in"]*_IN - (_M["bottom_in"]*_IN + 46)   # nominal caption band
STROKE_FLOOR_PT = 2.0
rows = []
REF_INK = None

for d in sorted(glob.glob(f"{book}/gen/p*/"), key=lambda p: int(p.rstrip('/').split('/p')[-1])):
    page = int(d.rstrip('/').split('/p')[-1])
    chosen = os.path.join(d, "CHOSEN")
    if not os.path.exists(chosen):
        continue
    src = os.path.realpath(chosen)
    dst = f"{book}/art/p{page}.png"
    _pg = next((x for x in _plan["pages"] if x["page"] == page), {})
    _im = Image.open(src); _s0 = min(_CW/_im.size[0], _AH/_im.size[1])
    r = (process(src, dst, _s0, STROKE_FLOOR_PT) if _pg.get("thicken_thin_strokes")
         else process(src, dst))

    bw = Image.open(dst).convert("L"); W, H = bw.size; px = bw.load()
    # safe area: min distance of any black pixel to the edge, as % of dimension
    # Ink density in the outer 7.5% band. Scenery grazing the edge is fine and
    # expected; a SUBJECT clipped by the edge shows up as a dense outer band.
    band = int(min(W, H) * 0.075)
    outer = inner = 0
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if px[x, y] == 0:
                if x < band or x >= W-band or y < band or y >= H-band: outer += 1
                else: inner += 1
    margin = outer / max(outer+inner, 1) * 100   # % of ink sitting in the edge band
    runs = []
    for y in range(0, H, 6):
        n = 0
        for x in range(W):
            if px[x, y] == 0: n += 1
            elif n: runs.append(n); n = 0
    stroke = statistics.median(runs) if runs else 0

    ink_mask = np.array(bw) < 128
    _s = min(_CW/W, _AH/H)
    sw = stroke_summary(ink_mask, _s, STROKE_FLOOR_PT) or dict(min_pt=0, thin_count=0, thin_ink_pct=0)

    rows.append(dict(page=page, ink=r["ink_pct"], stroke=stroke, margin=margin,
                     min_pt=sw["min_pt"], thin_count=sw["thin_count"], thin_ink_pct=sw["thin_ink_pct"],
                     frame=r["frame_removed"], midtone=r["midtone_pct"], src=os.path.basename(src)))

_ref_pg = next(p["page"] for p in _plan["pages"] if p.get("style_reference"))
ref = next(r for r in rows if r["page"] == _ref_pg)["ink"]
print(f"\n  reference ink = {ref:.2f}%   (drift flagged beyond ±50%)\n")
print(f"  stroke floor = {STROKE_FLOOR_PT:.1f}pt at final trim\n")
print(f"  {'pg':>3} {'ink%':>6} {'drift':>7} {'minPt':>6} {'edge-ink%':>10} {'frame':>6} {'midtone':>8}  flags")
print("  " + "-"*76)
flagged = []
for r in rows:
    drift = (r["ink"]/ref - 1)*100
    f = []
    _pp = next((x for x in _plan["pages"] if x["page"] == r["page"]), {})
    if abs(drift) > 50 and r["page"] not in SPARSE and not _pp.get("accept_ink_drift"):
        f.append("INK-DRIFT")
    if r["margin"] > 22: f.append("EDGE-HEAVY")
    if r["midtone"] > 0.01: f.append("MIDTONE")
    _p = next((x for x in _plan["pages"] if x["page"] == r["page"]), {})
    if r["thin_count"] and not _p.get("accept_thin_strokes"):
        f.append(f"THIN-STROKE({r['thin_count']})")
    if f: flagged.append((r["page"], f))
    print(f"  {r['page']:>3} {r['ink']:>6.2f} {drift:>+6.0f}% {r['min_pt']:>6.2f} "
          f"{r['margin']:>10.1f} {str(r['frame']):>6} {r['midtone']:>8.2f}  {' '.join(f)}")
print()
print(f"  {len(rows)} pages processed, {len(flagged)} flagged")
json.dump(rows, open(f"{book}/qa/report.json","w"), indent=2)

#!/usr/bin/env python3
"""Stroke-width measurement for line art, in points at final trim size.

Run-length along rows/columns overstates width on diagonals; naive ridge
detection undercounts, because stroke ENDPOINTS and corners are legitimately
1px and would flag every page. This uses an exact Euclidean distance transform
and measures each connected stroke component at its thickest point, which is
that component's actual stroke width.
"""
import numpy as np
from scipy import ndimage

MIN_COMPONENT_PX = 40      # ignore specks and tracing noise

def component_widths(ink):
    """[(width_px, area_px)] — one entry per connected ink component."""
    D = ndimage.distance_transform_edt(ink)
    lab, n = ndimage.label(ink, structure=np.ones((3, 3)))
    if n == 0:
        return []
    areas = ndimage.sum(ink, lab, range(1, n + 1))
    peaks = ndimage.maximum(D, lab, range(1, n + 1))
    return [(2.0 * p, a) for p, a in zip(peaks, areas) if a >= MIN_COMPONENT_PX]

def summarise(ink, px_to_pt, floor_pt=2.0):
    cw = component_widths(ink)
    if not cw:
        return None
    widths = np.array([w for w, _ in cw]) * px_to_pt
    areas = np.array([a for _, a in cw])
    thin = widths < floor_pt
    return dict(
        components=len(cw),
        min_pt=float(widths.min()),
        median_pt=float(np.median(widths)),
        max_pt=float(widths.max()),
        thin_count=int(thin.sum()),
        thin_ink_pct=float(areas[thin].sum() / areas.sum() * 100) if thin.any() else 0.0,
        px_to_pt=px_to_pt,
    )

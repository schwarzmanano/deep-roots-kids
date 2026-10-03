#!/usr/bin/env python3
"""Front-art retouch, Book Three cover (editor ruling 2026-10-03, option B).

Input : front-art-v5-01-shoulders.png — v5-01 with the two armhole skin wedges painted out
        (Son: smooth fabric fill; Daughter 3: row-wise fill + seam-spur fix), done in session.
Output: front-art-v5-01-retouched.png — scaled by S, placed bottom-anchored on a canvas with
        the front panel's exact aspect (8.625 x 11.25 in incl. right bleed), extended with:
          * top + side sky: low-pass of the painting's own sky (sky-coloured pixels only),
            vertical gradient eased upward, plus monochrome grain matched to its fine texture;
          * lower sides: zigzag reflection of character-free edge strips (no dog tail, no hand).
        No grass extension (bottom-anchored). Deterministic (fixed seeds).
Usage : python retouch_extend.py [scale]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage
S = float(sys.argv[1]) if len(sys.argv) > 1 else 0.84
FREE_L, FREE_R = 0.053, 0.035          # character-free edge strips, as fractions of the source width
src = Image.open("front-art-v5-01-shoulders.png").convert("RGB"); W0, H0 = src.size
sw, sh = round(W0 * S), round(H0 * S); Hc = H0; Wc = round(Hc * (8.625 / 11.25)); ox = (Wc - sw) // 2; oy = Hc - sh
sc = np.asarray(src.resize((sw, sh), Image.LANCZOS)).astype(float)
L = 0.299 * sc[..., 0] + 0.587 * sc[..., 1] + 0.114 * sc[..., 2]; sat = sc.max(2) - sc.min(2)
rng = np.random.default_rng(42)
skym = ndimage.binary_erosion((L > 185) & (sat < 90), iterations=6)
num = np.stack([ndimage.gaussian_filter(sc[..., k] * skym, 60) for k in range(3)], -1)
den = ndimage.gaussian_filter(skym.astype(float), 60)[..., None]; G = num / np.maximum(den, 1e-4)
gstd = (L - ndimage.gaussian_filter(L, 3))[skym].std()
def grain(h, w):
    n = ndimage.gaussian_filter(rng.normal(0, 1, (h, w)), 1.2); return (n / n.std() * gstd)[..., None] * np.ones(3)
out = np.zeros((Hc, Wc, 3))
slope = np.polyfit(np.arange(500), G[:500].reshape(500, -1), 1)[0].reshape(sw, 3)
slope = ndimage.gaussian_filter1d(slope, 60, axis=0); cols = np.clip(np.arange(Wc) - ox, 0, sw - 1)
for yy in range(oy):
    d = oy - yy; out[yy] = G[0, cols] - slope[cols] * 260 * (1 - np.exp(-d / 260))
out[:oy] += grain(oy, Wc)
out[oy:, ox:ox + sw] = sc
def zig(K, n):                     # 0,1,..,K-1,K-1,..,0,0,1,.. — mirror at the image edge, then alternate
    seq, k, d = [], 0, 1
    while len(seq) < n:
        seq.append(k); k += d
        if k == K: k, d = K - 1, -1
        elif k < 0: k, d = 0, 1
    return np.array(seq)
for side in ("L", "R"):
    edge = slice(0, 120) if side == "L" else slice(sw - 120, sw)
    end = np.nonzero((L[:, edge] < 120).any(1))[0][0] - 40
    ec = 0 if side == "L" else sw - 1
    xs = slice(0, ox) if side == "L" else slice(ox + sw, Wc)
    w = xs.stop - xs.start                                    # sides can differ by 1 px
    out[oy:oy + end, xs] = G[:end, ec][:, None, :] + grain(end, w)
    K = round((FREE_L if side == "L" else FREE_R) * W0 * S)
    if side == "L":
        strip = sc[end:, :K]; out[oy + end:, xs] = strip[:, zig(K, w)][:, ::-1]
    else:
        strip = sc[end:, sw - K:][:, ::-1]; out[oy + end:, xs] = strip[:, zig(K, w)]
    for i in range(30):
        a = i / 30; r = oy + end + i; out[r, xs] = out[oy + end - 1, xs] * (1 - a) + out[r, xs] * a
Image.fromarray(out.clip(0, 255).astype("uint8")).save("front-art-v5-01-retouched.png")
print(f"scale {S}: art {sw}x{sh} on {Wc}x{Hc}; top extension {oy}px ({oy/Hc*100:.1f}%), sides {ox}px")

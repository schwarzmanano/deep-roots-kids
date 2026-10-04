#!/usr/bin/env python3
"""Front-art retouch, Book One cover (editor ruling 2026-10-05, option A: retouch v3-03).

Input : front-art-v3-03.jpg (gemini 4K, 3584 x 4800)
Output: front-art-v3-03-retouched.png
  1. stray floating pointing hand (sky, right of Daughter 1's head) and the one bird that
     lands on the subtitle once placed, painted out with the painting's own sky (normalised
     low-pass of the surrounding sky + matched mono grain);
  2. three armhole skin wedges painted out in garment colour (Daughter 1 green, Daughter 2
     coral: row-wise fill from the garment side, the dress-edge line kept; Son: the skin oval
     inside the shirt filled from both sides, his arm line redrawn from the shoulder seam);
  3. the Son's tangled crouch (tube shorts, crossing leg lines) redrawn as a plain front-on
     squat: flat shorts, single-line legs bent at the knee, oval feet; his resting hand kept.
No scaling needed: on the grid the heads sit below the subtitle. Deterministic (fixed seed).
"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

SRC, OUT = "front-art-v3-03.jpg", "front-art-v3-03-retouched.png"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(float)
H, W, _ = a.shape
L = a @ [0.299, 0.587, 0.114]
rng = np.random.default_rng(7)
INK = (8, 6, 3)                             # measured on the painting's own outlines
LINE = 11                                    # outline width at 4K (measured 10-12 px)


def lowpass_fill(img, mask, box, sigma):
    """Fill mask (inside box) from the unmasked pixels around it, plus matched mono grain."""
    x0, y0, x1, y1 = box
    sub = img[y0:y1, x0:x1]; m = mask[y0:y1, x0:x1]; keep = (~m).astype(float)
    num = np.stack([ndimage.gaussian_filter(sub[..., k] * keep, sigma) for k in range(3)], -1)
    den = ndimage.gaussian_filter(keep, sigma)[..., None]
    fill = num / np.maximum(den, 1e-4)
    Ls = sub @ [0.299, 0.587, 0.114]
    hpf = Ls - ndimage.gaussian_filter(Ls, 3)
    hp = hpf[~ndimage.binary_dilation(m, iterations=20) & (np.abs(hpf) < 6)]
    n = ndimage.gaussian_filter(rng.normal(0, 1, m.shape), 1.1); n = n / n.std() * hp.std()
    fill = fill + n[..., None]
    soft = ndimage.gaussian_filter(m.astype(float), 1.5)[..., None]   # feather the seam
    img[y0:y1, x0:x1] = sub * (1 - soft) + fill * soft


def near(rgb, ref, tol):
    return np.linalg.norm(rgb - np.array(ref, float), axis=-1) < tol


# ---- 1. floating hand in the sky -------------------------------------------------------
box = (1640, 1740, 1850, 2010)
x0, y0, x1, y1 = box
sat = a.max(2) - a.min(2)
m = np.zeros((H, W), bool)
m[y0 + 15:y1 - 15, x0 + 15:x1 - 15] = ((L < 215) | (sat > 45))[y0 + 15:y1 - 15, x0 + 15:x1 - 15]
m = ndimage.binary_dilation(m, iterations=8)
lowpass_fill(a, m, (x0 - 120, y0 - 120, x1 + 120, y1 + 120), 30)
# 1b. the one bird that lands on the subtitle's last letters once placed on the grid
x0, y0, x1, y1 = 2180, 1478, 2280, 1528
m = np.zeros((H, W), bool)
m[y0:y1, x0:x1] = ((L < 225) | (sat > 40))[y0:y1, x0:x1]
m = ndimage.binary_dilation(m, iterations=6)
lowpass_fill(a, m, (x0 - 120, y0 - 120, x1 + 120, y1 + 120), 30)


def conv_fill(mask, good, box, sigma):
    """Fill mask from 'good' pixels only (normalised Gaussian), keeping the cloth's shading.
    Pixels too far from any good pixel at this sigma take the next, wider pass."""
    x0, y0, x1, y1 = box
    m = mask[y0:y1, x0:x1]; g = (good & ~mask)[y0:y1, x0:x1].astype(float); sub = a[y0:y1, x0:x1]
    todo = m.copy()
    for sg in (sigma, sigma * 2, sigma * 4, sigma * 8):
        den = ndimage.gaussian_filter(g, sg)
        num = np.stack([ndimage.gaussian_filter(sub[..., k] * g, sg) for k in range(3)], -1)
        ok = todo & (den > 0.08)
        sub[ok] = (num / np.maximum(den, 1e-4)[..., None])[ok]
        todo &= ~ok
        if not todo.any(): break


# ---- 2a/2b. girls' armhole wedges -----------------------------------------------------------
def wedge(poly, garment_pt):
    """Hand-measured polygon (from 3x ruler zooms) over the skin wedge and its inner outline,
    stopping at the kept dress-edge line and below the shoulder's top outline. Refilled from
    the surrounding cloth only, so its shading carries through."""
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    mask = np.asarray(m) > 0
    garment = near(a, a[garment_pt[1], garment_pt[0]], 50) & (L > 60)
    xs, ys = zip(*poly)
    conv_fill(mask, garment, (min(xs) - 50, min(ys) - 50, max(xs) + 50, max(ys) + 50), 6)


wedge([(1306, 2205), (1316, 2205), (1325, 2230), (1328, 2265), (1324, 2300), (1312, 2319),
       (1293, 2324), (1292, 2310), (1299, 2260)], (1340, 2280))          # Daughter 1, viewer-left
wedge([(2968, 3075), (2979, 3077), (2985, 3102), (2988, 3120), (2992, 3150), (2998, 3180),
       (2999, 3192), (2992, 3192), (2984, 3187), (2975, 3179), (2966, 3166), (2960, 3150), (2959, 3130),
       (2959, 3110), (2962, 3096)], (2950, 3150))                         # Daughter 2, viewer-right
# her kept dress-edge line, redrawn crisp over the fill's edge (centre measured 2985@3084 -> 3002.5@3180)
d0 = Image.new("RGBA", (80 * 4, 140 * 4), (0, 0, 0, 0))
ImageDraw.Draw(d0).line([((2984.5 - 2950) * 4, (3078 - 3065) * 4), ((3004 - 2950) * 4, (3190 - 3065) * 4)],
                        fill=INK + (255,), width=9 * 4)
d0 = np.asarray(d0.resize((80, 140), Image.LANCZOS)).astype(float)
reg = a[3065:3205, 2950:3030]; al0 = d0[..., 3:4] / 255
reg[:] = reg * (1 - al0) + d0[..., :3] * al0


# ---- 2c. Son: skin oval inside the shirt --------------------------------------------------
x0, y0, x1, y1 = 680, 3335, 780, 3460
sk = np.zeros((H, W), bool)
sk[y0:y1, x0:x1] = near(a[y0:y1, x0:x1], a[3400, 712], 50) | near(a[y0:y1, x0:x1], a[3400, 750], 50)
lab, _ = ndimage.label(sk); sk = (lab == lab[3400, 712]) | (lab == lab[3400, 750])
oval = ndimage.binary_dilation(sk, iterations=15)
protect = np.zeros((H, W), bool)                  # the shirt's own shoulder outline stays
for y in range(3300, 3470):
    row = L[y, 600:800] < 120; xs = np.where(row)[0]
    if not len(xs): continue
    splits = np.where(np.diff(xs) > 1)[0]
    runs = np.split(xs, splits + 1)
    if y < 3343: keep = runs
    elif len(runs) >= 2: keep = runs[:1]
    else: keep = []
    for r in keep: protect[y, 600 + r.min() - 2:600 + r.max() + 3] = True
oval &= ~protect
shirt = near(a, a[3420, 800], 70) & (L > 60)
conv_fill(oval, shirt, (600, 3260, 880, 3540), 8)
# his arm line: from the shoulder seam straight down into the existing line (centre 727, 11 px)
d0 = Image.new("RGBA", (120 * 4, 220 * 4), (0, 0, 0, 0))
ImageDraw.Draw(d0).line([((733 - 680) * 4, (3330 - 3300) * 4), ((727 - 680) * 4, (3462 - 3300) * 4)],
                        fill=INK + (255,), width=LINE * 4)
d0 = np.asarray(d0.resize((120, 220), Image.LANCZOS)).astype(float)
reg = a[3300:3520, 680:800]; al0 = d0[..., 3:4] / 255
reg[:] = reg * (1 - al0) + d0[..., :3] * al0


# ---- 3. Son's squat: erase tubes/legs/feet, rebuild ----------------------------------------
yy, xx = np.mgrid[0:H, 0:W]
R = (yy >= 3600) & (yy <= 3990) & (xx >= 690) & (xx <= 1020)
R &= ~((yy < 3613) & (xx < 880))                       # shirt above the new waistband stays
R &= ~((yy < 3618) & (xx > 1010))                      # his reaching arm passes here
# background: the same rows of clean grass 830 px to the right (between turtle and lamb)
ys_, xs_ = np.where(R)
def energy(dx):
    blk = L[ys_.min():ys_.max() + 1, xs_.min() + dx:xs_.max() + 1 + dx]
    return np.abs(blk - ndimage.gaussian_filter(blk, 4)).mean() + 50 * (blk < 90).mean()
DX = min(range(580, 1031, 10), key=energy)             # the cleanest grass strip on the same rows
print("grass source shift", DX)
src = np.roll(a, -DX, axis=1)
bx = (560, 3480, 1160, 4110)
base = a.copy(); good = np.ones((H, W), bool); good &= ~ndimage.binary_dilation(R, iterations=4)
good &= (L > 90) & (a[..., 1] > a[..., 2] + 20) & (a[..., 0] - a[..., 1] < 25)          # grass pixels only (no dog, no outlines)
conv_fill(ndimage.binary_dilation(R, iterations=4), good, bx, 45)
low = a.copy(); a[:] = base
src = low + (src - np.stack([ndimage.gaussian_filter(src[..., k], 45) for k in range(3)], -1))
feather = ndimage.gaussian_filter(R.astype(float), 3)[..., None]
grow = ndimage.binary_dilation(R, iterations=6)[..., None]
a = np.where(grow, a * (1 - feather) + src * feather, a)

# a stray dark tick in the copied grass, right of the shorts
Lg = a @ [0.299, 0.587, 0.114]
tick = np.zeros((H, W), bool); tick[3628:3672, 1004:1032] = True
conv_fill(tick, (Lg > 120) & (a[..., 1] > a[..., 2] + 20), (960, 3590, 1070, 3720), 6)

S4 = 4; bx0, by0, bx1, by1 = 600, 3540, 1040, 4010
lay = Image.new("RGBA", ((bx1 - bx0) * S4, (by1 - by0) * S4), (0, 0, 0, 0))
d = ImageDraw.Draw(lay)
P = lambda pts: [((x - bx0) * S4, (y - by0) * S4) for x, y in pts]
GOLD, SKIN, K = (221, 166, 84), (168, 108, 80), INK + (255,)
sh = Image.new("L", lay.size, 0); ImageDraw.Draw(sh).ellipse(P([(690, 3912), (990, 3968)]), fill=255)
d.line(P([(879, 3592), (881, 3618)]), fill=K, width=LINE * S4)                       # shirt edge
d.line(P([(742, 3790), (700, 3862), (738, 3926)]), fill=K, width=LINE * S4, joint="curve")   # legs
d.line(P([(850, 3762), (912, 3838), (890, 3904)]), fill=K, width=LINE * S4, joint="curve")
shorts = P([(688, 3662), (689, 3612), (880, 3611), (889, 3640), (892, 3700), (889, 3758), (878, 3775), (790, 3789), (690, 3800)])
d.polygon(shorts, fill=GOLD + (255,), outline=K, width=LINE * S4)
d.line(P([(790, 3788), (790, 3740)]), fill=K, width=int(LINE * 0.8 * S4))
d.line(P([(731, 3578), (741, 3600), (780, 3622), (830, 3646), (858, 3664)]), fill=K,
       width=LINE * S4, joint="curve")                                                # resting arm
d.ellipse(P([(890, 3646), (916, 3674)]), fill=SKIN + (255,), outline=K, width=int(LINE * 0.8 * S4))  # thumb bump
d.rounded_rectangle(P([(852, 3658), (920, 3706)]), radius=22 * S4, fill=SKIN + (255,), outline=K,
                    width=int(LINE * 0.9 * S4))                                       # mitten
d.ellipse(P([(893, 3652), (912, 3670)]), fill=SKIN + (255,))
for cx, cy in ((752, 3938), (904, 3918)):                                             # feet
    d.ellipse(P([(cx - 40, cy - 17), (cx + 40, cy + 17)]), fill=SKIN + (255,), outline=K,
              width=int(LINE * 0.9 * S4))
from PIL import ImageFilter
lay = lay.resize((bx1 - bx0, by1 - by0), Image.LANCZOS)
shd = np.asarray(sh.resize((bx1 - bx0, by1 - by0), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))).astype(float) / 255
region = a[by0:by1, bx0:bx1]
region *= (1 - 0.22 * shd)[..., None]
la = np.asarray(lay).astype(float); al = la[..., 3:4] / 255
region[:] = region * (1 - al) + la[..., :3] * al

Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT)
print("wrote", OUT)

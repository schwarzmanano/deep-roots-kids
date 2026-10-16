# Gate 2 — Style-lock tests (Stage 2–3), he-didnt-walk-away

2026-10-17. Gate 1 signed 2026-10-16. 8 tests × 2 attempts = 16 images, **$1.45** of the
$12 cap (12%; first stop at $6.00). Prompts: `prompts/pages/test-*.txt`; images: `gen/test-*/`
(not yet backed up to iCloud gen-archive — run the README rsync, dry-run first). Contact sheets:
`qa/stage2-contact-a.jpg` (shoot-refrain → dawn-hills), `qa/stage2-contact-b.jpg` (gate-outside →
family-six). Line weight referenced to made-like-him `art/style-lock.png` (REFERENCE A, 10.13 %
ink) — weight matches Book Three on every image; composition references D carried from Book Three.

Every attempt was thresholded (128), frame-stripped and traced with the production path
(`postproc.process` → `vectorize.trace`): midtone 0.00 % on all 16; frames drawn on 7 of 16 and
stripped in post (as Books Two and Three).

| Test | Result | Notes |
|---|---|---|
| shoot-refrain (D1, as p13) | **PASS** | Seed in a furrow, one shoot, two round leaves, sun half-circle with short light-lines; reads in pure black and white, no grey. a02 adds a frame (stripped). Ink 3.3–3.8 % (−62/−67 % vs lock → `density: sparse`, as Book Three p21/p27). |
| shoot-small (D1 at its SMALLEST, as p15) | **PASS** (a01) | a01: seedling ≈ 7 % of page height; after threshold + trace the two leaves, stem and soil line are closed, clean shapes (`qa` zoom checked). Couple from behind / three-quarters, single-line limbs, oval hands, straight hems; the man's head shows an ear and a hint of jaw — acceptable, no features. a02: **FAIL** — the man drawn from the front with a blank face, two-sided (tube) arms and legs; frame. |
| serpent-away (D2 A, D3 A+B, as p11) | **PASS** (a02) | a02: serpent small and far among the trunks, head low, dot eye, no mouth line; seedling in the foreground. a01: **FAIL** — the serpent mid-size (not diminished) and a winding PATH drawn with the shoot ON it (path is p31-only, D9); the shoot's veins came out green (colour — threshold removes it, but it shows the model colours the shoot unasked). |
| dawn-hills (D1 secondary, as p19) | **PASS** | Outlined hills, no fill, sun half-circle with short light-lines, seedling; both read in pure black and white. a02 frame; a02's seedling very small (≈ 3 %) — p19 names it larger. Ink 1.5–2.3 % (sparse). |
| gate-outside (D7 A, as p21) | **PASS** (a02) | a02: couple from behind in the worn garments (one-shoulder tunic, knee dress, uneven hems), single-line limbs, the sword with short light-lines small at the opening behind them, the sun ahead — two light sources on one page read fine. a01: **FAIL** — two-sided muscular limbs, the man's profile (nose and chin) visible. The tiny shape above the sword on a01 is the distant tree of life, not a figure. |
| mended-cup (R3, D8a A, as p27) | PASS with defect | Both: the cup on a step (a01) / small table (a02), seedling growing from soil inside, children NOT touching it, dog present, sun. **Defect (needs a ruling, B1 below): the "seam" came out as a branching CRACK line — in black and white the cup reads as still cracked, not mended.** Both attempts: children face the viewer instead of looking at the shoot (D-11); a01 adds an unasked raised garden bed with plants behind them; frames on both. |
| father-shirt (F23, as p25) | **1 of 2 FAIL — REPORTED** | a01: **tube limbs on the Father** (two-sided arms and legs) in the short-sleeved collared shirt; the dog's ear filled solid. a02: the same shirt with single-line arms and legs, mitten hands — the outfit CAN render in LINE vocabulary, but it fails half the time on this cast. Not silently swapped for sleeveless (brief §4). Son worried face, cup cracked and untouched, nobody fixing anything, on both. |
| family-six (D8a A / D-10, as p29) | **PASS** | Both attempts: EXACTLY six people — Father, Mother (head wrap, hair beneath, wrap dress), Daughter 1 (locs + glasses), Daughter 2 (braids + glasses), Daughter 3 (beaded braids), Son (curls) — plus the dog; the cup with the shoot on a step/table, not held; single-line limbs throughout, no hand-holding. Count defect D-10 did not occur. a01 frame + 14 edge slivers stripped. Ink 8.9–10.0 % (matches lock). |

## Findings for the editor (Gate 2 rulings needed)

1. **B1 — The mended cup's seam does not read as "mended" in line art.** The model draws the seam
   as a crack (a01 branching, a02 a jagged line), so p27/p29 look like the cracked cup of p23/p25.
   On the cover the Roots Gold seam carries the meaning; a coloring page has no colour. Options
   (plan amendments, your call): (a) accept one straight thin seam line and let your words carry
   "mended" (re-test once with "one straight hairline, not jagged, not branching"); (b) draw the
   seam as a short dotted/stitched line — unmistakably a repair, but "stitching" is a mender's
   mark (R3 risk: it shows that someone did it); (c) no seam on the page — the cup whole with the
   shoot inside; the difference from p23/p25 is "whole vs cracked" and the seam lives on the cover
   only; (d) a reference key: print nothing extra, but your p27 teaching line tells the child to
   colour the seam gold (text, not picture — your words).
2. **B2 — The Father's short-sleeved collared shirt fails 1 of 2 (tube limbs).** Reported, not
   worked around. Options: (a) keep the shirt and budget an extra attempt on p25/p29 (two family
   pages); (b) sleeveless round-neck top as Book Three p25 (tested LINE, no failures); (c) keep
   the shirt and send father-shirt a02 as the composition reference for p25 and p29.
3. **B3 — Children "looking at the shoot" came out as facing the viewer** on both mended-cup
   attempts (D-11 lined-up composition). Options: (a) accept facing-the-viewer for p27 (the cover
   does the same); (b) re-scene p27 with the children three-quarters toward the cup, heads turned
   down to it (faces still visible — bible rule).
4. **B4 — The seedling is drawn with a leaf midrib line and the model coloured it green once**
   (serpent-away a01). Threshold removes colour; the midrib is a fine line (~1.2 pt at trim on
   shoot-small) that `thicken_thin_strokes` will lift to the 2 pt floor where flagged. No ruling
   needed unless you want the leaves plain (no midrib) — say so and style.md names it.
5. **B5 — Style-lock candidate.** Line weight stays locked to Book Two's reference (as Book Three).
   For Book Four's own composition references (REFERENCE D): first-couple → `gate-outside a02`;
   family → `family-six a02` (clean six-count) or `father-shirt a02`. Confirm or pick others.
6. **B6 — Smallest-size proof done:** the seedling at ≈ 7 % of page height (shoot-small a01)
   survives threshold and vectorize as closed shapes. p15 and p17 may use that size; nothing
   smaller is planned.
7. **F8 (still open from Gate 1):** all family tests used the backyard garden with the picket
   fence (Book Three's cover setting) and a low back step for the cup — the (b) option. Rule
   (a)/(b)/(c) before page generation.

## Guardrails checked on the test images

- No figure, face, hand or light-shape in the sky on any image; light-lines only around the sun
  and the sword (§0, D1). No Christ-marker anywhere (§1/§2). No human mender, glue or tools on
  mended-cup/family-six (R3). No kneeling, folded hands or hugging (D4b). Serpent plain, dot eye,
  no mouth line, moving away (D3). No fruit, no fig leaves, no animal near the garments.
- Defects by family (factory/defects.md): D-01 tube limbs ×3 attempts (shoot-small a02,
  gate-outside a01, father-shirt a01); D-11 lined-up ×2; D-16 scope (path on serpent-away a01);
  D-20 frame ×7 (post); D-21 slivers ×3 (post); D-14 unasked objects ×1 (garden bed).

**STOPPED AT GATE 2.** No page generation until the editor rules B1–B5 and F8 and locks the
composition references in book.yaml.

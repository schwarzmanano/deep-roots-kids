# Gate 3 — Full proof (Stages 4–5), he-didnt-walk-away

2026-10-17. Gate 2 passed 2026-10-17 (B1 a → B1-2 post-drawn seam, B2 c, B3 a, B5, F8 b).
Two generation rounds: 15 pages × 2 + 6 pages × 2 = 42 attempts, **$3.88**; style tests $1.65;
**book total $5.53 of $12 (46 %)** — the 50 % stop at $6.00 has not been reached; the cover
(step 6) will cross it and needs `KIDS_PAST_CHECKPOINT=he-didnt-walk-away@50` on every call.
Rejection log with causes: `qa/defects.md`. Contact sheets: `qa/round1-contact-a..d.jpg`,
`qa/round2-contact-a.jpg`; final art `qa/gate3-contact.jpg`; rendered proof pages
`qa/gate3-proof-pages.jpg`. gen/ backed up to the iCloud gen-archive (24 folders).

## Mechanical QA (scripts/qa.py) — 15 pages, 0 flagged
Threshold 128 → bitonal (midtone 0.00 % on every page); frames stripped on 5 pages (p23–p31);
stroke floor 2.0 pt met everywhere (p25 thickened: 3 strokes at 1.68 pt → `thicken_thin_strokes`);
edge ink 4–16 % (floor 22 %); ink 2.3–10.1 % vs the lock's 10.13 % — pages beyond −50 % are the
`density: sparse` symbol pages (p9, p11, p13, p19, p31), as Book Three p21/p27.
Post corrections (`art/limbfix.py`, originals in `art/pre-limbfix/`): p27 one straight hairline seam
drawn; p29 the model's wavy crack erased and the same hairline drawn. Nothing else touched.
Vectorized (potrace, 789 KB of SVG). Text QA 0 fail; WEB fidelity 0 problems; provenance clean
(40 human, 6 public-domain); disclosure TEXT None.

## Print files (PROOF builds, stamped)
`out/interior.pdf` (KDP 8.5 × 11, 36 pp) and `out/interior-lulu.pdf` (8.75 × 11.25, bleed) —
both preflights PASS (K-only, DeviceGray images, no transparency, fonts embedded, margins 0.5 in).
The author's couplets print on two lines (layout.py now honours explicit line breaks).

## Vision rubric — points for the editor's own review
1. **p3 hiding is weak.** The man stands half behind a trunk, the woman beside hers in the open.
   Both rounds failed to hide them fully (round 1 open, round 2 a04 hugging the trunks). Options:
   accept (the words carry "we ran"), or one more re-scene with the trunks named wider than the
   figures.
2. **p3, p5 and p7 share one composition** (same trees, same couple placement) because p5 a01 is
   the plain-treatment composition reference and the model copied its scene, not only its
   framing (D-14). They read as a three-page sequence; the editor may prefer p7 re-rolled with a
   different reference.
3. **Wind marks in the sky on p3 and p5** (curved gust lines among the clouds) — wind, not
   voice-lines; confirm they pass DECISION-1.
4. **The seam on p27/p29 is a hairline** (3 px ≈ 2.5 pt at trim) — visible but quiet; in print it
   reads as a line down the cup, and the author's words carry "mended" (B1 a).
5. **p29 six-count correct**, all fixed markers present (Mother's head wrap with hair beneath,
   Daughter 1 locs + glasses, Daughter 2 braids + glasses, Daughter 3 beads, Son curls).
6. **Serpent sizes** p7 mid, p9 small, p11 smallest (D3 A+B) — confirm the p11 serpent is still
   recognisable at print size (it is ~4 % of page width).
7. The guardrail checklist in the signed review was walked against the final art: no figure, hand,
   face or light-shape in any sky; light-lines only around the sun and the p21 sword; no
   Christ-marker; no human mender; no contact poses; serpent plain, no mouth line.

**STOPPED AT GATE 3.** No cover work, no release build, until the editor reviews the proof.
Next after approval: step 6 cover "MENDED" (B&W stick reference first), step 7 print files for
both editions, step 8 listing.

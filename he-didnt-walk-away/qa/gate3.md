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

## Corrections at the editor's instruction (2026-10-17, "correct everything before the cover")
- **Text:** p7's WEB quotation now ends with the §8 added closing ”; p2 copyright holder reads
  "Deep Roots Publishing" (the ruled imprint); p17's duplicate Yahweh sentence removed so the
  name is explained once, on p7 (guardrails §6). Nothing was added or reworded; provenance
  re-pinned with the instruction as source; all guards clean.
- **p3 re-rolled (round 3)** with Book Three's approved hiding page as composition reference:
  a06 chosen — two thick trunks, the woman mostly behind hers, the man half behind his. A hint
  of the man's profile at the turned head (no features drawn).
- **p7 re-rolled (round 3)** with p9's page as composition reference so it no longer copies p5:
  a06 chosen — open ground, distant tree line, serpent moving away at the right, no sun.
- **p5 sky marks erased in post** (art/limbfix.py) — the sky is empty; wind lives in the trees.
- **Round 3 cost $0.37 — book total $5.90 of $12** (the $6.00 stop is $0.10 away: the cover
  needs `KIDS_PAST_CHECKPOINT=he-didnt-walk-away@50` on every call).
- QA re-run: 15 pages, 0 flagged (p7 edge ink 21.6 %, under the 22 % floor — the unasked flowers
  along the bottom edge); vectorized; both interiors rebuilt (PROOF) and both preflights PASS;
  gen/ backup re-synced.

## Remaining notes for the editor's eye (not defects)
1. The seam on p27/p29 is a quiet hairline (B1 a) — the author's words carry "mended".
2. p11's serpent is small by ruling (D3 A+B, ~4 % of page width) — still a plain snake at print size.
3. p7's foreground flowers were not asked for; harmless, removable in post if wanted.

**STOPPED AT GATE 3.** No cover work, no release build, until the editor approves this proof.
Next after approval: step 6 cover "MENDED" (B&W stick reference first), step 7 print files for
both editions, step 8 listing.

## Limb corrections before upload (editor 2026-10-17: "correct all the limbs on pages 3, 5, 7, 9, 15, 21")

`art/limbfix.py` now carries Book Three's tube-limb centre-fitting op and explicit line/oval ops:
- p5, p7, p9, p21: the woman's two-sided legs refitted as single lines (feet kept); stubs under
  the hem and above the feet walked out without nicking either.
- p15: the woman's legs refitted; her open half-oval feet redrawn as plain ovals; the man's left
  mitten and his pointing hand, and the woman's right mitten, redrawn as plain ovals on the arm
  lines (first couple: plain ovals, one pointing gesture carried by the arm).
- p3: the trunk edge runs into the man's left leg and arm, so legs and arm were drawn explicitly:
  single lines with oval feet/hand, the trunk edge untouched, old stubs erased.
Re-run after the corrections: QA 15 pages 0 flagged; vectorized; both release interiors rebuilt;
Lulu interior pure DeviceGray; preflights PASS; print_table PASS. Contact: `qa/limbfix-contact.jpg`.

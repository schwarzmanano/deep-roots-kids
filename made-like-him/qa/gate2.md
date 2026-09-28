# Gate 2 — Style Lock Review

**Book:** made-like-him · **Candidate page:** p19 "Made to Care for God's World"
**Status:** AWAITING EDITOR — nothing locked; `book.yaml generation.style_lock` is still null.
**Spend:** 4 attempts, $0.3770 (ledger $7.4739 of the $10.00 series cap).

Contact sheet: `qa/gate2-p19-contact.jpg`. Sources: `gen/p19/attempt-0{1..4}.jpg`.

## Measured (same checks as qa.py, run per attempt)

| # | ink % | min stroke pt | thin strokes | edge-ink % | frame drawn | midtone |
|---|---|---|---|---|---|---|
| 1 | 14.32 | 2.43 | 0 | 11.9 | yes | 0.00 |
| 2 | 11.66 | 2.25 | 0 | 15.5 | no | 0.00 |
| 3 | 11.07 | 2.39 | 0 | 9.4 | yes | 0.00 |
| 4 | 10.13 | 1.59 | 2 | 16.1 | no | 0.00 |

## Read against the contract

| # | Cast markers | Garments / limbs | Contract breaks | Verdict |
|---|---|---|---|---|
| 1 | head wrap plain; rest ok | short sleeves on 4 figures | unrequested cat; sleeves; crowded | reject |
| 2 | all six correct, patterned head wrap, D3 hem band | sleeveless, single-line limbs | D3 frowning; bowl not basket; edge crops | runner-up |
| 3 | head wrap plain | sleeves + Son in long trousers → tube limbs | open mouths; shed/shelf clutter | reject |
| 4 | all six correct, patterned head wrap + wrap tie, D3 hem band + beads | sleeveless, single-line limbs, arms away from torso | horizon + cloud run edge-to-edge; pumpkins cropped; 2 thin strokes (water drops) | **recommended** |

**Recommendation: lock attempt 4.** It's the most faithful to the cast sheet of the four,
and the only one where every contract item that matters for a *line-style* reference holds.
Its defects are compositional: the style lock is sent as "LINE STYLE ONLY", so they don't
carry through. Before p19 itself is placed as a page, those defects need either a re-roll
(conditioned on the lock) or `thicken_thin_strokes` plus an accepted edge note.

## Decisions for the editor

1. **Lock which attempt?** Recommended: 4.
2. **Ink reference.** Every candidate is 10–14% ink against genesis-1's 6.5%, because p19 is
   the busiest page in the book (6 figures + dog + garden). qa.py flags drift beyond ±50% of
   the lock, so sparse pages (p5: one figure) will flag low. Proposed: mark p5/p7 and p3
   `density: sparse`, as genesis-1 did, rather than choosing a thinner lock.
3. **Cast sheet vs. character bible.** The canonical `cast-sheet.jpg` draws Father in full
   trousers and Mother's wrap below the knee, but the bible rule says "hem at or above the
   knee". The model follows the sheet (attempts 2 and 4 both do). Recommended: accept the
   sheet as canonical for Father and Mother, since the legs still render as clean lines here.
4. **Spend cap.** The $10 cap covers the whole series and has $2.53 left. Book Two's budget
   is $3.29 (15 pages × 2.5 attempts). Raise `KIDS_SPEND_CAP_USD` (e.g. to $15), or rule
   the cap per book.

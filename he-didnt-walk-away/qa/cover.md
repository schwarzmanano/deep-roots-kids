# Cover "MENDED" — step 6 log, he-didnt-walk-away

Gate 3 approved by the editor 2026-10-17 ("proceed"); the 50 % spend stop passed on the same word
(`KIDS_PAST_CHECKPOINT=he-didnt-walk-away@50`). Concept fixed by R3; rulings F7 (Father on the
front, Mother off), F8 b (the Book Three garden with a low back step at the right), F9 (next
morning, light from the horizon only), F15 (Kindled Coral banner/spine), B1 (gold seam on the cover).

## Phase 1 — black-and-white stick-figure reference (construction check)

Prompts: `cover/ref-mended.txt` (2 attempts, $0.22), `cover/ref-mended-b.txt` (2 attempts, $0.23 —
hand-on-shoulder, one cup only, smaller figures named harder). References sent: the cast sheet and
Book Three's final cover art (setting + cup continuity). Contact sheet: `qa/cover-refs-contact.jpg`.
Book total after phase 1: **$6.34 of $12** (next stop $9.60).

| Attempt | Count | Son holds cup | Father's hand on Son's shoulder | One cup / one shoot | Notes |
|---|---|---|---|---|---|
| ref-mended-01 | 5 + dog ✓ | ✓ seam + shoot | ✗ (arm toward Daughter 1) | ✗ second seedling in the ground | heads at ~25 % |
| ref-mended-02 | 5 + dog ✓ | ✓ | ✗ | ✗ second cup on the ground | heads at ~20 % |
| ref-mended-b-01 | 5 + dog ✓ | ✓ | ✓ (behind the Son's right shoulder) | ✓ | heads at ~25 %; step at the right |
| **ref-mended-b-02** | 5 + dog ✓ | ✓ | ✓ clearest | ✓ | heads at ~26 %; step at the right; **candidate** |

Construction on b-02: every limb a single line with mitten hands and oval feet; faces dot eyes +
small mouth; fixed markers — Father's footballer cut and collared short-sleeved shirt, Daughter 1
rounded locs + round glasses, Daughter 2 neat braids + round glasses, Daughter 3 beaded braids,
Son wavy-curly hair; the dog with floppy darker ears; the cup is Book Three's rustic cup with a
handle, whole, one seam line, one shoot. Nobody mends anything (R3).

**Known and planned:** the model again keeps the figures large (heads at ~25 %, not below 40 %) —
as on Book Three, this is solved in post after the colour phase (scale to ~84 % and extend the sky
from the painting's own sky, `retouch_extend.py` pattern), not by re-rolling.

**STOPPED for the editor's construction confirmation** (limbs, faces, outfits, counts, vessel
continuity). Phase 2 (colour, 4K, brand palette, painterly background) starts only on his word.

## Phase 2 — colour art, retouch, both wraps (2026-10-17; construction confirmed by the editor)

Prompt `cover/front-art-full.txt` from the confirmed reference (ref-mended-b-02) + cast sheet +
Book Three's cover (garden, cup, skin tone); 2 attempts at 4K, **$0.44** — near-identical; **01
chosen**. Checked at full size: five people + dog, the Son holding the cup with both mitten hands,
the Father's hand on the Son's shoulder, gold seam and one shoot, brand palette, no sun disc, light
from the horizon, the step at the right. Garments reach the shoulder point (square neckline on
Daughter 1 is a neckline, not an armhole sliver) — no shoulder retouch needed.

**Retouch** (`cover/retouch_extend.py`, the Book Three method): art scaled to 84 % and bottom-
anchored on the front-panel canvas, the sky extended upward from the painting's own sky (16 %),
the sides filled from the hedge strip — the right side from the LEFT edge strip so the step is not
repeated. Heads now sit at ~37 % of the height, below the title zone. Output
`cover/front-art-01-retouched.png` (3680 × 4800, 427 ppi on the wrap).

**Grid build** (`cover.py`): Kindled Coral banner with Navy text (contrast 3.13); title Baloo 2
Bold 61 pt (KDP) / 57 pt (Lulu), subtitle Lora 19.5 / 18.5 pt fit-to-width (F17 still open);
blank Coral spine with the new `spine.overlap_in` 0.0625 in running past both folds (brief §6);
back panel as Books One to Three plus the new **series strip** — the four fronts in order from each
book's release cover.pdf (Book Four from its own front render), Four outlined in Storybook Navy,
the Navy→Coral shift visible — above the logo/barcode zone; `cover.website_line` slot added
(empty — awaits the author's words; the release guard holds it).

**Verification:** cover preflight PASS on both targets (lowest raster 400 ppi, DeviceCMYK, no
transparency, fonts embedded, text inside the safe zone, barcode band clear); `print_table.py`
PASS (KDP wrap 17.331 × 11.25 in, spine 0.0811 in; Lulu 17.391 × 11.25 in, spine 0.1411 in;
36 pp). Proof sheets with trim, fold and safe-zone lines: `qa/cover-kdp-proof.jpg`,
`qa/cover-lulu-proof.jpg`; clean front: `qa/cover-front-concept.png`.
Book total **$7.23 of $12** (next stop $9.60).

**STOPPED for the editor's cover approval.** YOUR CALL items on this cover: F17 subtitle size
rule (fit-to-width as built, or a fixed size / two-line stack for the series); the website line's
wording (or drop the slot); the spine overlap width (1/16 in as built). After approval: step 7
release builds for both editions (the release guard needs the website line resolved), step 8 listing.

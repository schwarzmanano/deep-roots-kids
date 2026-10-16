# Step 0 — Carry-forward check (Book Four, 2026-10-16, no spend)

Read: we-broke-it-all `book.yaml`, `plan/pages.yaml`, `provenance.yaml`, `plan/theology-review.md`,
`plan/my-words.md`, `cover/*.txt`, `publishing/kdp-listing.md`; genesis-1 and made-like-him
`book.yaml` + listings; `_brand/` (character-bible v2.2, brand-spec, theology-guardrails §0–§8,
authorship-policy, about-the-author, cover-grid, album/); `factory/audit.md`, `factory/defects.md`;
`_brand/spend-ledger.json`; scripts.

## Pipeline used

The Book Factory is **not operational**: `factory/` holds only the Phase 1 audit and defect
register (awaiting approval and rulings B1–B5). There is no `/new-book`, no `book.json`
manifest, no `.claude/agents/`, no `rulings.yaml`, no platform profiles. **Every stage of Book
Four therefore runs on the proven Book Three scripts** (`kids/scripts/`: gate.mjs → generate.mjs
--test/--page → qa.py → vectorize.py → layout.py → preflight.py → gen-cover-art.mjs → cover.py →
preflight-cover.py → print_table.py → lulu_fix/verify; textunits/provenance/disclosure/textqa/
web.py for text). Same folder naming: `kids/he-didnt-walk-away/{book.yaml,plan,prompts,art,qa,
gen,out,cover,publishing,provenance.yaml}`.

## Settings, rulings and lessons carried forward

1. Architecture 36 pp / 15 single-sided illustrations (p3–p31 odd), p33 closing, p35 About the
   Author (shared file), blank versos; margins 0.5 in on all sides (= Lulu safety, the strictest
   platform) — the house safe zone; single-sided; K-only black; white paper; 8.5 × 11.
2. Two print targets from one plan: KDP 8.5 × 11 no bleed; Lulu 8.75 × 11.25 with 0.125 in bleed
   (interior-lulu via lulu_fix: DeviceGray, 300–600 ppi, SMask flattened, PDF 1.3/X-1a-style).
3. Spines computed from the FINAL page count per printer: KDP pages × 0.002252 (white); Lulu
   pages/444 + 0.06 (60# white). Spine text only above KDP 80 / Lulu 81 pages — none at 36.
4. Series cover grid (`_brand/cover-grid.md`, grid_version 1): banner 1.40 in in the signature
   colour (textured), banner text Baloo 2 ≤ 18 pt in Navy or Cream by "stronger contrast wins";
   title Baloo 2 Bold (static wght-700) in the upper third; Lora subtitle; no front author line,
   no front logo; back logo bottom-left 0.85 in; barcode box bottom-right (KDP 2.0 × 1.2 in
   inset 0.25; Lulu 3.0 × 1.5 inset 0.5); spine signature colour only. Books One to Three are
   all on this grid (Book One moved 2026-10-04).
5. Signature colours fixed: B1 Canopy Green, B2 Roots Gold, B3 Storybook Navy. No
   movement-to-colour mapping exists in config; the eleven-book map is PROPOSED only (F15).
6. Cover art: two-phase (B&W stick-figure reference, editor confirms construction, then colour,
   Gemini 4K via gen-cover-art.mjs with --ref images); brand palette only; full-bleed painterly
   background, upper 35 % clear sky, heads below 40 %, children 40–45 % of height; the model will
   not shrink figures below ~50 % or drop the armhole wedge by prompt — retouch instead
   (cover/retouch_extend.py pattern); ICC sRGB→CMYK; logo flattened; upload copies at JPEG q88
   (Lulu browser cap 10 MB). Cover-grid rules for Books 4–11: subtitle formula `<Focus> • A Deep
   Roots Kids Coloring Book`; lock title/subtitle/author before first KDP upload; one cast across
   the series; **children only on the front** (rule 4 — see F7); book-specific scenery; the cover
   promises the interior.
7. Line weight: Book Two's Gate 2 lock `made-like-him/art/style-lock.png` (REFERENCE A, line
   style only) — also Book Three's; composition references REFERENCE D only.
8. Generation defaults: gemini-3.1-flash-image, 1k, 3:4, ~$0.088/image; cast sheet
   `_brand/cast-sheet.jpg` (faces/markers only); first couple `_brand/p25-figures-ref.jpg` +
   Book Three p29/p31 for the garments; style.md Positive/Negative/Human-figures sections lifted
   verbatim into every prompt; text banned repeatedly; frame strip + edge-sliver strip; threshold
   128 → bitonal BEFORE vectorize (potrace); thin strokes < 2 pt thickened; ink-density ±50 % flag
   with `density: sparse` exemption; EDGE-HEAVY flag (inner 85 % safe area); qa.py re-applies a
   book's art/limbfix.py, so always qa.py before vectorize.py.
9. Spend: per-book cap in book.yaml (`spend_cap_usd: 12`), checkpoints 50 % / 80 %, go-ahead
   `KIDS_PAST_CHECKPOINT=<slug>@<pct>` on every call past a checkpoint; log HTTP 402 stops.
   Actuals: Book Two $11.49, Book Three $8.97, Book One $6.75 (ongoing), series $28.93.
10. Gate discipline: generation blocked until theology-review.md `**Status:** SIGNED` with a
    Signed/Date block; page attempts predating the signature re-block (gen/test-* exempt); never
    edit a signed review (its mtime re-blocks the gate); no agent writes "approved"/"confirmed".
11. Authorship: AI never drafts print prose; pointers + verbatim excerpts with file/line
    locations only; every unit registered in provenance.yaml (page, kind, author, draft, sha);
    my-words.md is the source of truth; release guard (`layout.py --release`, `cover.py
    --release`) refuses ai-drafted / draft / unresolved / unconfirmed / sha-drift / stale units and
    any AI statement in print; proofs stamped PROOF - NOT FOR RELEASE; `print_ai_note: false`;
    disclosure computed by disclosure.py (expected text None / images AI-generated with extensive
    editing / translation none); "[cite: N]" paste artefacts never imported.
12. Scripture: WEB only (DECISION-4), public-domain tagged, verbatim-checked by web.py against
    `_brand/web/*.json` (cache extended today: GEN04, GAL03, GAL04, ROM16, 2CO01, HEB11; web.py
    now maps "galatians"); exactly three §8 departures (one added ”, sentence-initial capital,
    sentence-end period); no "(WEB)" tags on pages; "Yahweh" kept, the author's line at its
    first appearance per book; teaching-script ESV never printed; the companion curriculum
    (ESV) never opened for wording.
13. Text QA lessons (automated): lowercase generic "gods" (CAPITAL-GODS); no two pages opening
    with the same five words (REPEATED-OPENING, exact-set exceptions via book.yaml
    `textqa_exceptions`); NOT-WEB-VERBATIM; straight quote marks in Scripture flagged.
14. Book-number format: print surfaces use WORDS ("Book Three" in the series line, banner
    "BOOK THREE"); the platforms' series-number field is numeric by design ("Book 3" on KDP);
    the copyright line carries no number. Book Four follows the same split: words in print,
    numeral only in the KDP/Lulu series field. (No automated check exists for this — reported.)
15. US spelling throughout ("color" ruled 2026-10-12, incl. the back-cover fact line).
16. Frames must not clip artwork: find_frame_crop + strip_edge_slivers; inner 85 % safe area;
    EDGE-HEAVY flag; nothing important outside the 0.5 in zone (interior) or the safe box (cover).
17. Spine fold: the spine is a flat signature-colour band drawn to its computed width; the back
    panel is Parchment Cream and the front is art, so a colour change DOES sit on each fold today
    (Books One to Three). The brief's "redemption colour running continuously from back to front"
    is therefore a change to cover.py for Book Four (extend the band past the fold by a bleed
    tolerance, or wrap the band onto the back) — to be ruled with the cover (step 6).
18. Standing theology rules: guardrails §0–§8; DECISION-1; DECISION-5 (first couple: from behind,
    no faces, single-line limbs, oval hands/feet; straight hems before 3:21, uneven hems after);
    §2 Rescuer symbolic only; §5 outside-cast figures without markers; serpent plain, no mouth
    line; no fig leaves worn; no death imagery; no animal near the garments; no hand-holding
    unless the scene names it; one pointing gesture where the story needs it (bible v2.2); mitten
    hands with one thumb bump for the cast, ovals for the first couple; no hats/hoods; faces on
    cast members unless a DECISION says otherwise.
19. Known defect families to pre-empt (factory/defects.md): tube limbs from sleeves/coats and
    contact poses (hugging, holding, hand on shoulder, seated); cast-count errors on crowd pages;
    reference-object bleed; fruit as apples; frame drawn; text labels; realistic anatomy; the
    scale creep on covers.
20. Backups: `gen/` to iCloud gen-archive with the fixed rsync form (dry-run first; `.env` never
    in git; `out/`, `gen/`, unchosen cover candidates untracked).

## Continuity facts confirmed (how things were drawn and approved)

- **Adam and Eve:** see theology-review §Continuity — approved on Book Three p3–p31, limb-corrected
  2026-10-12 (art/limbfix.py). p31 is the worn-garments reference; p29 the laid-out gift.
- **The serpent:** Book Three p5, p7, p17, p21 — plain snake, dot eye, no mouth line (removed in
  the final release). p21 (alone on bare ground, moving away) is the reference for Book Four.
- **The guarded gate:** Book Three p31 — opening in a line of rounded trees, single upright sword
  with short light-lines, tree of life small inside, no figure/wings/flames.
- **Book Three's cover:** a **backyard garden at late afternoon** (low picket fence, side hedges,
  grass), NOT a porch; a **terracotta clay cup with a handle** and one crack, NOT a mug; Son
  (gold sleeveless tee, navy shorts, pointing at the dog) and Daughter 3 (coral sundress, beaded
  dark braids), the dog present; no adults. Prompt: `we-broke-it-all/cover/front-art-v5-full.txt`;
  final art `front-art-v5-01-retouched.png` (editor-approved 2026-10-03).
- **Family outfits approved in Book Three:** p19 Son sleeveless t-shirt + shorts; p25 Father
  sleeveless round-neck top + knee-length shorts, Daughter 3 sleeveless nightgown; cover as above.
  Tested LINE vocabulary (character-bible): short sleeves, sleeveless, shorts, skirts/dresses any
  length, pushed-up sleeves; trousers = SHAPE; long sleeves/coats = FAIL.

## Author, publisher, translation

- **Author field:** `Deep Roots` — identical on the live KDP and Lulu listings of Books One to
  Three (book.yaml `author:`, PDF metadata); copied into Book Four. Schwarz is credited only on
  the About the Author page. No front-cover author line.
- **Publisher / imprint:** Books One to Three print "© 2026 Deep Roots Kids" and list publisher
  "Deep Roots Kids"; KDP's free ISBN shows "Independently published"; Lulu Direct carries none.
  **YOUR CALL (F16):** keep "Deep Roots Kids" or move Book Four to the Deep Roots Publishing imprint
  (registered Oct 2026; already the curriculum's imprint) — the latter needs your own ISBN on KDP.
- **Translation:** WEB kept for Book Four unless ruled otherwise at Gate 1. The curriculum is ESV;
  no curriculum file was opened for wording, and the pipeline's WEB check would reject ESV text.

## Spend estimate (honest, against actuals)

Book Three: 30 style-test calls $2.78 · 38 page attempts $3.45 · cover 4 B&W refs + 12 colour
$2.74 → $8.97. Book Two: 113 interior attempts + 8 cover → $11.49. Book Four at Book Three's
rate: 7 test subjects × 2 ($1.30) + 15 pages × 3 ($4.10) + cover 4 refs + 6 colour ($1.50) ≈
**$6.90**; at Book Two's rate ≈ **$11.50** (past the 80 % stop at $9.60, under the $12 cap).

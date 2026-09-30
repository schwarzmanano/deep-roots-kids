# Deep Roots Kids — Character Bible

**Version 2.1 — 2026-09-30.** See [Changelog](#changelog). Book One (genesis-1) was built
under v1.0; its assets and `cast-sheet.jpg` are untouched by v2.0.

Flat-vector cast, clean black outline, minimal geometric shapes (circle heads, simple
rounded bodies). For coloring pages: pure black outline on white, zero color fill.
For full-color hybrid pieces: flat-vector characters over a painterly background.

## The Cast — fixed identity vs. flexible outfit

Each character is identified by fixed markers (hairstyle, accessories, silhouette) that
never change — these are what make them recognizable in outline form with no color.
Outfits change with the scene (v2.0 — see "Wardrobe" below).

**`cast-sheet.jpg` is canonical for faces and fixed identity markers only** (v2.0). The
outfits drawn on it are one example, not the canonical wardrobe.

| Character | Fixed markers (never change) | Default outfit | Outfit notes |
|---|---|---|---|
| Father | East African man; short, tight, rounded "footballer" haircut; gentle curved smile line | Collared shirt, trousers | Swap shirt/trousers for scene — haircut and build stay fixed |
| Mother | European woman; blonde wavy hair peeking from a colorful head wrap; head wrap itself is a fixed marker | Kitenge wrap-dress | Dress may vary — head wrap must always appear, hair always visible beneath |
| Daughter 1 | 18, mixed-race; rounded loc hairstyle; round glasses always on | Simple top and trousers/skirt | Glasses and locs are non-negotiable identifiers |
| Daughter 2 | 10, mixed-race; round glasses always on; neat braids | Simple dress or top/bottoms | Neat (unbeaded) braids distinguish her from Daughter 3 |
| Daughter 3 | 6, mixed-race; braids with beads (visible bead shapes) | Simple dress with a clear hemline | A garment must always be visibly drawn — bare-torso is a known defect |
| Son | 4, mixed-race; wavy-curly hair texture | Simple shirt and shorts | Curly hair texture is his identifier |

**Pets** — Dog: small family dog, light coat with darker ear markings, same flat outline
style. Cat: second household pet, simple undetailed design; keep it plain, not a named
character with its own bible.

## Wardrobe — scene-driven clothing (v2.0)

Characters change clothing to suit each scene where the scene calls for it — harvest,
garden, table, rain, church, bedtime, winter, and so on.

- **Age-appropriate and modest.** Children in ordinary child clothes, parents in ordinary
  adult clothes, babies and toddlers in baby and toddler clothes. Nothing sexualized.
  Nothing costume-like unless the scene is literally a costume.
- **Consistent within a scene.** Within one page — and across a facing spread — each
  character keeps the same outfit. Changes happen between scenes, never within one.
  Consecutive pages that are explicitly the same moment or place (e.g. "same street,
  different moment") count as one scene.
- **Fixed markers always win.** No garment, hat or hood may cover or replace a fixed marker:
  Mother's head wrap is always the head covering; hair, glasses, beads and braids stay
  visible. So no hats, hoods or caps on cast members.
- **Tested vocabulary only.** A book's pages use outfit types from the tested wardrobe
  vocabulary below. An untested type is tested before any page uses it.
- Each page records its outfits in `pages.yaml` as `outfits:` per character.

### Tested wardrobe vocabulary

Tested 2026-09-28 — `wardrobe-test-{warm,longtrousers,longsleeve,cold,sleep,baby}-01.jpg`,
6 sheets, $0.58, all conditioned on `cast-sheet.jpg`. Three construction outcomes:
**LINE** = limbs below the garment render as single lines (the v1 standard);
**SHAPE** = the garment itself covers the limb and renders as a clean, closed, slim garment
shape with a cuff, hand/foot oval emerging — not a single-line limb, but colourable and
clean (Father's trousers on `cast-sheet.jpg` and on the Gate 2 lock are this);
**FAIL** = the covered arm is absorbed into the torso outline (the v1 tube defect).

| Outfit type | Result | What makes it work |
|---|---|---|
| Short-sleeved tops, shirts, t-shirts | **LINE** ✓ | Sleeve ends at the upper arm; arm below is one line. |
| Sleeveless tops and dresses | **LINE** ✓ | v1 technique — unchanged. |
| Shorts; skirts and dresses at any length (knee → ankle) | **LINE** ✓ | Leg below the hem is one line; long skirts simply show less leg. |
| Wrap dress, A-line, sundress, hem-band dress | **LINE** ✓ | Garment detail lives on the torso, never on a limb. |
| Pushed-up / rolled sleeves (band at the elbow) | **LINE** ✓ | Name "sleeves pushed up above the elbow" — forearm is one line. |
| Full-length trousers | **SHAPE** ✓ | Slim straight leg shapes with a cuff; legs apart. Reads cleanly. |
| Rolled trousers (band at mid-calf) | partial | Model tends to draw them full-length with an ankle cuff — treat as SHAPE. |
| Short-sleeved sleepwear (pyjama shorts, knee nightgown) | **LINE** ✓ | Same as warm-weather. |
| Long nightgown (to ankle) | **LINE** ✓ | Legs below hem are lines. |
| Shawl / wrap over the shoulders | **LINE** ✓ | Covers the arms; hands emerge below. Best cold-weather option for Mother. |
| Swaddled newborn | ✓ | Blanket shape, face only; held in both arms by the carer. |
| Toddler romper (short sleeves, short legs) | **LINE** ✓ | Two small round hair puffs read clearly for the visiting child. |
| **Full-length long sleeves** (shirts, pyjama tops, dresses) | **FAIL** ✗ | Two attempts; the cast sheet's arms-down line-up pose overrides "arms out" in the prompt, and the sleeve hugs the torso. **Untested in an action pose.** |
| **Coats, raincoats, cardigans, puffy jackets** | **FAIL** ✗ | Same failure as long sleeves; puffy-jacket sleeves also segment into tube rings. |

**Rules from the test:**
- Pages use LINE types freely, and SHAPE for trousers.
- Full-length sleeves and coats are **not cleared for use**. Before any book needs them
  (winter, rain), run a scene-pose test: arms doing something (carrying, reaching, waving)
  with no line-up reference.
- Outside-cast figures picked up cast garments from the reference sheet (Mother's
  wrap-dress with tie, Daughter 3's hem-band dress). Their prompts must name plain,
  different garments. Guardrails §5 is about markers, but a borrowed signature garment
  still makes a stranger read as family.
- A line-up test sheet can't test pose. Pose-dependent types need a scene test.

## Universal construction rules (recurring failure points — non-negotiable)

- **Limbs**: every arm and leg is a single continuous line, one stroke — never two
  parallel lines forming a tube/capsule, never a filled sleeve or trouser silhouette.
  This has been the single most common defect across generations.
- **Hands** (v2.1): the family cast and outside-cast figures have **mitten hands with one
  small thumb bump**, exactly as drawn on `cast-sheet.jpg` — no separate fingers, no pointing
  index finger, no knuckles. The first man and woman (DECISION-5 pages) keep **plain closed
  ovals**, as on `p25-figures-ref.jpg`.
- **Feet**: plain, smooth, closed ovals for everyone — no shoes, no heel, no sole, no toes.
- **Faces**: every character gets a face, every time — simple dot/oval eyes, a small
  curved smile line. Blank/featureless faces are a defect, not a minimalist choice.
- **Detail-level matching**: backgrounds, animals and objects near a character must match
  the character's own simple flat-vector detail level.
- **Composition**: when multiple characters react to something, orient them toward it —
  not lined up facing the viewer with their backs to the subject.

## Two style modes

1. **Coloring-page mode** (this book): pure black outline, zero color, zero background wash.
2. **Hybrid full-color mode**: same flat-vector characters over a painterly background.

## Quick-reference prompt snippet

> Deep Roots Kids flat-vector cast style. [Coloring page: pure black outline, zero color
> fill.] Every limb a single continuous line — no tube shapes. Hands and feet: plain
> rounded ovals only, no fingers, no shoes. Every character fully faced — no blank faces.
> Match background/creature detail to character's own simple level.

## Generation note — how to actually get single-line limbs (2026-09-17)

Tube limbs are the bible's #1 named defect and they do NOT yield to negative prompting.
Three attempts at a full clothed cast lineup produced tube limbs every time, even with
explicit "one single line, no sleeve, no tube, no capsule" instructions.

The cause is the garment, not the model. **Long sleeves and trousers force tube limbs** —
the model draws the clothing silhouette, and that silhouette IS the tube. Single-line limbs
render correctly as soon as the limbs are BARE: a sleeveless tunic ending at the upper arm
and upper thigh, with arms and legs drawn below it.

Working reference: `character-ref-coloring.jpg`. Positive framing that works — "the whole
figure is built from one circle, one rounded tunic shape, four single lines and four small
ovals. Nothing else."

### RESOLVED — the two conditions for single-line limbs

Canonical cast sheet: **`cast-sheet.jpg`** (v5). Both conditions must hold together:

1. **Bare limbs.** A sleeveless tunic or dress ending at the upper arm and upper thigh. Long
   sleeves and trousers ARE the tube — the model draws the garment silhouette.
2. **Arms held away from the body.** An arm hanging flat against the torso gets absorbed into
   the body outline and renders as a shape, not a line. Pose both arms angled outward with
   clear white space between arm and torso. This was the last defect to fall: v3 had correct
   single-line LEGS but still-tubed ARMS purely because the arms rested against the sides.

Also note: the model adds character-name text labels unless text is banned explicitly and
repeatedly ("any text, any letters, any words, any names, any labels or captions").

Outfit note: sleeveless garments are bible-compliant — outfits are scene-flexible, only the
fixed markers are fixed. Reach for short/sleeveless whenever limb clarity matters.

## Garment identity vs. single-line limbs — NOT a conflict (2026-09-17)

The sleeveless fix initially flattened everyone into a uniform unisex tunic, which erased the
wardrobe spec (Father's collared shirt, Mother's kitenge wrap-dress). Reworking it showed the
two requirements are fully compatible, because **sleeves cause tube limbs — collars and
silhouettes do not**.

Garment identity lives entirely in features that never touch a limb:
- Father — pointed collar + straight centre button placket
- Mother — crossover V wrap, waist tie/knot, asymmetric diagonal hem
- Daughter 18 — two separate pieces, fitted top + flared skirt, split at the waist
- Daughter 10 — A-line, wide triangular silhouette, round neckline
- Daughter 6 — gathered waist + distinct horizontal hem band
- Son 4 — separate round-neck shirt + shorts, split at the waist

So the rule is narrower than "sleeveless tunic": **sleeveless, hem at or above the knee, and
arms posed away from the torso**. _(v1.0 technique — superseded as a rule by v2.0's tested
wardrobe vocabulary; kept here because it records why sleeveless works.)_ Everything else about the garment is free, which means the
wardrobe notes and the construction rules can both be honoured at once.

See `kids/_brand/brand-spec.md` for the governing colour/font/wardrobe spec.

## Changelog

- **v2.1 — 2026-09-30.** Hands standardised to what the canonical cast sheet draws (editor
  ruling, made-like-him Gate 3 audit): family and outside-cast figures use mitten hands with one
  small thumb bump; the first couple keeps plain ovals. Separate or pointing fingers are banned
  for everyone; feet are plain ovals for everyone. Previously the bible said "no thumb", which
  the cast sheet itself contradicted.

- **v2.0 — 2026-09-28.** Scene-driven wardrobe (editor ruling at made-like-him Gate 2).
  Characters change clothing to suit each scene; clothing age-appropriate and modest,
  consistent within a page/spread, changed only between scenes. The old "sleeveless, hem at
  or above the knee" rule is retired as a brand rule — it was a technique for avoiding tube
  limbs, and is replaced by the tested wardrobe vocabulary. `cast-sheet.jpg` is now canonical
  for faces and fixed identity markers only, not outfits. Unchanged: all fixed identity
  markers (hairstyle, head wrap, glasses, beads and braids, build, skin and hair hex values in
  brand-spec), flat-vector construction, the zero-colour coloring-page rule, faces on cast
  members (faces-unseen only where a page's DECISION says so), the dog and the cat.
  Book One's assets and cast sheet untouched.
- **v1.0 — 2026-09-17.** Cast, fixed markers, construction rules, sleeveless technique
  (genesis-1).

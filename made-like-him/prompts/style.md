# Style Contract — made-like-him

**LOCKED 2026-09-28** at Gate 2. Reference: `gen/p19/attempt-04.jpg`, post-processed to
`art/style-lock.png` (sent as line style only). Wardrobe per character-bible v2.0. Gate 1 rulings (signed 2026-09-27) and `kids/_brand/theology-guardrails.md` are
folded in. Every per-page prompt in `prompts/pages/` is this block plus that page's `scene`
from `plan/pages.yaml`, plus one "Human figures" section per value in the page's `figures:`.

Differs from genesis-1 in one structural way: this book is **flat-vector throughout**.
brand-spec reserves the naturalistic mode for Book One, so scenery, animals and objects are
drawn at the same simple geometric detail level as the figures (character bible:
"detail-level matching").

## Positive

- Black and white line art for a children's coloring book page, ages 4 to 7.
- Deep Roots Kids flat-vector style for the WHOLE page: figures, animals, plants, buildings
  and objects all built from simple geometric shapes at one matching level of detail.
- Pure black outlines on a pure white background. No grey.
- Thick, bold, confident, uniform line weight suitable for crayons.
- Every shape a fully CLOSED region so colour cannot leak out.
- Large simple shapes, few objects, generous open space inside each shape.
- Flat front-on storybook composition, centered.

## Negative — in every prompt, and checked in QA

Style:
- NO shading, hatching, crosshatching, stippling, gradients, solid black fills, texture.
- NO text, letters, numbers, words, names, labels, captions, signature, or border frame.
- NO naturalistic or realistic rendering of anything — no fur texture, no bark texture,
  no feathers drawn stroke by stroke.
- NO objects carried over from the style reference: no vegetables, pumpkins, cabbages,
  carrots, watering can, garden tools or dog UNLESS the SCENE itself names them.
- NO blank faces: every cast and outside-cast person seen from the front has eyes and a smile.

Theological — theology-guardrails §0-§3, non-negotiable, WLC 109:
- NO depiction of God in any form. No face in the sky. No hands reaching from clouds.
  No rays of light arranged into a figure. No dove. No radiant humanoid shape. No eye.
  No throne. No giant figure over the world.
- NO figure of Christ, and NO symbol standing for Him: no cross, no crown, no empty tomb,
  no shepherd's staff, no nail-marked hands, no halo.
- Where God acts in the text, depict only the RESULT of the act, never an actor.
- NO mirror, NO reflection of a person in water or glass.
- NO light, glow, sparkle or rays coming from any person. A lamp is only a lamp.
- NO angels, NO wings on any person.

Scope — the book ends at Gen 2:22:
- NO serpent, no fruit being taken, no fall imagery.
- NO single central, special or glowing tree in any garden scene.

## Human figures — first-couple

Pages 5-11 — the first man and woman. genesis-1 DECISION-5, carried unchanged:
- Seen from behind, at distance, small within a wide scene.
- Faces entirely unseen. No frontal view, no profile, no facial features.
- At work or in motion — planting, pointing, walking. Never posed, never facing the viewer.
- One reads male (short cropped hair, broader squarer build), one reads female (longer
  fuller hair past the shoulder, slighter build). No other markers of any kind.
- One plain simple sleeveless garment each, hem at or above the knee, un-tailored — no
  collar, no buttons, no wrap, no tie, no pattern, no fur or skin texture.
- Every arm and leg one single thin line; hands and feet plain closed ovals.
- Never in visual proximity to anything that could read as a depiction of God.

## Human figures — family

The Deep Roots Kids family cast. Faces and fixed markers copied from the cast sheet
(reference B); CLOTHES come from the OUTFITS list, not from the sheet:
- Father: short rounded haircut. Mother: head wrap with wavy hair visible beneath it.
- Daughter 1: rounded locs and round glasses. Daughter 2: neat braids and round glasses.
- Daughter 3: braids with round beads. Son: wavy-curly hair.
- Dog: small, floppy ears. Cat: plain and simple.
- Draw ONLY the family members the SCENE names.
- Every family member has a simple face: two dot eyes and a small curved smile line.
- Every arm and leg one single thin line; arms held away from the body with white space
  between arm and torso; hands and feet plain closed ovals, no fingers, no shoes.
- Short sleeves end at the upper arm; the arm below is one single thin line. Trousers are
  slim straight leg shapes with the foot oval below. No long sleeves, no coats.
- No hats, hoods or caps — hair, glasses, beads and the head wrap always visible.
- Mid-shot of people DOING something together, turned toward what they are doing.
  Never a close-up portrait. Never lined up facing the viewer.

## Human figures — outside-cast

Neighbours, strangers and the visiting family — theology-guardrails §5:
- Same construction as the family: simple face, single-line limbs, oval hands and feet,
  arms away from the body. Plain short-sleeved everyday clothes, or as named in OUTFITS.
- They carry NONE of the family's markers: no round glasses, no locs, no beaded braids,
  no head wrap over wavy hair. Nor the family's signature garments: no wrap-dress with a
  tie, no dress with a hem band.
- Variety shown by age, height, build, walking stick, wheelchair, and hairstyle.
- The visiting family: mother with a high round bun, father with a short beard, and their
  child with two round hair puffs once hair shows.

## Safe area — carried from genesis-1

- All meaningful content within the inner **85%** of frame.
- No element touching or crossing the frame edge.
- No horizontal line running unbroken edge to edge.

## Post-processing — mandatory, not optional

Unchanged from genesis-1: threshold at 128 → potrace → vector placement. See
`kids/genesis-1/prompts/style.md` for the measurements behind it.

## Known model behaviour — enforce in post, not in prompt

- **Border frame:** drawn despite prohibition (genesis-1, 3 of 3). Stripped
  deterministically in post-processing; not a QA failure.
- **Name labels:** the model adds character-name text when a cast sheet is sent (character
  bible). Banned in the prompt repeatedly; any label found is a reject, not a post fix.
- **Content bleed from references:** genesis-1 p11 inherited p23's animals. The style lock
  is sent as line style only; any object copied from it is a reject.

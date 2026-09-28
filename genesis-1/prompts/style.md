# Style Contract — genesis-1

**LOCKED 2026-09-17** at Gate 2. Reference: `gen/p23/attempt-03.jpg`
(ink 6.51%, largest open regions, thickest uniform stroke).
Gate 1 rulings folded in. Every per-page prompt in `prompts/pages/` is this block plus that
page's `scene` from `plan/pages.yaml`.

## Positive

- Black and white line art for a children's coloring book page, ages 4 to 7.
- Pure black outlines on a pure white background. No grey.
- Thick, bold, confident, uniform line weight suitable for crayons.
- Every shape a fully CLOSED region so colour cannot leak out.
- Large simple shapes, few objects, generous open space inside each shape.
- Flat front-on storybook composition, centered.

## Negative — in every prompt, and checked in QA

Style:
- NO shading, hatching, crosshatching, stippling, gradients, solid black fills, texture.
- NO text, letters, numbers, signature, or border frame.

Theological — DECISION-1, non-negotiable, WLC 109:
- NO depiction of God in any form. No face in the sky. No hands reaching from
  clouds. No rays of light arranged into a figure. No dove standing in for the
  Spirit. No radiant humanoid shape. No eye. No throne.
- Where God acts in the text, depict only the RESULT of the act — the light, the
  water, the creatures — never an actor performing it.

Scope:
- NO serpent, no fruit being taken, no fall imagery. The book ends at Gen 2:3.

## Human figures — DECISION-5, global rule

Humans appear on p25 and p27 only, and in one treatment:

- Seen **from behind**, at **distance**, **small** within a wide scene.
- Faces **entirely unseen**. No frontal view, no profile, no facial features.
- **At work** — tending, reaching, gathering. Never posed, never static, never
  facing the viewer.
- No bodily detail that would raise the clothing question. Simple covered forms.
- Never in visual proximity to anything that could read as a depiction of God.

Rationale, so it is not softened later: the image of God is shown in what they
do, not what they look like. Faces unseen means no bodily likeness is depicted,
which sidesteps Gen 2:25 entirely — there is no fall-state to get wrong.

## Safe area — added after the pre-gate test failed it

The Day 5 test cropped a fish at the frame edge and ran wave lines edge to edge.
At no-bleed that dies at the 0.25" trim and the 0.375" gutter.

- All meaningful content within the inner **85%** of frame.
- No element touching or crossing the frame edge.
- No horizontal line running unbroken edge to edge.

## Post-processing — mandatory, not optional

The API returns **JPEG**. Measured on the test image: all 256 grey levels
present, 3.2% midtone fringe, only 3.56% true black. Ringing that fine wrecks
potrace edges.

1. Threshold at 128 → pure bitonal. Verified: 256 levels → 2, midtone → 0.00%.
2. `potrace` → SVG.
3. Place vector in PDF. Resolution-independence is what makes 896x1200
   (109 DPI at 8.5x11) printable at all.

## Geometry

Generated 896x1200 = 0.747 aspect. Target 8.5x11 = 0.773. Pad, do not stretch.

## Known model behaviour — enforce in post, not in prompt

The model drew a border frame on 3 of 3 reference attempts despite an explicit
prohibition. Edge-run measured 91.6 / 93.0 / 91.7% against nothing else in the
image approaching that. The prior is strong and the negative instruction does
not override it.

Ruling: strip the frame deterministically in post-processing. Do not re-prompt
for it and do not spend on re-rolls. The prohibition stays in the prompt as a
cheap nudge, but QA treats the frame as expected-and-removed, not as a failure.

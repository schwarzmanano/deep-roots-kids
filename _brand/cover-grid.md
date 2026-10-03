# Deep Roots Kids — Series Cover Grid

> GOVERNANCE TIER: standing series asset, same standing as brand-spec.md and
> character-bible.md. Ruled by the editor 2026-10-03 (Book Three cover redesign). One formula
> for all eleven books: the geometry lives in the YAML block below and is read by
> `scripts/cover.py`, `scripts/preflight-cover.py` and `scripts/print_table.py` (via
> `scripts/covergrid.py`). Each book's `book.yaml` carries only its own values
> (`cover.layout: grid`, `cover.signature_colour`, its text units and front art).
>
> Rollout: Book Three first. **Books One and Two get the grid at Book One's rebuild — their
> live files are not touched until then** (they stay on `cover.layout: v2`).

## The grid (editor's rules)

**Front panel**
- **Top banner:** a textured band in the book's signature colour across the full width,
  with the series line (e.g. "CREATION TO GLORIFICATION • BOOK THREE") centred in Baloo 2,
  all caps. **Banner text colour: "stronger contrast wins"** (ruled 2026-10-03, option A) —
  Storybook Navy on light bands (gold, coral, sky), Parchment Cream on dark bands, chosen by the
  WCAG contrast ratio against the band. The band runs into the bleed; its text stays inside the
  safe zone.
- **Title:** the book title in **Baloo 2 Bold**, set as written in Title Case (never forced to
  capitals), in the upper third of the art, over a quiet area of
  sky, in Storybook Navy or Parchment Cream — whichever has the stronger contrast against the
  art behind it (measured per book by cover.py).
- **Subtitle:** directly below the title, in Lora, smaller, same colour rule.
- **No author line** on the front cover (matches Books One and Two). No front logo.

**Back panel**
- Deep Roots Kids logo at the bottom LEFT.
- The bottom-RIGHT barcode area stays clear on both KDP and Lulu files.
- Blurb, fact lines, series line and scripture scope set as one block above the bottom zone.

**Spine:** signature colour only — no text, no logo (every book in the series is below both
printers' spine-text minimums: KDP > 79 pp, Lulu > 80 pp).

**Art:** one continuous full-bleed painterly background (no panels, no inner border), 300+ ppi
at full cover size; upper third soft and low-detail for the title; everything important
inside the safe zone.

## Geometry (machine-readable — inches, trim-relative)

```yaml
grid_version: 1
banner:
  height_in: 1.40          # from the top trim edge down; the band also fills the top bleed (1.30 put the text 0.06in over Lulu's 0.5in safe line — 2026-10-03)
  text_font: Baloo2
  text_max_pt: 18
  text_colours: ["#2E4257", "#F7EEDD"]   # Navy or Cream — higher WCAG contrast vs the band wins (option A, 2026-10-03)
  texture: grain           # subtle paper grain + soft fibre streaks, ±4% lightness, raster CMYK
title:
  font: Baloo2-Bold        # static wght-700 instance (_brand/fonts/Baloo2-Bold.ttf) — fixes D-29
  max_pt: 84
  min_pt: 40
  top_gap_in: 0.35         # below the banner
  colours: ["#2E4257", "#F7EEDD"]   # Navy or Cream — the higher WCAG contrast vs the art wins
subtitle:
  font: Lora
  max_pt: 24
  min_pt: 14
  gap_in: 0.12             # below the title's descenders
back:
  logo_in: 0.85            # bottom-left, on the safety lines
  block_gap_in: 0.25       # clearance above the bottom zone
barcode:                   # bottom-right of the back panel, measured from the trim edges
  kdp:  {width_in: 2.0, height_in: 1.2, inset_in: 0.25}   # KDP's printed barcode box
  lulu: {width_in: 3.0, height_in: 1.5, inset_in: 0.50}   # conservative; verify against Lulu's downloaded template
spine:
  text: false
  text_min_pages: {kdp: 80, lulu: 81}
```

## Signature colours

Fixed by the editor: Book One Canopy Green `#4C7A5A`, Book Two Roots Gold `#D9A441`, Book
Three Storybook Navy `#2E4257`.

### PROPOSED eleven-book map — awaiting the editor's approval (not in use beyond Book Three)

Palette colours, and mixes of palette colours only (no new hues). Contrast is the WCAG ratio
of the banner text against the band; ≥ 3.0 is the floor for large text.

| Book | Track | Colour | Hex | Kind | Cream text | Navy text |
|---|---|---|---|---|---|---|
| 1 | He Made It All | Canopy Green | `#4C7A5A` | fixed | 4.30 | 2.08 |
| 2 | Made Like Him | Roots Gold | `#D9A441` | fixed | **1.95** | 4.59 |
| 3 | We Broke It All | Storybook Navy | `#2E4257` | fixed | 8.97 | 1.00 |
| 4 | He Didn't Walk Away | Kindled Coral | `#E2694B` | palette | **2.87** | 3.13 |
| 5 | We Need a Hero | Sky Wash 55% + Navy 45% | `#728D9E` | shade | 3.03 | 2.96 |
| 6 | Jesus Is the One | Roots Gold 70% + Navy 30% | `#A68748` | shade | **2.95** | 3.04 |
| 7 | Grace, Grace, Grace | Kindled Coral 70% + Navy 30% | `#AC5D4F` | shade | 4.11 | 2.18 |
| 8 | I Am Brand New | Canopy Green 75% + Sky Wash 25% | `#638E7A` | tint | 3.21 | 2.79 |
| 9 | Follow Every Day | Canopy Green 65% + Navy 35% | `#426659` | shade | 5.56 | 1.61 |
| 10 | He Won't Let Go | Kindled Coral 45% + Navy 55% | `#7F5452` | mix | 5.54 | 1.62 |
| 11 | Forever and Ever | Roots Gold 75% + Parchment Cream 25% | `#E0B668` | tint | **1.65** | 5.44 |

**Resolved 2026-10-03 (option A):** the banner text follows "stronger contrast wins", so the
bold Cream figures above are not used — those bands take Navy text (Book 2: Navy 4.59, Book 4:
3.13, Book 6: 3.04, Book 11: 5.44). The colour map itself remains PROPOSED.

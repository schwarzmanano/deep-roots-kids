# Gate 3 — Proof Review

**Book:** made-like-him · **Status:** AWAITING EDITOR — cover and KDP listing not started.
**Proof:** `out/interior.pdf` — 36 pp, every page stamped PROOF - NOT FOR RELEASE.
**Contact sheet:** `qa/gate3-contact.jpg` (rendered from the proof PDF itself).
**Spend:** made-like-him $5.0988 of $6 checkpoint / $10 cap.

## Art — 15/15 chosen
Rounds 1–4 (qa/round1.md, round2.md, this file). Round 3–4 rulings 2026-09-29:
p19 re-scened with fewer vegetables → attempt-12; p23 attempt-06 accepted, Daughter 1 not
at the market. QA: 0 flags. Drift measured against the Gate 2 lock (10.13%); every page
within −37% / +4%. Thin strokes thickened in post on p3, p19, p23, p25, p31.

## Preflight — PASSED
36 pages, even; 8.5×11 trim; fonts embedded (Baloo 2, Lora, Lora Italic); art vector; one
raster (interior logo) at 764 DPI; margins within 0.375" gutter / 0.5" outside.

## Text — release blocked, as intended
`layout.py --release` refuses: 69 problems across 35 units. Every non-Scripture unit except
the title is ai-drafted or empty, pending your words (`plan/my-words.md`, 35 units).
The p33 closing page prints "[ awaiting author's text ]" in the proof.

## Gate 3 rework — limb drift (editor flag 2026-09-30)
Editor flagged volumetric limbs / fingers on p13 p15 p17 p23 p27 p31. Style contract
strengthened (stick-figure construction tied to the Gate 2 lock). One attempt each, $0.557:
none fixed it — hugging, holding and seated poses still render limbs as shapes; p27 also
regained reference bleed. Current picks kept. Spend $5.6557; checkpoint $6 prevents a proper
second round. Diagnosis: the v1 fix (sleeveless + arms held out) is what the Gate 2 lock
used; v2.0 short sleeves combined with contact poses (hug, hold, sit) defeat it.

## Editor text 2026-09-30
35 units inserted verbatim (byte-checked); registered UNRESOLVED pending confirmation that
no AI tool drafted or polished them. No FIT PROBLEM (art height moves ≤16pt).

## 2026-09-30 — text final, limbs fixed, dual-printer interiors
- Text: all units the author's own (confirmed); requested edits only (quotes removed, God's
  pronouns capitalised, p23/p29/p35 wording, p33 heading "Be encouraged!"). Disclosure TEXT: None.
- p27 keeps "you are not a monkey" — editor override of D5, recorded in pages.yaml.
- Limbs: editor-approved sleeveless tops, knee hems, open-arm poses on p13 p15 p17 p23 p27 p31
  (past the $6 checkpoint by instruction). Picks: p13 a5, p15 a4, p17 a6, p23 a8, p27 a4, p31 a7.
  Notes: p15 includes Mother (not in the scene); p27 Son stands rather than kneels.
- Interiors: out/interior.pdf (KDP, 8.5x11 no bleed) and out/interior-lulu.pdf (Lulu, 8.75x11.25,
  0.125 bleed). Both: gutter 0.5 (Lulu safety), K-only black, grayscale flattened logo, no
  transparency, 36 pp. Both preflights PASSED. Spend made-like-him $6.7667.

## 2026-09-30 — hands/feet consistency audit (editor request)
Standard (character bible): hands and feet plain closed ovals — no fingers, no thumb.
Pass: p5 p7 p9 p11 p27 (and p17 after fix). Fail: thumb-bump mittens on p13 p19 p21 p23 p25
p29; pointing index fingers + thumb mittens on p15 p31. Feet: ovals throughout.
generate.mjs --edit-chosen added (edit the chosen image, plan untouched). One edit each, $0.85:
only p17 fixed (-> attempt-08, accepted). Others reproduced the hands; p19 regressed (rejected).
ROOT CAUSE: _brand/cast-sheet.jpg draws thumb-bump mittens; every family page is conditioned
on it. p25-figures-ref.jpg (first-couple pages) draws plain ovals. Spend $7.6179.

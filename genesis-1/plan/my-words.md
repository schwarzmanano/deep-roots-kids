# My Words — Book One, In the Beginning

> INTERNAL WORKSHEET (authorship-policy §8). Pointers, references, requirements and verbatim
> excerpts from your own Dad Teaching Script only. Nothing here is wording for the book, and
> the current AI placeholder text is deliberately NOT shown. Write under **MY TEXT:**; your
> words are inserted verbatim and registered `author: human`, `draft: false`. Problems are
> flagged, never rewritten (§9–§10).


**36 units are `ai-drafted` (refreshed 2026-10-01 from provenance.yaml).** Each is blocked from release until you write it below.

| Page | Unit | Kind |
|---|---|---|
| p2 | `p2.copyright.1` | copyright-page |
| p2 | `p2.copyright.2` | copyright-page |
| p3 | `p3.text` | page-text |
| p3 | `p3.teaching` | teaching |
| p5 | `p5.text` | page-text |
| p5 | `p5.teaching` | teaching |
| p7 | `p7.text` | page-text |
| p7 | `p7.teaching` | teaching |
| p9 | `p9.text` | page-text |
| p9 | `p9.teaching` | teaching |
| p11 | `p11.text` | page-text |
| p11 | `p11.teaching` | teaching |
| p13 | `p13.text` | page-text |
| p13 | `p13.teaching` | teaching |
| p15 | `p15.text` | page-text |
| p15 | `p15.teaching` | teaching |
| p17 | `p17.text` | page-text |
| p17 | `p17.teaching` | teaching |
| p19 | `p19.text` | page-text |
| p19 | `p19.teaching` | teaching |
| p21 | `p21.text` | page-text |
| p21 | `p21.teaching` | teaching |
| p23 | `p23.text` | page-text |
| p23 | `p23.teaching` | teaching |
| p25 | `p25.text` | page-text |
| p25 | `p25.teaching` | teaching |
| p27 | `p27.text` | page-text |
| p27 | `p27.teaching` | teaching |
| p29 | `p29.teaching` | teaching |
| p31 | `p31.text` | page-text |
| p31 | `p31.teaching` | teaching |
| p33 | `p33.body` | closing |
| cover | `cover.series_short` | series-line |
| back cover | `cover.back_blurb` | back-cover-blurb |
| back cover | `cover.spec.1` | back-cover-spec |
| back cover | `cover.spec.2` | back-cover-spec |

Also: `book.title`, `book.series_line`, `book.subtitle` are registered `human`, but their MY TEXT is empty. Under the 2026-10-01 rule (my-words.md is the source of truth) the release guard needs your wording in MY TEXT for them too.


> **2026-10-01 — STATUS LINES.** Each section ends with `**MY TEXT STATUS:**`. The pipeline copied the currently registered text of every human unit into MY TEXT verbatim and marked it `copied: awaiting confirmation`. Change the status to `confirmed` yourself after checking the line, or correct the text and then confirm. The release guard passes a human unit only when the printed text equals MY TEXT AND the status reads exactly `confirmed`. The pipeline never writes `confirmed`.

> **2026-10-02 — BOOK ONE RE-AUTHORING: VERBATIM CANDIDATES (Priority 0).** For each of the 36
> `ai-drafted` units, the pipeline searched your **Dad Teaching Script, Track 1** (the docx you
> named; byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`) and either:
> - **staged a candidate** (14 units): whole sentences, or a contiguous run of whole sentences,
>   copied verbatim and byte-checked against the docx. Status `candidate`, with source paragraph
>   and sentence numbers (¶1 = "Hi, friends…") and any flags. Nothing is confirmed; or
> - **left a gap** (22 units): MY TEXT reads `[SCHWARZ TO WRITE]`, with the page purpose, the WEB
>   text, a length limit and the theological point.
>
> To accept a candidate, change its status to `confirmed`. To replace it, write over it. The
> release guard treats `candidate` exactly like any other unconfirmed status.
>
> **Sources NOT used:** the album **lyrics** (`source/Creation_to_Glorification_LYRICS.pdf`). The
> PDF has no author metadata (macOS print-to-PDF, 2026-09-26) and it sits beside a music-style
> generation brief, so its authorship is uncertain. Track 1's lyrics would otherwise cover stars,
> oceans and "King over everything". Tell me if they're yours and may be used.
> Other tracks of the Dad Teaching Script were not searched (rule: Track 1 only).
>
> **Applies to every slot:** the teaching-line *pointers* (e.g. "Christ the Bread of Life") were
> written to fit the old AI-drafted lines. Track 1 itself has no Christ-forward material. Whether
> Book One's teaching lines keep pointing to Christ is your call (guardrails §2 allows it in text).
> Track 1 writes God's pronouns in lowercase ("he made you"); Book Two capitalised them at your
> request. Both are allowed (guardrails §8 governs quotation only), but the series now differs.

---

### `book.title` — title · p1, cover

- **Pointer:** title of Book One (Gen 1:1 – 2:3). ORIGIN NOT RECORDED — confirm the title is yours, or supply it
- **Soft target:** short title
- **Current status:** `human` (draft: false) — editor confirmation in chat 2026-09-29 ('All are mine')  _(refreshed 2026-10-01 from provenance.yaml)_
- **From your Dad Teaching Script:** no directly relevant passage in this track

**MY TEXT:**

In the Beginning

**MY TEXT STATUS:** confirmed


---

### `book.series_line` — series-line · p1, back cover

- **Pointer:** series placement: Deep Roots Kids · Creation to Glorification · Book One. Origin not recorded
- **Soft target:** one line
- **Current status:** `human` (draft: false) — editor confirmation in chat 2026-09-29 ('All are mine')  _(refreshed 2026-10-01 from provenance.yaml)_
- **From your Dad Teaching Script:** no directly relevant passage in this track

**MY TEXT:**

Deep Roots Kids: Creation to Glorification, Book One.

**MY TEXT STATUS:** confirmed


---

### `book.subtitle` — subtitle · p1, cover

- **Pointer:** what the book is: a coloring book, creation. Origin not recorded
- **Soft target:** short descriptor
- **Current status:** `human` (draft: false) — editor confirmation in chat 2026-09-29 ('All are mine')  _(refreshed 2026-10-01 from provenance.yaml)_
- **From your Dad Teaching Script:** no directly relevant passage in this track

**MY TEXT:**

A Coloring Book of Creation

**MY TEXT STATUS:** confirmed


---

### `p2.copyright.1` — copyright-page · p2

- **Pointer:** copyright notice: year, rights holder, rights reserved
- **Soft target:** legal notice line — your wording
- **Current status:** `ai-drafted` (draft: true) — standard line set in pipeline code (layout.py), now in book.yaml  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Purpose: copyright notice: year, rights holder, rights reserved
  - Length limit: one line, 9 pt Lora
  - Theological point: none — a factual/legal line

**MY TEXT:**

Copyright © 2026 Deep Roots Kids. All rights reserved.

**MY TEXT STATUS:** confirmed

---

### `p2.copyright.2` — copyright-page · p2

- **Pointer:** required Scripture attribution: WEB, public domain (policy §3 — keep)
- **Soft target:** legal notice line — your wording
- **Current status:** `ai-drafted` (draft: true) — standard line set in pipeline code (layout.py), now in book.yaml  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Purpose: required Scripture attribution: WEB, public domain (policy §3 — keep)
  - Length limit: one line, 9 pt Lora; must keep the WEB public-domain attribution (policy §3)
  - Theological point: none — a factual/legal line

**MY TEXT:**

Scripture quotations are from the World English Bible (WEB), which is in the public domain.

**MY TEXT STATUS:** confirmed

---

### `p3.text` — page-text · p3

- **Scripture:** Gen 1:1–2
- **Pointer:** God before everything; the beginning
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶3, sentence 4; also `_brand/album/teaching-script.md` line 19. 22 words. Selected and placed by the pipeline — not reworded, trimmed or merged.

**MY TEXT:**

Before there were mountains, before there were oceans, before there was one single bird singing one single song — there was God.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p3.teaching` — teaching · p3

- **Scripture:** Gen 1:1; Rev 21:5
- **Pointer:** everything begins with God; forward to Christ making all things new
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶2 last sentence + ¶3 sentence 1 (contiguous across the paragraph break; the line break is the source's own — teaching lines print whitespace-collapsed); also `_brand/album/teaching-script.md` line 18, 19. 25 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: "that question" refers back to the sentence before it — both are included, so the run stands on its own.

**MY TEXT:**

Have you ever wondered — who made all of this?
The Bible answers that question in the very first verse of the very first book.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p5.text` — page-text · p5

- **Scripture:** Gen 1:3–5
- **Pointer:** God speaks; light appears
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶4, sentence 6; also `_brand/album/teaching-script.md` line 20. 14 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: **Will fail the WEB release check (§8):** the Scripture quotation is in straight quotes ("…"); §8 requires the WEB's own curly quotes. Changing quote marks is an edit — yours to make or not.
  - FLAG: Spoken phrasing for a page: "in verse 3," and a **double space** after the comma (preserved as in the source).
  - FLAG: WEB Gen 1:3 reads: God said, “Let there be light,” and there was light.

**MY TEXT:**

He said, in verse 3,  "Let there be light" — and there was light.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p5.teaching` — teaching · p5

- **Scripture:** Gen 1:3; John 8:12
- **Pointer:** light from darkness by God's word; Christ the Light of the World
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶4, sentences 2–5; also `_brand/album/teaching-script.md` line 20. 31 words. Selected and placed by the pipeline — not reworded, trimmed or merged.

**MY TEXT:**

God did not need tools. He did not need helpers. He didn't need a hammer or a paintbrush or a whole team of builders. The Bible tells us God simply spoke.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p7.text` — page-text · p7

- **Scripture:** Gen 1:6–8
- **Pointer:** the expanse; waters above and below
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p7 "Day Two — Sky" — the expanse; waters above and below
  - Scripture (WEB, Genesis 1:6–8): [1:6] God said, “Let there be an expanse in the middle of the waters, and let it divide the waters from the waters.” [1:7] God made the expanse, and divided the waters which were under the expanse from the waters which were above the expanse; and it was so. [1:8] God called the expanse “sky”. There was evening and there was morning, a second day.
  - Length limit: one read-aloud sentence, set 13 pt Lora centred under the art (the art shrinks to make room — keep it to one or two lines)
  - Theological point: the expanse; waters above and below

**MY TEXT:**

God placed an expanse between the waters. He called it sky, giving the waters above and below their places.

**MY TEXT STATUS:** confirmed

---

### `p7.teaching` — teaching · p7

- **Scripture:** Gen 1:6–8; 1 Cor 14:33
- **Pointer:** God of order, not confusion
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p7 "Day Two — Sky" — God of order, not confusion
  - Scripture (WEB, Genesis 1:6–8): [1:6] God said, “Let there be an expanse in the middle of the waters, and let it divide the waters from the waters.” [1:7] God made the expanse, and divided the waters which were under the expanse from the waters which were above the expanse; and it was so. [1:8] God called the expanse “sky”. There was evening and there was morning, a second day.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: God of order, not confusion

**MY TEXT:**

God made a good and ordered world. He is not the author of confusion; his wise word gives creation its place and purpose.

**MY TEXT STATUS:** confirmed

---

### `p9.text` — page-text · p9

- **Scripture:** Gen 1:9–10
- **Pointer:** waters gathered; dry ground appears
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶4, sentence 7; also `_brand/album/teaching-script.md` line 20. 14 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: **Theological/§8 flag:** "Let there be land and sea" is set in quotation marks as God's words, but it is not the wording of Gen 1:9 (WEB: “Let the waters under the sky be gathered together to one place, and let the dry land appear;”). web.py will treat it as dialogue (no 4-word match), so it will not block mechanically — the question is yours.

**MY TEXT:**

He also said, "Let there be land and sea" — and it was so.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p9.teaching` — teaching · p9

- **Scripture:** Gen 1:9–10; Ps 40:2
- **Pointer:** solid ground from the deep; Christ the Rock
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p9 "Day Three — Land and Seas" — solid ground from the deep; Christ the Rock
  - Scripture (WEB, Genesis 1:9–10): [1:9] God said, “Let the waters under the sky be gathered together to one place, and let the dry land appear;” and it was so. [1:10] God called the dry land “earth”, and the gathering together of the waters he called “seas”. God saw that it was good.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: solid ground from the deep; Christ the Rock

**MY TEXT:**

God brought dry ground out of the deep, a firm place for life to flourish. In time, Jesus would show that he is the sure Rock on whom his people can stand.

**MY TEXT STATUS:** confirmed

---

### `p11.text` — page-text · p11

- **Scripture:** Gen 1:11–13
- **Pointer:** land brings forth plants and trees
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **FLAG (editor ruling 2026-10-01): AI paraphrase of Scripture: replace with WEB quotation or my teaching line.** (Text QA: p11.text and p21.text open with the same five words.)
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶8, sentence 4; also `_brand/album/teaching-script.md` line 24. 9 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: A prayer of thanks rather than a statement of the Day Three act (Gen 1:11–13).

**MY TEXT:**

Thank you, God, for the flowers and the trees.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p11.teaching` — teaching · p11

- **Scripture:** Gen 1:11–13; John 6:35
- **Pointer:** provision before need; Christ the Bread of Life
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶5, sentences 6–7; also `_brand/album/teaching-script.md` line 21. 16 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: Also names the ocean (Day Three seas are p9; sea creatures p17).

**MY TEXT:**

Who made the wide, deep ocean, and the tallest tree, and the smallest flower? God did.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p13.text` — page-text · p13

- **Scripture:** Gen 1:14–18
- **Pointer:** sun for day, moon for night — plain nouns (DECISION-2)
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶8, sentence 3; also `_brand/album/teaching-script.md` line 24. 9 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: Names the sun only; DECISION-2 page covers sun and moon.

**MY TEXT:**

Thank you, God, for the sun that warms us.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p13.teaching` — teaching · p13

- **Scripture:** Gen 1:14–18; Deut 4:19
- **Pointer:** Day 4: sun and moon are servants, not gods — the Genesis polemic (DECISION-2)
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶6, sentence 2; also `_brand/album/teaching-script.md` line 22. 12 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: Under the 15–35-word soft target (12 words).

**MY TEXT:**

He's not just powerful — he's the King over everything he made.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p15.text` — page-text · p15

- **Scripture:** Gen 1:16
- **Pointer:** the stars, almost in passing
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p15 "Day Four — Stars" — the stars, almost in passing
  - Scripture (WEB, Genesis 1:16): [1:16] God made the two great lights: the greater light to rule the day, and the lesser light to rule the night. He also made the stars.
  - Length limit: one read-aloud sentence, set 13 pt Lora centred under the art (the art shrinks to make room — keep it to one or two lines)
  - Theological point: the stars, almost in passing

**MY TEXT:**

God made the stars too—countless lights scattered across the night sky.

**MY TEXT STATUS:** confirmed

---

### `p15.teaching` — teaching · p15

- **Scripture:** Ps 147:4; Matt 2:9–10
- **Pointer:** Day 4: God names the stars; the star over Bethlehem; Christ the true Light the stars point to
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p15 "Day Four — Stars" — Day 4: God names the stars; the star over Bethlehem; Christ the true Light the stars point to
  - Scripture (WEB, Genesis 1:16): [1:16] God made the two great lights: the greater light to rule the day, and the lesser light to rule the night. He also made the stars.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: Day 4: God names the stars; the star over Bethlehem; Christ the true Light the stars point to

**MY TEXT:**

God knows and names the stars he made. One star guided visitors to the child Jesus, but Christ himself is the true Light: the one to whom the stars, like all creation, point.

**MY TEXT STATUS:** confirmed

---

### `p17.text` — page-text · p17

- **Scripture:** Gen 1:20–21
- **Pointer:** seas filled with creatures, great and small
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p17 "Day Five — Sea Creatures" — seas filled with creatures, great and small
  - Scripture (WEB, Genesis 1:20–21): [1:20] God said, “Let the waters abound with living creatures, and let birds fly above the earth in the open expanse of the sky.” [1:21] God created the large sea creatures and every living creature that moves, with which the waters swarmed, after their kind, and every winged bird after its kind. God saw that it was good.
  - Length limit: one read-aloud sentence, set 13 pt Lora centred under the art (the art shrinks to make room — keep it to one or two lines)
  - Theological point: seas filled with creatures, great and small

**MY TEXT:**

God filled the seas with living creatures, great and small, swimming through the waters he had made.

**MY TEXT STATUS:** confirmed

---

### `p17.teaching` — teaching · p17

- **Scripture:** Gen 1:21; Mark 6:48–51
- **Pointer:** the sea obeys its Maker; Christ walks on it
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p17 "Day Five — Sea Creatures" — the sea obeys its Maker; Christ walks on it
  - Scripture (WEB, Genesis 1:20–21): [1:20] God said, “Let the waters abound with living creatures, and let birds fly above the earth in the open expanse of the sky.” [1:21] God created the large sea creatures and every living creature that moves, with which the waters swarmed, after their kind, and every winged bird after its kind. God saw that it was good.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: the sea obeys its Maker; Christ walks on it

**MY TEXT:**

The sea belongs to God and obeys its Maker. Jesus showed his power over it when he walked on the waves and calmed the storm.

**MY TEXT STATUS:** confirmed

---

### `p19.text` — page-text · p19

- **Scripture:** Gen 1:21–23
- **Pointer:** birds fill the sky
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶5, sentences 4–5; also `_brand/album/teaching-script.md` line 21. 11 words. Selected and placed by the pipeline — not reworded, trimmed or merged.

**MY TEXT:**

Who taught the tiny birds to sing their song? God did.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p19.teaching` — teaching · p19

- **Scripture:** Gen 1:22; Matt 10:29–31
- **Pointer:** God's care for sparrows; worth of His children
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p19 "Day Five — Birds" — God's care for sparrows; worth of His children
  - Scripture (WEB, Genesis 1:21–23): [1:21] God created the large sea creatures and every living creature that moves, with which the waters swarmed, after their kind, and every winged bird after its kind. God saw that it was good. [1:22] God blessed them, saying, “Be fruitful, and multiply, and fill the waters in the seas, and let birds multiply on the earth.” [1:23] There was evening and there was morning, a fifth day.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: God's care for sparrows; worth of His children

**MY TEXT:**

God cares for even the sparrows. How much more does he care for his children, whom he made and welcomes through Jesus?

**MY TEXT STATUS:** confirmed

---

### `p21.text` — page-text · p21

- **Scripture:** Gen 1:24–25
- **Pointer:** the land filled with animals; 'and it was so'
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **FLAG (editor ruling 2026-10-01): AI paraphrase of Scripture: replace with WEB quotation or my teaching line.** (Text QA: p11.text and p21.text open with the same five words.)
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p21 "Day Six — Animals of the Land" — the land filled with animals; 'and it was so'
  - Scripture (WEB, Genesis 1:24–25): [1:24] God said, “Let the earth produce living creatures after their kind, livestock, creeping things, and animals of the earth after their kind;” and it was so. [1:25] God made the animals of the earth after their kind, and the livestock after their kind, and everything that creeps on the ground after its kind. God saw that it was good.
  - Length limit: one read-aloud sentence, set 13 pt Lora centred under the art (the art shrinks to make room — keep it to one or two lines)
  - Theological point: the land filled with animals; 'and it was so'

**MY TEXT:**

God filled the land with animals—large and small, wild and gentle. And it was so, just as God had spoken.

**MY TEXT STATUS:** confirmed

---

### `p21.teaching` — teaching · p21

- **Scripture:** Gen 1:25; Isa 11:6–9
- **Pointer:** animals good; the peaceable kingdom Christ brings
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p21 "Day Six — Animals of the Land" — animals good; the peaceable kingdom Christ brings
  - Scripture (WEB, Genesis 1:24–25): [1:24] God said, “Let the earth produce living creatures after their kind, livestock, creeping things, and animals of the earth after their kind;” and it was so. [1:25] God made the animals of the earth after their kind, and the livestock after their kind, and everything that creeps on the ground after its kind. God saw that it was good.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: animals good; the peaceable kingdom Christ brings

**MY TEXT:**

The animals are part of God’s good creation. The Bible promises a day of peace under Christ’s rule, when God will make all things new.

**MY TEXT STATUS:** confirmed

---

### `p23.text` — page-text · p23

- **Scripture:** Gen 1:24–25
- **Pointer:** every kind of creature on the ground
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p23 "Day Six — Wild Animals" — every kind of creature on the ground
  - Scripture (WEB, Genesis 1:24–25): [1:24] God said, “Let the earth produce living creatures after their kind, livestock, creeping things, and animals of the earth after their kind;” and it was so. [1:25] God made the animals of the earth after their kind, and the livestock after their kind, and everything that creeps on the ground after its kind. God saw that it was good.
  - Length limit: one read-aloud sentence, set 13 pt Lora centred under the art (the art shrinks to make room — keep it to one or two lines)
  - Theological point: every kind of creature on the ground

**MY TEXT:**

God made every kind of creature that moves along the ground, each according to its kind.

**MY TEXT STATUS:** confirmed

---

### `p23.teaching` — teaching · p23

- **Scripture:** Gen 1:25; Matt 10:29
- **Pointer:** each creature given its place; none forgotten by God
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p23 "Day Six — Wild Animals" — each creature given its place; none forgotten by God
  - Scripture (WEB, Genesis 1:24–25): [1:24] God said, “Let the earth produce living creatures after their kind, livestock, creeping things, and animals of the earth after their kind;” and it was so. [1:25] God made the animals of the earth after their kind, and the livestock after their kind, and everything that creeps on the ground after its kind. God saw that it was good.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: each creature given its place; none forgotten by God

**MY TEXT:**

God gave his creatures a place in the world he made. Not one is outside his care: he sees and sustains all that belongs to him.

**MY TEXT STATUS:** confirmed

---

### `p25.text` — page-text · p25

- **Scripture:** Gen 1:26–27
- **Pointer:** people made in God's image, loved (DECISION-5 page)
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶5, sentences 8–9; also `_brand/album/teaching-script.md` line 21. 18 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: Addresses the reader ("you"); the page is the DECISION-5 image-of-God page and the art shows the first man and woman from behind. "Image" is not mentioned.

**MY TEXT:**

And who made you? God did too — and he made you on purpose, because he loves you.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p25.teaching` — teaching · p25

- **Scripture:** Gen 1:27; Col 1:15
- **Pointer:** only people bear the image; Christ the perfect Image renewing broken image-bearers
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶8, sentence 5; also `_brand/album/teaching-script.md` line 24. 15 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: No mention of the image of God (the Gen 1:27 point); about God making "me".

**MY TEXT:**

Thank you, God, for making the whole wide world — and for making me, too.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p27.text` — page-text · p27

- **Scripture:** Gen 1:28–30
- **Pointer:** blessing; every plant and tree given for food
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p27 "Day Six — A Good Gift" — blessing; every plant and tree given for food
  - Scripture (WEB, Genesis 1:28–30): [1:28] God blessed them. God said to them, “Be fruitful, multiply, fill the earth, and subdue it. Have dominion over the fish of the sea, over the birds of the sky, and over every living thing that moves on the earth.” [1:29] God said, “Behold, I have given you every herb yielding seed, which is on the surface of all the earth, and every tree, which bears fruit yielding seed. It will be your food. [1:30] To every animal of the earth, and to every bird of the sky, and to everything that creeps on the earth, in which there is life, I have given every green herb for food;” and it was so.
  - Length limit: one read-aloud sentence, set 13 pt Lora centred under the art (the art shrinks to make room — keep it to one or two lines)
  - Theological point: blessing; every plant and tree given for food

**MY TEXT:**

God blessed the people he had made and gave them plants and trees for food. His world was full of good gifts.

**MY TEXT STATUS:** confirmed

---

### `p27.teaching` — teaching · p27

- **Scripture:** Gen 1:29; John 6:35
- **Pointer:** God's full provision; Christ the Bread from heaven
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p27 "Day Six — A Good Gift" — God's full provision; Christ the Bread from heaven
  - Scripture (WEB, Genesis 1:28–30): [1:28] God blessed them. God said to them, “Be fruitful, multiply, fill the earth, and subdue it. Have dominion over the fish of the sea, over the birds of the sky, and over every living thing that moves on the earth.” [1:29] God said, “Behold, I have given you every herb yielding seed, which is on the surface of all the earth, and every tree, which bears fruit yielding seed. It will be your food. [1:30] To every animal of the earth, and to every bird of the sky, and to everything that creeps on the earth, in which there is life, I have given every green herb for food;” and it was so.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: God's full provision; Christ the Bread from heaven

**MY TEXT:**

God generously provided food for his creatures. Later, Jesus called himself the Bread of Life, the one who gives lasting life to all who come to him.

**MY TEXT STATUS:** confirmed

---

### `p29.teaching` — teaching · p29

- **Scripture:** Gen 1:31; Rev 21:1–5
- **Pointer:** 'very good'; sin broke it; new creation in Christ
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶6, sentence 3; also `_brand/album/teaching-script.md` line 22. 19 words. Selected and placed by the pipeline — not reworded, trimmed or merged.

**MY TEXT:**

Big and small, near and far, it all belongs to him, and it's all good, because he is good.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p31.text` — page-text · p31

- **Scripture:** Gen 2:1–3
- **Pointer:** seventh day; God rests and makes it holy — 'day' left plain (DECISION-6)
- **Soft target:** one read-aloud sentence (no policy target) — or quote the WEB verse verbatim, which makes it public-domain
- **Current status:** `ai-drafted` (draft: true) — Stage 1 plan text written by the AI pipeline  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p31 "Day Seven — Rest" — seventh day; God rests and makes it holy — 'day' left plain (DECISION-6)
  - Scripture (WEB, Genesis 2:1–3): [2:1] The heavens, the earth, and all their vast array were finished. [2:2] On the seventh day God finished his work which he had done; and he rested on the seventh day from all his work which he had done. [2:3] God blessed the seventh day, and made it holy, because he rested in it from all his work of creation which he had done.
  - Length limit: one read-aloud sentence, set 13 pt Lora centred under the art (the art shrinks to make room — keep it to one or two lines)
  - Theological point: seventh day; God rests and makes it holy — 'day' left plain (DECISION-6)

**MY TEXT:**

On the seventh day, God finished his work. He rested from all he had made and made that day holy.

**MY TEXT STATUS:** confirmed

---

### `p31.teaching` — teaching · p31

- **Scripture:** Gen 2:2–3; Matt 11:28; Heb 4:9–10
- **Pointer:** God's rest is blessing, not tiredness; Christ our rest
- **Soft target:** 15–35 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Page purpose: p31 "Day Seven — Rest" — God's rest is blessing, not tiredness; Christ our rest
  - Scripture (WEB, Genesis 2:1–3): [2:1] The heavens, the earth, and all their vast array were finished. [2:2] On the seventh day God finished his work which he had done; and he rested on the seventh day from all his work which he had done. [2:3] God blessed the seventh day, and made it holy, because he rested in it from all his work of creation which he had done.
  - Length limit: 15–35 words (soft), set 9 pt Lora Italic at 88% of the text width
  - Theological point: God's rest is blessing, not tiredness; Christ our rest

**MY TEXT:**

God did not rest because he was tired. His rest showed that his work was complete and good. Jesus invites his people to find their rest in him, and one day they will share the joy of God’s finished new creation.

**MY TEXT STATUS:** confirmed

---

### `p33.body` — closing · p33

- **Scripture:** Gen 1 → Rev 21–22; John 1:9; Col 1:15–16; Heb 4:9–10
- **Pointer:** closing: Day One's light → the Lamb as the city's light; creation made through and for Christ; Creation · Fall · Redemption · Glorification; a question for families
- **Soft target:** 120–200 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **Candidate (2026-10-02):** verbatim from your Dad Teaching Script, Track 1 ¶7 (whole paragraph); also `_brand/album/teaching-script.md` line 23. 52 words. Selected and placed by the pipeline — not reworded, trimmed or merged.
  - FLAG: **Layout:** p33 has no `heading:` slot, so layout.py treats the body's FIRST LINE as the heading (legacy rule). This one-paragraph body would print entirely as a 20 pt heading. Adding a `heading:` unit to p33 (a pages.yaml change) needs your go-ahead; its text would be yours.
  - FLAG: ≈55 words against the 120–200-word soft target.
  - FLAG: Contains straight quotes around "nature." — not Scripture, so §8 does not apply.
  - FLAG: Alternative: ¶7 + ¶8 together (≈115 words), but ¶8's sentences are staged on p11, p13 and p25.

**MY TEXT:**

So here's what I want you to do today, friends. The next time you see a mountain, or hear a bird, or watch the ocean, I want you to remember — that's not an accident. That's not just "nature." That is God, showing you a little piece of how great he is.

**MY TEXT STATUS:** confirmed

_Provenance of this candidate: Dad Teaching Script.docx — iCloud DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/STICK FIGURE PROJECT/ (sha1 789f2bd1…, byte-identical to `_brand/album/source/Dad_Teaching_Script.docx`; created 2026-08-01, last saved 2026-08-04, creator and last editor schwarzmanano@gmail.com). Nothing in the repo history shows AI drafting of this document; authorship-policy §1.3/§1.4 name it as your own. Only your confirmation settles it._

---

### `p35.body` — about-the-author · p35

- **Pointer:** About the Author — facts only, from your own biography: ministry across East Africa, the UK and the US; MDiv, Westminster Theological Seminary; Cornhill Training Course, London; teaching-ministry leadership and assistant pastor in Kampala; youth and children's ministry in London and Kampala; now in Germany with wife and children; why Deep Roots Kids began. Shared file (`_brand/about-the-author.md`) — one text serves every book
- **Soft target:** 80–120 words
- **Current status:** `human` (draft: false) — author's own words — editor confirmation 2026-09-30 ('All the content including the About the Author is human   _(refreshed 2026-10-01 from provenance.yaml)_
- **From your Dad Teaching Script:** no directly relevant passage in this track

**MY TEXT:**


**MY TEXT STATUS:** awaiting your words


---

### `cover.series_short` — series-line · cover

- **Pointer:** front-cover series tag, very short: brand + book number
- **Soft target:** one line
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated (cover copy)  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Purpose: front-cover series tag, very short: brand + book number
  - Length limit: one short line (front cover)
  - Theological point: none — a factual/legal line

**MY TEXT:**

CREATION TO GLORIFICATION • BOOK ONE

**MY TEXT STATUS:** confirmed

---

### `cover.back_blurb` — back-cover-blurb · back cover

- **Pointer:** back cover: what the book is, for whom, what the child does with it
- **Soft target:** 60–100 words
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Purpose: back cover: what the book is, for whom, what the child does with it
  - Length limit: 60–100 words (soft); Phase 3 template may split it into a headline ≤60 characters + synopsis ≤90 words
  - Theological point: back cover: what the book is, for whom, what the child does with it

**MY TEXT:**

What kind of world did God make? In this book, children explore the creation story, noticing the creatures, lights, and gifts God placed in his world. As they read and colour, they discover that creation belongs to God—and that the story leads us to Jesus, the one who sustains his people and makes all things new.

**MY TEXT STATUS:** confirmed

---

### `cover.spec.1` — back-cover-spec · back cover

- **Pointer:** number of illustrations; to colour
- **Soft target:** short spec line
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Purpose: number of illustrations; to colour
  - Length limit: one short line
  - Theological point: none — a factual/legal line

**MY TEXT:**

15 illustrations to color

**MY TEXT STATUS:** confirmed

---

### `cover.spec.2` — back-cover-spec · back cover

- **Pointer:** age band; Scripture translation
- **Soft target:** short spec line
- **Current status:** `ai-drafted` (draft: true) — editor ruling 2026-09-29 (authorship-policy §5/§6): AI-originated  _(refreshed 2026-10-01 from provenance.yaml)_
- **GAP — no verbatim Track 1 source fits this slot.**
  - Purpose: age band; Scripture translation
  - Length limit: one short line
  - Theological point: none — a factual/legal line

**MY TEXT:**

For ages 4–7 · Scripture quotations from the WEB

**MY TEXT STATUS:** confirmed

---

## Sections added 2026-10-01 (units that had no worksheet section)

---

### `p35.heading` — heading · p35

- **Pointer:** About the Author page label

**MY TEXT:**

About the Author

**MY TEXT STATUS:** confirmed


# Authorship, Provenance, AI-Assistance Policy — Kids Coloring Books

> GOVERNANCE TIER: standing series asset, same standing as
> [theology-guardrails.md](theology-guardrails.md), [character-bible.md](character-bible.md)
> and [brand-spec.md](brand-spec.md). Ruled by the editor (Schwarz Martin Manano) 2026-09-29.
> Text below is the editor's own, saved verbatim. Enforced in code by
> `scripts/textunits.py` (registry), `scripts/disclosure.py` (audit) and
> `scripts/layout.py --release` (release guard).

<!-- BODY -->

Core Objective
The published books must contain genuinely human-authored reader-facing prose wherever the text is designated as human-authored.
AI may assist with planning, organization, research, quality assurance, technical production, provenance tracking, and other non-authorial tasks. AI must not generate, rewrite, paraphrase, polish, complete, or stylistically transform prose that will appear in the published books.
Do not optimize the workflow for making AI-generated writing appear human-written. Instead, maintain a provenance trail that accurately reflects how every published text unit originated.
The governing principle is:
AI may help me prepare the work, but it must not become the author of the words I publish as my own.

1. STANDING AUTHORSHIP POLICY
Save this policy as:
kids/_brand/authorship-policy.md
Reference it from:
theology-guardrails.md

1.1 Human authorship
All reader-facing prose in every book must be written by me, Schwarz, unless it is explicitly identified as public-domain Scripture or another legitimately reproduced public-domain text.
This includes:
* teaching lines
* closing pages
* About the Author
* back-cover copy
* footnotes
* explanatory notes
* captions
* title/subtitle text where applicable
* series descriptions appearing inside the book
* copyright-page explanatory prose
* any other reader-facing prose

1.2 AI must not author the prose
The pipeline must never generate prose intended for publication.
AI must not:
* draft a sentence for publication
* rewrite my sentence
* paraphrase my sentence
* improve my sentence
* polish my sentence
* shorten my sentence
* expand my sentence
* complete an unfinished sentence
* generate alternative wording
* suggest synonyms for a sentence intended for publication
* imitate my writing style
* combine fragments into a new sentence
* translate my prose for publication
* restructure my prose while preserving its meaning
* produce a "cleaned-up" version for me to approve
* generate a replacement when my text fails a length or reading-level check
If my text has a problem, flag the problem only.
Do not provide replacement wording.

1.3 Permitted AI assistance
AI may assist with:
* page planning
* Scripture-reference lookup and verification
* theological cross-checking
* identifying possible guardrail conflicts
* counting words
* checking spelling
* checking grammar
* checking reading level
* checking approximate age suitability
* identifying text-length problems
* organizing material I have already supplied
* identifying relevant excerpts from my own previously supplied teaching scripts
* provenance tracking
* disclosure calculations
* layout validation
* preflight checks
* technical production
* image generation and image-editing workflows where separately authorized
* creating internal worksheets that contain pointers rather than publishable prose
AI-generated planning language must never be silently transferred into the published book.

1.4 Stage 1 rule
For each new book, Stage 1 may supply only:
* page plans
* Scripture references
* theological pointers
* themes
* factual requirements
* candidate excerpts from my existing Dad Teaching Script
* exact source locations for those excerpts
* approximate length requirements
* internal production instructions
Stage 1 must not supply sentences intended to appear in the finished book.
Where a theological idea is required, express it as a conceptual pointer, not as publishable prose.

2. SCRIPTURE
Scripture quotations will use the WEB translation where appropriate.
WEB Scripture quotations are to be tagged as:
author: public-domain
The workflow must distinguish clearly between:
* Scripture quotation
* my original prose
* AI-generated placeholder text
* other source material
Do not attribute Scripture to me.

3. NO AI NOTE IN PRINTED PRODUCTS
Remove the paragraph:
"A note on how this book was made"
from the copyright page of every book.
Retain:
* copyright information
* required Scripture attribution
* WEB public-domain attribution
Add:
print_ai_note: false
to the series default in book.yaml.
Do not replace the AI note with a statement falsely claiming that a particular person wrote, edited, or checked material.
Before release, verify that no unauthorized AI-related statement appears on:
* cover
* back cover
* title page
* copyright page
* interior pages
* About the Author
* other reader-facing pages
Remove the AI note from kdp-listing.md unless a marketplace's current disclosure requirements require a disclosure.
Important: Internal provenance and marketplace disclosure are separate systems. Never alter provenance data merely to change an external disclosure answer.

4. INTERNAL TEXT PROVENANCE REGISTRY
Every text unit in every book must be registered in:
provenance.yaml
Each unit must contain:
* page
* kind
* author
* draft
Permitted author values:
* human
* ai-drafted
* public-domain
While a unit is only a placeholder, use:
draft: true
Once I personally supply the final text, use:
author: human
and:
draft: false
Critical provenance rule
A text unit may be changed to human only when the final wording has been supplied by me.
Approval, editing, selecting, or lightly modifying AI-generated wording does not by itself establish human authorship.
Never change provenance tags merely to make a disclosure result more favorable.

5. BOOK ONE PROVENANCE
Register every current text unit in Book One.
This includes:
* teaching line on every illustrated page
* p13 teaching line
* p33 closing
* About the Author
* cover copy
* back-cover copy
* title and series lines
* all other reader-facing prose
Count all units from the actual plan/files and report the number.
Any current text that was generated by AI must remain:
author: ai-drafted
including:
* p13
* any other teaching lines
* existing closing text
* About the Author
* cover/back-cover copy
* any other AI-originated prose
Do not relabel AI-originated text as human merely because it has been reviewed or approved.

6. BOOK TWO PROVENANCE
Register the same categories of text for Book Two, including:
* teaching lines
* Yahweh teaching line
* D2 footnote
* titles/series lines
* other reader-facing text
The Yahweh line currently generated by AI remains:
author: ai-drafted
The Gen 2:25/D2 footnote currently generated by AI remains:
author: ai-drafted
until I supply my own final wording.

7. DISCLOSURE SCRIPT
Create:
scripts/kids/disclosure.py
Usage:
scripts/kids/disclosure.py <book>
The script must calculate the disclosure status directly from provenance.yaml.
Rules:
Text
If any published text unit remains:
author: ai-drafted
then the calculated status must indicate AI-generated/drafted text remains.
Only when every non-Scripture text unit is either:
* human, or
* public-domain
may the text status return None.
Images
Current image production:
* many images are AI-generated
* extensive editing is performed
* this applies to interiors and covers
Record this accurately.
Translations
Current status:
none
Never manipulate provenance data to obtain a preferred disclosure answer.
The disclosure script is an audit tool, not a mechanism for changing authorship.
kdp-listing.md must use the output of this script.

8. MY-WORDS WORKSHEETS
Create:
kids/genesis-1/plan/my-words.md
and:
kids/made-like-him/plan/my-words.md
For every required text unit provide:
* page
* Scripture verse
* one-line theological pointer
* relevant candidate excerpts from my existing Dad Teaching Script
* exact source location
* soft length target
* empty MY TEXT: field
The worksheet must help me write the prose without writing the prose for me.
Length targets
* Teaching line: 15–35 words
* Closing page: 120–200 words
* About the Author: 80–120 words
* Back-cover blurb: 60–100 words
* Footnotes: 1–2 sentences
These are soft limits.
If my supplied text exceeds a limit, report the issue. Do not rewrite it.
Theological pointers
Pointers must contain themes, requirements, and references only.
Do not copy sentences from previously generated drafts.
Example:
Day 4: Christ is the true Light the stars point to.
This is a conceptual pointer, not publishable prose.
Yahweh requirement
Pointer:
Yahweh is God's own covenant name, given to His people.
Do not turn this pointer into a publishable sentence.
D2 footnote requirement
The footnote must communicate two ideas:
1. Adam and Eve are clothed in the illustration as a publishing convention appropriate for young readers.
2. Genesis 2:25 says they were naked and unashamed.
These are theological/content requirements, not wording to reproduce.

9. WHEN I SUPPLY TEXT
When I provide text:
1. Insert my text verbatim.
2. Do not alter punctuation, grammar, spelling, capitalization, or wording unless I explicitly ask for an edit.
3. Set:
author: human
4. Set:
draft: false
5. Re-run disclosure.py.
6. Run spelling, grammar, reading-level, length, and theological-guardrail checks.
7. Report problems only.
8. Do not rewrite the text.
9. Do not provide replacement sentences.
10. Do not silently correct the text.
If the text does not fit the available layout space, report:
FIT PROBLEM
and identify the affected page/unit.
I will decide how to revise my own wording.

10. IMPORTANT BOUNDARY: NO AI POLISHING
Never use a workflow in which I supply rough prose and AI turns it into polished prose that is subsequently labeled human-authored.
If I want editorial assistance, the system may:
* identify errors
* identify ambiguity
* identify repetition
* identify reading-level problems
* identify theological concerns
* identify length problems
But it must not supply replacement wording unless I explicitly change the authorship policy and ask for AI-generated text.
The default workflow is:
AI identifies → Schwarz decides → Schwarz writes → AI checks
not:
AI drafts → Schwarz approves → AI rewrites → publish

11. RELEASE GUARD
Add:
--release
to layout.py.
A release build must fail if any text unit:
* has author: ai-drafted
* has draft: true
* lacks a valid provenance record
* contains an unresolved provenance status
The error must identify:
* book
* page
* text unit
* provenance status
Non-release builds remain available for:
* proofs
* layout testing
* contact sheets
* QA
* preflight
Every non-release PDF must contain the footer:
PROOF - NOT FOR RELEASE
The release build must contain no proof stamp.

12. BOOK ONE RELEASE WORKFLOW
Do not rebuild the Book One interior or cover yet.
Wait until my final human-authored text has been supplied.
Then:
1. insert my text verbatim
2. update provenance
3. run authorship checks
4. run disclosure.py
5. rebuild interior
6. rebuild cover
7. update back-cover copy
8. run both preflights
9. confirm page count
10. confirm even/odd page requirements
11. update kdp-listing.md
12. perform final release audit
Do not modify the existing artwork.
The objective is one final rebuild and one re-upload to KDP after the text is complete.

13. BOOK TWO — CURRENT PRODUCTION STAGE
Continue Round 2:
* 7 pages
* 2 attempts per page
* approximately $1.35 current target
Accepted outfits remain fixed:
* p23 — present family members
* p25 — "another day"
* p31 — sleepwear
Do not regenerate accepted artwork without a specific QA reason.
After Round 2:
1. QA
2. vectorize
3. layout
4. generate non-release proof
5. apply PROOF - NOT FOR RELEASE
6. preflight
7. produce contact sheet
8. stop at Gate 3
Stop rules
Stop production if:
* cumulative generation cost reaches $6 checkpoint
* a page fails QA twice
* any change touches a theological/content guardrail
* any provenance rule is violated
* any release-only condition is encountered prematurely
Do not push past a stop gate without explicit instruction.
Book Two's copyright page follows the policy in Section 3.

14. BOOKS 3–11
For every subsequent book, Stage 1 must follow the same authorship boundary.
Stage 1 may provide:
* page plans
* Scripture references
* theological pointers
* factual/content requirements
* candidate excerpts from my existing Dad Teaching Scripts
* source locations
* soft word-count targets
* internal QA requirements
Stage 1 must not generate prose intended for publication.
The same provenance, disclosure, QA, and release rules apply to Books 3–11.

15. FINAL RELEASE PRINCIPLE
Before any book is released, the system must be able to answer:
Who supplied the words?
For every reader-facing text unit, the answer must be one of:
* Schwarz / human-authored
* public-domain Scripture
* another explicitly documented permitted source
No AI-drafted placeholder may survive into a release build.
The purpose of this workflow is not to make AI-generated writing look human.
The purpose is to ensure that the published prose is actually written by the stated human author, while AI remains a transparent production and quality-assurance assistant.
When uncertain, stop and flag the issue rather than making an authorship assumption.

---

## Amendment A1 — 2026-10-19, ruled by the editor (recorded by the assistant, not the editor's prose)

Occasion: the Creation to Glorification curriculum (Volume 1), whose questions, prayers, activities and
front matter were assembled from the editor's own material — his Dad Teaching Script, his lyrics, his music
brief, and his own planning document for the book (BLUEPRINT.md) — and placed under his approval.

The editor's ruling, in his words: "The questions, prayers, activities and front matter all came from my
material. They do not pass as AI."

Effect on this policy:
1. Text assembled from the editor's own supplied material — scripts, lyrics, briefs, and planning documents
   he authored — and placed with his section-by-section approval is the editor's work. Its provenance is
   recorded as his material (with the source named), and it is NOT tagged `ai-drafted`.
2. `ai-drafted` continues to mean prose with no source in the editor's material. Section 4's "critical
   provenance rule" still applies to that case unchanged.
3. The marketplace text-disclosure answer follows from the provenance so recorded (Section 7): a book whose
   every text unit is the editor's material, Scripture, or a documented permitted source discloses no
   AI-generated text. Image disclosure is unaffected.
4. The provenance file must still name the source of every unit (which script, which lyric, which planning
   document), so that "who supplied the words?" (Section 15) can always be answered.

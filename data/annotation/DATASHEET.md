# Datasheet: Kannada natural romanization and Kanglish (draft, 2026-10-23)

Draft following Gebru et al., "Datasheets for Datasets". Items marked **TBD** must be filled in by Aarnav before
release. Nothing in this file has been released.

## Motivation
- **Purpose.** Human-checked Kannada in Latin script, in two styles: *natural romanization* (Kannada typed in Latin
  letters word for word, as on a phone) and *Kanglish* (Kannada–English code-mixed, as on WhatsApp in Bengaluru), each
  parallel to native-script Kannada and to English. It supports the paper "Shattered Scripts" (evaluation of language
  models on romanized Kannada; the K1–K3 registrations in `RESULTS.md`) and tests whether an LLM's natural
  romanization is as natural as a human's (K3).
- **Created by.** The Shattered Scripts project (lead: Aarnav). **Funding:** TBD (none, if so state it).

## Composition
- **500 items** (`data/annotation/items_v2.jsonl`): 200 IndicSentiment test reviews (Kannada, with the parallel English
  review and a binary sentiment label) and 300 FLORES+ sentences (dev + devtest) that are also in SIB-200 (with the
  SIB topic label). Each item has: native Kannada, English, a Gemini natural-romanization draft, a Gemini Kanglish
  draft, and (after annotation) human ratings and corrected versions.
- **Sampling.**
  - Sentiment: the 200 items of the study's E0 sample (label-stratified, seed 0, 100 per label).
  - FLORES+: 300 drawn at random (seed 0) from the 515 sentences in SIB-200 and in the M4b test half.
  - 100 items (seed 1; 38 sentiment, 62 FLORES) are double-annotated. 40 of these (seed 2; 16 sentiment, 24 FLORES)
    are *blind* items (see below).
  - 2026-10-23: two items whose natural drafts stayed defective after 5 attempts (flores-993,
    indicsentiment-test-245) were replaced by random draws from the same pools (seed 4; flores-546,
    indicsentiment-test-295; every draw logged in `replacement_draws_v1.jsonl`). Neither was double or blind.
- **Sensitive content.** Product reviews and encyclopedic/news sentences; no personal data was added by the project.
  The sources may contain names of public figures and places.
- **Known issues.** 17 of 2,009 FLORES-200 Kannada sentences are not NFC-normalized at source (see `DATA_CARD.md`).
  Romanization has no single correct spelling: two valid versions can differ.

## Sources and licenses
| source | use here | license | status |
|---|---|---|---|
| FLORES+ (`openlanguagedata/flores_plus`, revision e707e62e) | 300 Kannada sentences and their English | CC BY-SA 4.0 | verified on the HF card, 2026-10-07 |
| SIB-200 (`Davlan/sib200`, revision 38977a66) | topic labels of the FLORES items | CC BY-SA 4.0 (card YAML; derived from FLORES-200) | verified, 2026-10-07 |
| IndicSentiment (`ai4bharat/IndicSentiment`, revision dc8f3f66) | 200 Kannada reviews, English, labels | CC0 1.0 (official AI4Bharat release; see note 1) | resolved 2026-10-24 at the official source (not a mirror) |
| Gemini drafts (`gemini-3.5-flash-lite`, temperature 0, prompts `natural_romanization_v1`, `kanglish_v1`) | drafts shown to annotators | Google claims no ownership of generated content (see note 2) | resolved 2026-10-24 (Gemini API Additional Terms) |

**Note 1: IndicSentiment license (checked 2026-10-24).** The dataset card on Hugging Face (`ai4bharat/IndicSentiment`)
states no license. IndicSentiment is one of the new IndicXTREME test sets released by AI4Bharat with IndicBERT v2
(Doddapaneni et al., ACL 2023). The official repository's README (github.com/AI4Bharat/IndicBERT, branch `main`, commit
4890441, "LICENSE" section) says: "All the datasets created as part of this work will be released under a CC-0
license". The README lists IndicSentiment as "A new, multilingual, and n-way parallel dataset for sentiment analysis in
13 Indic languages", so it is one of "the datasets created as part of this work". We therefore record CC0 1.0. CC0 puts
no condition on reuse, so it does not constrain the release. We still cite the paper and name the source.

**Note 2: Gemini API terms (checked 2026-10-24; "Gemini API Additional Terms of Service", ai.google.dev/gemini-api/terms,
"Effective March 23, 2026", page "Last updated 2026-04-28 UTC").**
- Section "Use of Generated Content": "Some of our Services allow you to generate original content. Google won't claim
  ownership over that content. You acknowledge that Google may generate the same or similar content for others and that
  we reserve all rights to do so. As required by the API Terms, you'll comply with applicable law in using generated
  content, which may require the provision of attribution to your users when returned as part of an API call. [...]
  You're responsible for your use of generated content, and for the use of that content by anyone you share it with."
- Section "Use Restrictions": "You may not use the Services to develop models that compete with the Services (e.g.,
  Gemini API or Google AI Studio)."
- Reading (not legal advice): the terms do not forbid publishing generated drafts in a research dataset. The project
  stays responsible for how the drafts are used, including by people it shares them with, and Google keeps the right
  to produce similar text. The competing-models restriction binds the project's own use of the API. Decided by
  Aarnav (2026-10-25): the release card carries a usage note passing this restriction on (see Intended uses). The release
  marks every draft as Gemini output (model, prompt, temperature) and keeps it separate from the human versions.

**Release plan (decided by Aarnav 2026-10-24; not yet released).**
- **Where:** a Hugging Face dataset repository, with this datasheet as the card and the paper citation.
- **License:** CC BY-SA 4.0 for the whole release. The FLORES+-derived items (and their SIB-200 labels) are CC BY-SA
  4.0, which requires share-alike. The IndicSentiment items (CC0, note 1) and the Gemini drafts (no ownership claimed by
  Google, note 2) can be included under CC BY-SA 4.0 without conflict.
- **Constraint from (a):** none, because CC0 imposes no conditions. The card still credits AI4Bharat and links the
  source.
- **Attribution:** the card credits FLORES+ (and the NLLB team), SIB-200, IndicSentiment / IndicXTREME (AI4Bharat), and
  states that the drafts were generated with Gemini (model, prompt version, temperature).
- **Not released:** annotator names or any identifying information (see Annotators).

## Collection and annotation protocol
- **Tool.** An offline HTML page (`annotation/annotate_v2.html`) that writes a CSV after every item; instructions in
  `annotation/instructions/`.
- **Roles (2026-10-23).** Annotator A annotates all 500 items. Annotator B annotates the 100 double items. Rater C
  rates the K3 pairs. Aarnav coordinates only and does not annotate or rate.
- **Standard condition (A on all 500; B on the 60 non-blind double items).** For each draft, the annotator first rates
  it as shown (naturalness 1–5; meaning preserved yes/no), then corrects it. Annotator A's corrections define the
  human-corrected forms.
- **Blind condition (B on 40 items, done first).** B sees only the native Kannada sentence (no English, no drafts) and
  writes the natural romanization and the Kanglish version from scratch. These are the "human" texts for K3.
- **Rater design (K3).** Rater C sees, for each blind item, the native sentence and two versions of each kind (B's text
  and the Gemini draft), source hidden, order randomized per item (seed 3; key kept outside the page), and rates
  naturalness 1–5 only. C sees no drafts or human versions beforehand. The rating page is generated only after B's 40
  blind items are complete.
- **Agreement.** On the 60 non-blind double items: Cohen's kappa (meaning), quadratic-weighted kappa (naturalness), and
  chrF between A's and B's corrections.
- **Annotators.** TBD: number, Kannada background (native/first language, region, age range), how they were recruited,
  compensation, and consent to release their annotations. No identifying information is released.

## Intended uses
- Evaluating language models on romanized and code-mixed Kannada; studying romanization variation; comparing LLM and
  human romanization (as in K3).
- **Not intended for:** training a system that claims to define "correct" Kannada romanization (spelling varies by
  writer); inferring anything about individual annotators.
- **Usage note (Gemini-drafted texts; added 2026-10-25 at Aarnav's decision).** The `*_draft` fields were generated
  with Google's Gemini API (`gemini-3.5-flash-lite`). They may not be used to develop models that compete with
  Google's Gemini services. The Gemini API Additional Terms of Service (ai.google.dev/gemini-api/terms, "Effective
  March 23, 2026", page "Last updated 2026-04-28 UTC"; checked 2026-10-24), section "Use Restrictions", state: "You may
  not use the Services to develop models that compete with the Services (e.g., Gemini API or Google AI Studio)." The
  same terms, section "Use of Generated Content", make the project "responsible for [its] use of generated content,
  and for the use of that content by anyone [it shares] it with", so this note applies to everyone who uses the
  drafts. The texts Annotator B wrote from scratch (blind items) are not Gemini output. Corrected texts start from a
  draft and can keep it unchanged in whole or in part, so the card treats them as covered too.

## Distribution and maintenance
- **Release:** with the paper, on Hugging Face under CC BY-SA 4.0 (see the release plan above); format CSV/JSONL with this
  datasheet. Not distributed before Aarnav says so.
- **Maintainer and contact:** TBD (Aarnav).
- **Errata:** corrections will be logged with dates in the release notes.

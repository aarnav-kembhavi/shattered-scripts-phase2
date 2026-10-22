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
| IndicSentiment (`ai4bharat/IndicSentiment`, revision dc8f3f66) | 200 Kannada reviews, English, labels | **not stated on the source card**; a mirror says CC0-1.0 | **TBD: confirm at source (IndicXTREME release) before release** |
| Gemini drafts (`gemini-3.5-flash-lite`, temperature 0, prompts `natural_romanization_v1`, `kanglish_v1`) | drafts shown to annotators | subject to the Gemini API terms | **TBD: check output-use terms before release** |

Derived text from CC BY-SA sources is released under CC BY-SA 4.0 (share-alike), unless the IndicSentiment check
requires otherwise.

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

## Distribution and maintenance
- **Release:** TBD (with the paper; format CSV/JSONL with this datasheet). Not distributed before Aarnav says so.
- **Maintainer and contact:** TBD (Aarnav).
- **Errata:** corrections will be logged with dates in the release notes.

# Every deviation, amendment, protocol change and clarification in RESULTS.md

Entries whose title matches the keywords `DEVIATION|deviation|AMENDMENT|ADDENDUM|PROTOCOL CHANGE|CLARIFICATION|Corrections?\b|Correction|CHANGE|Target change|NOTE|Note:` (verbatim, with commit and date). Phase 1 first.

## Phase 1

##### PRE-REGISTERED DEVIATIONS AND NEW REGISTRATIONS (2026-10-15, Aarnav's decisions; written before the natural form is scored and before any run below)

RESULTS.md lines 375 to 437; first line committed in `baf4f09` on 2026-10-15 00:56:53 +0530; last line in `baf4f09` on 2026-10-15 00:56:53 +0530; labels from the title and parent heading: registered, amended

`````text
## PRE-REGISTERED DEVIATIONS AND NEW REGISTRATIONS (2026-10-15, Aarnav's decisions; written before the natural form is scored and before any run below)

### E0b calibration (deviation from the 2026-10-14 registration)
Reason: the single content-free input "N/A" broke Qwen2.5 sentiment (Gate 1a; calibrated English 52.0 vs raw 98.5).
- **Primary**: contextual calibration averaged over three content-free inputs, "N/A", "" and "[MASK]" (each placed in
  every field of the template; per-label log-probs averaged over the three, then subtracted), following Zhao et al.
  2021.
- **Fallback rule**: if a model x task's calibrated English accuracy is more than 5 points below its raw English
  accuracy, the whole model x task row (all forms) uses raw scores, and the row is flagged.
- Also reported: raw, and "N/A"-only calibration.
- P1–P3, the informative-cell rule and the McNemar/Holm family are otherwise unchanged and use the primary scores.
- Natural romanization: all 20 defective outputs are retried (same model, prompt, temperature; up to 3 attempts).
  Items whose natural form is still defective afterwards are excluded from every comparison involving the natural
  form (the other forms keep all 200 items); the count is reported.

### Step 3 reclassification
The 2026-10-14 Step 3 result (linear word-identity probes on the tiny models) is recorded as **uninformative**,
not confirmed: the probe saturates after one block at every vocabulary, so the detok layer can only be 0 or 1 and
the split follows layer-0 (tokenizer) accuracy.

### Step 3b: MDL and erasure probes on the 18 E5 tiny models (replaces the saturated measure)
Words: frequent TinyStories validation words that are **>= 3 tokens under vocab 768** (hence also under 256, 384,
512), up to 40 occurrences each, identical across all 18 models.
- **MDL probe** (online code, Voita & Titov 2020): word identity at the word's last token per layer; blocks at
  0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.25, 12.5, 25, 50, 100% of the (shuffled, seed 0) data; first block coded
  uniformly; compression = uniform codelength / online codelength. MDL detok layer = first layer reaching 90% of
  the model's maximum compression; CI by bootstrapping per-item code costs.
- **Erasure probe** (Feucht et al. 2024 style): from the word's last-token state, predict the token at offset −1
  and −2 (only occurrences where that offset is inside the same word), per layer, held-out occurrences. Erasure
  layer = first layer after the peak where accuracy falls below 90% of the peak; erasure magnitude = peak minus
  final-layer accuracy.
- **Q1b**: the seed-mean MDL detok layer moves later as vocab shrinks: confirmed if Spearman(tokens per word,
  MDL detok layer) over the 6 conditions >= 0.8 and the vocab-256 mean exceeds the vocab-4096 mean by more than both
  seed sds; refuted if rho <= 0; else inconclusive.
- **Q2b**: Spearman(seed-mean MDL detok layer, BPB gap vs 4096) >= 0.8 (refuted if <= 0).
- **Q3b (erasure)**: at offset −1, erasure magnitude >= 0.2 in every condition with >= 50 in-word test occurrences
  (assembly then erasure happens), and the erasure layer moves later as vocab shrinks (Spearman >= 0.8 over those
  conditions); refuted if erasure magnitude < 0.05 everywhere.

### Step 2 full run: M1 + M4 on Qwen2.5-1.5B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B (forms English, native, ITRANS)
Data: M1 word probes on Kannada Wikipedia (the ~300 most frequent Kannada words with >= 30 whitespace occurrences;
ITRANS sentences built word by word, so every occurrence is paired) and English Wikipedia for English words; M1 also
reported on the subset of those words that occur in the E0 items. M4 on FLORES+ (dev+devtest, parallel English).
Natural romanization is not in this run (no natural text exists for Wikipedia; FLORES natural is 25% done).
Detok layer per form, three measures: MDL probe (primary), Patchscopes (FragMend setup; per-layer identification
rate), plain linear probe accuracy; each = first layer reaching 90% of the form's maximum. Erasure probe as above.
Alignment layer = first layer reaching 90% of maximum retrieval accuracy@1 vs English; linear CKA reported. Lag =
alignment layer minus MDL detok layer. Layers are compared within a model; across models as a fraction of depth.
CIs: bootstrap over words (Patchscopes), items/occurrences (probes, MDL), sentences (M4); native vs ITRANS
differences use paired bootstraps over the shared words/sentences.
- **H1 (meaning bottleneck)**: in both Qwen models, ITRANS detokenizes no later than native (MDL detok difference
  CI includes 0 or is negative) **and** has a larger lag than native (paired CI of lag difference excludes 0), or
  never reaches native's maximum retrieval accuracy.
- **H2 (assembly bottleneck)**: in both Qwen models, ITRANS detokenizes later than native (MDL detok difference CI
  excludes 0, positive) despite fewer tokens per word.
- **H3 (fragmentation-driven ordering)**: in every model the sign of (ITRANS − native MDL detok layer) matches the
  sign of (ITRANS − native tokens per word): negative in the Qwen models, positive in Sarvam-1 and Gemma 4, with the
  CI excluding 0 in at least 3 of 4 models. Refuted if ITRANS is later than native in all 4 models (that pattern
  supports familiarity, i.e. H2).
H1 and H2 are mutually exclusive on the Qwen detok comparison; if neither holds the outcome is inconclusive.
Disagreements between MDL, Patchscopes and the plain probe about the ordering are reported, not resolved.

---
`````

##### DEVIATIONS AND NEW REGISTRATIONS (2026-10-16, Aarnav's decisions; written before any run below)

RESULTS.md lines 693 to 740; first line committed in `e10b11e` on 2026-10-16 00:19:31 +0530; last line in `d8e2bd8` on 2026-10-16 00:49:27 +0530; labels from the title and parent heading: registered, amended

`````text
## DEVIATIONS AND NEW REGISTRATIONS (2026-10-16, Aarnav's decisions; written before any run below)

### Recorded deviations
- **(a) Primary M1 measure switched from Patchscopes to MDL.** The 2026-10-07 registration made Patchscopes
  primary. In the full run, Patchscopes identifies 0–7% of Kannada words in either script (native 0.0–0.7% in
  Qwen2.5, Qwen3.5 and Gemma 4; ITRANS 0.7–6.7% in all four). The one exception is Sarvam-1 native at 77%. So the
  registered Patchscopes Delta cannot be computed (0–2 words identified in both forms per model). MDL (online code)
  is the primary mechanism measure from here on, as the 2026-10-15 registration already stated for H1–H3.
  The Patchscopes failure is reported as a finding, not hidden. FragMend (arXiv 2604.16656, §6.5) reports that
  "smaller LMs are disadvantaged at detokenization" (fewer parameters per language; "fewer layers reduces the
  search space for detokenization") and hypothesizes "that detokenization improves with model scale". Their smallest
  scale point is Qwen3.5-0.8B, and they report weaker gains rather than outright failure. Our 1.5–2B models fail
  almost completely on Kannada while succeeding on English (61–98%).
- **(b) The "never reaches native's maximum retrieval" test in H1 was operationalized after seeing the maxima**
  (paired CI of native max minus ITRANS max retrieval above 0). The run log had printed the maxima before the
  analysis script was written. The gaps (0.088 to 0.876) are large enough that the verdict does not hinge on the
  choice, but the test is not pre-registered in its exact form.
- **(c) CIs for M1 are recomputed clustered by word** (resampling the 300 words with all their occurrences, not
  occurrences), for the large models and the 18 tiny models. Word-clustered CIs are primary; the occurrence-level
  CIs are kept alongside. M4 CIs stay over sentences (the unit of M4). The tiny models' per-item MDL costs were not
  saved in Step 3b, so the 18 MDL probes are recomputed (same words, seeds and settings) and the point estimates are
  checked against the stored ones.

### PRE-REGISTRATION — M4b linear mapping test (written 2026-10-16, before any mapping is fitted)
Question: is the poor ITRANS-to-English retrieval a misalignment that a linear map can repair (the meaning is in the
representation but in a different subspace) or is the meaning missing (strong H1)?
- Data: the cached FLORES+ sentence vectors from the full run (2,009 sentences, mean-pooled residual stream, every
  layer; `cache/activations/m14full`). Forms: native and ITRANS (natural is added later on a random 500 sentences,
  with the same procedure, reported separately). One random 50/50 split (seed 0; 1,004 train / 1,005 test), the same
  for every model, form and layer.
- Map: ridge regression from the form's vectors to the English vectors at the same layer (both centered with
  train-half means). The ridge strength is chosen per model, form and layer by 5-fold CV on the train half, using CV
  retrieval acc@1. The grid is lambda = alpha × mean squared row norm of the training features, alpha in {1e-3, 1e-2,
  1e-1, 1, 10, 100}.
- Retrieval: acc@1 by cosine among the 1,005 test English sentences (chance 0.1%). The **best layer is chosen on the
  train half** (CV retrieval for mapped, train-half retrieval for unmapped) and evaluated once on the test half. The
  full per-layer test curves are reported too. Unmapped retrieval is reported on the same test half, side by side.
- Control: the same ridge fitted on shuffled train pairs (expected near chance).
- CIs: 10,000 paired bootstrap resamples over test sentences.
- **Prediction (strong H1): mapped ITRANS retrieval stays well below mapped native.** Per model, at each form's
  best layer: "gap persists" if the CI lower bound of (mapped native − mapped ITRANS) is above 0.10; "gap closes" if
  the CI upper bound is below 0.10; otherwise "partial". Strong H1 is **supported** if the gap persists in all four
  models, **refuted** if it closes in at least three, and **inconclusive** otherwise. Also reported: the share of the
  unmapped native−ITRANS gap that remains after mapping, and whether mapping raises ITRANS above unmapped ITRANS.
- Not a test: the accuracy-vs-mechanism figure (sentiment accuracy vs tokens per word and vs best-layer
  retrieval, 4 models × {native, ITRANS}) is illustrative only (n = 8 points, no inference).

---
`````

##### 2026-10-16 — Word-clustered CIs for M1 (large and tiny models; deviation (c) above)

RESULTS.md lines 741 to 759; first line committed in `d8e2bd8` on 2026-10-16 00:49:27 +0530; last line in `d8e2bd8` on 2026-10-16 00:49:27 +0530; labels from the title and parent heading: none

`````text
## 2026-10-16 — Word-clustered CIs for M1 (large and tiny models; deviation (c) above)

Scripts: `scripts/m14_gate2.py` (rerun; clustered CIs are now primary, occurrence CIs kept with suffix `_occ`) and
`scripts/m1_tiny_mdl.py --items` (recomputed the 18 tiny MDL probes and saved per-item costs; outputs
`results/m1_tiny_mdl/{items_v*_s*.npz, clustered.csv}`). 10,000 resamples of the 300 words.
- **Tiny models:** all 18 recomputed detok layers equal the stored ones. The word-clustered CIs equal the occurrence
  CIs in 17 of 18 runs (all degenerate: 2 / 1 / 1 / 1 / 1 / 0 for vocab 256 / 384 / 512 / 768 / 1024 / 4096). The
  exception is v1024 seed 0, which widens from [1, 1] to [1, 2]. The Step 3b classification is unchanged.
- **Large models, MDL detok ITRANS − native (word-clustered [occurrence]):**
  - Qwen2.5 −3 [−4, −3] [−4, −3]
  - Qwen3.5 0 [0, 0] [0, 0]
  - Sarvam-1 +6 [5, 7] [6, 7]
  - Gemma 4 +2 [1, 2] [1, 2]

  On the E0-word subset, Gemma 4 widens to +1 [0, 2] (occurrence [1, 2]), now including 0. The others are unchanged.
  Per-form detok CIs are unchanged except Sarvam-1 native, which goes to [0, 1]. Lag differences: Sarvam-1 0 [−1, 1]
  (occurrence [−1, 0]), the others unchanged. **H1–H3 verdicts and the method-agreement table are unchanged.**

---
`````

##### ADDENDUM to the K1–K3 registration — annotation agreement (written 2026-10-17, Aarnav's decision of 2026-10-16; before any draft exists)

RESULTS.md lines 1033 to 1048; first line committed in `6a00276` on 2026-10-17 02:01:14 +0530; last line in `e56a80e` on 2026-10-17 02:17:11 +0530; labels from the title and parent heading: amended

`````text
## ADDENDUM to the K1–K3 registration — annotation agreement (written 2026-10-17, Aarnav's decision of 2026-10-16; before any draft exists)
- **Rating and correction.** Ratings (naturalness 1–5, meaning preserved yes/no) apply to the Gemini draft as shown,
  **before** correction. This is unchanged.
- **Human versions.** The primary annotator's corrections define the human-corrected forms used in K1–K3.
- **Second annotator.** They also rate and correct independently on the 100 double items.
- **Agreement on corrections.** For the two annotators' corrected versions of each item, sentence-level chrF
  (sacrebleu, chrF with character order 6, word order 0, β = 2). Reported:
  - the mean over the 100 items with a bootstrap CI (10,000 resamples);
  - computed separately for natural and Kanglish.
- **Edit size.** Each annotator's chrF between the Gemini draft and their own correction is also reported, as how
  much was changed.
- **Kappas, as registered.** Cohen's kappa (meaning) and quadratic-weighted kappa (naturalness), separately for
  natural and Kanglish.
- **No decision rule.** Agreement is descriptive and does not feed K1–K3.

---
`````

##### ADDENDUM to the surface-baseline registration — natural form (written 2026-10-21, at Aarnav's request; before computing)

RESULTS.md lines 1189 to 1199; first line committed in `7d86cfc` on 2026-10-21 22:22:48 +0530; last line in `d7693f7` on 2026-10-21 22:25:39 +0530; labels from the title and parent heading: amended

`````text
## ADDENDUM to the surface-baseline registration — natural form (written 2026-10-21, at Aarnav's request; before computing)
Script `scripts/m4c_surface.py`, CPU only.
- **Data:** the M4c sample, 496 retained FLORES+ sentences, with M4c's 50/50 split (seed 0), its folds and the M4b
  ridge grid.
- **Measures:** for native, ITRANS and natural in each of the 4 models, L0, Lb and gain, exactly as in (a) above.
  Ridge only.
- **Rule:** the same as in (a). Beyond surface if the gain's CI lower bound > 0.10, surface-level if its upper bound
  < 0.10, otherwise partial.
- **Not blind:** the M4c summary, with its best mapped layers, was already seen.

---
`````

##### 2026-10-22 — Corrections (Aarnav)

RESULTS.md lines 1301 to 1318; first line committed in `9710f74` on 2026-10-22 01:00:43 +0530; last line in `93a9f68` on 2026-10-22 01:03:02 +0530; labels from the title and parent heading: amended

`````text
## 2026-10-22 — Corrections (Aarnav)
- **Familiarity definition of 2026-10-15 (Gate 1 entry), corrected.** That note said natural romanization "scores
  about the same as ITRANS", which "supports reading the native-script advantage as pretraining exposure rather than
  everyday use". On accuracy (Gate 1) all romanized forms were well below native, but on meaning alignment M4c
  contradicts the natural ≈ ITRANS part:
  unmapped retrieval against English is natural > ITRANS by +0.23 to +0.32 in all 4 models
  (`results/m4c_natural/summary.csv`). **Familiarity is graded: native > natural romanization > ITRANS on alignment.**
  "Familiarity" still means exposure in pretraining corpora; natural romanized Kannada plausibly appears in web text
  (chats, comments, lyrics), ITRANS rarely. Not tested here: we have no corpus counts of either form. The 2026-10-15
  note is kept as written; this entry supersedes its last sentence.
- **M4c mapped measure: unreliable at this sample size; unmapped is primary for M4c.** With 248 training sentences the
  ridge map lowers retrieval below unmapped in most cells, including native, which is already aligned (native
  unmapped → mapped: Qwen3.5 1.000 → 0.952, Sarvam-1 0.988 → 0.843, Gemma 4 1.000 → 0.944;
  `results/m4c_natural/summary.csv`). So the mapped column of M4c, and any verdict that would rest on it, is weak
  evidence. The registered M4c verdict (refuted, on the unmapped measure) stands; the M4c entry already states both
  readings.

---
`````

##### 2026-10-22 — Correction: lossy vs ITRANS tokens-per-word ranges (2026-10-21 exploratory note)

RESULTS.md lines 1390 to 1402; first line committed in `cd6a097` on 2026-10-22 02:14:18 +0530; last line in `42c9bac` on 2026-10-22 02:14:54 +0530; labels from the title and parent heading: amended, exploratory

`````text
## 2026-10-22 — Correction: lossy vs ITRANS tokens-per-word ranges (2026-10-21 exploratory note)
The 2026-10-21 note ("Exploratory note: lossy > ITRANS is confounded") says lossy has fewer tokens per word than ITRANS
"by 0.66–0.89 on E0b sentiment/XNLI and 0.78–0.98 on SIB-200". The SIB-200 range is wrong at both ends by 0.01, and so
the overall range is wrong at its top. Stored values (ITRANS − lossy tokens per word; found by
`paper/scripts/check_numbers.py`, claim 12a):
- **E0b sentiment and XNLI** (`results/e0b_familiarity/gate1/fertility.csv`, 10 model × task cells): 0.657–0.891, so
  0.66–0.89 (unchanged, correct).
- **SIB-200** (`results/e0c_sib/gate/accuracy.csv`, column `tokens_per_word`, 5 models): 0.774 (Qwen2.5 and Qwen3, same
  tokenizer) to 0.974 (Sarvam-1), so **0.77–0.97**, not 0.78–0.98.
- **Overall** (15 cells): 0.657–0.974, so **0.66–0.97**.
The original note is left as written; this entry supersedes its SIB-200 range. No verdict depended on these ranges.

---
`````

##### 2026-10-22 — Note: back-translation summary key renamed (no value changed)

RESULTS.md lines 1403 to 1413; first line committed in `42c9bac` on 2026-10-22 02:14:54 +0530; last line in `8d7db7d` on 2026-10-22 02:16:28 +0530; labels from the title and parent heading: none

`````text
## 2026-10-22 — Note: back-translation summary key renamed (no value changed)
In `results/e0b_natural_check/summary_control.json` the final back-translation numbers (native 0.838, natural 0.621,
gap 0.217 [0.201, 0.234], n = 576; RESULTS.md 2026-10-15 "final" entry) sit under the key
`gap_all_controlled_BIASED_UPWARD_by_selection`. That name dates from the interim run, when the 24 lowest-similarity
texts had been controlled first, so the controlled set was selected and the gap biased upward. In the full run every
one of the 576 eligible texts is controlled (`complete_all_paired: true`), so there is no selection and no such bias.
A key `gap_all_controlled` with the identical block was added (copied programmatically from the old key, not
recomputed); the old key is kept. `scripts/e0b_backtranslate_control.py` now writes both, and
`paper/NUMBERS.md` points to the new key.

---
`````

##### PRE-REGISTRATION — K3 revised: blind human-written vs Gemini natural romanization; annotation deviations (written 2026-10-22, Aarnav's design; before any annotation exists and before the page is distributed)

RESULTS.md lines 1462 to 1507; first line committed in `5715d3e` on 2026-10-22 02:23:42 +0530; last line in `c1f9aa7` on 2026-10-22 02:24:23 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — K3 revised: blind human-written vs Gemini natural romanization; annotation deviations (written 2026-10-22, Aarnav's design; before any annotation exists and before the page is distributed)

### Deviations from the K1–K3 registration (2026-10-16) and its addendum (2026-10-17)
- **(a) Defective natural drafts re-asked beyond attempt 3.** 5 natural drafts were still defective after attempts 1–3
  (leftover Kannada script, CJK characters, or "ā"). Each got attempts 4–5 (same model, prompt, temperature;
  `scripts/k_annotation.py regen`, output `data/annotation/drafts_regen_v1.jsonl`). Clean after regeneration: flores-1113
  (attempt 4), flores-931 (attempt 5), indicsentiment-test-991 (attempt 4). **Still defective, flagged for Aarnav to fix
  by hand:** flores-993 (one word left in Kannada script) and indicsentiment-test-245 ("bāsigeya"). Hand fixes go in
  `data/annotation/drafts_manual_v1.jsonl` and override every Gemini draft on the page. The E0 natural file
  (`data/processed/natural_e0_v1.jsonl`, Gate 1 data) is not changed. The draft shown to annotators is recorded per
  item, so K1–K3 know which text was rated.
- **(b) Blind condition.** 40 of the 100 double-annotated items, chosen at random: `numpy.random.default_rng(2)
  .choice(100, 40, replace=False)` over the double items in `items_v1.jsonl` order (`scripts/k_annotation.py blind`,
  ids in `data/annotation/blind_v1.json`; 16 sentiment, 24 FLORES). For these, the **second annotator sees only the
  native Kannada sentence** (no English, no drafts) and writes the natural romanization and the Kanglish version from
  scratch; no draft ratings. The page (`annotation/annotate_v2.html`) puts the 40 blind items first in the second
  annotator's list, so they are written before any Gemini draft is seen. The primary annotator sees these items
  normally (drafts, ratings, corrections), as for every item.
- **(c) Agreement on 60, not 100.** Cohen's kappa (meaning), quadratic-weighted kappa (naturalness) and chrF between
  the two annotators' corrections are computed on the 60 non-blind double items (the second annotator neither rates
  nor corrects drafts on the blind 40).

### K3 (replaces the 2026-10-16 K3): Gemini natural romanization vs human-written, on the 40 blind items only
- **Texts:** for each blind item, the second annotator's from-scratch natural romanization ("human") and the Gemini
  natural draft shown on the page ("Gemini").
- **Measure 1, chrF** (sacrebleu chrF, char order 6, word order 0, β = 2) of Gemini against human, per item; mean with a
  bootstrap CI (10,000 resamples over the 40 items). Reported alongside, as a reference for how much two human
  romanizations differ: chrF between the two annotators' corrected natural versions on the 60 non-blind items.
- **Measure 2, naturalness rated by Aarnav:** a separate rating page shows each blind item's native sentence and the
  two versions, **in random order (seed 3, fixed per item) with the source hidden**; Aarnav rates each version's
  naturalness 1–5. Paired difference (human − Gemini) per item; mean with a bootstrap CI (10,000 over items).
- **Decision rule (proposed by Claude Code 2026-10-22; to be confirmed by Aarnav before any blind item is written):**
  on Measure 2, **K3 holds** ("Gemini's natural romanization is about as natural as a human's") if the CI of the mean
  difference lies within ±0.5 rating points; **human more natural** if the CI lower bound is above +0.5; **Gemini more
  natural** if the upper bound is below −0.5; otherwise **inconclusive**. Measure 1 has no threshold (two valid
  romanizations can differ in spelling) and is reported descriptively next to the human–human reference.
- **Stated limitations, now:** n = 40, so the CI is wide. Aarnav will have seen (and corrected) the Gemini drafts of
  these items in his own pass, which can unblind the rating; to limit this, the rating should be done **before**
  Aarnav annotates those 40 items, or else this is reported as a caveat. Kanglish blind texts are rated the same way
  and reported descriptively (no K3 rule).
- **The other 60 double items:** reported descriptively only (the second annotator's ratings of the drafts, draft vs
  correction chrF, agreement with the primary annotator).
- **The 2026-10-16 K3 test** (human-corrected vs Gemini natural accuracy within ±5 points on the 200 sentiment items)
  is **no longer a registered test**; if that scoring is run it is reported as descriptive.

---
`````

##### 2026-10-22 — NC1 deviations; gate approved (Aarnav)

RESULTS.md lines 1761 to 1769; first line committed in `83084bc` on 2026-10-22 20:21:26 +0530; last line in `0221b44` on 2026-10-22 20:27:55 +0530; labels from the title and parent heading: none

`````text
## 2026-10-22 — NC1 deviations; gate approved (Aarnav)
- **(c) re-split share below the registered gate:** on the M4c pilot sentences (c) re-split 79.4% (262/330) of
  multi-token words, below the registered 80% (sentiment 87.7%). Cause: vocabulary — for the remaining words the
  canonical split is the only k-piece segmentation at the canonical count. Aarnav approved the gate; NC1 proceeds as
  registered, threshold unchanged.
- **Sarvam-1 byte fallback:** 36 of 135,816 lossy tokens are byte-fallback tokens (non-ASCII punctuation in the sources);
  units containing them stay canonical in every condition and are flagged `atomic_token` (other tokenizers: 0).

---
`````

##### 2026-10-23 — Annotation deviations: roles, replacement of the two defective items (Aarnav; before any annotation exists and before any page is distributed)

RESULTS.md lines 1970 to 1988; first line committed in `7d88f63` on 2026-10-23 00:22:30 +0530; last line in `7d88f63` on 2026-10-23 00:22:30 +0530; labels from the title and parent heading: none

`````text
## 2026-10-23 — Annotation deviations: roles, replacement of the two defective items (Aarnav; before any annotation exists and before any page is distributed)
- **Roles.** Aarnav is not an annotator or rater (not fluent enough); Aarnav coordinates only. **Annotator A** does all
  500 items (Aarnav may later split this 250/250 between A1 and A2; if so it is logged before it happens).
  **Annotator B** does the 100 double-annotated items, the 40 blind items first (native sentence only, as registered).
  **Rater C** (independent; sees no drafts and no human versions before rating) rates the 40 blind pairs. "Primary
  annotator" in the K1–K3 registrations means Annotator A; "second annotator" means Annotator B.
- **K3 amended.** Measure 2 in the 2026-10-22 K3 revision ("naturalness rated by Aarnav") is superseded: Rater C rates,
  as in the 2026-10-22 K3 addendum. Any fallback in which Aarnav rates is removed. **If no independent rater is
  available, K3 is reported descriptively with no verdict** (unchanged from the addendum). The limitation about
  Aarnav's own pass unblinding the rating no longer applies (Rater C sees no drafts); Annotator A sees the Gemini
  drafts of the blind items, but A neither writes the blind texts nor rates them.
- **flores-993 and indicsentiment-test-245 are replaced, not hand-fixed** (supersedes "flagged for Aarnav to fix by
  hand" in deviation (a) of 2026-10-22). Two replacement items are drawn at random with a fixed, logged seed from the
  same source pools (FLORES+ dev+devtest; IndicSentiment test), excluding every item already in any study sample. Drafts
  come from the identical Gemini prompt; any draft with a non-Latin character fails and triggers a new draw, and every
  draw is logged. Each replacement inherits the double-annotated and blind status of the item it replaces. Then the page
  is rebuilt, 0 flagged drafts confirmed and the CSV round trip retested (Phase B; not done yet).

---
`````

##### 2026-10-25 17:05 IST — PROTOCOL CHANGE: annotation format HTML page → Excel (.xlsx) (Aarnav's decision; before anything is sent)

RESULTS.md lines 2622 to 2644; first line committed in `e9c40b3` on 2026-10-25 17:04:54 +0530; last line in `57218d6` on 2026-10-25 23:44:26 +0530; labels from the title and parent heading: amended

`````text
## 2026-10-25 17:05 IST — PROTOCOL CHANGE: annotation format HTML page → Excel (.xlsx) (Aarnav's decision; before anything is sent)
Nothing had been sent to any annotator or rater (the HTML packages were never distributed).
- **Change.** Annotators A and B, and later Rater C, work in Excel workbooks instead of the offline HTML pages
  (`annotation/annotate_v2.html`, `annotation/template_rater_v1.html`). The tasks are unchanged: the same items
  (`data/annotation/items_v2.jsonl`, with the logged replacements flores-546 and indicsentiment-test-295), the same
  blind set (`blind_v1.json`, 40 items, written first and from scratch), the same drafts (as shown on the page,
  `k_annotation.shown_drafts`), the same fields and options (naturalness 1–5, meaning yes/no, corrected text, note;
  for C naturalness 1–5 of each version), and the same rating-before-correcting instruction.
- **Reason.** Annotator convenience and offline use: Excel is familiar, works without a browser, and the file is the
  saved work.
- **Consequence.** Per-item timing is no longer recorded: the page wrote a timestamp per saved item (`saved_at`);
  the merge script (`annotation/merge_xlsx.py`) fills `saved_at` with the workbook's last-saved time, the same for
  every row of a file. The merge writes the same CSV format the page wrote, so downstream code is unchanged.
  Workbooks are protected without a password (to prevent accidents only); answers are checked by the merge script
  (IDs, required cells, valid values) and cells that look auto-corrected are flagged for Aarnav to check with the
  annotator (never fixed automatically).
- **B's items are split in two workbooks** so that B's first file contains no Gemini draft at all (the HTML page held
  every draft, including those of the blind items, in its embedded data): part 1 = the 40 blind items (native text
  only); part 2 = the other 60 double items with drafts, released under the existing rule for B's part 2 (after B's
  40 blind items are in and A has confirmed the worked examples).
- **No registered prediction changes** (K1, K2, K3, K3b and their addenda stay as registered).

---
`````

##### 2026-10-26 00:40 IST — PROTOCOL CHANGE: annotation "rate + correct" → "verify" (Aarnav's decision; before any valid annotation is returned)

RESULTS.md lines 2760 to 2780; first line committed in `acce939` on 2026-10-26 00:37:48 +0530; last line in `0ed79cc` on 2026-10-26 00:50:54 +0530; labels from the title and parent heading: amended

`````text
## 2026-10-26 00:40 IST — PROTOCOL CHANGE: annotation "rate + correct" → "verify" (Aarnav's decision; before any valid annotation is returned)
No annotation exists: nothing has been returned by any annotator.
- **Change.** Annotators verify the Gemini drafts instead of rating and correcting them: for each draft, **fine**
  (how people would type it on WhatsApp, and keeps the meaning) or **wrong**, with their fix. The verified text is the
  draft if fine, the fix if wrong. The naturalness 1–5 and meaning yes/no ratings are dropped. Annotator B still
  types the 40 blind items from scratch (native sentence only, before seeing any draft), unchanged. **Rater C is
  dropped.**
- **Reason.** Annotator time. Anchoring on the draft is no longer avoided by design; it is measured on B's blind 40
  (B's from-scratch text vs the Gemini draft and vs A's verified text).
- **Items, drafts, blind set, double set, seeds:** unchanged.
- **No decision rule or threshold changes.** How each registered prediction is affected:

| prediction | status after this change |
|---|---|
| K1 (Kanglish beats natural) | applies, rule unchanged, with the data label "human verified Gemini romanization" in place of "human-corrected" (A's verified natural and Kanglish); Gemini drafts stay the secondary comparison |
| K2a, K2b (more English, better) | apply, rules unchanged, on "human verified Gemini romanization" Kanglish |
| K3 (blind human vs Gemini natural; independent rater, TOST) | **descriptive, no verdict**, per the registered rule "if no independent rater is available, K3 is reported descriptively". No naturalness ratings exist, so the descriptive report is chrF Gemini vs B's blind text (with the human-human reference, A verified vs B verified on the 60, noted as biased upward), plus the anchoring measures and the K3b statistics for B's blind 40 vs Gemini on the same items (vowel doubling, h-digraphs, English-word share ratios with 90% CIs, as K3b; descriptive, no rule; added 2026-10-26 01:00, Aarnav) |
| K3b, K3b-hi (Dakshina) | apply as registered; no annotation involved (K3b already reported) |
| Agreement addendum (2026-10-17) | descriptive as before; kappas on naturalness and meaning cannot be computed (no ratings) and are replaced by Cohen's kappa on fine/wrong (A vs B, 60 items); chrF between A's and B's verified texts and draft-to-verified edit size as registered |

---
`````

##### 2026-10-26 03:10 IST — PROTOCOL CHANGE: Annotator A is a pool of about 50 people (Aarnav)

RESULTS.md lines 2881 to 2888; first line committed in `d5c0167` on 2026-10-26 03:13:39 +0530; last line in `d5c0167` on 2026-10-26 03:13:39 +0530; labels from the title and parent heading: amended

`````text
## 2026-10-26 03:10 IST — PROTOCOL CHANGE: Annotator A is a pool of about 50 people (Aarnav)
- **A = a pool of about 50 native Kannada speakers** who together verified the 500 items in one workbook
  (`annotation/xlsx/annotator_A_filled.xlsx`, file time 2026-10-26 02:57). There are no per-item annotator IDs.
- **Consequences:** agreement within A cannot be computed; A vs B agreement (kappa on fine/wrong, 60 items) compares
  B with a pool, not with one person; "Annotator A" in K1–K3 and the agreement addendum now means this pool. Consent
  and the datasheet entries are per pool (to be filled by Aarnav in `data/annotation/DATASHEET.md`).
- No decision rule or threshold changes.

`````

##### 2026-10-27 01:50 IST — Target change: TMLR (Aarnav)

RESULTS.md lines 3130 to 3145; first line committed in `01496f7` on 2026-10-27 01:48:09 +0530; last line in `2a9fec3` on 2026-10-27 02:45:12 +0530; labels from the title and parent heading: none

`````text
## 2026-10-27 01:50 IST — Target change: TMLR (Aarnav)
- **Venue.** The primary venue is now **TMLR** (OpenReview), submitted as soon as the gating results are in (target 2026-11-07
  to 2026-11-10). ACL/ARR (January 2027) is dropped for now; the ACL-format draft stays in git history.
- **Format.** `paper/` moves to the official TMLR LaTeX template in anonymous submission mode; main text up to 12 pages (hard
  cap, to keep the default review period), appendix unlimited. Figures cut for the ACL page limit are restored where they
  help (alignment curves, the full patching figure).
- **Gating results, in this order:** K1/K2 (running), H1-LF option 1 (waits for the SIB-1,004 Hindi drafts: 558 of 1,004
  done, Kannada complete), K3b-hi. **Experiments freeze once these three are in; nothing else new is started.**
- **Annotation scope in the paper.** K3 (blind human against Gemini, which needs Annotator B) and the A vs B agreement are
  **dropped from the paper**. Kept: the verification result (V-VER) and K3b. Annotator B's blind sample may be mentioned in
  one line as future work. The registered K3 and agreement analyses stay registered and unrun; they are not reported.
- **Pending placeholders** in the paper are used only for the three gating results.
- **Supplementary:** an anonymized code and data package (names, paths, institution and git history removed) with a README that
  reproduces every table from the included result files.

---
`````

## Phase 2

##### PHASE 2 CLARIFICATIONS (2026-11-02, Gate C decisions, Aarnav)

RESULTS.md lines 3472 to 3479; first line committed in `050df80` on 2026-11-02 16:36:01 +0530; last line in `9d408c4` on 2026-11-02 16:47:59 +0530; labels from the title and parent heading: amended

`````text
## PHASE 2 CLARIFICATIONS (2026-11-02, Gate C decisions, Aarnav)

**C1. X3 D3 sign convention (formal clarification; no verdict changes).** The X3 registration (2026-11-01) defines D3 = NC-O - c and then says "D3 positive effect = piece rarity at equal count costs". A rarity cost means NC-O (rarer pieces) is *worse* than c, which makes D3 *negative*; the two statements cannot both hold. The analysis (`scripts/x3_analyse.py`, run 2026-11-02) applied the literal rule (effect = Holm-significant positive difference in at least 3 of 4 accuracy models, 2 of 3 retrieval models, as for every contrast). **Clarification:** the intended meaning is that piece rarity at equal count costs when NC-O scores significantly *lower* than c; the effect rule is applied to the negative direction of D3 for the interpretation line. **Verdict unchanged under both readings:** literal reading, D3 has 0 significant positive models for SIB, sentiment and retrieval; cost-as-negative reading, D3 is significantly negative in 2 of 4 models for SIB (Qwen3.5, Sarvam-1; 3 needed), 0 of 4 for sentiment, 1 of 3 for retrieval (Gemma 4; 2 needed). D3 is "no effect detected" under both, and with D2 "no effect detected" the registered interpretation stays **unresolved**. Logged as deviation row in `paper2/tables/deviations.tex`.

**C2. X3 exploratory corpus-frequency regression (defined here, before it is run; the X3 text registers only the s_ref balance check, not a regression; Aarnav asked for it at Gate C, 2026-11-02).** Exploratory, no verdict, labelled so wherever it appears. For each model and each comparison split (c = the s_int frequency-matched split, and NC-O), on the model's eligible items of the c set: unit = item (SIB-200) or test-half sentence (retrieval, eligible M4c rows, layers as in `x3_analyse.py`); x_i = mean s_ref over the pieces of the canonical text span minus mean s_ref over the pieces of the comparison split's span (s_ref as registered: ln(1 + count) over the canonical tokenization of the 100,000-word reference sample); y_i = correct(canonical) - correct(split) in {-1, 0, 1} (SIB: calibrated prediction; retrieval: acc@1 hit). Model: ordinary least squares y_i = b0 + b1 x_i. Reported per model and measure: b0 (the accuracy change at zero corpus-frequency difference), b1, n, and 95% CIs by item bootstrap (10,000 resamples, seed 0). Counted and non-counted models are all reported, Qwen2.5 flagged as never counted. Sentiment and XNLI are not included (too few items per model for a slope).

---

`````

##### PHASE 2 AMENDMENT 2 (2026-11-02): X9 to X15, Kaggle compute, page policy

RESULTS.md lines 3486 to 3494; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: amended

`````text
## PHASE 2 AMENDMENT 2 (2026-11-02): X9 to X15, Kaggle compute, page policy

**APPROVED by Aarnav on 2026-11-02 with four edits (X12 exemption and rename, gate record, A1-R option (a)), applied below. Nothing in X9 to X15 had been run when it was approved.** This text is appended to
RESULTS.md unchanged, committed, and tagged `phase2-amendment-2`; `shattered.runlog.provenance()` then records that tag's commit as
`phase2_amendment2_commit` in every X9 to X15 result file (next to `phase2_registration_commit`). It supersedes `docs/X9_registration_DRAFT.md`.
Already registered and unchanged: X7 control (full 6-vocabulary grid with factorized embeddings, 3 seeds; running), X8 (n = 100, annotators
X8-P and X8-Q, agreement primary, vowel ratio descriptive), the Kaggle runner and its reproducibility gate (registered 2026-11-02 before
its first run). Citations are not added in this amendment.

`````

##### 2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run). The 8-bit LLM.int8 reference is withdrawn: it is an approximation, not a

RESULTS.md lines 3716 to 3725; first line committed in `78d6ad2` on 2026-11-02 23:17:45 +0530; last line in `eeafc85` on 2026-11-02 23:17:34 +0530; labels from the title and parent heading: registered, amended

`````text
- **2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run).** The 8-bit LLM.int8 reference is withdrawn: it is an approximation, not a
  valid ground truth for an fp16 fidelity check, so the two A1-P failures above (Qwen3-8B, Ambari-7B-base) are not used. **New reference: float32 with CPU offload** (device_map over both T4s,
  12 GiB per GPU, the rest of the weights in system RAM). Pass thresholds unchanged (raw-label agreement >= 0.98 per form, |accuracy difference| <= 0.01, no non-finite values, max fp16 hidden
  state < 65504). A1-P is re-run for Qwen3-8B and Ambari-7B-base-v0.1 against it, with the time reported. If a model fails against float32, it is out of the X12/X13 float16 runs, no further
  rescue is added, and a full float32-offload SIB run (1,004 x 4 forms) is timed and its hours reported before anything is run. If both pass, X12 Ambari base and X13 Qwen3-8B run as registered.
  *Two implementation faults found while preparing this (not rule changes):* (1) in `kaggle_precision.py` the float16 model was still referenced by the caller while float32 loaded, so the
  fp16 weights stayed on GPU 0; the "float32 out of memory (12.8 GiB)" for Ambari-7B-base above was probably caused by this, not by float32 not fitting (fixed: `model = free(model)`);
  (2) `kaggle_queue.py` read the previous `last_run.json` when the runner refused a dirty tree and recorded the old 8-bit Ambari result as new at 22:58 (fixed: `push()` returns None on refusal;
  the state was reset; nothing was pushed to Kaggle by that pass).

`````

##### 2026-11-02 23:17 IST, X12 CLARIFICATION (registered by Aarnav before any X12 result exists; no verdict rule is changed). Ambari-7B-Instruct-v0.2 uses the 32,000-token Llama-2

RESULTS.md lines 3726 to 3731; first line committed in `78d6ad2` on 2026-11-02 23:17:45 +0530; last line in `eeafc85` on 2026-11-02 23:17:34 +0530; labels from the title and parent heading: amended, result

`````text
- **2026-11-02 23:17 IST, X12 CLARIFICATION (registered by Aarnav before any X12 result exists; no verdict rule is changed).** Ambari-7B-Instruct-v0.2 uses the 32,000-token Llama-2
  tokenizer (`results/phase2/x12/tokenizers.json`: native 20.83, ITRANS 4.69 tokens per word), so it cannot be built on Ambari-7B-base (49,600; native 2.74, ITRANS 4.55). **Contrast 2 is renamed
  "instruction-pair exposure contrast":** Ambari-7B-Instruct-v0.1 (extended tokenizer plus 500M Kannada tokens) vs v0.2 (Llama-2 plus the same instruction tuning); it differs in **both** tokenizer
  and Kannada continued pretraining. **Primary statistic: the same DiD as contrast 1** (native gain minus ITRANS gain, on SIB-200 and on retrieval, 97.5% paired-bootstrap intervals, same
  verdict words). The MDL assembly comparison (300 Phase 1 probe words, fp16) is **descriptive only**, with this confound stated. **If Llama-2-7b-hf is still gated when X12 would run, this contrast
  stands in for contrast 1, and the paper says so.** Access: Ambari-7B-Instruct-v0.1 is now granted (downloads with the `.env` token); Llama-2-7b-hf and Llama-3.1-8B are still gated and are retried between jobs.
`````

##### 2026-11-02 23:21 IST, DEVIATION X9b-D1 (decided by Aarnav, registered before the pilot). The X9b memory and timing pilot runs on the Kaggle T4, not on the laptop, because the amendment fixes the

RESULTS.md lines 3741 to 3747; first line committed in `b3cbd64` on 2026-11-02 23:21:38 +0530; last line in `9d50e92` on 2026-11-02 23:24:17 +0530; labels from the title and parent heading: registered, amended

`````text
- **2026-11-02 23:21 IST, DEVIATION X9b-D1 (decided by Aarnav, registered before the pilot).** The X9b memory and timing pilot runs on the **Kaggle T4**, not on the laptop, because the amendment fixes the
  token budget B by a 50-step timing run on the machine that will train (the T4). No rule, threshold, condition, recipe or prediction changes. B = floor(0.9 x slowest measured tokens/s x 10,800 s),
  rounded down to a multiple of the tokens per optimizer step, per model, the same for the three conditions of a model, recorded here before any full run. The three training streams are built on
  CPU first and the registered exclusion scan must report overlap 0 for every stream or nothing runs; `scripts/kaggle_x9b.py` (pilot and full modes) writes `results/phase2/x9b/pilot_done.json`.
  Queue: the X9b pilot goes right after the A1-P job in flight, ahead of the X13 and X12 scoring (about an hour or less).
- Timestamps rule (Aarnav): every time in RESULTS.md, the deviations table or a log entry comes from `scripts/stamp.py` (system clock) or the commit, never typed; `scripts/check_results_times.py` and the pre-commit hook fail an entry later than its commit or the clock.

`````

##### 2026-11-03 00:04 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed). Annotators are not available. X1 T3 is marked "not run (instruction not verified)"; X15 is marked "not run (annotators unavailable)"; X8 is parked and mar

RESULTS.md lines 3769 to 3774; first line committed in `285c028` on 2026-11-03 00:04:58 +0530; last line in `d574ae9` on 2026-11-03 00:47:00 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-03 00:04 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** Annotators are not available. **X1 T3 is marked "not run (instruction not verified)"; X15 is marked "not run (annotators unavailable)"; X8 is parked and marked "not run"**
  (if the X8 files are sent later, it runs as registered). All three are removed from every queue (the laptop queue's "X1 T3" and the annotator-dependent items, and every pending annotation send); no chain or driver step referenced them. The
  workbooks, private keys, importers (`scripts/import_x8.py`, `import_x15.py`, `import_t3.py`, one command each over `annotation/returned/`, which is gitignored because returned files carry author fields) and analyses
  (`scripts/analyze_x8.py`, `analyze_x15.py`, tested on synthetic data only, outputs not kept) are kept. The three items and the reason are in `results/phase2/REGISTERED_OUTCOMES.md` (no Phase 2 outcomes table existed before; this is its start).
  The Kaggle and laptop queues continue as before.

`````

##### 2026-11-03 00:47 IST, STATUS NOTE: the tier prioritisation is WITHDRAWN and superseded (Aarnav). The tier message (tiers 1 to 3 over the experiments) was a misunderstanding of a question about which annotation is necessary; it never became 

RESULTS.md lines 3775 to 3780; first line committed in `d574ae9` on 2026-11-03 00:47:00 +0530; last line in `8a3a76f` on 2026-11-03 01:13:04 +0530; labels from the title and parent heading: none

`````text
- **2026-11-03 00:47 IST, STATUS NOTE: the tier prioritisation is WITHDRAWN and superseded (Aarnav).** The tier message (tiers 1 to 3 over the experiments) was a misunderstanding of a question about which annotation is necessary; it never became a registration entry and
  no queue, script or registered rule was changed because of it (checked against git and the queue driver: the instruction pair, Llama-3.1-8B and the X9b Qwen3.5-2B arm were never removed; X11 and X6 were never cut). Every experiment stays as registered in
  Amendment 2 and in the earlier ordering: laptop X7 control, X9a, X10, X11, X6, X4 Bengali and Telugu; Kaggle X9b (Sarvam-1 primary and Qwen3.5-2B secondary arm), X12 (contrast 1 primary, instruction pair secondary), X13 (Qwen3-8B, Llama-3.1-8B, the largest
  Sarvam that fits); X14 (Groq, under its caps). The Kaggle order is unchanged: A1-P pair, X9b pilot, scoring, Llama-2 A1-P and contrast 1, instruction pair, Llama-3.1-8B, X9b full; with the 18 h X9b Sarvam reserve and the cut order if quota is short
  (Llama-3.1-8B first, then the instruction pair, then the X9b Qwen3.5 arm). **Only the annotation part stands** (previous status note): X15 and T3 not run (annotators unavailable), X8 parked and run as registered if the files are sent.

`````

##### 2026-11-03 01:13 IST, CLARIFICATION (X1 T3): T3-2 was replaced by the native speaker's wording before any T3 scoring (Aarnav's message; no registered rule changes). The native speaker marked T3-1 (sentiment) and T3-3 (SIB-200) Correct and T

RESULTS.md lines 3781 to 3786; first line committed in `8a3a76f` on 2026-11-03 01:13:04 +0530; last line in `f39430f` on 2026-11-03 01:16:45 +0530; labels from the title and parent heading: amended

`````text
- **2026-11-03 01:13 IST, CLARIFICATION (X1 T3): T3-2 was replaced by the native speaker's wording before any T3 scoring (Aarnav's message; no registered rule changes).** The native speaker marked T3-1 (sentiment) and T3-3 (SIB-200) Correct and T3-2 (XNLI) Needs change, with the replacement
  `Question: Premise ಸತ್ಯವಾಗಿದ್ದರೆ, Hypothesis ಸಹ ಸತ್ಯವೇ? no, maybe, ಅಥವಾ yes ಆಯ್ಕೆಮಾಡಿ.` The returned workbook was not in `annotation/returned/` when this entry was written; the verdicts and the wording are taken from Aarnav's message and the file will be imported with
  `scripts/import_t3.py` when it arrives (any difference from this wording will be logged). The T3 instruction files are frozen with the new text before any T3 scoring: `e0_sentiment_v3.txt` (sha256 prefix d033e17f70369f67, unchanged), `e0_sib_v3.txt` (d0ac3dcb7c832384, unchanged),
  `e0_xnli_v3.txt` (6b8a23ef487ab848; before 71fd1dbbc2d6395c, which had ದತ್ತಾಂಶ and ಪರಿಕಲ್ಪನೆ for premise and hypothesis); hashes, the old line and the new line are in `results/phase2/x1/t3_templates.json` (`history`). **Every T3 result is labelled
  "instruction verified by a native speaker, exploratory"** (replacing "instruction not verified"; T3 stays exploratory with no registered claim). X1 T3 is back in the laptop queue after X9a (`scripts/x1t3_chain.sh`, same code path as T2 with `X1_TEMPLATE=v3`, outputs in `results/phase2/x1/t3/`); it is not started yet.

`````

##### 2026-11-03 01:16 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed). T3, X8 and X15 are no longer parked. T3: the returned `T3_verification.xlsx` was found at `annotation/xlsx/T3_verification.xlsx` (saved 01:03; it was not 

RESULTS.md lines 3787 to 3791; first line committed in `f39430f` on 2026-11-03 01:16:45 +0530; last line in `78e3f69` on 2026-11-03 01:37:59 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 01:16 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** T3, X8 and X15 are no longer parked. **T3:** the returned `T3_verification.xlsx` was found at `annotation/xlsx/T3_verification.xlsx` (saved 01:03; it was not in `annotation/returned/`) and imported with `scripts/import_t3.py` from a copy in `annotation/returned/` (0 blockers, 0 warnings): T3-1 Correct, T3-3 Correct, T3-2 Needs change with a corrected line identical to the wording in the clarification above; `results/phase2/x1/t3_verification_returned.json`.
  The previous "not run (instruction not verified)" mark for X1 T3 is withdrawn; X1 T3 is queued after X9a. **X8 and X15** are back in the registered design: X8_P and X8_Q (X8_Q goes to a different group of speakers, none of them in P, who never see X8_P) and eight X15 files for eight different people, none from the X8 groups.
  The workbooks are rebuilt **unprotected** (same 100 sentences and order, blank answer columns, same seeds; `annotation/xlsx/`); the importers no longer rely on locked cells: `scripts/import_x8.py`, `import_x15.py` and `import_t3.py` compare **every cell outside the answer cells with the original** (rebuilt deterministically) and block on any difference, and they also block when the same person (author-field hash) is behind two X15 files, behind P and Q, or behind an X8 and an X15 file.
  **If fewer than eight X15 files come back, the number is to be logged here as a deviation ("X15 DEVIATION: n of 8 files") before anything is analysed; `scripts/analyze_x15.py` refuses to run until that line exists.** (The instruction for the X8_P workbook was cut off in the message; X8_P is built the same way as X8_Q, unprotected.) Status table: `results/phase2/REGISTERED_OUTCOMES.md`. The Kaggle and laptop queues continue.

`````

##### 2026-11-03 01:37 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed). X15 is skipped: "not run (annotators unavailable)". No X15 files are built (`scripts/export_xlsx.py build` now skips them unless `--with-x15`), X15 is rem

RESULTS.md lines 3792 to 3795; first line committed in `78e3f69` on 2026-11-03 01:37:59 +0530; last line in `73546be` on 2026-11-03 02:24:19 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-03 01:37 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** **X15 is skipped: "not run (annotators unavailable)".** No X15 files are built (`scripts/export_xlsx.py build` now skips them unless `--with-x15`), X15 is removed from every to-do list and from `annotation/xlsx/SEND_ME.md`; the earlier X15 workbooks, importer and analysis scripts stay in the repository, unused. This supersedes the 01:1x note that put X15 back in the registered design.
  **T3** stands as logged: the returned workbook (`annotation/returned/T3_verification.xlsx`) was imported with 0 blockers and 0 warnings; T3-1 and T3-3 Correct, T3-2 replaced by the native speaker's wording before any T3 scoring; the instruction files are frozen with the new text (hashes in `results/phase2/x1/t3_templates.json`); X1 T3 is queued after X9a; every T3 result is labelled "instruction verified by a native speaker, exploratory".
  **X8:** `annotation/returned/` held only the T3 file when checked at 01:34; `annotation/xlsx/X8_Q.xlsx` (saved 01:32) holds 100 answers and was imported (0 blockers, 0 warnings; uppercase-start share 0.01, unexpected-character share 0.01 (one cell with Õ/õ), mean 16.3 words per sentence); `annotation/xlsx/X8_P.xlsx` has no answers. The registered X8 analysis (kappa, character error rate, descriptive ratios) needs both files and has not been run.

`````

##### 2026-11-03 12:58 IST, DEVIATION X7-D1 (Gate C decision, Aarnav): the X7 control's actual embedding parameters are not equal across vocabularies; the registered verdict "does not survive" stands, unchanged. Reason: the registered formula V x

RESULTS.md lines 3829 to 3833; first line committed in `2df4879` on 2026-11-03 12:58:00 +0530; last line in `cdef73d` on 2026-11-03 13:02:56 +0530; labels from the title and parent heading: amended, result

`````text
- **2026-11-03 12:58 IST, DEVIATION X7-D1 (Gate C decision, Aarnav): the X7 control's actual embedding parameters are not equal across vocabularies; the registered verdict "does not survive" stands, unchanged.** Reason: the registered formula V x e + e x 384 counted one projection ("tied input/output"), but the model has two (`emb_proj` and `unemb_proj`, `src/shattered/pretrain/model.py`); the grid records the actual count, which is e x (V + 769) (V x e table, 2 x e x 384 projections, plus e). **Actual embedding parameters per vocabulary (control; Phase 1 in brackets):** 256: 157,850 (98,688); 384: 147,584 (147,840); 512: 140,910 (196,992); 768: 130,645 (295,296); 1024: 125,510 (393,600); 4096: 107,030 (1,573,248). The control equalized the registered formula (98.5k) but not the real count (spread 47%, with the most fragmented vocabulary holding the most).
  **Bits per byte, control mean (seed SD, 3 seeds) next to Phase 1:** 256: 0.6017 (0.0032) vs 0.5970 (0.0009); 384: 0.5806 (0.0017) vs 0.5696 (0.0011); 512: 0.5799 (0.0029) vs 0.5606 (0.0021); 768: 0.5827 (0.0006) vs 0.5513 (0.0010); 1024: 0.5870 (0.0012) vs 0.5460 (0.0002); 4096: 0.6530 (0.0026) vs 0.5285 (0.0011).
  **Is the 256 minus 4096 gap of -0.0513 distinguishable from zero? Yes: reversed, not flat.** Welch test on the three seeds each: se 0.0024, t = -21.4 (df 3.9), p = 4e-5, 95% CI [-0.0581, -0.0445]; every one of the three seeds at 256 (0.6052, 0.5989, 0.6010) is below every seed at 4096 (0.6560, 0.6514, 0.6515); the gap is 16 times the larger seed SD. The control reverses the Phase 1 ordering at the extremes (Phase 1: 4096 best, gap +0.0685).
  **MDL assembly layer under the control: NOT measured.** The 18 control checkpoints exist (`checkpoints/e05/x7_v*_s*`). Cost to measure with the Phase 1 probes: the Phase 1 run on 18 models took 743 s of forward passes plus 1,024 s of probes = 0.49 GPU hours (98 s per model), plus a small change to `scripts/m1_tiny_probes.py` (it loads `run_v*_s*` names and the model config from `final.json`; the control runs are named `x7_v*_s*`), so about 0.5 h of laptop GPU and under an hour of work.

`````

##### 2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md). Removed 

RESULTS.md lines 3858 to 3859; first line committed in `3290232` on 2026-11-04 01:44:01 +0530; last line in `28803e6` on 2026-11-04 02:33:57 +0530; labels from the title and parent heading: registered, result, failed or not run

`````text
- **2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md).** Removed from every queue; added to `results/phase2/REGISTERED_OUTCOMES.md`. The draft text was never committed. **X8: the Q writer confirmed that they used no tool of any kind (Aarnav's statement), in addition to the earlier statements that the P and Q writers did not see each other's answers.** **X8 descriptive diagnostic (no threshold, no verdict; case-insensitive exact matches with whitespace collapsed; character difference = the registered CER definition per sentence):** exact matches: Gemini vs Q 1 of 100, Gemini vs P 1 of 100, P vs Q 0 of 100. Per-sentence character difference, Gemini vs Q: median 0.0631, quartiles 0.0423 to 0.0799, range 0.0000 to 0.1603, 6 of 100 below 2%; Gemini vs P: median 0.1039, quartiles 0.0759 to 0.1359, range 0.0000 to 0.2647, 1 of 100 below 2%; P vs Q (for comparison): median 0.0898, quartiles 0.0634 to 0.1237, 2 of 100 below 2%. The per-annotator table (Gemini vs P and Gemini vs Q: the three ratios, kappa, CER) stays in `results/phase2/x8/analysis.json` next to the registered mean-of-P-and-Q ratios. The paper is not edited.

`````

##### 2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD values above are unchanged). Gain = Ambari-7B-base minus Llama-2-7B, paired boot

RESULTS.md lines 3908 to 3909; first line committed in `72ff37e` on 2026-11-04 12:14:44 +0530; last line in `39d4c01` on 2026-11-04 13:21:46 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD values above are unchanged).** Gain = Ambari-7B-base minus Llama-2-7B, paired bootstrap over items, 95% interval (descriptive). SIB-200 (n = 1,004): native +0.389 [0.356, 0.423]; ITRANS -0.034 [-0.052, -0.016]; lossy -0.090 [-0.118, -0.063]; English -0.130 [-0.158, -0.103]. Retrieval (n = 1,005): native +0.692 [0.662, 0.721]; ITRANS +0.068 [0.051, 0.086]. A1-P (100 items x native/ITRANS/lossy, fp16 vs float32-offload): Ambari-7B-base raw label agreement 1.00 / 1.00 / 1.00, accuracy difference 0.000 in each form, max hidden state 1,730; Llama-2-7B agreement 1.00 / 0.99 / 1.00, accuracy difference 0.000 in each form, max hidden state 2,424; no non-finite value in either; mean |dlogprob| 0.003. Note: Ambari loses 13 points on English SIB-200 relative to Llama-2 (0.559 vs 0.689), so the continued pretraining also changed the model outside Kannada.

`````

##### 2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label agreement 1.00 in native, ITRANS and lossy, accuracy difference 0.00 in each, me

RESULTS.md lines 3938 to 3939; first line committed in `06404f2` on 2026-11-04 22:07:54 +0530; last line in `17dba9c` on 2026-11-04 22:24:09 +0530; labels from the title and parent heading: amended, result

`````text
- **2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label agreement 1.00 in native, ITRANS and lossy, accuracy difference 0.00 in each, mean |dlogprob| 0.003 to 0.004, max fp16 hidden state 559.5, no non-finite value).** Both instruction models have now passed A1-P (v0.2 earlier), so the pair is scored as registered; the scoring of v0.1 was pushed at 22:06 IST. Correction to my duplicate-push entry above: the 20:10 run was not lost: it completed and its output was fetched by the later push's fetch (identical numbers in both result folders, same fp16 load of 3,420 s and total of 6,754 s); the 21:41 push (5.0 h cap) was therefore possibly a redundant second run of the same job whose hours will count when it ends. The weights loaded from the private dataset took 3,420 s (57 minutes) in fp16 in this run, which did not yet have the copy-to-local-disk loader (committed after the push); the load-time comparison with the copy loader is still to be made on the next job that loads from a private dataset.

`````

##### 2026-11-05 02:25 IST, X6 screen stage 2 and run part 1 started (laptop). Rule (1), forward-pass peak memory in bf16 with hidden states on the 8 GB laptop GPU: NousResearch/Llama-3.2-1B 2.46 GiB; ashtok897/oroZ-1.7B-Indic-v1 4.29 GiB; both f

RESULTS.md lines 3954 to 3955; first line committed in `3c2e3a6` on 2026-11-05 02:25:27 +0530; last line in `ec3c085` on 2026-11-05 02:38:48 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 02:25 IST, X6 screen stage 2 and run part 1 started (laptop).** Rule (1), forward-pass peak memory in bf16 with hidden states on the 8 GB laptop GPU: NousResearch/Llama-3.2-1B 2.46 GiB; ashtok897/oroZ-1.7B-Indic-v1 4.29 GiB; both fit. The laptop queue was empty after X4 scoring (finished 02:10) and the X6 memory check (02:22), so the X6 SIB-200 counting run (rule 3; `scripts/x6_run.py`, chain `scripts/x6run_chain.sh`) was pulled forward and started at 02:24 IST; models added to the loader as llama-3.2-1b (mirror, deviation X6-D1) and oro-1.7b. The remaining laptop work that exists as registered but is not built: X4 lowercase form and ladder, retrieval, MDL and K3b parts, the full X6 runs for counted models.

`````

##### 2026-11-05 03:38 IST, X6 COUNTING RESULT (rule 3; laptop; `scripts/x6_run.py`, `results/phase2/x6/counting.json`): neither shortlist model is counted. SIB-200 (n = 1,004, T1, calibrated as Phase 1; no raw fallback): Llama-3.2-1B (NousResear

RESULTS.md lines 3962 to 3963; first line committed in `b9383db` on 2026-11-05 03:38:22 +0530; last line in `108fa59` on 2026-11-05 03:40:56 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 03:38 IST, X6 COUNTING RESULT (rule 3; laptop; `scripts/x6_run.py`, `results/phase2/x6/counting.json`): neither shortlist model is counted.** SIB-200 (n = 1,004, T1, calibrated as Phase 1; no raw fallback): **Llama-3.2-1B (NousResearch mirror, deviation X6-D1): native 0.412, 95% CI [0.381, 0.443]; lower bound 0.381, below 0.40: not counted.** English 0.633, ITRANS 0.213, lowercase 0.186, lossy 0.241. **oroZ-1.7B-Indic-v1: native 0.277 [0.249, 0.305], lower bound 0.249: not counted** (English 0.388, ITRANS 0.251, lowercase 0.250, lossy 0.252: the model is close to chance on Kannada in every form). Both are reported and never counted, so they do not enter any verdict; X6 adds no counted model. The remaining X6 runs (T2 template, retrieval, ladder) are registered for included models; because neither is counted they are not run, and X6 is closed as screened, run for counting, and not counted. No Arm B of X11 can be formed from a 4B-class X6 model (none was shortlisted). The paper is not edited.

`````

##### 2026-11-05 14:37 IST, X14 FINISHED (hosted models via Groq, exploratory, no registered verdict; `scripts/x14_run.py`, `scripts/x14_analyse.py`, `results/phase2/x14/analysis.json`; finished 14:23 IST after the 12:45 reset; 3,269 rows per mod

RESULTS.md lines 4005 to 4006; first line committed in `88cf86e` on 2026-11-05 14:37:51 +0530; last line in `0f01dd6` on 2026-11-05 14:38:09 +0530; labels from the title and parent heading: exploratory, result, failed or not run

`````text
- **2026-11-05 14:37 IST, X14 FINISHED (hosted models via Groq, exploratory, no registered verdict; `scripts/x14_run.py`, `scripts/x14_analyse.py`, `results/phase2/x14/analysis.json`; finished 14:23 IST after the 12:45 reset; 3,269 rows per model: 1,004 each for native, ITRANS and lossy, 257 natural).** SIB-200 accuracy with the registered prompt, temperature 0, exact match, unparsed counted wrong; 95% bootstrap intervals over items; gaps paired over item ids. **gpt-oss-120b: native 0.836 [0.813, 0.859], ITRANS 0.625 [0.595, 0.654], lossy 0.668 [0.638, 0.697], natural 0.700 [0.646, 0.755]; native minus ITRANS +0.211 [0.181, 0.241], minus lossy +0.167 [0.139, 0.196], minus natural +0.167 [0.117, 0.218] (n = 257); unparsed 0%.** **Qwen3.8-27B (the Groq model qwen/qwen3.8-27b): native 0.836 [0.813, 0.859], ITRANS 0.658 [0.628, 0.687], lossy 0.654 [0.625, 0.684], natural 0.696 [0.638, 0.751]; native minus ITRANS +0.177 [0.147, 0.207], minus lossy +0.181 [0.151, 0.210], minus natural +0.144 [0.093, 0.195]; unparsed at most 0.1%.** **ALLaM-2-7B: native 0.337 [0.308, 0.367], ITRANS 0.190 [0.166, 0.214], lossy 0.254 [0.227, 0.281], natural 0.296 [0.241, 0.354]; native minus ITRANS +0.146 [0.115, 0.179]; unparsed 35.5% native and 55.6% to 57.7% romanized, so its accuracies mix understanding with answer-format failure.** Reading, descriptive only: the large hosted models keep the familiarity ordering seen in the small open models (native above natural above ITRANS and lossy), with a native-to-romanized gap of 14 to 21 points that is far smaller than the small models' gaps in absolute accuracy terms but still well away from zero; natural romanization recovers about a third to a half of the ITRANS gap in gpt-oss-120b (natural 0.700 against ITRANS 0.625 on different item sets, so the paired natural gap is the comparable number: +0.167 against +0.211 on the 257 items for ITRANS from the main set) and the lossy form is not worse than ITRANS in either large model (gpt-oss: 0.668 against 0.625; Qwen3.8-27B: 0.654 against 0.658). Model names as in `model_choice.json`; deviation X14-D1 (token budget for one model) stands as logged. The paper is not edited.

`````

##### 2026-11-05 14:38 IST, CORRECTION NOTE to the X14 entry above (reading paragraph only; numbers unchanged). The sentence comparing natural with ITRANS mixed item sets. On the same 257 items the accuracies are: gpt-oss-120b native 0.868, ITRAN

RESULTS.md lines 4007 to 4008; first line committed in `0f01dd6` on 2026-11-05 14:38:09 +0530; last line in `2f9c9f1` on 2026-11-05 15:37:57 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 14:38 IST, CORRECTION NOTE to the X14 entry above (reading paragraph only; numbers unchanged).** The sentence comparing natural with ITRANS mixed item sets. On the same 257 items the accuracies are: gpt-oss-120b native 0.868, ITRANS 0.646, natural 0.700; Qwen3.8-27B native 0.840, ITRANS 0.658, natural 0.696; ALLaM-2-7B native 0.366, ITRANS 0.206, natural 0.296. So natural romanization recovers 54 of 222 points of the native-to-ITRANS gap in gpt-oss-120b (about a quarter), 38 of 182 in Qwen3.8-27B (about a fifth) and 90 of 160 in ALLaM-2-7B (a bit over half; format failures dominate that model); the earlier phrase 'about a third to a half' is withdrawn. The remaining statements (familiarity ordering native > natural > ITRANS in the three models; lossy not worse than ITRANS in the two large models; native-to-ITRANS gaps of 14.6 to 21.1 points on the 1,004 items) stand. The comparison to the small open models' gaps was not computed and is withdrawn too; no such statement is made.

`````

##### 2026-11-05 15:39 IST, CORRECTION NOTE to the X9a-low extra-seed entry above (one phrase). In the reading the phrase "0.3% seed 3 at 0.172" should read: the third ORIGINAL seed at 0.3% (code seed 2, retrieval 0.172) is 0.06 above the 0.1% se

RESULTS.md lines 4013 to 4014; first line committed in `c7f6e92` on 2026-11-05 15:39:07 +0530; last line in `3ecea71` on 2026-11-05 15:42:19 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 15:39 IST, CORRECTION NOTE to the X9a-low extra-seed entry above (one phrase).** In the reading the phrase "0.3% seed 3 at 0.172" should read: the third ORIGINAL seed at 0.3% (code seed 2, retrieval 0.172) is 0.06 above the 0.1% seeds (0.100 to 0.116); code seed 3 at 0.3% is 0.204. All other numbers stand.

`````

##### 2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged). After the power-loss restart the first extra run (`sarvam-1+itrans+s2`) reach

RESULTS.md lines 4025 to 4026; first line committed in `1d0616d` on 2026-11-05 22:59:17 +0530; last line in `4579347` on 2026-11-05 22:59:29 +0530; labels from the title and parent heading: amended, failed or not run

`````text
- **2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged).** After the power-loss restart the first extra run (`sarvam-1+itrans+s2`) reached step 100 at 22:50 and then sat in `torch.save` for more than 8 minutes with the GPU idle (py-spy: `serialization._save`, `write_record`, one core at 100%); the first attempt did the same (step 100 logged at about 16:20, checkpoint file last written 16:42, when the power failed). Cause: the optimizer state is the paged 8-bit AdamW state (bitsandbytes), whose pages migrate one by one while the 8 GB card is full; writing it takes over 20 minutes per checkpoint, three checkpoints per run, about 1 h of every 2.9 h run, about 6 to 7 h over six runs (the Kaggle T4s had room for it, the laptop does not). Fix, committed: checkpoints now hold the adapter, scheduler, scaler and step but not the optimizer state, which makes the save take seconds; the checkpoint is only ever read after an interruption, so an uninterrupted run is numerically identical to before; a run resumed from such a checkpoint resets the Adam moments, and `done.json` carries `resumed_without_optimizer_state` (true) so it can be reported or excluded. The running ITRANS run is resumed from its step-100 checkpoint, which does contain the optimizer state (written before the change), so it continues exactly; the chain `x9extra` is relaunched after the restart. The finish estimate improves by about 6 h: about 8 Nov 00:00 to 02:00 IST for the six laptop runs, if account 3 does not take the seed-4 runs.

`````

##### 2026-11-05 22:59 IST, CORRECTION NOTE (finish dates of the laptop X9b extra seeds; arithmetic error). The two entries above that give the six laptop runs a finish of "8 Nov" (after the power-loss restart, and in the checkpoint entry) are wr

RESULTS.md lines 4027 to 4028; first line committed in `4579347` on 2026-11-05 22:59:29 +0530; last line in `8c59c8a` on 2026-11-06 00:53:19 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 22:59 IST, CORRECTION NOTE (finish dates of the laptop X9b extra seeds; arithmetic error).** The two entries above that give the six laptop runs a finish of "8 Nov" (after the power-loss restart, and in the checkpoint entry) are wrong by about a day and a half: six runs of about 2.9 h each (2.5 h training, 0.4 h evaluation) started at 22:07 on 5 Nov end about **6 Nov 15:30 IST**, and the one run slowed by the 20-minute checkpoint stalls (about 1 h) moves that to about **6 Nov 16:30 to 17:30 IST** with the checkpoint fix in place. If account 3 becomes usable and takes the three seed-4 runs, the laptop's three seed-3 runs end about 6 Nov 07:00 IST. The earlier report to Aarnav quoted the wrong date and is corrected in the next report.

`````

##### 2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational). Windows logged a second unclean reboot (Kernel-Power 41; bugcheck 0x1e, an unhandled access violation, last good time 22:41:16; the earlier

RESULTS.md lines 4029 to 4030; first line committed in `8c59c8a` on 2026-11-06 00:53:19 +0530; last line in `fc1246a` on 2026-11-06 02:37:37 +0530; labels from the title and parent heading: amended, failed or not run

`````text
- **2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational).** Windows logged a second unclean reboot (Kernel-Power 41; bugcheck 0x1e, an unhandled access violation, last good time 22:41:16; the earlier one, 16:10, was bugcheck 0x9f, a driver power-state failure), the machine came back at 23:06 and the chain at 23:47. Both crashes came while the GPU was at full memory with shared-memory spill (peak 10.6 GiB asked of an 8 GB card at micro-batch 16) and, the second time, during the stalled checkpoint save. Consequences: GPU idle 22:41 to 23:47 (about 1 h 05 min, a crash, not a project process); the ITRANS seed-3 run (code seed 2) had no usable checkpoint and **restarted from step 0 at 23:47** (it is at step 140 or more now, ckpt written with the fast format at 00:31). Change (committed, recipe unchanged): the code reads an optional laptop-only file `build/x9b_max_micro_batch.txt` and caps the micro-batch at its value, with proportionally more accumulation steps, so the optimizer step is the same (16,384 tokens) while memory stays under the card's 8 GB; it holds 8 from now, so the run in progress (started at 23:47) keeps micro-batch 16 and the next five runs use 8 (done.json records the micro-batch used). Speed cost expected at a few percent. If the laptop crashes again the run resumes from the adapter checkpoint with reset Adam moments and is flagged in done.json (`resumed_without_optimizer_state`). Projected finish of the six laptop runs: the first at about 02:40 on 6 Nov, the last about 6 Nov 17:30 to 19:30 IST.

`````

##### 2026-11-08 16:23 IST, SARVAM-M X10 PILOT RESULT AND THE RUN DECISION (account 3; timing only, no chrF used for any decision). Pilot (16 sentences, native and ITRANS, batch 8, 4-bit, 2 x T4): model load 428 s; 28.0 s per sentence (native) an

RESULTS.md lines 4054 to 4055; first line committed in `0034538` on 2026-11-08 16:23:25 +0530; last line in `?` on ?; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-08 16:23 IST, SARVAM-M X10 PILOT RESULT AND THE RUN DECISION (account 3; timing only, no chrF used for any decision).** Pilot (16 sentences, native and ITRANS, batch 8, 4-bit, 2 x T4): model load 428 s; 28.0 s per sentence (native) and 22.3 s (ITRANS); no empty outputs and no reasoning preamble in the 32 outputs; kernel 0.41 h. Estimate for the full registered X10 (native, ITRANS, lowercase, lossy on 1,012 sentences and natural on 267) at that rate: about 4,315 sentences x 25 s = about 30 h, against 25.1 h left on account 3 and a 12 h session cap. **Decision (cut, logged): run native and ITRANS only, the registered X10-P contrast, as two resumable kernels at batch 16 (about 11 to 14 h of quota in total, one kernel per form, 10.5 h cap each); lowercase, lossy and natural are not run for Sarvam-m. This is a deviation from the full X10 form set for this extended model (the X10-P verdict concerns the four counted models and is unchanged).** Chain `x10sm`; if batch 16 runs out of memory the run is retried once at batch 8. Quota on account 3: 4.9 h used of 30 h.

`````

## The deviations table of the paper (paper2/tables/deviations.tex, verbatim)

`````text
\footnotesize
\begin{longtable}{>{\raggedright\arraybackslash}p{0.34\textwidth}>{\raggedright\arraybackslash}p{0.12\textwidth}>{\raggedright\arraybackslash}p{0.26\textwidth}>{\raggedright\arraybackslash}p{0.2\textwidth}}
\caption{Deviations from the registration and tests registered after related results were seen, one row per entry (dates are those of the entries in the project's registration log). ``Registered'' is the date of the entry that records the change; ``Relative to'' names the results already seen when it was written. Post hoc and exploratory analyses that were not registered are labelled as such where they are reported.}\label{tab:deviations}\\
\toprule
Deviation or late registration & Registered & Relative to & Effect \\
\midrule
\endfirsthead
\toprule
Deviation or late registration & Registered & Relative to & Effect \\
\midrule
\endhead
\bottomrule
\endfoot
Calibration changed from one content-free input (\texttt{N/A}) to the mean of three (\texttt{N/A}, empty, \texttt{[MASK]}). & 2026-10-15 & After Gate 1a (sentiment, five models), where the single input broke Qwen2.5. & Gate 1 predictions use the new scores. \\
Raw-score fallback: a model-by-task row uses raw scores if calibrated English accuracy is more than 5 points below raw. & 2026-10-15 & After Gate 1a. & Applies to whole rows; flagged in the tables. \\
Linear word-identity probes on the tiny GPTs reclassified as uninformative; MDL probes replace them. & 2026-10-15 & After the Step 3 result (probe saturated after one block). & Tiny-GPT assembly is measured with MDL. \\
Primary mechanism measure switched from Patchscopes to MDL. & 2026-10-16 & After the full Patchscopes run (0 to 7\% of Kannada words identified). & The Patchscopes failure is reported as a finding. \\
Test of ``ITRANS never reaches native's maximum retrieval'' (M-series H1) operationalized as a paired CI above 0. & 2026-10-16 & After the maxima had been printed. & Gaps are large; the verdict does not hinge on the choice. \\
Word-clustered CIs made primary for the assembly measure. & 2026-10-16 & After the occurrence-level CIs. & Both kept. \\
Surface baseline for the learned mapping (not blind), and its natural-romanization addendum. & 2026-10-17; 2026-10-21 & After the per-layer mapping curves, and after the natural-romanization retrieval summary. & Reported as an expectation, not a blind test. \\
Qwen2.5 never counted in tests of romanized forms against native, from the romanization ladder onward. & 2026-10-22 & After P-a, K1 and K2 had been registered counting it (retrieval prediction M4c, 2026-10-16, excluded it only in part). & K1 and K2 keep it counted, as registered (decision 2026-10-26). \\
Forced-tokenization gate: the equal-count re-split share was 79.4\%, below the registered 80\%; Sarvam-1 byte-fallback units kept canonical. & 2026-10-22 & After the NC1 pilot. & Run proceeded, threshold unchanged. \\
Operational deviations without a method change: timing pilot used two models; performance bug fixed before running; scoring job crashed on mixed id types and was restarted; first Kanglish pilot failed on an id type. & 2026-10-22; 2026-10-26 & During the jobs; no statistic had been computed. & None. \\
Annotation procedure: defective Gemini drafts re-asked beyond three attempts; two defective items replaced by seeded draws; annotator roles fixed. & 2026-10-22; 2026-10-23 & Before any annotation existed. & None on verdicts. \\
Annotation protocol changes: Excel workbooks instead of HTML pages; verify instead of rate-and-correct; annotator A is a pool of about 50 people. & 2026-10-25; 2026-10-26 (two entries) & Before any valid annotation was returned; the pool was recorded after its workbook arrived. & No within-pool agreement; the registered blind comparison (K3) is not reported. \\
English-share tagger: the registered tagger (v1) failed its validity check (recall below 0.9); a corrected tagger (v2) is primary, v1 reported alongside. & 2026-10-26 & After the validity check on a hand-marked sample, before any K2 result existed. & K2a and K2b verdicts do not differ between taggers. \\
H1-LF: the Kannada--Hindi test repeated at equal English-word share and on loan-free items. & 2026-10-23 & After the H1 results and the loan-free secondary were seen. & A follow-up; the H1 verdicts stand unchanged. \\
EP-R: patching recovery on all eligible items (exploratory). & 2026-10-26 & After the E-P1 and E-P2 results. & No verdict; registered outcomes unchanged. \\
K2b lexical-overlap control (exploratory). & 2026-10-28 & After the K2b result. & No verdict; the registered K2b outcome is unchanged. \\
X3 registration: the sign convention of the D3 contrast (NC-O minus matched split) was inconsistent with its interpretation line; clarified. & 2026-11-02 & After the X3 results (Gate C). & Verdict unchanged under both readings (no effect detected); interpretation unresolved. \\
X12 registration: contrast 2 renamed ``instruction-pair exposure contrast''; Ambari-7B-Instruct-v0.2 uses the 32,000-token Llama-2 tokenizer, so the pair differs in tokenizer and in Kannada continued pretraining; the primary statistic is the contrast-1 difference of gains; the assembly-layer comparison is descriptive only; this contrast stands in for contrast 1 if Llama-2-7b-hf is still gated. & 2026-11-02 & After the tokenizer screen only, before any X12 result. & No verdict rule changed; the claim tested is the pair comparison, not fragmentation with data fixed. \\
A1-P precision check (X12, X13): the first failures of Ambari-7B-base and Qwen3-8B came from an invalid 8-bit reference and from a harness bug (float16 weights left on the GPU when the float32 reference loaded); the reference is float32 with CPU offload (A1-P-D1), thresholds unchanged, and both models pass against it. & 2026-11-02; 2026-11-03 & After the first A1-P results (both models failed against the 8-bit reference). & The two models enter X12 and X13 as registered; no threshold or verdict rule changed. \\
X7 control: the actual embedding parameters are not equal across vocabularies in the factorized control (V=4096 has the fewest); the registered verdict is kept and the paper reports the parameter counts. & 2026-11-03 & After the X7 results (Gate C). & Verdict ``does not survive'' unchanged; X7b (equal actual parameters) not run. \\
X7-A: assembly layer on the 18 X7 runs (exploratory). & 2026-11-04 & After the X7 bits-per-byte result. & Exploratory; the X7 verdict is unchanged. \\
X9a-low: exposure levels 0.01 to 0.3 percent (exploratory). & 2026-11-04 & After the X9a-R ceiling was seen. & Exploratory; the X9a-R verdict is unchanged. \\
X2: a parametric (Poisson) interval on document counts replaces the bootstrap over shards (the romanized configs are single-shard files; deviation X2-D1). & 2026-11-05 & Logged with the X2 result. & The registered test and verdict rule are unchanged. \\
X14: the token budget of one hosted model (a reasoning model) is larger than the registered 20 new tokens (deviation X14-D1). & 2026-11-02 & After the first pilot calls. & Exploratory, no verdict. \\
X10 post hoc check: first non-empty line instead of the first line, for Qwen3.5-2B only. & 2026-11-05 & After the X10 result. & Not registered; the registered X10 verdict is unchanged. \\
Extra seeds for the X9b primary arm (Sarvam-1, seeds 3 and 4) and for X9a-low at 0.1, 0.3 and 1 percent (seeds 4 and 5). & 2026-11-05 & After seeds 1 and 2 (X9b) and seeds 1 to 3 (X9a-low) were seen. & Reported with all seeds together and the original seeds separately; registered verdicts unchanged. \\
Second set of extra seeds: X9b secondary arm (Qwen3.5-2B, seeds 2 and 3) and X9a-low at levels 0, 0.01 and 0.03 percent (seeds 4 and 5). & 2026-11-07 & After seed 1 of the Qwen arm and seeds 1 to 3 of X9a-low were seen. & Same reporting; registered verdicts unchanged. \\
Laptop training stability: micro-batch cap (16 to 8 for Sarvam-1, 4 to 2 for Qwen3.5-2B) after two system crashes and a memory-spill slowdown; checkpoints without optimizer state; resumed runs flagged. & 2026-11-06 & After the first extra run (X9b). & Same optimizer step and token budget; no run was resumed; recorded per run. \\
Compute location: some Kaggle compute (X9b batch 3 and the Qwen3.5-2B arm, X12 and X13 scoring, Sarvam-m) ran on teammates' Kaggle accounts; the Qwen arm's last evaluation was finished on the laptop after the kernel's time cap. & 2026-11-05 & Operational. & Same code and reproducibility check on every account; none of the registered statistics changed. \\
Counting rule for the models added in Phase 2 (native SIB-200 accuracy with a 95\% CI lower bound above 0.40). & 2026-11-01 & After the native SIB-200 score of Qwen2.5-1.5B (0.34) had been computed (2026-10-16). & The rule excludes Qwen2.5-1.5B; the headline counts are given with and without it. \\
\end{longtable}
\normalsize

`````

# Phase 1: RESULTS.md entries not matched to an experiment id above (verbatim, nothing omitted)

##### RESULTS.md preamble

RESULTS.md lines 1 to 7; first line committed in `7522757` on 2026-10-07 01:55:06 +0530; last line in `cec25d5` on 2026-10-07 03:07:13 +0530; labels from the title and parent heading: result

`````text
# Results log

One entry per experiment run: date, experiment id, config, commit hash, headline numbers (with n and CIs),
prediction, outcome (confirmed / refuted / inconclusive), surprises, next step. Every number here comes from a file in
`results/`.

---
`````

##### 2026-10-07 — Outcome corrections (agreed with Aarnav)

RESULTS.md lines 77 to 88; first line committed in `af094cc` on 2026-10-07 15:47:10 +0530; last line in `76c8073` on 2026-10-07 16:40:03 +0530; labels from the title and parent heading: none

`````text
## 2026-10-07 — Outcome corrections (agreed with Aarnav)

- **E1 prediction ("Dravidian languages cost at least 2x English on most tokenizers"): narrowly failed on o200k.**
  On o200k (GPT-4o) the Dravidian tax is 1.94–1.99x (Kannada 1.99 [1.97, 2.00], Tamil 1.98, Telugu 1.94, Malayalam
  1.95; n = 2009 FLORES-200 sentences each; `results/e01_cost/summary.csv`), i.e. below 2x. It holds on older and
  English-heavy tokenizers (6–15x). Recorded as: refuted for o200k, confirmed for most older tokenizers.
- **E3 assumption ("romanization cuts input tokens") is refuted for modern tokenizers.** Lossless ITRANS costs more
  than native Kannada on o200k (+21%), Gemma 4 (+25%) and Sarvam-1 (+124%); it saves tokens only on older tokenizers
  (cl100k −71%, Llama 2 −77%). Source: same file. E3's cost framing must be revised; E9 is the remaining route to a
  cost win.

---
`````

##### 2026-10-07 — Scope changes

RESULTS.md lines 133 to 143; first line committed in `8380e09` on 2026-10-07 16:49:31 +0530; last line in `8380e09` on 2026-10-07 16:49:31 +0530; labels from the title and parent heading: none

`````text
## 2026-10-07 — Scope changes

- **E9 dropped** after its gate: negative result as recorded above (held-out savings over ITRANS 1.0–4.8%, below the
  5% failure line on every target). Not pursued further.
- **E7 dropped**: FragMend (arXiv 2604.16656) already does Patchscopes detokenization and vocabulary expansion for
  non-Latin scripts.
- **Limitation (E1)**: no Anthropic API key will be used, so Claude tokenizers are not measured. Anthropic's pricing
  page (read 2026-10-07) states that Claude 4.7+ uses a newer tokenizer producing ~30% more tokens for the same text;
  we cannot verify how this affects Kannada.

---
`````

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

##### 2026-10-21 — Exploratory note: lossy > ITRANS is confounded (post hoc, Aarnav)

RESULTS.md lines 1268 to 1282; first line committed in `d7693f7` on 2026-10-21 22:25:39 +0530; last line in `d7693f7` on 2026-10-21 22:25:39 +0530; labels from the title and parent heading: exploratory, post hoc

`````text
## 2026-10-21 — Exploratory note: lossy > ITRANS is confounded (post hoc, Aarnav)
- **The finding.** Lossy romanization beats lossless ITRANS in accuracy in every model:
  - Gate 1 (P3 refuted);
  - E0c, +0.07 to +0.17, all significant.
- **What it refutes.** The information-loss account, under which more lossy romanization should hurt more.
- **Why it can't say more.** Lossy differs from ITRANS in two ways at once:
  - **Fragmentation.** Lossy has fewer tokens per word than ITRANS in every model and every task: by 0.66–0.89 on E0b
    sentiment/XNLI and 0.78–0.98 on SIB-200 (`results/e0b_familiarity/gate1/accuracy.csv`,
    `results/e0c_sib/gate/accuracy.csv`).
  - **Spelling familiarity.** It drops ITRANS's case and diacritic conventions and is closer to how Kannada is
    informally typed.
- **Conclusion.** lossy > ITRANS refutes the information-loss account. It cannot tell fragmentation and spelling
  familiarity apart. The same holds for natural > ITRANS in M4c.

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

##### 2026-10-22 — Audit: are form comparisons computed on matched items? (no verdict changed)

RESULTS.md lines 1431 to 1461; first line committed in `f76c726` on 2026-10-22 02:19:58 +0530; last line in `5715d3e` on 2026-10-22 02:23:42 +0530; labels from the title and parent heading: result

`````text
## 2026-10-22 — Audit: are form comparisons computed on matched items? (no verdict changed)
Checked every RESULTS.md claim that compares native, ITRANS, lowercase, lossy and natural. "Matched" = every compared
form on the same items. Only the natural form ever has fewer items than the others: in E0b, 9 natural texts stayed
defective, so natural has 198 sentiment and 193 XNLI items against 200 for every other form.

**Matched (no issue):** E1 cost atlas and E9 (same 2,009 sentences); E0 and Gate 1a (200 items, all forms); every Gate 1
McNemar test, hence every P1–P3 verdict (`mcnemar_table` pairs on items present in both forms: 198/193 for natural);
item-level fragmentation note (paired McNemar); Gate 2 M1 (words paired by construction) and M4 (2,009); M4b, its
robustness check and surface baseline (same split; filtered/random subsets compare forms within each subset); E0c
(1,004, all forms) and P-b (within form); M4c and the natural surface baseline (same 496/248 sentences); the
back-translation gap (576 paired texts); the lossy vs ITRANS tokens-per-word ranges (all items in both forms); the
ladder registration (L3 on sentiment paired on 198); the 2026-10-22 alignment curves (same 248).

**Not matched (point estimates or tokens per word quoted with natural on 198/193 and the other forms on 200):**
1. **Gate 1 accuracy table (2026-10-15):** natural n = 198/193, others n = 200 (stated in the entry's header). The
   paired values differ by up to 0.8 points, e.g. Sarvam-1 XNLI natural − ITRANS +7.3 paired vs +8.1 from the table
   (`results/e0b_familiarity/gate1/mcnemar.csv` vs `accuracy.csv`).
2. **Gate 1 P1 text:** "Qwen2.5 sentiment (51.5 vs 70.5)": 70.5 is native on all 200; on the 198 matched items native
   is 70.2 (`mcnemar.csv`, `acc_b`). The test and verdict used the matched 198.
3. **Gate 1 "Hint" and the M4c "Confound" bullet:** natural tokens per word (sentiment: 3.15–4.29) are on 198 texts,
   ITRANS and lossy on 200 (2 extra texts). The paper's main sentiment panel keeps this structure, because natural
   cannot exist for the 2 defective items; its caption states n = 200, natural n = 198. A strictly matched 198-item
   tokens-per-word comparison has not been computed.
4. **M4c reading, "Gate 1 (accuracy) still had native > natural in every model":** read from the unmatched table. On
   the matched items native > natural in every model on sentiment, but Qwen3.5 XNLI is a tie (34.2 vs 34.2, n = 193).
5. **Definition note (2026-10-15), "natural romanization … scores about the same as ITRANS"** (already superseded by
   the 2026-10-22 correction): based on the unmatched table.
None of these was a registered test, and no verdict changes. The paper's main tables now use matched items
(`results/matched/`, `scripts/matched_samples.py`, descriptive, no verdict; full-sample results go to appendix tables).

---
`````

##### 2026-10-23 — Exploratory note result: English share of ITRANS (registered 15:44 IST; exploratory, no verdict)

RESULTS.md lines 2391 to 2395; first line committed in `5064f46` on 2026-10-23 15:52:38 +0530; last line in `5064f46` on 2026-10-23 15:52:38 +0530; labels from the title and parent heading: exploratory, result

`````text
## 2026-10-23 — Exploratory note result: English share of ITRANS (registered 15:44 IST; exploratory, no verdict)
`results/h1lf/itrans_share.json`. Hindi ITRANS minus Kannada ITRANS English share, same ids: retrieval +0.049
[0.041, 0.057], SIB +0.050 [0.042, 0.058], sentiment +0.053 [0.044, 0.061]. **Not near zero.** Items with any match:
Hindi 187/246, Kannada 55/246 (retrieval set). Since ITRANS adds no loans, the measure itself flags Hindi words.

`````

##### 2026-10-23 — Diagnostic of the English-word measure (post hoc descriptive, dated, no verdict)

RESULTS.md lines 2396 to 2416; first line committed in `5064f46` on 2026-10-23 15:52:38 +0530; last line in `6867631` on 2026-10-23 16:00:59 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-23 — Diagnostic of the English-word measure (post hoc descriptive, dated, no verdict)
Most frequent matches (wordfreq English, Zipf ≥ 3, longer than 3 characters) on the 493 retrieval rows:
- **Hindi ITRANS (821 matches):** aura (और, 296), para (पर, 136), kara, karate, vale, jane, hone, hara, anya, mana —
  native Hindi words.
- **Hindi natural (1,238):** mein (में, 169), hone, logo, anya, jane, mana, band, agar, bare, karan, vale — native Hindi
  words — mixed with real loans (police, team, airline, design, million).
- **Kannada natural (518):** ella, matte, andre, vega, bali, sari (Kannada words) mixed with loans (police, british,
  website, internet, station). Kannada ITRANS: 133.
- **Consequence:** the addendum's English-word share and loan-free subset, option 2's δ, and option 1's registered
  loan-free subset all count native words (in Hindi far more than Kannada) as English. Option 2's intercept is
  therefore "at equal flagged-word share", not at equal loan share. The registered verdicts above stand as computed;
  this note qualifies what the measure means. No definition was changed. The option 1 analysis (`analyse1`) is held
  until Aarnav decides whether to keep or revise the definition (drafts and scoring are queued; they do not depend on
  it).

### Queue (2026-10-23 15:50 IST)
`ShatteredScripts_h1lf` (`scripts/h1lf_chain.sh`): waits for K3b (Kannada), then SIB-1,004 drafts both languages, then
scoring (4 models × 2 languages); stops before `analyse1`. `ShatteredScripts_k3bhi` re-queued to wait for the H1-LF
drafts marker (it was waiting, no request had been made).

---
`````

##### 2026-10-23 — v2 recomputations (post hoc descriptive, dated, no verdict)

RESULTS.md lines 2516 to 2540; first line committed in `7443e57` on 2026-10-23 16:12:55 +0530; last line in `7443e57` on 2026-10-23 16:12:55 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-23 — v2 recomputations (post hoc descriptive, dated, no verdict)
Outputs `results/h1lf/{v2_posthoc.json, h1_loanfree_v2_posthoc.csv, opt2_v2_posthoc*.csv/json}`.
- **Sanity list (top 20 v2 words, natural texts).** Kannada: collar, table, home, internet, lens, police, british,
  august, french, website, play, dark, cooler, buckle, water, star, brush, traffic, video, roman. Hindi: quality,
  design, police, system, video, sound, content, skin, film, material, control, collar, product, team, italy, japan,
  airline, show, table, dark. All are English loans or names; the native-word collisions of v1 (mein, aura, ella,
  matte) are gone.
- **English share, natural Hindi minus natural Kannada (v2):** retrieval +0.005 [−0.005, +0.015] (v1: +0.040);
  SIB +0.023 [0.012, 0.034] (v1: +0.050); sentiment +0.084 [0.070, 0.099] (v1: +0.106). Loan-free in both
  languages: retrieval 97 of 246, SIB 74 of 256, sentiment 21 of 197 (v1: 41 of 246, 31, 6).
- **Loan-free H1 (v2; rule outcome descriptive):**
  - retrieval (D = 172 rows, 97 test): rule met, 2 of 3 positive (Qwen3.5 0.485 [0.381, 0.588]; Gemma 4 0.258
    [0.165, 0.351]; Sarvam-1 0.021 [−0.021, 0.062]);
  - SIB (n = 74): not met, 1 of 4 positive (Gemma 4 0.270 [0.108, 0.419]); Qwen3.5 0.149 [0.000, 0.297] and Qwen3
    0.149 [0.000, 0.284], Holm p 0.156; Sarvam-1 0.027;
  - sentiment (n = 21): not met, 0 of 4.
- **Option 2 with v2 δ (rule outcome descriptive):** same outcomes as the registered option 2: retrieval met (2 of 3:
  Qwen3.5 intercept 0.431 [0.363, 0.499], Gemma 4 0.261 [0.205, 0.322]); SIB met (3 of 4: Qwen3 0.149, Qwen3.5 0.140,
  Gemma 4 0.164, all CIs exclude 0); sentiment not met (2 of 4: Qwen3 0.213, Gemma 4 0.129). Slopes with v2 are
  positive and their CIs exclude 0 for retrieval (Qwen3.5 1.65, Sarvam-1 0.45, Gemma 4 1.39) and SIB Qwen3 (0.84):
  items where Hindi carries more real loans show larger Hindi advantages, but the intercept at equal loan share
  stays positive. δ ≤ 0 for 63% (retrieval), 51% (SIB), 24% (sentiment) of items, so the intercept is not an
  extrapolation on retrieval and SIB. Continuous-outcome intercepts: CIs exclude 0 for every counted cell except
  Sarvam-1 SIB (0.144 [−0.058, 0.347]).

`````

##### 2026-10-26 01:35 IST — B part 1 back to the registered blind condition; how the anchoring comparison is read (Aarnav)

RESULTS.md lines 2818 to 2827; first line committed in `b47fdb8` on 2026-10-26 01:58:12 +0530; last line in `4cb7644` on 2026-10-26 02:35:53 +0530; labels from the title and parent heading: none

`````text
## 2026-10-26 01:35 IST — B part 1 back to the registered blind condition; how the anchoring comparison is read (Aarnav)
- **B part 1 shows the Kannada sentence only** (no English, no drafts), as in the registered blind condition
  (deviation (b), 2026-10-22). The English column of the 01:15 build is removed; B_part1.zip rebuilt. A's and B part
  2's workbooks are unchanged.
- **Reading of the anchoring comparison.** Annotator A sees the English sentence and the Gemini draft; B's blind 40 are
  written from the Kannada alone. So B blind vs A verified reflects seeing the draft **plus** seeing the English, not
  the draft alone, and is reported that way (also in `merge_xlsx.py anchor` output). B blind vs the Gemini draft is
  unaffected by this.

---
`````

##### 2026-10-26 03:10 IST — Merge of A's verification

RESULTS.md lines 2889 to 2905; first line committed in `d5c0167` on 2026-10-26 03:13:39 +0530; last line in `d5c0167` on 2026-10-26 03:13:39 +0530; labels from the title and parent heading: none

`````text
## 2026-10-26 03:10 IST — Merge of A's verification
`annotation/merge_xlsx.py A annotation/xlsx/annotator_A_filled.xlsx --final` → `annotation/results/annotator_A.csv`
(+ `_flags.csv`, `_invalid.csv`, `_quality.json`).
- **Integrity vs the build** (`annotator_A.xlsx`, commit 852f0c2): every item ID, Kannada, English and Gemini draft cell
  and all 3 example rows are identical (0 of 2,540 cells differ: 500 items × 5 locked columns, plus the header and the 3 example rows in full; value and type compared); the header and READ_ME are
  unchanged; no cells outside the layout. Sheet protection was removed on the items sheet (not refused, as instructed).
- **Counts (500 items, examples excluded):** natural fine 472, wrong 28; Kanglish fine 473, wrong 27. Empty cells 0;
  invalid cells 0; identical fixes repeated across rows 0.
- **AutoCorrect check:** 48 flags, all R1 (a sentence starting with a capital), 4 in natural fixes and 44 in Kanglish
  fixes; 41 are not in the draft. In the 28 wrong natural items the drafts have 14 sentence-initial capitals and the
  fixes 4; in the 27 wrong Kanglish items 32 and 44. Capitals added at sentence starts are consistent with Excel's
  "Capitalize first letter of sentences" or deliberate typing; not fixed (no R2 or R3 flags).
- **indicsentiment-test-249, natural fix: a paraphrase that drops content** (54 → 36 words; e.g. "ondata", "ellarigu",
  the check-in/check-out timings are dropped). Kept in the data and marked in the release notes; **not used in the
  natural_verified experiments: the draft is used for this item** (substitution logged in the verified-text build).

---
`````

##### 2026-10-26 03:45 IST — Rules (Aarnav)

RESULTS.md lines 2958 to 2971; first line committed in `07ba540` on 2026-10-26 03:26:12 +0530; last line in `46bd82a` on 2026-10-26 12:10:58 +0530; labels from the title and parent heading: none

`````text
## 2026-10-26 03:45 IST — Rules (Aarnav)
- **Wording.** In RESULTS.md and the paper, "human verified" applies only to the annotated subset: sentiment 198 items
  and FLORES 300 items, of which 80 overlap the M4c sample. Never state that the natural alignment (M4c retrieval) or
  natural accuracy results as a whole are human verified; V-VER replaces the natural text only for those items.
- **Standing rule, GPU queue.** When the H1-LF SIB-1004 drafts complete, H1-LF scoring goes ahead of everything queued,
  but a model already running is never interrupted (`wait_h1lf` in `scripts/chainlib.sh`, called before every model
  load of other chains; EP-R, started before the rule, finishes before the drafts can complete).
- **V-VER, changed to splicing (before any V-VER run):** retrieval and SIB-257 recompute only the items whose verified
  text differs (3 sentences each) and splice them into the stored per-item results; 2 unchanged items per model are
  recomputed as a control and must reproduce the stored vectors / log-probs (|Δ| < 1e-3). Sentiment is scored in full
  (18 changed items). Chain `scripts/vver_chain.sh`, queued after EP-R. The K1/K2 pilot is held until Aarnav approves
  the implementation details.

---
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

##### 2026-10-27 03:00 IST — Writing decisions for the TMLR draft (Aarnav)

RESULTS.md lines 3146 to 3159; first line committed in `2a9fec3` on 2026-10-27 02:45:12 +0530; last line in `488d268` on 2026-10-27 02:47:32 +0530; labels from the title and parent heading: none

`````text
## 2026-10-27 03:00 IST — Writing decisions for the TMLR draft (Aarnav)
- **Related work** states the RomanLens point head-on: if concepts are encoded similarly across scripts, the native versus romanized
  gap in reading points to the familiarity of the input form (exposure in training) rather than to a script-specific latent space;
  the scope note (we do not test the output-script setting) is kept.
- **Length:** the TMLR action-editor guidelines give a longer review period for submissions over 12 pages excluding the appendix;
  the paper stays at or under 12 pages of main text.
- **Supplementary package** includes the Gemini drafts and the verification data (anonymized) for reviewers; the public release
  remains upon acceptance.
- **Appendix statement:** "An AI coding assistant was used for code and drafting; the authors verified all content and results."
- **Human subjects:** if no IRB exists, the paper states that no IRB review was obtained, that annotators were volunteers who gave
  informed consent, and that no personal data were collected; the pool details are to be provided by the lead author (the
  Broader Impact Statement carries this text and is to be confirmed against them before submission).

---
`````

##### 2026-10-28 03:50 IST — Network-outage robustness for the chains (Aarnav, 2026-10-28)

RESULTS.md lines 3213 to 3226; first line committed in `126a488` on 2026-10-28 03:46:10 +0530; last line in `ca5c2e9` on 2026-10-28 05:39:02 +0530; labels from the title and parent heading: none

`````text
## 2026-10-28 03:50 IST — Network-outage robustness for the chains (Aarnav, 2026-10-28)
**Incident:** a network outage (`getaddrinfo failed`) failed the H1-LF drafts step and the chain wrote FAILED; the K3b-hi chain saw that
marker and stopped, although the scheduler restarted H1-LF itself on logon and it finished. **Rule now:** a network failure is
retried with backoff; it never writes FAILED and never stops a downstream chain.
- `src/shattered/llm/client.py`: network errors (ConnectError, timeouts, resets, `getaddrinfo failed`, anywhere in the exception chain)
  are classified RetryableError, so the existing in-process backoff (6 retries, up to 120 s) covers short outages.
- `scripts/chainlib.sh`: `run_net` re-runs a step whose new log lines carry a network signature or when the Gemini endpoint does not
  answer, with exponential backoff (60 s doubling, cap 30 min, at most 48 retries, status WAITING "network outage ... retry n in s");
  quota (exit 3) and other failures pass through unchanged. `upstream_dead`: an upstream FAILED or DEAD stops a downstream chain only after
  30 minutes without recovery (also used by `wait_h1lf`). Tested on fake steps (network x2 then success; bug; quota; retry cap; grace timer).
- `scripts/k3bhi_chain.sh` now uses both; relaunched 03:45 IST (API only, resumes from the cache; 154 of 900 drafts were already
  done). `scripts/h1lf_chain.sh` is mid-GPU-scoring and is not edited while it runs; its remaining steps need no network. It is patched
  after it finishes. Chains that already finished keep their old scripts.

`````

##### 2026-10-30 — Repo cleanup (Aarnav's decisions of 2026-10-30; plan in docs/CLEANUP_PLAN.md; archive manifest in ../shattered-scripts-archive/MANIFEST.md)

RESULTS.md lines 3310 to 3321; first line committed in `a5a446e` on 2026-10-30 01:11:23 +0530; last line in `f7ce5a8` on 2026-10-30 08:18:15 +0530; labels from the title and parent heading: none

`````text
## 2026-10-30 — Repo cleanup (Aarnav's decisions of 2026-10-30; plan in docs/CLEANUP_PLAN.md; archive manifest in ../shattered-scripts-archive/MANIFEST.md)
- First step: unregistered the 11 finished scheduled tasks (all chain statuses DONE); `ShatteredScripts_k3bhi` and `ShatteredScripts_watch` remain.
- Moved out of the repo (146 items, 7,184 MB): E5 `last.pt` (18), mid-training snapshots (54) and pilot checkpoints; M14 pilot and smoke activations;
  `results/m14_smoke`; logs and status files of finished chains; E9 search intermediates; 10 unused figure sets; the empty `paper/references.bib`;
  the Kaggle notebook; 4 one-off scripts. Kept: the 18 `final.safetensors` (the only E5 files any script loads), all gate-pilot results, all
  scripts that imported or produced a reported result (8 of the 12 archive candidates stayed, reasons in the README table and the manifest).
- Committed the previously untracked evidence: SIB-1004 drafts, `results/h_hindi/scores`, `results/nc1/scores`, `results/k3b`, `results/k3b_hi`.
  Untracked the four K2b vector files (kept on disk, in `.gitignore`; README gives the regeneration command).
- Verified: paper builds, 0 LaTeX errors; `check_numbers` 0 mismatches on all 12 sections; 14 analysis scripts re-run from the cleaned repo reproduce
  the committed outputs (identical apart from provenance fields); anonymized package rebuilt, 0 identifying hits, no vectors, no archive paths.

---
`````

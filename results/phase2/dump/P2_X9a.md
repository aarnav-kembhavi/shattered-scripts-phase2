# X9a: Tiny GPT, familiarity manipulated, fragmentation fixed; X9a-low and extra seeds (Phase 2)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3531-3573 | X9a. Tiny GPT, familiarity manipulated, fragmentation fixed (laptop) |
| result | `00bf9f6` | 2026-11-03 13:21:59 +0530 | 3838-3840 | 2026-11-03 13:21 IST, X9a prep and pilot (laptop; registered pilot first; results are checks, no accuracy is used for any decision). |
| result | `3290232` | 2026-11-04 01:44:01 +0530 | 3856-3856 | 2026-11-04 01:44 IST, X9a FINISHED (15 of 15 runs, laptop, finished 3 Nov 19:04 IST; `scripts/x9a.py analyse`, `results/phase2/x9a/analysis.json`): X9a-R REFUTE |
| registered, exploratory, result | `28803e6` | 2026-11-04 02:33:57 +0530 | 3860-3860 | 2026-11-04 02:33 IST, X9a-low REGISTERED (laptop; exploratory follow-up, added after seeing the X9a-R ceiling; the X9a-R verdict is unchanged and is not rerun). |
| none | `28803e6` | 2026-11-04 02:33:57 +0530 | 3861-3861 | 2026-11-04 02:33 IST, X9a level-0 observation (descriptive only, no rule). |
| none | `eff85fe` | 2026-11-04 02:34:12 +0530 | 3864-3865 | 2026-11-04 02:34 IST, correction note to the X9a-low entry above (text only; the rule is unchanged). |
| exploratory, result | `7bcba7d` | 2026-11-04 20:22:41 +0530 | 3922-3922 | 2026-11-04 20:22 IST, X9a-low RESULT (laptop, finished 20:21 IST; 12 new runs plus the X9a level 0 and level 1 runs; `scripts/x9a.py analyse_low`, `results/phas |
| result | `3c30aee` | 2026-11-04 20:44:16 +0530 | 3928-3928 | 2026-11-04 20:44 IST, X9a cipher token counts (descriptive; `results/phase2/x9a/cipher_tokens.json`, `scripts/x9a_cipher_tokens.py`). |
| result | `2f9c9f1` | 2026-11-05 15:37:57 +0530 | 4009-4010 | 2026-11-05 15:37 IST, X9a-low EXTRA SEEDS FINISHED (added after seeing the original seeds; registered above on 2026-11-05; laptop; `x9a_p{0p1,0p3,1}_s{3,4}.json |
| none | `c7f6e92` | 2026-11-05 15:39:07 +0530 | 4013-4014 | 2026-11-05 15:39 IST, CORRECTION NOTE to the X9a-low extra-seed entry above (one phrase). |
| result | `82e4226` | 2026-11-07 03:52:42 +0530 | 4044-4045 | 2026-11-07 03:52 IST, X9a-LOW EXTRA SEEDS, SECOND SET, FINISHED (added after seeing the originals; registered 2026-11-07; levels 0, 0.01% and 0.03%, code seeds  |

## Values observed in the result files (read from the files' own columns and keys)

- seeds: 0, 1, 2, 3, 4, 0.1, 1.0, 0.02, 0.04, 0.46, 0.024, 0.036, 0.052, 0.064, 0.068, 0.072, 0.112, 0.116, 0.172, 0.432, 0.988, 0.992, 0.996
- level: 0, 1, 5, 20, 50, 0p1, 0p3, 0p01, 0p03

Result directories: `results/phase2/x9a`

## RESULTS.md entries, verbatim

##### X9a. Tiny GPT, familiarity manipulated, fragmentation fixed (laptop)

RESULTS.md lines 3531 to 3573; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: amended

`````text
### X9a. Tiny GPT, familiarity manipulated, fragmentation fixed (laptop)

**Cipher.** A deterministic bijection on letters: ASCII a-z map to the first 26 Cyrillic lowercase letters (U+0430 to U+044F) by the
permutation `default_rng(9).permutation(26)`, A-Z to the same letters in Cyrillic capitals; digits, punctuation, spaces, newlines unchanged.
The inverse is built and the round trip is checked on every story used (all exact, otherwise nothing runs).

**Corpus and splits.** TinyStories V2, the Phase 1 E5 stream and order (`data_seed` 0, `configs/e05_pretrain.yaml`). *Evaluation:* the first
500 stories of the TinyStories V2 validation split, each as an English text and a cipher text (parallel pairs), truncated to the first 700
characters of the English story and the same positions of the cipher text; disjoint from every training and tokenizer story (exact match,
count reported, must be 0). *Exposure:* one random order of the training stories (`default_rng(9)`) is fixed; exposure p in {0, 1, 5, 20, 50}
percent replaces the first p percent of that order by their cipher renderings (nested sets). A story is seen in one rendering only, so there
is **no parallel supervision**; level 0 is the Phase 1 English stream.

**Tokenizer (one, fixed).** Byte-level BPE, 1,024 tokens, the Phase 1 recipe (`src/shattered/pretrain/data.py`), trained once on a fixed
100 MB mixture of **50 MB English stories and 50 MB cipher renderings of other stories** (disjoint from the evaluation stories, drawn before the
exposure order), and reused unchanged at all levels and seeds, so the segmentation of every text is identical across levels. **Reported before
any model is trained: English tokens per word and cipher tokens per word on the evaluation stories (expected near equal; if they differ by more
than 15 percent relative, this is reported and the run goes on, with the ratio stated in every table), and the sha256 of the tokenizer.**

**Models and budget.** The Phase 1 tiny GPT (8 layers, d_model 384, 6 heads), vocabulary 1,024, Phase 1 optimizer, schedule and evaluation
cadence, the same number of optimizer steps and tokens per step as the Phase 1 vocabulary-1,024 runs. Levels may consume slightly different
numbers of stories (cipher has more bytes per story); stories consumed per level are reported. 5 levels x 3 seeds (0, 1, 2) = 15 runs,
about 6 GPU hours (extrapolated from Phase 1 timing; pilot first: one run at level 20, seed 0, 10 percent of the budget, to check the round
trip, the tokenizer statistics and the timing).

**Measures (held-out pairs, final checkpoint).** (1) *Retrieval:* cipher story to English story, acc@1, the Phase 1 M4b protocol (mean residual per
layer, the layer chosen on the train half of the 500 pairs, seed 0, unmapped retrieval on the test half of 250; the mapped value is secondary).
Chance is 1/250. (2) *Assembly:* the Phase 1 MDL word-identity probe (`bootstrap_mdl_detok`, fraction 0.9) on cipher words: the 300 most frequent
space-preceded alphabetic words of the evaluation cipher texts that are at least 3 tokens under the X9 tokenizer (if fewer than 300, at least 2
tokens; the only fallback), up to 40 occurrences each, at most 2 per story; the same selection on English is probed as a descriptive reference.

**Prediction and decision rules.** Level 0 is **not** part of either rule: its cipher embeddings are untrained, so retrieval there is at chance
by construction (reported, expected within the bootstrap interval of 1/250), and its assembly layer is reported descriptively.
- **X9a-R (retrieval follows exposure).** Prediction: seed-mean retrieval rises monotonically with exposure from 1 percent upward. *Supported:* the
  seed means at 1, 5, 20, 50 are non-decreasing and mean(50) - mean(1) exceeds 3 times the larger of the two seed SDs (SD floor 1/250).
  *Refuted:* mean(50) <= mean(1), or the Spearman correlation between level and seed mean over the four levels is 0.6 or lower. *Inconclusive:* otherwise.
- **X9a-A (assembly layer is flat).** Prediction: the seed-mean MDL detok layer for cipher words varies by at most 1 layer across levels 1 to 50.
  *Supported:* max minus min of the four seed-mean detok layers is at most 1. *Refuted:* at least 2. *Inconclusive:* more than one run at a level has an
  undefined detok layer (counted and reported).
- **Joint reading (only if both are decided):** R supported and A supported = "familiarity moves meaning alignment while word assembly stays put at
  fixed fragmentation"; R supported and A refuted = "exposure also moves assembly; the dissociation is not clean"; R refuted = "no familiarity
  effect in this setting" (small model, letter cipher, no claim beyond that).

`````

##### 2026-11-03 13:21 IST, X9a prep and pilot (laptop; registered pilot first; results are checks, no accuracy is used for any decision).

RESULTS.md lines 3838 to 3840; first line committed in `00bf9f6` on 2026-11-03 13:21:59 +0530; last line in `3529fe7` on 2026-11-03 13:32:32 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 13:21 IST, X9a prep and pilot (laptop; registered pilot first; results are checks, no accuracy is used for any decision).** `scripts/x9a.py prep` (CPU, `results/phase2/x9a/prep.json`): **cipher round trip exact on every story used (0 failures) and 0 evaluation stories occur in the training or tokenizer stories** (checked by exact match; the 500 evaluation stories are the first 500 of the TinyStories V2 validation split); tokenizer: byte-level BPE 1,024 (+EOS), trained once on 50.0 MB English (61,923 stories) plus 50.0 MB cipher renderings (35,320 other stories) taken from the shuffled stories beyond the 400 MB training prefix; **sha256 0bcd40849208725e0b3d43cb3836ad147210c6e96418d3f197a625ff97324acf**. **Tokens per word on the evaluation stories: English 1.773, cipher 1.978 (relative difference 11.6%, inside the 15% bound; the ratio 1.116 is stated in every table).** Streams (each cut at 126,423,041 tokens = 6,173 steps x 64 x 320, the Phase 1 vocabulary-1,024 budget): stories consumed 435,911 (level 0), 435,402 (1), 433,370 (5), 425,916 (20), 411,712 (50), of which cipher 0, 4,344, 21,634, 85,246, 205,952 (shares 0, 1.0%, 5.0%, 20.0%, 50.0%).
  **Pilot** (level 20, seed 0, 617 steps = 10% of the budget; `results/phase2/x9a/pilot.json`): 0.157 s per step, 97 s of training, evaluation 90 s; the whole path ran (retrieval, MDL probes on cipher and English words, 300 words each at least 3 tokens). **Time estimate for the grid: 6,173 steps x 0.157 s = 0.27 h per run, 15 runs = 4.0 h plus about 0.4 h of evaluation (the registration extrapolated about 6 h).** **Implementation note (X9a-D1, no rule change):** the registered 700-character evaluation texts exceed the model's 320-token context for some stories; the pair is cut further at a word boundary, the same characters in English and cipher, for 17 of the 500 pairs (mean 654 characters, minimum 241), identical in every run (the tokenizer is fixed); `ctx_tokens` was added to the Phase 1 training code as an optional override so every level uses the Phase 1 context of 320 (Phase 1 runs are unaffected). The mapped retrieval value (secondary in the registration) is not computed in this version. The full grid is started now (`scripts/x9a_chain.sh`).

`````

##### 2026-11-04 01:44 IST, X9a FINISHED (15 of 15 runs, laptop, finished 3 Nov 19:04 IST; `scripts/x9a.py analyse`, `results/phase2/x9a/analysis.json`): X9a-R REFUTED by the registered rule (against the prediction); X9a-A SUPPORTED.

RESULTS.md lines 3856 to 3856; first line committed in `3290232` on 2026-11-04 01:44:01 +0530; last line in `3290232` on 2026-11-04 01:44:01 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 01:44 IST, X9a FINISHED (15 of 15 runs, laptop, finished 3 Nov 19:04 IST; `scripts/x9a.py analyse`, `results/phase2/x9a/analysis.json`): X9a-R REFUTED by the registered rule (against the prediction); X9a-A SUPPORTED.** *Retrieval, cipher story to English story, unmapped, test half n = 250, chance 0.004, seeds 0/1/2:* level 0: 0.024, 0.020, 0.040 (mean 0.028; **not at chance as the registration expected: the best layer is 0 or 1, where digits, punctuation and spaces, which the cipher leaves unchanged, are shared**); level 1: 1.000, 0.992, 0.988 (mean 0.9933); level 5: 1.000 x3 (1.0000); level 20: 1.000, 0.996, 1.000 (0.9987); level 50: 1.000, 1.000, 0.996 (0.9987). **X9a-R:** means at 1, 5, 20, 50 are not non-decreasing; mean(50) - mean(1) = +0.0053 against 3 x the larger seed SD (floor 1/250) = 0.0183; Spearman(level, seed mean) over the four levels = 0.32, which is 0.6 or lower: **refuted** by the registered rule. **Observation, not a verdict: retrieval is at its ceiling (0.99 to 1.00) from 1 percent exposure upward, so the rule could not see a rise; it jumps from 0.028 at level 0 to 0.993 at level 1.** The registered joint reading for "R refuted" is "no familiarity effect in this setting (small model, letter cipher, no claim beyond that)"; the ceiling means this setting cannot show a graded effect above 1 percent, and the level-0 versus level-1 jump is not covered by either rule. *Assembly (MDL detokenization layer of cipher words, 300 words, seeds 0/1/2):* level 0: 0, 0, 0 (descriptive); level 1: 2, 1, 1 (mean 1.33); levels 5, 20, 50: 1, 1, 1; English reference words: 1 at every level. **X9a-A:** max minus min of the four seed means (levels 1 to 50) = 0.33 <= 1: **supported**. **Joint reading (registered): "no familiarity effect in this setting".** Validation BPB on English falls with exposure only in cost: 0.561 to 0.564 (level 0), 0.563 to 0.566 (1), 0.566 to 0.570 (5), 0.574 to 0.581 (20), 0.619 to 0.622 (50). The paper is not edited.
`````

##### 2026-11-04 02:33 IST, X9a-low REGISTERED (laptop; exploratory follow-up, added after seeing the X9a-R ceiling; the X9a-R verdict is unchanged and is not rerun).

RESULTS.md lines 3860 to 3860; first line committed in `28803e6` on 2026-11-04 02:33:57 +0530; last line in `28803e6` on 2026-11-04 02:33:57 +0530; labels from the title and parent heading: registered, exploratory, result

`````text
- **2026-11-04 02:33 IST, X9a-low REGISTERED (laptop; exploratory follow-up, added after seeing the X9a-R ceiling; the X9a-R verdict is unchanged and is not rerun).** *Motivation:* X9a retrieval was already 0.993 at 1 percent exposure and 0.28 at level 0 was chance-like only by construction, so the X9a-R rule could not see a graded effect. *Design:* same tiny GPT, same fixed 1,024 tokenizer, same cipher, evaluation pairs, measures (retrieval and MDL assembly) and seeds 0, 1, 2 as X9a; **new exposure levels 0.01, 0.03, 0.1 and 0.3 percent** (cipher stories = round(n_train x level / 100) of the same story order, , each stream cut at the same 126,423,041 tokens); the existing X9a level 0 and level 1 runs supply the other two of the six levels (levels 0, 0.01, 0.03, 0.1, 0.3, 1). 12 new runs, about 0.3 GPU hours each. **Decision rule (written before any X9a-low run):** "dose-response present" if the Spearman correlation between exposure level and seed-mean retrieval across all six levels is at least 0.8 **and** mean retrieval at 1 percent minus mean retrieval at 0.01 percent is at least 0.05; otherwise "no dose-response". Reported with it, descriptively: the MDL assembly layer per level (seeds and mean) and retrieval per level and seed. *Label:* motivated by the X9a-R ceiling, added after seeing it; exploratory.
`````

##### 2026-11-04 02:33 IST, X9a level-0 observation (descriptive only, no rule).

RESULTS.md lines 3861 to 3861; first line committed in `28803e6` on 2026-11-04 02:33:57 +0530; last line in `28803e6` on 2026-11-04 02:33:57 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 02:33 IST, X9a level-0 observation (descriptive only, no rule).** Level-0 retrieval will additionally be reported on evaluation pairs with digits and punctuation removed from both the English and the cipher texts (the characters the cipher leaves unchanged), same seeds and checkpoints, layer chosen on the train half as in X9a.
`````

##### 2026-11-04 02:34 IST, correction note to the X9a-low entry above (text only; the rule is unchanged).

RESULTS.md lines 3864 to 3865; first line committed in `eff85fe` on 2026-11-04 02:34:12 +0530; last line in `98e2256` on 2026-11-04 02:46:00 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 02:34 IST, correction note to the X9a-low entry above (text only; the rule is unchanged).** A shell substitution dropped a code span: the phrase "of the same story order, , each stream" should read "of the same story order, `default_rng(9)`, each stream". Nothing else in the entry changed; the tag `phase2-x9a-low` marks the entry as committed.

`````

##### 2026-11-04 20:22 IST, X9a-low RESULT (laptop, finished 20:21 IST; 12 new runs plus the X9a level 0 and level 1 runs; `scripts/x9a.py analyse_low`, `results/phase2/x9a/analysis_low.json`): "dose-response present" by the registered rule (expl

RESULTS.md lines 3922 to 3922; first line committed in `7bcba7d` on 2026-11-04 20:22:41 +0530; last line in `7bcba7d` on 2026-11-04 20:22:41 +0530; labels from the title and parent heading: exploratory, result

`````text
- **2026-11-04 20:22 IST, X9a-low RESULT (laptop, finished 20:21 IST; 12 new runs plus the X9a level 0 and level 1 runs; `scripts/x9a.py analyse_low`, `results/phase2/x9a/analysis_low.json`): "dose-response present" by the registered rule (exploratory, motivated by the X9a-R ceiling and added after seeing it).** Registered rule (written before any run): present if the Spearman correlation between exposure and seed-mean retrieval over the six levels is at least 0.8 and mean(1%) minus mean(0.01%) is at least 0.05. **Spearman = 1.00; mean(1%) - mean(0.01%) = +0.951** (both met). Retrieval, cipher story to English story, unmapped, test half n = 250, chance 0.004, seeds 0/1/2 and mean: 0%: 0.024, 0.020, 0.040 (0.028); 0.01%: 0.036, 0.052, 0.040 (0.043); 0.03%: 0.072, 0.068, 0.064 (0.068); 0.1%: 0.100, 0.116, 0.112 (0.109); 0.3%: 0.432, 0.460, 0.172 (0.355; seed 2 is a low outlier); 1%: 1.000, 0.992, 0.988 (0.993). Retrieval rises monotonically with exposure over three orders of magnitude and saturates between 0.3 and 1 percent, which is why the X9a-R rule (1 to 50 percent) could not see it. **MDL assembly layer of cipher words (seeds 0/1/2; descriptive): 0%: 0, 0, 0; 0.01%: 0, 0, 0; 0.03%, 0.1%, 0.3%, 1%: 2, 1, 1 at each (mean 1.33).** So meaning alignment is graded in exposure while the assembly layer, once the cipher letters are learned at all (from 0.03%), does not move with further exposure: the X9a-A pattern extends down to 0.03%. The registered X9a-R verdict (refuted) and the joint reading stay as logged; this entry adds the graded effect below the ceiling. Nothing against a prediction (no prediction was registered for X9a-low). **Level-0 observation (descriptive only, `results/phase2/x9a/level0_stripped.json`):** with digits and punctuation removed from both texts, level-0 retrieval at the train-chosen layer is 0.004, 0.008, 0.016 (mean 0.009; chance 0.004) against 0.024, 0.020, 0.040 unstripped (mean 0.028): most of the above-chance level-0 retrieval came from the characters the cipher leaves unchanged. The paper is not edited.
`````

##### 2026-11-04 20:44 IST, X9a cipher token counts (descriptive; `results/phase2/x9a/cipher_tokens.json`, `scripts/x9a_cipher_tokens.py`).

RESULTS.md lines 3928 to 3928; first line committed in `3c30aee` on 2026-11-04 20:44:16 +0530; last line in `3c30aee` on 2026-11-04 20:44:16 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 20:44 IST, X9a cipher token counts (descriptive; `results/phase2/x9a/cipher_tokens.json`, `scripts/x9a_cipher_tokens.py`).** Cipher tokens in each stream of 126,423,042 tokens (cipher stories re-encoded with the fixed tokenizer, EOS included; the count is untruncated and cannot exceed the true count by more than one story, and the last story was English at every level): 0%: 0; 0.01%: 14,637 (43 stories); 0.03%: 42,245 (129); 0.1%: 137,613 (428); 0.3%: 424,425 (1,305); 1%: 1,405,615 (4,344); 5%: 7,011,185 (21,634); 20%: 27,640,583 (85,246); 50%: 66,714,543 (205,952). Share of the stream by tokens: 0.012%, 0.033%, 0.109%, 0.336%, 1.11%, 5.5%, 21.9%, 52.8%. **Parallel pairs: none.** Every training story appears once, either in English or as its letter-cipher rendering, never both; the English and cipher tokenizer data were different stories; the evaluation pairs (the first 500 validation stories, in both forms) are held out of training and of the tokenizer (overlap 0, checked in the X9a prep). Cipher exposure is monolingual cipher text only.
`````

##### 2026-11-05 15:37 IST, X9a-low EXTRA SEEDS FINISHED (added after seeing the original seeds; registered above on 2026-11-05; laptop; `x9a_p{0p1,0p3,1}_s{3,4}.json`, code seeds 3 and 4 = seeds 4 and 5).

RESULTS.md lines 4009 to 4010; first line committed in `2f9c9f1` on 2026-11-05 15:37:57 +0530; last line in `c7f6e92` on 2026-11-05 15:39:07 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 15:37 IST, X9a-low EXTRA SEEDS FINISHED (added after seeing the original seeds; registered above on 2026-11-05; laptop; `x9a_p{0p1,0p3,1}_s{3,4}.json`, code seeds 3 and 4 = seeds 4 and 5).** The registered X9a-low verdict ("dose-response present": Spearman 1.0 over six levels, mean at 1% minus mean at 0.01% = +0.951) is unchanged and was not re-run on a different set of seeds. Per-seed unmapped retrieval (test half, n = 250; chance 0.004), original seeds 1-3 then the added seeds 4-5: **0.1%: 0.100, 0.116, 0.112 | 0.084, 0.100 (mean of 3: 0.109; of 5: 0.102, sd 0.013). 0.3%: 0.432, 0.460, 0.172 | 0.204, 0.268 (mean of 3: 0.355, sd 0.159; of 5: 0.307, sd 0.132). 1%: 1.000, 0.992, 0.988 | 0.992, 0.968 (mean of 3: 0.993; of 5: 0.988, sd 0.012).** Cipher assembly layer (detokenization layer of cipher words), seeds 1-3 | 4-5: 0.1%: 2, 1, 1 | 1, 1; 0.3%: 2, 1, 1 | 2, 2; 1%: 2, 1, 1 | 2, 2; the English-word layer is 1 in all 15 runs. **Reading: the added seeds keep the order 0.1% < 0.3% < 1% in every seed pair (no seed at 0.3% reaches the 1% range, none at 0.1% reaches the 0.3% range except that 0.3% seed 3 at 0.172 is only 0.06 above the 0.1% seeds), but the 0.3% level is the unstable one: its five seeds run from 0.172 to 0.460, with one seed (0.172) and the two added seeds (0.204, 0.268) in the lower half; the added seeds lower the 0.3% mean from 0.355 to 0.307 and the picture of a steep rise between 0.3% and 1% is unchanged.** The 1% level is the X9a level-1 stream (regenerated, sha256 checked). The paper is not edited.

`````

##### 2026-11-05 15:39 IST, CORRECTION NOTE to the X9a-low extra-seed entry above (one phrase).

RESULTS.md lines 4013 to 4014; first line committed in `c7f6e92` on 2026-11-05 15:39:07 +0530; last line in `3ecea71` on 2026-11-05 15:42:19 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 15:39 IST, CORRECTION NOTE to the X9a-low extra-seed entry above (one phrase).** In the reading the phrase "0.3% seed 3 at 0.172" should read: the third ORIGINAL seed at 0.3% (code seed 2, retrieval 0.172) is 0.06 above the 0.1% seeds (0.100 to 0.116); code seed 3 at 0.3% is 0.204. All other numbers stand.

`````

##### 2026-11-07 03:52 IST, X9a-LOW EXTRA SEEDS, SECOND SET, FINISHED (added after seeing the originals; registered 2026-11-07; levels 0, 0.01% and 0.03%, code seeds 3 and 4 = seeds 4 and 5; laptop).

RESULTS.md lines 4044 to 4045; first line committed in `82e4226` on 2026-11-07 03:52:42 +0530; last line in `c42cfd4` on 2026-11-07 04:22:43 +0530; labels from the title and parent heading: result

`````text
- **2026-11-07 03:52 IST, X9a-LOW EXTRA SEEDS, SECOND SET, FINISHED (added after seeing the originals; registered 2026-11-07; levels 0, 0.01% and 0.03%, code seeds 3 and 4 = seeds 4 and 5; laptop).** The registered X9a-low verdict (dose-response present) is unchanged and was not re-run on a different set of seeds. Per-seed unmapped retrieval (test half, n = 250; chance 0.004), original seeds 1-3 | added seeds 4-5: **level 0: 0.024, 0.020, 0.040 | 0.012, 0.032 (mean of 3: 0.028; of 5: 0.026, sd 0.011). 0.01%: 0.036, 0.052, 0.040 | 0.052, 0.052 (mean of 3: 0.043; of 5: 0.046, sd 0.008). 0.03%: 0.072, 0.068, 0.064 | 0.044, 0.088 (mean of 3: 0.068; of 5: 0.067, sd 0.016).** Cipher assembly layer (seeds 1-3 | 4-5): level 0 and 0.01%: 0 in all ten runs; 0.03%: 2, 1, 1 | 3, 1. All three levels are near the floor and every seed stays far below the 0.1% level (0.084 to 0.116) only at level 0 and 0.01%; at 0.03% the added seeds spread wider (0.044 to 0.088) than the originals (0.064 to 0.072), so the 0.03% and 0.1% ranges now touch (0.088 against 0.084). Combined with the first extra set the five-seed table is: 0%: 0.026, 0.01%: 0.046, 0.03%: 0.067, 0.1%: 0.102, 0.3%: 0.307, 1%: 0.988 (mean unmapped retrieval, five seeds each; 0.01% to 0.1% from five seeds, the same ordering as the registered three-seed means). The paper is not edited.

`````

## Result files, every number

#### `results/phase2/x9a/analysis.json` (3,194 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a (decision rules X9a-R, X9a-A)"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T13:32:53+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "analyse"]
n_runs = 15
retrieval_by_level.0.seeds = [0.024, 0.02, 0.04]
retrieval_by_level.0.mean = 0.027999999999999997
retrieval_by_level.1.seeds = [1.0, 0.992, 0.988]
retrieval_by_level.1.mean = 0.9933333333333333
retrieval_by_level.5.seeds = [1.0, 1.0, 1.0]
retrieval_by_level.5.mean = 1.0
retrieval_by_level.20.seeds = [1.0, 0.996, 1.0]
retrieval_by_level.20.mean = 0.9986666666666667
retrieval_by_level.50.seeds = [1.0, 1.0, 0.996]
retrieval_by_level.50.mean = 0.9986666666666667
assembly_cipher_by_level.0.seeds = [0, 0, 0]
assembly_cipher_by_level.0.mean = 0.0
assembly_cipher_by_level.1.seeds = [2, 1, 1]
assembly_cipher_by_level.1.mean = 1.3333333333333333
assembly_cipher_by_level.5.seeds = [1, 1, 1]
assembly_cipher_by_level.5.mean = 1.0
assembly_cipher_by_level.20.seeds = [1, 1, 1]
assembly_cipher_by_level.20.mean = 1.0
assembly_cipher_by_level.50.seeds = [1, 1, 1]
assembly_cipher_by_level.50.mean = 1.0
assembly_english_by_level.0.seeds = [1, 1, 1]
assembly_english_by_level.1.seeds = [1, 1, 1]
assembly_english_by_level.5.seeds = [1, 1, 1]
assembly_english_by_level.20.seeds = [1, 1, 1]
assembly_english_by_level.50.seeds = [1, 1, 1]
X9a_R.means.1 = 0.9933333333333333
X9a_R.means.5 = 1.0
X9a_R.means.20 = 0.9986666666666667
X9a_R.means.50 = 0.9986666666666667
X9a_R.non_decreasing = false
X9a_R.mean50_minus_mean1 = 0.005333333333333412
X9a_R.3x_larger_seed_sd = 0.018330302779823376
X9a_R.spearman_level_vs_mean = 0.316227766016838
X9a_R.verdict = "refuted"
X9a_A.seed_mean_detok_layer = [1.3333333333333333, 1.0, 1.0, 1.0]
X9a_A.max_minus_min = 0.33333333333333326
X9a_A.undefined_by_level.1 = 0
X9a_A.undefined_by_level.5 = 0
X9a_A.undefined_by_level.20 = 0
X9a_A.undefined_by_level.50 = 0
X9a_A.verdict = "supported"
joint_reading = "no familiarity effect in this setting (small model, letter cipher, no claim beyond that)"
level0_descriptive.retrieval_seeds = [0.024, 0.02, 0.04]
level0_descriptive.chance = 0.004
level0_descriptive.assembly_cipher_seeds = [0, 0, 0]
`````

#### `results/phase2/x9a/analysis_low.json` (2,347 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a-low (tag phase2-x9a-low)"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T14:51:00+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "analyse_low"]
n_runs = 18
retrieval_by_level.0.0.seeds = [0.024, 0.02, 0.04]
retrieval_by_level.0.0.mean = 0.027999999999999997
retrieval_by_level.0.01.seeds = [0.036, 0.052, 0.04]
retrieval_by_level.0.01.mean = 0.042666666666666665
retrieval_by_level.0.03.seeds = [0.072, 0.068, 0.064]
retrieval_by_level.0.03.mean = 0.068
retrieval_by_level.0.1.seeds = [0.1, 0.116, 0.112]
retrieval_by_level.0.1.mean = 0.10933333333333334
retrieval_by_level.0.3.seeds = [0.432, 0.46, 0.172]
retrieval_by_level.0.3.mean = 0.3546666666666667
retrieval_by_level.1.0.seeds = [1.0, 0.992, 0.988]
retrieval_by_level.1.0.mean = 0.9933333333333333
assembly_cipher_by_level.0.0.seeds = [0, 0, 0]
assembly_cipher_by_level.0.0.mean = 0.0
assembly_cipher_by_level.0.01.seeds = [0, 0, 0]
assembly_cipher_by_level.0.01.mean = 0.0
assembly_cipher_by_level.0.03.seeds = [2, 1, 1]
assembly_cipher_by_level.0.03.mean = 1.3333333333333333
assembly_cipher_by_level.0.1.seeds = [2, 1, 1]
assembly_cipher_by_level.0.1.mean = 1.3333333333333333
assembly_cipher_by_level.0.3.seeds = [2, 1, 1]
assembly_cipher_by_level.0.3.mean = 1.3333333333333333
assembly_cipher_by_level.1.0.seeds = [2, 1, 1]
assembly_cipher_by_level.1.0.mean = 1.3333333333333333
rule.spearman_six_levels = 1.0
rule.mean_1pct_minus_mean_0p01pct = 0.9506666666666667
rule.verdict = "dose-response present"
rule.text = "present if Spearman >= 0.8 and mean(1%) - mean(0.01%) >= 0.05, else no dose-response"
`````

#### `results/phase2/x9a/cipher_tokens.json` (3,485 bytes; first commit 7640480 2026-11-04 20:43:54 +0530)

`````text
provenance.config.note = "descriptive; stream length n_tokens + 1 = 126423041"
provenance.git_commit = "7c964e8f305f9a77b917a4f7890545c239d3895b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T15:13:16+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a_cipher_tokens.py"]
0.exposure_percent = 0.0
0.cipher_tokens_untruncated = 0
0.cipher_stories_consumed = 0
0.stories_consumed = 435911
0.stream_tokens = 126423041
0.cipher_token_share_of_stream = 0.0
0.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
0p01.exposure_percent = 0.01
0p01.cipher_tokens_untruncated = 14637
0p01.cipher_stories_consumed = 43
0p01.stories_consumed = 435908
0p01.stream_tokens = 126423041
0p01.cipher_token_share_of_stream = 0.00011577794588883525
0p01.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
0p03.exposure_percent = 0.03
0p03.cipher_tokens_untruncated = 42245
0p03.cipher_stories_consumed = 129
0p03.stories_consumed = 435898
0p03.stream_tokens = 126423041
0p03.cipher_token_share_of_stream = 0.0003341558600856627
0p03.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
0p1.exposure_percent = 0.1
0p1.cipher_tokens_untruncated = 137613
0p1.cipher_stories_consumed = 428
0p1.stories_consumed = 435864
0p1.stream_tokens = 126423041
0p1.cipher_token_share_of_stream = 0.001088512022108375
0p1.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
0p3.exposure_percent = 0.3
0p3.cipher_tokens_untruncated = 424425
0p3.cipher_stories_consumed = 1305
0p3.stories_consumed = 435758
0p3.stream_tokens = 126423041
0p3.cipher_token_share_of_stream = 0.0033571807531508437
0p3.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
1.exposure_percent = 1.0
1.cipher_tokens_untruncated = 1405615
1.cipher_stories_consumed = 4344
1.stories_consumed = 435402
1.stream_tokens = 126423041
1.cipher_token_share_of_stream = 0.01111834511242298
1.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
5.exposure_percent = 5.0
5.cipher_tokens_untruncated = 7011185
5.cipher_stories_consumed = 21634
5.stories_consumed = 433370
5.stream_tokens = 126423041
5.cipher_token_share_of_stream = 0.05545812649768486
5.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
20.exposure_percent = 20.0
20.cipher_tokens_untruncated = 27640583
20.cipher_stories_consumed = 85246
20.stories_consumed = 425916
20.stream_tokens = 126423041
20.cipher_token_share_of_stream = 0.21863564411490466
20.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
50.exposure_percent = 50.0
50.cipher_tokens_untruncated = 66714543
50.cipher_stories_consumed = 205952
50.stories_consumed = 411712
50.stream_tokens = 126423041
50.cipher_token_share_of_stream = 0.5277087346759837
50.last_story_is_cipher_so_count_may_exceed_by_less_than_one_story = false
`````

#### `results/phase2/x9a/level0_stripped.json` (1,042 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a level-0 observation (descriptive only)"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T14:49:20+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "level0_stripped"]
by_seed.0.layer = 0
by_seed.0.acc_unmapped = 0.004
by_seed.0.n_test = 250
by_seed.0.chance = 0.004
by_seed.0.unstripped_acc = 0.024
by_seed.1.layer = 0
by_seed.1.acc_unmapped = 0.008
by_seed.1.n_test = 250
by_seed.1.chance = 0.004
by_seed.1.unstripped_acc = 0.02
by_seed.2.layer = 2
by_seed.2.acc_unmapped = 0.016
by_seed.2.n_test = 250
by_seed.2.chance = 0.004
by_seed.2.unstripped_acc = 0.04
mean = 0.009333333333333334
`````

#### `results/phase2/x9a/pilot.json` (1,685 bytes; first commit 00bf9f6 2026-11-03 13:21:59 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a pilot"
provenance.git_commit = "cdef73dd89f4daf3d348941b8a144b872a880ce8-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T07:51:22+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "pilot"]
train.status = "done"
train.steps = 617
train.val_bpb_full = 0.9101846086123556
train.train_seconds_this_session = 96.78965711593628
train.wall_seconds_this_session = 105.7286376953125
train.seconds_per_step = 0.15687140537428895
eval_seconds = 90.06357216835022
retrieval_acc = 0.864
retrieval_layer = 7
assembly_cipher_layer = 1
assembly_english_layer = 1
tokenizer_checks.steps = 6173
tokenizer_checks.ctx_tokens = 320
tokenizer_checks.tokens_per_run = 126423040
tokenizer_checks.n_train_stories = 496631
tokenizer_checks.round_trip_bad = 0
tokenizer_checks.eval_overlap = 0
tokenizer_checks.tokenizer_sha256 = "0bcd40849208725e0b3d43cb3836ad147210c6e96418d3f197a625ff97324acf"
tokenizer_checks.tokenizer_vocab_with_eos = 1025
tokenizer_checks.tokens_per_word_english_eval = 1.772812793979304
tokenizer_checks.tokens_per_word_cipher_eval = 1.9775741207173854
tokenizer_checks.tpw_relative_difference = 0.11550081736406505
tokenizer_checks.tokenizer_stories.english = 61923
tokenizer_checks.tokenizer_stories.cipher = 35320
tokenizer_checks.tokenizer_stories.english_bytes = 50000477
tokenizer_checks.tokenizer_stories.cipher_bytes = 50000650
full_run_hours_estimate = 0.26886015865537854
note = "timing and path check only; no accuracy is used for any decision"
`````

#### `results/phase2/x9a/prep.json` (2,049 bytes; first commit 00bf9f6 2026-11-03 13:21:59 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.seconds = 412.304349899292
provenance.git_commit = "cdef73dd89f4daf3d348941b8a144b872a880ce8-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T07:47:09+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "prep"]
steps = 6173
ctx_tokens = 320
tokens_per_run = 126423040
n_train_stories = 496631
round_trip_bad = 0
eval_overlap = 0
tokenizer_sha256 = "0bcd40849208725e0b3d43cb3836ad147210c6e96418d3f197a625ff97324acf"
tokenizer_vocab_with_eos = 1025
tokens_per_word_english_eval = 1.772812793979304
tokens_per_word_cipher_eval = 1.9775741207173854
tpw_relative_difference = 0.11550081736406505
tokenizer_stories.english = 61923
tokenizer_stories.cipher = 35320
tokenizer_stories.english_bytes = 50000477
tokenizer_stories.cipher_bytes = 50000650
levels.x9a_p0.train_tokens = 126423041
levels.x9a_p0.stories_consumed = 435911
levels.x9a_p0.cipher_stories_consumed = 0
levels.x9a_p0.cipher_share_consumed = 0.0
levels.x9a_p1.train_tokens = 126423041
levels.x9a_p1.stories_consumed = 435402
levels.x9a_p1.cipher_stories_consumed = 4344
levels.x9a_p1.cipher_share_consumed = 0.00997698678462662
levels.x9a_p5.train_tokens = 126423041
levels.x9a_p5.stories_consumed = 433370
levels.x9a_p5.cipher_stories_consumed = 21634
levels.x9a_p5.cipher_share_consumed = 0.049920391351501024
levels.x9a_p20.train_tokens = 126423041
levels.x9a_p20.stories_consumed = 425916
levels.x9a_p20.cipher_stories_consumed = 85246
levels.x9a_p20.cipher_share_consumed = 0.20014744691441505
levels.x9a_p50.train_tokens = 126423041
levels.x9a_p50.stories_consumed = 411712
levels.x9a_p50.cipher_stories_consumed = 205952
levels.x9a_p50.cipher_share_consumed = 0.5002331727032489
`````

#### `results/phase2/x9a/prep_low.json` (1,380 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a-low"
provenance.config.seconds = 215.26616501808167
provenance.git_commit = "eb2aa7a965c3dd2268c2af56b68dcae1b1053c2a-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T10:44:02+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "prep_low"]
x9a_p0p01.train_tokens = 126423041
x9a_p0p01.exposure_percent = 0.01
x9a_p0p01.stories_consumed = 435908
x9a_p0p01.cipher_stories_consumed = 43
x9a_p0p01.cipher_share_consumed = 9.864466814098388e-05
x9a_p0p03.train_tokens = 126423041
x9a_p0p03.exposure_percent = 0.03
x9a_p0p03.stories_consumed = 435898
x9a_p0p03.cipher_stories_consumed = 129
x9a_p0p03.cipher_share_consumed = 0.0002959407934883849
x9a_p0p1.train_tokens = 126423041
x9a_p0p1.exposure_percent = 0.1
x9a_p0p1.stories_consumed = 435864
x9a_p0p1.cipher_stories_consumed = 428
x9a_p0p1.cipher_share_consumed = 0.0009819576748710606
x9a_p0p3.train_tokens = 126423041
x9a_p0p3.exposure_percent = 0.3
x9a_p0p3.stories_consumed = 435758
x9a_p0p3.cipher_stories_consumed = 1305
x9a_p0p3.cipher_share_consumed = 0.0029947815071668217
`````

#### `results/phase2/x9a/x9a_p0_s0.json` (2,411 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0_s0/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T10:10:33+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0", "0"]
run = "x9a_p0_s0"
level = 0
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.024
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.024, 0.012, 0.016, 0.008, 0.012, 0.004, 0.004, 0.004, 0.0]
retrieval.train_acc_per_layer = [0.024, 0.012, 0.012, 0.012, 0.008, 0.004, 0.004, 0.004, 0.0]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3550753225081245, 1.176317246339706, 1.1630911141424107, 1.1625921560014343, 1.160245514745326, 1.1570188079328654, 1.154329029427951, 1.1515856716016712, 1.1452115792247657]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3131568353823546, 7.592411799291914, 7.827257606456817, 7.380914996298827, 6.894280552479246, 6.313581312980673, 5.654413903773419, 5.110414573915873, 4.365737798602105]
seconds = 67.68412637710571
train.steps = 6173
train.val_bpb_full = 0.561074401692164
train.train_seconds_this_session = 1072.5168080329895
train.wall_seconds_this_session = 1128.9207575321198
`````

#### `results/phase2/x9a/x9a_p0_s1.json` (2,410 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0_s1/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T11:51:47+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0", "1"]
run = "x9a_p0_s1"
level = 0
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.02
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.02, 0.036, 0.008, 0.028, 0.024, 0.004, 0.016, 0.004, 0.004]
retrieval.train_acc_per_layer = [0.036, 0.02, 0.004, 0.004, 0.004, 0.004, 0.008, 0.012, 0.012]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.356535345545133, 1.3217044954195454, 1.2968487400755164, 1.2804913904450055, 1.28478804332495, 1.2780483279396646, 1.2697416763402953, 1.2684828899867229, 1.250661511299353]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3109684399838177, 7.883696770321735, 7.824940540805107, 7.477384755463009, 7.000547600219255, 6.674066431039931, 6.059414122396086, 5.452814756780901, 4.490058331340333]
seconds = 66.53591704368591
train.steps = 6173
train.val_bpb_full = 0.564129145504233
train.train_seconds_this_session = 1022.4024729728699
train.wall_seconds_this_session = 1075.910816669464
`````

#### `results/phase2/x9a/x9a_p0_s2.json` (2,412 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0_s2/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T13:31:36+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0", "2"]
run = "x9a_p0_s2"
level = 0
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 1
retrieval.acc_unmapped = 0.04
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.024, 0.04, 0.04, 0.028, 0.004, 0.004, 0.0, 0.008, 0.008]
retrieval.train_acc_per_layer = [0.028, 0.04, 0.028, 0.012, 0.012, 0.004, 0.004, 0.004, 0.004]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.354349434771786, 1.7683982815525625, 1.6817871568967466, 1.6600971839518688, 1.6654123848769324, 1.6527859397711429, 1.6493043553283628, 1.6355510618021079, 1.6298505690243892]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3127083051509207, 7.818982437590116, 7.927502884727645, 7.690808565861275, 6.952829998160784, 6.599759462938944, 5.911665141615839, 5.326210768345889, 4.544567339182691]
seconds = 67.03815340995789
train.steps = 6173
train.val_bpb_full = 0.5643422501968086
train.train_seconds_this_session = 1003.4021208286285
train.wall_seconds_this_session = 1055.6093802452087
`````

#### `results/phase2/x9a/x9a_p0_s3.json` (2,411 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0_s3/final.safetensors"
provenance.git_commit = "b194514597abda1c395f06cba9a976d36991a78c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T20:45:07+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0", "3"]
run = "x9a_p0_s3"
level = "0"
seed = 3
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 1
retrieval.acc_unmapped = 0.012
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.024, 0.012, 0.02, 0.016, 0.028, 0.012, 0.004, 0.0, 0.004]
retrieval.train_acc_per_layer = [0.028, 0.032, 0.024, 0.02, 0.02, 0.004, 0.008, 0.008, 0.004]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.355025784894555, 1.398321297557462, 1.3764697293489088, 1.358425617686534, 1.3572015042204262, 1.3550722658454972, 1.3486779321649922, 1.3473854310540032, 1.3388748500065264]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.314028763446803, 7.818106833987892, 7.931523362205206, 7.381932050334845, 6.706253850440465, 6.2723510249437435, 5.642041900434188, 5.014023582950301, 4.395696212518832]
seconds = 70.43645071983337
train.steps = 6173
train.val_bpb_full = 0.5609158352516372
train.train_seconds_this_session = 1021.4968814849854
train.wall_seconds_this_session = 1074.91268825531
`````

#### `results/phase2/x9a/x9a_p0_s4.json` (2,414 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0_s4/final.safetensors"
provenance.git_commit = "2466b303da0a9b230a39bbc1c3f5ce01093cd498-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T21:45:52+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0", "4"]
run = "x9a_p0_s4"
level = "0"
seed = 4
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.032
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.032, 0.02, 0.016, 0.012, 0.004, 0.004, 0.0, 0.004, 0.004]
retrieval.train_acc_per_layer = [0.032, 0.032, 0.028, 0.004, 0.008, 0.012, 0.008, 0.008, 0.004]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3551098687392504, 1.3069441303876699, 1.264757883976972, 1.2527041459818007, 1.2503717480302712, 1.2514165866089304, 1.2464025323219767, 1.2362493043871272, 1.2309169302889358]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.311230254995575, 7.810413882881482, 7.961430570529367, 7.7031459584837245, 7.315992356449191, 6.806219219925703, 6.016466458803998, 5.261103072699342, 4.454840894099617]
seconds = 68.94039845466614
train.steps = 6173
train.val_bpb_full = 0.5627701411896574
train.train_seconds_this_session = 948.3045034408569
train.wall_seconds_this_session = 998.428797006607
`````

#### `results/phase2/x9a/x9a_p0p01_s0.json` (2,416 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p01_s0/final.safetensors"
provenance.git_commit = "eb2aa7a965c3dd2268c2af56b68dcae1b1053c2a-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T11:03:04+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p01", "0"]
run = "x9a_p0p01_s0"
level = "0p01"
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 2
retrieval.acc_unmapped = 0.036
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.032, 0.032, 0.036, 0.04, 0.02, 0.024, 0.032, 0.02, 0.04]
retrieval.train_acc_per_layer = [0.028, 0.02, 0.032, 0.02, 0.024, 0.012, 0.016, 0.012, 0.032]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3260524558736386, 2.205535256327002, 2.05443680905752, 2.0222975743943152, 1.995233637972327, 1.960738390283686, 1.8860253043073167, 1.890965273705639, 1.8084996392090766]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.313241082631547, 7.664690845164565, 7.75373616683677, 7.50636287004167, 6.979079177484329, 6.423371572408383, 5.697367769260227, 5.170972725313851, 4.430171469426561]
seconds = 66.1040301322937
train.steps = 6173
train.val_bpb_full = 0.5618694713969983
train.train_seconds_this_session = 993.4723925590515
train.wall_seconds_this_session = 1045.7312350273132
`````

#### `results/phase2/x9a/x9a_p0p01_s1.json` (2,427 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p01_s1/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T12:23:49+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p01", "1"]
run = "x9a_p0p01_s1"
level = "0p01"
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.052
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.052, 0.02, 0.032, 0.016, 0.012, 0.016, 0.012, 0.012, 0.028]
retrieval.train_acc_per_layer = [0.036, 0.032, 0.032, 0.016, 0.008, 0.02, 0.028, 0.008, 0.012]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3301284075268365, 1.9720412825748113, 1.9696644265253116, 1.9133092513823307, 1.9039127954578674, 1.9000249477870503, 1.8778436825793974, 1.8276540318379957, 1.7534209370322478]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3115743821429295, 7.819669037253117, 7.743758295699, 7.386827103738001, 6.866478366469609, 6.570474337193694, 5.964586625393731, 5.34725127443954, 4.426679628185715]
seconds = 67.26785945892334
train.steps = 6173
train.val_bpb_full = 0.5641676052299036
train.train_seconds_this_session = 1024.4871258735657
train.wall_seconds_this_session = 1078.2542071342468
`````

#### `results/phase2/x9a/x9a_p0p01_s2.json` (2,424 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p01_s2/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T13:43:47+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p01", "2"]
run = "x9a_p0p01_s2"
level = "0p01"
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 2
retrieval.acc_unmapped = 0.04
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.044, 0.036, 0.04, 0.028, 0.02, 0.012, 0.016, 0.02, 0.028]
retrieval.train_acc_per_layer = [0.032, 0.016, 0.036, 0.016, 0.004, 0.016, 0.02, 0.028, 0.012]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.32758529150327, 1.8962958455840082, 1.9182045736336226, 1.8890124918323634, 1.8997479825769898, 1.8471073869512626, 1.7940006107096524, 1.777495139907388, 1.7454148660614648]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3119267467577362, 7.699060615181631, 7.914801853605208, 7.684365019318715, 7.095976352724802, 6.821302297193327, 6.083419117880742, 5.424513668337989, 4.5748398395578995]
seconds = 68.09342050552368
train.steps = 6173
train.val_bpb_full = 0.5646225354039149
train.train_seconds_this_session = 1013.126134634018
train.wall_seconds_this_session = 1065.890903711319
`````

#### `results/phase2/x9a/x9a_p0p01_s3.json` (2,428 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p01_s3/final.safetensors"
provenance.git_commit = "acd0e833df82d4a7cde1676513d28dc844ae3c74-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T21:07:03+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p01", "3"]
run = "x9a_p0p01_s3"
level = "0p01"
seed = 3
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.052
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.052, 0.032, 0.016, 0.032, 0.02, 0.028, 0.032, 0.02, 0.024]
retrieval.train_acc_per_layer = [0.036, 0.024, 0.024, 0.008, 0.016, 0.012, 0.02, 0.024, 0.032]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.326060270116488, 2.142667263820093, 2.1165923453025632, 2.0803620982959914, 2.049960696861426, 2.0477018929895383, 2.0158464155616733, 1.9317151841932276, 1.8410202026522253]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.312748919866635, 7.9176944880823354, 7.951715216534014, 7.427596088654946, 6.768375164045051, 6.3213856571621125, 5.678995196763029, 4.989883041543407, 4.377498663500015]
seconds = 72.16976428031921
train.steps = 6173
train.val_bpb_full = 0.5624487754686265
train.train_seconds_this_session = 1130.3066844940186
train.wall_seconds_this_session = 1189.3752312660217
`````

#### `results/phase2/x9a/x9a_p0p01_s4.json` (2,422 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p01_s4/final.safetensors"
provenance.git_commit = "2466b303da0a9b230a39bbc1c3f5ce01093cd498-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T22:03:58+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p01", "4"]
run = "x9a_p0p01_s4"
level = "0p01"
seed = 4
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.052
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.052, 0.024, 0.028, 0.024, 0.02, 0.016, 0.016, 0.02, 0.028]
retrieval.train_acc_per_layer = [0.036, 0.02, 0.036, 0.012, 0.012, 0.012, 0.02, 0.028, 0.008]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 0
assembly_cipher.ci_low = 0.0
assembly_cipher.ci_high = 0.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.327794801544215, 1.8352183184073338, 1.8504200069644687, 1.8540917237675558, 1.8836711516102937, 1.845340813781545, 1.8494546410108255, 1.7935396895277456, 1.74971275402398]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3134360616006866, 7.828052227636139, 7.889098982658978, 7.642843378942354, 7.227895459109833, 6.709116171483268, 5.936875896778202, 5.165126314297687, 4.411147398354978]
seconds = 69.27791404724121
train.steps = 6173
train.val_bpb_full = 0.562667404128049
train.train_seconds_this_session = 952.0705833435059
train.wall_seconds_this_session = 1002.708165884018
`````

#### `results/phase2/x9a/x9a_p0p03_s0.json` (2,427 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p03_s0/final.safetensors"
provenance.git_commit = "eb2aa7a965c3dd2268c2af56b68dcae1b1053c2a-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T11:23:29+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p03", "0"]
run = "x9a_p0p03_s0"
level = "0p03"
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.072
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.072, 0.008, 0.016, 0.032, 0.024, 0.036, 0.024, 0.028, 0.028]
retrieval.train_acc_per_layer = [0.064, 0.032, 0.016, 0.016, 0.016, 0.016, 0.02, 0.028, 0.008]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 2.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3258359031752955, 2.480490735821604, 2.8316401371023017, 2.884242831143795, 2.7898273393648805, 2.684215902647401, 2.5105812394546825, 2.4666399212955956, 2.3667578011045114]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3137367709476466, 7.676671506625024, 7.931495871564914, 7.450034321265832, 6.909732609865106, 6.421533322784917, 5.60863826655126, 5.116326530141744, 4.396725481532334]
seconds = 66.28185677528381
train.steps = 6173
train.val_bpb_full = 0.5622025383735381
train.train_seconds_this_session = 1014.509247303009
train.wall_seconds_this_session = 1067.7700216770172
`````

#### `results/phase2/x9a/x9a_p0p03_s1.json` (2,430 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p03_s1/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T12:43:50+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p03", "1"]
run = "x9a_p0p03_s1"
level = "0p03"
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.068
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.068, 0.02, 0.048, 0.028, 0.036, 0.028, 0.024, 0.008, 0.032]
retrieval.train_acc_per_layer = [0.056, 0.024, 0.012, 0.016, 0.02, 0.024, 0.008, 0.016, 0.004]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3292059111676715, 3.237348106586698, 3.0985718457860454, 2.9758973717576307, 3.0037709335550726, 3.0435790803868175, 3.0997175582287464, 3.050381223132114, 2.830742766280891]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3131401994339176, 7.891607551208133, 7.7615487917404025, 7.251896047388419, 6.844731771100372, 6.5357197202248765, 5.977164271899117, 5.348833627139992, 4.422962081693102]
seconds = 67.58081603050232
train.steps = 6173
train.val_bpb_full = 0.5643808364833576
train.train_seconds_this_session = 1023.9117782115936
train.wall_seconds_this_session = 1077.2853684425354
`````

#### `results/phase2/x9a/x9a_p0p03_s2.json` (2,420 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p03_s2/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T14:05:05+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p03", "2"]
run = "x9a_p0p03_s2"
level = "0p03"
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.064
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.064, 0.056, 0.052, 0.028, 0.036, 0.032, 0.036, 0.032, 0.02]
retrieval.train_acc_per_layer = [0.036, 0.016, 0.028, 0.024, 0.02, 0.012, 0.02, 0.028, 0.024]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.327855462334968, 2.6717152298885556, 2.650966025238883, 2.58757533344404, 2.6894783953527286, 2.618604717769232, 2.651870953369794, 2.5927628391108346, 2.537636690205908]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.313117993956294, 7.822054591459343, 7.866045828087079, 7.562429973656876, 6.916342717273731, 6.557253720243994, 5.795440569581836, 5.221575897258298, 4.4913014239398]
seconds = 70.35212469100952
train.steps = 6173
train.val_bpb_full = 0.5636093110730239
train.train_seconds_this_session = 1081.7497086524963
train.wall_seconds_this_session = 1139.0705552101135
`````

#### `results/phase2/x9a/x9a_p0p03_s3.json` (2,425 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p03_s3/final.safetensors"
provenance.git_commit = "bbe3451b000de2f8d726bbd40858e5a13b652cc4-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T21:27:03+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p03", "3"]
run = "x9a_p0p03_s3"
level = "0p03"
seed = 3
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 4
retrieval.acc_unmapped = 0.044
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.052, 0.024, 0.028, 0.032, 0.044, 0.036, 0.036, 0.032, 0.02]
retrieval.train_acc_per_layer = [0.036, 0.012, 0.02, 0.044, 0.048, 0.012, 0.008, 0.012, 0.008]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 3
assembly_cipher.ci_low = 3.0
assembly_cipher.ci_high = 3.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.331643598129645, 2.477736862830707, 2.5114045122667656, 2.8811759755195774, 2.822713079158155, 2.936282029622773, 2.793073324543133, 2.663375994651256, 2.537977689631935]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.312917363440648, 7.936844772612203, 7.92428589158697, 7.4953581868283115, 6.8518791469136415, 6.336861075407748, 5.7023965116418385, 5.050561768803818, 4.4423241285457005]
seconds = 68.56951785087585
train.steps = 6173
train.val_bpb_full = 0.5631022893680478
train.train_seconds_this_session = 1018.411209821701
train.wall_seconds_this_session = 1071.6733939647675
`````

#### `results/phase2/x9a/x9a_p0p03_s4.json` (2,431 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p03_s4/final.safetensors"
provenance.git_commit = "2466b303da0a9b230a39bbc1c3f5ce01093cd498-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T22:21:59+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p03", "4"]
run = "x9a_p0p03_s4"
level = "0p03"
seed = 4
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.088
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.088, 0.032, 0.064, 0.076, 0.072, 0.056, 0.024, 0.036, 0.016]
retrieval.train_acc_per_layer = [0.072, 0.016, 0.048, 0.064, 0.056, 0.036, 0.02, 0.028, 0.024]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.328127391146376, 3.5631661817458666, 3.4711522771279757, 3.5007785704408136, 3.4286236073750365, 3.328589534665576, 3.3116087716108797, 3.3338510295929913, 2.9766451649701113]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3115293306640066, 7.7319024960715295, 7.881931136171487, 7.673872045001458, 7.259391082273634, 6.7169560566941895, 5.962615715243519, 5.2246471348351005, 4.483040944263095]
seconds = 68.61450862884521
train.steps = 6173
train.val_bpb_full = 0.5621463260762617
train.train_seconds_this_session = 952.620902299881
train.wall_seconds_this_session = 1003.1245820522308
`````

#### `results/phase2/x9a/x9a_p0p1_s0.json` (2,417 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p1_s0/final.safetensors"
provenance.git_commit = "eb2aa7a965c3dd2268c2af56b68dcae1b1053c2a-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T11:43:37+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p1", "0"]
run = "x9a_p0p1_s0"
level = "0p1"
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.1
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.1, 0.032, 0.048, 0.04, 0.048, 0.052, 0.032, 0.04, 0.028]
retrieval.train_acc_per_layer = [0.128, 0.048, 0.028, 0.02, 0.02, 0.036, 0.064, 0.032, 0.016]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 2.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3413198032398257, 5.465305305746593, 6.7161452269368915, 6.580050370522281, 6.474553157149655, 6.304745088039785, 6.2765554393799015, 6.186284559492392, 5.958933706722133]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3133122555347487, 7.645980745188811, 7.7910447669963405, 7.5571909323004025, 7.134392159225926, 6.474183455916138, 5.775161461638135, 5.182970328159683, 4.394073590663445]
seconds = 67.80612635612488
train.steps = 6173
train.val_bpb_full = 0.5634364698008689
train.train_seconds_this_session = 1018.1755571365356
train.wall_seconds_this_session = 1071.7658262252808
`````

#### `results/phase2/x9a/x9a_p0p1_s1.json` (2,415 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p1_s1/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T13:03:50+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p1", "1"]
run = "x9a_p0p1_s1"
level = "0p1"
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.116
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.116, 0.036, 0.04, 0.064, 0.056, 0.056, 0.036, 0.028, 0.012]
retrieval.train_acc_per_layer = [0.112, 0.048, 0.028, 0.048, 0.04, 0.032, 0.02, 0.028, 0.024]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.343216864734566, 7.0145795820146075, 6.964215469254234, 7.017678986665526, 7.304995648400225, 7.240972708235177, 7.174083517383907, 7.127029473202693, 6.815072167133172]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.310769063768599, 7.900459465293986, 7.877841635343034, 7.251510539127837, 6.835834934956135, 6.55123196797873, 5.941253081656548, 5.299831974294203, 4.423639034552714]
seconds = 66.71660995483398
train.steps = 6173
train.val_bpb_full = 0.5655173233882197
train.train_seconds_this_session = 1022.0133714675903
train.wall_seconds_this_session = 1075.594017982483
`````

#### `results/phase2/x9a/x9a_p0p1_s2.json` (2,416 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p1_s2/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T14:27:13+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p1", "2"]
run = "x9a_p0p1_s2"
level = "0p1"
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.112
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.112, 0.024, 0.028, 0.024, 0.04, 0.032, 0.024, 0.024, 0.016]
retrieval.train_acc_per_layer = [0.068, 0.016, 0.02, 0.008, 0.032, 0.052, 0.036, 0.036, 0.02]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.342630410782264, 7.5649455718946275, 7.57385173381736, 7.553658006933079, 7.758941816761628, 7.6052411990428554, 7.428966505134325, 7.32745483230624, 7.017468481259682]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3126125703361637, 7.843079861731592, 7.863708652360796, 7.662819217169711, 6.914959375670115, 6.616464543746782, 5.828755165925511, 5.194497033738561, 4.508440047543826]
seconds = 69.35376763343811
train.steps = 6173
train.val_bpb_full = 0.5650203517642011
train.train_seconds_this_session = 1087.4056479930878
train.wall_seconds_this_session = 1144.952663898468
`````

#### `results/phase2/x9a/x9a_p0p1_s3.json` (2,419 bytes; first commit 88cf86e 2026-11-05 14:37:51 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p1_s3/final.safetensors"
provenance.git_commit = "3b1e037f1c26a818e9752175dbf4605a66eb846f-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T08:10:57+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p1", "3"]
run = "x9a_p0p1_s3"
level = "0p1"
seed = 3
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.084
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.084, 0.02, 0.024, 0.052, 0.04, 0.032, 0.032, 0.02, 0.02]
retrieval.train_acc_per_layer = [0.072, 0.032, 0.04, 0.056, 0.068, 0.044, 0.032, 0.036, 0.032]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3400743302860065, 6.038082034463085, 6.321027852793548, 6.5298562820033546, 6.407083803226227, 6.418378633859503, 6.269853280551347, 6.095586526616755, 5.9046136281653645]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.313186895550669, 7.8857105852792175, 7.9189565258879435, 7.3119908978015875, 6.742124637492399, 6.366833340351914, 5.673600149904435, 4.9915042990373175, 4.405751495587107]
seconds = 68.04696249961853
train.steps = 6173
train.val_bpb_full = 0.56148112577624
train.train_seconds_this_session = 1038.5063753128052
train.wall_seconds_this_session = 1093.2757678031921
`````

#### `results/phase2/x9a/x9a_p0p1_s4.json` (2,414 bytes; first commit c7f6e92 2026-11-05 15:39:07 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p1_s4/final.safetensors"
provenance.git_commit = "0f01dd635a7f204e76d17d6d4d480a1a8e18fc7b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T09:19:37+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p1", "4"]
run = "x9a_p0p1_s4"
level = "0p1"
seed = 4
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.1
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.1, 0.02, 0.044, 0.056, 0.056, 0.04, 0.028, 0.032, 0.016]
retrieval.train_acc_per_layer = [0.088, 0.02, 0.036, 0.036, 0.028, 0.036, 0.028, 0.024, 0.036]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.342277603936379, 6.336239204418296, 6.9527045551707625, 6.862150911101792, 6.796694509098675, 6.646362053915084, 6.708635184883321, 6.933298140482223, 6.439561250460701]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3111608010881404, 7.851525205718548, 7.94673982848908, 7.656142254995841, 7.3049102625282885, 6.819704052027759, 6.065548956847262, 5.277807509094748, 4.495870759210773]
seconds = 68.57217645645142
train.steps = 6173
train.val_bpb_full = 0.5625737251042545
train.train_seconds_this_session = 1057.5166232585907
train.wall_seconds_this_session = 1113.2367177009583
`````

#### `results/phase2/x9a/x9a_p0p3_s0.json` (2,411 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p3_s0/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T12:04:04+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p3", "0"]
run = "x9a_p0p3_s0"
level = "0p3"
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.432
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.432, 0.276, 0.4, 0.396, 0.392, 0.424, 0.408, 0.376, 0.272]
retrieval.train_acc_per_layer = [0.432, 0.24, 0.34, 0.368, 0.38, 0.428, 0.424, 0.332, 0.24]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 2.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3478072708107742, 7.565660550898292, 10.00943725105391, 10.02730082017537, 9.876837874155433, 9.568840296762977, 9.032358691474911, 8.493403457288338, 7.60967908699132]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.313815142787537, 7.359440293502007, 7.848431232855266, 7.648440020767148, 7.22514433449258, 6.504611165316443, 5.822545087225438, 5.257291115817129, 4.432971778058259]
seconds = 67.33126306533813
train.steps = 6173
train.val_bpb_full = 0.5624925436178932
train.train_seconds_this_session = 1042.3520982265472
train.wall_seconds_this_session = 1096.347774028778
`````

#### `results/phase2/x9a/x9a_p0p3_s1.json` (2,414 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p3_s1/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T13:23:51+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p3", "1"]
run = "x9a_p0p3_s1"
level = "0p3"
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 0.46
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.46, 0.216, 0.224, 0.288, 0.296, 0.288, 0.2, 0.204, 0.228]
retrieval.train_acc_per_layer = [0.428, 0.168, 0.204, 0.28, 0.336, 0.3, 0.184, 0.204, 0.232]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.347214246436984, 8.583518196036737, 8.580121165840552, 8.565101170721901, 9.075232559955966, 9.090732287480305, 8.935869897124098, 8.674516567647661, 7.832356964926436]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.311802710016759, 7.9064368985136815, 7.8030333180802804, 7.167020219140405, 6.821740455188174, 6.524684165317331, 6.025618413470228, 5.393388270829705, 4.445049694035876]
seconds = 66.64374589920044
train.steps = 6173
train.val_bpb_full = 0.5639242057164855
train.train_seconds_this_session = 1021.3481051921844
train.wall_seconds_this_session = 1074.5327162742615
`````

#### `results/phase2/x9a/x9a_p0p3_s2.json` (2,414 bytes; first commit 7bcba7d 2026-11-04 20:22:41 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p3_s2/final.safetensors"
provenance.git_commit = "4770255763a4e0d26a106e99a7f5a10ba29d963c-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-04T14:48:43+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p3", "2"]
run = "x9a_p0p3_s2"
level = "0p3"
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 4
retrieval.acc_unmapped = 0.172
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.144, 0.088, 0.112, 0.12, 0.172, 0.164, 0.124, 0.108, 0.056]
retrieval.train_acc_per_layer = [0.152, 0.12, 0.112, 0.156, 0.196, 0.196, 0.176, 0.124, 0.06]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.345898092828956, 8.930583448134055, 9.186873856686722, 9.225090290921177, 9.264731912808463, 9.137082736345612, 8.695572553341513, 8.269991766322718, 7.550151643251321]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3116147938531895, 7.853741194161986, 7.868452817994048, 7.642413313862719, 7.005811492781703, 6.647052837326782, 5.913104862811761, 5.287414730185949, 4.5310534910365]
seconds = 69.4542191028595
train.steps = 6173
train.val_bpb_full = 0.5645034005824748
train.train_seconds_this_session = 1057.8673474788666
train.wall_seconds_this_session = 1113.9173538684845
`````

#### `results/phase2/x9a/x9a_p0p3_s3.json` (2,415 bytes; first commit 88cf86e 2026-11-05 14:37:51 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p3_s3/final.safetensors"
provenance.git_commit = "3b1e037f1c26a818e9752175dbf4605a66eb846f-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T08:31:17+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p3", "3"]
run = "x9a_p0p3_s3"
level = "0p3"
seed = 3
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 4
retrieval.acc_unmapped = 0.204
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.168, 0.1, 0.112, 0.172, 0.204, 0.164, 0.14, 0.164, 0.076]
retrieval.train_acc_per_layer = [0.2, 0.116, 0.128, 0.212, 0.256, 0.18, 0.176, 0.188, 0.088]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 2.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3473953805761036, 7.770970359847712, 9.449597260830835, 9.512469105781209, 9.445562850317646, 9.168097288486628, 8.828906403719028, 8.11863092136098, 7.544554175470947]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3146657892979077, 7.731549038063856, 7.929192444379759, 7.4260812593039764, 6.765621005299132, 6.282768690162446, 5.726003011093567, 5.058035399673629, 4.481355930980466]
seconds = 68.30632781982422
train.steps = 6173
train.val_bpb_full = 0.5628087868223011
train.train_seconds_this_session = 1055.0909624099731
train.wall_seconds_this_session = 1110.4906373023987
`````

#### `results/phase2/x9a/x9a_p0p3_s4.json` (2,412 bytes; first commit c7f6e92 2026-11-05 15:39:07 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p0p3_s4/final.safetensors"
provenance.git_commit = "0f01dd635a7f204e76d17d6d4d480a1a8e18fc7b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T09:39:41+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "0p3", "4"]
run = "x9a_p0p3_s4"
level = "0p3"
seed = 4
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 4
retrieval.acc_unmapped = 0.268
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.18, 0.132, 0.216, 0.26, 0.268, 0.176, 0.18, 0.168, 0.104]
retrieval.train_acc_per_layer = [0.192, 0.176, 0.236, 0.264, 0.284, 0.204, 0.18, 0.18, 0.092]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.350016440313013, 7.875995251501215, 8.701710317548168, 8.763609060658807, 8.79877227670825, 8.582464475461494, 8.431405621691141, 8.331094698920616, 7.500939136463235]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3115032291596815, 7.655761053751044, 7.884015804285094, 7.619066194212515, 7.218416714091663, 6.747087450468822, 6.036507998718838, 5.299819990089835, 4.468377179834246]
seconds = 68.7736439704895
train.steps = 6173
train.val_bpb_full = 0.5630347293914993
train.train_seconds_this_session = 1059.5827896595001
train.wall_seconds_this_session = 1114.981103181839
`````

#### `results/phase2/x9a/x9a_p1_s0.json` (2,393 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p1_s0/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T08:49:01+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "1", "0"]
run = "x9a_p1_s0"
level = 1
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 6
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.98, 0.972, 0.996, 1.0, 0.996, 1.0, 1.0, 1.0, 0.988]
retrieval.train_acc_per_layer = [0.98, 0.912, 0.972, 0.992, 0.996, 0.996, 1.0, 1.0, 0.996]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 2.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.350399679562248, 9.463427140741558, 10.838517589937693, 10.90066205549, 10.382213530358301, 9.747528226400128, 8.614217318001518, 7.629060366636978, 6.411015960193911]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3136350062984303, 7.614455301618164, 7.666824975541099, 7.478880812293434, 6.995960184451312, 6.489500212742987, 5.735887708275212, 5.191278339086311, 4.4395722685804335]
seconds = 174.20606875419617
train.steps = 6173
train.val_bpb_full = 0.562833778367288
train.train_seconds_this_session = 1695.1049947738647
train.wall_seconds_this_session = 1781.974327325821
`````

#### `results/phase2/x9a/x9a_p1_s1.json` (2,413 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p1_s1/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T10:51:43+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "1", "1"]
run = "x9a_p1_s1"
level = 1
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 4
retrieval.acc_unmapped = 0.992
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.952, 0.856, 0.956, 0.972, 0.992, 0.996, 0.996, 0.992, 0.984]
retrieval.train_acc_per_layer = [0.944, 0.856, 0.94, 0.964, 0.996, 0.996, 0.988, 0.988, 0.976]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3513161125793705, 10.02647639178935, 10.378744530072849, 10.537147180502354, 10.38982784908819, 10.443525055291918, 9.582520291717913, 8.487372813354789, 6.8349083210887125]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.311209982435086, 7.830881689464868, 7.72661562237305, 7.326424553221482, 6.924910160277967, 6.697592228979513, 6.2301382621289845, 5.559757450519044, 4.535866596681934]
seconds = 66.31443095207214
train.steps = 6173
train.val_bpb_full = 0.5657546913675725
train.train_seconds_this_session = 1024.1465842723846
train.wall_seconds_this_session = 1077.3586201667786
`````

#### `results/phase2/x9a/x9a_p1_s2.json` (2,407 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p1_s2/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T12:31:51+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "1", "2"]
run = "x9a_p1_s2"
level = 1
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 4
retrieval.acc_unmapped = 0.988
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.92, 0.812, 0.936, 0.972, 0.988, 0.984, 0.976, 0.984, 0.956]
retrieval.train_acc_per_layer = [0.92, 0.812, 0.912, 0.956, 0.992, 0.972, 0.968, 0.98, 0.948]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.349061947804371, 10.158035084317742, 10.477221222797809, 10.517730796743669, 10.186789746016679, 9.91397103741344, 8.833083009293079, 7.866303525128446, 6.658379465059376]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3141946505040534, 7.962424901477399, 7.8565553306588765, 7.512149689627979, 6.9002685084558015, 6.609357793393001, 5.855034558091628, 5.162792356559076, 4.411223258546101]
seconds = 66.68495464324951
train.steps = 6173
train.val_bpb_full = 0.5657644288336
train.train_seconds_this_session = 1023.020890712738
train.wall_seconds_this_session = 1076.494829416275
`````

#### `results/phase2/x9a/x9a_p1_s3.json` (2,406 bytes; first commit 88cf86e 2026-11-05 14:37:51 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p1_s3/final.safetensors"
provenance.git_commit = "753999e23228d513d47ab5fd1e5691743bbc5c69-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T08:59:12+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "1", "3"]
run = "x9a_p1_s3"
level = "1"
seed = 3
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 7
retrieval.acc_unmapped = 0.992
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.864, 0.868, 0.948, 0.976, 0.992, 0.988, 0.992, 0.992, 0.936]
retrieval.train_acc_per_layer = [0.832, 0.792, 0.9, 0.944, 0.98, 0.968, 0.968, 0.988, 0.904]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.350167189059108, 9.83405399731185, 10.99762561961253, 10.88013973912721, 10.173873419754443, 9.470246855792858, 8.570652209170081, 7.39601949294314, 6.45907603580541]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3138918942507454, 7.664663406647321, 7.91680509354338, 7.563108726469253, 6.848229916017335, 6.385649038818486, 5.789217299362635, 5.100632273704045, 4.433799576912743]
seconds = 68.35271978378296
train.steps = 6173
train.val_bpb_full = 0.5636811242598944
train.train_seconds_this_session = 1034.9844315052032
train.wall_seconds_this_session = 1089.6660232543945
`````

#### `results/phase2/x9a/x9a_p1_s4.json` (2,409 bytes; first commit c7f6e92 2026-11-05 15:39:07 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p1_s4/final.safetensors"
provenance.git_commit = "0f01dd635a7f204e76d17d6d4d480a1a8e18fc7b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T09:59:47+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "1", "4"]
run = "x9a_p1_s4"
level = "1"
seed = 4
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 5
retrieval.acc_unmapped = 0.968
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.724, 0.8, 0.96, 0.98, 0.964, 0.968, 0.976, 0.98, 0.572]
retrieval.train_acc_per_layer = [0.812, 0.808, 0.956, 0.976, 0.988, 0.996, 0.996, 0.984, 0.62]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 2
assembly_cipher.ci_low = 2.0
assembly_cipher.ci_high = 2.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3505888401802957, 9.387606742893777, 10.8978024762425, 10.832797046299795, 10.630293143167536, 10.137227557696058, 8.926051514260298, 7.724450562431169, 6.362540523902141]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3141305982125306, 7.619534877274344, 7.892965611427622, 7.59330328223463, 7.228841475764039, 6.883068325004925, 6.0797173340480315, 5.312512345939684, 4.471568026494757]
seconds = 70.12536382675171
train.steps = 6173
train.val_bpb_full = 0.5641711303290943
train.train_seconds_this_session = 1061.7836275100708
train.wall_seconds_this_session = 1117.7433314323425
`````

#### `results/phase2/x9a/x9a_p20_s0.json` (2,391 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p20_s0/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T08:15:55+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "20", "0"]
run = "x9a_p20_s0"
level = 20
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 2
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.98, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.96]
retrieval.train_acc_per_layer = [0.988, 0.996, 1.0, 1.0, 1.0, 1.0, 1.0, 0.996, 0.968]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3546337730010656, 11.086376352532048, 11.315426065227268, 10.671898964638068, 9.806806524523042, 8.826025226850806, 7.752448456856733, 6.876379688460315, 5.669283307183486]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3126110843573624, 7.686674730491836, 7.724514591343222, 7.216932683782088, 6.728282566973071, 6.164133612271939, 5.537803475915254, 5.074776254937606, 4.386703603509969]
seconds = 175.63230085372925
train.steps = 6173
train.val_bpb_full = 0.5742045614344106
train.train_seconds_this_session = 1181.6394398212433
train.wall_seconds_this_session = 1248.2431771755219
`````

#### `results/phase2/x9a/x9a_p20_s1.json` (2,386 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p20_s1/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T10:31:39+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "20", "1"]
run = "x9a_p20_s1"
level = 20
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 1
retrieval.acc_unmapped = 0.996
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.98, 0.996, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.924]
retrieval.train_acc_per_layer = [0.996, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.916]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3567814146918815, 11.589345922995351, 11.466806486471947, 10.831492712986392, 10.34964299611849, 9.830954966036535, 8.73283412841377, 7.589943570983091, 5.976957015739834]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3089958929490426, 7.880541037688124, 7.839804632663613, 7.401342172733278, 7.122596174942033, 6.782460258447962, 6.145005931543031, 5.481793175867772, 4.5309663854475]
seconds = 66.54018425941467
train.steps = 6173
train.val_bpb_full = 0.5804932925020884
train.train_seconds_this_session = 1020.55526471138
train.wall_seconds_this_session = 1073.9950375556946
`````

#### `results/phase2/x9a/x9a_p20_s2.json` (2,381 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p20_s2/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T12:11:48+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "20", "2"]
run = "x9a_p20_s2"
level = 20
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
retrieval.train_acc_per_layer = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3553219060640327, 11.271190441351298, 11.523075854416648, 11.22483643434191, 10.231237387337409, 9.589846670660167, 8.58472413120238, 7.374448763126481, 6.042115545276847]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3137618595334173, 7.848981750958064, 7.928623324608658, 7.6830117712502135, 6.94974610752105, 6.564254972568541, 5.9454081929594675, 5.266749200818234, 4.5082674244508745]
seconds = 65.65734910964966
train.steps = 6173
train.val_bpb_full = 0.5803919473895252
train.train_seconds_this_session = 1022.9064486026764
train.wall_seconds_this_session = 1076.3194813728333
`````

#### `results/phase2/x9a/x9a_p50_s0.json` (2,399 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p50_s0/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T09:24:13+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "50", "0"]
run = "x9a_p50_s0"
level = 50
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 4
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.912, 0.868, 0.972, 0.996, 1.0, 1.0, 1.0, 0.996, 0.968]
retrieval.train_acc_per_layer = [0.928, 0.884, 0.98, 0.996, 1.0, 1.0, 1.0, 1.0, 0.972]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.355558814697265, 11.339393016537525, 11.541505687871398, 10.845884320266158, 9.804949172166792, 8.96731278550155, 8.385204402334367, 7.39921140024482, 6.2307470964773835]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3117341982676436, 7.823690718400275, 7.669235358497741, 7.198871253843286, 6.66131390834106, 6.092849034461397, 5.701187785607417, 5.161364764969582, 4.484911476170531]
seconds = 178.57699465751648
train.steps = 6173
train.val_bpb_full = 0.6187410529692541
train.train_seconds_this_session = 1734.1785922050476
train.wall_seconds_this_session = 1821.2983362674713
`````

#### `results/phase2/x9a/x9a_p50_s1.json` (2,395 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p50_s1/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T11:11:46+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "50", "1"]
run = "x9a_p50_s1"
level = 50
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 3
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.984, 0.948, 0.988, 1.0, 1.0, 1.0, 1.0, 1.0, 0.992]
retrieval.train_acc_per_layer = [0.976, 0.96, 0.992, 1.0, 1.0, 1.0, 1.0, 1.0, 0.972]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3534983337827717, 11.394074236617172, 11.643508348397729, 11.210661298390201, 10.603582989365302, 9.700702763970318, 8.568859306895252, 7.450456868315345, 6.198632307647089]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3116879652342184, 7.7424969423355385, 7.876859090462698, 7.39902048075674, 6.927280774104294, 6.493836584430076, 6.072147590222648, 5.357746371042651, 4.600364160122759]
seconds = 66.06308698654175
train.steps = 6173
train.val_bpb_full = 0.6203365176429841
train.train_seconds_this_session = 1025.3504433631897
train.wall_seconds_this_session = 1078.788134098053
`````

#### `results/phase2/x9a/x9a_p50_s2.json` (2,400 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p50_s2/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T12:51:53+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "50", "2"]
run = "x9a_p50_s2"
level = 50
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 3
retrieval.acc_unmapped = 0.996
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.92, 0.904, 0.984, 0.996, 1.0, 1.0, 0.996, 1.0, 0.956]
retrieval.train_acc_per_layer = [0.912, 0.892, 0.964, 1.0, 1.0, 1.0, 0.996, 0.996, 0.96]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.35682374984025, 11.326685404179871, 11.388079802346173, 10.927653402494787, 9.796454275943718, 9.191068286441324, 8.410712986594898, 7.215585205978082, 6.124637190501839]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.313420638558899, 7.800019943786449, 7.666661272413606, 7.230144902518365, 6.7060605931887665, 6.3631073299795045, 5.78689432850926, 5.15574308704022, 4.559933898235826]
seconds = 66.40689468383789
train.steps = 6173
train.val_bpb_full = 0.622373704418018
train.train_seconds_this_session = 1023.9512829780579
train.wall_seconds_this_session = 1077.5141835212708
`````

#### `results/phase2/x9a/x9a_p5_s0.json` (2,374 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p5_s0/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T09:49:31+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "5", "0"]
run = "x9a_p5_s0"
level = 5
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
retrieval.train_acc_per_layer = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.355449966037214, 10.797453916246027, 11.372292620641968, 10.830222758863817, 9.938189192011396, 9.23469169576861, 7.917795612975681, 6.950710571731859, 5.753683489574699]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3134059096266193, 7.624579769211035, 7.778104293640612, 7.346454225783246, 6.784056941363857, 6.35195242113266, 5.605946486617836, 5.0953429858732795, 4.362752507135004]
seconds = 68.69159650802612
train.steps = 6173
train.val_bpb_full = 0.5656079659069411
train.train_seconds_this_session = 1355.0050151348114
train.wall_seconds_this_session = 1421.7037267684937
`````

#### `results/phase2/x9a/x9a_p5_s1.json` (2,385 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p5_s1/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T11:31:46+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "5", "1"]
run = "x9a_p5_s1"
level = 5
seed = 1
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 2
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.988, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.952]
retrieval.train_acc_per_layer = [0.992, 0.996, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.964]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.353012260390967, 11.407147134576984, 11.402714047101723, 10.796323727890037, 10.186258731323388, 9.594262513805202, 8.757702572699264, 7.450031664468349, 5.86551804386668]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3126994607421016, 7.950539855106118, 7.822073770110659, 7.378561967852844, 6.956870630032856, 6.6275875762776115, 6.158136329619898, 5.396621418087612, 4.460336801972589]
seconds = 65.68437337875366
train.steps = 6173
train.val_bpb_full = 0.5696379550496589
train.train_seconds_this_session = 1024.2819380760193
train.wall_seconds_this_session = 1077.585837841034
`````

#### `results/phase2/x9a/x9a_p5_s2.json` (2,376 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9a_p5_s2/final.safetensors"
provenance.git_commit = "4e6fd51a065381d3b86b072a482fa30f66639e8b-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T13:11:49+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "train", "5", "2"]
run = "x9a_p5_s2"
level = 5
seed = 2
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 0
retrieval.acc_unmapped = 1.0
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
retrieval.train_acc_per_layer = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.3549456817252437, 11.39968655426934, 11.589934135281762, 11.257992637227403, 10.408675748705958, 9.889315280436056, 8.77438479679237, 7.478714644183764, 6.045078449449248]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 1.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3127088064044847, 7.9006833577307525, 7.920316268445568, 7.625052912817812, 6.975981872131774, 6.671843568215548, 6.034569669804193, 5.308527508351261, 4.505425469574067]
seconds = 65.74035143852234
train.steps = 6173
train.val_bpb_full = 0.5691346720751064
train.train_seconds_this_session = 1019.3641133308411
train.wall_seconds_this_session = 1072.9353821277618
`````

#### `results/phase2/x9a/x9apilot_p20_s0.json` (2,393 bytes; first commit 7455dba 2026-11-04 09:53:29 +0530)

`````text
provenance.config.registration = "RESULTS.md X9a"
provenance.config.checkpoint = "checkpoints/e05/x9apilot_p20_s0/final.safetensors"
provenance.git_commit = "cdef73dd89f4daf3d348941b8a144b872a880ce8-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-03T07:51:22+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9a.py", "pilot"]
run = "x9apilot_p20_s0"
level = 20
seed = 0
pairs.pairs_cut_to_fit_context = 17
pairs.mean_chars = 654.476
pairs.min_chars = 241
retrieval.layer = 7
retrieval.acc_unmapped = 0.864
retrieval.n_test = 250
retrieval.chance = 0.004
retrieval.test_acc_per_layer = [0.54, 0.472, 0.496, 0.548, 0.68, 0.776, 0.876, 0.864, 0.756]
retrieval.train_acc_per_layer = [0.564, 0.428, 0.472, 0.516, 0.668, 0.76, 0.828, 0.848, 0.772]
retrieval.mapped = "secondary, not computed in this version"
assembly_cipher.detok_layer = 1
assembly_cipher.ci_low = 1.0
assembly_cipher.ci_high = 1.0
assembly_cipher.n_words = 300
assembly_cipher.n_occ = 5895
assembly_cipher.min_tokens = 3
assembly_cipher.tokens_per_word_probed = 3.4921119592875316
assembly_cipher.compression = [2.350497200814716, 9.585058478171247, 10.056882572204424, 10.142844935549551, 9.9771576677449, 9.441861746740607, 8.92270264406134, 8.123970928166006, 7.175443099173122]
assembly_english.detok_layer = 1
assembly_english.ci_low = 1.0
assembly_english.ci_high = 2.0
assembly_english.n_words = 300
assembly_english.n_occ = 4439
assembly_english.min_tokens = 3
assembly_english.tokens_per_word_probed = 3.381842757377788
assembly_english.compression = [2.3056526773884554, 6.400804207507196, 6.918022515504082, 7.0813054782620934, 7.039499169948848, 6.633741295893359, 6.397108177025131, 5.748410350954089, 5.090083920193911]
seconds = 89.20303153991699
train.steps = 617
train.val_bpb_full = 0.9101846086123556
train.train_seconds_this_session = 96.78965711593628
train.wall_seconds_this_session = 105.7286376953125
`````

## Not dumped (item-level, binary or too large; path and size only)

- none

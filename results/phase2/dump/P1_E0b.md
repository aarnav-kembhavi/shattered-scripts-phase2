# E0b: Familiarity test (sentiment, XNLI) (Phase 1)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| registered | `0a1d054` | 2026-10-14 18:42:59 +0530 | 241-272 | PRE-REGISTRATION — E0b familiarity test (written 2026-10-14, before any E0b scoring) |
| result | `20d1918` | 2026-10-14 22:39:12 +0530 | 338-374 | 2026-10-14 — E0b provisional GATE 1a (4 forms: English, native, ITRANS, lossy; natural pending) |
| result | `3565362` | 2026-10-15 16:40:24 +0530 | 504-560 | 2026-10-15 — E0b GATE 1 (five forms, five models) |

## Values observed in the result files (read from the files' own columns and keys)

- models: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
- forms: lossy, lower, itrans, native, english, natural
- tasks: sib, xnli, sentiment
- seeds: 0

Result directories: `results/e0b_familiarity`, `results/matched`

## RESULTS.md entries, verbatim

##### PRE-REGISTRATION — E0b familiarity test (written 2026-10-14, before any E0b scoring)

RESULTS.md lines 241 to 272; first line committed in `0a1d054` on 2026-10-14 18:42:59 +0530; last line in `81d420c` on 2026-10-14 22:16:36 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — E0b familiarity test (written 2026-10-14, before any E0b scoring)

Setup: models Qwen2.5-1.5B-Instruct, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B (Qwen3-1.7B also run as an extra);
tasks IndicSentiment (kn, binary) and IndicXNLI (kn, 3-way), the same 200 items each as E0; forms English, native,
ITRANS, lossy ITRANS, natural romanization (Gemini, prompt natural_romanization_v1). Scoring: log-likelihood of English
label words; **contextual calibration** (subtract each label's log-prob on the content-free input "N/A" placed in every
field of the same template) is primary from now on; uncalibrated reported alongside. 95% bootstrap CIs (10,000).
Paired McNemar tests within model and task: natural vs native, natural vs ITRANS (and lossy vs ITRANS for P3), Holm
correction across all McNemar tests of this experiment.

Cells where the model's English accuracy is below chance + 5 points are flagged uninformative and do not count for or
against any prediction.

- **P1 (familiarity dominates)**: natural >= ITRANS in every model (point estimate; no significant natural < ITRANS),
  and natural <= native even in the Qwen models where natural is less fragmented (no significant natural > native in
  any model).
- **P2 (fragmentation also matters)**: in both Qwen models natural > native (significant after Holm on at least one
  task, and no significant reversal on the other); in Sarvam-1 natural < native (significant on at least one task).
- **P3 (lossiness)**: lossy ITRANS < ITRANS (point estimate lower in every informative cell; significant after Holm in
  at least half of them).

P1 and P2 are mutually exclusive on the Qwen comparison; if neither holds, the outcome is recorded as inconclusive.
Constant-label rates (share of the most frequent predicted label) are reported per cell; there are no invalid outputs
with log-likelihood scoring.

- **Correction (2026-10-14):** the E0 scorer of 2026-10-08 prepended BOS only when the tokenizer's `add_bos_token`
  flag was set. Sarvam-1 reports False there (it adds BOS via its post-processor), so **E0's Sarvam-1 numbers were
  computed without BOS** (Gemma 4 was not scored). The scorer now always prepends BOS when a model has one; E0b
  rescores every model and supersedes E0. (With BOS, Gemma 4 scores obvious English sentiment examples decisively,
  e.g. log P(positive) −4.8 vs log P(negative) −22.2; without it, the two were within 0.5 nats.)

---
`````

##### 2026-10-14 — E0b provisional GATE 1a (4 forms: English, native, ITRANS, lossy; natural pending)

RESULTS.md lines 338 to 374; first line committed in `20d1918` on 2026-10-14 22:39:12 +0530; last line in `baf4f09` on 2026-10-15 00:56:53 +0530; labels from the title and parent heading: result

`````text
## 2026-10-14 — E0b provisional GATE 1a (4 forms: English, native, ITRANS, lossy; natural pending)

Config: `scripts/e0b_familiarity.py --forms english native itrans lossy --tag gate1a`, 5 models, 200 items/task, BOS
always prepended, contextual calibration ("N/A"). Outputs: `results/e0b_familiarity/gate1a/`. Scores are cached per
(model, form) and will be reused by the full Gate 1 run; the Holm family there will be larger (30 registered tests vs
10 here), so p-values will only get more conservative.

Calibrated accuracy, % [95% bootstrap CI], n = 200 per cell (raw in parentheses):

| model | sent. en | sent. native | sent. ITRANS | sent. lossy | XNLI en | XNLI native | XNLI ITRANS | XNLI lossy |
|---|---|---|---|---|---|---|---|---|
| Qwen2.5-1.5B | 52.0 [45.0,59.0] (98.5) | 50.5 (70.5) | 50.0 (49.5) | 50.0 (50.0) | 78.5 [73.0,84.0] (79.5) | 34.5 (51.0) | 32.5 (37.5) | 33.0 (37.5) |
| Qwen3-1.7B | 98.0 (98.5) | 79.0 [73.0,84.5] (86.5) | 54.0 [47.0,61.0] (58.0) | 52.0 (57.5) | 54.0 (61.5) | 42.5 (43.0) | 33.5 (37.0) | 33.5 (41.5) |
| Qwen3.5-2B | 97.5 (97.5) | 67.5 [61.0,74.0] (78.5) | 61.5 [54.5,68.5] (67.5) | 64.5 (67.5) | 45.0 (43.0) | 34.0 (34.0) | 34.0 (34.0) | 33.5 (34.0) |
| Sarvam-1 | 97.5 (97.5) | 96.0 [93.0,98.5] (96.0) | 78.0 [72.0,83.5] (84.5) | 86.0 [81.0,90.5] (91.0) | 47.5 (53.0) | 45.5 (52.0) | 37.0 (38.5) | 37.5 (46.0) |
| Gemma 4 E2B | 98.0 (98.5) | 98.5 [96.5,100] (98.5) | 76.5 [70.5,82.0] (75.0) | 78.5 [72.5,84.0] (79.0) | 60.0 [53.0,67.0] (73.5) | 46.5 (54.5) | 43.5 (41.0) | 39.5 (40.0) |

All CIs, constant-label rates (raw and calibrated) and tokens per word are in `accuracy.csv` / `fertility.csv`.

- **Calibration failure, Qwen2.5 sentiment:** the content-free "N/A" input is scored strongly negative (log P
  −1.86 vs −9.61), so subtracting it pushes every review to "positive": calibrated English drops from 98.5 to 52.0
  with 98% of predictions on one label. By the registered rule (English >= chance + 5) this cell is uninformative under
  calibration. Calibration helps elsewhere (e.g. Gemma XNLI constant-label rate 87% -> 60% on ITRANS). Raw numbers
  are reported alongside; changing the calibration recipe is Aarnav's call.
- **ITRANS < native (exploratory, separate Holm family of 10):** point estimate ITRANS <= native in all 10
  model x task cells (one tie: Qwen3.5 XNLI, both at chance). Significant in 5: Gemma 4 sentiment (−22.0 pts, 45 vs 1
  discordant), Sarvam-1 sentiment (−18.0) and XNLI (−8.5), Qwen3 sentiment (−25.0) and XNLI (−9.0). **The pattern
  survives the BOS fix, including for Sarvam-1 and Gemma 4**, where ITRANS is *more* fragmented than native (Sarvam
  2.27 -> 5.24 tokens/word, Gemma 3.08 -> 3.94) and for the Qwen models, where it is *less* fragmented (11.99 -> 4.23).
- **P3 (lossy < ITRANS): refuted.** Of 9 informative cells, lossy is lower in only 3 (by 0.5–4 pts), and no
  difference is significant after Holm (0 of 9). The largest difference goes the other way: Sarvam-1 sentiment lossy
  86.0 vs ITRANS 78.0 (25 vs 9 discordant, p = 0.009 uncorrected, 0.09 Holm). Lossy romanization is also *less*
  fragmented than ITRANS on every model (e.g. Sarvam 4.36 vs 5.24, Qwen 3.57 vs 4.23 tokens/word) and closer to
  how people actually type, so losing information did not hurt measurably here.
- P1 and P2 are pending until the natural form is scored.

---
`````

##### 2026-10-15 — E0b GATE 1 (five forms, five models)

RESULTS.md lines 504 to 560; first line committed in `3565362` on 2026-10-15 16:40:24 +0530; last line in `5abe5d6` on 2026-10-15 16:49:15 +0530; labels from the title and parent heading: result

`````text
## 2026-10-15 — E0b GATE 1 (five forms, five models)

Config: `scripts/e0b_familiarity.py --tag gate1`, 200 items per task, BOS always, primary calibration = mean of
content-free "N/A", "", "[MASK]" with the raw fallback rule (deviation registered 2026-10-15). Outputs:
`results/e0b_familiarity/gate1/` (accuracy with CIs and constant-label rates for primary, raw, N/A-only, avg3;
mcnemar.csv; mcnemar_exploratory.csv; fertility.csv; verdicts.json). Natural romanization: 587/587 texts; 27
outputs were retried (same model and prompt, up to 3 attempts), 18 came back clean, **9 remain defective and are
excluded** from the natural form (5 leftover Kannada, 3 diacritics, 1 stray Japanese characters), which removes 2
sentiment and 7 XNLI items (natural n = 198 and 193). Raw fallback applied to Gemma 4 XNLI and Qwen2.5 sentiment.
All 10 model x task cells are informative (English >= chance + 5).

Primary accuracy, % (natural n = 198 / 193; others n = 200); tokens per word in parentheses:

| model | task | English | native | ITRANS | lossy | natural |
|---|---|---|---|---|---|---|
| Qwen2.5-1.5B (raw) | sent. | 98.5 | 70.5 (11.99) | 49.5 (4.23) | 50.0 (3.57) | 51.5 (3.51) |
| Qwen2.5-1.5B | XNLI | 82.5 | 40.0 (11.80) | 32.0 (4.25) | 32.5 | 32.1 (3.54) |
| Qwen3-1.7B (extra) | sent. | 98.5 | 83.5 | 53.5 | 57.0 | 56.1 |
| Qwen3-1.7B (extra) | XNLI | 57.5 | 44.5 | 33.5 | 33.5 | 34.2 |
| Qwen3.5-2B | sent. | 98.0 | 73.5 (5.24) | 65.5 (4.09) | 68.0 (3.34) | 72.2 (3.32) |
| Qwen3.5-2B | XNLI | 49.0 | 34.0 | 34.0 | 33.5 | 34.2 |
| Sarvam-1 | sent. | 98.0 | 95.5 (2.27) | 82.0 (5.24) | 89.5 (4.36) | 89.4 (4.29) |
| Sarvam-1 | XNLI | 55.0 | 51.5 (2.15) | 38.5 (5.23) | 47.0 | 46.6 (4.32) |
| Gemma 4 E2B | sent. | 98.5 | 98.5 (3.08) | 75.5 (3.94) | 79.0 (3.21) | 80.3 (3.15) |
| Gemma 4 E2B (raw) | XNLI | 73.5 | 54.5 | 41.0 | 40.0 | 40.4 |

95% CIs are in accuracy.csv (half-widths about 3–7 points). Several XNLI cells sit at chance with one label
predicted 98–100% of the time (Qwen3.5 every Kannada form; Qwen3 ITRANS/lossy/natural), so XNLI carries little
signal for those models.

Verdicts (registered rules, Holm over the 30 registered McNemar tests):
- **P1 (familiarity dominates): not met by the registered rule.** Its second half holds everywhere: natural is never
  significantly above native, and is significantly *below* native in 5 of 10 cells, including Qwen2.5 sentiment
  (51.5 vs 70.5) where natural has a third of native's tokens per word (3.51 vs 11.99). Its first half (natural >=
  ITRANS in every cell) fails in one cell by a non-significant point estimate: Gemma 4 XNLI natural 40.4 vs ITRANS
  41.5 on the paired set (11 vs 13 discordant, p = 0.84).
- **P2 (fragmentation also matters): refuted.** In the Qwen models natural is not above native (Qwen2.5: below,
  significant on sentiment; Qwen3.5: no difference). Sarvam-1 natural is below native on both tasks (−6.1, −4.7)
  but not significantly after Holm.
- **P3 (lossy < ITRANS): refuted.** Lossy is at or above ITRANS in 8 of 10 cells and no difference is significant;
  Sarvam-1 lossy exceeds ITRANS by 7.5 and 8.5 points (uncorrected p = 0.006 and 0.012; Holm 0.15 and 0.28).
- Per the registration, with neither P1 nor P2 holding the outcome is **inconclusive**. Plainly: the data favour
  familiarity over fragmentation. Every romanized form (ITRANS, lossy, natural) lands well below native in every
  model, whether romanization is less fragmented (Qwen) or more fragmented (Sarvam-1, Gemma 4) than native, and the
  three romanized forms are within a few points of each other. What sank P1 is one −1-point cell.
- Exploratory (separate Holm family): ITRANS < native in 9 of 10 cells (tie: Qwen3.5 XNLI at chance), significant
  in 7.
- Hint, not a registered result: in Sarvam-1, the two less fragmented romanizations (lossy 4.36, natural 4.29
  tokens/word) beat ITRANS (5.24) by 7–9 points on both tasks, uncorrected p 0.006–0.024. Within the romanized forms,
  fragmentation may matter a little; this is confounded with ITRANS's unusual capitals.

- **Definition (2026-10-15):** "familiarity" in this paper means exposure in pretraining corpora (native Kannada
  script dominates Kannada web text), not how often people use a form. Natural romanization is what people actually
  type, yet it scores about the same as ITRANS (Gate 1); that supports reading the native-script advantage as
  pretraining exposure rather than everyday use.

---
`````

## Result files, every number

#### `results/e0b_familiarity/gate1/accuracy.csv` (9,845 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

| model | task | form | n | chance | acc_cal | acc_cal_ci_low | acc_cal_ci_high | constant_label_rate_cal | acc_raw | acc_raw_ci_low | acc_raw_ci_high | constant_label_rate_raw | acc_na | acc_na_ci_low | acc_na_ci_high | constant_label_rate_na | acc_avg3 | acc_avg3_ci_low | acc_avg3_ci_high | constant_label_rate_avg3 | tokens_per_word |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 1.2214038128249567 |
| gemma4-e2b | sentiment | itrans | 200 | 0.5 | 0.755 | 0.695 | 0.81 | 0.685 | 0.75 | 0.69 | 0.81 | 0.67 | 0.765 | 0.705 | 0.82 | 0.615 | 0.755 | 0.695 | 0.81 | 0.685 | 3.943434935521688 |
| gemma4-e2b | sentiment | lossy | 200 | 0.5 | 0.79 | 0.73 | 0.845 | 0.65 | 0.79 | 0.73 | 0.845 | 0.65 | 0.785 | 0.725 | 0.84 | 0.625 | 0.79 | 0.73 | 0.845 | 0.65 | 3.2110199296600235 |
| gemma4-e2b | sentiment | native | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 3.0767878077373974 |
| gemma4-e2b | sentiment | natural | 198 | 0.5 | 0.803030303030303 | 0.7474747474747475 | 0.8585858585858586 | 0.6717171717171717 | 0.803030303030303 | 0.7474747474747475 | 0.8585858585858586 | 0.6717171717171717 | 0.8282828282828283 | 0.7727272727272727 | 0.8787878787878788 | 0.6262626262626263 | 0.803030303030303 | 0.7474747474747475 | 0.8585858585858586 | 0.6717171717171717 | 3.1530703055473155 |
| gemma4-e2b | xnli | english | 200 | 0.3333333333333333 | 0.735 | 0.675 | 0.795 | 0.405 | 0.735 | 0.675 | 0.795 | 0.405 | 0.6 | 0.53 | 0.67 | 0.56 | 0.63 | 0.565 | 0.695 | 0.565 | 1.2397307559544357 |
| gemma4-e2b | xnli | itrans | 200 | 0.3333333333333333 | 0.41 | 0.34 | 0.48 | 0.87 | 0.41 | 0.34 | 0.48 | 0.87 | 0.435 | 0.365 | 0.505 | 0.6 | 0.445 | 0.375 | 0.51 | 0.68 | 3.9604674291397313 |
| gemma4-e2b | xnli | lossy | 200 | 0.3333333333333333 | 0.4 | 0.335 | 0.47 | 0.84 | 0.4 | 0.335 | 0.47 | 0.84 | 0.395 | 0.33 | 0.46 | 0.78 | 0.375 | 0.31 | 0.44 | 0.835 | 3.2031327697662855 |
| gemma4-e2b | xnli | native | 200 | 0.3333333333333333 | 0.545 | 0.475 | 0.615 | 0.595 | 0.545 | 0.475 | 0.615 | 0.595 | 0.465 | 0.395 | 0.535 | 0.615 | 0.5 | 0.43 | 0.57 | 0.59 | 3.1397314768771754 |
| gemma4-e2b | xnli | natural | 193 | 0.3333333333333333 | 0.40414507772020725 | 0.33678756476683935 | 0.47668393782383417 | 0.772020725388601 | 0.40414507772020725 | 0.33678756476683935 | 0.47668393782383417 | 0.772020725388601 | 0.39896373056994816 | 0.3316062176165803 | 0.47150259067357514 | 0.7253886010362695 | 0.38860103626943004 | 0.32124352331606215 | 0.45595854922279794 | 0.772020725388601 | 3.1711991711991714 |
| qwen2.5-1.5b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.52 | 0.45 | 0.59 | 0.98 | 0.88 | 0.835 | 0.925 | 0.62 | 1.231369150779896 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 0.5 | 0.495 | 0.425 | 0.565 | 0.995 | 0.495 | 0.425 | 0.565 | 0.995 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 | 4.22538100820633 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 0.5 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 | 3.5679953106682296 |
| qwen2.5-1.5b | sentiment | native | 200 | 0.5 | 0.705 | 0.64 | 0.765 | 0.625 | 0.705 | 0.64 | 0.765 | 0.625 | 0.505 | 0.435 | 0.575 | 0.995 | 0.615 | 0.545 | 0.68 | 0.815 | 11.985638921453694 |
| qwen2.5-1.5b | sentiment | natural | 198 | 0.5 | 0.5151515151515151 | 0.4444444444444444 | 0.5858585858585859 | 0.9696969696969697 | 0.5151515151515151 | 0.4444444444444444 | 0.5858585858585859 | 0.9696969696969697 | 0.494949494949495 | 0.42424242424242425 | 0.5656565656565656 | 1.0 | 0.494949494949495 | 0.42424242424242425 | 0.5656565656565656 | 1.0 | 3.5069712251557403 |
| qwen2.5-1.5b | xnli | english | 200 | 0.3333333333333333 | 0.825 | 0.77 | 0.875 | 0.38 | 0.795 | 0.735 | 0.85 | 0.45 | 0.785 | 0.73 | 0.84 | 0.49 | 0.825 | 0.77 | 0.875 | 0.38 | 1.2469796341042458 |
| qwen2.5-1.5b | xnli | itrans | 200 | 0.3333333333333333 | 0.32 | 0.255 | 0.385 | 0.67 | 0.375 | 0.31 | 0.445 | 0.845 | 0.325 | 0.26 | 0.39 | 0.965 | 0.32 | 0.255 | 0.385 | 0.67 | 4.25161611138737 |
| qwen2.5-1.5b | xnli | lossy | 200 | 0.3333333333333333 | 0.325 | 0.26 | 0.39 | 0.75 | 0.375 | 0.31 | 0.445 | 0.84 | 0.33 | 0.265 | 0.395 | 0.955 | 0.325 | 0.26 | 0.39 | 0.75 | 3.5532073595226255 |
| qwen2.5-1.5b | xnli | native | 200 | 0.3333333333333333 | 0.4 | 0.33 | 0.465 | 0.86 | 0.51 | 0.445 | 0.58 | 0.48 | 0.345 | 0.28 | 0.41 | 0.965 | 0.4 | 0.33 | 0.465 | 0.86 | 11.79860765788165 |
| qwen2.5-1.5b | xnli | natural | 193 | 0.3333333333333333 | 0.32124352331606215 | 0.2538860103626943 | 0.38860103626943004 | 0.7409326424870466 | 0.37305699481865284 | 0.30569948186528495 | 0.44041450777202074 | 0.7461139896373057 | 0.33678756476683935 | 0.2694300518134715 | 0.40414507772020725 | 0.9585492227979274 | 0.32124352331606215 | 0.2538860103626943 | 0.38860103626943004 | 0.7409326424870466 | 3.5423465423465426 |
| qwen3-1.7b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 1.231369150779896 |
| qwen3-1.7b | sentiment | itrans | 200 | 0.5 | 0.535 | 0.465 | 0.605 | 0.645 | 0.58 | 0.51 | 0.645 | 0.68 | 0.54 | 0.47 | 0.61 | 0.85 | 0.535 | 0.465 | 0.605 | 0.645 | 4.22538100820633 |
| qwen3-1.7b | sentiment | lossy | 200 | 0.5 | 0.57 | 0.5 | 0.64 | 0.68 | 0.575 | 0.505 | 0.64 | 0.715 | 0.52 | 0.45 | 0.59 | 0.91 | 0.57 | 0.5 | 0.64 | 0.68 | 3.5679953106682296 |
| qwen3-1.7b | sentiment | native | 200 | 0.5 | 0.835 | 0.78 | 0.885 | 0.595 | 0.865 | 0.815 | 0.91 | 0.525 | 0.79 | 0.73 | 0.845 | 0.68 | 0.835 | 0.78 | 0.885 | 0.595 | 11.985638921453694 |
| qwen3-1.7b | sentiment | natural | 198 | 0.5 | 0.5606060606060606 | 0.4898989898989899 | 0.6313131313131313 | 0.7424242424242424 | 0.6313131313131313 | 0.5656565656565656 | 0.696969696969697 | 0.5909090909090909 | 0.5202020202020202 | 0.4494949494949495 | 0.5909090909090909 | 0.9040404040404041 | 0.5606060606060606 | 0.4898989898989899 | 0.6313131313131313 | 0.7424242424242424 | 3.5069712251557403 |
| qwen3-1.7b | xnli | english | 200 | 0.3333333333333333 | 0.575 | 0.505 | 0.645 | 0.71 | 0.615 | 0.545 | 0.68 | 0.53 | 0.54 | 0.47 | 0.61 | 0.765 | 0.575 | 0.505 | 0.645 | 0.71 | 1.2469796341042458 |
| qwen3-1.7b | xnli | itrans | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.37 | 0.305 | 0.44 | 0.8 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.995 | 4.25161611138737 |
| qwen3-1.7b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.415 | 0.345 | 0.485 | 0.795 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.995 | 3.5532073595226255 |
| qwen3-1.7b | xnli | native | 200 | 0.3333333333333333 | 0.445 | 0.375 | 0.515 | 0.85 | 0.43 | 0.36 | 0.5 | 0.61 | 0.425 | 0.355 | 0.495 | 0.89 | 0.445 | 0.375 | 0.515 | 0.85 | 11.79860765788165 |
| qwen3-1.7b | xnli | natural | 193 | 0.3333333333333333 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9844559585492227 | 0.39896373056994816 | 0.3316062176165803 | 0.46632124352331605 | 0.7979274611398963 | 0.33678756476683935 | 0.2694300518134715 | 0.40414507772020725 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9844559585492227 | 3.5423465423465426 |
| qwen3.5-2b | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.525 | 0.98 | 0.96 | 0.995 | 0.51 | 1.2268197573656845 |
| qwen3.5-2b | sentiment | itrans | 200 | 0.5 | 0.655 | 0.59 | 0.72 | 0.775 | 0.675 | 0.61 | 0.74 | 0.665 | 0.615 | 0.545 | 0.685 | 0.855 | 0.655 | 0.59 | 0.72 | 0.775 | 4.087631887456038 |
| qwen3.5-2b | sentiment | lossy | 200 | 0.5 | 0.68 | 0.615 | 0.74 | 0.72 | 0.675 | 0.61 | 0.735 | 0.645 | 0.645 | 0.58 | 0.71 | 0.815 | 0.68 | 0.615 | 0.74 | 0.72 | 3.3423212192262604 |
| qwen3.5-2b | sentiment | native | 200 | 0.5 | 0.735 | 0.67 | 0.795 | 0.755 | 0.785 | 0.725 | 0.84 | 0.705 | 0.675 | 0.61 | 0.74 | 0.815 | 0.735 | 0.67 | 0.795 | 0.755 | 5.235052754982415 |
| qwen3.5-2b | sentiment | natural | 198 | 0.5 | 0.7222222222222222 | 0.6616161616161617 | 0.7828282828282829 | 0.6818181818181818 | 0.7373737373737373 | 0.6767676767676768 | 0.797979797979798 | 0.5757575757575758 | 0.6818181818181818 | 0.6161616161616161 | 0.7424242424242424 | 0.7525252525252525 | 0.7222222222222222 | 0.6616161616161617 | 0.7828282828282829 | 0.6818181818181818 | 3.32275289231682 |
| qwen3.5-2b | xnli | english | 200 | 0.3333333333333333 | 0.49 | 0.42 | 0.56 | 0.805 | 0.43 | 0.36 | 0.5 | 0.89 | 0.45 | 0.38 | 0.52 | 0.845 | 0.49 | 0.42 | 0.56 | 0.805 | 1.2424922333448394 |
| qwen3.5-2b | xnli | itrans | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 4.1282943809050225 |
| qwen3.5-2b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.99 | 0.34 | 0.275 | 0.405 | 0.995 | 0.335 | 0.27 | 0.4 | 0.99 | 0.335 | 0.27 | 0.4 | 0.99 | 3.3431128791645945 |
| qwen3.5-2b | xnli | native | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 5.230979612133267 |
| qwen3.5-2b | xnli | natural | 193 | 0.3333333333333333 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 | 3.346283346283346 |
| sarvam-1 | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.515 | 0.98 | 0.96 | 0.995 | 0.51 | 1.4204939341421143 |
| sarvam-1 | sentiment | itrans | 200 | 0.5 | 0.82 | 0.765 | 0.87 | 0.61 | 0.845 | 0.795 | 0.895 | 0.515 | 0.78 | 0.72 | 0.835 | 0.69 | 0.82 | 0.765 | 0.87 | 0.61 | 5.238569753810082 |
| sarvam-1 | sentiment | lossy | 200 | 0.5 | 0.895 | 0.85 | 0.935 | 0.575 | 0.91 | 0.87 | 0.95 | 0.51 | 0.86 | 0.81 | 0.905 | 0.63 | 0.895 | 0.85 | 0.935 | 0.575 | 4.357561547479484 |
| sarvam-1 | sentiment | native | 200 | 0.5 | 0.955 | 0.925 | 0.98 | 0.505 | 0.96 | 0.93 | 0.985 | 0.53 | 0.96 | 0.93 | 0.985 | 0.51 | 0.955 | 0.925 | 0.98 | 0.505 | 2.2708089097303636 |
| sarvam-1 | sentiment | natural | 198 | 0.5 | 0.8939393939393939 | 0.8484848484848485 | 0.9343434343434344 | 0.5808080808080808 | 0.9040404040404041 | 0.8635101010101012 | 0.9444444444444444 | 0.5303030303030303 | 0.8484848484848485 | 0.797979797979798 | 0.898989898989899 | 0.6464646464646465 | 0.8939393939393939 | 0.8484848484848485 | 0.9343434343434344 | 0.5808080808080808 | 4.29219816078315 |
| sarvam-1 | xnli | english | 200 | 0.3333333333333333 | 0.55 | 0.48 | 0.62 | 0.545 | 0.53 | 0.46 | 0.6 | 0.63 | 0.475 | 0.405 | 0.545 | 0.655 | 0.55 | 0.48 | 0.62 | 0.545 | 1.4326889886089058 |
| sarvam-1 | xnli | itrans | 200 | 0.3333333333333333 | 0.385 | 0.32 | 0.455 | 0.795 | 0.385 | 0.32 | 0.455 | 0.8 | 0.37 | 0.3 | 0.44 | 0.865 | 0.385 | 0.32 | 0.455 | 0.795 | 5.226255594231725 |
| sarvam-1 | xnli | lossy | 200 | 0.3333333333333333 | 0.47 | 0.4 | 0.54 | 0.58 | 0.46 | 0.39 | 0.53 | 0.595 | 0.375 | 0.31 | 0.44 | 0.905 | 0.47 | 0.4 | 0.54 | 0.58 | 4.335405271009448 |
| sarvam-1 | xnli | native | 200 | 0.3333333333333333 | 0.515 | 0.445 | 0.585 | 0.6 | 0.52 | 0.45 | 0.59 | 0.61 | 0.455 | 0.385 | 0.525 | 0.865 | 0.515 | 0.445 | 0.585 | 0.6 | 2.1452013923421185 |
| sarvam-1 | xnli | natural | 193 | 0.3333333333333333 | 0.46632124352331605 | 0.39378238341968913 | 0.533678756476684 | 0.5958549222797928 | 0.46632124352331605 | 0.39378238341968913 | 0.533678756476684 | 0.6113989637305699 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9222797927461139 | 0.46632124352331605 | 0.39378238341968913 | 0.533678756476684 | 0.5958549222797928 | 4.323750323750324 |

#### `results/e0b_familiarity/gate1/calibration_fallback.csv` (410 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

| model | task | english_raw | english_avg3 | use_raw |
|---|---|---|---|---|
| gemma4-e2b | sentiment | 0.985 | 0.985 | False |
| gemma4-e2b | xnli | 0.735 | 0.63 | True |
| qwen2.5-1.5b | sentiment | 0.985 | 0.88 | True |
| qwen2.5-1.5b | xnli | 0.795 | 0.825 | False |
| qwen3-1.7b | sentiment | 0.985 | 0.985 | False |
| qwen3-1.7b | xnli | 0.615 | 0.575 | False |
| qwen3.5-2b | sentiment | 0.975 | 0.98 | False |
| qwen3.5-2b | xnli | 0.43 | 0.49 | False |
| sarvam-1 | sentiment | 0.975 | 0.98 | False |
| sarvam-1 | xnli | 0.53 | 0.55 | False |

#### `results/e0b_familiarity/gate1/fertility.csv` (2,500 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

| model | task | form | n_texts | tokens_per_word |
|---|---|---|---|---|
| qwen2.5-1.5b | xnli | english | 400 | 1.2469796341042458 |
| qwen2.5-1.5b | sentiment | english | 200 | 1.231369150779896 |
| qwen2.5-1.5b | xnli | native | 400 | 11.79860765788165 |
| qwen2.5-1.5b | sentiment | native | 200 | 11.985638921453694 |
| qwen2.5-1.5b | xnli | itrans | 400 | 4.25161611138737 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen2.5-1.5b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen2.5-1.5b | xnli | natural | 386 | 3.5423465423465426 |
| qwen2.5-1.5b | sentiment | natural | 198 | 3.5069712251557403 |
| qwen3.5-2b | xnli | english | 400 | 1.2424922333448394 |
| qwen3.5-2b | sentiment | english | 200 | 1.2268197573656845 |
| qwen3.5-2b | xnli | native | 400 | 5.230979612133267 |
| qwen3.5-2b | sentiment | native | 200 | 5.235052754982415 |
| qwen3.5-2b | xnli | itrans | 400 | 4.1282943809050225 |
| qwen3.5-2b | sentiment | itrans | 200 | 4.087631887456038 |
| qwen3.5-2b | xnli | lossy | 400 | 3.3431128791645945 |
| qwen3.5-2b | sentiment | lossy | 200 | 3.3423212192262604 |
| qwen3.5-2b | xnli | natural | 386 | 3.346283346283346 |
| qwen3.5-2b | sentiment | natural | 198 | 3.32275289231682 |
| sarvam-1 | xnli | english | 400 | 1.4326889886089058 |
| sarvam-1 | sentiment | english | 200 | 1.4204939341421143 |
| sarvam-1 | xnli | native | 400 | 2.1452013923421185 |
| sarvam-1 | sentiment | native | 200 | 2.2708089097303636 |
| sarvam-1 | xnli | itrans | 400 | 5.226255594231725 |
| sarvam-1 | sentiment | itrans | 200 | 5.238569753810082 |
| sarvam-1 | xnli | lossy | 400 | 4.335405271009448 |
| sarvam-1 | sentiment | lossy | 200 | 4.357561547479484 |
| sarvam-1 | xnli | natural | 386 | 4.323750323750324 |
| sarvam-1 | sentiment | natural | 198 | 4.29219816078315 |
| gemma4-e2b | xnli | english | 400 | 1.2397307559544357 |
| gemma4-e2b | sentiment | english | 200 | 1.2214038128249567 |
| gemma4-e2b | xnli | native | 400 | 3.1397314768771754 |
| gemma4-e2b | sentiment | native | 200 | 3.0767878077373974 |
| gemma4-e2b | xnli | itrans | 400 | 3.9604674291397313 |
| gemma4-e2b | sentiment | itrans | 200 | 3.943434935521688 |
| gemma4-e2b | xnli | lossy | 400 | 3.2031327697662855 |
| gemma4-e2b | sentiment | lossy | 200 | 3.2110199296600235 |
| gemma4-e2b | xnli | natural | 386 | 3.1711991711991714 |
| gemma4-e2b | sentiment | natural | 198 | 3.1530703055473155 |
| qwen3-1.7b | xnli | english | 400 | 1.2469796341042458 |
| qwen3-1.7b | sentiment | english | 200 | 1.231369150779896 |
| qwen3-1.7b | xnli | native | 400 | 11.79860765788165 |
| qwen3-1.7b | sentiment | native | 200 | 11.985638921453694 |
| qwen3-1.7b | xnli | itrans | 400 | 4.25161611138737 |
| qwen3-1.7b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen3-1.7b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen3-1.7b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen3-1.7b | xnli | natural | 386 | 3.5423465423465426 |
| qwen3-1.7b | sentiment | natural | 198 | 3.5069712251557403 |

#### `results/e0b_familiarity/gate1/item_fragmentation.csv` (10,206 bytes; first commit c90c964 2026-10-15 16:51:21 +0530)

| model | task | form | n | accuracy | constant_label_rate | tpw_mean | tpw_sd | corr_tpw_chars | counted | coef_tpw_per_sd | se_tpw | p_tpw | coef_tpw_per_token | coef_chars_per_sd | p_chars | fit | p_holm | sig_neg | sig_pos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen2.5-1.5b | sentiment | itrans | 200 | 0.495 | 0.995 | 4.295531282552031 | 0.6353913433819524 | -0.029221993249686124 | False | 0.020137791449525273 | 0.14880834413479904 | 0.8923533137444825 | 0.03169352503661646 | 0.8491542799174431 | 3.6433012275901204e-05 | ok | 1.0 | False | False |
| qwen2.5-1.5b | sentiment | lossy | 200 | 0.5 | 0.97 | 3.617700241612504 | 0.5450644743708598 | 0.00623293755038356 | False | -0.16120608731752709 | 0.15078477178326288 | 0.28501837323324053 | -0.29575599749662473 | 0.8050281625911375 | 5.8362724180034205e-05 | ok | 1.0 | False | False |
| qwen2.5-1.5b | sentiment | native | 200 | 0.705 | 0.625 | 12.18603705463841 | 1.8799383464128974 | -0.017206523693710795 | True | 0.019187497246309533 | 0.15227391491834286 | 0.8997268095559198 | 0.010206450271585298 | 0.4016997473198773 | 0.03797386821968426 | ok | 1.0 | False | False |
| qwen2.5-1.5b | sentiment | natural | 198 | 0.5151515151515151 | 0.9696969696969697 | 3.5705831888882225 | 0.5973980596514787 | -0.021794276094276047 | False | -0.17087426160936933 | 0.15241708930825826 | 0.26224679882309665 | -0.2860308279358275 | 0.9340894047790863 | 1.8885411682290647e-05 | ok | 1.0 | False | False |
| qwen2.5-1.5b | xnli | itrans | 200 | 0.32 | 0.67 | 4.279229317133926 | 0.52166381468296 | 0.15637325583371384 | True | -0.0295362244132114 | 0.15384557976115876 | 0.847753034664569 | -0.056619270077534464 | 0.024032788044460362 | 0.8755197662165195 | ok | 1.0 | False | False |
| qwen2.5-1.5b | xnli | lossy | 200 | 0.325 | 0.75 | 3.582998414876505 | 0.45189903105711077 | 0.12072208770837949 | True | -0.09470884053329189 | 0.154301286197025 | 0.5393530179370849 | -0.20957964948883157 | 0.17921563471412597 | 0.2418879419506289 | ok | 1.0 | False | False |
| qwen2.5-1.5b | xnli | native | 200 | 0.4 | 0.86 | 11.862871403964448 | 1.5471485455629497 | 0.2531646222121239 | True | 0.008152951333344266 | 0.14922069726055961 | 0.9564277672952313 | 0.0052696629271481565 | 0.04241263090715762 | 0.7762067366888769 | ok | 1.0 | False | False |
| qwen2.5-1.5b | xnli | natural | 193 | 0.32124352331606215 | 0.7409326424870466 | 3.578814591766691 | 0.48379090985598344 | 0.07969949120426431 | True | 0.011044331912917819 | 0.1561528761249605 | 0.9436144841256282 | 0.022828729701030417 | 0.2218875864941163 | 0.155715606110982 | ok | 1.0 | False | False |
| qwen3.5-2b | sentiment | itrans | 200 | 0.655 | 0.775 | 4.156332233063232 | 0.6284690069441601 | -0.033276241213404154 | True | 0.05043293567301275 | 0.15272481549903397 | 0.7412330081419982 | 0.08024729161782476 | -0.18566900883227042 | 0.20287806748298653 | ok | 1.0 | False | False |
| qwen3.5-2b | sentiment | lossy | 200 | 0.68 | 0.72 | 3.3909360409180476 | 0.5056319956272015 | -0.002413036691860341 | True | 0.0060308627488251864 | 0.1514996958435485 | 0.96824639367394 | 0.011927375642722764 | 0.02180219315105461 | 0.8865318498861057 | ok | 1.0 | False | False |
| qwen3.5-2b | sentiment | native | 200 | 0.735 | 0.755 | 5.318592150817758 | 0.84029469765919 | -0.015325835946828686 | True | 0.13080950770688074 | 0.16972564913638766 | 0.44087796070861385 | 0.15567099027433703 | -0.15252502502398294 | 0.31984362955836576 | ok | 1.0 | False | False |
| qwen3.5-2b | sentiment | natural | 198 | 0.7222222222222222 | 0.6818181818181818 | 3.3771164397576046 | 0.5523635806816547 | -0.006634344542692214 | True | -0.19028396443320458 | 0.15603686060764832 | 0.22266173738557848 | -0.3444904245829913 | 0.10073049676724805 | 0.5472486855765377 | ok | 1.0 | False | False |
| qwen3.5-2b | xnli | itrans | 200 | 0.34 | 0.995 | 4.152864362065122 | 0.49878860622473964 | 0.1635873026012015 | False | 0.298103534716451 | 0.1533149960960309 | 0.05184891870525447 | 0.5976550606734072 | 0.046716536147786154 | 0.7600909364816562 | ok | 0.9851294553998349 | False | False |
| qwen3.5-2b | xnli | lossy | 200 | 0.335 | 0.99 | 3.36789723190433 | 0.4067928418516283 | 0.13325458710447552 | False | 0.25848139815521726 | 0.15309207260986685 | 0.09133353977349602 | 0.6354128479219764 | 0.10476543729503009 | 0.49160635284524135 | ok | 1.0 | False | False |
| qwen3.5-2b | xnli | native | 200 | 0.34 | 0.995 | 5.256461428990416 | 0.6941775475443901 | 0.16335111339779476 | False | 0.2274678064150156 | 0.1524726963295703 | 0.1357360404618232 | 0.327679578833497 | 0.0634679200486208 | 0.6771787227503703 | ok | 1.0 | False | False |
| qwen3.5-2b | xnli | natural | 193 | 0.34196891191709844 | 0.9948186528497409 | 3.3764122156104937 | 0.4323540050064572 | 0.09483068914028005 | False | 0.1180936076416053 | 0.15299940014703192 | 0.4401993225332149 | 0.2731410054588059 | 0.11135408793379033 | 0.46606399937425014 | ok | 1.0 | False | False |
| sarvam-1 | sentiment | itrans | 200 | 0.82 | 0.61 | 5.315650510051601 | 0.8175386096549263 | -0.00023145839923382103 | True | 0.034342767207044 | 0.17482183614657493 | 0.844262362710535 | 0.04200751720036769 | 0.8064539893348127 | 0.006502859506820967 | ok | 1.0 | False | False |
| sarvam-1 | sentiment | lossy | 200 | 0.895 | 0.575 | 4.411816434567003 | 0.6785314747737963 | 0.024124119678953747 | True | 0.13216206957683782 | 0.2161813994767173 | 0.5409692097707373 | 0.1947766234733577 | 1.0342866679110285 | 0.011913680618751546 | ok | 1.0 | False | False |
| sarvam-1 | sentiment | native | 200 | 0.955 | 0.505 | 2.3062248131139005 | 0.5073497158831363 | -0.015980113007359534 | True | -0.39744156248838003 | 0.24172998543908172 | 0.10014419096576763 | -0.7833680596362596 | 1.04750233965251 | 0.10233656310715464 | ok | 1.0 | False | False |
| sarvam-1 | sentiment | natural | 198 | 0.8939393939393939 | 0.5808080808080808 | 4.36704327297002 | 0.7175796116081594 | -0.016566722737852188 | True | 0.2832580540831478 | 0.235053542528275 | 0.2281728615294938 | 0.3947409451173528 | 0.6552503544967758 | 0.06500123242219345 | ok | 1.0 | False | False |
| sarvam-1 | xnli | itrans | 200 | 0.385 | 0.795 | 5.254543318514297 | 0.6850427888595407 | 0.18383080514929134 | True | 0.19051946376677797 | 0.15031910823051922 | 0.2050003507261392 | 0.2781132315602574 | 0.25081173592132244 | 0.096987762970545 | ok | 1.0 | False | False |
| sarvam-1 | xnli | lossy | 200 | 0.47 | 0.58 | 4.357462984882483 | 0.5736714467093725 | 0.19379219375452456 | True | 0.07307482601428435 | 0.1448798288784082 | 0.6139927309132073 | 0.12738097116990513 | 0.10123901342459218 | 0.4849230852415213 | ok | 1.0 | False | False |
| sarvam-1 | xnli | native | 200 | 0.515 | 0.6 | 2.158664918181051 | 0.33075272637202596 | 0.04932610907906452 | True | 0.014216133916653443 | 0.14172569454167064 | 0.9201002940673233 | 0.042981154146748704 | -0.036787261487979304 | 0.7951816669798157 | ok | 1.0 | False | False |
| sarvam-1 | xnli | natural | 193 | 0.46632124352331605 | 0.5958549222797928 | 4.359152000377277 | 0.5995570790796084 | 0.1354536308130454 | True | 0.017563912018978847 | 0.14649026348667818 | 0.9045638276444232 | 0.029294812173582447 | 0.2074856052141973 | 0.1596233399168493 | ok | 1.0 | False | False |
| gemma4-e2b | sentiment | itrans | 200 | 0.755 | 0.685 | 4.010912809703324 | 0.6095010354465041 | -0.0371369692277214 | True | -0.17193558880088458 | 0.15832515897686136 | 0.27749445628702085 | -0.28209236539676946 | 0.10243441565687149 | 0.5558834156334456 | ok | 1.0 | False | False |
| gemma4-e2b | sentiment | lossy | 200 | 0.79 | 0.65 | 3.256686942128547 | 0.4736714360482115 | -0.0022654720934111887 | True | -0.11013956761212927 | 0.1696643863133137 | 0.5162340696398017 | -0.23252313572254119 | 0.08787895132363385 | 0.6301247519587359 | ok | 1.0 | False | False |
| gemma4-e2b | sentiment | native | 200 | 0.985 | 0.505 | 3.124130456123692 | 0.5346188895906202 | -0.01840920160033421 | True | -1.0265717805876313 | 0.4037955770709464 | 0.011012382299968275 | -1.92019361937196 | 0.17882913442845577 | 0.8153003290033365 | ok | 0.2202476459993655 | False | False |
| gemma4-e2b | sentiment | natural | 198 | 0.803030303030303 | 0.6717171717171717 | 3.2060617319193363 | 0.5267216974294552 | -0.01248143211006864 | True | -0.04208671093198706 | 0.17407531960047096 | 0.8089560670500968 | -0.07990312747202485 | 0.17809915609207178 | 0.37386389576140866 | ok | 1.0 | False | False |
| gemma4-e2b | xnli | itrans | 200 | 0.41 | 0.87 | 3.9840321273986934 | 0.478993100445988 | 0.13881791734848867 | True | 0.3272793501165022 | 0.14974633609075774 | 0.02884793509458976 | 0.6832652700253389 | 0.10101058837053725 | 0.49379214877671596 | ok | 0.5769587018917952 | False | False |
| gemma4-e2b | xnli | lossy | 200 | 0.4 | 0.84 | 3.221559161105713 | 0.395593692503058 | 0.151469512097525 | True | 0.24389820557211148 | 0.14834369557352822 | 0.10014672761999939 | 0.6165371445355543 | 0.11788450789993828 | 0.42456222998225757 | ok | 1.0 | False | False |
| gemma4-e2b | xnli | native | 200 | 0.545 | 0.595 | 3.122365325471196 | 0.5161018188204811 | 0.20221389281115662 | True | 0.11625119264472934 | 0.1467569396517312 | 0.42828242387479754 | 0.22524856221280962 | 0.22915218045525193 | 0.12111066251610346 | ok | 1.0 | False | False |
| gemma4-e2b | xnli | natural | 193 | 0.40414507772020725 | 0.772020725388601 | 3.195950977534124 | 0.40663057177527956 | 0.10961354660277556 | True | 0.0932075707255804 | 0.1480293302447598 | 0.5289196108498471 | 0.22921928943672898 | 0.09454604473710294 | 0.5228618756911945 | ok | 1.0 | False | False |
| qwen3-1.7b | sentiment | itrans | 200 | 0.535 | 0.645 | 4.295531282552031 | 0.6353913433819524 | -0.029221993249686124 | True | -0.02530149611830531 | 0.142877967549527 | 0.8594418920714352 | -0.03982033495079557 | 0.38070412129287184 | 0.019465686868729144 | ok | 1.0 | False | False |
| qwen3-1.7b | sentiment | lossy | 200 | 0.57 | 0.68 | 3.617700241612504 | 0.5450644743708598 | 0.00623293755038356 | True | -0.2664518759302589 | 0.14860896119422856 | 0.07297721889353588 | -0.48884469353430293 | 0.5609670355462434 | 0.0023438034791970056 | ok | 1.0 | False | False |
| qwen3-1.7b | sentiment | native | 200 | 0.835 | 0.595 | 12.18603705463841 | 1.8799383464128974 | -0.017206523693710795 | True | 0.13724957975856134 | 0.18576733154806072 | 0.4600131675990121 | 0.07300748985755129 | 1.0606603601035465 | 0.0018159799626519153 | ok | 1.0 | False | False |
| qwen3-1.7b | sentiment | natural | 198 | 0.5606060606060606 | 0.7424242424242424 | 3.5705831888882225 | 0.5973980596514787 | -0.021794276094276047 | True | -0.1672208109704956 | 0.1486686375277771 | 0.2606785627898168 | -0.27991522280479453 | 0.7593632762178534 | 0.00022596611038442683 | ok | 1.0 | False | False |
| qwen3-1.7b | xnli | itrans | 200 | 0.335 | 0.995 | 4.279229317133926 | 0.52166381468296 | 0.15637325583371384 | False | 0.24193711896126335 | 0.15306687841492697 | 0.11397010737327909 | 0.4637797603583068 | 0.10491011585379177 | 0.4932670109543761 | ok | 1.0 | False | False |
| qwen3-1.7b | xnli | lossy | 200 | 0.335 | 0.995 | 3.582998414876505 | 0.45189903105711077 | 0.12072208770837949 | False | 0.20925943425806023 | 0.152662116472194 | 0.17045731844927636 | 0.4630667912001213 | 0.11900017500859167 | 0.4335248588350843 | ok | 1.0 | False | False |
| qwen3-1.7b | xnli | native | 200 | 0.445 | 0.85 | 11.862871403964448 | 1.5471485455629497 | 0.2531646222121239 | True | -0.0003465667539688133 | 0.14727125816257575 | 0.9981223762836674 | -0.0002240035418465333 | 0.09506828919457674 | 0.5188651631094563 | ok | 1.0 | False | False |
| qwen3-1.7b | xnli | natural | 193 | 0.34196891191709844 | 0.9844559585492227 | 3.578814591766691 | 0.48379090985598344 | 0.07969949120426431 | False | 0.0517256846339676 | 0.1530107598359515 | 0.7353235522954014 | 0.10691743805059398 | 0.16652623902897165 | 0.2767580963134786 | ok | 1.0 | False | False |

#### `results/e0b_familiarity/gate1/item_fragmentation.json` (3,717 bytes; first commit c90c964 2026-10-15 16:51:21 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-15"
provenance.config.const_max = 0.95
provenance.config.predictions = "pred_cal (avg3 calibration, raw fallback)"
provenance.git_commit = "5abe5d676059b7ef049ad9e98d97534a4164a5ef"
provenance.timestamp_utc = "2026-10-15T11:20:18+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0b_item_fragmentation.py"]
sentiment.native.n_cells = 5
sentiment.native.frac_negative = 0.4
sentiment.native.n_sig_neg = 0
sentiment.native.n_sig_pos = 0
sentiment.native.verdict = "contradicted"
sentiment.romanized.n_cells = 12
sentiment.romanized.frac_negative = 0.5833333333333334
sentiment.romanized.n_sig_neg = 0
sentiment.romanized.n_sig_pos = 0
sentiment.romanized.verdict = "no evidence"
xnli.native.n_cells = 4
xnli.native.frac_negative = 0.25
xnli.native.n_sig_neg = 0
xnli.native.n_sig_pos = 0
xnli.native.verdict = "contradicted"
xnli.romanized.n_cells = 9
xnli.romanized.frac_negative = 0.2222222222222222
xnli.romanized.n_sig_neg = 0
xnli.romanized.n_sig_pos = 0
xnli.romanized.verdict = "contradicted"
sarvam_within_romanization.rows[0].task = "sentiment"
sarvam_within_romanization.rows[0].a = "natural"
sarvam_within_romanization.rows[0].b = "itrans"
sarvam_within_romanization.rows[0].n = 198
sarvam_within_romanization.rows[0].acc_a = 0.8939393939393939
sarvam_within_romanization.rows[0].acc_b = 0.8181818181818182
sarvam_within_romanization.rows[0].diff = 0.0757575757575756
sarvam_within_romanization.rows[0].a_only = 27
sarvam_within_romanization.rows[0].b_only = 12
sarvam_within_romanization.rows[0].p = 0.023702702470473
sarvam_within_romanization.rows[0].p_holm = 0.4977567518799333
sarvam_within_romanization.rows[1].task = "sentiment"
sarvam_within_romanization.rows[1].a = "lossy"
sarvam_within_romanization.rows[1].b = "itrans"
sarvam_within_romanization.rows[1].n = 200
sarvam_within_romanization.rows[1].acc_a = 0.895
sarvam_within_romanization.rows[1].acc_b = 0.82
sarvam_within_romanization.rows[1].diff = 0.075
sarvam_within_romanization.rows[1].a_only = 21
sarvam_within_romanization.rows[1].b_only = 6
sarvam_within_romanization.rows[1].p = 0.0059246122837066
sarvam_within_romanization.rows[1].p_holm = 0.1481153070926666
sarvam_within_romanization.rows[2].task = "xnli"
sarvam_within_romanization.rows[2].a = "natural"
sarvam_within_romanization.rows[2].b = "itrans"
sarvam_within_romanization.rows[2].n = 193
sarvam_within_romanization.rows[2].acc_a = 0.466321243523316
sarvam_within_romanization.rows[2].acc_b = 0.3937823834196891
sarvam_within_romanization.rows[2].diff = 0.0725388601036269
sarvam_within_romanization.rows[2].a_only = 23
sarvam_within_romanization.rows[2].b_only = 9
sarvam_within_romanization.rows[2].p = 0.0200616070069372
sarvam_within_romanization.rows[2].p_holm = 0.4413553541526198
sarvam_within_romanization.rows[3].task = "xnli"
sarvam_within_romanization.rows[3].a = "lossy"
sarvam_within_romanization.rows[3].b = "itrans"
sarvam_within_romanization.rows[3].n = 200
sarvam_within_romanization.rows[3].acc_a = 0.47
sarvam_within_romanization.rows[3].acc_b = 0.385
sarvam_within_romanization.rows[3].diff = 0.0849999999999999
sarvam_within_romanization.rows[3].a_only = 29
sarvam_within_romanization.rows[3].b_only = 12
sarvam_within_romanization.rows[3].p = 0.011507789735333
sarvam_within_romanization.rows[3].p_holm = 0.2761869536479935
sarvam_within_romanization.tokens_per_word[0].task = "xnli"
sarvam_within_romanization.tokens_per_word[0].form = "english"
sarvam_within_romanization.tokens_per_word[0].tokens_per_word = 1.43
sarvam_within_romanization.tokens_per_word[1].task = "sentiment"
sarvam_within_romanization.tokens_per_word[1].form = "english"
sarvam_within_romanization.tokens_per_word[1].tokens_per_word = 1.42
sarvam_within_romanization.tokens_per_word[2].task = "xnli"
sarvam_within_romanization.tokens_per_word[2].form = "native"
sarvam_within_romanization.tokens_per_word[2].tokens_per_word = 2.15
sarvam_within_romanization.tokens_per_word[3].task = "sentiment"
sarvam_within_romanization.tokens_per_word[3].form = "native"
sarvam_within_romanization.tokens_per_word[3].tokens_per_word = 2.27
sarvam_within_romanization.tokens_per_word[4].task = "xnli"
sarvam_within_romanization.tokens_per_word[4].form = "itrans"
sarvam_within_romanization.tokens_per_word[4].tokens_per_word = 5.23
sarvam_within_romanization.tokens_per_word[5].task = "sentiment"
sarvam_within_romanization.tokens_per_word[5].form = "itrans"
sarvam_within_romanization.tokens_per_word[5].tokens_per_word = 5.24
sarvam_within_romanization.tokens_per_word[6].task = "xnli"
sarvam_within_romanization.tokens_per_word[6].form = "lossy"
sarvam_within_romanization.tokens_per_word[6].tokens_per_word = 4.34
sarvam_within_romanization.tokens_per_word[7].task = "sentiment"
sarvam_within_romanization.tokens_per_word[7].form = "lossy"
sarvam_within_romanization.tokens_per_word[7].tokens_per_word = 4.36
sarvam_within_romanization.tokens_per_word[8].task = "xnli"
sarvam_within_romanization.tokens_per_word[8].form = "natural"
sarvam_within_romanization.tokens_per_word[8].tokens_per_word = 4.32
sarvam_within_romanization.tokens_per_word[9].task = "sentiment"
sarvam_within_romanization.tokens_per_word[9].form = "natural"
sarvam_within_romanization.tokens_per_word[9].tokens_per_word = 4.29
sarvam_within_romanization.caveat = "exploratory; ITRANS uses capital letters for long vowels/retroflexes, lossy and natural do not"
`````

#### `results/e0b_familiarity/gate1/mcnemar.csv` (3,761 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

| model | task | a | b | acc_a | acc_b | n | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | natural | native | 0.803030303030303 | 0.9848484848484849 | 198 | -0.18181818181818188 | 2 | 38 | 1.4933903003111482e-09 | 4.33083187090233e-08 | True |
| gemma4-e2b | sentiment | natural | itrans | 0.803030303030303 | 0.7575757575757576 | 198 | 0.045454545454545414 | 16 | 7 | 0.0931396484375 | 1.0 | False |
| gemma4-e2b | sentiment | lossy | itrans | 0.79 | 0.755 | 200 | 0.03500000000000003 | 18 | 11 | 0.26493089646101 | 1.0 | False |
| gemma4-e2b | xnli | natural | native | 0.40414507772020725 | 0.538860103626943 | 193 | -0.13471502590673579 | 11 | 37 | 0.0002222449626216872 | 0.005778369028163867 | True |
| gemma4-e2b | xnli | natural | itrans | 0.40414507772020725 | 0.41450777202072536 | 193 | -0.010362694300518116 | 11 | 13 | 0.8388197422027588 | 1.0 | False |
| gemma4-e2b | xnli | lossy | itrans | 0.4 | 0.41 | 200 | -0.009999999999999953 | 11 | 13 | 0.8388197422027588 | 1.0 | False |
| qwen2.5-1.5b | sentiment | natural | native | 0.5151515151515151 | 0.702020202020202 | 198 | -0.18686868686868685 | 20 | 57 | 2.926311069930838e-05 | 0.0008193670995806346 | True |
| qwen2.5-1.5b | sentiment | natural | itrans | 0.5151515151515151 | 0.4898989898989899 | 198 | 0.02525252525252525 | 6 | 1 | 0.125 | 1.0 | False |
| qwen2.5-1.5b | sentiment | lossy | itrans | 0.5 | 0.495 | 200 | 0.0050000000000000044 | 4 | 3 | 1.0 | 1.0 | False |
| qwen2.5-1.5b | xnli | natural | native | 0.32124352331606215 | 0.40414507772020725 | 193 | -0.0829015544041451 | 16 | 32 | 0.029304946720529308 | 0.5860989344105861 | False |
| qwen2.5-1.5b | xnli | natural | itrans | 0.32124352331606215 | 0.32124352331606215 | 193 | 0.0 | 15 | 15 | 1.0 | 1.0 | False |
| qwen2.5-1.5b | xnli | lossy | itrans | 0.325 | 0.32 | 200 | 0.0050000000000000044 | 18 | 17 | 0.9999999999999998 | 1.0 | False |
| qwen3-1.7b | sentiment | natural | native | 0.5606060606060606 | 0.8333333333333334 | 198 | -0.2727272727272728 | 14 | 68 | 1.1349339471612945e-09 | 3.4048018414838833e-08 | True |
| qwen3-1.7b | sentiment | natural | itrans | 0.5606060606060606 | 0.5303030303030303 | 198 | 0.030303030303030276 | 30 | 24 | 0.49661743531793345 | 1.0 | False |
| qwen3-1.7b | sentiment | lossy | itrans | 0.57 | 0.535 | 200 | 0.03499999999999992 | 32 | 25 | 0.42704285650325524 | 1.0 | False |
| qwen3-1.7b | xnli | natural | native | 0.34196891191709844 | 0.44559585492227977 | 193 | -0.10362694300518133 | 3 | 23 | 8.797645568847656e-05 | 0.002375364303588867 | True |
| qwen3-1.7b | xnli | natural | itrans | 0.34196891191709844 | 0.33678756476683935 | 193 | 0.005181347150259086 | 1 | 0 | 1.0 | 1.0 | False |
| qwen3-1.7b | xnli | lossy | itrans | 0.335 | 0.335 | 200 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| qwen3.5-2b | sentiment | natural | native | 0.7222222222222222 | 0.7373737373737373 | 198 | -0.015151515151515138 | 26 | 29 | 0.7877061896700431 | 1.0 | False |
| qwen3.5-2b | sentiment | natural | itrans | 0.7222222222222222 | 0.6565656565656566 | 198 | 0.06565656565656564 | 29 | 16 | 0.07245426016254441 | 1.0 | False |
| qwen3.5-2b | sentiment | lossy | itrans | 0.68 | 0.655 | 200 | 0.025000000000000022 | 23 | 18 | 0.5327092552361137 | 1.0 | False |
| qwen3.5-2b | xnli | natural | native | 0.34196891191709844 | 0.34196891191709844 | 193 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| qwen3.5-2b | xnli | natural | itrans | 0.34196891191709844 | 0.34196891191709844 | 193 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| qwen3.5-2b | xnli | lossy | itrans | 0.335 | 0.34 | 200 | -0.0050000000000000044 | 0 | 1 | 1.0 | 1.0 | False |
| sarvam-1 | sentiment | natural | native | 0.8939393939393939 | 0.9545454545454546 | 198 | -0.06060606060606066 | 5 | 17 | 0.01690053939819336 | 0.38871240615844727 | False |
| sarvam-1 | sentiment | natural | itrans | 0.8939393939393939 | 0.8181818181818182 | 198 | 0.07575757575757569 | 27 | 12 | 0.023702702470473014 | 0.4977567518799333 | False |
| sarvam-1 | sentiment | lossy | itrans | 0.895 | 0.82 | 200 | 0.07500000000000007 | 21 | 6 | 0.005924612283706665 | 0.14811530709266663 | False |
| sarvam-1 | xnli | natural | native | 0.46632124352331605 | 0.5129533678756477 | 193 | -0.04663212435233166 | 14 | 23 | 0.18774155899882317 | 1.0 | False |
| sarvam-1 | xnli | natural | itrans | 0.46632124352331605 | 0.39378238341968913 | 193 | 0.07253886010362692 | 23 | 9 | 0.020061607006937265 | 0.44135535415261984 | False |
| sarvam-1 | xnli | lossy | itrans | 0.47 | 0.385 | 200 | 0.08499999999999996 | 29 | 12 | 0.011507789735333063 | 0.2761869536479935 | False |

#### `results/e0b_familiarity/gate1/mcnemar_exploratory.csv` (1,229 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

| model | task | a | b | acc_a | acc_b | n | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | itrans | native | 0.755 | 0.985 | 200 | -0.22999999999999998 | 1 | 47 | 3.481659405224491e-13 | 3.481659405224491e-12 | True |
| gemma4-e2b | xnli | itrans | native | 0.41 | 0.545 | 200 | -0.13500000000000006 | 14 | 41 | 0.00035528111863147854 | 0.0017764055931573928 | True |
| qwen2.5-1.5b | sentiment | itrans | native | 0.495 | 0.705 | 200 | -0.20999999999999996 | 16 | 58 | 9.674891137601897e-07 | 7.739912910081517e-06 | True |
| qwen2.5-1.5b | xnli | itrans | native | 0.32 | 0.4 | 200 | -0.08000000000000002 | 18 | 34 | 0.03648340000835981 | 0.07768824537970431 | False |
| qwen3-1.7b | sentiment | itrans | native | 0.535 | 0.835 | 200 | -0.29999999999999993 | 14 | 74 | 5.0891941127085865e-11 | 4.580274701437728e-10 | True |
| qwen3-1.7b | xnli | itrans | native | 0.335 | 0.445 | 200 | -0.10999999999999999 | 3 | 25 | 2.744048833847046e-05 | 0.00016464293003082275 | True |
| qwen3.5-2b | sentiment | itrans | native | 0.655 | 0.735 | 200 | -0.07999999999999996 | 15 | 31 | 0.02589608179323477 | 0.07768824537970431 | False |
| qwen3.5-2b | xnli | itrans | native | 0.34 | 0.34 | 200 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| sarvam-1 | sentiment | itrans | native | 0.82 | 0.955 | 200 | -0.135 | 6 | 33 | 1.429926123819314e-05 | 0.00010009482866735198 | True |
| sarvam-1 | xnli | itrans | native | 0.385 | 0.515 | 200 | -0.13 | 14 | 40 | 0.0005354355028570622 | 0.002141742011428249 | True |

#### `results/e0b_familiarity/gate1/summary.json` (64,437 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

`````text
provenance.config.models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
provenance.config.forms = ["english", "native", "itrans", "lossy", "natural"]
provenance.config.calibration = "primary: mean of content-free N/A, '', [MASK]; raw fallback if English drops > 5 pts"
provenance.config.calibration_fallback_rows[0].model = "gemma4-e2b"
provenance.config.calibration_fallback_rows[0].task = "xnli"
provenance.config.calibration_fallback_rows[1].model = "qwen2.5-1.5b"
provenance.config.calibration_fallback_rows[1].task = "sentiment"
provenance.config.natural_items_excluded_defective = 9
provenance.config.templates = "e0_{xnli,sentiment}_v1"
provenance.config.n_per_task = 200
provenance.config.seed = 0
provenance.config.bos = "always prepended"
provenance.config.seconds_per_model_form.qwen2.5-1.5b/english = 36.487061977386475
provenance.config.seconds_per_model_form.qwen2.5-1.5b/native = 60.4139928817749
provenance.config.seconds_per_model_form.qwen2.5-1.5b/itrans = 46.802143573760986
provenance.config.seconds_per_model_form.qwen2.5-1.5b/lossy = 49.93747925758362
provenance.config.seconds_per_model_form.qwen2.5-1.5b/natural = 35.85534334182739
provenance.config.seconds_per_model_form.qwen3.5-2b/english = 100.45982670783997
provenance.config.seconds_per_model_form.qwen3.5-2b/native = 137.80759501457214
provenance.config.seconds_per_model_form.qwen3.5-2b/itrans = 135.9841856956482
provenance.config.seconds_per_model_form.qwen3.5-2b/lossy = 107.09859132766724
provenance.config.seconds_per_model_form.qwen3.5-2b/natural = 69.45307636260986
provenance.config.seconds_per_model_form.sarvam-1/english = 52.38592600822449
provenance.config.seconds_per_model_form.sarvam-1/native = 54.95457744598389
provenance.config.seconds_per_model_form.sarvam-1/itrans = 60.9882435798645
provenance.config.seconds_per_model_form.sarvam-1/lossy = 57.89579892158508
provenance.config.seconds_per_model_form.sarvam-1/natural = 44.358845472335815
provenance.config.seconds_per_model_form.gemma4-e2b/english = 89.42716455459595
provenance.config.seconds_per_model_form.gemma4-e2b/native = 94.79906296730042
provenance.config.seconds_per_model_form.gemma4-e2b/itrans = 97.28406596183777
provenance.config.seconds_per_model_form.gemma4-e2b/lossy = 92.6928346157074
provenance.config.seconds_per_model_form.gemma4-e2b/natural = 81.26459240913391
provenance.config.seconds_per_model_form.qwen3-1.7b/english = 43.18634009361267
provenance.config.seconds_per_model_form.qwen3-1.7b/native = 65.9120557308197
provenance.config.seconds_per_model_form.qwen3-1.7b/itrans = 52.16321563720703
provenance.config.seconds_per_model_form.qwen3-1.7b/lossy = 49.83175706863403
provenance.config.seconds_per_model_form.qwen3-1.7b/natural = 41.86442446708679
provenance.git_commit = "42f52d1866b427f6415cac2f4f04a5eb52024670-dirty"
provenance.timestamp_utc = "2026-10-15T11:09:28+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0b_familiarity.py", "--models", "qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b", "--tag", "gate1"]
calibration_fallback[0].model = "gemma4-e2b"
calibration_fallback[0].task = "sentiment"
calibration_fallback[0].english_raw = 0.985
calibration_fallback[0].english_avg3 = 0.985
calibration_fallback[0].use_raw = false
calibration_fallback[1].model = "gemma4-e2b"
calibration_fallback[1].task = "xnli"
calibration_fallback[1].english_raw = 0.735
calibration_fallback[1].english_avg3 = 0.63
calibration_fallback[1].use_raw = true
calibration_fallback[2].model = "qwen2.5-1.5b"
calibration_fallback[2].task = "sentiment"
calibration_fallback[2].english_raw = 0.985
calibration_fallback[2].english_avg3 = 0.88
calibration_fallback[2].use_raw = true
calibration_fallback[3].model = "qwen2.5-1.5b"
calibration_fallback[3].task = "xnli"
calibration_fallback[3].english_raw = 0.795
calibration_fallback[3].english_avg3 = 0.825
calibration_fallback[3].use_raw = false
calibration_fallback[4].model = "qwen3-1.7b"
calibration_fallback[4].task = "sentiment"
calibration_fallback[4].english_raw = 0.985
calibration_fallback[4].english_avg3 = 0.985
calibration_fallback[4].use_raw = false
calibration_fallback[5].model = "qwen3-1.7b"
calibration_fallback[5].task = "xnli"
calibration_fallback[5].english_raw = 0.615
calibration_fallback[5].english_avg3 = 0.575
calibration_fallback[5].use_raw = false
calibration_fallback[6].model = "qwen3.5-2b"
calibration_fallback[6].task = "sentiment"
calibration_fallback[6].english_raw = 0.975
calibration_fallback[6].english_avg3 = 0.98
calibration_fallback[6].use_raw = false
calibration_fallback[7].model = "qwen3.5-2b"
calibration_fallback[7].task = "xnli"
calibration_fallback[7].english_raw = 0.43
calibration_fallback[7].english_avg3 = 0.49
calibration_fallback[7].use_raw = false
calibration_fallback[8].model = "sarvam-1"
calibration_fallback[8].task = "sentiment"
calibration_fallback[8].english_raw = 0.975
calibration_fallback[8].english_avg3 = 0.98
calibration_fallback[8].use_raw = false
calibration_fallback[9].model = "sarvam-1"
calibration_fallback[9].task = "xnli"
calibration_fallback[9].english_raw = 0.53
calibration_fallback[9].english_avg3 = 0.55
calibration_fallback[9].use_raw = false
accuracy[0].model = "gemma4-e2b"
accuracy[0].task = "sentiment"
accuracy[0].form = "english"
accuracy[0].n = 200
accuracy[0].chance = 0.5
accuracy[0].acc_cal = 0.985
accuracy[0].acc_cal_ci_low = 0.965
accuracy[0].acc_cal_ci_high = 1.0
accuracy[0].constant_label_rate_cal = 0.505
accuracy[0].acc_raw = 0.985
accuracy[0].acc_raw_ci_low = 0.965
accuracy[0].acc_raw_ci_high = 1.0
accuracy[0].constant_label_rate_raw = 0.505
accuracy[0].acc_na = 0.98
accuracy[0].acc_na_ci_low = 0.96
accuracy[0].acc_na_ci_high = 0.995
accuracy[0].constant_label_rate_na = 0.5
accuracy[0].acc_avg3 = 0.985
accuracy[0].acc_avg3_ci_low = 0.965
accuracy[0].acc_avg3_ci_high = 1.0
accuracy[0].constant_label_rate_avg3 = 0.505
accuracy[0].tokens_per_word = 1.2214038128249567
accuracy[1].model = "gemma4-e2b"
accuracy[1].task = "sentiment"
accuracy[1].form = "itrans"
accuracy[1].n = 200
accuracy[1].chance = 0.5
accuracy[1].acc_cal = 0.755
accuracy[1].acc_cal_ci_low = 0.695
accuracy[1].acc_cal_ci_high = 0.81
accuracy[1].constant_label_rate_cal = 0.685
accuracy[1].acc_raw = 0.75
accuracy[1].acc_raw_ci_low = 0.69
accuracy[1].acc_raw_ci_high = 0.81
accuracy[1].constant_label_rate_raw = 0.67
accuracy[1].acc_na = 0.765
accuracy[1].acc_na_ci_low = 0.705
accuracy[1].acc_na_ci_high = 0.82
accuracy[1].constant_label_rate_na = 0.615
accuracy[1].acc_avg3 = 0.755
accuracy[1].acc_avg3_ci_low = 0.695
accuracy[1].acc_avg3_ci_high = 0.81
accuracy[1].constant_label_rate_avg3 = 0.685
accuracy[1].tokens_per_word = 3.943434935521688
accuracy[2].model = "gemma4-e2b"
accuracy[2].task = "sentiment"
accuracy[2].form = "lossy"
accuracy[2].n = 200
accuracy[2].chance = 0.5
accuracy[2].acc_cal = 0.79
accuracy[2].acc_cal_ci_low = 0.73
accuracy[2].acc_cal_ci_high = 0.845
accuracy[2].constant_label_rate_cal = 0.65
accuracy[2].acc_raw = 0.79
accuracy[2].acc_raw_ci_low = 0.73
accuracy[2].acc_raw_ci_high = 0.845
accuracy[2].constant_label_rate_raw = 0.65
accuracy[2].acc_na = 0.785
accuracy[2].acc_na_ci_low = 0.725
accuracy[2].acc_na_ci_high = 0.84
accuracy[2].constant_label_rate_na = 0.625
accuracy[2].acc_avg3 = 0.79
accuracy[2].acc_avg3_ci_low = 0.73
accuracy[2].acc_avg3_ci_high = 0.845
accuracy[2].constant_label_rate_avg3 = 0.65
accuracy[2].tokens_per_word = 3.2110199296600235
accuracy[3].model = "gemma4-e2b"
accuracy[3].task = "sentiment"
accuracy[3].form = "native"
accuracy[3].n = 200
accuracy[3].chance = 0.5
accuracy[3].acc_cal = 0.985
accuracy[3].acc_cal_ci_low = 0.965
accuracy[3].acc_cal_ci_high = 1.0
accuracy[3].constant_label_rate_cal = 0.505
accuracy[3].acc_raw = 0.985
accuracy[3].acc_raw_ci_low = 0.965
accuracy[3].acc_raw_ci_high = 1.0
accuracy[3].constant_label_rate_raw = 0.505
accuracy[3].acc_na = 0.985
accuracy[3].acc_na_ci_low = 0.965
accuracy[3].acc_na_ci_high = 1.0
accuracy[3].constant_label_rate_na = 0.505
accuracy[3].acc_avg3 = 0.985
accuracy[3].acc_avg3_ci_low = 0.965
accuracy[3].acc_avg3_ci_high = 1.0
accuracy[3].constant_label_rate_avg3 = 0.505
accuracy[3].tokens_per_word = 3.0767878077373974
accuracy[4].model = "gemma4-e2b"
accuracy[4].task = "sentiment"
accuracy[4].form = "natural"
accuracy[4].n = 198
accuracy[4].chance = 0.5
accuracy[4].acc_cal = 0.803030303030303
accuracy[4].acc_cal_ci_low = 0.7474747474747475
accuracy[4].acc_cal_ci_high = 0.8585858585858586
accuracy[4].constant_label_rate_cal = 0.6717171717171717
accuracy[4].acc_raw = 0.803030303030303
accuracy[4].acc_raw_ci_low = 0.7474747474747475
accuracy[4].acc_raw_ci_high = 0.8585858585858586
accuracy[4].constant_label_rate_raw = 0.6717171717171717
accuracy[4].acc_na = 0.8282828282828283
accuracy[4].acc_na_ci_low = 0.7727272727272727
accuracy[4].acc_na_ci_high = 0.8787878787878788
accuracy[4].constant_label_rate_na = 0.6262626262626263
accuracy[4].acc_avg3 = 0.803030303030303
accuracy[4].acc_avg3_ci_low = 0.7474747474747475
accuracy[4].acc_avg3_ci_high = 0.8585858585858586
accuracy[4].constant_label_rate_avg3 = 0.6717171717171717
accuracy[4].tokens_per_word = 3.1530703055473155
accuracy[5].model = "gemma4-e2b"
accuracy[5].task = "xnli"
accuracy[5].form = "english"
accuracy[5].n = 200
accuracy[5].chance = 0.3333333333333333
accuracy[5].acc_cal = 0.735
accuracy[5].acc_cal_ci_low = 0.675
accuracy[5].acc_cal_ci_high = 0.795
accuracy[5].constant_label_rate_cal = 0.405
accuracy[5].acc_raw = 0.735
accuracy[5].acc_raw_ci_low = 0.675
accuracy[5].acc_raw_ci_high = 0.795
accuracy[5].constant_label_rate_raw = 0.405
accuracy[5].acc_na = 0.6
accuracy[5].acc_na_ci_low = 0.53
accuracy[5].acc_na_ci_high = 0.67
accuracy[5].constant_label_rate_na = 0.56
accuracy[5].acc_avg3 = 0.63
accuracy[5].acc_avg3_ci_low = 0.565
accuracy[5].acc_avg3_ci_high = 0.695
accuracy[5].constant_label_rate_avg3 = 0.565
accuracy[5].tokens_per_word = 1.2397307559544357
accuracy[6].model = "gemma4-e2b"
accuracy[6].task = "xnli"
accuracy[6].form = "itrans"
accuracy[6].n = 200
accuracy[6].chance = 0.3333333333333333
accuracy[6].acc_cal = 0.41
accuracy[6].acc_cal_ci_low = 0.34
accuracy[6].acc_cal_ci_high = 0.48
accuracy[6].constant_label_rate_cal = 0.87
accuracy[6].acc_raw = 0.41
accuracy[6].acc_raw_ci_low = 0.34
accuracy[6].acc_raw_ci_high = 0.48
accuracy[6].constant_label_rate_raw = 0.87
accuracy[6].acc_na = 0.435
accuracy[6].acc_na_ci_low = 0.365
accuracy[6].acc_na_ci_high = 0.505
accuracy[6].constant_label_rate_na = 0.6
accuracy[6].acc_avg3 = 0.445
accuracy[6].acc_avg3_ci_low = 0.375
accuracy[6].acc_avg3_ci_high = 0.51
accuracy[6].constant_label_rate_avg3 = 0.68
accuracy[6].tokens_per_word = 3.9604674291397313
accuracy[7].model = "gemma4-e2b"
accuracy[7].task = "xnli"
accuracy[7].form = "lossy"
accuracy[7].n = 200
accuracy[7].chance = 0.3333333333333333
accuracy[7].acc_cal = 0.4
accuracy[7].acc_cal_ci_low = 0.335
accuracy[7].acc_cal_ci_high = 0.47
accuracy[7].constant_label_rate_cal = 0.84
accuracy[7].acc_raw = 0.4
accuracy[7].acc_raw_ci_low = 0.335
accuracy[7].acc_raw_ci_high = 0.47
accuracy[7].constant_label_rate_raw = 0.84
accuracy[7].acc_na = 0.395
accuracy[7].acc_na_ci_low = 0.33
accuracy[7].acc_na_ci_high = 0.46
accuracy[7].constant_label_rate_na = 0.78
accuracy[7].acc_avg3 = 0.375
accuracy[7].acc_avg3_ci_low = 0.31
accuracy[7].acc_avg3_ci_high = 0.44
accuracy[7].constant_label_rate_avg3 = 0.835
accuracy[7].tokens_per_word = 3.2031327697662855
accuracy[8].model = "gemma4-e2b"
accuracy[8].task = "xnli"
accuracy[8].form = "native"
accuracy[8].n = 200
accuracy[8].chance = 0.3333333333333333
accuracy[8].acc_cal = 0.545
accuracy[8].acc_cal_ci_low = 0.475
accuracy[8].acc_cal_ci_high = 0.615
accuracy[8].constant_label_rate_cal = 0.595
accuracy[8].acc_raw = 0.545
accuracy[8].acc_raw_ci_low = 0.475
accuracy[8].acc_raw_ci_high = 0.615
accuracy[8].constant_label_rate_raw = 0.595
accuracy[8].acc_na = 0.465
accuracy[8].acc_na_ci_low = 0.395
accuracy[8].acc_na_ci_high = 0.535
accuracy[8].constant_label_rate_na = 0.615
accuracy[8].acc_avg3 = 0.5
accuracy[8].acc_avg3_ci_low = 0.43
accuracy[8].acc_avg3_ci_high = 0.57
accuracy[8].constant_label_rate_avg3 = 0.59
accuracy[8].tokens_per_word = 3.1397314768771754
accuracy[9].model = "gemma4-e2b"
accuracy[9].task = "xnli"
accuracy[9].form = "natural"
accuracy[9].n = 193
accuracy[9].chance = 0.3333333333333333
accuracy[9].acc_cal = 0.40414507772020725
accuracy[9].acc_cal_ci_low = 0.33678756476683935
accuracy[9].acc_cal_ci_high = 0.47668393782383417
accuracy[9].constant_label_rate_cal = 0.772020725388601
accuracy[9].acc_raw = 0.40414507772020725
accuracy[9].acc_raw_ci_low = 0.33678756476683935
accuracy[9].acc_raw_ci_high = 0.47668393782383417
accuracy[9].constant_label_rate_raw = 0.772020725388601
accuracy[9].acc_na = 0.39896373056994816
accuracy[9].acc_na_ci_low = 0.3316062176165803
accuracy[9].acc_na_ci_high = 0.47150259067357514
accuracy[9].constant_label_rate_na = 0.7253886010362695
accuracy[9].acc_avg3 = 0.38860103626943004
accuracy[9].acc_avg3_ci_low = 0.32124352331606215
accuracy[9].acc_avg3_ci_high = 0.45595854922279794
accuracy[9].constant_label_rate_avg3 = 0.772020725388601
accuracy[9].tokens_per_word = 3.1711991711991714
accuracy[10].model = "qwen2.5-1.5b"
accuracy[10].task = "sentiment"
accuracy[10].form = "english"
accuracy[10].n = 200
accuracy[10].chance = 0.5
accuracy[10].acc_cal = 0.985
accuracy[10].acc_cal_ci_low = 0.965
accuracy[10].acc_cal_ci_high = 1.0
accuracy[10].constant_label_rate_cal = 0.515
accuracy[10].acc_raw = 0.985
accuracy[10].acc_raw_ci_low = 0.965
accuracy[10].acc_raw_ci_high = 1.0
accuracy[10].constant_label_rate_raw = 0.515
accuracy[10].acc_na = 0.52
accuracy[10].acc_na_ci_low = 0.45
accuracy[10].acc_na_ci_high = 0.59
accuracy[10].constant_label_rate_na = 0.98
accuracy[10].acc_avg3 = 0.88
accuracy[10].acc_avg3_ci_low = 0.835
accuracy[10].acc_avg3_ci_high = 0.925
accuracy[10].constant_label_rate_avg3 = 0.62
accuracy[10].tokens_per_word = 1.231369150779896
accuracy[11].model = "qwen2.5-1.5b"
accuracy[11].task = "sentiment"
accuracy[11].form = "itrans"
accuracy[11].n = 200
accuracy[11].chance = 0.5
accuracy[11].acc_cal = 0.495
accuracy[11].acc_cal_ci_low = 0.425
accuracy[11].acc_cal_ci_high = 0.565
accuracy[11].constant_label_rate_cal = 0.995
accuracy[11].acc_raw = 0.495
accuracy[11].acc_raw_ci_low = 0.425
accuracy[11].acc_raw_ci_high = 0.565
accuracy[11].constant_label_rate_raw = 0.995
accuracy[11].acc_na = 0.5
accuracy[11].acc_na_ci_low = 0.43
accuracy[11].acc_na_ci_high = 0.57
accuracy[11].constant_label_rate_na = 1.0
accuracy[11].acc_avg3 = 0.5
accuracy[11].acc_avg3_ci_low = 0.43
accuracy[11].acc_avg3_ci_high = 0.57
accuracy[11].constant_label_rate_avg3 = 1.0
accuracy[11].tokens_per_word = 4.22538100820633
accuracy[12].model = "qwen2.5-1.5b"
accuracy[12].task = "sentiment"
accuracy[12].form = "lossy"
accuracy[12].n = 200
accuracy[12].chance = 0.5
accuracy[12].acc_cal = 0.5
accuracy[12].acc_cal_ci_low = 0.43
accuracy[12].acc_cal_ci_high = 0.57
accuracy[12].constant_label_rate_cal = 0.97
accuracy[12].acc_raw = 0.5
accuracy[12].acc_raw_ci_low = 0.43
accuracy[12].acc_raw_ci_high = 0.57
accuracy[12].constant_label_rate_raw = 0.97
accuracy[12].acc_na = 0.5
accuracy[12].acc_na_ci_low = 0.43
accuracy[12].acc_na_ci_high = 0.57
accuracy[12].constant_label_rate_na = 1.0
accuracy[12].acc_avg3 = 0.5
accuracy[12].acc_avg3_ci_low = 0.43
accuracy[12].acc_avg3_ci_high = 0.57
accuracy[12].constant_label_rate_avg3 = 1.0
accuracy[12].tokens_per_word = 3.5679953106682296
accuracy[13].model = "qwen2.5-1.5b"
accuracy[13].task = "sentiment"
accuracy[13].form = "native"
accuracy[13].n = 200
accuracy[13].chance = 0.5
accuracy[13].acc_cal = 0.705
accuracy[13].acc_cal_ci_low = 0.64
accuracy[13].acc_cal_ci_high = 0.765
accuracy[13].constant_label_rate_cal = 0.625
accuracy[13].acc_raw = 0.705
accuracy[13].acc_raw_ci_low = 0.64
accuracy[13].acc_raw_ci_high = 0.765
accuracy[13].constant_label_rate_raw = 0.625
accuracy[13].acc_na = 0.505
accuracy[13].acc_na_ci_low = 0.435
accuracy[13].acc_na_ci_high = 0.575
accuracy[13].constant_label_rate_na = 0.995
accuracy[13].acc_avg3 = 0.615
accuracy[13].acc_avg3_ci_low = 0.545
accuracy[13].acc_avg3_ci_high = 0.68
accuracy[13].constant_label_rate_avg3 = 0.815
accuracy[13].tokens_per_word = 11.985638921453694
accuracy[14].model = "qwen2.5-1.5b"
accuracy[14].task = "sentiment"
accuracy[14].form = "natural"
accuracy[14].n = 198
accuracy[14].chance = 0.5
accuracy[14].acc_cal = 0.5151515151515151
accuracy[14].acc_cal_ci_low = 0.4444444444444444
accuracy[14].acc_cal_ci_high = 0.5858585858585859
accuracy[14].constant_label_rate_cal = 0.9696969696969697
accuracy[14].acc_raw = 0.5151515151515151
accuracy[14].acc_raw_ci_low = 0.4444444444444444
accuracy[14].acc_raw_ci_high = 0.5858585858585859
accuracy[14].constant_label_rate_raw = 0.9696969696969697
accuracy[14].acc_na = 0.494949494949495
accuracy[14].acc_na_ci_low = 0.42424242424242425
accuracy[14].acc_na_ci_high = 0.5656565656565656
accuracy[14].constant_label_rate_na = 1.0
accuracy[14].acc_avg3 = 0.494949494949495
accuracy[14].acc_avg3_ci_low = 0.42424242424242425
accuracy[14].acc_avg3_ci_high = 0.5656565656565656
accuracy[14].constant_label_rate_avg3 = 1.0
accuracy[14].tokens_per_word = 3.5069712251557403
accuracy[15].model = "qwen2.5-1.5b"
accuracy[15].task = "xnli"
accuracy[15].form = "english"
accuracy[15].n = 200
accuracy[15].chance = 0.3333333333333333
accuracy[15].acc_cal = 0.825
accuracy[15].acc_cal_ci_low = 0.77
accuracy[15].acc_cal_ci_high = 0.875
accuracy[15].constant_label_rate_cal = 0.38
accuracy[15].acc_raw = 0.795
accuracy[15].acc_raw_ci_low = 0.735
accuracy[15].acc_raw_ci_high = 0.85
accuracy[15].constant_label_rate_raw = 0.45
accuracy[15].acc_na = 0.785
accuracy[15].acc_na_ci_low = 0.73
accuracy[15].acc_na_ci_high = 0.84
accuracy[15].constant_label_rate_na = 0.49
accuracy[15].acc_avg3 = 0.825
accuracy[15].acc_avg3_ci_low = 0.77
accuracy[15].acc_avg3_ci_high = 0.875
accuracy[15].constant_label_rate_avg3 = 0.38
accuracy[15].tokens_per_word = 1.2469796341042458
accuracy[16].model = "qwen2.5-1.5b"
accuracy[16].task = "xnli"
accuracy[16].form = "itrans"
accuracy[16].n = 200
accuracy[16].chance = 0.3333333333333333
accuracy[16].acc_cal = 0.32
accuracy[16].acc_cal_ci_low = 0.255
accuracy[16].acc_cal_ci_high = 0.385
accuracy[16].constant_label_rate_cal = 0.67
accuracy[16].acc_raw = 0.375
accuracy[16].acc_raw_ci_low = 0.31
accuracy[16].acc_raw_ci_high = 0.445
accuracy[16].constant_label_rate_raw = 0.845
accuracy[16].acc_na = 0.325
accuracy[16].acc_na_ci_low = 0.26
accuracy[16].acc_na_ci_high = 0.39
accuracy[16].constant_label_rate_na = 0.965
accuracy[16].acc_avg3 = 0.32
accuracy[16].acc_avg3_ci_low = 0.255
accuracy[16].acc_avg3_ci_high = 0.385
accuracy[16].constant_label_rate_avg3 = 0.67
accuracy[16].tokens_per_word = 4.25161611138737
accuracy[17].model = "qwen2.5-1.5b"
accuracy[17].task = "xnli"
accuracy[17].form = "lossy"
accuracy[17].n = 200
accuracy[17].chance = 0.3333333333333333
accuracy[17].acc_cal = 0.325
accuracy[17].acc_cal_ci_low = 0.26
accuracy[17].acc_cal_ci_high = 0.39
accuracy[17].constant_label_rate_cal = 0.75
accuracy[17].acc_raw = 0.375
accuracy[17].acc_raw_ci_low = 0.31
accuracy[17].acc_raw_ci_high = 0.445
accuracy[17].constant_label_rate_raw = 0.84
accuracy[17].acc_na = 0.33
accuracy[17].acc_na_ci_low = 0.265
accuracy[17].acc_na_ci_high = 0.395
accuracy[17].constant_label_rate_na = 0.955
accuracy[17].acc_avg3 = 0.325
accuracy[17].acc_avg3_ci_low = 0.26
accuracy[17].acc_avg3_ci_high = 0.39
accuracy[17].constant_label_rate_avg3 = 0.75
accuracy[17].tokens_per_word = 3.5532073595226255
accuracy[18].model = "qwen2.5-1.5b"
accuracy[18].task = "xnli"
accuracy[18].form = "native"
accuracy[18].n = 200
accuracy[18].chance = 0.3333333333333333
accuracy[18].acc_cal = 0.4
accuracy[18].acc_cal_ci_low = 0.33
accuracy[18].acc_cal_ci_high = 0.465
accuracy[18].constant_label_rate_cal = 0.86
accuracy[18].acc_raw = 0.51
accuracy[18].acc_raw_ci_low = 0.445
accuracy[18].acc_raw_ci_high = 0.58
accuracy[18].constant_label_rate_raw = 0.48
accuracy[18].acc_na = 0.345
accuracy[18].acc_na_ci_low = 0.28
accuracy[18].acc_na_ci_high = 0.41
accuracy[18].constant_label_rate_na = 0.965
accuracy[18].acc_avg3 = 0.4
accuracy[18].acc_avg3_ci_low = 0.33
accuracy[18].acc_avg3_ci_high = 0.465
accuracy[18].constant_label_rate_avg3 = 0.86
accuracy[18].tokens_per_word = 11.79860765788165
accuracy[19].model = "qwen2.5-1.5b"
accuracy[19].task = "xnli"
accuracy[19].form = "natural"
accuracy[19].n = 193
accuracy[19].chance = 0.3333333333333333
accuracy[19].acc_cal = 0.32124352331606215
accuracy[19].acc_cal_ci_low = 0.2538860103626943
accuracy[19].acc_cal_ci_high = 0.38860103626943004
accuracy[19].constant_label_rate_cal = 0.7409326424870466
accuracy[19].acc_raw = 0.37305699481865284
accuracy[19].acc_raw_ci_low = 0.30569948186528495
accuracy[19].acc_raw_ci_high = 0.44041450777202074
accuracy[19].constant_label_rate_raw = 0.7461139896373057
accuracy[19].acc_na = 0.33678756476683935
accuracy[19].acc_na_ci_low = 0.2694300518134715
accuracy[19].acc_na_ci_high = 0.40414507772020725
accuracy[19].constant_label_rate_na = 0.9585492227979274
accuracy[19].acc_avg3 = 0.32124352331606215
accuracy[19].acc_avg3_ci_low = 0.2538860103626943
accuracy[19].acc_avg3_ci_high = 0.38860103626943004
accuracy[19].constant_label_rate_avg3 = 0.7409326424870466
accuracy[19].tokens_per_word = 3.5423465423465426
accuracy[20].model = "qwen3-1.7b"
accuracy[20].task = "sentiment"
accuracy[20].form = "english"
accuracy[20].n = 200
accuracy[20].chance = 0.5
accuracy[20].acc_cal = 0.985
accuracy[20].acc_cal_ci_low = 0.965
accuracy[20].acc_cal_ci_high = 1.0
accuracy[20].constant_label_rate_cal = 0.515
accuracy[20].acc_raw = 0.985
accuracy[20].acc_raw_ci_low = 0.965
accuracy[20].acc_raw_ci_high = 1.0
accuracy[20].constant_label_rate_raw = 0.515
accuracy[20].acc_na = 0.98
accuracy[20].acc_na_ci_low = 0.96
accuracy[20].acc_na_ci_high = 0.995
accuracy[20].constant_label_rate_na = 0.5
accuracy[20].acc_avg3 = 0.985
accuracy[20].acc_avg3_ci_low = 0.965
accuracy[20].acc_avg3_ci_high = 1.0
accuracy[20].constant_label_rate_avg3 = 0.515
accuracy[20].tokens_per_word = 1.231369150779896
accuracy[21].model = "qwen3-1.7b"
accuracy[21].task = "sentiment"
accuracy[21].form = "itrans"
accuracy[21].n = 200
accuracy[21].chance = 0.5
accuracy[21].acc_cal = 0.535
accuracy[21].acc_cal_ci_low = 0.465
accuracy[21].acc_cal_ci_high = 0.605
accuracy[21].constant_label_rate_cal = 0.645
accuracy[21].acc_raw = 0.58
accuracy[21].acc_raw_ci_low = 0.51
accuracy[21].acc_raw_ci_high = 0.645
accuracy[21].constant_label_rate_raw = 0.68
accuracy[21].acc_na = 0.54
accuracy[21].acc_na_ci_low = 0.47
accuracy[21].acc_na_ci_high = 0.61
accuracy[21].constant_label_rate_na = 0.85
accuracy[21].acc_avg3 = 0.535
accuracy[21].acc_avg3_ci_low = 0.465
accuracy[21].acc_avg3_ci_high = 0.605
accuracy[21].constant_label_rate_avg3 = 0.645
accuracy[21].tokens_per_word = 4.22538100820633
accuracy[22].model = "qwen3-1.7b"
accuracy[22].task = "sentiment"
accuracy[22].form = "lossy"
accuracy[22].n = 200
accuracy[22].chance = 0.5
accuracy[22].acc_cal = 0.57
accuracy[22].acc_cal_ci_low = 0.5
accuracy[22].acc_cal_ci_high = 0.64
accuracy[22].constant_label_rate_cal = 0.68
accuracy[22].acc_raw = 0.575
accuracy[22].acc_raw_ci_low = 0.505
accuracy[22].acc_raw_ci_high = 0.64
accuracy[22].constant_label_rate_raw = 0.715
accuracy[22].acc_na = 0.52
accuracy[22].acc_na_ci_low = 0.45
accuracy[22].acc_na_ci_high = 0.59
accuracy[22].constant_label_rate_na = 0.91
accuracy[22].acc_avg3 = 0.57
accuracy[22].acc_avg3_ci_low = 0.5
accuracy[22].acc_avg3_ci_high = 0.64
accuracy[22].constant_label_rate_avg3 = 0.68
accuracy[22].tokens_per_word = 3.5679953106682296
accuracy[23].model = "qwen3-1.7b"
accuracy[23].task = "sentiment"
accuracy[23].form = "native"
accuracy[23].n = 200
accuracy[23].chance = 0.5
accuracy[23].acc_cal = 0.835
accuracy[23].acc_cal_ci_low = 0.78
accuracy[23].acc_cal_ci_high = 0.885
accuracy[23].constant_label_rate_cal = 0.595
accuracy[23].acc_raw = 0.865
accuracy[23].acc_raw_ci_low = 0.815
accuracy[23].acc_raw_ci_high = 0.91
accuracy[23].constant_label_rate_raw = 0.525
accuracy[23].acc_na = 0.79
accuracy[23].acc_na_ci_low = 0.73
accuracy[23].acc_na_ci_high = 0.845
accuracy[23].constant_label_rate_na = 0.68
accuracy[23].acc_avg3 = 0.835
accuracy[23].acc_avg3_ci_low = 0.78
accuracy[23].acc_avg3_ci_high = 0.885
accuracy[23].constant_label_rate_avg3 = 0.595
accuracy[23].tokens_per_word = 11.985638921453694
accuracy[24].model = "qwen3-1.7b"
accuracy[24].task = "sentiment"
accuracy[24].form = "natural"
accuracy[24].n = 198
accuracy[24].chance = 0.5
accuracy[24].acc_cal = 0.5606060606060606
accuracy[24].acc_cal_ci_low = 0.4898989898989899
accuracy[24].acc_cal_ci_high = 0.6313131313131313
accuracy[24].constant_label_rate_cal = 0.7424242424242424
accuracy[24].acc_raw = 0.6313131313131313
accuracy[24].acc_raw_ci_low = 0.5656565656565656
accuracy[24].acc_raw_ci_high = 0.696969696969697
accuracy[24].constant_label_rate_raw = 0.5909090909090909
accuracy[24].acc_na = 0.5202020202020202
accuracy[24].acc_na_ci_low = 0.4494949494949495
accuracy[24].acc_na_ci_high = 0.5909090909090909
accuracy[24].constant_label_rate_na = 0.9040404040404041
accuracy[24].acc_avg3 = 0.5606060606060606
accuracy[24].acc_avg3_ci_low = 0.4898989898989899
accuracy[24].acc_avg3_ci_high = 0.6313131313131313
accuracy[24].constant_label_rate_avg3 = 0.7424242424242424
accuracy[24].tokens_per_word = 3.5069712251557403
accuracy[25].model = "qwen3-1.7b"
accuracy[25].task = "xnli"
accuracy[25].form = "english"
accuracy[25].n = 200
accuracy[25].chance = 0.3333333333333333
accuracy[25].acc_cal = 0.575
accuracy[25].acc_cal_ci_low = 0.505
accuracy[25].acc_cal_ci_high = 0.645
accuracy[25].constant_label_rate_cal = 0.71
accuracy[25].acc_raw = 0.615
accuracy[25].acc_raw_ci_low = 0.545
accuracy[25].acc_raw_ci_high = 0.68
accuracy[25].constant_label_rate_raw = 0.53
accuracy[25].acc_na = 0.54
accuracy[25].acc_na_ci_low = 0.47
accuracy[25].acc_na_ci_high = 0.61
accuracy[25].constant_label_rate_na = 0.765
accuracy[25].acc_avg3 = 0.575
accuracy[25].acc_avg3_ci_low = 0.505
accuracy[25].acc_avg3_ci_high = 0.645
accuracy[25].constant_label_rate_avg3 = 0.71
accuracy[25].tokens_per_word = 1.2469796341042458
accuracy[26].model = "qwen3-1.7b"
accuracy[26].task = "xnli"
accuracy[26].form = "itrans"
accuracy[26].n = 200
accuracy[26].chance = 0.3333333333333333
accuracy[26].acc_cal = 0.335
accuracy[26].acc_cal_ci_low = 0.27
accuracy[26].acc_cal_ci_high = 0.4
accuracy[26].constant_label_rate_cal = 0.995
accuracy[26].acc_raw = 0.37
accuracy[26].acc_raw_ci_low = 0.305
accuracy[26].acc_raw_ci_high = 0.44
accuracy[26].constant_label_rate_raw = 0.8
accuracy[26].acc_na = 0.335
accuracy[26].acc_na_ci_low = 0.27
accuracy[26].acc_na_ci_high = 0.4
accuracy[26].constant_label_rate_na = 0.995
accuracy[26].acc_avg3 = 0.335
accuracy[26].acc_avg3_ci_low = 0.27
accuracy[26].acc_avg3_ci_high = 0.4
accuracy[26].constant_label_rate_avg3 = 0.995
accuracy[26].tokens_per_word = 4.25161611138737
accuracy[27].model = "qwen3-1.7b"
accuracy[27].task = "xnli"
accuracy[27].form = "lossy"
accuracy[27].n = 200
accuracy[27].chance = 0.3333333333333333
accuracy[27].acc_cal = 0.335
accuracy[27].acc_cal_ci_low = 0.27
accuracy[27].acc_cal_ci_high = 0.4
accuracy[27].constant_label_rate_cal = 0.995
accuracy[27].acc_raw = 0.415
accuracy[27].acc_raw_ci_low = 0.345
accuracy[27].acc_raw_ci_high = 0.485
accuracy[27].constant_label_rate_raw = 0.795
accuracy[27].acc_na = 0.335
accuracy[27].acc_na_ci_low = 0.27
accuracy[27].acc_na_ci_high = 0.4
accuracy[27].constant_label_rate_na = 0.995
accuracy[27].acc_avg3 = 0.335
accuracy[27].acc_avg3_ci_low = 0.27
accuracy[27].acc_avg3_ci_high = 0.4
accuracy[27].constant_label_rate_avg3 = 0.995
accuracy[27].tokens_per_word = 3.5532073595226255
accuracy[28].model = "qwen3-1.7b"
accuracy[28].task = "xnli"
accuracy[28].form = "native"
accuracy[28].n = 200
accuracy[28].chance = 0.3333333333333333
accuracy[28].acc_cal = 0.445
accuracy[28].acc_cal_ci_low = 0.375
accuracy[28].acc_cal_ci_high = 0.515
accuracy[28].constant_label_rate_cal = 0.85
accuracy[28].acc_raw = 0.43
accuracy[28].acc_raw_ci_low = 0.36
accuracy[28].acc_raw_ci_high = 0.5
accuracy[28].constant_label_rate_raw = 0.61
accuracy[28].acc_na = 0.425
accuracy[28].acc_na_ci_low = 0.355
accuracy[28].acc_na_ci_high = 0.495
accuracy[28].constant_label_rate_na = 0.89
accuracy[28].acc_avg3 = 0.445
accuracy[28].acc_avg3_ci_low = 0.375
accuracy[28].acc_avg3_ci_high = 0.515
accuracy[28].constant_label_rate_avg3 = 0.85
accuracy[28].tokens_per_word = 11.79860765788165
accuracy[29].model = "qwen3-1.7b"
accuracy[29].task = "xnli"
accuracy[29].form = "natural"
accuracy[29].n = 193
accuracy[29].chance = 0.3333333333333333
accuracy[29].acc_cal = 0.34196891191709844
accuracy[29].acc_cal_ci_low = 0.27461139896373055
accuracy[29].acc_cal_ci_high = 0.40932642487046633
accuracy[29].constant_label_rate_cal = 0.9844559585492227
accuracy[29].acc_raw = 0.39896373056994816
accuracy[29].acc_raw_ci_low = 0.3316062176165803
accuracy[29].acc_raw_ci_high = 0.46632124352331605
accuracy[29].constant_label_rate_raw = 0.7979274611398963
accuracy[29].acc_na = 0.33678756476683935
accuracy[29].acc_na_ci_low = 0.2694300518134715
accuracy[29].acc_na_ci_high = 0.40414507772020725
accuracy[29].constant_label_rate_na = 0.9948186528497409
accuracy[29].acc_avg3 = 0.34196891191709844
accuracy[29].acc_avg3_ci_low = 0.27461139896373055
accuracy[29].acc_avg3_ci_high = 0.40932642487046633
accuracy[29].constant_label_rate_avg3 = 0.9844559585492227
accuracy[29].tokens_per_word = 3.5423465423465426
accuracy[30].model = "qwen3.5-2b"
accuracy[30].task = "sentiment"
accuracy[30].form = "english"
accuracy[30].n = 200
accuracy[30].chance = 0.5
accuracy[30].acc_cal = 0.98
accuracy[30].acc_cal_ci_low = 0.96
accuracy[30].acc_cal_ci_high = 0.995
accuracy[30].constant_label_rate_cal = 0.51
accuracy[30].acc_raw = 0.975
accuracy[30].acc_raw_ci_low = 0.95
accuracy[30].acc_raw_ci_high = 0.995
accuracy[30].constant_label_rate_raw = 0.505
accuracy[30].acc_na = 0.975
accuracy[30].acc_na_ci_low = 0.95
accuracy[30].acc_na_ci_high = 0.995
accuracy[30].constant_label_rate_na = 0.525
accuracy[30].acc_avg3 = 0.98
accuracy[30].acc_avg3_ci_low = 0.96
accuracy[30].acc_avg3_ci_high = 0.995
accuracy[30].constant_label_rate_avg3 = 0.51
accuracy[30].tokens_per_word = 1.2268197573656845
accuracy[31].model = "qwen3.5-2b"
accuracy[31].task = "sentiment"
accuracy[31].form = "itrans"
accuracy[31].n = 200
accuracy[31].chance = 0.5
accuracy[31].acc_cal = 0.655
accuracy[31].acc_cal_ci_low = 0.59
accuracy[31].acc_cal_ci_high = 0.72
accuracy[31].constant_label_rate_cal = 0.775
accuracy[31].acc_raw = 0.675
accuracy[31].acc_raw_ci_low = 0.61
accuracy[31].acc_raw_ci_high = 0.74
accuracy[31].constant_label_rate_raw = 0.665
accuracy[31].acc_na = 0.615
accuracy[31].acc_na_ci_low = 0.545
accuracy[31].acc_na_ci_high = 0.685
accuracy[31].constant_label_rate_na = 0.855
accuracy[31].acc_avg3 = 0.655
accuracy[31].acc_avg3_ci_low = 0.59
accuracy[31].acc_avg3_ci_high = 0.72
accuracy[31].constant_label_rate_avg3 = 0.775
accuracy[31].tokens_per_word = 4.087631887456038
accuracy[32].model = "qwen3.5-2b"
accuracy[32].task = "sentiment"
accuracy[32].form = "lossy"
accuracy[32].n = 200
accuracy[32].chance = 0.5
accuracy[32].acc_cal = 0.68
accuracy[32].acc_cal_ci_low = 0.615
accuracy[32].acc_cal_ci_high = 0.74
accuracy[32].constant_label_rate_cal = 0.72
accuracy[32].acc_raw = 0.675
accuracy[32].acc_raw_ci_low = 0.61
accuracy[32].acc_raw_ci_high = 0.735
accuracy[32].constant_label_rate_raw = 0.645
accuracy[32].acc_na = 0.645
accuracy[32].acc_na_ci_low = 0.58
accuracy[32].acc_na_ci_high = 0.71
accuracy[32].constant_label_rate_na = 0.815
accuracy[32].acc_avg3 = 0.68
accuracy[32].acc_avg3_ci_low = 0.615
accuracy[32].acc_avg3_ci_high = 0.74
accuracy[32].constant_label_rate_avg3 = 0.72
accuracy[32].tokens_per_word = 3.3423212192262604
accuracy[33].model = "qwen3.5-2b"
accuracy[33].task = "sentiment"
accuracy[33].form = "native"
accuracy[33].n = 200
accuracy[33].chance = 0.5
accuracy[33].acc_cal = 0.735
accuracy[33].acc_cal_ci_low = 0.67
accuracy[33].acc_cal_ci_high = 0.795
accuracy[33].constant_label_rate_cal = 0.755
accuracy[33].acc_raw = 0.785
accuracy[33].acc_raw_ci_low = 0.725
accuracy[33].acc_raw_ci_high = 0.84
accuracy[33].constant_label_rate_raw = 0.705
accuracy[33].acc_na = 0.675
accuracy[33].acc_na_ci_low = 0.61
accuracy[33].acc_na_ci_high = 0.74
accuracy[33].constant_label_rate_na = 0.815
accuracy[33].acc_avg3 = 0.735
accuracy[33].acc_avg3_ci_low = 0.67
accuracy[33].acc_avg3_ci_high = 0.795
accuracy[33].constant_label_rate_avg3 = 0.755
accuracy[33].tokens_per_word = 5.235052754982415
accuracy[34].model = "qwen3.5-2b"
accuracy[34].task = "sentiment"
accuracy[34].form = "natural"
accuracy[34].n = 198
accuracy[34].chance = 0.5
accuracy[34].acc_cal = 0.7222222222222222
accuracy[34].acc_cal_ci_low = 0.6616161616161617
accuracy[34].acc_cal_ci_high = 0.7828282828282829
accuracy[34].constant_label_rate_cal = 0.6818181818181818
accuracy[34].acc_raw = 0.7373737373737373
accuracy[34].acc_raw_ci_low = 0.6767676767676768
accuracy[34].acc_raw_ci_high = 0.797979797979798
accuracy[34].constant_label_rate_raw = 0.5757575757575758
accuracy[34].acc_na = 0.6818181818181818
accuracy[34].acc_na_ci_low = 0.6161616161616161
accuracy[34].acc_na_ci_high = 0.7424242424242424
accuracy[34].constant_label_rate_na = 0.7525252525252525
accuracy[34].acc_avg3 = 0.7222222222222222
accuracy[34].acc_avg3_ci_low = 0.6616161616161617
accuracy[34].acc_avg3_ci_high = 0.7828282828282829
accuracy[34].constant_label_rate_avg3 = 0.6818181818181818
accuracy[34].tokens_per_word = 3.32275289231682
accuracy[35].model = "qwen3.5-2b"
accuracy[35].task = "xnli"
accuracy[35].form = "english"
accuracy[35].n = 200
accuracy[35].chance = 0.3333333333333333
accuracy[35].acc_cal = 0.49
accuracy[35].acc_cal_ci_low = 0.42
accuracy[35].acc_cal_ci_high = 0.56
accuracy[35].constant_label_rate_cal = 0.805
accuracy[35].acc_raw = 0.43
accuracy[35].acc_raw_ci_low = 0.36
accuracy[35].acc_raw_ci_high = 0.5
accuracy[35].constant_label_rate_raw = 0.89
accuracy[35].acc_na = 0.45
accuracy[35].acc_na_ci_low = 0.38
accuracy[35].acc_na_ci_high = 0.52
accuracy[35].constant_label_rate_na = 0.845
accuracy[35].acc_avg3 = 0.49
accuracy[35].acc_avg3_ci_low = 0.42
accuracy[35].acc_avg3_ci_high = 0.56
accuracy[35].constant_label_rate_avg3 = 0.805
accuracy[35].tokens_per_word = 1.2424922333448394
accuracy[36].model = "qwen3.5-2b"
accuracy[36].task = "xnli"
accuracy[36].form = "itrans"
accuracy[36].n = 200
accuracy[36].chance = 0.3333333333333333
accuracy[36].acc_cal = 0.34
accuracy[36].acc_cal_ci_low = 0.275
accuracy[36].acc_cal_ci_high = 0.405
accuracy[36].constant_label_rate_cal = 0.995
accuracy[36].acc_raw = 0.34
accuracy[36].acc_raw_ci_low = 0.275
accuracy[36].acc_raw_ci_high = 0.405
accuracy[36].constant_label_rate_raw = 0.995
accuracy[36].acc_na = 0.34
accuracy[36].acc_na_ci_low = 0.275
accuracy[36].acc_na_ci_high = 0.405
accuracy[36].constant_label_rate_na = 0.995
accuracy[36].acc_avg3 = 0.34
accuracy[36].acc_avg3_ci_low = 0.275
accuracy[36].acc_avg3_ci_high = 0.405
accuracy[36].constant_label_rate_avg3 = 0.995
accuracy[36].tokens_per_word = 4.1282943809050225
accuracy[37].model = "qwen3.5-2b"
accuracy[37].task = "xnli"
accuracy[37].form = "lossy"
accuracy[37].n = 200
accuracy[37].chance = 0.3333333333333333
accuracy[37].acc_cal = 0.335
accuracy[37].acc_cal_ci_low = 0.27
accuracy[37].acc_cal_ci_high = 0.4
accuracy[37].constant_label_rate_cal = 0.99
accuracy[37].acc_raw = 0.34
accuracy[37].acc_raw_ci_low = 0.275
accuracy[37].acc_raw_ci_high = 0.405
accuracy[37].constant_label_rate_raw = 0.995
accuracy[37].acc_na = 0.335
accuracy[37].acc_na_ci_low = 0.27
accuracy[37].acc_na_ci_high = 0.4
accuracy[37].constant_label_rate_na = 0.99
accuracy[37].acc_avg3 = 0.335
accuracy[37].acc_avg3_ci_low = 0.27
accuracy[37].acc_avg3_ci_high = 0.4
accuracy[37].constant_label_rate_avg3 = 0.99
accuracy[37].tokens_per_word = 3.3431128791645945
accuracy[38].model = "qwen3.5-2b"
accuracy[38].task = "xnli"
accuracy[38].form = "native"
accuracy[38].n = 200
accuracy[38].chance = 0.3333333333333333
accuracy[38].acc_cal = 0.34
accuracy[38].acc_cal_ci_low = 0.275
accuracy[38].acc_cal_ci_high = 0.405
accuracy[38].constant_label_rate_cal = 0.995
accuracy[38].acc_raw = 0.34
accuracy[38].acc_raw_ci_low = 0.275
accuracy[38].acc_raw_ci_high = 0.405
accuracy[38].constant_label_rate_raw = 0.995
accuracy[38].acc_na = 0.34
accuracy[38].acc_na_ci_low = 0.275
accuracy[38].acc_na_ci_high = 0.405
accuracy[38].constant_label_rate_na = 0.995
accuracy[38].acc_avg3 = 0.34
accuracy[38].acc_avg3_ci_low = 0.275
accuracy[38].acc_avg3_ci_high = 0.405
accuracy[38].constant_label_rate_avg3 = 0.995
accuracy[38].tokens_per_word = 5.230979612133267
accuracy[39].model = "qwen3.5-2b"
accuracy[39].task = "xnli"
accuracy[39].form = "natural"
accuracy[39].n = 193
accuracy[39].chance = 0.3333333333333333
accuracy[39].acc_cal = 0.34196891191709844
accuracy[39].acc_cal_ci_low = 0.27461139896373055
accuracy[39].acc_cal_ci_high = 0.40932642487046633
accuracy[39].constant_label_rate_cal = 0.9948186528497409
accuracy[39].acc_raw = 0.34196891191709844
accuracy[39].acc_raw_ci_low = 0.27461139896373055
accuracy[39].acc_raw_ci_high = 0.40932642487046633
accuracy[39].constant_label_rate_raw = 0.9948186528497409
accuracy[39].acc_na = 0.34196891191709844
accuracy[39].acc_na_ci_low = 0.27461139896373055
accuracy[39].acc_na_ci_high = 0.40932642487046633
accuracy[39].constant_label_rate_na = 0.9948186528497409
accuracy[39].acc_avg3 = 0.34196891191709844
accuracy[39].acc_avg3_ci_low = 0.27461139896373055
accuracy[39].acc_avg3_ci_high = 0.40932642487046633
accuracy[39].constant_label_rate_avg3 = 0.9948186528497409
accuracy[39].tokens_per_word = 3.346283346283346
accuracy[40].model = "sarvam-1"
accuracy[40].task = "sentiment"
accuracy[40].form = "english"
accuracy[40].n = 200
accuracy[40].chance = 0.5
accuracy[40].acc_cal = 0.98
accuracy[40].acc_cal_ci_low = 0.96
accuracy[40].acc_cal_ci_high = 0.995
accuracy[40].constant_label_rate_cal = 0.51
accuracy[40].acc_raw = 0.975
accuracy[40].acc_raw_ci_low = 0.95
accuracy[40].acc_raw_ci_high = 0.995
accuracy[40].constant_label_rate_raw = 0.505
accuracy[40].acc_na = 0.975
accuracy[40].acc_na_ci_low = 0.95
accuracy[40].acc_na_ci_high = 0.995
accuracy[40].constant_label_rate_na = 0.515
accuracy[40].acc_avg3 = 0.98
accuracy[40].acc_avg3_ci_low = 0.96
accuracy[40].acc_avg3_ci_high = 0.995
accuracy[40].constant_label_rate_avg3 = 0.51
accuracy[40].tokens_per_word = 1.4204939341421143
accuracy[41].model = "sarvam-1"
accuracy[41].task = "sentiment"
accuracy[41].form = "itrans"
accuracy[41].n = 200
accuracy[41].chance = 0.5
accuracy[41].acc_cal = 0.82
accuracy[41].acc_cal_ci_low = 0.765
accuracy[41].acc_cal_ci_high = 0.87
accuracy[41].constant_label_rate_cal = 0.61
accuracy[41].acc_raw = 0.845
accuracy[41].acc_raw_ci_low = 0.795
accuracy[41].acc_raw_ci_high = 0.895
accuracy[41].constant_label_rate_raw = 0.515
accuracy[41].acc_na = 0.78
accuracy[41].acc_na_ci_low = 0.72
accuracy[41].acc_na_ci_high = 0.835
accuracy[41].constant_label_rate_na = 0.69
accuracy[41].acc_avg3 = 0.82
accuracy[41].acc_avg3_ci_low = 0.765
accuracy[41].acc_avg3_ci_high = 0.87
accuracy[41].constant_label_rate_avg3 = 0.61
accuracy[41].tokens_per_word = 5.238569753810082
accuracy[42].model = "sarvam-1"
accuracy[42].task = "sentiment"
accuracy[42].form = "lossy"
accuracy[42].n = 200
accuracy[42].chance = 0.5
accuracy[42].acc_cal = 0.895
accuracy[42].acc_cal_ci_low = 0.85
accuracy[42].acc_cal_ci_high = 0.935
accuracy[42].constant_label_rate_cal = 0.575
accuracy[42].acc_raw = 0.91
accuracy[42].acc_raw_ci_low = 0.87
accuracy[42].acc_raw_ci_high = 0.95
accuracy[42].constant_label_rate_raw = 0.51
accuracy[42].acc_na = 0.86
accuracy[42].acc_na_ci_low = 0.81
accuracy[42].acc_na_ci_high = 0.905
accuracy[42].constant_label_rate_na = 0.63
accuracy[42].acc_avg3 = 0.895
accuracy[42].acc_avg3_ci_low = 0.85
accuracy[42].acc_avg3_ci_high = 0.935
accuracy[42].constant_label_rate_avg3 = 0.575
accuracy[42].tokens_per_word = 4.357561547479484
accuracy[43].model = "sarvam-1"
accuracy[43].task = "sentiment"
accuracy[43].form = "native"
accuracy[43].n = 200
accuracy[43].chance = 0.5
accuracy[43].acc_cal = 0.955
accuracy[43].acc_cal_ci_low = 0.925
accuracy[43].acc_cal_ci_high = 0.98
accuracy[43].constant_label_rate_cal = 0.505
accuracy[43].acc_raw = 0.96
accuracy[43].acc_raw_ci_low = 0.93
accuracy[43].acc_raw_ci_high = 0.985
accuracy[43].constant_label_rate_raw = 0.53
accuracy[43].acc_na = 0.96
accuracy[43].acc_na_ci_low = 0.93
accuracy[43].acc_na_ci_high = 0.985
accuracy[43].constant_label_rate_na = 0.51
accuracy[43].acc_avg3 = 0.955
accuracy[43].acc_avg3_ci_low = 0.925
accuracy[43].acc_avg3_ci_high = 0.98
accuracy[43].constant_label_rate_avg3 = 0.505
accuracy[43].tokens_per_word = 2.2708089097303636
accuracy[44].model = "sarvam-1"
accuracy[44].task = "sentiment"
accuracy[44].form = "natural"
accuracy[44].n = 198
accuracy[44].chance = 0.5
accuracy[44].acc_cal = 0.8939393939393939
accuracy[44].acc_cal_ci_low = 0.8484848484848485
accuracy[44].acc_cal_ci_high = 0.9343434343434344
accuracy[44].constant_label_rate_cal = 0.5808080808080808
accuracy[44].acc_raw = 0.9040404040404041
accuracy[44].acc_raw_ci_low = 0.8635101010101012
accuracy[44].acc_raw_ci_high = 0.9444444444444444
accuracy[44].constant_label_rate_raw = 0.5303030303030303
accuracy[44].acc_na = 0.8484848484848485
accuracy[44].acc_na_ci_low = 0.797979797979798
accuracy[44].acc_na_ci_high = 0.898989898989899
accuracy[44].constant_label_rate_na = 0.6464646464646465
accuracy[44].acc_avg3 = 0.8939393939393939
accuracy[44].acc_avg3_ci_low = 0.8484848484848485
accuracy[44].acc_avg3_ci_high = 0.9343434343434344
accuracy[44].constant_label_rate_avg3 = 0.5808080808080808
accuracy[44].tokens_per_word = 4.29219816078315
accuracy[45].model = "sarvam-1"
accuracy[45].task = "xnli"
accuracy[45].form = "english"
accuracy[45].n = 200
accuracy[45].chance = 0.3333333333333333
accuracy[45].acc_cal = 0.55
accuracy[45].acc_cal_ci_low = 0.48
accuracy[45].acc_cal_ci_high = 0.62
accuracy[45].constant_label_rate_cal = 0.545
accuracy[45].acc_raw = 0.53
accuracy[45].acc_raw_ci_low = 0.46
accuracy[45].acc_raw_ci_high = 0.6
accuracy[45].constant_label_rate_raw = 0.63
accuracy[45].acc_na = 0.475
accuracy[45].acc_na_ci_low = 0.405
accuracy[45].acc_na_ci_high = 0.545
accuracy[45].constant_label_rate_na = 0.655
accuracy[45].acc_avg3 = 0.55
accuracy[45].acc_avg3_ci_low = 0.48
accuracy[45].acc_avg3_ci_high = 0.62
accuracy[45].constant_label_rate_avg3 = 0.545
accuracy[45].tokens_per_word = 1.4326889886089058
accuracy[46].model = "sarvam-1"
accuracy[46].task = "xnli"
accuracy[46].form = "itrans"
accuracy[46].n = 200
accuracy[46].chance = 0.3333333333333333
accuracy[46].acc_cal = 0.385
accuracy[46].acc_cal_ci_low = 0.32
accuracy[46].acc_cal_ci_high = 0.455
accuracy[46].constant_label_rate_cal = 0.795
accuracy[46].acc_raw = 0.385
accuracy[46].acc_raw_ci_low = 0.32
accuracy[46].acc_raw_ci_high = 0.455
accuracy[46].constant_label_rate_raw = 0.8
accuracy[46].acc_na = 0.37
accuracy[46].acc_na_ci_low = 0.3
accuracy[46].acc_na_ci_high = 0.44
accuracy[46].constant_label_rate_na = 0.865
accuracy[46].acc_avg3 = 0.385
accuracy[46].acc_avg3_ci_low = 0.32
accuracy[46].acc_avg3_ci_high = 0.455
accuracy[46].constant_label_rate_avg3 = 0.795
accuracy[46].tokens_per_word = 5.226255594231725
accuracy[47].model = "sarvam-1"
accuracy[47].task = "xnli"
accuracy[47].form = "lossy"
accuracy[47].n = 200
accuracy[47].chance = 0.3333333333333333
accuracy[47].acc_cal = 0.47
accuracy[47].acc_cal_ci_low = 0.4
accuracy[47].acc_cal_ci_high = 0.54
accuracy[47].constant_label_rate_cal = 0.58
accuracy[47].acc_raw = 0.46
accuracy[47].acc_raw_ci_low = 0.39
accuracy[47].acc_raw_ci_high = 0.53
accuracy[47].constant_label_rate_raw = 0.595
accuracy[47].acc_na = 0.375
accuracy[47].acc_na_ci_low = 0.31
accuracy[47].acc_na_ci_high = 0.44
accuracy[47].constant_label_rate_na = 0.905
accuracy[47].acc_avg3 = 0.47
accuracy[47].acc_avg3_ci_low = 0.4
accuracy[47].acc_avg3_ci_high = 0.54
accuracy[47].constant_label_rate_avg3 = 0.58
accuracy[47].tokens_per_word = 4.335405271009448
accuracy[48].model = "sarvam-1"
accuracy[48].task = "xnli"
accuracy[48].form = "native"
accuracy[48].n = 200
accuracy[48].chance = 0.3333333333333333
accuracy[48].acc_cal = 0.515
accuracy[48].acc_cal_ci_low = 0.445
accuracy[48].acc_cal_ci_high = 0.585
accuracy[48].constant_label_rate_cal = 0.6
accuracy[48].acc_raw = 0.52
accuracy[48].acc_raw_ci_low = 0.45
accuracy[48].acc_raw_ci_high = 0.59
accuracy[48].constant_label_rate_raw = 0.61
accuracy[48].acc_na = 0.455
accuracy[48].acc_na_ci_low = 0.385
accuracy[48].acc_na_ci_high = 0.525
accuracy[48].constant_label_rate_na = 0.865
accuracy[48].acc_avg3 = 0.515
accuracy[48].acc_avg3_ci_low = 0.445
accuracy[48].acc_avg3_ci_high = 0.585
accuracy[48].constant_label_rate_avg3 = 0.6
accuracy[48].tokens_per_word = 2.1452013923421185
accuracy[49].model = "sarvam-1"
accuracy[49].task = "xnli"
accuracy[49].form = "natural"
accuracy[49].n = 193
accuracy[49].chance = 0.3333333333333333
accuracy[49].acc_cal = 0.46632124352331605
accuracy[49].acc_cal_ci_low = 0.39378238341968913
accuracy[49].acc_cal_ci_high = 0.533678756476684
accuracy[49].constant_label_rate_cal = 0.5958549222797928
accuracy[49].acc_raw = 0.46632124352331605
accuracy[49].acc_raw_ci_low = 0.39378238341968913
accuracy[49].acc_raw_ci_high = 0.533678756476684
accuracy[49].constant_label_rate_raw = 0.6113989637305699
accuracy[49].acc_na = 0.34196891191709844
accuracy[49].acc_na_ci_low = 0.27461139896373055
accuracy[49].acc_na_ci_high = 0.40932642487046633
accuracy[49].constant_label_rate_na = 0.9222797927461139
accuracy[49].acc_avg3 = 0.46632124352331605
accuracy[49].acc_avg3_ci_low = 0.39378238341968913
accuracy[49].acc_avg3_ci_high = 0.533678756476684
accuracy[49].constant_label_rate_avg3 = 0.5958549222797928
accuracy[49].tokens_per_word = 4.323750323750324
mcnemar[0].model = "gemma4-e2b"
mcnemar[0].task = "sentiment"
mcnemar[0].a = "natural"
mcnemar[0].b = "native"
mcnemar[0].acc_a = 0.803030303030303
mcnemar[0].acc_b = 0.9848484848484849
mcnemar[0].n = 198
mcnemar[0].diff = -0.18181818181818188
mcnemar[0].a_only = 2
mcnemar[0].b_only = 38
mcnemar[0].p = 1.4933903003111482e-09
mcnemar[0].p_holm = 4.33083187090233e-08
mcnemar[0].significant = true
mcnemar[1].model = "gemma4-e2b"
mcnemar[1].task = "sentiment"
mcnemar[1].a = "natural"
mcnemar[1].b = "itrans"
mcnemar[1].acc_a = 0.803030303030303
mcnemar[1].acc_b = 0.7575757575757576
mcnemar[1].n = 198
mcnemar[1].diff = 0.045454545454545414
mcnemar[1].a_only = 16
mcnemar[1].b_only = 7
mcnemar[1].p = 0.0931396484375
mcnemar[1].p_holm = 1.0
mcnemar[1].significant = false
mcnemar[2].model = "gemma4-e2b"
mcnemar[2].task = "sentiment"
mcnemar[2].a = "lossy"
mcnemar[2].b = "itrans"
mcnemar[2].acc_a = 0.79
mcnemar[2].acc_b = 0.755
mcnemar[2].n = 200
mcnemar[2].diff = 0.03500000000000003
mcnemar[2].a_only = 18
mcnemar[2].b_only = 11
mcnemar[2].p = 0.26493089646101
mcnemar[2].p_holm = 1.0
mcnemar[2].significant = false
mcnemar[3].model = "gemma4-e2b"
mcnemar[3].task = "xnli"
mcnemar[3].a = "natural"
mcnemar[3].b = "native"
mcnemar[3].acc_a = 0.40414507772020725
mcnemar[3].acc_b = 0.538860103626943
mcnemar[3].n = 193
mcnemar[3].diff = -0.13471502590673579
mcnemar[3].a_only = 11
mcnemar[3].b_only = 37
mcnemar[3].p = 0.0002222449626216872
mcnemar[3].p_holm = 0.005778369028163867
mcnemar[3].significant = true
mcnemar[4].model = "gemma4-e2b"
mcnemar[4].task = "xnli"
mcnemar[4].a = "natural"
mcnemar[4].b = "itrans"
mcnemar[4].acc_a = 0.40414507772020725
mcnemar[4].acc_b = 0.41450777202072536
mcnemar[4].n = 193
mcnemar[4].diff = -0.010362694300518116
mcnemar[4].a_only = 11
mcnemar[4].b_only = 13
mcnemar[4].p = 0.8388197422027588
mcnemar[4].p_holm = 1.0
mcnemar[4].significant = false
mcnemar[5].model = "gemma4-e2b"
mcnemar[5].task = "xnli"
mcnemar[5].a = "lossy"
mcnemar[5].b = "itrans"
mcnemar[5].acc_a = 0.4
mcnemar[5].acc_b = 0.41
mcnemar[5].n = 200
mcnemar[5].diff = -0.009999999999999953
mcnemar[5].a_only = 11
mcnemar[5].b_only = 13
mcnemar[5].p = 0.8388197422027588
mcnemar[5].p_holm = 1.0
mcnemar[5].significant = false
mcnemar[6].model = "qwen2.5-1.5b"
mcnemar[6].task = "sentiment"
mcnemar[6].a = "natural"
mcnemar[6].b = "native"
mcnemar[6].acc_a = 0.5151515151515151
mcnemar[6].acc_b = 0.702020202020202
mcnemar[6].n = 198
mcnemar[6].diff = -0.18686868686868685
mcnemar[6].a_only = 20
mcnemar[6].b_only = 57
mcnemar[6].p = 2.926311069930838e-05
mcnemar[6].p_holm = 0.0008193670995806346
mcnemar[6].significant = true
mcnemar[7].model = "qwen2.5-1.5b"
mcnemar[7].task = "sentiment"
mcnemar[7].a = "natural"
mcnemar[7].b = "itrans"
mcnemar[7].acc_a = 0.5151515151515151
mcnemar[7].acc_b = 0.4898989898989899
mcnemar[7].n = 198
mcnemar[7].diff = 0.02525252525252525
mcnemar[7].a_only = 6
mcnemar[7].b_only = 1
mcnemar[7].p = 0.125
mcnemar[7].p_holm = 1.0
mcnemar[7].significant = false
mcnemar[8].model = "qwen2.5-1.5b"
mcnemar[8].task = "sentiment"
mcnemar[8].a = "lossy"
mcnemar[8].b = "itrans"
mcnemar[8].acc_a = 0.5
mcnemar[8].acc_b = 0.495
mcnemar[8].n = 200
mcnemar[8].diff = 0.0050000000000000044
mcnemar[8].a_only = 4
mcnemar[8].b_only = 3
mcnemar[8].p = 1.0
mcnemar[8].p_holm = 1.0
mcnemar[8].significant = false
mcnemar[9].model = "qwen2.5-1.5b"
mcnemar[9].task = "xnli"
mcnemar[9].a = "natural"
mcnemar[9].b = "native"
mcnemar[9].acc_a = 0.32124352331606215
mcnemar[9].acc_b = 0.40414507772020725
mcnemar[9].n = 193
mcnemar[9].diff = -0.0829015544041451
mcnemar[9].a_only = 16
mcnemar[9].b_only = 32
mcnemar[9].p = 0.029304946720529308
mcnemar[9].p_holm = 0.5860989344105861
mcnemar[9].significant = false
mcnemar[10].model = "qwen2.5-1.5b"
mcnemar[10].task = "xnli"
mcnemar[10].a = "natural"
mcnemar[10].b = "itrans"
mcnemar[10].acc_a = 0.32124352331606215
mcnemar[10].acc_b = 0.32124352331606215
mcnemar[10].n = 193
mcnemar[10].diff = 0.0
mcnemar[10].a_only = 15
mcnemar[10].b_only = 15
mcnemar[10].p = 1.0
mcnemar[10].p_holm = 1.0
mcnemar[10].significant = false
mcnemar[11].model = "qwen2.5-1.5b"
mcnemar[11].task = "xnli"
mcnemar[11].a = "lossy"
mcnemar[11].b = "itrans"
mcnemar[11].acc_a = 0.325
mcnemar[11].acc_b = 0.32
mcnemar[11].n = 200
mcnemar[11].diff = 0.0050000000000000044
mcnemar[11].a_only = 18
mcnemar[11].b_only = 17
mcnemar[11].p = 0.9999999999999998
mcnemar[11].p_holm = 1.0
mcnemar[11].significant = false
mcnemar[12].model = "qwen3-1.7b"
mcnemar[12].task = "sentiment"
mcnemar[12].a = "natural"
mcnemar[12].b = "native"
mcnemar[12].acc_a = 0.5606060606060606
mcnemar[12].acc_b = 0.8333333333333334
mcnemar[12].n = 198
mcnemar[12].diff = -0.2727272727272728
mcnemar[12].a_only = 14
mcnemar[12].b_only = 68
mcnemar[12].p = 1.1349339471612945e-09
mcnemar[12].p_holm = 3.4048018414838833e-08
mcnemar[12].significant = true
mcnemar[13].model = "qwen3-1.7b"
mcnemar[13].task = "sentiment"
mcnemar[13].a = "natural"
mcnemar[13].b = "itrans"
mcnemar[13].acc_a = 0.5606060606060606
mcnemar[13].acc_b = 0.5303030303030303
mcnemar[13].n = 198
mcnemar[13].diff = 0.030303030303030276
mcnemar[13].a_only = 30
mcnemar[13].b_only = 24
mcnemar[13].p = 0.49661743531793345
mcnemar[13].p_holm = 1.0
mcnemar[13].significant = false
mcnemar[14].model = "qwen3-1.7b"
mcnemar[14].task = "sentiment"
mcnemar[14].a = "lossy"
mcnemar[14].b = "itrans"
mcnemar[14].acc_a = 0.57
mcnemar[14].acc_b = 0.535
mcnemar[14].n = 200
mcnemar[14].diff = 0.03499999999999992
mcnemar[14].a_only = 32
mcnemar[14].b_only = 25
mcnemar[14].p = 0.42704285650325524
mcnemar[14].p_holm = 1.0
mcnemar[14].significant = false
mcnemar[15].model = "qwen3-1.7b"
mcnemar[15].task = "xnli"
mcnemar[15].a = "natural"
mcnemar[15].b = "native"
mcnemar[15].acc_a = 0.34196891191709844
mcnemar[15].acc_b = 0.44559585492227977
mcnemar[15].n = 193
mcnemar[15].diff = -0.10362694300518133
mcnemar[15].a_only = 3
mcnemar[15].b_only = 23
mcnemar[15].p = 8.797645568847656e-05
mcnemar[15].p_holm = 0.002375364303588867
mcnemar[15].significant = true
mcnemar[16].model = "qwen3-1.7b"
mcnemar[16].task = "xnli"
mcnemar[16].a = "natural"
mcnemar[16].b = "itrans"
mcnemar[16].acc_a = 0.34196891191709844
mcnemar[16].acc_b = 0.33678756476683935
mcnemar[16].n = 193
mcnemar[16].diff = 0.005181347150259086
mcnemar[16].a_only = 1
mcnemar[16].b_only = 0
mcnemar[16].p = 1.0
mcnemar[16].p_holm = 1.0
mcnemar[16].significant = false
mcnemar[17].model = "qwen3-1.7b"
mcnemar[17].task = "xnli"
mcnemar[17].a = "lossy"
mcnemar[17].b = "itrans"
mcnemar[17].acc_a = 0.335
mcnemar[17].acc_b = 0.335
mcnemar[17].n = 200
mcnemar[17].diff = 0.0
mcnemar[17].a_only = 0
mcnemar[17].b_only = 0
mcnemar[17].p = 1.0
mcnemar[17].p_holm = 1.0
mcnemar[17].significant = false
mcnemar[18].model = "qwen3.5-2b"
mcnemar[18].task = "sentiment"
mcnemar[18].a = "natural"
mcnemar[18].b = "native"
mcnemar[18].acc_a = 0.7222222222222222
mcnemar[18].acc_b = 0.7373737373737373
mcnemar[18].n = 198
mcnemar[18].diff = -0.015151515151515138
mcnemar[18].a_only = 26
mcnemar[18].b_only = 29
mcnemar[18].p = 0.7877061896700431
mcnemar[18].p_holm = 1.0
mcnemar[18].significant = false
mcnemar[19].model = "qwen3.5-2b"
mcnemar[19].task = "sentiment"
mcnemar[19].a = "natural"
mcnemar[19].b = "itrans"
mcnemar[19].acc_a = 0.7222222222222222
mcnemar[19].acc_b = 0.6565656565656566
mcnemar[19].n = 198
mcnemar[19].diff = 0.06565656565656564
mcnemar[19].a_only = 29
mcnemar[19].b_only = 16
mcnemar[19].p = 0.07245426016254441
mcnemar[19].p_holm = 1.0
mcnemar[19].significant = false
mcnemar[20].model = "qwen3.5-2b"
mcnemar[20].task = "sentiment"
mcnemar[20].a = "lossy"
mcnemar[20].b = "itrans"
mcnemar[20].acc_a = 0.68
mcnemar[20].acc_b = 0.655
mcnemar[20].n = 200
mcnemar[20].diff = 0.025000000000000022
mcnemar[20].a_only = 23
mcnemar[20].b_only = 18
mcnemar[20].p = 0.5327092552361137
mcnemar[20].p_holm = 1.0
mcnemar[20].significant = false
mcnemar[21].model = "qwen3.5-2b"
mcnemar[21].task = "xnli"
mcnemar[21].a = "natural"
mcnemar[21].b = "native"
mcnemar[21].acc_a = 0.34196891191709844
mcnemar[21].acc_b = 0.34196891191709844
mcnemar[21].n = 193
mcnemar[21].diff = 0.0
mcnemar[21].a_only = 0
mcnemar[21].b_only = 0
mcnemar[21].p = 1.0
mcnemar[21].p_holm = 1.0
mcnemar[21].significant = false
mcnemar[22].model = "qwen3.5-2b"
mcnemar[22].task = "xnli"
mcnemar[22].a = "natural"
mcnemar[22].b = "itrans"
mcnemar[22].acc_a = 0.34196891191709844
mcnemar[22].acc_b = 0.34196891191709844
mcnemar[22].n = 193
mcnemar[22].diff = 0.0
mcnemar[22].a_only = 0
mcnemar[22].b_only = 0
mcnemar[22].p = 1.0
mcnemar[22].p_holm = 1.0
mcnemar[22].significant = false
mcnemar[23].model = "qwen3.5-2b"
mcnemar[23].task = "xnli"
mcnemar[23].a = "lossy"
mcnemar[23].b = "itrans"
mcnemar[23].acc_a = 0.335
mcnemar[23].acc_b = 0.34
mcnemar[23].n = 200
mcnemar[23].diff = -0.0050000000000000044
mcnemar[23].a_only = 0
mcnemar[23].b_only = 1
mcnemar[23].p = 1.0
mcnemar[23].p_holm = 1.0
mcnemar[23].significant = false
mcnemar[24].model = "sarvam-1"
mcnemar[24].task = "sentiment"
mcnemar[24].a = "natural"
mcnemar[24].b = "native"
mcnemar[24].acc_a = 0.8939393939393939
mcnemar[24].acc_b = 0.9545454545454546
mcnemar[24].n = 198
mcnemar[24].diff = -0.06060606060606066
mcnemar[24].a_only = 5
mcnemar[24].b_only = 17
mcnemar[24].p = 0.01690053939819336
mcnemar[24].p_holm = 0.38871240615844727
mcnemar[24].significant = false
mcnemar[25].model = "sarvam-1"
mcnemar[25].task = "sentiment"
mcnemar[25].a = "natural"
mcnemar[25].b = "itrans"
mcnemar[25].acc_a = 0.8939393939393939
mcnemar[25].acc_b = 0.8181818181818182
mcnemar[25].n = 198
mcnemar[25].diff = 0.07575757575757569
mcnemar[25].a_only = 27
mcnemar[25].b_only = 12
mcnemar[25].p = 0.023702702470473014
mcnemar[25].p_holm = 0.4977567518799333
mcnemar[25].significant = false
mcnemar[26].model = "sarvam-1"
mcnemar[26].task = "sentiment"
mcnemar[26].a = "lossy"
mcnemar[26].b = "itrans"
mcnemar[26].acc_a = 0.895
mcnemar[26].acc_b = 0.82
mcnemar[26].n = 200
mcnemar[26].diff = 0.07500000000000007
mcnemar[26].a_only = 21
mcnemar[26].b_only = 6
mcnemar[26].p = 0.005924612283706665
mcnemar[26].p_holm = 0.14811530709266663
mcnemar[26].significant = false
mcnemar[27].model = "sarvam-1"
mcnemar[27].task = "xnli"
mcnemar[27].a = "natural"
mcnemar[27].b = "native"
mcnemar[27].acc_a = 0.46632124352331605
mcnemar[27].acc_b = 0.5129533678756477
mcnemar[27].n = 193
mcnemar[27].diff = -0.04663212435233166
mcnemar[27].a_only = 14
mcnemar[27].b_only = 23
mcnemar[27].p = 0.18774155899882317
mcnemar[27].p_holm = 1.0
mcnemar[27].significant = false
mcnemar[28].model = "sarvam-1"
mcnemar[28].task = "xnli"
mcnemar[28].a = "natural"
mcnemar[28].b = "itrans"
mcnemar[28].acc_a = 0.46632124352331605
mcnemar[28].acc_b = 0.39378238341968913
mcnemar[28].n = 193
mcnemar[28].diff = 0.07253886010362692
mcnemar[28].a_only = 23
mcnemar[28].b_only = 9
mcnemar[28].p = 0.020061607006937265
mcnemar[28].p_holm = 0.44135535415261984
mcnemar[28].significant = false
mcnemar[29].model = "sarvam-1"
mcnemar[29].task = "xnli"
mcnemar[29].a = "lossy"
mcnemar[29].b = "itrans"
mcnemar[29].acc_a = 0.47
mcnemar[29].acc_b = 0.385
mcnemar[29].n = 200
mcnemar[29].diff = 0.08499999999999996
mcnemar[29].a_only = 29
mcnemar[29].b_only = 12
mcnemar[29].p = 0.011507789735333063
mcnemar[29].p_holm = 0.2761869536479935
mcnemar[29].significant = false
mcnemar_exploratory[0].model = "gemma4-e2b"
mcnemar_exploratory[0].task = "sentiment"
mcnemar_exploratory[0].a = "itrans"
mcnemar_exploratory[0].b = "native"
mcnemar_exploratory[0].acc_a = 0.755
mcnemar_exploratory[0].acc_b = 0.985
mcnemar_exploratory[0].n = 200
mcnemar_exploratory[0].diff = -0.22999999999999998
mcnemar_exploratory[0].a_only = 1
mcnemar_exploratory[0].b_only = 47
mcnemar_exploratory[0].p = 3.481659405224491e-13
mcnemar_exploratory[0].p_holm = 3.481659405224491e-12
mcnemar_exploratory[0].significant = true
mcnemar_exploratory[1].model = "gemma4-e2b"
mcnemar_exploratory[1].task = "xnli"
mcnemar_exploratory[1].a = "itrans"
mcnemar_exploratory[1].b = "native"
mcnemar_exploratory[1].acc_a = 0.41
mcnemar_exploratory[1].acc_b = 0.545
mcnemar_exploratory[1].n = 200
mcnemar_exploratory[1].diff = -0.13500000000000006
mcnemar_exploratory[1].a_only = 14
mcnemar_exploratory[1].b_only = 41
mcnemar_exploratory[1].p = 0.00035528111863147854
mcnemar_exploratory[1].p_holm = 0.0017764055931573928
mcnemar_exploratory[1].significant = true
mcnemar_exploratory[2].model = "qwen2.5-1.5b"
mcnemar_exploratory[2].task = "sentiment"
mcnemar_exploratory[2].a = "itrans"
mcnemar_exploratory[2].b = "native"
mcnemar_exploratory[2].acc_a = 0.495
mcnemar_exploratory[2].acc_b = 0.705
mcnemar_exploratory[2].n = 200
mcnemar_exploratory[2].diff = -0.20999999999999996
mcnemar_exploratory[2].a_only = 16
mcnemar_exploratory[2].b_only = 58
mcnemar_exploratory[2].p = 9.674891137601897e-07
mcnemar_exploratory[2].p_holm = 7.739912910081517e-06
mcnemar_exploratory[2].significant = true
mcnemar_exploratory[3].model = "qwen2.5-1.5b"
mcnemar_exploratory[3].task = "xnli"
mcnemar_exploratory[3].a = "itrans"
mcnemar_exploratory[3].b = "native"
mcnemar_exploratory[3].acc_a = 0.32
mcnemar_exploratory[3].acc_b = 0.4
mcnemar_exploratory[3].n = 200
mcnemar_exploratory[3].diff = -0.08000000000000002
mcnemar_exploratory[3].a_only = 18
mcnemar_exploratory[3].b_only = 34
mcnemar_exploratory[3].p = 0.03648340000835981
mcnemar_exploratory[3].p_holm = 0.07768824537970431
mcnemar_exploratory[3].significant = false
mcnemar_exploratory[4].model = "qwen3-1.7b"
mcnemar_exploratory[4].task = "sentiment"
mcnemar_exploratory[4].a = "itrans"
mcnemar_exploratory[4].b = "native"
mcnemar_exploratory[4].acc_a = 0.535
mcnemar_exploratory[4].acc_b = 0.835
mcnemar_exploratory[4].n = 200
mcnemar_exploratory[4].diff = -0.29999999999999993
mcnemar_exploratory[4].a_only = 14
mcnemar_exploratory[4].b_only = 74
mcnemar_exploratory[4].p = 5.0891941127085865e-11
mcnemar_exploratory[4].p_holm = 4.580274701437728e-10
mcnemar_exploratory[4].significant = true
mcnemar_exploratory[5].model = "qwen3-1.7b"
mcnemar_exploratory[5].task = "xnli"
mcnemar_exploratory[5].a = "itrans"
mcnemar_exploratory[5].b = "native"
mcnemar_exploratory[5].acc_a = 0.335
mcnemar_exploratory[5].acc_b = 0.445
mcnemar_exploratory[5].n = 200
mcnemar_exploratory[5].diff = -0.10999999999999999
mcnemar_exploratory[5].a_only = 3
mcnemar_exploratory[5].b_only = 25
mcnemar_exploratory[5].p = 2.744048833847046e-05
mcnemar_exploratory[5].p_holm = 0.00016464293003082275
mcnemar_exploratory[5].significant = true
mcnemar_exploratory[6].model = "qwen3.5-2b"
mcnemar_exploratory[6].task = "sentiment"
mcnemar_exploratory[6].a = "itrans"
mcnemar_exploratory[6].b = "native"
mcnemar_exploratory[6].acc_a = 0.655
mcnemar_exploratory[6].acc_b = 0.735
mcnemar_exploratory[6].n = 200
mcnemar_exploratory[6].diff = -0.07999999999999996
mcnemar_exploratory[6].a_only = 15
mcnemar_exploratory[6].b_only = 31
mcnemar_exploratory[6].p = 0.02589608179323477
mcnemar_exploratory[6].p_holm = 0.07768824537970431
mcnemar_exploratory[6].significant = false
mcnemar_exploratory[7].model = "qwen3.5-2b"
mcnemar_exploratory[7].task = "xnli"
mcnemar_exploratory[7].a = "itrans"
mcnemar_exploratory[7].b = "native"
mcnemar_exploratory[7].acc_a = 0.34
mcnemar_exploratory[7].acc_b = 0.34
mcnemar_exploratory[7].n = 200
mcnemar_exploratory[7].diff = 0.0
mcnemar_exploratory[7].a_only = 0
mcnemar_exploratory[7].b_only = 0
mcnemar_exploratory[7].p = 1.0
mcnemar_exploratory[7].p_holm = 1.0
mcnemar_exploratory[7].significant = false
mcnemar_exploratory[8].model = "sarvam-1"
mcnemar_exploratory[8].task = "sentiment"
mcnemar_exploratory[8].a = "itrans"
mcnemar_exploratory[8].b = "native"
mcnemar_exploratory[8].acc_a = 0.82
mcnemar_exploratory[8].acc_b = 0.955
mcnemar_exploratory[8].n = 200
mcnemar_exploratory[8].diff = -0.135
mcnemar_exploratory[8].a_only = 6
mcnemar_exploratory[8].b_only = 33
mcnemar_exploratory[8].p = 1.429926123819314e-05
mcnemar_exploratory[8].p_holm = 0.00010009482866735198
mcnemar_exploratory[8].significant = true
mcnemar_exploratory[9].model = "sarvam-1"
mcnemar_exploratory[9].task = "xnli"
mcnemar_exploratory[9].a = "itrans"
mcnemar_exploratory[9].b = "native"
mcnemar_exploratory[9].acc_a = 0.385
mcnemar_exploratory[9].acc_b = 0.515
mcnemar_exploratory[9].n = 200
mcnemar_exploratory[9].diff = -0.13
mcnemar_exploratory[9].a_only = 14
mcnemar_exploratory[9].b_only = 40
mcnemar_exploratory[9].p = 0.0005354355028570622
mcnemar_exploratory[9].p_holm = 0.002141742011428249
mcnemar_exploratory[9].significant = true
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.2469796341042458
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.231369150779896
fertility[2].model = "qwen2.5-1.5b"
fertility[2].task = "xnli"
fertility[2].form = "native"
fertility[2].n_texts = 400
fertility[2].tokens_per_word = 11.79860765788165
fertility[3].model = "qwen2.5-1.5b"
fertility[3].task = "sentiment"
fertility[3].form = "native"
fertility[3].n_texts = 200
fertility[3].tokens_per_word = 11.985638921453694
fertility[4].model = "qwen2.5-1.5b"
fertility[4].task = "xnli"
fertility[4].form = "itrans"
fertility[4].n_texts = 400
fertility[4].tokens_per_word = 4.25161611138737
fertility[5].model = "qwen2.5-1.5b"
fertility[5].task = "sentiment"
fertility[5].form = "itrans"
fertility[5].n_texts = 200
fertility[5].tokens_per_word = 4.22538100820633
fertility[6].model = "qwen2.5-1.5b"
fertility[6].task = "xnli"
fertility[6].form = "lossy"
fertility[6].n_texts = 400
fertility[6].tokens_per_word = 3.5532073595226255
fertility[7].model = "qwen2.5-1.5b"
fertility[7].task = "sentiment"
fertility[7].form = "lossy"
fertility[7].n_texts = 200
fertility[7].tokens_per_word = 3.5679953106682296
fertility[8].model = "qwen2.5-1.5b"
fertility[8].task = "xnli"
fertility[8].form = "natural"
fertility[8].n_texts = 386
fertility[8].tokens_per_word = 3.5423465423465426
fertility[9].model = "qwen2.5-1.5b"
fertility[9].task = "sentiment"
fertility[9].form = "natural"
fertility[9].n_texts = 198
fertility[9].tokens_per_word = 3.5069712251557403
fertility[10].model = "qwen3.5-2b"
fertility[10].task = "xnli"
fertility[10].form = "english"
fertility[10].n_texts = 400
fertility[10].tokens_per_word = 1.2424922333448394
fertility[11].model = "qwen3.5-2b"
fertility[11].task = "sentiment"
fertility[11].form = "english"
fertility[11].n_texts = 200
fertility[11].tokens_per_word = 1.2268197573656845
fertility[12].model = "qwen3.5-2b"
fertility[12].task = "xnli"
fertility[12].form = "native"
fertility[12].n_texts = 400
fertility[12].tokens_per_word = 5.230979612133267
fertility[13].model = "qwen3.5-2b"
fertility[13].task = "sentiment"
fertility[13].form = "native"
fertility[13].n_texts = 200
fertility[13].tokens_per_word = 5.235052754982415
fertility[14].model = "qwen3.5-2b"
fertility[14].task = "xnli"
fertility[14].form = "itrans"
fertility[14].n_texts = 400
fertility[14].tokens_per_word = 4.1282943809050225
fertility[15].model = "qwen3.5-2b"
fertility[15].task = "sentiment"
fertility[15].form = "itrans"
fertility[15].n_texts = 200
fertility[15].tokens_per_word = 4.087631887456038
fertility[16].model = "qwen3.5-2b"
fertility[16].task = "xnli"
fertility[16].form = "lossy"
fertility[16].n_texts = 400
fertility[16].tokens_per_word = 3.3431128791645945
fertility[17].model = "qwen3.5-2b"
fertility[17].task = "sentiment"
fertility[17].form = "lossy"
fertility[17].n_texts = 200
fertility[17].tokens_per_word = 3.3423212192262604
fertility[18].model = "qwen3.5-2b"
fertility[18].task = "xnli"
fertility[18].form = "natural"
fertility[18].n_texts = 386
fertility[18].tokens_per_word = 3.346283346283346
fertility[19].model = "qwen3.5-2b"
fertility[19].task = "sentiment"
fertility[19].form = "natural"
fertility[19].n_texts = 198
fertility[19].tokens_per_word = 3.32275289231682
fertility[20].model = "sarvam-1"
fertility[20].task = "xnli"
fertility[20].form = "english"
fertility[20].n_texts = 400
fertility[20].tokens_per_word = 1.4326889886089058
fertility[21].model = "sarvam-1"
fertility[21].task = "sentiment"
fertility[21].form = "english"
fertility[21].n_texts = 200
fertility[21].tokens_per_word = 1.4204939341421143
fertility[22].model = "sarvam-1"
fertility[22].task = "xnli"
fertility[22].form = "native"
fertility[22].n_texts = 400
fertility[22].tokens_per_word = 2.1452013923421185
fertility[23].model = "sarvam-1"
fertility[23].task = "sentiment"
fertility[23].form = "native"
fertility[23].n_texts = 200
fertility[23].tokens_per_word = 2.2708089097303636
fertility[24].model = "sarvam-1"
fertility[24].task = "xnli"
fertility[24].form = "itrans"
fertility[24].n_texts = 400
fertility[24].tokens_per_word = 5.226255594231725
fertility[25].model = "sarvam-1"
fertility[25].task = "sentiment"
fertility[25].form = "itrans"
fertility[25].n_texts = 200
fertility[25].tokens_per_word = 5.238569753810082
fertility[26].model = "sarvam-1"
fertility[26].task = "xnli"
fertility[26].form = "lossy"
fertility[26].n_texts = 400
fertility[26].tokens_per_word = 4.335405271009448
fertility[27].model = "sarvam-1"
fertility[27].task = "sentiment"
fertility[27].form = "lossy"
fertility[27].n_texts = 200
fertility[27].tokens_per_word = 4.357561547479484
fertility[28].model = "sarvam-1"
fertility[28].task = "xnli"
fertility[28].form = "natural"
fertility[28].n_texts = 386
fertility[28].tokens_per_word = 4.323750323750324
fertility[29].model = "sarvam-1"
fertility[29].task = "sentiment"
fertility[29].form = "natural"
fertility[29].n_texts = 198
fertility[29].tokens_per_word = 4.29219816078315
fertility[30].model = "gemma4-e2b"
fertility[30].task = "xnli"
fertility[30].form = "english"
fertility[30].n_texts = 400
fertility[30].tokens_per_word = 1.2397307559544357
fertility[31].model = "gemma4-e2b"
fertility[31].task = "sentiment"
fertility[31].form = "english"
fertility[31].n_texts = 200
fertility[31].tokens_per_word = 1.2214038128249567
fertility[32].model = "gemma4-e2b"
fertility[32].task = "xnli"
fertility[32].form = "native"
fertility[32].n_texts = 400
fertility[32].tokens_per_word = 3.1397314768771754
fertility[33].model = "gemma4-e2b"
fertility[33].task = "sentiment"
fertility[33].form = "native"
fertility[33].n_texts = 200
fertility[33].tokens_per_word = 3.0767878077373974
fertility[34].model = "gemma4-e2b"
fertility[34].task = "xnli"
fertility[34].form = "itrans"
fertility[34].n_texts = 400
fertility[34].tokens_per_word = 3.9604674291397313
fertility[35].model = "gemma4-e2b"
fertility[35].task = "sentiment"
fertility[35].form = "itrans"
fertility[35].n_texts = 200
fertility[35].tokens_per_word = 3.943434935521688
fertility[36].model = "gemma4-e2b"
fertility[36].task = "xnli"
fertility[36].form = "lossy"
fertility[36].n_texts = 400
fertility[36].tokens_per_word = 3.2031327697662855
fertility[37].model = "gemma4-e2b"
fertility[37].task = "sentiment"
fertility[37].form = "lossy"
fertility[37].n_texts = 200
fertility[37].tokens_per_word = 3.2110199296600235
fertility[38].model = "gemma4-e2b"
fertility[38].task = "xnli"
fertility[38].form = "natural"
fertility[38].n_texts = 386
fertility[38].tokens_per_word = 3.1711991711991714
fertility[39].model = "gemma4-e2b"
fertility[39].task = "sentiment"
fertility[39].form = "natural"
fertility[39].n_texts = 198
fertility[39].tokens_per_word = 3.1530703055473155
fertility[40].model = "qwen3-1.7b"
fertility[40].task = "xnli"
fertility[40].form = "english"
fertility[40].n_texts = 400
fertility[40].tokens_per_word = 1.2469796341042458
fertility[41].model = "qwen3-1.7b"
fertility[41].task = "sentiment"
fertility[41].form = "english"
fertility[41].n_texts = 200
fertility[41].tokens_per_word = 1.231369150779896
fertility[42].model = "qwen3-1.7b"
fertility[42].task = "xnli"
fertility[42].form = "native"
fertility[42].n_texts = 400
fertility[42].tokens_per_word = 11.79860765788165
fertility[43].model = "qwen3-1.7b"
fertility[43].task = "sentiment"
fertility[43].form = "native"
fertility[43].n_texts = 200
fertility[43].tokens_per_word = 11.985638921453694
fertility[44].model = "qwen3-1.7b"
fertility[44].task = "xnli"
fertility[44].form = "itrans"
fertility[44].n_texts = 400
fertility[44].tokens_per_word = 4.25161611138737
fertility[45].model = "qwen3-1.7b"
fertility[45].task = "sentiment"
fertility[45].form = "itrans"
fertility[45].n_texts = 200
fertility[45].tokens_per_word = 4.22538100820633
fertility[46].model = "qwen3-1.7b"
fertility[46].task = "xnli"
fertility[46].form = "lossy"
fertility[46].n_texts = 400
fertility[46].tokens_per_word = 3.5532073595226255
fertility[47].model = "qwen3-1.7b"
fertility[47].task = "sentiment"
fertility[47].form = "lossy"
fertility[47].n_texts = 200
fertility[47].tokens_per_word = 3.5679953106682296
fertility[48].model = "qwen3-1.7b"
fertility[48].task = "xnli"
fertility[48].form = "natural"
fertility[48].n_texts = 386
fertility[48].tokens_per_word = 3.5423465423465426
fertility[49].model = "qwen3-1.7b"
fertility[49].task = "sentiment"
fertility[49].form = "natural"
fertility[49].n_texts = 198
fertility[49].tokens_per_word = 3.5069712251557403
verdicts.informative_cells = ["gemma4-e2b/sentiment", "gemma4-e2b/xnli", "qwen2.5-1.5b/sentiment", "qwen2.5-1.5b/xnli", "qwen3-1.7b/sentiment", "qwen3-1.7b/xnli", "qwen3.5-2b/sentiment", "qwen3.5-2b/xnli", "sarvam-1/sentiment", "sarvam-1/xnli"]
verdicts.P3_lossy_lt_itrans = false
verdicts.P3_parts.all_cells_lossy_below_itrans = false
verdicts.P3_parts.fraction_significant = 0.0
verdicts.P3_parts.n_cells = 10
verdicts.P1_familiarity_dominates = false
verdicts.P2_fragmentation_also_matters = false
verdicts.P2_parts.qwen_natural_gt_native = false
verdicts.P2_parts.sarvam_natural_lt_native = false
`````

#### `results/e0b_familiarity/gate1/verdicts.json` (3,129 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

`````text
provenance.config.models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
provenance.config.forms = ["english", "native", "itrans", "lossy", "natural"]
provenance.config.calibration = "primary: mean of content-free N/A, '', [MASK]; raw fallback if English drops > 5 pts"
provenance.config.calibration_fallback_rows[0].model = "gemma4-e2b"
provenance.config.calibration_fallback_rows[0].task = "xnli"
provenance.config.calibration_fallback_rows[1].model = "qwen2.5-1.5b"
provenance.config.calibration_fallback_rows[1].task = "sentiment"
provenance.config.natural_items_excluded_defective = 9
provenance.config.templates = "e0_{xnli,sentiment}_v1"
provenance.config.n_per_task = 200
provenance.config.seed = 0
provenance.config.bos = "always prepended"
provenance.config.seconds_per_model_form.qwen2.5-1.5b/english = 36.487061977386475
provenance.config.seconds_per_model_form.qwen2.5-1.5b/native = 60.4139928817749
provenance.config.seconds_per_model_form.qwen2.5-1.5b/itrans = 46.802143573760986
provenance.config.seconds_per_model_form.qwen2.5-1.5b/lossy = 49.93747925758362
provenance.config.seconds_per_model_form.qwen2.5-1.5b/natural = 35.85534334182739
provenance.config.seconds_per_model_form.qwen3.5-2b/english = 100.45982670783997
provenance.config.seconds_per_model_form.qwen3.5-2b/native = 137.80759501457214
provenance.config.seconds_per_model_form.qwen3.5-2b/itrans = 135.9841856956482
provenance.config.seconds_per_model_form.qwen3.5-2b/lossy = 107.09859132766724
provenance.config.seconds_per_model_form.qwen3.5-2b/natural = 69.45307636260986
provenance.config.seconds_per_model_form.sarvam-1/english = 52.38592600822449
provenance.config.seconds_per_model_form.sarvam-1/native = 54.95457744598389
provenance.config.seconds_per_model_form.sarvam-1/itrans = 60.9882435798645
provenance.config.seconds_per_model_form.sarvam-1/lossy = 57.89579892158508
provenance.config.seconds_per_model_form.sarvam-1/natural = 44.358845472335815
provenance.config.seconds_per_model_form.gemma4-e2b/english = 89.42716455459595
provenance.config.seconds_per_model_form.gemma4-e2b/native = 94.79906296730042
provenance.config.seconds_per_model_form.gemma4-e2b/itrans = 97.28406596183777
provenance.config.seconds_per_model_form.gemma4-e2b/lossy = 92.6928346157074
provenance.config.seconds_per_model_form.gemma4-e2b/natural = 81.26459240913391
provenance.config.seconds_per_model_form.qwen3-1.7b/english = 43.18634009361267
provenance.config.seconds_per_model_form.qwen3-1.7b/native = 65.9120557308197
provenance.config.seconds_per_model_form.qwen3-1.7b/itrans = 52.16321563720703
provenance.config.seconds_per_model_form.qwen3-1.7b/lossy = 49.83175706863403
provenance.config.seconds_per_model_form.qwen3-1.7b/natural = 41.86442446708679
provenance.git_commit = "42f52d1866b427f6415cac2f4f04a5eb52024670-dirty"
provenance.timestamp_utc = "2026-10-15T11:09:28+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0b_familiarity.py", "--models", "qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b", "--tag", "gate1"]
informative_cells = ["gemma4-e2b/sentiment", "gemma4-e2b/xnli", "qwen2.5-1.5b/sentiment", "qwen2.5-1.5b/xnli", "qwen3-1.7b/sentiment", "qwen3-1.7b/xnli", "qwen3.5-2b/sentiment", "qwen3.5-2b/xnli", "sarvam-1/sentiment", "sarvam-1/xnli"]
P3_lossy_lt_itrans = false
P3_parts.all_cells_lossy_below_itrans = false
P3_parts.fraction_significant = 0.0
P3_parts.n_cells = 10
P1_familiarity_dominates = false
P2_fragmentation_also_matters = false
P2_parts.qwen_natural_gt_native = false
P2_parts.sarvam_natural_lt_native = false
`````

#### `results/e0b_familiarity/gate1a/accuracy.csv` (4,322 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

| model | task | form | n | chance | acc_cal | acc_cal_ci_low | acc_cal_ci_high | constant_label_rate_cal | acc_raw | acc_raw_ci_low | acc_raw_ci_high | constant_label_rate_raw | tokens_per_word |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 1.2214038128249567 |
| gemma4-e2b | sentiment | itrans | 200 | 0.5 | 0.765 | 0.705 | 0.82 | 0.615 | 0.75 | 0.69 | 0.81 | 0.67 | 3.943434935521688 |
| gemma4-e2b | sentiment | lossy | 200 | 0.5 | 0.785 | 0.725 | 0.84 | 0.625 | 0.79 | 0.73 | 0.845 | 0.65 | 3.2110199296600235 |
| gemma4-e2b | sentiment | native | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 3.0767878077373974 |
| gemma4-e2b | xnli | english | 200 | 0.3333333333333333 | 0.6 | 0.53 | 0.67 | 0.56 | 0.735 | 0.675 | 0.795 | 0.405 | 1.2397307559544357 |
| gemma4-e2b | xnli | itrans | 200 | 0.3333333333333333 | 0.435 | 0.365 | 0.505 | 0.6 | 0.41 | 0.34 | 0.48 | 0.87 | 3.9604674291397313 |
| gemma4-e2b | xnli | lossy | 200 | 0.3333333333333333 | 0.395 | 0.33 | 0.46 | 0.78 | 0.4 | 0.335 | 0.47 | 0.84 | 3.2031327697662855 |
| gemma4-e2b | xnli | native | 200 | 0.3333333333333333 | 0.465 | 0.395 | 0.535 | 0.615 | 0.545 | 0.475 | 0.615 | 0.595 | 3.1397314768771754 |
| qwen2.5-1.5b | sentiment | english | 200 | 0.5 | 0.52 | 0.45 | 0.59 | 0.98 | 0.985 | 0.965 | 1.0 | 0.515 | 1.231369150779896 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 0.5 | 0.5 | 0.43 | 0.57 | 1.0 | 0.495 | 0.425 | 0.565 | 0.995 | 4.22538100820633 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 0.5 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 0.97 | 3.5679953106682296 |
| qwen2.5-1.5b | sentiment | native | 200 | 0.5 | 0.505 | 0.435 | 0.575 | 0.995 | 0.705 | 0.64 | 0.765 | 0.625 | 11.985638921453694 |
| qwen2.5-1.5b | xnli | english | 200 | 0.3333333333333333 | 0.785 | 0.73 | 0.84 | 0.49 | 0.795 | 0.735 | 0.85 | 0.45 | 1.2469796341042458 |
| qwen2.5-1.5b | xnli | itrans | 200 | 0.3333333333333333 | 0.325 | 0.26 | 0.39 | 0.965 | 0.375 | 0.31 | 0.445 | 0.845 | 4.25161611138737 |
| qwen2.5-1.5b | xnli | lossy | 200 | 0.3333333333333333 | 0.33 | 0.265 | 0.395 | 0.955 | 0.375 | 0.31 | 0.445 | 0.84 | 3.5532073595226255 |
| qwen2.5-1.5b | xnli | native | 200 | 0.3333333333333333 | 0.345 | 0.28 | 0.41 | 0.965 | 0.51 | 0.445 | 0.58 | 0.48 | 11.79860765788165 |
| qwen3-1.7b | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 1.231369150779896 |
| qwen3-1.7b | sentiment | itrans | 200 | 0.5 | 0.54 | 0.47 | 0.61 | 0.85 | 0.58 | 0.51 | 0.645 | 0.68 | 4.22538100820633 |
| qwen3-1.7b | sentiment | lossy | 200 | 0.5 | 0.52 | 0.45 | 0.59 | 0.91 | 0.575 | 0.505 | 0.64 | 0.715 | 3.5679953106682296 |
| qwen3-1.7b | sentiment | native | 200 | 0.5 | 0.79 | 0.73 | 0.845 | 0.68 | 0.865 | 0.815 | 0.91 | 0.525 | 11.985638921453694 |
| qwen3-1.7b | xnli | english | 200 | 0.3333333333333333 | 0.54 | 0.47 | 0.61 | 0.765 | 0.615 | 0.545 | 0.68 | 0.53 | 1.2469796341042458 |
| qwen3-1.7b | xnli | itrans | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.37 | 0.305 | 0.44 | 0.8 | 4.25161611138737 |
| qwen3-1.7b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.415 | 0.345 | 0.485 | 0.795 | 3.5532073595226255 |
| qwen3-1.7b | xnli | native | 200 | 0.3333333333333333 | 0.425 | 0.355 | 0.495 | 0.89 | 0.43 | 0.36 | 0.5 | 0.61 | 11.79860765788165 |
| qwen3.5-2b | sentiment | english | 200 | 0.5 | 0.975 | 0.95 | 0.995 | 0.525 | 0.975 | 0.95 | 0.995 | 0.505 | 1.2268197573656845 |
| qwen3.5-2b | sentiment | itrans | 200 | 0.5 | 0.615 | 0.545 | 0.685 | 0.855 | 0.675 | 0.61 | 0.74 | 0.665 | 4.087631887456038 |
| qwen3.5-2b | sentiment | lossy | 200 | 0.5 | 0.645 | 0.58 | 0.71 | 0.815 | 0.675 | 0.61 | 0.735 | 0.645 | 3.3423212192262604 |
| qwen3.5-2b | sentiment | native | 200 | 0.5 | 0.675 | 0.61 | 0.74 | 0.815 | 0.785 | 0.725 | 0.84 | 0.705 | 5.235052754982415 |
| qwen3.5-2b | xnli | english | 200 | 0.3333333333333333 | 0.45 | 0.38 | 0.52 | 0.845 | 0.43 | 0.36 | 0.5 | 0.89 | 1.2424922333448394 |
| qwen3.5-2b | xnli | itrans | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 4.1282943809050225 |
| qwen3.5-2b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.99 | 0.34 | 0.275 | 0.405 | 0.995 | 3.3431128791645945 |
| qwen3.5-2b | xnli | native | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 5.230979612133267 |
| sarvam-1 | sentiment | english | 200 | 0.5 | 0.975 | 0.95 | 0.995 | 0.515 | 0.975 | 0.95 | 0.995 | 0.505 | 1.4204939341421143 |
| sarvam-1 | sentiment | itrans | 200 | 0.5 | 0.78 | 0.72 | 0.835 | 0.69 | 0.845 | 0.795 | 0.895 | 0.515 | 5.238569753810082 |
| sarvam-1 | sentiment | lossy | 200 | 0.5 | 0.86 | 0.81 | 0.905 | 0.63 | 0.91 | 0.87 | 0.95 | 0.51 | 4.357561547479484 |
| sarvam-1 | sentiment | native | 200 | 0.5 | 0.96 | 0.93 | 0.985 | 0.51 | 0.96 | 0.93 | 0.985 | 0.53 | 2.2708089097303636 |
| sarvam-1 | xnli | english | 200 | 0.3333333333333333 | 0.475 | 0.405 | 0.545 | 0.655 | 0.53 | 0.46 | 0.6 | 0.63 | 1.4326889886089058 |
| sarvam-1 | xnli | itrans | 200 | 0.3333333333333333 | 0.37 | 0.3 | 0.44 | 0.865 | 0.385 | 0.32 | 0.455 | 0.8 | 5.226255594231725 |
| sarvam-1 | xnli | lossy | 200 | 0.3333333333333333 | 0.375 | 0.31 | 0.44 | 0.905 | 0.46 | 0.39 | 0.53 | 0.595 | 4.335405271009448 |
| sarvam-1 | xnli | native | 200 | 0.3333333333333333 | 0.455 | 0.385 | 0.525 | 0.865 | 0.52 | 0.45 | 0.59 | 0.61 | 2.1452013923421185 |

#### `results/e0b_familiarity/gate1a/fertility.csv` (2,001 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

| model | task | form | n_texts | tokens_per_word |
|---|---|---|---|---|
| qwen2.5-1.5b | xnli | english | 400 | 1.2469796341042458 |
| qwen2.5-1.5b | sentiment | english | 200 | 1.231369150779896 |
| qwen2.5-1.5b | xnli | native | 400 | 11.79860765788165 |
| qwen2.5-1.5b | sentiment | native | 200 | 11.985638921453694 |
| qwen2.5-1.5b | xnli | itrans | 400 | 4.25161611138737 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen2.5-1.5b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen3.5-2b | xnli | english | 400 | 1.2424922333448394 |
| qwen3.5-2b | sentiment | english | 200 | 1.2268197573656845 |
| qwen3.5-2b | xnli | native | 400 | 5.230979612133267 |
| qwen3.5-2b | sentiment | native | 200 | 5.235052754982415 |
| qwen3.5-2b | xnli | itrans | 400 | 4.1282943809050225 |
| qwen3.5-2b | sentiment | itrans | 200 | 4.087631887456038 |
| qwen3.5-2b | xnli | lossy | 400 | 3.3431128791645945 |
| qwen3.5-2b | sentiment | lossy | 200 | 3.3423212192262604 |
| sarvam-1 | xnli | english | 400 | 1.4326889886089058 |
| sarvam-1 | sentiment | english | 200 | 1.4204939341421143 |
| sarvam-1 | xnli | native | 400 | 2.1452013923421185 |
| sarvam-1 | sentiment | native | 200 | 2.2708089097303636 |
| sarvam-1 | xnli | itrans | 400 | 5.226255594231725 |
| sarvam-1 | sentiment | itrans | 200 | 5.238569753810082 |
| sarvam-1 | xnli | lossy | 400 | 4.335405271009448 |
| sarvam-1 | sentiment | lossy | 200 | 4.357561547479484 |
| gemma4-e2b | xnli | english | 400 | 1.2397307559544357 |
| gemma4-e2b | sentiment | english | 200 | 1.2214038128249567 |
| gemma4-e2b | xnli | native | 400 | 3.1397314768771754 |
| gemma4-e2b | sentiment | native | 200 | 3.0767878077373974 |
| gemma4-e2b | xnli | itrans | 400 | 3.9604674291397313 |
| gemma4-e2b | sentiment | itrans | 200 | 3.943434935521688 |
| gemma4-e2b | xnli | lossy | 400 | 3.2031327697662855 |
| gemma4-e2b | sentiment | lossy | 200 | 3.2110199296600235 |
| qwen3-1.7b | xnli | english | 400 | 1.2469796341042458 |
| qwen3-1.7b | sentiment | english | 200 | 1.231369150779896 |
| qwen3-1.7b | xnli | native | 400 | 11.79860765788165 |
| qwen3-1.7b | sentiment | native | 200 | 11.985638921453694 |
| qwen3-1.7b | xnli | itrans | 400 | 4.25161611138737 |
| qwen3-1.7b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen3-1.7b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen3-1.7b | sentiment | lossy | 200 | 3.5679953106682296 |

#### `results/e0b_familiarity/gate1a/mcnemar.csv` (964 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

| model | task | a | b | acc_a | acc_b | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | lossy | itrans | 0.785 | 0.765 | 0.020000000000000018 | 19 | 15 | 0.6075913612730801 | 1.0 | False |
| gemma4-e2b | xnli | lossy | itrans | 0.395 | 0.435 | -0.03999999999999998 | 19 | 27 | 0.3019956131896606 | 1.0 | False |
| qwen2.5-1.5b | sentiment | lossy | itrans | 0.5 | 0.5 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| qwen2.5-1.5b | xnli | lossy | itrans | 0.33 | 0.325 | 0.0050000000000000044 | 4 | 3 | 1.0 | 1.0 | False |
| qwen3-1.7b | sentiment | lossy | itrans | 0.52 | 0.54 | -0.020000000000000018 | 14 | 18 | 0.5966148958541453 | 1.0 | False |
| qwen3-1.7b | xnli | lossy | itrans | 0.335 | 0.335 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| qwen3.5-2b | sentiment | lossy | itrans | 0.645 | 0.615 | 0.030000000000000027 | 22 | 16 | 0.417692190836533 | 1.0 | False |
| qwen3.5-2b | xnli | lossy | itrans | 0.335 | 0.34 | -0.0050000000000000044 | 0 | 1 | 1.0 | 1.0 | False |
| sarvam-1 | sentiment | lossy | itrans | 0.86 | 0.78 | 0.07999999999999996 | 25 | 9 | 0.00904118549078703 | 0.09041185490787029 | False |
| sarvam-1 | xnli | lossy | itrans | 0.375 | 0.37 | 0.0050000000000000044 | 12 | 11 | 1.0 | 1.0 | False |

#### `results/e0b_familiarity/gate1a/mcnemar_exploratory.csv` (1,114 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

| model | task | a | b | acc_a | acc_b | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | itrans | native | 0.765 | 0.985 | -0.21999999999999997 | 1 | 45 | 1.3358203432289883e-12 | 1.3358203432289883e-11 | True |
| gemma4-e2b | xnli | itrans | native | 0.435 | 0.465 | -0.030000000000000027 | 27 | 33 | 0.5189580031896519 | 1.0 | False |
| qwen2.5-1.5b | sentiment | itrans | native | 0.5 | 0.505 | -0.0050000000000000044 | 0 | 1 | 1.0 | 1.0 | False |
| qwen2.5-1.5b | xnli | itrans | native | 0.325 | 0.345 | -0.019999999999999962 | 1 | 5 | 0.21875 | 0.875 | False |
| qwen3-1.7b | sentiment | itrans | native | 0.54 | 0.79 | -0.25 | 10 | 60 | 8.004823399455647e-10 | 7.204341059510082e-09 | True |
| qwen3-1.7b | xnli | itrans | native | 0.335 | 0.425 | -0.08999999999999997 | 1 | 19 | 4.00543212890625e-05 | 0.0002803802490234375 | True |
| qwen3.5-2b | sentiment | itrans | native | 0.615 | 0.675 | -0.06000000000000005 | 12 | 24 | 0.06524533522315325 | 0.3262266761157662 | False |
| qwen3.5-2b | xnli | itrans | native | 0.34 | 0.34 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| sarvam-1 | sentiment | itrans | native | 0.78 | 0.96 | -0.17999999999999994 | 4 | 40 | 1.7051434042514302e-08 | 1.3641147234011441e-07 | True |
| sarvam-1 | xnli | itrans | native | 0.37 | 0.455 | -0.08500000000000002 | 6 | 23 | 0.002315700054168701 | 0.013894200325012207 | True |

#### `results/e0b_familiarity/gate1a/summary.json` (33,343 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
provenance.config.models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
provenance.config.forms = ["english", "native", "itrans", "lossy"]
provenance.config.calibration = "contextual, content-free 'N/A' in every field"
provenance.config.templates = "e0_{xnli,sentiment}_v1"
provenance.config.n_per_task = 200
provenance.config.seed = 0
provenance.config.bos = "always prepended"
provenance.config.seconds_per_model_form.qwen2.5-1.5b/english = 36.487061977386475
provenance.config.seconds_per_model_form.qwen2.5-1.5b/native = 60.4139928817749
provenance.config.seconds_per_model_form.qwen2.5-1.5b/itrans = 46.802143573760986
provenance.config.seconds_per_model_form.qwen2.5-1.5b/lossy = 49.93747925758362
provenance.config.seconds_per_model_form.qwen3.5-2b/english = 100.45982670783997
provenance.config.seconds_per_model_form.qwen3.5-2b/native = 137.80759501457214
provenance.config.seconds_per_model_form.qwen3.5-2b/itrans = 135.9841856956482
provenance.config.seconds_per_model_form.qwen3.5-2b/lossy = 107.09859132766724
provenance.config.seconds_per_model_form.sarvam-1/english = 52.38592600822449
provenance.config.seconds_per_model_form.sarvam-1/native = 54.95457744598389
provenance.config.seconds_per_model_form.sarvam-1/itrans = 60.9882435798645
provenance.config.seconds_per_model_form.sarvam-1/lossy = 57.89579892158508
provenance.config.seconds_per_model_form.gemma4-e2b/english = 89.42716455459595
provenance.config.seconds_per_model_form.gemma4-e2b/native = 94.79906296730042
provenance.config.seconds_per_model_form.gemma4-e2b/itrans = 97.28406596183777
provenance.config.seconds_per_model_form.gemma4-e2b/lossy = 92.6928346157074
provenance.config.seconds_per_model_form.qwen3-1.7b/english = 43.18634009361267
provenance.config.seconds_per_model_form.qwen3-1.7b/native = 65.9120557308197
provenance.config.seconds_per_model_form.qwen3-1.7b/itrans = 52.16321563720703
provenance.config.seconds_per_model_form.qwen3-1.7b/lossy = 49.83175706863403
provenance.git_commit = "81d420c0666f561831ae1024ecc85b18ba6ce4bb-dirty"
provenance.timestamp_utc = "2026-10-14T17:04:21+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0b_familiarity.py", "--models", "qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b", "--forms", "english", "native", "itrans", "lossy", "--tag", "gate1a"]
accuracy[0].model = "gemma4-e2b"
accuracy[0].task = "sentiment"
accuracy[0].form = "english"
accuracy[0].n = 200
accuracy[0].chance = 0.5
accuracy[0].acc_cal = 0.98
accuracy[0].acc_cal_ci_low = 0.96
accuracy[0].acc_cal_ci_high = 0.995
accuracy[0].constant_label_rate_cal = 0.5
accuracy[0].acc_raw = 0.985
accuracy[0].acc_raw_ci_low = 0.965
accuracy[0].acc_raw_ci_high = 1.0
accuracy[0].constant_label_rate_raw = 0.505
accuracy[0].tokens_per_word = 1.2214038128249567
accuracy[1].model = "gemma4-e2b"
accuracy[1].task = "sentiment"
accuracy[1].form = "itrans"
accuracy[1].n = 200
accuracy[1].chance = 0.5
accuracy[1].acc_cal = 0.765
accuracy[1].acc_cal_ci_low = 0.705
accuracy[1].acc_cal_ci_high = 0.82
accuracy[1].constant_label_rate_cal = 0.615
accuracy[1].acc_raw = 0.75
accuracy[1].acc_raw_ci_low = 0.69
accuracy[1].acc_raw_ci_high = 0.81
accuracy[1].constant_label_rate_raw = 0.67
accuracy[1].tokens_per_word = 3.943434935521688
accuracy[2].model = "gemma4-e2b"
accuracy[2].task = "sentiment"
accuracy[2].form = "lossy"
accuracy[2].n = 200
accuracy[2].chance = 0.5
accuracy[2].acc_cal = 0.785
accuracy[2].acc_cal_ci_low = 0.725
accuracy[2].acc_cal_ci_high = 0.84
accuracy[2].constant_label_rate_cal = 0.625
accuracy[2].acc_raw = 0.79
accuracy[2].acc_raw_ci_low = 0.73
accuracy[2].acc_raw_ci_high = 0.845
accuracy[2].constant_label_rate_raw = 0.65
accuracy[2].tokens_per_word = 3.2110199296600235
accuracy[3].model = "gemma4-e2b"
accuracy[3].task = "sentiment"
accuracy[3].form = "native"
accuracy[3].n = 200
accuracy[3].chance = 0.5
accuracy[3].acc_cal = 0.985
accuracy[3].acc_cal_ci_low = 0.965
accuracy[3].acc_cal_ci_high = 1.0
accuracy[3].constant_label_rate_cal = 0.505
accuracy[3].acc_raw = 0.985
accuracy[3].acc_raw_ci_low = 0.965
accuracy[3].acc_raw_ci_high = 1.0
accuracy[3].constant_label_rate_raw = 0.505
accuracy[3].tokens_per_word = 3.0767878077373974
accuracy[4].model = "gemma4-e2b"
accuracy[4].task = "xnli"
accuracy[4].form = "english"
accuracy[4].n = 200
accuracy[4].chance = 0.3333333333333333
accuracy[4].acc_cal = 0.6
accuracy[4].acc_cal_ci_low = 0.53
accuracy[4].acc_cal_ci_high = 0.67
accuracy[4].constant_label_rate_cal = 0.56
accuracy[4].acc_raw = 0.735
accuracy[4].acc_raw_ci_low = 0.675
accuracy[4].acc_raw_ci_high = 0.795
accuracy[4].constant_label_rate_raw = 0.405
accuracy[4].tokens_per_word = 1.2397307559544357
accuracy[5].model = "gemma4-e2b"
accuracy[5].task = "xnli"
accuracy[5].form = "itrans"
accuracy[5].n = 200
accuracy[5].chance = 0.3333333333333333
accuracy[5].acc_cal = 0.435
accuracy[5].acc_cal_ci_low = 0.365
accuracy[5].acc_cal_ci_high = 0.505
accuracy[5].constant_label_rate_cal = 0.6
accuracy[5].acc_raw = 0.41
accuracy[5].acc_raw_ci_low = 0.34
accuracy[5].acc_raw_ci_high = 0.48
accuracy[5].constant_label_rate_raw = 0.87
accuracy[5].tokens_per_word = 3.9604674291397313
accuracy[6].model = "gemma4-e2b"
accuracy[6].task = "xnli"
accuracy[6].form = "lossy"
accuracy[6].n = 200
accuracy[6].chance = 0.3333333333333333
accuracy[6].acc_cal = 0.395
accuracy[6].acc_cal_ci_low = 0.33
accuracy[6].acc_cal_ci_high = 0.46
accuracy[6].constant_label_rate_cal = 0.78
accuracy[6].acc_raw = 0.4
accuracy[6].acc_raw_ci_low = 0.335
accuracy[6].acc_raw_ci_high = 0.47
accuracy[6].constant_label_rate_raw = 0.84
accuracy[6].tokens_per_word = 3.2031327697662855
accuracy[7].model = "gemma4-e2b"
accuracy[7].task = "xnli"
accuracy[7].form = "native"
accuracy[7].n = 200
accuracy[7].chance = 0.3333333333333333
accuracy[7].acc_cal = 0.465
accuracy[7].acc_cal_ci_low = 0.395
accuracy[7].acc_cal_ci_high = 0.535
accuracy[7].constant_label_rate_cal = 0.615
accuracy[7].acc_raw = 0.545
accuracy[7].acc_raw_ci_low = 0.475
accuracy[7].acc_raw_ci_high = 0.615
accuracy[7].constant_label_rate_raw = 0.595
accuracy[7].tokens_per_word = 3.1397314768771754
accuracy[8].model = "qwen2.5-1.5b"
accuracy[8].task = "sentiment"
accuracy[8].form = "english"
accuracy[8].n = 200
accuracy[8].chance = 0.5
accuracy[8].acc_cal = 0.52
accuracy[8].acc_cal_ci_low = 0.45
accuracy[8].acc_cal_ci_high = 0.59
accuracy[8].constant_label_rate_cal = 0.98
accuracy[8].acc_raw = 0.985
accuracy[8].acc_raw_ci_low = 0.965
accuracy[8].acc_raw_ci_high = 1.0
accuracy[8].constant_label_rate_raw = 0.515
accuracy[8].tokens_per_word = 1.231369150779896
accuracy[9].model = "qwen2.5-1.5b"
accuracy[9].task = "sentiment"
accuracy[9].form = "itrans"
accuracy[9].n = 200
accuracy[9].chance = 0.5
accuracy[9].acc_cal = 0.5
accuracy[9].acc_cal_ci_low = 0.43
accuracy[9].acc_cal_ci_high = 0.57
accuracy[9].constant_label_rate_cal = 1.0
accuracy[9].acc_raw = 0.495
accuracy[9].acc_raw_ci_low = 0.425
accuracy[9].acc_raw_ci_high = 0.565
accuracy[9].constant_label_rate_raw = 0.995
accuracy[9].tokens_per_word = 4.22538100820633
accuracy[10].model = "qwen2.5-1.5b"
accuracy[10].task = "sentiment"
accuracy[10].form = "lossy"
accuracy[10].n = 200
accuracy[10].chance = 0.5
accuracy[10].acc_cal = 0.5
accuracy[10].acc_cal_ci_low = 0.43
accuracy[10].acc_cal_ci_high = 0.57
accuracy[10].constant_label_rate_cal = 1.0
accuracy[10].acc_raw = 0.5
accuracy[10].acc_raw_ci_low = 0.43
accuracy[10].acc_raw_ci_high = 0.57
accuracy[10].constant_label_rate_raw = 0.97
accuracy[10].tokens_per_word = 3.5679953106682296
accuracy[11].model = "qwen2.5-1.5b"
accuracy[11].task = "sentiment"
accuracy[11].form = "native"
accuracy[11].n = 200
accuracy[11].chance = 0.5
accuracy[11].acc_cal = 0.505
accuracy[11].acc_cal_ci_low = 0.435
accuracy[11].acc_cal_ci_high = 0.575
accuracy[11].constant_label_rate_cal = 0.995
accuracy[11].acc_raw = 0.705
accuracy[11].acc_raw_ci_low = 0.64
accuracy[11].acc_raw_ci_high = 0.765
accuracy[11].constant_label_rate_raw = 0.625
accuracy[11].tokens_per_word = 11.985638921453694
accuracy[12].model = "qwen2.5-1.5b"
accuracy[12].task = "xnli"
accuracy[12].form = "english"
accuracy[12].n = 200
accuracy[12].chance = 0.3333333333333333
accuracy[12].acc_cal = 0.785
accuracy[12].acc_cal_ci_low = 0.73
accuracy[12].acc_cal_ci_high = 0.84
accuracy[12].constant_label_rate_cal = 0.49
accuracy[12].acc_raw = 0.795
accuracy[12].acc_raw_ci_low = 0.735
accuracy[12].acc_raw_ci_high = 0.85
accuracy[12].constant_label_rate_raw = 0.45
accuracy[12].tokens_per_word = 1.2469796341042458
accuracy[13].model = "qwen2.5-1.5b"
accuracy[13].task = "xnli"
accuracy[13].form = "itrans"
accuracy[13].n = 200
accuracy[13].chance = 0.3333333333333333
accuracy[13].acc_cal = 0.325
accuracy[13].acc_cal_ci_low = 0.26
accuracy[13].acc_cal_ci_high = 0.39
accuracy[13].constant_label_rate_cal = 0.965
accuracy[13].acc_raw = 0.375
accuracy[13].acc_raw_ci_low = 0.31
accuracy[13].acc_raw_ci_high = 0.445
accuracy[13].constant_label_rate_raw = 0.845
accuracy[13].tokens_per_word = 4.25161611138737
accuracy[14].model = "qwen2.5-1.5b"
accuracy[14].task = "xnli"
accuracy[14].form = "lossy"
accuracy[14].n = 200
accuracy[14].chance = 0.3333333333333333
accuracy[14].acc_cal = 0.33
accuracy[14].acc_cal_ci_low = 0.265
accuracy[14].acc_cal_ci_high = 0.395
accuracy[14].constant_label_rate_cal = 0.955
accuracy[14].acc_raw = 0.375
accuracy[14].acc_raw_ci_low = 0.31
accuracy[14].acc_raw_ci_high = 0.445
accuracy[14].constant_label_rate_raw = 0.84
accuracy[14].tokens_per_word = 3.5532073595226255
accuracy[15].model = "qwen2.5-1.5b"
accuracy[15].task = "xnli"
accuracy[15].form = "native"
accuracy[15].n = 200
accuracy[15].chance = 0.3333333333333333
accuracy[15].acc_cal = 0.345
accuracy[15].acc_cal_ci_low = 0.28
accuracy[15].acc_cal_ci_high = 0.41
accuracy[15].constant_label_rate_cal = 0.965
accuracy[15].acc_raw = 0.51
accuracy[15].acc_raw_ci_low = 0.445
accuracy[15].acc_raw_ci_high = 0.58
accuracy[15].constant_label_rate_raw = 0.48
accuracy[15].tokens_per_word = 11.79860765788165
accuracy[16].model = "qwen3-1.7b"
accuracy[16].task = "sentiment"
accuracy[16].form = "english"
accuracy[16].n = 200
accuracy[16].chance = 0.5
accuracy[16].acc_cal = 0.98
accuracy[16].acc_cal_ci_low = 0.96
accuracy[16].acc_cal_ci_high = 0.995
accuracy[16].constant_label_rate_cal = 0.5
accuracy[16].acc_raw = 0.985
accuracy[16].acc_raw_ci_low = 0.965
accuracy[16].acc_raw_ci_high = 1.0
accuracy[16].constant_label_rate_raw = 0.515
accuracy[16].tokens_per_word = 1.231369150779896
accuracy[17].model = "qwen3-1.7b"
accuracy[17].task = "sentiment"
accuracy[17].form = "itrans"
accuracy[17].n = 200
accuracy[17].chance = 0.5
accuracy[17].acc_cal = 0.54
accuracy[17].acc_cal_ci_low = 0.47
accuracy[17].acc_cal_ci_high = 0.61
accuracy[17].constant_label_rate_cal = 0.85
accuracy[17].acc_raw = 0.58
accuracy[17].acc_raw_ci_low = 0.51
accuracy[17].acc_raw_ci_high = 0.645
accuracy[17].constant_label_rate_raw = 0.68
accuracy[17].tokens_per_word = 4.22538100820633
accuracy[18].model = "qwen3-1.7b"
accuracy[18].task = "sentiment"
accuracy[18].form = "lossy"
accuracy[18].n = 200
accuracy[18].chance = 0.5
accuracy[18].acc_cal = 0.52
accuracy[18].acc_cal_ci_low = 0.45
accuracy[18].acc_cal_ci_high = 0.59
accuracy[18].constant_label_rate_cal = 0.91
accuracy[18].acc_raw = 0.575
accuracy[18].acc_raw_ci_low = 0.505
accuracy[18].acc_raw_ci_high = 0.64
accuracy[18].constant_label_rate_raw = 0.715
accuracy[18].tokens_per_word = 3.5679953106682296
accuracy[19].model = "qwen3-1.7b"
accuracy[19].task = "sentiment"
accuracy[19].form = "native"
accuracy[19].n = 200
accuracy[19].chance = 0.5
accuracy[19].acc_cal = 0.79
accuracy[19].acc_cal_ci_low = 0.73
accuracy[19].acc_cal_ci_high = 0.845
accuracy[19].constant_label_rate_cal = 0.68
accuracy[19].acc_raw = 0.865
accuracy[19].acc_raw_ci_low = 0.815
accuracy[19].acc_raw_ci_high = 0.91
accuracy[19].constant_label_rate_raw = 0.525
accuracy[19].tokens_per_word = 11.985638921453694
accuracy[20].model = "qwen3-1.7b"
accuracy[20].task = "xnli"
accuracy[20].form = "english"
accuracy[20].n = 200
accuracy[20].chance = 0.3333333333333333
accuracy[20].acc_cal = 0.54
accuracy[20].acc_cal_ci_low = 0.47
accuracy[20].acc_cal_ci_high = 0.61
accuracy[20].constant_label_rate_cal = 0.765
accuracy[20].acc_raw = 0.615
accuracy[20].acc_raw_ci_low = 0.545
accuracy[20].acc_raw_ci_high = 0.68
accuracy[20].constant_label_rate_raw = 0.53
accuracy[20].tokens_per_word = 1.2469796341042458
accuracy[21].model = "qwen3-1.7b"
accuracy[21].task = "xnli"
accuracy[21].form = "itrans"
accuracy[21].n = 200
accuracy[21].chance = 0.3333333333333333
accuracy[21].acc_cal = 0.335
accuracy[21].acc_cal_ci_low = 0.27
accuracy[21].acc_cal_ci_high = 0.4
accuracy[21].constant_label_rate_cal = 0.995
accuracy[21].acc_raw = 0.37
accuracy[21].acc_raw_ci_low = 0.305
accuracy[21].acc_raw_ci_high = 0.44
accuracy[21].constant_label_rate_raw = 0.8
accuracy[21].tokens_per_word = 4.25161611138737
accuracy[22].model = "qwen3-1.7b"
accuracy[22].task = "xnli"
accuracy[22].form = "lossy"
accuracy[22].n = 200
accuracy[22].chance = 0.3333333333333333
accuracy[22].acc_cal = 0.335
accuracy[22].acc_cal_ci_low = 0.27
accuracy[22].acc_cal_ci_high = 0.4
accuracy[22].constant_label_rate_cal = 0.995
accuracy[22].acc_raw = 0.415
accuracy[22].acc_raw_ci_low = 0.345
accuracy[22].acc_raw_ci_high = 0.485
accuracy[22].constant_label_rate_raw = 0.795
accuracy[22].tokens_per_word = 3.5532073595226255
accuracy[23].model = "qwen3-1.7b"
accuracy[23].task = "xnli"
accuracy[23].form = "native"
accuracy[23].n = 200
accuracy[23].chance = 0.3333333333333333
accuracy[23].acc_cal = 0.425
accuracy[23].acc_cal_ci_low = 0.355
accuracy[23].acc_cal_ci_high = 0.495
accuracy[23].constant_label_rate_cal = 0.89
accuracy[23].acc_raw = 0.43
accuracy[23].acc_raw_ci_low = 0.36
accuracy[23].acc_raw_ci_high = 0.5
accuracy[23].constant_label_rate_raw = 0.61
accuracy[23].tokens_per_word = 11.79860765788165
accuracy[24].model = "qwen3.5-2b"
accuracy[24].task = "sentiment"
accuracy[24].form = "english"
accuracy[24].n = 200
accuracy[24].chance = 0.5
accuracy[24].acc_cal = 0.975
accuracy[24].acc_cal_ci_low = 0.95
accuracy[24].acc_cal_ci_high = 0.995
accuracy[24].constant_label_rate_cal = 0.525
accuracy[24].acc_raw = 0.975
accuracy[24].acc_raw_ci_low = 0.95
accuracy[24].acc_raw_ci_high = 0.995
accuracy[24].constant_label_rate_raw = 0.505
accuracy[24].tokens_per_word = 1.2268197573656845
accuracy[25].model = "qwen3.5-2b"
accuracy[25].task = "sentiment"
accuracy[25].form = "itrans"
accuracy[25].n = 200
accuracy[25].chance = 0.5
accuracy[25].acc_cal = 0.615
accuracy[25].acc_cal_ci_low = 0.545
accuracy[25].acc_cal_ci_high = 0.685
accuracy[25].constant_label_rate_cal = 0.855
accuracy[25].acc_raw = 0.675
accuracy[25].acc_raw_ci_low = 0.61
accuracy[25].acc_raw_ci_high = 0.74
accuracy[25].constant_label_rate_raw = 0.665
accuracy[25].tokens_per_word = 4.087631887456038
accuracy[26].model = "qwen3.5-2b"
accuracy[26].task = "sentiment"
accuracy[26].form = "lossy"
accuracy[26].n = 200
accuracy[26].chance = 0.5
accuracy[26].acc_cal = 0.645
accuracy[26].acc_cal_ci_low = 0.58
accuracy[26].acc_cal_ci_high = 0.71
accuracy[26].constant_label_rate_cal = 0.815
accuracy[26].acc_raw = 0.675
accuracy[26].acc_raw_ci_low = 0.61
accuracy[26].acc_raw_ci_high = 0.735
accuracy[26].constant_label_rate_raw = 0.645
accuracy[26].tokens_per_word = 3.3423212192262604
accuracy[27].model = "qwen3.5-2b"
accuracy[27].task = "sentiment"
accuracy[27].form = "native"
accuracy[27].n = 200
accuracy[27].chance = 0.5
accuracy[27].acc_cal = 0.675
accuracy[27].acc_cal_ci_low = 0.61
accuracy[27].acc_cal_ci_high = 0.74
accuracy[27].constant_label_rate_cal = 0.815
accuracy[27].acc_raw = 0.785
accuracy[27].acc_raw_ci_low = 0.725
accuracy[27].acc_raw_ci_high = 0.84
accuracy[27].constant_label_rate_raw = 0.705
accuracy[27].tokens_per_word = 5.235052754982415
accuracy[28].model = "qwen3.5-2b"
accuracy[28].task = "xnli"
accuracy[28].form = "english"
accuracy[28].n = 200
accuracy[28].chance = 0.3333333333333333
accuracy[28].acc_cal = 0.45
accuracy[28].acc_cal_ci_low = 0.38
accuracy[28].acc_cal_ci_high = 0.52
accuracy[28].constant_label_rate_cal = 0.845
accuracy[28].acc_raw = 0.43
accuracy[28].acc_raw_ci_low = 0.36
accuracy[28].acc_raw_ci_high = 0.5
accuracy[28].constant_label_rate_raw = 0.89
accuracy[28].tokens_per_word = 1.2424922333448394
accuracy[29].model = "qwen3.5-2b"
accuracy[29].task = "xnli"
accuracy[29].form = "itrans"
accuracy[29].n = 200
accuracy[29].chance = 0.3333333333333333
accuracy[29].acc_cal = 0.34
accuracy[29].acc_cal_ci_low = 0.275
accuracy[29].acc_cal_ci_high = 0.405
accuracy[29].constant_label_rate_cal = 0.995
accuracy[29].acc_raw = 0.34
accuracy[29].acc_raw_ci_low = 0.275
accuracy[29].acc_raw_ci_high = 0.405
accuracy[29].constant_label_rate_raw = 0.995
accuracy[29].tokens_per_word = 4.1282943809050225
accuracy[30].model = "qwen3.5-2b"
accuracy[30].task = "xnli"
accuracy[30].form = "lossy"
accuracy[30].n = 200
accuracy[30].chance = 0.3333333333333333
accuracy[30].acc_cal = 0.335
accuracy[30].acc_cal_ci_low = 0.27
accuracy[30].acc_cal_ci_high = 0.4
accuracy[30].constant_label_rate_cal = 0.99
accuracy[30].acc_raw = 0.34
accuracy[30].acc_raw_ci_low = 0.275
accuracy[30].acc_raw_ci_high = 0.405
accuracy[30].constant_label_rate_raw = 0.995
accuracy[30].tokens_per_word = 3.3431128791645945
accuracy[31].model = "qwen3.5-2b"
accuracy[31].task = "xnli"
accuracy[31].form = "native"
accuracy[31].n = 200
accuracy[31].chance = 0.3333333333333333
accuracy[31].acc_cal = 0.34
accuracy[31].acc_cal_ci_low = 0.275
accuracy[31].acc_cal_ci_high = 0.405
accuracy[31].constant_label_rate_cal = 0.995
accuracy[31].acc_raw = 0.34
accuracy[31].acc_raw_ci_low = 0.275
accuracy[31].acc_raw_ci_high = 0.405
accuracy[31].constant_label_rate_raw = 0.995
accuracy[31].tokens_per_word = 5.230979612133267
accuracy[32].model = "sarvam-1"
accuracy[32].task = "sentiment"
accuracy[32].form = "english"
accuracy[32].n = 200
accuracy[32].chance = 0.5
accuracy[32].acc_cal = 0.975
accuracy[32].acc_cal_ci_low = 0.95
accuracy[32].acc_cal_ci_high = 0.995
accuracy[32].constant_label_rate_cal = 0.515
accuracy[32].acc_raw = 0.975
accuracy[32].acc_raw_ci_low = 0.95
accuracy[32].acc_raw_ci_high = 0.995
accuracy[32].constant_label_rate_raw = 0.505
accuracy[32].tokens_per_word = 1.4204939341421143
accuracy[33].model = "sarvam-1"
accuracy[33].task = "sentiment"
accuracy[33].form = "itrans"
accuracy[33].n = 200
accuracy[33].chance = 0.5
accuracy[33].acc_cal = 0.78
accuracy[33].acc_cal_ci_low = 0.72
accuracy[33].acc_cal_ci_high = 0.835
accuracy[33].constant_label_rate_cal = 0.69
accuracy[33].acc_raw = 0.845
accuracy[33].acc_raw_ci_low = 0.795
accuracy[33].acc_raw_ci_high = 0.895
accuracy[33].constant_label_rate_raw = 0.515
accuracy[33].tokens_per_word = 5.238569753810082
accuracy[34].model = "sarvam-1"
accuracy[34].task = "sentiment"
accuracy[34].form = "lossy"
accuracy[34].n = 200
accuracy[34].chance = 0.5
accuracy[34].acc_cal = 0.86
accuracy[34].acc_cal_ci_low = 0.81
accuracy[34].acc_cal_ci_high = 0.905
accuracy[34].constant_label_rate_cal = 0.63
accuracy[34].acc_raw = 0.91
accuracy[34].acc_raw_ci_low = 0.87
accuracy[34].acc_raw_ci_high = 0.95
accuracy[34].constant_label_rate_raw = 0.51
accuracy[34].tokens_per_word = 4.357561547479484
accuracy[35].model = "sarvam-1"
accuracy[35].task = "sentiment"
accuracy[35].form = "native"
accuracy[35].n = 200
accuracy[35].chance = 0.5
accuracy[35].acc_cal = 0.96
accuracy[35].acc_cal_ci_low = 0.93
accuracy[35].acc_cal_ci_high = 0.985
accuracy[35].constant_label_rate_cal = 0.51
accuracy[35].acc_raw = 0.96
accuracy[35].acc_raw_ci_low = 0.93
accuracy[35].acc_raw_ci_high = 0.985
accuracy[35].constant_label_rate_raw = 0.53
accuracy[35].tokens_per_word = 2.2708089097303636
accuracy[36].model = "sarvam-1"
accuracy[36].task = "xnli"
accuracy[36].form = "english"
accuracy[36].n = 200
accuracy[36].chance = 0.3333333333333333
accuracy[36].acc_cal = 0.475
accuracy[36].acc_cal_ci_low = 0.405
accuracy[36].acc_cal_ci_high = 0.545
accuracy[36].constant_label_rate_cal = 0.655
accuracy[36].acc_raw = 0.53
accuracy[36].acc_raw_ci_low = 0.46
accuracy[36].acc_raw_ci_high = 0.6
accuracy[36].constant_label_rate_raw = 0.63
accuracy[36].tokens_per_word = 1.4326889886089058
accuracy[37].model = "sarvam-1"
accuracy[37].task = "xnli"
accuracy[37].form = "itrans"
accuracy[37].n = 200
accuracy[37].chance = 0.3333333333333333
accuracy[37].acc_cal = 0.37
accuracy[37].acc_cal_ci_low = 0.3
accuracy[37].acc_cal_ci_high = 0.44
accuracy[37].constant_label_rate_cal = 0.865
accuracy[37].acc_raw = 0.385
accuracy[37].acc_raw_ci_low = 0.32
accuracy[37].acc_raw_ci_high = 0.455
accuracy[37].constant_label_rate_raw = 0.8
accuracy[37].tokens_per_word = 5.226255594231725
accuracy[38].model = "sarvam-1"
accuracy[38].task = "xnli"
accuracy[38].form = "lossy"
accuracy[38].n = 200
accuracy[38].chance = 0.3333333333333333
accuracy[38].acc_cal = 0.375
accuracy[38].acc_cal_ci_low = 0.31
accuracy[38].acc_cal_ci_high = 0.44
accuracy[38].constant_label_rate_cal = 0.905
accuracy[38].acc_raw = 0.46
accuracy[38].acc_raw_ci_low = 0.39
accuracy[38].acc_raw_ci_high = 0.53
accuracy[38].constant_label_rate_raw = 0.595
accuracy[38].tokens_per_word = 4.335405271009448
accuracy[39].model = "sarvam-1"
accuracy[39].task = "xnli"
accuracy[39].form = "native"
accuracy[39].n = 200
accuracy[39].chance = 0.3333333333333333
accuracy[39].acc_cal = 0.455
accuracy[39].acc_cal_ci_low = 0.385
accuracy[39].acc_cal_ci_high = 0.525
accuracy[39].constant_label_rate_cal = 0.865
accuracy[39].acc_raw = 0.52
accuracy[39].acc_raw_ci_low = 0.45
accuracy[39].acc_raw_ci_high = 0.59
accuracy[39].constant_label_rate_raw = 0.61
accuracy[39].tokens_per_word = 2.1452013923421185
mcnemar[0].model = "gemma4-e2b"
mcnemar[0].task = "sentiment"
mcnemar[0].a = "lossy"
mcnemar[0].b = "itrans"
mcnemar[0].acc_a = 0.785
mcnemar[0].acc_b = 0.765
mcnemar[0].diff = 0.020000000000000018
mcnemar[0].a_only = 19
mcnemar[0].b_only = 15
mcnemar[0].p = 0.6075913612730801
mcnemar[0].p_holm = 1.0
mcnemar[0].significant = false
mcnemar[1].model = "gemma4-e2b"
mcnemar[1].task = "xnli"
mcnemar[1].a = "lossy"
mcnemar[1].b = "itrans"
mcnemar[1].acc_a = 0.395
mcnemar[1].acc_b = 0.435
mcnemar[1].diff = -0.03999999999999998
mcnemar[1].a_only = 19
mcnemar[1].b_only = 27
mcnemar[1].p = 0.3019956131896606
mcnemar[1].p_holm = 1.0
mcnemar[1].significant = false
mcnemar[2].model = "qwen2.5-1.5b"
mcnemar[2].task = "sentiment"
mcnemar[2].a = "lossy"
mcnemar[2].b = "itrans"
mcnemar[2].acc_a = 0.5
mcnemar[2].acc_b = 0.5
mcnemar[2].diff = 0.0
mcnemar[2].a_only = 0
mcnemar[2].b_only = 0
mcnemar[2].p = 1.0
mcnemar[2].p_holm = 1.0
mcnemar[2].significant = false
mcnemar[3].model = "qwen2.5-1.5b"
mcnemar[3].task = "xnli"
mcnemar[3].a = "lossy"
mcnemar[3].b = "itrans"
mcnemar[3].acc_a = 0.33
mcnemar[3].acc_b = 0.325
mcnemar[3].diff = 0.0050000000000000044
mcnemar[3].a_only = 4
mcnemar[3].b_only = 3
mcnemar[3].p = 1.0
mcnemar[3].p_holm = 1.0
mcnemar[3].significant = false
mcnemar[4].model = "qwen3-1.7b"
mcnemar[4].task = "sentiment"
mcnemar[4].a = "lossy"
mcnemar[4].b = "itrans"
mcnemar[4].acc_a = 0.52
mcnemar[4].acc_b = 0.54
mcnemar[4].diff = -0.020000000000000018
mcnemar[4].a_only = 14
mcnemar[4].b_only = 18
mcnemar[4].p = 0.5966148958541453
mcnemar[4].p_holm = 1.0
mcnemar[4].significant = false
mcnemar[5].model = "qwen3-1.7b"
mcnemar[5].task = "xnli"
mcnemar[5].a = "lossy"
mcnemar[5].b = "itrans"
mcnemar[5].acc_a = 0.335
mcnemar[5].acc_b = 0.335
mcnemar[5].diff = 0.0
mcnemar[5].a_only = 0
mcnemar[5].b_only = 0
mcnemar[5].p = 1.0
mcnemar[5].p_holm = 1.0
mcnemar[5].significant = false
mcnemar[6].model = "qwen3.5-2b"
mcnemar[6].task = "sentiment"
mcnemar[6].a = "lossy"
mcnemar[6].b = "itrans"
mcnemar[6].acc_a = 0.645
mcnemar[6].acc_b = 0.615
mcnemar[6].diff = 0.030000000000000027
mcnemar[6].a_only = 22
mcnemar[6].b_only = 16
mcnemar[6].p = 0.417692190836533
mcnemar[6].p_holm = 1.0
mcnemar[6].significant = false
mcnemar[7].model = "qwen3.5-2b"
mcnemar[7].task = "xnli"
mcnemar[7].a = "lossy"
mcnemar[7].b = "itrans"
mcnemar[7].acc_a = 0.335
mcnemar[7].acc_b = 0.34
mcnemar[7].diff = -0.0050000000000000044
mcnemar[7].a_only = 0
mcnemar[7].b_only = 1
mcnemar[7].p = 1.0
mcnemar[7].p_holm = 1.0
mcnemar[7].significant = false
mcnemar[8].model = "sarvam-1"
mcnemar[8].task = "sentiment"
mcnemar[8].a = "lossy"
mcnemar[8].b = "itrans"
mcnemar[8].acc_a = 0.86
mcnemar[8].acc_b = 0.78
mcnemar[8].diff = 0.07999999999999996
mcnemar[8].a_only = 25
mcnemar[8].b_only = 9
mcnemar[8].p = 0.00904118549078703
mcnemar[8].p_holm = 0.09041185490787029
mcnemar[8].significant = false
mcnemar[9].model = "sarvam-1"
mcnemar[9].task = "xnli"
mcnemar[9].a = "lossy"
mcnemar[9].b = "itrans"
mcnemar[9].acc_a = 0.375
mcnemar[9].acc_b = 0.37
mcnemar[9].diff = 0.0050000000000000044
mcnemar[9].a_only = 12
mcnemar[9].b_only = 11
mcnemar[9].p = 1.0
mcnemar[9].p_holm = 1.0
mcnemar[9].significant = false
mcnemar_exploratory[0].model = "gemma4-e2b"
mcnemar_exploratory[0].task = "sentiment"
mcnemar_exploratory[0].a = "itrans"
mcnemar_exploratory[0].b = "native"
mcnemar_exploratory[0].acc_a = 0.765
mcnemar_exploratory[0].acc_b = 0.985
mcnemar_exploratory[0].diff = -0.21999999999999997
mcnemar_exploratory[0].a_only = 1
mcnemar_exploratory[0].b_only = 45
mcnemar_exploratory[0].p = 1.3358203432289883e-12
mcnemar_exploratory[0].p_holm = 1.3358203432289883e-11
mcnemar_exploratory[0].significant = true
mcnemar_exploratory[1].model = "gemma4-e2b"
mcnemar_exploratory[1].task = "xnli"
mcnemar_exploratory[1].a = "itrans"
mcnemar_exploratory[1].b = "native"
mcnemar_exploratory[1].acc_a = 0.435
mcnemar_exploratory[1].acc_b = 0.465
mcnemar_exploratory[1].diff = -0.030000000000000027
mcnemar_exploratory[1].a_only = 27
mcnemar_exploratory[1].b_only = 33
mcnemar_exploratory[1].p = 0.5189580031896519
mcnemar_exploratory[1].p_holm = 1.0
mcnemar_exploratory[1].significant = false
mcnemar_exploratory[2].model = "qwen2.5-1.5b"
mcnemar_exploratory[2].task = "sentiment"
mcnemar_exploratory[2].a = "itrans"
mcnemar_exploratory[2].b = "native"
mcnemar_exploratory[2].acc_a = 0.5
mcnemar_exploratory[2].acc_b = 0.505
mcnemar_exploratory[2].diff = -0.0050000000000000044
mcnemar_exploratory[2].a_only = 0
mcnemar_exploratory[2].b_only = 1
mcnemar_exploratory[2].p = 1.0
mcnemar_exploratory[2].p_holm = 1.0
mcnemar_exploratory[2].significant = false
mcnemar_exploratory[3].model = "qwen2.5-1.5b"
mcnemar_exploratory[3].task = "xnli"
mcnemar_exploratory[3].a = "itrans"
mcnemar_exploratory[3].b = "native"
mcnemar_exploratory[3].acc_a = 0.325
mcnemar_exploratory[3].acc_b = 0.345
mcnemar_exploratory[3].diff = -0.019999999999999962
mcnemar_exploratory[3].a_only = 1
mcnemar_exploratory[3].b_only = 5
mcnemar_exploratory[3].p = 0.21875
mcnemar_exploratory[3].p_holm = 0.875
mcnemar_exploratory[3].significant = false
mcnemar_exploratory[4].model = "qwen3-1.7b"
mcnemar_exploratory[4].task = "sentiment"
mcnemar_exploratory[4].a = "itrans"
mcnemar_exploratory[4].b = "native"
mcnemar_exploratory[4].acc_a = 0.54
mcnemar_exploratory[4].acc_b = 0.79
mcnemar_exploratory[4].diff = -0.25
mcnemar_exploratory[4].a_only = 10
mcnemar_exploratory[4].b_only = 60
mcnemar_exploratory[4].p = 8.004823399455647e-10
mcnemar_exploratory[4].p_holm = 7.204341059510082e-09
mcnemar_exploratory[4].significant = true
mcnemar_exploratory[5].model = "qwen3-1.7b"
mcnemar_exploratory[5].task = "xnli"
mcnemar_exploratory[5].a = "itrans"
mcnemar_exploratory[5].b = "native"
mcnemar_exploratory[5].acc_a = 0.335
mcnemar_exploratory[5].acc_b = 0.425
mcnemar_exploratory[5].diff = -0.08999999999999997
mcnemar_exploratory[5].a_only = 1
mcnemar_exploratory[5].b_only = 19
mcnemar_exploratory[5].p = 4.00543212890625e-05
mcnemar_exploratory[5].p_holm = 0.0002803802490234375
mcnemar_exploratory[5].significant = true
mcnemar_exploratory[6].model = "qwen3.5-2b"
mcnemar_exploratory[6].task = "sentiment"
mcnemar_exploratory[6].a = "itrans"
mcnemar_exploratory[6].b = "native"
mcnemar_exploratory[6].acc_a = 0.615
mcnemar_exploratory[6].acc_b = 0.675
mcnemar_exploratory[6].diff = -0.06000000000000005
mcnemar_exploratory[6].a_only = 12
mcnemar_exploratory[6].b_only = 24
mcnemar_exploratory[6].p = 0.06524533522315325
mcnemar_exploratory[6].p_holm = 0.3262266761157662
mcnemar_exploratory[6].significant = false
mcnemar_exploratory[7].model = "qwen3.5-2b"
mcnemar_exploratory[7].task = "xnli"
mcnemar_exploratory[7].a = "itrans"
mcnemar_exploratory[7].b = "native"
mcnemar_exploratory[7].acc_a = 0.34
mcnemar_exploratory[7].acc_b = 0.34
mcnemar_exploratory[7].diff = 0.0
mcnemar_exploratory[7].a_only = 0
mcnemar_exploratory[7].b_only = 0
mcnemar_exploratory[7].p = 1.0
mcnemar_exploratory[7].p_holm = 1.0
mcnemar_exploratory[7].significant = false
mcnemar_exploratory[8].model = "sarvam-1"
mcnemar_exploratory[8].task = "sentiment"
mcnemar_exploratory[8].a = "itrans"
mcnemar_exploratory[8].b = "native"
mcnemar_exploratory[8].acc_a = 0.78
mcnemar_exploratory[8].acc_b = 0.96
mcnemar_exploratory[8].diff = -0.17999999999999994
mcnemar_exploratory[8].a_only = 4
mcnemar_exploratory[8].b_only = 40
mcnemar_exploratory[8].p = 1.7051434042514302e-08
mcnemar_exploratory[8].p_holm = 1.3641147234011441e-07
mcnemar_exploratory[8].significant = true
mcnemar_exploratory[9].model = "sarvam-1"
mcnemar_exploratory[9].task = "xnli"
mcnemar_exploratory[9].a = "itrans"
mcnemar_exploratory[9].b = "native"
mcnemar_exploratory[9].acc_a = 0.37
mcnemar_exploratory[9].acc_b = 0.455
mcnemar_exploratory[9].diff = -0.08500000000000002
mcnemar_exploratory[9].a_only = 6
mcnemar_exploratory[9].b_only = 23
mcnemar_exploratory[9].p = 0.002315700054168701
mcnemar_exploratory[9].p_holm = 0.013894200325012207
mcnemar_exploratory[9].significant = true
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.2469796341042458
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.231369150779896
fertility[2].model = "qwen2.5-1.5b"
fertility[2].task = "xnli"
fertility[2].form = "native"
fertility[2].n_texts = 400
fertility[2].tokens_per_word = 11.79860765788165
fertility[3].model = "qwen2.5-1.5b"
fertility[3].task = "sentiment"
fertility[3].form = "native"
fertility[3].n_texts = 200
fertility[3].tokens_per_word = 11.985638921453694
fertility[4].model = "qwen2.5-1.5b"
fertility[4].task = "xnli"
fertility[4].form = "itrans"
fertility[4].n_texts = 400
fertility[4].tokens_per_word = 4.25161611138737
fertility[5].model = "qwen2.5-1.5b"
fertility[5].task = "sentiment"
fertility[5].form = "itrans"
fertility[5].n_texts = 200
fertility[5].tokens_per_word = 4.22538100820633
fertility[6].model = "qwen2.5-1.5b"
fertility[6].task = "xnli"
fertility[6].form = "lossy"
fertility[6].n_texts = 400
fertility[6].tokens_per_word = 3.5532073595226255
fertility[7].model = "qwen2.5-1.5b"
fertility[7].task = "sentiment"
fertility[7].form = "lossy"
fertility[7].n_texts = 200
fertility[7].tokens_per_word = 3.5679953106682296
fertility[8].model = "qwen3.5-2b"
fertility[8].task = "xnli"
fertility[8].form = "english"
fertility[8].n_texts = 400
fertility[8].tokens_per_word = 1.2424922333448394
fertility[9].model = "qwen3.5-2b"
fertility[9].task = "sentiment"
fertility[9].form = "english"
fertility[9].n_texts = 200
fertility[9].tokens_per_word = 1.2268197573656845
fertility[10].model = "qwen3.5-2b"
fertility[10].task = "xnli"
fertility[10].form = "native"
fertility[10].n_texts = 400
fertility[10].tokens_per_word = 5.230979612133267
fertility[11].model = "qwen3.5-2b"
fertility[11].task = "sentiment"
fertility[11].form = "native"
fertility[11].n_texts = 200
fertility[11].tokens_per_word = 5.235052754982415
fertility[12].model = "qwen3.5-2b"
fertility[12].task = "xnli"
fertility[12].form = "itrans"
fertility[12].n_texts = 400
fertility[12].tokens_per_word = 4.1282943809050225
fertility[13].model = "qwen3.5-2b"
fertility[13].task = "sentiment"
fertility[13].form = "itrans"
fertility[13].n_texts = 200
fertility[13].tokens_per_word = 4.087631887456038
fertility[14].model = "qwen3.5-2b"
fertility[14].task = "xnli"
fertility[14].form = "lossy"
fertility[14].n_texts = 400
fertility[14].tokens_per_word = 3.3431128791645945
fertility[15].model = "qwen3.5-2b"
fertility[15].task = "sentiment"
fertility[15].form = "lossy"
fertility[15].n_texts = 200
fertility[15].tokens_per_word = 3.3423212192262604
fertility[16].model = "sarvam-1"
fertility[16].task = "xnli"
fertility[16].form = "english"
fertility[16].n_texts = 400
fertility[16].tokens_per_word = 1.4326889886089058
fertility[17].model = "sarvam-1"
fertility[17].task = "sentiment"
fertility[17].form = "english"
fertility[17].n_texts = 200
fertility[17].tokens_per_word = 1.4204939341421143
fertility[18].model = "sarvam-1"
fertility[18].task = "xnli"
fertility[18].form = "native"
fertility[18].n_texts = 400
fertility[18].tokens_per_word = 2.1452013923421185
fertility[19].model = "sarvam-1"
fertility[19].task = "sentiment"
fertility[19].form = "native"
fertility[19].n_texts = 200
fertility[19].tokens_per_word = 2.2708089097303636
fertility[20].model = "sarvam-1"
fertility[20].task = "xnli"
fertility[20].form = "itrans"
fertility[20].n_texts = 400
fertility[20].tokens_per_word = 5.226255594231725
fertility[21].model = "sarvam-1"
fertility[21].task = "sentiment"
fertility[21].form = "itrans"
fertility[21].n_texts = 200
fertility[21].tokens_per_word = 5.238569753810082
fertility[22].model = "sarvam-1"
fertility[22].task = "xnli"
fertility[22].form = "lossy"
fertility[22].n_texts = 400
fertility[22].tokens_per_word = 4.335405271009448
fertility[23].model = "sarvam-1"
fertility[23].task = "sentiment"
fertility[23].form = "lossy"
fertility[23].n_texts = 200
fertility[23].tokens_per_word = 4.357561547479484
fertility[24].model = "gemma4-e2b"
fertility[24].task = "xnli"
fertility[24].form = "english"
fertility[24].n_texts = 400
fertility[24].tokens_per_word = 1.2397307559544357
fertility[25].model = "gemma4-e2b"
fertility[25].task = "sentiment"
fertility[25].form = "english"
fertility[25].n_texts = 200
fertility[25].tokens_per_word = 1.2214038128249567
fertility[26].model = "gemma4-e2b"
fertility[26].task = "xnli"
fertility[26].form = "native"
fertility[26].n_texts = 400
fertility[26].tokens_per_word = 3.1397314768771754
fertility[27].model = "gemma4-e2b"
fertility[27].task = "sentiment"
fertility[27].form = "native"
fertility[27].n_texts = 200
fertility[27].tokens_per_word = 3.0767878077373974
fertility[28].model = "gemma4-e2b"
fertility[28].task = "xnli"
fertility[28].form = "itrans"
fertility[28].n_texts = 400
fertility[28].tokens_per_word = 3.9604674291397313
fertility[29].model = "gemma4-e2b"
fertility[29].task = "sentiment"
fertility[29].form = "itrans"
fertility[29].n_texts = 200
fertility[29].tokens_per_word = 3.943434935521688
fertility[30].model = "gemma4-e2b"
fertility[30].task = "xnli"
fertility[30].form = "lossy"
fertility[30].n_texts = 400
fertility[30].tokens_per_word = 3.2031327697662855
fertility[31].model = "gemma4-e2b"
fertility[31].task = "sentiment"
fertility[31].form = "lossy"
fertility[31].n_texts = 200
fertility[31].tokens_per_word = 3.2110199296600235
fertility[32].model = "qwen3-1.7b"
fertility[32].task = "xnli"
fertility[32].form = "english"
fertility[32].n_texts = 400
fertility[32].tokens_per_word = 1.2469796341042458
fertility[33].model = "qwen3-1.7b"
fertility[33].task = "sentiment"
fertility[33].form = "english"
fertility[33].n_texts = 200
fertility[33].tokens_per_word = 1.231369150779896
fertility[34].model = "qwen3-1.7b"
fertility[34].task = "xnli"
fertility[34].form = "native"
fertility[34].n_texts = 400
fertility[34].tokens_per_word = 11.79860765788165
fertility[35].model = "qwen3-1.7b"
fertility[35].task = "sentiment"
fertility[35].form = "native"
fertility[35].n_texts = 200
fertility[35].tokens_per_word = 11.985638921453694
fertility[36].model = "qwen3-1.7b"
fertility[36].task = "xnli"
fertility[36].form = "itrans"
fertility[36].n_texts = 400
fertility[36].tokens_per_word = 4.25161611138737
fertility[37].model = "qwen3-1.7b"
fertility[37].task = "sentiment"
fertility[37].form = "itrans"
fertility[37].n_texts = 200
fertility[37].tokens_per_word = 4.22538100820633
fertility[38].model = "qwen3-1.7b"
fertility[38].task = "xnli"
fertility[38].form = "lossy"
fertility[38].n_texts = 400
fertility[38].tokens_per_word = 3.5532073595226255
fertility[39].model = "qwen3-1.7b"
fertility[39].task = "sentiment"
fertility[39].form = "lossy"
fertility[39].n_texts = 200
fertility[39].tokens_per_word = 3.5679953106682296
verdicts.informative_cells = ["gemma4-e2b/sentiment", "gemma4-e2b/xnli", "qwen2.5-1.5b/xnli", "qwen3-1.7b/sentiment", "qwen3-1.7b/xnli", "qwen3.5-2b/sentiment", "qwen3.5-2b/xnli", "sarvam-1/sentiment", "sarvam-1/xnli"]
verdicts.P3_lossy_lt_itrans = false
verdicts.P3_parts.all_cells_lossy_below_itrans = false
verdicts.P3_parts.fraction_significant = 0.0
verdicts.P3_parts.n_cells = 9
verdicts.P1_familiarity_dominates = "pending (natural form not scored)"
verdicts.P2_fragmentation_also_matters = "pending (natural form not scored)"
`````

#### `results/e0b_familiarity/gate1a/verdicts.json` (2,568 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
provenance.config.models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
provenance.config.forms = ["english", "native", "itrans", "lossy"]
provenance.config.calibration = "contextual, content-free 'N/A' in every field"
provenance.config.templates = "e0_{xnli,sentiment}_v1"
provenance.config.n_per_task = 200
provenance.config.seed = 0
provenance.config.bos = "always prepended"
provenance.config.seconds_per_model_form.qwen2.5-1.5b/english = 36.487061977386475
provenance.config.seconds_per_model_form.qwen2.5-1.5b/native = 60.4139928817749
provenance.config.seconds_per_model_form.qwen2.5-1.5b/itrans = 46.802143573760986
provenance.config.seconds_per_model_form.qwen2.5-1.5b/lossy = 49.93747925758362
provenance.config.seconds_per_model_form.qwen3.5-2b/english = 100.45982670783997
provenance.config.seconds_per_model_form.qwen3.5-2b/native = 137.80759501457214
provenance.config.seconds_per_model_form.qwen3.5-2b/itrans = 135.9841856956482
provenance.config.seconds_per_model_form.qwen3.5-2b/lossy = 107.09859132766724
provenance.config.seconds_per_model_form.sarvam-1/english = 52.38592600822449
provenance.config.seconds_per_model_form.sarvam-1/native = 54.95457744598389
provenance.config.seconds_per_model_form.sarvam-1/itrans = 60.9882435798645
provenance.config.seconds_per_model_form.sarvam-1/lossy = 57.89579892158508
provenance.config.seconds_per_model_form.gemma4-e2b/english = 89.42716455459595
provenance.config.seconds_per_model_form.gemma4-e2b/native = 94.79906296730042
provenance.config.seconds_per_model_form.gemma4-e2b/itrans = 97.28406596183777
provenance.config.seconds_per_model_form.gemma4-e2b/lossy = 92.6928346157074
provenance.config.seconds_per_model_form.qwen3-1.7b/english = 43.18634009361267
provenance.config.seconds_per_model_form.qwen3-1.7b/native = 65.9120557308197
provenance.config.seconds_per_model_form.qwen3-1.7b/itrans = 52.16321563720703
provenance.config.seconds_per_model_form.qwen3-1.7b/lossy = 49.83175706863403
provenance.git_commit = "81d420c0666f561831ae1024ecc85b18ba6ce4bb-dirty"
provenance.timestamp_utc = "2026-10-14T17:04:21+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0b_familiarity.py", "--models", "qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b", "--forms", "english", "native", "itrans", "lossy", "--tag", "gate1a"]
informative_cells = ["gemma4-e2b/sentiment", "gemma4-e2b/xnli", "qwen2.5-1.5b/xnli", "qwen3-1.7b/sentiment", "qwen3-1.7b/xnli", "qwen3.5-2b/sentiment", "qwen3.5-2b/xnli", "sarvam-1/sentiment", "sarvam-1/xnli"]
P3_lossy_lt_itrans = false
P3_parts.all_cells_lossy_below_itrans = false
P3_parts.fraction_significant = 0.0
P3_parts.n_cells = 9
P1_familiarity_dominates = "pending (natural form not scored)"
P2_fragmentation_also_matters = "pending (natural form not scored)"
`````

#### `results/e0b_familiarity/gate1a_v2/accuracy.csv` (6,183 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

| model | task | form | n | chance | acc_cal | acc_cal_ci_low | acc_cal_ci_high | constant_label_rate_cal | acc_raw | acc_raw_ci_low | acc_raw_ci_high | constant_label_rate_raw | acc_na | acc_na_ci_low | acc_na_ci_high | constant_label_rate_na | acc_avg3 | acc_avg3_ci_low | acc_avg3_ci_high | constant_label_rate_avg3 | tokens_per_word |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 1.2214038128249567 |
| gemma4-e2b | sentiment | itrans | 200 | 0.5 | 0.755 | 0.695 | 0.81 | 0.685 | 0.75 | 0.69 | 0.81 | 0.67 | 0.765 | 0.705 | 0.82 | 0.615 | 0.755 | 0.695 | 0.81 | 0.685 | 3.943434935521688 |
| gemma4-e2b | sentiment | lossy | 200 | 0.5 | 0.79 | 0.73 | 0.845 | 0.65 | 0.79 | 0.73 | 0.845 | 0.65 | 0.785 | 0.725 | 0.84 | 0.625 | 0.79 | 0.73 | 0.845 | 0.65 | 3.2110199296600235 |
| gemma4-e2b | sentiment | native | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 3.0767878077373974 |
| gemma4-e2b | xnli | english | 200 | 0.3333333333333333 | 0.735 | 0.675 | 0.795 | 0.405 | 0.735 | 0.675 | 0.795 | 0.405 | 0.6 | 0.53 | 0.67 | 0.56 | 0.63 | 0.565 | 0.695 | 0.565 | 1.2397307559544357 |
| gemma4-e2b | xnli | itrans | 200 | 0.3333333333333333 | 0.41 | 0.34 | 0.48 | 0.87 | 0.41 | 0.34 | 0.48 | 0.87 | 0.435 | 0.365 | 0.505 | 0.6 | 0.445 | 0.375 | 0.51 | 0.68 | 3.9604674291397313 |
| gemma4-e2b | xnli | lossy | 200 | 0.3333333333333333 | 0.4 | 0.335 | 0.47 | 0.84 | 0.4 | 0.335 | 0.47 | 0.84 | 0.395 | 0.33 | 0.46 | 0.78 | 0.375 | 0.31 | 0.44 | 0.835 | 3.2031327697662855 |
| gemma4-e2b | xnli | native | 200 | 0.3333333333333333 | 0.545 | 0.475 | 0.615 | 0.595 | 0.545 | 0.475 | 0.615 | 0.595 | 0.465 | 0.395 | 0.535 | 0.615 | 0.5 | 0.43 | 0.57 | 0.59 | 3.1397314768771754 |
| qwen2.5-1.5b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.52 | 0.45 | 0.59 | 0.98 | 0.88 | 0.835 | 0.925 | 0.62 | 1.231369150779896 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 0.5 | 0.495 | 0.425 | 0.565 | 0.995 | 0.495 | 0.425 | 0.565 | 0.995 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 | 4.22538100820633 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 0.5 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 | 3.5679953106682296 |
| qwen2.5-1.5b | sentiment | native | 200 | 0.5 | 0.705 | 0.64 | 0.765 | 0.625 | 0.705 | 0.64 | 0.765 | 0.625 | 0.505 | 0.435 | 0.575 | 0.995 | 0.615 | 0.545 | 0.68 | 0.815 | 11.985638921453694 |
| qwen2.5-1.5b | xnli | english | 200 | 0.3333333333333333 | 0.825 | 0.77 | 0.875 | 0.38 | 0.795 | 0.735 | 0.85 | 0.45 | 0.785 | 0.73 | 0.84 | 0.49 | 0.825 | 0.77 | 0.875 | 0.38 | 1.2469796341042458 |
| qwen2.5-1.5b | xnli | itrans | 200 | 0.3333333333333333 | 0.32 | 0.255 | 0.385 | 0.67 | 0.375 | 0.31 | 0.445 | 0.845 | 0.325 | 0.26 | 0.39 | 0.965 | 0.32 | 0.255 | 0.385 | 0.67 | 4.25161611138737 |
| qwen2.5-1.5b | xnli | lossy | 200 | 0.3333333333333333 | 0.325 | 0.26 | 0.39 | 0.75 | 0.375 | 0.31 | 0.445 | 0.84 | 0.33 | 0.265 | 0.395 | 0.955 | 0.325 | 0.26 | 0.39 | 0.75 | 3.5532073595226255 |
| qwen2.5-1.5b | xnli | native | 200 | 0.3333333333333333 | 0.4 | 0.33 | 0.465 | 0.86 | 0.51 | 0.445 | 0.58 | 0.48 | 0.345 | 0.28 | 0.41 | 0.965 | 0.4 | 0.33 | 0.465 | 0.86 | 11.79860765788165 |
| qwen3-1.7b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 1.231369150779896 |
| qwen3-1.7b | sentiment | itrans | 200 | 0.5 | 0.535 | 0.465 | 0.605 | 0.645 | 0.58 | 0.51 | 0.645 | 0.68 | 0.54 | 0.47 | 0.61 | 0.85 | 0.535 | 0.465 | 0.605 | 0.645 | 4.22538100820633 |
| qwen3-1.7b | sentiment | lossy | 200 | 0.5 | 0.57 | 0.5 | 0.64 | 0.68 | 0.575 | 0.505 | 0.64 | 0.715 | 0.52 | 0.45 | 0.59 | 0.91 | 0.57 | 0.5 | 0.64 | 0.68 | 3.5679953106682296 |
| qwen3-1.7b | sentiment | native | 200 | 0.5 | 0.835 | 0.78 | 0.885 | 0.595 | 0.865 | 0.815 | 0.91 | 0.525 | 0.79 | 0.73 | 0.845 | 0.68 | 0.835 | 0.78 | 0.885 | 0.595 | 11.985638921453694 |
| qwen3-1.7b | xnli | english | 200 | 0.3333333333333333 | 0.575 | 0.505 | 0.645 | 0.71 | 0.615 | 0.545 | 0.68 | 0.53 | 0.54 | 0.47 | 0.61 | 0.765 | 0.575 | 0.505 | 0.645 | 0.71 | 1.2469796341042458 |
| qwen3-1.7b | xnli | itrans | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.37 | 0.305 | 0.44 | 0.8 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.995 | 4.25161611138737 |
| qwen3-1.7b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.415 | 0.345 | 0.485 | 0.795 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.995 | 3.5532073595226255 |
| qwen3-1.7b | xnli | native | 200 | 0.3333333333333333 | 0.445 | 0.375 | 0.515 | 0.85 | 0.43 | 0.36 | 0.5 | 0.61 | 0.425 | 0.355 | 0.495 | 0.89 | 0.445 | 0.375 | 0.515 | 0.85 | 11.79860765788165 |
| qwen3.5-2b | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.525 | 0.98 | 0.96 | 0.995 | 0.51 | 1.2268197573656845 |
| qwen3.5-2b | sentiment | itrans | 200 | 0.5 | 0.655 | 0.59 | 0.72 | 0.775 | 0.675 | 0.61 | 0.74 | 0.665 | 0.615 | 0.545 | 0.685 | 0.855 | 0.655 | 0.59 | 0.72 | 0.775 | 4.087631887456038 |
| qwen3.5-2b | sentiment | lossy | 200 | 0.5 | 0.68 | 0.615 | 0.74 | 0.72 | 0.675 | 0.61 | 0.735 | 0.645 | 0.645 | 0.58 | 0.71 | 0.815 | 0.68 | 0.615 | 0.74 | 0.72 | 3.3423212192262604 |
| qwen3.5-2b | sentiment | native | 200 | 0.5 | 0.735 | 0.67 | 0.795 | 0.755 | 0.785 | 0.725 | 0.84 | 0.705 | 0.675 | 0.61 | 0.74 | 0.815 | 0.735 | 0.67 | 0.795 | 0.755 | 5.235052754982415 |
| qwen3.5-2b | xnli | english | 200 | 0.3333333333333333 | 0.49 | 0.42 | 0.56 | 0.805 | 0.43 | 0.36 | 0.5 | 0.89 | 0.45 | 0.38 | 0.52 | 0.845 | 0.49 | 0.42 | 0.56 | 0.805 | 1.2424922333448394 |
| qwen3.5-2b | xnli | itrans | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 4.1282943809050225 |
| qwen3.5-2b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.99 | 0.34 | 0.275 | 0.405 | 0.995 | 0.335 | 0.27 | 0.4 | 0.99 | 0.335 | 0.27 | 0.4 | 0.99 | 3.3431128791645945 |
| qwen3.5-2b | xnli | native | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 5.230979612133267 |
| sarvam-1 | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.515 | 0.98 | 0.96 | 0.995 | 0.51 | 1.4204939341421143 |
| sarvam-1 | sentiment | itrans | 200 | 0.5 | 0.82 | 0.765 | 0.87 | 0.61 | 0.845 | 0.795 | 0.895 | 0.515 | 0.78 | 0.72 | 0.835 | 0.69 | 0.82 | 0.765 | 0.87 | 0.61 | 5.238569753810082 |
| sarvam-1 | sentiment | lossy | 200 | 0.5 | 0.895 | 0.85 | 0.935 | 0.575 | 0.91 | 0.87 | 0.95 | 0.51 | 0.86 | 0.81 | 0.905 | 0.63 | 0.895 | 0.85 | 0.935 | 0.575 | 4.357561547479484 |
| sarvam-1 | sentiment | native | 200 | 0.5 | 0.955 | 0.925 | 0.98 | 0.505 | 0.96 | 0.93 | 0.985 | 0.53 | 0.96 | 0.93 | 0.985 | 0.51 | 0.955 | 0.925 | 0.98 | 0.505 | 2.2708089097303636 |
| sarvam-1 | xnli | english | 200 | 0.3333333333333333 | 0.55 | 0.48 | 0.62 | 0.545 | 0.53 | 0.46 | 0.6 | 0.63 | 0.475 | 0.405 | 0.545 | 0.655 | 0.55 | 0.48 | 0.62 | 0.545 | 1.4326889886089058 |
| sarvam-1 | xnli | itrans | 200 | 0.3333333333333333 | 0.385 | 0.32 | 0.455 | 0.795 | 0.385 | 0.32 | 0.455 | 0.8 | 0.37 | 0.3 | 0.44 | 0.865 | 0.385 | 0.32 | 0.455 | 0.795 | 5.226255594231725 |
| sarvam-1 | xnli | lossy | 200 | 0.3333333333333333 | 0.47 | 0.4 | 0.54 | 0.58 | 0.46 | 0.39 | 0.53 | 0.595 | 0.375 | 0.31 | 0.44 | 0.905 | 0.47 | 0.4 | 0.54 | 0.58 | 4.335405271009448 |
| sarvam-1 | xnli | native | 200 | 0.3333333333333333 | 0.515 | 0.445 | 0.585 | 0.6 | 0.52 | 0.45 | 0.59 | 0.61 | 0.455 | 0.385 | 0.525 | 0.865 | 0.515 | 0.445 | 0.585 | 0.6 | 2.1452013923421185 |

#### `results/e0b_familiarity/gate1a_v2/calibration_fallback.csv` (410 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

| model | task | english_raw | english_avg3 | use_raw |
|---|---|---|---|---|
| gemma4-e2b | sentiment | 0.985 | 0.985 | False |
| gemma4-e2b | xnli | 0.735 | 0.63 | True |
| qwen2.5-1.5b | sentiment | 0.985 | 0.88 | True |
| qwen2.5-1.5b | xnli | 0.795 | 0.825 | False |
| qwen3-1.7b | sentiment | 0.985 | 0.985 | False |
| qwen3-1.7b | xnli | 0.615 | 0.575 | False |
| qwen3.5-2b | sentiment | 0.975 | 0.98 | False |
| qwen3.5-2b | xnli | 0.43 | 0.49 | False |
| sarvam-1 | sentiment | 0.975 | 0.98 | False |
| sarvam-1 | xnli | 0.53 | 0.55 | False |

#### `results/e0b_familiarity/gate1a_v2/fertility.csv` (2,001 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

| model | task | form | n_texts | tokens_per_word |
|---|---|---|---|---|
| qwen2.5-1.5b | xnli | english | 400 | 1.2469796341042458 |
| qwen2.5-1.5b | sentiment | english | 200 | 1.231369150779896 |
| qwen2.5-1.5b | xnli | native | 400 | 11.79860765788165 |
| qwen2.5-1.5b | sentiment | native | 200 | 11.985638921453694 |
| qwen2.5-1.5b | xnli | itrans | 400 | 4.25161611138737 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen2.5-1.5b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen3.5-2b | xnli | english | 400 | 1.2424922333448394 |
| qwen3.5-2b | sentiment | english | 200 | 1.2268197573656845 |
| qwen3.5-2b | xnli | native | 400 | 5.230979612133267 |
| qwen3.5-2b | sentiment | native | 200 | 5.235052754982415 |
| qwen3.5-2b | xnli | itrans | 400 | 4.1282943809050225 |
| qwen3.5-2b | sentiment | itrans | 200 | 4.087631887456038 |
| qwen3.5-2b | xnli | lossy | 400 | 3.3431128791645945 |
| qwen3.5-2b | sentiment | lossy | 200 | 3.3423212192262604 |
| sarvam-1 | xnli | english | 400 | 1.4326889886089058 |
| sarvam-1 | sentiment | english | 200 | 1.4204939341421143 |
| sarvam-1 | xnli | native | 400 | 2.1452013923421185 |
| sarvam-1 | sentiment | native | 200 | 2.2708089097303636 |
| sarvam-1 | xnli | itrans | 400 | 5.226255594231725 |
| sarvam-1 | sentiment | itrans | 200 | 5.238569753810082 |
| sarvam-1 | xnli | lossy | 400 | 4.335405271009448 |
| sarvam-1 | sentiment | lossy | 200 | 4.357561547479484 |
| gemma4-e2b | xnli | english | 400 | 1.2397307559544357 |
| gemma4-e2b | sentiment | english | 200 | 1.2214038128249567 |
| gemma4-e2b | xnli | native | 400 | 3.1397314768771754 |
| gemma4-e2b | sentiment | native | 200 | 3.0767878077373974 |
| gemma4-e2b | xnli | itrans | 400 | 3.9604674291397313 |
| gemma4-e2b | sentiment | itrans | 200 | 3.943434935521688 |
| gemma4-e2b | xnli | lossy | 400 | 3.2031327697662855 |
| gemma4-e2b | sentiment | lossy | 200 | 3.2110199296600235 |
| qwen3-1.7b | xnli | english | 400 | 1.2469796341042458 |
| qwen3-1.7b | sentiment | english | 200 | 1.231369150779896 |
| qwen3-1.7b | xnli | native | 400 | 11.79860765788165 |
| qwen3-1.7b | sentiment | native | 200 | 11.985638921453694 |
| qwen3-1.7b | xnli | itrans | 400 | 4.25161611138737 |
| qwen3-1.7b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen3-1.7b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen3-1.7b | sentiment | lossy | 200 | 3.5679953106682296 |

#### `results/e0b_familiarity/gate1a_v2/mcnemar.csv` (1,070 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

| model | task | a | b | acc_a | acc_b | n | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | lossy | itrans | 0.79 | 0.755 | 200 | 0.03500000000000003 | 18 | 11 | 0.26493089646101 | 1.0 | False |
| gemma4-e2b | xnli | lossy | itrans | 0.4 | 0.41 | 200 | -0.009999999999999953 | 11 | 13 | 0.8388197422027588 | 1.0 | False |
| qwen2.5-1.5b | sentiment | lossy | itrans | 0.5 | 0.495 | 200 | 0.0050000000000000044 | 4 | 3 | 1.0 | 1.0 | False |
| qwen2.5-1.5b | xnli | lossy | itrans | 0.325 | 0.32 | 200 | 0.0050000000000000044 | 18 | 17 | 0.9999999999999998 | 1.0 | False |
| qwen3-1.7b | sentiment | lossy | itrans | 0.57 | 0.535 | 200 | 0.03499999999999992 | 32 | 25 | 0.42704285650325524 | 1.0 | False |
| qwen3-1.7b | xnli | lossy | itrans | 0.335 | 0.335 | 200 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| qwen3.5-2b | sentiment | lossy | itrans | 0.68 | 0.655 | 200 | 0.025000000000000022 | 23 | 18 | 0.5327092552361137 | 1.0 | False |
| qwen3.5-2b | xnli | lossy | itrans | 0.335 | 0.34 | 200 | -0.0050000000000000044 | 0 | 1 | 1.0 | 1.0 | False |
| sarvam-1 | sentiment | lossy | itrans | 0.895 | 0.82 | 200 | 0.07500000000000007 | 21 | 6 | 0.005924612283706665 | 0.05924612283706665 | False |
| sarvam-1 | xnli | lossy | itrans | 0.47 | 0.385 | 200 | 0.08499999999999996 | 29 | 12 | 0.011507789735333063 | 0.10357010761799756 | False |

#### `results/e0b_familiarity/gate1a_v2/mcnemar_exploratory.csv` (1,229 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

| model | task | a | b | acc_a | acc_b | n | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | itrans | native | 0.755 | 0.985 | 200 | -0.22999999999999998 | 1 | 47 | 3.481659405224491e-13 | 3.481659405224491e-12 | True |
| gemma4-e2b | xnli | itrans | native | 0.41 | 0.545 | 200 | -0.13500000000000006 | 14 | 41 | 0.00035528111863147854 | 0.0017764055931573928 | True |
| qwen2.5-1.5b | sentiment | itrans | native | 0.495 | 0.705 | 200 | -0.20999999999999996 | 16 | 58 | 9.674891137601897e-07 | 7.739912910081517e-06 | True |
| qwen2.5-1.5b | xnli | itrans | native | 0.32 | 0.4 | 200 | -0.08000000000000002 | 18 | 34 | 0.03648340000835981 | 0.07768824537970431 | False |
| qwen3-1.7b | sentiment | itrans | native | 0.535 | 0.835 | 200 | -0.29999999999999993 | 14 | 74 | 5.0891941127085865e-11 | 4.580274701437728e-10 | True |
| qwen3-1.7b | xnli | itrans | native | 0.335 | 0.445 | 200 | -0.10999999999999999 | 3 | 25 | 2.744048833847046e-05 | 0.00016464293003082275 | True |
| qwen3.5-2b | sentiment | itrans | native | 0.655 | 0.735 | 200 | -0.07999999999999996 | 15 | 31 | 0.02589608179323477 | 0.07768824537970431 | False |
| qwen3.5-2b | xnli | itrans | native | 0.34 | 0.34 | 200 | 0.0 | 0 | 0 | 1.0 | 1.0 | False |
| sarvam-1 | sentiment | itrans | native | 0.82 | 0.955 | 200 | -0.135 | 6 | 33 | 1.429926123819314e-05 | 0.00010009482866735198 | True |
| sarvam-1 | xnli | itrans | native | 0.385 | 0.515 | 200 | -0.13 | 14 | 40 | 0.0005354355028570622 | 0.002141742011428249 | True |

#### `results/e0b_familiarity/gate1a_v2/summary.json` (46,016 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

`````text
provenance.config.models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
provenance.config.forms = ["english", "native", "itrans", "lossy"]
provenance.config.calibration = "primary: mean of content-free N/A, '', [MASK]; raw fallback if English drops > 5 pts"
provenance.config.calibration_fallback_rows[0].model = "gemma4-e2b"
provenance.config.calibration_fallback_rows[0].task = "xnli"
provenance.config.calibration_fallback_rows[1].model = "qwen2.5-1.5b"
provenance.config.calibration_fallback_rows[1].task = "sentiment"
provenance.config.natural_items_excluded_defective = 0
provenance.config.templates = "e0_{xnli,sentiment}_v1"
provenance.config.n_per_task = 200
provenance.config.seed = 0
provenance.config.bos = "always prepended"
provenance.config.seconds_per_model_form.qwen2.5-1.5b/english = 36.487061977386475
provenance.config.seconds_per_model_form.qwen2.5-1.5b/native = 60.4139928817749
provenance.config.seconds_per_model_form.qwen2.5-1.5b/itrans = 46.802143573760986
provenance.config.seconds_per_model_form.qwen2.5-1.5b/lossy = 49.93747925758362
provenance.config.seconds_per_model_form.qwen3.5-2b/english = 100.45982670783997
provenance.config.seconds_per_model_form.qwen3.5-2b/native = 137.80759501457214
provenance.config.seconds_per_model_form.qwen3.5-2b/itrans = 135.9841856956482
provenance.config.seconds_per_model_form.qwen3.5-2b/lossy = 107.09859132766724
provenance.config.seconds_per_model_form.sarvam-1/english = 52.38592600822449
provenance.config.seconds_per_model_form.sarvam-1/native = 54.95457744598389
provenance.config.seconds_per_model_form.sarvam-1/itrans = 60.9882435798645
provenance.config.seconds_per_model_form.sarvam-1/lossy = 57.89579892158508
provenance.config.seconds_per_model_form.gemma4-e2b/english = 89.42716455459595
provenance.config.seconds_per_model_form.gemma4-e2b/native = 94.79906296730042
provenance.config.seconds_per_model_form.gemma4-e2b/itrans = 97.28406596183777
provenance.config.seconds_per_model_form.gemma4-e2b/lossy = 92.6928346157074
provenance.config.seconds_per_model_form.qwen3-1.7b/english = 43.18634009361267
provenance.config.seconds_per_model_form.qwen3-1.7b/native = 65.9120557308197
provenance.config.seconds_per_model_form.qwen3-1.7b/itrans = 52.16321563720703
provenance.config.seconds_per_model_form.qwen3-1.7b/lossy = 49.83175706863403
provenance.git_commit = "d45dc1bf9e66523a94b2d9b731201f576803081f-dirty"
provenance.timestamp_utc = "2026-10-14T18:52:08+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0b_familiarity.py", "--models", "qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b", "--forms", "english", "native", "itrans", "lossy", "--tag", "gate1a_v2"]
calibration_fallback[0].model = "gemma4-e2b"
calibration_fallback[0].task = "sentiment"
calibration_fallback[0].english_raw = 0.985
calibration_fallback[0].english_avg3 = 0.985
calibration_fallback[0].use_raw = false
calibration_fallback[1].model = "gemma4-e2b"
calibration_fallback[1].task = "xnli"
calibration_fallback[1].english_raw = 0.735
calibration_fallback[1].english_avg3 = 0.63
calibration_fallback[1].use_raw = true
calibration_fallback[2].model = "qwen2.5-1.5b"
calibration_fallback[2].task = "sentiment"
calibration_fallback[2].english_raw = 0.985
calibration_fallback[2].english_avg3 = 0.88
calibration_fallback[2].use_raw = true
calibration_fallback[3].model = "qwen2.5-1.5b"
calibration_fallback[3].task = "xnli"
calibration_fallback[3].english_raw = 0.795
calibration_fallback[3].english_avg3 = 0.825
calibration_fallback[3].use_raw = false
calibration_fallback[4].model = "qwen3-1.7b"
calibration_fallback[4].task = "sentiment"
calibration_fallback[4].english_raw = 0.985
calibration_fallback[4].english_avg3 = 0.985
calibration_fallback[4].use_raw = false
calibration_fallback[5].model = "qwen3-1.7b"
calibration_fallback[5].task = "xnli"
calibration_fallback[5].english_raw = 0.615
calibration_fallback[5].english_avg3 = 0.575
calibration_fallback[5].use_raw = false
calibration_fallback[6].model = "qwen3.5-2b"
calibration_fallback[6].task = "sentiment"
calibration_fallback[6].english_raw = 0.975
calibration_fallback[6].english_avg3 = 0.98
calibration_fallback[6].use_raw = false
calibration_fallback[7].model = "qwen3.5-2b"
calibration_fallback[7].task = "xnli"
calibration_fallback[7].english_raw = 0.43
calibration_fallback[7].english_avg3 = 0.49
calibration_fallback[7].use_raw = false
calibration_fallback[8].model = "sarvam-1"
calibration_fallback[8].task = "sentiment"
calibration_fallback[8].english_raw = 0.975
calibration_fallback[8].english_avg3 = 0.98
calibration_fallback[8].use_raw = false
calibration_fallback[9].model = "sarvam-1"
calibration_fallback[9].task = "xnli"
calibration_fallback[9].english_raw = 0.53
calibration_fallback[9].english_avg3 = 0.55
calibration_fallback[9].use_raw = false
accuracy[0].model = "gemma4-e2b"
accuracy[0].task = "sentiment"
accuracy[0].form = "english"
accuracy[0].n = 200
accuracy[0].chance = 0.5
accuracy[0].acc_cal = 0.985
accuracy[0].acc_cal_ci_low = 0.965
accuracy[0].acc_cal_ci_high = 1.0
accuracy[0].constant_label_rate_cal = 0.505
accuracy[0].acc_raw = 0.985
accuracy[0].acc_raw_ci_low = 0.965
accuracy[0].acc_raw_ci_high = 1.0
accuracy[0].constant_label_rate_raw = 0.505
accuracy[0].acc_na = 0.98
accuracy[0].acc_na_ci_low = 0.96
accuracy[0].acc_na_ci_high = 0.995
accuracy[0].constant_label_rate_na = 0.5
accuracy[0].acc_avg3 = 0.985
accuracy[0].acc_avg3_ci_low = 0.965
accuracy[0].acc_avg3_ci_high = 1.0
accuracy[0].constant_label_rate_avg3 = 0.505
accuracy[0].tokens_per_word = 1.2214038128249567
accuracy[1].model = "gemma4-e2b"
accuracy[1].task = "sentiment"
accuracy[1].form = "itrans"
accuracy[1].n = 200
accuracy[1].chance = 0.5
accuracy[1].acc_cal = 0.755
accuracy[1].acc_cal_ci_low = 0.695
accuracy[1].acc_cal_ci_high = 0.81
accuracy[1].constant_label_rate_cal = 0.685
accuracy[1].acc_raw = 0.75
accuracy[1].acc_raw_ci_low = 0.69
accuracy[1].acc_raw_ci_high = 0.81
accuracy[1].constant_label_rate_raw = 0.67
accuracy[1].acc_na = 0.765
accuracy[1].acc_na_ci_low = 0.705
accuracy[1].acc_na_ci_high = 0.82
accuracy[1].constant_label_rate_na = 0.615
accuracy[1].acc_avg3 = 0.755
accuracy[1].acc_avg3_ci_low = 0.695
accuracy[1].acc_avg3_ci_high = 0.81
accuracy[1].constant_label_rate_avg3 = 0.685
accuracy[1].tokens_per_word = 3.943434935521688
accuracy[2].model = "gemma4-e2b"
accuracy[2].task = "sentiment"
accuracy[2].form = "lossy"
accuracy[2].n = 200
accuracy[2].chance = 0.5
accuracy[2].acc_cal = 0.79
accuracy[2].acc_cal_ci_low = 0.73
accuracy[2].acc_cal_ci_high = 0.845
accuracy[2].constant_label_rate_cal = 0.65
accuracy[2].acc_raw = 0.79
accuracy[2].acc_raw_ci_low = 0.73
accuracy[2].acc_raw_ci_high = 0.845
accuracy[2].constant_label_rate_raw = 0.65
accuracy[2].acc_na = 0.785
accuracy[2].acc_na_ci_low = 0.725
accuracy[2].acc_na_ci_high = 0.84
accuracy[2].constant_label_rate_na = 0.625
accuracy[2].acc_avg3 = 0.79
accuracy[2].acc_avg3_ci_low = 0.73
accuracy[2].acc_avg3_ci_high = 0.845
accuracy[2].constant_label_rate_avg3 = 0.65
accuracy[2].tokens_per_word = 3.2110199296600235
accuracy[3].model = "gemma4-e2b"
accuracy[3].task = "sentiment"
accuracy[3].form = "native"
accuracy[3].n = 200
accuracy[3].chance = 0.5
accuracy[3].acc_cal = 0.985
accuracy[3].acc_cal_ci_low = 0.965
accuracy[3].acc_cal_ci_high = 1.0
accuracy[3].constant_label_rate_cal = 0.505
accuracy[3].acc_raw = 0.985
accuracy[3].acc_raw_ci_low = 0.965
accuracy[3].acc_raw_ci_high = 1.0
accuracy[3].constant_label_rate_raw = 0.505
accuracy[3].acc_na = 0.985
accuracy[3].acc_na_ci_low = 0.965
accuracy[3].acc_na_ci_high = 1.0
accuracy[3].constant_label_rate_na = 0.505
accuracy[3].acc_avg3 = 0.985
accuracy[3].acc_avg3_ci_low = 0.965
accuracy[3].acc_avg3_ci_high = 1.0
accuracy[3].constant_label_rate_avg3 = 0.505
accuracy[3].tokens_per_word = 3.0767878077373974
accuracy[4].model = "gemma4-e2b"
accuracy[4].task = "xnli"
accuracy[4].form = "english"
accuracy[4].n = 200
accuracy[4].chance = 0.3333333333333333
accuracy[4].acc_cal = 0.735
accuracy[4].acc_cal_ci_low = 0.675
accuracy[4].acc_cal_ci_high = 0.795
accuracy[4].constant_label_rate_cal = 0.405
accuracy[4].acc_raw = 0.735
accuracy[4].acc_raw_ci_low = 0.675
accuracy[4].acc_raw_ci_high = 0.795
accuracy[4].constant_label_rate_raw = 0.405
accuracy[4].acc_na = 0.6
accuracy[4].acc_na_ci_low = 0.53
accuracy[4].acc_na_ci_high = 0.67
accuracy[4].constant_label_rate_na = 0.56
accuracy[4].acc_avg3 = 0.63
accuracy[4].acc_avg3_ci_low = 0.565
accuracy[4].acc_avg3_ci_high = 0.695
accuracy[4].constant_label_rate_avg3 = 0.565
accuracy[4].tokens_per_word = 1.2397307559544357
accuracy[5].model = "gemma4-e2b"
accuracy[5].task = "xnli"
accuracy[5].form = "itrans"
accuracy[5].n = 200
accuracy[5].chance = 0.3333333333333333
accuracy[5].acc_cal = 0.41
accuracy[5].acc_cal_ci_low = 0.34
accuracy[5].acc_cal_ci_high = 0.48
accuracy[5].constant_label_rate_cal = 0.87
accuracy[5].acc_raw = 0.41
accuracy[5].acc_raw_ci_low = 0.34
accuracy[5].acc_raw_ci_high = 0.48
accuracy[5].constant_label_rate_raw = 0.87
accuracy[5].acc_na = 0.435
accuracy[5].acc_na_ci_low = 0.365
accuracy[5].acc_na_ci_high = 0.505
accuracy[5].constant_label_rate_na = 0.6
accuracy[5].acc_avg3 = 0.445
accuracy[5].acc_avg3_ci_low = 0.375
accuracy[5].acc_avg3_ci_high = 0.51
accuracy[5].constant_label_rate_avg3 = 0.68
accuracy[5].tokens_per_word = 3.9604674291397313
accuracy[6].model = "gemma4-e2b"
accuracy[6].task = "xnli"
accuracy[6].form = "lossy"
accuracy[6].n = 200
accuracy[6].chance = 0.3333333333333333
accuracy[6].acc_cal = 0.4
accuracy[6].acc_cal_ci_low = 0.335
accuracy[6].acc_cal_ci_high = 0.47
accuracy[6].constant_label_rate_cal = 0.84
accuracy[6].acc_raw = 0.4
accuracy[6].acc_raw_ci_low = 0.335
accuracy[6].acc_raw_ci_high = 0.47
accuracy[6].constant_label_rate_raw = 0.84
accuracy[6].acc_na = 0.395
accuracy[6].acc_na_ci_low = 0.33
accuracy[6].acc_na_ci_high = 0.46
accuracy[6].constant_label_rate_na = 0.78
accuracy[6].acc_avg3 = 0.375
accuracy[6].acc_avg3_ci_low = 0.31
accuracy[6].acc_avg3_ci_high = 0.44
accuracy[6].constant_label_rate_avg3 = 0.835
accuracy[6].tokens_per_word = 3.2031327697662855
accuracy[7].model = "gemma4-e2b"
accuracy[7].task = "xnli"
accuracy[7].form = "native"
accuracy[7].n = 200
accuracy[7].chance = 0.3333333333333333
accuracy[7].acc_cal = 0.545
accuracy[7].acc_cal_ci_low = 0.475
accuracy[7].acc_cal_ci_high = 0.615
accuracy[7].constant_label_rate_cal = 0.595
accuracy[7].acc_raw = 0.545
accuracy[7].acc_raw_ci_low = 0.475
accuracy[7].acc_raw_ci_high = 0.615
accuracy[7].constant_label_rate_raw = 0.595
accuracy[7].acc_na = 0.465
accuracy[7].acc_na_ci_low = 0.395
accuracy[7].acc_na_ci_high = 0.535
accuracy[7].constant_label_rate_na = 0.615
accuracy[7].acc_avg3 = 0.5
accuracy[7].acc_avg3_ci_low = 0.43
accuracy[7].acc_avg3_ci_high = 0.57
accuracy[7].constant_label_rate_avg3 = 0.59
accuracy[7].tokens_per_word = 3.1397314768771754
accuracy[8].model = "qwen2.5-1.5b"
accuracy[8].task = "sentiment"
accuracy[8].form = "english"
accuracy[8].n = 200
accuracy[8].chance = 0.5
accuracy[8].acc_cal = 0.985
accuracy[8].acc_cal_ci_low = 0.965
accuracy[8].acc_cal_ci_high = 1.0
accuracy[8].constant_label_rate_cal = 0.515
accuracy[8].acc_raw = 0.985
accuracy[8].acc_raw_ci_low = 0.965
accuracy[8].acc_raw_ci_high = 1.0
accuracy[8].constant_label_rate_raw = 0.515
accuracy[8].acc_na = 0.52
accuracy[8].acc_na_ci_low = 0.45
accuracy[8].acc_na_ci_high = 0.59
accuracy[8].constant_label_rate_na = 0.98
accuracy[8].acc_avg3 = 0.88
accuracy[8].acc_avg3_ci_low = 0.835
accuracy[8].acc_avg3_ci_high = 0.925
accuracy[8].constant_label_rate_avg3 = 0.62
accuracy[8].tokens_per_word = 1.231369150779896
accuracy[9].model = "qwen2.5-1.5b"
accuracy[9].task = "sentiment"
accuracy[9].form = "itrans"
accuracy[9].n = 200
accuracy[9].chance = 0.5
accuracy[9].acc_cal = 0.495
accuracy[9].acc_cal_ci_low = 0.425
accuracy[9].acc_cal_ci_high = 0.565
accuracy[9].constant_label_rate_cal = 0.995
accuracy[9].acc_raw = 0.495
accuracy[9].acc_raw_ci_low = 0.425
accuracy[9].acc_raw_ci_high = 0.565
accuracy[9].constant_label_rate_raw = 0.995
accuracy[9].acc_na = 0.5
accuracy[9].acc_na_ci_low = 0.43
accuracy[9].acc_na_ci_high = 0.57
accuracy[9].constant_label_rate_na = 1.0
accuracy[9].acc_avg3 = 0.5
accuracy[9].acc_avg3_ci_low = 0.43
accuracy[9].acc_avg3_ci_high = 0.57
accuracy[9].constant_label_rate_avg3 = 1.0
accuracy[9].tokens_per_word = 4.22538100820633
accuracy[10].model = "qwen2.5-1.5b"
accuracy[10].task = "sentiment"
accuracy[10].form = "lossy"
accuracy[10].n = 200
accuracy[10].chance = 0.5
accuracy[10].acc_cal = 0.5
accuracy[10].acc_cal_ci_low = 0.43
accuracy[10].acc_cal_ci_high = 0.57
accuracy[10].constant_label_rate_cal = 0.97
accuracy[10].acc_raw = 0.5
accuracy[10].acc_raw_ci_low = 0.43
accuracy[10].acc_raw_ci_high = 0.57
accuracy[10].constant_label_rate_raw = 0.97
accuracy[10].acc_na = 0.5
accuracy[10].acc_na_ci_low = 0.43
accuracy[10].acc_na_ci_high = 0.57
accuracy[10].constant_label_rate_na = 1.0
accuracy[10].acc_avg3 = 0.5
accuracy[10].acc_avg3_ci_low = 0.43
accuracy[10].acc_avg3_ci_high = 0.57
accuracy[10].constant_label_rate_avg3 = 1.0
accuracy[10].tokens_per_word = 3.5679953106682296
accuracy[11].model = "qwen2.5-1.5b"
accuracy[11].task = "sentiment"
accuracy[11].form = "native"
accuracy[11].n = 200
accuracy[11].chance = 0.5
accuracy[11].acc_cal = 0.705
accuracy[11].acc_cal_ci_low = 0.64
accuracy[11].acc_cal_ci_high = 0.765
accuracy[11].constant_label_rate_cal = 0.625
accuracy[11].acc_raw = 0.705
accuracy[11].acc_raw_ci_low = 0.64
accuracy[11].acc_raw_ci_high = 0.765
accuracy[11].constant_label_rate_raw = 0.625
accuracy[11].acc_na = 0.505
accuracy[11].acc_na_ci_low = 0.435
accuracy[11].acc_na_ci_high = 0.575
accuracy[11].constant_label_rate_na = 0.995
accuracy[11].acc_avg3 = 0.615
accuracy[11].acc_avg3_ci_low = 0.545
accuracy[11].acc_avg3_ci_high = 0.68
accuracy[11].constant_label_rate_avg3 = 0.815
accuracy[11].tokens_per_word = 11.985638921453694
accuracy[12].model = "qwen2.5-1.5b"
accuracy[12].task = "xnli"
accuracy[12].form = "english"
accuracy[12].n = 200
accuracy[12].chance = 0.3333333333333333
accuracy[12].acc_cal = 0.825
accuracy[12].acc_cal_ci_low = 0.77
accuracy[12].acc_cal_ci_high = 0.875
accuracy[12].constant_label_rate_cal = 0.38
accuracy[12].acc_raw = 0.795
accuracy[12].acc_raw_ci_low = 0.735
accuracy[12].acc_raw_ci_high = 0.85
accuracy[12].constant_label_rate_raw = 0.45
accuracy[12].acc_na = 0.785
accuracy[12].acc_na_ci_low = 0.73
accuracy[12].acc_na_ci_high = 0.84
accuracy[12].constant_label_rate_na = 0.49
accuracy[12].acc_avg3 = 0.825
accuracy[12].acc_avg3_ci_low = 0.77
accuracy[12].acc_avg3_ci_high = 0.875
accuracy[12].constant_label_rate_avg3 = 0.38
accuracy[12].tokens_per_word = 1.2469796341042458
accuracy[13].model = "qwen2.5-1.5b"
accuracy[13].task = "xnli"
accuracy[13].form = "itrans"
accuracy[13].n = 200
accuracy[13].chance = 0.3333333333333333
accuracy[13].acc_cal = 0.32
accuracy[13].acc_cal_ci_low = 0.255
accuracy[13].acc_cal_ci_high = 0.385
accuracy[13].constant_label_rate_cal = 0.67
accuracy[13].acc_raw = 0.375
accuracy[13].acc_raw_ci_low = 0.31
accuracy[13].acc_raw_ci_high = 0.445
accuracy[13].constant_label_rate_raw = 0.845
accuracy[13].acc_na = 0.325
accuracy[13].acc_na_ci_low = 0.26
accuracy[13].acc_na_ci_high = 0.39
accuracy[13].constant_label_rate_na = 0.965
accuracy[13].acc_avg3 = 0.32
accuracy[13].acc_avg3_ci_low = 0.255
accuracy[13].acc_avg3_ci_high = 0.385
accuracy[13].constant_label_rate_avg3 = 0.67
accuracy[13].tokens_per_word = 4.25161611138737
accuracy[14].model = "qwen2.5-1.5b"
accuracy[14].task = "xnli"
accuracy[14].form = "lossy"
accuracy[14].n = 200
accuracy[14].chance = 0.3333333333333333
accuracy[14].acc_cal = 0.325
accuracy[14].acc_cal_ci_low = 0.26
accuracy[14].acc_cal_ci_high = 0.39
accuracy[14].constant_label_rate_cal = 0.75
accuracy[14].acc_raw = 0.375
accuracy[14].acc_raw_ci_low = 0.31
accuracy[14].acc_raw_ci_high = 0.445
accuracy[14].constant_label_rate_raw = 0.84
accuracy[14].acc_na = 0.33
accuracy[14].acc_na_ci_low = 0.265
accuracy[14].acc_na_ci_high = 0.395
accuracy[14].constant_label_rate_na = 0.955
accuracy[14].acc_avg3 = 0.325
accuracy[14].acc_avg3_ci_low = 0.26
accuracy[14].acc_avg3_ci_high = 0.39
accuracy[14].constant_label_rate_avg3 = 0.75
accuracy[14].tokens_per_word = 3.5532073595226255
accuracy[15].model = "qwen2.5-1.5b"
accuracy[15].task = "xnli"
accuracy[15].form = "native"
accuracy[15].n = 200
accuracy[15].chance = 0.3333333333333333
accuracy[15].acc_cal = 0.4
accuracy[15].acc_cal_ci_low = 0.33
accuracy[15].acc_cal_ci_high = 0.465
accuracy[15].constant_label_rate_cal = 0.86
accuracy[15].acc_raw = 0.51
accuracy[15].acc_raw_ci_low = 0.445
accuracy[15].acc_raw_ci_high = 0.58
accuracy[15].constant_label_rate_raw = 0.48
accuracy[15].acc_na = 0.345
accuracy[15].acc_na_ci_low = 0.28
accuracy[15].acc_na_ci_high = 0.41
accuracy[15].constant_label_rate_na = 0.965
accuracy[15].acc_avg3 = 0.4
accuracy[15].acc_avg3_ci_low = 0.33
accuracy[15].acc_avg3_ci_high = 0.465
accuracy[15].constant_label_rate_avg3 = 0.86
accuracy[15].tokens_per_word = 11.79860765788165
accuracy[16].model = "qwen3-1.7b"
accuracy[16].task = "sentiment"
accuracy[16].form = "english"
accuracy[16].n = 200
accuracy[16].chance = 0.5
accuracy[16].acc_cal = 0.985
accuracy[16].acc_cal_ci_low = 0.965
accuracy[16].acc_cal_ci_high = 1.0
accuracy[16].constant_label_rate_cal = 0.515
accuracy[16].acc_raw = 0.985
accuracy[16].acc_raw_ci_low = 0.965
accuracy[16].acc_raw_ci_high = 1.0
accuracy[16].constant_label_rate_raw = 0.515
accuracy[16].acc_na = 0.98
accuracy[16].acc_na_ci_low = 0.96
accuracy[16].acc_na_ci_high = 0.995
accuracy[16].constant_label_rate_na = 0.5
accuracy[16].acc_avg3 = 0.985
accuracy[16].acc_avg3_ci_low = 0.965
accuracy[16].acc_avg3_ci_high = 1.0
accuracy[16].constant_label_rate_avg3 = 0.515
accuracy[16].tokens_per_word = 1.231369150779896
accuracy[17].model = "qwen3-1.7b"
accuracy[17].task = "sentiment"
accuracy[17].form = "itrans"
accuracy[17].n = 200
accuracy[17].chance = 0.5
accuracy[17].acc_cal = 0.535
accuracy[17].acc_cal_ci_low = 0.465
accuracy[17].acc_cal_ci_high = 0.605
accuracy[17].constant_label_rate_cal = 0.645
accuracy[17].acc_raw = 0.58
accuracy[17].acc_raw_ci_low = 0.51
accuracy[17].acc_raw_ci_high = 0.645
accuracy[17].constant_label_rate_raw = 0.68
accuracy[17].acc_na = 0.54
accuracy[17].acc_na_ci_low = 0.47
accuracy[17].acc_na_ci_high = 0.61
accuracy[17].constant_label_rate_na = 0.85
accuracy[17].acc_avg3 = 0.535
accuracy[17].acc_avg3_ci_low = 0.465
accuracy[17].acc_avg3_ci_high = 0.605
accuracy[17].constant_label_rate_avg3 = 0.645
accuracy[17].tokens_per_word = 4.22538100820633
accuracy[18].model = "qwen3-1.7b"
accuracy[18].task = "sentiment"
accuracy[18].form = "lossy"
accuracy[18].n = 200
accuracy[18].chance = 0.5
accuracy[18].acc_cal = 0.57
accuracy[18].acc_cal_ci_low = 0.5
accuracy[18].acc_cal_ci_high = 0.64
accuracy[18].constant_label_rate_cal = 0.68
accuracy[18].acc_raw = 0.575
accuracy[18].acc_raw_ci_low = 0.505
accuracy[18].acc_raw_ci_high = 0.64
accuracy[18].constant_label_rate_raw = 0.715
accuracy[18].acc_na = 0.52
accuracy[18].acc_na_ci_low = 0.45
accuracy[18].acc_na_ci_high = 0.59
accuracy[18].constant_label_rate_na = 0.91
accuracy[18].acc_avg3 = 0.57
accuracy[18].acc_avg3_ci_low = 0.5
accuracy[18].acc_avg3_ci_high = 0.64
accuracy[18].constant_label_rate_avg3 = 0.68
accuracy[18].tokens_per_word = 3.5679953106682296
accuracy[19].model = "qwen3-1.7b"
accuracy[19].task = "sentiment"
accuracy[19].form = "native"
accuracy[19].n = 200
accuracy[19].chance = 0.5
accuracy[19].acc_cal = 0.835
accuracy[19].acc_cal_ci_low = 0.78
accuracy[19].acc_cal_ci_high = 0.885
accuracy[19].constant_label_rate_cal = 0.595
accuracy[19].acc_raw = 0.865
accuracy[19].acc_raw_ci_low = 0.815
accuracy[19].acc_raw_ci_high = 0.91
accuracy[19].constant_label_rate_raw = 0.525
accuracy[19].acc_na = 0.79
accuracy[19].acc_na_ci_low = 0.73
accuracy[19].acc_na_ci_high = 0.845
accuracy[19].constant_label_rate_na = 0.68
accuracy[19].acc_avg3 = 0.835
accuracy[19].acc_avg3_ci_low = 0.78
accuracy[19].acc_avg3_ci_high = 0.885
accuracy[19].constant_label_rate_avg3 = 0.595
accuracy[19].tokens_per_word = 11.985638921453694
accuracy[20].model = "qwen3-1.7b"
accuracy[20].task = "xnli"
accuracy[20].form = "english"
accuracy[20].n = 200
accuracy[20].chance = 0.3333333333333333
accuracy[20].acc_cal = 0.575
accuracy[20].acc_cal_ci_low = 0.505
accuracy[20].acc_cal_ci_high = 0.645
accuracy[20].constant_label_rate_cal = 0.71
accuracy[20].acc_raw = 0.615
accuracy[20].acc_raw_ci_low = 0.545
accuracy[20].acc_raw_ci_high = 0.68
accuracy[20].constant_label_rate_raw = 0.53
accuracy[20].acc_na = 0.54
accuracy[20].acc_na_ci_low = 0.47
accuracy[20].acc_na_ci_high = 0.61
accuracy[20].constant_label_rate_na = 0.765
accuracy[20].acc_avg3 = 0.575
accuracy[20].acc_avg3_ci_low = 0.505
accuracy[20].acc_avg3_ci_high = 0.645
accuracy[20].constant_label_rate_avg3 = 0.71
accuracy[20].tokens_per_word = 1.2469796341042458
accuracy[21].model = "qwen3-1.7b"
accuracy[21].task = "xnli"
accuracy[21].form = "itrans"
accuracy[21].n = 200
accuracy[21].chance = 0.3333333333333333
accuracy[21].acc_cal = 0.335
accuracy[21].acc_cal_ci_low = 0.27
accuracy[21].acc_cal_ci_high = 0.4
accuracy[21].constant_label_rate_cal = 0.995
accuracy[21].acc_raw = 0.37
accuracy[21].acc_raw_ci_low = 0.305
accuracy[21].acc_raw_ci_high = 0.44
accuracy[21].constant_label_rate_raw = 0.8
accuracy[21].acc_na = 0.335
accuracy[21].acc_na_ci_low = 0.27
accuracy[21].acc_na_ci_high = 0.4
accuracy[21].constant_label_rate_na = 0.995
accuracy[21].acc_avg3 = 0.335
accuracy[21].acc_avg3_ci_low = 0.27
accuracy[21].acc_avg3_ci_high = 0.4
accuracy[21].constant_label_rate_avg3 = 0.995
accuracy[21].tokens_per_word = 4.25161611138737
accuracy[22].model = "qwen3-1.7b"
accuracy[22].task = "xnli"
accuracy[22].form = "lossy"
accuracy[22].n = 200
accuracy[22].chance = 0.3333333333333333
accuracy[22].acc_cal = 0.335
accuracy[22].acc_cal_ci_low = 0.27
accuracy[22].acc_cal_ci_high = 0.4
accuracy[22].constant_label_rate_cal = 0.995
accuracy[22].acc_raw = 0.415
accuracy[22].acc_raw_ci_low = 0.345
accuracy[22].acc_raw_ci_high = 0.485
accuracy[22].constant_label_rate_raw = 0.795
accuracy[22].acc_na = 0.335
accuracy[22].acc_na_ci_low = 0.27
accuracy[22].acc_na_ci_high = 0.4
accuracy[22].constant_label_rate_na = 0.995
accuracy[22].acc_avg3 = 0.335
accuracy[22].acc_avg3_ci_low = 0.27
accuracy[22].acc_avg3_ci_high = 0.4
accuracy[22].constant_label_rate_avg3 = 0.995
accuracy[22].tokens_per_word = 3.5532073595226255
accuracy[23].model = "qwen3-1.7b"
accuracy[23].task = "xnli"
accuracy[23].form = "native"
accuracy[23].n = 200
accuracy[23].chance = 0.3333333333333333
accuracy[23].acc_cal = 0.445
accuracy[23].acc_cal_ci_low = 0.375
accuracy[23].acc_cal_ci_high = 0.515
accuracy[23].constant_label_rate_cal = 0.85
accuracy[23].acc_raw = 0.43
accuracy[23].acc_raw_ci_low = 0.36
accuracy[23].acc_raw_ci_high = 0.5
accuracy[23].constant_label_rate_raw = 0.61
accuracy[23].acc_na = 0.425
accuracy[23].acc_na_ci_low = 0.355
accuracy[23].acc_na_ci_high = 0.495
accuracy[23].constant_label_rate_na = 0.89
accuracy[23].acc_avg3 = 0.445
accuracy[23].acc_avg3_ci_low = 0.375
accuracy[23].acc_avg3_ci_high = 0.515
accuracy[23].constant_label_rate_avg3 = 0.85
accuracy[23].tokens_per_word = 11.79860765788165
accuracy[24].model = "qwen3.5-2b"
accuracy[24].task = "sentiment"
accuracy[24].form = "english"
accuracy[24].n = 200
accuracy[24].chance = 0.5
accuracy[24].acc_cal = 0.98
accuracy[24].acc_cal_ci_low = 0.96
accuracy[24].acc_cal_ci_high = 0.995
accuracy[24].constant_label_rate_cal = 0.51
accuracy[24].acc_raw = 0.975
accuracy[24].acc_raw_ci_low = 0.95
accuracy[24].acc_raw_ci_high = 0.995
accuracy[24].constant_label_rate_raw = 0.505
accuracy[24].acc_na = 0.975
accuracy[24].acc_na_ci_low = 0.95
accuracy[24].acc_na_ci_high = 0.995
accuracy[24].constant_label_rate_na = 0.525
accuracy[24].acc_avg3 = 0.98
accuracy[24].acc_avg3_ci_low = 0.96
accuracy[24].acc_avg3_ci_high = 0.995
accuracy[24].constant_label_rate_avg3 = 0.51
accuracy[24].tokens_per_word = 1.2268197573656845
accuracy[25].model = "qwen3.5-2b"
accuracy[25].task = "sentiment"
accuracy[25].form = "itrans"
accuracy[25].n = 200
accuracy[25].chance = 0.5
accuracy[25].acc_cal = 0.655
accuracy[25].acc_cal_ci_low = 0.59
accuracy[25].acc_cal_ci_high = 0.72
accuracy[25].constant_label_rate_cal = 0.775
accuracy[25].acc_raw = 0.675
accuracy[25].acc_raw_ci_low = 0.61
accuracy[25].acc_raw_ci_high = 0.74
accuracy[25].constant_label_rate_raw = 0.665
accuracy[25].acc_na = 0.615
accuracy[25].acc_na_ci_low = 0.545
accuracy[25].acc_na_ci_high = 0.685
accuracy[25].constant_label_rate_na = 0.855
accuracy[25].acc_avg3 = 0.655
accuracy[25].acc_avg3_ci_low = 0.59
accuracy[25].acc_avg3_ci_high = 0.72
accuracy[25].constant_label_rate_avg3 = 0.775
accuracy[25].tokens_per_word = 4.087631887456038
accuracy[26].model = "qwen3.5-2b"
accuracy[26].task = "sentiment"
accuracy[26].form = "lossy"
accuracy[26].n = 200
accuracy[26].chance = 0.5
accuracy[26].acc_cal = 0.68
accuracy[26].acc_cal_ci_low = 0.615
accuracy[26].acc_cal_ci_high = 0.74
accuracy[26].constant_label_rate_cal = 0.72
accuracy[26].acc_raw = 0.675
accuracy[26].acc_raw_ci_low = 0.61
accuracy[26].acc_raw_ci_high = 0.735
accuracy[26].constant_label_rate_raw = 0.645
accuracy[26].acc_na = 0.645
accuracy[26].acc_na_ci_low = 0.58
accuracy[26].acc_na_ci_high = 0.71
accuracy[26].constant_label_rate_na = 0.815
accuracy[26].acc_avg3 = 0.68
accuracy[26].acc_avg3_ci_low = 0.615
accuracy[26].acc_avg3_ci_high = 0.74
accuracy[26].constant_label_rate_avg3 = 0.72
accuracy[26].tokens_per_word = 3.3423212192262604
accuracy[27].model = "qwen3.5-2b"
accuracy[27].task = "sentiment"
accuracy[27].form = "native"
accuracy[27].n = 200
accuracy[27].chance = 0.5
accuracy[27].acc_cal = 0.735
accuracy[27].acc_cal_ci_low = 0.67
accuracy[27].acc_cal_ci_high = 0.795
accuracy[27].constant_label_rate_cal = 0.755
accuracy[27].acc_raw = 0.785
accuracy[27].acc_raw_ci_low = 0.725
accuracy[27].acc_raw_ci_high = 0.84
accuracy[27].constant_label_rate_raw = 0.705
accuracy[27].acc_na = 0.675
accuracy[27].acc_na_ci_low = 0.61
accuracy[27].acc_na_ci_high = 0.74
accuracy[27].constant_label_rate_na = 0.815
accuracy[27].acc_avg3 = 0.735
accuracy[27].acc_avg3_ci_low = 0.67
accuracy[27].acc_avg3_ci_high = 0.795
accuracy[27].constant_label_rate_avg3 = 0.755
accuracy[27].tokens_per_word = 5.235052754982415
accuracy[28].model = "qwen3.5-2b"
accuracy[28].task = "xnli"
accuracy[28].form = "english"
accuracy[28].n = 200
accuracy[28].chance = 0.3333333333333333
accuracy[28].acc_cal = 0.49
accuracy[28].acc_cal_ci_low = 0.42
accuracy[28].acc_cal_ci_high = 0.56
accuracy[28].constant_label_rate_cal = 0.805
accuracy[28].acc_raw = 0.43
accuracy[28].acc_raw_ci_low = 0.36
accuracy[28].acc_raw_ci_high = 0.5
accuracy[28].constant_label_rate_raw = 0.89
accuracy[28].acc_na = 0.45
accuracy[28].acc_na_ci_low = 0.38
accuracy[28].acc_na_ci_high = 0.52
accuracy[28].constant_label_rate_na = 0.845
accuracy[28].acc_avg3 = 0.49
accuracy[28].acc_avg3_ci_low = 0.42
accuracy[28].acc_avg3_ci_high = 0.56
accuracy[28].constant_label_rate_avg3 = 0.805
accuracy[28].tokens_per_word = 1.2424922333448394
accuracy[29].model = "qwen3.5-2b"
accuracy[29].task = "xnli"
accuracy[29].form = "itrans"
accuracy[29].n = 200
accuracy[29].chance = 0.3333333333333333
accuracy[29].acc_cal = 0.34
accuracy[29].acc_cal_ci_low = 0.275
accuracy[29].acc_cal_ci_high = 0.405
accuracy[29].constant_label_rate_cal = 0.995
accuracy[29].acc_raw = 0.34
accuracy[29].acc_raw_ci_low = 0.275
accuracy[29].acc_raw_ci_high = 0.405
accuracy[29].constant_label_rate_raw = 0.995
accuracy[29].acc_na = 0.34
accuracy[29].acc_na_ci_low = 0.275
accuracy[29].acc_na_ci_high = 0.405
accuracy[29].constant_label_rate_na = 0.995
accuracy[29].acc_avg3 = 0.34
accuracy[29].acc_avg3_ci_low = 0.275
accuracy[29].acc_avg3_ci_high = 0.405
accuracy[29].constant_label_rate_avg3 = 0.995
accuracy[29].tokens_per_word = 4.1282943809050225
accuracy[30].model = "qwen3.5-2b"
accuracy[30].task = "xnli"
accuracy[30].form = "lossy"
accuracy[30].n = 200
accuracy[30].chance = 0.3333333333333333
accuracy[30].acc_cal = 0.335
accuracy[30].acc_cal_ci_low = 0.27
accuracy[30].acc_cal_ci_high = 0.4
accuracy[30].constant_label_rate_cal = 0.99
accuracy[30].acc_raw = 0.34
accuracy[30].acc_raw_ci_low = 0.275
accuracy[30].acc_raw_ci_high = 0.405
accuracy[30].constant_label_rate_raw = 0.995
accuracy[30].acc_na = 0.335
accuracy[30].acc_na_ci_low = 0.27
accuracy[30].acc_na_ci_high = 0.4
accuracy[30].constant_label_rate_na = 0.99
accuracy[30].acc_avg3 = 0.335
accuracy[30].acc_avg3_ci_low = 0.27
accuracy[30].acc_avg3_ci_high = 0.4
accuracy[30].constant_label_rate_avg3 = 0.99
accuracy[30].tokens_per_word = 3.3431128791645945
accuracy[31].model = "qwen3.5-2b"
accuracy[31].task = "xnli"
accuracy[31].form = "native"
accuracy[31].n = 200
accuracy[31].chance = 0.3333333333333333
accuracy[31].acc_cal = 0.34
accuracy[31].acc_cal_ci_low = 0.275
accuracy[31].acc_cal_ci_high = 0.405
accuracy[31].constant_label_rate_cal = 0.995
accuracy[31].acc_raw = 0.34
accuracy[31].acc_raw_ci_low = 0.275
accuracy[31].acc_raw_ci_high = 0.405
accuracy[31].constant_label_rate_raw = 0.995
accuracy[31].acc_na = 0.34
accuracy[31].acc_na_ci_low = 0.275
accuracy[31].acc_na_ci_high = 0.405
accuracy[31].constant_label_rate_na = 0.995
accuracy[31].acc_avg3 = 0.34
accuracy[31].acc_avg3_ci_low = 0.275
accuracy[31].acc_avg3_ci_high = 0.405
accuracy[31].constant_label_rate_avg3 = 0.995
accuracy[31].tokens_per_word = 5.230979612133267
accuracy[32].model = "sarvam-1"
accuracy[32].task = "sentiment"
accuracy[32].form = "english"
accuracy[32].n = 200
accuracy[32].chance = 0.5
accuracy[32].acc_cal = 0.98
accuracy[32].acc_cal_ci_low = 0.96
accuracy[32].acc_cal_ci_high = 0.995
accuracy[32].constant_label_rate_cal = 0.51
accuracy[32].acc_raw = 0.975
accuracy[32].acc_raw_ci_low = 0.95
accuracy[32].acc_raw_ci_high = 0.995
accuracy[32].constant_label_rate_raw = 0.505
accuracy[32].acc_na = 0.975
accuracy[32].acc_na_ci_low = 0.95
accuracy[32].acc_na_ci_high = 0.995
accuracy[32].constant_label_rate_na = 0.515
accuracy[32].acc_avg3 = 0.98
accuracy[32].acc_avg3_ci_low = 0.96
accuracy[32].acc_avg3_ci_high = 0.995
accuracy[32].constant_label_rate_avg3 = 0.51
accuracy[32].tokens_per_word = 1.4204939341421143
accuracy[33].model = "sarvam-1"
accuracy[33].task = "sentiment"
accuracy[33].form = "itrans"
accuracy[33].n = 200
accuracy[33].chance = 0.5
accuracy[33].acc_cal = 0.82
accuracy[33].acc_cal_ci_low = 0.765
accuracy[33].acc_cal_ci_high = 0.87
accuracy[33].constant_label_rate_cal = 0.61
accuracy[33].acc_raw = 0.845
accuracy[33].acc_raw_ci_low = 0.795
accuracy[33].acc_raw_ci_high = 0.895
accuracy[33].constant_label_rate_raw = 0.515
accuracy[33].acc_na = 0.78
accuracy[33].acc_na_ci_low = 0.72
accuracy[33].acc_na_ci_high = 0.835
accuracy[33].constant_label_rate_na = 0.69
accuracy[33].acc_avg3 = 0.82
accuracy[33].acc_avg3_ci_low = 0.765
accuracy[33].acc_avg3_ci_high = 0.87
accuracy[33].constant_label_rate_avg3 = 0.61
accuracy[33].tokens_per_word = 5.238569753810082
accuracy[34].model = "sarvam-1"
accuracy[34].task = "sentiment"
accuracy[34].form = "lossy"
accuracy[34].n = 200
accuracy[34].chance = 0.5
accuracy[34].acc_cal = 0.895
accuracy[34].acc_cal_ci_low = 0.85
accuracy[34].acc_cal_ci_high = 0.935
accuracy[34].constant_label_rate_cal = 0.575
accuracy[34].acc_raw = 0.91
accuracy[34].acc_raw_ci_low = 0.87
accuracy[34].acc_raw_ci_high = 0.95
accuracy[34].constant_label_rate_raw = 0.51
accuracy[34].acc_na = 0.86
accuracy[34].acc_na_ci_low = 0.81
accuracy[34].acc_na_ci_high = 0.905
accuracy[34].constant_label_rate_na = 0.63
accuracy[34].acc_avg3 = 0.895
accuracy[34].acc_avg3_ci_low = 0.85
accuracy[34].acc_avg3_ci_high = 0.935
accuracy[34].constant_label_rate_avg3 = 0.575
accuracy[34].tokens_per_word = 4.357561547479484
accuracy[35].model = "sarvam-1"
accuracy[35].task = "sentiment"
accuracy[35].form = "native"
accuracy[35].n = 200
accuracy[35].chance = 0.5
accuracy[35].acc_cal = 0.955
accuracy[35].acc_cal_ci_low = 0.925
accuracy[35].acc_cal_ci_high = 0.98
accuracy[35].constant_label_rate_cal = 0.505
accuracy[35].acc_raw = 0.96
accuracy[35].acc_raw_ci_low = 0.93
accuracy[35].acc_raw_ci_high = 0.985
accuracy[35].constant_label_rate_raw = 0.53
accuracy[35].acc_na = 0.96
accuracy[35].acc_na_ci_low = 0.93
accuracy[35].acc_na_ci_high = 0.985
accuracy[35].constant_label_rate_na = 0.51
accuracy[35].acc_avg3 = 0.955
accuracy[35].acc_avg3_ci_low = 0.925
accuracy[35].acc_avg3_ci_high = 0.98
accuracy[35].constant_label_rate_avg3 = 0.505
accuracy[35].tokens_per_word = 2.2708089097303636
accuracy[36].model = "sarvam-1"
accuracy[36].task = "xnli"
accuracy[36].form = "english"
accuracy[36].n = 200
accuracy[36].chance = 0.3333333333333333
accuracy[36].acc_cal = 0.55
accuracy[36].acc_cal_ci_low = 0.48
accuracy[36].acc_cal_ci_high = 0.62
accuracy[36].constant_label_rate_cal = 0.545
accuracy[36].acc_raw = 0.53
accuracy[36].acc_raw_ci_low = 0.46
accuracy[36].acc_raw_ci_high = 0.6
accuracy[36].constant_label_rate_raw = 0.63
accuracy[36].acc_na = 0.475
accuracy[36].acc_na_ci_low = 0.405
accuracy[36].acc_na_ci_high = 0.545
accuracy[36].constant_label_rate_na = 0.655
accuracy[36].acc_avg3 = 0.55
accuracy[36].acc_avg3_ci_low = 0.48
accuracy[36].acc_avg3_ci_high = 0.62
accuracy[36].constant_label_rate_avg3 = 0.545
accuracy[36].tokens_per_word = 1.4326889886089058
accuracy[37].model = "sarvam-1"
accuracy[37].task = "xnli"
accuracy[37].form = "itrans"
accuracy[37].n = 200
accuracy[37].chance = 0.3333333333333333
accuracy[37].acc_cal = 0.385
accuracy[37].acc_cal_ci_low = 0.32
accuracy[37].acc_cal_ci_high = 0.455
accuracy[37].constant_label_rate_cal = 0.795
accuracy[37].acc_raw = 0.385
accuracy[37].acc_raw_ci_low = 0.32
accuracy[37].acc_raw_ci_high = 0.455
accuracy[37].constant_label_rate_raw = 0.8
accuracy[37].acc_na = 0.37
accuracy[37].acc_na_ci_low = 0.3
accuracy[37].acc_na_ci_high = 0.44
accuracy[37].constant_label_rate_na = 0.865
accuracy[37].acc_avg3 = 0.385
accuracy[37].acc_avg3_ci_low = 0.32
accuracy[37].acc_avg3_ci_high = 0.455
accuracy[37].constant_label_rate_avg3 = 0.795
accuracy[37].tokens_per_word = 5.226255594231725
accuracy[38].model = "sarvam-1"
accuracy[38].task = "xnli"
accuracy[38].form = "lossy"
accuracy[38].n = 200
accuracy[38].chance = 0.3333333333333333
accuracy[38].acc_cal = 0.47
accuracy[38].acc_cal_ci_low = 0.4
accuracy[38].acc_cal_ci_high = 0.54
accuracy[38].constant_label_rate_cal = 0.58
accuracy[38].acc_raw = 0.46
accuracy[38].acc_raw_ci_low = 0.39
accuracy[38].acc_raw_ci_high = 0.53
accuracy[38].constant_label_rate_raw = 0.595
accuracy[38].acc_na = 0.375
accuracy[38].acc_na_ci_low = 0.31
accuracy[38].acc_na_ci_high = 0.44
accuracy[38].constant_label_rate_na = 0.905
accuracy[38].acc_avg3 = 0.47
accuracy[38].acc_avg3_ci_low = 0.4
accuracy[38].acc_avg3_ci_high = 0.54
accuracy[38].constant_label_rate_avg3 = 0.58
accuracy[38].tokens_per_word = 4.335405271009448
accuracy[39].model = "sarvam-1"
accuracy[39].task = "xnli"
accuracy[39].form = "native"
accuracy[39].n = 200
accuracy[39].chance = 0.3333333333333333
accuracy[39].acc_cal = 0.515
accuracy[39].acc_cal_ci_low = 0.445
accuracy[39].acc_cal_ci_high = 0.585
accuracy[39].constant_label_rate_cal = 0.6
accuracy[39].acc_raw = 0.52
accuracy[39].acc_raw_ci_low = 0.45
accuracy[39].acc_raw_ci_high = 0.59
accuracy[39].constant_label_rate_raw = 0.61
accuracy[39].acc_na = 0.455
accuracy[39].acc_na_ci_low = 0.385
accuracy[39].acc_na_ci_high = 0.525
accuracy[39].constant_label_rate_na = 0.865
accuracy[39].acc_avg3 = 0.515
accuracy[39].acc_avg3_ci_low = 0.445
accuracy[39].acc_avg3_ci_high = 0.585
accuracy[39].constant_label_rate_avg3 = 0.6
accuracy[39].tokens_per_word = 2.1452013923421185
mcnemar[0].model = "gemma4-e2b"
mcnemar[0].task = "sentiment"
mcnemar[0].a = "lossy"
mcnemar[0].b = "itrans"
mcnemar[0].acc_a = 0.79
mcnemar[0].acc_b = 0.755
mcnemar[0].n = 200
mcnemar[0].diff = 0.03500000000000003
mcnemar[0].a_only = 18
mcnemar[0].b_only = 11
mcnemar[0].p = 0.26493089646101
mcnemar[0].p_holm = 1.0
mcnemar[0].significant = false
mcnemar[1].model = "gemma4-e2b"
mcnemar[1].task = "xnli"
mcnemar[1].a = "lossy"
mcnemar[1].b = "itrans"
mcnemar[1].acc_a = 0.4
mcnemar[1].acc_b = 0.41
mcnemar[1].n = 200
mcnemar[1].diff = -0.009999999999999953
mcnemar[1].a_only = 11
mcnemar[1].b_only = 13
mcnemar[1].p = 0.8388197422027588
mcnemar[1].p_holm = 1.0
mcnemar[1].significant = false
mcnemar[2].model = "qwen2.5-1.5b"
mcnemar[2].task = "sentiment"
mcnemar[2].a = "lossy"
mcnemar[2].b = "itrans"
mcnemar[2].acc_a = 0.5
mcnemar[2].acc_b = 0.495
mcnemar[2].n = 200
mcnemar[2].diff = 0.0050000000000000044
mcnemar[2].a_only = 4
mcnemar[2].b_only = 3
mcnemar[2].p = 1.0
mcnemar[2].p_holm = 1.0
mcnemar[2].significant = false
mcnemar[3].model = "qwen2.5-1.5b"
mcnemar[3].task = "xnli"
mcnemar[3].a = "lossy"
mcnemar[3].b = "itrans"
mcnemar[3].acc_a = 0.325
mcnemar[3].acc_b = 0.32
mcnemar[3].n = 200
mcnemar[3].diff = 0.0050000000000000044
mcnemar[3].a_only = 18
mcnemar[3].b_only = 17
mcnemar[3].p = 0.9999999999999998
mcnemar[3].p_holm = 1.0
mcnemar[3].significant = false
mcnemar[4].model = "qwen3-1.7b"
mcnemar[4].task = "sentiment"
mcnemar[4].a = "lossy"
mcnemar[4].b = "itrans"
mcnemar[4].acc_a = 0.57
mcnemar[4].acc_b = 0.535
mcnemar[4].n = 200
mcnemar[4].diff = 0.03499999999999992
mcnemar[4].a_only = 32
mcnemar[4].b_only = 25
mcnemar[4].p = 0.42704285650325524
mcnemar[4].p_holm = 1.0
mcnemar[4].significant = false
mcnemar[5].model = "qwen3-1.7b"
mcnemar[5].task = "xnli"
mcnemar[5].a = "lossy"
mcnemar[5].b = "itrans"
mcnemar[5].acc_a = 0.335
mcnemar[5].acc_b = 0.335
mcnemar[5].n = 200
mcnemar[5].diff = 0.0
mcnemar[5].a_only = 0
mcnemar[5].b_only = 0
mcnemar[5].p = 1.0
mcnemar[5].p_holm = 1.0
mcnemar[5].significant = false
mcnemar[6].model = "qwen3.5-2b"
mcnemar[6].task = "sentiment"
mcnemar[6].a = "lossy"
mcnemar[6].b = "itrans"
mcnemar[6].acc_a = 0.68
mcnemar[6].acc_b = 0.655
mcnemar[6].n = 200
mcnemar[6].diff = 0.025000000000000022
mcnemar[6].a_only = 23
mcnemar[6].b_only = 18
mcnemar[6].p = 0.5327092552361137
mcnemar[6].p_holm = 1.0
mcnemar[6].significant = false
mcnemar[7].model = "qwen3.5-2b"
mcnemar[7].task = "xnli"
mcnemar[7].a = "lossy"
mcnemar[7].b = "itrans"
mcnemar[7].acc_a = 0.335
mcnemar[7].acc_b = 0.34
mcnemar[7].n = 200
mcnemar[7].diff = -0.0050000000000000044
mcnemar[7].a_only = 0
mcnemar[7].b_only = 1
mcnemar[7].p = 1.0
mcnemar[7].p_holm = 1.0
mcnemar[7].significant = false
mcnemar[8].model = "sarvam-1"
mcnemar[8].task = "sentiment"
mcnemar[8].a = "lossy"
mcnemar[8].b = "itrans"
mcnemar[8].acc_a = 0.895
mcnemar[8].acc_b = 0.82
mcnemar[8].n = 200
mcnemar[8].diff = 0.07500000000000007
mcnemar[8].a_only = 21
mcnemar[8].b_only = 6
mcnemar[8].p = 0.005924612283706665
mcnemar[8].p_holm = 0.05924612283706665
mcnemar[8].significant = false
mcnemar[9].model = "sarvam-1"
mcnemar[9].task = "xnli"
mcnemar[9].a = "lossy"
mcnemar[9].b = "itrans"
mcnemar[9].acc_a = 0.47
mcnemar[9].acc_b = 0.385
mcnemar[9].n = 200
mcnemar[9].diff = 0.08499999999999996
mcnemar[9].a_only = 29
mcnemar[9].b_only = 12
mcnemar[9].p = 0.011507789735333063
mcnemar[9].p_holm = 0.10357010761799756
mcnemar[9].significant = false
mcnemar_exploratory[0].model = "gemma4-e2b"
mcnemar_exploratory[0].task = "sentiment"
mcnemar_exploratory[0].a = "itrans"
mcnemar_exploratory[0].b = "native"
mcnemar_exploratory[0].acc_a = 0.755
mcnemar_exploratory[0].acc_b = 0.985
mcnemar_exploratory[0].n = 200
mcnemar_exploratory[0].diff = -0.22999999999999998
mcnemar_exploratory[0].a_only = 1
mcnemar_exploratory[0].b_only = 47
mcnemar_exploratory[0].p = 3.481659405224491e-13
mcnemar_exploratory[0].p_holm = 3.481659405224491e-12
mcnemar_exploratory[0].significant = true
mcnemar_exploratory[1].model = "gemma4-e2b"
mcnemar_exploratory[1].task = "xnli"
mcnemar_exploratory[1].a = "itrans"
mcnemar_exploratory[1].b = "native"
mcnemar_exploratory[1].acc_a = 0.41
mcnemar_exploratory[1].acc_b = 0.545
mcnemar_exploratory[1].n = 200
mcnemar_exploratory[1].diff = -0.13500000000000006
mcnemar_exploratory[1].a_only = 14
mcnemar_exploratory[1].b_only = 41
mcnemar_exploratory[1].p = 0.00035528111863147854
mcnemar_exploratory[1].p_holm = 0.0017764055931573928
mcnemar_exploratory[1].significant = true
mcnemar_exploratory[2].model = "qwen2.5-1.5b"
mcnemar_exploratory[2].task = "sentiment"
mcnemar_exploratory[2].a = "itrans"
mcnemar_exploratory[2].b = "native"
mcnemar_exploratory[2].acc_a = 0.495
mcnemar_exploratory[2].acc_b = 0.705
mcnemar_exploratory[2].n = 200
mcnemar_exploratory[2].diff = -0.20999999999999996
mcnemar_exploratory[2].a_only = 16
mcnemar_exploratory[2].b_only = 58
mcnemar_exploratory[2].p = 9.674891137601897e-07
mcnemar_exploratory[2].p_holm = 7.739912910081517e-06
mcnemar_exploratory[2].significant = true
mcnemar_exploratory[3].model = "qwen2.5-1.5b"
mcnemar_exploratory[3].task = "xnli"
mcnemar_exploratory[3].a = "itrans"
mcnemar_exploratory[3].b = "native"
mcnemar_exploratory[3].acc_a = 0.32
mcnemar_exploratory[3].acc_b = 0.4
mcnemar_exploratory[3].n = 200
mcnemar_exploratory[3].diff = -0.08000000000000002
mcnemar_exploratory[3].a_only = 18
mcnemar_exploratory[3].b_only = 34
mcnemar_exploratory[3].p = 0.03648340000835981
mcnemar_exploratory[3].p_holm = 0.07768824537970431
mcnemar_exploratory[3].significant = false
mcnemar_exploratory[4].model = "qwen3-1.7b"
mcnemar_exploratory[4].task = "sentiment"
mcnemar_exploratory[4].a = "itrans"
mcnemar_exploratory[4].b = "native"
mcnemar_exploratory[4].acc_a = 0.535
mcnemar_exploratory[4].acc_b = 0.835
mcnemar_exploratory[4].n = 200
mcnemar_exploratory[4].diff = -0.29999999999999993
mcnemar_exploratory[4].a_only = 14
mcnemar_exploratory[4].b_only = 74
mcnemar_exploratory[4].p = 5.0891941127085865e-11
mcnemar_exploratory[4].p_holm = 4.580274701437728e-10
mcnemar_exploratory[4].significant = true
mcnemar_exploratory[5].model = "qwen3-1.7b"
mcnemar_exploratory[5].task = "xnli"
mcnemar_exploratory[5].a = "itrans"
mcnemar_exploratory[5].b = "native"
mcnemar_exploratory[5].acc_a = 0.335
mcnemar_exploratory[5].acc_b = 0.445
mcnemar_exploratory[5].n = 200
mcnemar_exploratory[5].diff = -0.10999999999999999
mcnemar_exploratory[5].a_only = 3
mcnemar_exploratory[5].b_only = 25
mcnemar_exploratory[5].p = 2.744048833847046e-05
mcnemar_exploratory[5].p_holm = 0.00016464293003082275
mcnemar_exploratory[5].significant = true
mcnemar_exploratory[6].model = "qwen3.5-2b"
mcnemar_exploratory[6].task = "sentiment"
mcnemar_exploratory[6].a = "itrans"
mcnemar_exploratory[6].b = "native"
mcnemar_exploratory[6].acc_a = 0.655
mcnemar_exploratory[6].acc_b = 0.735
mcnemar_exploratory[6].n = 200
mcnemar_exploratory[6].diff = -0.07999999999999996
mcnemar_exploratory[6].a_only = 15
mcnemar_exploratory[6].b_only = 31
mcnemar_exploratory[6].p = 0.02589608179323477
mcnemar_exploratory[6].p_holm = 0.07768824537970431
mcnemar_exploratory[6].significant = false
mcnemar_exploratory[7].model = "qwen3.5-2b"
mcnemar_exploratory[7].task = "xnli"
mcnemar_exploratory[7].a = "itrans"
mcnemar_exploratory[7].b = "native"
mcnemar_exploratory[7].acc_a = 0.34
mcnemar_exploratory[7].acc_b = 0.34
mcnemar_exploratory[7].n = 200
mcnemar_exploratory[7].diff = 0.0
mcnemar_exploratory[7].a_only = 0
mcnemar_exploratory[7].b_only = 0
mcnemar_exploratory[7].p = 1.0
mcnemar_exploratory[7].p_holm = 1.0
mcnemar_exploratory[7].significant = false
mcnemar_exploratory[8].model = "sarvam-1"
mcnemar_exploratory[8].task = "sentiment"
mcnemar_exploratory[8].a = "itrans"
mcnemar_exploratory[8].b = "native"
mcnemar_exploratory[8].acc_a = 0.82
mcnemar_exploratory[8].acc_b = 0.955
mcnemar_exploratory[8].n = 200
mcnemar_exploratory[8].diff = -0.135
mcnemar_exploratory[8].a_only = 6
mcnemar_exploratory[8].b_only = 33
mcnemar_exploratory[8].p = 1.429926123819314e-05
mcnemar_exploratory[8].p_holm = 0.00010009482866735198
mcnemar_exploratory[8].significant = true
mcnemar_exploratory[9].model = "sarvam-1"
mcnemar_exploratory[9].task = "xnli"
mcnemar_exploratory[9].a = "itrans"
mcnemar_exploratory[9].b = "native"
mcnemar_exploratory[9].acc_a = 0.385
mcnemar_exploratory[9].acc_b = 0.515
mcnemar_exploratory[9].n = 200
mcnemar_exploratory[9].diff = -0.13
mcnemar_exploratory[9].a_only = 14
mcnemar_exploratory[9].b_only = 40
mcnemar_exploratory[9].p = 0.0005354355028570622
mcnemar_exploratory[9].p_holm = 0.002141742011428249
mcnemar_exploratory[9].significant = true
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.2469796341042458
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.231369150779896
fertility[2].model = "qwen2.5-1.5b"
fertility[2].task = "xnli"
fertility[2].form = "native"
fertility[2].n_texts = 400
fertility[2].tokens_per_word = 11.79860765788165
fertility[3].model = "qwen2.5-1.5b"
fertility[3].task = "sentiment"
fertility[3].form = "native"
fertility[3].n_texts = 200
fertility[3].tokens_per_word = 11.985638921453694
fertility[4].model = "qwen2.5-1.5b"
fertility[4].task = "xnli"
fertility[4].form = "itrans"
fertility[4].n_texts = 400
fertility[4].tokens_per_word = 4.25161611138737
fertility[5].model = "qwen2.5-1.5b"
fertility[5].task = "sentiment"
fertility[5].form = "itrans"
fertility[5].n_texts = 200
fertility[5].tokens_per_word = 4.22538100820633
fertility[6].model = "qwen2.5-1.5b"
fertility[6].task = "xnli"
fertility[6].form = "lossy"
fertility[6].n_texts = 400
fertility[6].tokens_per_word = 3.5532073595226255
fertility[7].model = "qwen2.5-1.5b"
fertility[7].task = "sentiment"
fertility[7].form = "lossy"
fertility[7].n_texts = 200
fertility[7].tokens_per_word = 3.5679953106682296
fertility[8].model = "qwen3.5-2b"
fertility[8].task = "xnli"
fertility[8].form = "english"
fertility[8].n_texts = 400
fertility[8].tokens_per_word = 1.2424922333448394
fertility[9].model = "qwen3.5-2b"
fertility[9].task = "sentiment"
fertility[9].form = "english"
fertility[9].n_texts = 200
fertility[9].tokens_per_word = 1.2268197573656845
fertility[10].model = "qwen3.5-2b"
fertility[10].task = "xnli"
fertility[10].form = "native"
fertility[10].n_texts = 400
fertility[10].tokens_per_word = 5.230979612133267
fertility[11].model = "qwen3.5-2b"
fertility[11].task = "sentiment"
fertility[11].form = "native"
fertility[11].n_texts = 200
fertility[11].tokens_per_word = 5.235052754982415
fertility[12].model = "qwen3.5-2b"
fertility[12].task = "xnli"
fertility[12].form = "itrans"
fertility[12].n_texts = 400
fertility[12].tokens_per_word = 4.1282943809050225
fertility[13].model = "qwen3.5-2b"
fertility[13].task = "sentiment"
fertility[13].form = "itrans"
fertility[13].n_texts = 200
fertility[13].tokens_per_word = 4.087631887456038
fertility[14].model = "qwen3.5-2b"
fertility[14].task = "xnli"
fertility[14].form = "lossy"
fertility[14].n_texts = 400
fertility[14].tokens_per_word = 3.3431128791645945
fertility[15].model = "qwen3.5-2b"
fertility[15].task = "sentiment"
fertility[15].form = "lossy"
fertility[15].n_texts = 200
fertility[15].tokens_per_word = 3.3423212192262604
fertility[16].model = "sarvam-1"
fertility[16].task = "xnli"
fertility[16].form = "english"
fertility[16].n_texts = 400
fertility[16].tokens_per_word = 1.4326889886089058
fertility[17].model = "sarvam-1"
fertility[17].task = "sentiment"
fertility[17].form = "english"
fertility[17].n_texts = 200
fertility[17].tokens_per_word = 1.4204939341421143
fertility[18].model = "sarvam-1"
fertility[18].task = "xnli"
fertility[18].form = "native"
fertility[18].n_texts = 400
fertility[18].tokens_per_word = 2.1452013923421185
fertility[19].model = "sarvam-1"
fertility[19].task = "sentiment"
fertility[19].form = "native"
fertility[19].n_texts = 200
fertility[19].tokens_per_word = 2.2708089097303636
fertility[20].model = "sarvam-1"
fertility[20].task = "xnli"
fertility[20].form = "itrans"
fertility[20].n_texts = 400
fertility[20].tokens_per_word = 5.226255594231725
fertility[21].model = "sarvam-1"
fertility[21].task = "sentiment"
fertility[21].form = "itrans"
fertility[21].n_texts = 200
fertility[21].tokens_per_word = 5.238569753810082
fertility[22].model = "sarvam-1"
fertility[22].task = "xnli"
fertility[22].form = "lossy"
fertility[22].n_texts = 400
fertility[22].tokens_per_word = 4.335405271009448
fertility[23].model = "sarvam-1"
fertility[23].task = "sentiment"
fertility[23].form = "lossy"
fertility[23].n_texts = 200
fertility[23].tokens_per_word = 4.357561547479484
fertility[24].model = "gemma4-e2b"
fertility[24].task = "xnli"
fertility[24].form = "english"
fertility[24].n_texts = 400
fertility[24].tokens_per_word = 1.2397307559544357
fertility[25].model = "gemma4-e2b"
fertility[25].task = "sentiment"
fertility[25].form = "english"
fertility[25].n_texts = 200
fertility[25].tokens_per_word = 1.2214038128249567
fertility[26].model = "gemma4-e2b"
fertility[26].task = "xnli"
fertility[26].form = "native"
fertility[26].n_texts = 400
fertility[26].tokens_per_word = 3.1397314768771754
fertility[27].model = "gemma4-e2b"
fertility[27].task = "sentiment"
fertility[27].form = "native"
fertility[27].n_texts = 200
fertility[27].tokens_per_word = 3.0767878077373974
fertility[28].model = "gemma4-e2b"
fertility[28].task = "xnli"
fertility[28].form = "itrans"
fertility[28].n_texts = 400
fertility[28].tokens_per_word = 3.9604674291397313
fertility[29].model = "gemma4-e2b"
fertility[29].task = "sentiment"
fertility[29].form = "itrans"
fertility[29].n_texts = 200
fertility[29].tokens_per_word = 3.943434935521688
fertility[30].model = "gemma4-e2b"
fertility[30].task = "xnli"
fertility[30].form = "lossy"
fertility[30].n_texts = 400
fertility[30].tokens_per_word = 3.2031327697662855
fertility[31].model = "gemma4-e2b"
fertility[31].task = "sentiment"
fertility[31].form = "lossy"
fertility[31].n_texts = 200
fertility[31].tokens_per_word = 3.2110199296600235
fertility[32].model = "qwen3-1.7b"
fertility[32].task = "xnli"
fertility[32].form = "english"
fertility[32].n_texts = 400
fertility[32].tokens_per_word = 1.2469796341042458
fertility[33].model = "qwen3-1.7b"
fertility[33].task = "sentiment"
fertility[33].form = "english"
fertility[33].n_texts = 200
fertility[33].tokens_per_word = 1.231369150779896
fertility[34].model = "qwen3-1.7b"
fertility[34].task = "xnli"
fertility[34].form = "native"
fertility[34].n_texts = 400
fertility[34].tokens_per_word = 11.79860765788165
fertility[35].model = "qwen3-1.7b"
fertility[35].task = "sentiment"
fertility[35].form = "native"
fertility[35].n_texts = 200
fertility[35].tokens_per_word = 11.985638921453694
fertility[36].model = "qwen3-1.7b"
fertility[36].task = "xnli"
fertility[36].form = "itrans"
fertility[36].n_texts = 400
fertility[36].tokens_per_word = 4.25161611138737
fertility[37].model = "qwen3-1.7b"
fertility[37].task = "sentiment"
fertility[37].form = "itrans"
fertility[37].n_texts = 200
fertility[37].tokens_per_word = 4.22538100820633
fertility[38].model = "qwen3-1.7b"
fertility[38].task = "xnli"
fertility[38].form = "lossy"
fertility[38].n_texts = 400
fertility[38].tokens_per_word = 3.5532073595226255
fertility[39].model = "qwen3-1.7b"
fertility[39].task = "sentiment"
fertility[39].form = "lossy"
fertility[39].n_texts = 200
fertility[39].tokens_per_word = 3.5679953106682296
verdicts.informative_cells = ["gemma4-e2b/sentiment", "gemma4-e2b/xnli", "qwen2.5-1.5b/sentiment", "qwen2.5-1.5b/xnli", "qwen3-1.7b/sentiment", "qwen3-1.7b/xnli", "qwen3.5-2b/sentiment", "qwen3.5-2b/xnli", "sarvam-1/sentiment", "sarvam-1/xnli"]
verdicts.P3_lossy_lt_itrans = false
verdicts.P3_parts.all_cells_lossy_below_itrans = false
verdicts.P3_parts.fraction_significant = 0.0
verdicts.P3_parts.n_cells = 10
verdicts.P1_familiarity_dominates = "pending (natural form not scored)"
verdicts.P2_fragmentation_also_matters = "pending (natural form not scored)"
`````

#### `results/e0b_familiarity/gate1a_v2/verdicts.json` (2,908 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

`````text
provenance.config.models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
provenance.config.forms = ["english", "native", "itrans", "lossy"]
provenance.config.calibration = "primary: mean of content-free N/A, '', [MASK]; raw fallback if English drops > 5 pts"
provenance.config.calibration_fallback_rows[0].model = "gemma4-e2b"
provenance.config.calibration_fallback_rows[0].task = "xnli"
provenance.config.calibration_fallback_rows[1].model = "qwen2.5-1.5b"
provenance.config.calibration_fallback_rows[1].task = "sentiment"
provenance.config.natural_items_excluded_defective = 0
provenance.config.templates = "e0_{xnli,sentiment}_v1"
provenance.config.n_per_task = 200
provenance.config.seed = 0
provenance.config.bos = "always prepended"
provenance.config.seconds_per_model_form.qwen2.5-1.5b/english = 36.487061977386475
provenance.config.seconds_per_model_form.qwen2.5-1.5b/native = 60.4139928817749
provenance.config.seconds_per_model_form.qwen2.5-1.5b/itrans = 46.802143573760986
provenance.config.seconds_per_model_form.qwen2.5-1.5b/lossy = 49.93747925758362
provenance.config.seconds_per_model_form.qwen3.5-2b/english = 100.45982670783997
provenance.config.seconds_per_model_form.qwen3.5-2b/native = 137.80759501457214
provenance.config.seconds_per_model_form.qwen3.5-2b/itrans = 135.9841856956482
provenance.config.seconds_per_model_form.qwen3.5-2b/lossy = 107.09859132766724
provenance.config.seconds_per_model_form.sarvam-1/english = 52.38592600822449
provenance.config.seconds_per_model_form.sarvam-1/native = 54.95457744598389
provenance.config.seconds_per_model_form.sarvam-1/itrans = 60.9882435798645
provenance.config.seconds_per_model_form.sarvam-1/lossy = 57.89579892158508
provenance.config.seconds_per_model_form.gemma4-e2b/english = 89.42716455459595
provenance.config.seconds_per_model_form.gemma4-e2b/native = 94.79906296730042
provenance.config.seconds_per_model_form.gemma4-e2b/itrans = 97.28406596183777
provenance.config.seconds_per_model_form.gemma4-e2b/lossy = 92.6928346157074
provenance.config.seconds_per_model_form.qwen3-1.7b/english = 43.18634009361267
provenance.config.seconds_per_model_form.qwen3-1.7b/native = 65.9120557308197
provenance.config.seconds_per_model_form.qwen3-1.7b/itrans = 52.16321563720703
provenance.config.seconds_per_model_form.qwen3-1.7b/lossy = 49.83175706863403
provenance.git_commit = "d45dc1bf9e66523a94b2d9b731201f576803081f-dirty"
provenance.timestamp_utc = "2026-10-14T18:52:08+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0b_familiarity.py", "--models", "qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b", "--forms", "english", "native", "itrans", "lossy", "--tag", "gate1a_v2"]
informative_cells = ["gemma4-e2b/sentiment", "gemma4-e2b/xnli", "qwen2.5-1.5b/sentiment", "qwen2.5-1.5b/xnli", "qwen3-1.7b/sentiment", "qwen3-1.7b/xnli", "qwen3.5-2b/sentiment", "qwen3.5-2b/xnli", "sarvam-1/sentiment", "sarvam-1/xnli"]
P3_lossy_lt_itrans = false
P3_parts.all_cells_lossy_below_itrans = false
P3_parts.fraction_significant = 0.0
P3_parts.n_cells = 10
P1_familiarity_dominates = "pending (natural form not scored)"
P2_fragmentation_also_matters = "pending (natural form not scored)"
`````

#### `results/e0b_familiarity/scores/cf_gemma4-e2b.json` (536 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

`````text
N/A.xnli = [-8.601853370666504, -9.539353370666504, -0.320603609085083]
N/A.sentiment = [-11.390227317810059, -13.233977317810059]
xnli = [-9.796487808227539, -10.796487808227539, -8.421487808227539]
sentiment = [-7.080981731414795, -5.612231731414795]
[MASK].xnli = [-9.000367164611816, -14.859742164611816, -6.734742164611816]
[MASK].sentiment = [-10.317381858825684, -8.692381858825684]
`````

#### `results/e0b_familiarity/scores/cf_qwen2.5-1.5b.json` (535 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

`````text
N/A.xnli = [-1.815413475036621, -4.940413475036621, -1.440413475036621]
N/A.sentiment = [-1.862534523010254, -9.612534523010254]
xnli = [-2.464033842086792, -3.214033842086792, -1.339033842086792]
sentiment = [-2.3190255165100098, -4.44402551651001]
[MASK].xnli = [-1.9954825639724731, -2.8704824447631836, -2.4954824447631836]
[MASK].sentiment = [-1.3718047142028809, -2.621804714202881]
`````

#### `results/e0b_familiarity/scores/cf_qwen3-1.7b.json` (537 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

`````text
N/A.xnli = [-0.4630722999572754, -2.8380722999572754, -3.2130722999572754]
N/A.sentiment = [-1.7947381734848022, -4.294738292694092]
xnli = [-3.522855043411255, -7.522854804992676, -4.897854804992676]
sentiment = [-3.698035717010498, -3.698035717010498]
[MASK].xnli = [-1.049058437347412, -3.174058437347412, -3.174058437347412]
[MASK].sentiment = [-1.9486875534057617, -3.8236875534057617]
`````

#### `results/e0b_familiarity/scores/cf_qwen3.5-2b.json` (538 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

`````text
N/A.xnli = [-2.2064056396484375, -3.7064056396484375, -2.0814056396484375]
N/A.sentiment = [-3.836883068084717, -3.586883068084717]
xnli = [-2.6445693969726562, -6.019569396972656, -1.8945692777633667]
sentiment = [-3.79923677444458, -4.04923677444458]
[MASK].xnli = [-1.5050513744354248, -3.255051374435425, -1.5050513744354248]
[MASK].sentiment = [-3.8607988357543945, -3.4857988357543945]
`````

#### `results/e0b_familiarity/scores/cf_sarvam-1.json` (535 bytes; first commit baf4f09 2026-10-15 00:56:53 +0530)

`````text
N/A.xnli = [-3.174879312515259, -5.67487907409668, -1.9248793125152588]
N/A.sentiment = [-8.01157283782959, -9.63657283782959]
xnli = [-1.628244161605835, -3.628244161605835, -1.628244161605835]
sentiment = [-1.5957965850830078, -2.095796585083008]
[MASK].xnli = [-1.1337692737579346, -4.8837690353393555, -1.8837692737579346]
[MASK].sentiment = [-1.8119052648544312, -2.3119053840637207]
`````

#### `results/e0b_familiarity/scores/gemma4-e2b__english.json` (543 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-8.601853370666504, -9.539353370666504, -0.320603609085083]
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.2397307559544357
fertility[1].model = "gemma4-e2b"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.2214038128249567
seconds = 89.42716455459595
`````

#### `results/e0b_familiarity/scores/gemma4-e2b__itrans.json` (540 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-8.601853370666504, -9.539353370666504, -0.320603609085083]
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "xnli"
fertility[0].form = "itrans"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 3.9604674291397313
fertility[1].model = "gemma4-e2b"
fertility[1].task = "sentiment"
fertility[1].form = "itrans"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 3.943434935521688
seconds = 97.28406596183777
`````

#### `results/e0b_familiarity/scores/gemma4-e2b__lossy.json` (538 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-8.601853370666504, -9.539353370666504, -0.320603609085083]
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "xnli"
fertility[0].form = "lossy"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 3.2031327697662855
fertility[1].model = "gemma4-e2b"
fertility[1].task = "sentiment"
fertility[1].form = "lossy"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 3.2110199296600235
seconds = 92.6928346157074
`````

#### `results/e0b_familiarity/scores/gemma4-e2b__lower.json` (539 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.xnli = [-8.601853370666504, -9.539353370666504, -0.320603609085083]
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "xnli"
fertility[0].form = "lower"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.0790651417205375
fertility[1].model = "gemma4-e2b"
fertility[1].task = "sentiment"
fertility[1].form = "lower"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.146248534583822
seconds = 104.80236864089966
`````

#### `results/e0b_familiarity/scores/gemma4-e2b__native.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-8.601853370666504, -9.539353370666504, -0.320603609085083]
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "xnli"
fertility[0].form = "native"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 3.1397314768771754
fertility[1].model = "gemma4-e2b"
fertility[1].task = "sentiment"
fertility[1].form = "native"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 3.0767878077373974
seconds = 94.79906296730042
`````

#### `results/e0b_familiarity/scores/gemma4-e2b__natural.json` (543 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

`````text
content_free_logprobs.xnli = [-8.601853370666504, -9.539353370666504, -0.320603609085083]
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "xnli"
fertility[0].form = "natural"
fertility[0].n_texts = 386
fertility[0].tokens_per_word = 3.1711991711991714
fertility[1].model = "gemma4-e2b"
fertility[1].task = "sentiment"
fertility[1].form = "natural"
fertility[1].n_texts = 198
fertility[1].tokens_per_word = 3.1530703055473155
seconds = 81.26459240913391
`````

#### `results/e0b_familiarity/scores/qwen2.5-1.5b__english.json` (545 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-1.815413475036621, -4.940413475036621, -1.440413475036621]
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.2469796341042458
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.231369150779896
seconds = 36.487061977386475
`````

#### `results/e0b_familiarity/scores/qwen2.5-1.5b__itrans.json` (540 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-1.815413475036621, -4.940413475036621, -1.440413475036621]
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "itrans"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.25161611138737
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "itrans"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.22538100820633
seconds = 46.802143573760986
`````

#### `results/e0b_familiarity/scores/qwen2.5-1.5b__lossy.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-1.815413475036621, -4.940413475036621, -1.440413475036621]
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "lossy"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 3.5532073595226255
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "lossy"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 3.5679953106682296
seconds = 49.93747925758362
`````

#### `results/e0b_familiarity/scores/qwen2.5-1.5b__lower.json` (540 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.xnli = [-1.815413475036621, -4.940413475036621, -1.440413475036621]
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "lower"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.309547488811536
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "lower"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.393317702227432
seconds = 52.731520891189575
`````

#### `results/e0b_familiarity/scores/qwen2.5-1.5b__native.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-1.815413475036621, -4.940413475036621, -1.440413475036621]
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "native"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 11.79860765788165
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "native"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 11.985638921453694
seconds = 60.4139928817749
`````

#### `results/e0b_familiarity/scores/qwen2.5-1.5b__natural.json` (545 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

`````text
content_free_logprobs.xnli = [-1.815413475036621, -4.940413475036621, -1.440413475036621]
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "xnli"
fertility[0].form = "natural"
fertility[0].n_texts = 386
fertility[0].tokens_per_word = 3.5423465423465426
fertility[1].model = "qwen2.5-1.5b"
fertility[1].task = "sentiment"
fertility[1].form = "natural"
fertility[1].n_texts = 198
fertility[1].tokens_per_word = 3.5069712251557403
seconds = 35.85534334182739
`````

#### `results/e0b_familiarity/scores/qwen3-1.7b__english.json` (544 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-0.4630722999572754, -2.8380722999572754, -3.2130722999572754]
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.2469796341042458
fertility[1].model = "qwen3-1.7b"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.231369150779896
seconds = 43.18634009361267
`````

#### `results/e0b_familiarity/scores/qwen3-1.7b__itrans.json` (539 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-0.4630722999572754, -2.8380722999572754, -3.2130722999572754]
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "xnli"
fertility[0].form = "itrans"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.25161611138737
fertility[1].model = "qwen3-1.7b"
fertility[1].task = "sentiment"
fertility[1].form = "itrans"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.22538100820633
seconds = 52.16321563720703
`````

#### `results/e0b_familiarity/scores/qwen3-1.7b__lossy.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-0.4630722999572754, -2.8380722999572754, -3.2130722999572754]
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "xnli"
fertility[0].form = "lossy"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 3.5532073595226255
fertility[1].model = "qwen3-1.7b"
fertility[1].task = "sentiment"
fertility[1].form = "lossy"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 3.5679953106682296
seconds = 49.83175706863403
`````

#### `results/e0b_familiarity/scores/qwen3-1.7b__lower.json` (539 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.xnli = [-0.4630722999572754, -2.8380722999572754, -3.2130722999572754]
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "xnli"
fertility[0].form = "lower"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.309547488811536
fertility[1].model = "qwen3-1.7b"
fertility[1].task = "sentiment"
fertility[1].form = "lower"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.393317702227432
seconds = 51.56111025810242
`````

#### `results/e0b_familiarity/scores/qwen3-1.7b__native.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-0.4630722999572754, -2.8380722999572754, -3.2130722999572754]
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "xnli"
fertility[0].form = "native"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 11.79860765788165
fertility[1].model = "qwen3-1.7b"
fertility[1].task = "sentiment"
fertility[1].form = "native"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 11.985638921453694
seconds = 65.9120557308197
`````

#### `results/e0b_familiarity/scores/qwen3-1.7b__natural.json` (545 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

`````text
content_free_logprobs.xnli = [-0.4630722999572754, -2.8380722999572754, -3.2130722999572754]
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "xnli"
fertility[0].form = "natural"
fertility[0].n_texts = 386
fertility[0].tokens_per_word = 3.5423465423465426
fertility[1].model = "qwen3-1.7b"
fertility[1].task = "sentiment"
fertility[1].form = "natural"
fertility[1].n_texts = 198
fertility[1].tokens_per_word = 3.5069712251557403
seconds = 41.86442446708679
`````

#### `results/e0b_familiarity/scores/qwen3.5-2b__english.json` (545 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-2.2064056396484375, -3.7064056396484375, -2.0814056396484375]
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.2424922333448394
fertility[1].model = "qwen3.5-2b"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.2268197573656845
seconds = 100.45982670783997
`````

#### `results/e0b_familiarity/scores/qwen3.5-2b__itrans.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-2.2064056396484375, -3.7064056396484375, -2.0814056396484375]
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "xnli"
fertility[0].form = "itrans"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.1282943809050225
fertility[1].model = "qwen3.5-2b"
fertility[1].task = "sentiment"
fertility[1].form = "itrans"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.087631887456038
seconds = 135.9841856956482
`````

#### `results/e0b_familiarity/scores/qwen3.5-2b__lossy.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-2.2064056396484375, -3.7064056396484375, -2.0814056396484375]
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "xnli"
fertility[0].form = "lossy"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 3.3431128791645945
fertility[1].model = "qwen3.5-2b"
fertility[1].task = "sentiment"
fertility[1].form = "lossy"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 3.3423212192262604
seconds = 107.09859132766724
`````

#### `results/e0b_familiarity/scores/qwen3.5-2b__lower.json` (538 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.xnli = [-2.2064056396484375, -3.7064056396484375, -2.0814056396484375]
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "xnli"
fertility[0].form = "lower"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.134012928891099
fertility[1].model = "qwen3.5-2b"
fertility[1].task = "sentiment"
fertility[1].form = "lower"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.18493552168816
seconds = 112.49107551574707
`````

#### `results/e0b_familiarity/scores/qwen3.5-2b__native.json` (541 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-2.2064056396484375, -3.7064056396484375, -2.0814056396484375]
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "xnli"
fertility[0].form = "native"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 5.230979612133267
fertility[1].model = "qwen3.5-2b"
fertility[1].task = "sentiment"
fertility[1].form = "native"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 5.235052754982415
seconds = 137.80759501457214
`````

#### `results/e0b_familiarity/scores/qwen3.5-2b__natural.json` (541 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

`````text
content_free_logprobs.xnli = [-2.2064056396484375, -3.7064056396484375, -2.0814056396484375]
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "xnli"
fertility[0].form = "natural"
fertility[0].n_texts = 386
fertility[0].tokens_per_word = 3.346283346283346
fertility[1].model = "qwen3.5-2b"
fertility[1].task = "sentiment"
fertility[1].form = "natural"
fertility[1].n_texts = 198
fertility[1].tokens_per_word = 3.32275289231682
seconds = 69.45307636260986
`````

#### `results/e0b_familiarity/scores/sarvam-1__english.json` (535 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-3.174879312515259, -5.67487907409668, -1.9248793125152588]
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "xnli"
fertility[0].form = "english"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 1.4326889886089058
fertility[1].model = "sarvam-1"
fertility[1].task = "sentiment"
fertility[1].form = "english"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 1.4204939341421143
seconds = 52.38592600822449
`````

#### `results/e0b_familiarity/scores/sarvam-1__itrans.json` (530 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-3.174879312515259, -5.67487907409668, -1.9248793125152588]
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "xnli"
fertility[0].form = "itrans"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 5.226255594231725
fertility[1].model = "sarvam-1"
fertility[1].task = "sentiment"
fertility[1].form = "itrans"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 5.238569753810082
seconds = 60.9882435798645
`````

#### `results/e0b_familiarity/scores/sarvam-1__lossy.json` (529 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-3.174879312515259, -5.67487907409668, -1.9248793125152588]
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "xnli"
fertility[0].form = "lossy"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 4.335405271009448
fertility[1].model = "sarvam-1"
fertility[1].task = "sentiment"
fertility[1].form = "lossy"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 4.357561547479484
seconds = 57.89579892158508
`````

#### `results/e0b_familiarity/scores/sarvam-1__lower.json` (527 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.xnli = [-3.174879312515259, -5.67487907409668, -1.9248793125152588]
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "xnli"
fertility[0].form = "lower"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 5.331178518150174
fertility[1].model = "sarvam-1"
fertility[1].task = "sentiment"
fertility[1].form = "lower"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 5.31242672919109
seconds = 70.2407488822937
`````

#### `results/e0b_familiarity/scores/sarvam-1__native.json` (533 bytes; first commit 20d1918 2026-10-14 22:39:12 +0530)

`````text
content_free_logprobs.xnli = [-3.174879312515259, -5.67487907409668, -1.9248793125152588]
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "xnli"
fertility[0].form = "native"
fertility[0].n_texts = 400
fertility[0].tokens_per_word = 2.1452013923421185
fertility[1].model = "sarvam-1"
fertility[1].task = "sentiment"
fertility[1].form = "native"
fertility[1].n_texts = 200
fertility[1].tokens_per_word = 2.2708089097303636
seconds = 54.95457744598389
`````

#### `results/e0b_familiarity/scores/sarvam-1__natural.json` (533 bytes; first commit 3565362 2026-10-15 16:40:24 +0530)

`````text
content_free_logprobs.xnli = [-3.174879312515259, -5.67487907409668, -1.9248793125152588]
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "xnli"
fertility[0].form = "natural"
fertility[0].n_texts = 386
fertility[0].tokens_per_word = 4.323750323750324
fertility[1].model = "sarvam-1"
fertility[1].task = "sentiment"
fertility[1].form = "natural"
fertility[1].n_texts = 198
fertility[1].tokens_per_word = 4.29219816078315
seconds = 44.358845472335815
`````

#### `results/matched/accuracy.csv` (5,954 bytes; first commit f76c726 2026-10-22 02:19:58 +0530)

| model | task | sample | form | n | acc_cal | acc_cal_ci_low | acc_cal_ci_high |
|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | all 200 (natural: 198 clean) | english | 200 | 0.985 | 0.965 | 1.0 |
| gemma4-e2b | sentiment | all 200 (natural: 198 clean) | itrans | 200 | 0.755 | 0.695 | 0.81 |
| gemma4-e2b | sentiment | all 200 (natural: 198 clean) | lossy | 200 | 0.79 | 0.73 | 0.845 |
| gemma4-e2b | sentiment | all 200 (natural: 198 clean) | lower | 200 | 0.57 | 0.5 | 0.64 |
| gemma4-e2b | sentiment | all 200 (natural: 198 clean) | native | 200 | 0.985 | 0.965 | 1.0 |
| gemma4-e2b | sentiment | all 200 (natural: 198 clean) | natural | 198 | 0.803030303030303 | 0.7474747474747475 | 0.8585858585858586 |
| qwen2.5-1.5b | sentiment | all 200 (natural: 198 clean) | english | 200 | 0.985 | 0.965 | 1.0 |
| qwen2.5-1.5b | sentiment | all 200 (natural: 198 clean) | itrans | 200 | 0.495 | 0.425 | 0.565 |
| qwen2.5-1.5b | sentiment | all 200 (natural: 198 clean) | lossy | 200 | 0.5 | 0.43 | 0.57 |
| qwen2.5-1.5b | sentiment | all 200 (natural: 198 clean) | lower | 200 | 0.47 | 0.4 | 0.54 |
| qwen2.5-1.5b | sentiment | all 200 (natural: 198 clean) | native | 200 | 0.705 | 0.64 | 0.765 |
| qwen2.5-1.5b | sentiment | all 200 (natural: 198 clean) | natural | 198 | 0.5151515151515151 | 0.4444444444444444 | 0.5858585858585859 |
| qwen3-1.7b | sentiment | all 200 (natural: 198 clean) | english | 200 | 0.985 | 0.965 | 1.0 |
| qwen3-1.7b | sentiment | all 200 (natural: 198 clean) | itrans | 200 | 0.535 | 0.465 | 0.605 |
| qwen3-1.7b | sentiment | all 200 (natural: 198 clean) | lossy | 200 | 0.57 | 0.5 | 0.64 |
| qwen3-1.7b | sentiment | all 200 (natural: 198 clean) | lower | 200 | 0.49 | 0.42 | 0.56 |
| qwen3-1.7b | sentiment | all 200 (natural: 198 clean) | native | 200 | 0.835 | 0.78 | 0.885 |
| qwen3-1.7b | sentiment | all 200 (natural: 198 clean) | natural | 198 | 0.5606060606060606 | 0.4898989898989899 | 0.6313131313131313 |
| qwen3.5-2b | sentiment | all 200 (natural: 198 clean) | english | 200 | 0.98 | 0.96 | 0.995 |
| qwen3.5-2b | sentiment | all 200 (natural: 198 clean) | itrans | 200 | 0.655 | 0.59 | 0.72 |
| qwen3.5-2b | sentiment | all 200 (natural: 198 clean) | lossy | 200 | 0.68 | 0.615 | 0.74 |
| qwen3.5-2b | sentiment | all 200 (natural: 198 clean) | lower | 200 | 0.54 | 0.47 | 0.61 |
| qwen3.5-2b | sentiment | all 200 (natural: 198 clean) | native | 200 | 0.735 | 0.67 | 0.795 |
| qwen3.5-2b | sentiment | all 200 (natural: 198 clean) | natural | 198 | 0.7222222222222222 | 0.6616161616161617 | 0.7828282828282829 |
| sarvam-1 | sentiment | all 200 (natural: 198 clean) | english | 200 | 0.98 | 0.96 | 0.995 |
| sarvam-1 | sentiment | all 200 (natural: 198 clean) | itrans | 200 | 0.82 | 0.765 | 0.87 |
| sarvam-1 | sentiment | all 200 (natural: 198 clean) | lossy | 200 | 0.895 | 0.85 | 0.935 |
| sarvam-1 | sentiment | all 200 (natural: 198 clean) | lower | 200 | 0.765 | 0.705 | 0.825 |
| sarvam-1 | sentiment | all 200 (natural: 198 clean) | native | 200 | 0.955 | 0.925 | 0.98 |
| sarvam-1 | sentiment | all 200 (natural: 198 clean) | natural | 198 | 0.8939393939393939 | 0.8484848484848485 | 0.9343434343434344 |
| gemma4-e2b | sib | 257 SIB items with natural | english | 257 | 0.8015564202334631 | 0.7509727626459144 | 0.8482490272373541 |
| gemma4-e2b | sib | 257 SIB items with natural | itrans | 257 | 0.3735408560311284 | 0.3151750972762646 | 0.43190661478599224 |
| gemma4-e2b | sib | 257 SIB items with natural | lossy | 257 | 0.48638132295719844 | 0.42412451361867703 | 0.5486381322957199 |
| gemma4-e2b | sib | 257 SIB items with natural | lower | 257 | 0.43190661478599224 | 0.3735408560311284 | 0.490272373540856 |
| gemma4-e2b | sib | 257 SIB items with natural | native | 257 | 0.7587548638132295 | 0.7042801556420234 | 0.8093385214007782 |
| gemma4-e2b | sib | 257 SIB items with natural | natural | 257 | 0.5447470817120622 | 0.48638132295719844 | 0.6070038910505836 |
| qwen2.5-1.5b | sib | 257 SIB items with natural | english | 257 | 0.8210116731517509 | 0.77431906614786 | 0.867704280155642 |
| qwen2.5-1.5b | sib | 257 SIB items with natural | itrans | 257 | 0.2529182879377432 | 0.19844357976653695 | 0.30739299610894943 |
| qwen2.5-1.5b | sib | 257 SIB items with natural | lossy | 257 | 0.3852140077821012 | 0.32684824902723736 | 0.4474708171206226 |
| qwen2.5-1.5b | sib | 257 SIB items with natural | lower | 257 | 0.26459143968871596 | 0.21011673151750973 | 0.31906614785992216 |
| qwen2.5-1.5b | sib | 257 SIB items with natural | native | 257 | 0.32684824902723736 | 0.2723735408560311 | 0.3852140077821012 |
| qwen2.5-1.5b | sib | 257 SIB items with natural | natural | 257 | 0.4591439688715953 | 0.3968871595330739 | 0.5175097276264592 |
| qwen3-1.7b | sib | 257 SIB items with natural | english | 257 | 0.7859922178988327 | 0.7354085603112841 | 0.8326848249027238 |
| qwen3-1.7b | sib | 257 SIB items with natural | itrans | 257 | 0.245136186770428 | 0.19066147859922178 | 0.29961089494163423 |
| qwen3-1.7b | sib | 257 SIB items with natural | lossy | 257 | 0.3151750972762646 | 0.25680933852140075 | 0.3735408560311284 |
| qwen3-1.7b | sib | 257 SIB items with natural | lower | 257 | 0.2490272373540856 | 0.19844357976653695 | 0.3035019455252918 |
| qwen3-1.7b | sib | 257 SIB items with natural | native | 257 | 0.669260700389105 | 0.6108949416342413 | 0.7276264591439688 |
| qwen3-1.7b | sib | 257 SIB items with natural | natural | 257 | 0.36964980544747084 | 0.311284046692607 | 0.4280155642023346 |
| qwen3.5-2b | sib | 257 SIB items with natural | english | 257 | 0.8326848249027238 | 0.7859922178988327 | 0.8754863813229572 |
| qwen3.5-2b | sib | 257 SIB items with natural | itrans | 257 | 0.25680933852140075 | 0.20233463035019456 | 0.311284046692607 |
| qwen3.5-2b | sib | 257 SIB items with natural | lossy | 257 | 0.42023346303501946 | 0.3617704280155643 | 0.4786964980544733 |
| qwen3.5-2b | sib | 257 SIB items with natural | lower | 257 | 0.3540856031128405 | 0.29571984435797666 | 0.41245136186770426 |
| qwen3.5-2b | sib | 257 SIB items with natural | native | 257 | 0.6964980544747081 | 0.6381322957198443 | 0.7509727626459144 |
| qwen3.5-2b | sib | 257 SIB items with natural | natural | 257 | 0.45525291828793774 | 0.3968871595330739 | 0.5175097276264592 |
| sarvam-1 | sib | 257 SIB items with natural | english | 257 | 0.754863813229572 | 0.7003891050583657 | 0.8054474708171206 |
| sarvam-1 | sib | 257 SIB items with natural | itrans | 257 | 0.5486381322957199 | 0.490272373540856 | 0.6108949416342413 |
| sarvam-1 | sib | 257 SIB items with natural | lossy | 257 | 0.669260700389105 | 0.6108949416342413 | 0.7237354085603113 |
| sarvam-1 | sib | 257 SIB items with natural | lower | 257 | 0.4591439688715953 | 0.40077821011673154 | 0.5214007782101168 |
| sarvam-1 | sib | 257 SIB items with natural | native | 257 | 0.7509727626459144 | 0.6964980544747081 | 0.8015564202334631 |
| sarvam-1 | sib | 257 SIB items with natural | natural | 257 | 0.7276264591439688 | 0.6731517509727627 | 0.7821011673151751 |

#### `results/matched/provenance.json` (446 bytes; first commit f76c726 2026-10-22 02:19:58 +0530)

`````text
provenance.config.status = "descriptive, 2026-10-22, no verdict"
provenance.git_commit = "c1f9aa7f6578d154a899f58b9d3a6c3c0c583883-dirty"
provenance.timestamp_utc = "2026-10-21T21:43:56+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/matched_samples.py"]
n_sib257 = 257
gate1_sentiment_check_cells = 25
`````

#### `results/matched/tokens_per_word.csv` (4,472 bytes; first commit f76c726 2026-10-22 02:19:58 +0530)

| model | dataset | form | n_texts | tokens_per_word |
|---|---|---|---|---|
| qwen2.5-1.5b | sentiment | english | 200 | 1.231369150779896 |
| qwen2.5-1.5b | sentiment | native | 200 | 11.985638921453694 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen2.5-1.5b | sentiment | lower | 200 | 4.393317702227432 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen2.5-1.5b | sentiment | natural | 198 | 3.5069712251557403 |
| qwen2.5-1.5b | sib257 | english | 257 | 1.2607260726072607 |
| qwen2.5-1.5b | sib257 | native | 257 | 11.74926398429833 |
| qwen2.5-1.5b | sib257 | itrans | 257 | 4.30765456329735 |
| qwen2.5-1.5b | sib257 | lower | 257 | 4.40161923454367 |
| qwen2.5-1.5b | sib257 | lossy | 257 | 3.534838076545633 |
| qwen2.5-1.5b | sib257 | natural | 257 | 3.4903352091999023 |
| qwen2.5-1.5b | m4c496 | english | 496 | 1.260052860109496 |
| qwen2.5-1.5b | m4c496 | native | 496 | 11.793275377141397 |
| qwen2.5-1.5b | m4c496 | itrans | 496 | 4.318205062643825 |
| qwen2.5-1.5b | m4c496 | lower | 496 | 4.401176169777551 |
| qwen2.5-1.5b | m4c496 | lossy | 496 | 3.5634108923548964 |
| qwen2.5-1.5b | m4c496 | natural | 496 | 3.528491477995421 |
| qwen3.5-2b | sentiment | english | 200 | 1.2268197573656845 |
| qwen3.5-2b | sentiment | native | 200 | 5.235052754982415 |
| qwen3.5-2b | sentiment | itrans | 200 | 4.087631887456038 |
| qwen3.5-2b | sentiment | lower | 200 | 4.18493552168816 |
| qwen3.5-2b | sentiment | lossy | 200 | 3.3423212192262604 |
| qwen3.5-2b | sentiment | natural | 198 | 3.32275289231682 |
| qwen3.5-2b | sib257 | english | 257 | 1.2574257425742574 |
| qwen3.5-2b | sib257 | native | 257 | 5.299558390578999 |
| qwen3.5-2b | sib257 | itrans | 257 | 4.162168792934249 |
| qwen3.5-2b | sib257 | lower | 257 | 4.21540726202159 |
| qwen3.5-2b | sib257 | lossy | 257 | 3.310107948969578 |
| qwen3.5-2b | sib257 | natural | 257 | 3.2877416197700025 |
| qwen3.5-2b | m4c496 | english | 496 | 1.256277138002643 |
| qwen3.5-2b | m4c496 | native | 496 | 5.304014318588596 |
| qwen3.5-2b | m4c496 | itrans | 496 | 4.173612886729737 |
| qwen3.5-2b | m4c496 | lower | 496 | 4.21439529532089 |
| qwen3.5-2b | m4c496 | lossy | 496 | 3.3359754538481208 |
| qwen3.5-2b | m4c496 | natural | 496 | 3.3270160264563726 |
| sarvam-1 | sentiment | english | 200 | 1.4204939341421143 |
| sarvam-1 | sentiment | native | 200 | 2.2708089097303636 |
| sarvam-1 | sentiment | itrans | 200 | 5.238569753810082 |
| sarvam-1 | sentiment | lower | 200 | 5.31242672919109 |
| sarvam-1 | sentiment | lossy | 200 | 4.357561547479484 |
| sarvam-1 | sentiment | natural | 198 | 4.29219816078315 |
| sarvam-1 | sib257 | english | 257 | 1.4393105977264393 |
| sarvam-1 | sib257 | native | 257 | 2.392051030421982 |
| sarvam-1 | sib257 | itrans | 257 | 5.275515210991168 |
| sarvam-1 | sib257 | lower | 257 | 5.331697742885182 |
| sarvam-1 | sib257 | lossy | 257 | 4.30225711481845 |
| sarvam-1 | sib257 | natural | 257 | 4.252997308539271 |
| sarvam-1 | m4c496 | english | 496 | 1.432603360392675 |
| sarvam-1 | m4c496 | native | 496 | 2.391332140117617 |
| sarvam-1 | m4c496 | itrans | 496 | 5.30107389414472 |
| sarvam-1 | m4c496 | lower | 496 | 5.363206341089236 |
| sarvam-1 | m4c496 | lossy | 496 | 4.343901815392483 |
| sarvam-1 | m4c496 | natural | 496 | 4.308191299923683 |
| gemma4-e2b | sentiment | english | 200 | 1.2214038128249567 |
| gemma4-e2b | sentiment | native | 200 | 3.0767878077373974 |
| gemma4-e2b | sentiment | itrans | 200 | 3.943434935521688 |
| gemma4-e2b | sentiment | lower | 200 | 4.146248534583822 |
| gemma4-e2b | sentiment | lossy | 200 | 3.2110199296600235 |
| gemma4-e2b | sentiment | natural | 198 | 3.1530703055473155 |
| gemma4-e2b | sib257 | english | 257 | 1.2444077741107444 |
| gemma4-e2b | sib257 | native | 257 | 3.2210500490677134 |
| gemma4-e2b | sib257 | itrans | 257 | 4.005152109911678 |
| gemma4-e2b | sib257 | lower | 257 | 4.134200196270854 |
| gemma4-e2b | sib257 | lossy | 257 | 3.1768891069676153 |
| gemma4-e2b | sib257 | natural | 257 | 3.123073158796183 |
| gemma4-e2b | m4c496 | english | 496 | 1.2425901453653012 |
| gemma4-e2b | m4c496 | native | 496 | 3.2280746612119664 |
| gemma4-e2b | m4c496 | itrans | 496 | 4.0164919457939146 |
| gemma4-e2b | m4c496 | lower | 496 | 4.139989772436717 |
| gemma4-e2b | m4c496 | lossy | 496 | 3.20429557657888 |
| gemma4-e2b | m4c496 | natural | 496 | 3.163825998473671 |
| qwen3-1.7b | sentiment | english | 200 | 1.231369150779896 |
| qwen3-1.7b | sentiment | native | 200 | 11.985638921453694 |
| qwen3-1.7b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen3-1.7b | sentiment | lower | 200 | 4.393317702227432 |
| qwen3-1.7b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen3-1.7b | sentiment | natural | 198 | 3.5069712251557403 |
| qwen3-1.7b | sib257 | english | 257 | 1.2607260726072607 |
| qwen3-1.7b | sib257 | native | 257 | 11.74926398429833 |
| qwen3-1.7b | sib257 | itrans | 257 | 4.30765456329735 |
| qwen3-1.7b | sib257 | lower | 257 | 4.40161923454367 |
| qwen3-1.7b | sib257 | lossy | 257 | 3.534838076545633 |
| qwen3-1.7b | sib257 | natural | 257 | 3.4903352091999023 |
| qwen3-1.7b | m4c496 | english | 496 | 1.260052860109496 |
| qwen3-1.7b | m4c496 | native | 496 | 11.793275377141397 |
| qwen3-1.7b | m4c496 | itrans | 496 | 4.318205062643825 |
| qwen3-1.7b | m4c496 | lower | 496 | 4.401176169777551 |
| qwen3-1.7b | m4c496 | lossy | 496 | 3.5634108923548964 |
| qwen3-1.7b | m4c496 | natural | 496 | 3.528491477995421 |

## Not dumped (item-level, binary or too large; path and size only)

- `results/e0b_familiarity/gate1.log`: .log file, 8,802 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/gemma4-e2b__english.parquet`: .parquet file, 25,272 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/gemma4-e2b__itrans.parquet`: .parquet file, 25,532 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/gemma4-e2b__lossy.parquet`: .parquet file, 25,495 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/gemma4-e2b__lower.parquet`: .parquet file, 25,596 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/gemma4-e2b__native.parquet`: .parquet file, 25,564 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/gemma4-e2b__natural.parquet`: .parquet file, 25,053 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen2.5-1.5b__english.parquet`: .parquet file, 25,135 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen2.5-1.5b__itrans.parquet`: .parquet file, 25,326 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen2.5-1.5b__lossy.parquet`: .parquet file, 25,148 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen2.5-1.5b__lower.parquet`: .parquet file, 25,295 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen2.5-1.5b__native.parquet`: .parquet file, 25,730 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen2.5-1.5b__natural.parquet`: .parquet file, 24,728 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3-1.7b__english.parquet`: .parquet file, 25,251 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3-1.7b__itrans.parquet`: .parquet file, 25,370 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3-1.7b__lossy.parquet`: .parquet file, 25,293 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3-1.7b__lower.parquet`: .parquet file, 25,346 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3-1.7b__native.parquet`: .parquet file, 25,875 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3-1.7b__natural.parquet`: .parquet file, 24,851 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3.5-2b__english.parquet`: .parquet file, 24,889 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3.5-2b__itrans.parquet`: .parquet file, 24,900 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3.5-2b__lossy.parquet`: .parquet file, 24,827 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3.5-2b__lower.parquet`: .parquet file, 24,954 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3.5-2b__native.parquet`: .parquet file, 25,310 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/qwen3.5-2b__natural.parquet`: .parquet file, 24,427 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/sarvam-1__english.parquet`: .parquet file, 24,822 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/sarvam-1__itrans.parquet`: .parquet file, 24,900 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/sarvam-1__lossy.parquet`: .parquet file, 24,895 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/sarvam-1__lower.parquet`: .parquet file, 24,993 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/sarvam-1__native.parquet`: .parquet file, 25,030 bytes (binary or per-item data, not dumped)
- `results/e0b_familiarity/scores/sarvam-1__natural.parquet`: .parquet file, 24,524 bytes (binary or per-item data, not dumped)

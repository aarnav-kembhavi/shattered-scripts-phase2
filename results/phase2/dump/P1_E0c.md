# E0c: SIB-200 topic classification (Phase 1)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| registered | `ba54695` | 2026-10-16 02:29:27 +0530 | 833-868 | PRE-REGISTRATION — E0c SIB-200 topic classification (written 2026-10-16, before any SIB-200 item is scored) |
| result | `5e0ded5` | 2026-10-17 05:01:13 +0530 | 1119-1188 | 2026-10-17 — E0c SIB-200 topic classification (registered 2026-10-16): P-a partly supported, P-b inconclusive |

## Values observed in the result files (read from the files' own columns and keys)

- models: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
- forms: lossy, lower, itrans, native, english, natural257
- tasks: sib

Result directories: `results/e0c_sib`

## RESULTS.md entries, verbatim

##### PRE-REGISTRATION — E0c SIB-200 topic classification (written 2026-10-16, before any SIB-200 item is scored)

RESULTS.md lines 833 to 868; first line committed in `ba54695` on 2026-10-16 02:29:27 +0530; last line in `d21d633` on 2026-10-16 02:59:11 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — E0c SIB-200 topic classification (written 2026-10-16, before any SIB-200 item is scored)
`scripts/e0c_sib.py`.
- **Data:** Davlan/sib200 (revision 38977a6, CC-BY-SA 4.0, not gated; Adelani et al., EACL 2024). Kannada and
  English, train + dev + test = 1,004 sentences, 7 topics. `index_id` is the 0-based position in FLORES dev + devtest.
  All 1,004 Kannada and all 1,004 English sentences equal our FLORES+ text at that position after NFC, and the labels
  and IDs agree across the two languages (`results/e0c_sib/verify.json`). So the native, ITRANS and English inputs are
  exactly the M4 inputs, and lossy = to_lossy(native) as in E0b.
- **Scoring:** the E0b setup unchanged. Log-likelihood of English label words (" science", " travel", " politics",
  " sports", " health", " entertainment", " geography"; template `e0_sib_v1`), BOS always prepended, primary
  calibration = mean of content-free "N/A", "", "[MASK]", raw fallback if a model's calibrated English accuracy is more
  than 5 points below raw. Five models (Qwen2.5-1.5B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B, Qwen3-1.7B) × four forms
  (English, native, ITRANS, lossy). 95% bootstrap CI (10,000) on every cell; constant-label rates reported.
- **Informative model:** English accuracy ≥ chance + 5 points (14.3% + 5).
- **P-a (as in E0b):** native > ITRANS and native > lossy in every informative model. Paired McNemar, Holm over all
  native-vs-ITRANS and native-vs-lossy tests of informative models. **Supported** if every difference is positive and
  significant. **Refuted** if any difference is significantly negative, or none is significant. Otherwise **partly
  supported**, with the count given.
- **P-b (within form):** within native and within ITRANS, sentences that are better retrieved against English in M4 are
  classified correctly more often. Cells: the four M4 models × {native, ITRANS}. Sentences: the 515 SIB sentences in
  the M4b test half (seed-0 split), so neither M4b's layer choice nor its mapping was fitted on them.
  - **Predictor:** the rank of the true English sentence among the 1,005 test-half English sentences, using unmapped
    cosine at M4b's train-half best unmapped layer (**primary**). The secondary predictor is the same rank after
    M4b's ridge map at its train-half best mapped layer and alpha.
  - **Model:** logistic regression of correctness (primary calibrated prediction) on z(−log rank) + z(log tokens of
    the sentence in that form and model). One-sided test that the rank coefficient is > 0, Holm across counted cells,
    separately for the primary and the secondary predictor. Descriptively, accuracy among sentences retrieved at
    rank 1 vs not.
  - **Counted cells:** the model is informative and the cell's constant-label rate is ≤ 90%. The other cells are
    reported but not counted.
  - **Verdict (primary):** **supported** if the coefficient is > 0 in every counted cell and significant in at least
    half. **Refuted** if it is ≤ 0 in at least half. Otherwise **inconclusive**.
- **Exploratory:** lossy vs ITRANS (McNemar, separate Holm family).
- **Pilot:** 30 random items × 4 forms on Qwen2.5 and Gemma 4 for timing only. Their accuracies are not looked at for
  any decision.

---
`````

##### 2026-10-17 — E0c SIB-200 topic classification (registered 2026-10-16): P-a partly supported, P-b inconclusive

RESULTS.md lines 1119 to 1188; first line committed in `5e0ded5` on 2026-10-17 05:01:13 +0530; last line in `7d86cfc` on 2026-10-21 22:22:48 +0530; labels from the title and parent heading: result

`````text
## 2026-10-17 — E0c SIB-200 topic classification (registered 2026-10-16): P-a partly supported, P-b inconclusive
`scripts/e0c_sib.py`.
- **Run.** Scoring resumed from the cache: 15 model × form pairs, 02:03–04:59 IST, in the detached `e0c_chain.sh`.
  The analysis ran at the end of the same chain. Outputs are in `results/e0c_sib/gate/`.
- **Provenance.** The commit reads e56a80e-dirty; the only uncommitted files were the chain status and log.
- **Setup.** n = 1,004 per cell, chance 14.3%. The calibrated (average-of-3) prediction is primary everywhere, with no
  raw fallback (`calibration_fallback.csv`). All 5 models are informative.

Accuracy [95% CI]:

| model | English | native | ITRANS | lossy | tokens/word native |
|---|---|---|---|---|---|
| Qwen2.5-1.5B | 0.797 [0.772, 0.822] | 0.336 [0.307, 0.366] | 0.278 [0.250, 0.306] | 0.367 [0.337, 0.396] | 11.8 |
| Qwen3-1.7B | 0.782 [0.756, 0.807] | 0.672 [0.643, 0.701] | 0.240 [0.213, 0.266] | 0.307 [0.279, 0.336] | 11.8 |
| Qwen3.5-2B | 0.804 [0.779, 0.829] | 0.676 [0.647, 0.705] | 0.241 [0.215, 0.268] | 0.375 [0.347, 0.406] | 5.3 |
| Sarvam-1 | 0.768 [0.742, 0.794] | 0.766 [0.740, 0.792] | 0.539 [0.508, 0.571] | 0.705 [0.677, 0.733] | 2.4 |
| Gemma 4 E2B | 0.794 [0.769, 0.819] | 0.750 [0.723, 0.776] | 0.367 [0.337, 0.396] | 0.497 [0.466, 0.528] | 3.3 |

Constant-label rates (calibrated):
- native 0.20–0.24, except Qwen2.5 at 0.43;
- ITRANS 0.26–0.53;
- lossy 0.23–0.38.

**P-a: partly supported (9 of 10 differences positive and significant).**
- Native > ITRANS is significant in all 5 models (Holm): +0.06 (Qwen2.5), +0.43, +0.44, +0.23 and +0.38.
- Native > lossy is significant in 4 models: +0.37 (Qwen3), +0.30 (Qwen3.5), +0.06 (Sarvam-1), +0.25 (Gemma 4).
- **The miss is Qwen2.5, native vs lossy:** −0.031 (124 vs 155 discordant, p_holm = 0.072, not significant). This is
  the model whose native script is most fragmented (11.8 tokens per word) and barely aligned with English in M4
  (unmapped 0.178).
- The rule needed every difference positive and significant for "supported". No difference is significantly negative,
  so it is not refuted.
- Outcome against Gate 1 (sentiment): the same pattern. Native beats the romanized forms everywhere it is clearly
  above floor. Qwen2.5 is the only model where native comprehension is itself near floor.

**Exploratory, lossy vs ITRANS (separate Holm family):** lossy > ITRANS in all 5 models, all significant: +0.09,
+0.07, +0.13, +0.17 and +0.13. This repeats the Gate 1 refutation of P3. The lossless, more fragmented ITRANS is the
worse romanization, so information loss does not explain the romanization penalty.

**P-b: primary verdict inconclusive.**
- 8 counted cells: 4 M4 models × {native, ITRANS}, n = 515. All are informative, with constant-label rate ≤ 0.52.
- Logistic regression of correctness on z(−log rank) + z(log tokens); rank coefficient β, one-sided, Holm.

| model | native β (p_holm) | native share at rank 1 | ITRANS β (p_holm) | ITRANS share at rank 1 |
|---|---|---|---|---|
| Qwen2.5 | +0.184 (0.098) | 0.186 | +0.359 (0.001) ✓ | 0.064 |
| Qwen3.5 | −0.064 (1.0) | 0.977 | +0.669 (<0.001) ✓ | 0.117 |
| Sarvam-1 | −0.287 (1.0) | 0.942 | +0.406 (<0.001) ✓ | 0.520 |
| Gemma 4 | +0.143 (0.192) | 0.994 | +0.369 (0.001) ✓ | 0.262 |

- β > 0 in 6 of 8 cells, significant in 4, all of them ITRANS. β ≤ 0 in 2, both native.
- "Supported" needed β > 0 in every cell, so the verdict is inconclusive; "refuted" needed ≤ 0 in at least half.
- **Within ITRANS the prediction holds in all four models.** Accuracy when the sentence is retrieved at rank 1 vs not:
  - Qwen2.5: 0.39 vs 0.29;
  - Qwen3.5: 0.48 vs 0.21;
  - Sarvam-1: 0.60 vs 0.43;
  - Gemma 4: 0.51 vs 0.33.
- **Within native it is untestable in three models.** 94–99% of the sentences are retrieved at rank 1 (Qwen3.5,
  Sarvam-1, Gemma 4), so the predictor barely varies. In Qwen2.5 native it is positive but not significant after Holm.
  This explanation is post hoc: the registered rule did not exclude ceiling cells.
- **Secondary predictor (rank after the M4b ridge map):** significant only in Sarvam-1 ITRANS (β = 0.230,
  p_holm = 0.046). Mapped retrieval predicts accuracy less well than unmapped. This fits the M4b and surface results,
  where the ITRANS map works mostly at the lexical surface.

**Summary.**
- SIB-200 replicates Gate 1 on a second task, with the identical M4 sentences: native > romanized and lossy > ITRANS.
- Within a form, where retrieval against English varies (ITRANS), the sentences the model aligns with English are the
  ones it classifies correctly. This holds with token count held fixed, in all four models. It is the item-level link
  between the M4 alignment measure and accuracy that the earlier fragmentation regression did not find.

---
`````

## Result files, every number

#### `results/e0c_sib/gate/accuracy.csv` (7,703 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

| model | task | form | n | chance | acc_cal | acc_cal_ci_low | acc_cal_ci_high | constant_label_rate_cal | acc_raw | acc_raw_ci_low | acc_raw_ci_high | constant_label_rate_raw | acc_na | acc_na_ci_low | acc_na_ci_high | constant_label_rate_na | acc_avg3 | acc_avg3_ci_low | acc_avg3_ci_high | constant_label_rate_avg3 | tokens_per_word |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sib | english | 1004 | 0.14285714285714285 | 0.7938247011952191 | 0.7689243027888446 | 0.8187250996015937 | 0.20916334661354583 | 0.8007968127490039 | 0.7758964143426295 | 0.8256972111553785 | 0.21314741035856574 | 0.8007968127490039 | 0.7758964143426295 | 0.8256972111553785 | 0.2151394422310757 | 0.7938247011952191 | 0.7689243027888446 | 0.8187250996015937 | 0.20916334661354583 | 1.2353487077165792 |
| gemma4-e2b | sib | itrans | 1004 | 0.14285714285714285 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.2549800796812749 | 0.3904382470119522 | 0.3605577689243028 | 0.4213147410358566 | 0.28286852589641437 | 0.38247011952191234 | 0.35258964143426297 | 0.4123505976095618 | 0.2968127490039841 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.2549800796812749 | 4.003865336658354 |
| gemma4-e2b | sib | lossy | 1004 | 0.14285714285714285 | 0.49701195219123506 | 0.46613545816733065 | 0.5278884462151394 | 0.22709163346613545 | 0.5139442231075697 | 0.48306772908366535 | 0.545816733067729 | 0.2290836653386454 | 0.499003984063745 | 0.4681274900398406 | 0.5308764940239044 | 0.23207171314741035 | 0.49701195219123506 | 0.46613545816733065 | 0.5278884462151394 | 0.22709163346613545 | 3.174127182044888 |
| gemma4-e2b | sib | native | 1004 | 0.14285714285714285 | 0.75 | 0.7231075697211156 | 0.7759213147410354 | 0.19820717131474103 | 0.7619521912350598 | 0.7360557768924303 | 0.7878486055776892 | 0.2051792828685259 | 0.7539840637450199 | 0.7270916334661355 | 0.7808764940239044 | 0.2061752988047809 | 0.75 | 0.7231075697211156 | 0.7759213147410354 | 0.19820717131474103 | 3.2502493765586036 |
| qwen2.5-1.5b | sib | english | 1004 | 0.14285714285714285 | 0.796812749003984 | 0.7719123505976095 | 0.8217131474103586 | 0.18725099601593626 | 0.7141434262948207 | 0.6862549800796812 | 0.7420318725099602 | 0.29382470119521914 | 0.8077689243027888 | 0.7828685258964143 | 0.8316733067729084 | 0.20219123505976094 | 0.796812749003984 | 0.7719123505976095 | 0.8217131474103586 | 0.18725099601593626 | 1.2547909609762888 |
| qwen2.5-1.5b | sib | itrans | 1004 | 0.14285714285714285 | 0.2778884462151394 | 0.25 | 0.3057768924302789 | 0.4312749003984064 | 0.18725099601593626 | 0.16334661354581673 | 0.21215139442231076 | 0.8306772908366534 | 0.3157370517928287 | 0.2868525896414343 | 0.3456175298804781 | 0.3097609561752988 | 0.2778884462151394 | 0.25 | 0.3057768924302789 | 0.4312749003984064 | 4.307793017456359 |
| qwen2.5-1.5b | sib | lossy | 1004 | 0.14285714285714285 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.351593625498008 | 0.2798804780876494 | 0.25298804780876494 | 0.30876494023904383 | 0.6892430278884463 | 0.40039840637450197 | 0.3705179282868526 | 0.4312749003984064 | 0.24402390438247012 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.351593625498008 | 3.5341645885286783 |
| qwen2.5-1.5b | sib | native | 1004 | 0.14285714285714285 | 0.33565737051792827 | 0.30677290836653387 | 0.3655378486055777 | 0.43227091633466136 | 0.23207171314741035 | 0.2061752988047809 | 0.2589641434262948 | 0.7430278884462151 | 0.37350597609561753 | 0.3436254980079681 | 0.4043824701195219 | 0.3426294820717131 | 0.33565737051792827 | 0.30677290836653387 | 0.3655378486055777 | 0.43227091633466136 | 11.760536159600997 |
| qwen3-1.7b | sib | english | 1004 | 0.14285714285714285 | 0.7818725099601593 | 0.7559760956175299 | 0.8067729083665338 | 0.20916334661354583 | 0.7848605577689243 | 0.7589641434262948 | 0.8097609561752988 | 0.19621513944223107 | 0.7808764940239044 | 0.7549800796812749 | 0.8057768924302788 | 0.2061752988047809 | 0.7818725099601593 | 0.7559760956175299 | 0.8067729083665338 | 0.20916334661354583 | 1.2547909609762888 |
| qwen3-1.7b | sib | itrans | 1004 | 0.14285714285714285 | 0.2400398406374502 | 0.21314741035856574 | 0.2659611553784857 | 0.5189243027888446 | 0.2559760956175299 | 0.2290836653386454 | 0.28286852589641437 | 0.5 | 0.23705179282868527 | 0.21115537848605578 | 0.26294820717131473 | 0.48705179282868527 | 0.2400398406374502 | 0.21314741035856574 | 0.2659611553784857 | 0.5189243027888446 | 4.307793017456359 |
| qwen3-1.7b | sib | lossy | 1004 | 0.14285714285714285 | 0.30677290836653387 | 0.2788844621513944 | 0.33565737051792827 | 0.34063745019920316 | 0.30876494023904383 | 0.2798804780876494 | 0.3386454183266932 | 0.35358565737051795 | 0.299800796812749 | 0.27091633466135456 | 0.3286852589641434 | 0.3595617529880478 | 0.30677290836653387 | 0.2788844621513944 | 0.33565737051792827 | 0.34063745019920316 | 3.5341645885286783 |
| qwen3-1.7b | sib | native | 1004 | 0.14285714285714285 | 0.6723107569721115 | 0.6434262948207171 | 0.701195219123506 | 0.20219123505976094 | 0.6842629482071713 | 0.6543824701195219 | 0.7131474103585658 | 0.1902390438247012 | 0.6593625498007968 | 0.6304780876494024 | 0.6882470119521913 | 0.22211155378486055 | 0.6723107569721115 | 0.6434262948207171 | 0.701195219123506 | 0.20219123505976094 | 11.760536159600997 |
| qwen3.5-2b | sib | english | 1004 | 0.14285714285714285 | 0.8037848605577689 | 0.7788844621513944 | 0.8286852589641435 | 0.2400398406374502 | 0.7280876494023905 | 0.700199203187251 | 0.7549800796812749 | 0.2410358565737052 | 0.8057768924302788 | 0.7808764940239044 | 0.8296812749003984 | 0.2589641434262948 | 0.8037848605577689 | 0.7788844621513944 | 0.8286852589641435 | 0.2400398406374502 | 1.2509860331307132 |
| qwen3.5-2b | sib | itrans | 1004 | 0.14285714285714285 | 0.2410358565737052 | 0.2151394422310757 | 0.2679282868525896 | 0.5318725099601593 | 0.14840637450199204 | 0.12749003984063745 | 0.17031872509960158 | 0.8814741035856574 | 0.2798804780876494 | 0.25199203187250996 | 0.30876494023904383 | 0.299800796812749 | 0.2410358565737052 | 0.2151394422310757 | 0.2679282868525896 | 0.5318725099601593 | 4.167643391521197 |
| qwen3.5-2b | sib | lossy | 1004 | 0.14285714285714285 | 0.3754980079681275 | 0.3466135458167331 | 0.4063745019920319 | 0.3804780876494024 | 0.26593625498007967 | 0.23904382470119523 | 0.29382470119521914 | 0.7460159362549801 | 0.4123505976095618 | 0.38247011952191234 | 0.44322709163346613 | 0.2689243027888446 | 0.3754980079681275 | 0.3466135458167331 | 0.4063745019920319 | 0.3804780876494024 | 3.3111596009975064 |
| qwen3.5-2b | sib | native | 1004 | 0.14285714285714285 | 0.6762948207171314 | 0.647410358565737 | 0.7051792828685259 | 0.20119521912350596 | 0.5756972111553785 | 0.5448207171314741 | 0.6055776892430279 | 0.40936254980079684 | 0.7101593625498008 | 0.6822709163346613 | 0.7380478087649402 | 0.2101593625498008 | 0.6762948207171314 | 0.647410358565737 | 0.7051792828685259 | 0.20119521912350596 | 5.314214463840399 |
| sarvam-1 | sib | english | 1004 | 0.14285714285714285 | 0.7679282868525896 | 0.7420318725099602 | 0.7938247011952191 | 0.26294820717131473 | 0.5737051792828686 | 0.5428286852589641 | 0.6045816733067729 | 0.398406374501992 | 0.7539840637450199 | 0.7270916334661355 | 0.7808764940239044 | 0.33167330677290835 | 0.7679282868525896 | 0.7420318725099602 | 0.7938247011952191 | 0.26294820717131473 | 1.4350146164911142 |
| sarvam-1 | sib | itrans | 1004 | 0.14285714285714285 | 0.5388446215139442 | 0.5079681274900398 | 0.5707171314741036 | 0.4452191235059761 | 0.3247011952191235 | 0.2958167330677291 | 0.3545816733067729 | 0.5428286852589641 | 0.4940239043824701 | 0.4631474103585657 | 0.5249003984063745 | 0.6384462151394422 | 0.5388446215139442 | 0.5079681274900398 | 0.5707171314741036 | 0.4452191235059761 | 5.287842892768079 |
| sarvam-1 | sib | lossy | 1004 | 0.14285714285714285 | 0.7051792828685259 | 0.6772908366533864 | 0.7330677290836654 | 0.2340637450199203 | 0.46115537848605576 | 0.4312749003984064 | 0.49203187250996017 | 0.41932270916334663 | 0.7101593625498008 | 0.6822709163346613 | 0.7380478087649402 | 0.33067729083665337 | 0.7051792828685259 | 0.6772908366533864 | 0.7330677290836654 | 0.2340637450199203 | 4.313528678304239 |
| sarvam-1 | sib | native | 1004 | 0.14285714285714285 | 0.7659362549800797 | 0.7400398406374502 | 0.7918326693227091 | 0.2360557768924303 | 0.6454183266932271 | 0.6155378486055777 | 0.6752988047808764 | 0.3147410358565737 | 0.7739043824701195 | 0.74800796812749 | 0.798804780876494 | 0.2729083665338645 | 0.7659362549800797 | 0.7400398406374502 | 0.7918326693227091 | 0.2360557768924303 | 2.3889650872817954 |

#### `results/e0c_sib/gate/calibration_fallback.csv` (344 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

| model | task | english_raw | english_avg3 | use_raw |
|---|---|---|---|---|
| gemma4-e2b | sib | 0.8007968127490039 | 0.7938247011952191 | False |
| qwen2.5-1.5b | sib | 0.7141434262948207 | 0.796812749003984 | False |
| qwen3-1.7b | sib | 0.7848605577689243 | 0.7818725099601593 | False |
| qwen3.5-2b | sib | 0.7280876494023905 | 0.8037848605577689 | False |
| sarvam-1 | sib | 0.5737051792828686 | 0.7679282868525896 | False |

#### `results/e0c_sib/gate/mcnemar.csv` (1,543 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

| model | task | a | b | acc_a | acc_b | n | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sib | native | itrans | 0.75 | 0.3665338645418327 | 1004 | 0.3834661354581673 | 425 | 40 | 2.5188719631954495e-82 | 2.0150975705563596e-81 | True |
| gemma4-e2b | sib | native | lossy | 0.75 | 0.49701195219123506 | 1004 | 0.25298804780876494 | 293 | 39 | 2.668515711757834e-49 | 1.334257855878917e-48 | True |
| qwen2.5-1.5b | sib | native | itrans | 0.33565737051792827 | 0.2778884462151394 | 1004 | 0.05776892430278885 | 159 | 101 | 0.00038780629202563347 | 0.0007756125840512669 | True |
| qwen2.5-1.5b | sib | native | lossy | 0.33565737051792827 | 0.3665338645418327 | 1004 | -0.03087649402390441 | 124 | 155 | 0.07229593171431895 | 0.07229593171431895 | False |
| qwen3-1.7b | sib | native | itrans | 0.6723107569721115 | 0.2400398406374502 | 1004 | 0.4322709163346613 | 456 | 22 | 1.2990189533010863e-106 | 1.2990189533010864e-105 | True |
| qwen3-1.7b | sib | native | lossy | 0.6723107569721115 | 0.30677290836653387 | 1004 | 0.36553784860557764 | 398 | 31 | 2.529451058538525e-82 | 2.0150975705563596e-81 | True |
| qwen3.5-2b | sib | native | itrans | 0.6762948207171314 | 0.2410358565737052 | 1004 | 0.43525896414342624 | 462 | 25 | 2.8113371589728562e-105 | 2.5302034430755707e-104 | True |
| qwen3.5-2b | sib | native | lossy | 0.6762948207171314 | 0.3754980079681275 | 1004 | 0.30079681274900394 | 345 | 43 | 1.1158511919563684e-59 | 6.695107151738211e-59 | True |
| sarvam-1 | sib | native | itrans | 0.7659362549800797 | 0.5388446215139442 | 1004 | 0.22709163346613548 | 299 | 71 | 2.123868442850549e-34 | 8.495473771402196e-34 | True |
| sarvam-1 | sib | native | lossy | 0.7659362549800797 | 0.7051792828685259 | 1004 | 0.06075697211155373 | 126 | 65 | 1.2058675268138053e-05 | 3.617602580441416e-05 | True |

#### `results/e0c_sib/gate/mcnemar_exploratory.csv` (817 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

| model | task | a | b | acc_a | acc_b | n | diff | a_only | b_only | p | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sib | lossy | itrans | 0.49701195219123506 | 0.3665338645418327 | 1004 | 0.13047808764940239 | 203 | 72 | 1.2852237490631325e-15 | 3.855671247189398e-15 | True |
| qwen2.5-1.5b | sib | lossy | itrans | 0.3665338645418327 | 0.2778884462151394 | 1004 | 0.08864541832669326 | 166 | 77 | 1.1431301135982122e-08 | 2.2862602271964243e-08 | True |
| qwen3-1.7b | sib | lossy | itrans | 0.30677290836653387 | 0.2400398406374502 | 1004 | 0.06673306772908366 | 123 | 56 | 6.053759985241233e-07 | 6.053759985241233e-07 | True |
| qwen3.5-2b | sib | lossy | itrans | 0.3754980079681275 | 0.2410358565737052 | 1004 | 0.1344621513944223 | 180 | 45 | 2.5793608864659074e-20 | 1.031744354586363e-19 | True |
| sarvam-1 | sib | lossy | itrans | 0.7051792828685259 | 0.5388446215139442 | 1004 | 0.16633466135458175 | 232 | 65 | 3.6266614299672425e-23 | 1.8133307149836213e-22 | True |

#### `results/e0c_sib/gate/pb_cells.csv` (3,771 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

| model | form | retrieval | layer | n | counted | constant_label_rate | accuracy | retrieved_at1 | n_retrieved | acc_if_retrieved | acc_if_not_retrieved | median_rank | beta | se | p_one_sided | fit_ok | p_holm | significant |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen2.5-1.5b | native | unmapped | 15 | 515 | True | 0.429126213592233 | 0.34563106796116505 | 0.18640776699029127 | 96 | 0.4895833333333333 | 0.3126491646778043 | 86.0 | 0.18364197945250843 | 0.09334423896758653 | 0.02457070229531331 | True | 0.09828280918125323 | False |
| qwen2.5-1.5b | native | mapped | 1 | 515 | True | 0.429126213592233 | 0.34563106796116505 | 0.5495145631067961 | 283 | 0.3745583038869258 | 0.3103448275862069 | 1.0 | 0.19276061379326914 | 0.09917643933039175 | 0.025971070298573228 | True | 0.18179749209001259 | False |
| qwen2.5-1.5b | itrans | unmapped | 1 | 515 | True | 0.44271844660194176 | 0.29320388349514565 | 0.06407766990291262 | 33 | 0.3939393939393939 | 0.2863070539419087 | 103.0 | 0.35854005833672 | 0.09613737037711012 | 9.594694134570206e-05 | True | 0.0005139149782419686 | True |
| qwen2.5-1.5b | itrans | mapped | 1 | 515 | True | 0.44271844660194176 | 0.29320388349514565 | 0.5514563106796116 | 284 | 0.30985915492957744 | 0.2727272727272727 | 1.0 | 0.08997088755179476 | 0.10134117418320725 | 0.18732365886668778 | True | 0.9366182943334389 | False |
| qwen3.5-2b | native | unmapped | 15 | 515 | True | 0.20194174757281552 | 0.6737864077669903 | 0.9766990291262136 | 503 | 0.6719681908548708 | 0.75 | 1.0 | -0.06370169249877508 | 0.1039942796689513 | 0.7299130250225645 | True | 1.0 | False |
| qwen3.5-2b | native | mapped | 7 | 515 | True | 0.20194174757281552 | 0.6737864077669903 | 0.9650485436893204 | 497 | 0.676056338028169 | 0.6111111111111112 | 1.0 | -0.007061251972137678 | 0.09472134749248233 | 0.5297126783700703 | True | 1.0 | False |
| qwen3.5-2b | itrans | unmapped | 6 | 515 | True | 0.5223300970873787 | 0.2446601941747573 | 0.11650485436893204 | 60 | 0.48333333333333334 | 0.21318681318681318 | 44.0 | 0.66872850142407 | 0.10776367278208007 | 2.7259978799137734e-10 | True | 2.1807983039310187e-09 | True |
| qwen3.5-2b | itrans | mapped | 3 | 515 | True | 0.5223300970873787 | 0.2446601941747573 | 0.5067961165048543 | 261 | 0.2720306513409962 | 0.21653543307086615 | 1.0 | 0.19651713934838352 | 0.11125427498134184 | 0.0386661999057882 | True | 0.23199719943472918 | False |
| sarvam-1 | native | unmapped | 23 | 515 | True | 0.21359223300970873 | 0.7572815533980582 | 0.941747572815534 | 485 | 0.7505154639175258 | 0.8666666666666667 | 1.0 | -0.28720520565624463 | 0.1807862894564733 | 0.9439297004854689 | True | 1.0 | False |
| sarvam-1 | native | mapped | 26 | 515 | True | 0.21359223300970873 | 0.7572815533980582 | 0.916504854368932 | 472 | 0.7584745762711864 | 0.7441860465116279 | 1.0 | -0.006259901088759196 | 0.10438945420883801 | 0.5239089599213669 | True | 1.0 | False |
| sarvam-1 | itrans | unmapped | 21 | 515 | True | 0.4388349514563107 | 0.5223300970873787 | 0.5203883495145631 | 268 | 0.6044776119402985 | 0.4331983805668016 | 1.0 | 0.4058589713287531 | 0.09497406082178819 | 9.627178554750305e-06 | True | 6.739024988325213e-05 | True |
| sarvam-1 | itrans | mapped | 24 | 515 | True | 0.4388349514563107 | 0.5223300970873787 | 0.3766990291262136 | 194 | 0.5773195876288659 | 0.48909657320872274 | 3.0 | 0.23024769121946084 | 0.09102544766671788 | 0.005711469442947017 | True | 0.045691755543576136 | True |
| gemma4-e2b | native | unmapped | 7 | 515 | True | 0.22330097087378642 | 0.7650485436893204 | 0.9941747572815534 | 512 | 0.767578125 | 0.3333333333333333 | 1.0 | 0.1425895944964386 | 0.09365948263619767 | 0.06395123659252713 | True | 0.1918537097775814 | False |
| gemma4-e2b | native | mapped | 8 | 515 | True | 0.22330097087378642 | 0.7650485436893204 | 0.970873786407767 | 500 | 0.77 | 0.6 | 1.0 | 0.05847996959149546 | 0.09397556193342786 | 0.26687588752799035 | True | 1.0 | False |
| gemma4-e2b | itrans | unmapped | 7 | 515 | True | 0.24854368932038834 | 0.3786407766990291 | 0.2621359223300971 | 135 | 0.5111111111111111 | 0.33157894736842103 | 9.0 | 0.36920849473684314 | 0.09824708097377871 | 8.565249637366144e-05 | True | 0.0005139149782419686 | True |
| gemma4-e2b | itrans | mapped | 0 | 515 | True | 0.24854368932038834 | 0.3786407766990291 | 0.4854368932038835 | 250 | 0.372 | 0.3849056603773585 | 2.0 | -0.06541220759205002 | 0.09172097933685823 | 0.7621282211096545 | True | 1.0 | False |

#### `results/e0c_sib/gate/verdicts.json` (6,183 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
provenance.config.dataset = "Davlan/sib200@38977a667f6fc264d5c26ec57a01e16db040b358"
provenance.config.n_items = 1004
provenance.config.models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
provenance.config.forms = ["english", "native", "itrans", "lossy"]
provenance.config.template = "e0_sib_v1"
provenance.config.verbalizers = "loglik.VERBALIZERS['sib']"
provenance.config.calibration = "mean of content-free N/A, '', [MASK]; raw fallback if English drops > 5 pts"
provenance.config.bos = "always prepended"
provenance.config.pb_split = "M4b seed-0 test half"
provenance.config.registered = "RESULTS.md 2026-10-16 (E0c)"
provenance.git_commit = "e56a80e3a081fcf90d29e367c7fa9109f50e1631-dirty"
provenance.timestamp_utc = "2026-10-16T23:28:09+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0c_sib.py", "analyse"]
informative_models = ["qwen2.5-1.5b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
P_a = "partly supported"
P_a_tests[0].model = "gemma4-e2b"
P_a_tests[0].task = "sib"
P_a_tests[0].a = "native"
P_a_tests[0].b = "itrans"
P_a_tests[0].acc_a = 0.75
P_a_tests[0].acc_b = 0.3665338645418327
P_a_tests[0].n = 1004
P_a_tests[0].diff = 0.3834661354581673
P_a_tests[0].a_only = 425
P_a_tests[0].b_only = 40
P_a_tests[0].p = 2.5188719631954495e-82
P_a_tests[0].p_holm = 2.0150975705563596e-81
P_a_tests[0].significant = true
P_a_tests[1].model = "gemma4-e2b"
P_a_tests[1].task = "sib"
P_a_tests[1].a = "native"
P_a_tests[1].b = "lossy"
P_a_tests[1].acc_a = 0.75
P_a_tests[1].acc_b = 0.49701195219123506
P_a_tests[1].n = 1004
P_a_tests[1].diff = 0.25298804780876494
P_a_tests[1].a_only = 293
P_a_tests[1].b_only = 39
P_a_tests[1].p = 2.668515711757834e-49
P_a_tests[1].p_holm = 1.334257855878917e-48
P_a_tests[1].significant = true
P_a_tests[2].model = "qwen2.5-1.5b"
P_a_tests[2].task = "sib"
P_a_tests[2].a = "native"
P_a_tests[2].b = "itrans"
P_a_tests[2].acc_a = 0.33565737051792827
P_a_tests[2].acc_b = 0.2778884462151394
P_a_tests[2].n = 1004
P_a_tests[2].diff = 0.05776892430278885
P_a_tests[2].a_only = 159
P_a_tests[2].b_only = 101
P_a_tests[2].p = 0.00038780629202563347
P_a_tests[2].p_holm = 0.0007756125840512669
P_a_tests[2].significant = true
P_a_tests[3].model = "qwen2.5-1.5b"
P_a_tests[3].task = "sib"
P_a_tests[3].a = "native"
P_a_tests[3].b = "lossy"
P_a_tests[3].acc_a = 0.33565737051792827
P_a_tests[3].acc_b = 0.3665338645418327
P_a_tests[3].n = 1004
P_a_tests[3].diff = -0.03087649402390441
P_a_tests[3].a_only = 124
P_a_tests[3].b_only = 155
P_a_tests[3].p = 0.07229593171431895
P_a_tests[3].p_holm = 0.07229593171431895
P_a_tests[3].significant = false
P_a_tests[4].model = "qwen3-1.7b"
P_a_tests[4].task = "sib"
P_a_tests[4].a = "native"
P_a_tests[4].b = "itrans"
P_a_tests[4].acc_a = 0.6723107569721115
P_a_tests[4].acc_b = 0.2400398406374502
P_a_tests[4].n = 1004
P_a_tests[4].diff = 0.4322709163346613
P_a_tests[4].a_only = 456
P_a_tests[4].b_only = 22
P_a_tests[4].p = 1.2990189533010863e-106
P_a_tests[4].p_holm = 1.2990189533010864e-105
P_a_tests[4].significant = true
P_a_tests[5].model = "qwen3-1.7b"
P_a_tests[5].task = "sib"
P_a_tests[5].a = "native"
P_a_tests[5].b = "lossy"
P_a_tests[5].acc_a = 0.6723107569721115
P_a_tests[5].acc_b = 0.30677290836653387
P_a_tests[5].n = 1004
P_a_tests[5].diff = 0.36553784860557764
P_a_tests[5].a_only = 398
P_a_tests[5].b_only = 31
P_a_tests[5].p = 2.529451058538525e-82
P_a_tests[5].p_holm = 2.0150975705563596e-81
P_a_tests[5].significant = true
P_a_tests[6].model = "qwen3.5-2b"
P_a_tests[6].task = "sib"
P_a_tests[6].a = "native"
P_a_tests[6].b = "itrans"
P_a_tests[6].acc_a = 0.6762948207171314
P_a_tests[6].acc_b = 0.2410358565737052
P_a_tests[6].n = 1004
P_a_tests[6].diff = 0.43525896414342624
P_a_tests[6].a_only = 462
P_a_tests[6].b_only = 25
P_a_tests[6].p = 2.8113371589728562e-105
P_a_tests[6].p_holm = 2.5302034430755707e-104
P_a_tests[6].significant = true
P_a_tests[7].model = "qwen3.5-2b"
P_a_tests[7].task = "sib"
P_a_tests[7].a = "native"
P_a_tests[7].b = "lossy"
P_a_tests[7].acc_a = 0.6762948207171314
P_a_tests[7].acc_b = 0.3754980079681275
P_a_tests[7].n = 1004
P_a_tests[7].diff = 0.30079681274900394
P_a_tests[7].a_only = 345
P_a_tests[7].b_only = 43
P_a_tests[7].p = 1.1158511919563684e-59
P_a_tests[7].p_holm = 6.695107151738211e-59
P_a_tests[7].significant = true
P_a_tests[8].model = "sarvam-1"
P_a_tests[8].task = "sib"
P_a_tests[8].a = "native"
P_a_tests[8].b = "itrans"
P_a_tests[8].acc_a = 0.7659362549800797
P_a_tests[8].acc_b = 0.5388446215139442
P_a_tests[8].n = 1004
P_a_tests[8].diff = 0.22709163346613548
P_a_tests[8].a_only = 299
P_a_tests[8].b_only = 71
P_a_tests[8].p = 2.123868442850549e-34
P_a_tests[8].p_holm = 8.495473771402196e-34
P_a_tests[8].significant = true
P_a_tests[9].model = "sarvam-1"
P_a_tests[9].task = "sib"
P_a_tests[9].a = "native"
P_a_tests[9].b = "lossy"
P_a_tests[9].acc_a = 0.7659362549800797
P_a_tests[9].acc_b = 0.7051792828685259
P_a_tests[9].n = 1004
P_a_tests[9].diff = 0.06075697211155373
P_a_tests[9].a_only = 126
P_a_tests[9].b_only = 65
P_a_tests[9].p = 1.2058675268138053e-05
P_a_tests[9].p_holm = 3.617602580441416e-05
P_a_tests[9].significant = true
P_b_primary_unmapped = "inconclusive"
P_b_cells_counted = 8
P_b_secondary_mapped[0].model = "qwen2.5-1.5b"
P_b_secondary_mapped[0].form = "native"
P_b_secondary_mapped[0].beta = 0.19276061379326914
P_b_secondary_mapped[0].p_holm = 0.18179749209001259
P_b_secondary_mapped[1].model = "qwen2.5-1.5b"
P_b_secondary_mapped[1].form = "itrans"
P_b_secondary_mapped[1].beta = 0.08997088755179476
P_b_secondary_mapped[1].p_holm = 0.9366182943334389
P_b_secondary_mapped[2].model = "qwen3.5-2b"
P_b_secondary_mapped[2].form = "native"
P_b_secondary_mapped[2].beta = -0.007061251972137678
P_b_secondary_mapped[2].p_holm = 1.0
P_b_secondary_mapped[3].model = "qwen3.5-2b"
P_b_secondary_mapped[3].form = "itrans"
P_b_secondary_mapped[3].beta = 0.19651713934838352
P_b_secondary_mapped[3].p_holm = 0.23199719943472918
P_b_secondary_mapped[4].model = "sarvam-1"
P_b_secondary_mapped[4].form = "native"
P_b_secondary_mapped[4].beta = -0.006259901088759196
P_b_secondary_mapped[4].p_holm = 1.0
P_b_secondary_mapped[5].model = "sarvam-1"
P_b_secondary_mapped[5].form = "itrans"
P_b_secondary_mapped[5].beta = 0.23024769121946084
P_b_secondary_mapped[5].p_holm = 0.045691755543576136
P_b_secondary_mapped[6].model = "gemma4-e2b"
P_b_secondary_mapped[6].form = "native"
P_b_secondary_mapped[6].beta = 0.05847996959149546
P_b_secondary_mapped[6].p_holm = 1.0
P_b_secondary_mapped[7].model = "gemma4-e2b"
P_b_secondary_mapped[7].form = "itrans"
P_b_secondary_mapped[7].beta = -0.06541220759205002
P_b_secondary_mapped[7].p_holm = 1.0
`````

#### `results/e0c_sib/scores/cf_gemma4-e2b.json` (612 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
N/A.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
sib = [-2.4877829551696777, -3.8627829551696777, -5.550282955169678, -8.675283432006836, -5.550282955169678, -9.237783432006836, -5.675282955169678]
[MASK].sib = [-0.5948385000228882, -3.2198386192321777, -3.9698386192321777, -8.46983814239502, -4.094838619232178, -4.594838619232178, -4.844838619232178]
`````

#### `results/e0c_sib/scores/cf_qwen2.5-1.5b.json` (605 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
N/A.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
sib = [-2.681217670440674, -5.681217670440674, -7.056217670440674, -6.806217670440674, -3.931217670440674, -6.181217670440674, -1.4312175512313843]
[MASK].sib = [-3.935457706451416, -4.685457706451416, -4.435457706451416, -6.810457706451416, -2.435457706451416, -5.560457706451416, -0.310457706451416]
`````

#### `results/e0c_sib/scores/cf_qwen3-1.7b.json` (607 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
N/A.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
sib = [-0.616732656955719, -7.866732597351074, -5.616732597351074, -5.491732597351074, -8.116732597351074, -3.991732597351074, -4.741732597351074]
[MASK].sib = [-0.1491338461637497, -8.274133682250977, -3.6491339206695557, -3.1491339206695557, -5.649133682250977, -3.6491339206695557, -5.024133682250977]
`````

#### `results/e0c_sib/scores/cf_qwen3.5-2b.json` (614 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
N/A.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
sib = [-2.0323567390441895, -2.5323567390441895, -4.0948567390441895, -3.4073567390441895, -3.5948567390441895, -4.1573567390441895, -1.282356858253479]
[MASK].sib = [-2.0298879146575928, -2.7798879146575928, -4.279888153076172, -3.2798879146575928, -3.2798879146575928, -4.342388153076172, -1.9048879146575928]
`````

#### `results/e0c_sib/scores/cf_sarvam-1.json` (604 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
N/A.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
sib = [-1.7176564931869507, -3.2176566123962402, -3.7176566123962402, -4.71765661239624, -3.4676566123962402, -5.468843460083008, -0.9693723320960999]
[MASK].sib = [-1.23140287399292, -2.98140287399292, -3.73140287399292, -4.73140287399292, -3.48140287399292, -4.849200248718262, -1.0999197959899902]
`````

#### `results/e0c_sib/scores/gemma4-e2b__english.json` (421 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "english"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.2353487077165792
seconds = 947.087456703186
`````

#### `results/e0c_sib/scores/gemma4-e2b__itrans.json` (420 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.003865336658354
seconds = 949.5947008132935
`````

#### `results/e0c_sib/scores/gemma4-e2b__lossy.json` (419 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 3.174127182044888
seconds = 934.2984056472778
`````

#### `results/e0c_sib/scores/gemma4-e2b__lower.json` (419 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "lower"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.120885286783042
seconds = 708.9085204601288
`````

#### `results/e0c_sib/scores/gemma4-e2b__native.json` (421 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 3.2502493765586036
seconds = 933.5922472476959
`````

#### `results/e0c_sib/scores/gemma4-e2b__natural257.json` (424 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "natural257"
fertility[0].n_texts = 257
fertility[0].tokens_per_word = 3.123073158796183
seconds = 179.32358241081238
`````

#### `results/e0c_sib/scores/qwen2.5-1.5b__english.json` (421 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "english"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.2547909609762888
seconds = 344.20590138435364
`````

#### `results/e0c_sib/scores/qwen2.5-1.5b__itrans.json` (419 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.307793017456359
seconds = 392.99561381340027
`````

#### `results/e0c_sib/scores/qwen2.5-1.5b__lossy.json` (419 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 3.5341645885286783
seconds = 375.28615283966064
`````

#### `results/e0c_sib/scores/qwen2.5-1.5b__lower.json` (416 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "lower"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.379364089775561
seconds = 378.128146648407
`````

#### `results/e0c_sib/scores/qwen2.5-1.5b__native.json` (419 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 11.760536159600997
seconds = 525.7924020290375
`````

#### `results/e0c_sib/scores/qwen2.5-1.5b__natural257.json` (422 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "natural257"
fertility[0].n_texts = 257
fertility[0].tokens_per_word = 3.4903352091999023
seconds = 96.57636952400208
`````

#### `results/e0c_sib/scores/qwen3-1.7b__english.json` (418 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "english"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.2547909609762888
seconds = 463.12289214134216
`````

#### `results/e0c_sib/scores/qwen3-1.7b__itrans.json` (416 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.307793017456359
seconds = 415.52500653266907
`````

#### `results/e0c_sib/scores/qwen3-1.7b__lossy.json` (416 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 3.5341645885286783
seconds = 454.96290040016174
`````

#### `results/e0c_sib/scores/qwen3-1.7b__lower.json` (415 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "lower"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.379364089775561
seconds = 341.47905230522156
`````

#### `results/e0c_sib/scores/qwen3-1.7b__native.json` (416 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 11.760536159600997
seconds = 538.8889856338501
`````

#### `results/e0c_sib/scores/qwen3-1.7b__natural257.json` (419 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "natural257"
fertility[0].n_texts = 257
fertility[0].tokens_per_word = 3.4903352091999023
seconds = 85.64839959144592
`````

#### `results/e0c_sib/scores/qwen3.5-2b__english.json` (417 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "english"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.2509860331307132
seconds = 672.0790822505951
`````

#### `results/e0c_sib/scores/qwen3.5-2b__itrans.json` (415 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.167643391521197
seconds = 882.4301385879517
`````

#### `results/e0c_sib/scores/qwen3.5-2b__lossy.json` (415 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 3.3111596009975064
seconds = 886.5720937252045
`````

#### `results/e0c_sib/scores/qwen3.5-2b__lower.json` (414 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "lower"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.200561097256858
seconds = 842.4802198410034
`````

#### `results/e0c_sib/scores/qwen3.5-2b__native.json` (415 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 5.314214463840399
seconds = 959.3784322738647
`````

#### `results/e0c_sib/scores/qwen3.5-2b__natural257.json` (420 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "natural257"
fertility[0].n_texts = 257
fertility[0].tokens_per_word = 3.2877416197700025
seconds = 157.09868669509888
`````

#### `results/e0c_sib/scores/sarvam-1__english.json` (417 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "english"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.4350146164911142
seconds = 452.11667108535767
`````

#### `results/e0c_sib/scores/sarvam-1__itrans.json` (414 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 5.287842892768079
seconds = 545.6303536891937
`````

#### `results/e0c_sib/scores/sarvam-1__lossy.json` (413 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.313528678304239
seconds = 493.5927724838257
`````

#### `results/e0c_sib/scores/sarvam-1__lower.json` (414 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "lower"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 5.3287406483790525
seconds = 531.1507604122162
`````

#### `results/e0c_sib/scores/sarvam-1__native.json` (416 bytes; first commit 5e0ded5 2026-10-17 05:01:13 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.3889650872817954
seconds = 456.44608974456787
`````

#### `results/e0c_sib/scores/sarvam-1__natural257.json` (418 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "natural257"
fertility[0].n_texts = 257
fertility[0].tokens_per_word = 4.252997308539271
seconds = 118.37132906913757
`````

#### `results/e0c_sib/scores_pilot/cf_gemma4-e2b.json` (612 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
N/A.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
sib = [-2.4877829551696777, -3.8627829551696777, -5.550282955169678, -8.675283432006836, -5.550282955169678, -9.237783432006836, -5.675282955169678]
[MASK].sib = [-0.5948385000228882, -3.2198386192321777, -3.9698386192321777, -8.46983814239502, -4.094838619232178, -4.594838619232178, -4.844838619232178]
`````

#### `results/e0c_sib/scores_pilot/cf_qwen2.5-1.5b.json` (605 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
N/A.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
sib = [-2.681217670440674, -5.681217670440674, -7.056217670440674, -6.806217670440674, -3.931217670440674, -6.181217670440674, -1.4312175512313843]
[MASK].sib = [-3.935457706451416, -4.685457706451416, -4.435457706451416, -6.810457706451416, -2.435457706451416, -5.560457706451416, -0.310457706451416]
`````

#### `results/e0c_sib/scores_pilot/gemma4-e2b__english.json` (420 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "english"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 1.245583038869258
seconds = 27.152202367782593
`````

#### `results/e0c_sib/scores_pilot/gemma4-e2b__itrans.json` (420 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 3.9758771929824563
seconds = 23.472219228744507
`````

#### `results/e0c_sib/scores_pilot/gemma4-e2b__lossy.json` (418 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 3.168859649122807
seconds = 22.830742359161377
`````

#### `results/e0c_sib/scores_pilot/gemma4-e2b__native.json` (420 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 3.1666666666666665
seconds = 23.761407613754272
`````

#### `results/e0c_sib/scores_pilot/qwen2.5-1.5b__english.json` (419 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "english"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 1.2720848056537102
seconds = 11.093295335769653
`````

#### `results/e0c_sib/scores_pilot/qwen2.5-1.5b__itrans.json` (417 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 4.241228070175438
seconds = 10.627235651016235
`````

#### `results/e0c_sib/scores_pilot/qwen2.5-1.5b__lossy.json` (416 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 3.482456140350877
seconds = 10.707854747772217
`````

#### `results/e0c_sib/scores_pilot/qwen2.5-1.5b__native.json` (418 bytes; first commit d518063 2026-10-16 03:23:45 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 30
fertility[0].tokens_per_word = 11.903508771929825
seconds = 15.988689661026001
`````

#### `results/e0c_sib/verify.json` (1,074 bytes; first commit ba54695 2026-10-16 02:29:27 +0530)

`````text
provenance.config.dataset = "Davlan/sib200@38977a667f6fc264d5c26ec57a01e16db040b358"
provenance.git_commit = "e190b90993813f1e01ecdd3836c0e33c181cd09c-dirty"
provenance.timestamp_utc = "2026-10-15T20:58:43+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/e0c_sib.py", "verify"]
kan_Knda.n = 1004
kan_Knda.unique_ids = 1004
kan_Knda.text_equal_at_index = 1004
kan_Knda.nfc_changed = 8
kan_Knda.categories.science/technology = 252
kan_Knda.categories.travel = 198
kan_Knda.categories.politics = 146
kan_Knda.categories.sports = 122
kan_Knda.categories.health = 110
kan_Knda.categories.entertainment = 93
kan_Knda.categories.geography = 83
eng_Latn.n = 1004
eng_Latn.unique_ids = 1004
eng_Latn.text_equal_at_index = 1004
eng_Latn.nfc_changed = 0
eng_Latn.categories.science/technology = 252
eng_Latn.categories.travel = 198
eng_Latn.categories.politics = 146
eng_Latn.categories.sports = 122
eng_Latn.categories.health = 110
eng_Latn.categories.entertainment = 93
eng_Latn.categories.geography = 83
labels_and_ids_equal_kn_en = true
`````

## Not dumped (item-level, binary or too large; path and size only)

- `results/e0c_sib/gate/pb_items.csv`: 4,120 data rows, columns ['model', 'form', 'id', 'label', 'pred_cal', 'correct', 'rank_unmapped', 'rank_mapped', 'n_tokens'] (item-level file, not dumped)
- `results/e0c_sib/scores/gemma4-e2b__english.parquet`: .parquet file, 113,764 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/gemma4-e2b__itrans.parquet`: .parquet file, 122,291 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/gemma4-e2b__lossy.parquet`: .parquet file, 122,233 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/gemma4-e2b__lower.parquet`: .parquet file, 122,357 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/gemma4-e2b__native.parquet`: .parquet file, 119,689 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/gemma4-e2b__natural257.parquet`: .parquet file, 35,770 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen2.5-1.5b__english.parquet`: .parquet file, 120,200 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen2.5-1.5b__itrans.parquet`: .parquet file, 118,967 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen2.5-1.5b__lossy.parquet`: .parquet file, 119,232 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen2.5-1.5b__lower.parquet`: .parquet file, 118,723 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen2.5-1.5b__native.parquet`: .parquet file, 119,808 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen2.5-1.5b__natural257.parquet`: .parquet file, 35,082 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3-1.7b__english.parquet`: .parquet file, 120,931 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3-1.7b__itrans.parquet`: .parquet file, 121,955 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3-1.7b__lossy.parquet`: .parquet file, 121,959 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3-1.7b__lower.parquet`: .parquet file, 121,969 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3-1.7b__native.parquet`: .parquet file, 122,904 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3-1.7b__natural257.parquet`: .parquet file, 35,712 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3.5-2b__english.parquet`: .parquet file, 117,561 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3.5-2b__itrans.parquet`: .parquet file, 115,419 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3.5-2b__lossy.parquet`: .parquet file, 116,692 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3.5-2b__lower.parquet`: .parquet file, 116,090 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3.5-2b__native.parquet`: .parquet file, 118,255 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/qwen3.5-2b__natural257.parquet`: .parquet file, 34,470 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/sarvam-1__english.parquet`: .parquet file, 118,316 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/sarvam-1__itrans.parquet`: .parquet file, 117,449 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/sarvam-1__lossy.parquet`: .parquet file, 117,900 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/sarvam-1__lower.parquet`: .parquet file, 116,998 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/sarvam-1__native.parquet`: .parquet file, 119,235 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores/sarvam-1__natural257.parquet`: .parquet file, 34,948 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/gemma4-e2b__english.parquet`: .parquet file, 10,023 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/gemma4-e2b__itrans.parquet`: .parquet file, 10,227 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/gemma4-e2b__lossy.parquet`: .parquet file, 10,166 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/gemma4-e2b__native.parquet`: .parquet file, 10,142 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/qwen2.5-1.5b__english.parquet`: .parquet file, 10,123 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/qwen2.5-1.5b__itrans.parquet`: .parquet file, 10,068 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/qwen2.5-1.5b__lossy.parquet`: .parquet file, 10,110 bytes (binary or per-item data, not dumped)
- `results/e0c_sib/scores_pilot/qwen2.5-1.5b__native.parquet`: .parquet file, 10,061 bytes (binary or per-item data, not dumped)

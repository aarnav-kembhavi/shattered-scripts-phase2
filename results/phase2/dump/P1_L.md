# L: Romanization ladder L1 to L3 (Phase 1)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| registered | `93a9f68` | 2026-10-22 01:03:02 +0530 | 1319-1389 | PRE-REGISTRATION — Romanization ladder L1–L3 (written 2026-10-22, Aarnav's design; before any ladder form is run or scored) |
| result | `64ca06d` | 2026-10-22 03:14:00 +0530 | 1523-1578 | 2026-10-22 — Romanization ladder L1–L3 (registered 2026-10-22): results |
| post hoc, result | `f676f15` | 2026-10-22 18:09:29 +0530 | 1708-1731 | 2026-10-22 — L1 casing: post hoc note (post hoc descriptive, 2026-10-22, no verdict) |
| post hoc, result | `70fe375` | 2026-10-22 20:33:33 +0530 | 1794-1838 | 2026-10-22 — L3 on items with no English words in natural; net ITRANS → lossy on retrieval and SIB (post hoc descriptive, 2026-10-22, no verdict) |
| post hoc, result | `40de234` | 2026-10-22 23:55:36 +0530 | 1896-1969 | 2026-10-22 — NC1 and ladder: independent frequency reference, item-level decomposition, ladder piece familiarity (post hoc descriptive, 2026-10-22, no verdict) |

## Values observed in the result files (read from the files' own columns and keys)

- models: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
- forms: lossy, lower, itrans, native, english, natural, natural257
- tasks: sib, xnli, sentiment, sentiment (200)
- measures: sib, retrieval, sentiment, sib_L3_secondary, xnli_reported_only

Result directories: `results/l_ladder`, `results/l_ladder_posthoc`

## RESULTS.md entries, verbatim

##### PRE-REGISTRATION — Romanization ladder L1–L3 (written 2026-10-22, Aarnav's design; before any ladder form is run or scored)

RESULTS.md lines 1319 to 1389; first line committed in `93a9f68` on 2026-10-22 01:03:02 +0530; last line in `cd6a097` on 2026-10-22 02:14:18 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — Romanization ladder L1–L3 (written 2026-10-22, Aarnav's design; before any ladder form is run or scored)
Script `scripts/l_ladder.py` (written after this registration, before any run). Question: within romanized Kannada,
does casing, fragmentation or human spelling move alignment and accuracy? Four romanized forms, each step changing one
factor:

| form | capitals | tokens per word | spelling |
|---|---|---|---|
| ITRANS (our scheme) | yes | high | mechanical |
| **lowercase lossless** (E9 `universal|lower`) | no | high, about ITRANS | mechanical |
| lossy (`to_lossy`) | no | low | mechanical |
| natural (Gemini, natural_romanization_v1) | no | low, about lossy | human |

**Lowercase scheme: E9 `universal|lower`** (`results/e09_romanize/best_schemes.json`). Reasons: it is lossless (E9:
2009/2009 FLORES+ and 1048/1048 Wikipedia round trips; also 496/496 on the M4c sample, checked 2026-10-22), it uses
no capitals for Kannada units, and its sentence-level token count on FLORES+ is within about 2% of ITRANS on every
study tokenizer (`results/e09_romanize/savings.csv`: Qwen3.5 −0.0%, Qwen2.5/3 +0.9%, Sarvam-1 +0.4%, Gemma 4 +2.1%).
Its search objective covered o200k, Gemma 4, Qwen3.5 and Qwen3, not Sarvam-1. Three rare units use non-letters:
ಃ → `:`, ಽ → `'`, ಁ → `n~`. In the 496 M4c sentences: ಃ occurs 8 times (8 sentences); ಽ and ಁ do not occur. Latin text
already in the Kannada source keeps its case in every form (23 of the 496 sentences contain an ASCII capital in native).

**Contrasts (no directional predictions):**
- **L1 casing:** lowercase lossless − ITRANS. Check: tokens per word about equal.
- **L2 fragmentation:** lossy − lowercase lossless. Check: tokens per word differ. Confound, stated now: lossy also
  loses information (vowel length, retroflex/dental, etc.; E2 CER 3.09%), so L2 mixes fragmentation with information
  loss (and lossy's dropped distinctions are partly the ones informal spelling also drops).
- **L3 spelling familiarity:** natural − lossy. Check: tokens per word about equal.
- Tokens-per-word check, reported **per model** (and per dataset: M4c 496 sentences, sentiment, SIB-200): "about
  equal" if the two forms are within 10% of each other (relative to the second form); "differ" if lossy is at least
  10% below lowercase. The check is descriptive: a model that fails it is flagged in the verdict, not dropped.

**Counted models.** Qwen2.5-1.5B is reported in every table but **never counted**: its native-script baseline is at
floor (M4 unmapped native retrieval 0.178 on the M4b test half; SIB-200 native 0.336; it barely understands Kannada in
its own script), so differences between romanizations in it cannot say how a model that does read Kannada treats them.
- **Retrieval:** Qwen3.5-2B, Sarvam-1, Gemma 4 E2B. **Effect** if significant (below) in **at least 2 of 3**, same sign.
- **Accuracy:** Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B. **Effect** if significant in **at least 3 of 4**, same
  sign.
- Otherwise "no effect detected". Where an effect is found its sign is reported; there is no directional prediction.

**Measures that count.**
1. **Unmapped retrieval** against English (M4), on the M4c sample (496 retained sentences, M4c's seed-0 split, 248
   train / 248 test): test-half acc@1 at the train-half best unmapped layer, chosen per model × form, exactly as M4c.
   Needs new forward passes (lossy and lowercase on the 500 M4c sentences, 4 models; vectors as in M4).
2. **Accuracy, sentiment** (E0b items, 200; natural n = 198 after the 9 defective natural texts are dropped, so L3 is
   paired on 198). Lowercase is a new form scored on 5 models; the other forms reuse the Gate 1 scores.
3. **Accuracy, SIB-200** (E0c, 1,004) for L1 and L2. Lowercase is a new form scored on 5 models.
   **L3 on SIB-200 is secondary:** natural exists only for the M4c sample, so L3 uses the M4c ∩ SIB overlap,
   **n = 257** (natural scored on those 257 items in 5 models; lossy reused).
   **L3 accuracy has low power** (198 sentiment items, 257 SIB items, and at Gate 1 natural and lossy were within a few
   points of each other); a "no effect detected" on L3 accuracy is weak evidence of no effect.
- Accuracy scoring is the E0b/E0c setup unchanged: log-likelihood of the label words, BOS always, primary calibration =
  mean of "N/A", "", "[MASK]" with the raw fallback rule (decided per model × task by English, so lowercase follows the
  existing row decisions).
- **Reported only:** XNLI accuracy (all three contrasts; no verdict), the surface baseline (L0, Lb, gain, status as in
  the 2026-10-17 registration, ridge only) for all four forms plus native, mapped retrieval, tokens per word.

**Statistics.** For every model × contrast × measure: the paired difference with a 95% paired bootstrap CI (10,000
resamples over sentences/items) and an exact McNemar test on per-item correctness (retrieval hit or classification
correct). **Holm within each measure, across 3 contrasts × counted models:** retrieval 9 tests; sentiment 12;
SIB-200 L1–L2 8; SIB-200 L3 (secondary) 4. A difference is **significant** if its Holm-adjusted p < 0.05 (the
Holm-corrected counterpart of "CI excludes 0"); unadjusted CIs are reported alongside, and any disagreement between
the CI and the Holm decision is reported. Qwen2.5 cells get the same statistics outside the Holm families.

**Verdicts reported** per contrast and per measure (L1–L3 × retrieval, sentiment, SIB-200; L3 SIB-200 secondary);
measures are not combined into one verdict. Context, not a prediction: at Gate 1 natural ≈ lossy on accuracy, which
hints that at equal fragmentation human spelling adds little; M4c found natural > ITRANS on alignment, which the
ladder splits into L1 + L2 + L3.

**Order:** pilot (one model, timing), then forward passes and scoring detached (one model load at a time), then
analysis. Estimated GPU time from logged runs: about 1.7 h.

---
`````

##### 2026-10-22 — Romanization ladder L1–L3 (registered 2026-10-22): results

RESULTS.md lines 1523 to 1578; first line committed in `64ca06d` on 2026-10-22 03:14:00 +0530; last line in `83c256e` on 2026-10-22 17:55:12 +0530; labels from the title and parent heading: result

`````text
## 2026-10-22 — Romanization ladder L1–L3 (registered 2026-10-22): results
Run: detached `scripts/l_chain.sh` (forward 01:52, scoring, analysis finished 03:12 IST); `scripts/l_ladder.py`.
Outputs `results/l_ladder/{verdict.json, contrasts.csv, retrieval.csv, accuracy.csv, tokens_per_word.csv,
tokens_per_word_checks.csv}`; log `results/l_ladder.log`. Lowercase = E9 `universal|lower`.

**Tokens-per-word checks: all 60 passed** (5 models × 5 datasets × applicable contrasts; `tokens_per_word_checks.csv`).
Tokens per word, ITRANS / lowercase / lossy / natural (`tokens_per_word.csv`):

| model | M4c 496 | sentiment | SIB 1,004 (no natural) | SIB 257 (lossy / natural) |
|---|---|---|---|---|
| Qwen2.5-1.5B (not counted) | 4.32 / 4.40 / 3.56 / 3.53 | 4.23 / 4.39 / 3.57 / 3.51 | 4.31 / 4.38 / 3.53 | 3.53 / 3.49 |
| Qwen3-1.7B (same tokenizer) | 4.32 / 4.40 / 3.56 / 3.53 | 4.23 / 4.39 / 3.57 / 3.51 | 4.31 / 4.38 / 3.53 | 3.53 / 3.49 |
| Qwen3.5-2B | 4.17 / 4.21 / 3.34 / 3.33 | 4.09 / 4.18 / 3.34 / 3.32 | 4.17 / 4.20 / 3.31 | 3.31 / 3.29 |
| Sarvam-1 | 5.30 / 5.36 / 4.34 / 4.31 | 5.24 / 5.31 / 4.36 / 4.29 | 5.29 / 5.33 / 4.31 | 4.30 / 4.25 |
| Gemma 4 E2B | 4.02 / 4.14 / 3.20 / 3.16 | 3.94 / 4.15 / 3.21 / 3.15 | 4.00 / 4.12 / 3.17 | 3.18 / 3.12 |

**Registered verdicts** (significant = Holm-adjusted exact McNemar p < 0.05 within the measure; effect needs ≥ 2 of 3
counted models for retrieval, ≥ 3 of 4 for accuracy, same sign):

| contrast | retrieval (M4c test half, n = 248) | sentiment (n = 200; L3 n = 198) | SIB-200 (n = 1,004; L3 secondary n = 257) |
|---|---|---|---|
| **L1 casing** (lowercase − ITRANS) | **no effect detected** (0 of 3) | **no effect detected** (0 positive, 2 negative of 4) | **no effect detected** (2 positive, 1 negative of 4) |
| **L2 fragmentation** (lossy − lowercase) | **effect, positive** (3 of 3) | **effect, positive** (3 of 4) | **effect, positive** (4 of 4) |
| **L3 spelling** (natural − lossy) | **effect, positive** (2 of 3) | **no effect detected** (0 of 4) | secondary: **no effect detected** (0 of 4) |

Per counted model: difference [95% paired bootstrap CI], Holm p (`contrasts.csv`):

| measure | contrast | Qwen3-1.7B | Qwen3.5-2B | Sarvam-1 | Gemma 4 E2B |
|---|---|---|---|---|---|
| retrieval | L1 | — | +0.077 [+0.020, +0.137], 0.058 | −0.069 [−0.125, −0.012], 0.081 | −0.040 [−0.109, +0.024], 0.295 |
| retrieval | L2 | — | +0.109 [+0.044, +0.173], 0.0065 | +0.266 [+0.206, +0.327], <0.0001 | +0.169 [+0.101, +0.238], <0.0001 |
| retrieval | L3 | — | +0.137 [+0.081, +0.194], <0.0001 | +0.036 [+0.004, +0.069], 0.098 | +0.137 [+0.081, +0.198], 0.0001 |
| sentiment | L1 | −0.045 [−0.145, +0.050], 1.0 | −0.115 [−0.180, −0.055], 0.0048 | −0.055 [−0.115, +0.010], 0.82 | −0.185 [−0.250, −0.120], <0.0001 |
| sentiment | L2 | +0.080 [−0.020, +0.180], 0.87 | +0.140 [+0.075, +0.205], 0.0009 | +0.130 [+0.065, +0.195], 0.0020 | +0.220 [+0.155, +0.285], <0.0001 |
| sentiment | L3 | −0.005 [−0.076, +0.066], 1.0 | +0.040 [−0.025, +0.106], 1.0 | 0.000 [−0.040, +0.040], 1.0 | +0.015 [−0.035, +0.066], 1.0 |
| SIB | L1 | +0.001 [−0.026, +0.027], 1.0 | +0.055 [+0.026, +0.084], 0.0009 | −0.043 [−0.074, −0.012], 0.017 | +0.048 [+0.017, +0.080], 0.0093 |
| SIB | L2 | +0.066 [+0.038, +0.095], <0.0001 | +0.080 [+0.048, +0.112], <0.0001 | +0.209 [+0.176, +0.243], <0.0001 | +0.083 [+0.052, +0.114], <0.0001 |
| SIB 257 | L3 | +0.055 [+0.008, +0.101], 0.10 | +0.035 [−0.012, +0.086], 0.21 | +0.058 [+0.016, +0.105], 0.067 | +0.058 [+0.000, +0.117], 0.13 |

Qwen2.5 (reported, not counted; unadjusted): retrieval L1 0.000, L2 +0.069, L3 +0.177; sentiment L1 −0.025, L2 +0.030,
L3 +0.020; SIB L1 −0.003, L2 +0.092, SIB-257 L3 +0.074 (CIs in `contrasts.csv`). XNLI (reported only) is in
`contrasts.csv` (`xnli_reported_only`); most cells are near chance.

**CI vs Holm disagreements** (registered: Holm decides; reported here): the unadjusted CI excludes 0 but Holm p ≥ 0.05
for retrieval L1 in Qwen3.5 (+0.077) and Sarvam-1 (−0.069), retrieval L3 in Sarvam-1 (+0.036), and SIB-257 L3 in
Sarvam-1 (+0.058) and Qwen3 (+0.055). None changes a verdict except that, counted by CIs instead of Holm, retrieval L1
would have 1 positive and 1 negative (still no effect) and SIB-257 L3 would have 2 of 4 (still no effect).

**Deviations.** (1) The timing pilot used two models (Qwen2.5 and Gemma 4), not one; its 30-item SIB scores were
written to a throwaway directory and deleted without being looked at. (2) Before any run, a performance bug in the new
script (FLORES forms rebuilt 500 times) was fixed; no method changed. No other deviation.

**Registered confound (unchanged):** L2 changes information as well as fragmentation (lossy drops distinctions), so a
positive L2 is not attributable to fragmentation alone. L3 accuracy has low power (198 and 257 items).

---
`````

##### 2026-10-22 — L1 casing: post hoc note (post hoc descriptive, 2026-10-22, no verdict)

RESULTS.md lines 1708 to 1731; first line committed in `f676f15` on 2026-10-22 18:09:29 +0530; last line in `5127d0d` on 2026-10-22 18:17:44 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-22 — L1 casing: post hoc note (post hoc descriptive, 2026-10-22, no verdict)
The registered L1 verdict stays **no effect detected** on all three measures. Descriptively
(`results/l_ladder/{tokens_per_word_checks.csv, contrasts.csv}`): casing changed tokens per word by only **+0.8% to
+5.1%** (all models and datasets; L2 changed it by −18.0% to −23.0%), yet it moved **sentiment by −0.115 (Qwen3.5-2B,
Holm p 0.0048) and −0.185 (Gemma 4 E2B, Holm p 6.3e−7)**, and **SIB with mixed signs** (Qwen3.5 +0.055, Gemma 4
+0.048, Sarvam-1 −0.043, all Holm-significant; Qwen3 +0.001). So in single models casing alone shifted accuracy with
fragmentation nearly unchanged; the registered 3-of-4 same-sign rule is not met.

**Net ITRANS → lossy sentiment change = L1 + L2** (same items, so the differences add exactly; checked in the script).
`scripts/l_ladder_net.py` → `results/l_ladder_posthoc/net_itrans_to_lossy.csv`; paired bootstrap 95% CI (10,000, as
the ladder); McNemar p unadjusted, no test registered.

| model | L1 | L2 | net lossy − ITRANS [95% CI] | McNemar p (unadj.) |
|---|---|---|---|---|
| Qwen3-1.7B | −0.045 | +0.080 | +0.035 [−0.040, +0.105] | 0.43 |
| Qwen3.5-2B | −0.115 | +0.140 | +0.025 [−0.035, +0.090] | 0.53 |
| Sarvam-1 | −0.055 | +0.130 | +0.075 [+0.025, +0.125] | 0.0059 |
| Gemma 4 E2B | −0.185 | +0.220 | +0.035 [−0.015, +0.085] | 0.26 |
| Qwen2.5-1.5B (not counted) | −0.025 | +0.030 | +0.005 [−0.020, +0.030] | 1.0 |

Descriptively, on sentiment most of L2's gain offsets the loss from lowercasing; only Sarvam-1's net CI excludes 0.
No verdict.

---
`````

##### 2026-10-22 — L3 on items with no English words in natural; net ITRANS → lossy on retrieval and SIB (post hoc descriptive, 2026-10-22, no verdict)

RESULTS.md lines 1794 to 1838; first line committed in `70fe375` on 2026-10-22 20:33:33 +0530; last line in `a00f2ff` on 2026-10-22 23:16:03 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-22 — L3 on items with no English words in natural; net ITRANS → lossy on retrieval and SIB (post hoc descriptive, 2026-10-22, no verdict)
`scripts/l_ladder_posthoc.py` (CPU; stored ladder scores and cached vectors; retrieval per-item hits recomputed with
the ladder's procedure and asserted to reproduce `results/l_ladder/contrasts.csv` for L1, L2, L3 in every model).
Outputs `results/l_ladder_posthoc/{l3_no_english.csv, net_itrans_to_lossy_all.csv}`. McNemar p unadjusted; no test
is registered here; the registered L3 verdicts are unchanged.

**L3 (natural − lossy), full sample vs items whose natural text has no English word of 4+ characters** (wordfreq en,
Zipf ≥ 3, as the English-share entry). Difference [95% paired bootstrap CI]:

| measure | model | full: n, L3 | no-English subset: n, L3 |
|---|---|---|---|
| retrieval | Qwen3.5-2B | 248, +0.137 [+0.081, +0.194] | 130, +0.077 [+0.000, +0.154] |
| retrieval | Sarvam-1 | 248, +0.036 [+0.004, +0.069] | 130, +0.023 [−0.023, +0.069] |
| retrieval | Gemma 4 E2B | 248, +0.137 [+0.081, +0.198] | 130, +0.085 [+0.000, +0.169] |
| retrieval | Qwen2.5 (not counted) | 248, +0.177 [+0.129, +0.230] | 130, +0.062 [+0.015, +0.108] |
| sentiment | Qwen3-1.7B | 198, −0.005 [−0.076, +0.066] | 80, −0.025 [−0.150, +0.100] |
| sentiment | Qwen3.5-2B | 198, +0.040 [−0.025, +0.106] | 80, −0.013 [−0.100, +0.063] |
| sentiment | Sarvam-1 | 198, +0.000 [−0.040, +0.040] | 80, +0.025 [−0.038, +0.087] |
| sentiment | Gemma 4 E2B | 198, +0.015 [−0.035, +0.066] | 80, −0.037 [−0.112, +0.038] |
| sentiment | Qwen2.5 (not counted) | 198, +0.020 [−0.005, +0.051] | 80, −0.013 [−0.038, +0.000] |
| SIB-257 | Qwen3-1.7B | 257, +0.054 [+0.008, +0.101] | 132, +0.000 [−0.053, +0.053] |
| SIB-257 | Qwen3.5-2B | 257, +0.035 [−0.012, +0.086] | 132, +0.023 [−0.038, +0.083] |
| SIB-257 | Sarvam-1 | 257, +0.058 [+0.016, +0.105] | 132, +0.045 [−0.023, +0.114] |
| SIB-257 | Gemma 4 E2B | 257, +0.058 [+0.000, +0.117] | 132, +0.038 [−0.053, +0.129] |
| SIB-257 | Qwen2.5 (not counted) | 257, +0.074 [+0.019, +0.128] | 132, +0.023 [−0.038, +0.091] |

Descriptively: on items without English words, the retrieval L3 estimates are roughly half the full-sample ones in
every model, with CIs reaching 0 (n = 130); the subset is about half the sample and is not a random half (sentences
without loans or names may differ in other ways), so this neither confirms nor removes the registered L3 retrieval
effect.

**Net ITRANS → lossy (L1 + L2 = lossy − ITRANS)**, difference [95% paired bootstrap CI]:

| model | retrieval (248) | sentiment (200) | SIB-200 (1,004) |
|---|---|---|---|
| Qwen3-1.7B | — | +0.035 [−0.040, +0.105] | +0.067 [+0.041, +0.093] |
| Qwen3.5-2B | +0.185 [+0.121, +0.246] | +0.025 [−0.035, +0.090] | +0.134 [+0.107, +0.162] |
| Sarvam-1 | +0.198 [+0.141, +0.254] | +0.075 [+0.025, +0.125] | +0.166 [+0.134, +0.199] |
| Gemma 4 E2B | +0.129 [+0.065, +0.194] | +0.035 [−0.015, +0.085] | +0.130 [+0.100, +0.162] |
| Qwen2.5 (not counted) | +0.069 [+0.032, +0.109] | +0.005 [−0.020, +0.030] | +0.089 [+0.059, +0.119] |

Descriptively, lossy beats ITRANS on retrieval and SIB in every model; only on sentiment does the L1 loss mostly
cancel the L2 gain. No verdict.

---
`````

##### 2026-10-22 — NC1 and ladder: independent frequency reference, item-level decomposition, ladder piece familiarity (post hoc descriptive, 2026-10-22, no verdict)

RESULTS.md lines 1896 to 1969; first line committed in `40de234` on 2026-10-22 23:55:36 +0530; last line in `7d88f63` on 2026-10-23 00:22:30 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-22 — NC1 and ladder: independent frequency reference, item-level decomposition, ladder piece familiarity (post hoc descriptive, 2026-10-22, no verdict)
Aarnav: NC1 registered verdict kept (NC-F refuted). CPU only, no new GPU run. `scripts/nc1_posthoc.py`; outputs
`results/nc1_posthoc/{reference.json, piece_frequency_independent.csv, decomposition.csv, ladder_piece_familiarity.csv}`.

**Note on the earlier proxy:** the 2026-10-22 piece-frequency proxy (`results/nc1/piece_frequency.csv`) counted pieces
on a reference that contained the evaluation texts themselves (all lossy FLORES, sentiment, XNLI, SIB), so (a) was
in-distribution by construction: **partly circular**. It is superseded by the reference below.

**1. Independent reference.** Romanized Kannada: Dakshina `kn` romanized Wikipedia sentences (HF mirror, see
DATA_CARD.md), 10,000 sentences, 1.11M chars, 111,105 words, as written (1.7% uppercase chars); 0 dropped for overlap
with any evaluation native text (exact or containment, ≥ 20 chars). English: 255 whole articles from English
Wikipedia 20231101 shard 0 (seed-0 shuffle), 1.11M chars, matched to the Dakshina size; 0 skipped for containing an
evaluation English text. Canonical tokens: 637k (Gemma) to 829k (Sarvam-1). Dakshina is manual natural
romanization, not the lossy scheme; no scheme-converted text is in the reference.

Mean ln(count + 1), (a) / (b) / (c) [share unseen]:

| model | M4c 496 | sentiment | XNLI | SIB |
|---|---|---|---|---|
| Qwen3 (= Qwen2.5 tokenizer) | 6.73 / 6.14 / 5.55 [.007/.014/.023] | 6.69 / 6.11 / 5.45 | 6.60 / 6.03 / 5.43 | 6.60 / 6.09 / 5.45 |
| Qwen3.5 | 6.38 / 5.87 / 5.20 [.013/.027/.044] | 6.42 / 5.82 / 5.15 | 6.39 / 5.83 / 5.16 | 6.33 / 5.87 / 5.15 |
| Sarvam-1 | 7.77 / 7.55 / 7.04 [.001/.001/.002] | 7.81 / 7.55 / 7.03 | 7.79 / 7.55 / 7.02 | 7.74 / 7.53 / 7.01 |
| Gemma 4 | 6.11 / 5.64 / 4.94 [.017/.032/.054] | 6.18 / 5.60 / 4.89 | 6.14 / 5.59 / 4.91 | 6.05 / 5.62 / 4.89 |

The ordering (a) > (b) > (c) of the earlier proxy holds on the independent reference in every model × dataset: (c)
uses rarer pieces than (b).

**2. Item-level decomposition** (counted models). Score: sentiment/SIB calibrated gold log-prob margin (primary rule);
retrieval cosine margin (correct English minus best distractor, unmapped, M4c test half, at the layer selected for (a):
Qwen3.5 7, Sarvam-1 17, Gemma 8; the (a) margins reproduce the registered (a) acc@1). (b) and (c) pooled, y = score −
score in (a); OLS on extra pieces (vs canonical; 0 in (c)) and Δ mean piece ln-freq (vs (a), step 1 reference),
item-clustered SEs, 95% CIs. Correlation between the two predictors 0.59–0.73.

| model | measure (items) | per extra piece [95% CI] | per +1 Δ ln-freq [95% CI] |
|---|---|---|---|
| Qwen3.5 | retrieval (248) | −0.0006 [−0.0014, +0.0002] | +0.000 [−0.015, +0.016] |
| Sarvam-1 | retrieval (248) | **−0.0036 [−0.0053, −0.0020]** | **+0.050 [+0.010, +0.091]** |
| Gemma 4 | retrieval (248) | −0.0007 [−0.0015, +0.0000] | **+0.016 [+0.001, +0.031]** |
| Qwen3 | sentiment (200) | **−0.028 [−0.046, −0.010]** | +0.24 [−0.16, +0.63] |
| Qwen3.5 | sentiment (200) | −0.001 [−0.006, +0.003] | −0.01 [−0.12, +0.11] |
| Sarvam-1 | sentiment (200) | −0.000 [−0.020, +0.020] | +0.07 [−0.56, +0.70] |
| Gemma 4 | sentiment (200) | −0.040 [−0.100, +0.020] | +1.09 [−0.63, +2.81] |
| Qwen3 | SIB (1,004) | +0.043 [−0.017, +0.104] | −0.49 [−1.59, +0.61] |
| Qwen3.5 | SIB (1,004) | −0.006 [−0.016, +0.004] | +0.09 [−0.09, +0.27] |
| Sarvam-1 | SIB (1,004) | **−0.015 [−0.025, −0.005]** | −0.01 [−0.31, +0.29] |
| Gemma 4 | SIB (1,004) | **−0.046 [−0.090, −0.003]** | **+1.29 [+0.43, +2.14]** |

Predictor SDs: extra pieces 8.0–11.0, Δ ln-freq 0.34–0.52. Bold = CI excludes 0 (unadjusted, 11 models × measures).
Descriptively: where either coefficient is distinguishable from 0, extra pieces are negative and piece frequency
positive (Sarvam-1 retrieval and Gemma SIB show both with the other held fixed); most CIs include 0.

**3. Ladder piece familiarity** (canonical tokenization; reference of step 1). Tokens per word reproduce
`results/l_ladder/tokens_per_word.csv`.

| model | dataset | tokens/word: ITRANS / lower / lossy / natural | mean ln-freq: ITRANS / lower / lossy / natural |
|---|---|---|---|
| Qwen3 (= Qwen2.5) | M4c 496 | 4.32 / 4.40 / 3.56 / 3.53 | 5.83 / 6.00 / 6.73 / 6.64 |
| Qwen3 (= Qwen2.5) | sentiment | 4.23 / 4.39 / 3.57 / 3.51 | 5.83 / 5.99 / 6.76 / 6.63 |
| Qwen3.5 | M4c 496 | 4.17 / 4.21 / 3.34 / 3.33 | 5.58 / 5.67 / 6.38 / 6.32 |
| Qwen3.5 | sentiment | 4.09 / 4.19 / 3.34 / 3.32 | 5.59 / 5.63 / 6.41 / 6.32 |
| Sarvam-1 | M4c 496 | 5.30 / 5.36 / 4.34 / 4.31 | 7.13 / 7.22 / 7.77 / 7.69 |
| Sarvam-1 | sentiment | 5.24 / 5.31 / 4.36 / 4.29 | 7.16 / 7.21 / 7.81 / 7.66 |
| Gemma 4 | M4c 496 | 4.02 / 4.14 / 3.20 / 3.16 | 5.26 / 5.32 / 6.11 / 6.05 |
| Gemma 4 | sentiment | 3.94 / 4.15 / 3.21 / 3.15 | 5.30 / 5.29 / 6.17 / 6.05 |

Descriptively: L1 (ITRANS → lower) changes neither much; L2 (lower → lossy) lowers tokens per word by ~0.8–1.0 and
raises piece ln-freq by ~0.55–0.8 together, so the ladder cannot separate them; L3 (lossy → natural) changes both
slightly (tokens per word −0.01 to −0.07, ln-freq −0.06 to −0.15), so the L3 retrieval effect tracks neither piece
frequency nor token count. No verdict.

**4. L3 on loan-free items** was done earlier today (entry "L3 on items with no English words in natural",
`results/l_ladder_posthoc/l3_no_english.csv`); no new computation.

---
`````

## Result files, every number

#### `results/l_ladder/accuracy.csv` (17,714 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

| model | task | form | n | chance | acc_cal | acc_cal_ci_low | acc_cal_ci_high | constant_label_rate_cal | acc_raw | acc_raw_ci_low | acc_raw_ci_high | constant_label_rate_raw | acc_na | acc_na_ci_low | acc_na_ci_high | constant_label_rate_na | acc_avg3 | acc_avg3_ci_low | acc_avg3_ci_high | constant_label_rate_avg3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 |
| gemma4-e2b | sentiment | itrans | 200 | 0.5 | 0.755 | 0.695 | 0.81 | 0.685 | 0.75 | 0.69 | 0.81 | 0.67 | 0.765 | 0.705 | 0.82 | 0.615 | 0.755 | 0.695 | 0.81 | 0.685 |
| gemma4-e2b | sentiment | lossy | 200 | 0.5 | 0.79 | 0.73 | 0.845 | 0.65 | 0.79 | 0.73 | 0.845 | 0.65 | 0.785 | 0.725 | 0.84 | 0.625 | 0.79 | 0.73 | 0.845 | 0.65 |
| gemma4-e2b | sentiment | lower | 200 | 0.5 | 0.57 | 0.5 | 0.64 | 0.9 | 0.575 | 0.505 | 0.645 | 0.895 | 0.61 | 0.54 | 0.675 | 0.86 | 0.57 | 0.5 | 0.64 | 0.9 |
| gemma4-e2b | sentiment | natural | 198 | 0.5 | 0.803030303030303 | 0.7474747474747475 | 0.8585858585858586 | 0.6717171717171717 | 0.803030303030303 | 0.7474747474747475 | 0.8585858585858586 | 0.6717171717171717 | 0.8282828282828283 | 0.7727272727272727 | 0.8787878787878788 | 0.6262626262626263 | 0.803030303030303 | 0.7474747474747475 | 0.8585858585858586 | 0.6717171717171717 |
| gemma4-e2b | xnli | english | 200 | 0.3333333333333333 | 0.735 | 0.675 | 0.795 | 0.405 | 0.735 | 0.675 | 0.795 | 0.405 | 0.6 | 0.53 | 0.67 | 0.56 | 0.63 | 0.565 | 0.695 | 0.565 |
| gemma4-e2b | xnli | itrans | 200 | 0.3333333333333333 | 0.41 | 0.34 | 0.48 | 0.87 | 0.41 | 0.34 | 0.48 | 0.87 | 0.435 | 0.365 | 0.505 | 0.6 | 0.445 | 0.375 | 0.51 | 0.68 |
| gemma4-e2b | xnli | lossy | 200 | 0.3333333333333333 | 0.4 | 0.335 | 0.47 | 0.84 | 0.4 | 0.335 | 0.47 | 0.84 | 0.395 | 0.33 | 0.46 | 0.78 | 0.375 | 0.31 | 0.44 | 0.835 |
| gemma4-e2b | xnli | lower | 200 | 0.3333333333333333 | 0.38 | 0.315 | 0.45 | 0.915 | 0.38 | 0.315 | 0.45 | 0.915 | 0.405 | 0.34 | 0.475 | 0.755 | 0.395 | 0.33 | 0.46 | 0.74 |
| gemma4-e2b | xnli | natural | 193 | 0.3333333333333333 | 0.40414507772020725 | 0.33678756476683935 | 0.47668393782383417 | 0.772020725388601 | 0.40414507772020725 | 0.33678756476683935 | 0.47668393782383417 | 0.772020725388601 | 0.39896373056994816 | 0.3316062176165803 | 0.47150259067357514 | 0.7253886010362695 | 0.38860103626943004 | 0.32124352331606215 | 0.45595854922279794 | 0.772020725388601 |
| qwen2.5-1.5b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.52 | 0.45 | 0.59 | 0.98 | 0.88 | 0.835 | 0.925 | 0.62 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 0.5 | 0.495 | 0.425 | 0.565 | 0.995 | 0.495 | 0.425 | 0.565 | 0.995 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 0.5 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 |
| qwen2.5-1.5b | sentiment | lower | 200 | 0.5 | 0.47 | 0.4 | 0.54 | 0.9 | 0.47 | 0.4 | 0.54 | 0.9 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 |
| qwen2.5-1.5b | sentiment | natural | 198 | 0.5 | 0.5151515151515151 | 0.4444444444444444 | 0.5858585858585859 | 0.9696969696969697 | 0.5151515151515151 | 0.4444444444444444 | 0.5858585858585859 | 0.9696969696969697 | 0.494949494949495 | 0.42424242424242425 | 0.5656565656565656 | 1.0 | 0.494949494949495 | 0.42424242424242425 | 0.5656565656565656 | 1.0 |
| qwen2.5-1.5b | xnli | english | 200 | 0.3333333333333333 | 0.825 | 0.77 | 0.875 | 0.38 | 0.795 | 0.735 | 0.85 | 0.45 | 0.785 | 0.73 | 0.84 | 0.49 | 0.825 | 0.77 | 0.875 | 0.38 |
| qwen2.5-1.5b | xnli | itrans | 200 | 0.3333333333333333 | 0.32 | 0.255 | 0.385 | 0.67 | 0.375 | 0.31 | 0.445 | 0.845 | 0.325 | 0.26 | 0.39 | 0.965 | 0.32 | 0.255 | 0.385 | 0.67 |
| qwen2.5-1.5b | xnli | lossy | 200 | 0.3333333333333333 | 0.325 | 0.26 | 0.39 | 0.75 | 0.375 | 0.31 | 0.445 | 0.84 | 0.33 | 0.265 | 0.395 | 0.955 | 0.325 | 0.26 | 0.39 | 0.75 |
| qwen2.5-1.5b | xnli | lower | 200 | 0.3333333333333333 | 0.33 | 0.265 | 0.395 | 0.84 | 0.33 | 0.265 | 0.395 | 0.72 | 0.33 | 0.265 | 0.395 | 0.975 | 0.33 | 0.265 | 0.395 | 0.84 |
| qwen2.5-1.5b | xnli | natural | 193 | 0.3333333333333333 | 0.32124352331606215 | 0.2538860103626943 | 0.38860103626943004 | 0.7409326424870466 | 0.37305699481865284 | 0.30569948186528495 | 0.44041450777202074 | 0.7461139896373057 | 0.33678756476683935 | 0.2694300518134715 | 0.40414507772020725 | 0.9585492227979274 | 0.32124352331606215 | 0.2538860103626943 | 0.38860103626943004 | 0.7409326424870466 |
| qwen3-1.7b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 |
| qwen3-1.7b | sentiment | itrans | 200 | 0.5 | 0.535 | 0.465 | 0.605 | 0.645 | 0.58 | 0.51 | 0.645 | 0.68 | 0.54 | 0.47 | 0.61 | 0.85 | 0.535 | 0.465 | 0.605 | 0.645 |
| qwen3-1.7b | sentiment | lossy | 200 | 0.5 | 0.57 | 0.5 | 0.64 | 0.68 | 0.575 | 0.505 | 0.64 | 0.715 | 0.52 | 0.45 | 0.59 | 0.91 | 0.57 | 0.5 | 0.64 | 0.68 |
| qwen3-1.7b | sentiment | lower | 200 | 0.5 | 0.49 | 0.42 | 0.56 | 0.81 | 0.5 | 0.43 | 0.57 | 0.95 | 0.555 | 0.485 | 0.625 | 0.615 | 0.49 | 0.42 | 0.56 | 0.81 |
| qwen3-1.7b | sentiment | natural | 198 | 0.5 | 0.5606060606060606 | 0.4898989898989899 | 0.6313131313131313 | 0.7424242424242424 | 0.6313131313131313 | 0.5656565656565656 | 0.696969696969697 | 0.5909090909090909 | 0.5202020202020202 | 0.4494949494949495 | 0.5909090909090909 | 0.9040404040404041 | 0.5606060606060606 | 0.4898989898989899 | 0.6313131313131313 | 0.7424242424242424 |
| qwen3-1.7b | xnli | english | 200 | 0.3333333333333333 | 0.575 | 0.505 | 0.645 | 0.71 | 0.615 | 0.545 | 0.68 | 0.53 | 0.54 | 0.47 | 0.61 | 0.765 | 0.575 | 0.505 | 0.645 | 0.71 |
| qwen3-1.7b | xnli | itrans | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.37 | 0.305 | 0.44 | 0.8 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.995 |
| qwen3-1.7b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.415 | 0.345 | 0.485 | 0.795 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.995 |
| qwen3-1.7b | xnli | lower | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.985 | 0.4 | 0.33 | 0.47 | 0.76 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.985 |
| qwen3-1.7b | xnli | natural | 193 | 0.3333333333333333 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9844559585492227 | 0.39896373056994816 | 0.3316062176165803 | 0.46632124352331605 | 0.7979274611398963 | 0.33678756476683935 | 0.2694300518134715 | 0.40414507772020725 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9844559585492227 |
| qwen3.5-2b | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.525 | 0.98 | 0.96 | 0.995 | 0.51 |
| qwen3.5-2b | sentiment | itrans | 200 | 0.5 | 0.655 | 0.59 | 0.72 | 0.775 | 0.675 | 0.61 | 0.74 | 0.665 | 0.615 | 0.545 | 0.685 | 0.855 | 0.655 | 0.59 | 0.72 | 0.775 |
| qwen3.5-2b | sentiment | lossy | 200 | 0.5 | 0.68 | 0.615 | 0.74 | 0.72 | 0.675 | 0.61 | 0.735 | 0.645 | 0.645 | 0.58 | 0.71 | 0.815 | 0.68 | 0.615 | 0.74 | 0.72 |
| qwen3.5-2b | sentiment | lower | 200 | 0.5 | 0.54 | 0.47 | 0.61 | 0.85 | 0.545 | 0.475 | 0.615 | 0.765 | 0.52 | 0.45 | 0.59 | 0.91 | 0.54 | 0.47 | 0.61 | 0.85 |
| qwen3.5-2b | sentiment | natural | 198 | 0.5 | 0.7222222222222222 | 0.6616161616161617 | 0.7828282828282829 | 0.6818181818181818 | 0.7373737373737373 | 0.6767676767676768 | 0.797979797979798 | 0.5757575757575758 | 0.6818181818181818 | 0.6161616161616161 | 0.7424242424242424 | 0.7525252525252525 | 0.7222222222222222 | 0.6616161616161617 | 0.7828282828282829 | 0.6818181818181818 |
| qwen3.5-2b | xnli | english | 200 | 0.3333333333333333 | 0.49 | 0.42 | 0.56 | 0.805 | 0.43 | 0.36 | 0.5 | 0.89 | 0.45 | 0.38 | 0.52 | 0.845 | 0.49 | 0.42 | 0.56 | 0.805 |
| qwen3.5-2b | xnli | itrans | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 |
| qwen3.5-2b | xnli | lossy | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.99 | 0.34 | 0.275 | 0.405 | 0.995 | 0.335 | 0.27 | 0.4 | 0.99 | 0.335 | 0.27 | 0.4 | 0.99 |
| qwen3.5-2b | xnli | lower | 200 | 0.3333333333333333 | 0.345 | 0.28 | 0.41 | 0.99 | 0.34 | 0.275 | 0.405 | 0.995 | 0.345 | 0.28 | 0.41 | 0.99 | 0.345 | 0.28 | 0.41 | 0.99 |
| qwen3.5-2b | xnli | natural | 193 | 0.3333333333333333 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9948186528497409 |
| sarvam-1 | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.515 | 0.98 | 0.96 | 0.995 | 0.51 |
| sarvam-1 | sentiment | itrans | 200 | 0.5 | 0.82 | 0.765 | 0.87 | 0.61 | 0.845 | 0.795 | 0.895 | 0.515 | 0.78 | 0.72 | 0.835 | 0.69 | 0.82 | 0.765 | 0.87 | 0.61 |
| sarvam-1 | sentiment | lossy | 200 | 0.5 | 0.895 | 0.85 | 0.935 | 0.575 | 0.91 | 0.87 | 0.95 | 0.51 | 0.86 | 0.81 | 0.905 | 0.63 | 0.895 | 0.85 | 0.935 | 0.575 |
| sarvam-1 | sentiment | lower | 200 | 0.5 | 0.765 | 0.705 | 0.825 | 0.535 | 0.765 | 0.705 | 0.82 | 0.645 | 0.735 | 0.67 | 0.795 | 0.655 | 0.765 | 0.705 | 0.825 | 0.535 |
| sarvam-1 | sentiment | natural | 198 | 0.5 | 0.8939393939393939 | 0.8484848484848485 | 0.9343434343434344 | 0.5808080808080808 | 0.9040404040404041 | 0.8635101010101012 | 0.9444444444444444 | 0.5303030303030303 | 0.8484848484848485 | 0.797979797979798 | 0.898989898989899 | 0.6464646464646465 | 0.8939393939393939 | 0.8484848484848485 | 0.9343434343434344 | 0.5808080808080808 |
| sarvam-1 | xnli | english | 200 | 0.3333333333333333 | 0.55 | 0.48 | 0.62 | 0.545 | 0.53 | 0.46 | 0.6 | 0.63 | 0.475 | 0.405 | 0.545 | 0.655 | 0.55 | 0.48 | 0.62 | 0.545 |
| sarvam-1 | xnli | itrans | 200 | 0.3333333333333333 | 0.385 | 0.32 | 0.455 | 0.795 | 0.385 | 0.32 | 0.455 | 0.8 | 0.37 | 0.3 | 0.44 | 0.865 | 0.385 | 0.32 | 0.455 | 0.795 |
| sarvam-1 | xnli | lossy | 200 | 0.3333333333333333 | 0.47 | 0.4 | 0.54 | 0.58 | 0.46 | 0.39 | 0.53 | 0.595 | 0.375 | 0.31 | 0.44 | 0.905 | 0.47 | 0.4 | 0.54 | 0.58 |
| sarvam-1 | xnli | lower | 200 | 0.3333333333333333 | 0.365 | 0.3 | 0.435 | 0.815 | 0.365 | 0.3 | 0.435 | 0.82 | 0.395 | 0.325 | 0.465 | 0.85 | 0.365 | 0.3 | 0.435 | 0.815 |
| sarvam-1 | xnli | natural | 193 | 0.3333333333333333 | 0.46632124352331605 | 0.39378238341968913 | 0.533678756476684 | 0.5958549222797928 | 0.46632124352331605 | 0.39378238341968913 | 0.533678756476684 | 0.6113989637305699 | 0.34196891191709844 | 0.27461139896373055 | 0.40932642487046633 | 0.9222797927461139 | 0.46632124352331605 | 0.39378238341968913 | 0.533678756476684 | 0.5958549222797928 |
| gemma4-e2b | sib | english | 1004 | 0.14285714285714285 | 0.7938247011952191 | 0.7689243027888446 | 0.8187250996015937 | 0.20916334661354583 | 0.8007968127490039 | 0.7758964143426295 | 0.8256972111553785 | 0.21314741035856574 | 0.8007968127490039 | 0.7758964143426295 | 0.8256972111553785 | 0.2151394422310757 | 0.7938247011952191 | 0.7689243027888446 | 0.8187250996015937 | 0.20916334661354583 |
| gemma4-e2b | sib | itrans | 1004 | 0.14285714285714285 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.2549800796812749 | 0.3904382470119522 | 0.3605577689243028 | 0.4213147410358566 | 0.28286852589641437 | 0.38247011952191234 | 0.35258964143426297 | 0.4123505976095618 | 0.2968127490039841 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.2549800796812749 |
| gemma4-e2b | sib | lossy | 1004 | 0.14285714285714285 | 0.49701195219123506 | 0.46613545816733065 | 0.5278884462151394 | 0.22709163346613545 | 0.5139442231075697 | 0.48306772908366535 | 0.545816733067729 | 0.2290836653386454 | 0.499003984063745 | 0.4681274900398406 | 0.5308764940239044 | 0.23207171314741035 | 0.49701195219123506 | 0.46613545816733065 | 0.5278884462151394 | 0.22709163346613545 |
| gemma4-e2b | sib | lower | 1004 | 0.14285714285714285 | 0.41434262948207173 | 0.3834661354581673 | 0.4442231075697211 | 0.250996015936255 | 0.42330677290836655 | 0.39243027888446214 | 0.4541832669322709 | 0.2689243027888446 | 0.4163346613545817 | 0.3854581673306773 | 0.44621513944223107 | 0.2778884462151394 | 0.41434262948207173 | 0.3834661354581673 | 0.4442231075697211 | 0.250996015936255 |
| gemma4-e2b | sib | natural257 | 257 | 0.14285714285714285 | 0.5447470817120622 | 0.48638132295719844 | 0.6070038910505836 | 0.23346303501945526 | 0.5719844357976653 | 0.5136186770428015 | 0.6342412451361867 | 0.22568093385214008 | 0.5603112840466926 | 0.5019455252918288 | 0.622568093385214 | 0.22178988326848248 | 0.5447470817120622 | 0.48638132295719844 | 0.6070038910505836 | 0.23346303501945526 |
| qwen2.5-1.5b | sib | english | 1004 | 0.14285714285714285 | 0.796812749003984 | 0.7719123505976095 | 0.8217131474103586 | 0.18725099601593626 | 0.7141434262948207 | 0.6862549800796812 | 0.7420318725099602 | 0.29382470119521914 | 0.8077689243027888 | 0.7828685258964143 | 0.8316733067729084 | 0.20219123505976094 | 0.796812749003984 | 0.7719123505976095 | 0.8217131474103586 | 0.18725099601593626 |
| qwen2.5-1.5b | sib | itrans | 1004 | 0.14285714285714285 | 0.2778884462151394 | 0.25 | 0.3057768924302789 | 0.4312749003984064 | 0.18725099601593626 | 0.16334661354581673 | 0.21215139442231076 | 0.8306772908366534 | 0.3157370517928287 | 0.2868525896414343 | 0.3456175298804781 | 0.3097609561752988 | 0.2778884462151394 | 0.25 | 0.3057768924302789 | 0.4312749003984064 |
| qwen2.5-1.5b | sib | lossy | 1004 | 0.14285714285714285 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.351593625498008 | 0.2798804780876494 | 0.25298804780876494 | 0.30876494023904383 | 0.6892430278884463 | 0.40039840637450197 | 0.3705179282868526 | 0.4312749003984064 | 0.24402390438247012 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.351593625498008 |
| qwen2.5-1.5b | sib | lower | 1004 | 0.14285714285714285 | 0.2749003984063745 | 0.24701195219123506 | 0.30278884462151395 | 0.48306772908366535 | 0.17430278884462153 | 0.15139442231075698 | 0.19820717131474103 | 0.8466135458167331 | 0.3107569721115538 | 0.2818725099601594 | 0.3396414342629482 | 0.30677290836653387 | 0.2749003984063745 | 0.24701195219123506 | 0.30278884462151395 | 0.48306772908366535 |
| qwen2.5-1.5b | sib | natural257 | 257 | 0.14285714285714285 | 0.4591439688715953 | 0.3968871595330739 | 0.5175097276264592 | 0.3151750972762646 | 0.32684824902723736 | 0.26848249027237353 | 0.3852140077821012 | 0.6459143968871596 | 0.4708171206225681 | 0.4085603112840467 | 0.5291828793774319 | 0.22568093385214008 | 0.4591439688715953 | 0.3968871595330739 | 0.5175097276264592 | 0.3151750972762646 |
| qwen3-1.7b | sib | english | 1004 | 0.14285714285714285 | 0.7818725099601593 | 0.7559760956175299 | 0.8067729083665338 | 0.20916334661354583 | 0.7848605577689243 | 0.7589641434262948 | 0.8097609561752988 | 0.19621513944223107 | 0.7808764940239044 | 0.7549800796812749 | 0.8057768924302788 | 0.2061752988047809 | 0.7818725099601593 | 0.7559760956175299 | 0.8067729083665338 | 0.20916334661354583 |
| qwen3-1.7b | sib | itrans | 1004 | 0.14285714285714285 | 0.2400398406374502 | 0.21314741035856574 | 0.2659611553784857 | 0.5189243027888446 | 0.2559760956175299 | 0.2290836653386454 | 0.28286852589641437 | 0.5 | 0.23705179282868527 | 0.21115537848605578 | 0.26294820717131473 | 0.48705179282868527 | 0.2400398406374502 | 0.21314741035856574 | 0.2659611553784857 | 0.5189243027888446 |
| qwen3-1.7b | sib | lossy | 1004 | 0.14285714285714285 | 0.30677290836653387 | 0.2788844621513944 | 0.33565737051792827 | 0.34063745019920316 | 0.30876494023904383 | 0.2798804780876494 | 0.3386454183266932 | 0.35358565737051795 | 0.299800796812749 | 0.27091633466135456 | 0.3286852589641434 | 0.3595617529880478 | 0.30677290836653387 | 0.2788844621513944 | 0.33565737051792827 | 0.34063745019920316 |
| qwen3-1.7b | sib | lower | 1004 | 0.14285714285714285 | 0.2410358565737052 | 0.2151394422310757 | 0.2679282868525896 | 0.38645418326693226 | 0.2559760956175299 | 0.2290836653386454 | 0.28386454183266935 | 0.36852589641434264 | 0.2360557768924303 | 0.2101593625498008 | 0.26294820717131473 | 0.3605577689243028 | 0.2410358565737052 | 0.2151394422310757 | 0.2679282868525896 | 0.38645418326693226 |
| qwen3-1.7b | sib | natural257 | 257 | 0.14285714285714285 | 0.36964980544747084 | 0.311284046692607 | 0.4280155642023346 | 0.3657587548638132 | 0.39299610894941633 | 0.3346303501945525 | 0.45136186770428016 | 0.31906614785992216 | 0.3657587548638132 | 0.30739299610894943 | 0.42412451361867703 | 0.3968871595330739 | 0.36964980544747084 | 0.311284046692607 | 0.4280155642023346 | 0.3657587548638132 |
| qwen3.5-2b | sib | english | 1004 | 0.14285714285714285 | 0.8037848605577689 | 0.7788844621513944 | 0.8286852589641435 | 0.2400398406374502 | 0.7280876494023905 | 0.700199203187251 | 0.7549800796812749 | 0.2410358565737052 | 0.8057768924302788 | 0.7808764940239044 | 0.8296812749003984 | 0.2589641434262948 | 0.8037848605577689 | 0.7788844621513944 | 0.8286852589641435 | 0.2400398406374502 |
| qwen3.5-2b | sib | itrans | 1004 | 0.14285714285714285 | 0.2410358565737052 | 0.2151394422310757 | 0.2679282868525896 | 0.5318725099601593 | 0.14840637450199204 | 0.12749003984063745 | 0.17031872509960158 | 0.8814741035856574 | 0.2798804780876494 | 0.25199203187250996 | 0.30876494023904383 | 0.299800796812749 | 0.2410358565737052 | 0.2151394422310757 | 0.2679282868525896 | 0.5318725099601593 |
| qwen3.5-2b | sib | lossy | 1004 | 0.14285714285714285 | 0.3754980079681275 | 0.3466135458167331 | 0.4063745019920319 | 0.3804780876494024 | 0.26593625498007967 | 0.23904382470119523 | 0.29382470119521914 | 0.7460159362549801 | 0.4123505976095618 | 0.38247011952191234 | 0.44322709163346613 | 0.2689243027888446 | 0.3754980079681275 | 0.3466135458167331 | 0.4063745019920319 | 0.3804780876494024 |
| qwen3.5-2b | sib | lower | 1004 | 0.14285714285714285 | 0.2958167330677291 | 0.2679282868525896 | 0.3237051792828685 | 0.46215139442231074 | 0.17928286852589642 | 0.1553784860557769 | 0.20418326693227093 | 0.8396414342629482 | 0.34163346613545814 | 0.31274900398406374 | 0.3715139442231076 | 0.2918326693227092 | 0.2958167330677291 | 0.2679282868525896 | 0.3237051792828685 | 0.46215139442231074 |
| qwen3.5-2b | sib | natural257 | 257 | 0.14285714285714285 | 0.45525291828793774 | 0.3968871595330739 | 0.5175097276264592 | 0.3657587548638132 | 0.3463035019455253 | 0.28793774319066145 | 0.4046692607003891 | 0.642023346303502 | 0.4980544747081712 | 0.4357976653696498 | 0.5603112840466926 | 0.2723735408560311 | 0.45525291828793774 | 0.3968871595330739 | 0.5175097276264592 | 0.3657587548638132 |
| sarvam-1 | sib | english | 1004 | 0.14285714285714285 | 0.7679282868525896 | 0.7420318725099602 | 0.7938247011952191 | 0.26294820717131473 | 0.5737051792828686 | 0.5428286852589641 | 0.6045816733067729 | 0.398406374501992 | 0.7539840637450199 | 0.7270916334661355 | 0.7808764940239044 | 0.33167330677290835 | 0.7679282868525896 | 0.7420318725099602 | 0.7938247011952191 | 0.26294820717131473 |
| sarvam-1 | sib | itrans | 1004 | 0.14285714285714285 | 0.5388446215139442 | 0.5079681274900398 | 0.5707171314741036 | 0.4452191235059761 | 0.3247011952191235 | 0.2958167330677291 | 0.3545816733067729 | 0.5428286852589641 | 0.4940239043824701 | 0.4631474103585657 | 0.5249003984063745 | 0.6384462151394422 | 0.5388446215139442 | 0.5079681274900398 | 0.5707171314741036 | 0.4452191235059761 |
| sarvam-1 | sib | lossy | 1004 | 0.14285714285714285 | 0.7051792828685259 | 0.6772908366533864 | 0.7330677290836654 | 0.2340637450199203 | 0.46115537848605576 | 0.4312749003984064 | 0.49203187250996017 | 0.41932270916334663 | 0.7101593625498008 | 0.6822709163346613 | 0.7380478087649402 | 0.33067729083665337 | 0.7051792828685259 | 0.6772908366533864 | 0.7330677290836654 | 0.2340637450199203 |
| sarvam-1 | sib | lower | 1004 | 0.14285714285714285 | 0.4960159362549801 | 0.4641434262948207 | 0.5268924302788844 | 0.35258964143426297 | 0.250996015936255 | 0.2241035856573705 | 0.2788844621513944 | 0.646414342629482 | 0.500996015936255 | 0.4701195219123506 | 0.5328685258964143 | 0.5896414342629482 | 0.4960159362549801 | 0.4641434262948207 | 0.5268924302788844 | 0.35258964143426297 |
| sarvam-1 | sib | natural257 | 257 | 0.14285714285714285 | 0.7276264591439688 | 0.6731517509727627 | 0.7821011673151751 | 0.2140077821011673 | 0.5097276264591439 | 0.4474708171206226 | 0.5719844357976653 | 0.4046692607003891 | 0.7470817120622568 | 0.6926070038910506 | 0.7976653696498055 | 0.2840466926070039 | 0.7276264591439688 | 0.6731517509727627 | 0.7821011673151751 | 0.2140077821011673 |

#### `results/l_ladder/contrasts.csv` (10,986 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

| measure | model | contrast | a | b | n | acc_a | acc_b | diff | ci | a_only | b_only | p | counted | p_holm | significant | ci_excludes_0 | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | L1 | lower | itrans | 248 | 0.13306451612903225 | 0.13306451612903225 | 0.0 | [-0.03629032149910927, 0.03629032149910927] | 11 | 11 | 1.0 | False |  | False | False | False |
| retrieval | qwen2.5-1.5b | L2 | lossy | lower | 248 | 0.20161290322580644 | 0.13306451612903225 | 0.06854838709677419 | [0.02822580561041832, 0.1088709682226181] | 23 | 6 | 0.002315700054168701 | False |  | False | True | False |
| retrieval | qwen2.5-1.5b | L3 | natural | lossy | 248 | 0.3790322580645161 | 0.20161290322580644 | 0.1774193548387097 | [0.12903225421905518, 0.22983871400356293] | 46 | 2 | 8.363087999896379e-12 | False |  | False | True | False |
| retrieval | qwen3.5-2b | L1 | lower | itrans | 248 | 0.2661290322580645 | 0.18951612903225806 | 0.07661290322580644 | [0.02016128972172737, 0.13709677755832672] | 37 | 18 | 0.014453833533827728 | True | 0.05781533413531091 | False | True | True |
| retrieval | qwen3.5-2b | L2 | lossy | lower | 248 | 0.375 | 0.2661290322580645 | 0.1088709677419355 | [0.04435483738780022, 0.1733870953321457] | 47 | 20 | 0.0013071686857635996 | True | 0.006535843428817998 | True | True | False |
| retrieval | qwen3.5-2b | L3 | natural | lossy | 248 | 0.5120967741935484 | 0.375 | 0.13709677419354838 | [0.08064515888690948, 0.19354838132858276] | 44 | 10 | 3.3856859533720747e-06 | True | 2.7085487626976598e-05 | True | True | False |
| retrieval | sarvam-1 | L1 | lower | itrans | 248 | 0.6169354838709677 | 0.6854838709677419 | -0.06854838709677413 | [-0.125, -0.012096773833036423] | 18 | 35 | 0.027008317653722358 | True | 0.08102495296116707 | False | True | True |
| retrieval | sarvam-1 | L2 | lossy | lower | 248 | 0.8830645161290323 | 0.6169354838709677 | 0.2661290322580645 | [0.20564515888690948, 0.3266128897666931] | 71 | 5 | 5.249233110119942e-16 | True | 4.724309799107948e-15 | True | True | False |
| retrieval | sarvam-1 | L3 | natural | lossy | 248 | 0.9193548387096774 | 0.8830645161290323 | 0.03629032258064513 | [0.004032257944345474, 0.06854838877916336] | 13 | 4 | 0.049041748046875 | True | 0.09808349609375 | False | True | True |
| retrieval | gemma4-e2b | L1 | lower | itrans | 248 | 0.4032258064516129 | 0.4435483870967742 | -0.04032258064516131 | [-0.1088709682226181, 0.024193547666072845] | 32 | 42 | 0.29541328065567 | True | 0.29541328065567 | False | False | False |
| retrieval | gemma4-e2b | L2 | lossy | lower | 248 | 0.5725806451612904 | 0.4032258064516129 | 0.1693548387096775 | [0.10080645233392715, 0.23790322244167328] | 63 | 21 | 4.968015141912969e-06 | True | 3.477610599339078e-05 | True | True | False |
| retrieval | gemma4-e2b | L3 | natural | lossy | 248 | 0.7096774193548387 | 0.5725806451612904 | 0.13709677419354838 | [0.08064515888690948, 0.19758065044879913] | 48 | 14 | 1.7428522601631996e-05 | True | 0.00010457113560979198 | True | True | False |
| sentiment | qwen2.5-1.5b | L1 | lower | itrans | 200 | 0.47 | 0.495 | -0.025000000000000022 | [-0.0651249960064888, 0.014999999664723873] | 7 | 12 | 0.359283447265625 | False |  | False | False | False |
| sentiment | qwen2.5-1.5b | L2 | lossy | lower | 200 | 0.5 | 0.47 | 0.030000000000000027 | [-0.009999999776482582, 0.07000000029802322] | 12 | 6 | 0.237884521484375 | False |  | False | False | False |
| sentiment | qwen2.5-1.5b | L3 | natural | lossy | 198 | 0.5151515151515151 | 0.494949494949495 | 0.020202020202020166 | [-0.005050505045801401, 0.05050504952669144] | 6 | 2 | 0.2890625 | False |  | False | False | False |
| sentiment | qwen3.5-2b | L1 | lower | itrans | 200 | 0.54 | 0.655 | -0.11499999999999999 | [-0.18000000715255737, -0.054999999701976776] | 10 | 33 | 0.0006061066312668117 | True | 0.004848853050134494 | True | True | False |
| sentiment | qwen3.5-2b | L2 | lossy | lower | 200 | 0.68 | 0.54 | 0.14 | [0.07500000298023224, 0.20499999821186066] | 39 | 11 | 9.021490107130603e-05 | True | 0.0009021490107130603 | True | True | False |
| sentiment | qwen3.5-2b | L3 | natural | lossy | 198 | 0.7222222222222222 | 0.6818181818181818 | 0.04040404040404044 | [-0.02525252476334572, 0.10606060922145844] | 25 | 17 | 0.27995623852893914 | True | 1.0 | False | False | False |
| sentiment | sarvam-1 | L1 | lower | itrans | 200 | 0.765 | 0.82 | -0.05499999999999994 | [-0.11500000208616257, 0.009999999776482582] | 15 | 26 | 0.11727520595741225 | True | 0.8209264417018858 | False | False | False |
| sentiment | sarvam-1 | L2 | lossy | lower | 200 | 0.895 | 0.765 | 0.13 | [0.06499999761581421, 0.19499999284744263] | 37 | 11 | 0.0002222449626216872 | True | 0.0020002046635951847 | True | True | False |
| sentiment | sarvam-1 | L3 | natural | lossy | 198 | 0.8939393939393939 | 0.8939393939393939 | 0.0 | [-0.04040404036641121, 0.04040404036641121] | 8 | 8 | 1.0 | True | 1.0 | False | False | False |
| sentiment | gemma4-e2b | L1 | lower | itrans | 200 | 0.57 | 0.755 | -0.18500000000000005 | [-0.25, -0.11999999731779099] | 6 | 43 | 5.7277652842913085e-08 | True | 6.300541812720439e-07 | True | True | False |
| sentiment | gemma4-e2b | L2 | lossy | lower | 200 | 0.79 | 0.57 | 0.22000000000000008 | [0.1550000011920929, 0.2849999964237213] | 50 | 6 | 1.0182093779231849e-09 | True | 1.2218512535078219e-08 | True | True | False |
| sentiment | gemma4-e2b | L3 | natural | lossy | 198 | 0.803030303030303 | 0.7878787878787878 | 0.015151515151515138 | [-0.035353533923625946, 0.06565656512975693] | 14 | 11 | 0.6900379657745361 | True | 1.0 | False | False | False |
| sentiment | qwen3-1.7b | L1 | lower | itrans | 200 | 0.49 | 0.535 | -0.04500000000000004 | [-0.14499999582767487, 0.05000000074505806] | 44 | 53 | 0.41677484108909885 | True | 1.0 | False | False | False |
| sentiment | qwen3-1.7b | L2 | lossy | lower | 200 | 0.57 | 0.49 | 0.07999999999999996 | [-0.019999999552965164, 0.18000000715255737] | 61 | 45 | 0.14478233933005036 | True | 0.8686940359803021 | False | False | False |
| sentiment | qwen3-1.7b | L3 | natural | lossy | 198 | 0.5606060606060606 | 0.5656565656565656 | -0.005050505050505083 | [-0.07575757801532745, 0.06565656512975693] | 26 | 27 | 1.0 | True | 1.0 | False | False | False |
| sib | qwen2.5-1.5b | L1 | lower | itrans | 1004 | 0.2749003984063745 | 0.2778884462151394 | -0.0029880478087649376 | [-0.03187251091003418, 0.02589641511440277] | 110 | 113 | 0.8934971214685691 | False |  | False | False | False |
| sib | qwen2.5-1.5b | L2 | lossy | lower | 1004 | 0.3665338645418327 | 0.2749003984063745 | 0.0916334661354582 | [0.060756973922252655, 0.12450199574232101] | 181 | 89 | 2.2575435560775137e-08 | False |  | False | True | False |
| sib | qwen3.5-2b | L1 | lower | itrans | 1004 | 0.2958167330677291 | 0.2410358565737052 | 0.05478087649402391 | [0.02589641511440277, 0.08366534113883972] | 135 | 80 | 0.00021464778366412355 | True | 0.0008585911346564942 | True | True | False |
| sib | qwen3.5-2b | L2 | lossy | lower | 1004 | 0.3754980079681275 | 0.2958167330677291 | 0.07968127490039839 | [0.04780876636505127, 0.11155378818511963] | 172 | 92 | 9.679764898638525e-07 | True | 5.807858939183115e-06 | True | True | False |
| sib | sarvam-1 | L1 | lower | itrans | 1004 | 0.4960159362549801 | 0.5388446215139442 | -0.042828685258964105 | [-0.07370518147945404, -0.011952191591262817] | 107 | 150 | 0.008667040755707438 | True | 0.017334081511414877 | True | True | False |
| sib | sarvam-1 | L2 | lossy | lower | 1004 | 0.7051792828685259 | 0.4960159362549801 | 0.20916334661354585 | [0.17629481852054596, 0.24302789568901062] | 270 | 60 | 5.9732270627569956e-33 | True | 4.7785816502055964e-32 | True | True | False |
| sib | gemma4-e2b | L1 | lower | itrans | 1004 | 0.41434262948207173 | 0.3665338645418327 | 0.04780876494023906 | [0.016932271420955658, 0.07968127727508545] | 151 | 103 | 0.0031107066373511688 | True | 0.009332119912053505 | True | True | False |
| sib | gemma4-e2b | L2 | lossy | lower | 1004 | 0.49701195219123506 | 0.41434262948207173 | 0.08266932270916333 | [0.05179283022880554, 0.11354582011699677] | 171 | 88 | 2.780977551599325e-07 | True | 1.9466842861195277e-06 | True | True | False |
| sib | qwen3-1.7b | L1 | lower | itrans | 1004 | 0.2410358565737052 | 0.2400398406374502 | 0.0009960159362549792 | [-0.02589641511440277, 0.02689243108034134] | 87 | 86 | 0.9999999999999996 | True | 0.9999999999999996 | False | False | False |
| sib | qwen3-1.7b | L2 | lossy | lower | 1004 | 0.30677290836653387 | 0.2410358565737052 | 0.06573705179282868 | [0.03784860670566559, 0.09462151676416397] | 139 | 73 | 6.8395812435670525e-06 | True | 3.419790621783526e-05 | True | True | False |
| sib_L3_secondary | qwen2.5-1.5b | L3 | natural257 | lossy | 257 | 0.4591439688715953 | 0.3852140077821012 | 0.07392996108949412 | [0.019455252215266228, 0.1284046620130539] | 36 | 17 | 0.012660335802414213 | False |  | False | True | False |
| sib_L3_secondary | qwen3.5-2b | L3 | natural257 | lossy | 257 | 0.45525291828793774 | 0.42023346303501946 | 0.035019455252918275 | [-0.011673151515424252, 0.08560311049222946] | 25 | 16 | 0.21102359760880063 | True | 0.21102359760880063 | False | False | False |
| sib_L3_secondary | sarvam-1 | L3 | natural257 | lossy | 257 | 0.7276264591439688 | 0.669260700389105 | 0.05836575875486383 | [0.015564202331006527, 0.10505836457014084] | 25 | 10 | 0.016673847800120715 | True | 0.06669539120048286 | False | True | True |
| sib_L3_secondary | gemma4-e2b | L3 | natural257 | lossy | 257 | 0.5447470817120622 | 0.48638132295719844 | 0.05836575875486377 | [0.0, 0.11673151701688766] | 36 | 21 | 0.06273668035582848 | True | 0.12547336071165696 | False | False | False |
| sib_L3_secondary | qwen3-1.7b | L3 | natural257 | lossy | 257 | 0.36964980544747084 | 0.3151750972762646 | 0.054474708171206254 | [0.0077821011655032635, 0.10116731375455856] | 26 | 12 | 0.03355243967962451 | True | 0.10065731903887354 | False | True | True |
| xnli_reported_only | qwen2.5-1.5b | L1 | lower | itrans | 200 | 0.33 | 0.32 | 0.010000000000000009 | [-0.05000000074505806, 0.06499999761581421] | 18 | 16 | 0.8641662404406816 | False |  | False | False | False |
| xnli_reported_only | qwen2.5-1.5b | L2 | lossy | lower | 200 | 0.325 | 0.33 | -0.0050000000000000044 | [-0.054999999701976776, 0.04500000178813934] | 13 | 14 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen2.5-1.5b | L3 | natural | lossy | 193 | 0.32124352331606215 | 0.32642487046632124 | -0.005181347150259086 | [-0.062176164239645004, 0.05181347206234932] | 15 | 16 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen3.5-2b | L1 | lower | itrans | 200 | 0.345 | 0.34 | 0.004999999999999949 | [0.0, 0.014999999664723873] | 1 | 0 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen3.5-2b | L2 | lossy | lower | 200 | 0.335 | 0.345 | -0.009999999999999953 | [-0.02500000037252903, 0.0] | 0 | 2 | 0.5 | False |  | False | False | False |
| xnli_reported_only | qwen3.5-2b | L3 | natural | lossy | 193 | 0.34196891191709844 | 0.33678756476683935 | 0.005181347150259086 | [0.0, 0.015544041059911251] | 1 | 0 | 1.0 | False |  | False | False | False |
| xnli_reported_only | sarvam-1 | L1 | lower | itrans | 200 | 0.365 | 0.385 | -0.020000000000000018 | [-0.06499999761581421, 0.029999999329447746] | 10 | 14 | 0.5412561893463135 | False |  | False | False | False |
| xnli_reported_only | sarvam-1 | L2 | lossy | lower | 200 | 0.47 | 0.365 | 0.10499999999999998 | [0.04500000178813934, 0.16500000655651093] | 30 | 9 | 0.0010650196345523 | False |  | False | True | False |
| xnli_reported_only | sarvam-1 | L3 | natural | lossy | 193 | 0.46632124352331605 | 0.48186528497409326 | -0.015544041450777202 | [-0.062176164239645004, 0.031088082119822502] | 9 | 12 | 0.6636238098144531 | False |  | False | False | False |
| xnli_reported_only | gemma4-e2b | L1 | lower | itrans | 200 | 0.38 | 0.41 | -0.02999999999999997 | [-0.06499999761581421, 0.004999999888241291] | 4 | 10 | 0.1795654296875 | False |  | False | False | False |
| xnli_reported_only | gemma4-e2b | L2 | lossy | lower | 200 | 0.4 | 0.38 | 0.020000000000000018 | [-0.02500000037252903, 0.06499999761581421] | 12 | 8 | 0.5034446716308594 | False |  | False | False | False |
| xnli_reported_only | gemma4-e2b | L3 | natural | lossy | 193 | 0.40414507772020725 | 0.40414507772020725 | 0.0 | [-0.05181347206234932, 0.05181347206234932] | 12 | 12 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen3-1.7b | L1 | lower | itrans | 200 | 0.335 | 0.335 | 0.0 | [0.0, 0.0] | 0 | 0 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen3-1.7b | L2 | lossy | lower | 200 | 0.335 | 0.335 | 0.0 | [0.0, 0.0] | 0 | 0 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen3-1.7b | L3 | natural | lossy | 193 | 0.34196891191709844 | 0.33678756476683935 | 0.005181347150259086 | [0.0, 0.015544041059911251] | 1 | 0 | 1.0 | False |  | False | False | False |

#### `results/l_ladder/pilot_timing.json` (683 bytes; first commit 569e619 2026-10-22 01:52:07 +0530)

`````text
provenance.config.n = 30
provenance.config.accuracies = "not computed"
provenance.git_commit = "50c6a5fcf7ca041a4017c419d54e5c7e309f3454"
provenance.timestamp_utc = "2026-10-21T20:21:51+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/l_ladder.py", "pilot"]
qwen2.5-1.5b.load_s = 11.865798473358154
qwen2.5-1.5b.forward_30_sentences_s = 2.182551860809326
qwen2.5-1.5b.sib_30_items_incl_load_s = 16.520879983901978
gemma4-e2b.load_s = 10.887035369873047
gemma4-e2b.forward_30_sentences_s = 4.200024843215942
gemma4-e2b.sib_30_items_incl_load_s = 37.20833611488342
`````

#### `results/l_ladder/retrieval.csv` (4,544 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

| model | form | n_test | unmapped_test | unmapped_test_ci | unmapped_layer | mapped_test | mapped_layer | surface_L0 | surface_Lb | surface_Lb_layer | surface_gain | surface_gain_ci | surface_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen2.5-1.5b | native | 248 | 0.23790322580645162 | [0.1854838728904724, 0.2943548262119293] | 15 | 0.2903225806451613 | 27 | 0.09274193548387097 | 0.2903225806451613 | 27 | 0.19758064516129034 | [0.13709677755832672, 0.25806450843811035] | beyond surface |
| qwen2.5-1.5b | itrans | 248 | 0.13306451612903225 | [0.0927419364452362, 0.17741934955120087] | 1 | 0.2782258064516129 | 1 | 0.1532258064516129 | 0.2782258064516129 | 1 | 0.12499999999999997 | [0.07258064299821854, 0.18145161867141724] | partial |
| qwen2.5-1.5b | lower | 248 | 0.13306451612903225 | [0.0927419364452362, 0.17741934955120087] | 1 | 0.21370967741935484 | 1 | 0.15725806451612903 | 0.21370967741935484 | 1 | 0.05645161290322581 | [0.0, 0.11290322244167328] | partial |
| qwen2.5-1.5b | lossy | 248 | 0.20161290322580644 | [0.15322580933570862, 0.2540322542190552] | 1 | 0.2862903225806452 | 1 | 0.16532258064516128 | 0.2862903225806452 | 1 | 0.1209677419354839 | [0.060483869165182114, 0.18145161867141724] | partial |
| qwen2.5-1.5b | natural | 248 | 0.3790322580645161 | [0.31854838132858276, 0.4395161271095276] | 1 | 0.24596774193548387 | 1 | 0.1774193548387097 | 0.24596774193548387 | 1 | 0.06854838709677419 | [0.016129031777381897, 0.125] | partial |
| qwen3.5-2b | native | 248 | 1.0 | [1.0, 1.0] | 9 | 0.9516129032258065 | 7 | 0.11693548387096774 | 0.9516129032258065 | 7 | 0.8346774193548387 | [0.7862903475761414, 0.8790322542190552] | beyond surface |
| qwen3.5-2b | itrans | 248 | 0.18951612903225806 | [0.1411290317773819, 0.23790322244167328] | 10 | 0.28225806451612906 | 2 | 0.13306451612903225 | 0.28225806451612906 | 2 | 0.1491935483870968 | [0.08870967477560043, 0.20967741310596466] | partial |
| qwen3.5-2b | lower | 248 | 0.2661290322580645 | [0.21370968222618103, 0.32258063554763794] | 8 | 0.2661290322580645 | 2 | 0.08870967741935484 | 0.2661290322580645 | 2 | 0.17741935483870966 | [0.11693548411130905, 0.23790322244167328] | beyond surface |
| qwen3.5-2b | lossy | 248 | 0.375 | [0.3145161271095276, 0.4354838728904724] | 7 | 0.3225806451612903 | 3 | 0.12903225806451613 | 0.3225806451612903 | 3 | 0.1935483870967742 | [0.13306452333927155, 0.25806450843811035] | beyond surface |
| qwen3.5-2b | natural | 248 | 0.5120967741935484 | [0.4516128897666931, 0.5725806355476379] | 16 | 0.3225806451612903 | 7 | 0.13709677419354838 | 0.3225806451612903 | 7 | 0.18548387096774194 | [0.11693548411130905, 0.2540322542190552] | beyond surface |
| sarvam-1 | native | 248 | 0.9879032258064516 | [0.9717742204666138, 1.0] | 24 | 0.842741935483871 | 25 | 0.24596774193548387 | 0.842741935483871 | 25 | 0.5967741935483871 | [0.5322580933570862, 0.6612903475761414] | beyond surface |
| sarvam-1 | itrans | 248 | 0.6854838709677419 | [0.625, 0.7419354915618896] | 17 | 0.3185483870967742 | 21 | 0.18951612903225806 | 0.3185483870967742 | 21 | 0.12903225806451613 | [0.05645161122083664, 0.2016129046678543] | partial |
| sarvam-1 | lower | 248 | 0.6169354838709677 | [0.5564516186714172, 0.6774193644523621] | 17 | 0.28225806451612906 | 11 | 0.1774193548387097 | 0.28225806451612906 | 11 | 0.10483870967741937 | [0.04032257944345474, 0.16935484111309052] | partial |
| sarvam-1 | lossy | 248 | 0.8830645161290323 | [0.8427419066429138, 0.9194556474685669] | 17 | 0.5241935483870968 | 27 | 0.23387096774193547 | 0.5241935483870968 | 27 | 0.29032258064516125 | [0.2177419364452362, 0.3588709533214569] | beyond surface |
| sarvam-1 | natural | 248 | 0.9193548387096774 | [0.8830645084381104, 0.9516128897666931] | 18 | 0.6612903225806451 | 24 | 0.18951612903225806 | 0.6612903225806451 | 24 | 0.47177419354838707 | [0.39516130089759827, 0.5483871102333069] | beyond surface |
| gemma4-e2b | native | 248 | 1.0 | [1.0, 1.0] | 7 | 0.9435483870967742 | 7 | 0.20161290322580644 | 0.9435483870967742 | 7 | 0.7419354838709677 | [0.6854838728904724, 0.7943548560142517] | beyond surface |
| gemma4-e2b | itrans | 248 | 0.4435483870967742 | [0.38306450843811035, 0.5080645084381104] | 7 | 0.2540322580645161 | 0 | 0.2540322580645161 | 0.20967741935483872 | 8 | -0.04435483870967741 | [-0.11290322244167328, 0.024193547666072845] | surface-level |
| gemma4-e2b | lower | 248 | 0.4032258064516129 | [0.3427419364452362, 0.46370968222618103] | 7 | 0.23790322580645162 | 0 | 0.23790322580645162 | 0.23790322580645162 | 14 | 0.0 | [-0.06854838877916336, 0.06854838877916336] | surface-level |
| gemma4-e2b | lossy | 248 | 0.5725806451612904 | [0.5080645084381104, 0.6330645084381104] | 8 | 0.3387096774193548 | 7 | 0.25806451612903225 | 0.3387096774193548 | 7 | 0.08064516129032256 | [0.004032257944345474, 0.1572580635547638] | partial |
| gemma4-e2b | natural | 248 | 0.7096774193548387 | [0.6532257795333862, 0.7620967626571655] | 7 | 0.40725806451612906 | 8 | 0.22983870967741934 | 0.40725806451612906 | 8 | 0.17741935483870971 | [0.10080645233392715, 0.2540322542190552] | beyond surface |

#### `results/l_ladder/tokens_per_word.csv` (4,107 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

| model | dataset | form | n_texts | tokens_per_word |
|---|---|---|---|---|
| qwen2.5-1.5b | m4c496 | itrans | 496 | 4.318205062643825 |
| qwen2.5-1.5b | m4c496 | lower | 496 | 4.401176169777551 |
| qwen2.5-1.5b | m4c496 | lossy | 496 | 3.5634108923548964 |
| qwen2.5-1.5b | m4c496 | natural | 496 | 3.528491477995421 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen2.5-1.5b | sentiment | lower | 200 | 4.393317702227432 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen2.5-1.5b | sentiment | natural | 198 | 3.5069712251557403 |
| qwen2.5-1.5b | xnli | itrans | 400 | 4.25161611138737 |
| qwen2.5-1.5b | xnli | lower | 400 | 4.309547488811536 |
| qwen2.5-1.5b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen2.5-1.5b | xnli | natural | 386 | 3.5423465423465426 |
| qwen2.5-1.5b | sib | itrans | 1004 | 4.307793017456359 |
| qwen2.5-1.5b | sib | lower | 1004 | 4.379364089775561 |
| qwen2.5-1.5b | sib | lossy | 1004 | 3.5341645885286783 |
| qwen2.5-1.5b | sib257 | lossy | 257 | 3.534838076545633 |
| qwen2.5-1.5b | sib257 | natural | 257 | 3.4903352091999023 |
| qwen3.5-2b | m4c496 | itrans | 496 | 4.173612886729737 |
| qwen3.5-2b | m4c496 | lower | 496 | 4.21439529532089 |
| qwen3.5-2b | m4c496 | lossy | 496 | 3.3359754538481208 |
| qwen3.5-2b | m4c496 | natural | 496 | 3.3270160264563726 |
| qwen3.5-2b | sentiment | itrans | 200 | 4.087631887456038 |
| qwen3.5-2b | sentiment | lower | 200 | 4.18493552168816 |
| qwen3.5-2b | sentiment | lossy | 200 | 3.3423212192262604 |
| qwen3.5-2b | sentiment | natural | 198 | 3.32275289231682 |
| qwen3.5-2b | xnli | itrans | 400 | 4.1282943809050225 |
| qwen3.5-2b | xnli | lower | 400 | 4.134012928891099 |
| qwen3.5-2b | xnli | lossy | 400 | 3.3431128791645945 |
| qwen3.5-2b | xnli | natural | 386 | 3.346283346283346 |
| qwen3.5-2b | sib | itrans | 1004 | 4.167643391521197 |
| qwen3.5-2b | sib | lower | 1004 | 4.200561097256858 |
| qwen3.5-2b | sib | lossy | 1004 | 3.3111596009975064 |
| qwen3.5-2b | sib257 | lossy | 257 | 3.310107948969578 |
| qwen3.5-2b | sib257 | natural | 257 | 3.2877416197700025 |
| sarvam-1 | m4c496 | itrans | 496 | 5.30107389414472 |
| sarvam-1 | m4c496 | lower | 496 | 5.363206341089236 |
| sarvam-1 | m4c496 | lossy | 496 | 4.343901815392483 |
| sarvam-1 | m4c496 | natural | 496 | 4.308191299923683 |
| sarvam-1 | sentiment | itrans | 200 | 5.238569753810082 |
| sarvam-1 | sentiment | lower | 200 | 5.31242672919109 |
| sarvam-1 | sentiment | lossy | 200 | 4.357561547479484 |
| sarvam-1 | sentiment | natural | 198 | 4.29219816078315 |
| sarvam-1 | xnli | itrans | 400 | 5.226255594231725 |
| sarvam-1 | xnli | lower | 400 | 5.331178518150174 |
| sarvam-1 | xnli | lossy | 400 | 4.335405271009448 |
| sarvam-1 | xnli | natural | 386 | 4.323750323750324 |
| sarvam-1 | sib | itrans | 1004 | 5.287842892768079 |
| sarvam-1 | sib | lower | 1004 | 5.3287406483790525 |
| sarvam-1 | sib | lossy | 1004 | 4.313528678304239 |
| sarvam-1 | sib257 | lossy | 257 | 4.30225711481845 |
| sarvam-1 | sib257 | natural | 257 | 4.252997308539271 |
| gemma4-e2b | m4c496 | itrans | 496 | 4.0164919457939146 |
| gemma4-e2b | m4c496 | lower | 496 | 4.139989772436717 |
| gemma4-e2b | m4c496 | lossy | 496 | 3.20429557657888 |
| gemma4-e2b | m4c496 | natural | 496 | 3.163825998473671 |
| gemma4-e2b | sentiment | itrans | 200 | 3.943434935521688 |
| gemma4-e2b | sentiment | lower | 200 | 4.146248534583822 |
| gemma4-e2b | sentiment | lossy | 200 | 3.2110199296600235 |
| gemma4-e2b | sentiment | natural | 198 | 3.1530703055473155 |
| gemma4-e2b | xnli | itrans | 400 | 3.9604674291397313 |
| gemma4-e2b | xnli | lower | 400 | 4.0790651417205375 |
| gemma4-e2b | xnli | lossy | 400 | 3.2031327697662855 |
| gemma4-e2b | xnli | natural | 386 | 3.1711991711991714 |
| gemma4-e2b | sib | itrans | 1004 | 4.003865336658354 |
| gemma4-e2b | sib | lower | 1004 | 4.120885286783042 |
| gemma4-e2b | sib | lossy | 1004 | 3.174127182044888 |
| gemma4-e2b | sib257 | lossy | 257 | 3.1768891069676153 |
| gemma4-e2b | sib257 | natural | 257 | 3.123073158796183 |
| qwen3-1.7b | m4c496 | itrans | 496 | 4.318205062643825 |
| qwen3-1.7b | m4c496 | lower | 496 | 4.401176169777551 |
| qwen3-1.7b | m4c496 | lossy | 496 | 3.5634108923548964 |
| qwen3-1.7b | m4c496 | natural | 496 | 3.528491477995421 |
| qwen3-1.7b | sentiment | itrans | 200 | 4.22538100820633 |
| qwen3-1.7b | sentiment | lower | 200 | 4.393317702227432 |
| qwen3-1.7b | sentiment | lossy | 200 | 3.5679953106682296 |
| qwen3-1.7b | sentiment | natural | 198 | 3.5069712251557403 |
| qwen3-1.7b | xnli | itrans | 400 | 4.25161611138737 |
| qwen3-1.7b | xnli | lower | 400 | 4.309547488811536 |
| qwen3-1.7b | xnli | lossy | 400 | 3.5532073595226255 |
| qwen3-1.7b | xnli | natural | 386 | 3.5423465423465426 |
| qwen3-1.7b | sib | itrans | 1004 | 4.307793017456359 |
| qwen3-1.7b | sib | lower | 1004 | 4.379364089775561 |
| qwen3-1.7b | sib | lossy | 1004 | 3.5341645885286783 |
| qwen3-1.7b | sib257 | lossy | 257 | 3.534838076545633 |
| qwen3-1.7b | sib257 | natural | 257 | 3.4903352091999023 |

#### `results/l_ladder/tokens_per_word_checks.csv` (6,386 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

| model | dataset | contrast | a | b | tpw_a | tpw_b | ratio | check | check_passed |
|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | m4c496 | L1 | lower | itrans | 4.139989772436717 | 4.0164919457939146 | 1.0307476843747017 | about equal | True |
| gemma4-e2b | m4c496 | L2 | lossy | lower | 3.20429557657888 | 4.139989772436717 | 0.7739863508631071 | differ | True |
| gemma4-e2b | m4c496 | L3 | natural | lossy | 3.163825998473671 | 3.20429557657888 | 0.9873702106631446 | about equal | True |
| gemma4-e2b | sentiment | L1 | lower | itrans | 4.146248534583822 | 3.943434935521688 | 1.0514306949089558 | about equal | True |
| gemma4-e2b | sentiment | L2 | lossy | lower | 3.2110199296600235 | 4.146248534583822 | 0.7744398105605429 | differ | True |
| gemma4-e2b | sentiment | L3 | natural | lossy | 3.1530703055473155 | 3.2110199296600235 | 0.9819528917969551 | about equal | True |
| gemma4-e2b | sib | L1 | lower | itrans | 4.120885286783042 | 4.003865336658354 | 1.0292267447292205 | about equal | True |
| gemma4-e2b | sib | L2 | lossy | lower | 3.174127182044888 | 4.120885286783042 | 0.7702537103435756 | differ | True |
| gemma4-e2b | sib257 | L3 | natural | lossy | 3.123073158796183 | 3.1768891069676153 | 0.9830601741642785 | about equal | True |
| gemma4-e2b | xnli | L1 | lower | itrans | 4.0790651417205375 | 3.9604674291397313 | 1.029945382635445 | about equal | True |
| gemma4-e2b | xnli | L2 | lossy | lower | 3.2031327697662855 | 4.0790651417205375 | 0.7852614896988905 | differ | True |
| gemma4-e2b | xnli | L3 | natural | lossy | 3.1711991711991714 | 3.2031327697662855 | 0.9900305104838211 | about equal | True |
| qwen2.5-1.5b | m4c496 | L1 | lower | itrans | 4.401176169777551 | 4.318205062643825 | 1.0192142582230512 | about equal | True |
| qwen2.5-1.5b | m4c496 | L2 | lossy | lower | 3.5634108923548964 | 4.401176169777551 | 0.8096496833788416 | differ | True |
| qwen2.5-1.5b | m4c496 | L3 | natural | lossy | 3.528491477995421 | 3.5634108923548964 | 0.9902005647357723 | about equal | True |
| qwen2.5-1.5b | sentiment | L1 | lower | itrans | 4.393317702227432 | 4.22538100820633 | 1.0397447457862246 | about equal | True |
| qwen2.5-1.5b | sentiment | L2 | lossy | lower | 3.5679953106682296 | 4.393317702227432 | 0.8121414276184122 | differ | True |
| qwen2.5-1.5b | sentiment | L3 | natural | lossy | 3.5069712251557403 | 3.5679953106682296 | 0.98289681454176 | about equal | True |
| qwen2.5-1.5b | sib | L1 | lower | itrans | 4.379364089775561 | 4.307793017456359 | 1.0166143247897883 | about equal | True |
| qwen2.5-1.5b | sib | L2 | lossy | lower | 3.5341645885286783 | 4.379364089775561 | 0.8070040572282725 | differ | True |
| qwen2.5-1.5b | sib257 | L3 | natural | lossy | 3.4903352091999023 | 3.534838076545633 | 0.9874102104871461 | about equal | True |
| qwen2.5-1.5b | xnli | L1 | lower | itrans | 4.309547488811536 | 4.25161611138737 | 1.0136257309941519 | about equal | True |
| qwen2.5-1.5b | xnli | L2 | lossy | lower | 3.5532073595226255 | 4.309547488811536 | 0.8244966249350949 | differ | True |
| qwen2.5-1.5b | xnli | L3 | natural | lossy | 3.5423465423465426 | 3.5532073595226255 | 0.996943376482947 | about equal | True |
| qwen3-1.7b | m4c496 | L1 | lower | itrans | 4.401176169777551 | 4.318205062643825 | 1.0192142582230512 | about equal | True |
| qwen3-1.7b | m4c496 | L2 | lossy | lower | 3.5634108923548964 | 4.401176169777551 | 0.8096496833788416 | differ | True |
| qwen3-1.7b | m4c496 | L3 | natural | lossy | 3.528491477995421 | 3.5634108923548964 | 0.9902005647357723 | about equal | True |
| qwen3-1.7b | sentiment | L1 | lower | itrans | 4.393317702227432 | 4.22538100820633 | 1.0397447457862246 | about equal | True |
| qwen3-1.7b | sentiment | L2 | lossy | lower | 3.5679953106682296 | 4.393317702227432 | 0.8121414276184122 | differ | True |
| qwen3-1.7b | sentiment | L3 | natural | lossy | 3.5069712251557403 | 3.5679953106682296 | 0.98289681454176 | about equal | True |
| qwen3-1.7b | sib | L1 | lower | itrans | 4.379364089775561 | 4.307793017456359 | 1.0166143247897883 | about equal | True |
| qwen3-1.7b | sib | L2 | lossy | lower | 3.5341645885286783 | 4.379364089775561 | 0.8070040572282725 | differ | True |
| qwen3-1.7b | sib257 | L3 | natural | lossy | 3.4903352091999023 | 3.534838076545633 | 0.9874102104871461 | about equal | True |
| qwen3-1.7b | xnli | L1 | lower | itrans | 4.309547488811536 | 4.25161611138737 | 1.0136257309941519 | about equal | True |
| qwen3-1.7b | xnli | L2 | lossy | lower | 3.5532073595226255 | 4.309547488811536 | 0.8244966249350949 | differ | True |
| qwen3-1.7b | xnli | L3 | natural | lossy | 3.5423465423465426 | 3.5532073595226255 | 0.996943376482947 | about equal | True |
| qwen3.5-2b | m4c496 | L1 | lower | itrans | 4.21439529532089 | 4.173612886729737 | 1.0097714880842983 | about equal | True |
| qwen3.5-2b | m4c496 | L2 | lossy | lower | 3.3359754538481208 | 4.21439529532089 | 0.7915668132868193 | differ | True |
| qwen3.5-2b | m4c496 | L3 | natural | lossy | 3.3270160264563726 | 3.3359754538481208 | 0.9973143005649477 | about equal | True |
| qwen3.5-2b | sentiment | L1 | lower | itrans | 4.18493552168816 | 4.087631887456038 | 1.0238044023804402 | about equal | True |
| qwen3.5-2b | sentiment | L2 | lossy | lower | 3.3423212192262604 | 4.18493552168816 | 0.7986553680229708 | differ | True |
| qwen3.5-2b | sentiment | L3 | natural | lossy | 3.32275289231682 | 3.3423212192262604 | 0.9941452883711847 | about equal | True |
| qwen3.5-2b | sib | L1 | lower | itrans | 4.200561097256858 | 4.167643391521197 | 1.0078983978817935 | about equal | True |
| qwen3.5-2b | sib | L2 | lossy | lower | 3.3111596009975064 | 4.200561097256858 | 0.7882660254983155 | differ | True |
| qwen3.5-2b | sib257 | L3 | natural | lossy | 3.2877416197700025 | 3.310107948969578 | 0.9932430212112756 | about equal | True |
| qwen3.5-2b | xnli | L1 | lower | itrans | 4.134012928891099 | 4.1282943809050225 | 1.0013852083835222 | about equal | True |
| qwen3.5-2b | xnli | L2 | lossy | lower | 3.3431128791645945 | 4.134012928891099 | 0.8086846695134419 | differ | True |
| qwen3.5-2b | xnli | L3 | natural | lossy | 3.346283346283346 | 3.3431128791645945 | 1.0009483577831042 | about equal | True |
| sarvam-1 | m4c496 | L1 | lower | itrans | 5.363206341089236 | 5.30107389414472 | 1.0117207283250935 | about equal | True |
| sarvam-1 | m4c496 | L2 | lossy | lower | 4.343901815392483 | 5.363206341089236 | 0.8099449357583848 | differ | True |
| sarvam-1 | m4c496 | L3 | natural | lossy | 4.308191299923683 | 4.343901815392483 | 0.9917791614575033 | about equal | True |
| sarvam-1 | sentiment | L1 | lower | itrans | 5.31242672919109 | 5.238569753810082 | 1.014098690835851 | about equal | True |
| sarvam-1 | sentiment | L2 | lossy | lower | 4.357561547479484 | 5.31242672919109 | 0.82025819265144 | differ | True |
| sarvam-1 | sentiment | L3 | natural | lossy | 4.29219816078315 | 4.357561547479484 | 0.9850000083798836 | about equal | True |
| sarvam-1 | sib | L1 | lower | itrans | 5.3287406483790525 | 5.287842892768079 | 1.0077342985486402 | about equal | True |
| sarvam-1 | sib | L2 | lossy | lower | 4.313528678304239 | 5.3287406483790525 | 0.8094836966059457 | differ | True |
| sarvam-1 | sib257 | L3 | natural | lossy | 4.252997308539271 | 4.30225711481845 | 0.9885502411956015 | about equal | True |
| sarvam-1 | xnli | L1 | lower | itrans | 5.331178518150174 | 5.226255594231725 | 1.0200761179828735 | about equal | True |
| sarvam-1 | xnli | L2 | lossy | lower | 4.335405271009448 | 5.331178518150174 | 0.8132170506482606 | differ | True |
| sarvam-1 | xnli | L3 | natural | lossy | 4.323750323750324 | 4.335405271009448 | 0.997311682177198 | about equal | True |

#### `results/l_ladder/verdict.json` (2,982 bytes; first commit 64ca06d 2026-10-22 03:14:00 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-22 (romanization ladder)"
provenance.config.lower_scheme = "e09 universal|lower"
provenance.config.m4c_split_seed = 0
provenance.config.counted_retrieval = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
provenance.config.counted_accuracy = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
provenance.config.tpw_tolerance = 0.1
provenance.git_commit = "c1f9aa7f6578d154a899f58b9d3a6c3c0c583883"
provenance.timestamp_utc = "2026-10-21T21:42:11+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/l_ladder.py", "analyse"]
L1|retrieval.verdict = "no effect detected"
L1|retrieval.n_significant_positive = 0
L1|retrieval.n_significant_negative = 0
L1|retrieval.needed = 2
L1|retrieval.n_counted = 3
L1|retrieval.ci_holm_disagreements = ["qwen3.5-2b", "sarvam-1"]
L2|retrieval.verdict = "effect, positive"
L2|retrieval.n_significant_positive = 3
L2|retrieval.n_significant_negative = 0
L2|retrieval.needed = 2
L2|retrieval.n_counted = 3
L3|retrieval.verdict = "effect, positive"
L3|retrieval.n_significant_positive = 2
L3|retrieval.n_significant_negative = 0
L3|retrieval.needed = 2
L3|retrieval.n_counted = 3
L3|retrieval.ci_holm_disagreements = ["sarvam-1"]
L1|sentiment.verdict = "no effect detected"
L1|sentiment.n_significant_positive = 0
L1|sentiment.n_significant_negative = 2
L1|sentiment.needed = 3
L1|sentiment.n_counted = 4
L2|sentiment.verdict = "effect, positive"
L2|sentiment.n_significant_positive = 3
L2|sentiment.n_significant_negative = 0
L2|sentiment.needed = 3
L2|sentiment.n_counted = 4
L3|sentiment.verdict = "no effect detected"
L3|sentiment.n_significant_positive = 0
L3|sentiment.n_significant_negative = 0
L3|sentiment.needed = 3
L3|sentiment.n_counted = 4
L1|sib.verdict = "no effect detected"
L1|sib.n_significant_positive = 2
L1|sib.n_significant_negative = 1
L1|sib.needed = 3
L1|sib.n_counted = 4
L2|sib.verdict = "effect, positive"
L2|sib.n_significant_positive = 4
L2|sib.n_significant_negative = 0
L2|sib.needed = 3
L2|sib.n_counted = 4
L3|sib_L3_secondary.verdict = "no effect detected"
L3|sib_L3_secondary.n_significant_positive = 0
L3|sib_L3_secondary.n_significant_negative = 0
L3|sib_L3_secondary.needed = 3
L3|sib_L3_secondary.n_counted = 4
L3|sib_L3_secondary.ci_holm_disagreements = ["sarvam-1", "qwen3-1.7b"]
`````

#### `results/l_ladder_posthoc/l3_loanfree_register.csv` (692 bytes; first commit bb9fd5b 2026-10-23 00:34:32 +0530)

| dataset | group | n | mean_native_words | mean_natural_words | mean_caps_english | mean_caps_natural | share_with_caps_english |
|---|---|---|---|---|---|---|---|
| retrieval (M4c test half) | other | 118 | 17.25423728813559 | 17.677966101694917 | 2.7203389830508473 | 0.3389830508474576 | 0.7457627118644068 |
| retrieval (M4c test half) | loan-free | 130 | 14.684615384615384 | 14.669230769230769 | 0.9461538461538461 | 0.1 | 0.4 |
| sentiment | other | 118 | 19.864406779661017 | 19.89830508474576 | 0.8050847457627118 | 0.059322033898305086 | 0.3728813559322034 |
| sentiment | loan-free | 80 | 12.775 | 12.7875 | 0.4125 | 0.1 | 0.225 |
| SIB-257 | other | 125 | 17.016 | 17.112 | 2.72 | 0.424 | 0.72 |
| SIB-257 | loan-free | 132 | 14.765151515151516 | 14.757575757575758 | 0.8939393939393939 | 0.12121212121212122 | 0.4090909090909091 |

#### `results/l_ladder_posthoc/l3_loanfree_register_provenance.json` (437 bytes; first commit bb9fd5b 2026-10-23 00:34:32 +0530)

`````text
provenance.config.status = "post hoc descriptive, 2026-10-23, no verdict"
provenance.config.caps = "capitalized words not sentence-initial"
provenance.git_commit = "5daa27e39f56b597cefd4c1b3ac40bc0d6c8dc7c"
provenance.timestamp_utc = "2026-10-22T19:00:50+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/l3_loanfree_register.py"]
rows = 6
`````

#### `results/l_ladder_posthoc/l3_no_english.csv` (2,575 bytes; first commit 70fe375 2026-10-22 20:33:33 +0530)

| measure | model | counted | n_full | L3_full | ci_full | n_no_english | L3_no_english | ci_no_english | p_unadjusted_no_english |
|---|---|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | False | 248 | 0.1774193548387097 | [0.12903225421905518, 0.22983871400356293] | 130 | 0.06153846153846154 | [0.015384615398943424, 0.10769230872392654] | 0.021484375 |
| retrieval | qwen3.5-2b | True | 248 | 0.13709677419354838 | [0.08064515888690948, 0.19354838132858276] | 130 | 0.07692307692307693 | [0.0, 0.1538461595773697] | 0.07551869750022888 |
| retrieval | sarvam-1 | True | 248 | 0.03629032258064513 | [0.004032257944345474, 0.06854838877916336] | 130 | 0.023076923076922995 | [-0.023076923564076424, 0.06923077255487442] | 0.5078125 |
| retrieval | gemma4-e2b | True | 248 | 0.13709677419354838 | [0.08064515888690948, 0.19758065044879913] | 130 | 0.08461538461538465 | [0.0, 0.16923077404499054] | 0.07075554598122835 |
| sentiment | qwen2.5-1.5b | False | 198 | 0.020202020202020166 | [-0.005050505045801401, 0.05050504952669144] | 80 | -0.012500000000000011 | [-0.03750000149011612, 0.0] | 1.0 |
| sentiment | qwen3.5-2b | True | 198 | 0.04040404040404044 | [-0.02525252476334572, 0.10606060922145844] | 80 | -0.012500000000000067 | [-0.10000000149011612, 0.0625] | 1.0 |
| sentiment | sarvam-1 | True | 198 | 0.0 | [-0.04040404036641121, 0.04040404036641121] | 80 | 0.025000000000000022 | [-0.03750000149011612, 0.08749999850988388] | 0.6875 |
| sentiment | gemma4-e2b | True | 198 | 0.015151515151515138 | [-0.035353533923625946, 0.06565656512975693] | 80 | -0.03749999999999998 | [-0.11249999701976776, 0.03750000149011612] | 0.548828125 |
| sentiment | qwen3-1.7b | True | 198 | -0.005050505050505083 | [-0.07575757801532745, 0.06565656512975693] | 80 | -0.025000000000000022 | [-0.15000000596046448, 0.10000000149011612] | 0.8388197422027588 |
| sib_L3_secondary | qwen2.5-1.5b | False | 257 | 0.07392996108949412 | [0.019455252215266228, 0.1284046620130539] | 132 | 0.022727272727272707 | [-0.03787878900766373, 0.09090909361839294] | 0.6476058959960938 |
| sib_L3_secondary | qwen3.5-2b | True | 257 | 0.035019455252918275 | [-0.011673151515424252, 0.08560311049222946] | 132 | 0.022727272727272707 | [-0.03787878900766373, 0.0833333358168602] | 0.6476058959960938 |
| sib_L3_secondary | sarvam-1 | True | 257 | 0.05836575875486383 | [0.015564202331006527, 0.10505836457014084] | 132 | 0.045454545454545414 | [-0.022727273404598236, 0.11363636702299118] | 0.26317596435546875 |
| sib_L3_secondary | gemma4-e2b | True | 257 | 0.05836575875486377 | [0.0, 0.11673151701688766] | 132 | 0.0378787878787879 | [-0.05303030461072922, 0.12878787517547607] | 0.4995598332025112 |
| sib_L3_secondary | qwen3-1.7b | True | 257 | 0.054474708171206254 | [0.0077821011655032635, 0.10116731375455856] | 132 | 0.0 | [-0.05303030461072922, 0.05303030461072922] | 1.0 |

#### `results/l_ladder_posthoc/net_itrans_to_lossy.csv` (740 bytes; first commit f676f15 2026-10-22 18:09:29 +0530)

| model | counted | n | acc_itrans | acc_lossy | L1 | L2 | net_lossy_minus_itrans | ci_low | ci_high | mcnemar_p_unadjusted |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen2.5-1.5b | False | 200 | 0.495 | 0.5 | -0.025 | 0.03 | 0.0050000000000000044 | -0.019999999552965164 | 0.029999999329447746 | 1.0 |
| qwen3.5-2b | True | 200 | 0.655 | 0.68 | -0.1149999999999999 | 0.14 | 0.025000000000000022 | -0.03500000014901161 | 0.09000000357627869 | 0.5327092552361137 |
| sarvam-1 | True | 200 | 0.82 | 0.895 | -0.0549999999999999 | 0.13 | 0.07500000000000007 | 0.02500000037252903 | 0.125 | 0.005924612283706665 |
| gemma4-e2b | True | 200 | 0.755 | 0.79 | -0.185 | 0.22 | 0.03500000000000003 | -0.014999999664723873 | 0.08500000089406967 | 0.26493089646101 |
| qwen3-1.7b | True | 200 | 0.535 | 0.57 | -0.045 | 0.0799999999999999 | 0.03499999999999992 | -0.03999999910593033 | 0.10499999672174454 | 0.42704285650325524 |

#### `results/l_ladder_posthoc/net_itrans_to_lossy_all.csv` (1,968 bytes; first commit 70fe375 2026-10-22 20:33:33 +0530)

| measure | model | n | L1 | L2 | net_lossy_minus_itrans | ci_low | ci_high | mcnemar_p_unadjusted | counted |
|---|---|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | 248 | 0.0 | 0.0685483870967741 | 0.06854838709677419 | 0.032258063554763794 | 0.1088709682226181 | 0.0009105205535888672 | False |
| retrieval | qwen3.5-2b | 248 | 0.0766129032258064 | 0.1088709677419355 | 0.18548387096774194 | 0.12096773833036423 | 0.24596774578094482 | 2.2489162308892232e-08 | True |
| retrieval | sarvam-1 | 248 | -0.0685483870967741 | 0.2661290322580645 | 0.19758064516129037 | 0.1411290317773819 | 0.2540322542190552 | 1.9067358802971057e-11 | True |
| retrieval | gemma4-e2b | 248 | -0.0403225806451613 | 0.1693548387096775 | 0.12903225806451618 | 0.06451612710952759 | 0.19354838132858276 | 0.0002564885942369215 | True |
| sib | qwen2.5-1.5b | 1004 | -0.0029880478087649 | 0.0916334661354582 | 0.08864541832669326 | 0.05876494199037552 | 0.1185258999466896 | 1.1431301135982122e-08 | False |
| sib | qwen3.5-2b | 1004 | 0.0547808764940239 | 0.0796812749003983 | 0.1344621513944223 | 0.10657370835542679 | 0.162350594997406 | 2.5793608864659074e-20 | True |
| sib | sarvam-1 | 1004 | -0.0428286852589641 | 0.2091633466135458 | 0.16633466135458175 | 0.1344621479511261 | 0.19920319318771362 | 3.6266614299672425e-23 | True |
| sib | gemma4-e2b | 1004 | 0.047808764940239 | 0.0826693227091633 | 0.13047808764940239 | 0.09960159659385681 | 0.162350594997406 | 1.2852237490631325e-15 | True |
| sib | qwen3-1.7b | 1004 | 0.0009960159362549 | 0.0657370517928286 | 0.06673306772908366 | 0.04083665460348129 | 0.09262948483228683 | 6.053759985241233e-07 | True |
| sentiment | qwen2.5-1.5b | 200 | -0.025 | 0.03 | 0.005 | -0.0199999995529651 | 0.0299999993294477 | 1.0 | False |
| sentiment | qwen3.5-2b | 200 | -0.1149999999999999 | 0.14 | 0.025 | -0.0350000001490116 | 0.0900000035762786 | 0.5327092552361137 | True |
| sentiment | sarvam-1 | 200 | -0.0549999999999999 | 0.13 | 0.075 | 0.025000000372529 | 0.125 | 0.0059246122837066 | True |
| sentiment | gemma4-e2b | 200 | -0.185 | 0.22 | 0.035 | -0.0149999996647238 | 0.0850000008940696 | 0.26493089646101 | True |
| sentiment | qwen3-1.7b | 200 | -0.045 | 0.0799999999999999 | 0.0349999999999999 | -0.0399999991059303 | 0.1049999967217445 | 0.4270428565032552 | True |

#### `results/l_ladder_posthoc/net_itrans_to_lossy_provenance.json` (406 bytes; first commit f676f15 2026-10-22 18:09:29 +0530)

`````text
provenance.config.status = "post hoc descriptive, 2026-10-22, no verdict"
provenance.config.task = "sentiment (200)"
provenance.git_commit = "5ec703c98f771ec6fecd985c1786bfe7d435af03"
provenance.timestamp_utc = "2026-10-22T12:39:12+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/l_ladder_net.py"]
rows = 5
`````

#### `results/l_ladder_posthoc/posthoc_provenance.json` (448 bytes; first commit 70fe375 2026-10-22 20:33:33 +0530)

`````text
provenance.config.status = "post hoc descriptive, 2026-10-22, no verdict"
provenance.config.english = "wordfreq en Zipf>=3, len>=4"
provenance.git_commit = "0221b44def30c91600373510c02334ec7dc41d45"
provenance.timestamp_utc = "2026-10-22T15:03:09+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/l_ladder_posthoc.py"]
l3_rows = 14
net_rows = 14
`````

## Not dumped (item-level, binary or too large; path and size only)

- none

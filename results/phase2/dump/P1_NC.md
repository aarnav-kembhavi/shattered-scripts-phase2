# NC: NC1: non-canonical tokenization of lossy text (Phase 1)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| registered | `e50581c` | 2026-10-22 18:06:53 +0530 | 1615-1675 | PRE-REGISTRATION — NC1: non-canonical tokenization of lossy text (written 2026-10-22, Aarnav's design; before any NC1 code is written, run or scored) |
| none | `5127d0d` | 2026-10-22 18:17:44 +0530 | 1732-1760 | 2026-10-22 — NC1 pilot (Gemma 4 E2B; 20 sentiment items + 20 M4c sentences): **stopped at the gate** |
| none | `83084bc` | 2026-10-22 20:21:26 +0530 | 1761-1769 | 2026-10-22 — NC1 deviations; gate approved (Aarnav) |
| post hoc, result | `0221b44` | 2026-10-22 20:27:55 +0530 | 1770-1793 | 2026-10-22 — NC1 piece-frequency proxy (post hoc descriptive, 2026-10-22, no verdict) |
| none | `a00f2ff` | 2026-10-22 23:16:03 +0530 | 1839-1895 | 2026-10-22 — NC1 full run: non-canonical tokenization of lossy text (registered 2026-10-22) |
| post hoc, result | `40de234` | 2026-10-22 23:55:36 +0530 | 1896-1969 | 2026-10-22 — NC1 and ladder: independent frequency reference, item-level decomposition, ladder piece familiarity (post hoc descriptive, 2026-10-22, no verdict) |
| post hoc, result | `bb9fd5b` | 2026-10-23 00:34:32 +0530 | 2013-2038 | 2026-10-23 — Notes on NC-F and on the loan-free L3 subset (post hoc descriptive, 2026-10-23, no verdict; Aarnav) |
| registered | `6867631` | 2026-10-23 16:00:59 +0530 | 2436-2471 | PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by Aarnav with changes; b |

## Values observed in the result files (read from the files' own columns and keys)

- models: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
- forms: nc_a, nc_b, nc_c, lossy, lower, itrans, english, natural
- tasks: sib, xnli, sentiment
- conditions: a, b, c
- measures: sib, retrieval, sentiment, xnli_reported_only

Result directories: `results/nc1`, `results/nc1_posthoc`

## RESULTS.md entries, verbatim

##### PRE-REGISTRATION — NC1: non-canonical tokenization of lossy text (written 2026-10-22, Aarnav's design; before any NC1 code is written, run or scored)

RESULTS.md lines 1615 to 1675; first line committed in `e50581c` on 2026-10-22 18:06:53 +0530; last line in `e50581c` on 2026-10-22 18:06:53 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — NC1: non-canonical tokenization of lossy text (written 2026-10-22, Aarnav's design; before any NC1 code is written, run or scored)
**Question.** With the text held fixed (lossy), does more fragmentation alone lower alignment and accuracy? Every
condition decodes to the same lossy string, which removes L2's information-loss confound.

**Conditions** (all on the lossy text; the decoded string of the text span is identical to the lossy text):
- **(a) canonical:** the tokenizer's own output.
- **(b) non-canonical, fragmented:** per sentence, the text-span token count equals that model's token count for the
  **lowercase lossless** (E9 `universal|lower`) version of the same sentence, so tokens per word match the lowercase
  rung.
- **(c) non-canonical, same count:** every word that (b) re-splits is re-split at that word's **canonical** count,
  wherever a non-canonical split at that count exists; per-sentence count = canonical. Controls for out-of-distribution
  segmentation.

**Contrasts.** **NC-F (fragmentation) = (c) − (b)**, predicted significantly positive under the L2 thresholds.
**NC-O (OOD segmentation) = (a) − (c)**, reported separately with CI and Holm p; no prediction.

**Forced splits, per tokenizer.** All four study tokenizers are HF `tokenizers` BPE (Qwen3/Qwen3.5 byte-level with "Ġ";
Sarvam-1 and Gemma 4 with "▁" and byte fallback). Method: **random valid segmentation from the vocabulary** (not merge
dropout, which cannot hit an exact count).
- Units: canonical tokenization grouped into whitespace words via the offset map (a unit is a word with its space
  marker), so pretokenizer boundaries are never crossed.
- For a unit and a target piece count k, a dynamic program counts the segmentations into exactly k vocabulary pieces
  and one is sampled uniformly, rejecting the canonical split. (Lossy is ASCII lowercase; every character is a single
  vocabulary token in all four tokenizers — checked in the pilot.) If the canonical split is the only k-piece
  segmentation, the word stays canonical and is flagged.
- **(b):** extra pieces E = (lowercase-rung count) − (canonical count) are spread over the sentence's words at random,
  each word capped at its character length; every multi-token word is also re-split (at its canonical count if it gets
  no extra piece). If E < 0, words keep their minimal segmentation and the sentence is flagged and counted.
- **(c):** the words re-split in (b) are re-split at their canonical count where a non-canonical split exists
  (single-token words cannot be).
- Seeds: `numpy.random.default_rng` seeded from (base seed 0, model, condition, item id). Only the Kannada text span is
  re-split; prompt templates and calibration inputs stay canonical.

**Checks** (per model and dataset): (b) tokens per word within ±2% of the lowercase rung; (c) per-sentence count exactly
canonical; words re-split in (b) only, in (c) only, in both; token-id rank proxy (median token id of text-span pieces)
for (a), (b), (c). Failing models are flagged, not dropped (as in the ladder).

**Measures and models (as the ladder).** Retrieval: M4c split (seed 0), unmapped test-half acc@1 (248) at the
train-half best layer per model × condition; counted Qwen3.5, Sarvam-1, Gemma 4, effect if ≥ 2 of 3 significant with
the same sign. Accuracy: sentiment 200 and SIB 1,004 count (primary calibration with raw fallback), XNLI reported only;
counted Qwen3, Qwen3.5, Sarvam-1, Gemma 4, effect if ≥ 3 of 4. Qwen2.5 reported, never counted. Exact McNemar, paired
bootstrap 95% CIs (10,000), Holm within each measure over 2 contrasts × counted models; Holm decides on CI/Holm
disagreement. All three conditions go through the same forced-ids code path ((a) recomputed; stored lossy scores used
only for pilot check 4).

**Pilot** (Gemma 4 E2B; 20 sentiment items + 20 M4c sentences; no accuracy or retrieval value computed or looked at;
pilot scores deleted unseen): (1) every forced sequence decodes exactly to the lossy text (20/20 per condition); (2) (b)
per-sentence counts hit target (flagged sentences reported), (c) equals canonical 20/20; (3) words re-split in (b)
only / (c) only / both, and the rank proxy for (a), (b), (c); (4) canonical ids through the new path reproduce the
stored lossy predictions 20/20, max |Δ log-prob| reported; (5) wall time per item, extrapolated.
**Gate:** stop and report to Aarnav; continue only if 1, 2 and 4 pass, (c) re-splits ≥ 80% of multi-token words, and
Aarnav approves the time estimate. Prior estimate from the ladder log (forward 8 min for 2 forms × 4 models; scoring
68 min): about 12 min forward + 3 h scoring for 3 conditions, one model at a time; replaced by the pilot measurement.

**Interpretation (fixed now).** NC-F positive: more fragmentation lowers performance with string, information and OOD
status fixed. NC-F not detected: no evidence of a cost from fragmentation alone at the lowercase-rung level; L2's effect
then belongs to the information/spelling change or to familiar pieces, which NC1 cannot separate. NC-O describes the
cost of unfamiliar splits at equal count only. **If (b) uses substantially rarer pieces than (c), NC-F reflects
fragmentation plus piece rarity; reported as such.**

---
`````

##### 2026-10-22 — NC1 pilot (Gemma 4 E2B; 20 sentiment items + 20 M4c sentences): **stopped at the gate**

RESULTS.md lines 1732 to 1760; first line committed in `5127d0d` on 2026-10-22 18:17:44 +0530; last line in `83084bc` on 2026-10-22 20:21:26 +0530; labels from the title and parent heading: none

`````text
## 2026-10-22 — NC1 pilot (Gemma 4 E2B; 20 sentiment items + 20 M4c sentences): **stopped at the gate**
`scripts/nc1.py` (written after the NC1 registration); outputs `results/nc1/{chars.json, pilot.json}`. No accuracy or
retrieval value was computed; the pilot's log-probs and vectors were held in memory only and not written.

**Checks** (registered gate in bold):
1. **Decode identity:** forced sequences decode to the same text as canonical in 20/20 per condition (sentiment
   prompts and M4c sentences); ids outside the text span are unchanged (CPU dry run, 3 tokenizers, 20/20). **Pass.**
2. **Counts:** (b) hits the lowercase-rung span count in 20/20 (sentiment and M4c; differences all 0); (c) equals
   canonical in 20/20. Tokens per word, sentiment (a) 3.27 / (b) 4.10 / (c) 3.27 (lower target 4.10); M4c 3.09 / 3.99 /
   3.09 (target 3.99). No flagged sentences (no negative extra, no unreachable target). **Pass.**
3. Words re-split, (b) only / (c) only / both, of all words: sentiment 37 / 0 / 292 of 354 (333 multi-token); M4c
   47 / 0 / 262 of 360 (330 multi-token). Words that cannot be re-split at the canonical count (canonical split
   unique): sentiment 24, M4c 31 in (c). Token-id rank proxy (median token id of span pieces): sentiment (a) 6,244 /
   (b) 27,055 / (c) 14,252; M4c 6,244 / 51,405 / 31,012; mean piece length (a) 2.91 / (b) 2.32 / (c) 2.91 chars
   (sentiment). Descriptively (b) uses higher-id (later-merged, presumably rarer) pieces than (c), which falls under
   the registered clause: NC-F would reflect fragmentation plus piece rarity.
4. **Canonical ids through the forced path reproduce stored lossy results:** sentiment raw predictions 20/20, max
   |Δ log-prob| 0.0; M4c sentence vectors max relative |Δ| 0.0. **Pass.**
5. Time: forced path 1.05 × the standard path. Estimate for the full run: scoring 2.8 h (ladder `lower` scoring seconds
   × 1.05 × 3 conditions, 5 models) + forward 14.5 min (Gemma's measured rate, 500 sentences × 3 × 4 models).
- **Gate criterion "(c) re-splits ≥ 80% of multi-token words": sentiment 87.7% (pass), M4c 79.4% (fail, 262 of 330).**
  Per the registration the run does not continue without Aarnav's decision.

**Deviation (recorded now):** the registration says every character of lossy is a single vocabulary token. Checked in
token-string space (what the segmenter works on; `chars.json`): true for all four tokenizers, but Sarvam-1 encodes 36
of 135,816 lossy tokens as byte-fallback tokens (`<0xC2>` etc., from non-ASCII punctuation in the sources); units
containing them are kept canonical and flagged `atomic_token` (Qwen3, Qwen3.5, Gemma 4: 0).

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

##### 2026-10-22 — NC1 piece-frequency proxy (post hoc descriptive, 2026-10-22, no verdict)

RESULTS.md lines 1770 to 1793; first line committed in `0221b44` on 2026-10-22 20:27:55 +0530; last line in `70fe375` on 2026-10-22 20:33:33 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-22 — NC1 piece-frequency proxy (post hoc descriptive, 2026-10-22, no verdict)
Replaces the token-id rank proxy (Aarnav). `scripts/nc1_piece_frequency.py`, CPU, tokenizers only; output
`results/nc1/piece_frequency.csv`. Canonical token frequencies per tokenizer over all lossy text in the study (FLORES+
dev+devtest 2,009, sentiment 200, XNLI 200, SIB 1,004) plus English FLORES+ dev+devtest (2,009); for the pieces of the
Kannada span in each condition: mean / median ln(count + 1) and share of pieces with count 0. Splits regenerated with
NC1's fixed seeds (the ones the run uses); computed without reading any NC1 result.

Mean ln(count + 1), conditions (a) / (b) / (c) (median and unseen share in the CSV):

| model | M4c 496 | sentiment | SIB | XNLI |
|---|---|---|---|---|
| Qwen2.5 / Qwen3 (same tokenizer) | 6.18 / 5.22–5.24 / 4.69–4.71 | 6.14 / 5.14–5.15 / 4.54–4.56 | 6.00 / 5.11–5.12 / 4.53–4.55 | 5.95 / 5.01 / 4.46–4.48 |
| Qwen3.5-2B | 5.87 / 4.98 / 4.41 | 5.96 / 4.93 / 4.39 | 5.85 / 4.97 / 4.38 | 5.89 / 4.92 / 4.34 |
| Sarvam-1 | 7.09 / 6.57 / 6.15 | 7.16 / 6.60 / 6.16 | 7.06 / 6.55 / 6.12 | 7.11 / 6.58 / 6.14 |
| Gemma 4 E2B | 5.66 / 4.74 / 4.17 | 5.77 / 4.71 / 4.14 | 5.63 / 4.73 / 4.15 | 5.68 / 4.71 / 4.15 |

(Qwen2.5 and Qwen3 differ slightly because the seeds include the model name.) In every model and dataset the ordering
is (a) > (b) > (c): **(b) uses more frequent pieces than (c)** (and fewer unseen: Gemma 0.07 vs 0.10, Qwen3.5
0.05 vs 0.08). This reverses the token-id proxy (which put (b)'s median id above (c)'s); id order is not frequency
order. Under this proxy, NC-F = (c) − (b) is not inflated by (b) using rarer pieces. Caveat: (a) is in-distribution
by construction (the reference is canonical); its 2–3% unseen in Qwen comes from the field's first word in a prompt
carrying a leading-space token that the standalone reference texts lack. No verdict.

---
`````

##### 2026-10-22 — NC1 full run: non-canonical tokenization of lossy text (registered 2026-10-22)

RESULTS.md lines 1839 to 1895; first line committed in `a00f2ff` on 2026-10-22 23:16:03 +0530; last line in `40de234` on 2026-10-22 23:55:36 +0530; labels from the title and parent heading: none

`````text
## 2026-10-22 — NC1 full run: non-canonical tokenization of lossy text (registered 2026-10-22)
`scripts/nc1.py` via `scripts/nc1_chain.sh` (detached, one model at a time; forward → score → analyse); analysis at
commit 3b1cf25. Outputs `results/nc1/{segmentation.csv, retrieval.csv, accuracy.csv, contrasts.csv, verdict.json}`;
scores `results/nc1/scores/`; activations `cache/activations/nc1/`. Finished 2026-10-22 23:14 IST.

**Deviation (no method change):** the first score step crashed at 20:56 IST writing one parquet per model × condition
(`ArrowTypeError`: sentiment/XNLI ids are strings, SIB ids are ints). Fixed by writing sentiment+XNLI and SIB to
separate files (commit 3b1cf25) and restarted; cached forward activations reused; Qwen2.5 scoring redone from scratch.

**Checks (registered).** (b) tokens per word within ±2% of the lowercase rung: 20/20 model × dataset (ratio 0.999–
1.002). (c) per-item count equals canonical: all items in every model × dataset. Words re-split in (c) only: 0
everywhere; (b) only (no non-canonical split at the canonical count): 289–2,237 per model × dataset; (c) re-split share
of multi-token words 78.7–88.3% (Sarvam-1 79.2% M4c, 78.7% XNLI, 79.3% SIB; others ≥ 81.6%; the 80% was a pilot gate).
Sentences with negative extra (lowercase count < canonical) flagged: XNLI for Qwen2.5 and Qwen3 only. Token-id rank
proxy (median token id of span pieces), (a) / (b) / (c): Gemma 6,244–7,077 / 29,406–36,464 / 17,335–23,837; Sarvam-1
6,618–7,233 / 43,161–49,839 / 21,437–22,207; Qwen3.5 1,183–1,524 / 647–926 / 7,955–8,080; Qwen2.5 and Qwen3 848–927 /
586–742 / 5,566–5,840.

**NC-F = (c) − (b)** (registered prediction: positive). Holm within measure over 2 contrasts × counted models; Holm
decides on CI/Holm disagreement.

| measure | Qwen3-1.7B | Qwen3.5-2B | Sarvam-1 | Gemma 4 E2B | Qwen2.5 (not counted) | verdict |
|---|---|---|---|---|---|---|
| retrieval (248) | — | +0.073 [+0.012, +0.129] p_H .074 | **+0.117 [+0.065, +0.173] p_H .0002** | −0.044 [−0.105, +0.016] p_H .37 | +0.044 [+0.008, +0.081] | no effect detected (1/3, need 2) |
| sentiment (200) | +0.045 [−0.030, +0.120] p_H 1 | −0.015 [−0.070, +0.040] p_H 1 | −0.055 [−0.125, +0.015] p_H .72 | −0.015 [−0.065, +0.035] p_H 1 | −0.025 [−0.050, −0.005] | no effect detected (0/4, need 3) |
| SIB (1,004) | +0.006 [−0.018, +0.030] p_H 1 | +0.016 [−0.010, +0.043] p_H .77 | **+0.057 [+0.028, +0.084] p_H .0005** | −0.028 [−0.055, −0.001] p_H .21 | −0.010 [−0.035, +0.015] | no effect detected (1/4, need 3) |

**Outcome: NC-F refuted as registered** (not detected on any measure). Per the registered interpretation: no evidence
of a cost from fragmentation alone at the lowercase-rung level; L2's effect belongs to the information/spelling change
or to familiar pieces, which NC1 cannot separate. CI/Holm disagreements (Holm decides): Qwen3.5 retrieval (CI excludes
0, p_H .074); Gemma SIB (CI excludes 0 on the negative side, p_H .21). Only Sarvam-1 shows a fragmentation cost on
retrieval and SIB. Rarity clause: it applies to a positive NC-F, which was not found; for the record, the registered
token-id proxy has (b) above (c) for Gemma and Sarvam-1 and below for the Qwen tokenizers.

**NC-O = (a) − (c)** (reported, no prediction).

| measure | Qwen3-1.7B | Qwen3.5-2B | Sarvam-1 | Gemma 4 E2B | Qwen2.5 (not counted) | verdict |
|---|---|---|---|---|---|---|
| retrieval (248) | — | −0.004 [−0.060, +0.052] p_H 1 | **+0.133 [+0.089, +0.181] p_H < .0001** | **+0.153 [+0.101, +0.206] p_H < .0001** | +0.016 [−0.020, +0.052] | effect, positive (2/3) |
| sentiment (200) | −0.030 [−0.100, +0.040] p_H 1 | **+0.105 [+0.045, +0.165] p_H .010** | **+0.155 [+0.095, +0.220] p_H < .0001** | +0.055 [+0.005, +0.100] p_H .26 | +0.015 [−0.005, +0.040] | no effect detected (2/4, need 3) |
| SIB (1,004) | +0.003 [−0.020, +0.027] p_H 1 | **+0.065 [+0.040, +0.090] p_H < .0001** | **+0.170 [+0.140, +0.201] p_H < .0001** | **+0.074 [+0.048, +0.100] p_H < .0001** | +0.034 [+0.009, +0.058] | effect, positive (3/4) |

CI/Holm disagreement: Gemma sentiment (CI excludes 0, p_H .26). XNLI (reported only) NC-F: all CIs include 0; NC-O:
Sarvam-1 +0.105 [+0.040, +0.170], others include 0.

Accuracy and retrieval levels per condition: `results/nc1/{accuracy.csv, retrieval.csv}` (e.g. Sarvam-1 retrieval
(a) 0.883, (b) 0.633, (c) 0.750; SIB (a) 0.705, (b) 0.478, (c) 0.535).

**Alongside: piece frequency (post hoc descriptive, see the entry above).** Mean ln(count + 1) in the canonical
reference, (a) / (b) / (c), is ordered (a) > (b) > (c) in every model × dataset (e.g. Gemma M4c 5.66 / 4.74 / 4.17;
Sarvam-1 M4c 7.09 / 6.57 / 6.15): by this proxy (c) uses rarer pieces than (b), so NC-F compares more but more
frequent pieces against fewer but rarer ones. This proxy and the registered token-id proxy disagree for Gemma and
Sarvam-1. Post hoc, no verdict.

**Next:** report to Aarnav; no further NC1 runs planned.

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

##### 2026-10-23 — Notes on NC-F and on the loan-free L3 subset (post hoc descriptive, 2026-10-23, no verdict; Aarnav)

RESULTS.md lines 2013 to 2038; first line committed in `bb9fd5b` on 2026-10-23 00:34:32 +0530; last line in `6105b0c` on 2026-10-23 00:51:18 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-23 — Notes on NC-F and on the loan-free L3 subset (post hoc descriptive, 2026-10-23, no verdict; Aarnav)
**NC-F's null is not interpretable as "no fragmentation cost at inference".** The registered verdict (NC-F refuted)
stands. But in the A2 item-level decomposition (2026-10-22, `results/nc1_posthoc/decomposition.csv`), extra pieces and
piece frequency correlate 0.59–0.73 across (b)/(c) items, and once frequency is included, extra pieces carry a negative
coefficient with a 95% CI excluding 0 (unadjusted) in Sarvam-1 retrieval (−0.0036 per piece), Sarvam-1 SIB (−0.015),
Gemma 4 SIB (−0.046) and Qwen3 sentiment (−0.028). NC1 compared more-but-more-frequent pieces (b) with
fewer-but-rarer pieces (c), so the two costs can offset in NC-F; NC1 does not separate them.

**The loan-free L3 subset differs in register.** `scripts/l3_loanfree_register.py`, output
`results/l_ladder_posthoc/l3_loanfree_register.csv`. Named-entity proxy: capitalized words that are not
sentence-initial (English source; the natural romanizations are mostly lowercase, so their count is near 0).

| sample | group | n | native words | natural words | caps (English) | items with ≥ 1 (English) | caps (natural) |
|---|---|---|---|---|---|---|---|
| retrieval (M4c test half) | loan-free | 130 | 14.7 | 14.7 | 0.95 | 40% | 0.10 |
| | other | 118 | 17.3 | 17.7 | 2.72 | 75% | 0.34 |
| sentiment (198) | loan-free | 80 | 12.8 | 12.8 | 0.41 | 22% | 0.10 |
| | other | 118 | 19.9 | 19.9 | 0.81 | 37% | 0.06 |
| SIB-257 | loan-free | 132 | 14.8 | 14.8 | 0.89 | 41% | 0.12 |
| | other | 125 | 17.0 | 17.1 | 2.72 | 72% | 0.42 |

Loan-free items are shorter (2–7 native words) and carry about a third as many named entities (English side) on
retrieval and SIB. The smaller loan-free L3 estimates may therefore reflect fewer names and shorter sentences as much
as the absence of English loans; the subset analysis cannot separate these.

---
`````

##### PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by Aarnav with changes; before any patching code is written or run)

RESULTS.md lines 2436 to 2471; first line committed in `6867631` on 2026-10-23 16:00:59 +0530; last line in `6867631` on 2026-10-23 16:00:59 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by Aarnav with changes; before any patching code is written or run)
Local 2B models only, bf16, one model load at a time. Script `scripts/ep_patching.py` (written after this
registration); outputs `results/ep1/`.
- **Question.** NC-O showed that unfamiliar segmentations at the same token count cost accuracy (SIB: Qwen3.5,
  Sarvam-1, Gemma 4). Is that cost carried by the word representations built at each word's last token? (a) and (c)
  decode to the same lossy text and every word has the same number of pieces in both, so token positions align exactly.
- **Models:** Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B. Qwen2.5 is not run.
- **Items** (stored NC1 scores, calibrated primary rule), per model × task: primary = (a) correct and (c) wrong;
  control = (c) correct and (a) wrong. Available (primary / control), SIB: Qwen3 73/70, Qwen3.5 117/52, Sarvam-1
  222/51, Gemma 4 133/59; sentiment: 23/29, 31/10, 39/8, 18/7. **Primary SIB items capped at 200 per model (random,
  seed 0); all control items.** SIB carries the prediction; sentiment (n < 40) is descriptive.
- **Metric.** Gold margin M at the final prompt position: logit of the gold verbalizer's first token minus the largest
  logit among the other verbalizers' first tokens. Pilot check: first tokens must be distinct per tokenizer; otherwise
  the full-verbalizer log-prob margin is used for that model (logged).
- **Patching** at layer L (residual stream entering layer L; L = 0 is the embedding output; L = 0..N); the template
  stays canonical in both runs:
  - **final (primary):** replace the residual at every text word's last-token position in the (c) run with the (a)
    run's residual at the same position.
  - **all pieces (added; no prediction):** replace the residual at every piece of every text word.
  - Recovery R(L) = mean(M_patched − M_c) / mean(M_a − M_c) (ratio of means), bootstrap 95% CI (10,000 over items).
    R_all(L) is reported next to R_final(L).
- **Selection-safe peak.** 50/50 item split (seed 0); L* = argmax R_final(L) on the selection half; R_final(L*) and CI
  on the held-out half; full curves on all items.
- **Predictions (SIB, primary items):**
  - **P1a:** held-out R_final(L*) has a 95% CI lower bound > 0.5 in ≥ 3 of 4 models.
  - **P1b:** L* ≤ ⌊2N/3⌋ in ≥ 3 of 4 models.
  - **Control (reported):** on control items R(L*) has the same sign.
- **Caveats:** discordant-item selection inflates M_a − M_c (regression to the mean); Gemma 4's per-layer embeddings
  make its residual patches partial (lower bound); for "final", non-final pieces stay as in (c).
- **Pilot (Qwen3.5-2B, 10 SIB primary items); each check stops the run on failure:**
  1. Patching all text positions at L = 0 reproduces M_a (|Δ| < 0.05).
  2. Patching nothing reproduces M_c (|Δ| < 0.05).
  3. Patched-position indices map to the same decoded word in (a) and (c) (10/10).
  4. Wall time per item × layer × scheme, extrapolated. **Stop at the pilot gate and report.**

---
`````

## Result files, every number

#### `results/nc1/accuracy.csv` (12,457 bytes; first commit a00f2ff 2026-10-22 23:16:03 +0530)

| model | task | form | n | chance | acc_cal | acc_cal_ci_low | acc_cal_ci_high | constant_label_rate_cal | acc_raw | acc_raw_ci_low | acc_raw_ci_high | constant_label_rate_raw | acc_na | acc_na_ci_low | acc_na_ci_high | constant_label_rate_na | acc_avg3 | acc_avg3_ci_low | acc_avg3_ci_high | constant_label_rate_avg3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemma4-e2b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 | 0.985 | 0.965 | 1.0 | 0.505 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.505 |
| gemma4-e2b | sentiment | nc_a | 200 | 0.5 | 0.79 | 0.73 | 0.845 | 0.65 | 0.79 | 0.73 | 0.845 | 0.65 | 0.785 | 0.725 | 0.84 | 0.625 | 0.79 | 0.73 | 0.845 | 0.65 |
| gemma4-e2b | sentiment | nc_b | 200 | 0.5 | 0.75 | 0.69 | 0.81 | 0.68 | 0.755 | 0.695 | 0.815 | 0.675 | 0.76 | 0.7 | 0.815 | 0.65 | 0.75 | 0.69 | 0.81 | 0.68 |
| gemma4-e2b | sentiment | nc_c | 200 | 0.5 | 0.735 | 0.675 | 0.795 | 0.675 | 0.735 | 0.675 | 0.795 | 0.675 | 0.715 | 0.65 | 0.775 | 0.645 | 0.735 | 0.675 | 0.795 | 0.675 |
| gemma4-e2b | xnli | english | 200 | 0.3333333333333333 | 0.735 | 0.675 | 0.795 | 0.405 | 0.735 | 0.675 | 0.795 | 0.405 | 0.6 | 0.53 | 0.67 | 0.56 | 0.63 | 0.565 | 0.695 | 0.565 |
| gemma4-e2b | xnli | nc_a | 200 | 0.3333333333333333 | 0.4 | 0.335 | 0.47 | 0.84 | 0.4 | 0.335 | 0.47 | 0.84 | 0.395 | 0.33 | 0.46 | 0.78 | 0.375 | 0.31 | 0.44 | 0.835 |
| gemma4-e2b | xnli | nc_b | 200 | 0.3333333333333333 | 0.4 | 0.335 | 0.47 | 0.92 | 0.4 | 0.335 | 0.47 | 0.92 | 0.43 | 0.36 | 0.5 | 0.815 | 0.415 | 0.35 | 0.485 | 0.74 |
| gemma4-e2b | xnli | nc_c | 200 | 0.3333333333333333 | 0.39 | 0.325 | 0.46 | 0.93 | 0.39 | 0.325 | 0.46 | 0.93 | 0.405 | 0.335 | 0.475 | 0.83 | 0.4 | 0.335 | 0.4651249999999982 | 0.83 |
| qwen2.5-1.5b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.52 | 0.45 | 0.59 | 0.98 | 0.88 | 0.835 | 0.925 | 0.62 |
| qwen2.5-1.5b | sentiment | nc_a | 200 | 0.5 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 0.97 | 0.5 | 0.43 | 0.57 | 1.0 | 0.5 | 0.43 | 0.57 | 1.0 |
| qwen2.5-1.5b | sentiment | nc_b | 200 | 0.5 | 0.51 | 0.44 | 0.58 | 0.96 | 0.51 | 0.44 | 0.58 | 0.96 | 0.5 | 0.43 | 0.57 | 1.0 | 0.495 | 0.425 | 0.565 | 0.995 |
| qwen2.5-1.5b | sentiment | nc_c | 200 | 0.5 | 0.485 | 0.415 | 0.555 | 0.975 | 0.485 | 0.415 | 0.555 | 0.975 | 0.5 | 0.43 | 0.57 | 1.0 | 0.495 | 0.425 | 0.565 | 0.995 |
| qwen2.5-1.5b | xnli | english | 200 | 0.3333333333333333 | 0.825 | 0.77 | 0.875 | 0.38 | 0.795 | 0.735 | 0.85 | 0.45 | 0.785 | 0.73 | 0.84 | 0.49 | 0.825 | 0.77 | 0.875 | 0.38 |
| qwen2.5-1.5b | xnli | nc_a | 200 | 0.3333333333333333 | 0.325 | 0.26 | 0.39 | 0.75 | 0.375 | 0.31 | 0.445 | 0.84 | 0.33 | 0.265 | 0.395 | 0.955 | 0.325 | 0.26 | 0.39 | 0.75 |
| qwen2.5-1.5b | xnli | nc_b | 200 | 0.3333333333333333 | 0.38 | 0.315 | 0.45 | 0.75 | 0.375 | 0.31 | 0.445 | 0.74 | 0.355 | 0.29 | 0.42 | 0.95 | 0.38 | 0.315 | 0.45 | 0.75 |
| qwen2.5-1.5b | xnli | nc_c | 200 | 0.3333333333333333 | 0.365 | 0.3 | 0.435 | 0.75 | 0.355 | 0.29 | 0.42 | 0.795 | 0.335 | 0.27 | 0.4 | 0.955 | 0.365 | 0.3 | 0.435 | 0.75 |
| qwen3-1.7b | sentiment | english | 200 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 | 0.985 | 0.965 | 1.0 | 0.515 | 0.98 | 0.96 | 0.995 | 0.5 | 0.985 | 0.965 | 1.0 | 0.515 |
| qwen3-1.7b | sentiment | nc_a | 200 | 0.5 | 0.57 | 0.5 | 0.64 | 0.68 | 0.575 | 0.505 | 0.64 | 0.715 | 0.52 | 0.45 | 0.59 | 0.91 | 0.57 | 0.5 | 0.64 | 0.68 |
| qwen3-1.7b | sentiment | nc_b | 200 | 0.5 | 0.555 | 0.485 | 0.625 | 0.555 | 0.505 | 0.435 | 0.575 | 0.855 | 0.57 | 0.5 | 0.64 | 0.8 | 0.555 | 0.485 | 0.625 | 0.555 |
| qwen3-1.7b | sentiment | nc_c | 200 | 0.5 | 0.6 | 0.53 | 0.67 | 0.56 | 0.57 | 0.5 | 0.64 | 0.8 | 0.555 | 0.485 | 0.625 | 0.855 | 0.6 | 0.53 | 0.67 | 0.56 |
| qwen3-1.7b | xnli | english | 200 | 0.3333333333333333 | 0.575 | 0.505 | 0.645 | 0.71 | 0.615 | 0.545 | 0.68 | 0.53 | 0.54 | 0.47 | 0.61 | 0.765 | 0.575 | 0.505 | 0.645 | 0.71 |
| qwen3-1.7b | xnli | nc_a | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.995 | 0.415 | 0.345 | 0.485 | 0.795 | 0.335 | 0.27 | 0.4 | 0.995 | 0.335 | 0.27 | 0.4 | 0.995 |
| qwen3-1.7b | xnli | nc_b | 200 | 0.3333333333333333 | 0.33 | 0.265 | 0.395 | 0.975 | 0.4 | 0.33 | 0.47 | 0.65 | 0.34 | 0.275 | 0.405 | 0.995 | 0.33 | 0.265 | 0.395 | 0.975 |
| qwen3-1.7b | xnli | nc_c | 200 | 0.3333333333333333 | 0.33 | 0.265 | 0.395 | 0.98 | 0.425 | 0.355 | 0.495 | 0.71 | 0.33 | 0.265 | 0.395 | 0.995 | 0.33 | 0.265 | 0.395 | 0.98 |
| qwen3.5-2b | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.525 | 0.98 | 0.96 | 0.995 | 0.51 |
| qwen3.5-2b | sentiment | nc_a | 200 | 0.5 | 0.68 | 0.615 | 0.74 | 0.72 | 0.675 | 0.61 | 0.735 | 0.645 | 0.645 | 0.58 | 0.71 | 0.815 | 0.68 | 0.615 | 0.74 | 0.72 |
| qwen3.5-2b | sentiment | nc_b | 200 | 0.5 | 0.59 | 0.52 | 0.655 | 0.78 | 0.57 | 0.5 | 0.635 | 0.74 | 0.575 | 0.505 | 0.645 | 0.855 | 0.59 | 0.52 | 0.655 | 0.78 |
| qwen3.5-2b | sentiment | nc_c | 200 | 0.5 | 0.575 | 0.505 | 0.64 | 0.795 | 0.585 | 0.515 | 0.65 | 0.675 | 0.58 | 0.51 | 0.645 | 0.87 | 0.575 | 0.505 | 0.64 | 0.795 |
| qwen3.5-2b | xnli | english | 200 | 0.3333333333333333 | 0.49 | 0.42 | 0.56 | 0.805 | 0.43 | 0.36 | 0.5 | 0.89 | 0.45 | 0.38 | 0.52 | 0.845 | 0.49 | 0.42 | 0.56 | 0.805 |
| qwen3.5-2b | xnli | nc_a | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.99 | 0.34 | 0.275 | 0.405 | 0.995 | 0.335 | 0.27 | 0.4 | 0.99 | 0.335 | 0.27 | 0.4 | 0.99 |
| qwen3.5-2b | xnli | nc_b | 200 | 0.3333333333333333 | 0.34 | 0.275 | 0.405 | 0.995 | 0.335 | 0.27 | 0.4 | 1.0 | 0.34 | 0.275 | 0.405 | 0.995 | 0.34 | 0.275 | 0.405 | 0.995 |
| qwen3.5-2b | xnli | nc_c | 200 | 0.3333333333333333 | 0.335 | 0.27 | 0.4 | 0.99 | 0.34 | 0.275 | 0.405 | 0.995 | 0.335 | 0.27 | 0.4 | 0.99 | 0.335 | 0.27 | 0.4 | 0.99 |
| sarvam-1 | sentiment | english | 200 | 0.5 | 0.98 | 0.96 | 0.995 | 0.51 | 0.975 | 0.95 | 0.995 | 0.505 | 0.975 | 0.95 | 0.995 | 0.515 | 0.98 | 0.96 | 0.995 | 0.51 |
| sarvam-1 | sentiment | nc_a | 200 | 0.5 | 0.895 | 0.85 | 0.935 | 0.575 | 0.91 | 0.87 | 0.95 | 0.51 | 0.86 | 0.81 | 0.905 | 0.63 | 0.895 | 0.85 | 0.935 | 0.575 |
| sarvam-1 | sentiment | nc_b | 200 | 0.5 | 0.795 | 0.735 | 0.85 | 0.625 | 0.82 | 0.765 | 0.87 | 0.56 | 0.72 | 0.655 | 0.78 | 0.76 | 0.795 | 0.735 | 0.85 | 0.625 |
| sarvam-1 | sentiment | nc_c | 200 | 0.5 | 0.74 | 0.68 | 0.8 | 0.59 | 0.78 | 0.72 | 0.835 | 0.54 | 0.685 | 0.62 | 0.75 | 0.715 | 0.74 | 0.68 | 0.8 | 0.59 |
| sarvam-1 | xnli | english | 200 | 0.3333333333333333 | 0.55 | 0.48 | 0.62 | 0.545 | 0.53 | 0.46 | 0.6 | 0.63 | 0.475 | 0.405 | 0.545 | 0.655 | 0.55 | 0.48 | 0.62 | 0.545 |
| sarvam-1 | xnli | nc_a | 200 | 0.3333333333333333 | 0.47 | 0.4 | 0.54 | 0.58 | 0.46 | 0.39 | 0.53 | 0.595 | 0.375 | 0.31 | 0.44 | 0.905 | 0.47 | 0.4 | 0.54 | 0.58 |
| sarvam-1 | xnli | nc_b | 200 | 0.3333333333333333 | 0.39 | 0.32 | 0.46 | 0.79 | 0.395 | 0.325 | 0.465 | 0.81 | 0.35 | 0.285 | 0.415 | 0.88 | 0.39 | 0.32 | 0.46 | 0.79 |
| sarvam-1 | xnli | nc_c | 200 | 0.3333333333333333 | 0.365 | 0.3 | 0.435 | 0.77 | 0.365 | 0.3 | 0.435 | 0.78 | 0.34 | 0.275 | 0.405 | 0.915 | 0.365 | 0.3 | 0.435 | 0.77 |
| gemma4-e2b | sib | english | 1004 | 0.14285714285714285 | 0.7938247011952191 | 0.7689243027888446 | 0.8187250996015937 | 0.20916334661354583 | 0.8007968127490039 | 0.7758964143426295 | 0.8256972111553785 | 0.21314741035856574 | 0.8007968127490039 | 0.7758964143426295 | 0.8256972111553785 | 0.2151394422310757 | 0.7938247011952191 | 0.7689243027888446 | 0.8187250996015937 | 0.20916334661354583 |
| gemma4-e2b | sib | nc_a | 1004 | 0.14285714285714285 | 0.49701195219123506 | 0.46613545816733065 | 0.5278884462151394 | 0.22709163346613545 | 0.5139442231075697 | 0.48306772908366535 | 0.545816733067729 | 0.2290836653386454 | 0.499003984063745 | 0.4681274900398406 | 0.5308764940239044 | 0.23207171314741035 | 0.49701195219123506 | 0.46613545816733065 | 0.5278884462151394 | 0.22709163346613545 |
| gemma4-e2b | sib | nc_b | 1004 | 0.14285714285714285 | 0.45119521912350596 | 0.4213147410358566 | 0.4820717131474104 | 0.2778884462151394 | 0.45219123505976094 | 0.4213147410358566 | 0.48306772908366535 | 0.29382470119521914 | 0.45617529880478086 | 0.4252988047808765 | 0.48705179282868527 | 0.30776892430278885 | 0.45119521912350596 | 0.4213147410358566 | 0.4820717131474104 | 0.2778884462151394 |
| gemma4-e2b | sib | nc_c | 1004 | 0.14285714285714285 | 0.42330677290836655 | 0.39243027888446214 | 0.4531872509960159 | 0.250996015936255 | 0.43824701195219123 | 0.4073705179282869 | 0.46912350597609564 | 0.250996015936255 | 0.43227091633466136 | 0.40139442231075695 | 0.4631474103585657 | 0.2549800796812749 | 0.42330677290836655 | 0.39243027888446214 | 0.4531872509960159 | 0.250996015936255 |
| qwen2.5-1.5b | sib | english | 1004 | 0.14285714285714285 | 0.796812749003984 | 0.7719123505976095 | 0.8217131474103586 | 0.18725099601593626 | 0.7141434262948207 | 0.6862549800796812 | 0.7420318725099602 | 0.29382470119521914 | 0.8077689243027888 | 0.7828685258964143 | 0.8316733067729084 | 0.20219123505976094 | 0.796812749003984 | 0.7719123505976095 | 0.8217131474103586 | 0.18725099601593626 |
| qwen2.5-1.5b | sib | nc_a | 1004 | 0.14285714285714285 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.351593625498008 | 0.2798804780876494 | 0.25298804780876494 | 0.30876494023904383 | 0.6892430278884463 | 0.40039840637450197 | 0.3705179282868526 | 0.4312749003984064 | 0.24402390438247012 | 0.3665338645418327 | 0.33665338645418325 | 0.39641434262948205 | 0.351593625498008 |
| qwen2.5-1.5b | sib | nc_b | 1004 | 0.14285714285714285 | 0.3426294820717131 | 0.3137450199203187 | 0.37250996015936255 | 0.4103585657370518 | 0.23705179282868527 | 0.21115537848605578 | 0.2639442231075697 | 0.7529880478087649 | 0.3665338645418327 | 0.3376494023904382 | 0.39641434262948205 | 0.27091633466135456 | 0.3426294820717131 | 0.3137450199203187 | 0.37250996015936255 | 0.4103585657370518 |
| qwen2.5-1.5b | sib | nc_c | 1004 | 0.14285714285714285 | 0.33266932270916333 | 0.3047808764940239 | 0.36254980079681276 | 0.4103585657370518 | 0.23705179282868527 | 0.21115537848605578 | 0.2639442231075697 | 0.7559760956175299 | 0.3804780876494024 | 0.350597609561753 | 0.4103585657370518 | 0.2689243027888446 | 0.33266932270916333 | 0.3047808764940239 | 0.36254980079681276 | 0.4103585657370518 |
| qwen3-1.7b | sib | english | 1004 | 0.14285714285714285 | 0.7818725099601593 | 0.7559760956175299 | 0.8067729083665338 | 0.20916334661354583 | 0.7848605577689243 | 0.7589641434262948 | 0.8097609561752988 | 0.19621513944223107 | 0.7808764940239044 | 0.7549800796812749 | 0.8057768924302788 | 0.2061752988047809 | 0.7818725099601593 | 0.7559760956175299 | 0.8067729083665338 | 0.20916334661354583 |
| qwen3-1.7b | sib | nc_a | 1004 | 0.14285714285714285 | 0.30677290836653387 | 0.2788844621513944 | 0.33565737051792827 | 0.34063745019920316 | 0.30876494023904383 | 0.2798804780876494 | 0.3386454183266932 | 0.35358565737051795 | 0.299800796812749 | 0.27091633466135456 | 0.3286852589641434 | 0.3595617529880478 | 0.30677290836653387 | 0.2788844621513944 | 0.33565737051792827 | 0.34063745019920316 |
| qwen3-1.7b | sib | nc_b | 1004 | 0.14285714285714285 | 0.29780876494023906 | 0.2699203187250996 | 0.3256972111553785 | 0.351593625498008 | 0.30876494023904383 | 0.2798804780876494 | 0.3376494023904382 | 0.37250996015936255 | 0.2918326693227092 | 0.2639442231075697 | 0.3197211155378486 | 0.351593625498008 | 0.29780876494023906 | 0.2699203187250996 | 0.3256972111553785 | 0.351593625498008 |
| qwen3-1.7b | sib | nc_c | 1004 | 0.14285714285714285 | 0.30378486055776893 | 0.27589641434262946 | 0.33266932270916333 | 0.32270916334661354 | 0.3107569721115538 | 0.28286852589641437 | 0.3396414342629482 | 0.2948207171314741 | 0.29780876494023906 | 0.2699203187250996 | 0.32669322709163345 | 0.3804780876494024 | 0.30378486055776893 | 0.27589641434262946 | 0.33266932270916333 | 0.32270916334661354 |
| qwen3.5-2b | sib | english | 1004 | 0.14285714285714285 | 0.8037848605577689 | 0.7788844621513944 | 0.8286852589641435 | 0.2400398406374502 | 0.7280876494023905 | 0.700199203187251 | 0.7549800796812749 | 0.2410358565737052 | 0.8057768924302788 | 0.7808764940239044 | 0.8296812749003984 | 0.2589641434262948 | 0.8037848605577689 | 0.7788844621513944 | 0.8286852589641435 | 0.2400398406374502 |
| qwen3.5-2b | sib | nc_a | 1004 | 0.14285714285714285 | 0.3754980079681275 | 0.3466135458167331 | 0.4063745019920319 | 0.3804780876494024 | 0.26593625498007967 | 0.23904382470119523 | 0.29382470119521914 | 0.7460159362549801 | 0.4123505976095618 | 0.38247011952191234 | 0.44322709163346613 | 0.2689243027888446 | 0.3754980079681275 | 0.3466135458167331 | 0.4063745019920319 | 0.3804780876494024 |
| qwen3.5-2b | sib | nc_b | 1004 | 0.14285714285714285 | 0.2948207171314741 | 0.26693227091633465 | 0.3237051792828685 | 0.4631474103585657 | 0.22709163346613545 | 0.20119521912350596 | 0.25301294820717096 | 0.7858565737051793 | 0.3545816733067729 | 0.3256972111553785 | 0.3844621513944223 | 0.2968127490039841 | 0.2948207171314741 | 0.26693227091633465 | 0.3237051792828685 | 0.4631474103585657 |
| qwen3.5-2b | sib | nc_c | 1004 | 0.14285714285714285 | 0.3107569721115538 | 0.28286852589641437 | 0.3396414342629482 | 0.48904382470119523 | 0.23107569721115537 | 0.2051792828685259 | 0.25796812749003983 | 0.7788844621513944 | 0.3545816733067729 | 0.3247011952191235 | 0.3844621513944223 | 0.32768924302788843 | 0.3107569721115538 | 0.28286852589641437 | 0.3396414342629482 | 0.48904382470119523 |
| sarvam-1 | sib | english | 1004 | 0.14285714285714285 | 0.7679282868525896 | 0.7420318725099602 | 0.7938247011952191 | 0.26294820717131473 | 0.5737051792828686 | 0.5428286852589641 | 0.6045816733067729 | 0.398406374501992 | 0.7539840637450199 | 0.7270916334661355 | 0.7808764940239044 | 0.33167330677290835 | 0.7679282868525896 | 0.7420318725099602 | 0.7938247011952191 | 0.26294820717131473 |
| sarvam-1 | sib | nc_a | 1004 | 0.14285714285714285 | 0.7051792828685259 | 0.6772908366533864 | 0.7330677290836654 | 0.2340637450199203 | 0.46115537848605576 | 0.4312749003984064 | 0.49203187250996017 | 0.41932270916334663 | 0.7101593625498008 | 0.6822709163346613 | 0.7380478087649402 | 0.33067729083665337 | 0.7051792828685259 | 0.6772908366533864 | 0.7330677290836654 | 0.2340637450199203 |
| sarvam-1 | sib | nc_b | 1004 | 0.14285714285714285 | 0.47808764940239046 | 0.44721115537848605 | 0.5089641434262948 | 0.4243027888446215 | 0.26294820717131473 | 0.2360557768924303 | 0.2898406374501992 | 0.6344621513944223 | 0.450199203187251 | 0.41932270916334663 | 0.4810756972111554 | 0.6703187250996016 | 0.47808764940239046 | 0.44721115537848605 | 0.5089641434262948 | 0.4243027888446215 |
| sarvam-1 | sib | nc_c | 1004 | 0.14285714285714285 | 0.5348605577689243 | 0.5039840637450199 | 0.5657370517928287 | 0.34063745019920316 | 0.3197211155378486 | 0.2908366533864542 | 0.34860557768924305 | 0.5747011952191236 | 0.5368525896414342 | 0.5059760956175299 | 0.5677290836653387 | 0.5298804780876494 | 0.5348605577689243 | 0.5039840637450199 | 0.5657370517928287 | 0.34063745019920316 |

#### `results/nc1/chars.json` (1,136 bytes; first commit 5127d0d 2026-10-22 18:17:44 +0530)

`````text
provenance.config.texts = 2104
provenance.git_commit = "f676f15a822da091a9032f0c46c7d3fa6719323e"
provenance.timestamp_utc = "2026-10-22T12:43:50+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/nc1.py", "chars"]
qwen3-1.7b.n_tokens = 111303
qwen3-1.7b.n_atomic_tokens = 0
qwen3-1.7b.n_chars = 92
qwen3.5-2b.n_tokens = 104313
qwen3.5-2b.n_atomic_tokens = 0
qwen3.5-2b.n_chars = 92
sarvam-1.n_tokens = 135816
sarvam-1.n_atomic_tokens = 36
sarvam-1.atomic_examples = ["<0x80>", "<0x8B>", "<0x95>", "<0xB2>", "<0xB5>", "<0xBD>", "<0xBE>", "<0xC2>", "<0xC3>", "<0xE2>"]
sarvam-1.n_chars = 82
gemma4-e2b.n_tokens = 100058
gemma4-e2b.n_atomic_tokens = 0
gemma4-e2b.n_chars = 89
`````

#### `results/nc1/contrasts.csv` (6,916 bytes; first commit a00f2ff 2026-10-22 23:16:03 +0530)

| measure | model | contrast | a | b | n | acc_a | acc_b | diff | ci | a_only | b_only | p | counted | p_holm | significant | ci_excludes_0 | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | NC-F | c | b | 248 | 0.18548387096774194 | 0.14112903225806453 | 0.04435483870967741 | [0.008064515888690948, 0.08064515888690948] | 17 | 6 | 0.03468966484069824 | False |  | False | True | False |
| retrieval | qwen2.5-1.5b | NC-O | a | c | 248 | 0.20161290322580644 | 0.18548387096774194 | 0.016129032258064502 | [-0.02016128972172737, 0.052419353276491165] | 12 | 8 | 0.5034446716308594 | False |  | False | False | False |
| retrieval | qwen3.5-2b | NC-F | c | b | 248 | 0.3790322580645161 | 0.3064516129032258 | 0.07258064516129031 | [0.012096773833036423, 0.12913306057453156] | 38 | 20 | 0.024746035842440804 | True | 0.0742381075273224 | False | True | True |
| retrieval | qwen3.5-2b | NC-O | a | c | 248 | 0.375 | 0.3790322580645161 | -0.0040322580645161255 | [-0.060483869165182114, 0.052419353276491165] | 25 | 26 | 1.0 | True | 1.0 | False | False | False |
| retrieval | sarvam-1 | NC-F | c | b | 248 | 0.75 | 0.6330645161290323 | 0.11693548387096775 | [0.06451612710952759, 0.1733870953321457] | 40 | 11 | 5.703811637403078e-05 | True | 0.00022815246549612311 | True | True | False |
| retrieval | sarvam-1 | NC-O | a | c | 248 | 0.8830645161290323 | 0.75 | 0.13306451612903225 | [0.08860886842012405, 0.18145161867141724] | 36 | 3 | 3.608874976634979e-08 | True | 2.1653249859809875e-07 | True | True | False |
| retrieval | gemma4-e2b | NC-F | c | b | 248 | 0.41935483870967744 | 0.4637096774193548 | -0.04435483870967738 | [-0.10483870655298233, 0.016129031777381897] | 23 | 34 | 0.18485048241641844 | True | 0.3697009648328369 | False | False | False |
| retrieval | gemma4-e2b | NC-O | a | c | 248 | 0.5725806451612904 | 0.41935483870967744 | 0.15322580645161293 | [0.10080645233392715, 0.20564515888690948] | 46 | 8 | 1.38433549734529e-07 | True | 6.921677486726451e-07 | True | True | False |
| sentiment | qwen2.5-1.5b | NC-F | c | b | 200 | 0.485 | 0.51 | -0.025000000000000022 | [-0.05000000074505806, -0.004999999888241291] | 0 | 5 | 0.0625 | False |  | False | True | False |
| sentiment | qwen2.5-1.5b | NC-O | a | c | 200 | 0.5 | 0.485 | 0.015000000000000013 | [-0.004999999888241291, 0.03999999910593033] | 4 | 1 | 0.375 | False |  | False | False | False |
| sentiment | qwen3.5-2b | NC-F | c | b | 200 | 0.575 | 0.59 | -0.015000000000000013 | [-0.07000000029802322, 0.03999999910593033] | 15 | 18 | 0.7283324808813632 | True | 1.0 | False | False | False |
| sentiment | qwen3.5-2b | NC-O | a | c | 200 | 0.68 | 0.575 | 0.1050000000000001 | [0.04500000178813934, 0.16500000655651093] | 31 | 10 | 0.0014504910141113214 | True | 0.01015343709877925 | True | True | False |
| sentiment | sarvam-1 | NC-F | c | b | 200 | 0.74 | 0.795 | -0.05500000000000005 | [-0.125, 0.014999999664723873] | 18 | 29 | 0.14386508844054896 | True | 0.7193254422027449 | False | False | False |
| sentiment | sarvam-1 | NC-O | a | c | 200 | 0.895 | 0.74 | 0.15500000000000003 | [0.0949999988079071, 0.2199999988079071] | 39 | 8 | 5.539621596994947e-06 | True | 4.431697277595958e-05 | True | True | False |
| sentiment | gemma4-e2b | NC-F | c | b | 200 | 0.735 | 0.75 | -0.015000000000000013 | [-0.06499999761581421, 0.03500000014901161] | 12 | 15 | 0.7011080384254456 | True | 1.0 | False | False | False |
| sentiment | gemma4-e2b | NC-O | a | c | 200 | 0.79 | 0.735 | 0.05500000000000005 | [0.004999999888241291, 0.10000000149011612] | 18 | 7 | 0.043285250663757324 | True | 0.25971150398254395 | False | True | True |
| sentiment | qwen3-1.7b | NC-F | c | b | 200 | 0.6 | 0.555 | 0.04499999999999993 | [-0.029999999329447746, 0.11999999731779099] | 35 | 26 | 0.30567741986311836 | True | 1.0 | False | False | False |
| sentiment | qwen3-1.7b | NC-O | a | c | 200 | 0.57 | 0.6 | -0.030000000000000027 | [-0.10000000149011612, 0.03999999910593033] | 23 | 29 | 0.48845566937989204 | True | 1.0 | False | False | False |
| xnli_reported_only | qwen2.5-1.5b | NC-F | c | b | 200 | 0.365 | 0.38 | -0.015000000000000013 | [-0.05999999865889549, 0.029999999329447746] | 8 | 11 | 0.6476058959960938 | False |  | False | False | False |
| xnli_reported_only | qwen2.5-1.5b | NC-O | a | c | 200 | 0.325 | 0.365 | -0.03999999999999998 | [-0.08500000089406967, 0.004999999888241291] | 6 | 14 | 0.11531829833984375 | False |  | False | False | False |
| xnli_reported_only | qwen3.5-2b | NC-F | c | b | 200 | 0.335 | 0.34 | -0.0050000000000000044 | [-0.014999999664723873, 0.0] | 0 | 1 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen3.5-2b | NC-O | a | c | 200 | 0.335 | 0.335 | 0.0 | [0.0, 0.0] | 0 | 0 | 1.0 | False |  | False | False | False |
| xnli_reported_only | sarvam-1 | NC-F | c | b | 200 | 0.365 | 0.39 | -0.025000000000000022 | [-0.07999999821186066, 0.03500000014901161] | 15 | 20 | 0.4995598332025112 | False |  | False | False | False |
| xnli_reported_only | sarvam-1 | NC-O | a | c | 200 | 0.47 | 0.365 | 0.10499999999999998 | [0.03999999910593033, 0.17000000178813934] | 33 | 12 | 0.002458900322096724 | False |  | False | True | False |
| xnli_reported_only | gemma4-e2b | NC-F | c | b | 200 | 0.39 | 0.4 | -0.010000000000000009 | [-0.04500000178813934, 0.02500000037252903] | 5 | 7 | 0.7744140625 | False |  | False | False | False |
| xnli_reported_only | gemma4-e2b | NC-O | a | c | 200 | 0.4 | 0.39 | 0.010000000000000009 | [-0.029999999329447746, 0.05000000074505806] | 9 | 7 | 0.803619384765625 | False |  | False | False | False |
| xnli_reported_only | qwen3-1.7b | NC-F | c | b | 200 | 0.33 | 0.33 | 0.0 | [-0.02500000037252903, 0.02500000037252903] | 3 | 3 | 1.0 | False |  | False | False | False |
| xnli_reported_only | qwen3-1.7b | NC-O | a | c | 200 | 0.335 | 0.33 | 0.0050000000000000044 | [-0.009999999776482582, 0.019999999552965164] | 2 | 1 | 1.0 | False |  | False | False | False |
| sib | qwen2.5-1.5b | NC-F | c | b | 1004 | 0.33266932270916333 | 0.3426294820717131 | -0.009960159362549792 | [-0.0348854586482048, 0.014940239489078522] | 81 | 91 | 0.4926722176485527 | False |  | False | False | False |
| sib | qwen2.5-1.5b | NC-O | a | c | 1004 | 0.3665338645418327 | 0.33266932270916333 | 0.03386454183266935 | [0.008964143693447113, 0.05779382586479187] | 99 | 65 | 0.009756084718005844 | False |  | False | True | False |
| sib | qwen3.5-2b | NC-F | c | b | 1004 | 0.3107569721115538 | 0.2948207171314741 | 0.015936254980079667 | [-0.009960159659385681, 0.04282868653535843] | 96 | 80 | 0.25813376128396426 | True | 0.7744012838518928 | False | False | False |
| sib | qwen3.5-2b | NC-O | a | c | 1004 | 0.3754980079681275 | 0.3107569721115538 | 0.0647410358565737 | [0.039840638637542725, 0.08964143693447113] | 117 | 52 | 6.272187854845746e-07 | True | 3.7633127129074476e-06 | True | True | False |
| sib | sarvam-1 | NC-F | c | b | 1004 | 0.5348605577689243 | 0.47808764940239046 | 0.056772908366533814 | [0.027888447046279907, 0.08366534113883972] | 134 | 77 | 0.00010581242072765762 | True | 0.0005290621036382881 | True | True | False |
| sib | sarvam-1 | NC-O | a | c | 1004 | 0.7051792828685259 | 0.5348605577689243 | 0.17031872509960166 | [0.1404382437467575, 0.20119522511959076] | 222 | 51 | 1.3151471164170837e-26 | True | 1.052117693133667e-25 | True | True | False |
| sib | gemma4-e2b | NC-F | c | b | 1004 | 0.42330677290836655 | 0.45119521912350596 | -0.027888446215139417 | [-0.054780878126621246, -0.0009960159659385681] | 83 | 111 | 0.052283117673361953 | True | 0.20913247069344781 | False | True | True |
| sib | gemma4-e2b | NC-O | a | c | 1004 | 0.49701195219123506 | 0.42330677290836655 | 0.07370517928286852 | [0.04780876636505127, 0.09960159659385681] | 133 | 59 | 9.662849171339736e-08 | True | 6.763994419937815e-07 | True | True | False |
| sib | qwen3-1.7b | NC-F | c | b | 1004 | 0.30378486055776893 | 0.29780876494023906 | 0.005976095617529875 | [-0.017928287386894226, 0.029880478978157043] | 78 | 72 | 0.6832317601040961 | True | 1.0 | False | False | False |
| sib | qwen3-1.7b | NC-O | a | c | 1004 | 0.30677290836653387 | 0.30378486055776893 | 0.0029880478087649376 | [-0.019920319318771362, 0.02689243108034134] | 73 | 70 | 0.8672499070976049 | True | 1.0 | False | False | False |

#### `results/nc1/piece_frequency.csv` (5,189 bytes; first commit 0221b44 2026-10-22 20:27:55 +0530)

| model | dataset | condition | n_items | n_pieces | mean_log_freq | median_log_freq | share_unseen |
|---|---|---|---|---|---|---|---|
| qwen2.5-1.5b | m4c496 | a | 496 | 27873 | 6.184841119205768 | 6.48768401848461 | 0.0 |
| qwen2.5-1.5b | m4c496 | b | 496 | 34426 | 5.24159078239555 | 5.517452896464707 | 0.035031662115842674 |
| qwen2.5-1.5b | m4c496 | c | 496 | 27873 | 4.687623320417655 | 4.919980925828125 | 0.053384996232913574 |
| qwen2.5-1.5b | sentiment | a | 200 | 12174 | 6.139305508483198 | 6.587550014824796 | 0.015196320026285527 |
| qwen2.5-1.5b | sentiment | b | 200 | 14989 | 5.139825335958582 | 5.517452896464707 | 0.04623390486356661 |
| qwen2.5-1.5b | sentiment | c | 200 | 12174 | 4.536152268488863 | 4.855921334140644 | 0.06711023492689339 |
| qwen2.5-1.5b | xnli | a | 200 | 14301 | 5.949093203511099 | 6.302618975744905 | 0.02685126914201804 |
| qwen2.5-1.5b | xnli | b | 200 | 17356 | 5.013349151619226 | 5.407171771460119 | 0.06078589536759622 |
| qwen2.5-1.5b | xnli | c | 200 | 14301 | 4.479672679165852 | 4.787491742782046 | 0.0785259772043913 |
| qwen2.5-1.5b | sib | a | 1004 | 56668 | 6.001762413607338 | 6.336825731146441 | 0.017646643608385686 |
| qwen2.5-1.5b | sib | b | 1004 | 70279 | 5.118986740914825 | 5.4510384535657 | 0.05004339845473043 |
| qwen2.5-1.5b | sib | c | 1004 | 56668 | 4.532500925893854 | 4.836281906951478 | 0.07081598080045175 |
| qwen3.5-2b | m4c496 | a | 496 | 26094 | 5.874572219878453 | 6.035481432524756 | 0.0 |
| qwen3.5-2b | m4c496 | b | 496 | 32965 | 4.9773337543344915 | 5.267858159063328 | 0.052783254967389656 |
| qwen3.5-2b | m4c496 | c | 496 | 26094 | 4.4069600375289575 | 4.574710978503383 | 0.080018395033341 |
| qwen3.5-2b | sentiment | a | 200 | 11422 | 5.964401915859579 | 6.113682179832232 | 0.0006128523901243215 |
| qwen3.5-2b | sentiment | b | 200 | 14302 | 4.93482821003666 | 5.212210955225204 | 0.05390854425954412 |
| qwen3.5-2b | sentiment | c | 200 | 11422 | 4.3861482920947275 | 4.574710978503383 | 0.07686919978987918 |
| qwen3.5-2b | xnli | a | 200 | 13454 | 5.887371765316104 | 6.008813185442595 | 0.0002973093503790694 |
| qwen3.5-2b | xnli | b | 200 | 16640 | 4.921662664984302 | 5.214935757608986 | 0.05564903846153846 |
| qwen3.5-2b | xnli | c | 200 | 13454 | 4.341489976809201 | 4.454347296253507 | 0.08488181953322432 |
| qwen3.5-2b | sib | a | 1004 | 53084 | 5.852167431821965 | 6.003887067106539 | 0.0003390852234194861 |
| qwen3.5-2b | sib | b | 1004 | 67429 | 4.973679239570041 | 5.247024072160486 | 0.05247000548725326 |
| qwen3.5-2b | sib | c | 1004 | 53084 | 4.376164200703969 | 4.532599493153256 | 0.07947780875593399 |
| sarvam-1 | m4c496 | a | 496 | 33978 | 7.09284235222867 | 7.31455283232408 | 0.0 |
| sarvam-1 | m4c496 | b | 496 | 41951 | 6.574414598395966 | 6.911747300251674 | 0.004290720125861124 |
| sarvam-1 | m4c496 | c | 496 | 33978 | 6.149431008797158 | 6.363028103540465 | 0.005827300017658485 |
| sarvam-1 | sentiment | a | 200 | 14864 | 7.1591014762965175 | 7.398174092970465 | 0.0 |
| sarvam-1 | sentiment | b | 200 | 18122 | 6.595576851835534 | 6.931471805599453 | 0.003862708310341022 |
| sarvam-1 | sentiment | c | 200 | 14864 | 6.155605880673519 | 6.261491684321042 | 0.006054897739504844 |
| sarvam-1 | xnli | a | 200 | 17429 | 7.106940181335313 | 7.3395376954076745 | 0.0 |
| sarvam-1 | xnli | b | 200 | 21428 | 6.581076874928463 | 6.911747300251674 | 0.005600149337315662 |
| sarvam-1 | xnli | c | 200 | 17429 | 6.137829761802802 | 6.257667587882639 | 0.006598198404957255 |
| sarvam-1 | sib | a | 1004 | 69152 | 7.0606438627933175 | 7.259819610363186 | 0.0 |
| sarvam-1 | sib | b | 1004 | 85430 | 6.5499448547356405 | 6.900730664045173 | 0.0043778532131569705 |
| sarvam-1 | sib | c | 1004 | 69152 | 6.121034246738609 | 6.295266001439646 | 0.005552984729291994 |
| gemma4-e2b | m4c496 | a | 496 | 25064 | 5.660072687254529 | 5.8522024797744745 | 0.0 |
| gemma4-e2b | m4c496 | b | 496 | 32383 | 4.742251428589283 | 5.170483995038151 | 0.06633109965105148 |
| gemma4-e2b | m4c496 | c | 496 | 25064 | 4.170134289138848 | 4.3694478524670215 | 0.10233801468241302 |
| gemma4-e2b | sentiment | a | 200 | 10974 | 5.768062315265622 | 5.955837369464831 | 0.0010934937124111536 |
| gemma4-e2b | sentiment | b | 200 | 14165 | 4.708380348561383 | 5.159055299214529 | 0.06734909989410519 |
| gemma4-e2b | sentiment | c | 200 | 10974 | 4.136437937742569 | 4.30406509320417 | 0.1006925460178604 |
| gemma4-e2b | xnli | a | 200 | 12869 | 5.678202430003347 | 5.8522024797744745 | 0.00038853057735643794 |
| gemma4-e2b | xnli | b | 200 | 16397 | 4.707426286498088 | 5.159055299214529 | 0.06989083368908947 |
| gemma4-e2b | xnli | c | 200 | 12869 | 4.1485473317084836 | 4.343805421853684 | 0.10568031704095113 |
| gemma4-e2b | sib | a | 1004 | 50875 | 5.634065236622422 | 5.802118375377063 | 0.0004127764127764128 |
| gemma4-e2b | sib | b | 1004 | 66107 | 4.732705984752607 | 5.159055299214529 | 0.06536372850076391 |
| gemma4-e2b | sib | c | 1004 | 50875 | 4.153701088625521 | 4.330733340286331 | 0.1039017199017199 |
| qwen3-1.7b | m4c496 | a | 496 | 27873 | 6.184841119205768 | 6.48768401848461 | 0.0 |
| qwen3-1.7b | m4c496 | b | 496 | 34426 | 5.223543670556153 | 5.517452896464707 | 0.03686167431592401 |
| qwen3-1.7b | m4c496 | c | 496 | 27873 | 4.709903340705831 | 4.9344739331306915 | 0.052595701933771034 |
| qwen3-1.7b | sentiment | a | 200 | 12174 | 6.139305508483198 | 6.587550014824796 | 0.015196320026285527 |
| qwen3-1.7b | sentiment | b | 200 | 14989 | 5.146567884602032 | 5.5053315359323625 | 0.04670091400360264 |
| qwen3-1.7b | sentiment | c | 200 | 12174 | 4.55864545109614 | 4.859812404361672 | 0.06423525546246098 |
| qwen3-1.7b | xnli | a | 200 | 14301 | 5.949093203511099 | 6.302618975744905 | 0.02685126914201804 |
| qwen3-1.7b | xnli | b | 200 | 17356 | 5.010562041562157 | 5.402677381872279 | 0.060670661442728736 |
| qwen3-1.7b | xnli | c | 200 | 14301 | 4.461617253041583 | 4.727387818712341 | 0.08244178728760226 |
| qwen3-1.7b | sib | a | 1004 | 56668 | 6.001762413607338 | 6.336825731146441 | 0.017646643608385686 |
| qwen3-1.7b | sib | b | 1004 | 70279 | 5.108656023023475 | 5.4510384535657 | 0.04950269639579391 |
| qwen3-1.7b | sib | c | 1004 | 56668 | 4.547606278753583 | 4.844187086458591 | 0.06774546481259265 |

#### `results/nc1/piece_frequency_provenance.json` (437 bytes; first commit 0221b44 2026-10-22 20:27:55 +0530)

`````text
provenance.config.status = "post hoc descriptive, 2026-10-22, no verdict"
provenance.config.log = "natural log of (count + 1)"
provenance.git_commit = "16f9e0f3880d2b716c5bc79932ccac0e7df59eda"
provenance.timestamp_utc = "2026-10-22T14:57:18+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/nc1_piece_frequency.py"]
reference_texts = 5622
`````

#### `results/nc1/pilot.json` (4,684 bytes; first commit 5127d0d 2026-10-22 18:17:44 +0530)

`````text
provenance.config.status = "pilot, no accuracy or retrieval computed"
provenance.config.n = 20
provenance.config.model = "gemma4-e2b"
provenance.git_commit = "f676f15a822da091a9032f0c46c7d3fa6719323e"
provenance.timestamp_utc = "2026-10-22T12:47:15+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/nc1.py", "pilot"]
model = "gemma4-e2b"
load_s = 17.98546814918518
sentiment_build_s = 0.1658163070678711
sentiment_check2.b_hits_target = 20
sentiment_check2.c_equals_canonical = 20
sentiment_check2.b_minus_target = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sentiment_check2.n = 20
sentiment_check1_decode_identical.a = 20
sentiment_check1_decode_identical.b = 20
sentiment_check1_decode_identical.c = 20
sentiment_summary.a.span_tokens = 1159
sentiment_summary.a.tokens_per_word = 3.274011299435028
sentiment_summary.a.median_token_id = 6244.0
sentiment_summary.a.mean_piece_chars = 2.908541846419327
sentiment_summary.b.span_tokens = 1453
sentiment_summary.b.tokens_per_word = 4.104519774011299
sentiment_summary.b.median_token_id = 27055.0
sentiment_summary.b.mean_piece_chars = 2.320027529249828
sentiment_summary.c.span_tokens = 1159
sentiment_summary.c.tokens_per_word = 3.274011299435028
sentiment_summary.c.median_token_id = 14252.0
sentiment_summary.c.mean_piece_chars = 2.908541846419327
sentiment_summary.words.n = 354
sentiment_summary.words.multi_token = 333
sentiment_summary.words.resplit_b_only = 37
sentiment_summary.words.resplit_c_only = 0
sentiment_summary.words.resplit_both = 292
sentiment_summary.words.c_resplit_share_of_multi_token = 0.8768768768768769
sentiment_summary.words.unit_flags_b.infeasible_k = 0
sentiment_summary.words.unit_flags_b.canonical_unique = 17
sentiment_summary.words.unit_flags_b.atomic_token = 0
sentiment_summary.words.unit_flags_c.infeasible_k = 0
sentiment_summary.words.unit_flags_c.canonical_unique = 24
sentiment_summary.words.unit_flags_c.atomic_token = 0
sentiment_tokens_per_word_lower_target = 4.104519774011299
sentiment_check4.same_raw_prediction = 20
sentiment_check4.n = 20
sentiment_check4.max_abs_dlogprob = 0.0
sentiment_seconds_per_item.a = 0.2791321396827698
sentiment_seconds_per_item.b = 0.23996233940124512
sentiment_seconds_per_item.c = 0.2288636803627014
sentiment_seconds_per_item.standard_path = 0.23692641258239747
m4c_check1_decode_identical.a = 20
m4c_check1_decode_identical.b = 20
m4c_check1_decode_identical.c = 20
m4c_check1_canonical_decode_identical = 20
m4c_check2.b_hits_target = 20
m4c_check2.c_equals_canonical = 20
m4c_check2.b_minus_target = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
m4c_check2.n = 20
m4c_summary.a.span_tokens = 1113
m4c_summary.a.tokens_per_word = 3.091666666666667
m4c_summary.a.median_token_id = 6244.0
m4c_summary.a.mean_piece_chars = 2.802336028751123
m4c_summary.b.span_tokens = 1437
m4c_summary.b.tokens_per_word = 3.9916666666666667
m4c_summary.b.median_token_id = 51405.0
m4c_summary.b.mean_piece_chars = 2.1704940848990955
m4c_summary.c.span_tokens = 1113
m4c_summary.c.tokens_per_word = 3.091666666666667
m4c_summary.c.median_token_id = 31012.0
m4c_summary.c.mean_piece_chars = 2.802336028751123
m4c_summary.words.n = 360
m4c_summary.words.multi_token = 330
m4c_summary.words.resplit_b_only = 47
m4c_summary.words.resplit_c_only = 0
m4c_summary.words.resplit_both = 262
m4c_summary.words.c_resplit_share_of_multi_token = 0.793939393939394
m4c_summary.words.unit_flags_b.infeasible_k = 0
m4c_summary.words.unit_flags_b.canonical_unique = 37
m4c_summary.words.unit_flags_b.atomic_token = 0
m4c_summary.words.unit_flags_c.infeasible_k = 0
m4c_summary.words.unit_flags_c.canonical_unique = 31
m4c_summary.words.unit_flags_c.atomic_token = 0
m4c_tokens_per_word_lower_target = 3.9916666666666667
m4c_check4_canonical_vs_stored_vectors.max_rel_abs_diff = 0.0
m4c_check4_canonical_vs_stored_vectors.n = 20
m4c_seconds_per_sentence.a = 0.20280399322509765
m4c_seconds_per_sentence.b = 0.11738026142120361
m4c_seconds_per_sentence.c = 0.11466028690338134
estimate.forced_over_standard_time_ratio = 1.0523072702817855
estimate.scoring_s_per_model_3_conditions.qwen2.5-1.5b = 1360.1902818693316
estimate.scoring_s_per_model_3_conditions.qwen3.5-2b = 3014.7697110429685
estimate.scoring_s_per_model_3_conditions.sarvam-1 = 1898.545972549046
estimate.scoring_s_per_model_3_conditions.gemma4-e2b = 2568.821653525404
estimate.scoring_s_per_model_3_conditions.qwen3-1.7b = 1240.7970617343622
estimate.scoring_total_h = 2.8008679668669756
estimate.forward_total_min_using_gemma_rate = 14.494818051656088
estimate.basis = "ladder lower-form scoring seconds (E0b sentiment+xnli, E0c sib) x forced/standard ratio measured here x 3 conditions; forward at Gemma's measured rate"
`````

#### `results/nc1/retrieval.csv` (1,024 bytes; first commit a00f2ff 2026-10-22 23:16:03 +0530)

| model | condition | n_test | unmapped_test | unmapped_test_ci | unmapped_layer |
|---|---|---|---|---|---|
| qwen2.5-1.5b | a | 248 | 0.20161290322580644 | [0.15322580933570862, 0.2540322542190552] | 1 |
| qwen2.5-1.5b | b | 248 | 0.14112903225806453 | [0.09677419066429138, 0.1854838728904724] | 1 |
| qwen2.5-1.5b | c | 248 | 0.18548387096774194 | [0.13709677755832672, 0.2338709682226181] | 1 |
| qwen3.5-2b | a | 248 | 0.375 | [0.3145161271095276, 0.4354838728904724] | 7 |
| qwen3.5-2b | b | 248 | 0.3064516129032258 | [0.25, 0.3629032373428345] | 7 |
| qwen3.5-2b | c | 248 | 0.3790322580645161 | [0.31854838132858276, 0.4395161271095276] | 6 |
| sarvam-1 | a | 248 | 0.8830645161290323 | [0.8427419066429138, 0.9194556474685669] | 17 |
| sarvam-1 | b | 248 | 0.6330645161290323 | [0.5725806355476379, 0.6935483813285828] | 18 |
| sarvam-1 | c | 248 | 0.75 | [0.6935483813285828, 0.8024193644523621] | 18 |
| gemma4-e2b | a | 248 | 0.5725806451612904 | [0.5080645084381104, 0.6330645084381104] | 8 |
| gemma4-e2b | b | 248 | 0.4637096774193548 | [0.4032258093357086, 0.524193525314331] | 7 |
| gemma4-e2b | c | 248 | 0.41935483870967744 | [0.3588709533214569, 0.47983869910240173] | 8 |

#### `results/nc1/segmentation.csv` (18,671 bytes; first commit a00f2ff 2026-10-22 23:16:03 +0530)

| model | dataset | condition | n_items | span_tokens | tokens_per_word | median_token_id | mean_piece_chars | lower_rung_tokens_per_word | ratio_to_lower_rung | words_n | words_multi_token | words_resplit_b_only | words_resplit_c_only | words_resplit_both | words_c_resplit_share_of_multi_token | unit_flags_b | unit_flags_c | flags_b | b_within_2pct_of_lower | c_items_equal_canonical |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen2.5-1.5b | m4c496 | a | 496 | 27873 | 3.5634108923548964 | 877.0 | 2.6098733541420014 | 4.401176169777551 | 0.8096496833788416 | 7822 | 7450 | 797 | 0 | 6356 | 0.8531543624161074 | {"infeasible_k": 0, "canonical_unique": 498, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 596, "atomic_token": 0} | [] |  |  |
| qwen2.5-1.5b | m4c496 | b | 496 | 34426 | 4.401176169777551 | 586.0 | 2.1130831348399464 | 4.401176169777551 | 1.0 | 7822 | 7450 | 797 | 0 | 6356 | 0.8531543624161074 | {"infeasible_k": 0, "canonical_unique": 498, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 596, "atomic_token": 0} | [] | True |  |
| qwen2.5-1.5b | m4c496 | c | 496 | 27873 | 3.5634108923548964 | 5566.0 | 2.6098733541420014 | 4.401176169777551 | 0.8096496833788416 | 7822 | 7450 | 797 | 0 | 6356 | 0.8531543624161074 | {"infeasible_k": 0, "canonical_unique": 498, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 596, "atomic_token": 0} | [] |  | 496.0 |
| qwen2.5-1.5b | sentiment | a | 200 | 12174 | 3.5679953106682296 | 877.0 | 2.648923936257598 | 4.393317702227432 | 0.8121414276184122 | 3412 | 3239 | 289 | 0 | 2860 | 0.8829885767212102 | {"infeasible_k": 0, "canonical_unique": 188, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 191, "atomic_token": 0} | [] |  |  |
| qwen2.5-1.5b | sentiment | b | 200 | 14989 | 4.393024618991793 | 624.0 | 2.15144439255454 | 4.393317702227432 | 0.9999332888592395 | 3412 | 3239 | 289 | 0 | 2860 | 0.8829885767212102 | {"infeasible_k": 0, "canonical_unique": 188, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 191, "atomic_token": 0} | [] | True |  |
| qwen2.5-1.5b | sentiment | c | 200 | 12174 | 3.5679953106682296 | 5840.0 | 2.648923936257598 | 4.393317702227432 | 0.8121414276184122 | 3412 | 3239 | 289 | 0 | 2860 | 0.8829885767212102 | {"infeasible_k": 0, "canonical_unique": 188, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 191, "atomic_token": 0} | [] |  | 200.0 |
| qwen2.5-1.5b | xnli | a | 200 | 14301 | 3.555693684733963 | 848.0 | 2.649604922732676 | 4.309547488811536 | 0.8250735591069059 | 4022 | 3795 | 385 | 0 | 3244 | 0.8548089591567852 | {"infeasible_k": 0, "canonical_unique": 268, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 283, "atomic_token": 0} | ["negative_extra"] |  |  |
| qwen2.5-1.5b | xnli | b | 200 | 17356 | 4.315266036797613 | 742.0 | 2.183221940539295 | 4.309547488811536 | 1.0013269485951652 | 4022 | 3795 | 385 | 0 | 3244 | 0.8548089591567852 | {"infeasible_k": 0, "canonical_unique": 268, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 283, "atomic_token": 0} | ["negative_extra"] | True |  |
| qwen2.5-1.5b | xnli | c | 200 | 14301 | 3.555693684733963 | 5604.0 | 2.649604922732676 | 4.309547488811536 | 0.8250735591069059 | 4022 | 3795 | 385 | 0 | 3244 | 0.8548089591567852 | {"infeasible_k": 0, "canonical_unique": 268, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 283, "atomic_token": 0} | ["negative_extra"] |  | 200.0 |
| qwen2.5-1.5b | sib | a | 1004 | 56668 | 3.532917705735661 | 927.0 | 2.65850215289052 | 4.379364089775561 | 0.8067193394547655 | 16040 | 15223 | 1687 | 0 | 12848 | 0.8439860737042633 | {"infeasible_k": 0, "canonical_unique": 1140, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1235, "atomic_token": 0} | [] |  |  |
| qwen2.5-1.5b | sib | b | 1004 | 70279 | 4.381483790523691 | 624.0 | 2.1436275416554023 | 4.379364089775561 | 1.000484020214962 | 16040 | 15223 | 1687 | 0 | 12848 | 0.8439860737042633 | {"infeasible_k": 0, "canonical_unique": 1140, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1235, "atomic_token": 0} | [] | True |  |
| qwen2.5-1.5b | sib | c | 1004 | 56668 | 3.532917705735661 | 5799.0 | 2.65850215289052 | 4.379364089775561 | 0.8067193394547655 | 16040 | 15223 | 1687 | 0 | 12848 | 0.8439860737042633 | {"infeasible_k": 0, "canonical_unique": 1140, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1235, "atomic_token": 0} | [] |  | 1004.0 |
| qwen3.5-2b | m4c496 | a | 496 | 26094 | 3.3359754538481208 | 1506.0 | 2.7878056258143635 | 4.21439529532089 | 0.7915668132868193 | 7822 | 7284 | 874 | 0 | 6204 | 0.8517298187808896 | {"infeasible_k": 0, "canonical_unique": 494, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 586, "atomic_token": 0} | [] |  |  |
| qwen3.5-2b | m4c496 | b | 496 | 32965 | 4.21439529532089 | 647.0 | 2.2067344152889428 | 4.21439529532089 | 1.0 | 7822 | 7284 | 874 | 0 | 6204 | 0.8517298187808896 | {"infeasible_k": 0, "canonical_unique": 494, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 586, "atomic_token": 0} | [] | True |  |
| qwen3.5-2b | m4c496 | c | 496 | 26094 | 3.3359754538481208 | 7955.0 | 2.7878056258143635 | 4.21439529532089 | 0.7915668132868193 | 7822 | 7284 | 874 | 0 | 6204 | 0.8517298187808896 | {"infeasible_k": 0, "canonical_unique": 494, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 586, "atomic_token": 0} | [] |  | 496.0 |
| qwen3.5-2b | sentiment | a | 200 | 11422 | 3.347596717467761 | 1183.0 | 2.807564349500963 | 4.18493552168816 | 0.7999159605014357 | 3412 | 3178 | 342 | 0 | 2779 | 0.8744493392070485 | {"infeasible_k": 0, "canonical_unique": 186, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 213, "atomic_token": 0} | [] |  |  |
| qwen3.5-2b | sentiment | b | 200 | 14302 | 4.191676436107855 | 870.0 | 2.2422038875681722 | 4.18493552168816 | 1.0016107570558161 | 3412 | 3178 | 342 | 0 | 2779 | 0.8744493392070485 | {"infeasible_k": 0, "canonical_unique": 186, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 213, "atomic_token": 0} | [] | True |  |
| qwen3.5-2b | sentiment | c | 200 | 11422 | 3.347596717467761 | 7968.0 | 2.807564349500963 | 4.18493552168816 | 0.7999159605014357 | 3412 | 3178 | 342 | 0 | 2779 | 0.8744493392070485 | {"infeasible_k": 0, "canonical_unique": 186, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 213, "atomic_token": 0} | [] |  | 200.0 |
| qwen3.5-2b | xnli | a | 200 | 13454 | 3.3451019393336647 | 1214.0 | 2.787869778504534 | 4.134012928891099 | 0.8091658146388403 | 4022 | 3722 | 420 | 0 | 3237 | 0.869693713057496 | {"infeasible_k": 0, "canonical_unique": 227, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 258, "atomic_token": 0} | [] |  |  |
| qwen3.5-2b | xnli | b | 200 | 16640 | 4.137245151665838 | 926.0 | 2.2540865384615385 | 4.134012928891099 | 1.0007818608287724 | 4022 | 3722 | 420 | 0 | 3237 | 0.869693713057496 | {"infeasible_k": 0, "canonical_unique": 227, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 258, "atomic_token": 0} | [] | True |  |
| qwen3.5-2b | xnli | c | 200 | 13454 | 3.3451019393336647 | 8080.0 | 2.787869778504534 | 4.134012928891099 | 0.8091658146388403 | 4022 | 3722 | 420 | 0 | 3237 | 0.869693713057496 | {"infeasible_k": 0, "canonical_unique": 227, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 258, "atomic_token": 0} | [] |  | 200.0 |
| qwen3.5-2b | sib | a | 1004 | 53084 | 3.3094763092269326 | 1524.0 | 2.819324090121317 | 4.200561097256858 | 0.7878652952788042 | 16040 | 14924 | 1889 | 0 | 12607 | 0.8447467166979362 | {"infeasible_k": 0, "canonical_unique": 1115, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1202, "atomic_token": 0} | [] |  |  |
| qwen3.5-2b | sib | b | 1004 | 67429 | 4.203802992518703 | 682.0 | 2.2195346216019813 | 4.200561097256858 | 1.0007717767190585 | 16040 | 14924 | 1889 | 0 | 12607 | 0.8447467166979362 | {"infeasible_k": 0, "canonical_unique": 1115, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1202, "atomic_token": 0} | [] | True |  |
| qwen3.5-2b | sib | c | 1004 | 53084 | 3.3094763092269326 | 8080.0 | 2.819324090121317 | 4.200561097256858 | 0.7878652952788042 | 16040 | 14924 | 1889 | 0 | 12607 | 0.8447467166979362 | {"infeasible_k": 0, "canonical_unique": 1115, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1202, "atomic_token": 0} | [] |  | 1004.0 |
| sarvam-1 | m4c496 | a | 496 | 33978 | 4.343901815392483 | 7233.0 | 2.1584849019954087 | 5.363206341089236 | 0.8099449357583848 | 7822 | 7619 | 1091 | 0 | 6032 | 0.791704948155926 | {"infeasible_k": 0, "canonical_unique": 627, "atomic_token": 6} | {"infeasible_k": 0, "canonical_unique": 954, "atomic_token": 6} | [] |  |  |
| sarvam-1 | m4c496 | b | 496 | 41951 | 5.363206341089236 | 49839.0 | 1.7482539152821148 | 5.363206341089236 | 1.0 | 7822 | 7619 | 1091 | 0 | 6032 | 0.791704948155926 | {"infeasible_k": 0, "canonical_unique": 627, "atomic_token": 6} | {"infeasible_k": 0, "canonical_unique": 954, "atomic_token": 6} | [] | True |  |
| sarvam-1 | m4c496 | c | 496 | 33978 | 4.343901815392483 | 22207.0 | 2.1584849019954087 | 5.363206341089236 | 0.8099449357583848 | 7822 | 7619 | 1091 | 0 | 6032 | 0.791704948155926 | {"infeasible_k": 0, "canonical_unique": 627, "atomic_token": 6} | {"infeasible_k": 0, "canonical_unique": 954, "atomic_token": 6} | [] |  | 496.0 |
| sarvam-1 | sentiment | a | 200 | 14864 | 4.356389214536929 | 6618.0 | 2.157965554359526 | 5.31242672919109 | 0.8200375151715769 | 3412 | 3311 | 433 | 0 | 2701 | 0.8157656297191181 | {"infeasible_k": 0, "canonical_unique": 247, "atomic_token": 1} | {"infeasible_k": 0, "canonical_unique": 362, "atomic_token": 1} | [] |  |  |
| sarvam-1 | sentiment | b | 200 | 18122 | 5.311254396248534 | 43161.0 | 1.7700033108928375 | 5.31242672919109 | 0.9997793225201368 | 3412 | 3311 | 433 | 0 | 2701 | 0.8157656297191181 | {"infeasible_k": 0, "canonical_unique": 247, "atomic_token": 1} | {"infeasible_k": 0, "canonical_unique": 362, "atomic_token": 1} | [] | True |  |
| sarvam-1 | sentiment | c | 200 | 14864 | 4.356389214536929 | 21437.0 | 2.157965554359526 | 5.31242672919109 | 0.8200375151715769 | 3412 | 3311 | 433 | 0 | 2701 | 0.8157656297191181 | {"infeasible_k": 0, "canonical_unique": 247, "atomic_token": 1} | {"infeasible_k": 0, "canonical_unique": 362, "atomic_token": 1} | [] |  | 200.0 |
| sarvam-1 | xnli | a | 200 | 17429 | 4.333416210840378 | 6761.0 | 2.151988065867233 | 5.331178518150174 | 0.8128439511239623 | 4022 | 3893 | 571 | 0 | 3062 | 0.7865399434883124 | {"infeasible_k": 0, "canonical_unique": 330, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 501, "atomic_token": 0} | [] |  |  |
| sarvam-1 | xnli | b | 200 | 21428 | 5.327697662854301 | 49839.0 | 1.7503733432891544 | 5.331178518150174 | 0.9993470758324783 | 4022 | 3893 | 571 | 0 | 3062 | 0.7865399434883124 | {"infeasible_k": 0, "canonical_unique": 330, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 501, "atomic_token": 0} | [] | True |  |
| sarvam-1 | xnli | c | 200 | 17429 | 4.333416210840378 | 22100.0 | 2.151988065867233 | 5.331178518150174 | 0.8128439511239623 | 4022 | 3893 | 571 | 0 | 3062 | 0.7865399434883124 | {"infeasible_k": 0, "canonical_unique": 330, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 501, "atomic_token": 0} | [] |  | 200.0 |
| sarvam-1 | sib | a | 1004 | 69152 | 4.311221945137157 | 6821.0 | 2.1651579130032395 | 5.3287406483790525 | 0.8090508113673323 | 16040 | 15574 | 2237 | 0 | 12355 | 0.7933093617567741 | {"infeasible_k": 0, "canonical_unique": 1305, "atomic_token": 3} | {"infeasible_k": 0, "canonical_unique": 1911, "atomic_token": 3} | [] |  |  |
| sarvam-1 | sib | b | 1004 | 85430 | 5.326059850374065 | 48466.0 | 1.752604471497132 | 5.3287406483790525 | 0.9994969171551251 | 16040 | 15574 | 2237 | 0 | 12355 | 0.7933093617567741 | {"infeasible_k": 0, "canonical_unique": 1305, "atomic_token": 3} | {"infeasible_k": 0, "canonical_unique": 1911, "atomic_token": 3} | [] | True |  |
| sarvam-1 | sib | c | 1004 | 69152 | 4.311221945137157 | 22100.0 | 2.1651579130032395 | 5.3287406483790525 | 0.8090508113673323 | 16040 | 15574 | 2237 | 0 | 12355 | 0.7933093617567741 | {"infeasible_k": 0, "canonical_unique": 1305, "atomic_token": 3} | {"infeasible_k": 0, "canonical_unique": 1911, "atomic_token": 3} | [] |  | 1004.0 |
| gemma4-e2b | m4c496 | a | 496 | 25064 | 3.20429557657888 | 7077.0 | 2.901891158633897 | 4.139989772436717 | 0.7739863508631071 | 7822 | 7244 | 866 | 0 | 6267 | 0.8651297625621204 | {"infeasible_k": 0, "canonical_unique": 450, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 527, "atomic_token": 0} | [] |  |  |
| gemma4-e2b | m4c496 | b | 496 | 32383 | 4.139989772436717 | 36464.0 | 2.2460241484729644 | 4.139989772436717 | 1.0 | 7822 | 7244 | 866 | 0 | 6267 | 0.8651297625621204 | {"infeasible_k": 0, "canonical_unique": 450, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 527, "atomic_token": 0} | [] | True |  |
| gemma4-e2b | m4c496 | c | 496 | 25064 | 3.20429557657888 | 22401.5 | 2.901891158633897 | 4.139989772436717 | 0.7739863508631071 | 7822 | 7244 | 866 | 0 | 6267 | 0.8651297625621204 | {"infeasible_k": 0, "canonical_unique": 450, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 527, "atomic_token": 0} | [] |  | 496.0 |
| gemma4-e2b | sentiment | a | 200 | 10974 | 3.216295427901524 | 6244.0 | 2.921997448514671 | 4.146248534583822 | 0.7757121651233477 | 3412 | 3166 | 365 | 0 | 2772 | 0.8755527479469362 | {"infeasible_k": 0, "canonical_unique": 166, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 228, "atomic_token": 0} | [] |  |  |
| gemma4-e2b | sentiment | b | 200 | 14165 | 4.151524032825322 | 29406.0 | 2.2637486763148607 | 4.146248534583822 | 1.0012723545628048 | 3412 | 3166 | 365 | 0 | 2772 | 0.8755527479469362 | {"infeasible_k": 0, "canonical_unique": 166, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 228, "atomic_token": 0} | [] | True |  |
| gemma4-e2b | sentiment | c | 200 | 10974 | 3.216295427901524 | 17335.0 | 2.921997448514671 | 4.146248534583822 | 0.7757121651233477 | 3412 | 3166 | 365 | 0 | 2772 | 0.8755527479469362 | {"infeasible_k": 0, "canonical_unique": 166, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 228, "atomic_token": 0} | [] |  | 200.0 |
| gemma4-e2b | xnli | a | 200 | 12869 | 3.1996519144704125 | 6320.0 | 2.914600979097055 | 4.0790651417205375 | 0.7844081433621845 | 4022 | 3692 | 431 | 0 | 3216 | 0.8710725893824486 | {"infeasible_k": 0, "canonical_unique": 223, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 253, "atomic_token": 0} | [] |  |  |
| gemma4-e2b | xnli | b | 200 | 16397 | 4.076827449030334 | 33285.0 | 2.2874916143196926 | 4.0790651417205375 | 0.9994514202121175 | 4022 | 3692 | 431 | 0 | 3216 | 0.8710725893824486 | {"infeasible_k": 0, "canonical_unique": 223, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 253, "atomic_token": 0} | [] | True |  |
| gemma4-e2b | xnli | c | 200 | 12869 | 3.1996519144704125 | 21925.0 | 2.914600979097055 | 4.0790651417205375 | 0.7844081433621845 | 4022 | 3692 | 431 | 0 | 3216 | 0.8710725893824486 | {"infeasible_k": 0, "canonical_unique": 223, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 253, "atomic_token": 0} | [] |  | 200.0 |
| gemma4-e2b | sib | a | 1004 | 50875 | 3.1717581047381547 | 6862.0 | 2.9415036855036854 | 4.120885286783042 | 0.7696788151106674 | 16040 | 14818 | 1906 | 0 | 12658 | 0.8542313402618437 | {"infeasible_k": 0, "canonical_unique": 984, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1176, "atomic_token": 0} | [] |  |  |
| gemma4-e2b | sib | b | 1004 | 66107 | 4.121384039900249 | 34081.0 | 2.263739089657676 | 4.120885286783042 | 1.0001210305753492 | 16040 | 14818 | 1906 | 0 | 12658 | 0.8542313402618437 | {"infeasible_k": 0, "canonical_unique": 984, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1176, "atomic_token": 0} | [] | True |  |
| gemma4-e2b | sib | c | 1004 | 50875 | 3.1717581047381547 | 23837.0 | 2.9415036855036854 | 4.120885286783042 | 0.7696788151106674 | 16040 | 14818 | 1906 | 0 | 12658 | 0.8542313402618437 | {"infeasible_k": 0, "canonical_unique": 984, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1176, "atomic_token": 0} | [] |  | 1004.0 |
| qwen3-1.7b | m4c496 | a | 496 | 27873 | 3.5634108923548964 | 877.0 | 2.6098733541420014 | 4.401176169777551 | 0.8096496833788416 | 7822 | 7450 | 777 | 0 | 6356 | 0.8531543624161074 | {"infeasible_k": 0, "canonical_unique": 512, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 582, "atomic_token": 0} | [] |  |  |
| qwen3-1.7b | m4c496 | b | 496 | 34426 | 4.401176169777551 | 595.0 | 2.1130831348399464 | 4.401176169777551 | 1.0 | 7822 | 7450 | 777 | 0 | 6356 | 0.8531543624161074 | {"infeasible_k": 0, "canonical_unique": 512, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 582, "atomic_token": 0} | [] | True |  |
| qwen3-1.7b | m4c496 | c | 496 | 27873 | 3.5634108923548964 | 5566.0 | 2.6098733541420014 | 4.401176169777551 | 0.8096496833788416 | 7822 | 7450 | 777 | 0 | 6356 | 0.8531543624161074 | {"infeasible_k": 0, "canonical_unique": 512, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 582, "atomic_token": 0} | [] |  | 496.0 |
| qwen3-1.7b | sentiment | a | 200 | 12174 | 3.5679953106682296 | 877.0 | 2.648923936257598 | 4.393317702227432 | 0.8121414276184122 | 3412 | 3239 | 290 | 0 | 2860 | 0.8829885767212102 | {"infeasible_k": 0, "canonical_unique": 190, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 189, "atomic_token": 0} | [] |  |  |
| qwen3-1.7b | sentiment | b | 200 | 14989 | 4.393024618991793 | 649.0 | 2.15144439255454 | 4.393317702227432 | 0.9999332888592395 | 3412 | 3239 | 290 | 0 | 2860 | 0.8829885767212102 | {"infeasible_k": 0, "canonical_unique": 190, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 189, "atomic_token": 0} | [] | True |  |
| qwen3-1.7b | sentiment | c | 200 | 12174 | 3.5679953106682296 | 5683.0 | 2.648923936257598 | 4.393317702227432 | 0.8121414276184122 | 3412 | 3239 | 290 | 0 | 2860 | 0.8829885767212102 | {"infeasible_k": 0, "canonical_unique": 190, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 189, "atomic_token": 0} | [] |  | 200.0 |
| qwen3-1.7b | xnli | a | 200 | 14301 | 3.555693684733963 | 848.0 | 2.649604922732676 | 4.309547488811536 | 0.8250735591069059 | 4022 | 3795 | 392 | 0 | 3244 | 0.8548089591567852 | {"infeasible_k": 0, "canonical_unique": 284, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 267, "atomic_token": 0} | ["negative_extra"] |  |  |
| qwen3-1.7b | xnli | b | 200 | 17356 | 4.315266036797613 | 742.0 | 2.183221940539295 | 4.309547488811536 | 1.0013269485951652 | 4022 | 3795 | 392 | 0 | 3244 | 0.8548089591567852 | {"infeasible_k": 0, "canonical_unique": 284, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 267, "atomic_token": 0} | ["negative_extra"] | True |  |
| qwen3-1.7b | xnli | c | 200 | 14301 | 3.555693684733963 | 5831.0 | 2.649604922732676 | 4.309547488811536 | 0.8250735591069059 | 4022 | 3795 | 392 | 0 | 3244 | 0.8548089591567852 | {"infeasible_k": 0, "canonical_unique": 284, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 267, "atomic_token": 0} | ["negative_extra"] |  | 200.0 |
| qwen3-1.7b | sib | a | 1004 | 56668 | 3.532917705735661 | 927.0 | 2.65850215289052 | 4.379364089775561 | 0.8067193394547655 | 16040 | 15223 | 1690 | 0 | 12848 | 0.8439860737042633 | {"infeasible_k": 0, "canonical_unique": 1146, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1229, "atomic_token": 0} | [] |  |  |
| qwen3-1.7b | sib | b | 1004 | 70279 | 4.381483790523691 | 624.0 | 2.1436275416554023 | 4.379364089775561 | 1.000484020214962 | 16040 | 15223 | 1690 | 0 | 12848 | 0.8439860737042633 | {"infeasible_k": 0, "canonical_unique": 1146, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1229, "atomic_token": 0} | [] | True |  |
| qwen3-1.7b | sib | c | 1004 | 56668 | 3.532917705735661 | 5566.0 | 2.65850215289052 | 4.379364089775561 | 0.8067193394547655 | 16040 | 15223 | 1690 | 0 | 12848 | 0.8439860737042633 | {"infeasible_k": 0, "canonical_unique": 1146, "atomic_token": 0} | {"infeasible_k": 0, "canonical_unique": 1229, "atomic_token": 0} | [] |  | 1004.0 |

#### `results/nc1/verdict.json` (2,424 bytes; first commit a00f2ff 2026-10-22 23:16:03 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-22 (NC1)"
provenance.config.counted_retrieval = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
provenance.config.counted_accuracy = ["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
provenance.config.m4c_split_seed = 0
provenance.git_commit = "3b1cf25dd971d286dec9ad561aca63c81607f613"
provenance.timestamp_utc = "2026-10-22T17:43:40+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/nc1.py", "analyse"]
NC-F|retrieval.verdict = "no effect detected"
NC-F|retrieval.status = "registered prediction: positive"
NC-F|retrieval.n_significant_positive = 1
NC-F|retrieval.n_significant_negative = 0
NC-F|retrieval.needed = 2
NC-F|retrieval.n_counted = 3
NC-F|retrieval.ci_holm_disagreements = ["qwen3.5-2b"]
NC-O|retrieval.verdict = "effect, positive"
NC-O|retrieval.status = "reported, no prediction"
NC-O|retrieval.n_significant_positive = 2
NC-O|retrieval.n_significant_negative = 0
NC-O|retrieval.needed = 2
NC-O|retrieval.n_counted = 3
NC-F|sentiment.verdict = "no effect detected"
NC-F|sentiment.status = "registered prediction: positive"
NC-F|sentiment.n_significant_positive = 0
NC-F|sentiment.n_significant_negative = 0
NC-F|sentiment.needed = 3
NC-F|sentiment.n_counted = 4
NC-O|sentiment.verdict = "no effect detected"
NC-O|sentiment.status = "reported, no prediction"
NC-O|sentiment.n_significant_positive = 2
NC-O|sentiment.n_significant_negative = 0
NC-O|sentiment.needed = 3
NC-O|sentiment.n_counted = 4
NC-O|sentiment.ci_holm_disagreements = ["gemma4-e2b"]
NC-F|sib.verdict = "no effect detected"
NC-F|sib.status = "registered prediction: positive"
NC-F|sib.n_significant_positive = 1
NC-F|sib.n_significant_negative = 0
NC-F|sib.needed = 3
NC-F|sib.n_counted = 4
NC-F|sib.ci_holm_disagreements = ["gemma4-e2b"]
NC-O|sib.verdict = "effect, positive"
NC-O|sib.status = "reported, no prediction"
NC-O|sib.n_significant_positive = 3
NC-O|sib.n_significant_negative = 0
NC-O|sib.needed = 3
NC-O|sib.n_counted = 4
`````

#### `results/nc1_posthoc/decomposition.csv` (3,276 bytes; first commit 40de234 2026-10-22 23:55:36 +0530)

| model | measure | score | layer | n_items | n_obs | corr_extra_dfreq | extra_pieces_coef | extra_pieces_ci_low | extra_pieces_ci_high | extra_pieces_p | extra_pieces_sd | d_ln_freq_coef | d_ln_freq_ci_low | d_ln_freq_ci_high | d_ln_freq_p | d_ln_freq_sd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3.5-2b | retrieval | cosine margin | 7.0 | 248 | 496 | 0.695740212414773 | -0.0005883136852554843 | -0.0013940842388139364 | 0.00021745686830296782 | 0.15242453404382478 | 8.326616061023609 | 8.132485411883536e-05 | -0.015355850917054851 | 0.015518500625292522 | 0.9917617326918204 | 0.47026292127912717 |
| qwen3.5-2b | sentiment | calibrated gold log-prob margin |  | 200 | 400 | 0.6275251087408417 | -0.0013024004458240793 | -0.005504753710598171 | 0.002899952818950012 | 0.5435620282826406 | 9.759771146501347 | -0.006052721663816485 | -0.1192637415807627 | 0.10715829825312972 | 0.9165443118008084 | 0.4631894269791503 |
| qwen3.5-2b | sib | calibrated gold log-prob margin |  | 1004 | 2008 | 0.7008714654538155 | -0.006051120747700404 | -0.015726664992104896 | 0.0036244234967040866 | 0.22028575071173917 | 8.325928126112 | 0.08934042609617013 | -0.09246795548520786 | 0.2711488076775481 | 0.335485293948232 | 0.494485383506449 |
| sarvam-1 | retrieval | cosine margin | 17.0 | 248 | 496 | 0.6963926059103853 | -0.0036339302252689854 | -0.005279092369701156 | -0.001988768080836815 | 1.4959565197157595e-05 | 9.699700021898908 | 0.05042671951589282 | 0.00993263203712804 | 0.0909208069946576 | 0.014658190256141351 | 0.3550344863330584 |
| sarvam-1 | sentiment | calibrated gold log-prob margin |  | 200 | 400 | 0.6173888821541325 | -4.530646082659753e-05 | -0.01986283217566019 | 0.019772219254006997 | 0.996424824159823 | 11.006217199501675 | 0.070795622285446 | -0.5597473971225789 | 0.7013386416934709 | 0.825824953844669 | 0.3380912901327661 |
| sarvam-1 | sib | calibrated gold log-prob margin |  | 1004 | 2008 | 0.7306421219018788 | -0.015420686214094845 | -0.025464620200055077 | -0.005376752228134616 | 0.00261955213521186 | 9.493007240117988 | -0.010745783932398278 | -0.3097772550827522 | 0.28828568721795567 | 0.9438499155429715 | 0.3559564425202933 |
| gemma4-e2b | retrieval | cosine margin | 8.0 | 248 | 496 | 0.652780740812897 | -0.000727493688767333 | -0.001487339303047377 | 3.235192551271076e-05 | 0.06058464458657149 | 8.948066191253274 | 0.015932318668107792 | 0.0012892932874276758 | 0.03057534404878791 | 0.03296285309528401 | 0.5205297550016613 |
| gemma4-e2b | sentiment | calibrated gold log-prob margin |  | 200 | 400 | 0.6490600264169171 | -0.04018517695549921 | -0.10043864569470985 | 0.02006829178371143 | 0.19115513500711523 | 10.70460017526487 | 1.0899907793284198 | -0.6287083412214487 | 2.8086898998782885 | 0.21386790548090184 | 0.4774401441383517 |
| gemma4-e2b | sib | calibrated gold log-prob margin |  | 1004 | 2008 | 0.6690186302153871 | -0.04634136126752941 | -0.08967682436019853 | -0.0030058981748602998 | 0.03608983021532113 | 8.82372540433442 | 1.2858413062072538 | 0.4287950487681792 | 2.1428875636463283 | 0.0032761126831559037 | 0.5122535883775042 |
| qwen3-1.7b | sentiment | calibrated gold log-prob margin |  | 200 | 400 | 0.5870732740103235 | -0.02765910993891681 | -0.04576322151445511 | -0.009554998363378506 | 0.002749897789097902 | 9.459375943109709 | 0.23817438391116272 | -0.15685701240159497 | 0.6332057802239204 | 0.237320122730996 | 0.4579596363546959 |
| qwen3-1.7b | sib | calibrated gold log-prob margin |  | 1004 | 2008 | 0.6761252449218449 | 0.04340391580658523 | -0.016922022982372692 | 0.10372985459554315 | 0.15848810859955376 | 7.993968265875864 | -0.4896261678707431 | -1.5924127950105014 | 0.6131604592690151 | 0.38418877141218466 | 0.4599091229236063 |

#### `results/nc1_posthoc/ladder_piece_familiarity.csv` (3,596 bytes; first commit 40de234 2026-10-22 23:55:36 +0530)

| model | dataset | form | n_texts | tokens_per_word | mean_ln_freq | share_unseen |
|---|---|---|---|---|---|---|
| qwen2.5-1.5b | m4c496 | itrans | 496 | 4.318205062643825 | 5.831450091685021 | 0.029517127039109452 |
| qwen2.5-1.5b | m4c496 | lower | 496 | 4.401176169777551 | 5.9973108232455825 | 0.06954046360309069 |
| qwen2.5-1.5b | m4c496 | lossy | 496 | 3.5634108923548964 | 6.7273462974795715 | 0.0073189107738671835 |
| qwen2.5-1.5b | m4c496 | natural | 496 | 3.528491477995421 | 6.639212157785647 | 0.009768934068706969 |
| qwen2.5-1.5b | sentiment | itrans | 200 | 4.22538100820633 | 5.83300422705155 | 0.031074426024831795 |
| qwen2.5-1.5b | sentiment | lower | 200 | 4.393317702227432 | 5.990942377071138 | 0.07578385590393595 |
| qwen2.5-1.5b | sentiment | lossy | 200 | 3.5679953106682296 | 6.754795510921188 | 0.007474946607524232 |
| qwen2.5-1.5b | sentiment | natural | 198 | 3.5069712251557403 | 6.627446282826358 | 0.013280324818135679 |
| qwen3.5-2b | m4c496 | itrans | 496 | 4.173612886729737 | 5.579904895366181 | 0.035808368559701036 |
| qwen3.5-2b | m4c496 | lower | 496 | 4.21439529532089 | 5.6725879777400365 | 0.08226907325951767 |
| qwen3.5-2b | m4c496 | lossy | 496 | 3.3359754538481208 | 6.380357116485486 | 0.013144784241588105 |
| qwen3.5-2b | m4c496 | natural | 496 | 3.3270160264563726 | 6.316448478331173 | 0.014451198531941736 |
| qwen3.5-2b | sentiment | itrans | 200 | 4.087631887456038 | 5.58539687146868 | 0.03656700365670037 |
| qwen3.5-2b | sentiment | lower | 200 | 4.18493552168816 | 5.627877864171845 | 0.09006232929476854 |
| qwen3.5-2b | sentiment | lossy | 200 | 3.3423212192262604 | 6.40595162211575 | 0.012977902490354262 |
| qwen3.5-2b | sentiment | natural | 198 | 3.32275289231682 | 6.3153449758689915 | 0.01821265958396572 |
| sarvam-1 | m4c496 | itrans | 496 | 5.30107389414472 | 7.124885976321649 | 0.01181719522488846 |
| sarvam-1 | m4c496 | lower | 496 | 5.363206341089236 | 7.217301736127258 | 0.011561107005792472 |
| sarvam-1 | m4c496 | lossy | 496 | 4.343901815392483 | 7.771227295397824 | 0.0005591853552298546 |
| sarvam-1 | m4c496 | natural | 496 | 4.308191299923683 | 7.691532224542397 | 0.000944761004989519 |
| sarvam-1 | sentiment | itrans | 200 | 5.238569753810082 | 7.155715895249856 | 0.008112341949199955 |
| sarvam-1 | sentiment | lower | 200 | 5.31242672919109 | 7.210813756627873 | 0.009875317223877304 |
| sarvam-1 | sentiment | lossy | 200 | 4.357561547479484 | 7.810091162610003 | 0.0006725854183481302 |
| sarvam-1 | sentiment | natural | 198 | 4.29219816078315 | 7.659366882929594 | 0.0016587186398507154 |
| gemma4-e2b | m4c496 | itrans | 496 | 4.0164919457939146 | 5.260897810460535 | 0.05092784161441258 |
| gemma4-e2b | m4c496 | lower | 496 | 4.139989772436717 | 5.315625525241347 | 0.03955779266899299 |
| gemma4-e2b | m4c496 | lossy | 496 | 3.20429557657888 | 6.111505910790003 | 0.016836897542291732 |
| gemma4-e2b | m4c496 | natural | 496 | 3.163825998473671 | 6.051560397134003 | 0.018613813620648068 |
| gemma4-e2b | sentiment | itrans | 200 | 3.943434935521688 | 5.299417558682691 | 0.04600520252694166 |
| gemma4-e2b | sentiment | lower | 200 | 4.146248534583822 | 5.29030681727534 | 0.03612073231073726 |
| gemma4-e2b | sentiment | lossy | 200 | 3.2110199296600235 | 6.167853142157426 | 0.014968966776195691 |
| gemma4-e2b | sentiment | natural | 198 | 3.1530703055473155 | 6.050168152565773 | 0.021450747953711543 |
| qwen3-1.7b | m4c496 | itrans | 496 | 4.318205062643825 | 5.831450091685021 | 0.029517127039109452 |
| qwen3-1.7b | m4c496 | lower | 496 | 4.401176169777551 | 5.9973108232455825 | 0.06954046360309069 |
| qwen3-1.7b | m4c496 | lossy | 496 | 3.5634108923548964 | 6.7273462974795715 | 0.0073189107738671835 |
| qwen3-1.7b | m4c496 | natural | 496 | 3.528491477995421 | 6.639212157785647 | 0.009768934068706969 |
| qwen3-1.7b | sentiment | itrans | 200 | 4.22538100820633 | 5.83300422705155 | 0.031074426024831795 |
| qwen3-1.7b | sentiment | lower | 200 | 4.393317702227432 | 5.990942377071138 | 0.07578385590393595 |
| qwen3-1.7b | sentiment | lossy | 200 | 3.5679953106682296 | 6.754795510921188 | 0.007474946607524232 |
| qwen3-1.7b | sentiment | natural | 198 | 3.5069712251557403 | 6.627446282826358 | 0.013280324818135679 |

#### `results/nc1_posthoc/piece_frequency_independent.csv` (5,347 bytes; first commit 40de234 2026-10-22 23:55:36 +0530)

| model | dataset | condition | n_items | n_pieces | mean_ln_freq | median_ln_freq | share_unseen |
|---|---|---|---|---|---|---|---|
| qwen2.5-1.5b | m4c496 | a | 496 | 27873 | 6.7273462974795715 | 7.175489713624222 | 0.0073189107738671835 |
| qwen2.5-1.5b | m4c496 | b | 496 | 34426 | 6.1595602918981065 | 6.361302477572996 | 0.014233428222854819 |
| qwen2.5-1.5b | m4c496 | c | 496 | 27873 | 5.5448460264079396 | 5.746203190540153 | 0.023033042729523195 |
| qwen2.5-1.5b | sentiment | a | 200 | 12174 | 6.693771459456855 | 7.146772179452637 | 0.008789222934121899 |
| qwen2.5-1.5b | sentiment | b | 200 | 14989 | 6.085385839994501 | 6.338594078203183 | 0.015144439255453999 |
| qwen2.5-1.5b | sentiment | c | 200 | 12174 | 5.422953630180723 | 5.545177444479562 | 0.0234926893379333 |
| qwen2.5-1.5b | xnli | a | 200 | 14301 | 6.601274914339293 | 7.002155954403621 | 0.007971470526536606 |
| qwen2.5-1.5b | xnli | b | 200 | 17356 | 6.038602939469268 | 6.293419278846481 | 0.01619036644388108 |
| qwen2.5-1.5b | xnli | c | 200 | 14301 | 5.438251420539594 | 5.541263545158426 | 0.025802391441157962 |
| qwen2.5-1.5b | sib | a | 1004 | 56668 | 6.602619665769299 | 7.069874128458572 | 0.007446883602738759 |
| qwen2.5-1.5b | sib | b | 1004 | 70279 | 6.092078669287095 | 6.338594078203183 | 0.014584726589735197 |
| qwen2.5-1.5b | sib | c | 1004 | 56668 | 5.440781072709856 | 5.560681631015528 | 0.024158255099880004 |
| qwen3.5-2b | m4c496 | a | 496 | 26094 | 6.380357116485486 | 6.807934943699926 | 0.013144784241588105 |
| qwen3.5-2b | m4c496 | b | 496 | 32965 | 5.874351165330531 | 6.113682179832232 | 0.027210677991809495 |
| qwen3.5-2b | m4c496 | c | 496 | 26094 | 5.198475585201896 | 5.351858133476067 | 0.04387981911550548 |
| qwen3.5-2b | sentiment | a | 200 | 11422 | 6.422315077411337 | 6.825460036255307 | 0.012694799509718089 |
| qwen3.5-2b | sentiment | b | 200 | 14302 | 5.822141522677393 | 6.061456918928017 | 0.026709551111732625 |
| qwen3.5-2b | sentiment | c | 200 | 11422 | 5.152350584592767 | 5.288267030694535 | 0.04360007004027316 |
| qwen3.5-2b | xnli | a | 200 | 13454 | 6.38947764404165 | 6.741700694652055 | 0.013081611416679054 |
| qwen3.5-2b | xnli | b | 200 | 16640 | 5.829239723395716 | 6.113682179832232 | 0.029146634615384616 |
| qwen3.5-2b | xnli | c | 200 | 13454 | 5.160980328963837 | 5.308267697401205 | 0.04846142411178832 |
| qwen3.5-2b | sib | a | 1004 | 53084 | 6.3344186278446495 | 6.738152494595957 | 0.013940170296134428 |
| qwen3.5-2b | sib | b | 1004 | 67429 | 5.86945173876871 | 6.113682179832232 | 0.027347283809636802 |
| qwen3.5-2b | sib | c | 1004 | 53084 | 5.145475028990688 | 5.313205979041787 | 0.04781101650214754 |
| sarvam-1 | m4c496 | a | 496 | 33978 | 7.771227295397824 | 7.945201132412759 | 0.0005591853552298546 |
| sarvam-1 | m4c496 | b | 496 | 41951 | 7.549147997140204 | 7.7102051944325325 | 0.0012395413696932136 |
| sarvam-1 | m4c496 | c | 496 | 33978 | 7.037953914186451 | 7.330405211844402 | 0.0019130025310495026 |
| sarvam-1 | sentiment | a | 200 | 14864 | 7.809760530162289 | 7.982074875081202 | 0.0006727664155005383 |
| sarvam-1 | sentiment | b | 200 | 18122 | 7.546438557538682 | 7.726212650507529 | 0.0011588124931023065 |
| sarvam-1 | sentiment | c | 200 | 14864 | 7.029062882620667 | 7.293017679772782 | 0.002556512378902045 |
| sarvam-1 | xnli | a | 200 | 17429 | 7.790348296455574 | 7.982074875081202 | 0.0004016294681278329 |
| sarvam-1 | xnli | b | 200 | 21428 | 7.548956682789683 | 7.726212650507529 | 0.0013533694231846183 |
| sarvam-1 | xnli | c | 200 | 17429 | 7.021038949026424 | 7.293017679772782 | 0.002295025532159045 |
| sarvam-1 | sib | a | 1004 | 69152 | 7.734609728477998 | 7.923710333969238 | 0.0006218186024988431 |
| sarvam-1 | sib | b | 1004 | 85430 | 7.52841929520529 | 7.703459047867175 | 0.0014397752545944047 |
| sarvam-1 | sib | c | 1004 | 69152 | 7.007573275629077 | 7.305860032684009 | 0.0018799167052290606 |
| gemma4-e2b | m4c496 | a | 496 | 25064 | 6.111505910790003 | 6.499787040655854 | 0.016836897542291732 |
| gemma4-e2b | m4c496 | b | 496 | 32383 | 5.636763644794931 | 6.025865973825314 | 0.03168329061544638 |
| gemma4-e2b | m4c496 | c | 496 | 25064 | 4.940107453954374 | 5.030437921392435 | 0.05422119374401532 |
| gemma4-e2b | sentiment | a | 200 | 10974 | 6.18322540201794 | 6.536691597591305 | 0.015126663021687626 |
| gemma4-e2b | sentiment | b | 200 | 14165 | 5.60067795216212 | 5.940171252720432 | 0.029650547123190964 |
| gemma4-e2b | sentiment | c | 200 | 10974 | 4.889100123445306 | 5.0238805208462765 | 0.049298341534536175 |
| gemma4-e2b | xnli | a | 200 | 12869 | 6.142567228897338 | 6.48768401848461 | 0.015929753671613957 |
| gemma4-e2b | xnli | b | 200 | 16397 | 5.592822227653755 | 5.877735781779639 | 0.03299384033664695 |
| gemma4-e2b | xnli | c | 200 | 12869 | 4.911085049930787 | 5.0238805208462765 | 0.05975600279742016 |
| gemma4-e2b | sib | a | 1004 | 50875 | 6.054330026300573 | 6.424869023905388 | 0.017945945945945944 |
| gemma4-e2b | sib | b | 1004 | 66107 | 5.618984497689755 | 5.998936561946683 | 0.031993586155777756 |
| gemma4-e2b | sib | c | 1004 | 50875 | 4.889221870921447 | 5.030437921392435 | 0.05751351351351351 |
| qwen3-1.7b | m4c496 | a | 496 | 27873 | 6.7273462974795715 | 7.175489713624222 | 0.0073189107738671835 |
| qwen3-1.7b | m4c496 | b | 496 | 34426 | 6.141056085258985 | 6.361302477572996 | 0.014175332597455412 |
| qwen3-1.7b | m4c496 | c | 496 | 27873 | 5.554422722574233 | 5.746203190540153 | 0.0233200588383023 |
| qwen3-1.7b | sentiment | a | 200 | 12174 | 6.693771459456855 | 7.146772179452637 | 0.008789222934121899 |
| qwen3-1.7b | sentiment | b | 200 | 14989 | 6.10936509261007 | 6.338594078203183 | 0.014143705383948229 |
| qwen3-1.7b | sentiment | c | 200 | 12174 | 5.451339753205959 | 5.5797227059640075 | 0.022014128470510926 |
| qwen3-1.7b | xnli | a | 200 | 14301 | 6.601274914339293 | 7.002155954403621 | 0.007971470526536606 |
| qwen3-1.7b | xnli | b | 200 | 17356 | 6.030857598733234 | 6.293419278846481 | 0.0163632173311823 |
| qwen3-1.7b | xnli | c | 200 | 14301 | 5.434465792760651 | 5.541263545158426 | 0.025732466261100623 |
| qwen3-1.7b | sib | a | 1004 | 56668 | 6.602619665769299 | 7.069874128458572 | 0.007446883602738759 |
| qwen3-1.7b | sib | b | 1004 | 70279 | 6.0892689453053865 | 6.338594078203183 | 0.014613184592837121 |
| qwen3-1.7b | sib | c | 1004 | 56668 | 5.447718510694639 | 5.560681631015528 | 0.023628855791628434 |

#### `results/nc1_posthoc/reference.json` (1,056 bytes; first commit 40de234 2026-10-22 23:55:36 +0530)

`````text
provenance.config.status = "post hoc descriptive, 2026-10-22, no verdict"
provenance.config.log = "natural log of (count + 1)"
provenance.config.min_overlap_chars = 20
provenance.git_commit = "bb9fd5b47fcc58bc9d1e90ff763596d6c45a99d3-dirty"
provenance.timestamp_utc = "2026-10-22T19:08:33+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/nc1_posthoc.py"]
dakshina_sentences_total = 10000
dakshina_dropped_overlap = 0
dakshina_sentences = 10000
dakshina_chars = 1108579
dakshina_words = 111105
dakshina_uppercase_char_share = 0.01676921536489506
english_articles = 255
english_chars = 1109371
english_articles_skipped_overlap = 0
english_source = "wikimedia/wikipedia 20231101.en shard 0 (local), seed-0 shuffle"
reference_tokens_qwen2.5-1.5b = 681740
reference_tokens_qwen3.5-2b = 662593
reference_tokens_sarvam-1 = 828554
reference_tokens_gemma4-e2b = 636786
reference_tokens_qwen3-1.7b = 681740
`````

## Not dumped (item-level, binary or too large; path and size only)

- `results/nc1/scores/gemma4-e2b__nc_a__e0b.parquet`: .parquet file, 16,640 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/gemma4-e2b__nc_a__e0c.parquet`: .parquet file, 66,137 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/gemma4-e2b__nc_b__e0b.parquet`: .parquet file, 16,769 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/gemma4-e2b__nc_b__e0c.parquet`: .parquet file, 66,201 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/gemma4-e2b__nc_c__e0b.parquet`: .parquet file, 16,571 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/gemma4-e2b__nc_c__e0c.parquet`: .parquet file, 66,121 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen2.5-1.5b__nc_a__e0b.parquet`: .parquet file, 16,552 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen2.5-1.5b__nc_a__e0c.parquet`: .parquet file, 64,506 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen2.5-1.5b__nc_b__e0b.parquet`: .parquet file, 16,650 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen2.5-1.5b__nc_b__e0c.parquet`: .parquet file, 64,621 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen2.5-1.5b__nc_c__e0b.parquet`: .parquet file, 16,491 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen2.5-1.5b__nc_c__e0c.parquet`: .parquet file, 64,556 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3-1.7b__nc_a__e0b.parquet`: .parquet file, 16,604 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3-1.7b__nc_a__e0c.parquet`: .parquet file, 65,807 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3-1.7b__nc_b__e0b.parquet`: .parquet file, 16,708 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3-1.7b__nc_b__e0c.parquet`: .parquet file, 65,936 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3-1.7b__nc_c__e0b.parquet`: .parquet file, 16,595 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3-1.7b__nc_c__e0c.parquet`: .parquet file, 65,839 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3.5-2b__nc_a__e0b.parquet`: .parquet file, 16,435 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3.5-2b__nc_a__e0c.parquet`: .parquet file, 64,096 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3.5-2b__nc_b__e0b.parquet`: .parquet file, 16,519 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3.5-2b__nc_b__e0c.parquet`: .parquet file, 63,998 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3.5-2b__nc_c__e0b.parquet`: .parquet file, 16,452 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/qwen3.5-2b__nc_c__e0c.parquet`: .parquet file, 63,977 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/sarvam-1__nc_a__e0b.parquet`: .parquet file, 16,523 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/sarvam-1__nc_a__e0c.parquet`: .parquet file, 64,583 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/sarvam-1__nc_b__e0b.parquet`: .parquet file, 16,621 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/sarvam-1__nc_b__e0c.parquet`: .parquet file, 64,889 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/sarvam-1__nc_c__e0b.parquet`: .parquet file, 16,496 bytes (binary or per-item data, not dumped)
- `results/nc1/scores/sarvam-1__nc_c__e0c.parquet`: .parquet file, 64,774 bytes (binary or per-item data, not dumped)

# Results log

One entry per experiment run: date, experiment id, config, commit hash, headline numbers (with n and CIs),
prediction, outcome (confirmed / refuted / inconclusive), surprises, next step. Every number here comes from a file in
`results/`.

---
## 2026-10-07 — E2 step 1: transliteration round trip and lossy scheme (draft on FLORES-200)

- Config: `scripts/e02_translit.py --corpus flores200` and `--corpus wikipedia`; scheme `itrans` (our ASCII ITRANS,
  Dravidian e/E o/O convention; see `src/shattered/translit/scheme.py`).
- Results files: `results/e02_translit/roundtrip_flores200.json`, `lossy_flores200.json`, `roundtrip_wikipedia.json`.
- Headline numbers:
  - Round trip, FLORES-200 Kannada dev+devtest: **2009/2009 exact (100%)**, n = 2009 sentences, 270,103 chars.
    17 sentences are not NFC; after NFC normalization still 2009/2009 exact and zero non-ASCII chars in the output.
  - Round trip, Kannada Wikipedia: **31,437/31,437 articles exact (100%)**, 149.2M chars.
  - Lossy scheme information loss (FLORES Kannada, back-mapper trained on Kannada Wikipedia): **CER 3.09%**,
    word accuracy 88.5%, back-map vocabulary coverage 93.1% of tokens. Without the corpus (decode lossy as ITRANS):
    CER 19.2%. 10.4% of Wikipedia native word types collide with another type under the lossy map.
- Prediction: none pre-registered for this step (target was 100% round trip). Outcome: target met.
- Surprises: the `indic_transliteration` library default is not lossless and not ASCII (short e/o -> è/ò; '.' -> danda
  on the way back; Latin text and vowel hiatus not preserved). We use our own engine instead; see test suite.
- Caveat: FLORES-200 used because FLORES+ is gated pending terms acceptance; rerun with `--corpus flores_plus`.
- Next: E1 local token counts.

---
## 2026-10-07 — E1 (local part): token cost atlas, draft on FLORES-200

- Config: `configs/e01_cost.yaml`; script `scripts/e01_cost.py`; figures `scripts/e01_plots.py`.
- Results: `results/e01_cost/summary.csv` (table view of all figures), `token_counts.parquet`, `tokenizers.json`.
  Figures: `paper/figures/F1_tax_by_language`, `F1b_tax_drift`, `F1c_kannada_forms` (.pdf/.png).
- n = 2009 parallel sentences (FLORES-200 dev+devtest, NFC) per language; 33 tokenizers loaded, 23 distinct
  (identical groups: cl100k=OLMo 2; o200k=gpt-oss=Phi-4-mini; Qwen1.5=2.5=3; Qwen3.5=3.8;
  Tekken=Mistral Nemo=Sarvam-M=Krutrim-2=Apertus=Nemotron Nano v2; Sarvam-1=Sarvam 2B v0.5; Phi-3.5=Llama 2).
- Headline numbers (Kannada tax ratio = tokens / English tokens on the same sentences, paired bootstrap 95% CI):

  | Tokenizer | native | ITRANS | lossy |
  |---|---|---|---|
  | o200k (GPT-4o) | 1.99 [1.97, 2.00] | 2.41 [2.40, 2.43] | 1.89 [1.87, 1.90] |
  | Gemma 4 | 1.94 [1.92, 1.96] | 2.42 [2.40, 2.44] | 1.92 [1.90, 1.93] |
  | Qwen 3.5–3.8 | 3.13 [3.11, 3.16] | 2.49 [2.47, 2.51] | 1.97 [1.96, 1.99] |
  | Sarvam-1 | 1.23 [1.22, 1.24] | 2.76 [2.73, 2.78] | 2.25 [2.23, 2.27] |
  | cl100k (GPT-4) | 8.87 [8.79, 8.95] | 2.59 [2.57, 2.61] | 2.12 [2.10, 2.13] |
  | Llama 2 | 10.84 [10.74, 10.94] | 2.46 [2.44, 2.48] | 2.01 [1.99, 2.02] |

  o200k native tax for the four Dravidian languages: Kannada 1.99, Tamil 1.98, Telugu 1.94, Malayalam 1.95;
  Hindi 1.57, Bangla 1.72.
- Prediction: Dravidian languages cost >= 2x English on most English-centric tokenizers; newer generations narrow but do
  not close the gap; failure if < 1.3x on current commercial tokenizers.
- Outcome: **partly confirmed, inconclusive for commercial APIs.** On the 50k/100k-vocab tokenizers the tax is 6–15x;
  every family's newest generation narrows it a lot (OpenAI 13.6x -> 2.0x; Qwen 6.9x -> 3.1x for Kannada) but none
  closes it. On o200k it is just under 2x (1.94–1.99), not above. Indic-focused Sarvam-1 is 1.16–1.35x. The failure
  criterion concerns commercial API tokenizers (Gemini, Claude), which are not counted yet.
- **Surprise that contradicts a premise:** lossless ITRANS is *more* expensive than native script on current
  tokenizers (o200k +21%, Gemma 4 +25%, Sarvam-1 +124%); it only saves tokens on older tokenizers (cl100k −71%,
  Llama 2 −77%). Even the lossy form saves only ~5% on o200k. This undercuts E3 prediction (1) ("ITRANS cuts input
  tokens substantially") for modern models, and makes E9 the place where any cost win must come from (ITRANS
  capitals such as "rAjadhAni" likely fragment badly).
- Not done (blocked): API counters (Gemini, Claude), Llama 3 / Gemma 2–3 tokenizers (gated), natural romanization,
  rupee costs (prices.yaml needs verified prices). FLORES+ rerun pending access.

---
## 2026-10-07 — E5 pilot (GATE): timing and pilot-only signal

- Config: `configs/e05_pretrain.yaml` (pilot block); `scripts/e05_pretrain.py prepare` then `pilot`.
- Results: `results/e05_pretrain/pilot_report.json`, `data_meta.json`, `pilot_v{256,16384}_s0/` (log, final.json,
  minimal_pairs.json), `minimal_pairs_vocab.json`.
- Timing on RTX 3070 Laptop: vocab 256 0.57 s/step, 16k 0.20 s/step (incl. evals); extrapolated full grid
  (5 vocabs x 3 seeds x 400 MB) **8.3 h** on this GPU. T4 not measured.
- Pilot-only (n = 1 seed, 10% budget, not a finding): val BPB 1.142 (256) vs 0.833 (16k); minimal pairs 52.1% vs 80.1%
  (n = 472). Direction matches the prediction; the byte model had 3.4x the training FLOPs.
- Bytes/token: 1.00 / 2.41 / 3.16 / 3.96 / 4.10 for 256 / 512 / 1k / 4k / 16k — the 4k and 16k conditions are nearly
  identical in fragmentation on TinyStories; grid revision recommended at the gate.
- Outcome vs prediction: not assessable from the pilot. Next: GATE decision (budget, vocab grid, T4 timing).

---
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
## 2026-10-07 — E1/E2 rerun on FLORES+ (now primary)

- `results/e01_cost_flores_plus/summary.csv`, `results/e02_translit/{roundtrip,lossy}_flores_plus.json`; figures F1,
  F1b, F1c regenerated from FLORES+.
- E2: 2009/2009 exact round trip (17 non-NFC sentences; 2009/2009 after NFC); lossy CER 3.09%, word acc 88.5%.
- E1, o200k native tax (n = 2009): Kannada 1.98 [1.97, 2.00], Tamil 1.98 [1.96, 1.99], Telugu 1.94 [1.92, 1.95],
  Malayalam 1.95 [1.94, 1.97], Hindi 1.57, Bangla 1.72. Kannada ITRANS 2.41 [2.39, 2.43], lossy 1.88 [1.87, 1.90].
  All cells within 0.01 of the FLORES-200 draft; the outcome recorded above (narrow failure on o200k) is unchanged.

---
## 2026-10-07 — E0 add-on: native vs ITRANS tokens per word (FLORES+ Kannada, 31,530 words in context)

- `results/e00_gate/tokens_per_word.csv`. Mean tokens per word, native -> ITRANS (share of words >= 4 tokens):
  Qwen2.5/3 11.79 -> 4.32 (96% -> 59%); Qwen3.5 5.28 -> 4.18 (77% -> 57%); Param-1 4.13 -> 4.01;
  Phi-4-mini/o200k 3.25 -> 3.96 (40% -> 53%); Gemma 4 3.20 -> 4.01 (40% -> 54%); Sarvam-1 2.34 -> 5.31 (18% -> 72%).
- Implication for E4: the fragmentation ordering of native vs ITRANS **flips across model families** (ITRANS less
  fragmented on Qwen, more fragmented on Gemma 4 / Phi-4 / Sarvam-1). E4 can use this as a crossover: an effect
  driven by fragmentation should change sign between the families; an effect driven by script should not.
  Gated candidates (Llama 3.x, Gemma 2/3, Aya) are pending access.

---
## 2026-10-07 — E9 GATE: tokenizer-optimal reversible romanization (token savings only)

- Diagnostic (`results/e09_romanize/capitals.json`, FLORES+): lowercasing ITRANS (lossy) removes 97% of ITRANS's token
  excess over native on o200k and 85% on Gemma 4 (27% on Sarvam-1); 71% of ITRANS word tokens contain a mid-word
  capital. So capitals do explain the excess *when the information they carry is dropped*.
- Search (`scripts/e09_search.py`, `results/e09_romanize/search_jobs.json`, `best_schemes.json`): greedy coordinate
  descent over 59 units, candidates from ITRANS/HK/Velthuis/IAST-ASCII/informal spellings incl. lowercase-only
  lossless alternatives; objective = frequency-weighted tokens over the 50,513 Kannada Wikipedia words with
  count >= 30; 5 targets (o200k, Gemma 4, Qwen3.5, Qwen2.5/3, universal) x 2 variants (free, lowercase-only) x 4
  restarts. ("ru"/"ri" for vocalic r are excluded: they make ರು/ರಿ unencodable.)
- Losslessness: all 10 best schemes round-trip 2009/2009 FLORES+ sentences and 1048/1048 Wikipedia articles.
- Held-out savings (`results/e09_romanize/savings.csv`, FLORES+ Kannada, sentence level), best scheme for each target
  vs ITRANS on that tokenizer: **o200k −4.8%**, **Gemma 4 −2.3%**, **Qwen3.5 −1.0%**, **Qwen2.5/3 −2.3%**.
  Lowercase-only schemes: +0.3% to −0.7% (no gain). Versus native script, the best scheme is still +15.7% on o200k and
  +21.9% on Gemma 4 (−21.5% on Qwen3.5, −63.9% on Qwen2.5/3, where native script is badly fragmented).
  Search-objective savings (word list) were larger (o200k 6.3%), so part of the gain did not transfer to running text.
- Prediction: >= 10% fewer tokens than ITRANS on the target tokenizer, accuracy within ITRANS's CI. Failure: < 5%.
  **Outcome: refuted (failure criterion met on every target).** Lossless information costs tokens on modern
  tokenizers whatever the spelling within this candidate space; capitals are expensive, but their lowercase
  replacements (aa, tt, nn, ...) cost about as much. Per the gate, no accuracy evaluation was run.
- Figure: `paper/figures/F8_e09_savings` (draft). Mapping tables: `results/e09_romanize/schemes.md`.

---
## 2026-10-07 — Scope changes

- **E9 dropped** after its gate: negative result as recorded above (held-out savings over ITRANS 1.0–4.8%, below the
  5% failure line on every target). Not pursued further.
- **E7 dropped**: FragMend (arXiv 2604.16656) already does Patchscopes detokenization and vocabulary expansion for
  non-Latin scripts.
- **Limitation (E1)**: no Anthropic API key will be used, so Claude tokenizers are not measured. Anthropic's pricing
  page (read 2026-10-07) states that Claude 4.7+ uses a newer tokenizer producing ~30% more tokens for the same text;
  we cannot verify how this affects Kannada.

---
## PRE-REGISTRATION — M1 detokenization layer (written 2026-10-07, before any M1 run)

Models: Qwen 2.5/3 (Qwen3-1.7B or Qwen2.5-1.5B-Instruct, per E0), Qwen3.5-2B, Gemma 4 E2B, Sarvam-1.
Forms: native Kannada, ITRANS, English (reference). Methods: Patchscopes (FragMend setup) and linear probes.

Measured tokens per word (FLORES+ Kannada, `results/e00_gate/tokens_per_word.csv`), native -> ITRANS:
Qwen 2.5/3 11.79 -> 4.32; Qwen 3.5 5.28 -> 4.18; Gemma 4 3.20 -> 4.01; Sarvam-1 2.34 -> 5.31.

Competing predictions:
- **H-frag (fragmentation-driven)**: the form with more tokens per word detokenizes later. Native later than ITRANS on
  Qwen 2.5/3 and Qwen 3.5; ITRANS later than native on Gemma 4 and Sarvam-1 (ordering flips across families).
- **H-script (script-driven)**: ITRANS detokenizes earlier than native in all four models.

Operationalization and decision rule (fixed now):
- Statistic per model and method: Delta = mean over words of (detok layer native − detok layer ITRANS) / n_layers,
  computed on the same Kannada words in both forms (paired by construction), restricted to words detokenized in both
  forms; 95% paired bootstrap CI over words (10,000 resamples). Also reported: detokenization success rates per form.
- A model "favors ITRANS-earlier" if the CI of Delta lies above 0, "native-earlier" if below 0, "no difference" if it
  includes 0.
- H-frag is supported if Gemma 4 and Sarvam-1 are native-earlier while both Qwen models are ITRANS-earlier (or no
  difference for at most one Qwen model). H-script is supported if all four models are ITRANS-earlier. Any other
  pattern is recorded as inconclusive for both. Patchscopes is primary; probes are reported alongside, and
  disagreement between methods is reported, not resolved post hoc.
- Secondary (within form): detok layer increases with the word's token count (Spearman rho > 0, CI excluding 0), per
  model and form.

---
## 2026-10-08 — E5 controlled pretraining: full grid (6 vocabularies x 3 seeds)

- Config: `configs/e05_pretrain.yaml` (approved grid {256, 384, 512, 768, 1024, 4096}); `scripts/e05_pretrain.py grid`;
  analysis `scripts/e05_analysis.py`. Results: `results/e05_pretrain/T6.csv`, `analysis.json`, `curves.parquet`,
  `run_v*_s*/`. Figures: `paper/figures/F6_e05_fragmentation`, `F6b_e05_curves`. All 18 runs completed; identical
  400,001,505 training bytes per run; 14,162,304 non-embedding params in every condition; embedding params 0.10M (256)
  to 1.57M (4096).
- Validation bits per byte (mean ± sd over 3 seeds; tokens/word on TinyStories validation):

  | vocab | tokens/word | val BPB | minimal pairs (n = 472) | train FLOPs |
  |---|---|---|---|---|
  | 256 | 5.01 | 0.5970 ± 0.0009 | 0.886 ± 0.052 | 4.18e16 |
  | 384 | 2.54 | 0.5696 ± 0.0011 | 0.924 ± 0.050 | 1.93e16 |
  | 512 | 2.08 | 0.5606 ± 0.0021 | 0.889 ± 0.029 | 1.56e16 |
  | 768 | 1.74 | 0.5513 ± 0.0010 | 0.880 ± 0.074 | 1.29e16 |
  | 1024 | 1.58 | 0.5460 ± 0.0002 | 0.899 ± 0.074 | 1.18e16 |
  | 4096 | 1.27 | 0.5285 ± 0.0011 | 0.955 ± 0.023 | 1.00e16 |

- BPB vs tokens per word: Spearman rho = 1.0 across the 6 conditions; span 0.069 BPB vs max seed sd 0.002 (~33x).
  More fragmented conditions used *more* compute (byte-level 4.2x the FLOPs of 4096). At equal compute (1.0e16 FLOPs,
  read from the training curves, 2 MB validation subset): 256 0.792, 384 0.636, 512 0.599, 768 0.569, 1024 0.555,
  4096 0.527 — the gap widens when compute is equalized.
- Minimal pairs: not monotonic (Spearman rho = −0.43, p = 0.40, n = 6 conditions); seed sd 2–7 points. 4096 is best at
  every stage of training (mean over all evaluations 0.885 ± 0.006 vs 0.77–0.84 for the rest); byte-level learns
  slowest early (0.53 at 10% of training vs 0.73 for 4096) and partly catches up (0.886 at the end). Plural agreement
  (~0.97) and irregular past (1.00, n = 12) are near ceiling; singular agreement and determiner-noun carry the signal.
- Prediction: as tokens/word increases, BPB worse, minimal-pair accuracy lower, assembly depth later, all beyond seed
  variance; failure if no monotonic relationship or the effect disappears at equal compute.
- **Outcome: BPB confirmed** (monotonic, far beyond seed noise, stronger at equal compute). **Grammar: inconclusive**
  — only the extremes differ (4096 best and fastest; byte-level slowest to learn), middle conditions are within seed
  noise and the benchmark is partly at ceiling. **Assembly depth: pending** (M1 probes/Patchscopes on these models).
- Caveat: one corpus (TinyStories), one model size (8 layers, d = 384), 400 MB per run.

---
## 2026-10-08 — E0 GATE (4 of 5 models; Gemma 4 E2B not run)

- `scripts/e00_gate.py`; results `results/e00_gate/summary.csv`, `summary.json`, `scores_<model>.parquet`. n = 200 items
  per task (IndicXNLI kn test aligned to XNLI en; IndicSentiment kn test with English review), stratified, seed 0.
  Log-likelihood of English label words after an English instruction (templates e0_*_v1). Raw accuracy, 95%
  bootstrap CI. Chance: XNLI 33.3%, sentiment 50%.
- Gemma 4 E2B: the E0 job was stopped by Claude Code for low system memory while loading Gemma (the loader briefly
  materializes the 10 GB checkpoint in CPU RAM). Not restarted pending Aarnav's go-ahead.

  | model | sentiment en / native / ITRANS | XNLI en / native / ITRANS |
  |---|---|---|
  | Qwen2.5-1.5B-Instruct | 98.5 / 70.5 / 49.5 | 79.5 / 51.0 / 37.5 |
  | Qwen3-1.7B | 98.5 / 86.5 / 58.0 | 61.5 / 43.0 / 37.0 |
  | Qwen3.5-2B | 97.5 / 78.5 / 67.5 | 43.0 / 34.0 / 34.0 |
  | Sarvam-1 | 95.5 / 98.0 / 80.0 | 57.5 / 52.0 / 40.5 |

- Gate rule (native >= chance + 10 and English >= chance + 15 on one task): **all four pass**, via sentiment;
  Qwen2.5 and Sarvam-1 also pass on XNLI. Qwen3.5-2B collapses to one label on XNLI (99.5% of predictions in native
  and ITRANS; calibrated English 62.0%).
- **Finding relevant to M1/M2: ITRANS accuracy is below native in every model and task, including the Qwen models
  where ITRANS is far less fragmented** (Qwen2.5: native 70.5 vs ITRANS 49.5 on sentiment, with 99.5% of ITRANS
  predictions on one label; Qwen3 86.5 vs 58.0). Fewer tokens did not make ITRANS easier; familiarity with the form
  (training data) dominates at the accuracy level. This argues against the simplest fragmentation story for accuracy
  and has to be reported. Several ITRANS cells are at chance (all XNLI-ITRANS, Qwen2.5 sentiment-ITRANS), which limits
  M2/M6 for those cells.

---
## 2026-10-14 — Step 0 decisions

- Qwen 2.5/3 slot: **Qwen2.5-1.5B-Instruct** (passes E0 on both tasks).
- Gemma 4 E2B: retried with a new low-memory text-only loader (language-model tensors streamed from safetensors in
  bf16 onto a meta-initialized model; per-layer embedding table on CPU). Loads in 11 s, 4.25 GB GPU, 5.3 GB peak
  working set; chat sanity check correct. **Gemma 4 stays.** Note: Gemma's tokenizer does not add BOS by default and the
  model degenerates without it; all our Gemma inputs prepend BOS explicitly.

---
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
## 2026-10-14 — E0 natural romanization: defects and regeneration queue (no API calls made for this check)

501 of 587 unique E0 texts were romanized before the Gemini daily quota; the remaining 86 (all sentiment reviews) run
tomorrow with the same model and prompt. Correction to the 2026-10-14 status report: the 9 "flagged" outputs are not
word-count outliers (all word ratios are 0.95–1.0); the flag fired on **leftover Kannada script**.
The prompt asks for no diacritics or special symbols, so 20 of the 501 outputs violate it
(`data/processed/natural_e0_regen_queue_v1.json`):
- 9 with leftover Kannada script (usually one untransliterated word or suffix, e.g. "ಪಡೆಯುವಂತೆ", "ondಕ್ಕಿಂತ");
- 2 with another Indic script (Malayalam "tക്ഷണ" for ತಕ್ಷಣ; Telugu "ంత" inside a word);
- 9 with Latin diacritics or IPA (IAST-style ā ē ī ū ṇ ḍ ḷ ṭ ś ṣ ṅ ñ; š; ü; IPA ɛ ɩ).
One further output keeps "À" because the Kannada source has "À la carte"; it is valid.
All 20 will be re-asked tomorrow with the same model, prompt and temperature (attempts 2 and 3; the attempt number
only changes the cache key). First attempts are kept in the data; rows still defective after attempt 3 will be
reported, not silently fixed.

---
## PRE-REGISTRATION — Step 3: M1 word-identity probes on the E5 tiny models (written 2026-10-14, before any run)

Setup: all 18 final E5 checkpoints (vocab 256, 384, 512, 768, 1024, 4096 x seeds 0-2). One fixed set of ~300 frequent
TinyStories words (alphabetic, >= 3 letters, space-preceded) with a fixed set of occurrences in held-out validation
stories, identical across all 18 models. Residual stream at the word's last token at every layer (0 = embeddings,
1-8 = blocks). Linear probe for word identity per layer, held-out occurrences (70/30 split stratified by word, fixed
seed), random-label control (labels permuted across occurrences). Detokenization layer = first layer whose held-out
accuracy reaches 90% of that model's maximum over layers; 95% CI by bootstrapping test occurrences.

- **Q1 (detokenization moves later as vocabulary shrinks)**: the seed-mean detokenization layer is non-decreasing from
  vocab 4096 to vocab 256. Confirmed if Spearman rho(tokens per word, seed-mean detok layer) over the 6 conditions
  >= 0.8 and the vocab-256 mean exceeds the vocab-4096 mean by more than both conditions' seed sd; refuted if
  rho <= 0; otherwise inconclusive.
- **Q2 (detokenization depth tracks the BPB gap)**: Spearman rho(seed-mean detok layer, BPB gap vs vocab 4096) over the
  6 conditions >= 0.8. Refuted if rho <= 0; otherwise inconclusive. With 6 conditions and 9 possible layer values,
  ties are likely and n is small, so Q2 is weak evidence either way; it is reported with the per-seed points.
- Known limitation, stated now: at vocab 4096 most frequent words are single tokens, so their layer-0 accuracy is
  near-perfect by construction. The analysis is also reported restricted to multi-token occurrences.

---
## 2026-10-14 — Step 3 (GATE 3 draft): M1 word-identity probes on the 18 E5 tiny models

Config: `scripts/m1_tiny_probes.py` (300 words, 40 occurrences each in validation stories, 3,600 held-out test
occurrences; probe settings in `results/m1_tiny/analysis.json`). Outputs: `results/m1_tiny/{per_run,summary}.csv`,
`analysis.json`. Pilot (2 checkpoints) found that 900-character story cuts exceeded the 256-token context at vocab
4096; the cut was changed to 800 characters before the full run.

| vocab | tokens/word (valid) | multi-token share of probed occ. | layer-0 acc | max acc | control max | detok layer (3 seeds) | BPB gap vs 4096 |
|---|---|---|---|---|---|---|---|
| 256 | 5.01 | 1.00 | 0.070 | 1.000 | 0.004 | 1, 1, 1 | 0.068 |
| 384 | 2.54 | 0.92 | 0.300 | 1.000 | 0.007 | 1, 1, 1 | 0.041 |
| 512 | 2.08 | 0.77 | 0.533 | 1.000 | 0.004 | 1, 1, 1 | 0.032 |
| 768 | 1.74 | 0.43 | 0.847 | 1.000 | 0.004 | 1, 1, 1 | 0.023 |
| 1024 | 1.58 | 0.12 | 0.993 | 1.000 | 0.004 | 0, 0, 0 | 0.018 |
| 4096 | 1.27 | 0.00 | 1.000 | 1.000 | 0.004 | 0, 0, 0 | 0 |

- **Q1: confirmed by the registered rule** (Spearman 0.83, p = 0.042; 256 minus 4096 = 1 layer, seed sd 0).
  **Q2: confirmed by the registered rule** (Spearman 0.83 vs BPB gap).
- **But the result is degenerate and should not carry the paper's mechanism claim.** Word identity saturates after one
  block at every vocabulary size (held-out accuracy 0.987–1.000 at layer 1), so the detok layer can only be 0 or 1.
  The 0/1 split is decided by layer-0 accuracy, which is identical across seeds: it measures whether the last
  token alone identifies the word among 300 candidates (a property of the tokenizer), not how the model spends
  depth. The random-label control is at chance (<= 0.007) everywhere, so the probe is not memorizing.
- Plain reading: in these 8-layer models, linear word identity is assembled within the first block regardless of
  fragmentation. The BPB tax from E5 is not explained by "more layers spent on detokenization" as measured by a
  linear identity probe. Options for a more sensitive measure are listed in the Gate 3 report; no new design is
  run until Aarnav chooses.

---
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
## 2026-10-15 — Step 3b (GATE 3): MDL and erasure probes on the 18 E5 tiny models

Config: `scripts/m1_tiny_mdl.py` (300 words that are >= 3 tokens under vocab 768, 40 occurrences each, story cut 700
characters after the 800 cut overflowed the 256-token context at vocab 4096 in the pilot). Outputs:
`results/m1_tiny_mdl/{per_run,summary}.csv`, `analysis.json`.

| vocab | tokens/word (these words) | MDL detok layer (seeds 0,1,2) | compression at layer 0 | max compression | erasure magnitude at -1 |
|---|---|---|---|---|---|
| 256 | 6.66 | 2, 2, 2 | 1.66 | 21.4–21.8 | 0.000–0.001 |
| 384 | 4.29 | 1, 1, 1 | 2.21 | 21.5–21.6 | 0.003–0.007 |
| 512 | 3.84 | 1, 1, 1 | 2.51 | 21.0–21.5 | 0.005–0.010 |
| 768 | 3.39 | 1, 1, 1 | 2.86 | 21.1–21.3 | 0.009–0.012 |
| 1024 | 2.65 | 1, 1, 1 | 4.01 | 21.4–21.5 | 0.005–0.007 |
| 4096 | 1.00 | 0, 0, 0 | 23.3 | 23.3 | n/a (single tokens) |

- **Classification (agreed with Aarnav, 2026-10-15): MDL direction confirmed, magnitude small (0 to 2 layers of 8);
  erasure refuted.** No deeper tiny models are trained before Gate 2.
- Q1b: confirmed by the registered rule (Spearman 0.85, p = 0.034; 256 minus 4096 = 2 layers, seed sd 0).
  Q2b: confirmed by the rule (Spearman 0.85 vs BPB gap).
- Substantively it is still coarse: only the pure byte model needs a second block; every merged vocabulary (384–1024)
  assembles these 3+-token words within one block, and the bootstrap CIs are degenerate (all mass on one layer).
  MDL adds resolution over the saturated plain probe, but "more fragmentation costs more layers" holds only at the
  byte extreme in 8-layer models.
- **Q3b (erasure): refuted.** The identity of the previous in-word token stays 99–100% decodable at every layer
  (magnitude <= 0.012 in all 15 eligible runs). The tiny models do not erase sub-word information the way Feucht et
  al. report for large models.
- Unexpected: word-identity compression peaks at layers 1–3 and then falls steadily (to about 9 at layer 8) in every
  model, so word identity becomes less linearly accessible toward the output.

---
## 2026-10-15 — E0 natural romanization quality check

- **Spot checked by a native speaker (Aarnav, 2026-10-15), no issues found:** 20 outputs sampled at random (seed
  20261015) from the 482 non-defective outputs then available (`data/annotation/natural_spotcheck20_v1.json`).
- Back-translation (below) is not used as a quality check: the back-translator reads romanized Kannada poorly, so
  low similarity mostly reflects the reader, not the romanization. Among the 26 lowest-similarity texts, no clear
  romanization error was found.
- **Source noise** (`data/annotation/source_noise_v1.json`): 2 E0 texts whose Kannada does not match the dataset's
  English (xnli-test-555 hypothesis: the Kannada drops "a vacuum"; xnli-test-1375 hypothesis: the Kannada says "I
  cannot count anything"). Excluded from the back-translation statistics. Correction to an earlier draft that
  listed 4 such items: the other two (xnli-test-1558, indicsentiment-test-662) are faithful translations that the
  back-translator misread ("Ogle" -> "Google"; "not durable" -> "cannot be endured").

---
## 2026-10-15 — Large-model result: native vs romanized comprehension gap (back-translation)

Groq `openai/gpt-oss-120b` (temperature 0, reasoning effort low) translates each E0 text into English, once from the
natural romanization (prompt backtranslate_v1) and once from native Kannada script (backtranslate_native_v1);
cosine similarity of each back-translation to the dataset's English (all-mpnet-base-v2). Outputs:
`results/e0b_natural_check/{backtranslation_with_control.csv, summary_control.json}`.

- **Interim, not final.** The final number will come from all 501 paired texts (and the 86 new texts once they
  exist). 218 texts have both versions so far (2 source-noise items excluded); Groq's 200k tokens/day limit stopped
  the control. 95% bootstrap CIs (10,000 resamples), paired gap = native minus romanized cosine:
  - all 218 controlled texts: native 0.814, romanized 0.582, gap **0.232 [0.203, 0.262]**. **Biased upward by
    selection**: the 24 lowest-similarity texts (26 flagged minus the 2 source-noise items) were controlled first.
  - excluding those flagged texts: 194 texts, native 0.820, romanized 0.637, gap **0.183 [0.160, 0.208]**. Not a
    random sample either: these were taken in file order, so 193 of the 194 are XNLI texts (no sentiment reviews).
  - random subset: the remaining texts are now controlled in a seeded random order
    (`scripts/e0b_backtranslate_control.py`), and the summary reports the gap on the fully controlled prefix of
    that order (`gap_random_prefix`). It is empty until Groq's quota resets.
- Reading: a 120B multilingual model understands Kannada in its own script far better than the same sentences
  typed in natural romanization. This is consistent with the familiarity account (E0b), now seen in a model we do
  not study and through generation rather than classification.

---
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
## PRE-REGISTRATION (exploratory) — item-level fragmentation within form (written 2026-10-15, before computing)

Data: Gate 1 item scores (primary predictions, i.e. three-input calibration with the raw fallback; natural excludes
the 9 defective texts). For every model x task x form with form in {native, ITRANS, lossy, natural} (English not
included), in cells that are informative under the Gate 1 rule: logistic regression of item correctness on the
item's mean tokens per word (that model's tokenizer, that form's text; for XNLI premise and hypothesis pooled)
controlling for the item's length in characters (same text). Only tokenizers are used; no model is run.
- Primary family: sentiment, 5 models x 4 forms = 20 tests, Holm-corrected. Secondary family: XNLI, same, Holm
  separately (many XNLI cells predict one label 98–100% of the time and are reported but expected to be empty).
- **Prediction:** negative coefficient on tokens per word (more fragmentation, more errors), separately within
  native script and within the romanized forms (ITRANS, lossy, natural pooled as a group of cells).
- Rule, per group in the primary family: **supported** if most coefficients in the group are negative and at least
  one is significantly negative after Holm; **contradicted** if any is significantly positive or most are positive
  with none significantly negative; otherwise **no evidence**. Cells where the model predicts one label for >= 95% of
  items are reported but not counted.
- Also reported (exploratory, already seen in Gate 1, so not a test): Sarvam-1 lossy and natural vs ITRANS, which is
  confounded by ITRANS's capital letters.

---
## 2026-10-15 — Exploratory result: item-level fragmentation within form (registered above)

Script `scripts/e0b_item_fragmentation.py` (tokenizers only); outputs `results/e0b_familiarity/gate1/
item_fragmentation.{csv,json}`. Coefficients are per SD of the item's tokens per word, controlling for length.
- **Sentiment (primary family, Holm over 20 tests): no coefficient is significant** (smallest uncorrected p = 0.011,
  Holm 0.22: Gemma 4 native, negative, in a cell at 98.5% accuracy). Counted cells (constant-label rate < 95%):
  native 5 cells, 2 negative -> **"contradicted" by the registered rule** (most coefficients positive, none
  significantly negative); romanized 12 cells, 7 negative -> **"no evidence"**.
- **XNLI (secondary): no coefficient is significant** (smallest p = 0.029, Holm 0.58); native 1 of 4 negative and
  romanized 2 of 9 negative -> "contradicted" by the rule. Six XNLI cells predict one label >= 95% of the time and
  are not counted.
- Reading: within a form, items that happen to fragment more are not measurably harder once length is controlled.
  The within-form spread is narrow (SD about 0.5–0.8 tokens per word, 1.9 for Qwen native) and correctness is
  noisy, so this test has little power; it gives no support to fragmentation as an item-level driver.
- **Sarvam-1 within romanization (exploratory, already seen in Gate 1, confounded by ITRANS's capital letters):**
  lossy and natural (4.36 / 4.29 tokens per word on sentiment) vs ITRANS (5.24): sentiment +7.5 (lossy, 21 vs 6
  discordant, p = 0.006, Holm 0.15) and +7.6 (natural, 27 vs 12, p = 0.024, Holm 0.50); XNLI +8.5 (lossy, p = 0.012,
  Holm 0.28) and +7.3 (natural, p = 0.020, Holm 0.44). Consistent in direction, not significant after correction,
  and not separable from the capitals.

---
## 2026-10-15 — GATE 2: full M1/M4 run (Qwen2.5-1.5B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; English, native, ITRANS)

Run: `scripts/m14_full.py` via `scripts/chain.sh` (16:40–20:47 IST, 4.1 h: Qwen2.5 37.6 min, Qwen3.5 70.2,
Sarvam-1 46.2, Gemma 4 93.2; per model and form about 4–15 min forward pass, 4–13 min Patchscopes, 3–5 min probes;
`results/m14_full/timing.json`). Analysis: `scripts/m14_gate2.py` -> `results/m14_full/gate2/` (per_form, paired,
m4, erasure, patchscopes_prereg, patchscopes_spearman CSVs; verdicts.json). Draft figure
`paper/figures/F_m14_layer_curves_draft.{pdf,png}`. M1: 300 Kannada Wikipedia words x 30 occurrences (9,000,
ITRANS paired word by word; 208 of the words occur in E0) and 300 English words x 30. M4: 2,009 FLORES+ sentences.
CIs: 10,000 paired bootstrap resamples (occurrences for MDL and probes, words for Patchscopes, sentences for M4).

**MDL detok layer (primary; first layer reaching 90% of max compression).** Tokens per word are for these words.

| model (layers) | tpw native -> ITRANS | MDL native | MDL ITRANS | ITRANS − native [95% CI] | fraction of depth | E0-word subset (6,240 occ.) |
|---|---|---|---|---|---|---|
| Qwen2.5-1.5B (28) | 8.55 -> 3.24 | 4 | 1 | **−3 [−4, −3]** | −0.11 | −3 [−4, −3] |
| Qwen3.5-2B (24) | 3.90 -> 3.12 | 2 | 2 | 0 [0, 0] | 0 | 0 [0, 0] |
| Sarvam-1 (28) | 1.16 -> 3.94 | 0 | 6 | **+6 [6, 7]** | +0.21 | +6 [6, 6] |
| Gemma 4 E2B (35) | 2.05 -> 2.93 | 1 | 3 | **+2 [1, 2]** | +0.06 | +1 [1, 2] |

English detok is layer 0 in every model (the English words are single tokens). The E0-word subset gives the same
ordering in all four models.

**M4 (FLORES+ retrieval acc@1 against English, mean-pooled residuals).**

| model | max retrieval native [CI] | max retrieval ITRANS [CI] | alignment layer native / ITRANS | lag native / ITRANS | lag diff [CI] | max CKA native / ITRANS |
|---|---|---|---|---|---|---|
| Qwen2.5 | 0.144 [0.130, 0.161] | 0.057 [0.047, 0.067] | 14 / 1 | 10 / 0 | −10 [−11, −8] | 0.63 / 0.67 |
| Qwen3.5 | 0.973 [0.966, 0.980] | 0.097 [0.090, 0.112] | 4 / 2 | 2 / 0 | −2 [−2, 2] | 0.73 / 0.49 |
| Sarvam-1 | 0.941 [0.933, 0.952] | 0.458 [0.440, 0.481] | 10 / 16 | 10 / 10 | 0 [−1, 0] | 0.59 / 0.49 |
| Gemma 4 | 0.988 [0.984, 0.993] | 0.222 [0.204, 0.240] | 5 / 7 | 4 / 4 | 0 [0, 1] | 0.75 / 0.45 |

**Registered verdicts (2026-10-15).**
- **H1 (meaning bottleneck): holds by the rule, but only through its retrieval clause.** In both Qwen models ITRANS
  detokenizes no later than native (−3 and 0 layers), and ITRANS never reaches native's maximum retrieval (paired CI
  of native minus ITRANS max: Qwen2.5 +0.088 [0.071, 0.106], Qwen3.5 +0.876 [0.859, 0.885]). The lag clause goes the
  other way: ITRANS's lag is shorter (Qwen2.5 −10 [−11, −8]), because its "alignment layer" is taken against its own
  near-floor maximum (5.7% and 9.7%) and so means little. "Never reaches" was operationalized (paired CI above 0)
  after the run log had printed the maxima; the gaps are so large that any reasonable operationalization agrees.
- **H2 (assembly bottleneck): refuted** (ITRANS is not later in either Qwen model). Qwen outcome: H1.
- **H3 (fragmentation-driven ordering): not supported by the rule, but 3 of 4 models fit.** The sign of the detok
  difference matches the sign of the tokens-per-word difference with CIs excluding 0 in Qwen2.5 (−), Sarvam-1 (+)
  and Gemma 4 (+). Qwen3.5 has 0 [0, 0] where − was predicted (its native/ITRANS tokens-per-word gap is only 0.78).
  Not refuted (ITRANS is not later in all four).
- **Original registration (2026-10-07, Patchscopes primary): not testable.** With MDL reported alongside, the same
  rule gives **H-frag** (Qwen2.5 ITRANS-earlier, Qwen3.5 no difference, Sarvam-1 and Gemma 4 native-earlier; that
  rule allowed one Qwen model with no difference). H-script is refuted under MDL.

**Patchscopes (FragMend setup) fails on Kannada in these models.** Identification at any layer: native 0.0% (Qwen2.5),
0.7% (Qwen3.5), 0.7% (Gemma 4), 77% (Sarvam-1); ITRANS 1.7%, 6.7%, 2.3%, 0.7%; English 61–98%. Outputs are
inspected, not a scoring bug: "1, 1, 1, ...", repeated commas, newlines, or other scripts. Words identified in both
forms: 0–2 per model, so the registered Delta cannot be computed. A null for these 1.5–2B models, consistent with
RomanLens' remark that decoding methods break on byte-fragmented scripts. Secondary (detok layer rises with token
count, identified words only): Qwen2.5 English rho 0.46 [0.29, 0.60], Qwen3.5 English 0.25 [0.16, 0.32]; not shown
for Sarvam-1 English/native (CI touches 0); Gemma 4 English is constant (layer 0); not testable for every other cell.

**Plain linear probe: saturated, uninformative** (as in the tiny models). Held-out accuracy is 96–100% from layer 1
in every model and form (control <= 0.7%). Detok is 0 or 1 everywhere, so it disagrees with MDL on Qwen2.5 and
Gemma 4 only by being unable to resolve them; it agrees on Sarvam-1 (+1 [1, 1]).

**Erasure (Feucht style, offsets −1/−2): small everywhere.** Previous in-word token identity stays 92–100% decodable at
the last layer; magnitude (peak minus last) 0.002–0.080. By the Step 3b rule it is "inconclusive" (not all < 0.05:
Gemma 4 native −1 0.080, ITRANS −1/−2 0.056/0.072; Sarvam-1 0.052–0.061), not "confirmed" (none >= 0.2). Qwen2.5
native at −1 has only 30 classes (byte tokens). An erasure layer exists only in Gemma 4 (17–18 of 35).

**Unexpected.** (1) As in the tiny models, word-identity compression peaks early (layers 0–10) and then falls by 40–79%
by the last layer. (2) Qwen2.5 aligns native Kannada with English poorly (max 14.4% retrieval, vs 94–99% for the
other three). This matches its E0 XNLI collapse (40.0 native). (3) Sarvam-1 is the only model with substantial ITRANS
alignment (45.8%), and its ITRANS words detokenize 6 layers late.

**Reading.** Where fragmentation differs a lot between forms, the more fragmented form needs more layers to assemble a
word (Qwen2.5 native +3, Sarvam-1 ITRANS +6, Gemma 4 ITRANS +2), but the cost is a few layers out of 24–35. Assembly is
not where romanized input fails: in every model ITRANS words are assembled within a few layers, yet ITRANS sentences
barely align with English (6–46% retrieval vs 14–99% native). This includes the Qwen models, where ITRANS is the less
fragmented form. The bottleneck is meaning, not assembly, which fits the familiarity account from E0b/Gate 1.

Caveats: occurrence-level CIs treat the 30 occurrences of a word as independent, so they are narrower than
word-clustered CIs would be. Detok layers are coarse integers, and most CIs are degenerate. Retrieval uses mean
pooling with no training.

---
## 2026-10-15 — Back-translation comprehension gap: final (all paired texts)

All 587 E0 texts now have both back-translations (`results/e0b_natural_check/summary_control.json`). Excluded: the 2
source-noise items and the 9 defective natural outputs (also excluded from E0b; the control script now drops them),
leaving **n = 576** (378 XNLI, 198 sentiment). The bottom-5% flag (28 eligible texts) no longer selects anything,
because every text is controlled.
- **Final: native 0.838 [0.828, 0.849], natural romanization 0.621 [0.604, 0.639], paired gap 0.217 [0.201, 0.234].**
  This supersedes the interim 0.232 (biased upward by selection) and 0.183 (XNLI-only file order).
- Excluding the 28 flagged texts: 548 texts, gap 0.197 [0.182, 0.212].
- Texts where the romanized back-translation lost more than 0.3 cosine against native: 167 of 576.

---
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
## 2026-10-16 — M4b linear mapping test (registered above): strong H1 inconclusive

Script `scripts/m4b_mapping.py` (CPU, about 30 min with other jobs running); outputs
`results/m4b_mapping/{summary.csv, verdict.json, items.npz}`. Pilot on Qwen2.5 first: 3.3 min per model, results
identical to the full run. Test half n = 1,005 (chance 0.1%). Best layers are chosen on the train half.

| model | native unmapped (layer) | native mapped (layer) | ITRANS unmapped (layer) | ITRANS mapped (layer) | mapped gap native − ITRANS [CI] | status |
|---|---|---|---|---|---|---|
| Qwen2.5 | 0.178 (15) | 0.517 (1) | 0.066 (1) | 0.529 (1) | −0.012 [−0.043, 0.019] | closes |
| Qwen3.5 | 0.978 (15) | 0.961 (7) | 0.113 (6) | 0.485 (3) | 0.477 [0.445, 0.509] | persists |
| Sarvam-1 | 0.944 (23) | 0.899 (26) | 0.514 (21) | 0.380 (24) | 0.518 [0.487, 0.551] | persists |
| Gemma 4 | 0.995 (7) | 0.977 (8) | 0.269 (7) | 0.473 (0) | 0.504 [0.473, 0.536] | persists |

Shuffled-pair control: 0.1–0.3% everywhere. Share of the unmapped gap remaining after mapping: Qwen3.5 55%,
Gemma 4 69%, Sarvam-1 121%, Qwen2.5 −11%.
- **Registered verdict: strong H1 inconclusive.** The gap persists in 3 of 4 models (Qwen3.5, Sarvam-1, Gemma 4) and
  closes in Qwen2.5. The rule needed all 4 for "supported" and 3 closing for "refuted".
- Qwen2.5 "closes" at a low level. Its native script is barely aligned with English either (unmapped 0.178). Both
  forms map best at layer 1, to the same ~0.52, so neither form reaches an English-aligned representation that
  ITRANS could fall short of.
- Mapping raises ITRANS above unmapped in Qwen2.5 (+0.46), Qwen3.5 (+0.37) and Gemma 4 (+0.20), and lowers it in
  Sarvam-1 (−0.13). With 1,004 training pairs in 1,536–2,304 dimensions, the ridge map is not an upper bound: it
  also lowers native retrieval wherever native is already aligned (Qwen3.5 −0.02, Sarvam-1 −0.05, Gemma 4 −0.02).
- Observation (post hoc, not a test): where mapped ITRANS does best, it does so at the input end. The best layer by
  train-half CV is 1 (Qwen2.5), 3 (Qwen3.5) and 0 (Gemma 4); in Sarvam-1 CV picked 24 (0.380), but the highest test
  value is at layer 0 (0.406). From a quarter of depth onward, mapped ITRANS is 0.06–0.39 (maximum 0.18 Qwen2.5, 0.34 Qwen3.5, 0.39 Sarvam-1, 0.28 Gemma 4). Mapped native peaks at layers
  7–26 (except Qwen2.5). A linear map at layers 0–3 over mean-pooled token vectors is largely a learned
  bag-of-tokens dictionary: shared digits, names and Latin-script loanwords in ITRANS give it lexical anchors.
  So the ITRANS gains look lexical, not like a recovered meaning representation. That reading fits strong H1 but
  is not what the registered rule tested.

## 2026-10-16 — Accuracy vs mechanism (illustrative, n = 8)
`paper/figures/F_m14_accuracy_vs_mechanism_illustrative.{pdf,png}` (`shattered.plots.m14.accuracy_vs_mechanism`):
E0 sentiment accuracy (Gate 1 primary, 95% CI) against tokens per word, best-layer unmapped retrieval (Gate 2, all
2,009 sentences) and best-layer mapped retrieval (M4b). No inference. Descriptively:
- Accuracy rises with unmapped retrieval in a nearly monotone way across all 8 points.
- Tokens per word does not order accuracy. Qwen2.5 native (12.0 tokens per word) beats Qwen2.5 ITRANS (4.2), and
  Qwen3.5 native (5.2) beats ITRANS (4.1).
- Mapped retrieval compresses the ITRANS points to 0.38–0.53 while their accuracy spans 50–82%.

---
## PRE-REGISTRATION — M4c natural romanization in M4 (written 2026-10-16, before any natural FLORES+ sentence of this sample is romanized or run)
`scripts/m4c_natural_flores.py`.
- **Sample:** 500 FLORES+ sentences drawn at random (seed 0) from the 2,009.
- **Romanization:** same model, prompt and temperature as E0 (gemini-3.5-flash-lite, natural_romanization_v1,
  temperature 0; cached, so sentences already done for E2 are free). Defective outputs get attempts 2–3 and are
  excluded if still defective; the count is reported.
- **Measures:** on the same retained sentences for native, ITRANS and natural:
  - unmapped best-layer retrieval vs English among all retained sentences
  - the M4b mapping test (50/50 split of the retained sentences, seed 0, same procedure)
  - paired bootstrap CIs, 10,000 resamples
- **Prediction (familiarity):**
  - Natural ≈ ITRANS: the paired CI of natural − ITRANS lies within ±0.10, unmapped and mapped, in at least 3 of 4
    models.
  - Natural well below native: the CI of native − natural is above 0.10, unmapped, in Qwen3.5, Sarvam-1 and Gemma 4.
  - "Supported" if both hold, "refuted" if natural − ITRANS > 0.10 (CI) in at least 3 models, otherwise inconclusive.
  - Qwen2.5 is reported but not counted for the second part, because its native script is itself unaligned
    (0.144 on all 2,009).

---
## REGISTRATION — M4b robustness check (written 2026-10-16, before running)
`scripts/m4b_robustness.py`. Same cached vectors, split (seed 0), 5 folds and train-half layer selection as M4b.
Two alternative maps, each CV-tuned on the train half only:
- **ridge_wide:** the M4b ridge with the alpha grid widened to 1e-6 … 1e3. M4b's grid bottomed out at 1e-3, and
  Qwen2.5 chose 1e-3 at most layers.
- **procrustes:** orthogonal Procrustes between the top-k PCA subspaces of the form and of English (centered, rows
  unit-normalized), with k CV-tuned in {32, 64, 128, 256, 512}.

The registered M4b status rule (persists / closes / partial at 0.10) is applied to each. **The M4b verdict counts as
robust if every model's status is the same under both alternatives.** Any change is reported model by model. This is a
check of the analysis choices, not a new hypothesis, and it cannot change the registered M4b verdict.

---
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
## PRE-REGISTRATION — Kanglish and human-corrected natural romanization: K1–K3 (written 2026-10-16, before any Kanglish draft exists and before any scoring)
Scripts: `scripts/k_annotation.py` (items, drafts, annotation page, agreement). The scoring script will be written
before scoring and will follow this registration.

**Items (500), in `data/annotation/items_v1.jsonl`:**
- The 200 E0 sentiment items (seed 0, the same as E0/E0b).
- 300 FLORES+ sentences drawn at random (seed 0) from the 515 that are in SIB-200 and in the M4b test half.
- XNLI is dropped from annotation.
- 100 random items (seed 1; 38 sentiment, 62 FLORES) are marked for a second annotator.

**Drafts** (gemini-3.5-flash-lite, temperature 0, cached; retries as for E0):
- Natural romanization uses the existing prompt `natural_romanization_v1`. For the sentiment items these are the
  E0 drafts.
- Kanglish uses the new prompt `kanglish_v1`: Bengaluru WhatsApp style, keep the full meaning, mix in English
  words where natural.

**Annotation:** `annotation/annotate_v1.html`, offline, writes a CSV after every item. For each item and each draft,
the annotator:
- rates the draft as shown: naturalness 1–5 and meaning preserved yes/no;
- then corrects it.

The primary annotator's corrections define the human-corrected forms.

**Agreement:** on the 100 double items:
- Cohen's kappa for meaning preserved;
- quadratic-weighted kappa for naturalness;
- separately for the natural and Kanglish drafts.

**Scoring:** the E0b setup unchanged, on five models:
- log-likelihood of the label words, BOS always;
- calibration: mean of "N/A", "", "[MASK]", with the raw fallback rule.

Tasks:
- sentiment, on the 200 items, with the E0 template;
- SIB-200 topic, on the 300 FLORES items, with the E0c template.

A cell is a model × task pair. It is informative if English accuracy is at least chance + 5 points. 95% bootstrap
CIs on every cell; paired McNemar tests.

**Language tags:** `shattered.translit.codemix`, fixed now.
- English lexicon: the wordfreq 3.1.1 top 50k.
- Romanized-Kannada lexicon: to_lossy of the top 50k Kannada Wikipedia words.
- A word in both lexicons, or a number or punctuation, is language-independent.
- English word share = n_en / (n_en + n_kn). The Code Mixing Index (Das and Gambäck 2014) is reported alongside.

**K1: Kanglish beats natural romanization.** Human-corrected Kanglish vs human-corrected natural; the Gemini drafts
are a secondary comparison.
- **Supported** if Kanglish > natural in every informative cell (point estimate) and the difference is significant
  (McNemar, Holm across these cells) in at least half of them.
- **Refuted** if Kanglish ≤ natural in at least half of the informative cells, or if natural is significantly above
  Kanglish in any cell.
- Otherwise **inconclusive**.

**K2: within Kanglish, more English means better.** Accuracy and M4 retrieval both increase with the English word share.
- **K2a, accuracy.** In each informative cell, fit a logistic regression of correctness on z(English share) +
  z(log tokens of the item in that model). One-sided test that the coefficient is > 0; Holm across cells.
- **K2b, retrieval.**
  - Data: the 300 FLORES items. Each of the four M4 models gets a forward pass on the human-corrected Kanglish
    sentences, with the same sentence vectors as M4.
  - Layer: the train-half best unmapped layer M4b chose for native.
  - Outcome: the rank of the true English sentence among the 1,005 test-half English sentences.
  - Model: linear regression of −log rank on z(English share) + z(log tokens). One-sided test that the coefficient is
    > 0; Holm across the four models.
- **Rule, applied to K2a and K2b separately:**
  - **supported** if the coefficient is > 0 in every counted cell and significant in at least half;
  - **refuted** if it is ≤ 0 in at least half;
  - otherwise **inconclusive**.
- **Counted cells:** K2a cells need a constant-label rate ≤ 90%.
- **Caveat, stated now:** English words in the input overlap lexically with the English target, so K2b can rise for
  lexical reasons alone, as the M4b layer-0 observation showed. A positive K2b is therefore weak evidence about meaning.

**K3: human correction barely changes natural.** Human-corrected natural vs Gemini natural, on the 200 sentiment
items, per informative model.
- **Holds** if the 95% paired-bootstrap CI of (corrected − Gemini) accuracy lies within ±5 points in every
  informative model.
- **If it does not hold,** Gate 1's natural-romanization result is reported with both versions.
- Secondary: the same comparison on the 300 SIB items.

---
## 2026-10-16 — M4b robustness check (registered above): the M4b statuses are robust
Script `scripts/m4b_robustness.py`; outputs `results/m4b_robustness/{summary.csv, verdict.json, items.npz}` and log
`results/m4b_robustness.log`. CPU only, about 25 min. Test half n = 1,005. Layers and hyperparameters were chosen on
the train half.

| model | form | wide-grid ridge (layer, alpha) | Procrustes (layer, k) |
|---|---|---|---|
| Qwen2.5 | native | 0.517 (1, 0.01) | 0.219 (27, 512) |
| Qwen2.5 | ITRANS | 0.529 (1, 0.1) | 0.450 (0, 512) |
| Qwen3.5 | native | 0.961 (7, 0.1) | 0.971 (11, 512) |
| Qwen3.5 | ITRANS | 0.485 (3, 0.1) | 0.480 (1, 512) |
| Sarvam-1 | native | 0.899 (26, 0.1) | 0.921 (24, 512) |
| Sarvam-1 | ITRANS | 0.380 (24, 0.1) | 0.449 (19, 512) |
| Gemma 4 | native | 0.977 (8, 0.1) | 0.986 (8, 512) |
| Gemma 4 | ITRANS | 0.473 (0, 0.1) | 0.583 (0, 512) |

Mapped gap, native − ITRANS [95% CI], with status:

| model | wide-grid ridge | Procrustes | M4b |
|---|---|---|---|
| Qwen2.5 | −0.012 [−0.043, 0.019] closes | −0.231 [−0.269, −0.194] closes | closes |
| Qwen3.5 | 0.477 [0.445, 0.509] persists | 0.492 [0.460, 0.524] persists | persists |
| Sarvam-1 | 0.518 [0.487, 0.551] persists | 0.473 [0.442, 0.505] persists | persists |
| Gemma 4 | 0.504 [0.473, 0.536] persists | 0.403 [0.371, 0.433] persists | persists |

- **By the registered criterion, the M4b verdict is robust.** Every model's status is the same under both
  alternatives, and strong H1 remains inconclusive under each.
- **Wide-grid ridge reproduces M4b exactly.** At the train-half best layers the chosen alpha is inside the old grid
  (0.01–0.1). The 1e-3 edge that Qwen2.5 hit was at other layers.
- **Procrustes always chose k = 512, the top of the grid.** n_fit is about 800 per fold, so k cannot go much higher.
  Read the Procrustes numbers as a lower bound for an orthogonal map.
- **Procrustes beats ridge in some cells.** It does better wherever alignment is already high (native in three
  models), and for ITRANS in Sarvam-1 (+0.07) and Gemma 4 (+0.11, again at layer 0). The ITRANS gains still sit at
  the input end in Qwen3.5 and Gemma 4, as in the M4b observation.
- **Qwen2.5 native is not a rotation of English.** Under Procrustes it reaches only 0.219, against 0.517 with ridge.
  So in Qwen2.5 the native gap "closes" only with a non-orthogonal map.

---
## REGISTRATION — M4b surface baseline and entity/number filter (written 2026-10-17, Aarnav's decision of 2026-10-16; before running)
Script `scripts/m4b_surface.py`. A robustness analysis of M4b, CPU only, on the cached FLORES+ sentence vectors
(`cache/activations/m14full`), with the M4b split (seed 0, test half n = 1,005), folds, alpha grid and train-half
selection unchanged.

**(a) Surface baseline: layer 0.** Layer 0 is the input embeddings, mean-pooled over the sentence. A linear map from
there to English can use only which tokens occur: shared digits, names and Latin loanwords. So mapped retrieval at
layer 0 is the surface-only baseline.
- For each model × form (native, ITRANS) and each map, ridge (M4b, primary) and PCA Procrustes (robustness check):
  - L0 = mapped test retrieval at layer 0, with its hyperparameter CV-tuned on the train half as before.
  - Lb = mapped test retrieval at the train-half-CV-best layer among layers ≥ 1.
  - Gain = Lb − L0, with a paired bootstrap CI (10,000 resamples over test sentences). L0 and Lb get CIs too.
- Rule, per cell: **beyond surface** if the CI lower bound of the gain > 0.10, **surface-level** if the CI upper bound
  < 0.10, otherwise **partial**.
- **Not blind.** The M4b per-layer curves already exist, and the M4b post hoc note said mapped ITRANS does best at
  layers 0–3. So for ITRANS this is a description, not a test. Expectation: native beyond surface and ITRANS
  surface-level in Qwen3.5, Sarvam-1 and Gemma 4.

**(b) Entity/number filter.** A sentence is kept if its English has no digit (0–9) and no capitalised Latin word.
- The first word of the sentence and the pronoun "I" don't count as capitalised.
- Words are maximal runs of A–Z/a–z (apostrophes and hyphens inside a word allowed).
- This is a crude filter for named entities and numbers. A later sentence start inside the same item also removes it,
  which is conservative.
- Reported: the number kept per half, and how many kept native sentences still contain a digit or a Latin letter.

The M4b mapping (ridge, M4b grid) is rerun within the kept sentences:
- train = kept ∩ M4b train half, test = kept ∩ M4b test half;
- folds and CV as in M4b on that train set;
- retrieval among the kept test sentences only.

Reported per model:
- unmapped and mapped retrieval for native and ITRANS;
- the mapped gap native − ITRANS with its CI, and the M4b status rule (persists / closes / partial);
- L0 and the gain, as in (a).

**Size-matched random control.** Retrieval among fewer candidates is easier, and fewer training pairs make the map
weaker. So the same analysis is run on a random subset of the same size per half (seed 3), and both are reported side
by side.

**Prediction (blind; nothing on the subset has been computed):**
- The mapped gap persists (CI lower bound > 0.10) on the filtered subset in Qwen3.5, Sarvam-1 and Gemma 4.
- Mapped ITRANS is lower on the filtered subset than on the size-matched random subset, by more than mapped native is.
  This is reported as the two differences with independent-bootstrap CIs, descriptively.
- If the gap closes on the filtered subset in two or more of those three models, M4b's "persists" is reported as
  dependent on entities and numbers.

---
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
## 2026-10-17 — M4b surface baseline and entity/number filter (registered above)
Script `scripts/m4b_surface.py`, CPU only, about 9 min. Outputs: `results/m4b_surface/{surface.csv, subset.csv,
verdict.json}`; log `results/m4b_surface.log`.

**(a) Surface baseline, full test half (n = 1,005).**
- L0 is mapped retrieval at layer 0. Lb is mapped retrieval at the train-half-CV-best layer ≥ 1.
- Gain = Lb − L0 with a paired 95% CI. Status rule: beyond surface if the CI lower bound > 0.10, surface-level if the
  CI upper bound < 0.10, otherwise partial.

| model | form | ridge L0 → Lb (layer) | ridge gain [CI], status | Procrustes L0 → Lb (layer) | Procrustes gain [CI], status |
|---|---|---|---|---|---|
| Qwen2.5 | native | 0.112 → 0.517 (1) | +0.405 [0.372, 0.438] beyond | 0.131 → 0.219 (27) | +0.088 [0.056, 0.118] partial |
| Qwen2.5 | ITRANS | 0.352 → 0.529 (1) | +0.177 [0.142, 0.212] beyond | 0.450 → 0.403 (1) | −0.047 [−0.081, −0.012] surface |
| Qwen3.5 | native | 0.165 → 0.961 (7) | +0.796 [0.770, 0.821] beyond | 0.184 → 0.971 (11) | +0.787 [0.762, 0.812] beyond |
| Qwen3.5 | ITRANS | 0.245 → 0.485 (3) | +0.240 [0.203, 0.276] beyond | 0.386 → 0.480 (1) | +0.094 [0.060, 0.126] partial |
| Sarvam-1 | native | 0.456 → 0.899 (26) | +0.443 [0.409, 0.476] beyond | 0.492 → 0.921 (24) | +0.430 [0.396, 0.462] beyond |
| Sarvam-1 | ITRANS | 0.406 → 0.380 (24) | −0.026 [−0.065, 0.011] surface | 0.423 → 0.449 (19) | +0.026 [−0.013, 0.065] surface |
| Gemma 4 | native | 0.510 → 0.977 (8) | +0.467 [0.436, 0.499] beyond | 0.574 → 0.986 (8) | +0.412 [0.381, 0.443] beyond |
| Gemma 4 | ITRANS | 0.473 → 0.284 (14) | −0.189 [−0.227, −0.150] surface | 0.583 → 0.259 (14) | −0.324 [−0.362, −0.288] surface |

- **Expectation (not blind): partly met.**
  - Native is beyond surface in Qwen3.5, Sarvam-1 and Gemma 4 under both maps.
  - ITRANS is surface-level in Sarvam-1 and Gemma 4 under both maps.
  - **The exception is Qwen3.5 ITRANS.** It gains +0.24 above layer 0 with ridge (beyond surface) and +0.09 with
    Procrustes (partial). So Qwen3.5 does build something past the surface from ITRANS. It stops at 0.48, against 0.96
    for native.
- **Gemma 4 ITRANS gets worse with depth** (−0.19 ridge, −0.32 Procrustes). Its best mapped value is the layer-0 bag
  of tokens.
- **Layer 0 itself already sits at 0.41–0.58 for ITRANS in Sarvam-1 and Gemma 4.** It is 0.46–0.57 for native in
  those models too. A surface map is strong in these two models whatever the script.

**(b) Entity/number filter.**
- Kept: 369 train and 365 test sentences (734 of 2,009). 13 kept native sentences still contain a digit or a Latin
  letter.
- The size-matched random control has the same counts (seed 3).
- Retrieval is among the 365 test sentences (chance 0.27%). Shuffled-pair control ≤ 0.8% everywhere.

| model | filtered: native / ITRANS mapped | filtered gap [CI], status | random: native / ITRANS mapped | random gap [CI], status |
|---|---|---|---|---|
| Qwen2.5 | 0.258 / 0.301 | −0.044 [−0.099, 0.014] closes | 0.318 / 0.293 | 0.025 [−0.033, 0.082] closes |
| Qwen3.5 | 0.923 / 0.315 | 0.608 [0.556, 0.658] persists | 0.975 / 0.326 | 0.649 [0.597, 0.701] persists |
| Sarvam-1 | 0.841 / 0.285 | 0.556 [0.501, 0.611] persists | 0.855 / 0.304 | 0.551 [0.496, 0.603] persists |
| Gemma 4 | 0.973 / 0.370 | 0.603 [0.548, 0.655] persists | 0.959 / 0.244 | 0.715 [0.666, 0.762] persists |

Filtered minus random, mapped retrieval [independent-bootstrap CI]:

| model | native | ITRANS |
|---|---|---|
| Qwen2.5 | −0.060 [−0.126, 0.005] | +0.008 [−0.058, 0.074] |
| Qwen3.5 | −0.052 [−0.085, −0.022] | −0.011 [−0.077, 0.058] |
| Sarvam-1 | −0.014 [−0.066, 0.038] | −0.019 [−0.088, 0.047] |
| Gemma 4 | +0.014 [−0.011, 0.041] | +0.126 [0.060, 0.192] |

- **Blind prediction 1 (the gap persists on the filtered subset in Qwen3.5, Sarvam-1 and Gemma 4): supported.** It
  persists in all three. It closes in Qwen2.5, as on the full set. So M4b's "persists" does **not** depend on
  entities and numbers.
- **Blind prediction 2 (filtering lowers mapped ITRANS more than native): not supported.**
  - ITRANS drops more than native only in Sarvam-1, by a margin well inside noise.
  - In Gemma 4, mapped ITRANS is *higher* on the filtered subset (+0.126 [0.060, 0.192]), again at layer 0 (0.370 vs
    0.318 for L0 on the random subset).
  - Native loses a little in Qwen3.5 (−0.05).
- **Post hoc reading (not a test).**
  - The M4b note blamed the layer-0 ITRANS signal on shared digits, names and Latin loanwords. This result does not
    support that.
  - Removing sentences with numbers and capitalised names does not weaken it. The layer-0 map is still a
    bag-of-tokens dictionary, but its anchors seem to be ordinary words, not entities.
  - Either way, ITRANS meaning alignment beyond layer 0 stays small except in Qwen3.5. That part of the M4b reading
    stands.

---
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
## 2026-10-17 (written 2026-10-21) — M4c natural romanization in M4 (registered 2026-10-16): refuted, natural is well above ITRANS
`scripts/m4c_natural_flores.py`, run in the detached `m4c_chain.sh`.
- **Romanization** finished 2026-10-17 02:47 IST: 500 sentences, 4 still defective after 3 attempts and excluded, so
  n = 496.
- **Forward pass** 04:59–05:12 IST, started only after E0c had finished. Analysis followed.
- **Outputs:** `results/m4c_natural/{summary.csv, verdict.json}`. Split: 248 train, 248 test.
- **Unmapped** is retrieval on the test half at the train-half best layer, among 248. The all-496 best-layer value is
  in summary.csv.

| model | native unmapped / mapped | ITRANS unmapped / mapped | natural unmapped / mapped |
|---|---|---|---|
| Qwen2.5 | 0.238 / 0.290 | 0.133 / 0.278 | 0.379 / 0.246 |
| Qwen3.5 | 1.000 / 0.952 | 0.190 / 0.282 | 0.512 / 0.323 |
| Sarvam-1 | 0.988 / 0.843 | 0.685 / 0.319 | 0.919 / 0.661 |
| Gemma 4 | 1.000 / 0.944 | 0.444 / 0.254 | 0.710 / 0.407 |

Paired differences [95% CI]:

| model | natural − ITRANS, unmapped | natural − ITRANS, mapped | native − natural, unmapped | native − natural, mapped |
|---|---|---|---|---|
| Qwen2.5 | +0.246 [0.194, 0.302] | −0.032 [−0.093, 0.032] | −0.141 [−0.218, −0.065] | +0.044 [−0.024, 0.109] |
| Qwen3.5 | +0.323 [0.254, 0.391] | +0.040 [−0.032, 0.113] | +0.488 [0.427, 0.548] | +0.629 [0.569, 0.690] |
| Sarvam-1 | +0.234 [0.177, 0.290] | +0.343 [0.262, 0.419] | +0.069 [0.036, 0.105] | +0.181 [0.121, 0.242] |
| Gemma 4 | +0.266 [0.202, 0.331] | +0.153 [0.077, 0.230] | +0.290 [0.238, 0.347] | +0.536 [0.472, 0.601] |

**Registered verdict: refuted.**
- **Part 1, natural ≈ ITRANS (CI within ±0.10, unmapped and mapped, in ≥ 3 of 4 models): not met.**
  - Unmapped, natural − ITRANS is above 0.10 in all 4 models (CI lower bounds 0.18–0.25).
  - Mapped, the CI is within ±0.10 only in Qwen2.5.
- **Part 2, native − natural unmapped CI above 0.10 in Qwen3.5, Sarvam-1 and Gemma 4: not met in Sarvam-1**
  (0.069 [0.036, 0.105]). Met in Qwen3.5 and Gemma 4.
- **Refutation rule** ("natural − ITRANS > 0.10 (CI) in at least 3 models"): met on the unmapped measure, in all 4.
  - The rule did not say which measure counts. Unmapped is M4's primary measure, and part 2 of the rule uses it.
  - On the mapped measure the refutation would hold only in Sarvam-1, and the verdict would be inconclusive. Both
    are stated here.

**Reading:**
- **Natural romanization sits between ITRANS and native.** In Sarvam-1 it is close to native (0.919 vs 0.988).
- **The familiarity prediction treated the two romanizations alike, and that was wrong.** Natural romanization, the
  spelling people actually use online, aligns with English far better than the scholarly ITRANS scheme.
- **Confound (stated, not tested here).** Natural also fragments less than ITRANS, at about the same tokens per word
  as lossy (E0b sentiment items: natural 3.15–4.29, ITRANS 3.94–5.24, lossy 3.21–4.36). So, as for lossy > ITRANS
  (note below), natural > ITRANS cannot separate fragmentation from spelling familiarity.
- **Gate 1 (accuracy) still had native > natural in every model.** Alignment and accuracy agree on the order native >
  natural, except Qwen2.5, where natural aligns better than native unmapped.
- **Mapping hurts at this sample size.** With 248 training pairs the ridge map lowers retrieval below unmapped for
  most cells, so the mapped column is weak evidence here.

---
## 2026-10-21 — Surface baseline for the natural form (addendum registered above)
`scripts/m4c_surface.py`; outputs `results/m4c_surface/{surface.csv, verdict.json}`. M4c sample, n_test = 248, ridge
only.

| model | native L0 → Lb (layer), gain [CI] | ITRANS L0 → Lb (layer), gain [CI] | natural L0 → Lb (layer), gain [CI] |
|---|---|---|---|
| Qwen2.5 | 0.093 → 0.290 (27), +0.198 [0.137, 0.258] beyond | 0.153 → 0.278 (1), +0.125 [0.073, 0.181] partial | 0.177 → 0.246 (1), +0.069 [0.016, 0.125] partial |
| Qwen3.5 | 0.117 → 0.952 (7), +0.835 [0.786, 0.879] beyond | 0.133 → 0.282 (2), +0.149 [0.089, 0.210] partial | 0.137 → 0.323 (7), +0.185 [0.117, 0.254] beyond |
| Sarvam-1 | 0.246 → 0.843 (25), +0.597 [0.532, 0.661] beyond | 0.190 → 0.319 (21), +0.129 [0.056, 0.202] partial | 0.190 → 0.661 (24), +0.472 [0.395, 0.548] beyond |
| Gemma 4 | 0.202 → 0.944 (7), +0.742 [0.685, 0.794] beyond | 0.254 → 0.210 (8), −0.044 [−0.113, 0.024] surface | 0.230 → 0.407 (8), +0.177 [0.101, 0.254] beyond |

- **Natural goes beyond the surface in Qwen3.5, Sarvam-1 and Gemma 4.** In Sarvam-1 it gains +0.47, at the same depth
  as native (layer 24 vs 25).
- **ITRANS is surface-level in Gemma 4 and partial elsewhere.** The native gains are the largest in every model.
- **Small-sample caveat.** With 248 training pairs, layer-0 maps are much weaker than in M4b's 1,004-pair fit. For
  example, Gemma 4 ITRANS L0 is 0.254 here and 0.473 there. So two ITRANS cells move from surface-level or beyond
  (M4b) to partial here. Compare forms within this table, not across to the M4b table.

---
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
## 2026-10-21 — Chain incident: the Kanglish chain and watcher ended during laptop sleep
- **What stopped.** The Kanglish chain's last heartbeat was 2026-10-17 15:14:28 IST. The laptop went to sleep at
  about 15:15 and stayed asleep, apart from brief wakes, until 10-20 13:31 and again 10-21 12:33.
  - Both scheduled tasks had ended: Kanglish with code 0x40010004, the watcher with code 4.
  - The watcher ended too, so it never marked the status DEAD, and the file kept saying WAITING. No reboot happened
    (last boot 10-14).
  - The Task Scheduler event log is disabled, so the exact cause is not verified.
- **What finished first.** M4c and E0c were DONE before this. The drafts had reached 849 of 1,000 by 10-17 13:28,
  using the 10-16 and 10-17 quota windows. The 10-18 to 10-20 windows were lost.
- **Fix (2026-10-21).**
  - `scripts/detach.ps1` now also restarts each task at logon and 1 minute after every wake from sleep (System log,
    Power-Troubleshooter event 1).
  - A second instance is never started while one is running.
  - A chain whose status is DONE exits at once.
  - The Kanglish chain and the watcher were relaunched at 22:21 IST on 10-21, in the open 10-21 quota window.
  - Not yet tested across a real sleep.

---
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
## 2026-10-22 — Per-layer English alignment, natural vs native vs ITRANS, M4c test half (post hoc descriptive, 2026-10-22, no verdict)
Approved by Aarnav for the paper figure. `scripts/m4c_curves.py`, CPU only (cached sentence vectors, no model loaded).
Output `results/m4c_curves/curves.json`; figure `paper/figures/F_alignment_curves.{pdf,png}`.
- **What:** unmapped retrieval acc@1 against English at every layer for Qwen3.5-2B, Sarvam-1 and Gemma 4 E2B, forms
  native, ITRANS and natural, all on the same 248 M4c test-half sentences (M4c split, seed 0; train-half centering;
  248 candidates). This is M4c's `unmapped_test` measure computed at every layer instead of only at the train-half
  best layer.
- **Check:** at each form's train-half best layer the curve reproduces `results/m4c_natural/summary.csv`
  `unmapped_test` exactly in all 9 model × form cells (asserted in the script). No new number is reported here
  beyond the curves themselves.
- **Why:** the earlier figure drew native and ITRANS on all 2,009 sentences (Gate 2) and could not draw natural, which
  exists only for the M4c sample. The main figure now uses matched sentences for all three forms. The 2,009-sentence
  native/ITRANS curves are kept as an appendix figure, `paper/figures/F_alignment_curves_2009.{pdf,png}` (from
  `results/m14_full/<model>/m4.json`).
- **No verdict.** Nothing here tests or changes a registered prediction.

---
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
## 2026-10-22 — Annotation page v2 tested (not distributed)
`annotation/annotate_v2.html` (built by `scripts/k_annotation.py page` from `annotation/template_v2.html`; the v1 page
was removed so it cannot be distributed by mistake). Tested in Chrome on a localhost copy, with the File System Access
write path driven programmatically (the native file pickers cannot be automated); test data deleted afterwards.
- Second-annotator mode lists the 40 blind items first. On a blind item: English, drafts, ratings and Reset are hidden;
  both boxes start empty; saving with an empty box is refused; the saved row has `condition = blind`, empty drafts and
  ratings.
- Non-blind double items and the primary annotator's view (including of the 40 blind items) are unchanged: drafts
  shown, ratings required, `condition = draft`.
- CSV round trip exact for both conditions (quotes, commas, newlines, Kannada), new column `condition`.
- Still to do before distribution: Aarnav's hand fixes for flores-993 and indicsentiment-test-245
  (`data/annotation/drafts_manual_v1.jsonl`), then rebuild the page; the K3 rating page (built after the second
  annotator's blind texts exist); Aarnav to confirm the proposed K3 decision rule.

---
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
## 2026-10-22 — Share of English words in natural, lossy and ITRANS (post hoc descriptive, 2026-10-22, no verdict)
Requested by Aarnav. `scripts/english_share.py`, CPU only (text only, no model). Outputs
`results/english_share/{shares.csv, wordlist.json}` (commit 7129058 + this script).
- **Samples (matched):** the 496 retained M4c FLORES+ sentences; the 198 sentiment items with a clean natural
  romanization (2 of 200 are `natural_defective` and are dropped from every form).
- **Wordlist:** wordfreq 3.1.1 (Speer et al., https://github.com/rspeer/wordfreq), English "best" list. Primary:
  words with Zipf frequency ≥ 3 (29,269 words); sensitivity: Zipf ≥ 4 (7,223). A word (whitespace token, edge
  punctuation stripped, must contain an ASCII letter) is English if its lowercased form is in the list. ITRANS is also
  given "as written" (any uppercase letter = not English, since ITRANS uppercase marks Kannada phonemes).
- **Named entities:** no NE list exists in the repo, so proper nouns are approximated by capitalization in natural
  (capitalized, not sentence-initial). "No proper nouns" drops those words from natural and, best effort, drops the
  same lowercased word from lossy and ITRANS of that item.
- Share = English words / words, pooled; 95% CI from a paired bootstrap over items (10,000, seed 0).

| sample | wordlist | variant | natural | lossy | ITRANS | natural − lossy [95% CI] |
|---|---|---|---|---|---|---|
| M4c 496 | Zipf ≥ 3 | all words | 0.103 | 0.054 | 0.049 (as written 0.012) | +0.049 [+0.041, +0.057] |
| M4c 496 | Zipf ≥ 3 | no proper nouns | 0.096 | 0.051 | 0.046 | +0.045 [+0.037, +0.053] |
| M4c 496 | Zipf ≥ 4 | all words | 0.065 | 0.032 | 0.029 (as written 0.005) | +0.033 [+0.026, +0.041] |
| M4c 496 | Zipf ≥ 4 | no proper nouns | 0.060 | 0.030 | 0.027 | +0.030 [+0.023, +0.038] |
| sentiment 198 | Zipf ≥ 3 | all words | 0.110 | 0.041 | 0.038 (as written 0.007) | +0.068 [+0.057, +0.080] |
| sentiment 198 | Zipf ≥ 3 | no proper nouns | 0.108 | 0.041 | 0.038 | +0.067 [+0.055, +0.078] |
| sentiment 198 | Zipf ≥ 4 | all words | 0.065 | 0.024 | 0.021 (as written 0.003) | +0.041 [+0.031, +0.051] |
| sentiment 198 | Zipf ≥ 4 | no proper nouns | 0.064 | 0.024 | 0.021 | +0.040 [+0.029, +0.050] |

(Per-form CIs and natural − ITRANS are in `shares.csv`.)
- **Caveat, read before using the numbers:** lossy and ITRANS contain no deliberate English, so their share is a
  baseline of chance collisions between romanized Kannada and the English list (`i`, `a`, `ella`, `ne`, `ide`, `matte`).
  In natural on M4c, the largest contributors to the excess are Kannada words in natural spelling that happen to be in
  the list (`ee` = ಈ "this", 65; `na` 21; `aa` 19), not English loans; real loans and names appear lower down
  (`police`, `british`, `august`, `french`). On sentiment, real English loans contribute visibly (`air`, `collar`,
  `application`, `wifi`, `cooler`, `play`, `home`). Top-25 matched words per form are in `wordlist.json`. So the
  natural − lossy difference is an upper bound on "more English words", more so on M4c.
- **No verdict.** Nothing here tests or changes a registered prediction (L3 stays as registered).

---
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
## 2026-10-22 — K3 addendum: independent rater, TOST (Aarnav; before any blind item is written)
Amends the 2026-10-22 K3 registration; replaces Claude Code's proposed ±0.5 / 95% CI rule.
- **Primary rater:** a Kannada reader familiar with informal romanized Kannada who has seen **neither the Gemini
  drafts nor the human versions** (name TBD; not Aarnav, not the second annotator). Each of the 40 blind items shows the
  native sentence and both versions, **source hidden, order randomized** (seed 3, fixed per item); naturalness 1–5 for
  each.
- **Primary measure:** mean paired difference (human − Gemini). **Equivalence (TOST), margin ±0.5, 90% CI** (bootstrap
  percentile, 10,000 over items; t-based TOST p values alongside): "about as natural" if the 90% CI lies within
  (−0.5, +0.5); otherwise not shown equivalent, and a difference is reported if the 95% CI excludes 0 (with sign).
- **If no independent rater is available, K3 is reported descriptively (mean paired difference with 90% CI, chrF
  Gemini vs human with the human-human reference noted as biased upward); no verdict.**

---
## 2026-10-22 — English-word share: sensitivity excluding words of ≤ 3 characters (post hoc descriptive, 2026-10-22, no verdict)
Addendum to the English-share entry above (Aarnav's request). `scripts/english_share.py`, variant "words of 4+
characters": words of 3 characters or fewer are dropped from every form and from the denominator; Zipf ≥ 3 list; same
samples, bootstrap and seed (earlier rows of `results/english_share/shares.csv` reproduce exactly).

| sample | wordlist | variant | natural | lossy | ITRANS | natural − lossy [95% CI] |
|---|---|---|---|---|---|---|
| M4c 496 | Zipf ≥ 3 | words of 4+ characters | 0.071 | 0.022 | 0.018 | +0.049 [+0.042, +0.057] |
| sentiment 198 | Zipf ≥ 3 | words of 4+ characters | 0.084 | 0.018 | 0.015 | +0.066 [+0.054, +0.078] |

The difference is almost unchanged (+0.049 and +0.066 vs +0.049 and +0.068 with all words) while lossy's chance
baseline drops by more than half. In natural, the top matched 4+ character words are now mostly real English loans and
names (M4c: `police`, `british`, `august`, `french`, `website`, `internet`, `station`; sentiment: `collar`,
`application`, `wifi`, `cooler`, `bluetooth`), with some remaining collisions shared with lossy (`ella`, `matte`);
top-25 lists in `results/english_share/wordlist.json` (`top_matched_words_zipf3_4plus_chars`). This weakens the
earlier caveat that the M4c excess is mostly short Kannada words: those words inflate natural's share, but natural −
lossy survives their removal. No verdict.

---
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
## 2026-10-22 — NC1 deviations; gate approved (Aarnav)
- **(c) re-split share below the registered gate:** on the M4c pilot sentences (c) re-split 79.4% (262/330) of
  multi-token words, below the registered 80% (sentiment 87.7%). Cause: vocabulary — for the remaining words the
  canonical split is the only k-piece segmentation at the canonical count. Aarnav approved the gate; NC1 proceeds as
  registered, threshold unchanged.
- **Sarvam-1 byte fallback:** 36 of 135,816 lossy tokens are byte-fallback tokens (non-ASCII punctuation in the sources);
  units containing them stay canonical in every condition and are flagged `atomic_token` (other tokenizers: 0).

---
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
## 2026-10-23 — A6: largest family model for 4-bit accuracy-only runs on the RTX 3070 (information only; no download, nothing run)
Parameter counts from the HF safetensors metadata, architectures from each `config.json` (2026-10-23). bitsandbytes
0.50.2 is installed in `.venv` (native Windows wheels since 0.43); its CUDA kernels are **not yet tested on this
machine**. GPU: 8.0 GiB. Weight memory estimated as NF4 with double quantization (~0.52 bytes per Linear parameter),
input embeddings and lm_head kept in bf16 (transformers default), vision/audio towers not loaded (as for Gemma 4 E2B
now). These are estimates, not measurements; a pilot would replace them.

| family | candidate | params | est. GPU weights at 4-bit | fits 8 GB? |
|---|---|---|---|---|
| Qwen3 | Qwen3-8B (untied embeddings) | 8.19B | ~6.1 GB (~4.8 GB with the input embedding on CPU) | yes, ~6.6 GB peak with activations and CUDA context |
| Qwen3 | Qwen3-14B | 14.77B | ~9.9 GB (~8.4 GB embedding on CPU) | no |
| Qwen3.5 | Qwen3.5-9B (untied, vision tower 27 layers) | 9.65B | ~7.8 GB; ~5.7 GB with the input embedding on CPU | only with the embedding on CPU (as CPULookup does for Gemma's PLE) |
| Qwen3.5 | Qwen3.5-4B (tied) | 4.66B | ~3 GB | yes |
| Gemma 4 | Gemma 4 12B (tied, 262k vocab, 48 layers) | 11.96B | ~7.5 GB | no (no headroom) |
| Gemma 4 | Gemma 4 E4B (PLE table on CPU) | 8.0B | ~3.5–4 GB | yes |
| Sarvam | sarvam-m (24B) | 23.57B | ~12.5 GB | no; no general Sarvam LM between sarvam-1 (2.5B) and sarvam-m |

Runtime (extrapolated from the NC1 log, not measured at 4-bit): the 2B bf16 models scored sentiment + XNLI + SIB for 3
conditions in 24–30 min. With ~4× the parameters and bitsandbytes 4-bit dequantization overhead, an 8–9B model is
estimated at **4–8× that: ~35–80 min per form** over the three tasks. A pilot (50 items, one form) would replace this.
Note: running any of these conflicts with the 2026-10-23 scope rule "no models larger than our current set" and needs
Aarnav's explicit approval.

---
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
## 2026-10-23 — Dakshina: HF mirror verified against the official release; A1 rerun on the official files
- **Official source:** https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar (Dakshina v1.0,
  github.com/google-research-datasets/dakshina), CC BY-SA 4.0. MD5 of the full download matches the published hash.
- **Mirror vs official** (`kn.romanized.rejoined.tsv`): 10,000 vs 10,000 strings, identical row by row (native and
  romanized); seeded spot check (seed 5) 50 of 50 identical. Splits: dev 5,000 + test 5,000; 23 duplicate native strings.
- **A1 rerun:** `scripts/nc1_posthoc.py` now reads the official file. `piece_frequency_independent.csv`,
  `decomposition.csv` and `ladder_piece_familiarity.csv` are byte-identical to the mirror-based run, so every A1–A3
  number above stands.
- Hindi (`hi`): 10,000 strings, same procedure and splits, also native-speaker romanizations.

---
## 2026-10-23 — Phase B: replacements, page rebuild, rater page, instruction sheets, datasheet (no annotation yet)
- **Replacements (deviation logged above):**
  - **flores-993 → flores-546.** Pool: FLORES+ in SIB-200 ∩ M4b test half, minus items_v1 and the M4c 500; 167
    candidates; seed [4, 0]; accepted on draw 1.
  - **indicsentiment-test-245 → indicsentiment-test-295.** Pool: IndicSentiment test, minus items_v1; 798 candidates;
    seed [4, 1]; accepted on draw 1; same label (1), so the 100/100 label balance holds.
  - Natural and Kanglish drafts use the identical prompts, attempt 1, and neither is defective. Draws are logged in
    `data/annotation/replacement_draws_v1.jsonl`; drafts in `drafts_replace_v1.jsonl`; items in `items_v2.jsonl`
    (`items_v1.jsonl` is unchanged).
  - Neither replaced item was double or blind, so neither replacement is.
  - The sentiment replacement has no E0/E0b scores (the E0 sample is unchanged), so annotation-based scoring on the 200
    sentiment items covers 199 E0 items plus 1 new item.
  - Every FLORES pool item is also in the full-set SIB-200 and M4 evaluations, so "not in any sample" means not in the
    annotation set or the M4c 500.
- **Page rebuilt** (`annotation/annotate_v2.html`): 500 items, 40 blind, **0 flagged drafts**, 0 missing drafts. The
  CSV round trip was retested with the page's own `csvCell`/`toCSV`/`parseCSV` (Node) over all 500 items, using quotes,
  commas, LF/CRLF newlines and Kannada in the answers: 500 rows (40 blind), 0 mismatches in the page parser, 0 in pandas
  (`utf-8-sig`). The template is unchanged since the 2026-10-22 Chrome test.
- **Rater page for Rater C:** `python scripts/k_annotation.py rater <B.csv>` builds `annotation/rate_k3_v1.html` only
  when B's CSV has from-scratch texts for all 40 blind items (tested: 10 of 40 is refused). It shows the native sentence
  and, for natural and Kanglish, B's text and the Gemini draft as "Version 1/2"; the order is drawn once with seed 3,
  and the key is in `data/annotation/k3_rater_key_v1.json`, never in the page. Rating: naturalness 1–5 only; CSV
  download. A test build from synthetic data (scratchpad only) gave 80 pairs, the script compiles, and the words
  "human"/"Gemini" do not occur in the page. The real page does not exist yet.
- **Instruction sheets:** `annotation/instructions/{annotator_A, annotator_B, rater_C}.md`, each under one page.
- **Datasheet draft:** `data/annotation/DATASHEET.md`. Open items: the IndicSentiment license at source, the Gemini
  output terms, annotator details, release.
- **K3b:** drafted (`docs/drafts/K3b_prereg_draft.md`); not registered, not run.

---
## PRE-REGISTRATION — K3b: Gemini vs native-speaker natural romanization on Dakshina Kannada (written 2026-10-23 01:00 IST, Aarnav-approved with one change; before any Dakshina text is sent to Gemini)
Script: `scripts/k3b_dakshina.py` (written after this registration). Gemini quota: runs after the Hindi drafts below.
- **Data:** Dakshina v1.0 official release (MD5-verified 2026-10-23, CC BY-SA 4.0),
  `kn/romanized/kn.romanized.rejoined.tsv`: 10,000 Kannada Wikipedia strings romanized by native-speaker annotators.
  No overlap with any evaluation item.
- **Sample:** every native string occurring more than once is dropped (all copies), as is every string with fewer than
  3 native words (counts logged). From the rest, 500 are drawn with `numpy.random.default_rng(6)`.
- **Gemini primary:** `gemini-3.5-flash-lite`, prompt `natural_romanization_v1` (identical to our natural drafts),
  temperature 0, cached. A defective output (`defective()`: any Indic-script character or new non-ASCII character)
  gets attempts 2–3; strings still defective are excluded and counted.
- **Resample reference:** 200 of the 500 (`default_rng(7)`) get two more samples, G1 and G2, at temperature 1.0 with
  the same prompt. A defective sample is not retried; that string drops out of the reference.
- **Normalization:** both sides are lowercased. Letters are `[a-z]`.
- **Descriptive only (no rule):** chrF (sacrebleu, char order 6, word order 0, β = 2) of Gemini vs human (500, mean with
  bootstrap 95% CI) and of G1 vs G2 (≤ 200).
- **Statistics with the rule:**
  - (1) vowel doubling: occurrences of aa, ee, ii, oo, uu (non-overlapping, left to right) per 100 letters;
  - (2) h-digraph use: kh, gh, chh, jh, th, dh, ph, bh per 100 letters ("chh" counted once, not also as "ch"+"h");
  - (3) English-word share: words of 4+ letters in the wordfreq English list with Zipf ≥ 3 (`scripts/english_share.py`
    `words()` and list), as a share of words.
  - Each is pooled over strings: R = (Σ count_Gemini / Σ units_Gemini) / (Σ count_human / Σ units_human), with paired
    bootstrap CIs over strings (10,000; seed 0).
- **Decision rule:**
  - Per statistic: **matches** if the 90% CI of R lies within [0.80, 1.25]; **differs** if the 95% CI excludes 1 and
    the 90% CI is not within [0.80, 1.25]; otherwise **inconclusive** (also if the human pooled rate is 0).
  - **K3b holds** only if all three statistics match. **K3b refuted** if any differs (named with direction). Otherwise
    **inconclusive**.
- **Limitations stated now:**
  - Dakshina is formal Wikipedia text, romanized under the annotators' own instructions.
  - "th"/"dh" also mark dental consonants, so (2) is h-digraph use, not aspiration.
  - The temperature-1.0 reference likely overstates Gemini's everyday variation.

---
## PRE-REGISTRATION — Hindi natural romanization drafts and H-Hindi (written 2026-10-23 01:00 IST, Aarnav's design; before any Hindi draft or Hindi model output exists)
Scripts: `scripts/h_hindi.py` (written after this registration), chains `scripts/h_drafts_chain.sh` (Gemini, then
K3b) and `scripts/h_gpu_chain.sh` (GPU). Outputs in `results/h_hindi/`.

### Data (checked 2026-10-23 before registration; no model run)
- **FLORES+ `hin_Deva` dev + devtest:** 2,009 sentences, the same indices as Kannada.
- **IndicSentiment `data/test/hi.json`** (revision dc8f3f66886531c6897fedffca1e938a68fc5013): 1,000 rows, row-aligned
  with `kn.json`. English review and label are identical in all 1,000 rows, so the ids `indicsentiment-test-{row}` are
  shared.
- **SIB-200 `hin_Deva`** (same revision as Kannada): 1,004 items, the same index ids and topic labels. Native text is
  taken from FLORES+ by index, as for Kannada (SIB's own Hindi text equals FLORES+ in 917 of 1,004).
- **Items:**
  - the 200 Kannada E0 sentiment ids;
  - SIB 1,004;
  - the M4c rows: the same 500 FLORES indices, 496 retained by the Kannada mask.

### Forms
- **native:** Devanagari, NFC.
- **ITRANS (lossless):** the project's ITRANS scheme generated for Devanagari (`itrans_for(SCRIPTS["hin_Deva"])`).
  Encoded per sentence: it round-trips exactly on 2,009/2,009 FLORES+ and 1,000/1,000 sentiment texts. Per-word encoding,
  as used for Kannada FLORES, fails on 13 Hindi sentences.
- **lossy:** `to_lossy(text, "hin_Deva")`, the same rule table as Kannada with no change:
  - long → short vowels; retroflex → dental; aspirated → unaspirated;
  - anusvara → m before labials or at a word end, else n; chandrabindu (.N) → n;
  - nukta letters: क़ → k, ख़ → k, ग़ → g, ड़/ढ़ → d, य़ → y; फ़ → f and ज़ → z are kept;
  - avagraha dropped; then lowercased.
  - Not adapted: the Hindi inherent schwa is kept (for example सोमवार → "somavara"), because the Kannada rules have no
    schwa deletion. Hindi lossy is therefore further from natural Hindi than Kannada lossy is from natural Kannada.
- **natural:** Gemini drafts, `gemini-3.5-flash-lite`, temperature 0, cached.
  - Prompt `natural_romanization_hi_v1` is `natural_romanization_v1` with "Kannada" replaced by "Hindi" (3
    occurrences), verbatim:
    > Romanize the following Hindi sentence the way an ordinary Hindi speaker would type it in Latin script on a phone:
    > informal spelling, no diacritics, no special symbols. / Keep every word and the original word order. Do not
    > translate, explain, add or remove anything. Keep numbers, punctuation and any English words as they are. /
    > Output only the romanized sentence. / Hindi sentence: / {text}
  - Drafted for the 496 M4c sentences and the 200 sentiment items.
  - Same defect check and retries as Kannada: `defective()` (any Indic-script character, U+0900–U+0DFF, or new
    non-ASCII character); attempts 2–3; still defective → excluded and counted.
  - SIB natural is the M4c overlap (Kannada `natural257`) minus Hindi defects.

### Baseline gate (automatic, fixed now)
- **Accuracy:** a model counts for Hindi accuracy if its native Hindi accuracy CI excludes chance, lying above it, on
  BOTH sentiment 200 (0.5) and SIB 1,004 (1/7). Accuracy is the calibrated primary rule with bootstrap 95% CI (10,000).
- **Retrieval:** a model counts for Hindi retrieval if its native Hindi unmapped retrieval exceeds 0.5. This is acc@1
  on the M4c 248 test half at the train-half best layer, the same split and code as Kannada.
- **Counted for H1:** a model must pass the Hindi gate and also be counted for that measure in the Kannada ladder
  (retrieval: Qwen3.5, Sarvam-1, Gemma 4; accuracy: Qwen3, Qwen3.5, Sarvam-1, Gemma 4).
  - Qwen2.5 is reported, never counted.
  - Qwen3 has Hindi retrieval reported only, since there is no Kannada retrieval for it; its English M4c vectors are
    computed for this.
- Models failing the gate are reported, not counted.

### H1 (prediction): the native − natural gap is smaller for Hindi than for Kannada
- **Statistic per counted model:** d̄ = mean over items of [(Kannada native − Kannada natural) − (Hindi native −
  Hindi natural)], paired over the same item ids; 95% paired bootstrap CI (10,000; seed 0). Per-item scores are
  retrieval hit (0/1) or correctness (0/1, calibrated primary rule).
- **Measures:**
  - **Retrieval:** item set D = Kannada-retained ∩ Hindi-natural-clean M4c rows. Every form in both languages is
    recomputed on D with the M4c split restricted to D (train ∩ D, test ∩ D, folds as the ladder). Unmapped acc@1 on
    test ∩ D, with the best layer chosen on the train half per form and language. If no Hindi draft is defective, the
    Kannada values equal the ladder's.
  - **Sentiment:** the 198 clean Kannada natural ids ∩ Hindi-clean (n reported).
  - **SIB:** the 257 M4c-overlap ids ∩ Hindi-clean (n reported).
- **Calibration:** contextual calibration (mean of "N/A", "", "[MASK]") from each language's own run. The raw
  fallback is decided on the English rows of each model × task already scored for Kannada (identical English items).
- **Significance:** two-sided bootstrap p = 2·min(P(d* ≤ 0), P(d* ≥ 0)), floor 1/10,000, Holm-adjusted within each
  measure over its counted models. A model is positive if Holm p < 0.05 and d̄ > 0. Holm decides when it disagrees
  with the raw CI.
- **Verdict per measure:**
  - **Effect (H1 supported on that measure)** if positive in ≥ 2 of 3 counted retrieval models, or in ≥ 3 of 4 counted
    accuracy models (sentiment and SIB each separately).
  - If fewer models pass the gate: all but one, minimum 2. With fewer than 2 counted models the measure is "not
    testable".
  - **Refuted** on a measure if no effect. No pooled verdict across measures.
- **Exploratory, no prediction:** the same difference of gaps for native − ITRANS, on the same item sets.
- **Caveat stated now:** Hindi native performance is likely higher overall, so ceiling effects can shrink Hindi gaps.
  Native accuracy per language is reported next to every gap.
- **Ordering rule:** H1 is computed only after natural Hindi is scored (and its vectors computed) for every counted
  model.

### Run plan (overnight, detached, one model load at a time)
- **GPU, 5 models:** Hindi native, ITRANS and lossy on sentiment 200 and SIB 1,004. M4c 500-row sentence vectors for
  native, ITRANS and lossy, plus English for Qwen3. Tokens per word for every form, model and dataset. Then the gate.
- **Natural Hindi** (vectors and scores) runs when the drafts are complete.
- **Checks that stop the chain with a status file:**
  - data alignment as above;
  - vector arrays have the Kannada layer count and no NaN;
  - score files have the expected row counts and no NaN log-probs;
  - every natural draft is clean or excluded.
- **Estimate** (from the Kannada logs): forward about 15 min, scoring about 2.5 h for 3 forms × 5 models, natural about
  1 h once drafted. Drafts: about 700 Gemini requests plus retries (about 1 h). K3b follows: about 900–1,500 requests,
  likely over the 12:45 IST reset.

### H-Hindi — clarification and addendum (written 2026-10-23 12:05 IST, Aarnav's text; before natural Hindi results exist)
Status when written: Hindi natural drafts 486/696 (quota stop); no natural Hindi output has been scored or vectorized.
The native/ITRANS/lossy Hindi runs, tokens per word and the baseline gate already exist (`results/h_hindi/gate.json`).
1. **Counted models.** A model counts for H1 on a measure only if it passes the baseline in BOTH languages for that
   measure. Qwen2.5 passes the Hindi gate but is excluded: its native Kannada is at floor, so its Kannada gap is
   uninterpretable. Qwen3 is excluded from retrieval (no Kannada retrieval count). Counted: accuracy Qwen3, Qwen3.5,
   Sarvam-1, Gemma 4; retrieval Qwen3.5, Sarvam-1, Gemma 4. (Same lists the gate step already applied.)
2. **Defective drafts.** Items with a defective natural draft in EITHER language are dropped from BOTH languages for
   that measure: retrieval D = Kannada-retained ∩ Hindi-clean M4c rows; sentiment = Kannada-clean ∩ Hindi-clean ids;
   SIB = the M4c-overlap ids (Kannada-clean by construction) ∩ Hindi-clean. n is reported per measure.
3. **Secondary analysis** (registered now, reported with H1, no separate verdict):
   - (a) **English-word share** of natural Hindi vs natural Kannada on the same item ids (each measure's H1 item set).
     A word is English if, lowercased with edge punctuation stripped (`english_share.words()`), it is longer than 3
     characters and in the wordfreq English list with Zipf ≥ 3. Per-item share = English words / words. Statistic:
     mean over items of (Hindi share − Kannada share), with a paired bootstrap 95% CI (10,000; seed 0). No proper-noun
     filter.
   - (b) **Loan-free H1:** H1 recomputed exactly as registered (same statistic, Holm within measure over the counted
     models, same counting rule) on the items whose natural text has zero such English words in BOTH languages.
     For retrieval, D is restricted further and the M4c split restricted to it, with the layer re-chosen on its train
     half. n is reported. Its rule outcome is descriptive only.
   - **Interpretation fixed now:** if H1 holds on a measure on the full set but not on the loan-free set, it is
     reported as possibly driven by English loans.
4. **Primary emphasis.** Hindi native sentiment is near ceiling (0.925–0.990 across the five models), so H1 is
   interpreted mainly from SIB and retrieval; sentiment is reported with the ceiling caveat. The registered decision
   rule is unchanged.

---
## PRE-REGISTRATION — K3b-hi: Gemini vs native-speaker natural romanization on Dakshina Hindi (written 2026-10-23 12:05 IST, Aarnav's design; before any Dakshina Hindi text is sent to Gemini)
- **Design and rule:** identical to K3b (Kannada) above: same filters (duplicate native strings dropped, all copies;
  strings with fewer than 3 native words dropped), 500 strings drawn with `default_rng(6)`, resample subset of 200 with
  `default_rng(7)` and G1/G2 at temperature 1.0, same defect check and retries, same three statistics, same pooled
  ratio with bootstrap CIs, same [0.80, 1.25] rule, chrF descriptive only. K3b-hi holds only if all three match.
- **Data:** Dakshina v1.0 official release (MD5-verified 2026-10-23), `hi/romanized/hi.romanized.rejoined.tsv` (10,000
  rows, native Devanagari TAB native-speaker romanization).
- **Prompt:** `natural_romanization_hi_v1` (the K3b prompt with only the language name changed; the same prompt as the
  Hindi drafts above), `gemini-3.5-flash-lite`, temperature 0 for the primary draft.
- **Quota priority:** lowest. It runs only after the Hindi drafts and K3b (Kannada) are complete, in its own chain.
- **Outputs:** `results/k3b_hi/`. Separate verdict from K3b; no pooled verdict.
- **Limitation stated now:** "th"/"dh" and the h-digraphs mark aspiration and dentals differently in Hindi practice,
  so (2) remains h-digraph use, not aspiration; Hindi Wikipedia text has more English and Perso-Arabic loans.

---
## 2026-10-23 — H-Hindi results (registered 01:00 IST + 12:05 IST addendum)
Commit 7b4e869 (code); outputs `results/h_hindi/{gate.json, tokens_per_word.csv, h1.csv, h1_verdict.json,
exploratory_itrans.csv, h1_secondary.json, h1_loanfree.csv}`. GPU chain finished 14:16 IST; no failed check.
- **Drafts:** 696/696 Hindi natural drafts; 4 still defective after 3 attempts (flores-114, flores-1465, flores-1606,
  indicsentiment-test-846), excluded. Item sets: retrieval D = 493 rows (246 test), sentiment n = 197, SIB n = 256.
- **Gate:** all five models pass (Hindi native sentiment 0.895–0.990, SIB 0.660–0.781, retrieval 0.698–1.000). Counted:
  retrieval Qwen3.5, Sarvam-1, Gemma 4; accuracy Qwen3, Qwen3.5, Sarvam-1, Gemma 4.

### H1 (d̄ = Kannada native−natural gap minus Hindi gap; 95% paired bootstrap CI; Holm within measure)
| measure | model | Kn native | Kn natural | Hi native | Hi natural | d̄ [95% CI] | Holm p | positive |
|---|---|---|---|---|---|---|---|---|
| retrieval (n=246) | Qwen3.5 | 1.000 | 0.516 | 0.992 | 0.947 | 0.439 [0.370, 0.508] | <0.001 | yes |
| | Sarvam-1 | 0.988 | 0.919 | 0.992 | 0.939 | 0.016 [−0.012, 0.045] | 0.311 | no |
| | Gemma 4 | 1.000 | 0.711 | 1.000 | 0.980 | 0.268 [0.207, 0.329] | <0.001 | yes |
| SIB (n=256) | Qwen3 | 0.668 | 0.371 | 0.660 | 0.531 | 0.168 [0.086, 0.250] | <0.001 | yes |
| | Qwen3.5 | 0.699 | 0.457 | 0.723 | 0.633 | 0.152 [0.082, 0.223] | <0.001 | yes |
| | Sarvam-1 | 0.750 | 0.727 | 0.758 | 0.723 | −0.012 [−0.074, 0.051] | 0.772 | no |
| | Gemma 4 | 0.758 | 0.543 | 0.773 | 0.734 | 0.176 [0.102, 0.246] | <0.001 | yes |
| sentiment (n=197) | Qwen3 | 0.832 | 0.558 | 0.944 | 0.878 | 0.208 [0.107, 0.310] | 0.001 | yes |
| | Qwen3.5 | 0.736 | 0.721 | 0.924 | 0.944 | 0.036 [−0.046, 0.122] | 0.426 | no |
| | Sarvam-1 | 0.954 | 0.893 | 0.970 | 0.964 | 0.056 [0.010, 0.107] | 0.058 | no (Holm decides; raw CI excludes 0) |
| | Gemma 4 | 0.985 | 0.802 | 0.990 | 0.990 | 0.183 [0.122, 0.244] | <0.001 | yes |

Qwen2.5 (reported, never counted): retrieval −0.431, SIB −0.211, sentiment 0.056.

**Verdicts (registered rule):**
- **Retrieval: effect (H1 supported)**, 2 of 3 positive (needed 2).
- **SIB: effect (H1 supported)**, 3 of 4 positive (needed 3).
- **Sentiment: refuted**, 2 of 4 positive (needed 3). Hindi native sentiment is near ceiling (0.924–0.990); per the
  addendum, sentiment is reported with the ceiling caveat and H1 is interpreted mainly from SIB and retrieval.
- Sarvam-1 is not positive on any measure: its Kannada natural gap is already small (retrieval 0.069, SIB 0.023).

### Secondary (addendum item 3; no separate verdict)
- **(a) English-word share, Hindi natural minus Kannada natural (same ids):** retrieval items 0.104 vs 0.064, +0.040
  [0.031, 0.049]; SIB 0.119 vs 0.069, +0.050 [0.037, 0.063]; sentiment 0.178 vs 0.073, +0.106 [0.089, 0.122]. Natural
  Hindi contains more English words than natural Kannada on every item set.
- **(b) Loan-free H1** (items with zero English words in both languages): retrieval n = 41 test items, 1 of 3 positive
  (Gemma 4, d̄ 0.171 [0.073, 0.293]; Qwen3.5 0.195 [0.024, 0.366], Holm p 0.061); SIB n = 31, 1 of 4 positive (Gemma 4,
  0.355 [0.129, 0.548]); sentiment n = 6, 0 of 4. Rule outcome (descriptive): not met on any measure.
- **Registered interpretation applies:** H1 holds on retrieval and SIB on the full set but not on the loan-free set, so
  both are reported as **possibly driven by English loans**. The loan-free sets are small (41, 31, 6 items), so the
  loan-free outcome is low-powered; d̄ stays positive for 7 of 7 counted retrieval/SIB models (3 of 7 CIs exclude 0
  before Holm; Qwen3.5 SIB lower bound is 0.000). These are stated, not used to override the registered reading.

### Exploratory native − ITRANS (no prediction)
Positive (Holm): retrieval Qwen3.5 0.276, Gemma 4 0.329; Sarvam-1 retrieval −0.122 (Hindi ITRANS gap larger). No
accuracy model is positive; Sarvam-1 is negative on all three (SIB −0.102, sentiment −0.107, retrieval −0.122),
Qwen3.5 sentiment −0.142.

### Tokens per word (Hindi; SIB / natural on M4c 496)
native: Qwen 4.78, Qwen3.5 2.18, Sarvam 1.40, Gemma 1.39. ITRANS 2.52–3.29, lossy 1.90–2.67, natural (M4c) 1.67–2.52;
full table `results/h_hindi/tokens_per_word.csv`.

**Next:** K3b drafts 276/900 (quota stop; resumes 2026-10-24 12:45 IST), then K3b-hi.

---
## PRE-REGISTRATION — H1-LF: H1 at equal English-loan content (written 2026-10-23 15:44 IST, Aarnav's design; FOLLOW-UP REGISTERED POST H1: written after the H1 results and the loan-free secondary above were seen, before any H1-LF statistic, script or draft exists)
The registered H1 verdicts stand unchanged (retrieval effect, SIB effect, sentiment refuted; retrieval and SIB flagged
"possibly driven by English loans"). H1-LF asks whether the H1 effect survives at equal English-word share. Because it
was designed after seeing H1, it is a follow-up test, reported as such. Script `scripts/h1lf.py` (written after this
registration); outputs `results/h1lf/`.

### Option 2 (run now, CPU, existing scores and vectors)
- **Items and outcomes:** the H1 item sets and the same binary outcomes as H1 (retrieval hit at the train-half best
  layer, n = 246 test items; SIB n = 256; sentiment n = 197; calibrated primary rule), per counted model × measure
  (same counted models as H1).
- **Per item:** d_i = (Kannada native − natural)_i − (Hindi native − natural)_i (linear probability);
  δ_i = Hindi natural English share − Kannada natural English share (the addendum definition: lowercased
  `english_share.words()`, words longer than 3 characters in the wordfreq English list with Zipf ≥ 3; share = English
  words / words).
- **Model:** OLS d_i = a + b·δ_i. **Primary statistic: the intercept a** (H1 effect at equal English share), 95% item
  bootstrap CI (10,000; seed 0; percentile). Slope b reported with its CI.
- **Significance and rule (same as H1):** two-sided bootstrap p for a = 2·min(P(a* ≤ 0), P(a* ≥ 0)), floor 1/10,000;
  Holm within measure over the counted models; positive if Holm p < 0.05 and a > 0. Effect on a measure if positive in
  ≥ 2 of 3 counted retrieval models or ≥ 3 of 4 counted accuracy models (same fallback rule). Verdict per measure:
  "effect at equal English share" or "refuted". No pooled verdict.
- **Sensitivity (reported, no verdict):**
  - (a) Continuous outcomes, same regression and bootstrap. Retrieval: at the same chosen layer per language × form,
    after the same train-mean centering, cos(x_i, e_i) − max_{j≠i} cos(x_i, e_j) over the test set (similarity to the
    correct English sentence minus the best distractor). Accuracy: gold margin on the scores used for the calibrated
    primary prediction (avg3-calibrated log-probs, or raw where the English-row fallback applies): s_gold − max over
    other labels.
  - (b) δ binned into tertiles (within each measure's item set, by rank, ties broken by item order), mean d per bin
    with bootstrap 95% CI.
- **Caveats stated now:** δ is mostly positive (Hindi natural has more English), so the intercept partly extrapolates
  to δ = 0; the fraction of items with δ ≤ 0 is reported. The linear-probability model is a linearity assumption.

### Exploratory note (no verdict): native − ITRANS is a loan-free comparison
The exploratory native − ITRANS difference of gaps is positive for retrieval in Qwen3.5 (+0.276) and Gemma 4 (+0.329)
(`results/h_hindi/exploratory_itrans.csv`): the native − ITRANS gap is smaller for Hindi. ITRANS is a deterministic
transliteration of the native script and adds no English loans, so this bears on the loan account. To confirm the
English share is near equal, the English share (same definition) of Hindi ITRANS vs Kannada ITRANS is computed on the
same ids (each H1 item set), mean paired difference with bootstrap 95% CI. Reported, no verdict.

### Option 1 (queued; Gemini quota after K3b, before K3b-hi)
- **Drafts:** natural romanization for all 1,004 SIB items in both languages with the identical prompts and settings
  (Kannada `natural_romanization_v1` on the FLORES+ `kan_Knda` native text, as in E0c; Hindi `natural_romanization_hi_v1`
  on `hin_Deva`; `gemini-3.5-flash-lite`, temperature 0, cached; `defective()`, attempts 2–3, still defective →
  excluded and counted). The overlap items already drafted are the same API calls and come from the cache.
  About 1,500 new requests (several days of quota).
- **Scoring:** the counted accuracy models (Qwen3, Qwen3.5, Sarvam-1, Gemma 4) on natural SIB, all clean items, both
  languages (form `natural1004`), one model load at a time; calibration and fallback exactly as H1.
- **Checks (stop the chain on failure):** row counts and no NaN log-probs; on overlap items whose new draft text is
  identical to the H1 natural text, pred_cal agrees with the H1 natural predictions for ≥ 98% of items per model ×
  language.
- **Statistic and rule:** the H1 statistic (d̄, paired bootstrap, Holm over the 4 counted models, positive if Holm
  p < 0.05 and d̄ > 0, effect if ≥ 3 of 4) on the **loan-free subset of all 1,004**: items clean in both languages
  with zero English words longer than 3 characters (Zipf ≥ 3) in both natural texts. n reported. Verdict: "loan-free
  effect" or "refuted". The same statistic on all clean 1,004 items is reported descriptively.

### Gemini queue order
K3b (Kannada, running) → H1-LF option 1 drafts → K3b-hi.

---
## 2026-10-23 — H1-LF option 2 results (follow-up registered post H1, 15:44 IST)
Script `scripts/h1lf.py opt2`; outputs `results/h1lf/{opt2.csv, opt2_verdict.json, opt2_sensitivity.csv,
opt2_tertiles.csv}`. Check passed: the binary d_i reproduce the H1 n and d̄ for every model × measure.
OLS d_i = a + b·δ_i; a = H1 effect at equal English share (as measured; see the diagnostic below).

| measure | model | n | H1 d̄ | intercept a [95% CI] | Holm p | positive | slope b [95% CI] |
|---|---|---|---|---|---|---|---|
| retrieval | Qwen3.5 | 246 | 0.439 | 0.418 [0.346, 0.496] | <0.001 | yes | 0.67 [−0.20, 1.39] |
| | Sarvam-1 | 246 | 0.016 | 0.013 [−0.013, 0.041] | 0.336 | no | 0.11 [−0.17, 0.43] |
| | Gemma 4 | 246 | 0.268 | 0.248 [0.187, 0.314] | <0.001 | yes | 0.67 [−0.03, 1.29] |
| SIB | Qwen3 | 256 | 0.168 | 0.156 [0.077, 0.239] | <0.001 | yes | 0.23 [−0.51, 0.96] |
| | Qwen3.5 | 256 | 0.152 | 0.151 [0.075, 0.226] | 0.001 | yes | 0.04 [−0.60, 0.64] |
| | Sarvam-1 | 256 | −0.012 | 0.009 [−0.059, 0.076] | 0.814 | no | −0.41 [−1.13, 0.26] |
| | Gemma 4 | 256 | 0.176 | 0.164 [0.078, 0.246] | 0.001 | yes | 0.24 [−0.34, 0.89] |
| sentiment | Qwen3 | 197 | 0.208 | 0.195 [0.049, 0.336] | 0.026 | yes | 0.13 [−0.71, 1.12] |
| | Qwen3.5 | 197 | 0.036 | 0.037 [−0.071, 0.152] | 0.498 | no | −0.02 [−0.80, 0.75] |
| | Sarvam-1 | 197 | 0.056 | 0.054 [−0.007, 0.119] | 0.163 | no | 0.02 [−0.25, 0.29] |
| | Gemma 4 | 197 | 0.183 | 0.116 [0.024, 0.215] | 0.042 | yes | 0.63 [−0.05, 1.21] |

δ: mean 0.031 (retrieval), 0.050 (SIB), 0.106 (sentiment); share of items with δ ≤ 0: 0.40, 0.33, 0.17.

**Verdicts (H1 rule):** retrieval **effect at equal English share** (2 of 3, needed 2); SIB **effect at equal English
share** (3 of 4, needed 3); sentiment **refuted** (2 of 4, needed 3). Every counted slope CI includes 0.
- **Sensitivity (a), continuous outcomes (no verdict):** intercept CIs exclude 0 for every counted model × measure
  except Sarvam-1 SIB (0.155 [−0.051, 0.359]); same direction as the binary results.
- **Sensitivity (b), tertiles of δ (no verdict):** in the lowest tertile (δ ≤ 0.003; Hindi no more "English" than
  Kannada), mean d is 0.163–0.209 on SIB for Qwen3, Qwen3.5, Gemma 4 (CIs exclude 0) and 0.207–0.402 on retrieval for
  Qwen3.5, Gemma 4; no monotone trend across tertiles.

## 2026-10-23 — Exploratory note result: English share of ITRANS (registered 15:44 IST; exploratory, no verdict)
`results/h1lf/itrans_share.json`. Hindi ITRANS minus Kannada ITRANS English share, same ids: retrieval +0.049
[0.041, 0.057], SIB +0.050 [0.042, 0.058], sentiment +0.053 [0.044, 0.061]. **Not near zero.** Items with any match:
Hindi 187/246, Kannada 55/246 (retrieval set). Since ITRANS adds no loans, the measure itself flags Hindi words.

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
## PRE-REGISTRATION — English-loan measure v2 (written 2026-10-23 16:00 IST, Aarnav's design; follows the 2026-10-23 diagnostic of the English-word measure; before any H1-LF option 1 score exists and before any v2 count is computed)
- **Definition v2:** a word in a romanized text (lowercased `english_share.words()`) counts as an English loan if (i)
  it is in the wordfreq English list with Zipf ≥ 3, (ii) it is longer than 3 characters, and (iii) it appears in the
  item's parallel English sentence (FLORES+ `eng_Latn` for FLORES/SIB items, the IndicSentiment English review for
  sentiment items), case-insensitive, as the exact token or a simple plural/possessive variant. Variant rule: with w
  the romanized word and E the set of lowercased English tokens (each also with a trailing possessive 's removed),
  after removing a trailing possessive 's from w, w matches if w ∈ E, w+"s" ∈ E, w+"es" ∈ E, or w ends in "s" and
  w[:-1] ∈ E, or w ends in "es" and w[:-2] ∈ E. v2 share = v2 loans / words. **Stated as a lower bound on loan share**
  (loans respelled, or absent from the English sentence, are missed).
- **Validity check, fixed now:** Hindi ITRANS minus Kannada ITRANS v2 share on the same ids (the H1 retrieval test set
  and the H1 SIB set), mean paired difference with bootstrap 95% CI (10,000; seed 0), must lie within [−0.01, +0.01]
  on BOTH retrieval and SIB items. If it fails: stop and report; v2 is not used.
- **If the check passes:** v2 replaces the registered definition for H1-LF option 1 (loan-free subset = zero v2 loans
  in both languages). The original definition is also reported alongside.
- **Post hoc (labelled as such, no verdict):** recompute with v2 the addendum English-share comparison, the loan-free
  H1, and option 2 (intercept, slope, tertiles). Report the top 20 v2-matched words per language (natural texts) as a
  sanity list.

---
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
## PRE-REGISTRATION — E-P2: word-aligned patching native → lossy, with readout-position patching (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by Aarnav with changes; before any patching code is written or run)
Same script; outputs `results/ep2/`. Models and rules as E-P1.
- **Question.** Is the lossy cost carried by the word representations (word-final residuals) or by later processing at
  the readout position? Positions aligned by word (lossy is word-by-word: 200/200 sentiment items have equal word
  counts; SIB is checked in the pilot, mismatches excluded and counted).
- **Items:** primary = native correct and lossy wrong; control = lossy correct and native wrong (SIB primary/control:
  Qwen3 398/31, Qwen3.5 345/43, Sarvam-1 126/65, Gemma 4 293/39; sentiment 69/16, 27/16, 16/4, 41/2). **Primary SIB
  capped at 200 per model (seed 0); all control items.** SIB carries the predictions; sentiment is descriptive.
- **Metric:** gold margin M as E-P1; R(L) = mean(M_patched − M_lossy) / mean(M_native − M_lossy), bootstrap 95% CI.
- **Patch points L = 0..N+1:** L ≤ N is the residual entering layer L; **L = N+1 is the final residual stream after
  layer N, before the final norm.**
  - **word-aligned:** for each text word k, the lossy run's residual at word k's last token is replaced with the native
    run's residual at native word k's last token.
  - **readout:** only the final prompt position's residual is replaced with the native run's final-position residual.
- **Selection-safe peak:** 50/50 split (seed 0); L*_word = argmax R_word(L) on the selection half.
- **Predictions (SIB, primary items):**
  - **P2a:** held-out R_word(L*_word) has a 95% CI lower bound > 0.5 in ≥ 3 of 4 models.
  - **P2b (revised):** at L*_word, held-out R_word(L*_word) − R_read(L*_word) (paired over items, bootstrap) has a 95%
    CI lower bound > 0 in ≥ 3 of 4 models.
  - **Reported, no threshold:** the old comparison (L_read = first L with R_read(L) ≥ 0.5 on all items, vs L*_word) and
    the full R_word / R_read curves with CIs.
- **Caveats:** native vs lossy differ in information and familiarity; discordant selection; Gemma 4 per-layer
  embeddings; only word-final native pieces are patched.
- **Pilot (Qwen3.5-2B, 10 SIB primary items); each check stops the run on failure:**
  1. Readout patch at L = N+1 reproduces M_native (|Δ| < 0.05).
  2. No patch reproduces M_lossy (|Δ| < 0.05).
  3. Word alignment: equal word counts, and each patched pair decodes to word k in both (10/10).
  4. Wall time per item × layer × scheme. **Stop at the pilot gate and report.**

## 2026-10-23 16:00 IST — GPU safety rule (Aarnav)
Before every model load in every chain and patching run: check GPU memory with nvidia-smi. Under the WDDM driver
nvidia-smi does not report per-process memory, so the check is: total GPU memory in use ≤ 500 MB before our own load
(desktop baseline 148 MB); otherwise wait and retry every 5 minutes, logging the used memory and the listed GPU
processes. Another project's job (C:\PROJECTS\ISM) may be running.

---
## 2026-10-23 — English-loan measure v2: validity check (registered 16:00 IST)
`scripts/h1lf.py v2`; `results/h1lf/v2_check.json`. Hindi ITRANS minus Kannada ITRANS v2 share, same ids:
retrieval (n = 246) −0.0052 [−0.0080, −0.0025]; SIB (n = 256) −0.0063 [−0.0097, −0.0032]. Both CIs lie within
[−0.01, +0.01]: **check passed**. v2 therefore replaces the registered definition for H1-LF option 1 (the original is
reported alongside; `h1lf.py analyse1` now does this). Residual Kannada ITRANS matches are loans transliterated from
Kannada script (v2 share 0.009 Kannada, 0.004 Hindi), so the CI excludes 0 in the Kannada direction while staying in
the band.

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

## 2026-10-23 — E-P1 and E-P2 pilot gates (registered 16:00 IST)
`scripts/ep_patching.py`; `results/ep1/{items.json, pilot.json}`, `results/ep2/{items.json, pilot.json,
alignment_check.json}`. No recovery value was computed. GPU check before each load: 156 MB in use.
- **Items:** every registered primary/control count reproduces exactly from the stored scores (asserted). After the cap:
  E-P1 SIB primary Qwen3 73, Qwen3.5 117, Sarvam-1 200 (of 222), Gemma 4 133; E-P2 SIB primary 200 for Qwen3,
  Qwen3.5 and Gemma 4, Sarvam-1 126.
- **Verbalizer first tokens** are distinct for every item × form under all four tokenizers: the full-verbalizer fallback
  is not needed. **SIB word counts:** native = lossy for 1,004 of 1,004 items (no exclusions).
- **Patch points:** Qwen3.5-2B has 24 layers, so there are 25 points: P = 0 (embedding output), the residual entering
  each later layer, and P = 24 = the final residual stream after the last layer, before the final norm (the
  registration's E-P2 "L = N+1").
- **E-P1 pilot (Qwen3.5-2B, 10 SIB primary items): all checks 10/10.** (1) all text positions patched at P = 0
  reproduce M_a: |Δ| = 0.0000 on all 10; (2) hooks without a patch reproduce M_c: |Δ| = 0.0000; (3) (a) and (c)
  aligned with equal per-word piece counts and identical decoded words, 10/10. Time: 0.134 s (final), 0.126 s (all) per
  patched forward; 920 items over 4 models, 2 schemes, 25 points: about 1.7 h at Qwen3.5 speed.
- **E-P2 pilot (Qwen3.5-2B, 10 SIB primary items): all checks 10/10.** (1) readout patch at the final point
  reproduces M_native: |Δ| = 0.0000; (2) no patch reproduces M_lossy: |Δ| = 0.0000; (3) equal word counts and every
  word-final pair decodes to word k in both, 10/10. Time: 0.103 s (word), 0.105 s (read) per patched forward; 1,095
  items: about 1.6 h at Qwen3.5 speed.
- **Timing caveat:** Qwen3.5 runs its linear-attention layers on the reference PyTorch fallback (`causal_conv1d` and
  `flash-linear-attention` are not installed); layer counts differ across models (the point count scales the run).
  The estimates are from Qwen3.5 only.
- **Stopped at both gates; no full run started.**

## 2026-10-23 — Note on H1 and English loans after v2 (post hoc descriptive, dated, no verdict; Aarnav)
- **Retrieval:** on the retrieval items the v2 loan-share difference (Hindi minus Kannada natural) is +0.005
  [−0.005, 0.015], so the retrieval H1 effect cannot be attributed to English loans.
- **SIB:** the v2 loan-free subset (n = 74) does not meet the rule, and v2 is a lower bound on loan share, so the SIB
  reading awaits H1-LF option 1.
- The registered H1 verdicts and the registered H1-LF option 2 verdicts are unchanged.

---
## 2026-10-24 01:50 IST — E-P1 and E-P2 results (registered 2026-10-23 16:00 IST; full runs approved by Aarnav)
Chain `scripts/ep_chain.sh` (code at commit 23c422b), 2026-10-23 21:25 → 2026-10-24 01:47 IST, one model load at a
time; the GPU guard read 147–173 MB in use before every load. **Libraries (logged in every raw file's meta, unchanged
from earlier Qwen3.5 work):** torch 2.14.1+cu126 (CUDA 12.6), transformers 5.19.0, accelerate 1.15.0, numpy 2.5.3;
causal_conv1d and flash-linear-attention not installed. Files: `results/ep{1,2}/raw/<model>.json`,
`results/ep{1,2}/curves.csv`, `results/ep{1,2}/predictions.json`; figures `paper/figures/ep{1,2}_recovery_curves.{pdf,png}`
(full R(L) curves with bootstrap 95% CIs: SIB primary, SIB control, sentiment primary descriptive).
- **Integrity:** no item excluded in either experiment (E-P1 alignment / word match; E-P2 equal word counts and
  decoding). No-patch |Δ| = 0.0 for every model in both experiments. E-P2 readout patch at the final point vs M_native:
  |Δ| = 0.0 for all four models. E-P1 all pieces at P = 0 vs M_a: |Δ| = 0.0 for Qwen3, Qwen3.5, Sarvam-1; Gemma 4
  21.96 (registered caveat: its per-layer embeddings follow (c)'s ids, so the patch is partial; logged, not a stop).

### E-P1 (NC1 (a) → (c), SIB primary items; L* from the selection half, R on the held-out half)
| model | N | n (sel/held) | L* | ⌊2N/3⌋ | held-out R_final(L*) [95% CI] | P1a | P1b | control n, R(L*) [95% CI] |
|---|---|---|---|---|---|---|---|---|
| Qwen3-1.7B | 28 | 73 (36/37) | 5 | 18 | 0.374 [0.216, 0.555] | no | yes | 70, 0.343 [0.244, 0.451] |
| Qwen3.5-2B | 24 | 117 (58/59) | 7 | 16 | 0.413 [0.284, 0.533] | no | yes | 52, 0.371 [0.275, 0.471] |
| Sarvam-1 | 28 | 200 (100/100) | 15 | 18 | 0.476 [0.422, 0.529] | no | yes | 51, 0.442 [0.254, 0.627] |
| Gemma 4 E2B | 35 | 133 (66/67) | 9 | 23 | 0.461 [0.378, 0.542] | no | yes | 59, 0.306 [0.220, 0.398] |
- **P1a: refuted** (0 of 4; ≥ 3 needed). **P1b: confirmed** (4 of 4). **Control (reported):** R(L*) has the same
  (positive) sign in all four models.
- Reported, no prediction: held-out R_all(L*) = 0.977 (Qwen3), 0.793 (Qwen3.5), 0.823 (Sarvam-1), 0.889 (Gemma 4).

### E-P2 (native → lossy, SIB primary items; L*_word from the selection half, R on the held-out half)
| model | N | n (sel/held) | L*_word | held-out R_word [95% CI] | R_read(L*_word) [95% CI] | R_word − R_read [95% CI] | P2a | P2b | control n, R_word(L*) [95% CI] |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-1.7B | 28 | 200 (100/100) | 11 | 0.371 [0.291, 0.453] | 0.020 [0.005, 0.035] | 0.351 [0.273, 0.430] | no | yes | 31, 0.466 [0.300, 0.644] |
| Qwen3.5-2B | 24 | 200 (100/100) | 6 | 0.551 [0.495, 0.604] | −0.005 [−0.015, 0.004] | 0.556 [0.500, 0.610] | no | yes | 43, 0.412 [0.258, 0.539] |
| Sarvam-1 | 28 | 126 (63/63) | 14 | 0.475 [0.410, 0.537] | −0.078 [−0.116, −0.046] | 0.553 [0.469, 0.640] | no | yes | 65, 0.025 [−0.200, 0.181] |
| Gemma 4 E2B | 35 | 200 (100/100) | 9 | 0.520 [0.450, 0.590] | −0.002 [−0.004, 0.0003] | 0.522 [0.452, 0.591] | no | yes | 39, 0.546 [0.387, 0.708] |
- **P2a: refuted** (0 of 4; ≥ 3 needed; Qwen3.5's lower bound is 0.495, Gemma 4's 0.450). **P2b: confirmed** (4 of 4).
  **Control (reported):** same (positive) sign in all four models; Sarvam-1's control CI includes 0.
- Reported, no threshold: L_read (first point with R_read ≥ 0.5 on all items) = 18 (Qwen3), 16 (Qwen3.5), 22
  (Sarvam-1), 23 (Gemma 4); L*_word < L_read in all four.

### Post hoc descriptive (dated 2026-10-24, no verdict)
- E-P1: held-out R_final(L*) is below 0.5 in all four models, while patching every piece of every word recovers
  0.79–0.98 at the same L*: much of the (a)/(c) difference is carried at non-final pieces, which "final" leaves as in
  (c) (a registered caveat).
- E-P2: the word-final curve falls to near 0 before the readout curve begins to rise in all four models (figure;
  `curves.csv`), consistent with the relevant information moving from word positions to the readout position in the
  middle layers.
- Discordant-item selection inflates the denominators (registered caveat), so the absolute scale of R is uncertain.
  Control items (selected the other way) give R(L*) within 0.16 of the held-out primary R in 7 of 8
  model × experiment cells; the exception is Sarvam-1 in E-P2 (0.025 vs 0.475).

Next: the queue is unchanged (K3b drafts resume after 12:45 IST; then H1-LF option 1 drafts and scoring; then K3b-hi).

---
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
## 2026-10-25 23:45 IST — Annotation distributed
- Aarnav confirmed the send on 2026-10-25 (logged 23:45 IST): **A** got `annotation/dist/A.zip` with
  `messages/whatsapp_A.txt`; **B** got `annotation/dist/B_part1.zip` with `messages/whatsapp_B_part1.txt`
  (built at commit 7a2eb5e; B part 1 leak check clean: 0 of 10 XML parts contain any draft text or the words
  gemini/draft; the same check finds drafts in 2 parts of A's workbook, so it does detect them).
- Not sent: `B_part2.zip` (released only once B's 40 blind items are in and A has confirmed the worked examples) and
  Rater C's workbook (built from B's returned blind 40).

---
## 2026-10-25 23:45 IST — RESULT: K3b (registered 2026-10-23): **refuted**
Source: `results/k3b/verdict.json`, `stats.csv`, `chrf.json` (analysis run 2026-10-25 16:32 IST, commit 8b988cb).
- n = 493 Dakshina Kannada strings (500 sampled; 7 excluded because the primary draft was still defective after 3
  attempts).
- Ratio R (Gemini / human, pooled), 90% CI, 95% CI, verdict under the registered rule:
  - vowel doubling: R = 0.359, 90% [0.324, 0.395], 95% [0.318, 0.402]: **differs (Gemini lower)**;
  - h-digraph use: R = 1.048, 90% [0.983, 1.115], 95% [0.971, 1.129]: matches;
  - English-word share: R = 0.895, 90% [0.824, 0.968], 95% [0.810, 0.981]: matches.
- **K3b refuted**: Gemini differs from Dakshina human romanizations in vowel doubling (about a third of their rate);
  on h-digraphs and English-word share it matches them. (Wording revised 2026-10-26, Aarnav: the comparison is with
  Dakshina's human romanizations, not with how people type in general.)
- **What the human side is:** Dakshina's romanizations are native speakers' transcriptions of Wikipedia sentences,
  written under the dataset's own instructions; they may be more careful (e.g. more consistent about vowel length)
  than casual typing, so K3b says nothing directly about everyday chat typing.
- **Drops:** 7 of 500 strings excluded because Gemini's primary output was still invalid (defective) after 3 attempts;
  all three statistics use the same 493 strings on both sides.
- Descriptive only, and **not a matched comparison** (different strings and different n): chrF of Gemini vs human,
  79.95 [79.14, 80.76] on the 493 strings; chrF between two temperature-1.0 Gemini samples, 91.85 [90.59, 93.07] on
  the 184 of the 200 resample strings where both samples were valid. The two numbers are not to be read as a gap.
- Registered limitations apply (formal Wikipedia text; "th"/"dh" also mark dentals; the temperature-1.0 reference
  likely overstates Gemini's own variation).

Next: H1-LF option 1 SIB-1,004 drafts, Kannada 878 done (8 defective), Hindi 0; stopped on Gemini quota, resumes after
2026-10-26 12:45 IST; then scoring; then K3b-hi.

---
## 2026-10-25 23:58 IST — Rater C: "no drafts" means "never told which text is Gemini" (Aarnav)
Rater C's constraint "C sees no Gemini drafts" means C is **never told which text is Gemini**, consistent with the
registered K3 design (2026-10-22; addendum 2026-10-22): C rates B's blind text and the Gemini draft as an unlabelled
pair, "Version 1 / Version 2", left/right drawn per pair with `default_rng(3)` (`k_annotation.RATER_SEED`), the side
mapping in `data/annotation/k3_rater_key_v1.json`, never in C's package. C's workbook, instructions and message do not
say that any text is machine generated and do not mention Gemini or AI (checked by `k_xlsx.wordcheck_c` on every XML
part; it finds 25 hits in B part 2's workbook and instructions, so the check works). Template built now
(`annotation/xlsx/template_rater_C.xlsx`); filled only after B's blind 40 arrive (`k_xlsx.py rater`, then
`k_package.py c`).

---
## PRE-REGISTRATION (exploratory, post hoc) — natural+dbl: vowel-doubling sensitivity (written 2026-10-25 23:58 IST, Aarnav's design; before any natural+dbl text, count, score or vector exists)
**Status:** exploratory, motivated post hoc by the K3b result (Gemini doubles vowels at about a third of the Dakshina
human rate). No prediction, no verdict; no registered verdict changes whatever it shows.
- **Question:** do the natural-form results (M4c retrieval, SIB-257) move if Gemini's natural romanization doubles long
  vowels as often as Dakshina's human romanizations?
- **Source:** the M4c natural romanizations (`data/processed/natural_flores_m4_500_v1.jsonl`), the 496 retained
  sentences (those behind the natural retrieval, 248 test half, and SIB-257 results). Defective rows keep their text
  (they are never used).
- **Build (`scripts/v_dbl.py`, CPU):**
  - Native words: whitespace tokens with at least one Kannada letter. Natural words: whitespace tokens.
  - Word alignment: monotonic DP (Needleman–Wunsch, gaps free) between native and natural words; similarity =
    1 − normalized Levenshtein between `to_lossy(native word)` and the natural word, both lowercased, letters only, with
    runs of the same vowel collapsed; a pair counts only if similarity ≥ 0.5. A native word with no pair is an
    alignment failure.
  - Within a pair: native vowel nuclei (independent vowels; each consonant's sign, or inherent a; none after virama)
    against the natural word's vowel groups (maximal runs of a, e, i, o, u). If the counts differ, the word is an
    alignment failure. Otherwise each long nucleus (ಾ/ಆ → a, ೀ/ಈ → i, ೂ/ಊ → u, ೇ/ಏ → e, ೋ/ಓ → o) whose group is
    exactly the single same letter is a candidate (a → aa, etc.).
  - Natural words in the English list used by K3b (4+ letters, wordfreq Zipf ≥ 3) are left unchanged and counted
    separately (e.g. "traffic" for ಟ್ರಾಫಿಕ್ is not doubled). This exclusion is a design choice made here, before
    running.
  - **Alignment failure rate** = failed / native words with at least one long vowel (English-list words excluded from
    both), also reported over all native words. **Gate: above 20%, stop and report; nothing else runs.** Failed words
    are left unchanged.
  - Keep rate: each candidate gets u ~ U(0, 1) from `default_rng([26, sentence index])` (a per-string generator) and is
    doubled if u < p; one p for the corpus, found by bisection so that the pooled doubling rate of the 496 strings (K3b
    `counts()`: aa, ee, ii, oo, uu per letter) equals the Dakshina human rate, 0.045343 (`results/k3b/verdict.json`).
    If p = 1 falls short, p = 1 is used and the shortfall reported.
- **Pieces per word:** natural vs natural+dbl, every model's tokenizer (5), on the M4c 496 and SIB-257 texts.
- **Reruns (GPU, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; one model load at a time; GPU guard before each load):**
  - Retrieval: natural+dbl sentence vectors for the 500 M4c rows; unmapped retrieval against English with the ladder's
    procedure (`l_ladder.retrieval_part`: same split, seed, layer choice) on the same 248 test sentences.
  - SIB: the same 257 items, E0c prompt, calibration from the stored E0c content-free files and the English
    fallback rule, exactly as `natural257`.
  - Report natural+dbl − natural per model, paired 95% bootstrap CI (10,000; `m4b_mapping.boot`), exact McNemar p
    unadjusted, n.
- **Outputs:** `results/v_dbl/`, vectors `cache/activations/m14full/<model>/natural_dbl500.npz`, scores
  `results/v_dbl/scores/`. Nothing in the registered result directories changes.

---
## 2026-10-26 00:20 IST — natural+dbl: vowel-doubling sensitivity (exploratory, registered 2026-10-25 23:58 IST; post hoc descriptive, dated, no verdict)
`scripts/v_dbl.py`; outputs `results/v_dbl/{build.json, word_failures.csv, natural_dbl500.jsonl, tokens_per_word.csv,
differences.csv, summary.json, gpu.log}`. No registered verdict changes.
- **Build:** alignment failure rate 12.1% of native words with a long vowel (456 of 3,766: 154 unaligned, 302 with a
  nucleus/vowel-group count mismatch), under the 20% gate; 9.7% over all native words (7,183). 451 natural words in
  the English list left unchanged. 3,246 candidates; keep rate p = 0.620 gives 2,012 doublings in 463 of 496 strings;
  pooled doubling rate 0.0158 (natural) → 0.0453 (natural+dbl; target, Dakshina human rate, 0.0453; p = 1 would give
  0.0626).
- Limitation seen in the output: English loans written with a suffix in Kannada script are not in the English list as a
  whole word and get doubled (e.g. ಓಪನ್‌ನಲ್ಲಿ "opennalli" → "oopennalli").
- **Pieces per word, natural → natural+dbl (M4c 496):** Qwen2.5/Qwen3 3.53 → 3.66 (+3.6%), Qwen3.5 3.33 → 3.46
  (+4.1%), Sarvam-1 4.31 → 4.45 (+3.3%), Gemma 4 3.16 → 3.29 (+4.1%); SIB-257 the same within 0.2 points of a percent.
- **natural+dbl − natural** [paired 95% bootstrap CI], exact McNemar p unadjusted (natural values reproduce
  `results/l_ladder/{retrieval,accuracy}.csv`):

| measure | model | n | natural | natural+dbl | difference | p |
|---|---|---|---|---|---|---|
| retrieval | Qwen3.5-2B | 248 | 0.512 | 0.528 | +0.016 [−0.032, +0.065] | 0.64 |
| retrieval | Sarvam-1 | 248 | 0.919 | 0.915 | −0.004 [−0.028, +0.020] | 1.00 |
| retrieval | Gemma 4 E2B | 248 | 0.710 | 0.694 | −0.016 [−0.044, +0.012] | 0.39 |
| SIB-257 | Qwen3.5-2B | 257 | 0.455 | 0.451 | −0.004 [−0.039, +0.031] | 1.00 |
| SIB-257 | Sarvam-1 | 257 | 0.728 | 0.724 | −0.004 [−0.035, +0.031] | 1.00 |
| SIB-257 | Gemma 4 E2B | 257 | 0.545 | 0.521 | −0.023 [−0.066, +0.016] | 0.34 |

- Descriptively: every CI includes 0, and the estimates are within ±0.025. Raising vowel doubling to the Dakshina
  human rate does not visibly move the natural-form results in these three models, at these sample sizes. Note: the
  retrieval layer chosen on the training half moved for Qwen3.5 (16 → 6); Sarvam-1 18 → 17, Gemma 4 7 → 7.

---
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
## 2026-10-26 01:05 IST — The 2026-10-25 A workbook, and artefacts in the Gemini drafts (post hoc descriptive, dated, no verdict)
- **The A.zip sent on 2026-10-25 contained no ratings and no corrections.** Its `annotator_A.xlsx` is byte-identical
  (SHA-256 f7ae393d…) to the build in `annotation/xlsx/` (commit 7a2eb5e). In the sheet XML the naturalness, meaning
  and note columns hold only their header cells (F1, G1, J1, K1, M1), and the corrected columns equal the drafts in
  all 1,000 cells. The filled values Aarnav saw while reviewing (ratings, Yes/No, 24 changed rows) are not in this
  file or in any file this repo wrote; their origin is not known from here.
- **Artefacts in the Gemini drafts shown to annotators** (1,000 drafts):
  - HTML tag: 1 (indicsentiment-test-792 natural ends "… honde</h4>"; the native text has no tag). The same text is
    in `natural_e0_v1.jsonl` and was used in E0b (Gate 1), the ladder and the matched tables (1 of the 198 sentiment
    natural texts).
  - Spaces before punctuation: 8 drafts, all copying a space that is in the native source text; the same holds for the
    2 such texts in `natural_e0_v1` and 6 in the M4c file. Not an artefact of Gemini.
  - "nige" for ನಿಮಗೆ (expected "nimage"): 3 drafts; in the experiment texts 4 in `natural_e0_v1` and 1 in the M4c file
    (flores-1811, used in retrieval and SIB-257).
  - "romba" (Tamil for "very"; Kannada "tumba"): 3 Kanglish drafts; Kanglish drafts are not used in any experiment yet.
- Nothing is fixed: the drafts are what annotators verify, and the experiment texts stay as run. Gemini's raw output
  is the "Gemini natural" condition by design; these are its errors.

---
## 2026-10-26 01:15 IST — Verify workbooks built (protocol change of 00:40 IST; nothing sent yet)
- `scripts/k_xlsx.py build` → `annotation/xlsx/annotator_A.xlsx` (500 items), `annotator_B_part1.xlsx` (40 blind),
  `annotator_B_part2.xlsx` (B's other 60, verify layout). Each items sheet: Kannada | English | Gemini natural | Natural
  OK? | Natural fix | Gemini Kanglish | Kanglish OK? | Kanglish fix | Note | Item ID; B part 1: Kannada | English |
  Your natural | Your Kanglish | Note | Item ID (English column removed 2026-10-26 01:35, see below). The verify sheets have 3 locked EXAMPLE rows on top (one fine, one wrong
  with a fix, one wrong because the meaning changed; written by Claude Code, checked by A before use).
- Checks on the unzipped XML of every built file (`k_xlsx.py xmlcheck`): no answer cell has a value, formula or inline
  string; no hidden sheets, columns or rows, no names, comments or cells outside the layout. B part 1 leak check: 0 of
  10 XML parts contain any line of any Gemini draft (grep, 1,007 patterns; positive control: A's workbook matches) and
  none mention gemini/draft; the 6-word-run check matches only "Sporting Shooters Association of Australia (NSW)", the
  English source sentence of flores-1292, which the Kanglish draft copied (source text, not draft text).
- Self-test on dummy copies (`scripts/k_xlsx_selftest.py`): merges reproduce the filled answers exactly; invalid cells
  (wrong + empty fix, fix = draft, fine + fix, fix without OK?, value not fine/wrong) and empty cells are reported and
  left out; changed IDs, locked drafts and example rows are refused; B parts 1 + 2 merge to 100 rows; kappa and
  anchoring run; Excel's own open-and-save keeps protection, the dropdown (stop alert), Text format and the frozen
  header, and merges to the same rows.

---
## 2026-10-26 01:35 IST — B part 1 back to the registered blind condition; how the anchoring comparison is read (Aarnav)
- **B part 1 shows the Kannada sentence only** (no English, no drafts), as in the registered blind condition
  (deviation (b), 2026-10-22). The English column of the 01:15 build is removed; B_part1.zip rebuilt. A's and B part
  2's workbooks are unchanged.
- **Reading of the anchoring comparison.** Annotator A sees the English sentence and the Gemini draft; B's blind 40 are
  written from the Kannada alone. So B blind vs A verified reflects seeing the draft **plus** seeing the English, not
  the draft alone, and is reported that way (also in `merge_xlsx.py anchor` output). B blind vs the Gemini draft is
  unaffected by this.

---
## PRE-REGISTRATION (exploratory) — EP-R: E-P1 / E-P2 recovery on all eligible items (written 2026-10-26 02:40 IST, Aarnav's design; before any new patching run)
**Status:** exploratory robustness check of the registered E-P1 and E-P2 results (2026-10-24). No prediction, no
verdict; the registered P1a/P1b/P2a/P2b outcomes stay as recorded whatever this shows.
- **Problem.** E-P1 and E-P2 ran only discordant items (primary: source form correct, destination wrong, SIB capped at
  200; control: the reverse), which inflates the gap M_src − M_dst in the denominator of R.
- **Items:** all SIB-200 items (1,004) per model, for the four models already run (Qwen3-1.7B, Qwen3.5-2B, Sarvam-1,
  Gemma 4 E2B); eligible = the registered alignment checks pass (E-P1: (a)/(c) aligned with equal per-word piece counts
  and matching decoded words; E-P2: equal word counts and word-final pieces decoding to word k). Sentiment is not run.
- **Patching:** unchanged (`scripts/ep_patching.py` functions): E-P1 scheme "final" (each text word's last piece,
  (a) → (c)); E-P2 scheme "word" (lossy word k's last piece ← native word k's last piece); all points P = 0..N; same
  models, bf16, same metric (gold margin M). Items already run (registered primary and control) are reused from
  `results/ep{1,2}/raw/` after the pilot shows they reproduce (|Δ| < 0.05 at every point); only the other items are run.
- **Sets:** (a) selected = the registered SIB primary items as run (all of them, not only the held-out half);
  (b) all eligible items; (c) excluded by selection = (b) minus (a) (control items, concordant items, and Sarvam-1's
  E-P1 primary items beyond the cap). Breakdown of (c) into control / concordant reported alongside.
- **Estimates:**
  - Main: ratio of sums, R = Σ(M_patched − M_dst) / Σ(M_src − M_dst), which is the registered ratio of means; 95%
    bootstrap CI over items (10,000, seed 0).
  - Median of per-item R = (M_patched − M_dst)/(M_src − M_dst), over items with gap M_src − M_dst ≥ 0.5 logits only,
    with bootstrap 95% CI and the count used.
  - Gap counts per set: gap < 0 (negative), 0 ≤ gap < 0.5 (near 0), ≥ 0.5. Handling: every item stays in the ratio of
    sums (negative-gap items count with their sign); near-0 and negative items are left out of the per-item median
    only. Sensitivity: ratio of sums on gap ≥ 0.5 items.
- **Points ("layer bands"):** the registered L* per model (E-P1 L*, E-P2 L*_word, from `predictions.json`), and three
  bands of points: early P < ⌊N/3⌋, middle ⌊N/3⌋ ≤ P < ⌊2N/3⌋, late P ≥ ⌊2N/3⌋ (P = 0..N). Band R = ratio of sums over
  items and the band's points (= the mean of R(P) over the band).
- **Integrity (each stops the run):** hooks without a patch reproduce M_dst (first 3 items per model, |Δ| < 0.05); E-P2:
  patching the final position at P = N reproduces M_src (first 3 items); E-P1: all text pieces at P = 0 reproduce M_src
  (first 3 items; Gemma 4 not exact by design, reported).
- **Pilot (Qwen3.5-2B, 20 SIB items per experiment: 10 already-run items, 5 primary + 5 control, and 10 new items,
  `default_rng(0)`): stored curves reproduce (|Δ| < 0.05 at every point, 10/10); eligibility of all 1,004 items for
  Qwen3.5; integrity checks; timing per item and extrapolated run time. No R is computed in the pilot. Stop at the pilot
  gate and report.**
- **Run:** detached Task Scheduler chain, one model load at a time, GPU guard (≤ 500 MB in use) before every load.
  Outputs `results/ep_robust/`.

---
## 2026-10-26 03:00 IST — EP-R pilot gate (registered 02:40 IST; exploratory)
`scripts/ep_robust.py pilot` → `results/ep_robust/pilot.json`. Qwen3.5-2B, GPU guard 148 MB before the load. No R
computed.
- **Eligibility:** 1,004 of 1,004 SIB items pass the alignment checks in both E-P1 and E-P2 (Qwen3.5); 10/10 new pilot
  items eligible in each.
- **Stored curves reproduce:** 10/10 already-run items (5 primary, 5 control) per experiment, max |Δ| = 0.0 at every
  point; reuse of the registered runs' rows is exact.
- **Integrity:** hooks without a patch reproduce M_dst (|Δ| = 0.0); E-P1 all text pieces at P = 0 reproduce M_a
  (|Δ| = 0.0); E-P2 final-position patch at P = N reproduces M_native (|Δ| = 0.0).
- **Items still to run** (1,004 minus those reused): E-P1 Qwen3 861, Qwen3.5 835, Sarvam-1 753, Gemma 4 812; E-P2 773,
  761, 813, 765 (6,373 in total). Time: 2.88 s (E-P1) and 2.91 s (E-P2) per item on Qwen3.5 (25 points); scaled by
  point counts (29, 25, 29, 36) about 6.1 h at Qwen3.5 speed (Gemma 4 has been slower per point; estimate from Qwen3.5
  only).
- **Stopped at the gate; full run not started.** Chain ready: `scripts/ep_robust_chain.sh` (detached).

---
## 2026-10-26 03:10 IST — PROTOCOL CHANGE: Annotator A is a pool of about 50 people (Aarnav)
- **A = a pool of about 50 native Kannada speakers** who together verified the 500 items in one workbook
  (`annotation/xlsx/annotator_A_filled.xlsx`, file time 2026-10-26 02:57). There are no per-item annotator IDs.
- **Consequences:** agreement within A cannot be computed; A vs B agreement (kappa on fine/wrong, 60 items) compares
  B with a pool, not with one person; "Annotator A" in K1–K3 and the agreement addendum now means this pool. Consent
  and the datasheet entries are per pool (to be filled by Aarnav in `data/annotation/DATASHEET.md`).
- No decision rule or threshold changes.

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
## 2026-10-26 03:15 IST — Verified texts built
`scripts/k_verified.py` → `data/annotation/verified_A_v1.jsonl` (500 items, A's data as given),
`data/processed/natural_e0_verified_v1.jsonl` and `data/processed/natural_flores_m4_500_verified_v1.jsonl` (the
experiment files with the natural text replaced by the verified one, same format; `results/k_verified/build.json`).
A verified text replaces the experiment's text only where A's draft is identical to it.
- **E0 file (sentiment):** 199 of A's sentiment items are in it; 198 verified against the exact experiment text, **18
  changed**; indicsentiment-test-991 not substituted (A verified a regenerated draft; the E0 text was defective and is
  excluded from natural analyses anyway). indicsentiment-test-245 (E0) was replaced in the annotation set, so it is
  not verified; indicsentiment-test-295 is annotated but not in E0.
- **M4c file (retrieval, SIB-257):** 80 of A's FLORES items are in the M4c sample; 80 verified, **3 changed**.
- **Substitution:** indicsentiment-test-249 natural uses the draft (A's fix drops content), as decided.

---
## PRE-REGISTRATION (exploratory) — V-VER: natural_verified vs the natural drafts (written 2026-10-26 03:15 IST, Aarnav's design; before any run)
No prediction, no verdict; registered verdicts are unchanged.
- **Texts:** `natural_flores_m4_500_verified_v1.jsonl` and `natural_e0_verified_v1.jsonl` (built above) vs the
  original natural files; everything else identical.
- **Measures, same matched items as the natural results, all counted models:** retrieval (M4c, 248 test sentences,
  ladder procedure, unmapped, train-half layer; Qwen3.5, Sarvam-1, Gemma 4); SIB-257 and sentiment (198 clean natural
  items) accuracy with the E0b/E0c prompts and stored calibration (Qwen3, Qwen3.5, Sarvam-1, Gemma 4).
- **Report:** verified − original per model with paired 95% bootstrap CI (10,000), exact McNemar p unadjusted, and how
  many items' texts differ in each set (and how many predictions/hits change).
- `scripts/v_ver.py`; outputs `results/v_ver/`. GPU: queued after EP-R, detached chain, one model load at a time, GPU
  guard before each load.

---
## 2026-10-26 03:15 IST — K1 and K2: implementation choices written before the scoring script runs (registration 2026-10-16; no rule or threshold changed)
The K1–K2 registration (2026-10-16) leaves these details to the scoring script; they are fixed here before any K1/K2
score exists.
- **Data:** "human-corrected" = A's verified text ("human verified Gemini romanization", protocol change of 2026-10-26);
  natural uses the draft for indicsentiment-test-249 (as decided). Gemini drafts = the drafts A verified (secondary).
- **Models:** the five E0b models (Qwen2.5-1.5B, Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B) for K1 and K2a; the four
  M4 models (Qwen2.5, Qwen3.5, Sarvam-1, Gemma 4) for K2b.
- **Scoring:** E0b `score_model` unchanged (log-likelihood of label words, BOS, content-free calibration avg of "N/A",
  "", "[MASK]"); the raw-fallback decision per model × task is taken from the full stored English rows of E0b (sentiment)
  and E0c (SIB), exactly as in Gate 1 and E0c.
- **Informative cell:** stored English accuracy on the same items (199 sentiment items in E0b; 300 SIB items in E0c)
  ≥ chance + 5 points.
- **K1:** McNemar exact on paired correctness, Kanglish verified vs natural verified, Holm across informative cells.
- **K2a:** logit(correct on Kanglish verified) ~ z(English share) + z(log tokens), tokens = the Kanglish text's tokens
  under that model's tokenizer (no special tokens); English share from `shattered.translit.codemix`; one-sided p for the
  share coefficient; Holm across counted cells (informative and constant-label rate ≤ 90% on Kanglish verified).
- **K2b:** sentence vectors of the 300 Kanglish-verified FLORES texts (`shattered.interp.collect`, as M4); layer =
  M4b's train-half best unmapped layer for native (`results/m4b_mapping/summary.csv`); outcome = rank of the true English
  sentence among the 1,005 M4b test-half English vectors (cosine); OLS −log rank ~ z(English share) + z(log tokens);
  one-sided p; Holm across the four models.
- **Pilot (Qwen3.5-2B, 20 items: 10 sentiment, 10 SIB):** item mapping and labels; recomputed content-free log-probs
  equal the stored ones; prompts build for all four K forms; K2b vectors computed for the 10 SIB items; English share
  and token counts computed; timing and extrapolation. No accuracy, coefficient or test is computed. **Stop for Aarnav's
  OK.**

---
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
## 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists)
- **Definition in K2 (registered 2026-10-16, `shattered.translit.codemix`, "v1"):** neither the English-loan measure v1
  (wordfreq Zipf ≥ 3, > 3 characters) nor v2 (also in the parallel English sentence). A lower-cased alphabetic token
  is English if it is in the wordfreq top-50k English list and not in the romanized-Kannada lexicon (to_lossy of the
  top-50k Kannada Wikipedia words); in both lists it is language-independent; otherwise Kannada.
- **Check (Aarnav's design):** 50 kanglish_verified texts, `default_rng(0)`, 883 alphabetic tokens; every token type
  marked by Claude Code (`results/codemix_check/gold_sample0.json`: E English, K Kannada, N name/unit, H English stem +
  Kannada suffix; N and H count as not English). `scripts/codemix_check.py 0 v1` →
  `results/codemix_check/check_sample0_v1.json`.
- **Result: precision 0.928 (219/236), recall 0.883 (219/248): below 0.9, so stopped.**
  - False positives (17): names and name-derived adjectives tagged English (amsterdam, angola ×2, claudia, germany,
    iceland, luxembourg, machu, stearns, frank, BIS, austrian, russian, african, mediterranean) and one Kannada word
    (kami, "less", ×2).
  - Missed English (29): 24 common English words that are also in the Kannada lexicon and so become
    language-independent (and, on, so, but, air ×3, start ×2, help, post, skin, lens ×3, gel, LED, ad ×2, dark, bed,
    sharp, limited); 5 English words outside the top-50k list (eggless, moisturize, purifiers ×2, tuners,
    occasionaly).
  - Not counted as English in either definition: 9 English-stem + Kannada-suffix tokens (productginta, groupnalli,
    lensesgalu, skinannu, …); with them counted as English, recall is 0.852.
- **Fix, v2 (`codemix.tag_v2` / `code_mixing_v2`; v1 kept unchanged):** (1) single letters language-independent;
  (2) a token that occurs in the item's parallel English sentence only in Title case and not sentence-initially is a
  name (language-independent; all-caps acronyms not affected); (3) a token in both lists goes to the language where
  it ranks higher (English: position in the wordfreq top-50k list; Kannada: best rank of a Kannada Wikipedia word whose
  lossy romanization contains it); (4) a token in neither list is English if its wordfreq English Zipf ≥ 2.5, else
  Kannada; (5) English stem + Kannada suffix stays Kannada (the share is a lower bound for such loans).
- **v2 was designed after seeing sample 0's errors**, so its rerun on sample 0 is optimistic. A fresh sample
  (`default_rng(1)`, 50 texts) is marked by hand from the v1 view (before any v2 tag of it is seen) and is the deciding
  check: v2 is used for K2 only if precision and recall are both ≥ 0.9 on it. K2 uses v2 for the English share in
  K2a and K2b if it passes; v1 results are reported alongside.

---
## 2026-10-26 12:10 IST — English-share tagger v2: checks (stopped; decision needed from Aarnav)
`scripts/codemix_check.py <seed> <v1|v2>`; `results/codemix_check/check_sample{0,1}_{v1,v2}.json`; gold markings
`gold_sample0.json` (marked from v1, before v2 existed) and `gold_sample1.json` (fresh sample, `default_rng(1)`, 1,004
tokens, marked from the v1 view before any v2 tag of it was seen).

| tagger | sample 0 (883 tokens; v2 designed from its errors) | sample 1 (1,004 tokens; fresh) |
|---|---|---|
| v1 (registered) | P 0.928, R 0.883 | P 0.900, R 0.863 |
| v2 | P 0.929, R 0.891 | **P 0.924, R 0.941** |
| v2 without the name rule (informative only; tuned on both samples) | P 0.892, R 0.968 | P 0.880, R 0.981 |

(R with English-stem + Kannada-suffix tokens counted as English: v1 0.852 / 0.815; v2 0.860 / 0.888.)
- v2 passes the criterion stated before the check (fresh sample ≥ 0.9 on both) but **fails recall on the rerun of
  sample 0** (0.891). Causes: (a) the name rule also removes ordinary English words inside multi-word names in the
  English sentence (World War, Planned Parenthood, Senate subcommittee, Anne Frank Museum, State Symphony Orchestra);
  (b) the rank rule sends Kannada "ee" ("this") to English, because the lossy romanization writes ಈ as "i", so "ee" is
  rare in the Kannada lexicon; similarly andre, ana, anna. Without the name rule recall is high but precision falls
  below 0.9 (names counted as English).
- **Stopped:** neither variant clears 0.9 on both samples. No K2 result exists; the K1/K2 pilot is not queued.

## 2026-10-26 12:10 IST — Qwen2.5 in K1/K2: kept as registered
- K1–K3 registration (written 2026-10-16): "**Scoring:** the E0b setup unchanged, on five models"; the E0b setup
  (2026-10-14): "models Qwen2.5-1.5B-Instruct, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B (Qwen3-1.7B also run as an extra)".
- The general rule appears first in the ladder registration (written 2026-10-22): "Qwen2.5-1.5B is reported in every
  table but **never counted**", later repeated per experiment (NC1, H-Hindi). Earlier, M4c (2026-10-16) excluded
  Qwen2.5 only from the second part of its own prediction.
- The rule postdates K1/K2, so under Aarnav's instruction Qwen2.5 stays counted in K1 and K2a as registered (five
  models; K2b's four M4 models include it).

---
## 2026-10-26 12:20 IST — EP-R results (exploratory, registered 2026-10-26 02:40 IST; no verdict; registered E-P1/E-P2 outcomes unchanged)
Chain `scripts/ep_robust_chain.sh`, 2026-10-26 03:09 → 10:17 IST, one model load at a time, GPU guard before each.
Files `results/ep_robust/{raw/, table.csv, gaps.csv, summary.json}`.
- **Integrity:** 1,004 of 1,004 SIB items eligible in every model × experiment; stored rows reused exactly (pilot);
  no-patch |Δ| = 0.0 everywhere; integrity |Δ| = 0.0 except E-P1 Gemma 4 (0.52; registered caveat, per-layer
  embeddings follow (c)'s ids).
- **Gaps (M_src − M_dst) outside the selected set:** most unselected items have a gap near 0 or negative. E-P1 all
  items, gap < 0 / 0–0.5 / ≥ 0.5: Qwen3 511 / 34 / 459; Qwen3.5 396 / 240 / 368; Sarvam-1 198 / 143 / 663; Gemma 4
  435 / 43 / 526. E-P2: Qwen3 278 / 15 / 711; Qwen3.5 223 / 107 / 674; Sarvam-1 233 / 110 / 661; Gemma 4 217 / 17 /
  770 (`gaps.csv`, also by control / other). Handling as registered: all items stay in the ratio of sums; the per-item
  median uses gap ≥ 0.5 only.
- **E-P1: the ratio of sums is unstable on "all" and "excluded"** where the summed gap is near 0 (e.g. Qwen3 all items,
  mean gap −0.23: R(L*) = −0.48 [−8.06, 8.56]; Qwen3.5 and Gemma 4 excluded likewise), because the (a)/(c) margin
  difference averages to about zero on unselected items. On items with gap ≥ 0.5 (registered sensitivity) R(L*),
  selected / all / excluded: Qwen3 0.413 / 0.404 / 0.399; Qwen3.5 0.373 / 0.350 / 0.329; Sarvam-1 0.486 / 0.445 / 0.415;
  Gemma 4 0.422 / 0.402 / 0.382. Per-item median R(L*) (gap ≥ 0.5), selected / all: 0.442 / 0.377, 0.283 / 0.286,
  0.500 / 0.444, 0.405 / 0.383.
- **E-P2: R does not shrink outside the selected set in 3 of 4 models.** Ratio of sums R(L*_word) [95% CI], selected /
  all / excluded: Qwen3 0.375 [0.321, 0.430] / 0.422 [0.374, 0.471] / 0.468 [0.390, 0.547]; Qwen3.5 0.557 [0.516,
  0.598] / 0.588 [0.554, 0.624] / 0.616 [0.561, 0.675]; Gemma 4 0.552 [0.505, 0.597] / 0.602 [0.565, 0.639] / 0.656
  [0.598, 0.717]; Sarvam-1 0.510 [0.460, 0.561] / 0.440 [0.401, 0.482] / 0.412 [0.361, 0.464].
- Bands (early / middle / late, all three sets) in `table.csv`. Descriptively: for E-P2 the selection did not inflate
  word-level recovery (except Sarvam-1, about −0.1 on all items); for E-P1, on items with a real (a)/(c) gap, recovery
  at L* is 0.02–0.07 lower on all items than on the selected set.

## 2026-10-26 12:20 IST — V-VER results (exploratory, registered 2026-10-26 03:15 IST; no verdict)
Chain `scripts/vver_chain.sh`, 10:17 → 10:58 IST. `results/v_ver/{differences.csv, summary.json}`. Verified texts
replace the natural drafts only for the annotated items (sentiment: 198 human verified, 18 changed; M4c: 80 human
verified, 3 changed in the retrieval test half and 3 in SIB-257); every other item keeps its Gemini draft.
- **Controls:** the unchanged items recomputed with each splice reproduce the stored vectors and log-probs exactly
  (max |Δ| 0.0 in every model).
- **Retrieval (248; 3 texts changed):** verified − original: Qwen3.5 +0.004 [0.000, 0.012] (1 hit gained), Sarvam-1
  0.000, Gemma 4 +0.004 [0.000, 0.012]; McNemar p = 1.0; same train-half layers.
- **SIB-257 (3 texts changed):** 0.000 in all four models (1 prediction changed in Qwen3, none elsewhere).
- **Sentiment (198; 18 texts changed):** Qwen3 +0.020 [+0.005, +0.040] (4 items gained, 0 lost; McNemar p = 0.125),
  Qwen3.5 −0.005 [−0.020, +0.010], Sarvam-1 0.000 [−0.015, +0.015], Gemma 4 +0.005 [−0.015, +0.025].
- Descriptively: replacing the Gemini drafts with the human-verified texts on the annotated subset moves no result
  beyond 2 points; the only CI excluding 0 is Qwen3 sentiment (+2.0 points, 4 discordant items, McNemar not
  significant).

---
## 2026-10-26 14:40 IST — K2 English share: option A (Aarnav); lexicon correction "ee"; Qwen2.5 note (before any K2 data)
No K2 statistic, coefficient or accuracy has been computed.
- **Tagger:** K2a and K2b use codemix **v2** (defined 2026-10-26 12:05) for the English share; the registered v1
  tagger is run alongside as a sensitivity check. If the K2a or K2b verdict differs between v1 and v2, both are
  reported and the difference is flagged (`verdict.json` fields `K2a_differs_v1_v2`, `K2b_differs_v1_v2`).
- **One pre-data fix to v2: lexicon correction.** "ee" is tagged Kannada (the lossy romanization writes ಈ as "i", so
  the Kannada lexicon lacks "ee", "this"); `KN_FORCE = {"ee"}` in `codemix.tag_v2`. No other change to v2. Check
  after the correction (informative; the sample-0 gold marking is unchanged): sample 0 precision 0.953, recall 0.891;
  fresh sample 1 precision 0.937, recall 0.941.
- **Qwen2.5 in K1 and K2a:** counted as registered; its cells are reported with a note that native and romanized forms
  sit near floor for this model (native-script M4 retrieval 0.178; SIB-200 native 0.336; sentiment ITRANS and natural
  near chance).
- **K1/K2 pilot queued** on the free GPU (Qwen3.5-2B, 20 items, no accuracy or test), detached; the full run waits
  for Aarnav's OK on the pilot.

---
## 2026-10-26 14:45 IST — Wording for EP-R and V-VER (Aarnav); §6 updated
- **EP-R main estimates** (`results/ep_robust/main_estimates.csv`, `scripts/ep_robust.py main`; ratio of sums at the
  registered L*, 95% bootstrap CI over items): **E-P2 = all 1,004 items**: Qwen3 0.422 [0.374, 0.471], Qwen3.5 0.588
  [0.554, 0.624], Sarvam-1 0.440 [0.401, 0.482], Gemma 4 0.602 [0.565, 0.639] (selected items as run: 0.375, 0.557,
  0.510, 0.552). **E-P1 = items with gap (M_a − M_c) ≥ 0.5 only**: Qwen3 0.404 [0.339, 0.471], Qwen3.5 0.350 [0.306,
  0.396], Sarvam-1 0.445 [0.422, 0.469], Gemma 4 0.402 [0.363, 0.441]; share of the 1,004 items meeting that
  condition 45.7%, 36.7%, 66.0%, 52.4% (gap < 0.5: 545, 636, 341, 478 items; negative: 511, 396, 198, 435). **The
  all-items E-P1 ratio of sums is never reported** (it is unstable where the summed gap is near 0).
- **Sentence for the paper:** the unusual-segmentation deficit is concentrated in a subset of items (37 to 66% of items
  have a gap of at least 0.5 logits).
- **V-VER:** record as "verification changed no result". The Qwen3 sentiment +0.020 [+0.005, +0.040] is not
  significant (McNemar p = 0.125).
- §6 (`paper/sections/assembly.tex`) carries these numbers with claims A22 and A23 in `check_numbers.py`; section check
  23 claims, 0 mismatches, no untraced numbers.

## 2026-10-26 14:50 IST — K1/K2 pilot: first attempt failed on an id-type error (no computation; fixed, relaunched)
The pilot crashed while writing the scores file (`ArrowTypeError`: sentiment ids are strings, SIB ids are ints; same
cause as the NC1 crash of 2026-10-22). Fix: SIB ids are written as strings and converted back in the analysis
(`k_k12.for_scoring`). No score, accuracy or statistic had been computed; no design change.

## 2026-10-26 15:40 IST — K1/K2 pilot gate (registered 2026-10-16; implementation notes 2026-10-26; no accuracy or statistic computed)
`scripts/k_k12.py pilot` → `results/k12/pilot.json` (Qwen3.5-2B, 10 sentiment + 10 SIB items, GPU guard 142 MB; relaunch
after the id-type fix of 14:50 IST). All checks pass:
- items map to the stored E0b / E0c items: 199 of 200 sentiment items (indicsentiment-test-295 is annotated but not in
  E0b) and 300 of 300 SIB items, 0 label mismatches, 0 native-text mismatches;
- 80 of 80 prompts scored (20 items × 4 forms); recomputed content-free log-probs equal the stored ones (max |Δ| 0.0);
- K2b vectors computed (10 × 25 layers × 2048); layers from M4b: Qwen2.5 15, Qwen3.5 15, Sarvam-1 23, Gemma 4 7; all 300
  SIB items are in M4b's test half (1,005);
- English share (v2, Kanglish verified) ranges 0.00 to 0.57 on the pilot items.
Time: 184 s for 80 prompts including the model load, 26 s for the 10 forward passes; extrapolation (Qwen3.5 speed, load
included, so an overestimate): scoring 500 items × 4 forms × 5 models about 6.4 h, K2b vectors 300 items × 4 models about
0.9 h. **Stopped at the pilot gate; the full run waits for Aarnav's OK.**

## 2026-10-27 00:05 IST — K1/K2 full run started (Aarnav's OK after the pilot gate)
Chain `scripts/k12_full_chain.sh` (detached): five E0b models scored on both tasks, then K2b vectors for the four M4 models,
then `k_k12.py analyse` (K1; K2a and K2b with v2 English share primary and v1 sensitivity). One model load at a time, GPU
guard before every load; the H1-LF priority rule applies only once the H1-LF drafts are complete and never interrupts a model
(Aarnav, 2026-10-26). No rule or threshold changed.

---
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
## 2026-10-27 02:55 IST — K1 and K2 results (registered 2026-10-16; data label "human verified Gemini romanization", annotated subset only)
Run `scripts/k_k12.py` via `scripts/k12_full_chain.sh` (2026-10-27 00:05 to 02:16 IST, one model load at a time); outputs
`results/k12/{k1.csv, k2a.csv, k2b.csv, cells.csv, verdict.json}`. All ten model × task cells are informative (stored English
accuracy 0.78 to 0.985; chance + 5 points). Qwen2.5 is counted, as registered (its native and romanized forms sit near floor).
- **K1 (Kanglish verified vs natural verified; exact McNemar, Holm over 10 cells): inconclusive.** Kanglish is above natural in 9 of
  10 cells and below in one (Sarvam-1 sentiment, −0.045 [−0.085, −0.005], Holm p 0.147); significantly above after Holm in 5:
  Qwen2.5 sentiment (+0.130) and SIB (+0.137), Qwen3 SIB (+0.177), Qwen3.5 SIB (+0.150), Gemma 4 SIB (+0.093). Rule: supported needs
  Kanglish above natural in every informative cell; refuted needs it at or below in at least half or natural significantly above in any
  cell; neither holds. The secondary comparison (the Gemini drafts) gives the same signs.
- **K2a (English-word share, accuracy; logistic, one-sided, Holm over 10 counted cells): supported.** Coefficient positive in 10 of 10
  cells, Holm-significant in 7 (not Sarvam-1 in either task, not Gemma 4 sentiment).
- **K2b (English-word share, rank of the true English sentence among 1,005; OLS, one-sided, Holm over 4 models): supported.** Positive
  and Holm-significant in all four. The registered caveat applies: English words in the input overlap lexically with the English
  target, so a positive K2b is weak evidence about meaning.
- **Tagger:** v2 (with the "ee" correction) is primary, v1 (registered) alongside; K2a and K2b verdicts do not differ between them.
  v1 recall was below 0.9 on the hand-marked sample (`results/codemix_check/`).
- Per the 2026-10-26 wording rule these results concern the annotated subset only (200 sentiment and 300 FLORES items).

## 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched
The SIB-1,004 Hindi drafts hit `getaddrinfo failed` (no network) on 2026-10-27 after 15:18 IST and the H1-LF chain was marked
FAILED; it restarted at 02:46 IST and completed the drafts at 03:14 IST (Kannada 1,004 and Hindi 1,004 done; 9 and 10 still
defective after retries, excluded as registered), then started GPU scoring (qwen3-1.7b first). The K3b-hi chain, which stops
when it sees the H1-LF chain FAILED, ended at 02:46 IST without starting; relaunched at 03:17 IST (API only, no GPU). No design
change.

---
## 2026-10-28 03:40 IST — K2b lexical-overlap control (exploratory; registered before running; CPU only, stored vectors)
**Why:** the K2b registration (2026-10-16) states that English words in the Kanglish input overlap lexically with the English
target, so K2b can rise for lexical reasons alone. No control was run in the 2026-10-27 analysis. This one is exploratory,
added after the K2b result was seen; it carries no verdict and does not change the registered K2b outcome ("supported").
- **Data and models:** exactly K2b: the 300 FLORES items, the stored `results/k12/vectors/*__k_kan_ver300.npz`, the four M4 models,
  the layer M4b chose for native text, the rank of the true English sentence among the 1,005 candidates; no model is loaded
  (tokenizers only; the GPU queue is untouched).
- **Overlap measure:** `overlap_share` = (number of words that the v2 tagger marks English and whose lowercase form is also a
  word of the parallel English sentence) / (English plus Kannada tagged words), the same denominator as the English share.
  By construction overlap_share <= english_share. The correlation between them is reported.
- **Models fitted (OLS, outcome minus log rank, as K2b; v2 tagger primary, v1 as sensitivity):** (a) z(share) + z(log tokens)
  (reproduces K2b); (b) z(share) + z(log tokens) + z(overlap_share). Reported per model: the share coefficient in (a) and (b)
  with 95% CIs (OLS) and the overlap coefficient in (b); plus the overlap-only model (z(overlap_share) + z(log tokens)).
- **Reading, fixed now:** if the share coefficient in (b) keeps its sign and its CI excludes zero, the share effect is not only
  lexical overlap; if it loses significance, the K2b result is reported as consistent with lexical overlap. Either way the
  paper states both numbers. No threshold on the size of the drop.

---
## 2026-10-28 03:50 IST — K2b overlap control results (exploratory, no verdict; registered 03:40 IST; `scripts/k2b_overlap.py`, CPU)
Without the overlap predictor the K2b coefficients are reproduced exactly (v2 tagger: Qwen2.5 0.967, Qwen3.5 1.200, Sarvam-1 0.831,
Gemma 4 1.547). With z(overlap_share) added, the English-share coefficient is 0.671 [0.281, 1.061], 0.733 [0.321, 1.146],
0.744 [0.243, 1.245], 1.298 [0.878, 1.718]: positive with every 95% CI above zero in all four models, smaller than without in
each. The overlap coefficient in the same fit has a CI including zero in three of four models (only Qwen3.5: 0.558 [0.138, 0.978]).
The two predictors correlate 0.875 (v2; 0.80 for v1), so the fit cannot separate them sharply. v1 gives the same pattern
(`results/k12/k2b_overlap.csv`). The registered K2b outcome ("supported") is unchanged; the paper text, abstract and introduction
carry the lexical-overlap caveat and this control.

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

## 2026-10-28 05:45 IST — H1-LF option 1: scoring finished (all 8 model x language loads); check script bug fixed
The chain stopped at `score check` with a `KeyError: 'qwen2.5-1.5b'` in `scored()` (a crash, not a failed check): it concatenated English
rows of every H1 model but the option-1 score directories hold calibration for the four counted models only. Fix, no design change:
`scored()` keeps English rows only for models with calibration in that directory (identical for the H1 directories, which hold all
models). The check (row counts, no NaN, pred_cal agreement >= 0.98 on identical-text overlap) is re-run unchanged.

---
## 2026-10-28 06:05 IST — H1-LF option 1 results (registered 2026-10-23 15:44 IST; v2 loan definition primary because its validity check passed)
Score check (re-run after the 05:45 bug fix, unchanged rule): pred_cal agreement 1.000 on all identical-text overlap items (Kannada 257;
Hindi 256 per model). `scripts/h1lf.py analyse1`; `results/h1lf/opt1.csv`, `opt1_verdict.json`.
- **Verdict: loan-free effect** (3 of 4 counted models positive, Holm p < 0.05; rule needs 3). Loan-free subset n = 296 of 985 items clean in both languages.
- Difference of gaps (Kannada minus Hindi; native minus natural): Qwen3 +0.196, Qwen3.5 +0.199, Gemma 4 +0.233 (Holm p < 0.001 each);
  Sarvam-1 -0.047 (Holm p 0.165, not positive). On all 985 clean items (descriptive): +0.168, +0.149, +0.170, Sarvam-1 -0.019 (p 0.256).
  The loan-free differences are not smaller than the all-items ones. The registered v1 loan-free subset (n = 110) gives the same signs (3 of 4 positive).
- The H1-LF chain script was patched with run_net and the upstream grace period after finishing; its status was set to DONE by hand
  with the reason recorded in its status file.

---
## 2026-10-28 06:20 IST — H1-LF selection check (exploratory; registered before running; CPU; Aarnav 2026-10-28)
**Why:** the loan-free subset (296 of 985 items clean in both languages, v2 definition) is a selected set; it may differ from all clean
items in length, content or topic. The registered H1-LF verdict is not changed by this analysis; it carries no verdict.
- **Items:** the 296 loan-free and the 985 clean items of `results/h1lf/opt1_verdict.json` (same construction as `h1lf.py analyse1`).
- **Descriptives, loan-free versus the other 689 items:** English word count of the parallel sentence; Kannada native word count; Qwen3
  token count of the Kannada native text; share of items whose English sentence contains a digit; share containing a name (the
  `names_in` rule of the v2 English-word tagger); SIB topic distribution (the item's label). Mann-Whitney (lengths), Fisher exact (shares)
  and chi-square (topics) p values, reported descriptively; no threshold.
- **Refit (done whether or not the subsets differ):** per counted model, item-level d_i = (native − natural, Kannada) − (native − natural,
  Hindi), regressed on a loan-free indicator, z-scored English words, z-scored Kannada Qwen3 tokens, the digit and name indicators and topic
  dummies, over all 985 items, heteroscedasticity-robust (HC3) standard errors. Reported: the adjusted gap for loan-free items (intercept
  plus indicator, covariates at their 985-item means) with a 95% CI and p, the indicator coefficient (loan-free minus other items,
  adjusted), and the unadjusted loan-free mean as a check against opt1.csv.
- **Reading, fixed now:** "the loan-free gap survives" if the adjusted loan-free gap is positive with a 95% CI above zero; Holm over the
  four models is reported alongside the raw p. No claim about a causal role of the covariates.

## 2026-10-28 06:50 IST — H1-LF selection check results (exploratory, no verdict; registered 06:20 IST; `scripts/h1lf_selection.py`)
Loan-free items (n = 296) against the other 689 clean items: English words 20.1 vs 21.6 (p 0.001), Kannada words 14.7 vs 16.5, Qwen3
Kannada tokens 176 vs 193 (both p < 0.001), digit 10% vs 25%, name 30% vs 59% (both p < 0.001); topics differ (chi-square p 0.0001;
sports 7.8% vs 12.2% and entertainment 4.4% vs 9.3% of the group lower in loan-free). Refit over all 985 (lengths, digits, names, topic
dummies, HC3): adjusted loan-free gap (Kannada gap minus Hindi gap) Qwen3 0.194 [0.114, 0.273], Qwen3.5 0.177 [0.095, 0.260], Gemma 4 0.223
[0.150, 0.296] (Holm p < 0.001), Sarvam-1 -0.044 [-0.109, 0.022] (p 0.19); the loan-free indicator is not significant in any model
(p 0.44, 0.42, 0.37, 0.09). The loan-free gap survives. Wording change (Aarnav): "differences of the gaps" replaced by "the Kannada gap
exceeds the Hindi gap by ...".

## 2026-10-29 01:30 IST — K2b wording (Aarnav): the lexical-overlap caveat is replaced by the controlled result
Abstract, introduction and §7 now say: English share predicts retrieval after controlling for overlap with the English target in all four
models (coefficients fall by 11 to 39%: 30.6, 38.9, 10.5, 16.1; the 10.5 rounds to 11), every 95% CI above zero; the predictors correlate at
r = 0.88 so their contributions cannot be fully separated. Overlap's own coefficient is not interpreted (its sentence and claim are removed;
the value stays in the appendix table). The control is exploratory; the registered K2b outcome ("supported") is unchanged.

---
## 2026-10-29 02:00 IST — K2b overlap control, robustness (exploratory; registered before running; CPU, stored vectors; Aarnav)
Same data, layer, outcome (minus log rank) and v2 tagger as the 2026-10-28 overlap control (`scripts/k2b_overlap.py`).
1. **VIF** of z(English share), z(overlap share) and z(log tokens) in the three-predictor fit, per model.
2. **Stratified check:** the 300 items are binned into overlap-share quintiles (`pandas.qcut`; many items have overlap 0, so if the
   quintile edges are not unique, equal-valued items stay together and fewer bins result: `duplicates="drop"`, and the realized bins
   and their sizes are reported). Per model, OLS of -log rank on z(English share) and z(log tokens) with bin fixed effects (dummies),
   HC3 standard errors; the English-share coefficient with its 95% CI is reported. Per-bin coefficients are also stored.
- **Reading, fixed now:** "holds within bins" if the pooled coefficient is positive with a 95% CI above zero in all four models; otherwise
  the paper says in which models it does not. The abstract is changed only if the result contradicts it. Exploratory, no verdict.

## 2026-10-29 02:20 IST — K2b overlap control, robustness results (exploratory, no verdict; `scripts/k2b_strata.py`)
- **VIF** (three-predictor fit): English share 4.28 in every model, overlap 4.44 to 4.47, log tokens 1.20 to 1.24.
- **Stratified:** only 4 bins formed (sizes 120, 62, 62, 56; many items have overlap 0, so the quintile edges tie and `duplicates="drop"`
  applied as registered). English-share coefficient within bins (bin fixed effects, HC3): Qwen2.5 0.953 [0.585, 1.322], Qwen3.5 0.924
  [0.529, 1.318], Sarvam-1 0.788 [0.385, 1.190], Gemma 4 1.276 [0.888, 1.663]: positive with every CI above zero, so it holds in all four
  models (per-bin coefficients in `k2b_strata_bins.csv`: positive in 16 of 16 bins, with CIs including zero in 5 of 16 small bins of 56 to 62 items).
  The abstract is unchanged (no contradiction). One sentence added to §7; appendix table `k2b_strata`.

## 2026-10-29 03:05 IST — K2b §7 edits (Aarnav; exploratory, from existing results; `scripts/k2b_units.py` writes a descriptive units file only)
- **The 120-item bin is not the zero-overlap bin:** 86 items have overlap exactly 0; bin 0 holds those plus 34 items with overlap up to 0.087
  (qcut with ties kept together). So no sentence about "English words never appearing in the English reference" is made. A fit on the 86
  exact-zero items would be a new analysis; not run (the 2026-10-29 instruction says no new runs).
- Added to §7: per-bin coefficients positive in 16 of 16, CIs including zero in 5 of 16 (bins of 62 and 56 items; none in the 120-item bin);
  appendix table of per-bin coefficients.
- Units stated in §7: coefficients are per SD of English share (0.18 = 18 percentage points of words); outcome = minus ln(rank of the true
  English sentence among 1,005 candidates); a coefficient of 1 = rank improves by a factor of e (2.7).

## 2026-10-29 03:30 IST — §7 trimmed for K3b-hi (Aarnav): overlap-robustness detail moved to the appendix
VIF and per-bin detail now sit in the appendix (paragraph plus tables k2b_strata, k2b_strata_bins; claims F28 and F29 are checked in the
appendix section); §7 keeps the units sentence and one sentence: the effect holds within overlap bins in all four models (appendix).
The 86-item exact-zero-overlap fit is not run (Aarnav). Main text 11.64 pages.

---
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
## 2026-10-30 — K3b-hi result; EXPERIMENT FREEZE (Aarnav, 2026-10-30)
- **K3b-hi (registered 2026-10-23 12:05 IST; `results/k3b_hi/verdict.json`): inconclusive.** 499 sentences (1 excluded as defective). Vowel-doubling ratio
  0.876, 90% CI [0.765, 0.996]: the interval extends below the registered equivalence band [0.80, 1.25], so equivalence is not established (and the CI is not
  outside the band, so "differs" is not reached). h-digraph 0.999 [0.985, 1.014] matches; English-word share 1.120 [1.053, 1.193] matches. K3b-hi holds only if
  all three match, so it does not hold. Descriptive, not a registered contrast: the depression of vowel doubling is much weaker for Hindi (0.88) than for Kannada (0.36).
  The paper reports this as inconclusive (abstract half sentence, introduction, section 7, appendix table), and does not call the Hindi drafts "natural" or
  "equivalent to human romanization".
- **All three gating results are now in** (K1/K2 2026-10-27, H1-LF option 1 2026-10-28, K3b-hi 2026-10-30). **Freeze: no new experiments.** Remaining work is
  wording, checks and submission logistics. Only the claim-scoping pass was done after the freeze (changes listed in `paper/SCOPING_CHANGES.md`).
- **Scoping pass (abstract, introduction, section 7, conclusion; plus one limitations paragraph):** general claims now say small open models (about two billion
  parameters or fewer) or name the setting; familiarity is stated as confounded with pretraining exposure and with the script, so no sentence implies that the script
  itself causes the gap; each "inconclusive by rule" verdict (K1, K3b-hi) carries its one-line reason.

---
## PHASE 2 PRE-REGISTRATION (2026-11-01; Aarnav's design and Gate A decisions of 2026-11-01; written before any Phase 2 data, score, vector, draft or download-dependent statistic exists)

**Status of Phase 1.** Phase 1 verdicts (frozen at f7ce5a8, all entries above) are final and never change. Phase 2 adds results; where a Phase 2 result goes against a Phase 1 verdict, both are reported and the Phase 1 verdict stays as recorded. Extended verdicts with enlarged model sets are reported separately from the Phase 1 verdicts.

**Provenance.** This block is committed before any Phase 2 data are generated. The commit carries the git tag `phase2-registration`; `shattered.runlog.provenance()` writes `phase2_registration_commit` (the tag's commit) into every Phase 2 result file. Phase 2 results go under `results/phase2/<experiment>/`. Pilots are run on small subsets first and their time estimates reported before full runs; pilot scores are not looked at for any decision. Every job is resumable; failures write the error to CHAIN_STATUS and stop. Gates: A (orientation, done), B (this registration), C (X1 T2, X3, X7), D (X2, X4, X5), E (X6, X8; one table of every Phase 2 registered outcome).

**Standing rules carried over.** No fabricated or estimated results (every number from a file in `results/`); registered verdicts are never changed; post hoc analyses are labelled post hoc or exploratory; deviations are logged with dates; `cache/llm_cache.sqlite` is never deleted; no Anthropic key; bf16 only, one model-loading job at a time (RAM; check for a large process from `C:\PROJECTS\ISM`); GPU guard (<= 500 MB in use) and, from 2026-11-01, a disk guard (no GPU job starts with under 25 GB free; `disk_guard` in `scripts/chainlib.sh`, `require_free_disk` in `shattered.gpuguard`); the Gemini reset is kept at 12:45 IST (`next_reset`); `paper2/` text is not edited and no new table is `\input` into it (Phase 2 tables and figures go to `paper2/tables/phase2/` and `paper2/figures/phase2/`).

### General rules for all Phase 2 tests
- **Statistics (Phase 1 reporting standards):** exact McNemar on paired per-item correctness (or retrieval hit), Holm within each measure over the family stated for that test, 95% paired bootstrap CIs (10,000 resamples, seed 0; word-clustered where a unit is a word), a difference is **significant** when its Holm-adjusted p < 0.05; Holm decides on any CI/Holm disagreement (reported). n is reported for every number.
- **Effect rule for enlarged or changed model sets ("all counted models but one").** An effect is declared when the difference is significant with the same sign in all counted models but one, and in at least two models. Phase 1's "3 of 4" and "2 of 3" are the cases of 4 and 3 counted models. With fewer than three counted models a test is **uninformative** (reported, no verdict). This applies to any new model, to X6 extended verdicts, and to the counted set of each language in X4. (Phase 1's Hindi rule allowed two counted models; Phase 2 does not.)
- **Qwen2.5-1.5B** is reported in every table and never counted, in every Phase 2 test except where a Phase 1 rule counted it and that rule is quoted verbatim (T-a below). Qwen3-1.7B has no retrieval measure (no M4 vectors) except where X4 computes them; it is counted for accuracy only.
- **Counted models (Kannada, as Phase 1):** retrieval Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; accuracy Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B. Gemma 4 inputs always prepend BOS (custom text-only loader). Interpretability and accuracy runs in bf16.
- **Accuracy measure (unchanged from E0b/E0c):** log-likelihood of the English label words after an English instruction; calibration = mean of the content-free inputs "N/A", "", "[MASK]" (each placed in every field of the template); registered fallback to raw scores for a whole model x task x template row if calibrated English accuracy is more than 5 points below raw English accuracy (decided per template, on English). A cell is informative if English accuracy >= chance + 5 points. Verbalizers unchanged: sentiment " negative"/" positive"; XNLI " yes"/" maybe"/" no"; SIB " science"," travel"," politics"," sports"," health"," entertainment"," geography".
- **Retrieval measure (unchanged from M4/M4c):** unmapped acc@1 of the English translation by cosine on the mean-pooled residual stream, layer chosen on the train half; layer 0 surface baseline (mapped ridge, M4b/M4c procedure) reported where a registration below says so.

### X1. Second prompt template (Kannada; 5 models; inference only)
**Templates (verbatim; files in `src/shattered/llm/templates/`, loaded by `build_prompt(task, fields, version)`).** T1 = the Phase 1 v1 templates (unchanged; sha256 prefixes e0_sentiment_v1 `a365bff2ce73daef`, e0_sib_v1 `caf20dbba400dad3`, e0_xnli_v1 `a18ae37e2eb49edb`). T2 differs from T1 in the instruction wording and in the order in which the options are listed; the field layout (Text/Question/Answer) and the label words are unchanged, so calibration is comparable:

```
T1 sentiment (e0_sentiment_v1):
Review: {text}
Question: Is the sentiment of this review positive or negative?
Answer:

T2 sentiment (e0_sentiment_v2, sha256 0ff4ed52c33e4068):
Review: {text}
Question: Would you say this review is negative or positive?
Answer:

T1 SIB-200 (e0_sib_v1):
Text: {text}
Question: Which topic is this text about: science, travel, politics, sports, health, entertainment or geography?
Answer:

T2 SIB-200 (e0_sib_v2, sha256 0e2b3b8758e6ebe8):
Text: {text}
Question: What is the main topic of this text: geography, entertainment, health, sports, politics, travel or science?
Answer:

T1 XNLI (e0_xnli_v1):
Premise: {premise}
Hypothesis: {hypothesis}
Question: Does the premise entail the hypothesis? Answer yes, maybe, or no.
Answer:

T2 XNLI (e0_xnli_v2, sha256 dabff550d891f18a):
Premise: {premise}
Hypothesis: {hypothesis}
Question: If the premise is true, is the hypothesis true? Choose no, maybe, or yes.
Answer:
```
(No trailing newline; all files ASCII.) **T3 (exploratory, no registered claim):** the T2 instruction translated into Kannada script, label words and field names kept in English. It is drafted with Gemini (`gemini-3.5-flash-lite`, temperature 0, cached; about 3 requests), written to `src/shattered/llm/templates/e0_*_v3.txt`, its sha256 recorded in `results/phase2/x1/t3_templates.json`, and flagged for one native-speaker annotator to verify. If the annotator has not verified it before T3 is scored, every T3 result is labelled "instruction not verified". The Kannada instruction is frozen before any T3 scoring.

**Scope.** Models: Qwen2.5-1.5B, Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B. Forms: English, native, ITRANS, lowercase (E9 `universal|lower`), lossy, natural (n = 198 sentiment, 257 SIB items with a clean draft; XNLI 193), NC-F (Phase 1 condition (b), fragmented) and NC-O (Phase 1 condition (c), equal count) with the Phase 1 seeded segmentations (identical token ids). Tasks: sentiment (200), SIB-200 (1,004; natural and L3 on the 257), IndicXNLI (200; appendix, no registration, reported only). Calibration and fallback exactly as above, decided separately for T2 (and T3).

**T-a (primary).** Under T2, **P-a in its exact Phase 1 wording** (RESULTS.md, E0c registration): "native > ITRANS and native > lossy in every informative model. Paired McNemar, Holm over all native-vs-ITRANS and native-vs-lossy tests of informative models. Supported if every difference is positive and significant. Refuted if any difference is significantly negative, or none is significant. Otherwise partly supported, with the count given." Informative = T2 English accuracy >= 14.3% + 5 points (5 models incl. Qwen2.5). **Secondary line (reported next to T-a, same statistics, Holm over its own tests):** the same two contrasts in the four counted models only ("every counted model"), with the Phase 1 outcome of the same line (9 of 10 positive and significant; Qwen2.5 native vs lossy the miss).
**T-b.** For each of the 11 Phase 1 accuracy verdicts (P-a on SIB-200; L1, L2, L3 each on sentiment and SIB-200 [L3 SIB-200 is the secondary 257-item verdict]; NC-F and NC-O each on sentiment and SIB-200), recompute under T2 by the same rule with the same counted models, Holm families and item sets, and report how many keep the same verdict category (categories: supported / partly supported / refuted for P-a; effect positive / effect negative / no effect detected for L1-L3, NC-F, NC-O). No prediction beyond reporting. E0b P1-P3 (Gate 1) are not T-b verdicts; their T2 counterparts are reported descriptively.
**T-c (descriptive).** Per cell (model x task x form) T2 minus T1 accuracy with a paired 95% bootstrap CI; calibration-fallback rows listed.

### X2. Measured romanized exposure (CPU and network; no GPU)
Languages: Kannada, Hindi, Telugu, Bengali; Tamil, Malayalam, Marathi, Gujarati as descriptive context if cheap. **Source A:** a public multilingual web corpus that labels language and script separately (e.g. `kan_Knda` vs `kan_Latn`); the exact dataset, version/revision and config names are recorded when checked (not assumed here). **Source B** (run as a second measure even if A is complete, and required if A lacks any of the four languages): a fixed-size streamed sample of a general Common Crawl-derived web corpus (counts and IDs kept, no corpus stored); native-script documents counted by Unicode range per language; romanized Indic documents detected with a romanized-capable Indic language-ID model (IndicLID if available) after a fast general language ID removes English; precision check = 50 detected romanized documents per language classified by Gemini (cached; truncated snippets only), reporting precision and the precision-corrected rate; CIs by bootstrap over shards. Exposure ratio e = romanized / native-script documents (document counts primary, bytes reported), per language and per source. This measures web availability, not the pretraining mix of the study models. RAM: no language-ID job runs alongside a model job if combined RAM would exceed about 24 GB.
**Registered:** the romanized share is higher for Hindi than for Kannada (the H1 premise): e_hi > e_kn, **supported** if the 95% bootstrap CI (over shards) of e_hi - e_kn lies above 0 in the primary source (Source A if it covers Kannada and Hindi in both scripts, otherwise Source B), reported also for the other source; **refuted** if the CI lies below 0 or both sources disagree in sign; otherwise inconclusive. No prediction for other languages. **X5 choice, registered now:** X5 uses Source A if it covers all four languages, else Source B.

### X3. Frequency-matched non-canonical tokenization (Kannada)
**Conditions (all decode to the same lossy string).** a = canonical. **NC-O** = the Phase 1 equal-count random non-canonical split (Phase 1 condition (c), same seeds, same ids). **c** = the Phase 2 *frequency-matched* equal-count split defined below (called NC-M in the Gate A brief; the Phase 1 NC-F condition (b) is not rerun). *Naming: from here on "NC-O" always means the Phase 1 equal-count random split; "c" always means the frequency-matched split; the letters (a), (b), (c) of the Phase 1 registration are not used again.*
**Piece-frequency proxies, per tokenizer (all four study tokenizers are HF BPE).** Primary (tokenizer-internal): s_int(p) = ln(1 + merge rank of p), rank = 0-based index in the tokenizer's merge list of the merge that creates p; single-character/byte base pieces get rank 0 (documented; they occur in both canonical and non-canonical splits). Secondary (reference corpus): s_ref(p) = ln(1 + count of p) over the canonical tokenization of a lossy-romanized Kannada Wikipedia sample (20231101.kn, seed 0, 100,000 words after removing every article that shares an exact or containment (>= 20 characters) match with any FLORES+/SIB/IndicSentiment/XNLI evaluation text; `to_lossy`, word by word). A split's score = mean proxy over its pieces. SD_proxy = the standard deviation of the piece-score distribution over the canonical tokenization of the reference sample, per tokenizer and proxy.
**Matching tolerance (registered before any enumeration):** a word's non-canonical split is accepted if |mean s_int(split) - mean s_int(canonical split)| <= 0.25 x SD_int. **Enumeration:** for each multi-piece word of the lossy text (units = whitespace words with their space marker, as Phase 1; Sarvam-1 byte-fallback units stay canonical), segmentations into exactly the canonical piece count k from vocabulary pieces, excluding the canonical split; exhaustive if there are at most 50,000 segmentations, else 50,000 uniform samples (counting DP, seeded `default_rng([0, model, item id, word index])`). Among the segmentations within tolerance, choose the one with the smallest absolute difference (ties broken uniformly at random with the same seed); no segmentation within tolerance leaves the word canonical (flagged). **Item eligibility:** an item enters the c-set only if at least half of its multi-piece words were changed (strictly: changed words >= 0.5 x multi-piece words). **Floor:** a model with fewer than 300 eligible SIB-200 items is reported as **exploratory and does not count**; the equivalent floor for retrieval is **150 eligible M4c sentences [proposed amendment: 300 of 1,004 SIB items is 30%; 30% of 496 is 149]**; sentiment (200) is reported for models above the SIB floor and is not itself floor-tested. Coverage (eligible items and share of multi-piece words changed) is reported per model and dataset.
**Matched item sets.** Per model, the contrasts use only the model's eligible items, with canonical (a) and NC-O restricted to the same items (Phase 1 per-item NC1 scores restricted to the matched set; the forced-ids path reproduced the canonical results exactly in Phase 1, and 2 unchanged items per model are recomputed as a control, |Delta| < 1e-3; if a control fails, the matched set is rescored in full). For retrieval, the layer is chosen on the train half of the eligible M4c sentences (M4c split, seed 0, restricted to eligible rows) and evaluated on the eligible test half, for a, NC-O and c separately, as in H-Hindi. **Balance check (reported, not a gate):** mean s_int and mean s_ref of a, NC-O and c per model; c is judged matched if |mean(c) - mean(a)| <= 0.25 SD under s_int; the s_ref balance of the s_int-built split is reported (a failure is flagged, not dropped). **Exploratory:** a split built with s_ref (same tolerance rule, SD_ref), scored the same way, no verdict.
**Measures.** Accuracy: SIB-200 and sentiment; counted models Qwen3, Qwen3.5, Sarvam-1, Gemma 4 (those above the floor); retrieval: Qwen3.5, Sarvam-1, Gemma 4 (those above the floor); Qwen2.5 reported, never counted. XNLI reported only.
**Contrasts (two-sided; Holm within each measure over 3 contrasts x counted models; effect rule above):**
- **D1 = a - NC-O** (canonical minus NC-O; the Phase 1 NC-O contrast on the matched items);
- **D2 = a - c** (canonical minus c; unfamiliar segmentation at matched piece frequency; D2 = -M1 of the Gate A brief);
- **D3 = NC-O - c** (piece rarity at equal count, both unfamiliar; = M2 of the Gate A brief).
D1 is also reported on the full Phase 1 item sets next to its matched-set value (Phase 1 values: results/nc1/contrasts.csv).
**Registered interpretation (applied to counted models above the floor, verdict word per measure):** D2 positive effect = "segmentation unfamiliarity itself costs"; D3 positive effect = "piece rarity at equal count costs". D2 none and D3 effect: the Phase 1 NC-O cost is attributed to piece rarity. D2 effect and D3 none: segmentation unfamiliarity itself costs. Both effects: both contribute. Neither: unresolved. If fewer than three models are above the floor for a measure, the measure is uninformative.

### X4. Bengali and Telugu replication (core automatic pipeline; no Kanglish, no native-speaker verification, no patching)
**Data.** FLORES+ dev and devtest `ben_Beng`, `tel_Telu` (local); SIB-200 `ben_Beng`, `tel_Telu` and IndicSentiment `bn`, `te` (fetched 2026-11-01; skipped if IndicSentiment lacks the language); Wikipedia 20231101 bn/te for the assembly probes (300 most frequent words with >= 30 whitespace occurrences, 30 occurrences each) and the E9 scheme search and the lossy back-map; Dakshina v1.0 official `bn`, `te` romanized (re-streamed, MD5-checked). **The same 496 retained FLORES IDs as the Kannada natural sample (same 248/248 M4c split, seed 0); SIB natural = the 257 M4c-overlap ids; defective Kannada-excluded ids are kept only if clean in the new language (n reported).**
**Forms.** native; **ITRANS** = the project scheme for the script (`itrans_for`), exact native round trip required on all 2,009 FLORES+ sentences (else per-sentence encoding as for Hindi, or a fixed lossless scheme, logged as a deviation); **lowercase lossless**: the E9 scheme search rerun per language (objective: frequency-weighted tokens over words with count >= 30 in that language's Wikipedia, targets as Phase 1, held-out savings reported), accepted only if lossless on all FLORES+ sentences; **lossy**: `to_lossy` rule table ported with the Kannada merge classes (long to short vowels, retroflex to dental, aspirated to unaspirated, anusvara rules, avagraha dropped, lowercase), restoration CER with a corpus-trained back-map reported, and the **collision rate** (share of distinct native word types of that language's Wikipedia that merge with another type under the lossy map) reported per language next to Kannada's (10.4%) and Hindi's; **natural**: `gemini-3.5-flash-lite`, temperature 0, cached, prompt `natural_romanization_v1` with only the language name changed ("Bengali"/"Telugu" for "Kannada", all three occurrences), defect check = any Indic-script character (U+0900-U+0DFF) or a new non-ASCII character, attempts 2-3, then excluded and counted. **Batching** (several sentences per Gemini request) is used only if a pilot on the 30 Kannada sentences with cached unbatched outputs reproduces them exactly on at least 28 of 30 sentences [proposed threshold] (chrF reported); otherwise one sentence per call; the decision is logged either way.
**Models.** All 5 (plus X6 models if added). **Counted per language (registered now):** accuracy: native SIB-200 accuracy (calibrated, primary rule) has a 95% CI lower bound above 0.40; retrieval: native unmapped retrieval at the train-chosen layer on the M4b split of the 2,009 FLORES+ sentences (test half, n = 1,005) is at least 0.50. Qwen2.5 reported, never counted. The enlarged-set effect rule applies to the counted set of each language and measure; fewer than three counted models = uninformative.
**Measures.** Tokens per word per form and model (the crossover; descriptive); SIB-200 and sentiment (if available) accuracy for native, ITRANS, lowercase, lossy (natural on the 257); unmapped retrieval for native, ITRANS, lowercase and lossy on the 2,009 sentences (M4b split) and for natural (and the other forms on the same ids) on the 496 (M4c split); layer 0 surface baseline (ridge, as M4b/M4c); MDL assembly layer for native vs ITRANS (word-clustered CIs).
**Registered, per language (Phase 1 rule texts with the enlarged-set rule):**
- **R1:** native > ITRANS and native > lossy on SIB-200 (Holm over the 2 contrasts x counted accuracy models; effect positive for each contrast).
- **R2:** unmapped retrieval native > ITRANS on the 2,009 sentences (M4b test half), counted retrieval models.
- **R3:** unmapped retrieval natural > ITRANS on the 496 (M4c test half, n = 248), the M4c analog; "natural - ITRANS > 0.10" is not used here, the rule is the enlarged-set effect rule on the paired difference.
- **R4 (assembly follows fragmentation), Phase 1 H3 text:** "the sign of (ITRANS - native MDL detok layer) matches the sign of (ITRANS - native tokens per word), with the CI excluding 0", applied **only in models where native and ITRANS tokens per word differ by at least 1 (on that language's probe words)**, effect in all such models but one and at least two. **The filter stays exactly as registered, is not relaxed, and any model that drops out for a language is reported with its tokens-per-word difference.** With fewer than three qualifying models R4 is uninformative for that language.
- **Ladder L1-L3** (lowercase - ITRANS; lossy - lowercase; natural - lossy) on accuracy (SIB-200; sentiment if available; L3 on the 257) and retrieval (M4c 248 test half), same rules and Holm families as Phase 1; the tokens-per-word checks are reported.
- **K3b-bn, K3b-te:** Gemini vs Dakshina native-speaker romanization with the exact K3b design, rule and band (sample: duplicates and strings with fewer than 3 native words dropped, 500 drawn with `default_rng(6)`, resample subset `default_rng(7)` at temperature 1.0; pooled ratios R, 90% CI against [0.80, 1.25]). **Vowel doubling is defined per language** as the non-overlapping occurrences of aa, ee, ii, oo, uu per 100 letters, for both Bengali and Telugu; h-digraph use = kh, gh, chh, jh, th, dh, ph, bh per 100 letters; English-word share as K3b. *Note, stated now:* Bengali does not distinguish long and short vowels in speech (long vowels are written in the script but pronounced alike), so the human rate of doubling may be low and the ratio unstable (the K3b rule marks the statistic inconclusive if the human pooled rate is 0); Telugu does distinguish vowel length. "th"/"dh" also mark dentals.
Optional, only if cheap and from stored H-Hindi scores: native, ITRANS, lossy rows for Hindi, exploratory.

### X5. Cross-language consistency (analysis only, descriptive; after X2 and X4)
For Kannada, Hindi, Telugu, Bengali, on the FLORES ids with a clean natural romanization in all four languages (SIB-200 ids: the 257 overlap restricted likewise), compute per model the native - natural gap g on SIB-200 accuracy and on unmapped retrieval. Pair g with the X2 exposure ratio e (Source A if it covers all four languages, else Source B). **Registered (descriptive, no significance claimed with 4 languages):** the Spearman correlation between e and g across languages is negative (more romanized exposure goes with a smaller gap): for retrieval and for accuracy separately, "consistent" if negative in all counted models but one (a model enters a measure only if it is counted for that measure in all four languages; fewer than three such models: uninformative), otherwise "inconsistent". **No p value and no fitted line in the main text.** **Reported next to the X5 figure:** the K3b ratios for Kannada, Hindi (K3b-hi), Bengali and Telugu (vowel doubling, h-digraph, English share, with 90% CIs), because the draft fidelity differs by language (vowel-doubling ratio 0.36 for Kannada, 0.88 for Hindi). **Exploratory:** a pooled item-level model, gap ~ e + native accuracy, with language and model effects and bootstrap over items.

### X6. New models, only if they add a new tokenizer regime
**Screen first (short jobs only):** Llama 3.2 1B (base or instruct recorded with the reason; gated on HF, the token in `.env` is used) and a Hugging Face search for open decoder models of at most about 3B parameters with Indic pretraining or an Indic-extended tokenizer; names are not assumed: the screen lists parameters, license, tokenizer type, Kannada native and ITRANS tokens per word, and peak memory for a forward pass with hidden states in bf16. **Inclusion rule (at most two models):** (1) fits 8 GB in bf16 for probing; (2) its Kannada native tokens per word, or its native/ITRANS ratio, differs by at least 20% (relative) from every current model, or it is Indic-pretrained with an Indic-extended tokenizer; (3) it is counted only if its native SIB-200 CI lower bound is above 0.40. **Runs (Kannada):** accuracy for all forms and both T1/T2 templates; retrieval with the surface baseline; MDL assembly; ladder; NC-F, NC-O and c; E-P2 patching last and only if time allows (same registered rule as Phase 1). **Reporting:** Phase 1 verdicts stay as they are; **extended verdicts** with the enlarged counted set use the all-but-one rule (4 of 5 accuracy, 3 of 4 retrieval) and are reported separately.

### X7. Tiny-GPT embedding accounting and a factorized-embedding control
(i) **Accounting (analysis only):** from the saved configs and `results/e05_pretrain/T6.csv`, per vocabulary: embedding parameters, non-embedding parameters, total parameters, embedding share; plus one factual sentence on how embedding capacity varies with vocabulary (Phase 1 already records 14,162,304 non-embedding parameters in every condition and embedding parameters from 0.10M to 1.57M).
(ii) **Control (registered, after X3 and before X6 full):** retrain the E5 grid with the factorized embedding (`emb_dim` in `src/shattered/pretrain/model.py`, tied input/output) so that embedding capacity is equal across vocabularies: total embedding parameters (table V x e plus projection e x d_model, d_model = 384) match the vocab-256 baseline's 98,304 within 0.4%: e = 154 (V = 256), 128 (384), 110 (512), 85 (768), 70 (1024), 22 (4096) (chosen as argmin |V x e + e x 384 - 98,304|). **Vocabularies: the three most fragmented (256, 384, 512) and the three least fragmented (768, 1024, 4096) of the Phase 1 grid, i.e. the whole grid, 3 seeds (0, 1, 2) each, 18 runs; all other settings as Phase 1 (400 MB training bytes, same data order and hyperparameters); about 8 GPU hours [flagged for Aarnav: if only the two extremes were meant, 256 and 4096 x 3 seeds = 6 runs]. Prediction: the bits-per-byte ordering by fragmentation survives equalized embedding capacity.** Decision rule: **survives** if Spearman(tokens per word, seed-mean validation BPB) >= 0.8 over the vocabularies and the vocab-256 mean BPB exceeds the vocab-4096 mean by more than 3 times the larger of the two seed SDs; **does not survive** if the Spearman is <= 0 or the 256 - 4096 difference is <= 0; otherwise inconclusive. The Phase 1 MDL assembly probes are rerun on the control models and reported descriptively (Phase 1 magnitude: at most 2 of 8 layers).

### X8. Blind second-annotator sample (needs Aarnav's annotators)
**Items:** 100 (or 200; Aarnav decides n from the CI widths below) Kannada FLORES sentences from the 496 natural sample, chosen at random with seed `default_rng(8)`, preferring sentences not in the earlier verified subset (the 300 annotated FLORES items). **Annotators X8-P and X8-Q** (renamed from "A" and "B" to avoid the Phase 1 annotators A and B; recorded only as P and Q, no identities); each writes a natural romanization from scratch, seeing only the native Kannada sentence, no Gemini text and not the other's work. Page `annotation/annotate_blind_v1.html`: required annotator field (P or Q), JSON export, no Gemini text anywhere; tested in Chrome (saving and export) before it is declared ready; short forwardable instructions.
**K4 (registered; primary outcome = inter-annotator agreement):** (i) **Cohen's kappa** between X8-P and X8-Q on the binary per-word label "the word contains a doubled vowel (aa, ee, ii, oo, uu)", over words in sentences where P and Q have equal word counts (others counted and reported); (ii) **character error rate** between X8-P and X8-Q: per sentence, Levenshtein distance between the lowercased texts reduced to [a-z ], divided by the length of the longer string, averaged over sentences. Each with a 95% bootstrap CI over sentences (10,000, seed 0). No pass/fail threshold; the result is the agreement itself. **Descriptive (no rule, no verdict):** the K3b statistics (vowel doubling, h-digraph use, English-word share) for Gemini vs the mean of P and Q (pooled rates averaged over the two annotators), as ratios with 90% CIs against [0.80, 1.25] shown for orientation only. **K5 (descriptive):** chrF between P and Q; between each annotator and Gemini; the vowel-doubling rate of P vs Q. **K6 (exploratory):** retrieval and SIB-200 accuracy on the P, Q and Gemini texts.
**Expected CI widths** (full widths; computed 2026-11-01 from the K3b data, Gemini vs the single Dakshina human romanization, 493 Kannada strings, by repeated subsampling to n and bootstrapping with 1,500 resamples, `scripts/phase2_ciwidth.py`; they are a proxy because X8 compares two humans, whose agreement can differ):

| quantity | n = 100 | n = 200 |
|---|---|---|
| Cohen's kappa, 95% CI width (point value on the proxy: 0.33, 460 of 493 strings with equal word counts) | 0.17 | 0.13 |
| character error rate, 95% CI width (point value on the proxy: 0.081) | 0.016 | 0.011 |
| vowel-doubling ratio, 90% CI width (point value 0.36) | 0.15 | 0.11 |
| h-digraph ratio, 90% CI width (point value 1.05) | 0.28 | 0.20 |
| English-word-share ratio, 90% CI width (point value 0.89) | 0.31 | 0.22 |

At n = 100 the h-digraph and English-share ratios have 90% CIs about 0.28 to 0.31 wide, wider than the equivalence band [0.80, 1.25] has room for around a true ratio of 1 (the band is 0.45 wide), so those two statistics would often be inconclusive at n = 100 and still frequently at n = 200; this is why they are descriptive in K4.

### Scheduling (registered order)
**GPU queue (one model-loading job at a time):** X1 T2 -> X3 -> X7 control -> X6 screen -> X4 Bengali -> X4 Telugu -> X1 T3 -> X6 full -> optional patching. **T3 and X6 full are the first things cut if the timeline slips.** Native, ITRANS, lowercase and lossy forms of X4 are scored before the natural drafts finish. **Without a GPU, in parallel:** X2 (RAM limit), Gemini drafting for X4 spread over quota days, X7 accounting, the X8 page, data fetches for X4 (SIB-200, IndicSentiment, Wikipedia for bn/te; Dakshina bn/te re-streamed), the lossy collision-rate report. **Gemini quota priority:** (1) X4 natural romanization, Bengali then Telugu; (2) the X2 precision check; (3) the T3 instruction; (4) anything else (K3b-bn, K3b-te). Chains longer than 20 minutes run detached with 2-minute heartbeats in `results/CHAIN_STATUS*.md` and the watcher. At each gate, for every registered test: verdict, counted models, effect sizes with CIs, n, files; anything against prediction first.

### Items flagged at Gate B for Aarnav (proposed, written into the registration above and open to change before the first run of the affected experiment)
1. X3 retrieval floor 150 eligible M4c sentences (proposed). 2. X4 batching pilot threshold 28 of 30 exact matches (proposed). 3. X7(ii) vocabulary set: literal reading = the whole 6-vocabulary grid (about 8 GPU hours); the two-extremes alternative is 6 runs. 4. X8 n: 100 or 200 (CI widths above). 5. Matched-set X3 contrasts reuse Phase 1 per-item scores for a and NC-O restricted to the eligible items (with a recompute control) instead of a full rescore. 6. Qwen2.5 stays never counted in Phase 2 except under the verbatim P-a wording in T-a.

---

## PHASE 2 RESULT: X3 frequency-matched non-canonical tokenization (run 2026-11-02; registered 2026-11-01)

Commit of the run: see `results/phase2/x3/*/provenance` (`phase2_registration_commit` a57fe610). Scripts `scripts/x3.py`, `scripts/x3_analyse.py`. Files: `results/phase2/x3/{eligibility.csv, balance.csv, proxies.json, reference_sample.json, contrasts.csv, accuracy.csv, retrieval.csv, d1_full_vs_matched.csv, controls.csv, verdict.json}`.

**Setup facts.** Reference sample: 100,000 lossy words from 182 Kannada Wikipedia articles; 0 articles were removed by the evaluation-text containment check (3,394 evaluation texts). Every model is above both floors (eligible SIB 840-894 of 1,004; eligible M4c 400-451 of 496). Recompute control: 2 SIB items per model, canonical and NC-O ids through the new path against the stored Phase 1 scores, max |dlogprob| = 0 for all five models. Balance on s_int: |mean(c) - mean(a)| = 0.016-0.023 SD for every model (matched). NC-O differs from canonical by 0.12-0.25 SD on s_int. Balance on s_ref (reported, not a gate): c is 0.27-0.50 SD below canonical (not matched on the corpus proxy).

**Verdicts (m = s_int split; counted models; Holm within measure).** D1 = a - NC-O: SIB effect, positive (3 of 4); retrieval effect, positive (2 of 3); sentiment no effect detected (2 of 4 significant positive, 3 needed). D2 = a - c: SIB no effect detected (2 of 4 positive); sentiment no effect detected (1 of 4); retrieval no effect detected (0 of 3). D3 = NC-O - c as registered: SIB no effect detected (0 positive, 2 significant negative); sentiment none; retrieval none (0 positive, 1 significant negative). Registered interpretation: **unresolved** for all three measures.

**Sign note (not a change of any verdict).** The registration describes "D3 positive effect = piece rarity at equal count costs", but with D3 = NC-O - c a rarity cost makes D3 negative (NC-O worse than c). Both readings were applied: under the literal rule D3 shows no positive effect; under the cost-as-negative reading D3 is significant in 2 of 4 models (SIB: Qwen3.5, Sarvam-1) and 1 of 3 (retrieval: Gemma 4), below the 3 and 2 needed. The verdict is "no effect detected" under both, so the interpretation is unresolved either way. D1 on the matched sets agrees with the Phase 1 full-set values in direction and significance except retrieval for Qwen3.5 (matched 0.074, p_holm 0.083; full -0.004).

---

## PHASE 2 CLARIFICATIONS (2026-11-02, Gate C decisions, Aarnav)

**C1. X3 D3 sign convention (formal clarification; no verdict changes).** The X3 registration (2026-11-01) defines D3 = NC-O - c and then says "D3 positive effect = piece rarity at equal count costs". A rarity cost means NC-O (rarer pieces) is *worse* than c, which makes D3 *negative*; the two statements cannot both hold. The analysis (`scripts/x3_analyse.py`, run 2026-11-02) applied the literal rule (effect = Holm-significant positive difference in at least 3 of 4 accuracy models, 2 of 3 retrieval models, as for every contrast). **Clarification:** the intended meaning is that piece rarity at equal count costs when NC-O scores significantly *lower* than c; the effect rule is applied to the negative direction of D3 for the interpretation line. **Verdict unchanged under both readings:** literal reading, D3 has 0 significant positive models for SIB, sentiment and retrieval; cost-as-negative reading, D3 is significantly negative in 2 of 4 models for SIB (Qwen3.5, Sarvam-1; 3 needed), 0 of 4 for sentiment, 1 of 3 for retrieval (Gemma 4; 2 needed). D3 is "no effect detected" under both, and with D2 "no effect detected" the registered interpretation stays **unresolved**. Logged as deviation row in `paper2/tables/deviations.tex`.

**C2. X3 exploratory corpus-frequency regression (defined here, before it is run; the X3 text registers only the s_ref balance check, not a regression; Aarnav asked for it at Gate C, 2026-11-02).** Exploratory, no verdict, labelled so wherever it appears. For each model and each comparison split (c = the s_int frequency-matched split, and NC-O), on the model's eligible items of the c set: unit = item (SIB-200) or test-half sentence (retrieval, eligible M4c rows, layers as in `x3_analyse.py`); x_i = mean s_ref over the pieces of the canonical text span minus mean s_ref over the pieces of the comparison split's span (s_ref as registered: ln(1 + count) over the canonical tokenization of the 100,000-word reference sample); y_i = correct(canonical) - correct(split) in {-1, 0, 1} (SIB: calibrated prediction; retrieval: acc@1 hit). Model: ordinary least squares y_i = b0 + b1 x_i. Reported per model and measure: b0 (the accuracy change at zero corpus-frequency difference), b1, n, and 95% CIs by item bootstrap (10,000 resamples, seed 0). Counted and non-counted models are all reported, Qwen2.5 flagged as never counted. Sentiment and XNLI are not included (too few items per model for a slope).

---

## PHASE 2 REGISTRATION: Kaggle runner and reproducibility gate (2026-11-02, Aarnav; registered before the first Kaggle run)

**Remote compute is Kaggle only** (account with GPU T4 x2, 30 h per week; Modal is dropped from all plans). Credentials are in `.env` only (never committed, never in the anonymised package). `scripts/kaggle_runner.py` packages the repo at a commit (`git archive` of src, scripts, configs and listed result files), uploads it as a private Kaggle dataset, pushes a private GPU T4 x2 kernel with internet on, polls, downloads the outputs and writes `results/kaggle/<job>/last_run.json` (commit, hardware, torch, bf16 support, runtime) and `results/kaggle/quota.json` (weekly hours; a push that would exceed 30 h in 7 days, or a session over 11 h, is refused). Long jobs must be resumable with one output shard at a time, so a session timeout loses at most one shard.

**Gate (rule fixed now).** `scripts/kaggle_gate.py` rescored 100 SIB-200 Kannada items (the same ids as `e0c_sib.load_items(limit=100)`) in native, ITRANS and lossy forms with Sarvam-1 and Gemma 4 E2B on the T4, first in float16 and, if a model fails, in float32 (T4 has no bf16; the laptop scores are bf16). The forms are built from the public SIB-200 text with the project code. **Pass, per model and form:** raw-prediction agreement with the laptop run at least 95 of 100, |accuracy difference| at most 0.03, no non-finite log-probability, prompt token counts identical to the laptop run on all items, and no hidden state above 65,504 in a check forward (fp16 limit). A model passes when all three forms pass in some dtype; the first dtype that passes is the dtype used for that model on Kaggle. **No remote result counts until both models pass**; the runner refuses other jobs until `results/kaggle/kaggle_gate/gate_passed.json` exists. If a model passes only in float32 that is reported and used for that model.

## PHASE 2 AMENDMENT 2 (2026-11-02): X9 to X15, Kaggle compute, page policy

**APPROVED by Aarnav on 2026-11-02 with four edits (X12 exemption and rename, gate record, A1-R option (a)), applied below. Nothing in X9 to X15 had been run when it was approved.** This text is appended to
RESULTS.md unchanged, committed, and tagged `phase2-amendment-2`; `shattered.runlog.provenance()` then records that tag's commit as
`phase2_amendment2_commit` in every X9 to X15 result file (next to `phase2_registration_commit`). It supersedes `docs/X9_registration_DRAFT.md`.
Already registered and unchanged: X7 control (full 6-vocabulary grid with factorized embeddings, 3 seeds; running), X8 (n = 100, annotators
X8-P and X8-Q, agreement primary, vowel ratio descriptive), the Kaggle runner and its reproducibility gate (registered 2026-11-02 before
its first run). Citations are not added in this amendment.

### A0. General rules for X9 to X15

- **Compute.** Laptop (RTX 3070, 8 GB, bf16) and Kaggle (T4 x2, 30 h per week, no bf16; private kernels via `scripts/kaggle_runner.py`). Modal is
  dropped. A session never exceeds 12 h and a job writes one resumable shard at a time. **No Kaggle result counts until the gate passes**
  (both gate models, dtype recorded). The dtype of every Kaggle result is the gate dtype of that model, stated in the table.
- **Models never loaded by two jobs at once on one machine; one model-loading job at a time on the laptop; disk guard 25 GB.**
- **Interpretability stays bf16 or the gate dtype of an unquantized model** (fp16 or fp32 on the T4); retrieval vectors are never taken from
  a quantized model. Where a Kaggle retrieval number is compared with a laptop number, the Kaggle value for the same model and form must be
  within 0.03 of the laptop value, otherwise the Kaggle retrieval results are labelled exploratory (checked once by A1-R). Models without a laptop baseline
  count only after A1-P.
- **Statistics (Phase 1 standards).** Exact McNemar on paired per-item correctness, Holm within each stated family, 95% paired bootstrap CIs
  (10,000 resamples, seed 0), n reported for every number. Counted models are those of Phase 1 (accuracy: Qwen3, Qwen3.5, Sarvam-1, Gemma 4;
  retrieval: Qwen3.5, Sarvam-1, Gemma 4); Qwen2.5 is reported and never counted. A new model is counted only if its native SIB-200 accuracy
  has a 95% CI lower bound above 0.40. **The X12 models are contrast endpoints and are exempt from this counting rule; they still must pass A1-P.**
- **Gate record and reporting.** The reproducibility gate (2026-11-02) passed for both models in float16. **Sarvam-1 ITRANS raw-label agreement was 0.95, exactly at the
  pass threshold (0.95);** this is recorded here and does not change the gate verdict. **Every Kaggle result table reports the mean |delta logprob| of that model from
  its gate or A1-P run** (Sarvam-1 0.079 to 0.083, Gemma 4 E2B 0.112 to 0.124 in the gate; A1-P gives the value for each new model).
- **Pilots first** (timing and a validity check; no outcome value is looked at for a decision); results are reported with registered
  verdict words; anything against the prediction is reported first; failures are logged with dates and never silently re-run.

### A1. Kaggle precision and retrieval checks (added 2026-11-02 at Aarnav's request; not experiments, run before the experiments that depend on them)

- **A1-R. Retrieval gate (the two gate models).** Rescore FLORES+ retrieval on Kaggle for Sarvam-1 and Gemma 4 E2B, in the gate dtype (float16), for native and
  ITRANS: the same 2,009 sentences, the same sentence vectors (mean residual over tokens, every layer), the same M4b protocol (layer chosen on the train half,
  seed 0, unmapped retrieval on the test half of 1,005). **Kaggle retrieval results count only if, for each model and form, the Kaggle acc@1 is within 0.03 of the
  laptop value in `results/m4b_mapping`** (and no vector is non-finite). If either model fails, every Kaggle retrieval result is labelled exploratory (A0 rule). **Data (option (a), approved):**
  the 2,009 Kannada and English FLORES+ evaluation sentences are uploaded as a **private Kaggle dataset, kept private for the whole of Phase 2 and never made public;
  it is deleted at the end of Phase 2 and the deletion is logged in RESULTS.md.** These are the only FLORES+ text sent to Kaggle. Every later Kaggle retrieval job reads the same private dataset.
- **A1-P. Per-model precision check (every model without a laptop baseline: all 7 to 9B models of X12 and X13).** On Kaggle, score 100 SIB-200 items (the gate's
  100 ids) x 3 forms (native, ITRANS, lossy) in **float16 and in float32**; **8-bit (bitsandbytes LLM.int8) replaces float32 only if float32 does not fit 2 x T4**
  (a 7B model is 28 GB in float32 against 30 GB of VRAM, so for most models 8-bit will be the reference; this is stated in the table, and 8-bit is itself an
  approximation). **The model counts only if, per form, the raw-label agreement between float16 and the reference is at least 98% and the accuracies differ
  by at most 1 point** (0.01). Also reported: the maximum absolute hidden state over all layers in float16 (as in the gate), non-finite values (any = fail), and
  both dtypes. A model that fails is not run; it is reported as "failed the precision check" with the numbers. Gemma-family or other models with a laptop baseline
  are not exempt from the hidden-state report. Retrieval and all other results for a model are only produced after it passes.

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

### X9b. Real models, QLoRA continued pretraining (memory pilot on the laptop; full runs on Kaggle)

**Models.** Sarvam-1 (**primary**: 2 training seeds per cell) and Qwen3.5-2B (**secondary**: 1 seed per cell). Seeds are 0 and 1.
**Recipe (fixed now, not tuned on any evaluation number).** 4-bit NF4 with double quantisation; compute dtype bf16 on the laptop and fp16
(with loss scaling) on the T4; LoRA rank 16, alpha 32, dropout 0.05 on all attention and MLP projections, embeddings and norms frozen;
gradient checkpointing; 512-token sequences; paged 8-bit AdamW; learning rate 2e-4, cosine to 10 percent, warmup 3 percent, weight decay 0.
**Memory pilot (laptop, first):** peak VRAM and tokens per second over 50 steps for each model and condition at the largest micro-batch that fits
8 GB; reported with the **maximum feasible token budget B per run in about 3 GPU hours** = floor(0.9 x slowest measured tokens/s x 10,800 s)
rounded down to a multiple of the tokens per optimizer step. Because speed differs between machines, **B is fixed by a 50-step timing run on
the machine that will train (the T4)** and recorded in RESULTS.md before any full run; B is the same for the three conditions of a model.
Total: Sarvam-1 3 conditions x 2 seeds + Qwen3.5-2B 3 conditions x 1 seed = 9 runs, up to about 27 GPU hours (flagged: nearly one Kaggle
week; the Qwen3.5-2B arm is cut first if the quota is short, and that is logged).

**Conditions (equal token budget B under each model's own tokenizer).** (i) *ITRANS Kannada:* Kannada Wikipedia 20231101 articles rendered with
the project ITRANS scheme (`scheme.py`), seeded order (`default_rng(9)`); (ii) *native Kannada:* the same articles in the same order in native
script; (iii) *English:* English Wikipedia 20231101 shard 0, seeded order. Each stream is cut at B tokens; words and articles consumed are reported.
**Exclusion (hard rule).** Every article containing a FLORES+ sentence (Kannada or English, dev and devtest) or a SIB-200 sentence (Kannada or
English) is removed before sampling, by exact or containment (>= 20 characters) match; the ITRANS renderings of the evaluation sentences are also
searched in the ITRANS stream. The final streams are re-scanned with the same function: **overlap must be 0 for every stream, reported per stream,
or the run does not start.** Evaluation sentences whose source article is outside Wikipedia cannot be mapped to dump articles; the match rule is
the registered operationalisation and this is a stated limitation.

**Evaluation (Kannada; the base model and the tuned model in the same environment and dtype).** (1) SIB-200 accuracy, native and ITRANS, T1 template,
calibrated as in Phase 1, 1,004 items; (2) FLORES+ retrieval against English, native and ITRANS, on the 2,009 sentences (M4b split, unmapped
retrieval at the train-chosen layer, test half n = 1,005); (3) English SIB-200 (1,004), descriptive damage check (a drop of more than 5 points is
flagged, no verdict). The tokenizer is not changed by training; its sha256 before and after is reported, so tokens per word are unchanged by
construction. Caveat stated now: adapters are trained against the 4-bit base and evaluated on the unquantized base plus adapter.

**Prediction and decision rule.** Gap g(c) = native minus ITRANS (accuracy or retrieval) after training under condition c in {ITRANS, native, English},
g(0) before training. Prediction: the gap shrinks more after ITRANS training than after either control, D_N = g(native) - g(ITRANS) > 0 and
D_E = g(English) - g(ITRANS) > 0. **Primary: Sarvam-1.** Interval for each D: a paired bootstrap over items (SIB-200) or test sentences (retrieval),
10,000 resamples, in which, **within each cell, one of the two seeds is drawn at random in every resample (so the interval includes seed variance)**;
**97.5% intervals (Bonferroni over D_N and D_E)**; seed spread (the two seeds' D values) is reported next to every interval. *Supported:* both
intervals above 0. *Partly supported:* exactly one above 0 and none below 0. *Refuted:* none above 0 and at least one entirely below 0, or both point
estimates at or below 0. *Inconclusive:* otherwise. Verdicts per measure (SIB-200 accuracy; retrieval). **Qwen3.5-2B (secondary, one seed, item
variance only)** gets the same rule and is labelled secondary; its verdict does not enter the primary conclusion. With 2 seeds the seed variance
estimate is crude; stated as a limitation.

### X10. Generation: FLORES+ devtest to English (laptop pilot; laptop or Kaggle full)

**Setup.** FLORES+ devtest, 1,012 Kannada sentences to their English references; inputs native, ITRANS, lowercase, lossy, and natural (the devtest ids
that have a clean natural romanization; n reported). One registered instruction, identical for all forms, written in English: `Translate this Kannada
sentence into English.\nKannada: {sentence}\nEnglish:`. Base models, BOS always, greedy decoding, `max_new_tokens` = 128, output cut at the first
newline; empty outputs are scored as empty (share reported per model and form). Models: the four counted accuracy models. **Metric:** chrF
(sacreBLEU, chrF2: character order 6, word order 0, beta 2), sentence-level chrF for the paired bootstrap and corpus chrF reported. **Contrasts
(family for Holm: 4 contrasts x 4 models = 16):** native - ITRANS, native - lowercase, native - lossy (1,012 sentences), native - natural (natural subset).
**Pilot:** 20 sentences per model and form, timing and output sanity only (no chrF used for any decision); the time estimate is reported before the full run.
**Prediction X10-P:** native beats ITRANS in at least 3 of 4 models (Holm-significant, positive). *Supported:* at least 3 of 4; *partly supported:* exactly 2;
*refuted:* at most 1. The other three contrasts are reported with the same effect rule, no prediction.

### X11. Quantization control (laptop)

**Arm A (registered).** Qwen3.5-2B in 4-bit NF4 (bitsandbytes, double quantisation, bf16 compute) rerun on SIB-200, 1,004 items, native, ITRANS,
lowercase, lossy, T1 template, calibrated as Phase 1, against its stored full-precision (bf16) Phase 1 results on the same items. Reported: accuracy
per form and the change (exact McNemar, paired bootstrap CI), and the change in the native-minus-ITRANS gap. **Prediction:** quantization does not
change the picture. *Supported:* every form's accuracy change is within 3 points (point estimate) and the 95% CI of the gap change lies within +-5
points. *Refuted:* any form changes by more than 5 points with the CI excluding 0. *Partly supported:* otherwise. No retrieval (no interpretability
on quantized models). **Arm B (optional, only if time allows, descriptive):** one 4B-class model chosen by the X6 screen (name not assumed),
4-bit, SIB-200 native, ITRANS, lossy; the native-minus-ITRANS gap with CI, compared with the 2B models; no verdict.

### X12. Ambari natural experiment (Kaggle, 7B in fp16 sharded over 2 x T4)

**Tokenizer check (done 2026-11-02, CPU, tokenizer files only; `results/phase2/x12/tokenizers.json`).** Ambari-7B-base-v0.1: vocabulary 49,600, native
2.74 and ITRANS 4.55 tokens per word. Ambari-7B-Instruct-v0.2: vocabulary 32,000 (the original Llama-2 tokenizer; its config names meta-llama/Llama-2-7b-hf),
native 20.83 and ITRANS 4.69. Not loadable with the current access: meta-llama/Llama-2-7b-hf (manual gate) and Ambari-7B-Instruct-v0.1 (gated, auto approval
pending on the account). **Contrast 2 is therefore kept subject to access, with a caveat registered now:** the v0.2 card says it was fine-tuned on the same
dataset with the same parameters without vocabulary expansion, while v0.1 is built on Ambari-7B-base-v0.1 (500 million new Kannada tokens); the two
differ in the tokenizer and may differ in the base model's Kannada pretraining, so the contrast is **not** a clean "fragmentation with data fixed"
test unless the base models are shown to match. It is reported as the comparison of the two released instruction models, not as a causal test.
**Models and forms.** The X12 models are contrast endpoints, exempt from the A0 counting rule (native SIB CI lower bound above 0.40) and subject to A1-P. Kannada SIB-200 (native, ITRANS, lossy; natural on the 257) and FLORES+ retrieval (native, ITRANS), T1 template, calibrated as Phase 1,
fp16 (gate dtype), no quantization.
**Contrast 1 (form-specific exposure transfer).** Llama-2-7B vs Ambari-7B-base-v0.1. Ambari's continued pretraining was on native-script Kannada, so a native gain is
expected; the tested claim is that this exposure does **not** transfer equally to ITRANS (DiD > 0). The native gain (Ambari minus Llama-2) also confounds exposure with the
tokenizer extension; the ITRANS gain is the control (ITRANS tokens per word 4.69 vs 4.55). **X9b, not X12, is the causal test of familiarity;** X12 is a natural
experiment on released models. **Prediction:** the native gain exceeds the ITRANS gain on SIB-200 and on retrieval. Statistic:
DiD = gain(native) - gain(ITRANS), paired bootstrap over items (sentences), 97.5% interval (two measures). *Supported:* both above 0; *partly supported:*
one; *refuted:* neither above 0 and one below; *inconclusive:* otherwise.
**Contrast 2 (instruction models).** Ambari-7B-Instruct-v0.1 vs v0.2: MDL assembly layer for native Kannada words (the 300 Phase 1 probe words, Phase 1
protocol, fp16) with the prediction from the tiny GPTs that the more fragmented input (v0.2, native 20.83 vs 2.74 tokens per word) is assembled later;
registered rule as H3 (sign of the layer difference matches the sign of the tokens-per-word difference, CI excluding 0). Accuracy differences are exploratory.
If v0.2 is found not to use the original Llama tokenizer, contrast 2 is dropped (it does use it).

### X13. More 7-9B models on Kaggle

**Screen (CPU first, tokenizer and metadata only, then a one-forward check on Kaggle).** Qwen3-8B (Apache-2.0; native 11.84 and ITRANS 4.34 tokens per word,
checked), **the largest Sarvam model that fits 2 x T4** (name not assumed; the screen lists the sarvamai repositories, parameters, licence and the 4-bit
memory; 4-bit only when fp16 cannot fit, and then SIB and X10 only, no retrieval), and Llama-3.1-8B (gated, access pending; retried at each screen, dropped
if still unavailable at the end of the queue, which is logged). A model enters if it fits, its gate-style check (no non-finite value, fp16 or fp32) passes
and its native SIB-200 CI lower bound exceeds 0.40 **and it passes the A1-P precision check** (the same check applies to the X12 models; a 4-bit-only model is exempt
from A1-P but is limited to SIB and X10, as stated). **Runs:** SIB-200 (native, ITRANS, lossy, lowercase), retrieval (unquantized only), X10, MDL assembly.
**Extended verdicts** use the all-but-one rule on the enlarged counted set and are reported separately; Phase 1 verdicts do not change. **Activation
patching on one 7-9B model only if it fits one 12 h session (the Phase 1 E-P recipe, same registered rule); otherwise dropped and said so.**

### X14. Black-box hosted large models (exploratory, no verdict)

Groq and OpenRouter free models. **Model choice rule, applied and logged on the day of the first call:** list the free text models of both providers; take up
to 3 with the largest stated parameter counts from different families; **no Gemini-family model in any condition involving natural text** (the natural
romanization is Gemini output). Task: SIB-200 classification by generation with one registered prompt, `Classify the topic of the following Kannada text. Answer
with exactly one of: science/technology, travel, politics, sports, health, entertainment, geography.\n\nText: {text}\nTopic:`, temperature 0, 20 new tokens,
parsed by exact (case-insensitive) category match (unparsed = wrong, share reported). Forms native, ITRANS, lossy on 1,004 items and natural on the 257
items that have a clean natural romanization (n reported; 1,004 natural romanizations do not exist). Reported per model: accuracy per form with 95% CI and the native
minus ITRANS gap with a paired bootstrap CI. Provider limits spread the calls over days; responses are cached; failures and rate limits are logged.

### X15. Human intelligibility baseline (needs annotators)

100 SIB-200 items stratified by category (proportional allocation, seed 15) from the 257 items with a clean natural romanization; forms native, ITRANS,
lossy, natural. **Latin square:** four groups of annotators; group g sees item i in form (i + g) mod 4, so each annotator sees each item in one form
only; 2 annotators per group (8 annotators, 100 judgments each, 800 judgments), 2 judgments per item-form. Annotators are native Kannada speakers who
choose the topic from the seven labels (shown in English) with no model output visible; a page built like the X8 page; no identities recorded (roles
only). Statistics: accuracy per form with 95% bootstrap CIs resampling items and annotators; chance 1/7. **Prediction X15-P:** human accuracy on native
and natural differs by less than 5 points. *Supported:* |difference| < 0.05 and the 90% CI within +-0.12 (the width expected from 200 judgments per form);
*refuted:* |difference| >= 0.05 with the 95% CI excluding 0; *inconclusive:* otherwise. Model accuracies on the same 100 items are reported next to the human ones.

### Q. Queues and budget (cut from the end of either queue if time slips; stop at gates C, D, E)

- **Laptop:** X7 control (running, about 10 GPU hours) -> X9a (about 6 h) -> X9b memory pilot -> X10 pilot -> X4 Bengali -> X4 Telugu -> X1 T3 (only after a native
  speaker verifies `T3_verification.md`; the XNLI line is marked "needs rewrite") -> X6 -> X11 -> X10 full (if not on Kaggle).
- **Kaggle (after the gate and the approval of this amendment):** A1-R retrieval gate (may run before approval; it is not an experiment) -> A1-P for each 7 to 9B model (about 0.3 h each) -> X12 -> X13 -> X9b full (about 27 h) -> X10 full. The weekly cap (30 h) means X9b alone
  needs most of a week; the runner refuses pushes over the cap and the schedule is set from measured hours.
- **Needs people or access:** T3 verification, X8 annotators P and Q, X15 annotators, Hugging Face access to Llama-2-7b-hf, Ambari-7B-Instruct-v0.1 and
  Llama-3.1-8B.

### P. Page policy (applies to every integration)

The main text targets 12 pages and may exceed 12 only for material that carries a headline claim (X9, X12, X15). Robustness, extra models, bookkeeping and
per-cell tables go to the appendix. All scale work is in **one section, "Scale and replication"**. After each integration the main-text pages are reported
with a list of what moved to the appendix. Phase 2 results enter the paper only when Aarnav says so.

**Not claimed.** No new claim about why familiarity matters, no scaling law, no change to any Phase 1 or Phase 2 verdict.

## PHASE 2 EXECUTION LOG (Amendment 2, from 2026-11-02)

- **2026-11-02 19:00 IST, A1-R data.** Private Kaggle dataset `shattered-flores-private` created (option (a), approved): the 2,009 FLORES+ dev+devtest Kannada (NFC) and English sentences, and, from the second version, the 496 retained Kannada natural-romanization drafts keyed by FLORES index (derived text, no source sentence). It is private (the Kaggle CLI reports "Your private Dataset"), stays private for the whole of Phase 2, is deleted at the end of Phase 2, and the deletion will be logged here.
- **2026-11-02, X14 model choice (rule applied on the day of the first call; `results/phase2/x14/model_choice.json`).** 21 free text models listed across Groq and OpenRouter. **No OpenRouter key is in `.env` (empty), so no OpenRouter model can be called;** the rule is applied to the callable providers (Groq only): the three largest stated parameter counts from different families are `openai/gpt-oss-120b` (120B), `qwen/qwen3.8-27b` (27B) and `allam-2-7b` (7B). The OpenRouter listing, which would have chosen `nvidia/nemotron-3-ultra-550b-a55b:free` (550B), `openai/gpt-oss-120b` and `google/gemma-4-31b-it:free` (31B; Gemma is not Gemini-family under the literal rule, same lab as the generator of the natural text), is kept in the file. If an OpenRouter key is supplied the OpenRouter models are added as extra models, not substituted. **Deviation X14-D1:** gpt-oss-120b is a reasoning model; with the registered 20 new tokens it returned an empty answer in 5 of 5 pilot calls (finish reason `length`), so it is called with `reasoning_effort` low and 400 new tokens; the answer is parsed by the same exact match. Qwen and Allam use the registered 20 tokens. The pilot (5 items, native form) was used only to check that answers parse. X14 is exploratory; Groq's free limits spread the 3,269 calls per model over days.
- **2026-11-02, X4 natural drafts, batching pilot (registered rule).** 30 Kannada sentences with cached unbatched outputs were romanized again, 10 per request: 0 of 30 identical (threshold 28). **Decision: one sentence per call** (`results/phase2/x4/natural/batching_pilot.json`). Bengali then Telugu drafts run on `scripts/x4nat_chain.sh` within the daily cap (480 requests); templates `natural_romanization_bn_v1`, `_te_v1` are the Kannada prompt with the language name replaced three times.
- **2026-11-02, X8 page.** `annotation/annotate_blind_v1.html` built (not sent): 100 sentences drawn with `default_rng(8)` from the 416 of the 496 retained FLORES sentences that are not among the 300 annotated FLORES items (`results/phase2/x8/selection.json`); annotators P and Q; no Gemini text and no translation in the page.
- **2026-11-02, X15 pages.** `annotation/x15/annotate_x15_g{0..3}.html` built (not sent): 100 items, Latin square over four groups, no labels in the pages (`results/phase2/x15/selection.json`).
- **2026-11-02, T3 sheet.** XNLI line marked "needs rewrite" in `T3_verification.md`; XNLI is not scored under T3 until a verified line is returned.
- **2026-11-02 19:26 IST, A1-R retrieval gate: PASSED.** Sarvam-1 and Gemma 4 E2B, float16, T4 x2 (about 0.37 h of quota), unmapped FLORES+ retrieval acc@1 at the train-chosen layer on the M4b test half (n = 1,005) against `results/m4b_mapping/summary.csv`: Sarvam-1 native 0.9443 vs 0.9443 (difference 0.000), ITRANS 0.5104 vs 0.5144 (0.004); Gemma 4 native 0.9960 vs 0.9950 (0.001), ITRANS 0.2657 vs 0.2687 (0.003); tolerance 0.03; no non-finite vector; the per-layer curves differ by at most 0.007. The in-kernel `pass` flag read False only because the laptop summary file is not in the Kaggle package; the comparison was done locally with the registered rule (`results/kaggle/a1r_result.json`). Kaggle retrieval counts.
- **2026-11-02 19:55 IST, A1-P first results (`results/kaggle/kaggle_precision/2026-11-02T135712/out/`), float16 vs 8-bit, 100 SIB items x 3 forms, rule: agreement >= 0.98 and accuracy difference <= 0.01 per form.** **Qwen3-8B FAILS** (reference 8-bit because float32 needs about 30.5 GiB; agreement 0.93, 0.92, 0.93; accuracy difference -0.04, +0.04, +0.03; mean |d logprob| 0.62 to 0.89; maximum hidden state 11,864; no non-finite value). **Ambari-7B-base FAILS under the 8-bit reference** (agreement 0.95, 0.99, 0.96; accuracy difference +0.03, 0.00, +0.01; maximum hidden state 1,730; no non-finite value). Qwen3-8B is not run (registered rule); the 8-bit reference is itself an approximation, which the amendment states, so the failure does not by itself say which dtype is closer to the truth. **Implementation correction (not a rule change):** the amendment says 8-bit replaces float32 only if float32 does not fit 2 x T4; my first implementation excluded float32 above 24 GiB without trying it, and Ambari-7B-base (about 25.7 GiB in float32) can fit. A1-P for Ambari-7B-base is re-run with float32 attempted first (8-bit only after an out-of-memory error, recorded); the first result stays on disk. Qwen3-8B cannot fit float32 and its result stands.
- **2026-11-02 20:20 IST, A1-P re-run of Ambari-7B-base (`results/kaggle/kaggle_precision/2026-11-02T144532/out/`): FAILS.** Float32 was attempted first and ran out of memory on 2 x T4 (CUDA OOM, 12.81 GiB allocation), so float32 does not fit and the registered 8-bit reference applies; the numbers are those of the first run (agreement 0.95, 0.99, 0.96; accuracy difference +0.03, 0.00, +0.01). **Result under the registered rule: neither Ambari-7B-base nor Qwen3-8B passes A1-P, so X12 contrast 1 scoring and X13 Qwen3-8B are not run.** Nothing is scored on Kaggle beyond the gate and A1-R. The Kaggle queue driver is stopped and waits for Aarnav's decision: the 8-bit reference shows mean |d logprob| of 0.18 to 0.89 against float16, so it may be too noisy a yardstick for 7 to 9B models (any amendment of the reference, for example float16 against a second float16 run on different shard layouts, or bfloat16 emulated on the T4, is Aarnav's to decide; no rule was changed). Quota used so far: 1.67 h of 30.

- **2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run).** The 8-bit LLM.int8 reference is withdrawn: it is an approximation, not a
  valid ground truth for an fp16 fidelity check, so the two A1-P failures above (Qwen3-8B, Ambari-7B-base) are not used. **New reference: float32 with CPU offload** (device_map over both T4s,
  12 GiB per GPU, the rest of the weights in system RAM). Pass thresholds unchanged (raw-label agreement >= 0.98 per form, |accuracy difference| <= 0.01, no non-finite values, max fp16 hidden
  state < 65504). A1-P is re-run for Qwen3-8B and Ambari-7B-base-v0.1 against it, with the time reported. If a model fails against float32, it is out of the X12/X13 float16 runs, no further
  rescue is added, and a full float32-offload SIB run (1,004 x 4 forms) is timed and its hours reported before anything is run. If both pass, X12 Ambari base and X13 Qwen3-8B run as registered.
  *Two implementation faults found while preparing this (not rule changes):* (1) in `kaggle_precision.py` the float16 model was still referenced by the caller while float32 loaded, so the
  fp16 weights stayed on GPU 0; the "float32 out of memory (12.8 GiB)" for Ambari-7B-base above was probably caused by this, not by float32 not fitting (fixed: `model = free(model)`);
  (2) `kaggle_queue.py` read the previous `last_run.json` when the runner refused a dirty tree and recorded the old 8-bit Ambari result as new at 22:58 (fixed: `push()` returns None on refusal;
  the state was reset; nothing was pushed to Kaggle by that pass).

- **2026-11-02 23:17 IST, X12 CLARIFICATION (registered by Aarnav before any X12 result exists; no verdict rule is changed).** Ambari-7B-Instruct-v0.2 uses the 32,000-token Llama-2
  tokenizer (`results/phase2/x12/tokenizers.json`: native 20.83, ITRANS 4.69 tokens per word), so it cannot be built on Ambari-7B-base (49,600; native 2.74, ITRANS 4.55). **Contrast 2 is renamed
  "instruction-pair exposure contrast":** Ambari-7B-Instruct-v0.1 (extended tokenizer plus 500M Kannada tokens) vs v0.2 (Llama-2 plus the same instruction tuning); it differs in **both** tokenizer
  and Kannada continued pretraining. **Primary statistic: the same DiD as contrast 1** (native gain minus ITRANS gain, on SIB-200 and on retrieval, 97.5% paired-bootstrap intervals, same
  verdict words). The MDL assembly comparison (300 Phase 1 probe words, fp16) is **descriptive only**, with this confound stated. **If Llama-2-7b-hf is still gated when X12 would run, this contrast
  stands in for contrast 1, and the paper says so.** Access: Ambari-7B-Instruct-v0.1 is now granted (downloads with the `.env` token); Llama-2-7b-hf and Llama-3.1-8B are still gated and are retried between jobs.
- **2026-11-02 23:17 IST, weights-loading rule (decided by Aarnav).** Ambari-7B-Instruct-v0.2 ships only pickle `.bin` weights. It is loaded **only on Kaggle**, with `weights_only=True` forced on
  `torch.load`; `shattered.interp.load.load` refuses it anywhere else (never on the laptop).
- **2026-11-02 23:17 IST, Kaggle queue order (decided by Aarnav).** (a) the A1-P job in flight (Qwen3-8B, Ambari-7B-base, float32-offload reference); (b) score whichever of the two passes: X13 Qwen3-8B,
  then X12 Ambari-base; (c) A1-P for Ambari-Instruct v0.1 and v0.2; (d) X9b full, Sarvam-1 primary arm (6 runs, about 18 GPU hours), as soon as its laptop memory pilot is done. Before each push the remaining
  weekly quota is projected; the X9b Sarvam arm is reserved this week or next, X9b goes first if X12 instruct work would push it into a later week, and the Qwen3.5-2B arm is cut first if quota is short (as registered).
  To apply this order the queue driver was changed and a `results/kaggle/HOLD` file stops new pushes while the in-flight job continues (an implementation change; no rule).
- Time stamps of the three entries above were first written with wrong clock times and corrected to the commit times (the A1-P-D1 entry 22:59, the X12 clarification, weights rule and queue order 23:17).
- Time correction (checked by scripts/check_results_times.py, which found it): the A1-R entry above was stamped 19:35 by hand but committed at 19:26; its stamp is now the commit time. From now on stamps come from `scripts/stamp.py` (system clock), and a pre-commit hook fails any entry later than the clock.

- **2026-11-02 23:21 IST, DEVIATION X9b-D1 (decided by Aarnav, registered before the pilot).** The X9b memory and timing pilot runs on the **Kaggle T4**, not on the laptop, because the amendment fixes the
  token budget B by a 50-step timing run on the machine that will train (the T4). No rule, threshold, condition, recipe or prediction changes. B = floor(0.9 x slowest measured tokens/s x 10,800 s),
  rounded down to a multiple of the tokens per optimizer step, per model, the same for the three conditions of a model, recorded here before any full run. The three training streams are built on
  CPU first and the registered exclusion scan must report overlap 0 for every stream or nothing runs; `scripts/kaggle_x9b.py` (pilot and full modes) writes `results/phase2/x9b/pilot_done.json`.
  Queue: the X9b pilot goes right after the A1-P job in flight, ahead of the X13 and X12 scoring (about an hour or less).
- Timestamps rule (Aarnav): every time in RESULTS.md, the deviations table or a log entry comes from `scripts/stamp.py` (system clock) or the commit, never typed; `scripts/check_results_times.py` and the pre-commit hook fail an entry later than its commit or the clock.

- **2026-11-02 23:24 IST, A1-P re-run against float32-offload (commit 803b5e7, 0.35 h of quota): NO VERDICT, harness error.** Both Qwen3-8B and Ambari-7B-base ended in CUDA out-of-memory while loading the
  float32 reference (9.49 and 9.33 GiB requests with 7.8 GiB still held on GPU 0): the float16 weights were still resident. The first fix (`model = free(model)`) was incomplete, because the
  caller's variable still pointed at the model while `free()` ran. Fix (no rule change, thresholds unchanged): each precision now runs in its own subprocess (`scripts/kaggle_precision.py`,
  worker mode), so memory is released by process exit. The error results carry `pass: null`; the queue driver records no verdict for them and keeps the models queued. Both models are re-queued
  against the same reference. (This also means the earlier "float32 out of memory" for Ambari-7B-base was not evidence about float32 fitting; see A1-P-D1.)

- **2026-11-02 23:32 IST, HF ACCESS GRANTED (Llama-2-7b-hf, Llama-3.1-8B); X12 contrast roles; Kaggle queue order (decided by Aarnav).** Both repos download with the `.env` token (config, tokenizer, safetensors shards reachable).
  Tokenizers (`results/phase2/x12/tokenizers.json`): Llama-2-7b-hf vocabulary 32,000, native 20.83 and ITRANS 4.69 tokens per word, token-identical to Ambari-7B-Instruct-v0.2 on the first 200 FLORES+
  sentences (so v0.2 is Llama-2's tokenizer); Llama-3.1-8B vocabulary 128,256, native 14.90, ITRANS 4.29. **X12 contrast 1 (Llama-2-7B vs Ambari-7B-base) now runs as registered and is the
  primary X12 test; the instruction-pair contrast (v0.1 vs v0.2) stays registered as a secondary contrast; the stand-in clause ("this contrast stands in for contrast 1 if Llama-2-7b-hf is still
  gated") no longer applies.** Queue after the job in flight: (a) X9b Kaggle pilot; (b) score whichever of Qwen3-8B and Ambari-7B-base passed A1-P; (c) A1-P for Llama-2-7B, then X12 contrast 1 scoring if both
  endpoints passed; (d) A1-P for Ambari-Instruct v0.1 and v0.2, then the secondary contrast if both pass; (e) A1-P for Llama-3.1-8B, then X13 scoring if it passes; (f) X9b full, Sarvam-1 arm. The 18 h X9b Sarvam
  reserve is kept: a step that would push X9b Sarvam into a later week is moved behind it. Cut order if quota is short: Llama-3.1-8B first, then the instruction pair, then the X9b Qwen3.5 arm. The Llama
  retry loop in the queue driver is retired (access exists).

- **2026-11-02 23:48 IST, annotation tasks exported to Excel (nothing sent).** `annotation/xlsx/`: X8_P and X8_Q (identical 100 sentences in the registered default_rng(8) order; no Gemini text, no English), eight X15 files (G1..G4, seats a and b; group G sees item i in
  form (i + G) mod 4, so G4 is the registered g = 0; rows shuffled with seed 15000 + G; dropdown of the seven labels; every column except Topic locked, no password), T3_verification.xlsx (XNLI line
  marked "needs rewrite", the words ದತ್ತಾಂಶ and ಪರಿಕಲ್ಪನೆ flagged). Private keys (X15 gold labels, form per group, row-to-item maps, shuffle seeds, X8 order) are in `annotation/private/` (gitignored, excluded from the
  anonymised package); the tracked `results/phase2/x15/selection.json` now holds ids only (gold labels and the form mapping were removed from it). Hygiene check (`scripts/export_xlsx.py check`, report in
  `annotation/xlsx/HYGIENE_REPORT.json`): all 11 files pass. Importers: `scripts/import_x8.py`, `scripts/import_x15.py` (registered formats; tested on synthetic returned files, outputs deleted).

- **2026-11-03 00:04 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** Annotators are not available. **X1 T3 is marked "not run (instruction not verified)"; X15 is marked "not run (annotators unavailable)"; X8 is parked and marked "not run"**
  (if the X8 files are sent later, it runs as registered). All three are removed from every queue (the laptop queue's "X1 T3" and the annotator-dependent items, and every pending annotation send); no chain or driver step referenced them. The
  workbooks, private keys, importers (`scripts/import_x8.py`, `import_x15.py`, `import_t3.py`, one command each over `annotation/returned/`, which is gitignored because returned files carry author fields) and analyses
  (`scripts/analyze_x8.py`, `analyze_x15.py`, tested on synthetic data only, outputs not kept) are kept. The three items and the reason are in `results/phase2/REGISTERED_OUTCOMES.md` (no Phase 2 outcomes table existed before; this is its start).
  The Kaggle and laptop queues continue as before.

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

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

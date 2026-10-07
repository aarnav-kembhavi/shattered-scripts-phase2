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

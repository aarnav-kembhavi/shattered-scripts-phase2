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

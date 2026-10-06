# Overnight report — 2026-10-07

Every number below comes from the file it points to. Git log has one commit per finished task.

## Status at a glance

| # | Task | Status |
|---|---|---|
| 1 | Shared infrastructure + tests | **Done** — 56 tests pass |
| 2 | E2 step 1: round trip + lossy scheme | **Done on FLORES-200** (FLORES+ is gated, see blockers) |
| 3 | E1 local: fertility + tax, F1/F1b drafts | **Done on FLORES-200**, 33 tokenizers (23 distinct); Kannada natural romanization not done |
| 4 | E5 groundwork + pilot | **Done on local RTX 3070** — see "E5 pilot" below; T4 timing not measured |
| 5 | E0 prep: candidate list + downloads | **Done** — 27 candidates listed, 6 ungated models < 5 GB downloaded |
| 6 | Kannada Wikipedia word-frequency list | **Done** |

## 1. Shared infrastructure

- `src/shattered/llm/`: SQLite response cache keyed by sha256(provider, model, prompt, params), persistent per-day
  usage counters (to stay under free-tier caps), token bucket, exponential backoff; Gemini, Groq, OpenRouter clients;
  Gemini/Anthropic free token counters. Live smoke test passed on Gemini and Groq (cached on re-run).
- `src/shattered/interp/activations.py`: per-(model, form, item, positions) float16 safetensors cache.
- `src/shattered/tok/align.py`: word -> token spans from offset mappings; tested on Kannada mid-UTF-8 splits with
  GPT-2 (byte BPE), TinyLlama (SentencePiece byte fallback) and Qwen2.5.
- `src/shattered/translit/`: our own reversible scheme engine (see "decisions I made" below for why), ITRANS and
  lossy schemes for Kannada, Tamil, Telugu, Malayalam, Hindi, Bangla.
- Bugs found by tests and fixed: an empty cache object was falsy so injected caches were ignored; separator placement
  broke Malayalam റ്റി (R+virama+R+i read as vocalic r).

## 2. E2 step 1 — transliteration (`results/e02_translit/`)

- **Round trip native -> ITRANS -> native, FLORES-200 Kannada dev+devtest: 2009/2009 exact (100%).**
  No failing characters. 17/2009 sentences are not NFC in the source; after NFC normalization still 2009/2009, and
  the ITRANS output contains no non-ASCII script characters. (`roundtrip_flores200.json`)
- Kannada Wikipedia (31,437 articles, 149.2M chars): 31,437/31,437 exact with the final encoder
  (`roundtrip_wikipedia.json`; 70,846 separators and 329,707 raw runs, almost all Latin text).
- All six Indic FLORES languages round-trip 2009/2009 after NFC (checked during E1; Bangla has 117 orphan viramas
  from র‍্য that are kept as raw runs, which costs a few tokens but is lossless).
- **Lossy scheme information loss** (FLORES Kannada; best word-level inverse learned from Kannada Wikipedia):
  **CER 3.09%**, word accuracy 88.5%, inverse covers 93.1% of tokens; decoding the lossy text as ITRANS with no corpus
  gives CER 19.2%. 10.4% of Wikipedia word types collide with another type under the lossy map.
  (`lossy_flores200.json`)

## 3. E1 local — the language tax (`results/e01_cost/summary.csv`, figures in `paper/figures/F1*`)

n = 2009 parallel FLORES-200 sentences per language. Tax = tokens / English tokens on the same sentences, paired
bootstrap 95% CI (10,000 resamples).

| Kannada tax | native | ITRANS | lossy |
|---|---|---|---|
| o200k (GPT-4o; = gpt-oss, Phi-4-mini) | 1.99 [1.97, 2.00] | 2.41 [2.40, 2.43] | 1.89 [1.87, 1.90] |
| Gemma 4 | 1.94 [1.92, 1.96] | 2.42 [2.40, 2.44] | 1.92 [1.90, 1.93] |
| Qwen 3.5–3.8 | 3.13 [3.11, 3.16] | 2.49 [2.47, 2.51] | 1.97 [1.96, 1.99] |
| Sarvam-1 | 1.23 [1.22, 1.24] | 2.76 [2.73, 2.78] | 2.25 [2.23, 2.27] |
| cl100k (GPT-4) | 8.87 [8.79, 8.95] | 2.59 [2.57, 2.61] | 2.12 [2.10, 2.13] |
| Llama 2 | 10.84 [10.74, 10.94] | 2.46 [2.44, 2.48] | 2.01 [1.99, 2.02] |

- Prediction (Dravidian >= 2x on most English-centric tokenizers; newer generations narrow but don't close the gap):
  **partly confirmed.** Old tokenizers: 6–15x. Every family's newest generation narrows it sharply (OpenAI 13.6x ->
  2.0x, Qwen 6.9x -> 3.1x for Kannada) without closing it. On o200k the four Dravidian languages sit at 1.94–1.99x,
  i.e. just *under* 2x. The failure criterion (< 1.3x on commercial API tokenizers) can't be judged yet: the Gemini
  and Claude counters were not run (API part of E1).
- **Result that cuts against our story — please read:** lossless ITRANS is *more* expensive than native Kannada on
  every current tokenizer (o200k +21%, Gemma 4 +25%, Sarvam-1 +124%); it only saves tokens on older ones (cl100k −71%,
  Llama 2 −77%). Even lossy romanization saves only ~5% on o200k. E3 prediction (1) ("ITRANS cuts input tokens
  substantially") is therefore unlikely to hold for modern models. Any cost win now has to come from E9; ITRANS's
  capital letters (rAjadhAni) are a likely reason it fragments badly, which E9 can optimize away — or not.
- Identical tokenizers (same counts on all 38k texts): cl100k = OLMo 2; o200k = gpt-oss = Phi-4-mini;
  Qwen1.5 = 2.5 = 3; Qwen3.5 = 3.8; Tekken = Mistral Nemo = Sarvam-M = Krutrim-2 = Apertus = Nemotron Nano v2;
  Sarvam-1 = Sarvam 2B v0.5; Phi-3.5 = Llama 2.
- Draft figures: `F1_tax_by_language` (dot plot on a log axis rather than grouped bars, because ratios span 1–15x),
  `F1b_tax_drift` (one panel per language, one line per family), `F1c_kannada_forms` (native vs ITRANS vs lossy).

## 4. E5 — controlled pretraining groundwork (`results/e05_pretrain/`)

Setup (`configs/e05_pretrain.yaml`): TinyStories V2 (GPT-4), one epoch over the identical first 400,001,505 bytes
(496,631 stories) for every condition; byte-level BPE tokenizers at 256 / 512 / 1k / 4k / 16k trained on the first
100 MB; 8-layer, d=384, 6-head RoPE GPT (14.16M non-embedding params in every condition); context sized to ~1 KiB of
text; 64 sequences per step, so every condition takes ~6,100 steps over the same bytes. (`data_meta.json`)

| vocab | bytes/token | ctx tokens | full-budget steps | embedding params |
|---|---|---|---|---|
| 256 | 1.00 | 1024 | 6,103 | 98,688 |
| 512 | 2.41 | 424 | 6,120 | — |
| 1k | 3.16 | 320 | 6,173 | — |
| 4k | 3.96 | 256 | 6,162 | — |
| 16k | 4.10 | 248 | 6,146 | 6,291,840 |

**GATE numbers — pilot (2 conditions, seed 0, 10% of budget = 40 MB), local RTX 3070 Laptop** (`pilot_report.json`):

- Wall time: vocab 256: 610 steps in 7.0 min (0.57 s/step); vocab 16k: 614 steps in 2.5 min (0.20 s/step), including
  evals.
- Per-step benchmark for all five conditions (ms/step: 256: 498, 512: 195, 1k: 159, 4k: 155, 16k: 181).
- **Extrapolated full grid (5 vocabs x 3 seeds x 400 MB) on this GPU: 8.3 h** (per condition, all seeds: 256: 3.5 h,
  512: 1.35 h, 1k: 1.1 h, 4k: 1.1 h, 16k: 1.2 h). 256 and 16k come from the pilot runs; the other three from the benchmark
  times the pilot's measured eval/data overhead (x1.36).
- **T4 timing was not measured** (needs the repo on Kaggle, see blockers). I am not extrapolating to T4 from the 3070.
- Pilot-only signal (1 seed, 10% budget — not a result): validation BPB 1.142 (bytes) vs 0.833 (16k); minimal-pair
  accuracy 52.1% vs 80.1% (n = 472; driven by singular subject-verb agreement 13% vs 79%, n = 200 each). The byte
  model used 3.4x more training FLOPs (4.18e15 vs 1.24e15) and still did worse.

Things you should decide at this gate:
1. **The vocab grid barely spans the top end**: 4k and 16k give 3.96 vs 4.10 bytes/token on TinyStories (its vocabulary
   is small). Almost all the fragmentation range lies between 256 and 1k. I suggest {256, 384, 512, 768, 1024, 4096},
   or keep 16k only as an anchor.
2. Budget 400 MB/run is my proposal; the 8.3 h grid fits on this laptop over one or two nights, or on Kaggle's weekly
   GPU quota.
3. The equalized-embedding sensitivity run (factorized embedding) and the mismatched-domain tokenizer are implemented
   or planned but not run.
4. Small fixes found during the pilot: batch 64 x 1 KiB overflowed 8 GB VRAM (8.3 s/step), so I use 4 x 16
   micro-batches (0.59 s/step, same optimizer step); cuDNN attention was ~12x slower than the memory-efficient kernel,
   so the SDPA backend is pinned; one minimal pair (saw/*seed) was replaced because "seed" occurs 4,491x in training.

## 5. E0 prep (`results/e00_gate/candidates.md`)

- 27 candidates with params, hub size, license, gating, vocab, and fit (8 GB bf16 local / T4 fp16 / 4-bit).
- Downloaded (ungated, < 5 GB, all load as causal LMs in transformers 5.19): Qwen3.5-0.8B, Qwen3.5-2B,
  Qwen3.5-2B-Base, Qwen3-0.6B, Qwen3-1.7B, Qwen2.5-1.5B-Instruct (19.5 GB total).
- E0 datasets verified: IndicXNLI kn test 5010 items, balanced 3-way (chance 33.3%), CC0-1.0; IndicSentiment kn test
  1000 items, **binary** (506 pos / 492 neg / 2 unlabeled; chance ~50%), includes the parallel English review.
  E0 itself was not run (not on tonight's list).

## 6. Kannada word frequencies (`data/processed/kn_wiki_wordfreq.parquet`, `results/data_kn_wiki/summary.json`)

17.0M word tokens, 1.49M types, **50,513 types with >= 30 occurrences** (E4a needs ~500–1000). Top 20k annotated with
token counts. Mean tokens/word for the top 1000 words, native -> ITRANS: Qwen3 9.27 -> 3.41, Qwen3.5 4.23 -> 3.32,
o200k 2.34 -> 3.13, Gemma 4 2.34 -> 3.15, Sarvam-1 1.31 -> 4.23.

## Blocked / needs you

1. **Accept FLORES+ terms** on HF (`openlanguagedata/flores_plus`, auto-approve). Then I re-run E1/E2 with
   `--corpus flores_plus`; current numbers are on Meta's original FLORES-200 (same CC-BY-SA 4.0 license).
2. **Gated models/tokenizers**: Llama 3.2/3.1 (Meta reviews manually), Gemma 2/3, Aya. Missing from E1 drift and E0.
3. **Download approval just over 5 GB**: `sarvamai/sarvam-1` (5.05 GB total, largest file 4.77 GB; the most relevant
   Indic model) and `BharatGenAI/Param-1-2.9B-Instruct` (5.72 GB; custom `parambharatgen` architecture, may need
   trust_remote_code, which I avoid by default).
4. **Natural romanization (Kannada)**: IndicXlit needs fairseq (painful on Windows/Python 3.12) vs. a free-tier LLM
   with a fixed prompt. Your call; I'd use Gemini free tier with a cached, versioned prompt.
5. **API part of E1**: Gemini count_tokens is free and works with your key; Claude counting needs an Anthropic key.
   Prices in `configs/prices.yaml` are placeholders: may I fetch the official pricing pages?
6. **E5 GATE** (see section 4): budget and vocab grid, plus T4 timing. The Kaggle notebook
   (`notebooks/kaggle/e05_pilot_t4.ipynb`) needs the repo reachable from Kaggle: push to a private GitHub repo, or
   upload as a Kaggle dataset — your choice.
7. IndicSentiment license is not stated on the source card (an mteb mirror says CC0-1.0); needs confirming.

## Decisions I made without you (easy to reverse)

- **Our own ITRANS implementation.** `indic_transliteration` writes short e/o as è/ò (non-ASCII) and does not round
  trip ('.' -> danda, Latin text, vowel hiatus). Ours is ASCII with the Dravidian convention e/E, o/O; vocalic L is
  `L^i` because `LLi` collides with the very common ಳ್ಳಿ; Latin text is escaped `{...}`, native digits `#...#`.
- FLORES-200 as a stand-in for FLORES+; NFC normalization of every input.
- E5 proposed budget 400 MB of text per run, batch 64 x ~1 KiB windows (4 x 16 micro-batches to fit 8 GB), lr 1e-3,
  cosine; one epoch, identical text and order for all conditions; seeds vary only the init.
- Amended one local commit to drop a 29 MB derived parquet from git history (nothing was pushed).

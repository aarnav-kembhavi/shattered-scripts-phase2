# Data card

Every dataset used in this project: source, version/revision, license, splits, sizes, and how it was used.
Nothing is listed here until its availability and license have been verified on the source page.

| Dataset | Source | Revision / checksum | License (verified where) | Splits used | Size used | Experiments | Verified on |
|---|---|---|---|---|---|---|---|
| FLORES-200 (Meta, original release) | https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz | tarball sha256 `b8b0b767…44011f6` (Last-Modified 2022-07-14) | CC-BY-SA 4.0 (github.com/facebookresearch/flores README, "Licenses") | dev (997) + devtest (1012) | 2009 sentences/lang; eng_Latn, kan_Knda, tam_Taml, tel_Telu, mal_Mlym, hin_Deva, ben_Beng | E1 (draft), E2 step 1 (draft) | 2026-10-07 |
| FLORES+ | HF `openlanguagedata/flores_plus` | `e707e62e762a9e2faca3933aa315f4665cc3cd8f` | CC-BY-SA 4.0 (HF card) | dev, devtest | — | E1, E2 (primary since 2026-10-07), E4 (planned) | 2026-10-07; gated, access granted 2026-10-07 |
| Wikipedia, Kannada | HF `wikimedia/wikipedia`, config `20231101.kn` | `b04c8d1ceb2f5cd4588862100d08de323dccfbaa` | CC-BY-SA 3.0 and GFDL (HF card) | train (only split) | 31,437 articles, 149.2M chars | E2 (lossy back-map training, round-trip test), E4a/E9 word frequencies | 2026-10-07 |
| Wikipedia, English (shard 0 of 41) | HF `wikimedia/wikipedia`, config `20231101.en`, file `train-00000-of-00041.parquet` | `b04c8d1ceb2f5cd4588862100d08de323dccfbaa` | CC-BY-SA 3.0 and GFDL (HF card) | train (only split) | 156,289 articles, 700.5M chars | M1 English word-probe contexts | 2026-10-15 |
| TinyStories V2 (GPT-4) | HF `roneneldan/TinyStories`, files `TinyStoriesV2-GPT4-{train,valid}.txt` | `f54c09fd23315a6f9c86f9dc80f725de7d8f9c64` | CDLA-Sharing-1.0 (HF card) | train (2.23 GB), valid (22.5 MB) | E5: first 400 MB of the seeded document shuffle (proposed budget); tokenizers trained on first 100 MB | E5 | 2026-10-07 |
| IndicXNLI | HF `Divyanshu/indicxnli` (files `forward/{dev,test,train}/xnli_kn.json`) | `7092c27872e9` | CC0-1.0 (HF card YAML) | test (kn: 5010, balanced 1670/1670/1670; 0 = entailment, 1 = neutral, 2 = contradiction; chance 33.3%) | — (E0 samples 200) | E0, E2, E3, E8 (planned) | 2026-10-07 |
| IndicSentiment | HF `ai4bharat/IndicSentiment` (files `data/{validation,test}/kn.json`) | `dc8f3f668865` | **not stated on the source card**; mirror `mteb/IndicSentiment` card says CC0-1.0 — to confirm at source (IndicXTREME release) | test (kn: 1000; Positive 506, Negative 492, 2 unlabeled; binary, chance ~50%, not 3-way as the README says). Each item includes the parallel English review. | — | E0, E2, E3 (planned) | 2026-10-07 |
| XNLI (English test) | HF `facebook/xnli`, `en/test-00000-of-00001.parquet` | `b8dd5d7af51114dbda02c0e3f6133f332186418e` | not on HF card; to confirm at source (XNLI repo) | test (5010; verified aligned item-by-item with IndicXNLI kn test: identical label sequence, spot-checked translations) | 200 sampled with IndicXNLI | E0, M-experiments | 2026-10-07 |
| Gemma 4 E2B (model) | HF `google/gemma-4-E2B-it` | — | Apache-2.0 (HF card) | — | text-only, per-layer embeddings on CPU | E0, M1–M6 | 2026-10-07 |

Notes on task data
- IndicXNLI is machine-translated from English XNLI; some Kannada items drift in meaning (e.g. test-1234 hypothesis).
  This is noise we inherit, identical across forms (native and ITRANS are transliterations of the same text).

Derived data
- `data/processed/kn_wiki_wordfreq.parquet`: Kannada word frequencies from Wikipedia 20231101.kn (17.0M word tokens,
  1.49M types, 50,513 types with count >= 30), top 20k annotated with token counts under o200k, Qwen3, Qwen3.5,
  Gemma 4, Sarvam-1 (native and ITRANS). Built by `scripts/build_kn_wordfreq.py`.

Notes
- FLORES-200 Kannada: 17 of 2009 sentences are not NFC-normalized (decomposed vowel signs such as U+0CC6 U+0CC2
  U+0CD5 for ೋ). All experiments NFC-normalize inputs before deriving any form.
- Kannada Wikipedia 20231101: all 31,437 articles are NFC.

## Wikipedia English (shard 0 of 41), for M1 English word probes (added 2026-10-15)
- Source: `wikimedia/wikipedia`, config `20231101.en`, file `train-00000-of-00041.parquet` (420 MB), revision
  b04c8d1ceb2f5cd4588862100d08de323dccfbaa (same pinned revision as the Kannada dump). 156,289 articles.
- License: CC BY-SA 3.0 / GFDL (Wikipedia text), as for the Kannada dump.
- Use: contexts for frequent English words (M1 probes, English reference form). Not used for training.

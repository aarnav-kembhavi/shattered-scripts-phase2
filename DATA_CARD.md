# Data card

Every dataset used in this project: source, version/revision, license, splits, sizes, and how it was used.
Nothing is listed here until its availability and license have been verified on the source page.

| Dataset | Source | Revision / checksum | License (verified where) | Splits used | Size used | Experiments | Verified on |
|---|---|---|---|---|---|---|---|
| FLORES-200 (Meta, original release) | https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz | tarball sha256 `b8b0b767…44011f6` (Last-Modified 2022-07-14) | CC-BY-SA 4.0 (github.com/facebookresearch/flores README, "Licenses") | dev (997) + devtest (1012) | 2009 sentences/lang; eng_Latn, kan_Knda, tam_Taml, tel_Telu, mal_Mlym, hin_Deva, ben_Beng | E1 (draft), E2 step 1 (draft) | 2026-10-07 |
| FLORES+ | HF `openlanguagedata/flores_plus` | `e707e62e762a9e2faca3933aa315f4665cc3cd8f` | CC-BY-SA 4.0 (HF card) | dev, devtest | — | E1, E2 (primary since 2026-10-07), E4 (planned) | 2026-10-07; gated, access granted 2026-10-07 |
| Wikipedia, Kannada | HF `wikimedia/wikipedia`, config `20231101.kn` | `b04c8d1ceb2f5cd4588862100d08de323dccfbaa` | CC-BY-SA 3.0 and GFDL (HF card) | train (only split) | 31,437 articles, 149.2M chars | E2 (lossy back-map training, round-trip test), E4a/E9 word frequencies | 2026-10-07 |
| Wikipedia, English (shard 0 of 41) | HF `wikimedia/wikipedia`, config `20231101.en`, file `train-00000-of-00041.parquet` | `b04c8d1ceb2f5cd4588862100d08de323dccfbaa` | CC-BY-SA 3.0 and GFDL (HF card) | train (only split) | 156,289 articles, 700.5M chars | M1 English word-probe contexts | 2026-10-15 |
| Dakshina v1.0 (Google Research), official release: `kn` and `hi` romanized | https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar (github.com/google-research-datasets/dakshina) | tarball MD5 `pWCGix1nAmAsTqToN5T6Jg==` (base64; matches Google's published hash), Last-Modified 2020-05-27 | CC BY-SA 4.0 (README in the tarball and on GitHub, "License") | romanized rejoined: dev 5,000 + test 5,000 per language | kn: 10,000 strings, 1.11M romanized chars; hi: 10,000 strings, 1.03M romanized chars | NC1 post hoc frequency reference (kn); K3b (draft) | 2026-10-23 |
| Dakshina (Google Research), Kannada, romanized Wikipedia sentences | HF mirror `Anvesh-Lankala/Copy_Dakshina_Google_research_dataset`, file `data/kn-00000-of-00001.parquet` (original: github.com/google-research-datasets/dakshina) | `765309607a263b86d25a5bd1a4fa20ef34a87a85` | CC-BY-SA 4.0 (mirror HF card; the original Dakshina release is CC BY-SA 4.0) | kn (only) | 10,000 sentences, 1.11M romanized chars | first run of the NC1 post hoc reference; superseded by the official files (identical) | 2026-10-22 |
| TinyStories V2 (GPT-4) | HF `roneneldan/TinyStories`, files `TinyStoriesV2-GPT4-{train,valid}.txt` | `f54c09fd23315a6f9c86f9dc80f725de7d8f9c64` | CDLA-Sharing-1.0 (HF card) | train (2.23 GB), valid (22.5 MB) | E5: first 400 MB of the seeded document shuffle (proposed budget); tokenizers trained on first 100 MB | E5 | 2026-10-07 |
| IndicXNLI | HF `Divyanshu/indicxnli` (files `forward/{dev,test,train}/xnli_kn.json`) | `7092c27872e9` | CC0-1.0 (HF card YAML) | test (kn: 5010, balanced 1670/1670/1670; 0 = entailment, 1 = neutral, 2 = contradiction; chance 33.3%) | — (E0 samples 200) | E0, E2, E3, E8 (planned) | 2026-10-07 |
| IndicSentiment | HF `ai4bharat/IndicSentiment` (files `data/{validation,test}/kn.json`) | `dc8f3f668865` | **not stated on the source card**; mirror `mteb/IndicSentiment` card says CC0-1.0 — to confirm at source (IndicXTREME release) | test (kn: 1000; Positive 506, Negative 492, 2 unlabeled; binary, chance ~50%, not 3-way as the README says). Each item includes the parallel English review. | — | E0, E2, E3 (planned) | 2026-10-07 |
| XNLI (English test) | HF `facebook/xnli`, `en/test-00000-of-00001.parquet` | `b8dd5d7af51114dbda02c0e3f6133f332186418e` | not on HF card; to confirm at source (XNLI repo) | test (5010; verified aligned item-by-item with IndicXNLI kn test: identical label sequence, spot-checked translations) | 200 sampled with IndicXNLI | E0, M-experiments | 2026-10-07 |
| SIB-200 | HF `Davlan/sib200` (files `data/{kan_Knda,eng_Latn}/{train,dev,test}.tsv`) | `38977a667f6fc264d5c26ec57a01e16db040b358` | CC-BY-SA 4.0 (HF card YAML; card prose says "CC 4.0 Commercial"; derived from FLORES-200, CC-BY-SA 4.0); not gated | train 701 + dev 99 + test 204 = 1,004 per language, 7 topics (chance 14.3%); `index_id` = 0-based position in FLORES dev+devtest, all 1,004 kn and en texts equal FLORES+ at that position after NFC | all 1,004 | E0c | 2026-10-16 |
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

## Dakshina Kannada romanized sentences, for the NC1 post hoc frequency reference (added 2026-10-22)
- Source: third-party HF mirror `Anvesh-Lankala/Copy_Dakshina_Google_research_dataset` (revision
  765309607a263b86d25a5bd1a4fa20ef34a87a85), `data/kn-00000-of-00001.parquet` (5.1 MB) in `data/raw/dakshina/`.
  Columns `native`, `romanized` (manual romanization of Kannada Wikipedia sentences), plus lexicon/alignment columns.
  The full original release (2 GB tarball) was not downloaded; the mirror was not checked against it.
- License: CC BY-SA 4.0 (mirror card; matches the original release).
- Use: romanized Kannada half of the post hoc piece-frequency reference (`scripts/nc1_posthoc.py`); no evaluation
  item overlaps it (exact match and containment, >= 20 chars: 0 dropped). Not used for training or evaluation.

## Dakshina v1.0, official release (added 2026-10-23)
- Source: https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar (2.0 GB, 2,008,340,480 bytes),
  linked from github.com/google-research-datasets/dakshina. Streamed once; MD5 of the full stream equals the published
  `x-goog-hash` (pWCGix1nAmAsTqToN5T6Jg==). Only `kn/romanized/*`, `hi/romanized/*` and `README.md` were kept, in
  `data/raw/dakshina_official/` (not committed; `data/raw` is ignored).
- License: CC BY-SA 4.0 (README "License" section, in the tarball and on GitHub).
- Content: per language, 10,000 Wikipedia strings romanized by native-speaker annotators (strings of 30+ words split for
  annotation; `*.rejoined.tsv` rejoins them), shuffled into dev and test (5,000 each).
- Mirror check: the HF mirror's `kn` parquet equals the official `kn.romanized.rejoined.tsv` row by row (10,000 of 10,000,
  native and romanized; 50 of 50 in a seeded spot check). The official files are used from 2026-10-23.

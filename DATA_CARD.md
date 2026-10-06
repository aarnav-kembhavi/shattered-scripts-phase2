# Data card

Every dataset used in this project: source, version/revision, license, splits, sizes, and how it was used.
Nothing is listed here until its availability and license have been verified on the source page.

| Dataset | Source | Revision / checksum | License (verified where) | Splits used | Size used | Experiments | Verified on |
|---|---|---|---|---|---|---|---|
| FLORES-200 (Meta, original release) | https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz | tarball sha256 `b8b0b767…44011f6` (Last-Modified 2022-07-14) | CC-BY-SA 4.0 (github.com/facebookresearch/flores README, "Licenses") | dev (997) + devtest (1012) | 2009 sentences/lang; eng_Latn, kan_Knda, tam_Taml, tel_Telu, mal_Mlym, hin_Deva, ben_Beng | E1 (draft), E2 step 1 (draft) | 2026-10-07 |
| FLORES+ | HF `openlanguagedata/flores_plus` | `e707e62e762a9e2faca3933aa315f4665cc3cd8f` | CC-BY-SA 4.0 (HF card) | dev, devtest | — | E1, E2, E4 (planned) | 2026-10-07; **gated (auto-approve), terms not yet accepted** |
| Wikipedia, Kannada | HF `wikimedia/wikipedia`, config `20231101.kn` | `b04c8d1ceb2f5cd4588862100d08de323dccfbaa` | CC-BY-SA 3.0 and GFDL (HF card) | train (only split) | 31,437 articles, 149.2M chars | E2 (lossy back-map training, round-trip test), E4a/E9 word frequencies | 2026-10-07 |

Notes
- FLORES-200 Kannada: 17 of 2009 sentences are not NFC-normalized (decomposed vowel signs such as U+0CC6 U+0CC2
  U+0CD5 for ೋ). All experiments NFC-normalize inputs before deriving any form.
- Kannada Wikipedia 20231101: all 31,437 articles are NFC.

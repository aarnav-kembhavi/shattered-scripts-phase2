# Shattered Scripts: code, data and results

Anonymous code, data and results for a study of how small language models read **Kannada** in different written forms:
native script, and several Latin-letter romanizations. The question is whether the way a tokenizer *fragments* a written form
or how *familiar* the form is to the model better explains why romanized Kannada is read worse than native script.

> This repository is the anonymized release for review. It contains the code, the data we produced, and every result file the
> analyses read. It does not contain the paper source, model weights, activation caches or raw third-party downloads (see
> "What is not included").

## Short summary of what was found

All statements are about the models we tested (about 1.5 to 2.5 billion parameters; some experiments extend to 8B and one
4-bit 23.6B model) and about Kannada, with Hindi, Bengali and Telugu as comparisons. Our evidence tracks familiarity of the
written form more than fragmentation; the registered head-to-head comparison of the two is inconclusive, so we do not claim that
either outweighs the other.

- **Native script wins.** Native Kannada beats lossless ASCII romanization (ITRANS) on SIB-200 topic accuracy in all five small
  models and in all seven counted models up to 23.6B, and beats a lossy lowercase romanization in four of five small models.
  Natural (typed-style) romanization is never significantly above native.
- **Word assembly follows fragmentation; meaning follows familiarity.** The layer at which a word is assembled (an MDL probe)
  moves with how many pieces the tokenizer makes, while alignment with the English translation and task accuracy move with the
  familiarity of the form.
- **Tiny GPTs with only the vocabulary varied** (identical training data): more fragmentation delays word assembly slightly,
  but the bits-per-byte cost does not survive a control that equalizes embedding capacity (registered prediction that failed).
- **Causal evidence.** Patching native word-final states into the lossy-romanized run restores about 0.37 to 0.6 of the native
  advantage at early and middle layers; the cost of an unfamiliar form is spread over a word's pieces and concentrated in a subset
  of items.
- **Manipulating familiarity.** Continuing pretraining of Sarvam-1 on ITRANS Kannada closes more of the native-minus-ITRANS gap
  than the same amount of native or English text (accuracy +0.19 to +0.22, retrieval +0.34 to +0.41, four seeds). The model stays
  below native level, and the form trained on is also the form evaluated.
- **Replication in other languages.** Bengali and Telugu reproduce the Kannada pattern; the native-minus-natural gap is larger
  for Kannada than for Hindi.
- **Predictions that failed or were not decided are reported**, not hidden: the bits-per-byte cost, the patching threshold, a second
  prompt template, a cipher-exposure test (at a retrieval ceiling), forced segmentations at matched piece frequency, a 4-bit control
  (partly supported), and Gemini's romanization against human romanization (refuted in Kannada, Bengali and Telugu).

Where each number comes from: `results/phase2/RESULTS_READABLE.md` (one block per experiment with the full outcome and file
paths), `results/phase2/REGISTERED_OUTCOMES.md` (every registered outcome word and status), and
`results/phase2/PHASE2_CLAIMS_TABLE.md`.

## Written forms used

| Form | What it is |
|---|---|
| native | Kannada script (NFC) |
| ITRANS | lossless ASCII romanization with capitals; round-trips all 2,009 FLORES+ sentences |
| lowercase | lossless scheme without capitals, picked by a search over reversible schemes |
| lossy | merges sounds the script keeps apart (long/short vowels, retroflex/dental, aspirated/unaspirated), lowercase |
| natural | what people type: drafted by an LLM (`gemini-3.5-flash-lite`, temperature 0, one fixed prompt), English words kept |
| Kanglish | romanized Kannada mixed with English, on a verified subset |
| English | the parallel English text |
| non-canonical | the lossy text forced into an unfamiliar tokenization (same piece count per word) |

Natural romanizations are model drafts; native speakers verified 500 of them (200 sentiment items and 300 FLORES+ items). Only
those subsets are described as human-verified. The prompt and filtering for each language are in `scripts/e02_natural.py`,
`scripts/m4c_natural_flores.py`, `scripts/h_hindi.py` and `scripts/x4_natural.py`.

## Measures

- **Accuracy**: log-likelihood of English label words after an English instruction, calibrated with content-free inputs
  ("N/A", "", "[MASK]"), with a fallback to raw scores if calibration lowers English accuracy by more than 5 points.
- **Alignment**: unmapped retrieval of the English translation by cosine similarity of mean-pooled residual states (acc@1), at
  the layer chosen on a train half.
- **Word assembly**: first layer whose word-identity probe reaches 90 percent of its maximum compression (MDL probing).
- **Causal evidence**: word-aligned activation patching; recovery R = share of the source-minus-destination gold-label margin
  restored.
- **Statistics**: exact McNemar tests with Holm correction, 95 percent paired bootstrap intervals (10,000 resamples over items,
  seed 0). Experiments were registered before they were run; later additions are labelled post hoc or exploratory.

## Repository layout

| Path | Holds |
|---|---|
| `src/shattered/` | library: data loaders, tokenizer tools, transliteration and lossy rules, LLM client with response cache, pretraining, probes and patching, statistics, plots |
| `scripts/` | one entry point per experiment (flat on purpose: scripts import each other); table below. Each docstring states its usage and outputs |
| `configs/` | run configs for the cost atlas, the tiny-GPT grid, API prices |
| `tests/` | unit tests (`pytest`) for transliteration, alignment, pretraining, probes, patching and the LLM client |
| `results/<experiment>/` | outputs of each experiment: CSV and JSON files carrying the config and git commit that produced them |
| `results/phase2/` | the second set of experiments (X1 to X15), with `RESULTS_READABLE.md`, `REGISTERED_OUTCOMES.md`, `PHASE2_CLAIMS_TABLE.md` |
| `results/kaggle/` | scored outputs of the jobs run on Kaggle GPUs (the larger models): per-item parquet files and JSON summaries, and queue and quota records |
| `data/annotation/` | annotation items, Gemini drafts and the native-speaker verified texts, with `DATASHEET.md` |
| `data/processed/` | natural-romanization drafts (all versions) for Kannada, Hindi, Bengali and Telugu |
| `annotation/` | annotator instructions, examples, the verified-annotation table and the merge script (no annotator identities) |
| `docs/BRIEF.md` | the experiment brief the first set of experiments followed |
| `DATA_CARD.md` | every dataset used: source, revision, license, splits, sizes, use |

## Setup

Python 3.12, one consumer GPU (the small-model experiments ran on an 8 GB laptop GPU in bf16, one model load at a time).

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python torch --index-url https://download.pytorch.org/whl/cu126   # use .venv/Scripts/python.exe on Windows
uv pip install --python .venv/bin/python -r requirements.txt -e .
cp .env.example .env          # keys are only needed to re-draft romanizations or call hosted models; the response cache is not included
python scripts/env_check.py
pytest tests
```

Model weights download from the Hugging Face Hub on first use. Gated models (Llama) need an accepted license and a token.

## Experiments: what to run

Entry points; the analysis step of each is CPU-only and reads stored scores. Outputs are in the folders named.

### First set (Phase 1)

| Experiment | Entry point | Output |
|---|---|---|
| E0 model gate, tokens per word | `e00_gate.py`, `e00_tokens_per_word.py` | `results/e00_gate` |
| E1 token-cost atlas (context) | `e01_cost.py --config configs/e01_cost.yaml`, `e01_plots.py` | `results/e01_cost*` |
| E2 transliteration schemes | `e02_translit.py`; reversible lowercase search `e09_search.py`, `e09_capitals.py`, `e09_eval.py` | `results/e02_translit`, `results/e09_romanize` |
| E5 tiny GPTs (vocabulary varied, data fixed) | `e05_pretrain.py prepare / train`, `e05_analysis.py` | `results/e05_pretrain` |
| M1 tiny-model probes (MDL, erasure) | `m1_tiny_mdl.py`, `m1_tiny_probes.py` | `results/m1_tiny_mdl`, `results/m1_tiny` |
| M1/M4 pretrained models (assembly layer, alignment) | `m14_full.py`, `m14_gate2.py`, `m4b_mapping.py`, `m4b_robustness.py`, `m4b_surface.py` | `results/m14_full`, `results/m4b_*` |
| M4c natural-romanization alignment | `m4c_natural_flores.py romanize / forward / analyse`, `m4c_curves.py`, `m4c_surface.py` | `results/m4c_*` |
| Accuracy across forms (sentiment, SIB-200) | `e0b_familiarity.py`, `e0c_sib.py score / analyse` | `results/e0b_familiarity`, `results/e0c_sib` |
| Back-translation check | `e0b_backtranslate.py`, `e0b_backtranslate_control.py` | `results/e0b_natural_check` |
| Ladder L1 to L3 (casing, fragmentation, spelling) | `l_ladder.py forward / score / analyse`, `l_ladder_posthoc.py` | `results/l_ladder*` |
| NC1 forced non-canonical tokenization | `nc1.py chars / forward / score / analyse`, `nc1_posthoc.py`, `nc1_piece_frequency.py` | `results/nc1*` |
| E-P1, E-P2 activation patching; EP-R | `ep_patching.py`, `ep_robust.py run / analyse` | `results/ep1`, `ep2`, `ep_robust` |
| H1 Kannada against Hindi; H1-LF | `h_hindi.py`, `h1lf.py`, `h1lf_selection.py` | `results/h_hindi`, `results/h1lf` |
| K3b Gemini against human romanization | `k3b_dakshina.py sample / draft / analyse [hi]` | `results/k3b`, `results/k3b_hi` |
| K1, K2 (verified Kanglish), K2b controls | `k_k12.py`, `k2b_overlap.py`, `k2b_strata.py`, `k2b_units.py`, `codemix_check.py` | `results/k12`, `results/codemix_check` |
| V-VER, V-DBL (verification, vowel doubling) | `k_verified.py`, `v_ver.py`, `v_dbl.py` | `results/v_ver`, `results/v_dbl` |
| Matched samples for the main tables | `matched_samples.py` | `results/matched` |

### Second set (Phase 2), outputs under `results/phase2/<id>/`

| Id | What it tests | Entry points |
|---|---|---|
| X1 | a second prompt template; T3: instruction in Kannada (exploratory) | `x1_t2.py`, `x1_analyse.py`, `x1_t3_draft.py`, `x1_analyse_t3.py` |
| X2 | measured share of romanized text on the web (FineWeb-2) per language | `x2_exposure.py` |
| X3 | frequency-matched non-canonical tokenization of lossy Kannada | `x3.py`, `x3_analyse.py`, `x3_regress.py` |
| X4, X5 | Bengali and Telugu replication; cross-language consistency with measured exposure | `x4_*.py`, `x5_analyse.py` |
| X6 | screening of further small models | `x6_screen.py`, `x6_run.py` |
| X7, X7-A | tiny GPTs with a factorized embedding (equal capacity control) and assembly layer | `x7_control.py`, `x7_analyse.py`, `x7a_mdl.py` |
| X8 | blind second annotator on 100 sentences (agreement) | `x8_page.py`, `analyze_x8.py` |
| X9a | tiny GPT with familiarity manipulated and fragmentation fixed (cipher exposure) | `x9a.py`, `x9a_cipher_tokens.py` |
| X9b | continued pretraining (QLoRA) on ITRANS, native or English Kannada text | `x9b_streams.py`, `kaggle_x9b.py`, `x9b_analyse.py` |
| X10 | Kannada to English generation (chrF), native against ITRANS | `x10.py`, `kaggle_x10.py`, `x10_sarvam_m_analyse.py` |
| X11 | 4-bit quantization control | `x11.py` |
| X12 | exposure transfer with Llama-2-7B against its Kannada-extended variant; instruction pair | `x12_tokenizers.py`, `x12_analyse.py`, `x12_contrast2.py` |
| X13 | larger models (Qwen3-8B, Llama-3.1-8B, Sarvam-m 23.6B in 4-bit) | `x_score.py`, `x13_analyse.py`, `x13_mdl_analyse.py`, `x13_sarvam_m.py` |
| X14 | hosted black-box models (exploratory) | `x14_models.py`, `x14_run.py`, `x14_analyse.py` |
| X15 | human intelligibility baseline | not run (annotators were not available) |

The larger-model jobs ran on Kaggle GPUs through `kaggle_runner.py` and `kaggle_queue.py`; a reproducibility gate against the
laptop results is in `kaggle_gate.py`, `kaggle_precision.py` and `kaggle_retrieval_gate.py`.

## Rebuilding results

1. Regenerate what is not included (below).
2. Run an experiment's entry point; its `analyse` step recomputes the result files from stored scores, for example
   `python scripts/e0c_sib.py analyse`, `python scripts/x13_analyse.py`, `python scripts/x9b_analyse.py`.
3. `python scripts/results_readable2.py` rebuilds `results/phase2/RESULTS_READABLE.md` from the result files.

Docstrings and some result headers refer to a dated registration log (`RESULTS.md`). That log is not part of this release.

## What is not included

| Not in the repository | Why and how to regenerate |
|---|---|
| paper source and figures | not part of the code release |
| model weights, tiny-GPT checkpoints, LoRA adapters | large; train with `e05_pretrain.py` (about 8.3 h GPU for the full grid) and `kaggle_x9b.py` |
| activation caches, `results/k12/vectors/` | large and regenerable with each experiment's `forward` step (about 4 to 6 h GPU in total; K2b vectors about 40 min) |
| raw third-party data (`data/raw/`) | download from the sources and revisions in `DATA_CARD.md` |
| LLM response cache | not shareable; re-drafting romanizations needs API quota (all drafts are included in `data/processed/` and `data/annotation/`) |
| annotator workbooks and private keys | contain annotator metadata; the verified texts and instructions are included |
| run logs, chain launchers, cleanup and packaging helpers | process leftovers, not needed to reproduce |

## Data and ethics

- Datasets and licenses: `DATA_CARD.md`. Annotation protocol and provenance: `data/annotation/DATASHEET.md`.
- Annotation was done by volunteer native Kannada speakers who gave informed consent; no personal data are recorded and
  annotator identities are not stored with the items.
- Some experiments used hosted LLM APIs (romanization drafts and, for context, back-translation and hosted-model classification);
  prompts, models and settings are in the scripts named above.
- No license file is included in this anonymous release; dataset licenses are in `DATA_CARD.md`.

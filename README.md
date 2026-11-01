# Shattered Scripts

Code, data and paper for "Shattered Scripts: Familiarity Outweighs Fragmentation in How Language Models Read Romanized Kannada"
(TMLR submission, anonymous mode). An interpretability study of tokenizer-fragmented Kannada in tiny GPTs and in pretrained models of about two billion
parameters or fewer (Qwen2.5-1.5B, Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; each experiment states which it uses), plus a Hindi comparison.

- Rules, thesis and what is already known: `CLAUDE.md`. Full experiment brief: `docs/BRIEF.md`.
- **Every registered prediction, decision and result, dated:** `RESULTS.md`. Datasets and licenses: `DATA_CARD.md`.
- Every number in the paper traces to a file in `results/` (see "Rebuild the paper").
- The cleanup of 2026-10-30 is described in `docs/CLEANUP_PLAN.md`; the archived items are listed in `../shattered-scripts-archive/MANIFEST.md`.

## What is in each folder

| Folder | Holds |
|---|---|
| `paper2/` | `main.tex` (TMLR style, one merged file; the sections are cut out by `check_numbers.py`), generated `tables/` and `figures/`, `refs.bib`, and `paper2/scripts/` (`make_tables.py`, `make_figures.py`, `check_numbers.py` with the claim files `section_claims*.py`, `pages.py`, `build_paper.sh`) |
| `src/shattered/` | the library: data loaders, tokenizer tools, transliteration, LLM client with cache, pretraining, interpretability, stats, plots |
| `scripts/` | experiment entry points and chain launchers (flat on purpose: scripts import each other and the chains call them by path; table below) |
| `results/<experiment>/` | outputs of one experiment each: CSV and JSON with the config and commit that produced them. `results/CHAIN_STATUS_K3BHI.md` and the logs of running chains stay here |
| `data/raw/` | downloads (FLORES, SIB-200, IndicSentiment, Dakshina, TinyStories, Wikipedia); not in git |
| `data/processed/` | natural-romanization drafts from Gemini (all versions), word lists, E5 token streams (not in git) |
| `data/annotation/` | annotation items, drafts and the verified texts from annotator A |
| `annotation/` | annotation workbooks, instructions and templates (never distributed until the lead author says so) |
| `cache/` | `llm_cache.sqlite` (every API response; never delete) and `activations/` (large, regenerable, not in git) |
| `checkpoints/e05/` | the 18 final E5 tiny-GPT weights (`run_v*_s*/final.safetensors`), loaded by `e05_pretrain.py`, `m1_tiny_mdl.py` and `m1_tiny_probes.py` |
| `docs/` | brief, preregistration drafts, the cleanup plan, reference PDFs |
| `configs/`, `tests/` | run configs; unit tests |

## Setup (Windows or Linux, one consumer GPU)

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe torch --index-url https://download.pytorch.org/whl/cu126
uv pip install --python .venv/Scripts/python.exe -r requirements.txt -e .
cp .env.example .env     # API keys (Gemini free tier); never an Anthropic key
python scripts/env_check.py
```

Interpretability runs in bf16 only, one model load at a time, with a GPU guard first (`shattered.gpuguard`).

## Rebuild the paper

```bash
bash paper2/scripts/build_paper.sh                       # pdflatex + bibtex into paper2/build/, prints LaTeX errors, undefined citations, pages
python paper2/scripts/make_tables.py                     # paper2/tables/*.tex from results/ (a cell with no result file is marked MISSING)
python paper2/scripts/make_figures.py                    # paper2/figures/*.pdf from results/
python paper2/scripts/pages.py                           # main-text pages (TMLR asks for at most 12 before the appendix)
for s in intro related setup controlled accuracy assembly familiarity limitations conclusion broader_impact abstract appendix; do
  python paper2/scripts/check_numbers.py --section $s     # every number in the text against its result file
done
python scripts/anon_package.py                          # anonymized supplementary zip in build/ with an identifying-string scan
```

## Regenerating what is not in git

| What | How | Cost (estimate from the logs in RESULTS.md) |
|---|---|---|
| `cache/activations/m14full/`, `h_hindi/`, `nc1/` | `scripts/m14_full.py`, `l_ladder.py forward`, `m4c_natural_flores.py forward`, `v_ver.py forward`, `v_dbl.py forward`, `h_hindi.py forward`, `nc1.py forward` | about 4 to 6 h GPU in total, one model per load |
| `results/k12/vectors/*.npz` (K2b vectors, 121 MB, untracked) | `python scripts/k_k12.py forward <model>` for `qwen2.5-1.5b`, `qwen3.5-2b`, `sarvam-1`, `gemma4-e2b`, then `python scripts/k_k12.py analyse` | about 40 min GPU |
| `checkpoints/e05/`, `data/processed/e05/*.npy` | `python scripts/e05_pretrain.py prepare`, then one run per condition: `python scripts/e05_pretrain.py train --vocab <V> --seed <S>` (resumable; vocabularies and seeds in `configs/e05_pretrain.yaml`) | about 8.3 h GPU for the full grid |
| `cache/llm_cache.sqlite` | keeps itself; re-drafting needs days of Gemini quota, so never delete | days |

## Experiments: what to run

Every experiment was registered in `RESULTS.md` before it ran; its script is documented in its docstring (usage and outputs).

| Experiment | Entry point (analysis step is CPU) | Output |
|---|---|---|
| E0 model gate, tokens per word | `e00_gate.py`, `e00_tokens_per_word.py` | `results/e00_gate` |
| E1 token-cost atlas (context) | `e01_cost.py --config configs/e01_cost.yaml`, `e01_plots.py` | `results/e01_cost*` |
| E2 transliteration schemes | `e02_translit.py` | `results/e02_translit` |
| E5 tiny GPTs (controlled pretraining) | `e05_pretrain.py prepare / train`, then `e05_analysis.py` | `results/e05_pretrain` |
| M1 tiny-model probes (MDL, erasure) | `m1_tiny_mdl.py`, `m1_tiny_probes.py` | `results/m1_tiny_mdl`, `results/m1_tiny` |
| M1/M4 pretrained models (assembly layer, alignment) | `m14_full.py`, then `m14_gate2.py`; `m4b_mapping.py`, `m4b_robustness.py`, `m4b_surface.py` | `results/m14_full`, `results/m4b_*` |
| M4c natural romanization alignment | `m4c_natural_flores.py romanize / forward / analyse`, `m4c_curves.py`, `m4c_surface.py` | `results/m4c_*` |
| Accuracy across forms (sentiment, SIB-200) | `e0b_familiarity.py`, `e0c_sib.py score / analyse` | `results/e0b_familiarity`, `results/e0c_sib` |
| Back-translation check | `e0b_backtranslate.py`, `e0b_backtranslate_control.py` | `results/e0b_natural_check` |
| Ladder L1 to L3 | `l_ladder.py forward / score / analyse`, `l_ladder_posthoc.py` | `results/l_ladder*` |
| NC1 forced non-canonical tokenization | `nc1.py chars / forward / score / analyse`, `nc1_posthoc.py`, `nc1_piece_frequency.py` | `results/nc1*` |
| E-P1, E-P2 activation patching; EP-R | `ep_patching.py`, `ep_robust.py run / analyse` | `results/ep1`, `ep2`, `ep_robust` |
| H1 Kannada against Hindi; H1-LF | `h_hindi.py check / draft / forward / score / analyse` (H1); `h1lf.py draft / score / score check / analyse1`, `h1lf_selection.py` | `results/h_hindi`, `results/h1lf` |
| K3b Gemini against human romanization | `k3b_dakshina.py sample / draft / analyse [hi]` | `results/k3b`, `results/k3b_hi` |
| K1, K2 on verified Kanglish; K2b controls | `k_k12.py pilot / score / forward / analyse`, `k2b_overlap.py`, `k2b_strata.py`, `k2b_units.py`, `codemix_check.py` | `results/k12`, `results/codemix_check` |
| V-VER, V-DBL (verification and vowel doubling) | `k_verified.py`, `v_ver.py forward / score / analyse`, `v_dbl.py build / tpw / forward / score / analyse` | `results/v_ver`, `results/v_dbl` |
| Matched samples for the main tables | `matched_samples.py` | `results/matched` |

Long runs are detached Windows scheduled tasks (`scripts/detach.ps1 -Name <x> -Script scripts/<chain>.sh`) that source `scripts/chainlib.sh`
(heartbeat, quota waits from the clock, network failures retried with backoff, GPU guard). Only `ShatteredScripts_k3bhi` and
`ShatteredScripts_watch` are still registered.

## Scripts: role and experiment

Roles: **active** = produces a result the paper reads; **supporting** = helper, drafting, annotation packaging, chain launcher or tooling;
**superseded** = replaced or dropped, kept because a reported result in `RESULTS.md` came from it or another script imports it.

| Script | Experiment | Role |
|---|---|---|
| `e00_gate.py`, `e00_tokens_per_word.py` | E0 gate | active |
| `e00_candidates.py` | E0 candidate model list | superseded (reported in `results/e00_gate/candidates.json`) |
| `e01_cost.py`, `e01_plots.py` | E1 cost atlas | supporting (context, not read by the paper) |
| `e02_translit.py` | E2 transliteration | active |
| `e02_natural.py`, `e0b_natural.py`, `build_kn_wordfreq.py` | natural-romanization drafting, word list | supporting |
| `e05_pretrain.py`, `e05_analysis.py` | E5 tiny GPTs | active |
| `m1_tiny_mdl.py` | M1 tiny-model MDL and erasure probes | active |
| `m1_tiny_probes.py` | M1 tiny-model probes | supporting (imported by `m1_tiny_mdl.py`) |
| `m1_patchscopes.py` | M1a Patchscopes (fails on Kannada at this size) | superseded (MDL probe is primary) |
| `m14_full.py`, `m14_gate2.py` | M1/M4 on four pretrained models | active |
| `m14_pilot.py` | M14 pilot | superseded (`results/m14_pilot`) |
| `m4b_mapping.py`, `m4b_robustness.py`, `m4b_surface.py` | M4b linear mapping | active |
| `m4c_natural_flores.py`, `m4c_curves.py`, `m4c_surface.py` | M4c natural-form alignment | active |
| `e0b_familiarity.py`, `e0c_sib.py` | accuracy across forms | active |
| `e0b_backtranslate.py`, `e0b_backtranslate_control.py` | back-translation check | active (appendix) |
| `e0b_item_fragmentation.py` | item-level fragmentation (exploratory) | supporting |
| `e0b_check_sheet.py` | 50-item hand-check sheet for E0 | superseded (by the K verification protocol) |
| `english_share.py` | English-word share | active |
| `l_ladder.py`, `l_ladder_posthoc.py` | romanization ladder | active |
| `l_ladder_net.py`, `l3_loanfree_register.py` | ladder post hoc descriptives | supporting |
| `nc1.py`, `nc1_posthoc.py`, `nc1_piece_frequency.py` | NC1 | active |
| `ep_patching.py`, `ep_robust.py` | E-P1, E-P2, EP-R | active |
| `h_hindi.py`, `h1lf.py`, `h1lf_selection.py` | H1 Hindi, H1-LF | active |
| `k3b_dakshina.py` | K3b and K3b-hi | active |
| `k_k12.py`, `k_verified.py`, `codemix_check.py` | K1, K2, verified texts, tagger check | active |
| `k2b_overlap.py`, `k2b_strata.py`, `k2b_units.py` | K2b overlap control | active |
| `v_ver.py`, `v_dbl.py` | V-VER, V-DBL | active |
| `matched_samples.py` | matched samples | active |
| `k_annotation.py`, `k_package.py`, `k_xlsx.py`, `k_xlsx_selftest.py` | annotation items, packages, workbooks | supporting |
| `e09_search.py`, `e09_capitals.py`, `e09_eval.py` | E9 reversible romanization (dropped; negative result in `RESULTS.md`) | superseded (`e09_eval.py` is imported by `l_ladder.py`) |
| `anon_package.py` | anonymized supplementary package | supporting |
| `chain.sh`, `chainlib.sh`, `chain_watch.sh`, `detach.ps1`, `hidden.vbs`, `*_chain.sh` | detached chains | supporting |
| `env_check.py` | environment printout | supporting |

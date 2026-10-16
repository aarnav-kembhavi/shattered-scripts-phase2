# Shattered Scripts — project memory

Paper: "Shattered Scripts: How Tokenizer Fragmentation Taxes the Cost, Depth and Accuracy of Multilingual LLMs."
Lead author: Aarnav. Claude Code is the research engineer: builds the code, runs experiments, reports results honestly.
The full experiment brief (E0–E9, gates, predictions) is in `docs/BRIEF.md`. Read it before starting a new experiment.

## Thesis

English-centric tokenizers split Indian scripts (Kannada especially) into many byte-level fragments. We claim that this
fragmentation, independent of how much training data a language had, (a) raises API cost, and (b) forces the model to
spend early layers reassembling words, which leaves less depth for meaning and lowers accuracy. We also propose a cheap,
model-free fix: a tokenizer-optimal, fully reversible romanization applied to the input.

## The central confound we must beat

Every cross-language comparison confounds fragmentation with training-data scarcity: Kannada is both more fragmented and
less represented in pretraining than English. A reviewer will say "it is just less data." The paper survives only if at
least one experiment varies fragmentation while holding data fixed. That experiment is **E5 (controlled pretraining)**.
Treat E5 as the most important experiment in the project.

## What is already known (do not claim these as new)

- Petrov et al. 2023: non-English text costs more tokens.
- RomanSetu (ACL 2024): finetuning on romanized Indic text works as well as native-script finetuning.
- RomanLens (Findings ACL 2025): middle layers represent Indic words in Latin script ("latent romanization"); native and
  romanized inputs share concept representations. They note logit lens breaks on byte-fragmented scripts and leave the
  "why" open.
- Feucht et al. 2024 (token erasure) and Kaplan et al. 2024 (From Tokens to Words, inner lexicon): early layers merge
  multi-token English words.
- Goldman et al. 2024 (compression correlates with performance) vs Schmidt et al. 2024 (compression alone does not
  explain performance).
- 5 Dialects BN (2026): romanized Bangla underperforms native script, blamed on lossy romanization.
- KanCMD and DravidianLangTech: Kannada–English code-mixed data already exists (not parallel, not built for LLM eval).
- **FragMend** (Mehta, Subramani, Xu, Gupta, Srikumar; arXiv 2604.16656, 17 Apr 2026; code github.com/utahnlp/fragmend):
  interpretability-based vocabulary expansion for over-fragmented (mostly non-Latin) languages, built on Tokens2Words
  (Kaplan et al. 2025). Uses Patchscopes to find the earliest layer where a word (and, new in FragMend, a subword prefix)
  is "detokenized"; shows **subword detokenization** (prefixes merge progressively before the full word); initializes
  new embeddings from hidden states at that layer via Procrustes maps; ~20 pt gains over baseline inits for non-Latin
  languages; Qwen3-30B-A3B primary, Qwen3.5-{0.8B..9B} for scale. Their Patchscopes setup (from the code): the word is
  encoded alone with BOS, last-token hidden state at every layer, patched into every placeholder of "X, X, X, X," at the
  input-embedding level, 20 greedy tokens, detokenized at the first layer whose output starts with the word
  (letter-boundary regex; "first_id_layer"). **They already cover Patchscopes detokenization and vocabulary expansion
  for non-Latin scripts: we do not claim either. Our E7 and E9 are dropped.**

## Our contributions (what is actually new) — revised 2026-10-07: the paper is interpretability-first

1. A controlled experiment isolating fragmentation from training data (E5), with detokenization/circuit analyses
   applied to the tiny models.
2. A layer-wise mechanism (M1–M6) on Qwen 2.5/3, Qwen 3.5, Gemma 4 E2B and Sarvam-1, each on native Kannada, ITRANS and
   English: detokenization layer per word (Patchscopes replicating FragMend + linear probes), item-level link to errors,
   detokenization circuits, alignment lag, latent English, and an injection intervention.
3. A **crossover design**: native-vs-ITRANS fragmentation flips across families (ITRANS less fragmented on Qwen, more on
   Gemma 4 / Sarvam-1; `results/e00_gate/tokens_per_word.csv`), which separates fragmentation from script.
4. The token-cost atlas (E1) as context; a parallel Kannada set (E2) in native/ITRANS/lossy/natural forms (Kanglish
   optional).

## Direction changes (2026-10-07, Aarnav)

- No Anthropic key, ever: Claude token counting is dropped from E1 (stated as a limitation).
- E9 dropped (negative result recorded: searched reversible schemes save 1.0–4.8% over ITRANS held out). E7 dropped
  (FragMend covers vocabulary expansion).
- E3 shrinks to a small context table; Kanglish is optional.
- New experiments M1–M6 (see docs/BRIEF.md). Pre-registered predictions go into RESULTS.md before each runs; every M
  experiment is piloted on 50 items with a time estimate before its full run.
- E5 keeps running untouched; M1 and M3 will later be applied to the tiny E5 models.

## Non-negotiable rules

- **Never fabricate or estimate a result.** Every number in any report comes from a file in `results/` produced by code
  in this repo. If something fails, say so.
- **Zero cost by default.** Free-tier APIs, local CPU/GPU, free Kaggle (2x T4) or Colab (T4). Anything that costs money
  needs Aarnav's explicit approval first.
- **Stop at every GATE** (E0 results, E5 pilot timing, each M pilot) and report with numbers before continuing.
- **Pilot before full runs.** Run every expensive experiment on a tiny slice first, measure wall time, extrapolate,
  report the estimate.
- **Verify, do not assume.** Check Hugging Face for current model names, dataset availability and licenses before use.
  Do not rely on model names from memory. Record every dataset and license in `DATA_CARD.md`.
- **Reproducibility.** Fixed seeds, a config file for every run, all API calls cached, all results written to disk with
  the config and git commit hash that produced them.
- **Pre-registered predictions.** Record each outcome against its prediction, including failures. Negative results go in
  the paper, not the bin.
- Prices in `configs/prices.yaml` are never filled from memory: cite official page + date, or leave a placeholder and ask.

## Reporting standards

- Every accuracy has a 95% bootstrap CI (10,000 resamples, item level). Report n for every number.
- Paired comparisons between forms: McNemar, Holm correction across comparisons.
- Training experiments: 3 seeds, mean ± sd, show individual seeds.
- Figure functions live in `src/shattered/plots/`, read only from `results/`, save PDF+PNG to `paper/figures/`.
  Colorblind-safe palette; never rely on color alone.
- After each experiment append to `RESULTS.md`: date, experiment id, config, commit hash, headline numbers, prediction,
  outcome (confirmed / refuted / inconclusive), surprises, next step.

## Working conventions

- Logic lives in `src/shattered/`; `scripts/eNN_*.py` are thin entry points; notebooks are thin.
- Long runs (Kaggle) must be resumable: checkpoint every N steps, skip finished items via the cache.
- Commit after each working milestone with a clear message. Never commit `.env`.
- When a result contradicts the thesis, say so plainly.

## Environment notes

- Local machine: Windows 11, RTX 3070 Laptop GPU (8 GB VRAM), Python 3.12 via `uv` venv at `.venv/`.
- Gemma 4 E2B fits 8 GB in bf16 only text-only with its per-layer embedding table (2.35B params) on CPU; E4B needs
  9.3 GB GPU-resident and does not fit.
- Never launch long jobs with `nohup ... &` from the Bash tool (they survive unexpectedly); use run_in_background.
- Exception (Aarnav, 2026-10-17): multi-day chains run detached from Claude Code as Windows scheduled tasks via
  `scripts/detach.ps1 -Name <x> -Script scripts/<chain>.sh` (tasks `ShatteredScripts_*`). Chains source
  `scripts/chainlib.sh` (heartbeat every 2 min, quota resets computed from the clock, never hard-coded dates);
  `scripts/chain_watch.sh` (also detached) marks any status older than 20 min DEAD.
- Shells: PowerShell is primary; Git Bash also available.

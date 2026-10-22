# DRAFT PRE-REGISTRATION — E-P2: word-aligned patching native → lossy, with readout-position patching (draft 2026-10-23; not registered, not run)

To be appended to RESULTS.md only after Aarnav approves it. Local 2B models only, bf16, one model load at a time.

**Question.** Lossy romanized Kannada is classified less accurately than native script. Is the lossy cost carried by
the word representations (word-final residuals), or by later processing at the readout position? Native and lossy have
different token counts, so positions are aligned by word. Lossy is a word-by-word transliteration: 200/200 sentiment
items have the same whitespace word count (checked 2026-10-23; SIB is checked in the pilot, and mismatching items are
excluded and counted).

**Models:** Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B (counted accuracy models). Qwen2.5 is not run.

**Items** (stored E0b/E0c scores, calibrated primary rule), per model × task:
- **Primary:** native correct and lossy wrong.
- **Control:** lossy correct and native wrong.
- **Counts available (primary / control):**

  | model | SIB | sentiment |
  |---|---|---|
  | Qwen3 | 398 / 31 | 69 / 16 |
  | Qwen3.5 | 345 / 43 | 27 / 16 |
  | Sarvam-1 | 126 / 65 | 16 / 4 |
  | Gemma 4 | 293 / 39 | 41 / 2 |

- SIB carries the predictions; sentiment is descriptive. At most 200 primary SIB items per model (random, seed 0) to
  bound time; all control items.

**Metric:** the gold margin M as in E-P1 (first-token logit difference at the final prompt position; full-verbalizer
fallback logged). Recovery R(L) = mean(M_patched − M_lossy) / mean(M_native − M_lossy), ratio of means, bootstrap 95%
CI over items.

**Two patching schemes per layer L = 0..N** (residual entering layer L):
- **Word-aligned:** for each text word k, the lossy run's residual at word k's last token is replaced with the native
  run's residual at native word k's last token.
- **Readout position:** only the final prompt position's residual is replaced with the native run's final-position
  residual. The template is identical in both runs, so the final position is the same token.

**Selection-safe peak:** a 50/50 item split (seed 0). L*_word = argmax R_word(L) on the selection half, evaluated on
the held-out half.

**Predictions (SIB, primary items):**
- **P2a (the lossy cost sits in word representations):** held-out R_word(L*_word) has a 95% CI lower bound > 0.5 in
  ≥ 3 of 4 models.
- **P2b (words first, readout later):** let L_read = the first layer at which R_read(L) ≥ 0.5 on all items. Then
  L*_word < L_read in ≥ 3 of 4 models.
- **Comparison reported (no threshold):** the full R_word(L) and R_read(L) curves, with CIs.

**Caveats stated now:**
- Native and lossy differ in both information (lossy is lossy) and familiarity; E-P2 locates where the difference
  matters, not which of the two causes it.
- Discordant-item selection inflates the denominator, as in E-P1.
- Gemma 4's per-layer embeddings make its residual patches partial.
- Native words have more pieces than lossy words in most tokenizers. Only the word-final position is patched; the other
  native pieces have no counterpart.

**Pilot (Qwen3.5-2B, 10 SIB items).** Checks, each stopping the run on failure:
1. Readout patch at the last layer (L = N) reproduces M_native (|Δ| < 0.05).
2. No patch reproduces M_lossy.
3. Word alignment: native and lossy word counts equal, and each patched pair decodes to word k in both (10/10).
4. Wall time per item × layer × scheme.

**Time estimate:** about 300 items per model (primary capped at 200, plus control) × 2 schemes × (N + 1) patched
forwards. Native prompts are longer (300–500 tokens), at about 60–100 ms each. That is about 20–35 min per model, about
2 h for four models. CPU analysis takes minutes.

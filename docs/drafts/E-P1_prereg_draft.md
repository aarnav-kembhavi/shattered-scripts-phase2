# DRAFT PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (draft 2026-10-23; not registered, not run)

To be appended to RESULTS.md only after Aarnav approves it. Local 2B models only, bf16, one model load at a time.

**Question.** NC-O showed that unfamiliar segmentations at the same token count cost accuracy (SIB: Qwen3.5, Sarvam-1,
Gemma 4). Is that cost carried by the word representations built at each word's last token? (a) and (c) decode to the
same lossy text and every word has the same number of pieces in both, so token positions align exactly and a
word-final residual can be moved from (a) into (c) one for one.

**Models:** the four counted accuracy models (Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B). Qwen2.5 is not run.

**Items** (from the stored NC1 scores, calibrated primary rule), per model × task:
- **Primary:** (a) correct and (c) wrong.
- **Control:** (c) correct and (a) wrong. Patching (a) into (c) should move these toward (a), that is, lower the gold
  margin.
- **Counts available (primary / control):**

  | model | SIB | sentiment |
  |---|---|---|
  | Qwen3 | 73 / 70 | 23 / 29 |
  | Qwen3.5 | 117 / 52 | 31 / 10 |
  | Sarvam-1 | 222 / 51 | 39 / 8 |
  | Gemma 4 | 133 / 59 | 18 / 7 |

- SIB carries the prediction. Sentiment (n < 40) is reported descriptively.

**Metric.**
- **Gold margin M:** at the final prompt position, the logit of the gold verbalizer's first token minus the largest
  logit among the other verbalizers' first tokens.
- **Pilot check:** first tokens must be distinct per tokenizer. Otherwise the full-verbalizer log-prob margin is used
  for that model, and this is logged.
- **Patch at layer L** (residual stream entering layer L; L = 0 is the embedding output; L = 0..N): replace the
  residual at every text word's last-token position in the (c) run with the (a) run's residual at the same position.
  The template stays canonical in both runs.
- **Recovery** R(L) = mean(M_patched − M_c) / mean(M_a − M_c) over items (ratio of means), with a bootstrap 95% CI
  (10,000 over items).

**Selection-safe peak.** Items are split 50/50 (seed 0). L* = argmax R(L) on the selection half. R(L*) and its CI are
reported on the held-out half. The full curve R(L) is also reported on all items.

**Predictions (SIB, primary items):**
- **P1a (word-final states carry the cost):** held-out R(L*) has a 95% CI lower bound > 0.5 in ≥ 3 of 4 models.
- **P1b (it is an assembly-stage cost):** L* lies in the first two-thirds of the layers (L* ≤ ⌊2N/3⌋) in ≥ 3 of 4 models.
- **Control (no prediction, reported):** on control items, R(L*) has the same sign. Patching (a) into (c) moves the
  margin toward (a)'s.

**Caveats stated now:**
- Selecting discordant items inflates M_a − M_c through regression to the mean. The ratio of means and the held-out L*
  limit, but do not remove, this.
- Gemma 4 injects per-layer token embeddings at every layer, so a residual patch does not remove (c)'s token identity
  from later layers. Gemma's recovery is a lower bound and is reported as such.
- Non-final pieces of each word stay as in (c), so later layers can still attend to them.

**Pilot (Qwen3.5-2B, 10 SIB items).** Checks, each stopping the run on failure:
1. Patching every position at L = 0 reproduces M_a (|Δ| < 0.05).
2. Patching nothing reproduces M_c (|Δ| < 0.05).
3. Patched-position indices map to the same decoded word in (a) and (c) (10/10).
4. Wall time per item × layer, extrapolated.

**Time estimate** (from the NC1 scoring logs; the pilot replaces it): 1 forward with caching per item, plus N + 1
patched forwards (N = 24–35 layers) per item at about 40–80 ms. That is about 5–25 min per model for primary plus
control items, and about 1 h for all four models. CPU analysis takes minutes.

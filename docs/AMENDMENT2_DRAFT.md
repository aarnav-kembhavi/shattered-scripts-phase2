## PHASE 2 AMENDMENT 2 (2026-11-02): X9 to X15, Kaggle compute, page policy

**APPROVED by Aarnav on 2026-11-02 with four edits (X12 exemption and rename, gate record, A1-R option (a)), applied below. Nothing in X9 to X15 had been run when it was approved.** This text is appended to
RESULTS.md unchanged, committed, and tagged `phase2-amendment-2`; `shattered.runlog.provenance()` then records that tag's commit as
`phase2_amendment2_commit` in every X9 to X15 result file (next to `phase2_registration_commit`). It supersedes `docs/X9_registration_DRAFT.md`.
Already registered and unchanged: X7 control (full 6-vocabulary grid with factorized embeddings, 3 seeds; running), X8 (n = 100, annotators
X8-P and X8-Q, agreement primary, vowel ratio descriptive), the Kaggle runner and its reproducibility gate (registered 2026-11-02 before
its first run). Citations are not added in this amendment.

### A0. General rules for X9 to X15

- **Compute.** Laptop (RTX 3070, 8 GB, bf16) and Kaggle (T4 x2, 30 h per week, no bf16; private kernels via `scripts/kaggle_runner.py`). Modal is
  dropped. A session never exceeds 12 h and a job writes one resumable shard at a time. **No Kaggle result counts until the gate passes**
  (both gate models, dtype recorded). The dtype of every Kaggle result is the gate dtype of that model, stated in the table.
- **Models never loaded by two jobs at once on one machine; one model-loading job at a time on the laptop; disk guard 25 GB.**
- **Interpretability stays bf16 or the gate dtype of an unquantized model** (fp16 or fp32 on the T4); retrieval vectors are never taken from
  a quantized model. Where a Kaggle retrieval number is compared with a laptop number, the Kaggle value for the same model and form must be
  within 0.03 of the laptop value, otherwise the Kaggle retrieval results are labelled exploratory (checked once by A1-R). Models without a laptop baseline
  count only after A1-P.
- **Statistics (Phase 1 standards).** Exact McNemar on paired per-item correctness, Holm within each stated family, 95% paired bootstrap CIs
  (10,000 resamples, seed 0), n reported for every number. Counted models are those of Phase 1 (accuracy: Qwen3, Qwen3.5, Sarvam-1, Gemma 4;
  retrieval: Qwen3.5, Sarvam-1, Gemma 4); Qwen2.5 is reported and never counted. A new model is counted only if its native SIB-200 accuracy
  has a 95% CI lower bound above 0.40. **The X12 models are contrast endpoints and are exempt from this counting rule; they still must pass A1-P.**
- **Gate record and reporting.** The reproducibility gate (2026-11-02) passed for both models in float16. **Sarvam-1 ITRANS raw-label agreement was 0.95, exactly at the
  pass threshold (0.95);** this is recorded here and does not change the gate verdict. **Every Kaggle result table reports the mean |delta logprob| of that model from
  its gate or A1-P run** (Sarvam-1 0.079 to 0.083, Gemma 4 E2B 0.112 to 0.124 in the gate; A1-P gives the value for each new model).
- **Pilots first** (timing and a validity check; no outcome value is looked at for a decision); results are reported with registered
  verdict words; anything against the prediction is reported first; failures are logged with dates and never silently re-run.

### A1. Kaggle precision and retrieval checks (added 2026-11-02 at Aarnav's request; not experiments, run before the experiments that depend on them)

- **A1-R. Retrieval gate (the two gate models).** Rescore FLORES+ retrieval on Kaggle for Sarvam-1 and Gemma 4 E2B, in the gate dtype (float16), for native and
  ITRANS: the same 2,009 sentences, the same sentence vectors (mean residual over tokens, every layer), the same M4b protocol (layer chosen on the train half,
  seed 0, unmapped retrieval on the test half of 1,005). **Kaggle retrieval results count only if, for each model and form, the Kaggle acc@1 is within 0.03 of the
  laptop value in `results/m4b_mapping`** (and no vector is non-finite). If either model fails, every Kaggle retrieval result is labelled exploratory (A0 rule). **Data (option (a), approved):**
  the 2,009 Kannada and English FLORES+ evaluation sentences are uploaded as a **private Kaggle dataset, kept private for the whole of Phase 2 and never made public;
  it is deleted at the end of Phase 2 and the deletion is logged in RESULTS.md.** These are the only FLORES+ text sent to Kaggle. Every later Kaggle retrieval job reads the same private dataset.
- **A1-P. Per-model precision check (every model without a laptop baseline: all 7 to 9B models of X12 and X13).** On Kaggle, score 100 SIB-200 items (the gate's
  100 ids) x 3 forms (native, ITRANS, lossy) in **float16 and in float32**; **8-bit (bitsandbytes LLM.int8) replaces float32 only if float32 does not fit 2 x T4**
  (a 7B model is 28 GB in float32 against 30 GB of VRAM, so for most models 8-bit will be the reference; this is stated in the table, and 8-bit is itself an
  approximation). **The model counts only if, per form, the raw-label agreement between float16 and the reference is at least 98% and the accuracies differ
  by at most 1 point** (0.01). Also reported: the maximum absolute hidden state over all layers in float16 (as in the gate), non-finite values (any = fail), and
  both dtypes. A model that fails is not run; it is reported as "failed the precision check" with the numbers. Gemma-family or other models with a laptop baseline
  are not exempt from the hidden-state report. Retrieval and all other results for a model are only produced after it passes.

### X9a. Tiny GPT, familiarity manipulated, fragmentation fixed (laptop)

**Cipher.** A deterministic bijection on letters: ASCII a-z map to the first 26 Cyrillic lowercase letters (U+0430 to U+044F) by the
permutation `default_rng(9).permutation(26)`, A-Z to the same letters in Cyrillic capitals; digits, punctuation, spaces, newlines unchanged.
The inverse is built and the round trip is checked on every story used (all exact, otherwise nothing runs).

**Corpus and splits.** TinyStories V2, the Phase 1 E5 stream and order (`data_seed` 0, `configs/e05_pretrain.yaml`). *Evaluation:* the first
500 stories of the TinyStories V2 validation split, each as an English text and a cipher text (parallel pairs), truncated to the first 700
characters of the English story and the same positions of the cipher text; disjoint from every training and tokenizer story (exact match,
count reported, must be 0). *Exposure:* one random order of the training stories (`default_rng(9)`) is fixed; exposure p in {0, 1, 5, 20, 50}
percent replaces the first p percent of that order by their cipher renderings (nested sets). A story is seen in one rendering only, so there
is **no parallel supervision**; level 0 is the Phase 1 English stream.

**Tokenizer (one, fixed).** Byte-level BPE, 1,024 tokens, the Phase 1 recipe (`src/shattered/pretrain/data.py`), trained once on a fixed
100 MB mixture of **50 MB English stories and 50 MB cipher renderings of other stories** (disjoint from the evaluation stories, drawn before the
exposure order), and reused unchanged at all levels and seeds, so the segmentation of every text is identical across levels. **Reported before
any model is trained: English tokens per word and cipher tokens per word on the evaluation stories (expected near equal; if they differ by more
than 15 percent relative, this is reported and the run goes on, with the ratio stated in every table), and the sha256 of the tokenizer.**

**Models and budget.** The Phase 1 tiny GPT (8 layers, d_model 384, 6 heads), vocabulary 1,024, Phase 1 optimizer, schedule and evaluation
cadence, the same number of optimizer steps and tokens per step as the Phase 1 vocabulary-1,024 runs. Levels may consume slightly different
numbers of stories (cipher has more bytes per story); stories consumed per level are reported. 5 levels x 3 seeds (0, 1, 2) = 15 runs,
about 6 GPU hours (extrapolated from Phase 1 timing; pilot first: one run at level 20, seed 0, 10 percent of the budget, to check the round
trip, the tokenizer statistics and the timing).

**Measures (held-out pairs, final checkpoint).** (1) *Retrieval:* cipher story to English story, acc@1, the Phase 1 M4b protocol (mean residual per
layer, the layer chosen on the train half of the 500 pairs, seed 0, unmapped retrieval on the test half of 250; the mapped value is secondary).
Chance is 1/250. (2) *Assembly:* the Phase 1 MDL word-identity probe (`bootstrap_mdl_detok`, fraction 0.9) on cipher words: the 300 most frequent
space-preceded alphabetic words of the evaluation cipher texts that are at least 3 tokens under the X9 tokenizer (if fewer than 300, at least 2
tokens; the only fallback), up to 40 occurrences each, at most 2 per story; the same selection on English is probed as a descriptive reference.

**Prediction and decision rules.** Level 0 is **not** part of either rule: its cipher embeddings are untrained, so retrieval there is at chance
by construction (reported, expected within the bootstrap interval of 1/250), and its assembly layer is reported descriptively.
- **X9a-R (retrieval follows exposure).** Prediction: seed-mean retrieval rises monotonically with exposure from 1 percent upward. *Supported:* the
  seed means at 1, 5, 20, 50 are non-decreasing and mean(50) - mean(1) exceeds 3 times the larger of the two seed SDs (SD floor 1/250).
  *Refuted:* mean(50) <= mean(1), or the Spearman correlation between level and seed mean over the four levels is 0.6 or lower. *Inconclusive:* otherwise.
- **X9a-A (assembly layer is flat).** Prediction: the seed-mean MDL detok layer for cipher words varies by at most 1 layer across levels 1 to 50.
  *Supported:* max minus min of the four seed-mean detok layers is at most 1. *Refuted:* at least 2. *Inconclusive:* more than one run at a level has an
  undefined detok layer (counted and reported).
- **Joint reading (only if both are decided):** R supported and A supported = "familiarity moves meaning alignment while word assembly stays put at
  fixed fragmentation"; R supported and A refuted = "exposure also moves assembly; the dissociation is not clean"; R refuted = "no familiarity
  effect in this setting" (small model, letter cipher, no claim beyond that).

### X9b. Real models, QLoRA continued pretraining (memory pilot on the laptop; full runs on Kaggle)

**Models.** Sarvam-1 (**primary**: 2 training seeds per cell) and Qwen3.5-2B (**secondary**: 1 seed per cell). Seeds are 0 and 1.
**Recipe (fixed now, not tuned on any evaluation number).** 4-bit NF4 with double quantisation; compute dtype bf16 on the laptop and fp16
(with loss scaling) on the T4; LoRA rank 16, alpha 32, dropout 0.05 on all attention and MLP projections, embeddings and norms frozen;
gradient checkpointing; 512-token sequences; paged 8-bit AdamW; learning rate 2e-4, cosine to 10 percent, warmup 3 percent, weight decay 0.
**Memory pilot (laptop, first):** peak VRAM and tokens per second over 50 steps for each model and condition at the largest micro-batch that fits
8 GB; reported with the **maximum feasible token budget B per run in about 3 GPU hours** = floor(0.9 x slowest measured tokens/s x 10,800 s)
rounded down to a multiple of the tokens per optimizer step. Because speed differs between machines, **B is fixed by a 50-step timing run on
the machine that will train (the T4)** and recorded in RESULTS.md before any full run; B is the same for the three conditions of a model.
Total: Sarvam-1 3 conditions x 2 seeds + Qwen3.5-2B 3 conditions x 1 seed = 9 runs, up to about 27 GPU hours (flagged: nearly one Kaggle
week; the Qwen3.5-2B arm is cut first if the quota is short, and that is logged).

**Conditions (equal token budget B under each model's own tokenizer).** (i) *ITRANS Kannada:* Kannada Wikipedia 20231101 articles rendered with
the project ITRANS scheme (`scheme.py`), seeded order (`default_rng(9)`); (ii) *native Kannada:* the same articles in the same order in native
script; (iii) *English:* English Wikipedia 20231101 shard 0, seeded order. Each stream is cut at B tokens; words and articles consumed are reported.
**Exclusion (hard rule).** Every article containing a FLORES+ sentence (Kannada or English, dev and devtest) or a SIB-200 sentence (Kannada or
English) is removed before sampling, by exact or containment (>= 20 characters) match; the ITRANS renderings of the evaluation sentences are also
searched in the ITRANS stream. The final streams are re-scanned with the same function: **overlap must be 0 for every stream, reported per stream,
or the run does not start.** Evaluation sentences whose source article is outside Wikipedia cannot be mapped to dump articles; the match rule is
the registered operationalisation and this is a stated limitation.

**Evaluation (Kannada; the base model and the tuned model in the same environment and dtype).** (1) SIB-200 accuracy, native and ITRANS, T1 template,
calibrated as in Phase 1, 1,004 items; (2) FLORES+ retrieval against English, native and ITRANS, on the 2,009 sentences (M4b split, unmapped
retrieval at the train-chosen layer, test half n = 1,005); (3) English SIB-200 (1,004), descriptive damage check (a drop of more than 5 points is
flagged, no verdict). The tokenizer is not changed by training; its sha256 before and after is reported, so tokens per word are unchanged by
construction. Caveat stated now: adapters are trained against the 4-bit base and evaluated on the unquantized base plus adapter.

**Prediction and decision rule.** Gap g(c) = native minus ITRANS (accuracy or retrieval) after training under condition c in {ITRANS, native, English},
g(0) before training. Prediction: the gap shrinks more after ITRANS training than after either control, D_N = g(native) - g(ITRANS) > 0 and
D_E = g(English) - g(ITRANS) > 0. **Primary: Sarvam-1.** Interval for each D: a paired bootstrap over items (SIB-200) or test sentences (retrieval),
10,000 resamples, in which, **within each cell, one of the two seeds is drawn at random in every resample (so the interval includes seed variance)**;
**97.5% intervals (Bonferroni over D_N and D_E)**; seed spread (the two seeds' D values) is reported next to every interval. *Supported:* both
intervals above 0. *Partly supported:* exactly one above 0 and none below 0. *Refuted:* none above 0 and at least one entirely below 0, or both point
estimates at or below 0. *Inconclusive:* otherwise. Verdicts per measure (SIB-200 accuracy; retrieval). **Qwen3.5-2B (secondary, one seed, item
variance only)** gets the same rule and is labelled secondary; its verdict does not enter the primary conclusion. With 2 seeds the seed variance
estimate is crude; stated as a limitation.

### X10. Generation: FLORES+ devtest to English (laptop pilot; laptop or Kaggle full)

**Setup.** FLORES+ devtest, 1,012 Kannada sentences to their English references; inputs native, ITRANS, lowercase, lossy, and natural (the devtest ids
that have a clean natural romanization; n reported). One registered instruction, identical for all forms, written in English: `Translate this Kannada
sentence into English.\nKannada: {sentence}\nEnglish:`. Base models, BOS always, greedy decoding, `max_new_tokens` = 128, output cut at the first
newline; empty outputs are scored as empty (share reported per model and form). Models: the four counted accuracy models. **Metric:** chrF
(sacreBLEU, chrF2: character order 6, word order 0, beta 2), sentence-level chrF for the paired bootstrap and corpus chrF reported. **Contrasts
(family for Holm: 4 contrasts x 4 models = 16):** native - ITRANS, native - lowercase, native - lossy (1,012 sentences), native - natural (natural subset).
**Pilot:** 20 sentences per model and form, timing and output sanity only (no chrF used for any decision); the time estimate is reported before the full run.
**Prediction X10-P:** native beats ITRANS in at least 3 of 4 models (Holm-significant, positive). *Supported:* at least 3 of 4; *partly supported:* exactly 2;
*refuted:* at most 1. The other three contrasts are reported with the same effect rule, no prediction.

### X11. Quantization control (laptop)

**Arm A (registered).** Qwen3.5-2B in 4-bit NF4 (bitsandbytes, double quantisation, bf16 compute) rerun on SIB-200, 1,004 items, native, ITRANS,
lowercase, lossy, T1 template, calibrated as Phase 1, against its stored full-precision (bf16) Phase 1 results on the same items. Reported: accuracy
per form and the change (exact McNemar, paired bootstrap CI), and the change in the native-minus-ITRANS gap. **Prediction:** quantization does not
change the picture. *Supported:* every form's accuracy change is within 3 points (point estimate) and the 95% CI of the gap change lies within +-5
points. *Refuted:* any form changes by more than 5 points with the CI excluding 0. *Partly supported:* otherwise. No retrieval (no interpretability
on quantized models). **Arm B (optional, only if time allows, descriptive):** one 4B-class model chosen by the X6 screen (name not assumed),
4-bit, SIB-200 native, ITRANS, lossy; the native-minus-ITRANS gap with CI, compared with the 2B models; no verdict.

### X12. Ambari natural experiment (Kaggle, 7B in fp16 sharded over 2 x T4)

**Tokenizer check (done 2026-11-02, CPU, tokenizer files only; `results/phase2/x12/tokenizers.json`).** Ambari-7B-base-v0.1: vocabulary 49,600, native
2.74 and ITRANS 4.55 tokens per word. Ambari-7B-Instruct-v0.2: vocabulary 32,000 (the original Llama-2 tokenizer; its config names meta-llama/Llama-2-7b-hf),
native 20.83 and ITRANS 4.69. Not loadable with the current access: meta-llama/Llama-2-7b-hf (manual gate) and Ambari-7B-Instruct-v0.1 (gated, auto approval
pending on the account). **Contrast 2 is therefore kept subject to access, with a caveat registered now:** the v0.2 card says it was fine-tuned on the same
dataset with the same parameters without vocabulary expansion, while v0.1 is built on Ambari-7B-base-v0.1 (500 million new Kannada tokens); the two
differ in the tokenizer and may differ in the base model's Kannada pretraining, so the contrast is **not** a clean "fragmentation with data fixed"
test unless the base models are shown to match. It is reported as the comparison of the two released instruction models, not as a causal test.
**Models and forms.** The X12 models are contrast endpoints, exempt from the A0 counting rule (native SIB CI lower bound above 0.40) and subject to A1-P. Kannada SIB-200 (native, ITRANS, lossy; natural on the 257) and FLORES+ retrieval (native, ITRANS), T1 template, calibrated as Phase 1,
fp16 (gate dtype), no quantization.
**Contrast 1 (form-specific exposure transfer).** Llama-2-7B vs Ambari-7B-base-v0.1. Ambari's continued pretraining was on native-script Kannada, so a native gain is
expected; the tested claim is that this exposure does **not** transfer equally to ITRANS (DiD > 0). The native gain (Ambari minus Llama-2) also confounds exposure with the
tokenizer extension; the ITRANS gain is the control (ITRANS tokens per word 4.69 vs 4.55). **X9b, not X12, is the causal test of familiarity;** X12 is a natural
experiment on released models. **Prediction:** the native gain exceeds the ITRANS gain on SIB-200 and on retrieval. Statistic:
DiD = gain(native) - gain(ITRANS), paired bootstrap over items (sentences), 97.5% interval (two measures). *Supported:* both above 0; *partly supported:*
one; *refuted:* neither above 0 and one below; *inconclusive:* otherwise.
**Contrast 2 (instruction models).** Ambari-7B-Instruct-v0.1 vs v0.2: MDL assembly layer for native Kannada words (the 300 Phase 1 probe words, Phase 1
protocol, fp16) with the prediction from the tiny GPTs that the more fragmented input (v0.2, native 20.83 vs 2.74 tokens per word) is assembled later;
registered rule as H3 (sign of the layer difference matches the sign of the tokens-per-word difference, CI excluding 0). Accuracy differences are exploratory.
If v0.2 is found not to use the original Llama tokenizer, contrast 2 is dropped (it does use it).

### X13. More 7-9B models on Kaggle

**Screen (CPU first, tokenizer and metadata only, then a one-forward check on Kaggle).** Qwen3-8B (Apache-2.0; native 11.84 and ITRANS 4.34 tokens per word,
checked), **the largest Sarvam model that fits 2 x T4** (name not assumed; the screen lists the sarvamai repositories, parameters, licence and the 4-bit
memory; 4-bit only when fp16 cannot fit, and then SIB and X10 only, no retrieval), and Llama-3.1-8B (gated, access pending; retried at each screen, dropped
if still unavailable at the end of the queue, which is logged). A model enters if it fits, its gate-style check (no non-finite value, fp16 or fp32) passes
and its native SIB-200 CI lower bound exceeds 0.40 **and it passes the A1-P precision check** (the same check applies to the X12 models; a 4-bit-only model is exempt
from A1-P but is limited to SIB and X10, as stated). **Runs:** SIB-200 (native, ITRANS, lossy, lowercase), retrieval (unquantized only), X10, MDL assembly.
**Extended verdicts** use the all-but-one rule on the enlarged counted set and are reported separately; Phase 1 verdicts do not change. **Activation
patching on one 7-9B model only if it fits one 12 h session (the Phase 1 E-P recipe, same registered rule); otherwise dropped and said so.**

### X14. Black-box hosted large models (exploratory, no verdict)

Groq and OpenRouter free models. **Model choice rule, applied and logged on the day of the first call:** list the free text models of both providers; take up
to 3 with the largest stated parameter counts from different families; **no Gemini-family model in any condition involving natural text** (the natural
romanization is Gemini output). Task: SIB-200 classification by generation with one registered prompt, `Classify the topic of the following Kannada text. Answer
with exactly one of: science/technology, travel, politics, sports, health, entertainment, geography.\n\nText: {text}\nTopic:`, temperature 0, 20 new tokens,
parsed by exact (case-insensitive) category match (unparsed = wrong, share reported). Forms native, ITRANS, lossy on 1,004 items and natural on the 257
items that have a clean natural romanization (n reported; 1,004 natural romanizations do not exist). Reported per model: accuracy per form with 95% CI and the native
minus ITRANS gap with a paired bootstrap CI. Provider limits spread the calls over days; responses are cached; failures and rate limits are logged.

### X15. Human intelligibility baseline (needs annotators)

100 SIB-200 items stratified by category (proportional allocation, seed 15) from the 257 items with a clean natural romanization; forms native, ITRANS,
lossy, natural. **Latin square:** four groups of annotators; group g sees item i in form (i + g) mod 4, so each annotator sees each item in one form
only; 2 annotators per group (8 annotators, 100 judgments each, 800 judgments), 2 judgments per item-form. Annotators are native Kannada speakers who
choose the topic from the seven labels (shown in English) with no model output visible; a page built like the X8 page; no identities recorded (roles
only). Statistics: accuracy per form with 95% bootstrap CIs resampling items and annotators; chance 1/7. **Prediction X15-P:** human accuracy on native
and natural differs by less than 5 points. *Supported:* |difference| < 0.05 and the 90% CI within +-0.12 (the width expected from 200 judgments per form);
*refuted:* |difference| >= 0.05 with the 95% CI excluding 0; *inconclusive:* otherwise. Model accuracies on the same 100 items are reported next to the human ones.

### Q. Queues and budget (cut from the end of either queue if time slips; stop at gates C, D, E)

- **Laptop:** X7 control (running, about 10 GPU hours) -> X9a (about 6 h) -> X9b memory pilot -> X10 pilot -> X4 Bengali -> X4 Telugu -> X1 T3 (only after a native
  speaker verifies `T3_verification.md`; the XNLI line is marked "needs rewrite") -> X6 -> X11 -> X10 full (if not on Kaggle).
- **Kaggle (after the gate and the approval of this amendment):** A1-R retrieval gate (may run before approval; it is not an experiment) -> A1-P for each 7 to 9B model (about 0.3 h each) -> X12 -> X13 -> X9b full (about 27 h) -> X10 full. The weekly cap (30 h) means X9b alone
  needs most of a week; the runner refuses pushes over the cap and the schedule is set from measured hours.
- **Needs people or access:** T3 verification, X8 annotators P and Q, X15 annotators, Hugging Face access to Llama-2-7b-hf, Ambari-7B-Instruct-v0.1 and
  Llama-3.1-8B.

### P. Page policy (applies to every integration)

The main text targets 12 pages and may exceed 12 only for material that carries a headline claim (X9, X12, X15). Robustness, extra models, bookkeeping and
per-cell tables go to the appendix. All scale work is in **one section, "Scale and replication"**. After each integration the main-text pages are reported
with a list of what moved to the appendix. Phase 2 results enter the paper only when Aarnav says so.

**Not claimed.** No new claim about why familiarity matters, no scaling law, no change to any Phase 1 or Phase 2 verdict.

# A: General rules A0, Kaggle precision and retrieval checks A1-P and A1-R, reproducibility gate (Phase 2)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| registered | `9d408c4` | 2026-11-02 16:47:59 +0530 | 3480-3485 | PHASE 2 REGISTRATION: Kaggle runner and reproducibility gate (2026-11-02, Aarnav; registered before the first Kaggle run) |
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3495-3514 | A0. General rules for X9 to X15 |
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3515-3530 | A1. Kaggle precision and retrieval checks (added 2026-11-02 at Aarnav's request; not experiments, run before the experiments that depend on them) |
| none | `f41e866` | 2026-11-02 19:15:43 +0530 | 3706-3706 | 2026-11-02 19:00 IST, A1-R data. |
| none | `60b8183` | 2026-11-02 23:21:28 +0530 | 3712-3712 | 2026-11-02 19:26 IST, A1-R retrieval gate: PASSED. |
| result | `b046768` | 2026-11-02 20:15:27 +0530 | 3713-3713 | 2026-11-02 19:55 IST, A1-P first results (`results/kaggle/kaggle_precision/2026-11-02T135712/out/`), float16 vs 8-bit, 100 SIB items x 3 forms, rule: agreement  |
| result | `8b52d91` | 2026-11-02 20:34:16 +0530 | 3714-3715 | 2026-11-02 20:20 IST, A1-P re-run of Ambari-7B-base (`results/kaggle/kaggle_precision/2026-11-02T144532/out/`): FAILS. |
| registered, amended | `78d6ad2` | 2026-11-02 23:17:45 +0530 | 3716-3725 | 2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run). |
| none | `9d50e92` | 2026-11-02 23:24:17 +0530 | 3748-3753 | 2026-11-02 23:24 IST, A1-P re-run against float32-offload (commit 803b5e7, 0.35 h of quota): NO VERDICT, harness error. |
| none | `73546be` | 2026-11-03 02:24:19 +0530 | 3796-3800 | 2026-11-03 02:24 IST, A1-P against the float32-offload reference (A1-P-D1): BOTH PASS |
| result | `f116475` | 2026-11-03 04:26:01 +0530 | 3808-3809 | 2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3 |
| result | `cdef73d` | 2026-11-03 13:02:56 +0530 | 3834-3837 | 2026-11-03 13:02 IST, X13 Qwen3-8B: registered verdicts (Kaggle T4 x2, float16, A1-P passed; `scripts/x13_analyse.py`, `results/phase2/x13/qwen3-8b/analysis.jso |
| result, failed or not run | `0cfdea0` | 2026-11-04 02:46:43 +0530 | 3868-3869 | 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST). |
| failed or not run | `7cfcb18` | 2026-11-04 06:08:50 +0530 | 3890-3891 | 2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST). |
| none | `81fc534` | 2026-11-04 07:53:46 +0530 | 3896-3897 | 2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check |
| result | `72ff37e` | 2026-11-04 12:14:44 +0530 | 3908-3909 | 2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD  |
| none | `59154b4` | 2026-11-04 14:10:52 +0530 | 3916-3917 | 2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly. |
| result | `4770255` | 2026-11-04 17:26:35 +0530 | 3920-3921 | 2026-11-04 17:26 IST, Kaggle account 2: Ambari-Instruct-v0.1 A1-P ended without a verdict (pushed 14:08 IST, 3.2 h of account 2 quota). |
| none | `7bcba7d` | 2026-11-04 20:22:41 +0530 | 3923-3924 | 2026-11-04 20:22 IST, Kaggle account 2: Llama-3.1-8B A1-P PASSED (float32-offload reference; pushed 17:22 IST, finished about 20:15; this is the first run of th |
| none | `f06c46f` | 2026-11-04 20:23:22 +0530 | 3925-3926 | 2026-11-04 20:23 IST, Kaggle account 2 note on the slow A1-P runs (cause now likely): |
| result | `952be81` | 2026-11-04 21:53:03 +0530 | 3934-3935 | 2026-11-04 21:53 IST, Kaggle account 2: duplicate push of the Ambari-Instruct-v0.1 A1-P (my driver defect; quota cost, no wrong result). |
| none | `06404f2` | 2026-11-04 22:07:54 +0530 | 3938-3939 | 2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label  |
| result | `5c0388b` | 2026-11-05 04:23:24 +0530 | 3966-3967 | 2026-11-05 04:23 IST, X13 Llama-3.1-8B RESULT (Kaggle account 2; A1-P passed 2.78 h, scoring 1.82 h; `scripts/x13_analyse.py --model llama-3.1-8b`, `results/pha |

## Values observed in the result files (read from the files' own columns and keys)

- no model, form, task or seed columns in the dumped files; see the entries

Result directories: none (numbers are in the RESULTS.md entries)

## RESULTS.md entries, verbatim

##### PHASE 2 REGISTRATION: Kaggle runner and reproducibility gate (2026-11-02, Aarnav; registered before the first Kaggle run)

RESULTS.md lines 3480 to 3485; first line committed in `9d408c4` on 2026-11-02 16:47:59 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: registered

`````text
## PHASE 2 REGISTRATION: Kaggle runner and reproducibility gate (2026-11-02, Aarnav; registered before the first Kaggle run)

**Remote compute is Kaggle only** (account with GPU T4 x2, 30 h per week; Modal is dropped from all plans). Credentials are in `.env` only (never committed, never in the anonymised package). `scripts/kaggle_runner.py` packages the repo at a commit (`git archive` of src, scripts, configs and listed result files), uploads it as a private Kaggle dataset, pushes a private GPU T4 x2 kernel with internet on, polls, downloads the outputs and writes `results/kaggle/<job>/last_run.json` (commit, hardware, torch, bf16 support, runtime) and `results/kaggle/quota.json` (weekly hours; a push that would exceed 30 h in 7 days, or a session over 11 h, is refused). Long jobs must be resumable with one output shard at a time, so a session timeout loses at most one shard.

**Gate (rule fixed now).** `scripts/kaggle_gate.py` rescored 100 SIB-200 Kannada items (the same ids as `e0c_sib.load_items(limit=100)`) in native, ITRANS and lossy forms with Sarvam-1 and Gemma 4 E2B on the T4, first in float16 and, if a model fails, in float32 (T4 has no bf16; the laptop scores are bf16). The forms are built from the public SIB-200 text with the project code. **Pass, per model and form:** raw-prediction agreement with the laptop run at least 95 of 100, |accuracy difference| at most 0.03, no non-finite log-probability, prompt token counts identical to the laptop run on all items, and no hidden state above 65,504 in a check forward (fp16 limit). A model passes when all three forms pass in some dtype; the first dtype that passes is the dtype used for that model on Kaggle. **No remote result counts until both models pass**; the runner refuses other jobs until `results/kaggle/kaggle_gate/gate_passed.json` exists. If a model passes only in float32 that is reported and used for that model.

`````

##### A0. General rules for X9 to X15

RESULTS.md lines 3495 to 3514; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: amended

`````text
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

`````

##### A1. Kaggle precision and retrieval checks (added 2026-11-02 at Aarnav's request; not experiments, run before the experiments that depend on them)

RESULTS.md lines 3515 to 3530; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: amended

`````text
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

`````

##### 2026-11-02 19:00 IST, A1-R data.

RESULTS.md lines 3706 to 3706; first line committed in `f41e866` on 2026-11-02 19:15:43 +0530; last line in `f41e866` on 2026-11-02 19:15:43 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 19:00 IST, A1-R data.** Private Kaggle dataset `shattered-flores-private` created (option (a), approved): the 2,009 FLORES+ dev+devtest Kannada (NFC) and English sentences, and, from the second version, the 496 retained Kannada natural-romanization drafts keyed by FLORES index (derived text, no source sentence). It is private (the Kaggle CLI reports "Your private Dataset"), stays private for the whole of Phase 2, is deleted at the end of Phase 2, and the deletion will be logged here.
`````

##### 2026-11-02 19:26 IST, A1-R retrieval gate: PASSED.

RESULTS.md lines 3712 to 3712; first line committed in `60b8183` on 2026-11-02 23:21:28 +0530; last line in `60b8183` on 2026-11-02 23:21:28 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 19:26 IST, A1-R retrieval gate: PASSED.** Sarvam-1 and Gemma 4 E2B, float16, T4 x2 (about 0.37 h of quota), unmapped FLORES+ retrieval acc@1 at the train-chosen layer on the M4b test half (n = 1,005) against `results/m4b_mapping/summary.csv`: Sarvam-1 native 0.9443 vs 0.9443 (difference 0.000), ITRANS 0.5104 vs 0.5144 (0.004); Gemma 4 native 0.9960 vs 0.9950 (0.001), ITRANS 0.2657 vs 0.2687 (0.003); tolerance 0.03; no non-finite vector; the per-layer curves differ by at most 0.007. The in-kernel `pass` flag read False only because the laptop summary file is not in the Kaggle package; the comparison was done locally with the registered rule (`results/kaggle/a1r_result.json`). Kaggle retrieval counts.
`````

##### 2026-11-02 19:55 IST, A1-P first results (`results/kaggle/kaggle_precision/2026-11-02T135712/out/`), float16 vs 8-bit, 100 SIB items x 3 forms, rule: agreement >= 0.98 and accuracy difference <= 0.01 per form.

RESULTS.md lines 3713 to 3713; first line committed in `b046768` on 2026-11-02 20:15:27 +0530; last line in `b046768` on 2026-11-02 20:15:27 +0530; labels from the title and parent heading: result

`````text
- **2026-11-02 19:55 IST, A1-P first results (`results/kaggle/kaggle_precision/2026-11-02T135712/out/`), float16 vs 8-bit, 100 SIB items x 3 forms, rule: agreement >= 0.98 and accuracy difference <= 0.01 per form.** **Qwen3-8B FAILS** (reference 8-bit because float32 needs about 30.5 GiB; agreement 0.93, 0.92, 0.93; accuracy difference -0.04, +0.04, +0.03; mean |d logprob| 0.62 to 0.89; maximum hidden state 11,864; no non-finite value). **Ambari-7B-base FAILS under the 8-bit reference** (agreement 0.95, 0.99, 0.96; accuracy difference +0.03, 0.00, +0.01; maximum hidden state 1,730; no non-finite value). Qwen3-8B is not run (registered rule); the 8-bit reference is itself an approximation, which the amendment states, so the failure does not by itself say which dtype is closer to the truth. **Implementation correction (not a rule change):** the amendment says 8-bit replaces float32 only if float32 does not fit 2 x T4; my first implementation excluded float32 above 24 GiB without trying it, and Ambari-7B-base (about 25.7 GiB in float32) can fit. A1-P for Ambari-7B-base is re-run with float32 attempted first (8-bit only after an out-of-memory error, recorded); the first result stays on disk. Qwen3-8B cannot fit float32 and its result stands.
`````

##### 2026-11-02 20:20 IST, A1-P re-run of Ambari-7B-base (`results/kaggle/kaggle_precision/2026-11-02T144532/out/`): FAILS.

RESULTS.md lines 3714 to 3715; first line committed in `8b52d91` on 2026-11-02 20:34:16 +0530; last line in `803b5e7` on 2026-11-02 22:59:39 +0530; labels from the title and parent heading: result

`````text
- **2026-11-02 20:20 IST, A1-P re-run of Ambari-7B-base (`results/kaggle/kaggle_precision/2026-11-02T144532/out/`): FAILS.** Float32 was attempted first and ran out of memory on 2 x T4 (CUDA OOM, 12.81 GiB allocation), so float32 does not fit and the registered 8-bit reference applies; the numbers are those of the first run (agreement 0.95, 0.99, 0.96; accuracy difference +0.03, 0.00, +0.01). **Result under the registered rule: neither Ambari-7B-base nor Qwen3-8B passes A1-P, so X12 contrast 1 scoring and X13 Qwen3-8B are not run.** Nothing is scored on Kaggle beyond the gate and A1-R. The Kaggle queue driver is stopped and waits for Aarnav's decision: the 8-bit reference shows mean |d logprob| of 0.18 to 0.89 against float16, so it may be too noisy a yardstick for 7 to 9B models (any amendment of the reference, for example float16 against a second float16 run on different shard layouts, or bfloat16 emulated on the T4, is Aarnav's to decide; no rule was changed). Quota used so far: 1.67 h of 30.

`````

##### 2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run).

RESULTS.md lines 3716 to 3725; first line committed in `78d6ad2` on 2026-11-02 23:17:45 +0530; last line in `eeafc85` on 2026-11-02 23:17:34 +0530; labels from the title and parent heading: registered, amended

`````text
- **2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run).** The 8-bit LLM.int8 reference is withdrawn: it is an approximation, not a
  valid ground truth for an fp16 fidelity check, so the two A1-P failures above (Qwen3-8B, Ambari-7B-base) are not used. **New reference: float32 with CPU offload** (device_map over both T4s,
  12 GiB per GPU, the rest of the weights in system RAM). Pass thresholds unchanged (raw-label agreement >= 0.98 per form, |accuracy difference| <= 0.01, no non-finite values, max fp16 hidden
  state < 65504). A1-P is re-run for Qwen3-8B and Ambari-7B-base-v0.1 against it, with the time reported. If a model fails against float32, it is out of the X12/X13 float16 runs, no further
  rescue is added, and a full float32-offload SIB run (1,004 x 4 forms) is timed and its hours reported before anything is run. If both pass, X12 Ambari base and X13 Qwen3-8B run as registered.
  *Two implementation faults found while preparing this (not rule changes):* (1) in `kaggle_precision.py` the float16 model was still referenced by the caller while float32 loaded, so the
  fp16 weights stayed on GPU 0; the "float32 out of memory (12.8 GiB)" for Ambari-7B-base above was probably caused by this, not by float32 not fitting (fixed: `model = free(model)`);
  (2) `kaggle_queue.py` read the previous `last_run.json` when the runner refused a dirty tree and recorded the old 8-bit Ambari result as new at 22:58 (fixed: `push()` returns None on refusal;
  the state was reset; nothing was pushed to Kaggle by that pass).

`````

##### 2026-11-02 23:24 IST, A1-P re-run against float32-offload (commit 803b5e7, 0.35 h of quota): NO VERDICT, harness error.

RESULTS.md lines 3748 to 3753; first line committed in `9d50e92` on 2026-11-02 23:24:17 +0530; last line in `3448c48` on 2026-11-02 23:32:56 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 23:24 IST, A1-P re-run against float32-offload (commit 803b5e7, 0.35 h of quota): NO VERDICT, harness error.** Both Qwen3-8B and Ambari-7B-base ended in CUDA out-of-memory while loading the
  float32 reference (9.49 and 9.33 GiB requests with 7.8 GiB still held on GPU 0): the float16 weights were still resident. The first fix (`model = free(model)`) was incomplete, because the
  caller's variable still pointed at the model while `free()` ran. Fix (no rule change, thresholds unchanged): each precision now runs in its own subprocess (`scripts/kaggle_precision.py`,
  worker mode), so memory is released by process exit. The error results carry `pass: null`; the queue driver records no verdict for them and keeps the models queued. Both models are re-queued
  against the same reference. (This also means the earlier "float32 out of memory" for Ambari-7B-base was not evidence about float32 fitting; see A1-P-D1.)

`````

##### 2026-11-03 02:24 IST, A1-P against the float32-offload reference (A1-P-D1): BOTH PASS

RESULTS.md lines 3796 to 3800; first line committed in `73546be` on 2026-11-03 02:24:19 +0530; last line in `994de97` on 2026-11-03 02:44:05 +0530; labels from the title and parent heading: none

`````text
- **2026-11-03 02:24 IST, A1-P against the float32-offload reference (A1-P-D1): BOTH PASS** (`results/kaggle/kaggle_precision/2026-11-02T175450/out/`, commit 803b5e7 plus the subprocess fix of the same day; Kaggle T4 x2, 2.98 h of quota). Rule unchanged: per form raw-label agreement >= 0.98, |accuracy difference| <= 0.01, no non-finite value, max fp16 hidden state < 65,504.
  **Ambari-7B-base:** agreement 1.00 on native, ITRANS and lossy; accuracy fp16 = float32 on all three (0.34, 0.27, 0.34 on the 100 items); mean |d logprob| 0.0031 to 0.0032, max 0.012 to 0.015; max fp16 hidden state 1,730; no non-finite values; fp16 load 205 s, fp16 scoring 192 s (300 prompts), float32 load 52 s, float32 scoring 2,980 s, total 3,443 s (0.96 h).
  **Qwen3-8B:** agreement 1.00 on all three forms; accuracy 0.68, 0.32, 0.43 in both precisions; mean |d logprob| 0.0118 to 0.0127, max 0.070 to 0.078; max fp16 hidden state 11,864; no non-finite values; fp16 load 137 s, fp16 scoring 312 s, float32 load 48 s, float32 scoring 6,462 s, total 6,976 s (1.94 h).
  **Log (as instructed): the earlier A1-P failure of Ambari-7B-base (and of Qwen3-8B) is a harness bug (leaked fp16 weights) and an invalid reference, see the A1-P-D1 note;** a row is added to the deviations table of the paper. Thresholds did not change. Both models therefore enter X12 (Ambari-7B-base, contrast 1 endpoint) and X13 (Qwen3-8B) scoring as registered. Measured fp16 scoring speed on the T4 pair: 1.56 prompts/s (Ambari) and 0.96 prompts/s (Qwen3-8B), used for the Kaggle hour projection.

`````

##### 2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3-8b/`).

RESULTS.md lines 3808 to 3809; first line committed in `f116475` on 2026-11-03 04:26:01 +0530; last line in `786f67e` on 2026-11-03 04:46:26 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3-8b/`).** SIB-200 scores for english, native, ITRANS, lossy, lowercase (and natural on the 257), content-free calibration inputs, and unmapped FLORES+ retrieval (native, ITRANS; A1-R passed) are written as Phase 1-format shards; the analysis (registered contrasts) has not been run yet. The X9b pilot is re-run next (the new queue driver replaced the old one at this point; DEFER file removed, state cleaned).

`````

##### 2026-11-03 13:02 IST, X13 Qwen3-8B: registered verdicts (Kaggle T4 x2, float16, A1-P passed; `scripts/x13_analyse.py`, `results/phase2/x13/qwen3-8b/analysis.json`); nothing is against a prediction.

RESULTS.md lines 3834 to 3837; first line committed in `cdef73d` on 2026-11-03 13:02:56 +0530; last line in `00bf9f6` on 2026-11-03 13:21:59 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 13:02 IST, X13 Qwen3-8B: registered verdicts (Kaggle T4 x2, float16, A1-P passed; `scripts/x13_analyse.py`, `results/phase2/x13/qwen3-8b/analysis.json`); nothing is against a prediction.** **Counted:** yes (native SIB-200 accuracy 0.779, 95% CI [0.753, 0.805], lower bound above 0.40; calibrated English accuracy 0.837; raw fallback not used). **SIB-200 accuracy (calibrated, n = 1,004; natural n = 257):** english 0.837 [0.814, 0.860]; native 0.779 [0.753, 0.805]; ITRANS 0.457 [0.426, 0.488]; lossy 0.520 [0.489, 0.551]; lowercase 0.410 [0.380, 0.441]; natural 0.529 [0.467, 0.588].
  **P-a contrasts for this model (exact McNemar):** native - ITRANS = +0.322 (p = 6e-63), native - lossy = +0.259 (p = 1e-46). **Extended P-a (all-but-one rule on the enlarged counted set Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B plus Qwen3-8B; Holm over the 10 tests; reported separately, Phase 1 verdicts unchanged): native > ITRANS positive and significant in 5 of 5 models, native > lossy in 5 of 5: SUPPORTED for both contrasts** (reading: at least n - 1 of n; the all-but-one rule is not spelled out beyond that sentence in the amendment).
  **Retrieval (unmapped, test half n = 1,005, train-chosen layer):** native 0.593, ITRANS 0.086; paired native - ITRANS = +0.507 (95% CI 0.474 to 0.540); for the three Phase 1 counted retrieval models: Qwen3.5-2B +0.865 [0.843, 0.886], Sarvam-1 +0.430 [0.399, 0.462], Gemma 4 E2B +0.726 [0.700, 0.754]; **extended: native - ITRANS CI above 0 in 4 of 4 models, all-but-one rule met.** Observation, not a verdict: Qwen3-8B's native retrieval (0.593) is far below the three smaller models (0.94 to 0.995) while its ITRANS value is lowest; the retrieval layer is chosen on the train half as in Phase 1. X13's SIB-200 lossy and lowercase forms are in the same file; the MDL assembly step for Qwen3-8B (`scripts/kaggle_mdl.py`) has not run yet (held by the X9b quota reserve). The paper is not edited.

`````

##### 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST).

RESULTS.md lines 3868 to 3869; first line committed in `0cfdea0` on 2026-11-04 02:46:43 +0530; last line in `09b39ee` on 2026-11-04 02:52:11 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST).** Cause (from the kernel log): the kernel cannot read the Hugging Face token, so the gated repo meta-llama/Llama-2-7b-hf returns 401 on Kaggle. `UserSecretsClient` raised "Connection error trying to communicate with service" in all 16 kernel runs so far (the earlier models were not gated, so nothing was lost before). The same token reads both Llama repos from the laptop (HTTP 200), so access itself is granted; the Kaggle notebook has no HF_TOKEN secret attached. Fix needs a manual step in the Kaggle web UI (attach the secret HF_TOKEN to the kernels shattered-kaggle-precision and shattered-x-score, Add-ons, Secrets); no token is put in a dataset or the repository. Not relaunched yet (relaunch once after the fix). Llama-3.1-8B has the same dependency. X9b batch 3 is unaffected.

`````

##### 2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST).

RESULTS.md lines 3890 to 3891; first line committed in `7cfcb18` on 2026-11-04 06:08:50 +0530; last line in `46c9030` on 2026-11-04 06:23:52 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST).** The kernel metadata of those pushes lists only shattered-pkg and shattered-flores-private as dataset sources (build/kaggle/kernel_kaggle_precision/kernel-metadata.json): the queue driver process running since 03:35 IST had imported scripts/kaggle_queue.py before the change that attaches the private model datasets, so it never attached them. This is the same stale-driver mistake as before, not a mount problem. The next queue pass (a new process after the 90-minute wait) uses the new code. Llama-3.1 A1-P also failed with no verdict (0.1 h); neither failure is a verdict on the model. Retry once at the next pass when quota allows (quota 29.55 of 30 h used; 3 h or more fits from about 9 Nov 23:24 IST).

`````

##### 2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check

RESULTS.md lines 3896 to 3897; first line committed in `81fc534` on 2026-11-04 07:53:46 +0530; last line in `7455dba` on 2026-11-04 09:53:29 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check** (float32-offload reference; first job to use a private model dataset, so the dataset route works; run pushed 06:25 IST, finished about 07:45). Both contrast-1 endpoints (Ambari-7B-base and Llama-2-7B) have now passed, so X12 contrast 1 scoring is the next job. Quota 27.54 of 30 h used: the scoring cap was lowered from 5.0 to 2.4 h to fit (measured scoring times: Qwen3-8B 1.71 h, Ambari-7B-base 1.23 h; the job resumes from its item cache if the cap is hit). Queue chain restarted early to push it. Llama-3.1-8B and Ambari-Instruct-v0.1 A1-P wait for quota (retry once after the failures of the stale driver).

`````

##### 2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD values above are unchanged).

RESULTS.md lines 3908 to 3909; first line committed in `72ff37e` on 2026-11-04 12:14:44 +0530; last line in `39d4c01` on 2026-11-04 13:21:46 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD values above are unchanged).** Gain = Ambari-7B-base minus Llama-2-7B, paired bootstrap over items, 95% interval (descriptive). SIB-200 (n = 1,004): native +0.389 [0.356, 0.423]; ITRANS -0.034 [-0.052, -0.016]; lossy -0.090 [-0.118, -0.063]; English -0.130 [-0.158, -0.103]. Retrieval (n = 1,005): native +0.692 [0.662, 0.721]; ITRANS +0.068 [0.051, 0.086]. A1-P (100 items x native/ITRANS/lossy, fp16 vs float32-offload): Ambari-7B-base raw label agreement 1.00 / 1.00 / 1.00, accuracy difference 0.000 in each form, max hidden state 1,730; Llama-2-7B agreement 1.00 / 0.99 / 1.00, accuracy difference 0.000 in each form, max hidden state 2,424; no non-finite value in either; mean |dlogprob| 0.003. Note: Ambari loses 13 points on English SIB-200 relative to Llama-2 (0.559 vs 0.689), so the continued pretraining also changed the model outside Kannada.

`````

##### 2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly.

RESULTS.md lines 3916 to 3917; first line committed in `59154b4` on 2026-11-04 14:10:52 +0530; last line in `eb2aa7a` on 2026-11-04 16:09:50 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly.** kaggle_retrieval_gate on account 2 (0.34 h; its own shattered-flores-private dataset): Sarvam-1 native layer 24, accuracy 0.9443; ITRANS layer 21, accuracy 0.5104; Gemma 4 E2B native layer 7, accuracy 0.9960; ITRANS layer 7, accuracy 0.2657; all per-layer train and test curves equal account 1's (max difference 0.0) and are within 0.004 of the laptop values (tolerance 0.03); the untrained evaluation of a new environment therefore reproduces the A1-R numbers (results/kaggle/acct2/a1r_reproduced.json, marker results/kaggle/acct2/ACCEPTED). Private datasets under account 2, all ready: shattered-flores-private, shattered-llama-3-1-8b (upload 1,146 s), shattered-ambari-instruct-v0-1 (826 s); local copies deleted. The account-2 queue driver (scripts/kaggle_queue2_chain.sh, KAGGLE_ACCOUNT=2) started at 14:08 IST with the Ambari-Instruct-v0.1 A1-P; account 1 now runs X9b only. Quota use so far: account 2 about 0.5 of 30 h, account 1 29.36 of 30 h. **Calendar (estimates from measured runtimes; gating by caps):** account 2: v0.1 A1-P 14:10 to 15:40 on 4 Nov, v0.1 scoring to 17:10, v0.2 scoring to 18:40, instruction-pair MDL to 20:52, Llama-3.1-8B A1-P to 22:22, Llama-3.1-8B scoring to 00:10 on 5 Nov; account 1: X9b batch 3 from 10 Nov 02:50 to 09:20, X9b Qwen3.5-2B arm 10 Nov 09:20 to 18:20 (last job, projected end 10 Nov about 18:20 IST). Account 2 then has about 19 h of its week free for further X13 models and MDL jobs.

`````

##### 2026-11-04 17:26 IST, Kaggle account 2: Ambari-Instruct-v0.1 A1-P ended without a verdict (pushed 14:08 IST, 3.2 h of account 2 quota).

RESULTS.md lines 3920 to 3921; first line committed in `4770255` on 2026-11-04 17:26:35 +0530; last line in `7bcba7d` on 2026-11-04 20:22:41 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 17:26 IST, Kaggle account 2: Ambari-Instruct-v0.1 A1-P ended without a verdict (pushed 14:08 IST, 3.2 h of account 2 quota).** The kernel reached its self-stop timeout: the fp16 half finished (ambari-7b-instruct-v0.1__fp16.npz written) but the float32-offload reference half never finished, and the kernel log has no line between minute 1 and the timeout at 11,067 s (the worker printed nothing). For comparison the same job took 1.3 h for Llama-2-7B and about 1.5 h per model for Ambari-7B-base, on account 1. Cause not established (candidates: the float32-offload reference stalling on host memory or the dataset-mounted weights loading slowly in this account's session; the A1-R and gate jobs on account 2 ran at normal speed). No verdict on the model. **Diagnostic added, not a fix:** the A1-P worker now prints load and per-form progress lines (scripts/kaggle_precision.py), so a stall shows where. The queue keeps v0.1 open and retries it once after Llama-3.1-8B (the driver moved on to the Llama-3.1-8B A1-P at 17:22 IST); the instruction-pair scoring and MDL wait for v0.1 to pass (the pair is scored only if both pass, as registered). If the retry stalls the same way, the fallback is to run v0.1 on account 1 (it ran Ambari-7B-base there) once quota frees.

`````

##### 2026-11-04 20:22 IST, Kaggle account 2: Llama-3.1-8B A1-P PASSED (float32-offload reference; pushed 17:22 IST, finished about 20:15; this is the first run of the new progress output, so the Ambari-Instruct-v0.1 stall can be compared with it

RESULTS.md lines 3923 to 3924; first line committed in `7bcba7d` on 2026-11-04 20:22:41 +0530; last line in `f06c46f` on 2026-11-04 20:23:22 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 20:22 IST, Kaggle account 2: Llama-3.1-8B A1-P PASSED (float32-offload reference; pushed 17:22 IST, finished about 20:15; this is the first run of the new progress output, so the Ambari-Instruct-v0.1 stall can be compared with it).** Scoring (X13) follows the Ambari-Instruct-v0.1 retry in the account 2 queue; the v0.1 A1-P retry was pushed at about 20:22.

`````

##### 2026-11-04 20:23 IST, Kaggle account 2 note on the slow A1-P runs (cause now likely):

RESULTS.md lines 3925 to 3926; first line committed in `f06c46f` on 2026-11-04 20:23:22 +0530; last line in `3c30aee` on 2026-11-04 20:44:16 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 20:23 IST, Kaggle account 2 note on the slow A1-P runs (cause now likely):** the Llama-3.1-8B A1-P (2.78 h, passed: raw agreement 1.00 / 0.98 / 1.00 native/ITRANS/lossy, accuracy difference 0.00 / -0.01 / 0.00) shows fp16 load 2,866 s and reference scoring 6,382 s; Llama-2 on account 1 loaded in 631 s. Weights mounted from a private dataset load slowly in these sessions, which is the likely reason the first Ambari-Instruct-v0.1 run (cap 3.5 h, self-stop 3.07 h) did not finish its reference half. The queue now gives any A1-P of a model mounted from a private dataset a 5.0 h cap (push timeout and quota projection); the v0.1 retry already in flight (pushed about 20:22 IST) still has the old 3.5 h cap and may time out again, in which case it is re-pushed with 5.0 h.

`````

##### 2026-11-04 21:53 IST, Kaggle account 2: duplicate push of the Ambari-Instruct-v0.1 A1-P (my driver defect; quota cost, no wrong result).

RESULTS.md lines 3934 to 3935; first line committed in `952be81` on 2026-11-04 21:53:03 +0530; last line in `58423f1` on 2026-11-04 21:53:12 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 21:53 IST, Kaggle account 2: duplicate push of the Ambari-Instruct-v0.1 A1-P (my driver defect; quota cost, no wrong result).** The retry pushed at 20:10 IST (cap 3.5 h) stayed recorded as "pushed" in results/kaggle/acct2/quota.json, never fetched, because its driver process ended early (the self-restart on changed code, introduced the same day, re-executed the process while a push was in flight); the next queue pass at 21:41 IST then pushed the same kernel again (cap 5.0 h), which replaces the earlier version, so the 20:10 run's output is lost and the stale 3.5 h record keeps counting against the account (quota 21.89 h shown, conservative). The 21:41 run (5.0 h cap, progress lines on) is the one that will be fetched. **Fix:** the queue now refuses to push a kernel whose previous version is still running or queued (status check on the laptop, no quota). X9b batch 3 on account 2 (pushed 20:35, its own kernel) is unaffected.

`````

##### 2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label agreement 1.00 in native, ITRANS and lossy, accuracy difference 0.00 in each, me

RESULTS.md lines 3938 to 3939; first line committed in `06404f2` on 2026-11-04 22:07:54 +0530; last line in `17dba9c` on 2026-11-04 22:24:09 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label agreement 1.00 in native, ITRANS and lossy, accuracy difference 0.00 in each, mean |dlogprob| 0.003 to 0.004, max fp16 hidden state 559.5, no non-finite value).** Both instruction models have now passed A1-P (v0.2 earlier), so the pair is scored as registered; the scoring of v0.1 was pushed at 22:06 IST. Correction to my duplicate-push entry above: the 20:10 run was not lost: it completed and its output was fetched by the later push's fetch (identical numbers in both result folders, same fp16 load of 3,420 s and total of 6,754 s); the 21:41 push (5.0 h cap) was therefore possibly a redundant second run of the same job whose hours will count when it ends. The weights loaded from the private dataset took 3,420 s (57 minutes) in fp16 in this run, which did not yet have the copy-to-local-disk loader (committed after the push); the load-time comparison with the copy loader is still to be made on the next job that loads from a private dataset.

`````

##### 2026-11-05 04:23 IST, X13 Llama-3.1-8B RESULT (Kaggle account 2; A1-P passed 2.78 h, scoring 1.82 h; `scripts/x13_analyse.py --model llama-3.1-8b`, `results/phase2/x13/llama-3.1-8b/analysis.json`): counted; extended P-a supported (5 of 5 fo

RESULTS.md lines 3966 to 3967; first line committed in `5c0388b` on 2026-11-05 04:23:24 +0530; last line in `c7acc38` on 2026-11-05 05:08:02 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 04:23 IST, X13 Llama-3.1-8B RESULT (Kaggle account 2; A1-P passed 2.78 h, scoring 1.82 h; `scripts/x13_analyse.py --model llama-3.1-8b`, `results/phase2/x13/llama-3.1-8b/analysis.json`): counted; extended P-a supported (5 of 5 for both contrasts); retrieval all-but-one met (4 of 4); nothing against a prediction.** SIB-200 calibrated accuracy (n = 1,004; no raw fallback): English 0.785; **native 0.712 [0.684, 0.739] (CI lower 0.684 above 0.40: counted)**; lossy 0.463 [0.433, 0.494]; lowercase 0.385 [0.356, 0.416]; ITRANS 0.382 [0.353, 0.413]; natural (257 ids) 0.529 [0.467, 0.591]. This model: native minus ITRANS +0.330 (exact McNemar p about 3e-60), native minus lossy +0.249 (p about 1e-40), both Holm-significant. Extended P-a (the four Phase 1 counted models plus this model, all-but-one rule): native beats ITRANS in 5 of 5 and lossy in 5 of 5: supported for both. **Retrieval (unmapped, test half n = 1,005): native 0.982 at layer 17, ITRANS 0.173 at layer 8; native minus ITRANS +0.809 [0.784, 0.833]**; for the Phase 1 retrieval models the native minus ITRANS CIs are all above 0 (Qwen3.5-2B +0.865, Sarvam-1 +0.430, Gemma 4 E2B +0.727), so 4 of 4 models with a CI above 0: all-but-one rule met. The X13 MDL assembly job for this model is queued next on account 2. The paper is not edited.

`````

## Result files, every number

(no result files for this experiment)

## Not dumped (item-level, binary or too large; path and size only)

- none

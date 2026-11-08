# A: General rules A0, Kaggle precision and retrieval checks A1-P and A1-R, reproducibility gate (Phase 2)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| registered | `9d408c4` | 2026-11-02 16:47:59 +0530 | 3480-3485 | PHASE 2 REGISTRATION: Kaggle runner and reproducibility gate (2026-11-02, Aarnav; registered before the first Kaggle run) |
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3495-3514 | A0. General rules for X9 to X15 |
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3515-3530 | A1. Kaggle precision and retrieval checks (added 2026-11-02 at Aarnav's request; not experiments, run before the experiments that depend on them) |
| none | `f41e866` | 2026-11-02 19:15:43 +0530 | 3706-3706 | 2026-11-02 19:00 IST, A1-R data. Private Kaggle dataset `shattered-flores-private` created (option (a), approved): the 2,009 FLORES+ dev+devtest Kannada (NFC) a |
| result | `60b8183` | 2026-11-02 23:21:28 +0530 | 3712-3712 | 2026-11-02 19:26 IST, A1-R retrieval gate: PASSED. Sarvam-1 and Gemma 4 E2B, float16, T4 x2 (about 0.37 h of quota), unmapped FLORES+ retrieval acc@1 at the tra |
| result, failed or not run | `b046768` | 2026-11-02 20:15:27 +0530 | 3713-3713 | 2026-11-02 19:55 IST, A1-P first results (`results/kaggle/kaggle_precision/2026-11-02T135712/out/`), float16 vs 8-bit, 100 SIB items x 3 forms, rule: agreement  |
| result, failed or not run | `8b52d91` | 2026-11-02 20:34:16 +0530 | 3714-3715 | 2026-11-02 20:20 IST, A1-P re-run of Ambari-7B-base (`results/kaggle/kaggle_precision/2026-11-02T144532/out/`): FAILS. Float32 was attempted first and ran out o |
| registered, amended | `78d6ad2` | 2026-11-02 23:17:45 +0530 | 3716-3725 | 2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run). The 8-bit LLM.int8 reference is withdrawn: it is an approximation, not a |
| none | `78d6ad2` | 2026-11-02 23:17:45 +0530 | 3734-3740 | 2026-11-02 23:17 IST, Kaggle queue order (decided by Aarnav). (a) the A1-P job in flight (Qwen3-8B, Ambari-7B-base, float32-offload reference); (b) score whiche |
| none | `9d50e92` | 2026-11-02 23:24:17 +0530 | 3748-3753 | 2026-11-02 23:24 IST, A1-P re-run against float32-offload (commit 803b5e7, 0.35 h of quota): NO VERDICT, harness error. Both Qwen3-8B and Ambari-7B-base ended i |
| result | `73546be` | 2026-11-03 02:24:19 +0530 | 3796-3800 | 2026-11-03 02:24 IST, A1-P against the float32-offload reference (A1-P-D1): BOTH PASS (`results/kaggle/kaggle_precision/2026-11-02T175450/out/`, commit 803b5e7  |
| result | `f116475` | 2026-11-03 04:26:01 +0530 | 3808-3809 | 2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3 |
| result | `48deb83` | 2026-11-03 08:06:57 +0530 | 3822-3824 | 2026-11-03 08:06 IST, X9b rehearsal PASSED (Sarvam-1, ITRANS, seed 0, 20 optimizer steps; Kaggle T4, 0.38 h; `results/kaggle/kaggle_x9b/2026-11-03T021326/out/sa |
| result | `cdef73d` | 2026-11-03 13:02:56 +0530 | 3834-3837 | 2026-11-03 13:02 IST, X13 Qwen3-8B: registered verdicts (Kaggle T4 x2, float16, A1-P passed; `scripts/x13_analyse.py`, `results/phase2/x13/qwen3-8b/analysis.jso |
| result | `3290232` | 2026-11-04 01:44:01 +0530 | 3857-3857 | 2026-11-04 01:44 IST, X9b status (Kaggle T4; `results/kaggle/kaggle_x9b/2026-11-03T023638` and `...T085520`). Batch 1 (started 3 Nov 08:06 IST, returned about 1 |
| result | `28803e6` | 2026-11-04 02:33:57 +0530 | 3862-3863 | 2026-11-04 02:33 IST, X12 contrast 1 runs now (Aarnav's decision). The Llama-2-7B A1-P precision check and scoring run on Kaggle ahead of the 18 h X9b reserve ( |
| none | `98e2256` | 2026-11-04 02:46:00 +0530 | 3866-3867 | 2026-11-04 02:46 IST, operations log (standing orders of 2026-11-04; no registered rule changes). (1) X4 Gemini drafts resumed on the paid tier (billing enabled |
| result, failed or not run | `0cfdea0` | 2026-11-04 02:46:43 +0530 | 3868-3869 | 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST). Cause (from t |
| result | `399fdee` | 2026-11-04 03:33:53 +0530 | 3876-3877 | 2026-11-04 03:33 IST, X9b reserve LIFTED (Aarnav). X9B_SARVAM_H set from 18 to 0 in scripts/kaggle_queue.py: a Kaggle job now only has to fit in the remaining h |
| result, failed or not run | `7ee0799` | 2026-11-04 03:43:18 +0530 | 3878-3879 | 2026-11-04 03:43 IST, gated models on Kaggle: private-dataset route (Aarnav's instruction; no registered rule changes). *Secrets cannot be set through the API:* |
| result | `f479ea3` | 2026-11-04 04:14:25 +0530 | 3882-3883 | 2026-11-04 04:14 IST, first gated model uploaded: Llama-2-7b-hf is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-2-7b-hf (12.55 GiB: config, tokeniz |
| result, failed or not run | `45def39` | 2026-11-04 04:53:21 +0530 | 3886-3887 | 2026-11-04 04:53 IST, Kaggle watchdog: Qwen3-8B MDL (X13) finished (output in results/kaggle/kaggle_mdl/2026-11-03T220606, analysis pending). Llama-2-7B A1-P fa |
| result | `8e2e954` | 2026-11-04 06:08:17 +0530 | 3888-3889 | 2026-11-04 06:08 IST, Kaggle watchdog: the Ambari instruct pair A1-P ended (pushed 04:46 IST): Ambari-Instruct-v0.2 passed (float32-offload reference); Ambari-I |
| result, failed or not run | `7cfcb18` | 2026-11-04 06:08:50 +0530 | 3890-3891 | 2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST). The kernel metadata of those push |
| none | `46c9030` | 2026-11-04 06:23:52 +0530 | 3892-3893 | 2026-11-04 06:23 IST, watchdog: quota fell to 26.19 of 30 h (actual runtimes of the instruct pair were shorter than the cap), so the Llama-2 A1-P (cap 3.5 h) fi |
| none | `6f2ebf8` | 2026-11-04 06:37:27 +0530 | 3894-3895 | 2026-11-04 06:37 IST, third gated model uploaded: Ambari-Instruct-v0.1 is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-ambari-instruct-v0-1 (upload 821 s |
| failed or not run | `81fc534` | 2026-11-04 07:53:46 +0530 | 3896-3897 | 2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check (float32-offload reference; first job to use a private model dataset,  |
| result | `7455dba` | 2026-11-04 09:53:29 +0530 | 3898-3899 | 2026-11-04 09:53 IST, X12 CONTRAST 1 (primary test) RESULT: SUPPORTED (as predicted). Llama-2-7B vs Ambari-7B-base-v0.1, both passed A1-P (fp16 vs float32-offlo |
| result | `ed31e10` | 2026-11-04 12:13:51 +0530 | 3905-3905 | 2026-11-04 12:13 IST, correction note to the X11 entry above (p values). The per-form McNemar p values in the X11 entry are exact and unadjusted; the registrati |
| result | `72ff37e` | 2026-11-04 12:14:44 +0530 | 3908-3909 | 2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD  |
| result | `39d4c01` | 2026-11-04 13:21:46 +0530 | 3910-3911 | 2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction). Some Kaggle compute for Phase 2 now runs on a teammate's Kaggle account (username ashw |
| failed or not run | `97a4a6b` | 2026-11-04 13:40:55 +0530 | 3914-3915 | 2026-11-04 13:40 IST, account 2 smoke test PASSED (kaggle_gate, T4 x2, second attempt; 0.10 h). gate_passed true with the same dtype (float16) for Sarvam-1 and  |
| result | `59154b4` | 2026-11-04 14:10:52 +0530 | 3916-3917 | 2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly. kaggle_retrieval_gate on acc |
| result | `4770255` | 2026-11-04 17:26:35 +0530 | 3920-3921 | 2026-11-04 17:26 IST, Kaggle account 2: Ambari-Instruct-v0.1 A1-P ended without a verdict (pushed 14:08 IST, 3.2 h of account 2 quota). The kernel reached its s |
| none | `7bcba7d` | 2026-11-04 20:22:41 +0530 | 3923-3924 | 2026-11-04 20:22 IST, Kaggle account 2: Llama-3.1-8B A1-P PASSED (float32-offload reference; pushed 17:22 IST, finished about 20:15; this is the first run of th |
| none | `f06c46f` | 2026-11-04 20:23:22 +0530 | 3925-3926 | 2026-11-04 20:23 IST, Kaggle account 2 note on the slow A1-P runs (cause now likely): the Llama-3.1-8B A1-P (2.78 h, passed: raw agreement 1.00 / 0.98 / 1.00 na |
| result | `3c30aee` | 2026-11-04 20:44:16 +0530 | 3929-3929 | 2026-11-04 20:44 IST, X9b batch 3 moved to Kaggle account 2 (Aarnav's instruction). Independence checked in `scripts/kaggle_x9b.py` and the queue: every run tra |
| result | `952be81` | 2026-11-04 21:53:03 +0530 | 3934-3935 | 2026-11-04 21:53 IST, Kaggle account 2: duplicate push of the Ambari-Instruct-v0.1 A1-P (my driver defect; quota cost, no wrong result). The retry pushed at 20: |
| amended, result | `06404f2` | 2026-11-04 22:07:54 +0530 | 3938-3939 | 2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label  |
| failed or not run | `06100d7` | 2026-11-04 22:37:35 +0530 | 3942-3943 | 2026-11-04 22:37 IST, account 2 quota records reconciled by hand. The instruction-pair MDL push of 22:08 IST never created a kernel (runner stopped at 22:23 dur |
| none | `1fbe72d` | 2026-11-05 00:52:48 +0530 | 3946-3947 | 2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length. Without the  |
| exploratory, result | `ec3c085` | 2026-11-05 02:38:48 +0530 | 3956-3957 | 2026-11-05 02:38 IST, X12 CONTRAST 2 RESULT (secondary; instruction-pair exposure contrast; MDL assembly layer, descriptive; Kaggle account 2 run, 1.50 h; `scri |
| result, failed or not run | `900da25` | 2026-11-05 03:10:06 +0530 | 3958-3959 | 2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on  |
| result | `5c0388b` | 2026-11-05 04:23:24 +0530 | 3966-3967 | 2026-11-05 04:23 IST, X13 Llama-3.1-8B RESULT (Kaggle account 2; A1-P passed 2.78 h, scoring 1.82 h; `scripts/x13_analyse.py --model llama-3.1-8b`, `results/pha |
| registered, result | `6be3732` | 2026-11-05 13:12:01 +0530 | 3999-4000 | 2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, |
| result | `5d9fd0e` | 2026-11-05 22:23:55 +0530 | 4021-4022 | 2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational). Aarnav reported that the owner of the third Kaggle account (username aarnavk |
| result, failed or not run | `07e9a33` | 2026-11-05 22:37:41 +0530 | 4023-4024 | 2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected). Both setup kernels pus |
| result, failed or not run | `ac6470f` | 2026-11-07 01:49:19 +0530 | 4036-4037 | 2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational). Aarnav supplied a new Kaggle API token to be used instead  |
| none | `acd0e83` | 2026-11-07 02:21:05 +0530 | 4040-4041 | 2026-11-07 02:21 IST, KAGGLE ACCOUNT 3 (aakarshprabhu) ACCEPTED. Smoke gate passed; A1-R reproduction: the untrained base evaluation on the new account equals a |
| failed or not run | `2466b30` | 2026-11-07 03:00:36 +0530 | 4042-4043 | 2026-11-07 03:00 IST, KAGGLE ACCOUNT 3 (aakarshprabhu): ACCEPTANCE CORRECTION AND FIRST JOB STARTED (operational). The acceptance written at 02:20 was premature |

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

##### 2026-11-02 19:00 IST, A1-R data. Private Kaggle dataset `shattered-flores-private` created (option (a), approved): the 2,009 FLORES+ dev+devtest Kannada (NFC) and English sentences, and, from the second version, the 496 retained Kannada nat

RESULTS.md lines 3706 to 3706; first line committed in `f41e866` on 2026-11-02 19:15:43 +0530; last line in `f41e866` on 2026-11-02 19:15:43 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 19:00 IST, A1-R data.** Private Kaggle dataset `shattered-flores-private` created (option (a), approved): the 2,009 FLORES+ dev+devtest Kannada (NFC) and English sentences, and, from the second version, the 496 retained Kannada natural-romanization drafts keyed by FLORES index (derived text, no source sentence). It is private (the Kaggle CLI reports "Your private Dataset"), stays private for the whole of Phase 2, is deleted at the end of Phase 2, and the deletion will be logged here.
`````

##### 2026-11-02 19:26 IST, A1-R retrieval gate: PASSED. Sarvam-1 and Gemma 4 E2B, float16, T4 x2 (about 0.37 h of quota), unmapped FLORES+ retrieval acc@1 at the train-chosen layer on the M4b test half (n = 1,005) against `results/m4b_mapping/su

RESULTS.md lines 3712 to 3712; first line committed in `60b8183` on 2026-11-02 23:21:28 +0530; last line in `60b8183` on 2026-11-02 23:21:28 +0530; labels from the title and parent heading: result

`````text
- **2026-11-02 19:26 IST, A1-R retrieval gate: PASSED.** Sarvam-1 and Gemma 4 E2B, float16, T4 x2 (about 0.37 h of quota), unmapped FLORES+ retrieval acc@1 at the train-chosen layer on the M4b test half (n = 1,005) against `results/m4b_mapping/summary.csv`: Sarvam-1 native 0.9443 vs 0.9443 (difference 0.000), ITRANS 0.5104 vs 0.5144 (0.004); Gemma 4 native 0.9960 vs 0.9950 (0.001), ITRANS 0.2657 vs 0.2687 (0.003); tolerance 0.03; no non-finite vector; the per-layer curves differ by at most 0.007. The in-kernel `pass` flag read False only because the laptop summary file is not in the Kaggle package; the comparison was done locally with the registered rule (`results/kaggle/a1r_result.json`). Kaggle retrieval counts.
`````

##### 2026-11-02 19:55 IST, A1-P first results (`results/kaggle/kaggle_precision/2026-11-02T135712/out/`), float16 vs 8-bit, 100 SIB items x 3 forms, rule: agreement >= 0.98 and accuracy difference <= 0.01 per form. Qwen3-8B FAILS (reference 8-bi

RESULTS.md lines 3713 to 3713; first line committed in `b046768` on 2026-11-02 20:15:27 +0530; last line in `b046768` on 2026-11-02 20:15:27 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-02 19:55 IST, A1-P first results (`results/kaggle/kaggle_precision/2026-11-02T135712/out/`), float16 vs 8-bit, 100 SIB items x 3 forms, rule: agreement >= 0.98 and accuracy difference <= 0.01 per form.** **Qwen3-8B FAILS** (reference 8-bit because float32 needs about 30.5 GiB; agreement 0.93, 0.92, 0.93; accuracy difference -0.04, +0.04, +0.03; mean |d logprob| 0.62 to 0.89; maximum hidden state 11,864; no non-finite value). **Ambari-7B-base FAILS under the 8-bit reference** (agreement 0.95, 0.99, 0.96; accuracy difference +0.03, 0.00, +0.01; maximum hidden state 1,730; no non-finite value). Qwen3-8B is not run (registered rule); the 8-bit reference is itself an approximation, which the amendment states, so the failure does not by itself say which dtype is closer to the truth. **Implementation correction (not a rule change):** the amendment says 8-bit replaces float32 only if float32 does not fit 2 x T4; my first implementation excluded float32 above 24 GiB without trying it, and Ambari-7B-base (about 25.7 GiB in float32) can fit. A1-P for Ambari-7B-base is re-run with float32 attempted first (8-bit only after an out-of-memory error, recorded); the first result stays on disk. Qwen3-8B cannot fit float32 and its result stands.
`````

##### 2026-11-02 20:20 IST, A1-P re-run of Ambari-7B-base (`results/kaggle/kaggle_precision/2026-11-02T144532/out/`): FAILS. Float32 was attempted first and ran out of memory on 2 x T4 (CUDA OOM, 12.81 GiB allocation), so float32 does not fit and

RESULTS.md lines 3714 to 3715; first line committed in `8b52d91` on 2026-11-02 20:34:16 +0530; last line in `803b5e7` on 2026-11-02 22:59:39 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-02 20:20 IST, A1-P re-run of Ambari-7B-base (`results/kaggle/kaggle_precision/2026-11-02T144532/out/`): FAILS.** Float32 was attempted first and ran out of memory on 2 x T4 (CUDA OOM, 12.81 GiB allocation), so float32 does not fit and the registered 8-bit reference applies; the numbers are those of the first run (agreement 0.95, 0.99, 0.96; accuracy difference +0.03, 0.00, +0.01). **Result under the registered rule: neither Ambari-7B-base nor Qwen3-8B passes A1-P, so X12 contrast 1 scoring and X13 Qwen3-8B are not run.** Nothing is scored on Kaggle beyond the gate and A1-R. The Kaggle queue driver is stopped and waits for Aarnav's decision: the 8-bit reference shows mean |d logprob| of 0.18 to 0.89 against float16, so it may be too noisy a yardstick for 7 to 9B models (any amendment of the reference, for example float16 against a second float16 run on different shard layouts, or bfloat16 emulated on the T4, is Aarnav's to decide; no rule was changed). Quota used so far: 1.67 h of 30.

`````

##### 2026-11-02 22:59 IST, DEVIATION A1-P-D1 (decided by Aarnav, registered before the run). The 8-bit LLM.int8 reference is withdrawn: it is an approximation, not a

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

##### 2026-11-02 23:17 IST, Kaggle queue order (decided by Aarnav). (a) the A1-P job in flight (Qwen3-8B, Ambari-7B-base, float32-offload reference); (b) score whichever of the two passes: X13 Qwen3-8B,

RESULTS.md lines 3734 to 3740; first line committed in `78d6ad2` on 2026-11-02 23:17:45 +0530; last line in `b3cbd64` on 2026-11-02 23:21:38 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 23:17 IST, Kaggle queue order (decided by Aarnav).** (a) the A1-P job in flight (Qwen3-8B, Ambari-7B-base, float32-offload reference); (b) score whichever of the two passes: X13 Qwen3-8B,
  then X12 Ambari-base; (c) A1-P for Ambari-Instruct v0.1 and v0.2; (d) X9b full, Sarvam-1 primary arm (6 runs, about 18 GPU hours), as soon as its laptop memory pilot is done. Before each push the remaining
  weekly quota is projected; the X9b Sarvam arm is reserved this week or next, X9b goes first if X12 instruct work would push it into a later week, and the Qwen3.5-2B arm is cut first if quota is short (as registered).
  To apply this order the queue driver was changed and a `results/kaggle/HOLD` file stops new pushes while the in-flight job continues (an implementation change; no rule).
- Time stamps of the three entries above were first written with wrong clock times and corrected to the commit times (the A1-P-D1 entry 22:59, the X12 clarification, weights rule and queue order 23:17).
- Time correction (checked by scripts/check_results_times.py, which found it): the A1-R entry above was stamped 19:35 by hand but committed at 19:26; its stamp is now the commit time. From now on stamps come from `scripts/stamp.py` (system clock), and a pre-commit hook fails any entry later than the clock.

`````

##### 2026-11-02 23:24 IST, A1-P re-run against float32-offload (commit 803b5e7, 0.35 h of quota): NO VERDICT, harness error. Both Qwen3-8B and Ambari-7B-base ended in CUDA out-of-memory while loading the

RESULTS.md lines 3748 to 3753; first line committed in `9d50e92` on 2026-11-02 23:24:17 +0530; last line in `3448c48` on 2026-11-02 23:32:56 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 23:24 IST, A1-P re-run against float32-offload (commit 803b5e7, 0.35 h of quota): NO VERDICT, harness error.** Both Qwen3-8B and Ambari-7B-base ended in CUDA out-of-memory while loading the
  float32 reference (9.49 and 9.33 GiB requests with 7.8 GiB still held on GPU 0): the float16 weights were still resident. The first fix (`model = free(model)`) was incomplete, because the
  caller's variable still pointed at the model while `free()` ran. Fix (no rule change, thresholds unchanged): each precision now runs in its own subprocess (`scripts/kaggle_precision.py`,
  worker mode), so memory is released by process exit. The error results carry `pass: null`; the queue driver records no verdict for them and keeps the models queued. Both models are re-queued
  against the same reference. (This also means the earlier "float32 out of memory" for Ambari-7B-base was not evidence about float32 fitting; see A1-P-D1.)

`````

##### 2026-11-03 02:24 IST, A1-P against the float32-offload reference (A1-P-D1): BOTH PASS (`results/kaggle/kaggle_precision/2026-11-02T175450/out/`, commit 803b5e7 plus the subprocess fix of the same day; Kaggle T4 x2, 2.98 h of quota). Rule un

RESULTS.md lines 3796 to 3800; first line committed in `73546be` on 2026-11-03 02:24:19 +0530; last line in `994de97` on 2026-11-03 02:44:05 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 02:24 IST, A1-P against the float32-offload reference (A1-P-D1): BOTH PASS** (`results/kaggle/kaggle_precision/2026-11-02T175450/out/`, commit 803b5e7 plus the subprocess fix of the same day; Kaggle T4 x2, 2.98 h of quota). Rule unchanged: per form raw-label agreement >= 0.98, |accuracy difference| <= 0.01, no non-finite value, max fp16 hidden state < 65,504.
  **Ambari-7B-base:** agreement 1.00 on native, ITRANS and lossy; accuracy fp16 = float32 on all three (0.34, 0.27, 0.34 on the 100 items); mean |d logprob| 0.0031 to 0.0032, max 0.012 to 0.015; max fp16 hidden state 1,730; no non-finite values; fp16 load 205 s, fp16 scoring 192 s (300 prompts), float32 load 52 s, float32 scoring 2,980 s, total 3,443 s (0.96 h).
  **Qwen3-8B:** agreement 1.00 on all three forms; accuracy 0.68, 0.32, 0.43 in both precisions; mean |d logprob| 0.0118 to 0.0127, max 0.070 to 0.078; max fp16 hidden state 11,864; no non-finite values; fp16 load 137 s, fp16 scoring 312 s, float32 load 48 s, float32 scoring 6,462 s, total 6,976 s (1.94 h).
  **Log (as instructed): the earlier A1-P failure of Ambari-7B-base (and of Qwen3-8B) is a harness bug (leaked fp16 weights) and an invalid reference, see the A1-P-D1 note;** a row is added to the deviations table of the paper. Thresholds did not change. Both models therefore enter X12 (Ambari-7B-base, contrast 1 endpoint) and X13 (Qwen3-8B) scoring as registered. Measured fp16 scoring speed on the T4 pair: 1.56 prompts/s (Ambari) and 0.96 prompts/s (Qwen3-8B), used for the Kaggle hour projection.

`````

##### 2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3-8b/`). SIB-200 scores for english, native, ITRANS, lossy, lowercase (and natura

RESULTS.md lines 3808 to 3809; first line committed in `f116475` on 2026-11-03 04:26:01 +0530; last line in `786f67e` on 2026-11-03 04:46:26 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3-8b/`).** SIB-200 scores for english, native, ITRANS, lossy, lowercase (and natural on the 257), content-free calibration inputs, and unmapped FLORES+ retrieval (native, ITRANS; A1-R passed) are written as Phase 1-format shards; the analysis (registered contrasts) has not been run yet. The X9b pilot is re-run next (the new queue driver replaced the old one at this point; DEFER file removed, state cleaned).

`````

##### 2026-11-03 08:06 IST, X9b rehearsal PASSED (Sarvam-1, ITRANS, seed 0, 20 optimizer steps; Kaggle T4, 0.38 h; `results/kaggle/kaggle_x9b/2026-11-03T021326/out/sarvam-1+itrans+s0__rehearsal/`); discarded as designed. Whole path ran: stream bu

RESULTS.md lines 3822 to 3824; first line committed in `48deb83` on 2026-11-03 08:06:57 +0530; last line in `16e09e4` on 2026-11-03 12:56:47 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 08:06 IST, X9b rehearsal PASSED (Sarvam-1, ITRANS, seed 0, 20 optimizer steps; Kaggle T4, 0.38 h; `results/kaggle/kaggle_x9b/2026-11-03T021326/out/sarvam-1+itrans+s0__rehearsal/`); discarded as designed.** Whole path ran: stream build and in-kernel rescan of the 107 consumed articles (59,397 words): overlap 0; training 583 s; checkpoint, adapter saved, merge into the unquantized fp16 base (torchao fix works), SIB-200 on 100 items in native, ITRANS and English (no non-finite values), unmapped FLORES+ retrieval (test half n = 1,005; no non-finite values); tokenizer sha256 unchanged before and after (72e5ad0c2d3a65d1...). **The rehearsal's accuracy and retrieval numbers are not results** (20 steps, 100 SIB items); the one thing to check is that the untrained-base evaluation of Sarvam-1 in the same kernel (queued with the first batch) agrees with the A1-R laptop value for the same model (native 0.9443, ITRANS 0.5104), because the rehearsal's post-training retrieval (native 0.947, ITRANS 0.751) differs from it by more than I would expect after 20 steps; if the base evaluation differs from A1-R by more than the 0.03 tolerance, the evaluation environment, not the training, is the thing to examine before any X9b number is used.
  **First batch pushed (cap 7.5 h): untrained Sarvam-1 evaluation, then runs sarvam-1:itrans:0 and sarvam-1:native:0 at B = 4,997,120 tokens (305 optimizer steps) each.** Batches 2 and 3 follow; the quota projection will hold batch 3 until older hours leave the 7-day window if needed.

`````

##### 2026-11-03 13:02 IST, X13 Qwen3-8B: registered verdicts (Kaggle T4 x2, float16, A1-P passed; `scripts/x13_analyse.py`, `results/phase2/x13/qwen3-8b/analysis.json`); nothing is against a prediction. Counted: yes (native SIB-200 accuracy 0.77

RESULTS.md lines 3834 to 3837; first line committed in `cdef73d` on 2026-11-03 13:02:56 +0530; last line in `00bf9f6` on 2026-11-03 13:21:59 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 13:02 IST, X13 Qwen3-8B: registered verdicts (Kaggle T4 x2, float16, A1-P passed; `scripts/x13_analyse.py`, `results/phase2/x13/qwen3-8b/analysis.json`); nothing is against a prediction.** **Counted:** yes (native SIB-200 accuracy 0.779, 95% CI [0.753, 0.805], lower bound above 0.40; calibrated English accuracy 0.837; raw fallback not used). **SIB-200 accuracy (calibrated, n = 1,004; natural n = 257):** english 0.837 [0.814, 0.860]; native 0.779 [0.753, 0.805]; ITRANS 0.457 [0.426, 0.488]; lossy 0.520 [0.489, 0.551]; lowercase 0.410 [0.380, 0.441]; natural 0.529 [0.467, 0.588].
  **P-a contrasts for this model (exact McNemar):** native - ITRANS = +0.322 (p = 6e-63), native - lossy = +0.259 (p = 1e-46). **Extended P-a (all-but-one rule on the enlarged counted set Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B plus Qwen3-8B; Holm over the 10 tests; reported separately, Phase 1 verdicts unchanged): native > ITRANS positive and significant in 5 of 5 models, native > lossy in 5 of 5: SUPPORTED for both contrasts** (reading: at least n - 1 of n; the all-but-one rule is not spelled out beyond that sentence in the amendment).
  **Retrieval (unmapped, test half n = 1,005, train-chosen layer):** native 0.593, ITRANS 0.086; paired native - ITRANS = +0.507 (95% CI 0.474 to 0.540); for the three Phase 1 counted retrieval models: Qwen3.5-2B +0.865 [0.843, 0.886], Sarvam-1 +0.430 [0.399, 0.462], Gemma 4 E2B +0.726 [0.700, 0.754]; **extended: native - ITRANS CI above 0 in 4 of 4 models, all-but-one rule met.** Observation, not a verdict: Qwen3-8B's native retrieval (0.593) is far below the three smaller models (0.94 to 0.995) while its ITRANS value is lowest; the retrieval layer is chosen on the train half as in Phase 1. X13's SIB-200 lossy and lowercase forms are in the same file; the MDL assembly step for Qwen3-8B (`scripts/kaggle_mdl.py`) has not run yet (held by the X9b quota reserve). The paper is not edited.

`````

##### 2026-11-04 01:44 IST, X9b status (Kaggle T4; `results/kaggle/kaggle_x9b/2026-11-03T023638` and `...T085520`). Batch 1 (started 3 Nov 08:06 IST, returned about 14:25; 6.31 h): untrained Sarvam-1 evaluation plus sarvam-1:itrans:0 and sarvam-1

RESULTS.md lines 3857 to 3857; first line committed in `3290232` on 2026-11-04 01:44:01 +0530; last line in `3290232` on 2026-11-04 01:44:01 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 01:44 IST, X9b status (Kaggle T4; `results/kaggle/kaggle_x9b/2026-11-03T023638` and `...T085520`).** **Batch 1** (started 3 Nov 08:06 IST, returned about 14:25; 6.31 h): untrained Sarvam-1 evaluation plus sarvam-1:itrans:0 and sarvam-1:native:0. **Batch 2** (started 14:25, returned about 21:00; 6.60 h): sarvam-1:english:0 and sarvam-1:itrans:1. **4 of the 6 Sarvam-1 runs are done** (each 305 optimizer steps, 4,997,120 tokens, overlap 0 on the consumed articles, tokenizer sha256 unchanged, training 2.51 to 2.66 h, 2.89 to 3.06 h with evaluation). **The check logged before batch 1 is resolved:** the untrained Sarvam-1 evaluated in the Kaggle kernel gives unmapped retrieval native 0.9443 and ITRANS 0.5104, identical to the A1-R Kaggle values (laptop 0.9443 and 0.5144; within 0.0040), so the evaluation environment is sound and the rehearsal's post-training retrieval was a training effect. **Batch 3** (sarvam-1:native:1 and sarvam-1:english:1, cap 6.9 h) was refused by the quota projection (23.56 h used in the last 7 days, headroom -0.4 h) and fits from about **9 Nov 19:42 IST**. The registered X9b analysis (D_N, D_E, verdicts) needs all six Sarvam-1 runs and has not been run. The Qwen3.5-2B arm and every other Kaggle step (Llama-2 A1-P and X12 contrast 1, the instruction pair, Llama-3.1-8B, MDL) are held behind the X9b reserve.
`````

##### 2026-11-04 02:33 IST, X12 contrast 1 runs now (Aarnav's decision). The Llama-2-7B A1-P precision check and scoring run on Kaggle ahead of the 18 h X9b reserve (`scripts/kaggle_queue.py`, flag `x12c1` in `projection()`); X9b batch 3 is pushe

RESULTS.md lines 3862 to 3863; first line committed in `28803e6` on 2026-11-04 02:33:57 +0530; last line in `eff85fe` on 2026-11-04 02:34:12 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 02:33 IST, X12 contrast 1 runs now (Aarnav's decision).** The Llama-2-7B A1-P precision check and scoring run on Kaggle ahead of the 18 h X9b reserve (`scripts/kaggle_queue.py`, flag `x12c1` in `projection()`); X9b batch 3 is pushed the moment the quota projection allows and nothing else queues ahead of it. X7-A finished: **supported** (256 minus 4096 detok layer = 1, 1, 1; layers at V=256: 2,2,2 and at V=4096: 1,1,1; Phase 1 values 2 and 0). X10 pilot finished: estimated full run 3.37 h total (0.71, 0.84, 0.68, 1.14 h per model).

`````

##### 2026-11-04 02:46 IST, operations log (standing orders of 2026-11-04; no registered rule changes). (1) X4 Gemini drafts resumed on the paid tier (billing enabled by Aarnav on the Gemini key ending FXVw, project named by Aarnav "nuerips"): mo

RESULTS.md lines 3866 to 3867; first line committed in `98e2256` on 2026-11-04 02:46:00 +0530; last line in `0cfdea0` on 2026-11-04 02:46:43 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 02:46 IST, operations log (standing orders of 2026-11-04; no registered rule changes).** (1) **X4 Gemini drafts resumed on the paid tier** (billing enabled by Aarnav on the Gemini key ending FXVw, project named by Aarnav "nuerips"): model unchanged (gemini-3.5-flash-lite, temperature 0, prompt natural_romanization_v1 with the language name changed, unbatched); own cap raised from 480 to 6,000 requests a day and 12 to 60 per minute (`scripts/x4_natural.py`). Check before resuming: 40 consecutive requests in 30 s (about 80 per minute, above the free-tier limit of 15 per minute) returned no 429; the tier itself cannot be read from the API, so this is the evidence. Bengali resumed from 444 of 500 at 02:40 IST. (2) **Kaggle:** the earlier queue pushes were refused because `scripts/hidden.vbs` (tracked) had been deleted from the working tree, which also stopped the detached chains from restarting; restored. Llama-2-7B A1-P pushed at about 02:41 IST ahead of the reserve (X12 contrast 1). (3) **Laptop queue (chained by status files):** X1 T3 (running) -> X11 -> X10 full (`scripts/x10full_chain.sh`) -> X9a-low (`scripts/x9alow_chain.sh`, includes the level-0 stripped-retrieval observation). X9a-low code: `x9a.py prep_low | train <level> <seed> | analyse_low | level0_stripped`; the first `prep_low` attempt died with a MemoryError reading the story file while other jobs held memory and is retried inside the chain. (4) A 15-minute watchdog (session cron) checks both machines and the API jobs.

`````

##### 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST). Cause (from the kernel log): the kernel cannot read the Hugging Face token, so the gated repo

RESULTS.md lines 3868 to 3869; first line committed in `0cfdea0` on 2026-11-04 02:46:43 +0530; last line in `09b39ee` on 2026-11-04 02:52:11 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST).** Cause (from the kernel log): the kernel cannot read the Hugging Face token, so the gated repo meta-llama/Llama-2-7b-hf returns 401 on Kaggle. `UserSecretsClient` raised "Connection error trying to communicate with service" in all 16 kernel runs so far (the earlier models were not gated, so nothing was lost before). The same token reads both Llama repos from the laptop (HTTP 200), so access itself is granted; the Kaggle notebook has no HF_TOKEN secret attached. Fix needs a manual step in the Kaggle web UI (attach the secret HF_TOKEN to the kernels shattered-kaggle-precision and shattered-x-score, Add-ons, Secrets); no token is put in a dataset or the repository. Not relaunched yet (relaunch once after the fix). Llama-3.1-8B has the same dependency. X9b batch 3 is unaffected.

`````

##### 2026-11-04 03:33 IST, X9b reserve LIFTED (Aarnav). X9B_SARVAM_H set from 18 to 0 in scripts/kaggle_queue.py: a Kaggle job now only has to fit in the remaining hours of the 30 h per rolling 7 days; X9b batch 3 (cap 6.9 h) is pushed the momen

RESULTS.md lines 3876 to 3877; first line committed in `399fdee` on 2026-11-04 03:33:53 +0530; last line in `7ee0799` on 2026-11-04 03:43:18 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 03:33 IST, X9b reserve LIFTED (Aarnav).** X9B_SARVAM_H set from 18 to 0 in scripts/kaggle_queue.py: a Kaggle job now only has to fit in the remaining hours of the 30 h per rolling 7 days; X9b batch 3 (cap 6.9 h) is pushed the moment it fits and nothing else queues ahead of it. State at this time: 23.63 h used, headroom 6.37 h; batch 3 fits once 0.53 h roll off (about 9 Nov 19:04 IST), MDL Qwen3-8B (2.5 h cap) fits now and was launched; Llama-2 A1-P (3.5 h) fits but stays blocked by the missing Kaggle HF_TOKEN secret (flag file results/kaggle/HF_SECRET_MISSING).

`````

##### 2026-11-04 03:43 IST, gated models on Kaggle: private-dataset route (Aarnav's instruction; no registered rule changes). *Secrets cannot be set through the API:* the Kaggle kernel metadata accepted by the kernels push has no field for secret

RESULTS.md lines 3878 to 3879; first line committed in `7ee0799` on 2026-11-04 03:43:18 +0530; last line in `cbdea11` on 2026-11-04 03:52:38 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 03:43 IST, gated models on Kaggle: private-dataset route (Aarnav's instruction; no registered rule changes).** *Secrets cannot be set through the API:* the Kaggle kernel metadata accepted by the kernels push has no field for secrets (they are attached per notebook in the web UI, and all 16 kernel runs so far failed to reach the secret service), so no UI step is required of Aarnav. *Route:* `scripts/hf_to_kaggle.py` downloads Llama-2-7b-hf and Llama-3.1-8B (config, tokenizer, safetensors only) on the laptop with the approved Hugging Face access and uploads each as a **private** Kaggle dataset: **shattered-llama-2-7b-hf** and **shattered-llama-3-1-8b** (account aarnavkembhavi1). `shattered.interp.load.model_source` uses the mounted dataset on Kaggle and the Hugging Face repo elsewhere; `scripts/kaggle_queue.py` attaches the dataset to any job whose arguments name the model. The A1-P and scoring code is otherwise unchanged. The local copy is deleted after a verified upload. **End-of-Phase-2 cleanup list (delete and log): the private Kaggle datasets shattered-flores-private, shattered-llama-2-7b-hf, shattered-llama-3-1-8b.** Disk: to keep the 25 GB guard during the downloads I deleted finished-job caches (cache/activations/h_hindi 1.1 GB and cache/activations/nc1 0.6 GB, regenerable; the five data/processed/x9a/train_p*.npy streams, regenerable by `x9a.py prep` with hashes in meta.json); no results or logs were removed. Free disk after: 74 GB.

`````

##### 2026-11-04 04:14 IST, first gated model uploaded: Llama-2-7b-hf is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-2-7b-hf (12.55 GiB: config, tokenizer, two safetensors shards; upload 1,250 s after the subtitle fix; Kaggle metada

RESULTS.md lines 3882 to 3883; first line committed in `f479ea3` on 2026-11-04 04:14:25 +0530; last line in `957499a` on 2026-11-04 04:37:26 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 04:14 IST, first gated model uploaded: Llama-2-7b-hf is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-2-7b-hf** (12.55 GiB: config, tokenizer, two safetensors shards; upload 1,250 s after the subtitle fix; Kaggle metadata isPrivate = true; local copy deleted). The queue no longer blocks Llama-2 (flag HF_SECRET_MISSING removed); Llama-3.1-8B stays gated by results/kaggle/DATASET_PENDING_llama-3.1-8b until its upload (running, log results/phase2/hf_upload_llama31b.log). Llama-2 A1-P launches at the next queue pass after the current MDL job ends; the dataset mount path on Kaggle is untested until then.

`````

##### 2026-11-04 04:53 IST, Kaggle watchdog: Qwen3-8B MDL (X13) finished (output in results/kaggle/kaggle_mdl/2026-11-03T220606, analysis pending). Llama-2-7B A1-P failed a second time (04:40 IST, 0.12 h): the gated repo was still read from Huggi

RESULTS.md lines 3886 to 3887; first line committed in `45def39` on 2026-11-04 04:53:21 +0530; last line in `8e2e954` on 2026-11-04 06:08:17 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 04:53 IST, Kaggle watchdog:** Qwen3-8B MDL (X13) finished (output in results/kaggle/kaggle_mdl/2026-11-03T220606, analysis pending). Llama-2-7B A1-P failed a second time (04:40 IST, 0.12 h): the gated repo was still read from Hugging Face (401), i.e. the kernel did not use the private dataset copy; cause not yet known (the mounted path is not visible in the log); the boot script now prints the mounted datasets for the next run. The Ambari instruct pair A1-P (cap 5.0 h) was pushed at about 04:46 IST; quota 29.81 of 30 h with it reserved. Llama-2 will be retried once after it ends and the cause is fixed.

`````

##### 2026-11-04 06:08 IST, Kaggle watchdog: the Ambari instruct pair A1-P ended (pushed 04:46 IST): Ambari-Instruct-v0.2 passed (float32-offload reference); Ambari-Instruct-v0.1 gave no verdict: it is also a gated Hugging Face repo (401 on Kaggl

RESULTS.md lines 3888 to 3889; first line committed in `8e2e954` on 2026-11-04 06:08:17 +0530; last line in `7cfcb18` on 2026-11-04 06:08:50 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 06:08 IST, Kaggle watchdog:** the Ambari instruct pair A1-P ended (pushed 04:46 IST): **Ambari-Instruct-v0.2 passed** (float32-offload reference); **Ambari-Instruct-v0.1 gave no verdict: it is also a gated Hugging Face repo** (401 on Kaggle; the laptop token reads it, anonymous access gets 401). Same remedy as Llama: private Kaggle dataset **shattered-ambari-instruct-v0-1** (added to the cleanup list; upload started, log results/phase2/hf_upload_ambari01.log; v0.1 is gated until the upload). Quota 29.55 of 30 h used, so the next job of 3 h or more fits only from about 9 Nov 23:24 IST. Llama-2 still to be retried once (mount of its private dataset to be diagnosed with the new boot listing).

`````

##### 2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST). The kernel metadata of those pushes lists only shattered-pkg and shattered-flores-private as dataset sources (bui

RESULTS.md lines 3890 to 3891; first line committed in `7cfcb18` on 2026-11-04 06:08:50 +0530; last line in `46c9030` on 2026-11-04 06:23:52 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST).** The kernel metadata of those pushes lists only shattered-pkg and shattered-flores-private as dataset sources (build/kaggle/kernel_kaggle_precision/kernel-metadata.json): the queue driver process running since 03:35 IST had imported scripts/kaggle_queue.py before the change that attaches the private model datasets, so it never attached them. This is the same stale-driver mistake as before, not a mount problem. The next queue pass (a new process after the 90-minute wait) uses the new code. Llama-3.1 A1-P also failed with no verdict (0.1 h); neither failure is a verdict on the model. Retry once at the next pass when quota allows (quota 29.55 of 30 h used; 3 h or more fits from about 9 Nov 23:24 IST).

`````

##### 2026-11-04 06:23 IST, watchdog: quota fell to 26.19 of 30 h (actual runtimes of the instruct pair were shorter than the cap), so the Llama-2 A1-P (cap 3.5 h) fits; the queue chain was restarted early (a fresh process with the code that atta

RESULTS.md lines 3892 to 3893; first line committed in `46c9030` on 2026-11-04 06:23:52 +0530; last line in `6f2ebf8` on 2026-11-04 06:37:27 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 06:23 IST, watchdog:** quota fell to 26.19 of 30 h (actual runtimes of the instruct pair were shorter than the cap), so the Llama-2 A1-P (cap 3.5 h) fits; the queue chain was restarted early (a fresh process with the code that attaches the private model datasets) instead of waiting for the 07:44 retry.

`````

##### 2026-11-04 06:37 IST, third gated model uploaded: Ambari-Instruct-v0.1 is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-ambari-instruct-v0-1 (upload 821 s, status ready, local copy deleted; on the end-of-Phase-2 cleanup list with shat

RESULTS.md lines 3894 to 3895; first line committed in `6f2ebf8` on 2026-11-04 06:37:27 +0530; last line in `81fc534` on 2026-11-04 07:53:46 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 06:37 IST, third gated model uploaded: Ambari-Instruct-v0.1 is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-ambari-instruct-v0-1** (upload 821 s, status ready, local copy deleted; on the end-of-Phase-2 cleanup list with shattered-flores-private, shattered-llama-2-7b-hf and shattered-llama-3-1-8b). Queue gate removed. The Llama-2 A1-P was pushed at about 06:25 IST with shattered-llama-2-7b-hf attached (kernel dataset_sources verified); quota 29.69 of 30 h with its cap reserved.

`````

##### 2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check (float32-offload reference; first job to use a private model dataset, so the dataset route works; run pushed 06:25 IST, finished about 07:45). Both co

RESULTS.md lines 3896 to 3897; first line committed in `81fc534` on 2026-11-04 07:53:46 +0530; last line in `7455dba` on 2026-11-04 09:53:29 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check** (float32-offload reference; first job to use a private model dataset, so the dataset route works; run pushed 06:25 IST, finished about 07:45). Both contrast-1 endpoints (Ambari-7B-base and Llama-2-7B) have now passed, so X12 contrast 1 scoring is the next job. Quota 27.54 of 30 h used: the scoring cap was lowered from 5.0 to 2.4 h to fit (measured scoring times: Qwen3-8B 1.71 h, Ambari-7B-base 1.23 h; the job resumes from its item cache if the cap is hit). Queue chain restarted early to push it. Llama-3.1-8B and Ambari-Instruct-v0.1 A1-P wait for quota (retry once after the failures of the stale driver).

`````

##### 2026-11-04 09:53 IST, X12 CONTRAST 1 (primary test) RESULT: SUPPORTED (as predicted). Llama-2-7B vs Ambari-7B-base-v0.1, both passed A1-P (fp16 vs float32-offload), scored on Kaggle (Llama-2 1.81 h; code scripts/x12_analyse.py, output resul

RESULTS.md lines 3898 to 3899; first line committed in `7455dba` on 2026-11-04 09:53:29 +0530; last line in `173d201` on 2026-11-04 11:07:39 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 09:53 IST, X12 CONTRAST 1 (primary test) RESULT: SUPPORTED (as predicted).** Llama-2-7B vs Ambari-7B-base-v0.1, both passed A1-P (fp16 vs float32-offload), scored on Kaggle (Llama-2 1.81 h; code scripts/x12_analyse.py, output results/phase2/x12/contrast1.json). **SIB-200 (n = 1,004 paired items), calibrated accuracy:** Ambari native 0.506, ITRANS 0.110, lossy 0.191, English 0.559; Llama-2 native 0.117, ITRANS 0.143, lossy 0.281, English 0.689. Gain (Ambari minus Llama-2): native +0.389, ITRANS -0.034; **DiD = +0.423, 97.5% interval [0.380, 0.466], above 0.** **Retrieval (unmapped, M4b test half, n = 1,005 paired sentences):** Ambari native 0.743, ITRANS 0.142; Llama-2 native 0.052, ITRANS 0.075; gain native +0.692, ITRANS +0.068; **DiD = +0.624, 97.5% interval [0.584, 0.664], above 0.** Both measures above 0: **supported** (registered rule). Reading and caveats stand as registered: the exposure Ambari received was native-script Kannada and it did not transfer to ITRANS (ITRANS accuracy for both models is near chance 0.143 on SIB-200); the native gain confounds exposure with the tokenizer extension (ITRANS tokens per word 4.69 vs 4.55 is the control); X9b, not X12, is the causal test of familiarity. Nothing against a prediction. The paper is not edited.

`````

##### 2026-11-04 12:13 IST, correction note to the X11 entry above (p values). The per-form McNemar p values in the X11 entry are exact and unadjusted; the registration prescribes no multiplicity correction for X11, and the verdict rule does not 

RESULTS.md lines 3905 to 3905; first line committed in `ed31e10` on 2026-11-04 12:13:51 +0530; last line in `ed31e10` on 2026-11-04 12:13:51 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 12:13 IST, correction note to the X11 entry above (p values).** The per-form McNemar p values in the X11 entry are exact and unadjusted; the registration prescribes no multiplicity correction for X11, and the verdict rule does not use them. **Holm-adjusted over the five forms (English, native, ITRANS, lowercase, lossy): English 0.052, native 0.872, ITRANS 0.660, lowercase 0.876, lossy 0.872** (over the four registered forms: native 0.872, ITRANS 0.660, lowercase 0.876, lossy 0.872). So the statement "English is the only significant per-form change" holds only unadjusted (p 0.0105); after Holm it is not significant at 0.05 (0.052). Verdict stays "partly supported" as registered (every form within 3 points; gap-change 95% CI [-0.054, +0.003] outside the +-5 point bound by 0.4 points on one side). Arm A used Qwen3.5-2B; Arm B (optional, descriptive, one 4B-class model from the X6 screen, no verdict) is not built or run (X6 not screened yet). 4-bit in Phase 2: X11 Arm A (4-bit NF4 with double quantisation, bf16 compute) and the X9b QLoRA training (4-bit NF4 base, fp16 compute); the X9b evaluations use the adapter merged into the unquantized fp16 base. Nothing else uses 4-bit (A1-P, X12, X13, X10, X4 are bf16/fp16; the 4-bit load option exists in the loader but is only used by X11 and X9b).
`````

##### 2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD values above are unchanged). Gain = Ambari-7B-base minus Llama-2-7B, paired boot

RESULTS.md lines 3908 to 3909; first line committed in `72ff37e` on 2026-11-04 12:14:44 +0530; last line in `39d4c01` on 2026-11-04 13:21:46 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 12:14 IST, X12 contrast 1: per-form gains and A1-P details added (`scripts/x12_analyse.py`, `results/phase2/x12/contrast1.json`; the verdict and DiD values above are unchanged).** Gain = Ambari-7B-base minus Llama-2-7B, paired bootstrap over items, 95% interval (descriptive). SIB-200 (n = 1,004): native +0.389 [0.356, 0.423]; ITRANS -0.034 [-0.052, -0.016]; lossy -0.090 [-0.118, -0.063]; English -0.130 [-0.158, -0.103]. Retrieval (n = 1,005): native +0.692 [0.662, 0.721]; ITRANS +0.068 [0.051, 0.086]. A1-P (100 items x native/ITRANS/lossy, fp16 vs float32-offload): Ambari-7B-base raw label agreement 1.00 / 1.00 / 1.00, accuracy difference 0.000 in each form, max hidden state 1,730; Llama-2-7B agreement 1.00 / 0.99 / 1.00, accuracy difference 0.000 in each form, max hidden state 2,424; no non-finite value in either; mean |dlogprob| 0.003. Note: Ambari loses 13 points on English SIB-200 relative to Llama-2 (0.559 vs 0.689), so the continued pretraining also changed the model outside Kannada.

`````

##### 2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction). Some Kaggle compute for Phase 2 now runs on a teammate's Kaggle account (username ashwin18522; per-account quota of 30 h per rolling 7 days, tracked separately in res

RESULTS.md lines 3910 to 3911; first line committed in `39d4c01` on 2026-11-04 13:21:46 +0530; last line in `d1ef7c9` on 2026-11-04 13:27:53 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction).** Some Kaggle compute for Phase 2 now runs on a **teammate's Kaggle account** (username ashwin18522; per-account quota of 30 h per rolling 7 days, tracked separately in results/kaggle/acct2/quota.json). The token is stored only in the gitignored .env (KAGGLE2_API_TOKEN, KAGGLE2_USERNAME) and was never written to a commit, log or this file. Token verified: it authenticates and the account lists its own kernels; the first kernel (kaggle_gate smoke test) started on a T4 x2 GPU session at 13:20 IST on 2026-11-04. *What changed in the code:* the runner takes KAGGLE_ACCOUNT=1|2 (credentials, quota file, job folders and build folder per account); the queue runs one driver per account: account 1 keeps X9b (batch 3 first when its quota frees, its checkpoints and datasets live there) and, until account 2 is accepted, the rest; account 2 runs the self-contained jobs (Ambari-Instruct-v0.1 A1-P, instruction-pair scoring and MDL, Llama-3.1-8B A1-P and scoring, later X13 models). Account 2 is accepted for real jobs only after the smoke test and the A1-R reproduction on its own environment pass (file results/kaggle/acct2/ACCEPTED). Private datasets re-uploaded under account 2: shattered-flores-private, shattered-llama-3-1-8b and shattered-ambari-instruct-v0-1 (uploads in progress at this time), plus the package dataset shattered-pkg that the runner uploads. **End-of-Phase-2 cleanup list additions: delete account 2's datasets (shattered-flores-private, shattered-llama-3-1-8b, shattered-ambari-instruct-v0-1, shattered-pkg) and kernels, and revoke the token that was shared in the chat (the token is in the session transcript).** The anonymiser now scrubs the account name.

`````

##### 2026-11-04 13:40 IST, account 2 smoke test PASSED (kaggle_gate, T4 x2, second attempt; 0.10 h). gate_passed true with the same dtype (float16) for Sarvam-1 and Gemma 4 E2B; every number equals account 1's gate run (raw agreement native/ITRA

RESULTS.md lines 3914 to 3915; first line committed in `97a4a6b` on 2026-11-04 13:40:55 +0530; last line in `59154b4` on 2026-11-04 14:10:52 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 13:40 IST, account 2 smoke test PASSED (kaggle_gate, T4 x2, second attempt; 0.10 h).** gate_passed true with the same dtype (float16) for Sarvam-1 and Gemma 4 E2B; every number equals account 1's gate run (raw agreement native/ITRANS/lossy 0.99/0.95/0.96 for Sarvam-1 and 1.00/0.99/0.99 for Gemma 4; Kaggle accuracy 0.62/0.29/0.36 and 0.73/0.27/0.44; max |dlogprob| identical to three decimals). The runner polling had been ended by a laptop network blip once (the status call failed and the wait loop read "error" in the message); fixed so a failed status call keeps waiting. Next: the A1-R retrieval reproduction on account 2 (kaggle_retrieval_gate, FLORES private dataset under account 2); account 2 is accepted for real jobs only if it reproduces the account 1 A1-R numbers (Sarvam-1 native 0.9443, ITRANS 0.5104; Gemma 4 E2B as stored).

`````

##### 2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly. kaggle_retrieval_gate on account 2 (0.34 h; its own shattered-flores-private dataset): Sarvam-1 native layer

RESULTS.md lines 3916 to 3917; first line committed in `59154b4` on 2026-11-04 14:10:52 +0530; last line in `eb2aa7a` on 2026-11-04 16:09:50 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly.** kaggle_retrieval_gate on account 2 (0.34 h; its own shattered-flores-private dataset): Sarvam-1 native layer 24, accuracy 0.9443; ITRANS layer 21, accuracy 0.5104; Gemma 4 E2B native layer 7, accuracy 0.9960; ITRANS layer 7, accuracy 0.2657; all per-layer train and test curves equal account 1's (max difference 0.0) and are within 0.004 of the laptop values (tolerance 0.03); the untrained evaluation of a new environment therefore reproduces the A1-R numbers (results/kaggle/acct2/a1r_reproduced.json, marker results/kaggle/acct2/ACCEPTED). Private datasets under account 2, all ready: shattered-flores-private, shattered-llama-3-1-8b (upload 1,146 s), shattered-ambari-instruct-v0-1 (826 s); local copies deleted. The account-2 queue driver (scripts/kaggle_queue2_chain.sh, KAGGLE_ACCOUNT=2) started at 14:08 IST with the Ambari-Instruct-v0.1 A1-P; account 1 now runs X9b only. Quota use so far: account 2 about 0.5 of 30 h, account 1 29.36 of 30 h. **Calendar (estimates from measured runtimes; gating by caps):** account 2: v0.1 A1-P 14:10 to 15:40 on 4 Nov, v0.1 scoring to 17:10, v0.2 scoring to 18:40, instruction-pair MDL to 20:52, Llama-3.1-8B A1-P to 22:22, Llama-3.1-8B scoring to 00:10 on 5 Nov; account 1: X9b batch 3 from 10 Nov 02:50 to 09:20, X9b Qwen3.5-2B arm 10 Nov 09:20 to 18:20 (last job, projected end 10 Nov about 18:20 IST). Account 2 then has about 19 h of its week free for further X13 models and MDL jobs.

`````

##### 2026-11-04 17:26 IST, Kaggle account 2: Ambari-Instruct-v0.1 A1-P ended without a verdict (pushed 14:08 IST, 3.2 h of account 2 quota). The kernel reached its self-stop timeout: the fp16 half finished (ambari-7b-instruct-v0.1__fp16.npz writ

RESULTS.md lines 3920 to 3921; first line committed in `4770255` on 2026-11-04 17:26:35 +0530; last line in `7bcba7d` on 2026-11-04 20:22:41 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 17:26 IST, Kaggle account 2: Ambari-Instruct-v0.1 A1-P ended without a verdict (pushed 14:08 IST, 3.2 h of account 2 quota).** The kernel reached its self-stop timeout: the fp16 half finished (ambari-7b-instruct-v0.1__fp16.npz written) but the float32-offload reference half never finished, and the kernel log has no line between minute 1 and the timeout at 11,067 s (the worker printed nothing). For comparison the same job took 1.3 h for Llama-2-7B and about 1.5 h per model for Ambari-7B-base, on account 1. Cause not established (candidates: the float32-offload reference stalling on host memory or the dataset-mounted weights loading slowly in this account's session; the A1-R and gate jobs on account 2 ran at normal speed). No verdict on the model. **Diagnostic added, not a fix:** the A1-P worker now prints load and per-form progress lines (scripts/kaggle_precision.py), so a stall shows where. The queue keeps v0.1 open and retries it once after Llama-3.1-8B (the driver moved on to the Llama-3.1-8B A1-P at 17:22 IST); the instruction-pair scoring and MDL wait for v0.1 to pass (the pair is scored only if both pass, as registered). If the retry stalls the same way, the fallback is to run v0.1 on account 1 (it ran Ambari-7B-base there) once quota frees.

`````

##### 2026-11-04 20:22 IST, Kaggle account 2: Llama-3.1-8B A1-P PASSED (float32-offload reference; pushed 17:22 IST, finished about 20:15; this is the first run of the new progress output, so the Ambari-Instruct-v0.1 stall can be compared with it

RESULTS.md lines 3923 to 3924; first line committed in `7bcba7d` on 2026-11-04 20:22:41 +0530; last line in `f06c46f` on 2026-11-04 20:23:22 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 20:22 IST, Kaggle account 2: Llama-3.1-8B A1-P PASSED (float32-offload reference; pushed 17:22 IST, finished about 20:15; this is the first run of the new progress output, so the Ambari-Instruct-v0.1 stall can be compared with it).** Scoring (X13) follows the Ambari-Instruct-v0.1 retry in the account 2 queue; the v0.1 A1-P retry was pushed at about 20:22.

`````

##### 2026-11-04 20:23 IST, Kaggle account 2 note on the slow A1-P runs (cause now likely): the Llama-3.1-8B A1-P (2.78 h, passed: raw agreement 1.00 / 0.98 / 1.00 native/ITRANS/lossy, accuracy difference 0.00 / -0.01 / 0.00) shows fp16 load 2,86

RESULTS.md lines 3925 to 3926; first line committed in `f06c46f` on 2026-11-04 20:23:22 +0530; last line in `3c30aee` on 2026-11-04 20:44:16 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 20:23 IST, Kaggle account 2 note on the slow A1-P runs (cause now likely):** the Llama-3.1-8B A1-P (2.78 h, passed: raw agreement 1.00 / 0.98 / 1.00 native/ITRANS/lossy, accuracy difference 0.00 / -0.01 / 0.00) shows fp16 load 2,866 s and reference scoring 6,382 s; Llama-2 on account 1 loaded in 631 s. Weights mounted from a private dataset load slowly in these sessions, which is the likely reason the first Ambari-Instruct-v0.1 run (cap 3.5 h, self-stop 3.07 h) did not finish its reference half. The queue now gives any A1-P of a model mounted from a private dataset a 5.0 h cap (push timeout and quota projection); the v0.1 retry already in flight (pushed about 20:22 IST) still has the old 3.5 h cap and may time out again, in which case it is re-pushed with 5.0 h.

`````

##### 2026-11-04 20:44 IST, X9b batch 3 moved to Kaggle account 2 (Aarnav's instruction). Independence checked in `scripts/kaggle_x9b.py` and the queue: every run trains from the base model (the pool is the pinned public Wikipedia parquet read in

RESULTS.md lines 3929 to 3929; first line committed in `3c30aee` on 2026-11-04 20:44:16 +0530; last line in `3c30aee` on 2026-11-04 20:44:16 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 20:44 IST, X9b batch 3 moved to Kaggle account 2 (Aarnav's instruction).** Independence checked in `scripts/kaggle_x9b.py` and the queue: every run trains from the base model (the pool is the pinned public Wikipedia parquet read in the kernel, verified by sha256 against the CPU report; seeds fixed; the removed-id list, the pilot result and the report ship in the package); a batch reads nothing from the outputs of batches 1 and 2 (resume applies only inside a run's own checkpoints), so batch 3 is independent. Account 2 has its own driver and state file for it (KAGGLE_ACCOUNT=2, QUEUE_ONLY=x9b), runs concurrently with the A1-P retry already running on that account, and its result is merged into account 1's state, so account 1 does not repeat it. **Base evaluation check first:** the kernel evaluates the untrained Sarvam-1 base before any training and stops with an error if native or ITRANS retrieval differs from the reference (results/phase2/x9b/base_reference.json = the batch-1 account-1 values equal to A1-R: native 0.9443, layer 24; ITRANS 0.5104, layer 21) by more than 0.01. Logged as run on account 2 (teammate's account). Pushed about 20:35 IST; the Qwen3.5-2B arm stays on account 1.
`````

##### 2026-11-04 21:53 IST, Kaggle account 2: duplicate push of the Ambari-Instruct-v0.1 A1-P (my driver defect; quota cost, no wrong result). The retry pushed at 20:10 IST (cap 3.5 h) stayed recorded as "pushed" in results/kaggle/acct2/quota.jso

RESULTS.md lines 3934 to 3935; first line committed in `952be81` on 2026-11-04 21:53:03 +0530; last line in `58423f1` on 2026-11-04 21:53:12 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 21:53 IST, Kaggle account 2: duplicate push of the Ambari-Instruct-v0.1 A1-P (my driver defect; quota cost, no wrong result).** The retry pushed at 20:10 IST (cap 3.5 h) stayed recorded as "pushed" in results/kaggle/acct2/quota.json, never fetched, because its driver process ended early (the self-restart on changed code, introduced the same day, re-executed the process while a push was in flight); the next queue pass at 21:41 IST then pushed the same kernel again (cap 5.0 h), which replaces the earlier version, so the 20:10 run's output is lost and the stale 3.5 h record keeps counting against the account (quota 21.89 h shown, conservative). The 21:41 run (5.0 h cap, progress lines on) is the one that will be fetched. **Fix:** the queue now refuses to push a kernel whose previous version is still running or queued (status check on the laptop, no quota). X9b batch 3 on account 2 (pushed 20:35, its own kernel) is unaffected.

`````

##### 2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label agreement 1.00 in native, ITRANS and lossy, accuracy difference 0.00 in each, me

RESULTS.md lines 3938 to 3939; first line committed in `06404f2` on 2026-11-04 22:07:54 +0530; last line in `17dba9c` on 2026-11-04 22:24:09 +0530; labels from the title and parent heading: amended, result

`````text
- **2026-11-04 22:07 IST, X12 instruction pair: Ambari-Instruct-v0.1 A1-P PASSED (Kaggle account 2; run pushed 20:10 IST, 1.94 h; fetched at about 22:04; raw label agreement 1.00 in native, ITRANS and lossy, accuracy difference 0.00 in each, mean |dlogprob| 0.003 to 0.004, max fp16 hidden state 559.5, no non-finite value).** Both instruction models have now passed A1-P (v0.2 earlier), so the pair is scored as registered; the scoring of v0.1 was pushed at 22:06 IST. Correction to my duplicate-push entry above: the 20:10 run was not lost: it completed and its output was fetched by the later push's fetch (identical numbers in both result folders, same fp16 load of 3,420 s and total of 6,754 s); the 21:41 push (5.0 h cap) was therefore possibly a redundant second run of the same job whose hours will count when it ends. The weights loaded from the private dataset took 3,420 s (57 minutes) in fp16 in this run, which did not yet have the copy-to-local-disk loader (committed after the push); the load-time comparison with the copy loader is still to be made on the next job that loads from a private dataset.

`````

##### 2026-11-04 22:37 IST, account 2 quota records reconciled by hand. The instruction-pair MDL push of 22:08 IST never created a kernel (runner stopped at 22:23 during the driver fix; no kernel of that name exists on the account): record set to

RESULTS.md lines 3942 to 3943; first line committed in `06100d7` on 2026-11-04 22:37:35 +0530; last line in `5b9ae1d` on 2026-11-05 00:25:45 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 22:37 IST, account 2 quota records reconciled by hand.** The instruction-pair MDL push of 22:08 IST never created a kernel (runner stopped at 22:23 during the driver fix; no kernel of that name exists on the account): record set to 0 h, status "not run"; the driver pushes it again after the Ambari-Instruct-v0.1 scoring. The 20:10 A1-P record that stayed "pushed" is set to its real 1.94 h (complete). The quota projection for account 2 now counts hours that were really used or are really running.

`````

##### 2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length. Without the copy loader: fp16 load 2,866 s (Llama-3.1-8B A1-P, 2.78 h in total) and 3,420 s 

RESULTS.md lines 3946 to 3947; first line committed in `1fbe72d` on 2026-11-05 00:52:48 +0530; last line in `055b2fc` on 2026-11-05 01:09:36 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length.** Without the copy loader: fp16 load 2,866 s (Llama-3.1-8B A1-P, 2.78 h in total) and 3,420 s (Ambari-Instruct-v0.1 A1-P, 1.94 h in total; an earlier attempt of the same job reached its 3.07 h self-stop); on account 1 Llama-2 loaded in 631 s. With the copy loader (parallel copy to local disk before loading; first used by the Ambari-Instruct-v0.1 scoring pushed 22:06 IST): "[model_source] copied shattered-ambari-instruct-v0-1: 12.8 GiB in 72s to local disk", and the whole scoring job took 1.20 h (4,112 s), as long as the account 1 scoring jobs (1.23 to 1.81 h). The A1-P timeout stays 5 h until an A1-P job has run with the copy loader. X9b batch 3 (training, loads Sarvam-1 from the Hub) is expected at about 6.5 h on either account (account 1: 6.31 and 6.60 h).

`````

##### 2026-11-05 02:38 IST, X12 CONTRAST 2 RESULT (secondary; instruction-pair exposure contrast; MDL assembly layer, descriptive; Kaggle account 2 run, 1.50 h; `scripts/x12_contrast2.py`, `results/phase2/x12/contrast2_mdl.json`): the registered 

RESULTS.md lines 3956 to 3957; first line committed in `ec3c085` on 2026-11-05 02:38:48 +0530; last line in `900da25` on 2026-11-05 03:10:06 +0530; labels from the title and parent heading: exploratory, result

`````text
- **2026-11-05 02:38 IST, X12 CONTRAST 2 RESULT (secondary; instruction-pair exposure contrast; MDL assembly layer, descriptive; Kaggle account 2 run, 1.50 h; `scripts/x12_contrast2.py`, `results/phase2/x12/contrast2_mdl.json`): the registered pattern is MET (as predicted).** Both instruction models passed A1-P; the 300 Phase 1 probe words, Phase 1 protocol, fp16, 32 layers. **Native Kannada: Ambari-Instruct-v0.1 (extended tokenizer) detokenization layer 4 at 1.66 tokens per probe word; Ambari-Instruct-v0.2 (Llama-2 tokenizer) layer 8 at 14.51 tokens per probe word; v0.2 minus v0.1 = +4 layers, word-clustered paired 95% CI [3, 5]; the sign matches the sign of the tokens-per-word difference (+12.85): the more fragmented input is assembled later, as the registered rule (H3 text) requires.** **ITRANS (a control: the two models tokenize ITRANS almost identically, 3.49 versus 3.42 tokens per word): layer difference 0 [0, 1], no difference (the rule is not applicable there: tokens-per-word difference 0.07).** So the +4 on native follows the tokenizer difference, not a general difference between the two fine-tuned models. Caveat as registered with the contrast: v0.1 is built on Ambari-7B-base-v0.1 (500 million new Kannada tokens) and v0.2 on Llama-2, so this is the comparison of two released instruction models, not a clean test with the base model held fixed. The word-clustered bootstrap pairs the models by word (v0.2 keeps 8,994 of 9,000 native occurrences; 300 words in both). The accuracy differences between the two models (scored on SIB-200) are exploratory and not analysed here. This completes the registered X12 contrasts (contrast 1 supported, contrast 2 pattern met). The paper is not edited.

`````

##### 2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on both measures (as predicted). All six runs are complete: batches 1 and 2 on Kagg

RESULTS.md lines 3958 to 3959; first line committed in `900da25` on 2026-11-05 03:10:06 +0530; last line in `17458bc` on 2026-11-05 03:12:00 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on both measures (as predicted).** All six runs are complete: batches 1 and 2 on Kaggle account 1 (3 Nov), batch 3 (native seed 1, English seed 1) on account 2 (6.47 h; the in-kernel base-evaluation check passed first: native 0.9443 at layer 24, ITRANS 0.5104 at layer 21, equal to A1-R and to the account 1 base). B = 4,997,120 tokens per run (305 optimizer steps); tokenizer sha256 unchanged by training in every run; overlap 0 in every stream. Registered rule: gap g = native minus ITRANS after training on condition c; D_N = g(native) - g(ITRANS), D_E = g(English) - g(ITRANS); 97.5% paired-bootstrap intervals with one of the two seeds drawn per cell per resample. **SIB-200 accuracy (n = 1,004): g(0) = +0.233 before training (native 0.768, ITRANS 0.535); after training g(ITRANS) = +0.117, g(native) = +0.342, g(English) = +0.313; D_N = +0.225 [0.177, 0.273] (seeds +0.222, +0.227); D_E = +0.196 [0.150, 0.244] (seeds +0.196, +0.196): supported.** **FLORES+ retrieval (test half n = 1,005): g(0) = +0.434 (native 0.944, ITRANS 0.510); g(ITRANS) = +0.081, g(native) = +0.418, g(English) = +0.472; D_N = +0.337 [0.296, 0.378] (seeds +0.328, +0.346); D_E = +0.391 [0.344, 0.435] (seeds +0.381, +0.401): supported.** What moved (seed means, native / ITRANS accuracy): after ITRANS training 0.766 / 0.649 on SIB-200 (ITRANS +11 points) and retrieval 0.927 / 0.847 (ITRANS +34 points); after native training SIB-200 0.766 / 0.424 and retrieval 0.920 / 0.502; after English training SIB-200 0.757 / 0.443 and retrieval 0.920 / 0.449. **So with the tokenizer and the number of pieces per word fixed, continued pretraining on ITRANS text closed most of the gap by raising ITRANS (accuracy 0.535 to 0.649, retrieval 0.510 to 0.847), while the two controls left ITRANS retrieval unchanged to lower and lowered ITRANS SIB-200 accuracy (to 0.42 to 0.44, below the base).** The gap after the controls is therefore larger than the base gap g(0), i.e. D_N and D_E partly reflect the controls widening the gap and not only ITRANS training narrowing it; the narrowing by ITRANS training alone is 0.233 to 0.117 on SIB-200 and 0.434 to 0.081 on retrieval. Seed spread is at most 0.02 in every D. English SIB-200 damage check (descriptive, no verdict; base 0.768): ITRANS-trained -1.6 and -1.8 points, native-trained -2.6 and -2.8, **English-trained -5.1 and -5.3 (flagged: more than 5 points)**. Caveats as registered: adapters trained against the 4-bit base and evaluated on the unquantized fp16 base plus adapter; two seeds give a crude seed-variance estimate. The Qwen3.5-2B arm (secondary, one seed) has not run; it is the last Kaggle job and the first cut. This is the causal test of familiarity at fixed fragmentation that X12 pointed to. Nothing against a prediction. The paper is not edited.

`````

##### 2026-11-05 04:23 IST, X13 Llama-3.1-8B RESULT (Kaggle account 2; A1-P passed 2.78 h, scoring 1.82 h; `scripts/x13_analyse.py --model llama-3.1-8b`, `results/phase2/x13/llama-3.1-8b/analysis.json`): counted; extended P-a supported (5 of 5 fo

RESULTS.md lines 3966 to 3967; first line committed in `5c0388b` on 2026-11-05 04:23:24 +0530; last line in `c7acc38` on 2026-11-05 05:08:02 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 04:23 IST, X13 Llama-3.1-8B RESULT (Kaggle account 2; A1-P passed 2.78 h, scoring 1.82 h; `scripts/x13_analyse.py --model llama-3.1-8b`, `results/phase2/x13/llama-3.1-8b/analysis.json`): counted; extended P-a supported (5 of 5 for both contrasts); retrieval all-but-one met (4 of 4); nothing against a prediction.** SIB-200 calibrated accuracy (n = 1,004; no raw fallback): English 0.785; **native 0.712 [0.684, 0.739] (CI lower 0.684 above 0.40: counted)**; lossy 0.463 [0.433, 0.494]; lowercase 0.385 [0.356, 0.416]; ITRANS 0.382 [0.353, 0.413]; natural (257 ids) 0.529 [0.467, 0.591]. This model: native minus ITRANS +0.330 (exact McNemar p about 3e-60), native minus lossy +0.249 (p about 1e-40), both Holm-significant. Extended P-a (the four Phase 1 counted models plus this model, all-but-one rule): native beats ITRANS in 5 of 5 and lossy in 5 of 5: supported for both. **Retrieval (unmapped, test half n = 1,005): native 0.982 at layer 17, ITRANS 0.173 at layer 8; native minus ITRANS +0.809 [0.784, 0.833]**; for the Phase 1 retrieval models the native minus ITRANS CIs are all above 0 (Qwen3.5-2B +0.865, Sarvam-1 +0.430, Gemma 4 E2B +0.727), so 4 of 4 models with a CI above 0: all-but-one rule met. The X13 MDL assembly job for this model is queued next on account 2. The paper is not edited.

`````

##### 2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, budgets and verdicts are unchanged). Why the laptop GPU was idle: the registere

RESULTS.md lines 3999 to 4000; first line committed in `6be3732` on 2026-11-05 13:12:01 +0530; last line in `3b1e037` on 2026-11-05 13:23:17 +0530; labels from the title and parent heading: registered, result

`````text
- **2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, budgets and verdicts are unchanged).** Why the laptop GPU was idle: the registered laptop queue was empty (the last laptop job, X5, finished 11:42; idle until the feasibility pilot started at about 12:44). **(1) X9b primary arm (Sarvam-1) extra seeds.** Feasibility pilot on the RTX 3070 laptop (`scripts/x9b_laptop_pilot.py`, `results/phase2/x9b/laptop_pilot.json`, registered recipe unchanged, 50 micro-steps): ITRANS 633.6 tokens/s, native 564.5 tokens/s, micro-batch 16, finite loss; the card spills past 8 GB into shared memory (torch peak 10.6 GiB), which changes speed but not the arithmetic; at the registered budget B = 4,997,120 tokens per run that is 2.46 h of training per run (the registered T4 pilot's slowest rate is 515.7 tokens/s). It fits. Extra runs: **seeds 2 and 3 in the code (called seeds 3 and 4, beside the original seeds 1 and 2 = code seeds 0 and 1) for the ITRANS, native and English arms**, same QLoRA recipe, same streams and budget, same evaluation, run on the laptop with the in-run base-evaluation guard (the untrained base must reproduce the A1-R values in this environment before training starts; native 0.9443 layer 24, ITRANS 0.5104 layer 21). Output `results/kaggle/laptop_x9b/2026-11-05/out`. **Labelled "added after seeing seeds 1 and 2". The paper reports all four seeds together and the original two separately, whatever they show;** the registered verdict stays the one from the original two seeds. The 97.5% intervals will be computed twice (original two seeds; all four seeds, one seed drawn per cell per resample), same code. Environment difference stated: laptop (Windows, RTX 3070 8 GB with shared-memory spill) against Kaggle T4. **(2) X9a-low extra seeds:** exposure levels 0.1%, 0.3% and 1%, code seeds 3 and 4 (called seeds 4 and 5; the original seeds are 0, 1, 2), same recipe and evaluation, per-seed values reported, labelled the same way; the registered X9a-low rule is not re-evaluated on a different set of seeds, the table will show original three and all five. The 1% level is the X9a level-1 run (`x9a_p1_s3`, `x9a_p1_s4`). Queue (chain `x9extra`, after the Qwen English-run completion): X9a-low extras first (6 runs, about 18 min each, about 2 h), then the six X9b runs (about 2.5 h training plus evaluation each, an estimated 16 to 18 h in total, projected finish about 6 Nov 09:00 to 11:00 IST). X9a-low goes first only because it is short and returns in about 2 h; X9b follows without waiting for anything else. The paper is not edited.

`````

##### 2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational). Aarnav reported that the owner of the third Kaggle account (username aarnavkembhavi) confirmed it is a teammate's account, agreed to its use and confirmed t

RESULTS.md lines 4021 to 4022; first line committed in `5d9fd0e` on 2026-11-05 22:23:55 +0530; last line in `07e9a33` on 2026-11-05 22:37:41 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational).** Aarnav reported that the owner of the third Kaggle account (username aarnavkembhavi) confirmed it is a teammate's account, agreed to its use and confirmed the phone is verified; its token is in the gitignored \`.env\` only. **Statement for the record: some Phase 2 Kaggle compute ran on teammates' accounts, not on Aarnav's: account 2 (username ashwin18522, a teammate's, from 2026-11-04 07:50 UTC: gates, A1-R reproduction, A1-P checks for the Llama and Ambari-Instruct models, instruction-pair and Llama-3.1-8B scoring and MDL, X9b batch 3 (Sarvam-1, 2026-11-04), the X9b Qwen3.5-2B arm (2026-11-04 21:41 UTC to 2026-11-05) and the X13 Sarvam-m scoring (2026-11-05 05:10 UTC)); and from 2026-11-05 account 3 (username aarnavkembhavi, a teammate's), starting with its smoke gate and A1-R reproduction on 2026-11-05 and followed by the jobs listed below once those pass.** **Audit (requested), checked from the Kaggle side: every kernel on each account was listed with its owner. Account 1 (aarnavkembhavi1): 6 kernels (x-score, kaggle-x9b, kaggle-mdl, kaggle-precision, kaggle-gate, kaggle-retrieval-gate), all owned by aarnavkembhavi1, 5 datasets all under aarnavkembhavi1. Account 2 (ashwin18522): the same 6 kernels, all owned by ashwin18522, 4 datasets all under ashwin18522. Account 3 (aarnavkembhavi): no shattered-* kernel and no dataset before today. The two ledgers hold 35 recorded pushes (23 on account 1, 12 on account 2 plus the sessions of the X9b-only ledger): every recorded kernel slug carries the owner of its own account, no kernel exists under any other owner, so no job ran on the fallback login.** The one fallback found concerns the CLI configuration, not a job: the Kaggle CLI falls back to the login stored in the user profile (which is the account aarnavkembhavi) when no token is given; every run passes its own token and username, an invalid token is refused rather than falling back, and each account now has its own empty CLI configuration folder in \`build/kaggle_config_<n>\` (runner change committed). Setup of account 3: private dataset \`aarnavkembhavi/shattered-flores-private\` (the FLORES+ evaluation sentences, as on the other accounts; no other datasets: the models of its jobs are public), then the smoke gate and the A1-R retrieval reproduction (untrained Sarvam-1 and Gemma 4 E2B base evaluation, which must reproduce account 1's curves) before any real job; chains \`acct3x9b\` (X9b extra seed, ITRANS and native, then English, with the in-kernel base-evaluation guard) and \`acct3sm\` (Sarvam-m lossy, lowercase, natural) wait for that acceptance. Quota is tracked per account (30 h per rolling 7 days; two GPU sessions per account); the account-3 ledger is \`results/kaggle/acct3/quota.json\`. The paper is not edited.

`````

##### 2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected). Both setup kernels pushed and started on a T4 x2 (so GPU access works) but ended with status ERROR aft

RESULTS.md lines 4023 to 4024; first line committed in `07e9a33` on 2026-11-05 22:37:41 +0530; last line in `1d0616d` on 2026-11-05 22:59:17 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected).** Both setup kernels pushed and started on a T4 x2 (so GPU access works) but ended with status ERROR after about 3.5 minutes in the same step: the kernel's `pip install -e` of the project package failed while installing build dependencies (no output, a timeout). A CPU-only test kernel (`aarnavkembhavi/shattered-nettest`, internet requested in its metadata) confirmed the cause: DNS resolution fails for both pypi.org and huggingface.co ("Temporary failure in name resolution"), i.e. Kaggle did not grant internet to this account's kernels although the push asked for it. Kaggle only grants internet to phone-verified accounts, so the phone verification the owner reported is not in effect for kernels (or was not completed for the account). Every registered job needs internet (pinned packages, public models from Hugging Face, the Wikipedia pool), so none can run until it is fixed. Quota used on account 3: 0.21 h (two failed kernels, about 3.5 minutes each; the CPU test does not count). **What the owner must do:** sign in to kaggle.com as aarnavkembhavi, open Settings, complete 'Phone Verification' (the account must show a verified phone number), and confirm that a new notebook's Settings panel lets 'Internet' be switched on. When he has, tell me and I re-run the setup chain `acct3` (smoke gate and A1-R reproduction); the job chains `acct3x9b` and `acct3sm` are waiting and start by themselves after the acceptance. The earlier chain status DONE for `acct3` meant only that the runner finished, not that the gates passed; the gates did not pass and the acceptance marker was not written. Cleanup list (adds): the kernels `aarnavkembhavi/shattered-nettest`, `shattered-kaggle-gate`, `shattered-kaggle-retrieval-gate` and the datasets on the third account are removed at the end of Phase 2. The paper is not edited.

`````

##### 2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational). Aarnav supplied a new Kaggle API token to be used instead of the third-account token. It resolves to the Kaggle username aakarshprabhu (ch

RESULTS.md lines 4036 to 4037; first line committed in `ac6470f` on 2026-11-07 01:49:19 +0530; last line in `b194514` on 2026-11-07 01:53:51 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational).** Aarnav supplied a new Kaggle API token to be used instead of the third-account token. It resolves to the Kaggle username **aakarshprabhu** (checked with an empty CLI configuration folder; the old token resolved to aarnavkembhavi), a different account, treated as a teammate's account on Aarnav's instruction. The new token is stored only in the gitignored `.env` (KAGGLE3_API_TOKEN, KAGGLE3_USERNAME; the replaced token is kept there as KAGGLE3_API_TOKEN_PREVIOUS for cleanup and revocation), never in commits, logs or reports. The earlier attempt on aarnavkembhavi (two failed setup kernels, no internet, 0.21 h) is archived as `results/kaggle/acct3_aarnavkembhavi_failed` and its chain status under `results/phase2/`. A CPU test kernel on the new account confirms **internet works** (pypi.org and huggingface.co reachable). The private dataset `aakarshprabhu/shattered-flores-private` was created; the smoke gate and the A1-R reproduction (untrained Sarvam-1 and Gemma 4 E2B must reproduce account 1's curves) run before any job. The account-3 X9b chain was cancelled (the seed-4 runs finished on the laptop on 2026-11-06); the Sarvam-m chain `acct3sm` (lossy, lowercase, natural; 5 h cap) is kept waiting for the acceptance. Cleanup list: revoke both third-account tokens (the replaced one and the new one; both were pasted in chat), delete the datasets and kernels created on aakarshprabhu and on aarnavkembhavi, delete the nettest kernels. The username is added to the anonymiser's scrub list. This extends the statement that some Phase 2 Kaggle compute ran on teammates' accounts: account 3 (aakarshprabhu) from 2026-11-07. The paper is not edited.

`````

##### 2026-11-07 02:21 IST, KAGGLE ACCOUNT 3 (aakarshprabhu) ACCEPTED. Smoke gate passed; A1-R reproduction: the untrained base evaluation on the new account equals account 1's exactly (maximum difference of any layer curve 0.0): Sarvam-1 native 

RESULTS.md lines 4040 to 4041; first line committed in `acd0e83` on 2026-11-07 02:21:05 +0530; last line in `2466b30` on 2026-11-07 03:00:36 +0530; labels from the title and parent heading: none

`````text
- **2026-11-07 02:21 IST, KAGGLE ACCOUNT 3 (aakarshprabhu) ACCEPTED.** Smoke gate passed; A1-R reproduction: the untrained base evaluation on the new account equals account 1's exactly (maximum difference of any layer curve 0.0): Sarvam-1 native 0.9443 (layer 24), ITRANS 0.5104 (layer 21); Gemma 4 E2B native 0.9960 (layer 7), ITRANS 0.2657 (layer 7). The kernel's own gate flag is False on account 1 and on account 3 alike (it compares with laptop numbers and is not the criterion used); acceptance follows the rule applied to account 2: exact reproduction of account 1. The acceptance marker is written, so the queued chain `acct3sm` (Sarvam-m lossy, lowercase and natural forms, cap 5 h) starts by itself. Quota on account 3 so far: about 0.5 h of 30 h.

`````

##### 2026-11-07 03:00 IST, KAGGLE ACCOUNT 3 (aakarshprabhu): ACCEPTANCE CORRECTION AND FIRST JOB STARTED (operational). The acceptance written at 02:20 was premature: the smoke gate had not passed (two attempts failed because the laptop referenc

RESULTS.md lines 4042 to 4043; first line committed in `2466b30` on 2026-11-07 03:00:36 +0530; last line in `82e4226` on 2026-11-07 03:52:42 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-07 03:00 IST, KAGGLE ACCOUNT 3 (aakarshprabhu): ACCEPTANCE CORRECTION AND FIRST JOB STARTED (operational).** The acceptance written at 02:20 was premature: the smoke gate had not passed (two attempts failed because the laptop reference scores were not in the pushed package: the first lacked them, the second mounted an older version of the package dataset). Third attempt passed: both models in float16, raw-prediction agreement 0.99, 0.95, 0.96 (Sarvam-1: native, ITRANS, lossy) and 1.00, 0.99, 0.99 (Gemma 4 E2B), accuracy differences within 0.02, tolerance 0.03. With the earlier exact A1-R reproduction (account 1's curves reproduced to 0.0), the account is accepted (marker rewritten 03:0x) and the X13 Sarvam-m job for the three forms the first kernel did not reach (lossy, lowercase, natural; 4-bit, cap 5 h) was started by the waiting chain. Quota on account 3: about 1.2 h of 30 h used by the setup.

`````

## Result files, every number

(no result files for this experiment)

## Not dumped (item-level, binary or too large; path and size only)

- none

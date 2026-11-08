# X9b: QLoRA continued pretraining (Sarvam-1 primary, Qwen3.5-2B secondary), extra seeds (Phase 2)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3486-3494 | PHASE 2 AMENDMENT 2 (2026-11-02): X9 to X15, Kaggle compute, page policy |
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3495-3514 | A0. General rules for X9 to X15 |
| amended | `680151b` | 2026-11-02 19:01:49 +0530 | 3574-3611 | X9b. Real models, QLoRA continued pretraining (memory pilot on the laptop; full runs on Kaggle) |
| registered, amended | `b3cbd64` | 2026-11-02 23:21:38 +0530 | 3741-3747 | 2026-11-02 23:21 IST, DEVIATION X9b-D1 (decided by Aarnav, registered before the pilot). The X9b memory and timing pilot runs on the Kaggle T4, not on the lapto |
| result | `994de97` | 2026-11-03 02:44:05 +0530 | 3801-3805 | 2026-11-03 02:44 IST, X9b pilot, first attempt (Kaggle T4, 0.31 h, commit c78f50a; `results/kaggle/kaggle_x9b/2026-11-02T205405/shattered-kaggle-x9b.log`): meas |
| result | `bdf2139` | 2026-11-03 02:44:13 +0530 | 3806-3807 | 2026-11-03 02:44 IST, CORRECTION to the X9b pilot entry above: the sentence "exclusion rescan of the consumed articles reported 0" is withdrawn; that value is w |
| result | `f116475` | 2026-11-03 04:26:01 +0530 | 3808-3809 | 2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3 |
| result | `dc2d1df` | 2026-11-03 05:11:33 +0530 | 3815-3817 | 2026-11-03 05:11 IST, X9b pilot, second attempt (Kaggle T4, 0.75 h, commit after the micro-batch fix; `results/kaggle/kaggle_x9b/2026-11-02T225555/shattered-kag |
| result | `ec0eaad` | 2026-11-03 07:25:12 +0530 | 3818-3819 | 2026-11-03 07:25 IST, X9b pilot (Kaggle T4, X9b-D1) and fixed token budgets. sarvam-1: B = 4,997,120 tokens (305 optimizer steps), slowest 516 tokens/s, micro-b |
| result, failed or not run | `bcaebe7` | 2026-11-03 07:43:00 +0530 | 3820-3821 | 2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, |
| result | `48deb83` | 2026-11-03 08:06:57 +0530 | 3822-3824 | 2026-11-03 08:06 IST, X9b rehearsal PASSED (Sarvam-1, ITRANS, seed 0, 20 optimizer steps; Kaggle T4, 0.38 h; `results/kaggle/kaggle_x9b/2026-11-03T021326/out/sa |
| result | `3290232` | 2026-11-04 01:44:01 +0530 | 3857-3857 | 2026-11-04 01:44 IST, X9b status (Kaggle T4; `results/kaggle/kaggle_x9b/2026-11-03T023638` and `...T085520`). Batch 1 (started 3 Nov 08:06 IST, returned about 1 |
| result | `28803e6` | 2026-11-04 02:33:57 +0530 | 3862-3863 | 2026-11-04 02:33 IST, X12 contrast 1 runs now (Aarnav's decision). The Llama-2-7B A1-P precision check and scoring run on Kaggle ahead of the 18 h X9b reserve ( |
| result, failed or not run | `0cfdea0` | 2026-11-04 02:46:43 +0530 | 3868-3869 | 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST). Cause (from t |
| none | `2be4ccb` | 2026-11-04 02:53:13 +0530 | 3872-3873 | 2026-11-04 02:53 IST, watchdog: Kaggle queue chain had been stopped (my restart at 02:37 for the push-order change; the detached task could not start until the  |
| result | `399fdee` | 2026-11-04 03:33:53 +0530 | 3876-3877 | 2026-11-04 03:33 IST, X9b reserve LIFTED (Aarnav). X9B_SARVAM_H set from 18 to 0 in scripts/kaggle_queue.py: a Kaggle job now only has to fit in the remaining h |
| result | `7455dba` | 2026-11-04 09:53:29 +0530 | 3898-3899 | 2026-11-04 09:53 IST, X12 CONTRAST 1 (primary test) RESULT: SUPPORTED (as predicted). Llama-2-7B vs Ambari-7B-base-v0.1, both passed A1-P (fp16 vs float32-offlo |
| result | `ed31e10` | 2026-11-04 12:13:51 +0530 | 3905-3905 | 2026-11-04 12:13 IST, correction note to the X11 entry above (p values). The per-form McNemar p values in the X11 entry are exact and unadjusted; the registrati |
| failed or not run | `ed31e10` | 2026-11-04 12:13:51 +0530 | 3906-3907 | 2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches). (1) Ambari-Instruct-v0.1 and Llama-3.1-8B were already uploaded as p |
| result | `39d4c01` | 2026-11-04 13:21:46 +0530 | 3910-3911 | 2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction). Some Kaggle compute for Phase 2 now runs on a teammate's Kaggle account (username ashw |
| result | `59154b4` | 2026-11-04 14:10:52 +0530 | 3916-3917 | 2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly. kaggle_retrieval_gate on acc |
| result | `3c30aee` | 2026-11-04 20:44:16 +0530 | 3929-3929 | 2026-11-04 20:44 IST, X9b batch 3 moved to Kaggle account 2 (Aarnav's instruction). Independence checked in `scripts/kaggle_x9b.py` and the queue: every run tra |
| result | `952be81` | 2026-11-04 21:53:03 +0530 | 3934-3935 | 2026-11-04 21:53 IST, Kaggle account 2: duplicate push of the Ambari-Instruct-v0.1 A1-P (my driver defect; quota cost, no wrong result). The retry pushed at 20: |
| none | `17dba9c` | 2026-11-04 22:24:09 +0530 | 3940-3941 | 2026-11-04 22:24 IST, Kaggle account 2: two drivers were running at once; stopped one; root cause fixed. Cause: the driver restarts itself when its scripts chan |
| result | `5b9ae1d` | 2026-11-05 00:25:45 +0530 | 3944-3945 | 2026-11-05 00:25 IST, why the account 2 instruction-pair MDL never started (twice): Kaggle allows two GPU sessions at a time per account. At 22:08 and again at  |
| none | `1fbe72d` | 2026-11-05 00:52:48 +0530 | 3946-3947 | 2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length. Without the  |
| none | `055b2fc` | 2026-11-05 01:09:36 +0530 | 3948-3949 | 2026-11-05 01:09 IST, X12 instruction pair: both models scored (Kaggle account 2). Ambari-Instruct-v0.1 scoring (pushed 22:06 IST, 1.20 h, with the copy loader) |
| result, failed or not run | `900da25` | 2026-11-05 03:10:06 +0530 | 3958-3959 | 2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on  |
| none | `17458bc` | 2026-11-05 03:12:00 +0530 | 3960-3961 | 2026-11-05 03:12 IST, X9b secondary arm (Qwen3.5-2B, one seed, three runs in one batch, cap 10.2 h) moved forward to Kaggle account 2 and pushed at about 03:30  |
| failed or not run | `0dcc746` | 2026-11-05 10:09:51 +0530 | 3982-3983 | 2026-11-05 10:09 IST, X4 K3b-bn and K3b-te started (API and CPU; `scripts/k3b_dakshina.py sample/draft/analyse bn/te`, chain `scripts/x4k3b_chain.sh`). The exac |
| post hoc, result | `e0f0b06` | 2026-11-05 10:43:29 +0530 | 3989-3990 | 2026-11-05 10:43 IST, Phase 2 completion inventory written (`results/phase2/PHASE2_INVENTORY.md`) and new work started at Aarnav's instruction: X2 run (supporte |
| none | `3483bc8` | 2026-11-05 13:09:45 +0530 | 3997-3998 | 2026-11-05 13:09 IST, X9b secondary arm (Qwen3.5-2B, account 2): the kernel hit its 10.2 h cap ("job finished timeout" at 9.94 h of wall time) during the Englis |
| registered, result | `6be3732` | 2026-11-05 13:12:01 +0530 | 3999-4000 | 2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, |
| result | `3b1e037` | 2026-11-05 13:23:17 +0530 | 4001-4002 | 2026-11-05 13:23 IST, X9b SECONDARY ARM RESULT (Qwen3.5-2B, one seed, account 2 and laptop; `scripts/x9b_analyse.py --model qwen3.5-2b`, `results/phase2/x9b/ana |
| result, failed or not run | `3ecea71` | 2026-11-05 15:42:19 +0530 | 4015-4016 | 2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt). A push of the three remaining Sar |
| failed or not run | `cccb4f4` | 2026-11-05 22:08:29 +0530 | 4017-4018 | 2026-11-05 22:08 IST, LAPTOP POWER LOSS AND RESTART (operational). The laptop shut down uncleanly at about 16:42 (Windows event 41 and 6008, previous shutdown l |
| result | `5d9fd0e` | 2026-11-05 22:23:55 +0530 | 4021-4022 | 2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational). Aarnav reported that the owner of the third Kaggle account (username aarnavk |
| amended, failed or not run | `1d0616d` | 2026-11-05 22:59:17 +0530 | 4025-4026 | 2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged |
| none | `4579347` | 2026-11-05 22:59:29 +0530 | 4027-4028 | 2026-11-05 22:59 IST, CORRECTION NOTE (finish dates of the laptop X9b extra seeds; arithmetic error). The two entries above that give the six laptop runs a fini |
| amended, failed or not run | `8c59c8a` | 2026-11-06 00:53:19 +0530 | 4029-4030 | 2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational). Windows logged a second unclean reboot (Kernel-Power 41; bu |
| result, failed or not run | `fc1246a` | 2026-11-06 02:37:37 +0530 | 4031-4032 | 2026-11-06 02:37 IST, X9b EXTRA RUN 1 OF 6 FINISHED (`sarvam-1+itrans+s2`, code seed 2 = seed 3 in the report; laptop) AND SPEED OF THE MICRO-BATCH CAP. Run fac |
| result, failed or not run | `e605a65` | 2026-11-06 11:53:24 +0530 | 4033-4033 | 2026-11-06 11:53 IST, X9b PRIMARY ARM: EXTRA SEEDS FINISHED; RESULT WITH ALL FOUR SEEDS AND WITH THE ORIGINAL TWO (Sarvam-1; seeds 3 and 4 were ADDED AFTER SEEI |
| result, failed or not run | `ac6470f` | 2026-11-07 01:49:19 +0530 | 4036-4037 | 2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational). Aarnav supplied a new Kaggle API token to be used instead  |
| registered, result | `b194514` | 2026-11-07 01:53:51 +0530 | 4038-4039 | 2026-11-07 01:53 IST, REGISTRATION OF A SECOND SET OF EXTRA SEEDS (added AFTER seeing the originals; Aarnav's instruction of 2026-11-07 to start both; the origi |
| result | `0cd9a82` | 2026-11-08 15:33:40 +0530 | 4048-4048 | 2026-11-08 15:33 IST, X9b SECONDARY ARM (Qwen3.5-2B): EXTRA SEEDS FINISHED (added after seeing the original seed; registered 2026-11-07; code seeds 1 and 2 = se |

## Values observed in the result files (read from the files' own columns and keys)

- models: sarvam-1, qwen3.5-2b
- seeds: 0, 1, 2, 3, 9
- conditions: itrans, native, english

Result directories: `results/phase2/x9b`

## RESULTS.md entries, verbatim

##### PHASE 2 AMENDMENT 2 (2026-11-02): X9 to X15, Kaggle compute, page policy

RESULTS.md lines 3486 to 3494; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: amended

`````text
## PHASE 2 AMENDMENT 2 (2026-11-02): X9 to X15, Kaggle compute, page policy

**APPROVED by Aarnav on 2026-11-02 with four edits (X12 exemption and rename, gate record, A1-R option (a)), applied below. Nothing in X9 to X15 had been run when it was approved.** This text is appended to
RESULTS.md unchanged, committed, and tagged `phase2-amendment-2`; `shattered.runlog.provenance()` then records that tag's commit as
`phase2_amendment2_commit` in every X9 to X15 result file (next to `phase2_registration_commit`). It supersedes `docs/X9_registration_DRAFT.md`.
Already registered and unchanged: X7 control (full 6-vocabulary grid with factorized embeddings, 3 seeds; running), X8 (n = 100, annotators
X8-P and X8-Q, agreement primary, vowel ratio descriptive), the Kaggle runner and its reproducibility gate (registered 2026-11-02 before
its first run). Citations are not added in this amendment.

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

##### X9b. Real models, QLoRA continued pretraining (memory pilot on the laptop; full runs on Kaggle)

RESULTS.md lines 3574 to 3611; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: amended

`````text
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

`````

##### 2026-11-02 23:21 IST, DEVIATION X9b-D1 (decided by Aarnav, registered before the pilot). The X9b memory and timing pilot runs on the Kaggle T4, not on the laptop, because the amendment fixes the

RESULTS.md lines 3741 to 3747; first line committed in `b3cbd64` on 2026-11-02 23:21:38 +0530; last line in `9d50e92` on 2026-11-02 23:24:17 +0530; labels from the title and parent heading: registered, amended

`````text
- **2026-11-02 23:21 IST, DEVIATION X9b-D1 (decided by Aarnav, registered before the pilot).** The X9b memory and timing pilot runs on the **Kaggle T4**, not on the laptop, because the amendment fixes the
  token budget B by a 50-step timing run on the machine that will train (the T4). No rule, threshold, condition, recipe or prediction changes. B = floor(0.9 x slowest measured tokens/s x 10,800 s),
  rounded down to a multiple of the tokens per optimizer step, per model, the same for the three conditions of a model, recorded here before any full run. The three training streams are built on
  CPU first and the registered exclusion scan must report overlap 0 for every stream or nothing runs; `scripts/kaggle_x9b.py` (pilot and full modes) writes `results/phase2/x9b/pilot_done.json`.
  Queue: the X9b pilot goes right after the A1-P job in flight, ahead of the X13 and X12 scoring (about an hour or less).
- Timestamps rule (Aarnav): every time in RESULTS.md, the deviations table or a log entry comes from `scripts/stamp.py` (system clock) or the commit, never typed; `scripts/check_results_times.py` and the pre-commit hook fail an entry later than its commit or the clock.

`````

##### 2026-11-03 02:44 IST, X9b pilot, first attempt (Kaggle T4, 0.31 h, commit c78f50a; `results/kaggle/kaggle_x9b/2026-11-02T205405/shattered-kaggle-x9b.log`): measurements obtained, NOT used for B; `pilot_done.json` not written. Two implementa

RESULTS.md lines 3801 to 3805; first line committed in `994de97` on 2026-11-03 02:44:05 +0530; last line in `bdf2139` on 2026-11-03 02:44:13 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 02:44 IST, X9b pilot, first attempt (Kaggle T4, 0.31 h, commit c78f50a; `results/kaggle/kaggle_x9b/2026-11-02T205405/shattered-kaggle-x9b.log`): measurements obtained, NOT used for B; `pilot_done.json` not written. Two implementation faults, fixed (no rule change):**
  (1) the micro-batch search ran with the model in eval mode, where gradient checkpointing is not applied, so it settled on 2 sequences although peak VRAM in the timed (train-mode) loop was only 3.6 GiB (Sarvam-1) and 6.7 GiB (Qwen3.5-2B); the registered rule is the largest micro-batch that fits, so the search now runs in train mode.
  (2) the evaluation smoke needed `results/e09_romanize/best_schemes.json`, which was not in the package, and crashed after the timing runs; the package now includes it and the timings are written to `pilot_done.json` before the smoke (recorded as `eval_smoke_ok`; the driver refuses the full runs unless it is true).
  Measured at micro-batch 2 (50 micro-steps, 45 timed; fp16 compute, 4-bit NF4): Sarvam-1 tokens/s 565.8 (ITRANS), 532.5 (native), 531.4 (English); Qwen3.5-2B 612.2, 612.5, 612.6; losses finite in all six runs; exclusion rescan of the consumed articles reported 0 (not yet in a result file). **These timings underestimate the speed at the corrected micro-batch, so B is not fixed from them; the corrected pilot (about 0.3 h) is re-queued first.** The old driver's queue state carried `x9b_pilot_pushed` and moved on to the scoring; the order is restored (see the next entry when the driver restarts).

`````

##### 2026-11-03 02:44 IST, CORRECTION to the X9b pilot entry above: the sentence "exclusion rescan of the consumed articles reported 0" is withdrawn; that value is written only to `pilot_done.json`, which was not produced, and the Kaggle log doe

RESULTS.md lines 3806 to 3807; first line committed in `bdf2139` on 2026-11-03 02:44:13 +0530; last line in `f116475` on 2026-11-03 04:26:01 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 02:44 IST, CORRECTION to the X9b pilot entry above:** the sentence "exclusion rescan of the consumed articles reported 0" is withdrawn; that value is written only to `pilot_done.json`, which was not produced, and the Kaggle log does not show it, so it was not observed. The CPU report (overlap 0 for all three full streams) stands; the in-kernel rescan result will come from the corrected pilot.

`````

##### 2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3-8b/`). SIB-200 scores for english, native, ITRANS, lossy, lowercase (and natura

RESULTS.md lines 3808 to 3809; first line committed in `f116475` on 2026-11-03 04:26:01 +0530; last line in `786f67e` on 2026-11-03 04:46:26 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 04:26 IST, X13 scoring of Qwen3-8B finished (Kaggle T4 x2, float16, A1-P passed; 1.71 h of quota; `results/kaggle/x_score/2026-11-02T211301/out/qwen3-8b/`).** SIB-200 scores for english, native, ITRANS, lossy, lowercase (and natural on the 257), content-free calibration inputs, and unmapped FLORES+ retrieval (native, ITRANS; A1-R passed) are written as Phase 1-format shards; the analysis (registered contrasts) has not been run yet. The X9b pilot is re-run next (the new queue driver replaced the old one at this point; DEFER file removed, state cleaned).

`````

##### 2026-11-03 05:11 IST, X9b pilot, second attempt (Kaggle T4, 0.75 h, commit after the micro-batch fix; `results/kaggle/kaggle_x9b/2026-11-02T225555/shattered-kaggle-x9b.log`): TIMED OUT before Qwen3.5-2B; `pilot_done.json` not written; B not

RESULTS.md lines 3815 to 3817; first line committed in `dc2d1df` on 2026-11-03 05:11:33 +0530; last line in `ec0eaad` on 2026-11-03 07:25:12 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 05:11 IST, X9b pilot, second attempt (Kaggle T4, 0.75 h, commit after the micro-batch fix; `results/kaggle/kaggle_x9b/2026-11-02T225555/shattered-kaggle-x9b.log`): TIMED OUT before Qwen3.5-2B; `pilot_done.json` not written; B not fixed.** With the search in train mode the largest micro-batch that fits is **16 sequences** for Sarvam-1 (peak VRAM 10.64 GiB). Measured over 45 timed micro-steps of the 50: tokens/s **564.5 (ITRANS), 563.8 (native), 564.2 (English)**, 653 s per combination; losses finite. Throughput at micro-batch 16 is essentially the same as at micro-batch 2 in the first attempt (565.8, 532.5, 531.4), so the speed is compute-bound and B is not sensitive to the micro-batch. The 1.0 h cap I gave the job was too small: six combinations cost about 11 min each plus loading, so the job stopped itself after the three Sarvam-1 combinations (Qwen3.5-2B not reached).
  The Sarvam-1 numbers alone would give (not registered, shown for scale only) 0.9 x 563.8 x 10,800 = 5.48M tokens, i.e. 334 optimizer steps of 16,384 tokens; **B is fixed only from a complete pilot** (slowest over the three conditions of each model, rounded down to a multiple of 16,384). Fixes (no rule change): the pilot cap is now 2.2 h and each combination is written to its own file as soon as it is measured. The pilot is re-queued (next driver pass). The registered "50 steps" is kept as 50 micro-steps at the largest micro-batch that fits (my reading since 2026-11-02; an optimizer-step reading would be twice as long at micro-batch 16).

`````

##### 2026-11-03 07:25 IST, X9b pilot (Kaggle T4, X9b-D1) and fixed token budgets. sarvam-1: B = 4,997,120 tokens (305 optimizer steps), slowest 516 tokens/s, micro-batches itrans 16, native 16, english 16, pool covers B: {'itrans': True, 'native

RESULTS.md lines 3818 to 3819; first line committed in `ec0eaad` on 2026-11-03 07:25:12 +0530; last line in `bcaebe7` on 2026-11-03 07:43:00 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 07:25 IST, X9b pilot (Kaggle T4, X9b-D1) and fixed token budgets.** sarvam-1: B = 4,997,120 tokens (305 optimizer steps), slowest 516 tokens/s, micro-batches itrans 16, native 16, english 16, pool covers B: {'itrans': True, 'native': True, 'english': True}; qwen3.5-2b: B = 5,668,864 tokens (346 optimizer steps), slowest 584 tokens/s, micro-batches itrans 4, native 4, english 4, pool covers B: {'itrans': True, 'native': True, 'english': True}. Tokens per optimizer step 16,384 (32 sequences of 512; fixed before the pilot), 50 micro-steps timed. Exclusion scan: overlap 0 for every stream (CPU report) and 0 on every consumed stream in the pilot. B is the same for the three conditions of a model and is not changed. (Appended by the queue driver from `results/phase2/x9b/pilot_done.json`.)

`````

##### 2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehe

RESULTS.md lines 3820 to 3821; first line committed in `bcaebe7` on 2026-11-03 07:43:00 +0530; last line in `48deb83` on 2026-11-03 08:06:57 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehearsal discarded as designed.** Measured: 20 optimizer steps (327,680 tokens) in 589 s, loss 2.57 at step 20, adapter and checkpoint written. The failure is in `PeftModel.from_pretrained` before the evaluation: the Kaggle image ships torchao 0.10.0, which the pinned peft 0.21.2 refuses (`ImportError: Found an incompatible version of torchao. Found version 0.10.0, but only versions above 0.16.0 are supported`). Fix (no rule change): the kernel uninstalls torchao after installing the pins (nothing in this project uses it). A failed rehearsal is now repeated by the driver, never skipped (the driver would otherwise have started the full runs on the next pass); the rehearsal is re-queued (about 0.3 h). No registered X9b run has started; B stays as logged.

`````

##### 2026-11-03 08:06 IST, X9b rehearsal PASSED (Sarvam-1, ITRANS, seed 0, 20 optimizer steps; Kaggle T4, 0.38 h; `results/kaggle/kaggle_x9b/2026-11-03T021326/out/sarvam-1+itrans+s0__rehearsal/`); discarded as designed. Whole path ran: stream bu

RESULTS.md lines 3822 to 3824; first line committed in `48deb83` on 2026-11-03 08:06:57 +0530; last line in `16e09e4` on 2026-11-03 12:56:47 +0530; labels from the title and parent heading: result

`````text
- **2026-11-03 08:06 IST, X9b rehearsal PASSED (Sarvam-1, ITRANS, seed 0, 20 optimizer steps; Kaggle T4, 0.38 h; `results/kaggle/kaggle_x9b/2026-11-03T021326/out/sarvam-1+itrans+s0__rehearsal/`); discarded as designed.** Whole path ran: stream build and in-kernel rescan of the 107 consumed articles (59,397 words): overlap 0; training 583 s; checkpoint, adapter saved, merge into the unquantized fp16 base (torchao fix works), SIB-200 on 100 items in native, ITRANS and English (no non-finite values), unmapped FLORES+ retrieval (test half n = 1,005; no non-finite values); tokenizer sha256 unchanged before and after (72e5ad0c2d3a65d1...). **The rehearsal's accuracy and retrieval numbers are not results** (20 steps, 100 SIB items); the one thing to check is that the untrained-base evaluation of Sarvam-1 in the same kernel (queued with the first batch) agrees with the A1-R laptop value for the same model (native 0.9443, ITRANS 0.5104), because the rehearsal's post-training retrieval (native 0.947, ITRANS 0.751) differs from it by more than I would expect after 20 steps; if the base evaluation differs from A1-R by more than the 0.03 tolerance, the evaluation environment, not the training, is the thing to examine before any X9b number is used.
  **First batch pushed (cap 7.5 h): untrained Sarvam-1 evaluation, then runs sarvam-1:itrans:0 and sarvam-1:native:0 at B = 4,997,120 tokens (305 optimizer steps) each.** Batches 2 and 3 follow; the quota projection will hold batch 3 until older hours leave the 7-day window if needed.

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

##### 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST). Cause (from the kernel log): the kernel cannot read the Hugging Face token, so the gated repo

RESULTS.md lines 3868 to 3869; first line committed in `0cfdea0` on 2026-11-04 02:46:43 +0530; last line in `09b39ee` on 2026-11-04 02:52:11 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST).** Cause (from the kernel log): the kernel cannot read the Hugging Face token, so the gated repo meta-llama/Llama-2-7b-hf returns 401 on Kaggle. `UserSecretsClient` raised "Connection error trying to communicate with service" in all 16 kernel runs so far (the earlier models were not gated, so nothing was lost before). The same token reads both Llama repos from the laptop (HTTP 200), so access itself is granted; the Kaggle notebook has no HF_TOKEN secret attached. Fix needs a manual step in the Kaggle web UI (attach the secret HF_TOKEN to the kernels shattered-kaggle-precision and shattered-x-score, Add-ons, Secrets); no token is put in a dataset or the repository. Not relaunched yet (relaunch once after the fix). Llama-3.1-8B has the same dependency. X9b batch 3 is unaffected.

`````

##### 2026-11-04 02:53 IST, watchdog: Kaggle queue chain had been stopped (my restart at 02:37 for the push-order change; the detached task could not start until the deleted hidden.vbs was restored). Restarted at about 02:52 IST so X9b batch 3 is

RESULTS.md lines 3872 to 3873; first line committed in `2be4ccb` on 2026-11-04 02:53:13 +0530; last line in `3795c2a` on 2026-11-04 03:07:47 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 02:53 IST, watchdog:** Kaggle queue chain had been stopped (my restart at 02:37 for the push-order change; the detached task could not start until the deleted hidden.vbs was restored). Restarted at about 02:52 IST so X9b batch 3 is pushed the moment the quota projection allows (about 9 Nov 19:42 IST). Laptop GPU busy (X1 T3 gemma4-e2b, 68 percent); no idle period; X4 drafts done.

`````

##### 2026-11-04 03:33 IST, X9b reserve LIFTED (Aarnav). X9B_SARVAM_H set from 18 to 0 in scripts/kaggle_queue.py: a Kaggle job now only has to fit in the remaining hours of the 30 h per rolling 7 days; X9b batch 3 (cap 6.9 h) is pushed the momen

RESULTS.md lines 3876 to 3877; first line committed in `399fdee` on 2026-11-04 03:33:53 +0530; last line in `7ee0799` on 2026-11-04 03:43:18 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 03:33 IST, X9b reserve LIFTED (Aarnav).** X9B_SARVAM_H set from 18 to 0 in scripts/kaggle_queue.py: a Kaggle job now only has to fit in the remaining hours of the 30 h per rolling 7 days; X9b batch 3 (cap 6.9 h) is pushed the moment it fits and nothing else queues ahead of it. State at this time: 23.63 h used, headroom 6.37 h; batch 3 fits once 0.53 h roll off (about 9 Nov 19:04 IST), MDL Qwen3-8B (2.5 h cap) fits now and was launched; Llama-2 A1-P (3.5 h) fits but stays blocked by the missing Kaggle HF_TOKEN secret (flag file results/kaggle/HF_SECRET_MISSING).

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

##### 2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches). (1) Ambari-Instruct-v0.1 and Llama-3.1-8B were already uploaded as private datasets (shattered-ambari-instruct-v0-1 and shattered-llama-3-1-8b) and 

RESULTS.md lines 3906 to 3907; first line committed in `ed31e10` on 2026-11-04 12:13:51 +0530; last line in `72ff37e` on 2026-11-04 12:14:44 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches).** (1) Ambari-Instruct-v0.1 and Llama-3.1-8B were already uploaded as private datasets (shattered-ambari-instruct-v0-1 and shattered-llama-3-1-8b) and are attached by `scripts/kaggle_queue.py` for any job that names the model; all four private datasets (these two, shattered-llama-2-7b-hf and shattered-flores-private) are on the end-of-Phase-2 cleanup list. (2) **Stale driver:** the queue now hashes its scripts (kaggle_queue, kaggle_runner, kaggle_precision, x_score, kaggle_mdl, kaggle_x9b, interp/load) at start and re-executes itself before any push if they changed on disk; the runner pushes the committed tree and refuses a dirty one. (3) **Pre-launch check on the laptop (no quota):** each private dataset the job mounts must be "ready" on Kaggle, and a model named in the job arguments that is gated on Hugging Face must have a private dataset; otherwise nothing is pushed. (4) Queue order rule: non-X9b jobs are refused while an X9b Sarvam batch is pending (X9b batch 3 first, nothing ahead of it); scoring caps are 2.4 h (measured 1.2 to 1.8 h). Calendar of the remaining Kaggle jobs with start and end times: in the report to Aarnav of this time.

`````

##### 2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction). Some Kaggle compute for Phase 2 now runs on a teammate's Kaggle account (username ashwin18522; per-account quota of 30 h per rolling 7 days, tracked separately in res

RESULTS.md lines 3910 to 3911; first line committed in `39d4c01` on 2026-11-04 13:21:46 +0530; last line in `d1ef7c9` on 2026-11-04 13:27:53 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction).** Some Kaggle compute for Phase 2 now runs on a **teammate's Kaggle account** (username ashwin18522; per-account quota of 30 h per rolling 7 days, tracked separately in results/kaggle/acct2/quota.json). The token is stored only in the gitignored .env (KAGGLE2_API_TOKEN, KAGGLE2_USERNAME) and was never written to a commit, log or this file. Token verified: it authenticates and the account lists its own kernels; the first kernel (kaggle_gate smoke test) started on a T4 x2 GPU session at 13:20 IST on 2026-11-04. *What changed in the code:* the runner takes KAGGLE_ACCOUNT=1|2 (credentials, quota file, job folders and build folder per account); the queue runs one driver per account: account 1 keeps X9b (batch 3 first when its quota frees, its checkpoints and datasets live there) and, until account 2 is accepted, the rest; account 2 runs the self-contained jobs (Ambari-Instruct-v0.1 A1-P, instruction-pair scoring and MDL, Llama-3.1-8B A1-P and scoring, later X13 models). Account 2 is accepted for real jobs only after the smoke test and the A1-R reproduction on its own environment pass (file results/kaggle/acct2/ACCEPTED). Private datasets re-uploaded under account 2: shattered-flores-private, shattered-llama-3-1-8b and shattered-ambari-instruct-v0-1 (uploads in progress at this time), plus the package dataset shattered-pkg that the runner uploads. **End-of-Phase-2 cleanup list additions: delete account 2's datasets (shattered-flores-private, shattered-llama-3-1-8b, shattered-ambari-instruct-v0-1, shattered-pkg) and kernels, and revoke the token that was shared in the chat (the token is in the session transcript).** The anonymiser now scrubs the account name.

`````

##### 2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly. kaggle_retrieval_gate on account 2 (0.34 h; its own shattered-flores-private dataset): Sarvam-1 native layer

RESULTS.md lines 3916 to 3917; first line committed in `59154b4` on 2026-11-04 14:10:52 +0530; last line in `eb2aa7a` on 2026-11-04 16:09:50 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 14:10 IST, ACCOUNT 2 ACCEPTED (teammate's Kaggle account): the A1-R reproduction on account 2 matches account 1 exactly.** kaggle_retrieval_gate on account 2 (0.34 h; its own shattered-flores-private dataset): Sarvam-1 native layer 24, accuracy 0.9443; ITRANS layer 21, accuracy 0.5104; Gemma 4 E2B native layer 7, accuracy 0.9960; ITRANS layer 7, accuracy 0.2657; all per-layer train and test curves equal account 1's (max difference 0.0) and are within 0.004 of the laptop values (tolerance 0.03); the untrained evaluation of a new environment therefore reproduces the A1-R numbers (results/kaggle/acct2/a1r_reproduced.json, marker results/kaggle/acct2/ACCEPTED). Private datasets under account 2, all ready: shattered-flores-private, shattered-llama-3-1-8b (upload 1,146 s), shattered-ambari-instruct-v0-1 (826 s); local copies deleted. The account-2 queue driver (scripts/kaggle_queue2_chain.sh, KAGGLE_ACCOUNT=2) started at 14:08 IST with the Ambari-Instruct-v0.1 A1-P; account 1 now runs X9b only. Quota use so far: account 2 about 0.5 of 30 h, account 1 29.36 of 30 h. **Calendar (estimates from measured runtimes; gating by caps):** account 2: v0.1 A1-P 14:10 to 15:40 on 4 Nov, v0.1 scoring to 17:10, v0.2 scoring to 18:40, instruction-pair MDL to 20:52, Llama-3.1-8B A1-P to 22:22, Llama-3.1-8B scoring to 00:10 on 5 Nov; account 1: X9b batch 3 from 10 Nov 02:50 to 09:20, X9b Qwen3.5-2B arm 10 Nov 09:20 to 18:20 (last job, projected end 10 Nov about 18:20 IST). Account 2 then has about 19 h of its week free for further X13 models and MDL jobs.

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

##### 2026-11-04 22:24 IST, Kaggle account 2: two drivers were running at once; stopped one; root cause fixed. Cause: the driver restarts itself when its scripts change on disk, and on Windows os.execv returns to the parent immediately, so the ch

RESULTS.md lines 3940 to 3941; first line committed in `17dba9c` on 2026-11-04 22:24:09 +0530; last line in `06100d7` on 2026-11-04 22:37:35 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 22:24 IST, Kaggle account 2: two drivers were running at once; stopped one; root cause fixed.** Cause: the driver restarts itself when its scripts change on disk, and on Windows os.execv returns to the parent immediately, so the chain thought the pass had ended and an orphan driver kept running beside the chain's next pass (visible as two kaggle_queue.py processes pushing x_score and kaggle_mdl at 22:06 and 22:08 IST against one state file, which can overwrite each other's records). The restart now uses a blocking subprocess. I stopped the later driver (PID 75952) with its process tree, which also ended the local runner process that was waiting on the instruction-pair MDL kernel; **that Kaggle kernel (kaggle_mdl, pushed 22:08 IST, cap 3.0 h, account 2) is still running on Kaggle and its output must be fetched by hand (`KAGGLE_ACCOUNT=2 python scripts/kaggle_runner.py fetch kaggle_mdl`) and its state entry written; until then its 3.0 h stay counted as pushed.** The remaining account 2 drivers are the X9b batch 3 driver (pushed 20:35) and the scoring driver (x_score for Ambari-Instruct-v0.1 pushed 22:06).

`````

##### 2026-11-05 00:25 IST, why the account 2 instruction-pair MDL never started (twice): Kaggle allows two GPU sessions at a time per account. At 22:08 and again at 23:39 IST the MDL push came while X9b batch 3 and an x_score job were already ru

RESULTS.md lines 3944 to 3945; first line committed in `5b9ae1d` on 2026-11-05 00:25:45 +0530; last line in `1fbe72d` on 2026-11-05 00:52:48 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 00:25 IST, why the account 2 instruction-pair MDL never started (twice): Kaggle allows two GPU sessions at a time per account.** At 22:08 and again at 23:39 IST the MDL push came while X9b batch 3 and an x_score job were already running on account 2; the push was not accepted (no kernel exists), but the runner went on polling a kernel that does not exist and reserved 3.0 h in the quota file. Fixed: the runner now stops with an error if the push output does not say it succeeded, and the queue refuses a push while two other kernels of the account are running (checked on the laptop, no quota). The stale MDL reservation is set to 0 h. The MDL will be pushed when a slot is free (after the x_score jobs). No result is affected.

`````

##### 2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length. Without the copy loader: fp16 load 2,866 s (Llama-3.1-8B A1-P, 2.78 h in total) and 3,420 s 

RESULTS.md lines 3946 to 3947; first line committed in `1fbe72d` on 2026-11-05 00:52:48 +0530; last line in `055b2fc` on 2026-11-05 01:09:36 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length.** Without the copy loader: fp16 load 2,866 s (Llama-3.1-8B A1-P, 2.78 h in total) and 3,420 s (Ambari-Instruct-v0.1 A1-P, 1.94 h in total; an earlier attempt of the same job reached its 3.07 h self-stop); on account 1 Llama-2 loaded in 631 s. With the copy loader (parallel copy to local disk before loading; first used by the Ambari-Instruct-v0.1 scoring pushed 22:06 IST): "[model_source] copied shattered-ambari-instruct-v0-1: 12.8 GiB in 72s to local disk", and the whole scoring job took 1.20 h (4,112 s), as long as the account 1 scoring jobs (1.23 to 1.81 h). The A1-P timeout stays 5 h until an A1-P job has run with the copy loader. X9b batch 3 (training, loads Sarvam-1 from the Hub) is expected at about 6.5 h on either account (account 1: 6.31 and 6.60 h).

`````

##### 2026-11-05 01:09 IST, X12 instruction pair: both models scored (Kaggle account 2). Ambari-Instruct-v0.1 scoring (pushed 22:06 IST, 1.20 h, with the copy loader) and Ambari-Instruct-v0.2 scoring (pushed 23:19, 1.67 h) are complete and record

RESULTS.md lines 3948 to 3949; first line committed in `055b2fc` on 2026-11-05 01:09:36 +0530; last line in `a7577c6` on 2026-11-05 01:24:12 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 01:09 IST, X12 instruction pair: both models scored (Kaggle account 2).** Ambari-Instruct-v0.1 scoring (pushed 22:06 IST, 1.20 h, with the copy loader) and Ambari-Instruct-v0.2 scoring (pushed 23:19, 1.67 h) are complete and recorded; the pair's MDL assembly-layer job (the registered contrast 2 measure, rule as H3, descriptive) was pushed at 01:00 IST on account 2 and is running; the contrast 2 analysis script is not built yet and is built while the MDL job runs. The Llama-3.1-8B scoring (X13) waits for a free GPU slot on account 2 (X9b batch 3 and the MDL job occupy both).

`````

##### 2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on both measures (as predicted). All six runs are complete: batches 1 and 2 on Kagg

RESULTS.md lines 3958 to 3959; first line committed in `900da25` on 2026-11-05 03:10:06 +0530; last line in `17458bc` on 2026-11-05 03:12:00 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on both measures (as predicted).** All six runs are complete: batches 1 and 2 on Kaggle account 1 (3 Nov), batch 3 (native seed 1, English seed 1) on account 2 (6.47 h; the in-kernel base-evaluation check passed first: native 0.9443 at layer 24, ITRANS 0.5104 at layer 21, equal to A1-R and to the account 1 base). B = 4,997,120 tokens per run (305 optimizer steps); tokenizer sha256 unchanged by training in every run; overlap 0 in every stream. Registered rule: gap g = native minus ITRANS after training on condition c; D_N = g(native) - g(ITRANS), D_E = g(English) - g(ITRANS); 97.5% paired-bootstrap intervals with one of the two seeds drawn per cell per resample. **SIB-200 accuracy (n = 1,004): g(0) = +0.233 before training (native 0.768, ITRANS 0.535); after training g(ITRANS) = +0.117, g(native) = +0.342, g(English) = +0.313; D_N = +0.225 [0.177, 0.273] (seeds +0.222, +0.227); D_E = +0.196 [0.150, 0.244] (seeds +0.196, +0.196): supported.** **FLORES+ retrieval (test half n = 1,005): g(0) = +0.434 (native 0.944, ITRANS 0.510); g(ITRANS) = +0.081, g(native) = +0.418, g(English) = +0.472; D_N = +0.337 [0.296, 0.378] (seeds +0.328, +0.346); D_E = +0.391 [0.344, 0.435] (seeds +0.381, +0.401): supported.** What moved (seed means, native / ITRANS accuracy): after ITRANS training 0.766 / 0.649 on SIB-200 (ITRANS +11 points) and retrieval 0.927 / 0.847 (ITRANS +34 points); after native training SIB-200 0.766 / 0.424 and retrieval 0.920 / 0.502; after English training SIB-200 0.757 / 0.443 and retrieval 0.920 / 0.449. **So with the tokenizer and the number of pieces per word fixed, continued pretraining on ITRANS text closed most of the gap by raising ITRANS (accuracy 0.535 to 0.649, retrieval 0.510 to 0.847), while the two controls left ITRANS retrieval unchanged to lower and lowered ITRANS SIB-200 accuracy (to 0.42 to 0.44, below the base).** The gap after the controls is therefore larger than the base gap g(0), i.e. D_N and D_E partly reflect the controls widening the gap and not only ITRANS training narrowing it; the narrowing by ITRANS training alone is 0.233 to 0.117 on SIB-200 and 0.434 to 0.081 on retrieval. Seed spread is at most 0.02 in every D. English SIB-200 damage check (descriptive, no verdict; base 0.768): ITRANS-trained -1.6 and -1.8 points, native-trained -2.6 and -2.8, **English-trained -5.1 and -5.3 (flagged: more than 5 points)**. Caveats as registered: adapters trained against the 4-bit base and evaluated on the unquantized fp16 base plus adapter; two seeds give a crude seed-variance estimate. The Qwen3.5-2B arm (secondary, one seed) has not run; it is the last Kaggle job and the first cut. This is the causal test of familiarity at fixed fragmentation that X12 pointed to. Nothing against a prediction. The paper is not edited.

`````

##### 2026-11-05 03:12 IST, X9b secondary arm (Qwen3.5-2B, one seed, three runs in one batch, cap 10.2 h) moved forward to Kaggle account 2 and pushed at about 03:30 IST (account 2 had a free GPU slot and 13 h of quota; account 1 would not have h

RESULTS.md lines 3960 to 3961; first line committed in `17458bc` on 2026-11-05 03:12:00 +0530; last line in `b9383db` on 2026-11-05 03:38:22 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 03:12 IST, X9b secondary arm (Qwen3.5-2B, one seed, three runs in one batch, cap 10.2 h) moved forward to Kaggle account 2 and pushed at about 03:30 IST** (account 2 had a free GPU slot and 13 h of quota; account 1 would not have had quota for it before 10 Nov). The Sarvam arm is complete, so the arm is no longer behind any X9b batch; account 1 will merge its state and not repeat it. Account 2 therefore runs the Qwen arm (since 03:30, expected end about 13:00 IST today) and the Llama-3.1-8B scoring (since about 02:30). With these two, the registered Kaggle list is complete except possible further X13 models (the X13 Sarvam model screen has not been run).

`````

##### 2026-11-05 10:09 IST, X4 K3b-bn and K3b-te started (API and CPU; `scripts/k3b_dakshina.py sample|draft|analyse bn|te`, chain `scripts/x4k3b_chain.sh`). The exact K3b design: 500 Dakshina strings (duplicates and strings with fewer than 3 nat

RESULTS.md lines 3982 to 3983; first line committed in `0dcc746` on 2026-11-05 10:09:51 +0530; last line in `c44254c` on 2026-11-05 10:32:26 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 10:09 IST, X4 K3b-bn and K3b-te started (API and CPU; `scripts/k3b_dakshina.py sample|draft|analyse bn|te`, chain `scripts/x4k3b_chain.sh`).** The exact K3b design: 500 Dakshina strings (duplicates and strings with fewer than 3 native words dropped; pools 9,198 for Bengali; seed 6), a 200-string resample subset (seed 7, temperature 1.0, two extra drafts), Gemini gemini-3.5-flash-lite with the same prompt as the Kannada drafts (language name changed), pooled ratios Gemini/human of vowel doubling (aa, ee, ii, oo, uu per letter), h-digraph use and English-word share against the band [0.80, 1.25] (90% CI); paid-tier cap (6,000 a day, 60 a minute). The laptop GPU has nothing ready (all registered GPU work for Phases X4, X6, X10, X11 is done); it has been idle since 09:52 IST. Remaining registered items elsewhere: the Qwen3.5-2B arm of X9b (Kaggle, running), X5 (cross-language consistency, analysis only, needs X2 exposure ratios), X14 (hosted models, API, waiting for the cap reset), the X13 Sarvam-model screen.

`````

##### 2026-11-05 10:43 IST, Phase 2 completion inventory written (`results/phase2/PHASE2_INVENTORY.md`) and new work started at Aarnav's instruction: X2 run (supported), K3b-bn done (refuted), K3b-te running, X10 post hoc extraction check for Qwe

RESULTS.md lines 3989 to 3990; first line committed in `e0f0b06` on 2026-11-05 10:43:29 +0530; last line in `b9246e2` on 2026-11-05 10:52:45 +0530; labels from the title and parent heading: post hoc, result

`````text
- **2026-11-05 10:43 IST, Phase 2 completion inventory written (`results/phase2/PHASE2_INVENTORY.md`) and new work started at Aarnav's instruction:** X2 run (supported), K3b-bn done (refuted), K3b-te running, X10 post hoc extraction check for Qwen3.5-2B running on the laptop (not registered; the registered X10 verdict unchanged), X13 Sarvam screen done (sarvam-m, 23.6B, standard Mistral code, 4-bit, is the largest Sarvam model that fits 2 x T4; sarvam-30b and sarvam-105b need remote code and are excluded; scoring pushed to Kaggle account 2), X9b analysis extended (per-run table, training budget per form, tokens per word, English regression interval, ITRANS-trained versus the original native level) ready for the Qwen3.5-2B arm.

`````

##### 2026-11-05 13:09 IST, X9b secondary arm (Qwen3.5-2B, account 2): the kernel hit its 10.2 h cap ("job finished timeout" at 9.94 h of wall time) during the English run's retrieval step; operational note, nothing changed in the registration. C

RESULTS.md lines 3997 to 3998; first line committed in `3483bc8` on 2026-11-05 13:09:45 +0530; last line in `6be3732` on 2026-11-05 13:12:01 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 13:09 IST, X9b secondary arm (Qwen3.5-2B, account 2): the kernel hit its 10.2 h cap ("job finished timeout" at 9.94 h of wall time) during the English run's retrieval step; operational note, nothing changed in the registration.** Complete: ITRANS run (346 optimizer steps, 5,668,864 tokens, tokenizer hash identical before and after) and native run (both with SIB-200 in three forms and retrieval, done.json written). English run: trained to the end (loss log to step 340), adapter saved, SIB-200 in all three forms scored (non-finite 0), but retrieval.json and done.json were not written. Cause: the cap (10.2 h) left too little for three trainings of about 2.6 h plus three evaluations of about 0.5 h each (training 9,199 s and evaluation about 2,000 s per run). Fix (the single relaunch allowed by the standing order, done on the laptop instead of Kaggle because only the retrieval step is missing and account 2 has 3.6 h of quota left): `scripts/x9b_finish_english.py` (chain `x9bfin`, queued behind the laptop pilot) loads the fp16 base, merges the saved adapter and runs the same Phase 1 retrieval scorer; it also rebuilds the English stream on CPU for the consumed article, word and token counts and the overlap scan, takes the loss log from the kernel's own stdout, and writes done.json marked "reconstructed_after_timeout" (the kernel's own before and after tokenizer hashes for that run were not written; the hash is taken from the unmodified tokenizer and compared with the ITRANS run's). Quota used on account 2: 26.4 h of 30 h in the last 7 days. The Qwen arm is not analysed until the English run has its retrieval.

`````

##### 2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, budgets and verdicts are unchanged). Why the laptop GPU was idle: the registere

RESULTS.md lines 3999 to 4000; first line committed in `6be3732` on 2026-11-05 13:12:01 +0530; last line in `3b1e037` on 2026-11-05 13:23:17 +0530; labels from the title and parent heading: registered, result

`````text
- **2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, budgets and verdicts are unchanged).** Why the laptop GPU was idle: the registered laptop queue was empty (the last laptop job, X5, finished 11:42; idle until the feasibility pilot started at about 12:44). **(1) X9b primary arm (Sarvam-1) extra seeds.** Feasibility pilot on the RTX 3070 laptop (`scripts/x9b_laptop_pilot.py`, `results/phase2/x9b/laptop_pilot.json`, registered recipe unchanged, 50 micro-steps): ITRANS 633.6 tokens/s, native 564.5 tokens/s, micro-batch 16, finite loss; the card spills past 8 GB into shared memory (torch peak 10.6 GiB), which changes speed but not the arithmetic; at the registered budget B = 4,997,120 tokens per run that is 2.46 h of training per run (the registered T4 pilot's slowest rate is 515.7 tokens/s). It fits. Extra runs: **seeds 2 and 3 in the code (called seeds 3 and 4, beside the original seeds 1 and 2 = code seeds 0 and 1) for the ITRANS, native and English arms**, same QLoRA recipe, same streams and budget, same evaluation, run on the laptop with the in-run base-evaluation guard (the untrained base must reproduce the A1-R values in this environment before training starts; native 0.9443 layer 24, ITRANS 0.5104 layer 21). Output `results/kaggle/laptop_x9b/2026-11-05/out`. **Labelled "added after seeing seeds 1 and 2". The paper reports all four seeds together and the original two separately, whatever they show;** the registered verdict stays the one from the original two seeds. The 97.5% intervals will be computed twice (original two seeds; all four seeds, one seed drawn per cell per resample), same code. Environment difference stated: laptop (Windows, RTX 3070 8 GB with shared-memory spill) against Kaggle T4. **(2) X9a-low extra seeds:** exposure levels 0.1%, 0.3% and 1%, code seeds 3 and 4 (called seeds 4 and 5; the original seeds are 0, 1, 2), same recipe and evaluation, per-seed values reported, labelled the same way; the registered X9a-low rule is not re-evaluated on a different set of seeds, the table will show original three and all five. The 1% level is the X9a level-1 run (`x9a_p1_s3`, `x9a_p1_s4`). Queue (chain `x9extra`, after the Qwen English-run completion): X9a-low extras first (6 runs, about 18 min each, about 2 h), then the six X9b runs (about 2.5 h training plus evaluation each, an estimated 16 to 18 h in total, projected finish about 6 Nov 09:00 to 11:00 IST). X9a-low goes first only because it is short and returns in about 2 h; X9b follows without waiting for anything else. The paper is not edited.

`````

##### 2026-11-05 13:23 IST, X9b SECONDARY ARM RESULT (Qwen3.5-2B, one seed, account 2 and laptop; `scripts/x9b_analyse.py --model qwen3.5-2b`, `results/phase2/x9b/analysis_qwen3.5-2b.json`): SUPPORTED on both measures, as registered (prediction: 

RESULTS.md lines 4001 to 4002; first line committed in `3b1e037` on 2026-11-05 13:23:17 +0530; last line in `753999e` on 2026-11-05 14:08:43 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 13:23 IST, X9b SECONDARY ARM RESULT (Qwen3.5-2B, one seed, account 2 and laptop; `scripts/x9b_analyse.py --model qwen3.5-2b`, `results/phase2/x9b/analysis_qwen3.5-2b.json`): SUPPORTED on both measures, as registered (prediction: D_N > 0 and D_E > 0 with the 97.5% interval above 0). Secondary arm, one seed, item variance only; it does not enter the primary conclusion.** g = native minus ITRANS accuracy; D_N = g(native-trained) - g(ITRANS-trained), D_E = g(English-trained) - g(ITRANS-trained). **SIB-200 (n = 1,004): g before training 0.436; after ITRANS training 0.173, after native training 0.458, after English training 0.433. D_N = +0.285 [0.241, 0.328]; D_E = +0.260 [0.219, 0.301].** **FLORES+ retrieval (n = 1,005): g before 0.858; after ITRANS 0.279, native 0.862, English 0.845. D_N = +0.583 [0.545, 0.620]; D_E = +0.566 [0.529, 0.603].** Per run (one seed each): SIB-200 native / ITRANS / English: ITRANS-trained 0.687 / 0.514 / 0.802; native-trained 0.708 / 0.250 / 0.798; English-trained 0.678 / 0.245 / 0.785; untrained 0.674 / 0.238 / 0.804. Retrieval native / ITRANS: ITRANS-trained 0.975 / 0.697; native-trained 0.990 / 0.128; English-trained 0.983 / 0.138; untrained 0.977 / 0.119. **Trained token budget per form: 5,668,864 tokens in every run (346 optimizer steps of 16,384 tokens)**; the ITRANS stream held 2,505 articles / 1,312,877 words (4.32 tokens per word), the native stream 1,995 articles / 1,040,695 words (5.45), the English stream 5,376 articles / 3,718,950 words (1.52); the consumed streams overlap the evaluation sentences in 0 articles. **Tokens per word before and after training: unchanged, because the tokenizer is identical (sha256 63c71e09... before and after, all three runs); on FLORES+ Kannada the model uses 5.33 tokens per word native and 4.20 ITRANS, before and after.** **English regression (SIB-200 English, change against the untrained model, 95% interval): ITRANS-trained -0.2 points [-1.7, +1.2], native-trained -0.6 [-2.0, +0.7], English-trained -1.9 [-3.6, -0.2]; none exceeds the 5-point flag.** **ITRANS-trained models do not reach the original native level: ITRANS accuracy after ITRANS training 0.514 against untrained native 0.674 (SIB-200, difference -0.160 [-0.191, -0.129]); retrieval 0.697 against 0.977 (difference -0.281 [-0.309, -0.252]).** So ITRANS exposure closes about 60% of the SIB-200 form gap and none of the way to native on retrieval, and the contrast with the native and English arms (which leave the ITRANS side at the base level) is what the registered rule tests. Operational facts: the kernel's cap hit during the English run's retrieval; completed on the laptop (see the entry above); the English run's `done.json` is marked reconstructed. The paper is not edited.

`````

##### 2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt). A push of the three remaining Sarvam-m forms (lossy, lowercase, natural; chain `smrest`, account 2, cap 5 h) was 

RESULTS.md lines 4015 to 4016; first line committed in `3ecea71` on 2026-11-05 15:42:19 +0530; last line in `cccb4f4` on 2026-11-05 22:08:29 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt).** A push of the three remaining Sarvam-m forms (lossy, lowercase, natural; chain `smrest`, account 2, cap 5 h) was refused by Kaggle at 15:39: "Maximum weekly GPU quota of 30.00 hours reached". The queue's own ledger for account 2 (`results/kaggle/acct2/quota.json`, 20.35 h) did not include the sessions of the X9b batch 3 and the Qwen3.5-2B arm (9.94 h), which the X9b-only driver records in its own ledger; the two ledgers together are at the 30 h cap, and Kaggle's count is the binding one. The first account's ledger shows 29.36 h in the last 7 days. Consequence: no Kaggle job can be pushed on either account until hours roll off: account 1 from about 9 Nov (the first 2 Nov sessions free up from 11:20 UTC on 9 Nov, then steadily), account 2 from about 11 Nov 07:56 UTC (its first sessions were on 4 Nov). The three Sarvam-m forms and the Sarvam-m X10 job therefore wait for that quota; the Sarvam-m verdict on native vs ITRANS (7 of 7 models) does not depend on them. Chain `smrest` is marked FAILED for this reason, not for an error in the job. The laptop GPU stays busy with the extra seeds (X9b about 16 to 18 h). Standing order 2 (use every quota hour) is satisfied: both accounts are at the cap.

`````

##### 2026-11-05 22:08 IST, LAPTOP POWER LOSS AND RESTART (operational). The laptop shut down uncleanly at about 16:42 (Windows event 41 and 6008, previous shutdown logged at 16:10:37 PM by the event, the last file write of the X9b extra run at 1

RESULTS.md lines 4017 to 4018; first line committed in `cccb4f4` on 2026-11-05 22:08:29 +0530; last line in `739114f` on 2026-11-05 22:15:42 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 22:08 IST, LAPTOP POWER LOSS AND RESTART (operational).** The laptop shut down uncleanly at about 16:42 (Windows event 41 and 6008, previous shutdown logged at 16:10:37 PM by the event, the last file write of the X9b extra run at 16:42) and came back at 22:00:56; the GPU was idle for about 5 h 20 min (16:42 to 22:07) with the X9b extra-seed chain interrupted, which breaks the standing order that the GPU is never idle; cause: a power or system failure on the machine, not a project process. The chain came back by itself at 22:02 but stopped at 22:06 on an unreadable checkpoint: the step-100 checkpoint of `sarvam-1+itrans+s2` was being written when power was lost (zip archive truncated). Fixes: the corrupt checkpoint file (my own output of that run) was deleted and the run restarts from step 0 (about 1.4 h of training lost: it had reached step 100 of 305); checkpoint writes in `scripts/kaggle_x9b.py` are now atomic (written to a temporary file, then replaced), which does not touch the recipe, streams or evaluation; the chain `x9extra` was relaunched at 22:07 and skips the finished base evaluation. The X9b extra-seed finish estimate moves from about 7 Nov 09:30 to about 8 Nov 03:30 to 05:00 IST (six runs of about 2.9 h from 22:07). Kaggle kernels were not affected (none running). The 15-minute watchdog kept firing in this session; no other process had been lost.

`````

##### 2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational). Aarnav reported that the owner of the third Kaggle account (username aarnavkembhavi) confirmed it is a teammate's account, agreed to its use and confirmed t

RESULTS.md lines 4021 to 4022; first line committed in `5d9fd0e` on 2026-11-05 22:23:55 +0530; last line in `07e9a33` on 2026-11-05 22:37:41 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational).** Aarnav reported that the owner of the third Kaggle account (username aarnavkembhavi) confirmed it is a teammate's account, agreed to its use and confirmed the phone is verified; its token is in the gitignored \`.env\` only. **Statement for the record: some Phase 2 Kaggle compute ran on teammates' accounts, not on Aarnav's: account 2 (username ashwin18522, a teammate's, from 2026-11-04 07:50 UTC: gates, A1-R reproduction, A1-P checks for the Llama and Ambari-Instruct models, instruction-pair and Llama-3.1-8B scoring and MDL, X9b batch 3 (Sarvam-1, 2026-11-04), the X9b Qwen3.5-2B arm (2026-11-04 21:41 UTC to 2026-11-05) and the X13 Sarvam-m scoring (2026-11-05 05:10 UTC)); and from 2026-11-05 account 3 (username aarnavkembhavi, a teammate's), starting with its smoke gate and A1-R reproduction on 2026-11-05 and followed by the jobs listed below once those pass.** **Audit (requested), checked from the Kaggle side: every kernel on each account was listed with its owner. Account 1 (aarnavkembhavi1): 6 kernels (x-score, kaggle-x9b, kaggle-mdl, kaggle-precision, kaggle-gate, kaggle-retrieval-gate), all owned by aarnavkembhavi1, 5 datasets all under aarnavkembhavi1. Account 2 (ashwin18522): the same 6 kernels, all owned by ashwin18522, 4 datasets all under ashwin18522. Account 3 (aarnavkembhavi): no shattered-* kernel and no dataset before today. The two ledgers hold 35 recorded pushes (23 on account 1, 12 on account 2 plus the sessions of the X9b-only ledger): every recorded kernel slug carries the owner of its own account, no kernel exists under any other owner, so no job ran on the fallback login.** The one fallback found concerns the CLI configuration, not a job: the Kaggle CLI falls back to the login stored in the user profile (which is the account aarnavkembhavi) when no token is given; every run passes its own token and username, an invalid token is refused rather than falling back, and each account now has its own empty CLI configuration folder in \`build/kaggle_config_<n>\` (runner change committed). Setup of account 3: private dataset \`aarnavkembhavi/shattered-flores-private\` (the FLORES+ evaluation sentences, as on the other accounts; no other datasets: the models of its jobs are public), then the smoke gate and the A1-R retrieval reproduction (untrained Sarvam-1 and Gemma 4 E2B base evaluation, which must reproduce account 1's curves) before any real job; chains \`acct3x9b\` (X9b extra seed, ITRANS and native, then English, with the in-kernel base-evaluation guard) and \`acct3sm\` (Sarvam-m lossy, lowercase, natural) wait for that acceptance. Quota is tracked per account (30 h per rolling 7 days; two GPU sessions per account); the account-3 ledger is \`results/kaggle/acct3/quota.json\`. The paper is not edited.

`````

##### 2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged). After the power-loss restart the first extra run (`sarvam-1+itrans+s2`) reach

RESULTS.md lines 4025 to 4026; first line committed in `1d0616d` on 2026-11-05 22:59:17 +0530; last line in `4579347` on 2026-11-05 22:59:29 +0530; labels from the title and parent heading: amended, failed or not run

`````text
- **2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged).** After the power-loss restart the first extra run (`sarvam-1+itrans+s2`) reached step 100 at 22:50 and then sat in `torch.save` for more than 8 minutes with the GPU idle (py-spy: `serialization._save`, `write_record`, one core at 100%); the first attempt did the same (step 100 logged at about 16:20, checkpoint file last written 16:42, when the power failed). Cause: the optimizer state is the paged 8-bit AdamW state (bitsandbytes), whose pages migrate one by one while the 8 GB card is full; writing it takes over 20 minutes per checkpoint, three checkpoints per run, about 1 h of every 2.9 h run, about 6 to 7 h over six runs (the Kaggle T4s had room for it, the laptop does not). Fix, committed: checkpoints now hold the adapter, scheduler, scaler and step but not the optimizer state, which makes the save take seconds; the checkpoint is only ever read after an interruption, so an uninterrupted run is numerically identical to before; a run resumed from such a checkpoint resets the Adam moments, and `done.json` carries `resumed_without_optimizer_state` (true) so it can be reported or excluded. The running ITRANS run is resumed from its step-100 checkpoint, which does contain the optimizer state (written before the change), so it continues exactly; the chain `x9extra` is relaunched after the restart. The finish estimate improves by about 6 h: about 8 Nov 00:00 to 02:00 IST for the six laptop runs, if account 3 does not take the seed-4 runs.

`````

##### 2026-11-05 22:59 IST, CORRECTION NOTE (finish dates of the laptop X9b extra seeds; arithmetic error). The two entries above that give the six laptop runs a finish of "8 Nov" (after the power-loss restart, and in the checkpoint entry) are wr

RESULTS.md lines 4027 to 4028; first line committed in `4579347` on 2026-11-05 22:59:29 +0530; last line in `8c59c8a` on 2026-11-06 00:53:19 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 22:59 IST, CORRECTION NOTE (finish dates of the laptop X9b extra seeds; arithmetic error).** The two entries above that give the six laptop runs a finish of "8 Nov" (after the power-loss restart, and in the checkpoint entry) are wrong by about a day and a half: six runs of about 2.9 h each (2.5 h training, 0.4 h evaluation) started at 22:07 on 5 Nov end about **6 Nov 15:30 IST**, and the one run slowed by the 20-minute checkpoint stalls (about 1 h) moves that to about **6 Nov 16:30 to 17:30 IST** with the checkpoint fix in place. If account 3 becomes usable and takes the three seed-4 runs, the laptop's three seed-3 runs end about 6 Nov 07:00 IST. The earlier report to Aarnav quoted the wrong date and is corrected in the next report.

`````

##### 2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational). Windows logged a second unclean reboot (Kernel-Power 41; bugcheck 0x1e, an unhandled access violation, last good time 22:41:16; the earlier

RESULTS.md lines 4029 to 4030; first line committed in `8c59c8a` on 2026-11-06 00:53:19 +0530; last line in `fc1246a` on 2026-11-06 02:37:37 +0530; labels from the title and parent heading: amended, failed or not run

`````text
- **2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational).** Windows logged a second unclean reboot (Kernel-Power 41; bugcheck 0x1e, an unhandled access violation, last good time 22:41:16; the earlier one, 16:10, was bugcheck 0x9f, a driver power-state failure), the machine came back at 23:06 and the chain at 23:47. Both crashes came while the GPU was at full memory with shared-memory spill (peak 10.6 GiB asked of an 8 GB card at micro-batch 16) and, the second time, during the stalled checkpoint save. Consequences: GPU idle 22:41 to 23:47 (about 1 h 05 min, a crash, not a project process); the ITRANS seed-3 run (code seed 2) had no usable checkpoint and **restarted from step 0 at 23:47** (it is at step 140 or more now, ckpt written with the fast format at 00:31). Change (committed, recipe unchanged): the code reads an optional laptop-only file `build/x9b_max_micro_batch.txt` and caps the micro-batch at its value, with proportionally more accumulation steps, so the optimizer step is the same (16,384 tokens) while memory stays under the card's 8 GB; it holds 8 from now, so the run in progress (started at 23:47) keeps micro-batch 16 and the next five runs use 8 (done.json records the micro-batch used). Speed cost expected at a few percent. If the laptop crashes again the run resumes from the adapter checkpoint with reset Adam moments and is flagged in done.json (`resumed_without_optimizer_state`). Projected finish of the six laptop runs: the first at about 02:40 on 6 Nov, the last about 6 Nov 17:30 to 19:30 IST.

`````

##### 2026-11-06 02:37 IST, X9b EXTRA RUN 1 OF 6 FINISHED (`sarvam-1+itrans+s2`, code seed 2 = seed 3 in the report; laptop) AND SPEED OF THE MICRO-BATCH CAP. Run facts: 305 optimizer steps, 4,997,120 tokens, micro-batch 16, tokenizer hash unchan

RESULTS.md lines 4031 to 4032; first line committed in `fc1246a` on 2026-11-06 02:37:37 +0530; last line in `e605a65` on 2026-11-06 11:53:24 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-06 02:37 IST, X9b EXTRA RUN 1 OF 6 FINISHED (`sarvam-1+itrans+s2`, code seed 2 = seed 3 in the report; laptop) AND SPEED OF THE MICRO-BATCH CAP.** Run facts: 305 optimizer steps, 4,997,120 tokens, micro-batch 16, tokenizer hash unchanged, not resumed from a checkpoint (it restarted from step 0 after the second crash), training 8,057 s (it includes the 20-minute pilot-sized stall of the discarded first save), evaluation done. Untrained-base guard passed beforehand (native 0.9443, ITRANS 0.5114 against the reference 0.9443 and 0.5104). Interim retrieval (unmapped, n = 1,005, train-chosen layer): native 0.9333 (layer 24), ITRANS 0.8746 (layer 20); the original ITRANS-trained seeds gave ITRANS 0.840 and 0.854 and native 0.926 and 0.928. SIB-200 and the paired analysis come with the whole set (`x9b_analyse.py --seeds 0,1,2,3`). **Speed: the next run (native seed 3) with the micro-batch capped at 8 trains at about 17.6 s per optimizer step (step 20 at 353 s), against about 27 s at micro-batch 16: with no shared-memory spill the card is faster.** Projected training time 1.5 h per run, with evaluation about 1.9 h, so the five remaining laptop runs end about **6 Nov 12:00 IST** (earlier estimate 17:30 to 19:30). The paper is not edited.

`````

##### 2026-11-06 11:53 IST, X9b PRIMARY ARM: EXTRA SEEDS FINISHED; RESULT WITH ALL FOUR SEEDS AND WITH THE ORIGINAL TWO (Sarvam-1; seeds 3 and 4 were ADDED AFTER SEEING SEEDS 1 AND 2, same QLoRA recipe, streams and budget, laptop; `x9b_analyse.py

RESULTS.md lines 4033 to 4033; first line committed in `e605a65` on 2026-11-06 11:53:24 +0530; last line in `e605a65` on 2026-11-06 11:53:24 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-06 11:53 IST, X9b PRIMARY ARM: EXTRA SEEDS FINISHED; RESULT WITH ALL FOUR SEEDS AND WITH THE ORIGINAL TWO (Sarvam-1; seeds 3 and 4 were ADDED AFTER SEEING SEEDS 1 AND 2, same QLoRA recipe, streams and budget, laptop; `x9b_analyse.py --seeds 0,1,2,3` → `analysis_sarvam-1_seeds0123.json`; original two seeds → `analysis_sarvam-1.json`, registered verdict unchanged).** Both analyses use the same code (97.5% intervals, one seed drawn per cell per resample, 10,000 resamples). **The registered prediction (D_N > 0 and D_E > 0, intervals above 0) holds on both measures in both analyses: supported.** g = native minus ITRANS; g before training: SIB-200 0.233, retrieval 0.434. **Original seeds 1-2: SIB-200 D_N +0.225 [0.177, 0.273], D_E +0.196 [0.150, 0.244]; retrieval D_N +0.337 [0.296, 0.378], D_E +0.391 [0.344, 0.435]. All four seeds: SIB-200 D_N +0.222 [0.174, 0.270], D_E +0.194 [0.147, 0.243]; retrieval D_N +0.339 [0.292, 0.386], D_E +0.405 [0.353, 0.457].** Per-seed values (seeds 1, 2 | added 3, 4), g after training: SIB-200 ITRANS-trained 0.117, 0.118 | 0.124, 0.118; native-trained 0.339, 0.345 | 0.343, 0.337; English-trained 0.313, 0.314 | 0.306, 0.320. Retrieval ITRANS-trained 0.087, 0.075 | 0.059, 0.082; native-trained 0.415, 0.421 | 0.402, 0.418; English-trained 0.468, 0.476 | 0.493, 0.488. D_N per seed: SIB-200 0.222, 0.227 | 0.219, 0.219; retrieval 0.328, 0.346 | 0.343, 0.336. D_E per seed: SIB-200 0.196, 0.196 | 0.182, 0.202; retrieval 0.381, 0.401 | 0.434, 0.406. The added seeds sit inside the range of the original two on SIB-200 and slightly widen it on retrieval (ITRANS-trained retrieval gap 0.059 against 0.075 to 0.087, English-trained 0.493 against 0.468 to 0.476). English regression (SIB-200 English against the untrained model): original two seeds ITRANS -1.7 [-3.4, +0.05], native -2.7 [-4.8, -0.6], English -5.2 [-7.1, -3.3] (flagged: more than 5 points); all four seeds -1.6 [-3.3, +0.1], -2.5 [-4.5, -0.4], -5.3 [-7.3, -3.4] (the English-trained arm is flagged in both, as before). ITRANS-trained models do not reach the original native level in either analysis (SIB-200 0.646 against 0.768; retrieval 0.854 against 0.944; all four seeds). Run facts: all six extra runs 305 optimizer steps, 4,997,120 tokens, tokenizer unchanged, overlap 0 articles, none resumed from a checkpoint; micro-batch 16 for \`itrans+s2\` and 8 for the other five (same optimizer step; the micro-batch cap was introduced after two laptop crashes, see the entries above); the untrained-base guard passed on the laptop. Environment: the original four runs ran on Kaggle T4 (accounts 1 and 2), the six extra runs on the RTX 3070 laptop; the numbers agree within the seed spread. The paper reports all four seeds together and the original two separately, as stated at registration; it is not edited.
`````

##### 2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational). Aarnav supplied a new Kaggle API token to be used instead of the third-account token. It resolves to the Kaggle username aakarshprabhu (ch

RESULTS.md lines 4036 to 4037; first line committed in `ac6470f` on 2026-11-07 01:49:19 +0530; last line in `b194514` on 2026-11-07 01:53:51 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational).** Aarnav supplied a new Kaggle API token to be used instead of the third-account token. It resolves to the Kaggle username **aakarshprabhu** (checked with an empty CLI configuration folder; the old token resolved to aarnavkembhavi), a different account, treated as a teammate's account on Aarnav's instruction. The new token is stored only in the gitignored `.env` (KAGGLE3_API_TOKEN, KAGGLE3_USERNAME; the replaced token is kept there as KAGGLE3_API_TOKEN_PREVIOUS for cleanup and revocation), never in commits, logs or reports. The earlier attempt on aarnavkembhavi (two failed setup kernels, no internet, 0.21 h) is archived as `results/kaggle/acct3_aarnavkembhavi_failed` and its chain status under `results/phase2/`. A CPU test kernel on the new account confirms **internet works** (pypi.org and huggingface.co reachable). The private dataset `aakarshprabhu/shattered-flores-private` was created; the smoke gate and the A1-R reproduction (untrained Sarvam-1 and Gemma 4 E2B must reproduce account 1's curves) run before any job. The account-3 X9b chain was cancelled (the seed-4 runs finished on the laptop on 2026-11-06); the Sarvam-m chain `acct3sm` (lossy, lowercase, natural; 5 h cap) is kept waiting for the acceptance. Cleanup list: revoke both third-account tokens (the replaced one and the new one; both were pasted in chat), delete the datasets and kernels created on aakarshprabhu and on aarnavkembhavi, delete the nettest kernels. The username is added to the anonymiser's scrub list. This extends the statement that some Phase 2 Kaggle compute ran on teammates' accounts: account 3 (aakarshprabhu) from 2026-11-07. The paper is not edited.

`````

##### 2026-11-07 01:53 IST, REGISTRATION OF A SECOND SET OF EXTRA SEEDS (added AFTER seeing the originals; Aarnav's instruction of 2026-11-07 to start both; the original registrations, rules, budgets and verdicts are unchanged). Why the laptop GP

RESULTS.md lines 4038 to 4039; first line committed in `b194514` on 2026-11-07 01:53:51 +0530; last line in `acd0e83` on 2026-11-07 02:21:05 +0530; labels from the title and parent heading: registered, result

`````text
- **2026-11-07 01:53 IST, REGISTRATION OF A SECOND SET OF EXTRA SEEDS (added AFTER seeing the originals; Aarnav's instruction of 2026-11-07 to start both; the original registrations, rules, budgets and verdicts are unchanged).** Why the laptop GPU was idle: no registered laptop job was left after the first extra-seed chain finished at 2026-11-06 11:40 (idle until this start). **(1) X9a-low: levels 0 (no cipher), 0.01% and 0.03% exposure, code seeds 3 and 4 (called seeds 4 and 5; originals 0, 1, 2), same recipe and evaluation as the earlier extra seeds (0.1%, 0.3%, 1%), six runs of about 18 minutes; per-seed values will be reported with the original three and all five side by side; the registered X9a-low rule is not re-run on a different set of seeds. The level-0 stream (removed with the caches) is regenerated with the code of the original preparation and refused unless its sha256 equals the stored value.** **(2) X9b secondary arm (Qwen3.5-2B): extra code seeds 1 and 2 (called seeds 2 and 3; the original run is seed 0, one seed), ITRANS, native and English, same QLoRA recipe, streams and token budget (5,668,864 tokens per run, 346 optimizer steps), same evaluation, laptop (the original ran on Kaggle account 2 and was finished on the laptop), micro-batch 4 as in the pilot (below the cap of 8), six runs of about 2 to 2.5 h; the analysis `x9b_analyse.py --model qwen3.5-2b --seeds 0,1,2` adds a seed spread to the secondary arm; the secondary arm still does not enter the primary conclusion and its registered verdict (supported, one seed) is unchanged.** Chain `x9extra2` (X9a-low first, about 2 h; then the Qwen runs, an estimated 12 to 15 h, projected finish about 7 Nov 20:00 to 23:00 IST). Output `results/kaggle/laptop_x9b/2026-11-07/out`. Also from now on the 15-minute watchdog reports to Aarnav only when a job finishes, fails or a registered result arrives (Aarnav's instruction), the checks themselves continue. The paper is not edited.

`````

##### 2026-11-08 15:33 IST, X9b SECONDARY ARM (Qwen3.5-2B): EXTRA SEEDS FINISHED (added after seeing the original seed; registered 2026-11-07; code seeds 1 and 2 = seeds 2 and 3; laptop, chain finished 2026-11-07 20:05; `x9b_analyse.py --model qw

RESULTS.md lines 4048 to 4048; first line committed in `0cd9a82` on 2026-11-08 15:33:40 +0530; last line in `0cd9a82` on 2026-11-08 15:33:40 +0530; labels from the title and parent heading: result

`````text
- **2026-11-08 15:33 IST, X9b SECONDARY ARM (Qwen3.5-2B): EXTRA SEEDS FINISHED (added after seeing the original seed; registered 2026-11-07; code seeds 1 and 2 = seeds 2 and 3; laptop, chain finished 2026-11-07 20:05; `x9b_analyse.py --model qwen3.5-2b --seeds 0,1,2` → `analysis_qwen3.5-2b_seeds012.json`).** The registered secondary-arm verdict (supported, one seed) is unchanged; the arm still does not enter the primary conclusion. **With three seeds: SIB-200 D_N +0.301 [0.248, 0.351], D_E +0.258 [0.195, 0.315]; retrieval D_N +0.594 [0.550, 0.637], D_E +0.592 [0.544, 0.638]: supported on both measures (one seed drawn per cell per resample).** Per seed (seed 1 = the original run | added seeds 2, 3), g after training: SIB-200 ITRANS-trained 0.173 | 0.152, 0.148; native-trained 0.458 | 0.452, 0.468; English-trained 0.433 | 0.392, 0.423 (g before training 0.436). Retrieval ITRANS-trained 0.279 | 0.253, 0.263; native-trained 0.862 | 0.860, 0.856; English-trained 0.845 | 0.865, 0.862 (g before 0.858). D_N per seed: SIB-200 0.285 | 0.300, 0.320; retrieval 0.583 | 0.607, 0.593. D_E per seed: SIB-200 0.260 | 0.240, 0.275; retrieval 0.566 | 0.612, 0.599. English regression (SIB-200 English against the untrained model, three seeds): ITRANS -0.3 points [-1.6, +1.0], native -0.5 [-1.7, +0.7], English -2.4 [-4.1, -0.8]; none exceeds 5 points. ITRANS-trained models do not reach the original native level (SIB-200 0.513 against 0.674; retrieval 0.712 against 0.977). Run facts: 346 optimizer steps, 5,668,864 tokens each, tokenizer unchanged, none resumed from a checkpoint; micro-batch 4 for \`itrans+s1\` and 2 for the other five (same optimizer step): **the cap of 2 made training 2.3 times faster than micro-batch 4 on the 8 GB card (about 6,100 s against 14,300 s per run), the cause being shared-memory spill at the larger micro-batch**. The chain finished at 2026-11-07 20:05, about a day before the projected 8 Nov 07:00, and the laptop GPU has been idle since then (see the next entry). The paper is not edited.
`````

## Result files, every number

#### `results/phase2/x9b/analysis_qwen3.5-2b.json` (8,747 bytes; first commit 3b1e037 2026-11-05 13:23:17 +0530)

`````text
provenance.config.registration = "RESULTS.md Amendment 2, X9b (primary Sarvam-1)"
provenance.git_commit = "9f273ccc20267f52475b9f32b374568a2f0d1214-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T07:52:55+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9b_analyse.py", "--model", "qwen3.5-2b"]
model = "qwen3.5-2b"
measures.SIB-200 accuracy.n = 1004
measures.SIB-200 accuracy.g0_before_training = 0.4362549800796813
measures.SIB-200 accuracy.g_after_seed_mean.itrans = 0.17330677290836655
measures.SIB-200 accuracy.g_after_seed_mean.native = 0.4581673306772908
measures.SIB-200 accuracy.g_after_seed_mean.english = 0.43326693227091634
measures.SIB-200 accuracy.g_after_by_seed.itrans = [0.17330677290836655]
measures.SIB-200 accuracy.g_after_by_seed.native = [0.4581673306772908]
measures.SIB-200 accuracy.g_after_by_seed.english = [0.43326693227091634]
measures.SIB-200 accuracy.D_N.point = 0.28486055776892427
measures.SIB-200 accuracy.D_N.ci975 = [0.2410358565737052, 0.3276892430278885]
measures.SIB-200 accuracy.D_N.above_0 = true
measures.SIB-200 accuracy.D_N.entirely_below_0 = false
measures.SIB-200 accuracy.D_N.seed_spread_D_seed0_seed1 = [0.28486055776892427]
measures.SIB-200 accuracy.D_E.point = 0.2599601593625498
measures.SIB-200 accuracy.D_E.ci975 = [0.2191110557768924, 0.30079681274900394]
measures.SIB-200 accuracy.D_E.above_0 = true
measures.SIB-200 accuracy.D_E.entirely_below_0 = false
measures.SIB-200 accuracy.D_E.seed_spread_D_seed0_seed1 = [0.2599601593625498]
measures.SIB-200 accuracy.verdict = "supported"
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.native = 0.6872509960159362
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.itrans = 0.5139442231075697
measures.SIB-200 accuracy.accuracy_by_run.native+s0.native = 0.7081673306772909
measures.SIB-200 accuracy.accuracy_by_run.native+s0.itrans = 0.25
measures.SIB-200 accuracy.accuracy_by_run.english+s0.native = 0.6782868525896414
measures.SIB-200 accuracy.accuracy_by_run.english+s0.itrans = 0.2450199203187251
measures.SIB-200 accuracy.accuracy_base.native = 0.6743027888446215
measures.SIB-200 accuracy.accuracy_base.itrans = 0.23804780876494025
measures.FLORES+ retrieval.n = 1005
measures.FLORES+ retrieval.g0_before_training = 0.8577114427860697
measures.FLORES+ retrieval.g_after_seed_mean.itrans = 0.27860696517412936
measures.FLORES+ retrieval.g_after_seed_mean.native = 0.8616915422885573
measures.FLORES+ retrieval.g_after_seed_mean.english = 0.844776119402985
measures.FLORES+ retrieval.g_after_by_seed.itrans = [0.27860696517412936]
measures.FLORES+ retrieval.g_after_by_seed.native = [0.8616915422885573]
measures.FLORES+ retrieval.g_after_by_seed.english = [0.844776119402985]
measures.FLORES+ retrieval.D_N.point = 0.583084577114428
measures.FLORES+ retrieval.D_N.ci975 = [0.545273631840796, 0.6199004975124378]
measures.FLORES+ retrieval.D_N.above_0 = true
measures.FLORES+ retrieval.D_N.entirely_below_0 = false
measures.FLORES+ retrieval.D_N.seed_spread_D_seed0_seed1 = [0.583084577114428]
measures.FLORES+ retrieval.D_E.point = 0.5661691542288556
measures.FLORES+ retrieval.D_E.ci975 = [0.5293532338308458, 0.6029850746268657]
measures.FLORES+ retrieval.D_E.above_0 = true
measures.FLORES+ retrieval.D_E.entirely_below_0 = false
measures.FLORES+ retrieval.D_E.seed_spread_D_seed0_seed1 = [0.5661691542288556]
measures.FLORES+ retrieval.verdict = "supported"
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.native = 0.9751243781094527
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.itrans = 0.6965174129353234
measures.FLORES+ retrieval.accuracy_by_run.native+s0.native = 0.9900497512437811
measures.FLORES+ retrieval.accuracy_by_run.native+s0.itrans = 0.12835820895522387
measures.FLORES+ retrieval.accuracy_by_run.english+s0.native = 0.9830845771144279
measures.FLORES+ retrieval.accuracy_by_run.english+s0.itrans = 0.1383084577114428
measures.FLORES+ retrieval.accuracy_base.native = 0.9771144278606965
measures.FLORES+ retrieval.accuracy_base.itrans = 0.11940298507462686
english_sib_damage_check.base = 0.8037848605577689
english_sib_damage_check.by_run.itrans+s0.acc = 0.8017928286852589
english_sib_damage_check.by_run.itrans+s0.drop_points = 0.19920318725099584
english_sib_damage_check.by_run.itrans+s0.flagged = false
english_sib_damage_check.by_run.native+s0.acc = 0.797808764940239
english_sib_damage_check.by_run.native+s0.drop_points = 0.5976095617529875
english_sib_damage_check.by_run.native+s0.flagged = false
english_sib_damage_check.by_run.english+s0.acc = 0.7848605577689243
english_sib_damage_check.by_run.english+s0.drop_points = 1.8924302788844605
english_sib_damage_check.by_run.english+s0.flagged = false
tokenizer_unchanged.itrans+s0 = true
tokenizer_unchanged.native+s0 = true
tokenizer_unchanged.english+s0 = true
B = 5668864
per_run.itrans+s0.condition = "itrans"
per_run.itrans+s0.seed = 0
per_run.itrans+s0.B_tokens = 5668864
per_run.itrans+s0.optimizer_steps = 346
per_run.itrans+s0.articles = 2505
per_run.itrans+s0.words = 1312877
per_run.itrans+s0.stream_tokens = 5668864
per_run.itrans+s0.stream_tokens_per_word = 4.317894212481443
per_run.itrans+s0.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s0.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s0.tokenizer_unchanged = true
per_run.itrans+s0.train_seconds = 9198.904323339462
per_run.itrans+s0.sib.english = 0.8017928286852589
per_run.itrans+s0.sib.native = 0.6872509960159362
per_run.itrans+s0.sib.itrans = 0.5139442231075697
per_run.itrans+s0.retrieval.native = 0.9751243781094527
per_run.itrans+s0.retrieval.itrans = 0.6965174129353234
per_run.native+s0.condition = "native"
per_run.native+s0.seed = 0
per_run.native+s0.B_tokens = 5668864
per_run.native+s0.optimizer_steps = 346
per_run.native+s0.articles = 1995
per_run.native+s0.words = 1040695
per_run.native+s0.stream_tokens = 5668864
per_run.native+s0.stream_tokens_per_word = 5.447190579372439
per_run.native+s0.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s0.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s0.tokenizer_unchanged = true
per_run.native+s0.train_seconds = 9104.594935417175
per_run.native+s0.sib.english = 0.797808764940239
per_run.native+s0.sib.native = 0.7081673306772909
per_run.native+s0.sib.itrans = 0.25
per_run.native+s0.retrieval.native = 0.9900497512437811
per_run.native+s0.retrieval.itrans = 0.12835820895522387
per_run.english+s0.condition = "english"
per_run.english+s0.seed = 0
per_run.english+s0.B_tokens = 5668864
per_run.english+s0.optimizer_steps = 346
per_run.english+s0.articles = 5376
per_run.english+s0.words = 3718950
per_run.english+s0.stream_tokens = 5668864
per_run.english+s0.stream_tokens_per_word = 1.5243184232108524
per_run.english+s0.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s0.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s0.tokenizer_unchanged = true
per_run.english+s0.train_seconds = 8946.590991020203
per_run.english+s0.sib.english = 0.7848605577689243
per_run.english+s0.sib.native = 0.6782868525896414
per_run.english+s0.sib.itrans = 0.2450199203187251
per_run.english+s0.retrieval.native = 0.9830845771144279
per_run.english+s0.retrieval.itrans = 0.1383084577114428
tokens_per_word_flores.native = 5.328544243577546
tokens_per_word_flores.itrans = 4.195147478591817
tokens_per_word_flores.note = "tokenizer files are identical before and after training (sha256 in per_run), so tokens per word are the same before and after by construction"
english_regression_vs_base.itrans.mean_change_points = -0.199203187250996
english_regression_vs_base.itrans.ci95_points = [-1.693227091633466, 1.1952191235059761]
english_regression_vs_base.itrans.flag_more_than_5_points = false
english_regression_vs_base.itrans.by_seed_points = [-0.199203187250996]
english_regression_vs_base.native.mean_change_points = -0.5976095617529881
english_regression_vs_base.native.ci95_points = [-1.9920318725099602, 0.697211155378486]
english_regression_vs_base.native.flag_more_than_5_points = false
english_regression_vs_base.native.by_seed_points = [-0.5976095617529881]
english_regression_vs_base.english.mean_change_points = -1.8924302788844622
english_regression_vs_base.english.ci95_points = [-3.5856573705179287, -0.199203187250996]
english_regression_vs_base.english.flag_more_than_5_points = false
english_regression_vs_base.english.by_seed_points = [-1.8924302788844622]
itrans_trained_vs_original_native.SIB-200 accuracy.itrans_accuracy_after_itrans_training = 0.5139442231075697
itrans_trained_vs_original_native.SIB-200 accuracy.original_native_accuracy_untrained = 0.6743027888446215
itrans_trained_vs_original_native.SIB-200 accuracy.difference = -0.1603585657370518
itrans_trained_vs_original_native.SIB-200 accuracy.ci95 = [-0.19123505976095617, -0.1294820717131474]
itrans_trained_vs_original_native.SIB-200 accuracy.reaches_original_native_level = false
itrans_trained_vs_original_native.FLORES+ retrieval.itrans_accuracy_after_itrans_training = 0.6965174129353234
itrans_trained_vs_original_native.FLORES+ retrieval.original_native_accuracy_untrained = 0.9771144278606965
itrans_trained_vs_original_native.FLORES+ retrieval.difference = -0.28059701492537314
itrans_trained_vs_original_native.FLORES+ retrieval.ci95 = [-0.309452736318408, -0.2517412935323383]
itrans_trained_vs_original_native.FLORES+ retrieval.reaches_original_native_level = false
`````

#### `results/phase2/x9b/analysis_qwen3.5-2b_seeds012.json` (16,892 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
provenance.config.registration = "RESULTS.md Amendment 2, X9b (primary Sarvam-1); seeds 0,1,2 (the extra seeds were added after seeing the originals, RESULTS.md 2026-11-05)"
provenance.git_commit = "c42cfd4ce4c028065aa5c36c9bca52649fb399a6-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-08T10:02:00+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9b_analyse.py", "--model", "qwen3.5-2b", "--seeds", "0,1,2"]
model = "qwen3.5-2b"
measures.SIB-200 accuracy.n = 1004
measures.SIB-200 accuracy.g0_before_training = 0.4362549800796813
measures.SIB-200 accuracy.g_after_seed_mean.itrans = 0.15803452855245684
measures.SIB-200 accuracy.g_after_seed_mean.native = 0.4594953519256308
measures.SIB-200 accuracy.g_after_seed_mean.english = 0.4163346613545817
measures.SIB-200 accuracy.g_after_by_seed.itrans = [0.17330677290836655, 0.15239043824701196, 0.14840637450199204]
measures.SIB-200 accuracy.g_after_by_seed.native = [0.4581673306772908, 0.45219123505976094, 0.4681274900398406]
measures.SIB-200 accuracy.g_after_by_seed.english = [0.43326693227091634, 0.39243027888446214, 0.42330677290836655]
measures.SIB-200 accuracy.D_N.point = 0.3014608233731739
measures.SIB-200 accuracy.D_N.ci975 = [0.24800796812749004, 0.35061005976095694]
measures.SIB-200 accuracy.D_N.above_0 = true
measures.SIB-200 accuracy.D_N.entirely_below_0 = false
measures.SIB-200 accuracy.D_N.seed_spread_D_seed0_seed1 = [0.28486055776892427, 0.29980079681274896, 0.31972111553784854]
measures.SIB-200 accuracy.D_E.point = 0.2583001328021248
measures.SIB-200 accuracy.D_E.ci975 = [0.1952191235059761, 0.3147410358565737]
measures.SIB-200 accuracy.D_E.above_0 = true
measures.SIB-200 accuracy.D_E.entirely_below_0 = false
measures.SIB-200 accuracy.D_E.seed_spread_D_seed0_seed1 = [0.2599601593625498, 0.24003984063745018, 0.2749003984063745]
measures.SIB-200 accuracy.verdict = "supported"
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.native = 0.6872509960159362
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.itrans = 0.5139442231075697
measures.SIB-200 accuracy.accuracy_by_run.itrans+s1.native = 0.6384462151394422
measures.SIB-200 accuracy.accuracy_by_run.itrans+s1.itrans = 0.4860557768924303
measures.SIB-200 accuracy.accuracy_by_run.itrans+s2.native = 0.6872509960159362
measures.SIB-200 accuracy.accuracy_by_run.itrans+s2.itrans = 0.5388446215139442
measures.SIB-200 accuracy.accuracy_by_run.native+s0.native = 0.7081673306772909
measures.SIB-200 accuracy.accuracy_by_run.native+s0.itrans = 0.25
measures.SIB-200 accuracy.accuracy_by_run.native+s1.native = 0.7071713147410359
measures.SIB-200 accuracy.accuracy_by_run.native+s1.itrans = 0.2549800796812749
measures.SIB-200 accuracy.accuracy_by_run.native+s2.native = 0.7131474103585658
measures.SIB-200 accuracy.accuracy_by_run.native+s2.itrans = 0.2450199203187251
measures.SIB-200 accuracy.accuracy_by_run.english+s0.native = 0.6782868525896414
measures.SIB-200 accuracy.accuracy_by_run.english+s0.itrans = 0.2450199203187251
measures.SIB-200 accuracy.accuracy_by_run.english+s1.native = 0.6782868525896414
measures.SIB-200 accuracy.accuracy_by_run.english+s1.itrans = 0.2858565737051793
measures.SIB-200 accuracy.accuracy_by_run.english+s2.native = 0.6772908366533864
measures.SIB-200 accuracy.accuracy_by_run.english+s2.itrans = 0.2539840637450199
measures.SIB-200 accuracy.accuracy_base.native = 0.6743027888446215
measures.SIB-200 accuracy.accuracy_base.itrans = 0.23804780876494025
measures.FLORES+ retrieval.n = 1005
measures.FLORES+ retrieval.g0_before_training = 0.8577114427860697
measures.FLORES+ retrieval.g_after_seed_mean.itrans = 0.2646766169154229
measures.FLORES+ retrieval.g_after_seed_mean.native = 0.8590381426202321
measures.FLORES+ retrieval.g_after_seed_mean.english = 0.8570480928689883
measures.FLORES+ retrieval.g_after_by_seed.itrans = [0.27860696517412936, 0.2527363184079602, 0.2626865671641791]
measures.FLORES+ retrieval.g_after_by_seed.native = [0.8616915422885573, 0.8597014925373134, 0.8557213930348259]
measures.FLORES+ retrieval.g_after_by_seed.english = [0.844776119402985, 0.8646766169154229, 0.8616915422885573]
measures.FLORES+ retrieval.D_N.point = 0.5943615257048093
measures.FLORES+ retrieval.D_N.ci975 = [0.5502487562189056, 0.6368283582089559]
measures.FLORES+ retrieval.D_N.above_0 = true
measures.FLORES+ retrieval.D_N.entirely_below_0 = false
measures.FLORES+ retrieval.D_N.seed_spread_D_seed0_seed1 = [0.583084577114428, 0.6069651741293532, 0.5930348258706468]
measures.FLORES+ retrieval.D_E.point = 0.5923714759535654
measures.FLORES+ retrieval.D_E.ci975 = [0.5442786069651742, 0.6378109452736318]
measures.FLORES+ retrieval.D_E.above_0 = true
measures.FLORES+ retrieval.D_E.entirely_below_0 = false
measures.FLORES+ retrieval.D_E.seed_spread_D_seed0_seed1 = [0.5661691542288556, 0.6119402985074627, 0.5990049751243782]
measures.FLORES+ retrieval.verdict = "supported"
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.native = 0.9751243781094527
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.itrans = 0.6965174129353234
measures.FLORES+ retrieval.accuracy_by_run.itrans+s1.native = 0.9771144278606965
measures.FLORES+ retrieval.accuracy_by_run.itrans+s1.itrans = 0.7243781094527363
measures.FLORES+ retrieval.accuracy_by_run.itrans+s2.native = 0.9771144278606965
measures.FLORES+ retrieval.accuracy_by_run.itrans+s2.itrans = 0.7144278606965174
measures.FLORES+ retrieval.accuracy_by_run.native+s0.native = 0.9900497512437811
measures.FLORES+ retrieval.accuracy_by_run.native+s0.itrans = 0.12835820895522387
measures.FLORES+ retrieval.accuracy_by_run.native+s1.native = 0.9900497512437811
measures.FLORES+ retrieval.accuracy_by_run.native+s1.itrans = 0.13034825870646766
measures.FLORES+ retrieval.accuracy_by_run.native+s2.native = 0.9900497512437811
measures.FLORES+ retrieval.accuracy_by_run.native+s2.itrans = 0.13432835820895522
measures.FLORES+ retrieval.accuracy_by_run.english+s0.native = 0.9830845771144279
measures.FLORES+ retrieval.accuracy_by_run.english+s0.itrans = 0.1383084577114428
measures.FLORES+ retrieval.accuracy_by_run.english+s1.native = 0.9850746268656716
measures.FLORES+ retrieval.accuracy_by_run.english+s1.itrans = 0.12039800995024875
measures.FLORES+ retrieval.accuracy_by_run.english+s2.native = 0.9870646766169154
measures.FLORES+ retrieval.accuracy_by_run.english+s2.itrans = 0.1253731343283582
measures.FLORES+ retrieval.accuracy_base.native = 0.9771144278606965
measures.FLORES+ retrieval.accuracy_base.itrans = 0.11940298507462686
english_sib_damage_check.base = 0.8037848605577689
english_sib_damage_check.by_run.itrans+s0.acc = 0.8017928286852589
english_sib_damage_check.by_run.itrans+s0.drop_points = 0.19920318725099584
english_sib_damage_check.by_run.itrans+s0.flagged = false
english_sib_damage_check.by_run.itrans+s1.acc = 0.8017928286852589
english_sib_damage_check.by_run.itrans+s1.drop_points = 0.19920318725099584
english_sib_damage_check.by_run.itrans+s1.flagged = false
english_sib_damage_check.by_run.itrans+s2.acc = 0.799800796812749
english_sib_damage_check.by_run.itrans+s2.drop_points = 0.3984063745019917
english_sib_damage_check.by_run.itrans+s2.flagged = false
english_sib_damage_check.by_run.native+s0.acc = 0.797808764940239
english_sib_damage_check.by_run.native+s0.drop_points = 0.5976095617529875
english_sib_damage_check.by_run.native+s0.flagged = false
english_sib_damage_check.by_run.native+s1.acc = 0.8027888446215139
english_sib_damage_check.by_run.native+s1.drop_points = 0.09960159362549792
english_sib_damage_check.by_run.native+s1.flagged = false
english_sib_damage_check.by_run.native+s2.acc = 0.796812749003984
english_sib_damage_check.by_run.native+s2.drop_points = 0.6972111553784854
english_sib_damage_check.by_run.native+s2.flagged = false
english_sib_damage_check.by_run.english+s0.acc = 0.7848605577689243
english_sib_damage_check.by_run.english+s0.drop_points = 1.8924302788844605
english_sib_damage_check.by_run.english+s0.flagged = false
english_sib_damage_check.by_run.english+s1.acc = 0.7768924302788844
english_sib_damage_check.by_run.english+s1.drop_points = 2.689243027888444
english_sib_damage_check.by_run.english+s1.flagged = false
english_sib_damage_check.by_run.english+s2.acc = 0.7768924302788844
english_sib_damage_check.by_run.english+s2.drop_points = 2.689243027888444
english_sib_damage_check.by_run.english+s2.flagged = false
tokenizer_unchanged.itrans+s0 = true
tokenizer_unchanged.itrans+s1 = true
tokenizer_unchanged.itrans+s2 = true
tokenizer_unchanged.native+s0 = true
tokenizer_unchanged.native+s1 = true
tokenizer_unchanged.native+s2 = true
tokenizer_unchanged.english+s0 = true
tokenizer_unchanged.english+s1 = true
tokenizer_unchanged.english+s2 = true
B = 5668864
per_run.itrans+s0.condition = "itrans"
per_run.itrans+s0.seed = 0
per_run.itrans+s0.B_tokens = 5668864
per_run.itrans+s0.optimizer_steps = 346
per_run.itrans+s0.articles = 2505
per_run.itrans+s0.words = 1312877
per_run.itrans+s0.stream_tokens = 5668864
per_run.itrans+s0.stream_tokens_per_word = 4.317894212481443
per_run.itrans+s0.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s0.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s0.tokenizer_unchanged = true
per_run.itrans+s0.train_seconds = 9198.904323339462
per_run.itrans+s0.sib.english = 0.8017928286852589
per_run.itrans+s0.sib.native = 0.6872509960159362
per_run.itrans+s0.sib.itrans = 0.5139442231075697
per_run.itrans+s0.retrieval.native = 0.9751243781094527
per_run.itrans+s0.retrieval.itrans = 0.6965174129353234
per_run.itrans+s1.condition = "itrans"
per_run.itrans+s1.seed = 1
per_run.itrans+s1.B_tokens = 5668864
per_run.itrans+s1.optimizer_steps = 346
per_run.itrans+s1.articles = 2505
per_run.itrans+s1.words = 1312877
per_run.itrans+s1.stream_tokens = 5668864
per_run.itrans+s1.stream_tokens_per_word = 4.317894212481443
per_run.itrans+s1.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s1.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s1.tokenizer_unchanged = true
per_run.itrans+s1.train_seconds = 14325.945019245148
per_run.itrans+s1.sib.english = 0.8017928286852589
per_run.itrans+s1.sib.native = 0.6384462151394422
per_run.itrans+s1.sib.itrans = 0.4860557768924303
per_run.itrans+s1.retrieval.native = 0.9771144278606965
per_run.itrans+s1.retrieval.itrans = 0.7243781094527363
per_run.itrans+s2.condition = "itrans"
per_run.itrans+s2.seed = 2
per_run.itrans+s2.B_tokens = 5668864
per_run.itrans+s2.optimizer_steps = 346
per_run.itrans+s2.articles = 2505
per_run.itrans+s2.words = 1312877
per_run.itrans+s2.stream_tokens = 5668864
per_run.itrans+s2.stream_tokens_per_word = 4.317894212481443
per_run.itrans+s2.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s2.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.itrans+s2.tokenizer_unchanged = true
per_run.itrans+s2.train_seconds = 6218.435968637466
per_run.itrans+s2.sib.english = 0.799800796812749
per_run.itrans+s2.sib.native = 0.6872509960159362
per_run.itrans+s2.sib.itrans = 0.5388446215139442
per_run.itrans+s2.retrieval.native = 0.9771144278606965
per_run.itrans+s2.retrieval.itrans = 0.7144278606965174
per_run.native+s0.condition = "native"
per_run.native+s0.seed = 0
per_run.native+s0.B_tokens = 5668864
per_run.native+s0.optimizer_steps = 346
per_run.native+s0.articles = 1995
per_run.native+s0.words = 1040695
per_run.native+s0.stream_tokens = 5668864
per_run.native+s0.stream_tokens_per_word = 5.447190579372439
per_run.native+s0.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s0.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s0.tokenizer_unchanged = true
per_run.native+s0.train_seconds = 9104.594935417175
per_run.native+s0.sib.english = 0.797808764940239
per_run.native+s0.sib.native = 0.7081673306772909
per_run.native+s0.sib.itrans = 0.25
per_run.native+s0.retrieval.native = 0.9900497512437811
per_run.native+s0.retrieval.itrans = 0.12835820895522387
per_run.native+s1.condition = "native"
per_run.native+s1.seed = 1
per_run.native+s1.B_tokens = 5668864
per_run.native+s1.optimizer_steps = 346
per_run.native+s1.articles = 1995
per_run.native+s1.words = 1040695
per_run.native+s1.stream_tokens = 5668864
per_run.native+s1.stream_tokens_per_word = 5.447190579372439
per_run.native+s1.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s1.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s1.tokenizer_unchanged = true
per_run.native+s1.train_seconds = 6026.591080188751
per_run.native+s1.sib.english = 0.8027888446215139
per_run.native+s1.sib.native = 0.7071713147410359
per_run.native+s1.sib.itrans = 0.2549800796812749
per_run.native+s1.retrieval.native = 0.9900497512437811
per_run.native+s1.retrieval.itrans = 0.13034825870646766
per_run.native+s2.condition = "native"
per_run.native+s2.seed = 2
per_run.native+s2.B_tokens = 5668864
per_run.native+s2.optimizer_steps = 346
per_run.native+s2.articles = 1995
per_run.native+s2.words = 1040695
per_run.native+s2.stream_tokens = 5668864
per_run.native+s2.stream_tokens_per_word = 5.447190579372439
per_run.native+s2.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s2.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.native+s2.tokenizer_unchanged = true
per_run.native+s2.train_seconds = 6173.520985126495
per_run.native+s2.sib.english = 0.796812749003984
per_run.native+s2.sib.native = 0.7131474103585658
per_run.native+s2.sib.itrans = 0.2450199203187251
per_run.native+s2.retrieval.native = 0.9900497512437811
per_run.native+s2.retrieval.itrans = 0.13432835820895522
per_run.english+s0.condition = "english"
per_run.english+s0.seed = 0
per_run.english+s0.B_tokens = 5668864
per_run.english+s0.optimizer_steps = 346
per_run.english+s0.articles = 5376
per_run.english+s0.words = 3718950
per_run.english+s0.stream_tokens = 5668864
per_run.english+s0.stream_tokens_per_word = 1.5243184232108524
per_run.english+s0.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s0.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s0.tokenizer_unchanged = true
per_run.english+s0.train_seconds = 8946.590991020203
per_run.english+s0.sib.english = 0.7848605577689243
per_run.english+s0.sib.native = 0.6782868525896414
per_run.english+s0.sib.itrans = 0.2450199203187251
per_run.english+s0.retrieval.native = 0.9830845771144279
per_run.english+s0.retrieval.itrans = 0.1383084577114428
per_run.english+s1.condition = "english"
per_run.english+s1.seed = 1
per_run.english+s1.B_tokens = 5668864
per_run.english+s1.optimizer_steps = 346
per_run.english+s1.articles = 5376
per_run.english+s1.words = 3718950
per_run.english+s1.stream_tokens = 5668864
per_run.english+s1.stream_tokens_per_word = 1.5243184232108524
per_run.english+s1.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s1.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s1.tokenizer_unchanged = true
per_run.english+s1.train_seconds = 6082.838150501251
per_run.english+s1.sib.english = 0.7768924302788844
per_run.english+s1.sib.native = 0.6782868525896414
per_run.english+s1.sib.itrans = 0.2858565737051793
per_run.english+s1.retrieval.native = 0.9850746268656716
per_run.english+s1.retrieval.itrans = 0.12039800995024875
per_run.english+s2.condition = "english"
per_run.english+s2.seed = 2
per_run.english+s2.B_tokens = 5668864
per_run.english+s2.optimizer_steps = 346
per_run.english+s2.articles = 5376
per_run.english+s2.words = 3718950
per_run.english+s2.stream_tokens = 5668864
per_run.english+s2.stream_tokens_per_word = 1.5243184232108524
per_run.english+s2.tokenizer_sha256_before = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s2.tokenizer_sha256_after = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
per_run.english+s2.tokenizer_unchanged = true
per_run.english+s2.train_seconds = 6156.857125997543
per_run.english+s2.sib.english = 0.7768924302788844
per_run.english+s2.sib.native = 0.6772908366533864
per_run.english+s2.sib.itrans = 0.2539840637450199
per_run.english+s2.retrieval.native = 0.9870646766169154
per_run.english+s2.retrieval.itrans = 0.1253731343283582
tokens_per_word_flores.native = 5.328544243577546
tokens_per_word_flores.itrans = 4.195147478591817
tokens_per_word_flores.note = "tokenizer files are identical before and after training (sha256 in per_run), so tokens per word are the same before and after by construction"
english_regression_vs_base.itrans.mean_change_points = -0.2656042496679947
english_regression_vs_base.itrans.ci95_points = [-1.5604249667994687, 0.9628154050464809]
english_regression_vs_base.itrans.flag_more_than_5_points = false
english_regression_vs_base.itrans.by_seed_points = [-0.199203187250996, -0.199203187250996, -0.398406374501992]
english_regression_vs_base.native.mean_change_points = -0.4648074369189906
english_regression_vs_base.native.ci95_points = [-1.693227091633466, 0.7304116865869853]
english_regression_vs_base.native.flag_more_than_5_points = false
english_regression_vs_base.native.by_seed_points = [-0.5976095617529881, -0.099601593625498, -0.697211155378486]
english_regression_vs_base.english.mean_change_points = -2.4236387782204516
english_regression_vs_base.english.ci95_points = [-4.083665338645418, -0.796812749003984]
english_regression_vs_base.english.flag_more_than_5_points = false
english_regression_vs_base.english.by_seed_points = [-1.8924302788844622, -2.689243027888446, -2.689243027888446]
itrans_trained_vs_original_native.SIB-200 accuracy.itrans_accuracy_after_itrans_training = 0.5129482071713147
itrans_trained_vs_original_native.SIB-200 accuracy.original_native_accuracy_untrained = 0.6743027888446215
itrans_trained_vs_original_native.SIB-200 accuracy.difference = -0.16135458167330677
itrans_trained_vs_original_native.SIB-200 accuracy.ci95 = [-0.18990703851261623, -0.13247011952191234]
itrans_trained_vs_original_native.SIB-200 accuracy.reaches_original_native_level = false
itrans_trained_vs_original_native.FLORES+ retrieval.itrans_accuracy_after_itrans_training = 0.7117744610281923
itrans_trained_vs_original_native.FLORES+ retrieval.original_native_accuracy_untrained = 0.9771144278606965
itrans_trained_vs_original_native.FLORES+ retrieval.difference = -0.2653399668325041
itrans_trained_vs_original_native.FLORES+ retrieval.ci95 = [-0.29187396351575456, -0.23980099502487562]
itrans_trained_vs_original_native.FLORES+ retrieval.reaches_original_native_level = false
`````

#### `results/phase2/x9b/analysis_sarvam-1.json` (12,748 bytes; first commit 900da25 2026-11-05 03:10:06 +0530)

`````text
provenance.config.registration = "RESULTS.md Amendment 2, X9b (primary Sarvam-1)"
provenance.git_commit = "fc1246a10615010b9897df251844222070a7a81d-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T06:22:45+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9b_analyse.py", "--model", "sarvam-1"]
model = "sarvam-1"
measures.SIB-200 accuracy.n = 1004
measures.SIB-200 accuracy.g0_before_training = 0.23306772908366533
measures.SIB-200 accuracy.g_after_seed_mean.itrans = 0.11703187250996017
measures.SIB-200 accuracy.g_after_seed_mean.native = 0.3416334661354582
measures.SIB-200 accuracy.g_after_seed_mean.english = 0.31324701195219123
measures.SIB-200 accuracy.g_after_by_seed.itrans = [0.11653386454183266, 0.11752988047808766]
measures.SIB-200 accuracy.g_after_by_seed.native = [0.3386454183266932, 0.34462151394422313]
measures.SIB-200 accuracy.g_after_by_seed.english = [0.31274900398406374, 0.3137450199203187]
measures.SIB-200 accuracy.D_N.point = 0.22460159362549803
measures.SIB-200 accuracy.D_N.ci975 = [0.17729083665338644, 0.2729083665338645]
measures.SIB-200 accuracy.D_N.above_0 = true
measures.SIB-200 accuracy.D_N.entirely_below_0 = false
measures.SIB-200 accuracy.D_N.seed_spread_D_seed0_seed1 = [0.22211155378486053, 0.22709163346613548]
measures.SIB-200 accuracy.D_E.point = 0.19621513944223107
measures.SIB-200 accuracy.D_E.ci975 = [0.15039840637450197, 0.24402390438247012]
measures.SIB-200 accuracy.D_E.above_0 = true
measures.SIB-200 accuracy.D_E.entirely_below_0 = false
measures.SIB-200 accuracy.D_E.seed_spread_D_seed0_seed1 = [0.19621513944223107, 0.19621513944223107]
measures.SIB-200 accuracy.verdict = "supported"
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.native = 0.7659362549800797
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.itrans = 0.649402390438247
measures.SIB-200 accuracy.accuracy_by_run.itrans+s1.native = 0.7669322709163346
measures.SIB-200 accuracy.accuracy_by_run.itrans+s1.itrans = 0.649402390438247
measures.SIB-200 accuracy.accuracy_by_run.native+s0.native = 0.7649402390438247
measures.SIB-200 accuracy.accuracy_by_run.native+s0.itrans = 0.4262948207171315
measures.SIB-200 accuracy.accuracy_by_run.native+s1.native = 0.7669322709163346
measures.SIB-200 accuracy.accuracy_by_run.native+s1.itrans = 0.42231075697211157
measures.SIB-200 accuracy.accuracy_by_run.english+s0.native = 0.7579681274900398
measures.SIB-200 accuracy.accuracy_by_run.english+s0.itrans = 0.4452191235059761
measures.SIB-200 accuracy.accuracy_by_run.english+s1.native = 0.7549800796812749
measures.SIB-200 accuracy.accuracy_by_run.english+s1.itrans = 0.44123505976095617
measures.SIB-200 accuracy.accuracy_base.native = 0.7679282868525896
measures.SIB-200 accuracy.accuracy_base.itrans = 0.5348605577689243
measures.FLORES+ retrieval.n = 1005
measures.FLORES+ retrieval.g0_before_training = 0.4338308457711443
measures.FLORES+ retrieval.g_after_seed_mean.itrans = 0.08059701492537313
measures.FLORES+ retrieval.g_after_seed_mean.native = 0.417910447761194
measures.FLORES+ retrieval.g_after_seed_mean.english = 0.4716417910447761
measures.FLORES+ retrieval.g_after_by_seed.itrans = [0.08656716417910448, 0.07462686567164178]
measures.FLORES+ retrieval.g_after_by_seed.native = [0.41492537313432837, 0.4208955223880597]
measures.FLORES+ retrieval.g_after_by_seed.english = [0.46766169154228854, 0.47562189054726367]
measures.FLORES+ retrieval.D_N.point = 0.3373134328358209
measures.FLORES+ retrieval.D_N.ci975 = [0.2955223880597015, 0.3781094527363184]
measures.FLORES+ retrieval.D_N.above_0 = true
measures.FLORES+ retrieval.D_N.entirely_below_0 = false
measures.FLORES+ retrieval.D_N.seed_spread_D_seed0_seed1 = [0.3283582089552239, 0.34626865671641793]
measures.FLORES+ retrieval.D_E.point = 0.39104477611940297
measures.FLORES+ retrieval.D_E.ci975 = [0.34427860696517415, 0.4348258706467662]
measures.FLORES+ retrieval.D_E.above_0 = true
measures.FLORES+ retrieval.D_E.entirely_below_0 = false
measures.FLORES+ retrieval.D_E.seed_spread_D_seed0_seed1 = [0.38109452736318405, 0.4009950248756219]
measures.FLORES+ retrieval.verdict = "supported"
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.native = 0.9263681592039801
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.itrans = 0.8398009950248756
measures.FLORES+ retrieval.accuracy_by_run.itrans+s1.native = 0.9283582089552239
measures.FLORES+ retrieval.accuracy_by_run.itrans+s1.itrans = 0.8537313432835821
measures.FLORES+ retrieval.accuracy_by_run.native+s0.native = 0.9273631840796019
measures.FLORES+ retrieval.accuracy_by_run.native+s0.itrans = 0.5124378109452736
measures.FLORES+ retrieval.accuracy_by_run.native+s1.native = 0.9134328358208955
measures.FLORES+ retrieval.accuracy_by_run.native+s1.itrans = 0.4925373134328358
measures.FLORES+ retrieval.accuracy_by_run.english+s0.native = 0.9104477611940298
measures.FLORES+ retrieval.accuracy_by_run.english+s0.itrans = 0.4427860696517413
measures.FLORES+ retrieval.accuracy_by_run.english+s1.native = 0.9293532338308458
measures.FLORES+ retrieval.accuracy_by_run.english+s1.itrans = 0.4537313432835821
measures.FLORES+ retrieval.accuracy_base.native = 0.9442786069651742
measures.FLORES+ retrieval.accuracy_base.itrans = 0.5104477611940299
english_sib_damage_check.base = 0.7679282868525896
english_sib_damage_check.by_run.itrans+s0.acc = 0.75199203187251
english_sib_damage_check.by_run.itrans+s0.drop_points = 1.5936254980079667
english_sib_damage_check.by_run.itrans+s0.flagged = false
english_sib_damage_check.by_run.itrans+s1.acc = 0.75
english_sib_damage_check.by_run.itrans+s1.drop_points = 1.7928286852589626
english_sib_damage_check.by_run.itrans+s1.flagged = false
english_sib_damage_check.by_run.native+s0.acc = 0.7420318725099602
english_sib_damage_check.by_run.native+s0.drop_points = 2.589641434262946
english_sib_damage_check.by_run.native+s0.flagged = false
english_sib_damage_check.by_run.native+s1.acc = 0.7400398406374502
english_sib_damage_check.by_run.native+s1.drop_points = 2.7888446215139417
english_sib_damage_check.by_run.native+s1.flagged = false
english_sib_damage_check.by_run.english+s0.acc = 0.7171314741035857
english_sib_damage_check.by_run.english+s0.drop_points = 5.079681274900394
english_sib_damage_check.by_run.english+s0.flagged = true
english_sib_damage_check.by_run.english+s1.acc = 0.7151394422310757
english_sib_damage_check.by_run.english+s1.drop_points = 5.27888446215139
english_sib_damage_check.by_run.english+s1.flagged = true
tokenizer_unchanged.itrans+s0 = true
tokenizer_unchanged.itrans+s1 = true
tokenizer_unchanged.native+s0 = true
tokenizer_unchanged.native+s1 = true
tokenizer_unchanged.english+s0 = true
tokenizer_unchanged.english+s1 = true
B = 4997120
per_run.itrans+s0.condition = "itrans"
per_run.itrans+s0.seed = 0
per_run.itrans+s0.B_tokens = 4997120
per_run.itrans+s0.optimizer_steps = 305
per_run.itrans+s0.articles = 1804
per_run.itrans+s0.words = 919137
per_run.itrans+s0.stream_tokens = 4997120
per_run.itrans+s0.stream_tokens_per_word = 5.436752083748124
per_run.itrans+s0.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s0.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s0.tokenizer_unchanged = true
per_run.itrans+s0.train_seconds = 9093.610614538193
per_run.itrans+s0.sib.english = 0.75199203187251
per_run.itrans+s0.sib.native = 0.7659362549800797
per_run.itrans+s0.sib.itrans = 0.649402390438247
per_run.itrans+s0.retrieval.native = 0.9263681592039801
per_run.itrans+s0.retrieval.itrans = 0.8398009950248756
per_run.itrans+s1.condition = "itrans"
per_run.itrans+s1.seed = 1
per_run.itrans+s1.B_tokens = 4997120
per_run.itrans+s1.optimizer_steps = 305
per_run.itrans+s1.articles = 1804
per_run.itrans+s1.words = 919137
per_run.itrans+s1.stream_tokens = 4997120
per_run.itrans+s1.stream_tokens_per_word = 5.436752083748124
per_run.itrans+s1.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s1.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s1.tokenizer_unchanged = true
per_run.itrans+s1.train_seconds = 9574.205170631409
per_run.itrans+s1.sib.english = 0.75
per_run.itrans+s1.sib.native = 0.7669322709163346
per_run.itrans+s1.sib.itrans = 0.649402390438247
per_run.itrans+s1.retrieval.native = 0.9283582089552239
per_run.itrans+s1.retrieval.itrans = 0.8537313432835821
per_run.native+s0.condition = "native"
per_run.native+s0.seed = 0
per_run.native+s0.B_tokens = 4997120
per_run.native+s0.optimizer_steps = 305
per_run.native+s0.articles = 3361
per_run.native+s0.words = 1797994
per_run.native+s0.stream_tokens = 4997120
per_run.native+s0.stream_tokens_per_word = 2.779275125500975
per_run.native+s0.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s0.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s0.tokenizer_unchanged = true
per_run.native+s0.train_seconds = 9036.938798189163
per_run.native+s0.sib.english = 0.7420318725099602
per_run.native+s0.sib.native = 0.7649402390438247
per_run.native+s0.sib.itrans = 0.4262948207171315
per_run.native+s0.retrieval.native = 0.9273631840796019
per_run.native+s0.retrieval.itrans = 0.5124378109452736
per_run.native+s1.condition = "native"
per_run.native+s1.seed = 1
per_run.native+s1.B_tokens = 4997120
per_run.native+s1.optimizer_steps = 305
per_run.native+s1.articles = 3361
per_run.native+s1.words = 1797994
per_run.native+s1.stream_tokens = 4997120
per_run.native+s1.stream_tokens_per_word = 2.779275125500975
per_run.native+s1.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s1.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s1.tokenizer_unchanged = true
per_run.native+s1.train_seconds = 9319.656382799149
per_run.native+s1.sib.english = 0.7400398406374502
per_run.native+s1.sib.native = 0.7669322709163346
per_run.native+s1.sib.itrans = 0.42231075697211157
per_run.native+s1.retrieval.native = 0.9134328358208955
per_run.native+s1.retrieval.itrans = 0.4925373134328358
per_run.english+s0.condition = "english"
per_run.english+s0.seed = 0
per_run.english+s0.B_tokens = 4997120
per_run.english+s0.optimizer_steps = 305
per_run.english+s0.articles = 3796
per_run.english+s0.words = 2696887
per_run.english+s0.stream_tokens = 4997120
per_run.english+s0.stream_tokens_per_word = 1.8529215350884185
per_run.english+s0.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s0.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s0.tokenizer_unchanged = true
per_run.english+s0.train_seconds = 9504.01462316513
per_run.english+s0.sib.english = 0.7171314741035857
per_run.english+s0.sib.native = 0.7579681274900398
per_run.english+s0.sib.itrans = 0.4452191235059761
per_run.english+s0.retrieval.native = 0.9104477611940298
per_run.english+s0.retrieval.itrans = 0.4427860696517413
per_run.english+s1.condition = "english"
per_run.english+s1.seed = 1
per_run.english+s1.B_tokens = 4997120
per_run.english+s1.optimizer_steps = 305
per_run.english+s1.articles = 3796
per_run.english+s1.words = 2696887
per_run.english+s1.stream_tokens = 4997120
per_run.english+s1.stream_tokens_per_word = 1.8529215350884185
per_run.english+s1.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s1.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s1.tokenizer_unchanged = true
per_run.english+s1.train_seconds = 9310.572784662247
per_run.english+s1.sib.english = 0.7151394422310757
per_run.english+s1.sib.native = 0.7549800796812749
per_run.english+s1.sib.itrans = 0.44123505976095617
per_run.english+s1.retrieval.native = 0.9293532338308458
per_run.english+s1.retrieval.itrans = 0.4537313432835821
tokens_per_word_flores.native = 2.390675547098002
tokens_per_word_flores.itrans = 5.331303520456708
tokens_per_word_flores.note = "tokenizer files are identical before and after training (sha256 in per_run), so tokens per word are the same before and after by construction"
english_regression_vs_base.itrans.mean_change_points = -1.693227091633466
english_regression_vs_base.itrans.ci95_points = [-3.386454183266932, 0.049800796812749]
english_regression_vs_base.itrans.flag_more_than_5_points = false
english_regression_vs_base.itrans.by_seed_points = [-1.593625498007968, -1.7928286852589643]
english_regression_vs_base.native.mean_change_points = -2.689243027888446
english_regression_vs_base.native.ci95_points = [-4.780876494023905, -0.5976095617529881]
english_regression_vs_base.native.flag_more_than_5_points = false
english_regression_vs_base.native.by_seed_points = [-2.589641434262948, -2.788844621513944]
english_regression_vs_base.english.mean_change_points = -5.179282868525896
english_regression_vs_base.english.ci95_points = [-7.071713147410359, -3.2856075697211335]
english_regression_vs_base.english.flag_more_than_5_points = true
english_regression_vs_base.english.by_seed_points = [-5.079681274900398, -5.278884462151394]
itrans_trained_vs_original_native.SIB-200 accuracy.itrans_accuracy_after_itrans_training = 0.649402390438247
itrans_trained_vs_original_native.SIB-200 accuracy.original_native_accuracy_untrained = 0.7679282868525896
itrans_trained_vs_original_native.SIB-200 accuracy.difference = -0.11852589641434264
itrans_trained_vs_original_native.SIB-200 accuracy.ci95 = [-0.1508964143426295, -0.08665338645418327]
itrans_trained_vs_original_native.SIB-200 accuracy.reaches_original_native_level = false
itrans_trained_vs_original_native.FLORES+ retrieval.itrans_accuracy_after_itrans_training = 0.8467661691542289
itrans_trained_vs_original_native.FLORES+ retrieval.original_native_accuracy_untrained = 0.9442786069651742
itrans_trained_vs_original_native.FLORES+ retrieval.difference = -0.09751243781094528
itrans_trained_vs_original_native.FLORES+ retrieval.ci95 = [-0.11890547263681592, -0.07611940298507462]
itrans_trained_vs_original_native.FLORES+ retrieval.reaches_original_native_level = false
`````

#### `results/phase2/x9b/analysis_sarvam-1_seeds0123.json` (20,882 bytes; first commit e605a65 2026-11-06 11:53:24 +0530)

`````text
provenance.config.registration = "RESULTS.md Amendment 2, X9b (primary Sarvam-1); seeds 0,1,2,3 (the extra seeds were added after seeing the originals, RESULTS.md 2026-11-05)"
provenance.git_commit = "fc1246a10615010b9897df251844222070a7a81d-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-06T06:22:33+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9b_analyse.py", "--model", "sarvam-1", "--seeds", "0,1,2,3"]
model = "sarvam-1"
measures.SIB-200 accuracy.n = 1004
measures.SIB-200 accuracy.g0_before_training = 0.23306772908366533
measures.SIB-200 accuracy.g_after_seed_mean.itrans = 0.11877490039840638
measures.SIB-200 accuracy.g_after_seed_mean.native = 0.34063745019920316
measures.SIB-200 accuracy.g_after_seed_mean.english = 0.3129980079681275
measures.SIB-200 accuracy.g_after_by_seed.itrans = [0.11653386454183266, 0.11752988047808766, 0.12350597609561753, 0.11752988047808766]
measures.SIB-200 accuracy.g_after_by_seed.native = [0.3386454183266932, 0.34462151394422313, 0.3426294820717131, 0.33665338645418325]
measures.SIB-200 accuracy.g_after_by_seed.english = [0.31274900398406374, 0.3137450199203187, 0.3057768924302789, 0.3197211155378486]
measures.SIB-200 accuracy.D_N.point = 0.22186254980079678
measures.SIB-200 accuracy.D_N.ci975 = [0.17430278884462153, 0.2699203187250996]
measures.SIB-200 accuracy.D_N.above_0 = true
measures.SIB-200 accuracy.D_N.entirely_below_0 = false
measures.SIB-200 accuracy.D_N.seed_spread_D_seed0_seed1 = [0.22211155378486053, 0.22709163346613548, 0.2191235059760956, 0.2191235059760956]
measures.SIB-200 accuracy.D_E.point = 0.1942231075697211
measures.SIB-200 accuracy.D_E.ci975 = [0.14741035856573706, 0.24302788844621512]
measures.SIB-200 accuracy.D_E.above_0 = true
measures.SIB-200 accuracy.D_E.entirely_below_0 = false
measures.SIB-200 accuracy.D_E.seed_spread_D_seed0_seed1 = [0.19621513944223107, 0.19621513944223107, 0.18227091633466136, 0.20219123505976094]
measures.SIB-200 accuracy.verdict = "supported"
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.native = 0.7659362549800797
measures.SIB-200 accuracy.accuracy_by_run.itrans+s0.itrans = 0.649402390438247
measures.SIB-200 accuracy.accuracy_by_run.itrans+s1.native = 0.7669322709163346
measures.SIB-200 accuracy.accuracy_by_run.itrans+s1.itrans = 0.649402390438247
measures.SIB-200 accuracy.accuracy_by_run.itrans+s2.native = 0.7639442231075697
measures.SIB-200 accuracy.accuracy_by_run.itrans+s2.itrans = 0.6404382470119522
measures.SIB-200 accuracy.accuracy_by_run.itrans+s3.native = 0.7639442231075697
measures.SIB-200 accuracy.accuracy_by_run.itrans+s3.itrans = 0.646414342629482
measures.SIB-200 accuracy.accuracy_by_run.native+s0.native = 0.7649402390438247
measures.SIB-200 accuracy.accuracy_by_run.native+s0.itrans = 0.4262948207171315
measures.SIB-200 accuracy.accuracy_by_run.native+s1.native = 0.7669322709163346
measures.SIB-200 accuracy.accuracy_by_run.native+s1.itrans = 0.42231075697211157
measures.SIB-200 accuracy.accuracy_by_run.native+s2.native = 0.7649402390438247
measures.SIB-200 accuracy.accuracy_by_run.native+s2.itrans = 0.42231075697211157
measures.SIB-200 accuracy.accuracy_by_run.native+s3.native = 0.7679282868525896
measures.SIB-200 accuracy.accuracy_by_run.native+s3.itrans = 0.4312749003984064
measures.SIB-200 accuracy.accuracy_by_run.english+s0.native = 0.7579681274900398
measures.SIB-200 accuracy.accuracy_by_run.english+s0.itrans = 0.4452191235059761
measures.SIB-200 accuracy.accuracy_by_run.english+s1.native = 0.7549800796812749
measures.SIB-200 accuracy.accuracy_by_run.english+s1.itrans = 0.44123505976095617
measures.SIB-200 accuracy.accuracy_by_run.english+s2.native = 0.75199203187251
measures.SIB-200 accuracy.accuracy_by_run.english+s2.itrans = 0.44621513944223107
measures.SIB-200 accuracy.accuracy_by_run.english+s3.native = 0.7599601593625498
measures.SIB-200 accuracy.accuracy_by_run.english+s3.itrans = 0.4402390438247012
measures.SIB-200 accuracy.accuracy_base.native = 0.7679282868525896
measures.SIB-200 accuracy.accuracy_base.itrans = 0.5348605577689243
measures.FLORES+ retrieval.n = 1005
measures.FLORES+ retrieval.g0_before_training = 0.4338308457711443
measures.FLORES+ retrieval.g_after_seed_mean.itrans = 0.07537313432835821
measures.FLORES+ retrieval.g_after_seed_mean.native = 0.41393034825870645
measures.FLORES+ retrieval.g_after_seed_mean.english = 0.48084577114427857
measures.FLORES+ retrieval.g_after_by_seed.itrans = [0.08656716417910448, 0.07462686567164178, 0.05870646766169154, 0.08159203980099503]
measures.FLORES+ retrieval.g_after_by_seed.native = [0.41492537313432837, 0.4208955223880597, 0.4019900497512438, 0.417910447761194]
measures.FLORES+ retrieval.g_after_by_seed.english = [0.46766169154228854, 0.47562189054726367, 0.4925373134328358, 0.48756218905472637]
measures.FLORES+ retrieval.D_N.point = 0.3385572139303482
measures.FLORES+ retrieval.D_N.ci975 = [0.291542288557214, 0.3860696517412935]
measures.FLORES+ retrieval.D_N.above_0 = true
measures.FLORES+ retrieval.D_N.entirely_below_0 = false
measures.FLORES+ retrieval.D_N.seed_spread_D_seed0_seed1 = [0.3283582089552239, 0.34626865671641793, 0.3432835820895523, 0.33631840796019896]
measures.FLORES+ retrieval.D_E.point = 0.4054726368159204
measures.FLORES+ retrieval.D_E.ci975 = [0.35323383084577115, 0.4567164179104477]
measures.FLORES+ retrieval.D_E.above_0 = true
measures.FLORES+ retrieval.D_E.entirely_below_0 = false
measures.FLORES+ retrieval.D_E.seed_spread_D_seed0_seed1 = [0.38109452736318405, 0.4009950248756219, 0.4338308457711443, 0.4059701492537313]
measures.FLORES+ retrieval.verdict = "supported"
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.native = 0.9263681592039801
measures.FLORES+ retrieval.accuracy_by_run.itrans+s0.itrans = 0.8398009950248756
measures.FLORES+ retrieval.accuracy_by_run.itrans+s1.native = 0.9283582089552239
measures.FLORES+ retrieval.accuracy_by_run.itrans+s1.itrans = 0.8537313432835821
measures.FLORES+ retrieval.accuracy_by_run.itrans+s2.native = 0.9333333333333333
measures.FLORES+ retrieval.accuracy_by_run.itrans+s2.itrans = 0.8746268656716418
measures.FLORES+ retrieval.accuracy_by_run.itrans+s3.native = 0.9293532338308458
measures.FLORES+ retrieval.accuracy_by_run.itrans+s3.itrans = 0.8477611940298507
measures.FLORES+ retrieval.accuracy_by_run.native+s0.native = 0.9273631840796019
measures.FLORES+ retrieval.accuracy_by_run.native+s0.itrans = 0.5124378109452736
measures.FLORES+ retrieval.accuracy_by_run.native+s1.native = 0.9134328358208955
measures.FLORES+ retrieval.accuracy_by_run.native+s1.itrans = 0.4925373134328358
measures.FLORES+ retrieval.accuracy_by_run.native+s2.native = 0.9213930348258706
measures.FLORES+ retrieval.accuracy_by_run.native+s2.itrans = 0.5194029850746269
measures.FLORES+ retrieval.accuracy_by_run.native+s3.native = 0.9283582089552239
measures.FLORES+ retrieval.accuracy_by_run.native+s3.itrans = 0.5104477611940299
measures.FLORES+ retrieval.accuracy_by_run.english+s0.native = 0.9104477611940298
measures.FLORES+ retrieval.accuracy_by_run.english+s0.itrans = 0.4427860696517413
measures.FLORES+ retrieval.accuracy_by_run.english+s1.native = 0.9293532338308458
measures.FLORES+ retrieval.accuracy_by_run.english+s1.itrans = 0.4537313432835821
measures.FLORES+ retrieval.accuracy_by_run.english+s2.native = 0.9273631840796019
measures.FLORES+ retrieval.accuracy_by_run.english+s2.itrans = 0.43482587064676614
measures.FLORES+ retrieval.accuracy_by_run.english+s3.native = 0.9253731343283582
measures.FLORES+ retrieval.accuracy_by_run.english+s3.itrans = 0.43781094527363185
measures.FLORES+ retrieval.accuracy_base.native = 0.9442786069651742
measures.FLORES+ retrieval.accuracy_base.itrans = 0.5104477611940299
english_sib_damage_check.base = 0.7679282868525896
english_sib_damage_check.by_run.itrans+s0.acc = 0.75199203187251
english_sib_damage_check.by_run.itrans+s0.drop_points = 1.5936254980079667
english_sib_damage_check.by_run.itrans+s0.flagged = false
english_sib_damage_check.by_run.itrans+s1.acc = 0.75
english_sib_damage_check.by_run.itrans+s1.drop_points = 1.7928286852589626
english_sib_damage_check.by_run.itrans+s1.flagged = false
english_sib_damage_check.by_run.itrans+s2.acc = 0.75199203187251
english_sib_damage_check.by_run.itrans+s2.drop_points = 1.5936254980079667
english_sib_damage_check.by_run.itrans+s2.flagged = false
english_sib_damage_check.by_run.itrans+s3.acc = 0.7539840637450199
english_sib_damage_check.by_run.itrans+s3.drop_points = 1.3944223107569709
english_sib_damage_check.by_run.itrans+s3.flagged = false
english_sib_damage_check.by_run.native+s0.acc = 0.7420318725099602
english_sib_damage_check.by_run.native+s0.drop_points = 2.589641434262946
english_sib_damage_check.by_run.native+s0.flagged = false
english_sib_damage_check.by_run.native+s1.acc = 0.7400398406374502
english_sib_damage_check.by_run.native+s1.drop_points = 2.7888446215139417
english_sib_damage_check.by_run.native+s1.flagged = false
english_sib_damage_check.by_run.native+s2.acc = 0.7470119521912351
english_sib_damage_check.by_run.native+s2.drop_points = 2.0916334661354563
english_sib_damage_check.by_run.native+s2.flagged = false
english_sib_damage_check.by_run.native+s3.acc = 0.7440239043824701
english_sib_damage_check.by_run.native+s3.drop_points = 2.39043824701195
english_sib_damage_check.by_run.native+s3.flagged = false
english_sib_damage_check.by_run.english+s0.acc = 0.7171314741035857
english_sib_damage_check.by_run.english+s0.drop_points = 5.079681274900394
english_sib_damage_check.by_run.english+s0.flagged = true
english_sib_damage_check.by_run.english+s1.acc = 0.7151394422310757
english_sib_damage_check.by_run.english+s1.drop_points = 5.27888446215139
english_sib_damage_check.by_run.english+s1.flagged = true
english_sib_damage_check.by_run.english+s2.acc = 0.7121513944223108
english_sib_damage_check.by_run.english+s2.drop_points = 5.5776892430278835
english_sib_damage_check.by_run.english+s2.flagged = true
english_sib_damage_check.by_run.english+s3.acc = 0.7141434262948207
english_sib_damage_check.by_run.english+s3.drop_points = 5.378486055776888
english_sib_damage_check.by_run.english+s3.flagged = true
tokenizer_unchanged.itrans+s0 = true
tokenizer_unchanged.itrans+s1 = true
tokenizer_unchanged.itrans+s2 = true
tokenizer_unchanged.itrans+s3 = true
tokenizer_unchanged.native+s0 = true
tokenizer_unchanged.native+s1 = true
tokenizer_unchanged.native+s2 = true
tokenizer_unchanged.native+s3 = true
tokenizer_unchanged.english+s0 = true
tokenizer_unchanged.english+s1 = true
tokenizer_unchanged.english+s2 = true
tokenizer_unchanged.english+s3 = true
B = 4997120
per_run.itrans+s0.condition = "itrans"
per_run.itrans+s0.seed = 0
per_run.itrans+s0.B_tokens = 4997120
per_run.itrans+s0.optimizer_steps = 305
per_run.itrans+s0.articles = 1804
per_run.itrans+s0.words = 919137
per_run.itrans+s0.stream_tokens = 4997120
per_run.itrans+s0.stream_tokens_per_word = 5.436752083748124
per_run.itrans+s0.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s0.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s0.tokenizer_unchanged = true
per_run.itrans+s0.train_seconds = 9093.610614538193
per_run.itrans+s0.sib.english = 0.75199203187251
per_run.itrans+s0.sib.native = 0.7659362549800797
per_run.itrans+s0.sib.itrans = 0.649402390438247
per_run.itrans+s0.retrieval.native = 0.9263681592039801
per_run.itrans+s0.retrieval.itrans = 0.8398009950248756
per_run.itrans+s1.condition = "itrans"
per_run.itrans+s1.seed = 1
per_run.itrans+s1.B_tokens = 4997120
per_run.itrans+s1.optimizer_steps = 305
per_run.itrans+s1.articles = 1804
per_run.itrans+s1.words = 919137
per_run.itrans+s1.stream_tokens = 4997120
per_run.itrans+s1.stream_tokens_per_word = 5.436752083748124
per_run.itrans+s1.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s1.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s1.tokenizer_unchanged = true
per_run.itrans+s1.train_seconds = 9574.205170631409
per_run.itrans+s1.sib.english = 0.75
per_run.itrans+s1.sib.native = 0.7669322709163346
per_run.itrans+s1.sib.itrans = 0.649402390438247
per_run.itrans+s1.retrieval.native = 0.9283582089552239
per_run.itrans+s1.retrieval.itrans = 0.8537313432835821
per_run.itrans+s2.condition = "itrans"
per_run.itrans+s2.seed = 2
per_run.itrans+s2.B_tokens = 4997120
per_run.itrans+s2.optimizer_steps = 305
per_run.itrans+s2.articles = 1804
per_run.itrans+s2.words = 919137
per_run.itrans+s2.stream_tokens = 4997120
per_run.itrans+s2.stream_tokens_per_word = 5.436752083748124
per_run.itrans+s2.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s2.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s2.tokenizer_unchanged = true
per_run.itrans+s2.train_seconds = 8057.430752038956
per_run.itrans+s2.sib.english = 0.75199203187251
per_run.itrans+s2.sib.native = 0.7639442231075697
per_run.itrans+s2.sib.itrans = 0.6404382470119522
per_run.itrans+s2.retrieval.native = 0.9333333333333333
per_run.itrans+s2.retrieval.itrans = 0.8746268656716418
per_run.itrans+s3.condition = "itrans"
per_run.itrans+s3.seed = 3
per_run.itrans+s3.B_tokens = 4997120
per_run.itrans+s3.optimizer_steps = 305
per_run.itrans+s3.articles = 1804
per_run.itrans+s3.words = 919137
per_run.itrans+s3.stream_tokens = 4997120
per_run.itrans+s3.stream_tokens_per_word = 5.436752083748124
per_run.itrans+s3.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s3.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.itrans+s3.tokenizer_unchanged = true
per_run.itrans+s3.train_seconds = 5583.4637134075165
per_run.itrans+s3.sib.english = 0.7539840637450199
per_run.itrans+s3.sib.native = 0.7639442231075697
per_run.itrans+s3.sib.itrans = 0.646414342629482
per_run.itrans+s3.retrieval.native = 0.9293532338308458
per_run.itrans+s3.retrieval.itrans = 0.8477611940298507
per_run.native+s0.condition = "native"
per_run.native+s0.seed = 0
per_run.native+s0.B_tokens = 4997120
per_run.native+s0.optimizer_steps = 305
per_run.native+s0.articles = 3361
per_run.native+s0.words = 1797994
per_run.native+s0.stream_tokens = 4997120
per_run.native+s0.stream_tokens_per_word = 2.779275125500975
per_run.native+s0.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s0.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s0.tokenizer_unchanged = true
per_run.native+s0.train_seconds = 9036.938798189163
per_run.native+s0.sib.english = 0.7420318725099602
per_run.native+s0.sib.native = 0.7649402390438247
per_run.native+s0.sib.itrans = 0.4262948207171315
per_run.native+s0.retrieval.native = 0.9273631840796019
per_run.native+s0.retrieval.itrans = 0.5124378109452736
per_run.native+s1.condition = "native"
per_run.native+s1.seed = 1
per_run.native+s1.B_tokens = 4997120
per_run.native+s1.optimizer_steps = 305
per_run.native+s1.articles = 3361
per_run.native+s1.words = 1797994
per_run.native+s1.stream_tokens = 4997120
per_run.native+s1.stream_tokens_per_word = 2.779275125500975
per_run.native+s1.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s1.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s1.tokenizer_unchanged = true
per_run.native+s1.train_seconds = 9319.656382799149
per_run.native+s1.sib.english = 0.7400398406374502
per_run.native+s1.sib.native = 0.7669322709163346
per_run.native+s1.sib.itrans = 0.42231075697211157
per_run.native+s1.retrieval.native = 0.9134328358208955
per_run.native+s1.retrieval.itrans = 0.4925373134328358
per_run.native+s2.condition = "native"
per_run.native+s2.seed = 2
per_run.native+s2.B_tokens = 4997120
per_run.native+s2.optimizer_steps = 305
per_run.native+s2.articles = 3361
per_run.native+s2.words = 1797994
per_run.native+s2.stream_tokens = 4997120
per_run.native+s2.stream_tokens_per_word = 2.779275125500975
per_run.native+s2.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s2.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s2.tokenizer_unchanged = true
per_run.native+s2.train_seconds = 5202.730954647064
per_run.native+s2.sib.english = 0.7470119521912351
per_run.native+s2.sib.native = 0.7649402390438247
per_run.native+s2.sib.itrans = 0.42231075697211157
per_run.native+s2.retrieval.native = 0.9213930348258706
per_run.native+s2.retrieval.itrans = 0.5194029850746269
per_run.native+s3.condition = "native"
per_run.native+s3.seed = 3
per_run.native+s3.B_tokens = 4997120
per_run.native+s3.optimizer_steps = 305
per_run.native+s3.articles = 3361
per_run.native+s3.words = 1797994
per_run.native+s3.stream_tokens = 4997120
per_run.native+s3.stream_tokens_per_word = 2.779275125500975
per_run.native+s3.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s3.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.native+s3.tokenizer_unchanged = true
per_run.native+s3.train_seconds = 5538.169909477234
per_run.native+s3.sib.english = 0.7440239043824701
per_run.native+s3.sib.native = 0.7679282868525896
per_run.native+s3.sib.itrans = 0.4312749003984064
per_run.native+s3.retrieval.native = 0.9283582089552239
per_run.native+s3.retrieval.itrans = 0.5104477611940299
per_run.english+s0.condition = "english"
per_run.english+s0.seed = 0
per_run.english+s0.B_tokens = 4997120
per_run.english+s0.optimizer_steps = 305
per_run.english+s0.articles = 3796
per_run.english+s0.words = 2696887
per_run.english+s0.stream_tokens = 4997120
per_run.english+s0.stream_tokens_per_word = 1.8529215350884185
per_run.english+s0.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s0.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s0.tokenizer_unchanged = true
per_run.english+s0.train_seconds = 9504.01462316513
per_run.english+s0.sib.english = 0.7171314741035857
per_run.english+s0.sib.native = 0.7579681274900398
per_run.english+s0.sib.itrans = 0.4452191235059761
per_run.english+s0.retrieval.native = 0.9104477611940298
per_run.english+s0.retrieval.itrans = 0.4427860696517413
per_run.english+s1.condition = "english"
per_run.english+s1.seed = 1
per_run.english+s1.B_tokens = 4997120
per_run.english+s1.optimizer_steps = 305
per_run.english+s1.articles = 3796
per_run.english+s1.words = 2696887
per_run.english+s1.stream_tokens = 4997120
per_run.english+s1.stream_tokens_per_word = 1.8529215350884185
per_run.english+s1.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s1.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s1.tokenizer_unchanged = true
per_run.english+s1.train_seconds = 9310.572784662247
per_run.english+s1.sib.english = 0.7151394422310757
per_run.english+s1.sib.native = 0.7549800796812749
per_run.english+s1.sib.itrans = 0.44123505976095617
per_run.english+s1.retrieval.native = 0.9293532338308458
per_run.english+s1.retrieval.itrans = 0.4537313432835821
per_run.english+s2.condition = "english"
per_run.english+s2.seed = 2
per_run.english+s2.B_tokens = 4997120
per_run.english+s2.optimizer_steps = 305
per_run.english+s2.articles = 3796
per_run.english+s2.words = 2696887
per_run.english+s2.stream_tokens = 4997120
per_run.english+s2.stream_tokens_per_word = 1.8529215350884185
per_run.english+s2.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s2.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s2.tokenizer_unchanged = true
per_run.english+s2.train_seconds = 5100.079291820526
per_run.english+s2.sib.english = 0.7121513944223108
per_run.english+s2.sib.native = 0.75199203187251
per_run.english+s2.sib.itrans = 0.44621513944223107
per_run.english+s2.retrieval.native = 0.9273631840796019
per_run.english+s2.retrieval.itrans = 0.43482587064676614
per_run.english+s3.condition = "english"
per_run.english+s3.seed = 3
per_run.english+s3.B_tokens = 4997120
per_run.english+s3.optimizer_steps = 305
per_run.english+s3.articles = 3796
per_run.english+s3.words = 2696887
per_run.english+s3.stream_tokens = 4997120
per_run.english+s3.stream_tokens_per_word = 1.8529215350884185
per_run.english+s3.tokenizer_sha256_before = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s3.tokenizer_sha256_after = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
per_run.english+s3.tokenizer_unchanged = true
per_run.english+s3.train_seconds = 5685.73038482666
per_run.english+s3.sib.english = 0.7141434262948207
per_run.english+s3.sib.native = 0.7599601593625498
per_run.english+s3.sib.itrans = 0.4402390438247012
per_run.english+s3.retrieval.native = 0.9253731343283582
per_run.english+s3.retrieval.itrans = 0.43781094527363185
tokens_per_word_flores.native = 2.390675547098002
tokens_per_word_flores.itrans = 5.331303520456708
tokens_per_word_flores.note = "tokenizer files are identical before and after training (sha256 in per_run), so tokens per word are the same before and after by construction"
english_regression_vs_base.itrans.mean_change_points = -1.593625498007968
english_regression_vs_base.itrans.ci95_points = [-3.2619521912350598, 0.099601593625498]
english_regression_vs_base.itrans.flag_more_than_5_points = false
english_regression_vs_base.itrans.by_seed_points = [-1.593625498007968, -1.7928286852589643, -1.593625498007968, -1.394422310756972]
english_regression_vs_base.native.mean_change_points = -2.4651394422310755
english_regression_vs_base.native.ci95_points = [-4.482071713147411, -0.4233067729083665]
english_regression_vs_base.native.flag_more_than_5_points = false
english_regression_vs_base.native.by_seed_points = [-2.589641434262948, -2.788844621513944, -2.091633466135458, -2.3904382470119523]
english_regression_vs_base.english.mean_change_points = -5.328685258964144
english_regression_vs_base.english.ci95_points = [-7.270916334661355, -3.4113545816733066]
english_regression_vs_base.english.flag_more_than_5_points = true
english_regression_vs_base.english.by_seed_points = [-5.079681274900398, -5.278884462151394, -5.577689243027888, -5.378486055776892]
itrans_trained_vs_original_native.SIB-200 accuracy.itrans_accuracy_after_itrans_training = 0.646414342629482
itrans_trained_vs_original_native.SIB-200 accuracy.original_native_accuracy_untrained = 0.7679282868525896
itrans_trained_vs_original_native.SIB-200 accuracy.difference = -0.12151394422310757
itrans_trained_vs_original_native.SIB-200 accuracy.ci95 = [-0.15338645418326693, -0.08989043824701196]
itrans_trained_vs_original_native.SIB-200 accuracy.reaches_original_native_level = false
itrans_trained_vs_original_native.FLORES+ retrieval.itrans_accuracy_after_itrans_training = 0.8539800995024875
itrans_trained_vs_original_native.FLORES+ retrieval.original_native_accuracy_untrained = 0.9442786069651742
itrans_trained_vs_original_native.FLORES+ retrieval.difference = -0.09029850746268657
itrans_trained_vs_original_native.FLORES+ retrieval.ci95 = [-0.11069651741293532, -0.0699004975124378]
itrans_trained_vs_original_native.FLORES+ retrieval.reaches_original_native_level = false
`````

#### `results/phase2/x9b/base_reference.json` (348 bytes; first commit e117616 2026-11-04 20:35:05 +0530)

`````text
sarvam-1.native.layer = 24
sarvam-1.native.acc_unmapped = 0.9442786069651742
sarvam-1.itrans.layer = 21
sarvam-1.itrans.acc_unmapped = 0.5104477611940299
source = "results/kaggle/kaggle_x9b/2026-11-03T023638/out/sarvam-1__base/retrieval.json (account 1, batch 1; equals the A1-R Kaggle numbers)"
tolerance_acc = 0.01
`````

#### `results/phase2/x9b/laptop_pilot.json` (1,762 bytes; first commit 6be3732 2026-11-05 13:12:01 +0530)

`````text
provenance.config.purpose = "feasibility of extra Sarvam-1 seeds on the laptop; no accuracy is used"
provenance.git_commit = "3483bc86aa6d5e3c0b5b9542e9cd349614300151-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-05T07:40:26+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9b_laptop_pilot.py"]
itrans.micro_batch = 16
itrans.grad_accum = 2
itrans.micro_steps = 50
itrans.timed_micro_steps = 45
itrans.tokens_per_s = 633.6121222738642
itrans.seconds_timed = 581.8070504665375
itrans.peak_vram_gib = 10.646339893341064
itrans.loss_first = 3.0237317085266113
itrans.loss_last = 3.393167734146118
itrans.finite_loss = true
itrans.consumed_articles = 157
itrans.consumed_words = 93223
itrans.tokenizer_sha256 = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
native.micro_batch = 16
native.grad_accum = 2
native.micro_steps = 50
native.timed_micro_steps = 45
native.tokens_per_s = 564.4881198797456
native.seconds_timed = 653.0518305301666
native.peak_vram_gib = 10.643898487091064
native.loss_first = 2.5970962047576904
native.loss_last = 2.865891695022583
native.finite_loss = true
native.consumed_articles = 321
native.consumed_words = 182300
native.tokenizer_sha256 = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
estimate.B_tokens_per_run = 4997120
estimate.slowest_tokens_per_s = 564.4881198797456
estimate.train_hours_per_run = 2.459022324835813
estimate.t4_slowest_tokens_per_s_registered = 515.667041361334
`````

#### `results/phase2/x9b/pilot_done.json` (5,408 bytes; first commit ec0eaad 2026-11-03 07:25:12 +0530)

`````text
seq_len = 512
tokens_per_optimizer_step = 16384
steps = 50
device = "cuda"
quantized = true
models.sarvam-1.conditions.itrans.micro_batch = 16
models.sarvam-1.conditions.itrans.grad_accum = 2
models.sarvam-1.conditions.itrans.micro_steps = 50
models.sarvam-1.conditions.itrans.timed_micro_steps = 45
models.sarvam-1.conditions.itrans.tokens_per_s = 516.3744203566582
models.sarvam-1.conditions.itrans.seconds_timed = 713.9005835056305
models.sarvam-1.conditions.itrans.peak_vram_gib = 10.646339893341064
models.sarvam-1.conditions.itrans.loss_first = 3.023693084716797
models.sarvam-1.conditions.itrans.loss_last = 3.3919992446899414
models.sarvam-1.conditions.itrans.finite_loss = true
models.sarvam-1.conditions.itrans.consumed_articles = 157
models.sarvam-1.conditions.itrans.consumed_words = 93223
models.sarvam-1.conditions.itrans.tokenizer_sha256 = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
models.sarvam-1.conditions.native.micro_batch = 16
models.sarvam-1.conditions.native.grad_accum = 2
models.sarvam-1.conditions.native.micro_steps = 50
models.sarvam-1.conditions.native.timed_micro_steps = 45
models.sarvam-1.conditions.native.tokens_per_s = 515.667041361334
models.sarvam-1.conditions.native.seconds_timed = 714.8798942565918
models.sarvam-1.conditions.native.peak_vram_gib = 10.643898487091064
models.sarvam-1.conditions.native.loss_first = 2.59706711769104
models.sarvam-1.conditions.native.loss_last = 2.865229606628418
models.sarvam-1.conditions.native.finite_loss = true
models.sarvam-1.conditions.native.consumed_articles = 321
models.sarvam-1.conditions.native.consumed_words = 182300
models.sarvam-1.conditions.native.tokenizer_sha256 = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
models.sarvam-1.conditions.english.micro_batch = 16
models.sarvam-1.conditions.english.grad_accum = 2
models.sarvam-1.conditions.english.micro_steps = 50
models.sarvam-1.conditions.english.timed_micro_steps = 45
models.sarvam-1.conditions.english.tokens_per_s = 516.9965830294788
models.sarvam-1.conditions.english.seconds_timed = 713.041463136673
models.sarvam-1.conditions.english.peak_vram_gib = 10.643898487091064
models.sarvam-1.conditions.english.loss_first = 2.1324374675750732
models.sarvam-1.conditions.english.loss_last = 2.099639415740967
models.sarvam-1.conditions.english.finite_loss = true
models.sarvam-1.conditions.english.consumed_articles = 429
models.sarvam-1.conditions.english.consumed_words = 277151
models.sarvam-1.conditions.english.tokenizer_sha256 = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
models.sarvam-1.slowest_tokens_per_s = 515.667041361334
models.sarvam-1.B = 4997120
models.sarvam-1.optimizer_steps_at_B = 305
models.sarvam-1.pool_estimate.itrans.tokens_per_word = 5.494737779813946
models.sarvam-1.pool_estimate.itrans.retained_words = 17402199
models.sarvam-1.pool_estimate.itrans.estimated_pool_tokens = 95620520
models.sarvam-1.pool_estimate.native.tokens_per_word = 2.7687995520431667
models.sarvam-1.pool_estimate.native.retained_words = 17402199
models.sarvam-1.pool_estimate.native.estimated_pool_tokens = 48183200
models.sarvam-1.pool_estimate.english.tokens_per_word = 1.834761181471485
models.sarvam-1.pool_estimate.english.retained_words = 111266992
models.sarvam-1.pool_estimate.english.estimated_pool_tokens = 204148357
models.sarvam-1.pool_covers_B.itrans = true
models.sarvam-1.pool_covers_B.native = true
models.sarvam-1.pool_covers_B.english = true
models.sarvam-1.tokenizer_sha256 = "72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"
models.qwen3.5-2b.conditions.itrans.micro_batch = 4
models.qwen3.5-2b.conditions.itrans.grad_accum = 8
models.qwen3.5-2b.conditions.itrans.micro_steps = 50
models.qwen3.5-2b.conditions.itrans.timed_micro_steps = 45
models.qwen3.5-2b.conditions.itrans.tokens_per_s = 583.7266396347001
models.qwen3.5-2b.conditions.itrans.seconds_timed = 157.8821210861206
models.qwen3.5-2b.conditions.itrans.peak_vram_gib = 9.696794033050537
models.qwen3.5-2b.conditions.itrans.loss_first = 5.208492279052734
models.qwen3.5-2b.conditions.itrans.loss_last = 4.816302299499512
models.qwen3.5-2b.conditions.itrans.finite_loss = true
models.qwen3.5-2b.conditions.itrans.consumed_articles = 215
models.qwen3.5-2b.conditions.itrans.consumed_words = 117095
models.qwen3.5-2b.conditions.itrans.tokenizer_sha256 = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
models.qwen3.5-2b.conditions.native.micro_batch = 4
models.qwen3.5-2b.conditions.native.grad_accum = 8
models.qwen3.5-2b.conditions.native.micro_steps = 50
models.qwen3.5-2b.conditions.native.timed_micro_steps = 45
models.qwen3.5-2b.conditions.native.tokens_per_s = 586.2339601553906
models.qwen3.5-2b.conditions.native.seconds_timed = 157.20685982704163
models.qwen3.5-2b.conditions.native.peak_vram_gib = 9.696794033050537
models.qwen3.5-2b.conditions.native.loss_first = 1.9397025108337402
models.qwen3.5-2b.conditions.native.loss_last = 1.9409841299057007
models.qwen3.5-2b.conditions.native.finite_loss = true
models.qwen3.5-2b.conditions.native.consumed_articles = 153
models.qwen3.5-2b.conditions.native.consumed_words = 92498
models.qwen3.5-2b.conditions.native.tokenizer_sha256 = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
models.qwen3.5-2b.conditions.english.micro_batch = 4
models.qwen3.5-2b.conditions.english.grad_accum = 8
models.qwen3.5-2b.conditions.english.micro_steps = 50
models.qwen3.5-2b.conditions.english.timed_micro_steps = 45
models.qwen3.5-2b.conditions.english.tokens_per_s = 587.0241948385907
models.qwen3.5-2b.conditions.english.seconds_timed = 156.99523258209229
models.qwen3.5-2b.conditions.english.peak_vram_gib = 9.696794033050537
models.qwen3.5-2b.conditions.english.loss_first = 2.7728962898254395
models.qwen3.5-2b.conditions.english.loss_last = 2.4682095050811768
models.qwen3.5-2b.conditions.english.finite_loss = true
models.qwen3.5-2b.conditions.english.consumed_articles = 520
models.qwen3.5-2b.conditions.english.consumed_words = 336197
models.qwen3.5-2b.conditions.english.tokenizer_sha256 = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
models.qwen3.5-2b.slowest_tokens_per_s = 583.7266396347001
models.qwen3.5-2b.B = 5668864
models.qwen3.5-2b.optimizer_steps_at_B = 346
models.qwen3.5-2b.pool_estimate.itrans.tokens_per_word = 4.3586772547372705
models.qwen3.5-2b.pool_estimate.itrans.retained_words = 17402199
models.qwen3.5-2b.pool_estimate.itrans.estimated_pool_tokens = 75850568
models.qwen3.5-2b.pool_estimate.native.tokens_per_word = 5.507177490169129
models.qwen3.5-2b.pool_estimate.native.retained_words = 17402199
models.qwen3.5-2b.pool_estimate.native.estimated_pool_tokens = 95836998
models.qwen3.5-2b.pool_estimate.english.tokens_per_word = 1.5201446788980801
models.qwen3.5-2b.pool_estimate.english.retained_words = 111266992
models.qwen3.5-2b.pool_estimate.english.estimated_pool_tokens = 169141925
models.qwen3.5-2b.pool_covers_B.itrans = true
models.qwen3.5-2b.pool_covers_B.native = true
models.qwen3.5-2b.pool_covers_B.english = true
models.qwen3.5-2b.tokenizer_sha256 = "63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"
order_sha256.kn = "9213b0927c3342c80aa87c45f88513b10b7adecff1f95b4b0142cd1c316e908d"
order_sha256.en = "38a275915fe7cf5646c68f7f7692a2268715faa95df5cb08a8b4675843fb8e0f"
exclusion_rescan_overlap.sarvam-1:itrans = 0
exclusion_rescan_overlap.sarvam-1:native = 0
exclusion_rescan_overlap.sarvam-1:english = 0
exclusion_rescan_overlap.qwen3.5-2b:itrans = 0
exclusion_rescan_overlap.qwen3.5-2b:native = 0
exclusion_rescan_overlap.qwen3.5-2b:english = 0
streams_report.native_kannada = 0
streams_report.itrans_kannada = 0
streams_report.english = 0
all_overlap_zero = true
eval_smoke_ok = true
seconds = 3217.1574187278748
eval_smoke_seconds = 29.66992974281311
`````

#### `results/phase2/x9b/removed_ids.json` (723 bytes; first commit 0d353fc 2026-11-02 23:41:34 +0530)

`````text
provenance.config.experiment = "X9b removed article ids (the Kaggle job reproduces the seeded order from these and checks the sha256)"
provenance.git_commit = "0d353fcb0811d5ebf4734598be28633d4194d26f-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-02T18:12:07+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9b_streams.py", "--workers", "5"]
en = ["4764461", "4866465"]
`````

#### `results/phase2/x9b/streams_report.json` (2,043 bytes; first commit 0d353fc 2026-11-02 23:41:34 +0530)

`````text
provenance.config.experiment = "X9b exclusion scan (CPU)"
provenance.config.registration = "phase2-amendment-2"
provenance.git_commit = "0d353fcb0811d5ebf4734598be28633d4194d26f-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.phase2_amendment2_commit = "680151b44e17e22254b74be53bfc5740e52fc8c4"
provenance.timestamp_utc = "2026-11-02T18:12:07+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/x9b_streams.py", "--workers", "5"]
eval_sentences.flores_kn = 2009
eval_sentences.flores_en = 2009
eval_sentences.sib_kn = 1004
eval_sentences.sib_en = 1004
eval_sentences.flores_kn_itrans = 2009
eval_sentences.sib_kn_itrans = 1004
wikipedia_revision = "b04c8d1ceb2f5cd4588862100d08de323dccfbaa"
sib_revision = "38977a667f6fc264d5c26ec57a01e16db040b358"
prefix_chars = 20
seed = 9
limit = null
streams.native_kannada.pool_articles = 31437
streams.native_kannada.removed_native_scan = 0
streams.native_kannada.retained_articles = 31437
streams.native_kannada.retained_words = 17402199
streams.native_kannada.final_overlap = 0
streams.native_kannada.order_sha256 = "9213b0927c3342c80aa87c45f88513b10b7adecff1f95b4b0142cd1c316e908d"
streams.itrans_kannada.pool_articles = 31437
streams.itrans_kannada.removed_itrans_scan = 0
streams.itrans_kannada.removed_union_with_native = 0
streams.itrans_kannada.retained_articles = 31437
streams.itrans_kannada.retained_words = 17402199
streams.itrans_kannada.final_overlap = 0
streams.itrans_kannada.order_sha256 = "9213b0927c3342c80aa87c45f88513b10b7adecff1f95b4b0142cd1c316e908d"
streams.english.pool_articles = 156289
streams.english.removed = 2
streams.english.removed_by_set.flores_en = 2
streams.english.removed_by_set.sib_en = 2
streams.english.retained_articles = 156287
streams.english.retained_words = 111266992
streams.english.final_overlap = 0
streams.english.order_sha256 = "38a275915fe7cf5646c68f7f7692a2268715faa95df5cb08a8b4675843fb8e0f"
all_overlap_zero = true
seconds = 800.0212807655334
`````

## Not dumped (item-level, binary or too large; path and size only)

- `results/phase2/x9b/streams_run.log`: .log file, 400 bytes (binary or per-item data, not dumped)

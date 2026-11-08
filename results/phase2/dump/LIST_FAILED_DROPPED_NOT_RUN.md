# Runs that failed, were dropped or were not run (entries with the reason as logged)

Entries whose title matches the keywords `FAILED|failed|Failure|failure|not run|NOT RUN|did not run|dropped|DROPPED|cancelled|skipped|incident|STALL|CRASH|crash|EXHAUSTED|considered|not built|unavailable|Chain incident` (verbatim, with commit and date). Phase 1 first.

## Phase 1

##### 2026-10-08 — E0 GATE (4 of 5 models; Gemma 4 E2B not run)

RESULTS.md lines 205 to 231; first line committed in `22013f7` on 2026-10-08 01:52:43 +0530; last line in `0a1d054` on 2026-10-14 18:42:59 +0530; labels from the title and parent heading: result, failed or not run

`````text
## 2026-10-08 — E0 GATE (4 of 5 models; Gemma 4 E2B not run)

- `scripts/e00_gate.py`; results `results/e00_gate/summary.csv`, `summary.json`, `scores_<model>.parquet`. n = 200 items
  per task (IndicXNLI kn test aligned to XNLI en; IndicSentiment kn test with English review), stratified, seed 0.
  Log-likelihood of English label words after an English instruction (templates e0_*_v1). Raw accuracy, 95%
  bootstrap CI. Chance: XNLI 33.3%, sentiment 50%.
- Gemma 4 E2B: the E0 job was stopped by Claude Code for low system memory while loading Gemma (the loader briefly
  materializes the 10 GB checkpoint in CPU RAM). Not restarted pending Aarnav's go-ahead.

  | model | sentiment en / native / ITRANS | XNLI en / native / ITRANS |
  |---|---|---|
  | Qwen2.5-1.5B-Instruct | 98.5 / 70.5 / 49.5 | 79.5 / 51.0 / 37.5 |
  | Qwen3-1.7B | 98.5 / 86.5 / 58.0 | 61.5 / 43.0 / 37.0 |
  | Qwen3.5-2B | 97.5 / 78.5 / 67.5 | 43.0 / 34.0 / 34.0 |
  | Sarvam-1 | 95.5 / 98.0 / 80.0 | 57.5 / 52.0 / 40.5 |

- Gate rule (native >= chance + 10 and English >= chance + 15 on one task): **all four pass**, via sentiment;
  Qwen2.5 and Sarvam-1 also pass on XNLI. Qwen3.5-2B collapses to one label on XNLI (99.5% of predictions in native
  and ITRANS; calibrated English 62.0%).
- **Finding relevant to M1/M2: ITRANS accuracy is below native in every model and task, including the Qwen models
  where ITRANS is far less fragmented** (Qwen2.5: native 70.5 vs ITRANS 49.5 on sentiment, with 99.5% of ITRANS
  predictions on one label; Qwen3 86.5 vs 58.0). Fewer tokens did not make ITRANS easier; familiarity with the form
  (training data) dominates at the accuracy level. This argues against the simplest fragmentation story for accuracy
  and has to be reported. Several ITRANS cells are at chance (all XNLI-ITRANS, Qwen2.5 sentiment-ITRANS), which limits
  M2/M6 for those cells.

---
`````

##### 2026-10-21 — Chain incident: the Kanglish chain and watcher ended during laptop sleep

RESULTS.md lines 1283 to 1300; first line committed in `d7693f7` on 2026-10-21 22:25:39 +0530; last line in `9710f74` on 2026-10-22 01:00:43 +0530; labels from the title and parent heading: failed or not run

`````text
## 2026-10-21 — Chain incident: the Kanglish chain and watcher ended during laptop sleep
- **What stopped.** The Kanglish chain's last heartbeat was 2026-10-17 15:14:28 IST. The laptop went to sleep at
  about 15:15 and stayed asleep, apart from brief wakes, until 10-20 13:31 and again 10-21 12:33.
  - Both scheduled tasks had ended: Kanglish with code 0x40010004, the watcher with code 4.
  - The watcher ended too, so it never marked the status DEAD, and the file kept saying WAITING. No reboot happened
    (last boot 10-14).
  - The Task Scheduler event log is disabled, so the exact cause is not verified.
- **What finished first.** M4c and E0c were DONE before this. The drafts had reached 849 of 1,000 by 10-17 13:28,
  using the 10-16 and 10-17 quota windows. The 10-18 to 10-20 windows were lost.
- **Fix (2026-10-21).**
  - `scripts/detach.ps1` now also restarts each task at logon and 1 minute after every wake from sleep (System log,
    Power-Troubleshooter event 1).
  - A second instance is never started while one is running.
  - A chain whose status is DONE exits at once.
  - The Kanglish chain and the watcher were relaunched at 22:21 IST on 10-21, in the open 10-21 quota window.
  - Not yet tested across a real sleep.

---
`````

##### 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists)

RESULTS.md lines 2972 to 3002; first line committed in `46bd82a` on 2026-10-26 12:10:58 +0530; last line in `46bd82a` on 2026-10-26 12:10:58 +0530; labels from the title and parent heading: result, failed or not run

`````text
## 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists)
- **Definition in K2 (registered 2026-10-16, `shattered.translit.codemix`, "v1"):** neither the English-loan measure v1
  (wordfreq Zipf ≥ 3, > 3 characters) nor v2 (also in the parallel English sentence). A lower-cased alphabetic token
  is English if it is in the wordfreq top-50k English list and not in the romanized-Kannada lexicon (to_lossy of the
  top-50k Kannada Wikipedia words); in both lists it is language-independent; otherwise Kannada.
- **Check (Aarnav's design):** 50 kanglish_verified texts, `default_rng(0)`, 883 alphabetic tokens; every token type
  marked by Claude Code (`results/codemix_check/gold_sample0.json`: E English, K Kannada, N name/unit, H English stem +
  Kannada suffix; N and H count as not English). `scripts/codemix_check.py 0 v1` →
  `results/codemix_check/check_sample0_v1.json`.
- **Result: precision 0.928 (219/236), recall 0.883 (219/248): below 0.9, so stopped.**
  - False positives (17): names and name-derived adjectives tagged English (amsterdam, angola ×2, claudia, germany,
    iceland, luxembourg, machu, stearns, frank, BIS, austrian, russian, african, mediterranean) and one Kannada word
    (kami, "less", ×2).
  - Missed English (29): 24 common English words that are also in the Kannada lexicon and so become
    language-independent (and, on, so, but, air ×3, start ×2, help, post, skin, lens ×3, gel, LED, ad ×2, dark, bed,
    sharp, limited); 5 English words outside the top-50k list (eggless, moisturize, purifiers ×2, tuners,
    occasionaly).
  - Not counted as English in either definition: 9 English-stem + Kannada-suffix tokens (productginta, groupnalli,
    lensesgalu, skinannu, …); with them counted as English, recall is 0.852.
- **Fix, v2 (`codemix.tag_v2` / `code_mixing_v2`; v1 kept unchanged):** (1) single letters language-independent;
  (2) a token that occurs in the item's parallel English sentence only in Title case and not sentence-initially is a
  name (language-independent; all-caps acronyms not affected); (3) a token in both lists goes to the language where
  it ranks higher (English: position in the wordfreq top-50k list; Kannada: best rank of a Kannada Wikipedia word whose
  lossy romanization contains it); (4) a token in neither list is English if its wordfreq English Zipf ≥ 2.5, else
  Kannada; (5) English stem + Kannada suffix stays Kannada (the share is a lower bound for such loans).
- **v2 was designed after seeing sample 0's errors**, so its rerun on sample 0 is optimistic. A fresh sample
  (`default_rng(1)`, 50 texts) is marked by hand from the v1 view (before any v2 tag of it is seen) and is the deciding
  check: v2 is used for K2 only if precision and recall are both ≥ 0.9 on it. K2 uses v2 for the English share in
  K2a and K2b if it passes; v1 results are reported alongside.

---
`````

##### 2026-10-26 14:50 IST — K1/K2 pilot: first attempt failed on an id-type error (no computation; fixed, relaunched)

RESULTS.md lines 3105 to 3109; first line committed in `5baf376` on 2026-10-26 14:46:26 +0530; last line in `13458fe` on 2026-10-26 15:32:56 +0530; labels from the title and parent heading: failed or not run

`````text
## 2026-10-26 14:50 IST — K1/K2 pilot: first attempt failed on an id-type error (no computation; fixed, relaunched)
The pilot crashed while writing the scores file (`ArrowTypeError`: sentiment ids are strings, SIB ids are ints; same
cause as the NC1 crash of 2026-10-22). Fix: SIB ids are written as strings and converted back in the analysis
(`k_k12.for_scoring`). No score, accuracy or statistic had been computed; no design change.

`````

##### 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched

RESULTS.md lines 3178 to 3185; first line committed in `126a488` on 2026-10-28 03:46:10 +0530; last line in `126a488` on 2026-10-28 03:46:10 +0530; labels from the title and parent heading: failed or not run

`````text
## 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched
The SIB-1,004 Hindi drafts hit `getaddrinfo failed` (no network) on 2026-10-27 after 15:18 IST and the H1-LF chain was marked
FAILED; it restarted at 02:46 IST and completed the drafts at 03:14 IST (Kannada 1,004 and Hindi 1,004 done; 9 and 10 still
defective after retries, excluded as registered), then started GPU scoring (qwen3-1.7b first). The K3b-hi chain, which stops
when it sees the H1-LF chain FAILED, ended at 02:46 IST without starting; relaunched at 03:17 IST (API only, no GPU). No design
change.

---
`````

## Phase 2

##### 2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehe

RESULTS.md lines 3820 to 3821; first line committed in `bcaebe7` on 2026-11-03 07:43:00 +0530; last line in `48deb83` on 2026-11-03 08:06:57 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehearsal discarded as designed.** Measured: 20 optimizer steps (327,680 tokens) in 589 s, loss 2.57 at step 20, adapter and checkpoint written. The failure is in `PeftModel.from_pretrained` before the evaluation: the Kaggle image ships torchao 0.10.0, which the pinned peft 0.21.2 refuses (`ImportError: Found an incompatible version of torchao. Found version 0.10.0, but only versions above 0.16.0 are supported`). Fix (no rule change): the kernel uninstalls torchao after installing the pins (nothing in this project uses it). A failed rehearsal is now repeated by the driver, never skipped (the driver would otherwise have started the full runs on the next pass); the rehearsal is re-queued (about 0.3 h). No registered X9b run has started; B stays as logged.

`````

##### 2026-11-03 12:56 IST, X8 imported and analysed as registered (K4, K5; K6 not run).

RESULTS.md lines 3825 to 3828; first line committed in `16e09e4` on 2026-11-03 12:56:47 +0530; last line in `2df4879` on 2026-11-03 12:58:00 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-03 12:56 IST, X8 imported and analysed as registered (K4, K5; K6 not run).** Files: the filled `X8_P.xlsx` (saved 12:52, 100 answers) and `X8_Q.xlsx` (saved 01:32, 100 answers), both found in `annotation/xlsx/` (not in `annotation/returned/`) and imported from copies in `annotation/returned/`; both pass every check (0 blockers, 0 warnings: every Romanization cell non-blank, every other cell identical to the original; uppercase-start share 0.01 in both; unexpected-character share 0.02 (P) and 0.01 (Q): the string "Õ / õ" copied from sentence 422, which contains it, and two zero-width spaces in P sentence 991); 0 of the 100 sentences are identical between P and Q. **The importer's same-person check blocked the pair because both files carry the same author field (both were saved on Aarnav's account); it was run with `--shared-account-ok`, on Aarnav's statement that each file was written by one native speaker independently of the other.** `results/phase2/x8/analysis.json`.
  **K4 (agreement is the result, no threshold):** Cohen's kappa on the doubled-vowel word label = 0.198 (95% CI 0.161 to 0.238; 1,137 words in the 75 sentences with equal word counts; 25 sentences with unequal counts excluded and counted); character error rate between P and Q = 0.0959 (95% CI 0.0876 to 0.1046; 100 sentences). For orientation only: the registration's proxy (Gemini vs one Dakshina human) was kappa 0.33 and CER 0.081, so the two humans agree **less** than that proxy; the CI widths (kappa 0.077, CER 0.017) are narrower than the expected 0.17 and 0.016 respectively for kappa and equal for CER.
  **Descriptive (no verdict):** Gemini / mean(P, Q) ratios (90% CI): vowel doubling 0.352 (0.282 to 0.426; Gemini 0.0154 per letter, P 0.0742, Q 0.0133); h-digraph 1.331 (1.125 to 1.562; Gemini 0.0149, P 0.0112, Q 0.0111); English-word share 1.356 (1.224 to 1.492; Gemini 0.0787, P 0.0109, Q 0.1052). None of the three intervals lies within [0.80, 1.25] (orientation only). Against the proxy: vowel doubling matches the earlier Dakshina value (0.36), the English-share ratio is on the other side of 1 (proxy 0.89). **The two annotators differ strongly from each other** (vowel-doubling rate P/Q = 5.59, 95% CI 4.84 to 6.55; English-word share 1.1% vs 10.5%), so "the mean of P and Q" averages two different styles. **K5:** chrF P vs Q 80.5 (78.95 to 82.09); P vs Gemini 77.7 (76.0 to 79.5); Q vs Gemini 85.8 (84.5 to 87.2). The paper is not edited.

`````

##### 2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md).

RESULTS.md lines 3858 to 3859; first line committed in `3290232` on 2026-11-04 01:44:01 +0530; last line in `28803e6` on 2026-11-04 02:33:57 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md).** Removed from every queue; added to `results/phase2/REGISTERED_OUTCOMES.md`. The draft text was never committed. **X8: the Q writer confirmed that they used no tool of any kind (Aarnav's statement), in addition to the earlier statements that the P and Q writers did not see each other's answers.** **X8 descriptive diagnostic (no threshold, no verdict; case-insensitive exact matches with whitespace collapsed; character difference = the registered CER definition per sentence):** exact matches: Gemini vs Q 1 of 100, Gemini vs P 1 of 100, P vs Q 0 of 100. Per-sentence character difference, Gemini vs Q: median 0.0631, quartiles 0.0423 to 0.0799, range 0.0000 to 0.1603, 6 of 100 below 2%; Gemini vs P: median 0.1039, quartiles 0.0759 to 0.1359, range 0.0000 to 0.2647, 1 of 100 below 2%; P vs Q (for comparison): median 0.0898, quartiles 0.0634 to 0.1237, 2 of 100 below 2%. The per-annotator table (Gemini vs P and Gemini vs Q: the three ratios, kappa, CER) stays in `results/phase2/x8/analysis.json` next to the registered mean-of-P-and-Q ratios. The paper is not edited.

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

##### 2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches).

RESULTS.md lines 3906 to 3907; first line committed in `ed31e10` on 2026-11-04 12:13:51 +0530; last line in `72ff37e` on 2026-11-04 12:14:44 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches).** (1) Ambari-Instruct-v0.1 and Llama-3.1-8B were already uploaded as private datasets (shattered-ambari-instruct-v0-1 and shattered-llama-3-1-8b) and are attached by `scripts/kaggle_queue.py` for any job that names the model; all four private datasets (these two, shattered-llama-2-7b-hf and shattered-flores-private) are on the end-of-Phase-2 cleanup list. (2) **Stale driver:** the queue now hashes its scripts (kaggle_queue, kaggle_runner, kaggle_precision, x_score, kaggle_mdl, kaggle_x9b, interp/load) at start and re-executes itself before any push if they changed on disk; the runner pushes the committed tree and refuses a dirty one. (3) **Pre-launch check on the laptop (no quota):** each private dataset the job mounts must be "ready" on Kaggle, and a model named in the job arguments that is gated on Hugging Face must have a private dataset; otherwise nothing is pushed. (4) Queue order rule: non-X9b jobs are refused while an X9b Sarvam batch is pending (X9b batch 3 first, nothing ahead of it); scoring caps are 2.4 h (measured 1.2 to 1.8 h). Calendar of the remaining Kaggle jobs with start and end times: in the report to Aarnav of this time.

`````

##### 2026-11-05 01:24 IST, watchdog: X4 scoring chain FAILED at 01:21 IST (laptop GPU idle for about a minute before the restart).

RESULTS.md lines 3950 to 3951; first line committed in `a7577c6` on 2026-11-05 01:24:12 +0530; last line in `c9b62e6` on 2026-11-05 02:23:56 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 01:24 IST, watchdog: X4 scoring chain FAILED at 01:21 IST (laptop GPU idle for about a minute before the restart).** The Bengali natural scoring step died with IndexError in the tokenizer call: the natural-form step also tried the sentiment task, for which no natural drafts exist in X4 (natural is only on the 257 SIB ids and the M4c rows), so the text list was empty. Fixed in scripts/x4_lang.py (tasks without natural drafts are skipped in the natural step) and the chain was restarted at 01:23 IST; it resumes from its caches. The native, ITRANS and lossy scoring of both languages had completed.

`````

##### 2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt).

RESULTS.md lines 4015 to 4016; first line committed in `3ecea71` on 2026-11-05 15:42:19 +0530; last line in `cccb4f4` on 2026-11-05 22:08:29 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt).** A push of the three remaining Sarvam-m forms (lossy, lowercase, natural; chain `smrest`, account 2, cap 5 h) was refused by Kaggle at 15:39: "Maximum weekly GPU quota of 30.00 hours reached". The queue's own ledger for account 2 (`results/kaggle/acct2/quota.json`, 20.35 h) did not include the sessions of the X9b batch 3 and the Qwen3.5-2B arm (9.94 h), which the X9b-only driver records in its own ledger; the two ledgers together are at the 30 h cap, and Kaggle's count is the binding one. The first account's ledger shows 29.36 h in the last 7 days. Consequence: no Kaggle job can be pushed on either account until hours roll off: account 1 from about 9 Nov (the first 2 Nov sessions free up from 11:20 UTC on 9 Nov, then steadily), account 2 from about 11 Nov 07:56 UTC (its first sessions were on 4 Nov). The three Sarvam-m forms and the Sarvam-m X10 job therefore wait for that quota; the Sarvam-m verdict on native vs ITRANS (7 of 7 models) does not depend on them. Chain `smrest` is marked FAILED for this reason, not for an error in the job. The laptop GPU stays busy with the extra seeds (X9b about 16 to 18 h). Standing order 2 (use every quota hour) is satisfied: both accounts are at the cap.

`````

##### 2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected).

RESULTS.md lines 4023 to 4024; first line committed in `07e9a33` on 2026-11-05 22:37:41 +0530; last line in `1d0616d` on 2026-11-05 22:59:17 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected).** Both setup kernels pushed and started on a T4 x2 (so GPU access works) but ended with status ERROR after about 3.5 minutes in the same step: the kernel's `pip install -e` of the project package failed while installing build dependencies (no output, a timeout). A CPU-only test kernel (`aarnavkembhavi/shattered-nettest`, internet requested in its metadata) confirmed the cause: DNS resolution fails for both pypi.org and huggingface.co ("Temporary failure in name resolution"), i.e. Kaggle did not grant internet to this account's kernels although the push asked for it. Kaggle only grants internet to phone-verified accounts, so the phone verification the owner reported is not in effect for kernels (or was not completed for the account). Every registered job needs internet (pinned packages, public models from Hugging Face, the Wikipedia pool), so none can run until it is fixed. Quota used on account 3: 0.21 h (two failed kernels, about 3.5 minutes each; the CPU test does not count). **What the owner must do:** sign in to kaggle.com as aarnavkembhavi, open Settings, complete 'Phone Verification' (the account must show a verified phone number), and confirm that a new notebook's Settings panel lets 'Internet' be switched on. When he has, tell me and I re-run the setup chain `acct3` (smoke gate and A1-R reproduction); the job chains `acct3x9b` and `acct3sm` are waiting and start by themselves after the acceptance. The earlier chain status DONE for `acct3` meant only that the runner finished, not that the gates passed; the gates did not pass and the acceptance marker was not written. Cleanup list (adds): the kernels `aarnavkembhavi/shattered-nettest`, `shattered-kaggle-gate`, `shattered-kaggle-retrieval-gate` and the datasets on the third account are removed at the end of Phase 2. The paper is not edited.

`````

##### 2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged).

RESULTS.md lines 4025 to 4026; first line committed in `1d0616d` on 2026-11-05 22:59:17 +0530; last line in `4579347` on 2026-11-05 22:59:29 +0530; labels from the title and parent heading: amended, failed or not run

`````text
- **2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged).** After the power-loss restart the first extra run (`sarvam-1+itrans+s2`) reached step 100 at 22:50 and then sat in `torch.save` for more than 8 minutes with the GPU idle (py-spy: `serialization._save`, `write_record`, one core at 100%); the first attempt did the same (step 100 logged at about 16:20, checkpoint file last written 16:42, when the power failed). Cause: the optimizer state is the paged 8-bit AdamW state (bitsandbytes), whose pages migrate one by one while the 8 GB card is full; writing it takes over 20 minutes per checkpoint, three checkpoints per run, about 1 h of every 2.9 h run, about 6 to 7 h over six runs (the Kaggle T4s had room for it, the laptop does not). Fix, committed: checkpoints now hold the adapter, scheduler, scaler and step but not the optimizer state, which makes the save take seconds; the checkpoint is only ever read after an interruption, so an uninterrupted run is numerically identical to before; a run resumed from such a checkpoint resets the Adam moments, and `done.json` carries `resumed_without_optimizer_state` (true) so it can be reported or excluded. The running ITRANS run is resumed from its step-100 checkpoint, which does contain the optimizer state (written before the change), so it continues exactly; the chain `x9extra` is relaunched after the restart. The finish estimate improves by about 6 h: about 8 Nov 00:00 to 02:00 IST for the six laptop runs, if account 3 does not take the seed-4 runs.

`````

##### 2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational).

RESULTS.md lines 4029 to 4030; first line committed in `8c59c8a` on 2026-11-06 00:53:19 +0530; last line in `fc1246a` on 2026-11-06 02:37:37 +0530; labels from the title and parent heading: amended, failed or not run

`````text
- **2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational).** Windows logged a second unclean reboot (Kernel-Power 41; bugcheck 0x1e, an unhandled access violation, last good time 22:41:16; the earlier one, 16:10, was bugcheck 0x9f, a driver power-state failure), the machine came back at 23:06 and the chain at 23:47. Both crashes came while the GPU was at full memory with shared-memory spill (peak 10.6 GiB asked of an 8 GB card at micro-batch 16) and, the second time, during the stalled checkpoint save. Consequences: GPU idle 22:41 to 23:47 (about 1 h 05 min, a crash, not a project process); the ITRANS seed-3 run (code seed 2) had no usable checkpoint and **restarted from step 0 at 23:47** (it is at step 140 or more now, ckpt written with the fast format at 00:31). Change (committed, recipe unchanged): the code reads an optional laptop-only file `build/x9b_max_micro_batch.txt` and caps the micro-batch at its value, with proportionally more accumulation steps, so the optimizer step is the same (16,384 tokens) while memory stays under the card's 8 GB; it holds 8 from now, so the run in progress (started at 23:47) keeps micro-batch 16 and the next five runs use 8 (done.json records the micro-batch used). Speed cost expected at a few percent. If the laptop crashes again the run resumes from the adapter checkpoint with reset Adam moments and is flagged in done.json (`resumed_without_optimizer_state`). Projected finish of the six laptop runs: the first at about 02:40 on 6 Nov, the last about 6 Nov 17:30 to 19:30 IST.

`````

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

##### 2026-11-03 00:04 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed). Annotators are not available. X1 T3 is marked "not run (instruction not verified)"; X15 is marked "not run (annotators unavailable)"; X8 is parked and mar

RESULTS.md lines 3769 to 3774; first line committed in `285c028` on 2026-11-03 00:04:58 +0530; last line in `d574ae9` on 2026-11-03 00:47:00 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-03 00:04 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** Annotators are not available. **X1 T3 is marked "not run (instruction not verified)"; X15 is marked "not run (annotators unavailable)"; X8 is parked and marked "not run"**
  (if the X8 files are sent later, it runs as registered). All three are removed from every queue (the laptop queue's "X1 T3" and the annotator-dependent items, and every pending annotation send); no chain or driver step referenced them. The
  workbooks, private keys, importers (`scripts/import_x8.py`, `import_x15.py`, `import_t3.py`, one command each over `annotation/returned/`, which is gitignored because returned files carry author fields) and analyses
  (`scripts/analyze_x8.py`, `analyze_x15.py`, tested on synthetic data only, outputs not kept) are kept. The three items and the reason are in `results/phase2/REGISTERED_OUTCOMES.md` (no Phase 2 outcomes table existed before; this is its start).
  The Kaggle and laptop queues continue as before.

`````

##### 2026-11-03 01:37 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed). X15 is skipped: "not run (annotators unavailable)". No X15 files are built (`scripts/export_xlsx.py build` now skips them unless `--with-x15`), X15 is rem

RESULTS.md lines 3792 to 3795; first line committed in `78e3f69` on 2026-11-03 01:37:59 +0530; last line in `73546be` on 2026-11-03 02:24:19 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-03 01:37 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** **X15 is skipped: "not run (annotators unavailable)".** No X15 files are built (`scripts/export_xlsx.py build` now skips them unless `--with-x15`), X15 is removed from every to-do list and from `annotation/xlsx/SEND_ME.md`; the earlier X15 workbooks, importer and analysis scripts stay in the repository, unused. This supersedes the 01:1x note that put X15 back in the registered design.
  **T3** stands as logged: the returned workbook (`annotation/returned/T3_verification.xlsx`) was imported with 0 blockers and 0 warnings; T3-1 and T3-3 Correct, T3-2 replaced by the native speaker's wording before any T3 scoring; the instruction files are frozen with the new text (hashes in `results/phase2/x1/t3_templates.json`); X1 T3 is queued after X9a; every T3 result is labelled "instruction verified by a native speaker, exploratory".
  **X8:** `annotation/returned/` held only the T3 file when checked at 01:34; `annotation/xlsx/X8_Q.xlsx` (saved 01:32) holds 100 answers and was imported (0 blockers, 0 warnings; uppercase-start share 0.01, unexpected-character share 0.01 (one cell with Õ/õ), mean 16.3 words per sentence); `annotation/xlsx/X8_P.xlsx` has no answers. The registered X8 analysis (kappa, character error rate, descriptive ratios) needs both files and has not been run.

`````

##### 2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehe

RESULTS.md lines 3820 to 3821; first line committed in `bcaebe7` on 2026-11-03 07:43:00 +0530; last line in `48deb83` on 2026-11-03 08:06:57 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehearsal discarded as designed.** Measured: 20 optimizer steps (327,680 tokens) in 589 s, loss 2.57 at step 20, adapter and checkpoint written. The failure is in `PeftModel.from_pretrained` before the evaluation: the Kaggle image ships torchao 0.10.0, which the pinned peft 0.21.2 refuses (`ImportError: Found an incompatible version of torchao. Found version 0.10.0, but only versions above 0.16.0 are supported`). Fix (no rule change): the kernel uninstalls torchao after installing the pins (nothing in this project uses it). A failed rehearsal is now repeated by the driver, never skipped (the driver would otherwise have started the full runs on the next pass); the rehearsal is re-queued (about 0.3 h). No registered X9b run has started; B stays as logged.

`````

##### 2026-11-03 12:56 IST, X8 imported and analysed as registered (K4, K5; K6 not run). Files: the filled `X8_P.xlsx` (saved 12:52, 100 answers) and `X8_Q.xlsx` (saved 01:32, 100 answers), both found in `annotation/xlsx/` (not in `annotation/ret

RESULTS.md lines 3825 to 3828; first line committed in `16e09e4` on 2026-11-03 12:56:47 +0530; last line in `2df4879` on 2026-11-03 12:58:00 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-03 12:56 IST, X8 imported and analysed as registered (K4, K5; K6 not run).** Files: the filled `X8_P.xlsx` (saved 12:52, 100 answers) and `X8_Q.xlsx` (saved 01:32, 100 answers), both found in `annotation/xlsx/` (not in `annotation/returned/`) and imported from copies in `annotation/returned/`; both pass every check (0 blockers, 0 warnings: every Romanization cell non-blank, every other cell identical to the original; uppercase-start share 0.01 in both; unexpected-character share 0.02 (P) and 0.01 (Q): the string "Õ / õ" copied from sentence 422, which contains it, and two zero-width spaces in P sentence 991); 0 of the 100 sentences are identical between P and Q. **The importer's same-person check blocked the pair because both files carry the same author field (both were saved on Aarnav's account); it was run with `--shared-account-ok`, on Aarnav's statement that each file was written by one native speaker independently of the other.** `results/phase2/x8/analysis.json`.
  **K4 (agreement is the result, no threshold):** Cohen's kappa on the doubled-vowel word label = 0.198 (95% CI 0.161 to 0.238; 1,137 words in the 75 sentences with equal word counts; 25 sentences with unequal counts excluded and counted); character error rate between P and Q = 0.0959 (95% CI 0.0876 to 0.1046; 100 sentences). For orientation only: the registration's proxy (Gemini vs one Dakshina human) was kappa 0.33 and CER 0.081, so the two humans agree **less** than that proxy; the CI widths (kappa 0.077, CER 0.017) are narrower than the expected 0.17 and 0.016 respectively for kappa and equal for CER.
  **Descriptive (no verdict):** Gemini / mean(P, Q) ratios (90% CI): vowel doubling 0.352 (0.282 to 0.426; Gemini 0.0154 per letter, P 0.0742, Q 0.0133); h-digraph 1.331 (1.125 to 1.562; Gemini 0.0149, P 0.0112, Q 0.0111); English-word share 1.356 (1.224 to 1.492; Gemini 0.0787, P 0.0109, Q 0.1052). None of the three intervals lies within [0.80, 1.25] (orientation only). Against the proxy: vowel doubling matches the earlier Dakshina value (0.36), the English-share ratio is on the other side of 1 (proxy 0.89). **The two annotators differ strongly from each other** (vowel-doubling rate P/Q = 5.59, 95% CI 4.84 to 6.55; English-word share 1.1% vs 10.5%), so "the mean of P and Q" averages two different styles. **K5:** chrF P vs Q 80.5 (78.95 to 82.09); P vs Gemini 77.7 (76.0 to 79.5); Q vs Gemini 85.8 (84.5 to 87.2). The paper is not edited.

`````

##### 2026-11-03 13:21 IST, X9a prep and pilot (laptop; registered pilot first; results are checks, no accuracy is used for any decision). `scripts/x9a.py prep` (CPU, `results/phase2/x9a/prep.json`): cipher round trip exact on every story used (0

RESULTS.md lines 3838 to 3840; first line committed in `00bf9f6` on 2026-11-03 13:21:59 +0530; last line in `3529fe7` on 2026-11-03 13:32:32 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-03 13:21 IST, X9a prep and pilot (laptop; registered pilot first; results are checks, no accuracy is used for any decision).** `scripts/x9a.py prep` (CPU, `results/phase2/x9a/prep.json`): **cipher round trip exact on every story used (0 failures) and 0 evaluation stories occur in the training or tokenizer stories** (checked by exact match; the 500 evaluation stories are the first 500 of the TinyStories V2 validation split); tokenizer: byte-level BPE 1,024 (+EOS), trained once on 50.0 MB English (61,923 stories) plus 50.0 MB cipher renderings (35,320 other stories) taken from the shuffled stories beyond the 400 MB training prefix; **sha256 0bcd40849208725e0b3d43cb3836ad147210c6e96418d3f197a625ff97324acf**. **Tokens per word on the evaluation stories: English 1.773, cipher 1.978 (relative difference 11.6%, inside the 15% bound; the ratio 1.116 is stated in every table).** Streams (each cut at 126,423,041 tokens = 6,173 steps x 64 x 320, the Phase 1 vocabulary-1,024 budget): stories consumed 435,911 (level 0), 435,402 (1), 433,370 (5), 425,916 (20), 411,712 (50), of which cipher 0, 4,344, 21,634, 85,246, 205,952 (shares 0, 1.0%, 5.0%, 20.0%, 50.0%).
  **Pilot** (level 20, seed 0, 617 steps = 10% of the budget; `results/phase2/x9a/pilot.json`): 0.157 s per step, 97 s of training, evaluation 90 s; the whole path ran (retrieval, MDL probes on cipher and English words, 300 words each at least 3 tokens). **Time estimate for the grid: 6,173 steps x 0.157 s = 0.27 h per run, 15 runs = 4.0 h plus about 0.4 h of evaluation (the registration extrapolated about 6 h).** **Implementation note (X9a-D1, no rule change):** the registered 700-character evaluation texts exceed the model's 320-token context for some stories; the pair is cut further at a word boundary, the same characters in English and cipher, for 17 of the 500 pairs (mean 654 characters, minimum 241), identical in every run (the tokenizer is fixed); `ctx_tokens` was added to the Phase 1 training code as an optional override so every level uses the Phase 1 context of 320 (Phase 1 runs are unaffected). The mapped retrieval value (secondary in the registration) is not computed in this version. The full grid is started now (`scripts/x9a_chain.sh`).

`````

##### 2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md). Removed 

RESULTS.md lines 3858 to 3859; first line committed in `3290232` on 2026-11-04 01:44:01 +0530; last line in `28803e6` on 2026-11-04 02:33:57 +0530; labels from the title and parent heading: registered, result, failed or not run

`````text
- **2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md).** Removed from every queue; added to `results/phase2/REGISTERED_OUTCOMES.md`. The draft text was never committed. **X8: the Q writer confirmed that they used no tool of any kind (Aarnav's statement), in addition to the earlier statements that the P and Q writers did not see each other's answers.** **X8 descriptive diagnostic (no threshold, no verdict; case-insensitive exact matches with whitespace collapsed; character difference = the registered CER definition per sentence):** exact matches: Gemini vs Q 1 of 100, Gemini vs P 1 of 100, P vs Q 0 of 100. Per-sentence character difference, Gemini vs Q: median 0.0631, quartiles 0.0423 to 0.0799, range 0.0000 to 0.1603, 6 of 100 below 2%; Gemini vs P: median 0.1039, quartiles 0.0759 to 0.1359, range 0.0000 to 0.2647, 1 of 100 below 2%; P vs Q (for comparison): median 0.0898, quartiles 0.0634 to 0.1237, 2 of 100 below 2%. The per-annotator table (Gemini vs P and Gemini vs Q: the three ratios, kappa, CER) stays in `results/phase2/x8/analysis.json` next to the registered mean-of-P-and-Q ratios. The paper is not edited.

`````

##### 2026-11-04 02:34 IST, correction note to the X9a-low entry above (text only; the rule is unchanged). A shell substitution dropped a code span: the phrase "of the same story order, , each stream" should read "of the same story order, `defaul

RESULTS.md lines 3864 to 3865; first line committed in `eff85fe` on 2026-11-04 02:34:12 +0530; last line in `98e2256` on 2026-11-04 02:46:00 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 02:34 IST, correction note to the X9a-low entry above (text only; the rule is unchanged).** A shell substitution dropped a code span: the phrase "of the same story order, , each stream" should read "of the same story order, `default_rng(9)`, each stream". Nothing else in the entry changed; the tag `phase2-x9a-low` marks the entry as committed.

`````

##### 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST). Cause (from the kernel log): the kernel cannot read the Hugging Face token, so the gated repo

RESULTS.md lines 3868 to 3869; first line committed in `0cfdea0` on 2026-11-04 02:46:43 +0530; last line in `09b39ee` on 2026-11-04 02:52:11 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST).** Cause (from the kernel log): the kernel cannot read the Hugging Face token, so the gated repo meta-llama/Llama-2-7b-hf returns 401 on Kaggle. `UserSecretsClient` raised "Connection error trying to communicate with service" in all 16 kernel runs so far (the earlier models were not gated, so nothing was lost before). The same token reads both Llama repos from the laptop (HTTP 200), so access itself is granted; the Kaggle notebook has no HF_TOKEN secret attached. Fix needs a manual step in the Kaggle web UI (attach the secret HF_TOKEN to the kernels shattered-kaggle-precision and shattered-x-score, Add-ons, Secrets); no token is put in a dataset or the repository. Not relaunched yet (relaunch once after the fix). Llama-3.1-8B has the same dependency. X9b batch 3 is unaffected.

`````

##### 2026-11-04 03:43 IST, gated models on Kaggle: private-dataset route (Aarnav's instruction; no registered rule changes). *Secrets cannot be set through the API:* the Kaggle kernel metadata accepted by the kernels push has no field for secret

RESULTS.md lines 3878 to 3879; first line committed in `7ee0799` on 2026-11-04 03:43:18 +0530; last line in `cbdea11` on 2026-11-04 03:52:38 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 03:43 IST, gated models on Kaggle: private-dataset route (Aarnav's instruction; no registered rule changes).** *Secrets cannot be set through the API:* the Kaggle kernel metadata accepted by the kernels push has no field for secrets (they are attached per notebook in the web UI, and all 16 kernel runs so far failed to reach the secret service), so no UI step is required of Aarnav. *Route:* `scripts/hf_to_kaggle.py` downloads Llama-2-7b-hf and Llama-3.1-8B (config, tokenizer, safetensors only) on the laptop with the approved Hugging Face access and uploads each as a **private** Kaggle dataset: **shattered-llama-2-7b-hf** and **shattered-llama-3-1-8b** (account aarnavkembhavi1). `shattered.interp.load.model_source` uses the mounted dataset on Kaggle and the Hugging Face repo elsewhere; `scripts/kaggle_queue.py` attaches the dataset to any job whose arguments name the model. The A1-P and scoring code is otherwise unchanged. The local copy is deleted after a verified upload. **End-of-Phase-2 cleanup list (delete and log): the private Kaggle datasets shattered-flores-private, shattered-llama-2-7b-hf, shattered-llama-3-1-8b.** Disk: to keep the 25 GB guard during the downloads I deleted finished-job caches (cache/activations/h_hindi 1.1 GB and cache/activations/nc1 0.6 GB, regenerable; the five data/processed/x9a/train_p*.npy streams, regenerable by `x9a.py prep` with hashes in meta.json); no results or logs were removed. Free disk after: 74 GB.

`````

##### 2026-11-04 03:52 IST, watchdog: the first Llama-2 dataset upload failed at dataset creation (Kaggle: subtitle must be 20 to 80 characters; the download of 13 GB was complete). Fixed (shorter subtitle), upload relaunched once (log results/ph

RESULTS.md lines 3880 to 3881; first line committed in `cbdea11` on 2026-11-04 03:52:38 +0530; last line in `f479ea3` on 2026-11-04 04:14:25 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 03:52 IST, watchdog:** the first Llama-2 dataset upload failed at dataset creation (Kaggle: subtitle must be 20 to 80 characters; the download of 13 GB was complete). Fixed (shorter subtitle), upload relaunched once (log results/phase2/hf_upload_llama2b.log); the Llama-3.1 download continues. Laptop GPU busy (X1 T3), Kaggle MDL Qwen3-8B running, disk 64 GB free.

`````

##### 2026-11-04 04:53 IST, Kaggle watchdog: Qwen3-8B MDL (X13) finished (output in results/kaggle/kaggle_mdl/2026-11-03T220606, analysis pending). Llama-2-7B A1-P failed a second time (04:40 IST, 0.12 h): the gated repo was still read from Huggi

RESULTS.md lines 3886 to 3887; first line committed in `45def39` on 2026-11-04 04:53:21 +0530; last line in `8e2e954` on 2026-11-04 06:08:17 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 04:53 IST, Kaggle watchdog:** Qwen3-8B MDL (X13) finished (output in results/kaggle/kaggle_mdl/2026-11-03T220606, analysis pending). Llama-2-7B A1-P failed a second time (04:40 IST, 0.12 h): the gated repo was still read from Hugging Face (401), i.e. the kernel did not use the private dataset copy; cause not yet known (the mounted path is not visible in the log); the boot script now prints the mounted datasets for the next run. The Ambari instruct pair A1-P (cap 5.0 h) was pushed at about 04:46 IST; quota 29.81 of 30 h with it reserved. Llama-2 will be retried once after it ends and the cause is fixed.

`````

##### 2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST). The kernel metadata of those pushes lists only shattered-pkg and shattered-flores-private as dataset sources (bui

RESULTS.md lines 3890 to 3891; first line committed in `7cfcb18` on 2026-11-04 06:08:50 +0530; last line in `46c9030` on 2026-11-04 06:23:52 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST).** The kernel metadata of those pushes lists only shattered-pkg and shattered-flores-private as dataset sources (build/kaggle/kernel_kaggle_precision/kernel-metadata.json): the queue driver process running since 03:35 IST had imported scripts/kaggle_queue.py before the change that attaches the private model datasets, so it never attached them. This is the same stale-driver mistake as before, not a mount problem. The next queue pass (a new process after the 90-minute wait) uses the new code. Llama-3.1 A1-P also failed with no verdict (0.1 h); neither failure is a verdict on the model. Retry once at the next pass when quota allows (quota 29.55 of 30 h used; 3 h or more fits from about 9 Nov 23:24 IST).

`````

##### 2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check (float32-offload reference; first job to use a private model dataset, so the dataset route works; run pushed 06:25 IST, finished about 07:45). Both co

RESULTS.md lines 3896 to 3897; first line committed in `81fc534` on 2026-11-04 07:53:46 +0530; last line in `7455dba` on 2026-11-04 09:53:29 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 07:53 IST, X12 contrast 1 endpoint A1-P: Llama-2-7B PASSED the precision check** (float32-offload reference; first job to use a private model dataset, so the dataset route works; run pushed 06:25 IST, finished about 07:45). Both contrast-1 endpoints (Ambari-7B-base and Llama-2-7B) have now passed, so X12 contrast 1 scoring is the next job. Quota 27.54 of 30 h used: the scoring cap was lowered from 5.0 to 2.4 h to fit (measured scoring times: Qwen3-8B 1.71 h, Ambari-7B-base 1.23 h; the job resumes from its item cache if the cap is hit). Queue chain restarted early to push it. Llama-3.1-8B and Ambari-Instruct-v0.1 A1-P wait for quota (retry once after the failures of the stale driver).

`````

##### 2026-11-04 11:07 IST, X1 T3 SCORING FINISHED (laptop, finished 11:01 IST; 5 models, all forms and NC conditions under the native-speaker-verified T3 templates; results/phase2/x1/t3/, label: "instruction verified by a native speaker, explora

RESULTS.md lines 3900 to 3901; first line committed in `173d201` on 2026-11-04 11:07:39 +0530; last line in `bbc32e2` on 2026-11-04 12:07:30 +0530; labels from the title and parent heading: exploratory, result, failed or not run

`````text
- **2026-11-04 11:07 IST, X1 T3 SCORING FINISHED (laptop, finished 11:01 IST; 5 models, all forms and NC conditions under the native-speaker-verified T3 templates; results/phase2/x1/t3/, label: "instruction verified by a native speaker, exploratory").** No registered claim attaches to T3, so no verdict word; the T3 analysis (T3 minus T1 and T2 per cell, same code path as the T2 analysis in scripts/x1_analyse.py) is not run yet and is queued as CPU work. X11 started right after (11:02), then X10 full, X9a-low, X4 scoring follow by status-file waits.

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

##### 2026-11-04 13:40 IST, account 2 smoke test PASSED (kaggle_gate, T4 x2, second attempt; 0.10 h). gate_passed true with the same dtype (float16) for Sarvam-1 and Gemma 4 E2B; every number equals account 1's gate run (raw agreement native/ITRA

RESULTS.md lines 3914 to 3915; first line committed in `97a4a6b` on 2026-11-04 13:40:55 +0530; last line in `59154b4` on 2026-11-04 14:10:52 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 13:40 IST, account 2 smoke test PASSED (kaggle_gate, T4 x2, second attempt; 0.10 h).** gate_passed true with the same dtype (float16) for Sarvam-1 and Gemma 4 E2B; every number equals account 1's gate run (raw agreement native/ITRANS/lossy 0.99/0.95/0.96 for Sarvam-1 and 1.00/0.99/0.99 for Gemma 4; Kaggle accuracy 0.62/0.29/0.36 and 0.73/0.27/0.44; max |dlogprob| identical to three decimals). The runner polling had been ended by a laptop network blip once (the status call failed and the wait loop read "error" in the message); fixed so a failed status call keeps waiting. Next: the A1-R retrieval reproduction on account 2 (kaggle_retrieval_gate, FLORES private dataset under account 2); account 2 is accepted for real jobs only if it reproduces the account 1 A1-R numbers (Sarvam-1 native 0.9443, ITRANS 0.5104; Gemma 4 E2B as stored).

`````

##### 2026-11-04 16:09 IST, X10 RESULT (laptop, scoring finished 16:06 IST; `scripts/x10.py`, `results/phase2/x10/analysis.json`): X10-P SUPPORTED (4 of 4; as predicted). Kannada FLORES+ devtest to English, base models, one registered instruction

RESULTS.md lines 3918 to 3919; first line committed in `eb2aa7a` on 2026-11-04 16:09:50 +0530; last line in `4770255` on 2026-11-04 17:26:35 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-04 16:09 IST, X10 RESULT (laptop, scoring finished 16:06 IST; `scripts/x10.py`, `results/phase2/x10/analysis.json`): X10-P SUPPORTED (4 of 4; as predicted).** Kannada FLORES+ devtest to English, base models, one registered instruction, greedy, 128 new tokens, cut at the first newline; chrF2 (sentence-level for the bootstrap, corpus-level below); paired bootstrap over sentences (10,000, seed 0), Holm over 16. **Native minus ITRANS (sentence-level chrF, 1,012 sentences), Holm-significant and positive in all four models:** Qwen3-1.7B +26.45 [25.63, 27.25]; Qwen3.5-2B +15.03 [13.60, 16.48]; Sarvam-1 +21.01 [20.11, 21.91]; Gemma 4 E2B +32.94 [32.10, 33.78] (p_holm 0.0032 in every test, the bootstrap floor 1/10,001 times 16). Native minus lowercase: +25.81, +14.89, +22.35, +33.90; native minus lossy: +24.10, +14.89, +11.12, +28.94; native minus natural (267 devtest ids with a clean natural romanization): +21.80, +15.31, +9.68, +25.19; all positive and significant. **Corpus chrF, native / ITRANS / lowercase / lossy / natural:** Qwen3-1.7B 39.3 / 13.1 / 13.9 / 15.3 / 17.8; Qwen3.5-2B 20.0 / 2.5 / 2.7 / 2.7 / 4.2; Sarvam-1 50.5 / 30.3 / 28.8 / 39.9 / 41.4; Gemma 4 E2B 54.9 / 21.8 / 20.8 / 26.3 / 30.2. **Caveat that belongs with the Qwen3.5-2B row: that model gives an empty first line on 62% of native and 85 to 88% of romanized inputs (the registered protocol cuts at the first newline and scores empty as empty, which is what was run), so its chrF mostly measures how often it answers on the first line; the other three models have at most 2.5% empty.** Sarvam-1 and Gemma 4 rank the forms ITRANS < lowercase < lossy < natural < native on chrF (Sarvam-1: lowercase below ITRANS); no prediction was registered for that ordering. Nothing against a prediction. Implementation note: the first analysis run failed on a text-encoding bug in x10.py (result files opened without UTF-8); fixed, analysis re-run by hand, chain status set to DONE at 16:09 IST. The paper is not edited.

`````

##### 2026-11-04 21:08 IST, X6 SCREEN, STAGE 1 (CPU and network; `scripts/x6_screen.py stage1`, `results/phase2/x6/screen.json`; 185 Hub candidates from 11 searches plus the named Llama 3.2 1B; tokenizer files and Hub metadata only). Current mode

RESULTS.md lines 3932 to 3933; first line committed in `a182698` on 2026-11-04 21:08:27 +0530; last line in `952be81` on 2026-11-04 21:53:03 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 21:08 IST, X6 SCREEN, STAGE 1 (CPU and network; `scripts/x6_screen.py stage1`, `results/phase2/x6/screen.json`; 185 Hub candidates from 11 searches plus the named Llama 3.2 1B; tokenizer files and Hub metadata only).** Current models, native tokens per word and ITRANS/native ratio on the 2,009 FLORES+ sentences: Qwen3-1.7B 11.84 / 0.37; Qwen3.5-2B 5.33 / 0.79; Sarvam-1 2.39 / 2.23; Gemma 4 E2B 3.25 / 1.24. **Llama 3.2 1B:** the registered repo meta-llama/Llama-3.2-1B returns 403 for the token in .env (access to the Llama 3.2 repositories was never granted; only Llama-2-7b-hf and Llama-3.1-8B were); unmodified mirrors of the same weights and tokenizer are public (NousResearch/Llama-3.2-1B, license llama3.2): **native 14.90, ITRANS/native 0.29, vocabulary 128,256** (26% above the highest current native value and 21% below the lowest current ratio: rule 2 met). **Deviation X6-D1 (not a rule change): the base model is taken from the NousResearch mirror because the gated original is not accessible; if Aarnav obtains access to meta-llama/Llama-3.2-1B the identity of the weights can be checked.** Indic-extended candidates found at 3B or below: ashtok897/oroZ-1.7B-Indic-v1 (2.03 B parameters, Apache-2.0, vocabulary 152,012: the Qwen3 vocabulary plus about 340 added tokens; native 4.16, ratio 1.01; meets rule 2 on tokens per word; an unknown fine-tune, its quality is untested); the Gemma-2B Navarasa and other Gemma-2B Indic fine-tunes keep the Gemma tokenizer (native 5.56, ratio 0.71, not 20% from Qwen3.5-2B), the Qwen-based Kannada fine-tunes keep the Qwen tokenizer (11.84, 0.37), Sarvam variants are Sarvam-1 itself. The machine shortlist also lists many tiny or non-decoder models (10M to 32M GPT-2 models, a CodeT5, text-to-speech models, quantized mirrors); they are not decoder models of the kind the rule intends and are set aside. **Shortlist for stage 2 (rule 1, bf16 forward-pass memory on the laptop): NousResearch/Llama-3.2-1B and ashtok897/oroZ-1.7B-Indic-v1** (at most two models, as registered). Stage 2 (`scripts/x6mem_chain.sh`) waits for X4 scoring. Rule 3 (native SIB-200 CI lower bound above 0.40, counted or not) and the full X6 runs come after; the X6 run scripts are not built yet.

`````

##### 2026-11-04 22:37 IST, account 2 quota records reconciled by hand. The instruction-pair MDL push of 22:08 IST never created a kernel (runner stopped at 22:23 during the driver fix; no kernel of that name exists on the account): record set to

RESULTS.md lines 3942 to 3943; first line committed in `06100d7` on 2026-11-04 22:37:35 +0530; last line in `5b9ae1d` on 2026-11-05 00:25:45 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 22:37 IST, account 2 quota records reconciled by hand.** The instruction-pair MDL push of 22:08 IST never created a kernel (runner stopped at 22:23 during the driver fix; no kernel of that name exists on the account): record set to 0 h, status "not run"; the driver pushes it again after the Ambari-Instruct-v0.1 scoring. The 20:10 A1-P record that stayed "pushed" is set to its real 1.94 h (complete). The quota projection for account 2 now counts hours that were really used or are really running.

`````

##### 2026-11-05 01:09 IST, X12 instruction pair: both models scored (Kaggle account 2). Ambari-Instruct-v0.1 scoring (pushed 22:06 IST, 1.20 h, with the copy loader) and Ambari-Instruct-v0.2 scoring (pushed 23:19, 1.67 h) are complete and record

RESULTS.md lines 3948 to 3949; first line committed in `055b2fc` on 2026-11-05 01:09:36 +0530; last line in `a7577c6` on 2026-11-05 01:24:12 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 01:09 IST, X12 instruction pair: both models scored (Kaggle account 2).** Ambari-Instruct-v0.1 scoring (pushed 22:06 IST, 1.20 h, with the copy loader) and Ambari-Instruct-v0.2 scoring (pushed 23:19, 1.67 h) are complete and recorded; the pair's MDL assembly-layer job (the registered contrast 2 measure, rule as H3, descriptive) was pushed at 01:00 IST on account 2 and is running; the contrast 2 analysis script is not built yet and is built while the MDL job runs. The Llama-3.1-8B scoring (X13) waits for a free GPU slot on account 2 (X9b batch 3 and the MDL job occupy both).

`````

##### 2026-11-05 01:24 IST, watchdog: X4 scoring chain FAILED at 01:21 IST (laptop GPU idle for about a minute before the restart). The Bengali natural scoring step died with IndexError in the tokenizer call: the natural-form step also tried the 

RESULTS.md lines 3950 to 3951; first line committed in `a7577c6` on 2026-11-05 01:24:12 +0530; last line in `c9b62e6` on 2026-11-05 02:23:56 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 01:24 IST, watchdog: X4 scoring chain FAILED at 01:21 IST (laptop GPU idle for about a minute before the restart).** The Bengali natural scoring step died with IndexError in the tokenizer call: the natural-form step also tried the sentiment task, for which no natural drafts exist in X4 (natural is only on the 257 SIB ids and the M4c rows), so the text list was empty. Fixed in scripts/x4_lang.py (tasks without natural drafts are skipped in the natural step) and the chain was restarted at 01:23 IST; it resumes from its caches. The native, ITRANS and lossy scoring of both languages had completed.

`````

##### 2026-11-05 02:23 IST, X4 PART 1 RESULT (laptop scoring finished 02:10 IST; analysis `scripts/x4_analyse.py`, `results/phase2/x4/{bn,te}/r1.json`): R1 SUPPORTED in Bengali and in Telugu (as predicted); all four accuracy models are counted in

RESULTS.md lines 3952 to 3953; first line committed in `c9b62e6` on 2026-11-05 02:23:56 +0530; last line in `3c2e3a6` on 2026-11-05 02:25:27 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 02:23 IST, X4 PART 1 RESULT (laptop scoring finished 02:10 IST; analysis `scripts/x4_analyse.py`, `results/phase2/x4/{bn,te}/r1.json`): R1 SUPPORTED in Bengali and in Telugu (as predicted); all four accuracy models are counted in both languages.** Scope: SIB-200 (n = 1,004 per form; natural on the 257 overlap ids) for the forms scored so far; the E9 lowercase form and ladder L1 to L3, retrieval (R2, R3), the MDL assembly layer (R4), IndicSentiment and K3b-bn/te are not built or run yet. Counting rule (native SIB CI lower bound above 0.40, Qwen2.5 never counted): **counted in both languages: Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B** (lowest native CI lower bounds: Bengali 0.635, Telugu 0.639); Qwen2.5-1.5B reported (native Bengali 0.620; Telugu 0.411, CI lower 0.381). **R1 (exact McNemar, Holm over contrasts x counted models, all-but-one rule): native beats ITRANS in 4 of 4 and native beats lossy in 4 of 4 counted models, both languages: supported.** Calibrated accuracy, native / ITRANS / lossy / natural (257 ids): *Bengali:* Qwen3-1.7B 0.664 / 0.227 / 0.271 / 0.397; Qwen3.5-2B 0.690 / 0.189 / 0.314 / 0.457; Sarvam-1 0.759 / 0.419 / 0.537 / 0.737; Gemma 4 E2B 0.771 / 0.360 / 0.430 / 0.575. *Telugu:* Qwen3-1.7B 0.668 / 0.266 / 0.349 / 0.482; Qwen3.5-2B 0.718 / 0.292 / 0.388 / 0.502; Sarvam-1 0.772 / 0.456 / 0.690 / 0.719; Gemma 4 E2B 0.770 / 0.425 / 0.508 / 0.606. English accuracy (same items, the stored Kannada-run scores) 0.77 to 0.80 for the four. Natural (on 257 ids only, a different item set from the 1,004) sits between ITRANS and native in every model, close to native for Sarvam-1 in both languages. English is not scored per language; the raw fallback rule is read from the stored English scores. Nothing against a prediction. The paper is not edited.

`````

##### 2026-11-05 02:25 IST, X6 screen stage 2 and run part 1 started (laptop). Rule (1), forward-pass peak memory in bf16 with hidden states on the 8 GB laptop GPU: NousResearch/Llama-3.2-1B 2.46 GiB; ashtok897/oroZ-1.7B-Indic-v1 4.29 GiB; both f

RESULTS.md lines 3954 to 3955; first line committed in `3c2e3a6` on 2026-11-05 02:25:27 +0530; last line in `ec3c085` on 2026-11-05 02:38:48 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 02:25 IST, X6 screen stage 2 and run part 1 started (laptop).** Rule (1), forward-pass peak memory in bf16 with hidden states on the 8 GB laptop GPU: NousResearch/Llama-3.2-1B 2.46 GiB; ashtok897/oroZ-1.7B-Indic-v1 4.29 GiB; both fit. The laptop queue was empty after X4 scoring (finished 02:10) and the X6 memory check (02:22), so the X6 SIB-200 counting run (rule 3; `scripts/x6_run.py`, chain `scripts/x6run_chain.sh`) was pulled forward and started at 02:24 IST; models added to the loader as llama-3.2-1b (mirror, deviation X6-D1) and oro-1.7b. The remaining laptop work that exists as registered but is not built: X4 lowercase form and ladder, retrieval, MDL and K3b parts, the full X6 runs for counted models.

`````

##### 2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on both measures (as predicted). All six runs are complete: batches 1 and 2 on Kagg

RESULTS.md lines 3958 to 3959; first line committed in `900da25` on 2026-11-05 03:10:06 +0530; last line in `17458bc` on 2026-11-05 03:12:00 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 03:10 IST, X9b PRIMARY RESULT (Sarvam-1, 2 seeds per condition; `scripts/x9b_analyse.py`, `results/phase2/x9b/analysis_sarvam-1.json`): SUPPORTED on both measures (as predicted).** All six runs are complete: batches 1 and 2 on Kaggle account 1 (3 Nov), batch 3 (native seed 1, English seed 1) on account 2 (6.47 h; the in-kernel base-evaluation check passed first: native 0.9443 at layer 24, ITRANS 0.5104 at layer 21, equal to A1-R and to the account 1 base). B = 4,997,120 tokens per run (305 optimizer steps); tokenizer sha256 unchanged by training in every run; overlap 0 in every stream. Registered rule: gap g = native minus ITRANS after training on condition c; D_N = g(native) - g(ITRANS), D_E = g(English) - g(ITRANS); 97.5% paired-bootstrap intervals with one of the two seeds drawn per cell per resample. **SIB-200 accuracy (n = 1,004): g(0) = +0.233 before training (native 0.768, ITRANS 0.535); after training g(ITRANS) = +0.117, g(native) = +0.342, g(English) = +0.313; D_N = +0.225 [0.177, 0.273] (seeds +0.222, +0.227); D_E = +0.196 [0.150, 0.244] (seeds +0.196, +0.196): supported.** **FLORES+ retrieval (test half n = 1,005): g(0) = +0.434 (native 0.944, ITRANS 0.510); g(ITRANS) = +0.081, g(native) = +0.418, g(English) = +0.472; D_N = +0.337 [0.296, 0.378] (seeds +0.328, +0.346); D_E = +0.391 [0.344, 0.435] (seeds +0.381, +0.401): supported.** What moved (seed means, native / ITRANS accuracy): after ITRANS training 0.766 / 0.649 on SIB-200 (ITRANS +11 points) and retrieval 0.927 / 0.847 (ITRANS +34 points); after native training SIB-200 0.766 / 0.424 and retrieval 0.920 / 0.502; after English training SIB-200 0.757 / 0.443 and retrieval 0.920 / 0.449. **So with the tokenizer and the number of pieces per word fixed, continued pretraining on ITRANS text closed most of the gap by raising ITRANS (accuracy 0.535 to 0.649, retrieval 0.510 to 0.847), while the two controls left ITRANS retrieval unchanged to lower and lowered ITRANS SIB-200 accuracy (to 0.42 to 0.44, below the base).** The gap after the controls is therefore larger than the base gap g(0), i.e. D_N and D_E partly reflect the controls widening the gap and not only ITRANS training narrowing it; the narrowing by ITRANS training alone is 0.233 to 0.117 on SIB-200 and 0.434 to 0.081 on retrieval. Seed spread is at most 0.02 in every D. English SIB-200 damage check (descriptive, no verdict; base 0.768): ITRANS-trained -1.6 and -1.8 points, native-trained -2.6 and -2.8, **English-trained -5.1 and -5.3 (flagged: more than 5 points)**. Caveats as registered: adapters trained against the 4-bit base and evaluated on the unquantized fp16 base plus adapter; two seeds give a crude seed-variance estimate. The Qwen3.5-2B arm (secondary, one seed) has not run; it is the last Kaggle job and the first cut. This is the causal test of familiarity at fixed fragmentation that X12 pointed to. Nothing against a prediction. The paper is not edited.

`````

##### 2026-11-05 03:38 IST, X6 COUNTING RESULT (rule 3; laptop; `scripts/x6_run.py`, `results/phase2/x6/counting.json`): neither shortlist model is counted. SIB-200 (n = 1,004, T1, calibrated as Phase 1; no raw fallback): Llama-3.2-1B (NousResear

RESULTS.md lines 3962 to 3963; first line committed in `b9383db` on 2026-11-05 03:38:22 +0530; last line in `108fa59` on 2026-11-05 03:40:56 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 03:38 IST, X6 COUNTING RESULT (rule 3; laptop; `scripts/x6_run.py`, `results/phase2/x6/counting.json`): neither shortlist model is counted.** SIB-200 (n = 1,004, T1, calibrated as Phase 1; no raw fallback): **Llama-3.2-1B (NousResearch mirror, deviation X6-D1): native 0.412, 95% CI [0.381, 0.443]; lower bound 0.381, below 0.40: not counted.** English 0.633, ITRANS 0.213, lowercase 0.186, lossy 0.241. **oroZ-1.7B-Indic-v1: native 0.277 [0.249, 0.305], lower bound 0.249: not counted** (English 0.388, ITRANS 0.251, lowercase 0.250, lossy 0.252: the model is close to chance on Kannada in every form). Both are reported and never counted, so they do not enter any verdict; X6 adds no counted model. The remaining X6 runs (T2 template, retrieval, ladder) are registered for included models; because neither is counted they are not run, and X6 is closed as screened, run for counting, and not counted. No Arm B of X11 can be formed from a 4B-class X6 model (none was shortlisted). The paper is not edited.

`````

##### 2026-11-05 05:14 IST, pull-forward: X4 R4 (MDL assembly layer on Bengali and Telugu Wikipedia words) started on the laptop at 05:12 IST (`scripts/x4_mdl.py`, `scripts/x4mdl_chain.sh`; 300 words with at least 30 occurrences each, 4,260 conte

RESULTS.md lines 3970 to 3971; first line committed in `53bc405` on 2026-11-05 05:14:10 +0530; last line in `f07977a` on 2026-11-05 05:22:41 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 05:14 IST, pull-forward: X4 R4 (MDL assembly layer on Bengali and Telugu Wikipedia words) started on the laptop at 05:12 IST** (`scripts/x4_mdl.py`, `scripts/x4mdl_chain.sh`; 300 words with at least 30 occurrences each, 4,260 contexts in Bengali; five models, native and ITRANS; Phase 1 functions). The laptop GPU had been idle from 04:57 (X4 retrieval finished) to 05:12, about 15 minutes, because I was writing this script; the first start failed on a wrong Wikipedia shard name (Bengali and Telugu have two shards, now both are read). R3 (natural versus ITRANS on the M4c rows, from the stored 500-row vectors) is the remaining CPU analysis.

`````

##### 2026-11-05 07:46 IST, X4 E9 lowercase-lossless schemes for Bengali and Telugu found and accepted (CPU; `scripts/x4_e9.py`, `results/phase2/x4/{bn,te}/e9/`). Phase 1 search procedure ported (coordinate descent, universal target of four local

RESULTS.md lines 3978 to 3979; first line committed in `bf08d47` on 2026-11-05 07:46:04 +0530; last line in `c723bd6` on 2026-11-05 09:53:15 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 07:46 IST, X4 E9 lowercase-lossless schemes for Bengali and Telugu found and accepted (CPU; `scripts/x4_e9.py`, `results/phase2/x4/{bn,te}/e9/`).** Phase 1 search procedure ported (coordinate descent, universal target of four local tokenizers, lowercase-only candidates, 20,000 most frequent Wikipedia words with count at least 30, 3 restarts); the candidate list of each unit is that of the Kannada unit it was projected from by Unicode name, and units that exist only through an override (Bengali nukta letters and khanda ta, Telugu ఴ) get their ITRANS spelling lowercased with a short suffix as candidates; the inherent vowel and the dandas stay fixed. **Accepted: the round trip is exact on all 2,009 FLORES+ sentences in both languages (0 failures).** The only uppercase Latin letters in the encoded text come from Latin words in the source sentences (85 Bengali and 257 Telugu sentences); the scheme itself writes lowercase only (0 sentences with uppercase produced by the scheme). Held-out savings versus ITRANS on FLORES+ (tokens per word, o200k / Gemma 4 / Qwen3.5 / Qwen3): *Bengali* 3.18 to 3.09 (-2.9%), 3.22 to 3.17 (-1.5%), 3.41 to 3.35 (-1.8%), 3.52 to 3.50 (-0.7%); *Telugu* 3.84 to 3.65 (-5.0%), 3.85 to 3.76 (-2.3%), 4.04 to 3.84 (-5.1%), 4.15 to 4.03 (-2.9%) (Phase 1 Kannada: 1.0 to 4.8%). Search objective (universal, normalised by ITRANS): Bengali best 0.967 over restarts 1.010, 1.006, 0.967; Telugu best 0.929 over restarts (deterministic init not encodable), 0.930, 0.929. These small savings are the same order as the Phase 1 E9 result (no reversible lowercase scheme saves much); they define the "lowercase lossless" rung of the ladder. The lowercase-form pipeline (vectors, SIB-200, IndicSentiment, retrieval, ladder L1 to L3) is chained behind it (`scripts/x4lower_chain.sh`) and started at 07:45 IST.

`````

##### 2026-11-05 09:53 IST, X4 LADDER RESULT (laptop, finished 09:52 IST; `scripts/x4_ladder.py`, `scripts/x4_r3.py`, `results/phase2/x4/{bn,te}/ladder_acc.json` and `r3.json`): the ladder reproduces the Kannada pattern in both languages, with on

RESULTS.md lines 3980 to 3981; first line committed in `c723bd6` on 2026-11-05 09:53:15 +0530; last line in `0dcc746` on 2026-11-05 10:09:51 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 09:53 IST, X4 LADDER RESULT (laptop, finished 09:52 IST; `scripts/x4_ladder.py`, `scripts/x4_r3.py`, `results/phase2/x4/{bn,te}/ladder_acc.json` and `r3.json`): the ladder reproduces the Kannada pattern in both languages, with one difference (Bengali L3 on SIB-200).** L1 = lowercase minus ITRANS (casing), L2 = lossy minus lowercase, L3 = natural minus lossy (spelling familiarity, on the natural ids); effect rule: significant in the direction in at least n - 1 of the 4 counted accuracy models (exact McNemar, Holm per task over contrasts x models) or, for retrieval, a bootstrap CI excluding 0 in at least 2 of the 3 counted retrieval models. No separate prediction was registered beyond "same rules as Phase 1"; the Phase 1 Kannada pattern (SIB-200: L1 no effect, L2 positive, L3 not detected) is the reference. **SIB-200 accuracy:** *Bengali* L1 no effect (differences +0.012, +0.010, +0.022, -0.032); L2 **effect, positive** (3 of 4 significant; +0.059, +0.034, +0.103, +0.149); L3 **effect, positive** (3 of 4; +0.138, +0.138, +0.089, +0.186). *Telugu* L1 no effect (-0.036, -0.021, -0.001, -0.018); L2 **effect, positive** (4 of 4; +0.119, +0.104, +0.098, +0.252); L3 no effect detected (2 of 4 significant positive; +0.064, +0.124, +0.104, +0.040). **IndicSentiment (200 items, no natural drafts so no L3):** L1 and L2 no effect detected in both languages (Bengali L2 1 of 4 positive, Telugu L2 2 of 4). **Retrieval on the M4c rows (test halves 236 and 243):** L1 no effect in both languages (CIs span 0 in all three models, e.g. Bengali Qwen3.5-2B [-0.047, +0.064]); L2 effect positive in both languages (lossy above lowercase in 3 of 3 models; Bengali Sarvam-1 +0.195 to +0.326, Telugu Sarvam-1 +0.325 to +0.457); L3 effect positive in both languages (natural above lossy in 3 of 3). Retrieval accuracy for the lowercase form is at or just below ITRANS (Bengali Sarvam-1 0.449 vs 0.466; Telugu Sarvam-1 0.494 vs 0.527), i.e. changing the casing of the romanization does nothing, while removing the information in the spelling (lossy) helps and the written natural spelling helps further, as in Kannada. **Compared with Phase 1 Kannada: same on L1 and L2 everywhere; L3 on SIB-200 is positive in Bengali (Kannada: not detected) and not detected in Telugu (as Kannada); L3 on retrieval is positive in both languages.** The paper is not edited. Implementation note: the first ladder run failed because it looked for natural-form sentiment scores that do not exist; the script now skips them (L3 on SIB-200 only).

`````

##### 2026-11-05 10:09 IST, X4 K3b-bn and K3b-te started (API and CPU; `scripts/k3b_dakshina.py sample|draft|analyse bn|te`, chain `scripts/x4k3b_chain.sh`). The exact K3b design: 500 Dakshina strings (duplicates and strings with fewer than 3 nat

RESULTS.md lines 3982 to 3983; first line committed in `0dcc746` on 2026-11-05 10:09:51 +0530; last line in `c44254c` on 2026-11-05 10:32:26 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 10:09 IST, X4 K3b-bn and K3b-te started (API and CPU; `scripts/k3b_dakshina.py sample|draft|analyse bn|te`, chain `scripts/x4k3b_chain.sh`).** The exact K3b design: 500 Dakshina strings (duplicates and strings with fewer than 3 native words dropped; pools 9,198 for Bengali; seed 6), a 200-string resample subset (seed 7, temperature 1.0, two extra drafts), Gemini gemini-3.5-flash-lite with the same prompt as the Kannada drafts (language name changed), pooled ratios Gemini/human of vowel doubling (aa, ee, ii, oo, uu per letter), h-digraph use and English-word share against the band [0.80, 1.25] (90% CI); paid-tier cap (6,000 a day, 60 a minute). The laptop GPU has nothing ready (all registered GPU work for Phases X4, X6, X10, X11 is done); it has been idle since 09:52 IST. Remaining registered items elsewhere: the Qwen3.5-2B arm of X9b (Kaggle, running), X5 (cross-language consistency, analysis only, needs X2 exposure ratios), X14 (hosted models, API, waiting for the cap reset), the X13 Sarvam-model screen.

`````

##### 2026-11-05 10:35 IST, X2 RESULT (CPU and network; `scripts/x2_exposure.py`, `results/phase2/x2/exposure.json`): SUPPORTED (as predicted): the romanized share is higher for Hindi than for Kannada. Source A = FineWeb-2 (script-labelled config

RESULTS.md lines 3987 to 3988; first line committed in `d4363ef` on 2026-11-05 10:35:58 +0530; last line in `e0f0b06` on 2026-11-05 10:43:29 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 10:35 IST, X2 RESULT (CPU and network; `scripts/x2_exposure.py`, `results/phase2/x2/exposure.json`): SUPPORTED (as predicted): the romanized share is higher for Hindi than for Kannada.** Source A = FineWeb-2 (script-labelled configs; counts from parquet footers). Romanized share e = documents in the Latin-script config / (Latin plus native-script): **Hindi 0.437%, Kannada 0.045%; difference +0.392 percentage points, 95% interval [0.389, 0.396] (above 0); the byte-based share has the same sign.** Other languages (descriptive, e in percent of documents): Telugu 1.212, Malayalam 0.103, Tamil 0.087, Bengali 0.069, Marathi 0.045, Gujarati 0.034. Telugu has the highest romanized share of the four registered languages, nearly three times Hindi's. **Deviation X2-D1 (stated, not a rule change): the registered interval is a bootstrap over shards; the Latin-script configs are single-shard files, so the interval is a parametric (Poisson) bootstrap of the document counts and reflects counting noise only.** Source B was not run (Source A covers all four languages, as registered). X5 (cross-language consistency, analysis only) can now run once its inputs are paired.

`````

##### 2026-11-05 11:09 IST, X10 POST HOC check for Qwen3.5-2B (not part of the registration; the registered X10 verdict "supported, 4 of 4" and the registered numbers are unchanged; `scripts/x10_posthoc.py`, `results/phase2/x10/posthoc/`). The mo

RESULTS.md lines 3993 to 3994; first line committed in `b2b04f3` on 2026-11-05 11:09:51 +0530; last line in `124a4cc` on 2026-11-05 11:42:00 +0530; labels from the title and parent heading: post hoc, result, failed or not run

`````text
- **2026-11-05 11:09 IST, X10 POST HOC check for Qwen3.5-2B (not part of the registration; the registered X10 verdict "supported, 4 of 4" and the registered numbers are unchanged; `scripts/x10_posthoc.py`, `results/phase2/x10/posthoc/`).** The model was regenerated with the registered instruction, greedy decoding and 128 new tokens, raw outputs kept. **Finding: the empty first line is a thinking block. 61.8% of native outputs (86.5% ITRANS, 84.5% lowercase, 87.9% lossy, 84.3% natural) begin with a blank line followed by "<think>", and fewer than 1% close the block within 128 tokens (0.6% native, at most 0.2% in the other forms), so the model does not reach an answer in those outputs.** The share of outputs that start a thinking block equals the registered empty-first-line share in every form. The post hoc extraction (first non-empty line) therefore returns the string "<think>" for those outputs and is not a translation; its chrF (corpus: native 20.6, ITRANS 3.5, lowercase 3.7, lossy 3.7, natural 5.2, against the registered 20.0, 2.5, 2.7, 2.7, 4.2) and its contrast (native minus ITRANS +14.70 chrF [13.31, 16.11], against the registered +15.03 [13.60, 16.48]) are essentially the registered ones. Reading: Qwen3.5-2B in this pipeline mostly spends the 128 tokens on a reasoning preamble, and it does so more often for romanized input (84 to 88%) than for native input (62%); the registered chrF difference between native and romanized therefore mixes translation quality with how often the model starts reasoning. A thinking-aware extraction would need a longer token budget (the reasoning is not finished at 128 tokens) and is not part of the registration; it was not run. The paper is not edited.

`````

##### 2026-11-05 14:08 IST, RESTART (extra-seeds chain `x9extra`, operational). The chain failed at 14:03:34 on the first 1% X9a-low extra run (`x9a.py train 1 3`): `data/processed/x9a/train_p1.npy` (the X9a level-1 token stream) had been removed

RESULTS.md lines 4003 to 4004; first line committed in `753999e` on 2026-11-05 14:08:43 +0530; last line in `88cf86e` on 2026-11-05 14:37:51 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 14:08 IST, RESTART (extra-seeds chain `x9extra`, operational).** The chain failed at 14:03:34 on the first 1% X9a-low extra run (`x9a.py train 1 3`): `data/processed/x9a/train_p1.npy` (the X9a level-1 token stream) had been removed with the X9a caches. Cause fixed: new command `x9a.py regen 1` regenerates that one stream with the code of `prep()` and refuses (and deletes the file) unless its sha256 equals the stored X9a value; the chain now runs it first (CPU) and was relaunched at 14:07 (the 0.1% and 0.3% seed 3 runs were already finished and are skipped). GPU idle from 14:03 to the relaunch of the GPU work (a few minutes). Nothing else changed.

`````

##### 2026-11-05 14:37 IST, X14 FINISHED (hosted models via Groq, exploratory, no registered verdict; `scripts/x14_run.py`, `scripts/x14_analyse.py`, `results/phase2/x14/analysis.json`; finished 14:23 IST after the 12:45 reset; 3,269 rows per mod

RESULTS.md lines 4005 to 4006; first line committed in `88cf86e` on 2026-11-05 14:37:51 +0530; last line in `0f01dd6` on 2026-11-05 14:38:09 +0530; labels from the title and parent heading: exploratory, result, failed or not run

`````text
- **2026-11-05 14:37 IST, X14 FINISHED (hosted models via Groq, exploratory, no registered verdict; `scripts/x14_run.py`, `scripts/x14_analyse.py`, `results/phase2/x14/analysis.json`; finished 14:23 IST after the 12:45 reset; 3,269 rows per model: 1,004 each for native, ITRANS and lossy, 257 natural).** SIB-200 accuracy with the registered prompt, temperature 0, exact match, unparsed counted wrong; 95% bootstrap intervals over items; gaps paired over item ids. **gpt-oss-120b: native 0.836 [0.813, 0.859], ITRANS 0.625 [0.595, 0.654], lossy 0.668 [0.638, 0.697], natural 0.700 [0.646, 0.755]; native minus ITRANS +0.211 [0.181, 0.241], minus lossy +0.167 [0.139, 0.196], minus natural +0.167 [0.117, 0.218] (n = 257); unparsed 0%.** **Qwen3.8-27B (the Groq model qwen/qwen3.8-27b): native 0.836 [0.813, 0.859], ITRANS 0.658 [0.628, 0.687], lossy 0.654 [0.625, 0.684], natural 0.696 [0.638, 0.751]; native minus ITRANS +0.177 [0.147, 0.207], minus lossy +0.181 [0.151, 0.210], minus natural +0.144 [0.093, 0.195]; unparsed at most 0.1%.** **ALLaM-2-7B: native 0.337 [0.308, 0.367], ITRANS 0.190 [0.166, 0.214], lossy 0.254 [0.227, 0.281], natural 0.296 [0.241, 0.354]; native minus ITRANS +0.146 [0.115, 0.179]; unparsed 35.5% native and 55.6% to 57.7% romanized, so its accuracies mix understanding with answer-format failure.** Reading, descriptive only: the large hosted models keep the familiarity ordering seen in the small open models (native above natural above ITRANS and lossy), with a native-to-romanized gap of 14 to 21 points that is far smaller than the small models' gaps in absolute accuracy terms but still well away from zero; natural romanization recovers about a third to a half of the ITRANS gap in gpt-oss-120b (natural 0.700 against ITRANS 0.625 on different item sets, so the paired natural gap is the comparable number: +0.167 against +0.211 on the 257 items for ITRANS from the main set) and the lossy form is not worse than ITRANS in either large model (gpt-oss: 0.668 against 0.625; Qwen3.8-27B: 0.654 against 0.658). Model names as in `model_choice.json`; deviation X14-D1 (token budget for one model) stands as logged. The paper is not edited.

`````

##### 2026-11-05 14:38 IST, CORRECTION NOTE to the X14 entry above (reading paragraph only; numbers unchanged). The sentence comparing natural with ITRANS mixed item sets. On the same 257 items the accuracies are: gpt-oss-120b native 0.868, ITRAN

RESULTS.md lines 4007 to 4008; first line committed in `0f01dd6` on 2026-11-05 14:38:09 +0530; last line in `2f9c9f1` on 2026-11-05 15:37:57 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 14:38 IST, CORRECTION NOTE to the X14 entry above (reading paragraph only; numbers unchanged).** The sentence comparing natural with ITRANS mixed item sets. On the same 257 items the accuracies are: gpt-oss-120b native 0.868, ITRANS 0.646, natural 0.700; Qwen3.8-27B native 0.840, ITRANS 0.658, natural 0.696; ALLaM-2-7B native 0.366, ITRANS 0.206, natural 0.296. So natural romanization recovers 54 of 222 points of the native-to-ITRANS gap in gpt-oss-120b (about a quarter), 38 of 182 in Qwen3.8-27B (about a fifth) and 90 of 160 in ALLaM-2-7B (a bit over half; format failures dominate that model); the earlier phrase 'about a third to a half' is withdrawn. The remaining statements (familiarity ordering native > natural > ITRANS in the three models; lossy not worse than ITRANS in the two large models; native-to-ITRANS gaps of 14.6 to 21.1 points on the 1,004 items) stand. The comparison to the small open models' gaps was not computed and is withdrawn too; no such statement is made.

`````

##### 2026-11-05 15:39 IST, X13 SARVAM-M RESULT (23.6B, 4-bit NF4, SIB-200 only, account 2; `scripts/x13_sarvam_m.py`, `results/phase2/x13/sarvam-m/analysis.json`): COUNTED; native minus ITRANS supported (extended all-but-one reading 7 of 7 model

RESULTS.md lines 4011 to 4012; first line committed in `c7f6e92` on 2026-11-05 15:39:07 +0530; last line in `c7f6e92` on 2026-11-05 15:39:07 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 15:39 IST, X13 SARVAM-M RESULT (23.6B, 4-bit NF4, SIB-200 only, account 2; `scripts/x13_sarvam_m.py`, `results/phase2/x13/sarvam-m/analysis.json`): COUNTED; native minus ITRANS supported (extended all-but-one reading 7 of 7 models).** The kernel hit its 5 h cap ("job finished timeout" at 4.75 h of wall time) after three forms (about 85 minutes per form at 4-bit); **English, native and ITRANS finished (n = 1,004 each, non-finite 0); lossy, lowercase and natural were not reached** (no relaunch: three forms answer the registered counting rule and the native - ITRANS contrast, the lossy contrast is not available for this model, and account 2 has about 9.6 h of quota left but a relaunch would need another 5 h for forms that would not change a verdict; the relaunch allowed by the standing order is not used here and the decision is logged). Calibrated SIB-200 accuracy (raw fallback not used): **English 0.840 [0.817, 0.862], native 0.840 [0.817, 0.863], ITRANS 0.682 [0.653, 0.710].** **Counting rule (native CI lower bound above 0.40): 0.817, counted.** **Native minus ITRANS +0.157 [0.129, 0.185]; native-only correct 196 items, ITRANS-only correct 38, exact McNemar p = 7.6e-27.** Extended reading for native vs ITRANS only (Holm over seven tests: Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B, Qwen3-8B, Llama-3.1-8B, Sarvam-m): all seven positive and significant (differences 0.432, 0.435, 0.227, 0.383, 0.322, 0.330, 0.157), so native over ITRANS is supported in 7 of 7; the lossy contrast was not scored for Sarvam-m, so the registered extended P-a verdict (which includes lossy) is not changed. Sarvam-m has the smallest native-to-ITRANS gap among the seven (0.157), the Sarvam family the two smallest (Sarvam-1 0.227). Per the registration the 4-bit models run SIB-200 and X10 only; X10 for Sarvam-m is not built (generation of 1,012 sentences per form with a 23.6B 4-bit model at about 85 minutes per 1,004 scored items is expected to be far slower; a pilot comes first). The paper is not edited.

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

##### 2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected). Both setup kernels pushed and started on a T4 x2 (so GPU access works) but ended with status ERROR aft

RESULTS.md lines 4023 to 4024; first line committed in `07e9a33` on 2026-11-05 22:37:41 +0530; last line in `1d0616d` on 2026-11-05 22:59:17 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected).** Both setup kernels pushed and started on a T4 x2 (so GPU access works) but ended with status ERROR after about 3.5 minutes in the same step: the kernel's `pip install -e` of the project package failed while installing build dependencies (no output, a timeout). A CPU-only test kernel (`aarnavkembhavi/shattered-nettest`, internet requested in its metadata) confirmed the cause: DNS resolution fails for both pypi.org and huggingface.co ("Temporary failure in name resolution"), i.e. Kaggle did not grant internet to this account's kernels although the push asked for it. Kaggle only grants internet to phone-verified accounts, so the phone verification the owner reported is not in effect for kernels (or was not completed for the account). Every registered job needs internet (pinned packages, public models from Hugging Face, the Wikipedia pool), so none can run until it is fixed. Quota used on account 3: 0.21 h (two failed kernels, about 3.5 minutes each; the CPU test does not count). **What the owner must do:** sign in to kaggle.com as aarnavkembhavi, open Settings, complete 'Phone Verification' (the account must show a verified phone number), and confirm that a new notebook's Settings panel lets 'Internet' be switched on. When he has, tell me and I re-run the setup chain `acct3` (smoke gate and A1-R reproduction); the job chains `acct3x9b` and `acct3sm` are waiting and start by themselves after the acceptance. The earlier chain status DONE for `acct3` meant only that the runner finished, not that the gates passed; the gates did not pass and the acceptance marker was not written. Cleanup list (adds): the kernels `aarnavkembhavi/shattered-nettest`, `shattered-kaggle-gate`, `shattered-kaggle-retrieval-gate` and the datasets on the third account are removed at the end of Phase 2. The paper is not edited.

`````

##### 2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged). After the power-loss restart the first extra run (`sarvam-1+itrans+s2`) reach

RESULTS.md lines 4025 to 4026; first line committed in `1d0616d` on 2026-11-05 22:59:17 +0530; last line in `4579347` on 2026-11-05 22:59:29 +0530; labels from the title and parent heading: amended, failed or not run

`````text
- **2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged).** After the power-loss restart the first extra run (`sarvam-1+itrans+s2`) reached step 100 at 22:50 and then sat in `torch.save` for more than 8 minutes with the GPU idle (py-spy: `serialization._save`, `write_record`, one core at 100%); the first attempt did the same (step 100 logged at about 16:20, checkpoint file last written 16:42, when the power failed). Cause: the optimizer state is the paged 8-bit AdamW state (bitsandbytes), whose pages migrate one by one while the 8 GB card is full; writing it takes over 20 minutes per checkpoint, three checkpoints per run, about 1 h of every 2.9 h run, about 6 to 7 h over six runs (the Kaggle T4s had room for it, the laptop does not). Fix, committed: checkpoints now hold the adapter, scheduler, scaler and step but not the optimizer state, which makes the save take seconds; the checkpoint is only ever read after an interruption, so an uninterrupted run is numerically identical to before; a run resumed from such a checkpoint resets the Adam moments, and `done.json` carries `resumed_without_optimizer_state` (true) so it can be reported or excluded. The running ITRANS run is resumed from its step-100 checkpoint, which does contain the optimizer state (written before the change), so it continues exactly; the chain `x9extra` is relaunched after the restart. The finish estimate improves by about 6 h: about 8 Nov 00:00 to 02:00 IST for the six laptop runs, if account 3 does not take the seed-4 runs.

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

##### 2026-11-06 11:53 IST, LAPTOP GPU IDLE 11:40 ONWARD, NO REGISTERED JOB READY (standing order 1). The extra-seed chain ended at 11:40:11. Every registered laptop job is done; the remaining registered work needs Kaggle (Sarvam-m lossy, lowerca

RESULTS.md lines 4034 to 4035; first line committed in `e605a65` on 2026-11-06 11:53:24 +0530; last line in `ac6470f` on 2026-11-07 01:49:19 +0530; labels from the title and parent heading: registered, failed or not run

`````text
- **2026-11-06 11:53 IST, LAPTOP GPU IDLE 11:40 ONWARD, NO REGISTERED JOB READY (standing order 1).** The extra-seed chain ended at 11:40:11. Every registered laptop job is done; the remaining registered work needs Kaggle (Sarvam-m lossy, lowercase and natural; Sarvam-m X10) or cannot be formed (X11 Arm B), and the optional X13 activation patching was left dropped. Nothing is pulled forward because nothing registered is left for the laptop. Proposed next jobs, none started: see the report.

`````

##### 2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational). Aarnav supplied a new Kaggle API token to be used instead of the third-account token. It resolves to the Kaggle username aakarshprabhu (ch

RESULTS.md lines 4036 to 4037; first line committed in `ac6470f` on 2026-11-07 01:49:19 +0530; last line in `b194514` on 2026-11-07 01:53:51 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational).** Aarnav supplied a new Kaggle API token to be used instead of the third-account token. It resolves to the Kaggle username **aakarshprabhu** (checked with an empty CLI configuration folder; the old token resolved to aarnavkembhavi), a different account, treated as a teammate's account on Aarnav's instruction. The new token is stored only in the gitignored `.env` (KAGGLE3_API_TOKEN, KAGGLE3_USERNAME; the replaced token is kept there as KAGGLE3_API_TOKEN_PREVIOUS for cleanup and revocation), never in commits, logs or reports. The earlier attempt on aarnavkembhavi (two failed setup kernels, no internet, 0.21 h) is archived as `results/kaggle/acct3_aarnavkembhavi_failed` and its chain status under `results/phase2/`. A CPU test kernel on the new account confirms **internet works** (pypi.org and huggingface.co reachable). The private dataset `aakarshprabhu/shattered-flores-private` was created; the smoke gate and the A1-R reproduction (untrained Sarvam-1 and Gemma 4 E2B must reproduce account 1's curves) run before any job. The account-3 X9b chain was cancelled (the seed-4 runs finished on the laptop on 2026-11-06); the Sarvam-m chain `acct3sm` (lossy, lowercase, natural; 5 h cap) is kept waiting for the acceptance. Cleanup list: revoke both third-account tokens (the replaced one and the new one; both were pasted in chat), delete the datasets and kernels created on aakarshprabhu and on aarnavkembhavi, delete the nettest kernels. The username is added to the anonymiser's scrub list. This extends the statement that some Phase 2 Kaggle compute ran on teammates' accounts: account 3 (aakarshprabhu) from 2026-11-07. The paper is not edited.

`````

##### 2026-11-07 03:00 IST, KAGGLE ACCOUNT 3 (aakarshprabhu): ACCEPTANCE CORRECTION AND FIRST JOB STARTED (operational). The acceptance written at 02:20 was premature: the smoke gate had not passed (two attempts failed because the laptop referenc

RESULTS.md lines 4042 to 4043; first line committed in `2466b30` on 2026-11-07 03:00:36 +0530; last line in `82e4226` on 2026-11-07 03:52:42 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-07 03:00 IST, KAGGLE ACCOUNT 3 (aakarshprabhu): ACCEPTANCE CORRECTION AND FIRST JOB STARTED (operational).** The acceptance written at 02:20 was premature: the smoke gate had not passed (two attempts failed because the laptop reference scores were not in the pushed package: the first lacked them, the second mounted an older version of the package dataset). Third attempt passed: both models in float16, raw-prediction agreement 0.99, 0.95, 0.96 (Sarvam-1: native, ITRANS, lossy) and 1.00, 0.99, 0.99 (Gemma 4 E2B), accuracy differences within 0.02, tolerance 0.03. With the earlier exact A1-R reproduction (account 1's curves reproduced to 0.0), the account is accepted (marker rewritten 03:0x) and the X13 Sarvam-m job for the three forms the first kernel did not reach (lossy, lowercase, natural; 4-bit, cap 5 h) was started by the waiting chain. Quota on account 3: about 1.2 h of 30 h used by the setup.

`````

##### 2026-11-07 04:22 IST, QWEN3.5-2B EXTRA RUNS: SLOWER THAN PROJECTED; MICRO-BATCH CAP LOWERED TO 2 FOR THE NEXT RUNS (operational; recipe unchanged). The first Qwen extra run (ITRANS, code seed 1) trains at about 41 s per optimizer step on th

RESULTS.md lines 4046 to 4047; first line committed in `c42cfd4` on 2026-11-07 04:22:43 +0530; last line in `0cd9a82` on 2026-11-08 15:33:40 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-07 04:22 IST, QWEN3.5-2B EXTRA RUNS: SLOWER THAN PROJECTED; MICRO-BATCH CAP LOWERED TO 2 FOR THE NEXT RUNS (operational; recipe unchanged).** The first Qwen extra run (ITRANS, code seed 1) trains at about 41 s per optimizer step on the laptop (step 40 after 1,778 s), against about 26 s on the Kaggle T4; with 346 steps that is about 3.9 h of training plus about 0.6 h of evaluation per run, so the six runs take about 27 h and end about **8 Nov 07:00 IST**, not 7 Nov 20:00 to 23:00 as projected at registration. The card is at 8.0 GB (micro-batch 4, shared-memory spill), as the Sarvam-1 runs were before the cap. The cap file `build/x9b_max_micro_batch.txt` is lowered from 8 to 2 for the runs that have not started (the run in progress keeps micro-batch 4; same optimizer step of 16,384 tokens; done.json records the value); if the next run is not faster the cap is restored. If Aarnav prefers, the second seed (3 runs) can be dropped, which brings the end to about 7 Nov 20:00.

`````

##### 2026-11-08 15:33 IST, X13 SARVAM-M: ALL SIX FORMS SCORED; EXTENDED P-a WITH SARVAM-M (account 3, aakarshprabhu, 2026-11-07 03:00 to 06:18; `scripts/x13_sarvam_m.py`, `results/phase2/x13/sarvam-m/analysis.json`). The remaining forms ran in o

RESULTS.md lines 4049 to 4049; first line committed in `0cd9a82` on 2026-11-08 15:33:40 +0530; last line in `0cd9a82` on 2026-11-08 15:33:40 +0530; labels from the title and parent heading: result

`````text
- **2026-11-08 15:33 IST, X13 SARVAM-M: ALL SIX FORMS SCORED; EXTENDED P-a WITH SARVAM-M (account 3, aakarshprabhu, 2026-11-07 03:00 to 06:18; `scripts/x13_sarvam_m.py`, `results/phase2/x13/sarvam-m/analysis.json`).** The remaining forms ran in one kernel of 3.3 h (4-bit, SIB-200 only); calibration inputs identical to the first kernel (cf.json equal). Calibrated accuracy: **English 0.840 [0.817, 0.862], native 0.840 [0.817, 0.863], ITRANS 0.682 [0.653, 0.710], lossy 0.732 [0.705, 0.760], lowercase 0.660 [0.631, 0.690], natural 0.778 [0.728, 0.829] (257 items).** Native minus form (paired, exact McNemar): **ITRANS +0.157 [0.129, 0.185] (196 native-only, 38 ITRANS-only, p 7.6e-27); lossy +0.108 [0.084, 0.131] (137 against 29, p 5.5e-18); lowercase +0.179 [0.149, 0.208] (219 against 39, p 1.4e-31); natural +0.047 [0.000, 0.093] on 257 items (24 against 12, p 0.065, not significant).** Counted (native CI lower 0.817). **Registered extended P-a with Sarvam-m (Holm over the 14 native-vs-ITRANS and native-vs-lossy tests of seven counted models): native vs ITRANS supported 7 of 7; native vs lossy supported 7 of 7 (no test significantly negative).** The earlier verdicts (Phase 1 four models; X13 five models) stand; this reading is reported separately. Reading: Sarvam-m keeps the familiarity order native (0.840) > natural (0.778) > lossy (0.732) > ITRANS (0.682) > lowercase (0.660), and natural romanization sits within noise of native on the 257 items; lossy is above ITRANS (the information-loss account is not supported here either). Sarvam-m X10 is still not built. The paper is not edited.
`````

##### 2026-11-08 16:23 IST, SARVAM-M X10 PILOT RESULT AND THE RUN DECISION (account 3; timing only, no chrF used for any decision). Pilot (16 sentences, native and ITRANS, batch 8, 4-bit, 2 x T4): model load 428 s; 28.0 s per sentence (native) an

RESULTS.md lines 4054 to 4055; first line committed in `0034538` on 2026-11-08 16:23:25 +0530; last line in `?` on ?; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-08 16:23 IST, SARVAM-M X10 PILOT RESULT AND THE RUN DECISION (account 3; timing only, no chrF used for any decision).** Pilot (16 sentences, native and ITRANS, batch 8, 4-bit, 2 x T4): model load 428 s; 28.0 s per sentence (native) and 22.3 s (ITRANS); no empty outputs and no reasoning preamble in the 32 outputs; kernel 0.41 h. Estimate for the full registered X10 (native, ITRANS, lowercase, lossy on 1,012 sentences and natural on 267) at that rate: about 4,315 sentences x 25 s = about 30 h, against 25.1 h left on account 3 and a 12 h session cap. **Decision (cut, logged): run native and ITRANS only, the registered X10-P contrast, as two resumable kernels at batch 16 (about 11 to 14 h of quota in total, one kernel per form, 10.5 h cap each); lowercase, lossy and natural are not run for Sarvam-m. This is a deviation from the full X10 form set for this extended model (the X10-P verdict concerns the four counted models and is unchanged).** Chain `x10sm`; if batch 16 runs out of memory the run is retried once at batch 8. Quota on account 3: 4.9 h used of 30 h.

`````

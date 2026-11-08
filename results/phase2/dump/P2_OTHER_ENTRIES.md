# Phase 2: RESULTS.md entries not matched to an experiment id above (verbatim, nothing omitted)

##### PHASE 2 PRE-REGISTRATION (2026-11-01; Aarnav's design and Gate A decisions of 2026-11-01; written before any Phase 2 data, score, vector, draft or download-dependent statistic exists)

RESULTS.md lines 3336 to 3343; first line committed in `a57fe61` on 2026-11-01 20:14:53 +0530; last line in `a57fe61` on 2026-11-01 20:14:53 +0530; labels from the title and parent heading: registered

`````text
## PHASE 2 PRE-REGISTRATION (2026-11-01; Aarnav's design and Gate A decisions of 2026-11-01; written before any Phase 2 data, score, vector, draft or download-dependent statistic exists)

**Status of Phase 1.** Phase 1 verdicts (frozen at f7ce5a8, all entries above) are final and never change. Phase 2 adds results; where a Phase 2 result goes against a Phase 1 verdict, both are reported and the Phase 1 verdict stays as recorded. Extended verdicts with enlarged model sets are reported separately from the Phase 1 verdicts.

**Provenance.** This block is committed before any Phase 2 data are generated. The commit carries the git tag `phase2-registration`; `shattered.runlog.provenance()` writes `phase2_registration_commit` (the tag's commit) into every Phase 2 result file. Phase 2 results go under `results/phase2/<experiment>/`. Pilots are run on small subsets first and their time estimates reported before full runs; pilot scores are not looked at for any decision. Every job is resumable; failures write the error to CHAIN_STATUS and stop. Gates: A (orientation, done), B (this registration), C (X1 T2, X3, X7), D (X2, X4, X5), E (X6, X8; one table of every Phase 2 registered outcome).

**Standing rules carried over.** No fabricated or estimated results (every number from a file in `results/`); registered verdicts are never changed; post hoc analyses are labelled post hoc or exploratory; deviations are logged with dates; `cache/llm_cache.sqlite` is never deleted; no Anthropic key; bf16 only, one model-loading job at a time (RAM; check for a large process from `C:\PROJECTS\ISM`); GPU guard (<= 500 MB in use) and, from 2026-11-01, a disk guard (no GPU job starts with under 25 GB free; `disk_guard` in `scripts/chainlib.sh`, `require_free_disk` in `shattered.gpuguard`); the Gemini reset is kept at 12:45 IST (`next_reset`); `paper2/` text is not edited and no new table is `\input` into it (Phase 2 tables and figures go to `paper2/tables/phase2/` and `paper2/figures/phase2/`).

`````

##### General rules for all Phase 2 tests

RESULTS.md lines 3344 to 3351; first line committed in `a57fe61` on 2026-11-01 20:14:53 +0530; last line in `a57fe61` on 2026-11-01 20:14:53 +0530; labels from the title and parent heading: registered

`````text
### General rules for all Phase 2 tests
- **Statistics (Phase 1 reporting standards):** exact McNemar on paired per-item correctness (or retrieval hit), Holm within each measure over the family stated for that test, 95% paired bootstrap CIs (10,000 resamples, seed 0; word-clustered where a unit is a word), a difference is **significant** when its Holm-adjusted p < 0.05; Holm decides on any CI/Holm disagreement (reported). n is reported for every number.
- **Effect rule for enlarged or changed model sets ("all counted models but one").** An effect is declared when the difference is significant with the same sign in all counted models but one, and in at least two models. Phase 1's "3 of 4" and "2 of 3" are the cases of 4 and 3 counted models. With fewer than three counted models a test is **uninformative** (reported, no verdict). This applies to any new model, to X6 extended verdicts, and to the counted set of each language in X4. (Phase 1's Hindi rule allowed two counted models; Phase 2 does not.)
- **Qwen2.5-1.5B** is reported in every table and never counted, in every Phase 2 test except where a Phase 1 rule counted it and that rule is quoted verbatim (T-a below). Qwen3-1.7B has no retrieval measure (no M4 vectors) except where X4 computes them; it is counted for accuracy only.
- **Counted models (Kannada, as Phase 1):** retrieval Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; accuracy Qwen3-1.7B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B. Gemma 4 inputs always prepend BOS (custom text-only loader). Interpretability and accuracy runs in bf16.
- **Accuracy measure (unchanged from E0b/E0c):** log-likelihood of the English label words after an English instruction; calibration = mean of the content-free inputs "N/A", "", "[MASK]" (each placed in every field of the template); registered fallback to raw scores for a whole model x task x template row if calibrated English accuracy is more than 5 points below raw English accuracy (decided per template, on English). A cell is informative if English accuracy >= chance + 5 points. Verbalizers unchanged: sentiment " negative"/" positive"; XNLI " yes"/" maybe"/" no"; SIB " science"," travel"," politics"," sports"," health"," entertainment"," geography".
- **Retrieval measure (unchanged from M4/M4c):** unmapped acc@1 of the English translation by cosine on the mean-pooled residual stream, layer chosen on the train half; layer 0 surface baseline (mapped ridge, M4b/M4c procedure) reported where a registration below says so.

`````

##### Scheduling (registered order)

RESULTS.md lines 3452 to 3454; first line committed in `a57fe61` on 2026-11-01 20:14:53 +0530; last line in `a57fe61` on 2026-11-01 20:14:53 +0530; labels from the title and parent heading: registered

`````text
### Scheduling (registered order)
**GPU queue (one model-loading job at a time):** X1 T2 -> X3 -> X7 control -> X6 screen -> X4 Bengali -> X4 Telugu -> X1 T3 -> X6 full -> optional patching. **T3 and X6 full are the first things cut if the timeline slips.** Native, ITRANS, lowercase and lossy forms of X4 are scored before the natural drafts finish. **Without a GPU, in parallel:** X2 (RAM limit), Gemini drafting for X4 spread over quota days, X7 accounting, the X8 page, data fetches for X4 (SIB-200, IndicSentiment, Wikipedia for bn/te; Dakshina bn/te re-streamed), the lossy collision-rate report. **Gemini quota priority:** (1) X4 natural romanization, Bengali then Telugu; (2) the X2 precision check; (3) the T3 instruction; (4) anything else (K3b-bn, K3b-te). Chains longer than 20 minutes run detached with 2-minute heartbeats in `results/CHAIN_STATUS*.md` and the watcher. At each gate, for every registered test: verdict, counted models, effect sizes with CIs, n, files; anything against prediction first.

`````

##### Items flagged at Gate B for Aarnav (proposed, written into the registration above and open to change before the first run of the affected experiment)

RESULTS.md lines 3455 to 3459; first line committed in `a57fe61` on 2026-11-01 20:14:53 +0530; last line in `9dec97e` on 2026-11-02 16:00:24 +0530; labels from the title and parent heading: registered

`````text
### Items flagged at Gate B for Aarnav (proposed, written into the registration above and open to change before the first run of the affected experiment)
1. X3 retrieval floor 150 eligible M4c sentences (proposed). 2. X4 batching pilot threshold 28 of 30 exact matches (proposed). 3. X7(ii) vocabulary set: literal reading = the whole 6-vocabulary grid (about 8 GPU hours); the two-extremes alternative is 6 runs. 4. X8 n: 100 or 200 (CI widths above). 5. Matched-set X3 contrasts reuse Phase 1 per-item scores for a and NC-O restricted to the eligible items (with a recompute control) instead of a full rescore. 6. Qwen2.5 stays never counted in Phase 2 except under the verbatim P-a wording in T-a.

---

`````

##### PHASE 2 CLARIFICATIONS (2026-11-02, Gate C decisions, Aarnav)

RESULTS.md lines 3472 to 3479; first line committed in `050df80` on 2026-11-02 16:36:01 +0530; last line in `9d408c4` on 2026-11-02 16:47:59 +0530; labels from the title and parent heading: amended

`````text
## PHASE 2 CLARIFICATIONS (2026-11-02, Gate C decisions, Aarnav)

**C1. X3 D3 sign convention (formal clarification; no verdict changes).** The X3 registration (2026-11-01) defines D3 = NC-O - c and then says "D3 positive effect = piece rarity at equal count costs". A rarity cost means NC-O (rarer pieces) is *worse* than c, which makes D3 *negative*; the two statements cannot both hold. The analysis (`scripts/x3_analyse.py`, run 2026-11-02) applied the literal rule (effect = Holm-significant positive difference in at least 3 of 4 accuracy models, 2 of 3 retrieval models, as for every contrast). **Clarification:** the intended meaning is that piece rarity at equal count costs when NC-O scores significantly *lower* than c; the effect rule is applied to the negative direction of D3 for the interpretation line. **Verdict unchanged under both readings:** literal reading, D3 has 0 significant positive models for SIB, sentiment and retrieval; cost-as-negative reading, D3 is significantly negative in 2 of 4 models for SIB (Qwen3.5, Sarvam-1; 3 needed), 0 of 4 for sentiment, 1 of 3 for retrieval (Gemma 4; 2 needed). D3 is "no effect detected" under both, and with D2 "no effect detected" the registered interpretation stays **unresolved**. Logged as deviation row in `paper2/tables/deviations.tex`.

**C2. X3 exploratory corpus-frequency regression (defined here, before it is run; the X3 text registers only the s_ref balance check, not a regression; Aarnav asked for it at Gate C, 2026-11-02).** Exploratory, no verdict, labelled so wherever it appears. For each model and each comparison split (c = the s_int frequency-matched split, and NC-O), on the model's eligible items of the c set: unit = item (SIB-200) or test-half sentence (retrieval, eligible M4c rows, layers as in `x3_analyse.py`); x_i = mean s_ref over the pieces of the canonical text span minus mean s_ref over the pieces of the comparison split's span (s_ref as registered: ln(1 + count) over the canonical tokenization of the 100,000-word reference sample); y_i = correct(canonical) - correct(split) in {-1, 0, 1} (SIB: calibrated prediction; retrieval: acc@1 hit). Model: ordinary least squares y_i = b0 + b1 x_i. Reported per model and measure: b0 (the accuracy change at zero corpus-frequency difference), b1, n, and 95% CIs by item bootstrap (10,000 resamples, seed 0). Counted and non-counted models are all reported, Qwen2.5 flagged as never counted. Sentiment and XNLI are not included (too few items per model for a slope).

---

`````

##### Q. Queues and budget (cut from the end of either queue if time slips; stop at gates C, D, E)

RESULTS.md lines 3687 to 3695; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `680151b` on 2026-11-02 19:01:49 +0530; labels from the title and parent heading: amended

`````text
### Q. Queues and budget (cut from the end of either queue if time slips; stop at gates C, D, E)

- **Laptop:** X7 control (running, about 10 GPU hours) -> X9a (about 6 h) -> X9b memory pilot -> X10 pilot -> X4 Bengali -> X4 Telugu -> X1 T3 (only after a native
  speaker verifies `T3_verification.md`; the XNLI line is marked "needs rewrite") -> X6 -> X11 -> X10 full (if not on Kaggle).
- **Kaggle (after the gate and the approval of this amendment):** A1-R retrieval gate (may run before approval; it is not an experiment) -> A1-P for each 7 to 9B model (about 0.3 h each) -> X12 -> X13 -> X9b full (about 27 h) -> X10 full. The weekly cap (30 h) means X9b alone
  needs most of a week; the runner refuses pushes over the cap and the schedule is set from measured hours.
- **Needs people or access:** T3 verification, X8 annotators P and Q, X15 annotators, Hugging Face access to Llama-2-7b-hf, Ambari-7B-Instruct-v0.1 and
  Llama-3.1-8B.

`````

##### P. Page policy (applies to every integration)

RESULTS.md lines 3696 to 3703; first line committed in `680151b` on 2026-11-02 19:01:49 +0530; last line in `f41e866` on 2026-11-02 19:15:43 +0530; labels from the title and parent heading: amended

`````text
### P. Page policy (applies to every integration)

The main text targets 12 pages and may exceed 12 only for material that carries a headline claim (X9, X12, X15). Robustness, extra models, bookkeeping and
per-cell tables go to the appendix. All scale work is in **one section, "Scale and replication"**. After each integration the main-text pages are reported
with a list of what moved to the appendix. Phase 2 results enter the paper only when Aarnav says so.

**Not claimed.** No new claim about why familiarity matters, no scaling law, no change to any Phase 1 or Phase 2 verdict.

`````

##### PHASE 2 EXECUTION LOG (Amendment 2, from 2026-11-02)

RESULTS.md lines 3704 to 3705; first line committed in `f41e866` on 2026-11-02 19:15:43 +0530; last line in `f41e866` on 2026-11-02 19:15:43 +0530; labels from the title and parent heading: none

`````text
## PHASE 2 EXECUTION LOG (Amendment 2, from 2026-11-02)

`````

##### 2026-11-02 23:17 IST, weights-loading rule (decided by Aarnav). Ambari-7B-Instruct-v0.2 ships only pickle `.bin` weights. It is loaded only on Kaggle, with `weights_only=True` forced on

RESULTS.md lines 3732 to 3733; first line committed in `78d6ad2` on 2026-11-02 23:17:45 +0530; last line in `eeafc85` on 2026-11-02 23:17:34 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 23:17 IST, weights-loading rule (decided by Aarnav).** Ambari-7B-Instruct-v0.2 ships only pickle `.bin` weights. It is loaded **only on Kaggle**, with `weights_only=True` forced on
  `torch.load`; `shattered.interp.load.load` refuses it anywhere else (never on the laptop).
`````

##### 2026-11-03 00:47 IST, STATUS NOTE: the tier prioritisation is WITHDRAWN and superseded (Aarnav). The tier message (tiers 1 to 3 over the experiments) was a misunderstanding of a question about which annotation is necessary; it never became 

RESULTS.md lines 3775 to 3780; first line committed in `d574ae9` on 2026-11-03 00:47:00 +0530; last line in `8a3a76f` on 2026-11-03 01:13:04 +0530; labels from the title and parent heading: none

`````text
- **2026-11-03 00:47 IST, STATUS NOTE: the tier prioritisation is WITHDRAWN and superseded (Aarnav).** The tier message (tiers 1 to 3 over the experiments) was a misunderstanding of a question about which annotation is necessary; it never became a registration entry and
  no queue, script or registered rule was changed because of it (checked against git and the queue driver: the instruction pair, Llama-3.1-8B and the X9b Qwen3.5-2B arm were never removed; X11 and X6 were never cut). Every experiment stays as registered in
  Amendment 2 and in the earlier ordering: laptop X7 control, X9a, X10, X11, X6, X4 Bengali and Telugu; Kaggle X9b (Sarvam-1 primary and Qwen3.5-2B secondary arm), X12 (contrast 1 primary, instruction pair secondary), X13 (Qwen3-8B, Llama-3.1-8B, the largest
  Sarvam that fits); X14 (Groq, under its caps). The Kaggle order is unchanged: A1-P pair, X9b pilot, scoring, Llama-2 A1-P and contrast 1, instruction pair, Llama-3.1-8B, X9b full; with the 18 h X9b Sarvam reserve and the cut order if quota is short
  (Llama-3.1-8B first, then the instruction pair, then the X9b Qwen3.5 arm). **Only the annotation part stands** (previous status note): X15 and T3 not run (annotators unavailable), X8 parked and run as registered if the files are sent.

`````

##### 2026-11-04 04:37 IST, second gated model uploaded: Llama-3.1-8B is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-3-1-8b (upload 945 s, status ready, local copy deleted). Queue gate for Llama-3.1 removed. Both datasets are on the

RESULTS.md lines 3884 to 3885; first line committed in `957499a` on 2026-11-04 04:37:26 +0530; last line in `45def39` on 2026-11-04 04:53:21 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 04:37 IST, second gated model uploaded: Llama-3.1-8B is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-3-1-8b** (upload 945 s, status ready, local copy deleted). Queue gate for Llama-3.1 removed. Both datasets are on the end-of-Phase-2 cleanup list with shattered-flores-private. Kaggle MDL Qwen3-8B still running (pushed 03:36 IST).

`````

##### 2026-11-04 13:27 IST, account 2 smoke test, attempt 1 (kaggle_gate, 0.10 h): the kernel ran on a T4 x2 session but the gate needs the laptop scores in the package (results/e0c_sib/scores, 3.2 MB), which were not included in the push: FileNo

RESULTS.md lines 3912 to 3913; first line committed in `d1ef7c9` on 2026-11-04 13:27:53 +0530; last line in `97a4a6b` on 2026-11-04 13:40:55 +0530; labels from the title and parent heading: result

`````text
- **2026-11-04 13:27 IST, account 2 smoke test, attempt 1 (kaggle_gate, 0.10 h):** the kernel ran on a T4 x2 session but the gate needs the laptop scores in the package (results/e0c_sib/scores, 3.2 MB), which were not included in the push: FileNotFoundError in all four rows, gate_passed false. Setup error, not an environment difference. Relaunched once with --include results/e0c_sib/scores (log results/phase2/acct2_gate_run2.log).

`````

##### 2026-11-04 21:53 IST, correction note to the entry above: why the 20:10 driver process ended without fetching is not established; the self-restart on changed code is the likely cause (it re-executes the process) but I did not verify it. The

RESULTS.md lines 3936 to 3937; first line committed in `58423f1` on 2026-11-04 21:53:12 +0530; last line in `06404f2` on 2026-11-04 22:07:54 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 21:53 IST, correction note to the entry above:** why the 20:10 driver process ended without fetching is not established; the self-restart on changed code is the likely cause (it re-executes the process) but I did not verify it. The fix (refuse to push a kernel still running or queued) does not depend on the cause.

`````

##### 2026-11-05 22:15 IST, THIRD KAGGLE ACCOUNT: TOKEN RECEIVED AND VERIFIED, NO COMPUTE USED YET (operational). Aarnav supplied a third Kaggle API token, described as belonging to another teammate. It is stored only in the gitignored `.env` (KA

RESULTS.md lines 4019 to 4020; first line committed in `739114f` on 2026-11-05 22:15:42 +0530; last line in `5d9fd0e` on 2026-11-05 22:23:55 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 22:15 IST, THIRD KAGGLE ACCOUNT: TOKEN RECEIVED AND VERIFIED, NO COMPUTE USED YET (operational).** Aarnav supplied a third Kaggle API token, described as belonging to another teammate. It is stored only in the gitignored `.env` (KAGGLE3_API_TOKEN, KAGGLE3_USERNAME) and never echoed. Verification: the token authenticates (an invalid token is refused) and resolves to the Kaggle username **aarnavkembhavi** (no trailing 1), an account with notebooks from 2024. That name matches Aarnav's own naming and is not the name of a teammate, so ownership was put back to Aarnav before any job runs on it; no kernel, dataset or quota has been used on it, and its GPU access (phone verification, T4 x2) is not yet tested, since that needs a kernel push. Code prepared (no secrets): `scripts/kaggle_runner.py` now knows account 3 (job folders `results/kaggle/acct3`, build folder, credentials KAGGLE3_*) and gives each account its own empty CLI config folder, because the Kaggle CLI otherwise falls back to the login stored in the user profile (that login is the account `aarnavkembhavi`). Accounts 1 and 2 were re-checked and still resolve to aarnavkembhavi1 and ashwin18522. Cleanup list additions (after Aarnav closes Phase 2): revoke the third token, delete any private datasets and kernels created on the third account, delete build/kaggle_config_3. The token was pasted in chat, so revocation matters.

`````

##### 2026-11-07 04:22 IST, QWEN3.5-2B EXTRA RUNS: SLOWER THAN PROJECTED; MICRO-BATCH CAP LOWERED TO 2 FOR THE NEXT RUNS (operational; recipe unchanged). The first Qwen extra run (ITRANS, code seed 1) trains at about 41 s per optimizer step on th

RESULTS.md lines 4046 to 4047; first line committed in `c42cfd4` on 2026-11-07 04:22:43 +0530; last line in `0cd9a82` on 2026-11-08 15:33:40 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-07 04:22 IST, QWEN3.5-2B EXTRA RUNS: SLOWER THAN PROJECTED; MICRO-BATCH CAP LOWERED TO 2 FOR THE NEXT RUNS (operational; recipe unchanged).** The first Qwen extra run (ITRANS, code seed 1) trains at about 41 s per optimizer step on the laptop (step 40 after 1,778 s), against about 26 s on the Kaggle T4; with 346 steps that is about 3.9 h of training plus about 0.6 h of evaluation per run, so the six runs take about 27 h and end about **8 Nov 07:00 IST**, not 7 Nov 20:00 to 23:00 as projected at registration. The card is at 8.0 GB (micro-batch 4, shared-memory spill), as the Sarvam-1 runs were before the cap. The cap file `build/x9b_max_micro_batch.txt` is lowered from 8 to 2 for the runs that have not started (the run in progress keeps micro-batch 4; same optimizer step of 16,384 tokens; done.json records the value); if the next run is not faster the cap is restored. If Aarnav prefers, the second seed (3 runs) can be dropped, which brings the end to about 7 Nov 20:00.

`````

##### 2026-11-08 15:33 IST, OPERATIONAL: LAPTOP GPU IDLE FROM 2026-11-07 20:05 TO NOW (about 19.5 h) AND THE WATCHDOG PAUSED (standing order 1 broken). The Qwen extra-seed chain ended at 20:05 on 7 Nov; no registered laptop job remained, and the 

RESULTS.md lines 4050 to 4051; first line committed in `0cd9a82` on 2026-11-08 15:33:40 +0530; last line in `79e0484` on 2026-11-08 15:58:25 +0530; labels from the title and parent heading: none

`````text
- **2026-11-08 15:33 IST, OPERATIONAL: LAPTOP GPU IDLE FROM 2026-11-07 20:05 TO NOW (about 19.5 h) AND THE WATCHDOG PAUSED (standing order 1 broken).** The Qwen extra-seed chain ended at 20:05 on 7 Nov; no registered laptop job remained, and the watchdog and this session were paused by the weekly usage limit (the session continued at the reset), so neither the finish nor the idle GPU was handled for about 19 h. Both finished jobs above were analysed on resume. Nothing was running on any Kaggle account that needed a restart (account 3's Sarvam-m job ended 2026-11-07 06:18).

`````

##### 2026-11-08 15:58 IST, BACKUP (Aarnav's instruction of 2026-11-08; no secrets in this entry). (1) Private GitHub repo `aarnav-kembhavi/shattered-scripts-phase2` created; the full git history was pushed (branch master, all tags; history scann

RESULTS.md lines 4052 to 4053; first line committed in `79e0484` on 2026-11-08 15:58:25 +0530; last line in `0034538` on 2026-11-08 16:23:25 +0530; labels from the title and parent heading: result

`````text
- **2026-11-08 15:58 IST, BACKUP (Aarnav's instruction of 2026-11-08; no secrets in this entry).** (1) Private GitHub repo `aarnav-kembhavi/shattered-scripts-phase2` created; the full git history was pushed (branch master, all tags; history scanned first: `.env` never committed, no key patterns in any revision, no blob over 100 MB). (2) `results/` archived with `scripts/backup_manifest.py`: 12,921 files, 352,387,091 bytes (246,404,518 zipped), uploaded as release asset `results.zip` of release `backup-2026-11-08` in the same private repo and verified by downloading it again (sha256 c831157a…47233 equals the local archive's). (3) Also archived locally: `annotation.zip` (60 files) and `root_docs.zip` (494 files: RESULTS.md, docs, paper2, configs, scripts, src), in `C:\PROJECTS\PROMPT\backup_phase2_2026-11-08` with `MANIFEST.json`; the annotation archive was deliberately not put on GitHub (those folders are kept out of git for annotator anonymity). (4) Google Drive: a private folder `Shattered Scripts Phase 2 backup 2026-11-08` was created and holds README.txt and the manifest; **the zip files could not be uploaded to Drive from this session** (the connector passes file content inline and the browser upload tool is limited to 10 MB per call and cannot operate the native file picker), so the three zip files must be dragged into that folder by hand. Excluded on purpose: .env and every token or credential file, the Hugging Face cache, model weights and training checkpoints (25 files, 1,947,197,584 bytes: adapter_model.safetensors and ckpt.pt), the virtual environment, cache/, build/, data/raw, .git. Backup location of record: GitHub private repo + the laptop folder above; Drive folder id in the Drive account of the lead author.

`````

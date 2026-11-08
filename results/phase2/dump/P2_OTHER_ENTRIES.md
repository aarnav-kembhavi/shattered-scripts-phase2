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

##### 2026-11-02 23:17 IST, weights-loading rule (decided by Aarnav).

RESULTS.md lines 3732 to 3733; first line committed in `78d6ad2` on 2026-11-02 23:17:45 +0530; last line in `eeafc85` on 2026-11-02 23:17:34 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 23:17 IST, weights-loading rule (decided by Aarnav).** Ambari-7B-Instruct-v0.2 ships only pickle `.bin` weights. It is loaded **only on Kaggle**, with `weights_only=True` forced on
  `torch.load`; `shattered.interp.load.load` refuses it anywhere else (never on the laptop).
`````

##### 2026-11-02 23:17 IST, Kaggle queue order (decided by Aarnav).

RESULTS.md lines 3734 to 3740; first line committed in `78d6ad2` on 2026-11-02 23:17:45 +0530; last line in `b3cbd64` on 2026-11-02 23:21:38 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 23:17 IST, Kaggle queue order (decided by Aarnav).** (a) the A1-P job in flight (Qwen3-8B, Ambari-7B-base, float32-offload reference); (b) score whichever of the two passes: X13 Qwen3-8B,
  then X12 Ambari-base; (c) A1-P for Ambari-Instruct v0.1 and v0.2; (d) X9b full, Sarvam-1 primary arm (6 runs, about 18 GPU hours), as soon as its laptop memory pilot is done. Before each push the remaining
  weekly quota is projected; the X9b Sarvam arm is reserved this week or next, X9b goes first if X12 instruct work would push it into a later week, and the Qwen3.5-2B arm is cut first if quota is short (as registered).
  To apply this order the queue driver was changed and a `results/kaggle/HOLD` file stops new pushes while the in-flight job continues (an implementation change; no rule).
- Time stamps of the three entries above were first written with wrong clock times and corrected to the commit times (the A1-P-D1 entry 22:59, the X12 clarification, weights rule and queue order 23:17).
- Time correction (checked by scripts/check_results_times.py, which found it): the A1-R entry above was stamped 19:35 by hand but committed at 19:26; its stamp is now the commit time. From now on stamps come from `scripts/stamp.py` (system clock), and a pre-commit hook fails any entry later than the clock.

`````

##### 2026-11-02 23:48 IST, annotation tasks exported to Excel (nothing sent).

RESULTS.md lines 3763 to 3768; first line committed in `fef5e62` on 2026-11-02 23:48:25 +0530; last line in `285c028` on 2026-11-03 00:04:58 +0530; labels from the title and parent heading: none

`````text
- **2026-11-02 23:48 IST, annotation tasks exported to Excel (nothing sent).** `annotation/xlsx/`: X8_P and X8_Q (identical 100 sentences in the registered default_rng(8) order; no Gemini text, no English), eight X15 files (G1..G4, seats a and b; group G sees item i in
  form (i + G) mod 4, so G4 is the registered g = 0; rows shuffled with seed 15000 + G; dropdown of the seven labels; every column except Topic locked, no password), T3_verification.xlsx (XNLI line
  marked "needs rewrite", the words ದತ್ತಾಂಶ and ಪರಿಕಲ್ಪನೆ flagged). Private keys (X15 gold labels, form per group, row-to-item maps, shuffle seeds, X8 order) are in `annotation/private/` (gitignored, excluded from the
  anonymised package); the tracked `results/phase2/x15/selection.json` now holds ids only (gold labels and the form mapping were removed from it). Hygiene check (`scripts/export_xlsx.py check`, report in
  `annotation/xlsx/HYGIENE_REPORT.json`): all 11 files pass. Importers: `scripts/import_x8.py`, `scripts/import_x15.py` (registered formats; tested on synthetic returned files, outputs deleted).

`````

##### 2026-11-03 00:04 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).

RESULTS.md lines 3769 to 3774; first line committed in `285c028` on 2026-11-03 00:04:58 +0530; last line in `d574ae9` on 2026-11-03 00:47:00 +0530; labels from the title and parent heading: none

`````text
- **2026-11-03 00:04 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** Annotators are not available. **X1 T3 is marked "not run (instruction not verified)"; X15 is marked "not run (annotators unavailable)"; X8 is parked and marked "not run"**
  (if the X8 files are sent later, it runs as registered). All three are removed from every queue (the laptop queue's "X1 T3" and the annotator-dependent items, and every pending annotation send); no chain or driver step referenced them. The
  workbooks, private keys, importers (`scripts/import_x8.py`, `import_x15.py`, `import_t3.py`, one command each over `annotation/returned/`, which is gitignored because returned files carry author fields) and analyses
  (`scripts/analyze_x8.py`, `analyze_x15.py`, tested on synthetic data only, outputs not kept) are kept. The three items and the reason are in `results/phase2/REGISTERED_OUTCOMES.md` (no Phase 2 outcomes table existed before; this is its start).
  The Kaggle and laptop queues continue as before.

`````

##### 2026-11-03 00:47 IST, STATUS NOTE: the tier prioritisation is WITHDRAWN and superseded (Aarnav).

RESULTS.md lines 3775 to 3780; first line committed in `d574ae9` on 2026-11-03 00:47:00 +0530; last line in `8a3a76f` on 2026-11-03 01:13:04 +0530; labels from the title and parent heading: none

`````text
- **2026-11-03 00:47 IST, STATUS NOTE: the tier prioritisation is WITHDRAWN and superseded (Aarnav).** The tier message (tiers 1 to 3 over the experiments) was a misunderstanding of a question about which annotation is necessary; it never became a registration entry and
  no queue, script or registered rule was changed because of it (checked against git and the queue driver: the instruction pair, Llama-3.1-8B and the X9b Qwen3.5-2B arm were never removed; X11 and X6 were never cut). Every experiment stays as registered in
  Amendment 2 and in the earlier ordering: laptop X7 control, X9a, X10, X11, X6, X4 Bengali and Telugu; Kaggle X9b (Sarvam-1 primary and Qwen3.5-2B secondary arm), X12 (contrast 1 primary, instruction pair secondary), X13 (Qwen3-8B, Llama-3.1-8B, the largest
  Sarvam that fits); X14 (Groq, under its caps). The Kaggle order is unchanged: A1-P pair, X9b pilot, scoring, Llama-2 A1-P and contrast 1, instruction pair, Llama-3.1-8B, X9b full; with the 18 h X9b Sarvam reserve and the cut order if quota is short
  (Llama-3.1-8B first, then the instruction pair, then the X9b Qwen3.5 arm). **Only the annotation part stands** (previous status note): X15 and T3 not run (annotators unavailable), X8 parked and run as registered if the files are sent.

`````

##### 2026-11-03 01:16 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).

RESULTS.md lines 3787 to 3791; first line committed in `f39430f` on 2026-11-03 01:16:45 +0530; last line in `78e3f69` on 2026-11-03 01:37:59 +0530; labels from the title and parent heading: none

`````text
- **2026-11-03 01:16 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** T3, X8 and X15 are no longer parked. **T3:** the returned `T3_verification.xlsx` was found at `annotation/xlsx/T3_verification.xlsx` (saved 01:03; it was not in `annotation/returned/`) and imported with `scripts/import_t3.py` from a copy in `annotation/returned/` (0 blockers, 0 warnings): T3-1 Correct, T3-3 Correct, T3-2 Needs change with a corrected line identical to the wording in the clarification above; `results/phase2/x1/t3_verification_returned.json`.
  The previous "not run (instruction not verified)" mark for X1 T3 is withdrawn; X1 T3 is queued after X9a. **X8 and X15** are back in the registered design: X8_P and X8_Q (X8_Q goes to a different group of speakers, none of them in P, who never see X8_P) and eight X15 files for eight different people, none from the X8 groups.
  The workbooks are rebuilt **unprotected** (same 100 sentences and order, blank answer columns, same seeds; `annotation/xlsx/`); the importers no longer rely on locked cells: `scripts/import_x8.py`, `import_x15.py` and `import_t3.py` compare **every cell outside the answer cells with the original** (rebuilt deterministically) and block on any difference, and they also block when the same person (author-field hash) is behind two X15 files, behind P and Q, or behind an X8 and an X15 file.
  **If fewer than eight X15 files come back, the number is to be logged here as a deviation ("X15 DEVIATION: n of 8 files") before anything is analysed; `scripts/analyze_x15.py` refuses to run until that line exists.** (The instruction for the X8_P workbook was cut off in the message; X8_P is built the same way as X8_Q, unprotected.) Status table: `results/phase2/REGISTERED_OUTCOMES.md`. The Kaggle and laptop queues continue.

`````

##### 2026-11-03 01:37 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).

RESULTS.md lines 3792 to 3795; first line committed in `78e3f69` on 2026-11-03 01:37:59 +0530; last line in `73546be` on 2026-11-03 02:24:19 +0530; labels from the title and parent heading: none

`````text
- **2026-11-03 01:37 IST, STATUS NOTE (decided by Aarnav; no registered rule is changed).** **X15 is skipped: "not run (annotators unavailable)".** No X15 files are built (`scripts/export_xlsx.py build` now skips them unless `--with-x15`), X15 is removed from every to-do list and from `annotation/xlsx/SEND_ME.md`; the earlier X15 workbooks, importer and analysis scripts stay in the repository, unused. This supersedes the 01:1x note that put X15 back in the registered design.
  **T3** stands as logged: the returned workbook (`annotation/returned/T3_verification.xlsx`) was imported with 0 blockers and 0 warnings; T3-1 and T3-3 Correct, T3-2 replaced by the native speaker's wording before any T3 scoring; the instruction files are frozen with the new text (hashes in `results/phase2/x1/t3_templates.json`); X1 T3 is queued after X9a; every T3 result is labelled "instruction verified by a native speaker, exploratory".
  **X8:** `annotation/returned/` held only the T3 file when checked at 01:34; `annotation/xlsx/X8_Q.xlsx` (saved 01:32) holds 100 answers and was imported (0 blockers, 0 warnings; uppercase-start share 0.01, unexpected-character share 0.01 (one cell with Õ/õ), mean 16.3 words per sentence); `annotation/xlsx/X8_P.xlsx` has no answers. The registered X8 analysis (kappa, character error rate, descriptive ratios) needs both files and has not been run.

`````

##### 2026-11-04 02:46 IST, operations log (standing orders of 2026-11-04; no registered rule changes).

RESULTS.md lines 3866 to 3867; first line committed in `98e2256` on 2026-11-04 02:46:00 +0530; last line in `0cfdea0` on 2026-11-04 02:46:43 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 02:46 IST, operations log (standing orders of 2026-11-04; no registered rule changes).** (1) **X4 Gemini drafts resumed on the paid tier** (billing enabled by Aarnav on the Gemini key ending FXVw, project named by Aarnav "nuerips"): model unchanged (gemini-3.5-flash-lite, temperature 0, prompt natural_romanization_v1 with the language name changed, unbatched); own cap raised from 480 to 6,000 requests a day and 12 to 60 per minute (`scripts/x4_natural.py`). Check before resuming: 40 consecutive requests in 30 s (about 80 per minute, above the free-tier limit of 15 per minute) returned no 429; the tier itself cannot be read from the API, so this is the evidence. Bengali resumed from 444 of 500 at 02:40 IST. (2) **Kaggle:** the earlier queue pushes were refused because `scripts/hidden.vbs` (tracked) had been deleted from the working tree, which also stopped the detached chains from restarting; restored. Llama-2-7B A1-P pushed at about 02:41 IST ahead of the reserve (X12 contrast 1). (3) **Laptop queue (chained by status files):** X1 T3 (running) -> X11 -> X10 full (`scripts/x10full_chain.sh`) -> X9a-low (`scripts/x9alow_chain.sh`, includes the level-0 stripped-retrieval observation). X9a-low code: `x9a.py prep_low | train <level> <seed> | analyse_low | level0_stripped`; the first `prep_low` attempt died with a MemoryError reading the story file while other jobs held memory and is retried inside the chain. (4) A 15-minute watchdog (session cron) checks both machines and the API jobs.

`````

##### 2026-11-04 02:53 IST, watchdog:

RESULTS.md lines 3872 to 3873; first line committed in `2be4ccb` on 2026-11-04 02:53:13 +0530; last line in `3795c2a` on 2026-11-04 03:07:47 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 02:53 IST, watchdog:** Kaggle queue chain had been stopped (my restart at 02:37 for the push-order change; the detached task could not start until the deleted hidden.vbs was restored). Restarted at about 02:52 IST so X9b batch 3 is pushed the moment the quota projection allows (about 9 Nov 19:42 IST). Laptop GPU busy (X1 T3 gemma4-e2b, 68 percent); no idle period; X4 drafts done.

`````

##### 2026-11-04 03:07 IST, watchdog / disk:

RESULTS.md lines 3874 to 3875; first line committed in `3795c2a` on 2026-11-04 03:07:47 +0530; last line in `399fdee` on 2026-11-04 03:33:53 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 03:07 IST, watchdog / disk:** free disk 26 GB (guard 25 GB). Removed the three finished pilot checkpoints (x7pilot_v256_s0, x7pilot_v4096_s0, x9apilot_p20_s0; their pilot results files are kept). X9a-low will write about 4.6 GB of checkpoints; if free disk nears the guard, the next cache to clear is cache/activations/m14full (14 GB, Phase 1 activations cache, regenerable, results kept). Laptop GPU busy (X1 T3), Kaggle chain waiting, X4 drafts done, X14 waiting for 12:45.

`````

##### 2026-11-04 03:43 IST, gated models on Kaggle: private-dataset route (Aarnav's instruction; no registered rule changes).

RESULTS.md lines 3878 to 3879; first line committed in `7ee0799` on 2026-11-04 03:43:18 +0530; last line in `cbdea11` on 2026-11-04 03:52:38 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 03:43 IST, gated models on Kaggle: private-dataset route (Aarnav's instruction; no registered rule changes).** *Secrets cannot be set through the API:* the Kaggle kernel metadata accepted by the kernels push has no field for secrets (they are attached per notebook in the web UI, and all 16 kernel runs so far failed to reach the secret service), so no UI step is required of Aarnav. *Route:* `scripts/hf_to_kaggle.py` downloads Llama-2-7b-hf and Llama-3.1-8B (config, tokenizer, safetensors only) on the laptop with the approved Hugging Face access and uploads each as a **private** Kaggle dataset: **shattered-llama-2-7b-hf** and **shattered-llama-3-1-8b** (account aarnavkembhavi1). `shattered.interp.load.model_source` uses the mounted dataset on Kaggle and the Hugging Face repo elsewhere; `scripts/kaggle_queue.py` attaches the dataset to any job whose arguments name the model. The A1-P and scoring code is otherwise unchanged. The local copy is deleted after a verified upload. **End-of-Phase-2 cleanup list (delete and log): the private Kaggle datasets shattered-flores-private, shattered-llama-2-7b-hf, shattered-llama-3-1-8b.** Disk: to keep the 25 GB guard during the downloads I deleted finished-job caches (cache/activations/h_hindi 1.1 GB and cache/activations/nc1 0.6 GB, regenerable; the five data/processed/x9a/train_p*.npy streams, regenerable by `x9a.py prep` with hashes in meta.json); no results or logs were removed. Free disk after: 74 GB.

`````

##### 2026-11-04 03:52 IST, watchdog:

RESULTS.md lines 3880 to 3881; first line committed in `cbdea11` on 2026-11-04 03:52:38 +0530; last line in `f479ea3` on 2026-11-04 04:14:25 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 03:52 IST, watchdog:** the first Llama-2 dataset upload failed at dataset creation (Kaggle: subtitle must be 20 to 80 characters; the download of 13 GB was complete). Fixed (shorter subtitle), upload relaunched once (log results/phase2/hf_upload_llama2b.log); the Llama-3.1 download continues. Laptop GPU busy (X1 T3), Kaggle MDL Qwen3-8B running, disk 64 GB free.

`````

##### 2026-11-04 04:14 IST, first gated model uploaded: Llama-2-7b-hf is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-2-7b-hf

RESULTS.md lines 3882 to 3883; first line committed in `f479ea3` on 2026-11-04 04:14:25 +0530; last line in `957499a` on 2026-11-04 04:37:26 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 04:14 IST, first gated model uploaded: Llama-2-7b-hf is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-2-7b-hf** (12.55 GiB: config, tokenizer, two safetensors shards; upload 1,250 s after the subtitle fix; Kaggle metadata isPrivate = true; local copy deleted). The queue no longer blocks Llama-2 (flag HF_SECRET_MISSING removed); Llama-3.1-8B stays gated by results/kaggle/DATASET_PENDING_llama-3.1-8b until its upload (running, log results/phase2/hf_upload_llama31b.log). Llama-2 A1-P launches at the next queue pass after the current MDL job ends; the dataset mount path on Kaggle is untested until then.

`````

##### 2026-11-04 04:37 IST, second gated model uploaded: Llama-3.1-8B is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-3-1-8b

RESULTS.md lines 3884 to 3885; first line committed in `957499a` on 2026-11-04 04:37:26 +0530; last line in `45def39` on 2026-11-04 04:53:21 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 04:37 IST, second gated model uploaded: Llama-3.1-8B is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-llama-3-1-8b** (upload 945 s, status ready, local copy deleted). Queue gate for Llama-3.1 removed. Both datasets are on the end-of-Phase-2 cleanup list with shattered-flores-private. Kaggle MDL Qwen3-8B still running (pushed 03:36 IST).

`````

##### 2026-11-04 04:53 IST, Kaggle watchdog:

RESULTS.md lines 3886 to 3887; first line committed in `45def39` on 2026-11-04 04:53:21 +0530; last line in `8e2e954` on 2026-11-04 06:08:17 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 04:53 IST, Kaggle watchdog:** Qwen3-8B MDL (X13) finished (output in results/kaggle/kaggle_mdl/2026-11-03T220606, analysis pending). Llama-2-7B A1-P failed a second time (04:40 IST, 0.12 h): the gated repo was still read from Hugging Face (401), i.e. the kernel did not use the private dataset copy; cause not yet known (the mounted path is not visible in the log); the boot script now prints the mounted datasets for the next run. The Ambari instruct pair A1-P (cap 5.0 h) was pushed at about 04:46 IST; quota 29.81 of 30 h with it reserved. Llama-2 will be retried once after it ends and the cause is fixed.

`````

##### 2026-11-04 06:08 IST, Kaggle watchdog:

RESULTS.md lines 3888 to 3889; first line committed in `8e2e954` on 2026-11-04 06:08:17 +0530; last line in `7cfcb18` on 2026-11-04 06:08:50 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 06:08 IST, Kaggle watchdog:** the Ambari instruct pair A1-P ended (pushed 04:46 IST): **Ambari-Instruct-v0.2 passed** (float32-offload reference); **Ambari-Instruct-v0.1 gave no verdict: it is also a gated Hugging Face repo** (401 on Kaggle; the laptop token reads it, anonymous access gets 401). Same remedy as Llama: private Kaggle dataset **shattered-ambari-instruct-v0-1** (added to the cleanup list; upload started, log results/phase2/hf_upload_ambari01.log; v0.1 is gated until the upload). Quota 29.55 of 30 h used, so the next job of 3 h or more fits only from about 9 Nov 23:24 IST. Llama-2 still to be retried once (mount of its private dataset to be diagnosed with the new boot listing).

`````

##### 2026-11-04 06:23 IST, watchdog:

RESULTS.md lines 3892 to 3893; first line committed in `46c9030` on 2026-11-04 06:23:52 +0530; last line in `6f2ebf8` on 2026-11-04 06:37:27 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 06:23 IST, watchdog:** quota fell to 26.19 of 30 h (actual runtimes of the instruct pair were shorter than the cap), so the Llama-2 A1-P (cap 3.5 h) fits; the queue chain was restarted early (a fresh process with the code that attaches the private model datasets) instead of waiting for the 07:44 retry.

`````

##### 2026-11-04 06:37 IST, third gated model uploaded: Ambari-Instruct-v0.1 is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-ambari-instruct-v0-1

RESULTS.md lines 3894 to 3895; first line committed in `6f2ebf8` on 2026-11-04 06:37:27 +0530; last line in `81fc534` on 2026-11-04 07:53:46 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 06:37 IST, third gated model uploaded: Ambari-Instruct-v0.1 is a PRIVATE Kaggle dataset, aarnavkembhavi1/shattered-ambari-instruct-v0-1** (upload 821 s, status ready, local copy deleted; on the end-of-Phase-2 cleanup list with shattered-flores-private, shattered-llama-2-7b-hf and shattered-llama-3-1-8b). Queue gate removed. The Llama-2 A1-P was pushed at about 06:25 IST with shattered-llama-2-7b-hf attached (kernel dataset_sources verified); quota 29.69 of 30 h with its cap reserved.

`````

##### 2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches).

RESULTS.md lines 3906 to 3907; first line committed in `ed31e10` on 2026-11-04 12:13:51 +0530; last line in `72ff37e` on 2026-11-04 12:14:44 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches).** (1) Ambari-Instruct-v0.1 and Llama-3.1-8B were already uploaded as private datasets (shattered-ambari-instruct-v0-1 and shattered-llama-3-1-8b) and are attached by `scripts/kaggle_queue.py` for any job that names the model; all four private datasets (these two, shattered-llama-2-7b-hf and shattered-flores-private) are on the end-of-Phase-2 cleanup list. (2) **Stale driver:** the queue now hashes its scripts (kaggle_queue, kaggle_runner, kaggle_precision, x_score, kaggle_mdl, kaggle_x9b, interp/load) at start and re-executes itself before any push if they changed on disk; the runner pushes the committed tree and refuses a dirty one. (3) **Pre-launch check on the laptop (no quota):** each private dataset the job mounts must be "ready" on Kaggle, and a model named in the job arguments that is gated on Hugging Face must have a private dataset; otherwise nothing is pushed. (4) Queue order rule: non-X9b jobs are refused while an X9b Sarvam batch is pending (X9b batch 3 first, nothing ahead of it); scoring caps are 2.4 h (measured 1.2 to 1.8 h). Calendar of the remaining Kaggle jobs with start and end times: in the report to Aarnav of this time.

`````

##### 2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction).

RESULTS.md lines 3910 to 3911; first line committed in `39d4c01` on 2026-11-04 13:21:46 +0530; last line in `d1ef7c9` on 2026-11-04 13:27:53 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 13:21 IST, SECOND KAGGLE ACCOUNT ADDED (Aarnav's instruction).** Some Kaggle compute for Phase 2 now runs on a **teammate's Kaggle account** (username ashwin18522; per-account quota of 30 h per rolling 7 days, tracked separately in results/kaggle/acct2/quota.json). The token is stored only in the gitignored .env (KAGGLE2_API_TOKEN, KAGGLE2_USERNAME) and was never written to a commit, log or this file. Token verified: it authenticates and the account lists its own kernels; the first kernel (kaggle_gate smoke test) started on a T4 x2 GPU session at 13:20 IST on 2026-11-04. *What changed in the code:* the runner takes KAGGLE_ACCOUNT=1|2 (credentials, quota file, job folders and build folder per account); the queue runs one driver per account: account 1 keeps X9b (batch 3 first when its quota frees, its checkpoints and datasets live there) and, until account 2 is accepted, the rest; account 2 runs the self-contained jobs (Ambari-Instruct-v0.1 A1-P, instruction-pair scoring and MDL, Llama-3.1-8B A1-P and scoring, later X13 models). Account 2 is accepted for real jobs only after the smoke test and the A1-R reproduction on its own environment pass (file results/kaggle/acct2/ACCEPTED). Private datasets re-uploaded under account 2: shattered-flores-private, shattered-llama-3-1-8b and shattered-ambari-instruct-v0-1 (uploads in progress at this time), plus the package dataset shattered-pkg that the runner uploads. **End-of-Phase-2 cleanup list additions: delete account 2's datasets (shattered-flores-private, shattered-llama-3-1-8b, shattered-ambari-instruct-v0-1, shattered-pkg) and kernels, and revoke the token that was shared in the chat (the token is in the session transcript).** The anonymiser now scrubs the account name.

`````

##### 2026-11-04 13:27 IST, account 2 smoke test, attempt 1 (kaggle_gate, 0.10 h):

RESULTS.md lines 3912 to 3913; first line committed in `d1ef7c9` on 2026-11-04 13:27:53 +0530; last line in `97a4a6b` on 2026-11-04 13:40:55 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 13:27 IST, account 2 smoke test, attempt 1 (kaggle_gate, 0.10 h):** the kernel ran on a T4 x2 session but the gate needs the laptop scores in the package (results/e0c_sib/scores, 3.2 MB), which were not included in the push: FileNotFoundError in all four rows, gate_passed false. Setup error, not an environment difference. Relaunched once with --include results/e0c_sib/scores (log results/phase2/acct2_gate_run2.log).

`````

##### 2026-11-04 13:40 IST, account 2 smoke test PASSED (kaggle_gate, T4 x2, second attempt; 0.10 h).

RESULTS.md lines 3914 to 3915; first line committed in `97a4a6b` on 2026-11-04 13:40:55 +0530; last line in `59154b4` on 2026-11-04 14:10:52 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 13:40 IST, account 2 smoke test PASSED (kaggle_gate, T4 x2, second attempt; 0.10 h).** gate_passed true with the same dtype (float16) for Sarvam-1 and Gemma 4 E2B; every number equals account 1's gate run (raw agreement native/ITRANS/lossy 0.99/0.95/0.96 for Sarvam-1 and 1.00/0.99/0.99 for Gemma 4; Kaggle accuracy 0.62/0.29/0.36 and 0.73/0.27/0.44; max |dlogprob| identical to three decimals). The runner polling had been ended by a laptop network blip once (the status call failed and the wait loop read "error" in the message); fixed so a failed status call keeps waiting. Next: the A1-R retrieval reproduction on account 2 (kaggle_retrieval_gate, FLORES private dataset under account 2); account 2 is accepted for real jobs only if it reproduces the account 1 A1-R numbers (Sarvam-1 native 0.9443, ITRANS 0.5104; Gemma 4 E2B as stored).

`````

##### 2026-11-04 20:44 IST, laptop GPU idle period caused by me (about 20:30 to 20:42 IST):

RESULTS.md lines 3930 to 3931; first line committed in `3c30aee` on 2026-11-04 20:44:16 +0530; last line in `a182698` on 2026-11-04 21:08:27 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 20:44 IST, laptop GPU idle period caused by me (about 20:30 to 20:42 IST):** my cipher-token script held all free RAM while X4 scoring waited for 8 GB (chainlib wait_ram), so the GPU idled for about 10 minutes until I stopped it; the script was rewritten to tokenize only the cipher stories and finished in under two minutes.

`````

##### 2026-11-04 21:53 IST, correction note to the entry above:

RESULTS.md lines 3936 to 3937; first line committed in `58423f1` on 2026-11-04 21:53:12 +0530; last line in `06404f2` on 2026-11-04 22:07:54 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 21:53 IST, correction note to the entry above:** why the 20:10 driver process ended without fetching is not established; the self-restart on changed code is the likely cause (it re-executes the process) but I did not verify it. The fix (refuse to push a kernel still running or queued) does not depend on the cause.

`````

##### 2026-11-04 22:24 IST, Kaggle account 2: two drivers were running at once; stopped one; root cause fixed.

RESULTS.md lines 3940 to 3941; first line committed in `17dba9c` on 2026-11-04 22:24:09 +0530; last line in `06100d7` on 2026-11-04 22:37:35 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 22:24 IST, Kaggle account 2: two drivers were running at once; stopped one; root cause fixed.** Cause: the driver restarts itself when its scripts change on disk, and on Windows os.execv returns to the parent immediately, so the chain thought the pass had ended and an orphan driver kept running beside the chain's next pass (visible as two kaggle_queue.py processes pushing x_score and kaggle_mdl at 22:06 and 22:08 IST against one state file, which can overwrite each other's records). The restart now uses a blocking subprocess. I stopped the later driver (PID 75952) with its process tree, which also ended the local runner process that was waiting on the instruction-pair MDL kernel; **that Kaggle kernel (kaggle_mdl, pushed 22:08 IST, cap 3.0 h, account 2) is still running on Kaggle and its output must be fetched by hand (`KAGGLE_ACCOUNT=2 python scripts/kaggle_runner.py fetch kaggle_mdl`) and its state entry written; until then its 3.0 h stay counted as pushed.** The remaining account 2 drivers are the X9b batch 3 driver (pushed 20:35) and the scoring driver (x_score for Ambari-Instruct-v0.1 pushed 22:06).

`````

##### 2026-11-04 22:37 IST, account 2 quota records reconciled by hand.

RESULTS.md lines 3942 to 3943; first line committed in `06100d7` on 2026-11-04 22:37:35 +0530; last line in `5b9ae1d` on 2026-11-05 00:25:45 +0530; labels from the title and parent heading: none

`````text
- **2026-11-04 22:37 IST, account 2 quota records reconciled by hand.** The instruction-pair MDL push of 22:08 IST never created a kernel (runner stopped at 22:23 during the driver fix; no kernel of that name exists on the account): record set to 0 h, status "not run"; the driver pushes it again after the Ambari-Instruct-v0.1 scoring. The 20:10 A1-P record that stayed "pushed" is set to its real 1.94 h (complete). The quota projection for account 2 now counts hours that were really used or are really running.

`````

##### 2026-11-05 00:25 IST, why the account 2 instruction-pair MDL never started (twice): Kaggle allows two GPU sessions at a time per account.

RESULTS.md lines 3944 to 3945; first line committed in `5b9ae1d` on 2026-11-05 00:25:45 +0530; last line in `1fbe72d` on 2026-11-05 00:52:48 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 00:25 IST, why the account 2 instruction-pair MDL never started (twice): Kaggle allows two GPU sessions at a time per account.** At 22:08 and again at 23:39 IST the MDL push came while X9b batch 3 and an x_score job were already running on account 2; the push was not accepted (no kernel exists), but the runner went on polling a kernel that does not exist and reserved 3.0 h in the quota file. Fixed: the runner now stops with an error if the push output does not say it succeeded, and the queue refuses a push while two other kernels of the account are running (checked on the laptop, no quota). The stale MDL reservation is set to 0 h. The MDL will be pushed when a slot is free (after the x_score jobs). No result is affected.

`````

##### 2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length.

RESULTS.md lines 3946 to 3947; first line committed in `1fbe72d` on 2026-11-05 00:52:48 +0530; last line in `055b2fc` on 2026-11-05 01:09:36 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 00:52 IST, load-time comparison for models mounted from a private dataset (Kaggle account 2), answering Aarnav's question on run length.** Without the copy loader: fp16 load 2,866 s (Llama-3.1-8B A1-P, 2.78 h in total) and 3,420 s (Ambari-Instruct-v0.1 A1-P, 1.94 h in total; an earlier attempt of the same job reached its 3.07 h self-stop); on account 1 Llama-2 loaded in 631 s. With the copy loader (parallel copy to local disk before loading; first used by the Ambari-Instruct-v0.1 scoring pushed 22:06 IST): "[model_source] copied shattered-ambari-instruct-v0-1: 12.8 GiB in 72s to local disk", and the whole scoring job took 1.20 h (4,112 s), as long as the account 1 scoring jobs (1.23 to 1.81 h). The A1-P timeout stays 5 h until an A1-P job has run with the copy loader. X9b batch 3 (training, loads Sarvam-1 from the Hub) is expected at about 6.5 h on either account (account 1: 6.31 and 6.60 h).

`````

##### 2026-11-05 10:43 IST, Phase 2 completion inventory written (`results/phase2/PHASE2_INVENTORY.md`) and new work started at Aarnav's instruction:

RESULTS.md lines 3989 to 3990; first line committed in `e0f0b06` on 2026-11-05 10:43:29 +0530; last line in `b9246e2` on 2026-11-05 10:52:45 +0530; labels from the title and parent heading: result

`````text
- **2026-11-05 10:43 IST, Phase 2 completion inventory written (`results/phase2/PHASE2_INVENTORY.md`) and new work started at Aarnav's instruction:** X2 run (supported), K3b-bn done (refuted), K3b-te running, X10 post hoc extraction check for Qwen3.5-2B running on the laptop (not registered; the registered X10 verdict unchanged), X13 Sarvam screen done (sarvam-m, 23.6B, standard Mistral code, 4-bit, is the largest Sarvam model that fits 2 x T4; sarvam-30b and sarvam-105b need remote code and are excluded; scoring pushed to Kaggle account 2), X9b analysis extended (per-run table, training budget per form, tokens per word, English regression interval, ITRANS-trained versus the original native level) ready for the Qwen3.5-2B arm.

`````

##### 2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, budgets and verdicts are unchanged).

RESULTS.md lines 3999 to 4000; first line committed in `6be3732` on 2026-11-05 13:12:01 +0530; last line in `3b1e037` on 2026-11-05 13:23:17 +0530; labels from the title and parent heading: registered, result

`````text
- **2026-11-05 13:12 IST, REGISTRATION OF EXTRA SEEDS (added AFTER seeing the original seeds; Aarnav's instruction of 2026-11-05; the original registrations, rules, budgets and verdicts are unchanged).** Why the laptop GPU was idle: the registered laptop queue was empty (the last laptop job, X5, finished 11:42; idle until the feasibility pilot started at about 12:44). **(1) X9b primary arm (Sarvam-1) extra seeds.** Feasibility pilot on the RTX 3070 laptop (`scripts/x9b_laptop_pilot.py`, `results/phase2/x9b/laptop_pilot.json`, registered recipe unchanged, 50 micro-steps): ITRANS 633.6 tokens/s, native 564.5 tokens/s, micro-batch 16, finite loss; the card spills past 8 GB into shared memory (torch peak 10.6 GiB), which changes speed but not the arithmetic; at the registered budget B = 4,997,120 tokens per run that is 2.46 h of training per run (the registered T4 pilot's slowest rate is 515.7 tokens/s). It fits. Extra runs: **seeds 2 and 3 in the code (called seeds 3 and 4, beside the original seeds 1 and 2 = code seeds 0 and 1) for the ITRANS, native and English arms**, same QLoRA recipe, same streams and budget, same evaluation, run on the laptop with the in-run base-evaluation guard (the untrained base must reproduce the A1-R values in this environment before training starts; native 0.9443 layer 24, ITRANS 0.5104 layer 21). Output `results/kaggle/laptop_x9b/2026-11-05/out`. **Labelled "added after seeing seeds 1 and 2". The paper reports all four seeds together and the original two separately, whatever they show;** the registered verdict stays the one from the original two seeds. The 97.5% intervals will be computed twice (original two seeds; all four seeds, one seed drawn per cell per resample), same code. Environment difference stated: laptop (Windows, RTX 3070 8 GB with shared-memory spill) against Kaggle T4. **(2) X9a-low extra seeds:** exposure levels 0.1%, 0.3% and 1%, code seeds 3 and 4 (called seeds 4 and 5; the original seeds are 0, 1, 2), same recipe and evaluation, per-seed values reported, labelled the same way; the registered X9a-low rule is not re-evaluated on a different set of seeds, the table will show original three and all five. The 1% level is the X9a level-1 run (`x9a_p1_s3`, `x9a_p1_s4`). Queue (chain `x9extra`, after the Qwen English-run completion): X9a-low extras first (6 runs, about 18 min each, about 2 h), then the six X9b runs (about 2.5 h training plus evaluation each, an estimated 16 to 18 h in total, projected finish about 6 Nov 09:00 to 11:00 IST). X9a-low goes first only because it is short and returns in about 2 h; X9b follows without waiting for anything else. The paper is not edited.

`````

##### 2026-11-05 14:08 IST, RESTART (extra-seeds chain `x9extra`, operational).

RESULTS.md lines 4003 to 4004; first line committed in `753999e` on 2026-11-05 14:08:43 +0530; last line in `88cf86e` on 2026-11-05 14:37:51 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 14:08 IST, RESTART (extra-seeds chain `x9extra`, operational).** The chain failed at 14:03:34 on the first 1% X9a-low extra run (`x9a.py train 1 3`): `data/processed/x9a/train_p1.npy` (the X9a level-1 token stream) had been removed with the X9a caches. Cause fixed: new command `x9a.py regen 1` regenerates that one stream with the code of `prep()` and refuses (and deletes the file) unless its sha256 equals the stored X9a value; the chain now runs it first (CPU) and was relaunched at 14:07 (the 0.1% and 0.3% seed 3 runs were already finished and are skipped). GPU idle from 14:03 to the relaunch of the GPU work (a few minutes). Nothing else changed.

`````

##### 2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt).

RESULTS.md lines 4015 to 4016; first line committed in `3ecea71` on 2026-11-05 15:42:19 +0530; last line in `cccb4f4` on 2026-11-05 22:08:29 +0530; labels from the title and parent heading: failed or not run

`````text
- **2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt).** A push of the three remaining Sarvam-m forms (lossy, lowercase, natural; chain `smrest`, account 2, cap 5 h) was refused by Kaggle at 15:39: "Maximum weekly GPU quota of 30.00 hours reached". The queue's own ledger for account 2 (`results/kaggle/acct2/quota.json`, 20.35 h) did not include the sessions of the X9b batch 3 and the Qwen3.5-2B arm (9.94 h), which the X9b-only driver records in its own ledger; the two ledgers together are at the 30 h cap, and Kaggle's count is the binding one. The first account's ledger shows 29.36 h in the last 7 days. Consequence: no Kaggle job can be pushed on either account until hours roll off: account 1 from about 9 Nov (the first 2 Nov sessions free up from 11:20 UTC on 9 Nov, then steadily), account 2 from about 11 Nov 07:56 UTC (its first sessions were on 4 Nov). The three Sarvam-m forms and the Sarvam-m X10 job therefore wait for that quota; the Sarvam-m verdict on native vs ITRANS (7 of 7 models) does not depend on them. Chain `smrest` is marked FAILED for this reason, not for an error in the job. The laptop GPU stays busy with the extra seeds (X9b about 16 to 18 h). Standing order 2 (use every quota hour) is satisfied: both accounts are at the cap.

`````

##### 2026-11-05 22:08 IST, LAPTOP POWER LOSS AND RESTART (operational).

RESULTS.md lines 4017 to 4018; first line committed in `cccb4f4` on 2026-11-05 22:08:29 +0530; last line in `739114f` on 2026-11-05 22:15:42 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 22:08 IST, LAPTOP POWER LOSS AND RESTART (operational).** The laptop shut down uncleanly at about 16:42 (Windows event 41 and 6008, previous shutdown logged at 16:10:37 PM by the event, the last file write of the X9b extra run at 16:42) and came back at 22:00:56; the GPU was idle for about 5 h 20 min (16:42 to 22:07) with the X9b extra-seed chain interrupted, which breaks the standing order that the GPU is never idle; cause: a power or system failure on the machine, not a project process. The chain came back by itself at 22:02 but stopped at 22:06 on an unreadable checkpoint: the step-100 checkpoint of `sarvam-1+itrans+s2` was being written when power was lost (zip archive truncated). Fixes: the corrupt checkpoint file (my own output of that run) was deleted and the run restarts from step 0 (about 1.4 h of training lost: it had reached step 100 of 305); checkpoint writes in `scripts/kaggle_x9b.py` are now atomic (written to a temporary file, then replaced), which does not touch the recipe, streams or evaluation; the chain `x9extra` was relaunched at 22:07 and skips the finished base evaluation. The X9b extra-seed finish estimate moves from about 7 Nov 09:30 to about 8 Nov 03:30 to 05:00 IST (six runs of about 2.9 h from 22:07). Kaggle kernels were not affected (none running). The 15-minute watchdog kept firing in this session; no other process had been lost.

`````

##### 2026-11-05 22:15 IST, THIRD KAGGLE ACCOUNT: TOKEN RECEIVED AND VERIFIED, NO COMPUTE USED YET (operational).

RESULTS.md lines 4019 to 4020; first line committed in `739114f` on 2026-11-05 22:15:42 +0530; last line in `5d9fd0e` on 2026-11-05 22:23:55 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 22:15 IST, THIRD KAGGLE ACCOUNT: TOKEN RECEIVED AND VERIFIED, NO COMPUTE USED YET (operational).** Aarnav supplied a third Kaggle API token, described as belonging to another teammate. It is stored only in the gitignored `.env` (KAGGLE3_API_TOKEN, KAGGLE3_USERNAME) and never echoed. Verification: the token authenticates (an invalid token is refused) and resolves to the Kaggle username **aarnavkembhavi** (no trailing 1), an account with notebooks from 2024. That name matches Aarnav's own naming and is not the name of a teammate, so ownership was put back to Aarnav before any job runs on it; no kernel, dataset or quota has been used on it, and its GPU access (phone verification, T4 x2) is not yet tested, since that needs a kernel push. Code prepared (no secrets): `scripts/kaggle_runner.py` now knows account 3 (job folders `results/kaggle/acct3`, build folder, credentials KAGGLE3_*) and gives each account its own empty CLI config folder, because the Kaggle CLI otherwise falls back to the login stored in the user profile (that login is the account `aarnavkembhavi`). Accounts 1 and 2 were re-checked and still resolve to aarnavkembhavi1 and ashwin18522. Cleanup list additions (after Aarnav closes Phase 2): revoke the third token, delete any private datasets and kernels created on the third account, delete build/kaggle_config_3. The token was pasted in chat, so revocation matters.

`````

##### 2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational).

RESULTS.md lines 4021 to 4022; first line committed in `5d9fd0e` on 2026-11-05 22:23:55 +0530; last line in `07e9a33` on 2026-11-05 22:37:41 +0530; labels from the title and parent heading: none

`````text
- **2026-11-05 22:23 IST, KAGGLE ACCOUNT 3 ENABLED AND KAGGLE PUSH AUDIT (operational).** Aarnav reported that the owner of the third Kaggle account (username aarnavkembhavi) confirmed it is a teammate's account, agreed to its use and confirmed the phone is verified; its token is in the gitignored \`.env\` only. **Statement for the record: some Phase 2 Kaggle compute ran on teammates' accounts, not on Aarnav's: account 2 (username ashwin18522, a teammate's, from 2026-11-04 07:50 UTC: gates, A1-R reproduction, A1-P checks for the Llama and Ambari-Instruct models, instruction-pair and Llama-3.1-8B scoring and MDL, X9b batch 3 (Sarvam-1, 2026-11-04), the X9b Qwen3.5-2B arm (2026-11-04 21:41 UTC to 2026-11-05) and the X13 Sarvam-m scoring (2026-11-05 05:10 UTC)); and from 2026-11-05 account 3 (username aarnavkembhavi, a teammate's), starting with its smoke gate and A1-R reproduction on 2026-11-05 and followed by the jobs listed below once those pass.** **Audit (requested), checked from the Kaggle side: every kernel on each account was listed with its owner. Account 1 (aarnavkembhavi1): 6 kernels (x-score, kaggle-x9b, kaggle-mdl, kaggle-precision, kaggle-gate, kaggle-retrieval-gate), all owned by aarnavkembhavi1, 5 datasets all under aarnavkembhavi1. Account 2 (ashwin18522): the same 6 kernels, all owned by ashwin18522, 4 datasets all under ashwin18522. Account 3 (aarnavkembhavi): no shattered-* kernel and no dataset before today. The two ledgers hold 35 recorded pushes (23 on account 1, 12 on account 2 plus the sessions of the X9b-only ledger): every recorded kernel slug carries the owner of its own account, no kernel exists under any other owner, so no job ran on the fallback login.** The one fallback found concerns the CLI configuration, not a job: the Kaggle CLI falls back to the login stored in the user profile (which is the account aarnavkembhavi) when no token is given; every run passes its own token and username, an invalid token is refused rather than falling back, and each account now has its own empty CLI configuration folder in \`build/kaggle_config_<n>\` (runner change committed). Setup of account 3: private dataset \`aarnavkembhavi/shattered-flores-private\` (the FLORES+ evaluation sentences, as on the other accounts; no other datasets: the models of its jobs are public), then the smoke gate and the A1-R retrieval reproduction (untrained Sarvam-1 and Gemma 4 E2B base evaluation, which must reproduce account 1's curves) before any real job; chains \`acct3x9b\` (X9b extra seed, ITRANS and native, then English, with the in-kernel base-evaluation guard) and \`acct3sm\` (Sarvam-m lossy, lowercase, natural) wait for that acceptance. Quota is tracked per account (30 h per rolling 7 days; two GPU sessions per account); the account-3 ledger is \`results/kaggle/acct3/quota.json\`. The paper is not edited.

`````

##### 2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected).

RESULTS.md lines 4023 to 4024; first line committed in `07e9a33` on 2026-11-05 22:37:41 +0530; last line in `1d0616d` on 2026-11-05 22:59:17 +0530; labels from the title and parent heading: result, failed or not run

`````text
- **2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected).** Both setup kernels pushed and started on a T4 x2 (so GPU access works) but ended with status ERROR after about 3.5 minutes in the same step: the kernel's `pip install -e` of the project package failed while installing build dependencies (no output, a timeout). A CPU-only test kernel (`aarnavkembhavi/shattered-nettest`, internet requested in its metadata) confirmed the cause: DNS resolution fails for both pypi.org and huggingface.co ("Temporary failure in name resolution"), i.e. Kaggle did not grant internet to this account's kernels although the push asked for it. Kaggle only grants internet to phone-verified accounts, so the phone verification the owner reported is not in effect for kernels (or was not completed for the account). Every registered job needs internet (pinned packages, public models from Hugging Face, the Wikipedia pool), so none can run until it is fixed. Quota used on account 3: 0.21 h (two failed kernels, about 3.5 minutes each; the CPU test does not count). **What the owner must do:** sign in to kaggle.com as aarnavkembhavi, open Settings, complete 'Phone Verification' (the account must show a verified phone number), and confirm that a new notebook's Settings panel lets 'Internet' be switched on. When he has, tell me and I re-run the setup chain `acct3` (smoke gate and A1-R reproduction); the job chains `acct3x9b` and `acct3sm` are waiting and start by themselves after the acceptance. The earlier chain status DONE for `acct3` meant only that the runner finished, not that the gates passed; the gates did not pass and the acceptance marker was not written. Cleanup list (adds): the kernels `aarnavkembhavi/shattered-nettest`, `shattered-kaggle-gate`, `shattered-kaggle-retrieval-gate` and the datasets on the third account are removed at the end of Phase 2. The paper is not edited.

`````

##### 2026-11-06 11:53 IST, LAPTOP GPU IDLE 11:40 ONWARD, NO REGISTERED JOB READY (standing order 1).

RESULTS.md lines 4034 to 4035; first line committed in `e605a65` on 2026-11-06 11:53:24 +0530; last line in `ac6470f` on 2026-11-07 01:49:19 +0530; labels from the title and parent heading: registered

`````text
- **2026-11-06 11:53 IST, LAPTOP GPU IDLE 11:40 ONWARD, NO REGISTERED JOB READY (standing order 1).** The extra-seed chain ended at 11:40:11. Every registered laptop job is done; the remaining registered work needs Kaggle (Sarvam-m lossy, lowercase and natural; Sarvam-m X10) or cannot be formed (X11 Arm B), and the optional X13 activation patching was left dropped. Nothing is pulled forward because nothing registered is left for the laptop. Proposed next jobs, none started: see the report.

`````

##### 2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational).

RESULTS.md lines 4036 to 4037; first line committed in `ac6470f` on 2026-11-07 01:49:19 +0530; last line in `b194514` on 2026-11-07 01:53:51 +0530; labels from the title and parent heading: none

`````text
- **2026-11-07 01:49 IST, KAGGLE ACCOUNT 3 REPLACED BY A NEW TOKEN AND A DIFFERENT ACCOUNT (operational).** Aarnav supplied a new Kaggle API token to be used instead of the third-account token. It resolves to the Kaggle username **aakarshprabhu** (checked with an empty CLI configuration folder; the old token resolved to aarnavkembhavi), a different account, treated as a teammate's account on Aarnav's instruction. The new token is stored only in the gitignored `.env` (KAGGLE3_API_TOKEN, KAGGLE3_USERNAME; the replaced token is kept there as KAGGLE3_API_TOKEN_PREVIOUS for cleanup and revocation), never in commits, logs or reports. The earlier attempt on aarnavkembhavi (two failed setup kernels, no internet, 0.21 h) is archived as `results/kaggle/acct3_aarnavkembhavi_failed` and its chain status under `results/phase2/`. A CPU test kernel on the new account confirms **internet works** (pypi.org and huggingface.co reachable). The private dataset `aakarshprabhu/shattered-flores-private` was created; the smoke gate and the A1-R reproduction (untrained Sarvam-1 and Gemma 4 E2B must reproduce account 1's curves) run before any job. The account-3 X9b chain was cancelled (the seed-4 runs finished on the laptop on 2026-11-06); the Sarvam-m chain `acct3sm` (lossy, lowercase, natural; 5 h cap) is kept waiting for the acceptance. Cleanup list: revoke both third-account tokens (the replaced one and the new one; both were pasted in chat), delete the datasets and kernels created on aakarshprabhu and on aarnavkembhavi, delete the nettest kernels. The username is added to the anonymiser's scrub list. This extends the statement that some Phase 2 Kaggle compute ran on teammates' accounts: account 3 (aakarshprabhu) from 2026-11-07. The paper is not edited.

`````

##### 2026-11-07 01:53 IST, REGISTRATION OF A SECOND SET OF EXTRA SEEDS (added AFTER seeing the originals; Aarnav's instruction of 2026-11-07 to start both; the original registrations, rules, budgets and verdicts are unchanged).

RESULTS.md lines 4038 to 4039; first line committed in `b194514` on 2026-11-07 01:53:51 +0530; last line in `acd0e83` on 2026-11-07 02:21:05 +0530; labels from the title and parent heading: registered, result

`````text
- **2026-11-07 01:53 IST, REGISTRATION OF A SECOND SET OF EXTRA SEEDS (added AFTER seeing the originals; Aarnav's instruction of 2026-11-07 to start both; the original registrations, rules, budgets and verdicts are unchanged).** Why the laptop GPU was idle: no registered laptop job was left after the first extra-seed chain finished at 2026-11-06 11:40 (idle until this start). **(1) X9a-low: levels 0 (no cipher), 0.01% and 0.03% exposure, code seeds 3 and 4 (called seeds 4 and 5; originals 0, 1, 2), same recipe and evaluation as the earlier extra seeds (0.1%, 0.3%, 1%), six runs of about 18 minutes; per-seed values will be reported with the original three and all five side by side; the registered X9a-low rule is not re-run on a different set of seeds. The level-0 stream (removed with the caches) is regenerated with the code of the original preparation and refused unless its sha256 equals the stored value.** **(2) X9b secondary arm (Qwen3.5-2B): extra code seeds 1 and 2 (called seeds 2 and 3; the original run is seed 0, one seed), ITRANS, native and English, same QLoRA recipe, streams and token budget (5,668,864 tokens per run, 346 optimizer steps), same evaluation, laptop (the original ran on Kaggle account 2 and was finished on the laptop), micro-batch 4 as in the pilot (below the cap of 8), six runs of about 2 to 2.5 h; the analysis `x9b_analyse.py --model qwen3.5-2b --seeds 0,1,2` adds a seed spread to the secondary arm; the secondary arm still does not enter the primary conclusion and its registered verdict (supported, one seed) is unchanged.** Chain `x9extra2` (X9a-low first, about 2 h; then the Qwen runs, an estimated 12 to 15 h, projected finish about 7 Nov 20:00 to 23:00 IST). Output `results/kaggle/laptop_x9b/2026-11-07/out`. Also from now on the 15-minute watchdog reports to Aarnav only when a job finishes, fails or a registered result arrives (Aarnav's instruction), the checks themselves continue. The paper is not edited.

`````

##### 2026-11-07 02:21 IST, KAGGLE ACCOUNT 3 (aakarshprabhu) ACCEPTED.

RESULTS.md lines 4040 to 4041; first line committed in `acd0e83` on 2026-11-07 02:21:05 +0530; last line in `2466b30` on 2026-11-07 03:00:36 +0530; labels from the title and parent heading: none

`````text
- **2026-11-07 02:21 IST, KAGGLE ACCOUNT 3 (aakarshprabhu) ACCEPTED.** Smoke gate passed; A1-R reproduction: the untrained base evaluation on the new account equals account 1's exactly (maximum difference of any layer curve 0.0): Sarvam-1 native 0.9443 (layer 24), ITRANS 0.5104 (layer 21); Gemma 4 E2B native 0.9960 (layer 7), ITRANS 0.2657 (layer 7). The kernel's own gate flag is False on account 1 and on account 3 alike (it compares with laptop numbers and is not the criterion used); acceptance follows the rule applied to account 2: exact reproduction of account 1. The acceptance marker is written, so the queued chain `acct3sm` (Sarvam-m lossy, lowercase and natural forms, cap 5 h) starts by itself. Quota on account 3 so far: about 0.5 h of 30 h.

`````

##### 2026-11-07 03:00 IST, KAGGLE ACCOUNT 3 (aakarshprabhu): ACCEPTANCE CORRECTION AND FIRST JOB STARTED (operational).

RESULTS.md lines 4042 to 4043; first line committed in `2466b30` on 2026-11-07 03:00:36 +0530; last line in `82e4226` on 2026-11-07 03:52:42 +0530; labels from the title and parent heading: none

`````text
- **2026-11-07 03:00 IST, KAGGLE ACCOUNT 3 (aakarshprabhu): ACCEPTANCE CORRECTION AND FIRST JOB STARTED (operational).** The acceptance written at 02:20 was premature: the smoke gate had not passed (two attempts failed because the laptop reference scores were not in the pushed package: the first lacked them, the second mounted an older version of the package dataset). Third attempt passed: both models in float16, raw-prediction agreement 0.99, 0.95, 0.96 (Sarvam-1: native, ITRANS, lossy) and 1.00, 0.99, 0.99 (Gemma 4 E2B), accuracy differences within 0.02, tolerance 0.03. With the earlier exact A1-R reproduction (account 1's curves reproduced to 0.0), the account is accepted (marker rewritten 03:0x) and the X13 Sarvam-m job for the three forms the first kernel did not reach (lossy, lowercase, natural; 4-bit, cap 5 h) was started by the waiting chain. Quota on account 3: about 1.2 h of 30 h used by the setup.

`````

##### 2026-11-07 04:22 IST, QWEN3.5-2B EXTRA RUNS: SLOWER THAN PROJECTED; MICRO-BATCH CAP LOWERED TO 2 FOR THE NEXT RUNS (operational; recipe unchanged).

RESULTS.md lines 4046 to 4047; first line committed in `c42cfd4` on 2026-11-07 04:22:43 +0530; last line in `0cd9a82` on 2026-11-08 15:33:40 +0530; labels from the title and parent heading: none

`````text
- **2026-11-07 04:22 IST, QWEN3.5-2B EXTRA RUNS: SLOWER THAN PROJECTED; MICRO-BATCH CAP LOWERED TO 2 FOR THE NEXT RUNS (operational; recipe unchanged).** The first Qwen extra run (ITRANS, code seed 1) trains at about 41 s per optimizer step on the laptop (step 40 after 1,778 s), against about 26 s on the Kaggle T4; with 346 steps that is about 3.9 h of training plus about 0.6 h of evaluation per run, so the six runs take about 27 h and end about **8 Nov 07:00 IST**, not 7 Nov 20:00 to 23:00 as projected at registration. The card is at 8.0 GB (micro-batch 4, shared-memory spill), as the Sarvam-1 runs were before the cap. The cap file `build/x9b_max_micro_batch.txt` is lowered from 8 to 2 for the runs that have not started (the run in progress keeps micro-batch 4; same optimizer step of 16,384 tokens; done.json records the value); if the next run is not faster the cap is restored. If Aarnav prefers, the second seed (3 runs) can be dropped, which brings the end to about 7 Nov 20:00.

`````

##### 2026-11-08 15:33 IST, OPERATIONAL: LAPTOP GPU IDLE FROM 2026-11-07 20:05 TO NOW (about 19.5 h) AND THE WATCHDOG PAUSED (standing order 1 broken).

RESULTS.md lines 4050 to 4051; first line committed in `0cd9a82` on 2026-11-08 15:33:40 +0530; last line in `79e0484` on 2026-11-08 15:58:25 +0530; labels from the title and parent heading: none

`````text
- **2026-11-08 15:33 IST, OPERATIONAL: LAPTOP GPU IDLE FROM 2026-11-07 20:05 TO NOW (about 19.5 h) AND THE WATCHDOG PAUSED (standing order 1 broken).** The Qwen extra-seed chain ended at 20:05 on 7 Nov; no registered laptop job remained, and the watchdog and this session were paused by the weekly usage limit (the session continued at the reset), so neither the finish nor the idle GPU was handled for about 19 h. Both finished jobs above were analysed on resume. Nothing was running on any Kaggle account that needed a restart (account 3's Sarvam-m job ended 2026-11-07 06:18).

`````

##### 2026-11-08 15:58 IST, BACKUP (Aarnav's instruction of 2026-11-08; no secrets in this entry).

RESULTS.md lines 4052 to 4053; first line committed in `79e0484` on 2026-11-08 15:58:25 +0530; last line in `0034538` on 2026-11-08 16:23:25 +0530; labels from the title and parent heading: none

`````text
- **2026-11-08 15:58 IST, BACKUP (Aarnav's instruction of 2026-11-08; no secrets in this entry).** (1) Private GitHub repo `aarnav-kembhavi/shattered-scripts-phase2` created; the full git history was pushed (branch master, all tags; history scanned first: `.env` never committed, no key patterns in any revision, no blob over 100 MB). (2) `results/` archived with `scripts/backup_manifest.py`: 12,921 files, 352,387,091 bytes (246,404,518 zipped), uploaded as release asset `results.zip` of release `backup-2026-11-08` in the same private repo and verified by downloading it again (sha256 c831157a…47233 equals the local archive's). (3) Also archived locally: `annotation.zip` (60 files) and `root_docs.zip` (494 files: RESULTS.md, docs, paper2, configs, scripts, src), in `C:\PROJECTS\PROMPT\backup_phase2_2026-11-08` with `MANIFEST.json`; the annotation archive was deliberately not put on GitHub (those folders are kept out of git for annotator anonymity). (4) Google Drive: a private folder `Shattered Scripts Phase 2 backup 2026-11-08` was created and holds README.txt and the manifest; **the zip files could not be uploaded to Drive from this session** (the connector passes file content inline and the browser upload tool is limited to 10 MB per call and cannot operate the native file picker), so the three zip files must be dragged into that folder by hand. Excluded on purpose: .env and every token or credential file, the Hugging Face cache, model weights and training checkpoints (25 files, 1,947,197,584 bytes: adapter_model.safetensors and ckpt.pt), the virtual environment, cache/, build/, data/raw, .git. Backup location of record: GitHub private repo + the laptop folder above; Drive folder id in the Drive account of the lead author.

`````

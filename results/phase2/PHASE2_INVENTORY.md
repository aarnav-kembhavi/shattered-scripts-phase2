# Phase 2 completion inventory

Written 2026-11-05 10:50 IST (system clock). Source: RESULTS.md (append-only log) and `results/phase2/REGISTERED_OUTCOMES.md`; where those two disagree on a row's status, this file is the current reading (the ledger keeps its older rows and appends corrections).
Machines: **L** = laptop (RTX 3070 8 GB, CPU), **K1** = Kaggle account 1 (Aarnav), **K2** = Kaggle account 2 (teammate), **API** = hosted API (Gemini or Groq). Verdict words are the registered ones.

## Done

| Experiment | Verdict / result (one line) | Ran on |
|---|---|---|
| A1-R, A1-P (checks) | A1-R passed on both accounts (identical numbers); A1-P passed for Qwen3-8B, Ambari-7B-base, Llama-2-7B, Llama-3.1-8B, Ambari-Instruct v0.1 and v0.2 | K1, K2 |
| X1 T2, T3 (second and third prompt templates) | T2 analysed; T3 exploratory (verbatim P-a reads "refuted" through Qwen2.5-1.5B; four counted models 8 of 8 supported) | L |
| X2 (measured romanized exposure, Source A) | **supported** (Hindi 0.437% vs Kannada 0.045%); deviation X2-D1 (Poisson interval) | L (network) |
| X3 (frequency-matched non-canonical tokenization) | **unresolved** (all three measures) | L |
| X4 (Bengali, Telugu): R1, R2, R3, ladder, E9 schemes | R1, R2, R3 **supported** both languages; ladder L1 no effect, L2 positive, L3 positive (retrieval both; SIB-200 Bengali only) | L |
| X4 R4 (MDL layer) | main analysis (Qwen2.5-1.5B not counted): **Bengali supported, Telugu uninformative** (two qualifying models); including Qwen2.5-1.5B both supported | L |
| X4 K3b-bn | **refuted** (against the prediction): vowel doubling ratio 0.144; h-digraph and English share match | API, L |
| X6 (new models) | screened and run for counting: **neither model counted** (Llama-3.2-1B native CI [0.381, 0.443]; oroZ-1.7B [0.249, 0.305]); no threshold change | L |
| X7 control | **does not survive** (against the prediction); X7-A **supported**; X7b considered, not run (docs/X7B_NOTE.md) | L |
| X8 (blind second annotator) | complete; low agreement is the result (kappa 0.198, CER 0.096) | annotators, L |
| X9a, X9a-low | X9a-R **refuted** (ceiling), X9a-A **supported**; X9a-low **dose-response present** | L |
| X9b primary (Sarvam-1, 2 seeds) | **supported** on SIB-200 and retrieval | K1 (batches 1, 2), K2 (batch 3) |
| X10 (Kannada to English generation) | X10-P **supported** 4 of 4 (Qwen3.5-2B has 62 to 88% empty first lines) | L |
| X11 Arm A (4-bit control) | **partly supported** (kept as registered) | L |
| X12 contrast 1 (primary) | **supported**; contrast 2 (instruction pair, MDL) pattern **met** | K1, K2 |
| X13 Qwen3-8B, Llama-3.1-8B | both counted; extended P-a **supported** (5 of 5); retrieval all-but-one **met**; MDL pattern met for both | K1, K2 |

## Running

| Experiment | What is running | Machine | Projected finish (IST) |
|---|---|---|---|
| X9b secondary (Qwen3.5-2B, 1 seed, 3 runs) | Kaggle kernel, about 8.3 h in against a 10.2 h cap | K2 | 5 Nov about 13:00 |
| X13 Sarvam-m (23.6B, 4-bit, SIB-200 only; the largest Sarvam model that fits 2 x T4 with standard code; sarvam-30b and 105b need remote code and are excluded; no retrieval; exempt from A1-P) | Kaggle kernel pushed 10:40 (47 GB download plus 4-bit load; unmeasured, cap 5 h) | K2 | 5 Nov about 14:00 to 16:00 |
| X4 K3b-te | finished 10:52: refuted | API, L | done |
| X10 post hoc (extraction check for Qwen3.5-2B; not registered; the registered X10 verdict is unchanged) | raw generation on the laptop GPU | L | 5 Nov about 11:45 |
| X14 (hosted large models, exploratory, no verdict) | Groq rows per model 2,699 / 2,543 / 2,539 of 3,269; waits for the 12:45 daily reset | API (Groq) | 5 Nov evening to 6 Nov (about 900 rows per reset) |

## Not run yet (registered, still to do)

| Experiment | What is left | Machine | Plan and projected date |
|---|---|---|---|
| X5 (cross-language consistency, analysis only) | inputs now exist (X2 and X4 done; Kannada and Hindi from Phase 1 and the Hindi replication); the pairing script is not built | L (CPU) | build and run 5 Nov |
| X13 Sarvam-m: X10 (4-bit models run SIB-200 and X10) | no Kaggle X10 job exists; 24B 4-bit generation of 1,012 sentences per form is slow and its time is unmeasured; pilot first | K1 (idle) | build the job and pilot 5 to 6 Nov; if the pilot's estimate exceeds the quota, report and cut |
| X13 activation patching on one 7 to 9B model | registered as optional (only if it fits one 12 h session); not built | K1 or K2 | decision needed: leave dropped unless time allows |
| X11 Arm B (one 4B-class model, descriptive, no verdict) | no 4B-class model was shortlisted by X6, so it cannot be formed | none | not run |

## Not run (by decision or impossibility)

| Experiment | Reason |
|---|---|
| X7b | considered and not run (embedding rank argument; Aarnav's decision) |
| X15 (human intelligibility baseline) | annotators unavailable; skipped by decision |

## End-of-Phase-2 housekeeping (after Aarnav says Phase 2 is closed)

Delete the private Kaggle datasets (account 1: shattered-flores-private, shattered-llama-2-7b-hf, shattered-llama-3-1-8b, shattered-ambari-instruct-v0-1; account 2: the same names, minus Llama-2, plus shattered-pkg), delete the kernels on both accounts, revoke the shared Kaggle token, log each deletion. Phase 2 results enter the paper only when Aarnav says so; the paper has not been edited.

## Machine load now

Laptop GPU: X10 post hoc (about 1 h); then nothing registered is ready on it except what X5 and any X13 follow-up produce. K1: idle (X10 for Sarvam-m is the only registered job that could use it). K2: X9b secondary and X13 Sarvam-m.

# Phase 2 registered outcomes: annotation-dependent items

Status ledger (created 2026-11-03 00:04 IST from the system clock). Updated 2026-11-03 01:16 IST (T3, X8 and X15 are no longer parked). Rows for the other Phase 2 experiments are added when each one reports its registered verdict word; none of the registered rules below or elsewhere is changed.

| Experiment | Registered outcome words | Status | Reason / next step |
|---|---|---|---|
| X1 T3 (Kannada instruction line) | exploratory, no registered claim | **verified; queued after X9a; not yet run** | the native speaker marked T3-1 and T3-3 Correct and replaced T3-2 (XNLI); template frozen (e0_xnli_v3.txt, sha256 prefix 6b8a23ef487ab848); every T3 result is labelled "instruction verified by a native speaker, exploratory" |
| X15 (human intelligibility baseline) | supported / refuted / inconclusive (X15-P) | **registered design (8 files, 8 different people, none from the X8 groups); not run, awaiting files** | unprotected workbooks sent; if fewer than eight files come back, the number is logged as a deviation before any analysis (`scripts/analyze_x15.py` refuses otherwise) |
| X8 (blind second-annotator sample) | K4 agreement (kappa, character error rate) reported as the result, no threshold | **registered design (P and Q, different groups of speakers, no overlap); not run, awaiting files** | runs as registered when the files return (`scripts/import_x8.py`, `scripts/analyze_x8.py`) |

# Phase 2 registered outcomes: annotation-dependent items

Status ledger (created 2026-11-03 00:04 IST from the system clock). Updated 2026-11-03 01:16 IST (T3, X8 and X15 are no longer parked). Rows for the other Phase 2 experiments are added when each one reports its registered verdict word; none of the registered rules below or elsewhere is changed.

| Experiment | Registered outcome words | Status | Reason / next step |
|---|---|---|---|
| X1 T3 (Kannada instruction line) | exploratory, no registered claim | **verified and imported; queued after X9a; not yet run** | T3-1 and T3-3 Correct; T3-2 replaced by the native speaker's wording; template frozen (e0_xnli_v3.txt, sha256 prefix 6b8a23ef487ab848); every T3 result is labelled "instruction verified by a native speaker, exploratory" |
| X15 (human intelligibility baseline) | supported / refuted / inconclusive (X15-P) | **not run (annotators unavailable)** | skipped by decision (2026-11-03 01:37 IST); no X15 files are built; the earlier workbooks, importer and analysis scripts stay in the repository unused |
| X8 (blind second-annotator sample) | K4 agreement (kappa, character error rate) reported as the result, no threshold | **partly returned: X8_Q imported (100 answers, valid); X8_P not yet returned; analysis not run** | the registered analysis needs both files (\`scripts/import_x8.py\`, \`scripts/analyze_x8.py\`) |

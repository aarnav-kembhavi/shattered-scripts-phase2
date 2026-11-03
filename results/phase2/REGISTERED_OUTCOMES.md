# Phase 2 registered outcomes: status ledger

Last updated 2026-11-04 01:50 IST (system clock). Rows for other experiments are added when each reports its registered verdict word; no registered rule is changed.

| Experiment | Registered outcome words | Status | Result or reason |
|---|---|---|---|
| X7 control (factorized embedding) | survives / does not survive / inconclusive | **complete: does not survive** (against the prediction) | Spearman -0.37; 256 minus 4096 BPB = -0.051 (reversed); embedding parameters were not equal (deviation X7-D1); V=4096 had the fewest embedding parameters in the control (107,030 vs 157,850); report in the paper |
| X7-A (assembly layer on the 18 X7 runs; exploratory) | supported / refuted / inconclusive | **registered 2026-11-04 (tag `phase2-x7a`), running** | exploratory because added after the X7 BPB result |
| X7b (equal ACTUAL embedding parameters) | n/a | **considered, not run** | with equal parameters the embedding rank is 114 at V=256 and 24 at V=4096, so the BPB rule would measure the bottleneck, not fragmentation (see `docs/X7B_NOTE.md`) |
| X9a (familiarity manipulated, fragmentation fixed) | X9a-R, X9a-A, joint reading | **complete: R refuted (against the prediction), A supported** | retrieval at ceiling (0.99 to 1.00) from 1 percent exposure; level 0 above chance (0.028); joint reading as registered: no familiarity effect in this setting; see RESULTS.md |
| X9b (QLoRA, Sarvam-1 primary) | supported / partly / refuted / inconclusive per measure | **4 of 6 Sarvam-1 runs done; analysis needs all six** | batch 3 fits from about 9 Nov 19:42 IST |
| X13 Qwen3-8B | extended P-a, retrieval all-but-one | **complete: extended P-a supported (5 of 5, both contrasts); retrieval all-but-one met (4 of 4)** | nothing against a prediction |
| X8 (blind second-annotator sample) | K4 agreement reported as the result, no threshold | **complete** | kappa 0.198, CER 0.096: low agreement is the result; registered P = X8_P_v2 (sha256 3084ca8c...), earlier P excluded |
| X1 T3 (Kannada instruction line) | exploratory | **verified; queued after X7-A** | labelled "instruction verified by a native speaker, exploratory" |
| X15 (human intelligibility baseline) | supported / refuted / inconclusive | **not run (annotators unavailable)** | skipped by decision; no X15 files are built |

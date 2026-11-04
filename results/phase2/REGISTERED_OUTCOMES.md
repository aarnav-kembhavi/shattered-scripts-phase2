# Phase 2 registered outcomes: status ledger

Last updated 2026-11-05 02:23 IST (system clock). Rows for other experiments are added when each reports its registered verdict word; no registered rule is changed.

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
| X12 contrast 1 (Llama-2-7B vs Ambari-7B-base) | supported / partly / refuted / inconclusive | **complete: supported (both measures)** | SIB DiD +0.423 [0.380, 0.466]; retrieval DiD +0.624 [0.584, 0.664] (97.5% intervals); native gain confounds exposure with the tokenizer extension; X9b is the causal test; nothing against a prediction |
| X11 Arm A (4-bit control, Qwen3.5-2B) | supported / partly / refuted | **complete: partly supported** | every form within 3 points; gap change -0.026, 95% CI [-0.054, +0.003] just outside the +-5 point bound; English -0.020 (only significant form change); exploratory control |
| X10 (Kannada to English generation, chrF) | supported / partly / refuted | **complete: X10-P supported (4 of 4)** | native beats ITRANS by +15.0 to +32.9 chrF (Holm-significant) in all four models; caveat: Qwen3.5-2B returns an empty first line for 62-88% of inputs; nothing against a prediction |
| X9a-low (exposure 0.01 to 0.3 percent; exploratory, added after the X9a-R ceiling) | dose-response present / no dose-response | **complete: dose-response present** | Spearman 1.00 over six levels, mean(1%) minus mean(0.01%) = +0.951; retrieval 0.028 / 0.043 / 0.068 / 0.109 / 0.355 / 0.993; assembly layer flat (1.33) from 0.03%; level-0 retrieval on stripped text 0.009 (chance 0.004); X9a-R verdict unchanged |
| X4 Bengali and Telugu, part 1 (counting rule and R1 on SIB-200) | supported / refuted per rule | **R1 supported in both languages (4 of 4 counted models, both contrasts)** | ITRANS-ladder, retrieval, MDL and K3b parts not built yet; nothing against a prediction |

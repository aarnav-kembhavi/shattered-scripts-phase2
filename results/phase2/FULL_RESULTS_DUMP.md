# Full results dump (Phase 1 and Phase 2)

Generated 2026-11-08 by `scripts/full_results_dump.py`, read-only. Every number is copied from RESULTS.md (verbatim entries with the commit and date of the first line, from `git blame`), from the files under `results/` and from the paper tables; nothing is
rounded, shortened, interpreted or recomputed. The only labels are keywords found in each entry's own title. Registered rules and verdicts are in the verbatim entries.
Not dumped, by rule (listed by path and size at the end of each file): CSV files with more than 2,000 data rows, JSON files above 600,000 bytes, and binary or per-item files (parquet, npy, npz, adapters, checkpoints).

Each experiment file has: the table of its RESULTS.md entries (labels, commit, date, lines, title); the models, languages, forms, tasks and seeds found in its result files; the entries verbatim; every result file with its path and first commit; the not-dumped list.

## Index (Phase 1, then Phase 2, then cross-cutting lists)

| phase | id | name | file | lines in file | RESULTS.md entries |
|---|---|---|---|---|---|
| 1 | E1 | Token cost atlas | `results/phase2/dump/P1_E1.md` | 2267 | 2 |
| 1 | E2 | Transliteration round trip and lossy scheme | `results/phase2/dump/P1_E2.md` | 422 | 2 |
| 1 | E5 | Controlled pretraining of tiny GPTs | `results/phase2/dump/P1_E5.md` | 10845 | 5 |
| 1 | E9 | Tokenizer-optimal reversible romanization | `results/phase2/dump/P1_E9.md` | 1929 | 1 |
| 1 | E0 | Gate, tokens per word, natural romanization checks, Step 0 | `results/phase2/dump/P1_E0.md` | 2679 | 5 |
| 1 | M1 | Detokenization layer (M1) on pretrained models | `results/phase2/dump/P1_M1.md` | 1455 | 5 |
| 1 | S3 | Step 3 and 3b: word-identity, MDL and erasure probes on the E5 tiny models | `results/phase2/dump/P1_S3.md` | 1891 | 3 |
| 1 | M4 | M4, M4b, M4c: retrieval, mapping, surface baseline, natural romanization | `results/phase2/dump/P1_M4.md` | 1132 | 12 |
| 1 | E0b | Familiarity test (sentiment, XNLI) | `results/phase2/dump/P1_E0b.md` | 6165 | 3 |
| 1 | E0c | SIB-200 topic classification | `results/phase2/dump/P1_E0c.md` | 998 | 2 |
| 1 | BT | Back-translation comprehension gap (large model) | `results/phase2/dump/P1_BT.md` | 94 | 3 |
| 1 | L | Romanization ladder L1 to L3 | `results/phase2/dump/P1_L.md` | 839 | 5 |
| 1 | NC | NC1: non-canonical tokenization of lossy text | `results/phase2/dump/P1_NC.md` | 1037 | 8 |
| 1 | K | Kanglish, annotation, K1 to K3, K3b, natural+dbl, V-VER, K2b | `results/phase2/dump/P1_K.md` | 4056 | 43 |
| 1 | H | Hindi: H-Hindi, H1, H1-LF, K3b-hi, English-loan measures | `results/phase2/dump/P1_H.md` | 7446 | 20 |
| 1 | EP | Activation patching E-P1, E-P2, EP-R | `results/phase2/dump/P1_EP.md` | 40326 | 9 |
| 1 | OTHER | Entries not matched to an experiment id | `results/phase2/dump/P1_OTHER_ENTRIES.md` | 519 | 20 |
| 1 | FILES | Other files at the top of results/ (OVERNIGHT.md, logs, markers) | `results/phase2/dump/P1_OTHER_FILES.md` | 15 | 0 |
| 2 | X1 | Second prompt template (T2) and Kannada instruction (T3) | `results/phase2/dump/P2_X1.md` | 3722 | 11 |
| 2 | X2 | Measured romanized exposure | `results/phase2/dump/P2_X2.md` | 186 | 6 |
| 2 | X3 | Frequency-matched non-canonical tokenization | `results/phase2/dump/P2_X3.md` | 777 | 2 |
| 2 | X4 | Bengali and Telugu replication, K3b-bn, K3b-te | `results/phase2/dump/P2_X4.md` | 7688 | 26 |
| 2 | X5 | Cross-language consistency | `results/phase2/dump/P2_X5.md` | 193 | 5 |
| 2 | X6 | New models screen and counting | `results/phase2/dump/P2_X6.md` | 1880 | 7 |
| 2 | X7 | Tiny-GPT embedding accounting, factorized control, X7-A, X7b | `results/phase2/dump/P2_X7.md` | 1091 | 6 |
| 2 | X8 | Blind second-annotator sample | `results/phase2/dump/P2_X8.md` | 791 | 7 |
| 2 | X9a | Tiny GPT, familiarity manipulated, fragmentation fixed; X9a-low and extra seeds | `results/phase2/dump/P2_X9a.md` | 2481 | 17 |
| 2 | X9b | QLoRA continued pretraining (Sarvam-1 primary, Qwen3.5-2B secondary), extra seeds | `results/phase2/dump/P2_X9b.md` | 1874 | 45 |
| 2 | X10 | Generation FLORES+ devtest to English (and post hoc, Sarvam-m) | `results/phase2/dump/P2_X10.md` | 1638 | 14 |
| 2 | X11 | Quantization control | `results/phase2/dump/P2_X11.md` | 189 | 8 |
| 2 | X12 | Ambari natural experiment | `results/phase2/dump/P2_X12.md` | 447 | 16 |
| 2 | X13 | 7 to 9B and Sarvam-m models | `results/phase2/dump/P2_X13.md` | 960 | 22 |
| 2 | X14 | Black-box hosted models | `results/phase2/dump/P2_X14.md` | 415 | 6 |
| 2 | X15 | Human intelligibility baseline | `results/phase2/dump/P2_X15.md` | 165 | 8 |
| 2 | A | General rules A0, Kaggle precision and retrieval checks A1-P and A1-R, reproducibility gate | `results/phase2/dump/P2_A.md` | 578 | 50 |
| 2 | OTHER | Entries not matched to an experiment id | `results/phase2/dump/P2_OTHER_ENTRIES.md` | 194 | 17 |
| 2 | KAGGLE | Kaggle and laptop run outputs (results/kaggle) | `results/phase2/dump/P2_KAGGLE_RUNS.md` | 8252 | 0 |
| 2 | FILES | Other files in results/phase2 (ledgers, model sizes, claims table, inventory) | `results/phase2/dump/P2_OTHER_FILES.md` | 122 | 0 |
| all | LIST | Deviations, amendments, protocol changes (all phases) | `results/phase2/dump/LIST_DEVIATIONS.md` | 717 | 38 |
| all | LIST | Failed, dropped, not run (all phases) | `results/phase2/dump/LIST_FAILED_DROPPED_NOT_RUN.md` | 596 | 56 |
| all | LIST | Chain status files (running, waiting, done, failed) | `results/phase2/dump/LIST_RUNNING_AND_CHAIN_STATUS.md` | 224 | 0 |
| all | LIST | Paper tables | `results/phase2/dump/PAPER_TABLES.md` | 182 | 0 |
| all | LIST | RESULTS.md ledger in file order (every entry once) | `results/phase2/dump/RESULTS_MD_LEDGER.md` | 6199 | 306 |

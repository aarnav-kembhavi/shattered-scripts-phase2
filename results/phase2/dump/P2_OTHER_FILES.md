# Phase 2: other result files in results/phase2 (outside the experiment folders)

#### `results/phase2/CHAIN_STATUS_ACCT3_aarnavkembhavi_attempt.md` (168 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
# Account 3 setup chain status

- state: **DONE**
- heartbeat: 2026-11-05 22:34:55 IST
- detail: Account 3 setup finished at 2026-11-05 22:34:55 IST
- pid: 2031 (bash)
`````

#### `results/phase2/CHAIN_STATUS_ACCT3_first_gate.md` (168 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
# Account 3 setup chain status

- state: **DONE**
- heartbeat: 2026-11-07 02:20:30 IST
- detail: Account 3 setup finished at 2026-11-07 02:20:30 IST
- pid: 2082 (bash)
`````

#### `results/phase2/CHAIN_STATUS_ACCT3SM_failed_gate.md` (625 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
# Account 3 Sarvam-m chain status

- state: **FAILED**
- heartbeat: 2026-11-07 02:24:06 IST
- detail: x_score exited 1 at 2026-11-07 02:24:06; see results/phase2/acct3_smrest.log
- pid: 945 (bash)

```
=== 2026-11-07 02:22:06 account 3 Sarvam-m lossy/lower/natural: .venv/Scripts/python.exe -u scripts/kaggle_runner.py run x_score --timeout-h 5.0 --private-data shattered-flores-private --include results/e09_romanize/best_schemes.json -- --models sarvam-m --no-retrieval --quant 4bit --forms lossy lower natural
reproducibility gate has not passed: no remote result counts (results/kaggle/kaggle_gate/gate_passed.json)

```
`````

#### `results/phase2/CHAIN_STATUS_ACCT3X9B_cancelled.md` (153 bytes; first commit 0cd9a82 2026-11-08 15:33:40 +0530)

`````text
# Account 3 X9b chain status

- state: **WAITING**
- heartbeat: 2026-11-07 01:46:05 IST
- detail: waiting for the account-3 acceptance
- pid: 952 (bash)
`````

#### `results/phase2/CLEANUP_LIST.md` (1,790 bytes; first commit f05ca34 2026-11-08 16:24:21 +0530)

`````text
# Phase 2 cleanup list (nothing is deleted until Aarnav says so)

Written 2026-11-08. Delete only after Phase 2 is closed; log every deletion in RESULTS.md.

## Kaggle (private datasets and kernels; all private)
- Account 1 (aarnavkembhavi1): datasets shattered-pkg, shattered-flores-private, shattered-ambari-instruct-v0-1, shattered-llama-3-1-8b, shattered-llama-2-7b-hf; kernels shattered-x-score, shattered-kaggle-x9b, shattered-kaggle-mdl, shattered-kaggle-precision, shattered-kaggle-gate, shattered-kaggle-retrieval-gate.
- Account 2 (a teammate's): datasets shattered-pkg, shattered-flores-private, shattered-ambari-instruct-v0-1, shattered-llama-3-1-8b; the same six kernels.
- Account 3 (a teammate's, current): datasets shattered-pkg, shattered-flores-private, shattered-x10-inputs; kernels shattered-kaggle-gate, shattered-kaggle-retrieval-gate, shattered-x-score, shattered-kaggle-x10, shattered-nettest.
- Earlier third-account attempt (a different teammate login, no internet): dataset shattered-flores-private and shattered-pkg; kernels shattered-kaggle-gate, shattered-kaggle-retrieval-gate, shattered-nettest.

## Tokens to revoke (the first two and the third were pasted in chat)
- Account 2's Kaggle token (KAGGLE2_API_TOKEN).
- The first third-account token (KAGGLE3_API_TOKEN_PREVIOUS) and the current one (KAGGLE3_API_TOKEN).
- Remove the lines from `.env` after revocation; delete `build/kaggle_config_*`.

## Other
- Keep: GitHub private repo and its backup release, the Drive folder (README and manifest; the zip files are still to be dragged in), the local backup folder C:\PROJECTS\PROMPT\backup_phase2_2026-11-08.
- Local: Hugging Face cache and model weights are not backed up and are not part of the project record; `cache/llm_cache.sqlite` is never deleted.
`````

#### `results/phase2/model_sizes.json` (2,281 bytes; first commit 57310bf 2026-11-02 01:40:58 +0530)

`````text
provenance.config.source = "safetensors headers of the local HF snapshots"
provenance.git_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44-dirty"
provenance.phase2_registration_commit = "a57fe610c6ea8b4f9d6484843950fa745d2d8e44"
provenance.timestamp_utc = "2026-11-01T20:06:29+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/model_sizes.py"]
models.Qwen2.5-1.5B.repo = "Qwen/Qwen2.5-1.5B-Instruct"
models.Qwen2.5-1.5B.files = 1
models.Qwen2.5-1.5B.total = 1543714304
models.Qwen2.5-1.5B.vision_tower = 0
models.Qwen2.5-1.5B.audio_tower = 0
models.Qwen2.5-1.5B.per_layer_embedding_table = 0
models.Qwen2.5-1.5B.effective_text = 1543714304
models.Qwen2.5-1.5B.total_b = 1.544
models.Qwen2.5-1.5B.vision_tower_b = 0.0
models.Qwen2.5-1.5B.audio_tower_b = 0.0
models.Qwen2.5-1.5B.per_layer_embedding_table_b = 0.0
models.Qwen2.5-1.5B.effective_text_b = 1.544
models.Qwen3-1.7B.repo = "Qwen/Qwen3-1.7B"
models.Qwen3-1.7B.files = 2
models.Qwen3-1.7B.total = 2031739904
models.Qwen3-1.7B.vision_tower = 0
models.Qwen3-1.7B.audio_tower = 0
models.Qwen3-1.7B.per_layer_embedding_table = 0
models.Qwen3-1.7B.effective_text = 2031739904
models.Qwen3-1.7B.total_b = 2.032
models.Qwen3-1.7B.vision_tower_b = 0.0
models.Qwen3-1.7B.audio_tower_b = 0.0
models.Qwen3-1.7B.per_layer_embedding_table_b = 0.0
models.Qwen3-1.7B.effective_text_b = 2.032
models.Qwen3.5-2B.repo = "Qwen/Qwen3.5-2B"
models.Qwen3.5-2B.files = 1
models.Qwen3.5-2B.total = 2274069824
models.Qwen3.5-2B.vision_tower = 331416576
models.Qwen3.5-2B.audio_tower = 0
models.Qwen3.5-2B.per_layer_embedding_table = 0
models.Qwen3.5-2B.effective_text = 1942653248
models.Qwen3.5-2B.total_b = 2.274
models.Qwen3.5-2B.vision_tower_b = 0.331
models.Qwen3.5-2B.audio_tower_b = 0.0
models.Qwen3.5-2B.per_layer_embedding_table_b = 0.0
models.Qwen3.5-2B.effective_text_b = 1.943
models.Sarvam-1.repo = "sarvamai/sarvam-1"
models.Sarvam-1.files = 2
models.Sarvam-1.total = 2525087744
models.Sarvam-1.vision_tower = 0
models.Sarvam-1.audio_tower = 0
models.Sarvam-1.per_layer_embedding_table = 0
models.Sarvam-1.effective_text = 2525087744
models.Sarvam-1.total_b = 2.525
models.Sarvam-1.vision_tower_b = 0.0
models.Sarvam-1.audio_tower_b = 0.0
models.Sarvam-1.per_layer_embedding_table_b = 0.0
models.Sarvam-1.effective_text_b = 2.525
models.Gemma 4 E2B.repo = "google/gemma-4-E2B-it"
models.Gemma 4 E2B.files = 1
models.Gemma 4 E2B.total = 5123178979
models.Gemma 4 E2B.vision_tower = 168544704
models.Gemma 4 E2B.audio_tower = 307184384
models.Gemma 4 E2B.per_layer_embedding_table = 2348810240
models.Gemma 4 E2B.effective_text = 2298639651
models.Gemma 4 E2B.total_b = 5.123
models.Gemma 4 E2B.vision_tower_b = 0.169
models.Gemma 4 E2B.audio_tower_b = 0.307
models.Gemma 4 E2B.per_layer_embedding_table_b = 2.349
models.Gemma 4 E2B.effective_text_b = 2.299
`````

#### `results/phase2/PHASE2_CLAIMS_TABLE.md` (12,549 bytes; first commit 133731e 2026-11-08 16:03:37 +0530)

`````text
# Phase 2: registered experiments, claims and verdicts

Generated by `paper2/scripts/phase2_outcomes.py` from `results/phase2/` (no number typed by hand). Order: results against a prediction first.


## Against a prediction, or not as predicted

| Experiment | Claim | Registered rule | Result | Verdict | Status |
|---|---|---|---|---|---|
| X7 (control) | The bits-per-byte ordering by fragmentation survives equal embedding capacity. | Larger fragmentation costs bits per byte (256 minus 4096 above 3 SDs, 3 seeds). | 256 minus 4096 BPB -0.051 (reversed, -16.0 SD); Spearman -0.37, p 0.47; n = 18 runs | **does not survive** | complete; against the prediction |
| X9a-R | In the tiny GPT, retrieval of the cipher text follows the amount of exposure (1 to 50 percent). | Supported if means non-decreasing and mean(50) minus mean(1) above 3 SDs; refuted if mean(50) at or below mean(1) or Spearman at most 0.6. | retrieval already at the ceiling from 1 percent: means 0.993 (1%), 1.000, 0.999, 0.999 (50%); Spearman 0.32 | **refuted** | complete; against the prediction (ceiling) |
| X4 K3b-bn | Gemini romanization of Bengali matches the Dakshina native-speaker romanization. | Holds if all three statistics have ratio CI inside [0.80, 1.25] (90% CI, 500 strings). | vowel doubling 0.144 [0.095, 0.197]; h-digraph 1.053 [1.024, 1.082]; English share 1.010 [0.949, 1.075]; n = 490 | **refuted** | complete; against the prediction |
| X4 K3b-te | Gemini romanization of Telugu matches the Dakshina native-speaker romanization. | Holds if all three statistics have ratio CI inside [0.80, 1.25] (90% CI, 500 strings). | vowel doubling 0.328 [0.293, 0.366]; h-digraph 1.199 [1.111, 1.292]; English share 1.051 [0.986, 1.122]; n = 496 | **refuted** | complete; against the prediction |
| X1 T-a (second template) | Under the second prompt template, native beats ITRANS and lossy in every informative model (Phase 1 P-a wording). | Supported if every difference is positive and significant; refuted if any is significantly negative. | 9 of 10 tests positive and significant; the miss is Qwen2.5-1.5B native vs lossy (p_Holm 0.043); every-counted-model reading 8 of 8; T-b: 8 of 11 verdicts keep their Phase 1 category | **refuted** | complete (the counted-model reading is supported) |
| X1 T3 (Kannada instruction, exploratory) | The pattern survives an instruction written in Kannada script (instruction verified by a native speaker). | Exploratory, no registered claim. | 9 of 10 tests positive and significant (all informative models), 8 of 8 in the counted models | **refuted (all models); supported (counted models)** | complete; exploratory |
| X3 | Unfamiliar segmentation, or piece rarity at equal token count, explains the cost of non-canonical tokenization. | D2 (canonical minus frequency-matched) and D3 (equal-count minus matched) per measure, effect rule (all counted models but one). | D2 and D3: no detected effect on retrieval, sentiment and SIB-200 (D1, the Phase 1 contrast on matched items, positive on retrieval) | **unresolved (all three measures)** | complete |
| X11 Arm A (4-bit control) | Quantizing Qwen3.5-2B to 4 bits does not change the picture. | Supported if every form changes by at most 3 points and the CI of the gap change lies within 5 points. | gap change -0.026 [-0.054, 0.003]; every form within 3 points; English -0.020 (McNemar p 0.010, not significant after Holm) | **partly supported** | complete; exploratory control |
| X4 R4 (assembly follows fragmentation) | In Bengali and Telugu the assembly layer follows the tokens-per-word difference. | Sign rule in models with a tokens-per-word difference of at least 1; at least three qualifying models, effect in all but one. | Bengali: 3 qualifying models (supported); Telugu: 2 qualifying models without Qwen2.5-1.5B (uninformative (fewer than three qualifying models)); with Qwen2.5-1.5B (sensitivity) supported in Bengali and supported in Telugu | **Bengali supported; Telugu uninformative** | complete |
| X6 (new models) | Llama-3.2-1B and oro-1.7B add a counted tokenizer regime. | Counted only if native SIB-200 CI lower bound above 0.40. | native CI lower bound (counting rule: above 0.40): Llama-3.2-1B 0.381 (point estimate 0.412), oro-1.7B 0.249 (point estimate 0.277) | **neither model counted** | complete |
| X8 (blind second annotator) | Two independent annotators agree on how Kannada is romanized (and Gemini matches both). | Agreement reported as the result, no threshold. | kappa on doubled vowels 0.198 [0.161, 0.238]; character error rate between annotators 0.096 [0.088, 0.105]; n = 100; Gemini differs from annotator Q by 0.064 and from P by 0.107 | **low agreement (the result)** | complete |

## As predicted or exploratory

| Experiment | Claim | Registered rule | Result | Verdict | Status |
|---|---|---|---|---|---|
| X7-A (assembly layer, exploratory) | Assembly layer is later at the most fragmented vocabulary in the control runs (added after the X7 BPB result). | Supported if each seed difference (256 minus 4096) is at least 1. | mean assembly layer 2 at V=256 and 1 at V=4096; seed differences [1, 1, 1] | **supported** | complete; exploratory |
| X9a-A | Word assembly layer stays flat across exposure levels. | Supported if max minus min of the four seed-mean layers is at most 1. | max minus min 0.33 layers | **supported** | complete |
| X2 (measured exposure) | Romanized Kannada is rarer on the web than romanized Hindi. | Supported if the 95% CI of e_hi minus e_kn is above 0 (FineWeb-2, documents). | Hindi 0.437% against Kannada 0.045%; difference 0.392 points 0.389 to 0.396 | **supported** | complete |
| X5 (cross-language) | More romanized exposure goes with a smaller native-minus-natural gap across four languages. | Spearman between exposure and gap negative in all counted models but one (descriptive, no p value). | accuracy: negative in 3 of 4 models; retrieval: 3 of 3; driven mostly by Hindi | **consistent (accuracy); consistent (retrieval)** | complete; descriptive |
| X4 Bengali (R1 to R3) | The Kannada accuracy and retrieval pattern replicates in Bengali. | R1 native above ITRANS and lossy (SIB-200); R2 native above ITRANS (retrieval); R3 natural above ITRANS (M4c); effect in all counted models but one. | R1 4 of 4 models (ITRANS) and 4 of 4 (lossy); R2 3 of 3; R3 3 of 3 (n = 476 ids) | **R1 supported; R2 supported; R3 supported** | complete |
| X4 Telugu (R1 to R3) | The Kannada accuracy and retrieval pattern replicates in Telugu. | R1 native above ITRANS and lossy (SIB-200); R2 native above ITRANS (retrieval); R3 natural above ITRANS (M4c); effect in all counted models but one. | R1 4 of 4 models (ITRANS) and 4 of 4 (lossy); R2 3 of 3; R3 3 of 3 (n = 487 ids) | **R1 supported; R2 supported; R3 supported** | complete |
| X9a-low (exploratory, added after the X9a-R ceiling) | Retrieval rises with exposure between 0.01 and 1 percent. | Dose-response present if Spearman at least 0.8 and mean(1%) minus mean(0.01%) at least 0.05. | Spearman 1.00; mean(1%) minus mean(0.01%) +0.951; means 0.028, 0.043, 0.068, 0.109, 0.355, 0.993 (levels 0, 0.01, 0.03, 0.1, 0.3, 1 percent, 3 seeds); extra seeds 4 and 5 added after seeing these (appendix) | **dose-response present** | complete; exploratory; extra seeds added later |
| X9b primary (Sarvam-1, original two seeds) | Training on ITRANS Kannada at a fixed tokenizer shrinks the native-minus-ITRANS gap more than training on native Kannada or English. | D_N and D_E (97.5% intervals, one seed drawn per cell): supported if both above 0. | SIB-200 D_N +0.225 [0.177, 0.273], D_E +0.196 [0.150, 0.244]; retrieval D_N +0.337 [0.296, 0.378], D_E +0.391 [0.344, 0.435] | **supported (SIB-200); supported (retrieval)** | complete (registered; two seeds) |
| X9b primary (Sarvam-1, all four seeds) | Same claim with the two extra seeds added after seeing seeds 1 and 2. | Same rule and code; all four seeds together (original two shown separately above). | SIB-200 D_N +0.222 [0.174, 0.270], D_E +0.194 [0.147, 0.243]; retrieval D_N +0.339 [0.292, 0.386], D_E +0.405 [0.353, 0.457] | **supported (SIB-200); supported (retrieval)** | complete; seeds 3 and 4 added after seeing the originals |
| X9b secondary (Qwen3.5-2B) | Same claim in a second model (secondary arm; does not enter the primary conclusion). | Same rule; one seed (registered), three seeds (added after seeing the first). | one seed: SIB-200 D_N +0.285 [0.241, 0.328], D_E +0.260 [0.219, 0.301], retrieval D_N +0.583 [0.545, 0.620], D_E +0.566 [0.529, 0.603]; three seeds: SIB-200 D_N +0.301 [0.248, 0.351], D_E +0.258 [0.195, 0.315], retrieval D_N +0.594 [0.550, 0.637], D_E +0.592 [0.544, 0.638] | **supported (both measures; one seed and three seeds)** | complete; secondary; seeds 2 and 3 added later |
| X10 (generation) | Kannada-to-English generation is better from native script than from ITRANS. | X10-P supported if native beats ITRANS (Holm-significant) in at least 3 of 4 models. | native minus ITRANS chrF +26.4, +15.0, +21.0, +32.9 (4 models, n = 1012); Qwen3.5-2B mostly writes a reasoning preamble (post hoc check, registered verdict unchanged) | **supported (4 of 4)** | complete |
| X12 contrast 1 (Ambari natural experiment) | Continued native-script Kannada pretraining transfers more to native than to ITRANS (Llama-2-7B vs Ambari-7B-base). | DiD = native gain minus ITRANS gain, 97.5% intervals on SIB-200 and retrieval; supported if both above 0. | SIB-200 DiD +0.423 [0.380, 0.466]; retrieval DiD +0.624 [0.584, 0.664]; the native gain confounds exposure with the tokenizer extension (ITRANS control: gain -0.034 on SIB-200) | **supported (both measures); confounded** | complete |
| X12 contrast 2 (Ambari instruction models, secondary) | The more fragmented model assembles words later (v0.2 against v0.1). | H3 sign rule on the assembly layer; descriptive (the pair is not clean). | native assembly layer difference +4 [3.000, 5.000] layers; tokens per word difference 12.85 | **pattern met (secondary)** | complete; secondary |
| X13 Qwen3-8B | The pattern holds in a 7 to 9B model (Qwen3-8B). | Extended P-a (all-but-one rule, enlarged model set); retrieval all-but-one. | counted (native CI lower 0.753); native minus ITRANS +0.322 and minus lossy +0.259; extended P-a 5 of 5 (ITRANS), 5 of 5 (lossy) | **supported (extended)** | complete |
| X13 Llama-3.1-8B | The pattern holds in a 7 to 9B model (Llama-3.1-8B). | Extended P-a (all-but-one rule, enlarged model set); retrieval all-but-one. | counted (native CI lower 0.684); native minus ITRANS +0.330 and minus lossy +0.249; extended P-a 5 of 5 (ITRANS), 5 of 5 (lossy) | **supported (extended)** | complete |
| X13 Sarvam-m (23.6B, 4-bit, SIB-200 only) | The pattern holds in a larger Indic-focused model. | Counted if native CI lower bound above 0.40; extended P-a with seven models. | native 0.840, natural 0.778, lossy 0.732, ITRANS 0.682, lowercase 0.660; native minus ITRANS +0.157 [0.129, 0.185]; extended P-a with seven models: ITRANS 7 of 7, lossy 7 of 7 | **supported (7 of 7, both contrasts); counted** | complete (X10 for this model pending) |
| X14 (hosted models, exploratory) | Large hosted models show the same native-over-romanized ordering on SIB-200. | Exploratory, no verdict. | allam-2-7b: native 0.337, ITRANS 0.190, gap +0.146 [0.115, 0.179]; gpt-oss-120b: native 0.836, ITRANS 0.625, gap +0.211 [0.181, 0.241]; qwen3.8-27b: native 0.836, ITRANS 0.658, gap +0.177 [0.147, 0.207] | **no verdict (native above natural above ITRANS in all three)** | complete; exploratory |

## Not run

| Experiment | Claim | Registered rule | Result | Verdict | Status |
|---|---|---|---|---|---|
| X15 (human baseline) | Humans read native and natural romanization equally well. | - | not run: annotators unavailable (skipped by decision) | **-** | not run |
| X7b (equal actual embedding parameters) | BPB control with equal actual parameters. | - | not run: with equal parameters the embedding rank is 114 at V=256 and 24 at V=4096, so it would measure the bottleneck (docs/X7B_NOTE.md; decision) | **-** | not run |
| X11 Arm B | Quantization gap of a 4B-class model. | - | not run: X6 shortlisted no 4B-class model | **-** | not run |
| X13 activation patching | Patching on one 7 to 9B model. | - | not run: optional; it fits one session only for one model and was dropped | **-** | not run |
| X10 for Sarvam-m | Generation in the 23.6B model. | - | pending: pilot running on Kaggle; to be run if the quota fits | **-** | pending |
`````

#### `results/phase2/PHASE2_INVENTORY.md` (5,365 bytes; first commit e0f0b06 2026-11-05 10:43:29 +0530)

`````text
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
| X9b secondary (Qwen3.5-2B, 1 seed, 3 runs) | **supported** on SIB-200 and retrieval (English run completed on the laptop after the kernel cap) | K2, L |
| X13 Sarvam-m (23.6B, 4-bit, SIB-200 only) | finished 15:3x: counted; native minus ITRANS +0.157; three forms only (5 h cap) | K2 | done |
| X4 K3b-te | finished 10:52: refuted | API, L | done |
| X10 post hoc | finished 11:09: the empty first line is a "<think>" block; registered verdict unchanged | L | done |
| X14 (hosted large models, exploratory, no verdict) | finished 14:23 IST (3,269 rows per model; analysis in RESULTS.md) | API (Groq), L | done |

## Not run yet (registered, still to do)

| Experiment | What is left | Machine | Plan and projected date |
|---|---|---|---|
| X5 (cross-language consistency, analysis only) | DONE 11:55: consistent on both measures (see RESULTS.md) | L |
| X13 Sarvam-m: lossy, lowercase, natural forms and X10 | not run: Kaggle quota exhausted on both accounts (30 h cap); earliest push about 9 Nov (K1) or 11 Nov (K2) | K1, K2 | after quota rolls off |
| X13 activation patching on one 7 to 9B model | registered as optional (only if it fits one 12 h session); not built | K1 or K2 | decision needed: leave dropped unless time allows |
| X11 Arm B (one 4B-class model, descriptive, no verdict) | no 4B-class model was shortlisted by X6, so it cannot be formed | none | not run |

## Not run (by decision or impossibility)

| Experiment | Reason |
|---|---|
| X7b | considered and not run (embedding rank argument; Aarnav's decision) |
| X15 (human intelligibility baseline) | annotators unavailable; skipped by decision |

## End-of-Phase-2 housekeeping (after Aarnav says Phase 2 is closed)

Delete the private Kaggle datasets (account 1: shattered-flores-private, shattered-llama-2-7b-hf, shattered-llama-3-1-8b, shattered-ambari-instruct-v0-1; account 2: the same names, minus Llama-2, plus shattered-pkg), delete the kernels on both accounts, revoke the shared Kaggle token (account 2) and the third account's token (KAGGLE3_API_TOKEN, pasted in chat 2026-11-05), delete any private datasets and kernels created on the third account (aarnavkembhavi), log each deletion. Phase 2 results enter the paper only when Aarnav says so; the paper has not been edited.

## Machine load now

Laptop GPU: X10 post hoc (about 1 h); then nothing registered is ready on it except what X5 and any X13 follow-up produce. K1: idle (X10 for Sarvam-m is the only registered job that could use it). K2: X9b secondary and X13 Sarvam-m.
`````

#### `results/phase2/REGISTERED_OUTCOMES.md` (8,879 bytes; first commit 285c028 2026-11-03 00:04:58 +0530)

`````text
# Phase 2 registered outcomes: status ledger

Last updated 2026-11-08 15:33 IST (system clock). Rows for other experiments are added when each reports its registered verdict word; no registered rule is changed.

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
| X12 contrast 2 (Ambari-Instruct v0.1 vs v0.2, MDL layer, descriptive) | H3-style sign rule | **complete: pattern met** | native layer 4 (v0.1) vs 8 (v0.2), difference +4 [3, 5], matches the tokens-per-word sign; ITRANS control 0 [0, 1]; the two models are not a clean base-model-fixed pair (registered caveat) |
| X9b primary (Sarvam-1, QLoRA continued pretraining at fixed tokenizer) | supported / partly / refuted per measure | **complete: supported on SIB-200 and on retrieval (D_N and D_E intervals above 0)** | SIB D_N +0.225 [0.177, 0.273], D_E +0.196 [0.150, 0.244]; retrieval D_N +0.337 [0.296, 0.378], D_E +0.391 [0.344, 0.435]; ITRANS training closed most of the gap; controls widened it; English-trained run flagged for -5 points on English; Qwen3.5-2B arm not run |
| X13 Llama-3.1-8B | extended P-a, retrieval all-but-one | **complete: counted (native 0.712, CI lower 0.684); extended P-a supported (5 of 5, both contrasts); retrieval all-but-one met (4 of 4)** | native minus ITRANS +0.330 on SIB-200 and +0.809 on retrieval; MDL job queued; nothing against a prediction |
| X4 Bengali and Telugu, R2 (retrieval native > ITRANS on the 2,009 sentences) | supported / refuted | **R2 supported in both languages (3 of 3 counted models)** | R3, R4, ladder, sentiment, K3b still to build; nothing against a prediction |
| X4 R4 (assembly follows fragmentation, Bengali and Telugu) | H3-style sign rule | **supported in both languages (4 of 4 Bengali, 3 of 3 Telugu qualifying models)** | Telugu is uninformative if Qwen2.5-1.5B is excluded (only two qualifying models); lowercase ladder, R3, sentiment, K3b still to do |
| X4 R3 (natural > ITRANS retrieval, M4c analog, Bengali and Telugu) | supported / refuted | **supported in both languages (3 of 3 counted models)** | n = 236 and 243 test sentences (defective drafts removed); lowercase ladder, sentiment analysis and K3b-bn/te still to do |
| X4 ladder L1-L3 (Bengali and Telugu; lowercase form from the per-language E9 scheme) | effect rules as Phase 1 | **complete: L1 no effect; L2 positive (SIB-200 and retrieval, both languages); L3 positive on retrieval in both languages and on SIB-200 in Bengali, not detected on SIB-200 in Telugu** | matches Kannada except Bengali L3 on SIB-200; K3b-bn/te (Gemini vs Dakshina) still to run; nothing registered against |
| X4 R4, restated (main analysis excludes Qwen2.5-1.5B; supersedes the R4 row above) | H3-style sign rule | **Bengali supported (3 of 3 qualifying); Telugu uninformative (2 qualifying)**; sensitivity including Qwen2.5-1.5B: both supported | the rule is unchanged |
| X4 K3b-bn (Gemini vs Dakshina, Bengali) | holds / refuted / inconclusive | **refuted (against the prediction)** | vowel-doubling ratio 0.144 [0.095, 0.197] (Gemini lower); h-digraph and English share match; K3b-te running |
| X2 (measured romanized exposure, Source A) | e_hi > e_kn: supported / refuted / inconclusive | **supported** | Hindi 0.437% vs Kannada 0.045%, difference +0.392 pp [0.389, 0.396]; deviation X2-D1 (Poisson interval, single-shard configs) |
| X4 K3b-te (Gemini vs Dakshina, Telugu) | holds / refuted / inconclusive | **refuted (against the prediction)** | vowel doubling ratio 0.328 [0.293, 0.366] (Gemini lower); h-digraph 1.199 [1.111, 1.292] (Gemini higher); English share matches |
| X5 (cross-language consistency, descriptive) | consistent / inconsistent | **consistent on SIB-200 accuracy (negative in 3 of 4 models) and on retrieval (3 of 3)** | driven mostly by Hindi; Telugu has the highest exposure but similar gaps to Kannada and Bengali |
| X9b secondary (Qwen3.5-2B, 1 seed) | D_N > 0 and D_E > 0 | **supported on SIB-200 and retrieval** | SIB-200 D_N +0.285 [0.241, 0.328], D_E +0.260 [0.219, 0.301]; retrieval D_N +0.583 [0.545, 0.620], D_E +0.566 [0.529, 0.603]; secondary, one seed |
| X13 Sarvam-m (4-bit, SIB-200) | counted if native CI lower bound > 0.40 | **counted** (0.817); native - ITRANS +0.157 [0.129, 0.185]; native over ITRANS 7 of 7 models | forms English, native, ITRANS only (5 h cap); lossy not scored |
| X9b primary (Sarvam-1), extra seeds 3 and 4 (added after seeing seeds 1, 2) | D_N > 0 and D_E > 0 | **supported on SIB-200 and retrieval, with all four seeds and with the original two** | all four: SIB-200 D_N +0.222 [0.174, 0.270], D_E +0.194 [0.147, 0.243]; retrieval D_N +0.339 [0.292, 0.386], D_E +0.405 [0.353, 0.457] |
| X9b secondary (Qwen3.5-2B), extra seeds 2 and 3 (added after seeing seed 1) | D_N > 0 and D_E > 0 | **supported on SIB-200 and retrieval with three seeds** | SIB-200 D_N +0.301 [0.248, 0.351], D_E +0.258 [0.195, 0.315]; retrieval D_N +0.594 [0.550, 0.637], D_E +0.592 [0.544, 0.638] |
| X13 Sarvam-m, all six forms (extended P-a with seven models) | native vs ITRANS and native vs lossy, all-but-one | **native vs ITRANS 7 of 7; native vs lossy 7 of 7** | native minus ITRANS +0.157, lossy +0.108, lowercase +0.179, natural +0.047 (n = 257, p 0.065) |
`````

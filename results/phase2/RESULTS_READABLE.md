# Results, readable (one block per experiment id, at most 15 lines each; plain facts)

Source: result files under results/ and verbatim RESULTS.md titles (commit and date from git blame). Numbers are raw, not rounded. No interpretation. Phase 1, then Phase 2, then failed, dropped and not run.

## Phase 1

### E1: Token cost atlas
Registered: no separate registration entry (see the result entry)
Models run: not recorded as a column or key in the result files
Forms/conditions run: lossy, itrans, native; tasks/measures: not recorded as a column or key in the result files; seeds: 0
row 1 of 627: tokenizer=r50k_base; lang=eng_Latn; form=native; n_sentences=2009; tokens_total=52785; tokens_per_sentence=26.27426580388253; fertility=1.231711585579279; bytes_per_token=4.8761201098797; tax_ratio=1.0; tax_ci_low=1.0; tax_ci_high=1.0; family=OpenAI; gen=r50k (GPT-3); released=2020-06; kind=tiktoken; vocab_size=50257  [e01_cost/summary.csv]
row 2 of 627: tokenizer=r50k_base; lang=kan_Knda; form=native; n_sentences=2009; tokens_total=717433; tokens_per_sentence=357.1095072175211; fertility=22.75398033618776; bytes_per_token=1.0217623109056873; tax_ratio=13.591607464241735; tax_ci_low=13.476251632237446; tax_ci_high=13.708391752973734; family=OpenAI; gen=r50k (GPT-3); released=2020-06; kind=tiktoken; vocab_size=50257  [e01_cost/summary.csv]
Result entry: 2026-10-07 — E1/E2 rerun on FLORES+ (now primary) [RESULTS.md 89-98, `76c8073` 2026-10-07 16:40:03 +0530]
Source files: results/e01_cost/summary.csv

### E2: Transliteration round trip and lossy scheme
Registered: no separate registration entry (see the result entry)
Models run: gemini-3.5-flash-lite
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
n_texts = 2009  [e02_translit/roundtrip_flores_plus.json]
n_chars = 269806  [e02_translit/roundtrip_flores_plus.json]
n_exact = 2009  [e02_translit/roundtrip_flores_plus.json]
exact_rate = 1.0  [e02_translit/roundtrip_flores_plus.json]
examples[first of 5]: native="\u0c85\u0c82\u0ca6\u0cbe\u0c9c\u0cc1 \u0ca4\u0cb2\u0cbe \u0c92\u0c82\u0ca6\u0cc1 \u0caf\u0cc1.\u0c8e\u0cb8\u0ccd\u200c \u0cb8\u0cc6\u0c82\u0c9f\u0ccd\u200c\u0ca8\u0cbf\u0c82\u0ca6 \u0caa\u0ccd\u0cb0\u0cae\u0cbe\u0ca3\u0cbf\u0ca4 \u0c87\u0c82\u0c95\u0ccd\u200c\u0c9c\u0cc6\u0c9f\u0ccd \u0caa\u0ccd\u0cb0\u0cbf\u0c82\u0c9f\u0cb0\u0cc1\u0c97\u0cb3\u0ca8\u0ccd\u0ca8\u0cc1 \u0cac\u0cb3\u0cb8\u0cbf \u0c89\u0ca4\u0ccd\u0caa\u0cbe\u0ca6\u0cbf\u0cb8\u0cac\u0cb9\u0cc1\u0ca6\u0cbe\u0ca6 \u0cb8\u0ca3\u0ccd\u0ca3 \u0caa\u0ccd\u0cb0\u0cbf\u0c82\u0c9f\u0ccd \u0cae\u0cbe\u0ca1\u0cac\u0cb9\u0cc1\u0ca6\u0cbe\u0ca6 \u0c9a\u0cbf\u0caa\u0ccd\u200c \u0c86\u0c97\u0cbf\u0cb0\u0cc1\u0cb5 \u0cb8\u0cc6\u0cb2\u0ccd\u200c\u0c97\u0cb3 \u0cb5\u0cbf\u0ca7\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c86\u0caf\u0ccb\u0c9c\u0cbf\u0cb8\u0cc1\u0cb5 \u0cb9\u0cca\u0cb8 \u0caa\u0ca4\u0ccd\u0ca4\u0cc6 \u0caa\u0cb0\u0cbf\u0c95\u0cb0\u0ca6 \u0c85\u0ca8\u0ccd\u0cb5\u0cc7\u0cb7\u0ca3\u0cc6\u0caf \u0c98\u0ccb\u0cb7\u0ca3\u0cc6\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb8\u0ccd\u0c9f\u0cbe\u0ca8\u0ccd\u200c\u0cab\u0ccb\u0cb0\u0ccd\u0ca1\u0ccd\u200c \u0cb5\u0cbf\u0cb6\u0ccd\u0cb5\u0cb5\u0cbf\u0ca6\u0ccd\u0caf\u0cbe\u0cb2\u0caf\u0ca6 \u0c94\u0cb7\u0ca7 \u0cb6\u0cbe\u0cb2\u0cc6\u0caf \u0cb5\u0cbf\u0ca6\u0ccd\u0caf\u0cbe\u0cb0\u0ccd\u0ca5\u0cbf\u0c97\u0cb3\u0cc1 \u0cb8\u0ccb\u0cae\u0cb5\u0cbe\u0cb0 \u0cae\u0cbe\u0ca1\u0cbf\u0ca6\u0ccd\u0ca6\u0cbe\u0cb0\u0cc6."; lossy="andaju tala ondu yu.es sentninda pramanita inkjet printarugalannu balasi utpadisabahudada sanna print madabahudada chip agiruva selgala vidavannu ayojisuva hosa patte parikarada anveshaneya goshaneyannu stanpord vishvavidyalayada aushada shaleya vidyartigalu somavara madiddare."; inverted="\u0c85\u0c82\u0ca6\u0cbe\u0c9c\u0cc1 \u0ca4\u0cb2\u0cbe \u0c92\u0c82\u0ca6\u0cc1 \u0caf\u0cc1.\u0c8e\u0cb8\u0ccd \u0cb8\u0cc6\u0ca8\u0ccd\u0ca4\u0ccd\u0ca8\u0cbf\u0ca8\u0ccd\u0ca6 \u0caa\u0ccd\u0cb0\u0cae\u0cbe\u0ca3\u0cbf\u0ca4 \u0c87\u0c82\u0c95\u0ccd\u200c\u0c9c\u0cc6\u0c9f\u0ccd\u200c \u0caa\u0ccd\u0cb0\u0cbf\u0ca8\u0ccd\u0ca4\u0cb0\u0cc1\u0c97\u0cb2\u0ca8\u0ccd\u0ca8\u0cc1 \u0cac\u0cb3\u0cb8\u0cbf \u0c89\u0ca4\u0ccd\u0caa\u0cbe\u0ca6\u0cbf\u0cb8\u0cac\u0cb9\u0cc1\u0ca6\u0cbe\u0ca6 \u0cb8\u0ca3\u0ccd\u0ca3 \u0caa\u0ccd\u0cb0\u0cbf\u0c82\u0c9f\u0ccd \u0cae\u0cbe\u0ca1\u0cac\u0cb9\u0cc1\u0ca6\u0cbe\u0ca6 \u0c9a\u0cbf\u0caa\u0ccd \u0c86\u0c97\u0cbf\u0cb0\u0cc1\u0cb5 \u0cb8\u0cc6\u0cb2\u0ccd\u200c\u0c97\u0cb3 \u0cb5\u0cbf\u0ca7\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c86\u0caf\u0ccb\u0c9c\u0cbf\u0cb8\u0cc1\u0cb5 \u0cb9\u0cca\u0cb8 \u0caa\u0ca4\u0ccd\u0ca4\u0cc6 \u0caa\u0cb0\u0cbf\u0c95\u0cb0\u0ca6 \u0c85\u0ca8\u0ccd\u0cb5\u0cc7\u0cb7\u0ca3\u0cc6\u0caf \u0c98\u0ccb\u0cb7\u0ca3\u0cc6\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb8\u0ccd\u0c9f\u0cbe\u0ca8\u0ccd\u200c\u0cab\u0ccb\u0cb0\u0ccd\u0ca1\u0ccd \u0cb5\u0cbf\u0cb6\u0ccd\u0cb5\u0cb5\u0cbf\u0ca6\u0ccd\u0caf\u0cbe\u0cb2\u0caf\u0ca6 \u0c94\u0cb7\u0ca7 \u0cb6\u0cbe\u0cb2\u0cc6\u0caf \u0cb5\u0cbf\u0ca6\u0ccd\u0caf\u0cbe\u0cb0\u0ccd\u0ca5\u0cbf\u0c97\u0cb3\u0cc1 \u0cb8\u0ccb\u0cae\u0cb5\u0cbe\u0cb0 \u0cae\u0cbe\u0ca1\u0cbf\u0ca6\u0ccd\u0ca6\u0cbe\u0cb0\u0cc6."  [e02_translit/lossy_flores_plus.json]
examples[last of 5]: native="\u0cb5\u0cbf\u0cae\u0cbe\u0ca8 \u0ca8\u0cbf\u0cb2\u0ccd\u0ca6\u0cbe\u0ca3\u0ca6 \u0c85\u0c97\u0ccd\u0ca8\u0cbf \u0cb6\u0cbe\u0cae\u0c95 \u0ca6\u0cb3\u0ca6 \u0c92\u0c82\u0ca6\u0cc1 \u0cb5\u0ccd\u0caf\u0cbe\u0ca8\u0cc1, \u0cb8\u0ccd\u0cab\u0ccb\u0c9f\u0ca6 \u0c9c\u0cbe\u0c97\u0c95\u0ccd\u0c95\u0cc6 \u0cb9\u0ccb\u0c97\u0cc1\u0cb5\u0cbe\u0c97 \u0c89\u0cb0\u0cc1\u0cb3\u0cbf\u0ca4\u0cc1 \u0c8e\u0c82\u0ca6\u0cc1 \u0cb8\u0ccd\u0ca5\u0cb3\u0cc0\u0caf \u0cae\u0cbe\u0ca7\u0ccd\u0caf\u0cae\u0c97\u0cb3\u0cc1 \u0cb5\u0cb0\u0ca6\u0cbf \u0cae\u0cbe\u0ca1\u0cbf\u0cb5\u0cc6."; lossy="vimana nildanada agni shamaka dalada ondu vyanu, spotada jagakke hoguvaga urulitu endu staliya madyamagalu varadi madive."; inverted="\u0cb5\u0cbf\u0cae\u0cbe\u0ca8 \u0ca8\u0cbf\u0cb2\u0ccd\u0ca6\u0cbe\u0ca3\u0ca6 \u0c85\u0c97\u0ccd\u0ca8\u0cbf \u0cb6\u0cbe\u0cae\u0c95 \u0ca6\u0cb3\u0ca6 \u0c92\u0c82\u0ca6\u0cc1 \u0cb5\u0ccd\u0caf\u0cbe\u0ca8\u0cc1, \u0cb8\u0ccd\u0cab\u0ccb\u0c9f\u0ca6 \u0c9c\u0cbe\u0c97\u0c95\u0ccd\u0c95\u0cc6 \u0cb9\u0ccb\u0c97\u0cc1\u0cb5\u0cbe\u0c97 \u0c89\u0cb0\u0cc1\u0cb2\u0cbf\u0ca4\u0cc1 \u0c8e\u0c82\u0ca6\u0cc1 \u0cb8\u0ccd\u0ca5\u0cb3\u0cc0\u0caf \u0cae\u0cbe\u0ca7\u0ccd\u0caf\u0cae\u0c97\u0cb3\u0cc1 \u0cb5\u0cb0\u0ca6\u0cbf \u0cae\u0cbe\u0ca1\u0cbf\u0cb5\u0cc6."  [e02_translit/lossy_flores_plus.json]
Result entry: 2026-10-07 — E1/E2 rerun on FLORES+ (now primary) [RESULTS.md 89-98, `76c8073` 2026-10-07 16:40:03 +0530]
Source files: results/e02_translit/roundtrip_flores_plus.json; results/e02_translit/lossy_flores_plus.json

### E5: Controlled pretraining of tiny GPTs
Registered: PRE-REGISTRATION — Step 3: M1 word-identity probes on the E5 tiny models (written 2026-10-14, before any run) [RESULTS.md 289-308, `81d420c` 2026-10-14 22:16:36 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2, 3, 4
T6[first of 6]: vocab=256; bytes_per_token=1.0; tokens_per_word=5.013751512875088; ctx_tokens=1024.0; params_embedding=98688.0; params_non_embedding=14162304.0; train_flops=4.177259875270656e+16; val_bpb_mean=0.5969501412691028; val_bpb_sd=0.0009023194088351287  [e05_pretrain/analysis.json]
T6[last of 6]: vocab=4096; bytes_per_token=3.962679221179897; tokens_per_word=1.2652428402676088; ctx_tokens=256.0; params_embedding=1573248.0; params_non_embedding=14162304.0; train_flops=1.0008179383468032e+16; val_bpb_mean=0.528462391737498; val_bpb_sd=0.0010521012093391913  [e05_pretrain/analysis.json]
runs[first of 18]: vocab=256; seed=0; bytes_per_token=1.0; tokens_per_word=5.013751512875088; ctx_tokens=1024; params_embedding=98688; params_non_embedding=14162304; train_flops=41772598752706560; val_bpb=0.5965823017595128  [e05_pretrain/analysis.json]
runs[last of 18]: vocab=4096; seed=2; bytes_per_token=3.962679221179897; tokens_per_word=1.2652428402676088; ctx_tokens=256; params_embedding=1573248; params_non_embedding=14162304; train_flops=10008179383468032; val_bpb=0.5282917142317326  [e05_pretrain/analysis.json]
Result entry: 2026-10-15 — Step 3b (GATE 3): MDL and erasure probes on the 18 E5 tiny models [RESULTS.md 438-467, `baf4f09` 2026-10-15 00:56:53 +0530]
Source files: results/e05_pretrain/analysis.json

### E9: Tokenizer-optimal reversible romanization
Registered: no separate registration entry (see the result entry)
Models run: not recorded as a column or key in the result files
Forms/conditions run: itrans, native, e09:o200k|free, e09:qwen3|free, e09:gemma4|free, e09:o200k|lower, e09:qwen3|lower, e09:gemma4|lower, e09:qwen3.5|free, e09:qwen3.5|lower, e09:universal|free, e09:universal|lower; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
rows[first of 156]: tokenizer="o200k (GPT-4o)"; form="native"; tokens=103948; vs_native=1.0; vs_itrans=0.8226532760353601  [e09_romanize/savings.json]
rows[last of 156]: tokenizer="EuroLLM"; form="e09:universal|lower"; tokens=136125; vs_native=0.18638273051898263; vs_itrans=1.009619663571365  [e09_romanize/savings.json]
Result entry: 2026-10-07 — E9 GATE: tokenizer-optimal reversible romanization (token savings only) [RESULTS.md 110-132, `76c8073` 2026-10-07 16:40:03 +0530]
Source files: results/e09_romanize/savings.json

### E0: Gate, tokens per word, natural romanization checks, Step 0
Registered: no separate registration entry (see the result entry)
Models run: sarvam-1, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, openai/gpt-oss-120b, gemini-3.5-flash-lite
Forms/conditions run: itrans, native, english; tasks/measures: xnli, sentiment; seeds: 0
summary[first of 24]: model="qwen2.5-1.5b"; task="sentiment"; form="english"; n=200; chance=0.5; acc=0.985; acc_ci_low=0.965; acc_ci_high=1.0; acc_calibrated=0.995  [e00_gate/summary.json]
summary[last of 24]: model="sarvam-1"; task="xnli"; form="native"; n=200; chance=0.3333333333333333; acc=0.52; acc_ci_low=0.45; acc_ci_high=0.59; acc_calibrated=0.5  [e00_gate/summary.json]
gate[first of 4]: model="qwen2.5-1.5b"; passes=true  [e00_gate/summary.json]
gate[last of 4]: model="sarvam-1"; passes=true  [e00_gate/summary.json]
Result entry: 2026-10-08 — E0 GATE (4 of 5 models; Gemma 4 E2B not run) [RESULTS.md 205-231, `22013f7` 2026-10-08 01:52:43 +0530]
Source files: results/e00_gate/summary.json

### M1: Detokenization layer (M1) on pretrained models
Registered: PRE-REGISTRATION — M1 detokenization layer (written 2026-10-07, before any M1 run) [RESULTS.md 144-170, `8380e09` 2026-10-07 16:49:31 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: 4, itrans, native, english; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
verdicts.H1.per_qwen_model.qwen2.5-1.5b.holds = true  [m14_full/gate2/verdicts.json]
verdicts.H1.per_qwen_model.qwen3.5-2b.holds = true  [m14_full/gate2/verdicts.json]
verdicts.H1.holds = true  [m14_full/gate2/verdicts.json]
verdicts.H2.holds = false  [m14_full/gate2/verdicts.json]
Result entry: 2026-10-15 — GATE 2: full M1/M4 run (Qwen2.5-1.5B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; English, native, ITRANS) [RESULTS.md 601-680, `051f261` 2026-10-15 21:21:07 +0530]
Source files: results/m14_full/gate2/verdicts.json

### S3: Step 3 and 3b: word-identity, MDL and erasure probes on the E5 tiny models
Registered: PRE-REGISTRATION — Step 3: M1 word-identity probes on the E5 tiny models (written 2026-10-14, before any run) [RESULTS.md 289-308, `81d420c` 2026-10-14 22:16:36 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2
Q1b.verdict = "confirmed"  [m1_tiny_mdl/analysis.json]
Q2b.verdict = "confirmed"  [m1_tiny_mdl/analysis.json]
Q3b.verdict = "refuted"  [m1_tiny_mdl/analysis.json]
Result entry: 2026-10-15 — Step 3b (GATE 3): MDL and erasure probes on the 18 E5 tiny models [RESULTS.md 438-467, `baf4f09` 2026-10-15 00:56:53 +0530]
Source files: results/m1_tiny_mdl/analysis.json

### M4: M4, M4b, M4c: retrieval, mapping, surface baseline, natural romanization
Registered: PRE-REGISTRATION — M4c natural romanization in M4 (written 2026-10-16, before any natural FLORES+ sentence of this sample is romanized or run) [RESULTS.md 801-819, `d8e2bd8` 2026-10-16 00:49:27 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: itrans, native, natural; tasks/measures: unmapped retrieval acc@1, train-half centering, 248 candidates (as m4c_natural unmapped_test); seeds: not recorded as a column or key in the result files
verdict.per_model.qwen2.5-1.5b.status = "closes"  [m4b_mapping/verdict.json]
verdict.per_model.qwen3.5-2b.status = "persists"  [m4b_mapping/verdict.json]
verdict.per_model.sarvam-1.status = "persists"  [m4b_mapping/verdict.json]
verdict.per_model.gemma4-e2b.status = "persists"  [m4b_mapping/verdict.json]
paired_differences.qwen2.5-1.5b|native-natural|mapped.diff = 0.044354838709677435; CI = [-0.024193547666072845, 0.1088709682226181]  [m4c_natural/verdict.json]
paired_differences.qwen2.5-1.5b|native-natural|unmapped.diff = -0.1411290322580645; CI = [-0.2177419364452362, -0.06451612710952759]  [m4c_natural/verdict.json]
paired_differences.qwen2.5-1.5b|natural-itrans|mapped.diff = -0.032258064516129004; CI = [-0.0927419364452362, 0.032258063554763794]  [m4c_natural/verdict.json]
paired_differences.qwen2.5-1.5b|natural-itrans|unmapped.diff = 0.24596774193548387; CI = [0.19354838132858276, 0.30241936445236206]  [m4c_natural/verdict.json]
Result entry: 2026-10-17 (written 2026-10-21) — M4c natural romanization in M4 (registered 2026-10-16): refuted, natural is well above ITRANS [RESULTS.md 1200-1248, `d7693f7` 2026-10-21 22:25:39 +0530]
Source files: results/m4b_mapping/verdict.json; results/m4c_natural/verdict.json; results/m4b_surface/verdict.json; results/m4b_robustness/verdict.json

### E0b: Familiarity test (sentiment, XNLI)
Registered: PRE-REGISTRATION — E0b familiarity test (written 2026-10-14, before any E0b scoring) [RESULTS.md 241-272, `0a1d054` 2026-10-14 18:42:59 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: lossy, lower, itrans, native, english, natural; tasks/measures: sib, xnli, sentiment; seeds: 0
P3_parts.fraction_significant = 0.0  [e0b_familiarity/gate1/verdicts.json]
P3_parts.n_cells = 10  [e0b_familiarity/gate1/verdicts.json]
Result entry: 2026-10-15 — E0b GATE 1 (five forms, five models) [RESULTS.md 504-560, `3565362` 2026-10-15 16:40:24 +0530]
Source files: results/e0b_familiarity/gate1/verdicts.json

### E0c: SIB-200 topic classification
Registered: PRE-REGISTRATION — E0c SIB-200 topic classification (written 2026-10-16, before any SIB-200 item is scored) [RESULTS.md 833-868, `ba54695` 2026-10-16 02:29:27 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: lossy, lower, itrans, native, english, natural257; tasks/measures: sib; seeds: not recorded as a column or key in the result files
P_a = "partly supported"  [e0c_sib/gate/verdicts.json]
P_a_tests[first of 10]: model="gemma4-e2b"; task="sib"; a="native"; b="itrans"; acc_a=0.75; acc_b=0.3665338645418327; n=1004; diff=0.3834661354581673; a_only=425  [e0c_sib/gate/verdicts.json]
P_a_tests[last of 10]: model="sarvam-1"; task="sib"; a="native"; b="lossy"; acc_a=0.7659362549800797; acc_b=0.7051792828685259; n=1004; diff=0.06075697211155373; a_only=126  [e0c_sib/gate/verdicts.json]
P_b_secondary_mapped[first of 8]: model="qwen2.5-1.5b"; form="native"; beta=0.19276061379326914; p_holm=0.18179749209001259  [e0c_sib/gate/verdicts.json]
Result entry: 2026-10-17 — E0c SIB-200 topic classification (registered 2026-10-16): P-a partly supported, P-b inconclusive [RESULTS.md 1119-1188, `5e0ded5` 2026-10-17 05:01:13 +0530]
Source files: results/e0c_sib/gate/verdicts.json

### BT: Back-translation comprehension gap (large model)
Registered: no separate registration entry (see the result entry)
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
no result file; the numbers are in the RESULTS.md entry cited below
Result entry: 2026-10-15 — Large-model result: native vs romanized comprehension gap (back-translation) [RESULTS.md 482-503, `d0a6aa0` 2026-10-15 01:19:38 +0530]
Source files: none

### L: Romanization ladder L1 to L3
Registered: PRE-REGISTRATION — Romanization ladder L1–L3 (written 2026-10-22, Aarnav's design; before any ladder form is run or scored) [RESULTS.md 1319-1389, `93a9f68` 2026-10-22 01:03:02 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: lossy, lower, itrans, native, english, natural, natural257; tasks/measures: sib, xnli, sentiment, retrieval, sib_L3_secondary, xnli_reported_only; seeds: not recorded as a column or key in the result files
L1|retrieval.verdict = "no effect detected"  [l_ladder/verdict.json]
L1|retrieval.n_significant_positive = 0  [l_ladder/verdict.json]
L1|retrieval.needed = 2  [l_ladder/verdict.json]
L1|retrieval.n_counted = 3  [l_ladder/verdict.json]
Result entry: 2026-10-22 — Romanization ladder L1–L3 (registered 2026-10-22): results [RESULTS.md 1523-1578, `64ca06d` 2026-10-22 03:14:00 +0530]
Source files: results/l_ladder/verdict.json

### NC: NC1: non-canonical tokenization of lossy text
Registered: PRE-REGISTRATION — NC1: non-canonical tokenization of lossy text (written 2026-10-22, Aarnav's design; before any NC1 code is written, run or scored) [RESULTS.md 1615-1675, `e50581c` 2026-10-22 18:06:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: nc_a, nc_b, nc_c, lossy, lower, itrans, english, natural, a, b, c; tasks/measures: sib, xnli, sentiment, retrieval, xnli_reported_only; seeds: not recorded as a column or key in the result files
NC-F|retrieval.verdict = "no effect detected"  [nc1/verdict.json]
NC-F|retrieval.status = "registered prediction: positive"  [nc1/verdict.json]
NC-F|retrieval.n_significant_positive = 1  [nc1/verdict.json]
NC-F|retrieval.needed = 2  [nc1/verdict.json]
Result entry: PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by Aarnav with changes; before any patching code is written or run) [RESULTS.md 2436-2471, `6867631` 2026-10-23 16:00:59 +0530]
Source files: results/nc1/verdict.json

### K: Kanglish, annotation, K1 to K3, K3b, natural+dbl, V-VER, K2b
Registered: PRE-REGISTRATION — Kanglish and human-corrected natural romanization: K1–K3 (written 2026-10-16, before any Kanglish draft exists and before any scoring) [RESULTS.md 869-947, `d21d633` 2026-10-16 02:59:11 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: natural, k_kan_ver, k_nat_ver, k_kan_draft, k_nat_draft, natural_dbl, natural_dbl257, natural_verified, natural_verified257; tasks/measures: sib, sentiment, sib257, retrieval; seeds: 6, 26
K3b = "refuted"  [k3b/verdict.json]
statistics.vowel_doubling.verdict = "differs (Gemini lower)"  [k3b/verdict.json]
statistics.h_digraph.verdict = "matches"  [k3b/verdict.json]
statistics.english_word_share.verdict = "matches"  [k3b/verdict.json]
row 1 of 20: model=qwen2.5-1.5b; task=sentiment; comparison=primary; informative=True; n=200; acc_kanglish=0.645; acc_natural=0.515; diff=0.13; ci_low=0.07999999821186066; ci_high=0.1850000023841858; p=2.5560148060321808e-06; p_holm=1.7892103642225266e-05  [k12/k1.csv]
row 2 of 20: model=qwen2.5-1.5b; task=sentiment; comparison=secondary_drafts; informative=True; n=200; acc_kanglish=0.63; acc_natural=0.52; diff=0.10999999999999999; ci_low=0.05999999865889549; ci_high=0.1599999964237213; p=2.744048833847046e-05; p_holm=  [k12/k1.csv]
differences[first of 6]: measure="retrieval"; model="qwen3.5-2b"; n=248; acc_natural_dbl=0.5282258064516129; acc_natural=0.5120967741935484; diff=0.016129032258064502; ci_low=-0.032258063554763794; ci_high=0.06451612710952759; dbl_only=22  [v_dbl/summary.json]
differences[last of 6]: measure="sib257"; model="gemma4-e2b"; n=257; acc_natural_dbl=0.5214007782101168; acc_natural=0.5447470817120622; diff=-0.023346303501945442; ci_low=-0.06614785641431808; ci_high=0.015564202331006527; dbl_only=11  [v_dbl/summary.json]
Result entry: 2026-10-30 — K3b-hi result; EXPERIMENT FREEZE (Aarnav, 2026-10-30) [RESULTS.md 3322-3335, `f7ce5a8` 2026-10-30 08:18:15 +0530]
Source files: results/k3b/verdict.json; results/k12/k1.csv; results/v_dbl/summary.json

### H: Hindi: H-Hindi, H1, H1-LF, K3b-hi, English-loan measures
Registered: PRE-REGISTRATION — Hindi natural romanization drafts and H-Hindi (written 2026-10-23 01:00 IST, Aarnav's design; before any Hindi draft or Hindi model output exists) [RESULTS.md 2113-2232, `dcf9cfe` 2026-10-23 01:02:11 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: lossy, itrans, native, natural, natural1004; tasks/measures: sib, sentiment, en_words, has_name, kn_words, has_digit, kn_tokens, retrieval; seeds: 0, 1, 6
retrieval.n_counted = 3  [h_hindi/h1_verdict.json]
retrieval.needed = 2  [h_hindi/h1_verdict.json]
retrieval.n_positive = 2  [h_hindi/h1_verdict.json]
retrieval.verdict = "effect (H1 supported)"  [h_hindi/h1_verdict.json]
n_positive = 3  [h1lf/opt1_verdict.json]
needed = 3  [h1lf/opt1_verdict.json]
verdict = "loan-free effect"  [h1lf/opt1_verdict.json]
K3b = "inconclusive"  [k3b_hi/verdict.json]
Result entry: 2026-10-28 06:50 IST — H1-LF selection check results (exploratory, no verdict; registered 06:20 IST; `scripts/h1lf_selection.py`) [RESULTS.md 3261-3269, `9fbb738` 2026-10-28 10:17:38 +0530]
Source files: results/h_hindi/h1_verdict.json; results/h1lf/opt1_verdict.json; results/k3b_hi/verdict.json

### EP: Activation patching E-P1, E-P2, EP-R
Registered: PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by Aarnav with changes; before any patching code is written or run) [RESULTS.md 2436-2471, `6867631` 2026-10-23 16:00:59 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: sib, sentiment; seeds: 0
verdict.P1a.n_positive = 0  [ep1/predictions.json]
verdict.P1a.needed = 3  [ep1/predictions.json]
verdict.P1b.n_positive = 4  [ep1/predictions.json]
verdict.P1b.needed = 3  [ep1/predictions.json]
verdict.P2a.n_positive = 0  [ep2/predictions.json]
verdict.P2a.needed = 3  [ep2/predictions.json]
verdict.P2b.n_positive = 4  [ep2/predictions.json]
verdict.P2b.needed = 3  [ep2/predictions.json]
Result entry: 2026-10-26 12:20 IST — EP-R results (exploratory, registered 2026-10-26 02:40 IST; no verdict; registered E-P1/E-P2 outcomes unchanged) [RESULTS.md 3033-3057, `46bd82a` 2026-10-26 12:10:58 +0530]
Source files: results/ep1/predictions.json; results/ep2/predictions.json; results/ep_robust/summary.json

## Phase 2

### X1: Second prompt template (T2) and Kannada instruction (T3)
Registered: X1. Second prompt template (Kannada; 5 models; inference only) [RESULTS.md 3352-3395, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: nc_a, nc_b, nc_c, lossy, lower, itrans, native, english, natural, natural257; tasks/measures: sib, xnli, sentiment, sib_nc, sentiment_nc, sib_L3_secondary; seeds: not recorded as a column or key in the result files
T-a.primary_P_a_exact_wording_all_informative_models.verdict = "refuted"  [phase2/x1/t2/analysis/summary.json]
T-a.secondary_every_counted_model.verdict = "supported"  [phase2/x1/t2/analysis/summary.json]
T-a.phase1_same_lines.P_a = "partly supported"  [phase2/x1/t2/analysis/summary.json]
t2_effect_verdicts.L1|sentiment.verdict = "no effect detected"  [phase2/x1/t2/analysis/summary.json]
Result entry: 2026-11-04 20:44 IST, X1 T3 ANALYSIS (exploratory; label "instruction verified by a native speaker, exploratory"; `scripts/x1_analyse_t3.py`, same code and rules as the T2 analysis with T3 in place of T2; `results/phase2/x1/t3/ana [RESULTS.md 3927-3927, `3c30aee` 2026-11-04 20:44:16 +0530]
Source files: results/phase2/x1/t2/analysis/summary.json

### X2: Measured romanized exposure
Registered: X2. Measured romanized exposure (CPU and network; no GPU) [RESULTS.md 3396-3399, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
registered_test.verdict = "supported"  [phase2/x2/exposure.json]
languages.kn.documents_native = 2390982  [phase2/x2/exposure.json]
languages.kn.documents_latin = 1070  [phase2/x2/exposure.json]
languages.kn.e_documents = 0.00044731469048331726  [phase2/x2/exposure.json]
Result entry: 2026-11-05 10:35 IST, X2 RESULT (CPU and network; `scripts/x2_exposure.py`, `results/phase2/x2/exposure.json`): SUPPORTED (as predicted): the romanized share is higher for Hindi than for Kannada. [RESULTS.md 3987-3988, `d4363ef` 2026-11-05 10:35:58 +0530]
Source files: results/phase2/x2/exposure.json

### X3: Frequency-matched non-canonical tokenization
Registered: X3. Frequency-matched non-canonical tokenization (Kannada) [RESULTS.md 3400-3412, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: nc_a, nc_c, x3_m, x3_r, a, c, m, r; tasks/measures: sib, xnli, sentiment, retrieval, xnli_reported_only; seeds: 0
D1|retrieval|m.verdict = "effect, positive"  [phase2/x3/verdict.json]
D1|retrieval|m.status = "registered"  [phase2/x3/verdict.json]
D1|retrieval|m.n_significant_positive = 2  [phase2/x3/verdict.json]
D1|retrieval|m.needed = 2  [phase2/x3/verdict.json]
Result entry: PHASE 2 RESULT: X3 frequency-matched non-canonical tokenization (run 2026-11-02; registered 2026-11-01) [RESULTS.md 3460-3471, `9dec97e` 2026-11-02 16:00:24 +0530]
Source files: results/phase2/x3/verdict.json

### X4: Bengali and Telugu replication, K3b-bn, K3b-te
Registered: X4. Bengali and Telugu replication (core automatic pipeline; no Kanglish, no native-speaker verification, no patching) [RESULTS.md 3413-3426, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: lossy, lower, itrans, native, natural; tasks/measures: sib, sentiment; seeds: 6
R1.native_vs_itrans.n_counted = 4  [phase2/x4/bn/r1.json]
R1.native_vs_itrans.verdict = "supported"  [phase2/x4/bn/r1.json]
R1.native_vs_lossy.n_counted = 4  [phase2/x4/bn/r1.json]
R1.native_vs_lossy.verdict = "supported"  [phase2/x4/bn/r1.json]
R1.native_vs_itrans.n_counted = 4  [phase2/x4/te/r1.json]
R1.native_vs_itrans.verdict = "supported"  [phase2/x4/te/r1.json]
R1.native_vs_lossy.n_counted = 4  [phase2/x4/te/r1.json]
R1.native_vs_lossy.verdict = "supported"  [phase2/x4/te/r1.json]
Result entry: 2026-11-05 10:52 IST, K3b-te RESULT (Gemini vs Dakshina native-speaker romanization, Telugu; `results/phase2/x4/k3b_te/verdict.json`): REFUTED by the registered rule (against the prediction that Gemini matches the human romanizati [RESULTS.md 3991-3992, `b9246e2` 2026-11-05 10:52:45 +0530]
Source files: results/phase2/x4/bn/r1.json; results/phase2/x4/te/r1.json; results/phase2/x4/k3b_bn/verdict.json; results/phase2/x4/k3b_te/verdict.json

### X5: Cross-language consistency
Registered: X5. Cross-language consistency (analysis only, descriptive; after X2 and X4) [RESULTS.md 3427-3429, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
accuracy_verdict.verdict = "consistent"  [phase2/x5/analysis.json]
retrieval_verdict.verdict = "consistent"  [phase2/x5/analysis.json]
k3b_reported_next_to_the_figure.kn.verdict = "refuted"  [phase2/x5/analysis.json]
k3b_reported_next_to_the_figure.hi.verdict = "inconclusive"  [phase2/x5/analysis.json]
Result entry: 2026-11-05 11:42 IST, X5 RESULT (analysis only, descriptive; `scripts/x5_analyse.py`, `results/phase2/x5/analysis.json`): "consistent" on both measures (as predicted). [RESULTS.md 3995-3996, `124a4cc` 2026-11-05 11:42:00 +0530]
Source files: results/phase2/x5/analysis.json

### X6: New models screen and counting
Registered: X6. New models, only if they add a new tokenizer regime [RESULTS.md 3430-3432, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: oro-1.7b, llama-3.2-1b
Forms/conditions run: lossy, lower, itrans, native, english; tasks/measures: sib; seeds: not recorded as a column or key in the result files
llama-3.2-1b.accuracy.english.acc_cal = 0.6334661354581673; CI = [0.603585657370518, 0.6623505976095617]; n = 1004  [phase2/x6/counting.json]
llama-3.2-1b.accuracy.itrans.acc_cal = 0.21314741035856574; CI = [0.18824701195219123, 0.23904382470119523]; n = 1004  [phase2/x6/counting.json]
llama-3.2-1b.accuracy.lossy.acc_cal = 0.2410358565737052; CI = [0.2151394422310757, 0.2679282868525896]; n = 1004  [phase2/x6/counting.json]
llama-3.2-1b.accuracy.lower.acc_cal = 0.18625498007968128; CI = [0.16235059760956175, 0.21115537848605578]; n = 1004  [phase2/x6/counting.json]
Result entry: 2026-11-05 03:38 IST, X6 COUNTING RESULT (rule 3; laptop; `scripts/x6_run.py`, `results/phase2/x6/counting.json`): neither shortlist model is counted. [RESULTS.md 3962-3963, `b9383db` 2026-11-05 03:38:22 +0530]
Source files: results/phase2/x6/counting.json

### X7: Tiny-GPT embedding accounting, factorized control, X7-A, X7b
Registered: X7. Tiny-GPT embedding accounting and a factorized-embedding control [RESULTS.md 3433-3436, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2
verdict = "does not survive"  [phase2/x7/analysis.json]
per_vocab[first of 6]: vocab=256; bpb_mean=0.601669; bpb_sd_ddof1=0.00321; bpb_sd_ddof0=0.002621; n_seeds=3; embedding_params=157850; non_embedding_params=14162304; total_params=14320154; embedding_share=0.011023  [phase2/x7/analysis.json]
per_vocab[last of 6]: vocab=4096; bpb_mean=0.652979; bpb_sd_ddof1=0.002645; bpb_sd_ddof0=0.00216; n_seeds=3; embedding_params=107030; non_embedding_params=14162304; total_params=14269334; embedding_share=0.007501  [phase2/x7/analysis.json]
verdict = "supported"  [phase2/x7a/analysis.json]
detok_layer_by_vocab.256.seeds = [2, 2, 2]  [phase2/x7a/analysis.json]
detok_layer_by_vocab.256.mean = 2.0  [phase2/x7a/analysis.json]
detok_layer_by_vocab.256.phase1_seeds = [2, 2, 2]  [phase2/x7a/analysis.json]
Result entry: 2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md) [RESULTS.md 3858-3859, `3290232` 2026-11-04 01:44:01 +0530]
Source files: results/phase2/x7/analysis.json; results/phase2/x7a/analysis.json

### X8: Blind second-annotator sample
Registered: X8. Blind second-annotator sample (needs Aarnav's annotators) [RESULTS.md 3437-3451, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 8
K4_i_kappa.status = "primary outcome: the agreement itself, no threshold"  [phase2/x8/analysis.json]
K4_ii_cer.status = "primary outcome: the agreement itself, no threshold"  [phase2/x8/analysis.json]
descriptive_K3b_statistics.vowel_doubling.status = "descriptive, no verdict"  [phase2/x8/analysis.json]
descriptive_K3b_statistics.h_digraph.status = "descriptive, no verdict"  [phase2/x8/analysis.json]
Result entry: 2026-11-03 13:32 IST, X8 COMPLETE (decisions of Aarnav; no registered rule changed). [RESULTS.md 3841-3843, `3529fe7` 2026-11-03 13:32:32 +0530]
Source files: results/phase2/x8/analysis.json

### X9a: Tiny GPT, familiarity manipulated, fragmentation fixed; X9a-low and extra seeds
Registered: X9a. Tiny GPT, familiarity manipulated, fragmentation fixed (laptop) [RESULTS.md 3531-3573, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2, 3, 4, 0.1, 1.0, 0.02, 0.04, 0.46, 0.024, 0.036, 0.052, 0.064, 0.068, 0.072, 0.112, 0.116, 0.172, 0.432, 0.988, 0.992, 0.996
X9a_R.verdict = "refuted"  [phase2/x9a/analysis.json]
X9a_A.verdict = "supported"  [phase2/x9a/analysis.json]
n_runs = 18  [phase2/x9a/analysis_low.json]
retrieval_by_level.0.0.seeds = [0.024, 0.02, 0.04]  [phase2/x9a/analysis_low.json]
retrieval_by_level.0.0.mean = 0.027999999999999997  [phase2/x9a/analysis_low.json]
retrieval_by_level.0.01.seeds = [0.036, 0.052, 0.04]  [phase2/x9a/analysis_low.json]
Result entry: 2026-11-04 20:44 IST, X9a cipher token counts (descriptive; `results/phase2/x9a/cipher_tokens.json`, `scripts/x9a_cipher_tokens.py`). [RESULTS.md 3928-3928, `3c30aee` 2026-11-04 20:44:16 +0530]
Source files: results/phase2/x9a/analysis.json; results/phase2/x9a/analysis_low.json

### X9b: QLoRA continued pretraining (Sarvam-1 primary, Qwen3.5-2B secondary), extra seeds
Registered: X9b. Real models, QLoRA continued pretraining (memory pilot on the laptop; full runs on Kaggle) [RESULTS.md 3574-3611, `680151b` 2026-11-02 19:01:49 +0530]
Models run: sarvam-1, qwen3.5-2b
Forms/conditions run: itrans, native, english; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2, 3, 9
measures.SIB-200 accuracy.verdict = "supported"  [phase2/x9b/analysis_sarvam-1.json]
measures.FLORES+ retrieval.verdict = "supported"  [phase2/x9b/analysis_sarvam-1.json]
measures.SIB-200 accuracy.D_N.point = 0.22460159362549803; CI = [0.17729083665338644, 0.2729083665338645]  [phase2/x9b/analysis_sarvam-1.json]
measures.SIB-200 accuracy.D_E.point = 0.19621513944223107; CI = [0.15039840637450197, 0.24402390438247012]  [phase2/x9b/analysis_sarvam-1.json]
measures.SIB-200 accuracy.verdict = "supported"  [phase2/x9b/analysis_sarvam-1_seeds0123.json]
measures.FLORES+ retrieval.verdict = "supported"  [phase2/x9b/analysis_sarvam-1_seeds0123.json]
measures.SIB-200 accuracy.D_N.point = 0.22186254980079678; CI = [0.17430278884462153, 0.2699203187250996]  [phase2/x9b/analysis_sarvam-1_seeds0123.json]
measures.SIB-200 accuracy.D_E.point = 0.1942231075697211; CI = [0.14741035856573706, 0.24302788844621512]  [phase2/x9b/analysis_sarvam-1_seeds0123.json]
Result entry: 2026-11-06 11:53 IST, X9b PRIMARY ARM: EXTRA SEEDS FINISHED; RESULT WITH ALL FOUR SEEDS AND WITH THE ORIGINAL TWO (Sarvam-1; seeds 3 and 4 were ADDED AFTER SEEING SEEDS 1 AND 2, same QLoRA recipe, streams and budget, laptop; `x9b_ [RESULTS.md 4033-4033, `e605a65` 2026-11-06 11:53:24 +0530]
Source files: results/phase2/x9b/analysis_sarvam-1.json; results/phase2/x9b/analysis_sarvam-1_seeds0123.json; results/phase2/x9b/analysis_qwen3.5-2b_seeds012.json

### X10: Generation FLORES+ devtest to English (and post hoc, Sarvam-m)
Registered: X10. Generation: FLORES+ devtest to English (laptop pilot; laptop or Kaggle full) [RESULTS.md 3612-3623, `680151b` 2026-11-02 19:01:49 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b
Forms/conditions run: lossy, lower, itrans, native, natural; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
X10_P.verdict = "supported"  [phase2/x10/analysis.json]
contrasts[0].diff = 26.44827439335156; CI = [25.629326137797776, 27.25200599075477]; n = 1012  [phase2/x10/analysis.json]
contrasts[1].diff = 25.80510643671627; CI = [24.96249548080026, 26.647807384271786]; n = 1012  [phase2/x10/analysis.json]
contrasts[2].diff = 24.096581630985153; CI = [23.2863699721278, 24.92023944637181]; n = 1012  [phase2/x10/analysis.json]
Result entry: 2026-11-08 16:23 IST, SARVAM-M X10 PILOT RESULT AND THE RUN DECISION (account 3; timing only, no chrF used for any decision). [RESULTS.md 4054-4055, `0034538` 2026-11-08 16:23:25 +0530]
Source files: results/phase2/x10/analysis.json

### X11: Quantization control
Registered: X11. Quantization control (laptop) [RESULTS.md 3624-3633, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
verdict = "partly supported"  [phase2/x11/analysis.json]
forms.english.change.diff = -0.0199203187250996; CI = [-0.0348605577689243, -0.0049800796812749]  [phase2/x11/analysis.json]
forms.native.change.diff = -0.00796812749003984; CI = [-0.02390438247011952, 0.0069721115537848604]  [phase2/x11/analysis.json]
forms.itrans.change.diff = 0.017928286852589643; CI = [-0.00597609561752988, 0.04183266932270916]  [phase2/x11/analysis.json]
Result entry: 2026-11-04 12:07 IST, X11 ARM A RESULT (laptop, finished 12:00 IST): PARTLY SUPPORTED (registered rule; the prediction "quantization does not change the picture" is not fully met by the rule). [RESULTS.md 3902-3903, `bbc32e2` 2026-11-04 12:07:30 +0530]
Source files: results/phase2/x11/analysis.json

### X12: Ambari natural experiment
Registered: X12. Ambari natural experiment (Kaggle, 7B in fp16 sharded over 2 x T4) [RESULTS.md 3634-3655, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
verdict = "supported"  [phase2/x12/contrast1.json]
sib.did = 0.42330677290836655; CI = [0.3804780876494024, 0.46613545816733065]; n = 1004  [phase2/x12/contrast1.json]
retrieval.did = 0.6238805970149254; CI = [0.5840796019900497, 0.663681592039801]; n = 1005  [phase2/x12/contrast1.json]
models.ambari-7b-instruct-v0.1.native.detok_layer = 4  [phase2/x12/contrast2_mdl.json]
models.ambari-7b-instruct-v0.1.native.tokens_per_word = 1.6562222222222223  [phase2/x12/contrast2_mdl.json]
models.ambari-7b-instruct-v0.1.native.n_layers = 32  [phase2/x12/contrast2_mdl.json]
models.ambari-7b-instruct-v0.1.itrans.detok_layer = 3  [phase2/x12/contrast2_mdl.json]
Result entry: 2026-11-05 02:38 IST, X12 CONTRAST 2 RESULT (secondary; instruction-pair exposure contrast; MDL assembly layer, descriptive; Kaggle account 2 run, 1.50 h; `scripts/x12_contrast2.py`, `results/phase2/x12/contrast2_mdl.json`): the r [RESULTS.md 3956-3957, `ec3c085` 2026-11-05 02:38:48 +0530]
Source files: results/phase2/x12/contrast1.json; results/phase2/x12/contrast2_mdl.json

### X13: 7 to 9B and Sarvam-m models
Registered: X13. More 7-9B models on Kaggle [RESULTS.md 3656-3666, `680151b` 2026-11-02 19:01:49 +0530]
Models run: qwen3-8b, sarvam-1, sarvam-m, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, llama-3.1-8b
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: sib; seeds: not recorded as a column or key in the result files
P_a_extended.native_vs_itrans.verdict = "supported"  [phase2/x13/qwen3-8b/analysis.json]
P_a_extended.native_vs_lossy.verdict = "supported"  [phase2/x13/qwen3-8b/analysis.json]
accuracy.english.acc_cal = 0.8366533864541833; CI = [0.8137450199203188, 0.8595617529880478]; n = 1004  [phase2/x13/qwen3-8b/analysis.json]
accuracy.itrans.acc_cal = 0.45717131474103584; CI = [0.4262948207171315, 0.48804780876494025]; n = 1004  [phase2/x13/qwen3-8b/analysis.json]
P_a_extended.native_vs_itrans.verdict = "supported"  [phase2/x13/llama-3.1-8b/analysis.json]
P_a_extended.native_vs_lossy.verdict = "supported"  [phase2/x13/llama-3.1-8b/analysis.json]
accuracy.english.acc_cal = 0.7848605577689243; CI = [0.7589641434262948, 0.8107569721115537]; n = 1004  [phase2/x13/llama-3.1-8b/analysis.json]
accuracy.itrans.acc_cal = 0.38247011952191234; CI = [0.35258964143426297, 0.41334661354581675]; n = 1004  [phase2/x13/llama-3.1-8b/analysis.json]
Result entry: 2026-11-08 15:33 IST, X13 SARVAM-M: ALL SIX FORMS SCORED; EXTENDED P-a WITH SARVAM-M (account 3, aakarshprabhu, 2026-11-07 03:00 to 06:18; `scripts/x13_sarvam_m.py`, `results/phase2/x13/sarvam-m/analysis.json`). [RESULTS.md 4049-4049, `0cd9a82` 2026-11-08 15:33:40 +0530]
Source files: results/phase2/x13/qwen3-8b/analysis.json; results/phase2/x13/llama-3.1-8b/analysis.json; results/phase2/x13/sarvam-m/analysis.json

### X14: Black-box hosted models
Registered: X14. Black-box hosted large models (exploratory, no verdict) [RESULTS.md 3667-3676, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
allam-2-7b.acc.native.acc = 0.33665338645418325; CI = [0.30776892430278885, 0.3665338645418327]; n = 1004  [phase2/x14/analysis.json]
allam-2-7b.acc.itrans.acc = 0.1902390438247012; CI = [0.16633466135458166, 0.21414342629482072]; n = 1004  [phase2/x14/analysis.json]
allam-2-7b.acc.lossy.acc = 0.2539840637450199; CI = [0.22709163346613545, 0.28087649402390436]; n = 1004  [phase2/x14/analysis.json]
allam-2-7b.acc.natural.acc = 0.29571984435797666; CI = [0.24124513618677043, 0.3540856031128405]; n = 257  [phase2/x14/analysis.json]
Result entry: 2026-11-05 14:37 IST, X14 FINISHED (hosted models via Groq, exploratory, no registered verdict; `scripts/x14_run.py`, `scripts/x14_analyse.py`, `results/phase2/x14/analysis.json`; finished 14:23 IST after the 12:45 reset; 3,269 ro [RESULTS.md 4005-4006, `88cf86e` 2026-11-05 14:37:51 +0530]
Source files: results/phase2/x14/analysis.json

### X15: Human intelligibility baseline
Registered: X15. Human intelligibility baseline (needs annotators) [RESULTS.md 3677-3686, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 15
not run; no result file
Result entry: 2026-11-02, X15 pages. [RESULTS.md 3710-3710, `f41e866` 2026-11-02 19:15:43 +0530]
Source files: none

### A: General rules A0, Kaggle precision and retrieval checks A1-P and A1-R, reproducibility gate
Registered: A0. General rules for X9 to X15 [RESULTS.md 3495-3514, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
gate_passed = false  [kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json]
models.sarvam-1.seconds = 327.2035653591156  [kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json]
models.sarvam-1.nonfinite.english = 0  [kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json]
models.sarvam-1.nonfinite.native = 0  [kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json]
Result entry: 2026-11-05 04:23 IST, X13 Llama-3.1-8B RESULT (Kaggle account 2; A1-P passed 2.78 h, scoring 1.82 h; `scripts/x13_analyse.py --model llama-3.1-8b`, `results/phase2/x13/llama-3.1-8b/analysis.json`): counted; extended P-a supported  [RESULTS.md 3966-3967, `5c0388b` 2026-11-05 04:23:24 +0530]
Source files: results/kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json

## Failed, dropped and not run (one line each, as logged)

- 2026-10-08 | 2026-10-08 — E0 GATE (4 of 5 models; Gemma 4 E2B not run) [RESULTS.md 205-231, `22013f7`]
- 2026-10-21 | 2026-10-21 — Chain incident: the Kanglish chain and watcher ended during laptop sleep [RESULTS.md 1283-1300, `d7693f7`]
- 2026-10-26 | 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists) [RESULTS.md 2972-3002, `46bd82a`]
- 2026-10-26 | 2026-10-26 14:50 IST — K1/K2 pilot: first attempt failed on an id-type error (no computation; fixed, relaunched) [RESULTS.md 3105-3109, `5baf376`]
- 2026-10-28 | 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched [RESULTS.md 3178-3185, `126a488`]
- 2026-11-03 | 2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehearsal discarded as designed. [RESULTS.md 3820-3821, `bcaebe7`]
- 2026-11-03 | 2026-11-03 12:56 IST, X8 imported and analysed as registered (K4, K5; K6 not run). [RESULTS.md 3825-3828, `16e09e4`]
- 2026-11-04 | 2026-11-04 01:44 IST, X7b DROPPED (Aarnav): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md). [RESULTS.md 3858-3859, `3290232`]
- 2026-11-04 | 2026-11-04 02:46 IST, Kaggle failure: Llama-2-7B A1-P (X12 contrast 1) did not run (harness error, no verdict, 0.07 h of quota; pushed 02:41 IST). [RESULTS.md 3868-3869, `0cfdea0`]
- 2026-11-04 | 2026-11-04 06:08 IST, cause of the Llama-2 and Llama-3.1 A1-P failures found (both 401 on Kaggle; Llama-3.1 pushed 06:04 IST). [RESULTS.md 3890-3891, `7cfcb18`]
- 2026-11-04 | 2026-11-04 12:13 IST, Kaggle driver fixes (decided 2026-11-04 after three failed launches). [RESULTS.md 3906-3907, `ed31e10`]
- 2026-11-05 | 2026-11-05 01:24 IST, watchdog: X4 scoring chain FAILED at 01:21 IST (laptop GPU idle for about a minute before the restart). [RESULTS.md 3950-3951, `a7577c6`]
- 2026-11-05 | 2026-11-05 15:42 IST, KAGGLE QUOTA EXHAUSTED ON BOTH ACCOUNTS (operational; nothing was pushed, no quota used by the attempt). [RESULTS.md 4015-4016, `3ecea71`]
- 2026-11-05 | 2026-11-05 22:37 IST, ACCOUNT 3 SMOKE GATE FAILED: THE ACCOUNT'S KERNELS HAVE NO INTERNET (operational; accounts 1 and 2 are unaffected). [RESULTS.md 4023-4024, `07e9a33`]
- 2026-11-05 | 2026-11-05 22:59 IST, X9b LAPTOP RUNS: CHECKPOINT SAVE STALLS 20+ MINUTES; CHANGE TO WHAT IS CHECKPOINTED (operational; recipe, streams and evaluation unchanged). [RESULTS.md 4025-4026, `1d0616d`]
- 2026-11-06 | 2026-11-06 00:53 IST, SECOND LAPTOP CRASH AND STABILITY CHANGE FOR THE X9b EXTRA RUNS (operational). [RESULTS.md 4029-4030, `8c59c8a`]

From results/phase2/PHASE2_INVENTORY.md, the rows listed as not run (verbatim):

- | X5 (cross-language consistency, analysis only) | DONE 11:55: consistent on both measures (see RESULTS.md) | L |
- | X13 Sarvam-m: lossy, lowercase, natural forms and X10 | not run: Kaggle quota exhausted on both accounts (30 h cap); earliest push about 9 Nov (K1) or 11 Nov (K2) | K1, K2 | after quota rolls off |
- | X13 activation patching on one 7 to 9B model | registered as optional (only if it fits one 12 h session); not built | K1 or K2 | decision needed: leave dropped unless time allows |
- | X11 Arm B (one 4B-class model, descriptive, no verdict) | no 4B-class model was shortlisted by X6, so it cannot be formed | none | not run |
- | X7b | considered and not run (embedding rank argument; Aarnav's decision) |
- | X15 (human intelligibility baseline) | annotators unavailable; skipped by decision |

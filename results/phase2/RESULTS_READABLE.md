# Results, readable (one block per experiment id; tables of every comparison of the registered rule; plain facts)

Source: result files under results/ (paths in each block) and verbatim RESULTS.md titles (commit and date from git blame). Numbers are raw, not rounded. No interpretation. Each table row is `label | field=value; ...` as stored in the file (CI as [low, high]; p_holm is the Holm-adjusted p where the file has it; verdict fields are the stored strings). A table is cut only where its header says CAP, with the file's row count. Phase 1, then Phase 2, then failed, dropped and not run.

## Phase 1

### E1: Token cost atlas
Registered: no separate registration entry (see the result entry)
Models run: not recorded as a column or key in the result files
Forms/conditions run: lossy, itrans, native; tasks/measures: not recorded as a column or key in the result files; seeds: 0
Table [e01_cost/summary.csv] (33 rows of 627):
  tokenizer=r50k_base | form=native | n_sentences=2009 | tokens_total=717433 | fertility=22.75398033618776 | tax_ratio=13.591607464241735 | tax_ci_low=13.476251632237446 | tax_ci_high=13.708391752973734
  tokenizer=p50k_base | form=native | n_sentences=2009 | tokens_total=717317 | fertility=22.750301300348873 | tax_ratio=13.589409870228284 | tax_ci_low=13.474160559552294 | tax_ci_high=13.706310488340785
  tokenizer=cl100k_base | form=native | n_sentences=2009 | tokens_total=470026 | fertility=14.907262924199175 | tax_ratio=8.871260593020402 | tax_ci_low=8.794954472447548 | tax_ci_high=8.948817403415243
  tokenizer=o200k_base | form=native | n_sentences=2009 | tokens_total=104138 | fertility=3.3028227085315573 | tax_ratio=1.98702512927169 | tax_ci_low=1.9718557541294852 | tax_ci_high=2.0024865569787114
  tokenizer=openai/gpt-oss-20b | form=native | n_sentences=2009 | tokens_total=104138 | fertility=3.3028227085315573 | tax_ratio=1.98702512927169 | tax_ci_low=1.9718557541294852 | tax_ci_high=2.0024865569787114
  tokenizer=TinyLlama/TinyLlama-1.1B-Chat-v1.0 | form=native | n_sentences=2009 | tokens_total=656897 | fertility=20.834031081509675 | tax_ratio=10.836486910044705 | tax_ci_low=10.735763413356645 | tax_ci_high=10.936704399351072
  tokenizer=bigscience/bloom-560m | form=native | n_sentences=2009 | tokens_total=70342 | fertility=2.230954646368538 | tax_ratio=1.3175619989510752 | tax_ci_low=1.3072865133770573 | tax_ci_high=1.328027457420478
  tokenizer=Qwen/Qwen1.5-7B | form=native | n_sentences=2009 | tokens_total=373436 | fertility=11.84383127180463 | tax_ratio=6.931398025094662 | tax_ci_low=6.866909993401721 | tax_ci_high=6.9959833030072796
  tokenizer=Qwen/Qwen2.5-7B-Instruct | form=native | n_sentences=2009 | tokens_total=373436 | fertility=11.84383127180463 | tax_ratio=6.931398025094662 | tax_ci_low=6.866909993401721 | tax_ci_high=6.9959833030072796
  tokenizer=Qwen/Qwen3-8B | form=native | n_sentences=2009 | tokens_total=373436 | fertility=11.84383127180463 | tax_ratio=6.931398025094662 | tax_ci_low=6.866909993401721 | tax_ci_high=6.9959833030072796
  tokenizer=Qwen/Qwen3.5-9B | form=native | n_sentences=2009 | tokens_total=168219 | fertility=5.335204567078972 | tax_ratio=3.1326865060151214 | tax_ci_low=3.1068301062434744 | tax_ci_high=3.158786323180118
  tokenizer=Qwen/Qwen3.8-27B | form=native | n_sentences=2009 | tokens_total=168219 | fertility=5.335204567078972 | tax_ratio=3.1326865060151214 | tax_ci_low=3.1068301062434744 | tax_ci_high=3.158786323180118
  tokenizer=google/gemma-4-E2B-it | form=native | n_sentences=2009 | tokens_total=102774 | fertility=3.2595623215984775 | tax_ratio=1.939315029719785 | tax_ci_low=1.924032612548252 | tax_ci_high=1.9550541289936059
  tokenizer=sarvamai/sarvam-2b-v0.5 | form=native | n_sentences=2009 | tokens_total=75589 | fertility=2.3973675864256263 | tax_ratio=1.2323958588081845 | tax_ci_low=1.2222147867858213 | tax_ci_high=1.2428478097023825
  tokenizer=sarvamai/sarvam-1 | form=native | n_sentences=2009 | tokens_total=75589 | fertility=2.3973675864256263 | tax_ratio=1.2323556743890312 | tax_ci_low=1.2221892941787817 | tax_ci_high=1.2428085588501505
  tokenizer=sarvamai/sarvam-m | form=native | n_sentences=2009 | tokens_total=120846 | fertility=3.8327307326355853 | tax_ratio=2.2253199521222724 | tax_ci_low=2.208427787258256 | tax_ci_high=2.24269258373967
  tokenizer=sarvamai/sarvam-30b | form=native | n_sentences=2009 | tokens_total=80738 | fertility=2.560672375515382 | tax_ratio=1.523272267607494 | tax_ci_low=1.5108000628997003 | tax_ci_high=1.536223397917724
  tokenizer=microsoft/phi-2 | form=native | n_sentences=2009 | tokens_total=716340 | fertility=22.719314938154138 | tax_ratio=13.570900824097755 | tax_ci_low=13.455871714206141 | tax_ci_high=13.688212394044996
  tokenizer=microsoft/Phi-3.5-mini-instruct | form=native | n_sentences=2009 | tokens_total=656897 | fertility=20.834031081509675 | tax_ratio=10.836486910044705 | tax_ci_low=10.735763413356645 | tax_ci_high=10.936704399351072
  tokenizer=microsoft/Phi-4-mini-instruct | form=native | n_sentences=2009 | tokens_total=104138 | fertility=3.3028227085315573 | tax_ratio=1.98702512927169 | tax_ci_low=1.9718557541294852 | tax_ci_high=2.0024865569787114
  tokenizer=mistralai/Mistral-7B-Instruct-v0.3 | form=native | n_sentences=2009 | tokens_total=367511 | fertility=11.655915001585791 | tax_ratio=6.283098543390549 | tax_ci_low=6.225468134061291 | tax_ci_high=6.339730919325315
  tokenizer=mistralai/Mistral-Nemo-Instruct-2407 | form=native | n_sentences=2009 | tokens_total=120846 | fertility=3.8327307326355853 | tax_ratio=2.2253199521222724 | tax_ci_low=2.208427787258256 | tax_ci_high=2.24269258373967
  tokenizer=deepseek-ai/DeepSeek-V3 | form=native | n_sentences=2009 | tokens_total=195642 | fertility=6.204947668886774 | tax_ratio=3.709837682038835 | tax_ci_low=3.681060861638074 | tax_ci_high=3.739628367271179
  tokenizer=allenai/OLMo-2-1124-7B | form=native | n_sentences=2009 | tokens_total=470026 | fertility=14.907262924199175 | tax_ratio=8.871260593020402 | tax_ci_low=8.794954472447548 | tax_ci_high=8.948817403415243
  tokenizer=utter-project/EuroLLM-9B-Instruct-2512 | form=native | n_sentences=2009 | tokens_total=730556 | fertility=23.170187123374564 | tax_ratio=12.966454864932022 | tax_ci_low=12.843771549086044 | tax_ci_high=13.086395336955238
  tokenizer=ibm-granite/granite-3.3-8b-instruct | form=native | n_sentences=2009 | tokens_total=556505 | fertility=17.6500158579131 | tax_ratio=8.684399431968915 | tax_ci_low=8.601698734060543 | tax_ci_high=8.768759882817807
  tokenizer=tiiuae/Falcon3-7B-Instruct | form=native | n_sentences=2009 | tokens_total=702457 | fertility=22.279004123057405 | tax_ratio=13.192671749990609 | tax_ci_low=13.062801065479366 | tax_ci_high=13.323704542467299
  tokenizer=BharatGenAI/Param-1-2.9B-Instruct | form=native | n_sentences=2009 | tokens_total=133279 | fertility=4.227053599746274 | tax_ratio=2.5280059179454106 | tax_ci_low=2.5071627128699747 | tax_ci_high=2.5491808660530144
  tokenizer=krutrim-ai-labs/Krutrim-2-instruct | form=native | n_sentences=2009 | tokens_total=120846 | fertility=3.8327307326355853 | tax_ratio=2.2253199521222724 | tax_ci_low=2.208427787258256 | tax_ci_high=2.24269258373967
  tokenizer=HuggingFaceTB/SmolLM3-3B | form=native | n_sentences=2009 | tokens_total=469868 | fertility=14.902251823660006 | tax_ratio=8.871627362498348 | tax_ci_low=8.795140784298933 | tax_ci_high=8.949260624721619
  tokenizer=swiss-ai/Apertus-8B-Instruct-2509 | form=native | n_sentences=2009 | tokens_total=120846 | fertility=3.8327307326355853 | tax_ratio=2.2253199521222724 | tax_ci_low=2.208427787258256 | tax_ci_high=2.24269258373967
  tokenizer=nvidia/NVIDIA-Nemotron-Nano-9B-v2 | form=native | n_sentences=2009 | tokens_total=120846 | fertility=3.8327307326355853 | tax_ratio=2.2253199521222724 | tax_ci_low=2.208427787258256 | tax_ci_high=2.24269258373967
  tokenizer=zai-org/GLM-4.5-Air | form=native | n_sentences=2009 | tokens_total=469929 | fertility=14.90418648905804 | tax_ratio=8.865915779941137 | tax_ci_low=8.788569223373583 | tax_ci_high=8.943567646841279
Result entry: 2026-10-07 — E1/E2 rerun on FLORES+ (now primary) [RESULTS.md 89-98, `76c8073` 2026-10-07 16:40:03 +0530]
Source files: results/e01_cost/summary.csv

### E2: Transliteration round trip and lossy scheme
Registered: no separate registration entry (see the result entry)
Models run: gemini-3.5-flash-lite
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [e02_translit/roundtrip_flores_plus.json] (5 records):
  (top) | n_texts=2009; n_chars=269806; n_exact=2009; exact_rate=1.0; n_separators=14; separators_per_text=0.006968641114982578; n_raw_runs=220; failing_chars=[]; failures=[]; seconds=2.3; n_texts_not_nfc=17
  unit_counts | IV=7054; S=6878; C=131185; V=107483; LIT=37673; RAW=220; DIG=1
  non_ascii_chars_in_raw_runs | U+0CD5=20; U+0CC2=9; U+0CD6=1
  nfc | n_texts=2009; n_chars=269776; n_exact=2009; exact_rate=1.0; n_separators=14; separators_per_text=0.006968641114982578; n_raw_runs=195; failing_chars=[]
  nfc.unit_counts | IV=7054; S=6878; C=131185; V=107483; LIT=37673; RAW=195; DIG=1
Table [e02_translit/lossy_flores_plus.json] (1 records):
  (top) | n_sentences=2009; n_ref_chars=268707; cer_corpus_backmap=0.030937042950127835; cer_itrans_decode_only=0.1924252066377132; word_accuracy_backmap=0.8846141647372261; backmap_coverage_tokens=0.9307304386437882; train_native_word_types=2334929; train_lossy_word_types=2092504; train_types_merged_frac=0.10382542681169316
Result entry: 2026-10-07 — E1/E2 rerun on FLORES+ (now primary) [RESULTS.md 89-98, `76c8073` 2026-10-07 16:40:03 +0530]
Source files: results/e02_translit/roundtrip_flores_plus.json; results/e02_translit/lossy_flores_plus.json

### E5: Controlled pretraining of tiny GPTs
Registered: PRE-REGISTRATION — Step 3: M1 word-identity probes on the E5 tiny models (written 2026-10-14, before any run) [RESULTS.md 289-308, `81d420c` 2026-10-14 22:16:36 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2, 3, 4
Table [e05_pretrain/analysis.json] (34 records):
  (top) | bpb_span_across_conditions=0.06848774953160486; max_seed_sd_bpb=0.002079757394676226; n_words_valid=4408824
  T6[0] | vocab=256; bytes_per_token=1.0; tokens_per_word=5.013751512875088; ctx_tokens=1024.0; params_embedding=98688.0; params_non_embedding=14162304.0; train_flops=4.177259875270656e+16; val_bpb_mean=0.5969501412691028; val_bpb_sd=0.0009023194088351287; mp_all_mean=0.885593220338983; mp_all_sd=0.05202554727885028; n_seeds=3; mp_subject_verb_agreement_singular_mean=0.8316666666666667; mp_subject_verb_agreement_plural_mean=0.9666666666666667; mp_determiner_noun_agreement_mean=0.7722222222222223; mp_irregular_past_mean=1.0
  T6[1] | vocab=384; bytes_per_token=1.9775921626158446; tokens_per_word=2.535280836794574; ctx_tokens=520.0; params_embedding=147840.0; params_non_embedding=14162304.0; train_flops=1.931584877494272e+16; val_bpb_mean=0.5695644725935474; val_bpb_sd=0.001125144996807496; mp_all_mean=0.9237288135593221; mp_all_sd=0.0500914848200716; n_seeds=3; mp_subject_verb_agreement_singular_mean=0.9083333333333333; mp_subject_verb_agreement_plural_mean=0.9666666666666667; mp_determiner_noun_agreement_mean=0.8166666666666668; mp_irregular_past_mean=1.0
  T6[2] | vocab=512; bytes_per_token=2.410593339881614; tokens_per_word=2.079882753314716; ctx_tokens=424.0; params_embedding=196992.0; params_non_embedding=14162304.0; train_flops=1.560597268267008e+16; val_bpb_mean=0.5606376892703318; val_bpb_sd=0.002079757394676226; mp_all_mean=0.8891242937853109; mp_all_sd=0.029229098992337384; n_seeds=3; mp_subject_verb_agreement_singular_mean=0.7933333333333333; mp_subject_verb_agreement_plural_mean=0.9899999999999999; mp_determiner_noun_agreement_mean=0.85; mp_irregular_past_mean=1.0
  T6[3] | vocab=768; bytes_per_token=2.8895688447462256; tokens_per_word=1.73512097557081; ctx_tokens=352.0; params_embedding=295296.0; params_non_embedding=14162304.0; train_flops=1.29172630929408e+16; val_bpb_mean=0.5512907961115897; val_bpb_sd=0.0010226931202805083; mp_all_mean=0.8799435028248587; mp_all_sd=0.07401116466110982; n_seeds=3; mp_subject_verb_agreement_singular_mean=0.7933333333333333; mp_subject_verb_agreement_plural_mean=0.9616666666666666; mp_determiner_noun_agreement_mean=0.8722222222222222; mp_irregular_past_mean=1.0
  T6[4] | vocab=1024; bytes_per_token=3.165708732285685; tokens_per_word=1.583769050431589; ctx_tokens=320.0; params_embedding=393600.0; params_non_embedding=14162304.0; train_flops=1.178688323321856e+16; val_bpb_mean=0.5460106494254117; val_bpb_sd=0.0001778703445224515; mp_all_mean=0.8990112994350282; mp_all_sd=0.07401116466110988; n_seeds=3; mp_subject_verb_agreement_singular_mean=0.8116666666666666; mp_subject_verb_agreement_plural_mean=0.9983333333333334; mp_determiner_noun_agreement_mean=0.8388888888888889; mp_irregular_past_mean=1.0
  T6[5] | vocab=4096; bytes_per_token=3.962679221179897; tokens_per_word=1.2652428402676088; ctx_tokens=256.0; params_embedding=1573248.0; params_non_embedding=14162304.0; train_flops=1.0008179383468032e+16; val_bpb_mean=0.528462391737498; val_bpb_sd=0.0010521012093391913; mp_all_mean=0.9548022598870057; mp_all_sd=0.022851256620569877; n_seeds=3; mp_subject_verb_agreement_singular_mean=0.94; mp_subject_verb_agreement_plural_mean=0.9700000000000001; mp_determiner_noun_agreement_mean=0.9444444444444443; mp_irregular_past_mean=1.0
  runs[0] | vocab=256; seed=0; bytes_per_token=1.0; tokens_per_word=5.013751512875088; ctx_tokens=1024; params_embedding=98688; params_non_embedding=14162304; train_flops=41772598752706560; val_bpb=0.5965823017595128; mp_determiner_noun_agreement=0.7666666666666667; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.99; mp_subject_verb_agreement_singular=0.84; mp_all=0.8983050847457628; mp_perbyte_determiner_noun_agreement=0.8333333333333334; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.93; mp_perbyte_subject_verb_agreement_singular=0.94; mp_perbyte_all=0.923728813559322
  runs[1] | vocab=256; seed=1; bytes_per_token=1.0; tokens_per_word=5.013751512875088; ctx_tokens=1024; params_embedding=98688; params_non_embedding=14162304; train_flops=41772598752706560; val_bpb=0.5962898448863188; mp_determiner_noun_agreement=0.75; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.955; mp_subject_verb_agreement_singular=0.955; mp_all=0.9300847457627118; mp_perbyte_determiner_noun_agreement=0.7833333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.895; mp_perbyte_subject_verb_agreement_singular=0.99; mp_perbyte_all=0.923728813559322
  runs[2] | vocab=256; seed=2; bytes_per_token=1.0; tokens_per_word=5.013751512875088; ctx_tokens=1024; params_embedding=98688; params_non_embedding=14162304; train_flops=41772598752706560; val_bpb=0.5979782771614769; mp_determiner_noun_agreement=0.8; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.955; mp_subject_verb_agreement_singular=0.7; mp_all=0.8283898305084746; mp_perbyte_determiner_noun_agreement=0.7666666666666667; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.72; mp_perbyte_subject_verb_agreement_singular=0.9; mp_perbyte_all=0.809322033898305
  runs[3] | vocab=384; seed=0; bytes_per_token=1.9775921626158444; tokens_per_word=2.535280836794574; ctx_tokens=520; params_embedding=147840; params_non_embedding=14162304; train_flops=19315848774942720; val_bpb=0.5707841386797021; mp_determiner_noun_agreement=0.8; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.985; mp_subject_verb_agreement_singular=0.945; mp_all=0.9449152542372882; mp_perbyte_determiner_noun_agreement=0.8166666666666667; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.905; mp_perbyte_subject_verb_agreement_singular=0.98; mp_perbyte_all=0.9279661016949152
  runs[4] | vocab=384; seed=1; bytes_per_token=1.9775921626158444; tokens_per_word=2.535280836794574; ctx_tokens=520; params_embedding=147840; params_non_embedding=14162304; train_flops=19315848774942720; val_bpb=0.5685670028100107; mp_determiner_noun_agreement=0.7833333333333333; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=1.0; mp_subject_verb_agreement_singular=0.97; mp_all=0.9597457627118644; mp_perbyte_determiner_noun_agreement=0.7833333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.975; mp_perbyte_subject_verb_agreement_singular=0.995; mp_perbyte_all=0.9597457627118644
  runs[5] | vocab=384; seed=2; bytes_per_token=1.9775921626158444; tokens_per_word=2.535280836794574; ctx_tokens=520; params_embedding=147840; params_non_embedding=14162304; train_flops=19315848774942720; val_bpb=0.5693422762909293; mp_determiner_noun_agreement=0.8666666666666667; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.915; mp_subject_verb_agreement_singular=0.81; mp_all=0.8665254237288136; mp_perbyte_determiner_noun_agreement=0.8666666666666667; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.865; mp_perbyte_subject_verb_agreement_singular=0.88; mp_perbyte_all=0.875
  runs[6] | vocab=512; seed=0; bytes_per_token=2.410593339881614; tokens_per_word=2.079882753314716; ctx_tokens=424; params_embedding=196992; params_non_embedding=14162304; train_flops=15605972682670080; val_bpb=0.5582516786426197; mp_determiner_noun_agreement=0.9166666666666666; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.995; mp_subject_verb_agreement_singular=0.69; mp_all=0.8559322033898306; mp_perbyte_determiner_noun_agreement=0.95; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.97; mp_perbyte_subject_verb_agreement_singular=0.82; mp_perbyte_all=0.9046610169491526
  runs[7] | vocab=512; seed=1; bytes_per_token=2.410593339881614; tokens_per_word=2.079882753314716; ctx_tokens=424; params_embedding=196992; params_non_embedding=14162304; train_flops=15605972682670080; val_bpb=0.5615948857971498; mp_determiner_noun_agreement=0.8666666666666667; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.975; mp_subject_verb_agreement_singular=0.83; mp_all=0.9004237288135594; mp_perbyte_determiner_noun_agreement=0.9333333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.86; mp_perbyte_subject_verb_agreement_singular=0.91; mp_perbyte_all=0.8940677966101694
  runs[8] | vocab=512; seed=2; bytes_per_token=2.410593339881614; tokens_per_word=2.079882753314716; ctx_tokens=424; params_embedding=196992; params_non_embedding=14162304; train_flops=15605972682670080; val_bpb=0.5620665033712258; mp_determiner_noun_agreement=0.7666666666666667; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=1.0; mp_subject_verb_agreement_singular=0.86; mp_all=0.9110169491525424; mp_perbyte_determiner_noun_agreement=0.8; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.995; mp_perbyte_subject_verb_agreement_singular=0.95; mp_perbyte_all=0.951271186440678
  runs[9] | vocab=768; seed=0; bytes_per_token=2.8895688447462256; tokens_per_word=1.73512097557081; ctx_tokens=352; params_embedding=295296; params_non_embedding=14162304; train_flops=12917263092940800; val_bpb=0.5507297846697937; mp_determiner_noun_agreement=0.95; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.995; mp_subject_verb_agreement_singular=0.84; mp_all=0.923728813559322; mp_perbyte_determiner_noun_agreement=0.9833333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.92; mp_perbyte_subject_verb_agreement_singular=0.915; mp_perbyte_all=0.9279661016949152
  runs[10] | vocab=768; seed=1; bytes_per_token=2.8895688447462256; tokens_per_word=1.73512097557081; ctx_tokens=352; params_embedding=295296; params_non_embedding=14162304; train_flops=12917263092940800; val_bpb=0.5506713847030253; mp_determiner_noun_agreement=0.7166666666666667; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.995; mp_subject_verb_agreement_singular=0.905; mp_all=0.9216101694915254; mp_perbyte_determiner_noun_agreement=0.7666666666666667; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.945; mp_perbyte_subject_verb_agreement_singular=0.945; mp_perbyte_all=0.923728813559322
  runs[11] | vocab=768; seed=2; bytes_per_token=2.8895688447462256; tokens_per_word=1.73512097557081; ctx_tokens=352; params_embedding=295296; params_non_embedding=14162304; train_flops=12917263092940800; val_bpb=0.5524712189619498; mp_determiner_noun_agreement=0.95; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.895; mp_subject_verb_agreement_singular=0.635; mp_all=0.7944915254237288; mp_perbyte_determiner_noun_agreement=0.9333333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.78; mp_perbyte_subject_verb_agreement_singular=0.845; mp_perbyte_all=0.8326271186440678
  runs[12] | vocab=1024; seed=0; bytes_per_token=3.165708732285685; tokens_per_word=1.583769050431589; ctx_tokens=320; params_embedding=393600; params_non_embedding=14162304; train_flops=11786883233218560; val_bpb=0.5459755093459301; mp_determiner_noun_agreement=0.8166666666666667; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=1.0; mp_subject_verb_agreement_singular=0.915; mp_all=0.940677966101695; mp_perbyte_determiner_noun_agreement=0.9; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.97; mp_perbyte_subject_verb_agreement_singular=0.98; mp_perbyte_all=0.9661016949152542
  runs[13] | vocab=1024; seed=1; bytes_per_token=3.165708732285685; tokens_per_word=1.583769050431589; ctx_tokens=320; params_embedding=393600; params_non_embedding=14162304; train_flops=11786883233218560; val_bpb=0.5462034671201185; mp_determiner_noun_agreement=0.85; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.995; mp_subject_verb_agreement_singular=0.61; mp_all=0.8135593220338984; mp_perbyte_determiner_noun_agreement=0.9; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.985; mp_perbyte_subject_verb_agreement_singular=0.81; mp_perbyte_all=0.9004237288135594
  runs[14] | vocab=1024; seed=2; bytes_per_token=3.165708732285685; tokens_per_word=1.583769050431589; ctx_tokens=320; params_embedding=393600; params_non_embedding=14162304; train_flops=11786883233218560; val_bpb=0.5458529718101867; mp_determiner_noun_agreement=0.85; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=1.0; mp_subject_verb_agreement_singular=0.91; mp_all=0.9427966101694916; mp_perbyte_determiner_noun_agreement=0.7833333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.99; mp_perbyte_subject_verb_agreement_singular=1.0; mp_perbyte_all=0.9682203389830508
  runs[15] | vocab=4096; seed=0; bytes_per_token=3.962679221179897; tokens_per_word=1.2652428402676088; ctx_tokens=256; params_embedding=1573248; params_non_embedding=14162304; train_flops=10008179383468032; val_bpb=0.5295893968700158; mp_determiner_noun_agreement=0.95; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.98; mp_subject_verb_agreement_singular=0.89; mp_all=0.9385593220338984; mp_perbyte_determiner_noun_agreement=0.9833333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.93; mp_perbyte_subject_verb_agreement_singular=0.955; mp_perbyte_all=0.9491525423728814
  runs[16] | vocab=4096; seed=1; bytes_per_token=3.962679221179897; tokens_per_word=1.2652428402676088; ctx_tokens=256; params_embedding=1573248; params_non_embedding=14162304; train_flops=10008179383468032; val_bpb=0.5275060641107455; mp_determiner_noun_agreement=0.9166666666666666; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.935; mp_subject_verb_agreement_singular=0.96; mp_all=0.9449152542372882; mp_perbyte_determiner_noun_agreement=0.9333333333333333; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.805; mp_perbyte_subject_verb_agreement_singular=0.995; mp_perbyte_all=0.9067796610169492
  runs[17] | vocab=4096; seed=2; bytes_per_token=3.962679221179897; tokens_per_word=1.2652428402676088; ctx_tokens=256; params_embedding=1573248; params_non_embedding=14162304; train_flops=10008179383468032; val_bpb=0.5282917142317326; mp_determiner_noun_agreement=0.9666666666666667; mp_irregular_past=1.0; mp_subject_verb_agreement_plural=0.995; mp_subject_verb_agreement_singular=0.97; mp_all=0.9809322033898306; mp_perbyte_determiner_noun_agreement=1.0; mp_perbyte_irregular_past=1.0; mp_perbyte_subject_verb_agreement_plural=0.95; mp_perbyte_subject_verb_agreement_singular=1.0; mp_perbyte_all=0.9788135593220338
  spearman_tokens_per_word_vs_bpb | rho=1.0; p=0.0
  spearman_tokens_per_word_vs_mp | rho=-0.4285714285714286; p=0.3965014577259473
  equal_flops | flops=10008179383468032
  equal_flops.by_vocab.256 | bpb_mean=0.7920808382746287; bpb_sd=0.0017969276590197346; mp_mean=0.7378928572763949
  equal_flops.by_vocab.384 | bpb_mean=0.6364129670600183; bpb_sd=0.001623577222464179; mp_mean=0.8607517965327052
  equal_flops.by_vocab.512 | bpb_mean=0.5993913088386774; bpb_sd=0.001747711246599841; mp_mean=0.7841414179552165
  equal_flops.by_vocab.768 | bpb_mean=0.5689910150316818; bpb_sd=0.0007308908641859406; mp_mean=0.857513725904715
  equal_flops.by_vocab.1024 | bpb_mean=0.5545248804515381; bpb_sd=0.0002436611682812971; mp_mean=0.8803883793913898
  equal_flops.by_vocab.4096 | bpb_mean=0.5267596360553096; bpb_sd=0.0011260266985855128; mp_mean=0.9548022598870057
Result entry: 2026-10-15 — Step 3b (GATE 3): MDL and erasure probes on the 18 E5 tiny models [RESULTS.md 438-467, `baf4f09` 2026-10-15 00:56:53 +0530]
Source files: results/e05_pretrain/analysis.json

### E9: Tokenizer-optimal reversible romanization
Registered: no separate registration entry (see the result entry)
Models run: not recorded as a column or key in the result files
Forms/conditions run: itrans, native, e09:o200k|free, e09:qwen3|free, e09:gemma4|free, e09:o200k|lower, e09:qwen3|lower, e09:gemma4|lower, e09:qwen3.5|free, e09:qwen3.5|lower, e09:universal|free, e09:universal|lower; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [e09_romanize/savings.json] (167 records; CAP 60):
  (top) | n_sentences=2009
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="native"; tokens=103948; vs_native=1.0; vs_itrans=0.8226532760353601
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="itrans"; tokens=126357; vs_native=1.2155789433178128; vs_itrans=1.0
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:o200k|free"; tokens=120263; vs_native=1.1569534767383691; vs_itrans=0.9517715678593193
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:o200k|lower"; tokens=125929; vs_native=1.2114614999807596; vs_itrans=0.9966127717498833
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:gemma4|free"; tokens=123303; vs_native=1.1861988686651017; vs_itrans=0.9758303853367839
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:gemma4|lower"; tokens=127113; vs_native=1.222851810520645; vs_itrans=1.00598304803058
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:qwen3.5|free"; tokens=124366; vs_native=1.1964251356447455; vs_itrans=0.9842430573691999
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:qwen3.5|lower"; tokens=125981; vs_native=1.2119617501058222; vs_itrans=0.997024304154103
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:qwen3|free"; tokens=124366; vs_native=1.1964251356447455; vs_itrans=0.9842430573691999
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:qwen3|lower"; tokens=126517; vs_native=1.2171181744718513; vs_itrans=1.0012662535514456
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:universal|free"; tokens=122916; vs_native=1.182475853311271; vs_itrans=0.9727676345592251
  rows[tokenizer=o200k (GPT-4o)] | tokenizer="o200k (GPT-4o)"; form="e09:universal|lower"; tokens=127036; vs_native=1.222111055527764; vs_itrans=1.005373663508947
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="native"; tokens=469817; vs_native=1.0; vs_itrans=3.431475232627781
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="itrans"; tokens=136914; vs_native=0.2914198507078288; vs_itrans=1.0
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:o200k|free"; tokens=135326; vs_native=0.2880398112456552; vs_itrans=0.9884014783002468
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:o200k|lower"; tokens=138856; vs_native=0.2955533750375146; vs_itrans=1.0141840863607812
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:gemma4|free"; tokens=135302; vs_native=0.2879887275258239; vs_itrans=0.9882261857808551
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:gemma4|lower"; tokens=138510; vs_native=0.2948169180766128; vs_itrans=1.0116569525395505
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:qwen3.5|free"; tokens=136589; vs_native=0.2907280920017794; vs_itrans=0.9976262471332369
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:qwen3.5|lower"; tokens=137259; vs_native=0.29215417918040426; vs_itrans=1.002519829966256
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:qwen3|free"; tokens=133694; vs_native=0.2845661182971242; vs_itrans=0.9764815869816089
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:qwen3|lower"; tokens=137196; vs_native=0.29202008441584704; vs_itrans=1.0020596871028529
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:universal|free"; tokens=135439; vs_native=0.2882803304265278; vs_itrans=0.989226813912383
  rows[tokenizer=cl100k (GPT-4)] | tokenizer="cl100k (GPT-4)"; form="e09:universal|lower"; tokens=138197; vs_native=0.2941507012304791; vs_itrans=1.0093708459324833
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="native"; tokens=717138; vs_native=1.0; vs_itrans=5.016529677171138
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="itrans"; tokens=142955; vs_native=0.19934099155253243; vs_itrans=1.0
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:o200k|free"; tokens=145939; vs_native=0.203501975909797; vs_itrans=1.0208737015144627
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:o200k|lower"; tokens=152777; vs_native=0.2130371002512766; vs_itrans=1.068706935749012
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:gemma4|free"; tokens=141897; vs_native=0.19786568275562025; vs_itrans=0.9925990696372985
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:gemma4|lower"; tokens=147895; vs_native=0.20622948442280287; vs_itrans=1.0345563289146935
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:qwen3.5|free"; tokens=148340; vs_native=0.20685000655382924; vs_itrans=1.0376691966003289
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:qwen3.5|lower"; tokens=150984; vs_native=0.21053688411435456; vs_itrans=1.0561645272988003
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:qwen3|free"; tokens=144424; vs_native=0.20138941180079706; vs_itrans=1.0102759609667378
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:qwen3|lower"; tokens=151223; vs_native=0.21087015330382716; vs_itrans=1.0578363820782763
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:universal|free"; tokens=141283; vs_native=0.19700950165797937; vs_itrans=0.9883040117519499
  rows[tokenizer=r50k (GPT-3)] | tokenizer="r50k (GPT-3)"; form="e09:universal|lower"; tokens=147565; vs_native=0.20576932194361475; vs_itrans=1.0322479101815256
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="native"; tokens=102578; vs_native=1.0; vs_itrans=0.8011402686660418
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="itrans"; tokens=128040; vs_native=1.2482208660726473; vs_itrans=1.0
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:o200k|free"; tokens=130316; vs_native=1.2704088595995242; vs_itrans=1.0177756950952828
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:o200k|lower"; tokens=137033; vs_native=1.335890736805163; vs_itrans=1.0702358637925649
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:gemma4|free"; tokens=125055; vs_native=1.2191210590964925; vs_itrans=0.9766869728209935
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:gemma4|lower"; tokens=130777; vs_native=1.2749030006434128; vs_itrans=1.0213761324586066
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:qwen3.5|free"; tokens=132182; vs_native=1.2885998947142663; vs_itrans=1.0323492658544204
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:qwen3.5|lower"; tokens=134082; vs_native=1.3071223849168438; vs_itrans=1.0471883786316776
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:qwen3|free"; tokens=130704; vs_native=1.2741913470724717; vs_itrans=1.0208059981255857
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:qwen3|lower"; tokens=135220; vs_native=1.3182163816802823; vs_itrans=1.056076226179319
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:universal|free"; tokens=125176; vs_native=1.220300649262025; vs_itrans=0.9776319900031241
  rows[tokenizer=Gemma 4] | tokenizer="Gemma 4"; form="e09:universal|lower"; tokens=130787; vs_native=1.2750004874339527; vs_itrans=1.0214542330521712
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="native"; tokens=168009; vs_native=1.0; vs_itrans=1.2607609185051778
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="itrans"; tokens=133260; vs_native=0.7931717943681589; vs_itrans=1.0
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:o200k|free"; tokens=130752; vs_native=0.7782440226416442; vs_itrans=0.9811796488068437
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:o200k|lower"; tokens=133992; vs_native=0.7975287038194382; vs_itrans=1.0054930211616389
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:gemma4|free"; tokens=130534; vs_native=0.7769464731056074; vs_itrans=0.979543749061984
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:gemma4|lower"; tokens=133347; vs_native=0.7936896237701552; vs_itrans=1.00065285907249
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:qwen3.5|free"; tokens=131884; vs_native=0.7849817569296883; vs_itrans=0.9896743208764821
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:qwen3.5|lower"; tokens=132333; vs_native=0.7876542328089566; vs_itrans=0.9930436740207114
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:qwen3|free"; tokens=131117; vs_native=0.780416525305192; vs_itrans=0.9839186552603932
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:qwen3|lower"; tokens=133315; vs_native=0.793499157783214; vs_itrans=1.00041272699985
  rows[tokenizer=Qwen 3.5-3.8] | tokenizer="Qwen 3.5-3.8"; form="e09:universal|free"; tokens=130955; vs_native=0.7794522912463023; vs_itrans=0.9827029866426534
Result entry: 2026-10-07 — E9 GATE: tokenizer-optimal reversible romanization (token savings only) [RESULTS.md 110-132, `76c8073` 2026-10-07 16:40:03 +0530]
Source files: results/e09_romanize/savings.json

### E0: Gate, tokens per word, natural romanization checks, Step 0
Registered: no separate registration entry (see the result entry)
Models run: sarvam-1, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, openai/gpt-oss-120b, gemini-3.5-flash-lite
Forms/conditions run: itrans, native, english; tasks/measures: xnli, sentiment; seeds: 0
Table [e00_gate/summary.json] (32 records):
  summary[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="sentiment"; form="english"; n=200; chance=0.5; acc=0.985; acc_ci_low=0.965; acc_ci_high=1.0; acc_calibrated=0.995; acc_cal_ci_low=0.985; acc_cal_ci_high=1.0; pred_majority_share=0.515; mean_prompt_tokens=44.47
  summary[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="sentiment"; form="itrans"; n=200; chance=0.5; acc=0.495; acc_ci_low=0.425; acc_ci_high=0.565; acc_calibrated=0.515; acc_cal_ci_low=0.445; acc_cal_ci_high=0.585; pred_majority_share=0.995; mean_prompt_tokens=88.2
  summary[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="sentiment"; form="native"; n=200; chance=0.5; acc=0.705; acc_ci_low=0.64; acc_ci_high=0.765; acc_calibrated=0.73; acc_cal_ci_low=0.665; acc_cal_ci_high=0.79; pred_majority_share=0.625; mean_prompt_tokens=221.135
  summary[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="xnli"; form="english"; n=200; chance=0.3333333333333333; acc=0.795; acc_ci_low=0.735; acc_ci_high=0.85; acc_calibrated=0.835; acc_cal_ci_low=0.78; acc_cal_ci_high=0.885; pred_majority_share=0.45; mean_prompt_tokens=62.14
  summary[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="xnli"; form="itrans"; n=200; chance=0.3333333333333333; acc=0.375; acc_ci_low=0.31; acc_ci_high=0.445; acc_calibrated=0.43; acc_cal_ci_low=0.36; acc_cal_ci_high=0.5; pred_majority_share=0.845; mean_prompt_tokens=111.645
  summary[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="xnli"; form="native"; n=200; chance=0.3333333333333333; acc=0.51; acc_ci_low=0.445; acc_ci_high=0.58; acc_calibrated=0.465; acc_cal_ci_low=0.395; acc_cal_ci_high=0.535; pred_majority_share=0.48; mean_prompt_tokens=264.68
  summary[model=qwen3-1.7b] | model="qwen3-1.7b"; task="sentiment"; form="english"; n=200; chance=0.5; acc=0.985; acc_ci_low=0.965; acc_ci_high=1.0; acc_calibrated=0.98; acc_cal_ci_low=0.96; acc_cal_ci_high=0.995; pred_majority_share=0.515; mean_prompt_tokens=44.47
  summary[model=qwen3-1.7b] | model="qwen3-1.7b"; task="sentiment"; form="itrans"; n=200; chance=0.5; acc=0.58; acc_ci_low=0.51; acc_ci_high=0.645; acc_calibrated=0.555; acc_cal_ci_low=0.485; acc_cal_ci_high=0.625; pred_majority_share=0.68; mean_prompt_tokens=88.2
  summary[model=qwen3-1.7b] | model="qwen3-1.7b"; task="sentiment"; form="native"; n=200; chance=0.5; acc=0.865; acc_ci_low=0.815; acc_ci_high=0.91; acc_calibrated=0.87; acc_cal_ci_low=0.825; acc_cal_ci_high=0.915; pred_majority_share=0.525; mean_prompt_tokens=221.135
  summary[model=qwen3-1.7b] | model="qwen3-1.7b"; task="xnli"; form="english"; n=200; chance=0.3333333333333333; acc=0.615; acc_ci_low=0.545; acc_ci_high=0.68; acc_calibrated=0.64; acc_cal_ci_low=0.575; acc_cal_ci_high=0.705; pred_majority_share=0.53; mean_prompt_tokens=62.14
  summary[model=qwen3-1.7b] | model="qwen3-1.7b"; task="xnli"; form="itrans"; n=200; chance=0.3333333333333333; acc=0.37; acc_ci_low=0.305; acc_ci_high=0.44; acc_calibrated=0.405; acc_cal_ci_low=0.335; acc_cal_ci_high=0.475; pred_majority_share=0.8; mean_prompt_tokens=111.645
  summary[model=qwen3-1.7b] | model="qwen3-1.7b"; task="xnli"; form="native"; n=200; chance=0.3333333333333333; acc=0.43; acc_ci_low=0.36; acc_ci_high=0.5; acc_calibrated=0.45; acc_cal_ci_low=0.38; acc_cal_ci_high=0.52; pred_majority_share=0.61; mean_prompt_tokens=264.68
  summary[model=qwen3.5-2b] | model="qwen3.5-2b"; task="sentiment"; form="english"; n=200; chance=0.5; acc=0.975; acc_ci_low=0.95; acc_ci_high=0.995; acc_calibrated=0.975; acc_cal_ci_low=0.95; acc_cal_ci_high=0.995; pred_majority_share=0.505; mean_prompt_tokens=46.23
  summary[model=qwen3.5-2b] | model="qwen3.5-2b"; task="sentiment"; form="itrans"; n=200; chance=0.5; acc=0.675; acc_ci_low=0.61; acc_ci_high=0.74; acc_calibrated=0.7; acc_cal_ci_low=0.635; acc_cal_ci_high=0.76; pred_majority_share=0.665; mean_prompt_tokens=87.86
  summary[model=qwen3.5-2b] | model="qwen3.5-2b"; task="sentiment"; form="native"; n=200; chance=0.5; acc=0.785; acc_ci_low=0.725; acc_ci_high=0.84; acc_calibrated=0.9; acc_cal_ci_low=0.855; acc_cal_ci_high=0.94; pred_majority_share=0.705; mean_prompt_tokens=107.305
  summary[model=qwen3.5-2b] | model="qwen3.5-2b"; task="xnli"; form="english"; n=200; chance=0.3333333333333333; acc=0.43; acc_ci_low=0.36; acc_ci_high=0.5; acc_calibrated=0.62; acc_cal_ci_low=0.555; acc_cal_ci_high=0.685; pred_majority_share=0.89; mean_prompt_tokens=64.875
  summary[model=qwen3.5-2b] | model="qwen3.5-2b"; task="xnli"; form="itrans"; n=200; chance=0.3333333333333333; acc=0.34; acc_ci_low=0.275; acc_ci_high=0.405; acc_calibrated=0.355; acc_cal_ci_low=0.29; acc_cal_ci_high=0.42; pred_majority_share=0.995; mean_prompt_tokens=112.11
  summary[model=qwen3.5-2b] | model="qwen3.5-2b"; task="xnli"; form="native"; n=200; chance=0.3333333333333333; acc=0.34; acc_ci_low=0.275; acc_ci_high=0.405; acc_calibrated=0.405; acc_cal_ci_low=0.34; acc_cal_ci_high=0.475; pred_majority_share=0.995; mean_prompt_tokens=134.015
  summary[model=sarvam-1] | model="sarvam-1"; task="sentiment"; form="english"; n=200; chance=0.5; acc=0.955; acc_ci_low=0.925; acc_ci_high=0.98; acc_calibrated=0.97; acc_cal_ci_low=0.945; acc_cal_ci_high=0.99; pred_majority_share=0.505; mean_prompt_tokens=54.785
  summary[model=sarvam-1] | model="sarvam-1"; task="sentiment"; form="itrans"; n=200; chance=0.5; acc=0.8; acc_ci_low=0.745; acc_ci_high=0.855; acc_calibrated=0.82; acc_cal_ci_low=0.765; acc_cal_ci_high=0.87; pred_majority_share=0.64; mean_prompt_tokens=111.37
  summary[model=sarvam-1] | model="sarvam-1"; task="sentiment"; form="native"; n=200; chance=0.5; acc=0.98; acc_ci_low=0.96; acc_ci_high=0.995; acc_calibrated=0.96; acc_cal_ci_low=0.93; acc_cal_ci_high=0.985; pred_majority_share=0.52; mean_prompt_tokens=60.74
  summary[model=sarvam-1] | model="sarvam-1"; task="xnli"; form="english"; n=200; chance=0.3333333333333333; acc=0.575; acc_ci_low=0.505; acc_ci_high=0.645; acc_calibrated=0.51; acc_cal_ci_low=0.44; acc_cal_ci_high=0.58; pred_majority_share=0.555; mean_prompt_tokens=78.505
  summary[model=sarvam-1] | model="sarvam-1"; task="xnli"; form="itrans"; n=200; chance=0.3333333333333333; acc=0.405; acc_ci_low=0.335; acc_ci_high=0.475; acc_calibrated=0.445; acc_cal_ci_low=0.375; acc_cal_ci_high=0.515; pred_majority_share=0.67; mean_prompt_tokens=142.1
  summary[model=sarvam-1] | model="sarvam-1"; task="xnli"; form="native"; n=200; chance=0.3333333333333333; acc=0.52; acc_ci_low=0.45; acc_ci_high=0.59; acc_calibrated=0.5; acc_cal_ci_low=0.43; acc_cal_ci_high=0.57; pred_majority_share=0.62; mean_prompt_tokens=80.14
  gate[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; passes=true
  gate[model=qwen2.5-1.5b].by_task | sentiment=true; xnli=true
  gate[model=qwen3-1.7b] | model="qwen3-1.7b"; passes=true
  gate[model=qwen3-1.7b].by_task | sentiment=true; xnli=false
  gate[model=qwen3.5-2b] | model="qwen3.5-2b"; passes=true
  gate[model=qwen3.5-2b].by_task | sentiment=true; xnli=false
  gate[model=sarvam-1] | model="sarvam-1"; passes=true
  gate[model=sarvam-1].by_task | sentiment=true; xnli=true
Result entry: 2026-10-08 — E0 GATE (4 of 5 models; Gemma 4 E2B not run) [RESULTS.md 205-231, `22013f7` 2026-10-08 01:52:43 +0530]
Source files: results/e00_gate/summary.json

### M1: Detokenization layer (M1) on pretrained models
Registered: PRE-REGISTRATION — M1 detokenization layer (written 2026-10-07, before any M1 run) [RESULTS.md 144-170, `8380e09` 2026-10-07 16:49:31 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: 4, itrans, native, english; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [m14_full/gate2/verdicts.json] (31 records):
  verdicts | qwen_outcome_H1_vs_H2="H1"
  verdicts.H1 | holds=true
  verdicts.H1.per_qwen_model.qwen2.5-1.5b | detok_not_later=true; larger_lag=false; never_reaches_native_max_retrieval=true; holds=true
  verdicts.H1.per_qwen_model.qwen3.5-2b | detok_not_later=true; larger_lag=false; never_reaches_native_max_retrieval=true; holds=true
  verdicts.H2 | holds=false
  verdicts.H2.mdl_sign_ci | qwen2.5-1.5b=-1; qwen3.5-2b=0
  verdicts.H3 | n_models_ci_excluding_0_in_expected_direction=3; verdict="not supported"
  verdicts.H3.expected_sign_from_tpw | qwen2.5-1.5b=-1; qwen3.5-2b=-1; sarvam-1=1; gemma4-e2b=1
  verdicts.H3.mdl_point_sign | qwen2.5-1.5b=-1; qwen3.5-2b=0; sarvam-1=1; gemma4-e2b=1
  verdicts.H3.mdl_ci_sign | qwen2.5-1.5b=-1; qwen3.5-2b=0; sarvam-1=1; gemma4-e2b=1
  verdicts.original_2026_10_07.patchscopes_primary | testable=false; verdict="not testable"
  verdicts.original_2026_10_07.patchscopes_primary.favors | qwen2.5-1.5b="not testable (< 30 words identified in both forms)"; qwen3.5-2b="not testable (< 30 words identified in both forms)"; sarvam-1="not testable (< 30 words identified in both forms)"; gemma4-e2b="not testable (< 30 words identified in both forms)"
  verdicts.original_2026_10_07.mdl_alongside | verdict="H-frag"
  verdicts.original_2026_10_07.mdl_alongside.favors | qwen2.5-1.5b="ITRANS-earlier"; qwen3.5-2b="no difference"; sarvam-1="native-earlier"; gemma4-e2b="native-earlier"
  verdicts.method_agreement[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; mdl=-1; probe=0; agree=false
  verdicts.method_agreement[model=qwen3.5-2b] | model="qwen3.5-2b"; mdl=0; probe=0; agree=true
  verdicts.method_agreement[model=sarvam-1] | model="sarvam-1"; mdl=1; probe=1; agree=true
  verdicts.method_agreement[model=gemma4-e2b] | model="gemma4-e2b"; mdl=1; probe=0; agree=false
  verdicts.notes | ps_min_rate="post hoc: Patchscopes detok computed only where identification rate >= 0.5"; never_reaches="operationalized as the paired CI of (native max - ITRANS max retrieval) above 0; chosen after the max retrieval values were printed by the run log"
  curves.qwen2.5-1.5b | L=28
  curves.qwen2.5-1.5b.mdl | english=[29 values]; native=[29 values]; itrans=[29 values]
  curves.qwen2.5-1.5b.retrieval | native=[29 values]; itrans=[29 values]
  curves.qwen3.5-2b | L=24
  curves.qwen3.5-2b.mdl | english=[25 values]; native=[25 values]; itrans=[25 values]
  curves.qwen3.5-2b.retrieval | native=[25 values]; itrans=[25 values]
  curves.sarvam-1 | L=28
  curves.sarvam-1.mdl | english=[29 values]; native=[29 values]; itrans=[29 values]
  curves.sarvam-1.retrieval | native=[29 values]; itrans=[29 values]
  curves.gemma4-e2b | L=35
  curves.gemma4-e2b.mdl | english=[36 values]; native=[36 values]; itrans=[36 values]
  curves.gemma4-e2b.retrieval | native=[36 values]; itrans=[36 values]
Result entry: 2026-10-15 — GATE 2: full M1/M4 run (Qwen2.5-1.5B, Qwen3.5-2B, Sarvam-1, Gemma 4 E2B; English, native, ITRANS) [RESULTS.md 601-680, `051f261` 2026-10-15 21:21:07 +0530]
Source files: results/m14_full/gate2/verdicts.json

### S3: Step 3 and 3b: word-identity, MDL and erasure probes on the E5 tiny models
Registered: PRE-REGISTRATION — Step 3: M1 word-identity probes on the E5 tiny models (written 2026-10-14, before any run) [RESULTS.md 289-308, `81d420c` 2026-10-14 22:16:36 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2
Table [m1_tiny_mdl/analysis.json] (9 records):
  summary[0] | vocab=256; mdl_detok_mean=2.0; mdl_detok_std=0.0; mdl_ci_low_mean=2.0; mdl_ci_low_std=0.0; mdl_ci_high_mean=2.0; mdl_ci_high_std=0.0; compression_layer0_mean=1.6565086381181933; compression_layer0_std=0.0001852934407456983; compression_max_mean=21.5984974012688; compression_max_std=0.22202966495282433; erasure1_layer_mean=NaN; erasure1_layer_std=NaN; erasure1_magnitude_mean=0.000462949275970459; erasure1_magnitude_std=0.0005782320503617322; erasure1_peak_mean=1.6666666666666667; erasure1_peak_std=0.5773502691896257; erasure1_n_test_mean=3600.0; erasure1_n_test_std=0.0; erasure2_layer_mean=NaN; erasure2_layer_std=NaN; erasure2_magnitude_mean=0.0008333126703898112; erasure2_magnitude_std=0.0002777874475085965; tokens_per_word_probed_mean=6.656666666666666; tokens_per_word_probed_std=0.0; tokens_per_word_valid_mean=5.013751512875088; tokens_per_word_valid_std=0.0; bpb_gap_vs_4096_mean=0.06848774953160486; bpb_gap_vs_4096_std=0.0
  summary[1] | vocab=384; mdl_detok_mean=1.0; mdl_detok_std=0.0; mdl_ci_low_mean=1.0; mdl_ci_low_std=0.0; mdl_ci_high_mean=1.0; mdl_ci_high_std=0.0; compression_layer0_mean=2.21024686349991; compression_layer0_std=1.5111685129387032e-05; compression_max_mean=21.55662096577937; compression_max_std=0.05522984899494173; erasure1_layer_mean=NaN; erasure1_layer_std=NaN; erasure1_magnitude_mean=0.004907369613647461; erasure1_magnitude_std=0.0019510555025530534; erasure1_peak_mean=1.0; erasure1_peak_std=0.0; erasure1_n_test_mean=3600.0; erasure1_n_test_std=0.0; erasure2_layer_mean=NaN; erasure2_layer_std=NaN; erasure2_magnitude_mean=0.009074032306671143; erasure2_magnitude_std=0.0016276350381407814; tokens_per_word_probed_mean=4.286666666666667; tokens_per_word_probed_std=0.0; tokens_per_word_valid_mean=2.535280836794574; tokens_per_word_valid_std=0.0; bpb_gap_vs_4096_mean=0.04110208085604938; bpb_gap_vs_4096_std=0.0
  summary[2] | vocab=512; mdl_detok_mean=1.0; mdl_detok_std=0.0; mdl_ci_low_mean=1.0; mdl_ci_low_std=0.0; mdl_ci_high_mean=1.0; mdl_ci_high_std=0.0; compression_layer0_mean=2.509778251539322; compression_layer0_std=0.0004999855226099743; compression_max_mean=21.148225153387056; compression_max_std=0.26755046620422707; erasure1_layer_mean=NaN; erasure1_layer_std=NaN; erasure1_magnitude_mean=0.008333305517832438; erasure1_magnitude_std=0.0026787893233585856; erasure1_peak_mean=1.0; erasure1_peak_std=0.0; erasure1_n_test_mean=3600.0; erasure1_n_test_std=0.0; erasure2_layer_mean=NaN; erasure2_layer_std=NaN; erasure2_magnitude_mean=0.010092556476593018; erasure2_magnitude_std=0.00042430782468989327; tokens_per_word_probed_mean=3.84; tokens_per_word_probed_std=0.0; tokens_per_word_valid_mean=2.079882753314716; tokens_per_word_valid_std=0.0; bpb_gap_vs_4096_mean=0.03217529753283377; bpb_gap_vs_4096_std=0.0
  summary[3] | vocab=768; mdl_detok_mean=1.0; mdl_detok_std=0.0; mdl_ci_low_mean=1.0; mdl_ci_low_std=0.0; mdl_ci_high_mean=1.0; mdl_ci_high_std=0.0; compression_layer0_mean=2.8636417538585417; compression_layer0_std=0.0011507602824265047; compression_max_mean=21.247275336836946; compression_max_std=0.11836304042669059; erasure1_layer_mean=NaN; erasure1_layer_std=NaN; erasure1_magnitude_mean=0.011018494764963785; erasure1_magnitude_std=0.001529888868416852; erasure1_peak_mean=1.0; erasure1_peak_std=0.0; erasure1_n_test_mean=3600.0; erasure1_n_test_std=0.0; erasure2_layer_mean=NaN; erasure2_layer_std=NaN; erasure2_magnitude_mean=0.008240719636281332; erasure2_magnitude_std=0.0026691616993216897; tokens_per_word_probed_mean=3.39; tokens_per_word_probed_std=0.0; tokens_per_word_valid_mean=1.73512097557081; tokens_per_word_valid_std=0.0; bpb_gap_vs_4096_mean=0.022828404374091726; bpb_gap_vs_4096_std=0.0
  summary[4] | vocab=1024; mdl_detok_mean=1.0; mdl_detok_std=0.0; mdl_ci_low_mean=1.0; mdl_ci_low_std=0.0; mdl_ci_high_mean=1.0; mdl_ci_high_std=0.0; compression_layer0_mean=4.0092650380321695; compression_layer0_std=0.0030024191802110415; compression_max_mean=21.444826888451164; compression_max_std=0.0618497107432253; erasure1_layer_mean=NaN; erasure1_layer_std=NaN; erasure1_magnitude_mean=0.00596704085667928; erasure1_magnitude_std=0.00128497442838285; erasure1_peak_mean=1.0; erasure1_peak_std=0.0; erasure1_n_test_mean=3240.0; erasure1_n_test_std=0.0; erasure2_layer_mean=NaN; erasure2_layer_std=NaN; erasure2_magnitude_mean=0.005494515101114909; erasure2_magnitude_std=0.0019958310213691157; tokens_per_word_probed_mean=2.65; tokens_per_word_probed_std=0.0; tokens_per_word_valid_mean=1.583769050431589; tokens_per_word_valid_std=0.0; bpb_gap_vs_4096_mean=0.017548257687913682; bpb_gap_vs_4096_std=0.0
  summary[5] | vocab=4096; mdl_detok_mean=0.0; mdl_detok_std=0.0; mdl_ci_low_mean=0.0; mdl_ci_low_std=0.0; mdl_ci_high_mean=0.0; mdl_ci_high_std=0.0; compression_layer0_mean=23.258879009257168; compression_layer0_std=0.008685933930716915; compression_max_mean=23.258879009257168; compression_max_std=0.008685933930716915; erasure1_layer_mean=NaN; erasure1_layer_std=NaN; erasure1_magnitude_mean=NaN; erasure1_magnitude_std=NaN; erasure1_peak_mean=NaN; erasure1_peak_std=NaN; erasure1_n_test_mean=0.0; erasure1_n_test_std=0.0; erasure2_layer_mean=NaN; erasure2_layer_std=NaN; erasure2_magnitude_mean=NaN; erasure2_magnitude_std=NaN; tokens_per_word_probed_mean=1.0; tokens_per_word_probed_std=0.0; tokens_per_word_valid_mean=1.2652428402676088; tokens_per_word_valid_std=0.0; bpb_gap_vs_4096_mean=0.0; bpb_gap_vs_4096_std=0.0
  Q1b | spearman_tpw_vs_mdl_detok=0.8451542547285166; p=0.03410942316740963; v256_minus_v4096=2.0; gap_exceeds_seed_sd=true; verdict="confirmed"
  Q2b | spearman_mdl_detok_vs_bpb_gap=0.8451542547285165; p=0.03410942316740967; verdict="confirmed"
  Q3b | conditions=[5 values]; magnitudes=[5 values]; spearman_tpw_vs_erasure_layer=null; verdict="refuted"
Result entry: 2026-10-15 — Step 3b (GATE 3): MDL and erasure probes on the 18 E5 tiny models [RESULTS.md 438-467, `baf4f09` 2026-10-15 00:56:53 +0530]
Source files: results/m1_tiny_mdl/analysis.json

### M4: M4, M4b, M4c: retrieval, mapping, surface baseline, natural romanization
Registered: PRE-REGISTRATION — M4c natural romanization in M4 (written 2026-10-16, before any natural FLORES+ sentence of this sample is romanized or run) [RESULTS.md 801-819, `d8e2bd8` 2026-10-16 00:49:27 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: itrans, native, natural; tasks/measures: unmapped retrieval acc@1, train-half centering, 248 candidates (as m4c_natural unmapped_test); seeds: not recorded as a column or key in the result files
Table [m4b_mapping/summary.csv] (8 rows of 8):
  model=qwen2.5-1.5b | form=native | n_layers=28 | best_layer_mapped=1 | mapped=0.5174129353233831 | mapped_ci=[0.4865671694278717, 0.5482587218284607] | alpha=0.01 | best_layer_unmapped=15 | unmapped=0.1781094527363184 | unmapped_ci=[0.15422885119915009, 0.20099502801895142] | mapped_minus_unmapped_ci=[0.3024875521659851, 0.3751492500305176] | shuffled_control=0.001990049751243781 | max_test_mapped_any_layer=0.5174129353233831 | max_test_unmapped_any_layer=0.1781094527363184
  model=qwen2.5-1.5b | form=itrans | n_layers=28 | best_layer_mapped=1 | mapped=0.5293532338308458 | mapped_ci=[0.49850746989250183, 0.5601990222930908] | alpha=0.1 | best_layer_unmapped=1 | unmapped=0.06567164179104477 | unmapped_ci=[0.05074626952409744, 0.08059701323509216] | mapped_minus_unmapped_ci=[0.4308457672595978, 0.4965174198150635] | shuffled_control=0.001990049751243781 | max_test_mapped_any_layer=0.5293532338308458 | max_test_unmapped_any_layer=0.06567164179104477
  model=qwen3.5-2b | form=native | n_layers=24 | best_layer_mapped=7 | mapped=0.9611940298507463 | mapped_ci=[0.9492537379264832, 0.9731343388557434] | alpha=0.1 | best_layer_unmapped=15 | unmapped=0.9781094527363184 | unmapped_ci=[0.9681591987609863, 0.9870646595954895] | mapped_minus_unmapped_ci=[-0.030845770612359047, -0.0029850746504962444] | shuffled_control=0.0029850746268656717 | max_test_mapped_any_layer=0.9671641791044776 | max_test_unmapped_any_layer=0.9870646766169154
  model=qwen3.5-2b | form=itrans | n_layers=24 | best_layer_mapped=3 | mapped=0.4845771144278607 | mapped_ci=[0.45373135805130005, 0.5154228806495667] | alpha=0.1 | best_layer_unmapped=6 | unmapped=0.11343283582089553 | unmapped_ci=[0.09452736377716064, 0.13333334028720856] | mapped_minus_unmapped_ci=[0.3372885584831238, 0.40497511625289917] | shuffled_control=0.0009950248756218905 | max_test_mapped_any_layer=0.4845771144278607 | max_test_unmapped_any_layer=0.1253731343283582
  model=sarvam-1 | form=native | n_layers=28 | best_layer_mapped=26 | mapped=0.8985074626865671 | mapped_ci=[0.8796020150184631, 0.9164178967475891] | alpha=0.1 | best_layer_unmapped=23 | unmapped=0.9442786069651742 | unmapped_ci=[0.93034827709198, 0.9572139382362366] | mapped_minus_unmapped_ci=[-0.06669154763221741, -0.024875622242689133] | shuffled_control=0.0009950248756218905 | max_test_mapped_any_layer=0.8985074626865671 | max_test_unmapped_any_layer=0.9512437810945273
  model=sarvam-1 | form=itrans | n_layers=28 | best_layer_mapped=24 | mapped=0.3800995024875622 | mapped_ci=[0.3502487540245056, 0.40995025634765625] | alpha=0.1 | best_layer_unmapped=21 | unmapped=0.5144278606965174 | unmapped_ci=[0.483582079410553, 0.544278621673584] | mapped_minus_unmapped_ci=[-0.16915422677993774, -0.09850746393203735] | shuffled_control=0.0009950248756218905 | max_test_mapped_any_layer=0.4059701492537313 | max_test_unmapped_any_layer=0.5144278606965174
  model=gemma4-e2b | form=native | n_layers=35 | best_layer_mapped=8 | mapped=0.9771144278606965 | mapped_ci=[0.967164158821106, 0.9860696792602539] | alpha=0.1 | best_layer_unmapped=7 | unmapped=0.9950248756218906 | unmapped_ci=[0.9900497794151306, 0.9990049600601196] | mapped_minus_unmapped_ci=[-0.026865672320127487, -0.009950248524546623] | shuffled_control=0.001990049751243781 | max_test_mapped_any_layer=0.9771144278606965 | max_test_unmapped_any_layer=0.9950248756218906
  model=gemma4-e2b | form=itrans | n_layers=35 | best_layer_mapped=0 | mapped=0.472636815920398 | mapped_ci=[0.4417910575866699, 0.5034825801849365] | alpha=0.1 | best_layer_unmapped=7 | unmapped=0.26865671641791045 | unmapped_ci=[0.2407960146665573, 0.29651740193367004] | mapped_minus_unmapped_ci=[0.16517412662506104, 0.24378108978271484] | shuffled_control=0.0009950248756218905 | max_test_mapped_any_layer=0.472636815920398 | max_test_unmapped_any_layer=0.26865671641791045
Table [m4c_natural/summary.csv] (12 rows of 12):
  model=qwen2.5-1.5b | form=native | n_sentences=496 | unmapped_all_best=0.21774193548387097 | unmapped_all_best_layer=16 | mapped_test=0.2903225806451613 | mapped_test_ci=[0.2338709682226181, 0.3467741906642914] | mapped_layer=27 | unmapped_test=0.23790322580645162 | unmapped_test_ci=[0.1854838728904724, 0.2943548262119293] | shuffled_control=0.008064516129032258
  model=qwen2.5-1.5b | form=itrans | n_sentences=496 | unmapped_all_best=0.10080645161290322 | unmapped_all_best_layer=1 | mapped_test=0.2782258064516129 | mapped_test_ci=[0.22177419066429138, 0.33467742800712585] | mapped_layer=1 | unmapped_test=0.13306451612903225 | unmapped_test_ci=[0.0927419364452362, 0.17741934955120087] | shuffled_control=0.008064516129032258
  model=qwen2.5-1.5b | form=natural | n_sentences=496 | unmapped_all_best=0.3326612903225806 | unmapped_all_best_layer=1 | mapped_test=0.24596774193548387 | mapped_test_ci=[0.19354838132858276, 0.30241936445236206] | mapped_layer=1 | unmapped_test=0.3790322580645161 | unmapped_test_ci=[0.31854838132858276, 0.4395161271095276] | shuffled_control=0.004032258064516129
  model=qwen3.5-2b | form=native | n_sentences=496 | unmapped_all_best=0.9919354838709677 | unmapped_all_best_layer=15 | mapped_test=0.9516129032258065 | mapped_test_ci=[0.9233871102333069, 0.975806474685669] | mapped_layer=7 | unmapped_test=1.0 | unmapped_test_ci=[1.0, 1.0] | shuffled_control=0.004032258064516129
  model=qwen3.5-2b | form=itrans | n_sentences=496 | unmapped_all_best=0.18951612903225806 | unmapped_all_best_layer=5 | mapped_test=0.28225806451612906 | mapped_test_ci=[0.22580644488334656, 0.33870968222618103] | mapped_layer=2 | unmapped_test=0.18951612903225806 | unmapped_test_ci=[0.1411290317773819, 0.23790322244167328] | shuffled_control=0.016129032258064516
  model=qwen3.5-2b | form=natural | n_sentences=496 | unmapped_all_best=0.4778225806451613 | unmapped_all_best_layer=6 | mapped_test=0.3225806451612903 | mapped_test_ci=[0.2661290466785431, 0.3790322542190552] | mapped_layer=7 | unmapped_test=0.5120967741935484 | unmapped_test_ci=[0.4516128897666931, 0.5725806355476379] | shuffled_control=0.004032258064516129
  model=sarvam-1 | form=native | n_sentences=496 | unmapped_all_best=0.9657258064516129 | unmapped_all_best_layer=24 | mapped_test=0.842741935483871 | mapped_test_ci=[0.7943548560142517, 0.8870967626571655] | mapped_layer=25 | unmapped_test=0.9879032258064516 | unmapped_test_ci=[0.9717742204666138, 1.0] | shuffled_control=0.004032258064516129
  model=sarvam-1 | form=itrans | n_sentences=496 | unmapped_all_best=0.6169354838709677 | unmapped_all_best_layer=17 | mapped_test=0.3185483870967742 | mapped_test_ci=[0.2620967626571655, 0.375] | mapped_layer=21 | unmapped_test=0.6854838709677419 | unmapped_test_ci=[0.625, 0.7419354915618896] | shuffled_control=0.016129032258064516
  model=sarvam-1 | form=natural | n_sentences=496 | unmapped_all_best=0.9233870967741935 | unmapped_all_best_layer=19 | mapped_test=0.6612903225806451 | mapped_test_ci=[0.600806474685669, 0.7177419066429138] | mapped_layer=24 | unmapped_test=0.9193548387096774 | unmapped_test_ci=[0.8830645084381104, 0.9516128897666931] | shuffled_control=0.008064516129032258
  model=gemma4-e2b | form=native | n_sentences=496 | unmapped_all_best=0.9979838709677419 | unmapped_all_best_layer=7 | mapped_test=0.9435483870967742 | mapped_test_ci=[0.9112903475761414, 0.9717742204666138] | mapped_layer=7 | unmapped_test=1.0 | unmapped_test_ci=[1.0, 1.0] | shuffled_control=0.0
  model=gemma4-e2b | form=itrans | n_sentences=496 | unmapped_all_best=0.35685483870967744 | unmapped_all_best_layer=7 | mapped_test=0.2540322580645161 | mapped_test_ci=[0.2016129046678543, 0.30645161867141724] | mapped_layer=0 | unmapped_test=0.4435483870967742 | unmapped_test_ci=[0.38306450843811035, 0.5080645084381104] | shuffled_control=0.0
  model=gemma4-e2b | form=natural | n_sentences=496 | unmapped_all_best=0.6532258064516129 | unmapped_all_best_layer=7 | mapped_test=0.40725806451612906 | mapped_test_ci=[0.3467741906642914, 0.4677419364452362] | mapped_layer=8 | unmapped_test=0.7096774193548387 | unmapped_test_ci=[0.6532257795333862, 0.7620967626571655] | shuffled_control=0.004032258064516129
Table [m4b_surface/verdict.json] (23 records):
  (top) | prediction_gap_persists_filtered_3_models=true; gap_entity_dependent=false
  surface | qwen2.5-1.5b|native|ridge="beyond surface"; qwen2.5-1.5b|native|procrustes="partial"; qwen2.5-1.5b|itrans|ridge="beyond surface"; qwen2.5-1.5b|itrans|procrustes="surface-level"; qwen3.5-2b|native|ridge="beyond surface"; qwen3.5-2b|native|procrustes="beyond surface"; qwen3.5-2b|itrans|ridge="beyond surface"; qwen3.5-2b|itrans|procrustes="partial"; sarvam-1|native|ridge="beyond surface"; sarvam-1|native|procrustes="beyond surface"; sarvam-1|itrans|ridge="surface-level"; sarvam-1|itrans|procrustes="surface-level"; gemma4-e2b|native|ridge="beyond surface"; gemma4-e2b|native|procrustes="beyond surface"; gemma4-e2b|itrans|ridge="surface-level"; gemma4-e2b|itrans|procrustes="surface-level"
  subset_gap.qwen2.5-1.5b|filtered | mapped_gap=-0.04383561643835615; mapped_gap_ci=[-0.0986301377415657, 0.013698630034923553]; status="closes"; native_mapped=0.25753424657534246; itrans_mapped=0.3013698630136986; native_mapped_ci=[0.2136986255645752, 0.3041096031665802]; itrans_mapped_ci=[0.25479450821876526, 0.3506849408149719]
  subset_gap.qwen2.5-1.5b|random_size_matched | mapped_gap=0.024657534246575352; mapped_gap_ci=[-0.03287671133875847, 0.08219178020954132]; status="closes"; native_mapped=0.3178082191780822; itrans_mapped=0.29315068493150687; native_mapped_ci=[0.27123287320137024, 0.3643835484981537]; itrans_mapped_ci=[0.24657534062862396, 0.3397260308265686]
  subset_gap.qwen3.5-2b|filtered | mapped_gap=0.6082191780821917; mapped_gap_ci=[0.5561643838882446, 0.6575342416763306]; status="persists"; native_mapped=0.9232876712328767; itrans_mapped=0.3150684931506849; native_mapped_ci=[0.8931506872177124, 0.9479451775550842]; itrans_mapped_ci=[0.2684931457042694, 0.36164382100105286]
  subset_gap.qwen3.5-2b|random_size_matched | mapped_gap=0.6493150684931507; mapped_gap_ci=[0.5972602963447571, 0.7013698816299438]; status="persists"; native_mapped=0.9753424657534246; itrans_mapped=0.32602739726027397; native_mapped_ci=[0.9589040875434875, 0.9890410900115967]; itrans_mapped_ci=[0.2767123281955719, 0.375342458486557]
  subset_gap.sarvam-1|filtered | mapped_gap=0.5561643835616439; mapped_gap_ci=[0.501369833946228, 0.6109589338302612]; status="persists"; native_mapped=0.8410958904109589; itrans_mapped=0.28493150684931506; native_mapped_ci=[0.8027397394180298, 0.8767123222351074]; itrans_mapped_ci=[0.23835615813732147, 0.3315068483352661]
  subset_gap.sarvam-1|random_size_matched | mapped_gap=0.5506849315068494; mapped_gap_ci=[0.49589040875434875, 0.6027397513389587]; status="persists"; native_mapped=0.8547945205479452; itrans_mapped=0.3041095890410959; native_mapped_ci=[0.8164383769035339, 0.8904109597206116]; itrans_mapped_ci=[0.2575342357158661, 0.3506849408149719]
  subset_gap.gemma4-e2b|filtered | mapped_gap=0.6027397260273972; mapped_gap_ci=[0.5479452013969421, 0.6547945141792297]; status="persists"; native_mapped=0.9726027397260274; itrans_mapped=0.3698630136986301; native_mapped_ci=[0.9561643600463867, 0.9890410900115967]; itrans_mapped_ci=[0.3205479383468628, 0.4191780686378479]
  subset_gap.gemma4-e2b|random_size_matched | mapped_gap=0.7150684931506849; mapped_gap_ci=[0.6657534241676331, 0.7616438269615173]; status="persists"; native_mapped=0.958904109589041; itrans_mapped=0.24383561643835616; native_mapped_ci=[0.9369863271713257, 0.9780821800231934]; itrans_mapped_ci=[0.20000000298023224, 0.2876712381839752]
  filtered_minus_random_mapped.qwen2.5-1.5b | itrans_drops_more_than_native=false
  filtered_minus_random_mapped.qwen2.5-1.5b.native | diff=-0.060273972602739756; ci=[-0.12602739726027395, 0.005479452054794498]
  filtered_minus_random_mapped.qwen2.5-1.5b.itrans | diff=0.008219178082191747; ci=[-0.05753424657534245, 0.07397260273972606]
  filtered_minus_random_mapped.qwen3.5-2b | itrans_drops_more_than_native=false
  filtered_minus_random_mapped.qwen3.5-2b.native | diff=-0.05205479452054795; ci=[-0.08493150684931505, -0.021917808219178103]
  filtered_minus_random_mapped.qwen3.5-2b.itrans | diff=-0.010958904109589052; ci=[-0.07678082191780818, 0.05753424657534245]
  filtered_minus_random_mapped.sarvam-1 | itrans_drops_more_than_native=true
  filtered_minus_random_mapped.sarvam-1.native | diff=-0.013698630136986356; ci=[-0.06575342465753431, 0.0383561643835616]
  filtered_minus_random_mapped.sarvam-1.itrans | diff=-0.019178082191780854; ci=[-0.0876712328767123, 0.04657534246575343]
  filtered_minus_random_mapped.gemma4-e2b | itrans_drops_more_than_native=false
  filtered_minus_random_mapped.gemma4-e2b.native | diff=0.013698630136986356; ci=[-0.010958904109589107, 0.041095890410958846]
  filtered_minus_random_mapped.gemma4-e2b.itrans | diff=0.12602739726027395; ci=[0.060273972602739756, 0.19178082191780824]
  n | kept_train=369; kept_test=365; kept_native_with_digit_or_latin=13
Table [m4b_mapping/verdict.json] (1 records):
  verdict | strong_H1="inconclusive"
Table [m4c_natural/verdict.json] (17 records):
  (top) | n_sentences=496; n_defective_excluded=4
  paired_differences.qwen2.5-1.5b|native-natural|mapped | diff=0.044354838709677435; ci=[-0.024193547666072845, 0.1088709682226181]
  paired_differences.qwen2.5-1.5b|native-natural|unmapped | diff=-0.1411290322580645; ci=[-0.2177419364452362, -0.06451612710952759]
  paired_differences.qwen2.5-1.5b|natural-itrans|mapped | diff=-0.032258064516129004; ci=[-0.0927419364452362, 0.032258063554763794]
  paired_differences.qwen2.5-1.5b|natural-itrans|unmapped | diff=0.24596774193548387; ci=[0.19354838132858276, 0.30241936445236206]
  paired_differences.qwen3.5-2b|native-natural|mapped | diff=0.6290322580645162; ci=[0.5685483813285828, 0.6895161271095276]
  paired_differences.qwen3.5-2b|native-natural|unmapped | diff=0.4879032258064516; ci=[0.42741936445236206, 0.5483871102333069]
  paired_differences.qwen3.5-2b|natural-itrans|mapped | diff=0.040322580645161255; ci=[-0.032258063554763794, 0.11290322244167328]
  paired_differences.qwen3.5-2b|natural-itrans|unmapped | diff=0.3225806451612903; ci=[0.2540322542190552, 0.3911290466785431]
  paired_differences.sarvam-1|native-natural|mapped | diff=0.18145161290322587; ci=[0.12096773833036423, 0.24193547666072845]
  paired_differences.sarvam-1|native-natural|unmapped | diff=0.06854838709677424; ci=[0.03629032149910927, 0.10483870655298233]
  paired_differences.sarvam-1|natural-itrans|mapped | diff=0.34274193548387094; ci=[0.2620967626571655, 0.4193548262119293]
  paired_differences.sarvam-1|natural-itrans|unmapped | diff=0.2338709677419355; ci=[0.17741934955120087, 0.2904233932495117]
  paired_differences.gemma4-e2b|native-natural|mapped | diff=0.5362903225806452; ci=[0.4717741906642914, 0.600806474685669]
  paired_differences.gemma4-e2b|native-natural|unmapped | diff=0.29032258064516125; ci=[0.23790322244167328, 0.3467741906642914]
  paired_differences.gemma4-e2b|natural-itrans|mapped | diff=0.15322580645161293; ci=[0.07661290466785431, 0.22983871400356293]
  paired_differences.gemma4-e2b|natural-itrans|unmapped | diff=0.26612903225806456; ci=[0.2016129046678543, 0.3306451737880707]
Result entry: 2026-10-17 (written 2026-10-21) — M4c natural romanization in M4 (registered 2026-10-16): refuted, natural is well above ITRANS [RESULTS.md 1200-1248, `d7693f7` 2026-10-21 22:25:39 +0530]
Source files: results/m4b_mapping/summary.csv; results/m4c_natural/summary.csv; results/m4b_surface/verdict.json; results/m4b_mapping/verdict.json; results/m4c_natural/verdict.json

### E0b: Familiarity test (sentiment, XNLI)
Registered: PRE-REGISTRATION — E0b familiarity test (written 2026-10-14, before any E0b scoring) [RESULTS.md 241-272, `0a1d054` 2026-10-14 18:42:59 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: lossy, lower, itrans, native, english, natural; tasks/measures: sib, xnli, sentiment; seeds: 0
Table [e0b_familiarity/gate1/verdicts.json] (3 records):
  (top) | informative_cells=[10 values]; P3_lossy_lt_itrans=false; P1_familiarity_dominates=false; P2_fragmentation_also_matters=false
  P3_parts | all_cells_lossy_below_itrans=false; fraction_significant=0.0; n_cells=10
  P2_parts | qwen_natural_gt_native=false; sarvam_natural_lt_native=false
Table [e0b_familiarity/gate1/mcnemar.csv] (30 rows of 30):
  model=gemma4-e2b | task=sentiment | a=natural | b=native | acc_a=0.803030303030303 | acc_b=0.9848484848484849 | n=198 | diff=-0.18181818181818188 | a_only=2 | b_only=38 | p=1.4933903003111482e-09 | p_holm=4.33083187090233e-08 | significant=True
  model=gemma4-e2b | task=sentiment | a=natural | b=itrans | acc_a=0.803030303030303 | acc_b=0.7575757575757576 | n=198 | diff=0.045454545454545414 | a_only=16 | b_only=7 | p=0.0931396484375 | p_holm=1.0 | significant=False
  model=gemma4-e2b | task=sentiment | a=lossy | b=itrans | acc_a=0.79 | acc_b=0.755 | n=200 | diff=0.03500000000000003 | a_only=18 | b_only=11 | p=0.26493089646101 | p_holm=1.0 | significant=False
  model=gemma4-e2b | task=xnli | a=natural | b=native | acc_a=0.40414507772020725 | acc_b=0.538860103626943 | n=193 | diff=-0.13471502590673579 | a_only=11 | b_only=37 | p=0.0002222449626216872 | p_holm=0.005778369028163867 | significant=True
  model=gemma4-e2b | task=xnli | a=natural | b=itrans | acc_a=0.40414507772020725 | acc_b=0.41450777202072536 | n=193 | diff=-0.010362694300518116 | a_only=11 | b_only=13 | p=0.8388197422027588 | p_holm=1.0 | significant=False
  model=gemma4-e2b | task=xnli | a=lossy | b=itrans | acc_a=0.4 | acc_b=0.41 | n=200 | diff=-0.009999999999999953 | a_only=11 | b_only=13 | p=0.8388197422027588 | p_holm=1.0 | significant=False
  model=qwen2.5-1.5b | task=sentiment | a=natural | b=native | acc_a=0.5151515151515151 | acc_b=0.702020202020202 | n=198 | diff=-0.18686868686868685 | a_only=20 | b_only=57 | p=2.926311069930838e-05 | p_holm=0.0008193670995806346 | significant=True
  model=qwen2.5-1.5b | task=sentiment | a=natural | b=itrans | acc_a=0.5151515151515151 | acc_b=0.4898989898989899 | n=198 | diff=0.02525252525252525 | a_only=6 | b_only=1 | p=0.125 | p_holm=1.0 | significant=False
  model=qwen2.5-1.5b | task=sentiment | a=lossy | b=itrans | acc_a=0.5 | acc_b=0.495 | n=200 | diff=0.0050000000000000044 | a_only=4 | b_only=3 | p=1.0 | p_holm=1.0 | significant=False
  model=qwen2.5-1.5b | task=xnli | a=natural | b=native | acc_a=0.32124352331606215 | acc_b=0.40414507772020725 | n=193 | diff=-0.0829015544041451 | a_only=16 | b_only=32 | p=0.029304946720529308 | p_holm=0.5860989344105861 | significant=False
  model=qwen2.5-1.5b | task=xnli | a=natural | b=itrans | acc_a=0.32124352331606215 | acc_b=0.32124352331606215 | n=193 | diff=0.0 | a_only=15 | b_only=15 | p=1.0 | p_holm=1.0 | significant=False
  model=qwen2.5-1.5b | task=xnli | a=lossy | b=itrans | acc_a=0.325 | acc_b=0.32 | n=200 | diff=0.0050000000000000044 | a_only=18 | b_only=17 | p=0.9999999999999998 | p_holm=1.0 | significant=False
  model=qwen3-1.7b | task=sentiment | a=natural | b=native | acc_a=0.5606060606060606 | acc_b=0.8333333333333334 | n=198 | diff=-0.2727272727272728 | a_only=14 | b_only=68 | p=1.1349339471612945e-09 | p_holm=3.4048018414838833e-08 | significant=True
  model=qwen3-1.7b | task=sentiment | a=natural | b=itrans | acc_a=0.5606060606060606 | acc_b=0.5303030303030303 | n=198 | diff=0.030303030303030276 | a_only=30 | b_only=24 | p=0.49661743531793345 | p_holm=1.0 | significant=False
  model=qwen3-1.7b | task=sentiment | a=lossy | b=itrans | acc_a=0.57 | acc_b=0.535 | n=200 | diff=0.03499999999999992 | a_only=32 | b_only=25 | p=0.42704285650325524 | p_holm=1.0 | significant=False
  model=qwen3-1.7b | task=xnli | a=natural | b=native | acc_a=0.34196891191709844 | acc_b=0.44559585492227977 | n=193 | diff=-0.10362694300518133 | a_only=3 | b_only=23 | p=8.797645568847656e-05 | p_holm=0.002375364303588867 | significant=True
  model=qwen3-1.7b | task=xnli | a=natural | b=itrans | acc_a=0.34196891191709844 | acc_b=0.33678756476683935 | n=193 | diff=0.005181347150259086 | a_only=1 | b_only=0 | p=1.0 | p_holm=1.0 | significant=False
  model=qwen3-1.7b | task=xnli | a=lossy | b=itrans | acc_a=0.335 | acc_b=0.335 | n=200 | diff=0.0 | a_only=0 | b_only=0 | p=1.0 | p_holm=1.0 | significant=False
  model=qwen3.5-2b | task=sentiment | a=natural | b=native | acc_a=0.7222222222222222 | acc_b=0.7373737373737373 | n=198 | diff=-0.015151515151515138 | a_only=26 | b_only=29 | p=0.7877061896700431 | p_holm=1.0 | significant=False
  model=qwen3.5-2b | task=sentiment | a=natural | b=itrans | acc_a=0.7222222222222222 | acc_b=0.6565656565656566 | n=198 | diff=0.06565656565656564 | a_only=29 | b_only=16 | p=0.07245426016254441 | p_holm=1.0 | significant=False
  model=qwen3.5-2b | task=sentiment | a=lossy | b=itrans | acc_a=0.68 | acc_b=0.655 | n=200 | diff=0.025000000000000022 | a_only=23 | b_only=18 | p=0.5327092552361137 | p_holm=1.0 | significant=False
  model=qwen3.5-2b | task=xnli | a=natural | b=native | acc_a=0.34196891191709844 | acc_b=0.34196891191709844 | n=193 | diff=0.0 | a_only=0 | b_only=0 | p=1.0 | p_holm=1.0 | significant=False
  model=qwen3.5-2b | task=xnli | a=natural | b=itrans | acc_a=0.34196891191709844 | acc_b=0.34196891191709844 | n=193 | diff=0.0 | a_only=0 | b_only=0 | p=1.0 | p_holm=1.0 | significant=False
  model=qwen3.5-2b | task=xnli | a=lossy | b=itrans | acc_a=0.335 | acc_b=0.34 | n=200 | diff=-0.0050000000000000044 | a_only=0 | b_only=1 | p=1.0 | p_holm=1.0 | significant=False
  model=sarvam-1 | task=sentiment | a=natural | b=native | acc_a=0.8939393939393939 | acc_b=0.9545454545454546 | n=198 | diff=-0.06060606060606066 | a_only=5 | b_only=17 | p=0.01690053939819336 | p_holm=0.38871240615844727 | significant=False
  model=sarvam-1 | task=sentiment | a=natural | b=itrans | acc_a=0.8939393939393939 | acc_b=0.8181818181818182 | n=198 | diff=0.07575757575757569 | a_only=27 | b_only=12 | p=0.023702702470473014 | p_holm=0.4977567518799333 | significant=False
  model=sarvam-1 | task=sentiment | a=lossy | b=itrans | acc_a=0.895 | acc_b=0.82 | n=200 | diff=0.07500000000000007 | a_only=21 | b_only=6 | p=0.005924612283706665 | p_holm=0.14811530709266663 | significant=False
  model=sarvam-1 | task=xnli | a=natural | b=native | acc_a=0.46632124352331605 | acc_b=0.5129533678756477 | n=193 | diff=-0.04663212435233166 | a_only=14 | b_only=23 | p=0.18774155899882317 | p_holm=1.0 | significant=False
  model=sarvam-1 | task=xnli | a=natural | b=itrans | acc_a=0.46632124352331605 | acc_b=0.39378238341968913 | n=193 | diff=0.07253886010362692 | a_only=23 | b_only=9 | p=0.020061607006937265 | p_holm=0.44135535415261984 | significant=False
  model=sarvam-1 | task=xnli | a=lossy | b=itrans | acc_a=0.47 | acc_b=0.385 | n=200 | diff=0.08499999999999996 | a_only=29 | b_only=12 | p=0.011507789735333063 | p_holm=0.2761869536479935 | significant=False
Result entry: 2026-10-15 — E0b GATE 1 (five forms, five models) [RESULTS.md 504-560, `3565362` 2026-10-15 16:40:24 +0530]
Source files: results/e0b_familiarity/gate1/verdicts.json; results/e0b_familiarity/gate1/mcnemar.csv

### E0c: SIB-200 topic classification
Registered: PRE-REGISTRATION — E0c SIB-200 topic classification (written 2026-10-16, before any SIB-200 item is scored) [RESULTS.md 833-868, `ba54695` 2026-10-16 02:29:27 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: lossy, lower, itrans, native, english, natural257; tasks/measures: sib; seeds: not recorded as a column or key in the result files
Table [e0c_sib/gate/verdicts.json] (19 records):
  (top) | informative_models=[5 values]; P_a="partly supported"; P_b_primary_unmapped="inconclusive"; P_b_cells_counted=8
  P_a_tests[model=gemma4-e2b] | model="gemma4-e2b"; task="sib"; a="native"; b="itrans"; acc_a=0.75; acc_b=0.3665338645418327; n=1004; diff=0.3834661354581673; a_only=425; b_only=40; p=2.5188719631954495e-82; p_holm=2.0150975705563596e-81; significant=true
  P_a_tests[model=gemma4-e2b] | model="gemma4-e2b"; task="sib"; a="native"; b="lossy"; acc_a=0.75; acc_b=0.49701195219123506; n=1004; diff=0.25298804780876494; a_only=293; b_only=39; p=2.668515711757834e-49; p_holm=1.334257855878917e-48; significant=true
  P_a_tests[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="sib"; a="native"; b="itrans"; acc_a=0.33565737051792827; acc_b=0.2778884462151394; n=1004; diff=0.05776892430278885; a_only=159; b_only=101; p=0.00038780629202563347; p_holm=0.0007756125840512669; significant=true
  P_a_tests[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="sib"; a="native"; b="lossy"; acc_a=0.33565737051792827; acc_b=0.3665338645418327; n=1004; diff=-0.03087649402390441; a_only=124; b_only=155; p=0.07229593171431895; p_holm=0.07229593171431895; significant=false
  P_a_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; task="sib"; a="native"; b="itrans"; acc_a=0.6723107569721115; acc_b=0.2400398406374502; n=1004; diff=0.4322709163346613; a_only=456; b_only=22; p=1.2990189533010863e-106; p_holm=1.2990189533010864e-105; significant=true
  P_a_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; task="sib"; a="native"; b="lossy"; acc_a=0.6723107569721115; acc_b=0.30677290836653387; n=1004; diff=0.36553784860557764; a_only=398; b_only=31; p=2.529451058538525e-82; p_holm=2.0150975705563596e-81; significant=true
  P_a_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; task="sib"; a="native"; b="itrans"; acc_a=0.6762948207171314; acc_b=0.2410358565737052; n=1004; diff=0.43525896414342624; a_only=462; b_only=25; p=2.8113371589728562e-105; p_holm=2.5302034430755707e-104; significant=true
  P_a_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; task="sib"; a="native"; b="lossy"; acc_a=0.6762948207171314; acc_b=0.3754980079681275; n=1004; diff=0.30079681274900394; a_only=345; b_only=43; p=1.1158511919563684e-59; p_holm=6.695107151738211e-59; significant=true
  P_a_tests[model=sarvam-1] | model="sarvam-1"; task="sib"; a="native"; b="itrans"; acc_a=0.7659362549800797; acc_b=0.5388446215139442; n=1004; diff=0.22709163346613548; a_only=299; b_only=71; p=2.123868442850549e-34; p_holm=8.495473771402196e-34; significant=true
  P_a_tests[model=sarvam-1] | model="sarvam-1"; task="sib"; a="native"; b="lossy"; acc_a=0.7659362549800797; acc_b=0.7051792828685259; n=1004; diff=0.06075697211155373; a_only=126; b_only=65; p=1.2058675268138053e-05; p_holm=3.617602580441416e-05; significant=true
  P_b_secondary_mapped[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; form="native"; beta=0.19276061379326914; p_holm=0.18179749209001259
  P_b_secondary_mapped[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; form="itrans"; beta=0.08997088755179476; p_holm=0.9366182943334389
  P_b_secondary_mapped[model=qwen3.5-2b] | model="qwen3.5-2b"; form="native"; beta=-0.007061251972137678; p_holm=1.0
  P_b_secondary_mapped[model=qwen3.5-2b] | model="qwen3.5-2b"; form="itrans"; beta=0.19651713934838352; p_holm=0.23199719943472918
  P_b_secondary_mapped[model=sarvam-1] | model="sarvam-1"; form="native"; beta=-0.006259901088759196; p_holm=1.0
  P_b_secondary_mapped[model=sarvam-1] | model="sarvam-1"; form="itrans"; beta=0.23024769121946084; p_holm=0.045691755543576136
  P_b_secondary_mapped[model=gemma4-e2b] | model="gemma4-e2b"; form="native"; beta=0.05847996959149546; p_holm=1.0
  P_b_secondary_mapped[model=gemma4-e2b] | model="gemma4-e2b"; form="itrans"; beta=-0.06541220759205002; p_holm=1.0
Table [e0c_sib/gate/mcnemar.csv] (10 rows of 10):
  model=gemma4-e2b | task=sib | a=native | b=itrans | acc_a=0.75 | acc_b=0.3665338645418327 | n=1004 | diff=0.3834661354581673 | a_only=425 | b_only=40 | p=2.5188719631954495e-82 | p_holm=2.0150975705563596e-81 | significant=True
  model=gemma4-e2b | task=sib | a=native | b=lossy | acc_a=0.75 | acc_b=0.49701195219123506 | n=1004 | diff=0.25298804780876494 | a_only=293 | b_only=39 | p=2.668515711757834e-49 | p_holm=1.334257855878917e-48 | significant=True
  model=qwen2.5-1.5b | task=sib | a=native | b=itrans | acc_a=0.33565737051792827 | acc_b=0.2778884462151394 | n=1004 | diff=0.05776892430278885 | a_only=159 | b_only=101 | p=0.00038780629202563347 | p_holm=0.0007756125840512669 | significant=True
  model=qwen2.5-1.5b | task=sib | a=native | b=lossy | acc_a=0.33565737051792827 | acc_b=0.3665338645418327 | n=1004 | diff=-0.03087649402390441 | a_only=124 | b_only=155 | p=0.07229593171431895 | p_holm=0.07229593171431895 | significant=False
  model=qwen3-1.7b | task=sib | a=native | b=itrans | acc_a=0.6723107569721115 | acc_b=0.2400398406374502 | n=1004 | diff=0.4322709163346613 | a_only=456 | b_only=22 | p=1.2990189533010863e-106 | p_holm=1.2990189533010864e-105 | significant=True
  model=qwen3-1.7b | task=sib | a=native | b=lossy | acc_a=0.6723107569721115 | acc_b=0.30677290836653387 | n=1004 | diff=0.36553784860557764 | a_only=398 | b_only=31 | p=2.529451058538525e-82 | p_holm=2.0150975705563596e-81 | significant=True
  model=qwen3.5-2b | task=sib | a=native | b=itrans | acc_a=0.6762948207171314 | acc_b=0.2410358565737052 | n=1004 | diff=0.43525896414342624 | a_only=462 | b_only=25 | p=2.8113371589728562e-105 | p_holm=2.5302034430755707e-104 | significant=True
  model=qwen3.5-2b | task=sib | a=native | b=lossy | acc_a=0.6762948207171314 | acc_b=0.3754980079681275 | n=1004 | diff=0.30079681274900394 | a_only=345 | b_only=43 | p=1.1158511919563684e-59 | p_holm=6.695107151738211e-59 | significant=True
  model=sarvam-1 | task=sib | a=native | b=itrans | acc_a=0.7659362549800797 | acc_b=0.5388446215139442 | n=1004 | diff=0.22709163346613548 | a_only=299 | b_only=71 | p=2.123868442850549e-34 | p_holm=8.495473771402196e-34 | significant=True
  model=sarvam-1 | task=sib | a=native | b=lossy | acc_a=0.7659362549800797 | acc_b=0.7051792828685259 | n=1004 | diff=0.06075697211155373 | a_only=126 | b_only=65 | p=1.2058675268138053e-05 | p_holm=3.617602580441416e-05 | significant=True
Result entry: 2026-10-17 — E0c SIB-200 topic classification (registered 2026-10-16): P-a partly supported, P-b inconclusive [RESULTS.md 1119-1188, `5e0ded5` 2026-10-17 05:01:13 +0530]
Source files: results/e0c_sib/gate/verdicts.json; results/e0c_sib/gate/mcnemar.csv

### BT: Back-translation comprehension gap (large model)
Registered: no separate registration entry (see the result entry)
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
no result file; the numbers are in the RESULTS.md entry cited below
Result entry: 2026-10-15 — Large-model result: native vs romanized comprehension gap (back-translation) [RESULTS.md 482-503, `d0a6aa0` 2026-10-15 01:19:38 +0530]
Source files: none

### L: Romanization ladder L1 to L3
Registered: PRE-REGISTRATION — Romanization ladder L1–L3 (written 2026-10-22, the lead author's design; before any ladder form is run or scored) [RESULTS.md 1319-1389, `93a9f68` 2026-10-22 01:03:02 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: lossy, lower, itrans, native, english, natural, natural257; tasks/measures: sib, xnli, sentiment, retrieval, sib_L3_secondary, xnli_reported_only; seeds: not recorded as a column or key in the result files
Table [l_ladder/verdict.json] (9 records):
  L1|retrieval | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; needed=2; n_counted=3; tpw_check_failed_models=[]; ci_holm_disagreements=["qwen3.5-2b", "sarvam-1"]
  L2|retrieval | verdict="effect, positive"; n_significant_positive=3; n_significant_negative=0; needed=2; n_counted=3; tpw_check_failed_models=[]; ci_holm_disagreements=[]
  L3|retrieval | verdict="effect, positive"; n_significant_positive=2; n_significant_negative=0; needed=2; n_counted=3; tpw_check_failed_models=[]; ci_holm_disagreements=["sarvam-1"]
  L1|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=2; needed=3; n_counted=4; tpw_check_failed_models=[]; ci_holm_disagreements=[]
  L2|sentiment | verdict="effect, positive"; n_significant_positive=3; n_significant_negative=0; needed=3; n_counted=4; tpw_check_failed_models=[]; ci_holm_disagreements=[]
  L3|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; needed=3; n_counted=4; tpw_check_failed_models=[]; ci_holm_disagreements=[]
  L1|sib | verdict="no effect detected"; n_significant_positive=2; n_significant_negative=1; needed=3; n_counted=4; tpw_check_failed_models=[]; ci_holm_disagreements=[]
  L2|sib | verdict="effect, positive"; n_significant_positive=4; n_significant_negative=0; needed=3; n_counted=4; tpw_check_failed_models=[]; ci_holm_disagreements=[]
  L3|sib_L3_secondary | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; needed=3; n_counted=4; tpw_check_failed_models=[]; ci_holm_disagreements=["sarvam-1", "qwen3-1.7b"]
Table [l_ladder/contrasts.csv] (57 rows of 57):
  measure=retrieval | model=qwen2.5-1.5b | contrast=L1 | a=lower | b=itrans | n=248 | acc_a=0.13306451612903225 | acc_b=0.13306451612903225 | diff=0.0 | ci=[-0.03629032149910927, 0.03629032149910927] | a_only=11 | b_only=11 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=retrieval | model=qwen2.5-1.5b | contrast=L2 | a=lossy | b=lower | n=248 | acc_a=0.20161290322580644 | acc_b=0.13306451612903225 | diff=0.06854838709677419 | ci=[0.02822580561041832, 0.1088709682226181] | a_only=23 | b_only=6 | p=0.002315700054168701 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=qwen2.5-1.5b | contrast=L3 | a=natural | b=lossy | n=248 | acc_a=0.3790322580645161 | acc_b=0.20161290322580644 | diff=0.1774193548387097 | ci=[0.12903225421905518, 0.22983871400356293] | a_only=46 | b_only=2 | p=8.363087999896379e-12 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=qwen3.5-2b | contrast=L1 | a=lower | b=itrans | n=248 | acc_a=0.2661290322580645 | acc_b=0.18951612903225806 | diff=0.07661290322580644 | ci=[0.02016128972172737, 0.13709677755832672] | a_only=37 | b_only=18 | p=0.014453833533827728 | counted=True | p_holm=0.05781533413531091 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=retrieval | model=qwen3.5-2b | contrast=L2 | a=lossy | b=lower | n=248 | acc_a=0.375 | acc_b=0.2661290322580645 | diff=0.1088709677419355 | ci=[0.04435483738780022, 0.1733870953321457] | a_only=47 | b_only=20 | p=0.0013071686857635996 | counted=True | p_holm=0.006535843428817998 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=qwen3.5-2b | contrast=L3 | a=natural | b=lossy | n=248 | acc_a=0.5120967741935484 | acc_b=0.375 | diff=0.13709677419354838 | ci=[0.08064515888690948, 0.19354838132858276] | a_only=44 | b_only=10 | p=3.3856859533720747e-06 | counted=True | p_holm=2.7085487626976598e-05 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=sarvam-1 | contrast=L1 | a=lower | b=itrans | n=248 | acc_a=0.6169354838709677 | acc_b=0.6854838709677419 | diff=-0.06854838709677413 | ci=[-0.125, -0.012096773833036423] | a_only=18 | b_only=35 | p=0.027008317653722358 | counted=True | p_holm=0.08102495296116707 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=retrieval | model=sarvam-1 | contrast=L2 | a=lossy | b=lower | n=248 | acc_a=0.8830645161290323 | acc_b=0.6169354838709677 | diff=0.2661290322580645 | ci=[0.20564515888690948, 0.3266128897666931] | a_only=71 | b_only=5 | p=5.249233110119942e-16 | counted=True | p_holm=4.724309799107948e-15 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=sarvam-1 | contrast=L3 | a=natural | b=lossy | n=248 | acc_a=0.9193548387096774 | acc_b=0.8830645161290323 | diff=0.03629032258064513 | ci=[0.004032257944345474, 0.06854838877916336] | a_only=13 | b_only=4 | p=0.049041748046875 | counted=True | p_holm=0.09808349609375 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=retrieval | model=gemma4-e2b | contrast=L1 | a=lower | b=itrans | n=248 | acc_a=0.4032258064516129 | acc_b=0.4435483870967742 | diff=-0.04032258064516131 | ci=[-0.1088709682226181, 0.024193547666072845] | a_only=32 | b_only=42 | p=0.29541328065567 | counted=True | p_holm=0.29541328065567 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=retrieval | model=gemma4-e2b | contrast=L2 | a=lossy | b=lower | n=248 | acc_a=0.5725806451612904 | acc_b=0.4032258064516129 | diff=0.1693548387096775 | ci=[0.10080645233392715, 0.23790322244167328] | a_only=63 | b_only=21 | p=4.968015141912969e-06 | counted=True | p_holm=3.477610599339078e-05 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=gemma4-e2b | contrast=L3 | a=natural | b=lossy | n=248 | acc_a=0.7096774193548387 | acc_b=0.5725806451612904 | diff=0.13709677419354838 | ci=[0.08064515888690948, 0.19758065044879913] | a_only=48 | b_only=14 | p=1.7428522601631996e-05 | counted=True | p_holm=0.00010457113560979198 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=qwen2.5-1.5b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.47 | acc_b=0.495 | diff=-0.025000000000000022 | ci=[-0.0651249960064888, 0.014999999664723873] | a_only=7 | b_only=12 | p=0.359283447265625 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen2.5-1.5b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.5 | acc_b=0.47 | diff=0.030000000000000027 | ci=[-0.009999999776482582, 0.07000000029802322] | a_only=12 | b_only=6 | p=0.237884521484375 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen2.5-1.5b | contrast=L3 | a=natural | b=lossy | n=198 | acc_a=0.5151515151515151 | acc_b=0.494949494949495 | diff=0.020202020202020166 | ci=[-0.005050505045801401, 0.05050504952669144] | a_only=6 | b_only=2 | p=0.2890625 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen3.5-2b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.54 | acc_b=0.655 | diff=-0.11499999999999999 | ci=[-0.18000000715255737, -0.054999999701976776] | a_only=10 | b_only=33 | p=0.0006061066312668117 | counted=True | p_holm=0.004848853050134494 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=qwen3.5-2b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.68 | acc_b=0.54 | diff=0.14 | ci=[0.07500000298023224, 0.20499999821186066] | a_only=39 | b_only=11 | p=9.021490107130603e-05 | counted=True | p_holm=0.0009021490107130603 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=qwen3.5-2b | contrast=L3 | a=natural | b=lossy | n=198 | acc_a=0.7222222222222222 | acc_b=0.6818181818181818 | diff=0.04040404040404044 | ci=[-0.02525252476334572, 0.10606060922145844] | a_only=25 | b_only=17 | p=0.27995623852893914 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=sarvam-1 | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.765 | acc_b=0.82 | diff=-0.05499999999999994 | ci=[-0.11500000208616257, 0.009999999776482582] | a_only=15 | b_only=26 | p=0.11727520595741225 | counted=True | p_holm=0.8209264417018858 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=sarvam-1 | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.895 | acc_b=0.765 | diff=0.13 | ci=[0.06499999761581421, 0.19499999284744263] | a_only=37 | b_only=11 | p=0.0002222449626216872 | counted=True | p_holm=0.0020002046635951847 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=sarvam-1 | contrast=L3 | a=natural | b=lossy | n=198 | acc_a=0.8939393939393939 | acc_b=0.8939393939393939 | diff=0.0 | ci=[-0.04040404036641121, 0.04040404036641121] | a_only=8 | b_only=8 | p=1.0 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=gemma4-e2b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.57 | acc_b=0.755 | diff=-0.18500000000000005 | ci=[-0.25, -0.11999999731779099] | a_only=6 | b_only=43 | p=5.7277652842913085e-08 | counted=True | p_holm=6.300541812720439e-07 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=gemma4-e2b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.79 | acc_b=0.57 | diff=0.22000000000000008 | ci=[0.1550000011920929, 0.2849999964237213] | a_only=50 | b_only=6 | p=1.0182093779231849e-09 | counted=True | p_holm=1.2218512535078219e-08 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=gemma4-e2b | contrast=L3 | a=natural | b=lossy | n=198 | acc_a=0.803030303030303 | acc_b=0.7878787878787878 | diff=0.015151515151515138 | ci=[-0.035353533923625946, 0.06565656512975693] | a_only=14 | b_only=11 | p=0.6900379657745361 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen3-1.7b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.49 | acc_b=0.535 | diff=-0.04500000000000004 | ci=[-0.14499999582767487, 0.05000000074505806] | a_only=44 | b_only=53 | p=0.41677484108909885 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen3-1.7b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.57 | acc_b=0.49 | diff=0.07999999999999996 | ci=[-0.019999999552965164, 0.18000000715255737] | a_only=61 | b_only=45 | p=0.14478233933005036 | counted=True | p_holm=0.8686940359803021 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen3-1.7b | contrast=L3 | a=natural | b=lossy | n=198 | acc_a=0.5606060606060606 | acc_b=0.5656565656565656 | diff=-0.005050505050505083 | ci=[-0.07575757801532745, 0.06565656512975693] | a_only=26 | b_only=27 | p=1.0 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib | model=qwen2.5-1.5b | contrast=L1 | a=lower | b=itrans | n=1004 | acc_a=0.2749003984063745 | acc_b=0.2778884462151394 | diff=-0.0029880478087649376 | ci=[-0.03187251091003418, 0.02589641511440277] | a_only=110 | b_only=113 | p=0.8934971214685691 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib | model=qwen2.5-1.5b | contrast=L2 | a=lossy | b=lower | n=1004 | acc_a=0.3665338645418327 | acc_b=0.2749003984063745 | diff=0.0916334661354582 | ci=[0.060756973922252655, 0.12450199574232101] | a_only=181 | b_only=89 | p=2.2575435560775137e-08 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=qwen3.5-2b | contrast=L1 | a=lower | b=itrans | n=1004 | acc_a=0.2958167330677291 | acc_b=0.2410358565737052 | diff=0.05478087649402391 | ci=[0.02589641511440277, 0.08366534113883972] | a_only=135 | b_only=80 | p=0.00021464778366412355 | counted=True | p_holm=0.0008585911346564942 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=qwen3.5-2b | contrast=L2 | a=lossy | b=lower | n=1004 | acc_a=0.3754980079681275 | acc_b=0.2958167330677291 | diff=0.07968127490039839 | ci=[0.04780876636505127, 0.11155378818511963] | a_only=172 | b_only=92 | p=9.679764898638525e-07 | counted=True | p_holm=5.807858939183115e-06 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=sarvam-1 | contrast=L1 | a=lower | b=itrans | n=1004 | acc_a=0.4960159362549801 | acc_b=0.5388446215139442 | diff=-0.042828685258964105 | ci=[-0.07370518147945404, -0.011952191591262817] | a_only=107 | b_only=150 | p=0.008667040755707438 | counted=True | p_holm=0.017334081511414877 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=sarvam-1 | contrast=L2 | a=lossy | b=lower | n=1004 | acc_a=0.7051792828685259 | acc_b=0.4960159362549801 | diff=0.20916334661354585 | ci=[0.17629481852054596, 0.24302789568901062] | a_only=270 | b_only=60 | p=5.9732270627569956e-33 | counted=True | p_holm=4.7785816502055964e-32 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=gemma4-e2b | contrast=L1 | a=lower | b=itrans | n=1004 | acc_a=0.41434262948207173 | acc_b=0.3665338645418327 | diff=0.04780876494023906 | ci=[0.016932271420955658, 0.07968127727508545] | a_only=151 | b_only=103 | p=0.0031107066373511688 | counted=True | p_holm=0.009332119912053505 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=gemma4-e2b | contrast=L2 | a=lossy | b=lower | n=1004 | acc_a=0.49701195219123506 | acc_b=0.41434262948207173 | diff=0.08266932270916333 | ci=[0.05179283022880554, 0.11354582011699677] | a_only=171 | b_only=88 | p=2.780977551599325e-07 | counted=True | p_holm=1.9466842861195277e-06 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=qwen3-1.7b | contrast=L1 | a=lower | b=itrans | n=1004 | acc_a=0.2410358565737052 | acc_b=0.2400398406374502 | diff=0.0009960159362549792 | ci=[-0.02589641511440277, 0.02689243108034134] | a_only=87 | b_only=86 | p=0.9999999999999996 | counted=True | p_holm=0.9999999999999996 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib | model=qwen3-1.7b | contrast=L2 | a=lossy | b=lower | n=1004 | acc_a=0.30677290836653387 | acc_b=0.2410358565737052 | diff=0.06573705179282868 | ci=[0.03784860670566559, 0.09462151676416397] | a_only=139 | b_only=73 | p=6.8395812435670525e-06 | counted=True | p_holm=3.419790621783526e-05 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib_L3_secondary | model=qwen2.5-1.5b | contrast=L3 | a=natural257 | b=lossy | n=257 | acc_a=0.4591439688715953 | acc_b=0.3852140077821012 | diff=0.07392996108949412 | ci=[0.019455252215266228, 0.1284046620130539] | a_only=36 | b_only=17 | p=0.012660335802414213 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib_L3_secondary | model=qwen3.5-2b | contrast=L3 | a=natural257 | b=lossy | n=257 | acc_a=0.45525291828793774 | acc_b=0.42023346303501946 | diff=0.035019455252918275 | ci=[-0.011673151515424252, 0.08560311049222946] | a_only=25 | b_only=16 | p=0.21102359760880063 | counted=True | p_holm=0.21102359760880063 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib_L3_secondary | model=sarvam-1 | contrast=L3 | a=natural257 | b=lossy | n=257 | acc_a=0.7276264591439688 | acc_b=0.669260700389105 | diff=0.05836575875486383 | ci=[0.015564202331006527, 0.10505836457014084] | a_only=25 | b_only=10 | p=0.016673847800120715 | counted=True | p_holm=0.06669539120048286 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=sib_L3_secondary | model=gemma4-e2b | contrast=L3 | a=natural257 | b=lossy | n=257 | acc_a=0.5447470817120622 | acc_b=0.48638132295719844 | diff=0.05836575875486377 | ci=[0.0, 0.11673151701688766] | a_only=36 | b_only=21 | p=0.06273668035582848 | counted=True | p_holm=0.12547336071165696 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib_L3_secondary | model=qwen3-1.7b | contrast=L3 | a=natural257 | b=lossy | n=257 | acc_a=0.36964980544747084 | acc_b=0.3151750972762646 | diff=0.054474708171206254 | ci=[0.0077821011655032635, 0.10116731375455856] | a_only=26 | b_only=12 | p=0.03355243967962451 | counted=True | p_holm=0.10065731903887354 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=xnli_reported_only | model=qwen2.5-1.5b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.33 | acc_b=0.32 | diff=0.010000000000000009 | ci=[-0.05000000074505806, 0.06499999761581421] | a_only=18 | b_only=16 | p=0.8641662404406816 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen2.5-1.5b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.325 | acc_b=0.33 | diff=-0.0050000000000000044 | ci=[-0.054999999701976776, 0.04500000178813934] | a_only=13 | b_only=14 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen2.5-1.5b | contrast=L3 | a=natural | b=lossy | n=193 | acc_a=0.32124352331606215 | acc_b=0.32642487046632124 | diff=-0.005181347150259086 | ci=[-0.062176164239645004, 0.05181347206234932] | a_only=15 | b_only=16 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3.5-2b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.345 | acc_b=0.34 | diff=0.004999999999999949 | ci=[0.0, 0.014999999664723873] | a_only=1 | b_only=0 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3.5-2b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.335 | acc_b=0.345 | diff=-0.009999999999999953 | ci=[-0.02500000037252903, 0.0] | a_only=0 | b_only=2 | p=0.5 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3.5-2b | contrast=L3 | a=natural | b=lossy | n=193 | acc_a=0.34196891191709844 | acc_b=0.33678756476683935 | diff=0.005181347150259086 | ci=[0.0, 0.015544041059911251] | a_only=1 | b_only=0 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=sarvam-1 | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.365 | acc_b=0.385 | diff=-0.020000000000000018 | ci=[-0.06499999761581421, 0.029999999329447746] | a_only=10 | b_only=14 | p=0.5412561893463135 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=sarvam-1 | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.47 | acc_b=0.365 | diff=0.10499999999999998 | ci=[0.04500000178813934, 0.16500000655651093] | a_only=30 | b_only=9 | p=0.0010650196345523 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=xnli_reported_only | model=sarvam-1 | contrast=L3 | a=natural | b=lossy | n=193 | acc_a=0.46632124352331605 | acc_b=0.48186528497409326 | diff=-0.015544041450777202 | ci=[-0.062176164239645004, 0.031088082119822502] | a_only=9 | b_only=12 | p=0.6636238098144531 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=gemma4-e2b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.38 | acc_b=0.41 | diff=-0.02999999999999997 | ci=[-0.06499999761581421, 0.004999999888241291] | a_only=4 | b_only=10 | p=0.1795654296875 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=gemma4-e2b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.4 | acc_b=0.38 | diff=0.020000000000000018 | ci=[-0.02500000037252903, 0.06499999761581421] | a_only=12 | b_only=8 | p=0.5034446716308594 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=gemma4-e2b | contrast=L3 | a=natural | b=lossy | n=193 | acc_a=0.40414507772020725 | acc_b=0.40414507772020725 | diff=0.0 | ci=[-0.05181347206234932, 0.05181347206234932] | a_only=12 | b_only=12 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3-1.7b | contrast=L1 | a=lower | b=itrans | n=200 | acc_a=0.335 | acc_b=0.335 | diff=0.0 | ci=[0.0, 0.0] | a_only=0 | b_only=0 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3-1.7b | contrast=L2 | a=lossy | b=lower | n=200 | acc_a=0.335 | acc_b=0.335 | diff=0.0 | ci=[0.0, 0.0] | a_only=0 | b_only=0 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3-1.7b | contrast=L3 | a=natural | b=lossy | n=193 | acc_a=0.34196891191709844 | acc_b=0.33678756476683935 | diff=0.005181347150259086 | ci=[0.0, 0.015544041059911251] | a_only=1 | b_only=0 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
Result entry: 2026-10-22 — Romanization ladder L1–L3 (registered 2026-10-22): results [RESULTS.md 1523-1578, `64ca06d` 2026-10-22 03:14:00 +0530]
Source files: results/l_ladder/verdict.json; results/l_ladder/contrasts.csv

### NC: NC1: non-canonical tokenization of lossy text
Registered: PRE-REGISTRATION — NC1: non-canonical tokenization of lossy text (written 2026-10-22, the lead author's design; before any NC1 code is written, run or scored) [RESULTS.md 1615-1675, `e50581c` 2026-10-22 18:06:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: nc_a, nc_b, nc_c, lossy, lower, itrans, english, natural, a, b, c; tasks/measures: sib, xnli, sentiment, retrieval, xnli_reported_only; seeds: not recorded as a column or key in the result files
Table [nc1/verdict.json] (6 records):
  NC-F|retrieval | verdict="no effect detected"; status="registered prediction: positive"; n_significant_positive=1; n_significant_negative=0; needed=2; n_counted=3; tpw_check_b_failed_models=[]; ci_holm_disagreements=["qwen3.5-2b"]
  NC-O|retrieval | verdict="effect, positive"; status="reported, no prediction"; n_significant_positive=2; n_significant_negative=0; needed=2; n_counted=3; tpw_check_b_failed_models=[]; ci_holm_disagreements=[]
  NC-F|sentiment | verdict="no effect detected"; status="registered prediction: positive"; n_significant_positive=0; n_significant_negative=0; needed=3; n_counted=4; tpw_check_b_failed_models=[]; ci_holm_disagreements=[]
  NC-O|sentiment | verdict="no effect detected"; status="reported, no prediction"; n_significant_positive=2; n_significant_negative=0; needed=3; n_counted=4; tpw_check_b_failed_models=[]; ci_holm_disagreements=["gemma4-e2b"]
  NC-F|sib | verdict="no effect detected"; status="registered prediction: positive"; n_significant_positive=1; n_significant_negative=0; needed=3; n_counted=4; tpw_check_b_failed_models=[]; ci_holm_disagreements=["gemma4-e2b"]
  NC-O|sib | verdict="effect, positive"; status="reported, no prediction"; n_significant_positive=3; n_significant_negative=0; needed=3; n_counted=4; tpw_check_b_failed_models=[]; ci_holm_disagreements=[]
Table [nc1/contrasts.csv] (38 rows of 38):
  measure=retrieval | model=qwen2.5-1.5b | contrast=NC-F | a=c | b=b | n=248 | acc_a=0.18548387096774194 | acc_b=0.14112903225806453 | diff=0.04435483870967741 | ci=[0.008064515888690948, 0.08064515888690948] | a_only=17 | b_only=6 | p=0.03468966484069824 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=qwen2.5-1.5b | contrast=NC-O | a=a | b=c | n=248 | acc_a=0.20161290322580644 | acc_b=0.18548387096774194 | diff=0.016129032258064502 | ci=[-0.02016128972172737, 0.052419353276491165] | a_only=12 | b_only=8 | p=0.5034446716308594 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=retrieval | model=qwen3.5-2b | contrast=NC-F | a=c | b=b | n=248 | acc_a=0.3790322580645161 | acc_b=0.3064516129032258 | diff=0.07258064516129031 | ci=[0.012096773833036423, 0.12913306057453156] | a_only=38 | b_only=20 | p=0.024746035842440804 | counted=True | p_holm=0.0742381075273224 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=retrieval | model=qwen3.5-2b | contrast=NC-O | a=a | b=c | n=248 | acc_a=0.375 | acc_b=0.3790322580645161 | diff=-0.0040322580645161255 | ci=[-0.060483869165182114, 0.052419353276491165] | a_only=25 | b_only=26 | p=1.0 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=retrieval | model=sarvam-1 | contrast=NC-F | a=c | b=b | n=248 | acc_a=0.75 | acc_b=0.6330645161290323 | diff=0.11693548387096775 | ci=[0.06451612710952759, 0.1733870953321457] | a_only=40 | b_only=11 | p=5.703811637403078e-05 | counted=True | p_holm=0.00022815246549612311 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=sarvam-1 | contrast=NC-O | a=a | b=c | n=248 | acc_a=0.8830645161290323 | acc_b=0.75 | diff=0.13306451612903225 | ci=[0.08860886842012405, 0.18145161867141724] | a_only=36 | b_only=3 | p=3.608874976634979e-08 | counted=True | p_holm=2.1653249859809875e-07 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=retrieval | model=gemma4-e2b | contrast=NC-F | a=c | b=b | n=248 | acc_a=0.41935483870967744 | acc_b=0.4637096774193548 | diff=-0.04435483870967738 | ci=[-0.10483870655298233, 0.016129031777381897] | a_only=23 | b_only=34 | p=0.18485048241641844 | counted=True | p_holm=0.3697009648328369 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=retrieval | model=gemma4-e2b | contrast=NC-O | a=a | b=c | n=248 | acc_a=0.5725806451612904 | acc_b=0.41935483870967744 | diff=0.15322580645161293 | ci=[0.10080645233392715, 0.20564515888690948] | a_only=46 | b_only=8 | p=1.38433549734529e-07 | counted=True | p_holm=6.921677486726451e-07 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=qwen2.5-1.5b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.485 | acc_b=0.51 | diff=-0.025000000000000022 | ci=[-0.05000000074505806, -0.004999999888241291] | a_only=0 | b_only=5 | p=0.0625 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=qwen2.5-1.5b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.5 | acc_b=0.485 | diff=0.015000000000000013 | ci=[-0.004999999888241291, 0.03999999910593033] | a_only=4 | b_only=1 | p=0.375 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen3.5-2b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.575 | acc_b=0.59 | diff=-0.015000000000000013 | ci=[-0.07000000029802322, 0.03999999910593033] | a_only=15 | b_only=18 | p=0.7283324808813632 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen3.5-2b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.68 | acc_b=0.575 | diff=0.1050000000000001 | ci=[0.04500000178813934, 0.16500000655651093] | a_only=31 | b_only=10 | p=0.0014504910141113214 | counted=True | p_holm=0.01015343709877925 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=sarvam-1 | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.74 | acc_b=0.795 | diff=-0.05500000000000005 | ci=[-0.125, 0.014999999664723873] | a_only=18 | b_only=29 | p=0.14386508844054896 | counted=True | p_holm=0.7193254422027449 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=sarvam-1 | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.895 | acc_b=0.74 | diff=0.15500000000000003 | ci=[0.0949999988079071, 0.2199999988079071] | a_only=39 | b_only=8 | p=5.539621596994947e-06 | counted=True | p_holm=4.431697277595958e-05 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sentiment | model=gemma4-e2b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.735 | acc_b=0.75 | diff=-0.015000000000000013 | ci=[-0.06499999761581421, 0.03500000014901161] | a_only=12 | b_only=15 | p=0.7011080384254456 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=gemma4-e2b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.79 | acc_b=0.735 | diff=0.05500000000000005 | ci=[0.004999999888241291, 0.10000000149011612] | a_only=18 | b_only=7 | p=0.043285250663757324 | counted=True | p_holm=0.25971150398254395 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=sentiment | model=qwen3-1.7b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.6 | acc_b=0.555 | diff=0.04499999999999993 | ci=[-0.029999999329447746, 0.11999999731779099] | a_only=35 | b_only=26 | p=0.30567741986311836 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sentiment | model=qwen3-1.7b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.57 | acc_b=0.6 | diff=-0.030000000000000027 | ci=[-0.10000000149011612, 0.03999999910593033] | a_only=23 | b_only=29 | p=0.48845566937989204 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen2.5-1.5b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.365 | acc_b=0.38 | diff=-0.015000000000000013 | ci=[-0.05999999865889549, 0.029999999329447746] | a_only=8 | b_only=11 | p=0.6476058959960938 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen2.5-1.5b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.325 | acc_b=0.365 | diff=-0.03999999999999998 | ci=[-0.08500000089406967, 0.004999999888241291] | a_only=6 | b_only=14 | p=0.11531829833984375 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3.5-2b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.335 | acc_b=0.34 | diff=-0.0050000000000000044 | ci=[-0.014999999664723873, 0.0] | a_only=0 | b_only=1 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3.5-2b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.335 | acc_b=0.335 | diff=0.0 | ci=[0.0, 0.0] | a_only=0 | b_only=0 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=sarvam-1 | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.365 | acc_b=0.39 | diff=-0.025000000000000022 | ci=[-0.07999999821186066, 0.03500000014901161] | a_only=15 | b_only=20 | p=0.4995598332025112 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=sarvam-1 | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.47 | acc_b=0.365 | diff=0.10499999999999998 | ci=[0.03999999910593033, 0.17000000178813934] | a_only=33 | b_only=12 | p=0.002458900322096724 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=xnli_reported_only | model=gemma4-e2b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.39 | acc_b=0.4 | diff=-0.010000000000000009 | ci=[-0.04500000178813934, 0.02500000037252903] | a_only=5 | b_only=7 | p=0.7744140625 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=gemma4-e2b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.4 | acc_b=0.39 | diff=0.010000000000000009 | ci=[-0.029999999329447746, 0.05000000074505806] | a_only=9 | b_only=7 | p=0.803619384765625 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3-1.7b | contrast=NC-F | a=c | b=b | n=200 | acc_a=0.33 | acc_b=0.33 | diff=0.0 | ci=[-0.02500000037252903, 0.02500000037252903] | a_only=3 | b_only=3 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=xnli_reported_only | model=qwen3-1.7b | contrast=NC-O | a=a | b=c | n=200 | acc_a=0.335 | acc_b=0.33 | diff=0.0050000000000000044 | ci=[-0.009999999776482582, 0.019999999552965164] | a_only=2 | b_only=1 | p=1.0 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib | model=qwen2.5-1.5b | contrast=NC-F | a=c | b=b | n=1004 | acc_a=0.33266932270916333 | acc_b=0.3426294820717131 | diff=-0.009960159362549792 | ci=[-0.0348854586482048, 0.014940239489078522] | a_only=81 | b_only=91 | p=0.4926722176485527 | counted=False | p_holm= | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib | model=qwen2.5-1.5b | contrast=NC-O | a=a | b=c | n=1004 | acc_a=0.3665338645418327 | acc_b=0.33266932270916333 | diff=0.03386454183266935 | ci=[0.008964143693447113, 0.05779382586479187] | a_only=99 | b_only=65 | p=0.009756084718005844 | counted=False | p_holm= | significant=False | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=qwen3.5-2b | contrast=NC-F | a=c | b=b | n=1004 | acc_a=0.3107569721115538 | acc_b=0.2948207171314741 | diff=0.015936254980079667 | ci=[-0.009960159659385681, 0.04282868653535843] | a_only=96 | b_only=80 | p=0.25813376128396426 | counted=True | p_holm=0.7744012838518928 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib | model=qwen3.5-2b | contrast=NC-O | a=a | b=c | n=1004 | acc_a=0.3754980079681275 | acc_b=0.3107569721115538 | diff=0.0647410358565737 | ci=[0.039840638637542725, 0.08964143693447113] | a_only=117 | b_only=52 | p=6.272187854845746e-07 | counted=True | p_holm=3.7633127129074476e-06 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=sarvam-1 | contrast=NC-F | a=c | b=b | n=1004 | acc_a=0.5348605577689243 | acc_b=0.47808764940239046 | diff=0.056772908366533814 | ci=[0.027888447046279907, 0.08366534113883972] | a_only=134 | b_only=77 | p=0.00010581242072765762 | counted=True | p_holm=0.0005290621036382881 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=sarvam-1 | contrast=NC-O | a=a | b=c | n=1004 | acc_a=0.7051792828685259 | acc_b=0.5348605577689243 | diff=0.17031872509960166 | ci=[0.1404382437467575, 0.20119522511959076] | a_only=222 | b_only=51 | p=1.3151471164170837e-26 | counted=True | p_holm=1.052117693133667e-25 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=gemma4-e2b | contrast=NC-F | a=c | b=b | n=1004 | acc_a=0.42330677290836655 | acc_b=0.45119521912350596 | diff=-0.027888446215139417 | ci=[-0.054780878126621246, -0.0009960159659385681] | a_only=83 | b_only=111 | p=0.052283117673361953 | counted=True | p_holm=0.20913247069344781 | significant=False | ci_excludes_0=True | ci_holm_disagree=True
  measure=sib | model=gemma4-e2b | contrast=NC-O | a=a | b=c | n=1004 | acc_a=0.49701195219123506 | acc_b=0.42330677290836655 | diff=0.07370517928286852 | ci=[0.04780876636505127, 0.09960159659385681] | a_only=133 | b_only=59 | p=9.662849171339736e-08 | counted=True | p_holm=6.763994419937815e-07 | significant=True | ci_excludes_0=True | ci_holm_disagree=False
  measure=sib | model=qwen3-1.7b | contrast=NC-F | a=c | b=b | n=1004 | acc_a=0.30378486055776893 | acc_b=0.29780876494023906 | diff=0.005976095617529875 | ci=[-0.017928287386894226, 0.029880478978157043] | a_only=78 | b_only=72 | p=0.6832317601040961 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
  measure=sib | model=qwen3-1.7b | contrast=NC-O | a=a | b=c | n=1004 | acc_a=0.30677290836653387 | acc_b=0.30378486055776893 | diff=0.0029880478087649376 | ci=[-0.019920319318771362, 0.02689243108034134] | a_only=73 | b_only=70 | p=0.8672499070976049 | counted=True | p_holm=1.0 | significant=False | ci_excludes_0=False | ci_holm_disagree=False
Result entry: PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by the lead author with changes; before any patching code is written or run) [RESULTS.md 2436-2471, `6867631` 2026-10-23 16:00:59 +0530]
Source files: results/nc1/verdict.json; results/nc1/contrasts.csv

### K: Kanglish, annotation, K1 to K3, K3b, natural+dbl, V-VER, K2b
Registered: PRE-REGISTRATION — Kanglish and human-corrected natural romanization: K1–K3 (written 2026-10-16, before any Kanglish draft exists and before any scoring) [RESULTS.md 869-947, `d21d633` 2026-10-16 02:59:11 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: natural, k_kan_ver, k_nat_ver, k_kan_draft, k_nat_draft, natural_dbl, natural_dbl257, natural_verified, natural_verified257; tasks/measures: sib, sentiment, sib257, retrieval; seeds: 6, 26
Table [k3b/verdict.json] (4 records):
  (top) | K3b="refuted"; n=493; n_primary_defective_excluded=7
  statistics.vowel_doubling | gemini_rate=0.01626761826917326; human_rate=0.045342854948936494; ratio=0.358769166332673; ci90=[0.32414029872728917, 0.39481366675250124]; ci95=[0.31827503247469824, 0.40161500348221796]; verdict="differs (Gemini lower)"
  statistics.h_digraph | gemini_rate=0.017782739578557045; human_rate=0.01696997619596099; ratio=1.0478941969753321; ci90=[0.9834651630457045, 1.1151838743372948]; ci95=[0.9713704942340576, 1.1287855684470784]; verdict="matches"
  statistics.english_word_share | gemini_rate=0.060409556313993175; human_rate=0.06750982737993505; ratio=0.8948261113751242; ci90=[0.823589997261118, 0.9675963977440726]; ci95=[0.8102824367013685, 0.981258846870941]; verdict="matches"
Table [k12/verdict.json] (4 records):
  (top) | K1="inconclusive"; K1_n_informative=10; K1_n_significant_positive=5; K2a_differs_v1_v2=false; K2b_differs_v1_v2=false; primary_tagger="v2 (codemix_v2 with KN_FORCE 'ee'); v1 = registered tagger, sensitivity"
  K2a | v2="supported"; v1="supported"
  K2a_n_counted | v2=10; v1=10
  K2b | v2="supported"; v1="supported"
Table [k12/k1.csv] (20 rows of 20):
  model=qwen2.5-1.5b | task=sentiment | comparison=primary | informative=True | n=200 | acc_kanglish=0.645 | acc_natural=0.515 | diff=0.13 | ci_low=0.07999999821186066 | ci_high=0.1850000023841858 | p=2.5560148060321808e-06 | p_holm=1.7892103642225266e-05
  model=qwen2.5-1.5b | task=sentiment | comparison=secondary_drafts | informative=True | n=200 | acc_kanglish=0.63 | acc_natural=0.52 | diff=0.10999999999999999 | ci_low=0.05999999865889549 | ci_high=0.1599999964237213 | p=2.744048833847046e-05 | p_holm=
  model=qwen3.5-2b | task=sentiment | comparison=primary | informative=True | n=200 | acc_kanglish=0.805 | acc_natural=0.72 | diff=0.08500000000000008 | ci_low=0.019999999552965164 | ci_high=0.15000000596046448 | p=0.016094360031274842 | p_holm=0.08047180015637422
  model=qwen3.5-2b | task=sentiment | comparison=secondary_drafts | informative=True | n=200 | acc_kanglish=0.795 | acc_natural=0.725 | diff=0.07000000000000006 | ci_low=0.004999999888241291 | ci_high=0.13500000536441803 | p=0.054076031858869555 | p_holm=
  model=sarvam-1 | task=sentiment | comparison=primary | informative=True | n=200 | acc_kanglish=0.85 | acc_natural=0.895 | diff=-0.04500000000000004 | ci_low=-0.08500000089406967 | ci_high=-0.004999999888241291 | p=0.049041748046875 | p_holm=0.147125244140625
  model=sarvam-1 | task=sentiment | comparison=secondary_drafts | informative=True | n=200 | acc_kanglish=0.84 | acc_natural=0.895 | diff=-0.05500000000000005 | ci_low=-0.10000000149011612 | ci_high=-0.009999999776482582 | p=0.02660369873046875 | p_holm=
  model=gemma4-e2b | task=sentiment | comparison=primary | informative=True | n=200 | acc_kanglish=0.82 | acc_natural=0.81 | diff=0.009999999999999898 | ci_low=-0.04500000178813934 | ci_high=0.06499999761581421 | p=0.8641662404406816 | p_holm=1.0
  model=gemma4-e2b | task=sentiment | comparison=secondary_drafts | informative=True | n=200 | acc_kanglish=0.82 | acc_natural=0.805 | diff=0.014999999999999902 | ci_low=-0.03999999910593033 | ci_high=0.07000000029802322 | p=0.735878800856881 | p_holm=
  model=qwen3-1.7b | task=sentiment | comparison=primary | informative=True | n=200 | acc_kanglish=0.67 | acc_natural=0.585 | diff=0.08500000000000008 | ci_low=0.009999999776482582 | ci_high=0.1599999964237213 | p=0.036343179957053884 | p_holm=0.14537271982821554
  model=qwen3-1.7b | task=sentiment | comparison=secondary_drafts | informative=True | n=200 | acc_kanglish=0.65 | acc_natural=0.565 | diff=0.08500000000000008 | ci_low=0.009999999776482582 | ci_high=0.1599999964237213 | p=0.03314396778750544 | p_holm=
  model=qwen2.5-1.5b | task=sib | comparison=primary | informative=True | n=300 | acc_kanglish=0.63 | acc_natural=0.49333333333333335 | diff=0.13666666666666666 | ci_low=0.0833333358168602 | ci_high=0.1899999976158142 | p=1.5256583158538737e-06 | p_holm=1.220526652683099e-05
  model=qwen2.5-1.5b | task=sib | comparison=secondary_drafts | informative=True | n=300 | acc_kanglish=0.6266666666666667 | acc_natural=0.49333333333333335 | diff=0.13333333333333336 | ci_low=0.0833333358168602 | ci_high=0.18666666746139526 | p=1.652519847797991e-06 | p_holm=
  model=qwen3.5-2b | task=sib | comparison=primary | informative=True | n=300 | acc_kanglish=0.5966666666666667 | acc_natural=0.44666666666666666 | diff=0.15000000000000002 | ci_low=0.09666666388511658 | ci_high=0.20666666328907013 | p=2.4176312825015983e-07 | p_holm=2.1758681542514384e-06
  model=qwen3.5-2b | task=sib | comparison=secondary_drafts | informative=True | n=300 | acc_kanglish=0.5933333333333334 | acc_natural=0.44666666666666666 | diff=0.14666666666666672 | ci_low=0.09333333373069763 | ci_high=0.20000000298023224 | p=5.663739625418237e-07 | p_holm=
  model=sarvam-1 | task=sib | comparison=primary | informative=True | n=300 | acc_kanglish=0.7633333333333333 | acc_natural=0.7533333333333333 | diff=0.010000000000000009 | ci_low=-0.02666666731238365 | ci_high=0.05000000074505806 | p=0.735878800856881 | p_holm=1.0
  model=sarvam-1 | task=sib | comparison=secondary_drafts | informative=True | n=300 | acc_kanglish=0.76 | acc_natural=0.7533333333333333 | diff=0.00666666666666671 | ci_low=-0.03333333507180214 | ci_high=0.046666666865348816 | p=0.8714146793645341 | p_holm=
  model=gemma4-e2b | task=sib | comparison=primary | informative=True | n=300 | acc_kanglish=0.6866666666666666 | acc_natural=0.5933333333333334 | diff=0.09333333333333327 | ci_low=0.04333333298563957 | ci_high=0.1433333307504654 | p=0.0004970915863810334 | p_holm=0.0029825495182862006
  model=gemma4-e2b | task=sib | comparison=secondary_drafts | informative=True | n=300 | acc_kanglish=0.68 | acc_natural=0.5866666666666667 | diff=0.09333333333333338 | ci_low=0.04333333298563957 | ci_high=0.1433333307504654 | p=0.0004970915863810334 | p_holm=
  model=qwen3-1.7b | task=sib | comparison=primary | informative=True | n=300 | acc_kanglish=0.5633333333333334 | acc_natural=0.38666666666666666 | diff=0.1766666666666667 | ci_low=0.12333333492279053 | ci_high=0.23000000417232513 | p=3.108521862394645e-10 | p_holm=3.1085218623946452e-09
  model=qwen3-1.7b | task=sib | comparison=secondary_drafts | informative=True | n=300 | acc_kanglish=0.5633333333333334 | acc_natural=0.38333333333333336 | diff=0.18 | ci_low=0.12999999523162842 | ci_high=0.23000000417232513 | p=8.957423581215867e-11 | p_holm=
Table [k12/k2a.csv] (20 rows of 20):
  tagger=v2 | model=qwen2.5-1.5b | task=sentiment | n=200 | coef_english_share=0.8084371367667522 | p_one_sided=7.678591990657368e-06 | constant_label_rate=0.825 | counted=True | p_holm=6.142873592525895e-05
  tagger=v1 | model=qwen2.5-1.5b | task=sentiment | n=200 | coef_english_share=0.7753630013222352 | p_one_sided=1.490030019242173e-05 | constant_label_rate=0.825 | counted=True | p_holm=8.940180115453038e-05
  tagger=v2 | model=qwen3.5-2b | task=sentiment | n=200 | coef_english_share=0.47030151049381463 | p_one_sided=0.007842919255183678 | constant_label_rate=0.535 | counted=True | p_holm=0.03137167702073471
  tagger=v1 | model=qwen3.5-2b | task=sentiment | n=200 | coef_english_share=0.4554861392353978 | p_one_sided=0.010234808577162793 | constant_label_rate=0.535 | counted=True | p_holm=0.04093923430865117
  tagger=v2 | model=sarvam-1 | task=sentiment | n=200 | coef_english_share=0.2494388047896516 | p_one_sided=0.1145075464372986 | constant_label_rate=0.62 | counted=True | p_holm=0.2290150928745972
  tagger=v1 | model=sarvam-1 | task=sentiment | n=200 | coef_english_share=0.21889988516361428 | p_one_sided=0.1437883934197025 | constant_label_rate=0.62 | counted=True | p_holm=0.1888377478769853
  tagger=v2 | model=gemma4-e2b | task=sentiment | n=200 | coef_english_share=0.3410396161710691 | p_one_sided=0.040510024947393856 | constant_label_rate=0.57 | counted=True | p_holm=0.12153007484218156
  tagger=v1 | model=gemma4-e2b | task=sentiment | n=200 | coef_english_share=0.27536626421445315 | p_one_sided=0.078719471713871 | constant_label_rate=0.57 | counted=True | p_holm=0.1888377478769853
  tagger=v2 | model=qwen3-1.7b | task=sentiment | n=200 | coef_english_share=0.7803296242863422 | p_one_sided=9.164682095283901e-06 | constant_label_rate=0.65 | counted=True | p_holm=6.415277466698731e-05
  tagger=v1 | model=qwen3-1.7b | task=sentiment | n=200 | coef_english_share=0.7986073086847726 | p_one_sided=8.294853573122715e-06 | constant_label_rate=0.65 | counted=True | p_holm=5.8063975011859e-05
  tagger=v2 | model=qwen2.5-1.5b | task=sib | n=300 | coef_english_share=0.5452765173677874 | p_one_sided=8.124501378819961e-05 | constant_label_rate=0.20666666666666667 | counted=True | p_holm=0.00048747008272919767
  tagger=v1 | model=qwen2.5-1.5b | task=sib | n=300 | coef_english_share=0.686879343445831 | p_one_sided=2.49788900115909e-06 | constant_label_rate=0.20666666666666667 | counted=True | p_holm=1.998311200927272e-05
  tagger=v2 | model=qwen3.5-2b | task=sib | n=300 | coef_english_share=0.701699738776044 | p_one_sided=8.377698447870186e-07 | constant_label_rate=0.24666666666666667 | counted=True | p_holm=8.377698447870186e-06
  tagger=v1 | model=qwen3.5-2b | task=sib | n=300 | coef_english_share=0.7779797735793113 | p_one_sided=1.1137733110520808e-07 | constant_label_rate=0.24666666666666667 | counted=True | p_holm=1.0023959799468728e-06
  tagger=v2 | model=sarvam-1 | task=sib | n=300 | coef_english_share=0.17922685923621487 | p_one_sided=0.11739136867463945 | constant_label_rate=0.20333333333333334 | counted=True | p_holm=0.2290150928745972
  tagger=v1 | model=sarvam-1 | task=sib | n=300 | coef_english_share=0.23304294974658654 | p_one_sided=0.0629459159589951 | constant_label_rate=0.20333333333333334 | counted=True | p_holm=0.1888377478769853
  tagger=v2 | model=gemma4-e2b | task=sib | n=300 | coef_english_share=0.4275304077333724 | p_one_sided=0.0015241541374322774 | constant_label_rate=0.24333333333333335 | counted=True | p_holm=0.007620770687161387
  tagger=v1 | model=gemma4-e2b | task=sib | n=300 | coef_english_share=0.4407088947756835 | p_one_sided=0.0011569492396341385 | constant_label_rate=0.24333333333333335 | counted=True | p_holm=0.005784746198170692
  tagger=v2 | model=qwen3-1.7b | task=sib | n=300 | coef_english_share=0.6677690439199794 | p_one_sided=1.4760720459074671e-06 | constant_label_rate=0.28 | counted=True | p_holm=1.3284648413167204e-05
  tagger=v1 | model=qwen3-1.7b | task=sib | n=300 | coef_english_share=0.8920671926688742 | p_one_sided=3.164154916814838e-09 | constant_label_rate=0.28 | counted=True | p_holm=3.164154916814838e-08
Table [k12/k2b.csv] (8 rows of 8):
  tagger=v2 | model=qwen2.5-1.5b | layer=15 | n=300 | median_rank=63.0 | coef_english_share=0.9671966090266525 | p_one_sided=2.5639168505065217e-18 | p_holm=5.1278337010130434e-18
  tagger=v1 | model=qwen2.5-1.5b | layer=15 | n=300 | median_rank=63.0 | coef_english_share=1.118560300916038 | p_one_sided=2.0381549816824252e-24 | p_holm=4.0763099633648504e-24
  tagger=v2 | model=qwen3.5-2b | layer=15 | n=300 | median_rank=66.0 | coef_english_share=1.200350817696526 | p_one_sided=1.220650753598434e-23 | p_holm=3.661952260795302e-23
  tagger=v1 | model=qwen3.5-2b | layer=15 | n=300 | median_rank=66.0 | coef_english_share=1.3665876362343665 | p_one_sided=4.820755556842525e-31 | p_holm=1.4462266670527574e-30
  tagger=v2 | model=sarvam-1 | layer=23 | n=300 | median_rank=6.0 | coef_english_share=0.8309962219824116 | p_one_sided=8.852693837107346e-10 | p_holm=8.852693837107346e-10
  tagger=v1 | model=sarvam-1 | layer=23 | n=300 | median_rank=6.0 | coef_english_share=1.0444505431462798 | p_one_sided=9.390169768266736e-15 | p_holm=9.390169768266736e-15
  tagger=v2 | model=gemma4-e2b | layer=7 | n=300 | median_rank=20.0 | coef_english_share=1.5466855700507325 | p_one_sided=1.1065700930642643e-34 | p_holm=4.426280372257057e-34
  tagger=v1 | model=gemma4-e2b | layer=7 | n=300 | median_rank=20.0 | coef_english_share=1.7003515678446601 | p_one_sided=3.3539271304331167e-43 | p_holm=1.3415708521732467e-42
Table [v_dbl/summary.json] (6 records):
  differences[model=qwen3.5-2b] | measure="retrieval"; model="qwen3.5-2b"; n=248; acc_natural_dbl=0.5282258064516129; acc_natural=0.5120967741935484; diff=0.016129032258064502; ci_low=-0.032258063554763794; ci_high=0.06451612710952759; dbl_only=22; natural_only=18; p_mcnemar=0.6358280026288412; layer_natural=16.0; layer_natural_dbl=6.0
  differences[model=sarvam-1] | measure="retrieval"; model="sarvam-1"; n=248; acc_natural_dbl=0.9153225806451613; acc_natural=0.9193548387096774; diff=-0.0040322580645161255; ci_low=-0.02822580561041832; ci_high=0.02016128972172737; dbl_only=4; natural_only=5; p_mcnemar=1.0; layer_natural=18.0; layer_natural_dbl=17.0
  differences[model=gemma4-e2b] | measure="retrieval"; model="gemma4-e2b"; n=248; acc_natural_dbl=0.6935483870967742; acc_natural=0.7096774193548387; diff=-0.016129032258064502; ci_low=-0.04435483738780022; ci_high=0.012096773833036423; dbl_only=4; natural_only=8; p_mcnemar=0.3876953125; layer_natural=7.0; layer_natural_dbl=7.0
  differences[model=qwen3.5-2b] | measure="sib257"; model="qwen3.5-2b"; n=257; acc_natural_dbl=0.45136186770428016; acc_natural=0.45525291828793774; diff=-0.0038910505836575737; ci_low=-0.038910504430532455; ci_high=0.031128404662013054; dbl_only=9; natural_only=10; p_mcnemar=1.0; layer_natural=NaN; layer_natural_dbl=NaN
  differences[model=sarvam-1] | measure="sib257"; model="sarvam-1"; n=257; acc_natural_dbl=0.7237354085603113; acc_natural=0.7276264591439688; diff=-0.0038910505836575737; ci_low=-0.03501945361495018; ci_high=0.031128404662013054; dbl_only=9; natural_only=10; p_mcnemar=1.0; layer_natural=NaN; layer_natural_dbl=NaN
  differences[model=gemma4-e2b] | measure="sib257"; model="gemma4-e2b"; n=257; acc_natural_dbl=0.5214007782101168; acc_natural=0.5447470817120622; diff=-0.023346303501945442; ci_low=-0.06614785641431808; ci_high=0.015564202331006527; dbl_only=11; natural_only=17; p_mcnemar=0.34492845088243484; layer_natural=NaN; layer_natural_dbl=NaN
Result entry: 2026-10-30 — K3b-hi result; EXPERIMENT FREEZE (the lead author, 2026-10-30) [RESULTS.md 3322-3335, `f7ce5a8` 2026-10-30 08:18:15 +0530]
Source files: results/k3b/verdict.json; results/k12/verdict.json; results/k12/k1.csv; results/k12/k2a.csv; results/k12/k2b.csv; results/v_dbl/summary.json

### H: Hindi: H-Hindi, H1, H1-LF, K3b-hi, English-loan measures
Registered: PRE-REGISTRATION — Hindi natural romanization drafts and H-Hindi (written 2026-10-23 01:00 IST, the lead author's design; before any Hindi draft or Hindi model output exists) [RESULTS.md 2113-2232, `dcf9cfe` 2026-10-23 01:02:11 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: lossy, itrans, native, natural, natural1004; tasks/measures: sib, sentiment, en_words, has_name, kn_words, has_digit, kn_tokens, retrieval; seeds: 0, 1, 6
Table [h_hindi/h1_verdict.json] (3 records):
  retrieval | n_counted=3; needed=2; n_positive=2; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]; n_items=246; verdict="effect (H1 supported)"; ci_holm_disagreements=[]
  sentiment | n_counted=4; needed=3; n_positive=2; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]; n_items=197; verdict="refuted"; ci_holm_disagreements=["sarvam-1"]
  sib | n_counted=4; needed=3; n_positive=3; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]; n_items=256; verdict="effect (H1 supported)"; ci_holm_disagreements=[]
Table [h_hindi/h1.csv] (14 rows of 14):
  measure=retrieval | comparison=native-natural | model=qwen2.5-1.5b | counted=False | kannada_native=0.24390243902439024 | kannada_other=0.37398373983739835 | hindi_native=0.6951219512195121 | hindi_other=0.3943089430894309 | n=246 | diff_of_gaps=-0.43089430894308944 | ci=[-0.524390243902439, -0.3333333333333333] | p=0.0001 | p_holm= | positive=False | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=qwen2.5-1.5b | counted=False | kannada_native=0.700507614213198 | kannada_other=0.5177664974619289 | hindi_native=0.8934010152284264 | hindi_other=0.766497461928934 | n=197 | diff_of_gaps=0.05583756345177665 | ci=[-0.04568527918781726, 0.15736040609137056] | p=0.3252 | p_holm= | positive=False | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=qwen2.5-1.5b | counted=False | kannada_native=0.32421875 | kannada_other=0.45703125 | hindi_native=0.66015625 | hindi_other=0.58203125 | n=256 | diff_of_gaps=-0.2109375 | ci=[-0.296875, -0.125] | p=0.0001 | p_holm= | positive=False | ci_holm_disagree=False
  measure=retrieval | comparison=native-natural | model=qwen3.5-2b | counted=True | kannada_native=1.0 | kannada_other=0.516260162601626 | hindi_native=0.991869918699187 | hindi_other=0.9471544715447154 | n=246 | diff_of_gaps=0.43902439024390244 | ci=[0.3699186991869919, 0.508130081300813] | p=0.0001 | p_holm=0.00030000000000000003 | positive=True | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=qwen3.5-2b | counted=True | kannada_native=0.7360406091370558 | kannada_other=0.7208121827411168 | hindi_native=0.9238578680203046 | hindi_other=0.9441624365482234 | n=197 | diff_of_gaps=0.03553299492385787 | ci=[-0.04568527918781726, 0.1218274111675127] | p=0.4258 | p_holm=0.4258 | positive=False | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=qwen3.5-2b | counted=True | kannada_native=0.69921875 | kannada_other=0.45703125 | hindi_native=0.72265625 | hindi_other=0.6328125 | n=256 | diff_of_gaps=0.15234375 | ci=[0.08203125, 0.22265625] | p=0.0001 | p_holm=0.0004 | positive=True | ci_holm_disagree=False
  measure=retrieval | comparison=native-natural | model=sarvam-1 | counted=True | kannada_native=0.9878048780487805 | kannada_other=0.9186991869918699 | hindi_native=0.991869918699187 | hindi_other=0.9390243902439024 | n=246 | diff_of_gaps=0.016260162601626018 | ci=[-0.012195121951219513, 0.044715447154471545] | p=0.311 | p_holm=0.311 | positive=False | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=sarvam-1 | counted=True | kannada_native=0.9543147208121827 | kannada_other=0.8934010152284264 | hindi_native=0.9695431472081218 | hindi_other=0.9644670050761421 | n=197 | diff_of_gaps=0.05583756345177665 | ci=[0.01015228426395939, 0.1065989847715736] | p=0.0288 | p_holm=0.0576 | positive=False | ci_holm_disagree=True
  measure=sib | comparison=native-natural | model=sarvam-1 | counted=True | kannada_native=0.75 | kannada_other=0.7265625 | hindi_native=0.7578125 | hindi_other=0.72265625 | n=256 | diff_of_gaps=-0.01171875 | ci=[-0.07421875, 0.05078125] | p=0.7716 | p_holm=0.7716 | positive=False | ci_holm_disagree=False
  measure=retrieval | comparison=native-natural | model=gemma4-e2b | counted=True | kannada_native=1.0 | kannada_other=0.7113821138211383 | hindi_native=1.0 | hindi_other=0.9796747967479674 | n=246 | diff_of_gaps=0.2682926829268293 | ci=[0.2073170731707317, 0.32926829268292684] | p=0.0001 | p_holm=0.00030000000000000003 | positive=True | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=gemma4-e2b | counted=True | kannada_native=0.9847715736040609 | kannada_other=0.8020304568527918 | hindi_native=0.9898477157360406 | hindi_other=0.9898477157360406 | n=197 | diff_of_gaps=0.18274111675126903 | ci=[0.1218274111675127, 0.2436548223350254] | p=0.0001 | p_holm=0.0004 | positive=True | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=gemma4-e2b | counted=True | kannada_native=0.7578125 | kannada_other=0.54296875 | hindi_native=0.7734375 | hindi_other=0.734375 | n=256 | diff_of_gaps=0.17578125 | ci=[0.1015625, 0.24609375] | p=0.0001 | p_holm=0.0004 | positive=True | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=qwen3-1.7b | counted=True | kannada_native=0.8324873096446701 | kannada_other=0.5583756345177665 | hindi_native=0.9441624365482234 | hindi_other=0.8781725888324873 | n=197 | diff_of_gaps=0.20812182741116753 | ci=[0.1065989847715736, 0.3096446700507614] | p=0.0004 | p_holm=0.0012000000000000001 | positive=True | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=qwen3-1.7b | counted=True | kannada_native=0.66796875 | kannada_other=0.37109375 | hindi_native=0.66015625 | hindi_other=0.53125 | n=256 | diff_of_gaps=0.16796875 | ci=[0.0859375, 0.25] | p=0.0002 | p_holm=0.0004 | positive=True | ci_holm_disagree=False
Table [h1lf/opt1_verdict.json] (1 records):
  (top) | loan_definition="v2"; n_items_loan_free=296; n_items_loan_free_v1=110; n_items_loan_free_v2=296; n_items_clean_both=985; n_positive=3; needed=3; verdict="loan-free effect"; all_clean_descriptive_n_positive=3
Table [h1lf/opt1.csv] (12 rows of 12):
  subset=loan_free | model=qwen3-1.7b | n=296 | kannada_native=0.6722972972972973 | kannada_natural=0.26013513513513514 | hindi_native=0.6790540540540541 | hindi_natural=0.46283783783783783 | diff_of_gaps=0.19594594594594594 | ci=[0.11486486486486487, 0.27702702702702703] | p=0.0001 | p_holm=0.0004 | positive=True
  subset=loan_free | model=qwen3.5-2b | n=296 | kannada_native=0.6283783783783784 | kannada_natural=0.28040540540540543 | hindi_native=0.6824324324324325 | hindi_natural=0.5337837837837838 | diff_of_gaps=0.19932432432432431 | ci=[0.12162162162162163, 0.27702702702702703] | p=0.0001 | p_holm=0.0004 | positive=True
  subset=loan_free | model=sarvam-1 | n=296 | kannada_native=0.7668918918918919 | kannada_natural=0.7331081081081081 | hindi_native=0.777027027027027 | hindi_natural=0.6959459459459459 | diff_of_gaps=-0.0472972972972973 | ci=[-0.11148648648648649, 0.016891891891891893] | p=0.1652 | p_holm=0.1652 | positive=False
  subset=loan_free | model=gemma4-e2b | n=296 | kannada_native=0.7331081081081081 | kannada_natural=0.4391891891891892 | hindi_native=0.7635135135135135 | hindi_natural=0.7027027027027027 | diff_of_gaps=0.23310810810810811 | ci=[0.16216216216216217, 0.30405405405405406] | p=0.0001 | p_holm=0.0004 | positive=True
  subset=loan_free_v1 | model=qwen3-1.7b | n=110 | kannada_native=0.6 | kannada_natural=0.24545454545454545 | hindi_native=0.6363636363636364 | hindi_natural=0.44545454545454544 | diff_of_gaps=0.16363636363636364 | ci=[0.045454545454545456, 0.2820454545454512] | p=0.013 | p_holm=0.026 | positive=True
  subset=loan_free_v1 | model=qwen3.5-2b | n=110 | kannada_native=0.5909090909090909 | kannada_natural=0.23636363636363636 | hindi_native=0.6636363636363637 | hindi_natural=0.5636363636363636 | diff_of_gaps=0.2545454545454545 | ci=[0.12727272727272726, 0.38181818181818183] | p=0.0001 | p_holm=0.0004 | positive=True
  subset=loan_free_v1 | model=sarvam-1 | n=110 | kannada_native=0.7 | kannada_natural=0.6454545454545455 | hindi_native=0.6909090909090909 | hindi_natural=0.6090909090909091 | diff_of_gaps=-0.02727272727272727 | ci=[-0.12727272727272726, 0.07272727272727272] | p=0.655 | p_holm=0.655 | positive=False
  subset=loan_free_v1 | model=gemma4-e2b | n=110 | kannada_native=0.6818181818181818 | kannada_natural=0.42727272727272725 | hindi_native=0.7272727272727273 | hindi_natural=0.6818181818181818 | diff_of_gaps=0.20909090909090908 | ci=[0.08181818181818182, 0.32727272727272727] | p=0.001 | p_holm=0.003 | positive=True
  subset=all_clean | model=qwen3-1.7b | n=985 | kannada_native=0.6741116751269035 | kannada_natural=0.38578680203045684 | hindi_native=0.6893401015228426 | hindi_natural=0.5685279187817259 | diff_of_gaps=0.16751269035532995 | ci=[0.12588832487309645, 0.20913705583756345] | p=0.0001 | p_holm=0.0004 | positive=True
  subset=all_clean | model=qwen3.5-2b | n=985 | kannada_native=0.6781725888324873 | kannada_natural=0.44263959390862945 | hindi_native=0.7197969543147208 | hindi_natural=0.6335025380710659 | diff_of_gaps=0.14923857868020304 | ci=[0.10964467005076142, 0.18883248730964466] | p=0.0001 | p_holm=0.0004 | positive=True
  subset=all_clean | model=sarvam-1 | n=985 | kannada_native=0.766497461928934 | kannada_natural=0.7380710659898477 | hindi_native=0.7807106598984772 | hindi_natural=0.732994923857868 | diff_of_gaps=-0.019289340101522844 | ci=[-0.05078680203045683, 0.013197969543147208] | p=0.256 | p_holm=0.256 | positive=False
  subset=all_clean | model=gemma4-e2b | n=985 | kannada_native=0.7482233502538072 | kannada_natural=0.531979695431472 | hindi_native=0.7725888324873097 | hindi_natural=0.7258883248730964 | diff_of_gaps=0.16954314720812183 | ci=[0.13401015228426397, 0.20406091370558377] | p=0.0001 | p_holm=0.0004 | positive=True
Table [h1lf/opt2_verdict.json] (3 records):
  retrieval | n_counted=3; needed=2; n_positive=2; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]; n_items=246; verdict="effect at equal English share"; ci_holm_disagreements=[]
  sentiment | n_counted=4; needed=3; n_positive=2; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]; n_items=197; verdict="refuted"; ci_holm_disagreements=[]
  sib | n_counted=4; needed=3; n_positive=3; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]; n_items=256; verdict="effect at equal English share"; ci_holm_disagreements=[]
Table [h1lf/opt2.csv] (14 rows of 14):
  measure=retrieval | comparison=native-natural | model=qwen2.5-1.5b | counted=False | n=246 | intercept=-0.4764596354760473 | intercept_ci=[-0.5703309887757246, -0.3834786066813491] | p=0.0001 | slope=1.4817238546322515 | slope_ci=[0.5492742645423278, 2.514729266589454] | mean_d=-0.43089430894308944 | mean_delta=0.03075156439609776 | frac_delta_le_0=0.3983739837398374 | p_holm= | positive=False | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=qwen2.5-1.5b | counted=False | n=197 | intercept=0.03972009676230391 | intercept_ci=[-0.098295356022866, 0.17789009101733425] | p=0.5626 | slope=0.15272043312485645 | slope_ci=[-0.6900967432630928, 0.9347685321392747] | mean_d=0.05583756345177665 | mean_delta=0.10553575811493358 | frac_delta_le_0=0.17258883248730963 | p_holm= | positive=False | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=qwen2.5-1.5b | counted=False | n=256 | intercept=-0.24956594725069042 | intercept_ci=[-0.34062845896637195, -0.1573585249367517] | p=0.0001 | slope=0.7706624814199687 | slope_ci=[0.023068157733446015, 1.477821480318102] | mean_d=-0.2109375 | mean_delta=0.05012368991872598 | frac_delta_le_0=0.328125 | p_holm= | positive=False | ci_holm_disagree=False
  measure=retrieval | comparison=native-natural | model=qwen3.5-2b | counted=True | n=246 | intercept=0.41844718151448557 | intercept_ci=[0.34575812021485036, 0.4959915546078536] | p=0.0001 | slope=0.6691434772023502 | slope_ci=[-0.20077900818615865, 1.392265327101491] | mean_d=0.43902439024390244 | mean_delta=0.03075156439609776 | frac_delta_le_0=0.3983739837398374 | p_holm=0.00030000000000000003 | positive=True | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=qwen3.5-2b | counted=True | n=197 | intercept=0.037129838421535485 | intercept_ci=[-0.0713945209882613, 0.15208541463575134] | p=0.4982 | slope=-0.015130828888712505 | slope_ci=[-0.797368243238602, 0.750449503733528] | mean_d=0.03553299492385787 | mean_delta=0.10553575811493358 | frac_delta_le_0=0.17258883248730963 | p_holm=0.4982 | positive=False | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=qwen3.5-2b | counted=True | n=256 | intercept=0.1505105541683601 | intercept_ci=[0.07510654493524827, 0.22572865191928324] | p=0.0002 | slope=0.03657344131312708 | slope_ci=[-0.5958762906142828, 0.644100637566434] | mean_d=0.15234375 | mean_delta=0.05012368991872598 | frac_delta_le_0=0.328125 | p_holm=0.0006000000000000001 | positive=True | ci_holm_disagree=False
  measure=retrieval | comparison=native-natural | model=sarvam-1 | counted=True | n=246 | intercept=0.012982641687717233 | intercept_ci=[-0.013312299169250265, 0.04077866561053541] | p=0.336 | slope=0.1065806237267294 | slope_ci=[-0.17310007099162525, 0.432565815186648] | mean_d=0.016260162601626018 | mean_delta=0.03075156439609776 | frac_delta_le_0=0.3983739837398374 | p_holm=0.336 | positive=False | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=sarvam-1 | counted=True | n=197 | intercept=0.05417699283764358 | intercept_ci=[-0.007145414379490325, 0.11895072817716948] | p=0.0816 | slope=0.015734672719407827 | slope_ci=[-0.25057647823041634, 0.28887186805597925] | mean_d=0.05583756345177665 | mean_delta=0.10553575811493358 | frac_delta_le_0=0.17258883248730963 | p_holm=0.1632 | positive=False | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=sarvam-1 | counted=True | n=256 | intercept=0.008617538663087971 | intercept_ci=[-0.05881559499772433, 0.07587981135894331] | p=0.8138 | slope=-0.40572209859375147 | slope_ci=[-1.1302655377714608, 0.26181484438924546] | mean_d=-0.01171875 | mean_delta=0.05012368991872598 | frac_delta_le_0=0.328125 | p_holm=0.8138 | positive=False | ci_holm_disagree=False
  measure=retrieval | comparison=native-natural | model=gemma4-e2b | counted=True | n=246 | intercept=0.24775279556169733 | intercept_ci=[0.18677900080623847, 0.3140738656816757] | p=0.0001 | slope=0.6679298360423701 | slope_ci=[-0.03333074371485695, 1.2864186983066723] | mean_d=0.2682926829268293 | mean_delta=0.03075156439609776 | frac_delta_le_0=0.3983739837398374 | p_holm=0.00030000000000000003 | positive=True | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=gemma4-e2b | counted=True | n=197 | intercept=0.11615837313271568 | intercept_ci=[0.024197870196541977, 0.21537185151491434] | p=0.014 | slope=0.6309022155887817 | slope_ci=[-0.045255598753819876, 1.2147808039645593] | mean_d=0.18274111675126903 | mean_delta=0.10553575811493358 | frac_delta_le_0=0.17258883248730963 | p_holm=0.042 | positive=True | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=gemma4-e2b | counted=True | n=256 | intercept=0.16364302520432697 | intercept_ci=[0.07786038283429435, 0.2461954078417022] | p=0.0002 | slope=0.24216542747261394 | slope_ci=[-0.3398537275258259, 0.8867681666992515] | mean_d=0.17578125 | mean_delta=0.05012368991872598 | frac_delta_le_0=0.328125 | p_holm=0.0006000000000000001 | positive=True | ci_holm_disagree=False
  measure=sentiment | comparison=native-natural | model=qwen3-1.7b | counted=True | n=197 | intercept=0.19463252470978368 | intercept_ci=[0.04869537697393107, 0.33639916391792846] | p=0.0066 | slope=0.12781736676106814 | slope_ci=[-0.7081198896891855, 1.1196601317600314] | mean_d=0.20812182741116753 | mean_delta=0.10553575811493358 | frac_delta_le_0=0.17258883248730963 | p_holm=0.0264 | positive=True | ci_holm_disagree=False
  measure=sib | comparison=native-natural | model=qwen3-1.7b | counted=True | n=256 | intercept=0.15623983103008784 | intercept_ci=[0.07729797102461314, 0.23893636919776692] | p=0.0001 | slope=0.2339995117863477 | slope_ci=[-0.5134239675271841, 0.9615997953136305] | mean_d=0.16796875 | mean_delta=0.05012368991872598 | frac_delta_le_0=0.328125 | p_holm=0.0004 | positive=True | ci_holm_disagree=False
Table [k3b_hi/verdict.json] (4 records):
  (top) | K3b="inconclusive"; n=499; n_primary_defective_excluded=1
  statistics.vowel_doubling | gemini_rate=0.013083335156540574; human_rate=0.01493871854145767; ratio=0.8758003653547612; ci90=[0.7652356242062518, 0.9964025473338749]; ci95=[0.743037014212196, 1.022126295537717]; verdict="inconclusive"
  statistics.h_digraph | gemini_rate=0.028529546896536636; human_rate=0.028547127840537357; ratio=0.9993841431579763; ci90=[0.9849955131866562, 1.0139375163516189]; ci95=[0.9821778954535723, 1.016670940027307]; verdict="matches"
  statistics.english_word_share | gemini_rate=0.0862589853109699; human_rate=0.0770033388981636; ratio=1.1201979881034356; ci90=[1.0530057097907044, 1.193341769677889]; ci95=[1.0404890729787815, 1.2068213660921743]; verdict="matches"
Result entry: 2026-10-28 06:50 IST — H1-LF selection check results (exploratory, no verdict; registered 06:20 IST; `scripts/h1lf_selection.py`) [RESULTS.md 3261-3269, `9fbb738` 2026-10-28 10:17:38 +0530]
Source files: results/h_hindi/h1_verdict.json; results/h_hindi/h1.csv; results/h1lf/opt1_verdict.json; results/h1lf/opt1.csv; results/h1lf/opt2_verdict.json; results/h1lf/opt2.csv; results/k3b_hi/verdict.json

### EP: Activation patching E-P1, E-P2, EP-R
Registered: PRE-REGISTRATION — E-P1: word-aligned activation patching, NC1 (a) → (c) (written 2026-10-23 16:00 IST; the 2026-10-23 draft, approved by the lead author with changes; before any patching code is written or run) [RESULTS.md 2436-2471, `6867631` 2026-10-23 16:00:59 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: sib, sentiment; seeds: 0
Table [ep1/predictions.json] (6 records):
  per_model.qwen3-1.7b | n_layers=28; n_items=73; n_selection=36; n_heldout=37; L_star=5; heldout_R_final=0.3737526459026308; heldout_R_final_ci=[0.21586872403357643, 0.555386548795285]; P1a_positive=false; P1b_bound=18; P1b_positive=true; heldout_R_all_at_L_star_reported=0.976716056849108; control_n=70; control_R_at_L_star=0.34342211460855526; control_R_ci=[0.244191195355786, 0.45086786016724645]; control_same_sign=true
  per_model.qwen3.5-2b | n_layers=24; n_items=117; n_selection=58; n_heldout=59; L_star=7; heldout_R_final=0.4129137276180141; heldout_R_final_ci=[0.2842422539920761, 0.5332177040014932]; P1a_positive=false; P1b_bound=16; P1b_positive=true; heldout_R_all_at_L_star_reported=0.7932718393922952; control_n=52; control_R_at_L_star=0.3712797619047619; control_R_ci=[0.2746310716556832, 0.47077739210001535]; control_same_sign=true
  per_model.sarvam-1 | n_layers=28; n_items=200; n_selection=100; n_heldout=100; L_star=15; heldout_R_final=0.4756871035940803; heldout_R_final_ci=[0.42159682443975494, 0.5293479361027988]; P1a_positive=false; P1b_bound=18; P1b_positive=true; heldout_R_all_at_L_star_reported=0.8234672304439745; control_n=51; control_R_at_L_star=0.44230769230769235; control_R_ci=[0.2535211267605634, 0.6269841269841269]; control_same_sign=true
  per_model.gemma4-e2b | n_layers=35; n_items=133; n_selection=66; n_heldout=67; L_star=9; heldout_R_final=0.46101155004076017; heldout_R_final_ci=[0.3778535204905811, 0.542191978110641]; P1a_positive=false; P1b_bound=23; P1b_positive=true; heldout_R_all_at_L_star_reported=0.8888244678990657; control_n=59; control_R_at_L_star=0.3062208240308504; control_R_ci=[0.22027842468253855, 0.3984177137381146]; control_same_sign=true
  verdict.P1a | n_positive=0; needed=3; of=4; outcome="refuted"
  verdict.P1b | n_positive=4; needed=3; of=4; outcome="confirmed"
Table [ep2/predictions.json] (6 records):
  per_model.qwen3-1.7b | n_layers=28; n_items=200; n_selection=100; n_heldout=100; L_star=11; heldout_R_word=0.3708914303618988; heldout_R_word_ci=[0.29128835770863326, 0.45271641072979324]; P2a_positive=false; heldout_R_read_at_L_star=0.020053266489111706; heldout_R_read_ci=[0.0054593858903426475, 0.03450551675569546]; heldout_word_minus_read=0.3508381638727871; heldout_word_minus_read_ci=[0.27292476637466623, 0.4303777591371316]; P2b_positive=true; L_read_reported=18; L_star_word_lt_L_read_reported=true; control_n=31; control_R_at_L_star=0.46557298527122504; control_R_ci=[0.300298594649744, 0.6436016577920343]; control_same_sign=true
  per_model.qwen3.5-2b | n_layers=24; n_items=200; n_selection=100; n_heldout=100; L_star=6; heldout_R_word=0.5508817343471929; heldout_R_word_ci=[0.49480271347476246, 0.6037412722270918]; P2a_positive=false; heldout_R_read_at_L_star=-0.005015369681281346; heldout_R_read_ci=[-0.014606551212641733, 0.004333012962447943]; heldout_word_minus_read=0.5558971040284743; heldout_word_minus_read_ci=[0.5000834725853198, 0.6095706023807879]; P2b_positive=true; L_read_reported=16; L_star_word_lt_L_read_reported=true; control_n=43; control_R_at_L_star=0.4122994652406417; control_R_ci=[0.25797589319700204, 0.538723830483607]; control_same_sign=true
  per_model.sarvam-1 | n_layers=28; n_items=126; n_selection=63; n_heldout=63; L_star=14; heldout_R_word=0.47476901208244493; heldout_R_word_ci=[0.41045694799659005, 0.5371601228699581]; P2a_positive=false; heldout_R_read_at_L_star=-0.07818052594171998; heldout_R_read_ci=[-0.11550703934821491, -0.045745585713032645]; heldout_word_minus_read=0.5529495380241649; heldout_word_minus_read_ci=[0.46918551128316494, 0.6396396396396395]; P2b_positive=true; L_read_reported=22; L_star_word_lt_L_read_reported=true; control_n=65; control_R_at_L_star=0.024806201550387597; control_R_ci=[-0.20001022494887527, 0.18107493193092378]; control_same_sign=true
  per_model.gemma4-e2b | n_layers=35; n_items=200; n_selection=100; n_heldout=100; L_star=9; heldout_R_word=0.5201953176494198; heldout_R_word_ci=[0.45041964392444284, 0.5895672777867308]; P2a_positive=false; heldout_R_read_at_L_star=-0.0019454047130441968; heldout_R_read_ci=[-0.004203377497400369, 0.00028658781738425895]; heldout_word_minus_read=0.522140722362464; heldout_word_minus_read_ci=[0.4522450631254503, 0.5914664987402138]; P2b_positive=true; L_read_reported=23; L_star_word_lt_L_read_reported=true; control_n=39; control_R_at_L_star=0.546271701310461; control_R_ci=[0.386944949354477, 0.7075474655139404]; control_same_sign=true
  verdict.P2a | n_positive=0; needed=3; of=4; outcome="refuted"
  verdict.P2b | n_positive=4; needed=3; of=4; outcome="confirmed"
Table [ep_robust/main_estimates.csv] (24 rows of 24):
  experiment=E-P1 | model=qwen3-1.7b | L_star=5 | set=all items | n=1004 | share_of_1004=1.0 | R=-0.4841323430114787 | lo=-8.055703885196223 | hi=8.556801696457914 | median_item_R=0.3767123287671233 | median_n=459 | n_gap_ge_0.5=459 | share_gap_ge_0.5=0.45717131474103584 | n_gap_lt_0.5=545 | n_gap_negative=511
  experiment=E-P1 | model=qwen3-1.7b | L_star=5 | set=gap >= 0.5 | n=459 | share_of_1004=0.45717131474103584 | R=0.40428182918209155 | lo=0.33866748857775064 | hi=0.47077508645343075 | median_item_R=0.3767123287671233 | median_n=459 | n_gap_ge_0.5=459 | share_gap_ge_0.5=0.45717131474103584 | n_gap_lt_0.5=545 | n_gap_negative=511
  experiment=E-P1 | model=qwen3-1.7b | L_star=5 | set=selected (as run) | n=73 | share_of_1004=0.07270916334661355 | R=0.4129422132695455 | lo=0.30299975094847226 | hi=0.5219209463332585 | median_item_R=0.44155844155844154 | median_n=73 | n_gap_ge_0.5=459 | share_gap_ge_0.5=0.45717131474103584 | n_gap_lt_0.5=545 | n_gap_negative=511
  experiment=E-P1 | model=qwen3.5-2b | L_star=7 | set=all items | n=1004 | share_of_1004=1.0 | R=0.3577023498694517 | lo=0.22880388122392253 | hi=0.4801844321944399 | median_item_R=0.2857142857142857 | median_n=368 | n_gap_ge_0.5=368 | share_gap_ge_0.5=0.3665338645418327 | n_gap_lt_0.5=636 | n_gap_negative=396
  experiment=E-P1 | model=qwen3.5-2b | L_star=7 | set=gap >= 0.5 | n=368 | share_of_1004=0.3665338645418327 | R=0.3501344871944802 | lo=0.30570874338118076 | hi=0.39562235325916506 | median_item_R=0.2857142857142857 | median_n=368 | n_gap_ge_0.5=368 | share_gap_ge_0.5=0.3665338645418327 | n_gap_lt_0.5=636 | n_gap_negative=396
  experiment=E-P1 | model=qwen3.5-2b | L_star=7 | set=selected (as run) | n=117 | share_of_1004=0.11653386454183266 | R=0.375030599755202 | lo=0.29517555268007717 | hi=0.45385205455670025 | median_item_R=0.28348214285714285 | median_n=106 | n_gap_ge_0.5=368 | share_gap_ge_0.5=0.3665338645418327 | n_gap_lt_0.5=636 | n_gap_negative=396
  experiment=E-P1 | model=sarvam-1 | L_star=15 | set=all items | n=1004 | share_of_1004=1.0 | R=0.4394607843137255 | lo=0.4076614796102824 | hi=0.4714402417029669 | median_item_R=0.4444444444444444 | median_n=663 | n_gap_ge_0.5=663 | share_gap_ge_0.5=0.6603585657370518 | n_gap_lt_0.5=341 | n_gap_negative=198
  experiment=E-P1 | model=sarvam-1 | L_star=15 | set=gap >= 0.5 | n=663 | share_of_1004=0.6603585657370518 | R=0.4452244203360987 | lo=0.42183782126609526 | hi=0.4690212058220521 | median_item_R=0.4444444444444444 | median_n=663 | n_gap_ge_0.5=663 | share_gap_ge_0.5=0.6603585657370518 | n_gap_lt_0.5=341 | n_gap_negative=198
  experiment=E-P1 | model=sarvam-1 | L_star=15 | set=selected (as run) | n=200 | share_of_1004=0.199203187250996 | R=0.4882323485227842 | lo=0.4536119910484465 | hi=0.5224114710728441 | median_item_R=0.5 | median_n=191 | n_gap_ge_0.5=663 | share_gap_ge_0.5=0.6603585657370518 | n_gap_lt_0.5=341 | n_gap_negative=198
  experiment=E-P1 | model=gemma4-e2b | L_star=9 | set=all items | n=1004 | share_of_1004=1.0 | R=0.4937825870746116 | lo=0.37333605543315534 | hi=0.6364855226824059 | median_item_R=0.38275541795665635 | median_n=526 | n_gap_ge_0.5=526 | share_gap_ge_0.5=0.5239043824701195 | n_gap_lt_0.5=478 | n_gap_negative=435
  experiment=E-P1 | model=gemma4-e2b | L_star=9 | set=gap >= 0.5 | n=526 | share_of_1004=0.5239043824701195 | R=0.40188742934385646 | lo=0.3629774100841185 | hi=0.4409202984222956 | median_item_R=0.38275541795665635 | median_n=526 | n_gap_ge_0.5=526 | share_gap_ge_0.5=0.5239043824701195 | n_gap_lt_0.5=478 | n_gap_negative=435
  experiment=E-P1 | model=gemma4-e2b | L_star=9 | set=selected (as run) | n=133 | share_of_1004=0.13247011952191234 | R=0.4221351553159507 | lo=0.3659638172033873 | hi=0.4785494679844849 | median_item_R=0.4051698545315747 | median_n=132 | n_gap_ge_0.5=526 | share_gap_ge_0.5=0.5239043824701195 | n_gap_lt_0.5=478 | n_gap_negative=435
  experiment=E-P2 | model=qwen3-1.7b | L_star=11 | set=all items | n=1004 | share_of_1004=1.0 | R=0.42242524217592825 | lo=0.37376779003424065 | hi=0.4709512600812421 | median_item_R=0.36220472440944884 | median_n=711 | n_gap_ge_0.5=711 | share_gap_ge_0.5=0.7081673306772909 | n_gap_lt_0.5=293 | n_gap_negative=278
  experiment=E-P2 | model=qwen3-1.7b | L_star=11 | set=gap >= 0.5 | n=711 | share_of_1004=0.7081673306772909 | R=0.41645247495073057 | lo=0.3806017600559112 | hi=0.4529330550324756 | median_item_R=0.36220472440944884 | median_n=711 | n_gap_ge_0.5=711 | share_gap_ge_0.5=0.7081673306772909 | n_gap_lt_0.5=293 | n_gap_negative=278
  experiment=E-P2 | model=qwen3-1.7b | L_star=11 | set=selected (as run) | n=200 | share_of_1004=0.199203187250996 | R=0.3750137364793796 | lo=0.3207114502068774 | hi=0.42981683277524724 | median_item_R=0.2864518364518365 | median_n=200 | n_gap_ge_0.5=711 | share_gap_ge_0.5=0.7081673306772909 | n_gap_lt_0.5=293 | n_gap_negative=278
  experiment=E-P2 | model=qwen3.5-2b | L_star=6 | set=all items | n=1004 | share_of_1004=1.0 | R=0.5884156477411252 | lo=0.5537570336831944 | hi=0.6237500855692426 | median_item_R=0.5540150995195607 | median_n=674 | n_gap_ge_0.5=674 | share_gap_ge_0.5=0.6713147410358565 | n_gap_lt_0.5=330 | n_gap_negative=223
  experiment=E-P2 | model=qwen3.5-2b | L_star=6 | set=gap >= 0.5 | n=674 | share_of_1004=0.6713147410358565 | R=0.557301709731328 | lo=0.5304243310758937 | hi=0.5836059317443457 | median_item_R=0.5540150995195607 | median_n=674 | n_gap_ge_0.5=674 | share_gap_ge_0.5=0.6713147410358565 | n_gap_lt_0.5=330 | n_gap_negative=223
  experiment=E-P2 | model=qwen3.5-2b | L_star=6 | set=selected (as run) | n=200 | share_of_1004=0.199203187250996 | R=0.5567967275015733 | lo=0.5160325038256607 | hi=0.5978277818866994 | median_item_R=0.5529411764705883 | median_n=197 | n_gap_ge_0.5=674 | share_gap_ge_0.5=0.6713147410358565 | n_gap_lt_0.5=330 | n_gap_negative=223
  experiment=E-P2 | model=sarvam-1 | L_star=14 | set=all items | n=1004 | share_of_1004=1.0 | R=0.4400930593253199 | lo=0.4012549489666715 | hi=0.4815879434948118 | median_item_R=0.3333333333333333 | median_n=661 | n_gap_ge_0.5=661 | share_gap_ge_0.5=0.6583665338645418 | n_gap_lt_0.5=343 | n_gap_negative=233
  experiment=E-P2 | model=sarvam-1 | L_star=14 | set=gap >= 0.5 | n=661 | share_of_1004=0.6583665338645418 | R=0.3716216216216216 | lo=0.3446945220982753 | hi=0.3978418203456237 | median_item_R=0.3333333333333333 | median_n=661 | n_gap_ge_0.5=661 | share_gap_ge_0.5=0.6583665338645418 | n_gap_lt_0.5=343 | n_gap_negative=233
  experiment=E-P2 | model=sarvam-1 | L_star=14 | set=selected (as run) | n=126 | share_of_1004=0.1254980079681275 | R=0.5102383350117489 | lo=0.4599229263240456 | hi=0.5607601078900362 | median_item_R=0.5 | median_n=122 | n_gap_ge_0.5=661 | share_gap_ge_0.5=0.6583665338645418 | n_gap_lt_0.5=343 | n_gap_negative=233
  experiment=E-P2 | model=gemma4-e2b | L_star=9 | set=all items | n=1004 | share_of_1004=1.0 | R=0.6021840862088874 | lo=0.56521985366825 | hi=0.6389320958104592 | median_item_R=0.6260673162177 | median_n=770 | n_gap_ge_0.5=770 | share_gap_ge_0.5=0.7669322709163346 | n_gap_lt_0.5=234 | n_gap_negative=217
  experiment=E-P2 | model=gemma4-e2b | L_star=9 | set=gap >= 0.5 | n=770 | share_of_1004=0.7669322709163346 | R=0.5838231487306933 | lo=0.5558354884277296 | hi=0.6121448033373303 | median_item_R=0.6260673162177 | median_n=770 | n_gap_ge_0.5=770 | share_gap_ge_0.5=0.7669322709163346 | n_gap_lt_0.5=234 | n_gap_negative=217
  experiment=E-P2 | model=gemma4-e2b | L_star=9 | set=selected (as run) | n=200 | share_of_1004=0.199203187250996 | R=0.551674914946263 | lo=0.5045777111738318 | hi=0.5971617986018742 | median_item_R=0.6354900704676489 | median_n=199 | n_gap_ge_0.5=770 | share_gap_ge_0.5=0.7669322709163346 | n_gap_lt_0.5=234 | n_gap_negative=217
Result entry: 2026-10-26 12:20 IST — EP-R results (exploratory, registered 2026-10-26 02:40 IST; no verdict; registered E-P1/E-P2 outcomes unchanged) [RESULTS.md 3033-3057, `46bd82a` 2026-10-26 12:10:58 +0530]
Source files: results/ep1/predictions.json; results/ep2/predictions.json; results/ep_robust/main_estimates.csv

## Phase 2

### X1: Second prompt template (T2) and Kannada instruction (T3)
Registered: X1. Second prompt template (Kannada; 5 models; inference only) [RESULTS.md 3352-3395, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: nc_a, nc_b, nc_c, lossy, lower, itrans, native, english, natural, natural257; tasks/measures: sib, xnli, sentiment, sib_nc, sentiment_nc, sib_L3_secondary; seeds: not recorded as a column or key in the result files
Table [phase2/x1/t2/analysis/summary.json] (40 records):
  (top) | T-b_same_category=8; T-b_total=11; t1_pipeline_reproduces_phase1_verdicts=true; t2_calibration_fallback_rows=[]
  T-a.primary_P_a_exact_wording_all_informative_models | verdict="refuted"; n_positive_significant=9; n_tests=10; informative_models=[5 values]
  T-a.primary_P_a_exact_wording_all_informative_models.english_acc_cal | qwen2.5-1.5b=0.8286852589641435; qwen3.5-2b=0.8137450199203188; sarvam-1=0.7719123505976095; gemma4-e2b=0.8266932270916335; qwen3-1.7b=0.8077689243027888
  T-a.primary_P_a_exact_wording_all_informative_models.misses[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; b="lossy"; diff=-0.03884462151394419; p_holm=0.042968453350769216
  T-a.secondary_every_counted_model | verdict="supported"; n_positive_significant=8; n_tests=8; informative_models=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]; misses=[]
  T-a.secondary_every_counted_model.english_acc_cal | qwen3-1.7b=0.8077689243027888; qwen3.5-2b=0.8137450199203188; sarvam-1=0.7719123505976095; gemma4-e2b=0.8266932270916335
  T-a.phase1_same_lines | P_a="partly supported"; n_positive_significant=9; n_tests=10; counted_four="supported"
  T-b[verdict_line=P-a on SIB-200] | verdict_line="P-a on SIB-200"; t1="partly supported"; t2="refuted"; same=false
  T-b[verdict_line=L1 sentiment] | verdict_line="L1 sentiment"; t1="no effect detected"; t2="no effect detected"; same=true
  T-b[verdict_line=L2 sentiment] | verdict_line="L2 sentiment"; t1="effect, positive"; t2="no effect detected"; same=false
  T-b[verdict_line=L3 sentiment] | verdict_line="L3 sentiment"; t1="no effect detected"; t2="no effect detected"; same=true
  T-b[verdict_line=L1 sib] | verdict_line="L1 sib"; t1="no effect detected"; t2="no effect detected"; same=true
  T-b[verdict_line=L2 sib] | verdict_line="L2 sib"; t1="effect, positive"; t2="effect, positive"; same=true
  T-b[verdict_line=L3 sib] | verdict_line="L3 sib"; t1="no effect detected"; t2="no effect detected"; same=true
  T-b[verdict_line=NC-F sentiment] | verdict_line="NC-F sentiment"; t1="no effect detected"; t2="no effect detected"; same=true
  T-b[verdict_line=NC-O sentiment] | verdict_line="NC-O sentiment"; t1="no effect detected"; t2="effect, positive"; same=false
  T-b[verdict_line=NC-F sib] | verdict_line="NC-F sib"; t1="no effect detected"; t2="no effect detected"; same=true
  T-b[verdict_line=NC-O sib] | verdict_line="NC-O sib"; t1="effect, positive"; t2="effect, positive"; same=true
  t1_calibration_fallback_rows[model=gemma4-e2b] | model="gemma4-e2b"; task="xnli"
  t1_calibration_fallback_rows[model=qwen2.5-1.5b] | model="qwen2.5-1.5b"; task="sentiment"
  t2_effect_verdicts.L1|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=1; n_counted=4; ci_holm_disagreements=[]
  t2_effect_verdicts.L2|sentiment | verdict="no effect detected"; n_significant_positive=2; n_significant_negative=0; n_counted=4; ci_holm_disagreements=["qwen3.5-2b"]
  t2_effect_verdicts.L3|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t2_effect_verdicts.NC-F|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; n_counted=4; ci_holm_disagreements=["gemma4-e2b"]
  t2_effect_verdicts.NC-O|sentiment | verdict="effect, positive"; n_significant_positive=3; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t2_effect_verdicts.L1|sib | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; n_counted=4; ci_holm_disagreements=["sarvam-1"]
  t2_effect_verdicts.L2|sib | verdict="effect, positive"; n_significant_positive=4; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t2_effect_verdicts.L3|sib | verdict="no effect detected"; n_significant_positive=1; n_significant_negative=0; n_counted=4; ci_holm_disagreements=["qwen3.5-2b"]
  t2_effect_verdicts.NC-F|sib | verdict="no effect detected"; n_significant_positive=1; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t2_effect_verdicts.NC-O|sib | verdict="effect, positive"; n_significant_positive=3; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t1_effect_verdicts.L1|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=2; n_counted=4; ci_holm_disagreements=[]
  t1_effect_verdicts.L2|sentiment | verdict="effect, positive"; n_significant_positive=3; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t1_effect_verdicts.L3|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t1_effect_verdicts.NC-F|sentiment | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t1_effect_verdicts.NC-O|sentiment | verdict="no effect detected"; n_significant_positive=2; n_significant_negative=0; n_counted=4; ci_holm_disagreements=["gemma4-e2b"]
  t1_effect_verdicts.L1|sib | verdict="no effect detected"; n_significant_positive=2; n_significant_negative=1; n_counted=4; ci_holm_disagreements=[]
  t1_effect_verdicts.L2|sib | verdict="effect, positive"; n_significant_positive=4; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
  t1_effect_verdicts.L3|sib | verdict="no effect detected"; n_significant_positive=0; n_significant_negative=0; n_counted=4; ci_holm_disagreements=["qwen3-1.7b", "sarvam-1"]
  t1_effect_verdicts.NC-F|sib | verdict="no effect detected"; n_significant_positive=1; n_significant_negative=0; n_counted=4; ci_holm_disagreements=["gemma4-e2b"]
  t1_effect_verdicts.NC-O|sib | verdict="effect, positive"; n_significant_positive=3; n_significant_negative=0; n_counted=4; ci_holm_disagreements=[]
Table [phase2/x1/t2/analysis/ta_primary_mcnemar.csv] (10 rows of 10):
  model=gemma4-e2b | task=sib | a=native | b=itrans | acc_a=0.7908366533864541 | acc_b=0.3645418326693227 | n=1004 | diff=0.42629482071713143 | a_only=464 | b_only=36 | p=7.123281604386148e-96 | p_holm=7.123281604386148e-95 | significant=True
  model=gemma4-e2b | task=sib | a=native | b=lossy | acc_a=0.7908366533864541 | acc_b=0.5079681274900398 | n=1004 | diff=0.2828685258964143 | a_only=323 | b_only=39 | p=8.737757751023445e-57 | p_holm=5.242654650614067e-56 | significant=True
  model=qwen2.5-1.5b | task=sib | a=native | b=itrans | acc_a=0.4252988047808765 | acc_b=0.36852589641434264 | n=1004 | diff=0.05677290836653387 | a_only=194 | b_only=137 | p=0.0020377594974601326 | p_holm=0.004075518994920265 | significant=True
  model=qwen2.5-1.5b | task=sib | a=native | b=lossy | acc_a=0.4252988047808765 | acc_b=0.4641434262948207 | n=1004 | diff=-0.03884462151394419 | a_only=157 | b_only=196 | p=0.042968453350769216 | p_holm=0.042968453350769216 | significant=True
  model=qwen3-1.7b | task=sib | a=native | b=itrans | acc_a=0.7221115537848606 | acc_b=0.28386454183266935 | n=1004 | diff=0.43824701195219123 | a_only=482 | b_only=42 | p=8.545377768767467e-96 | p_holm=7.69083999189072e-95 | significant=True
  model=qwen3-1.7b | task=sib | a=native | b=lossy | acc_a=0.7221115537848606 | acc_b=0.34063745019920316 | n=1004 | diff=0.3814741035856574 | a_only=432 | b_only=49 | p=1.2565807101806356e-77 | p_holm=8.796064971264449e-77 | significant=True
  model=qwen3.5-2b | task=sib | a=native | b=itrans | acc_a=0.6802788844621513 | acc_b=0.3137450199203187 | n=1004 | diff=0.3665338645418326 | a_only=395 | b_only=27 | p=5.947973676248414e-85 | p_holm=4.758378940998731e-84 | significant=True
  model=qwen3.5-2b | task=sib | a=native | b=lossy | acc_a=0.6802788844621513 | acc_b=0.4103585657370518 | n=1004 | diff=0.26992031872509953 | a_only=308 | b_only=37 | p=2.4648309714396693e-54 | p_holm=1.2324154857198347e-53 | significant=True
  model=sarvam-1 | task=sib | a=native | b=itrans | acc_a=0.7599601593625498 | acc_b=0.5328685258964143 | n=1004 | diff=0.22709163346613548 | a_only=292 | b_only=64 | p=6.455121364889042e-36 | p_holm=2.5820485459556167e-35 | significant=True
  model=sarvam-1 | task=sib | a=native | b=lossy | acc_a=0.7599601593625498 | acc_b=0.6962151394422311 | n=1004 | diff=0.06374501992031867 | a_only=131 | b_only=67 | p=6.346997755773931e-06 | p_holm=1.9040993267321793e-05 | significant=True
Table [phase2/x1/t2/analysis/ta_secondary_mcnemar.csv] (8 rows of 8):
  model=gemma4-e2b | task=sib | a=native | b=itrans | acc_a=0.7908366533864541 | acc_b=0.3645418326693227 | n=1004 | diff=0.42629482071713143 | a_only=464 | b_only=36 | p=7.123281604386148e-96 | p_holm=5.6986252835089185e-95 | significant=True
  model=gemma4-e2b | task=sib | a=native | b=lossy | acc_a=0.7908366533864541 | acc_b=0.5079681274900398 | n=1004 | diff=0.2828685258964143 | a_only=323 | b_only=39 | p=8.737757751023445e-57 | p_holm=3.495103100409378e-56 | significant=True
  model=qwen3-1.7b | task=sib | a=native | b=itrans | acc_a=0.7221115537848606 | acc_b=0.28386454183266935 | n=1004 | diff=0.43824701195219123 | a_only=482 | b_only=42 | p=8.545377768767467e-96 | p_holm=5.981764438137226e-95 | significant=True
  model=qwen3-1.7b | task=sib | a=native | b=lossy | acc_a=0.7221115537848606 | acc_b=0.34063745019920316 | n=1004 | diff=0.3814741035856574 | a_only=432 | b_only=49 | p=1.2565807101806356e-77 | p_holm=6.2829035509031785e-77 | significant=True
  model=qwen3.5-2b | task=sib | a=native | b=itrans | acc_a=0.6802788844621513 | acc_b=0.3137450199203187 | n=1004 | diff=0.3665338645418326 | a_only=395 | b_only=27 | p=5.947973676248414e-85 | p_holm=3.5687842057490486e-84 | significant=True
  model=qwen3.5-2b | task=sib | a=native | b=lossy | acc_a=0.6802788844621513 | acc_b=0.4103585657370518 | n=1004 | diff=0.26992031872509953 | a_only=308 | b_only=37 | p=2.4648309714396693e-54 | p_holm=7.394492914319008e-54 | significant=True
  model=sarvam-1 | task=sib | a=native | b=itrans | acc_a=0.7599601593625498 | acc_b=0.5328685258964143 | n=1004 | diff=0.22709163346613548 | a_only=292 | b_only=64 | p=6.455121364889042e-36 | p_holm=1.2910242729778084e-35 | significant=True
  model=sarvam-1 | task=sib | a=native | b=lossy | acc_a=0.7599601593625498 | acc_b=0.6962151394422311 | n=1004 | diff=0.06374501992031867 | a_only=131 | b_only=67 | p=6.346997755773931e-06 | p_holm=6.346997755773931e-06 | significant=True
Table [phase2/x1/t2/analysis/tb_verdicts.csv] (11 rows of 11):
  verdict_line=P-a on SIB-200 | t1=partly supported | t2=refuted | same=False
  verdict_line=L1 sentiment | t1=no effect detected | t2=no effect detected | same=True
  verdict_line=L2 sentiment | t1=effect, positive | t2=no effect detected | same=False
  verdict_line=L3 sentiment | t1=no effect detected | t2=no effect detected | same=True
  verdict_line=L1 sib | t1=no effect detected | t2=no effect detected | same=True
  verdict_line=L2 sib | t1=effect, positive | t2=effect, positive | same=True
  verdict_line=L3 sib | t1=no effect detected | t2=no effect detected | same=True
  verdict_line=NC-F sentiment | t1=no effect detected | t2=no effect detected | same=True
  verdict_line=NC-O sentiment | t1=no effect detected | t2=effect, positive | same=False
  verdict_line=NC-F sib | t1=no effect detected | t2=no effect detected | same=True
  verdict_line=NC-O sib | t1=effect, positive | t2=effect, positive | same=True
Result entry: 2026-11-04 20:44 IST, X1 T3 ANALYSIS (exploratory; label "instruction verified by a native speaker, exploratory"; `scripts/x1_analyse_t3.py`, same code and rules as the T2 analysis with T3 in place of T2; `results/phase2/x1/t3/ana [RESULTS.md 3927-3927, `3c30aee` 2026-11-04 20:44:16 +0530]
Source files: results/phase2/x1/t2/analysis/summary.json; results/phase2/x1/t2/analysis/ta_primary_mcnemar.csv; results/phase2/x1/t2/analysis/ta_secondary_mcnemar.csv; results/phase2/x1/t2/analysis/tb_verdicts.csv

### X2: Measured romanized exposure
Registered: X2. Measured romanized exposure (CPU and network; no GPU) [RESULTS.md 3396-3399, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [phase2/x2/exposure.json] (9 records):
  languages.kn | native_config="kan_Knda"; latin_config="kan_Latn"; documents_native=2390982; documents_latin=1070; e_documents=0.00044731469048331726; e_documents_ci95_poisson=[0.00042055667158982915, 0.00047421065108332915]; bytes_native=3526351166; bytes_latin=2406737; e_bytes=0.0006820351710594525
  languages.hi | native_config="hin_Deva"; latin_config="hin_Latn"; documents_native=22095985; documents_latin=97024; e_documents=0.004371827182154524; e_documents_ci95_poisson=[0.00434475217389756, 0.0043992759906306385]; bytes_native=34272968716; bytes_latin=198462618; e_bytes=0.005757307147389948
  languages.te | native_config="tel_Telu"; latin_config="tel_Latn"; documents_native=1964395; documents_latin=24103; e_documents=0.012121209073381014; e_documents_ci95_poisson=[0.011970719734613286, 0.012271547107613188]; bytes_native=3950350913; bytes_latin=46935113; e_bytes=0.011741744947625622
  languages.bn | native_config="ben_Beng"; latin_config="ben_Latn"; documents_native=15185742; documents_latin=10458; e_documents=0.0006881983653808189; e_documents_ci95_poisson=[0.0006749755941617783, 0.0007012931761882781]; bytes_native=23894953700; bytes_latin=32545716; e_bytes=0.0013601804114238996
  languages.ta | native_config="tam_Taml"; latin_config="tam_Latn"; documents_native=5528854; documents_latin=4828; e_documents=0.0008724751440361047; e_documents_ci95_poisson=[0.0008479254428573898, 0.0008970440779039811]; bytes_native=9438382231; bytes_latin=13266958; e_bytes=0.0014036659354052545
  languages.ml | native_config="mal_Mlym"; latin_config="mal_Latn"; documents_native=3322526; documents_latin=3434; e_documents=0.00103248385428568; e_documents_ci95_poisson=[0.000997656154898646, 0.0010665521146213989]; bytes_native=5915341648; bytes_latin=7399476; e_bytes=0.0012493330106926348
  languages.mr | native_config="mar_Deva"; latin_config="mar_Latn"; documents_native=3912702; documents_latin=1757; e_documents=0.00044884874257208977; e_documents_ci95_poisson=[0.0004282540208660332, 0.0004698626730148011]; bytes_native=6278522796; bytes_latin=3264635; e_bytes=0.0005196984195755095
  languages.gu | native_config="guj_Gujr"; latin_config="guj_Latn"; documents_native=2127094; documents_latin=713; e_documents=0.00033508678183688653; e_documents_ci95_poisson=[0.0003111829374582217, 0.0003606435098033437]; bytes_native=3338859951; bytes_latin=1340064; e_bytes=0.00040119274114786804
  registered_test | e_hi=0.004371827182154524; e_kn=0.00044731469048331726; difference=0.003924512491671207; ci95_poisson=[0.003886533807229467, 0.003962697251453456]; verdict="supported"; bytes_measure_same_sign=true
Result entry: 2026-11-05 10:35 IST, X2 RESULT (CPU and network; `scripts/x2_exposure.py`, `results/phase2/x2/exposure.json`): SUPPORTED (as predicted): the romanized share is higher for Hindi than for Kannada. [RESULTS.md 3987-3988, `d4363ef` 2026-11-05 10:35:58 +0530]
Source files: results/phase2/x2/exposure.json

### X3: Frequency-matched non-canonical tokenization
Registered: X3. Frequency-matched non-canonical tokenization (Kannada) [RESULTS.md 3400-3412, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b
Forms/conditions run: nc_a, nc_c, x3_m, x3_r, a, c, m, r; tasks/measures: sib, xnli, sentiment, retrieval, xnli_reported_only; seeds: 0
Table [phase2/x3/verdict.json] (20 records):
  (top) | interpretation|retrieval="unresolved"; interpretation|sentiment="unresolved"; interpretation|sib="unresolved"
  D1|retrieval|m | verdict="effect, positive"; status="registered"; n_significant_positive=2; n_significant_negative=0; needed=2; models_above_floor=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D2|retrieval|m | verdict="no effect detected"; status="registered"; n_significant_positive=0; n_significant_negative=0; needed=2; models_above_floor=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D3|retrieval|m | verdict="no effect detected"; status="registered"; n_significant_positive=0; n_significant_negative=1; needed=2; models_above_floor=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D1|sentiment|m | verdict="no effect detected"; status="registered"; n_significant_positive=2; n_significant_negative=0; needed=3; models_above_floor=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D2|sentiment|m | verdict="no effect detected"; status="registered"; n_significant_positive=1; n_significant_negative=0; needed=3; models_above_floor=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D3|sentiment|m | verdict="no effect detected"; status="registered"; n_significant_positive=0; n_significant_negative=0; needed=3; models_above_floor=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D1|sib|m | verdict="effect, positive"; status="registered"; n_significant_positive=3; n_significant_negative=0; needed=3; models_above_floor=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D2|sib|m | verdict="no effect detected"; status="registered"; n_significant_positive=2; n_significant_negative=0; needed=3; models_above_floor=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D3|sib|m | verdict="no effect detected"; status="registered"; n_significant_positive=0; n_significant_negative=2; needed=3; models_above_floor=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D1|retrieval|r | verdict="no effect detected"; status="exploratory (s_ref split), no verdict"; n_significant_positive=1; n_significant_negative=0; needed=2; models_above_floor=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D2|retrieval|r | verdict="no effect detected"; status="exploratory (s_ref split), no verdict"; n_significant_positive=0; n_significant_negative=0; needed=2; models_above_floor=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D3|retrieval|r | verdict="no effect detected"; status="exploratory (s_ref split), no verdict"; n_significant_positive=0; n_significant_negative=0; needed=2; models_above_floor=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  D1|sentiment|r | verdict="uninformative (fewer than 3 models above the floor)"; status="exploratory (s_ref split), no verdict"; n_significant_positive=0; n_significant_negative=0; needed=3; models_above_floor=["qwen3.5-2b", "sarvam-1"]
  D2|sentiment|r | verdict="uninformative (fewer than 3 models above the floor)"; status="exploratory (s_ref split), no verdict"; n_significant_positive=0; n_significant_negative=0; needed=3; models_above_floor=["qwen3.5-2b", "sarvam-1"]
  D3|sentiment|r | verdict="uninformative (fewer than 3 models above the floor)"; status="exploratory (s_ref split), no verdict"; n_significant_positive=0; n_significant_negative=0; needed=3; models_above_floor=["qwen3.5-2b", "sarvam-1"]
  D1|sib|r | verdict="uninformative (fewer than 3 models above the floor)"; status="exploratory (s_ref split), no verdict"; n_significant_positive=2; n_significant_negative=0; needed=3; models_above_floor=["qwen3.5-2b", "sarvam-1"]
  D2|sib|r | verdict="uninformative (fewer than 3 models above the floor)"; status="exploratory (s_ref split), no verdict"; n_significant_positive=0; n_significant_negative=0; needed=3; models_above_floor=["qwen3.5-2b", "sarvam-1"]
  D3|sib|r | verdict="uninformative (fewer than 3 models above the floor)"; status="exploratory (s_ref split), no verdict"; n_significant_positive=0; n_significant_negative=1; needed=3; models_above_floor=["qwen3.5-2b", "sarvam-1"]
  recompute_control | max_abs_dlogprob=0.0; all_below_1e-3=true
Table [phase2/x3/contrasts.csv] (66 rows of 114):
  measure=sentiment | model=qwen3.5-2b | contrast=D1 | cond=m | n=171 | diff=0.11111111111111105 | ci=[0.04093567281961441, 0.1812865436077118] | p=0.0033778479119064286 | p_holm=0.033778479119064286 | significant=True | ci_excludes_0=True
  measure=sentiment | model=qwen3.5-2b | contrast=D2 | cond=m | n=171 | diff=0.03508771929824561 | ci=[-0.023391813039779663, 0.09356725215911865] | p=0.32693958282470703 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3.5-2b | contrast=D3 | cond=m | n=171 | diff=-0.07602339181286544 | ci=[-0.1461988240480423, -0.011695906519889832] | p=0.040959591511636986 | p_holm=0.36863632360473286 | significant=False | ci_excludes_0=True
  measure=sentiment | model=sarvam-1 | contrast=D1 | cond=m | n=163 | diff=0.14110429447852768 | ci=[0.07361963391304016, 0.20858895778656006] | p=0.0001168418675661087 | p_holm=0.0014021024107933044 | significant=True | ci_excludes_0=True
  measure=sentiment | model=sarvam-1 | contrast=D2 | cond=m | n=163 | diff=0.09815950920245409 | ci=[0.04907975345849991, 0.15337423980236053] | p=0.0004024505615234375 | p_holm=0.0044269561767578125 | significant=True | ci_excludes_0=True
  measure=sentiment | model=sarvam-1 | contrast=D3 | cond=m | n=163 | diff=-0.042944785276073594 | ci=[-0.11656441539525986, 0.030674846842885017] | p=0.3240086000878364 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=gemma4-e2b | contrast=D1 | cond=m | n=175 | diff=0.05714285714285705 | ci=[0.0057142856530845165, 0.11428571492433548] | p=0.06391465663909912 | p_holm=0.511317253112793 | significant=False | ci_excludes_0=True
  measure=sentiment | model=gemma4-e2b | contrast=D2 | cond=m | n=175 | diff=0.05142857142857138 | ci=[0.0, 0.10285714268684387] | p=0.0783538818359375 | p_holm=0.5484771728515625 | significant=False | ci_excludes_0=False
  measure=sentiment | model=gemma4-e2b | contrast=D3 | cond=m | n=175 | diff=-0.005714285714285672 | ci=[-0.05714285746216774, 0.04571428522467613] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3-1.7b | contrast=D1 | cond=m | n=170 | diff=-0.01764705882352935 | ci=[-0.0941176488995552, 0.05882352963089943] | p=0.765991824244793 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3-1.7b | contrast=D2 | cond=m | n=170 | diff=-0.02352941176470591 | ci=[-0.10588235408067703, 0.052941177040338516] | p=0.6654658120766188 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3-1.7b | contrast=D3 | cond=m | n=170 | diff=-0.005882352941176561 | ci=[-0.08235294371843338, 0.06470588594675064] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3.5-2b | contrast=D1 | cond=r | n=54 | diff=0.11111111111111116 | ci=[-0.018518518656492233, 0.24074074625968933] | p=0.1795654296875 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3.5-2b | contrast=D2 | cond=r | n=54 | diff=0.0185185185185186 | ci=[-0.1111111119389534, 0.12962962687015533] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3.5-2b | contrast=D3 | cond=r | n=54 | diff=-0.09259259259259256 | ci=[-0.20370370149612427, 0.018518518656492233] | p=0.1796875 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=sarvam-1 | contrast=D1 | cond=r | n=62 | diff=0.14516129032258063 | ci=[0.04838709533214569, 0.24193547666072845] | p=0.01171875 | p_holm=0.140625 | significant=False | ci_excludes_0=True
  measure=sentiment | model=sarvam-1 | contrast=D2 | cond=r | n=62 | diff=0.048387096774193505 | ci=[-0.016129031777381897, 0.12903225421905518] | p=0.375 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=sarvam-1 | contrast=D3 | cond=r | n=62 | diff=-0.09677419354838712 | ci=[-0.20967741310596466, 0.016129031777381897] | p=0.1795654296875 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=gemma4-e2b | contrast=D1 | cond=r | n=48 | diff=0.0625 | ci=[-0.0416666679084301, 0.1666666716337204] | p=0.453125 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=gemma4-e2b | contrast=D2 | cond=r | n=48 | diff=-0.02083333333333337 | ci=[-0.125, 0.0833333358168602] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=gemma4-e2b | contrast=D3 | cond=r | n=48 | diff=-0.08333333333333337 | ci=[-0.1666666716337204, -0.02083333395421505] | p=0.125 | p_holm=1.0 | significant=False | ci_excludes_0=True
  measure=sentiment | model=qwen3-1.7b | contrast=D1 | cond=r | n=42 | diff=-0.07142857142857145 | ci=[-0.2142857164144516, 0.0714285746216774] | p=0.5078125 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3-1.7b | contrast=D2 | cond=r | n=42 | diff=0.0 | ci=[-0.1428571492433548, 0.1428571492433548] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sentiment | model=qwen3-1.7b | contrast=D3 | cond=r | n=42 | diff=0.07142857142857145 | ci=[-0.0714285746216774, 0.2380952388048172] | p=0.548828125 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sib | model=qwen3.5-2b | contrast=D1 | cond=m | n=890 | diff=0.07078651685393261 | ci=[0.043820224702358246, 0.09775280952453613] | p=3.0857298163196464e-07 | p_holm=3.085729816319646e-06 | significant=True | ci_excludes_0=True
  measure=sib | model=qwen3.5-2b | contrast=D2 | cond=m | n=890 | diff=0.031460674157303414 | ci=[0.007865168154239655, 0.056179776787757874] | p=0.014984618863332373 | p_holm=0.07492309431666186 | significant=False | ci_excludes_0=True
  measure=sib | model=qwen3.5-2b | contrast=D3 | cond=m | n=890 | diff=-0.0393258426966292 | ci=[-0.06292134523391724, -0.01460674125701189] | p=0.0018730949300322214 | p_holm=0.01311166451022555 | significant=True | ci_excludes_0=True
  measure=sib | model=sarvam-1 | contrast=D1 | cond=m | n=840 | diff=0.17738095238095242 | ci=[0.14523810148239136, 0.21071428060531616] | p=7.791184970385513e-25 | p_holm=9.349421964462615e-24 | significant=True | ci_excludes_0=True
  measure=sib | model=sarvam-1 | contrast=D2 | cond=m | n=840 | diff=0.07023809523809521 | ci=[0.04404762014746666, 0.09761904925107956] | p=3.957630638799941e-07 | p_holm=3.561867574919947e-06 | significant=True | ci_excludes_0=True
  measure=sib | model=sarvam-1 | contrast=D3 | cond=m | n=840 | diff=-0.1071428571428572 | ci=[-0.13809524476528168, -0.07500000298023224] | p=7.591488591636762e-11 | p_holm=8.350637450800438e-10 | significant=True | ci_excludes_0=True
  measure=sib | model=gemma4-e2b | contrast=D1 | cond=m | n=894 | diff=0.07158836689038034 | ci=[0.043624162673950195, 0.09955257177352905] | p=8.739141189402488e-07 | p_holm=6.99131295152199e-06 | significant=True | ci_excludes_0=True
  measure=sib | model=gemma4-e2b | contrast=D2 | cond=m | n=894 | diff=0.04250559284116334 | ci=[0.014541386626660824, 0.07158836722373962] | p=0.00464181232910736 | p_holm=0.02785087397464416 | significant=True | ci_excludes_0=True
  measure=sib | model=gemma4-e2b | contrast=D3 | cond=m | n=894 | diff=-0.029082774049216997 | ci=[-0.05480984225869179, -0.003355704713612795] | p=0.038179441579785395 | p_holm=0.15271776631914158 | significant=False | ci_excludes_0=True
  measure=sib | model=qwen3-1.7b | contrast=D1 | cond=m | n=854 | diff=0.004683840749414525 | ci=[-0.02107728272676468, 0.029274005442857742] | p=0.7877465824023331 | p_holm=0.7877465824023331 | significant=False | ci_excludes_0=False
  measure=sib | model=qwen3-1.7b | contrast=D2 | cond=m | n=854 | diff=0.01756440281030447 | ci=[-0.004683840554207563, 0.03981264680624008] | p=0.1505180638902295 | p_holm=0.45155419167068855 | significant=False | ci_excludes_0=False
  measure=sib | model=qwen3-1.7b | contrast=D3 | cond=m | n=854 | diff=0.012880562060889944 | ci=[-0.011709601618349552, 0.03747072443366051] | p=0.3337051161974391 | p_holm=0.6674102323948782 | significant=False | ci_excludes_0=False
  measure=sib | model=qwen3.5-2b | contrast=D1 | cond=r | n=304 | diff=0.09868421052631582 | ci=[0.055921051651239395, 0.14473684132099152] | p=3.5887916129517805e-05 | p_holm=0.00035887916129517805 | significant=True | ci_excludes_0=True
  measure=sib | model=qwen3.5-2b | contrast=D2 | cond=r | n=304 | diff=0.0460526315789474 | ci=[0.00657894741743803, 0.08881578594446182] | p=0.048766765904474596 | p_holm=0.2926005954268476 | significant=False | ci_excludes_0=True
  measure=sib | model=qwen3.5-2b | contrast=D3 | cond=r | n=304 | diff=-0.05263157894736842 | ci=[-0.10197368264198303, -0.00657894741743803] | p=0.04022356409571669 | p_holm=0.2815649486700168 | significant=False | ci_excludes_0=True
  measure=sib | model=sarvam-1 | contrast=D1 | cond=r | n=370 | diff=0.1594594594594595 | ci=[0.11081080883741379, 0.2108108103275299] | p=1.7924150285414489e-09 | p_holm=2.1508980342497386e-08 | significant=True | ci_excludes_0=True
  measure=sib | model=sarvam-1 | contrast=D2 | cond=r | n=370 | diff=0.04594594594594603 | ci=[0.008108108304440975, 0.08648648858070374] | p=0.027008317653722358 | p_holm=0.21606654122977886 | significant=False | ci_excludes_0=True
  measure=sib | model=sarvam-1 | contrast=D3 | cond=r | n=370 | diff=-0.11351351351351346 | ci=[-0.1621621549129486, -0.06756756454706192] | p=4.968015141912969e-06 | p_holm=5.464816656104266e-05 | significant=True | ci_excludes_0=True
  measure=sib | model=gemma4-e2b | contrast=D1 | cond=r | n=273 | diff=0.08058608058608058 | ci=[0.029304029420018196, 0.1318681389093399] | p=0.003838265880326096 | p_holm=0.03454439292293486 | significant=True | ci_excludes_0=True
  measure=sib | model=gemma4-e2b | contrast=D2 | cond=r | n=273 | diff=0.043956043956043966 | ci=[-0.007326007355004549, 0.095238097012043] | p=0.11892045255943628 | p_holm=0.5946022627971814 | significant=False | ci_excludes_0=False
  measure=sib | model=gemma4-e2b | contrast=D3 | cond=r | n=273 | diff=-0.03663003663003661 | ci=[-0.08791209012269974, 0.014652014710009098] | p=0.20263875106454066 | p_holm=0.8105550042581626 | significant=False | ci_excludes_0=False
  measure=sib | model=qwen3-1.7b | contrast=D1 | cond=r | n=267 | diff=0.0 | ci=[-0.048689138144254684, 0.048689138144254684] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sib | model=qwen3-1.7b | contrast=D2 | cond=r | n=267 | diff=0.018726591760299616 | ci=[-0.02247191034257412, 0.05992509424686432] | p=0.48685024166479707 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=sib | model=qwen3-1.7b | contrast=D3 | cond=r | n=267 | diff=0.018726591760299616 | ci=[-0.026217227801680565, 0.06741572916507721] | p=0.5223973804968411 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=retrieval | model=qwen3.5-2b | contrast=D1 | cond=m | n=216 | diff=0.07407407407407413 | ci=[0.018518518656492233, 0.12962962687015533] | p=0.013852965261321515 | p_holm=0.08311779156792909 | significant=False | ci_excludes_0=True
  measure=retrieval | model=qwen3.5-2b | contrast=D2 | cond=m | n=216 | diff=0.05092592592592593 | ci=[0.0, 0.10185185074806213] | p=0.08014331245794892 | p_holm=0.230438232421875 | significant=False | ci_excludes_0=False
  measure=retrieval | model=qwen3.5-2b | contrast=D3 | cond=m | n=216 | diff=-0.023148148148148195 | ci=[-0.07870370149612427, 0.032407406717538834] | p=0.5113757815852296 | p_holm=0.5113757815852296 | significant=False | ci_excludes_0=False
  measure=retrieval | model=qwen3.5-2b | contrast=D1 | cond=r | n=62 | diff=0.11290322580645162 | ci=[-0.016129031777381897, 0.25806450843811035] | p=0.1670684814453125 | p_holm=0.66827392578125 | significant=False | ci_excludes_0=False
  measure=retrieval | model=qwen3.5-2b | contrast=D2 | cond=r | n=62 | diff=0.12903225806451613 | ci=[0.032258063554763794, 0.24193547666072845] | p=0.03857421875 | p_holm=0.27001953125 | significant=False | ci_excludes_0=True
  measure=retrieval | model=qwen3.5-2b | contrast=D3 | cond=r | n=62 | diff=0.016129032258064502 | ci=[-0.08064515888690948, 0.11290322244167328] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=retrieval | model=sarvam-1 | contrast=D1 | cond=m | n=187 | diff=0.10160427807486627 | ci=[0.05882352963089943, 0.14973261952400208] | p=6.604194641113281e-05 | p_holm=0.0005283355712890625 | significant=True | ci_excludes_0=True
  measure=retrieval | model=sarvam-1 | contrast=D2 | cond=m | n=187 | diff=0.04278074866310155 | ci=[0.005347593687474728, 0.08556149899959564] | p=0.076812744140625 | p_holm=0.230438232421875 | significant=False | ci_excludes_0=True
  measure=retrieval | model=sarvam-1 | contrast=D3 | cond=m | n=187 | diff=-0.05882352941176472 | ci=[-0.10695187002420425, -0.010695187374949455] | p=0.03468966484069824 | p_holm=0.1734483242034912 | significant=False | ci_excludes_0=True
  measure=retrieval | model=sarvam-1 | contrast=D1 | cond=r | n=75 | diff=0.14666666666666672 | ci=[0.06666667014360428, 0.23999999463558197] | p=0.00341796875 | p_holm=0.03076171875 | significant=True | ci_excludes_0=True
  measure=retrieval | model=sarvam-1 | contrast=D2 | cond=r | n=75 | diff=0.026666666666666727 | ci=[-0.03999999910593033, 0.09333333373069763] | p=0.6875 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=retrieval | model=sarvam-1 | contrast=D3 | cond=r | n=75 | diff=-0.12 | ci=[-0.20000000298023224, -0.03999999910593033] | p=0.01171875 | p_holm=0.09375 | significant=False | ci_excludes_0=True
  measure=retrieval | model=gemma4-e2b | contrast=D1 | cond=m | n=221 | diff=0.16742081447963808 | ci=[0.09954751282930374, 0.23529411852359772] | p=1.969878418086636e-06 | p_holm=1.7728905762779724e-05 | significant=True | ci_excludes_0=True
  measure=retrieval | model=gemma4-e2b | contrast=D2 | cond=m | n=221 | diff=0.07239819004524894 | ci=[0.009049774147570133, 0.13574661314487457] | p=0.04022356409571669 | p_holm=0.1734483242034912 | significant=False | ci_excludes_0=True
  measure=retrieval | model=gemma4-e2b | contrast=D3 | cond=m | n=221 | diff=-0.09502262443438914 | ci=[-0.1538461595773697, -0.031674209982156754] | p=0.003801654409748778 | p_holm=0.026611580868241447 | significant=True | ci_excludes_0=True
  measure=retrieval | model=gemma4-e2b | contrast=D1 | cond=r | n=69 | diff=0.1159420289855072 | ci=[0.0, 0.23188406229019165] | p=0.076812744140625 | p_holm=0.384063720703125 | significant=False | ci_excludes_0=False
  measure=retrieval | model=gemma4-e2b | contrast=D2 | cond=r | n=69 | diff=-0.01449275362318847 | ci=[-0.11594203114509583, 0.07246376574039459] | p=1.0 | p_holm=1.0 | significant=False | ci_excludes_0=False
  measure=retrieval | model=gemma4-e2b | contrast=D3 | cond=r | n=69 | diff=-0.13043478260869568 | ci=[-0.24637681245803833, -0.014492753893136978] | p=0.049041748046875 | p_holm=0.29425048828125 | significant=False | ci_excludes_0=True
Note (facts from results/phase2/x3/verdict.json and RESULTS.md 3400-3412): D1 = a minus NC-O is the Phase 1 NC-O contrast on the matched items; D2 = a minus c and D3 = NC-O minus c are the contrasts the registered interpretation uses. D1|retrieval|m = effect, positive (2 of 2 needed); D2|retrieval|m and D3|retrieval|m = no effect detected (0 of 2 needed). Registered interpretation applied (RESULTS.md 3460-3471): unresolved for all three measures.
Result entry: PHASE 2 RESULT: X3 frequency-matched non-canonical tokenization (run 2026-11-02; registered 2026-11-01) [RESULTS.md 3460-3471, `9dec97e` 2026-11-02 16:00:24 +0530]
Source files: results/phase2/x3/verdict.json; results/phase2/x3/contrasts.csv

### X4: Bengali and Telugu replication, K3b-bn, K3b-te
Registered: X4. Bengali and Telugu replication (core automatic pipeline; no Kanglish, no native-speaker verification, no patching) [RESULTS.md 3413-3426, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
Forms/conditions run: lossy, lower, itrans, native, natural; tasks/measures: sib, sentiment; seeds: 6
Table [phase2/x4/bn/r1.json] (47 records):
  (top) | language="bn"; raw_fallback_rows=[]; counted_models=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  accuracy.gemma4-e2b.english | n=1004; acc_cal=0.7938247011952191; ci95=[0.7689243027888446, 0.8187250996015937]
  accuracy.gemma4-e2b.itrans | n=1004; acc_cal=0.3595617529880478; ci95=[0.3296812749003984, 0.3894422310756972]
  accuracy.gemma4-e2b.lossy | n=1004; acc_cal=0.4302788844621514; ci95=[0.40039840637450197, 0.46115537848605576]
  accuracy.gemma4-e2b.native | n=1004; acc_cal=0.7709163346613546; ci95=[0.7450199203187251, 0.795816733067729]
  accuracy.gemma4-e2b.natural | n=247; acc_cal=0.5748987854251012; ci95=[0.5141700404858299, 0.6356275303643725]
  accuracy.qwen2.5-1.5b.english | n=1004; acc_cal=0.796812749003984; ci95=[0.7719123505976095, 0.8217131474103586]
  accuracy.qwen2.5-1.5b.itrans | n=1004; acc_cal=0.27589641434262946; ci95=[0.24800796812749004, 0.30378486055776893]
  accuracy.qwen2.5-1.5b.lossy | n=1004; acc_cal=0.3057768924302789; ci95=[0.27689243027888444, 0.3346613545816733]
  accuracy.qwen2.5-1.5b.native | n=1004; acc_cal=0.6195219123505976; ci95=[0.5896414342629482, 0.649402390438247]
  accuracy.qwen2.5-1.5b.natural | n=247; acc_cal=0.4331983805668016; ci95=[0.3724696356275304, 0.4939271255060729]
  accuracy.qwen3-1.7b.english | n=1004; acc_cal=0.7818725099601593; ci95=[0.7559760956175299, 0.8067729083665338]
  accuracy.qwen3-1.7b.itrans | n=1004; acc_cal=0.22709163346613545; ci95=[0.20119521912350596, 0.25298804780876494]
  accuracy.qwen3-1.7b.lossy | n=1004; acc_cal=0.27091633466135456; ci95=[0.24402390438247012, 0.29880478087649404]
  accuracy.qwen3-1.7b.native | n=1004; acc_cal=0.6643426294820717; ci95=[0.635433266932271, 0.6932270916334662]
  accuracy.qwen3-1.7b.natural | n=247; acc_cal=0.3967611336032389; ci95=[0.3360323886639676, 0.4574898785425101]
  accuracy.qwen3.5-2b.english | n=1004; acc_cal=0.8037848605577689; ci95=[0.7788844621513944, 0.8286852589641435]
  accuracy.qwen3.5-2b.itrans | n=1004; acc_cal=0.1892430278884462; ci95=[0.16533864541832669, 0.21414342629482072]
  accuracy.qwen3.5-2b.lossy | n=1004; acc_cal=0.3137450199203187; ci95=[0.2848605577689243, 0.3426294820717131]
  accuracy.qwen3.5-2b.native | n=1004; acc_cal=0.6902390438247012; ci95=[0.6613545816733067, 0.7191235059760956]
  accuracy.qwen3.5-2b.natural | n=247; acc_cal=0.4574898785425101; ci95=[0.3967611336032389, 0.5182186234817814]
  accuracy.sarvam-1.english | n=1004; acc_cal=0.7679282868525896; ci95=[0.7420318725099602, 0.7938247011952191]
  accuracy.sarvam-1.itrans | n=1004; acc_cal=0.41932270916334663; ci95=[0.3884462151394422, 0.45119521912350596]
  accuracy.sarvam-1.lossy | n=1004; acc_cal=0.5368525896414342; ci95=[0.5049800796812749, 0.5677290836653387]
  accuracy.sarvam-1.native | n=1004; acc_cal=0.7589641434262948; ci95=[0.7320717131474104, 0.7848605577689243]
  accuracy.sarvam-1.natural | n=247; acc_cal=0.7368421052631579; ci95=[0.680161943319838, 0.7894736842105263]
  counted.qwen3-1.7b | native_ci_lower=0.635433266932271; counted=true; english_acc=0.7818725099601593
  counted.qwen3.5-2b | native_ci_lower=0.6613545816733067; counted=true; english_acc=0.8037848605577689
  counted.sarvam-1 | native_ci_lower=0.7320717131474104; counted=true; english_acc=0.7679282868525896
  counted.gemma4-e2b | native_ci_lower=0.7450199203187251; counted=true; english_acc=0.7938247011952191
  counted.qwen2.5-1.5b | native_ci_lower=0.5896414342629482; counted=false; english_acc=0.796812749003984
  R1_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="itrans"; acc_a=0.7709163346613546; acc_b=0.3595617529880478; n=1004; diff=0.41135458167330674; a_only=462; b_only=49; p=2.6241066729616217e-85; p_holm=1.3120533364808108e-84; significant=true
  R1_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="lossy"; acc_a=0.7709163346613546; acc_b=0.4302788844621514; n=1004; diff=0.34063745019920316; a_only=401; b_only=59; p=1.4723913326592726e-63; p_holm=4.417173997977818e-63; significant=true
  R1_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="itrans"; acc_a=0.6643426294820717; acc_b=0.22709163346613545; n=1004; diff=0.4372509960159362; a_only=466; b_only=27; p=1.8794432629542004e-104; p_holm=1.3156102840679403e-103; significant=true
  R1_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="lossy"; acc_a=0.6643426294820717; acc_b=0.27091633466135456; n=1004; diff=0.3934262948207171; a_only=430; b_only=35; p=1.3658210340659348e-87; p_holm=8.19492620439561e-87; significant=true
  R1_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="itrans"; acc_a=0.6902390438247012; acc_b=0.1892430278884462; n=1004; diff=0.500996015936255; a_only=519; b_only=16; p=3.1492097101872245e-131; p_holm=2.5193677681497796e-130; significant=true
  R1_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="lossy"; acc_a=0.6902390438247012; acc_b=0.3137450199203187; n=1004; diff=0.3764940239043825; a_only=412; b_only=34; p=1.3353085715969984e-83; p_holm=5.341234286387994e-83; significant=true
  R1_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="itrans"; acc_a=0.7589641434262948; acc_b=0.41932270916334663; n=1004; diff=0.3396414342629482; a_only=406; b_only=65; p=2.5658712964385488e-61; p_holm=5.1317425928770976e-61; significant=true
  R1_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="lossy"; acc_a=0.7589641434262948; acc_b=0.5368525896414342; n=1004; diff=0.22211155378486058; a_only=300; b_only=77; p=3.40038049201884e-32; p_holm=3.40038049201884e-32; significant=true
  R1 | R1="supported"
  R1.native_vs_itrans | n_counted=4; positive_and_significant=4; significantly_negative=0; verdict="supported"
  R1.native_vs_lossy | n_counted=4; positive_and_significant=4; significantly_negative=0; verdict="supported"
  natural_257_accuracy.qwen3-1.7b | n=247; acc_cal=0.3967611336032389; ci95=[0.3360323886639676, 0.4574898785425101]
  natural_257_accuracy.qwen3.5-2b | n=247; acc_cal=0.4574898785425101; ci95=[0.3967611336032389, 0.5182186234817814]
  natural_257_accuracy.sarvam-1 | n=247; acc_cal=0.7368421052631579; ci95=[0.680161943319838, 0.7894736842105263]
  natural_257_accuracy.gemma4-e2b | n=247; acc_cal=0.5748987854251012; ci95=[0.5141700404858299, 0.6356275303643725]
  natural_257_accuracy.qwen2.5-1.5b | n=247; acc_cal=0.4331983805668016; ci95=[0.3724696356275304, 0.4939271255060729]
Table [phase2/x4/bn/r2.json] (22 records):
  (top) | language="bn"; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  models.qwen3.5-2b | counted=true
  models.qwen3.5-2b.acc | native=0.991044776119403; itrans=0.15024875621890546; lossy=0.25671641791044775; lower=0.16517412935323383
  models.qwen3.5-2b.layer | native=6; itrans=6; lossy=6; lower=6
  models.qwen3.5-2b.native_minus_itrans | diff=0.8407960199004975; ci95=[0.817910447761194, 0.8626865671641791]; n=1005
  models.qwen3.5-2b.native_minus_lossy | diff=0.7343283582089553; ci95=[0.7074626865671642, 0.7611940298507462]; n=1005
  models.sarvam-1 | counted=true
  models.sarvam-1.acc | native=0.9412935323383085; itrans=0.32238805970149254; lossy=0.6059701492537314; lower=0.28059701492537314
  models.sarvam-1.layer | native=26; itrans=17; lossy=17; lower=17
  models.sarvam-1.native_minus_itrans | diff=0.618905472636816; ci95=[0.5870646766169154, 0.6497512437810945]; n=1005
  models.sarvam-1.native_minus_lossy | diff=0.3353233830845771; ci95=[0.3044776119402985, 0.36716417910447763]; n=1005
  models.gemma4-e2b | counted=true
  models.gemma4-e2b.acc | native=0.9960199004975124; itrans=0.30149253731343284; lossy=0.40696517412935324; lower=0.3194029850746269
  models.gemma4-e2b.layer | native=7; itrans=7; lossy=8; lower=8
  models.gemma4-e2b.native_minus_itrans | diff=0.6945273631840796; ci95=[0.6666666666666666, 0.7233830845771144]; n=1005
  models.gemma4-e2b.native_minus_lossy | diff=0.5890547263681593; ci95=[0.5592039800995025, 0.6199004975124378]; n=1005
  models.qwen2.5-1.5b | counted=false
  models.qwen2.5-1.5b.acc | native=0.4766169154228856; itrans=0.06666666666666667; lossy=0.11741293532338308; lower=0.08557213930348259
  models.qwen2.5-1.5b.layer | native=16; itrans=1; lossy=1; lower=1
  models.qwen2.5-1.5b.native_minus_itrans | diff=0.4099502487562189; ci95=[0.37512437810945276, 0.44477611940298506]; n=1005
  models.qwen2.5-1.5b.native_minus_lossy | diff=0.3592039800995025; ci95=[0.32338308457711445, 0.39502487562189054]; n=1005
  R2 | n_counted=3; native_minus_itrans_ci_above_0=3; ci_below_0=0; verdict="supported"
Table [phase2/x4/bn/r3.json] (23 records):
  (top) | language="bn"; n_ids_with_natural=476
  models.qwen3.5-2b.acc_test_half | native=0.9957627118644068; natural=0.5127118644067796; itrans=0.23728813559322035; lossy=0.3813559322033898; lower=0.2457627118644068
  models.qwen3.5-2b.natural_minus_itrans | diff=0.2754237288135593; ci95=[0.2076271186440678, 0.3432203389830508]; n=236
  models.qwen3.5-2b.native_minus_natural | diff=0.4830508474576271; ci95=[0.4194915254237288, 0.5466101694915254]; n=236
  models.qwen3.5-2b.natural_minus_lossy | diff=0.13135593220338984; ci95=[0.059322033898305086, 0.2033898305084746]; n=236
  models.qwen3.5-2b.L1_lower_minus_itrans | diff=0.00847457627118644; ci95=[-0.046610169491525424, 0.0635593220338983]; n=236
  models.qwen3.5-2b.L2_lossy_minus_lower | diff=0.13559322033898305; ci95=[0.07203389830508475, 0.19915254237288135]; n=236
  models.sarvam-1.acc_test_half | native=0.9957627118644068; natural=0.8940677966101694; itrans=0.4661016949152542; lossy=0.7076271186440678; lower=0.4491525423728814
  models.sarvam-1.natural_minus_itrans | diff=0.4279661016949153; ci95=[0.3601694915254237, 0.4957627118644068]; n=236
  models.sarvam-1.native_minus_natural | diff=0.1016949152542373; ci95=[0.0635593220338983, 0.13983050847457626]; n=236
  models.sarvam-1.natural_minus_lossy | diff=0.1864406779661017; ci95=[0.13135593220338984, 0.24152542372881355]; n=236
  models.sarvam-1.L1_lower_minus_itrans | diff=-0.01694915254237288; ci95=[-0.0847457627118644, 0.05084745762711865]; n=236
  models.sarvam-1.L2_lossy_minus_lower | diff=0.2584745762711864; ci95=[0.19491525423728814, 0.326271186440678]; n=236
  models.gemma4-e2b.acc_test_half | native=1.0; natural=0.8432203389830508; itrans=0.4661016949152542; lossy=0.6313559322033898; lower=0.4915254237288136
  models.gemma4-e2b.natural_minus_itrans | diff=0.3771186440677966; ci95=[0.3093220338983051, 0.4449152542372881]; n=236
  models.gemma4-e2b.native_minus_natural | diff=0.15677966101694915; ci95=[0.11016949152542373, 0.2033898305084746]; n=236
  models.gemma4-e2b.natural_minus_lossy | diff=0.211864406779661; ci95=[0.1483050847457627, 0.2754237288135593]; n=236
  models.gemma4-e2b.L1_lower_minus_itrans | diff=0.025423728813559324; ci95=[-0.046610169491525424, 0.09745762711864407]; n=236
  models.gemma4-e2b.L2_lossy_minus_lower | diff=0.13983050847457626; ci95=[0.06779661016949153, 0.211864406779661]; n=236
  R3 | n_counted=3; natural_minus_itrans_ci_above_0=3; ci_below_0=0; verdict="supported"
  retrieval_ladder_M4c.L1 | ci_above_0=0; ci_below_0=0; verdict="no effect detected"
  retrieval_ladder_M4c.L2 | ci_above_0=3; ci_below_0=0; verdict="effect, positive"
  retrieval_ladder_M4c.L3 | ci_above_0=3; ci_below_0=0; verdict="effect, positive"
Table [phase2/x4/bn/r4.json] (13 records):
  (top) | language="bn"; qualifying=["qwen3-1.7b", "sarvam-1", "gemma4-e2b"]; effect_in=["qwen3-1.7b", "sarvam-1", "gemma4-e2b"]; R4="supported"
  models.qwen3-1.7b | native_layer=3; itrans_layer=1; itrans_minus_native=-2; ci95=[-2.0, -1.0]; qualifies=true; expected_sign=-1; ci_sign=-1; effect=true
  models.qwen3-1.7b.tokens_per_word | native=6.461; itrans=3.1301111111111113; diff=-3.330888888888889
  models.qwen3.5-2b | native_layer=1; itrans_layer=2; itrans_minus_native=1; ci95=[0.0, 1.0]; qualifies=false; expected_sign=1; ci_sign=0; effect=false
  models.qwen3.5-2b.tokens_per_word | native=2.5585555555555555; itrans=3.0144444444444445; diff=0.455888888888889
  models.sarvam-1 | native_layer=0; itrans_layer=7; itrans_minus_native=7; ci95=[7.0, 9.0]; qualifies=true; expected_sign=1; ci_sign=1; effect=true
  models.sarvam-1.tokens_per_word | native=1.1446666666666667; itrans=3.8333333333333335; diff=2.6886666666666668
  models.gemma4-e2b | native_layer=0; itrans_layer=1; itrans_minus_native=1; ci95=[1.0, 2.0]; qualifies=true; expected_sign=1; ci_sign=1; effect=true
  models.gemma4-e2b.tokens_per_word | native=1.0685555555555555; itrans=2.818888888888889; diff=1.7503333333333335
  models.qwen2.5-1.5b | native_layer=4; itrans_layer=1; itrans_minus_native=-3; ci95=[-3.0, -3.0]; qualifies=true; expected_sign=-1; ci_sign=-1; effect=true
  models.qwen2.5-1.5b.tokens_per_word | native=6.461; itrans=3.1301111111111113; diff=-3.330888888888889
  main_analysis_excluding_qwen2.5 | qualifying=["qwen3-1.7b", "sarvam-1", "gemma4-e2b"]; effect_in=["qwen3-1.7b", "sarvam-1", "gemma4-e2b"]; verdict="supported"
  sensitivity_including_qwen2.5 | qualifying=["qwen3-1.7b", "sarvam-1", "gemma4-e2b", "qwen2.5-1.5b"]; effect_in=["qwen3-1.7b", "sarvam-1", "gemma4-e2b", "qwen2.5-1.5b"]; verdict="supported"
Table [phase2/x4/te/r1.json] (47 records):
  (top) | language="te"; raw_fallback_rows=[]; counted_models=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  accuracy.gemma4-e2b.english | n=1004; acc_cal=0.7938247011952191; ci95=[0.7689243027888446, 0.8187250996015937]
  accuracy.gemma4-e2b.itrans | n=1004; acc_cal=0.4252988047808765; ci95=[0.3954183266932271, 0.45617529880478086]
  accuracy.gemma4-e2b.lossy | n=1004; acc_cal=0.5079681274900398; ci95=[0.4770916334661355, 0.5388446215139442]
  accuracy.gemma4-e2b.native | n=1004; acc_cal=0.7699203187250996; ci95=[0.7440239043824701, 0.795816733067729]
  accuracy.gemma4-e2b.natural | n=249; acc_cal=0.606425702811245; ci95=[0.5461847389558233, 0.6666666666666666]
  accuracy.qwen2.5-1.5b.english | n=1004; acc_cal=0.796812749003984; ci95=[0.7719123505976095, 0.8217131474103586]
  accuracy.qwen2.5-1.5b.itrans | n=1004; acc_cal=0.3107569721115538; ci95=[0.2818725099601594, 0.3396414342629482]
  accuracy.qwen2.5-1.5b.lossy | n=1004; acc_cal=0.40936254980079684; ci95=[0.3784860557768924, 0.4392430278884462]
  accuracy.qwen2.5-1.5b.native | n=1004; acc_cal=0.4113545816733068; ci95=[0.38147410358565736, 0.44123505976095617]
  accuracy.qwen2.5-1.5b.natural | n=249; acc_cal=0.5301204819277109; ci95=[0.46586345381526106, 0.5903614457831325]
  accuracy.qwen3-1.7b.english | n=1004; acc_cal=0.7818725099601593; ci95=[0.7559760956175299, 0.8067729083665338]
  accuracy.qwen3-1.7b.itrans | n=1004; acc_cal=0.26593625498007967; ci95=[0.23904382470119523, 0.29382470119521914]
  accuracy.qwen3-1.7b.lossy | n=1004; acc_cal=0.34860557768924305; ci95=[0.3197211155378486, 0.3784860557768924]
  accuracy.qwen3-1.7b.native | n=1004; acc_cal=0.6683266932270916; ci95=[0.6394422310756972, 0.6972111553784861]
  accuracy.qwen3-1.7b.natural | n=249; acc_cal=0.4819277108433735; ci95=[0.41767068273092367, 0.5421686746987951]
  accuracy.qwen3.5-2b.english | n=1004; acc_cal=0.8037848605577689; ci95=[0.7788844621513944, 0.8286852589641435]
  accuracy.qwen3.5-2b.itrans | n=1004; acc_cal=0.2918326693227092; ci95=[0.2639442231075697, 0.3207171314741036]
  accuracy.qwen3.5-2b.lossy | n=1004; acc_cal=0.3884462151394422; ci95=[0.35856573705179284, 0.41932270916334663]
  accuracy.qwen3.5-2b.native | n=1004; acc_cal=0.7181274900398407; ci95=[0.6912350597609562, 0.7460159362549801]
  accuracy.qwen3.5-2b.natural | n=249; acc_cal=0.5020080321285141; ci95=[0.43775100401606426, 0.5622489959839357]
  accuracy.sarvam-1.english | n=1004; acc_cal=0.7679282868525896; ci95=[0.7420318725099602, 0.7938247011952191]
  accuracy.sarvam-1.itrans | n=1004; acc_cal=0.45617529880478086; ci95=[0.4243027888446215, 0.48705179282868527]
  accuracy.sarvam-1.lossy | n=1004; acc_cal=0.6902390438247012; ci95=[0.6623505976095617, 0.7191235059760956]
  accuracy.sarvam-1.native | n=1004; acc_cal=0.7719123505976095; ci95=[0.7460159362549801, 0.797808764940239]
  accuracy.sarvam-1.natural | n=249; acc_cal=0.7188755020080321; ci95=[0.6626506024096386, 0.7751004016064257]
  counted.qwen3-1.7b | native_ci_lower=0.6394422310756972; counted=true; english_acc=0.7818725099601593
  counted.qwen3.5-2b | native_ci_lower=0.6912350597609562; counted=true; english_acc=0.8037848605577689
  counted.sarvam-1 | native_ci_lower=0.7460159362549801; counted=true; english_acc=0.7679282868525896
  counted.gemma4-e2b | native_ci_lower=0.7440239043824701; counted=true; english_acc=0.7938247011952191
  counted.qwen2.5-1.5b | native_ci_lower=0.38147410358565736; counted=false; english_acc=0.796812749003984
  R1_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="itrans"; acc_a=0.7699203187250996; acc_b=0.4252988047808765; n=1004; diff=0.3446215139442231; a_only=391; b_only=45; p=6.057708699192705e-70; p_holm=3.028854349596353e-69; significant=true
  R1_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="lossy"; acc_a=0.7699203187250996; acc_b=0.5079681274900398; n=1004; diff=0.26195219123505975; a_only=309; b_only=46; p=5.632666389647595e-49; p_holm=1.126533277929519e-48; significant=true
  R1_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="itrans"; acc_a=0.6683266932270916; acc_b=0.26593625498007967; n=1004; diff=0.40239043824701193; a_only=433; b_only=29; p=1.561176664981617e-93; p_holm=1.0928236654871318e-92; significant=true
  R1_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="lossy"; acc_a=0.6683266932270916; acc_b=0.34860557768924305; n=1004; diff=0.31972111553784854; a_only=379; b_only=58; p=7.574557505427686e-59; p_holm=3.0298230021710743e-58; significant=true
  R1_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="itrans"; acc_a=0.7181274900398407; acc_b=0.2918326693227092; n=1004; diff=0.4262948207171315; a_only=460; b_only=32; p=3.167137949727029e-98; p_holm=2.533710359781623e-97; significant=true
  R1_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="lossy"; acc_a=0.7181274900398407; acc_b=0.3884462151394422; n=1004; diff=0.32968127490039845; a_only=362; b_only=31; p=1.0431150385447563e-72; p_holm=6.258690231268538e-72; significant=true
  R1_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="itrans"; acc_a=0.7719123505976095; acc_b=0.45617529880478086; n=1004; diff=0.3157370517928287; a_only=388; b_only=71; p=6.203633714498157e-54; p_holm=1.8610901143494472e-53; significant=true
  R1_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="lossy"; acc_a=0.7719123505976095; acc_b=0.6902390438247012; n=1004; diff=0.0816733067729083; a_only=155; b_only=73; p=5.9110376349771216e-08; p_holm=5.9110376349771216e-08; significant=true
  R1 | R1="supported"
  R1.native_vs_itrans | n_counted=4; positive_and_significant=4; significantly_negative=0; verdict="supported"
  R1.native_vs_lossy | n_counted=4; positive_and_significant=4; significantly_negative=0; verdict="supported"
  natural_257_accuracy.qwen3-1.7b | n=249; acc_cal=0.4819277108433735; ci95=[0.41767068273092367, 0.5421686746987951]
  natural_257_accuracy.qwen3.5-2b | n=249; acc_cal=0.5020080321285141; ci95=[0.43775100401606426, 0.5622489959839357]
  natural_257_accuracy.sarvam-1 | n=249; acc_cal=0.7188755020080321; ci95=[0.6626506024096386, 0.7751004016064257]
  natural_257_accuracy.gemma4-e2b | n=249; acc_cal=0.606425702811245; ci95=[0.5461847389558233, 0.6666666666666666]
  natural_257_accuracy.qwen2.5-1.5b | n=249; acc_cal=0.5301204819277109; ci95=[0.46586345381526106, 0.5903614457831325]
Table [phase2/x4/te/r2.json] (22 records):
  (top) | language="te"; counted_models=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
  models.qwen3.5-2b | counted=true
  models.qwen3.5-2b.acc | native=0.9731343283582089; itrans=0.1691542288557214; lossy=0.3124378109452736; lower=0.18208955223880596
  models.qwen3.5-2b.layer | native=9; itrans=2; lossy=6; lower=6
  models.qwen3.5-2b.native_minus_itrans | diff=0.8039800995024876; ci95=[0.7781094527363184, 0.8288557213930349]; n=1005
  models.qwen3.5-2b.native_minus_lossy | diff=0.6606965174129353; ci95=[0.6308208955223881, 0.690547263681592]; n=1005
  models.sarvam-1 | counted=true
  models.sarvam-1.acc | native=0.9273631840796019; itrans=0.34228855721393037; lossy=0.8378109452736319; lower=0.37213930348258706
  models.sarvam-1.layer | native=11; itrans=17; lossy=21; lower=17
  models.sarvam-1.native_minus_itrans | diff=0.5850746268656717; ci95=[0.5532338308457712, 0.6169154228855721]; n=1005
  models.sarvam-1.native_minus_lossy | diff=0.08955223880597014; ci95=[0.0626865671641791, 0.11641791044776119]; n=1005
  models.gemma4-e2b | counted=true
  models.gemma4-e2b.acc | native=0.9890547263681592; itrans=0.28756218905472636; lossy=0.5343283582089552; lower=0.25870646766169153
  models.gemma4-e2b.layer | native=7; itrans=7; lossy=7; lower=7
  models.gemma4-e2b.native_minus_itrans | diff=0.7014925373134329; ci95=[0.672636815920398, 0.7293532338308458]; n=1005
  models.gemma4-e2b.native_minus_lossy | diff=0.454726368159204; ci95=[0.4248756218905473, 0.4855721393034826]; n=1005
  models.qwen2.5-1.5b | counted=false
  models.qwen2.5-1.5b.acc | native=0.18109452736318407; itrans=0.11243781094527364; lossy=0.18706467661691542; lower=0.12437810945273632
  models.qwen2.5-1.5b.layer | native=17; itrans=1; lossy=1; lower=1
  models.qwen2.5-1.5b.native_minus_itrans | diff=0.06865671641791045; ci95=[0.03880597014925373, 0.09850746268656717]; n=1005
  models.qwen2.5-1.5b.native_minus_lossy | diff=-0.005970149253731343; ci95=[-0.03980099502487562, 0.025870646766169153]; n=1005
  R2 | n_counted=3; native_minus_itrans_ci_above_0=3; ci_below_0=0; verdict="supported"
Table [phase2/x4/te/r3.json] (23 records):
  (top) | language="te"; n_ids_with_natural=487
  models.qwen3.5-2b.acc_test_half | native=0.9876543209876543; natural=0.6748971193415638; itrans=0.2551440329218107; lossy=0.45267489711934156; lower=0.2674897119341564
  models.qwen3.5-2b.natural_minus_itrans | diff=0.41975308641975306; ci95=[0.3497942386831276, 0.4897119341563786]; n=243
  models.qwen3.5-2b.native_minus_natural | diff=0.31275720164609055; ci95=[0.2551440329218107, 0.37448559670781895]; n=243
  models.qwen3.5-2b.natural_minus_lossy | diff=0.2222222222222222; ci95=[0.16049382716049382, 0.2839506172839506]; n=243
  models.qwen3.5-2b.L1_lower_minus_itrans | diff=0.012345679012345678; ci95=[-0.0411522633744856, 0.06584362139917696]; n=243
  models.qwen3.5-2b.L2_lossy_minus_lower | diff=0.18518518518518517; ci95=[0.12345679012345678, 0.25102880658436216]; n=243
  models.sarvam-1.acc_test_half | native=0.9547325102880658; natural=0.9259259259259259; itrans=0.5267489711934157; lossy=0.8847736625514403; lower=0.49382716049382713
  models.sarvam-1.natural_minus_itrans | diff=0.3991769547325103; ci95=[0.3374485596707819, 0.4609053497942387]; n=243
  models.sarvam-1.native_minus_natural | diff=0.02880658436213992; ci95=[-0.012345679012345678, 0.06995884773662552]; n=243
  models.sarvam-1.natural_minus_lossy | diff=0.0411522633744856; ci95=[0.00823045267489712, 0.07407407407407407]; n=243
  models.sarvam-1.L1_lower_minus_itrans | diff=-0.03292181069958848; ci95=[-0.09876543209876543, 0.03292181069958848]; n=243
  models.sarvam-1.L2_lossy_minus_lower | diff=0.39094650205761317; ci95=[0.32510288065843623, 0.4567901234567901]; n=243
  models.gemma4-e2b.acc_test_half | native=0.9958847736625515; natural=0.8559670781893004; itrans=0.48559670781893005; lossy=0.6831275720164609; lower=0.4444444444444444
  models.gemma4-e2b.natural_minus_itrans | diff=0.37037037037037035; ci95=[0.3004115226337449, 0.43621399176954734]; n=243
  models.gemma4-e2b.native_minus_natural | diff=0.13991769547325103; ci95=[0.09876543209876543, 0.18518518518518517]; n=243
  models.gemma4-e2b.natural_minus_lossy | diff=0.1728395061728395; ci95=[0.11522633744855967, 0.23045267489711935]; n=243
  models.gemma4-e2b.L1_lower_minus_itrans | diff=-0.0411522633744856; ci95=[-0.10699588477366255, 0.0205761316872428]; n=243
  models.gemma4-e2b.L2_lossy_minus_lower | diff=0.23868312757201646; ci95=[0.1728395061728395, 0.3045267489711934]; n=243
  R3 | n_counted=3; natural_minus_itrans_ci_above_0=3; ci_below_0=0; verdict="supported"
  retrieval_ladder_M4c.L1 | ci_above_0=0; ci_below_0=0; verdict="no effect detected"
  retrieval_ladder_M4c.L2 | ci_above_0=3; ci_below_0=0; verdict="effect, positive"
  retrieval_ladder_M4c.L3 | ci_above_0=3; ci_below_0=0; verdict="effect, positive"
Table [phase2/x4/te/r4.json] (13 records):
  (top) | language="te"; qualifying=["qwen3-1.7b", "sarvam-1"]; effect_in=["qwen3-1.7b", "sarvam-1"]; R4="uninformative (fewer than three qualifying models)"
  models.qwen3-1.7b | native_layer=5; itrans_layer=2; itrans_minus_native=-3; ci95=[-5.0, -2.0]; qualifies=true; expected_sign=-1; ci_sign=-1; effect=true
  models.qwen3-1.7b.tokens_per_word | native=10.376444444444445; itrans=3.6935555555555557; diff=-6.68288888888889
  models.qwen3.5-2b | native_layer=2; itrans_layer=2; itrans_minus_native=0; ci95=[0.0, 0.0]; qualifies=false; expected_sign=-1; ci_sign=0; effect=false
  models.qwen3.5-2b.tokens_per_word | native=4.383222222222222; itrans=3.5923333333333334; diff=-0.7908888888888885
  models.sarvam-1 | native_layer=2; itrans_layer=7; itrans_minus_native=5; ci95=[5.0, 7.0]; qualifies=true; expected_sign=1; ci_sign=1; effect=true
  models.sarvam-1.tokens_per_word | native=1.856; itrans=4.403555555555555; diff=2.5475555555555554
  models.gemma4-e2b | native_layer=1; itrans_layer=2; itrans_minus_native=1; ci95=[1.0, 2.0]; qualifies=false; expected_sign=1; ci_sign=1; effect=false
  models.gemma4-e2b.tokens_per_word | native=2.449; itrans=3.337666666666667; diff=0.8886666666666669
  models.qwen2.5-1.5b | native_layer=5; itrans_layer=1; itrans_minus_native=-4; ci95=[-5.0, -2.0]; qualifies=true; expected_sign=-1; ci_sign=-1; effect=true
  models.qwen2.5-1.5b.tokens_per_word | native=10.376444444444445; itrans=3.6935555555555557; diff=-6.68288888888889
  main_analysis_excluding_qwen2.5 | qualifying=["qwen3-1.7b", "sarvam-1"]; effect_in=["qwen3-1.7b", "sarvam-1"]; verdict="uninformative (fewer than three qualifying models)"
  sensitivity_including_qwen2.5 | qualifying=["qwen3-1.7b", "sarvam-1", "qwen2.5-1.5b"]; effect_in=["qwen3-1.7b", "sarvam-1", "qwen2.5-1.5b"]; verdict="supported"
Table [phase2/x4/k3b_bn/verdict.json] (4 records):
  (top) | K3b="refuted"; n=490; n_primary_defective_excluded=10
  statistics.vowel_doubling | gemini_rate=0.0009495701270370846; human_rate=0.0066021685584418885; ratio=0.14382700451095165; ci90=[0.09471841159363945, 0.19694176278724737]; ci95=[0.086815734577584, 0.20842633432122057]; verdict="differs (Gemini lower)"
  statistics.h_digraph | gemini_rate=0.030642884640061593; human_rate=0.029100327569132323; ratio=1.0530082373562526; ci90=[1.0242733659220826, 1.0823699147491797]; ci95=[1.0191290615802133, 1.0877862524071542]; verdict="matches"
  statistics.english_word_share | gemini_rate=0.09398014729426833; human_rate=0.09306069876026404; ratio=1.0098800948870252; ci90=[0.9487823980224456, 1.074782858384047]; ci95=[0.9375053352906352, 1.0879930212033773]; verdict="matches"
Table [phase2/x4/k3b_te/verdict.json] (4 records):
  (top) | K3b="refuted"; n=496; n_primary_defective_excluded=4
  statistics.vowel_doubling | gemini_rate=0.016842753588856778; human_rate=0.051304327945311964; ratio=0.32829108699777476; ci90=[0.293083065079531, 0.3658766103318625]; ci95=[0.28667444247851276, 0.37361137069627043]; verdict="differs (Gemini lower)"
  statistics.h_digraph | gemini_rate=0.023736201260245417; human_rate=0.019799263814902032; ratio=1.1988426176926956; ci90=[1.1111400376283775, 1.2916617601021299]; ci95=[1.095237046146036, 1.3114117727268901]; verdict="differs (Gemini higher)"
  statistics.english_word_share | gemini_rate=0.0717123935666982; human_rate=0.06824196597353498; ratio=1.0508547422931676; ci90=[0.9860681427256742, 1.1215122140559257]; ci95=[0.9739994696029738, 1.135156513641658]; verdict="matches"
Result entry: 2026-11-05 10:52 IST, K3b-te RESULT (Gemini vs Dakshina native-speaker romanization, Telugu; `results/phase2/x4/k3b_te/verdict.json`): REFUTED by the registered rule (against the prediction that Gemini matches the human romanizati [RESULTS.md 3991-3992, `b9246e2` 2026-11-05 10:52:45 +0530]
Source files: results/phase2/x4/bn/r1.json; results/phase2/x4/bn/r2.json; results/phase2/x4/bn/r3.json; results/phase2/x4/bn/r4.json; results/phase2/x4/te/r1.json; results/phase2/x4/te/r2.json; results/phase2/x4/te/r3.json; results/phase2/x4/te/r4.json; results/phase2/x4/k3b_bn/verdict.json; results/phase2/x4/k3b_te/verdict.json

### X5: Cross-language consistency
Registered: X5. Cross-language consistency (analysis only, descriptive; after X2 and X4) [RESULTS.md 3427-3429, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [phase2/x5/analysis.json] (35 records):
  (top) | n_common_flores_ids=465; n_common_sib_ids=239
  e_documents | kn=0.00044731469048331726; hi=0.004371827182154524; bn=0.0006881983653808189; te=0.012121209073381014
  accuracy.qwen3-1.7b | entered=true; spearman_e_vs_gap=-0.6000000000000001
  accuracy.qwen3-1.7b.gap_by_language | kn=0.28870292887029286; hi=0.13807531380753146; bn=0.29288702928870286; te=0.20083682008368203
  accuracy.qwen3.5-2b | entered=true; spearman_e_vs_gap=-0.7378647873726218
  accuracy.qwen3.5-2b.gap_by_language | kn=0.2426778242677824; hi=0.08786610878661094; bn=0.2426778242677824; te=0.2343096234309623
  accuracy.sarvam-1 | entered=true; spearman_e_vs_gap=0.0
  accuracy.sarvam-1.gap_by_language | kn=0.01673640167364021; hi=0.04184100418410042; bn=-0.008368200836820106; te=0.0167364016736401
  accuracy.gemma4-e2b | entered=true; spearman_e_vs_gap=-0.7999999999999999
  accuracy.gemma4-e2b.gap_by_language | kn=0.20502092050209209; hi=0.03347280334728042; bn=0.20083682008368198; te=0.17991631799163177
  retrieval.qwen3.5-2b | entered=true; spearman_e_vs_gap=-0.6000000000000001
  retrieval.qwen3.5-2b.gap_by_language.kn | native=1.0; natural=0.5826086956521739; gap=0.4173913043478261; n_test=230
  retrieval.qwen3.5-2b.gap_by_language.hi | native=0.991304347826087; natural=0.9260869565217391; gap=0.0652173913043479; n_test=230
  retrieval.qwen3.5-2b.gap_by_language.bn | native=0.9956521739130435; natural=0.508695652173913; gap=0.4869565217391305; n_test=230
  retrieval.qwen3.5-2b.gap_by_language.te | native=0.9869565217391304; natural=0.6608695652173913; gap=0.32608695652173914; n_test=230
  retrieval.sarvam-1 | entered=true; spearman_e_vs_gap=-0.7999999999999999
  retrieval.sarvam-1.gap_by_language.kn | native=0.9869565217391304; natural=0.9173913043478261; gap=0.06956521739130428; n_test=230
  retrieval.sarvam-1.gap_by_language.hi | native=0.991304347826087; natural=0.9347826086956522; gap=0.05652173913043479; n_test=230
  retrieval.sarvam-1.gap_by_language.bn | native=0.9956521739130435; natural=0.8913043478260869; gap=0.10434782608695659; n_test=230
  retrieval.sarvam-1.gap_by_language.te | native=0.9521739130434783; natural=0.9260869565217391; gap=0.026086956521739202; n_test=230
  retrieval.gemma4-e2b | entered=true; spearman_e_vs_gap=-0.7999999999999999
  retrieval.gemma4-e2b.gap_by_language.kn | native=1.0; natural=0.717391304347826; gap=0.28260869565217395; n_test=230
  retrieval.gemma4-e2b.gap_by_language.hi | native=1.0; natural=0.9782608695652174; gap=0.021739130434782594; n_test=230
  retrieval.gemma4-e2b.gap_by_language.bn | native=1.0; natural=0.8434782608695652; gap=0.15652173913043477; n_test=230
  retrieval.gemma4-e2b.gap_by_language.te | native=1.0; natural=0.8608695652173913; gap=0.13913043478260867; n_test=230
  accuracy_verdict | n_models=4; negative_in=["qwen3-1.7b", "qwen3.5-2b", "gemma4-e2b"]; verdict="consistent"
  retrieval_verdict | n_models=3; negative_in=["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]; verdict="consistent"
  k3b_reported_next_to_the_figure.kn | verdict="refuted"
  k3b_reported_next_to_the_figure.kn.ratios | vowel_doubling=0.358769166332673; h_digraph=1.0478941969753321; english_word_share=0.8948261113751242
  k3b_reported_next_to_the_figure.hi | verdict="inconclusive"
  k3b_reported_next_to_the_figure.hi.ratios | vowel_doubling=0.8758003653547612; h_digraph=0.9993841431579763; english_word_share=1.1201979881034356
  k3b_reported_next_to_the_figure.bn | verdict="refuted"
  k3b_reported_next_to_the_figure.bn.ratios | vowel_doubling=0.14382700451095165; h_digraph=1.0530082373562526; english_word_share=1.0098800948870252
  k3b_reported_next_to_the_figure.te | verdict="refuted"
  k3b_reported_next_to_the_figure.te.ratios | vowel_doubling=0.32829108699777476; h_digraph=1.1988426176926956; english_word_share=1.0508547422931676
Result entry: 2026-11-05 11:42 IST, X5 RESULT (analysis only, descriptive; `scripts/x5_analyse.py`, `results/phase2/x5/analysis.json`): "consistent" on both measures (as predicted). [RESULTS.md 3995-3996, `124a4cc` 2026-11-05 11:42:00 +0530]
Source files: results/phase2/x5/analysis.json

### X6: New models screen and counting
Registered: X6. New models, only if they add a new tokenizer regime [RESULTS.md 3430-3432, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: oro-1.7b, llama-3.2-1b
Forms/conditions run: lossy, lower, itrans, native, english; tasks/measures: sib; seeds: not recorded as a column or key in the result files
Table [phase2/x6/counting.json] (12 records):
  llama-3.2-1b | raw_fallback_used=false; native_ci_lower=0.38147410358565736; counted=false; english_above_chance_plus_5=true
  llama-3.2-1b.accuracy.english | n=1004; acc_cal=0.6334661354581673; ci95=[0.603585657370518, 0.6623505976095617]
  llama-3.2-1b.accuracy.itrans | n=1004; acc_cal=0.21314741035856574; ci95=[0.18824701195219123, 0.23904382470119523]
  llama-3.2-1b.accuracy.lossy | n=1004; acc_cal=0.2410358565737052; ci95=[0.2151394422310757, 0.2679282868525896]
  llama-3.2-1b.accuracy.lower | n=1004; acc_cal=0.18625498007968128; ci95=[0.16235059760956175, 0.21115537848605578]
  llama-3.2-1b.accuracy.native | n=1004; acc_cal=0.4123505976095618; ci95=[0.38147410358565736, 0.44322709163346613]
  oro-1.7b | raw_fallback_used=false; native_ci_lower=0.24900398406374502; counted=false; english_above_chance_plus_5=true
  oro-1.7b.accuracy.english | n=1004; acc_cal=0.3884462151394422; ci95=[0.35856573705179284, 0.41932270916334663]
  oro-1.7b.accuracy.itrans | n=1004; acc_cal=0.250996015936255; ci95=[0.2241035856573705, 0.2778884462151394]
  oro-1.7b.accuracy.lossy | n=1004; acc_cal=0.25199203187250996; ci95=[0.2241035856573705, 0.2788844621513944]
  oro-1.7b.accuracy.lower | n=1004; acc_cal=0.25; ci95=[0.22310756972111553, 0.27689243027888444]
  oro-1.7b.accuracy.native | n=1004; acc_cal=0.27689243027888444; ci95=[0.24900398406374502, 0.3047808764940239]
Result entry: 2026-11-05 03:38 IST, X6 COUNTING RESULT (rule 3; laptop; `scripts/x6_run.py`, `results/phase2/x6/counting.json`): neither shortlist model is counted. [RESULTS.md 3962-3963, `b9383db` 2026-11-05 03:38:22 +0530]
Source files: results/phase2/x6/counting.json

### X7: Tiny-GPT embedding accounting, factorized control, X7-A, X7b
Registered: X7. Tiny-GPT embedding accounting and a factorized-embedding control [RESULTS.md 3433-3436, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2
Table [phase2/x7/analysis.json] (9 records):
  (top) | n_runs=18; spearman_tokens_per_word_vs_bpb=-0.3714285714285715; spearman_p=0.4684781341107872; verdict="does not survive"; verdict_if_ddof0="does not survive"; phase1_embedding_params_range=[98688.0, 1573248.0]; control_embedding_params_range=[107030.0, 157850.0]; total_wall_hours=12.098382669024998; mdl_probes_on_control_models="not run yet (descriptive, separate step)"
  per_vocab[0] | vocab=256; bpb_mean=0.601669; bpb_sd_ddof1=0.00321; bpb_sd_ddof0=0.002621; n_seeds=3; embedding_params=157850; non_embedding_params=14162304; total_params=14320154; embedding_share=0.011023; tokens_per_word=5.013752; phase1_bpb_mean=0.59695; phase1_embedding_params=98688.0
  per_vocab[1] | vocab=384; bpb_mean=0.58064; bpb_sd_ddof1=0.001656; bpb_sd_ddof0=0.001353; n_seeds=3; embedding_params=147584; non_embedding_params=14162304; total_params=14309888; embedding_share=0.010313; tokens_per_word=2.535281; phase1_bpb_mean=0.569564; phase1_embedding_params=147840.0
  per_vocab[2] | vocab=512; bpb_mean=0.579868; bpb_sd_ddof1=0.002907; bpb_sd_ddof0=0.002374; n_seeds=3; embedding_params=140910; non_embedding_params=14162304; total_params=14303214; embedding_share=0.009852; tokens_per_word=2.079883; phase1_bpb_mean=0.560638; phase1_embedding_params=196992.0
  per_vocab[3] | vocab=768; bpb_mean=0.582687; bpb_sd_ddof1=0.00056; bpb_sd_ddof0=0.000457; n_seeds=3; embedding_params=130645; non_embedding_params=14162304; total_params=14292949; embedding_share=0.009141; tokens_per_word=1.735121; phase1_bpb_mean=0.551291; phase1_embedding_params=295296.0
  per_vocab[4] | vocab=1024; bpb_mean=0.587005; bpb_sd_ddof1=0.001226; bpb_sd_ddof0=0.001001; n_seeds=3; embedding_params=125510; non_embedding_params=14162304; total_params=14287814; embedding_share=0.008784; tokens_per_word=1.583769; phase1_bpb_mean=0.546011; phase1_embedding_params=393600.0
  per_vocab[5] | vocab=4096; bpb_mean=0.652979; bpb_sd_ddof1=0.002645; bpb_sd_ddof0=0.00216; n_seeds=3; embedding_params=107030; non_embedding_params=14162304; total_params=14269334; embedding_share=0.007501; tokens_per_word=1.265243; phase1_bpb_mean=0.528462; phase1_embedding_params=1573248.0
  decision.ddof1 | larger_sd=0.00320988189781573; diff_256_minus_4096=-0.051309914322210326; diff_over_sd=-15.984985104008297; exceeds_3sd=false
  decision.ddof0 | larger_sd=0.002620857594748344; diff_256_minus_4096=-0.051309914322210326; diff_over_sd=-19.577528525405107; exceeds_3sd=false
Table [phase2/x7a/analysis.json] (7 records):
  (top) | differences_256_minus_4096_by_seed=[1, 1, 1]; verdict="supported"
  detok_layer_by_vocab.256 | seeds=[2, 2, 2]; mean=2.0; phase1_seeds=[2, 2, 2]
  detok_layer_by_vocab.384 | seeds=[1, 1, 1]; mean=1.0; phase1_seeds=[1, 1, 1]
  detok_layer_by_vocab.512 | seeds=[1, 1, 1]; mean=1.0; phase1_seeds=[1, 1, 1]
  detok_layer_by_vocab.768 | seeds=[2, 2, 2]; mean=2.0; phase1_seeds=[1, 1, 1]
  detok_layer_by_vocab.1024 | seeds=[1, 1, 1]; mean=1.0; phase1_seeds=[1, 1, 1]
  detok_layer_by_vocab.4096 | seeds=[1, 1, 1]; mean=1.0; phase1_seeds=[0, 0, 0]
Result entry: 2026-11-04 01:44 IST, X7b DROPPED (the lead author): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md) [RESULTS.md 3858-3859, `3290232` 2026-11-04 01:44:01 +0530]
Source files: results/phase2/x7/analysis.json; results/phase2/x7a/analysis.json

### X8: Blind second-annotator sample
Registered: X8. Blind second-annotator sample (needs the lead author's annotators) [RESULTS.md 3437-3451, `a57fe61` 2026-11-01 20:14:53 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 8
Table [phase2/x8/analysis.json] (27 records):
  (top) | n_sentences=100; n_boot=10000; seed=0; K6="exploratory (retrieval and SIB-200 on the P, Q and Gemini texts): needs the GPU, not run here"
  descriptive_diagnostic_match_and_difference.gemini_vs_Q | exact_matches_case_insensitive=1; n=100; char_difference_mean=0.06431627045345188; char_difference_median=0.0630911070286453; q1=0.042272347535505427; q3=0.07992208077260755; min=0.0; max=0.16030534351145037; n_below_2_percent=6; n_zero=1
  descriptive_diagnostic_match_and_difference.gemini_vs_P | exact_matches_case_insensitive=1; n=100; char_difference_mean=0.10742861387835166; char_difference_median=0.10392734413352969; q1=0.07593478646110224; q3=0.13587662337662337; min=0.0; max=0.2647058823529412; n_below_2_percent=1; n_zero=1
  descriptive_diagnostic_match_and_difference.P_vs_Q | exact_matches_case_insensitive=0; n=100; char_difference_mean=0.09592943108665235; char_difference_median=0.08977140643161566; q1=0.06343376494023904; q3=0.12373588610702013; min=0.01818181818181818; max=0.2619047619047619; n_below_2_percent=2; n_zero=0
  descriptive_per_text.gemini | vowel_doubling_per_letter=0.015395273650989146; h_digraph_per_letter=0.014856439073204527; english_word_share=0.07874519846350832
  descriptive_per_text.P | vowel_doubling_per_letter=0.07416714531878231; h_digraph_per_letter=0.011200459506031017; english_word_share=0.010918432883750802
  descriptive_per_text.Q | vowel_doubling_per_letter=0.013278071993245837; h_digraph_per_letter=0.01112901987873206; english_word_share=0.10522999369880277
  descriptive_gemini_vs_each_annotator.gemini_vs_P.vowel_doubling | gemini_rate=0.015395273650989146; other_rate=0.07416714531878231; ratio=0.2075753837473154; ci90=[0.16544846247616235, 0.25259805369488353]; ci95=[0.1584774174586027, 0.2618311008937341]
  descriptive_gemini_vs_each_annotator.gemini_vs_P.h_digraph | gemini_rate=0.014856439073204527; other_rate=0.011200459506031017; ratio=1.326413355202517; ci90=[1.1203975326908893, 1.5525556155990279]; ci95=[1.0864973334721624, 1.604963919994337]
  descriptive_gemini_vs_each_annotator.gemini_vs_P.english_word_share | gemini_rate=0.07874519846350832; other_rate=0.010918432883750802; ratio=7.212133765157792; ci90=[5.227320501523107, 11.44481771399579]; ci95=[4.976650119976004, 12.8484225253872]
  descriptive_gemini_vs_each_annotator.gemini_vs_P.kappa_doubled_vowel | kappa=0.20726358610864182; ci95=[0.15578103211756503, 0.26590959639900075]; n_sentences_equal_word_count=90; n_sentences_other=10
  descriptive_gemini_vs_each_annotator.gemini_vs_P.cer | mean=0.10742861387835166; ci95=[0.09867669026644556, 0.11616121250743464]
  descriptive_gemini_vs_each_annotator.gemini_vs_Q.vowel_doubling | gemini_rate=0.015395273650989146; other_rate=0.013278071993245837; ratio=1.159450984963801; ci90=[0.9258314451903924, 1.433758781170359]; ci95=[0.8785924165340709, 1.4908450862483462]
  descriptive_gemini_vs_each_annotator.gemini_vs_Q.h_digraph | gemini_rate=0.014856439073204527; other_rate=0.01112901987873206; ratio=1.3349278943778053; ci90=[1.12288102489481, 1.5806204613775607]; ci95=[1.0919581436653454, 1.6350736842448863]
  descriptive_gemini_vs_each_annotator.gemini_vs_Q.english_word_share | gemini_rate=0.07874519846350832; other_rate=0.10522999369880277; ratio=0.748315149470585; ci90=[0.6738933280713023, 0.8237319711813409]; ci95=[0.6592001094098258, 0.8376926937841483]
  descriptive_gemini_vs_each_annotator.gemini_vs_Q.kappa_doubled_vowel | kappa=0.4180454149641636; ci95=[0.3361380451966284, 0.5014976179720111]; n_sentences_equal_word_count=71; n_sentences_other=29
  descriptive_gemini_vs_each_annotator.gemini_vs_Q.cer | mean=0.06431627045345188; ci95=[0.05801717421483584, 0.07071399502284151]
  K4_i_kappa | kappa=0.19807053642889777; ci95=[0.16105587822678788, 0.23846231018967673]; n_sentences_equal_word_count=75; n_sentences_other=25; n_words=1137; bootstrap_nan_share=0.0; status="primary outcome: the agreement itself, no threshold"
  K4_ii_cer | cer_mean=0.09592943108665235; ci95=[0.08755239789813977, 0.10462703065420798]; n_sentences=100; status="primary outcome: the agreement itself, no threshold"
  descriptive_K3b_statistics.vowel_doubling | gemini_rate=0.015395273650989146; human_rate_mean_of_P_Q=0.04372260865601407; rate_P=0.07416714531878231; rate_Q=0.013278071993245837; ratio_gemini_over_human=0.35211242247942853; ci90=[0.2816819033849112, 0.42646844491604335]; ci95=[0.27003622607204675, 0.443581490710693]; orientation_only_ci90_within_0.80_1.25=false; status="descriptive, no verdict"
  descriptive_K3b_statistics.h_digraph | gemini_rate=0.014856439073204527; human_rate_mean_of_P_Q=0.011164739692381537; rate_P=0.011200459506031017; rate_Q=0.01112901987873206; ratio_gemini_over_human=1.330657004331421; ci90=[1.1245927414417576, 1.5619430595046417]; ci95=[1.0933283631865318, 1.6124359743004586]; orientation_only_ci90_within_0.80_1.25=false; status="descriptive, no verdict"
  descriptive_K3b_statistics.english_word_share | gemini_rate=0.07874519846350832; human_rate_mean_of_P_Q=0.05807421329127679; rate_P=0.010918432883750802; rate_Q=0.10522999369880277; ratio_gemini_over_human=1.3559408556867438; ci90=[1.224165206908417, 1.4922657412842564]; ci95=[1.196571916431089, 1.5192259260108123]; orientation_only_ci90_within_0.80_1.25=false; status="descriptive, no verdict"
  K5 | vowel_doubling_rate_P=0.07416714531878231; vowel_doubling_rate_Q=0.013278071993245837
  K5.chrF_P_vs_Q | mean=80.54147793740317; ci95=[78.95398865248936, 82.08573653318535]; n=100
  K5.chrF_P_vs_Gemini | mean=77.72730446694051; ci95=[76.00608268265471, 79.45652323234376]; n=100
  K5.chrF_Q_vs_Gemini | mean=85.84695452611206; ci95=[84.47071474139435, 87.19239563124087]; n=100
  K5.vowel_doubling_ratio_P_over_Q | ratio=5.585686337331877; ci95=[4.839013785812079, 6.547121240356009]; status="descriptive"
Result entry: 2026-11-03 13:32 IST, X8 COMPLETE (decisions of the lead author; no registered rule changed). [RESULTS.md 3841-3843, `3529fe7` 2026-11-03 13:32:32 +0530]
Source files: results/phase2/x8/analysis.json

### X9a: Tiny GPT, familiarity manipulated, fragmentation fixed; X9a-low and extra seeds
Registered: X9a. Tiny GPT, familiarity manipulated, fragmentation fixed (laptop) [RESULTS.md 3531-3573, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2, 3, 4, 0.1, 1.0, 0.02, 0.04, 0.46, 0.024, 0.036, 0.052, 0.064, 0.068, 0.072, 0.112, 0.116, 0.172, 0.432, 0.988, 0.992, 0.996
Table [phase2/x9a/analysis.json] (21 records):
  (top) | n_runs=15; missing=[]; joint_reading="no familiarity effect in this setting (small model, letter cipher, no claim beyond that)"
  retrieval_by_level.0 | seeds=[0.024, 0.02, 0.04]; mean=0.027999999999999997
  retrieval_by_level.1 | seeds=[1.0, 0.992, 0.988]; mean=0.9933333333333333
  retrieval_by_level.5 | seeds=[1.0, 1.0, 1.0]; mean=1.0
  retrieval_by_level.20 | seeds=[1.0, 0.996, 1.0]; mean=0.9986666666666667
  retrieval_by_level.50 | seeds=[1.0, 1.0, 0.996]; mean=0.9986666666666667
  assembly_cipher_by_level.0 | seeds=[0, 0, 0]; mean=0.0
  assembly_cipher_by_level.1 | seeds=[2, 1, 1]; mean=1.3333333333333333
  assembly_cipher_by_level.5 | seeds=[1, 1, 1]; mean=1.0
  assembly_cipher_by_level.20 | seeds=[1, 1, 1]; mean=1.0
  assembly_cipher_by_level.50 | seeds=[1, 1, 1]; mean=1.0
  assembly_english_by_level.0 | seeds=[1, 1, 1]
  assembly_english_by_level.1 | seeds=[1, 1, 1]
  assembly_english_by_level.5 | seeds=[1, 1, 1]
  assembly_english_by_level.20 | seeds=[1, 1, 1]
  assembly_english_by_level.50 | seeds=[1, 1, 1]
  X9a_R | non_decreasing=false; mean50_minus_mean1=0.005333333333333412; 3x_larger_seed_sd=0.018330302779823376; spearman_level_vs_mean=0.316227766016838; verdict="refuted"
  X9a_R.means | 1=0.9933333333333333; 5=1.0; 20=0.9986666666666667; 50=0.9986666666666667
  X9a_A | seed_mean_detok_layer=[1.3333333333333333, 1.0, 1.0, 1.0]; max_minus_min=0.33333333333333326; verdict="supported"
  X9a_A.undefined_by_level | 1=0; 5=0; 20=0; 50=0
  level0_descriptive | retrieval_seeds=[0.024, 0.02, 0.04]; chance=0.004; assembly_cipher_seeds=[0, 0, 0]
Table [phase2/x9a/analysis_low.json] (13 records):
  (top) | n_runs=18; missing=[]
  retrieval_by_level.0.0 | seeds=[0.024, 0.02, 0.04]; mean=0.027999999999999997
  retrieval_by_level.0.01 | seeds=[0.036, 0.052, 0.04]; mean=0.042666666666666665
  retrieval_by_level.0.03 | seeds=[0.072, 0.068, 0.064]; mean=0.068
  retrieval_by_level.0.1 | seeds=[0.1, 0.116, 0.112]; mean=0.10933333333333334
  retrieval_by_level.0.3 | seeds=[0.432, 0.46, 0.172]; mean=0.3546666666666667
  retrieval_by_level.1.0 | seeds=[1.0, 0.992, 0.988]; mean=0.9933333333333333
  assembly_cipher_by_level.0.0 | seeds=[0, 0, 0]; mean=0.0
  assembly_cipher_by_level.0.01 | seeds=[0, 0, 0]; mean=0.0
  assembly_cipher_by_level.0.03 | seeds=[2, 1, 1]; mean=1.3333333333333333
  assembly_cipher_by_level.0.1 | seeds=[2, 1, 1]; mean=1.3333333333333333
  assembly_cipher_by_level.0.3 | seeds=[2, 1, 1]; mean=1.3333333333333333
  assembly_cipher_by_level.1.0 | seeds=[2, 1, 1]; mean=1.3333333333333333
Result entry: 2026-11-04 20:44 IST, X9a cipher token counts (descriptive; `results/phase2/x9a/cipher_tokens.json`, `scripts/x9a_cipher_tokens.py`). [RESULTS.md 3928-3928, `3c30aee` 2026-11-04 20:44:16 +0530]
Source files: results/phase2/x9a/analysis.json; results/phase2/x9a/analysis_low.json

### X9b: QLoRA continued pretraining (Sarvam-1 primary, Qwen3.5-2B secondary), extra seeds
Registered: X9b. Real models, QLoRA continued pretraining (memory pilot on the laptop; full runs on Kaggle) [RESULTS.md 3574-3611, `680151b` 2026-11-02 19:01:49 +0530]
Models run: sarvam-1, qwen3.5-2b
Forms/conditions run: itrans, native, english; tasks/measures: not recorded as a column or key in the result files; seeds: 0, 1, 2, 3, 9
Table [phase2/x9b/analysis_sarvam-1.json] (57 records):
  (top) | model="sarvam-1"; B=4997120
  measures.SIB-200 accuracy | n=1004; g0_before_training=0.23306772908366533; verdict="supported"
  measures.SIB-200 accuracy.g_after_seed_mean | itrans=0.11703187250996017; native=0.3416334661354582; english=0.31324701195219123
  measures.SIB-200 accuracy.g_after_by_seed | itrans=[0.11653386454183266, 0.11752988047808766]; native=[0.3386454183266932, 0.34462151394422313]; english=[0.31274900398406374, 0.3137450199203187]
  measures.SIB-200 accuracy.D_N | point=0.22460159362549803; ci975=[0.17729083665338644, 0.2729083665338645]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.22211155378486053, 0.22709163346613548]
  measures.SIB-200 accuracy.D_E | point=0.19621513944223107; ci975=[0.15039840637450197, 0.24402390438247012]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.19621513944223107, 0.19621513944223107]
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s0 | native=0.7659362549800797; itrans=0.649402390438247
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s1 | native=0.7669322709163346; itrans=0.649402390438247
  measures.SIB-200 accuracy.accuracy_by_run.native+s0 | native=0.7649402390438247; itrans=0.4262948207171315
  measures.SIB-200 accuracy.accuracy_by_run.native+s1 | native=0.7669322709163346; itrans=0.42231075697211157
  measures.SIB-200 accuracy.accuracy_by_run.english+s0 | native=0.7579681274900398; itrans=0.4452191235059761
  measures.SIB-200 accuracy.accuracy_by_run.english+s1 | native=0.7549800796812749; itrans=0.44123505976095617
  measures.SIB-200 accuracy.accuracy_base | native=0.7679282868525896; itrans=0.5348605577689243
  measures.FLORES+ retrieval | n=1005; g0_before_training=0.4338308457711443; verdict="supported"
  measures.FLORES+ retrieval.g_after_seed_mean | itrans=0.08059701492537313; native=0.417910447761194; english=0.4716417910447761
  measures.FLORES+ retrieval.g_after_by_seed | itrans=[0.08656716417910448, 0.07462686567164178]; native=[0.41492537313432837, 0.4208955223880597]; english=[0.46766169154228854, 0.47562189054726367]
  measures.FLORES+ retrieval.D_N | point=0.3373134328358209; ci975=[0.2955223880597015, 0.3781094527363184]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.3283582089552239, 0.34626865671641793]
  measures.FLORES+ retrieval.D_E | point=0.39104477611940297; ci975=[0.34427860696517415, 0.4348258706467662]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.38109452736318405, 0.4009950248756219]
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s0 | native=0.9263681592039801; itrans=0.8398009950248756
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s1 | native=0.9283582089552239; itrans=0.8537313432835821
  measures.FLORES+ retrieval.accuracy_by_run.native+s0 | native=0.9273631840796019; itrans=0.5124378109452736
  measures.FLORES+ retrieval.accuracy_by_run.native+s1 | native=0.9134328358208955; itrans=0.4925373134328358
  measures.FLORES+ retrieval.accuracy_by_run.english+s0 | native=0.9104477611940298; itrans=0.4427860696517413
  measures.FLORES+ retrieval.accuracy_by_run.english+s1 | native=0.9293532338308458; itrans=0.4537313432835821
  measures.FLORES+ retrieval.accuracy_base | native=0.9442786069651742; itrans=0.5104477611940299
  english_sib_damage_check | base=0.7679282868525896
  english_sib_damage_check.by_run.itrans+s0 | acc=0.75199203187251; drop_points=1.5936254980079667; flagged=false
  english_sib_damage_check.by_run.itrans+s1 | acc=0.75; drop_points=1.7928286852589626; flagged=false
  english_sib_damage_check.by_run.native+s0 | acc=0.7420318725099602; drop_points=2.589641434262946; flagged=false
  english_sib_damage_check.by_run.native+s1 | acc=0.7400398406374502; drop_points=2.7888446215139417; flagged=false
  english_sib_damage_check.by_run.english+s0 | acc=0.7171314741035857; drop_points=5.079681274900394; flagged=true
  english_sib_damage_check.by_run.english+s1 | acc=0.7151394422310757; drop_points=5.27888446215139; flagged=true
  tokenizer_unchanged | itrans+s0=true; itrans+s1=true; native+s0=true; native+s1=true; english+s0=true; english+s1=true
  per_run.itrans+s0 | condition="itrans"; seed=0; B_tokens=4997120; optimizer_steps=305; articles=1804; words=919137; stream_tokens=4997120; stream_tokens_per_word=5.436752083748124; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9093.610614538193
  per_run.itrans+s0.sib | english=0.75199203187251; native=0.7659362549800797; itrans=0.649402390438247
  per_run.itrans+s0.retrieval | native=0.9263681592039801; itrans=0.8398009950248756
  per_run.itrans+s1 | condition="itrans"; seed=1; B_tokens=4997120; optimizer_steps=305; articles=1804; words=919137; stream_tokens=4997120; stream_tokens_per_word=5.436752083748124; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9574.205170631409
  per_run.itrans+s1.sib | english=0.75; native=0.7669322709163346; itrans=0.649402390438247
  per_run.itrans+s1.retrieval | native=0.9283582089552239; itrans=0.8537313432835821
  per_run.native+s0 | condition="native"; seed=0; B_tokens=4997120; optimizer_steps=305; articles=3361; words=1797994; stream_tokens=4997120; stream_tokens_per_word=2.779275125500975; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9036.938798189163
  per_run.native+s0.sib | english=0.7420318725099602; native=0.7649402390438247; itrans=0.4262948207171315
  per_run.native+s0.retrieval | native=0.9273631840796019; itrans=0.5124378109452736
  per_run.native+s1 | condition="native"; seed=1; B_tokens=4997120; optimizer_steps=305; articles=3361; words=1797994; stream_tokens=4997120; stream_tokens_per_word=2.779275125500975; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9319.656382799149
  per_run.native+s1.sib | english=0.7400398406374502; native=0.7669322709163346; itrans=0.42231075697211157
  per_run.native+s1.retrieval | native=0.9134328358208955; itrans=0.4925373134328358
  per_run.english+s0 | condition="english"; seed=0; B_tokens=4997120; optimizer_steps=305; articles=3796; words=2696887; stream_tokens=4997120; stream_tokens_per_word=1.8529215350884185; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9504.01462316513
  per_run.english+s0.sib | english=0.7171314741035857; native=0.7579681274900398; itrans=0.4452191235059761
  per_run.english+s0.retrieval | native=0.9104477611940298; itrans=0.4427860696517413
  per_run.english+s1 | condition="english"; seed=1; B_tokens=4997120; optimizer_steps=305; articles=3796; words=2696887; stream_tokens=4997120; stream_tokens_per_word=1.8529215350884185; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9310.572784662247
  per_run.english+s1.sib | english=0.7151394422310757; native=0.7549800796812749; itrans=0.44123505976095617
  per_run.english+s1.retrieval | native=0.9293532338308458; itrans=0.4537313432835821
  tokens_per_word_flores | native=2.390675547098002; itrans=5.331303520456708
  english_regression_vs_base.itrans | mean_change_points=-1.693227091633466; ci95_points=[-3.386454183266932, 0.049800796812749]; flag_more_than_5_points=false; by_seed_points=[-1.593625498007968, -1.7928286852589643]
  english_regression_vs_base.native | mean_change_points=-2.689243027888446; ci95_points=[-4.780876494023905, -0.5976095617529881]; flag_more_than_5_points=false; by_seed_points=[-2.589641434262948, -2.788844621513944]
  english_regression_vs_base.english | mean_change_points=-5.179282868525896; ci95_points=[-7.071713147410359, -3.2856075697211335]; flag_more_than_5_points=true; by_seed_points=[-5.079681274900398, -5.278884462151394]
  itrans_trained_vs_original_native.SIB-200 accuracy | itrans_accuracy_after_itrans_training=0.649402390438247; original_native_accuracy_untrained=0.7679282868525896; difference=-0.11852589641434264; ci95=[-0.1508964143426295, -0.08665338645418327]; reaches_original_native_level=false
  itrans_trained_vs_original_native.FLORES+ retrieval | itrans_accuracy_after_itrans_training=0.8467661691542289; original_native_accuracy_untrained=0.9442786069651742; difference=-0.09751243781094528; ci95=[-0.11890547263681592, -0.07611940298507462]; reaches_original_native_level=false
Table [phase2/x9b/analysis_sarvam-1_seeds0123.json] (93 records):
  (top) | model="sarvam-1"; B=4997120
  measures.SIB-200 accuracy | n=1004; g0_before_training=0.23306772908366533; verdict="supported"
  measures.SIB-200 accuracy.g_after_seed_mean | itrans=0.11877490039840638; native=0.34063745019920316; english=0.3129980079681275
  measures.SIB-200 accuracy.g_after_by_seed | itrans=[0.11653386454183266, 0.11752988047808766, 0.12350597609561753, 0.11752988047808766]; native=[0.3386454183266932, 0.34462151394422313, 0.3426294820717131, 0.33665338645418325]; english=[0.31274900398406374, 0.3137450199203187, 0.3057768924302789, 0.3197211155378486]
  measures.SIB-200 accuracy.D_N | point=0.22186254980079678; ci975=[0.17430278884462153, 0.2699203187250996]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.22211155378486053, 0.22709163346613548, 0.2191235059760956, 0.2191235059760956]
  measures.SIB-200 accuracy.D_E | point=0.1942231075697211; ci975=[0.14741035856573706, 0.24302788844621512]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.19621513944223107, 0.19621513944223107, 0.18227091633466136, 0.20219123505976094]
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s0 | native=0.7659362549800797; itrans=0.649402390438247
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s1 | native=0.7669322709163346; itrans=0.649402390438247
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s2 | native=0.7639442231075697; itrans=0.6404382470119522
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s3 | native=0.7639442231075697; itrans=0.646414342629482
  measures.SIB-200 accuracy.accuracy_by_run.native+s0 | native=0.7649402390438247; itrans=0.4262948207171315
  measures.SIB-200 accuracy.accuracy_by_run.native+s1 | native=0.7669322709163346; itrans=0.42231075697211157
  measures.SIB-200 accuracy.accuracy_by_run.native+s2 | native=0.7649402390438247; itrans=0.42231075697211157
  measures.SIB-200 accuracy.accuracy_by_run.native+s3 | native=0.7679282868525896; itrans=0.4312749003984064
  measures.SIB-200 accuracy.accuracy_by_run.english+s0 | native=0.7579681274900398; itrans=0.4452191235059761
  measures.SIB-200 accuracy.accuracy_by_run.english+s1 | native=0.7549800796812749; itrans=0.44123505976095617
  measures.SIB-200 accuracy.accuracy_by_run.english+s2 | native=0.75199203187251; itrans=0.44621513944223107
  measures.SIB-200 accuracy.accuracy_by_run.english+s3 | native=0.7599601593625498; itrans=0.4402390438247012
  measures.SIB-200 accuracy.accuracy_base | native=0.7679282868525896; itrans=0.5348605577689243
  measures.FLORES+ retrieval | n=1005; g0_before_training=0.4338308457711443; verdict="supported"
  measures.FLORES+ retrieval.g_after_seed_mean | itrans=0.07537313432835821; native=0.41393034825870645; english=0.48084577114427857
  measures.FLORES+ retrieval.g_after_by_seed | itrans=[0.08656716417910448, 0.07462686567164178, 0.05870646766169154, 0.08159203980099503]; native=[0.41492537313432837, 0.4208955223880597, 0.4019900497512438, 0.417910447761194]; english=[0.46766169154228854, 0.47562189054726367, 0.4925373134328358, 0.48756218905472637]
  measures.FLORES+ retrieval.D_N | point=0.3385572139303482; ci975=[0.291542288557214, 0.3860696517412935]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.3283582089552239, 0.34626865671641793, 0.3432835820895523, 0.33631840796019896]
  measures.FLORES+ retrieval.D_E | point=0.4054726368159204; ci975=[0.35323383084577115, 0.4567164179104477]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.38109452736318405, 0.4009950248756219, 0.4338308457711443, 0.4059701492537313]
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s0 | native=0.9263681592039801; itrans=0.8398009950248756
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s1 | native=0.9283582089552239; itrans=0.8537313432835821
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s2 | native=0.9333333333333333; itrans=0.8746268656716418
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s3 | native=0.9293532338308458; itrans=0.8477611940298507
  measures.FLORES+ retrieval.accuracy_by_run.native+s0 | native=0.9273631840796019; itrans=0.5124378109452736
  measures.FLORES+ retrieval.accuracy_by_run.native+s1 | native=0.9134328358208955; itrans=0.4925373134328358
  measures.FLORES+ retrieval.accuracy_by_run.native+s2 | native=0.9213930348258706; itrans=0.5194029850746269
  measures.FLORES+ retrieval.accuracy_by_run.native+s3 | native=0.9283582089552239; itrans=0.5104477611940299
  measures.FLORES+ retrieval.accuracy_by_run.english+s0 | native=0.9104477611940298; itrans=0.4427860696517413
  measures.FLORES+ retrieval.accuracy_by_run.english+s1 | native=0.9293532338308458; itrans=0.4537313432835821
  measures.FLORES+ retrieval.accuracy_by_run.english+s2 | native=0.9273631840796019; itrans=0.43482587064676614
  measures.FLORES+ retrieval.accuracy_by_run.english+s3 | native=0.9253731343283582; itrans=0.43781094527363185
  measures.FLORES+ retrieval.accuracy_base | native=0.9442786069651742; itrans=0.5104477611940299
  english_sib_damage_check | base=0.7679282868525896
  english_sib_damage_check.by_run.itrans+s0 | acc=0.75199203187251; drop_points=1.5936254980079667; flagged=false
  english_sib_damage_check.by_run.itrans+s1 | acc=0.75; drop_points=1.7928286852589626; flagged=false
  english_sib_damage_check.by_run.itrans+s2 | acc=0.75199203187251; drop_points=1.5936254980079667; flagged=false
  english_sib_damage_check.by_run.itrans+s3 | acc=0.7539840637450199; drop_points=1.3944223107569709; flagged=false
  english_sib_damage_check.by_run.native+s0 | acc=0.7420318725099602; drop_points=2.589641434262946; flagged=false
  english_sib_damage_check.by_run.native+s1 | acc=0.7400398406374502; drop_points=2.7888446215139417; flagged=false
  english_sib_damage_check.by_run.native+s2 | acc=0.7470119521912351; drop_points=2.0916334661354563; flagged=false
  english_sib_damage_check.by_run.native+s3 | acc=0.7440239043824701; drop_points=2.39043824701195; flagged=false
  english_sib_damage_check.by_run.english+s0 | acc=0.7171314741035857; drop_points=5.079681274900394; flagged=true
  english_sib_damage_check.by_run.english+s1 | acc=0.7151394422310757; drop_points=5.27888446215139; flagged=true
  english_sib_damage_check.by_run.english+s2 | acc=0.7121513944223108; drop_points=5.5776892430278835; flagged=true
  english_sib_damage_check.by_run.english+s3 | acc=0.7141434262948207; drop_points=5.378486055776888; flagged=true
  tokenizer_unchanged | itrans+s0=true; itrans+s1=true; itrans+s2=true; itrans+s3=true; native+s0=true; native+s1=true; native+s2=true; native+s3=true; english+s0=true; english+s1=true; english+s2=true; english+s3=true
  per_run.itrans+s0 | condition="itrans"; seed=0; B_tokens=4997120; optimizer_steps=305; articles=1804; words=919137; stream_tokens=4997120; stream_tokens_per_word=5.436752083748124; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9093.610614538193
  per_run.itrans+s0.sib | english=0.75199203187251; native=0.7659362549800797; itrans=0.649402390438247
  per_run.itrans+s0.retrieval | native=0.9263681592039801; itrans=0.8398009950248756
  per_run.itrans+s1 | condition="itrans"; seed=1; B_tokens=4997120; optimizer_steps=305; articles=1804; words=919137; stream_tokens=4997120; stream_tokens_per_word=5.436752083748124; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9574.205170631409
  per_run.itrans+s1.sib | english=0.75; native=0.7669322709163346; itrans=0.649402390438247
  per_run.itrans+s1.retrieval | native=0.9283582089552239; itrans=0.8537313432835821
  per_run.itrans+s2 | condition="itrans"; seed=2; B_tokens=4997120; optimizer_steps=305; articles=1804; words=919137; stream_tokens=4997120; stream_tokens_per_word=5.436752083748124; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=8057.430752038956
  per_run.itrans+s2.sib | english=0.75199203187251; native=0.7639442231075697; itrans=0.6404382470119522
  per_run.itrans+s2.retrieval | native=0.9333333333333333; itrans=0.8746268656716418
  per_run.itrans+s3 | condition="itrans"; seed=3; B_tokens=4997120; optimizer_steps=305; articles=1804; words=919137; stream_tokens=4997120; stream_tokens_per_word=5.436752083748124; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=5583.4637134075165
  per_run.itrans+s3.sib | english=0.7539840637450199; native=0.7639442231075697; itrans=0.646414342629482
  per_run.itrans+s3.retrieval | native=0.9293532338308458; itrans=0.8477611940298507
  per_run.native+s0 | condition="native"; seed=0; B_tokens=4997120; optimizer_steps=305; articles=3361; words=1797994; stream_tokens=4997120; stream_tokens_per_word=2.779275125500975; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9036.938798189163
  per_run.native+s0.sib | english=0.7420318725099602; native=0.7649402390438247; itrans=0.4262948207171315
  per_run.native+s0.retrieval | native=0.9273631840796019; itrans=0.5124378109452736
  per_run.native+s1 | condition="native"; seed=1; B_tokens=4997120; optimizer_steps=305; articles=3361; words=1797994; stream_tokens=4997120; stream_tokens_per_word=2.779275125500975; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9319.656382799149
  per_run.native+s1.sib | english=0.7400398406374502; native=0.7669322709163346; itrans=0.42231075697211157
  per_run.native+s1.retrieval | native=0.9134328358208955; itrans=0.4925373134328358
  per_run.native+s2 | condition="native"; seed=2; B_tokens=4997120; optimizer_steps=305; articles=3361; words=1797994; stream_tokens=4997120; stream_tokens_per_word=2.779275125500975; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=5202.730954647064
  per_run.native+s2.sib | english=0.7470119521912351; native=0.7649402390438247; itrans=0.42231075697211157
  per_run.native+s2.retrieval | native=0.9213930348258706; itrans=0.5194029850746269
  per_run.native+s3 | condition="native"; seed=3; B_tokens=4997120; optimizer_steps=305; articles=3361; words=1797994; stream_tokens=4997120; stream_tokens_per_word=2.779275125500975; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=5538.169909477234
  per_run.native+s3.sib | english=0.7440239043824701; native=0.7679282868525896; itrans=0.4312749003984064
  per_run.native+s3.retrieval | native=0.9283582089552239; itrans=0.5104477611940299
  per_run.english+s0 | condition="english"; seed=0; B_tokens=4997120; optimizer_steps=305; articles=3796; words=2696887; stream_tokens=4997120; stream_tokens_per_word=1.8529215350884185; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9504.01462316513
  per_run.english+s0.sib | english=0.7171314741035857; native=0.7579681274900398; itrans=0.4452191235059761
  per_run.english+s0.retrieval | native=0.9104477611940298; itrans=0.4427860696517413
  per_run.english+s1 | condition="english"; seed=1; B_tokens=4997120; optimizer_steps=305; articles=3796; words=2696887; stream_tokens=4997120; stream_tokens_per_word=1.8529215350884185; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=9310.572784662247
  per_run.english+s1.sib | english=0.7151394422310757; native=0.7549800796812749; itrans=0.44123505976095617
  per_run.english+s1.retrieval | native=0.9293532338308458; itrans=0.4537313432835821
  per_run.english+s2 | condition="english"; seed=2; B_tokens=4997120; optimizer_steps=305; articles=3796; words=2696887; stream_tokens=4997120; stream_tokens_per_word=1.8529215350884185; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=5100.079291820526
  per_run.english+s2.sib | english=0.7121513944223108; native=0.75199203187251; itrans=0.44621513944223107
  per_run.english+s2.retrieval | native=0.9273631840796019; itrans=0.43482587064676614
  per_run.english+s3 | condition="english"; seed=3; B_tokens=4997120; optimizer_steps=305; articles=3796; words=2696887; stream_tokens=4997120; stream_tokens_per_word=1.8529215350884185; tokenizer_sha256_before="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_sha256_after="72e5ad0c2d3a65d199ffea57f14c01cb24bffb81d4600ecb68d6818613eb9baa"; tokenizer_unchanged=true; train_seconds=5685.73038482666
  per_run.english+s3.sib | english=0.7141434262948207; native=0.7599601593625498; itrans=0.4402390438247012
  per_run.english+s3.retrieval | native=0.9253731343283582; itrans=0.43781094527363185
  tokens_per_word_flores | native=2.390675547098002; itrans=5.331303520456708
  english_regression_vs_base.itrans | mean_change_points=-1.593625498007968; ci95_points=[-3.2619521912350598, 0.099601593625498]; flag_more_than_5_points=false; by_seed_points=[-1.593625498007968, -1.7928286852589643, -1.593625498007968, -1.394422310756972]
  english_regression_vs_base.native | mean_change_points=-2.4651394422310755; ci95_points=[-4.482071713147411, -0.4233067729083665]; flag_more_than_5_points=false; by_seed_points=[-2.589641434262948, -2.788844621513944, -2.091633466135458, -2.3904382470119523]
  english_regression_vs_base.english | mean_change_points=-5.328685258964144; ci95_points=[-7.270916334661355, -3.4113545816733066]; flag_more_than_5_points=true; by_seed_points=[-5.079681274900398, -5.278884462151394, -5.577689243027888, -5.378486055776892]
  itrans_trained_vs_original_native.SIB-200 accuracy | itrans_accuracy_after_itrans_training=0.646414342629482; original_native_accuracy_untrained=0.7679282868525896; difference=-0.12151394422310757; ci95=[-0.15338645418326693, -0.08989043824701196]; reaches_original_native_level=false
  itrans_trained_vs_original_native.FLORES+ retrieval | itrans_accuracy_after_itrans_training=0.8539800995024875; original_native_accuracy_untrained=0.9442786069651742; difference=-0.09029850746268657; ci95=[-0.11069651741293532, -0.0699004975124378]; reaches_original_native_level=false
Table [phase2/x9b/analysis_qwen3.5-2b.json] (39 records):
  (top) | model="qwen3.5-2b"; B=5668864
  measures.SIB-200 accuracy | n=1004; g0_before_training=0.4362549800796813; verdict="supported"
  measures.SIB-200 accuracy.g_after_seed_mean | itrans=0.17330677290836655; native=0.4581673306772908; english=0.43326693227091634
  measures.SIB-200 accuracy.g_after_by_seed | itrans=[0.17330677290836655]; native=[0.4581673306772908]; english=[0.43326693227091634]
  measures.SIB-200 accuracy.D_N | point=0.28486055776892427; ci975=[0.2410358565737052, 0.3276892430278885]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.28486055776892427]
  measures.SIB-200 accuracy.D_E | point=0.2599601593625498; ci975=[0.2191110557768924, 0.30079681274900394]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.2599601593625498]
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s0 | native=0.6872509960159362; itrans=0.5139442231075697
  measures.SIB-200 accuracy.accuracy_by_run.native+s0 | native=0.7081673306772909; itrans=0.25
  measures.SIB-200 accuracy.accuracy_by_run.english+s0 | native=0.6782868525896414; itrans=0.2450199203187251
  measures.SIB-200 accuracy.accuracy_base | native=0.6743027888446215; itrans=0.23804780876494025
  measures.FLORES+ retrieval | n=1005; g0_before_training=0.8577114427860697; verdict="supported"
  measures.FLORES+ retrieval.g_after_seed_mean | itrans=0.27860696517412936; native=0.8616915422885573; english=0.844776119402985
  measures.FLORES+ retrieval.g_after_by_seed | itrans=[0.27860696517412936]; native=[0.8616915422885573]; english=[0.844776119402985]
  measures.FLORES+ retrieval.D_N | point=0.583084577114428; ci975=[0.545273631840796, 0.6199004975124378]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.583084577114428]
  measures.FLORES+ retrieval.D_E | point=0.5661691542288556; ci975=[0.5293532338308458, 0.6029850746268657]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.5661691542288556]
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s0 | native=0.9751243781094527; itrans=0.6965174129353234
  measures.FLORES+ retrieval.accuracy_by_run.native+s0 | native=0.9900497512437811; itrans=0.12835820895522387
  measures.FLORES+ retrieval.accuracy_by_run.english+s0 | native=0.9830845771144279; itrans=0.1383084577114428
  measures.FLORES+ retrieval.accuracy_base | native=0.9771144278606965; itrans=0.11940298507462686
  english_sib_damage_check | base=0.8037848605577689
  english_sib_damage_check.by_run.itrans+s0 | acc=0.8017928286852589; drop_points=0.19920318725099584; flagged=false
  english_sib_damage_check.by_run.native+s0 | acc=0.797808764940239; drop_points=0.5976095617529875; flagged=false
  english_sib_damage_check.by_run.english+s0 | acc=0.7848605577689243; drop_points=1.8924302788844605; flagged=false
  tokenizer_unchanged | itrans+s0=true; native+s0=true; english+s0=true
  per_run.itrans+s0 | condition="itrans"; seed=0; B_tokens=5668864; optimizer_steps=346; articles=2505; words=1312877; stream_tokens=5668864; stream_tokens_per_word=4.317894212481443; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=9198.904323339462
  per_run.itrans+s0.sib | english=0.8017928286852589; native=0.6872509960159362; itrans=0.5139442231075697
  per_run.itrans+s0.retrieval | native=0.9751243781094527; itrans=0.6965174129353234
  per_run.native+s0 | condition="native"; seed=0; B_tokens=5668864; optimizer_steps=346; articles=1995; words=1040695; stream_tokens=5668864; stream_tokens_per_word=5.447190579372439; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=9104.594935417175
  per_run.native+s0.sib | english=0.797808764940239; native=0.7081673306772909; itrans=0.25
  per_run.native+s0.retrieval | native=0.9900497512437811; itrans=0.12835820895522387
  per_run.english+s0 | condition="english"; seed=0; B_tokens=5668864; optimizer_steps=346; articles=5376; words=3718950; stream_tokens=5668864; stream_tokens_per_word=1.5243184232108524; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=8946.590991020203
  per_run.english+s0.sib | english=0.7848605577689243; native=0.6782868525896414; itrans=0.2450199203187251
  per_run.english+s0.retrieval | native=0.9830845771144279; itrans=0.1383084577114428
  tokens_per_word_flores | native=5.328544243577546; itrans=4.195147478591817
  english_regression_vs_base.itrans | mean_change_points=-0.199203187250996; ci95_points=[-1.693227091633466, 1.1952191235059761]; flag_more_than_5_points=false; by_seed_points=[-0.199203187250996]
  english_regression_vs_base.native | mean_change_points=-0.5976095617529881; ci95_points=[-1.9920318725099602, 0.697211155378486]; flag_more_than_5_points=false; by_seed_points=[-0.5976095617529881]
  english_regression_vs_base.english | mean_change_points=-1.8924302788844622; ci95_points=[-3.5856573705179287, -0.199203187250996]; flag_more_than_5_points=false; by_seed_points=[-1.8924302788844622]
  itrans_trained_vs_original_native.SIB-200 accuracy | itrans_accuracy_after_itrans_training=0.5139442231075697; original_native_accuracy_untrained=0.6743027888446215; difference=-0.1603585657370518; ci95=[-0.19123505976095617, -0.1294820717131474]; reaches_original_native_level=false
  itrans_trained_vs_original_native.FLORES+ retrieval | itrans_accuracy_after_itrans_training=0.6965174129353234; original_native_accuracy_untrained=0.9771144278606965; difference=-0.28059701492537314; ci95=[-0.309452736318408, -0.2517412935323383]; reaches_original_native_level=false
Table [phase2/x9b/analysis_qwen3.5-2b_seeds012.json] (75 records):
  (top) | model="qwen3.5-2b"; B=5668864
  measures.SIB-200 accuracy | n=1004; g0_before_training=0.4362549800796813; verdict="supported"
  measures.SIB-200 accuracy.g_after_seed_mean | itrans=0.15803452855245684; native=0.4594953519256308; english=0.4163346613545817
  measures.SIB-200 accuracy.g_after_by_seed | itrans=[0.17330677290836655, 0.15239043824701196, 0.14840637450199204]; native=[0.4581673306772908, 0.45219123505976094, 0.4681274900398406]; english=[0.43326693227091634, 0.39243027888446214, 0.42330677290836655]
  measures.SIB-200 accuracy.D_N | point=0.3014608233731739; ci975=[0.24800796812749004, 0.35061005976095694]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.28486055776892427, 0.29980079681274896, 0.31972111553784854]
  measures.SIB-200 accuracy.D_E | point=0.2583001328021248; ci975=[0.1952191235059761, 0.3147410358565737]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.2599601593625498, 0.24003984063745018, 0.2749003984063745]
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s0 | native=0.6872509960159362; itrans=0.5139442231075697
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s1 | native=0.6384462151394422; itrans=0.4860557768924303
  measures.SIB-200 accuracy.accuracy_by_run.itrans+s2 | native=0.6872509960159362; itrans=0.5388446215139442
  measures.SIB-200 accuracy.accuracy_by_run.native+s0 | native=0.7081673306772909; itrans=0.25
  measures.SIB-200 accuracy.accuracy_by_run.native+s1 | native=0.7071713147410359; itrans=0.2549800796812749
  measures.SIB-200 accuracy.accuracy_by_run.native+s2 | native=0.7131474103585658; itrans=0.2450199203187251
  measures.SIB-200 accuracy.accuracy_by_run.english+s0 | native=0.6782868525896414; itrans=0.2450199203187251
  measures.SIB-200 accuracy.accuracy_by_run.english+s1 | native=0.6782868525896414; itrans=0.2858565737051793
  measures.SIB-200 accuracy.accuracy_by_run.english+s2 | native=0.6772908366533864; itrans=0.2539840637450199
  measures.SIB-200 accuracy.accuracy_base | native=0.6743027888446215; itrans=0.23804780876494025
  measures.FLORES+ retrieval | n=1005; g0_before_training=0.8577114427860697; verdict="supported"
  measures.FLORES+ retrieval.g_after_seed_mean | itrans=0.2646766169154229; native=0.8590381426202321; english=0.8570480928689883
  measures.FLORES+ retrieval.g_after_by_seed | itrans=[0.27860696517412936, 0.2527363184079602, 0.2626865671641791]; native=[0.8616915422885573, 0.8597014925373134, 0.8557213930348259]; english=[0.844776119402985, 0.8646766169154229, 0.8616915422885573]
  measures.FLORES+ retrieval.D_N | point=0.5943615257048093; ci975=[0.5502487562189056, 0.6368283582089559]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.583084577114428, 0.6069651741293532, 0.5930348258706468]
  measures.FLORES+ retrieval.D_E | point=0.5923714759535654; ci975=[0.5442786069651742, 0.6378109452736318]; above_0=true; entirely_below_0=false; seed_spread_D_seed0_seed1=[0.5661691542288556, 0.6119402985074627, 0.5990049751243782]
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s0 | native=0.9751243781094527; itrans=0.6965174129353234
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s1 | native=0.9771144278606965; itrans=0.7243781094527363
  measures.FLORES+ retrieval.accuracy_by_run.itrans+s2 | native=0.9771144278606965; itrans=0.7144278606965174
  measures.FLORES+ retrieval.accuracy_by_run.native+s0 | native=0.9900497512437811; itrans=0.12835820895522387
  measures.FLORES+ retrieval.accuracy_by_run.native+s1 | native=0.9900497512437811; itrans=0.13034825870646766
  measures.FLORES+ retrieval.accuracy_by_run.native+s2 | native=0.9900497512437811; itrans=0.13432835820895522
  measures.FLORES+ retrieval.accuracy_by_run.english+s0 | native=0.9830845771144279; itrans=0.1383084577114428
  measures.FLORES+ retrieval.accuracy_by_run.english+s1 | native=0.9850746268656716; itrans=0.12039800995024875
  measures.FLORES+ retrieval.accuracy_by_run.english+s2 | native=0.9870646766169154; itrans=0.1253731343283582
  measures.FLORES+ retrieval.accuracy_base | native=0.9771144278606965; itrans=0.11940298507462686
  english_sib_damage_check | base=0.8037848605577689
  english_sib_damage_check.by_run.itrans+s0 | acc=0.8017928286852589; drop_points=0.19920318725099584; flagged=false
  english_sib_damage_check.by_run.itrans+s1 | acc=0.8017928286852589; drop_points=0.19920318725099584; flagged=false
  english_sib_damage_check.by_run.itrans+s2 | acc=0.799800796812749; drop_points=0.3984063745019917; flagged=false
  english_sib_damage_check.by_run.native+s0 | acc=0.797808764940239; drop_points=0.5976095617529875; flagged=false
  english_sib_damage_check.by_run.native+s1 | acc=0.8027888446215139; drop_points=0.09960159362549792; flagged=false
  english_sib_damage_check.by_run.native+s2 | acc=0.796812749003984; drop_points=0.6972111553784854; flagged=false
  english_sib_damage_check.by_run.english+s0 | acc=0.7848605577689243; drop_points=1.8924302788844605; flagged=false
  english_sib_damage_check.by_run.english+s1 | acc=0.7768924302788844; drop_points=2.689243027888444; flagged=false
  english_sib_damage_check.by_run.english+s2 | acc=0.7768924302788844; drop_points=2.689243027888444; flagged=false
  tokenizer_unchanged | itrans+s0=true; itrans+s1=true; itrans+s2=true; native+s0=true; native+s1=true; native+s2=true; english+s0=true; english+s1=true; english+s2=true
  per_run.itrans+s0 | condition="itrans"; seed=0; B_tokens=5668864; optimizer_steps=346; articles=2505; words=1312877; stream_tokens=5668864; stream_tokens_per_word=4.317894212481443; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=9198.904323339462
  per_run.itrans+s0.sib | english=0.8017928286852589; native=0.6872509960159362; itrans=0.5139442231075697
  per_run.itrans+s0.retrieval | native=0.9751243781094527; itrans=0.6965174129353234
  per_run.itrans+s1 | condition="itrans"; seed=1; B_tokens=5668864; optimizer_steps=346; articles=2505; words=1312877; stream_tokens=5668864; stream_tokens_per_word=4.317894212481443; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=14325.945019245148
  per_run.itrans+s1.sib | english=0.8017928286852589; native=0.6384462151394422; itrans=0.4860557768924303
  per_run.itrans+s1.retrieval | native=0.9771144278606965; itrans=0.7243781094527363
  per_run.itrans+s2 | condition="itrans"; seed=2; B_tokens=5668864; optimizer_steps=346; articles=2505; words=1312877; stream_tokens=5668864; stream_tokens_per_word=4.317894212481443; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=6218.435968637466
  per_run.itrans+s2.sib | english=0.799800796812749; native=0.6872509960159362; itrans=0.5388446215139442
  per_run.itrans+s2.retrieval | native=0.9771144278606965; itrans=0.7144278606965174
  per_run.native+s0 | condition="native"; seed=0; B_tokens=5668864; optimizer_steps=346; articles=1995; words=1040695; stream_tokens=5668864; stream_tokens_per_word=5.447190579372439; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=9104.594935417175
  per_run.native+s0.sib | english=0.797808764940239; native=0.7081673306772909; itrans=0.25
  per_run.native+s0.retrieval | native=0.9900497512437811; itrans=0.12835820895522387
  per_run.native+s1 | condition="native"; seed=1; B_tokens=5668864; optimizer_steps=346; articles=1995; words=1040695; stream_tokens=5668864; stream_tokens_per_word=5.447190579372439; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=6026.591080188751
  per_run.native+s1.sib | english=0.8027888446215139; native=0.7071713147410359; itrans=0.2549800796812749
  per_run.native+s1.retrieval | native=0.9900497512437811; itrans=0.13034825870646766
  per_run.native+s2 | condition="native"; seed=2; B_tokens=5668864; optimizer_steps=346; articles=1995; words=1040695; stream_tokens=5668864; stream_tokens_per_word=5.447190579372439; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=6173.520985126495
  per_run.native+s2.sib | english=0.796812749003984; native=0.7131474103585658; itrans=0.2450199203187251
  per_run.native+s2.retrieval | native=0.9900497512437811; itrans=0.13432835820895522
  per_run.english+s0 | condition="english"; seed=0; B_tokens=5668864; optimizer_steps=346; articles=5376; words=3718950; stream_tokens=5668864; stream_tokens_per_word=1.5243184232108524; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=8946.590991020203
  per_run.english+s0.sib | english=0.7848605577689243; native=0.6782868525896414; itrans=0.2450199203187251
  per_run.english+s0.retrieval | native=0.9830845771144279; itrans=0.1383084577114428
  per_run.english+s1 | condition="english"; seed=1; B_tokens=5668864; optimizer_steps=346; articles=5376; words=3718950; stream_tokens=5668864; stream_tokens_per_word=1.5243184232108524; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=6082.838150501251
  per_run.english+s1.sib | english=0.7768924302788844; native=0.6782868525896414; itrans=0.2858565737051793
  per_run.english+s1.retrieval | native=0.9850746268656716; itrans=0.12039800995024875
  per_run.english+s2 | condition="english"; seed=2; B_tokens=5668864; optimizer_steps=346; articles=5376; words=3718950; stream_tokens=5668864; stream_tokens_per_word=1.5243184232108524; tokenizer_sha256_before="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_sha256_after="63c71e09abe4f3dd8136e921bae930667e07bb9aa16b81560a76a0d1be369ec1"; tokenizer_unchanged=true; train_seconds=6156.857125997543
  per_run.english+s2.sib | english=0.7768924302788844; native=0.6772908366533864; itrans=0.2539840637450199
  per_run.english+s2.retrieval | native=0.9870646766169154; itrans=0.1253731343283582
  tokens_per_word_flores | native=5.328544243577546; itrans=4.195147478591817
  english_regression_vs_base.itrans | mean_change_points=-0.2656042496679947; ci95_points=[-1.5604249667994687, 0.9628154050464809]; flag_more_than_5_points=false; by_seed_points=[-0.199203187250996, -0.199203187250996, -0.398406374501992]
  english_regression_vs_base.native | mean_change_points=-0.4648074369189906; ci95_points=[-1.693227091633466, 0.7304116865869853]; flag_more_than_5_points=false; by_seed_points=[-0.5976095617529881, -0.099601593625498, -0.697211155378486]
  english_regression_vs_base.english | mean_change_points=-2.4236387782204516; ci95_points=[-4.083665338645418, -0.796812749003984]; flag_more_than_5_points=false; by_seed_points=[-1.8924302788844622, -2.689243027888446, -2.689243027888446]
  itrans_trained_vs_original_native.SIB-200 accuracy | itrans_accuracy_after_itrans_training=0.5129482071713147; original_native_accuracy_untrained=0.6743027888446215; difference=-0.16135458167330677; ci95=[-0.18990703851261623, -0.13247011952191234]; reaches_original_native_level=false
  itrans_trained_vs_original_native.FLORES+ retrieval | itrans_accuracy_after_itrans_training=0.7117744610281923; original_native_accuracy_untrained=0.9771144278606965; difference=-0.2653399668325041; ci95=[-0.29187396351575456, -0.23980099502487562]; reaches_original_native_level=false
Result entry: 2026-11-06 11:53 IST, X9b PRIMARY ARM: EXTRA SEEDS FINISHED; RESULT WITH ALL FOUR SEEDS AND WITH THE ORIGINAL TWO (Sarvam-1; seeds 3 and 4 were ADDED AFTER SEEING SEEDS 1 AND 2, same QLoRA recipe, streams and budget, laptop; `x9b_ [RESULTS.md 4033-4033, `e605a65` 2026-11-06 11:53:24 +0530]
Source files: results/phase2/x9b/analysis_sarvam-1.json; results/phase2/x9b/analysis_sarvam-1_seeds0123.json; results/phase2/x9b/analysis_qwen3.5-2b.json; results/phase2/x9b/analysis_qwen3.5-2b_seeds012.json

### X10: Generation FLORES+ devtest to English (and post hoc, Sarvam-m)
Registered: X10. Generation: FLORES+ devtest to English (laptop pilot; laptop or Kaggle full) [RESULTS.md 3612-3623, `680151b` 2026-11-02 19:01:49 +0530]
Models run: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b
Forms/conditions run: lossy, lower, itrans, native, natural; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [phase2/x10/analysis.json] (37 records):
  contrasts[model=qwen3-1.7b] | model="qwen3-1.7b"; contrast="native - itrans"; n=1012; diff=26.44827439335156; ci95=[25.629326137797776, 27.25200599075477]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=qwen3-1.7b] | model="qwen3-1.7b"; contrast="native - lower"; n=1012; diff=25.80510643671627; ci95=[24.96249548080026, 26.647807384271786]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=qwen3-1.7b] | model="qwen3-1.7b"; contrast="native - lossy"; n=1012; diff=24.096581630985153; ci95=[23.2863699721278, 24.92023944637181]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=qwen3-1.7b] | model="qwen3-1.7b"; contrast="native - natural"; n=267; diff=21.80251964932438; ci95=[20.14227889792387, 23.43062819553147]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=qwen3.5-2b] | model="qwen3.5-2b"; contrast="native - itrans"; n=1012; diff=15.03107920523715; ci95=[13.601704607345603, 16.481224176909706]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=qwen3.5-2b] | model="qwen3.5-2b"; contrast="native - lower"; n=1012; diff=14.89478458511976; ci95=[13.464165628849717, 16.342061426354196]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=qwen3.5-2b] | model="qwen3.5-2b"; contrast="native - lossy"; n=1012; diff=14.89420072130378; ci95=[13.481858903142667, 16.33624975687795]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=qwen3.5-2b] | model="qwen3.5-2b"; contrast="native - natural"; n=267; diff=15.30637885850178; ci95=[12.348948940420728, 18.326440048143834]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=sarvam-1] | model="sarvam-1"; contrast="native - itrans"; n=1012; diff=21.011808535450207; ci95=[20.110761253070862, 21.913998922038722]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=sarvam-1] | model="sarvam-1"; contrast="native - lower"; n=1012; diff=22.34751620316676; ci95=[21.46344802480997, 23.251620738822794]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=sarvam-1] | model="sarvam-1"; contrast="native - lossy"; n=1012; diff=11.124578563366136; ci95=[10.325166443701416, 11.926503584491817]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=sarvam-1] | model="sarvam-1"; contrast="native - natural"; n=267; diff=9.680314575921786; ci95=[8.156872125651507, 11.216160923398865]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=gemma4-e2b] | model="gemma4-e2b"; contrast="native - itrans"; n=1012; diff=32.93908463815114; ci95=[32.10402380831005, 33.77503218694888]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=gemma4-e2b] | model="gemma4-e2b"; contrast="native - lower"; n=1012; diff=33.90147422323989; ci95=[33.013747983176806, 34.77724792764156]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=gemma4-e2b] | model="gemma4-e2b"; contrast="native - lossy"; n=1012; diff=28.938491628943254; ci95=[28.097516979756357, 29.79563716487]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  contrasts[model=gemma4-e2b] | model="gemma4-e2b"; contrast="native - natural"; n=267; diff=25.189588927284326; ci95=[23.651950039172352, 26.72236152624106]; p=0.00019998000199980003; p_holm=0.0031996800319968005; significant_positive=true
  corpus.qwen3-1.7b__native | corpus_chrf=39.32528311233748; empty_share=0.0; n=1012
  corpus.qwen3-1.7b__itrans | corpus_chrf=13.145973529897883; empty_share=0.0; n=1012
  corpus.qwen3-1.7b__lower | corpus_chrf=13.886892815175592; empty_share=0.0; n=1012
  corpus.qwen3-1.7b__lossy | corpus_chrf=15.285610436709815; empty_share=0.0; n=1012
  corpus.qwen3-1.7b__natural | corpus_chrf=17.788452520437605; empty_share=0.0; n=267
  corpus.qwen3.5-2b__native | corpus_chrf=19.982483176908186; empty_share=0.6175889328063241; n=1012
  corpus.qwen3.5-2b__itrans | corpus_chrf=2.484816524679512; empty_share=0.8646245059288538; n=1012
  corpus.qwen3.5-2b__lower | corpus_chrf=2.654168905126047; empty_share=0.8448616600790514; n=1012
  corpus.qwen3.5-2b__lossy | corpus_chrf=2.6694584801858117; empty_share=0.8794466403162056; n=1012
  corpus.qwen3.5-2b__natural | corpus_chrf=4.218964107508173; empty_share=0.8426966292134831; n=267
  corpus.sarvam-1__native | corpus_chrf=50.48300334976595; empty_share=0.0; n=1012
  corpus.sarvam-1__itrans | corpus_chrf=30.260968661162085; empty_share=0.0; n=1012
  corpus.sarvam-1__lower | corpus_chrf=28.824786177989136; empty_share=0.0; n=1012
  corpus.sarvam-1__lossy | corpus_chrf=39.85444843507945; empty_share=0.0; n=1012
  corpus.sarvam-1__natural | corpus_chrf=41.418717244729734; empty_share=0.0; n=267
  corpus.gemma4-e2b__native | corpus_chrf=54.858657077298; empty_share=0.0; n=1012
  corpus.gemma4-e2b__itrans | corpus_chrf=21.829928099629083; empty_share=0.018774703557312252; n=1012
  corpus.gemma4-e2b__lower | corpus_chrf=20.808773999825185; empty_share=0.023715415019762844; n=1012
  corpus.gemma4-e2b__lossy | corpus_chrf=26.339865205519036; empty_share=0.024703557312252964; n=1012
  corpus.gemma4-e2b__natural | corpus_chrf=30.23313028144836; empty_share=0.0149812734082397; n=267
  X10_P | models_native_beats_itrans_holm_significant=["qwen3-1.7b", "qwen3.5-2b", "sarvam-1", "gemma4-e2b"]; n_models=4; verdict="supported"
Result entry: 2026-11-08 21:37 IST, SARVAM-M X10, NATIVE FORM FINISHED (Kaggle account 3, `results/kaggle/acct3/kaggle_x10/2026-11-08T105332/out/sarvam-m/native.json`; generation only, no chrF computed yet). [RESULTS.md 4056-4057, `9b49dfa` 2026-11-08 21:37:42 +0530]
Source files: results/phase2/x10/analysis.json

### X11: Quantization control
Registered: X11. Quantization control (laptop) [RESULTS.md 3624-3633, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [phase2/x11/analysis.json] (14 records):
  (top) | n_items=1004; raw_fallback_4bit=false; raw_fallback_bf16=false; verdict="partly supported"
  forms.english | acc_4bit=0.7838645418326693; acc_bf16=0.8037848605577689; mcnemar_p=0.01045481832189218; only_4bit_correct=18; only_bf16_correct=38
  forms.english.change | diff=-0.0199203187250996; ci95=[-0.0348605577689243, -0.0049800796812749]
  forms.native | acc_4bit=0.6683266932270916; acc_bf16=0.6762948207171314; mcnemar_p=0.36629400670329104; only_4bit_correct=26; only_bf16_correct=34
  forms.native.change | diff=-0.00796812749003984; ci95=[-0.02390438247011952, 0.0069721115537848604]
  forms.itrans | acc_4bit=0.2589641434262948; acc_bf16=0.2410358565737052; mcnemar_p=0.16490698265644313; only_4bit_correct=84; only_bf16_correct=66
  forms.itrans.change | diff=0.017928286852589643; ci95=[-0.00597609561752988, 0.04183266932270916]
  forms.lower | acc_4bit=0.29880478087649404; acc_bf16=0.2958167330677291; mcnemar_p=0.8763306838960284; only_4bit_correct=84; only_bf16_correct=81
  forms.lower.change | diff=0.00298804780876494; ci95=[-0.021912350597609563, 0.027888446215139442]
  forms.lossy | acc_4bit=0.36254980079681276; acc_bf16=0.3754980079681275; mcnemar_p=0.2906878547807372; only_4bit_correct=58; only_bf16_correct=71
  forms.lossy.change | diff=-0.012948207171314742; ci95=[-0.035856573705179286, 0.008964143426294821]
  gap_native_minus_itrans | gap_4bit=0.40936254980079684; gap_bf16=0.4352589641434263
  gap_native_minus_itrans.change | diff=-0.025896414342629483; ci95=[-0.053784860557768925, 0.00298804780876494]
  rule_check | every_form_within_3_points=true; gap_change_ci_within_5_points=false; forms_changed_by_more_than_5_points_with_ci_excluding_0=[]
Result entry: 2026-11-04 12:07 IST, X11 ARM A RESULT (laptop, finished 12:00 IST): PARTLY SUPPORTED (registered rule; the prediction "quantization does not change the picture" is not fully met by the rule). [RESULTS.md 3902-3903, `bbc32e2` 2026-11-04 12:07:30 +0530]
Source files: results/phase2/x11/analysis.json

### X12: Ambari natural experiment
Registered: X12. Ambari natural experiment (Kaggle, 7B in fp16 sharded over 2 x T4) [RESULTS.md 3634-3655, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [phase2/x12/contrast1.json] (23 records):
  (top) | contrast="1: Llama-2-7B vs Ambari-7B-base-v0.1"; verdict="supported"
  sib | did=0.42330677290836655; ci975=[0.3804780876494024, 0.46613545816733065]; n=1004; above_0=true; below_0=false; gain_native=0.3894422310756972; gain_itrans=-0.033864541832669334
  sib.gain_by_form.english | gain=-0.13047808764940239; ci95=[-0.15836653386454183, -0.10258964143426295]; acc_ambari=0.5587649402390438; acc_llama2=0.6892430278884463
  sib.gain_by_form.native | gain=0.3894422310756972; ci95=[0.3555776892430279, 0.42330677290836655]; acc_ambari=0.5059760956175299; acc_llama2=0.11653386454183266
  sib.gain_by_form.itrans | gain=-0.03386454183266932; ci95=[-0.05179282868525897, -0.01593625498007968]; acc_ambari=0.10956175298804781; acc_llama2=0.14342629482071714
  sib.gain_by_form.lossy | gain=-0.08964143426294821; ci95=[-0.11752988047808766, -0.06274900398406374]; acc_ambari=0.19123505976095617; acc_llama2=0.28087649402390436
  sib_accuracy_by_form.ambari-7b-base | english=0.5587649402390438; native=0.5059760956175299; itrans=0.10956175298804781; lossy=0.19123505976095617
  sib_accuracy_by_form.llama-2-7b | english=0.6892430278884463; native=0.11653386454183266; itrans=0.14342629482071714; lossy=0.28087649402390436
  retrieval | did=0.6238805970149254; ci975=[0.5840796019900497, 0.663681592039801]; n=1005; above_0=true; below_0=false; gain_native=0.691542288557214; gain_itrans=0.06766169154228857
  retrieval.acc.ambari-7b-base | native=0.7432835820895523; itrans=0.14228855721393036
  retrieval.acc.llama-2-7b | native=0.051741293532338306; itrans=0.07462686567164178
  retrieval.gain_by_form.native | gain=0.6915422885572139; ci95=[0.6616915422885572, 0.7213930348258707]; acc_ambari=0.7432835820895523; acc_llama2=0.051741293532338306
  retrieval.gain_by_form.itrans | gain=0.06766169154228856; ci95=[0.050746268656716415, 0.08557213930348259]; acc_ambari=0.14228855721393036; acc_llama2=0.07462686567164178
  calibration.ambari-7b-base | raw_fallback_used=false
  calibration.llama-2-7b | raw_fallback_used=false
  a1p.ambari-7b-base | pass=true
  a1p.ambari-7b-base.forms.native | raw_agreement=1.0; acc_fp16=0.34; acc_ref=0.34; mean_abs_dlogprob=0.0031082376411982944; max_abs_dlogprob=0.014201164245605469; acc_diff=0.0; pass=true
  a1p.ambari-7b-base.forms.itrans | raw_agreement=1.0; acc_fp16=0.27; acc_ref=0.27; mean_abs_dlogprob=0.0032262577329363142; max_abs_dlogprob=0.01457357406616211; acc_diff=0.0; pass=true
  a1p.ambari-7b-base.forms.lossy | raw_agreement=1.0; acc_fp16=0.34; acc_ref=0.34; mean_abs_dlogprob=0.0030786706720079696; max_abs_dlogprob=0.012140274047851562; acc_diff=0.0; pass=true
  a1p.llama-2-7b | pass=true
  a1p.llama-2-7b.forms.native | raw_agreement=1.0; acc_fp16=0.21; acc_ref=0.21; mean_abs_dlogprob=0.002907275131770543; max_abs_dlogprob=0.015195846557617188; acc_diff=0.0; pass=true
  a1p.llama-2-7b.forms.itrans | raw_agreement=0.99; acc_fp16=0.28; acc_ref=0.28; mean_abs_dlogprob=0.003198042256491525; max_abs_dlogprob=0.013013839721679688; acc_diff=0.0; pass=true
  a1p.llama-2-7b.forms.lossy | raw_agreement=1.0; acc_fp16=0.36; acc_ref=0.36; mean_abs_dlogprob=0.0027376747131347655; max_abs_dlogprob=0.013242244720458984; acc_diff=0.0; pass=true
Table [phase2/x12/contrast2_mdl.json] (9 records):
  (top) | registered_form="native"; verdict_native="pattern met (more fragmented input assembled later)"
  models.ambari-7b-instruct-v0.1.native | detok_layer=4; tokens_per_word=1.6562222222222223; n_layers=32
  models.ambari-7b-instruct-v0.1.itrans | detok_layer=3; tokens_per_word=3.4233333333333333; n_layers=32
  models.ambari-7b-instruct-v0.2.native | detok_layer=8; tokens_per_word=14.506782299310652; n_layers=32
  models.ambari-7b-instruct-v0.2.itrans | detok_layer=3; tokens_per_word=3.493333333333333; n_layers=32
  occurrences.native | ambari-7b-instruct-v0.1=9000; ambari-7b-instruct-v0.2=8994; words_in_both=300
  occurrences.itrans | ambari-7b-instruct-v0.1=9000; ambari-7b-instruct-v0.2=9000; words_in_both=300
  contrast.native | v02_minus_v01_layer=4; ci95=[3.0, 5.0]; tokens_per_word_difference_v02_minus_v01=12.85056007708843; sign_ci=1; sign_expected_from_tpw=1; H3_pattern_met=true
  contrast.itrans | v02_minus_v01_layer=0; ci95=[0.0, 1.0]; tokens_per_word_difference_v02_minus_v01=0.06999999999999984; sign_ci=0; sign_expected_from_tpw=1; H3_pattern_met=false
Result entry: 2026-11-05 02:38 IST, X12 CONTRAST 2 RESULT (secondary; instruction-pair exposure contrast; MDL assembly layer, descriptive; Kaggle account 2 run, 1.50 h; `scripts/x12_contrast2.py`, `results/phase2/x12/contrast2_mdl.json`): the r [RESULTS.md 3956-3957, `ec3c085` 2026-11-05 02:38:48 +0530]
Source files: results/phase2/x12/contrast1.json; results/phase2/x12/contrast2_mdl.json

### X13: 7 to 9B and Sarvam-m models
Registered: X13. More 7-9B models on Kaggle [RESULTS.md 3656-3666, `680151b` 2026-11-02 19:01:49 +0530]
Models run: qwen3-8b, sarvam-1, sarvam-m, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, llama-3.1-8b
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: sib; seeds: not recorded as a column or key in the result files
Table [phase2/x13/qwen3-8b/analysis.json] (28 records):
  (top) | model="qwen3-8b"; dtype="float16 (A1-P passed: True)"; raw_fallback_used=false; english_accuracy_calibrated=0.8366533864541833
  accuracy.english | n=1004; acc_cal=0.8366533864541833; ci95=[0.8137450199203188, 0.8595617529880478]; acc_raw=0.8187250996015937
  accuracy.itrans | n=1004; acc_cal=0.45717131474103584; ci95=[0.4262948207171315, 0.48804780876494025]; acc_raw=0.37350597609561753
  accuracy.lossy | n=1004; acc_cal=0.5199203187250996; ci95=[0.48904382470119523, 0.5507968127490039]; acc_raw=0.41733067729083667
  accuracy.lower | n=1004; acc_cal=0.4103585657370518; ci95=[0.3804780876494024, 0.44123505976095617]; acc_raw=0.29282868525896416
  accuracy.native | n=1004; acc_cal=0.7788844621513944; ci95=[0.7529880478087649, 0.8047808764940239]; acc_raw=0.7320717131474104
  accuracy.natural257 | n=257; acc_cal=0.5291828793774319; ci95=[0.4669260700389105, 0.5875486381322957]; acc_raw=0.4396887159533074
  counted | native_ci_lower=0.7529880478087649; counted=true; informative_english_above_chance_plus_5=true
  P_a_this_model[model=qwen3-8b] | model="qwen3-8b"; task="sib"; a="native"; b="itrans"; acc_a=0.7788844621513944; acc_b=0.45717131474103584; n=1004; diff=0.32171314741035856; a_only=371; b_only=48; p=6.103209006153903e-63
  P_a_this_model[model=qwen3-8b] | model="qwen3-8b"; task="sib"; a="native"; b="lossy"; acc_a=0.7788844621513944; acc_b=0.5199203187250996; n=1004; diff=0.2589641434262948; a_only=311; b_only=51; p=1.2665686088107343e-46
  P_a_extended_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="itrans"; diff=0.3834661354581673; p=2.5188719631954495e-82; p_holm_extended=2.0150975705563596e-81; significant_extended=true
  P_a_extended_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="lossy"; diff=0.25298804780876494; p=2.668515711757834e-49; p_holm_extended=1.0674062847031336e-48; significant_extended=true
  P_a_extended_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="itrans"; diff=0.4322709163346613; p=1.2990189533010863e-106; p_holm_extended=1.2990189533010864e-105; significant_extended=true
  P_a_extended_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="lossy"; diff=0.36553784860557764; p=2.529451058538525e-82; p_holm_extended=2.0150975705563596e-81; significant_extended=true
  P_a_extended_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="itrans"; diff=0.43525896414342624; p=2.8113371589728562e-105; p_holm_extended=2.5302034430755707e-104; significant_extended=true
  P_a_extended_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="lossy"; diff=0.30079681274900394; p=1.1158511919563684e-59; p_holm_extended=5.579255959781843e-59; significant_extended=true
  P_a_extended_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="itrans"; diff=0.22709163346613548; p=2.123868442850549e-34; p_holm_extended=4.247736885701098e-34; significant_extended=true
  P_a_extended_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="lossy"; diff=0.06075697211155373; p=1.2058675268138053e-05; p_holm_extended=1.2058675268138053e-05; significant_extended=true
  P_a_extended_tests[model=qwen3-8b] | model="qwen3-8b"; a="native"; b="itrans"; diff=0.32171314741035856; p=6.103209006153903e-63; p_holm_extended=3.661925403692342e-62; significant_extended=true
  P_a_extended_tests[model=qwen3-8b] | model="qwen3-8b"; a="native"; b="lossy"; diff=0.2589641434262948; p=1.2665686088107343e-46; p_holm_extended=3.799705826432203e-46; significant_extended=true
  P_a_extended.native_vs_itrans | n_models=5; positive_and_significant=5; significantly_negative=0; verdict="supported"
  P_a_extended.native_vs_lossy | n_models=5; positive_and_significant=5; significantly_negative=0; verdict="supported"
  retrieval.qwen3-8b | native=0.5930348258706468; itrans=0.08557213930348259; diff=0.5074626865671642; ci95=[0.4736318407960199, 0.5402985074626866]; n=1005; layer_native=26; layer_itrans=5
  retrieval.qwen3.5-2b | native=0.9781094527363184; itrans=0.11343283582089553; diff=0.8646766169154229; ci95=[0.8427860696517413, 0.8855721393034826]; n=1005
  retrieval.sarvam-1 | native=0.9442786069651742; itrans=0.5144278606965174; diff=0.4298507462686567; ci95=[0.3990049751243781, 0.4616915422885572]; n=1005
  retrieval.gemma4-e2b | native=0.9950248756218906; itrans=0.26865671641791045; diff=0.7263681592039801; ci95=[0.699502487562189, 0.7542288557213931]; n=1005
  retrieval_extended | n_models=4; native_minus_itrans_ci_above_0=4; all_but_one_met=true
  scoring | hours=1.705509816010793; dir="results\\kaggle\\x_score\\2026-11-02T211301\\out\\qwen3-8b"
Table [phase2/x13/llama-3.1-8b/analysis.json] (28 records):
  (top) | model="llama-3.1-8b"; dtype="float16 (A1-P passed: True)"; raw_fallback_used=false; english_accuracy_calibrated=0.7848605577689243
  accuracy.english | n=1004; acc_cal=0.7848605577689243; ci95=[0.7589641434262948, 0.8107569721115537]; acc_raw=0.8087649402390438
  accuracy.itrans | n=1004; acc_cal=0.38247011952191234; ci95=[0.35258964143426297, 0.41334661354581675]; acc_raw=0.37749003984063745
  accuracy.lossy | n=1004; acc_cal=0.4631474103585657; ci95=[0.43326693227091634, 0.49404880478087615]; acc_raw=0.4701195219123506
  accuracy.lower | n=1004; acc_cal=0.3854581673306773; ci95=[0.3555776892430279, 0.4163346613545817]; acc_raw=0.4033864541832669
  accuracy.native | n=1004; acc_cal=0.7121513944223108; ci95=[0.6842629482071713, 0.7390438247011952]; acc_raw=0.7430278884462151
  accuracy.natural257 | n=257; acc_cal=0.5291828793774319; ci95=[0.4669260700389105, 0.5914396887159533]; acc_raw=0.5291828793774319
  counted | native_ci_lower=0.6842629482071713; counted=true; informative_english_above_chance_plus_5=true
  P_a_this_model[model=llama-3.1-8b] | model="llama-3.1-8b"; task="sib"; a="native"; b="itrans"; acc_a=0.7121513944223108; acc_b=0.38247011952191234; n=1004; diff=0.32968127490039845; a_only=392; b_only=61; p=3.059812743752219e-60
  P_a_this_model[model=llama-3.1-8b] | model="llama-3.1-8b"; task="sib"; a="native"; b="lossy"; acc_a=0.7121513944223108; acc_b=0.4631474103585657; n=1004; diff=0.24900398406374508; a_only=314; b_only=64; p=1.0181114460761287e-40
  P_a_extended_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="itrans"; diff=0.3834661354581673; p=2.5188719631954495e-82; p_holm_extended=2.0150975705563596e-81; significant_extended=true
  P_a_extended_tests[model=gemma4-e2b] | model="gemma4-e2b"; a="native"; b="lossy"; diff=0.25298804780876494; p=2.668515711757834e-49; p_holm_extended=1.0674062847031336e-48; significant_extended=true
  P_a_extended_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="itrans"; diff=0.4322709163346613; p=1.2990189533010863e-106; p_holm_extended=1.2990189533010864e-105; significant_extended=true
  P_a_extended_tests[model=qwen3-1.7b] | model="qwen3-1.7b"; a="native"; b="lossy"; diff=0.36553784860557764; p=2.529451058538525e-82; p_holm_extended=2.0150975705563596e-81; significant_extended=true
  P_a_extended_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="itrans"; diff=0.43525896414342624; p=2.8113371589728562e-105; p_holm_extended=2.5302034430755707e-104; significant_extended=true
  P_a_extended_tests[model=qwen3.5-2b] | model="qwen3.5-2b"; a="native"; b="lossy"; diff=0.30079681274900394; p=1.1158511919563684e-59; p_holm_extended=5.579255959781843e-59; significant_extended=true
  P_a_extended_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="itrans"; diff=0.22709163346613548; p=2.123868442850549e-34; p_holm_extended=4.247736885701098e-34; significant_extended=true
  P_a_extended_tests[model=sarvam-1] | model="sarvam-1"; a="native"; b="lossy"; diff=0.06075697211155373; p=1.2058675268138053e-05; p_holm_extended=1.2058675268138053e-05; significant_extended=true
  P_a_extended_tests[model=llama-3.1-8b] | model="llama-3.1-8b"; a="native"; b="itrans"; diff=0.32968127490039845; p=3.059812743752219e-60; p_holm_extended=1.8358876462513314e-59; significant_extended=true
  P_a_extended_tests[model=llama-3.1-8b] | model="llama-3.1-8b"; a="native"; b="lossy"; diff=0.24900398406374508; p=1.0181114460761287e-40; p_holm_extended=3.0543343382283862e-40; significant_extended=true
  P_a_extended.native_vs_itrans | n_models=5; positive_and_significant=5; significantly_negative=0; verdict="supported"
  P_a_extended.native_vs_lossy | n_models=5; positive_and_significant=5; significantly_negative=0; verdict="supported"
  retrieval.llama-3.1-8b | native=0.982089552238806; itrans=0.17313432835820897; diff=0.808955223880597; ci95=[0.7840796019900498, 0.8328606965174126]; n=1005; layer_native=17; layer_itrans=8
  retrieval.qwen3.5-2b | native=0.9781094527363184; itrans=0.11343283582089553; diff=0.8646766169154229; ci95=[0.8427860696517413, 0.8855721393034826]; n=1005
  retrieval.sarvam-1 | native=0.9442786069651742; itrans=0.5144278606965174; diff=0.4298507462686567; ci95=[0.3990049751243781, 0.4616915422885572]; n=1005
  retrieval.gemma4-e2b | native=0.9950248756218906; itrans=0.26865671641791045; diff=0.7263681592039801; ci95=[0.699502487562189, 0.7542288557213931]; n=1005
  retrieval_extended | n_models=4; native_minus_itrans_ci_above_0=4; all_but_one_met=true
  scoring | hours=1.8198573695951037; dir="results\\kaggle\\acct2\\x_score\\2026-11-04T210109\\out\\llama-3.1-8b"
Table [phase2/x13/sarvam-m/analysis.json] (36 records):
  (top) | model="sarvam-m"; quantization="4-bit NF4 (exempt from A1-P)"; forms_scored=[6 values]; forms_not_reached=[]; reason="first kernel (account 2) reached English, native, ITRANS before its 5 h cap; the second (account 3) scored lossy, lowercase, natural"; raw_fallback_used=false
  accuracy.english | n=1004; acc_cal=0.8396414342629482; ci95=[0.8167330677290837, 0.8615537848605578]; acc_raw=0.8406374501992032
  accuracy.itrans | n=1004; acc_cal=0.6822709163346613; ci95=[0.6533864541832669, 0.7101593625498008]; acc_raw=0.6752988047808764
  accuracy.lossy | n=1004; acc_cal=0.7320717131474104; ci95=[0.7051792828685259, 0.7599601593625498]; acc_raw=0.7300796812749004
  accuracy.lower | n=1004; acc_cal=0.6603585657370518; ci95=[0.6314741035856574, 0.6902390438247012]; acc_raw=0.6583665338645418
  accuracy.native | n=1004; acc_cal=0.8396414342629482; ci95=[0.8167330677290837, 0.8625498007968128]; acc_raw=0.8266932270916335
  accuracy.natural | n=257; acc_cal=0.7782101167315175; ci95=[0.7276264591439688, 0.8287937743190662]; acc_raw=0.7470817120622568
  counted | native_ci_lower=0.8167330677290837; counted=true
  native_minus_itrans | diff=0.15737051792828685; ci95=[0.1294820717131474, 0.1852589641434263]; n=1004; native_only_correct=196; itrans_only_correct=38; p_exact_mcnemar=7.645067691303307e-27
  native_minus_lossy | diff=0.10756972111553785; ci95=[0.08366533864541832, 0.13147410358565736]; n=1004; native_only_correct=137; form_only_correct=29; p_exact_mcnemar=5.4835683715181025e-18
  native_minus_lower | diff=0.17928286852589642; ci95=[0.14940239043824702, 0.20816733067729085]; n=1004; native_only_correct=219; form_only_correct=39; p_exact_mcnemar=1.4078488195734723e-31
  native_minus_natural | diff=0.04669260700389105; ci95=[0.0, 0.0933852140077821]; n=257; native_only_correct=24; form_only_correct=12; p_exact_mcnemar=0.06524533522315325
  extended_native_vs_itrans | n_models=7; positive_and_significant=7; verdict_all_but_one="supported"
  extended_native_vs_itrans.tests[model=gemma4-e2b] | model="gemma4-e2b"; diff=0.3834661354581673; p=2.5188719631954495e-82; p_holm=1.2594359815977248e-81; significant=true
  extended_native_vs_itrans.tests[model=qwen3-1.7b] | model="qwen3-1.7b"; diff=0.4322709163346613; p=1.2990189533010863e-106; p_holm=9.093132673107604e-106; significant=true
  extended_native_vs_itrans.tests[model=qwen3.5-2b] | model="qwen3.5-2b"; diff=0.43525896414342624; p=2.8113371589728562e-105; p_holm=1.6868022953837136e-104; significant=true
  extended_native_vs_itrans.tests[model=sarvam-1] | model="sarvam-1"; diff=0.22709163346613548; p=2.123868442850549e-34; p_holm=4.247736885701098e-34; significant=true
  extended_native_vs_itrans.tests[model=qwen3-8b] | model="qwen3-8b"; diff=0.32171314741035856; p=6.103209006153903e-63; p_holm=2.441283602461561e-62; significant=true
  extended_native_vs_itrans.tests[model=llama-3.1-8b] | model="llama-3.1-8b"; diff=0.32968127490039845; p=3.059812743752219e-60; p_holm=9.179438231256657e-60; significant=true
  extended_native_vs_itrans.tests[model=sarvam-m] | model="sarvam-m"; diff=0.15737051792828685; p=7.645067691303307e-27; p_holm=7.645067691303307e-27; significant=true
  P_a_extended_with_sarvam_m.tests[model=gemma4-e2b] | model="gemma4-e2b"; b="itrans"; diff=0.3834661354581673; p=2.5188719631954495e-82; p_holm_extended=3.0226463558345393e-81; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=gemma4-e2b] | model="gemma4-e2b"; b="lossy"; diff=0.25298804780876494; p=2.668515711757834e-49; p_holm_extended=1.8679609982304836e-48; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=qwen3-1.7b] | model="qwen3-1.7b"; b="itrans"; diff=0.4322709163346613; p=1.2990189533010863e-106; p_holm_extended=1.8186265346215207e-105; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=qwen3-1.7b] | model="qwen3-1.7b"; b="lossy"; diff=0.36553784860557764; p=2.529451058538525e-82; p_holm_extended=3.0226463558345393e-81; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=qwen3.5-2b] | model="qwen3.5-2b"; b="itrans"; diff=0.43525896414342624; p=2.8113371589728562e-105; p_holm_extended=3.654738306664713e-104; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=qwen3.5-2b] | model="qwen3.5-2b"; b="lossy"; diff=0.30079681274900394; p=1.1158511919563684e-59; p_holm_extended=8.926809535650948e-59; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=sarvam-1] | model="sarvam-1"; b="itrans"; diff=0.22709163346613548; p=2.123868442850549e-34; p_holm_extended=8.495473771402196e-34; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=sarvam-1] | model="sarvam-1"; b="lossy"; diff=0.06075697211155373; p=1.2058675268138053e-05; p_holm_extended=1.2058675268138053e-05; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=qwen3-8b] | model="qwen3-8b"; b="itrans"; diff=0.32171314741035856; p=6.103209006153903e-63; p_holm_extended=6.103209006153903e-62; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=qwen3-8b] | model="qwen3-8b"; b="lossy"; diff=0.2589641434262948; p=1.2665686088107343e-46; p_holm_extended=7.599411652864406e-46; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=llama-3.1-8b] | model="llama-3.1-8b"; b="itrans"; diff=0.32968127490039845; p=3.059812743752219e-60; p_holm_extended=2.753831469376997e-59; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=llama-3.1-8b] | model="llama-3.1-8b"; b="lossy"; diff=0.24900398406374508; p=1.0181114460761287e-40; p_holm_extended=5.090557230380643e-40; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=sarvam-m] | model="sarvam-m"; b="itrans"; diff=0.15737051792828685; p=7.645067691303307e-27; p_holm_extended=2.293520307390992e-26; significant_extended=true
  P_a_extended_with_sarvam_m.tests[model=sarvam-m] | model="sarvam-m"; b="lossy"; diff=0.10756972111553785; p=5.4835683715181025e-18; p_holm_extended=1.0967136743036205e-17; significant_extended=true
  P_a_extended_with_sarvam_m.result.native_vs_itrans | n_models=7; positive_and_significant=7; significantly_negative=0; verdict="supported"
  P_a_extended_with_sarvam_m.result.native_vs_lossy | n_models=7; positive_and_significant=7; significantly_negative=0; verdict="supported"
Note: results/phase2/PHASE2_INVENTORY.md (last changed 2026-11-05 22:15) still lists `X13 Sarvam-m: lossy, lowercase, natural forms and X10` as not run (quota); analysis.json here has forms_scored = six forms and forms_not_reached = [] (RESULTS.md 4049, 2026-11-08 15:33 IST entry: scored 2026-11-07 03:00 to 06:18 on account 3).
Result entry: 2026-11-08 15:33 IST, X13 SARVAM-M: ALL SIX FORMS SCORED; EXTENDED P-a WITH SARVAM-M (account 3, [third-account], 2026-11-07 03:00 to 06:18; `scripts/x13_sarvam_m.py`, `results/phase2/x13/sarvam-m/analysis.json`). [RESULTS.md 4049-4049, `0cd9a82` 2026-11-08 15:33:40 +0530]
Source files: results/phase2/x13/qwen3-8b/analysis.json; results/phase2/x13/llama-3.1-8b/analysis.json; results/phase2/x13/sarvam-m/analysis.json

### X14: Black-box hosted models
Registered: X14. Black-box hosted large models (exploratory, no verdict) [RESULTS.md 3667-3676, `680151b` 2026-11-02 19:01:49 +0530]
Models run: not recorded as a column or key in the result files
Forms/conditions run: not recorded as a column or key in the result files; tasks/measures: not recorded as a column or key in the result files; seeds: not recorded as a column or key in the result files
Table [phase2/x14/analysis.json] (24 records):
  allam-2-7b.acc.native | n=1004; acc=0.33665338645418325; ci95=[0.30776892430278885, 0.3665338645418327]
  allam-2-7b.acc.itrans | n=1004; acc=0.1902390438247012; ci95=[0.16633466135458166, 0.21414342629482072]
  allam-2-7b.acc.lossy | n=1004; acc=0.2539840637450199; ci95=[0.22709163346613545, 0.28087649402390436]
  allam-2-7b.acc.natural | n=257; acc=0.29571984435797666; ci95=[0.24124513618677043, 0.3540856031128405]
  allam-2-7b.gap_native_minus.itrans | n=1004; gap=0.14641434262948208; ci95=[0.1145418326693227, 0.17928286852589642]
  allam-2-7b.gap_native_minus.lossy | n=1004; gap=0.08266932270916334; ci95=[0.04880478087649402, 0.11653386454183266]
  allam-2-7b.gap_native_minus.natural | n=257; gap=0.07003891050583658; ci95=[0.0038910505836575876, 0.13618677042801555]
  allam-2-7b.unparsed_share | native=0.3545816733067729; itrans=0.5766932270916335; lossy=0.5617529880478087; natural=0.556420233463035
  openai__gpt-oss-120b.acc.native | n=1004; acc=0.8356573705179283; ci95=[0.8127490039840638, 0.8585657370517928]
  openai__gpt-oss-120b.acc.itrans | n=1004; acc=0.6245019920318725; ci95=[0.5946215139442231, 0.6543824701195219]
  openai__gpt-oss-120b.acc.lossy | n=1004; acc=0.6683266932270916; ci95=[0.6384462151394422, 0.6972111553784861]
  openai__gpt-oss-120b.acc.natural | n=257; acc=0.7003891050583657; ci95=[0.6459143968871596, 0.754863813229572]
  openai__gpt-oss-120b.gap_native_minus.itrans | n=1004; gap=0.21115537848605578; ci95=[0.18127490039840638, 0.2410358565737052]
  openai__gpt-oss-120b.gap_native_minus.lossy | n=1004; gap=0.16733067729083664; ci95=[0.1394422310756972, 0.19621513944223107]
  openai__gpt-oss-120b.gap_native_minus.natural | n=257; gap=0.16731517509727625; ci95=[0.11673151750972763, 0.2178988326848249]
  openai__gpt-oss-120b.unparsed_share | native=0.0; itrans=0.0; lossy=0.0; natural=0.0
  qwen__qwen3.8-27b.acc.native | n=1004; acc=0.8356573705179283; ci95=[0.8127490039840638, 0.8585657370517928]
  qwen__qwen3.8-27b.acc.itrans | n=1004; acc=0.6583665338645418; ci95=[0.6284860557768924, 0.6872509960159362]
  qwen__qwen3.8-27b.acc.lossy | n=1004; acc=0.6543824701195219; ci95=[0.6245019920318725, 0.6842629482071713]
  qwen__qwen3.8-27b.acc.natural | n=257; acc=0.6964980544747081; ci95=[0.6381322957198443, 0.7509727626459144]
  qwen__qwen3.8-27b.gap_native_minus.itrans | n=1004; gap=0.17729083665338646; ci95=[0.14741035856573706, 0.20717131474103587]
  qwen__qwen3.8-27b.gap_native_minus.lossy | n=1004; gap=0.18127490039840638; ci95=[0.15139442231075698, 0.2101593625498008]
  qwen__qwen3.8-27b.gap_native_minus.natural | n=257; gap=0.14396887159533073; ci95=[0.0933852140077821, 0.19455252918287938]
  qwen__qwen3.8-27b.unparsed_share | native=0.00099601593625498; itrans=0.0; lossy=0.00099601593625498; natural=0.0
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
Table [kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json] (9 records):
  (top) | gate_passed=false
  models.sarvam-1 | seconds=327.2035653591156; pass=false
  models.sarvam-1.nonfinite | english=0; native=0; itrans=0
  models.sarvam-1.forms.native | layer_kaggle=24; acc_kaggle=0.9442786069651742
  models.sarvam-1.forms.itrans | layer_kaggle=21; acc_kaggle=0.5104477611940299
  models.gemma4-e2b | seconds=587.7208812236786; pass=false
  models.gemma4-e2b.nonfinite | english=0; native=0; itrans=0
  models.gemma4-e2b.forms.native | layer_kaggle=7; acc_kaggle=0.9960199004975124
  models.gemma4-e2b.forms.itrans | layer_kaggle=7; acc_kaggle=0.2656716417910448
Table [kaggle/a1r_result.json] (7 records):
  (top) | gate_passed=true
  models.sarvam-1 | pass=true
  models.sarvam-1.native | kaggle_layer=24; laptop_layer=23; acc_kaggle=0.9442786069651742; acc_laptop=0.9442786069651742; abs_diff=0.0; kaggle_acc_at_laptop_layer=0.9412935323383085; max_abs_curve_diff_all_layers=0.00497512437810943; pass=true
  models.sarvam-1.itrans | kaggle_layer=21; laptop_layer=21; acc_kaggle=0.5104477611940299; acc_laptop=0.5144278606965174; abs_diff=0.003980099502487455; kaggle_acc_at_laptop_layer=0.5104477611940299; max_abs_curve_diff_all_layers=0.006965174129353213; pass=true
  models.gemma4-e2b | pass=true
  models.gemma4-e2b.native | kaggle_layer=7; laptop_layer=7; acc_kaggle=0.9960199004975124; acc_laptop=0.9950248756218906; abs_diff=0.0009950248756218638; kaggle_acc_at_laptop_layer=0.9960199004975124; max_abs_curve_diff_all_layers=0.006965174129353269; pass=true
  models.gemma4-e2b.itrans | kaggle_layer=7; laptop_layer=7; acc_kaggle=0.2656716417910448; acc_laptop=0.2686567164179104; abs_diff=0.0029850746268655914; kaggle_acc_at_laptop_layer=0.2656716417910448; max_abs_curve_diff_all_layers=0.004975124378109458; pass=true
Note (facts from the files and RESULTS.md 3712): gate_passed=false and models.*.pass=false in gate_retrieval.json are the in-kernel flags; the laptop reference file results/m4b_mapping/summary.csv was not in the Kaggle package, so the kernel had no reference to compare with. The registered comparison (tolerance 0.03) was run locally and is in results/kaggle/a1r_result.json (commit 43865a1, 2026-11-02 19:26:56 +0530): all four cells have pass=true; RESULTS.md 3712 logs it as `A1-R retrieval gate: PASSED`.
Result entry: 2026-11-02 19:26 IST, A1-R retrieval gate: PASSED. [RESULTS.md 3712-3712, `60b8183` 2026-11-02 23:21:28 +0530]
Source files: results/kaggle/kaggle_retrieval_gate/2026-11-02T133412/out/gate_retrieval.json; results/kaggle/a1r_result.json

## Failed, dropped and not run (one line each, as logged)

- 2026-10-08 | 2026-10-08 — E0 GATE (4 of 5 models; Gemma 4 E2B not run) [RESULTS.md 205-231, `22013f7`]
- 2026-10-21 | 2026-10-21 — Chain incident: the Kanglish chain and watcher ended during laptop sleep [RESULTS.md 1283-1300, `d7693f7`]
- 2026-10-26 | 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists) [RESULTS.md 2972-3002, `46bd82a`]
- 2026-10-26 | 2026-10-26 14:50 IST — K1/K2 pilot: first attempt failed on an id-type error (no computation; fixed, relaunched) [RESULTS.md 3105-3109, `5baf376`]
- 2026-10-28 | 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched [RESULTS.md 3178-3185, `126a488`]
- 2026-11-03 | 2026-11-03 07:43 IST, X9b rehearsal (Sarvam-1, ITRANS, seed 0, 20 optimizer steps, Kaggle T4, 0.19 h; `results/kaggle/kaggle_x9b/2026-11-03T015522/`): training, checkpoint and adapter saving worked; the merge into the fp16 base failed; rehearsal discarded as designed. [RESULTS.md 3820-3821, `bcaebe7`]
- 2026-11-03 | 2026-11-03 12:56 IST, X8 imported and analysed as registered (K4, K5; K6 not run). [RESULTS.md 3825-3828, `16e09e4`]
- 2026-11-04 | 2026-11-04 01:44 IST, X7b DROPPED (the lead author): considered, not run: with equal parameters the embedding rank is 114 at V = 256 and 24 at V = 4096, so the BPB rule would measure the bottleneck, not fragmentation (see docs/X7B_NOTE.md). [RESULTS.md 3858-3859, `3290232`]
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
- | X13 Sarvam-m: lossy, lowercase, natural forms and X10 | not run: Kaggle quota exhausted on both accounts (30 h cap); earliest push about 9 Nov (K1) or 11 Nov (K2) | K1, K2 | after quota rolls off | **SUPERSEDED by later entries:** lossy, lowercase and natural were scored 2026-11-07 03:00 to 06:18 on account 3 (RESULTS.md 4049; x13/sarvam-m/analysis.json forms_scored = six forms, forms_not_reached = []); X10 for Sarvam-m: pilot 2026-11-08 16:23, native finished 2026-11-08 21:37 (RESULTS.md 4056), ITRANS running, lossy, lowercase and natural not run by the decision of 2026-11-08 16:23 (RESULTS.md 4054).
- | X13 activation patching on one 7 to 9B model | registered as optional (only if it fits one 12 h session); not built | K1 or K2 | decision needed: leave dropped unless time allows |
- | X11 Arm B (one 4B-class model, descriptive, no verdict) | no 4B-class model was shortlisted by X6, so it cannot be formed | none | not run |
- | X7b | considered and not run (embedding rank argument; the lead author's decision) |
- | X15 (human intelligibility baseline) | annotators unavailable; skipped by decision |

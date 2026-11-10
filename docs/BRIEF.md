# Shattered Scripts: Implementation and Experiment Brief

(Verbatim copy of the brief from the lead author, 2026-10-07. Section 0 "Project memory" lives in `CLAUDE.md`.)

## 1. Environment and repo layout

### Setup
- Python 3.11+. Use uv or pip with a pinned requirements.txt.
- Core libraries: torch, transformers, accelerate, bitsandbytes (4-bit on T4), datasets, tokenizers, tiktoken,
  sentencepiece, indic_transliteration, aksharamukha, scikit-learn, scipy, statsmodels, pandas, pyarrow, matplotlib,
  seaborn, wordfreq, nnsight or transformer_lens (pick whichever supports the chosen models; nnsight is usually more
  flexible for arbitrary HF models), google-genai, anthropic, groq, openai (for OpenRouter's OpenAI-compatible
  endpoint), python-dotenv, tqdm, pyyaml.
- scripts/env_check.py prints: CPU, RAM, GPU (if any) and VRAM, disk, library versions, and which API keys are present
  in .env. Run it first.
- .env.example with: GEMINI_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY, ANTHROPIC_API_KEY (used only for the free token
  counting endpoint), HF_TOKEN. Never commit .env.

### Layout
```
shattered-scripts/
  CLAUDE.md                 project memory (section 0)
  README.md                 how to reproduce everything
  DATA_CARD.md              every dataset, source, license, split, size
  RESULTS.md                running log: one entry per experiment, prediction vs outcome
  requirements.txt
  .env.example
  configs/                  one YAML per experiment run; prices.yaml; models.yaml
  src/shattered/
    translit/               native<->ITRANS, controlled lossy scheme, natural romanization, round trip checks
    tok/                    tokenizer loaders (local + API counting), fertility metrics
    data/                   dataset loaders, item selection, parallel set builder, annotation export/import
    llm/                    API clients, rate limiter, response cache (sqlite), prompt templates, answer parsing
    eval/                   accuracy, F1, log likelihood scoring for open models
    interp/                 activation caching, probes, CKA, retrieval, head analysis, patching
    pretrain/               tiny GPT, BPE training, training loop, eval (BPB, minimal pairs, probes)
    romanize_opt/           scheme search, decoder, round trip verification
    stats/                  bootstrap, McNemar, Holm correction, mixed effects models
    plots/                  one function per paper figure
  scripts/                  e00_*.py ... e09_*.py, thin entry points calling src/
  notebooks/kaggle/         Kaggle-ready notebooks that pip install the repo and call scripts/
  data/raw|processed|annotation/
  results/eNN_<name>/       outputs, configs, logs per experiment
  paper/figures|tables/
```

### Shared infrastructure to build first
- **LLM client with cache.** Every API call keyed by sha256(provider, model, prompt, params), stored in sqlite.
  Re-running never re-calls the API. Token-bucket rate limiter per provider, exponential backoff. Temperature 0. Log
  provider-reported token usage.
- **Activation cache.** For open models, cache residual stream activations per layer for a given (model, input form,
  item) to .npy or .safetensors in float16 so probes and CKA never re-run the model.
- **Word alignment utility.** Given text and a tokenizer, return each whitespace word's token span using offset
  mappings. Must work for SentencePiece and byte-level BPE, including words that split mid UTF-8 character. Unit test
  on Kannada with known cases.
- **Transliteration module** (details in E2) with a round-trip test suite.

## 2. Experiments, in order

Rough schedule (part time, ~14 weeks): E0 week 1; E1 and E2 weeks 1–4; E3 weeks 3–6; E4 weeks 5–9; E5 weeks 6–10;
E6–E8 weeks 8–11; E9 weeks 9–12; writing weeks 12–14. E5 can start as soon as E0 is done (does not depend on Kannada).

### E0. Week 1 gate: can small open models understand Kannada at all?
Why: if the open models we can run do not understand Kannada, every interpretability result (E4) is meaningless. This
decides which models E4 uses.

Steps
- Search HF for current small instruct or base models in the 1B–9B range from the major families (Qwen, Gemma, Llama,
  others with strong multilingual claims), plus Indic-focused models (e.g. Sarvam 1, anything current from Sarvam or
  AI4Bharat). List candidates with parameter count, tokenizer type, vocab size, license, and whether they fit a T4
  (16 GB) in fp16 or 4-bit. Show the list before downloading anything over 5 GB.
- Data: Kannada and English test splits of IndicXNLI (3-way NLI, chance 33.3%) and IndicSentiment (verify labels and
  chance level). Sample 200 items per task, fixed seed. Verify availability and licenses first.
- Scoring for open models: log likelihood of each label verbalizer given an English instruction prompt (no free
  generation for small models). Instruction and label words in English for every input form; only content varies.
- Run each candidate on: English, native Kannada, ITRANS Kannada. Accuracy with 95% bootstrap CIs.
- Also compute each model's tokenizer fertility (tokens per word) on FLORES Kannada and English.

GATE: a model passes for E4 if native Kannada accuracy is ≥10 points above chance on at least one task AND English
accuracy is ≥15 points above chance on that task. Report a table of all candidates. If no model passes on CPU or a
single T4, report which larger models (4-bit on Kaggle 2x T4) might pass and expected run time. the lead author decides the E4
model set.

### E1. The language tax: token cost atlas
Prediction: Kannada, Telugu, Tamil, Malayalam cost ≥2x English tokens on most English-centric tokenizers; newer tokenizer
generations narrow the gap but do not close it. Failure: gap under 1.3x on current commercial tokenizers (report
honestly).

Steps
- Data: FLORES (current HF release, e.g. openlanguagedata/flores_plus), dev and devtest, for English, Kannada, Tamil,
  Telugu, Malayalam, Hindi, Bangla. All parallel.
- Input forms per Indic language: native, ITRANS, controlled lossy (from E2). Natural romanization for Kannada only.
- Tokenizers: local tiktoken r50k_base, p50k_base, cl100k_base, o200k_base; HF tokenizers of E0 candidate families
  including older and newer generations of the same family (drift). API (free counting endpoints, no generation):
  Anthropic token counting for each available Claude model; Gemini count_tokens for each available Gemini model. Cache
  everything.
- Metrics: tokens per sentence, tokens per word (fertility), ratio to English (the "tax"), bytes per token.
- Cost: configs/prices.yaml with per-million input and output prices per API model and USD→INR rate, each with date and
  source URL. Do not fill prices from memory; fetch and cite official pages or leave placeholders and ask. Report cost in
  rupees per 1,000 FLORES sentences per language, form and model.
- Outputs: results/e01_cost/ parquet tables; Figure F1 (tax ratio by language and tokenizer, grouped bars); Figure F1b
  (tax ratio across tokenizer generations, drift plot).

### E2. Building the parallel Kannada evaluation set
Goal: ~500 items, each in five forms: native, ITRANS, lossy, natural romanization, Kanglish. Plus English (from the
source dataset where parallel, otherwise via the dataset's English version).

Step 1: Transliteration module
- Native→ITRANS via indic_transliteration.sanscript. Check handling of Kannada-specific characters: short e/o vs long
  E/O, the Dravidian retroflex lateral, ZWJ/ZWNJ, nukta, Kannada digits, punctuation. Build ITRANS→native back
  conversion and round-trip test on all FLORES Kannada sentences. Target 100% exact round trip; if not, list failing
  characters and patch the mapping in our own wrapper. Report final round-trip rate.
- Controlled lossy scheme (deterministic, from ITRANS): collapse long vowels to short, retroflex to dental, aspirated to
  unaspirated, anusvara variants to m/n, then lowercase. Measure information loss as CER after best possible back
  conversion (map each lossy string back using the most frequent native source in a training corpus).
- Natural romanization: AI4Bharat IndicXlit native→roman if available, else a free-tier LLM with fixed prompt. Record
  which was used.
- Unit tests for all of the above.

Step 2: Item selection
- Sources: Kannada IndicXNLI and IndicSentiment test splits. Skip QA in the first version.
- Stratify by label, filter items with heavy English or digits, cap length. Target 250 NLI pairs + 250 sentiment items.
  Fixed seed. Disjoint from E0's 200-item samples.

Step 3: Kanglish drafting
- Free-tier LLM with fixed, versioned prompt: rewrite the Kannada item as a Bengaluru speaker would type it on WhatsApp,
  in Latin script, mixing English words where natural, keeping meaning and label unchanged. Cache outputs.
- Export to data/annotation/kanglish_batch_XX.csv with columns: id, native, kanglish_draft, kanglish_final (empty),
  naturalness_1to5 (empty), meaning_preserved_yn (empty), annotator, notes.
- Humans correct by hand. scripts/import_annotations.py validates filled CSVs (no empty finals, valid ratings) and
  merges.
- ~100 items rated independently by two annotators: Cohen's kappa for meaning_preserved, quadratic weighted kappa for
  naturalness.
- Code-mixing stats per item: fraction of English tokens (word-level LID via wordfreq with threshold), CMI.

Outputs: data/processed/parallel_set_v1.jsonl, dataset statistics table, kappa values, DATA_CARD.md entry.

### E3. Cost versus accuracy frontier
Predictions: (1) ITRANS loses little accuracy vs native on strong API models while cutting input tokens substantially.
(2) Controlled lossy loses clearly more than ITRANS ("lossiness, not romanization, causes the penalty"). (3) Kanglish sits
between native and lossy. Failure: ITRANS loses as much as lossy.

Steps
- Models: every free-tier API model available (Gemini free tier, Groq-hosted open models, OpenRouter free models; list
  and verify), plus E0-passing open models (log-likelihood scoring).
- Forms: English, native, ITRANS, lossy, natural, Kanglish.
- Prompts: fixed English instruction, item text in the given form, request to answer with exactly one English label.
  Templates in src/shattered/llm/templates/ with version ids. Zero-shot primary; 3-shot (examples in same form)
  secondary.
- Selective romanization (NLI): romanize premise only, keep hypothesis native, and vice versa.
- Answer parsing: strict label match after normalization. Invalid = wrong; report invalid rate per model and form.
- Metrics: accuracy, macro F1, input tokens, output tokens, rupees per 1,000 items, frontier metric: accuracy retained
  per rupee saved relative to native.
- Statistics: paired McNemar between forms per model, bootstrap 95% CIs on accuracy differences, Holm correction.
- Free-tier budgeting: compute total calls first, compare to each provider's current free limits, schedule across days.
  Show the plan before launching.

Outputs: Figure F2 (accuracy vs cost per model, one point per form, frontier highlighted); Table T2 (accuracy by model x
form with CIs); invalid-rate table.

### E4. Mechanism inside open models (interpretability)
Only E0-passing models. Use E2 items plus FLORES (parallel English). Use a larger Kannada sample (e.g. Kannada Wikipedia
on HF) where probes need many word occurrences. Rely on trained probes and representation similarity, not raw logit
lens. Transliteration is deterministic, so the same word has the same identity label in native, ITRANS and lossy forms.

E4a. Word assembly depth (probes)
- K most frequent Kannada words (K ~500–1000), ≥30 occurrences, multi-token in native script.
- Residual stream at the word's last token, every layer.
- Linear probe (logistic regression, L2, CV) per layer predicting word identity. Hold out occurrences, not words.
- Assembly depth = first layer where probe accuracy reaches 90% of that form's max. Also full curve.
- Second probe (Feucht-style erasure): at last token of a multi-token word, predict token at offset −1 and −2. Layer
  where this drops marks merging/erasure.
- Run for native, ITRANS, lossy, and English words of matched frequency.
- Controls: random-label probe (selectivity), layer-0 embedding probe.
- Prediction: native assembly depth later than ITRANS, later than or similar to English. Failure: no consistent ordering.

E4b. Alignment with English
- FLORES parallel sentences, mean-pool residual stream over content tokens per layer, per form and English.
- Linear CKA vs English per layer. Cross-lingual retrieval accuracy per layer (nearest English sentence by cosine).
- Prediction: native and lossy reach peak alignment later or lower than ITRANS.

E4c. Detokenization heads
- Per head: attention mass from a word's last token to earlier tokens of the same word, averaged over many words, per
  form. Rank heads; plot top-head distribution by layer per form.
- Validation: zero/mean-ablate top 5–10 heads; E4a probe accuracy at later layers should drop more than ablating random
  heads from the same layers.
- Prediction: native script recruits these heads across more and later layers.

E4d. Activation patching
- Items correct on ITRANS and wrong on native (or logit diff favors ITRANS). Cap ~150–200.
- Readout-position patching: patch final-position residual from ITRANS run into native run, one layer at a time.
- Word-aligned patching: for each word, patch residual at its last token from ITRANS into native's last token of same
  word, at layer L, all words at once.
- Metric: recovery = (patched − native) / (ITRANS − native) logit diff, per layer, bootstrap CIs.
- If compute is tight, ~6 evenly spaced layers first, then refine.
- Frame as cross-form patching, not clean vs corrupted.
- Prediction: word-aligned patching at early–middle layers recovers most of the gap; readout patching only at late layers.

Outputs: F3 (probe acc by layer per form), F4 (CKA and retrieval by layer), F5 (patching recovery by layer), head
analysis figure; all with CIs; per model.

### E5. Controlled pretraining: isolating fragmentation from data (MOST IMPORTANT)
Train tiny GPTs on the identical English corpus, changing only tokenizer vocab size.

Design
- Corpus: TinyStories (verify HF dataset and license). Hold out validation.
- Tokenizers: byte-level BPE trained on TinyStories train with vocab {256 (pure bytes), 512, 1k, 4k, 16k}. Optional:
  mismatched tokenizer trained on a different domain (general web text) at same size.
- Model: fixed non-embedding architecture across conditions, e.g. 8 layers, d_model 384, 6 heads. Report embedding
  params separately. If possible one condition with equalized embedding size (factorized embedding) as sensitivity check.
- Equalize text, not tokens: every condition sees the same number of training bytes. Context length per condition so
  each window covers ~same bytes (context_tokens ≈ target_context_bytes / bytes_per_token). Report FLOPs per condition.
- Seeds: 3 per condition.
- Pilot: 2 conditions, 1 seed, 10% budget. Measure wall time on Kaggle T4. Extrapolate. GATE: report estimate and grid.

Metrics
- Validation bits per byte.
- Assembly depth (E4a method) on frequent TinyStories words multi-token under smaller vocabs.
- Grammatical minimal pairs: BLiMP-style restricted to TinyStories vocab (filter BLiMP or templated pairs: subject-verb
  agreement, determiner-noun agreement, irregular past tense). Score by higher total log prob (per-byte normalization
  where relevant).
- Optional: downstream probe (story sentiment or character gender from a mid layer).

Predictions: as tokens/word increases, assembly depth later, BPB worse, minimal-pair accuracy lower, effect larger than
seed variance. Failure: no monotonic relationship, or effect disappears once compute equalized. Either is reportable.

Outputs: F6 (assembly depth, BPB, minimal-pair acc vs tokens/word, seed error bars); training curves; T6.

### E6. Frequency-matched English word pairs (observational)
- wordfreq pairs with |ΔZipf| < 0.1 and length within 1 char, but different token counts under a model's tokenizer
  (e.g. 1 vs ≥3).
- Natural contexts from a public corpus sample (FineWeb or Wikipedia on HF).
- Assembly depth (E4a) multi-token vs single-token partner. Explicitly observational.

### E7. Vocabulary expansion (optional, time-boxed to one week)
- Kaplan et al. 2024 finetuning-free expansion: new token per whole Kannada word, input embedding = model's hidden state
  at the word's last fragment from the layer where E4a shows assembly complete (try a few layers and scales).
- Replace fragment sequences in held-out sentences. Measure perplexity on remaining tokens, E2 task accuracy, assembly
  depth.
- Fallback: freeze model, train only new embedding rows on Kannada Wikipedia for a few hundred steps on free GPU.
- If neither helps in the time box, stop and report negative. Do not escalate compute.

### E8. Fragmentation curve across languages
- IndicXNLI across Indic languages + English. Per language and model: fertility (E1) and accuracy gap vs English.
- Mixed effects: gap ~ log(fertility), random intercept per model.
- Training-data proxy covariate per language (Wikipedia article count or published Common Crawl share; record source);
  report whether fertility still predicts gap. Say this only partially addresses the confound; E5 is the real answer.
- Add E3 within-Kannada points (native, ITRANS, lossy).
- Output: F7 (gap vs fertility, fitted line with CI).

### E9. Tokenizer-optimal reversible romanization (the fix)
Search
- Decompose Kannada into units: independent vowels, consonants, dependent vowel signs, virama, anusvara, visarga,
  specials.
- Per unit, candidate Latin spellings from ITRANS, Harvard-Kyoto, Velthuis, IAST ASCII variants, common natural spellings.
- Hard constraint: unambiguous decoding. Longest-match decoder; 100% exact round trip on a large Kannada sample. Reject
  failing schemes.
- Objective: total token count on a Kannada training corpus under a target tokenizer. Greedy coordinate descent over
  units with a few random restarts. Local tokenizers only (o200k_base and open-model tokenizers); never hammer API
  counters during search.
- One scheme per tokenizer family plus one "universal" scheme (average across tokenizers).

Evaluation
- Token savings on held-out FLORES Kannada vs native and vs ITRANS on every tokenizer, incl. API counters.
- Accuracy on E2 parallel set (E3 protocol), input only.
- Legend ablation: with vs without short scheme description in system prompt; measure net cost.
- Optional output-side test: free-text answers in the scheme; adherence and round-trip exactness.

Predictions: optimized scheme beats ITRANS by ≥10% tokens on target tokenizer with accuracy within ITRANS CI. Failure:
<5% savings over ITRANS. GATE: report savings before accuracy evaluation.

Outputs: F8 (token savings per tokenizer), T9 (accuracy and cost per scheme), scheme mapping tables, demo script.

## 3. Statistics and reporting standards
- Every accuracy: 95% bootstrap CI (10,000 resamples, item level).
- Paired comparisons: McNemar; Holm correction.
- Training experiments: 3 seeds, mean and sd, show individual seeds.
- Report n for every number.
- Figure functions in src/shattered/plots/, read only from results/, save PDF+PNG to paper/figures/. Colorblind-safe;
  never color alone.
- After each experiment append to RESULTS.md: date, id, config, commit hash, headline numbers, prediction, outcome,
  surprises, next step.

## 4. How to work with the lead author
- Start: env_check.py, repo skeleton and CLAUDE.md, shared infrastructure with tests, then E0. Do not jump ahead.
- At each GATE (E0 results, E5 pilot timing, E9 savings) stop with a short report: what ran, numbers, implications,
  recommended decision.
- When something is ambiguous (license, availability, free-tier limit), check and report rather than guess.
- When a result contradicts the thesis, say so plainly.
- Commit after each working milestone. Notebooks thin; logic in src/.
- Long Kaggle runs: resumable scripts (checkpoint every N steps, skip finished items via cache).

---

## Revision 2026-10-07 (the lead author): interpretability-first

**Dropped / changed**
- No Anthropic key, ever: Claude token counting is removed from E1 and stated as a limitation.
- E9 dropped (negative result in RESULTS.md). E7 dropped: FragMend (arXiv 2604.16656) already does Patchscopes
  detokenization and vocabulary expansion for non-Latin scripts.
- E3 shrinks to a small context table (accuracy and tokens by form for one or two free models). Kanglish is optional.
- E5 continues unchanged; afterwards M1 and M3 are applied to the tiny models.

**Models** (each with English, native Kannada and ITRANS forms):
- Qwen 2.5/3 family (identical tokenizer): Qwen3-1.7B; Qwen2.5-1.5B-Instruct also run in E0, better one kept.
- Qwen 3.5: Qwen3.5-2B.
- Gemma 4: gemma-4-E2B-it, the largest Gemma 4 that fits 8 GB in bf16 — text-only, per-layer embedding table
  (2.35B params) on CPU. E4B needs 9.3 GB GPU-resident.
- Sarvam-1 (base).
E0 runs first on these models (M2 and M6 need above-chance accuracy). Every M experiment is piloted on 50 items with a
time estimate before its full run.

**Shared data**: E0 items (IndicXNLI kn + IndicSentiment kn with parallel English), FLORES+ (kan/eng) for representation
analyses, Kannada Wikipedia (word inventory and probe contexts; ITRANS by deterministic transliteration, so word identity
is shared across native and ITRANS).

### M1. Detokenization layer per word (two methods)
- (a) **Patchscopes, replicating FragMend**: word encoded alone with BOS; last-token hidden state at every layer
  (embeddings = layer 0); patched into every placeholder of "X, X, X, X," at the input-embedding level; 20 greedy tokens;
  detokenization layer = first layer whose stripped output starts with the word and contains it with letter
  boundaries ("first_id_layer"). For ITRANS the target is the ITRANS spelling. Sensitivity: a language-labelled prompt
  and an in-context variant (state taken at the word's last token inside its sentence).
- (b) **Linear probes**: word-identity probe per layer on in-context occurrences (held-out occurrences); detokenization
  layer = first layer reaching 90% of the form's maximum probe accuracy; previous-token erasure probe as a second
  signal; random-label and layer-0 controls.
- Pre-registered competing predictions (written to RESULTS.md before running):
  fragmentation-driven = the native-vs-ITRANS ordering follows tokens per word and so flips across families (ITRANS
  earlier on Qwen 2.5/3 and Qwen 3.5; native earlier on Gemma 4 and Sarvam-1); script-driven = ITRANS earlier in all
  four models.

### M2. Item-level link
Within a model: does later detokenization predict wrong answers? Logistic regression of item correctness on the item's
detokenization lateness (mean and max over its words, from M1), controlling for word frequency (Kannada Wikipedia,
log), word length (characters) and token count; per model and form, plus a pooled model with form effects.

### M3. Circuits
Rank attention heads by within-word attention (mass from a word's last token to its earlier tokens) and MLP layers by
their contribution to detokenization (ablation effect on M1 signals). Ablate the top components vs random components
from the same layers; measure the change in detokenization (M1) and task accuracy (E0 scoring); compute the overlap
(Jaccard, rank correlation) of top components between native and ITRANS.

### M4. Alignment lag
Per form and layer: cross-lingual retrieval accuracy (FLORES+ sentence -> nearest English sentence by cosine of
mean-pooled residuals) and linear CKA with English. Alignment layer = first layer reaching 90% of the form's maximum
retrieval accuracy. Lag = alignment layer minus the form's detokenization layer (M1).

### M5. Latent English
Per form: the layer at which a word's English translation becomes decodable from its residual (logit lens on the
English target token, and a Patchscopes translation prompt). Requires a Kannada->English word list (source to be
verified and licensed before use).

### M6. Injection (stretch)
Inject each word's assembled representation (its state at the detokenization layer) at an early layer of the same run
at the word's last token, norm-matched to the original residual there; measure the accuracy change versus controls
(norm-matched representation of a different word; re-injecting the word's own early state).

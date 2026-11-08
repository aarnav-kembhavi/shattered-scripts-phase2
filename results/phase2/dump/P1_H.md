# H: Hindi: H-Hindi, H1, H1-LF, K3b-hi, English-loan measures (Phase 1)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| result | `d8e2bd8` | 2026-10-16 00:49:27 +0530 | 760-790 | 2026-10-16 — M4b linear mapping test (registered above): strong H1 inconclusive |
| post hoc, result | `83c256e` | 2026-10-22 17:55:12 +0530 | 1579-1614 | 2026-10-22 — Share of English words in natural, lossy and ITRANS (post hoc descriptive, 2026-10-22, no verdict) |
| post hoc, result | `5ec703c` | 2026-10-22 18:08:26 +0530 | 1689-1707 | 2026-10-22 — English-word share: sensitivity excluding words of ≤ 3 characters (post hoc descriptive, 2026-10-22, no verdict) |
| post hoc, result | `70fe375` | 2026-10-22 20:33:33 +0530 | 1794-1838 | 2026-10-22 — L3 on items with no English words in natural; net ITRANS → lossy on retrieval and SIB (post hoc descriptive, 2026-10-22, no verdict) |
| post hoc, result | `bb9fd5b` | 2026-10-23 00:34:32 +0530 | 2013-2038 | 2026-10-23 — Notes on NC-F and on the loan-free L3 subset (post hoc descriptive, 2026-10-23, no verdict; Aarnav) |
| registered | `dcf9cfe` | 2026-10-23 01:02:11 +0530 | 2113-2232 | PRE-REGISTRATION — Hindi natural romanization drafts and H-Hindi (written 2026-10-23 01:00 IST, Aarnav's design; before any Hindi draft or Hindi model output ex |
| registered | `176c284` | 2026-10-23 12:04:11 +0530 | 2233-2247 | PRE-REGISTRATION — K3b-hi: Gemini vs native-speaker natural romanization on Dakshina Hindi (written 2026-10-23 12:05 IST, Aarnav's design; before any Dakshina H |
| result | `5e44d59` | 2026-10-23 14:17:52 +0530 | 2248-2303 | 2026-10-23 — H-Hindi results (registered 01:00 IST + 12:05 IST addendum) |
| registered, result | `6fa02b3` | 2026-10-23 15:44:48 +0530 | 2304-2361 | PRE-REGISTRATION — H1-LF: H1 at equal English-loan content (written 2026-10-23 15:44 IST, Aarnav's design; FOLLOW-UP REGISTERED POST H1: written after the H1 re |
| result | `5064f46` | 2026-10-23 15:52:38 +0530 | 2362-2390 | 2026-10-23 — H1-LF option 2 results (follow-up registered post H1, 15:44 IST) |
| registered | `6867631` | 2026-10-23 16:00:59 +0530 | 2417-2435 | PRE-REGISTRATION — English-loan measure v2 (written 2026-10-23 16:00 IST, Aarnav's design; follows the 2026-10-23 diagnostic of the English-word measure; before |
| none | `7443e57` | 2026-10-23 16:12:55 +0530 | 2508-2515 | 2026-10-23 — English-loan measure v2: validity check (registered 16:00 IST) |
| post hoc, result | `0aec6a3` | 2026-10-23 21:17:49 +0530 | 2565-2572 | 2026-10-23 — Note on H1 and English loans after v2 (post hoc descriptive, dated, no verdict; Aarnav) |
| result, failed or not run | `46bd82a` | 2026-10-26 12:10:58 +0530 | 2972-3002 | 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists) |
| none | `46bd82a` | 2026-10-26 12:10:58 +0530 | 3003-3022 | 2026-10-26 12:10 IST — English-share tagger v2: checks (stopped; decision needed from Aarnav) |
| failed or not run | `126a488` | 2026-10-28 03:46:10 +0530 | 3178-3185 | 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched |
| none | `ca5c2e9` | 2026-10-28 05:39:02 +0530 | 3227-3233 | 2026-10-28 05:45 IST — H1-LF option 1: scoring finished (all 8 model x language loads); check script bug fixed |
| result | `ca5c2e9` | 2026-10-28 05:39:02 +0530 | 3234-3244 | 2026-10-28 06:05 IST — H1-LF option 1 results (registered 2026-10-23 15:44 IST; v2 loan definition primary because its validity check passed) |
| registered, exploratory | `9fbb738` | 2026-10-28 10:17:38 +0530 | 3245-3260 | 2026-10-28 06:20 IST — H1-LF selection check (exploratory; registered before running; CPU; Aarnav 2026-10-28) |
| exploratory, result | `9fbb738` | 2026-10-28 10:17:38 +0530 | 3261-3269 | 2026-10-28 06:50 IST — H1-LF selection check results (exploratory, no verdict; registered 06:20 IST; `scripts/h1lf_selection.py`) |

## Values observed in the result files (read from the files' own columns and keys)

- models: sarvam-1, gemma4-e2b, qwen3-1.7b, qwen3.5-2b, qwen2.5-1.5b, gemini-3.5-flash-lite
- languages: hindi
- forms: lossy, itrans, native, natural, natural1004
- tasks: sib, sentiment
- seeds: 0, 1, 6
- level: E
- measures: sib, en_words, has_name, kn_words, has_digit, kn_tokens, retrieval, sentiment

Result directories: `results/h_hindi`, `results/h1lf`, `results/k3b_hi`, `results/english_share`, `results/codemix_check`

## RESULTS.md entries, verbatim

##### 2026-10-16 — M4b linear mapping test (registered above): strong H1 inconclusive

RESULTS.md lines 760 to 790; first line committed in `d8e2bd8` on 2026-10-16 00:49:27 +0530; last line in `d8e2bd8` on 2026-10-16 00:49:27 +0530; labels from the title and parent heading: result

`````text
## 2026-10-16 — M4b linear mapping test (registered above): strong H1 inconclusive

Script `scripts/m4b_mapping.py` (CPU, about 30 min with other jobs running); outputs
`results/m4b_mapping/{summary.csv, verdict.json, items.npz}`. Pilot on Qwen2.5 first: 3.3 min per model, results
identical to the full run. Test half n = 1,005 (chance 0.1%). Best layers are chosen on the train half.

| model | native unmapped (layer) | native mapped (layer) | ITRANS unmapped (layer) | ITRANS mapped (layer) | mapped gap native − ITRANS [CI] | status |
|---|---|---|---|---|---|---|
| Qwen2.5 | 0.178 (15) | 0.517 (1) | 0.066 (1) | 0.529 (1) | −0.012 [−0.043, 0.019] | closes |
| Qwen3.5 | 0.978 (15) | 0.961 (7) | 0.113 (6) | 0.485 (3) | 0.477 [0.445, 0.509] | persists |
| Sarvam-1 | 0.944 (23) | 0.899 (26) | 0.514 (21) | 0.380 (24) | 0.518 [0.487, 0.551] | persists |
| Gemma 4 | 0.995 (7) | 0.977 (8) | 0.269 (7) | 0.473 (0) | 0.504 [0.473, 0.536] | persists |

Shuffled-pair control: 0.1–0.3% everywhere. Share of the unmapped gap remaining after mapping: Qwen3.5 55%,
Gemma 4 69%, Sarvam-1 121%, Qwen2.5 −11%.
- **Registered verdict: strong H1 inconclusive.** The gap persists in 3 of 4 models (Qwen3.5, Sarvam-1, Gemma 4) and
  closes in Qwen2.5. The rule needed all 4 for "supported" and 3 closing for "refuted".
- Qwen2.5 "closes" at a low level. Its native script is barely aligned with English either (unmapped 0.178). Both
  forms map best at layer 1, to the same ~0.52, so neither form reaches an English-aligned representation that
  ITRANS could fall short of.
- Mapping raises ITRANS above unmapped in Qwen2.5 (+0.46), Qwen3.5 (+0.37) and Gemma 4 (+0.20), and lowers it in
  Sarvam-1 (−0.13). With 1,004 training pairs in 1,536–2,304 dimensions, the ridge map is not an upper bound: it
  also lowers native retrieval wherever native is already aligned (Qwen3.5 −0.02, Sarvam-1 −0.05, Gemma 4 −0.02).
- Observation (post hoc, not a test): where mapped ITRANS does best, it does so at the input end. The best layer by
  train-half CV is 1 (Qwen2.5), 3 (Qwen3.5) and 0 (Gemma 4); in Sarvam-1 CV picked 24 (0.380), but the highest test
  value is at layer 0 (0.406). From a quarter of depth onward, mapped ITRANS is 0.06–0.39 (maximum 0.18 Qwen2.5, 0.34 Qwen3.5, 0.39 Sarvam-1, 0.28 Gemma 4). Mapped native peaks at layers
  7–26 (except Qwen2.5). A linear map at layers 0–3 over mean-pooled token vectors is largely a learned
  bag-of-tokens dictionary: shared digits, names and Latin-script loanwords in ITRANS give it lexical anchors.
  So the ITRANS gains look lexical, not like a recovered meaning representation. That reading fits strong H1 but
  is not what the registered rule tested.

`````

##### 2026-10-22 — Share of English words in natural, lossy and ITRANS (post hoc descriptive, 2026-10-22, no verdict)

RESULTS.md lines 1579 to 1614; first line committed in `83c256e` on 2026-10-22 17:55:12 +0530; last line in `e50581c` on 2026-10-22 18:06:53 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-22 — Share of English words in natural, lossy and ITRANS (post hoc descriptive, 2026-10-22, no verdict)
Requested by Aarnav. `scripts/english_share.py`, CPU only (text only, no model). Outputs
`results/english_share/{shares.csv, wordlist.json}` (commit 7129058 + this script).
- **Samples (matched):** the 496 retained M4c FLORES+ sentences; the 198 sentiment items with a clean natural
  romanization (2 of 200 are `natural_defective` and are dropped from every form).
- **Wordlist:** wordfreq 3.1.1 (Speer et al., https://github.com/rspeer/wordfreq), English "best" list. Primary:
  words with Zipf frequency ≥ 3 (29,269 words); sensitivity: Zipf ≥ 4 (7,223). A word (whitespace token, edge
  punctuation stripped, must contain an ASCII letter) is English if its lowercased form is in the list. ITRANS is also
  given "as written" (any uppercase letter = not English, since ITRANS uppercase marks Kannada phonemes).
- **Named entities:** no NE list exists in the repo, so proper nouns are approximated by capitalization in natural
  (capitalized, not sentence-initial). "No proper nouns" drops those words from natural and, best effort, drops the
  same lowercased word from lossy and ITRANS of that item.
- Share = English words / words, pooled; 95% CI from a paired bootstrap over items (10,000, seed 0).

| sample | wordlist | variant | natural | lossy | ITRANS | natural − lossy [95% CI] |
|---|---|---|---|---|---|---|
| M4c 496 | Zipf ≥ 3 | all words | 0.103 | 0.054 | 0.049 (as written 0.012) | +0.049 [+0.041, +0.057] |
| M4c 496 | Zipf ≥ 3 | no proper nouns | 0.096 | 0.051 | 0.046 | +0.045 [+0.037, +0.053] |
| M4c 496 | Zipf ≥ 4 | all words | 0.065 | 0.032 | 0.029 (as written 0.005) | +0.033 [+0.026, +0.041] |
| M4c 496 | Zipf ≥ 4 | no proper nouns | 0.060 | 0.030 | 0.027 | +0.030 [+0.023, +0.038] |
| sentiment 198 | Zipf ≥ 3 | all words | 0.110 | 0.041 | 0.038 (as written 0.007) | +0.068 [+0.057, +0.080] |
| sentiment 198 | Zipf ≥ 3 | no proper nouns | 0.108 | 0.041 | 0.038 | +0.067 [+0.055, +0.078] |
| sentiment 198 | Zipf ≥ 4 | all words | 0.065 | 0.024 | 0.021 (as written 0.003) | +0.041 [+0.031, +0.051] |
| sentiment 198 | Zipf ≥ 4 | no proper nouns | 0.064 | 0.024 | 0.021 | +0.040 [+0.029, +0.050] |

(Per-form CIs and natural − ITRANS are in `shares.csv`.)
- **Caveat, read before using the numbers:** lossy and ITRANS contain no deliberate English, so their share is a
  baseline of chance collisions between romanized Kannada and the English list (`i`, `a`, `ella`, `ne`, `ide`, `matte`).
  In natural on M4c, the largest contributors to the excess are Kannada words in natural spelling that happen to be in
  the list (`ee` = ಈ "this", 65; `na` 21; `aa` 19), not English loans; real loans and names appear lower down
  (`police`, `british`, `august`, `french`). On sentiment, real English loans contribute visibly (`air`, `collar`,
  `application`, `wifi`, `cooler`, `play`, `home`). Top-25 matched words per form are in `wordlist.json`. So the
  natural − lossy difference is an upper bound on "more English words", more so on M4c.
- **No verdict.** Nothing here tests or changes a registered prediction (L3 stays as registered).

---
`````

##### 2026-10-22 — English-word share: sensitivity excluding words of ≤ 3 characters (post hoc descriptive, 2026-10-22, no verdict)

RESULTS.md lines 1689 to 1707; first line committed in `5ec703c` on 2026-10-22 18:08:26 +0530; last line in `f676f15` on 2026-10-22 18:09:29 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-22 — English-word share: sensitivity excluding words of ≤ 3 characters (post hoc descriptive, 2026-10-22, no verdict)
Addendum to the English-share entry above (Aarnav's request). `scripts/english_share.py`, variant "words of 4+
characters": words of 3 characters or fewer are dropped from every form and from the denominator; Zipf ≥ 3 list; same
samples, bootstrap and seed (earlier rows of `results/english_share/shares.csv` reproduce exactly).

| sample | wordlist | variant | natural | lossy | ITRANS | natural − lossy [95% CI] |
|---|---|---|---|---|---|---|
| M4c 496 | Zipf ≥ 3 | words of 4+ characters | 0.071 | 0.022 | 0.018 | +0.049 [+0.042, +0.057] |
| sentiment 198 | Zipf ≥ 3 | words of 4+ characters | 0.084 | 0.018 | 0.015 | +0.066 [+0.054, +0.078] |

The difference is almost unchanged (+0.049 and +0.066 vs +0.049 and +0.068 with all words) while lossy's chance
baseline drops by more than half. In natural, the top matched 4+ character words are now mostly real English loans and
names (M4c: `police`, `british`, `august`, `french`, `website`, `internet`, `station`; sentiment: `collar`,
`application`, `wifi`, `cooler`, `bluetooth`), with some remaining collisions shared with lossy (`ella`, `matte`);
top-25 lists in `results/english_share/wordlist.json` (`top_matched_words_zipf3_4plus_chars`). This weakens the
earlier caveat that the M4c excess is mostly short Kannada words: those words inflate natural's share, but natural −
lossy survives their removal. No verdict.

---
`````

##### 2026-10-22 — L3 on items with no English words in natural; net ITRANS → lossy on retrieval and SIB (post hoc descriptive, 2026-10-22, no verdict)

RESULTS.md lines 1794 to 1838; first line committed in `70fe375` on 2026-10-22 20:33:33 +0530; last line in `a00f2ff` on 2026-10-22 23:16:03 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-22 — L3 on items with no English words in natural; net ITRANS → lossy on retrieval and SIB (post hoc descriptive, 2026-10-22, no verdict)
`scripts/l_ladder_posthoc.py` (CPU; stored ladder scores and cached vectors; retrieval per-item hits recomputed with
the ladder's procedure and asserted to reproduce `results/l_ladder/contrasts.csv` for L1, L2, L3 in every model).
Outputs `results/l_ladder_posthoc/{l3_no_english.csv, net_itrans_to_lossy_all.csv}`. McNemar p unadjusted; no test
is registered here; the registered L3 verdicts are unchanged.

**L3 (natural − lossy), full sample vs items whose natural text has no English word of 4+ characters** (wordfreq en,
Zipf ≥ 3, as the English-share entry). Difference [95% paired bootstrap CI]:

| measure | model | full: n, L3 | no-English subset: n, L3 |
|---|---|---|---|
| retrieval | Qwen3.5-2B | 248, +0.137 [+0.081, +0.194] | 130, +0.077 [+0.000, +0.154] |
| retrieval | Sarvam-1 | 248, +0.036 [+0.004, +0.069] | 130, +0.023 [−0.023, +0.069] |
| retrieval | Gemma 4 E2B | 248, +0.137 [+0.081, +0.198] | 130, +0.085 [+0.000, +0.169] |
| retrieval | Qwen2.5 (not counted) | 248, +0.177 [+0.129, +0.230] | 130, +0.062 [+0.015, +0.108] |
| sentiment | Qwen3-1.7B | 198, −0.005 [−0.076, +0.066] | 80, −0.025 [−0.150, +0.100] |
| sentiment | Qwen3.5-2B | 198, +0.040 [−0.025, +0.106] | 80, −0.013 [−0.100, +0.063] |
| sentiment | Sarvam-1 | 198, +0.000 [−0.040, +0.040] | 80, +0.025 [−0.038, +0.087] |
| sentiment | Gemma 4 E2B | 198, +0.015 [−0.035, +0.066] | 80, −0.037 [−0.112, +0.038] |
| sentiment | Qwen2.5 (not counted) | 198, +0.020 [−0.005, +0.051] | 80, −0.013 [−0.038, +0.000] |
| SIB-257 | Qwen3-1.7B | 257, +0.054 [+0.008, +0.101] | 132, +0.000 [−0.053, +0.053] |
| SIB-257 | Qwen3.5-2B | 257, +0.035 [−0.012, +0.086] | 132, +0.023 [−0.038, +0.083] |
| SIB-257 | Sarvam-1 | 257, +0.058 [+0.016, +0.105] | 132, +0.045 [−0.023, +0.114] |
| SIB-257 | Gemma 4 E2B | 257, +0.058 [+0.000, +0.117] | 132, +0.038 [−0.053, +0.129] |
| SIB-257 | Qwen2.5 (not counted) | 257, +0.074 [+0.019, +0.128] | 132, +0.023 [−0.038, +0.091] |

Descriptively: on items without English words, the retrieval L3 estimates are roughly half the full-sample ones in
every model, with CIs reaching 0 (n = 130); the subset is about half the sample and is not a random half (sentences
without loans or names may differ in other ways), so this neither confirms nor removes the registered L3 retrieval
effect.

**Net ITRANS → lossy (L1 + L2 = lossy − ITRANS)**, difference [95% paired bootstrap CI]:

| model | retrieval (248) | sentiment (200) | SIB-200 (1,004) |
|---|---|---|---|
| Qwen3-1.7B | — | +0.035 [−0.040, +0.105] | +0.067 [+0.041, +0.093] |
| Qwen3.5-2B | +0.185 [+0.121, +0.246] | +0.025 [−0.035, +0.090] | +0.134 [+0.107, +0.162] |
| Sarvam-1 | +0.198 [+0.141, +0.254] | +0.075 [+0.025, +0.125] | +0.166 [+0.134, +0.199] |
| Gemma 4 E2B | +0.129 [+0.065, +0.194] | +0.035 [−0.015, +0.085] | +0.130 [+0.100, +0.162] |
| Qwen2.5 (not counted) | +0.069 [+0.032, +0.109] | +0.005 [−0.020, +0.030] | +0.089 [+0.059, +0.119] |

Descriptively, lossy beats ITRANS on retrieval and SIB in every model; only on sentiment does the L1 loss mostly
cancel the L2 gain. No verdict.

---
`````

##### 2026-10-23 — Notes on NC-F and on the loan-free L3 subset (post hoc descriptive, 2026-10-23, no verdict; Aarnav)

RESULTS.md lines 2013 to 2038; first line committed in `bb9fd5b` on 2026-10-23 00:34:32 +0530; last line in `6105b0c` on 2026-10-23 00:51:18 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-23 — Notes on NC-F and on the loan-free L3 subset (post hoc descriptive, 2026-10-23, no verdict; Aarnav)
**NC-F's null is not interpretable as "no fragmentation cost at inference".** The registered verdict (NC-F refuted)
stands. But in the A2 item-level decomposition (2026-10-22, `results/nc1_posthoc/decomposition.csv`), extra pieces and
piece frequency correlate 0.59–0.73 across (b)/(c) items, and once frequency is included, extra pieces carry a negative
coefficient with a 95% CI excluding 0 (unadjusted) in Sarvam-1 retrieval (−0.0036 per piece), Sarvam-1 SIB (−0.015),
Gemma 4 SIB (−0.046) and Qwen3 sentiment (−0.028). NC1 compared more-but-more-frequent pieces (b) with
fewer-but-rarer pieces (c), so the two costs can offset in NC-F; NC1 does not separate them.

**The loan-free L3 subset differs in register.** `scripts/l3_loanfree_register.py`, output
`results/l_ladder_posthoc/l3_loanfree_register.csv`. Named-entity proxy: capitalized words that are not
sentence-initial (English source; the natural romanizations are mostly lowercase, so their count is near 0).

| sample | group | n | native words | natural words | caps (English) | items with ≥ 1 (English) | caps (natural) |
|---|---|---|---|---|---|---|---|
| retrieval (M4c test half) | loan-free | 130 | 14.7 | 14.7 | 0.95 | 40% | 0.10 |
| | other | 118 | 17.3 | 17.7 | 2.72 | 75% | 0.34 |
| sentiment (198) | loan-free | 80 | 12.8 | 12.8 | 0.41 | 22% | 0.10 |
| | other | 118 | 19.9 | 19.9 | 0.81 | 37% | 0.06 |
| SIB-257 | loan-free | 132 | 14.8 | 14.8 | 0.89 | 41% | 0.12 |
| | other | 125 | 17.0 | 17.1 | 2.72 | 72% | 0.42 |

Loan-free items are shorter (2–7 native words) and carry about a third as many named entities (English side) on
retrieval and SIB. The smaller loan-free L3 estimates may therefore reflect fewer names and shorter sentences as much
as the absence of English loans; the subset analysis cannot separate these.

---
`````

##### PRE-REGISTRATION — Hindi natural romanization drafts and H-Hindi (written 2026-10-23 01:00 IST, Aarnav's design; before any Hindi draft or Hindi model output exists)

RESULTS.md lines 2113 to 2232; first line committed in `dcf9cfe` on 2026-10-23 01:02:11 +0530; last line in `176c284` on 2026-10-23 12:04:11 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — Hindi natural romanization drafts and H-Hindi (written 2026-10-23 01:00 IST, Aarnav's design; before any Hindi draft or Hindi model output exists)
Scripts: `scripts/h_hindi.py` (written after this registration), chains `scripts/h_drafts_chain.sh` (Gemini, then
K3b) and `scripts/h_gpu_chain.sh` (GPU). Outputs in `results/h_hindi/`.

### Data (checked 2026-10-23 before registration; no model run)
- **FLORES+ `hin_Deva` dev + devtest:** 2,009 sentences, the same indices as Kannada.
- **IndicSentiment `data/test/hi.json`** (revision dc8f3f66886531c6897fedffca1e938a68fc5013): 1,000 rows, row-aligned
  with `kn.json`. English review and label are identical in all 1,000 rows, so the ids `indicsentiment-test-{row}` are
  shared.
- **SIB-200 `hin_Deva`** (same revision as Kannada): 1,004 items, the same index ids and topic labels. Native text is
  taken from FLORES+ by index, as for Kannada (SIB's own Hindi text equals FLORES+ in 917 of 1,004).
- **Items:**
  - the 200 Kannada E0 sentiment ids;
  - SIB 1,004;
  - the M4c rows: the same 500 FLORES indices, 496 retained by the Kannada mask.

### Forms
- **native:** Devanagari, NFC.
- **ITRANS (lossless):** the project's ITRANS scheme generated for Devanagari (`itrans_for(SCRIPTS["hin_Deva"])`).
  Encoded per sentence: it round-trips exactly on 2,009/2,009 FLORES+ and 1,000/1,000 sentiment texts. Per-word encoding,
  as used for Kannada FLORES, fails on 13 Hindi sentences.
- **lossy:** `to_lossy(text, "hin_Deva")`, the same rule table as Kannada with no change:
  - long → short vowels; retroflex → dental; aspirated → unaspirated;
  - anusvara → m before labials or at a word end, else n; chandrabindu (.N) → n;
  - nukta letters: क़ → k, ख़ → k, ग़ → g, ड़/ढ़ → d, य़ → y; फ़ → f and ज़ → z are kept;
  - avagraha dropped; then lowercased.
  - Not adapted: the Hindi inherent schwa is kept (for example सोमवार → "somavara"), because the Kannada rules have no
    schwa deletion. Hindi lossy is therefore further from natural Hindi than Kannada lossy is from natural Kannada.
- **natural:** Gemini drafts, `gemini-3.5-flash-lite`, temperature 0, cached.
  - Prompt `natural_romanization_hi_v1` is `natural_romanization_v1` with "Kannada" replaced by "Hindi" (3
    occurrences), verbatim:
    > Romanize the following Hindi sentence the way an ordinary Hindi speaker would type it in Latin script on a phone:
    > informal spelling, no diacritics, no special symbols. / Keep every word and the original word order. Do not
    > translate, explain, add or remove anything. Keep numbers, punctuation and any English words as they are. /
    > Output only the romanized sentence. / Hindi sentence: / {text}
  - Drafted for the 496 M4c sentences and the 200 sentiment items.
  - Same defect check and retries as Kannada: `defective()` (any Indic-script character, U+0900–U+0DFF, or new
    non-ASCII character); attempts 2–3; still defective → excluded and counted.
  - SIB natural is the M4c overlap (Kannada `natural257`) minus Hindi defects.

### Baseline gate (automatic, fixed now)
- **Accuracy:** a model counts for Hindi accuracy if its native Hindi accuracy CI excludes chance, lying above it, on
  BOTH sentiment 200 (0.5) and SIB 1,004 (1/7). Accuracy is the calibrated primary rule with bootstrap 95% CI (10,000).
- **Retrieval:** a model counts for Hindi retrieval if its native Hindi unmapped retrieval exceeds 0.5. This is acc@1
  on the M4c 248 test half at the train-half best layer, the same split and code as Kannada.
- **Counted for H1:** a model must pass the Hindi gate and also be counted for that measure in the Kannada ladder
  (retrieval: Qwen3.5, Sarvam-1, Gemma 4; accuracy: Qwen3, Qwen3.5, Sarvam-1, Gemma 4).
  - Qwen2.5 is reported, never counted.
  - Qwen3 has Hindi retrieval reported only, since there is no Kannada retrieval for it; its English M4c vectors are
    computed for this.
- Models failing the gate are reported, not counted.

### H1 (prediction): the native − natural gap is smaller for Hindi than for Kannada
- **Statistic per counted model:** d̄ = mean over items of [(Kannada native − Kannada natural) − (Hindi native −
  Hindi natural)], paired over the same item ids; 95% paired bootstrap CI (10,000; seed 0). Per-item scores are
  retrieval hit (0/1) or correctness (0/1, calibrated primary rule).
- **Measures:**
  - **Retrieval:** item set D = Kannada-retained ∩ Hindi-natural-clean M4c rows. Every form in both languages is
    recomputed on D with the M4c split restricted to D (train ∩ D, test ∩ D, folds as the ladder). Unmapped acc@1 on
    test ∩ D, with the best layer chosen on the train half per form and language. If no Hindi draft is defective, the
    Kannada values equal the ladder's.
  - **Sentiment:** the 198 clean Kannada natural ids ∩ Hindi-clean (n reported).
  - **SIB:** the 257 M4c-overlap ids ∩ Hindi-clean (n reported).
- **Calibration:** contextual calibration (mean of "N/A", "", "[MASK]") from each language's own run. The raw
  fallback is decided on the English rows of each model × task already scored for Kannada (identical English items).
- **Significance:** two-sided bootstrap p = 2·min(P(d* ≤ 0), P(d* ≥ 0)), floor 1/10,000, Holm-adjusted within each
  measure over its counted models. A model is positive if Holm p < 0.05 and d̄ > 0. Holm decides when it disagrees
  with the raw CI.
- **Verdict per measure:**
  - **Effect (H1 supported on that measure)** if positive in ≥ 2 of 3 counted retrieval models, or in ≥ 3 of 4 counted
    accuracy models (sentiment and SIB each separately).
  - If fewer models pass the gate: all but one, minimum 2. With fewer than 2 counted models the measure is "not
    testable".
  - **Refuted** on a measure if no effect. No pooled verdict across measures.
- **Exploratory, no prediction:** the same difference of gaps for native − ITRANS, on the same item sets.
- **Caveat stated now:** Hindi native performance is likely higher overall, so ceiling effects can shrink Hindi gaps.
  Native accuracy per language is reported next to every gap.
- **Ordering rule:** H1 is computed only after natural Hindi is scored (and its vectors computed) for every counted
  model.

### Run plan (overnight, detached, one model load at a time)
- **GPU, 5 models:** Hindi native, ITRANS and lossy on sentiment 200 and SIB 1,004. M4c 500-row sentence vectors for
  native, ITRANS and lossy, plus English for Qwen3. Tokens per word for every form, model and dataset. Then the gate.
- **Natural Hindi** (vectors and scores) runs when the drafts are complete.
- **Checks that stop the chain with a status file:**
  - data alignment as above;
  - vector arrays have the Kannada layer count and no NaN;
  - score files have the expected row counts and no NaN log-probs;
  - every natural draft is clean or excluded.
- **Estimate** (from the Kannada logs): forward about 15 min, scoring about 2.5 h for 3 forms × 5 models, natural about
  1 h once drafted. Drafts: about 700 Gemini requests plus retries (about 1 h). K3b follows: about 900–1,500 requests,
  likely over the 12:45 IST reset.

### H-Hindi — clarification and addendum (written 2026-10-23 12:05 IST, Aarnav's text; before natural Hindi results exist)
Status when written: Hindi natural drafts 486/696 (quota stop); no natural Hindi output has been scored or vectorized.
The native/ITRANS/lossy Hindi runs, tokens per word and the baseline gate already exist (`results/h_hindi/gate.json`).
1. **Counted models.** A model counts for H1 on a measure only if it passes the baseline in BOTH languages for that
   measure. Qwen2.5 passes the Hindi gate but is excluded: its native Kannada is at floor, so its Kannada gap is
   uninterpretable. Qwen3 is excluded from retrieval (no Kannada retrieval count). Counted: accuracy Qwen3, Qwen3.5,
   Sarvam-1, Gemma 4; retrieval Qwen3.5, Sarvam-1, Gemma 4. (Same lists the gate step already applied.)
2. **Defective drafts.** Items with a defective natural draft in EITHER language are dropped from BOTH languages for
   that measure: retrieval D = Kannada-retained ∩ Hindi-clean M4c rows; sentiment = Kannada-clean ∩ Hindi-clean ids;
   SIB = the M4c-overlap ids (Kannada-clean by construction) ∩ Hindi-clean. n is reported per measure.
3. **Secondary analysis** (registered now, reported with H1, no separate verdict):
   - (a) **English-word share** of natural Hindi vs natural Kannada on the same item ids (each measure's H1 item set).
     A word is English if, lowercased with edge punctuation stripped (`english_share.words()`), it is longer than 3
     characters and in the wordfreq English list with Zipf ≥ 3. Per-item share = English words / words. Statistic:
     mean over items of (Hindi share − Kannada share), with a paired bootstrap 95% CI (10,000; seed 0). No proper-noun
     filter.
   - (b) **Loan-free H1:** H1 recomputed exactly as registered (same statistic, Holm within measure over the counted
     models, same counting rule) on the items whose natural text has zero such English words in BOTH languages.
     For retrieval, D is restricted further and the M4c split restricted to it, with the layer re-chosen on its train
     half. n is reported. Its rule outcome is descriptive only.
   - **Interpretation fixed now:** if H1 holds on a measure on the full set but not on the loan-free set, it is
     reported as possibly driven by English loans.
4. **Primary emphasis.** Hindi native sentiment is near ceiling (0.925–0.990 across the five models), so H1 is
   interpreted mainly from SIB and retrieval; sentiment is reported with the ceiling caveat. The registered decision
   rule is unchanged.

---
`````

##### PRE-REGISTRATION — K3b-hi: Gemini vs native-speaker natural romanization on Dakshina Hindi (written 2026-10-23 12:05 IST, Aarnav's design; before any Dakshina Hindi text is sent to Gemini)

RESULTS.md lines 2233 to 2247; first line committed in `176c284` on 2026-10-23 12:04:11 +0530; last line in `5e44d59` on 2026-10-23 14:17:52 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — K3b-hi: Gemini vs native-speaker natural romanization on Dakshina Hindi (written 2026-10-23 12:05 IST, Aarnav's design; before any Dakshina Hindi text is sent to Gemini)
- **Design and rule:** identical to K3b (Kannada) above: same filters (duplicate native strings dropped, all copies;
  strings with fewer than 3 native words dropped), 500 strings drawn with `default_rng(6)`, resample subset of 200 with
  `default_rng(7)` and G1/G2 at temperature 1.0, same defect check and retries, same three statistics, same pooled
  ratio with bootstrap CIs, same [0.80, 1.25] rule, chrF descriptive only. K3b-hi holds only if all three match.
- **Data:** Dakshina v1.0 official release (MD5-verified 2026-10-23), `hi/romanized/hi.romanized.rejoined.tsv` (10,000
  rows, native Devanagari TAB native-speaker romanization).
- **Prompt:** `natural_romanization_hi_v1` (the K3b prompt with only the language name changed; the same prompt as the
  Hindi drafts above), `gemini-3.5-flash-lite`, temperature 0 for the primary draft.
- **Quota priority:** lowest. It runs only after the Hindi drafts and K3b (Kannada) are complete, in its own chain.
- **Outputs:** `results/k3b_hi/`. Separate verdict from K3b; no pooled verdict.
- **Limitation stated now:** "th"/"dh" and the h-digraphs mark aspiration and dentals differently in Hindi practice,
  so (2) remains h-digraph use, not aspiration; Hindi Wikipedia text has more English and Perso-Arabic loans.

---
`````

##### 2026-10-23 — H-Hindi results (registered 01:00 IST + 12:05 IST addendum)

RESULTS.md lines 2248 to 2303; first line committed in `5e44d59` on 2026-10-23 14:17:52 +0530; last line in `70a57ab` on 2026-10-23 15:44:41 +0530; labels from the title and parent heading: result

`````text
## 2026-10-23 — H-Hindi results (registered 01:00 IST + 12:05 IST addendum)
Commit 7b4e869 (code); outputs `results/h_hindi/{gate.json, tokens_per_word.csv, h1.csv, h1_verdict.json,
exploratory_itrans.csv, h1_secondary.json, h1_loanfree.csv}`. GPU chain finished 14:16 IST; no failed check.
- **Drafts:** 696/696 Hindi natural drafts; 4 still defective after 3 attempts (flores-114, flores-1465, flores-1606,
  indicsentiment-test-846), excluded. Item sets: retrieval D = 493 rows (246 test), sentiment n = 197, SIB n = 256.
- **Gate:** all five models pass (Hindi native sentiment 0.895–0.990, SIB 0.660–0.781, retrieval 0.698–1.000). Counted:
  retrieval Qwen3.5, Sarvam-1, Gemma 4; accuracy Qwen3, Qwen3.5, Sarvam-1, Gemma 4.

### H1 (d̄ = Kannada native−natural gap minus Hindi gap; 95% paired bootstrap CI; Holm within measure)
| measure | model | Kn native | Kn natural | Hi native | Hi natural | d̄ [95% CI] | Holm p | positive |
|---|---|---|---|---|---|---|---|---|
| retrieval (n=246) | Qwen3.5 | 1.000 | 0.516 | 0.992 | 0.947 | 0.439 [0.370, 0.508] | <0.001 | yes |
| | Sarvam-1 | 0.988 | 0.919 | 0.992 | 0.939 | 0.016 [−0.012, 0.045] | 0.311 | no |
| | Gemma 4 | 1.000 | 0.711 | 1.000 | 0.980 | 0.268 [0.207, 0.329] | <0.001 | yes |
| SIB (n=256) | Qwen3 | 0.668 | 0.371 | 0.660 | 0.531 | 0.168 [0.086, 0.250] | <0.001 | yes |
| | Qwen3.5 | 0.699 | 0.457 | 0.723 | 0.633 | 0.152 [0.082, 0.223] | <0.001 | yes |
| | Sarvam-1 | 0.750 | 0.727 | 0.758 | 0.723 | −0.012 [−0.074, 0.051] | 0.772 | no |
| | Gemma 4 | 0.758 | 0.543 | 0.773 | 0.734 | 0.176 [0.102, 0.246] | <0.001 | yes |
| sentiment (n=197) | Qwen3 | 0.832 | 0.558 | 0.944 | 0.878 | 0.208 [0.107, 0.310] | 0.001 | yes |
| | Qwen3.5 | 0.736 | 0.721 | 0.924 | 0.944 | 0.036 [−0.046, 0.122] | 0.426 | no |
| | Sarvam-1 | 0.954 | 0.893 | 0.970 | 0.964 | 0.056 [0.010, 0.107] | 0.058 | no (Holm decides; raw CI excludes 0) |
| | Gemma 4 | 0.985 | 0.802 | 0.990 | 0.990 | 0.183 [0.122, 0.244] | <0.001 | yes |

Qwen2.5 (reported, never counted): retrieval −0.431, SIB −0.211, sentiment 0.056.

**Verdicts (registered rule):**
- **Retrieval: effect (H1 supported)**, 2 of 3 positive (needed 2).
- **SIB: effect (H1 supported)**, 3 of 4 positive (needed 3).
- **Sentiment: refuted**, 2 of 4 positive (needed 3). Hindi native sentiment is near ceiling (0.924–0.990); per the
  addendum, sentiment is reported with the ceiling caveat and H1 is interpreted mainly from SIB and retrieval.
- Sarvam-1 is not positive on any measure: its Kannada natural gap is already small (retrieval 0.069, SIB 0.023).

### Secondary (addendum item 3; no separate verdict)
- **(a) English-word share, Hindi natural minus Kannada natural (same ids):** retrieval items 0.104 vs 0.064, +0.040
  [0.031, 0.049]; SIB 0.119 vs 0.069, +0.050 [0.037, 0.063]; sentiment 0.178 vs 0.073, +0.106 [0.089, 0.122]. Natural
  Hindi contains more English words than natural Kannada on every item set.
- **(b) Loan-free H1** (items with zero English words in both languages): retrieval n = 41 test items, 1 of 3 positive
  (Gemma 4, d̄ 0.171 [0.073, 0.293]; Qwen3.5 0.195 [0.024, 0.366], Holm p 0.061); SIB n = 31, 1 of 4 positive (Gemma 4,
  0.355 [0.129, 0.548]); sentiment n = 6, 0 of 4. Rule outcome (descriptive): not met on any measure.
- **Registered interpretation applies:** H1 holds on retrieval and SIB on the full set but not on the loan-free set, so
  both are reported as **possibly driven by English loans**. The loan-free sets are small (41, 31, 6 items), so the
  loan-free outcome is low-powered; d̄ stays positive for 7 of 7 counted retrieval/SIB models (3 of 7 CIs exclude 0
  before Holm; Qwen3.5 SIB lower bound is 0.000). These are stated, not used to override the registered reading.

### Exploratory native − ITRANS (no prediction)
Positive (Holm): retrieval Qwen3.5 0.276, Gemma 4 0.329; Sarvam-1 retrieval −0.122 (Hindi ITRANS gap larger). No
accuracy model is positive; Sarvam-1 is negative on all three (SIB −0.102, sentiment −0.107, retrieval −0.122),
Qwen3.5 sentiment −0.142.

### Tokens per word (Hindi; SIB / natural on M4c 496)
native: Qwen 4.78, Qwen3.5 2.18, Sarvam 1.40, Gemma 1.39. ITRANS 2.52–3.29, lossy 1.90–2.67, natural (M4c) 1.67–2.52;
full table `results/h_hindi/tokens_per_word.csv`.

**Next:** K3b drafts 276/900 (quota stop; resumes 2026-10-24 12:45 IST), then K3b-hi.

---
`````

##### PRE-REGISTRATION — H1-LF: H1 at equal English-loan content (written 2026-10-23 15:44 IST, Aarnav's design; FOLLOW-UP REGISTERED POST H1: written after the H1 results and the loan-free secondary above were seen, before any H1-LF statistic, s

RESULTS.md lines 2304 to 2361; first line committed in `6fa02b3` on 2026-10-23 15:44:48 +0530; last line in `5064f46` on 2026-10-23 15:52:38 +0530; labels from the title and parent heading: registered, result

`````text
## PRE-REGISTRATION — H1-LF: H1 at equal English-loan content (written 2026-10-23 15:44 IST, Aarnav's design; FOLLOW-UP REGISTERED POST H1: written after the H1 results and the loan-free secondary above were seen, before any H1-LF statistic, script or draft exists)
The registered H1 verdicts stand unchanged (retrieval effect, SIB effect, sentiment refuted; retrieval and SIB flagged
"possibly driven by English loans"). H1-LF asks whether the H1 effect survives at equal English-word share. Because it
was designed after seeing H1, it is a follow-up test, reported as such. Script `scripts/h1lf.py` (written after this
registration); outputs `results/h1lf/`.

### Option 2 (run now, CPU, existing scores and vectors)
- **Items and outcomes:** the H1 item sets and the same binary outcomes as H1 (retrieval hit at the train-half best
  layer, n = 246 test items; SIB n = 256; sentiment n = 197; calibrated primary rule), per counted model × measure
  (same counted models as H1).
- **Per item:** d_i = (Kannada native − natural)_i − (Hindi native − natural)_i (linear probability);
  δ_i = Hindi natural English share − Kannada natural English share (the addendum definition: lowercased
  `english_share.words()`, words longer than 3 characters in the wordfreq English list with Zipf ≥ 3; share = English
  words / words).
- **Model:** OLS d_i = a + b·δ_i. **Primary statistic: the intercept a** (H1 effect at equal English share), 95% item
  bootstrap CI (10,000; seed 0; percentile). Slope b reported with its CI.
- **Significance and rule (same as H1):** two-sided bootstrap p for a = 2·min(P(a* ≤ 0), P(a* ≥ 0)), floor 1/10,000;
  Holm within measure over the counted models; positive if Holm p < 0.05 and a > 0. Effect on a measure if positive in
  ≥ 2 of 3 counted retrieval models or ≥ 3 of 4 counted accuracy models (same fallback rule). Verdict per measure:
  "effect at equal English share" or "refuted". No pooled verdict.
- **Sensitivity (reported, no verdict):**
  - (a) Continuous outcomes, same regression and bootstrap. Retrieval: at the same chosen layer per language × form,
    after the same train-mean centering, cos(x_i, e_i) − max_{j≠i} cos(x_i, e_j) over the test set (similarity to the
    correct English sentence minus the best distractor). Accuracy: gold margin on the scores used for the calibrated
    primary prediction (avg3-calibrated log-probs, or raw where the English-row fallback applies): s_gold − max over
    other labels.
  - (b) δ binned into tertiles (within each measure's item set, by rank, ties broken by item order), mean d per bin
    with bootstrap 95% CI.
- **Caveats stated now:** δ is mostly positive (Hindi natural has more English), so the intercept partly extrapolates
  to δ = 0; the fraction of items with δ ≤ 0 is reported. The linear-probability model is a linearity assumption.

### Exploratory note (no verdict): native − ITRANS is a loan-free comparison
The exploratory native − ITRANS difference of gaps is positive for retrieval in Qwen3.5 (+0.276) and Gemma 4 (+0.329)
(`results/h_hindi/exploratory_itrans.csv`): the native − ITRANS gap is smaller for Hindi. ITRANS is a deterministic
transliteration of the native script and adds no English loans, so this bears on the loan account. To confirm the
English share is near equal, the English share (same definition) of Hindi ITRANS vs Kannada ITRANS is computed on the
same ids (each H1 item set), mean paired difference with bootstrap 95% CI. Reported, no verdict.

### Option 1 (queued; Gemini quota after K3b, before K3b-hi)
- **Drafts:** natural romanization for all 1,004 SIB items in both languages with the identical prompts and settings
  (Kannada `natural_romanization_v1` on the FLORES+ `kan_Knda` native text, as in E0c; Hindi `natural_romanization_hi_v1`
  on `hin_Deva`; `gemini-3.5-flash-lite`, temperature 0, cached; `defective()`, attempts 2–3, still defective →
  excluded and counted). The overlap items already drafted are the same API calls and come from the cache.
  About 1,500 new requests (several days of quota).
- **Scoring:** the counted accuracy models (Qwen3, Qwen3.5, Sarvam-1, Gemma 4) on natural SIB, all clean items, both
  languages (form `natural1004`), one model load at a time; calibration and fallback exactly as H1.
- **Checks (stop the chain on failure):** row counts and no NaN log-probs; on overlap items whose new draft text is
  identical to the H1 natural text, pred_cal agrees with the H1 natural predictions for ≥ 98% of items per model ×
  language.
- **Statistic and rule:** the H1 statistic (d̄, paired bootstrap, Holm over the 4 counted models, positive if Holm
  p < 0.05 and d̄ > 0, effect if ≥ 3 of 4) on the **loan-free subset of all 1,004**: items clean in both languages
  with zero English words longer than 3 characters (Zipf ≥ 3) in both natural texts. n reported. Verdict: "loan-free
  effect" or "refuted". The same statistic on all clean 1,004 items is reported descriptively.

### Gemini queue order
K3b (Kannada, running) → H1-LF option 1 drafts → K3b-hi.

---
`````

##### 2026-10-23 — H1-LF option 2 results (follow-up registered post H1, 15:44 IST)

RESULTS.md lines 2362 to 2390; first line committed in `5064f46` on 2026-10-23 15:52:38 +0530; last line in `5064f46` on 2026-10-23 15:52:38 +0530; labels from the title and parent heading: result

`````text
## 2026-10-23 — H1-LF option 2 results (follow-up registered post H1, 15:44 IST)
Script `scripts/h1lf.py opt2`; outputs `results/h1lf/{opt2.csv, opt2_verdict.json, opt2_sensitivity.csv,
opt2_tertiles.csv}`. Check passed: the binary d_i reproduce the H1 n and d̄ for every model × measure.
OLS d_i = a + b·δ_i; a = H1 effect at equal English share (as measured; see the diagnostic below).

| measure | model | n | H1 d̄ | intercept a [95% CI] | Holm p | positive | slope b [95% CI] |
|---|---|---|---|---|---|---|---|
| retrieval | Qwen3.5 | 246 | 0.439 | 0.418 [0.346, 0.496] | <0.001 | yes | 0.67 [−0.20, 1.39] |
| | Sarvam-1 | 246 | 0.016 | 0.013 [−0.013, 0.041] | 0.336 | no | 0.11 [−0.17, 0.43] |
| | Gemma 4 | 246 | 0.268 | 0.248 [0.187, 0.314] | <0.001 | yes | 0.67 [−0.03, 1.29] |
| SIB | Qwen3 | 256 | 0.168 | 0.156 [0.077, 0.239] | <0.001 | yes | 0.23 [−0.51, 0.96] |
| | Qwen3.5 | 256 | 0.152 | 0.151 [0.075, 0.226] | 0.001 | yes | 0.04 [−0.60, 0.64] |
| | Sarvam-1 | 256 | −0.012 | 0.009 [−0.059, 0.076] | 0.814 | no | −0.41 [−1.13, 0.26] |
| | Gemma 4 | 256 | 0.176 | 0.164 [0.078, 0.246] | 0.001 | yes | 0.24 [−0.34, 0.89] |
| sentiment | Qwen3 | 197 | 0.208 | 0.195 [0.049, 0.336] | 0.026 | yes | 0.13 [−0.71, 1.12] |
| | Qwen3.5 | 197 | 0.036 | 0.037 [−0.071, 0.152] | 0.498 | no | −0.02 [−0.80, 0.75] |
| | Sarvam-1 | 197 | 0.056 | 0.054 [−0.007, 0.119] | 0.163 | no | 0.02 [−0.25, 0.29] |
| | Gemma 4 | 197 | 0.183 | 0.116 [0.024, 0.215] | 0.042 | yes | 0.63 [−0.05, 1.21] |

δ: mean 0.031 (retrieval), 0.050 (SIB), 0.106 (sentiment); share of items with δ ≤ 0: 0.40, 0.33, 0.17.

**Verdicts (H1 rule):** retrieval **effect at equal English share** (2 of 3, needed 2); SIB **effect at equal English
share** (3 of 4, needed 3); sentiment **refuted** (2 of 4, needed 3). Every counted slope CI includes 0.
- **Sensitivity (a), continuous outcomes (no verdict):** intercept CIs exclude 0 for every counted model × measure
  except Sarvam-1 SIB (0.155 [−0.051, 0.359]); same direction as the binary results.
- **Sensitivity (b), tertiles of δ (no verdict):** in the lowest tertile (δ ≤ 0.003; Hindi no more "English" than
  Kannada), mean d is 0.163–0.209 on SIB for Qwen3, Qwen3.5, Gemma 4 (CIs exclude 0) and 0.207–0.402 on retrieval for
  Qwen3.5, Gemma 4; no monotone trend across tertiles.

`````

##### PRE-REGISTRATION — English-loan measure v2 (written 2026-10-23 16:00 IST, Aarnav's design; follows the 2026-10-23 diagnostic of the English-word measure; before any H1-LF option 1 score exists and before any v2 count is computed)

RESULTS.md lines 2417 to 2435; first line committed in `6867631` on 2026-10-23 16:00:59 +0530; last line in `6867631` on 2026-10-23 16:00:59 +0530; labels from the title and parent heading: registered

`````text
## PRE-REGISTRATION — English-loan measure v2 (written 2026-10-23 16:00 IST, Aarnav's design; follows the 2026-10-23 diagnostic of the English-word measure; before any H1-LF option 1 score exists and before any v2 count is computed)
- **Definition v2:** a word in a romanized text (lowercased `english_share.words()`) counts as an English loan if (i)
  it is in the wordfreq English list with Zipf ≥ 3, (ii) it is longer than 3 characters, and (iii) it appears in the
  item's parallel English sentence (FLORES+ `eng_Latn` for FLORES/SIB items, the IndicSentiment English review for
  sentiment items), case-insensitive, as the exact token or a simple plural/possessive variant. Variant rule: with w
  the romanized word and E the set of lowercased English tokens (each also with a trailing possessive 's removed),
  after removing a trailing possessive 's from w, w matches if w ∈ E, w+"s" ∈ E, w+"es" ∈ E, or w ends in "s" and
  w[:-1] ∈ E, or w ends in "es" and w[:-2] ∈ E. v2 share = v2 loans / words. **Stated as a lower bound on loan share**
  (loans respelled, or absent from the English sentence, are missed).
- **Validity check, fixed now:** Hindi ITRANS minus Kannada ITRANS v2 share on the same ids (the H1 retrieval test set
  and the H1 SIB set), mean paired difference with bootstrap 95% CI (10,000; seed 0), must lie within [−0.01, +0.01]
  on BOTH retrieval and SIB items. If it fails: stop and report; v2 is not used.
- **If the check passes:** v2 replaces the registered definition for H1-LF option 1 (loan-free subset = zero v2 loans
  in both languages). The original definition is also reported alongside.
- **Post hoc (labelled as such, no verdict):** recompute with v2 the addendum English-share comparison, the loan-free
  H1, and option 2 (intercept, slope, tertiles). Report the top 20 v2-matched words per language (natural texts) as a
  sanity list.

---
`````

##### 2026-10-23 — English-loan measure v2: validity check (registered 16:00 IST)

RESULTS.md lines 2508 to 2515; first line committed in `7443e57` on 2026-10-23 16:12:55 +0530; last line in `7443e57` on 2026-10-23 16:12:55 +0530; labels from the title and parent heading: none

`````text
## 2026-10-23 — English-loan measure v2: validity check (registered 16:00 IST)
`scripts/h1lf.py v2`; `results/h1lf/v2_check.json`. Hindi ITRANS minus Kannada ITRANS v2 share, same ids:
retrieval (n = 246) −0.0052 [−0.0080, −0.0025]; SIB (n = 256) −0.0063 [−0.0097, −0.0032]. Both CIs lie within
[−0.01, +0.01]: **check passed**. v2 therefore replaces the registered definition for H1-LF option 1 (the original is
reported alongside; `h1lf.py analyse1` now does this). Residual Kannada ITRANS matches are loans transliterated from
Kannada script (v2 share 0.009 Kannada, 0.004 Hindi), so the CI excludes 0 in the Kannada direction while staying in
the band.

`````

##### 2026-10-23 — Note on H1 and English loans after v2 (post hoc descriptive, dated, no verdict; Aarnav)

RESULTS.md lines 2565 to 2572; first line committed in `0aec6a3` on 2026-10-23 21:17:49 +0530; last line in `f4f5555` on 2026-10-24 01:49:51 +0530; labels from the title and parent heading: post hoc, result

`````text
## 2026-10-23 — Note on H1 and English loans after v2 (post hoc descriptive, dated, no verdict; Aarnav)
- **Retrieval:** on the retrieval items the v2 loan-share difference (Hindi minus Kannada natural) is +0.005
  [−0.005, 0.015], so the retrieval H1 effect cannot be attributed to English loans.
- **SIB:** the v2 loan-free subset (n = 74) does not meet the rule, and v2 is a lower bound on loan share, so the SIB
  reading awaits H1-LF option 1.
- The registered H1 verdicts and the registered H1-LF option 2 verdicts are unchanged.

---
`````

##### 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists)

RESULTS.md lines 2972 to 3002; first line committed in `46bd82a` on 2026-10-26 12:10:58 +0530; last line in `46bd82a` on 2026-10-26 12:10:58 +0530; labels from the title and parent heading: result, failed or not run

`````text
## 2026-10-26 12:05 IST — English-share tagger for K2: validity check of codemix v1 FAILED; pre-data fix v2 (no K2 result exists)
- **Definition in K2 (registered 2026-10-16, `shattered.translit.codemix`, "v1"):** neither the English-loan measure v1
  (wordfreq Zipf ≥ 3, > 3 characters) nor v2 (also in the parallel English sentence). A lower-cased alphabetic token
  is English if it is in the wordfreq top-50k English list and not in the romanized-Kannada lexicon (to_lossy of the
  top-50k Kannada Wikipedia words); in both lists it is language-independent; otherwise Kannada.
- **Check (Aarnav's design):** 50 kanglish_verified texts, `default_rng(0)`, 883 alphabetic tokens; every token type
  marked by Claude Code (`results/codemix_check/gold_sample0.json`: E English, K Kannada, N name/unit, H English stem +
  Kannada suffix; N and H count as not English). `scripts/codemix_check.py 0 v1` →
  `results/codemix_check/check_sample0_v1.json`.
- **Result: precision 0.928 (219/236), recall 0.883 (219/248): below 0.9, so stopped.**
  - False positives (17): names and name-derived adjectives tagged English (amsterdam, angola ×2, claudia, germany,
    iceland, luxembourg, machu, stearns, frank, BIS, austrian, russian, african, mediterranean) and one Kannada word
    (kami, "less", ×2).
  - Missed English (29): 24 common English words that are also in the Kannada lexicon and so become
    language-independent (and, on, so, but, air ×3, start ×2, help, post, skin, lens ×3, gel, LED, ad ×2, dark, bed,
    sharp, limited); 5 English words outside the top-50k list (eggless, moisturize, purifiers ×2, tuners,
    occasionaly).
  - Not counted as English in either definition: 9 English-stem + Kannada-suffix tokens (productginta, groupnalli,
    lensesgalu, skinannu, …); with them counted as English, recall is 0.852.
- **Fix, v2 (`codemix.tag_v2` / `code_mixing_v2`; v1 kept unchanged):** (1) single letters language-independent;
  (2) a token that occurs in the item's parallel English sentence only in Title case and not sentence-initially is a
  name (language-independent; all-caps acronyms not affected); (3) a token in both lists goes to the language where
  it ranks higher (English: position in the wordfreq top-50k list; Kannada: best rank of a Kannada Wikipedia word whose
  lossy romanization contains it); (4) a token in neither list is English if its wordfreq English Zipf ≥ 2.5, else
  Kannada; (5) English stem + Kannada suffix stays Kannada (the share is a lower bound for such loans).
- **v2 was designed after seeing sample 0's errors**, so its rerun on sample 0 is optimistic. A fresh sample
  (`default_rng(1)`, 50 texts) is marked by hand from the v1 view (before any v2 tag of it is seen) and is the deciding
  check: v2 is used for K2 only if precision and recall are both ≥ 0.9 on it. K2 uses v2 for the English share in
  K2a and K2b if it passes; v1 results are reported alongside.

---
`````

##### 2026-10-26 12:10 IST — English-share tagger v2: checks (stopped; decision needed from Aarnav)

RESULTS.md lines 3003 to 3022; first line committed in `46bd82a` on 2026-10-26 12:10:58 +0530; last line in `46bd82a` on 2026-10-26 12:10:58 +0530; labels from the title and parent heading: none

`````text
## 2026-10-26 12:10 IST — English-share tagger v2: checks (stopped; decision needed from Aarnav)
`scripts/codemix_check.py <seed> <v1|v2>`; `results/codemix_check/check_sample{0,1}_{v1,v2}.json`; gold markings
`gold_sample0.json` (marked from v1, before v2 existed) and `gold_sample1.json` (fresh sample, `default_rng(1)`, 1,004
tokens, marked from the v1 view before any v2 tag of it was seen).

| tagger | sample 0 (883 tokens; v2 designed from its errors) | sample 1 (1,004 tokens; fresh) |
|---|---|---|
| v1 (registered) | P 0.928, R 0.883 | P 0.900, R 0.863 |
| v2 | P 0.929, R 0.891 | **P 0.924, R 0.941** |
| v2 without the name rule (informative only; tuned on both samples) | P 0.892, R 0.968 | P 0.880, R 0.981 |

(R with English-stem + Kannada-suffix tokens counted as English: v1 0.852 / 0.815; v2 0.860 / 0.888.)
- v2 passes the criterion stated before the check (fresh sample ≥ 0.9 on both) but **fails recall on the rerun of
  sample 0** (0.891). Causes: (a) the name rule also removes ordinary English words inside multi-word names in the
  English sentence (World War, Planned Parenthood, Senate subcommittee, Anne Frank Museum, State Symphony Orchestra);
  (b) the rank rule sends Kannada "ee" ("this") to English, because the lossy romanization writes ಈ as "i", so "ee" is
  rare in the Kannada lexicon; similarly andre, ana, anna. Without the name rule recall is high but precision falls
  below 0.9 (names counted as English).
- **Stopped:** neither variant clears 0.9 on both samples. No K2 result exists; the K1/K2 pilot is not queued.

`````

##### 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched

RESULTS.md lines 3178 to 3185; first line committed in `126a488` on 2026-10-28 03:46:10 +0530; last line in `126a488` on 2026-10-28 03:46:10 +0530; labels from the title and parent heading: failed or not run

`````text
## 2026-10-28 03:17 IST — Chain incident: network outage during the H1-LF drafts; K3b-hi chain relaunched
The SIB-1,004 Hindi drafts hit `getaddrinfo failed` (no network) on 2026-10-27 after 15:18 IST and the H1-LF chain was marked
FAILED; it restarted at 02:46 IST and completed the drafts at 03:14 IST (Kannada 1,004 and Hindi 1,004 done; 9 and 10 still
defective after retries, excluded as registered), then started GPU scoring (qwen3-1.7b first). The K3b-hi chain, which stops
when it sees the H1-LF chain FAILED, ended at 02:46 IST without starting; relaunched at 03:17 IST (API only, no GPU). No design
change.

---
`````

##### 2026-10-28 05:45 IST — H1-LF option 1: scoring finished (all 8 model x language loads); check script bug fixed

RESULTS.md lines 3227 to 3233; first line committed in `ca5c2e9` on 2026-10-28 05:39:02 +0530; last line in `ca5c2e9` on 2026-10-28 05:39:02 +0530; labels from the title and parent heading: none

`````text
## 2026-10-28 05:45 IST — H1-LF option 1: scoring finished (all 8 model x language loads); check script bug fixed
The chain stopped at `score check` with a `KeyError: 'qwen2.5-1.5b'` in `scored()` (a crash, not a failed check): it concatenated English
rows of every H1 model but the option-1 score directories hold calibration for the four counted models only. Fix, no design change:
`scored()` keeps English rows only for models with calibration in that directory (identical for the H1 directories, which hold all
models). The check (row counts, no NaN, pred_cal agreement >= 0.98 on identical-text overlap) is re-run unchanged.

---
`````

##### 2026-10-28 06:05 IST — H1-LF option 1 results (registered 2026-10-23 15:44 IST; v2 loan definition primary because its validity check passed)

RESULTS.md lines 3234 to 3244; first line committed in `ca5c2e9` on 2026-10-28 05:39:02 +0530; last line in `9fbb738` on 2026-10-28 10:17:38 +0530; labels from the title and parent heading: result

`````text
## 2026-10-28 06:05 IST — H1-LF option 1 results (registered 2026-10-23 15:44 IST; v2 loan definition primary because its validity check passed)
Score check (re-run after the 05:45 bug fix, unchanged rule): pred_cal agreement 1.000 on all identical-text overlap items (Kannada 257;
Hindi 256 per model). `scripts/h1lf.py analyse1`; `results/h1lf/opt1.csv`, `opt1_verdict.json`.
- **Verdict: loan-free effect** (3 of 4 counted models positive, Holm p < 0.05; rule needs 3). Loan-free subset n = 296 of 985 items clean in both languages.
- Difference of gaps (Kannada minus Hindi; native minus natural): Qwen3 +0.196, Qwen3.5 +0.199, Gemma 4 +0.233 (Holm p < 0.001 each);
  Sarvam-1 -0.047 (Holm p 0.165, not positive). On all 985 clean items (descriptive): +0.168, +0.149, +0.170, Sarvam-1 -0.019 (p 0.256).
  The loan-free differences are not smaller than the all-items ones. The registered v1 loan-free subset (n = 110) gives the same signs (3 of 4 positive).
- The H1-LF chain script was patched with run_net and the upstream grace period after finishing; its status was set to DONE by hand
  with the reason recorded in its status file.

---
`````

##### 2026-10-28 06:20 IST — H1-LF selection check (exploratory; registered before running; CPU; Aarnav 2026-10-28)

RESULTS.md lines 3245 to 3260; first line committed in `9fbb738` on 2026-10-28 10:17:38 +0530; last line in `9fbb738` on 2026-10-28 10:17:38 +0530; labels from the title and parent heading: registered, exploratory

`````text
## 2026-10-28 06:20 IST — H1-LF selection check (exploratory; registered before running; CPU; Aarnav 2026-10-28)
**Why:** the loan-free subset (296 of 985 items clean in both languages, v2 definition) is a selected set; it may differ from all clean
items in length, content or topic. The registered H1-LF verdict is not changed by this analysis; it carries no verdict.
- **Items:** the 296 loan-free and the 985 clean items of `results/h1lf/opt1_verdict.json` (same construction as `h1lf.py analyse1`).
- **Descriptives, loan-free versus the other 689 items:** English word count of the parallel sentence; Kannada native word count; Qwen3
  token count of the Kannada native text; share of items whose English sentence contains a digit; share containing a name (the
  `names_in` rule of the v2 English-word tagger); SIB topic distribution (the item's label). Mann-Whitney (lengths), Fisher exact (shares)
  and chi-square (topics) p values, reported descriptively; no threshold.
- **Refit (done whether or not the subsets differ):** per counted model, item-level d_i = (native − natural, Kannada) − (native − natural,
  Hindi), regressed on a loan-free indicator, z-scored English words, z-scored Kannada Qwen3 tokens, the digit and name indicators and topic
  dummies, over all 985 items, heteroscedasticity-robust (HC3) standard errors. Reported: the adjusted gap for loan-free items (intercept
  plus indicator, covariates at their 985-item means) with a 95% CI and p, the indicator coefficient (loan-free minus other items,
  adjusted), and the unadjusted loan-free mean as a check against opt1.csv.
- **Reading, fixed now:** "the loan-free gap survives" if the adjusted loan-free gap is positive with a 95% CI above zero; Holm over the
  four models is reported alongside the raw p. No claim about a causal role of the covariates.

`````

##### 2026-10-28 06:50 IST — H1-LF selection check results (exploratory, no verdict; registered 06:20 IST; `scripts/h1lf_selection.py`)

RESULTS.md lines 3261 to 3269; first line committed in `9fbb738` on 2026-10-28 10:17:38 +0530; last line in `4b45908` on 2026-10-29 01:14:35 +0530; labels from the title and parent heading: exploratory, result

`````text
## 2026-10-28 06:50 IST — H1-LF selection check results (exploratory, no verdict; registered 06:20 IST; `scripts/h1lf_selection.py`)
Loan-free items (n = 296) against the other 689 clean items: English words 20.1 vs 21.6 (p 0.001), Kannada words 14.7 vs 16.5, Qwen3
Kannada tokens 176 vs 193 (both p < 0.001), digit 10% vs 25%, name 30% vs 59% (both p < 0.001); topics differ (chi-square p 0.0001;
sports 7.8% vs 12.2% and entertainment 4.4% vs 9.3% of the group lower in loan-free). Refit over all 985 (lengths, digits, names, topic
dummies, HC3): adjusted loan-free gap (Kannada gap minus Hindi gap) Qwen3 0.194 [0.114, 0.273], Qwen3.5 0.177 [0.095, 0.260], Gemma 4 0.223
[0.150, 0.296] (Holm p < 0.001), Sarvam-1 -0.044 [-0.109, 0.022] (p 0.19); the loan-free indicator is not significant in any model
(p 0.44, 0.42, 0.37, 0.09). The loan-free gap survives. Wording change (Aarnav): "differences of the gaps" replaced by "the Kannada gap
exceeds the Hindi gap by ...".

`````

## Result files, every number

#### `results/h_hindi/data_check.json` (600 bytes; first commit 358fee8 2026-10-23 01:09:49 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 (H-Hindi)"
provenance.git_commit = "358fee81584b19edc19e8ce33a21a3f5e6091b23"
provenance.timestamp_utc = "2026-10-22T19:40:20+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h_hindi.py", "check"]
flores_hi_2009 = true
sentiment_rows_aligned = true
sib_ids_labels_aligned = true
itrans_lossless_flores = true
itrans_lossless_sentiment = true
sentiment_items_200 = true
m4c_rows_500_retained_496 = true
`````

#### `results/h_hindi/exploratory_itrans.csv` (2,742 bytes; first commit 5e44d59 2026-10-23 14:17:52 +0530)

| measure | comparison | model | counted | kannada_native | kannada_other | hindi_native | hindi_other | n | diff_of_gaps | ci | p | p_holm | positive | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | native-itrans | qwen2.5-1.5b | False | 0.24390243902439024 | 0.13008130081300814 | 0.6951219512195121 | 0.16666666666666666 | 246 | -0.4146341463414634 | [-0.5040650406504065, -0.32113821138211385] | 0.0001 |  | False | False |
| sentiment | native-itrans | qwen2.5-1.5b | False | 0.700507614213198 | 0.49238578680203043 | 0.8934010152284264 | 0.49746192893401014 | 197 | -0.18781725888324874 | [-0.2639593908629442, -0.116751269035533] | 0.0001 |  | False | False |
| sib | native-itrans | qwen2.5-1.5b | False | 0.32421875 | 0.25390625 | 0.66015625 | 0.30078125 | 256 | -0.2890625 | [-0.37890625, -0.19921875] | 0.0001 |  | False | False |
| retrieval | native-itrans | qwen3.5-2b | True | 1.0 | 0.21544715447154472 | 0.991869918699187 | 0.483739837398374 | 246 | 0.2764227642276423 | [0.2032520325203252, 0.34959349593495936] | 0.0001 | 0.00030000000000000003 | True | False |
| sentiment | native-itrans | qwen3.5-2b | True | 0.7360406091370558 | 0.6548223350253807 | 0.9238578680203046 | 0.700507614213198 | 197 | -0.14213197969543148 | [-0.22842639593908629, -0.05583756345177665] | 0.0012 | 0.0048 | False | False |
| sib | native-itrans | qwen3.5-2b | True | 0.69921875 | 0.2578125 | 0.72265625 | 0.27734375 | 256 | -0.00390625 | [-0.078125, 0.0703125] | 0.962 | 0.962 | False | False |
| retrieval | native-itrans | sarvam-1 | True | 0.9878048780487805 | 0.6829268292682927 | 0.991869918699187 | 0.5650406504065041 | 246 | -0.12195121951219512 | [-0.1910569105691057, -0.056910569105691054] | 0.0004 | 0.0004 | False | False |
| sentiment | native-itrans | sarvam-1 | True | 0.9543147208121827 | 0.8223350253807107 | 0.9695431472081218 | 0.7309644670050761 | 197 | -0.1065989847715736 | [-0.18274111675126903, -0.025380710659898477] | 0.0092 | 0.0276 | False | False |
| sib | native-itrans | sarvam-1 | True | 0.75 | 0.546875 | 0.7578125 | 0.453125 | 256 | -0.1015625 | [-0.1796875, -0.0234375] | 0.0114 | 0.0456 | False | False |
| retrieval | native-itrans | gemma4-e2b | True | 1.0 | 0.44308943089430897 | 1.0 | 0.7723577235772358 | 246 | 0.32926829268292684 | [0.25203252032520324, 0.4024390243902439] | 0.0001 | 0.00030000000000000003 | True | False |
| sentiment | native-itrans | gemma4-e2b | True | 0.9847715736040609 | 0.7563451776649747 | 0.9898477157360406 | 0.817258883248731 | 197 | 0.05583756345177665 | [-0.01015228426395939, 0.12690355329949238] | 0.124 | 0.248 | False | False |
| sib | native-itrans | gemma4-e2b | True | 0.7578125 | 0.375 | 0.7734375 | 0.45703125 | 256 | 0.06640625 | [-0.01171875, 0.14453125] | 0.1032 | 0.3096 | False | False |
| sentiment | native-itrans | qwen3-1.7b | True | 0.8324873096446701 | 0.5329949238578681 | 0.9441624365482234 | 0.6345177664974619 | 197 | -0.01015228426395939 | [-0.1116751269035533, 0.09137055837563451] | 0.8718 | 0.8718 | False | False |
| sib | native-itrans | qwen3-1.7b | True | 0.66796875 | 0.24609375 | 0.66015625 | 0.296875 | 256 | 0.05859375 | [-0.01953125, 0.13671875] | 0.1652 | 0.3304 | False | False |

#### `results/h_hindi/gate.json` (3,933 bytes; first commit 5e44d59 2026-10-23 14:17:52 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 (H-Hindi)"
provenance.config.rule = "fixed before data"
provenance.git_commit = "0a6e64ccd76dc32bbfd1145d74bf3e7f89047266-dirty"
provenance.timestamp_utc = "2026-10-22T22:49:46+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h_hindi.py", "gate"]
qwen2.5-1.5b.sentiment.n = 200
qwen2.5-1.5b.sentiment.acc = 0.895
qwen2.5-1.5b.sentiment.ci = [0.85, 0.935]
qwen2.5-1.5b.sentiment.chance = 0.5
qwen2.5-1.5b.sentiment.above_chance = true
qwen2.5-1.5b.sib.n = 1004
qwen2.5-1.5b.sib.acc = 0.6603585657370518
qwen2.5-1.5b.sib.ci = [0.6314741035856574, 0.6902390438247012]
qwen2.5-1.5b.sib.chance = 0.14285714285714285
qwen2.5-1.5b.sib.above_chance = true
qwen2.5-1.5b.retrieval.n_test = 248
qwen2.5-1.5b.retrieval.unmapped_test = 0.6975806451612904
qwen2.5-1.5b.retrieval.ci = [0.6410282254219055, 0.7540322542190552]
qwen2.5-1.5b.counts_accuracy = true
qwen2.5-1.5b.counts_retrieval = true
qwen2.5-1.5b.counted_h1_accuracy = false
qwen2.5-1.5b.counted_h1_retrieval = false
qwen3.5-2b.sentiment.n = 200
qwen3.5-2b.sentiment.acc = 0.925
qwen3.5-2b.sentiment.ci = [0.885, 0.96]
qwen3.5-2b.sentiment.chance = 0.5
qwen3.5-2b.sentiment.above_chance = true
qwen3.5-2b.sib.n = 1004
qwen3.5-2b.sib.acc = 0.7191235059760956
qwen3.5-2b.sib.ci = [0.6902390438247012, 0.7470119521912351]
qwen3.5-2b.sib.chance = 0.14285714285714285
qwen3.5-2b.sib.above_chance = true
qwen3.5-2b.retrieval.n_test = 248
qwen3.5-2b.retrieval.unmapped_test = 0.9919354838709677
qwen3.5-2b.retrieval.ci = [0.9798387289047241, 1.0]
qwen3.5-2b.counts_accuracy = true
qwen3.5-2b.counts_retrieval = true
qwen3.5-2b.counted_h1_accuracy = true
qwen3.5-2b.counted_h1_retrieval = true
sarvam-1.sentiment.n = 200
sarvam-1.sentiment.acc = 0.97
sarvam-1.sentiment.ci = [0.945, 0.99]
sarvam-1.sentiment.chance = 0.5
sarvam-1.sentiment.above_chance = true
sarvam-1.sib.n = 1004
sarvam-1.sib.acc = 0.7808764940239044
sarvam-1.sib.ci = [0.7559760956175299, 0.8057768924302788]
sarvam-1.sib.chance = 0.14285714285714285
sarvam-1.sib.above_chance = true
sarvam-1.retrieval.n_test = 248
sarvam-1.retrieval.unmapped_test = 0.9919354838709677
sarvam-1.retrieval.ci = [0.9798387289047241, 1.0]
sarvam-1.counts_accuracy = true
sarvam-1.counts_retrieval = true
sarvam-1.counted_h1_accuracy = true
sarvam-1.counted_h1_retrieval = true
gemma4-e2b.sentiment.n = 200
gemma4-e2b.sentiment.acc = 0.99
gemma4-e2b.sentiment.ci = [0.975, 1.0]
gemma4-e2b.sentiment.chance = 0.5
gemma4-e2b.sentiment.above_chance = true
gemma4-e2b.sib.n = 1004
gemma4-e2b.sib.acc = 0.7739043824701195
gemma4-e2b.sib.ci = [0.74800796812749, 0.798804780876494]
gemma4-e2b.sib.chance = 0.14285714285714285
gemma4-e2b.sib.above_chance = true
gemma4-e2b.retrieval.n_test = 248
gemma4-e2b.retrieval.unmapped_test = 1.0
gemma4-e2b.retrieval.ci = [1.0, 1.0]
gemma4-e2b.counts_accuracy = true
gemma4-e2b.counts_retrieval = true
gemma4-e2b.counted_h1_accuracy = true
gemma4-e2b.counted_h1_retrieval = true
qwen3-1.7b.sentiment.n = 200
qwen3-1.7b.sentiment.acc = 0.945
qwen3-1.7b.sentiment.ci = [0.91, 0.975]
qwen3-1.7b.sentiment.chance = 0.5
qwen3-1.7b.sentiment.above_chance = true
qwen3-1.7b.sib.n = 1004
qwen3-1.7b.sib.acc = 0.6912350597609562
qwen3-1.7b.sib.ci = [0.6623256972111554, 0.7191235059760956]
qwen3-1.7b.sib.chance = 0.14285714285714285
qwen3-1.7b.sib.above_chance = true
qwen3-1.7b.retrieval.n_test = 248
qwen3-1.7b.retrieval.unmapped_test = 0.8709677419354839
qwen3-1.7b.retrieval.ci = [0.8266128897666931, 0.9112903475761414]
qwen3-1.7b.counts_accuracy = true
qwen3-1.7b.counts_retrieval = true
qwen3-1.7b.counted_h1_accuracy = true
qwen3-1.7b.counted_h1_retrieval = false
`````

#### `results/h_hindi/h1.csv` (2,740 bytes; first commit 5e44d59 2026-10-23 14:17:52 +0530)

| measure | comparison | model | counted | kannada_native | kannada_other | hindi_native | hindi_other | n | diff_of_gaps | ci | p | p_holm | positive | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | native-natural | qwen2.5-1.5b | False | 0.24390243902439024 | 0.37398373983739835 | 0.6951219512195121 | 0.3943089430894309 | 246 | -0.43089430894308944 | [-0.524390243902439, -0.3333333333333333] | 0.0001 |  | False | False |
| sentiment | native-natural | qwen2.5-1.5b | False | 0.700507614213198 | 0.5177664974619289 | 0.8934010152284264 | 0.766497461928934 | 197 | 0.05583756345177665 | [-0.04568527918781726, 0.15736040609137056] | 0.3252 |  | False | False |
| sib | native-natural | qwen2.5-1.5b | False | 0.32421875 | 0.45703125 | 0.66015625 | 0.58203125 | 256 | -0.2109375 | [-0.296875, -0.125] | 0.0001 |  | False | False |
| retrieval | native-natural | qwen3.5-2b | True | 1.0 | 0.516260162601626 | 0.991869918699187 | 0.9471544715447154 | 246 | 0.43902439024390244 | [0.3699186991869919, 0.508130081300813] | 0.0001 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | qwen3.5-2b | True | 0.7360406091370558 | 0.7208121827411168 | 0.9238578680203046 | 0.9441624365482234 | 197 | 0.03553299492385787 | [-0.04568527918781726, 0.1218274111675127] | 0.4258 | 0.4258 | False | False |
| sib | native-natural | qwen3.5-2b | True | 0.69921875 | 0.45703125 | 0.72265625 | 0.6328125 | 256 | 0.15234375 | [0.08203125, 0.22265625] | 0.0001 | 0.0004 | True | False |
| retrieval | native-natural | sarvam-1 | True | 0.9878048780487805 | 0.9186991869918699 | 0.991869918699187 | 0.9390243902439024 | 246 | 0.016260162601626018 | [-0.012195121951219513, 0.044715447154471545] | 0.311 | 0.311 | False | False |
| sentiment | native-natural | sarvam-1 | True | 0.9543147208121827 | 0.8934010152284264 | 0.9695431472081218 | 0.9644670050761421 | 197 | 0.05583756345177665 | [0.01015228426395939, 0.1065989847715736] | 0.0288 | 0.0576 | False | True |
| sib | native-natural | sarvam-1 | True | 0.75 | 0.7265625 | 0.7578125 | 0.72265625 | 256 | -0.01171875 | [-0.07421875, 0.05078125] | 0.7716 | 0.7716 | False | False |
| retrieval | native-natural | gemma4-e2b | True | 1.0 | 0.7113821138211383 | 1.0 | 0.9796747967479674 | 246 | 0.2682926829268293 | [0.2073170731707317, 0.32926829268292684] | 0.0001 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | gemma4-e2b | True | 0.9847715736040609 | 0.8020304568527918 | 0.9898477157360406 | 0.9898477157360406 | 197 | 0.18274111675126903 | [0.1218274111675127, 0.2436548223350254] | 0.0001 | 0.0004 | True | False |
| sib | native-natural | gemma4-e2b | True | 0.7578125 | 0.54296875 | 0.7734375 | 0.734375 | 256 | 0.17578125 | [0.1015625, 0.24609375] | 0.0001 | 0.0004 | True | False |
| sentiment | native-natural | qwen3-1.7b | True | 0.8324873096446701 | 0.5583756345177665 | 0.9441624365482234 | 0.8781725888324873 | 197 | 0.20812182741116753 | [0.1065989847715736, 0.3096446700507614] | 0.0004 | 0.0012000000000000001 | True | False |
| sib | native-natural | qwen3-1.7b | True | 0.66796875 | 0.37109375 | 0.66015625 | 0.53125 | 256 | 0.16796875 | [0.0859375, 0.25] | 0.0002 | 0.0004 | True | False |

#### `results/h_hindi/h1_loanfree.csv` (2,746 bytes; first commit 5e44d59 2026-10-23 14:17:52 +0530)

| measure | comparison | model | counted | kannada_native | kannada_other | hindi_native | hindi_other | n | diff_of_gaps | ci | p | p_holm | positive | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | native-natural | qwen2.5-1.5b | False | 0.2926829268292683 | 0.24390243902439024 | 0.6829268292682927 | 0.36585365853658536 | 41 | -0.2682926829268293 | [-0.4878048780487805, -0.04878048780487805] | 0.0184 |  | False | False |
| sentiment | native-natural | qwen2.5-1.5b | False | 0.8333333333333334 | 0.16666666666666666 | 0.6666666666666666 | 0.5 | 6 | 0.5 | [0.16666666666666666, 0.8333333333333334] | 0.0308 |  | False | False |
| sib | native-natural | qwen2.5-1.5b | False | 0.16129032258064516 | 0.25806451612903225 | 0.5483870967741935 | 0.3870967741935484 | 31 | -0.25806451612903225 | [-0.4838709677419355, -0.03225806451612903] | 0.0448 |  | False | False |
| retrieval | native-natural | qwen3.5-2b | True | 0.9024390243902439 | 0.6341463414634146 | 0.9512195121951219 | 0.8780487804878049 | 41 | 0.1951219512195122 | [0.024390243902439025, 0.36585365853658536] | 0.0304 | 0.0608 | False | True |
| sentiment | native-natural | qwen3.5-2b | True | 1.0 | 0.8333333333333334 | 0.8333333333333334 | 0.8333333333333334 | 6 | 0.16666666666666666 | [0.0, 0.5] | 0.6684 | 1.0 | False | False |
| sib | native-natural | qwen3.5-2b | True | 0.6451612903225806 | 0.25806451612903225 | 0.8064516129032258 | 0.6451612903225806 | 31 | 0.22580645161290322 | [0.0, 0.41935483870967744] | 0.0526 | 0.1578 | False | False |
| retrieval | native-natural | sarvam-1 | True | 1.0 | 0.9024390243902439 | 0.975609756097561 | 0.9512195121951219 | 41 | 0.07317073170731707 | [-0.024390243902439025, 0.17073170731707318] | 0.2396 | 0.2396 | False | False |
| sentiment | native-natural | sarvam-1 | True | 1.0 | 0.8333333333333334 | 1.0 | 0.6666666666666666 | 6 | -0.16666666666666666 | [-0.5, 0.0] | 0.6708 | 1.0 | False | False |
| sib | native-natural | sarvam-1 | True | 0.7741935483870968 | 0.6774193548387096 | 0.6774193548387096 | 0.6129032258064516 | 31 | 0.03225806451612903 | [-0.12903225806451613, 0.22580645161290322] | 0.8866 | 0.8866 | False | False |
| retrieval | native-natural | gemma4-e2b | True | 1.0 | 0.8292682926829268 | 1.0 | 1.0 | 41 | 0.17073170731707318 | [0.07317073170731707, 0.2926829268292683] | 0.001 | 0.003 | True | False |
| sentiment | native-natural | gemma4-e2b | True | 1.0 | 0.8333333333333334 | 1.0 | 1.0 | 6 | 0.16666666666666666 | [0.0, 0.5] | 0.6684 | 1.0 | False | False |
| sib | native-natural | gemma4-e2b | True | 0.7741935483870968 | 0.41935483870967744 | 0.7419354838709677 | 0.7419354838709677 | 31 | 0.3548387096774194 | [0.12903225806451613, 0.5483870967741935] | 0.0014 | 0.0056 | True | False |
| sentiment | native-natural | qwen3-1.7b | True | 0.8333333333333334 | 0.16666666666666666 | 0.8333333333333334 | 0.6666666666666666 | 6 | 0.5 | [0.16666666666666666, 0.8333333333333334] | 0.0318 | 0.1272 | False | True |
| sib | native-natural | qwen3-1.7b | True | 0.5483870967741935 | 0.25806451612903225 | 0.5806451612903226 | 0.41935483870967744 | 31 | 0.12903225806451613 | [-0.0967741935483871, 0.3548387096774194] | 0.3016 | 0.6032 | False | False |

#### `results/h_hindi/h1_secondary.json` (2,603 bytes; first commit 5e44d59 2026-10-23 14:17:52 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 12:05 addendum, item 3"
provenance.config.status = "secondary, no separate verdict"
provenance.config.wordlist = "wordfreq en best, Zipf >= 3, words longer than 3 characters, lowercased"
provenance.git_commit = "7b4e869de00e422b1e17f26c6eec9b44b3cc70c7-dirty"
provenance.timestamp_utc = "2026-10-23T08:45:39+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h_hindi.py", "analyse"]
english_word_share.retrieval.n = 493
english_word_share.retrieval.kannada_share = 0.0642749235949141
english_word_share.retrieval.hindi_share = 0.10443818172343591
english_word_share.retrieval.hindi_minus_kannada = 0.04016325812852181
english_word_share.retrieval.ci = [0.03140249825517279, 0.04883893877081539]
english_word_share.retrieval.n_english_free_both = 67
english_word_share.sentiment.n = 197
english_word_share.sentiment.kannada_share = 0.07262916104660293
english_word_share.sentiment.hindi_share = 0.1781649191615365
english_word_share.sentiment.hindi_minus_kannada = 0.10553575811493358
english_word_share.sentiment.ci = [0.08946535560558928, 0.12197336722918936]
english_word_share.sentiment.n_english_free_both = 6
english_word_share.sib.n = 256
english_word_share.sib.kannada_share = 0.06906919966325174
english_word_share.sib.hindi_share = 0.11919288958197771
english_word_share.sib.hindi_minus_kannada = 0.05012368991872598
english_word_share.sib.ci = [0.03702615893214939, 0.06313080178208379]
english_word_share.sib.n_english_free_both = 31
loan_free_h1.retrieval.n_counted = 3
loan_free_h1.retrieval.needed = 2
loan_free_h1.retrieval.n_positive = 1
loan_free_h1.retrieval.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
loan_free_h1.retrieval.n_items = 41
loan_free_h1.retrieval.ci_holm_disagreements = ["qwen3.5-2b"]
loan_free_h1.retrieval.rule_outcome_descriptive = "refuted"
loan_free_h1.retrieval.flag = "possibly driven by English loans"
loan_free_h1.sentiment.n_counted = 4
loan_free_h1.sentiment.needed = 3
loan_free_h1.sentiment.n_positive = 0
loan_free_h1.sentiment.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
loan_free_h1.sentiment.n_items = 6
loan_free_h1.sentiment.ci_holm_disagreements = ["qwen3-1.7b"]
loan_free_h1.sentiment.rule_outcome_descriptive = "refuted"
loan_free_h1.sentiment.flag = null
loan_free_h1.sib.n_counted = 4
loan_free_h1.sib.needed = 3
loan_free_h1.sib.n_positive = 1
loan_free_h1.sib.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
loan_free_h1.sib.n_items = 31
loan_free_h1.sib.rule_outcome_descriptive = "refuted"
loan_free_h1.sib.flag = "possibly driven by English loans"
`````

#### `results/h_hindi/h1_verdict.json` (1,285 bytes; first commit 5e44d59 2026-10-23 14:17:52 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 (H-Hindi + 12:05 addendum)"
provenance.config.n_retrieval_items_D = 493
provenance.git_commit = "7b4e869de00e422b1e17f26c6eec9b44b3cc70c7-dirty"
provenance.timestamp_utc = "2026-10-23T08:44:51+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h_hindi.py", "analyse"]
retrieval.n_counted = 3
retrieval.needed = 2
retrieval.n_positive = 2
retrieval.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
retrieval.n_items = 246
retrieval.verdict = "effect (H1 supported)"
sentiment.n_counted = 4
sentiment.needed = 3
sentiment.n_positive = 2
sentiment.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
sentiment.n_items = 197
sentiment.verdict = "refuted"
sentiment.ci_holm_disagreements = ["sarvam-1"]
sib.n_counted = 4
sib.needed = 3
sib.n_positive = 3
sib.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
sib.n_items = 256
sib.verdict = "effect (H1 supported)"
`````

#### `results/h_hindi/scores/sentiment/cf_gemma4-e2b.json` (264 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sentiment = [-11.390227317810059, -13.233977317810059]
sentiment = [-7.080981731414795, -5.612231731414795]
[MASK].sentiment = [-10.317381858825684, -8.692381858825684]
`````

#### `results/h_hindi/scores/sentiment/cf_qwen2.5-1.5b.json` (262 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sentiment = [-1.862534523010254, -9.612534523010254]
sentiment = [-2.3190255165100098, -4.44402551651001]
[MASK].sentiment = [-1.3718047142028809, -2.621804714202881]
`````

#### `results/h_hindi/scores/sentiment/cf_qwen3-1.7b.json` (264 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sentiment = [-1.7947381734848022, -4.294738292694092]
sentiment = [-3.698035717010498, -3.698035717010498]
[MASK].sentiment = [-1.9486875534057617, -3.8236875534057617]
`````

#### `results/h_hindi/scores/sentiment/cf_qwen3.5-2b.json` (261 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sentiment = [-3.836883068084717, -3.586883068084717]
sentiment = [-3.79923677444458, -4.04923677444458]
[MASK].sentiment = [-3.8607988357543945, -3.4857988357543945]
`````

#### `results/h_hindi/scores/sentiment/cf_sarvam-1.json` (262 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sentiment = [-8.01157283782959, -9.63657283782959]
sentiment = [-1.5957965850830078, -2.095796585083008]
[MASK].sentiment = [-1.8119052648544312, -2.3119053840637207]
`````

#### `results/h_hindi/scores/sentiment/gemma4-e2b__itrans.json` (309 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sentiment"
fertility[0].form = "itrans"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.4185005594927267
seconds = 43.68393063545227
`````

#### `results/h_hindi/scores/sentiment/gemma4-e2b__lossy.json` (309 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sentiment"
fertility[0].form = "lossy"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 1.8789630734800447
seconds = 51.557610750198364
`````

#### `results/h_hindi/scores/sentiment/gemma4-e2b__native.json` (309 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sentiment"
fertility[0].form = "native"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 1.3817605371130175
seconds = 43.32610464096069
`````

#### `results/h_hindi/scores/sentiment/gemma4-e2b__natural.json` (311 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-11.390227317810059, -13.233977317810059]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sentiment"
fertility[0].form = "natural"
fertility[0].n_texts = 199
fertility[0].tokens_per_word = 1.5162677636499626
seconds = 1295.8050136566162
`````

#### `results/h_hindi/scores/sentiment/qwen2.5-1.5b__itrans.json` (309 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sentiment"
fertility[0].form = "itrans"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.601454681089146
seconds = 17.582542181015015
`````

#### `results/h_hindi/scores/sentiment/qwen2.5-1.5b__lossy.json` (309 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sentiment"
fertility[0].form = "lossy"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.1186124580380454
seconds = 16.752504348754883
`````

#### `results/h_hindi/scores/sentiment/qwen2.5-1.5b__native.json` (308 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sentiment"
fertility[0].form = "native"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 4.73591943304737
seconds = 21.202560424804688
`````

#### `results/h_hindi/scores/sentiment/qwen2.5-1.5b__natural.json` (310 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.862534523010254, -9.612534523010254]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sentiment"
fertility[0].form = "natural"
fertility[0].n_texts = 199
fertility[0].tokens_per_word = 1.8044128646222888
seconds = 38.27434802055359
`````

#### `results/h_hindi/scores/sentiment/qwen3-1.7b__itrans.json` (308 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sentiment"
fertility[0].form = "itrans"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.601454681089146
seconds = 22.288427591323853
`````

#### `results/h_hindi/scores/sentiment/qwen3-1.7b__lossy.json` (307 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sentiment"
fertility[0].form = "lossy"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.1186124580380454
seconds = 23.76427912712097
`````

#### `results/h_hindi/scores/sentiment/qwen3-1.7b__native.json` (306 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sentiment"
fertility[0].form = "native"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 4.73591943304737
seconds = 26.49006986618042
`````

#### `results/h_hindi/scores/sentiment/qwen3-1.7b__natural.json` (310 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-1.7947381734848022, -4.294738292694092]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sentiment"
fertility[0].form = "natural"
fertility[0].n_texts = 199
fertility[0].tokens_per_word = 1.8044128646222888
seconds = 18.085410833358765
`````

#### `results/h_hindi/scores/sentiment/qwen3.5-2b__itrans.json` (307 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sentiment"
fertility[0].form = "itrans"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.5225662066393135
seconds = 77.88773083686829
`````

#### `results/h_hindi/scores/sentiment/qwen3.5-2b__lossy.json` (305 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sentiment"
fertility[0].form = "lossy"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 1.991048116374487
seconds = 68.04694366455078
`````

#### `results/h_hindi/scores/sentiment/qwen3.5-2b__native.json` (307 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sentiment"
fertility[0].form = "native"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.1840731070496084
seconds = 71.25917148590088
`````

#### `results/h_hindi/scores/sentiment/qwen3.5-2b__natural.json` (306 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-3.836883068084717, -3.586883068084717]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sentiment"
fertility[0].form = "natural"
fertility[0].n_texts = 199
fertility[0].tokens_per_word = 1.730179506357517
seconds = 77.1780149936676
`````

#### `results/h_hindi/scores/sentiment/sarvam-1__itrans.json` (304 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "sentiment"
fertility[0].form = "itrans"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 3.2588586348377473
seconds = 29.022637367248535
`````

#### `results/h_hindi/scores/sentiment/sarvam-1__lossy.json` (303 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "sentiment"
fertility[0].form = "lossy"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 2.6879895561357703
seconds = 27.188088178634644
`````

#### `results/h_hindi/scores/sentiment/sarvam-1__native.json` (303 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "sentiment"
fertility[0].form = "native"
fertility[0].n_texts = 200
fertility[0].tokens_per_word = 1.4571055576277507
seconds = 22.49263858795166
`````

#### `results/h_hindi/scores/sentiment/sarvam-1__natural.json` (304 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sentiment = [-8.01157283782959, -9.63657283782959]
fertility[0].model = "sarvam-1"
fertility[0].task = "sentiment"
fertility[0].form = "natural"
fertility[0].n_texts = 199
fertility[0].tokens_per_word = 2.3272251308900525
seconds = 39.74878239631653
`````

#### `results/h_hindi/scores/sib/cf_gemma4-e2b.json` (612 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
sib = [-2.4877829551696777, -3.8627829551696777, -5.550282955169678, -8.675283432006836, -5.550282955169678, -9.237783432006836, -5.675282955169678]
[MASK].sib = [-0.5948385000228882, -3.2198386192321777, -3.9698386192321777, -8.46983814239502, -4.094838619232178, -4.594838619232178, -4.844838619232178]
`````

#### `results/h_hindi/scores/sib/cf_qwen2.5-1.5b.json` (605 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
sib = [-2.681217670440674, -5.681217670440674, -7.056217670440674, -6.806217670440674, -3.931217670440674, -6.181217670440674, -1.4312175512313843]
[MASK].sib = [-3.935457706451416, -4.685457706451416, -4.435457706451416, -6.810457706451416, -2.435457706451416, -5.560457706451416, -0.310457706451416]
`````

#### `results/h_hindi/scores/sib/cf_qwen3-1.7b.json` (607 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
sib = [-0.616732656955719, -7.866732597351074, -5.616732597351074, -5.491732597351074, -8.116732597351074, -3.991732597351074, -4.741732597351074]
[MASK].sib = [-0.1491338461637497, -8.274133682250977, -3.6491339206695557, -3.1491339206695557, -5.649133682250977, -3.6491339206695557, -5.024133682250977]
`````

#### `results/h_hindi/scores/sib/cf_qwen3.5-2b.json` (614 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
sib = [-2.0323567390441895, -2.5323567390441895, -4.0948567390441895, -3.4073567390441895, -3.5948567390441895, -4.1573567390441895, -1.282356858253479]
[MASK].sib = [-2.0298879146575928, -2.7798879146575928, -4.279888153076172, -3.2798879146575928, -3.2798879146575928, -4.342388153076172, -1.9048879146575928]
`````

#### `results/h_hindi/scores/sib/cf_sarvam-1.json` (604 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
N/A.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
sib = [-1.7176564931869507, -3.2176566123962402, -3.7176566123962402, -4.71765661239624, -3.4676566123962402, -5.468843460083008, -0.9693723320960999]
[MASK].sib = [-1.23140287399292, -2.98140287399292, -3.73140287399292, -4.73140287399292, -3.48140287399292, -4.849200248718262, -1.0999197959899902]
`````

#### `results/h_hindi/scores/sib/gemma4-e2b__itrans.json` (419 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.5244032775204843
seconds = 790.34343791008
`````

#### `results/h_hindi/scores/sib/gemma4-e2b__lossy.json` (419 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.902109804852947
seconds = 750.2275288105011
`````

#### `results/h_hindi/scores/sib/gemma4-e2b__native.json` (421 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.3900170209397142
seconds = 778.6934289932251
`````

#### `results/h_hindi/scores/sib/gemma4-e2b__natural.json` (421 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "natural"
fertility[0].n_texts = 256
fertility[0].tokens_per_word = 1.6679162761636988
seconds = 505.0973813533783
`````

#### `results/h_hindi/scores/sib/qwen2.5-1.5b__itrans.json` (418 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.727150378023196
seconds = 576.8840198516846
`````

#### `results/h_hindi/scores/sib/qwen2.5-1.5b__lossy.json` (417 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.153465542492974
seconds = 584.7312669754028
`````

#### `results/h_hindi/scores/sib/qwen2.5-1.5b__native.json` (418 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.778252780746547
seconds = 430.9101495742798
`````

#### `results/h_hindi/scores/sib/qwen2.5-1.5b__natural.json` (418 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-4.905157566070557, -6.530157566070557, -6.655157566070557, -8.280158042907715, -5.655157566070557, -5.530157566070557, -0.9051576852798462]
fertility[0].model = "qwen2.5-1.5b"
fertility[0].task = "sib"
fertility[0].form = "natural"
fertility[0].n_texts = 256
fertility[0].tokens_per_word = 1.972352389878163
seconds = 158.2754044532776
`````

#### `results/h_hindi/scores/sib/qwen3-1.7b__itrans.json` (416 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.727150378023196
seconds = 371.53632640838623
`````

#### `results/h_hindi/scores/sib/qwen3-1.7b__lossy.json` (413 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.153465542492974
seconds = 362.024210691452
`````

#### `results/h_hindi/scores/sib/qwen3-1.7b__native.json` (415 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 4.778252780746547
seconds = 458.5777952671051
`````

#### `results/h_hindi/scores/sib/qwen3-1.7b__natural.json` (415 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "natural"
fertility[0].n_texts = 256
fertility[0].tokens_per_word = 1.972352389878163
seconds = 83.32775568962097
`````

#### `results/h_hindi/scores/sib/qwen3.5-2b__itrans.json` (417 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.6307643589439103
seconds = 1146.1717410087585
`````

#### `results/h_hindi/scores/sib/qwen3.5-2b__lossy.json` (415 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.0233938962118514
seconds = 729.2934546470642
`````

#### `results/h_hindi/scores/sib/qwen3.5-2b__native.json` (417 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.1780469461267464
seconds = 1319.3230752944946
`````

#### `results/h_hindi/scores/sib/qwen3.5-2b__natural.json` (416 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "natural"
fertility[0].n_texts = 256
fertility[0].tokens_per_word = 1.8812870977819431
seconds = 362.1070258617401
`````

#### `results/h_hindi/scores/sib/sarvam-1__itrans.json` (415 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "itrans"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 3.2867830423940148
seconds = 498.7073414325714
`````

#### `results/h_hindi/scores/sib/sarvam-1__lossy.json` (413 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "lossy"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 2.669675018802201
seconds = 495.8556499481201
`````

#### `results/h_hindi/scores/sib/sarvam-1__native.json` (415 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "native"
fertility[0].n_texts = 1004
fertility[0].tokens_per_word = 1.398052487828049
seconds = 424.09565591812134
`````

#### `results/h_hindi/scores/sib/sarvam-1__natural.json` (416 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "natural"
fertility[0].n_texts = 256
fertility[0].tokens_per_word = 2.5048422368009997
seconds = 310.09715461730957
`````

#### `results/h_hindi/tokens_per_word.csv` (3,354 bytes; first commit 5e44d59 2026-10-23 14:17:52 +0530)

| language | model | dataset | form | n_texts | tokens_per_word |
|---|---|---|---|---|---|
| hindi | qwen2.5-1.5b | m4c496 | native | 496 | 4.707180104292018 |
| hindi | qwen2.5-1.5b | m4c496 | itrans | 496 | 2.693140794223827 |
| hindi | qwen2.5-1.5b | m4c496 | lossy | 496 | 2.123144805455275 |
| hindi | qwen2.5-1.5b | m4c496 | natural | 493 | 1.9835364377370672 |
| hindi | qwen2.5-1.5b | sentiment | native | 200 | 4.73591943304737 |
| hindi | qwen2.5-1.5b | sentiment | itrans | 200 | 2.601454681089146 |
| hindi | qwen2.5-1.5b | sentiment | lossy | 200 | 2.1186124580380454 |
| hindi | qwen2.5-1.5b | sentiment | natural | 199 | 1.8044128646222888 |
| hindi | qwen2.5-1.5b | sib | native | 1004 | 4.778252780746547 |
| hindi | qwen2.5-1.5b | sib | itrans | 1004 | 2.727150378023196 |
| hindi | qwen2.5-1.5b | sib | lossy | 1004 | 2.153465542492974 |
| hindi | qwen2.5-1.5b | sib257 | natural | 256 | 1.972352389878163 |
| hindi | qwen3.5-2b | m4c496 | native | 496 | 2.1369434416365825 |
| hindi | qwen3.5-2b | m4c496 | itrans | 496 | 2.599197753710389 |
| hindi | qwen3.5-2b | m4c496 | lossy | 496 | 1.9958283192940232 |
| hindi | qwen3.5-2b | m4c496 | natural | 493 | 1.8911306593495278 |
| hindi | qwen3.5-2b | sentiment | native | 200 | 2.1840731070496084 |
| hindi | qwen3.5-2b | sentiment | itrans | 200 | 2.5225662066393135 |
| hindi | qwen3.5-2b | sentiment | lossy | 200 | 1.991048116374487 |
| hindi | qwen3.5-2b | sentiment | natural | 199 | 1.730179506357517 |
| hindi | qwen3.5-2b | sib | native | 1004 | 2.1780469461267464 |
| hindi | qwen3.5-2b | sib | itrans | 1004 | 2.6307643589439103 |
| hindi | qwen3.5-2b | sib | lossy | 1004 | 2.0233938962118514 |
| hindi | qwen3.5-2b | sib257 | natural | 256 | 1.8812870977819431 |
| hindi | sarvam-1 | m4c496 | native | 496 | 1.3853991175290814 |
| hindi | sarvam-1 | m4c496 | itrans | 496 | 3.243321299638989 |
| hindi | sarvam-1 | m4c496 | lossy | 496 | 2.6337745687926195 |
| hindi | sarvam-1 | m4c496 | natural | 493 | 2.5171495440238885 |
| hindi | sarvam-1 | sentiment | native | 200 | 1.4571055576277507 |
| hindi | sarvam-1 | sentiment | itrans | 200 | 3.2588586348377473 |
| hindi | sarvam-1 | sentiment | lossy | 200 | 2.6879895561357703 |
| hindi | sarvam-1 | sentiment | natural | 199 | 2.3272251308900525 |
| hindi | sarvam-1 | sib | native | 1004 | 1.398052487828049 |
| hindi | sarvam-1 | sib | itrans | 1004 | 3.2867830423940148 |
| hindi | sarvam-1 | sib | lossy | 1004 | 2.669675018802201 |
| hindi | sarvam-1 | sib257 | natural | 256 | 2.5048422368009997 |
| hindi | gemma4-e2b | m4c496 | native | 496 | 1.377055756117128 |
| hindi | gemma4-e2b | m4c496 | itrans | 496 | 2.491295627757722 |
| hindi | gemma4-e2b | m4c496 | lossy | 496 | 1.8658644203770558 |
| hindi | gemma4-e2b | m4c496 | natural | 493 | 1.6747639415704947 |
| hindi | gemma4-e2b | sentiment | native | 200 | 1.3817605371130175 |
| hindi | gemma4-e2b | sentiment | itrans | 200 | 2.4185005594927267 |
| hindi | gemma4-e2b | sentiment | lossy | 200 | 1.8789630734800447 |
| hindi | gemma4-e2b | sentiment | natural | 199 | 1.5162677636499626 |
| hindi | gemma4-e2b | sib | native | 1004 | 1.3900170209397142 |
| hindi | gemma4-e2b | sib | itrans | 1004 | 2.5244032775204843 |
| hindi | gemma4-e2b | sib | lossy | 1004 | 1.902109804852947 |
| hindi | gemma4-e2b | sib257 | natural | 256 | 1.6679162761636988 |
| hindi | qwen3-1.7b | m4c496 | native | 496 | 4.707180104292018 |
| hindi | qwen3-1.7b | m4c496 | itrans | 496 | 2.693140794223827 |
| hindi | qwen3-1.7b | m4c496 | lossy | 496 | 2.123144805455275 |
| hindi | qwen3-1.7b | m4c496 | natural | 493 | 1.9835364377370672 |
| hindi | qwen3-1.7b | sentiment | native | 200 | 4.73591943304737 |
| hindi | qwen3-1.7b | sentiment | itrans | 200 | 2.601454681089146 |
| hindi | qwen3-1.7b | sentiment | lossy | 200 | 2.1186124580380454 |
| hindi | qwen3-1.7b | sentiment | natural | 199 | 1.8044128646222888 |
| hindi | qwen3-1.7b | sib | native | 1004 | 4.778252780746547 |
| hindi | qwen3-1.7b | sib | itrans | 1004 | 2.727150378023196 |
| hindi | qwen3-1.7b | sib | lossy | 1004 | 2.153465542492974 |
| hindi | qwen3-1.7b | sib257 | natural | 256 | 1.972352389878163 |

#### `results/h1lf/h1_loanfree_v2_posthoc.csv` (2,962 bytes; first commit 7443e57 2026-10-23 16:12:55 +0530)

| measure | comparison | model | counted | kannada_native | kannada_other | hindi_native | hindi_other | n | diff_of_gaps | ci | p | p_holm | positive | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | native-natural | qwen2.5-1.5b | False | 0.26804123711340205 | 0.26804123711340205 | 0.5979381443298969 | 0.21649484536082475 | 97 | -0.38144329896907214 | [-0.5360824742268041, -0.2268041237113402] | 0.0001 |  | False | False |
| sentiment | native-natural | qwen2.5-1.5b | False | 0.6190476190476191 | 0.42857142857142855 | 0.7619047619047619 | 0.5238095238095238 | 21 | -0.047619047619047616 | [-0.3333333333333333, 0.23809523809523808] | 0.8608 |  | False | False |
| sib | native-natural | qwen2.5-1.5b | False | 0.24324324324324326 | 0.2702702702702703 | 0.5945945945945946 | 0.4864864864864865 | 74 | -0.13513513513513514 | [-0.3108108108108108, 0.02702702702702703] | 0.119 |  | False | False |
| retrieval | native-natural | qwen3.5-2b | True | 1.0 | 0.422680412371134 | 1.0 | 0.9072164948453608 | 97 | 0.4845360824742268 | [0.38144329896907214, 0.5876288659793815] | 0.0001 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | qwen3.5-2b | True | 0.8095238095238095 | 0.6666666666666666 | 0.8571428571428571 | 0.8571428571428571 | 21 | 0.14285714285714285 | [-0.09523809523809523, 0.38095238095238093] | 0.3356 | 1.0 | False | False |
| sib | native-natural | qwen3.5-2b | True | 0.6486486486486487 | 0.33783783783783783 | 0.7297297297297297 | 0.5675675675675675 | 74 | 0.14864864864864866 | [0.0, 0.2972972972972973] | 0.052 | 0.156 | False | False |
| retrieval | native-natural | sarvam-1 | True | 0.9690721649484536 | 0.9381443298969072 | 0.979381443298969 | 0.9690721649484536 | 97 | 0.020618556701030927 | [-0.020618556701030927, 0.061855670103092786] | 0.462 | 0.462 | False | False |
| sentiment | native-natural | sarvam-1 | True | 0.9047619047619048 | 0.8095238095238095 | 0.9523809523809523 | 0.9047619047619048 | 21 | 0.047619047619047616 | [-0.14285714285714285, 0.23809523809523808] | 0.8328 | 1.0 | False | False |
| sib | native-natural | sarvam-1 | True | 0.7837837837837838 | 0.7027027027027027 | 0.7432432432432432 | 0.6891891891891891 | 74 | 0.02702702702702703 | [-0.12162162162162163, 0.17567567567567569] | 0.7888 | 0.7888 | False | False |
| retrieval | native-natural | gemma4-e2b | True | 1.0 | 0.7319587628865979 | 1.0 | 0.9896907216494846 | 97 | 0.25773195876288657 | [0.16494845360824742, 0.35051546391752575] | 0.0001 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | gemma4-e2b | True | 0.9523809523809523 | 0.7619047619047619 | 1.0 | 0.9047619047619048 | 21 | 0.09523809523809523 | [-0.14285714285714285, 0.3333333333333333] | 0.5912 | 1.0 | False | False |
| sib | native-natural | gemma4-e2b | True | 0.7837837837837838 | 0.43243243243243246 | 0.8108108108108109 | 0.7297297297297297 | 74 | 0.2702702702702703 | [0.10810810810810811, 0.4189189189189189] | 0.0008 | 0.0032 | True | False |
| sentiment | native-natural | qwen3-1.7b | True | 0.6190476190476191 | 0.42857142857142855 | 0.9523809523809523 | 0.7619047619047619 | 21 | 0.0 | [-0.3333333333333333, 0.3333333333333333] | 1.0 | 1.0 | False | False |
| sib | native-natural | qwen3-1.7b | True | 0.6351351351351351 | 0.22972972972972974 | 0.6621621621621622 | 0.40540540540540543 | 74 | 0.14864864864864866 | [0.0, 0.28378378378378377] | 0.056 | 0.156 | False | False |

#### `results/h1lf/itrans_share.json` (1,460 bytes; first commit 5064f46 2026-10-23 15:52:38 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 15:44 IST (exploratory note)"
provenance.config.status = "exploratory, no verdict"
provenance.git_commit = "6fa02b35dadb0e7f7d7e021b9430bfbaca245de2"
provenance.timestamp_utc = "2026-10-23T10:17:08+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf.py", "itrans"]
retrieval.n = 246
retrieval.kannada_itrans_share = 0.017770625679426555
retrieval.hindi_itrans_share = 0.06668995841147284
retrieval.hindi_minus_kannada = 0.04891933273204628
retrieval.ci = [0.04118246274619258, 0.05674794844815665]
retrieval.items_with_any_english_kannada = 55
retrieval.items_with_any_english_hindi = 187
sentiment.n = 197
sentiment.kannada_itrans_share = 0.013313736104598857
sentiment.hindi_itrans_share = 0.06614848390463042
sentiment.hindi_minus_kannada = 0.052834747800031556
sentiment.ci = [0.04448494126764333, 0.061094431725147336]
sentiment.items_with_any_english_kannada = 39
sentiment.items_with_any_english_hindi = 160
sib.n = 256
sib.kannada_itrans_share = 0.018945726736091406
sib.hindi_itrans_share = 0.06928941178436289
sib.hindi_minus_kannada = 0.050343685048271476
sib.ci = [0.042356466074938585, 0.05821973723911247]
sib.items_with_any_english_kannada = 62
sib.items_with_any_english_hindi = 198
`````

#### `results/h1lf/opt1.csv` (2,323 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

| subset | model | n | kannada_native | kannada_natural | hindi_native | hindi_natural | diff_of_gaps | ci | p | p_holm | positive |
|---|---|---|---|---|---|---|---|---|---|---|---|
| loan_free | qwen3-1.7b | 296 | 0.6722972972972973 | 0.26013513513513514 | 0.6790540540540541 | 0.46283783783783783 | 0.19594594594594594 | [0.11486486486486487, 0.27702702702702703] | 0.0001 | 0.0004 | True |
| loan_free | qwen3.5-2b | 296 | 0.6283783783783784 | 0.28040540540540543 | 0.6824324324324325 | 0.5337837837837838 | 0.19932432432432431 | [0.12162162162162163, 0.27702702702702703] | 0.0001 | 0.0004 | True |
| loan_free | sarvam-1 | 296 | 0.7668918918918919 | 0.7331081081081081 | 0.777027027027027 | 0.6959459459459459 | -0.0472972972972973 | [-0.11148648648648649, 0.016891891891891893] | 0.1652 | 0.1652 | False |
| loan_free | gemma4-e2b | 296 | 0.7331081081081081 | 0.4391891891891892 | 0.7635135135135135 | 0.7027027027027027 | 0.23310810810810811 | [0.16216216216216217, 0.30405405405405406] | 0.0001 | 0.0004 | True |
| loan_free_v1 | qwen3-1.7b | 110 | 0.6 | 0.24545454545454545 | 0.6363636363636364 | 0.44545454545454544 | 0.16363636363636364 | [0.045454545454545456, 0.2820454545454512] | 0.013 | 0.026 | True |
| loan_free_v1 | qwen3.5-2b | 110 | 0.5909090909090909 | 0.23636363636363636 | 0.6636363636363637 | 0.5636363636363636 | 0.2545454545454545 | [0.12727272727272726, 0.38181818181818183] | 0.0001 | 0.0004 | True |
| loan_free_v1 | sarvam-1 | 110 | 0.7 | 0.6454545454545455 | 0.6909090909090909 | 0.6090909090909091 | -0.02727272727272727 | [-0.12727272727272726, 0.07272727272727272] | 0.655 | 0.655 | False |
| loan_free_v1 | gemma4-e2b | 110 | 0.6818181818181818 | 0.42727272727272725 | 0.7272727272727273 | 0.6818181818181818 | 0.20909090909090908 | [0.08181818181818182, 0.32727272727272727] | 0.001 | 0.003 | True |
| all_clean | qwen3-1.7b | 985 | 0.6741116751269035 | 0.38578680203045684 | 0.6893401015228426 | 0.5685279187817259 | 0.16751269035532995 | [0.12588832487309645, 0.20913705583756345] | 0.0001 | 0.0004 | True |
| all_clean | qwen3.5-2b | 985 | 0.6781725888324873 | 0.44263959390862945 | 0.7197969543147208 | 0.6335025380710659 | 0.14923857868020304 | [0.10964467005076142, 0.18883248730964466] | 0.0001 | 0.0004 | True |
| all_clean | sarvam-1 | 985 | 0.766497461928934 | 0.7380710659898477 | 0.7807106598984772 | 0.732994923857868 | -0.019289340101522844 | [-0.05078680203045683, 0.013197969543147208] | 0.256 | 0.256 | False |
| all_clean | gemma4-e2b | 985 | 0.7482233502538072 | 0.531979695431472 | 0.7725888324873097 | 0.7258883248730964 | 0.16954314720812183 | [0.13401015228426397, 0.20406091370558377] | 0.0001 | 0.0004 | True |

#### `results/h1lf/opt1_reproduction.json` (1,246 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
provenance.config.rule = "pred_cal agreement >= 0.98 on identical-text overlap"
provenance.git_commit = "126a4882ac1a54c8952472a61cd85e970461447c-dirty"
provenance.timestamp_utc = "2026-10-28T00:07:42+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf.py", "score", "check"]
kannada/qwen3-1.7b.n_identical_text = 257
kannada/qwen3-1.7b.n_overlap = 257
kannada/qwen3-1.7b.agreement = 1.0
kannada/qwen3.5-2b.n_identical_text = 257
kannada/qwen3.5-2b.n_overlap = 257
kannada/qwen3.5-2b.agreement = 1.0
kannada/sarvam-1.n_identical_text = 257
kannada/sarvam-1.n_overlap = 257
kannada/sarvam-1.agreement = 1.0
kannada/gemma4-e2b.n_identical_text = 257
kannada/gemma4-e2b.n_overlap = 257
kannada/gemma4-e2b.agreement = 1.0
hindi/qwen3-1.7b.n_identical_text = 256
hindi/qwen3-1.7b.n_overlap = 493
hindi/qwen3-1.7b.agreement = 1.0
hindi/qwen3.5-2b.n_identical_text = 256
hindi/qwen3.5-2b.n_overlap = 493
hindi/qwen3.5-2b.agreement = 1.0
hindi/sarvam-1.n_identical_text = 256
hindi/sarvam-1.n_overlap = 493
hindi/sarvam-1.agreement = 1.0
hindi/gemma4-e2b.n_identical_text = 256
hindi/gemma4-e2b.n_overlap = 493
hindi/gemma4-e2b.agreement = 1.0
`````

#### `results/h1lf/opt1_verdict.json` (676 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 15:44 IST (H1-LF option 1, follow-up registered post H1)"
provenance.git_commit = "126a4882ac1a54c8952472a61cd85e970461447c-dirty"
provenance.timestamp_utc = "2026-10-28T00:08:04+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf.py", "analyse1"]
loan_definition = "v2"
n_items_loan_free = 296
n_items_loan_free_v1 = 110
n_items_loan_free_v2 = 296
n_items_clean_both = 985
n_positive = 3
needed = 3
verdict = "loan-free effect"
all_clean_descriptive_n_positive = 3
`````

#### `results/h1lf/opt2.csv` (3,705 bytes; first commit 5064f46 2026-10-23 15:52:38 +0530)

| measure | comparison | model | counted | n | intercept | intercept_ci | p | slope | slope_ci | mean_d | mean_delta | frac_delta_le_0 | p_holm | positive | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | native-natural | qwen2.5-1.5b | False | 246 | -0.4764596354760473 | [-0.5703309887757246, -0.3834786066813491] | 0.0001 | 1.4817238546322515 | [0.5492742645423278, 2.514729266589454] | -0.43089430894308944 | 0.03075156439609776 | 0.3983739837398374 |  | False | False |
| sentiment | native-natural | qwen2.5-1.5b | False | 197 | 0.03972009676230391 | [-0.098295356022866, 0.17789009101733425] | 0.5626 | 0.15272043312485645 | [-0.6900967432630928, 0.9347685321392747] | 0.05583756345177665 | 0.10553575811493358 | 0.17258883248730963 |  | False | False |
| sib | native-natural | qwen2.5-1.5b | False | 256 | -0.24956594725069042 | [-0.34062845896637195, -0.1573585249367517] | 0.0001 | 0.7706624814199687 | [0.023068157733446015, 1.477821480318102] | -0.2109375 | 0.05012368991872598 | 0.328125 |  | False | False |
| retrieval | native-natural | qwen3.5-2b | True | 246 | 0.41844718151448557 | [0.34575812021485036, 0.4959915546078536] | 0.0001 | 0.6691434772023502 | [-0.20077900818615865, 1.392265327101491] | 0.43902439024390244 | 0.03075156439609776 | 0.3983739837398374 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | qwen3.5-2b | True | 197 | 0.037129838421535485 | [-0.0713945209882613, 0.15208541463575134] | 0.4982 | -0.015130828888712505 | [-0.797368243238602, 0.750449503733528] | 0.03553299492385787 | 0.10553575811493358 | 0.17258883248730963 | 0.4982 | False | False |
| sib | native-natural | qwen3.5-2b | True | 256 | 0.1505105541683601 | [0.07510654493524827, 0.22572865191928324] | 0.0002 | 0.03657344131312708 | [-0.5958762906142828, 0.644100637566434] | 0.15234375 | 0.05012368991872598 | 0.328125 | 0.0006000000000000001 | True | False |
| retrieval | native-natural | sarvam-1 | True | 246 | 0.012982641687717233 | [-0.013312299169250265, 0.04077866561053541] | 0.336 | 0.1065806237267294 | [-0.17310007099162525, 0.432565815186648] | 0.016260162601626018 | 0.03075156439609776 | 0.3983739837398374 | 0.336 | False | False |
| sentiment | native-natural | sarvam-1 | True | 197 | 0.05417699283764358 | [-0.007145414379490325, 0.11895072817716948] | 0.0816 | 0.015734672719407827 | [-0.25057647823041634, 0.28887186805597925] | 0.05583756345177665 | 0.10553575811493358 | 0.17258883248730963 | 0.1632 | False | False |
| sib | native-natural | sarvam-1 | True | 256 | 0.008617538663087971 | [-0.05881559499772433, 0.07587981135894331] | 0.8138 | -0.40572209859375147 | [-1.1302655377714608, 0.26181484438924546] | -0.01171875 | 0.05012368991872598 | 0.328125 | 0.8138 | False | False |
| retrieval | native-natural | gemma4-e2b | True | 246 | 0.24775279556169733 | [0.18677900080623847, 0.3140738656816757] | 0.0001 | 0.6679298360423701 | [-0.03333074371485695, 1.2864186983066723] | 0.2682926829268293 | 0.03075156439609776 | 0.3983739837398374 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | gemma4-e2b | True | 197 | 0.11615837313271568 | [0.024197870196541977, 0.21537185151491434] | 0.014 | 0.6309022155887817 | [-0.045255598753819876, 1.2147808039645593] | 0.18274111675126903 | 0.10553575811493358 | 0.17258883248730963 | 0.042 | True | False |
| sib | native-natural | gemma4-e2b | True | 256 | 0.16364302520432697 | [0.07786038283429435, 0.2461954078417022] | 0.0002 | 0.24216542747261394 | [-0.3398537275258259, 0.8867681666992515] | 0.17578125 | 0.05012368991872598 | 0.328125 | 0.0006000000000000001 | True | False |
| sentiment | native-natural | qwen3-1.7b | True | 197 | 0.19463252470978368 | [0.04869537697393107, 0.33639916391792846] | 0.0066 | 0.12781736676106814 | [-0.7081198896891855, 1.1196601317600314] | 0.20812182741116753 | 0.10553575811493358 | 0.17258883248730963 | 0.0264 | True | False |
| sib | native-natural | qwen3-1.7b | True | 256 | 0.15623983103008784 | [0.07729797102461314, 0.23893636919776692] | 0.0001 | 0.2339995117863477 | [-0.5134239675271841, 0.9615997953136305] | 0.16796875 | 0.05012368991872598 | 0.328125 | 0.0004 | True | False |

#### `results/h1lf/opt2_sensitivity.csv` (3,209 bytes; first commit 5064f46 2026-10-23 15:52:38 +0530)

| measure | model | outcome | n | intercept | intercept_ci | p | slope | slope_ci | mean_d | mean_delta | frac_delta_le_0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | continuous | 246 | -0.33363965543016344 | [-0.4129772280913068, -0.2603860622280166] | 0.0001 | 0.502637935236411 | [-0.29647098332443284, 1.3274384291693095] | -0.31818275259681933 | 0.03075156439609776 | 0.3983739837398374 |
| sentiment | qwen2.5-1.5b | continuous | 197 | 1.2365155656552824 | [0.1372083208295907, 2.4009043430222268] | 0.0294 | 1.5647224609725248 | [-5.980017278874945, 8.292477543354629] | 1.4016497368134824 | 0.10553575811493358 | 0.17258883248730963 |
| sib | qwen2.5-1.5b | continuous | 256 | -2.048020592312154 | [-2.8332972409487556, -1.3041484578207398] | 0.0001 | 8.851925569071172 | [2.3937175759918943, 16.040494786128825] | -1.6043294199043887 | 0.05012368991872598 | 0.328125 |
| retrieval | qwen3.5-2b | continuous | 246 | 0.1373609827490512 | [0.11986404187313558, 0.15552703963256895] | 0.0001 | 0.4045232665830877 | [0.1701441300322147, 0.6048892980813123] | 0.14980070603110085 | 0.03075156439609776 | 0.3983739837398374 |
| sentiment | qwen3.5-2b | continuous | 197 | 0.3805854292584903 | [0.20370733851516287, 0.555245399540722] | 0.0001 | 0.6309801214279293 | [-0.3278239743089879, 1.7157424478594583] | 0.4471763947288397 | 0.10553575811493358 | 0.17258883248730963 |
| sib | qwen3.5-2b | continuous | 256 | 0.6848835341336774 | [0.39761468358023655, 0.961649657821428] | 0.0001 | 0.9743982783341577 | [-1.8911120653716402, 3.9480010799436047] | 0.7337239712942392 | 0.05012368991872598 | 0.328125 |
| retrieval | sarvam-1 | continuous | 246 | 0.023943635908533396 | [0.005081550197400863, 0.04574972926986177] | 0.0116 | 0.1375556680284754 | [-0.08648615007924307, 0.32630341104886473] | 0.028173687891959304 | 0.03075156439609776 | 0.3983739837398374 |
| sentiment | sarvam-1 | continuous | 197 | 0.6892143092970625 | [0.34512369071398447, 1.033262794364805] | 0.0001 | -0.10943529833110208 | [-1.8830427232693698, 1.649650451779704] | 0.6776649721231557 | 0.10553575811493358 | 0.17258883248730963 |
| sib | sarvam-1 | continuous | 256 | 0.15498492123407714 | [-0.05080049478529854, 0.3585048313011431] | 0.1344 | -0.18222252452881646 | [-2.0224795836099565, 1.636903821590601] | 0.1458512559183873 | 0.05012368991872598 | 0.328125 |
| retrieval | gemma4-e2b | continuous | 246 | 0.15113656619084712 | [0.1311002410681647, 0.1725204298960629] | 0.0001 | 0.2941508322287406 | [-0.0007821402607712672, 0.5503796872411099] | 0.16018216445029498 | 0.03075156439609776 | 0.3983739837398374 |
| sentiment | gemma4-e2b | continuous | 197 | 5.986531896001875 | [4.015429676746328, 7.9520367222974135] | 0.0001 | 5.701304812507294 | [-6.031410323535973, 17.545451234168564] | 6.588223421634151 | 0.10553575811493358 | 0.17258883248730963 |
| sib | gemma4-e2b | continuous | 256 | 4.024855752463022 | [2.4071673112896943, 5.569945084914688] | 0.0001 | 4.695292483660374 | [-8.569940807884207, 20.641260523206046] | 4.260201136991739 | 0.05012368991872598 | 0.328125 |
| sentiment | qwen3-1.7b | continuous | 197 | 2.091173219185518 | [1.1449865746695767, 2.982374741617256] | 0.0001 | 1.0359938846144352 | [-5.224039056975834, 8.397207680795507] | 2.200507619200738 | 0.10553575811493358 | 0.17258883248730963 |
| sib | qwen3-1.7b | continuous | 256 | 3.0371018392856755 | [1.154089012837956, 4.887916586274645] | 0.0004 | 3.476252167687546 | [-10.814795753596702, 19.102711045783856] | 3.211344425018145 | 0.05012368991872598 | 0.328125 |

#### `results/h1lf/opt2_tertiles.csv` (5,035 bytes; first commit 5064f46 2026-10-23 15:52:38 +0530)

| measure | model | tertile | n | delta_min | delta_max | mean_d | ci |
|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | 1 | 82 | -0.48989898989898983 | 0.0 | -0.524390243902439 | [-0.6829268292682927, -0.36585365853658536] |
| retrieval | qwen2.5-1.5b | 2 | 82 | 0.0 | 0.06470588235294117 | -0.5 | [-0.6585365853658537, -0.34146341463414637] |
| retrieval | qwen2.5-1.5b | 3 | 82 | 0.06666666666666667 | 0.375 | -0.2682926829268293 | [-0.43902439024390244, -0.0975609756097561] |
| sentiment | qwen2.5-1.5b | 1 | 66 | -0.18181818181818182 | 0.05555555555555555 | 0.06060606060606061 | [-0.12121212121212122, 0.24242424242424243] |
| sentiment | qwen2.5-1.5b | 2 | 65 | 0.05681818181818182 | 0.13793103448275862 | 0.1076923076923077 | [-0.07692307692307693, 0.27692307692307694] |
| sentiment | qwen2.5-1.5b | 3 | 66 | 0.13793103448275862 | 0.625 | 0.0 | [-0.18181818181818182, 0.16666666666666666] |
| sib | qwen2.5-1.5b | 1 | 86 | -0.48989898989898983 | 0.0030769230769230743 | -0.26744186046511625 | [-0.4072674418604649, -0.11627906976744186] |
| sib | qwen2.5-1.5b | 2 | 85 | 0.0073710073710073765 | 0.08 | -0.24705882352941178 | [-0.4, -0.09411764705882353] |
| sib | qwen2.5-1.5b | 3 | 85 | 0.08108108108108109 | 0.375 | -0.11764705882352941 | [-0.27058823529411763, 0.03529411764705882] |
| retrieval | qwen3.5-2b | 1 | 82 | -0.48989898989898983 | 0.0 | 0.4024390243902439 | [0.2804878048780488, 0.524390243902439] |
| retrieval | qwen3.5-2b | 2 | 82 | 0.0 | 0.06470588235294117 | 0.5 | [0.3902439024390244, 0.6097560975609756] |
| retrieval | qwen3.5-2b | 3 | 82 | 0.06666666666666667 | 0.375 | 0.4146341463414634 | [0.2926829268292683, 0.5365853658536586] |
| sentiment | qwen3.5-2b | 1 | 66 | -0.18181818181818182 | 0.05555555555555555 | 0.045454545454545456 | [-0.09090909090909091, 0.18181818181818182] |
| sentiment | qwen3.5-2b | 2 | 65 | 0.05681818181818182 | 0.13793103448275862 | 0.046153846153846156 | [-0.09230769230769231, 0.16923076923076924] |
| sentiment | qwen3.5-2b | 3 | 66 | 0.13793103448275862 | 0.625 | 0.015151515151515152 | [-0.15151515151515152, 0.18181818181818182] |
| sib | qwen3.5-2b | 1 | 86 | -0.48989898989898983 | 0.0030769230769230743 | 0.16279069767441862 | [0.03488372093023256, 0.29069767441860467] |
| sib | qwen3.5-2b | 2 | 85 | 0.0073710073710073765 | 0.08 | 0.18823529411764706 | [0.07058823529411765, 0.3058823529411765] |
| sib | qwen3.5-2b | 3 | 85 | 0.08108108108108109 | 0.375 | 0.10588235294117647 | [-0.011764705882352941, 0.2235294117647059] |
| retrieval | sarvam-1 | 1 | 82 | -0.48989898989898983 | 0.0 | 0.024390243902439025 | [0.0, 0.06097560975609756] |
| retrieval | sarvam-1 | 2 | 82 | 0.0 | 0.06470588235294117 | 0.0 | [-0.04878048780487805, 0.04878048780487805] |
| retrieval | sarvam-1 | 3 | 82 | 0.06666666666666667 | 0.375 | 0.024390243902439025 | [-0.036585365853658534, 0.08536585365853659] |
| sentiment | sarvam-1 | 1 | 66 | -0.18181818181818182 | 0.05555555555555555 | 0.06060606060606061 | [-0.030303030303030304, 0.15151515151515152] |
| sentiment | sarvam-1 | 2 | 65 | 0.05681818181818182 | 0.13793103448275862 | 0.046153846153846156 | [-0.03076923076923077, 0.13846153846153847] |
| sentiment | sarvam-1 | 3 | 66 | 0.13793103448275862 | 0.625 | 0.06060606060606061 | [0.0, 0.13636363636363635] |
| sib | sarvam-1 | 1 | 86 | -0.48989898989898983 | 0.0030769230769230743 | 0.05813953488372093 | [-0.03488372093023256, 0.16279069767441862] |
| sib | sarvam-1 | 2 | 85 | 0.0073710073710073765 | 0.08 | -0.08235294117647059 | [-0.21176470588235294, 0.047058823529411764] |
| sib | sarvam-1 | 3 | 85 | 0.08108108108108109 | 0.375 | -0.011764705882352941 | [-0.11764705882352941, 0.09411764705882353] |
| retrieval | gemma4-e2b | 1 | 82 | -0.48989898989898983 | 0.0 | 0.2073170731707317 | [0.10975609756097561, 0.3048780487804878] |
| retrieval | gemma4-e2b | 2 | 82 | 0.0 | 0.06470588235294117 | 0.34146341463414637 | [0.24390243902439024, 0.43902439024390244] |
| retrieval | gemma4-e2b | 3 | 82 | 0.06666666666666667 | 0.375 | 0.25609756097560976 | [0.14634146341463414, 0.36585365853658536] |
| sentiment | gemma4-e2b | 1 | 66 | -0.18181818181818182 | 0.05555555555555555 | 0.13636363636363635 | [0.030303030303030304, 0.25757575757575757] |
| sentiment | gemma4-e2b | 2 | 65 | 0.05681818181818182 | 0.13793103448275862 | 0.13846153846153847 | [0.046153846153846156, 0.23076923076923078] |
| sentiment | gemma4-e2b | 3 | 66 | 0.13793103448275862 | 0.625 | 0.2727272727272727 | [0.16666666666666666, 0.3787878787878788] |
| sib | gemma4-e2b | 1 | 86 | -0.48989898989898983 | 0.0030769230769230743 | 0.20930232558139536 | [0.06976744186046512, 0.3372093023255814] |
| sib | gemma4-e2b | 2 | 85 | 0.0073710073710073765 | 0.08 | 0.09411764705882353 | [-0.03529411764705882, 0.2235294117647059] |
| sib | gemma4-e2b | 3 | 85 | 0.08108108108108109 | 0.375 | 0.2235294117647059 | [0.11764705882352941, 0.3411764705882353] |
| sentiment | qwen3-1.7b | 1 | 66 | -0.18181818181818182 | 0.05555555555555555 | 0.21212121212121213 | [0.030303030303030304, 0.3939393939393939] |
| sentiment | qwen3-1.7b | 2 | 65 | 0.05681818181818182 | 0.13793103448275862 | 0.24615384615384617 | [0.07692307692307693, 0.4153846153846154] |
| sentiment | qwen3-1.7b | 3 | 66 | 0.13793103448275862 | 0.625 | 0.16666666666666666 | [-0.015151515151515152, 0.3484848484848485] |
| sib | qwen3-1.7b | 1 | 86 | -0.48989898989898983 | 0.0030769230769230743 | 0.1744186046511628 | [0.05813953488372093, 0.3023255813953488] |
| sib | qwen3-1.7b | 2 | 85 | 0.0073710073710073765 | 0.08 | 0.08235294117647059 | [-0.058823529411764705, 0.2235294117647059] |
| sib | qwen3-1.7b | 3 | 85 | 0.08108108108108109 | 0.375 | 0.24705882352941178 | [0.09411764705882353, 0.4] |

#### `results/h1lf/opt2_v2_posthoc.csv` (3,690 bytes; first commit 7443e57 2026-10-23 16:12:55 +0530)

| measure | comparison | model | counted | n | intercept | intercept_ci | p | slope | slope_ci | mean_d | mean_delta | frac_delta_le_0 | p_holm | positive | ci_holm_disagree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | native-natural | qwen2.5-1.5b | False | 246 | -0.4413932395610134 | [-0.5347142179762674, -0.3484088494983834] | 0.0001 | 2.0477688184739846 | [0.8767536535743949, 3.534286949359867] | -0.43089430894308944 | 0.005127009710865629 | 0.6260162601626016 |  | False | False |
| sentiment | native-natural | qwen2.5-1.5b | False | 197 | 0.02233268313497218 | [-0.10922429936938811, 0.15630192936086795] | 0.7382 | 0.39957165201030487 | [-0.6209528292285224, 1.3070494017844656] | 0.05583756345177665 | 0.08385199537613941 | 0.2436548223350254 |  | False | False |
| sib | native-natural | qwen2.5-1.5b | False | 256 | -0.2289057904303972 | [-0.3157951873604057, -0.14115474165235462] | 0.0001 | 0.7827700082990231 | [-0.20942176833488832, 1.6970055604905885] | -0.2109375 | 0.022954750744018256 | 0.51171875 |  | False | False |
| retrieval | native-natural | qwen3.5-2b | True | 246 | 0.43055238423953196 | [0.3631416440375298, 0.49947429788273207] | 0.0001 | 1.652426361981685 | [0.6703929696089757, 2.3545901378187053] | 0.43902439024390244 | 0.005127009710865629 | 0.6260162601626016 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | qwen3.5-2b | True | 197 | 0.03197959103229569 | [-0.07437886631165423, 0.14212577134004228] | 0.548 | 0.04237709401693409 | [-0.8137779538388579, 0.9198903136324771] | 0.03553299492385787 | 0.08385199537613941 | 0.2436548223350254 | 0.548 | False | False |
| sib | native-natural | qwen3.5-2b | True | 256 | 0.14028368673525785 | [0.06607723701830089, 0.2129354978425853] | 0.0002 | 0.52538419603118 | [-0.1952221845168482, 1.3310012360278511] | 0.15234375 | 0.022954750744018256 | 0.51171875 | 0.0006000000000000001 | True | False |
| retrieval | native-natural | sarvam-1 | True | 246 | 0.013972532234948298 | [-0.012783025627721687, 0.040994896950084805] | 0.327 | 0.4461919316886731 | [0.08538006769712497, 0.996917387016189] | 0.016260162601626018 | 0.005127009710865629 | 0.6260162601626016 | 0.327 | False | False |
| sentiment | native-natural | sarvam-1 | True | 197 | 0.06557259077572807 | [0.005449115465435342, 0.12992605687450245] | 0.0328 | -0.11609774198315112 | [-0.39224093506255825, 0.1661803538448143] | 0.05583756345177665 | 0.08385199537613941 | 0.2436548223350254 | 0.0656 | False | True |
| sib | native-natural | sarvam-1 | True | 256 | -0.004716797526735285 | [-0.06957726840349425, 0.06145036854531423] | 0.8994 | -0.305032825289525 | [-1.0035617399537184, 0.32752780364522904] | -0.01171875 | 0.022954750744018256 | 0.51171875 | 0.8994 | False | False |
| retrieval | native-natural | gemma4-e2b | True | 246 | 0.26115393221222866 | [0.20469896280774302, 0.32229360754898934] | 0.0001 | 1.3923809622344858 | [0.6032170242315689, 2.0112263259295466] | 0.2682926829268293 | 0.005127009710865629 | 0.6260162601626016 | 0.00030000000000000003 | True | False |
| sentiment | native-natural | gemma4-e2b | True | 197 | 0.12948701252007058 | [0.044521698514708094, 0.218308525837755] | 0.0024 | 0.6350964457352941 | [-0.08480243475243002, 1.2610597142122801] | 0.18274111675126903 | 0.08385199537613941 | 0.2436548223350254 | 0.0072 | True | False |
| sib | native-natural | gemma4-e2b | True | 256 | 0.16447116591579747 | [0.08739474119163192, 0.2395964202153329] | 0.0001 | 0.49271212788706953 | [-0.17867692237456617, 1.3283830161758645] | 0.17578125 | 0.022954750744018256 | 0.51171875 | 0.0004 | True | False |
| sentiment | native-natural | qwen3-1.7b | True | 197 | 0.212504951498035 | [0.08098248117863444, 0.3387090637169551] | 0.0012 | -0.05227215008069694 | [-0.9410835198044224, 1.049748132427965] | 0.20812182741116753 | 0.08385199537613941 | 0.2436548223350254 | 0.0048 | True | False |
| sib | native-natural | qwen3-1.7b | True | 256 | 0.1487712532170653 | [0.06951781389129436, 0.2285922240950659] | 0.0004 | 0.8363191130680152 | [0.05124909550092299, 1.7853595376720148] | 0.16796875 | 0.022954750744018256 | 0.51171875 | 0.0008 | True | False |

#### `results/h1lf/opt2_v2_posthoc_sensitivity.csv` (3,219 bytes; first commit 7443e57 2026-10-23 16:12:55 +0530)

| measure | model | outcome | n | intercept | intercept_ci | p | slope | slope_ci | mean_d | mean_delta | frac_delta_le_0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | continuous | 246 | -0.32243445855335406 | [-0.39614879794257435, -0.25293899177248247] | 0.0001 | 0.8292759710448989 | [0.11713425059755067, 1.7773554492773362] | -0.31818275259681933 | 0.005127009710865629 | 0.6260162601626016 |
| sentiment | qwen2.5-1.5b | continuous | 197 | 1.167435269649988 | [0.05095709495799806, 2.348162431574535] | 0.0406 | 2.7931889529028635 | [-6.741857181990856, 10.782466183973545] | 1.4016497368134824 | 0.08385199537613941 | 0.2436548223350254 |
| sib | qwen2.5-1.5b | continuous | 256 | -1.8181681554712237 | [-2.555652277559576, -1.1070137278745291] | 0.0001 | 9.315663583171723 | [1.209547591760411, 19.55185771274378] | -1.6043294199043887 | 0.022954750744018256 | 0.51171875 |
| retrieval | qwen3.5-2b | continuous | 246 | 0.14675345875763493 | [0.13039793814821682, 0.1632450348216236] | 0.0001 | 0.5943517655150737 | [0.33063164452209876, 0.7873271088013134] | 0.14980070603110085 | 0.005127009710865629 | 0.6260162601626016 |
| sentiment | qwen3.5-2b | continuous | 197 | 0.36917292231186594 | [0.19792850538704262, 0.5385297157695937] | 0.0001 | 0.9302518332100435 | [-0.17416709142377612, 2.2645982270030696] | 0.4471763947288397 | 0.08385199537613941 | 0.2436548223350254 |
| sib | qwen3.5-2b | continuous | 256 | 0.6813491839891248 | [0.3964530812291199, 0.9491823364148207] | 0.0001 | 2.2816534968807103 | [-1.0325152918964133, 6.469104959530918] | 0.7337239712942392 | 0.022954750744018256 | 0.51171875 |
| retrieval | sarvam-1 | continuous | 246 | 0.025569935512857078 | [0.009375076745105538, 0.04255966823629372] | 0.0014 | 0.5078500970232442 | [0.28973679430856153, 0.7060072142419361] | 0.028173687891959304 | 0.005127009710865629 | 0.6260162601626016 |
| sentiment | sarvam-1 | continuous | 197 | 0.6824693726782896 | [0.3620333710233978, 1.006804358346849] | 0.0001 | -0.057296198302527426 | [-1.9527843872784885, 1.8094523661767388] | 0.6776649721231557 | 0.08385199537613941 | 0.2436548223350254 |
| sib | sarvam-1 | continuous | 256 | 0.14441309091167018 | [-0.05766653240060158, 0.3465848673712373] | 0.1548 | 0.06265217264848232 | [-2.3664754634342584, 2.2468321147232775] | 0.1458512559183873 | 0.022954750744018256 | 0.51171875 |
| retrieval | gemma4-e2b | continuous | 246 | 0.1570374101930826 | [0.1390485772664494, 0.17585712185523578] | 0.0001 | 0.6133700606315857 | [0.31538585915621054, 0.8330344560189002] | 0.16018216445029498 | 0.005127009710865629 | 0.6260162601626016 |
| sentiment | gemma4-e2b | continuous | 197 | 6.475077482787692 | [4.722618516708213, 8.262082479850012] | 0.0001 | 1.3493529681543537 | [-10.978718579967358, 13.077640948254158] | 6.588223421634151 | 0.08385199537613941 | 0.2436548223350254 |
| sib | gemma4-e2b | continuous | 256 | 4.05731656829465 | [2.605223990961291, 5.4887096846655] | 0.0001 | 8.838456621009456 | [-6.396393835821903, 29.441843698610317] | 4.260201136991739 | 0.022954750744018256 | 0.51171875 |
| sentiment | qwen3-1.7b | continuous | 197 | 2.222130286421173 | [1.309861142154151, 3.0659492947475893] | 0.0001 | -0.2578670563943194 | [-7.132472985909258, 8.29151078586275] | 2.200507619200738 | 0.08385199537613941 | 0.2436548223350254 |
| sib | qwen3-1.7b | continuous | 256 | 2.9319562607787497 | [1.1018353246395534, 4.719941028434178] | 0.001 | 12.171256719579098 | [-2.380487663498374, 31.571099311900802] | 3.211344425018145 | 0.022954750744018256 | 0.51171875 |

#### `results/h1lf/opt2_v2_posthoc_tertiles.csv` (5,066 bytes; first commit 7443e57 2026-10-23 16:12:55 +0530)

| measure | model | tertile | n | delta_min | delta_max | mean_d | ci |
|---|---|---|---|---|---|---|---|
| retrieval | qwen2.5-1.5b | 1 | 82 | -0.5454545454545454 | 0.0 | -0.573170731707317 | [-0.7195121951219512, -0.4268292682926829] |
| retrieval | qwen2.5-1.5b | 2 | 82 | 0.0 | 0.016666666666666663 | -0.34146341463414637 | [-0.5121951219512195, -0.15853658536585366] |
| retrieval | qwen2.5-1.5b | 3 | 82 | 0.016666666666666677 | 0.23529411764705882 | -0.3780487804878049 | [-0.5365853658536586, -0.2073170731707317] |
| sentiment | qwen2.5-1.5b | 1 | 66 | -0.1746031746031746 | 0.03552532123960697 | -0.045454545454545456 | [-0.22727272727272727, 0.12121212121212122] |
| sentiment | qwen2.5-1.5b | 2 | 65 | 0.037037037037037035 | 0.1050420168067227 | 0.15384615384615385 | [-0.03076923076923077, 0.3384615384615385] |
| sentiment | qwen2.5-1.5b | 3 | 66 | 0.10714285714285714 | 0.625 | 0.06060606060606061 | [-0.10606060606060606, 0.22727272727272727] |
| sib | qwen2.5-1.5b | 1 | 86 | -0.5454545454545454 | 0.0 | -0.26744186046511625 | [-0.4186046511627907, -0.11627906976744186] |
| sib | qwen2.5-1.5b | 2 | 85 | 0.0 | 0.043478260869565216 | -0.2 | [-0.3411764705882353, -0.058823529411764705] |
| sib | qwen2.5-1.5b | 3 | 85 | 0.04444444444444444 | 0.43478260869565216 | -0.16470588235294117 | [-0.3176470588235294, -0.011764705882352941] |
| retrieval | qwen3.5-2b | 1 | 82 | -0.5454545454545454 | 0.0 | 0.3170731707317073 | [0.1951219512195122, 0.43902439024390244] |
| retrieval | qwen3.5-2b | 2 | 82 | 0.0 | 0.016666666666666663 | 0.5609756097560976 | [0.43902439024390244, 0.6707317073170732] |
| retrieval | qwen3.5-2b | 3 | 82 | 0.016666666666666677 | 0.23529411764705882 | 0.43902439024390244 | [0.32926829268292684, 0.5487804878048781] |
| sentiment | qwen3.5-2b | 1 | 66 | -0.1746031746031746 | 0.03552532123960697 | 0.0 | [-0.13636363636363635, 0.13636363636363635] |
| sentiment | qwen3.5-2b | 2 | 65 | 0.037037037037037035 | 0.1050420168067227 | 0.13846153846153847 | [0.0, 0.27692307692307694] |
| sentiment | qwen3.5-2b | 3 | 66 | 0.10714285714285714 | 0.625 | -0.030303030303030304 | [-0.18181818181818182, 0.13636363636363635] |
| sib | qwen3.5-2b | 1 | 86 | -0.5454545454545454 | 0.0 | 0.10465116279069768 | [-0.023255813953488372, 0.23255813953488372] |
| sib | qwen3.5-2b | 2 | 85 | 0.0 | 0.043478260869565216 | 0.2 | [0.07058823529411765, 0.32941176470588235] |
| sib | qwen3.5-2b | 3 | 85 | 0.04444444444444444 | 0.43478260869565216 | 0.15294117647058825 | [0.03529411764705882, 0.27058823529411763] |
| retrieval | sarvam-1 | 1 | 82 | -0.5454545454545454 | 0.0 | -0.012195121951219513 | [-0.036585365853658534, 0.0] |
| retrieval | sarvam-1 | 2 | 82 | 0.0 | 0.016666666666666663 | 0.0 | [-0.06097560975609756, 0.06097560975609756] |
| retrieval | sarvam-1 | 3 | 82 | 0.016666666666666677 | 0.23529411764705882 | 0.06097560975609756 | [0.012195121951219513, 0.12195121951219512] |
| sentiment | sarvam-1 | 1 | 66 | -0.1746031746031746 | 0.03552532123960697 | 0.07575757575757576 | [-0.015151515151515152, 0.16666666666666666] |
| sentiment | sarvam-1 | 2 | 65 | 0.037037037037037035 | 0.1050420168067227 | 0.07692307692307693 | [-0.03076923076923077, 0.18461538461538463] |
| sentiment | sarvam-1 | 3 | 66 | 0.10714285714285714 | 0.625 | 0.015151515151515152 | [-0.030303030303030304, 0.07575757575757576] |
| sib | sarvam-1 | 1 | 86 | -0.5454545454545454 | 0.0 | 0.03488372093023256 | [-0.05813953488372093, 0.12790697674418605] |
| sib | sarvam-1 | 2 | 85 | 0.0 | 0.043478260869565216 | -0.058823529411764705 | [-0.2, 0.08235294117647059] |
| sib | sarvam-1 | 3 | 85 | 0.04444444444444444 | 0.43478260869565216 | -0.011764705882352941 | [-0.11764705882352941, 0.08235294117647059] |
| retrieval | gemma4-e2b | 1 | 82 | -0.5454545454545454 | 0.0 | 0.1951219512195122 | [0.0975609756097561, 0.2926829268292683] |
| retrieval | gemma4-e2b | 2 | 82 | 0.0 | 0.016666666666666663 | 0.32926829268292684 | [0.21951219512195122, 0.43902439024390244] |
| retrieval | gemma4-e2b | 3 | 82 | 0.016666666666666677 | 0.23529411764705882 | 0.2804878048780488 | [0.18292682926829268, 0.3780487804878049] |
| sentiment | gemma4-e2b | 1 | 66 | -0.1746031746031746 | 0.03552532123960697 | 0.13636363636363635 | [0.015151515151515152, 0.25757575757575757] |
| sentiment | gemma4-e2b | 2 | 65 | 0.037037037037037035 | 0.1050420168067227 | 0.16923076923076924 | [0.07692307692307693, 0.27692307692307694] |
| sentiment | gemma4-e2b | 3 | 66 | 0.10714285714285714 | 0.625 | 0.24242424242424243 | [0.15151515151515152, 0.3484848484848485] |
| sib | gemma4-e2b | 1 | 86 | -0.5454545454545454 | 0.0 | 0.16279069767441862 | [0.03488372093023256, 0.27906976744186046] |
| sib | gemma4-e2b | 2 | 85 | 0.0 | 0.043478260869565216 | 0.16470588235294117 | [0.023529411764705882, 0.29411764705882354] |
| sib | gemma4-e2b | 3 | 85 | 0.04444444444444444 | 0.43478260869565216 | 0.2 | [0.08235294117647059, 0.3176470588235294] |
| sentiment | qwen3-1.7b | 1 | 66 | -0.1746031746031746 | 0.03552532123960697 | 0.13636363636363635 | [-0.030303030303030304, 0.30303030303030304] |
| sentiment | qwen3-1.7b | 2 | 65 | 0.037037037037037035 | 0.1050420168067227 | 0.2923076923076923 | [0.1076923076923077, 0.46153846153846156] |
| sentiment | qwen3-1.7b | 3 | 66 | 0.10714285714285714 | 0.625 | 0.19696969696969696 | [0.015151515151515152, 0.3787878787878788] |
| sib | qwen3-1.7b | 1 | 86 | -0.5454545454545454 | 0.0 | 0.09302325581395349 | [-0.023255813953488372, 0.20930232558139536] |
| sib | qwen3-1.7b | 2 | 85 | 0.0 | 0.043478260869565216 | 0.11764705882352941 | [-0.023529411764705882, 0.24705882352941178] |
| sib | qwen3-1.7b | 3 | 85 | 0.04444444444444444 | 0.43478260869565216 | 0.29411764705882354 | [0.1411764705882353, 0.4470588235294118] |

#### `results/h1lf/opt2_v2_posthoc_verdict.json` (1,319 bytes; first commit 7443e57 2026-10-23 16:12:55 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 16:00 IST (v2; post hoc, no verdict)"
provenance.git_commit = "f12603cbfe340aa304170f66ac23ec381d940cee-dirty"
provenance.timestamp_utc = "2026-10-23T10:41:19+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf.py", "v2"]
retrieval.n_counted = 3
retrieval.needed = 2
retrieval.n_positive = 2
retrieval.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
retrieval.n_items = 246
retrieval.rule_outcome_descriptive = "effect at equal English share"
sentiment.n_counted = 4
sentiment.needed = 3
sentiment.n_positive = 2
sentiment.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
sentiment.n_items = 197
sentiment.ci_holm_disagreements = ["sarvam-1"]
sentiment.rule_outcome_descriptive = "refuted"
sib.n_counted = 4
sib.needed = 3
sib.n_positive = 3
sib.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
sib.n_items = 256
sib.rule_outcome_descriptive = "effect at equal English share"
`````

#### `results/h1lf/opt2_verdict.json` (1,266 bytes; first commit 5064f46 2026-10-23 15:52:38 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 15:44 IST (H1-LF option 2, follow-up registered post H1)"
provenance.git_commit = "6fa02b35dadb0e7f7d7e021b9430bfbaca245de2-dirty"
provenance.timestamp_utc = "2026-10-23T10:21:57+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf.py", "opt2"]
retrieval.n_counted = 3
retrieval.needed = 2
retrieval.n_positive = 2
retrieval.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
retrieval.n_items = 246
retrieval.verdict = "effect at equal English share"
sentiment.n_counted = 4
sentiment.needed = 3
sentiment.n_positive = 2
sentiment.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
sentiment.n_items = 197
sentiment.verdict = "refuted"
sib.n_counted = 4
sib.needed = 3
sib.n_positive = 3
sib.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
sib.n_items = 256
sib.verdict = "effect at equal English share"
`````

#### `results/h1lf/scores/hindi/cf_gemma4-e2b.json` (612 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
sib = [-2.4877829551696777, -3.8627829551696777, -5.550282955169678, -8.675283432006836, -5.550282955169678, -9.237783432006836, -5.675282955169678]
[MASK].sib = [-0.5948385000228882, -3.2198386192321777, -3.9698386192321777, -8.46983814239502, -4.094838619232178, -4.594838619232178, -4.844838619232178]
`````

#### `results/h1lf/scores/hindi/cf_qwen3-1.7b.json` (607 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
sib = [-0.616732656955719, -7.866732597351074, -5.616732597351074, -5.491732597351074, -8.116732597351074, -3.991732597351074, -4.741732597351074]
[MASK].sib = [-0.1491338461637497, -8.274133682250977, -3.6491339206695557, -3.1491339206695557, -5.649133682250977, -3.6491339206695557, -5.024133682250977]
`````

#### `results/h1lf/scores/hindi/cf_qwen3.5-2b.json` (614 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
sib = [-2.0323567390441895, -2.5323567390441895, -4.0948567390441895, -3.4073567390441895, -3.5948567390441895, -4.1573567390441895, -1.282356858253479]
[MASK].sib = [-2.0298879146575928, -2.7798879146575928, -4.279888153076172, -3.2798879146575928, -3.2798879146575928, -4.342388153076172, -1.9048879146575928]
`````

#### `results/h1lf/scores/hindi/cf_sarvam-1.json` (604 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
sib = [-1.7176564931869507, -3.2176566123962402, -3.7176566123962402, -4.71765661239624, -3.4676566123962402, -5.468843460083008, -0.9693723320960999]
[MASK].sib = [-1.23140287399292, -2.98140287399292, -3.73140287399292, -4.73140287399292, -3.48140287399292, -4.849200248718262, -1.0999197959899902]
`````

#### `results/h1lf/scores/hindi/gemma4-e2b__natural1004.json` (424 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 994
fertility[0].tokens_per_word = 1.6793636836004637
seconds = 747.726334810257
`````

#### `results/h1lf/scores/hindi/qwen3-1.7b__natural1004.json` (421 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 994
fertility[0].tokens_per_word = 1.9905671689515967
seconds = 318.94289803504944
`````

#### `results/h1lf/scores/hindi/qwen3.5-2b__natural1004.json` (420 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 994
fertility[0].tokens_per_word = 1.8961589192213917
seconds = 897.5954067707062
`````

#### `results/h1lf/scores/hindi/sarvam-1__natural1004.json` (420 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 994
fertility[0].tokens_per_word = 2.5172069227387186
seconds = 473.13787937164307
`````

#### `results/h1lf/scores/kannada/cf_gemma4-e2b.json` (612 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
sib = [-2.4877829551696777, -3.8627829551696777, -5.550282955169678, -8.675283432006836, -5.550282955169678, -9.237783432006836, -5.675282955169678]
[MASK].sib = [-0.5948385000228882, -3.2198386192321777, -3.9698386192321777, -8.46983814239502, -4.094838619232178, -4.594838619232178, -4.844838619232178]
`````

#### `results/h1lf/scores/kannada/cf_qwen3-1.7b.json` (607 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
sib = [-0.616732656955719, -7.866732597351074, -5.616732597351074, -5.491732597351074, -8.116732597351074, -3.991732597351074, -4.741732597351074]
[MASK].sib = [-0.1491338461637497, -8.274133682250977, -3.6491339206695557, -3.1491339206695557, -5.649133682250977, -3.6491339206695557, -5.024133682250977]
`````

#### `results/h1lf/scores/kannada/cf_qwen3.5-2b.json` (614 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
sib = [-2.0323567390441895, -2.5323567390441895, -4.0948567390441895, -3.4073567390441895, -3.5948567390441895, -4.1573567390441895, -1.282356858253479]
[MASK].sib = [-2.0298879146575928, -2.7798879146575928, -4.279888153076172, -3.2798879146575928, -3.2798879146575928, -4.342388153076172, -1.9048879146575928]
`````

#### `results/h1lf/scores/kannada/cf_sarvam-1.json` (604 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
N/A.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
sib = [-1.7176564931869507, -3.2176566123962402, -3.7176566123962402, -4.71765661239624, -3.4676566123962402, -5.468843460083008, -0.9693723320960999]
[MASK].sib = [-1.23140287399292, -2.98140287399292, -3.73140287399292, -4.73140287399292, -3.48140287399292, -4.849200248718262, -1.0999197959899902]
`````

#### `results/h1lf/scores/kannada/gemma4-e2b__natural1004.json` (426 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-9.264066696166992, -11.170316696166992, -11.014066696166992, -13.842191696166992, -10.264066696166992, -16.162504196166992, -9.420316696166992]
fertility[0].model = "gemma4-e2b"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 995
fertility[0].tokens_per_word = 3.1156526652853644
seconds = 3351.8681168556213
`````

#### `results/h1lf/scores/kannada/qwen3-1.7b__natural1004.json` (419 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-1.056042194366455, -8.306041717529297, -4.931042194366455, -4.681042194366455, -8.306041717529297, -1.556042194366455, -6.931042194366455]
fertility[0].model = "qwen3-1.7b"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 995
fertility[0].tokens_per_word = 3.4753563131788785
seconds = 341.701779127121
`````

#### `results/h1lf/scores/kannada/qwen3.5-2b__natural1004.json` (419 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-2.373037338256836, -2.873037338256836, -3.748037338256836, -3.123037338256836, -3.373037338256836, -4.060537338256836, -1.123037338256836]
fertility[0].model = "qwen3.5-2b"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 995
fertility[0].tokens_per_word = 3.280592704212972
seconds = 798.1782264709473
`````

#### `results/h1lf/scores/kannada/sarvam-1__natural1004.json` (417 bytes; first commit ca5c2e9 2026-10-28 05:39:02 +0530)

`````text
content_free_logprobs.sib = [-3.4820597171783447, -4.482059478759766, -4.982059478759766, -5.982059478759766, -4.482059478759766, -6.540065765380859, -1.290734052658081]
fertility[0].model = "sarvam-1"
fertility[0].task = "sib"
fertility[0].form = "natural1004"
fertility[0].n_texts = 995
fertility[0].tokens_per_word = 4.25849186915301
seconds = 475.3777012825012
`````

#### `results/h1lf/selection.json` (628 bytes; first commit 9fbb738 2026-10-28 10:17:38 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-28 06:20 IST (exploratory)"
provenance.git_commit = "ca5c2e9120aa27bbc204e63ba285464ae5abdd96-dirty"
provenance.timestamp_utc = "2026-10-28T04:44:51+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf_selection.py"]
n_all = 985
n_loan_free = 296
topic_chi2_p = 0.00014856860268295854
covariates = ["const", "loan_free", "en_words", "kn_tokens", "has_digit", "has_name", 1, 2, 3, 4, 5, 6]
`````

#### `results/h1lf/selection_desc.csv` (568 bytes; first commit 9fbb738 2026-10-28 10:17:38 +0530)

| measure | loan_free_mean | other_mean | all_mean | std_diff | p |
|---|---|---|---|---|---|
| en_words | 20.050675675675677 | 21.61103047895501 | 21.14213197969543 | -0.22566713857240686 | 0.0008488033311716057 |
| kn_words | 14.655405405405405 | 16.515239477503627 | 15.956345177664975 | -0.3280410361117911 | 5.4239743576919845e-06 |
| kn_tokens | 176.34121621621622 | 192.68505079825835 | 187.7736040609137 | -0.24806915376890815 | 0.0004831566841131902 |
| has_digit | 0.10472972972972973 | 0.2525399129172714 | 0.20812182741116753 |  | 5.3320991677081496e-08 |
| has_name | 0.30405405405405406 | 0.5921625544267054 | 0.5055837563451777 |  | 7.103110889940667e-17 |

#### `results/h1lf/selection_fit.csv` (1,154 bytes; first commit 9fbb738 2026-10-28 10:17:38 +0530)

| model | n | n_loan_free | unadjusted_loan_free_gap | unadjusted_other_gap | adjusted_loan_free_gap | adj_ci_low | adj_ci_high | adj_p | indicator_coef | ind_ci_low | ind_ci_high | ind_p | adj_p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3-1.7b | 985 | 296 | 0.19594594594594594 | 0.15529753265602322 | 0.19394539729543203 | 0.11445906324838163 | 0.27343173134248244 | 1.733170730163059e-06 | 0.037788412679246056 | -0.05758904018093061 | 0.13316586553942272 | 0.43743317884723165 | 5.199512190489177e-06 |
| qwen3.5-2b | 985 | 296 | 0.19932432432432431 | 0.12772133526850507 | 0.17720602798200985 | 0.09454725213840964 | 0.25986480382561006 | 2.6477572006426445e-05 | 0.03998249283349674 | -0.05743512424615915 | 0.13740010991315263 | 0.4211570239205772 | 5.295514401285289e-05 |
| sarvam-1 | 985 | 296 | -0.0472972972972973 | -0.00725689404934688 | -0.04354671569693479 | -0.10862673408550373 | 0.021533302691634157 | 0.18970160288873017 | -0.03467854130838972 | -0.11062756872020735 | 0.04127048610342792 | 0.37082712077430546 | 0.18970160288873017 |
| gemma4-e2b | 985 | 296 | 0.23310810810810811 | 0.14223512336719885 | 0.22272929953074777 | 0.14990410159157477 | 0.2955544974699208 | 2.0427194086998493e-09 | 0.0760353556426508 | -0.010906165652785543 | 0.16297687693808716 | 0.08651015703239455 | 8.170877634799397e-09 |

#### `results/h1lf/selection_topics.csv` (394 bytes; first commit 9fbb738 2026-10-28 10:17:38 +0530)

| topic | n_loan_free | n_other | share_loan_free | share_all |
|---|---|---|---|---|
| 0 | 82 | 163 | 0.27702702702702703 | 0.24873096446700507 |
| 1 | 72 | 123 | 0.24324324324324326 | 0.19796954314720813 |
| 2 | 39 | 105 | 0.13175675675675674 | 0.14619289340101524 |
| 3 | 23 | 97 | 0.0777027027027027 | 0.1218274111675127 |
| 4 | 39 | 68 | 0.13175675675675674 | 0.10862944162436548 |
| 5 | 13 | 79 | 0.04391891891891892 | 0.09340101522842639 |
| 6 | 28 | 54 | 0.0945945945945946 | 0.083248730964467 |

#### `results/h1lf/v2_check.json` (1,047 bytes; first commit 7443e57 2026-10-23 16:12:55 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 16:00 IST (v2 validity check)"
provenance.config.rule = "Hindi ITRANS - Kannada ITRANS v2 share, 95% CI within [-0.01, 0.01] on retrieval and SIB"
provenance.git_commit = "f12603cbfe340aa304170f66ac23ec381d940cee-dirty"
provenance.timestamp_utc = "2026-10-23T10:34:11+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf.py", "v2"]
retrieval.n = 246
retrieval.kannada = 0.009041313538500732
retrieval.hindi = 0.003861963064493125
retrieval.hindi_minus_kannada = -0.005179350474007607
retrieval.ci = [-0.007975964103060793, -0.0024911999554997075]
retrieval.within_pm_0.01 = true
sib.n = 256
sib.kannada = 0.009683528443472846
sib.hindi = 0.0034161588373085657
sib.hindi_minus_kannada = -0.0062673696061642786
sib.ci = [-0.009670477835670694, -0.003199285175342369]
sib.within_pm_0.01 = true
passed = true
`````

#### `results/h1lf/v2_posthoc.json` (4,339 bytes; first commit 7443e57 2026-10-23 16:12:55 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 16:00 IST (v2)"
provenance.config.status = "post hoc, no verdict"
provenance.git_commit = "f12603cbfe340aa304170f66ac23ec381d940cee-dirty"
provenance.timestamp_utc = "2026-10-23T10:35:44+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/h1lf.py", "v2"]
english_share_natural.retrieval.n = 246
english_share_natural.retrieval.kannada = 0.0525072355498768
english_share_natural.retrieval.hindi = 0.05763424526074243
english_share_natural.retrieval.hindi_minus_kannada = 0.005127009710865629
english_share_natural.retrieval.ci = [-0.00462736535085937, 0.01469192508119882]
english_share_natural.retrieval.n_loan_free_both = 97
english_share_natural.sentiment.n = 197
english_share_natural.sentiment.kannada = 0.05380297738372687
english_share_natural.sentiment.hindi = 0.13765497275986627
english_share_natural.sentiment.hindi_minus_kannada = 0.08385199537613941
english_share_natural.sentiment.ci = [0.06956951713221658, 0.09858163454694854]
english_share_natural.sentiment.n_loan_free_both = 21
english_share_natural.sib.n = 256
english_share_natural.sib.kannada = 0.053979289032881
english_share_natural.sib.hindi = 0.07693403977689925
english_share_natural.sib.hindi_minus_kannada = 0.022954750744018256
english_share_natural.sib.ci = [0.01223648609810336, 0.03368763970983716]
english_share_natural.sib.n_loan_free_both = 74
loan_free_h1.retrieval.n_counted = 3
loan_free_h1.retrieval.needed = 2
loan_free_h1.retrieval.n_positive = 2
loan_free_h1.retrieval.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b"]
loan_free_h1.retrieval.n_items = 97
loan_free_h1.retrieval.rule_outcome_descriptive = "effect (H1 supported)"
loan_free_h1.sentiment.n_counted = 4
loan_free_h1.sentiment.needed = 3
loan_free_h1.sentiment.n_positive = 0
loan_free_h1.sentiment.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
loan_free_h1.sentiment.n_items = 21
loan_free_h1.sentiment.rule_outcome_descriptive = "refuted"
loan_free_h1.sib.n_counted = 4
loan_free_h1.sib.needed = 3
loan_free_h1.sib.n_positive = 1
loan_free_h1.sib.counted_models = ["qwen3.5-2b", "sarvam-1", "gemma4-e2b", "qwen3-1.7b"]
loan_free_h1.sib.n_items = 74
loan_free_h1.sib.rule_outcome_descriptive = "refuted"
n_retrieval_D_loan_free = 172
top20_v2_words_natural.kannada[0] = ["collar", 5]
top20_v2_words_natural.kannada[1] = ["table", 4]
top20_v2_words_natural.kannada[2] = ["home", 4]
top20_v2_words_natural.kannada[3] = ["internet", 4]
top20_v2_words_natural.kannada[4] = ["lens", 4]
top20_v2_words_natural.kannada[5] = ["police", 4]
top20_v2_words_natural.kannada[6] = ["british", 4]
top20_v2_words_natural.kannada[7] = ["august", 4]
top20_v2_words_natural.kannada[8] = ["french", 4]
top20_v2_words_natural.kannada[9] = ["website", 4]
top20_v2_words_natural.kannada[10] = ["play", 3]
top20_v2_words_natural.kannada[11] = ["dark", 3]
top20_v2_words_natural.kannada[12] = ["cooler", 3]
top20_v2_words_natural.kannada[13] = ["buckle", 3]
top20_v2_words_natural.kannada[14] = ["water", 3]
top20_v2_words_natural.kannada[15] = ["star", 3]
top20_v2_words_natural.kannada[16] = ["brush", 3]
top20_v2_words_natural.kannada[17] = ["traffic", 3]
top20_v2_words_natural.kannada[18] = ["video", 3]
top20_v2_words_natural.kannada[19] = ["roman", 3]
top20_v2_words_natural.hindi[0] = ["quality", 13]
top20_v2_words_natural.hindi[1] = ["design", 10]
top20_v2_words_natural.hindi[2] = ["police", 9]
top20_v2_words_natural.hindi[3] = ["system", 8]
top20_v2_words_natural.hindi[4] = ["video", 8]
top20_v2_words_natural.hindi[5] = ["sound", 8]
top20_v2_words_natural.hindi[6] = ["content", 7]
top20_v2_words_natural.hindi[7] = ["skin", 7]
top20_v2_words_natural.hindi[8] = ["film", 7]
top20_v2_words_natural.hindi[9] = ["material", 6]
top20_v2_words_natural.hindi[10] = ["control", 6]
top20_v2_words_natural.hindi[11] = ["collar", 6]
top20_v2_words_natural.hindi[12] = ["product", 6]
top20_v2_words_natural.hindi[13] = ["team", 6]
top20_v2_words_natural.hindi[14] = ["italy", 6]
top20_v2_words_natural.hindi[15] = ["japan", 6]
top20_v2_words_natural.hindi[16] = ["airline", 6]
top20_v2_words_natural.hindi[17] = ["show", 5]
top20_v2_words_natural.hindi[18] = ["table", 5]
top20_v2_words_natural.hindi[19] = ["dark", 5]
`````

#### `results/k3b_hi/chrf.json` (722 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 12:05 (K3b-hi)"
provenance.git_commit = "4b459081c6cfa05ec09123165f0f6f8a65778d39"
provenance.timestamp_utc = "2026-10-29T08:22:37+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/k3b_dakshina.py", "analyse", "hi"]
gemini_vs_human.n = 499
gemini_vs_human.mean = 80.47282447805598
gemini_vs_human.ci = [79.39568832134124, 81.48771503931106]
gemini_vs_gemini_resample.n = 196
gemini_vs_gemini_resample.mean = 94.45799450012424
gemini_vs_gemini_resample.ci = [93.3939231991582, 95.4525441748424]
status = "descriptive only"
`````

#### `results/k3b_hi/sample.json` (230,237 bytes; first commit 7b4e869 2026-10-23 12:28:46 +0530)

`````text
provenance.config.n_total = 10000
provenance.config.n_dropped_duplicate_native = 158
provenance.config.n_dropped_short = 656
provenance.config.pool = 9186
provenance.config.seed = 6
provenance.config.seed_resample = 7
provenance.git_commit = "176c2841a6c06f332723e8e6cf63813fbfbfdfbf-dirty"
provenance.timestamp_utc = "2026-10-23T06:56:05+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/k3b_dakshina.py", "sample", "hi"]
rows[0].row = 13
rows[0].native = "आदरणीय भारत के राष्ट्रिय नागरिक महोदय व् नागरिक बन्धुओं हमारे भरत के नागरिकों पर राज करने वाले राष्ट्रिय नागरिकों से विनम्र अपील हमारे देश का कोई भी प्रधानमंत्री अगर किसी राज्य में बीस करोड़ की मदद देने की घोषणा करते है यह तो अच्चा है परन्तु मान लो की किसी राज्य की जनता पेड़ के पत्तों के पत्तल दोने का व्यापर करने में सक्षम है तो प्रधानमन्त्री जी को यह घोषणा करने की करपा करनी चाहिए की केन्द्र सर्कार दस करोड़ नगद देगे और दस करोड़ के सालाना राज्य की जनता से पेड़ के पत्तों के पत्तल दोने खरीदेंगे फिर देश की जनता को भोज के लिए हर गैस सरेण्डर के साथ मुफ्त देंगे जो देश की जनता जल पानी बर्बादी से जानलेवा मलेरिया व जल पानी बर्बादी से स्टील के बर्तन व् स्टील के ठीकरे धोनें पर चमड़ी कटने की बीमारी न हो जो जितना आमिर आदमी उतना बरबाद क्यों उसका इलाज ही नहीं होता स्टील के बर्तन को धोने वाले की परेशानी दूर बर्तन धोने वाले को रोज लगभग दोनों समय 150 ठकरे धोने से निजात मिलेगी स्टील के बरतन को धोने से जो जल बहता है जल बहने से मलेरिया के मछरों का आतंक मिट सकता है मलेरिया की बिमारियों पर परिवार बरबाद होने में कमी आएगी दवाइयों में शासनात्मक कमीशन बाजी व घोटाले बाजी जो देश को बरबाद करने में तुली हुई ह उसमें कमी आ सकती है यह योजना हर परिवार के पास पहुचती है तो हर परिवार ६ सदस्य ४० हजार रूपये की बचत व सरकार को मलेरिया के लिए परेशानी में कमी आएगी मानव व जानवरों को एलरजी नमक बिमारियों से छुटकारा पाने में मदद मिलेगी और किसी राज्य का मुख्यमंत्री जो अपने राज्य को मेहनतकस व महत्वाकान्सी आत्म शक्तिशाली बनाना चाहता है तो अपनी राज्य की जनता को पेड़ के पत्तों के पत्तल दोने का व्यापर करवाने व पेड़ के पत्तों के पत्तल दोने में खाने का प्रचार होना चाहिए सरकारें जनता नो पेड़ के पत्तों के पत्तल दोने का व्यापर का अनुदान देगी तो उस राज्य में हरियाली की कमी कभी नहीं आएगी== महुआ =="
rows[0].human = "Adarniy Bharat ke rashtriy nagarik mahoday v nagarik bandhuon hamare Bharat ke nagarikon par raj karne wale rashtriy nagarikon se vinamr appeal Hamare desh ka koi bhi Pradhanmantri agar kisi rajya men bees crore ki madad dene ki ghoshana karte hain to yah achha hai parant maan lo ki kisi rajya ki janta ped ke patton ke pattal done ka vyapar karne men sakshan hai to pradhanmantri ji ko yah ghoshana karne ki karpa karni chahiye ki kendra sarkar das crore nagad denge aur das crore ke salana rajya ki janta se ped ke patto ke pattal done kharidenge fir desh ki janta ko bhoj je liye har gas surrender ke saath muft denge jo desh ki janta jal pani barbadi se janleva malaria v jal pani barbadi se steel ke bartan va steel ke thikare dhhone par chamdi katne ki bimari n ho ji jitna amirr admi utna barbad kyon uska ilaj hi nahi hota steel ke bartan ko dhone wale ki pareshani dur bartan dhone wale ko roj lagbhag dono samay 150 thakre dhone se nijaat milegi steel ke bartan ko dhone se jo jal bahata hai jal bahane se malaria ke machharon ka atank mit sakta hai malaria ke bimariyon par parivar barbad hone men kami ayegi davaiyon men shasanatmak commission baji va ghotale baji jo desh ko barbad karne men tuli hui hai usmen kami aa sakti hai yah yojana har parivar ke pas pahunchti hai to har parivar 6 sadasya 40 hajar rupaye ki bachat v sarkar ko malaria ke liye pareshani men kami ayegi manav va janvaron ko allergy namak bimariyon se chhutkara pane men madad milegi aur kisi rajya ka mukhyamantri jo apne rajya ko mehnatkas va mahattwakansi atm Shaktishali banana chahata hai to apni rajya ki janta ko ped ke patto ke pattal done ka vyapar karnave v ped ke patton ke patta dono men khane ka prachar hona chahiye Sarkaren janta no ped ke patton je patta done ka vyapar ka anudan degi to us rajya men haiyali ki kami kabhi nahi ayegi== mahua =="
rows[1].row = 52
rows[1].native = "ए. बेरेडल कीथ: एक हिस्ट्री ऑव संस्कृत लिटरेचर;"
rows[1].human = "A. Beredal Keith: A history of Sanskrit Literature;"
rows[2].row = 56
rows[2].native = "वह ब्रिटेन के स्कॉलैंड यार्ड में महानगरीय पुलिस में विशेष प्रशिक्षण भी हासिल कर चुकी हैं।"
rows[2].human = "Vah vritain ke Scotland Yard men Mahanagaroy Police men vishesh prashikshan bhi hasil kar chuki hain."
rows[3].row = 71
rows[3].native = "चौरंगा एक हिन्दी फ़िल्म है।"
rows[3].human = "Chauranga ek Hindi film hai."
rows[4].row = 85
rows[4].native = "वे शेख मुजीब के तानाशाही रवईये के विरोधी थे, और 1975 में शेख मुजीब ने विपक्ष को बर्खास्त कर बाकसाल नामक एकदलीय शासत स्थापित किया, तब अहमद उनके विचारों से पूर्णतः विरुद्ध थे।"
rows[4].human = "Ve Shaikh Mujib ke Tanashashi ravaiye ke virodhi the, aur 1975 men Shaikh Mujib ne vipaksh ko barkhast kar Baksal namak ekdaliya shasat sthapit kiya, ab Ahmad unke vicharon se purnatah virudhha the."
rows[5].row = 87
rows[5].native = "सय्यद वहीद अशरफ़"
rows[5].human = "Sayyad Wahid Ashraf"
rows[6].row = 116
rows[6].native = "दिसंबर 2000 क़ो, अमेरिकन एक्सप्रेस ने पेसिफिक सेंचुरी फ़ाइनेंशियल कॉरपोरेशन के डिवीज़न, बैंक ऑफ हवाई के क्रेडिट कार्ड पोर्टफोलियो का अधिग्रहण करने की सहमति दी।"
rows[6].human = "December 2000 ko, American Express ne Pacific Century Financial Corporation ke division, Bank of Hawaii ke credit card portfolio ka adhigrahan karne ki sahamati di."
rows[7].row = 164
rows[7].native = "2016 मे पानमा पेपर लीक में नाम आने के बाद 2017 में सुप्रीम काेर्ट ने प्रधानमंत्री के पद के लिए अयोग करार दिया 28 जुलाई 2017 में नवाज़ शरीफ काे प्रधानमंत्री के पद से हटाना पड़ा , नवाज़ शरीफ को वर्ष 2000 में तत्कालीन सैन्य शासक मुशर्रफ़ ने निर्वासित कर दिया था, इसके पहले उनकी निर्वाचित सरकार को भी बर्खास्त कर दिया गया था।"
rows[7].human = "2016 me Panama Paper leak men naam ane ke baad 2017 men Supreme Court ne Pradhanmantri ke pad ke liye ayog karar diya 28 July 2017 men Nawaz Sharif ko pradhanmantri ke pad se hatna pada , Nawaz Sharif ko varsh 2000 men tatkalin sainya Shasak Musharaf ne nirvasit kar diya tha, iske pahale unki nirvachit sarakar ko bhi barkhast kar diya gaya tha."
rows[8].row = 219
rows[8].native = "इमारतें और बन्दर, कोहरे में कैद रंग, धूल पौधों पर।"
rows[8].human = "Imaraton aur bandar, kohare men kaid rang, dhul paudhon par."
rows[9].row = 260
rows[9].native = "फरीदपुर सिंघारा , भारतीय जनगणना अनुसार यह गाँव, तहसील बिलारी, जिला मुरादाबाद, उत्तर प्रदेश में स्थित है।"
rows[9].human = "Faridpur singhara , Bharatoy Janganana anusar yah gaon, Tahsil bilari, Zilla Muradabad, Uttar Pradesh men sthit hai."
rows[10].row = 294
rows[10].native = "उनकी साफ सुथरी छवि के कारण ही उन्हें 1964 में देश का प्रधानमन्त्री बनाया गया।"
rows[10].human = "Inki saaf suthari chhavi ke karan hi unhe 1964 men desh ka pradhanmantri banaya gaya."
rows[11].row = 337
rows[11].native = "सिंगापुर का स्वयंभू समुद्री डाकू साओ फेंग (चाउ युन-फैट विशेष रूप से उसकी ओर घृणा का भाव रखता है।"
rows[11].human = "Singapore ka swayambhu samudri daku Sao feng (Chow Yun-Fat vishesh rup se uski aur ghrunaa ka bhav rakhta hai."
rows[12].row = 401
rows[12].native = "आम तौर पर बुढ़ापे तक जीवित रहते हैं।"
rows[12].human = "aam taur par budhape tak jivit rahte hain."
rows[13].row = 411
rows[13].native = "१९९४ के बाद से यह दल चामलिंग के नेतृत्व में राज्य में निरंतर सत्ता में है।"
rows[13].human = "1994 ke baad se yah dal Chamling ke netrutwa men rajya men nirantar satta men hai."
rows[14].row = 436
rows[14].native = "परन्तु उन्हें उनमें कुछ विशेष धन प्राप्त नहीं हो सका।"
rows[14].human = "Parantu Unhe unmen kuchh vishesh dhan prapt nahi ho saka."
rows[15].row = 451
rows[15].native = "इसका उलट भी सत्य है।"
rows[15].human = "Iska ulat bhi satya hai."
rows[16].row = 459
rows[16].native = "बुंदेलखंड को ह्मष साम्राजय् के बाहर माना गया है।"
rows[16].human = "Bundelkhand ko hashm samrajya ke bahar mana gaya hai."
rows[17].row = 488
rows[17].native = "पौधों की वृद्धि एवं विकास के लिए भौतिक रसायनिक तथा जैविक शक्ति तीनों का अपना-अपना महत्व है यदि एक भी शक्ति कम है,तो मृदा की उर्वरता यह स्वास्थ्य कम होगा।"
rows[17].human = "Paudhon ke vruddhi evam vikas ke liye bhautik rasayanik tatha jaivik shakti tinon ka apna-apna mahattwa hai yadi ek bhi shakti kam hai,to mruda ki uvarta yah swasthya kam hoga,"
rows[18].row = 491
rows[18].native = "राजा मंदिरों की व्यवस्था के लिये कभी कभी भूमिकर का दान दे देता था।"
rows[18].human = "Raja mandiron ki vyvastha ke liye kabhi kabhi bhumikar ka daan de deta tha."
rows[19].row = 569
rows[19].native = "चूजे अंडे सेने के बाद बाहर आते ही माँ के पीछे पीछे घूमने लगते हैं।"
rows[19].human = "Chooje ande sene ke baad bahar ate hi maa ke picche pichhe ghumne lagte hain."
rows[20].row = 571
rows[20].native = "सोने की मुहरोंवाली थैली"
rows[20].human = "Sone ki muharonwali thaili"
rows[21].row = 572
rows[21].native = "पार्कर संयुक्त राज्य अमेरिका के दक्षिण डकोटा राज्य की काउण्टी की काउण्टी सीट है।"
rows[21].human = "Parker sanyukta Rajya America ke dakshan Dakota Rajya ki county ki kounty seat hai."
rows[22].row = 574
rows[22].native = "ये 100 से भी ज्यादा पर्यटन स्थलों पर अपनी सुविधाएं उपलब्ध कराती हैं।"
rows[22].human = "ye 100 se bhi jyada paryatan sthalon par pani svidhayen upalabdh karati hain."
rows[23].row = 604
rows[23].native = "तुम ने तो हुक्म-ए-तर्क-ए-तमन्ना सुना दिया, किस दिल से आह तर्क-ए-तमन्ना करे कोई"
rows[23].human = "Tum ne to Hukum-e-trk-e-tamanna suna diya, kis dil se aah tark-e-tamanna kare koi"
rows[24].row = 628
rows[24].native = "तंत्रशास्त्र की दृष्टि से अधिकार शब्द का मूल्य साधनात्मक है।"
rows[24].human = "Tantrashastra ki drushti se adhikar shabd ka mulya sadhanatmak hai."
rows[25].row = 669
rows[25].native = "आधुनिक कला की राष्ट्रीय गैलरी -भारत सरकार"
rows[25].human = "Adhunik kala ki rashtriy gallery -Bharat Sarkar."
rows[26].row = 716
rows[26].native = "समूचे देश में स्थान-स्थान पर चिनगारियों के रूप में नई-नई समितियाँ गठित हो गयीं।"
rows[26].human = "Samuche Desh men sthan-sthan par chingariyon ke rup men nai-nai samitoyan gathit ho gayi."
rows[27].row = 726
rows[27].native = "स्टैंडर्ड एंड पूअर्स बिल्डिंग"
rows[27].human = "Standard and Poors Building"
rows[28].row = 735
rows[28].native = "थॉमसन ने प्रिंसटन विश्वविद्यालय में वर्ष १८९६ में चार व्याख्यानों की शृंखला रखी जो वर्ष १८९७ में डिसचार्ज ऑफ़ इलेक्ट्रीसिटी थ्रो गैसेस (अनुवाद: गैसों में विद्युत् विसर्जन) के रूप में प्रकाशित हुई।"
rows[28].human = "Tomson ne Priceton Vishwavidyalay men varsh 1896 men char vyakhyanon ki shrnkhala rakhi jo varsh 1897 men discharge of electricity throw gases (anuvad: Gaison men vidyt visarjan) ke rup men prakashit hui."
rows[29].row = 761
rows[29].native = "शायद ही कभी यह एकल प्रस्तुति हो सकती है, जिसे टीवी प्रोग्राम कहा जाता है।"
rows[29].human = "Shayad hi kabhi ya ekal prastuti ho sakti hai, jise TV program kaha jata hai."
rows[30].row = 766
rows[30].native = "१ दिसम्बर २०१२ को दोपहर बाद ३ बजे उनकी अंत्येष्टि शान्ति वन और विजय घाट के मध्यवर्ती क्षेत्र \"स्मृति स्थल\" पर पूरे राजकीय सम्मान के साथ की गयी।"
rows[30].human = "1 December 2012 ko dopahar baad 3 baje unki antyeshti shanti van aur Vijay Ghat ke madhyavarti kshetra \"Smruti Sthal\" par pure rajakiy samman ke saath ki gai."
rows[31].row = 788
rows[31].native = "यह यूफॉरबिएसिई कुल का छोटा झाड़ीदार वृक्ष है, जिसका बीज सुखाकर तेल निकालने के लिये पैदा किया जाता है।"
rows[31].human = "Yah EufraBiCi kul ka chhota jhadidar vruksha hai, jiska beej sukhakar tel nikalne ke liye paida kiya jata hai."
rows[32].row = 819
rows[32].native = "बंदूकधारियों के पास नौ बंधक थे; योसेफ गुटफ़्रुंड, तेजतर्रार निशानेबाज़ी के प्रशिक्षक केहत शोर, खेल कूद के प्रशिक्षक अमीतजुर शपीरा, तलवारबाजी के खिलाडी आंद्रे स्पिट्जर, भारोत्तोलन के पंच याकोव स्प्रिंगर, पहलवान एलीज़र हाल्फिन और मार्क स्लेविन, और भारोत्तोलक डेविड बर्जर और जेव फ्राइडमैन।"
rows[32].human = "Bandukdhariyon ke pas nau bandhak the; Yosef Gutfrund, teztarrar nishanebaji ke prashikshak kehat shor, khel kud ke prashikshak Amitjur Shapira, Talwarbaji ke khiladi Andre Spitzer, Bharottolam ke panch Yakov Springer, Pahalvan Elizar Halfin aur Mark Slewin aur Bharottolak David Burger aur Jev Friedman."
rows[33].row = 821
rows[33].native = "विभाजन के बाद इन दोनों को प्रशासन करने कि ज़िम्मेदारी उन्ही की थी।"
rows[33].human = "Vibhajan ke baad in dinon ko prashan karne ki jimmedari unhi ki thi."
rows[34].row = 878
rows[34].native = "भारत की राष्ट्रीय क्रिकेट टीम ने 1980-81 के मौसम में ऑस्ट्रेलिया का दौरा किया और 3 टेस्ट मैच खेले।"
rows[34].human = "Bharat ki rashtriy cricket team ne 1980-81 ke mausam men Australia ka daura kiya aur 3 test match khelen."
rows[35].row = 884
rows[35].native = "\"नखोन\" थाई भाषा में \"नगर\" का रूप है जबकि ख्मेर में \"फनोम\" का अर्थ \"पहाड़\" है।"
rows[35].human = "\"Nakhon\" Thai bhasha men \"nagar\" ka rup hai jabki Khmer men \"Phnom\" ka arth \"pahad\" hain."
rows[36].row = 892
rows[36].native = "बुकोविना के साथ रोमानिया के विलेय की पुष्टि 1919 में सेन्ट जर्मन की संधि में हुई, और बेसर्बिया के साथ 1920 में पेरिस की संधि में हुई."
rows[36].human = "Bukovina ke saath Romania ke vilay ki prushti 1919 men Saint German ki sandhi men hui, aur Besbirya ke saath 1920 men Paris ki sandhi men hui."
rows[37].row = 915
rows[37].native = "आधुनिक भारत में सामाजिक परिवर्तन - एम.एन. श्रीनिवास"
rows[37].human = "Adhunik Bharat men samajik parivartan - M.N. Shrinivas"
rows[38].row = 927
rows[38].native = "उदाहरण के लिए, यदि जेनर वोल्टेज से अधिक रिवर्स-बायस्ड वोल्टेज प्रयोग किया जाता है तो एक डायोड जिसका जेनर निपात वोल्टेज 3.2V है, 3.2 V वोल्टेज ड्रॉप का प्रदर्शन करेगा।"
rows[38].human = "Udaharan ke liye, yadi genre voltage se adhik reverse-baised voltage prayog kiya jat hai to ek diode jiska jener nipaat voltage 3.2V hain, 3.2 V voltage drop ka pradarshan karega."
rows[39].row = 930
rows[39].native = "अत: भावी निष्पत्तियों के पूर्वकथानात्मक परीक्षण विभिन्न योग्यताओं से संबद्ध होते हैं, अत: कार्य के विभिन्न क्षेत्रों का प्रतिनिधित्व करने के लिये अनेक अभिवृत्तिपरीक्षणों का निर्माण किया गया है।"
rows[39].human = "Atah bhavi nishpatiyon ke purvakathanatmak parikshan vibhinn yogyataon se sambandh hote hain, atah karya ke vibhinn kshetron ka partinidhitwa karne ke liye anek abhivyaktiparishanon ka nirman kiy gaya hai."
rows[40].row = 1002
rows[40].native = "भारतीय दर्शन में चार्वाक ने ही बिना धर्म और ईश्वर के सुख की कल्पना की।"
rows[40].human = "Bharatiy darshan men chaarvaak ne hi bina dharm aur ishwar ke sukh ki kalpana ki."
rows[41].row = 1006
rows[41].native = "वॄष राशि वालो के लिये अपने ही अन्दर डूबे रहने की और आलस की आदत के अलावा और कोई बडी बीमारी नहीं होती है, इनमे शारीरिक अक्षमता की आदत नहीं होती है, इनके अन्दर टांसिल, डिप्थीरिया, पायरिया, जैसे मुँह और गले के रोग होते हैं, जब तक इनके दांत ठीक होते है, यह लोग आराम से जीवन को निकालते हैं, और दांत खराब होते ही इनका जीवन समाप्ति की ओर जाने लगता है।"
rows[41].human = "Vrush rashi valon ke liye apne hi andar dube rahne ki aur alas ki adat ke alava aur koi badi bimari nahi hoi hai, inmen sharirik akshamata ki adat nahi hoti hai, inke andar tonsol, diphteria, payriya jaise muh aur gale ke rog hote hain, jab tak inke dant thik hote hai, yah log aaram se jivan ko nikalte hain, aur daant kharab hote hi inka jivan samapti ki or jane lagta hai."
rows[42].row = 1025
rows[42].native = "इसके तट पर एक कटेवा जनपद था।"
rows[42].human = "Iske tat par ek kateva janpad tha."
rows[43].row = 1026
rows[43].native = "हमारी हिंदी भाषा में संधि के द्वारा पुरे शब्दों को लिखने की परम्परा नहीं है।"
rows[43].human = "Hamari Hindi Bhasha men sandhi ke dwara pure shabdon ko likhne ki parampara nahi hai."
rows[44].row = 1067
rows[44].native = "शब्दकोश से प्रतिदिन एक शब्द याद कीजिये और उसे अपने वार्तालाप में प्रयोग करन की कोशिश कीजिये।"
rows[44].human = "Shabdkosh se pratidin ek shabd yad kijiye aur use apne vartalap men prayog karne ki koshish kijiye."
rows[45].row = 1095
rows[45].native = "यह दो बीटा श्रृंखला के बहुलक प्रक्रिया को प्रेरित करता है और इसलिए उनका स्वरूप पहेली (या ताला और चाबी) के समान होता है; जिसका मतलब है कि वे एक अनुदैर्ध्य बहुलक का निर्माण करते हुए एक-दूसरे में फिट होते हैं जो कोशिका को विरूपित और अत्यंत कठोर करता है जिससे नाड़ी अंतर्विरोध फलित होता है।"
rows[45].human = "Yah do beta shrunkhala ke bahulak prakriya ko prerit karta hai aur isliye unka swarup paheli (ya tala aur chabi) ke saman hota hai; jiska matlab hai ki Ve ek anudairdhya bahulak ka nirman karte huye ek-dusre men fir hote hain jo koshika ko virupit aur atyant kathor karta hai jisse nadi antarvirodh falit hota hai."
rows[46].row = 1120
rows[46].native = "2008 में अपनी प्रेमिका, प्रीति जिंटा के साथ वाडिया ने मोहाली-अवस्थित इंडियन प्रीमियर लीग (IPL) के ट्वेंटी 20 क्रिकेट टीम का स्वामित्व अधिकार हासिल किया।"
rows[46].human = "2008 men apni premika, Preeti Zinta ke saath Wadia ne Mohali-avasthit Indian Premiere League (IPL) ke twenty 20 cricket team ka swamitwa adhikar hasil kiya."
rows[47].row = 1123
rows[47].native = "यह यात्रा ५ किलोमीटर लम्बी होती है।"
rows[47].human = "Yah yatra 5 kilometer lambi hoti hai."
rows[48].row = 1127
rows[48].native = "सन्‌ 1851 में आस्ट्रिया के लिंज तथा डोनाविट्ज़ धातुविज्ञों ने बेसेमर विधि के संपरिवर्तित रूप की खोज की, जिसे उनके नाम पर एल."
rows[48].human = "San 1851 men Austria men Linz tatha Donawitz Dhatuvigyon ne Basemar vidhi ke samparivartit rup ki khoj ki, jise unke naam par L"
rows[49].row = 1133
rows[49].native = "लघु देवी देवताओं के रूप में ईरानी म्थ्राि, (युद्ध के देवता) इटाली लाइवर पेटर (सुरा देवी) वद्याल (सूर्य देवता) मा और आइसिस, लेनस और वोल्कनेस की बड़ी मान्यता थी।"
rows[49].human = "Laghu Devi devataon ke rup men Irani Mithra, (Yudh ki devata) Italy Live Peter (Sura Devi) Vadyal (Surya Devta) ma aur Isis, Lenos, aur Volcanus ki badi manyata thi."
rows[50].row = 1143
rows[50].native = "विक्रम ने सच जानकर भवन की ओर कदम बढ़ा दिया।"
rows[50].human = "Vikram ne sach jankar bhawan ki or kadam badha diya."
rows[51].row = 1147
rows[51].native = "आचार्य दण्डी मुक्तक नाम से न सही पर अनिबद्ध काव्य के रूप में इससे परिचित थे."
rows[51].human = "Acharya Dandi muktak naam se na sahi par anibiddha kavya ke rup men isse parichit the."
rows[52].row = 1153
rows[52].native = "वो १६वीं लोकसभा में जयपुर ग्रामीण लोकसभा क्षेत्र से भाजपा के सांसद चुने गये।"
rows[52].human = "vo 16vin Loksabha men Jaipur Gramin Loksabha kshetra se BJP ke sansad chune gaye."
rows[53].row = 1156
rows[53].native = "जयसिम्हा ने आग्रह स्वीकार किया और अपने पुत्र अवनिजनश्रया पुलकेसी को नागभट्ट प्रथम को समर्थन देने के लिए भेजा ।"
rows[53].human = "Jaisimha ne agraha swikar kiya aur apne putra avanijanshraya pulkesi ko naagbhatt pratham ko samarthan dene ke liye bheja ."
rows[54].row = 1160
rows[54].native = "इस दिशा में, कुछ देशों में स्कूल नागरिकता शिक्षा उपलब्ध करते हैं।"
rows[54].human = "Is disha men, kuch deshon me school nagarikta shiksha upalabdh karte hain."
rows[55].row = 1162
rows[55].native = "प्रशासनिक दृष्टि से यह मिमारोपा प्रशासनिक क्षेत्र का भाग है और प्रान्त का दर्जा रखता है।"
rows[55].human = "Prashasanik drushti se yh mimaropa Prashasanik kshetra ka bhag hai aur prant ka darja rakhata hai."
rows[56].row = 1165
rows[56].native = "उत्तर प्रान्त (लेबनान)"
rows[56].human = "Uttar Prant (Lebanon)"
rows[57].row = 1208
rows[57].native = "मानव बस्तियों के पास रहने वाले वयस्क मोरों का शिकार कभी कभी घरेलू कुत्ते द्वारा किया जाता है, (दक्षिणी तमिलनाडु) में कहावत है कि मोर के तेल लोक उपचार होता है।"
rows[57].human = "manav bastiyon ke paas rahne wale vayask moron ka shikar kabhi kabhi gharelu kutte dwara kiya jata hai, (Dakshini Tamilnadu) men Kahavat hai ki Mor ke tel lok upchar hota hai."
rows[58].row = 1238
rows[58].native = "कविता में श्रीकृष्ण के विषय की उन कहानियों का वर्णन है जिनका संबंध उनके जन्म से लेकर अंत तक है।"
rows[58].human = "Kavita men Shrikrushna ke vishay ki un kahaniyon ka varnan hai jinka sambandh unke janam se lekar ant tak hai."
rows[59].row = 1323
rows[59].native = "बुकारेस्ट यहाँ की राजधानी तथा रेलों का केंद्र है।"
rows[59].human = "Bucharest yaha ki rajdhani tatha relon ka kendra hai."
rows[60].row = 1329
rows[60].native = "तो उनके प्रशंसकों व शुभचिन्तकों की अपार भीड़ उनके बँगले पर जमा हो गयी।"
rows[60].human = "o unke prashansakon va shubhchintakon ki apar bheed unke bangle par jama ho gai."
rows[61].row = 1362
rows[61].native = "उर्दू के श्रेष्ठ हास्य व्यंग्य - स. सुरजीत"
rows[61].human = "Urdu ke shresht hasya vyangya - S. Surjeet"
rows[62].row = 1393
rows[62].native = "इस्लामी स्वर्ण युग"
rows[62].human = "Islami swarna yug"
rows[63].row = 1395
rows[63].native = "ग्रंथ को लेकर वे सातवाहन नरेश की सभा में पुन: गए जहाँ उन्हें वांछित सत्कार नहीं मिला।"
rows[63].human = "Granth ko lekar ve satvaahan naresh ki sabha men punah gaye jahan unhe vanchhit satkar nahi mila."
rows[64].row = 1413
rows[64].native = "यह मारगाँव से एक घण्टे की दूरी पर है।"
rows[64].human = "Yah Maargoa se ek ghante ki duri par hai."
rows[65].row = 1439
rows[65].native = "बिस्मिल की अन्त्येष्टि के बाद बाबा राघव दास ने गोरखपुर के पास स्थित देवरिया जिले के बरहज नामक स्थान पर ताम्रपात्र में उनकी अस्थियों को संचित कर एक चबूतरा जैसा स्मृति-स्थल बनवा दिया।"
rows[65].human = "Bismil ki anteshti ke baad Baba Raghav Das ne Gorakhapur ke paas sthit Devariya Zile ke barhaj Namak sthan par tamrapaatra men unki asthuyon ko sanchit kar ek chabutara jaisa smruti-sthal banva diya."
rows[66].row = 1455
rows[66].native = "उन्होंने बाद में राइट के साथ बात की और उन्हें अपना समर्थन दिया, लेकिन एल्बम पर उनके योगदान की कमी के बारे में उन्हें याद दिलाया।"
rows[66].human = "Unhone baad men Right ke saath baat ki aur unhe apna samarthan diya, lekin album par unke yogdan ki kami ke bare men unhe uyaad dilaya."
rows[67].row = 1469
rows[67].native = "व्याकरणिक आधार सबसे अधिक प्रामाणिक होता है।"
rows[67].human = "Vyakaranik aadhar sabse adhik pramanik hota hai."
rows[68].row = 1492
rows[68].native = "इस शो में एक गाना है,\"ला विए बोहेम,\" जो उत्तराधुनिक बोहेमियन संस्कृति का कीर्तिगान करता है।"
rows[68].human = "Is show men ek gana hai, \"la Via Bohem,\"jo uttaradhunik Bohemian sanskruti ka kirtigaan karta hai."
rows[69].row = 1535
rows[69].native = "काबा को 692 में मक्का की दूसरी घेराबंदी में पत्थरों से बमबारी कर दिया गया था, जिसमें उमाय्याद सेना का नेतृत्व अल-हजज इब्न यूसुफ ने किया था।"
rows[69].human = "Kaba ko 692 men Mecca ki dusri gherabandi men patharon se bambari kar diya gaya tha, jismen Umaayaad sena ka netrutwa Al-Hajj Ibin Yusuf ne kiya tha."
rows[70].row = 1550
rows[70].native = "वेंडी पिल्ट्ज़ एक ऑस्ट्रेलियाई महिला क्रिकेट टीम की पूर्व महिला क्रिकेट खिलाड़ी है, जो ऑस्ट्रेलिया के लिए १९८० के दशक में एक दिवसीय अंतर्राष्ट्रीय मैच और टेस्ट क्रिकेट मैच खेला करती थी।"
rows[70].human = "Wendy Piltrij ek austreliyayi mahila cricket teem ki purva mahila cricket khiladi hai, jo Australia ke liye 1980 ke dashak men ek diasaiy antarrashtriy match aur test cricket match khela karti thi."
rows[71].row = 1559
rows[71].native = "BBC 6Music के लिए मई 2008 के साक्षात्कार में, डेविड गिल्मर ने संकेत दिया कि वे एक और एकल प्रस्तुति के पक्ष में हैं, लेकिन एक पूर्ण दौरे को खारिज कर दिया।"
rows[71].human = "BBC 6Music ke liye May 2008 ke sakshatkar men, David Gilmer ne sanker diya ki ve ek aur ekal prastuti ke paksh men hain, lekin ek purn daure ko kharij kar diya."
rows[72].row = 1605
rows[72].native = "एक दिन उन लोगों को यह अजगर मिल गया और उन्होंने मिलकर उसे मृत्यु के घाट उतार कर उसको समाप्त कर दिया।"
rows[72].human = "Ek din un logon ko yah ajgar il gaya aur unhone milkar use mrutyu ki ghat utaar kar isko samapt kar diya."
rows[73].row = 1627
rows[73].native = "यहाँ का चित्र संग्रह, विशेषकर लघुचित्रों का विश्व में अपना एक विशिष्ट स्थान रखता है।"
rows[73].human = "yahan ka chitra sangrah, visheshkar laghuchitron ka vishwa men apna ek vishishta sthan rakhata hai."
rows[74].row = 1637
rows[74].native = "परंतु नई कविता की यथार्थवादी दृष्टि काल्पनिक या आदर्शवादी मानववाद से संतृष्ट न होकर जीवन का मूल्य, उसका सौंदर्य, उसका प्रकाश जीवन में ही खोजती है।"
rows[74].human = "parantu nai kavita ki yatharthvadi drushti kalpanik y adarshwadi manavvad se santusht n hokar jivan ka mulya, uska saundarya, uska prakash jivan men hi khojati hai."
rows[75].row = 1643
rows[75].native = "इसमें दोनों के बीच में एक ऐसी प्रतियोगिता शुरू हो जाती है जिसमें दोनों में से कोई भी पीछे नहीं हटना चाहता लेकिन किसी के भी न हटने पर दोनों को भारी हानि होती है।"
rows[75].human = "Ismen dono ke beeech men ek aisi pratiyogita shuru ho jaati hai jismen donon men se koi bhi Picche nahi hatna chahta lekin kisi ke bhi n hatne par donon ko bhari hani hoti hai."
rows[76].row = 1673
rows[76].native = "फिल्म निर्माण का सामूहीकरण को कम्युनिस्ट राज्य की प्रोग्रामिक पूर्ति के लिए केंद्रीय था।"
rows[76].human = "Film nirman ka samuhikaran ko communist rajya ki programmik purti ke liye kendriy tha."
rows[77].row = 1678
rows[77].native = "इसमें न तो कहनी जैसी एकसूत्रता, सघन बुनावट और प्रभावान्विति होती है और न ही उपन्यास जैसा फैलाव तथा निरूपण वैविध्य।"
rows[77].human = "Ismen n to kahni jaise eksutrata, saghan bunavat aur prabhavanviti hoti hai aur n hi upanyas jaisa failab tatha nirupan vaividhya."
rows[78].row = 1681
rows[78].native = "इस उत्पाद में फिश स्टिक की एक श्रृंखला थी, जिसे चिकन टेंडर्स जैसी शैली वाले डिब्बों में ही बेचा जाता था और इसमें डुबोने के लिये एक टार्टर सॉस पैकेज होता था।"
rows[78].human = "Us utapad men fish stick ki ek shrunkhala thi, jise chicken tenders jaisi shaili wale dibbon me hi becha jata hai aur ismen Dubone ke liye ek tartar sauce package hota hai"
rows[79].row = 1685
rows[79].native = "सिटीजनस बैंक पार्क, फिलाडेल्फिया नगर, संयुक्त राज्य अमेरिका में स्थित एक बेसबॉल स्टेडियम है।"
rows[79].human = "Citizen's Bank park, Philedelphia nagar, Sanyukta rajya Americ men sthit ek baseball stadium hai."
rows[80].row = 1690
rows[80].native = "धरती में पहुंचकर वे व्हाइट हाउस में घुसते हैं, और संयुक्त राज्य के राष्ट्रपति को एक अंतर्राष्ट्रीय टेलीविजन प्रसारण के दौरान पूरे ग्रह की तरफ से आत्मसमर्पण करने के लिए कहते हैं।"
rows[80].human = "Dharti men pahunchkar ve White House men ghuste hain, aur sanyukta rajya ke rashtrapati ko ek antararashtriy television prasaran ke dauan pure grah ki taraf se aatmasamarpan karne ke liye kahate hain."
rows[81].row = 1709
rows[81].native = "डॉ अहमद ने एक लोकप्रिय आंदोलन का विरोध किया था और मुस्लिम जनता को अलगाव करने का जोखिम उठाया था।"
rows[81].human = "Dr Ahmad ne ek lokpriya andolan ka virodh kiya tha aur Muslim janta ko algaav karne ka jokhim uthaya tha."
rows[82].row = 1744
rows[82].native = "सातवीं बार युद्ध में बन्दी बनाकर उसकी हत्या कर दी गयी।"
rows[82].human = "Saatvin baar yuddh men bandi banakar uski hatya kar di gayi."
rows[83].row = 1759
rows[83].native = "रुपांतरण एक अंतर्वलन है, जहाँ,"
rows[83].human = "Rupantar ek antarvalan hai, jahan,"
rows[84].row = 1764
rows[84].native = "उत्तराफ़ाल्गुनी के दूसरे चरण के स्वामी सूर्य और शनि है।"
rows[84].human = "Uttarafalguni ke dusre charan ke swami Surya aur shani hai."
rows[85].row = 1786
rows[85].native = "साहिर लुधियानवी के प्रबल आशावाद 'वो सुबह कभी तो आयेगी' और फ़ैज़ के मोहभंग 'वो इन्‍तज़ार था जिसका ये वो स‍हर तो नहीं' की स्‍मृति जगाता यह उपन्‍यास एक उपलब्धि है।"
rows[85].human = "Sahir Ludhiyanvi ke prabal ashawada 'wo subah kahi to ayega' aur Faiz ke mohbhang 'vo intezaar. tha jiska ye vo sahar to nahi ki smruti jagata yah upanyas ek upalabdhi hai."
rows[86].row = 1791
rows[86].native = "धूल की प्रकृति एवं रंग के आधार पर इन्हें काली अथवा पीली आँधियां कहा जाता है।"
rows[86].human = "Dhul ki prakruti eva rang ke adhaar par inhe kali athava pili andhitan kaha jata hai."
rows[87].row = 1825
rows[87].native = "आधुनिक विद्वानों मिथकों को देखें और उन्हें एक करने की कोशिश में अध्ययन करने के लिए प्राचीन ग्रीस, इसके सभ्यता के धार्मिक और राजनीतिक संस्थाओं पर प्रकाश फेंक और मिथक खुद बनाने की प्रकृति की समझ सकें."
rows[87].human = "Adhunik vidwanon mithakon ko dekhen aur unhe ek karne ki koshish men adhyayan karne ke liye prachin Greece, iske Sabhyata ke dharmik aur rajnitik sansthaon par prakash fenk aur mithak khud banane ki prakruti ki samajh saken."
rows[88].row = 1830
rows[88].native = "आज शेफील्ड तथा डानकैस्टर के बीच की डान की घाटी इस्पात का मुख्य प्रदेश बन गई है।"
rows[88].human = "Aaj Sheffield tatha Dancaster ke beech ki Daan ki ghati ispat ka mukhya pradesh ban gai hai."
rows[89].row = 1851
rows[89].native = "वाकाटक साम्राज्य एवं शासक"
rows[89].human = "Wakatak Samrajya evam shasak"
rows[90].row = 1864
rows[90].native = "मराठी चलचित्र उद्योग भी मुंबई में ही स्थित है।"
rows[90].human = "Marathi Chalchitra udyog bhi Mumbai men hi sthit hai."
rows[91].row = 1874
rows[91].native = "वैश्विक मंदी विश्वव्यापी आर्थिक मंदी की अवधि है।"
rows[91].human = "Vaishwik mandi vishwavyapi aarthik mandi ko avadhi hai."
rows[92].row = 1903
rows[92].native = "कथा में आने वाले अलौकिक प्रसंग जैसे कृष्‍ण के जन्म के समय कारागार के द्वार स्वत: खुल जाने को तर्कसंगत एवं युगानुकूल बनाया गया है।"
rows[92].human = "Katha men ane wale aalaukik prrasang jaise Krushna ke janam ke samay karagar ke dwar swatah khul jane ko tarksangat evam yuganukul banaya gaya hai."
rows[93].row = 1921
rows[93].native = "ऐसा तापमान और दबाव, जिसमें किसी पदार्थ की तीनों अवस्थाएँ (ठोस, तरल और वाष्प) एक साथ संतुलन में रहते हैं।"
rows[93].human = "aisa taapman aur dabav, jismen kisi padarth ki teenon avasthayen (thos, taral aur vashpa) ek saath santulan men rahte hain."
rows[94].row = 1924
rows[94].native = "नर गौरैया को चिड़ा और मादा चिड़ी या चिड़िया भी कहते हैं।"
rows[94].human = "Nar gaureya ko chida aur mada chidi ya chidiya bhi kahte hain."
rows[95].row = 1954
rows[95].native = "उसके ना-नुकुर करने पर घोड़े ने उसे समझाया कि वह राजा का दूत है, इसलिए उसके उपहार का उपयोग वह कर सकता है।"
rows[95].human = "Uske na-nukr karne par ghode ne use samjhaya ki vah raja ka doot hai, isliye uske uphar ka upayog vah kar sakta hai."
rows[96].row = 1961
rows[96].native = "हिन्दी की उपभाषाओं, बोलियों, व्यवहारिक हिन्दी, मानक हिन्दी में बोला जाता है- 'ग़ालिब का दीवान'।"
rows[96].human = "Hini ki upabhashaon, boliyon, vyavaharik Hindi, manak Hindi men bola jata hai- 'Gaalib ka Diwan'."
rows[97].row = 1962
rows[97].native = "सलन्द्र कहलगाँव, भागलपुर, बिहार स्थित एक गाँव है।"
rows[97].human = "Salandra Kahalagaon, Bhagalapur, Bihar sthit ek gaon hai."
rows[98].row = 2001
rows[98].native = "पर तब तक जर्मन अपार्टमेंट में कई संवाददाताओं ने स्तिथी का प्रसारण शुरू किया था जिस कारण आतंकवादीयों को इस निती का पता चल गया।"
rows[98].human = "par tab tak German Apartment men kai sanvaddaton ne sthiti ka prasaran shuru kiya tha jis karam atankwadiyon ko is niti ka pata chal gaya."
rows[99].row = 2014
rows[99].native = "यह राजा मेरा अतिथि है इसलिये मैं इसको शाप भी नहीं दे सकता और इसके पास विशाल सेना होने के कारण इससे युद्ध में भी विजय प्राप्त नहीं कर सकता।"
rows[99].human = "Yah raja mera athiti hai isliye main iskoo shaap bhi nahi de sakta aur iske paas vishal seba hone ke karan isse yuddh ,en bhi vijay prapt nahi kar sakta"
rows[100].row = 2033
rows[100].native = "शाहजहाँपुर: शहीदे-आज़म पं॰ रामप्रसाद बिस्मिल ट्रस्ट."
rows[100].human = "Shanjahanpur: Shahde-aajam Pan. Ramprasasd bismal trust."
rows[101].row = 2045
rows[101].native = "कैरियर में एक, मलेरिया परजीवी की उपस्थिति के साथ समय से पहले दोषपूर्ण हीमोग्लोबिन लाल रक्त कोशिकाओं का कारण बनता है टूटना, पुन: पेश करने के लिए प्लाज्मोडियम में असमर्थ है।"
rows[101].human = "kariyar men em, Maleriya prjeevi ki upsthiti ke sath samy se pahle doshpoorn Himoglobin lall rakt. koshikaaon ka karan banta hai tootna, punah pesh karne ke liye Paajmodiyam me asmarth hai."
rows[102].row = 2050
rows[102].native = "मुंशी इन्द्रजीत ने रामप्रसाद को आर्य समाज के सम्बन्ध में बताया और स्वामी दयानन्द सरस्वती की लिखी पुस्तक सत्यार्थ प्रकाश पढ़ने को दी।"
rows[102].human = "munshi Indrjeet ne Ramprasad ko Arya samaj ke sambahdh men bataya aur Swami Dayanand Sarswwati kii likhi pustak Satyarth Prakash padhne ko dee."
rows[103].row = 2067
rows[103].native = "इस माप को पूर्ण माना जाता है क्योंकि यह किसी मानदंड को संदर्भित नहीं करता है और मानदंड के खराब विकल्प से संबंधित कमियों से दूर रहता है।"
rows[103].human = "is maap ko poorn mana jaata hai kyonki yah kis manddand ko sandrbhit nahin karra hai aur mandand ke kharaab vikalp se sambandhit kamiyon se door rahta hai."
rows[104].row = 2106
rows[104].native = "प्लूटोनियम के समस्थानिक"
rows[104].human = "Plyutoninum ke samsthanki"
rows[105].row = 2118
rows[105].native = "इनका रंग काला, भूरा, लाल, अथवा सन के रेशे सा होता है।"
rows[105].human = "inka rang kala, bhoora, laal, athva san ke reshe saa hota hai."
rows[106].row = 2140
rows[106].native = "किंतु अभी यह कहना कठिन है कि परिवार का संयुक्त रूप समाप्त हो रह है।"
rows[106].human = "kint abhi yah kahna kathin hai ki pariar kaa sanyukt roop samapt ho raha his."
rows[107].row = 2179
rows[107].native = "फिलिप वी कार्डन फूड एंड एग्रीकल्चरल आर्गनाइज़ेशन के तीसरे महानिदेशक थे।"
rows[107].human = "Filip vee Kaardan food and agrikalchar organizeshan ke teesre mahanirdeshak the."
rows[108].row = 2210
rows[108].native = "वर्तमान में अस्तित्व रखने वाली अधिकतर जातियाँ निशाचरी (रात्रि को सक्रीय) हैं।"
rows[108].human = "vartman men astitwa rakhane waali adhiktar jatiya nishachari (ratri ko sakriya) hain."
rows[109].row = 2216
rows[109].native = "डाइक्रोमेट भी जलविलेय होता है।"
rows[109].human = "Daikromet bhi jalviley hota hai."
rows[110].row = 2249
rows[110].native = "इतिहास का क्षेत्र बड़ा व्यापक है।"
rows[110].human = "itihas ka shetra bada vyapak hai."
rows[111].row = 2269
rows[111].native = "तथापि, आदेश को उस हद तक संशोधित किया गया है कि किसानों को मूल्‍य समर्थन सुनिश्चित करने के लिए चावल के लेवी आदेश को बरकरार रखा गया है, जबकि सार्वजनिक वितरण प्रणाली/कल्‍याण योजनाओं के लिए भारतीय खाद्य निगम/राज्‍य सरकार की एजेंसियों के अधिकार में चावल की पर्याप्‍त उपलब्‍धता सुनिश्चित की गई है।"
rows[111].human = "tatapi, aadesh ko us had tak sanshodhit kiya gaya hai ki kisanon ko mulya samrthan sunichit karane ke liye chaval ke levi aadesh ko barkarar rakha gaya hai, jabki sarwjanik vitran pranali/kalyan yojnaon ke liye bhartiy khadya nigam/rajya sarkar ki yejensiyo ke adhikar men chaval ki paryapt uplabdata sunichit ki gai hai."
rows[112].row = 2315
rows[112].native = "इसका अनुभव प्राप्त करना और एक ही जीवन में सभी कर्मों का फल भुगतना असंभव है।"
rows[112].human = "iska anubhav prapt karna aur ek hi jivan men sabhi karmon ka fal bhugtna asambhav hai."
rows[113].row = 2327
rows[113].native = "क्योंकि उनका मानना था की न्युरोसिस अच्छे जीवन के लिए आवश्यक भी है।"
rows[113].human = "kyonki unka manana tha kee Nurosis achhe jivan ke liye aavshak bhi hai."
rows[114].row = 2338
rows[114].native = "विरोध प्रदर्शन में कई छात्रों की मृत्यु हो गई, जो बंगाली भाषा को भविष्य की पीढ़ियों के लिए बचाना चाहते थे।"
rows[114].human = "virodh pradarshan men kai chhatron ki mrutu ho gai, jo Bangali Bhasha ko bhavishya ki pidhiyon ke liye bachana chahate the."
rows[115].row = 2345
rows[115].native = "इस हमले में खुद मेजर जनरल प्रसाद के काफिले पर भी भीषण हमला हुआ और उन्हें अपना वाहन छोड़ कर पीछे हटना पड़ा।"
rows[115].human = "is hamle men khud mejar Jenral Prasad ke kafile par bhi bhisan hamla hua aur unhen apna vaahan chhod kar pinchhen hatna pada."
rows[116].row = 2366
rows[116].native = "पुट्ठे और पूंछ के बालों की छंटाई से पिछले पैरों तथा शक्तिशाली पतवार-जैसी पूंछ के संचालन में आसानी होती है।"
rows[116].human = "Putthe aur Punchh ke balon ki chhantai se pichhale pairon tatha shaktishali patvaar-jaisi punchh ke sanchalan men aasani hoti hai."
rows[117].row = 2394
rows[117].native = "अंग्रेजों का इस क्षेत्र पर पूर्ण अधिकार 4 अप्रैल 1816 को सुगौली की सन्धि के बाद इस पूरे क्षेत्र पर हो गया और नेपाल की सीमा काली नदी घोषित हुई।"
rows[117].human = "Angrejon ka is shetra par purn adhikar 4 April 1816 ko Sugauli ki sandhi ke baad is poore shetra par ho gaya aur Nepaal ki seema Kali nadi ghoshit hui."
rows[118].row = 2395
rows[118].native = "इनमें अंतराआण्विक दूरियाँ लघु होती हैं।"
rows[118].human = "inmen antaraanvik duriya laghu hoti hain."
rows[119].row = 2405
rows[119].native = "यह स्थल पानीपत की लड़ाई से ताल्लुक रखता है।"
rows[119].human = "yah sthal Panipat ki ladai se talluk rakhata hai."
rows[120].row = 2424
rows[120].native = "मर्रियट होटल ब्रांड का पहला होटल था जो इंडिया में खोला गया था।"
rows[120].human = "Marriott Hotel brond ka pahila hotel tha jo India men khola gaya tha."
rows[121].row = 2426
rows[121].native = "संकर्षा (कॉर्सेट) बनाना यहाँ की विशेषता है।"
rows[121].human = "Sakrsha (Corset) banana yaha ki visheshta hai."
rows[122].row = 2443
rows[122].native = "उक्त कन्हाई नाटयशाला में राधाकृष्ण एवं चैतन्य महाप्रभु के पदचिह्न आज भी मौजूद है।"
rows[122].human = "ukt kanhai natyashala men Radhakrushna avm Chaitnya Mahaprabhu ke padchihan aaj bhi maujud hai."
rows[123].row = 2449
rows[123].native = "चूंकि व्यक्ति, व्यापार संस्थान तथा सरकार सभी के काम करने के लिये वित्त अत्यावश्यक है, इसलिये वित्त के क्षेत्र को भी तीन प्रकार से विभाजित किया जाता है-"
rows[123].human = "chunki vyakti, vyapar sansthan tatha sakar sabhi ke kaam karne ke liye vitt atyavshyak hai, isliye vitt ke shetra ko bhi teen prakar se vibhajit kiya jata hai-"
rows[124].row = 2497
rows[124].native = "मेला तीन दिन या अधिक भी चलता है।"
rows[124].human = "Mela teen din ya adhik bhi chalta hai."
rows[125].row = 2504
rows[125].native = "प्रांत जिलों और ग्रामों में विभक्त थे।"
rows[125].human = "prant jilon aur gramon men vibhakt the."
rows[126].row = 2517
rows[126].native = "तारों से प्राप्त होनेवाली प्रकाशतरंगों से व्यतिकरण द्वारा तारों की दिशा, दूरी तथा विस्तार का निर्धारण किया जाता है।"
rows[126].human = "taron se prapt honewali prakashtarangon se vyaktikaran dwara taron ki disha, duri tatha visthar ka nirdharan kiya jata hai."
rows[127].row = 2519
rows[127].native = "केंद्रीय कक्ष के दरवाजे के ऊपर हमें पंचतंत्र से संस्‍कृत का एक पद्यांश देखने को मिलता है :-"
rows[127].human = "kendriy kaksh ke darwaje ke upar hamen Panchtantr se sansrut ka ek padyansh dekhane ko milta hai :-"
rows[128].row = 2520
rows[128].native = "अंग फिटिंग केंद्र गतिविधि, विशेष शिविर गतिविधि, ए0डी0आई0पी0 - सर्व शिक्षा अभियान, शिविर गतिविधि, मुख्यालय गतिविधि के माध्यम से सबसे बड़ी ए0डी0आई0पी0 कार्यान्वयन एजेंसी की स्थिति बनाए रखना।"
rows[128].human = "ang feeting kendra gatividhi, vishesh shivir gatividhi A.D.I.P. - sarv shiksha abhiyan, shivir gatividhi, mukhyalay gatividhi ke madhyam se sabse badi A.D.I.P. karyanvayan Agency ki sthiti banaye rakhana."
rows[129].row = 2560
rows[129].native = "इस समय भारोपीय परिवार की भाषाओं का अध्ययन इतना हो चुका है कि यह पूर्ण प्रक्रिया उस पर लागू हो जाती है।"
rows[129].human = "is samay Bharopiy parivaar ki bhashaon ka adhyayan itna ho chuka hai ki yah purn prakirya us par lagu ho jati hai."
rows[130].row = 2566
rows[130].native = "न कुछ खाना, न पीना, सोना और आराम करना भूलकर साधना में लीन रहे।"
rows[130].human = "n kuchh khana, n pina, sona aur aaram karna bhulkar sadhana men leen rahe."
rows[131].row = 2569
rows[131].native = "गौरतलब है कि इससे पहले उत्तरी अमेरिका में देवदार के 4,000 से 5,000 वर्ष पुराने पेड़ों के बारे में पता चला था।"
rows[131].human = "gaurtalab hai ki isse pahle Uttari America men Devdar ke 4,000 se 5,000 varsh purane pedon ke baare men pata chala tha."
rows[132].row = 2571
rows[132].native = "उदाहरण के लिए, कौशितकी उपनिषद 1.2 कहता है कि कृमि, कीड़े-मकौड़े, मछली, पंक्षी, सिंह, सुअर, सांप या मानव जैसे जीवन का विभिन्न अवस्था में जन्म लेना व्यक्ति द्वारा किए गए कार्यों और ज्ञान द्वारा निर्धारित होता है।"
rows[132].human = "udaharan ke liye, Kaushitki upnishad 1.2 kahta hai ki Krumi, Kide-Makode, Machhali, Pankshi, Sinh, Suar, Sanp ya Manav jaise jivan ka vibhinn avstha men janm lena vyakti dwara kiye gaye karyon aur dnyan dwara nirdharit hota hai."
rows[133].row = 2575
rows[133].native = "इससे वह अपनी नींद खो देता है।"
rows[133].human = "isse wah apni nind kho deta hai."
rows[134].row = 2598
rows[134].native = "अदी ने इसे जल्दी से उठाया और फेकने का प्रयास किया किन्तु ग्रेनेड ने विस्फोट कर दिया और अदी घायल हो गए।"
rows[134].human = "adi ne ise jaldi se uthaya aur fekne ka pryas kiya kintu Grened ne visphot kar diya aur adi ghayal ho gaye."
rows[135].row = 2609
rows[135].native = "वृद्धावस्था एक धीरे-धीरे आने वाली अवस्था है जो कि स्वभाविक व प्राकृतिक घटना है।"
rows[135].human = "vrudavstha ek dhire-dhire aane wali avstha hai jo ki swabhavik v prakritik ghatna hai."
rows[136].row = 2613
rows[136].native = "फ्रैंक ग्रिलो ऑलरोवि पर"
rows[136].human = "Frank Grilo Aulrovi par"
rows[137].row = 2618
rows[137].native = "सिकल सेल रोग के परिणामस्वरूप रक्ताल्पता तथा ऐसे संकट उत्पन्न हो सकते हैं जो कई प्रकार के होते हैं जैसे वाहिका-पूर्णावरोधक संकट, अविकासी संकट, ज़ब्ती संकट, उच्च अरक्तता संकट, तथा अन्य प्रकार के संकट."
rows[137].human = "sikal cell rog ke parinamswarup raktalpata tatha aise sankat utpann ho sakte hain jo kai prakar ke hote hain jaise vahika-purnavrodhak sankat, aviksi sankat, jbti sankat, ucch arktata sankat, tatha anya prakar ke sankat."
rows[138].row = 2688
rows[138].native = "अथार्त जब दो शब्द आपस में मिलकर कोई तीसरा शब्द बनती हैं तब जो परिवर्तन होता है , उसे संधि कहते हैं।"
rows[138].human = "arthat jab do shabd aapas men milkar koi teesra shabd banati hain tab jo parivartan hota hai , use sandhi kahte hain."
rows[139].row = 2743
rows[139].native = "राजस्थानी रंगमंच पर अब तक जितने भी नाटकों का मंचन हुआ है या तो वे गुमनामी की चादर ओढ़े हुए है या उन्हें दर्शकों तक पहुँचाने में असमर्थता प्रमुख कारण रहा हो..."
rows[139].human = "Rajsthani rangmanch par ab tak jitne bhi natkon ka manchan hua hai ya to ve gumnami ki Chadar odhe huye hai ya unhen darshkon tak pahunchane men asmarthata pramukh karan raha ho…"
rows[140].row = 2753
rows[140].native = "इस दृष्टि से यह संस्था भारतीय भाषाओं की आवाज है।"
rows[140].human = "is drushti se yah sanstha Bhartiy bhashaon ki aawaaj hai."
rows[141].row = 2794
rows[141].native = "२४ जुलाई २०१६ को अल्पमत में आ जाने पर राष्ट्रपति को अपना त्यागपत्र सौंप दिया।"
rows[141].human = "24 Jully 2016 ko alpmat men aa jane par Rashtrapati ko apna tyagpatr saunp diya."
rows[142].row = 2815
rows[142].native = "साथ ही, ये हमले मैदानों में बसे हुए समुदायों पर अपनी ताकत दिखलाने का भी एक तरीका था।"
rows[142].human = "saath hi ye hamle maidanon men base huye samudayon par apni taakat dikhalane ka bhi ek tarikha tha."
rows[143].row = 2822
rows[143].native = "विशेष रूप से, कार्सवेल ने पाए गए चोटों का वर्णन \" शोष के साथ मेरु रज्जु के एक विलक्षण घाव\" के रूप में किया।"
rows[143].human = "vishesh roop se, Karsvel ne paye gaye choton ka varnan \"shosh ke saath Meru rajju ke ek vilkshan ghav\" ke roop men kiya ."
rows[144].row = 2850
rows[144].native = "इसे कृत्रिम-अतिवृद्धि कहा जाता है।"
rows[144].human = "ise krutrim-ativruddhi kaha jata hai."
rows[145].row = 2883
rows[145].native = "वहां एक स्त्री उनके पास आई और बोली -"
rows[145].human = "wahan ek stri unke paas aai aur boli -"
rows[146].row = 2887
rows[146].native = "एजरिन, वाटर्स के एकल एल्बम पर काम करने में असमर्थ थे और इसके बजाए उन्होंने गिल्मर के साथ काम करने का फैसला किया: \"... डेव और मेरे लिए फ़्लॉइड रिकॉर्ड का हमारा संस्करण बनाना अपेक्षाकृत काफी आसान है।\""
rows[146].human = "Yejrin, Waters ke yekal album par kaam karne men asmarth the aur iske bajaye unhone Gilmar ke sath kaam karne ka faisla kiya: \"… Dev aur mere liye flaid record ka hamara sanskaran banana apekshakrut kafi aasan hai.\""
rows[147].row = 2938
rows[147].native = "दलितों को लगने लगा है कि हिंदू धर्म से बाहर निकलना उनके लिए बेहतर रास्ता हो सकता है क्योंकि बीते सालों में नवयान बौद्धों की हालत सुधरी है जबकि हिंदू दलितों की जिंदगी वोट बैंक के रूप संगठित होने के बावजूद ज्यादा नहीं बदली है।"
rows[147].human = "Daliton ko lagne laga hai ki Hindu dharm se bahar nikalna unke liye behatar rasta ho sakta hai kyonki beete salon men Navyaan Bauddhon ki haalat sudhari hai jabki Hindu Daliton ki jindagi vot bank ke roop sangathit hone ke bavjud jyada nahin badli hai."
rows[148].row = 2943
rows[148].native = "किसी भी मात्रा में व्‍यापारी को मुक्‍त खरीददारी करने, भण्‍डारण बिक्री, परिवहन, वितरण, बिक्री करने की अनुमति दी गई है।."
rows[148].human = "kisi bhi matra men vyapari ko mukt khariddari karne, bhandaran bikri, parivahan, vitaran, bikri karne ki anumati di gai hai."
rows[149].row = 2948
rows[149].native = "हमसफ़र, टीम या एकल डाइविंग"
rows[149].human = "Hansafar, team ya ekal daiwing"
rows[150].row = 2954
rows[150].native = "कंपनी ने अपने कायापलट की कहानी रची है।"
rows[150].human = "Company ne apne kayapalat ki kahaani rachi hai."
rows[151].row = 2956
rows[151].native = "प्रत्येक साल नवरात्र के दौरान यहां पर एक बड़े मेले का आयोजन महान देशभक्त के त्याग का गुणगान करने के लिए किया जाता है।"
rows[151].human = "pratyek saal Navratr ke dauran yahan par ek bade mele ka aayojan mahaan deshbhakt ke tyaag ka gungaan karne ke liye kiya jata hai."
rows[152].row = 2960
rows[152].native = "ऋण जोखिम, एक ऐसा जोखिम है कि बाध्यताधारी द्वारा देय पैसे का भुगतान नहीं किया जाएगा."
rows[152].human = "run jokhinm, ek aisa jokhim hai ki badhyatadhari dwara dey paise ka bhugtaan nahin kiya jayega."
rows[153].row = 2963
rows[153].native = "शहरों, कस्बों गाँवों और खेतों के आसपास यह बहुतायत से पाई जाती है।"
rows[153].human = "shahron, kasbon gaonon aur kheton ke aaspaas yah bahutayat se paai jaati hai."
rows[154].row = 2996
rows[154].native = "सालिम अली का जन्म बॉम्बे के एक सुलेमानी बोहरा मुस्लिम परिवार में हुआ।"
rows[154].human = "Salim Ali ka janm Bombey ke ek Sulemani Bohra Muslim pariwaar men huaa."
rows[155].row = 3016
rows[155].native = "भस्मीकरण या उसके समान ऊष्मीय ऑक्सीकरण प्रक्रिया अभी भी आम तौर पर रोगनिदान संबंधी अपशिष्ट और अन्य बहुत विषाक्त और/या संक्रामक चिकित्सा अपशिष्ट के लिए अनिवार्य होती है।"
rows[155].human = "bhasmikaran ya uske samaan ushmiy oxikaran prakriya abhi bhi aam taur par rognidaan sanbandhi apshisht aur any bahut vishakt aur/ya sankraman chikitsa apshisht ke liye anivary hoti hai."
rows[156].row = 3045
rows[156].native = "763 ग्रेगोरी कैलंडर का एक साधारण वर्ष है।"
rows[156].human = "763 Gregori Calender ka ek sadharan varsh hai."
rows[157].row = 3050
rows[157].native = "जो लकडी और लकडी की बनी चीज़ेँ जैसे फर्निचर आदि कुतरकर खा जाते हैँ।"
rows[157].human = "jo lakdi aur lakdi ki bani chijen jaise farnichar aadi katarkar kha jate hain."
rows[158].row = 3080
rows[158].native = "लापुटा के उड़ान द्वीप के खिलाफ लिंडालीनो के सतही शहर के विद्रोह को बताने वाला, भाग III का छोटा एपिसोड (पांच पैराग्राफ से युक्त), ड्रेपियर्स लेटर्स के लिए स्पष्ट रूप से अन्योक्तिपरक था, जिस पर स्विफ्ट को गर्व था।"
rows[158].human = "Laputa ke udaan dwip ke khilap Lidalino ke satahi shahar ke vidroh ko batane wala, bhag ||| ka chhota Episod (panch pairagraf se yukt), Drepiyars letars ke liye spasht roop se anyoktiparak tha, jis par swift ko garv tha."
rows[159].row = 3091
rows[159].native = "वर्त्तमान में डॉ॰ विनायक पाण्डेय यह दायित्व निभा रहे है।"
rows[159].human = "vartmaan men Dr. Vinayak Pandey yah dayitw nibha rahe hai."
rows[160].row = 3095
rows[160].native = "कर्म के परिणाम या उसके अभाव को नियंत्रित करने में दैवीय शक्ति की भूमिका के बारे में हिंदू धर्म में कई भिन्न प्रकार के दर्शन हैं, कुछ का स्वरूप आज भी वर्तमान है और कुछ ऐतिहासिक हैं।"
rows[160].human = "karm ke parinaam ya uske abhaav ko niyantrit karne men daiviy shakti ki bhumika ke baare men Hindu darm men kai bhinn prakar ke darshan hain, kuchh ka swarup aaj bhi vartmaan hai aur kuchh aitihasik hai."
rows[161].row = 3096
rows[161].native = "हेल (अंग्रेज़ी: Hale) एक उत्तर लंदन में बार्नेट बरो का जिला है।"
rows[161].human = "Hel (angreji; Hale) ek uttar London men Barnet Baro ka jila hai."
rows[162].row = 3100
rows[162].native = "इन गतिविधियों का विवरण देते हुए, जाधव ने कहा:"
rows[162].human = "in gatividhiyon ka vivran dete huye, Jadhav ne kaha:"
rows[163].row = 3141
rows[163].native = "२०१५ में उन्होंने पंजाबी फिल्म \"अंग्रेज़\" से अपना फ़िल्मी करियर शिरू किया।"
rows[163].human = "2015 men unhone Panjabi film \"Angrej\" se apna filmi kariyar shiru kiya."
rows[164].row = 3193
rows[164].native = "कथाकार की कल्पना अब सीमाबद्ध हो गई।"
rows[164].human = "kathakar ki kalpna ab seemabaddh ho gai."
rows[165].row = 3218
rows[165].native = "राज एक्सप्रेस भारत में प्रकाशित होने वाला हिंदी भाषा का एक समाचार पत्र (अखबार) है।"
rows[165].human = "Raaj express Bharat men prakashit hone wala Hindi bhasha ka ek samachar patr (akhabaar) hai."
rows[166].row = 3235
rows[166].native = "कुछ समय बाद उसके नाना भी नहीं रहे।"
rows[166].human = "kuchh samay baad uske nana bhi nahin rahe."
rows[167].row = 3267
rows[167].native = "इस गुरुशिष्य-परम्परा को सुनियोजित रूप देते हुए संस्कृत के अनेक अध्ययन केन्द्र देश भर में चलते रहे उसी परम्परा में ही 20 वीं सदी में अनेक संस्कृत विश्वविद्यालय स्थापित हुए।"
rows[167].human = "is gurishishy-parmpara ko suniyojit roop dete hua Sanskrut ke anek adhyayan kendr desh bhar men chalte rahe usi parampara men hi 20 vu sadi men anek Sanskrut vishwavidyalay sthapit huye."
rows[168].row = 3347
rows[168].native = "2005 में एंजल जलप्रपात पर पैरामोटर का उनका प्रयास, होप एण्ड होम्स फॉर चिल्ड्रेन चैरिटी की मदद के लिए था।"
rows[168].human = "2005 men anjal jalprapaat par pairamotar ka unka prayas, hop and homes for chidren charity ki madad ke liye tha."
rows[169].row = 3367
rows[169].native = "उत्तराखण्ड राज्य राजमार्ग ४० दो अलग अलग मार्गों के नाम से प्रख्यात है; पहला कालाढूंगी रोड, जो मंगल पड़ाव से शुरू होकर पश्चिम की ओर कालाढूंगी होते हुए रामनगर तक जाता है, और दूसरा चोरगलिया रोड, जो काठगोदाम से शुरू होकर दक्षिण की ओर चोरगलिया होते हुए सितारगंज तक जाता है।"
rows[169].human = "Uttarakhand rajy rajmarg 40 do alag alag margon ke naam se prakhyat hai; pahla Kaladhungi rod, jo Mangal padav se shuru hokar pashchim ki aur Kaladhungi hote huye Ramnagar tak jata hai, aur dusra Chorgaliya rod, jo Kathgodam se shuru hokar Dakshin ki aur Chorgaliya hote huye Sitarganj tak jata hai."
rows[170].row = 3415
rows[170].native = "पाकिस्तानी इंटर सर्विसेज इंटेलिजेंस ने बगावत को प्रोत्साहित किया और समर्थन किया।"
rows[170].human = "Pakisthani Inter sarvices Inteligence ne bagavat ko protsahit kiya aur samrthan kiya."
rows[171].row = 3416
rows[171].native = "उनकी तपोभूमि धारा नगरी में उनकी तपस्या और साधना से प्रसन्न हो कर माँ सरस्वती ने स्वयं प्रकट हो कर दर्शन दिए।"
rows[171].human = "unki tapobhumi dhara nagri men unki tapsya aur sadhna se prasann ho kar maa Sarswati ne swayn prakat ho kar darshan diye."
rows[172].row = 3422
rows[172].native = "भारतीय मीडिया ने सरकारी सूत्रों का हवाला दिया कि जाधव का ईरान में कार्गो व्यवसाय था और वह बंदर अब्बास और चाबहार बंदरगाहों से काम कर रहा था।"
rows[172].human = "Bhartiy midiya ne sarkari sutron ka havala diya ki Jadhav ka Iran men kargo vyavsaay tha aur wah Bandar Abbas aur Chabhar banargahon se kaam kar raha tha."
rows[173].row = 3461
rows[173].native = "मसलन अक्टूबर १९६२ में हुए क्यूबाई मिसाइल संकट में सोवियत संघ और संयुक्त राज्य अमेरिका के बीच तनाव लगातार बढ़ता गया और अगर कोई पीछे न हटता हो परमाणु प्रलय हो सकता था, लेकिन उसमें सोवियत संघ ने पीछे पाँव खींच लिए।"
rows[173].human = "Maslan Octomber 1962 men huye Qubai misail sankat men Soviyat sangh aur sanyukt rajy America ke beech tanav lagataar badhta gaya aur agar koi pichhe n hatata ho paarmanu pralay ho sakta tha, lekin usmen Soviyat sangh ne pichhe pav khinch liye."
rows[174].row = 3470
rows[174].native = "इसी कल्पना के आधार पर मिस्र में सूर्य की आदिकल्पना तथा मूर्तिविधान में सूर्य को सपक्ष आभामंडल (्ध्रत्दढ़ड्ढड्ड द्मद्वद ड्डत्द्मत्त्) के रूप में माना गया।"
rows[174].human = "isi kalpna ke aadhar par Misr men Sury ki aadikalpna tatha murtividhan main Sury ko sapksh aabhamandal (udhtdtdhdddhddd yaddvd idtdhtthu) ke roop men mana gaya."
rows[175].row = 3518
rows[175].native = "बुंदेलखंड का राजविद्रोह वास्तव में जनता का विद्रोह न होकर सामन्तों और सेना का विद्रोह था इसी पृष्ठभूमि में सांस्कृतिक और धार्मिक भावना के साथ साथ स्वामिभक्ति का पुट विशेष है।"
rows[175].human = "Bundelkhand ka rajvidroh vastav men janta ka vidroh n hokar samantton aur sena ka vidroh tha isi prushtbhumi men sanskrutik aur dharmik bhavna ke sath sath Swamibhakti ka put vishesh hai."
rows[176].row = 3549
rows[176].native = "लखनऊ जिला जेल, जो उन दिनों संयुक्त प्रान्त (यू॰पी॰) की सेण्ट्रल जेल कहलाती थी, की ११ नम्बर बैरक में सभी क्रान्तिकारियों को एक साथ रक्खा गया और हजरतगंज चौराहे के पास रिंग थियेटर नाम की एक आलीशान बिल्डिंग में अस्थाई अदालत का निर्माण किया गया।"
rows[176].human = "Lakhanau jila jel, jo un dinon sanyukt prant (U.P.) ki central jel kahlati thi, ki 11 nambar bairak men sabhi krantikariyon ko ek sath rakkha gaya aur Hajaratganj chaurahe ke paas Ring theater naam ki ek aalishan bilding men asthai adalat ka nirmaan kiya gaya."
rows[177].row = 3565
rows[177].native = "1985 में यह संयुक्त राष्ट्र का विशिष्ट अभिकरण बन गया।"
rows[177].human = "1985 men yah Sanyukt Rashtr ka vishisht abhikaran ban gaya."
rows[178].row = 3595
rows[178].native = "श्री जगन्नाथ संस्कृत विश्वविद्यालय का जालघर"
rows[178].human = "Shri Jagnnath Sanskrut Vishwavidyalay ka jaalghar"
rows[179].row = 3610
rows[179].native = "ये हैं हाउस स्पैरो, स्पेनिश स्पैरो, सिंड स्पैरो, रसेट स्पैरो, डेड सी स्पैरो और ट्री स्पैरो।"
rows[179].human = "ye hain House Sparo, Spenish, Sparo, Sind Sparo, Raset Sparo, Ded C Sparo aur Tree Sparo."
rows[180].row = 3615
rows[180].native = "बांग्लादेशी महिलाओं और लड़कियों को पुरुषों के रूप में हर जगह आंदोलन की आजादी का अधिकार नहीं मिलता है, समाज पितृसत्तात्मक मूल्यों और महिलाओं और लड़की की स्वतंत्रता के प्रति सामाजिक रूढ़िवादी नीतियों पर आधारित है|"
rows[180].human = "Bangadeshi Mahilaon aur Ladkion ko Purushon ke roop men har jagah aandolan ki aajadi ka adhikar nahin milta hai, samaj pitrusattatmak mulyon aur Mahilaon aur Ladki ki swantrata ke prati samajik rudhiwadi nitiyon par aadharit hai."
rows[181].row = 3667
rows[181].native = "यह एक छोटी-सी गर्त भूमि पर है जहां वर्षा का पानी जमा हो जाता है जो कुछ महीनों तक भरा रहता है और बाद में सूख जाता है।"
rows[181].human = "yah ek chhoti-si gart Bhumi par hai jahan Varsha ka pani jama ho jata hai jo kuchh Mahinon tak bhara raahta hai aur baad men sukh jata hai."
rows[182].row = 3668
rows[182].native = "मानव जीवन का मनोवैज्ञानिक विकास पर चर्चा करने के लिए एरिक एरिकस ने मनोसामाजिक विकास के अपने चरणों का प्रसताव दिया।"
rows[182].human = "Maanav jeevan ka Manovaidhnyanik vikas par charcha karne ke liye Arik Aricus ne Manosamajik vikaas ke apne charnon ka prastav diya."
rows[183].row = 3682
rows[183].native = "बाद में सन् 1935 में बालक और बालिकाओं दोनों के लिये बंबई में वीदृ पीदृ कामथ ने मराठी और कन्नड़ में बिने स्केल की रचना की।"
rows[183].human = "baad men san 1935 men balak aur baalikaon donon ke liye bambai men vitt pitt kamath ne marathi aur kannade men bine skel kii rachna kii."
rows[184].row = 3705
rows[184].native = "हालांकि बैरेट उनके मुख्य गीतकार थे, वाटर्स और राइट ने नई सामग्री तैयार की, जैसे कि \"इट वुड बी सो नाइस\" और \"केयरफुल विथ दैट एक्स, यूजीन\"."
rows[184].human = "hanaanki Bairet unke mukhy geetkaar the, Waters aur Wrie ne naii samgri taiya kii, jaise ki \"It would be so nice\" aur \"Careful with that ax, Yugin.\"."
rows[185].row = 3726
rows[185].native = "जो न केवल ब्राह्मणवादी व मनुवादी साहित्यिक संकल्पना है बल्कि व्यक्तिगत महिमामंडन और अवैज्ञानिक भी है।"
rows[185].human = "jo na keval brahmanwadi v vanuwadi sahitiyaik sankalpna hai bali yaktigat mahimamandan aur avaigyanki bhi hai."
rows[186].row = 3732
rows[186].native = "टामस एक्विनस की धारणा थी कि ज्ञान के कुछ क्षेत्र विश्वास के ही विषय हैं; इसपर भी इंद्रियदत्त ज्ञान उन मूल नियमों की सहायता से, जो प्रत्येक की सक्रिय बुद्धि में विद्यमान हैं, विश्व और परमात्मा के स्वरूप के विषय में कुछ बता सकता है।"
rows[186].human = "Tomas Aquinas kee dhaarna thee ki gyan ke kuchh kshetr vishwas ke hi vishay hain; ispar bhi indirydatt gyan un mool niyamon kee sahayata se, jo pratyek kii sakriy buddi men vidyaman hain, vishv aur pramatma ke swarup ke vishay men kuchh bata sakta hain."
rows[187].row = 3741
rows[187].native = "शेयरसन लोएब रोड्स, स्वयं ही १९७० के दशक में कई विलयों का जनक था, जिनमें १९७४ का वेइल्स हेडन, स्टोन एंड कंपनी का शेयरसन हेडन स्टोन से शेयरसन, हैम्मिल एंड कंपनी के साथ किया गया विलय शामिल है।"
rows[187].human = "Sheyson Loab Rhods, swaym hi 1970 ke dashak men kaii vilayon ka janak tha, jinmen 1974 ka Wedls Heden, Stone & Company ka Sheyarson Heden Stone se Sheyarson, Hammil & Company ke sath kya gya vilay shamil hai."
rows[188].row = 3770
rows[188].native = "अत: यह मत साक्ष्यसंमत नहीं प्रतीत होता।"
rows[188].human = "atah yah mat sakshysammat nahin pratit hota."
rows[189].row = 3799
rows[189].native = "सन्‌ १९१२ में गुरुद्वारा ठीकरीवाल का शिलान्यास किया गया।"
rows[189].human = "san 1912 men gurudwara Theekariwal ka shilanyas kiya gaya."
rows[190].row = 3809
rows[190].native = "1987 में, अमेरिकन एक्सप्रेस ने अपना पहला क्रेडिट कार्ड उत्पाद, ऑप्टिमा कार्ड प्रस्तुत किया।"
rows[190].human = "1987 men, American Express ne apna pahla Credit Card utpaad, Optima Card prastut kiya."
rows[191].row = 3842
rows[191].native = "करण मल्होत्रा, भारतीय फ़िल्म निर्देशक तथा लेखक"
rows[191].human = "Karan Malhotra, Bhartiy Film nirdeshak tatha Lekhak"
rows[192].row = 3847
rows[192].native = "जब वह 15 साल की थी तब लक्ष्मी पर एसिड अटैक हुआ था।"
rows[192].human = "jab wah 15 saal ki thi tab Laxmi par Acid Attack hua tha."
rows[193].row = 3893
rows[193].native = "दौरा इस अवसर पर, नज़दीक था।"
rows[193].human = "daur is avasar par, najdik tha."
rows[194].row = 3924
rows[194].native = "यह ट्वेंटी-20 में रनों के मामले में पाकिस्तान की सबसे बड़ी जीत थी।"
rows[194].human = "yah Twenty-20 men ranon ke mamle men Pakisthan ki sabse badi jeet thi."
rows[195].row = 3965
rows[195].native = "फिर चाचा ने विशाल को गोली मारने की कोशिश में अरुण को गोली मार दी।"
rows[195].human = "fir Chacha ne Vishal ko goli marne ki koshish men Arun ko goli maar di."
rows[196].row = 3993
rows[196].native = "वह कप्तान जो तीसरी विनाशकारी यात्रा में गुलिवर को अपने जहाज पर सर्जन का काम करने के लिए आमंत्रित करता है, उसका नाम रोबिनसन है।"
rows[196].human = "wah kaptaan jo teesri vinashkaari yatra men Guliwar ko apne Jahaaj par sarjan ka kaam karne ke liye aamantrit karta hai, uska naam Robonson hai."
rows[197].row = 4022
rows[197].native = "जैन धर्म बाहुबली"
rows[197].human = "Jain Dharm Bahubali"
rows[198].row = 4026
rows[198].native = "रमैनी में चार स्थलों पर जीवों को चेतावनी दी गई हैं।"
rows[198].human = "Ramaini men char sthalon par jeevon ko chetawani di gai hain."
rows[199].row = 4033
rows[199].native = "कनाडा में, चॅक के आकार और प्रकार - और साथ ही परांकन अपेक्षाएं तथा MICR छूट पर कैनेडियन पेमेंट्स एसोसिएशन (CPA) की निगरानी रहती है।"
rows[199].human = "Canada men, chek ke aakar aur prakar - aur sath hi parankan apekshayen tatha MICR chhut par Canedian Pements Asosiation (CPA) ki nigrani rahti hai."
rows[200].row = 4058
rows[200].native = "यहां हम आपको बताते चलें कि मगध के सबसे प्राचीन वंश के संस्थापक का नाम भी"
rows[200].human = "yahan ham aapko batate chalen ki Magadh ke sabse Prachin Vansh ke Sansthapak ka naam bhi"
rows[201].row = 4070
rows[201].native = "जाबिर हुसैन ने डायरी विधा में एक अभिनव प्रयोग किया है जो"
rows[201].human = "Jabir Husain ne dayri Vidha men ek Abhinav prayog kiya hai jo"
rows[202].row = 4071
rows[202].native = "इस वंश के सम्राटों के संस्कृत नाम थे।"
rows[202].human = "is Vansh ke Samraton ke Sanskrut naam the."
rows[203].row = 4090
rows[203].native = "लक्ष्मणगढ़ दुर्ग सीकर से 30 किलोमीटर की दूरी पर स्थित है।"
rows[203].human = "Laxmangadh Durgh Seekar se 30 kilometer ki duri par sthit hai."
rows[204].row = 4130
rows[204].native = "साहित्यिक रूप से फ्रेंच कल्पना में बोहीमियन लोग घुमंतू रोमानी लोगों से सम्बंधित माने जाते थे (ऐसा माना जाता था की वे बोहेमियासे आये हैं), पारंपरिक समाज से हटकर और उनकी असम्मती से बेफिक्र।"
rows[204].human = "Sahityik roop se French kalpana men Bohimian Log Ghumantu Romaani logon se sambdhit mane jate the (aisa mana jata tha kee we Bohemiyase aaye hain), paramparik Samaaj se hatkar aur unki asammati se Befikr."
rows[205].row = 4163
rows[205].native = "नागों द्वारा स्थापित शिवाल्यों के अवशेष भ्रमरा (नागौद) बैजनाथ (रीवाँ के पास) कुहरा (अजयगढ़) में अब भी मिलते हैं।"
rows[205].human = "nagon dwara sthapit Shivalyon ke avshesh Bhramara (Nagaud) Baijynaath (Reevon ke paas) Kuhra (Ajaygadh) men ab bhi milte hain."
rows[206].row = 4164
rows[206].native = "तुरंत उपयुक्त चिकित्सा अपेक्षित है।"
rows[206].human = "turant upyukt chikitsa apekshit hai."
rows[207].row = 4165
rows[207].native = "कई स्ट्रेपसिराइनी प्राणियों के जबड़ों के सामने के निचले दांत कंघी जैसी व्यवस्था में होते हैं जिनसे वे अपने बाल सँवार सकते हैं।"
rows[207].human = "kai Strepsirrhine praniyon ke jabdon ke saamne ke nichale Dant Kanghi jaisi vyavsta men hote hain jinse we apne baal sanvaar sakte hain."
rows[208].row = 4171
rows[208].native = "उसके ठीक बाद क्या हुआ यह अस्पष्ट बना हुआ है।"
rows[208].human = "uske thik baad kya hua yah aspsht bana hua hai."
rows[209].row = 4172
rows[209].native = "इस वजह से, विषम युग्मज में, दोनों सम युग्मज की तुलना में उच्च फिटनेस होगी."
rows[209].human = "is wajah se, Visham Yugmaj men, donon sam Yugmaj ki tulna men ucch Fitness hogi."
rows[210].row = 4187
rows[210].native = "भविष्य का धर्म एवं दर्शन"
rows[210].human = "bhavishy ka dharm evm darshan"
rows[211].row = 4194
rows[211].native = "इन में शामिल हैं, सरकार के प्रकाशन, पद के आदेश, मंत्री नियमों और नगर निगम के द्वारा-कानूनों."
rows[211].human = "in men shamil hain, sarkar ke prakashan, pad ke aadesh, manti niyamon aur nagar nigam ke dwara-kanoonon"
rows[212].row = 4227
rows[212].native = "यह अवश्य है कि, मलूकदास धरमदास, दादूदयाल, नानक, आदि भक्तों के संबंध में 'भक्तमाल' में कुछ नहीं कहा गया।"
rows[212].human = "yah avashya hai ki, Malukdas Dharmadas, Daddyaal, Nanak, aadi bhakto ke sambandh men 'Bhaktmaal' men kuchh nahin kaha gaya."
rows[213].row = 4229
rows[213].native = "मगर यदा कदा इन्हें गैर आदिवासी साबित करने की कोशिश किया जाना एवं इसके लिये तरह तरह के छोटी-मोटी गलतियां ढ़ूंढ़ने और उसे ऐन-केन-प्रकारेण सही साबित करने की कोशिश करना अत्यंत दुर्भाग्यपूर्ण है।"
rows[213].human = "magar yada kada inhne fair aadivasi sabit karne ki koshish kiya jana evm iske liye tarah tarah ke chhoti-moti galatiyan dhoondhne aur use ain-ken-prakaren sahi saabit karne kii koshish karna atyant durbhagyapoorn hai."
rows[214].row = 4245
rows[214].native = "तृतीय शताब्दी ईo पूo के उत्तरार्ध में जीवित था।"
rows[214].human = "tritiy shatabdi ee poo ke uttrardh men jeevit thaa."
rows[215].row = 4252
rows[215].native = "उड़ी, जम्मू और कश्मीर"
rows[215].human = "Udi, Jammu aur Kashmir"
rows[216].row = 4260
rows[216].native = "इनके अतिरिक्त अन्य कई पेड़ों और लताओं से भी रबर प्राप्त होता है।"
rows[216].human = "inke atirikt anya kaii pedon aur lataon se bhi rabar prapt hota hai."
rows[217].row = 4268
rows[217].native = "इस प्रकार हैहय वंशी राजाओं के शिवनाथ के उत्तर में अठारह और शिवनाथ के दक्षिण में अठारह अर्थात् छत्तीस गढ़ हो गये और यही इस क्षेत्र का 'छत्तीसगढ़' कहलाने का कारण बना।"
rows[217].human = "is prakar haihay vanshi rajaaon ke Shivnath ke uttar men atharah aur Shivnath ke dakshin men atharah arthat Chhatis Gadh ho vaye aur yahi is kshetr ka 'Chhatisgadh' kahlane ka karan bana."
rows[218].row = 4287
rows[218].native = "मुख्य मेला अष्टमी को प्रारंभ होता है।"
rows[218].human = "mukhy mela ashtmi ko prarambh hota hai."
rows[219].row = 4288
rows[219].native = "चेरुश्शेरि ने अपने पूर्ववर्ती लेखकों द्वारा प्रयुत्त संस्कृत एवं तमिल छंदों का बहिष्कार किया है।"
rows[219].human = "Cherusshere ne apne poorvarti lekhakon dwara prayukt sanskrit evm tamil chhandon ka bahishkar kiya hai."
rows[220].row = 4302
rows[220].native = "भारतीय पशु और पक्षी"
rows[220].human = "bhariya pashu aur pakshi"
rows[221].row = 4306
rows[221].native = "वह समाज कर्मसिद्धांत पर आधारित था।"
rows[221].human = "vah samaj karmshiddhan par aadharit thaa."
rows[222].row = 4313
rows[222].native = "चेरुशेरी मलयालम में कविता लेखन के गाधा शैली के प्रवर्तक है।"
rows[222].human = "Chrusheri malyalam men kavit lekhan kee gaadha shaili ke prvarak hai."
rows[223].row = 4317
rows[223].native = "मुस्लिम की पुस्तक कद में धीरे-धीरे बढ़ी है, जैसे कि सुन्नी मुसलमानों में हदीस का सबसे प्रामाणिक संग्रह माना जाता है, सहीह बुख़ारी के बाद दूसरा स्थान प्राप्त किया है।"
rows[223].human = "mulsmi kii pustak kad men dheere-dheere badhi hai, jais ki sunni musalmaanon me hadis ka sabse pramanik sangrah mana jata hai, Sahih Bukhari ke baad doosra shtan prapt kiya his."
rows[224].row = 4325
rows[224].native = "ललित कला अकादमी द्वारा \"फाड़ चित्रकारी और श्री लाल जोशी\""
rows[224].human = "Lalti Kala Akadami dwara \"Faad Chitrakari aur Shri Lal Joshi\""
rows[225].row = 4327
rows[225].native = "सातवाहनों के पश्चात इक्ष्वाकु नरेशों ने यहाँ राज्य किया।"
rows[225].human = "saatvahanon ke pashchatg icchaku narshon ne yahan rajy kiya."
rows[226].row = 4346
rows[226].native = "गोविन्द मिश्र अनेक प्रतिष्ठित संस्थाओं द्वारा पुरस्कृत सम्मानित किया गया है।"
rows[226].human = "Govind Mishr anek pratishthit sansthaon dwara purskirt sammanit kiya gaya hai."
rows[227].row = 4410
rows[227].native = "वे सभी उज़बेक समुदाय से हैं और अपने गानों में उज़्बेकिस्तान की लोक-धुनों और कविताओं का मिश्रण करते हैं।"
rows[227].human = "ve sabhi Ujbek samuday se hai aur apne ganon men Ujbekistan kii log-dhunon aur kavitaaon ka mishran karte hain."
rows[228].row = 4415
rows[228].native = "इसमें एक बड़ा क़दम जागीरदारों को हटाना था, जिनका झोऊ ज़माने में हर किसान मोहताज होता था।"
rows[228].human = "ismen ek bada kadam jaagirdaarohn ko hatana tha, jinka jhou jamane men har kisan mohtaj hota tha."
rows[229].row = 4428
rows[229].native = "प्रथम शताब्दी में यहाँ सातवाहन नरेशों का राज्य था।"
rows[229].human = "pratham shatabdi men yahan saatvahan nareshon ka rajy tha."
rows[230].row = 4441
rows[230].native = "संख्या सिद्धान्त और ज्यामिति जैसे अन्य क्षेत्रों से योगदान के बाद, समूह धारणा को सामान्यीकृत और दृढ़तापूर्वक 1870 के आसपास स्थापित किया गया था।"
rows[230].human = "sankya siddhant aur jyamiti jaise anya kshetron se yogdan ke baad, samuh dharanaa ko samavikrit aur dridhtapurvak 1870 ke aaspaas sthapit kiya gaya tha."
rows[231].row = 4454
rows[231].native = "गर्भावस्था बीमारी के पुनरावर्तन के प्रति अतिसंवेदनशीलता को प्रभावित कराती है जिसमें गर्भावस्था के प्रत्येक त्रिमास में बीमारी के पुनरावर्तन की दर निम्न होती है।"
rows[231].human = "garbhavastha bimari ke punravartan ke prati atisanvedansheelta ko prabhavit karati hai jismen garbhavstha ke prtyek trimas me bimari ke punarvartan kii dar nimn hoti hai."
rows[232].row = 4478
rows[232].native = "वह विशुद्ध चैतन्य स्वरूप की ओर अग्रसर हो रहा होता है।"
rows[232].human = "vah vishuddh chaitanya swarup ki or agrasar ho raha hota hai."
rows[233].row = 4505
rows[233].native = "वे राजमहल की पहाड़ियों के इर्द-गिर्द रहा करते थे।"
rows[233].human = "ve rajmahl kii pahadiyon ke ird-grid raha karte the."
rows[234].row = 4533
rows[234].native = "यह ऊमेनेट नामित निगम द्वरा शहर में बिजली और इंटरनेट के सेवाएं प्रदान करती है।"
rows[234].human = "yan Umnet namit nigak dwara shahar men bijli aur internet ke sevayen pradan karti hai."
rows[235].row = 4568
rows[235].native = "‘अग्निपुराण’ में मुक्तक को परिभाषित करते हुए कहा गया कि:"
rows[235].human = "Agnipuraan' men muktak ko paribhashit karte huye kaha gaya ki:"
rows[236].row = 4572
rows[236].native = "संदर्भ को परिभाषित करने की इस प्रारंभिक प्रक्रिया के बाद, संदर्भ का मूल्यांकन स्थल की विस्तृत जानकारी के सम्बन्ध में इसलिए किया जाता है कि जिससे स्थल को चरणों में बांटने की आवश्यकता को जांचा जा सके, इसके पश्चात इसे विभिन्न तरीकों से हटाया व रिकॉर्ड किया जाता है।"
rows[236].human = "sandarbh ko paribhashit karne ki is prarambhik prakriya ke baad, sandarbh ka mulyankan Sthal ki vistrut jankari ke sambandh men isliye kiya jata hai ki jisse Sthal ko charnon men bantane ki aavshyakta ko jancha ja sake, iske pashchat ise vibhinn tarikon se hataya v Record kiya jata hai."
rows[237].row = 4579
rows[237].native = "मुंबई में बहुत से समाचार-पत्र, प्रकाशन गृह, दूरदर्शन और रेडियो स्टेशन हैं।"
rows[237].human = "Mumbai men bahut se Samachaar-Patr, Prakashan Gruh, Doordarshan aur Redio station hain."
rows[238].row = 4593
rows[238].native = "१९३१ में पार्कर क़ूईक्क् (त्वरित सुखाने स्याही) जो ब्बॉळ्टीण्ग्ग लिए की आवश्यकता समाप्त बनाया।"
rows[238].human = "1931 men Parker Quink (twarit sukhane syahi) jo Boltignh liye ki aavshyakta samapt banaya."
rows[239].row = 4595
rows[239].native = "एक संविदागत अनुबंध, जिसमें संविदा दिनांक को पूर्व-निर्धारित ब्याज दरों पर ब्याज दर राशि का निपटान निर्दिष्ट होता है।"
rows[239].human = "ek Sanvidagat Anubandh, jismen Sanvidha Dinank ko purv-nirdharit byaaj daron par byaaj dar Rashi ka niptaan nirdisht hota hai."
rows[240].row = 4674
rows[240].native = "उपनिवेशवादियों को मजबूरन नक्रूमा को सत्तारूढ़ होने के लिए जेल से रिहा करना पड़ा।"
rows[240].human = "upniveshvadiyon ko majburan nkrumah ko sattarudh hone ke liye jel se riha karna pada."
rows[241].row = 4710
rows[241].native = "शुक्राणु की सूक्ष्म पता लगान"
rows[241].human = "shukranu ki sukshma pata lagan."
rows[242].row = 4718
rows[242].native = "हिन्दुस्थान समाचार (यूनिकोडित)"
rows[242].human = "hindustan samachaar (unicodit)"
rows[243].row = 4725
rows[243].native = "संसार में दांपत्य जीवन में प्राय: एकपत्नीत्व ही सबसे अधिक प्रचलित है, यद्यपि अनेक समाजों में पुरुषों को एक से अधिक पत्नियाँ रखने की भी छूट है।"
rows[243].human = "sansaar mein dampatya jeevan mein prayah ekpatnitva hi sabse adhik prachalit hai, yadyapi anek samaajon mein purushon ko ek se adhik patniya rakhne ki bhi chhut hai."
rows[244].row = 4726
rows[244].native = "अत्यधिक काटा जाना चरण को लापरवाही के साथ हटाया जाना परिलक्षित करता है।"
rows[244].human = "atyadhik kata jana charan ko laparwahi ke saath hataya jana parilakshit karta hai."
rows[245].row = 4842
rows[245].native = "उत्तम कोटि के पादप, जैसे अनावृतबीजी तथा आवृतबीजी की लगभग ३०,००० जातियाँ इस देश में पाई जाती हैं।"
rows[245].human = "uttam koti ke padap, jaise anavritabiji tatha aavritabiji ki lagabhag 30,000 jatiyan is desh mein pai jaati hain."
rows[246].row = 4875
rows[246].native = "उनके दो बेटे हैं।"
rows[246].human = "unke do bete hain."
rows[247].row = 4878
rows[247].native = "बिबर प्रबेस कीन्ह जेहि भाँती। कपिन्ह बहोरि मिला संपाती।।"
rows[247].human = "bibar prabes kinh jehi bhaanti. kapinh bahori milaa sanpaati.."
rows[248].row = 4932
rows[248].native = "बातों ही बातों में उस अधिकारी को वीडिओ फूटेज दिखा दिए। .."
rows[248].human = "baaton hi baaton mein us adhikaari ko vidio footage dikhaa diye. .."
rows[249].row = 4938
rows[249].native = "एक समय पूडल अधिक लंबे बालों वाले हुआ करते थे, जो कि पुर्तगाली समुद्री कुत्ते की एक किस्म है।"
rows[249].human = "ek samay pudal adhik lambe baalon wale huaa karte the, jo ki purtagaali samudri kutte ki ek kism hai."
rows[250].row = 4958
rows[250].native = "यह सूची एशिया के देशों के शहरों की है:-"
rows[250].human = "yah suchi Asia ke deshon ke shaharon ki hai:-"
rows[251].row = 5044
rows[251].native = "उन्‍होने अपने कैरियर के दौरान एक चावल की 19,000 प्रजातियाँ एकत्र की थी।"
rows[251].human = "un‍hone apne career ke dauraan ek chaval ki 19,000 prajatiyan ektra ki thi."
rows[252].row = 5052
rows[252].native = "लेसोथो नाम मोटे तौर पर \"सेसोथो बोलने वाले लोगों की भूमि\" का अनुवाद करता है।"
rows[252].human = "Lesotho naam mote taur par \"sesotho bolne wale logon ki bhumi\" ka anuvaad karta hai."
rows[253].row = 5080
rows[253].native = "1945 के बाद ही अंग्रेज़ों ने मलाया के अनुदारपंथी परम्परागत शासकों के साथ गठजोड़ करके एक केंद्रीकृत प्रशासन खड़ा कर लिया था।"
rows[253].human = "1945 ke baad hi angrejon ne malaya ke anudarpanthi paramparagat shaaskon ke saath gathjode karke ek kendrikrit prashasan khada kar liya tha."
rows[254].row = 5102
rows[254].native = "उर्दू कहानीकार राजेन्द्र सिंह बेदी - नन्द किशोर विक्रम"
rows[254].human = "Urdu kahanikaar Rajendra Singh Bedi - Nand Kishor Vikram"
rows[255].row = 5113
rows[255].native = "इसे लौकिक, शास्त्र, पहाड़ी या कच्चा संवत्‌ भी कहते हैं।"
rows[255].human = "ise laukik, shastra, pahadi ya kachcha samvata bhi kahte hain."
rows[256].row = 5119
rows[256].native = "इंटरसिटी एक्स्प्रेस 3503 भारतीय रेल द्वारा संचालित एक मेल एक्स्प्रेस ट्रेन है।"
rows[256].human = "intercity express 3503 bhartiya rail dwaraa sanchalit ek mail expres train hai."
rows[257].row = 5122
rows[257].native = "(2) संसारगत कार्य-कारण-नियम को जगत् पर लागू करके यह कहा जाता है कि जैसे यहां प्रत्येक कार्य के उपादान और निमित्त कारण होते हैं, उसी प्रकार समस्त जगत् का उपादान और निमित्त कारण भी होना चाहिए और वह ईश्वर है (कास्मोलॉजिकल, अर्थात् सृष्टिकारण युक्ति)।"
rows[257].human = "(2) sansargat kary-kaaran-niyam ko jagat par lagu karke yah kaha jata hai ki jaise yahan pratyek kary ke upaadaan aur nimitt kaaran hote hain, usi prakaar samast jagat kaa upaadaan aur nimitt kaaran bhi hona chahiye aur vah ishwar hai (cosmological, arthaat sristikaaran yukti)."
rows[258].row = 5124
rows[258].native = "कुछ परंपरा में आकाश देवता को नारी रूप में मान्यता प्राप्त हैं।"
rows[258].human = "kuchh paramparaa mein aakash devta ko naari roop mein manyataa prapt hain."
rows[259].row = 5129
rows[259].native = "गढिया किले के पूर्वी दिशा मे स्थित द्वार धरमदेव राजा के नाम पर धरम द्वार कहलाता था।"
rows[259].human = "Gadhiyaa kile ke purvi disha me sthit dvaar Dharamdev raja ke naam par dharam dvaar kahlata tha."
rows[260].row = 5150
rows[260].native = "अधिक खतरनाक है, लेकिन बहुत कम आम हैं इंटरफेरॉन से होने वाली गुर्दे की क्षति; ह्रदय संबंधी गंभीर विषाक्तता, बांझपन और माइटॉक्सैनट्रोन kaa गंभीर मज्जाभ (myeloid) ल्यूकेमिया, और नैतैलीज़ुमैब (natalizumab) एवं तेजी से फैलने वाले बहुकेंद्रीय मस्तिष्क संबंधी ल्यूकेमिया के बीच विख्यात संबंध."
rows[260].human = "adhik khatarnaak hai, lekin bahut kam aam hain Interferon se hone wali gurde ki kshati; hriday sambandhi gambhir visaaktataa, baanjhpan aur Mitoxantrone ka gambhir majjaabh (myeloid) Leukaemia, aur Natalizumab (natalizumab) evam teji se failne wale bahukendriy mastisk sambandhi leukaemia ke bich vikhyaat sambandh."
rows[261].row = 5168
rows[261].native = "शहरों की सूची"
rows[261].human = "shaharon ki suchi"
rows[262].row = 5194
rows[262].native = "न्याय मंजरी पदवाक्यप्रमाणपारावरीणजरन्नैयायिक जयन्तहभट्ट कृत एक वृत्ति ग्रन्थ है |"
rows[262].human = "nyaay manjari padvakyapramanparavarinjarnnaiyayik jayantahbhatt krut ek vrutti granth hai ."
rows[263].row = 5196
rows[263].native = "१९४८ में, मार्गरेट लेई ने कैथोलिक धर्म में परिवर्तित किया और १९५० में एक कॉन्वेंट में प्रवेश किया।"
rows[263].human = "1948 mein margaret lai ne katholik dharma mein parivartit kiya aur 1950 mein ek convent mein pravesh kiya."
rows[264].row = 5208
rows[264].native = "1970 में दि पार्टी एट किट्टी एंड स्टड के अलावा, स्टैलोन नो प्लेस टू हाइड में भी नजर आए, जिसे पुन:संपादित किया गया और फिर उसे नया नाम रिबेल दिया गया, इस दूसरे संस्करण में स्टैलोन उसके स्टार के रूप में दिखे."
rows[264].human = "1970 mein The party at kitty and stud ke alavaa, Stalleone No place to hide mein bhi najar aaye, jise pun:sampaadit kiya gaya aur fir use nyaa naam rebel diya gaya, is dusare sanskaran mein Stallone uske star ke rup mein dikhe."
rows[265].row = 5220
rows[265].native = "\"दुनिया वाले भी क्या याद\" - ज़ुर्म"
rows[265].human = "\"duniyaa vaale bhi kyaa yaad\" - jurm"
rows[266].row = 5224
rows[266].native = "डेप एक पुरानी हॉलीवुड शैली के पुनर्जीवित होने की संभावना से उत्साहित थे और बाद में यह देखकर खुश हुए कि स्क्रिप्ट उनकी अनोखी संवेदनशीलताओं से मेल खाती थी: ब्लैक पर्ल का चालक दल खजाने की खोज के लिए नहीं जा रहा था बल्कि इसकी बजाय इसे उनके अभिशाप को हटाने के लिए वापस आ रहा था।"
rows[266].human = "Depp ek puraani hollywood shaili ke punarjivit hone ki sambhavna se utsaahit the aur baad mein yah dekhkar khush hue ki skript unki anokhi samvedanshiltaaon se mel khaati thi: Black Pearl kaa chaalak dal khajaane ki khoj ke liye nahin jaa rhaa thaa balki iski bajaay ise unke abhishaap ko hataane ke liye vaapas aa raha tha."
rows[267].row = 5225
rows[267].native = "रंग दे बसंती की तरह इंडिया गेट पर मोमबत्ती जला के लोगों ने प्रियदर्शिनी मट्टू और जेसिका लाल के केसों में अदालत के फैसलों के खिलाफ मोर्चा निकाला और शायद स्वतंत्र भारत के इतिहास में पहली बार इस तरह से शांतिप्रिय जुलूस निकाल के उच्च न्यायालय को और सरकार को ये मुकदमे फिर से खोलने पर मजबूर कर दिया।"
rows[267].human = "Rang De Basanti ki tarah India Gate par mombatti jala ke logo ne Priyadarshini Mattu aur Jessica Lal ke keson mein adaalat ke faisalon ke khilaaf morchaa nikala aur shaayad svatntra bharat ke itihaas mein pahali baar is tarah se shaatipriya julus nikaal ke uchch nyayaalaya ko aur sarkaar ko ye mukadme fir se kholne par majbur kar diyaa."
rows[268].row = 5263
rows[268].native = "अनन्त राव सार देसाई, जो कि मराठी और पुर्तगाली भाषाओ के रेडियों के नाटककार और लघु-कथा लेखक जो मार्दोल में रहे और औषधि-शास्त्र का अभ्यास किया।"
rows[268].human = "Anant Rao Sardesai, jo ki marathi aur purtgali bhasao ke radio ke natkaar aur laghu-katha lekhak jo maardol mein rehe aur ausadhi-shastra ka abhyaas kiya."
rows[269].row = 5285
rows[269].native = "यह जलवाष्प उष्मामापी से कुछ भिन्न होता है।"
rows[269].human = "yah jalvashp ushmaamaapi se kuchh bhinna hota hai."
rows[270].row = 5314
rows[270].native = "इस लोककथा से ही इस प्रपात का नाम तब से उस अजगर के नाम पर पड़ गया और इस झरने की लोकप्रियता और भी बढ़ गयी।"
rows[270].human = "is lokakatha se hi is prapaat ka naam tab se us ajgar ke naam par pad gaya aur is jharne ki lokpriyta aur bhi badh gayi."
rows[271].row = 5328
rows[271].native = "खड़ी बोली वह बोली है जिसपर ब्रजभाषा या अवधी आदि की छाप न हो।"
rows[271].human = "khadi boli vah boli hai jispar brajbhasha ya awadhi aadi ki chhaap na ho."
rows[272].row = 5329
rows[272].native = "इसके बावजूद ज्योतिबा फूले ने हमेशा ही तथाकथित 'नीची' जाति के लोगों के अधिकारों की पैरवी की।"
rows[272].human = "iske bavjud Jyotiba Phule ne hamesha hi tathakathit 'nichi' jaati ke logon ke adhikaron ki pairvi ki."
rows[273].row = 5340
rows[273].native = "1985 में, सेगा के तीसरे-व्यक्ति वाले आर्केड रेल शूटर खेल स्पेस हैरियर में एक वास्तविक एनालॉग उड़ान छड़ी, जिसका प्रयोग गतिशीलता के लिए किया जाता था, प्रस्तुत की गई।"
rows[273].human = "1985 mein, Sega ke tisre-vyakti vale orked rel shootar khel spes heriyar mein ek vaastvik enalog udan chhadi, jiska prayog gatishilta ke liye kiya jataa tha, prastut ki gayi."
rows[274].row = 5385
rows[274].native = "इसके बावजूद, गर्भाशय ग्रीवा agenesis के साथ महिलाओं में कई गर्भधारण की सूचना मिली है, जो शल्य चिकित्सा उपचार किया गया था।"
rows[274].human = "isake bavjud, garbhashay griva agenesis ke sath mahilaon mein kayi garbhdharan ki suchna mili hai, jo shalya chikitsa upchar kiya gaya tha."
rows[275].row = 5397
rows[275].native = "प्रख्यात उपन्यासकार नरेन्द्र कोहली ने अपने उपन्यास ‘वसुदेव’ के द्वारा इस कमी को पूरा करने का प्रयास किया है।"
rows[275].human = "prakhyat upnyaskar Narendra Kohli ne apne upanyas 'Vasudev' ke dwara is kammi ko pura karne ka prayas kiya hai."
rows[276].row = 5414
rows[276].native = "10 जनवरी- भारत और पाकिस्तान ने शांति समझौता किया।"
rows[276].human = "10 January- Bharat aur Pakistan ne shanti samjhauta kiya."
rows[277].row = 5442
rows[277].native = "इस प्रकार, उन्होंने जाति व्यवस्था की नई व्याख्या दी, जैसा कि उनका मानना है कि किसी व्यक्ति की जाति उसके स्वभाव से संबंधित है, न कि उसके जन्म से; माधव के अनुसार जन्म वर्ण द्वारा निर्धारित नहीं होता है; धर्मपरायण प्रबुद्ध चांडाल (जातिच्युत) एक अज्ञानी ब्राह्मण से कहीं अधिक श्रेष्ठ है।"
rows[277].human = "is prakar, unhone jati vyavstha ki nayi vyakhya di, jaisa ki unka manna hai ki kisi vyakti ki jati uske svabhav se sambandhit hai, na ki uske janm se; Madhav ke anusar janm varn dvara nirdharit nahi hota hai; dharmaparayan prabuddh chandaal (jatichyut) ek agyani brahman se kahin adhik shreshth hai."
rows[278].row = 5448
rows[278].native = "आधुनिक दर्शन के प्रमुख झुकाव"
rows[278].human = "adhunik darshan ke pramukh jhukav"
rows[279].row = 5449
rows[279].native = "भगवान ने कर्म के नियम बनाये हैं और भगवान इसका उल्लंघन नहीं करेंगे।"
rows[279].human = "Bhagwan ne karm ke niyam banaye hain aur bhagwan iska ullanghan nahi karenge."
rows[280].row = 5497
rows[280].native = "जे सी शाह भारत के सर्वोच्च न्यायालय के भूतपूर्व न्यायाधीश रहे हैं।"
rows[280].human = "J C Shah Bharat ke sarvochch nyayalay ke bhutpurv nyayadhish rahe hain."
rows[281].row = 5502
rows[281].native = "शब्द पुरातात्विक उत्खनन के दो अर्थ हैं।"
rows[281].human = "shabd puratatvik utkhanan ke do arth hain."
rows[282].row = 5506
rows[282].native = "तब शरीर की और लसीका ग्रंथियाँ (गिल्टियाँ) सूजती हैं।"
rows[282].human = "tab sharir ki aur lasica granthiyan (giltiyan) sujati hain."
rows[283].row = 5539
rows[283].native = "आकांक्षा सरीन - अर्पिता, पुचकी की माँ"
rows[283].human = "Akanksha Sareen - Arpita, Puchki ki maa"
rows[284].row = 5570
rows[284].native = "बीरबल दि क्लैवर"
rows[284].human = "Birbal The Clever"
rows[285].row = 5578
rows[285].native = "खाद्य व्यवसायियों का यह अनैतिक एवं समाजविरोधी आचरण संसार के सभी देशों में पाया जाता है, किंतु अशिक्षित, निर्धन और अल्पविकसित देशों में यह अधिक देखने में आता है।"
rows[285].human = "khadya vyavsayiyon ka yah anaitik evam samajvirodhi achran sansar ke sabhi deshon mein paya jata hai, kintu ashikshit, nirdhan aur alpviksit deshon mein yah adhik dekhne mein aata hai."
rows[286].row = 5631
rows[286].native = "वेइल्स शेयरसन लोएब रोड्स को शेयरसन/अमेरिकन एक्सप्रेस को खरीदा."
rows[286].human = "Welles Shearson Loeb Rhodes ko Shareerson/American Express ko kharida."
rows[287].row = 5656
rows[287].native = "शिरोभूषण जो कि पोशाक का सबसे पवित्र तथ्य है, देवत की मूर्ति के साम्ने पहना जाता है, पार्ंपरिक वाध्यों के साथ कलाकार अपना प्रतिबिंब आइने में देखता है।"
rows[287].human = "shirobhushan jo ki poshaak ka sabse paavitra tathya hai, devat ki murti ke saamne pahnaa jata hai, paramparik vaadhyon ke saath kalakar apna pratibimb aaine men dekhtaa hai."
rows[288].row = 5665
rows[288].native = "पुस्तक की सूक्ष्मता और गहराई के बावजूद, इसे अक्सर बच्चों के कहानियों के रूप में वर्गीकृत किया जाता है।"
rows[288].human = "pustak ki sukshmta aur gahrayi ke baavjud, ise aksar bachchon ke kahaaniyon ke rup mein vargikrit kiya jaata hai."
rows[289].row = 5674
rows[289].native = "इस तकनीक में और अधिक शोध करने पर जीन चिकित्सा, रक्त आधान एवं सामयिक दवाओं के क्षेत्र लाभान्वित होने की संभावना को नकारा नहीं जा सकता."
rows[289].human = "is taknik mein aur adhik shodh karne par gene chikitsaa, rakt aadhaan evam saamayik davaaon ke kshetra labhanvit hone ki sambhavna ko nakara nahin ja sakaa."
rows[290].row = 5723
rows[290].native = "मरीन पार्क में प्रशिक्षित डॉल्फिन अपने करतब दिखाती हैं।"
rows[290].human = "marine park mein prashikshit dolphin apne kartab dikhaati hain."
rows[291].row = 5727
rows[291].native = "बुराई की समस्या"
rows[291].human = "burai ki samsyaa"
rows[292].row = 5729
rows[292].native = "राज्य के बाकी हिस्सों में पश्चिम में गहन कृषि के लिए दिया गया प्रेरी है और दक्षिणपूर्व में पतझड़ी जंगल शामिल है।"
rows[292].human = "rajya ke baki hisson mein pashchim mein gahan krishi ke liye diya gaya preri hai aur dakshinpurv mein patjhadi jangal shaamil hai."
rows[293].row = 5740
rows[293].native = "उमर पचपन की दिल बचपन का 1992 में बनी हिन्दी भाषा की फिल्म है।"
rows[293].human = "umar pachapan ki dil bachapan ka 1992 mein bni hindi bhasaa ki film hai."
rows[294].row = 5757
rows[294].native = "अपर्याप्त निधि वाले खाते से आहरित किये गए चॅक को नकारा गया कहते हैं या रबर चॅक कहा जा सकता है।"
rows[294].human = "aparyaapt nidhi wale khaate se aaharit kiye gaye cheque ko nakara gaya kahte hain ya rabar cheque kaha ja sakta hai."
rows[295].row = 5777
rows[295].native = "कानूनी राशि (शब्दों में राशि) की भी अत्यधिक सिफारिश की जाती है, पर सख्ती से ज़रूरी नहीं है।"
rows[295].human = "kaanuni rashi (shabdon mein rashi) ki bhi atyadhik sifaarish ki jati hai, par sakhti se jaruri nahin hai."
rows[296].row = 5831
rows[296].native = "1980 के दशक के मध्य में, अनुसंधान परिषद ने सिफारिश की कि एनएएल को भारत की नागरिक उड्डयन आवश्यकताओं का अध्ययन करना चाहिए और एक व्यवहार्य नागरिक उड्डयन उद्योग की स्थापना के तरीके सुझाए जाने चाहिए।"
rows[296].human = "1980 ke dashak ke madhya mein, anusandhaan parisad ne sifaarish kee ki NAL ko bharat ki nagarik uddayan aavashyakataaon ka adhyayan karnaa chahiye aur ek vyavhaary nagarik uddayan udyoga ki sthaapanaa ke tarike sujhaye jane chahiye."
rows[297].row = 5883
rows[297].native = "कभी कभी संदर्भों से जमा किये गए नमूने भी लिए जाते हैं ताकि बाद में इनका पर्यावरणीय विश्लेषण अथवा वैज्ञानिक कालांकन किया जा सके।"
rows[297].human = "kabhi kabhi sandarbhon se jamaa kiye gaye namune bhi liye jaate hain taaki baad mein inkaa paryaavaraniy vishleshan athavaa vaigyaanik kaalaankan kiya ja sake."
rows[298].row = 5898
rows[298].native = "अर्देशिर, जनरल रतंजीबा के परिवार के थे जिन्होंने शिवाजी की सेना का नेतृत्व किया था और उन्हें 100 गांवों से सम्मानित किया गया था जिसमें तारापोर मुख्य गांव था, जहां से परिवार का नाम आता है।"
rows[298].human = "Ardeshi, General Ratangiba ke parivaar ke the jinhonne shivaji ki sena ka netritva kiya tha aur unhein 100 gaavon se sammaanit kiya gaya tha jismein Tarapor mukhya gaon tha, jahan se parivaar ka naam ataa hai."
rows[299].row = 5914
rows[299].native = "भारत में सामूहिक विनाश के हथियार"
rows[299].human = "bharat mein samuhik vinaash ke hathiyaar"
rows[300].row = 5942
rows[300].native = "अपनी बेटी को बचाने के लिए अर्पिता वहाँ से अपनी बेटी के साथ भागने का प्रयास भी करती है, लेकिन भागने में विफल हो जाती है।"
rows[300].human = "apni beti ko bachaane ke liye Arpita vahan se apni beti ke saath bhaagane ka prayaas bhi karti hai, lekin bhaagane mein vifal ho jati hai."
rows[301].row = 5946
rows[301].native = "कुछ पर जया बच्चन द्वारा दूरदर्शन धारावाहिक सात फेरे का निर्माण किया गया है तथा कुछ कहानियां गुलज़ार के दूरदर्शन धारावाहिक किरदार में तथा भावना धारावाहिक में शामिल की जा चुकी हैं।"
rows[301].human = "kuchh par jaya bachchan dwara doordarshan dharavahik Saat Phere ka nirmaan kiya gaya hai tatha kuchh kahaaniyaan Gulzar ke doordarshan dharavahik kirdaar mein tatha bhavna dharavahik mein shaamil ki ja chuki hain."
rows[302].row = 5974
rows[302].native = "श्री मुथुस्वमि दीक्षितर का यह मानना था की वडिवेलू गानो के बोल को एक बार सुनते ही दोहरा सकते थे।"
rows[302].human = "Shri Muthuswami Dikshitar ka yah maananaa tha ki Vadivelu gaano ke bol ko ek baar sunate hi doharaa sakte the."
rows[303].row = 5996
rows[303].native = "सौरमान एवं चांद्रमान के ३२ महीनों में १ महीने का अंतर पड़ जाता है।"
rows[303].human = "saurmaan evam chandramaan ke 32 mahinon mein 1 mahine ka antar pada jata hai."
rows[304].row = 6039
rows[304].native = "समाज के विभिन्न आयामों को उनसे अधिक विश्वसनीयता से दिखा पाने वाले परिदर्शक को हिन्दी-उर्दू की दुनिया नहीं जानती."
rows[304].human = "samaaj ke vibhinn aayaamon ko unse adhik vishvsaniyataa se dikhaa pane wale paridarshak ko hindi-urdu ki duniya nahin jaanati."
rows[305].row = 6045
rows[305].native = "इस प्रकार ये केवल इनपुट उपकरण ही नहीं, बल्कि सक्रिय उपकरण भी हैं।"
rows[305].human = "is prakaar ye keval input upakaran hi nahin, balki sakriya upakaran bhi hain."
rows[306].row = 6050
rows[306].native = "इसमें पीले छोटे फल लगते हैं, जो खाने में काफी मीठे और स्वादिष्ठ होते हैं।"
rows[306].human = "ismein peele chhote fal lagate hain, jo khaane mein kaafi mithe aur swaadisht hote hain."
rows[307].row = 6081
rows[307].native = "ये दिल्ली राज्य से हैं।"
rows[307].human = "ye Delhi rajya se hain."
rows[308].row = 6082
rows[308].native = "ओसीआनास और थीटिस ही यूनानी देवपरिवार के आदि पिता और माता है।"
rows[308].human = "Oceania aur thetis hi yunani devpariwar ke aadi pita aur mata hai."
rows[309].row = 6099
rows[309].native = "विद्युत प्रवृत्ति है,"
rows[309].human = "vidyut pravrutti hai,"
rows[310].row = 6125
rows[310].native = "यदि गर्मी अच्छी पड़ती है तो वर्षा भी खूब होती है।"
rows[310].human = "yadi garmi achchi padti hai to varsha bhi khoob hoti hai."
rows[311].row = 6136
rows[311].native = "निम्नलिखित धर्म या नेकी करने से कैसे बुरे कर्म को कम किया जा सकता है इसके उदाहरण हैं: अच्छे काम करना, जैसे कि दूसरों की सहायता करना; भक्ति योग, या दया पाने के लिए भगवान की पूजा करना; और भगवान की दया पाने के लिए चिदंबरम मंदिर या रामेश्वरम जैसे पवित्र स्थलों की तीर्थयात्रा करना।"
rows[311].human = "nimnlikhit dharm ya neki karne se kaise bure karm ko kam kiya ja sakta hai iske udaaharan hain: achche kaam karna, jaise ki dusron ki sahayta karna; bhakti yog, ya daya paane ke liye bhagvan ki pooja karna; aur bhagvaan ki daya paane ke liye Chidabaram Mandir ya Rameshwaram jaise pavitra sthalon ki tirthyatra karna."
rows[312].row = 6148
rows[312].native = "ऐसी समस्या के उपस्थित होने पर, जिसका समाधान कई तरह से हो सकता है, व्यक्ति अपनी बुद्धि का जिस प्रकार प्रयोग करता है वह उसके व्यक्तित्व गठन को प्रतिबिंबित करता है।"
rows[312].human = "aisi samasya ke upsthit hone par, jiska samadhan kai tarah se ho sakta hai, vyakti apni buddhi ka jis prakar prayog karta hai vah uske vyaktitv gathan ko pratibimbit karta hai."
rows[313].row = 6207
rows[313].native = "संवेद फाउण्डेशन की इस अनियतकालीन पत्रिका की शुरूआत बिहार के छोटे से कस्बे जमालपुर (मुंगेर) में सन् 1991 ईस्वी में हुई।"
rows[313].human = "Samved Foundation ki is aniyatkaalin patrika ki shuruaat Bihar ke chhote se kasbe Jamalpur (Munger) mein san 1991 isvi mein hui."
rows[314].row = 6227
rows[314].native = "मुंबई: सोमैया प्रकाशन."
rows[314].human = "Mumbai: Somaiya Prakashan."
rows[315].row = 6235
rows[315].native = "टोडा जनजाति की भाषा में तमिल भाषा के काफी शब्द पाए जाते हैं और शेष बडागा जनजाति की भाषा से मिलते हुए होते हैं।"
rows[315].human = "toda janjaati ki bhasha mein tamil bhasha ke kafi shabd paaye jate hain aur shesh badaga janjaati ki bhasha se milte huye hote hain."
rows[316].row = 6256
rows[316].native = "कुल मिलाकर यह 800 किलोमीटर की ऊंचाई तक पहुंचेगी।"
rows[316].human = "kul milakar yah 800 kilometer ki unchai tak pahunchegi."
rows[317].row = 6277
rows[317].native = "उनके इस प्रकार कहने से त्रिशंकु ने क्रोधित होकर वशिष्ठ जी के पुत्रों को अपशब्द कहे।"
rows[317].human = "unke is prakar kahne se Trishanku ne krodhit hokar Vashishth ji ke putron ko apshabd kahe."
rows[318].row = 6340
rows[318].native = "जफरनगर मुंगेर, मुंगेर, बिहार स्थित एक गाँव है।"
rows[318].human = "Jaffarnagar Munger, Munger, Bihar sthit ek gaanv hai."
rows[319].row = 6352
rows[319].native = "यह संस्तुति राज्यों के लिए बाध्यता मूलक नहीं थी क्योंकि शिक्षा राज्यों का विषय है।"
rows[319].human = "yah sanstuti rajyon ke liye badhyata mulak nahi thi kyonki shiksha rajyon ka vishay hai."
rows[320].row = 6369
rows[320].native = "भारत के विभिन्न प्रांतों में विभिन्न नामों से पायी जाती है।"
rows[320].human = "Bharat ke vibhinn praanton mein vibhinn namon se paai jaati hai."
rows[321].row = 6392
rows[321].native = "इस तरह की टिप्पणियां न्यू जर्सी के रटगर्स विश्वविद्यालय के धर्म के संयुक्त प्राध्यापक एडविन ब्रायंट द्वारा प्रदान की गयी हैं।"
rows[321].human = "is tarah ki tippniyan New Jersey ke Rutgers vishwavidyalay ke dhar ke sanyukt praadhyapak Edwin Briant dvara pradan ki gayi hain."
rows[322].row = 6427
rows[322].native = "व्यसन के इस प्रकार में शान्तिदायक या पीड़ाशामक मादक पदार्थ आते हैं।"
rows[322].human = "vyasan ke is praakar mein shantidayak ya peedashamak maadak padarth aate hain."
rows[323].row = 6454
rows[323].native = "इसमें सहजावस्था विषयासक्ति से आत्मप्रतीति का अभाव, आत्मपूजा, रामनाम के व्यवसायी, संसार की असारता का विचार, आत्मपरिचय की आवश्यकता का उल्लेख, संसार की असारता और विनाशिता, शरीर की हीनता और अनित्यता, राम राजा का आत्मपरिचय और राम कहानी, ननद और भावज का प्रपंच, गाली शब्द और माया के आखेट खेल का निरूपण किया गया है।"
rows[323].human = "ismein sahjavastha vishayasakti se aatmpratiti ka abhav aatmapooja, ramnaam ke vyavsaayi, sansaar ki asarta ka vichar, aatmaparichay ki avshyakta ka ullekh, sansaar ki asarta aur vinashita, sharir ki heenta aur anityata, Ram raja ka aatmaparichay aur Ram kahani, nanad aur bhavaj ka prapanch, gaali shand aur maya ke aakhet khel ka niroopan kiya gaya hai."
rows[324].row = 6466
rows[324].native = "ऋजु रेखाओं द्वारा जनन होनेवाले, अर्थात्‌ रेखज पृष्ठों के प्रतिरूप, सरलतापूर्वक बनाए जा सकते हैं, क्योंकि जनकों को क्रमिक ताने हुए डोरकों से निरूपति किया जा सकता है।"
rows[324].human = "riju rekhaon dvara janan honevale, arthat rekhaj pruthon ke pratiroop, saraltapurvak banaye jaa sakte hain, kyonki janakon ko kramik taane huye dorakon se niroopit kiya ja sakta hai."
rows[325].row = 6495
rows[325].native = "राष्ट्रीय राजमार्ग १०९, जिसे नैनीताल रोड, या बरेली-बागेश्वर हाईवे भी कहा जाता है, रुद्रपुर से शुरू होकर पंतनगर, हल्द्वानी, नैनीताल, भवाली, अल्मोड़ा, रानीखेत, द्वाराहाट, चौखुटिया, गैरसैण तथा आदिबद्री होते हुए कर्णप्रयाग तक जाता है।"
rows[325].human = "rashtriy rajmarg 109, jise Nainital road, ya Bareilly-Bageshwar highway bhi kaha jata hai, Rudrapur se shuru hokar Pantnagar, Haldwani, Nainital, Bhawali, Almora, Ranikhet, Dwarahat, Chaukhootia, Gairsain tatha Adibadri hote hue Karnaprang tak jata hai."
rows[326].row = 6520
rows[326].native = "विशाखापट्‌नम- गुंटूर प्रदेश"
rows[326].human = "Visakhapatnam- Guntur Pradesh"
rows[327].row = 6564
rows[327].native = "अब समुद्री डाकुओं का विद्रोह शुरू हो जाता है और ये डाकू कुछ समय के लिए उसे अपने साथ रखते हैं और फिर उसे पहले शांत भूमि क्षेत्र में छोड़ देते हैं।"
rows[327].human = "ab samudri daakuon ka vidroh shuru ho jata hai aur ye daaku kuchh samay ke liye use apne saath rakhte hain aur fir use pahle shaant bhumi kshetra mein chhod dete hain."
rows[328].row = 6584
rows[328].native = "उन्होंने दो ऐसे चरित्रों को निभाया, जो अमेरिकी सांस्कृतिक शब्दकोश का एक हिस्सा बन गए: रॉकी बैलबोआ, मुक्केबाज जिसने प्रेम और गौरव की राह में आयी बाधाओं के लिए लड़ाई लड़ कर जीत हासिल की और जॉन रैंबो, एक साहसी सैनिक जो हिंसा से राहत और प्रतिशोध मिशन का विशेषज्ञ था।"
rows[328].human = "unhonne do aise charitron ko nibhaya, jo americi saanskritik shabdkosh ka ek hissaa ban gaye: Rocky Balboa, mukkebaaj jisne prem aur gaurav ki raah mein aayi badhaon ke liye ladai lad kar jeet haasil ki aur john rainbow, ek saahasi sainik jo hinsaa se raahat aur pratishodh mission ka vishesagy tha."
rows[329].row = 6614
rows[329].native = "'साहित्यिक भाषा' में भाषा के अलावा अन्य बहुत से तत्व होते हैं।"
rows[329].human = "saahityik bhasa' mein bhasa ke alawa anya bahut se tatv hote hain."
rows[330].row = 6636
rows[330].native = "वल्कनीकरण प्रेस में, या भाप की उपस्थिति में, या शुष्क ताप पर संपन्न हाता है।"
rows[330].human = "valkanikaran press mein, ya bhaap ki upsthiti mein, ya shusk taap par sampann hota hai."
rows[331].row = 6645
rows[331].native = "एलो वरिएगटा - तीतर-छाती एलो, टाइगर एलो"
rows[331].human = "Aloe Vertegata - titar-chhati Aloe, Tiger Aloe"
rows[332].row = 6704
rows[332].native = "बर्लिन समिति 1915 के बाद बाद से भारतीय स्वतंत्रता समिति (जर्मन: दास इंडिस्की अनभांगिग्केट्स्कोमी), 1914 में जर्मनी में भारतीय छात्रों और देश में रहने वाले राजनीतिक कार्यकर्ताओं द्वारा प्रथम विश्व युद्ध के दौरान जर्मनी में गठित एक संगठन था।"
rows[332].human = "Berlin samiti 1915 ke baad baad se bharatiy svatantrtaa samiti (German: Das Indiski Anbhangigatskosumi), 1914 mein Germany mein bhaaratiy chhaatron aur desh mein rahne wale rajnitik karykartaon dwara pratham vishv yuddh ke dauran Germany mein gathit ek sangathan tha."
rows[333].row = 6705
rows[333].native = "डी के बीच रहता करते है।"
rows[333].human = "D ke bich rahtaa karte hai."
rows[334].row = 6718
rows[334].native = "2006 में, रोमानिया में कम्युनिस्ट तानाशाही के अध्ययन के लिए राष्ट्रपति आयोग ने दो मिलियन लोगों पर कम्युनिस्ट दमन के प्रत्यक्ष पीड़ितों की संख्या का अनुमान लगाया."
rows[334].human = "2006 mein, romaniya mein communist tanashahi ke adhyayan ke liye rastrapati aayoga ne do milion logon par communist daman ke pratyaksh piditon ki sankhayaa ka anuman lagaya."
rows[335].row = 6750
rows[335].native = "परंतु फिर भी टोडा लोग तमिल को भली प्रकार बोल-समझ लेते हैं।"
rows[335].human = "prantu fir bhi toda log tamil ko bhali prakaar bol-samajh lete hain."
rows[336].row = 6751
rows[336].native = "युवराज इंटरनेट मूवी डेटाबेस पर"
rows[336].human = "Yuvraj internet movie database par"
rows[337].row = 6805
rows[337].native = "यह द फ्लिनस्टोन के ठीक विपरित है, जहां फ्लिनस्टोन पक्षियों और डायनासोर द्वारा चलित वाहनों के साथ पाषाण युग में जीवन बसर करता है, वहीं जेटसन में सुदूर भविष्य 2062 में रोबोट, एलियंस, होलोग्राम और इसी तरह के अन्य अविष्कारों के बीच जीवनबसर करता है।"
rows[337].human = "yah the Flynnstone ke thik viparit hai, jahan flinstone pakashiyon aur dinosaurs dwara chalit vaahanon ke saath paasaan yuga mein jivan basar karta hai, vahin Jetson mein sudur bhavisya 2062 mein robot, alien, hologram aur isi tarah ke anya aviskaaron ke bich jivanbasar kartaa hai."
rows[338].row = 6811
rows[338].native = "इसके बाद लंबे समय तक नरसंहार और अत्याचार का दौर चला।"
rows[338].human = "iske baad lambe samay tak narsanhaar aur atyaachaar kaa daur chalaa."
rows[339].row = 6818
rows[339].native = "वाक्पति मुंज के बाद उसका छोटा भाई सिन्धु परमार वंश का शासक हुआ।"
rows[339].human = "vaakpati munj ke baad uska chhota bhai sindhu parmaar vansh ka shaasak hua."
rows[340].row = 6830
rows[340].native = "हार्बल औषधि का इस्तेमाल कई पश्चिमी देशों में 1950 के दशक में इस लोकप्रिय हुआ था।"
rows[340].human = "Herbal ausadhi ka istemaal kai pashchimi deshon mein 1950 ke dashak mein is lokpriy hua tha."
rows[341].row = 6860
rows[341].native = "पक्षियों की आम पक्षियों आवाज बहुत तेज पिया-ओ या मिया-ओ होती है।"
rows[341].human = "pakshiyon ki aam pakshiyon aawaj bahut tej piya-o ya miya-o hoti hai."
rows[342].row = 6870
rows[342].native = "प्रख्यात साहित्यकार अज्ञेय ने यद्यपि कहानियां कम ही लिखीं और एक समय के बाद कहानी लिखना बिलकुल बंद कर दिया, परंतु हिन्दी कहानी को आधुनिकता की दिशा में एक नया और स्थायी मोड़ देने का श्रेय भी उन्हीं को प्राप्त है।"
rows[342].human = "prakhyaat saahitykaar agyeya ne yadyapi kahaniyaan kam hi likhin aur ek samay ke baad kahani likhanaa bilkul band kar diya, parantu hindi kahaani ko aadhuniktaa ki disha mein ek naya aur sthaayi mode dene ka shrey bhi unhin ko praapt hai."
rows[343].row = 6950
rows[343].native = "क्रियाओं के माध्यम से जो हम स्वयं करते हैं।"
rows[343].human = "kriyaon ke madhyam se jo ham svayam karte hain."
rows[344].row = 6975
rows[344].native = "प्रथम के कन्नारशाह, उदयशाह और जामशाह पैदा हुए।"
rows[344].human = "pratham ke Kannarshah, Udayshah aur Jamshah paida huye."
rows[345].row = 7028
rows[345].native = "मेडिसिन हेड का एल्बम, एक व्यावसायिक असफलता रही और इसलिए शीर्षक को बैंड की मूल वरीयता में वापस बदल दिया गया।"
rows[345].human = "Medicine Head ka elbam, ek vyaavasayik asafalta rahi aur isliye shirshak ko baind ki mool variyta mein vaapas badal diya gaya."
rows[346].row = 7053
rows[346].native = "उत्तेजक द्रव्य अधिकांशतः मुख से लिए जाते हैं लेकिन कुछ पदार्थ जैसे मेथेड्रीन इंजेक्शान द्वारा भी लिए जाते हैं।"
rows[346].human = "uttejak dravya adhikanshatah mukh se liye jaate hain lekin kuch padarth jaise methedrin injekshan dvara bhi liye jaate hain."
rows[347].row = 7076
rows[347].native = "यह परिनिष्ठित पश्चिमी हिंदी का एक रूप है।"
rows[347].human = "yah parinishthit pashchimi hindi ka ek roop hai."
rows[348].row = 7099
rows[348].native = "सहारनपुर लखनऊ एक्स्प्रेस 5012 भारतीय रेल द्वारा संचालित एक मेल एक्स्प्रेस ट्रेन है।"
rows[348].human = "saharanpur lucknow express 5012 bhartiya rail dwara sanchalit ek mail express train hai."
rows[349].row = 7125
rows[349].native = "चंडोज्ञ उपनिषद 5.10.7 ने अच्छे जन्म, जैसे कि आध्यात्मिक परिवार में जन्म, अर्थात (ब्राह्मण जाति) या बुरा जन्म, जैसे कि कुत्ता या सुअर के रूप में जन्म लेने के बीच के अंतर को बताता है।"
rows[349].human = "chandoz upnishad 5.10.7 ne acche janam, jaise ki aadhyatmik pariwar mein janam, arthat (brahman jaati) ya bura janam, jaise ki kutta ya suar ke roop mein janam lene ke beech ke antar ko btaata hai."
rows[350].row = 7139
rows[350].native = "इस गतिशील व्यक्ति के साथ एक लंबी अवधि के रिश्ते चाहने वाले लोगों में निष्ठा और ईमानदारी सबसे जरूरी है।"
rows[350].human = "is gatishil vyakti ke sath ek lambi avadhi ke rishte chahne wale logon mein nistha aur imanadari sabase jaruri hai."
rows[351].row = 7151
rows[351].native = "इधर वनजीवों के मांसाभाव का कारण जानने के लिये सातवाहन द्वारा पूछताछ किए जाने पर लुब्धकों ने जो उत्तर दिया उसके अनुसार वे गुणाढ्य को मनाने अथवा ‘बड्डकहा’ को बचाने के उद्देश्य से वन की ओर गए।"
rows[351].human = "idhar vanjeevo ke masanbhav ka kaaran janne ke liye satvaahan dwara puchtach kiye jaane par lubhdhako ne jo uttar diya uske anusar ve gunadhay ko manane athva 'baddkaha' ko bachane ke uddeshya se van ki aur gae."
rows[352].row = 7157
rows[352].native = "कई प्रशंसकों को उम्मीद थी कि बैंड की लाइव 8 पर उपस्थिति, एक पुनर्मिलन दौरे में फलित होगी।"
rows[352].human = "kai prashansko ko umeed thi ki band ki live 8 par upasthitti, ek punarmilan daure mein falit hogi."
rows[353].row = 7176
rows[353].native = "तारीख एक शाम से दूसरी शाम तक चलती है।"
rows[353].human = "taarikh ekk sham se dusri sham tak chalti hai."
rows[354].row = 7217
rows[354].native = "ग्रीष्म ऋतु, वर्ष की छह ऋतओं में से एक ऋतु है, जिसमें वातावरण का तापमान प्रायः उच्च रहता है।"
rows[354].human = "garishma ritu, varsh ki chaha rituon mein se ek ritu hai, jismein vatavarana ka tapman prayah uccha rehta hai."
rows[355].row = 7242
rows[355].native = "सर असुतोश मुखर्जी कलकत्ता विश्वविद्यालय के कुलपति थे।."
rows[355].human = "sir ashutos mukharji kalakatta visvavidyalaya ke kulapati the.."
rows[356].row = 7281
rows[356].native = "हम यह नहीं मानते कि कोई भी अल्लाह के उच्चतम ज्ञान के बराबर हो सकता है, या इसे स्वतंत्र रूप से प्राप्त कर सकता है, और न ही हम यह कहते हैं कि अल्लाह ने पैगंबर को ज्ञान दिया है (अल्लाह उसे आशीर्वाद देता है और उसे शांति देता है) कुछ भी नहीं है।"
rows[356].human = "ham yeh nahi mante ki koi bhi allah ke ucchtam gyan ke barabar ho sakta hai, ya ise swatantra rup se prapt kar sakta hai, aur na hi ham yeh kehte hai ki allah ne paigambar ko gyan diya hai (allah use ashirvad deta hai aur use shanti deta hai) kuch bhi nahi hai."
rows[357].row = 7286
rows[357].native = "आप सफल कैंसे हों - जेम्स ऐलन"
rows[357].human = "aap safal kaise ho - james allen"
rows[358].row = 7308
rows[358].native = "भारत सरकार के अनुदान से बृहत् हिंदी शब्दकोश प्रकाशित किया गया।"
rows[358].human = "bharat sarakar ke anudan se brhat hindi sabdakosh prakashit kiya gaya."
rows[359].row = 7324
rows[359].native = "नींद के खो जाने से उसकी थकावट और भी बढ़ जाती है और फिर वह पागलपन की स्थिति में आ जाता है।"
rows[359].human = "nind ke kho jane se uski thakavat aur bhi badh jati hai aur fir veh pagalpan ki sthiti me aa jata hai."
rows[360].row = 7367
rows[360].native = "दस्तावेजों में सजरे नस्बे, कुर्सी नामा (जो साबित करता है कि रतन सिंह महाराजा रणजीत सिंह की दूसरी पत्नी से पैदा हुए थे) महाराजा रणजीत सिंह और उनके बेटे रतन सिंह के चित्र शामिल हैं।"
rows[360].human = "dastavejo me sajre nasbe, kursi nama (jo sabit karta hai ki ratna singh maharaja ranjeet singh ki dusri patni se paida hue the) maharaja ranjeet singh aur unke bete ratan singh ke chitr shamil hai."
rows[361].row = 7376
rows[361].native = "राजनीतिक और सामाजिक हर रूप में इसका विरोध स्वाभाविक था।"
rows[361].human = "rajnitik aur samajik har rup me iska virodh svabhavik tha."
rows[362].row = 7384
rows[362].native = "संयुक्त राष्ट्र अमरीका का संविधान;"
rows[362].human = "sanyukt rashtra america ka sanvidhan;"
rows[363].row = 7390
rows[363].native = "इसका उद्भव मिथुन तारामंडल से माना जाता है।"
rows[363].human = "iska udbhav mithun taramandal se mana jata hai."
rows[364].row = 7403
rows[364].native = "भूटान में सनथन धर्म की आध्यात्मिक परंपराओं और प्रथाओं को बढ़ावा देने के लिए समर्पित है ताकि मानव मूल्यों को बढ़ावा और मजबूत किया जा सके।"
rows[364].human = "bhutan me sanathana dharma ki adhyatmik paramparao aur prathao ko badhava dene ke lie samarpita hai taki manav mulyo ko badhava aur majbut kiya ja sake."
rows[365].row = 7410
rows[365].native = "इस उपन्यास में हॅरी पॉटर का सामना अनिष्ठ देव (वोल्डेमॉर्ट) से होता है।"
rows[365].human = "is upanyas me harry potter ka samna anistha deva (voldemorta) se hota hai."
rows[366].row = 7425
rows[366].native = "वे भारतीय जनता पार्टी से संबद्ध हैं।"
rows[366].human = "ve bharatiya janta party se sambaddh hai."
rows[367].row = 7443
rows[367].native = "पाठ्यक्रम शुरू में इस्लामी धार्मिक अध्ययन, इस्लामी क़ानून, अरबी साहित्य और अंकगणित पर केंद्रित था, और बाद में इतिहास, गणित, भौतिक विज्ञान और संगीत में विस्तारित किया गया था।"
rows[367].human = "pathyakrama shuru me islami dharmika adhyayana, islami kanun, arbi sahitya aur ankganit par kendrit tha, aur baad me itihas, ganit, bhautik vigyan aur sangeet me vistarit kiya gaya tha."
rows[368].row = 7459
rows[368].native = "नौसेना - जो समुद्रों, झीलों व नदियों पर लड़ती है"
rows[368].human = "nausena - jo samudro, jhilom v nadiyo par ladti hai"
rows[369].row = 7466
rows[369].native = "उसने लिखा, गंजुरिया में अभी-अभी काफ़ी जुताई की गई है जिससे यह पता चलता है कि इसे कितने शानदार इला्के बदला जा सकता है मैं सोचता हूँ, इसकी सुंदरता और समृद्ध विश्व के किसी भी क्षेत्र जैसी विकसित की जा सकती है।"
rows[369].human = "usne likha, ganjuriya me abhi-abhi kafi jutai ki gai hai jisse yeh pata chalta hai ki ise kitne shanadar ilake badla ja sakta hai mai sochta hu, iski sundarta aur samrddha vishv ke kisi bhi kshetra jaisi viksit ki ja sakti hai."
rows[370].row = 7470
rows[370].native = "इरोम शर्मिला इस कानून का विरोध करने वालों में मणिपुर की कार्यकर्ता इरोम शर्मिला का नाम प्रमुख है, जो इस कानून के खिलाफ 16 वर्षों से उपवास पर"
rows[370].human = "irom sharmila is kanun ka virodh karne valo me manipur ki karyakarta irom sharmila ka nam pramukha hai, jo is kanuna ke khilaf 16 varsho se upvas par"
rows[371].row = 7513
rows[371].native = "इन उपायों में से अधिकांशतः शौक्षणिक उपायों में नशे के शारीर और मन पर पड़ने वाले प्रभाव के सम्बन्ध में ज्ञान प्रदान कर जागरूकता लाने का प्रयास किया जाता है ताकि नशीले पदार्थ के सेवन के प्रति भय उत्पन्न हो जाए।"
rows[371].human = "in upayo me se adhikansatah saukshanik upayo me nashe ke sharir aur man par padne vale prabhav ke sambandh me gyan pradan kar jagrukta laane ka prayas kiya jata hai taki nashile padartha ke sevan ke prati bhay utpanna ho jae."
rows[372].row = 7519
rows[372].native = "यदि कच्चे लोहे में फॉस्फोरस की मात्रा अधिक होती है तो समाक्षारीय विधि का उपयोग किया जाता है।"
rows[372].human = "yadi kacche lohe me phosphoras ki matra adhik hoti hai to samakshariy vidhi ka upyog kiya jata hai."
rows[373].row = 7563
rows[373].native = "बुकानन जहाँ कहीं भी गया, वहाँ उसने निवासियों के व्यवहार को शत्रुतापूर्ण पाया।"
rows[373].human = "bukanan jahan kahin bhi gaya, vahan usne nivasiyo ke vyavahar ko shatrutapurn paya."
rows[374].row = 7604
rows[374].native = "1905 में, खान ने हिजाज के समकालीन लोगों के अनुरोध पर, पेपर का उपयोग मुद्रा के रूप में उपयोग करने की अनुमति पर एक फैसले लिखा, जिसका शीर्षक किफ्ल-उल-फैक्हेहिल फेहिम फे अहकम-ए-किर्तस दहरिम था।"
rows[374].human = "1905 me, khan ne hijaj ke samkalin logo ke anurodh par, paper ka upyog mudra ke rup me upyog karne ki anumati par ek faisle likha, jiska shirshak kifal-ul-faik'hehil fehim fe ehkam-e-kirtas deharim tha."
rows[375].row = 7617
rows[375].native = "उनके चित्रों में एक-सी घरेलू वस्तुओं का फीका संयोजन बहुतायत में दीखता है।"
rows[375].human = "unake citrom mem eka-si gharelu vastu'om ka phika sanyojana bahutayata mem dikhata hai."
rows[376].row = 7621
rows[376].native = "इस राजवंश का शासन मध्यप्रदेश के अधिक भूभाग तथा प्राचीन बरार (आंध्र प्रदेश) पर विस्तृत था, जिसके सर्वप्रथम शासक विन्ध्यशक्ति का नाम वायुपुराण तथा अजंतालेख मे मिलता है।"
rows[376].human = "isa rajavansa ka sasana madhyapradesa ke adhika bhubhaga tatha pracina barara (andhra pradesa) para vistrta tha, jisake sarvaprathama sasaka vindhyasakti ka nama vayupurana tatha ajantalekha me milata hai."
rows[377].row = 7646
rows[377].native = "उदाहरण में, भगवती तेय्यम की पंथ, जिसे देवी की मातृ रूप में पूजा की जाती है, देवी के मूल रूप से व्युत्पन्न है।"
rows[377].human = "udaharana mem, bhagavati teyyama ki pantha, jise devi ki matr rupa mem puja ki jati hai, devi ke mula rupa se vyutpanna hai."
rows[378].row = 7664
rows[378].native = "वह मोहनीश बहल की मौसी और रानी मुखर्जी की ताई हैं।"
rows[378].human = "vaha mohanisa bahala ki mausi aura rani mukharji ki ta'i haim."
rows[379].row = 7688
rows[379].native = "इसका मुख्यालय दिल्ली में है।"
rows[379].human = "isaka mukhyalaya dilli mem hai."
rows[380].row = 7719
rows[380].native = "652 ग्रेगोरी कैलंडर का एक अधिवर्ष है।"
rows[380].human = "652 gregori kailandara ka eka adhivarsa hai."
rows[381].row = 7742
rows[381].native = "अब विजय क्रोध में फूट गया और अपने सभी दुश्मनों को नष्ट करने के लिए जेल से भाग गया।"
rows[381].human = "aba vijaya krodha mem phuta gaya aura apane sabhi dusmanom ko nasta karane ke li'e jela se bhaga gaya."
rows[382].row = 7753
rows[382].native = "अधिक संभवतः एम्एस कुछ आनुवंशिक, पर्यावरण संबंधी और संक्रमण संबंधी कारकों के एक परिणाम के रूप में उत्पन्न होता है।"
rows[382].human = "adhika sambhavatah emesa kucha anuvansika, paryavarana sambandhi aura sankramana sambandhi karakom ke eka parinama ke rupa mem utpanna hota hai."
rows[383].row = 7758
rows[383].native = "आगे चलकर देश के राजनयिकों ने भी इस तरह की भाषा को मान्यता देने की कोशिश की और कहा कि इसे फारसी और नागरी दोनों लिपियों में लिखा जा सकता है।"
rows[383].human = "age calakara desa ke rajanayikom ne bhi isa taraha ki bhasa ko man'yata dene ki kosisa ki aura kaha ki ise pharasi aura nagari donom lipiyom mem likha ja sakata hai."
rows[384].row = 7781
rows[384].native = "देवकी-वसुदेव की कथा कहते हुए लेखक ने बड़ी कुशलता से कृष्ण की बाललीलाओं का भी चित्रण किया है।"
rows[384].human = "devki-vasudev ki katha kehte hue lekhak ne badi kushalta se krishna ki baallilao ka bhi chitran kiya hai."
rows[385].row = 7837
rows[385].native = "हुमा क़ुरैशी (झिमली)"
rows[385].human = "huma qureshi (jhimli)"
rows[386].row = 7842
rows[386].native = "उनके नाना-नानी होलोकौस्ट उत्तरजीवी थे।"
rows[386].human = "unke nana-nani holocaust uttarjivi the."
rows[387].row = 7858
rows[387].native = "इन व्यक्तियों का उपचार विभिन्न चिकित्सा केन्द्रों, मेडिकल कॉलेजों एवं नशा मुक्ति केन्द्रों पर निःशुल्क भी किया जाता है।"
rows[387].human = "in vyaktiyo ka upchar vibhinn chikitsa kendro, medical collejo evam nasha mukti kendro par nihshulk bhi kiya jata hai."
rows[388].row = 7873
rows[388].native = "बंद की गये रेकाडसो को फिर से खोल दि जा रहि है।"
rows[388].human = "band ki gaye rekadso ko fir se khol di ja rahi hai."
rows[389].row = 7887
rows[389].native = "अभ्यास रूप में, आवेश संरक्षण एक भौतिक नियम है जिसके अनुसार एक निश्चित आयतन में विद्युत आवेश में कुल अंतर, उन आयतन में आगम आवेश और उस आयतन से निर्गत आवेश के अन्तर के एकदम बराबर होता है।"
rows[389].human = "abhyas rup me, aavesh sanrakshan ek bhautik niyam hai jiske anusar ek nischit aaytan me vidyut aavesh me kul antar, un aaytan me aagam aavesh aur us aaytan se nirgat aavesh ke antar ke ekdum barabar hota hai."
rows[390].row = 7892
rows[390].native = "कभी उन्हें शिकायत का कोई मौका नहीं दिया।"
rows[390].human = "kabhi unhe sikhayat ka koi mauka nahi diya."
rows[391].row = 7900
rows[391].native = "विभिन्न मात्रा में ज्ञान संबंधी दुर्बलता और अवसाद के लक्षण या अस्थिर मन भी सामान्य हैं।"
rows[391].human = "vibhinn matra me gyan sambandhi durbalta aur avsad ke lakshan ya asthir man bhi samany hai."
rows[392].row = 7902
rows[392].native = "इसके बाद यह नाटक इतनी चर्चा में आ गया कि इसके प्रदर्शन कराची, दुबई, वाशिंगटन डीसी, सिडनी, लाहौर तथा अन्य शहरों में हुए।"
rows[392].human = "iske baad yeh natak itni charcha me aa gaya ki iske pradarshan karachi, dubai, washington DC, sydney, lahore tatha anya sheharo me hue."
rows[393].row = 7927
rows[393].native = "मुंशी इन्द्रजीत ने रामप्रसाद को स्वामीजी की सेवा में नियुक्त कर दिया।"
rows[393].human = "munshi indrajeet ne ramprasad ko swamiji ki seva me niyukt kar diya."
rows[394].row = 7935
rows[394].native = "ये वे गाँव थे जिनके नामों के अंत में पत आता है।"
rows[394].human = "ye ve ganv the jinke naamo ke ant me pat aata hai."
rows[395].row = 7939
rows[395].native = "तिमोर सागर, एक अपेक्षाकृत उथला समुद्र है जो उत्तर में तिमोर द्वीप, पूर्व में अराफुरा सागर, दक्षिण में ऑस्ट्रेलिया और पश्चिम में हिंद महासागर से घिरा है।"
rows[395].human = "timor sagar, ek apekshakrit uthla samundra hai jo uttar me timor dvip, purv me arafura sagar, dakshin me austrelia aur paschim me hind mahasagar se ghira hai."
rows[396].row = 7948
rows[396].native = "खड़ी बोली से तात्पर्य खड़ी बोली हिंदी से है जिसे भारतीय संविधान ने राजभाषा के रूप में स्वीकृत किया है।"
rows[396].human = "khadi boli se tatpary khadi boli hindi se hai jise bharatiy sanvidhan ne rajbhasha ke rup me svikrit kiya hai."
rows[397].row = 7963
rows[397].native = "लोहा धरती के गर्भ में स्वतंत्र अवस्था में नहीं पाया जाता है, बल्कि यह ऑक्सीजन और सल्फर के साथ यौगिक अवस्था में पाया जाता है।"
rows[397].human = "loha dharti ke garbh me svatantr avastha me nahi paya jata hai, balki yeh oxygen aura sulphur ke sath yaugik avastha me paya jata hai."
rows[398].row = 7972
rows[398].native = "जाने कितने मेमोरेंडम दिये गये कितने आंदोलन किये गये, मगर धोखा, छल व ठगी के अलावे अब तक कुछ नहीं मिला।"
rows[398].human = "jaane kitne memorendam diye gaye kitne aandolan kiye gaye, magar dhokha, chal va thagi ke alava ab tak kuch nahi mila."
rows[399].row = 7981
rows[399].native = "फिर वो दोनों आवारा घूमते हैं।"
rows[399].human = "phir vo dono aawara ghumte hai."
rows[400].row = 7990
rows[400].native = "945 तक ख़लीफा का रहने की जगह बनाई गई थी।"
rows[400].human = "945 tak khalifa ka rehne ki jagah banai gai thi."
rows[401].row = 8001
rows[401].native = "जनमत जागरण की भी आवश्यकता है।"
rows[401].human = "janmat jagran ki bhi aavashyakta hai."
rows[402].row = 8017
rows[402].native = "इसके आस-पास का सौंदर्य पर्यटकों को बरबस ही अपनी ओर आकर्षित कर लेता है।"
rows[402].human = "iske aas-paas ka saundary paryatako ko barbas hi apni aur aakarshit kar leta hai."
rows[403].row = 8027
rows[403].native = "समाजसेवा में संबंध ही संपूर्ण सहायता का आधार है और यह व्यावसायिक संबंध सदैव साभिप्रय होता है।"
rows[403].human = "samajseva me sambandh hi sampurn sahayta ka aadhar hai aur yeh vyavasayik sambandh sadaiv sabhipray hota hai."
rows[404].row = 8042
rows[404].native = "उन्‍होंने कुश्‍ती में भारत को अंतरराष्‍ट्रीय स्‍तर पर पहचान दिलाने में अहम भूमिका निभाई थी।"
rows[404].human = "unhone kushti me bharat ko antarrashtriy star par pehchan dilane me ahem bhumika nibhai thi."
rows[405].row = 8056
rows[405].native = "उन दिनों ये माउजर आज की ए॰ के॰ - ४७ रायफल की तरह चर्चित थे।"
rows[405].human = "un dino ye mauser aaj ki A K - 47 rifle ki tarah charchit the."
rows[406].row = 8058
rows[406].native = "इस प्रकार, कर्म के लिए आस्तिकता-संबंधी एक प्रशासक या पर्यवेक्षक होना ही चाहिए, अर्थात, भगवान होना ही चाहिए।"
rows[406].human = "is prakar, karma ke lie aastikta-sambandhi ek prashasak ya paryavekshak hona hi chahiye, arthat, bhagvan hona hi chahiye."
rows[407].row = 8067
rows[407].native = "प्रोफेट का मतलब पैगाम देने वाला और प्रोफेसी करने वाला।"
rows[407].human = "prophet ka matlab paigam dene vala aur prophesi karne vala."
rows[408].row = 8074
rows[408].native = "नए संस्करण में 120 चित्र शामिल हैं।"
rows[408].human = "nae sanskaran me 120 chitr shamil hai."
rows[409].row = 8112
rows[409].native = "रामेसेस द्वितीय के प्रताप के कारण लोग पिछले सभी महान फैरो जैसे सेती प्रथम और ठुतोमोस तृतीय की वीरता को भूल गए।"
rows[409].human = "rameses dvitiya ke pratap ke karan log pichle sabhi mahan fairo jaise seti pratham aur thutomos trtiya ki virta ko bhul gae."
rows[410].row = 8146
rows[410].native = "पूर्व प्रधानमंत्री श्री अटलबिहारी वाजपेयी जी भी युवावस्था में वीणा के लेखक रहे हैं।"
rows[410].human = "purv pradhanmantri shri atalbihari vajpayi ji bhi yuvavastha me vina ke lekhak rahe hai."
rows[411].row = 8169
rows[411].native = "जनता के दर्शनार्थ उनका पार्थिव शरीर उनके सरकारी आवास ५ जनपथ नई दिल्ली में रक्खा गया।"
rows[411].human = "janta ke darshanarth unka parthiv sharir unke sarkari aavas 5 janpath nayi delhi me rakkha gaya."
rows[412].row = 8180
rows[412].native = "इसका गूदा संतरी रंग का होता है जो साधारण केलों के सफ़ेद एवं पीले गूदे से पूर्णतया भिन्न है।"
rows[412].human = "iska guda santari rang ka hota hai jo sadharan kelo ke safed evam pile gude se purnataya bhinn hai."
rows[413].row = 8236
rows[413].native = "ATVS प्रणाली के विभिन्न घटकों के संचालन के लिए ड्राइवर पीआरएल में विकसित किए गए हैं।"
rows[413].human = "ATVS pranali ke vibhinna ghatako ke sanchalan ke lie driver PRL mem viksit kiye gaye hai."
rows[414].row = 8271
rows[414].native = "रक्त-मस्तिष्क अवरोध में रिसाव पैदा होते हैं, जो बदले में अन्य क्षति पहुंचाने वाले प्रभाव उत्पन्न करते हैं जैसे कि सूजन, वृहत भक्षक कोशिका (मैक्रोफेज) का सक्रियण और साइटोकाइन तथा अन्य हानिकर प्रोटीनों का अधिक सक्रियण."
rows[414].human = "rakt-mastishka avarodh me risav paida hote hai, jo badle me anya kshati pahuchane vale prabhav utpann karte hai jaise ki sujan, vrihat bhaksak koshika (macrophase) ka sakriyan aur cycotine tatha anya haanikar proteino ka adhik sakriyan."
rows[415].row = 8275
rows[415].native = "ध्वनिविज्ञान में, ध्वनि के परावर्तन के कारण प्रतिध्वनि सुनाई पड़ती है जो सोनार में उपयोग में लायी जाती है।"
rows[415].human = "dhvanivigyan me, dhvani ke paravartan ke karan pratidhvani sunai padti hai jo sonar me upayog me laayi jati hai."
rows[416].row = 8300
rows[416].native = "रॉय ब्रान्सगीस्ट (राइनो)"
rows[416].human = "roy bransgist (rhino)"
rows[417].row = 8325
rows[417].native = "इन नामों में थोड़ी हेर-फेर हो सकता है, किन्तु इस प्रक्रिया की अवस्थाओं में प्रायः कोई अन्तर नहीं होता।"
rows[417].human = "in naamo me thodi her-pher ho sakta hai, kintu is prakriya ki avasthao me prayh koi antar nahi hota."
rows[418].row = 8345
rows[418].native = "उसके बाद शंकर और गौरी वहाँ से भाग जाते हैं।"
rows[418].human = "uske baad shankar aur gauri vaha se bhag jate hai."
rows[419].row = 8349
rows[419].native = "यह विधि इस कल्पना पर निर्धारित है कि जब कोई वस्तु किसी समावृत्त (environment) में शीतल होती है तो समय की उस अवधि में उसके द्वारा उत्सर्जित उष्मा dQ वस्तु के समावृत्त पर, ताप के आधिक्य पर, उसके तल की प्रकृति पर, तथा तल के क्षेत्रफल पर निर्भर करती है।"
rows[419].human = "yeh vidhi is kalpana par nirdharit hai ki jab koi vastu kisi samavritt (environment) me shital hoti hai to samay ki us avadhi me uske dvara utsarjit ushma dQ vastu ke samavritt par, taap ke adhikya par, uske tal ki prakriti par, tatha tal ke kshetrafal par nirbhar karti hai."
rows[420].row = 8360
rows[420].native = "बहुरूपी रूपों के बीच परिवर्तन कुछ विशेष कारकों अर्थात दाब, प्रकाश व ताप के प्रभाव से शुरू होता है।"
rows[420].human = "bahurupi rupo ke bich parivartan kuch vishesh karko arthat daab, prakash va taap ke prabhav se shuru hota hai."
rows[421].row = 8390
rows[421].native = "व्यवहार्यता अध्ययन (नवंबर 1989) ने दिखाया कि देश में 9-14 सीट मल्टी-रोल एलटीए के लिए एक महत्वपूर्ण मांग थी और अगले 10 वर्षों में लगभग 250-350 विमानों की बाजार संभावना का अनुमान लगाया गया था।"
rows[421].human = "vyavaharyta adhyayan (november 1989) ne dikhaya ki desh me 9-14 seat multi-role LTA ke lie ek mahatvpurn mang thi aur agle 10 varsho me lagbhag 250-350 vimano ki bajar sambhavna ka anuman lagaya gaya tha."
rows[422].row = 8404
rows[422].native = "ऐसा रूप जिसमें प्राप्त सभी विकल्पों में एक को मानक मान लिया गया हो तथा जिस भाषा रूप को उस भाषा के सारे बोलने वाले मानक स्वीकार करते हों।"
rows[422].human = "aisa rup jisme prapt sabhi vikalpo me ek ko manak man liya gaya ho tatha jis bhasha rup ko us bhasha ke sare bolne vale manak svikar karte ho."
rows[423].row = 8441
rows[423].native = "विशिष्ट संयोजन के साथ इसका अक्सर एक विशेष अर्थ होता है जैसे कि कर्म योग या कर्म-कांड का अर्थ क्रमश: \"योग या कार्य\" या \"भौतिकवादी गतिविधि की कार्यप्रणाली\" है।"
rows[423].human = "vishist sanyojan ke sath iska aksar ek vishesh arth hota hai jaise ki karma yoga ya karma-kand ka arth kramasa: \"yoga ya karya\" ya \"bhautikvadi gatividhi ki karyapranali\" hai."
rows[424].row = 8457
rows[424].native = "प्रथम इकाई पैकी तथा दूसरी इकाई पेक्कन, कट्टन, केन्ना तथा टोडी उप-इकाईयों में बंटी हुई है।"
rows[424].human = "pratham ikai paiki tatha dusri ikai pekkan, kattan, kenna tatha todi up-ikaiyo me banti hui hai."
rows[425].row = 8468
rows[425].native = "इनमें से सबसे प्रसिद्ध हैं मरीन पार्क और सफारी।"
rows[425].human = "inme se sabse prasiddh hai marine park aur safari."
rows[426].row = 8480
rows[426].native = "अर्पिता की मौत हो जाती है।"
rows[426].human = "arpita ki maut ho jati hai."
rows[427].row = 8497
rows[427].native = "दस न्यूरोटिक आवश्यकताओं की जांच करने पर हरनी ने उन्हें तीन व्यापक श्रेणीओं में रखा हैं-"
rows[427].human = "dus neurotic aavashyaktao ki janch karne par harni ne unhe teen vyapak shrenio me rakha hai-"
rows[428].row = 8506
rows[428].native = "मोट्टे ने गुमनाम रहते हुए गुलिवर्स ट्रेवल्स का प्रकाशन किया, इसके बाद अगले कुछ सालों में कई अनुवर्तियों (मेमोइर्स ऑफ़ द कोर्ट ऑफ़ लिलिपुट), पेरोडियों, (टू लिलीपुटीयन ओडीज़, द फर्स्ट ओन द फेमस इंजन विथ विच केप्टिन गुलिवर एक्सटिंगविश्ड द पेलेस फायर) और \"कीस\" (गुलिवर देसिफर'द और लेम्यूल गुलिवर्स ट्रेवल्स इनटू सेवरल रिमोट रीजन्स ऑफ़ द वर्ल्ड कम्पेंदीयसली मेथादिज़'द, दूसरी को एडमड कर्ल के द्वारा इसी तरह से 1705 में स्विफ्ट की टेल ऑफ़ अ टब के लिए एक \"की\" के रूप में लिखा गया) का उत्पादन किया गया।"
rows[428].human = "motte ne gumnam rehte hue gulivers travels ka prakashan kiya, iske baad agle kuch salo me kai anuvartiyo (memoirs of the court of liliput), perodiyo, (to liliputian odiz, the first on the famous engine with which captin gulivar extinguished the palace fire) aur \"kiss\" (gulivar desifar'the aur lemyul gulivars travels into several remote regions of the world compendiyasali methadiz'da, dusri ko edmad curl ke dvara isi tarah se 1705 me swift ki tail of a tub ke lie ek \"key\" ke rup me likha gaya) ka utpadan kiya gaya."
rows[429].row = 8510
rows[429].native = "बृज बिहारी प्रसाद बिहार राज्य के पूर्व विधायक और मंत्री रहे थे।"
rows[429].human = "brij bihari prasad bihar rajya ke purv vidhayak aur mantri rahe the."
rows[430].row = 8518
rows[430].native = "अत: गुणाढ्य का काल निस्संदेह तृतीय चतुर्थ शताब्दी में कभी माना जा सकता है।"
rows[430].human = "ata: gunadhya ka kaal nissandeh tritiya chaturth shatabdi me kabhi mana ja sakta hai."
rows[431].row = 8523
rows[431].native = "यह मुख्यतः अलमुनियम के सिलिकेट एवं अन्य बहुसिलिकेट (पॉलीसिलिकेट) का मिश्रण है।"
rows[431].human = "yah mukhyatah almunium ke silicate evam anya bahusilicate (polisilicate) ka mishran hai."
rows[432].row = 8536
rows[432].native = "प्रशिक्षण, प्रलेखन, प्रकाशन एवं अन्तराष्ट्रीय सम्पर्क इत्यादि।"
rows[432].human = "prashikshan, pralekhan, prakashan evam antarashtriya sampark ityadi."
rows[433].row = 8560
rows[433].native = "षष्ठी के दिन गोधूली बेला में केले के पोड़ों का चयन विशिष्ट प्रक्रिया और विधि-विधान के साथ किया जाता है।"
rows[433].human = "sasthi ke din godhuli bela me kele ke podo ka chayan vishist prakriya aur vidhi-vidhan ke sath kiya jata hai."
rows[434].row = 8564
rows[434].native = "सपोटरा डांग जो की बंदूक धारी बागियों और बीहड क्षेत्र होने के कारण दुर्दान्त रहा और पानी के अभाव में खेती बाडी न होने, अवेध खनन् से पर्यावरण बर्बाद होने जैसे कारणों से ग्राम वासियों को रहने में दुर्गम कठिनाईयों का सामना करना पड़ता रहा होगा।"
rows[434].human = "sapotra dang jo ki banduk dhari bagiyo aur bihad kshetra hone ke karan durdant raha aur pani ke abhav me kheti baadi na hone, avedh khanan se paryavaran barbad hone jaise karano se gram vasiyo ko rehne me durgam kathinaiyo ka samna karna padta raha hoga."
rows[435].row = 8598
rows[435].native = "बोल्शेविकों की करतूत: स्वतन्त्र भारत में प्रथम बार सन् २००६ में प्रकाशित रामप्रसाद 'बिस्मिल' का क्रान्तिकारी उपन्यास।"
rows[435].human = "bolsheviko ki karatut: svatantr bharat me pratham baar san 2006 me prakashit ramprasad 'bismil' ka krantikari upanyas."
rows[436].row = 8603
rows[436].native = "भागवत पुराण की 10वीं पुस्तक के अध्याय 1 में वसुदेव कंस को अपनी पत्नी और कृष्ण की मां देवकी की ह्त्या न करने का उपदेश देते हैं, यह कहते हुए कि जिन्होंने जन्म लिया है उनके लिए मृत्यु निश्चित है और जब शरीर पंच तत्वों में विलीन हो जाता है, तब आत्मा शरीर छोड़कर असहाय होकर कर्म के नियम के अनुरूप अन्य रूप धारण करती है, उन्होंने बृहदारण्यक उपनिषद, IV:4:3 के उद्धरण का उल्लेख किया।"
rows[436].human = "bhagavata puran ki 10vi pustak ke adhyay 1 me vasudev kans ko apni patni aur krishna ki ma devki ki hatya na karne ka updesh dete hai, yah kehte hue ki jinhone janma liya hai unke lie mrityu nischit hai aur jab sharir panch tatvo me vilin ho jata hai, tab aatma sharir chodkar asahay hokar karma ke niyam ke anurup anya rup dharan karti hai, unhone brhadaranyak upnishad, IV:4:3 ke uddharan ka ullekh kiya."
rows[437].row = 8644
rows[437].native = "दूसरे विश्व युद्ध में इंग्लैण्ड को बुरी तरह उलझता देख जैसे ही नेताजी ने आजाद हिन्द फौज को \"दिल्ली चलो\" का नारा दिया, गान्धी जी ने मौके की नजाकत को भाँपते हुए 8 अगस्त 1942 की रात में ही बम्बई से अँग्रेजों को \"भारत छोड़ो\" व भारतीयों को \"करो या मरो\" का आदेश जारी किया और सरकारी सुरक्षा में यरवदा पुणे स्थित आगा खान पैलेस में चले गये।"
rows[437].human = "dusre vishv yuddh me englanda ko buri tarah ulajhta dekh jaise hi netaji ne azaad hind fauj ko \"dilli chalo\" ka nara diya, gandhi ji ne mauke ki najakat ko bhampte hue 8 august 1942 ki raat me hi bambai se angrejo ko \"bharat chodo\" va bharatiyo ko \"karo ya maro\" ka aadesh jari kiya aur sarkari suraksha me yarvada pune sthit aaga khan palace me chale gaye."
rows[438].row = 8723
rows[438].native = "हालांकि इसराइल सीडब्ल्यूसी पर हस्ताक्षर किए हैं,परंतु संधि की पुष्टि नहीं की है और इसलिए आधिकारिक तौर पर अपने सिद्धांतों से बाध्य नहीं है।"
rows[438].human = "halanki isrile CWC par hastakshar kie hai,parantu sandhi ki pushti nahi ki hai aur isliye adhikarik taur par apne siddhanto se badhya nahi hai."
rows[439].row = 8732
rows[439].native = "एल्बम दिसम्बर, 1976 में पूरा हो गया और उसके आवरण पर काम शुरू हुआ।"
rows[439].human = "album december, 1976 me pura ho gaya aur uske avran par kam shuru hua."
rows[440].row = 8759
rows[440].native = "इससे साबित होता है, कि छोटानागपुर के कुड़मी शेष भारत के कुर्मियों से पूर्णतया भिन्न हैं।"
rows[440].human = "isse sabit hota hai, ki chotanagpur ke kudmi shesh bharata ke kudmiyo se purnataya bhinna hai."
rows[441].row = 8767
rows[441].native = "अन्य किसी तंत्र के माध्यम से सहायता प्रदान करना"
rows[441].human = "anya kisi tantra ke madhyam se sahayata pradan karna"
rows[442].row = 8786
rows[442].native = "केसरी को ऋषि-मुनियों ने अत्यंत बलशाली और सेवाभावी संतान होने का आशीर्वाद दिया।"
rows[442].human = "kesari ko rishi-muniyo ne atyant balshali aur sevabhavi santan hone ka ashirvad diya."
rows[443].row = 8800
rows[443].native = "२००६ में, राष्ट्रीय नाट्य विद्यालय ने थियेटर आलोचक, दिवान सिंह बजेली द्वारा लिखी गई उनकी आत्मकथा प्रकाशित की, जिसका शीर्षक था, \"मोहन उप्रेती - द मैन एंड हिस आर्ट\"।"
rows[443].human = "2006 me, rashtriya natya vidyalaya ne theater alochak, divan singh bajeli dvara likhi gai unki aatmkatha prakashit ki, jiska sirshak tha, \"mohan upreti - the man and his art\"."
rows[444].row = 8816
rows[444].native = "इस राज्य के लोग इतने आत्मनिर्भर है#े कि सारा काम खुद ही करते हैं, इसलिए उसे कोई रोज़गार भी नहीं देता।"
rows[444].human = "is rajya ke log itne aatmnirbhar hai#e ki sara kaam khud hi karte hai, isliye use koi rozgar bhi nahi deta."
rows[445].row = 8817
rows[445].native = "वो शंकर से अपने सारे गलत कामों के लिए माफी मांगता है, पर राजा उसे माफ नहीं करता और आग में डाल देता है।"
rows[445].human = "vo shankar se apne sare galat kamo ke lie mafi mangta hai, par raja use maaf nahi karta aur aag me daal deta hai."
rows[446].row = 8831
rows[446].native = "वैसे आप ग्रीष्म ऋतु को छोड़कर किसी भी समय यहां आ-जा सकते हैं।"
rows[446].human = "vaise aap grishma ritu ko chodkar kisi bhi samay yaha aa-jaa sakte hai."
rows[447].row = 8871
rows[447].native = "लक्ष्मी प्रसाद सिहरे को १९८६ में भारत सरकार ने प्रशासकीय सेवा के क्षेत्र में पद्म भूषण से सम्मानित किया था।"
rows[447].human = "lakshmi prasad sihre ko 1986 me bharat sarkar ne prashasakiy seva ke kshetra me padma bhushan se sammanit kiya tha."
rows[448].row = 8874
rows[448].native = "शास्त्रीजी ने एक वाक्य में तत्काल उत्तर दिया: \"आप देश की रक्षा कीजिये और मुझे बताइये कि हमें क्या करना है?\""
rows[448].human = "shastriji ne ek vakya me tatkal uttar diya: \"aap desh ki raksha kijiye aur mujhe bataiye ki hame kya karna hai?\""
rows[449].row = 8947
rows[449].native = "क्षेत्रीय और अंतर्राष्ट्रीय संबंधों में उनके उपलब्धियों के लिए मध्य पूर्व बिजनेसवमेन एंड लीडर अचीवमेंट अवार्ड (२००७)"
rows[449].human = "kshetriya aur antarrashtriya sambandho me unke upalabdhiyo ke lie madhya purva businessmen and leader achievement award (2007)"
rows[450].row = 8984
rows[450].native = "ये स्वभी कर्मचारी एवं अधिकारी विभिन्न पदों पर आसीन रहते हैं।"
rows[450].human = "ye svabhi karmachari evam adhikari vibhinna pado par aasin rehte hai."
rows[451].row = 8995
rows[451].native = "यह उस द्वीपसमूह के सेरम द्वीप पर भारी वनों से ढका हुआ खड़ा है।"
rows[451].human = "yah us dvipsamuh ke seram dvip par bhari vano se dhaka hua khada hai."
rows[452].row = 9001
rows[452].native = "बुढापे में जलोदर और लकवा वाले रोग भी पीछे पड जाते है।"
rows[452].human = "budhape me jalodar aur lakva vale rog bhi piche pad jate hai."
rows[453].row = 9025
rows[453].native = "'वंशभास्कर' को पूर्ण करने का कार्य कवि सूर्यमल के दत्तक पुत्र मुरारीदान ने किया था।"
rows[453].human = "vanshabhaskar' ko purn karne ka karya kavi suryamal ke dattak putra muraridan ne kiya tha."
rows[454].row = 9036
rows[454].native = "या जब कम स्टॉक हो, दीर्घ वायदे करते हैं।"
rows[454].human = "ya jab kam stock ho, dirgh vayade karte hai."
rows[455].row = 9056
rows[455].native = "(3) सर्व खलु इदं ब्रह्म - यह समस्त संसार ब्रह्म ही है (पैथीज्म), इस सिद्धांत के अनुसार संसार और भगवान कोई अलग-अलग वस्तु नहीं हैं।"
rows[455].human = "(3) sarva khalu idam brahma - yah samast sansar brahma hi hai (pathijm), is siddhant ke anusar sansar aur bhagavan koi alag-alag vastu nahi hai."
rows[456].row = 9178
rows[456].native = "मामले के अभी भी लंबित होने की हालत में, वाटर्स ने ओ'रुरके को निकाल दिया और पीटर रुज को अपने मामलों के प्रबंधन के लिए नियुक्त किया।"
rows[456].human = "mamal ke abhi bhi lambit hone ki halat me, waters ne o'rurke ko nikal diya aur peter ruj ko apne mamlo ke prabandhan ke lie niyukt kiya."
rows[457].row = 9211
rows[457].native = "इनका प्राइमरी क्लासिफिकेशन परीक्षण, शैक्षिक और बुद्धिपरीक्षणों का संमिश्रण था और यह हिंदी, उर्दू तथा अंग्रेजी में तैयार किया गया था।"
rows[457].human = "inka primary classification parikshan, shaikshik aur buddhiparikshano ka sammishran tha aur yah hindi, urdu tatha angreji me taiyar kiya gaya tha."
rows[458].row = 9217
rows[458].native = "चन्देल काल में बुंदेलखंड में मूर्तिकला, वास्तुकला तथा अन्य कलाओं का विशेष विकास हुआ।"
rows[458].human = "chandel kaal me bundelkhand me murtikala, vastukala tatha anya kalao ka vishesh vikas hua."
rows[459].row = 9225
rows[459].native = "यह गार्डन बड़ी संख्या में पर्यटकों को अपनी ओर आकर्षित करता है।"
rows[459].human = "yaha gardana bari sankhya mem paryatakom ko apani ora akarsita karata hai."
rows[460].row = 9227
rows[460].native = "वह अपनी पीढ़ी के सबसे महत्वपूर्ण ऑस्ट्रेलियाई बल्लेबाज थे।"
rows[460].human = "vah apni pidhi ke sabse mahatvpurn austreliai ballebaj the."
rows[461].row = 9228
rows[461].native = "धारा.3 ये स्पष्ट नही करती है कि किस आधार पर किसी क्षेत्र को अशाँत घोषित किया जाएगा ।"
rows[461].human = "dhara.3 ye spasht nahi karti hai ki kis adhar par kisi kshetra ko ashant ghoshit kiya jaega ."
rows[462].row = 9237
rows[462].native = "वर्ष 2010 में हार्दिक सहजानन्द महाविद्यालय, अहमदाबाद में बीकॉम की पढ़ाई की।"
rows[462].human = "varsh 2010 me hardik sahajanand mahavidyalaya, ahmadabad me b.com ki padhai ki."
rows[463].row = 9248
rows[463].native = "जगत् में सामंजस्य एवं समन्वय इसके चेतन कर्ता से आता है।"
rows[463].human = "jagat me samanjasya evam samanvaya iske chetan karta se aata hai."
rows[464].row = 9252
rows[464].native = "एक समय ऐसा भी था जब उनके नाटकों ने पेशावर, लाहौर और अमृतसर से लेकर दिल्ली, जोधपुर, बंबई, मद्रास और ढाका तक पूरे हिन्दुस्तान में धूम मचा रक्खी थी।"
rows[464].human = "ek samay aisa bhi tha jab unke natako ne peshavar, lahore aur amritsar se lekar dilli, jodhpur, bambai, madras aur dhaka tak pure hindustan me dhoom macha rakkhi thi."
rows[465].row = 9277
rows[465].native = "अमेरिकन एक्सप्रेस कार्ड के लिए एक विशिष्ट विज्ञापन शुरु की गई जिसमें मशहूर हस्तियां दर्शकों से पूछते हैं कि: \"क्या आप मुझे जानते हैं?\""
rows[465].human = "american express card ke lie ek vishisht vigyapan shuru ki gai jisme mashur hastiya darshako se puchte hai ki: \"kya aap mujhe jante hai?\""
rows[466].row = 9285
rows[466].native = "शाम, झूलती जड़ें, परतों के बीच और यात्राएं ..."
rows[466].human = "sham, jhulti jade, parto ke bich aur yatrae ..."
rows[467].row = 9322
rows[467].native = "हेमंत चौधरी — गौरी शंकर सुराना, समर के पिता"
rows[467].human = "hemant chaudhari - gauri shankar surana, samar ke pita"
rows[468].row = 9340
rows[468].native = "जॉर्डन के शहरों की सूची"
rows[468].human = "jordan ke sheharo ki suchi"
rows[469].row = 9346
rows[469].native = "इसी बीच नारायण लाल को स्थानीय निवासियों की सहायता से एक पाठशाला में सात रुपये मासिक पर नौकरी मिल गयी।"
rows[469].human = "is bich narayan lal ko sthaniya nivasiyo ki sahayata se ek pathshala me saat rupaye masik par naukari mil gayi."
rows[470].row = 9372
rows[470].native = "बहुत से लोगों को इस के कई लाभकारी परिणामों का लाभ मिला है, कई लोग इस स्वास्थ्य संबंधी डेटा को लाभकारी मानते हैं, लेकिन इस तरह के काम अक्सर विवादास्पद होते हैं क्योंकि कई मापदंड इस तरह के रूप गुणवत्ता समायोजित जीवन वर्ष और विकलांगता से समायोजित जीवन वर्ष से प्रेरित होते हैं, जो व्यक्तिपरक अवधारणाओं जैसे अस्तित्व, जीवन की गुणवत्ता और उत्पादकता के मापदंडों के लाभ के अनुसार होते हैं।"
rows[470].human = "bahut se logo ko is ke kai labhkari parinamo ka labh mila hai, kai log is svasthya sambandhi data ko labhkari mante hai, lekin is tarah ke kaam aksar vivadaspad hote hai kyonki kai mapdand is tarah ke rup gunavatta samayojit jivan varsh aur viklangta se samayojit jivan varsh se prerit hote hai, jo vyaktiparak avdharanao jaise astitva, jivan ki gunvatta aur utpadakata ke mapdando ke labh ke anusar hote hai."
rows[471].row = 9378
rows[471].native = "वे अपने साम्राज्य को औपचारिक रूप से 'श्वेत और उच्च महान शिया राज्य' (, फियोव ब्यिय ल्हयिय ल्हयिय) बुलाते थे।"
rows[471].human = "ve apne samrajya ko aupcharik rup se 'shwet aur ucch mahan shiya rajya' (, phiyov byiya lhayiya lhayiya) bulate the."
rows[472].row = 9380
rows[472].native = "वे तीरथराज निषाद के पु्त्र एवं प्रयागराज के पौत्र थे और निषाद राज एक महान महाराजा थे"
rows[472].human = "ve tirathraj nishad ke putr evam prayagraj ke pautra the aur nishad raj ek mahan maharaja the"
rows[473].row = 9395
rows[473].native = "इसने सशस्त्र आक्रामकता से निपटने के लिए राज्य सशस्त्र पुलिस की अपर्याप्तता का खुलासा किया जिसके कारण भारत सरकार ने विशेष रूप से नियंत्रित सीमा सुरक्षा बल की आवश्यकता महसूस की, जिसे पाकिस्तान के साथ अंतर्राष्ट्रीय सीमा बनाने के लिए सशस्त्र और प्रशिक्षित किया जाएगा।"
rows[473].human = "isne sashastra akramakta se nipatne ke lie rajya sashastra police ki aparyaptata ka khulasa kiya jiske karan bharat sarkar ne visesh rup se niyantrit sima suraksha bal ki aavashyakta mehsus ki, jise pakistan ke sath antarrashtriya sima banane ke lie sashastra aur prasikshit kiya jaega."
rows[474].row = 9424
rows[474].native = "हालांकि शुक्र के वायुमंडलीय मापन के अपने अभियान मे यह विफल हो गया, पर किसी अन्य ग्रह की धरती को छुने वाली यह पहली मानव निर्मित वस्तुं बन गई।"
rows[474].human = "halanki shukr ke vayumandaliya mapan ke apne abhiyan me yah vifal ho gaya, par kisi anya grah ki dharti ko chune vali yah pehli manav nirmit vastu ban gai."
rows[475].row = 9454
rows[475].native = "प्रिओम गुज्जर — विजय शंकर सुराना, समर का चचेरा भाई"
rows[475].human = "priyom gujjar - vijay shankar surana, samar ka chacera bhai"
rows[476].row = 9455
rows[476].native = "बिस्मिल की आत्मकथा को हिन्दी में काकोरी षड्यन्त्र नामक एक पुस्तक के अन्दर निज जीवन की एक छटा के नाम से भजनलाल बुकसेलर ने आर्ट प्रेस सिन्ध (अब पाकिस्तान) से और काकोरी के शहीद शीर्षक से गणेश शंकर विद्यार्थी ने प्रताप प्रेस, कानपुर से छापा था।"
rows[476].human = "bismil ki aatmkatha ko hindi me kakori shadyantra namak ek pustak ke andar nij jivan ki ek chata ke nam se bhajanlal bookseller ne art press sindh (ab pakistan) se aur kakori ke shahid sirshak se ganesh shankar vidyarthi ne pratap press, kanpur se chapa tha."
rows[477].row = 9489
rows[477].native = "श्रीकांत शास्त्री काल जैसे मगही साहित्य काल की भी परिकल्पना कर ली है।"
rows[477].human = "shrikant shastri kaal jaise maghi sahitya kaal ki bhi parikalpana kar li hai."
rows[478].row = 9496
rows[478].native = "अलू कप (पीएनजी) अपने पहले वनडे में अंपायर के रूप में खड़ा था।"
rows[478].human = "alu cup (PNG) apne pehle oneday me umpire ke rup me khada tha."
rows[479].row = 9511
rows[479].native = "वह उलझन में पड़ा था कि एक दिन स्वप्न में विक्रम खुद आए।"
rows[479].human = "vah uljhan me pada tha ki ek din svapna me vikram khuda aae."
rows[480].row = 9515
rows[480].native = "जब रॅपन्ज़ेल की उम्र बारह साल की थी, जादूगरनी ने उसे सबकी नज़रों से दूर जंगल के बीच एक ऐसी मीनार में बंद कर दिया, जिस पर चढ़ने के लिए न तो सीढ़ियां थीं और ना ही अंदर घुसने के लिए कोई दरवाज़ा, उसमें था तो सिर्फ़ एक कमरा और एक खिड़की."
rows[480].human = "jab repanzel ki umr barah sal ki thi, jadugarni ne use sabki nazro se dur jungle ke bich ek aisi minar me band kar diya, jis par chadhne ke lie na to sidhiyan thi aur na hi andar ghusne ke lie koi darvaza, usme tha to sirf ek kamra aur ek khidki."
rows[481].row = 9534
rows[481].native = "यहां पहाड़ों के मध्य फैली झील के आसपास किसी गेस्ट हाउस में रुक प्रकृति का मजा उठा सकते हैं।"
rows[481].human = "yaha pahado ke madhya faili jhil ke aaspas kisi guest house me ruk prakriti ka maja utha sakte hai."
rows[482].row = 9549
rows[482].native = "एक सराहनीय अग्रणी सूचीपत्र इस संग्रह के सभी सहित, शीर्षक, अध्याय और colophons, द्वारा बनाया गया था कनेको में जापान."
rows[482].human = "ek sarahaniya agarni suchipatr is sangrah ke sabhi sahit, sirshak, adhyaya aur colophons, dvara banaya gaya tha kaneko me japan."
rows[483].row = 9575
rows[483].native = "ग्रिल्स यह पद संभालने वाले दसवें व्यक्ति हैं और 1920 में रॉबर्ट बेडन पावेल के लिए इस पद के रचे जाने के बाद सबसे युवा चीफ़ स्काउट."
rows[483].human = "grills yah pad sambhalne vale dasve vyakti hai aur 1920 me robert bedan pavel ke liye is pad ke rache jane ke baad sabse yuva chief scout."
rows[484].row = 9590
rows[484].native = "2004 में ग्रिल्स को रॉयल नेवल रिज़र्व में लेफ्टिनेंट कमांडर के मानद दर्जे से सम्मानित किया गया।"
rows[484].human = "2004 me grills ko royal neval reserve me leftinent commander ke manad darje se sammanit kiya gaya."
rows[485].row = 9637
rows[485].native = "गतिशीलता के प्रभाव के लिए संगीत की लय को त्यागकर नई कविता ध्वनि-परिवर्तन की ओर बढ़ती गई है।"
rows[485].human = "gatishilta ke prabhav ke liye sangeet ki laiy ko tyagkar nayi kavita dhvani-parivartan ki or badhti gai hai."
rows[486].row = 9644
rows[486].native = "लघु वित्त (माइक्रो फाइनेंस)"
rows[486].human = "laghu vitt (micro finance)"
rows[487].row = 9668
rows[487].native = "एडविन म्योर : द स्ट्रक्चर ऑव द नावेल"
rows[487].human = "edwin myor : the structure ov the naavel"
rows[488].row = 9673
rows[488].native = "यहाँ की सबसे ऊँची पर्वत नजूरीकुण्ड है।"
rows[488].human = "yaha ki sabse unchi parvat najurikund hai."
rows[489].row = 9751
rows[489].native = "इसमें जटिल यौगिक बनाने की भी प्रवृत्ति पाई जाती है।"
rows[489].human = "isme jatil yaugik banane ki bhi pravritti payi jati hai."
rows[490].row = 9787
rows[490].native = "जिन लाहौर नईं वेख्या ओ जम्याइ नईं - 1991 (दिनमान प्रकाशन, दिल्ली से; बाद में वाणी प्रकाशन, नयी दिल्ली से)"
rows[490].human = "jin lahore nayi vekhya o jamyai nayi - 1991 (dinman prakashan, delhi se; baad me vani prakashan, new delhi se)"
rows[491].row = 9788
rows[491].native = "इसको मुर्गी और तीतर के बीच का बताया जाता है।"
rows[491].human = "isko murgi aur titar ke bich ka bataya jata hai."
rows[492].row = 9802
rows[492].native = "जनवरी 2006 को, अमेरिकन एक्सप्रेस ने अपने बैंक ऑफ हवाई कार्ड पोर्टफोलियो को बैंक ऑफ अमेरिका (MBNA) को बेच दिया।"
rows[492].human = "january 2006 ko, american express ne apne bank of havai card portfolio ko bank of america (MBNA) ko bech diya."
rows[493].row = 9851
rows[493].native = "बाल प्रधानत: निम्नलिखित चार प्रकार के होते हैं :"
rows[493].human = "baal pradhanata: nimnalikhit chaar prakar ke hote hai :"
rows[494].row = 9901
rows[494].native = "संयुक्त राज्य अमेरिका में एक दोहरी नागरिकता प्रणाली है जिसमें व्यक्ति अपने निवास राज्य के साथ संयुक्त राज्य का भी नागरिक है।"
rows[494].human = "sanyukta rajya america me ek dohri nagrikta pranali hai jisme vyakti apne nivas rajya ke sath sanyukta rajya ka bhi nagrik hai."
rows[495].row = 9923
rows[495].native = "राजस्थानी भाषा के साहित्यकार गोरधन सिंह शेखावत द्वारा संपादित शेखावाटी के साहित्यकार व रघुनाथ प्रसाद तिवारी 'उमंग' के ग्रंथ खंडेला क्षेत्र का सांस्कृतिकवैभव में भी जोशी का वर्णन है।"
rows[495].human = "rajsthani bhasha ke sahityakar gordhan singh shekhavat dvara sampadit shekhavati ke sahityakar va raghunath prasad tivari 'umang' ke granth khandela kshetra ka sanskrtikvaibhav me bhi joshi ka varnan hai."
rows[496].row = 9932
rows[496].native = "इस एल्बम के जारी होने पर लगभग किसी का ध्यान नहीं गया।"
rows[496].human = "is album ke jari hone par lagbhag kisi ka dhyan nahi gaya."
rows[497].row = 9949
rows[497].native = "इसका उपयोग कुटीर उद्योग के रूप में सूत उत्पादन में किया जाता है।"
rows[497].human = "iska upayog kutir udyog ke rup me sut utpadan me kiya jata hai."
rows[498].row = 9965
rows[498].native = "पाश्चात्य दर्शन के सम्प्रदाय (गूगल पुस्तक; लेखिका - शोभा निगम)"
rows[498].human = "paschatya darshan ke sampraday (google pustak; lekhika - shobha nigam)"
rows[499].row = 9969
rows[499].native = "2003 में गद्दाफी ने पश्चिमी देशों के साथ \"मैत्री\" के बदले में सीडब्ल्यूसी को स्वीकार करने के लिए सहमति प्रदान की।"
rows[499].human = "2003 me gaddafi ne paschimi desho ke sath \"maitri\" ke badle me cwc ko svikar karne ke liye sehmati pradan ki."
resample_positions = [1, 3, 4, 6, 12, 15, 16, 17, 18, 22, 24, 27, 28, 35, 36, 37, 39, 41, 42, 43, 49, 55, 58, 59, 61, 64, 66, 69, 70, 71, 73, 74, 83, 84, 88, 90, 92, 93, 94, 96, 97, 102, 103, 110, 114, 115, 128, 132, 133, 137, 138, 145, 149, 154, 155, 157, 158, 164, 165, 166, 169, 174, 176, 177, 179, 181, 183, 184, 185, 186, 188, 189, 192, 196, 202, 203, 207, 210, 211, 214, 218, 219, 221, 225, 227, 232, 233, 235, 237, 239, 240, 241, 244, 247, 249, 251, 253, 255, 256, 257, 259, 260, 262, 266, 267, 268, 270, 272, 275, 276, 284, 285, 286, 288, 289, 290, 293, 295, 296, 302, 311, 313, 323, 326, 327, 328, 332, 336, 337, 338, 342, 343, 347, 348, 356, 357, 358, 359, 362, 363, 369, 370, 374, 375, 381, 386, 387, 389, 394, 399, 400, 401, 402, 406, 407, 408, 409, 412, 414, 415, 417, 420, 421, 422, 423, 424, 425, 426, 429, 430, 437, 438, 446, 447, 448, 451, 452, 455, 456, 460, 461, 466, 468, 469, 472, 473, 475, 476, 477, 478, 479, 482, 483, 484, 488, 489, 491, 493, 497, 499]
`````

#### `results/k3b_hi/stats.csv` (566 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

| statistic | gemini_rate | human_rate | ratio | ci90 | ci95 | verdict |
|---|---|---|---|---|---|---|
| vowel_doubling | 0.013083335156540574 | 0.01493871854145767 | 0.8758003653547612 | [0.7652356242062518, 0.9964025473338749] | [0.743037014212196, 1.022126295537717] | inconclusive |
| h_digraph | 0.028529546896536636 | 0.028547127840537357 | 0.9993841431579763 | [0.9849955131866562, 1.0139375163516189] | [0.9821778954535723, 1.016670940027307] | matches |
| english_word_share | 0.0862589853109699 | 0.0770033388981636 | 1.1201979881034356 | [1.0530057097907044, 1.193341769677889] | [1.0404890729787815, 1.2068213660921743] | matches |

#### `results/k3b_hi/verdict.json` (1,625 bytes; first commit a5a446e 2026-10-30 01:11:23 +0530)

`````text
provenance.config.registered = "RESULTS.md 2026-10-23 12:05 (K3b-hi)"
provenance.config.model = "gemini-3.5-flash-lite"
provenance.config.prompt = "natural_romanization_hi_v1"
provenance.git_commit = "4b459081c6cfa05ec09123165f0f6f8a65778d39"
provenance.timestamp_utc = "2026-10-29T08:22:37+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/k3b_dakshina.py", "analyse", "hi"]
K3b = "inconclusive"
statistics.vowel_doubling.gemini_rate = 0.013083335156540574
statistics.vowel_doubling.human_rate = 0.01493871854145767
statistics.vowel_doubling.ratio = 0.8758003653547612
statistics.vowel_doubling.ci90 = [0.7652356242062518, 0.9964025473338749]
statistics.vowel_doubling.ci95 = [0.743037014212196, 1.022126295537717]
statistics.vowel_doubling.verdict = "inconclusive"
statistics.h_digraph.gemini_rate = 0.028529546896536636
statistics.h_digraph.human_rate = 0.028547127840537357
statistics.h_digraph.ratio = 0.9993841431579763
statistics.h_digraph.ci90 = [0.9849955131866562, 1.0139375163516189]
statistics.h_digraph.ci95 = [0.9821778954535723, 1.016670940027307]
statistics.h_digraph.verdict = "matches"
statistics.english_word_share.gemini_rate = 0.0862589853109699
statistics.english_word_share.human_rate = 0.0770033388981636
statistics.english_word_share.ratio = 1.1201979881034356
statistics.english_word_share.ci90 = [1.0530057097907044, 1.193341769677889]
statistics.english_word_share.ci95 = [1.0404890729787815, 1.2068213660921743]
statistics.english_word_share.verdict = "matches"
n = 499
n_primary_defective_excluded = 1
`````

#### `results/english_share/shares.csv` (9,925 bytes; first commit 83c256e 2026-10-22 17:55:12 +0530)

| sample | n_items | wordlist | variant | quantity | n_words | n_english | value | ci_low | ci_high |
|---|---|---|---|---|---|---|---|---|---|
| m4c496 | 496 | zipf>=3 | all words | natural | 7706.0 | 794.0 | 0.10303659486114716 | 0.09248333172033575 | 0.11380530550774974 |
| m4c496 | 496 | zipf>=3 | all words | lossy | 7665.0 | 417.0 | 0.054403131115459885 | 0.048186231863869354 | 0.06080729493167001 |
| m4c496 | 496 | zipf>=3 | all words | itrans | 7665.0 | 378.0 | 0.049315068493150684 | 0.043449606849767175 | 0.05542235259411518 |
| m4c496 | 496 | zipf>=3 | all words | natural - lossy |  |  | 0.04863346374568728 | 0.04080176599336014 | 0.056657197862294166 |
| m4c496 | 496 | zipf>=3 | all words | natural - itrans |  |  | 0.05372152636799648 | 0.045504912280370687 | 0.06214049301917147 |
| m4c496 | 496 | zipf>=3 | no proper nouns | natural | 7598.0 | 727.0 | 0.09568307449328771 | 0.08576788438952816 | 0.105935792920926 |
| m4c496 | 496 | zipf>=3 | no proper nouns | lossy | 7617.0 | 387.0 | 0.05080740448995667 | 0.04498442088665966 | 0.05690428655881502 |
| m4c496 | 496 | zipf>=3 | no proper nouns | itrans | 7623.0 | 350.0 | 0.04591368227731864 | 0.040379863088476124 | 0.05161897454525179 |
| m4c496 | 496 | zipf>=3 | no proper nouns | natural - lossy |  |  | 0.044875670003331036 | 0.03736731944422698 | 0.05258294672168892 |
| m4c496 | 496 | zipf>=3 | no proper nouns | natural - itrans |  |  | 0.04976939221596907 | 0.04199283350839436 | 0.057805973910247936 |
| m4c496 | 496 | zipf>=3 | all words, ITRANS as written | natural | 7706.0 | 794.0 | 0.10303659486114716 | 0.09248333172033575 | 0.11380530550774974 |
| m4c496 | 496 | zipf>=3 | all words, ITRANS as written | lossy | 7665.0 | 417.0 | 0.054403131115459885 | 0.048186231863869354 | 0.06080729493167001 |
| m4c496 | 496 | zipf>=3 | all words, ITRANS as written | itrans | 7665.0 | 94.0 | 0.012263535551206784 | 0.00949708376092469 | 0.015290220165431566 |
| m4c496 | 496 | zipf>=3 | all words, ITRANS as written | natural - lossy |  |  | 0.04863346374568728 | 0.04080176599336014 | 0.056657197862294166 |
| m4c496 | 496 | zipf>=3 | all words, ITRANS as written | natural - itrans |  |  | 0.09077305930994038 | 0.0811472099836099 | 0.10051375688235968 |
| m4c496 | 496 | zipf>=3 | words of 4+ characters | natural | 7312.0 | 519.0 | 0.07097921225382932 | 0.06211657994438943 | 0.0801322737273348 |
| m4c496 | 496 | zipf>=3 | words of 4+ characters | lossy | 7272.0 | 157.0 | 0.02158965896589659 | 0.01813178390524432 | 0.02514614479623727 |
| m4c496 | 496 | zipf>=3 | words of 4+ characters | itrans | 7280.0 | 133.0 | 0.01826923076923077 | 0.015053146835648915 | 0.0215711930985026 |
| m4c496 | 496 | zipf>=3 | words of 4+ characters | natural - lossy |  |  | 0.04938955328793273 | 0.041673594336962536 | 0.057383572227381184 |
| m4c496 | 496 | zipf>=3 | words of 4+ characters | natural - itrans |  |  | 0.052709981484598545 | 0.04469287129391108 | 0.060967397589282254 |
| m4c496 | 496 | zipf>=4 | all words | natural | 7706.0 | 502.0 | 0.06514404360238775 | 0.05652621455122704 | 0.07417088319057902 |
| m4c496 | 496 | zipf>=4 | all words | lossy | 7665.0 | 245.0 | 0.0319634703196347 | 0.02744178950182281 | 0.0366159556552689 |
| m4c496 | 496 | zipf>=4 | all words | itrans | 7665.0 | 220.0 | 0.028701891715590344 | 0.0243486630347265 | 0.033165409695676475 |
| m4c496 | 496 | zipf>=4 | all words | natural - lossy |  |  | 0.03318057328275305 | 0.02579870215656963 | 0.040774294716185294 |
| m4c496 | 496 | zipf>=4 | all words | natural - itrans |  |  | 0.036442151886797405 | 0.028762301772784927 | 0.044394531417819974 |
| m4c496 | 496 | zipf>=4 | no proper nouns | natural | 7598.0 | 459.0 | 0.060410634377467756 | 0.051927155759545686 | 0.0693044012903845 |
| m4c496 | 496 | zipf>=4 | no proper nouns | lossy | 7617.0 | 229.0 | 0.030064329788630696 | 0.025757117126783483 | 0.034549702094147566 |
| m4c496 | 496 | zipf>=4 | no proper nouns | itrans | 7623.0 | 206.0 | 0.027023481568936115 | 0.022850157259164845 | 0.03129614412804715 |
| m4c496 | 496 | zipf>=4 | no proper nouns | natural - lossy |  |  | 0.03034630458883706 | 0.023124687272819258 | 0.03792693068711946 |
| m4c496 | 496 | zipf>=4 | no proper nouns | natural - itrans |  |  | 0.03338715280853164 | 0.02588258246580862 | 0.041273996949608295 |
| m4c496 | 496 | zipf>=4 | all words, ITRANS as written | natural | 7706.0 | 502.0 | 0.06514404360238775 | 0.05652621455122704 | 0.07417088319057902 |
| m4c496 | 496 | zipf>=4 | all words, ITRANS as written | lossy | 7665.0 | 245.0 | 0.0319634703196347 | 0.02744178950182281 | 0.0366159556552689 |
| m4c496 | 496 | zipf>=4 | all words, ITRANS as written | itrans | 7665.0 | 42.0 | 0.005479452054794521 | 0.003655615782175722 | 0.007505031909216076 |
| m4c496 | 496 | zipf>=4 | all words, ITRANS as written | natural - lossy |  |  | 0.03318057328275305 | 0.02579870215656963 | 0.040774294716185294 |
| m4c496 | 496 | zipf>=4 | all words, ITRANS as written | natural - itrans |  |  | 0.05966459154759323 | 0.051430049042211115 | 0.0682610228906823 |
| m4c496 | 496 | zipf>=4 | words of 4+ characters | natural | 7312.0 | 343.0 | 0.04690919037199125 | 0.039623818582107284 | 0.054581514919860775 |
| m4c496 | 496 | zipf>=4 | words of 4+ characters | lossy | 7272.0 | 58.0 | 0.007975797579757976 | 0.005860693174094866 | 0.010194010508970031 |
| m4c496 | 496 | zipf>=4 | words of 4+ characters | itrans | 7280.0 | 44.0 | 0.006043956043956044 | 0.004184058080642721 | 0.008016616561943277 |
| m4c496 | 496 | zipf>=4 | words of 4+ characters | natural - lossy |  |  | 0.03893339279223327 | 0.03215482860394437 | 0.046002130323198075 |
| m4c496 | 496 | zipf>=4 | words of 4+ characters | natural - itrans |  |  | 0.0408652343280352 | 0.03396950031732427 | 0.04813632676758927 |
| sentiment198 | 198 | zipf>=3 | all words | natural | 3328.0 | 365.0 | 0.10967548076923077 | 0.09636788590326058 | 0.12303226339648388 |
| sentiment198 | 198 | zipf>=3 | all words | lossy | 3310.0 | 137.0 | 0.04138972809667674 | 0.03417105699321102 | 0.048552348403680466 |
| sentiment198 | 198 | zipf>=3 | all words | itrans | 3310.0 | 125.0 | 0.0377643504531722 | 0.03073644116526077 | 0.044830815783011305 |
| sentiment198 | 198 | zipf>=3 | all words | natural - lossy |  |  | 0.06828575267255403 | 0.05685300184177052 | 0.07986584074022215 |
| sentiment198 | 198 | zipf>=3 | all words | natural - itrans |  |  | 0.07191113031605856 | 0.0600131178406972 | 0.08377953795836804 |
| sentiment198 | 198 | zipf>=3 | no proper nouns | natural | 3314.0 | 357.0 | 0.10772480386240194 | 0.0944902214840229 | 0.12112600146429855 |
| sentiment198 | 198 | zipf>=3 | no proper nouns | lossy | 3307.0 | 136.0 | 0.04112488660417297 | 0.03384882280411624 | 0.04832161851231224 |
| sentiment198 | 198 | zipf>=3 | no proper nouns | itrans | 3306.0 | 124.0 | 0.03750756200846945 | 0.030389728181191993 | 0.04457442923096145 |
| sentiment198 | 198 | zipf>=3 | no proper nouns | natural - lossy |  |  | 0.06659991725822897 | 0.0552043279524618 | 0.07806310975984303 |
| sentiment198 | 198 | zipf>=3 | no proper nouns | natural - itrans |  |  | 0.0702172418539325 | 0.058508603151008726 | 0.08201966758458855 |
| sentiment198 | 198 | zipf>=3 | all words, ITRANS as written | natural | 3328.0 | 365.0 | 0.10967548076923077 | 0.09636788590326058 | 0.12303226339648388 |
| sentiment198 | 198 | zipf>=3 | all words, ITRANS as written | lossy | 3310.0 | 137.0 | 0.04138972809667674 | 0.03417105699321102 | 0.048552348403680466 |
| sentiment198 | 198 | zipf>=3 | all words, ITRANS as written | itrans | 3310.0 | 24.0 | 0.0072507552870090634 | 0.004477134633834346 | 0.010256529850746267 |
| sentiment198 | 198 | zipf>=3 | all words, ITRANS as written | natural - lossy |  |  | 0.06828575267255403 | 0.05685300184177052 | 0.07986584074022215 |
| sentiment198 | 198 | zipf>=3 | all words, ITRANS as written | natural - itrans |  |  | 0.1024247254822217 | 0.08924303198593754 | 0.11581858785255453 |
| sentiment198 | 198 | zipf>=3 | words of 4+ characters | natural | 3095.0 | 259.0 | 0.08368336025848142 | 0.07142857142857142 | 0.09591701229716947 |
| sentiment198 | 198 | zipf>=3 | words of 4+ characters | lossy | 3081.0 | 55.0 | 0.017851346965271016 | 0.013141416754918006 | 0.022837089553474577 |
| sentiment198 | 198 | zipf>=3 | words of 4+ characters | itrans | 3082.0 | 46.0 | 0.014925373134328358 | 0.010613510695857581 | 0.01969597364710922 |
| sentiment198 | 198 | zipf>=3 | words of 4+ characters | natural - lossy |  |  | 0.0658320132932104 | 0.05402572940362109 | 0.0778461840892361 |
| sentiment198 | 198 | zipf>=3 | words of 4+ characters | natural - itrans |  |  | 0.06875798712415306 | 0.056821961491841134 | 0.0808749219112494 |
| sentiment198 | 198 | zipf>=4 | all words | natural | 3328.0 | 217.0 | 0.06520432692307693 | 0.0539107718505966 | 0.07641033758546055 |
| sentiment198 | 198 | zipf>=4 | all words | lossy | 3310.0 | 80.0 | 0.02416918429003021 | 0.018734321540567506 | 0.02993691277154562 |
| sentiment198 | 198 | zipf>=4 | all words | itrans | 3310.0 | 70.0 | 0.021148036253776436 | 0.015943258359540764 | 0.026551798740167634 |
| sentiment198 | 198 | zipf>=4 | all words | natural - lossy |  |  | 0.041035142633046716 | 0.03053792007383642 | 0.05148326554683049 |
| sentiment198 | 198 | zipf>=4 | all words | natural - itrans |  |  | 0.04405629066930049 | 0.033449324431291116 | 0.05451017401533986 |
| sentiment198 | 198 | zipf>=4 | no proper nouns | natural | 3314.0 | 211.0 | 0.06366928183464092 | 0.05256828278005575 | 0.07474722044905974 |
| sentiment198 | 198 | zipf>=4 | no proper nouns | lossy | 3307.0 | 79.0 | 0.02388872089507106 | 0.018435747377045203 | 0.029697147897677155 |
| sentiment198 | 198 | zipf>=4 | no proper nouns | itrans | 3306.0 | 69.0 | 0.020871143375680582 | 0.015638480066548978 | 0.026292201971915147 |
| sentiment198 | 198 | zipf>=4 | no proper nouns | natural - lossy |  |  | 0.03978056093956986 | 0.029456072708439265 | 0.050014721696556165 |
| sentiment198 | 198 | zipf>=4 | no proper nouns | natural - itrans |  |  | 0.04279813845896034 | 0.0324433729639251 | 0.052958996086941275 |
| sentiment198 | 198 | zipf>=4 | all words, ITRANS as written | natural | 3328.0 | 217.0 | 0.06520432692307693 | 0.0539107718505966 | 0.07641033758546055 |
| sentiment198 | 198 | zipf>=4 | all words, ITRANS as written | lossy | 3310.0 | 80.0 | 0.02416918429003021 | 0.018734321540567506 | 0.02993691277154562 |
| sentiment198 | 198 | zipf>=4 | all words, ITRANS as written | itrans | 3310.0 | 9.0 | 0.002719033232628399 | 0.0011671931218183284 | 0.004514689674011276 |
| sentiment198 | 198 | zipf>=4 | all words, ITRANS as written | natural - lossy |  |  | 0.041035142633046716 | 0.03053792007383642 | 0.05148326554683049 |
| sentiment198 | 198 | zipf>=4 | all words, ITRANS as written | natural - itrans |  |  | 0.06248529369044853 | 0.05145230080422855 | 0.07360583413015194 |
| sentiment198 | 198 | zipf>=4 | words of 4+ characters | natural | 3095.0 | 160.0 | 0.051696284329563816 | 0.04148963876777892 | 0.06191200015740169 |
| sentiment198 | 198 | zipf>=4 | words of 4+ characters | lossy | 3081.0 | 23.0 | 0.007465108730931516 | 0.0044885877121560456 | 0.010671740984887603 |
| sentiment198 | 198 | zipf>=4 | words of 4+ characters | itrans | 3082.0 | 15.0 | 0.004866969500324465 | 0.0024234530148249155 | 0.007617745735916297 |
| sentiment198 | 198 | zipf>=4 | words of 4+ characters | natural - lossy |  |  | 0.0442311755986323 | 0.03460496575988525 | 0.05411858824760904 |
| sentiment198 | 198 | zipf>=4 | words of 4+ characters | natural - itrans |  |  | 0.046829314829239355 | 0.03718877937086411 | 0.056624235076009236 |

#### `results/english_share/wordlist.json` (17,782 bytes; first commit 83c256e 2026-10-22 17:55:12 +0530)

`````text
provenance.config.status = "post hoc descriptive, 2026-10-22, no verdict"
provenance.config.bootstrap = 10000
provenance.config.seed = 0
provenance.git_commit = "e50581c51fa4c7a4b7e492d86c89e144bb8b2186-dirty"
provenance.timestamp_utc = "2026-10-22T12:38:13+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/english_share.py"]
source = "wordfreq 3.1.1, language en, list 'best'"
url = "https://github.com/rspeer/wordfreq"
sizes.zipf>=3 = 29269
sizes.zipf>=4 = 7223
top_matched_words_zipf3_all_words.m4c496.natural[0] = ["ee", 65]
top_matched_words_zipf3_all_words.m4c496.natural[1] = ["na", 21]
top_matched_words_zipf3_all_words.m4c496.natural[2] = ["aa", 19]
top_matched_words_zipf3_all_words.m4c496.natural[3] = ["ella", 16]
top_matched_words_zipf3_all_words.m4c496.natural[4] = ["ne", 14]
top_matched_words_zipf3_all_words.m4c496.natural[5] = ["ra", 10]
top_matched_words_zipf3_all_words.m4c496.natural[6] = ["matte", 7]
top_matched_words_zipf3_all_words.m4c496.natural[7] = ["ada", 6]
top_matched_words_zipf3_all_words.m4c496.natural[8] = ["new", 5]
top_matched_words_zipf3_all_words.m4c496.natural[9] = ["andre", 5]
top_matched_words_zipf3_all_words.m4c496.natural[10] = ["ide", 5]
top_matched_words_zipf3_all_words.m4c496.natural[11] = ["ive", 5]
top_matched_words_zipf3_all_words.m4c496.natural[12] = ["of", 4]
top_matched_words_zipf3_all_words.m4c496.natural[13] = ["vega", 4]
top_matched_words_zipf3_all_words.m4c496.natural[14] = ["police", 4]
top_matched_words_zipf3_all_words.m4c496.natural[15] = ["da", 4]
top_matched_words_zipf3_all_words.m4c496.natural[16] = ["british", 4]
top_matched_words_zipf3_all_words.m4c496.natural[17] = ["august", 4]
top_matched_words_zipf3_all_words.m4c496.natural[18] = ["french", 4]
top_matched_words_zipf3_all_words.m4c496.natural[19] = ["bali", 4]
top_matched_words_zipf3_all_words.m4c496.natural[20] = ["website", 4]
top_matched_words_zipf3_all_words.m4c496.natural[21] = ["kai", 4]
top_matched_words_zipf3_all_words.m4c496.natural[22] = ["ski", 4]
top_matched_words_zipf3_all_words.m4c496.natural[23] = ["reed", 3]
top_matched_words_zipf3_all_words.m4c496.natural[24] = ["roman", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[0] = ["i", 67]
top_matched_words_zipf3_all_words.m4c496.lossy[1] = ["a", 21]
top_matched_words_zipf3_all_words.m4c496.lossy[2] = ["ella", 16]
top_matched_words_zipf3_all_words.m4c496.lossy[3] = ["ne", 14]
top_matched_words_zipf3_all_words.m4c496.lossy[4] = ["ra", 10]
top_matched_words_zipf3_all_words.m4c496.lossy[5] = ["ap", 7]
top_matched_words_zipf3_all_words.m4c496.lossy[6] = ["matte", 7]
top_matched_words_zipf3_all_words.m4c496.lossy[7] = ["na", 7]
top_matched_words_zipf3_all_words.m4c496.lossy[8] = ["ada", 6]
top_matched_words_zipf3_all_words.m4c496.lossy[9] = ["ide", 5]
top_matched_words_zipf3_all_words.m4c496.lossy[10] = ["ive", 5]
top_matched_words_zipf3_all_words.m4c496.lossy[11] = ["ski", 5]
top_matched_words_zipf3_all_words.m4c496.lossy[12] = ["rid", 4]
top_matched_words_zipf3_all_words.m4c496.lossy[13] = ["vega", 4]
top_matched_words_zipf3_all_words.m4c496.lossy[14] = ["british", 4]
top_matched_words_zipf3_all_words.m4c496.lossy[15] = ["bali", 4]
top_matched_words_zipf3_all_words.m4c496.lossy[16] = ["kai", 4]
top_matched_words_zipf3_all_words.m4c496.lossy[17] = ["roman", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[18] = ["bu", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[19] = ["sari", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[20] = ["raja", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[21] = ["lens", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[22] = ["jan", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[23] = ["nyu", 3]
top_matched_words_zipf3_all_words.m4c496.lossy[24] = ["ge", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[0] = ["i", 67]
top_matched_words_zipf3_all_words.m4c496.itrans[1] = ["a", 21]
top_matched_words_zipf3_all_words.m4c496.itrans[2] = ["ella", 16]
top_matched_words_zipf3_all_words.m4c496.itrans[3] = ["ne", 14]
top_matched_words_zipf3_all_words.m4c496.itrans[4] = ["ra", 10]
top_matched_words_zipf3_all_words.m4c496.itrans[5] = ["matte", 7]
top_matched_words_zipf3_all_words.m4c496.itrans[6] = ["na", 7]
top_matched_words_zipf3_all_words.m4c496.itrans[7] = ["ada", 6]
top_matched_words_zipf3_all_words.m4c496.itrans[8] = ["ide", 5]
top_matched_words_zipf3_all_words.m4c496.itrans[9] = ["ive", 5]
top_matched_words_zipf3_all_words.m4c496.itrans[10] = ["ski", 5]
top_matched_words_zipf3_all_words.m4c496.itrans[11] = ["rid", 4]
top_matched_words_zipf3_all_words.m4c496.itrans[12] = ["vega", 4]
top_matched_words_zipf3_all_words.m4c496.itrans[13] = ["british", 4]
top_matched_words_zipf3_all_words.m4c496.itrans[14] = ["bali", 4]
top_matched_words_zipf3_all_words.m4c496.itrans[15] = ["kai", 4]
top_matched_words_zipf3_all_words.m4c496.itrans[16] = ["roman", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[17] = ["sari", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[18] = ["raja", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[19] = ["lens", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[20] = ["jan", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[21] = ["nyu", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[22] = ["ge", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[23] = ["travel", 3]
top_matched_words_zipf3_all_words.m4c496.itrans[24] = ["adi", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[0] = ["ee", 26]
top_matched_words_zipf3_all_words.sentiment198.natural[1] = ["ella", 15]
top_matched_words_zipf3_all_words.sentiment198.natural[2] = ["ac", 6]
top_matched_words_zipf3_all_words.sentiment198.natural[3] = ["air", 6]
top_matched_words_zipf3_all_words.sentiment198.natural[4] = ["collar", 5]
top_matched_words_zipf3_all_words.sentiment198.natural[5] = ["ide", 5]
top_matched_words_zipf3_all_words.sentiment198.natural[6] = ["application", 5]
top_matched_words_zipf3_all_words.sentiment198.natural[7] = ["play", 4]
top_matched_words_zipf3_all_words.sentiment198.natural[8] = ["fan", 4]
top_matched_words_zipf3_all_words.sentiment198.natural[9] = ["home", 4]
top_matched_words_zipf3_all_words.sentiment198.natural[10] = ["na", 4]
top_matched_words_zipf3_all_words.sentiment198.natural[11] = ["ge", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[12] = ["wifi", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[13] = ["table", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[14] = ["dark", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[15] = ["cooler", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[16] = ["buckle", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[17] = ["brush", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[18] = ["andre", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[19] = ["order", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[20] = ["bluetooth", 3]
top_matched_words_zipf3_all_words.sentiment198.natural[21] = ["online", 2]
top_matched_words_zipf3_all_words.sentiment198.natural[22] = ["booking", 2]
top_matched_words_zipf3_all_words.sentiment198.natural[23] = ["tv", 2]
top_matched_words_zipf3_all_words.sentiment198.natural[24] = ["e", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[0] = ["i", 30]
top_matched_words_zipf3_all_words.sentiment198.lossy[1] = ["ella", 15]
top_matched_words_zipf3_all_words.sentiment198.lossy[2] = ["er", 6]
top_matched_words_zipf3_all_words.sentiment198.lossy[3] = ["ide", 4]
top_matched_words_zipf3_all_words.sentiment198.lossy[4] = ["dark", 3]
top_matched_words_zipf3_all_words.sentiment198.lossy[5] = ["ada", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[6] = ["adi", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[7] = ["pet", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[8] = ["omega", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[9] = ["mane", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[10] = ["ap", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[11] = ["said", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[12] = ["hat", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[13] = ["ji", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[14] = ["ya", 2]
top_matched_words_zipf3_all_words.sentiment198.lossy[15] = ["ge", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[16] = ["park", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[17] = ["oh", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[18] = ["rum", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[19] = ["tay", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[20] = ["la", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[21] = ["ive", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[22] = ["aha", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[23] = ["ring", 1]
top_matched_words_zipf3_all_words.sentiment198.lossy[24] = ["ray", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[0] = ["i", 30]
top_matched_words_zipf3_all_words.sentiment198.itrans[1] = ["ella", 15]
top_matched_words_zipf3_all_words.sentiment198.itrans[2] = ["er", 6]
top_matched_words_zipf3_all_words.sentiment198.itrans[3] = ["ide", 4]
top_matched_words_zipf3_all_words.sentiment198.itrans[4] = ["dark", 3]
top_matched_words_zipf3_all_words.sentiment198.itrans[5] = ["ada", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[6] = ["adi", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[7] = ["pet", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[8] = ["omega", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[9] = ["mane", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[10] = ["said", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[11] = ["hat", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[12] = ["ji", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[13] = ["ya", 2]
top_matched_words_zipf3_all_words.sentiment198.itrans[14] = ["ge", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[15] = ["park", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[16] = ["oh", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[17] = ["rum", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[18] = ["la", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[19] = ["ive", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[20] = ["aha", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[21] = ["ray", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[22] = ["patel", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[23] = ["ni", 1]
top_matched_words_zipf3_all_words.sentiment198.itrans[24] = ["ra", 1]
top_matched_words_zipf3_4plus_chars.m4c496.natural[0] = ["ella", 16]
top_matched_words_zipf3_4plus_chars.m4c496.natural[1] = ["matte", 7]
top_matched_words_zipf3_4plus_chars.m4c496.natural[2] = ["andre", 5]
top_matched_words_zipf3_4plus_chars.m4c496.natural[3] = ["vega", 4]
top_matched_words_zipf3_4plus_chars.m4c496.natural[4] = ["police", 4]
top_matched_words_zipf3_4plus_chars.m4c496.natural[5] = ["british", 4]
top_matched_words_zipf3_4plus_chars.m4c496.natural[6] = ["august", 4]
top_matched_words_zipf3_4plus_chars.m4c496.natural[7] = ["french", 4]
top_matched_words_zipf3_4plus_chars.m4c496.natural[8] = ["bali", 4]
top_matched_words_zipf3_4plus_chars.m4c496.natural[9] = ["website", 4]
top_matched_words_zipf3_4plus_chars.m4c496.natural[10] = ["reed", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[11] = ["roman", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[12] = ["internet", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[13] = ["july", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[14] = ["station", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[15] = ["sari", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[16] = ["german", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[17] = ["lens", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[18] = ["john", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[19] = ["running", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[20] = ["travel", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[21] = ["australia", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[22] = ["luna", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[23] = ["france", 3]
top_matched_words_zipf3_4plus_chars.m4c496.natural[24] = ["traffic", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[0] = ["ella", 16]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[1] = ["matte", 7]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[2] = ["vega", 4]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[3] = ["british", 4]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[4] = ["bali", 4]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[5] = ["roman", 3]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[6] = ["sari", 3]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[7] = ["raja", 3]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[8] = ["lens", 3]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[9] = ["travel", 3]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[10] = ["luna", 3]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[11] = ["star", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[12] = ["hana", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[13] = ["march", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[14] = ["japan", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[15] = ["port", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[16] = ["visa", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[17] = ["jerusalem", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[18] = ["shaping", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[19] = ["banda", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[20] = ["patti", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[21] = ["nobel", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[22] = ["devi", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[23] = ["apis", 2]
top_matched_words_zipf3_4plus_chars.m4c496.lossy[24] = ["sporting", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[0] = ["ella", 16]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[1] = ["matte", 7]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[2] = ["vega", 4]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[3] = ["british", 4]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[4] = ["bali", 4]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[5] = ["roman", 3]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[6] = ["sari", 3]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[7] = ["raja", 3]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[8] = ["lens", 3]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[9] = ["travel", 3]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[10] = ["luna", 3]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[11] = ["star", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[12] = ["hana", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[13] = ["march", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[14] = ["japan", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[15] = ["visa", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[16] = ["jerusalem", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[17] = ["patti", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[18] = ["nobel", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[19] = ["devi", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[20] = ["kimi", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[21] = ["sami", 2]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[22] = ["pakistani", 1]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[23] = ["shri", 1]
top_matched_words_zipf3_4plus_chars.m4c496.itrans[24] = ["maga", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[0] = ["ella", 15]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[1] = ["collar", 5]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[2] = ["application", 5]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[3] = ["play", 4]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[4] = ["home", 4]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[5] = ["wifi", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[6] = ["table", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[7] = ["dark", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[8] = ["cooler", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[9] = ["buckle", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[10] = ["brush", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[11] = ["andre", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[12] = ["order", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[13] = ["bluetooth", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[14] = ["online", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[15] = ["booking", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[16] = ["theater", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[17] = ["love", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[18] = ["omega", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[19] = ["mane", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[20] = ["side", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[21] = ["clip", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[22] = ["multimedia", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[23] = ["filter", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.natural[24] = ["slot", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[0] = ["ella", 15]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[1] = ["dark", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[2] = ["omega", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[3] = ["mane", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[4] = ["said", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[5] = ["park", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[6] = ["ring", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[7] = ["bank", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[8] = ["patel", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[9] = ["patti", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[10] = ["tennis", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[11] = ["dina", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[12] = ["star", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[13] = ["kilo", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[14] = ["kris", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[15] = ["plan", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[16] = ["insta", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[17] = ["smart", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[18] = ["mimi", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[19] = ["chanel", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[20] = ["bust", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[21] = ["kate", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[22] = ["pest", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[23] = ["reddit", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.lossy[24] = ["sink", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[0] = ["ella", 15]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[1] = ["dark", 3]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[2] = ["omega", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[3] = ["mane", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[4] = ["said", 2]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[5] = ["park", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[6] = ["patel", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[7] = ["patti", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[8] = ["tennis", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[9] = ["dina", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[10] = ["star", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[11] = ["kilo", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[12] = ["kris", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[13] = ["plan", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[14] = ["smart", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[15] = ["mimi", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[16] = ["chanel", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[17] = ["bust", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[18] = ["pest", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[19] = ["reddit", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[20] = ["edit", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[21] = ["amish", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[22] = ["modi", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[23] = ["bali", 1]
top_matched_words_zipf3_4plus_chars.sentiment198.itrans[24] = ["split", 1]
proper_noun_rule = "capitalized, not sentence-initial, in natural"
`````

#### `results/codemix_check/check_sample0_v1.json` (2,968 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
provenance.config.gold = "gold_sample0.json"
provenance.git_commit = "07ba540f5d484beeb92d283e5be387b748d48300-dirty"
provenance.timestamp_utc = "2026-10-26T06:36:23+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/codemix_check.py", "0", "v1"]
seed = 0
tagger = "v1"
texts = 50
alphabetic_tokens = 883
tokens_tagged_en = 236
main (H not English).tp = 219
main (H not English).fp = 17
main (H not English).fn = 29
main (H not English).precision = 0.9279661016949152
main (H not English).recall = 0.8830645161290323
sensitivity (H English).tp = 219
sensitivity (H English).fp = 17
sensitivity (H English).fn = 38
sensitivity (H English).precision = 0.9279661016949152
sensitivity (H English).recall = 0.8521400778210116
errors.false_positive[0] = ["african", "N"]
errors.false_positive[1] = ["amsterdam", "N"]
errors.false_positive[2] = ["angola", "N"]
errors.false_positive[3] = ["austrian", "N"]
errors.false_positive[4] = ["bis", "N"]
errors.false_positive[5] = ["claudia", "N"]
errors.false_positive[6] = ["frank", "N"]
errors.false_positive[7] = ["germany", "N"]
errors.false_positive[8] = ["iceland", "N"]
errors.false_positive[9] = ["kami", "K"]
errors.false_positive[10] = ["luxembourg", "N"]
errors.false_positive[11] = ["machu", "N"]
errors.false_positive[12] = ["mediterranean", "N"]
errors.false_positive[13] = ["russian", "N"]
errors.false_positive[14] = ["stearns", "N"]
errors.missed_english[0] = ["ad", "u"]
errors.missed_english[1] = ["air", "u"]
errors.missed_english[2] = ["and", "u"]
errors.missed_english[3] = ["bed", "u"]
errors.missed_english[4] = ["but", "u"]
errors.missed_english[5] = ["dark", "u"]
errors.missed_english[6] = ["eggless", "kn"]
errors.missed_english[7] = ["gel", "u"]
errors.missed_english[8] = ["help", "u"]
errors.missed_english[9] = ["led", "u"]
errors.missed_english[10] = ["lens", "u"]
errors.missed_english[11] = ["limited", "u"]
errors.missed_english[12] = ["moisturize", "kn"]
errors.missed_english[13] = ["occasionaly", "kn"]
errors.missed_english[14] = ["on", "u"]
errors.missed_english[15] = ["post", "u"]
errors.missed_english[16] = ["purifiers", "kn"]
errors.missed_english[17] = ["sharp", "u"]
errors.missed_english[18] = ["skin", "u"]
errors.missed_english[19] = ["so", "u"]
errors.missed_english[20] = ["start", "u"]
errors.missed_english[21] = ["tuners", "kn"]
errors.hybrid_H = ["groupnalli", "jetsgalannu", "lensesgalige", "lensesgalu", "manufacturercellu", "pitchnalli", "productginta", "productionalli", "skinannu"]
`````

#### `results/codemix_check/check_sample0_v2.json` (2,702 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
provenance.config.gold = "gold_sample0.json"
provenance.git_commit = "46bd82a80ef6bf72fdc3187817de2e5a8dd24a87-dirty"
provenance.timestamp_utc = "2026-10-26T09:11:08+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/codemix_check.py", "0", "v2"]
seed = 0
tagger = "v2"
texts = 50
alphabetic_tokens = 883
tokens_tagged_en = 232
main (H not English).tp = 221
main (H not English).fp = 11
main (H not English).fn = 27
main (H not English).precision = 0.9525862068965517
main (H not English).recall = 0.8911290322580645
sensitivity (H English).tp = 221
sensitivity (H English).fp = 11
sensitivity (H English).fn = 36
sensitivity (H English).precision = 0.9525862068965517
sensitivity (H English).recall = 0.8599221789883269
errors.false_positive[0] = ["ana", "K"]
errors.false_positive[1] = ["andre", "K"]
errors.false_positive[2] = ["angola", "N"]
errors.false_positive[3] = ["bis", "N"]
errors.false_positive[4] = ["kami", "K"]
errors.false_positive[5] = ["luxembourg", "N"]
errors.false_positive[6] = ["pakistani", "N"]
errors.false_positive[7] = ["russian", "N"]
errors.false_positive[8] = ["stearns", "N"]
errors.missed_english[0] = ["carbon", "u"]
errors.missed_english[1] = ["commerce", "u"]
errors.missed_english[2] = ["committee", "u"]
errors.missed_english[3] = ["eggless", "kn"]
errors.missed_english[4] = ["energy", "u"]
errors.missed_english[5] = ["giant", "u"]
errors.missed_english[6] = ["house", "u"]
errors.missed_english[7] = ["investigations", "u"]
errors.missed_english[8] = ["lens", "kn"]
errors.missed_english[9] = ["museum", "u"]
errors.missed_english[10] = ["occasionaly", "kn"]
errors.missed_english[11] = ["oversight", "u"]
errors.missed_english[12] = ["parenthood", "u"]
errors.missed_english[13] = ["planned", "u"]
errors.missed_english[14] = ["purifiers", "kn"]
errors.missed_english[15] = ["slalom", "u"]
errors.missed_english[16] = ["split", "u"]
errors.missed_english[17] = ["street", "u"]
errors.missed_english[18] = ["subcommittee", "u"]
errors.missed_english[19] = ["tuners", "kn"]
errors.missed_english[20] = ["war", "u"]
errors.missed_english[21] = ["world", "u"]
errors.hybrid_H = ["groupnalli", "jetsgalannu", "lensesgalige", "lensesgalu", "manufacturercellu", "pitchnalli", "productginta", "productionalli", "skinannu"]
`````

#### `results/codemix_check/check_sample1_v1.json` (4,037 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
provenance.config.gold = "gold_sample1.json"
provenance.git_commit = "07ba540f5d484beeb92d283e5be387b748d48300-dirty"
provenance.timestamp_utc = "2026-10-26T06:36:29+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/codemix_check.py", "1", "v1"]
seed = 1
tagger = "v1"
texts = 50
alphabetic_tokens = 1004
tokens_tagged_en = 259
main (H not English).tp = 233
main (H not English).fp = 26
main (H not English).fn = 37
main (H not English).precision = 0.8996138996138996
main (H not English).recall = 0.8629629629629629
sensitivity (H English).tp = 233
sensitivity (H English).fp = 26
sensitivity (H English).fn = 53
sensitivity (H English).precision = 0.8996138996138996
sensitivity (H English).recall = 0.8146853146853147
errors.false_positive[0] = ["aa", "K"]
errors.false_positive[1] = ["america", "N"]
errors.false_positive[2] = ["asia", "N"]
errors.false_positive[3] = ["austrian", "N"]
errors.false_positive[4] = ["claudia", "N"]
errors.false_positive[5] = ["ebola", "N"]
errors.false_positive[6] = ["europe", "N"]
errors.false_positive[7] = ["fallujah", "N"]
errors.false_positive[8] = ["galapagos", "N"]
errors.false_positive[9] = ["germany", "N"]
errors.false_positive[10] = ["greek", "N"]
errors.false_positive[11] = ["gru", "N"]
errors.false_positive[12] = ["indian", "N"]
errors.false_positive[13] = ["iraq", "N"]
errors.false_positive[14] = ["istanbul", "N"]
errors.false_positive[15] = ["koo", "K"]
errors.false_positive[16] = ["minions", "N"]
errors.false_positive[17] = ["murray", "N"]
errors.false_positive[18] = ["nigeria", "N"]
errors.false_positive[19] = ["nim", "K"]
errors.false_positive[20] = ["olympics", "N"]
errors.false_positive[21] = ["pythagoras", "N"]
errors.false_positive[22] = ["shetland", "N"]
errors.false_positive[23] = ["vela", "K"]
errors.false_positive[24] = ["xian", "N"]
errors.missed_english[0] = ["ad", "u"]
errors.missed_english[1] = ["and", "u"]
errors.missed_english[2] = ["anti", "u"]
errors.missed_english[3] = ["bad", "u"]
errors.missed_english[4] = ["band", "u"]
errors.missed_english[5] = ["carrom", "kn"]
errors.missed_english[6] = ["cationic", "kn"]
errors.missed_english[7] = ["end", "u"]
errors.missed_english[8] = ["evaporator", "kn"]
errors.missed_english[9] = ["halo", "u"]
errors.missed_english[10] = ["hole", "u"]
errors.missed_english[11] = ["innings", "u"]
errors.missed_english[12] = ["is", "u"]
errors.missed_english[13] = ["it", "u"]
errors.missed_english[14] = ["janisary", "kn"]
errors.missed_english[15] = ["level", "u"]
errors.missed_english[16] = ["on", "u"]
errors.missed_english[17] = ["order", "u"]
errors.missed_english[18] = ["post", "u"]
errors.missed_english[19] = ["radar", "u"]
errors.missed_english[20] = ["rate", "u"]
errors.missed_english[21] = ["red", "u"]
errors.missed_english[22] = ["skin", "u"]
errors.missed_english[23] = ["so", "u"]
errors.missed_english[24] = ["star", "u"]
errors.missed_english[25] = ["stars", "u"]
errors.missed_english[26] = ["start", "u"]
errors.missed_english[27] = ["target", "u"]
errors.missed_english[28] = ["tennis", "u"]
errors.missed_english[29] = ["tie", "u"]
errors.missed_english[30] = ["visa", "u"]
errors.hybrid_H = ["breaknalli", "cholesterolge", "effectsnalli", "groupnalli", "heightnalli", "hotelgala", "matchgalu", "poundsginta", "servgalannu", "setannu", "setnalli", "speedalli", "submarinegalu", "surfaceginta", "teamgalu", "weekendalli"]
`````

#### `results/codemix_check/check_sample1_v2.json` (2,803 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
provenance.config.gold = "gold_sample1.json"
provenance.git_commit = "46bd82a80ef6bf72fdc3187817de2e5a8dd24a87-dirty"
provenance.timestamp_utc = "2026-10-26T09:11:11+00:00"
provenance.python = "3.12.13"
provenance.platform = "Windows-11-10.0.26300-SP0"
provenance.argv = ["scripts/codemix_check.py", "1", "v2"]
seed = 1
tagger = "v2"
texts = 50
alphabetic_tokens = 1004
tokens_tagged_en = 271
main (H not English).tp = 254
main (H not English).fp = 17
main (H not English).fn = 16
main (H not English).precision = 0.9372693726937269
main (H not English).recall = 0.9407407407407408
sensitivity (H English).tp = 254
sensitivity (H English).fp = 17
sensitivity (H English).fn = 32
sensitivity (H English).precision = 0.9372693726937269
sensitivity (H English).recall = 0.8881118881118881
errors.false_positive[0] = ["aa", "K"]
errors.false_positive[1] = ["america", "N"]
errors.false_positive[2] = ["andre", "K"]
errors.false_positive[3] = ["anna", "K"]
errors.false_positive[4] = ["asia", "N"]
errors.false_positive[5] = ["europe", "N"]
errors.false_positive[6] = ["germany", "N"]
errors.false_positive[7] = ["iraq", "N"]
errors.false_positive[8] = ["koo", "K"]
errors.false_positive[9] = ["minions", "N"]
errors.false_positive[10] = ["murray", "N"]
errors.false_positive[11] = ["nim", "K"]
errors.false_positive[12] = ["tokyo", "N"]
errors.false_positive[13] = ["vela", "K"]
errors.false_positive[14] = ["xian", "N"]
errors.missed_english[0] = ["brakes", "u"]
errors.missed_english[1] = ["brother", "u"]
errors.missed_english[2] = ["carrom", "kn"]
errors.missed_english[3] = ["cationic", "u"]
errors.missed_english[4] = ["evaporator", "kn"]
errors.missed_english[5] = ["giant", "u"]
errors.missed_english[6] = ["ions", "u"]
errors.missed_english[7] = ["janisary", "kn"]
errors.missed_english[8] = ["orchestra", "u"]
errors.missed_english[9] = ["silver", "u"]
errors.missed_english[10] = ["slalom", "u"]
errors.missed_english[11] = ["state", "u"]
errors.missed_english[12] = ["symphony", "u"]
errors.missed_english[13] = ["tennis", "kn"]
errors.missed_english[14] = ["twin", "u"]
errors.missed_english[15] = ["villainy", "u"]
errors.hybrid_H = ["breaknalli", "cholesterolge", "effectsnalli", "groupnalli", "heightnalli", "hotelgala", "matchgalu", "poundsginta", "servgalannu", "setannu", "setnalli", "speedalli", "submarinegalu", "surfaceginta", "teamgalu", "weekendalli"]
`````

#### `results/codemix_check/gold_sample0.json` (1,494 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
_about = "Claude Code's marking (2026-10-26) of the token types in the 50 kanglish_verified texts sampled with default_rng(0) (results/codemix_check/sample_tokens.json). Gold labels: E English word; K Kannada (incl. Kannada written with an English-looking spelling); N proper name, name-derived adjective, acronym name or unit (neither language); H English stem + Kannada suffix written as one word. Types not listed take the gold label implied by the codemix v1 tag after review: en -> E, kn -> K, u -> K. Marked with the item contexts in view."
overrides.amsterdam = "N"
overrides.angola = "N"
overrides.claudia = "N"
overrides.germany = "N"
overrides.iceland = "N"
overrides.luxembourg = "N"
overrides.machu = "N"
overrides.stearns = "N"
overrides.frank = "N"
overrides.bis = "N"
overrides.austrian = "N"
overrides.russian = "N"
overrides.african = "N"
overrides.mediterranean = "N"
overrides.kami = "K"
overrides.ad = "E"
overrides.air = "E"
overrides.and = "E"
overrides.bed = "E"
overrides.but = "E"
overrides.dark = "E"
overrides.gel = "E"
overrides.help = "E"
overrides.led = "E"
overrides.lens = "E"
overrides.limited = "E"
overrides.on = "E"
overrides.post = "E"
overrides.sharp = "E"
overrides.skin = "E"
overrides.so = "E"
overrides.start = "E"
overrides.anne = "N"
overrides.richard = "N"
overrides.park = "N"
overrides.sans = "N"
overrides.pakistani = "N"
overrides.eggless = "E"
overrides.moisturize = "E"
overrides.purifiers = "E"
overrides.tuners = "E"
overrides.occasionaly = "E"
overrides.veermen = "N"
overrides.mbit = "N"
overrides.italiya = "N"
overrides.hungaryya = "N"
overrides.africavannu = "N"
overrides.kolkattada = "N"
overrides.groupnalli = "H"
overrides.lensesgalige = "H"
overrides.lensesgalu = "H"
overrides.manufacturercellu = "H"
overrides.pitchnalli = "H"
overrides.productginta = "H"
overrides.productionalli = "H"
overrides.skinannu = "H"
overrides.jetsgalannu = "H"
`````

#### `results/codemix_check/gold_sample1.json` (1,825 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
_about = "Claude Code's marking (2026-10-26) of the token types in the 50 kanglish_verified texts sampled with default_rng(1), done from the codemix v1 view and the item contexts BEFORE any v2 tag of this sample was seen. Labels as gold_sample0.json (E English; K Kannada; N name/brand/unit/single letter used as a symbol; H English stem + Kannada suffix). Types not listed take the label implied by their v1 tag: en -> E, kn -> K, u -> K."
overrides.america = "N"
overrides.asia = "N"
overrides.claudia = "N"
overrides.europe = "N"
overrides.fallujah = "N"
overrides.galapagos = "N"
overrides.germany = "N"
overrides.iraq = "N"
overrides.istanbul = "N"
overrides.murray = "N"
overrides.nigeria = "N"
overrides.pythagoras = "N"
overrides.shetland = "N"
overrides.xian = "N"
overrides.ebola = "N"
overrides.olympics = "N"
overrides.minions = "N"
overrides.gru = "N"
overrides.austrian = "N"
overrides.greek = "N"
overrides.indian = "N"
overrides.aa = "K"
overrides.koo = "K"
overrides.nim = "K"
overrides.vela = "K"
overrides.ad = "E"
overrides.and = "E"
overrides.anti = "E"
overrides.bad = "E"
overrides.band = "E"
overrides.end = "E"
overrides.hole = "E"
overrides.innings = "E"
overrides.is = "E"
overrides.it = "E"
overrides.level = "E"
overrides.on = "E"
overrides.order = "E"
overrides.post = "E"
overrides.radar = "E"
overrides.rate = "E"
overrides.red = "E"
overrides.skin = "E"
overrides.so = "E"
overrides.star = "E"
overrides.stars = "E"
overrides.start = "E"
overrides.target = "E"
overrides.tennis = "E"
overrides.tie = "E"
overrides.visa = "E"
overrides.halo = "E"
overrides.china = "N"
overrides.tokyo = "N"
overrides.muslim = "N"
overrides.u = "N"
overrides.v = "N"
overrides.carrom = "E"
overrides.cationic = "E"
overrides.evaporator = "E"
overrides.janisary = "E"
overrides.godrej = "N"
overrides.fatih = "N"
overrides.irkutsk = "N"
overrides.erkos = "N"
overrides.gorses = "N"
overrides.agnps = "N"
overrides.zmapp = "N"
overrides.swiggy = "N"
overrides.votiervina = "N"
overrides.noosa = "N"
overrides.hungaryya = "N"
overrides.breaknalli = "H"
overrides.cholesterolge = "H"
overrides.effectsnalli = "H"
overrides.groupnalli = "H"
overrides.heightnalli = "H"
overrides.hotelgala = "H"
overrides.matchgalu = "H"
overrides.poundsginta = "H"
overrides.servgalannu = "H"
overrides.setannu = "H"
overrides.setnalli = "H"
overrides.speedalli = "H"
overrides.submarinegalu = "H"
overrides.surfaceginta = "H"
overrides.teamgalu = "H"
overrides.weekendalli = "H"
`````

#### `results/codemix_check/out_0_v1.txt` (2,127 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
warning: in the working copy of 'RESULTS.md', LF will be replaced by CRLF the next time Git touches it
{
 "seed": 0,
 "tagger": "v1",
 "texts": 50,
 "alphabetic_tokens": 883,
 "tokens_tagged_en": 236,
 "main (H not English)": {
  "tp": 219,
  "fp": 17,
  "fn": 29,
  "precision": 0.9279661016949152,
  "recall": 0.8830645161290323
 },
 "sensitivity (H English)": {
  "tp": 219,
  "fp": 17,
  "fn": 38,
  "precision": 0.9279661016949152,
  "recall": 0.8521400778210116
 },
 "errors": {
  "false_positive": [
   [
    "african",
    "N"
   ],
   [
    "amsterdam",
    "N"
   ],
   [
    "angola",
    "N"
   ],
   [
    "austrian",
    "N"
   ],
   [
    "bis",
    "N"
   ],
   [
    "claudia",
    "N"
   ],
   [
    "frank",
    "N"
   ],
   [
    "germany",
    "N"
   ],
   [
    "iceland",
    "N"
   ],
   [
    "kami",
    "K"
   ],
   [
    "luxembourg",
    "N"
   ],
   [
    "machu",
    "N"
   ],
   [
    "mediterranean",
    "N"
   ],
   [
    "russian",
    "N"
   ],
   [
    "stearns",
    "N"
   ]
  ],
  "missed_english": [
   [
    "ad",
    "u"
   ],
   [
    "air",
    "u"
   ],
   [
    "and",
    "u"
   ],
   [
    "bed",
    "u"
   ],
   [
    "but",
    "u"
   ],
   [
    "dark",
    "u"
   ],
   [
    "eggless",
    "kn"
   ],
   [
    "gel",
    "u"
   ],
   [
    "help",
    "u"
   ],
   [
    "led",
    "u"
   ],
   [
    "lens",
    "u"
   ],
   [
    "limited",
    "u"
   ],
   [
    "moisturize",
    "kn"
   ],
   [
    "occasionaly",
    "kn"
   ],
   [
    "on",
    "u"
   ],
   [
    "post",
    "u"
   ],
   [
    "purifiers",
    "kn"
   ],
   [
    "sharp",
    "u"
   ],
   [
    "skin",
    "u"
   ],
   [
    "so",
    "u"
   ],
   [
    "start",
    "u"
   ],
   [
    "tuners",
    "kn"
   ]
  ],
  "hybrid_H": [
   "groupnalli",
   "jetsgalannu",
   "lensesgalige",
   "lensesgalu",
   "manufacturercellu",
   "pitchnalli",
   "productginta",
   "productionalli",
   "skinannu"
  ]
 }
}
`````

#### `results/codemix_check/out_0_v2.txt` (1,842 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
{
 "seed": 0,
 "tagger": "v2",
 "texts": 50,
 "alphabetic_tokens": 883,
 "tokens_tagged_en": 232,
 "main (H not English)": {
  "tp": 221,
  "fp": 11,
  "fn": 27,
  "precision": 0.9525862068965517,
  "recall": 0.8911290322580645
 },
 "sensitivity (H English)": {
  "tp": 221,
  "fp": 11,
  "fn": 36,
  "precision": 0.9525862068965517,
  "recall": 0.8599221789883269
 },
 "errors": {
  "false_positive": [
   [
    "ana",
    "K"
   ],
   [
    "andre",
    "K"
   ],
   [
    "angola",
    "N"
   ],
   [
    "bis",
    "N"
   ],
   [
    "kami",
    "K"
   ],
   [
    "luxembourg",
    "N"
   ],
   [
    "pakistani",
    "N"
   ],
   [
    "russian",
    "N"
   ],
   [
    "stearns",
    "N"
   ]
  ],
  "missed_english": [
   [
    "carbon",
    "u"
   ],
   [
    "commerce",
    "u"
   ],
   [
    "committee",
    "u"
   ],
   [
    "eggless",
    "kn"
   ],
   [
    "energy",
    "u"
   ],
   [
    "giant",
    "u"
   ],
   [
    "house",
    "u"
   ],
   [
    "investigations",
    "u"
   ],
   [
    "lens",
    "kn"
   ],
   [
    "museum",
    "u"
   ],
   [
    "occasionaly",
    "kn"
   ],
   [
    "oversight",
    "u"
   ],
   [
    "parenthood",
    "u"
   ],
   [
    "planned",
    "u"
   ],
   [
    "purifiers",
    "kn"
   ],
   [
    "slalom",
    "u"
   ],
   [
    "split",
    "u"
   ],
   [
    "street",
    "u"
   ],
   [
    "subcommittee",
    "u"
   ],
   [
    "tuners",
    "kn"
   ],
   [
    "war",
    "u"
   ],
   [
    "world",
    "u"
   ]
  ],
  "hybrid_H": [
   "groupnalli",
   "jetsgalannu",
   "lensesgalige",
   "lensesgalu",
   "manufacturercellu",
   "pitchnalli",
   "productginta",
   "productionalli",
   "skinannu"
  ]
 }
}
`````

#### `results/codemix_check/out_1_v1.txt` (2,909 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
warning: in the working copy of 'RESULTS.md', LF will be replaced by CRLF the next time Git touches it
{
 "seed": 1,
 "tagger": "v1",
 "texts": 50,
 "alphabetic_tokens": 1004,
 "tokens_tagged_en": 259,
 "main (H not English)": {
  "tp": 233,
  "fp": 26,
  "fn": 37,
  "precision": 0.8996138996138996,
  "recall": 0.8629629629629629
 },
 "sensitivity (H English)": {
  "tp": 233,
  "fp": 26,
  "fn": 53,
  "precision": 0.8996138996138996,
  "recall": 0.8146853146853147
 },
 "errors": {
  "false_positive": [
   [
    "aa",
    "K"
   ],
   [
    "america",
    "N"
   ],
   [
    "asia",
    "N"
   ],
   [
    "austrian",
    "N"
   ],
   [
    "claudia",
    "N"
   ],
   [
    "ebola",
    "N"
   ],
   [
    "europe",
    "N"
   ],
   [
    "fallujah",
    "N"
   ],
   [
    "galapagos",
    "N"
   ],
   [
    "germany",
    "N"
   ],
   [
    "greek",
    "N"
   ],
   [
    "gru",
    "N"
   ],
   [
    "indian",
    "N"
   ],
   [
    "iraq",
    "N"
   ],
   [
    "istanbul",
    "N"
   ],
   [
    "koo",
    "K"
   ],
   [
    "minions",
    "N"
   ],
   [
    "murray",
    "N"
   ],
   [
    "nigeria",
    "N"
   ],
   [
    "nim",
    "K"
   ],
   [
    "olympics",
    "N"
   ],
   [
    "pythagoras",
    "N"
   ],
   [
    "shetland",
    "N"
   ],
   [
    "vela",
    "K"
   ],
   [
    "xian",
    "N"
   ]
  ],
  "missed_english": [
   [
    "ad",
    "u"
   ],
   [
    "and",
    "u"
   ],
   [
    "anti",
    "u"
   ],
   [
    "bad",
    "u"
   ],
   [
    "band",
    "u"
   ],
   [
    "carrom",
    "kn"
   ],
   [
    "cationic",
    "kn"
   ],
   [
    "end",
    "u"
   ],
   [
    "evaporator",
    "kn"
   ],
   [
    "halo",
    "u"
   ],
   [
    "hole",
    "u"
   ],
   [
    "innings",
    "u"
   ],
   [
    "is",
    "u"
   ],
   [
    "it",
    "u"
   ],
   [
    "janisary",
    "kn"
   ],
   [
    "level",
    "u"
   ],
   [
    "on",
    "u"
   ],
   [
    "order",
    "u"
   ],
   [
    "post",
    "u"
   ],
   [
    "radar",
    "u"
   ],
   [
    "rate",
    "u"
   ],
   [
    "red",
    "u"
   ],
   [
    "skin",
    "u"
   ],
   [
    "so",
    "u"
   ],
   [
    "star",
    "u"
   ],
   [
    "stars",
    "u"
   ],
   [
    "start",
    "u"
   ],
   [
    "target",
    "u"
   ],
   [
    "tennis",
    "u"
   ],
   [
    "tie",
    "u"
   ],
   [
    "visa",
    "u"
   ]
  ],
  "hybrid_H": [
   "breaknalli",
   "cholesterolge",
   "effectsnalli",
   "groupnalli",
   "heightnalli",
   "hotelgala",
   "matchgalu",
   "poundsginta",
   "servgalannu",
   "setannu",
   "setnalli",
   "speedalli",
   "submarinegalu",
   "surfaceginta",
   "teamgalu",
   "weekendalli"
  ]
 }
}
`````

#### `results/codemix_check/out_1_v2.txt` (1,922 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
{
 "seed": 1,
 "tagger": "v2",
 "texts": 50,
 "alphabetic_tokens": 1004,
 "tokens_tagged_en": 271,
 "main (H not English)": {
  "tp": 254,
  "fp": 17,
  "fn": 16,
  "precision": 0.9372693726937269,
  "recall": 0.9407407407407408
 },
 "sensitivity (H English)": {
  "tp": 254,
  "fp": 17,
  "fn": 32,
  "precision": 0.9372693726937269,
  "recall": 0.8881118881118881
 },
 "errors": {
  "false_positive": [
   [
    "aa",
    "K"
   ],
   [
    "america",
    "N"
   ],
   [
    "andre",
    "K"
   ],
   [
    "anna",
    "K"
   ],
   [
    "asia",
    "N"
   ],
   [
    "europe",
    "N"
   ],
   [
    "germany",
    "N"
   ],
   [
    "iraq",
    "N"
   ],
   [
    "koo",
    "K"
   ],
   [
    "minions",
    "N"
   ],
   [
    "murray",
    "N"
   ],
   [
    "nim",
    "K"
   ],
   [
    "tokyo",
    "N"
   ],
   [
    "vela",
    "K"
   ],
   [
    "xian",
    "N"
   ]
  ],
  "missed_english": [
   [
    "brakes",
    "u"
   ],
   [
    "brother",
    "u"
   ],
   [
    "carrom",
    "kn"
   ],
   [
    "cationic",
    "u"
   ],
   [
    "evaporator",
    "kn"
   ],
   [
    "giant",
    "u"
   ],
   [
    "ions",
    "u"
   ],
   [
    "janisary",
    "kn"
   ],
   [
    "orchestra",
    "u"
   ],
   [
    "silver",
    "u"
   ],
   [
    "slalom",
    "u"
   ],
   [
    "state",
    "u"
   ],
   [
    "symphony",
    "u"
   ],
   [
    "tennis",
    "kn"
   ],
   [
    "twin",
    "u"
   ],
   [
    "villainy",
    "u"
   ]
  ],
  "hybrid_H": [
   "breaknalli",
   "cholesterolge",
   "effectsnalli",
   "groupnalli",
   "heightnalli",
   "hotelgala",
   "matchgalu",
   "poundsginta",
   "servgalannu",
   "setannu",
   "setnalli",
   "speedalli",
   "submarinegalu",
   "surfaceginta",
   "teamgalu",
   "weekendalli"
  ]
 }
}
`````

#### `results/codemix_check/sample_tokens.json` (65,582 bytes; first commit 46bd82a 2026-10-26 12:10:58 +0530)

`````text
seed = 0
items = ["indicsentiment-test-249", "indicsentiment-test-581", "indicsentiment-test-660", "indicsentiment-test-234", "indicsentiment-test-540", "indicsentiment-test-913", "indicsentiment-test-727", "indicsentiment-test-283", "indicsentiment-test-792", "indicsentiment-test-87", "indicsentiment-test-555", "indicsentiment-test-67", "indicsentiment-test-207", "indicsentiment-test-520", "indicsentiment-test-724", "indicsentiment-test-239", "indicsentiment-test-887", "indicsentiment-test-277", "indicsentiment-test-826", "indicsentiment-test-744", "indicsentiment-test-516", "flores-18", "flores-259", "flores-266", "flores-276", "flores-398", "flores-434", "flores-455", "flores-456", "flores-458", "flores-560", "flores-602", "flores-678", "flores-706", "flores-764", "flores-811", "flores-822", "flores-856", "flores-879", "flores-983", "flores-1040", "flores-1095", "flores-1148", "flores-1153", "flores-1272", "flores-1279", "flores-1335", "flores-1357", "flores-1522", "flores-1651"]
tokens[0].item_id = "indicsentiment-test-249"
tokens[0].token = "Kolkattada"
tokens[0].tag = "kn"
tokens[1].item_id = "indicsentiment-test-249"
tokens[1].token = "Park"
tokens[1].tag = "u"
tokens[2].item_id = "indicsentiment-test-249"
tokens[2].token = "Street"
tokens[2].tag = "en"
tokens[3].item_id = "indicsentiment-test-249"
tokens[3].token = "nalliro"
tokens[3].tag = "kn"
tokens[4].item_id = "indicsentiment-test-249"
tokens[4].token = "ee"
tokens[4].tag = "u"
tokens[5].item_id = "indicsentiment-test-249"
tokens[5].token = "place"
tokens[5].tag = "en"
tokens[6].item_id = "indicsentiment-test-249"
tokens[6].token = "tumba"
tokens[6].tag = "kn"
tokens[7].item_id = "indicsentiment-test-249"
tokens[7].token = "attractive"
tokens[7].tag = "en"
tokens[8].item_id = "indicsentiment-test-249"
tokens[8].token = "clean"
tokens[8].tag = "en"
tokens[9].item_id = "indicsentiment-test-249"
tokens[9].token = "pocket"
tokens[9].tag = "en"
tokens[10].item_id = "indicsentiment-test-249"
tokens[10].token = "friendly"
tokens[10].tag = "en"
tokens[11].item_id = "indicsentiment-test-249"
tokens[11].token = "mattu"
tokens[11].tag = "kn"
tokens[12].item_id = "indicsentiment-test-249"
tokens[12].token = "women"
tokens[12].tag = "en"
tokens[13].item_id = "indicsentiment-test-249"
tokens[13].token = "ge"
tokens[13].tag = "u"
tokens[14].item_id = "indicsentiment-test-249"
tokens[14].token = "safe"
tokens[14].tag = "en"
tokens[15].item_id = "indicsentiment-test-249"
tokens[15].token = "Rooms"
tokens[15].tag = "en"
tokens[16].item_id = "indicsentiment-test-249"
tokens[16].token = "alli"
tokens[16].tag = "u"
tokens[17].item_id = "indicsentiment-test-249"
tokens[17].token = "bunk"
tokens[17].tag = "en"
tokens[18].item_id = "indicsentiment-test-249"
tokens[18].token = "bed"
tokens[18].tag = "u"
tokens[19].item_id = "indicsentiment-test-249"
tokens[19].token = "accommodation"
tokens[19].tag = "en"
tokens[20].item_id = "indicsentiment-test-249"
tokens[20].token = "matra"
tokens[20].tag = "kn"
tokens[21].item_id = "indicsentiment-test-249"
tokens[21].token = "ide"
tokens[21].tag = "u"
tokens[22].item_id = "indicsentiment-test-249"
tokens[22].token = "Breakfast"
tokens[22].tag = "en"
tokens[23].item_id = "indicsentiment-test-249"
tokens[23].token = "fantastic"
tokens[23].tag = "en"
tokens[24].item_id = "indicsentiment-test-249"
tokens[24].token = "fast"
tokens[24].tag = "en"
tokens[25].item_id = "indicsentiment-test-249"
tokens[25].token = "wifi"
tokens[25].tag = "en"
tokens[26].item_id = "indicsentiment-test-249"
tokens[26].token = "ide"
tokens[26].tag = "u"
tokens[27].item_id = "indicsentiment-test-249"
tokens[27].token = "mattu"
tokens[27].tag = "kn"
tokens[28].item_id = "indicsentiment-test-249"
tokens[28].token = "AC"
tokens[28].tag = "en"
tokens[29].item_id = "indicsentiment-test-249"
tokens[29].token = "non"
tokens[29].tag = "en"
tokens[30].item_id = "indicsentiment-test-249"
tokens[30].token = "AC"
tokens[30].tag = "en"
tokens[31].item_id = "indicsentiment-test-249"
tokens[31].token = "rooms"
tokens[31].tag = "en"
tokens[32].item_id = "indicsentiment-test-249"
tokens[32].token = "online"
tokens[32].tag = "en"
tokens[33].item_id = "indicsentiment-test-249"
tokens[33].token = "athava"
tokens[33].tag = "kn"
tokens[34].item_id = "indicsentiment-test-249"
tokens[34].token = "on"
tokens[34].tag = "u"
tokens[35].item_id = "indicsentiment-test-249"
tokens[35].token = "spot"
tokens[35].tag = "en"
tokens[36].item_id = "indicsentiment-test-249"
tokens[36].token = "booking"
tokens[36].tag = "en"
tokens[37].item_id = "indicsentiment-test-249"
tokens[37].token = "moolaka"
tokens[37].tag = "kn"
tokens[38].item_id = "indicsentiment-test-249"
tokens[38].token = "sigutte"
tokens[38].tag = "kn"
tokens[39].item_id = "indicsentiment-test-581"
tokens[39].token = "Neevu"
tokens[39].tag = "kn"
tokens[40].item_id = "indicsentiment-test-581"
tokens[40].token = "TV"
tokens[40].tag = "en"
tokens[41].item_id = "indicsentiment-test-581"
tokens[41].token = "show"
tokens[41].tag = "en"
tokens[42].item_id = "indicsentiment-test-581"
tokens[42].token = "play"
tokens[42].tag = "en"
tokens[43].item_id = "indicsentiment-test-581"
tokens[43].token = "madoke"
tokens[43].tag = "kn"
tokens[44].item_id = "indicsentiment-test-581"
tokens[44].token = "try"
tokens[44].tag = "en"
tokens[45].item_id = "indicsentiment-test-581"
tokens[45].token = "madidaga"
tokens[45].tag = "kn"
tokens[46].item_id = "indicsentiment-test-581"
tokens[46].token = "tumba"
tokens[46].tag = "kn"
tokens[47].item_id = "indicsentiment-test-581"
tokens[47].token = "ads"
tokens[47].tag = "en"
tokens[48].item_id = "indicsentiment-test-581"
tokens[48].token = "barutte"
tokens[48].tag = "kn"
tokens[49].item_id = "indicsentiment-test-581"
tokens[49].token = "mattu"
tokens[49].tag = "kn"
tokens[50].item_id = "indicsentiment-test-581"
tokens[50].token = "tumba"
tokens[50].tag = "kn"
tokens[51].item_id = "indicsentiment-test-581"
tokens[51].token = "sala"
tokens[51].tag = "u"
tokens[52].item_id = "indicsentiment-test-581"
tokens[52].token = "oops"
tokens[52].tag = "en"
tokens[53].item_id = "indicsentiment-test-581"
tokens[53].token = "eno"
tokens[53].tag = "u"
tokens[54].item_id = "indicsentiment-test-581"
tokens[54].token = "tappagide"
tokens[54].tag = "kn"
tokens[55].item_id = "indicsentiment-test-581"
tokens[55].token = "error"
tokens[55].tag = "en"
tokens[56].item_id = "indicsentiment-test-581"
tokens[56].token = "torisutte"
tokens[56].tag = "kn"
tokens[57].item_id = "indicsentiment-test-581"
tokens[57].token = "Halavu"
tokens[57].tag = "kn"
tokens[58].item_id = "indicsentiment-test-581"
tokens[58].token = "sala"
tokens[58].tag = "u"
tokens[59].item_id = "indicsentiment-test-581"
tokens[59].token = "report"
tokens[59].tag = "en"
tokens[60].item_id = "indicsentiment-test-581"
tokens[60].token = "madidru"
tokens[60].tag = "kn"
tokens[61].item_id = "indicsentiment-test-581"
tokens[61].token = "backend"
tokens[61].tag = "en"
tokens[62].item_id = "indicsentiment-test-581"
tokens[62].token = "code"
tokens[62].tag = "en"
tokens[63].item_id = "indicsentiment-test-581"
tokens[63].token = "nalli"
tokens[63].tag = "kn"
tokens[64].item_id = "indicsentiment-test-581"
tokens[64].token = "error"
tokens[64].tag = "en"
tokens[65].item_id = "indicsentiment-test-581"
tokens[65].token = "fix"
tokens[65].tag = "en"
tokens[66].item_id = "indicsentiment-test-581"
tokens[66].token = "madilla"
tokens[66].tag = "kn"
tokens[67].item_id = "indicsentiment-test-660"
tokens[67].token = "Kelvu"
tokens[67].tag = "kn"
tokens[68].item_id = "indicsentiment-test-660"
tokens[68].token = "niroopakarige"
tokens[68].tag = "kn"
tokens[69].item_id = "indicsentiment-test-660"
tokens[69].token = "bahala"
tokens[69].tag = "kn"
tokens[70].item_id = "indicsentiment-test-660"
tokens[70].token = "ekatanate"
tokens[70].tag = "kn"
tokens[71].item_id = "indicsentiment-test-660"
tokens[71].token = "Avaru"
tokens[71].tag = "kn"
tokens[72].item_id = "indicsentiment-test-660"
tokens[72].token = "adhe"
tokens[72].tag = "kn"
tokens[73].item_id = "indicsentiment-test-660"
tokens[73].token = "pitchnalli"
tokens[73].tag = "kn"
tokens[74].item_id = "indicsentiment-test-660"
tokens[74].token = "vishayavannu"
tokens[74].tag = "kn"
tokens[75].item_id = "indicsentiment-test-660"
tokens[75].token = "vivarisuttare"
tokens[75].tag = "kn"
tokens[76].item_id = "indicsentiment-test-660"
tokens[76].token = "idu"
tokens[76].tag = "kn"
tokens[77].item_id = "indicsentiment-test-660"
tokens[77].token = "pustakagalannu"
tokens[77].tag = "kn"
tokens[78].item_id = "indicsentiment-test-660"
tokens[78].token = "kelvomme"
tokens[78].tag = "kn"
tokens[79].item_id = "indicsentiment-test-660"
tokens[79].token = "neerasagolisuttade"
tokens[79].tag = "kn"
tokens[80].item_id = "indicsentiment-test-234"
tokens[80].token = "Professionals"
tokens[80].tag = "en"
tokens[81].item_id = "indicsentiment-test-234"
tokens[81].token = "ge"
tokens[81].tag = "u"
tokens[82].item_id = "indicsentiment-test-234"
tokens[82].token = "suitable"
tokens[82].tag = "en"
tokens[83].item_id = "indicsentiment-test-234"
tokens[83].token = "alla"
tokens[83].tag = "u"
tokens[84].item_id = "indicsentiment-test-234"
tokens[84].token = "LED"
tokens[84].tag = "u"
tokens[85].item_id = "indicsentiment-test-234"
tokens[85].token = "lights"
tokens[85].tag = "en"
tokens[86].item_id = "indicsentiment-test-234"
tokens[86].token = "ashtu"
tokens[86].tag = "kn"
tokens[87].item_id = "indicsentiment-test-234"
tokens[87].token = "intense"
tokens[87].tag = "en"
tokens[88].item_id = "indicsentiment-test-234"
tokens[88].token = "agilla"
tokens[88].tag = "kn"
tokens[89].item_id = "indicsentiment-test-234"
tokens[89].token = "so"
tokens[89].tag = "u"
tokens[90].item_id = "indicsentiment-test-234"
tokens[90].token = "nimma"
tokens[90].tag = "kn"
tokens[91].item_id = "indicsentiment-test-234"
tokens[91].token = "personal"
tokens[91].tag = "en"
tokens[92].item_id = "indicsentiment-test-234"
tokens[92].token = "lights"
tokens[92].tag = "en"
tokens[93].item_id = "indicsentiment-test-234"
tokens[93].token = "use"
tokens[93].tag = "en"
tokens[94].item_id = "indicsentiment-test-234"
tokens[94].token = "madodu"
tokens[94].tag = "kn"
tokens[95].item_id = "indicsentiment-test-234"
tokens[95].token = "better"
tokens[95].tag = "en"
tokens[96].item_id = "indicsentiment-test-540"
tokens[96].token = "Bridge"
tokens[96].tag = "en"
tokens[97].item_id = "indicsentiment-test-540"
tokens[97].token = "horabanditu"
tokens[97].tag = "kn"
tokens[98].item_id = "indicsentiment-test-540"
tokens[98].token = "mattu"
tokens[98].tag = "kn"
tokens[99].item_id = "indicsentiment-test-540"
tokens[99].token = "tuners"
tokens[99].tag = "kn"
tokens[100].item_id = "indicsentiment-test-540"
tokens[100].token = "ondu"
tokens[100].tag = "kn"
tokens[101].item_id = "indicsentiment-test-540"
tokens[101].token = "mahina"
tokens[101].tag = "kn"
tokens[102].item_id = "indicsentiment-test-540"
tokens[102].token = "athava"
tokens[102].tag = "kn"
tokens[103].item_id = "indicsentiment-test-540"
tokens[103].token = "athinta"
tokens[103].tag = "kn"
tokens[104].item_id = "indicsentiment-test-540"
tokens[104].token = "hechchina"
tokens[104].tag = "kn"
tokens[105].item_id = "indicsentiment-test-540"
tokens[105].token = "avadhiyalli"
tokens[105].tag = "kn"
tokens[106].item_id = "indicsentiment-test-540"
tokens[106].token = "fiddle"
tokens[106].tag = "en"
tokens[107].item_id = "indicsentiment-test-540"
tokens[107].token = "start"
tokens[107].tag = "u"
tokens[108].item_id = "indicsentiment-test-540"
tokens[108].token = "madthare"
tokens[108].tag = "kn"
tokens[109].item_id = "indicsentiment-test-913"
tokens[109].token = "Plot"
tokens[109].tag = "en"
tokens[110].item_id = "indicsentiment-test-913"
tokens[110].token = "ashtu"
tokens[110].tag = "kn"
tokens[111].item_id = "indicsentiment-test-913"
tokens[111].token = "clear"
tokens[111].tag = "en"
tokens[112].item_id = "indicsentiment-test-913"
tokens[112].token = "irlilla"
tokens[112].tag = "kn"
tokens[113].item_id = "indicsentiment-test-913"
tokens[113].token = "acting"
tokens[113].tag = "en"
tokens[114].item_id = "indicsentiment-test-913"
tokens[114].token = "mediocre"
tokens[114].tag = "en"
tokens[115].item_id = "indicsentiment-test-913"
tokens[115].token = "agittu"
tokens[115].tag = "kn"
tokens[116].item_id = "indicsentiment-test-913"
tokens[116].token = "mattu"
tokens[116].tag = "kn"
tokens[117].item_id = "indicsentiment-test-913"
tokens[117].token = "story"
tokens[117].tag = "en"
tokens[118].item_id = "indicsentiment-test-913"
tokens[118].token = "ge"
tokens[118].tag = "u"
tokens[119].item_id = "indicsentiment-test-913"
tokens[119].token = "konegu"
tokens[119].tag = "kn"
tokens[120].item_id = "indicsentiment-test-913"
tokens[120].token = "yavude"
tokens[120].tag = "kn"
tokens[121].item_id = "indicsentiment-test-913"
tokens[121].token = "point"
tokens[121].tag = "en"
tokens[122].item_id = "indicsentiment-test-913"
tokens[122].token = "athava"
tokens[122].tag = "kn"
tokens[123].item_id = "indicsentiment-test-913"
tokens[123].token = "meaning"
tokens[123].tag = "en"
tokens[124].item_id = "indicsentiment-test-913"
tokens[124].token = "irlilla"
tokens[124].tag = "kn"
tokens[125].item_id = "indicsentiment-test-727"
tokens[125].token = "idu"
tokens[125].tag = "kn"
tokens[126].item_id = "indicsentiment-test-727"
tokens[126].token = "romba"
tokens[126].tag = "kn"
tokens[127].item_id = "indicsentiment-test-727"
tokens[127].token = "sharp"
tokens[127].tag = "u"
tokens[128].item_id = "indicsentiment-test-727"
tokens[128].token = "hagyu"
tokens[128].tag = "kn"
tokens[129].item_id = "indicsentiment-test-727"
tokens[129].token = "durable"
tokens[129].tag = "en"
tokens[130].item_id = "indicsentiment-test-727"
tokens[130].token = "agide"
tokens[130].tag = "kn"
tokens[131].item_id = "indicsentiment-test-727"
tokens[131].token = "motor"
tokens[131].tag = "en"
tokens[132].item_id = "indicsentiment-test-727"
tokens[132].token = "tumba"
tokens[132].tag = "kn"
tokens[133].item_id = "indicsentiment-test-727"
tokens[133].token = "kamma"
tokens[133].tag = "kn"
tokens[134].item_id = "indicsentiment-test-727"
tokens[134].token = "sound"
tokens[134].tag = "en"
tokens[135].item_id = "indicsentiment-test-727"
tokens[135].token = "mattu"
tokens[135].tag = "kn"
tokens[136].item_id = "indicsentiment-test-727"
tokens[136].token = "vibration"
tokens[136].tag = "en"
tokens[137].item_id = "indicsentiment-test-727"
tokens[137].token = "madutte"
tokens[137].tag = "kn"
tokens[138].item_id = "indicsentiment-test-283"
tokens[138].token = "Idu"
tokens[138].tag = "kn"
tokens[139].item_id = "indicsentiment-test-283"
tokens[139].token = "vastavikate"
tokens[139].tag = "kn"
tokens[140].item_id = "indicsentiment-test-283"
tokens[140].token = "mattu"
tokens[140].tag = "kn"
tokens[141].item_id = "indicsentiment-test-283"
tokens[141].token = "ativastavikavadadalli"
tokens[141].tag = "kn"
tokens[142].item_id = "indicsentiment-test-283"
tokens[142].token = "mulugiruva"
tokens[142].tag = "kn"
tokens[143].item_id = "indicsentiment-test-283"
tokens[143].token = "prayogatmakka"
tokens[143].tag = "kn"
tokens[144].item_id = "indicsentiment-test-283"
tokens[144].token = "dark"
tokens[144].tag = "u"
tokens[145].item_id = "indicsentiment-test-283"
tokens[145].token = "fable"
tokens[145].tag = "en"
tokens[146].item_id = "indicsentiment-test-283"
tokens[146].token = "agide"
tokens[146].tag = "kn"
tokens[147].item_id = "indicsentiment-test-283"
tokens[147].token = "Mattu"
tokens[147].tag = "kn"
tokens[148].item_id = "indicsentiment-test-283"
tokens[148].token = "ee"
tokens[148].tag = "u"
tokens[149].item_id = "indicsentiment-test-283"
tokens[149].token = "amshu"
tokens[149].tag = "kn"
tokens[150].item_id = "indicsentiment-test-283"
tokens[150].token = "idu"
tokens[150].tag = "kn"
tokens[151].item_id = "indicsentiment-test-283"
tokens[151].token = "anthaha"
tokens[151].tag = "kn"
tokens[152].item_id = "indicsentiment-test-283"
tokens[152].token = "vishistha"
tokens[152].tag = "kn"
tokens[153].item_id = "indicsentiment-test-283"
tokens[153].token = "chalanchitravannagi"
tokens[153].tag = "kn"
tokens[154].item_id = "indicsentiment-test-283"
tokens[154].token = "madutte"
tokens[154].tag = "kn"
tokens[155].item_id = "indicsentiment-test-792"
tokens[155].token = "Tumba"
tokens[155].tag = "kn"
tokens[156].item_id = "indicsentiment-test-792"
tokens[156].token = "olle"
tokens[156].tag = "kn"
tokens[157].item_id = "indicsentiment-test-792"
tokens[157].token = "activity"
tokens[157].tag = "en"
tokens[158].item_id = "indicsentiment-test-792"
tokens[158].token = "based"
tokens[158].tag = "en"
tokens[159].item_id = "indicsentiment-test-792"
tokens[159].token = "book"
tokens[159].tag = "en"
tokens[160].item_id = "indicsentiment-test-792"
tokens[160].token = "Colourful"
tokens[160].tag = "en"
tokens[161].item_id = "indicsentiment-test-792"
tokens[161].token = "mattu"
tokens[161].tag = "kn"
tokens[162].item_id = "indicsentiment-test-792"
tokens[162].token = "attractive"
tokens[162].tag = "en"
tokens[163].item_id = "indicsentiment-test-792"
tokens[163].token = "pictures"
tokens[163].tag = "en"
tokens[164].item_id = "indicsentiment-test-792"
tokens[164].token = "hagu"
tokens[164].tag = "kn"
tokens[165].item_id = "indicsentiment-test-792"
tokens[165].token = "writing"
tokens[165].tag = "en"
tokens[166].item_id = "indicsentiment-test-792"
tokens[166].token = "activities"
tokens[166].tag = "en"
tokens[167].item_id = "indicsentiment-test-792"
tokens[167].token = "jothe"
tokens[167].tag = "kn"
tokens[168].item_id = "indicsentiment-test-792"
tokens[168].token = "maguvina"
tokens[168].tag = "kn"
tokens[169].item_id = "indicsentiment-test-792"
tokens[169].token = "pre"
tokens[169].tag = "en"
tokens[170].item_id = "indicsentiment-test-792"
tokens[170].token = "writing"
tokens[170].tag = "en"
tokens[171].item_id = "indicsentiment-test-792"
tokens[171].token = "skills"
tokens[171].tag = "en"
tokens[172].item_id = "indicsentiment-test-792"
tokens[172].token = "strengthen"
tokens[172].tag = "en"
tokens[173].item_id = "indicsentiment-test-792"
tokens[173].token = "madoke"
tokens[173].tag = "kn"
tokens[174].item_id = "indicsentiment-test-792"
tokens[174].token = "bekada"
tokens[174].tag = "kn"
tokens[175].item_id = "indicsentiment-test-792"
tokens[175].token = "ellavoo"
tokens[175].tag = "kn"
tokens[176].item_id = "indicsentiment-test-792"
tokens[176].token = "idaralli"
tokens[176].tag = "kn"
tokens[177].item_id = "indicsentiment-test-792"
tokens[177].token = "ide"
tokens[177].tag = "u"
tokens[178].item_id = "indicsentiment-test-87"
tokens[178].token = "gel"
tokens[178].tag = "u"
tokens[179].item_id = "indicsentiment-test-87"
tokens[179].token = "chennagi"
tokens[179].tag = "kn"
tokens[180].item_id = "indicsentiment-test-87"
tokens[180].token = "norebarutte"
tokens[180].tag = "kn"
tokens[181].item_id = "indicsentiment-test-87"
tokens[181].token = "mattu"
tokens[181].tag = "kn"
tokens[182].item_id = "indicsentiment-test-87"
tokens[182].token = "luxurious"
tokens[182].tag = "en"
tokens[183].item_id = "indicsentiment-test-87"
tokens[183].token = "bullgalannu"
tokens[183].tag = "kn"
tokens[184].item_id = "indicsentiment-test-87"
tokens[184].token = "srishtisutte"
tokens[184].tag = "kn"
tokens[185].item_id = "indicsentiment-test-87"
tokens[185].token = "effectively"
tokens[185].tag = "en"
tokens[186].item_id = "indicsentiment-test-87"
tokens[186].token = "nimmma"
tokens[186].tag = "kn"
tokens[187].item_id = "indicsentiment-test-87"
tokens[187].token = "skinannu"
tokens[187].tag = "kn"
tokens[188].item_id = "indicsentiment-test-87"
tokens[188].token = "clean"
tokens[188].tag = "en"
tokens[189].item_id = "indicsentiment-test-87"
tokens[189].token = "madutte"
tokens[189].tag = "kn"
tokens[190].item_id = "indicsentiment-test-87"
tokens[190].token = "mattu"
tokens[190].tag = "kn"
tokens[191].item_id = "indicsentiment-test-87"
tokens[191].token = "moisturize"
tokens[191].tag = "kn"
tokens[192].item_id = "indicsentiment-test-87"
tokens[192].token = "madutte"
tokens[192].tag = "kn"
tokens[193].item_id = "indicsentiment-test-87"
tokens[193].token = "mattu"
tokens[193].tag = "kn"
tokens[194].item_id = "indicsentiment-test-87"
tokens[194].token = "nige"
tokens[194].tag = "kn"
tokens[195].item_id = "indicsentiment-test-87"
tokens[195].token = "ullasavannu"
tokens[195].tag = "kn"
tokens[196].item_id = "indicsentiment-test-87"
tokens[196].token = "needutte"
tokens[196].tag = "kn"
tokens[197].item_id = "indicsentiment-test-555"
tokens[197].token = "antharneermitha"
tokens[197].tag = "kn"
tokens[198].item_id = "indicsentiment-test-555"
tokens[198].token = "pathagalannu"
tokens[198].tag = "kn"
tokens[199].item_id = "indicsentiment-test-555"
tokens[199].token = "olagondanthe"
tokens[199].tag = "kn"
tokens[200].item_id = "indicsentiment-test-555"
tokens[200].token = "halavaru"
tokens[200].tag = "kn"
tokens[201].item_id = "indicsentiment-test-555"
tokens[201].token = "reethiya"
tokens[201].tag = "kn"
tokens[202].item_id = "indicsentiment-test-555"
tokens[202].token = "settings"
tokens[202].tag = "en"
tokens[203].item_id = "indicsentiment-test-555"
tokens[203].token = "upakaranagalu"
tokens[203].tag = "kn"
tokens[204].item_id = "indicsentiment-test-555"
tokens[204].token = "matthu"
tokens[204].tag = "kn"
tokens[205].item_id = "indicsentiment-test-555"
tokens[205].token = "aykegalive"
tokens[205].tag = "kn"
tokens[206].item_id = "indicsentiment-test-67"
tokens[206].token = "avara"
tokens[206].tag = "kn"
tokens[207].item_id = "indicsentiment-test-67"
tokens[207].token = "eggless"
tokens[207].tag = "kn"
tokens[208].item_id = "indicsentiment-test-67"
tokens[208].token = "pastry"
tokens[208].tag = "en"
tokens[209].item_id = "indicsentiment-test-67"
tokens[209].token = "collection"
tokens[209].tag = "en"
tokens[210].item_id = "indicsentiment-test-67"
tokens[210].token = "tumba"
tokens[210].tag = "kn"
tokens[211].item_id = "indicsentiment-test-67"
tokens[211].token = "limited"
tokens[211].tag = "u"
tokens[212].item_id = "indicsentiment-test-67"
tokens[212].token = "ittu"
tokens[212].tag = "kn"
tokens[213].item_id = "indicsentiment-test-67"
tokens[213].token = "service"
tokens[213].tag = "en"
tokens[214].item_id = "indicsentiment-test-67"
tokens[214].token = "sometimes"
tokens[214].tag = "en"
tokens[215].item_id = "indicsentiment-test-67"
tokens[215].token = "hot"
tokens[215].tag = "en"
tokens[216].item_id = "indicsentiment-test-67"
tokens[216].token = "chocolate"
tokens[216].tag = "en"
tokens[217].item_id = "indicsentiment-test-67"
tokens[217].token = "na"
tokens[217].tag = "u"
tokens[218].item_id = "indicsentiment-test-67"
tokens[218].token = "tarnish"
tokens[218].tag = "en"
tokens[219].item_id = "indicsentiment-test-67"
tokens[219].token = "madoke"
tokens[219].tag = "kn"
tokens[220].item_id = "indicsentiment-test-67"
tokens[220].token = "thumba"
tokens[220].tag = "kn"
tokens[221].item_id = "indicsentiment-test-67"
tokens[221].token = "time"
tokens[221].tag = "en"
tokens[222].item_id = "indicsentiment-test-67"
tokens[222].token = "togoltade"
tokens[222].tag = "kn"
tokens[223].item_id = "indicsentiment-test-67"
tokens[223].token = "Allade"
tokens[223].tag = "kn"
tokens[224].item_id = "indicsentiment-test-67"
tokens[224].token = "snacks"
tokens[224].tag = "en"
tokens[225].item_id = "indicsentiment-test-67"
tokens[225].token = "sometimes"
tokens[225].tag = "en"
tokens[226].item_id = "indicsentiment-test-67"
tokens[226].token = "stale"
tokens[226].tag = "en"
tokens[227].item_id = "indicsentiment-test-67"
tokens[227].token = "agi"
tokens[227].tag = "u"
tokens[228].item_id = "indicsentiment-test-67"
tokens[228].token = "physical"
tokens[228].tag = "en"
tokens[229].item_id = "indicsentiment-test-67"
tokens[229].token = "discomfort"
tokens[229].tag = "en"
tokens[230].item_id = "indicsentiment-test-67"
tokens[230].token = "untu"
tokens[230].tag = "kn"
tokens[231].item_id = "indicsentiment-test-67"
tokens[231].token = "madutte"
tokens[231].tag = "kn"
tokens[232].item_id = "indicsentiment-test-207"
tokens[232].token = "Ee"
tokens[232].tag = "u"
tokens[233].item_id = "indicsentiment-test-207"
tokens[233].token = "janru"
tokens[233].tag = "kn"
tokens[234].item_id = "indicsentiment-test-207"
tokens[234].token = "product"
tokens[234].tag = "en"
tokens[235].item_id = "indicsentiment-test-207"
tokens[235].token = "price"
tokens[235].tag = "en"
tokens[236].item_id = "indicsentiment-test-207"
tokens[236].token = "na"
tokens[236].tag = "u"
tokens[237].item_id = "indicsentiment-test-207"
tokens[237].token = "kami"
tokens[237].tag = "en"
tokens[238].item_id = "indicsentiment-test-207"
tokens[238].token = "madoke"
tokens[238].tag = "kn"
tokens[239].item_id = "indicsentiment-test-207"
tokens[239].token = "kapa"
tokens[239].tag = "kn"
tokens[240].item_id = "indicsentiment-test-207"
tokens[240].token = "quality"
tokens[240].tag = "en"
tokens[241].item_id = "indicsentiment-test-207"
tokens[241].token = "materials"
tokens[241].tag = "en"
tokens[242].item_id = "indicsentiment-test-207"
tokens[242].token = "use"
tokens[242].tag = "en"
tokens[243].item_id = "indicsentiment-test-207"
tokens[243].token = "madtare"
tokens[243].tag = "kn"
tokens[244].item_id = "indicsentiment-test-207"
tokens[244].token = "adre"
tokens[244].tag = "kn"
tokens[245].item_id = "indicsentiment-test-207"
tokens[245].token = "idu"
tokens[245].tag = "kn"
tokens[246].item_id = "indicsentiment-test-207"
tokens[246].token = "product"
tokens[246].tag = "en"
tokens[247].item_id = "indicsentiment-test-207"
tokens[247].token = "kapa"
tokens[247].tag = "kn"
tokens[248].item_id = "indicsentiment-test-207"
tokens[248].token = "quality"
tokens[248].tag = "en"
tokens[249].item_id = "indicsentiment-test-207"
tokens[249].token = "nalli"
tokens[249].tag = "kn"
tokens[250].item_id = "indicsentiment-test-207"
tokens[250].token = "result"
tokens[250].tag = "en"
tokens[251].item_id = "indicsentiment-test-207"
tokens[251].token = "madutte"
tokens[251].tag = "kn"
tokens[252].item_id = "indicsentiment-test-520"
tokens[252].token = "Nanna"
tokens[252].tag = "kn"
tokens[253].item_id = "indicsentiment-test-520"
tokens[253].token = "hour"
tokens[253].tag = "en"
tokens[254].item_id = "indicsentiment-test-520"
tokens[254].token = "athava"
tokens[254].tag = "kn"
tokens[255].item_id = "indicsentiment-test-520"
tokens[255].token = "adakkinta"
tokens[255].tag = "kn"
tokens[256].item_id = "indicsentiment-test-520"
tokens[256].token = "hechu"
tokens[256].tag = "kn"
tokens[257].item_id = "indicsentiment-test-520"
tokens[257].token = "samaya"
tokens[257].tag = "kn"
tokens[258].item_id = "indicsentiment-test-520"
tokens[258].token = "vyarthavaitu"
tokens[258].tag = "kn"
tokens[259].item_id = "indicsentiment-test-520"
tokens[259].token = "mattu"
tokens[259].tag = "kn"
tokens[260].item_id = "indicsentiment-test-520"
tokens[260].token = "yavude"
tokens[260].tag = "kn"
tokens[261].item_id = "indicsentiment-test-520"
tokens[261].token = "action"
tokens[261].tag = "en"
tokens[262].item_id = "indicsentiment-test-520"
tokens[262].token = "illa"
tokens[262].tag = "kn"
tokens[263].item_id = "indicsentiment-test-520"
tokens[263].token = "sahasa"
tokens[263].tag = "kn"
tokens[264].item_id = "indicsentiment-test-520"
tokens[264].token = "illa"
tokens[264].tag = "kn"
tokens[265].item_id = "indicsentiment-test-520"
tokens[265].token = "fight"
tokens[265].tag = "en"
tokens[266].item_id = "indicsentiment-test-520"
tokens[266].token = "illa"
tokens[266].tag = "kn"
tokens[267].item_id = "indicsentiment-test-724"
tokens[267].token = "Idhu"
tokens[267].tag = "kn"
tokens[268].item_id = "indicsentiment-test-724"
tokens[268].token = "nutrition"
tokens[268].tag = "en"
tokens[269].item_id = "indicsentiment-test-724"
tokens[269].token = "kodutte"
tokens[269].tag = "kn"
tokens[270].item_id = "indicsentiment-test-724"
tokens[270].token = "mattu"
tokens[270].tag = "kn"
tokens[271].item_id = "indicsentiment-test-724"
tokens[271].token = "vasaneni"
tokens[271].tag = "kn"
tokens[272].item_id = "indicsentiment-test-724"
tokens[272].token = "twarittede"
tokens[272].tag = "kn"
tokens[273].item_id = "indicsentiment-test-724"
tokens[273].token = "control"
tokens[273].tag = "en"
tokens[274].item_id = "indicsentiment-test-724"
tokens[274].token = "madoke"
tokens[274].tag = "kn"
tokens[275].item_id = "indicsentiment-test-724"
tokens[275].token = "help"
tokens[275].tag = "u"
tokens[276].item_id = "indicsentiment-test-724"
tokens[276].token = "madutte"
tokens[276].tag = "kn"
tokens[277].item_id = "indicsentiment-test-724"
tokens[277].token = "Skin"
tokens[277].tag = "u"
tokens[278].item_id = "indicsentiment-test-724"
tokens[278].token = "irritation"
tokens[278].tag = "en"
tokens[279].item_id = "indicsentiment-test-724"
tokens[279].token = "avoid"
tokens[279].tag = "en"
tokens[280].item_id = "indicsentiment-test-724"
tokens[280].token = "madoke"
tokens[280].tag = "kn"
tokens[281].item_id = "indicsentiment-test-724"
tokens[281].token = "idhu"
tokens[281].tag = "kn"
tokens[282].item_id = "indicsentiment-test-724"
tokens[282].token = "thumba"
tokens[282].tag = "kn"
tokens[283].item_id = "indicsentiment-test-724"
tokens[283].token = "gentle"
tokens[283].tag = "en"
tokens[284].item_id = "indicsentiment-test-724"
tokens[284].token = "mattu"
tokens[284].tag = "kn"
tokens[285].item_id = "indicsentiment-test-724"
tokens[285].token = "alcohol"
tokens[285].tag = "en"
tokens[286].item_id = "indicsentiment-test-724"
tokens[286].token = "free"
tokens[286].tag = "en"
tokens[287].item_id = "indicsentiment-test-724"
tokens[287].token = "aagide"
tokens[287].tag = "kn"
tokens[288].item_id = "indicsentiment-test-239"
tokens[288].token = "aatakke"
tokens[288].tag = "kn"
tokens[289].item_id = "indicsentiment-test-239"
tokens[289].token = "hechchu"
tokens[289].tag = "kn"
tokens[290].item_id = "indicsentiment-test-239"
tokens[290].token = "vaividhyamaya"
tokens[290].tag = "kn"
tokens[291].item_id = "indicsentiment-test-239"
tokens[291].token = "thunakugalu"
tokens[291].tag = "kn"
tokens[292].item_id = "indicsentiment-test-239"
tokens[292].token = "agatyavide"
tokens[292].tag = "kn"
tokens[293].item_id = "indicsentiment-test-239"
tokens[293].token = "nanu"
tokens[293].tag = "kn"
tokens[294].item_id = "indicsentiment-test-239"
tokens[294].token = "onde"
tokens[294].tag = "kn"
tokens[295].item_id = "indicsentiment-test-239"
tokens[295].token = "akaragalappade"
tokens[295].tag = "kn"
tokens[296].item_id = "indicsentiment-test-239"
tokens[296].token = "irutte"
tokens[296].tag = "kn"
tokens[297].item_id = "indicsentiment-test-239"
tokens[297].token = "ella"
tokens[297].tag = "u"
tokens[298].item_id = "indicsentiment-test-239"
tokens[298].token = "onte"
tokens[298].tag = "kn"
tokens[299].item_id = "indicsentiment-test-239"
tokens[299].token = "tara"
tokens[299].tag = "u"
tokens[300].item_id = "indicsentiment-test-239"
tokens[300].token = "aakaragalu"
tokens[300].tag = "kn"
tokens[301].item_id = "indicsentiment-test-239"
tokens[301].token = "bartide"
tokens[301].tag = "kn"
tokens[302].item_id = "indicsentiment-test-239"
tokens[302].token = "tumbaa"
tokens[302].tag = "kn"
tokens[303].item_id = "indicsentiment-test-239"
tokens[303].token = "advertisements"
tokens[303].tag = "en"
tokens[304].item_id = "indicsentiment-test-239"
tokens[304].token = "bartide"
tokens[304].tag = "kn"
tokens[305].item_id = "indicsentiment-test-239"
tokens[305].token = "neevu"
tokens[305].tag = "kn"
tokens[306].item_id = "indicsentiment-test-239"
tokens[306].token = "hosaa"
tokens[306].tag = "kn"
tokens[307].item_id = "indicsentiment-test-239"
tokens[307].token = "round"
tokens[307].tag = "en"
tokens[308].item_id = "indicsentiment-test-239"
tokens[308].token = "start"
tokens[308].tag = "u"
tokens[309].item_id = "indicsentiment-test-239"
tokens[309].token = "madovaga"
tokens[309].tag = "kn"
tokens[310].item_id = "indicsentiment-test-239"
tokens[310].token = "ad"
tokens[310].tag = "u"
tokens[311].item_id = "indicsentiment-test-239"
tokens[311].token = "play"
tokens[311].tag = "en"
tokens[312].item_id = "indicsentiment-test-239"
tokens[312].token = "agatte"
tokens[312].tag = "kn"
tokens[313].item_id = "indicsentiment-test-239"
tokens[313].token = "mattu"
tokens[313].tag = "kn"
tokens[314].item_id = "indicsentiment-test-239"
tokens[314].token = "nimage"
tokens[314].tag = "kn"
tokens[315].item_id = "indicsentiment-test-239"
tokens[315].token = "game"
tokens[315].tag = "en"
tokens[316].item_id = "indicsentiment-test-239"
tokens[316].token = "inda"
tokens[316].tag = "kn"
tokens[317].item_id = "indicsentiment-test-239"
tokens[317].token = "horabarokku"
tokens[317].tag = "kn"
tokens[318].item_id = "indicsentiment-test-239"
tokens[318].token = "chance"
tokens[318].tag = "en"
tokens[319].item_id = "indicsentiment-test-239"
tokens[319].token = "kodovgu"
tokens[319].tag = "kn"
tokens[320].item_id = "indicsentiment-test-239"
tokens[320].token = "munche"
tokens[320].tag = "kn"
tokens[321].item_id = "indicsentiment-test-239"
tokens[321].token = "ad"
tokens[321].tag = "u"
tokens[322].item_id = "indicsentiment-test-239"
tokens[322].token = "play"
tokens[322].tag = "en"
tokens[323].item_id = "indicsentiment-test-239"
tokens[323].token = "agatte"
tokens[323].tag = "kn"
tokens[324].item_id = "indicsentiment-test-887"
tokens[324].token = "kammi"
tokens[324].tag = "kn"
tokens[325].item_id = "indicsentiment-test-887"
tokens[325].token = "noise"
tokens[325].tag = "en"
tokens[326].item_id = "indicsentiment-test-887"
tokens[326].token = "cancellation"
tokens[326].tag = "en"
tokens[327].item_id = "indicsentiment-test-887"
tokens[327].token = "ondu"
tokens[327].tag = "kn"
tokens[328].item_id = "indicsentiment-test-887"
tokens[328].token = "major"
tokens[328].tag = "en"
tokens[329].item_id = "indicsentiment-test-887"
tokens[329].token = "problem"
tokens[329].tag = "en"
tokens[330].item_id = "indicsentiment-test-887"
tokens[330].token = "agide"
tokens[330].tag = "kn"
tokens[331].item_id = "indicsentiment-test-277"
tokens[331].token = "Ee"
tokens[331].tag = "u"
tokens[332].item_id = "indicsentiment-test-277"
tokens[332].token = "purushara"
tokens[332].tag = "kn"
tokens[333].item_id = "indicsentiment-test-277"
tokens[333].token = "sugandhdravyadinda"
tokens[333].tag = "kn"
tokens[334].item_id = "indicsentiment-test-277"
tokens[334].token = "neevu"
tokens[334].tag = "kn"
tokens[335].item_id = "indicsentiment-test-277"
tokens[335].token = "neerina"
tokens[335].tag = "kn"
tokens[336].item_id = "indicsentiment-test-277"
tokens[336].token = "kamala"
tokens[336].tag = "u"
tokens[337].item_id = "indicsentiment-test-277"
tokens[337].token = "mattu"
tokens[337].tag = "kn"
tokens[338].item_id = "indicsentiment-test-277"
tokens[338].token = "devadaru"
tokens[338].tag = "kn"
tokens[339].item_id = "indicsentiment-test-277"
tokens[339].token = "marada"
tokens[339].tag = "kn"
tokens[340].item_id = "indicsentiment-test-277"
tokens[340].token = "sihi"
tokens[340].tag = "kn"
tokens[341].item_id = "indicsentiment-test-277"
tokens[341].token = "sugandhavannu"
tokens[341].tag = "kn"
tokens[342].item_id = "indicsentiment-test-277"
tokens[342].token = "anubhavisabahudu"
tokens[342].tag = "kn"
tokens[343].item_id = "indicsentiment-test-277"
tokens[343].token = "Idu"
tokens[343].tag = "kn"
tokens[344].item_id = "indicsentiment-test-277"
tokens[344].token = "deergha"
tokens[344].tag = "kn"
tokens[345].item_id = "indicsentiment-test-277"
tokens[345].token = "kala"
tokens[345].tag = "u"
tokens[346].item_id = "indicsentiment-test-277"
tokens[346].token = "baalikeyige"
tokens[346].tag = "kn"
tokens[347].item_id = "indicsentiment-test-277"
tokens[347].token = "baruttade"
tokens[347].tag = "kn"
tokens[348].item_id = "indicsentiment-test-826"
tokens[348].token = "iga"
tokens[348].tag = "u"
tokens[349].item_id = "indicsentiment-test-826"
tokens[349].token = "split"
tokens[349].tag = "en"
tokens[350].item_id = "indicsentiment-test-826"
tokens[350].token = "ac"
tokens[350].tag = "en"
tokens[351].item_id = "indicsentiment-test-826"
tokens[351].token = "lli"
tokens[351].tag = "kn"
tokens[352].item_id = "indicsentiment-test-826"
tokens[352].token = "air"
tokens[352].tag = "u"
tokens[353].item_id = "indicsentiment-test-826"
tokens[353].token = "purifiers"
tokens[353].tag = "kn"
tokens[354].item_id = "indicsentiment-test-826"
tokens[354].token = "barutte"
tokens[354].tag = "kn"
tokens[355].item_id = "indicsentiment-test-826"
tokens[355].token = "but"
tokens[355].tag = "u"
tokens[356].item_id = "indicsentiment-test-826"
tokens[356].token = "air"
tokens[356].tag = "u"
tokens[357].item_id = "indicsentiment-test-826"
tokens[357].token = "purifiers"
tokens[357].tag = "kn"
tokens[358].item_id = "indicsentiment-test-826"
tokens[358].token = "carbon"
tokens[358].tag = "en"
tokens[359].item_id = "indicsentiment-test-826"
tokens[359].token = "dioxide"
tokens[359].tag = "en"
tokens[360].item_id = "indicsentiment-test-826"
tokens[360].token = "na"
tokens[360].tag = "u"
tokens[361].item_id = "indicsentiment-test-826"
tokens[361].token = "remove"
tokens[361].tag = "en"
tokens[362].item_id = "indicsentiment-test-826"
tokens[362].token = "madalla"
tokens[362].tag = "kn"
tokens[363].item_id = "indicsentiment-test-826"
tokens[363].token = "adakke"
tokens[363].tag = "kn"
tokens[364].item_id = "indicsentiment-test-826"
tokens[364].token = "occasionaly"
tokens[364].tag = "kn"
tokens[365].item_id = "indicsentiment-test-826"
tokens[365].token = "windows"
tokens[365].tag = "en"
tokens[366].item_id = "indicsentiment-test-826"
tokens[366].token = "open"
tokens[366].tag = "en"
tokens[367].item_id = "indicsentiment-test-826"
tokens[367].token = "madodu"
tokens[367].tag = "kn"
tokens[368].item_id = "indicsentiment-test-826"
tokens[368].token = "thumba"
tokens[368].tag = "kn"
tokens[369].item_id = "indicsentiment-test-826"
tokens[369].token = "important"
tokens[369].tag = "en"
tokens[370].item_id = "indicsentiment-test-826"
tokens[370].token = "Doors"
tokens[370].tag = "en"
tokens[371].item_id = "indicsentiment-test-826"
tokens[371].token = "and"
tokens[371].tag = "u"
tokens[372].item_id = "indicsentiment-test-826"
tokens[372].token = "windows"
tokens[372].tag = "en"
tokens[373].item_id = "indicsentiment-test-826"
tokens[373].token = "open"
tokens[373].tag = "en"
tokens[374].item_id = "indicsentiment-test-826"
tokens[374].token = "ittukollodu"
tokens[374].tag = "kn"
tokens[375].item_id = "indicsentiment-test-826"
tokens[375].token = "air"
tokens[375].tag = "u"
tokens[376].item_id = "indicsentiment-test-826"
tokens[376].token = "purifier"
tokens[376].tag = "en"
tokens[377].item_id = "indicsentiment-test-826"
tokens[377].token = "effectiveness"
tokens[377].tag = "en"
tokens[378].item_id = "indicsentiment-test-826"
tokens[378].token = "na"
tokens[378].tag = "u"
tokens[379].item_id = "indicsentiment-test-826"
tokens[379].token = "kami"
tokens[379].tag = "en"
tokens[380].item_id = "indicsentiment-test-826"
tokens[380].token = "madutte"
tokens[380].tag = "kn"
tokens[381].item_id = "indicsentiment-test-744"
tokens[381].token = "Idhu"
tokens[381].tag = "kn"
tokens[382].item_id = "indicsentiment-test-744"
tokens[382].token = "BIS"
tokens[382].tag = "en"
tokens[383].item_id = "indicsentiment-test-744"
tokens[383].token = "pramanikruthavagide"
tokens[383].tag = "kn"
tokens[384].item_id = "indicsentiment-test-744"
tokens[384].token = "mattu"
tokens[384].tag = "kn"
tokens[385].item_id = "indicsentiment-test-744"
tokens[385].token = "surakshitavagide"
tokens[385].tag = "kn"
tokens[386].item_id = "indicsentiment-test-744"
tokens[386].token = "endu"
tokens[386].tag = "kn"
tokens[387].item_id = "indicsentiment-test-744"
tokens[387].token = "helikolluttade"
tokens[387].tag = "kn"
tokens[388].item_id = "indicsentiment-test-516"
tokens[388].token = "Voice"
tokens[388].tag = "en"
tokens[389].item_id = "indicsentiment-test-516"
tokens[389].token = "over"
tokens[389].tag = "en"
tokens[390].item_id = "indicsentiment-test-516"
tokens[390].token = "thumba"
tokens[390].tag = "kn"
tokens[391].item_id = "indicsentiment-test-516"
tokens[391].token = "chennagittu"
tokens[391].tag = "kn"
tokens[392].item_id = "indicsentiment-test-516"
tokens[392].token = "matthu"
tokens[392].tag = "kn"
tokens[393].item_id = "indicsentiment-test-516"
tokens[393].token = "katheya"
tokens[393].tag = "kn"
tokens[394].item_id = "indicsentiment-test-516"
tokens[394].token = "mitiyannu"
tokens[394].tag = "kn"
tokens[395].item_id = "indicsentiment-test-516"
tokens[395].token = "gamanadalli"
tokens[395].tag = "kn"
tokens[396].item_id = "indicsentiment-test-516"
tokens[396].token = "ittukondu"
tokens[396].tag = "kn"
tokens[397].item_id = "indicsentiment-test-516"
tokens[397].token = "anusarisalu"
tokens[397].tag = "kn"
tokens[398].item_id = "indicsentiment-test-516"
tokens[398].token = "sulabhavagide"
tokens[398].tag = "kn"
tokens[399].item_id = "indicsentiment-test-516"
tokens[399].token = "mattu"
tokens[399].tag = "kn"
tokens[400].item_id = "indicsentiment-test-516"
tokens[400].token = "todagisikondide"
tokens[400].tag = "kn"
tokens[401].item_id = "flores-18"
tokens[401].token = "pratpanchadadhyanta"
tokens[401].tag = "kn"
tokens[402].item_id = "flores-18"
tokens[402].token = "pratibatanegalu"
tokens[402].tag = "kn"
tokens[403].item_id = "flores-18"
tokens[403].token = "nadadavu"
tokens[403].tag = "kn"
tokens[404].item_id = "flores-18"
tokens[404].token = "halavu"
tokens[404].tag = "kn"
tokens[405].item_id = "flores-18"
tokens[405].token = "criminal"
tokens[405].tag = "en"
tokens[406].item_id = "flores-18"
tokens[406].token = "mokaddamegalu"
tokens[406].tag = "kn"
tokens[407].item_id = "flores-18"
tokens[407].token = "adavu"
tokens[407].tag = "kn"
tokens[408].item_id = "flores-18"
tokens[408].token = "mattu"
tokens[408].tag = "kn"
tokens[409].item_id = "flores-18"
tokens[409].token = "Iceland"
tokens[409].tag = "en"
tokens[410].item_id = "flores-18"
tokens[410].token = "hagu"
tokens[410].tag = "kn"
tokens[411].item_id = "flores-18"
tokens[411].token = "Pakistani"
tokens[411].tag = "u"
tokens[412].item_id = "flores-18"
tokens[412].token = "sarkarangala"
tokens[412].tag = "kn"
tokens[413].item_id = "flores-18"
tokens[413].token = "nayakaru"
tokens[413].tag = "kn"
tokens[414].item_id = "flores-18"
tokens[414].token = "rajinameneyu"
tokens[414].tag = "kn"
tokens[415].item_id = "flores-18"
tokens[415].token = "saha"
tokens[415].tag = "kn"
tokens[416].item_id = "flores-18"
tokens[416].token = "kottaru"
tokens[416].tag = "kn"
tokens[417].item_id = "flores-259"
tokens[417].token = "pipeline"
tokens[417].tag = "en"
tokens[418].item_id = "flores-259"
tokens[418].token = "entrance"
tokens[418].tag = "en"
tokens[419].item_id = "flores-259"
tokens[419].token = "block"
tokens[419].tag = "en"
tokens[420].item_id = "flores-259"
tokens[420].token = "madoke"
tokens[420].tag = "kn"
tokens[421].item_id = "flores-259"
tokens[421].token = "dump"
tokens[421].tag = "en"
tokens[422].item_id = "flores-259"
tokens[422].token = "trucks"
tokens[422].tag = "en"
tokens[423].item_id = "flores-259"
tokens[423].token = "use"
tokens[423].tag = "en"
tokens[424].item_id = "flores-259"
tokens[424].token = "madtidru"
tokens[424].tag = "kn"
tokens[425].item_id = "flores-259"
tokens[425].token = "matte"
tokens[425].tag = "u"
tokens[426].item_id = "flores-259"
tokens[426].token = "police"
tokens[426].tag = "en"
tokens[427].item_id = "flores-259"
tokens[427].token = "officers"
tokens[427].tag = "en"
tokens[428].item_id = "flores-259"
tokens[428].token = "drivers"
tokens[428].tag = "en"
tokens[429].item_id = "flores-259"
tokens[429].token = "na"
tokens[429].tag = "u"
tokens[430].item_id = "flores-259"
tokens[430].token = "bypass"
tokens[430].tag = "en"
tokens[431].item_id = "flores-259"
tokens[431].token = "kade"
tokens[431].tag = "kn"
tokens[432].item_id = "flores-259"
tokens[432].token = "karkond"
tokens[432].tag = "kn"
tokens[433].item_id = "flores-259"
tokens[433].token = "hogoke"
tokens[433].tag = "kn"
tokens[434].item_id = "flores-259"
tokens[434].token = "support"
tokens[434].tag = "en"
tokens[435].item_id = "flores-259"
tokens[435].token = "madru"
tokens[435].tag = "kn"
tokens[436].item_id = "flores-266"
tokens[436].token = "Russian"
tokens[436].tag = "en"
tokens[437].item_id = "flores-266"
tokens[437].token = "bhu"
tokens[437].tag = "kn"
tokens[438].item_id = "flores-266"
tokens[438].token = "niyanthrakavu"
tokens[438].tag = "kn"
tokens[439].item_id = "flores-266"
tokens[439].token = "jetsgalannu"
tokens[439].tag = "kn"
tokens[440].item_id = "flores-266"
tokens[440].token = "sakriyagolisithu"
tokens[440].tag = "kn"
tokens[441].item_id = "flores-266"
tokens[441].token = "mattu"
tokens[441].tag = "kn"
tokens[442].item_id = "flores-266"
tokens[442].token = "station"
tokens[442].tag = "en"
tokens[443].item_id = "flores-266"
tokens[443].token = "na"
tokens[443].tag = "u"
tokens[444].item_id = "flores-266"
tokens[444].token = "samanya"
tokens[444].tag = "kn"
tokens[445].item_id = "flores-266"
tokens[445].token = "ettaravannu"
tokens[445].tag = "kn"
tokens[446].item_id = "flores-266"
tokens[446].token = "marugalike"
tokens[446].tag = "kn"
tokens[447].item_id = "flores-266"
tokens[447].token = "madikollalayithu"
tokens[447].tag = "kn"
tokens[448].item_id = "flores-276"
tokens[448].token = "House"
tokens[448].tag = "en"
tokens[449].item_id = "flores-276"
tokens[449].token = "energy"
tokens[449].tag = "en"
tokens[450].item_id = "flores-276"
tokens[450].token = "mattu"
tokens[450].tag = "kn"
tokens[451].item_id = "flores-276"
tokens[451].token = "commerce"
tokens[451].tag = "en"
tokens[452].item_id = "flores-276"
tokens[452].token = "committee"
tokens[452].tag = "en"
tokens[453].item_id = "flores-276"
tokens[453].token = "adiyalli"
tokens[453].tag = "kn"
tokens[454].item_id = "flores-276"
tokens[454].token = "iro"
tokens[454].tag = "kn"
tokens[455].item_id = "flores-276"
tokens[455].token = "oversight"
tokens[455].tag = "en"
tokens[456].item_id = "flores-276"
tokens[456].token = "mattu"
tokens[456].tag = "kn"
tokens[457].item_id = "flores-276"
tokens[457].token = "investigations"
tokens[457].tag = "en"
tokens[458].item_id = "flores-276"
tokens[458].token = "subcommittee"
tokens[458].tag = "en"
tokens[459].item_id = "flores-276"
tokens[459].token = "chief"
tokens[459].tag = "en"
tokens[460].item_id = "flores-276"
tokens[460].token = "post"
tokens[460].tag = "u"
tokens[461].item_id = "flores-276"
tokens[461].token = "dalli"
tokens[461].tag = "kn"
tokens[462].item_id = "flores-276"
tokens[462].token = "planned"
tokens[462].tag = "en"
tokens[463].item_id = "flores-276"
tokens[463].token = "parenthood"
tokens[463].tag = "en"
tokens[464].item_id = "flores-276"
tokens[464].token = "dwara"
tokens[464].tag = "kn"
tokens[465].item_id = "flores-276"
tokens[465].token = "abortions"
tokens[465].tag = "en"
tokens[466].item_id = "flores-276"
tokens[466].token = "ge"
tokens[466].tag = "u"
tokens[467].item_id = "flores-276"
tokens[467].token = "funds"
tokens[467].tag = "en"
tokens[468].item_id = "flores-276"
tokens[468].token = "kodo"
tokens[468].tag = "kn"
tokens[469].item_id = "flores-276"
tokens[469].token = "koskara"
tokens[469].tag = "kn"
tokens[470].item_id = "flores-276"
tokens[470].token = "taxes"
tokens[470].tag = "en"
tokens[471].item_id = "flores-276"
tokens[471].token = "use"
tokens[471].tag = "en"
tokens[472].item_id = "flores-276"
tokens[472].token = "madta"
tokens[472].tag = "kn"
tokens[473].item_id = "flores-276"
tokens[473].token = "idara"
tokens[473].tag = "kn"
tokens[474].item_id = "flores-276"
tokens[474].token = "anta"
tokens[474].tag = "kn"
tokens[475].item_id = "flores-276"
tokens[475].token = "Stearns"
tokens[475].tag = "en"
tokens[476].item_id = "flores-276"
tokens[476].token = "investigate"
tokens[476].tag = "en"
tokens[477].item_id = "flores-276"
tokens[477].token = "madtiddare"
tokens[477].tag = "kn"
tokens[478].item_id = "flores-398"
tokens[478].token = "Italiya"
tokens[478].tag = "kn"
tokens[479].item_id = "flores-398"
tokens[479].token = "mukhya"
tokens[479].tag = "kn"
tokens[480].item_id = "flores-398"
tokens[480].token = "vaada"
tokens[480].tag = "kn"
tokens[481].item_id = "flores-398"
tokens[481].token = "gurigalu"
tokens[481].tag = "kn"
tokens[482].item_id = "flores-398"
tokens[482].token = "endre"
tokens[482].tag = "kn"
tokens[483].item_id = "flores-398"
tokens[483].token = "African"
tokens[483].tag = "en"
tokens[484].item_id = "flores-398"
tokens[484].token = "deshagalu"
tokens[484].tag = "kn"
tokens[485].item_id = "flores-398"
tokens[485].token = "Matte"
tokens[485].tag = "u"
tokens[486].item_id = "flores-398"
tokens[486].token = "ee"
tokens[486].tag = "u"
tokens[487].item_id = "flores-398"
tokens[487].token = "deshagalannu"
tokens[487].tag = "kn"
tokens[488].item_id = "flores-398"
tokens[488].token = "vashapadisikollalu"
tokens[488].tag = "kn"
tokens[489].item_id = "flores-398"
tokens[489].token = "avarige"
tokens[489].tag = "kn"
tokens[490].item_id = "flores-398"
tokens[490].token = "senapadeyu"
tokens[490].tag = "kn"
tokens[491].item_id = "flores-398"
tokens[491].token = "Mediterranean"
tokens[491].tag = "en"
tokens[492].item_id = "flores-398"
tokens[492].token = "sagaradaadanta"
tokens[492].tag = "kn"
tokens[493].item_id = "flores-398"
tokens[493].token = "saagi"
tokens[493].tag = "kn"
tokens[494].item_id = "flores-398"
tokens[494].token = "Africavannu"
tokens[494].tag = "kn"
tokens[495].item_id = "flores-398"
tokens[495].token = "akramisikollalu"
tokens[495].tag = "kn"
tokens[496].item_id = "flores-398"
tokens[496].token = "sena"
tokens[496].tag = "u"
tokens[497].item_id = "flores-398"
tokens[497].token = "tukadigalannu"
tokens[497].tag = "kn"
tokens[498].item_id = "flores-398"
tokens[498].token = "sagisalu"
tokens[498].tag = "kn"
tokens[499].item_id = "flores-398"
tokens[499].token = "launch"
tokens[499].tag = "en"
tokens[500].item_id = "flores-398"
tokens[500].token = "padgalu"
tokens[500].tag = "kn"
tokens[501].item_id = "flores-398"
tokens[501].token = "bekagittu"
tokens[501].tag = "kn"
tokens[502].item_id = "flores-434"
tokens[502].token = "Luxembourg"
tokens[502].tag = "en"
tokens[503].item_id = "flores-434"
tokens[503].token = "yavaglu"
tokens[503].tag = "kn"
tokens[504].item_id = "flores-434"
tokens[504].token = "ondu"
tokens[504].tag = "kn"
tokens[505].item_id = "flores-434"
tokens[505].token = "neutral"
tokens[505].tag = "en"
tokens[506].item_id = "flores-434"
tokens[506].token = "nation"
tokens[506].tag = "en"
tokens[507].item_id = "flores-434"
tokens[507].token = "agi"
tokens[507].tag = "u"
tokens[508].item_id = "flores-434"
tokens[508].token = "iroke"
tokens[508].tag = "kn"
tokens[509].item_id = "flores-434"
tokens[509].token = "ista"
tokens[509].tag = "kn"
tokens[510].item_id = "flores-434"
tokens[510].token = "pattu"
tokens[510].tag = "kn"
tokens[511].item_id = "flores-434"
tokens[511].token = "ana"
tokens[511].tag = "u"
tokens[512].item_id = "flores-434"
tokens[512].token = "adanna"
tokens[512].tag = "kn"
tokens[513].item_id = "flores-434"
tokens[513].token = "first"
tokens[513].tag = "en"
tokens[514].item_id = "flores-434"
tokens[514].token = "world"
tokens[514].tag = "en"
tokens[515].item_id = "flores-434"
tokens[515].token = "war"
tokens[515].tag = "en"
tokens[516].item_id = "flores-434"
tokens[516].token = "mathu"
tokens[516].tag = "kn"
tokens[517].item_id = "flores-434"
tokens[517].token = "second"
tokens[517].tag = "en"
tokens[518].item_id = "flores-434"
tokens[518].token = "world"
tokens[518].tag = "en"
tokens[519].item_id = "flores-434"
tokens[519].token = "war"
tokens[519].tag = "en"
tokens[520].item_id = "flores-434"
tokens[520].token = "eradralu"
tokens[520].tag = "kn"
tokens[521].item_id = "flores-434"
tokens[521].token = "Germany"
tokens[521].tag = "en"
tokens[522].item_id = "flores-434"
tokens[522].token = "invade"
tokens[522].tag = "en"
tokens[523].item_id = "flores-434"
tokens[523].token = "madithu"
tokens[523].tag = "kn"
tokens[524].item_id = "flores-455"
tokens[524].token = "lens"
tokens[524].tag = "u"
tokens[525].item_id = "flores-455"
tokens[525].token = "manufacturercellu"
tokens[525].tag = "kn"
tokens[526].item_id = "flores-455"
tokens[526].token = "lens"
tokens[526].tag = "u"
tokens[527].item_id = "flores-455"
tokens[527].token = "productionalli"
tokens[527].tag = "kn"
tokens[528].item_id = "flores-455"
tokens[528].token = "high"
tokens[528].tag = "en"
tokens[529].item_id = "flores-455"
tokens[529].token = "quality"
tokens[529].tag = "en"
tokens[530].item_id = "flores-455"
tokens[530].token = "achieve"
tokens[530].tag = "en"
tokens[531].item_id = "flores-455"
tokens[531].token = "maadirt"
tokens[531].tag = "kn"
tokens[532].item_id = "flores-455"
tokens[532].token = "irodrinda"
tokens[532].tag = "kn"
tokens[533].item_id = "flores-455"
tokens[533].token = "problem"
tokens[533].tag = "en"
tokens[534].item_id = "flores-455"
tokens[534].token = "adre"
tokens[534].tag = "kn"
tokens[535].item_id = "flores-455"
tokens[535].token = "swalpa"
tokens[535].tag = "kn"
tokens[536].item_id = "flores-455"
tokens[536].token = "kammi"
tokens[536].tag = "kn"
tokens[537].item_id = "flores-455"
tokens[537].token = "agtide"
tokens[537].tag = "kn"
tokens[538].item_id = "flores-456"
tokens[538].token = "idrindaagi"
tokens[538].tag = "kn"
tokens[539].item_id = "flores-456"
tokens[539].token = "nigaadita"
tokens[539].tag = "kn"
tokens[540].item_id = "flores-456"
tokens[540].token = "focal"
tokens[540].tag = "en"
tokens[541].item_id = "flores-456"
tokens[541].token = "length"
tokens[541].tag = "en"
tokens[542].item_id = "flores-456"
tokens[542].token = "lensesgalige"
tokens[542].tag = "kn"
tokens[543].item_id = "flores-456"
tokens[543].token = "holisidare"
tokens[543].tag = "kn"
tokens[544].item_id = "flores-456"
tokens[544].token = "zoom"
tokens[544].tag = "en"
tokens[545].item_id = "flores-456"
tokens[545].token = "lensesgalu"
tokens[545].tag = "kn"
tokens[546].item_id = "flores-456"
tokens[546].token = "gunamattada"
tokens[546].tag = "kn"
tokens[547].item_id = "flores-456"
tokens[547].token = "chitragalannu"
tokens[547].tag = "kn"
tokens[548].item_id = "flores-456"
tokens[548].token = "rachisalu"
tokens[548].tag = "kn"
tokens[549].item_id = "flores-456"
tokens[549].token = "anuvu"
tokens[549].tag = "kn"
tokens[550].item_id = "flores-456"
tokens[550].token = "maadikoduttade"
tokens[550].tag = "kn"
tokens[551].item_id = "flores-458"
tokens[551].token = "Idarindaagi"
tokens[551].tag = "kn"
tokens[552].item_id = "flores-458"
tokens[552].token = "agga"
tokens[552].tag = "kn"
tokens[553].item_id = "flores-458"
tokens[553].token = "zoom"
tokens[553].tag = "en"
tokens[554].item_id = "flores-458"
tokens[554].token = "lens"
tokens[554].tag = "u"
tokens[555].item_id = "flores-458"
tokens[555].token = "galannu"
tokens[555].tag = "kn"
tokens[556].item_id = "flores-458"
tokens[556].token = "flash"
tokens[556].tag = "en"
tokens[557].item_id = "flores-458"
tokens[557].token = "illade"
tokens[557].tag = "kn"
tokens[558].item_id = "flores-458"
tokens[558].token = "low"
tokens[558].tag = "en"
tokens[559].item_id = "flores-458"
tokens[559].token = "light"
tokens[559].tag = "en"
tokens[560].item_id = "flores-458"
tokens[560].token = "situations"
tokens[560].tag = "en"
tokens[561].item_id = "flores-458"
tokens[561].token = "alli"
tokens[561].tag = "u"
tokens[562].item_id = "flores-458"
tokens[562].token = "use"
tokens[562].tag = "en"
tokens[563].item_id = "flores-458"
tokens[563].token = "madodu"
tokens[563].tag = "kn"
tokens[564].item_id = "flores-458"
tokens[564].token = "thumba"
tokens[564].tag = "kn"
tokens[565].item_id = "flores-458"
tokens[565].token = "kashta"
tokens[565].tag = "kn"
tokens[566].item_id = "flores-458"
tokens[566].token = "agutte"
tokens[566].tag = "kn"
tokens[567].item_id = "flores-560"
tokens[567].token = "gayagondavanannu"
tokens[567].tag = "kn"
tokens[568].item_id = "flores-560"
tokens[568].token = "parikshisalu"
tokens[568].tag = "kn"
tokens[569].item_id = "flores-560"
tokens[569].token = "nimma"
tokens[569].tag = "kn"
tokens[570].item_id = "flores-560"
tokens[570].token = "surakshateyannu"
tokens[570].tag = "kn"
tokens[571].item_id = "flores-560"
tokens[571].token = "khachitapadisukollalu"
tokens[571].tag = "kn"
tokens[572].item_id = "flores-560"
tokens[572].token = "drushyavannu"
tokens[572].tag = "kn"
tokens[573].item_id = "flores-560"
tokens[573].token = "modalu"
tokens[573].tag = "kn"
tokens[574].item_id = "flores-560"
tokens[574].token = "thanikhe"
tokens[574].tag = "kn"
tokens[575].item_id = "flores-560"
tokens[575].token = "madabeku"
tokens[575].tag = "kn"
tokens[576].item_id = "flores-602"
tokens[576].token = "Neeru"
tokens[576].tag = "kn"
tokens[577].item_id = "flores-602"
tokens[577].token = "innondu"
tokens[577].tag = "kn"
tokens[578].item_id = "flores-602"
tokens[578].token = "udaharane"
tokens[578].tag = "kn"
tokens[579].item_id = "flores-602"
tokens[579].token = "Neerina"
tokens[579].tag = "kn"
tokens[580].item_id = "flores-602"
tokens[580].token = "samyukthavu"
tokens[580].tag = "kn"
tokens[581].item_id = "flores-602"
tokens[581].token = "eradu"
tokens[581].tag = "kn"
tokens[582].item_id = "flores-602"
tokens[582].token = "hydrogen"
tokens[582].tag = "en"
tokens[583].item_id = "flores-602"
tokens[583].token = "paramanugalu"
tokens[583].tag = "kn"
tokens[584].item_id = "flores-602"
tokens[584].token = "mattu"
tokens[584].tag = "kn"
tokens[585].item_id = "flores-602"
tokens[585].token = "ondu"
tokens[585].tag = "kn"
tokens[586].item_id = "flores-602"
tokens[586].token = "aamlanajaka"
tokens[586].tag = "kn"
tokens[587].item_id = "flores-602"
tokens[587].token = "paramanuvininda"
tokens[587].tag = "kn"
tokens[588].item_id = "flores-602"
tokens[588].token = "koodide"
tokens[588].tag = "kn"
tokens[589].item_id = "flores-678"
tokens[589].token = "Pratiyondu"
tokens[589].tag = "kn"
tokens[590].item_id = "flores-678"
tokens[590].token = "deshavu"
tokens[590].tag = "kn"
tokens[591].item_id = "flores-678"
tokens[591].token = "car"
tokens[591].tag = "en"
tokens[592].item_id = "flores-678"
tokens[592].token = "nalli"
tokens[592].tag = "kn"
tokens[593].item_id = "flores-678"
tokens[593].token = "agatyavagi"
tokens[593].tag = "kn"
tokens[594].item_id = "flores-678"
tokens[594].token = "irabekadanta"
tokens[594].tag = "kn"
tokens[595].item_id = "flores-678"
tokens[595].token = "turtu"
tokens[595].tag = "kn"
tokens[596].item_id = "flores-678"
tokens[596].token = "paristhiti"
tokens[596].tag = "kn"
tokens[597].item_id = "flores-678"
tokens[597].token = "vastugala"
tokens[597].tag = "kn"
tokens[598].item_id = "flores-678"
tokens[598].token = "bagge"
tokens[598].tag = "kn"
tokens[599].item_id = "flores-678"
tokens[599].token = "tannade"
tokens[599].tag = "kn"
tokens[600].item_id = "flores-678"
tokens[600].token = "ada"
tokens[600].tag = "u"
tokens[601].item_id = "flores-678"
tokens[601].token = "vishishta"
tokens[601].tag = "kn"
tokens[602].item_id = "flores-678"
tokens[602].token = "kanunugalannu"
tokens[602].tag = "kn"
tokens[603].item_id = "flores-678"
tokens[603].token = "hondiruttade"
tokens[603].tag = "kn"
tokens[604].item_id = "flores-706"
tokens[604].token = "machu"
tokens[604].tag = "en"
tokens[605].item_id = "flores-706"
tokens[605].token = "pichuvina"
tokens[605].tag = "kn"
tokens[606].item_id = "flores-706"
tokens[606].token = "uttarada"
tokens[606].tag = "kn"
tokens[607].item_id = "flores-706"
tokens[607].token = "thudiyinda"
tokens[607].tag = "kn"
tokens[608].item_id = "flores-706"
tokens[608].token = "meliruva"
tokens[608].tag = "kn"
tokens[609].item_id = "flores-706"
tokens[609].token = "ee"
tokens[609].tag = "u"
tokens[610].item_id = "flores-706"
tokens[610].token = "kadidaada"
tokens[610].tag = "kn"
tokens[611].item_id = "flores-706"
tokens[611].token = "parvatavu"
tokens[611].tag = "kn"
tokens[612].item_id = "flores-706"
tokens[612].token = "avashegala"
tokens[612].tag = "kn"
tokens[613].item_id = "flores-706"
tokens[613].token = "halavaru"
tokens[613].tag = "kn"
tokens[614].item_id = "flores-706"
tokens[614].token = "bhavachitragalige"
tokens[614].tag = "kn"
tokens[615].item_id = "flores-706"
tokens[615].token = "hidida"
tokens[615].tag = "kn"
tokens[616].item_id = "flores-706"
tokens[616].token = "kannadiyaagide"
tokens[616].tag = "kn"
tokens[617].item_id = "flores-764"
tokens[617].token = "Hostel"
tokens[617].tag = "en"
tokens[618].item_id = "flores-764"
tokens[618].token = "galu"
tokens[618].tag = "kn"
tokens[619].item_id = "flores-764"
tokens[619].token = "moolata"
tokens[619].tag = "kn"
tokens[620].item_id = "flores-764"
tokens[620].token = "yuva"
tokens[620].tag = "kn"
tokens[621].item_id = "flores-764"
tokens[621].token = "janategashte"
tokens[621].tag = "kn"
tokens[622].item_id = "flores-764"
tokens[622].token = "jaga"
tokens[622].tag = "kn"
tokens[623].item_id = "flores-764"
tokens[623].token = "koduttave"
tokens[623].tag = "kn"
tokens[624].item_id = "flores-764"
tokens[624].token = "sadharanavagi"
tokens[624].tag = "kn"
tokens[625].item_id = "flores-764"
tokens[625].token = "ippattara"
tokens[625].tag = "kn"
tokens[626].item_id = "flores-764"
tokens[626].token = "harayadavaru"
tokens[626].tag = "kn"
tokens[627].item_id = "flores-764"
tokens[627].token = "adaru"
tokens[627].tag = "kn"
tokens[628].item_id = "flores-764"
tokens[628].token = "madhyavayaska"
tokens[628].tag = "kn"
tokens[629].item_id = "flores-764"
tokens[629].token = "pravasigannoo"
tokens[629].tag = "kn"
tokens[630].item_id = "flores-764"
tokens[630].token = "alli"
tokens[630].tag = "u"
tokens[631].item_id = "flores-764"
tokens[631].token = "kanabahudu"
tokens[631].tag = "kn"
tokens[632].item_id = "flores-811"
tokens[632].token = "Hiking"
tokens[632].tag = "en"
tokens[633].item_id = "flores-811"
tokens[633].token = "enbudu"
tokens[633].tag = "kn"
tokens[634].item_id = "flores-811"
tokens[634].token = "outdoor"
tokens[634].tag = "en"
tokens[635].item_id = "flores-811"
tokens[635].token = "activity"
tokens[635].tag = "en"
tokens[636].item_id = "flores-811"
tokens[636].token = "aagiddu"
tokens[636].tag = "kn"
tokens[637].item_id = "flores-811"
tokens[637].token = "hiking"
tokens[637].tag = "en"
tokens[638].item_id = "flores-811"
tokens[638].token = "dariyalli"
tokens[638].tag = "kn"
tokens[639].item_id = "flores-811"
tokens[639].token = "natural"
tokens[639].tag = "en"
tokens[640].item_id = "flores-811"
tokens[640].token = "environment"
tokens[640].tag = "en"
tokens[641].item_id = "flores-811"
tokens[641].token = "nalli"
tokens[641].tag = "kn"
tokens[642].item_id = "flores-811"
tokens[642].token = "nadeduvodu"
tokens[642].tag = "kn"
tokens[643].item_id = "flores-811"
tokens[643].token = "iruttade"
tokens[643].tag = "kn"
tokens[644].item_id = "flores-822"
tokens[644].token = "Hecchina"
tokens[644].tag = "kn"
tokens[645].item_id = "flores-822"
tokens[645].token = "agencies"
tokens[645].tag = "en"
tokens[646].item_id = "flores-822"
tokens[646].token = "extra"
tokens[646].tag = "en"
tokens[647].item_id = "flores-822"
tokens[647].token = "regular"
tokens[647].tag = "en"
tokens[648].item_id = "flores-822"
tokens[648].token = "booking"
tokens[648].tag = "en"
tokens[649].item_id = "flores-822"
tokens[649].token = "orders"
tokens[649].tag = "en"
tokens[650].item_id = "flores-822"
tokens[650].token = "thagkoloke"
tokens[650].tag = "kn"
tokens[651].item_id = "flores-822"
tokens[651].token = "ready"
tokens[651].tag = "en"
tokens[652].item_id = "flores-822"
tokens[652].token = "iddrunu"
tokens[652].tag = "kn"
tokens[653].item_id = "flores-822"
tokens[653].token = "thumba"
tokens[653].tag = "kn"
tokens[654].item_id = "flores-822"
tokens[654].token = "jana"
tokens[654].tag = "u"
tokens[655].item_id = "flores-822"
tokens[655].token = "agents"
tokens[655].tag = "en"
tokens[656].item_id = "flores-822"
tokens[656].token = "nirdishta"
tokens[656].tag = "kn"
tokens[657].item_id = "flores-822"
tokens[657].token = "tharaha"
tokens[657].tag = "kn"
tokens[658].item_id = "flores-822"
tokens[658].token = "yatra"
tokens[658].tag = "kn"
tokens[659].item_id = "flores-822"
tokens[659].token = "budget"
tokens[659].tag = "en"
tokens[660].item_id = "flores-822"
tokens[660].token = "limits"
tokens[660].tag = "en"
tokens[661].item_id = "flores-822"
tokens[661].token = "illa"
tokens[661].tag = "kn"
tokens[662].item_id = "flores-822"
tokens[662].token = "destinations"
tokens[662].tag = "en"
tokens[663].item_id = "flores-822"
tokens[663].token = "bagge"
tokens[663].tag = "kn"
tokens[664].item_id = "flores-822"
tokens[664].token = "expertise"
tokens[664].tag = "en"
tokens[665].item_id = "flores-822"
tokens[665].token = "hondirthare"
tokens[665].tag = "kn"
tokens[666].item_id = "flores-856"
tokens[666].token = "Itararigaagi"
tokens[666].tag = "kn"
tokens[667].item_id = "flores-856"
tokens[667].token = "oyyuvadu"
tokens[667].tag = "kn"
tokens[668].item_id = "flores-856"
tokens[668].token = "nimma"
tokens[668].tag = "kn"
tokens[669].item_id = "flores-856"
tokens[669].token = "baggage"
tokens[669].tag = "en"
tokens[670].item_id = "flores-856"
tokens[670].token = "gala"
tokens[670].tag = "u"
tokens[671].item_id = "flores-856"
tokens[671].token = "mele"
tokens[671].tag = "kn"
tokens[672].item_id = "flores-856"
tokens[672].token = "hecchu"
tokens[672].tag = "kn"
tokens[673].item_id = "flores-856"
tokens[673].token = "eccharavahisi"
tokens[673].tag = "kn"
tokens[674].item_id = "flores-856"
tokens[674].token = "adaralloo"
tokens[674].tag = "kn"
tokens[675].item_id = "flores-856"
tokens[675].token = "visheshavaagi"
tokens[675].tag = "kn"
tokens[676].item_id = "flores-856"
tokens[676].token = "antaraashtriya"
tokens[676].tag = "kn"
tokens[677].item_id = "flores-856"
tokens[677].token = "gadigalannu"
tokens[677].tag = "kn"
tokens[678].item_id = "flores-856"
tokens[678].token = "daatuttiruvaaga"
tokens[678].tag = "kn"
tokens[679].item_id = "flores-856"
tokens[679].token = "thumba"
tokens[679].tag = "kn"
tokens[680].item_id = "flores-856"
tokens[680].token = "eccharadindirabeku"
tokens[680].tag = "kn"
tokens[681].item_id = "flores-879"
tokens[681].token = "anek"
tokens[681].tag = "kn"
tokens[682].item_id = "flores-879"
tokens[682].token = "sarkargalu"
tokens[682].tag = "kn"
tokens[683].item_id = "flores-879"
tokens[683].token = "thamm"
tokens[683].tag = "kn"
tokens[684].item_id = "flores-879"
tokens[684].token = "deshake"
tokens[684].tag = "kn"
tokens[685].item_id = "flores-879"
tokens[685].token = "beti"
tokens[685].tag = "kn"
tokens[686].item_id = "flores-879"
tokens[686].token = "niduvavrige"
tokens[686].tag = "kn"
tokens[687].item_id = "flores-879"
tokens[687].token = "athva"
tokens[687].tag = "kn"
tokens[688].item_id = "flores-879"
tokens[688].token = "horhoguv"
tokens[688].tag = "kn"
tokens[689].item_id = "flores-879"
tokens[689].token = "nivasigalu"
tokens[689].tag = "kn"
tokens[690].item_id = "flores-879"
tokens[690].token = "halavaru"
tokens[690].tag = "kn"
tokens[691].item_id = "flores-879"
tokens[691].token = "rogagala"
tokens[691].tag = "kn"
tokens[692].item_id = "flores-879"
tokens[692].token = "lasike"
tokens[692].tag = "kn"
tokens[693].item_id = "flores-879"
tokens[693].token = "nidbekagutte"
tokens[693].tag = "kn"
tokens[694].item_id = "flores-983"
tokens[694].token = "hakki"
tokens[694].tag = "kn"
tokens[695].item_id = "flores-983"
tokens[695].token = "jwara"
tokens[695].tag = "kn"
tokens[696].item_id = "flores-983"
tokens[696].token = "athava"
tokens[696].tag = "kn"
tokens[697].item_id = "flores-983"
tokens[697].token = "adra"
tokens[697].tag = "kn"
tokens[698].item_id = "flores-983"
tokens[698].token = "munchina"
tokens[698].tag = "kn"
tokens[699].item_id = "flores-983"
tokens[699].token = "hesarada"
tokens[699].tag = "kn"
tokens[700].item_id = "flores-983"
tokens[700].token = "avian"
tokens[700].tag = "en"
tokens[701].item_id = "flores-983"
tokens[701].token = "influenza"
tokens[701].tag = "en"
tokens[702].item_id = "flores-983"
tokens[702].token = "vu"
tokens[702].tag = "u"
tokens[703].item_id = "flores-983"
tokens[703].token = "pakshi"
tokens[703].tag = "kn"
tokens[704].item_id = "flores-983"
tokens[704].token = "mattu"
tokens[704].tag = "kn"
tokens[705].item_id = "flores-983"
tokens[705].token = "sasthnigaleradakkvu"
tokens[705].tag = "kn"
tokens[706].item_id = "flores-983"
tokens[706].token = "sonku"
tokens[706].tag = "kn"
tokens[707].item_id = "flores-983"
tokens[707].token = "tagulbahudu"
tokens[707].tag = "kn"
tokens[708].item_id = "flores-1040"
tokens[708].token = "n"
tokens[708].tag = "u"
tokens[709].item_id = "flores-1040"
tokens[709].token = "speed"
tokens[709].tag = "en"
tokens[710].item_id = "flores-1040"
tokens[710].token = "adu"
tokens[710].tag = "kn"
tokens[711].item_id = "flores-1040"
tokens[711].token = "munche"
tokens[711].tag = "kn"
tokens[712].item_id = "flores-1040"
tokens[712].token = "iroda"
tokens[712].tag = "kn"
tokens[713].item_id = "flores-1040"
tokens[713].token = "productginta"
tokens[713].tag = "kn"
tokens[714].item_id = "flores-1040"
tokens[714].token = "thumba"
tokens[714].tag = "kn"
tokens[715].item_id = "flores-1040"
tokens[715].token = "fast"
tokens[715].tag = "en"
tokens[716].item_id = "flores-1040"
tokens[716].token = "irutthe"
tokens[716].tag = "kn"
tokens[717].item_id = "flores-1040"
tokens[717].token = "max"
tokens[717].tag = "en"
tokens[718].item_id = "flores-1040"
tokens[718].token = "theoretical"
tokens[718].tag = "en"
tokens[719].item_id = "flores-1040"
tokens[719].token = "throughput"
tokens[719].tag = "en"
tokens[720].item_id = "flores-1040"
tokens[720].token = "bandbitthu"
tokens[720].tag = "kn"
tokens[721].item_id = "flores-1040"
tokens[721].token = "Mbit"
tokens[721].tag = "kn"
tokens[722].item_id = "flores-1040"
tokens[722].token = "s"
tokens[722].tag = "u"
tokens[723].item_id = "flores-1040"
tokens[723].token = "aagide"
tokens[723].tag = "kn"
tokens[724].item_id = "flores-1095"
tokens[724].token = "ondu"
tokens[724].tag = "kn"
tokens[725].item_id = "flores-1095"
tokens[725].token = "sandarshanadalli"
tokens[725].tag = "kn"
tokens[726].item_id = "flores-1095"
tokens[726].token = "hosa"
tokens[726].tag = "kn"
tokens[727].item_id = "flores-1095"
tokens[727].token = "variety"
tokens[727].tag = "en"
tokens[728].item_id = "flores-1095"
tokens[728].token = "thumba"
tokens[728].tag = "kn"
tokens[729].item_id = "flores-1095"
tokens[729].token = "troublesome"
tokens[729].tag = "en"
tokens[730].item_id = "flores-1095"
tokens[730].token = "mattu"
tokens[730].tag = "kn"
tokens[731].item_id = "flores-1095"
tokens[731].token = "alarming"
tokens[731].tag = "en"
tokens[732].item_id = "flores-1095"
tokens[732].token = "agide"
tokens[732].tag = "kn"
tokens[733].item_id = "flores-1095"
tokens[733].token = "yake"
tokens[733].tag = "kn"
tokens[734].item_id = "flores-1095"
tokens[734].token = "andre"
tokens[734].tag = "u"
tokens[735].item_id = "flores-1095"
tokens[735].token = "marana"
tokens[735].tag = "kn"
tokens[736].item_id = "flores-1095"
tokens[736].token = "dara"
tokens[736].tag = "u"
tokens[737].item_id = "flores-1095"
tokens[737].token = "thumba"
tokens[737].tag = "kn"
tokens[738].item_id = "flores-1095"
tokens[738].token = "jasthi"
tokens[738].tag = "kn"
tokens[739].item_id = "flores-1095"
tokens[739].token = "ide"
tokens[739].tag = "u"
tokens[740].item_id = "flores-1095"
tokens[740].token = "anthu"
tokens[740].tag = "kn"
tokens[741].item_id = "flores-1095"
tokens[741].token = "avaru"
tokens[741].tag = "kn"
tokens[742].item_id = "flores-1095"
tokens[742].token = "heliddare"
tokens[742].tag = "kn"
tokens[743].item_id = "flores-1148"
tokens[743].token = "medicines"
tokens[743].tag = "en"
tokens[744].item_id = "flores-1148"
tokens[744].token = "sans"
tokens[744].tag = "u"
tokens[745].item_id = "flores-1148"
tokens[745].token = "frontiers"
tokens[745].tag = "en"
tokens[746].item_id = "flores-1148"
tokens[746].token = "ge"
tokens[746].tag = "u"
tokens[747].item_id = "flores-1148"
tokens[747].token = "vaktararada"
tokens[747].tag = "kn"
tokens[748].item_id = "flores-1148"
tokens[748].token = "richard"
tokens[748].tag = "u"
tokens[749].item_id = "flores-1148"
tokens[749].token = "veermen"
tokens[749].tag = "kn"
tokens[750].item_id = "flores-1148"
tokens[750].token = "helidaru"
tokens[750].tag = "kn"
tokens[751].item_id = "flores-1148"
tokens[751].token = "angola"
tokens[751].tag = "en"
tokens[752].item_id = "flores-1148"
tokens[752].token = "tanna"
tokens[752].tag = "kn"
tokens[753].item_id = "flores-1148"
tokens[753].token = "atyanta"
tokens[753].tag = "kn"
tokens[754].item_id = "flores-1148"
tokens[754].token = "hadagetta"
tokens[754].tag = "kn"
tokens[755].item_id = "flores-1148"
tokens[755].token = "sthitige"
tokens[755].tag = "kn"
tokens[756].item_id = "flores-1148"
tokens[756].token = "hoguttide"
tokens[756].tag = "kn"
tokens[757].item_id = "flores-1148"
tokens[757].token = "mattu"
tokens[757].tag = "kn"
tokens[758].item_id = "flores-1148"
tokens[758].token = "ide"
tokens[758].tag = "u"
tokens[759].item_id = "flores-1148"
tokens[759].token = "hadagetta"
tokens[759].tag = "kn"
tokens[760].item_id = "flores-1148"
tokens[760].token = "sthithiyalli"
tokens[760].tag = "kn"
tokens[761].item_id = "flores-1148"
tokens[761].token = "angola"
tokens[761].tag = "en"
tokens[762].item_id = "flores-1148"
tokens[762].token = "helidaru"
tokens[762].tag = "kn"
tokens[763].item_id = "flores-1148"
tokens[763].token = "endu"
tokens[763].tag = "kn"
tokens[764].item_id = "flores-1148"
tokens[764].token = "helidaru"
tokens[764].tag = "kn"
tokens[765].item_id = "flores-1153"
tokens[765].token = "maravu"
tokens[765].tag = "kn"
tokens[766].item_id = "flores-1153"
tokens[766].token = "shiligandradinda"
tokens[766].tag = "kn"
tokens[767].item_id = "flores-1153"
tokens[767].token = "sonkige"
tokens[767].tag = "kn"
tokens[768].item_id = "flores-1153"
tokens[768].token = "olagagide"
tokens[768].tag = "kn"
tokens[769].item_id = "flores-1153"
tokens[769].token = "mattu"
tokens[769].tag = "kn"
tokens[770].item_id = "flores-1153"
tokens[770].token = "adu"
tokens[770].tag = "kn"
tokens[771].item_id = "flores-1153"
tokens[771].token = "biluva"
tokens[771].tag = "kn"
tokens[772].item_id = "flores-1153"
tokens[772].token = "sannihita"
tokens[772].tag = "kn"
tokens[773].item_id = "flores-1153"
tokens[773].token = "apayadallide"
tokens[773].tag = "kn"
tokens[774].item_id = "flores-1153"
tokens[774].token = "endu"
tokens[774].tag = "kn"
tokens[775].item_id = "flores-1153"
tokens[775].token = "vadisuvudarinda"
tokens[775].tag = "kn"
tokens[776].item_id = "flores-1153"
tokens[776].token = "sarvajanika"
tokens[776].tag = "kn"
tokens[777].item_id = "flores-1153"
tokens[777].token = "arogyakke"
tokens[777].tag = "kn"
tokens[778].item_id = "flores-1153"
tokens[778].token = "apayavidede"
tokens[778].tag = "kn"
tokens[779].item_id = "flores-1153"
tokens[779].token = "endu"
tokens[779].tag = "kn"
tokens[780].item_id = "flores-1153"
tokens[780].token = "nagarada"
tokens[780].tag = "kn"
tokens[781].item_id = "flores-1153"
tokens[781].token = "amsterdam"
tokens[781].tag = "en"
tokens[782].item_id = "flores-1153"
tokens[782].token = "mattu"
tokens[782].tag = "kn"
tokens[783].item_id = "flores-1153"
tokens[783].token = "anne"
tokens[783].tag = "u"
tokens[784].item_id = "flores-1153"
tokens[784].token = "frank"
tokens[784].tag = "en"
tokens[785].item_id = "flores-1153"
tokens[785].token = "museum"
tokens[785].tag = "en"
tokens[786].item_id = "flores-1153"
tokens[786].token = "adhikarigalu"
tokens[786].tag = "kn"
tokens[787].item_id = "flores-1153"
tokens[787].token = "heluttare"
tokens[787].tag = "kn"
tokens[788].item_id = "flores-1272"
tokens[788].token = "akeya"
tokens[788].tag = "kn"
tokens[789].item_id = "flores-1272"
tokens[789].token = "innondu"
tokens[789].tag = "kn"
tokens[790].item_id = "flores-1272"
tokens[790].token = "spardhe"
tokens[790].tag = "kn"
tokens[791].item_id = "flores-1272"
tokens[791].token = "da"
tokens[791].tag = "u"
tokens[792].item_id = "flores-1272"
tokens[792].token = "giant"
tokens[792].tag = "en"
tokens[793].item_id = "flores-1272"
tokens[793].token = "slalom"
tokens[793].tag = "en"
tokens[794].item_id = "flores-1272"
tokens[794].token = "mahileyara"
tokens[794].tag = "kn"
tokens[795].item_id = "flores-1272"
tokens[795].token = "sitting"
tokens[795].tag = "en"
tokens[796].item_id = "flores-1272"
tokens[796].token = "groupnalli"
tokens[796].tag = "kn"
tokens[797].item_id = "flores-1272"
tokens[797].token = "hattene"
tokens[797].tag = "kn"
tokens[798].item_id = "flores-1272"
tokens[798].token = "sthanadalli"
tokens[798].tag = "kn"
tokens[799].item_id = "flores-1272"
tokens[799].token = "otada"
tokens[799].tag = "kn"
tokens[800].item_id = "flores-1272"
tokens[800].token = "samaya"
tokens[800].tag = "kn"
tokens[801].item_id = "flores-1272"
tokens[801].token = "dongide"
tokens[801].tag = "kn"
tokens[802].item_id = "flores-1272"
tokens[802].token = "mugisidalu"
tokens[802].tag = "kn"
tokens[803].item_id = "flores-1272"
tokens[803].token = "idu"
tokens[803].tag = "kn"
tokens[804].item_id = "flores-1272"
tokens[804].token = "prathama"
tokens[804].tag = "kn"
tokens[805].item_id = "flores-1272"
tokens[805].token = "sthana"
tokens[805].tag = "kn"
tokens[806].item_id = "flores-1272"
tokens[806].token = "pateda"
tokens[806].tag = "kn"
tokens[807].item_id = "flores-1272"
tokens[807].token = "Austrian"
tokens[807].tag = "en"
tokens[808].item_id = "flores-1272"
tokens[808].token = "Claudia"
tokens[808].tag = "en"
tokens[809].item_id = "flores-1272"
tokens[809].token = "Loshgintha"
tokens[809].tag = "kn"
tokens[810].item_id = "flores-1272"
tokens[810].token = "nimishagalashtu"
tokens[810].tag = "kn"
tokens[811].item_id = "flores-1272"
tokens[811].token = "nidhana"
tokens[811].tag = "kn"
tokens[812].item_id = "flores-1272"
tokens[812].token = "haagu"
tokens[812].tag = "kn"
tokens[813].item_id = "flores-1272"
tokens[813].token = "ombatenne"
tokens[813].tag = "kn"
tokens[814].item_id = "flores-1272"
tokens[814].token = "sthanadalli"
tokens[814].tag = "kn"
tokens[815].item_id = "flores-1272"
tokens[815].token = "mugisida"
tokens[815].tag = "kn"
tokens[816].item_id = "flores-1272"
tokens[816].token = "Hungaryya"
tokens[816].tag = "kn"
tokens[817].item_id = "flores-1272"
tokens[817].token = "Jangi"
tokens[817].tag = "kn"
tokens[818].item_id = "flores-1272"
tokens[818].token = "Danyikkintha"
tokens[818].tag = "kn"
tokens[819].item_id = "flores-1272"
tokens[819].token = "nimisha"
tokens[819].tag = "kn"
tokens[820].item_id = "flores-1272"
tokens[820].token = "nidhanavagide"
tokens[820].tag = "kn"
tokens[821].item_id = "flores-1279"
tokens[821].token = "Adagyu"
tokens[821].tag = "kn"
tokens[822].item_id = "flores-1279"
tokens[822].token = "driver"
tokens[822].tag = "en"
tokens[823].item_id = "flores-1279"
tokens[823].token = "talege"
tokens[823].tag = "kn"
tokens[824].item_id = "flores-1279"
tokens[824].token = "gambhira"
tokens[824].tag = "kn"
tokens[825].item_id = "flores-1279"
tokens[825].token = "gayagaladaru"
tokens[825].tag = "kn"
tokens[826].item_id = "flores-1279"
tokens[826].token = "sahiskondanu"
tokens[826].tag = "kn"
tokens[827].item_id = "flores-1335"
tokens[827].token = "Saarige"
tokens[827].tag = "kn"
tokens[828].item_id = "flores-1335"
tokens[828].token = "saadhanegala"
tokens[828].tag = "kn"
tokens[829].item_id = "flores-1335"
tokens[829].token = "korategala"
tokens[829].tag = "kn"
tokens[830].item_id = "flores-1335"
tokens[830].token = "hedarikeyinda"
tokens[830].tag = "kn"
tokens[831].item_id = "flores-1335"
tokens[831].token = "tandada"
tokens[831].tag = "kn"
tokens[832].item_id = "flores-1335"
tokens[832].token = "bembaligara"
tokens[832].tag = "kn"
tokens[833].item_id = "flores-1335"
tokens[833].token = "bembala"
tokens[833].tag = "kn"
tokens[834].item_id = "flores-1335"
tokens[834].token = "illade"
tokens[834].tag = "kn"
tokens[835].item_id = "flores-1335"
tokens[835].token = "muchchida"
tokens[835].tag = "kn"
tokens[836].item_id = "flores-1335"
tokens[836].token = "baagilugala"
tokens[836].tag = "kn"
tokens[837].item_id = "flores-1335"
tokens[837].token = "hinde"
tokens[837].tag = "kn"
tokens[838].item_id = "flores-1335"
tokens[838].token = "aatavaaduva"
tokens[838].tag = "kn"
tokens[839].item_id = "flores-1335"
tokens[839].token = "saadhyategalu"
tokens[839].tag = "kn"
tokens[840].item_id = "flores-1335"
tokens[840].token = "hechchaayitu"
tokens[840].tag = "kn"
tokens[841].item_id = "flores-1357"
tokens[841].token = "anthimavagi"
tokens[841].tag = "kn"
tokens[842].item_id = "flores-1357"
tokens[842].token = "keetagalu"
tokens[842].tag = "kn"
tokens[843].item_id = "flores-1357"
tokens[843].token = "damshekagalu"
tokens[843].tag = "kn"
tokens[844].item_id = "flores-1357"
tokens[844].token = "halligalu"
tokens[844].tag = "kn"
tokens[845].item_id = "flores-1357"
tokens[845].token = "mattu"
tokens[845].tag = "kn"
tokens[846].item_id = "flores-1357"
tokens[846].token = "pakshigalantha"
tokens[846].tag = "kn"
tokens[847].item_id = "flores-1357"
tokens[847].token = "halavaru"
tokens[847].tag = "kn"
tokens[848].item_id = "flores-1357"
tokens[848].token = "sanna"
tokens[848].tag = "kn"
tokens[849].item_id = "flores-1357"
tokens[849].token = "putta"
tokens[849].tag = "kn"
tokens[850].item_id = "flores-1357"
tokens[850].token = "hulugalannu"
tokens[850].tag = "kn"
tokens[851].item_id = "flores-1357"
tokens[851].token = "beteyaduva"
tokens[851].tag = "kn"
tokens[852].item_id = "flores-1357"
tokens[852].token = "sanna"
tokens[852].tag = "kn"
tokens[853].item_id = "flores-1357"
tokens[853].token = "bekkugalide"
tokens[853].tag = "kn"
tokens[854].item_id = "flores-1357"
tokens[854].token = "saku"
tokens[854].tag = "kn"
tokens[855].item_id = "flores-1357"
tokens[855].token = "bekkugalu"
tokens[855].tag = "kn"
tokens[856].item_id = "flores-1357"
tokens[856].token = "serikondu"
tokens[856].tag = "kn"
tokens[857].item_id = "flores-1522"
tokens[857].token = "ne"
tokens[857].tag = "u"
tokens[858].item_id = "flores-1522"
tokens[858].token = "shatamanada"
tokens[858].tag = "kn"
tokens[859].item_id = "flores-1522"
tokens[859].token = "research"
tokens[859].tag = "en"
tokens[860].item_id = "flores-1522"
tokens[860].token = "anusaraka"
tokens[860].tag = "kn"
tokens[861].item_id = "flores-1522"
tokens[861].token = "anuvanshika"
tokens[861].tag = "kn"
tokens[862].item_id = "flores-1522"
tokens[862].token = "badalavaneya"
tokens[862].tag = "kn"
tokens[863].item_id = "flores-1522"
tokens[863].token = "eradu"
tokens[863].tag = "kn"
tokens[864].item_id = "flores-1522"
tokens[864].token = "layers"
tokens[864].tag = "en"
tokens[865].item_id = "flores-1522"
tokens[865].token = "ide"
tokens[865].tag = "u"
tokens[866].item_id = "flores-1522"
tokens[866].token = "antha"
tokens[866].tag = "kn"
tokens[867].item_id = "flores-1522"
tokens[867].token = "thorside"
tokens[867].tag = "kn"
tokens[868].item_id = "flores-1522"
tokens[868].token = "adu"
tokens[868].tag = "kn"
tokens[869].item_id = "flores-1522"
tokens[869].token = "vyakta"
tokens[869].tag = "kn"
tokens[870].item_id = "flores-1522"
tokens[870].token = "mattu"
tokens[870].tag = "kn"
tokens[871].item_id = "flores-1522"
tokens[871].token = "avyakta"
tokens[871].tag = "kn"
tokens[872].item_id = "flores-1651"
tokens[872].token = "Vishaya"
tokens[872].tag = "kn"
tokens[873].item_id = "flores-1651"
tokens[873].token = "siddantagalu"
tokens[873].tag = "kn"
tokens[874].item_id = "flores-1651"
tokens[874].token = "manushyanige"
tokens[874].tag = "kn"
tokens[875].item_id = "flores-1651"
tokens[875].token = "yava"
tokens[875].tag = "kn"
tokens[876].item_id = "flores-1651"
tokens[876].token = "vishaya"
tokens[876].tag = "kn"
tokens[877].item_id = "flores-1651"
tokens[877].token = "ishtavagutte"
tokens[877].tag = "kn"
tokens[878].item_id = "flores-1651"
tokens[878].token = "athava"
tokens[878].tag = "kn"
tokens[879].item_id = "flores-1651"
tokens[879].token = "kenakutte"
tokens[879].tag = "kn"
tokens[880].item_id = "flores-1651"
tokens[880].token = "enbuddhannu"
tokens[880].tag = "kn"
tokens[881].item_id = "flores-1651"
tokens[881].token = "kanduhidiyalu"
tokens[881].tag = "kn"
tokens[882].item_id = "flores-1651"
tokens[882].token = "prayatnisuthave"
tokens[882].tag = "kn"
`````

## Not dumped (item-level, binary or too large; path and size only)

- `results/h_hindi/natural_drafts.DONE`: .DONE file, 512 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/gemma4-e2b__itrans.parquet`: .parquet file, 14,617 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/gemma4-e2b__lossy.parquet`: .parquet file, 14,540 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/gemma4-e2b__native.parquet`: .parquet file, 14,422 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/gemma4-e2b__natural.parquet`: .parquet file, 14,470 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen2.5-1.5b__itrans.parquet`: .parquet file, 14,535 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen2.5-1.5b__lossy.parquet`: .parquet file, 14,556 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen2.5-1.5b__native.parquet`: .parquet file, 14,763 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen2.5-1.5b__natural.parquet`: .parquet file, 14,552 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3-1.7b__itrans.parquet`: .parquet file, 14,664 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3-1.7b__lossy.parquet`: .parquet file, 14,639 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3-1.7b__native.parquet`: .parquet file, 14,833 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3-1.7b__natural.parquet`: .parquet file, 14,661 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3.5-2b__itrans.parquet`: .parquet file, 14,350 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3.5-2b__lossy.parquet`: .parquet file, 14,267 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3.5-2b__native.parquet`: .parquet file, 14,430 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/qwen3.5-2b__natural.parquet`: .parquet file, 14,333 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/sarvam-1__itrans.parquet`: .parquet file, 14,514 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/sarvam-1__lossy.parquet`: .parquet file, 14,507 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/sarvam-1__native.parquet`: .parquet file, 14,491 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sentiment/sarvam-1__natural.parquet`: .parquet file, 14,547 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/gemma4-e2b__itrans.parquet`: .parquet file, 122,140 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/gemma4-e2b__lossy.parquet`: .parquet file, 122,018 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/gemma4-e2b__native.parquet`: .parquet file, 120,095 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/gemma4-e2b__natural.parquet`: .parquet file, 35,239 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen2.5-1.5b__itrans.parquet`: .parquet file, 119,124 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen2.5-1.5b__lossy.parquet`: .parquet file, 119,324 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen2.5-1.5b__native.parquet`: .parquet file, 120,558 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen2.5-1.5b__natural.parquet`: .parquet file, 35,183 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3-1.7b__itrans.parquet`: .parquet file, 121,889 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3-1.7b__lossy.parquet`: .parquet file, 121,845 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3-1.7b__native.parquet`: .parquet file, 122,153 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3-1.7b__natural.parquet`: .parquet file, 35,429 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3.5-2b__itrans.parquet`: .parquet file, 115,741 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3.5-2b__lossy.parquet`: .parquet file, 116,376 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3.5-2b__native.parquet`: .parquet file, 118,203 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/qwen3.5-2b__natural.parquet`: .parquet file, 34,332 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/sarvam-1__itrans.parquet`: .parquet file, 116,643 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/sarvam-1__lossy.parquet`: .parquet file, 117,312 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/sarvam-1__native.parquet`: .parquet file, 119,130 bytes (binary or per-item data, not dumped)
- `results/h_hindi/scores/sib/sarvam-1__natural.parquet`: .parquet file, 34,826 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/hindi/gemma4-e2b__natural1004.parquet`: .parquet file, 119,867 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/hindi/qwen3-1.7b__natural1004.parquet`: .parquet file, 120,616 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/hindi/qwen3.5-2b__natural1004.parquet`: .parquet file, 116,329 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/hindi/sarvam-1__natural1004.parquet`: .parquet file, 117,528 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/kannada/gemma4-e2b__natural1004.parquet`: .parquet file, 121,085 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/kannada/qwen3-1.7b__natural1004.parquet`: .parquet file, 121,103 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/kannada/qwen3.5-2b__natural1004.parquet`: .parquet file, 116,028 bytes (binary or per-item data, not dumped)
- `results/h1lf/scores/kannada/sarvam-1__natural1004.parquet`: .parquet file, 117,257 bytes (binary or per-item data, not dumped)
- `results/h1lf/sib1004_drafts.DONE`: .DONE file, 641 bytes (binary or per-item data, not dumped)
- `results/k3b_hi/drafts.jsonl`: .jsonl file, 170,857 bytes (binary or per-item data, not dumped)

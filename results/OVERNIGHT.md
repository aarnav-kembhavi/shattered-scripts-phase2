# Overnight run, 2026-10-16 (about 02:15–03:25 IST)

No LLM API calls were made, and no download was larger than 5 GB (SIB-200 Kannada and English: 0.8 MB). The 12:45 M4c
chain was not touched.

## 1. M4b mapping robustness check: done
Registered before running in RESULTS.md. Script `scripts/m4b_robustness.py`; outputs
`results/m4b_robustness/{summary.csv, verdict.json, items.npz}` and `results/m4b_robustness.log`. Commits e190b90
(registration), 3399027 (results).

| model | M4b status | wide-grid ridge: gap [CI], status | PCA Procrustes: gap [CI], status |
|---|---|---|---|
| Qwen2.5 | closes | −0.012 [−0.043, 0.019] closes | −0.231 [−0.269, −0.194] closes |
| Qwen3.5 | persists | 0.477 [0.445, 0.509] persists | 0.492 [0.460, 0.524] persists |
| Sarvam-1 | persists | 0.518 [0.487, 0.551] persists | 0.473 [0.442, 0.505] persists |
| Gemma 4 | persists | 0.504 [0.473, 0.536] persists | 0.403 [0.371, 0.433] persists |

- **Verdict: the M4b result is robust by the registered criterion.** Every model keeps its status under both
  alternative maps, and strong H1 stays inconclusive.
- **Wide-grid ridge reproduces M4b exactly.** At the chosen layers, alpha was inside the old grid.
- **Procrustes always chose k = 512, the top of its grid.** With about 800 fitting rows per fold, k cannot go much
  higher.
- **Mapped ITRANS is higher under Procrustes for Gemma 4 and Sarvam-1.** Gemma 4 reaches 0.583, again at layer 0;
  Sarvam-1 reaches 0.449.
- **Qwen2.5 native is not a rotation of English.** It reaches only 0.219 under Procrustes, against 0.517 with ridge.

## 2. E0c SIB-200: verified and registered; scoring INTERRUPTED (not restarted)
- **Dataset:** HF `Davlan/sib200`, revision 38977a6, CC-BY-SA 4.0 per the card YAML (the card's prose says
  "CC 4.0 Commercial"), not gated. Added to DATA_CARD.md.
- **Match with FLORES+:**
  - `index_id` is the 0-based position in FLORES dev + devtest.
  - All 1,004 Kannada and all 1,004 English sentences equal our FLORES+ text at that position after NFC.
  - Labels and IDs agree across the two languages. See `results/e0c_sib/verify.json`.
  - 515 of the 1,004 sentences are in the M4b test half; these are the P-b sentences.
- **Registered before scoring** (RESULTS.md, commit ba54695): P-a and P-b, with exact rules, the template
  `e0_sib_v1`, the 7 label words, and the E0b calibration and fallback rule.
- **Pilot** (30 items × 4 forms, timing only, `results/e0c_sib/scores_pilot/`): about 0.4 s per item per form on
  Qwen2.5 and 0.8 s on Gemma 4.
- **Full scoring.** `scripts/e0c_sib.py score` started at about 02:55 IST.
  - At about 03:20 IST, Claude Code stopped it because the system was critically low on memory. The cause was not
    this job: a separate python process from another project (`C:\PROJECTS\ISM`, `gatelog_check.py`) was using
    10.8 GB.
  - Per the harness rule, I did not restart it.
  - **Finished and cached:** Qwen2.5 in all 4 forms (English 344 s, native 526 s, ITRANS 393 s, lossy 375 s) and
    Qwen3.5 English (672 s). They are in `results/e0c_sib/scores/`.
  - **Missing:** 15 model × form pairs (Qwen3.5 ×3, Sarvam-1 ×4, Gemma 4 ×4, Qwen3 ×4), about 2.5–3 h of GPU.
  - Scoring resumes from the cache: `python scripts/e0c_sib.py score`, then `python scripts/e0c_sib.py analyse`.
- **No E0c accuracies, P-a or P-b verdicts exist yet.** I have not looked at the partial scores.

## 3. Kanglish annotation (your mid-night message): set up and registered; drafting queued
- **Registered before any draft or scoring** (RESULTS.md, commit d21d633): K1, K2a/K2b and K3, with exact
  decision rules, plus the language tagger used for the English word share. The tagger is fixed in
  `src/shattered/translit/codemix.py`: wordfreq top 50k English vs lossy-romanized top 50k Kannada Wikipedia words.
- **Items:** `data/annotation/items_v1.jsonl`, 500 items.
  - The 200 E0 sentiment items.
  - 300 FLORES+ sentences (seed 0) drawn from the 515 that are in SIB-200 and in the M4b test half.
  - 100 items marked for double annotation (seed 1): 38 sentiment, 62 FLORES.
- **Kanglish prompt:** `src/shattered/llm/templates/kanglish_v1.txt`.
- **Annotation page:** `annotation/template_v1.html`. `python scripts/k_annotation.py page` writes
  `annotation/annotate_v1.html` with the drafts embedded.
  - It is one offline HTML file showing native Kannada and English, with two editable boxes (natural and Kanglish),
    each with naturalness 1–5 and meaning yes/no.
  - It rewrites the annotator's CSV after every save (Chrome/Edge file API). There is a localStorage backup and a
    Download CSV fallback for other browsers.
  - It has a "Second annotator (100 items)" mode.
  - Checked: JS syntax with node, and a CSV round trip with quotes, newlines and Kannada. Not yet opened in a browser.
- **Agreement:** `python scripts/k_annotation.py agreement` computes Cohen's kappa (meaning) and quadratic-weighted
  kappa (naturalness) once two annotators have finished the 100 double items. The results go to
  `results/k_annotation/agreement.json`.
- **Gemini quota needed**, counted from the cache with no calls (`k_annotation.py plan`):
  - 800 first-attempt requests in total. 67 are already cached, and the E0 sentiment natural drafts are reused.
  - Of the 233 natural drafts still needed, the M4c chain will make 61 itself, since those sentences are in its
    sample.
  - That leaves about **672 calls (172 natural + 500 Kanglish), plus about 5% retries ≈ 700**.
  - The free tier stopped us at 501–502 requests a day (`cache/llm_cache.sqlite`, usage table: 2026-10-07 and
    2026-10-14).
  - M4c uses about 400 calls today, which leaves about 100. So drafting needs **3 quota days: 10-16 (leftover),
    10-17 and 10-18**, and the annotation page can be built on 2026-10-18.
- **Chain:** `scripts/k_chain.sh`, status in `results/CHAIN_STATUS_KANGLISH.md`.
  - It waits until the M4c chain reports DONE or FAILED, then drafts.
  - On a quota stop it resumes the next day at 12:45 IST, for at most 6 days. Then it builds the page.

## Background jobs: what is alive
- Claude Code's low-memory reaper reported all four background tasks killed at about 03:20. Checked afterwards: the
  two chain **shells survived** (Git Bash processes, still sleeping).
  - `scripts/m4c_chain.sh 2026-10-16` (pid 1100) is still WAITING for 12:45 and will run as planned.
  - `scripts/k_chain.sh` (pid 1751) is still WAITING for M4c.
  - Their heartbeats in `results/CHAIN_STATUS*.md` show they are alive. A heartbeat older than about 20 minutes
    means a chain has died.
- **Risk for 12:45 onward:** the M4c forward step loads each model; for Gemma 4 that includes about 4.7 GB of
  per-layer embeddings in RAM. If the other project's 10.8 GB process is still running, free RAM (3.7 GB at 03:25)
  may not be enough.
- **Only E0c scoring is actually dead.** It needs a restart from you.

## Blocked / needs you
1. **E0c scoring:** restart when memory allows. It resumes from the cache; about 2.5–3 h, then `analyse`.
2. **The other project's 10.8 GB python process** (`C:\PROJECTS\ISM`). I left it alone; it is what pushed memory
   over.
3. **Annotation design choice to confirm:** ratings are of the Gemini draft as shown, before correction, and the
   primary annotator's corrections define the human-corrected forms. Say if you meant ratings of the corrected text.

## Correction (2026-10-17, 01:55 IST)
The "Background jobs" section above is wrong after 11:40 IST on 10-16:
- **Both chain shells died** around 11:40 IST on 2026-10-16, before the 12:45 start. Their last heartbeats were
  10-16 11:40:04 (`m4c_chain.sh`) and 11:39:30 (`k_chain.sh`). They were most likely killed when the Claude Code
  session ended.
- **M4c never ran.** There is no `results/m4c_natural.log`, and the cache's usage table shows no Gemini request on
  2026-10-16.
- **No Kanglish draft exists.** There is no `data/annotation/drafts_v1.jsonl`.
- **The status files were misleading.** Both still said WAITING. From 2026-10-17, chains run detached from Claude Code
  (Windows Task Scheduler), compute dates and quota resets themselves, and a detached watcher marks any status whose
  heartbeat is older than 20 minutes as DEAD.
- **The ISM process was no longer running** at 01:51 IST on 10-17 (16.9 GB RAM free).

# CLEANUP_PLAN.md (Phase 1: inventory only; nothing has been moved, deleted or edited)

Written 2026-10-29. Sizes from `du` (MB, rounded) and `find -printf %s`. "Paper dependency" comes from `build/anon_trace.json` (files read by
make_tables, make_figures and check_numbers; generated 2026-10-27, so it predates the K2b and H1-LF additions, which I added by hand
from the scripts) plus a grep of the paper scripts. Regeneration times are **estimates from timing lines in RESULTS.md**, not measurements.

## 0. Protected throughout (the K3b-hi chain is running; scheduled task `ShatteredScripts_k3bhi`)

Not touched in either phase until the chain reports DONE: `scripts/k3bhi_chain.sh`, `scripts/chainlib.sh`, `scripts/k3b_dakshina.py`,
`scripts/chain_watch.sh`, `scripts/detach.ps1`, `scripts/hidden.vbs`, `results/k3b_hi/`, `results/CHAIN_STATUS_K3BHI.md`, `results/k3bhi.log`,
`results/chain_watch.log`, `cache/llm_cache.sqlite`, `src/`, `configs/`, `.venv/`, `data/raw/dakshina*`, `data/annotation/`. Also never touched:
`RESULTS.md`, `DATA_CARD.md`, `CLAUDE.md`, `annotation/`, every registered prediction.

## 1. Total size

| | Before | After (proposed) |
|---|---|---|
| Working tree incl. `.venv` | about 34.7 GB | about 27.5 GB |
| of which `.venv` (untouched) | 5.0 GB | 5.0 GB |
| `.git` | 180 MB | 180 MB (history is not rewritten; see 6.4) |
| Moved out of the repo to the archive folder | | about 7.2 GB (mostly E5 resume and snapshot checkpoints) |
| Deleted outright | | under 20 MB (caches such as `__pycache__`, `.pytest_cache`) |

## 2. Every top-level folder

| Path | Size | What it is | Made by | Paper / check_numbers depends | Git tracked | Class |
|---|---|---|---|---|---|---|
| `cache/` | 16,520 MB | activations plus the LLM response cache | forward-pass scripts; `shattered.llm.cache` | indirectly (see 3) | no (`.gitignore`) | see 3 |
| `checkpoints/` | 7,554 MB | E5 tiny-GPT training checkpoints | `scripts/e05_pretrain.py` | final weights feed `results/m1_tiny_mdl` (used by the paper) | no | see 4 |
| `data/` | 5,364 MB | raw downloads (2.8 GB), processed (2.5 GB, mostly E5 token arrays), annotation (2 MB) | download scripts; `e05_pretrain.py prepare`; annotation pipeline | processed natural-romanization files and `data/annotation/` yes | 30 files (small ones only) | see 5 |
| `.venv/` | 5,031 MB | Python environment | `uv` | no | no | KEEP, untouched |
| `results/` | 183 MB | one folder per experiment, plus loose logs and CHAIN_STATUS files | all analysis scripts | yes (28 folders) | 688 files | see 6 |
| `build/` | 12 MB | anonymized package builder output | `scripts/anon_package.py` | no | no (`build/` ignored) | REGENERABLE (rebuilt at freeze) |
| `paper/` | 5 MB | LaTeX, generated tables and figures, bib, check scripts | by hand and `paper/scripts/` | is the paper | 165 files | KEEP (see 7) |
| `annotation/` | 3 MB | annotation templates, distributed workbooks, instructions, annotator A results | `scripts/k_package.py`, `k_xlsx.py`, `merge_xlsx.py` | A's results via `data/annotation/verified_A_v1.jsonl` | 28 files | KEEP (never touched) |
| `scripts/` | 2 MB, 84 files | experiment and chain scripts | by hand | yes, many (imports) | 83 | see 8 |
| `src/shattered/` | 1 MB | the library | by hand | yes | 52 | KEEP |
| `docs/` | 2 MB | BRIEF.md, prereg drafts, one reference PDF (ignored) | by hand | no | 4 | KEEP |
| `tests/`, `configs/`, `notebooks/` | about 1 MB each | unit tests, run configs, one Kaggle notebook | by hand | configs yes | tracked | KEEP (notebook is dead since Kaggle was dropped: ARCHIVE) |
| root files | | `RESULTS.md`, `DATA_CARD.md`, `CLAUDE.md`, `README.md`, `pyproject.toml`, `requirements.*`, `.env*`, `.gitignore`, `.gitattributes` | | RESULTS and DATA_CARD yes | tracked except `.env` | KEEP |
| `.pytest_cache/`, `__pycache__/` (14 dirs outside `.venv`) | under 2 MB | caches | tools | no | no | DELETE |

## 3. `cache/` (16.5 GB, not tracked; REGENERABLE items are never deleted)

| Path | Size | What | Made by | Used by | Class | Time to regenerate (estimate) |
|---|---|---|---|---|---|---|
| `cache/llm_cache.sqlite` | 11 MB | every Gemini and Groq response (drafts, back-translation) | LLMClient | all draft steps; the drafts cannot be re-bought quickly (quota) | **KEEP, never delete** | days of Gemini quota |
| `cache/activations/m14full/` | 14,194 MB (12 big files of 0.9 to 1.25 GB: english, native, itrans per model; 919 MB of 500-sentence files) | sentence and word vectors per model and form | `m14_full.py`, `l_ladder.py`, `m4c_natural_flores.py`, `v_dbl.py`, `v_ver.py` | `m4b_mapping`, `m4c_curves`, `ep_*`, K2b (`english.npz`) analyses | REGENERABLE | about 2 to 3 h GPU for all four models, one model load at a time (RESULTS.md: 4 to 15 min per model and form) |
| `cache/activations/h_hindi/` | 1,083 MB | Hindi and Kannada 500-sentence vectors (H1) | `h_hindi.py` | H1 retrieval | REGENERABLE | about 1 h |
| `cache/activations/nc1/` | 603 MB | NC1 forced-segmentation vectors | `nc1.py` | NC1 retrieval | REGENERABLE | about 1 h |
| `cache/activations/m14/` | 410 MB | M14 pilot (Qwen2.5 only, `*_w50_s50_o20.npz`) | `m14_pilot.py` | nothing (superseded by `m14full`) | **ARCHIVE** | not needed |
| `cache/activations/m14smoke/` | 222 MB | smoke test of `m14_full.py` (Gemma 4) | `m14_full.py --smoke` | nothing | **ARCHIVE** | not needed |

## 4. `checkpoints/e05/` (7,554 MB, not tracked)

| Path | Size | What | Used by | Class |
|---|---|---|---|---|
| `run_v*_s*/final.safetensors` (18 files) | about 1,004 MB | final weights of the 18 E5 runs | `m1_tiny_mdl.py`, `m1_tiny_probes.py`, `e05_pretrain.py` (paper §4) | **REGENERABLE (keep in place)**; E5 full grid about 8.3 h GPU (RESULTS.md, pilot gate) |
| `run_v*_s*/last.pt` (18 files) | 3,010 MB | optimizer and resume state | `train.py` resume only; all runs completed | **ARCHIVE** |
| `run_v*_s*/snapshot_step*.safetensors` (54 files) | 3,010 MB | mid-training weights | produced by `train.py`; nothing downstream reads them | **ARCHIVE** |
| `pilot_v256_s0/`, `pilot_v16384_s0/` | 531 MB | E5 pilot runs (their record is `results/e05_pretrain/pilot_*`) | nothing | **ARCHIVE** |

## 5. `data/` (5,364 MB)

| Path | Size | What | Tracked | Class |
|---|---|---|---|---|
| `data/raw/tinystories` | 2,147 MB | TinyStories V2 text | no | REGENERABLE (download; needed only to rerun E5 `prepare`) |
| `data/raw/wikipedia_en`, `wikipedia_kn` | 401 + 141 MB | Wikipedia dumps (word frequencies, Kannada word list) | no | REGENERABLE (download) |
| `data/raw/flores200`, `flores_plus`, `sib200`, `indicsentiment`, `indicxnli`, `xnli`, `dakshina`, `dakshina_official` | 162 MB together | evaluation data | no | REGENERABLE; **keep in place** (Dakshina is used by the running K3b-hi) |
| `data/processed/e05/train_*_400000000.npy` (7 files) | 2,482 MB | tokenized TinyStories per vocabulary | no | REGENERABLE (about 30 to 60 min CPU; estimate) |
| `data/processed/natural_*_v1.jsonl`, `kn_wiki_wordfreq.parquet` | 30 MB | Gemini drafts, word list | 6 tracked; **`natural_sib1004_{kn,hi}_v1.jsonl` are NOT tracked** | KEEP; track the two SIB-1004 files (see 6.3) |
| `data/annotation/` | 2 MB | items, drafts, verified A | tracked | KEEP, never touched |

## 6. `results/` (183 MB; 40 folders, 28 of them read by the paper scripts)

6.1 Folders (KEEP unless stated; sizes are small; "paper" means a result file is read by make_tables, make_figures or check_numbers):

| Folder | Size | Paper | Tracked | Class |
|---|---|---|---|---|
| `k12` | 124 MB (121 MB is `vectors/*.npz`) | yes | all 61 | KEEP the CSVs; the 4 npz vectors are REGENERABLE (`k_k12.py forward`, about 40 min): untrack them (`git rm --cached`), keep on disk |
| `m14_full` | 15 MB | yes | yes (incl. 16 small npz) | KEEP |
| `m1_tiny_mdl` | 10 MB | yes | yes (18 npz) | KEEP |
| `e01_cost`, `e01_cost_flores_plus` | 6.6 MB each | no (RESULTS.md context; they differ, not duplicates) | yes | KEEP |
| `ep_robust`, `ep1`, `ep2`, `e0c_sib`, `e0b_familiarity`, `e0b_natural_check`, `e05_pretrain`, `h1lf`, `v_dbl`, `v_ver`, `nc1`, `nc1_posthoc`, `l_ladder`, `l_ladder_posthoc`, `h_hindi`, `m4b_mapping`, `m4b_robustness`, `m4b_surface`, `m4c_*`, `matched`, `codemix_check`, `k3b`, `k_verified`, `e00_gate`, `e02_translit`, `english_share` | under 4 MB each | yes (all but `m4b_surface`/`l_ladder_posthoc`/`english_share`, which RESULTS.md cites) | mostly; **untracked pieces: `h_hindi/scores/`, `h_hindi/natural_drafts.DONE`, `k3b/{drafts.jsonl, chrf.json, stats.csv, verdict.json}`, `nc1/scores/`** | KEEP; track the missing pieces |
| `k3b_hi` | 0.4 MB | not yet | 1 file | KEEP, **protected** (running) |
| `e09_romanize` | 0.26 MB | no (E9 dropped; negative result is in RESULTS.md) | yes | KEEP `savings.csv`, `savings.json`, `best_schemes.json`; ARCHIVE `search_jobs.json`, `capitals.json`, `schemes.md` (search intermediates) |
| `m14_smoke`, `m14_pilot`, `m4b_mapping_pilot_qwen25`, `e0c_sib/scores_pilot` | 0.3 + 0.06 + 0.03 + 0.12 MB | no | partly | **ARCHIVE** |

6.2 Loose files in `results/` (about 14 `CHAIN_STATUS_*.md` and 30 `*.log`): finished chains' status and logs are ARCHIVE
(`CHAIN_STATUS` for EP, EPR, E0C, H1LF, HDRAFTS, HGPU, K12FULL, K12PILOT, KANGLISH, LADDER, NC1, VVER and the generic `CHAIN_STATUS.md`; logs
for finished experiments, `detach_test.log`, pilot logs). Their final state is summarized in RESULTS.md. **KEEP in place:**
`CHAIN_STATUS_K3BHI.md`, `k3bhi.log`, `chain_watch.log`. **Prerequisite for moving a CHAIN_STATUS file:** the 11 finished scheduled tasks
re-run their chain at logon unless the status says DONE; moving the file would re-run it. Phase 2 therefore unregisters the 11 finished
`ShatteredScripts_*` tasks first (everything except `k3bhi`; `watch` after K3b-hi is DONE).

6.3 **Found while inventorying (needs fixing whatever else you decide):** `git status` shows 41 untracked, non-ignored paths: 27 are logs and chain status files (6.2), the rest matter for reproducibility (the two SIB-1004 draft files, `results/h_hindi/scores/` and `natural_drafts.DONE`, `results/nc1/scores/`, `results/k3b/*`, `results/k3b_hi/*` (protected until DONE) and `results/m14_smoke/` (to archive)), among them
`data/processed/natural_sib1004_{kn,hi}_v1.jsonl` (the Gemini drafts behind H1-LF), `results/k3b/*`, `results/h_hindi/scores/`. Phase 2 commits
them (the K3b-hi outputs are committed only after the chain is DONE).

6.4 `.git` is 180 MB because 41 tracked npz files (about 140 MB) are in history. I do **not** propose rewriting history (it would change commit
hashes cited in RESULTS.md provenance). Untracking the four `k12/vectors` files stops the growth only.

## 7. `paper/` (KEEP)

Generated per-section `NUMBERS_*.md`, `MISSING.md`, `BIB_REPORT.md`, `bib_fetched/` (60 files) stay. `paper/build/` is ignored. Figures: only
`ep2_recovery_curves` and `F_alignment_curves_2009` are included by the paper. The other 13 figure sets (28 files, a few MB: F1, F1b, F1c, F6,
F6b, F6c, F8, `F_e05_bpb_vs_tpw`, `F_m14_*`, `F_alignment_curves`, `ep1_*`, `ep2_recovery_main`) are **ARCHIVE** (regenerable from
`src/shattered/plots`). `paper/references.bib` is stale (only `OUTLINE.md` mentions it): **ARCHIVE**; `refs_original.bib` and `refs.bib` stay.

## 8. `scripts/` (84 files)

**Do not reorganize into `scripts/active/` and `scripts/archive/`.** 31 scripts do `sys.path.insert(scripts/)` and 20 modules are imported by others
(`l_ladder` by 18, `e0b_familiarity` by 14, `m4b_mapping` 14, `m14_full` 12, `m4c_natural_flores` 10, `english_share` 7); 33 script paths are hard-coded in the
chains, the paper scripts and `anon_package.py`; and the running chain calls `scripts/k3b_dakshina.py` after each quota reset. A move would need about 70 path
edits and cannot be done while K3b-hi runs. Proposal: keep `scripts/` flat and document it in `README.md` (a table: script, experiment, outputs).
Only dead scripts leave (to the archive folder, mirrored path `scripts/...`):

| Script | Why |
|---|---|
| `after_e5.sh`, `detach_test.sh`, `xlshot.ps1`, `env_check.py` | one-off helpers |
| `e00_candidates.py`, `e09_capitals.py`, `e09_eval.py`, `e09_search.py`, `m1_patchscopes.py` | dead experiments (E9 dropped; Patchscopes not in the paper; nothing imports them except each other) |
| `m14_pilot.py`, `k12_pilot_chain.sh`, `e0b_check_sheet.py` | pilots and one-off checks (outputs are archived or recorded in RESULTS.md) |

Everything else is KEEP (it produced a result in RESULTS.md or is imported). `scripts/__pycache__` DELETE.

## 9. Proposed layout (no path changes needed for the paper or check_numbers)

```
shattered-scripts/
  README.md        map + how to rebuild the paper and rerun each experiment (new)
  RESULTS.md  DATA_CARD.md  CLAUDE.md  CLEANUP_PLAN.md -> docs/ after approval
  paper/           unchanged (main.tex, sections/, tables/, figures/ [2 used], scripts/, refs.bib)
  src/shattered/   unchanged
  scripts/         flat, unchanged paths; archived scripts removed
  results/<experiment>/   unchanged; status files and logs of finished chains removed
  data/{raw,processed,annotation}   unchanged
  cache/           llm_cache.sqlite + activations/{m14full,h_hindi,nc1}
  checkpoints/e05/run_v*_s*/final.safetensors only
  annotation/      unchanged
  docs/            BRIEF.md, drafts/, papers/, CLEANUP_PLAN.md
  tests/ configs/  unchanged
Archive (outside the repo): C:\PROJECTS\PROMPT\shattered-scripts-archive\ (mirrored paths) + MANIFEST.md
```
The only code path changes: none in `src/`, `paper/` or `check_numbers`. `.gitignore` gains `results/k12/vectors/`, `results/*.log`, `results/CHAIN_STATUS*.md`,
`**/__pycache__/`, `.pytest_cache/`, `build/`. `README.md` is rewritten.

## 10. Decisions needed from you before Phase 2

1. **Scripts layout:** keep `scripts/` flat (recommended, reasons in 8), or do the `active/archive` split with about 70 path edits after K3b-hi finishes.
2. **Archive E5 `last.pt` (3.0 GB), mid-training snapshots (3.0 GB) and the two pilot checkpoints (0.5 GB):** all 18 runs are complete and only `final.safetensors` is read.
   They are moved, not deleted, so anything can come back.
3. **Archive the 13 figure sets not in the paper** and `paper/references.bib`.
4. **Unregister the 11 finished scheduled tasks** (so moving their status files cannot re-run them).
5. **Commit the untracked result and data files** listed in 6.3, and untrack `results/k12/vectors/*.npz`.
6. History rewrite: not proposed.

Verification planned after Phase 2: paper build 0 errors; `check_numbers` on all 12 sections with 0 mismatches; one analysis per experiment rerun from the
cleaned repo (`k_k12.py analyse`, `h1lf.py analyse1`, `ep_robust.py` analysis step, `l_ladder.py` analysis, `nc1.py` analysis, `m4b_mapping.py`, E5 `e05_analysis.py`,
`m1_tiny_mdl.py` analysis, `v_ver.py` analysis); the anonymized package rebuilt (0 identifying hits). Nothing GPU-bound is rerun.

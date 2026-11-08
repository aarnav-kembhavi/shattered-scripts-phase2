# BT: Back-translation comprehension gap (large model) (Phase 1)

Source: RESULTS.md entries (verbatim) and result files (paths given with every file). No interpretation added.

## Registration and log entries in RESULTS.md (commit and date of the first line from git blame)

| status labels (keywords in the title and parent heading) | commit | date | lines | title |
|---|---|---|---|---|
| result | `d0a6aa0` | 2026-10-15 01:19:38 +0530 | 482-503 | 2026-10-15 — Large-model result: native vs romanized comprehension gap (back-translation) |
| none | `051f261` | 2026-10-15 21:21:07 +0530 | 681-692 | 2026-10-15 — Back-translation comprehension gap: final (all paired texts) |
| none | `42c9bac` | 2026-10-22 02:14:54 +0530 | 1403-1413 | 2026-10-22 — Note: back-translation summary key renamed (no value changed) |

## Values observed in the result files (read from the files' own columns and keys)

- no model, form, task or seed columns in the dumped files; see the entries

Result directories: none (numbers are in the RESULTS.md entries)

## RESULTS.md entries, verbatim

##### 2026-10-15 — Large-model result: native vs romanized comprehension gap (back-translation)

RESULTS.md lines 482 to 503; first line committed in `d0a6aa0` on 2026-10-15 01:19:38 +0530; last line in `3565362` on 2026-10-15 16:40:24 +0530; labels from the title and parent heading: result

`````text
## 2026-10-15 — Large-model result: native vs romanized comprehension gap (back-translation)

Groq `openai/gpt-oss-120b` (temperature 0, reasoning effort low) translates each E0 text into English, once from the
natural romanization (prompt backtranslate_v1) and once from native Kannada script (backtranslate_native_v1);
cosine similarity of each back-translation to the dataset's English (all-mpnet-base-v2). Outputs:
`results/e0b_natural_check/{backtranslation_with_control.csv, summary_control.json}`.

- **Interim, not final.** The final number will come from all 501 paired texts (and the 86 new texts once they
  exist). 218 texts have both versions so far (2 source-noise items excluded); Groq's 200k tokens/day limit stopped
  the control. 95% bootstrap CIs (10,000 resamples), paired gap = native minus romanized cosine:
  - all 218 controlled texts: native 0.814, romanized 0.582, gap **0.232 [0.203, 0.262]**. **Biased upward by
    selection**: the 24 lowest-similarity texts (26 flagged minus the 2 source-noise items) were controlled first.
  - excluding those flagged texts: 194 texts, native 0.820, romanized 0.637, gap **0.183 [0.160, 0.208]**. Not a
    random sample either: these were taken in file order, so 193 of the 194 are XNLI texts (no sentiment reviews).
  - random subset: the remaining texts are now controlled in a seeded random order
    (`scripts/e0b_backtranslate_control.py`), and the summary reports the gap on the fully controlled prefix of
    that order (`gap_random_prefix`). It is empty until Groq's quota resets.
- Reading: a 120B multilingual model understands Kannada in its own script far better than the same sentences
  typed in natural romanization. This is consistent with the familiarity account (E0b), now seen in a model we do
  not study and through generation rather than classification.

---
`````

##### 2026-10-15 — Back-translation comprehension gap: final (all paired texts)

RESULTS.md lines 681 to 692; first line committed in `051f261` on 2026-10-15 21:21:07 +0530; last line in `e10b11e` on 2026-10-16 00:19:31 +0530; labels from the title and parent heading: none

`````text
## 2026-10-15 — Back-translation comprehension gap: final (all paired texts)

All 587 E0 texts now have both back-translations (`results/e0b_natural_check/summary_control.json`). Excluded: the 2
source-noise items and the 9 defective natural outputs (also excluded from E0b; the control script now drops them),
leaving **n = 576** (378 XNLI, 198 sentiment). The bottom-5% flag (28 eligible texts) no longer selects anything,
because every text is controlled.
- **Final: native 0.838 [0.828, 0.849], natural romanization 0.621 [0.604, 0.639], paired gap 0.217 [0.201, 0.234].**
  This supersedes the interim 0.232 (biased upward by selection) and 0.183 (XNLI-only file order).
- Excluding the 28 flagged texts: 548 texts, gap 0.197 [0.182, 0.212].
- Texts where the romanized back-translation lost more than 0.3 cosine against native: 167 of 576.

---
`````

##### 2026-10-22 — Note: back-translation summary key renamed (no value changed)

RESULTS.md lines 1403 to 1413; first line committed in `42c9bac` on 2026-10-22 02:14:54 +0530; last line in `8d7db7d` on 2026-10-22 02:16:28 +0530; labels from the title and parent heading: none

`````text
## 2026-10-22 — Note: back-translation summary key renamed (no value changed)
In `results/e0b_natural_check/summary_control.json` the final back-translation numbers (native 0.838, natural 0.621,
gap 0.217 [0.201, 0.234], n = 576; RESULTS.md 2026-10-15 "final" entry) sit under the key
`gap_all_controlled_BIASED_UPWARD_by_selection`. That name dates from the interim run, when the 24 lowest-similarity
texts had been controlled first, so the controlled set was selected and the gap biased upward. In the full run every
one of the 576 eligible texts is controlled (`complete_all_paired: true`), so there is no selection and no such bias.
A key `gap_all_controlled` with the identical block was added (copied programmatically from the old key, not
recomputed); the old key is kept. `scripts/e0b_backtranslate_control.py` now writes both, and
`paper/NUMBERS.md` points to the new key.

---
`````

## Result files, every number

(no result files for this experiment)

## Not dumped (item-level, binary or too large; path and size only)

- none

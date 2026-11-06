#!/usr/bin/env bash
# Second extra-seed set (added 2026-11-07 AFTER seeing the originals, at Aarnav's go; registered in RESULTS.md the same day), laptop GPU:
# (1) X9a-low at level 0 (no cipher), 0.01 and 0.03 percent exposure, code seeds 3 and 4 (called seeds 4 and 5; originals 0, 1, 2): 6 runs, about 18 min each;
# (2) X9b secondary arm (Qwen3.5-2B), code seeds 1 and 2 (the original run is code seed 0): ITRANS, native and English, same QLoRA recipe, streams and budget (5,668,864 tokens per run), 6 runs.
# Detached:  powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x9extra2 -Script scripts/x9extra2_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X9EXTRA2.md; TITLE="Extra seeds chain 2 status (X9a-low levels 0/0.01/0.03, X9b Qwen)"; LOG=results/phase2/x9extra2.log
. scripts/chainlib.sh
[ -f data/processed/x9a/train_p0.npy ] || { wait_ram 8; run_hb "X9a level-0 stream regeneration (CPU; sha256 checked)" env PYTHONPATH=src $PY -u scripts/x9a.py regen 0 || fail "x9a regen 0 exited $?"; }
for s in 3 4; do
  for p in 0 0p01 0p03; do
    [ -f results/phase2/x9a/x9a_p${p}_s${s}.json ] && continue
    wait_ram 8; wait_gpu
    run_hb "X9a-low extra seed: level ${p} seed ${s}" env PYTHONPATH=src $PY -u scripts/x9a.py train $p $s || fail "x9a extra train $p $s exited $?"
  done
done
OUT=results/kaggle/laptop_x9b/2026-11-07/out
for s in 1 2; do
  for c in itrans native english; do
    [ -f $OUT/qwen3.5-2b+${c}+s${s}/done.json ] && continue
    wait_ram 8; wait_gpu
    run_hb "X9b Qwen extra seed: qwen3.5-2b ${c} seed ${s}" env PYTHONPATH=src $PY -u scripts/kaggle_x9b.py --out $OUT --mode full --runs qwen3.5-2b:${c}:${s} || fail "x9b qwen extra ${c} ${s} exited $?"
  done
done
st DONE "Extra seeds chain 2 finished at $(date '+%F %T %Z')"

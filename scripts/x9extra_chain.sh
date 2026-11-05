#!/usr/bin/env bash
# Extra seeds added 2026-11-05 AFTER seeing the original seeds (registered in RESULTS.md the same day): (1) X9a-low at 0.1, 0.3 and 1 percent exposure, seeds 3 and 4 (the original seeds are 0, 1, 2);
# (2) X9b primary arm (Sarvam-1) seeds 2 and 3 (the original seeds are 0 and 1; called seeds 3 and 4 beside the original 1 and 2), ITRANS, native and English, same QLoRA recipe and token budget, laptop GPU
# (the pilot on this GPU: 565 tokens/s slowest, 2.46 h of training per run). Waits for the Qwen English-run completion. Detached:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x9extra -Script scripts/x9extra_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X9EXTRA.md; TITLE="Extra seeds chain status (X9a-low, X9b)"; LOG=results/phase2/x9extra.log
. scripts/chainlib.sh
until [ "$(state_of results/CHAIN_STATUS_X9BFIN.md)" = DONE ]; do st WAITING "extra seeds wait for the Qwen English-run completion"; sleep "$HB"; done
[ -f data/processed/x9a/train_p1.npy ] || { wait_ram 8; run_hb "X9a level-1 stream regeneration (CPU; the file was removed with the X9a caches; sha256 checked)" env PYTHONPATH=src $PY -u scripts/x9a.py regen 1 || fail "x9a regen 1 exited $?"; }
for s in 3 4; do
  for p in 0p1 0p3 1; do
    [ -f results/phase2/x9a/x9a_p${p}_s${s}.json ] && continue
    wait_ram 8; wait_gpu
    run_hb "X9a-low extra seed: level ${p} seed ${s}" env PYTHONPATH=src $PY -u scripts/x9a.py train $p $s || fail "x9a extra train $p $s exited $?"
  done
done
OUT=results/kaggle/laptop_x9b/2026-11-05/out
for s in 2 3; do
  for c in itrans native english; do
    [ -f $OUT/sarvam-1+${c}+s${s}/done.json ] && continue
    wait_ram 8; wait_gpu
    run_hb "X9b extra seed: sarvam-1 ${c} seed ${s}" env PYTHONPATH=src $PY -u scripts/kaggle_x9b.py --out $OUT --mode full --base-eval sarvam-1 --runs sarvam-1:${c}:${s} || fail "x9b extra ${c} ${s} exited $?"
  done
done
st DONE "Extra seeds finished at $(date '+%F %T %Z')"

#!/usr/bin/env bash
# Phase 2 laptop queue: the X4 lowercase form (E9 scheme per language) and the ladder: vectors and scores for the lowercase form (M4c rows, SIB-200, IndicSentiment), 2,009-sentence retrieval for the
# lowercase form, tokens per word, then the R2, R3 and ladder analyses. Waits for the E9 search chain.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x4lower -Script scripts/x4lower_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X4LOWER.md; TITLE="Phase 2 X4 lowercase and ladder chain status"; LOG=results/phase2/x4lower.log
. scripts/chainlib.sh
mkdir -p results/phase2
for f in ${WAIT_FOR:-results/CHAIN_STATUS_X4E9.md}; do until [ "$(state_of $f)" = DONE ]; do st WAITING "X4 lowercase waits for $f"; sleep "$HB"; done; done
for L in bn te; do
  export X4_LANG=$L
  wait_ram 8; wait_gpu
  run_hb "X4 $L lowercase vectors (M4c rows)" env PYTHONPATH=src $PY -u scripts/x4_lang.py forward || fail "x4 $L forward exited $?"
  wait_ram 8; wait_gpu
  run_hb "X4 $L lowercase scores (SIB-200, sentiment)" env PYTHONPATH=src $PY -u scripts/x4_lang.py score || fail "x4 $L score exited $?"
  run_hb "X4 $L tokens per word" env PYTHONPATH=src $PY -u scripts/x4_lang.py tpw || fail "x4 $L tpw exited $?"
done
wait_ram 8; wait_gpu
run_hb "X4 retrieval, lowercase form (2,009 sentences)" env PYTHONPATH=src $PY -u scripts/x4_ret.py score || fail "x4 ret score exited $?"
run_hb "X4 R2 analysis" env PYTHONPATH=src $PY -u scripts/x4_ret.py analyse || fail "x4 ret analyse exited $?"
for L in bn te; do
  run_hb "X4 $L R3 and retrieval ladder" env X4_LANG=$L PYTHONPATH=src $PY -u scripts/x4_r3.py || fail "x4 r3 $L exited $?"
done
run_hb "X4 accuracy ladder" env PYTHONPATH=src $PY -u scripts/x4_ladder.py || fail "x4 ladder exited $?"
st DONE "X4 lowercase and ladder finished at $(date '+%F %T %Z'); results/phase2/x4/{bn,te}/ladder_acc.json r3.json"

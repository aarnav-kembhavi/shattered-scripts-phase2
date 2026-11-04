#!/usr/bin/env bash
# Phase 2 laptop queue: X4 scoring for Bengali then Telugu (scripts/x4_lang.py, generalised from the Hindi pipeline): native/ITRANS/lossy vectors and scores, tokens per word; then, once the Gemini drafts of the
# language are complete, the natural vectors and scores. Waits for the status files in WAIT_FOR (default: X9a-low). Analysis (registered R1-R4, ladder) and the E9 lowercase form are not built yet.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x4score -Script scripts/x4score_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X4SCORE.md; TITLE="Phase 2 X4 scoring chain status"; LOG=results/phase2/x4score.log
. scripts/chainlib.sh
mkdir -p results/phase2
for f in ${WAIT_FOR:-results/CHAIN_STATUS_X9ALOW.md}; do until [ "$(state_of $f)" = DONE ]; do st WAITING "X4 scoring waits for $f"; sleep "$HB"; done; done
for L in bn te; do
  export X4_LANG=$L
  run_hb "X4 $L data check" env PYTHONPATH=src $PY -u scripts/x4_lang.py check || fail "x4 $L check failed (exit $?)"
  wait_ram 8; wait_gpu
  run_hb "X4 $L forward native/itrans/lossy" env PYTHONPATH=src $PY -u scripts/x4_lang.py forward || fail "x4 $L forward exited $?"
  wait_ram 8; wait_gpu
  run_hb "X4 $L scoring native/itrans/lossy" env PYTHONPATH=src $PY -u scripts/x4_lang.py score || fail "x4 $L score exited $?"
  run_hb "X4 $L tokens per word" env PYTHONPATH=src $PY -u scripts/x4_lang.py tpw || fail "x4 $L tpw exited $?"
done
for L in bn te; do
  export X4_LANG=$L
  until grep -q '"complete": true' results/phase2/x4/natural/status_$L.json 2>/dev/null; do st WAITING "X4 $L natural drafts not complete"; sleep "$HB"; done
  wait_ram 8; wait_gpu
  run_hb "X4 $L forward natural" env PYTHONPATH=src $PY -u scripts/x4_lang.py forward natural || fail "x4 $L natural forward exited $?"
  wait_ram 8; wait_gpu
  run_hb "X4 $L scoring natural" env PYTHONPATH=src $PY -u scripts/x4_lang.py score natural || fail "x4 $L natural score exited $?"
done
st DONE "X4 scoring (forms and natural) finished at $(date '+%F %T %Z'); results/phase2/x4/{bn,te}/"

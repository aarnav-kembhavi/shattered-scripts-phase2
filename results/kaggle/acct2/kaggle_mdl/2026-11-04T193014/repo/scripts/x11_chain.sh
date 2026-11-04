#!/usr/bin/env bash
# Phase 2 laptop queue: X11 Arm A (4-bit control), after X6 in the registered order; waits for the previous laptop chains named in WAIT_FOR (space-separated status files; default X1T3).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x11 -Script scripts/x11_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X11.md; TITLE="Phase 2 X11 chain status"; LOG=results/phase2/x11.log
. scripts/chainlib.sh
mkdir -p results/phase2
for f in ${WAIT_FOR:-results/CHAIN_STATUS_X1T3.md}; do until [ "$(state_of $f)" = DONE ]; do st WAITING "X11 waits for $f"; sleep "$HB"; done; done
wait_ram 8; wait_gpu
run_hb "X11 4-bit scoring" env PYTHONPATH=src $PY -u scripts/x11.py score || fail "x11 score exited $?"
run_hb "X11 analysis" env PYTHONPATH=src $PY -u scripts/x11.py analyse || fail "x11 analyse exited $?"
st DONE "X11 finished at $(date '+%F %T %Z'); results/phase2/x11/analysis.json"

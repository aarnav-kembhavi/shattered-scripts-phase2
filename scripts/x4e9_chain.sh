#!/usr/bin/env bash
# Phase 2: X4 E9 lowercase scheme search for Bengali and Telugu (CPU), then the lowercase-form scoring chain waits on it.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x4e9 -Script scripts/x4e9_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X4E9.md; TITLE="Phase 2 X4 E9 search chain status"; LOG=results/phase2/x4e9.log
. scripts/chainlib.sh
mkdir -p results/phase2
for L in bn te; do
  run_hb "X4 E9 search $L (20,000 words, 3 restarts)" env PYTHONPATH=src $PY -u scripts/x4_e9.py search $L --words 20000 --restarts 3 --workers 3 || fail "x4 e9 search $L exited $?"
done
st DONE "X4 E9 search finished at $(date '+%F %T %Z'); results/phase2/x4/{bn,te}/e9/"

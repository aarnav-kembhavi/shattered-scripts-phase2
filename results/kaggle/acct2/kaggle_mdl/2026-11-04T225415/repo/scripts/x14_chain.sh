#!/usr/bin/env bash
# Phase 2 X14 black-box hosted models (Groq; API only, no GPU, exploratory): runs until every model has every item and form, waiting for the next
# daily reset whenever the own caps are reached. Responses are cached. Status: results/CHAIN_STATUS_X14.md.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x14 -Script scripts/x14_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X14.md; TITLE="Phase 2 X14 hosted models chain status"; LOG=results/phase2/x14.log
. scripts/chainlib.sh
while :; do
  run_net "X14 hosted models" env PYTHONPATH=src $PY -u scripts/x14_run.py run; c=$?
  [ $c = 0 ] && break
  [ $c = 3 ] || fail "x14 exited $c"
  wait_until "$(next_reset)" "X14: daily caps reached, waiting for the reset"
done
PYTHONPATH=src $PY scripts/x14_run.py report >> "$LOG" 2>&1
st DONE "X14 finished at $(date '+%F %T %Z')"

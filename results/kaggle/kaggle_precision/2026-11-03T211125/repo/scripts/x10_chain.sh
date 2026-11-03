#!/usr/bin/env bash
# Phase 2 laptop queue: X10 generation. MODE=pilot (default): 20 sentences per model and form (timing and sanity), then the status is DONE; MODE=full: score each model, then analyse.
# Queue position (Aarnav): X9a, X7-A, X10 pilot, X4, X1 T3, X6, X11, X10 full. Run detached, e.g.:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x10p -Script scripts/x10_chain.sh
set -u
cd "$(dirname "$0")/.."
MODE=${MODE:-pilot}
if [ "$MODE" = pilot ]; then STATUS=results/CHAIN_STATUS_X10P.md; TITLE="Phase 2 X10 pilot chain status"; LOG=results/phase2/x10p.log
else STATUS=results/CHAIN_STATUS_X10.md; TITLE="Phase 2 X10 full chain status"; LOG=results/phase2/x10.log; fi
. scripts/chainlib.sh
mkdir -p results/phase2
until [ "$(state_of results/CHAIN_STATUS_X7A.md)" = DONE ]; do st WAITING "X10 waits for X7-A (CHAIN_STATUS_X7A.md)"; sleep "$HB"; done
if [ "$MODE" = pilot ]; then
  wait_ram 8; wait_gpu
  run_hb "X10 pilot (20 sentences per model and form)" env PYTHONPATH=src $PY -u scripts/x10.py pilot || fail "x10 pilot exited $?"
  st DONE "X10 pilot finished at $(date '+%F %T %Z'); results/phase2/x10/pilot.json"
else
  for m in qwen3-1.7b qwen3.5-2b sarvam-1 gemma4-e2b; do
    wait_ram 8; wait_gpu
    run_hb "X10 full: $m" env PYTHONPATH=src $PY -u scripts/x10.py score $m || fail "x10 score $m exited $?"
  done
  run_hb "X10 analysis" env PYTHONPATH=src $PY -u scripts/x10.py analyse || fail "x10 analyse exited $?"
  st DONE "X10 finished at $(date '+%F %T %Z'); results/phase2/x10/analysis.json"
fi

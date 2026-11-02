#!/usr/bin/env bash
# Kaggle queue (A1-P pair -> score X13/X12 -> A1-P Ambari-Instruct pair -> X9b when ready; order set 2026-11-02 23:30) driven by scripts/kaggle_queue.py; repeats every 90 minutes (up to 40 passes) so that gated models are retried
# between jobs; ends when no X12/X13 model is left waiting. One Kaggle job at a time (the driver blocks on each push). Status: results/CHAIN_STATUS_KQUEUE.md.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name kqueue -Script scripts/kaggle_queue_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_KQUEUE.md; TITLE="Phase 2 Kaggle queue status"; LOG=results/phase2/kqueue.log
. scripts/chainlib.sh
for i in $(seq 1 40); do
  run_net "Kaggle queue pass $i" env PYTHONPATH=src $PY -u scripts/kaggle_queue.py || fail "kaggle queue exited $?"
  $PY scripts/kaggle_queue.py --open && break   # exit 0 = nothing left open (every wanted model scored, failed A1-P, or not applicable)
  until=$(( $(date +%s) + 5400 )); while [ "$(date +%s)" -lt "$until" ]; do st WAITING "Kaggle queue: pass $i done, waiting to retry gated models (until $(date -d "@$until" '+%T'))"; sleep "$HB"; done
done
st DONE "Kaggle queue finished at $(date '+%F %T %Z')"

#!/usr/bin/env bash
# Kaggle queue (A1-P -> X12 -> X13) driven by scripts/kaggle_queue.py; repeats every 90 minutes (up to 40 passes) so that gated models are retried
# between jobs; ends when no X12/X13 model is left waiting. One Kaggle job at a time (the driver blocks on each push). Status: results/CHAIN_STATUS_KQUEUE.md.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name kqueue -Script scripts/kaggle_queue_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_KQUEUE.md; TITLE="Phase 2 Kaggle queue status"; LOG=results/phase2/kqueue.log
. scripts/chainlib.sh
for i in $(seq 1 40); do
  run_net "Kaggle queue pass $i" env PYTHONPATH=src $PY -u scripts/kaggle_queue.py || fail "kaggle queue exited $?"
  $PY - <<'PYEOF' && break
import json, sys
s = json.load(open("results/kaggle/queue_state.json"))
want = ["qwen3-8b", "ambari-7b-base", "llama-2-7b", "llama-3.1-8b"]
open_ = [m for m in want if m not in s["scored"] and s["precision"].get(m, {}).get("pass") is not False]
sys.exit(0 if not open_ else 1)
PYEOF
  until=$(( $(date +%s) + 5400 )); while [ "$(date +%s)" -lt "$until" ]; do st WAITING "Kaggle queue: pass $i done, waiting to retry gated models (until $(date -d "@$until" '+%T'))"; sleep "$HB"; done
done
st DONE "Kaggle queue finished at $(date '+%F %T %Z')"

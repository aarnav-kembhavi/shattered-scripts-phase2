#!/usr/bin/env bash
# Heartbeat for a long chain step, run alongside the chain without touching it.
#   bash scripts/chain_watch.sh <chain_bash_pid> <step_name> <step_log>   (Windows PIDs)
# Every 5 minutes, while the status says RUNNING in <step_name>, refresh the heartbeat with the step log's last line.
# Exits when the chain records DONE or FAILED. If the chain process disappears while the status still says RUNNING or
# WAITING, the chain died without a trace: mark it DEAD.
cd "$(dirname "$0")/.."
S=results/CHAIN_STATUS.md; CHAIN=$1; STEP=$2; LOG=$3
alive() { powershell -NoProfile -Command "if (Get-Process -Id $1 -ErrorAction SilentlyContinue) {exit 0} else {exit 1}"; }
while true; do
  if grep -q "state: \*\*DONE\|state: \*\*FAILED" "$S"; then echo "chain finished: $(grep 'state:' "$S")"; exit 0; fi
  if ! alive "$CHAIN"; then
    sleep 10
    if grep -q "state: \*\*RUNNING\|state: \*\*WAITING" "$S"; then
      sed -i "s|^- state: .*|- state: **DEAD** (chain process $CHAIN gone at $(date '+%F %T %Z') without recording DONE or FAILED)|" "$S"
      echo DEAD; exit 1
    fi
    exit 0
  fi
  if grep -q "state: \*\*RUNNING" "$S" && grep -q "current step: $STEP " "$S"; then
    last=$(tr '\r' '\n' < "$LOG" | grep -v "Loading\|^$\|warn" | tail -1 | cut -c1-160)
    sed -i "s|^- heartbeat: .*|- heartbeat: $(date '+%F %T %Z') (watcher: chain alive; last log line: ${last//|/ })|" "$S"
  fi
  sleep 300
done

#!/usr/bin/env bash
# NC1 non-canonical tokenization (registered 2026-10-22; gate approved 2026-10-22). Run detached:
# scripts/detach.ps1 -Name nc1 -Script scripts/nc1_chain.sh. Forward passes (4 models), scoring (5 models), analysis.
# One model load at a time; each GPU step waits for free RAM. Steps resume from their caches.
# Status in results/CHAIN_STATUS_NC1.md. No API calls.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_NC1.md; TITLE="NC1 chain status"; LOG=results/nc1.log
. scripts/chainlib.sh
wait_ram 8
run_hb "forward pass (a, b, c; 4 models)" $PY -u scripts/nc1.py forward || fail "forward exited $?"
wait_ram 8
run_hb "accuracy scoring (a, b, c; 5 models)" $PY -u scripts/nc1.py score || fail "score exited $?"
run_hb "analysis" $PY -u scripts/nc1.py analyse || fail "analyse exited $?"
st DONE "NC1 finished at $(date '+%F %T %Z'); results/nc1/"

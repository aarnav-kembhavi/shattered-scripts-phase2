#!/usr/bin/env bash
# Phase 2 laptop queue: X6 run part 1 (SIB-200 counting run for the shortlist). Pulled forward on 2026-11-05 when the laptop queue ran dry.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x6run -Script scripts/x6run_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X6RUN.md; TITLE="Phase 2 X6 run chain status"; LOG=results/phase2/x6run.log
. scripts/chainlib.sh
mkdir -p results/phase2
wait_ram 8; wait_gpu
run_hb "X6 SIB-200 scoring" env PYTHONPATH=src $PY -u scripts/x6_run.py score || fail "x6 score exited $?"
run_hb "X6 counting analysis" env PYTHONPATH=src $PY -u scripts/x6_run.py analyse || fail "x6 analyse exited $?"
st DONE "X6 counting run finished at $(date '+%F %T %Z'); results/phase2/x6/counting.json"

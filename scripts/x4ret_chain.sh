#!/usr/bin/env bash
# Phase 2 laptop queue: X4 retrieval (R2) for Bengali and Telugu. Pulled forward on 2026-11-05 when the laptop queue ran dry after the X6 counting run.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x4ret -Script scripts/x4ret_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X4RET.md; TITLE="Phase 2 X4 retrieval chain status"; LOG=results/phase2/x4ret.log
. scripts/chainlib.sh
mkdir -p results/phase2
wait_ram 8; wait_gpu
run_hb "X4 retrieval forward and curves (bn, te; 4 models)" env PYTHONPATH=src $PY -u scripts/x4_ret.py score || fail "x4 ret score exited $?"
run_hb "X4 retrieval R2 analysis" env PYTHONPATH=src $PY -u scripts/x4_ret.py analyse || fail "x4 ret analyse exited $?"
st DONE "X4 retrieval finished at $(date '+%F %T %Z'); results/phase2/x4/{bn,te}/r2.json"

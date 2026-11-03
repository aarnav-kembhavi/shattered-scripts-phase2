#!/usr/bin/env bash
# Phase 2 GPU queue, step 3: X7 factorized-embedding control, 18 runs (registered 2026-11-01). Run detached:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x7 -Script scripts/x7_chain.sh
# Seed-major; each run resumes from its checkpoint. Status in results/CHAIN_STATUS_X7.md. No API calls.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X7.md; TITLE="Phase 2 X7 control chain status"; LOG=results/phase2/x7.log
. scripts/chainlib.sh
wait_ram 8; wait_gpu
run_hb "X7 factorized-embedding grid (18 runs)" env PYTHONPATH=src $PY -u scripts/x7_control.py grid || fail "x7 grid exited $?"
st DONE "X7 control finished at $(date '+%F %T %Z'); results/phase2/x7/ and results/e05_pretrain/x7_*"

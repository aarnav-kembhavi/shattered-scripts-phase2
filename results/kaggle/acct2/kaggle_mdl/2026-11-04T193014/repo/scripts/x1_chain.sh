#!/usr/bin/env bash
# Phase 2 GPU queue, step 1: X1 T2 scoring (registered 2026-11-01). Run detached:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x1 -Script scripts/x1_chain.sh
# One model load at a time (RAM and GPU guards, disk guard inside wait_gpu); each model resumes from its stored parquet files.
# Status in results/CHAIN_STATUS_X1.md. No API calls.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X1.md; TITLE="Phase 2 X1 (T2 scoring) chain status"; LOG=results/phase2/x1.log
. scripts/chainlib.sh
mkdir -p results/phase2
for m in gemma4-e2b sarvam-1 qwen3.5-2b qwen3-1.7b qwen2.5-1.5b; do
  wait_ram 8; wait_gpu
  run_hb "T2 scoring: $m" env PYTHONPATH=src $PY -u scripts/x1_t2.py score "$m" || fail "x1 score $m exited $?"
done
st DONE "X1 T2 scoring finished at $(date '+%F %T %Z'); results/phase2/x1/t2/ (analysis not yet run)"

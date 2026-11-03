#!/usr/bin/env bash
# Phase 2 GPU queue, step 2: X3 scoring of the frequency-matched splits (registered 2026-11-01). Run detached:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x3 -Script scripts/x3_chain.sh
# One model load at a time; each model resumes from its stored score files. Status in results/CHAIN_STATUS_X3.md. No API calls.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X3.md; TITLE="Phase 2 X3 chain status"; LOG=results/phase2/x3.log
. scripts/chainlib.sh
for m in gemma4-e2b sarvam-1 qwen3.5-2b qwen3-1.7b qwen2.5-1.5b; do
  wait_ram 8; wait_gpu
  run_hb "X3 scoring: $m" env PYTHONPATH=src $PY -u scripts/x3.py score "$m" || fail "x3 score $m exited $?"
done
st DONE "X3 scoring finished at $(date '+%F %T %Z'); results/phase2/x3/ (analysis not yet run)"

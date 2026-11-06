#!/usr/bin/env bash
# X10 post hoc extraction check for Qwen3.5-2B (not part of the registration). Laptop GPU filler on 2026-11-05.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X10PH.md; TITLE="X10 post hoc chain status"; LOG=results/phase2/x10ph.log
. scripts/chainlib.sh
wait_ram 8; wait_gpu
run_hb "X10 post hoc generation (Qwen3.5-2B, raw outputs)" env PYTHONPATH=src $PY -u scripts/x10_posthoc.py score || fail "x10 posthoc score exited $?"
run_hb "X10 post hoc analysis" env PYTHONPATH=src $PY -u scripts/x10_posthoc.py analyse || fail "x10 posthoc analyse exited $?"
st DONE "X10 post hoc finished at $(date '+%F %T %Z'); results/phase2/x10/posthoc/analysis.json"

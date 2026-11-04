#!/usr/bin/env bash
# Phase 2 laptop queue: X6 screen stage 2 (forward-pass peak memory in bf16 with hidden states, registered rule 1) for the stage 1 shortlist chosen on 2026-11-04. Waits for X4 scoring (the laptop GPU is in use).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x6mem -Script scripts/x6mem_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X6MEM.md; TITLE="Phase 2 X6 memory check chain status"; LOG=results/phase2/x6mem.log
. scripts/chainlib.sh
mkdir -p results/phase2
for f in ${WAIT_FOR:-results/CHAIN_STATUS_X4SCORE.md}; do until [ "$(state_of $f)" = DONE ]; do st WAITING "X6 memory check waits for $f"; sleep "$HB"; done; done
wait_ram 8; wait_gpu
run_hb "X6 stage 2 memory check" env PYTHONPATH=src $PY -u scripts/x6_screen.py mem NousResearch/Llama-3.2-1B ashtok897/oroZ-1.7B-Indic-v1 || fail "x6 mem exited $?"
st DONE "X6 memory check finished at $(date '+%F %T %Z'); results/phase2/x6/mem.json"

#!/usr/bin/env bash
# K1/K2 pilot (registered 2026-10-16; implementation notes 2026-10-26): one model load, RAM and GPU checks and the
# H1-LF priority rule first. Stops after the pilot (no accuracy or test computed); the full run needs Aarnav's OK.
# Run detached: scripts/detach.ps1 -Name k12pilot -Script scripts/k12_pilot_chain.sh. Status: results/CHAIN_STATUS_K12PILOT.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_K12PILOT.md; TITLE="K1/K2 pilot chain status"; LOG=results/k12_pilot.log
. scripts/chainlib.sh
wait_h1lf; wait_ram 8; wait_gpu
run_hb "K1/K2 pilot (Qwen3.5-2B, 20 items)" $PY -u scripts/k_k12.py pilot || fail "K1/K2 pilot exited $? (a check failed or an error)"
st DONE "K1/K2 pilot finished at $(date '+%F %T %Z'); results/k12/pilot.json. Full run waits for Aarnav's OK."

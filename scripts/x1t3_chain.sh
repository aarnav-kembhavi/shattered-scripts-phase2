#!/usr/bin/env bash
# Phase 2 laptop queue: X1 T3 scoring (exploratory; instruction verified by a native speaker). Queue position: after X9a (Aarnav, 2026-11-03). Run detached, only when the laptop GPU is free:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x1t3 -Script scripts/x1t3_chain.sh
# Same code path as the T2 scoring (scripts/x1_t2.py) with X1_TEMPLATE=v3; outputs under results/phase2/x1/t3/ with LABEL.txt "instruction verified by a native speaker, exploratory".
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X1T3.md; TITLE="Phase 2 X1 T3 scoring chain status"; LOG=results/phase2/x1t3.log
. scripts/chainlib.sh
mkdir -p results/phase2
# queue position (Aarnav): after X9a and X7-A; never two model-loading jobs at once, so wait for the X7-A chain (and the X10 pilot chain if present) to be DONE
until [ "$(state_of results/CHAIN_STATUS_X7A.md)" = DONE ]; do st WAITING "X1 T3 waits for X7-A (CHAIN_STATUS_X7A.md)"; sleep "$HB"; done
until [ "$(state_of results/CHAIN_STATUS_X10P.md)" = DONE ]; do st WAITING "X1 T3 waits for the X10 pilot (CHAIN_STATUS_X10P.md)"; sleep "$HB"; done
for m in gemma4-e2b sarvam-1 qwen3.5-2b qwen3-1.7b qwen2.5-1.5b; do
  wait_ram 8; wait_gpu
  run_hb "T3 scoring: $m" env X1_TEMPLATE=v3 PYTHONPATH=src $PY -u scripts/x1_t2.py score "$m" || fail "x1 t3 score $m exited $?"
done
st DONE "X1 T3 scoring finished at $(date '+%F %T %Z'); results/phase2/x1/t3/ (label: instruction verified by a native speaker, exploratory)"

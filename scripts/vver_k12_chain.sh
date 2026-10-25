#!/usr/bin/env bash
# Queued after EP-R (Aarnav, 2026-10-26): waits for results/CHAIN_STATUS_EPR.md to be DONE (stops if it FAILED or is
# DEAD), then V-VER (exploratory, registered 2026-10-26 03:15 IST: forward 3 retrieval models, score 4 models,
# analysis), then the K1/K2 pilot (Qwen3.5-2B, 20 items) and STOPS: the K1/K2 full run needs Aarnav's OK.
# One process per model load, RAM and GPU checks before each. Run detached:
# scripts/detach.ps1 -Name vver_k12 -Script scripts/vver_k12_chain.sh. Status in results/CHAIN_STATUS_VVER.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_VVER.md; TITLE="V-VER + K1/K2 pilot chain status"; LOG=results/vver_k12.log
. scripts/chainlib.sh
while :; do
  s=$(state_of results/CHAIN_STATUS_EPR.md)
  [ "$s" = DONE ] && break
  case "$s" in FAILED|DEAD) fail "EP-R chain is $s; not starting";; esac
  st WAITING "queued behind EP-R (EP-R: ${s:-no status})"
  sleep 120
done
for m in qwen3.5-2b sarvam-1 gemma4-e2b; do
  wait_ram 8; wait_gpu
  run_hb "V-VER forward, $m" $PY -u scripts/v_ver.py forward $m || fail "V-VER forward $m exited $?"
done
for m in qwen3-1.7b qwen3.5-2b sarvam-1 gemma4-e2b; do
  wait_ram 8; wait_gpu
  run_hb "V-VER score, $m" $PY -u scripts/v_ver.py score $m || fail "V-VER score $m exited $?"
done
run_hb "V-VER analysis" $PY -u scripts/v_ver.py analyse || fail "V-VER analyse exited $?"
wait_ram 8; wait_gpu
run_hb "K1/K2 pilot (Qwen3.5-2B, 20 items)" $PY -u scripts/k_k12.py pilot || fail "K1/K2 pilot exited $? (a check failed or an error)"
st DONE "V-VER and the K1/K2 pilot finished at $(date '+%F %T %Z'); results/v_ver/, results/k12/pilot.json. K1/K2 full run waits for Aarnav's OK."

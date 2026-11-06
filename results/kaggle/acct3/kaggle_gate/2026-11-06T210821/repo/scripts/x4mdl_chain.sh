#!/usr/bin/env bash
# Phase 2 laptop queue: X4 R4 (MDL assembly layer on Bengali and Telugu Wikipedia words). Pulled forward on 2026-11-05 when the laptop queue ran dry after X4 retrieval.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x4mdl -Script scripts/x4mdl_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X4MDL.md; TITLE="Phase 2 X4 MDL chain status"; LOG=results/phase2/x4mdl.log
. scripts/chainlib.sh
mkdir -p results/phase2
for L in bn te; do
  wait_ram 8; wait_gpu
  run_hb "X4 MDL scoring $L" env PYTHONPATH=src $PY -u scripts/x4_mdl.py score $L || fail "x4 mdl score $L exited $?"
done
run_hb "X4 R4 analysis" env PYTHONPATH=src $PY -u scripts/x4_mdl.py analyse || fail "x4 mdl analyse exited $?"
st DONE "X4 MDL finished at $(date '+%F %T %Z'); results/phase2/x4/{bn,te}/r4.json"

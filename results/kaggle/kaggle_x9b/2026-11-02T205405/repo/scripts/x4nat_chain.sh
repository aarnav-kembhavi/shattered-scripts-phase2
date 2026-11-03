#!/usr/bin/env bash
# Phase 2 X4 natural romanization drafts (Gemini, API only, no GPU): Bengali then Telugu, one sentence per call (batching pilot decided
# "unbatched", results/phase2/x4/natural/batching_pilot.json), own cap 480 requests a day; waits for the next quota reset and continues.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x4nat -Script scripts/x4nat_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X4NAT.md; TITLE="Phase 2 X4 natural drafts chain status"; LOG=results/phase2/x4nat.log
. scripts/chainlib.sh
for L in bn te; do
  while :; do
    run_net "X4 natural drafts $L" env PYTHONPATH=src $PY -u scripts/x4_natural.py romanize $L; c=$?
    [ $c = 0 ] || fail "x4 natural $L exited $c"
    grep -q '"complete": true' results/phase2/x4/natural/status_$L.json && break
    wait_until "$(next_reset)" "X4 natural $L: daily Gemini cap reached, waiting for the reset"
  done
done
st DONE "X4 natural drafts bn and te finished at $(date '+%F %T %Z')"

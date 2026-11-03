#!/usr/bin/env bash
# Phase 2 laptop queue: X7-A (exploratory MDL assembly probes on the 18 X7 control runs; registered in RESULTS.md, tag phase2-x7a). Right after X9a, before the X10 pilot (Aarnav).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x7a -Script scripts/x7a_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X7A.md; TITLE="Phase 2 X7-A chain status"; LOG=results/phase2/x7a.log
. scripts/chainlib.sh
mkdir -p results/phase2
wait_ram 8; wait_gpu
run_hb "X7-A MDL probes on the 18 X7 runs" env PYTHONPATH=src $PY -u scripts/x7a_mdl.py || fail "x7a exited $?"
st DONE "X7-A finished at $(date '+%F %T %Z'); results/phase2/x7a/analysis.json"

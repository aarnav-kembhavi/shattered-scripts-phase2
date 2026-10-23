#!/usr/bin/env bash
# E-P1 then E-P2 full runs (registered 2026-10-23 16:00 IST; full runs approved by Aarnav 2026-10-23 after the pilot
# gates). One process per model load, with the RAM and GPU checks before each; no library or kernel change (versions
# are logged in each raw file's meta). Run detached: scripts/detach.ps1 -Name ep -Script scripts/ep_chain.sh.
# Status in results/CHAIN_STATUS_EP.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_EP.md; TITLE="E-P1 / E-P2 patching chain status"; LOG=results/ep.log
. scripts/chainlib.sh
for e in 1 2; do
  for m in qwen3-1.7b qwen3.5-2b sarvam-1 gemma4-e2b; do
    wait_ram 8; wait_gpu
    run_hb "E-P$e run, $m" $PY -u scripts/ep_patching.py run $e $m || fail "E-P$e run $m exited $?"
  done
  run_hb "E-P$e analysis and figure" $PY -u scripts/ep_patching.py analyse $e || fail "E-P$e analyse exited $?"
done
st DONE "E-P1 and E-P2 finished at $(date '+%F %T %Z'); results/ep1/, results/ep2/, paper/figures/ep*_recovery_curves.*"

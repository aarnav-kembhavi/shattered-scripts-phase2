#!/usr/bin/env bash
# EP-R full run (exploratory, registered 2026-10-26 02:40 IST; started only after Aarnav approves the pilot gate).
# One process per model load, with the RAM and GPU checks before each (ISM may need the GPU); no library or kernel
# change. Run detached: scripts/detach.ps1 -Name ep_robust -Script scripts/ep_robust_chain.sh.
# Status in results/CHAIN_STATUS_EPR.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_EPR.md; TITLE="EP-R (E-P1/E-P2 on all eligible items) chain status"; LOG=results/ep_robust.log
. scripts/chainlib.sh
for e in 1 2; do
  for m in qwen3-1.7b qwen3.5-2b sarvam-1 gemma4-e2b; do
    wait_ram 8; wait_gpu
    run_hb "EP-R E-P$e, $m" $PY -u scripts/ep_robust.py run $e $m || fail "EP-R E-P$e $m exited $?"
  done
done
run_hb "EP-R analysis" $PY -u scripts/ep_robust.py analyse || fail "EP-R analyse exited $?"
st DONE "EP-R finished at $(date '+%F %T %Z'); results/ep_robust/"

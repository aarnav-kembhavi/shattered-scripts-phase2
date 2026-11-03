#!/usr/bin/env bash
# Romanization ladder L1-L3 (registered 2026-10-22). Run detached: scripts/detach.ps1 -Name ladder.
# Waits until the Kanglish chain is not running (no shared GPU/RAM), then: forward passes (lossy, lower; 4 models),
# accuracy scoring (lower on E0b/E0c, natural257 on SIB; 5 models), analysis. One model load at a time; each GPU step
# waits for free RAM. Steps resume from their caches. Status in results/CHAIN_STATUS_LADDER.md. No API calls.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_LADDER.md; TITLE="Ladder chain status (L1-L3)"; LOG=results/l_ladder.log
. scripts/chainlib.sh
while :; do
  s=$(state_of results/CHAIN_STATUS_KANGLISH.md)
  case "$s" in RUNNING|WAITING) ;; *) break ;; esac
  st WAITING "for the Kanglish chain to finish (state: $s)"; sleep "$HB"
done
wait_ram 8
run_hb "forward pass (lossy, lower; 4 models)" $PY -u scripts/l_ladder.py forward || fail "forward exited $?"
wait_ram 8
run_hb "accuracy scoring (lower, natural257; 5 models)" $PY -u scripts/l_ladder.py score || fail "score exited $?"
run_hb "analysis" $PY -u scripts/l_ladder.py analyse || fail "analyse exited $?"
st DONE "ladder finished at $(date '+%F %T %Z'); results/l_ladder/"

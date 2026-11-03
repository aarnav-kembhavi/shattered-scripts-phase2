#!/usr/bin/env bash
# M4c (natural romanization in M4). Run detached: scripts/detach.ps1 -Name m4c. Status in results/CHAIN_STATUS.md.
# 1. Romanize now; on a Gemini quota stop wait for the next 12:45 IST reset and resume from the cache (at most 5
#    resets). Writes results/m4c_romanize.DONE when complete, which releases the Kanglish chain (M4c has quota priority).
# 2. Forward pass only after the E0c chain has finished (DONE/FAILED, or DEAD with no E0c python left): never two
#    model loads at once. 3. Analysis.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS.md; TITLE="Chain status: m4c (natural romanization in M4)"; LOG=results/m4c_natural.log
. scripts/chainlib.sh
for i in $(seq 0 5); do
  run_hb "romanize (attempt after $i quota resets)" $PY -u scripts/m4c_natural_flores.py romanize || fail "romanize exited $?"
  tail -1 "$LOG" | grep -q "'complete': True" && break
  [ "$i" = 5 ] && fail "romanize incomplete after 5 quota resets"
  wait_until "$(next_reset)" "Gemini quota stop; resume after the next reset"
done
date '+%F %T %Z' > results/m4c_romanize.DONE
while :; do
  s=$(state_of results/CHAIN_STATUS_E0C.md)
  case "$s" in DONE|FAILED) break ;; DEAD) py_alive e0c_sib.py || break ;; esac
  st WAITING "romanization complete; forward pass waits for the E0c chain (state: ${s:-none})"; sleep "$HB"
done
wait_ram 8
run_hb "forward pass (natural, 4 models)" $PY -u scripts/m4c_natural_flores.py forward || fail "forward exited $?"
run_hb "analysis" $PY -u scripts/m4c_natural_flores.py analyse || fail "analyse exited $?"
st DONE "m4c finished at $(date '+%F %T %Z'); results/m4c_natural/"

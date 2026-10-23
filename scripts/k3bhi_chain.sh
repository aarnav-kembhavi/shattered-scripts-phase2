#!/usr/bin/env bash
# K3b-hi (registered 2026-10-23 12:05 IST): Gemini vs native-speaker romanization on Dakshina Hindi. Lowest Gemini
# priority (queue order registered 2026-10-23 15:44 IST: K3b, H1-LF option 1 drafts, K3b-hi): waits for the H1-LF
# SIB-1004 drafts marker (results/h1lf/sib1004_drafts.DONE), and stops if the H1-LF chain FAILED or is DEAD first. Run detached: scripts/detach.ps1 -Name k3bhi -Script scripts/k3bhi_chain.sh. API only: loads no
# model. On a quota stop waits for the next 12:45 IST reset and resumes from the cache (at most 6 resets).
# Status in results/CHAIN_STATUS_K3BHI.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_K3BHI.md; TITLE="K3b-hi chain status"; LOG=results/k3bhi.log
. scripts/chainlib.sh
while :; do
  [ -f results/h1lf/sib1004_drafts.DONE ] && break
  s=$(state_of results/CHAIN_STATUS_H1LF.md)
  case "$s" in FAILED|DEAD) fail "H1-LF chain is $s before its drafts finished; K3b-hi not started" ;; esac
  st WAITING "queued behind the H1-LF SIB-1004 drafts (H1-LF chain: ${s:-none})"; sleep "$HB"
done
[ -f results/k3b_hi/sample.json ] || { run_hb "K3b-hi sample" $PY -u scripts/k3b_dakshina.py sample hi || fail "K3b-hi sample exited $?"; }
for i in $(seq 0 6); do
  run_hb "K3b-hi drafts (after $i quota resets)" $PY -u scripts/k3b_dakshina.py draft hi; code=$?
  [ $code = 0 ] && break
  [ $code = 3 ] || fail "K3b-hi drafts exited $code"
  [ "$i" = 6 ] && fail "K3b-hi drafts incomplete after 6 quota resets"
  wait_until "$(next_reset)" "K3b-hi drafts: Gemini quota stop; resume after the next reset"
done
run_hb "K3b-hi analysis" $PY -u scripts/k3b_dakshina.py analyse hi || fail "K3b-hi analyse exited $?"
st DONE "K3b-hi finished at $(date '+%F %T %Z'); results/k3b_hi/"

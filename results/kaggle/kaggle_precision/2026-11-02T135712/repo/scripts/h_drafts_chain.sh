#!/usr/bin/env bash
# Gemini drafts (registered 2026-10-23): Hindi natural romanization (H-Hindi), then K3b on Dakshina Kannada. Run
# detached: scripts/detach.ps1 -Name hdrafts -Script scripts/h_drafts_chain.sh. API only: loads no model. On a quota
# stop waits for the next 12:45 IST reset and resumes from the cache (at most 6 resets per step).
# Status in results/CHAIN_STATUS_HDRAFTS.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_HDRAFTS.md; TITLE="Hindi drafts + K3b chain status"; LOG=results/h_drafts.log
. scripts/chainlib.sh
quota_loop() {  # quota_loop "<label>" cmd args... : exit 0 done, 3 quota stop (wait and retry), else fail
  local label=$1; shift
  for i in $(seq 0 6); do
    run_hb "$label (after $i quota resets)" "$@"; local code=$?
    [ $code = 0 ] && return 0
    [ $code = 3 ] || fail "$label exited $code"
    [ "$i" = 6 ] && fail "$label incomplete after 6 quota resets"
    wait_until "$(next_reset)" "$label: Gemini quota stop; resume after the next reset"
  done
}
quota_loop "Hindi natural drafts" $PY -u scripts/h_hindi.py draft
[ -f results/h_hindi/natural_drafts.DONE ] || fail "Hindi drafts finished without the DONE marker"
[ -f results/k3b/sample.json ] || { run_hb "K3b sample" $PY -u scripts/k3b_dakshina.py sample || fail "K3b sample exited $?"; }
quota_loop "K3b drafts" $PY -u scripts/k3b_dakshina.py draft
run_hb "K3b analysis" $PY -u scripts/k3b_dakshina.py analyse || fail "K3b analyse exited $?"
st DONE "Hindi drafts and K3b finished at $(date '+%F %T %Z'); results/h_hindi/, results/k3b/"

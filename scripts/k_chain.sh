#!/usr/bin/env bash
# Kanglish/natural drafting for the annotation set (K1-K3). Run detached: scripts/detach.ps1 -Name kanglish.
# Gemini quota priority goes to M4c: waits until M4c's romanization is complete (results/m4c_romanize.DONE), or the M4c
# chain has ended (DONE/FAILED, or DEAD with no M4c romanize python left). Then drafts with whatever quota is left; on a
# quota stop waits for the next 12:45 IST reset and continues from the cache (at most 6 resets). Finally builds
# annotation/annotate_v1.html. Status in results/CHAIN_STATUS_KANGLISH.md. API only: loads no model.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_KANGLISH.md; TITLE="Kanglish chain status"; LOG=results/k_drafts.log
. scripts/chainlib.sh
while [ ! -f results/m4c_romanize.DONE ]; do
  s=$(state_of results/CHAIN_STATUS.md)
  case "$s" in DONE|FAILED) break ;; DEAD) py_alive "m4c_natural_flores.py romanize" || break ;; esac
  st WAITING "for M4c romanization to finish (M4c has Gemini priority; M4c state: ${s:-none})"; sleep "$HB"
done
for i in $(seq 0 6); do
  run_hb "drafting (attempt after $i quota resets)" $PY -u scripts/k_annotation.py draft; code=$?
  [ $code = 0 ] && break
  [ $code = 3 ] || fail "draft exited $code"
  [ "$i" = 6 ] && fail "drafts incomplete after 6 quota resets"
  wait_until "$(next_reset)" "Gemini quota stop; resume after the next reset"
done
run_hb "building the annotation page" $PY -u scripts/k_annotation.py page || fail "page exited $?"
st DONE "drafts complete, annotation/annotate_v1.html built at $(date '+%F %T %Z')"

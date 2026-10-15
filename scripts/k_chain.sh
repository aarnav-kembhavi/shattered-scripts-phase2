#!/usr/bin/env bash
# Kanglish/natural drafting for the annotation set (K1-K3). Waits until the M4c chain has finished (results/
# CHAIN_STATUS.md says DONE or FAILED for chain m4c), so the two never compete for the Gemini daily quota. Then drafts
# with the leftover quota; on a quota stop waits until 12:45 IST the next day (at most 6 days) and continues from the
# cache. Finally builds annotation/annotate_v1.html. Status in results/CHAIN_STATUS_KANGLISH.md.
set -u
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
LOG=results/k_drafts.log; STATUS=results/CHAIN_STATUS_KANGLISH.md
st() { printf '# Kanglish chain status\n\n- state: **%s**\n- heartbeat: %s\n- detail: %s\n' "$1" "$(date '+%F %T %Z')" "$2" > "$STATUS"; }
fail() { st FAILED "$1 at $(date '+%T'); see $LOG"; { echo; echo '```'; tail -n 30 "$LOG"; echo '```'; } >> "$STATUS"; exit 1; }
until grep -q "chain: m4c" results/CHAIN_STATUS.md && grep -qE "state: \*\*(DONE|FAILED)" results/CHAIN_STATUS.md; do
  st WAITING "for the M4c chain to finish"; sleep 600; done
for day in $(seq 1 6); do
  st RUNNING "drafting, quota day $day"
  $PY -u scripts/k_annotation.py draft >> "$LOG" 2>&1; code=$?
  [ $code = 0 ] && break
  [ $code = 3 ] || fail "draft exited $code"
  [ "$day" = 6 ] && fail "drafts incomplete after 6 quota days"
  next="$(date -d tomorrow +%F)"
  until [ "$(date +%F)" = "$next" ] && [ "$(date +%H%M)" -ge 1245 ]; do st WAITING "Gemini quota (day $day); resumes $next 12:45 IST"; sleep 600; done
done
st RUNNING "building the annotation page"; $PY -u scripts/k_annotation.py page >> "$LOG" 2>&1 || fail "page exited $?"
st DONE "drafts complete, annotation/annotate_v1.html built at $(date '+%F %T %Z')"

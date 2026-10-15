#!/usr/bin/env bash
# M4c (natural romanization in M4): wait for the Gemini daily reset, romanize (retry every 30 min on quota stops,
# at most 12 tries), then the GPU forward pass and the analysis. Status in results/CHAIN_STATUS.md.
set -u
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
LOG=results/m4c_natural.log; STATUS=results/CHAIN_STATUS.md
st() { printf '# Chain status\n\n- state: **%s**\n- chain: m4c (natural romanization in M4)\n- heartbeat: %s\n- detail: %s\n' "$1" "$(date '+%F %T %Z')" "$2" > "$STATUS"; }
fail() { st FAILED "$1 at $(date '+%T'); see $LOG"; { echo; echo '```'; tail -n 30 "$LOG"; echo '```'; } >> "$STATUS"; exit 1; }
until [ "$(date +%H%M)" -ge 1245 ] && [ "$(date +%F)" = "$1" ]; do st WAITING "until $1 12:45 IST (Gemini reset)"; sleep 600; done
for i in $(seq 1 12); do
  st RUNNING "romanize try $i"
  $PY -u scripts/m4c_natural_flores.py romanize >> "$LOG" 2>&1 || fail "romanize exited $?"
  tail -1 "$LOG" | grep -q "'complete': True" && break
  [ "$i" = 12 ] && fail "romanize incomplete after 12 tries"
  st WAITING "Gemini quota (try $i); retry at $(date -d '+30 min' '+%T')"; sleep 1800
done
st RUNNING "forward pass (natural, 4 models)"; $PY -u scripts/m4c_natural_flores.py forward >> "$LOG" 2>&1 || fail "forward exited $?"
st RUNNING "analysis"; $PY -u scripts/m4c_natural_flores.py analyse >> "$LOG" 2>&1 || fail "analyse exited $?"
st DONE "m4c finished at $(date '+%F %T %Z')"

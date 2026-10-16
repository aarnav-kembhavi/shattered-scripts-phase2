# Shared helpers for the detached chains (source it after setting STATUS, TITLE and LOG).
# - The status file's mtime is the heartbeat: every waiting loop and every running step rewrites it at least every
#   5 minutes, so scripts/chain_watch.sh can mark a status DEAD when it is older than 20 minutes.
# - Dates are never hard-coded: quota waits compute the next 12:45 IST Gemini reset from the clock.
PY=.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
HB=120  # seconds between heartbeats

st() { printf '# %s\n\n- state: **%s**\n- heartbeat: %s\n- detail: %s\n- pid: %s (bash)\n' "$TITLE" "$1" \
  "$(date '+%F %T %Z')" "$2" "$$" > "$STATUS"; }
fail() { st FAILED "$1 at $(date '+%F %T'); see $LOG"; { echo; echo '```'; tail -n 30 "$LOG" | tr '\r' '\n' | tail -n 30; echo '```'; } >> "$STATUS"; exit 1; }

# run_hb "<label>" cmd args...  : run a step, heartbeat while it runs, return its exit code
run_hb() {
  local label=$1; shift
  echo "=== $(date '+%F %T') $label: $*" >> "$LOG"
  "$@" >> "$LOG" 2>&1 & local p=$!
  while kill -0 "$p" 2>/dev/null; do
    local last; last=$(tail -c 2000 "$LOG" | tr '\r' '\n' | grep -v '^\s*$' | tail -1 | cut -c1-150)
    st RUNNING "$label (last log line: ${last//|/ })"; sleep "$HB"
  done
  wait "$p"
}

next_reset() {  # epoch seconds of the next 12:45 IST (Gemini daily reset is about 12:30 IST)
  local t; t=$(date -d "today 12:45" +%s)
  [ "$(date +%s)" -ge "$t" ] && t=$(date -d "tomorrow 12:45" +%s)
  echo "$t"
}

wait_until() {  # wait_until <epoch> "<detail>"
  while [ "$(date +%s)" -lt "$1" ]; do st WAITING "$2 (until $(date -d "@$1" '+%F %T'))"; sleep "$HB"; done
}

state_of() { grep -o 'state: \*\*[A-Z]*' "$1" 2>/dev/null | sed 's/.*\*\*//'; }

py_alive() {  # py_alive <substring of a python command line>
  powershell -NoProfile -Command "if (Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*$1*' }) {exit 0} else {exit 1}"
}

free_gb() { powershell -NoProfile -Command "[math]::Floor((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB)"; }

wait_ram() {  # wait_ram <GB> : before any model load (RAM is the binding constraint)
  local f; f=$(free_gb | tr -d '\r')
  while [ "$f" -lt "$1" ]; do st WAITING "free RAM ${f} GB < $1 GB needed for a model load"; sleep "$HB"; f=$(free_gb | tr -d '\r'); done
}

# Shared helpers for the detached chains (source it after setting STATUS, TITLE and LOG).
# - The status file's mtime is the heartbeat: every waiting loop and every running step rewrites it at least every
#   5 minutes, so scripts/chain_watch.sh can mark a status DEAD when it is older than 20 minutes.
# - Dates are never hard-coded: quota waits compute the next 12:45 IST Gemini reset from the clock.
PY=.venv/Scripts/python.exe; export PYTHONIOENCODING=utf-8
HB=120  # seconds between heartbeats
# Tasks are also restarted at logon and on wake from sleep (scripts/detach.ps1): a chain that already finished exits.
grep -q 'state: \*\*DONE' "$STATUS" 2>/dev/null && exit 0

st() { printf '# %s\n\n- state: **%s**\n- heartbeat: %s\n- detail: %s\n- pid: %s (bash)\n' "$TITLE" "$1" \
  "$(date '+%F %T %Z')" "$2" "$$" > "$STATUS"; }
fail() { st FAILED "$1 at $(date '+%F %T'); see $LOG"; { echo; echo '```'; tail -n 30 "$LOG" | tr '\r' '\n' | tail -n 30; echo '```'; } >> "$STATUS"; exit 1; }

# run_hb "<label>" cmd args...  : run a step, heartbeat while it runs, return its exit code
run_hb() {
  local label=$1; shift
  echo "=== $(date '+%F %T') $label: $*" >> "$LOG"
  "$@" >> "$LOG" 2>&1 & local p=$!
  while kill -0 "$p" 2>/dev/null; do
    local last; last=$(tail -c 2000 "$LOG" | tr '\r' '\n' | grep -av '^\s*$' | tail -1 | cut -c1-150)
    st RUNNING "$label (last log line: ${last//|/ })"; sleep "$HB"
  done
  wait "$p"
}

# ---- network outages (rule of 2026-10-28, Aarnav): never a FAILED marker, never a stop for downstream chains.
# net_ok: any HTTP answer from the Gemini endpoint counts as "network up" (override NET_CHECK_CMD in tests).
NET_BASE=${NET_BASE:-60}; NET_CAP=${NET_CAP:-1800}; NET_MAX=${NET_MAX:-48}
NET_SIG='getaddrinfo failed|ConnectError|ConnectTimeout|ReadTimeout|RemoteProtocolError|ConnectionError|name resolution|Network is unreachable|Connection reset|Connection aborted'
net_ok() { if [ -n "${NET_CHECK_CMD:-}" ]; then eval "$NET_CHECK_CMD"; else curl -s -o /dev/null --max-time 10 https://generativelanguage.googleapis.com/; fi; }

# run_net "<label>" cmd args... : run_hb; if the step failed with a network signature in its new log lines (or the network
# is down), wait with exponential backoff (NET_BASE, doubling, capped at NET_CAP) until the network answers, then re-run
# the step (steps resume from their caches). Returns the step's exit code for success (0), quota (3) and any other failure;
# only NET_MAX consecutive network retries return 99. The caller never sees a FAILED marker for an outage.
run_net() {
  local label=$1 try=0 off code delay; shift
  while :; do
    off=$(stat -c %s "$LOG" 2>/dev/null || echo 0)
    run_hb "$label" "$@"; code=$?
    [ $code = 0 ] || [ $code = 3 ] && return $code
    if tail -c +$((off + 1)) "$LOG" 2>/dev/null | tr '' '
' | grep -aqE "$NET_SIG" || ! net_ok; then
      try=$((try + 1))
      [ "$try" -gt "$NET_MAX" ] && { echo "$(date '+%F %T') run_net: $label still failing on the network after $NET_MAX retries" >> "$LOG"; return 99; }
      delay=$(( NET_BASE * 2 ** (try - 1) )); [ "$delay" -gt "$NET_CAP" ] && delay=$NET_CAP
      echo "$(date '+%F %T') run_net: network failure in '$label' (exit $code), retry $try in ${delay}s" >> "$LOG"
      local until=$(( $(date +%s) + delay ))
      while [ "$(date +%s)" -lt "$until" ]; do st WAITING "network outage in '$label': retry $try in $(( until - $(date +%s) )) s (backoff)"; sleep "$(( HB < until - $(date +%s) ? HB : 1 ))"; done
      while ! net_ok; do st WAITING "network outage in '$label': waiting for the network (retry $try)"; sleep "$HB"; done
    else
      return $code
    fi
  done
}

# upstream_dead <state>: true only when the upstream chain has been FAILED or DEAD for GRACE seconds without recovering
# (the scheduler restarts a chain at logon or wake, so a FAILED seen for a moment is not a stop). Caller keeps one
# upstream per call site (the timer is a shell variable).
GRACE=${GRACE:-1800}; _bad_since=
upstream_dead() {
  case "$1" in
    FAILED|DEAD) [ -z "$_bad_since" ] && _bad_since=$(date +%s); [ $(( $(date +%s) - _bad_since )) -ge "$GRACE" ] ;;
    *) _bad_since=; return 1 ;;
  esac
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

gpu_used_mb() { nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1 | tr -d '\r '; }

wait_gpu() {  # before every model load (rule of 2026-10-23): total GPU memory in use must be <= 500 MB (under WDDM
  # nvidia-smi has no per-process memory, so anything above the desktop baseline is another process); retry every 5 min
  local u; u=$(gpu_used_mb)
  while [ -z "$u" ] || [ "$u" -gt 500 ]; do
    local apps; apps=$(nvidia-smi --query-compute-apps=pid,process_name --format=csv,noheader | tr '\r\n' '  ')
    echo "$(date '+%F %T') wait_gpu: ${u:-?} MB in use > 500 MB; GPU processes: $apps" >> "$LOG"
    st WAITING "GPU busy: ${u:-?} MB in use by another process (> 500 MB); retry in 5 min"
    sleep 300; u=$(gpu_used_mb)
  done
}

wait_h1lf() {  # standing rule (Aarnav, 2026-10-26): once the H1-LF SIB-1004 drafts are complete, H1-LF scoring goes
  # ahead of everything queued. Call before every model load of any other chain; it never interrupts a running model.
  while [ -f results/h1lf/sib1004_drafts.DONE ]; do
    local s; s=$(state_of results/CHAIN_STATUS_H1LF.md)
    case "$s" in DONE) return 0 ;; esac
    upstream_dead "$s" && return 0
    st WAITING "H1-LF scoring has priority (H1-LF chain: ${s:-no status}); waiting before the next model load"
    sleep 120
  done
}

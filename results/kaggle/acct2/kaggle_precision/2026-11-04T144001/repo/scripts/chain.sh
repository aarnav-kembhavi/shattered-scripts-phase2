#!/usr/bin/env bash
# Resumable pipeline with a loud status file (results/CHAIN_STATUS.md).
#   bash scripts/chain.sh <from_step> <to_step>
# Steps, in order: natural (finish natural romanization + retries; waits on the Gemini daily quota), gate1 (E0b, all
# five forms), m14 (full M1/M4 run), backtranslate (Groq back-translation + native control; stops on its daily limit).
# Every step is idempotent: finished pieces are skipped (API cache, per-(model, form) score files, per-(model, form)
# activations/results written atomically), so resuming never redoes finished work or re-spends API quota.
# On any failure the step, time, exit code and the end of the step's log go to CHAIN_STATUS.md and the chain stops.
# If the process is killed outright (e.g. the Claude Code session ends) nothing can be written: a heartbeat older
# than 40 minutes with state RUNNING/WAITING therefore means the chain is dead.
set -u
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python.exe
export PYTHONIOENCODING=utf-8
STATUS=results/CHAIN_STATUS.md
STEPS=(natural gate1 m14 backtranslate)
FROM=${1:-natural}; TO=${2:-backtranslate}
STEP=none; LOG=none; STARTED=$(date '+%F %T %Z')

status() {  # state, detail
  {
    echo "# Chain status"
    echo
    echo "- state: **$1**"
    echo "- steps requested: $FROM -> $TO"
    echo "- current step: $STEP (log: $LOG)"
    echo "- chain started: $STARTED"
    echo "- heartbeat: $(date '+%F %T %Z')"
    echo "- detail: $2"
    echo
    echo "A heartbeat older than 40 minutes with state RUNNING or WAITING means the chain died without a trace."
  } > "$STATUS.partial" && mv "$STATUS.partial" "$STATUS"
}

fail() {  # exit code
  status FAILED "step '$STEP' exited with code $1 at $(date '+%F %T %Z'). End of its log:"
  { echo; echo '```'; tail -n 30 "$LOG" 2>/dev/null; echo '```'; } >> "$STATUS"
  echo "FAILED step=$STEP code=$1"
  exit 1
}

trap 'status FAILED "chain interrupted by a signal during step $STEP"; exit 1' INT TERM HUP

run_natural() {
  LOG=results/e0b_natural_day2.log
  for i in $(seq 1 28); do
    status RUNNING "natural romanization, try $i"
    $PY -u scripts/e0b_natural.py >> "$LOG" 2>&1 || fail $?
    if tail -1 "$LOG" | grep -q "'complete': True"; then return 0; fi
    if ! tail -1 "$LOG" | grep -q "RESOURCE_EXHAUSTED\|daily"; then fail "incomplete-without-quota-stop"; fi
    [ "$i" = 28 ] && fail "quota-not-reset-after-28-tries"
    status WAITING "Gemini daily quota exhausted (try $i); next try at $(date -d '+30 min' '+%T')"
    sleep 1800
  done
}

run_gate1() {
  LOG=results/e0b_familiarity/gate1.log
  status RUNNING "E0b scoring, all five forms (only the natural form is new)"
  $PY -u scripts/e0b_familiarity.py --models qwen2.5-1.5b qwen3.5-2b sarvam-1 gemma4-e2b qwen3-1.7b \
      --tag gate1 > "$LOG" 2>&1 || fail $?
}

run_m14() {
  LOG=results/m14_full/run.log
  status RUNNING "full M1/M4 run (4 models x 3 forms; resumes per model and form)"
  $PY -u scripts/m14_full.py --models qwen2.5-1.5b qwen3.5-2b sarvam-1 gemma4-e2b >> "$LOG" 2>&1 || fail $?
}

run_backtranslate() {
  LOG=results/e0b_backtranslate.log
  status RUNNING "back-translation of new texts, then native control"
  $PY -u scripts/e0b_backtranslate.py > "$LOG" 2>&1 || fail $?
  LOG=results/e0b_backtranslate_control.log
  $PY -u scripts/e0b_backtranslate_control.py > "$LOG" 2>&1 || fail $?
}

active=0
for s in "${STEPS[@]}"; do
  [ "$s" = "$FROM" ] && active=1
  if [ $active = 1 ]; then
    STEP=$s
    "run_$s"
    echo "STEP_DONE $s $(date '+%F %T')"
  fi
  [ "$s" = "$TO" ] && break
done
STEP=none; LOG=none
status DONE "steps $FROM -> $TO finished at $(date '+%F %T %Z')"
echo "CHAIN_DONE"

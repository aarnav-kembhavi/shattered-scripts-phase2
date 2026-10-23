#!/usr/bin/env bash
# H1-LF option 1 (registered 2026-10-23 15:44 IST): natural drafts for all 1,004 SIB items in both languages, then the
# counted accuracy models on natural SIB 1,004 (GPU, one model load at a time). Gemini queue: waits until the Hindi
# drafts + K3b chain is DONE (stops if it FAILED or is DEAD); K3b-hi waits for this chain's drafts marker.
# The loan-free analysis (h1lf.py analyse1) is NOT run here: held for Aarnav's decision on the English-word definition
# (2026-10-23: the Zipf >= 3 list matches native Hindi words such as "mein"). Run detached:
# scripts/detach.ps1 -Name h1lf -Script scripts/h1lf_chain.sh. Status in results/CHAIN_STATUS_H1LF.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_H1LF.md; TITLE="H1-LF option 1 chain status"; LOG=results/h1lf.log
. scripts/chainlib.sh
while :; do
  s=$(state_of results/CHAIN_STATUS_HDRAFTS.md)
  [ "$s" = DONE ] && break
  case "$s" in FAILED|DEAD) fail "Hindi drafts + K3b chain is $s; H1-LF drafts not started" ;; esac
  st WAITING "queued behind the Hindi drafts + K3b chain (state: ${s:-none})"; sleep "$HB"
done
for i in $(seq 0 8); do
  run_hb "SIB-1004 natural drafts (after $i quota resets)" $PY -u scripts/h1lf.py draft; code=$?
  [ $code = 0 ] && break
  [ $code = 3 ] || fail "SIB-1004 drafts exited $code"
  [ "$i" = 8 ] && fail "SIB-1004 drafts incomplete after 8 quota resets"
  wait_until "$(next_reset)" "SIB-1004 drafts: Gemini quota stop; resume after the next reset"
done
[ -f results/h1lf/sib1004_drafts.DONE ] || fail "SIB-1004 drafts finished without the DONE marker"
for m in qwen3-1.7b qwen3.5-2b sarvam-1 gemma4-e2b; do for lg in kannada hindi; do  # one process per model load
  wait_ram 8; wait_gpu
  run_hb "scoring natural SIB 1,004, $m $lg" $PY -u scripts/h1lf.py score $m $lg || fail "score $m $lg exited $?"
done; done
run_hb "scoring checks (rows, reproduction)" $PY -u scripts/h1lf.py score check || fail "score check exited $?"
st DONE "drafts and scores finished at $(date '+%F %T %Z'); analyse1 held for Aarnav (English-word definition)"

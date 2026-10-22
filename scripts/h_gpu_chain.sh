#!/usr/bin/env bash
# H-Hindi GPU chain (registered 2026-10-23). Run detached: scripts/detach.ps1 -Name hgpu -Script scripts/h_gpu_chain.sh.
# Data check, then native/ITRANS/lossy vectors and scores (5 models, one model load at a time), tokens per word and
# the baseline gate; then waits for the Hindi natural drafts (scripts/h_drafts_chain.sh), runs natural vectors and
# scores, and the H1 analysis. Any failed check stops the chain with FAILED. Steps resume from their caches.
# Status in results/CHAIN_STATUS_HGPU.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_HGPU.md; TITLE="H-Hindi GPU chain status"; LOG=results/h_gpu.log
. scripts/chainlib.sh
run_hb "data check" $PY -u scripts/h_hindi.py check || fail "data check failed (exit $?)"
wait_ram 8
run_hb "forward native/itrans/lossy (5 models)" $PY -u scripts/h_hindi.py forward || fail "forward exited $?"
wait_ram 8
run_hb "scoring native/itrans/lossy (5 models)" $PY -u scripts/h_hindi.py score || fail "score exited $?"
run_hb "tokens per word" $PY -u scripts/h_hindi.py tpw || fail "tpw exited $?"
run_hb "baseline gate" $PY -u scripts/h_hindi.py gate || fail "gate exited $?"
while [ ! -f results/h_hindi/natural_drafts.DONE ]; do
  s=$(state_of results/CHAIN_STATUS_HDRAFTS.md)
  [ "$s" = FAILED ] && fail "the Hindi drafts chain FAILED"
  st WAITING "gate done; waiting for the Hindi natural drafts (drafts chain: ${s:-none})"; sleep "$HB"
done
wait_ram 8
run_hb "forward natural (5 models)" $PY -u scripts/h_hindi.py forward natural || fail "natural forward exited $?"
wait_ram 8
run_hb "scoring natural (5 models)" $PY -u scripts/h_hindi.py score natural || fail "natural score exited $?"
run_hb "tokens per word (with natural)" $PY -u scripts/h_hindi.py tpw || fail "tpw exited $?"
run_hb "H1 analysis" $PY -u scripts/h_hindi.py analyse || fail "analyse exited $?"
st DONE "H-Hindi finished at $(date '+%F %T %Z'); results/h_hindi/"

#!/usr/bin/env bash
# V-VER (exploratory, registered 2026-10-26 03:15 IST), queued after EP-R (Aarnav, 2026-10-26): waits for
# results/CHAIN_STATUS_EPR.md to be DONE (stops if it FAILED or is DEAD). Sentiment scored in full; SIB-257 and retrieval
# recompute only the items whose verified text differs (+ controls) and splice them into the stored results. Before every
# model load: RAM and GPU checks and the H1-LF priority rule (wait_h1lf). The K1/K2 pilot is NOT run here (waits for
# Aarnav's OK on the implementation details). Run detached: scripts/detach.ps1 -Name vver -Script scripts/vver_chain.sh.
# Status in results/CHAIN_STATUS_VVER.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_VVER.md; TITLE="V-VER chain status"; LOG=results/vver.log
. scripts/chainlib.sh
while :; do
  s=$(state_of results/CHAIN_STATUS_EPR.md)
  [ "$s" = DONE ] && break
  case "$s" in FAILED|DEAD) fail "EP-R chain is $s; not starting";; esac
  st WAITING "queued behind EP-R (EP-R: ${s:-no status})"
  sleep 120
done
for m in qwen3-1.7b qwen3.5-2b sarvam-1 gemma4-e2b; do
  wait_h1lf; wait_ram 8; wait_gpu
  run_hb "V-VER score (sentiment full, SIB changed + controls), $m" $PY -u scripts/v_ver.py score $m || fail "V-VER score $m exited $?"
done
for m in qwen3.5-2b sarvam-1 gemma4-e2b; do
  wait_h1lf; wait_ram 8; wait_gpu
  run_hb "V-VER retrieval vectors (changed + controls, spliced), $m" $PY -u scripts/v_ver.py forward $m || fail "V-VER forward $m exited $?"
done
run_hb "V-VER analysis" $PY -u scripts/v_ver.py analyse || fail "V-VER analyse exited $?"
st DONE "V-VER finished at $(date '+%F %T %Z'); results/v_ver/"

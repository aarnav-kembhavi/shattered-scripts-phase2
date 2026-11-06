#!/usr/bin/env bash
# Phase 2 X4: K3b-bn and K3b-te (Gemini vs Dakshina native-speaker romanization, the exact K3b design: 500 strings seed 6, resample subset 200 seed 7 at temperature 1.0; paid-tier Gemini cap raised on 2026-11-04).
# API and CPU only. Output: results/phase2/x4/k3b_bn, k3b_te.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x4k3b -Script scripts/x4k3b_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X4K3B.md; TITLE="Phase 2 X4 K3b chain status"; LOG=results/phase2/x4k3b.log
. scripts/chainlib.sh
mkdir -p results/phase2
for L in bn te; do
  run_hb "K3b-$L sample" env PYTHONPATH=src $PY -u scripts/k3b_dakshina.py sample $L || fail "k3b sample $L exited $?"
  while :; do
    run_net "K3b-$L drafts" env PYTHONPATH=src $PY -u scripts/k3b_dakshina.py draft $L; c=$?
    [ $c = 0 ] && break
    [ $c = 3 ] || fail "k3b draft $L exited $c"
    wait_until "$(next_reset)" "K3b-$L: daily Gemini cap reached, waiting for the reset"
  done
  run_hb "K3b-$L analysis" env PYTHONPATH=src $PY -u scripts/k3b_dakshina.py analyse $L || fail "k3b analyse $L exited $?"
done
st DONE "X4 K3b-bn and K3b-te finished at $(date '+%F %T %Z'); results/phase2/x4/k3b_{bn,te}/verdict.json"

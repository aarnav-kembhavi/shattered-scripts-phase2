#!/usr/bin/env bash
# Phase 2 laptop queue: X9a-low (registered 2026-11-04, tag phase2-x9a-low; exploratory, motivated by the X9a-R ceiling): exposure levels 0.01, 0.03, 0.1, 0.3 percent x 3 seeds = 12 runs, then the
# level-0 digit/punctuation-stripped retrieval (descriptive) and the registered rule. Waits for the status files in WAIT_FOR (default: X10 full). Run detached:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x9alow -Script scripts/x9alow_chain.sh
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X9ALOW.md; TITLE="Phase 2 X9a-low chain status"; LOG=results/phase2/x9alow.log
. scripts/chainlib.sh
mkdir -p results/phase2
for f in ${WAIT_FOR:-results/CHAIN_STATUS_X10.md}; do until [ "$(state_of $f)" = DONE ]; do st WAITING "X9a-low waits for $f"; sleep "$HB"; done; done
[ -f data/processed/x9a/meta_low.json ] || { wait_ram 8; run_hb "X9a-low prep (CPU)" env PYTHONPATH=src $PY -u scripts/x9a.py prep_low || fail "x9a prep_low exited $?"; }
for s in 0 1 2; do
  for p in 0p01 0p03 0p1 0p3; do
    [ -f results/phase2/x9a/x9a_p${p}_s${s}.json ] && continue
    wait_ram 8; wait_gpu
    run_hb "X9a-low level ${p} seed ${s}" env PYTHONPATH=src $PY -u scripts/x9a.py train $p $s || fail "x9a-low train $p $s exited $?"
  done
done
[ -f results/phase2/x9a/level0_stripped.json ] || { wait_gpu; run_hb "X9a level-0 stripped retrieval (descriptive)" env PYTHONPATH=src $PY -u scripts/x9a.py level0_stripped || fail "level0_stripped exited $?"; }
run_hb "X9a-low analysis (registered rule)" env PYTHONPATH=src $PY -u scripts/x9a.py analyse_low || fail "x9a analyse_low exited $?"
st DONE "X9a-low finished at $(date '+%F %T %Z'); results/phase2/x9a/analysis_low.json"

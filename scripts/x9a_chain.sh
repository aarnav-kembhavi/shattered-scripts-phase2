#!/usr/bin/env bash
# Phase 2 laptop queue: X9a full grid (5 exposure levels x 3 seeds = 15 runs, seed-major; each run resumable from its checkpoint, evaluated right after training). Registered in RESULTS.md (Amendment 2, X9a);
# the pilot (level 20, seed 0, 10 percent budget) passed first. Run detached:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/detach.ps1 -Name x9a -Script scripts/x9a_chain.sh
# Status in results/CHAIN_STATUS_X9A.md. No API calls. The decision rules (X9a-R, X9a-A) run in `scripts/x9a.py analyse` after the 15 runs.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X9A.md; TITLE="Phase 2 X9a chain status"; LOG=results/phase2/x9a.log
. scripts/chainlib.sh
mkdir -p results/phase2
for s in 0 1 2; do
  for p in 20 1 50 5 0; do
    [ -f results/phase2/x9a/x9a_p${p}_s${s}.json ] && continue
    wait_ram 8; wait_gpu
    run_hb "X9a level ${p} seed ${s}" env PYTHONPATH=src $PY -u scripts/x9a.py train $p $s || fail "x9a train $p $s exited $?"
  done
done
run_hb "X9a analysis (decision rules)" env PYTHONPATH=src $PY -u scripts/x9a.py analyse || fail "x9a analyse exited $?"
st DONE "X9a finished at $(date '+%F %T %Z'); results/phase2/x9a/analysis.json"

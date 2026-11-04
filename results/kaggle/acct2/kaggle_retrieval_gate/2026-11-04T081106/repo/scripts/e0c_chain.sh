#!/usr/bin/env bash
# E0c SIB-200: score (resumes from results/e0c_sib/scores/), then analyse. Run detached: scripts/detach.ps1 -Name e0c.
# Status in results/CHAIN_STATUS_E0C.md. The M4c forward step waits for this chain to finish (no two model loads).
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_E0C.md; TITLE="E0c chain status (SIB-200 scoring and analysis)"; LOG=results/e0c_sib_score.log
. scripts/chainlib.sh
wait_ram 8
run_hb "scoring (5 models x 4 forms, resumes from cache)" $PY -u scripts/e0c_sib.py score || fail "score exited $?"
run_hb "analysis" $PY -u scripts/e0c_sib.py analyse || fail "analyse exited $?"
st DONE "E0c finished at $(date '+%F %T %Z'); results/e0c_sib/gate/"

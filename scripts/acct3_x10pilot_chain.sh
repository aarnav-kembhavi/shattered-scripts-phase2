#!/usr/bin/env bash
# X10 for Sarvam-m (4-bit, registered), pilot on Kaggle account 3: 16 sentences, native and ITRANS, batch 8; timing only (no chrF used for any decision), cap 1.5 h.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X10PILOT3.md; TITLE="Sarvam-m X10 pilot (account 3)"; LOG=results/phase2/x10pilot3.log
. scripts/chainlib.sh
export KAGGLE_ACCOUNT=3
run_hb "Sarvam-m X10 pilot on Kaggle account 3" $PY -u scripts/kaggle_runner.py run kaggle_x10 --timeout-h 1.5 --private-data shattered-x10-inputs -- --models sarvam-m --n 16 --batch 8 --forms native itrans || fail "runner exited $?"
st DONE "Sarvam-m X10 pilot finished at $(date '+%F %T %Z')"

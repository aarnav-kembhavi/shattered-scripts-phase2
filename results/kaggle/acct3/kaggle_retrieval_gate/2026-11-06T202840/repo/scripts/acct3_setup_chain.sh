#!/usr/bin/env bash
# Account 3 (a teammate's account, user aarnavkembhavi, confirmed by its owner 2026-11-05): reproducibility smoke gate, then the A1-R retrieval reproduction (untrained base evaluation), both on Kaggle.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_ACCT3.md; TITLE="Account 3 setup chain status"; LOG=results/phase2/acct3_setup.log
. scripts/chainlib.sh
export KAGGLE_ACCOUNT=3
[ -f results/kaggle/acct3/kaggle_gate/gate_passed.json ] || run_hb "account 3: smoke gate (kaggle_gate)" $PY -u scripts/kaggle_runner.py run kaggle_gate --timeout-h 0.5 || fail "kaggle_gate exited $?"
run_hb "account 3: A1-R retrieval reproduction (kaggle_retrieval_gate)" $PY -u scripts/kaggle_runner.py run kaggle_retrieval_gate --timeout-h 2.0 --private-data shattered-flores-private || fail "kaggle_retrieval_gate exited $?"
st DONE "Account 3 setup finished at $(date '+%F %T %Z')"

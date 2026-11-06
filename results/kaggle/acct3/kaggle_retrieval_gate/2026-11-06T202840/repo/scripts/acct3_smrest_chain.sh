#!/usr/bin/env bash
# Account 3 (teammate's account, confirmed 2026-11-05): X13 Sarvam-m, the forms the first kernel (account 2) did not reach: lossy, lowercase, natural (4-bit, SIB-200 only, cap 5 h). Waits for the account-3 acceptance.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_ACCT3SM.md; TITLE="Account 3 Sarvam-m chain status"; LOG=results/phase2/acct3_smrest.log
. scripts/chainlib.sh
export KAGGLE_ACCOUNT=3
until [ -f results/kaggle/acct3/ACCEPTED ]; do st WAITING "waiting for the account-3 acceptance"; sleep "$HB"; done
run_hb "account 3 Sarvam-m lossy/lower/natural" $PY -u scripts/kaggle_runner.py run x_score --timeout-h 5.0 --private-data shattered-flores-private --include results/e09_romanize/best_schemes.json -- --models sarvam-m --no-retrieval --quant 4bit --forms lossy lower natural || fail "x_score exited $?"
st DONE "Account 3 Sarvam-m finished at $(date '+%F %T %Z')"

#!/usr/bin/env bash
# X13 Sarvam-m, the three forms the first kernel did not reach (lossy, lowercase, natural), Kaggle account 2 (KAGGLE_ACCOUNT=2), 4-bit, SIB-200 only, cap 5 h. Fetches into results/kaggle/acct2/x_score/<stamp>/out/sarvam-m.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_SMREST.md; TITLE="Sarvam-m remaining forms chain status"; LOG=results/phase2/smrest.log
. scripts/chainlib.sh
export KAGGLE_ACCOUNT=2
run_hb "Sarvam-m lossy/lower/natural on Kaggle account 2" $PY -u scripts/kaggle_runner.py run x_score --timeout-h 5.0 --private-data shattered-flores-private --include results/e09_romanize/best_schemes.json -- --models sarvam-m --no-retrieval --quant 4bit --forms lossy lower natural || fail "runner exited $?"
st DONE "Sarvam-m remaining forms finished at $(date '+%F %T %Z')"

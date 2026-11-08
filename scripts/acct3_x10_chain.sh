#!/usr/bin/env bash
# X10 for Sarvam-m (4-bit), Kaggle account 3, native then ITRANS (the registered X10-P contrast), batch 16, one kernel per form (the kernel slug is shared, so sequential), cap 10.5 h each.
# Lowercase, lossy and natural are not run: at the pilot's 22 to 28 s per sentence the five forms would need about 30 h, the account has about 25 h (cut decided 2026-11-08, logged in RESULTS.md).
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X10SM.md; TITLE="Sarvam-m X10 (account 3)"; LOG=results/phase2/x10sm.log
. scripts/chainlib.sh
export KAGGLE_ACCOUNT=3
for f in native itrans; do
  d=$(ls -d results/kaggle/acct3/kaggle_x10/*/out/sarvam-m 2>/dev/null | while read x; do [ -f "$x/$f.json" ] && echo "$x"; done | tail -1)
  [ -n "$d" ] && continue
  run_hb "Sarvam-m X10 $f on Kaggle account 3" $PY -u scripts/kaggle_runner.py run kaggle_x10 --timeout-h 10.5 --private-data shattered-x10-inputs -- --models sarvam-m --forms $f --batch 16 || fail "runner exited $? ($f)"
done
st DONE "Sarvam-m X10 finished at $(date '+%F %T %Z')"

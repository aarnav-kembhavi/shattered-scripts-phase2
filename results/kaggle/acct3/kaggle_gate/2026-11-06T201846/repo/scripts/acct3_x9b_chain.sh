#!/usr/bin/env bash
# Account 3 (teammate's account, confirmed 2026-11-05): X9b extra seed (code seed 3 = seed 4 in the report): ITRANS and native in one kernel (about 6.6 h, with the in-kernel base-evaluation guard), then English in a second.
# After each fetch the finished run folders are copied next to the laptop's extra-seed runs so the laptop chain skips them. Waits for the account-3 acceptance (smoke gate and A1-R reproduction).
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_ACCT3X9B.md; TITLE="Account 3 X9b chain status"; LOG=results/phase2/acct3_x9b.log
. scripts/chainlib.sh
export KAGGLE_ACCOUNT=3
until [ -f results/kaggle/acct3/ACCEPTED ]; do st WAITING "waiting for the account-3 acceptance"; sleep "$HB"; done
LAP=results/kaggle/laptop_x9b/2026-11-05/out
push() {  # $1 timeout h; rest = runs
  local th=$1; shift
  run_hb "account 3 X9b: $*" $PY -u scripts/kaggle_runner.py run kaggle_x9b --timeout-h $th -- --mode full --base-eval sarvam-1 --runs "$@" || fail "kaggle_x9b $* exited $?"
  d=$(ls -d results/kaggle/acct3/kaggle_x9b/*/out | tail -1)
  for r in "$@"; do tag=$(echo $r | awk -F: '{print $1"+"$2"+s"$3}'); [ -f $d/$tag/done.json ] && { mkdir -p $LAP; rm -rf $LAP/$tag; cp -r $d/$tag $LAP/$tag; }; done
}
push 7.5 sarvam-1:itrans:3 sarvam-1:native:3
push 4.5 sarvam-1:english:3
st DONE "Account 3 X9b finished at $(date '+%F %T %Z')"

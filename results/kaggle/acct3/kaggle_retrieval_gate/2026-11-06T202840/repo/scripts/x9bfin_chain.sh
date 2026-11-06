#!/usr/bin/env bash
# X9b secondary arm (Qwen3.5-2B): finish the English run (retrieval and done.json) after the Kaggle cap hit; laptop GPU.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X9BFIN.md; TITLE="X9b Qwen English-run completion chain status"; LOG=results/phase2/x9bfin.log
. scripts/chainlib.sh
wait_ram 8; wait_gpu
run_hb "X9b Qwen3.5-2B English run: retrieval and done.json" env PYTHONPATH=src $PY -u scripts/x9b_finish_english.py || fail "x9b_finish_english exited $?"
st DONE "English run completed at $(date '+%F %T %Z')"

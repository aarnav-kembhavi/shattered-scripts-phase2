#!/usr/bin/env bash
# Regenerates the Hindi M4c sentence vectors (cache/activations/h_hindi, deleted on 2026-11-04 for disk space; regenerable) that X5 needs: native, ITRANS, lossy, then natural. GPU, laptop.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_X5HIN.md; TITLE="X5 Hindi vectors chain status"; LOG=results/phase2/x5hin.log
. scripts/chainlib.sh
wait_ram 8; wait_gpu
run_hb "Hindi M4c vectors (native, ITRANS, lossy)" env PYTHONPATH=src $PY -u scripts/h_hindi.py forward || fail "h_hindi forward exited $?"
wait_ram 8; wait_gpu
run_hb "Hindi M4c vectors (natural)" env PYTHONPATH=src $PY -u scripts/h_hindi.py forward natural || fail "h_hindi forward natural exited $?"
st DONE "Hindi vectors regenerated at $(date '+%F %T %Z')"

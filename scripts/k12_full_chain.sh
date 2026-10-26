#!/usr/bin/env bash
# K1/K2 full run (registered 2026-10-16; implementation notes 2026-10-26; pilot passed 2026-10-26; full run approved by
# Aarnav 2026-10-26). Scores the four forms on both tasks for the five E0b models (one model load each), then the K2b
# Kanglish-verified vectors for the four M4 models, then the analysis. One process per model load; RAM check, GPU guard
# and the H1-LF priority rule (wait_h1lf, which only applies once the H1-LF drafts are complete) before every load.
# Run detached: scripts/detach.ps1 -Name k12full -Script scripts/k12_full_chain.sh. Status: results/CHAIN_STATUS_K12FULL.md.
set -u
cd "$(dirname "$0")/.."
STATUS=results/CHAIN_STATUS_K12FULL.md; TITLE="K1/K2 full run chain status"; LOG=results/k12_full.log
. scripts/chainlib.sh
for m in qwen3.5-2b sarvam-1 gemma4-e2b qwen3-1.7b qwen2.5-1.5b; do
  wait_h1lf; wait_ram 8; wait_gpu
  run_hb "K1/K2 score, $m" $PY -u scripts/k_k12.py score $m || fail "K1/K2 score $m exited $?"
done
for m in qwen2.5-1.5b qwen3.5-2b sarvam-1 gemma4-e2b; do
  wait_h1lf; wait_ram 8; wait_gpu
  run_hb "K2b vectors, $m" $PY -u scripts/k_k12.py forward $m || fail "K2b vectors $m exited $?"
done
run_hb "K1/K2 analysis" $PY -u scripts/k_k12.py analyse || fail "K1/K2 analyse exited $?"
st DONE "K1/K2 finished at $(date '+%F %T %Z'); results/k12/"

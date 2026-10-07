#!/usr/bin/env bash
# Wait until the E5 grid process (pid in results/e05_pretrain/grid.lock) exits, then run GPU jobs that must not
# share the 8 GB card with E5. Never touches E5 itself.
set -u
cd "$(dirname "$0")/.."
LOCK=results/e05_pretrain/grid.lock
PY=.venv/Scripts/python.exe
while [ -f "$LOCK" ] && "$PY" -c "import psutil,sys; sys.exit(0 if psutil.pid_exists(int(open('$LOCK').read() or 0)) else 1)"; do
  sleep 60
done
echo "E5 grid finished at $(date -u +%FT%TZ); starting E0"
PYTHONIOENCODING=utf-8 "$PY" -u scripts/e00_gate.py --models qwen3-1.7b qwen2.5-1.5b qwen3.5-2b sarvam-1 gemma4-e2b --device cuda
echo "E0 exit code $?"

#!/usr/bin/env bash
# Watcher for every chain status file (results/CHAIN_STATUS*.md). Run detached: scripts/detach.ps1 -Name watch.
# Chains rewrite their status at least every 5 minutes (scripts/chainlib.sh), so a RUNNING or WAITING status whose
# file is older than 20 minutes belongs to a dead chain: it is rewritten to DEAD (a chain that was only suspended, e.g.
# by laptop sleep, overwrites DEAD with its next heartbeat). Exits when no status is RUNNING or WAITING.
cd "$(dirname "$0")/.."
LOG=results/chain_watch.log
while :; do
  live=0
  for f in results/CHAIN_STATUS*.md; do
    grep -qE 'state: \*\*(RUNNING|WAITING)' "$f" || continue
    age=$(( $(date +%s) - $(stat -c %Y "$f") ))
    if [ "$age" -gt 1200 ]; then
      sed -i "s|^- state: .*|- state: **DEAD** (no heartbeat for $((age / 60)) min; marked by chain_watch.sh at $(date '+%F %T %Z'))|" "$f"
      echo "$(date '+%F %T') $f marked DEAD (heartbeat age ${age}s)" >> "$LOG"
    else
      live=1
    fi
  done
  [ "$live" = 0 ] && { echo "$(date '+%F %T') no live chain; watcher exits" >> "$LOG"; exit 0; }
  sleep 300
done

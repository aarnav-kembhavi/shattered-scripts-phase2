#!/usr/bin/env bash
# Trivial job to test scripts/detach.ps1: writes a heartbeat line every 20 s for 5 minutes.
cd "$(dirname "$0")/.."
for i in $(seq 1 15); do echo "$(date '+%F %T') tick $i pid $$ ppid $PPID" >> results/detach_test.log; sleep 20; done
echo "$(date '+%F %T') finished" >> results/detach_test.log

#!/usr/bin/env bash
# X10 full run (waits for X11); wrapper because detach.ps1 cannot set MODE.
cd "$(dirname "$0")/.."
MODE=full exec bash scripts/x10_chain.sh

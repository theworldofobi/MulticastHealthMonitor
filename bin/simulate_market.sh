#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

# USE --drop TO SIMULATE PACKET DROPS
DROP_FLAG=""
if [[ "${1:-}" == "-drop" ]]; then
  DROP_FLAG="--drop-every 20"
  echo "Simulating 5% packet loss"
fi

python -m src.monitor & 
MONITOR_PID=$!
echo "Monitor PID: $MONITOR_PID"

sleep 1

python -m src.sender $DROP_FLAG

trap "kill $MONITOR_PID 2>/dev/null" EXIT

#!/bin/bash
#
# Bench multiple values of the threshold, from $1 to $2
#
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo "=== Starting loop from T=$1 to T=$2 ==="

for ((i = $1; i <= $2; i++)); do
  echo "=> Setting T=$i"
  "$CURRENT_PATH"/../machines-setup/python_scripts/configure_scheduler.sh $i
  sleep 30
  echo "=> Starting test with T=$i"
  "$CURRENT_PATH"/bench_multi_machine_f-pigo-f.sh
  sleep 300
done

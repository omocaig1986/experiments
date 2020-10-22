#!/bin/bash
#
# Bench multiple values of the threshold, from $1 to $2
#
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo "=== Starting loop from tau=$1 to tau=$2, delta_tau=$3, T=$4 ==="

for ((tau = $1; tau <= $2; tau = tau + $3)); do
  echo "=> Setting tau=$tau"
  "$CURRENT_PATH"/../machines-setup/python_scripts/configure_pwr_n_tau_scheduler.sh "$4" "${tau}ms"
  sleep 15
  echo "=> Starting test with tau=$tau"
  "$CURRENT_PATH"/bench_multi_machine_f-pigo.sh
  sleep 60
done

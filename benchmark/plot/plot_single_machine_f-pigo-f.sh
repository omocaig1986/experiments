#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

K=10
T=1
FUNCTION_NAME="PigoFaceDetectF"
SERVER_DIR="BladeServers"
ALGORITHM="RR(K=$K)/_bench_multi_machine-11112019-152823"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/../env/bin/activate
"$CURRENT_PATH"/../env/bin/python plot_times.py --files-prefix "results-machine-" \
  --files-n "1" \
  --path "$CURRENT_PATH/../../../experiments-data/$SERVER_DIR/$FUNCTION_NAME/$ALGORITHM" \
  --function "Pigo Face Detect (F)" \
  --fanout "1" \
  --job-duration "0.30" \
  -k $K \
  --algorithm "NS(K)" \
  --threshold $T

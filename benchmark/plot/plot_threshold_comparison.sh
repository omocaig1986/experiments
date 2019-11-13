#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
FUNCTION_NAME="PigoFaceDetectF"
SERVER_DIR="BladeServers"
REQUESTS="20000reqs"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate

f=1

python plot_threshold_comparison.py \
  --path "/Users/gabrielepmattia/Coding/p2p-faas/experiments-data/$SERVER_DIR/$FUNCTION_NAME/LL-PS($f,K)/$REQUESTS/_8machines" \
  --function "Pigo Face Detect (F)" \
  --fanout $f \
  --from-threshold "0" \
  --to-threshold "10" \
  --job-duration "0.30" \
  -k "10" \
  --start-lambda "3.0" \
  --end-lambda "3.0" \
  --lambda-delta "0.1" \
  --n-machines "8"

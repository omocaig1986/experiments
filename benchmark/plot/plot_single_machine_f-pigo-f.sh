#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
FUNCTION_NAME="PigoFaceDetectF"
SERVER_DIR="BladeServers/debian"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate

k=10
T=1

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate
"$CURRENT_PATH"/env/bin/python plot_times.py --files-prefix "results-machine-" \
  --files-n "1" \
  --path "$CURRENT_PATH/../../experiments-data/$SERVER_DIR/$FUNCTION_NAME/NS(K=$k)" \
  --function "Pigo Face Detect (F)" \
  --fanout "1" \
  --job-duration "0.30" \
  --with-model \
  --model-name "M/M/1/$k" \
  -k $k \
  --algorithm "NS(K)" \
  --threshold $T

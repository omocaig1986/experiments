#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate

k=20
T=1

source "$CURRENT_PATH"/env/bin/activate
"$CURRENT_PATH"/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
  --files-n "1" \
  --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/BladeServers/debian/PigoFaceDetect/NS(K$k)" \
  --function "Pigo Face Detect" \
  --fanout "1" \
  --job-duration "0.275" \
  --with-model \
  --model-name "M/M/1/$k" \
  -k $k \
  --algorithm "NS(K)" \
  --threshold $T

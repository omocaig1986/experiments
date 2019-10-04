#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate
"$CURRENT_PATH"/env/bin/python bench_single_machine.py \
  --host "192.168.1.61:18080" \
  --function-url "function/pigo-face-detector-f" \
  --start-lambda "2.0" \
  --end-lambda "3.4" \
  --lambda-delta "0.1" \
  --requests "5000" \
  --poisson

#  -p "/Users/gabry3795/Coding/p2p-fog/experiments/benchmark/blobs/family.jpg" \
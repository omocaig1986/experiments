#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate

f=1

python plot_threshold_comparison.py \
  --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/Raspberries/PigoFaceDetect/LL-PS($f,K)/25000reqs/_5machines" \
  --function "Pigo Face Detect" \
  --fanout $f \
  --from-threshold "0" \
  --to-threshold "10" \
  --job-duration "0.77" \
  -k "10" \
  --start-lambda "5.40" \
  --end-lambda "5.40" \
  --lambda-delta "0.1" \
  --n-machines "5"

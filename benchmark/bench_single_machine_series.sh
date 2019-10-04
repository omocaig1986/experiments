#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate
"$CURRENT_PATH"/env/bin/python becn_single_machine_series.py \
  --host "192.168.99.100:18080" \
  --function "function/pigo-face-detector" \
  --payload "$CURRENT_PATH/blobs/family.jpg" \
  --requests "200"

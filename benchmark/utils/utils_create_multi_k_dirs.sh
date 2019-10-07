#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)/.."

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate
"$CURRENT_PATH"/env/bin/python utils_create_multi_k_dirs.py \
  --out-dir "/Users/gabrielepmattia/Coding/p2p-fog/experiments-data/BladeServers/PigoFaceDetectF/LL-PS(1,K)/2000reqs" \
  --machines-n "8" \
  --fanout "1" \
  --threshold-from "0" \
  --threshold-to "10" \
  --algorithm-name "LL-PS"

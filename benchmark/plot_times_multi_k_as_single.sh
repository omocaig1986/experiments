#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
FUNCTION_NAME="PigoFaceDetectF"
SERVER_DIR="BladeServers"
REQUESTS="20000reqs-3"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate

f=1

#!/bin/bash
for i in {0..10}; do

  "$CURRENT_PATH"/env/bin/python plot_times.py --files-prefix "results-machine-" \
    --files-n "8" \
    --path "/Users/gabrielepmattia/Coding/p2p-faas/experiments-data/$SERVER_DIR/$FUNCTION_NAME/LL-PS($f,K)/$REQUESTS/LL-PS($f,$i)-8machines" \
    --function "Pigo Face Detect (F)" \
    --fanout $f \
    --threshold $i \
    --job-duration "0.30" \
    --with-model \
    --model-name "M/M/1/10" \
    -k "10" \
    --algorithm "LL-PS(F,T)"
  # --plot-every-machine

done

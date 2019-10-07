#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)/.."

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate

f=1

#!/bin/bash
for i in {0..10}; do

  # source $CURRENT_PATH/env/bin/activate
  # $CURRENT_PATH/env/bin/python plot_times.py --files-prefix "results-machine-" \
  #
  python3 plot_times.py --files-prefix "results-machine-" \
    --files-n "5" \
    --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/Raspberries/PigoFaceDetect/LL-PS($f,K)/25000reqs/LL($f,K-$i)-5machines" \
    --function "Pigo Face Detect" \
    --fanout $f \
    --threshold $i \
    --job-duration "0.77" \
    --with-model \
    --model-name "M/M/1/10" \
    -k "10" \
    --algorithm "LL-PS(F,T)"
  # --plot-every-machine

done

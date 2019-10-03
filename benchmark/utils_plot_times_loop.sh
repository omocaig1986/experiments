#!/bin/sh
CURRENT_PATH=$(dirname $0)

f=1

#!/bin/bash
for i in {0..10}
do

    # source $CURRENT_PATH/env/bin/activate
    # $CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
    #
    python3 utils_plot_times.py --files-prefix "results-machine-" \
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
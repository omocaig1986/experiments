#!/bin/sh
CURRENT_PATH=$(dirname $0)
T=0

#!/bin/bash
for i in {0..9}
do

    source $CURRENT_PATH/env/bin/activate
    $CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
                            --files-n "8" \
                            --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/BladeServers/debian/PigoFaceDetect/MultiNode/25000reqs-2/LL(1,K-$i)-8machines" \
                            --function "Pigo Face Detect" \
                            --fanout "1" \
                            --threshold $i \
                            --job-duration "0.27" \
                            --with-model \
                            --model-name "M/M/1/10" \
                            -k "10"

done
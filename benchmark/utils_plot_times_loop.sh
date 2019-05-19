#!/bin/sh
CURRENT_PATH=$(dirname $0)

f=2

#!/bin/bash
for i in {0..10}
do

    source $CURRENT_PATH/env/bin/activate
    $CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
                            --files-n "8" \
                            --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/BladeServers/debian/PigoFaceDetect/LL(2,K)/25000reqs/LL($f,K-$i)-8machines" \
                            --function "Pigo Face Detect" \
                            --fanout $f \
                            --threshold $i \
                            --job-duration "0.28" \
                            --with-model \
                            --model-name "M/M/1/10" \
                            -k "10" \
                            --algorithm "LL-PS(F,T)"

done
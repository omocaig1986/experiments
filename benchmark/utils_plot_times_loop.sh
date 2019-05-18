#!/bin/sh
CURRENT_PATH=$(dirname $0)

f=1

#!/bin/bash
for i in {0..10}
do

    source $CURRENT_PATH/env/bin/activate
    $CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
                            --files-n "8" \
                            --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/BladeServers/debian/PigoFaceDetect/LL(1,K)/700reqs/LL($f,K-$i)-8machines" \
                            --function "Pigo Face Detect" \
                            --fanout $f \
                            --threshold $i \
                            --job-duration "0.301769" \
                            --with-model \
                            --model-name "M/M/1/10" \
                            -k "10"

done
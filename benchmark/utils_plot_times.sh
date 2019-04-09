#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
                        --files-n "8" \
                        --path "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Experiments/BladeServers/PigoFaceDetect/MultiNode/LL(1,K-3)-8machines" \
                        --function "Pigo Face Detect" \
                        --fanout "1" \
                        --threshold "3" \
                        --job-duration "0.274371" \
                        --with-model \
                        --model-name "M/M/1/10" \
                        -k "10"
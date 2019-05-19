#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_threshold_comparison.py \
                        --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/BladeServers/debian/PigoFaceDetect/LL(1,K)/700reqs/_8machines" \
                        --function "Pigo Face Detect" \
                        --fanout "1" \
                        --from-threshold "0" \
                        --to-threshold "10" \
                        --job-duration "0.27" \
                        -k "10" \
                        --start-lambda "1.0" \
                        --end-lambda "3.60" \
                        --lambda-delta "0.1"
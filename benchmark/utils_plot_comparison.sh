#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_comparison.py \
                        --path "/Users/gabry3795/Coding/p2p-fog/experiments-data/BladeServers/debian/PigoFaceDetect/MultiNode/25000reqs-2/_8machines" \
                        --function "Pigo Face Detect" \
                        --fanout "1" \
                        --from-threshold "1" \
                        --to-threshold "10" \
                        --job-duration "0.27" \
                        -k "10" \
                        --start-lambda "3.50" \
                        --end-lambda "3.50" \
                        --lambda-delta "0.05"
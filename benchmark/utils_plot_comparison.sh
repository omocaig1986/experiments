#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_comparison.py \
                        --path "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Experiments/BladeServers/PigoFaceDetect/MultiNode/_8machines" \
                        --function "Pigo Face Detect" \
                        --fanout "1" \
                        --from-threshold "1" \
                        --to-threshold "8" \
                        --job-duration "0.274371" \
                        -k "10" \
                        --start-lambda "0.1" \
                        --end-lambda "3.80" \
                        --lambda-delta "0.05"
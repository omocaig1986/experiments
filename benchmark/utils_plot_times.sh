#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
                        --files-n "14" \
                        --path "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/MultiNode/Loop/LL(1,K-2)-16machines" \
                        --function "Pigo Face Detect" \
                        --fanout "15" \
                        --threshold "10" \
                        --job-duration "1.02" \
                        --with-model \
                        --model-name "M/M/1/10" \
                        -k "10"
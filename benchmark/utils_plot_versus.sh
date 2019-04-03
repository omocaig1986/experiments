#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_versus.py \
                                --first-file "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/SingleNode/Loop/NS(K10)/out.txt" \
                                --second-file "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/MultiNode/Loop/LL(1,K-2)-16machines/_computed/avg-results.txt" \
                                --first-title "NS(K10)" \
                                --second-title "LL(1,K-2)-16machines" \
                                --x-axis "λ" \
                                --model-name "M/M/1/10" \
                                --model-k "10" \
                                --model-job-len "1.02" \
                                --out-dir ${CURRENT_PATH}"/tmp"